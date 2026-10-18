"""Untimed correctness and repeated-build prerequisites for a frozen cohort."""
import argparse
import json
import os
from pathlib import Path
import shutil
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/daily-performance"))
from measure import digest, source_case

CASES = {"string-building": "trbnf0", "n-body": "trbnf4"}

READINESS_ROLES = ("previous", "native", "typerb-go", "pure-go")


def inspect_ir(text, case):
    match = re.search(r'function[^\n]*\$' + CASES[case] + r'\([^\n]*\) \{.*?\n\}', text, re.S)
    if not match:
        raise ValueError("Missing unchanged consumer in diagnostic IR")
    body = match.group(0)
    return {"sqrtCalls": body.count("call $sqrt("), "sqrtOperations": body.count("=d sqrt ")}


def expected_ir(case, role):
    primary = case == "n-body"
    return dict(sqrtCalls=int(primary and role == "previous"),
                sqrtOperations=int(primary and role == "native"))


def validate_ir(ir):
    for case in CASES:
        for role in ("previous", "native"):
            if ir[case][role] != expected_ir(case, role):
                raise ValueError(f"{case}/{role}: registered sqrt or control lowering differs")


def gc_stats(stderr, require_automatic=True):
    stats = {}
    for line in stderr.decode().splitlines():
        tag, key, value = line.split(",")
        if tag != "type-rb-native-gc-stat-v1" or key in stats or not value.isdigit():
            raise ValueError("Unexpected GC statistics")
        stats[key] = int(value)
    if (set(stats) != {"collections", "automatic-collections", "allocated-bytes", "reclaimed-bytes", "live-bytes", "peak-heap-bytes"}
            or stats["allocated-bytes"] != stats["reclaimed-bytes"] or stats["live-bytes"] != 0
            or stats["collections"] <= 0 or stats["allocated-bytes"] <= 0
            or (require_automatic and stats["automatic-collections"] <= 0)):
        raise ValueError("Incomplete collection or reclamation evidence")
    return stats


def validate_gc(rows):
    controls = {(r["case"], r["role"]): r for r in rows}
    for case in CASES:
        for role in ("native", "previous"):
            if "gc" not in controls[(case, role)]:
                raise ValueError("Missing readiness GC control")
            stats = controls[(case, role)]["gc"]
            encoded = "".join(f"type-rb-native-gc-stat-v1,{key},{value}\n" for key,value in stats.items()).encode()
            gc_stats(encoded, require_automatic=case == "string-building")
        if controls[(case, "native")]["gc"] != controls[(case, "previous")]["gc"]:
            raise ValueError(f"{case}: allocation or collection accounting changed")
    return {"unchangedCases": sorted(CASES)}


