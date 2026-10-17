import copy
import unittest
import readiness


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.ir = {case: {role: dict(binaryCalls=3 if case == 'string-building' else 1,
                                    fusedCalls=0, scratchAllocations=0, entryScratchBytes=[])
                          for role in ('previous', 'native')}
                   for case in readiness.CASES}
        self.ir['string-building']['native'].update(binaryCalls=1, fusedCalls=1,
                                                    scratchAllocations=1, entryScratchBytes=['24'])

    def test_expected_fusion_and_unchanged_hash(self):
        readiness.validate_ir(self.ir)

    def test_missing_fusion_or_loop_scratch_stops_before_timing(self):
        for case in readiness.CASES:
            for role in ('previous', 'native'):
                for field in ('binaryCalls', 'fusedCalls', 'scratchAllocations'):
                    changed = copy.deepcopy(self.ir)
                    changed[case][role][field] += 1
                    with self.assertRaises(ValueError):
                        readiness.validate_ir(changed)
        changed = copy.deepcopy(self.ir)
        changed['string-building']['native']['entryScratchBytes'] = []
        with self.assertRaises(ValueError):
            readiness.validate_ir(changed)

    def test_inspection_separates_entry_from_loop_and_other_functions(self):
        body = 'function l $trbnf0() {\n@start\n %string_fragments =l alloc8 24\n jmp @mir_0\n@mir_0\n call $trbn_string_concat_many(l %string_fragments, l 3)\n call $trbn_string_concat(l %a, l %b)\n ret 0\n}\n'
        other = 'function l $trbnf9() {\n call $trbn_string_concat(l %a, l %b)\n}\n'
        self.assertEqual(readiness.inspect_ir(body + other, 'string-building'), self.ir['string-building']['native'])
        moved = body.replace(' %string_fragments =l alloc8 24\n', '').replace('@mir_0\n', '@mir_0\n %string_fragments =l alloc8 24\n')
        self.assertEqual(readiness.inspect_ir(moved, 'string-building')['entryScratchBytes'], [])
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

    def test_allocation_reduction_cannot_be_missing_or_equal(self):
        rows = [dict(case=case,role=role,gc={'allocated-bytes':90 if role=='native' else 100})
                for case in readiness.CASES for role in ('native','previous')]
        self.assertEqual(readiness.validate_gc(rows)['nativeAllocatedBytes'],90)
        rows[0]['gc']['allocated-bytes'] = 100
        with self.assertRaises(ValueError): readiness.validate_gc(rows)
        del rows[0]['gc']
        with self.assertRaises(ValueError): readiness.validate_gc(rows)

if __name__ == '__main__': unittest.main()
