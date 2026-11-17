#!/usr/bin/env python3
"""Check Array insertion/removal lifetimes and retained REPL identities."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile
import sys

parser = argparse.ArgumentParser()
parser.add_argument('binary', type=Path)
binary = parser.parse_args().binary.resolve()
repository = Path(__file__).resolve().parent.parent

with tempfile.TemporaryDirectory(prefix='native-array-mutation-') as temporary:
    root = Path(temporary)
    env = dict(os.environ, NO_COLOR='1', TERM='dumb', TRBN_HISTORY=str(root / 'history'))

    def run(command, *, data=None, stats=False):
        environment = dict(env, TYPE_RB_NATIVE_RUNTIME_STATS='1') if stats else env
        result = subprocess.run(list(map(str, command)), input=data, cwd=root,
                                env=environment, text=True, capture_output=True, timeout=60)
        assert result.returncode == 0, (command, result.stdout, result.stderr)
        return result

    fixture = repository / 'compiler/conformance/valid/array-mutation-managed-mir'
    source = root / 'main.trb'
    source.write_text(fixture.with_suffix('.trb').read_text().replace('def main()', 'def exercise()') +
                      '\ndef main()\n(0...30).each { |_index| exercise() }\nend\n')
    emitted = run([binary, '--internal-driver', 'emit-qbe', source])
    assert emitted.stderr == '', emitted
    # Collection at the insertion runtime's growth boundary must see both the
    # retained owner and its managed element, including captured callbacks.
    marker = ' call $trbn_array_push_paced(l %array, l %value)'
    assert emitted.stdout.count(marker) == 1
    forced = emitted.stdout.replace(marker, ' call $trbn_gc_collect(w 0)\n' + marker)
    il, assembly, program = [root / name for name in ('program.ssa', 'program.s', 'program')]
    il.write_text(forced)
    run([binary.with_name('qbe'), '-o', assembly, il])
    run(['/usr/bin/cc', assembly, '-lm', '-o', program])
    result = run([program], stats=True)
    assert result.stdout == fixture.with_suffix('.out').read_text() * 30, result
    statistics = {}
    for line in result.stderr.splitlines():
        prefix, key, value = line.split(',')
        assert prefix == 'type-rb-native-gc-stat-v1' and key not in statistics, line
        statistics[key] = int(value)
    assert statistics['collections'] >= 600, statistics
    assert statistics['live-bytes'] == 0, statistics
    assert statistics['allocated-bytes'] == statistics['reclaimed-bytes'], statistics
    assert statistics['peak-heap-bytes'] < 4 * 1024 * 1024, statistics

    # The same retained pool identity is visible through an immutable alias
    # across submissions and after a failing final assignment bounds check.
    repl = run([binary, 'repl'], data='''mut values := [1, 2]
view := values
values.unshift(0)
values.pop()
view
def remove(mut items: Array<Integer>): Integer
items.pop()
return 9
end
values[-1] = remove(values)
puts(view.size())
puts(view[0])
values.unshift(7)
puts(view[0])
:quit
''')
    assert repl.stdout == ('[1, 2] : Array<Integer> [mut]\n'
                           '[1, 2] : Array<Integer>\n'
                           '2 : Integer\n[0, 1] : Array<Integer>\n1\n0\n7\n'), repl
    assert len(repl.stderr.splitlines()) == 1 and 'index is out of bounds' in repl.stderr, repl


    # Exercise logical windows through the ordinary CLI and the same runtime
    # under forced allocation-boundary collections. Shift itself cannot collect.
    window = repository / 'compiler/conformance/valid/array-window-mir'
    source.write_text(window.with_suffix('.trb').read_text())
    expected = window.with_suffix('.out').read_text()
    assert run([binary, 'check', source]).stdout == 'ok\n'
    run([binary, 'build', '--compile', '--outfile', program, source])
    assert run([program], stats=True).stdout == expected
    emitted = run([binary, '--internal-driver', 'emit-qbe', source])
    forced = emitted.stdout.replace('call $trbn_gc_maybe_collect(l %projected)',
                                    'call $trbn_gc_collect(w 0)')
    forced = forced.replace('call $trbn_gc_maybe_collect(l %growth)',
                            'call $trbn_gc_collect(w 0)')
    assert forced != emitted.stdout
    il.write_text(forced)
    run([binary.with_name('qbe'), '-o', assembly, il])
    run(['/usr/bin/cc', assembly, '-lm', '-o', program])
    result = run([program], stats=True)
    assert result.stdout == expected, result
    statistics = {line.split(',')[1]: int(line.split(',')[2])
                  for line in result.stderr.splitlines()}
    assert statistics['live-bytes'] == 0, statistics
    assert statistics['allocated-bytes'] == statistics['reclaimed-bytes'], statistics
    assert statistics['collections'] > 100, statistics

    repl = run([binary, 'repl'], data='mut queue := [1, 2, 3, 4]\nview := queue\nqueue.shift()\nqueue.push(5)\nqueue.unshift(0)\nputs(view[0])\nputs(view[-1])\nputs(queue.shift())\nputs(queue.shift())\nputs(view[0])\n:quit\n')
    assert repl.stdout == ('[1, 2, 3, 4] : Array<Integer> [mut]\n'
                           '[1, 2, 3, 4] : Array<Integer>\n'
                           '1 : Integer\n0\n5\n0\n2\n3\n'), repl
    assert repl.stderr == '', repl

print('Array mutation GC and retained REPL checks passed')

subprocess.run([sys.executable, str(repository / "tools/native-array-window-test.py"), str(binary)], check=True)
