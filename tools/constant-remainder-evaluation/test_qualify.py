import copy
import unittest
import qualify


class TradeTests(unittest.TestCase):
    def setUp(self):
        self.rows, self.groups = {}, {}
        for case in ('enum-result', 'n-body', 'fannkuch-redux', 'control'):
            for role, build, runtime in (('native', 1.03, .9 if case == 'enum-result' else .99),
                                         ('previous', 1., 1.), ('typerb-go', 2., 1.), ('pure-go', 1.5, 1.)):
                self.rows[(case, role)] = {'build': {'wallSeconds': build, 'cpuSeconds': build, 'memoryBytes': 100},
                    'runtime': {'wallSeconds': runtime, 'cpuSeconds': runtime, 'memoryBytes': 100}, 'artifactBytes': 100}
                self.groups[(case, role, 'runtime')] = [{'phase': 'retained', 'wallSeconds': runtime}] * 5

    def result(self):
        return qualify.evaluate_trade(self.rows, self.groups)

    def test_qualified_gain_and_new_go_win_are_both_recorded(self):
        result = self.result()
        self.assertEqual(result['status'], 'met')
        self.assertEqual(result['qualifiedPrimaries'], ['enum-result'])
        self.assertEqual(result['newGoWins'], ['enum-result'])

    def test_useful_gain_can_close_the_go_gap_without_crossing_it(self):
        self.rows[('enum-result', 'typerb-go')]['runtime']['wallSeconds'] = .8
        result = self.result()
        self.assertEqual(result['qualifiedPrimaries'], ['enum-result'])
        self.assertEqual(result['requestedOutcome'], 'met')
        self.assertGreater(result['goRatios']['enum-result']['native'], 1.)
        self.assertEqual(result['newGoWins'], [])

    def test_existing_go_win_is_distinguished_but_can_improve(self):
        self.rows[('enum-result', 'typerb-go')]['runtime']['wallSeconds'] = 2.
        self.assertEqual(self.result()['newGoWins'], [])
        self.assertEqual(self.result()['requestedOutcome'], 'met')

    def test_a_control_cannot_replace_primary(self):
        self.rows[('enum-result', 'native')]['runtime']['wallSeconds'] = .99
        self.rows[('n-body', 'native')]['runtime'].update(wallSeconds=.9, cpuSeconds=.9)
        self.assertEqual(self.result()['qualifiedPrimaries'], [])
        self.assertEqual(self.result()['newGoWins'], [])

    def test_unregistered_control_cannot_replace_primary(self):
        self.rows[('enum-result', 'native')]['runtime']['wallSeconds'] = .99
        self.rows[('control', 'native')]['runtime'].update(wallSeconds=.8, cpuSeconds=.8)
        self.assertEqual(self.result()['qualifiedPrimaries'], [])
        self.assertEqual(self.result()['newGoWins'], [])

    def test_cpu_must_be_positive_measurable_and_improved(self):
        for cpu in (0., .96, 1., 1.01):
            self.rows[('enum-result', 'native')]['runtime']['cpuSeconds'] = cpu
            self.assertEqual(self.result()['qualifiedPrimaries'], [])

    def test_savings_cannot_be_combined_across_cases(self):
        self.rows[('enum-result', 'native')]['runtime']['cpuSeconds'] = 1.
        self.rows[('n-body', 'native')]['runtime']['cpuSeconds'] = .8
        self.assertEqual(self.result()['qualifiedPrimaries'], [])

    def test_both_metrics_need_ten_percent(self):
        for metric in ('wallSeconds', 'cpuSeconds'):
            for value in (.90001, .95):
                rows = copy.deepcopy(self.rows)
                rows[('enum-result', 'native')]['runtime'][metric] = value
                self.assertEqual(qualify.evaluate_trade(rows, self.groups)['qualifiedPrimaries'], [])

    def test_preexisting_runtime_faster_must_be_preserved(self):
        self.rows[('control', 'typerb-go')]['runtime']['wallSeconds'] = 1.1
        self.rows[('control', 'native')]['runtime']['wallSeconds'] = 1.049
        self.assertIn('control/lost-runtime-faster/typerb-go', self.result()['failures'])

    def test_preexisting_build_faster_must_be_preserved(self):
        self.rows[('control', 'pure-go')]['build']['wallSeconds'] = 1.1
        self.rows[('control', 'native')]['build']['wallSeconds'] = 1.049
        self.assertIn('control/lost-build-faster/pure-go', self.result()['failures'])

    def test_validation_requires_exact_source_and_complete_run(self):
        registration={'candidate':'a'*40,'requiredValidationRun':1}
        run={'id':1,'head_sha':'a'*40,'event':'pull_request','name':'Pull request validation','status':'completed','conclusion':'success'}
        qualify.validate_ci(run,registration)
        for field,value in [('head_sha','b'*40),('status','in_progress'),('conclusion','failure'),('id',2)]:
            changed=copy.deepcopy(run);changed[field]=value
            with self.assertRaises(ValueError):qualify.validate_ci(changed,registration)

    def test_runtime_and_build_alarms_are_retained(self):
        self.rows[('control', 'native')]['runtime']['cpuSeconds'] = 1.06
        self.rows[('enum-result', 'native')]['build']['wallSeconds'] = 1.26
        failures = self.result()['failures']
        self.assertIn('control/runtime/cpuSeconds', failures)
        self.assertIn('enum-result/build/wallSeconds', failures)

    def test_unresolved_control_cpu_is_not_an_automatic_pass(self):
        self.rows[('control', 'native')]['runtime']['cpuSeconds'] = 0
        result = self.result()
        self.assertEqual(result['status'], 'review-required')
        self.assertIn('control/runtime/cpuSeconds', result['unknown'])

    def test_rss_has_its_separate_prospective_policy(self):
        self.rows[('enum-result', 'native')]['runtime']['memoryBytes'] = 106
        self.assertNotIn('enum-result/runtime/memoryBytes', self.result()['failures'])

    def test_missing_pure_go_cannot_authorize_increased_build_cost(self):
        self.rows[('enum-result', 'native')]['build']['wallSeconds'] = 1.06
        del self.rows[('enum-result', 'pure-go')]
        result = self.result()
        self.assertEqual(result['missingComparators'], ['enum-result'])
        self.assertIn('enum-result/build-trade/missing-pure-go', result['unknown'])

    def test_lost_build_advantage_is_retained(self):
        self.rows[('enum-result', 'pure-go')]['build']['wallSeconds'] = 1.02
        self.assertIn('enum-result/lost-build-advantage/pure-go', self.result()['failures'])

    def test_comparator_warmup_outlier_is_retained(self):
        self.groups[('enum-result', 'typerb-go', 'runtime')].append({'phase': 'warmup', 'wallSeconds': 2.1})
        self.assertIn('enum-result/outlier/typerb-go', self.result()['failures'])

    def test_incomplete_cohort_is_invalid(self):
        with self.assertRaises((ValueError, KeyError)):
            qualify.assess({'registration': {'candidate': 'a' * 40}}, {'revision': 'a' * 40, 'status': 'measured-with-failures'}, [])


