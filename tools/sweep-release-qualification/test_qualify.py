import unittest
import qualify


class TradeTests(unittest.TestCase):
    def setUp(self):
        self.rows, self.groups = {}, {}
        for case in ("allocation", "control"):
            for role, build, run in (("native", 1.1, .9), ("previous", 1., 1.), ("typerb-go", 2., 1.), ("pure-go", 1.5, 1.)):
                self.rows[(case, role)] = {"build": {"wallSeconds": build, "cpuSeconds": build, "memoryBytes": 100},
                    "runtime": {"wallSeconds": run, "cpuSeconds": run, "memoryBytes": 100}, "artifactBytes": 100}
                self.groups[(case, role, "runtime")] = [{"phase": "retained", "wallSeconds": run}] * 5

    def test_cost_trade_requires_retained_competitor_advantage(self):
        self.assertEqual(qualify.evaluate_trade(self.rows, self.groups)["status"], "met")
        self.rows[("allocation", "pure-go")]["build"]["wallSeconds"] = 1.05
        self.assertIn("allocation/lost-build-advantage/pure-go", qualify.evaluate_trade(self.rows, self.groups)["failures"])

    def test_investigation_ceiling_and_runtime_benefit_still_block(self):
        self.rows[("allocation", "native")]["build"]["wallSeconds"] = 1.26
        for case in ("allocation", "control"):
            self.rows[(case, "native")]["runtime"]["cpuSeconds"] = .96
        r = qualify.evaluate_trade(self.rows, self.groups)
        self.assertIn("allocation/build/wallSeconds", r["failures"])
        self.assertIn("allocation/no-case-meets-both-5-percent-and-1-ms", r["failures"])

    def test_below_resolution_is_not_pass(self):
        self.rows[("allocation", "previous")]["runtime"]["cpuSeconds"] = 0
        self.assertEqual(qualify.evaluate_trade(self.rows, self.groups)["status"], "unmet")

    def test_gc_memory_regression_not_traded(self):
        self.rows[("allocation", "native")]["runtime"]["memoryBytes"] = 106
        self.assertIn("allocation/runtime/memoryBytes", qualify.evaluate_trade(self.rows, self.groups)["failures"])

    def test_missing_pure_go_is_explicit(self):
        del self.rows[("allocation", "pure-go")]
        self.assertEqual(qualify.evaluate_trade(self.rows, self.groups)["missingComparators"], ["allocation"])

    def test_failed_or_incomplete_cohort_is_rejected(self):
        with self.assertRaises((ValueError, KeyError)):
            qualify.assess({"registration": {"candidate": "a" * 40}}, {"revision": "a" * 40, "status": "measured-with-failures"}, [])

    def test_candidate_zero_cpu_is_unknown(self):
        self.rows[("allocation", "native")]["runtime"]["cpuSeconds"] = 0
        self.assertEqual(qualify.evaluate_trade(self.rows, self.groups)["status"], "unmet")

    def test_reference_build_advantage_is_required_even_if_previously_lost(self):
        self.rows[("allocation", "typerb-go")]["build"]["wallSeconds"] = .8
        self.assertIn("allocation/not-faster-build/typerb-go", qualify.evaluate_trade(self.rows, self.groups)["failures"])

    def test_missing_pure_go_cannot_authorize_increased_build_cost(self):
        del self.rows[("allocation", "pure-go")]
        self.assertIn("allocation/build-trade/missing-pure-go", qualify.evaluate_trade(self.rows, self.groups)["unknown"])

    def test_comparator_warmup_outlier_is_reported(self):
        self.groups[("allocation", "typerb-go", "runtime")].append({"phase": "warmup", "wallSeconds": 2.1})
        self.assertIn("allocation/outlier/typerb-go", qualify.evaluate_trade(self.rows, self.groups)["failures"])

    def test_absolute_build_cost_and_runtime_savings_are_explicit(self):
        row = qualify.evaluate_trade(self.rows, self.groups)["ratios"]["allocation"]
        self.assertAlmostEqual(row["buildWallAddedSeconds"], .1)
        self.assertAlmostEqual(row["runtimeWallSavedSeconds"], .1)

    def test_primary_wall_and_cpu_cannot_be_combined_across_cases(self):
        self.rows[("allocation", "native")]["runtime"]["cpuSeconds"] = .99
        self.rows[("control", "native")]["runtime"]["wallSeconds"] = .99
        self.assertIn("allocation/no-case-meets-both-5-percent-and-1-ms", qualify.evaluate_trade(self.rows, self.groups)["failures"])

    def test_other_case_cannot_replace_primary(self):
        self.rows[("allocation", "native")]["runtime"]["cpuSeconds"] = .99
        self.assertEqual(qualify.evaluate_trade(self.rows, self.groups)["qualifiedPrimaries"], [])

    def test_primary_absolute_saving_is_required(self):
        for case in ("allocation", "control"):
            self.rows[(case, "previous")]["runtime"]["wallSeconds"] = .001
            self.rows[(case, "native")]["runtime"]["wallSeconds"] = .0009
        self.assertIn("allocation/no-case-meets-both-5-percent-and-1-ms", qualify.evaluate_trade(self.rows, self.groups)["failures"])


