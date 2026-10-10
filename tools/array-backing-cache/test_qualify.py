import copy
import unittest
import qualify


class TradeTests(unittest.TestCase):
    def setUp(self):
        self.rows, self.groups = {}, {}
        for case in ('allocation', 'n-body', 'fannkuch-redux', 'control'):
            for role, build, runtime in (('native', 1.1, .9 if case == 'allocation' else .99),
                                         ('previous', 1., 1.), ('typerb-go', 2., 1.), ('pure-go', 1.5, 1.)):
                self.rows[(case, role)] = {'build': {'wallSeconds': build, 'cpuSeconds': build, 'memoryBytes': 100},
                    'runtime': {'wallSeconds': runtime, 'cpuSeconds': runtime, 'memoryBytes': 100}, 'artifactBytes': 100}
                self.groups[(case, role, 'runtime')] = [{'phase': 'retained', 'wallSeconds': runtime}] * 5

    def result(self):
        return qualify.evaluate_trade(self.rows, self.groups)

    def test_qualified_gain_and_new_go_win_are_both_recorded(self):
        result = self.result()
        self.assertEqual(result['status'], 'met')
        self.assertEqual(result['qualifiedPrimaries'], ['allocation'])
        self.assertEqual(result['newGoWins'], ['allocation'])

    def test_incremental_gain_cannot_replace_a_go_win(self):
        self.rows[('allocation', 'typerb-go')]['runtime']['wallSeconds'] = .8
        result = self.result()
        self.assertEqual(result['qualifiedPrimaries'], ['allocation'])
        self.assertEqual(result['requestedOutcome'], 'unmet')
        self.assertIn('allocation/not-go-faster', result['failures'])

    def test_existing_go_win_is_distinguished_but_can_improve(self):
        self.rows[('allocation', 'typerb-go')]['runtime']['wallSeconds'] = 2.
        self.assertEqual(self.result()['newGoWins'], [])
        self.assertEqual(self.result()['requestedOutcome'], 'met')

    def test_a_control_cannot_replace_allocation(self):
        self.rows[('allocation', 'native')]['runtime']['wallSeconds'] = .99
        self.rows[('n-body', 'native')]['runtime'].update(wallSeconds=.9, cpuSeconds=.9)
        self.assertEqual(self.result()['qualifiedPrimaries'], [])
        self.assertEqual(self.result()['newGoWins'], [])

    def test_unregistered_control_cannot_replace_primary(self):
        self.rows[('allocation', 'native')]['runtime']['wallSeconds'] = .99
        self.rows[('control', 'native')]['runtime'].update(wallSeconds=.8, cpuSeconds=.8)
        self.assertEqual(self.result()['qualifiedPrimaries'], [])
        self.assertEqual(self.result()['newGoWins'], [])

    def test_cpu_must_be_positive_measurable_and_improved(self):
        for cpu in (0., .96, 1., 1.01):
            self.rows[('allocation', 'native')]['runtime']['cpuSeconds'] = cpu
            self.assertEqual(self.result()['qualifiedPrimaries'], [])

    def test_savings_cannot_be_combined_across_cases(self):
        self.rows[('allocation', 'native')]['runtime']['cpuSeconds'] = 1.
        self.rows[('n-body', 'native')]['runtime']['cpuSeconds'] = .8
        self.assertEqual(self.result()['qualifiedPrimaries'], [])

    def test_absolute_saving_is_required(self):
        self.rows[('allocation', 'previous')]['runtime']['wallSeconds'] = .001
        self.rows[('allocation', 'native')]['runtime']['wallSeconds'] = .0009
        self.assertEqual(self.result()['qualifiedPrimaries'], [])

    def test_runtime_and_build_alarms_are_retained(self):
        self.rows[('control', 'native')]['runtime']['cpuSeconds'] = 1.06
        self.rows[('allocation', 'native')]['build']['wallSeconds'] = 1.26
        failures = self.result()['failures']
        self.assertIn('control/runtime/cpuSeconds', failures)
        self.assertIn('allocation/build/wallSeconds', failures)

    def test_rss_has_its_separate_prospective_policy(self):
        self.rows[('allocation', 'native')]['runtime']['memoryBytes'] = 106
        self.assertNotIn('allocation/runtime/memoryBytes', self.result()['failures'])

    def test_missing_pure_go_cannot_authorize_increased_build_cost(self):
        del self.rows[('allocation', 'pure-go')]
        result = self.result()
        self.assertEqual(result['missingComparators'], ['allocation'])
        self.assertIn('allocation/build-trade/missing-pure-go', result['unknown'])

    def test_lost_build_advantage_is_retained(self):
        self.rows[('allocation', 'pure-go')]['build']['wallSeconds'] = 1.05
        self.assertIn('allocation/lost-build-advantage/pure-go', self.result()['failures'])

    def test_comparator_warmup_outlier_is_retained(self):
        self.groups[('allocation', 'typerb-go', 'runtime')].append({'phase': 'warmup', 'wallSeconds': 2.1})
        self.assertIn('allocation/outlier/typerb-go', self.result()['failures'])

    def test_incomplete_cohort_is_invalid(self):
        with self.assertRaises((ValueError, KeyError)):
            qualify.assess({'registration': {'candidate': 'a' * 40}}, {'revision': 'a' * 40, 'status': 'measured-with-failures'}, [])


