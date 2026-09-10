"""Bounded, read-only Actions state retrieval and daily snapshot publication."""
import argparse
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import subprocess
import zipfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = "daily-performance.yml"
ARTIFACT = "daily-performance-state"
SHA = re.compile(r"[0-9a-f]{40}")


def now():
    return datetime.now(timezone.utc).isoformat()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT).decode().strip()


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    temporary.replace(path)


def empty():
    return {"schemaVersion": 1, "latest": None, "attempt": None, "history": []}


def validate(state):
    if state.get("schemaVersion") != 1 or not isinstance(state.get("history"), list):
        raise ValueError("Unsupported daily state")
    if len(state["history"]) > 60:
        raise ValueError("History exceeds its bounded retention")
    for snapshot in [state.get("latest"), *state["history"]]:
        if snapshot is None:
            continue
        if not SHA.fullmatch(snapshot.get("revision", "")) or not isinstance(snapshot.get("rows"), list):
            raise ValueError("Malformed snapshot")
        roles = snapshot.get("roles", {})
        if set(roles) != {"native", "previous", "baseline", "typerb-go"}:
            raise ValueError("Incomplete compiler identities")
        if roles["native"]["revision"] != snapshot["revision"]:
            raise ValueError("Native revision does not match the snapshot")
        for role in roles.values():
            if not SHA.fullmatch(role.get("revision", "")):
                raise ValueError("Invalid compiler revision")
        cases = {}
        if not 1 <= len(snapshot["rows"]) <= 100:
            raise ValueError("Invalid row count")
        for row in snapshot["rows"]:
            case, role = row.get("case"), row.get("role")
            if not isinstance(case, str) or not re.fullmatch(r"[a-z0-9-]+", case) or role not in roles:
                raise ValueError("Invalid row identity")
            if role in cases.setdefault(case, set()):
                raise ValueError("Duplicate observation row")
            cases[case].add(role)
            if row.get("status") not in {"pass", "timeout", "nonzero-exit", "output-mismatch", "unexpected-stderr", "build-failure"}:
                raise ValueError("Invalid observation status")
            if row["status"] == "pass" and (row.get("runtime") is None or row.get("build") is None):
                raise ValueError("Passing row has missing measurements")
            if row["status"] != "pass" and row.get("runtime") is not None:
                raise ValueError("Failed row has a passing runtime median")
            for group in ("runtime", "build"):
                metrics = row.get(group)
                if metrics is not None:
                    for name in ("wallSeconds", "cpuSeconds", "memoryBytes", "wallMin", "wallMax"):
                        value = metrics.get(name)
                        if not isinstance(value, (float, int)) or not math.isfinite(value) or value < 0:
                            raise ValueError("Invalid measurement metric")
                    if not 0 < metrics["wallMin"] <= metrics["wallSeconds"] <= metrics["wallMax"]:
                        raise ValueError("Invalid measurement range")
        if any(members != set(roles) for members in cases.values()):
            raise ValueError("Missing comparison role")
    return state


def gh(endpoint, binary=False):
    result = subprocess.check_output(["gh", "api", endpoint], timeout=60)
    return result if binary else json.loads(result)


def restore(destination):
    repo = os.environ["GITHUB_REPOSITORY"]
    # A repository artifact name alone is not an authority: verify the producer.
    artifacts = gh(f"repos/{repo}/actions/artifacts?name={ARTIFACT}&per_page=100")["artifacts"]
    if not artifacts:
        write(destination, empty())
        return
    workflow_id = gh(f"repos/{repo}/actions/workflows/{WORKFLOW}")["id"]
    for artifact in sorted(artifacts, key=lambda item: item["id"], reverse=True):
        if artifact["expired"] or artifact["workflow_run"]["head_branch"] != "main":
            continue
        run = gh(f"repos/{repo}/actions/runs/{artifact['workflow_run']['id']}")
        if run["workflow_id"] != workflow_id or run["event"] not in ("schedule", "workflow_dispatch"):
            continue
        if run["status"] != "completed":
            continue
        if run["head_repository"]["full_name"] != repo:
            continue
        if artifact["size_in_bytes"] > 8_000_000:
            raise ValueError("Daily state artifact is too large")
        archive = zipfile.ZipFile(io.BytesIO(gh(f"repos/{repo}/actions/artifacts/{artifact['id']}/zip", True)))
        member = archive.getinfo("state.json")
        if member.file_size > 8_000_000:
            raise ValueError("Daily state expands beyond its limit")
        state = validate(json.loads(archive.read(member)))
        write(destination, state)
        return
    write(destination, empty())


