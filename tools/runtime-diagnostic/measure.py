"""One registered hardware diagnostic, separate from acceptance and publication."""
import argparse
import json
import os
from pathlib import Path
import platform
import re
import shutil
import statistics
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "daily-performance"))
from measure import correct, digest, observe, source_case
from state import ROOT, git, read, write


def validate_registration(plan):
    if plan["cohortBudget"] != 1 or plan["firstSamples"] != 1 or plan["steadySamples"] != 5:
        raise ValueError("Expected one first execution and five steady executions")
    variants = plan["variants"]
    if not 2 <= len(variants) <= 4 or list(variants)[0] != "accepted":
        raise ValueError("Expected accepted source followed by bounded candidates")
    if plan["suiteSHA256"] != digest(ROOT / "tools/daily-performance/suite.json"):
        raise ValueError("Registered workload suite changed")
    if str(os.environ.get("GITHUB_RUN_ATTEMPT", "1")) != "1":
        raise ValueError("Do not retry a completed diagnostic cohort")
    suite = read(ROOT / "tools/daily-performance/suite.json")
    cases = {case["id"] for case in suite["cases"]}
    for role, variant in variants.items():
        if not re.fullmatch(r"[a-z][a-z0-9-]*", role):
            raise ValueError("Invalid role name")
        revision = variant["revision"]
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise ValueError("Each source revision must be exact")
        git("merge-base", "--is-ancestor", revision, "HEAD")
        if set(variant["appSHA256"]) != cases or any(
                not re.fullmatch(r"[0-9a-f]{64}", value)
                for value in variant["appSHA256"].values()):
            raise ValueError("Every Native application must have a fixed identity")
        # Changes to workload or reference inputs cannot masquerade as a
        # compiler comparison. Verify all public inputs before preparation.
        files = {"TYPE_RB_REVISION", "tools/daily-performance/suite.json"}
        for case in suite["cases"]:
            files.add(case["source"])
            files.update(case[key] for key in ("expectedFile", "pureGoSource") if key in case)
        for name in files:
            saved = subprocess.check_output(["git", "show", f"{revision}:{name}"], cwd=ROOT)
            if saved != (ROOT / name).read_bytes():
                raise ValueError(f"{role}: workload or reference differs: {name}")
    return suite


def summary(records):
    if len(records) != 6 or any(record["status"] != "pass" for record in records):
        return None
    steady = [record for record in records if record["phase"] == "steady"]
    if len(steady) != 5 or len([r for r in records if r["phase"] == "first"]) != 1:
        raise ValueError("Incomplete first/steady observation set")
    result = {key: statistics.median(row[key] for row in steady)
              for key in ("wallSeconds", "cpuSeconds", "memoryBytes")}
    result["steadyWallSpread"] = max(r["wallSeconds"] for r in steady) / min(r["wallSeconds"] for r in steady)
    result["allWallSpread"] = max(r["wallSeconds"] for r in records) / min(r["wallSeconds"] for r in records)
    result["cpuResolved"] = all(row["cpuSeconds"] > 0 for row in steady)
    return result


