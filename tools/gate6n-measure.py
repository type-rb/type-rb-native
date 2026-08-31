#!/usr/bin/env python3

"""Measure one Gate 6N command with a monotonic clock.

The measured command is executed directly, without an intermediary shell.  Peak
RSS is intentionally measured by a separate GNU time invocation owned by the
Gate 6N harness so elapsed time and orchestration-root RSS remain independent
observations.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def usage() -> int:
    print(
        "usage: gate6n-measure.py RECORD STDOUT STDERR ARTIFACT|- -- COMMAND [ARG ...]",
        file=sys.stderr,
    )
    return 64


def artifact_record(path: str) -> dict[str, object]:
    artifact = Path(path)
    if not artifact.is_file():
        return {"path": path, "exists": False}

    digest = hashlib.sha256()
    with artifact.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return {
        "path": path,
        "exists": True,
        "executable": os.access(artifact, os.X_OK),
        "size": artifact.stat().st_size,
        "sha256": digest.hexdigest(),
    }


def main(arguments: list[str]) -> int:
    if len(arguments) < 7 or arguments[5] != "--":
        return usage()

    record_path = Path(arguments[1])
    stdout_path = Path(arguments[2])
    stderr_path = Path(arguments[3])
    artifact_path = arguments[4]
    command = arguments[6:]
    if not command:
        return usage()

    try:
        clock = time.get_clock_info("monotonic")
        input_before = artifact_record(command[0])
        started = time.monotonic_ns()
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        finished = time.monotonic_ns()
        input_after = artifact_record(command[0])

        stdout_path.write_bytes(process.stdout)
        stderr_path.write_bytes(process.stderr)
        elapsed_nanoseconds = finished - started
        record: dict[str, object] = {
            "schemaVersion": 1,
            "clock": "time.monotonic_ns",
            "clockInfo": {
                "implementation": clock.implementation,
                "resolutionSeconds": clock.resolution,
                "monotonic": clock.monotonic,
                "adjustable": clock.adjustable,
            },
            "command": command,
            "elapsedNanoseconds": elapsed_nanoseconds,
            "elapsedSeconds": f"{elapsed_nanoseconds / 1_000_000_000:.9f}",
            "status": process.returncode,
            "inputExecutableBefore": input_before,
            "inputExecutableAfter": input_after,
            "artifact": None if artifact_path == "-" else artifact_record(artifact_path),
        }
        record_path.write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    except (OSError, ValueError) as error:
        print(f"gate6n-measure: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
