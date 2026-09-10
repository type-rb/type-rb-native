#!/usr/bin/env python3
"""Exercise the built CLI through public commands and a real terminal."""
import argparse
import errno
import json
import os
from pathlib import Path
import pty
import select
import signal
import subprocess
import tempfile
import time

parser = argparse.ArgumentParser()
parser.add_argument('binary', type=Path)
args = parser.parse_args()
binary = args.binary.resolve()
repository = Path(__file__).resolve().parent.parent

with tempfile.TemporaryDirectory(prefix='native cli ') as temporary:
    root = Path(temporary)
    env = dict(os.environ, TRBN_HISTORY=str(root / 'history.json'), TERM='xterm', NO_COLOR='1')

    def run(*arguments, text=None, cwd=root, success=True):
        result = subprocess.run([str(binary), *map(str, arguments)], input=text,
                                text=True, capture_output=True, cwd=cwd, env=env,
                                timeout=30)
        if (result.returncode == 0) != success:
            raise AssertionError((arguments, result.returncode, result.stdout, result.stderr))
        return result.stdout + result.stderr

    # These sources exercise the checked compiler and the independent REPL evaluator.
    for case_name in ('elsif-control', 'elsif-managed', 'loop-transfer-control',
                      'loop-transfer-effects', 'loop-transfer-managed', 'array-assignment-targets',
                      'array-assignment-managed', 'array-assignment-recovery',
                      'boolean-array-values', 'boolean-array-effects', 'boolean-array-managed',
                      'record-field-values', 'record-array-values',
                      'record-array-effects', 'record-array-managed', 'local-array-header-mir',
                      'stable-array-bindings', 'conditional-array-headers', 'loop-array-headers',
                      'hash-values', 'hash-managed', 'hash-cycles'):
        fixture = repository / 'compiler/conformance/valid' / (case_name + '.trb')
        expected = fixture.with_suffix('.out').read_text()
        case_source = root / (case_name + '.trb')
        case_source.write_text(fixture.read_text())
        assert run('check', case_source) == 'ok\n'
        case_output = root / case_name
        run('build', '--compile', '--outfile', case_output, case_source)
        assert subprocess.check_output([case_output], text=True, timeout=30) == expected
        if case_name in ('elsif-managed', 'loop-transfer-managed', 'array-assignment-managed',
                         'boolean-array-managed', 'record-array-managed', 'hash-managed', 'hash-cycles'):
            collected = subprocess.run([case_output], text=True, capture_output=True,
                                       env=dict(env, TYPE_RB_NATIVE_RUNTIME_STATS='1'), timeout=30)
            assert collected.returncode == 0 and collected.stdout == expected
            automatic = [line.split(',')[-1] for line in collected.stderr.splitlines()
                         if line.startswith('type-rb-native-gc-stat-v1,automatic-collections,')]
            assert len(automatic) == 1 and int(automatic[0]) > 0, collected.stderr
        submission = fixture.read_text().replace('def main()', 'def exercise_control_case()')
        assert run('repl', text=submission + '\nexercise_control_case()\n:quit\n') == expected
    failure = repository / 'compiler/conformance/runtime-invalid/array-assignment-initial.trb'
    submission = failure.read_text().replace('def main()', 'def invalid_assignment_case()')
    failure_output = run('repl', text=submission + '\ninvalid_assignment_case()\n:quit\n')
    assert 'out of bounds' in failure_output, failure_output
    assert 'unexpected RHS' not in failure_output, failure_output
    for case_name in ('boolean-array-negative', 'boolean-array-past-end',
                      'record-array-negative', 'record-array-past-end', 'local-array-header-bounds',
                      'stable-array-bindings-bounds', 'conditional-array-header-bounds',
                      'loop-array-header-bounds', 'loop-array-header-negative'):
        fixture = repository / 'compiler/conformance/runtime-invalid' / (case_name + '.trb')
        case_source = root / (case_name + '.trb')
        case_source.write_text(fixture.read_text())
        assert run('check', case_source) == 'ok\n'
        case_output = root / case_name
        run('build', '--compile', '--outfile', case_output, case_source)
        failed = subprocess.run([case_output], text=True, capture_output=True, timeout=30)
        assert failed.returncode != 0 and failed.stdout == '', failed
        assert failed.stderr == fixture.with_suffix('.stderr').read_text(), failed
        submission = fixture.read_text().replace('def main()', 'def invalid_boolean_index()')
        assert 'out of bounds' in run('repl', text=submission + '\ninvalid_boolean_index()\n:quit\n')
    for case_name in ('elsif-after-else', 'elsif-branch-binding', 'elsif-condition',
                      'elsif-escaping-binding', 'elsif-missing-condition', 'elsif-outside-if',
                      'loop-transfer-break-outside-loop', 'loop-transfer-next-outside-loop',
                      'loop-transfer-break-value', 'loop-transfer-next-value',
                      'loop-transfer-break-condition', 'boolean-array-element', 'boolean-array-write',
                      'boolean-array-push', 'boolean-array-index', 'boolean-array-constant-mutation',
                      'boolean-array-depth', 'boolean-array-parameter', 'boolean-array-readonly',
                      'boolean-array-invariance', 'record-field-write', 'record-field-compound',
                      'record-field-parenthesized', 'record-field-array-replace', 'record-field-call',
                      'record-field-array-immutable', 'record-field-nested', 'record-field-return',
                      'record-array-element', 'record-array-write', 'record-array-push',
                      'record-array-index', 'record-array-constant-mutation', 'record-array-readonly',
                      'record-array-invariance', 'record-array-field-mutation', 'record-array-depth',
                      'record-array-unknown'):
        fixture = repository / 'compiler/conformance/invalid' / (case_name + '.source')
        case_source = root / (case_name + '.trb')
        case_source.write_text(fixture.read_text())
        assert 'TRBN' in run('check', case_source, success=False)
        assert 'TRBN' in run('build', '--compile', case_source, success=False)
        submission = fixture.read_text().replace('def main()', 'def invalid_control_case()')
        rejection = run('repl', text=submission + '\n:quit\n')
        if case_name == 'loop-transfer-break-condition':
            assert 'incomplete input at end of session' in rejection
        else:
            assert 'TRBN' in rejection

    failed_condition = run('repl', text='def visited(): Boolean\nputs("unexpected effect")\nreturn true\nend\nif false\nputs("wrong")\nelsif 1 / 0 == 0\nputs("wrong")\nelsif visited()\nputs("wrong")\nend\n:quit\n')
    assert 'division by zero' in failed_condition
    assert 'unexpected effect' not in failed_condition
    assert 'wrong' not in failed_condition

    assert 'default mode: trb' in run('--version')
    assert 'Usage:' in run()
    assert 'Usage:' in run('-h')
    for arguments in [('fmt',), ('--mode=',), ('--config',), ('build', '--compile', '--stdout')]:
        run(*arguments, success=False)
    hello = root / 'hello world.trb'
    hello.write_text('import trb/std/process\ndef main()\nputs(Process.argv()[0])\nend\n')
    assert run(hello, '--', 'spaces; $literal') == 'spaces; $literal\n'
    assert run('run', hello, '--', '--flag') == '--flag\n'
    run('check', hello)
    run('check', hello, '--mode=trb')
    assert 'not implemented' in run('check', hello, '--mode', 'go', success=False)
    run('build', hello)
    assert (root / 'build/hello world.ssa').read_text().lstrip().startswith('data ')
    assert 'export function' in run('build', hello, '--stdout')
    executable = root / 'out dir/hello'
    run('build', hello, '--compile', '--outfile', executable)
    assert subprocess.check_output([executable, 'compiled'], text=True) == 'compiled\n'
    before = executable.read_bytes()
    hello.write_text('def main()\nputs(1 + true)\nend\n')
    run('build', hello, '--compile', '--outfile', executable, success=False)
    assert executable.read_bytes() == before, 'failed build replaced an existing executable'
    hello.write_text('def main()\nputs("unsupported: é")\nend\n')
    assert 'TRBN' in run('build', hello, '--compile', success=False)
    hello.write_text('def main()\nputs("program ready")\nwhile true\nend\nend\n')
    child = subprocess.Popen([str(binary), 'run', str(hello)], cwd=root, env=env,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        assert select.select([child.stdout], [], [], 20)[0], 'program did not start'
        assert child.stdout.readline() == 'program ready\n'
        child.send_signal(signal.SIGINT)
        stdout, stderr = child.communicate(timeout=10)
        assert child.returncode == 130, (child.returncode, stdout, stderr)
    finally:
        if child.poll() is None:
            child.kill()
            child.communicate()

    assert run('run', cwd=repository) == 'Hello from TypeRB Native!\n'
    project = root / 'project'
    (project / 'src/nested').mkdir(parents=True)
    (project / 'src/main.trb').write_text('def answer(): Integer\nreturn 42\nend\ndef main()\nputs("project")\nend\n')
    config = project / 'trbconfig.jsonc'
    config.write_text('{"name":"demo","sourceDir":"src"}')
    assert run('run', cwd=project / 'src/nested') == 'project\n'
    assert '42 : Integer' in run('repl', text='answer()\n:quit\n', cwd=project)
    (project / 'src/model.trb').write_text('record Box\nvalue: Integer\nend\n')
    records = run('repl', text='mut box := Box.new(value: 3)\nrecord Point\nx: Integer\ny: Integer\nend\nbox\n:type box\nbox.value\n:quit\n', cwd=project)
    assert records.count('Box(value: 3) : Box') == 2, records
    assert 'Box\n3 : Integer' in records, records

    # Imported record aliases retain declaration identity inside Array types.
    record_project = root / 'record-arrays'
    record_project.mkdir()
    (record_project / 'model.trb').write_text(
        'record Entry\nid: Integer\nend\ndef entries(): Array<Entry>\n'
        'return [Entry.new(id: 3)]\nend\n')
    record_entry = record_project / 'main.trb'
    record_entry.write_text(
        'import { Entry as Item, entries } from model\n'
        'def read(values: Array<Item>): Integer\nreturn values[0].id\nend\n'
        'def main()\nmut values: Array<Item> := entries()\n'
        'values.push(Item.new(id: 4))\nputs(read(values))\nputs(values[1].id)\nend\n')
    assert run('check', record_entry) == 'ok\n'
    assert run('run', record_entry) == '3\n4\n'
    record_entry.write_text(
        'import { entries } from model\nrecord Entry\nid: Integer\nend\n'
        'def consume(values: Array<Entry>)\nputs(values.size())\nend\n'
        'def main()\nconsume(entries())\nend\n')
    assert 'TRBN4004' in run('check', record_entry, success=False)
    record_entry.write_text(record_entry.read_text().replace(
        'record Entry', 'record OtherEntry').replace('Array<Entry>', 'Array<OtherEntry>'))
    assert 'TRBN4004' in run('check', record_entry, success=False)

    assert 'override' in run('check', '--mode', 'trb', cwd=project, success=False)
    config.write_text('{"name":"demo","mode":"go","sourceDir":"src","go":{"module":"example.com/demo"}}')
    assert 'not implemented' in run('run', cwd=project, success=False)
    assert '42 : Integer' in run('repl', '--mode=trb', text='answer()\n:quit\n', cwd=project)
    run('run', 'missing.trb', cwd=project, success=False)
    assert 'ASCII String literals only' in run('repl', text='"é"\n:quit\n')
    logical = run('repl', text='''def mark(value: Boolean): Boolean
puts("visited")
return value
end
true || mark(false)
false && mark(true)
false || mark(true) && !false
true || 1 / 0 == 0
false && (true || 1 / 0 == 0)
false == 1 < 2 || 3 > 2 == true
:exit
''')
    assert logical.count('visited') == 1, logical
    assert logical.count('true : Boolean') == 4, logical
    assert logical.count('false : Boolean') == 2, logical
    assert 'panic:' not in logical, logical
    unary = run('repl', text='-1 + 2\n-1 * 2 + 3\n-(1 + 2)\n!true && false || true\n:quit\n')
    assert unary == '1 : Integer\n1 : Integer\n-3 : Integer\ntrue : Boolean\n', unary
    required_rhs = run('repl', text='false || 1 / 0 == 0\n:q\n')
    assert 'division by zero' in required_rhs, required_rhs
    (root / 'helpers.trb').write_text('# A declaration file\ndef loaded(): Integer\nreturn 8\nend\n')
    assert '8 : Integer' in run('repl', text=':load helpers.trb\nloaded()\n:quit\n')
    replay = run('repl', text='mut n := 1\nn += 2\nputs("replay marker")\n:reload\nn\n:load helpers.trb\nn + loaded()\n:q\n')
    assert replay.count('replay marker') == 3, replay
    assert 'reloaded' in replay and '11 : Integer' in replay, replay
    (root / 'invalid.trb').write_text('1 + "bad"\n')
    rejected = run('repl', text='puts("do not replay")\n:load invalid.trb\n:q\n')
    assert rejected.count('do not replay') == 1, rejected


    output = run('repl', text='''mut total := 2
puts("once")
:type puts("must not print")
total += 3
total
:type total + 1
mut xs := [1, 2]
mut ys := xs
ys.push(3)
xs[0] = 9
ys
xs[99]
ys
1 + "bad"
1 + 2
"invalid".to_i()
"+12".to_i()
"9007199254740992".to_i()
[1, 2.5]
9007199254740991 + 1
10 / 0
def sum(xs: Array<Integer>): Integer
mut i := 0
mut n := 0
while i < xs.size()
n += xs[i]
i += 1
end
return n
end
sum(xs)
record Pair
left: Integer
right: Integer
end
mut pair := Pair.new(left: 2, right: 4)
pair.left = 7
pair
pair = Pair.new(left: 7, right: 4)
pair
:quit
''')
    for expected in ['5 : Integer', 'Integer\n', '[9, 2, 3]', 'out of bounds',
                     '3 : Integer', 'invalid Integer', '12 : Integer',
                     'outside the portable range', '[1, 2.5] : Array<Float>',
                     'division by zero', '14 : Integer', 'record field is readonly',
                     'left: 2, right: 4', 'left: 7, right: 4']:
        assert expected in output, (expected, output)
    assert output.count('once') == 1, output
    assert 'must not print' not in output, output
    assert output.count('[9, 2, 3]') >= 2, output

    # A controlling terminal exercises native editing, tab completion, history and SIGINT.
    pid, descriptor = pty.fork()
    if pid == 0:
        os.chdir(root)
        os.execve(binary, [str(binary)], env)
    pending = b''

    def expect(needle, timeout=15):
        global pending
        end = time.monotonic() + timeout
        target = needle.encode()
        while target not in pending:
            assert time.monotonic() < end, (needle, pending.decode(errors='replace'))
            if select.select([descriptor], [], [], 0.2)[0]:
                try:
                    part = os.read(descriptor, 65536)
                except OSError as error:
                    if error.errno == errno.EIO:
                        part = b''
                    else:
                        raise
                assert part, ('terminal exited', pending)
                pending += part
        before, pending = pending.split(target, 1)
        return before.decode(errors='replace')

    def send(text):
        os.write(descriptor, text.encode())

    try:
        expect('trbn:trb> ')
        send('mut apples := 4\n')
        expect('4 : Integer')
        expect('trbn:trb> ')
        send('app\t\n')
        expect('4 : Integer')
        expect('trbn:trb> ')
        send('\x1b[A\n')
        expect('4 : Integer')
        expect('trbn:trb> ')
        send('if true\n')
        expect('...> ')
        send('puts("loop started")\nwhile true\nend\nend\n')
        expect('loop started\r\n')
        send('\x03')
        expect('Interrupted')
        expect('trbn:trb> ')
        send('apples\n')
        expect('4 : Integer')
        expect('trbn:trb> ')
        send('apples +')
        expect('apples +')
        send('\x03')
        expect('trbn:trb> ')
        send('apples\n')
        expect('4 : Integer')
        expect('trbn:trb> ')
        send(':quit\n')
        deadline = time.monotonic() + 10
        while True:
            waited, status = os.waitpid(pid, os.WNOHANG)
            if waited:
                assert os.waitstatus_to_exitcode(status) == 0
                pid = 0
                break
            if select.select([descriptor], [], [], 0)[0]:
                try:
                    pending += os.read(descriptor, 65536)
                except OSError as error:
                    if error.errno != errno.EIO:
                        raise
            assert time.monotonic() < deadline, ('REPL did not exit', pending)
            time.sleep(0.02)
    finally:
        os.close(descriptor)
        if pid:
            os.kill(pid, signal.SIGKILL)
            os.waitpid(pid, 0)
    history = json.loads((root / 'history.json').read_text())
    assert 'mut apples := 4' in history
    assert 'if true\n  puts("loop started")\n  while true\n  end\nend' in history

print('Native CLI, project configuration, REPL and terminal tests passed')
