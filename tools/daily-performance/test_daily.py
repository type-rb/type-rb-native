import csv
import hashlib
import copy
import io
import json
import os
from pathlib import Path
import platform
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).parent))
import state
import measure


def snapshot(status="measured"):
    metrics = {"wallSeconds": 1, "cpuSeconds": .9, "memoryBytes": 1024, "wallMin": .8, "wallMax": 1.2}
    roles = {role: {"revision": "a" * 40} for role in ("native", "previous", "baseline", "typerb-go")}
    return {"revision": "a" * 40, "status": status, "fingerprint": "old", "series": "series",
            "roles": roles, "rows": [{"case": "example", "role": role, "status": "pass",
                                     "runtime": dict(metrics), "build": dict(metrics)} for role in roles]}


class DailyTests(unittest.TestCase):
    def test_nonperformance_changes_skip_but_runtime_and_inputs_do_not(self):
        for path in ["docs/example.md", "compiler/src/parser_test.trb", "README.md"]:
            self.assertFalse(state.relevant(path), path)
        for path in ["compiler/src/parser.trb", "src/runtime.trb", "TYPE_RB_REVISION",
                     "tools/daily-performance/measure.py", ".github/workflows/daily-performance.yml",
                     "tools/runtime-worker-soak/workload.trb"]:
            self.assertTrue(state.relevant(path), path)

    def test_unchanged_and_forced_plans(self):
        with tempfile.TemporaryDirectory() as directory:
            path, output = Path(directory) / "state.json", Path(directory) / "output"
            state.write(path, {**state.empty(), "latest": snapshot()})
            with patch.object(state, "fingerprint", return_value="old"), patch.object(state, "series", return_value="series"), \
                 patch.object(state, "git", return_value="b" * 40), \
                 patch.dict(os.environ, {"GITHUB_REPOSITORY": "type-rb/type-rb-native", "GITHUB_RUN_ID": "42"}):
                state.plan(path, output, False)
                self.assertIn("measure=false", output.read_text())
                self.assertIsNone(state.read(path)["attempt"])
                output.unlink()
                state.plan(path, output, True)
                self.assertIn("measure=true", output.read_text())
                self.assertEqual(state.read(path)["attempt"]["status"], "running")

    def test_infrastructure_failure_preserves_previous_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            data = {**state.empty(), "latest": snapshot(), "attempt": {"status": "running"}}
            state.write(path, data)
            state.finish(path, Path(directory) / "missing.json", "failure")
            actual = state.read(path)
            self.assertEqual(actual["latest"], data["latest"])
            self.assertEqual(actual["attempt"]["status"], "infrastructure-failure")

    def test_regression_and_failed_cases_publish_without_green_filter(self):
        with tempfile.TemporaryDirectory() as directory:
            path, measurement = Path(directory) / "state.json", Path(directory) / "snapshot.json"
            data = {**state.empty(), "latest": snapshot(), "checked": {"fingerprint": "new"},
                    "attempt": {"status": "running", "runUrl": "https://github.com/type-rb/type-rb-native/actions/runs/42"}}
            candidate = snapshot("measured-with-failures")
            candidate["rows"][0].update(status="timeout", runtime=None)
            state.write(path, data)
            state.write(measurement, candidate)
            with patch.object(state, "series", return_value="series"):
                state.finish(path, measurement, "success")
            self.assertEqual(state.read(path)["latest"]["rows"][0]["status"], "timeout")
            self.assertEqual(state.read(path)["latest"]["fingerprint"], "new")

    def test_missing_duplicate_nonfinite_or_false_passing_rows_rejected(self):
        cases = []
        missing = snapshot(); missing["rows"].pop(); cases.append(missing)
        duplicate = snapshot(); duplicate["rows"].append(copy.deepcopy(duplicate["rows"][0])); cases.append(duplicate)
        nonfinite = snapshot(); nonfinite["rows"][0]["runtime"]["wallSeconds"] = float("nan"); cases.append(nonfinite)
        failed = snapshot(); failed["rows"][0]["status"] = "timeout"; cases.append(failed)
        partial = snapshot(); partial["rows"][0]["runtime"] = None; cases.append(partial)
        for item in cases:
            with self.assertRaises(ValueError):
                state.validate({**state.empty(), "latest": item})

    def test_pure_go_coverage_is_explicit_and_old_history_survives(self):
        old = snapshot()
        current = snapshot()
        current["rows"] = []
        current["pureGoCases"] = ["fannkuch-redux", "n-body", "spectral-norm"]
        current["roles"]["pure-go"] = {"revision": "b" * 40}
        for name in [*current["pureGoCases"], "startup"]:
            for role in current["roles"]:
                if name == "startup" and role == "pure-go": continue
                row = copy.deepcopy(old["rows"][0])
                row.update(case=name, role=role)
                current["rows"].append(row)
        state.validate({**state.empty(), "latest": current, "history": [old, current]})
        missing = copy.deepcopy(current)
        missing["rows"] = [r for r in missing["rows"] if not (r["case"] == "n-body" and r["role"] == "pure-go")]
        with self.assertRaises(ValueError): state.validate({**state.empty(), "latest": missing})
        extra = copy.deepcopy(current)
        extra["rows"].append({**copy.deepcopy(old["rows"][0]), "case": "startup", "role": "pure-go"})
        with self.assertRaises(ValueError): state.validate({**state.empty(), "latest": extra})

    def test_pure_go_sources_match_the_registered_upstream_bytes(self):
        with open(state.ROOT / "benchmarks/benchmarksgame/context-sources.tsv") as stream:
            hashes = {r["case"]: r["source_sha256"] for r in csv.DictReader(stream, delimiter="\t") if r["language"] == "go"}
        cases = state.read(state.ROOT / "tools/daily-performance/suite.json")["cases"]
        selected = [case for case in cases if "pureGoSource" in case]
        self.assertEqual(len(selected), 3)
        for case in selected:
            self.assertEqual(hashlib.sha256((state.ROOT / case["pureGoSource"]).read_bytes()).hexdigest(), hashes[case["id"]])

    def test_restore_rejects_same_name_from_unrelated_workflow(self):
        archive = io.BytesIO()
        with zipfile.ZipFile(archive, "w") as output:
            output.writestr("state.json", json.dumps(state.empty()))
            output.writestr("../escape", "never extracted")
        artifacts = [{"id": number, "expired": False, "size_in_bytes": 300,
                      "workflow_run": {"head_branch": "main", "id": number}} for number in (1, 2)]
        def gh(endpoint, binary=False):
            if endpoint.endswith("/daily-performance.yml"): return {"id": 100}
            if "?name=" in endpoint: return {"artifacts": artifacts}
            if "/runs/" in endpoint:
                return {"workflow_id": 99 if endpoint.endswith("/2") else 100, "status": "completed",
                        "event": "workflow_dispatch", "head_repository": {"full_name": "type-rb/type-rb-native"}}
            self.assertTrue(endpoint.endswith("/1/zip"))
            return archive.getvalue()
        with tempfile.TemporaryDirectory() as directory, patch.object(state, "gh", side_effect=gh), \
             patch.dict(os.environ, {"GITHUB_REPOSITORY": "type-rb/type-rb-native"}):
            path = Path(directory) / "state.json"
            state.restore(path)
            self.assertEqual(state.read(path), state.empty())
            self.assertFalse((Path(directory) / "escape").exists())

    def test_api_failure_is_not_empty_history(self):
        with patch.object(state, "gh", side_effect=RuntimeError("unavailable")), \
             patch.dict(os.environ, {"GITHUB_REPOSITORY": "type-rb/type-rb-native"}):
            with self.assertRaises(RuntimeError):
                state.restore("unused")

    def test_first_deployment_does_not_require_a_previously_registered_run(self):
        with tempfile.TemporaryDirectory() as directory, \
             patch.object(state, "gh", return_value={"artifacts": []}) as api, \
             patch.dict(os.environ, {"GITHUB_REPOSITORY": "type-rb/type-rb-native"}):
            path = Path(directory) / "state.json"
            state.restore(path)
            self.assertEqual(state.read(path), state.empty())
            self.assertEqual(api.call_count, 1)

    def test_warmups_excluded_and_partial_sample_medians_rejected(self):
        records = [{"phase": phase, "status": "pass", "wallSeconds": wall, "cpuSeconds": wall, "memoryBytes": 100}
                   for phase, wall in [("warmup", 100), ("retained", 1), ("retained", 2), ("retained", 3)]]
        self.assertEqual(measure.summarize(records, 3)["wallSeconds"], 2)
        self.assertIsNone(measure.summarize(records, 5))
        records[-1]["status"] = "output-mismatch"
        self.assertIsNone(measure.summarize(records, 3))

    def test_all_sources_have_exact_derivations_and_oracles(self):
        for case in state.read(state.ROOT / "tools/daily-performance/suite.json")["cases"]:
            with tempfile.TemporaryDirectory() as directory:
                expected = measure.source_case(case, Path(directory))
                self.assertTrue(expected.endswith(b"\n"))
                self.assertTrue((Path(directory) / "src/main.trb").exists())

    @unittest.skipUnless(platform.system() == "Linux", "GNU time is Linux-specific")
    def test_real_timeout_and_output_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            timeout = Path(directory) / "timeout"
            result = measure.observe([sys.executable, "-c", "import time; time.sleep(10)"], timeout, .1)
            self.assertEqual(result["status"], "timeout")
            wrong = Path(directory) / "wrong"
            result = measure.observe([sys.executable, "-c", "print('wrong')"], wrong, 5)
            self.assertEqual(measure.correct(result, wrong, b"right\n")["status"], "output-mismatch")


if __name__ == "__main__":
    unittest.main()
