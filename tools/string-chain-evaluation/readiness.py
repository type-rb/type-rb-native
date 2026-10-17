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

CASES = {"string-building": "trbnf0", "hash-string-keys": "trbnf0"}


def inspect_ir(text, case):
    match = re.search(r'function[^\n]*\$' + CASES[case] + r'\([^\n]*\) \{.*?\n\}', text, re.S)
    if not match:
        raise ValueError("Missing unchanged consumer in diagnostic IR")
    body = match.group(0)
    entry = body.split("jmp @mir_", 1)[0]
    return {"binaryCalls": body.count("call $trbn_string_concat(l "),
            "fusedCalls": body.count("call $trbn_string_concat_many(l "),
            "scratchAllocations": len(re.findall(r"%string_fragments =l alloc8 ", body)),
            "entryScratchBytes": re.findall(r"%string_fragments =l alloc8 (\d+)", entry)}


def validate_ir(ir):
    for case in CASES:
        for role in ("previous", "native"):
            fused = case == "string-building" and role == "native"
            expected = {"binaryCalls": 1 if fused or case == "hash-string-keys" else 3,
                        "fusedCalls": int(fused), "scratchAllocations": int(fused),
                        "entryScratchBytes": ["24"] if fused else []}
            if ir[case][role] != expected:
                raise ValueError(f"{case}/{role}: registered chain lowering or entry scratch differs")


def gc_stats(stderr):
    stats = {}
    for line in stderr.decode().splitlines():
        tag, key, value = line.split(",")
        if tag != "type-rb-native-gc-stat-v1" or key in stats or not value.isdigit():
            raise ValueError("Unexpected GC statistics")
        stats[key] = int(value)
    if (set(stats) != {"collections", "automatic-collections", "allocated-bytes", "reclaimed-bytes", "live-bytes", "peak-heap-bytes"}
            or stats["allocated-bytes"] != stats["reclaimed-bytes"] or stats["live-bytes"] != 0
            or stats["automatic-collections"] <= 0):
        raise ValueError("Incomplete collection or reclamation evidence")
    return stats


def validate_gc(rows):
    controls = {(r["case"], r["role"]): r for r in rows}
    for case in CASES:
        for role in ("native", "previous"):
            if "gc" not in controls[(case, role)]:
                raise ValueError("Missing readiness GC control")
    current = controls[("string-building", "native")]["gc"]["allocated-bytes"]
    previous = controls[("string-building", "previous")]["gc"]["allocated-bytes"]
    if current >= previous:
        raise ValueError("String chain did not reduce allocated bytes")
    return {"nativeAllocatedBytes": current, "previousAllocatedBytes": previous}


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
                        stats = gc_stats(run.stderr)
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
            if case == "string-building" and current["sha256"] == previous["sha256"]:
                raise ValueError(f"{case}: primary application did not change")
            ir[case] = {}
            for role in ("previous", "native"):
                emitted = execute([roles[role]["path"], "emit-qbe", str(args.output / case / "src/main.trb")],
                                  args.output, 90)
                if emitted.stderr:
                    raise ValueError("Primary IR emission has stderr")
                (args.output / (role + "-" + case + ".ssa")).write_bytes(emitted.stdout)
                ir[case][role] = inspect_ir(emitted.stdout.decode(), case)
        validate_ir(ir)
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
