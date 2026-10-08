import copy
import unittest
import qualify


class TradeTests(unittest.TestCase):
    def setUp(self):
        self.rows, self.groups = {}, {}
        for role, build, run in (("native", 1.1, .9), ("previous", 1., 1.), ("typerb-go", 2., 1.), ("pure-go", 1.5, 1.)):
            self.rows[("allocation", role)] = {"build": {"wallSeconds": build, "cpuSeconds": build, "memoryBytes": 100},
                "runtime": {"wallSeconds": run, "cpuSeconds": run, "memoryBytes": 100}, "artifactBytes": 100}
            self.groups[("allocation", role, "runtime")] = [{"phase": "retained", "wallSeconds": run}] * 5

    def test_cost_trade_requires_retained_competitor_advantage(self):
        self.assertEqual(qualify.evaluate_trade(self.rows, self.groups)["status"], "met")
        self.rows[("allocation", "pure-go")]["build"]["wallSeconds"] = 1.05
        self.assertIn("allocation/lost-build-advantage/pure-go", qualify.evaluate_trade(self.rows, self.groups)["failures"])

    def test_investigation_ceiling_and_runtime_benefit_still_block(self):
        self.rows[("allocation", "native")]["build"]["wallSeconds"] = 1.26
        self.rows[("allocation", "native")]["runtime"]["cpuSeconds"] = .98
        r = qualify.evaluate_trade(self.rows, self.groups)
        self.assertIn("allocation/build/wallSeconds", r["failures"])
        self.assertIn("allocation/primary/cpuSeconds", r["failures"])

    def test_below_resolution_is_not_pass(self):
        self.rows[("allocation", "previous")]["runtime"]["cpuSeconds"] = 0
        self.assertEqual(qualify.evaluate_trade(self.rows, self.groups)["status"], "incomplete")

    def test_gc_memory_regression_not_traded(self):
        self.rows[("allocation", "native")]["runtime"]["memoryBytes"] = 106
        self.assertIn("allocation/runtime/memoryBytes", qualify.evaluate_trade(self.rows, self.groups)["failures"])

    def test_missing_pure_go_is_explicit(self):
        del self.rows[("allocation", "pure-go")]
        self.assertEqual(qualify.evaluate_trade(self.rows, self.groups)["missingComparators"], ["allocation"])

    def test_failed_or_incomplete_cohort_is_rejected(self):
        with self.assertRaises((ValueError, KeyError)):
            qualify.assess({"registration": {"candidate": "a" * 40}}, {"revision": "a" * 40, "status": "measured-with-failures"}, [])
