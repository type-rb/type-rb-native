#!/usr/bin/env python3
"""Compare public diagnostic origins with the pinned reference renderer."""
import argparse
import os
from pathlib import Path
import re
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('binary', type=Path)
parser.add_argument('--reference', type=Path)
args = parser.parse_args()
binary = args.binary.resolve()
reference = args.reference.resolve() if args.reference else None


def run(tool, root, command, source=None):
    result = subprocess.run([str(tool), *map(str, command)], cwd=root,
                            input=source, text=True, capture_output=True,
                            env=dict(os.environ, NO_COLOR='1',
                                     TRBN_HISTORY=str(root / 'history')))
    assert '\x1b' not in result.stderr, result
    return result


def origin(text):
    # Native retains its own diagnoses and line-only source origins. Compare
    # actual paths, line numbers, severity and channel with the reference.
    match = re.fullmatch(r'(.+?):(\d+)(?::\d+)?: (error)(?:\[[A-Z0-9]+\])?: .+\n', text)
    assert match, text
    return match.groups()


with tempfile.TemporaryDirectory(prefix='native-diagnostics-') as temporary:
    root = Path(temporary).resolve()
    entry = root / 'main.trb'
    entry.write_text('def main()\n  missing\nend\n')
    expected = (str(entry), '2', 'error')
    for command in [('check', entry), ('build', entry, '--stdout'),
                    ('build', entry), ('build', entry, '--compile'), ('run', entry)]:
        result = run(binary, root, command)
        assert result.returncode == 1 and result.stdout == '', result
        assert origin(result.stderr) == expected, result
    if reference:
        result = run(reference, root, ('check', entry))
        assert result.returncode == 1 and origin(result.stderr) == expected, result
    assert not list(root.rglob('*.ssa')), list(root.rglob('*'))
    assert not (root / 'bin/main').exists()

    library = root / 'helper.trb'
    library.write_text('def answer(): Integer\n  return missing\nend\n')
    entry.write_text('import { answer } from helper\ndef main()\n  puts(answer())\nend\n')
    result = run(binary, root, ('check', entry))
    assert origin(result.stderr) == (str(library), '2', 'error'), result
    if reference:
        assert origin(run(reference, root, ('check', entry)).stderr) == origin(result.stderr)

    # Project mode and imported REPL modules must keep the real file origin.
    (root / 'trbconfig.jsonc').write_text('{"name":"diagnostics","mode":"trb","sourceDir":"."}')
    result = run(binary, root, ('check',))
    assert origin(result.stderr) == (str(library), '2', 'error'), result
    (root / 'trbconfig.jsonc').unlink()
    entry.unlink()
    result = run(binary, root, ('repl',), 'import { answer } from helper\n:quit\n')
    assert origin(result.stderr) == (str(library), '2', 'error'), result
    library.unlink()

    cases = [
        ('missing\n', [1]),
        ('1 + true\n', [1]),
        ('mut x := 1\nmissing\nmissing\n', [2, 2]),
        ('1\nmissing\n', [2]),
        ('def answer(): Integer\n  return true\nend\n', [2]),
        ('def answer(): Integer\n  return 1\nend\nmut x := 2\nmissing\n', [5]),
        ('mut x := 1\n1 / 0\nmissing\n', [2, 2]),
    ]
    for source, lines in cases:
        result = run(binary, root, ('repl',), source + ':quit\n')
        assert result.returncode == 0, result
        actual = [origin(line + '\n') for line in result.stderr.splitlines()]
        assert actual == [('(trb)', str(line), 'error') for line in lines], (source, result)
        if reference:
            baseline = run(reference, root, ('repl',), source + ':quit\n')
            assert actual == [origin(line + '\n') for line in baseline.stderr.splitlines()], baseline
        if '1 / 0' in source:
            assert '(trb):2: error: division by zero\n' in result.stderr, result
    loaded = root / 'session.trb'
    loaded.write_text('mut x := 1\ndef answer(): Integer\n  return true\nend\n')
    result = run(binary, root, ('repl',), f':load {loaded}\nputs(123)\n:quit\n')
    assert origin(result.stderr) == ('(trb)', '3', 'error'), result
    assert result.stdout == '123\n', result
    loaded.write_text('mut x := 1\ndef answer(): Integer\n  return 1\nend\nmissing\n')
    result = run(binary, root, ('repl',), f':load {loaded}\n:quit\n')
    assert origin(result.stderr) == ('(trb)', '5', 'error'), result

    # Rejected input never enters the session; recovery remains usable.
    result = run(binary, root, ('repl',), 'missing\nputs(123)\n:quit\n')
    assert result.stdout == '123\n' and len(result.stderr.splitlines()) == 1, result
print('Native file/project/REPL diagnostic origins and reference presentation passed')
