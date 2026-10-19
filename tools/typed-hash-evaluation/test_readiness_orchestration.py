"""Exercise readiness orchestration without executing compilers or programs."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import readiness


class ReadinessOrchestrationTests(unittest.TestCase):
    def exercise_matrix(self, both_pure_go):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / 'observations'
            daily = root / 'tools/daily-performance'
            controller = root / 'tools/typed-hash-evaluation'
            daily.mkdir(parents=True)
            controller.mkdir(parents=True)
            cases = [dict(id='hash-string-keys', args=[]),
                     dict(id='hash-integer-keys', args=[], pureGoSource='strings.go')]
            if both_pure_go:
                cases[0]['pureGoSource'] = 'integers.go'
                (root / 'integers.go').write_text('package main\n')
            (daily / 'suite.json').write_text(json.dumps(dict(cases=cases)))
            (controller / 'registration.json').write_text(json.dumps(dict(priorLinuxCompilers={})))
            (root / 'strings.go').write_text('package main\n')
            compilers = root / 'compilers.json'
            compilers.write_text(json.dumps({role: dict(path=role+'-tool')
                                            for role in ('native', 'previous', 'typerb-go', 'baseline')}))
            gc = dict(collections=2, **{'automatic-collections': 1, 'allocated-bytes': 100,
                      'reclaimed-bytes': 100, 'live-bytes': 0, 'peak-heap-bytes': 100})
            gc_text = ''.join(f'type-rb-native-gc-stat-v1,{key},{value}\n' for key, value in gc.items()).encode()
            observed_commands = []

            def stage_source(case, directory):
                (directory / 'src').mkdir(parents=True)
                (directory / 'src/main.trb').write_text('def main()\nend\n')
                return b'expected\n'

            def external_command(command, cwd, env, **unused):
                observed_commands.append(command)
                stdout, stderr = b'', b''
                if len(command) > 1 and command[1] == 'emit-qbe':
                    case = Path(command[2]).parents[1].name
                    role = command[0].removesuffix('-tool')
                    expected = readiness.expected_ir(case, role)
                    body = 'function l $trbnf0() {\n@start\n'
                    for field, name in [('typedMembership','contains'),('typedRead','get'),('typedSlot','existing_slot')]:
                        body += (' call $trbn_hash_' + name + '_integer(l 0,l 0)\n') * expected[field]
                    body += ' ret 0\n}\n'
                    if expected['specializedProbe']:
                        body += 'function l $trbn_hash_slot_integer(l %table,l %key) {\n ret 0\n}\n'
                    stdout = body.encode()
                elif len(command) > 1 and command[1] == 'build':
                    flag = next(flag for flag in ('--output', '--outfile', '-o') if flag in command)
                    executable = Path(command[command.index(flag) + 1])
                    role, case = executable.parent.name, executable.parents[1].name
                    identity = 'same-native' if case == 'hash-string-keys' and role in ('native', 'previous') else role
                    executable.write_bytes((case + '/' + identity).encode())
                else:
                    self.assertEqual(Path(command[0]).name, 'program')
                    stdout = b'expected\n'
                    if env.get('TYPE_RB_NATIVE_RUNTIME_STATS') == '1':
                        stderr = gc_text
                return subprocess.CompletedProcess(command, 0, stdout, stderr)

            argv = ['readiness.py', '--compilers', str(compilers), '--qbe', 'qbe-tool', '--output', str(output)]
            with patch.object(readiness, 'ROOT', root), \
                 patch.object(readiness, 'REGISTRATION', controller / 'registration.json', create=True), \
                 patch.object(readiness, 'source_case', side_effect=stage_source), \
                 patch.object(readiness, 'validate_prior_compilers'), \
                 patch.object(readiness.shutil, 'which', return_value='pure-go-tool'), \
                 patch.object(readiness.subprocess, 'run', side_effect=external_command), \
                 patch.object(readiness.subprocess, 'check_output', return_value='go version test'), \
                 patch.object(readiness.sys, 'argv', argv), contextlib.redirect_stdout(io.StringIO()):
                readiness.main()
            result = json.loads((output / 'readiness.json').read_text())
            self.assertEqual(result['status'], 'pass')
            self.assertEqual(result['productExecutions'], 36 if both_pure_go else 32)
            self.assertEqual(len(observed_commands), 36 if both_pure_go else 32)
            self.assertEqual(len(result['rows']), 8 if both_pure_go else 7)
            self.assertEqual(('hash-string-keys', 'pure-go') in {(row['case'], row['role']) for row in result['rows']}, both_pure_go)
            self.assertEqual(set(result['ir']), {'hash-string-keys', 'hash-integer-keys'})
            self.assertEqual(result['allocation']['allocatedBytesRatio'], 1.)


    def test_both_pure_go_cases_complete_eight_row_matrix(self):
        self.exercise_matrix(True)

    def test_missing_comparator_cannot_satisfy_registered_command_budget(self):
        with self.assertRaisesRegex(ValueError, "Incomplete readiness command budget"):
            self.exercise_matrix(False)

    def matrix(self):
        suite = dict(cases=[dict(id='hash-string-keys'), dict(id='hash-integer-keys', pureGoSource='strings.go')])
        pairs = [('hash-string-keys', role) for role in ('native', 'previous', 'typerb-go')]
        pairs += [('hash-integer-keys', role) for role in ('native', 'previous', 'typerb-go', 'pure-go')]
        return suite, [dict(case=case, role=role) for case, role in pairs]

    def test_declared_seven_pair_matrix_is_complete(self):
        suite, rows = self.matrix()
        readiness.validate_matrix(rows, suite)

    def test_missing_duplicate_and_unavailable_roles_are_rejected(self):
        suite, rows = self.matrix()
        for index in range(len(rows)):
            with self.assertRaises(ValueError):
                readiness.validate_matrix(rows[:index] + rows[index+1:], suite)
        for extra in [rows[0], dict(case='hash-string-keys', role='pure-go'),
                      dict(case='hash-integer-keys', role='baseline')]:
            with self.assertRaises(ValueError):
                readiness.validate_matrix(rows + [extra], suite)
        with self.assertRaises(ValueError):
            readiness.validate_matrix(rows[:-1] + [rows[0]], suite)

    def test_missing_or_duplicate_suite_cases_are_rejected(self):
        suite, rows = self.matrix()
        with self.assertRaises(ValueError):
            readiness.validate_matrix(rows, dict(cases=suite['cases'][:1]))
        with self.assertRaises(ValueError):
            readiness.validate_matrix(rows, dict(cases=suite['cases'] + [suite['cases'][0]]))


if __name__ == '__main__':
    unittest.main()
