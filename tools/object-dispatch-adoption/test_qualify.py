import unittest
import qualify


class TradeTests(unittest.TestCase):
    def setUp(self):
        self.rows, self.groups = {}, {}
        for case in ("object-dispatch", "control"):
            for role, build, run in (("native", 1.1, .9), ("previous", 1., 1.), ("typerb-go", 2., 1.), ("pure-go", 1.5, 1.)):
                self.rows[(case, role)] = {"build": {"wallSeconds": build, "cpuSeconds": build, "memoryBytes": 100},
                    "runtime": {"wallSeconds": run, "cpuSeconds": run, "memoryBytes": 100}, "artifactBytes": 100}
                self.groups[(case, role, "runtime")] = [{"phase": "retained", "wallSeconds": run}] * 5

    def test_cost_trade_requires_retained_competitor_advantage(self):
        self.assertEqual(qualify.evaluate_trade(self.rows, self.groups)["status"], "met")
        self.rows[("object-dispatch", "pure-go")]["build"]["wallSeconds"] = 1.05
        self.assertIn("object-dispatch/lost-build-advantage/pure-go", qualify.evaluate_trade(self.rows, self.groups)["failures"])

    def test_investigation_ceiling_and_runtime_benefit_still_block(self):
        self.rows[("object-dispatch", "native")]["build"]["wallSeconds"] = 1.26
        for case in ("object-dispatch", "control"):
            self.rows[(case, "native")]["runtime"]["cpuSeconds"] = .96
        r = qualify.evaluate_trade(self.rows, self.groups)
        self.assertIn("object-dispatch/build/wallSeconds", r["failures"])
        self.assertIn("object-dispatch/no-case-meets-both-5-percent-and-1-ms", r["failures"])

    def test_below_resolution_is_not_pass(self):
        self.rows[("object-dispatch", "previous")]["runtime"]["cpuSeconds"] = 0
        self.assertEqual(qualify.evaluate_trade(self.rows, self.groups)["status"], "unmet")

    def test_rss_uses_separate_prospective_policy(self):
        self.rows[("object-dispatch", "native")]["runtime"]["memoryBytes"] = 106
        self.assertNotIn("object-dispatch/runtime/memoryBytes", qualify.evaluate_trade(self.rows, self.groups)["failures"])

    def test_missing_pure_go_is_explicit(self):
        del self.rows[("object-dispatch", "pure-go")]
        self.assertEqual(qualify.evaluate_trade(self.rows, self.groups)["missingComparators"], ["object-dispatch"])

    def test_failed_or_incomplete_cohort_is_rejected(self):
        with self.assertRaises((ValueError, KeyError)):
            qualify.assess({"registration": {"candidate": "a" * 40}}, {"revision": "a" * 40, "status": "measured-with-failures"}, [])

    def test_candidate_zero_cpu_is_unknown(self):
        self.rows[("object-dispatch", "native")]["runtime"]["cpuSeconds"] = 0
        self.assertEqual(qualify.evaluate_trade(self.rows, self.groups)["status"], "unmet")

    def test_reference_build_advantage_is_required_even_if_previously_lost(self):
        self.rows[("object-dispatch", "typerb-go")]["build"]["wallSeconds"] = .8
        self.assertIn("object-dispatch/not-faster-build/typerb-go", qualify.evaluate_trade(self.rows, self.groups)["failures"])

    def test_missing_pure_go_cannot_authorize_increased_build_cost(self):
        del self.rows[("object-dispatch", "pure-go")]
        self.assertIn("object-dispatch/build-trade/missing-pure-go", qualify.evaluate_trade(self.rows, self.groups)["unknown"])

    def test_comparator_warmup_outlier_is_reported(self):
        self.groups[("object-dispatch", "typerb-go", "runtime")].append({"phase": "warmup", "wallSeconds": 2.1})
        self.assertIn("object-dispatch/outlier/typerb-go", qualify.evaluate_trade(self.rows, self.groups)["failures"])

    def test_absolute_build_cost_and_runtime_savings_are_explicit(self):
        row = qualify.evaluate_trade(self.rows, self.groups)["ratios"]["object-dispatch"]
        self.assertAlmostEqual(row["buildWallAddedSeconds"], .1)
        self.assertAlmostEqual(row["runtimeWallSavedSeconds"], .1)

    def test_primary_wall_and_cpu_cannot_be_combined_across_cases(self):
        self.rows[("object-dispatch", "native")]["runtime"]["cpuSeconds"] = .99
        self.rows[("control", "native")]["runtime"]["wallSeconds"] = .99
        self.assertIn("object-dispatch/no-case-meets-both-5-percent-and-1-ms", qualify.evaluate_trade(self.rows, self.groups)["failures"])

    def test_other_case_cannot_replace_primary(self):
        self.rows[("object-dispatch", "native")]["runtime"]["cpuSeconds"] = .99
        self.assertEqual(qualify.evaluate_trade(self.rows, self.groups)["qualifiedPrimaries"], [])

    def test_primary_absolute_saving_is_required(self):
        for case in ("object-dispatch", "control"):
            self.rows[(case, "previous")]["runtime"]["wallSeconds"] = .001
            self.rows[(case, "native")]["runtime"]["wallSeconds"] = .0009
        self.assertIn("object-dispatch/no-case-meets-both-5-percent-and-1-ms", qualify.evaluate_trade(self.rows, self.groups)["failures"])

    def test_unmeasurable_control_cpu_is_disclosed_without_overriding_valid_primary(self):
        self.rows[("control", "native")]["runtime"]["cpuSeconds"] = 0
        result = qualify.evaluate_trade(self.rows, self.groups)
        self.assertEqual(result["status"], "met")
        self.assertIn("control/runtime/cpuSeconds", result["unknown"])

    def test_known_control_regression_remains_blocking(self):
        self.rows[("control", "native")]["runtime"]["cpuSeconds"] = 1.06
        self.assertIn("control/runtime/cpuSeconds", qualify.evaluate_trade(self.rows, self.groups)["failures"])
