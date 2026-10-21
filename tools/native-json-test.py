#!/usr/bin/env python3
"""Verify JSON source ownership, retained values and managed recursive payloads."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('binary', type=Path)
args = parser.parse_args()
binary = args.binary.resolve()
source = r'''import trb/std/json
import trb/std/jsonc
import trb/std/result
import trb/std/url

def display(value: JSON::Value)
case JSON.stringify(value)
when Result::Ok(text)
puts(text)
when Result::Err(error)
puts(error.message)
end
end

def probe()
held := JSON::Value::Object({"held" => JSON::Value::Array([JSON::Value::String("retained"), JSON::Value::Integer(7)])})
mut index := 0
while index < 32
case JSONC.parse("/* comment */{\"z\":[null,true,{\"text\":\"\\ud83d\\ude00\"}],\"a\":1}")
when Result::Ok(value)
case JSON.field(value, "z")
when Result::Ok(items)
if index == 31
display(items)
end
when Result::Err(error)
puts(error.message)
end
when Result::Err(error)
puts(error.message)
end
index += 1
end
display(held)
puts(URL.encode_component("json + url"))
end

def main()
probe()
end
'''
expected = '[null,true,{"text":"😀"}]\n{"held":["retained",7]}\njson%20%2B%20url\n'

with tempfile.TemporaryDirectory(prefix='native-json-') as temporary:
    root = Path(temporary)
    env = dict(os.environ, NO_COLOR='1', TERM='dumb', TRBN_HISTORY=str(root / 'history'))
    env.pop('TYPE_RB_NATIVE_RUNTIME_TRACE', None)
    env.pop('TYPE_RB_NATIVE_RUNTIME_STATS', None)

    def run(command, *, data=None, success=True, environment=env):
        result = subprocess.run(list(map(str, command)), cwd=root, env=environment,
                                input=data, capture_output=True, text=True, timeout=120)
        assert (result.returncode == 0) == success, (command, result.stdout, result.stderr)
        return result

    file_root = root / 'file root'
    file_root.mkdir()
    main = file_root / 'main.trb'
    main.write_text(source)
    shadow = file_root / 'trb/std/json/index.trb'
    shadow.parent.mkdir(parents=True)
    shadow.write_text('module JSON\ndef wrong()\nunknown()\nend\nend\n')
    assert run([binary, 'check', main]).stdout == 'ok\n'
    program = root / 'program'
    run([binary, 'build', '--compile', main, '--outfile', program])
    result = run([program], environment=dict(env, TYPE_RB_NATIVE_RUNTIME_STATS='1'))
    assert result.stdout == expected, result
    statistics = {}
    for line in result.stderr.splitlines():
        prefix, key, value = line.split(',')
        assert prefix == 'type-rb-native-gc-stat-v1' and key not in statistics, line
        statistics[key] = int(value)
    assert statistics['live-bytes'] == 0, statistics
    assert statistics['allocated-bytes'] == statistics['reclaimed-bytes'], statistics
    assert run([binary, 'run', main]).stdout == expected

    # Collect at each decoded string boundary while raw nodes, recursive values
    # and an unrelated retained object are live in ordinary checked MIR.
    emitted = run([binary, '--internal-driver', 'emit-qbe', main]).stdout
    match = re.search(r'^function l \$trbn_bytes_to_string\([^\n]*\) \{.*?^\}', emitted, re.M | re.S)
    assert match
    hook = ' %result =l call $trbn_string_alloc(l %size)'
    assert match[0].count(hook) == 1
    forced = emitted.replace(match[0], match[0].replace(hook, ' call $trbn_gc_collect(w 0)\n' + hook))
    ssa, assembly, forced_program = root / 'forced.ssa', root / 'forced.s', root / 'forced'
    ssa.write_text(forced)
    run([binary.with_name('qbe'), '-o', assembly, ssa])
    run(['/usr/bin/cc', assembly, '-lm', '-o', forced_program])
    assert run([forced_program]).stdout == expected

    project = root / 'project'
    (project / 'src').mkdir(parents=True)
    config = project / 'trbconfig.jsonc'
    config.write_text(json.dumps({'name': 'json-import', 'mode': 'trb', 'sourceDir': 'src'}))
    (project / 'src/main.trb').write_text(source)
    assert run([binary, 'check', '--config', config]).stdout == 'ok\n'
    run([binary, 'build', '--compile', '--config', config, '--outfile', program])
    assert run([program]).stdout == expected

    declarations = source.split('def main()')[0]
    retained = run([binary, 'repl'], data=declarations + 'probe()\nclass Later\nend\nprobe()\n:quit\n')
    assert not retained.stderr and retained.stdout == expected * 2, retained

    # Alias and default importers must share recursive enum identity.
    (file_root / 'helper.trb').write_text('import trb/std/json as OtherJSON\n'
        'def identity(value: OtherJSON::Value): OtherJSON::Value\nreturn value\nend\n')
    main.write_text('import trb/std/json\nimport trb/std/result\nimport { identity } from helper\n'
        'def main()\ncase JSON.stringify(identity(JSON::Value::Array([JSON::Value::Integer(7)])))\n'
        'when Result::Ok(text)\nputs(text)\nwhen Result::Err(error)\nputs(error.message)\nend\nend\n')
    run([binary, 'build', '--compile', main, '--outfile', program])
    assert run([program]).stdout == '[7]\n'

    for declarations in ('import trb/internal/json as Hidden\n',
                         'module JSON\nend\nimport trb/internal/json as Hidden\n'):
        main.write_text(declarations + 'def main()\nputs("unreachable")\nend\n')
        result = run([binary, 'check', main], success=False)
        assert 'internal package imports are reserved for verified standard sources' in result.stderr, result

print('PASS JSON file/project ownership, recursive values, forced collection and retained REPL')
