#!/usr/bin/env python3
"""Bounded, opt-in application coverage; never part of the daily victory score."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import selectors
import shutil
import signal
import statistics
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
SUITE = Path(__file__).with_name("suite.json")
SOURCE = ROOT / "benchmarks/representative/src/main.trb"
GO_SOURCE = ROOT / "benchmarks/representative/go/main.go"
OUTPUT_LIMIT = 1024 * 1024


def write(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def percentile(values, fraction):
    """Nearest rank; sparse tails remain unknown, never a favorable score."""
    minimum = {0.5: 1, 0.95: 20, 0.99: 100}[fraction]
    if len(values) < minimum:
        return None
    return sorted(values)[math.ceil(len(values) * fraction) - 1]


def distribution(values):
    return {"count": len(values), "p50": percentile(values, 0.5),
            "p95": percentile(values, 0.95), "p99": percentile(values, 0.99),
            "maximum": max(values) if values else None}


def observe(command, directory, timeout, env=None):
    """Observe one owned process, including CPU/RSS and stdout arrival times.

    wait4 measures this child, not a cumulative maximum over preceding children.
    Batch timestamps are observer-side completion arrivals, including pipe and
    scheduler overhead. Coalesced lines are recorded and invalidate interval
    percentiles; they cannot be interpreted as zero-latency work.
    """
    directory.mkdir(parents=True)
    started = time.monotonic()
    record = {"command": list(map(str, command)), "timeoutSeconds": timeout,
              "status": "pass", "arrivals": []}
    process = subprocess.Popen(record["command"], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, start_new_session=True, env=env)
    streams = {"stdout": bytearray(), "stderr": bytearray()}
    pending = bytearray()
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ, "stdout")
    selector.register(process.stderr, selectors.EVENT_READ, "stderr")
    usage = None
    status = None
    terminated = False

    def terminate():
        nonlocal terminated
        if terminated:
            return
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        terminated = True

    try:
        while selector.get_map() or status is None:
            elapsed = time.monotonic() - started
            if elapsed >= timeout:
                record["status"] = "timeout"
                terminate()
                break
            for key, _ in selector.select(min(0.02, timeout - elapsed)):
                chunk = os.read(key.fileobj.fileno(), 65536)
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                streams[key.data].extend(chunk)
                if sum(map(len, streams.values())) > OUTPUT_LIMIT:
                    record["status"] = "output-limit"
                    terminate()
                    break
                if key.data == "stdout":
                    pending.extend(chunk)
                    lines = pending.split(b"\n")
                    pending = bytearray(lines.pop())
                    arrival = time.monotonic() - started
                    for line in lines:
                        record["arrivals"].append({"line": line.decode("utf-8", errors="replace"),
                                                   "seconds": arrival, "coalesced": len(lines) > 1})
            if record["status"] != "pass":
                break
            if status is None:
                pid, child_status, child_usage = os.wait4(process.pid, os.WNOHANG)
                if pid:
                    status, usage = child_status, child_usage
                    process.returncode = os.waitstatus_to_exitcode(status)
        if status is None:
            _, status, usage = os.wait4(process.pid, 0)
            process.returncode = os.waitstatus_to_exitcode(status)
        record.update(exitCode=process.returncode, wallSeconds=time.monotonic() - started,
                      cpuSeconds=usage.ru_utime + usage.ru_stime,
                      peakRssBytes=int(usage.ru_maxrss * (1 if sys.platform == "darwin" else 1024)))
        if process.returncode and record["status"] == "pass":
            record["status"] = "nonzero-exit"
    finally:
        terminate()
        selector.close()
        process.stdout.close()
        process.stderr.close()
        process.wait()
        for name, data in streams.items():
            (directory / name).write_bytes(data)
        write(directory / "observation.json", record)
    return record


def expected(case):
    """Independent correctness oracle for every registered input, not timings."""
    count, variant, workload = case["count"], case["variant"], case["workload"]
    cache, retained = [""] * 128, [""] * count if variant == "retained" else []
    completed = 0
    lines = ["ready"]
    for batch in range(case["batches"]):
        if workload == "log-pipeline":
            totals, rejected = {}, 0
            for index in range(count):
                if variant == "mixed" and index % 17 == 0:
                    rejected += 1
                else:
                    key = f"group-{index % 127}"
                    totals[key] = totals.get(key, 0) + index % 1000
            checksum = len("\n".join(f"{key}={totals[key]}" for key in sorted(totals))) + rejected
        elif workload == "json-transform":
            checksum = sum(1 if variant == "mixed" and index % 17 == 0 else
                           len(json.dumps([index + 1, "aβ😀" * 4, True], ensure_ascii=False,
                                          separators=(",", ":"))) for index in range(count))
        elif workload == "worker":
            checksum = 0
            for index in range(count):
                if index % 17 == 0:
                    checksum += 1
                    continue
                value = f"job-{batch}-{index}-" + "aβ😀" * 8 + ("-retry" if index % 11 == 0 else "")
                cache[(index + batch) % 128] = value
                completed += 1
                checksum += len(value)
            checksum += sum(map(len, cache)) + completed
        elif workload == "hash":
            checksum = sum(1 if variant == "miss-heavy" and index % 10 else index for index in range(count))
        elif workload == "strings":
            checksum = count * (3 * (512 if variant == "long" else 4) + 5)
        elif workload == "arrays":
            values = {"sorted": lambda i: i, "reverse": lambda i: count - i,
                      "duplicates": lambda i: i % 8, "random": lambda i: (i * 7919 + 17) % 100003}
            checksum = sum(value * (index % 7 + 1) for index, value in
                           enumerate(sorted(values[variant](i) for i in range(count)))) % 1000000007
        elif workload == "allocation":
            values = [f"object-{batch}-{index}-" + "aβ😀" * 16 for index in range(count)]
            checksum = sum(map(len, values))
            if variant == "retained":
                retained = values
        else:
            raise ValueError("Unknown workload: " + workload)
        lines.append(f"{batch},{checksum}")
    lines.append(f"done,{sum(map(len, retained))}")
    return ("\n".join(lines) + "\n").encode()


def validate(record, directory, oracle):
    if record["status"] == "pass":
        if (directory / "stdout").read_bytes() != oracle:
            record["status"] = "output-mismatch"
        elif (directory / "stderr").stat().st_size:
            record["status"] = "unexpected-stderr"
    write(directory / "observation.json", record)
    return record


def summarize(records, units):
    retained = [r for r in records if r["phase"] == "retained"]
    if not retained or any(r["status"] != "pass" for r in records):
        return None
    walls = [r["wallSeconds"] for r in retained]
    intervals, coalesced = [], False
    for record in retained:
        arrivals = record["arrivals"]
        ready = next(a for a in arrivals if a["line"] == "ready")
        previous = ready["seconds"]
        for arrival in arrivals:
            if arrival["line"].split(",")[0].isdigit():
                coalesced |= arrival["coalesced"]
                intervals.append(arrival["seconds"] - previous)
                previous = arrival["seconds"]
    return {"processWallSeconds": distribution(walls),
            "cpuSeconds": statistics.median(r["cpuSeconds"] for r in retained),
            "peakRssBytes": statistics.median(r["peakRssBytes"] for r in retained),
            "unitsPerSecond": units / statistics.median(walls),
            "batchArrivalIntervalSeconds": None if coalesced else distribution(intervals),
            "batchIntervalUnavailableReason": "coalesced stdout markers" if coalesced else None,
            "firstProcessWallSeconds": records[0]["wallSeconds"]}


def load_cases(smoke=False, selected=None):
    suite = json.loads(SUITE.read_text())
    cases = suite["cases"]
    if selected:
        known = {c["id"] for c in cases}
        if set(selected) - known:
            raise ValueError("Unknown case IDs: " + ", ".join(sorted(set(selected) - known)))
        cases = [c for c in cases if c["id"] in selected]
    if smoke:
        # Cover each path once with small inputs; timing has no acceptance role.
        unique = {}
        for case in cases:
            key = (case["workload"], case["variant"])
            unique.setdefault(key, dict(case, count=23, batches=2))
        cases = list(unique.values())
    return suite, cases


def build_programs(args, workspace, evidence, env):
    binaries = {}
    if args.native:
        binaries["native"] = workspace / "native"
        command = [args.native, "build", "--compile", SOURCE, "--outfile", binaries["native"]]
        result = observe(command, evidence / "build-native", 120, env)
        if result["status"] != "pass":
            raise RuntimeError("Native build failed; see build-native")
    if args.go:
        binaries["pure-go"] = workspace / "pure-go"
        result = observe([args.go, "build", "-trimpath", "-o", binaries["pure-go"], GO_SOURCE],
                         evidence / "build-pure-go", 120, env)
        if result["status"] != "pass":
            raise RuntimeError("Pure Go build failed; see build-pure-go")
    if args.reference:
        project = workspace / "reference"
        (project / "src").mkdir(parents=True)
        shutil.copyfile(SOURCE, project / "src/main.trb")
        config = project / "trbconfig.jsonc"
        write(config, {"name": "representative-performance", "version": "0.1.0", "mode": "go",
                       "sourceDir": "src", "outDir": "build", "copyFiles": False,
                       "packageManagement": "managed", "go": {"module": "example.org/representative", "version": "1.27"}})
        binaries["typerb-go"] = workspace / "typerb-go"
        result = observe([args.reference, "build", "--config", config, "--compile", "--outfile", binaries["typerb-go"]],
                         evidence / "build-typerb-go", 120, env)
        if result["status"] != "pass":
            raise RuntimeError("TypeRB Go build failed; see build-typerb-go")
    return binaries


def gc_probe(binary, case, evidence, env):
    """Untimed Native managed-heap counters; not a Go heap comparison."""
    directory = evidence / case["id"] / "native-gc-probe"
    command = [binary, case["workload"], str(case["count"]), case["variant"], str(case["batches"])]
    record = observe(command, directory, 30, dict(env, TYPE_RB_NATIVE_RUNTIME_STATS="1"))
    counters = {}
    if record["status"] == "pass":
        if (directory / "stdout").read_bytes() != expected(case):
            record["status"] = "output-mismatch"
        else:
            for line in (directory / "stderr").read_text().splitlines():
                fields = line.split(",")
                if len(fields) != 3 or fields[0] != "type-rb-native-gc-stat-v1" or fields[1] in counters or not fields[2].isdigit():
                    record["status"] = "invalid-gc-counters"
                    break
                counters[fields[1]] = int(fields[2])
            if not {"allocated-bytes", "reclaimed-bytes", "live-bytes"} <= counters.keys():
                record["status"] = "missing-gc-counters"
    record.update(instrumented=True, comparisonScope="Native managed allocations only", counters=counters)
    write(directory / "observation.json", record)
    if record["status"] != "pass":
        raise RuntimeError(f"{case['id']}: {record['status']}")
    return {"input": case, "status": record["status"], "counters": counters}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--native", type=Path, help="Already built current Native CLI; never builds a compiler")
    parser.add_argument("--reference", type=Path, help="Pinned TypeRB Go CLI")
    parser.add_argument("--go", type=Path, help="Go executable for the hand-written control")
    parser.add_argument("--evidence", required=True, type=Path, help="New output directory")
    parser.add_argument("--smoke", action="store_true", help="Small correctness-only inputs")
    parser.add_argument("--case", action="append", help="Select an exact case ID (repeatable)")
    parser.add_argument("--samples", type=int, help="Fixed retained process count, 1..100")
    parser.add_argument("--gc-probes", action="store_true", help="Separate untimed Native worker/allocation counters")
    args = parser.parse_args()
    if not (args.native or args.reference or args.go):
        parser.error("Provide at least one compiler")
    if args.samples is not None and not 1 <= args.samples <= 100:
        parser.error("--samples must be between 1 and 100")
    if args.gc_probes and (not args.native or args.smoke):
        parser.error("--gc-probes requires --native without --smoke")
    for name in ("native", "reference", "go"):
        if getattr(args, name):
            setattr(args, name, getattr(args, name).resolve(strict=True))
    suite, cases = load_cases(args.smoke, args.case)
    evidence = args.evidence.resolve()
    evidence.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ, GOMAXPROCS="1", NO_COLOR="1", TERM="dumb")
    env.pop("TYPE_RB_NATIVE_RUNTIME_STATS", None)
    env.pop("TYPE_RB_NATIVE_RUNTIME_TRACE", None)
    result = {"schemaVersion": 1, "diagnosticOnly": True, "smoke": args.smoke,
              "startedAt": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(), "machine": platform.machine(),
              "sourceSha256": digest(SOURCE), "goSourceSha256": digest(GO_SOURCE),
              "suiteSha256": digest(SUITE), "cases": [], "status": "running",
              "plannedCases": cases,
              "coverageGaps": ["file/network input", "request queueing and service latency", "parallel scaling"],
              "measurementScope": "fresh-process wall/CPU/peak RSS; observer-side batch completion intervals include pipe/scheduler overhead"}
    write(evidence / "manifest.json", result)
    try:
        with tempfile.TemporaryDirectory(prefix="representative-performance-") as temporary:
            binaries = build_programs(args, Path(temporary), evidence, env)
            result["binaries"] = {role: {"sha256": digest(binary), "bytes": binary.stat().st_size}
                                  for role, binary in binaries.items()}
            result["tools"] = {name: {"path": str(getattr(args, name)), "sha256": digest(getattr(args, name))}
                               for name in ("native", "reference", "go") if getattr(args, name)}
            for name, tool in result["tools"].items():
                version = subprocess.run([tool["path"], "--version" if name == "native" else "version"],
                                         capture_output=True, text=True, timeout=10)
                if version.returncode:
                    raise RuntimeError(name + " version query failed")
                tool["version"] = version.stdout.strip()
            result["repositoryRevision"] = subprocess.check_output(["git", "-C", ROOT, "rev-parse", "HEAD"], text=True).strip()
            result["controllerSha256"] = digest(__file__)
            result["environment"] = {"GOMAXPROCS": "1", "cpuCount": os.cpu_count(),
                                     "affinity": sorted(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else None,
                                     "filesystemCache": "uncontrolled local warm cache", "cpuPinning": "none"}
            roles = list(binaries)
            started = time.monotonic()
            samples = 1 if args.smoke else args.samples or suite["samples"]
            warmups = 0 if args.smoke else suite["warmups"]
            result.update(samples=samples, warmups=warmups)
            for case in cases:
                oracle = expected(case)
                rows = {role: [] for role in roles}
                for index in range(samples + warmups):
                    order = roles[index % len(roles):] + roles[:index % len(roles)]
                    for role in order:
                        remaining = suite["suiteTimeoutSeconds"] - (time.monotonic() - started)
                        if remaining <= 0:
                            raise TimeoutError("Suite time budget exhausted; partial evidence retained")
                        directory = evidence / case["id"] / role / str(index)
                        command = [binaries[role], case["workload"], str(case["count"]), case["variant"], str(case["batches"])]
                        record = observe(command, directory, min(remaining, suite["timeoutSeconds"]), env)
                        record.update(phase="warmup" if index < warmups else "retained", role=role)
                        validate(record, directory, oracle)
                        rows[role].append(record)
                        if record["status"] != "pass":
                            raise RuntimeError(f"{case['id']}/{role}: {record['status']}; observations retained")
                summaries = {role: summarize(records, case["count"] * case["batches"]) for role, records in rows.items()}
                ratios = {}
                if "native" in summaries:
                    for role in roles:
                        if role != "native":
                            ratios[role] = summaries["native"]["processWallSeconds"]["p50"] / summaries[role]["processWallSeconds"]["p50"]
                result["cases"].append({"input": case, "summaries": summaries, "nativeWallRatio": ratios})
                write(evidence / "manifest.json", result)
                print(case["id"] + ": pass", flush=True)
            if args.gc_probes:
                result["nativeGcProbes"] = []
                for case in cases:
                    if case["size"] == "medium" and case["workload"] in ("worker", "allocation"):
                        result["nativeGcProbes"].append(gc_probe(binaries["native"], case, evidence, env))
                        write(evidence / "manifest.json", result)
            result["status"] = "pass"
    except Exception as error:
        result.update(status="failed", error=str(error))
        raise
    finally:
        result["finishedAt"] = datetime.now(timezone.utc).isoformat()
        write(evidence / "manifest.json", result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
