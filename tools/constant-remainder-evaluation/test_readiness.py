import copy
import unittest
import readiness


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        calls = ['call $trbnf3', 'call $trbnf5', 'call $trbnf3', 'call $trbnf5', 'call $trbnf2']
        self.ir = {case: {role: {'directCalls': calls if case == 'object-dispatch' else [],
                                'enumSlots': 0, 'reciprocalCorrections': 0,
                                'reciprocalGuards': count if role == 'native' else 0}
                          for role in ('previous', 'native')}
                   for case, (_, count) in readiness.CASES.items()}

    def test_joint_lowering_keeps_existing_calls(self):
        readiness.validate_ir(self.ir)

    def test_regressed_or_missing_lowering_stops_before_timing(self):
        for case in readiness.CASES:
            for role in ('previous', 'native'):
                for field in ('enumSlots', 'reciprocalCorrections', 'reciprocalGuards'):
                    changed = copy.deepcopy(self.ir)
                    changed[case][role][field] += 1
                    with self.assertRaises(ValueError):
                        readiness.validate_ir(changed)
        changed = copy.deepcopy(self.ir)
        changed['object-dispatch']['native']['directCalls'].pop()
        with self.assertRaises(ValueError):
            readiness.validate_ir(changed)

    def test_inspection_excludes_other_functions(self):
        body = 'function l $trbnf3() {\n %v =w cultl %n, 2147483648\n ret 0\n}\n'
        other = 'function l $trbnf9() {\n %v =l sar %n, 63\n call $trbnf2()\n}\n'
        row = readiness.inspect_ir(body + other, 'enum-result')
        self.assertEqual(row['reciprocalGuards'], 1)
        self.assertEqual(row['reciprocalCorrections'], 0)
        self.assertEqual(row['directCalls'], [])
        with self.assertRaises(ValueError):
            readiness.inspect_ir(other, 'enum-result')


if __name__ == '__main__':
    unittest.main()
