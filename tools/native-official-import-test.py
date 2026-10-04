#!/usr/bin/env python3
"""Exercise embedded official sources through ordinary file/project/REPL imports."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('binary', type=Path)
parser.add_argument('--reference', type=Path)
args = parser.parse_args()
binary = args.binary.resolve()
reference = args.reference.resolve() if args.reference else None
source = '''import { Headers as HeaderMap, HttpMethod, Body } from trb/http
def probe()
puts(HeaderMap.new().size())
puts(HttpMethod.get().to_s())
puts(Body.new("A😀".to_bytes()).size())
puts(Body.new("body".to_bytes()).bytes().to_s())
headers := HeaderMap.new().add("X-Test", "first").add("x-test", "second")
puts(headers.values("X-TEST").size())
puts(headers.with("X-Test", "kept").size())
puts(headers.without("X-Test").size())
end
def main()
probe()
end
'''
expected = '0\nGET\n5\nbody\n2\n1\n0\n'

with tempfile.TemporaryDirectory(prefix='native-official-import-') as temporary:
    root = Path(temporary)
    environment = dict(os.environ, NO_COLOR='1', TERM='dumb', TRBN_HISTORY=str(root / 'history'))

    def run(command, *, data=None, success=True):
        result = subprocess.run(list(map(str, command)), cwd=root, env=environment,
                                input=data, capture_output=True, text=True, timeout=90)
        assert (result.returncode == 0) == success, (command, result.stdout, result.stderr)
        return result

    file_root = root / 'file root'
    file_root.mkdir()
    main = file_root / 'main.trb'
    main.write_text(source)
    # A filesystem spelling cannot replace the compiler-owned official source.
    shadow = file_root / 'trb/http/index.trb'
    shadow.parent.mkdir(parents=True)
    shadow.write_text('class Headers\ndef invalid()\nunknown()\nend\nend\n')
    assert run([binary, 'check', main]).stdout == 'ok\n'
    program = file_root / 'program'
    run([binary, 'build', '--compile', main, '--outfile', program])
    assert run([program]).stdout == expected

    project = root / 'project'
    (project / 'src').mkdir(parents=True)
    config = project / 'trbconfig.jsonc'
    config.write_text(json.dumps({'name': 'official-import', 'mode': 'trb', 'sourceDir': 'src'}))
    (project / 'src/main.trb').write_text(source)
    assert run([binary, 'check', '--config', config]).stdout == 'ok\n'
    run([binary, 'build', '--compile', '--config', config, '--outfile', program])
    assert run([program]).stdout == expected

    declarations = source.split('def main()')[0]
    retained = run([binary, 'repl'], data=declarations + 'probe()\nclass Later\nend\nprobe()\n:quit\n')
    assert not retained.stderr and retained.stdout == expected * 2, retained

    # Independent importers keep the same nominal identity.
    (file_root / 'helper.trb').write_text('import { Headers } from trb/http\n'
        'def identity(value: Headers): Headers\nreturn value\nend\n')
    main.write_text('import { Headers as HeaderMap } from trb/http\nimport { identity } from helper\n'
                    'def main()\nputs(identity(HeaderMap.new()).size())\nend\n')
    run([binary, 'build', '--compile', main, '--outfile', program])
    assert run([program]).stdout == '0\n'

    for imports, marker in [
        ('import { Headers, Headers as Other } from trb/http', 'already imported'),
        ('import { Missing } from trb/http', 'Missing'),
        ('import trb/not_a_package', 'package imports'),
        ('import trb/internal/runtime', 'package imports'),
        ('import trb/platform/typescript/browser', 'unimplemented platform or semantic provider'),
        ('import trb/platform/go/cli', 'unimplemented platform or semantic provider'),
        ('import trb/web/middleware', 'unimplemented platform or semantic provider: trb/web/index'),
    ]:
        main.write_text(imports + '\ndef main()\nreturn\nend\n')
        rejected = run([binary, 'check', main], success=False)
        assert marker in rejected.stderr, rejected
    internal = run([binary, 'repl'], data='import trb/internal/runtime\n:quit\n')
    assert internal.stderr, internal

    if reference:
        main.write_text(source)
        run([reference, 'check', main])
        run([reference, 'build', '--compile', '--outfile', program, main])
        assert run([program]).stdout == expected
        observed = run([reference, 'repl'], data=declarations + 'probe()\nprobe()\n:quit\n')
        assert not observed.stderr and observed.stdout == expected * 2, observed

print('PASS exact bundled HTTP imports, canonical identity, file/project/REPL and rejected boundaries')
