#!/usr/bin/env python3
"""Verify binary64 conversion boundaries and retained scalar conversion calls."""
import decimal
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile

binary = Path(sys.argv[1]).resolve()


def canonical(value):
    if math.isinf(value):
        return '-Infinity' if value < 0 else 'Infinity'
    if value == 0:
        return '0.0'
    # Python's shortest-roundtrip oracle is independent of the runtime's
    # precision search. Decimal expands its digits without rounding the value.
    text = format(decimal.Decimal(repr(value)), 'f')
    return text if '.' in text else text + '.0'


with tempfile.TemporaryDirectory(prefix='native-scalar-strings-') as temporary:
    root = Path(temporary)
    env = dict(os.environ, NO_COLOR='1', TERM='dumb', TRBN_HISTORY=str(root / 'history'))

    def run(*arguments, text=None):
        result = subprocess.run([str(binary), *map(str, arguments)], input=text,
                                cwd=root, env=env, capture_output=True, text=True,
                                timeout=180)
        assert result.returncode == 0 and not result.stderr, (result.returncode, result.stderr)
        return result.stdout

    # All binades, including subnormals and asymmetric intervals at powers of
    # two. Both neighboring directions expose precision-search-only mistakes.
    (root / 'main.trb').write_text('''def main()
mut value := 1.0
mut index := 0
while index < 1074
value = value / 2.0
index += 1
end
index = 0
while index < 2098
values := [value, -value, value * 1.0000000000000002, value * 0.9999999999999999]
values.each do |item|
puts(item.to_s())
end
value = value * 2.0
index += 1
end
end
''')
    expected = []
    for exponent in range(-1074, 1024):
        value = math.ldexp(1, exponent)
        expected.extend(map(canonical, [value, -value, value * 1.0000000000000002,
                                       value * 0.9999999999999999]))
    actual = run('run', root / 'main.trb').splitlines()
    assert len(actual) == len(expected), (len(actual), len(expected))
    for index, (got, wanted) in enumerate(zip(actual, expected)):
        assert got == wanted, (index, got, wanted)
    (root / 'main.trb').unlink()

    retained = run('repl', text='''convert := fn(value: Float): String; return value.to_s(); end
saved := convert(0.1)
flag := true.to_s()
record Later
value: Integer
end
puts(saved)
puts(flag)
puts(convert(1.25))
absent: Float? := nil
puts(absent&.to_s() == nil)
:reload
puts(saved)
puts(convert(-2.5))
:quit
''')
    assert retained.count('0.1\n') == 3, retained
    assert retained.count('true\n') == 4, retained
    assert retained.endswith('0.1\n-2.5\n'), retained
    assert 'reloaded\n' in retained, retained

print('PASS scalar String conversion: 8,392 binary64 boundaries, retained callbacks and replay')
