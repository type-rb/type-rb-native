"""Controls for diagnostic identities, failed observations and first executions."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("hardware_diagnostic", ROOT / "measure.py")
diagnostic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diagnostic)
from reuse import PREFIX, unpack_verified, validate_reuse, verified_compiler, verified_program


class DiagnosticTest(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT / "registration.json").read_text())

    def test_registered_public_inputs_are_unchanged(self):
        diagnostic.validate_registration(self.plan)

    def test_floating_sources_and_changed_workloads_are_rejected(self):
        for field, value in (("revision", "main"), ("appSHA256", {})):
            plan = copy.deepcopy(self.plan)
            plan["variants"]["accepted"][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                diagnostic.validate_registration(plan)
        self.plan["suiteSHA256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "workload suite changed"):
            diagnostic.validate_registration(self.plan)

    def test_reruns_do_not_replace_a_completed_cohort(self):
        with patch.dict(os.environ, {"GITHUB_RUN_ATTEMPT": "2"}):
            with self.assertRaisesRegex(ValueError, "retry"):
                diagnostic.validate_registration(self.plan)

    def test_first_execution_and_unresolved_cpu_remain_visible(self):
        records = [{"phase": "first" if n == 0 else "steady", "status": "pass",
                    "wallSeconds": 10 if n == 0 else 1, "cpuSeconds": 0,
                    "memoryBytes": 1024} for n in range(6)]
        result = diagnostic.summary(records)
        self.assertEqual(result["wallSeconds"], 1)
        self.assertEqual(result["allWallSpread"], 10)
        self.assertEqual(result["steadyWallSpread"], 1)
        self.assertFalse(result["cpuResolved"])
        records[0]["status"] = "output-mismatch"
        self.assertIsNone(diagnostic.summary(records))
        self.assertIsNone(diagnostic.summary(records[1:]))

    def test_reuse_requires_exact_archive_and_preparation_identifiers(self):
        valid = {"runId": 1, "artifactId": 2, "archiveSHA256": "a" * 64,
                 "controllerRevision": "b" * 40}
        validate_reuse(valid)
        for key, value in (("runId", True), ("artifactId", -1),
                           ("archiveSHA256", "latest"), ("controllerRevision", "main")):
            changed = dict(valid, **{key: value})
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_reuse(changed)
        plan = copy.deepcopy(self.plan)
        plan["reuse"] = valid
        plan["variants"]["accepted"]["reusedRole"] = "../other"
        with self.assertRaisesRegex(ValueError, "preparation mode"):
            diagnostic.validate_registration(plan)

    def test_changed_archive_and_unsafe_members_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "evidence.zip"
            with zipfile.ZipFile(archive, "w") as packed:
                packed.writestr(PREFIX + "../outside", b"untrusted")
            with self.assertRaisesRegex(ValueError, "digest differs"):
                unpack_verified(archive, root / "output", "0" * 64)
            with self.assertRaisesRegex(ValueError, "Unsafe"):
                unpack_verified(archive, root / "output", diagnostic.digest(archive))
            self.assertFalse((root / "outside").exists())

    def test_archive_reuse_extracts_only_registered_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "evidence.zip"
            with zipfile.ZipFile(archive, "w") as packed:
                packed.writestr(PREFIX + "context.json", b"{}")
                packed.writestr("unrelated/file", b"not evidence")
            output = root / "output"
            unpack_verified(archive, output, diagnostic.digest(archive))
            self.assertEqual([p.name for p in output.iterdir()], ["context.json"])

    def test_reused_binary_tampering_and_unclosed_compilers_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            directory = root / "compilers/accepted"
            (directory / "3").mkdir(parents=True)
            compiler = directory / "3/compiler"
            compiler.write_bytes(b"verified compiler")
            identity = {"sha256": diagnostic.digest(compiler), "bytes": compiler.stat().st_size}
            generations = directory / "generations.json"
            generations.write_text(json.dumps([identity] * 4))
            self.assertEqual(verified_compiler(root, "accepted"), compiler)
            generations.write_text(json.dumps([identity]))
            with self.assertRaisesRegex(ValueError, "fixed point"):
                verified_compiler(root, "accepted")
            generations.write_text(json.dumps([identity] * 4))
            compiler.write_bytes(b"changed compiler")
            with self.assertRaisesRegex(ValueError, "identity differs"):
                verified_compiler(root, "accepted")
            (root / "program").write_bytes(b"changed app")
            with self.assertRaisesRegex(ValueError, "identity differs"):
                verified_program(root, identity)


if __name__ == "__main__":
    unittest.main()
