#!/usr/bin/env python3
"""Check stable natural Array ordering, retained copies and managed lifetime."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('binary', type=Path)
binary = parser.parse_args().binary.resolve()
repository = Path(__file__).resolve().parent.parent

with tempfile.TemporaryDirectory(prefix='native-array-sorting-') as temporary:
    root = Path(temporary)
    env = dict(os.environ, NO_COLOR='1', TERM='dumb', TRBN_HISTORY=str(root / 'history'))

    def run(command, *, data=None, stats=False):
        environment = dict(env, TYPE_RB_NATIVE_RUNTIME_STATS='1') if stats else env
        result = subprocess.run(list(map(str, command)), input=data, cwd=root,
                                env=environment, text=True, capture_output=True, timeout=60)
        assert result.returncode == 0, (command, result.stdout, result.stderr)
        return result

    # The CLI is built by the current compiler. Include literal byte cases that
    # the preceding seed's recovery source does not itself construct.
    fixture = repository / 'compiler/conformance/valid/array-sorting-managed-mir'
    body = fixture.with_suffix('.trb').read_text().replace('def main()', 'def exercise()')
    body = body.replace('"a"\n', '"日"\n', 1).replace('part + "b"', 'part + "本"')
    body = body.replace('"aa"', '"a\\x00"').replace('"zz"', '"😀"').replace('"x"', '"é"')
    source = root / 'main.trb'
    source.write_text(body + '\ndef main()\n(0...30).each { |_index| exercise() }\nend\n')
    expected = ('|a|a|a\0|z|é|日本|😀\n日本\ntrue\n'
                '😀|日本|é|z|changed|a\0|a|a\n😀\ntrue\na\n') * 30
    emitted = run([binary, '--internal-driver', 'emit-qbe', source])
    assert emitted.stderr == '', emitted
    forced, ordinary, hooks = [], False, 0
    for line in emitted.stdout.splitlines():
        if line.startswith('function '):
            ordinary = '$trbnf' in line
        if line == '}':
            ordinary = False
        if ordinary and any(marker in line for marker in (
                'call $trbn_array_new(', 'call $trbn_array_push_', 'call $trbn_array_copy(',
                'call $trbn_gc_alloc(', 'call $trbn_string_concat(', 'call $trbn_array_join(')):
            forced.append('\tcall $trbn_gc_collect(w 0)')
            hooks += 1
        forced.append(line)
    assert hooks >= 16, hooks
    il, assembly, program = [root / name for name in ('program.ssa', 'program.s', 'program')]
    il.write_text('\n'.join(forced) + '\n')
    run([binary.with_name('qbe'), '-o', assembly, il])
    run(['/usr/bin/cc', assembly, '-lm', '-o', program])
    result = run([program], stats=True)
    assert result.stdout == expected, (result.stdout, expected, result.stderr)
    statistics = {}
    for line in result.stderr.splitlines():
        prefix, key, value = line.split(',')
        assert prefix == 'type-rb-native-gc-stat-v1' and key not in statistics, line
        statistics[key] = int(value)
    assert statistics['collections'] >= 480, statistics
    assert statistics['live-bytes'] == 0, statistics
    assert statistics['allocated-bytes'] == statistics['reclaimed-bytes'], statistics
    assert statistics['peak-heap-bytes'] < 4 * 1024 * 1024, statistics

    # Odd tails, repeated keys, empty runs and power-of-two boundaries use an
    # independent host oracle. A single authored sort body covers every length.
    source.write_text('''def main()
(0...68).each do |size|
mut values: Array<Integer> := []
(0...size).each { |index| values.push((index * 37 + size * 11) % 23 - 11) }
values.sort().each { |value| puts(value) }
values.sort_descending().each { |value| puts(value) }
puts(values.size())
end
end
''')
    result = run([binary, 'run', source])
    expected = []
    for size in range(68):
        values = [(index * 37 + size * 11) % 23 - 11 for index in range(size)]
        expected.extend(map(str, sorted(values)))
        expected.extend(map(str, sorted(values, reverse=True)))
        expected.append(str(size))
    assert result.stdout == '\n'.join(expected) + '\n' and result.stderr == '', result

    # A rejected call preserves retained source/copy storage. Replay rebuilds
    # those same independent bindings and nominal declarations cannot disturb it.
    retained = run([binary, 'repl'], data='''mut values := [3, 1, 2]
mut ordered := values.sort()
values[0] = 7
ordered[0] = 8
values.sort(1)
record Before
text: String
end
:type ordered
puts(values[0])
puts(ordered[0])
puts(values.sort()[0])
:reload
puts(values[0])
puts(ordered[0])
puts(ordered.sort_descending()[0])
:quit
''')
    assert retained.stdout == ('[3, 1, 2] : Array<Integer> [mut]\n'
                               '[1, 2, 3] : Array<Integer> [mut]\n'
                               '7 : Integer\n8 : Integer\nArray<Integer>\n7\n8\n1\n'
                               '7\n8\n1\nreloaded\n7\n8\n8\n'), retained
    assert len(retained.stderr.splitlines()) == 1 and 'argument count' in retained.stderr, retained

print('Array sorting CLI, replay, ordering and collection checks passed')
