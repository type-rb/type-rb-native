from pathlib import Path
import tempfile
import unittest

from bootstrap_snapshot_size import check_size, compiler_input_limit


class SnapshotSizeTest(unittest.TestCase):
    def test_actual_decoder_boundary_without_allocating_large_input(self):
        decoder = Path(__file__).resolve().parent.parent / "recovery/src/managed/snapshot.trb"
        limit = compiler_input_limit(decoder)
        with tempfile.TemporaryDirectory() as directory:
            snapshot = Path(directory) / "snapshot.json"
            for size in (1, limit, limit + 1, 0):
                with self.subTest(size=size):
                    with snapshot.open("wb") as output:
                        output.truncate(size)
                    if 0 < size <= limit:
                        self.assertEqual(check_size(snapshot, decoder), (size, limit))
                    else:
                        with self.assertRaisesRegex(ValueError, f"has {size} bytes"):
                            check_size(snapshot, decoder)

    def test_missing_or_ambiguous_bound_cannot_silently_disable_preflight(self):
        declaration = "COMPILER_RECOVERY_MAX_INPUT_BYTES := 12\n"
        with tempfile.TemporaryDirectory() as directory:
            decoder = Path(directory) / "snapshot.trb"
            for source in ("", declaration * 2, declaration.replace("12", "0")):
                decoder.write_text(source, encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "one positive"):
                    compiler_input_limit(decoder)


if __name__ == "__main__":
    unittest.main()
