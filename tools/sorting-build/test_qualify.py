import copy
import unittest
import qualify
import readiness

class BuildTests(unittest.TestCase):
    def setUp(self):
        self.rows, self.groups = {}, {}
        for case in ('array-sorting', 'control'):
            for role, build in (('native', .8), ('previous', 1.1 if case == 'array-sorting' else .85), ('typerb-go', 1.), ('pure-go', .9)):
                runtime = .8 if role in ('native', 'previous') else 1.
                self.rows[(case, role)] = {'build': {'wallSeconds': build, 'cpuSeconds': build, 'memoryBytes': 100},
                    'runtime': {'wallSeconds': runtime, 'cpuSeconds': runtime, 'memoryBytes': 100}, 'artifactBytes': 100}
                self.groups[(case, role, 'runtime')] = [{'phase': 'retained', 'wallSeconds': runtime}] * 5
    def result(self):
        return qualify.evaluate_trade(self.rows, self.groups)
    def test_complete_win_is_met(self):
        self.assertEqual(self.result()['status'], 'met')
        self.assertEqual(self.result()['requestedOutcome'], 'met')
    def test_equal_build_is_not_faster(self):
        self.rows[('array-sorting','native')]['build']['wallSeconds'] = .9
        self.assertEqual(self.result()['requestedOutcome'], 'unmet')
    def test_display_band_is_preserved(self):
        self.rows[('array-sorting','native')]['build']['wallSeconds'] = .86
        self.assertIn('array-sorting/build/not-faster/pure-go', self.result()['failures'])
    def test_cpu_is_independent(self):
        self.rows[('array-sorting','native')]['build']['cpuSeconds'] = .9
        self.assertEqual(self.result()['requestedOutcome'], 'unmet')
    def test_primary_cpu_must_be_measured(self):
        self.rows[('array-sorting','native')]['build']['cpuSeconds'] = 0
        self.assertEqual(self.result()['requestedOutcome'], 'unmet')
    def test_control_win_cannot_replace_primary(self):
        self.rows[('array-sorting','native')]['build']['wallSeconds'] = 1.1
        self.assertEqual(self.result()['requestedOutcome'], 'unmet')
    def test_missing_sorting_comparator_is_invalid(self):
        del self.rows[('array-sorting','pure-go')]
        with self.assertRaises(ValueError): self.result()
    def test_runtime_regressions_are_not_build_trades(self):
        self.rows[('control','native')]['runtime']['cpuSeconds'] = .85
        self.assertIn('control/runtime/cpuSeconds', self.result()['failures'])
    def test_runtime_win_must_remain_faster(self):
        self.rows[('control','previous')]['runtime']['wallSeconds'] = .94
        self.rows[('control','native')]['runtime']['wallSeconds'] = .96
        self.assertIn('control/runtime/lost-win/typerb-go', self.result()['failures'])
    def test_control_build_regression_is_retained(self):
        self.rows[('control','native')]['build']['cpuSeconds'] = .9
        self.assertIn('control/build/cpuSeconds', self.result()['failures'])
    def test_build_memory_has_ordinary_guard(self):
        self.rows[('control','native')]['build']['memoryBytes'] = 106
        self.assertIn('control/build/memoryBytes', self.result()['failures'])
    def test_runtime_rss_has_separate_policy(self):
        self.rows[('control','native')]['runtime']['memoryBytes'] = 200
        self.assertNotIn('control/runtime/memoryBytes', self.result()['failures'])
    def test_application_size_has_ordinary_guard(self):
        self.rows[('control','native')]['artifactBytes'] = 106
        self.assertIn('control/bytes', self.result()['failures'])
    def test_outlier_in_comparator_warmup_is_retained(self):
        self.groups[('array-sorting','pure-go','runtime')].append({'phase':'warmup','wallSeconds':2.1})
        self.assertIn('array-sorting/outlier/pure-go', self.result()['failures'])
    def test_incomplete_cohort_is_invalid(self):
        with self.assertRaises((ValueError, KeyError)):
            qualify.assess({'registration': {'candidate':'a'*40}}, {'revision':'a'*40,'status':'measured-with-failures'}, [])
    def test_matched_compiler_cost_guards(self):
        c={'ratios':{'wallSeconds':1.,'cpuSeconds':1.,'memoryBytes':1.},'compilerBytes':{'native':100,'previous':100}}
        self.assertEqual(qualify.compiler_cost_failures(c),[])
        c['ratios']['wallSeconds']=1.06
        self.assertEqual(qualify.compiler_cost_failures(c),['compiler-self/wallSeconds'])
    def test_validation_requires_exact_source_and_complete_run(self):
        registration={'candidate':'a'*40,'requiredValidationRun':1}
        run={'id':1,'head_sha':'a'*40,'event':'pull_request','name':'Pull request validation','status':'completed','conclusion':'success'}
        qualify.validate_ci(run,registration)
        for field,value in [('head_sha','b'*40),('status','in_progress'),('conclusion','failure'),('id',2)]:
            changed=copy.deepcopy(run);changed[field]=value
            with self.assertRaises(ValueError):qualify.validate_ci(changed,registration)

class ReadinessTests(unittest.TestCase):
    def test_linked_binary_can_be_identical(self):
        readiness.check_primary([{'case':'array-sorting','role':role,'sha256':'a'*64} for role in ('native','previous')])
    def test_primary_must_exist(self):
        with self.assertRaises(ValueError):readiness.check_primary([])
    def test_ir_can_only_remove_unreferenced_definitions(self):
        previous='function $kept() {\nret\n}\nfunction $unused() {\nret\n}\n'
        current='function $kept() {\nret\n}\n'
        self.assertEqual(readiness.check_primary_ir(previous,current)['removedDefinitions'],1)
        with self.assertRaises(ValueError):readiness.check_primary_ir(previous,previous)
        with self.assertRaises(ValueError):readiness.check_primary_ir(previous,current.replace('ret','hlt'))
        previous='function $kept() {\ncall $unused()\nret\n}\nfunction $unused() {\nret\n}\n'
        with self.assertRaises(ValueError):readiness.check_primary_ir(previous,previous.split('function $unused')[0])

if __name__=='__main__':unittest.main()
