import tempfile
import unittest
from pathlib import Path

from recovery_layout_sync import synchronize


class RecoveryLayoutSyncTest(unittest.TestCase):
    def test_changed_import_is_detected_and_repaired_without_reordering(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "compiler/src").mkdir(parents=True)
            layout = root / "src/compiler_recovery_layout.trb"
            original = (
                'RecoveryCompilerModule.new(name: "second", imports: ""),\n'
                '\t\tRecoveryCompilerModule.new(name: "first", imports: ""),\n'
            )
            # The fixture uses the same canonical row indentation as the source.
            original = '\t\t' + original
            layout.write_text(original)
            (root / "compiler/src/first.trb").write_text(
                "import { value } from second\n\nrecord First\nend\n"
            )
            (root / "compiler/src/second.trb").write_text("record Second\nend\n")

            self.assertEqual(synchronize(root, False), ["first"])
            self.assertEqual(layout.read_text(), original)
            self.assertEqual(synchronize(root, True), ["first"])
            self.assertEqual(synchronize(root, False), [])
            self.assertTrue(layout.read_text().startswith(
                '\t\tRecoveryCompilerModule.new(name: "second", imports: ""),\n'
            ))
            self.assertIn('imports: "import { value } from second\\n\\n"', layout.read_text())


if __name__ == "__main__":
    unittest.main()
