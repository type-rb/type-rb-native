#!/usr/bin/env python3
"""Validate the tracked TypeRB Native compatibility declaration."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


class ValidationError(Exception):
    pass


def _reject_duplicate_members(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"duplicate JSON object member: {key}")
        result[key] = value
    return result


def load_json_text_strict(source: str, label: str) -> Any:
    try:
        return json.loads(source, object_pairs_hook=_reject_duplicate_members)
    except json.JSONDecodeError as error:
        raise ValidationError(
            f"{label}: invalid JSON at line {error.lineno}, column {error.colno}: {error.msg}"
        ) from error


def load_json_strict(path: Path) -> Any:
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as error:
        raise ValidationError(f"cannot read {path}: {error}") from error
    return load_json_text_strict(source, str(path))


def _json_type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "null":
        return value is None
    raise ValidationError(f"schema uses unsupported type {expected!r}")


def validate_schema(instance: Any, schema: dict[str, Any], location: str = "$") -> None:
    expected_type = schema.get("type")
    if expected_type is not None and not _json_type_matches(instance, expected_type):
        raise ValidationError(f"{location}: expected {expected_type}")

    if "const" in schema and instance != schema["const"]:
        raise ValidationError(f"{location}: expected constant {schema['const']!r}")
    if "enum" in schema and instance not in schema["enum"]:
        raise ValidationError(f"{location}: value is not in the allowed set")

    if isinstance(instance, str) and "pattern" in schema:
        try:
            matched = re.search(schema["pattern"], instance)
        except re.error as error:
            raise ValidationError(f"{location}: invalid schema pattern: {error}") from error
        if matched is None:
            raise ValidationError(f"{location}: value does not match the required pattern")

    if isinstance(instance, dict):
        required = schema.get("required", [])
        missing = [key for key in required if key not in instance]
        if missing:
            raise ValidationError(f"{location}: missing required member {missing[0]!r}")

        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            unknown = [key for key in instance if key not in properties]
            if unknown:
                raise ValidationError(f"{location}: unknown member {unknown[0]!r}")
        for key, value in instance.items():
            if key in properties:
                validate_schema(value, properties[key], f"{location}.{key}")

    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            raise ValidationError(f"{location}: array has too few items")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            raise ValidationError(f"{location}: array has too many items")
        if schema.get("uniqueItems"):
            encoded = [json.dumps(value, sort_keys=True, separators=(",", ":")) for value in instance]
            if len(encoded) != len(set(encoded)):
                raise ValidationError(f"{location}: array items must be unique")
        item_schema = schema.get("items")
        if item_schema is not None:
            for index, value in enumerate(instance):
                validate_schema(value, item_schema, f"{location}[{index}]")


def _canonical_line(path: Path) -> str:
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as error:
        raise ValidationError(f"cannot read canonical input {path}: {error}") from error
    if not source.endswith("\n") or source.count("\n") != 1:
        raise ValidationError(f"{path}: expected exactly one newline-terminated value")
    value = source[:-1]
    if not value:
        raise ValidationError(f"{path}: canonical value is empty")
    return value


def _repository_path(root: Path, relative: str) -> Path:
    if Path(relative).is_absolute():
        raise ValidationError(f"evidence path must be relative: {relative}")
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as error:
        raise ValidationError(f"evidence path escapes the repository: {relative}") from error
    if not candidate.is_file():
        raise ValidationError(f"evidence file does not exist: {relative}")
    return candidate


def _require_text(path: Path, values: list[str], label: str) -> str:
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as error:
        raise ValidationError(f"cannot read {path}: {error}") from error
    for value in values:
        if value not in source:
            raise ValidationError(f"{label}: canonical value {value!r} is absent from {path}")
    return source


def _expected_targets(seed_manifest: dict[str, Any]) -> list[dict[str, str]]:
    targets: list[dict[str, str]] = []
    for target in seed_manifest["targets"]:
        targets.append(
            {
                "profile": target["profile"],
                "status": "experimental",
                "os": target["os"],
                "architecture": target["architecture"],
                "qbeTarget": target["qbeTarget"],
                "ccBoundary": target["ccBoundary"],
            }
        )
    return targets


def validate_repository_values(
    root: Path, manifest: dict[str, Any], reference_trb: Path | None = None
) -> None:
    native_version = _canonical_line(root / "NATIVE_VERSION")
    type_rb_revision = _canonical_line(root / "TYPE_RB_REVISION")
    if manifest["nativeVersion"] != native_version:
        raise ValidationError("nativeVersion disagrees with NATIVE_VERSION")
    if manifest["typeRB"]["revision"] != type_rb_revision:
        raise ValidationError("typeRB.revision disagrees with TYPE_RB_REVISION")

    workflow = _require_text(
        root / ".github/workflows/gate-zero.yml",
        [f"ref: {type_rb_revision}"],
        "reference checkout",
    )
    checkout_revisions = re.findall(r"(?m)^\s*ref:\s*([0-9a-f]{40})\s*$", workflow)
    if checkout_revisions != [type_rb_revision]:
        raise ValidationError("gate-zero reference checkout is not the single exact TypeRB revision")

    if reference_trb is not None:
        try:
            completed = subprocess.run(
                [str(reference_trb), "version"],
                check=False,
                capture_output=True,
                text=True,
            )
        except OSError as error:
            raise ValidationError(f"cannot execute reference compiler {reference_trb}: {error}") from error
        reported = completed.stdout.rstrip("\n")
        if completed.returncode != 0 or completed.stderr or "\n" in reported:
            raise ValidationError("reference compiler did not return one clean version line")
        if reported != manifest["typeRB"]["version"]:
            raise ValidationError("typeRB.version disagrees with the pinned reference compiler")

    snapshot_version = manifest["bootstrap"]["snapshotSchemaVersion"]
    snapshot_source = _require_text(
        root / "src/gate3_snapshot.trb",
        [f"if version != {snapshot_version}"],
        "bootstrap snapshot",
    )
    if not re.search(rf"if version != {snapshot_version}\b", snapshot_source):
        raise ValidationError("snapshotSchemaVersion disagrees with the current decoder")
    if f"--snapshot-version {snapshot_version}" not in workflow:
        raise ValidationError("snapshotSchemaVersion disagrees with the bootstrap workflow")

    seed_manifest_path = (
        root
        / "results/2026-08-30-gate6l-bootstrap-seed-darwin-linux-arm64/release/"
        "type-rb-native-bootstrap-manifest-v1.json"
    )
    seed_manifest = load_json_strict(seed_manifest_path)
    seed = manifest["bootstrap"]["seed"]
    if seed["releaseTag"] != seed_manifest["releaseTag"]:
        raise ValidationError("bootstrap seed releaseTag disagrees with the retained release manifest")
    if seed["manifestSchemaVersion"] != seed_manifest["schemaVersion"]:
        raise ValidationError("bootstrap seed manifestSchemaVersion disagrees with the retained release manifest")
    if seed["status"] != seed_manifest["status"]:
        raise ValidationError("bootstrap seed status disagrees with the retained release manifest")

    expected_backend = {
        "name": seed_manifest["backend"]["name"],
        "version": seed_manifest["backend"]["version"],
        "sourceURL": seed_manifest["backend"]["sourceUrl"],
        "sourceSHA256": seed_manifest["backend"]["sourceSha256"],
    }
    if manifest["backend"] != expected_backend:
        raise ValidationError("backend identity disagrees with the retained release manifest")

    expected_targets = _expected_targets(seed_manifest)
    if manifest["targets"] != expected_targets:
        raise ValidationError("target profiles disagree with the retained release manifest")

    compiler_source = _require_text(
        root / "compiler/gate4/src/compiler.trb",
        [
            *[f'b \\"{target["profile"]}\\"' for target in expected_targets],
            *[f'b \\"{target["qbeTarget"]}\\"' for target in expected_targets],
        ],
        "self-hosted target profile",
    )
    if not compiler_source:
        raise ValidationError("self-hosted compiler source is empty")

    bootstrap_tool = (root / "tools/bootstrap-seed.sh").read_text(encoding="utf-8")
    for target in expected_targets:
        mapping = re.compile(
            rf"(?m)^{re.escape(target['profile'])}\)\n"
            rf"\s*os={re.escape(target['os'])}\n"
            rf"\s*architecture={re.escape(target['architecture'])}\n"
            rf"\s*qbe_target={re.escape(target['qbeTarget'])}\n"
        )
        if mapping.search(bootstrap_tool) is None:
            raise ValidationError(f"target profile {target['profile']} disagrees with bootstrap tooling")

    seed_tool = _require_text(
        root / "tools/bootstrap-seed-manifest.sh",
        [
            f"RELEASE_TAG={seed['releaseTag']}",
            f"QBE_SOURCE_URL={expected_backend['sourceURL']}",
            f"QBE_SOURCE_SHA256={expected_backend['sourceSHA256']}",
            f'version: "{expected_backend["version"]}"',
        ],
        "bootstrap and backend identity",
    )
    if not seed_tool:
        raise ValidationError("bootstrap seed manifest tool is empty")

    compatibility_evidence = manifest["evidence"]["compatibility"]
    compatibility_path = _repository_path(root, compatibility_evidence["result"])
    _require_text(
        compatibility_path,
        [
            manifest["typeRB"]["version"],
            manifest["typeRB"]["revision"],
            compatibility_evidence["nativeRevision"],
            compatibility_evidence["workflow"],
        ],
        "compatibility evidence",
    )

    bootstrap_evidence = manifest["evidence"]["bootstrap"]
    bootstrap_path = _repository_path(root, bootstrap_evidence["result"])
    _require_text(
        bootstrap_path,
        [
            bootstrap_evidence["nativeRevision"],
            seed["releaseTag"],
            bootstrap_evidence["release"],
        ],
        "bootstrap evidence",
    )
    if not bootstrap_evidence["release"].endswith("/" + seed["releaseTag"]):
        raise ValidationError("bootstrap evidence release disagrees with bootstrap.seed.releaseTag")


def validate_manifest_data(
    root: Path,
    manifest: dict[str, Any],
    schema: dict[str, Any],
    reference_trb: Path | None = None,
) -> None:
    validate_schema(manifest, schema)
    validate_repository_values(root, manifest, reference_trb)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    default_root = Path(__file__).resolve().parent.parent
    parser.add_argument("--root", type=Path, default=default_root)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--schema", type=Path)
    parser.add_argument("--reference-trb", type=Path)
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    root = arguments.root.resolve()
    manifest_path = arguments.manifest or root / "compatibility/current.json"
    schema_path = arguments.schema or root / "compatibility/schema-v1.json"
    try:
        manifest = load_json_strict(manifest_path)
        schema = load_json_strict(schema_path)
        if not isinstance(manifest, dict) or not isinstance(schema, dict):
            raise ValidationError("manifest and schema roots must be JSON objects")
        validate_manifest_data(root, manifest, schema, arguments.reference_trb)
    except ValidationError as error:
        print(f"compatibility-manifest: {error}", file=sys.stderr)
        return 1
    print(
        "compatibility-manifest: valid "
        f"Native {manifest['nativeVersion']} -> "
        f"TypeRB {manifest['typeRB']['version']}@{manifest['typeRB']['revision']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
