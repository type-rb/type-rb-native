"""One prospective A/A cohort using only retained accepted-main executables."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/daily-performance"))
from measure import observe, correct, digest


def write(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n")


def ordering(block, case_index, round_index):
    return ("A", "B") if (block + case_index + round_index) % 2 == 0 else ("B", "A")


def assess(records):
    rows = []
    failures = []
    for block in range(3):
        for case in ("object-dispatch", "fannkuch-redux", "array-streaming"):
            samples = {role: [r for r in records if r["block"] == block and r["case"] == case and r["role"] == role] for role in ("A", "B")}
            row = {"block": block, "case": case, "metrics": {}}
            if any(len(s) != 6 or any(r["status"] != "pass" for r in s) for s in samples.values()):
                failures.append(f"incomplete-or-invalid:{block}:{case}")
                rows.append(row)
                continue
            medians = {role: {metric: statistics.median(r[metric] for r in s if r["round"] > 0) for metric in ("wallSeconds", "cpuSeconds", "memoryBytes")} for role, s in samples.items()}
            for metric in ("wallSeconds", "cpuSeconds", "memoryBytes"):
                a, b = medians["A"][metric], medians["B"][metric]
                unknown = metric == "cpuSeconds" and min(a, b) < 0.01
                ratio = None if unknown or min(a, b) <= 0 else max(a, b) / min(a, b)
                passed = None if unknown else ratio is not None and ratio <= 1.05
                row["metrics"][metric] = {"A": a, "B": b, "ratio": ratio, "pass": passed}
                if passed is False:
                    failures.append(f"spread:{block}:{case}:{metric}")
            for role, s in samples.items():
                if any(r["wallSeconds"] > 2 * medians[role]["wallSeconds"] for r in s):
                    failures.append(f"outlier:{block}:{case}:{role}")
            rows.append(row)
    return {"status": "pass" if len(records) == 108 and not failures else "unmet", "observations": len(records), "rows": rows, "failures": failures}


def run(args):
    registration = json.loads((Path(__file__).parent / "registration.json").read_text())
    if platform.system() != "Linux" or platform.machine() not in ("aarch64", "arm64"):
        raise ValueError("Linux arm64 is required")
    if os.environ.get("GITHUB_RUN_ATTEMPT") != "1":
        raise ValueError("Only the first dispatched attempt is allowed")
    if digest(ROOT / "tools/daily-performance/measure.py") != registration["measureSha256"]:
        raise ValueError("Measurement primitive changed")
    evidence = Path(args.evidence).resolve()
    evidence.mkdir(parents=True, exist_ok=False)
    core = min(os.sched_getaffinity(0))
    environment = {k: v for k, v in os.environ.items() if not k.startswith("TYPE_RB_NATIVE_RUNTIME_")}
    environment.update(LC_ALL="C", GOMAXPROCS="1")
    context = {"registration": registration, "controllerSha256": digest(__file__), "core": core,
               "platform": platform.platform(), "cpu": subprocess.check_output(["lscpu"]).decode(),
               "swaps": Path("/proc/swaps").read_text(), "timeVersion": subprocess.check_output(["/usr/bin/time", "--version"]).decode(),
               "cachePolicy": "warm filesystem; no cache drops", "runId": os.environ.get("GITHUB_RUN_ID")}
    write(evidence / "context.json", context)
    if len(context["swaps"].strip().splitlines()) != 1:
        raise ValueError("Swap must be disabled")
    selected = []
    for case in registration["cases"]:
        original = Path(args.archive) / "measurements/artifacts/sha256" / case["sha256"]
        data = original.read_bytes()
        if len(data) != case["bytes"] or hashlib.sha256(data).hexdigest() != case["sha256"]:
            raise ValueError("Retained accepted executable identity mismatch")
        program = evidence / (case["id"] + "-accepted")
        program.write_bytes(data)
        program.chmod(0o755)
        selected.append((case, program))
    records = []
    write(evidence / "started.json", {"maximumExecutions": 108, "candidateExecutions": 0})
    try:
        for block in range(3):
            for case_index, (case, program) in enumerate(selected):
                for round_index in range(6):
                    for role in ordering(block, case_index, round_index):
                        directory = evidence / case["id"] / str(block) / f"{round_index}-{role}"
                        if digest(program) != case["sha256"]:
                            raise ValueError("Executable changed before invocation")
                        write(evidence / "attempt.json", {"attempt": len(records) + 1, "case": case["id"], "block": block, "round": round_index, "role": role})
                        record = observe([program, *case["args"]], directory, 30, env=environment, core=core)
                        record = correct(record, directory, case["expected"].encode())
                        record.update(block=block, case=case["id"], round=round_index, role=role, sha256=case["sha256"])
                        write(directory / "observation.json", record)
                        records.append(record)
                        write(evidence / "raw.json", records)
                        if record["status"] != "pass":
                            raise ValueError("Product output or execution failed")
    finally:
        write(evidence / "assessment.json", assess(records))
    result = assess(records)
    print(json.dumps(result))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", required=True)
    parser.add_argument("--evidence", required=True)
    sys.exit(run(parser.parse_args()))