def relevant(path):
    if path.endswith(".md") or path.endswith("_test.trb"):
        return False
    return path.startswith(("compiler/", "src/", "benchmarks/", "tools/daily-performance/",
                            "tools/runtime-memory-soak/", "tools/runtime-worker-soak/",
                            "tools/native-mir-array-loop-recovery/")) or path in (
        "TYPE_RB_REVISION", ".github/workflows/daily-performance.yml",
        "tools/bootstrap-seed.sh", "tools/bootstrap-seed-download.sh", "tools/compiler-project.sh")


def fingerprint():
    entries = subprocess.check_output(["git", "ls-tree", "-rz", "HEAD"], cwd=ROOT).split(b"\0")
    selected = [entry for entry in entries if entry and relevant(entry.split(b"\t", 1)[1].decode())]
    return hashlib.sha256(b"\0".join(selected)).hexdigest()


def series():
    suite = read(ROOT / "tools/daily-performance/suite.json")
    digest = hashlib.sha256((ROOT / "tools/daily-performance/suite.json").read_bytes())
    digest.update((ROOT / "tools/daily-performance/measure.py").read_bytes())
    digest.update((ROOT / "TYPE_RB_REVISION").read_bytes())
    for case in suite["cases"]:
        digest.update((ROOT / case["source"]).read_bytes())
        if "expectedFile" in case:
            digest.update((ROOT / case["expectedFile"]).read_bytes())
    return digest.hexdigest()


def plan(path, output, force):
    state = validate(read(path))
    current = fingerprint()
    latest = state["latest"]
    should_run = force or not latest or latest["fingerprint"] != current
    revision = git("rev-parse", "HEAD")
    state["checked"] = {"revision": revision, "at": now(), "fingerprint": current}
    if should_run:
        state["attempt"] = {"revision": revision, "at": now(), "status": "running",
                            "runUrl": os.environ.get("GITHUB_SERVER_URL", "https://github.com") + "/" +
                            os.environ["GITHUB_REPOSITORY"] + "/actions/runs/" + os.environ["GITHUB_RUN_ID"]}
    write(path, state)
    previous = latest["revision"] if latest and latest.get("series") == series() else revision
    with open(output, "a") as stream:
        stream.write(f"measure={str(should_run).lower()}\nprevious={previous}\n")


def finish(path, snapshot_path, status):
    state = validate(read(path))
    snapshot = read(snapshot_path) if Path(snapshot_path).exists() else None
    if snapshot and status == "success":
        snapshot.update({"fingerprint": state["checked"]["fingerprint"], "series": series(),
                         "runUrl": state["attempt"]["runUrl"]})
        validate({**empty(), "latest": snapshot})
        state["latest"] = snapshot
        state["history"] = [*state["history"], snapshot][-60:]
        state["attempt"]["status"] = snapshot["status"]
    else:
        state["attempt"]["status"] = "infrastructure-failure"
    write(path, state)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["restore", "plan", "finish", "site"])
    parser.add_argument("--state", required=True)
    parser.add_argument("--output")
    parser.add_argument("--snapshot")
    parser.add_argument("--status")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.command == "restore":
        restore(args.state)
    elif args.command == "plan":
        plan(args.state, args.output, args.force)
    elif args.command == "finish":
        finish(args.state, args.snapshot, args.status)
    else:
        state = validate(read(args.state))
        trigger = os.environ.get("TRIGGER_RUN_ID")
        if trigger and os.environ.get("TRIGGER_CONCLUSION") in ("failure", "cancelled", "timed_out"):
            run_url = f"https://github.com/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{trigger}"
            if (state.get("attempt") or {}).get("runUrl") != run_url:
                state["attempt"] = {"status": "infrastructure-failure", "revision": git("rev-parse", "HEAD"),
                                    "at": now(), "runUrl": run_url}
        state["siteRevision"] = git("rev-parse", "HEAD")
        state["pendingChanges"] = not state["latest"] or state["latest"]["fingerprint"] != fingerprint()
        write(args.output, state)


if __name__ == "__main__":
    main()
