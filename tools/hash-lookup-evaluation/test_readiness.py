import copy
import unittest
import readiness


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.ir = {case: {role: dict(getCalls=2 if case == 'hash-string-keys' else 0,
                                    setCalls=2 if case == 'hash-string-keys' else 0,
                                    reusedLookups=0, binaryStrings=1,
                                    directStrings=int(case == 'string-building'))
                          for role in ('previous', 'native')}
                   for case in readiness.CASES}
        self.ir['hash-string-keys']['native'].update(getCalls=1, setCalls=1, reusedLookups=1)

    def test_expected_lookup_reuse_and_unchanged_string(self):
        readiness.validate_ir(self.ir)

    def test_changed_lookup_or_control_lowering_stops_before_timing(self):
        for case in readiness.CASES:
            for role in ('previous', 'native'):
                for field in ('getCalls', 'setCalls', 'reusedLookups', 'binaryStrings', 'directStrings'):
                    changed = copy.deepcopy(self.ir)
                    changed[case][role][field] += 1
                    with self.assertRaises(ValueError):
                        readiness.validate_ir(changed)
    def test_inspection_separates_consumer_from_other_functions(self):
        body = 'function l $trbnf0() {\n@start\n jmp @mir_0\n@mir_0\n call $trbn_string_concat_three(l %a, l %b, l %c)\n call $trbn_string_concat(l %a, l %b)\n ret 0\n}\n'
        other = 'function l $trbnf9() {\n call $trbn_string_concat(l %a, l %b)\n}\n'
        self.assertEqual(readiness.inspect_ir(body + other, 'string-building'), self.ir['string-building']['native'])
        body = body.replace(' call $trbn_string_concat_three(l %a, l %b, l %c)\n',
                            ' call $trbn_hash_get(l %h, l %k)\n call $trbn_hash_set(l %h, l %k, l %v)\n call $trbn_hash_existing_slot(l %h, l %k)\n')
        self.assertEqual(readiness.inspect_ir(body + other, 'hash-string-keys'), self.ir['hash-string-keys']['native'])
        with self.assertRaises(ValueError):
            readiness.inspect_ir(other, 'string-building')

    def test_gc_requires_complete_real_reclamation(self):
        values = dict(collections=2, **{'automatic-collections':1,'allocated-bytes':100,'reclaimed-bytes':100,'live-bytes':0,'peak-heap-bytes':100})
        encode = lambda v: ''.join(f'type-rb-native-gc-stat-v1,{k},{n}\n' for k,n in v.items()).encode()
        self.assertEqual(readiness.gc_stats(encode(values)), values)
        for field, value in [('automatic-collections',0),('reclaimed-bytes',99),('live-bytes',1)]:
            changed = dict(values); changed[field] = value
            with self.assertRaises(ValueError): readiness.gc_stats(encode(changed))
        with self.assertRaises(ValueError): readiness.gc_stats(encode(values) + b'unexpected\n')
        with self.assertRaises(ValueError): readiness.gc_stats(b'')

    def test_gc_accounting_must_be_present_and_identical(self):
        values = dict(collections=2, **{'automatic-collections':1,'allocated-bytes':100,'reclaimed-bytes':100,'live-bytes':0,'peak-heap-bytes':100})
        rows = [dict(case=case,role=role,gc=dict(values))
                for case in readiness.CASES for role in ('native','previous')]
        self.assertEqual(readiness.validate_gc(rows)['unchangedCases'], sorted(readiness.CASES))
        for field in values:
            changed = copy.deepcopy(rows)
            changed[0]['gc'][field] += 1
            with self.assertRaises(ValueError): readiness.validate_gc(changed)
        del rows[0]['gc']
        with self.assertRaises(ValueError): readiness.validate_gc(rows)

if __name__ == '__main__': unittest.main()
