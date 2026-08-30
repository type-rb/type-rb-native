#!/usr/bin/env python3

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

from compatibility_manifest import (  # noqa: E402
    ValidationError,
    load_json_strict,
    load_json_text_strict,
    validate_manifest_data,
)


class CompatibilityManifestTest(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = load_json_strict(ROOT / "compatibility/current.json")
        self.schema = load_json_strict(ROOT / "compatibility/schema-v1.json")

    def validate(self, manifest: dict) -> None:
        validate_manifest_data(ROOT, manifest, self.schema)

    def test_current_manifest_is_valid(self) -> None:
        self.validate(self.manifest)

    def test_unknown_and_missing_members_are_rejected(self) -> None:
        unknown = copy.deepcopy(self.manifest)
        unknown["implicitSupport"] = True
        with self.assertRaisesRegex(ValidationError, "unknown member"):
            self.validate(unknown)

        missing = copy.deepcopy(self.manifest)
        del missing["runtimeABI"]
        with self.assertRaisesRegex(ValidationError, "missing required member"):
            self.validate(missing)

    def test_duplicate_members_are_rejected_before_validation(self) -> None:
        duplicate = '{"schemaVersion":1,"schemaVersion":2}'
        with self.assertRaisesRegex(ValidationError, "duplicate JSON object member"):
            load_json_text_strict(duplicate, "duplicate fixture")

    def test_only_exact_typerb_support_is_allowed(self) -> None:
        ranged = copy.deepcopy(self.manifest)
        ranged["typeRB"]["supportMode"] = "range"
        with self.assertRaisesRegex(ValidationError, "expected constant 'exact'"):
            self.validate(ranged)

    def test_canonical_repository_identities_must_match(self) -> None:
        mutations = [
            ("Native version", lambda value: value.update(nativeVersion="0.1.1-dev"), "NATIVE_VERSION"),
            (
                "TypeRB revision",
                lambda value: value["typeRB"].update(revision="a" * 40),
                "TYPE_RB_REVISION",
            ),
            (
                "snapshot schema",
                lambda value: value["bootstrap"].update(snapshotSchemaVersion=5),
                "bootstrap snapshot",
            ),
            (
                "target profile",
                lambda value: value["targets"][0].update(profile="darwin-arm64-v1"),
                "target profiles",
            ),
            (
                "backend identity",
                lambda value: value["backend"].update(version="1.4"),
                "backend identity",
            ),
        ]
        for label, mutate, message in mutations:
            with self.subTest(label=label):
                changed = copy.deepcopy(self.manifest)
                mutate(changed)
                with self.assertRaisesRegex(ValidationError, message):
                    self.validate(changed)

    def test_evidence_paths_cannot_escape_the_repository(self) -> None:
        escaped = copy.deepcopy(self.manifest)
        escaped["evidence"]["compatibility"]["result"] = "results/../../README.md"
        with self.assertRaisesRegex(ValidationError, "escapes the repository"):
            self.validate(escaped)


if __name__ == "__main__":
    unittest.main()
