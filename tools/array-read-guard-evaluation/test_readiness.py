import copy
import unittest
import tempfile
from pathlib import Path
import readiness


class ReadinessTests(unittest.TestCase):
    def test_prior_compiler_identities_reject_redefined_comparisons(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'compiler'
            path.write_bytes(b'frozen compiler')
            roles = {role: {'path': str(path)} for role in ('previous', 'baseline')}
            expected = {role: {'sha256': readiness.digest(path), 'bytes': path.stat().st_size} for role in roles}
            readiness.validate_prior_compilers(roles, expected)
            for field in ('sha256', 'bytes'):
                changed = copy.deepcopy(expected)
                changed['previous'][field] = '0' * 64 if field == 'sha256' else 0
                with self.assertRaises(ValueError): readiness.validate_prior_compilers(roles, changed)

    def setUp(self):
        self.ir = {case: {role: readiness.expected_ir(case, role) for role in ('previous', 'native')}
                   for case in readiness.CASES}

    def test_expected_array_guards_and_control(self):
        readiness.validate_ir(self.ir)

    def test_changed_calls_stop_before_timing(self):
        for case in readiness.CASES:
            for role in ('previous', 'native'):
                for field in self.ir[case][role]:
                    changed = copy.deepcopy(self.ir)
                    changed[case][role][field] += 1
                    with self.assertRaises(ValueError): readiness.validate_ir(changed)

    def test_inspection_separates_algorithm_from_other_functions(self):
        for case in readiness.CASES:
            for role in ('native', 'previous'):
                wanted = self.ir[case][role]
                body = 'function l $trbnf0() {\n@start\n'
                body += ' call $trbn_fail(l $trbn_bounds_error)\n' * wanted['boundsFailureSites']
                body += ''.join(f' %mir_array_checked_index{i} =l copy 1\n' for i in range(wanted['capturedReadPositions']))
                body += ' ret 0\n}\n'
                other = 'function l $trbnf9() {\n call $trbn_fail(l $trbn_bounds_error)\n}\n'
                self.assertEqual(readiness.inspect_ir(body + other, case), wanted)
        with self.assertRaises(ValueError): readiness.inspect_ir(other, 'fannkuch-redux')

    def stats(self, allocated=100):
        return dict(collections=2, **{'automatic-collections':1,'allocated-bytes':allocated,
                    'reclaimed-bytes':allocated,'live-bytes':0,'peak-heap-bytes':100})

    def encode(self, values):
        return ''.join(f'type-rb-native-gc-stat-v1,{k},{n}\n' for k,n in values.items()).encode()

    def test_fannkuch_zero_automatic_collections_still_requires_full_reclamation(self):
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

    def test_all_six_counters_stay_equal_for_both_cases(self):
        rows = [dict(case=case,role=role,gc=self.stats())
                for case in readiness.CASES for role in ('native','previous')]
        for row in rows:
            if row['case'] == 'fannkuch-redux': row['gc']['automatic-collections'] = 0
        self.assertEqual(readiness.validate_gc(rows)['unchangedCases'], list(readiness.CASES))
        for case in readiness.CASES:
            for field in self.stats():
                changed = copy.deepcopy(rows)
                next(r for r in changed if r['case']==case and r['role']=='native')['gc'][field] += 1
                with self.assertRaises(ValueError): readiness.validate_gc(changed)
        del rows[0]['gc']
        with self.assertRaises(ValueError): readiness.validate_gc(rows)


if __name__ == '__main__': unittest.main()