class CompilerCostAlarmTests(unittest.TestCase):
    def test_compiler_cost_alarms_cannot_be_hidden_by_runtime_gain(self):
        cost = {"ratios": dict.fromkeys(qualify.METRICS, 1.),
                "compilerBytes": {"native": 100, "previous": 100}}
        self.assertEqual(qualify.compiler_cost_failures(cost), [])
        for metric in qualify.METRICS:
            changed = copy.deepcopy(cost)
            changed["ratios"][metric] = 1.051
            self.assertEqual(qualify.compiler_cost_failures(changed), ["compiler-self/" + metric])
        cost["compilerBytes"]["native"] = 106
        self.assertEqual(qualify.compiler_cost_failures(cost), ["compiler/bytes"])


class MatchedInputTests(unittest.TestCase):
    def test_both_compilers_build_the_accepted_input_and_output(self):
        roles = {role: {'revision':role, 'sha256':role, 'bytes':100 + index}
                 for index, role in enumerate(('previous','native','baseline'))}
        order = ['previous','native','native','previous','previous','native','native','previous']
        raw = [dict(role=role,phase='warmup' if i < 2 else 'retained',status='pass',exitCode=0,
                    timeoutSeconds=120,revision=role,sourceRevision='previous',binarySha256='previous',
                    binaryBytes=100,wallSeconds=1.,cpuSeconds=1.,memoryBytes=100)
               for i,role in enumerate(order)]
        summary = dict(wallSeconds=1.,cpuSeconds=1.,memoryBytes=100,wallMin=1.,wallMax=1.)
        cost = dict(status='pass',raw=raw,summaries={role:summary for role in ('previous','native')},
                    compilerBytes={role:r['bytes'] for role,r in roles.items()},
                    ratios=dict(wallSeconds=1.,cpuSeconds=1.,memoryBytes=1.))
        qualify.check_compiler_cost(cost,roles)
        for field,value in [('sourceRevision','native'),('binarySha256','native'),('binaryBytes',101)]:
            changed=copy.deepcopy(cost);changed['raw'][1][field]=value
            with self.assertRaises(ValueError):qualify.check_compiler_cost(changed,roles)

if __name__=='__main__':unittest.main()
