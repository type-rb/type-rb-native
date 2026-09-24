import tempfile
import unittest
from pathlib import Path

from recovery_layout_sync import InventoryError, closure, synchronize


LAYOUT_HEAD = "record RecoveryCompilerModule\n\tname: String\n\timports: String\nend\n\ndef compiler_recovery_layout(): Array<RecoveryCompilerModule>\n\treturn [\n"
MUTATIONS_HEAD = "def compiler_recovery_mutations(): Array<Array<String>>\n\treturn [\n"
FRONTEND = (
    'describe("Compiler") do\n\ttest("parses the checked-in compiler closure through its own frontend") do\n'
    '\t\tnames := [{names}]\n\t\tputs(names.size())\n\tend\nend\n'
)


class RecoveryInventorySyncTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        (self.root / "src").mkdir()
        (self.root / "compiler/src").mkdir(parents=True)
        self.source("compiler", 'import { label } from first\n\ndef main()\n\tputs(label())\n\treturn\nend\n')
        self.source("first", 'import { Point } from second\n\ndef label(): String\n\treturn "first label"\nend\n')
        self.source("second", "record Point\n\tx: Integer\n\ty: String\nend\n")
        self.source("unrelated", 'def unused(): String\n\treturn "not in the closure"\nend\n')
        self.write("src/compiler_recovery_layout.trb", LAYOUT_HEAD +
                   '\t\tRecoveryCompilerModule.new(name: "second", imports: ""),\n'
                   '\t\tRecoveryCompilerModule.new(name: "compiler", imports: "import { label } from first\\n\\n"),\n'
                   '\t\tRecoveryCompilerModule.new(name: "first", imports: "import { Point } from second\\n\\n"),\n'
                   "\t]\nend\n")
        self.write("src/compiler_recovery_mutations.trb", MUTATIONS_HEAD +
                   '\t\t["first", "\\"first label\\"", "\\"first title\\""],\n'
                   '\t\t["second", "\\tx: Integer\\n\\ty: String", "\\ty: String\\n\\tx: Integer"],\n'
                   "\t]\nend\n")
        self.write("compiler/src/compiler_test.trb", FRONTEND.format(names='"compiler", "second", "first"'))

    def tearDown(self):
        self.directory.cleanup()

    def source(self, name, text):
        self.write(f"compiler/src/{name}.trb", text)

    def write(self, relative, text):
        (self.root / relative).write_text(text)

    def read(self, relative):
        return (self.root / relative).read_text()

    def snapshot(self):
        return {path: self.read(path) for path in (
            "src/compiler_recovery_layout.trb", "src/compiler_recovery_mutations.trb", "compiler/src/compiler_test.trb")}

    def test_synchronized_inventories_are_unchanged(self):
        self.assertEqual(closure(self.root), ["compiler", "first", "second"])
        before = self.snapshot()
        self.assertEqual(synchronize(self.root, True), [])
        self.assertEqual(self.snapshot(), before)

    def test_added_module_enters_every_inventory_without_reordering(self):
        self.source("first", 'import { Point } from second\nimport { extra } from third\n\n'
                             'def label(): String\n\treturn "first label" + extra()\nend\n')
        self.source("third", 'def extra(): String\n\treturn "third extra"\nend\n')
        before = self.snapshot()
        changes = synchronize(self.root, False)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(changes, ["layout: add third", "layout: imports first", "mutations: add third",
                                   "frontend test: add third"])
        synchronize(self.root, True)
        self.assertEqual(synchronize(self.root, False), [])
        layout = self.read("src/compiler_recovery_layout.trb")
        self.assertLess(layout.index('"second"'), layout.index('"compiler"'))
        self.assertIn('RecoveryCompilerModule.new(name: "third", imports: ""),\n\t]', layout)
        self.assertIn('imports: "import { Point } from second\\nimport { extra } from third\\n\\n"', layout)
        self.assertIn('["third", "\\"third extra\\"", "\\"third extra~\\""],\n\t]',
                      self.read("src/compiler_recovery_mutations.trb"))
        self.assertIn('names := ["compiler", "second", "first", "third"]', self.read("compiler/src/compiler_test.trb"))

    def test_module_leaving_the_closure_is_removed_everywhere(self):
        self.source("first", 'def label(): String\n\treturn "first label"\nend\n')
        self.assertEqual(synchronize(self.root, True), [
            "layout: remove second", "layout: imports first", "mutations: remove second", "frontend test: remove second"])
        self.assertNotIn('"second"', self.read("src/compiler_recovery_layout.trb"))
        self.assertNotIn('"second"', self.read("src/compiler_recovery_mutations.trb"))
        self.assertIn('names := ["compiler", "first"]', self.read("compiler/src/compiler_test.trb"))

    def test_stale_needles_regenerate_from_literals_or_record_fields(self):
        self.source("first", 'import { Point } from second\n\ndef label(): String\n\treturn "renamed label"\nend\n')
        self.source("second", "record Point\n\ty: String\n\tx: Integer\nend\n")
        self.assertEqual(synchronize(self.root, True), ["mutations: regenerate first", "mutations: regenerate second"])
        mutations = self.read("src/compiler_recovery_mutations.trb")
        self.assertIn('["first", "\\"renamed label\\"", "\\"renamed label~\\""]', mutations)
        self.assertIn('["second", "\\ty: String\\n\\tx: Integer", "\\tx: Integer\\n\\ty: String"]', mutations)

    def test_modules_without_an_observable_default_need_a_manual_mutation(self):
        self.source("second", "record Point\n\tx: Integer\nend\n")
        with self.assertRaisesRegex(InventoryError, "second"):
            synchronize(self.root, False)

    def test_imports_must_lead_and_the_entry_must_start_the_frontend_list(self):
        self.source("first", 'def label(): String\n\treturn "first label"\nend\nimport { Point } from second\n')
        with self.assertRaisesRegex(InventoryError, "leading block"):
            synchronize(self.root, False)
        self.tearDown()
        self.setUp()
        self.write("compiler/src/compiler_test.trb", FRONTEND.format(names='"first", "compiler", "second"'))
        with self.assertRaisesRegex(InventoryError, "compiler entry"):
            synchronize(self.root, False)


if __name__ == "__main__":
    unittest.main()
