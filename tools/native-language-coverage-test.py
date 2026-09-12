#!/usr/bin/env python3
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch, Mock

spec = importlib.util.spec_from_file_location("coverage", Path(__file__).with_name("native-language-coverage.py"))
coverage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(coverage)


class LanguageCoverageTests(unittest.TestCase):
    def setUp(self):
        self.document = json.loads(Path(__file__).with_name("native-language-cases.json").read_text())

    def test_registry_and_distinct_execution_paths(self):
        cases = coverage.validate(self.document)
        self.assertEqual(len(cases), 19)
        utf8 = next(case for case in cases if case["id"] == "utf8-string")
        expected = coverage.expected_native(utf8)
        self.assertEqual(expected["check"]["code"], 0)
        self.assertEqual(expected["build"]["code"], 1)
        self.assertIsNone(expected["execute"])
        self.assertEqual(expected["repl"]["code"], 0)
        self.assertNotEqual(expected["repl"]["stderr"], "")

    def test_empty_duplicate_unknown_or_unreviewed_registry_is_rejected(self):
        mutations = [lambda d: d.update(schemaVersion=True), lambda d: d.update(extra=1),
                     lambda d: d.update(cases=[]), lambda d: d["cases"].append(copy.deepcopy(d["cases"][0])),
                     lambda d: d["cases"][0].update(native=None), lambda d: d["cases"][0].update(extra=1),
                     lambda d: d["cases"][0].update(id="../outside"),
                     lambda d: d["cases"][0]["native"].update(check=""),
                     lambda d: d["cases"][0]["native"]["repl"].update(code=1)]
        for mutation in mutations:
            document = copy.deepcopy(self.document)
            mutation(document)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                coverage.validate(document)

    def test_table_does_not_count_session_exit_zero_as_feature_support(self):
        table = coverage.coverage_table(coverage.validate(self.document))
        self.assertIn("| UTF-8 String literal | accepts | rejects | not reached | rejects |", table)
        self.assertIn("| while | accepts | accepts | matches reference | output differs |", table)
        self.assertIn("| elsif | accepts | accepts | matches reference | matches reference |", table)
        self.assertIn("Array&lt;Boolean&gt;", table)
        self.assertEqual(table, coverage.coverage_table(self.document["cases"]))

    def test_exact_output_and_diagnostics_are_not_normalized_away(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            observed = coverage.observe(Path(sys.executable),
                                        ["-c", "import os,sys; print(os.getcwd()); print('diagnostic',file=sys.stderr); sys.exit(7)"], root)
        self.assertEqual(observed, {"code": 7, "stdout": "<case>\n", "stderr": "diagnostic\n"})

    def test_timeout_kills_the_owned_process_group_and_remains_failure(self):
        child = Mock(pid=123, returncode=-9)
        child.communicate.side_effect = [subprocess.TimeoutExpired("synthetic", 30), ("partial", "error")]
        with patch.object(coverage.subprocess, "Popen", return_value=child) as spawn, patch.object(coverage.os, "killpg") as kill:
            observed = coverage.observe(Path("/synthetic"), [], Path("/case"))
        self.assertTrue(spawn.call_args.kwargs["start_new_session"])
        kill.assert_called_once_with(123, coverage.signal.SIGKILL)
        self.assertEqual(observed, {"code": 124, "stdout": "partial", "stderr": "error", "timedOut": True})

    def test_invalid_reference_input_cannot_be_counted_as_native_gap(self):
        failure = {"code": 1, "stdout": "", "stderr": "invalid source"}
        with tempfile.TemporaryDirectory() as temporary, patch.object(coverage, "observe", return_value=failure):
            with self.assertRaisesRegex(ValueError, "invalid reference fixture"):
                coverage.collect(self.document["cases"][0], None, Path("/reference"), Path(temporary))

    def test_changed_native_observation_fails_without_rewriting_expectations(self):
        case = self.document["cases"][0]
        wrong = copy.deepcopy(coverage.expected_native(case))
        wrong["execute"]["stdout"] = "wrong\n"
        registry = Path(__file__).with_name("native-language-cases.json")
        before = registry.read_bytes()
        for observe, status in ((False, 1), (True, 0)):
            argv = ["coverage", "--native", sys.executable, "--case", case["id"]]
            if observe:
                argv.append("--observe")
            with patch.object(sys, "argv", argv), patch.object(coverage, "collect", return_value={"native": wrong}), patch("builtins.print"):
                self.assertEqual(coverage.main(), status)
            self.assertEqual(registry.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
