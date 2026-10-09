import unittest
from run import assess, ordering


def samples():
    return [dict(block=b, case=c, role=r, round=i, status="pass", wallSeconds=1.0,
                 cpuSeconds=0.2, memoryBytes=1024000)
            for b in range(3) for c in ("object-dispatch", "fannkuch-redux", "array-streaming")
            for i in range(6) for r in ("A", "B")]


class AssessmentTest(unittest.TestCase):
    def test_exact_identity_passes(self):
        self.assertEqual(assess(samples())["status"], "pass")

    def test_one_block_memory_failure_is_not_averaged_away(self):
        data = samples()
        for row in data:
            if row["block"] == 1 and row["case"] == "fannkuch-redux" and row["role"] == "B":
                row["memoryBytes"] *= 1.0625
        self.assertIn("spread:1:fannkuch-redux:memoryBytes", assess(data)["failures"])

    def test_both_ratio_directions(self):
        for role in ("A", "B"):
            data = samples()
            for row in data:
                if row["role"] == role:
                    row["wallSeconds"] = 1.051
            self.assertEqual(assess(data)["status"], "unmet")

    def test_cpu_below_resolution_remains_unknown(self):
        data = samples()
        for row in data:
            row["cpuSeconds"] = 0.0
        result = assess(data)
        self.assertEqual(result["status"], "pass")
        self.assertIsNone(result["rows"][0]["metrics"]["cpuSeconds"]["pass"])

    def test_warmup_outlier_is_retained(self):
        data = samples()
        data[0]["wallSeconds"] = 2.1
        self.assertEqual(assess(data)["status"], "unmet")

    def test_missing_or_failed_record_blocks(self):
        self.assertEqual(assess(samples()[:-1])["status"], "unmet")
        data = samples()
        data[0]["status"] = "output-mismatch"
        self.assertEqual(assess(data)["status"], "unmet")

    def test_balanced_adjacent_roles(self):
        for block in range(3):
            for case in range(3):
                pairs = [ordering(block, case, i) for i in range(6)]
                self.assertEqual(sum(pair[0] == "A" for pair in pairs), 3)
                self.assertTrue(all(set(pair) == {"A", "B"} for pair in pairs))


if __name__ == "__main__":
    unittest.main()
