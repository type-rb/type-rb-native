#!/usr/bin/env python3
"""Check byte-preserving join, bounded allocation and retained operands."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('binary', type=Path)
binary = parser.parse_args().binary.resolve()
repository = Path(__file__).resolve().parent.parent

with tempfile.TemporaryDirectory(prefix='native-array-join-') as temporary:
    root = Path(temporary)
    env = dict(os.environ, NO_COLOR='1', TERM='dumb', TRBN_HISTORY=str(root / 'history'))

    def run(command, *, data=None, stats=False, code=0):
        environment = dict(env, TYPE_RB_NATIVE_RUNTIME_STATS='1') if stats else env
        result = subprocess.run(list(map(str, command)), input=data, cwd=root,
                                env=environment, text=True, capture_output=True, timeout=60)
        assert result.returncode == code, (command, result.stdout, result.stderr)
        return result

    def compile_il(text):
        il, assembly, program = [root / name for name in ('program.ssa', 'program.s', 'program')]
        il.write_text(text)
        run([binary.with_name('qbe'), '-o', assembly, il])
        run(['/usr/bin/cc', assembly, '-lm', '-o', program])
        return program

    def statistics(result):
        values = {}
        for line in result.stderr.splitlines():
            prefix, key, value = line.split(',')
            assert prefix == 'type-rb-native-gc-stat-v1' and key not in values, line
            values[key] = int(value)
        assert values['live-bytes'] == 0, values
        assert values['allocated-bytes'] == values['reclaimed-bytes'], values
        return values

    fixture = repository / 'compiler/conformance/valid/array-join-managed-mir'
    body = fixture.with_suffix('.trb').read_text().replace('def main()', 'def exercise()')
    body = body.replace('"a" + "b"', '"こんに" + "ちは"')
    body = body.replace('"c" + "d"', '"A" + "\\x00B"')
    source = root / 'main.trb'
    source.write_text(body + '\ndef main()\n(0...20).each { |_index| exercise() }\nend\n')
    emitted = run([binary, '--internal-driver', 'emit-qbe', source])
    marker = ' %result =l call $trbn_string_alloc(l %payload)'
    start = emitted.stdout.index('function l $trbn_array_join(')
    end = emitted.stdout.index('\n}', start) + 2
    runtime = emitted.stdout[start:end]
    assert runtime.count(marker) == 1
    # Collect after sizing, immediately before allocation, with both operands
    # dead after the join at some call sites. Their MIR roots must still hold.
    forced = runtime.replace(marker, ' call $trbn_gc_collect(w 0)\n' + marker)
    program = compile_il(emitted.stdout[:start] + forced + emitted.stdout[end:])
    result = run([program], stats=True)
    expected = fixture.with_suffix('.out').read_text().replace('ab', 'こんにちは').replace('cd', 'A\0B')
    assert result.stdout == expected * 20, result
    measured = statistics(result)
    assert measured['collections'] >= 300, measured
    assert measured['peak-heap-bytes'] < 4 * 1024 * 1024, measured

    # Bound total copying/allocation without a wall-clock performance assertion.
    source.write_text('''def main()
mut values: Array<String> := []
(0...4096).each { |_index| values.push("abcd") }
puts(values.join("/").size())
end
''')
    emitted = run([binary, '--internal-driver', 'emit-qbe', source])
    result = run([compile_il(emitted.stdout)], stats=True)
    assert result.stdout == '20479\n', result
    assert statistics(result)['allocated-bytes'] < 512 * 1024, result.stderr

    # A reduced test-only capacity exercises both overflow exits before copy.
    for expression in ('["aaaa", "bbb"].join("")', '["aa", "bb"].join("---")'):
        source.write_text('def main()\nputs(' + expression + ')\nend\n')
        emitted = run([binary, '--internal-driver', 'emit-qbe', source])
        start = emitted.stdout.index('function l $trbn_array_join(')
        end = emitted.stdout.index('\n}', start) + 2
        runtime = emitted.stdout[start:end]
        assert runtime.count('sub 9007199254740991,') == 2
        limited = runtime.replace('sub 9007199254740991,', 'sub 6,')
        program = compile_il(emitted.stdout[:start] + limited + emitted.stdout[end:])
        failed = run([program], code=2)
        assert failed.stdout == '' and failed.stderr == 'panic: allocation failed\n', failed

    retained = run([binary, 'repl'], data='''mut words := ["こんにちは", "😀"]
def separator(): String
return "/"
end
joined := words.join(separator())
words[0] = "changed"
puts(joined)
words.join(1)
puts(words.join("|"))
:quit
''')
    assert 'こんにちは/😀\n' in retained.stdout, retained
    assert retained.stdout.endswith('changed|😀\n'), retained
    assert len(retained.stderr.splitlines()) == 1 and 'error[' in retained.stderr, retained

print('Array join byte, GC, allocation and retained REPL checks passed')
