import copy
import json
from pathlib import Path
import unittest
import qualify


class IntegrationAssessmentTests(unittest.TestCase):
    def test_fixed_runtime_role_order_fails_even_with_complete_counts(self):
        rows = [dict(case="synthetic", role=role) for role in ("native", "previous")]
        raw = []
        for kind, count in (("build", 4), ("runtime", 6)):
            for index in range(count):
                for role in (("native", "previous") if index % 2 == 0 else ("previous", "native")):
                    raw.append(dict(case="synthetic", kind=kind, role=role,
                                    phase="warmup" if index == 0 else "retained"))
        qualify.validate_observation_order(rows, raw)
        wrong = copy.deepcopy(raw)
        wrong[10:12] = reversed(wrong[10:12])
        with self.assertRaisesRegex(ValueError, "observation order"):
            qualify.validate_observation_order(rows, wrong)

    def setUp(self):
        self.rows, self.groups = {}, {}
        self.cases = [case['id'] for case in json.loads((Path(__file__).parents[1] / 'daily-performance/suite.json').read_text())['cases']]
        for case in self.cases:
            for role, build, runtime in [('native', 1.03, .9), ('previous', 1., 1.), ('typerb-go', 2., 1.), ('pure-go', 1.5, 1.)]:
                self.rows[case, role] = dict(build=dict(wallSeconds=build, cpuSeconds=build, memoryBytes=100), runtime=dict(wallSeconds=runtime, cpuSeconds=runtime, memoryBytes=100), artifactBytes=100)
                self.groups[case, role, 'runtime'] = [dict(phase='retained', wallSeconds=runtime)] * 5

    def result(self):
        return qualify.evaluate_trade(self.rows, self.groups)

    def test_all_sixteen_and_every_primary_are_counted(self):
        result = self.result()
        self.assertEqual(result['requestedOutcome'], 'met')
        self.assertEqual(result['status'], 'met')
        self.assertEqual(len(result['runtimeGoWins']), 16)
        self.assertEqual(result['qualifiedPrimaries'], list(qualify.PRIMARIES))

    def test_one_tie_or_small_advantage_does_not_count_as_all_wins(self):
        for value in [.950001, 1., 1.1]:
            self.rows['startup', 'native']['runtime']['wallSeconds'] = value
            result = self.result()
            self.assertEqual(result['requestedOutcome'], 'unmet')
            self.assertEqual(len(result['runtimeGoWins']), 15)

    def test_threshold_is_inclusive(self):
        self.rows['startup', 'native']['runtime']['wallSeconds'] = .95
        self.assertEqual(self.result()['requestedOutcome'], 'met')

    def test_missing_case_never_becomes_fifteen_of_fifteen(self):
        for key in list(self.rows):
            if key[0] == 'startup': del self.rows[key]
        self.assertEqual(self.result()['requestedOutcome'], 'unmet')

    def test_primary_gain_and_all_wins_are_distinct(self):
        self.rows['closures', 'typerb-go']['runtime']['wallSeconds'] = .8
        result = self.result()
        self.assertIn('closures', result['qualifiedPrimaries'])
        self.assertEqual(result['requestedOutcome'], 'unmet')

    def test_gain_needs_three_percent_wall_and_cpu_and_one_ms(self):
        for case in qualify.PRIMARIES:
            self.rows[case, 'native']['runtime']['cpuSeconds'] = .98
        self.assertEqual(self.result()['qualifiedPrimaries'], [])
        for case in qualify.PRIMARIES:
            for role, value in [('native', .0008), ('previous', .001)]:
                self.rows[case, role]['runtime'].update(wallSeconds=value, cpuSeconds=value)
                self.groups[case, role, 'runtime'] = [dict(phase='retained', wallSeconds=value)] * 5
        self.assertEqual(self.result()['qualifiedPrimaries'], [])

    def test_unknown_cpu_is_retained(self):
        self.rows['startup', 'native']['runtime']['cpuSeconds'] = 0
        self.assertIn('startup/runtime/cpuSeconds', self.result()['unknown'])

    def test_ordinary_regression_remains_a_miss_despite_all_go_wins(self):
        self.rows['startup', 'previous']['runtime']['wallSeconds'] = .5
        result = self.result()
        self.assertEqual(result['requestedOutcome'], 'met')
        self.assertIn('startup/runtime/wallSeconds', result['failures'])

    def test_existing_pure_go_win_and_build_advantage_are_preserved(self):
        self.rows['array-sorting', 'pure-go']['runtime']['wallSeconds'] = 1.2
        self.rows['array-sorting', 'native']['runtime']['wallSeconds'] = 1.15
        self.rows['array-sorting', 'pure-go']['build']['wallSeconds'] = 1.02
        result = self.result()
        self.assertIn('array-sorting/lost-runtime-faster/pure-go', result['failures'])
        self.assertIn('array-sorting/lost-build-advantage/pure-go', result['failures'])

    def test_first_run_outlier_is_not_removed(self):
        self.groups['startup', 'typerb-go', 'runtime'].append(dict(phase='warmup', wallSeconds=3.))
        self.assertIn('startup/outlier/typerb-go', self.result()['failures'])

    def test_compiler_cost_thresholds_are_not_changed(self):
        cost = dict(ratios={key:1.051 for key in qualify.METRICS}, compilerBytes=dict(native=106,previous=100))
        self.assertEqual(len(qualify.compiler_cost_failures(cost)), 4)

    def test_validation_requires_exact_successful_runs_and_every_job(self):
        registration = dict(candidate='a'*40,requiredValidationRun=1,requiredValidationAttempt=1,validationRevision='b'*40,requiredCompleteRun=2,requiredCompleteJobs=['native / verify','Native CI acceptance'])
        product = dict(id=1,run_attempt=1,head_sha='a'*40,event='pull_request',name='Pull request validation',status='completed',conclusion='success')
        complete = dict(product,id=2,head_sha='b'*40)
        jobs = [dict(name=name,status='completed',conclusion='success') for name in registration['requiredCompleteJobs']]
        evidence = dict(production=product,complete=complete,completeJobs=dict(jobs=jobs))
        qualify.validate_ci(evidence,registration)
        for role in ['production','complete']:
            for field,value in [('head_sha','c'*40),('id',3),('run_attempt',2),('status','in_progress'),('conclusion','failure'),('event','push')]:
                changed=copy.deepcopy(evidence);changed[role][field]=value
                with self.assertRaises(ValueError):qualify.validate_ci(changed,registration)
        for replacement in [jobs[:1],jobs+jobs[:1],[dict(jobs[0],conclusion='skipped'),jobs[1]]]:
            changed=copy.deepcopy(evidence);changed['completeJobs']['jobs']=replacement
            with self.assertRaises(ValueError):qualify.validate_ci(changed,registration)


    def test_one_full_exact_source_run_can_supply_both_ci_authorities(self):
        registration = dict(candidate='a'*40,requiredValidationRun=1,requiredValidationAttempt=1,validationRevision='a'*40,requiredCompleteRun=1,requiredCompleteJobs=['native / verify','Native CI acceptance'])
        run = dict(id=1,run_attempt=1,head_sha='a'*40,event='pull_request',name='Pull request validation',status='completed',conclusion='success')
        jobs = [dict(name=name,status='completed',conclusion='success') for name in registration['requiredCompleteJobs']]
        evidence = dict(production=run,complete=run,completeJobs=dict(jobs=jobs))
        qualify.validate_ci(evidence,registration)
        evidence['completeJobs']['jobs'][0]['conclusion'] = 'skipped'
        with self.assertRaises(ValueError):qualify.validate_ci(evidence,registration)


if __name__ == '__main__': unittest.main()
