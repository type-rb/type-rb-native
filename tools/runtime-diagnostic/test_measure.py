"""Controls for diagnostic identities, failed observations and first executions."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("hardware_diagnostic", ROOT / "measure.py")
diagnostic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diagnostic)


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


if __name__ == "__main__":
    unittest.main()