class PreparationTests(unittest.TestCase):
    def test_registered_go_flags_are_exact(self):
        qualify.check_go_flags("-trimpath")
        for flags in ("", "-race", "-trimpath -race"):
            with self.assertRaises(ValueError):
                qualify.check_go_flags(flags)


class IdentityTests(unittest.TestCase):
    def test_every_build_and_runtime_hash_matches_selected_artifact(self):
        identity = "a" * 64
        rows = {("allocation", "typerb-go"): {"artifactSha256": identity}}
        groups = {("allocation", "typerb-go", kind): [{"artifact": {"sha256": identity}}] * count
                  for kind, count in (("build", 4), ("runtime", 6))}
        self.assertEqual(qualify.artifact_failures(rows, groups), [])
        groups[("allocation", "typerb-go", "build")][0] = {"artifact": {"sha256": "b" * 64}}
        self.assertEqual(qualify.artifact_failures(rows, groups),
                         ["allocation/typerb-go/build/artifact-identity"])
        groups[("allocation", "typerb-go", "runtime")][0] = {}
        self.assertIn("allocation/typerb-go/runtime/artifact-identity", qualify.artifact_failures(rows, groups))

class CpuTradeTests(unittest.TestCase):
    setUp = TradeTests.setUp
    def test_pure_go_cpu_advantage_cannot_be_inferred_from_wall(self):
        self.rows[("allocation", "pure-go")]["build"]["cpuSeconds"] = .9
        self.assertIn("allocation/build-trade/not-faster-pure-go", qualify.evaluate_trade(self.rows, self.groups)["failures"])

    def test_unknown_pure_go_cpu_cannot_authorize_trade(self):
        self.rows[("allocation", "pure-go")]["build"]["cpuSeconds"] = 0
        self.assertIn("allocation/build-trade/unresolved-pure-go", qualify.evaluate_trade(self.rows, self.groups)["unknown"])


class GcProbeTests(unittest.TestCase):
    def test_output_counter_and_reclamation_checks(self):
        import hashlib, json, tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            expected = b"ok\n"
            rows = []
            counters = {"collections": 3, "automatic-collections": 2, "allocated-bytes": 100,
                        "reclaimed-bytes": 100, "live-bytes": 0, "peak-heap-bytes": 100}
            for case in ("allocation", "worker"):
                for role in ("native", "previous", "baseline"):
                    rows.append({"case": case, "role": role, "gcProbe": True,
                                 "expectedSha256": hashlib.sha256(expected).hexdigest()})
                    directory = root / case / role / "gc-probe"
                    directory.mkdir(parents=True)
                    (directory / "observation.json").write_text(json.dumps({"status": "pass", "exitCode": 0}))
                    (directory / "stdout").write_bytes(expected)
                    (directory / "stderr").write_text("".join(f"type-rb-native-gc-stat-v1,{k},{v}\n" for k,v in counters.items()))
            selection = {"rows": rows}
            self.assertEqual(len(qualify.check_gc_probes(selection, root)), 6)
            output = root / "allocation/native/gc-probe/stdout"
            output.write_bytes(b"wrong\n")
            with self.assertRaisesRegex(ValueError, "output differs"):
                qualify.check_gc_probes(selection, root)
            output.write_bytes(expected)
            error = root / "allocation/native/gc-probe/stderr"
            original = error.read_text()
            error.write_text(original + "type-rb-native-gc-stat-v1,collections,3\n")
            with self.assertRaisesRegex(ValueError, "Invalid GC"):
                qualify.check_gc_probes(selection, root)
            error.write_text(original.replace("collections,3", "collections,4"))
            with self.assertRaisesRegex(ValueError, "counters differ"):
                qualify.check_gc_probes(selection, root)
