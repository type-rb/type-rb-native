#!/usr/bin/env python3
"""Fail-closed dependency identity and capability controls."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qbe_toolchain as qbe


class BackendTest(unittest.TestCase):
    def test_identity_and_patch_tampering(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(qbe.ROOT / "tools/qbe", root / "tools/qbe")
            original = qbe.backend_identity(root)
            self.assertEqual(original["variant"], "typerb-arm64-memory-v2")
            manifest = root / "tools/qbe/backend.json"
            for key, value in (("variant", "stock"), ("version", "1.4"),
                               ("patches", []), ("patches", original["patches"][::-1]),
                               ("patches", [original["patches"][0]] * 2), ("sourceSHA256", "invalid")):
                with self.subTest(key=key):
                    changed = copy.deepcopy(original)
                    changed[key] = value
                    manifest.write_text(json.dumps(changed))
                    with self.assertRaises(ValueError):
                        qbe.backend_identity(root)
            manifest.write_text(json.dumps(original))
            for item in original["patches"]:
                path = root / item["path"]
                text = path.read_text()
                path.write_text(text + "changed\n")
                with self.assertRaisesRegex(ValueError, "patch digest"):
                    qbe.backend_identity(root)
                path.write_text(text)

    def test_corrupt_archive_is_rejected_before_unpacking(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "source.tar.xz"
            archive.write_bytes(b"corrupt source")
            with patch.object(qbe.subprocess, "run") as run:
                with self.assertRaisesRegex(ValueError, "archive digest"):
                    qbe.build(root / "output", archive)
                run.assert_not_called()
            self.assertFalse((root / "output/qbe").exists())

    def test_stock_or_partial_backend_cannot_pass_capability(self):
        for status, assembly in ((1, ""), (0, "call sqrt"), (0, "fsqrt d0, d0")):
            with self.subTest(status=status, assembly=assembly):
                with patch.object(qbe.subprocess, "run", return_value=subprocess.CompletedProcess(
                        [], status, assembly, "unsupported")):
                    with self.assertRaisesRegex(ValueError, "required"):
                        qbe.check_capability(Path("synthetic-qbe"))

    def test_verified_cache_requires_matching_binary_and_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            binary = root / "qbe"
            binary.write_bytes(b"not a verified binary")
            (root / "build-info.json").write_text(json.dumps({"inputs": {}, "binarySHA256": qbe.digest(binary)}))
            archive = root / "source.tar.xz"
            archive.write_bytes(b"corrupt source")
            with self.assertRaisesRegex(ValueError, "archive digest"):
                qbe.build(root, archive)
            self.assertEqual(binary.read_bytes(), b"not a verified binary")

    def test_constant_memory_backend_does_not_claim_indexed_capability(self):
        previous = ("fsqrt d0, d0\nadd x0, x0, #7\nand x0, x0, #65535\nasr x0, x0, #1\n"
                    "ldr x0, [x1, #8]\nstr x0, [x1, #16]\n")
        with patch.object(qbe.subprocess, "run", return_value=subprocess.CompletedProcess(
                [], 0, previous, "")):
            with self.assertRaisesRegex(ValueError, "indexed memory"):
                qbe.check_capability(Path("synthetic-previous-qbe"))


if __name__ == "__main__":
    unittest.main()
