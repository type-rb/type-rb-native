#!/usr/bin/env python3
"""Exercise concrete object methods through Native code and retained REPL values."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

binary = Path(sys.argv[1]).resolve()
repository = Path(__file__).resolve().parent.parent

with tempfile.TemporaryDirectory(prefix='native-object-methods-') as temporary:
    root = Path(temporary)
    environment = dict(os.environ, NO_COLOR='1', TERM='dumb',
                       TRBN_HISTORY=str(root / 'history'))

    def run(command, *, data=None, stats=False):
        env = dict(environment, TYPE_RB_NATIVE_RUNTIME_STATS='1') if stats else environment
        result = subprocess.run(list(map(str, command)), input=data, cwd=root,
                                env=env, capture_output=True, text=True, timeout=60)
        assert result.returncode == 0, (command, result.stdout, result.stderr)
        return result

    for name in ('object-class-static-method', 'object-class-generic-instance-method'):
        fixture = repository / 'compiler/conformance/valid' / name
        source = root / 'main.trb'
        source.write_text(fixture.with_suffix('.trb').read_text())
        checked = run([binary, '--internal-driver', 'check', source])
        assert not checked.stderr, checked
        emitted = run([binary, '--internal-driver', 'emit-qbe', source])
        assert not emitted.stderr, emitted
        forced, ordinary, hooks = [], False, 0
        for line in emitted.stdout.splitlines():
            if line.startswith('function '):
                ordinary = '$trbnf' in line
            if line == '}':
                ordinary = False
            if ordinary and ('call $trbn_gc_alloc(' in line or 'call $trbnf' in line):
                forced.append('\tcall $trbn_gc_collect(w 0)')
                hooks += 1
            forced.append(line)
        assert hooks > 0
        il, assembly, program = [root / item for item in ('program.ssa', 'program.s', 'program')]
        il.write_text('\n'.join(forced) + '\n')
        run([binary.with_name('qbe'), '-o', assembly, il])
        run(['/usr/bin/cc', assembly, '-lm', '-o', program])
        result = run([program], stats=True)
        assert result.stdout == fixture.with_suffix('.out').read_text(), result
        statistics = {}
        for line in result.stderr.splitlines():
            prefix, key, value = line.split(',')
            assert prefix == 'type-rb-native-gc-stat-v1' and key not in statistics, line
            statistics[key] = int(value)
        assert statistics['live-bytes'] == 0, statistics
        assert statistics['allocated-bytes'] == statistics['reclaimed-bytes'], statistics

    retained = run([binary, 'repl'], data='''interface Source<T>
def get(): T
end
class Box<T>
def identity<U>(value: U): U
return value
end
def value(input: T): T
return input
end
def read(): Integer
return 42
end
end
mut saved := Box<Integer>.new()
read := fn(): Integer; return saved.read(); end
puts(saved.identity<String>("held"))
class Earlier
end
:type saved
puts(saved.value(7))
puts(read())
:reload
puts(saved.value(9))
puts(read())
:quit
''')
    assert not retained.stderr, retained
    assert retained.stdout == (
        '#<Box > : Box<Integer> [mut]\n#<fn> : () -> Integer\n'
        'held\nBox<Integer>\n7\n42\nheld\n7\n42\nreloaded\n9\n42\n'), retained

    initialized = run([binary, 'repl'], data='''class Answer
def initialize(*, marker: Integer = 7)
puts(marker)
end
def self.make(): Answer
return Answer.new(marker: 9)
end
def value(*, extra: Integer = 2): Integer
return 40 + extra
end
end
item := Answer.new()
class Later
end
puts(item.value())
puts(Answer.make().value(extra: 3))
:quit
''')
    assert not initialized.stderr, initialized
    assert initialized.stdout == '7\n#<Answer > : Answer\n42\n9\n43\n', initialized

    (root / 'src').mkdir()
    (root / 'trbconfig.jsonc').write_text('{"name":"objects","sourceDir":"src"}')
    (root / 'src/helper.trb').write_text(
        'class Helper\ndef value(): Integer\nreturn 17\nend\nend\n')
    imported = run([binary, 'repl'], data='value := Helper.new()\nputs(value.value())\n:reload\nputs(value.value())\n:quit\n')
    assert not imported.stderr, imported
    assert imported.stdout == '#<Helper > : Helper\n17\n17\nreloaded\n17\n', imported

print('Native object methods, forced collection, retained identities and replay passed')