class CompilerCostTests(unittest.TestCase):
    def setUp(self):
        self.roles = {role: {'revision': code * 40, 'sha256': code * 64, 'bytes': 100}
                      for role, code in [('native', 'a'), ('previous', 'b'), ('baseline', 'c')]}
        self.cost = {'status': 'pass', 'raw': [], 'summaries': {}, 'ratios': {},
                     'compilerBytes': dict.fromkeys(self.roles, 100)}
        for index in range(4):
            order = ('previous', 'native') if index % 2 == 0 else ('native', 'previous')
            for role in order:
                identity = self.roles[role]
                self.cost['raw'].append({'role': role, 'phase': 'warmup' if index == 0 else 'retained',
                    'status': 'pass', 'exitCode': 0, 'timeoutSeconds': 120,
                    'revision': identity['revision'], 'binarySha256': identity['sha256'],
                    'binaryBytes': 100, 'wallSeconds': 2, 'cpuSeconds': 1, 'memoryBytes': 100})
        for role in ('native', 'previous'):
            self.cost['summaries'][role] = {'wallSeconds': 2, 'cpuSeconds': 1,
                                           'memoryBytes': 100, 'wallMin': 2, 'wallMax': 2}
        self.cost['ratios'] = dict.fromkeys(qualify.METRICS, 1)

    def test_complete_matched_cost_is_required(self):
        qualify.check_compiler_cost(self.cost, self.roles)
        with self.assertRaises(ValueError):
            qualify.check_compiler_cost(None, self.roles)
        for change in ('status', 'count', 'order', 'source', 'binary', 'sample-count', 'summary', 'ratio'):
            value = copy.deepcopy(self.cost)
            if change == 'status': value['status'] = 'fail'
            if change == 'count': value['raw'].pop()
            if change == 'order': value['raw'].reverse()
            if change == 'source': value['raw'][0]['revision'] = 'c' * 40
            if change == 'binary': value['raw'][0]['binarySha256'] = 'c' * 64
            if change == 'sample-count': value['raw'][0]['phase'] = 'retained'
            if change == 'summary': value['summaries']['native']['wallSeconds'] = 3
            if change == 'ratio': value['ratios']['cpuSeconds'] = 2
            with self.subTest(change=change), self.assertRaises(ValueError):
                qualify.check_compiler_cost(value, self.roles)


if __name__ == '__main__':
    unittest.main()
