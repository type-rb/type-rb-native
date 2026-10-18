import copy
import unittest
import readiness


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.ir = {case: {role: readiness.expected_ir(case, role) for role in ('previous', 'native')}
                   for case in readiness.CASES}

    def test_expected_join_elision_and_control(self):
        readiness.validate_ir(self.ir)

    def test_changed_calls_stop_before_timing(self):
        for case in readiness.CASES:
            for role in ('previous', 'native'):
                for field in self.ir[case][role]:
                    changed = copy.deepcopy(self.ir)
                    changed[case][role][field] += 1
                    with self.assertRaises(ValueError): readiness.validate_ir(changed)

    def test_inspection_separates_consumer_from_other_functions(self):
        body = 'function l $trbnf0() {\n@start\n call $trbn_string_concat_three(l %a, l %b, l %c)\n call $trbn_string_concat(l %a, l %b)\n call $trbn_string_join(l %p, l 3, l %s)\n ret 0\n}\n'
        other = 'function l $trbnf9() {\n call $trbn_array_new(l 4)\n}\n'
        self.assertEqual(readiness.inspect_ir(body + other, 'string-building'), self.ir['string-building']['native'])
        body = 'function $trbnf4() {\n ret\n}\n'
        self.assertEqual(readiness.inspect_ir(body + other, 'n-body'), self.ir['n-body']['native'])
        with self.assertRaises(ValueError): readiness.inspect_ir(other, 'string-building')

    def stats(self, allocated=100):
        return dict(collections=2, **{'automatic-collections':1,'allocated-bytes':allocated,
                    'reclaimed-bytes':allocated,'live-bytes':0,'peak-heap-bytes':100})

    def encode(self, values):
        return ''.join(f'type-rb-native-gc-stat-v1,{k},{n}\n' for k,n in values.items()).encode()

    def test_n_body_zero_automatic_collections_still_requires_full_reclamation(self):
        values = self.stats(); values['automatic-collections'] = 0
        self.assertEqual(readiness.gc_stats(self.encode(values), require_automatic=False), values)
        with self.assertRaises(ValueError): readiness.gc_stats(self.encode(values))
        for field, value in [('collections',0),('allocated-bytes',0),('reclaimed-bytes',99),('live-bytes',1)]:
            changed = dict(values); changed[field] = value
            with self.assertRaises(ValueError): readiness.gc_stats(self.encode(changed), require_automatic=False)

    def test_gc_requires_complete_real_reclamation(self):
        values = self.stats()
        self.assertEqual(readiness.gc_stats(self.encode(values)), values)
        for field, value in [('automatic-collections',0),('reclaimed-bytes',99),('live-bytes',1)]:
            changed = dict(values); changed[field] = value
            with self.assertRaises(ValueError): readiness.gc_stats(self.encode(changed))
        with self.assertRaises(ValueError): readiness.gc_stats(self.encode(values) + b'unexpected\n')
        with self.assertRaises(ValueError): readiness.gc_stats(b'')

    def test_only_primary_allocation_may_change(self):
        rows = [dict(case=case,role=role,gc=self.stats(90 if case=='string-building' and role=='native' else 100))
                for case in readiness.CASES for role in ('native','previous')]
        self.assertEqual(readiness.validate_gc(rows)['unchangedCases'], ['n-body'])
        self.assertEqual(readiness.validate_gc(rows)['allocatedBytesRatio'], .9)
        for field in self.stats():
            changed = copy.deepcopy(rows)
            next(r for r in changed if r['case']=='n-body' and r['role']=='native')['gc'][field] += 1
            with self.assertRaises(ValueError): readiness.validate_gc(changed)
        for field,value in [('allocated-bytes',100),('reclaimed-bytes',89),('peak-heap-bytes',101),('live-bytes',1),('automatic-collections',0)]:
            changed=copy.deepcopy(rows)
            next(r for r in changed if r['case']=='string-building' and r['role']=='native')['gc'][field]=value
            with self.assertRaises(ValueError): readiness.validate_gc(changed)
        del rows[0]['gc']
        with self.assertRaises(ValueError): readiness.validate_gc(rows)


if __name__ == '__main__': unittest.main()
