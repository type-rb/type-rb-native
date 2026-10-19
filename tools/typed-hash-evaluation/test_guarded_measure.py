import copy
from pathlib import Path
import tempfile
import unittest
from guarded_measure import Guard


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.record = dict(status="pass", wallSeconds=1., cpuSeconds=.9, memoryBytes=1024,
                           artifact={"sha256": "a" * 64, "bytes": 100})

    def test_both_rotated_orders_accept_valid_pairs(self):
        for order in [("native", "previous"), ("previous", "native")]:
            g = Guard()
            for role in order:
                g.check(Path("case") / role / "runtime-0", self.record)

    def test_each_paired_metric_stops_in_both_orders(self):
        for metric in ("wallSeconds", "cpuSeconds", "memoryBytes"):
            for order in [("native", "previous"), ("previous", "native")]:
                g = Guard()
                for index, role in enumerate(order):
                    r = copy.deepcopy(self.record)
                    if role == "native": r[metric] *= 2.01
                    if index:
                        with self.assertRaisesRegex(ValueError, "catastrophe"):
                            g.check(Path("case") / role / "runtime-0", r)
                    else: g.check(Path("case") / role / "runtime-0", r)

    def test_failed_output_or_timeout_stops(self):
        for status in ("timeout", "wrong-output", "build-failure"):
            r = dict(self.record, status=status)
            with self.assertRaisesRegex(ValueError, "failed observation"):
                Guard().check("case/native/runtime-0", r)

    def test_repeated_artifacts_must_match_within_each_role(self):
        g = Guard();g.check("case/native/build-0", self.record)
        r = copy.deepcopy(self.record);r["artifact"]["sha256"] = "b" * 64
        with self.assertRaisesRegex(ValueError, "identity differs"):
            g.check("case/native/build-1", r)

    def test_partial_build_write_does_not_consume_pair(self):
        g = Guard();r = dict(self.record);del r["artifact"]
        g.check("case/native/build-0", r)
        self.assertEqual(g.pairs, {})
        g.check("case/native/build-0", self.record)
        self.assertEqual(len(g.pairs), 1)

    def test_rounds_and_cases_cannot_form_a_pair(self):
        g = Guard();g.check("one/previous/runtime-0", self.record)
        r = dict(self.record, wallSeconds=3.)
        g.check("one/native/runtime-1", r);g.check("two/native/runtime-0", r)
        self.assertEqual(len(g.pairs), 3)

    def test_zero_cpu_is_not_claimed_as_a_regression_or_gain(self):
        g = Guard();g.check("case/previous/runtime-0", dict(self.record, cpuSeconds=0))
        g.check("case/native/runtime-0", self.record)

    def test_gc_requires_output_and_complete_reclamation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)/"case";d = root/"native/gc-probe";d.mkdir(parents=True)
            (root/"expected").write_text("ok\n");(d/"stdout").write_text("ok\n")
            (d/"stderr").write_text("type-rb-native-gc-stat-v1,allocated-bytes,10\ntype-rb-native-gc-stat-v1,reclaimed-bytes,10\ntype-rb-native-gc-stat-v1,live-bytes,0\n")
            Guard().check(d, self.record)
            (d/"stdout").write_text("wrong\n")
            with self.assertRaisesRegex(ValueError,"GC output"):
                Guard().check(d, self.record)

    def test_incomplete_or_invalid_gc_counters_fail(self):
        for counters in ["live-bytes,0", "allocated-bytes,-1\nreclaimed-bytes,-1\nlive-bytes,0", "allocated-bytes,10\nreclaimed-bytes,9\nlive-bytes,0"]:
            with tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)/"case";d = root/"native/gc-probe";d.mkdir(parents=True)
                (root/"expected").write_text("ok\n");(d/"stdout").write_text("ok\n")
                (d/"stderr").write_text("".join("type-rb-native-gc-stat-v1,"+line+"\n" for line in counters.splitlines()))
                with self.assertRaisesRegex(ValueError,"reclamation"):
                    Guard().check(d, self.record)
