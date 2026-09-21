#!/usr/bin/env python3
"""Verify String transform bytes, Unicode lookup, retained roots and allocation."""
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile

binary = Path(sys.argv[1]).resolve()
repository = Path(__file__).resolve().parent.parent

with tempfile.TemporaryDirectory(prefix='native-string-transforms-') as temporary:
    root = Path(temporary)
    env = dict(os.environ, NO_COLOR='1', TERM='dumb', TRBN_HISTORY=str(root / 'history'))

    def run(command, *, data=None, stats=False):
        environment = dict(env, TYPE_RB_NATIVE_RUNTIME_STATS='1') if stats else env
        result = subprocess.run([item if isinstance(item, bytes) else str(item) for item in command],
                                cwd=root, env=environment, input=data, capture_output=True, timeout=90)
        assert result.returncode == 0, (command, result.stdout, result.stderr)
        return result

    def emit(source):
        (root / 'main.trb').write_text(source)
        result = run([binary, '--internal-driver', 'emit-qbe', root / 'main.trb'])
        assert result.stderr == b'', result.stderr
        return result.stdout

    def assemble(il):
        (root / 'program.ssa').write_bytes(il)
        run([binary.with_name('qbe'), '-o', root / 'program.s', root / 'program.ssa'])
        run(['/usr/bin/cc', root / 'program.s', '-lm', '-o', root / 'program'])
        return root / 'program'

    def compile_source(source):
        il = emit(source)
        for symbol, markers in (
            (b'trbn_string_split', (b' %text =l call $trbn_string_from_bytes(', b' call $trbn_array_push_paced(')),
            (b'trbn_string_replace', (b' %result =l call $trbn_string_alloc(',)),
            (b'trbn_string_case', (b' %result =l call $trbn_string_alloc(',)),
        ):
            start = il.index(b'function l $' + symbol + b'(')
            end = il.index(b'\n}', start) + 2
            body = il[start:end]
            for marker in markers:
                assert body.count(marker) == 1, (symbol, marker)
                body = body.replace(marker, b' call $trbn_gc_collect(w 0)\n' + marker)
            il = il[:start] + body + il[end:]
        return assemble(il)

    def statistics(result):
        values = {}
        for line in result.stderr.decode().splitlines():
            prefix, key, value = line.split(',')
            assert prefix == 'type-rb-native-gc-stat-v1' and key not in values, line
            values[key] = int(value)
        assert values['live-bytes'] == 0, values
        assert values['allocated-bytes'] == values['reclaimed-bytes'], values
        return values

    # Go's complete mapping tables are independently regenerated in quick CI.
    # Compare the actual QBE binary-search implementation at every code point.
    maps = {}
    for line in (repository / 'compiler/src/unicode_case_data.trb').read_text().splitlines():
        if '\tqbe_output_line(output, ' not in line:
            continue
        declaration = json.loads(line.split('output, ', 1)[1][:-1])
        name = re.search(r'data \$trbn_case_(upper|lower) =', declaration)[1]
        maps[name] = {int(a): int(b) for a, b in re.findall(r'w (\d+), w (\d+)', declaration)}
    expected = hashlib.sha256()
    for point in range(0x110000):
        expected.update(struct.pack('<II', maps['upper'].get(point, point), maps['lower'].get(point, point)))
    il = emit('def main()\nend\n')
    il, renamed = re.subn(rb'(export function w \$)main\(', rb'\1checked_main(', il)
    assert renamed == 1
    il += b'''
export function w $main() {
@start
 %buffer =l call $calloc(l 1114112, l 8)
 jmp @loop
@loop
 %point =l phi @start 0, @write %next
 %done =w ceql %point, 1114112
 jnz %done, @finish, @write
@write
 %upper =l call $trbn_case_point(l %point, l 0)
 %lower =l call $trbn_case_point(l %point, l 1)
 %offset =l mul %point, 8
 %first =l add %buffer, %offset
 %second =l add %first, 4
 storew %upper, %first
 storew %lower, %second
 %next =l add %point, 1
 jmp @loop
@finish
 %written =l call $write(w 1, l %buffer, l 8912896)
 call $free(l %buffer)
 ret 0
}
'''
    result = run([assemble(il)])
    assert len(result.stdout) == 8912896 and not result.stderr, result.stderr
    assert hashlib.sha256(result.stdout).digest() == expected.digest()

    # Check managed inputs at each allocation and append, including byte-width
    # changes and UTF-8 sequences formed across replacement boundaries.
    program = compile_source('''import trb/std/process
def main()
args := Process.argv()
text := args[0]
pattern := args[1]
replacement := args[2]
puts(text.split(pattern).join("/"))
puts(text.replace_all(pattern, replacement))
puts(text.upcase())
puts(text.downcase())
end
''')
    for text, pattern, replacement, expected_output in (
        ('日本😀a😀'.encode(), '😀'.encode(), 'İ'.encode(), '日本/a/\n日本İaİ\n日本😀A😀\n日本😀a😀\n'.encode()),
        (b'\xffA\xffB', b'\xff', b'Z', b'/A/B\nZAZB\n' + '�A�B\n�a�b\n'.encode()),
        ('ȺıſK'.encode(), 'ı'.encode(), b'', 'Ⱥ/ſK\nȺſK\nȺISK\nⱥıſk\n'.encode()),
        (b'\xc2X\xa0', b'X', b'', b'\xc2/\xa0\n\xc2\xa0\n' + '�X�\n�x�\n'.encode()),
    ):
        result = run([program, text, pattern, replacement], stats=True)
        assert result.stdout == expected_output, result
        assert statistics(result)['collections'] >= 5

    program = compile_source('''def main()
text := "a\\x00b\\x00"
puts(text.split("\\x00").join("/"))
puts(text.replace_all("\\x00", "😀").size())
puts(text.replace_all("b", "\\x00").upcase())
end
''')
    result = run([program], stats=True)
    assert result.stdout == b'a/b/\n4\nA\x00\x00\x00\n', result
    statistics(result)

    program = compile_source('''import trb/std/process
def main()
text := Process.argv()[0]
parts := text.split(":")
puts(parts.size())
puts(parts.join(":") == text)
puts(text.replace_all(":", "日本").size())
puts(text.upcase().downcase() == text)
end
''')
    large = 'word:' * 2048
    result = run([program, large], stats=True)
    assert result.stdout == b'2049\ntrue\n12288\ntrue\n', result
    measured = statistics(result)
    assert measured['collections'] >= 4096 and measured['peak-heap-bytes'] < 2 * 1024 * 1024, measured
    assert measured['allocated-bytes'] < 1024 * 1024, measured

    retained = run([binary, 'repl'], data='''mut source := "a😀b😀"
parts := source.split("😀")
saved := source.replace_all("😀", "日本").upcase()
source = "changed"
record Later
value: String
end
puts(parts.join("/"))
puts(saved)
source.split("")
source.replace_all("", "x")
puts(saved.downcase())
:quit
'''.encode())
    assert 'a/b/\nA日本B日本\n'.encode() in retained.stdout, retained
    assert retained.stdout.endswith('a日本b日本\n'.encode()), retained
    assert len(retained.stderr.splitlines()) == 2, retained
    assert b'String split separator is empty' in retained.stderr, retained
    assert b'String replacement pattern is empty' in retained.stderr, retained

print('String transform Unicode, byte, lifetime, allocation and retained REPL checks passed')
