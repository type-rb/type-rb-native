import csv
from argparse import Namespace
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
    def test_self_compile_records_sizes_without_retaining_generated_artifacts(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            revision = "a" * 40
            compilers = root / "compilers"
            source = compilers / revision / "source/compiler/src/compiler.trb"
            source.parent.mkdir(parents=True)
            source.write_text("def main()\nend\n")
            evidence = root / "evidence"
            evidence.mkdir()

            def observed(command, directory, _timeout, **_kwargs):
                directory.mkdir()
                if command[1] == "emit-qbe":
                    (directory / "stdout").write_bytes(b"function l $main() {}\n")
                else:
                    (directory / "stdout").write_bytes(b"")
                    Path(command[command.index("--output") + 1]).write_bytes(b"compiler binary")
                (directory / "stderr").write_bytes(b"")
                return {"status": "pass", "wallSeconds": 1.0, "cpuSeconds": 0.8,
                        "memoryBytes": 1234}

            with patch.object(measure, "observe", side_effect=observed):
                result, records = measure.measure_self_compilation(
                    Namespace(compilers=str(compilers / "compilers.json"), qbe="qbe"),
                    {"native": {"revision": revision, "path": "compiler"}},
                    evidence, {}, 0)
            self.assertEqual(result["status"], "pass")
            self.assertEqual(result["ir"]["bytes"], len(b"function l $main() {}\n"))
            self.assertEqual(result["binaryBytes"], len(b"compiler binary"))
            self.assertEqual(len(records), 4)
            self.assertFalse(list((evidence / "compiler-self").rglob("compiler-[0-9]")))
            self.assertFalse((evidence / "compiler-self/emit-qbe/stdout").exists())
            self.assertTrue((evidence / "compiler-self/emit-qbe/observation.json").exists())

    def test_compiler_self_measurement_is_optional_but_complete_when_passing(self):
        old = snapshot()
        state.validate({**state.empty(), "latest": old})
        current = snapshot()
        current["compilerSelf"] = {
            "status": "pass", "sourceSha256": "b" * 64,
            "ir": {"sha256": "c" * 64, "bytes": 24000000,
                   "wallSeconds": 8, "cpuSeconds": 7.5, "memoryBytes": 200000000},
            "build": {"wallSeconds": 30, "cpuSeconds": 29, "memoryBytes": 300000000,
                      "wallMin": 29, "wallMax": 31},
            "binaryBytes": 2000000, "binarySha256": "d" * 64,
        }
        state.validate({**state.empty(), "latest": current, "history": [old]})
        for field, value in (("ir", None), ("binarySha256", "bad"), ("build", None)):
            invalid = copy.deepcopy(current)
            invalid["compilerSelf"][field] = value
            with self.assertRaises(ValueError):
                state.validate({**state.empty(), "latest": invalid})

    def test_nonperformance_changes_skip_but_runtime_and_inputs_do_not(self):
        for path in ["docs/example.md", "compiler/src/parser_test.trb", "README.md"]:
            self.assertFalse(state.relevant(path), path)
        for path in ["compiler/src/parser.trb", "src/runtime.trb", "TYPE_RB_REVISION",
                     "tools/daily-performance/measure.py", ".github/workflows/daily-performance.yml",
                     "tools/runtime-worker-soak/workload.trb", "tools/compiler-cost.sh"]:
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
        upstream = [case for case in cases if "pureGoSource" in case and case["id"] in hashes]
        self.assertEqual({case["id"] for case in upstream}, {"fannkuch-redux", "n-body", "spectral-norm"})
        for case in upstream:
            self.assertEqual(hashlib.sha256((state.ROOT / case["pureGoSource"]).read_bytes()).hexdigest(), hashes[case["id"]])

    def test_language_area_kernels_map_to_coverage_families(self):
        registry = state.read(state.ROOT / "tools/native-language-cases.json")
        families = {feature["id"] for feature in registry["features"]}
        cases = state.read(state.ROOT / "tools/daily-performance/suite.json")["cases"]
        kernels = [case for case in cases if case["source"].startswith("benchmarks/features/")]
        self.assertGreaterEqual(len(kernels), 9)
        self.assertEqual(len({case["id"] for case in cases}), len(cases))
        for case in kernels:
            self.assertIn(case["family"], families, case["id"])
            self.assertFalse(case["frozenBaseline"], case["id"])
            self.assertEqual(case["pureGoSource"], f"benchmarks/features/pure-go/{case['id']}/main.go")
            self.assertTrue((state.ROOT / case["pureGoSource"]).is_file(), case["id"])
            self.assertTrue((state.ROOT / f"benchmarks/features/{case['id']}/trbconfig.jsonc").is_file(), case["id"])

    def test_frozen_baseline_coverage_is_explicit_and_legacy_snapshots_require_it(self):
        current = snapshot()
        current["baselineCases"] = ["example"]
        kernel = [dict(copy.deepcopy(row), case="kernel", family="strings")
                  for row in current["rows"] if row["role"] != "baseline"]
        current["rows"].extend(kernel)
        state.validate({**state.empty(), "latest": current})
        legacy = copy.deepcopy(current); del legacy["baselineCases"]
        with self.assertRaises(ValueError): state.validate({**state.empty(), "latest": legacy})
        extra = copy.deepcopy(current)
        extra["rows"].append({**copy.deepcopy(kernel[0]), "role": "baseline"})
        with self.assertRaises(ValueError): state.validate({**state.empty(), "latest": extra})
        for invalid in ("not-a-list", ["example", "example"], ["missing"]):
            broken = copy.deepcopy(current); broken["baselineCases"] = invalid
            with self.assertRaises(ValueError): state.validate({**state.empty(), "latest": broken})
        family = copy.deepcopy(current); family["rows"][-1]["family"] = "Not a family"
        with self.assertRaises(ValueError): state.validate({**state.empty(), "latest": family})

    def test_weekly_profile_requires_all_languages_and_cases(self):
        weekly = snapshot()
        weekly["profile"] = "weekly"
        weekly["roles"] = {role: {"revision": "a" * 40} for role in ("native", "pure-go", "c", "cpp", "rust", "java")}
        template = weekly["rows"][0]
        weekly["rows"] = [{**copy.deepcopy(template), "role": role, "case": case}
                          for role in weekly["roles"] for case in ("fannkuch-redux", "n-body", "spectral-norm")]
        state.validate({**state.empty(), "latest": weekly})
        partial = copy.deepcopy(weekly); partial["rows"].pop()
        with self.assertRaises(ValueError): state.validate({**state.empty(), "latest": partial})
        wrong = copy.deepcopy(weekly); wrong["profile"] = "unknown"
        with self.assertRaises(ValueError): state.validate({**state.empty(), "latest": wrong})
        failed = copy.deepcopy(weekly); failed["rows"][0].update(status="timeout", runtime=None)
        state.validate({**state.empty(), "latest": failed})

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

    def test_simulated_run_produces_a_valid_snapshot_for_every_registered_case(self):
        suite = state.read(state.ROOT / "tools/daily-performance/suite.json")
        def observe(command, directory, timeout, cwd=None, env=None, core=None):
            directory.mkdir(parents=True, exist_ok=False)
            arguments = list(map(str, command))
            if arguments[1:2] == ["emit-qbe"]:
                (directory / "stdout").write_bytes(b"function l $main() {}\n")
            elif "--output" in arguments or "--outfile" in arguments or arguments[1:2] == ["build"]:
                output = arguments[arguments.index("--output" if "--output" in arguments else
                                                   "--outfile" if "--outfile" in arguments else "-o") + 1]
                Path(output).write_bytes(b"program")
                (directory / "stdout").write_bytes(b"")
            else:
                (directory / "stdout").write_bytes((Path(arguments[0]).parent.parent / "expected").read_bytes())
            (directory / "stderr").write_bytes(b"")
            record = {"command": arguments, "timeoutSeconds": timeout, "status": "pass", "wallSeconds": .5,
                      "exitCode": 0, "cpuSeconds": .4, "memoryBytes": 4096}
            state.write(directory / "observation.json", record)
            return record
        def check_output(command, *args, **kwargs):
            return b"go version go1.27 linux/arm64" if command[:2] == ["/usr/bin/go", "version"] or command == ["go", "version"] else b"host"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            compilers = {role: {"revision": "a" * 40, "path": str(root / role)}
                         for role in ("native", "previous", "baseline", "typerb-go")}
            for role in [*compilers, "go", "qbe"]:
                (root / role).write_bytes(role.encode())
            source = root / ("a" * 40) / "source/compiler/src/compiler.trb"
            source.parent.mkdir(parents=True)
            source.write_text("def main()\nend\n")
            state.write(root / "compilers.json", compilers)
            arguments = type("Arguments", (), {"compilers": root / "compilers.json", "qbe": root / "qbe",
                                               "evidence": root / "evidence", "output": root / "snapshot.json"})
            with patch.object(measure.platform, "system", return_value="Linux"), \
                 patch.object(measure.platform, "machine", return_value="aarch64"), \
                 patch.object(measure.platform, "platform", return_value="Linux-aarch64"), \
                 patch.object(measure.os, "sched_getaffinity", return_value={0}, create=True), \
                 patch.object(measure.shutil, "which", return_value=str(root / "go")), \
                 patch.object(measure.subprocess, "check_output", side_effect=check_output), \
                 patch.object(measure.subprocess, "run"), \
                 patch.object(measure, "observe", side_effect=observe), \
                 patch.object(measure, "git", return_value="a" * 40), \
                 patch("builtins.print"):
                measure.run(arguments)
            result = state.read(root / "snapshot.json")
        state.validate({**state.empty(), "latest": result})
        self.assertEqual(result["status"], "measured")
        self.assertEqual(result["compilerSelf"]["status"], "pass")
        self.assertEqual({row["case"] for row in result["rows"]}, {case["id"] for case in suite["cases"]})
        kernels = {case["id"] for case in suite["cases"] if not case.get("frozenBaseline", True)}
        self.assertTrue(kernels)
        self.assertFalse(any(row["role"] == "baseline" and row["case"] in kernels for row in result["rows"]))
        self.assertTrue(all(row.get("family") for row in result["rows"] if row["case"] in kernels))

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
