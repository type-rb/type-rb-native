#!/usr/bin/env python3
from pathlib import Path
import tempfile
import unittest

from compiler_layout import check, import_header


class OwnershipTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.write('src/compiler', 'import frontend/checking/expression\n')
        self.write('src/frontend/checking/expression', 'def expression(): Integer\n\treturn 1\nend\n')

    def write(self, name, source=''):
        path = self.root / 'compiler' / (name + '.trb')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source)

    def errors(self):
        return check(self.root)[0]

    def test_cross_directory_cycles_and_same_group_recursion_are_allowed(self):
        self.write('src/frontend/checking/expression', 'import mir/construction\nimport frontend/checking/statement\n')
        self.write('src/frontend/checking/statement', 'import frontend/checking/expression\n')
        self.write('src/mir/construction', 'import frontend/checking/expression\n')
        self.assertEqual(self.errors(), [])

    def test_unknown_nested_owners_and_unresolved_imports_fail(self):
        self.write('src/misc/new', 'import support/missing\n')
        errors = '\n'.join(self.errors())
        self.assertIn('missing responsibility owner', errors)
        self.assertIn('missing composed module support/missing', errors)

    def test_support_and_backend_boundaries_are_enforced(self):
        self.write('src/support/path', 'import backend/qbe/output\n')
        self.write('src/backend/qbe/output', 'import frontend/checking/expression\n')
        self.assertEqual(len(self.errors()), 2)
        self.assertIn('support -> backend/qbe', self.errors()[1])

    def test_identity_exception_does_not_allow_neighboring_resolution_imports(self):
        self.write('src/backend/qbe/qbe_constants', 'import frontend/resolution/entry_resolution\n')
        self.write('src/frontend/resolution/entry_resolution')
        self.assertEqual(self.errors(), [])
        self.write('src/backend/qbe/other', 'import frontend/resolution/entry_resolution\n')
        self.assertEqual(len(self.errors()), 1)

    def test_tests_cover_all_core_owners_but_production_cannot_import_them(self):
        self.write('src/support/path_test', 'import backend/qbe/output\nimport compiler_test\nimport trb/std/test\n')
        self.write('src/backend/qbe/output')
        self.write('src/compiler_test')
        self.assertEqual(self.errors(), [])
        self.write('src/frontend/checking/expression', 'import support/path_test\n')
        self.assertIn('production code imports test module', self.errors()[0])
        self.write('src/frontend/checking/expression', 'import trb/std/test\n')
        self.assertIn('production code imports test support', self.errors()[0])

    def test_parsed_state_exception_does_not_admit_other_syntax_dependencies(self):
        self.write('src/state/source_state', 'import frontend/syntax/iteration_syntax\n')
        self.write('src/frontend/syntax/iteration_syntax')
        self.assertEqual(self.errors(), [])
        self.write('src/state/other', 'import frontend/syntax/iteration_syntax\n')
        self.write('src/frontend/syntax/parser')
        self.write('src/state/source_state', 'import frontend/syntax/parser\n')
        self.assertEqual(len(self.errors()), 2)

    def test_cli_can_compose_core_but_core_cannot_import_cli(self):
        self.write('cli/main', 'import compiler\nimport frontend/checking/expression\n')
        self.assertEqual(self.errors(), [])
        self.write('src/compiler_test', 'import main\n')
        self.assertIn('core cannot depend on CLI', self.errors()[0])

    def test_composed_collisions_and_symlinks_fail(self):
        self.write('cli/compiler')
        self.assertIn('duplicate composed module', self.errors()[0])
        (self.root / 'compiler/cli/compiler.trb').unlink()
        (self.root / 'compiler/src/support').mkdir()
        (self.root / 'outside.trb').write_text('')
        (self.root / 'compiler/src/support/escape.trb').symlink_to(self.root / 'outside.trb')
        self.assertIn('source must stay inside', self.errors()[0])

    def test_embedded_program_imports_are_not_compiler_dependencies(self):
        source = '# Header\nimport { helper } from support/path\n\nvalue := "\nimport missing\n"\n'
        self.assertEqual(import_header(source), [(2, 'support/path')])
        with self.assertRaises(ValueError):
            import_header('import { broken\n')


if __name__ == '__main__':
    unittest.main()
