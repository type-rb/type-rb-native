"""Qualify one fixed guarded-successor candidate without writing daily state."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import re
import statistics
import subprocess
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools/daily-performance"))
from rss_policy import assess as assess_rss


ROOT = Path(__file__).resolve().parents[2]
SHA = re.compile(r"[0-9a-f]{40}")
DIGEST = re.compile(r"[0-9a-f]{64}")
ADJACENT = ("string-scanning", "string-building", "hash-string-keys", "enum-result", "closures")
METRICS = ("wallSeconds", "cpuSeconds", "memoryBytes")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(value).hexdigest()


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root)


def select_sources(root, registration):
    candidate, comparison = (registration[key] for key in ("candidate", "comparison"))
    require(all(isinstance(value, str) and SHA.fullmatch(value) for value in (candidate, comparison)),
            "Sources must be full lowercase commit SHAs")
    require(candidate != comparison, "Comparison must be a distinct earlier source")
    workflow = git(root, "rev-parse", "HEAD").decode().strip()
    accepted = git(root, "rev-parse", "origin/main").decode().strip()
    require(accepted == comparison, "Accepted main moved; registration is stale")
    for older, newer in ((comparison, candidate), (candidate, workflow)):
        require(git(root, "rev-parse", f"{older}^{{commit}}").decode().strip() == older,
                "Source is not an exact commit object")
        subprocess.run(["git", "merge-base", "--is-ancestor", older, newer], cwd=root, check=True)
    # The diagnostic commit may change tooling only; production stays fixed.
    for path in ("compiler", "TYPE_RB_REVISION", "tools/daily-performance", "benchmarks",
                 "tools/build-reference.py", "tools/bootstrap-seed-download.sh", "tools/bootstrap-seed-manifest.sh"):
        require(git(root, "rev-parse", f"{candidate}:{path}") ==
                git(root, "rev-parse", f"{workflow}:{path}"), "Registered production or measurement inputs are stale")
    blob = lambda revision, path: git(root, "show", f"{revision}:{path}")
    suite_bytes = blob(candidate, "tools/daily-performance/suite.json")
    require(digest(suite_bytes) == registration["suiteSha256"], "Registered suite changed")
    suite = json.loads(suite_bytes)
    require((suite["warmups"], suite["samples"], suite["timeoutSeconds"]) == (1, 5, 30),
            "Unexpected measurement budget")
    roles = {"native": candidate, "previous": comparison, "baseline": suite["baseline"],
             "typerb-go": blob(candidate, "TYPE_RB_REVISION").decode().strip(),
             "pure-go": suite["pureGoRevision"]}
    rows = []
    for case in suite["cases"]:
        for field in ("source", "expectedFile", "pureGoSource"):
            if field in case:
                require(blob(candidate, case[field]) == blob(accepted, case[field]),
                        "Registered workload inputs are stale")
        source = blob(candidate, case["source"])
        expected = (blob(candidate, case["expectedFile"]) if "expectedFile" in case
                    else case["expected"].encode())
        if case["id"] in ADJACENT:
            require(source == blob(comparison, case["source"]), "Adjacent workload changed")
            require(expected == blob(comparison, case["expectedFile"]), "Adjacent oracle changed")
        if "replace" in case:
            before, after = (value.encode() for value in case["replace"])
            require(source.count(before) == 1, "Workload replacement is not unique")
            source = source.replace(before, after)
        for role in roles:
            if role == "pure-go" and "pureGoSource" not in case:
                continue
            if role == "baseline" and not case.get("frozenBaseline", True):
                continue
            data = blob(candidate, case["pureGoSource"]) if role == "pure-go" else source
            rows.append({"case": case["id"], "role": role, "sourceSha256": digest(data),
                         "expectedSha256": digest(expected), "args": case["args"],
                         "gcProbe": bool(case.get("gcProbe") and role in ("native", "previous", "baseline"))})
    require(len(rows) == registration["rows"] == 67 and
            len(rows) * 10 + 4 == registration["timedObservations"] == 674,
            "Suite no longer matches the registered finite budget")
    require(set(ADJACENT) <= {row["case"] for row in rows}, "Missing registered adjacent workload")
    return {"registration": registration, "workflowRevision": workflow, "acceptedMain": accepted,
            "roles": roles, "rows": rows,
            "comparisonReference": blob(comparison, "TYPE_RB_REVISION").decode().strip(),
            "compilerSourceSha256": digest(blob(candidate, "compiler/src/compiler.trb")),
            "controllerSha256": {name: digest(blob(candidate, f"tools/daily-performance/{name}"))
                                 for name in ("prepare-compilers.sh", "measure.py", "state.py")}}


def number(value, positive=False):
    require(type(value) in (float, int) and math.isfinite(value) and
            (value > 0 if positive else value >= 0), "Invalid numeric observation")
    return value


def check_summary(summary, records):
    retained = [record for record in records if record["phase"] == "retained"]
    for metric in METRICS:
        require(number(summary[metric]) == statistics.median(record[metric] for record in retained),
                "Summary differs from retained observations")
    require(summary["wallMin"] == min(record["wallSeconds"] for record in retained) and
            summary["wallMax"] == max(record["wallSeconds"] for record in retained),
            "Summary range differs from retained observations")


def assess(selection, snapshot, raw):
    registration = selection["registration"]
    require(snapshot["revision"] == registration["candidate"] and snapshot["status"] == "measured",
            "Incomplete or different-source snapshot")
    require(snapshot["platform"] == "Linux arm64 / ubuntu-24.04-arm" and
            snapshot["samples"] == 5 and snapshot["buildSamples"] == 3, "Different measurement conditions")
    require(set(snapshot["roles"]) == set(selection["roles"]), "Different compiler roles")
    for role, revision in selection["roles"].items():
        identity = snapshot["roles"][role]
        require(identity["revision"] == revision and DIGEST.fullmatch(identity["sha256"]),
                "Compiler identity mismatch")
        number(identity["bytes"], positive=True)
    expected = {(row["case"], row["role"]): row for row in selection["rows"]}
    rows = {(row["case"], row["role"]): row for row in snapshot["rows"]}
    require(len(snapshot["rows"]) == len(expected) and rows.keys() == expected.keys(),
            "Missing, duplicated or unexpected case/role row")
    require(len(raw) == registration["timedObservations"], "Incomplete or exceeded finite budget")
    groups = defaultdict(list)
    for record in raw:
        require(record["status"] == "pass" and record["exitCode"] == 0, "Failed observation retained")
        for metric in METRICS:
            number(record[metric], positive=metric != "cpuSeconds")
        groups[(record["case"], record["role"], record["kind"])].append(record)
    counts = {"build": (1, 3, 90), "runtime": (1, 5, 30),
              "compiler-ir": (0, 1, 90), "compiler-self": (1, 2, 120)}
    expected_groups = {(case, role, kind) for case, role in expected for kind in ("build", "runtime")}
    expected_groups |= {("compiler-self", "native", kind) for kind in ("compiler-ir", "compiler-self")}
    require(groups.keys() == expected_groups, "Unexpected observation group")
    for (_, _, kind), records in groups.items():
        warmups, retained, timeout = counts[kind]
        phases = Counter(record["phase"] for record in records)
        require(phases == Counter({"warmup": warmups, "retained": retained}), "Different sample count")
        require(all(record["timeoutSeconds"] == timeout for record in records), "Different command bound")
    for key, row in rows.items():
        require(row["status"] == "pass", "Failed case/role row")
        for field in ("sourceSha256", "expectedSha256", "args"):
            require(row[field] == expected[key][field], "Different workload or oracle")
        require(DIGEST.fullmatch(row["artifactSha256"]), "Missing application identity")
        number(row["artifactBytes"], positive=True)
        number(row["strippedBytes"], positive=True)
        if expected[key]["gcProbe"]:
            require(row["coverage"] == "GC observed", "GC coverage unconfirmed")
        for kind in ("build", "runtime"):
            check_summary(row[kind], groups[(*key, kind)])
    compiler = snapshot["compilerSelf"]
    require(compiler["status"] == "pass" and compiler["sourceSha256"] == selection["compilerSourceSha256"] and
            compiler["binarySha256"] == snapshot["roles"]["native"]["sha256"] and
            compiler["binaryBytes"] == snapshot["roles"]["native"]["bytes"], "Compiler self-build identity mismatch")
    check_summary(compiler["build"], groups[("compiler-self", "native", "compiler-self")])
    ir = compiler["ir"]
    require(DIGEST.fullmatch(ir["sha256"]), "Missing compiler IR identity")
    number(ir["bytes"], positive=True)
    for metric in METRICS:
        require(number(ir[metric]) == groups[("compiler-self", "native", "compiler-ir")][0][metric],
                "Compiler IR summary differs from observation")
    # Every build must reproduce the exact executable that was timed.
    for key, row in rows.items():
        identities = {(record["artifact"]["sha256"], record["artifact"]["bytes"])
                      for record in groups[(*key, "build")]}
        require(identities == {(row["artifactSha256"], row["artifactBytes"])},
                "Repeated application build identity differs")
        require(all(record["artifact"]["sha256"] == row["artifactSha256"]
                    for record in groups[(*key, "runtime")]), "Runtime artifact differs")
    result = evaluate_trade(rows, groups)
    rss = assess_rss(snapshot["rows"], json.loads((ROOT / "tools/daily-performance/suite.json").read_text())["cases"])
    result["runtimeRSS"] = rss
    if rss["status"] != "met":
        result["status"] = "unmet" if result["failures"] or rss["status"] == "unmet" else "review-required"
        result["failures"].extend(rss["failures"])

    return {**result, "registration": registration,
            "workflowRevision": selection["workflowRevision"], "roles": snapshot["roles"],
            "rows": snapshot["rows"], "compilerSelf": compiler,
            "compilerCostScope": "Current-source self-build only; matched previous cost remains unmeasured",
            "adoption": False}


def evaluate_trade(rows, groups):
    failures, unknown, ratios = [], [], {}
    cases = sorted(case for case, role in rows if role == "native")
    def ratio(a, b, label):
        if a <= 0 or b <= 0:
            unknown.append(label)
            return None
        return a / b
    def limit(value, ceiling, label):
        if value is not None and value > ceiling:
            failures.append(label)
    for case in cases:
        current, previous = rows[(case, "native")], rows[(case, "previous")]
        result = ratios[case] = {}
        for kind in ("runtime", "build"):
            result[kind] = {}
            for metric in METRICS:
                label = f"{case}/{kind}/{metric}"
                value = ratio(current[kind][metric], previous[kind][metric], label)
                result[kind][metric] = value
                ceiling = 1.25 if kind == "build" and metric != "memoryBytes" else 1.05
                if (kind, metric) != ("runtime", "memoryBytes"):
                    limit(value, ceiling, label)
        limit(ratio(current["artifactBytes"], previous["artifactBytes"], case + "/bytes"), 1.05, case + "/bytes")
        for role in ("typerb-go", "pure-go"):
            if (case, role) not in rows:
                continue
            other = rows[(case, role)]["build"]["wallSeconds"]
            value = ratio(current["build"]["wallSeconds"], other, case + "/" + role)
            result["build"][role] = value
            if role == "typerb-go" and (value is None or value >= 1):
                failures.append(case + "/not-faster-build/typerb-go")
            if previous["build"]["wallSeconds"] < other:
                if value is None or value >= 1:
                    failures.append(case + "/lost-build-advantage/" + role)
            else:
                limit(result["build"]["wallSeconds"], 1.05, case + "/already-slower-build/" + role)
        result["buildWallAddedSeconds"] = current["build"]["wallSeconds"] - previous["build"]["wallSeconds"]
        result["runtimeWallSavedSeconds"] = previous["runtime"]["wallSeconds"] - current["runtime"]["wallSeconds"]
        increased_cost = any(result["build"][metric] is not None and result["build"][metric] > 1.05
                             for metric in ("wallSeconds", "cpuSeconds"))
        if increased_cost and (case, "pure-go") not in rows:
            unknown.append(case + "/build-trade/missing-pure-go")
        elif increased_cost and result["build"].get("pure-go", 1) >= 1:
            failures.append(case + "/build-trade/not-faster-pure-go")
        for row_case, role in rows:
            if row_case != case:
                continue
            records = groups[(case, role, "runtime")]
            values = [r["wallSeconds"] for r in records if r["phase"] == "retained"]
            limit(max(r["wallSeconds"] for r in records) / statistics.median(values),
                  2, case + "/outlier/" + role)
    primary_gains, qualified_primaries, go_ratios, new_go_wins = {}, [], {}, []
    for case in ("allocation", "n-body", "fannkuch-redux"):
        require(all((case, role) in rows for role in ("native", "previous", "typerb-go")),
                "Missing registered near-win workload")
        current = rows[(case, "native")]["runtime"]
        previous = rows[(case, "previous")]["runtime"]
        comparator = rows[(case, "typerb-go")]["runtime"]["wallSeconds"]
        gain = previous["wallSeconds"] - current["wallSeconds"]
        primary_gains[case] = gain
        wall, cpu = (ratios[case]["runtime"][metric] for metric in ("wallSeconds", "cpuSeconds"))
        if wall is not None and wall <= .97 and cpu is not None and cpu < 1 and gain >= .001:
            qualified_primaries.append(case)
        go_ratio = ratio(current["wallSeconds"], comparator, case + "/runtime/typerb-go")
        previous_go_ratio = ratio(previous["wallSeconds"], comparator, case + "/previous-runtime/typerb-go")
        go_ratios[case] = {"native": go_ratio, "previous": previous_go_ratio}
        if go_ratio is not None and go_ratio <= .95 and previous_go_ratio is not None and previous_go_ratio > .95:
            new_go_wins.append(case)
    if not qualified_primaries:
        failures.append("near-wins/no-case-meets-3-percent-wall-positive-cpu-and-1-ms")
    if not new_go_wins:
        failures.append("near-wins/no-new-go-faster-case")
    return {"status": "unmet" if failures else "incomplete" if any("/build-trade/" in item for item in unknown) else "met",
            "failures": failures, "unknown": unknown, "ratios": ratios,
            "primaryWallSavedSeconds": primary_gains, "qualifiedPrimaries": qualified_primaries,
            "goRatios": go_ratios, "newGoWins": new_go_wins,
            "requestedOutcome": "met" if new_go_wins else "unmet",
            "missingComparators": [case for case in cases if (case, "pure-go") not in rows]}



def write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    select = commands.add_parser("select")
    select.add_argument("--registration", default=ROOT / "tools/guarded-successor-go-win/registration.json", type=Path)
    select.add_argument("--output", required=True)
    assessment = commands.add_parser("assess")
    for name in ("selection", "snapshot", "raw", "output"):
        assessment.add_argument(f"--{name}", required=True)
    args = parser.parse_args()
    read = lambda path: json.loads(Path(path).read_text())
    if args.command == "select":
        write(args.output, select_sources(ROOT, read(args.registration)))
        return 0
    try:
        result = assess(read(args.selection), read(args.snapshot), read(args.raw))
    except (ValueError, KeyError, TypeError, OSError) as error:
        # Preserve failed/missing observations as invalid, never as a passing snapshot.
        write(args.output, {"status": "invalid", "error": str(error)})
        return 1
    write(args.output, result)
    return 0 if result["status"] == "met" else 1


if __name__ == "__main__":
    raise SystemExit(main())