def run(args):
    plan = read(args.registration)
    suite = validate_registration(plan)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    evidence = output / "evidence"
    evidence.mkdir()
    write(evidence / "registration.json", plan)
    cpu = subprocess.check_output(["lscpu"]).decode()
    core = min(os.sched_getaffinity(0))
    write(evidence / "context.json", {
        "cpu": cpu, "platform": platform.platform(), "core": core,
        "controllerRevision": git("rev-parse", "HEAD"),
        "controllerSHA256": digest(__file__), "runId": os.environ.get("GITHUB_RUN_ID"),
        "scope": "Hardware diagnosis only; no acceptance or publication state changes",
        "firstExecution": "Retained independently; all-sample spread is also reported",
        "buildTiming": "One preparation observation, not a build performance claim",
        "seedSHA256": digest(args.seed), "referenceSHA256": digest(args.reference),
        "goVersion": subprocess.check_output(["go", "version"]).decode().strip(),
        "referenceRevision": (ROOT / "TYPE_RB_REVISION").read_text().strip(),
    })
    if platform.system() != "Linux" or platform.machine() != "aarch64" or "Neoverse-N2" not in cpu:
        raise ValueError("The registered comparison requires a Neoverse N2 runner")
    if digest(args.seed) != "3627fd8c574a668173ac6bb25eb41371c0f6cf0fa9da1016eebfc08b078d4060":
        raise ValueError("Published Native input seed differs")
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("TYPE_RB_NATIVE_RUNTIME_")}
    env.update(LC_ALL="C", GOMAXPROCS="1")
    raw, prepared = [], {}

    def record(command, directory, timeout, **metadata):
        item = observe(command, directory, timeout, env=env, core=core)
        item.update(metadata)
        raw.append(item)
        write(directory / "observation.json", item)
        write(evidence / "raw.json", raw)
        if item["status"] != "pass":
            raise ValueError(f"Command failed: {directory}")
        return item

    for role, variant in plan["variants"].items():
        print(f"Prepare {role} at {variant['revision']}", flush=True)
        source = output / "sources" / role
        source.parent.mkdir(exist_ok=True)
        subprocess.run(["git", "worktree", "add", "--detach", source, variant["revision"]],
                       cwd=ROOT, check=True)
        directory = evidence / "compilers" / role
        directory.mkdir(parents=True)
        qbe_root = output / "backends" / role
        record(["python3", source / "tools/qbe_toolchain.py", qbe_root],
               directory / "qbe-build", 120, kind="qbe-build", role=role)
        qbe = qbe_root / "qbe"
        shutil.copyfile(qbe_root / "build-info.json", directory / "qbe-build-info.json")
        compiler = args.seed
        generations = []
        for generation in range(4):
            generation_dir = directory / str(generation)
            generation_dir.mkdir()
            produced = generation_dir / "compiler"
            trace = generation_dir / "process.trace"
            record(["strace", "-f", "-e", "trace=process", "-o", trace,
                    compiler, "build", source / "compiler/src/compiler.trb",
                    "--output", produced, "--qbe", qbe, "--cc", "/usr/bin/cc",
                    "--target", "linux-arm64-v0"],
                   generation_dir / "build", 240, kind="ordinary-generation",
                   role=role, generation=generation)
            if re.search(r'execve\("[^"]*/(?:go|trb|sh|bash|zsh)"', trace.read_text()):
                raise ValueError("Unexpected host compiler or shell in ordinary build")
            if (generation_dir / "build/stdout").stat().st_size or (generation_dir / "build/stderr").stat().st_size:
                raise ValueError("Unexpected ordinary compiler output")
            generations.append({"sha256": digest(produced), "bytes": produced.stat().st_size})
            compiler = produced
        write(directory / "generations.json", generations)
        if generations[-1] != generations[-2]:
            raise ValueError("Ordinary compiler fixed point differs")
        prepared[role] = {"compiler": compiler, "qbe": qbe}

    cases = []
    for case in suite["cases"]:
        case_dir = evidence / "apps" / case["id"]
        case_dir.mkdir(parents=True)
        expected = source_case(case, case_dir)
        (case_dir / "expected").write_bytes(expected)
        roles = [*prepared, "typerb-go"]
        if "pureGoSource" in case:
            roles.append("pure-go")
            shutil.copyfile(ROOT / case["pureGoSource"], case_dir / "pure-go.go")
        artifacts = {}
        for role in roles:
            role_dir = case_dir / role
            role_dir.mkdir()
            program = role_dir / "program"
            if role == "pure-go":
                command = ["go", "build", "-trimpath", "-o", program, case_dir / "pure-go.go"]
            elif role == "typerb-go":
                command = [args.reference, "build", "--compile", "--config",
                           case_dir / "trbconfig.jsonc", "--outfile", program]
            else:
                compiler = prepared[role]["compiler"]
                qbe = prepared[role]["qbe"]
                command = [compiler, "build", case_dir / "src/main.trb", "--output",
                           program, "--qbe", qbe, "--cc", "/usr/bin/cc", "--target", "linux-arm64-v0"]
            record(command, role_dir / "build", 120, kind="application-build",
                   case=case["id"], role=role)
            if not program.is_file() or (role_dir / "build/stderr").stat().st_size:
                raise ValueError("Application build failed")
            artifacts[role] = {"sha256": digest(program), "bytes": program.stat().st_size}
            write(case_dir / "identities.json", artifacts)
            if role in prepared:
                if artifacts[role]["sha256"] != plan["variants"][role]["appSHA256"][case["id"]]:
                    raise ValueError(f"{case['id']} {role}: application differs from registered diagnostic")
                with (role_dir / "program.ssa").open("wb") as emitted:
                    subprocess.run([prepared[role]["compiler"], "emit-qbe", case_dir / "src/main.trb"],
                                   stdout=emitted, check=True, env=env, timeout=90)
                subprocess.run([prepared[role]["qbe"], "-t", "arm64", "-o",
                                role_dir / "program.s", role_dir / "program.ssa"], check=True)
        cases.append((case, case_dir, expected, roles, artifacts))

    for iteration in range(6):
        rotated = cases[iteration % len(cases):] + cases[:iteration % len(cases)]
        for index, (case, directory, expected, roles, artifacts) in enumerate(rotated):
            offset = (iteration + index) % len(roles)
            for role in roles[offset:] + roles[:offset]:
                program = directory / role / "program"
                if digest(program) != artifacts[role]["sha256"]:
                    raise ValueError("Application changed after preparation")
                observation_dir = directory / role / f"runtime-{iteration}"
                item = record([program, *case["args"]], observation_dir, 30,
                              kind="runtime", case=case["id"], role=role,
                              phase="first" if iteration == 0 else "steady",
                              iteration=iteration, artifact=artifacts[role])
                correct(item, observation_dir, expected)
                write(evidence / "raw.json", raw)
                if item["status"] != "pass":
                    raise ValueError("Runtime output differs")
        print(f"Completed round {iteration}; {len(raw)} observations retained", flush=True)
    rows = []
    for case, _directory, _expected, roles, artifacts in cases:
        for role in roles:
            rows.append({"case": case["id"], "role": role, "artifact": artifacts[role],
                         "runtime": summary([r for r in raw if r["kind"] == "runtime"
                                             and r["case"] == case["id"] and r["role"] == role])})
    write(evidence / "summary.json", {"scope": "Diagnostic, not final qualification", "rows": rows})
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registration", type=Path, required=True)
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args())
