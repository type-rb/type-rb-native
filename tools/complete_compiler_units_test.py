"""Synthetic process-level controls for the complete compiler unit runner."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


RUNNER = Path(__file__).with_name("complete_compiler_units.py")
FAKE = r"""#!/usr/bin/env python3
import json
import os
from pathlib import Path
import sys
import time

path = os.environ["TRB_TEST_FILE"]
stem = Path(path).stem
mode = os.environ.get("FAKE_MODE", "")
if mode == "zero" and stem == "beta_test":
    print(json.dumps({"type": "test_summary", "total": 0, "failed": 0}))
    sys.exit(0)
if mode == "diagnostic" and stem == "beta_test":
    print("expected compiler diagnostic")
if mode == "timeout" and stem == "beta_test":
    time.sleep(2)
name = "same" if mode == "duplicate" else stem
event_path = "/wrong/source.trb" if mode == "wrong" else path
for kind in ("test_started", "test_failed" if mode == "fail" and stem == "beta_test" else "test_passed"):
    print(json.dumps({"type": kind, "name": name, "test_file": event_path}))
failed = int(mode == "fail" and stem == "beta_test")
print(json.dumps({"type": "test_summary", "total": 1, "failed": failed}))
sys.exit(failed)
"""


class CompleteCompilerUnitsTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        source = self.root / "compiler" / "src"
        source.mkdir(parents=True)
        for name in ("alpha_test.trb", "beta_test.trb"):
            (source / name).write_text('describe("synthetic") do\nend\n')
        self.binary = self.root / "fake-test-executable"
        self.binary.write_text(FAKE)
        self.binary.chmod(0o755)

    def run_runner(self, mode=""):
        environment = os.environ.copy()
        environment["FAKE_MODE"] = mode
        return subprocess.run(
            [sys.executable, str(RUNNER), "--root", str(self.root),
             "--binary", str(self.binary), "--scratch", str(self.root), "--jobs", "2",
             "--timeout-seconds", "1"],
            env=environment, capture_output=True, text=True, check=False,
        )

    def test_executes_each_file_once_and_reports_every_case(self):
        for mode in ("", "diagnostic"):
            with self.subTest(mode=mode):
                result = self.run_runner(mode)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("2 files, 2 tests", result.stdout)
                self.assertIn('"name": "alpha_test"', result.stdout)
                self.assertIn('"name": "beta_test"', result.stdout)

    def test_rejects_missing_wrong_duplicate_and_failed_cases(self):
        for mode, expected in (
            ("zero", "test summary does not match"),
            ("wrong", "test identity differs"),
            ("duplicate", "duplicate test names"),
            ("fail", "test executable exited"),
            ("timeout", "timed out after 1s"),
        ):
            with self.subTest(mode=mode):
                result = self.run_runner(mode)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected, result.stderr)


if __name__ == "__main__":
    unittest.main()
