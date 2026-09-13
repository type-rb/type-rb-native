#!/usr/bin/env python3
"""Exercise ordinary UTF-8 input, output and managed lifetimes, including GC."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('binary', type=Path)
args = parser.parse_args()
binary = args.binary.resolve()
qbe = binary.with_name('qbe')

with tempfile.TemporaryDirectory(prefix='native UTF-8 日本語 ') as directory:
    root = Path(directory)
    env = dict(os.environ, NO_COLOR='1', TERM='dumb', TRBN_HISTORY=str(root / 'history.json'))

    def run(command, *, data=None, success=True):
        result = subprocess.run([item if isinstance(item, bytes) else str(item) for item in command], input=data, capture_output=True,
                                cwd=root, env=env, timeout=30)
        assert (result.returncode == 0) == success, (command, result)
        return result

    def compile_source(text, expected, *, force_gc=False, arguments=()):
        source = root / 'main.trb'
        source.write_text(text)
        result = run([binary, 'check', source])
        assert result.stdout == b'ok\n' and result.stderr == b'', result
        output = root / 'program'
        if force_gc:
            emitted = run([binary, '--internal-driver', 'emit-qbe', source])
            assert emitted.stderr == b'', emitted
            marker = b'\t%result =l call $trbn_gc_alloc(l $trbn_desc_string, l %size, l 0)'
            assert emitted.stdout.count(marker) == 1
            il = emitted.stdout.replace(marker, b'\tcall $trbn_gc_collect(w 0)\n' + marker)
            (root / 'program.ssa').write_bytes(il)
            run([qbe, '-o', root / 'program.s', root / 'program.ssa'])
            run(['/usr/bin/cc', root / 'program.s', '-lm', '-o', output])
        else:
            result = run([binary, 'build', '--compile', '--outfile', output, source])
            assert result.stdout == result.stderr == b'', result
        result = run([output, *arguments])
        assert result.stdout == expected and result.stderr == b'', result

    # Both MIR String functions and the nominal/Hash adapter must retain indexed
    # values and their owners when every String allocation collects the heap.
    compile_source('''record Box
text: String
end
def join(left: String, right: String): String
return left + right
end
def indexed(text: String): String
return join(text[1], text[-1])
end
def stored(): String
mut values := ["あ" + "😀"]
saved := values[0][0]
values[0] = "replacement"
mut table := {"日本" => Box.new(text: saved)}
table["日本語"] = Box.new(text: indexed("Aあ😀"))
return table["日本"].text + table["日本" + "語"].text
end
def main()
puts(stored())
puts(indexed("Aあ😀"))
end
''', 'ああ😀\nあ😀\n'.encode(), force_gc=True)

    # A real NUL in a literal must retain the full byte and code-point lengths.
    compile_source('def main()\ntext := "あ\0😀"\nputs(text)\nputs(text.size())\nputs(text[1])\nend\n',
                   'あ\0😀\n3\n\0\n'.encode())
    long = '日本語😀' * 90
    compile_source('def main()\ntext := "' + long + '"\nputs(text)\nputs(text.size())\nend\n',
                   (long + '\n360\n').encode())
    compile_source('''import trb/std/process
def main()
arguments := Process.argv()
puts(arguments[0])
puts(arguments[0].size())
puts(arguments[0][-1])
end
''', 'こんにちは😀\n6\n😀\n'.encode(), arguments=('こんにちは😀',))

    # External byte fragments can form one code point only after concatenation.
    compile_source('import trb/std/process\ndef main()\nargs := Process.argv()\nvalue := args[0] + args[1]\nputs(value)\nputs(value.size())\nputs(value[-1])\nend\n',
                   '¢\n1\n¢\n'.encode(), arguments=(b'\xc2', b'\xa2'))

    # Invalid source bytes must be rejected before token decoding can replace
    # them with U+FFFD. Valid U+FFFD remains an ordinary character.
    compile_source('def main()\nputs("�")\nend\n', '�\n'.encode())
    for malformed in (b'\xff', b'\xc0\xaf', b'\xe3\x81', b'\xed\xa0\x80', b'\xf4\x90\x80\x80'):
        (root / 'main.trb').write_bytes(b'def main()\nputs("' + malformed + b'")\nend\n')
        for command in ('check', 'build'):
            result = run([binary, command, root / 'main.trb'], success=False)
            assert result.stdout == b'' and b'source is not valid UTF-8' in result.stderr, result
        # Avoid loading the invalid project entry before the REPL submission.
        (root / 'main.trb').unlink()
        result = run([binary, 'repl'], data=b'"' + malformed + b'"\n:quit\n')
        assert result.stdout == b'' and b'source is not valid UTF-8' in result.stderr, result

print('UTF-8: literals, NUL, long data, argv, Hash/record lifetimes, forced GC and invalid source passed')
