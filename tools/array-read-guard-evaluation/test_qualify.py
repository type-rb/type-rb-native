import copy
import unittest
import qualify


class TradeTests(unittest.TestCase):
    def setUp(self):
        self.rows, self.groups = {}, {}
        for case in ('fannkuch-redux', 'array-sorting', 'n-body', 'recursion', 'control'):
            for role, build, runtime in (('native', 1.03, .9 if case == 'fannkuch-redux' else .99),
                                         ('previous', 1., 1.), ('typerb-go', 2., 1.), ('pure-go', 1.5, 1.)):
                self.rows[(case, role)] = {'build': {'wallSeconds': build, 'cpuSeconds': build, 'memoryBytes': 100},
                    'runtime': {'wallSeconds': runtime, 'cpuSeconds': runtime, 'memoryBytes': 100}, 'artifactBytes': 100}
                self.groups[(case, role, 'runtime')] = [{'phase': 'retained', 'wallSeconds': runtime}] * 5

    def result(self):
        return qualify.evaluate_trade(self.rows, self.groups)

    def test_qualified_gain_and_new_go_win_are_both_recorded(self):
        result = self.result()
        self.assertEqual(result['status'], 'met')
        self.assertEqual(result['qualifiedPrimaries'], ['fannkuch-redux'])
        self.assertEqual(result['newGoWins'], ['fannkuch-redux'])

    def test_useful_gain_can_close_the_go_gap_without_crossing_it(self):
        self.rows[('fannkuch-redux', 'typerb-go')]['runtime']['wallSeconds'] = .8
        result = self.result()
        self.assertEqual(result['qualifiedPrimaries'], ['fannkuch-redux'])
        self.assertEqual(result['requestedOutcome'], 'met')
        self.assertGreater(result['goRatios']['fannkuch-redux']['native'], 1.)
        self.assertEqual(result['newGoWins'], [])

    def test_existing_go_win_is_distinguished_but_can_improve(self):
        self.rows[('fannkuch-redux', 'typerb-go')]['runtime']['wallSeconds'] = 2.
        self.assertEqual(self.result()['newGoWins'], [])
        self.assertEqual(self.result()['requestedOutcome'], 'met')

    def test_a_control_cannot_replace_primary(self):
        self.rows[('fannkuch-redux', 'native')]['runtime']['wallSeconds'] = .99
        self.rows[('array-sorting', 'native')]['runtime'].update(wallSeconds=.9, cpuSeconds=.9)
        self.assertEqual(self.result()['qualifiedPrimaries'], [])
        self.assertEqual(self.result()['newGoWins'], [])

    def test_unregistered_control_cannot_replace_primary(self):
        self.rows[('fannkuch-redux', 'native')]['runtime']['wallSeconds'] = .99
        self.rows[('control', 'native')]['runtime'].update(wallSeconds=.8, cpuSeconds=.8)
        self.assertEqual(self.result()['qualifiedPrimaries'], [])
        self.assertEqual(self.result()['newGoWins'], [])

    def test_primary_requires_one_millisecond_absolute_savings(self):
        for role, value in (("previous", .001), ("native", .0008)):
            self.rows[("fannkuch-redux", role)]["runtime"].update(wallSeconds=value, cpuSeconds=value)
            self.groups[("fannkuch-redux", role, "runtime")] = [{"phase":"retained", "wallSeconds":value}] * 5
        self.assertEqual(self.result()["qualifiedPrimaries"], [])

    def test_cpu_must_be_positive_measurable_and_improved(self):
        for cpu in (0., .98, 1., 1.01):
            self.rows[('fannkuch-redux', 'native')]['runtime']['cpuSeconds'] = cpu
            self.assertEqual(self.result()['qualifiedPrimaries'], [])

    def test_savings_cannot_be_combined_across_cases(self):
        self.rows[('fannkuch-redux', 'native')]['runtime']['cpuSeconds'] = 1.
        self.rows[('array-sorting', 'native')]['runtime']['cpuSeconds'] = .8
        self.assertEqual(self.result()['qualifiedPrimaries'], [])

    def test_both_metrics_need_three_percent(self):
        for metric in ('wallSeconds', 'cpuSeconds'):
            for value in (.97001, 1.):
                rows = copy.deepcopy(self.rows)
                rows[('fannkuch-redux', 'native')]['runtime'][metric] = value
                self.assertEqual(qualify.evaluate_trade(rows, self.groups)['qualifiedPrimaries'], [])

    def test_preexisting_runtime_faster_must_be_preserved(self):
        self.rows[('control', 'typerb-go')]['runtime']['wallSeconds'] = 1.1
        self.rows[('control', 'native')]['runtime']['wallSeconds'] = 1.049
        self.assertIn('control/lost-runtime-faster/typerb-go', self.result()['failures'])

    def test_primary_wall_and_cpu_are_joint_controls(self):
        for metric in ('wallSeconds', 'cpuSeconds'):
            rows = copy.deepcopy(self.rows)
            rows[('array-sorting', 'native')]['runtime'][metric] = 1.051
            self.assertIn('array-sorting/runtime/' + metric,
                          qualify.evaluate_trade(rows, self.groups)['failures'])

    def test_primary_win_cannot_be_exchanged_for_hash_win(self):
        self.rows[('array-sorting', 'typerb-go')]['runtime']['wallSeconds'] = 1.1
        self.rows[('array-sorting', 'native')]['runtime']['wallSeconds'] = 1.049
        result = self.result()
        self.assertEqual(result['newGoWins'], ['fannkuch-redux'])
        self.assertIn('array-sorting/lost-runtime-faster/typerb-go', result['failures'])

    def test_primary_control_cannot_be_omitted(self):
        del self.rows[('array-sorting', 'previous')]
        with self.assertRaises(ValueError):
            self.result()

    def test_preexisting_build_faster_must_be_preserved(self):
        self.rows[('control', 'pure-go')]['build']['wallSeconds'] = 1.1
        self.rows[('control', 'native')]['build']['wallSeconds'] = 1.049
        self.assertIn('control/lost-build-faster/pure-go', self.result()['failures'])

    def test_validation_requires_exact_source_and_complete_run(self):
        registration={'candidate':'a'*40,'requiredValidationRun':1,
                      'validationRevision':'b'*40,'requiredCompleteRun':2,
                      'requiredCompleteJobs':['native / verify','Native CI acceptance']}
        production={'id':1,'head_sha':'a'*40,'event':'pull_request','name':'Pull request validation','status':'completed','conclusion':'success'}
        complete=dict(production,id=2,head_sha='b'*40)
        jobs=[dict(name=name,status='completed',conclusion='success') for name in registration['requiredCompleteJobs']]
        run={'production':production,'complete':complete,'completeJobs':{'jobs':jobs}}
        qualify.validate_ci(run,registration)
        for role in ('production','complete'):
            for field,value in [('head_sha','c'*40),('status','in_progress'),('conclusion','failure'),('id',3),('event','push')]:
                changed=copy.deepcopy(run);changed[role][field]=value
                with self.assertRaises(ValueError):qualify.validate_ci(changed,registration)
        for replacement in (jobs[:1], jobs + jobs[:1], [dict(jobs[0],conclusion='skipped'),jobs[1]]):
            changed=copy.deepcopy(run);changed['completeJobs']['jobs']=replacement
            with self.assertRaises(ValueError):qualify.validate_ci(changed,registration)

    def test_runtime_and_build_alarms_are_retained(self):
        self.rows[('control', 'native')]['runtime']['cpuSeconds'] = 1.06
        self.rows[('fannkuch-redux', 'native')]['build']['wallSeconds'] = 1.26
        failures = self.result()['failures']
        self.assertIn('control/runtime/cpuSeconds', failures)
        self.assertIn('fannkuch-redux/build/wallSeconds', failures)

    def test_unresolved_control_cpu_is_not_an_automatic_pass(self):
        self.rows[('control', 'native')]['runtime']['cpuSeconds'] = 0
        result = self.result()
        self.assertEqual(result['status'], 'review-required')
        self.assertIn('control/runtime/cpuSeconds', result['unknown'])

    def test_rss_has_its_separate_prospective_policy(self):
        self.rows[('fannkuch-redux', 'native')]['runtime']['memoryBytes'] = 106
        self.assertNotIn('fannkuch-redux/runtime/memoryBytes', self.result()['failures'])

    def test_missing_pure_go_cannot_authorize_increased_build_cost(self):
        self.rows[('fannkuch-redux', 'native')]['build']['wallSeconds'] = 1.06
        del self.rows[('fannkuch-redux', 'pure-go')]
        result = self.result()
        self.assertEqual(result['missingComparators'], ['fannkuch-redux'])
        self.assertIn('fannkuch-redux/build-trade/missing-pure-go', result['unknown'])

    def test_lost_build_advantage_is_retained(self):
        self.rows[('fannkuch-redux', 'pure-go')]['build']['wallSeconds'] = 1.02
        self.assertIn('fannkuch-redux/lost-build-advantage/pure-go', self.result()['failures'])

    def test_comparator_warmup_outlier_is_retained(self):
        self.groups[('fannkuch-redux', 'typerb-go', 'runtime')].append({'phase': 'warmup', 'wallSeconds': 2.1})
        self.assertIn('fannkuch-redux/outlier/typerb-go', self.result()['failures'])

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
        roles = {role: {'revision':role, 'sha256':str(index)*64, 'bytes':100 + index}
                 for index, role in enumerate(('previous','native','baseline'))}
        order = ['previous','native','native','previous','previous','native','native','previous']
        raw = [dict(role=role,phase='warmup' if i < 2 else 'retained',status='pass',exitCode=0,
                    timeoutSeconds=120,revision=role,sourceRevision='previous',binarySha256=roles['previous']['sha256'],
                    binaryBytes=100,wallSeconds=1.,cpuSeconds=1.,memoryBytes=100)
               for i,role in enumerate(order)]
        summary = dict(wallSeconds=1.,cpuSeconds=1.,memoryBytes=100,wallMin=1.,wallMax=1.)
        cost = dict(status='pass',raw=raw,outputIdentities={role:{'sha256':roles['previous']['sha256'],'bytes':100} for role in ('native','previous')},summaries={role:summary for role in ('previous','native')},
                    compilerBytes={role:r['bytes'] for role,r in roles.items()},
                    ratios=dict(wallSeconds=1.,cpuSeconds=1.,memoryBytes=1.))
        qualify.check_compiler_cost(cost,roles)
        optimized = copy.deepcopy(cost)
        optimized['outputIdentities']['native'] = {'sha256':'f'*64,'bytes':99}
        for row in optimized['raw']:
            if row['role'] == 'native':
                row['binarySha256'] = 'f'*64
                row['binaryBytes'] = 99
        qualify.check_compiler_cost(optimized, roles)
        optimized['raw'][1]['binarySha256'] = 'e'*64
        with self.assertRaises(ValueError):
            qualify.check_compiler_cost(optimized, roles)
        for field,value in [('sourceRevision','native'),('binarySha256','native'),('binaryBytes',101)]:
            changed=copy.deepcopy(cost);changed['raw'][1][field]=value
            with self.assertRaises(ValueError):qualify.check_compiler_cost(changed,roles)

if __name__=='__main__':unittest.main()
