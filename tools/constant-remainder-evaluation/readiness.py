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

CASES = {"enum-result": ("trbnf3", 6), "object-dispatch": ("trbnf0", 4)}


def inspect_ir(text, case):
    symbol, _ = CASES[case]
    match = re.search(r'function[^\n]*\$' + symbol + r'\([^\n]*\) \{.*?\n\}', text, re.S)
    if not match:
        raise ValueError("Missing unchanged consumer in diagnostic IR")
    body = match.group(0)
    return {"directCalls": re.findall(r'call \$trbnf\d+', body),
            "enumSlots": body.count("enum_slot"),
            "reciprocalCorrections": body.count(" =l sar "),
            "reciprocalGuards": body.count(", 2147483648")}


def validate_ir(ir):
    expected_calls = {"enum-result": [], "object-dispatch":
                      ["call $trbnf3", "call $trbnf5", "call $trbnf3", "call $trbnf5", "call $trbnf2"]}
    for case, (_, count) in CASES.items():
        for role in ("previous", "native"):
            row = ir[case][role]
            if (row["directCalls"] != expected_calls[case] or row["enumSlots"] != 0 or
                    row["reciprocalCorrections"] != 0 or
                    row["reciprocalGuards"] != (count if role == "native" else 0)):
                raise ValueError(f"{case}/{role}: registered lowering or retained scalarization differs")


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

    def execute(command, cwd, timeout):
        if len(commands) >= 36:
            raise ValueError("Readiness product execution cap exceeded")
        index = len(commands)
        commands.append({"command": command, "cwd": str(cwd), "timeoutSeconds": timeout, "status": "started"})
        (args.output / "commands.json").write_text(json.dumps(commands, indent=2) + "\n")
        result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, timeout=timeout)
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
                    run = execute([str(output), *case["args"]], directory, 30)
                    if run.stdout != expected or run.stderr:
                        raise ValueError(f"{case['id']}/{role}: incorrect output")
                    hashes.append(digest(output))
                if len(set(hashes)) != 1:
                    raise ValueError(f"{case['id']}/{role}: repeated build identity differs")
                rows.append({"case": case["id"], "role": role, "sha256": hashes[0], "builds": 2, "outputs": 2})
                print(f"ready {case['id']} {role}", flush=True)
        if len(rows) != 8:
            raise ValueError("Incomplete readiness matrix")
        ir = {}
        for case in CASES:
            current = next(row for row in rows if row["case"] == case and row["role"] == "native")
            previous = next(row for row in rows if row["case"] == case and row["role"] == "previous")
            if current["sha256"] == previous["sha256"]:
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
        if len(commands) != 36:
            raise ValueError("Incomplete readiness command budget")
        result = {"status": "pass", "rows": rows, "ir": ir, "productExecutions": len(commands), "timingObservations": 0,
                  "goFlags": env["GOFLAGS"], "goVersion": subprocess.check_output(["go", "version"], text=True).strip()}
    except Exception as error:
        result = {"status": "fail", "rows": rows, "error": str(error), "productExecutions": len(commands), "timingObservations": 0}
        raise
    finally:
        (args.output / "readiness.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