def backend_preflight(qbe, roles, suite):
    directory = ROOT / "tools/nbody-sqrt-evaluation"
    registration = json.loads((directory / "registration.json").read_text())
    proof_file = directory / "backend-compatibility.json"
    if digest(proof_file) != registration["backendCompatibilitySHA256"]:
        raise ValueError("Backend compatibility evidence differs")
    proof = json.loads(proof_file.read_text())
    if proof["status"] != "pass" or proof["sourceRevision"] != registration["comparison"]:
        raise ValueError("Backend compatibility source differs")
    receipt = json.loads((Path(qbe).parent / "build-info.json").read_text())
    if receipt["inputs"]["backend"] != registration["backend"] or receipt["binarySHA256"] != digest(qbe):
        raise ValueError("Built QBE identity differs")
    import hashlib
    expected = {}
    for case in suite["cases"]:
        source = (ROOT / case["source"]).read_text()
        if "replace" in case:
            source = source.replace(*case["replace"])
        for target in ("arm64_apple", "arm64", "amd64_sysv"):
            expected[(case["id"], target)] = hashlib.sha256(source.encode()).hexdigest()
    actual = {(row["case"], row["target"]): row for row in proof["rows"]}
    if len(proof["rows"]) != 48 or actual.keys() != expected.keys():
        raise ValueError("Backend compatibility matrix is incomplete")
    for key, row in actual.items():
        if not row["identical"] or row["sourceSHA256"] != expected[key]:
            raise ValueError("Accepted-code backend assembly differs")
    # Same-image prior Linux fixed points must survive the changed backend too.
    for role, identity in registration["priorLinuxCompilers"].items():
        binary = Path(roles[role]["path"])
        if {"sha256": digest(binary), "bytes": binary.stat().st_size} != identity:
            raise ValueError(f"{role}: prior Linux compiler fixed point changed")
    return proof


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--compilers", type=Path, required=True)
    parser.add_argument("--qbe", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    roles = json.loads(args.compilers.read_text())
    roles["pure-go"] = {"path": shutil.which("go")}
    suite = json.loads((ROOT / "tools/daily-performance/suite.json").read_text())
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("TYPE_RB_NATIVE_RUNTIME_")}
    env.update(GOFLAGS="-trimpath", GOMAXPROCS="1", LC_ALL="C")
    backend_proof = backend_preflight(args.qbe, roles, suite)
    rows = []
    commands = []

    def execute(command, cwd, timeout, stats=False):
        if len(commands) >= 36:
            raise ValueError("Readiness product execution cap exceeded")
        index = len(commands)
        commands.append({"command": command, "cwd": str(cwd), "timeoutSeconds": timeout, "status": "started", "gcStats": stats})
        (args.output / "commands.json").write_text(json.dumps(commands, indent=2) + "\n")
        run_env = dict(env, TYPE_RB_NATIVE_RUNTIME_STATS="1") if stats else env
        result = subprocess.run(command, cwd=cwd, env=run_env, capture_output=True, timeout=timeout)
        (args.output / f"command-{index:02d}.stdout").write_bytes(result.stdout)
        (args.output / f"command-{index:02d}.stderr").write_bytes(result.stderr)
        commands[-1].update(exitCode=result.returncode, status="pass" if result.returncode == 0 else "fail")
        (args.output / "commands.json").write_text(json.dumps(commands, indent=2) + "\n")
        result.check_returncode()
        return result

    try:
        for case in suite["cases"]:
            if case["id"] not in CASES:
                continue
            directory = args.output / case["id"]
            expected = source_case(case, directory)
            if "pureGoSource" in case:
                shutil.copyfile(ROOT / case["pureGoSource"], directory / "pure-go.go")
            for role, compiler in roles.items():
                if role not in READINESS_ROLES:
                    continue
                if role == "pure-go" and "pureGoSource" not in case:
                    continue
                if role == "baseline" and not case.get("frozenBaseline", True):
                    continue
                hashes = []
                stats = None
                for index in range(2):
                    output = directory / role / "program"
                    output.parent.mkdir(exist_ok=True)
                    output.unlink(missing_ok=True)
                    shutil.rmtree(directory / "build", ignore_errors=True)
                    if role == "pure-go":
                        command = [compiler["path"], "build", "-trimpath", "-o", str(output), str(directory / "pure-go.go")]
                    elif role == "typerb-go":
                        command = [compiler["path"], "build", "--compile", "--config", "trbconfig.jsonc", "--outfile", str(output)]
                    else:
                        command = [compiler["path"], "build", str(directory / "src/main.trb"), "--output", str(output),
                                   "--qbe", args.qbe, "--cc", "/usr/bin/cc", "--target", "linux-arm64-v0"]
                    build = execute(command, directory, 90)
                    if build.stderr:
                        raise ValueError(f"{case['id']}/{role}: build stderr: {build.stderr.decode(errors='replace')}")
                    with_stats = index == 1 and role in ("native", "previous")
                    run = execute([str(output), *case["args"]], directory, 30, stats=with_stats)
                    if with_stats:
                        stats = gc_stats(run.stderr, require_automatic=case["id"] == "string-building")
                    if run.stdout != expected or (run.stderr and not with_stats):
                        raise ValueError(f"{case['id']}/{role}: incorrect output")
                    hashes.append(digest(output))
                if len(set(hashes)) != 1:
                    raise ValueError(f"{case['id']}/{role}: repeated build identity differs")
                rows.append({"case": case["id"], "role": role, "sha256": hashes[0], "builds": 2, "outputs": 2, **({"gc": stats} if stats else {})})
                print(f"ready {case['id']} {role}", flush=True)
        if len(rows) != 8:
            raise ValueError("Incomplete readiness matrix")
        ir = {}
        for case in CASES:
            current = next(row for row in rows if row["case"] == case and row["role"] == "native")
            previous = next(row for row in rows if row["case"] == case and row["role"] == "previous")
            if case == "n-body" and current["sha256"] == previous["sha256"]:
                raise ValueError(f"{case}: primary application did not change")
            ir[case] = {}
            for role in ("previous", "native"):
                emitted = execute([roles[role]["path"], "emit-qbe", str(args.output / case / "src/main.trb")],
                                  args.output, 90)
                if emitted.stderr:
                    raise ValueError("Primary IR emission has stderr")
                (args.output / (role + "-" + case + ".ssa")).write_bytes(emitted.stdout)
                ir[case][role] = inspect_ir(emitted.stdout.decode(), case)
                if role == "previous":
                    expected_ir_hash = next(row["irSHA256"] for row in backend_proof["rows"]
                                            if row["case"] == case and row["target"] == "arm64")
                    if digest(args.output / (role + "-" + case + ".ssa")) != expected_ir_hash:
                        raise ValueError("Linux accepted IR differs from the backend compatibility proof")
        validate_ir(ir)
        if next(r for r in rows if r["case"] == "string-building" and r["role"] == "native")["sha256"] != next(r for r in rows if r["case"] == "string-building" and r["role"] == "previous")["sha256"]:
            raise ValueError("String-building control application changed")
        allocation = validate_gc(rows)
        if len(commands) != 36:
            raise ValueError("Incomplete readiness command budget")
        result = {"status": "pass", "rows": rows, "ir": ir, "allocation": allocation, "productExecutions": len(commands), "timingObservations": 0,
                  "goFlags": env["GOFLAGS"], "goVersion": subprocess.check_output(["go", "version"], text=True).strip()}
    except Exception as error:
        result = {"status": "fail", "rows": rows, "error": str(error), "productExecutions": len(commands), "timingObservations": 0}
        raise
    finally:
        (args.output / "readiness.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
