#!/usr/bin/env python3
"""The bundle comparison derives its authority from committed reference objects."""

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("official_sources", Path(__file__).with_name("official-sources.py"))
bundle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bundle)


class OfficialSourceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "native"
        self.reference = Path(self.temporary.name) / "reference checkout"
        self.root.mkdir()
        self.reference.mkdir()
        self.git("init", "-q")
        self.git("config", "user.name", "Source Test")
        self.git("config", "user.email", "source-test@example.invalid")
        self.git("config", "core.autocrlf", "false")
        self.source = self.reference / bundle.SOURCE_ROOT / "trb/sample/src/index.trb"
        self.source.parent.mkdir(parents=True)
        self.source.write_bytes(b"# preserved source\r\ndef sample(): String\n\treturn \"sample\"\nend\n")
        self.manifest = self.source.parent.parent / "trbpackage.json"
        self.manifest.write_text('{"name":"trb/sample","source":"src/index.trb"}\n')
        (self.reference / "LICENSE").write_text("Synthetic license\n")
        self.git("add", ".")
        self.git("commit", "-qm", "Synthetic reference")
        self.revision = self.git("rev-parse", "HEAD")
        (self.root / "TYPE_RB_REVISION").write_text(self.revision + "\n")
        bundle.sync(self.root, self.reference)
        self.vendored = self.root / bundle.BUNDLE / "packages/trb/sample/src/index.trb"

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.reference), *args], text=True).strip()

    def test_exact_bytes_and_deterministic_sync(self):
        first = bundle.bundle_files(self.root)
        self.assertEqual(self.vendored.read_bytes(), self.source.read_bytes())
        self.assertEqual(bundle.check(self.root, self.reference), 3)
        self.assertEqual(bundle.sync(self.root, self.reference), 3)
        self.assertEqual(first, bundle.bundle_files(self.root))
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_uses_pin_instead_of_head_or_dirty_working_files(self):
        self.source.write_text("replacement\n")
        self.git("add", ".")
        self.git("commit", "-qm", "Later reference")
        self.source.write_text("uncommitted replacement\n")
        before = self.git("status", "--porcelain")
        original = self.vendored.read_bytes()
        bundle.sync(self.root, self.reference)
        self.assertEqual(original, self.vendored.read_bytes())
        bundle.check(self.root, self.reference)
        self.assertEqual(self.git("status", "--porcelain"), before)

    def test_rejects_modified_missing_and_additional_files(self):
        self.vendored.write_text("changed\n")
        with self.assertRaisesRegex(bundle.ValidationError, "differs"):
            bundle.check(self.root, self.reference)
        self.vendored.unlink()
        with self.assertRaisesRegex(bundle.ValidationError, "missing"):
            bundle.check(self.root, self.reference)
        bundle.sync(self.root, self.reference)
        (self.vendored.parent / "extra.trb").write_text("extra\n")
        with self.assertRaisesRegex(bundle.ValidationError, "unexpected"):
            bundle.check(self.root, self.reference)
        bundle.sync(self.root, self.reference)
        bundle.check(self.root, self.reference)

    def test_rejects_forged_provenance_even_with_matching_local_hash(self):
        self.vendored.write_text("forged\n")
        provenance = self.root / bundle.BUNDLE / "provenance.json"
        data = json.loads(provenance.read_text())
        entry = next(row for row in data["files"] if row["path"].endswith("index.trb"))
        entry.update(bytes=self.vendored.stat().st_size,
                     sha256=hashlib.sha256(self.vendored.read_bytes()).hexdigest())
        provenance.write_text(json.dumps(data, indent=2) + "\n")
        with self.assertRaisesRegex(bundle.ValidationError, "differs"):
            bundle.check(self.root, self.reference)

    def test_rejects_stale_pin_and_unavailable_commit(self):
        self.source.write_text("new committed source\n")
        self.git("add", ".")
        self.git("commit", "-qm", "Changed pin")
        (self.root / "TYPE_RB_REVISION").write_text(self.git("rev-parse", "HEAD") + "\n")
        with self.assertRaisesRegex(bundle.ValidationError, "differs"):
            bundle.check(self.root, self.reference)
        (self.root / "TYPE_RB_REVISION").write_text("f" * 40 + "\n")
        with self.assertRaises(bundle.ValidationError):
            bundle.check(self.root, self.reference)

    def test_rejects_provenance_only_tampering(self):
        provenance = self.root / bundle.BUNDLE / "provenance.json"
        provenance.write_text(provenance.read_text().replace(bundle.REPOSITORY, "https://example.invalid/source"))
        with self.assertRaisesRegex(bundle.ValidationError, "provenance.json"):
            bundle.check(self.root, self.reference)

    def test_ignores_mutable_git_object_replacements(self):
        relative = self.source.relative_to(self.reference).as_posix()
        original_blob = self.git("rev-parse", self.revision + ":" + relative)
        self.source.write_text("replacement object\n")
        replacement_blob = self.git("hash-object", "-w", str(self.source))
        self.git("replace", original_blob, replacement_blob)
        original = self.vendored.read_bytes()
        bundle.sync(self.root, self.reference)
        self.assertEqual(self.vendored.read_bytes(), original)
        bundle.check(self.root, self.reference)

    def test_rejects_file_and_directory_symlinks_without_touching_target(self):
        self.vendored.unlink()
        self.vendored.symlink_to(self.source)
        original = self.source.read_bytes()
        for operation in (bundle.check, bundle.sync):
            with self.assertRaisesRegex(bundle.ValidationError, "symlink"):
                operation(self.root, self.reference)
        self.vendored.unlink()
        bundle.sync(self.root, self.reference)
        (self.root / bundle.BUNDLE / "external").symlink_to(self.reference, target_is_directory=True)
        with self.assertRaisesRegex(bundle.ValidationError, "symlink"):
            bundle.check(self.root, self.reference)
        self.assertEqual(original, self.source.read_bytes())

    def test_rejects_symlink_in_reference_commit(self):
        self.source.unlink()
        self.source.symlink_to("../../../../LICENSE")
        self.git("add", ".")
        self.git("commit", "-qm", "Invalid source object")
        (self.root / "TYPE_RB_REVISION").write_text(self.git("rev-parse", "HEAD") + "\n")
        with self.assertRaisesRegex(bundle.ValidationError, "regular file"):
            bundle.sync(self.root, self.reference)


if __name__ == "__main__":
    unittest.main()
