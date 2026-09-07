#!/usr/bin/env python3
"""Strict packaging/verification for the registered previous-Native seed refresh.

This is a release observer, never a compiler or ordinary build stage. The v1
initial-root verifier remains separate and unchanged.
"""
import hashlib
import csv
import json
import math
from pathlib import Path
import re
import shutil
import statistics
import sys

TAG = "bootstrap-seed-2026-09-07"
MANIFEST = "type-rb-native-bootstrap-manifest-v2.json"
PREDECESSOR = {
    "releaseTag": "bootstrap-seed-2026-08-30",
    "nativeRevision": "0058818314977633c50393796ef9b9f8f1fda50f",
    "manifestSha256": "a46d8c789f661a96aa38b1d4b9fd9ee21e46ccb3f4f2303a4f4d43caae1701b0",
    "targets": [
        {"asset": "type-rb-native-bootstrap-darwin-arm64", "sha256": "ef438d13598c534766334b408a39715c56ff1b69db528910ebf7d90ec7720b65"},
        {"asset": "type-rb-native-bootstrap-linux-arm64", "sha256": "b4307c244edc9e4da620f2a7c1b03a733e575da032efefae615f9edf75048a37"},
    ],
}
BACKEND = {"name": "QBE", "version": "1.3", "sourceSha256": "d587905d620dc5e1d2bfa7c2cc642b9b837aa89a3188c6e37b53d756cf66e320"}
TARGETS = [
    ("darwin-arm64", "darwin", "macos-15", "arm64_apple", 350000),
    ("linux-arm64", "linux", "ubuntu-24.04-arm", "arm64", 317000),
]
TARGET_KEYS = {"asset", "profile", "os", "architecture", "runnerImage", "qbeTarget", "ccBoundary", "mode", "size", "sha256", "attestationSubjectSha256", "qbeBinarySize", "qbeBinarySha256"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def invalid_constant(_value):
    raise ValueError("non-finite JSON")


def read_json(path):
    return json.loads(Path(path).read_text(), object_pairs_hook=unique_object,
                      parse_constant=invalid_constant)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sha(value, width=64):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{%d}" % width, value) is not None


def size(value, maximum=None):
    return type(value) is int and value > 0 and (maximum is None or value <= maximum)


def validate_target(target, expected):
    name, os_name, runner, qbe_target, limit = expected
    require(isinstance(target, dict) and set(target) == TARGET_KEYS, "target keys differ")
    for key, value in {"asset": "type-rb-native-bootstrap-" + name,
                       "profile": name + "-v0", "os": os_name, "architecture": "arm64",
                       "runnerImage": runner, "qbeTarget": qbe_target,
                       "ccBoundary": "system-cc", "mode": "0755"}.items():
        require(target[key] == value, "target identity differs: " + key)
    require(size(target["size"], limit), "compiler size exceeds accepted target limit")
    require(sha(target["sha256"]) and target["attestationSubjectSha256"] == target["sha256"], "target digest differs")
    require(size(target["qbeBinarySize"]) and sha(target["qbeBinarySha256"]), "QBE binary identity invalid")


def validate_manifest(manifest, revision):
    require(sha(revision, 40), "invalid source revision")
    require(isinstance(manifest, dict) and set(manifest) == {
        "schemaVersion", "status", "releaseTag", "nativeRevision", "predecessor", "backend", "targets"
    }, "manifest keys differ")
    require(type(manifest["schemaVersion"]) is int and manifest["schemaVersion"] == 2, "manifest version differs")
    require(manifest["status"] == "experimental" and manifest["releaseTag"] == TAG, "release identity differs")
    require(manifest["nativeRevision"] == revision, "source revision differs")
    require(manifest["predecessor"] == PREDECESSOR, "predecessor provenance differs")
    require(manifest["backend"] == BACKEND, "backend identity differs")
    require(isinstance(manifest["targets"], list) and len(manifest["targets"]) == 2, "target count differs")
    for target, expected in zip(manifest["targets"], TARGETS):
        validate_target(target, expected)
    require(sum(target["size"] for target in manifest["targets"]) <= 667000, "combined size exceeds accepted limit")


def create(revision, inputs, output):
    inputs, output = Path(inputs), Path(output)
    manifest = {"schemaVersion": 2, "status": "experimental", "releaseTag": TAG,
                "nativeRevision": revision, "predecessor": PREDECESSOR,
                "backend": BACKEND, "targets": [read_json(inputs / (t[0] + ".json")) for t in TARGETS]}
    validate_manifest(manifest, revision)
    for target in manifest["targets"]:
        binary = inputs / target["asset"]
        require(binary.is_file() and binary.stat().st_size == target["size"] and digest(binary) == target["sha256"], "input compiler differs")
    output.mkdir()  # Never overwrite a prior package.
    for target in manifest["targets"]:
        binary = output / target["asset"]
        shutil.copyfile(inputs / target["asset"], binary)
        binary.chmod(0o755)
    (output / MANIFEST).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    names = [target["asset"] for target in manifest["targets"]] + [MANIFEST]
    (output / "SHA256SUMS").write_text("".join(digest(output / name) + "  " + name + "\n" for name in names))


def verify(revision, asset, directory, release_path):
    directory = Path(directory)
    manifest = read_json(directory / MANIFEST)
    validate_manifest(manifest, revision)
    targets = {target["asset"]: target for target in manifest["targets"]}
    require(asset in targets, "unknown target")
    target = targets[asset]
    binary = directory / asset
    require(binary.is_file() and binary.stat().st_size == target["size"] and digest(binary) == target["sha256"], "downloaded compiler differs")
    expected_sums = "".join(t["sha256"] + "  " + t["asset"] + "\n" for t in manifest["targets"])
    expected_sums += digest(directory / MANIFEST) + "  " + MANIFEST + "\n"
    require((directory / "SHA256SUMS").read_text() == expected_sums, "checksum index differs")
    release = read_json(release_path)
    require(release.get("tag_name") == TAG and release.get("target_commitish") == revision,
            "published release revision differs")
    require(release.get("draft") is False and release.get("prerelease") is True and release.get("immutable") is True,
            "release is not an immutable prerelease")
    expected = {t["asset"]: (t["size"], t["sha256"]) for t in manifest["targets"]}
    for name in (MANIFEST, "SHA256SUMS"):
        expected[name] = ((directory / name).stat().st_size, digest(directory / name))
    assets = release.get("assets")
    require(isinstance(assets, list) and len(assets) == len(expected), "release asset count differs")
    require({a.get("name") for a in assets} == set(expected), "release asset names differ")
    for entry in assets:
        count, checksum = expected[entry["name"]]
        require(type(entry.get("size")) is int and entry["size"] == count and entry.get("digest") == "sha256:" + checksum,
                "release asset metadata differs")


def observations(path, role):
    require(role in ("ordinary", "transition"), "unknown measurement role")
    stages = ["b2-b3", "b3-b4"]
    if role == "ordinary":
        stages.insert(0, "b1-b2")
    with Path(path).open(newline="") as source:
        reader = csv.DictReader(source)
        require(reader.fieldnames == ["stage", "iteration", "elapsed_seconds", "peak_rss_bytes", "status", "cpu_seconds"], "measurement fields differ")
        rows = list(reader)
    require(len(rows) == 7 * len(stages), "measurement count differs")
    require({row["stage"] for row in rows} == set(stages), "measurement stages differ")
    for stage in stages:
        iterations = [row["iteration"] for row in rows if row["stage"] == stage]
        require(sorted(iterations) == list("1234567"), "missing or repeated observation")
    require(all(row["status"] == "0" for row in rows), "failed observation")
    for metric in ("elapsed_seconds", "peak_rss_bytes", "cpu_seconds"):
        values = [float(row[metric]) for row in rows]
        require(all(math.isfinite(value) and value > 0 for value in values), "invalid observation")
        medians = [statistics.median(float(row[metric]) for row in rows if row["stage"] == stage) for stage in stages]
        require(max(medians) <= min(medians) * 1.25, "adjacent median limit exceeded")
        require(max(values) <= min(medians) * 2, "retained catastrophic limit exceeded")


if __name__ == "__main__":
    try:
        command, *arguments = sys.argv[1:]
        if command == "create" and len(arguments) == 3:
            create(*arguments)
        elif command == "verify" and len(arguments) == 4:
            verify(*arguments)
        elif command == "observations" and len(arguments) == 2:
            observations(*arguments)
        else:
            raise ValueError("usage: bootstrap-seed-release.py create REV INPUTS OUTPUT | verify REV ASSET DIRECTORY RELEASE_JSON | observations CSV ordinary|transition")
        print("bootstrap seed package " + command + " passed")
    except (ValueError, OSError, KeyError, TypeError) as error:
        sys.exit("bootstrap seed package: " + str(error))
