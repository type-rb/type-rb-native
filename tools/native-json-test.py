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

    # Cover every raw non-control octet, UTF-8 width boundary and invalid
    # prefix. JSON decoding replaces each invalid byte, unlike Bytes#to_s's
    # maximal-subpart replacement. String escaping must also preserve HTML
    # and JavaScript safety after a long, otherwise unescaped prefix.
    def quoted(text):
        encoded = json.dumps(text, ensure_ascii=False)
        for character in ('<', '>', '&', '\u2028', '\u2029'):
            encoded = encoded.replace(character, f'\\u{ord(character):04x}')
        return encoded

    pairs = [(bytes([octet]), chr(octet) if octet < 128 else '\ufffd')
             for octet in range(32, 256) if octet not in (34, 92)]
    for point in (0x80, 0x7ff, 0x800, 0xd7ff, 0xe000, 0xffff,
                  0x10000, 0x10ffff, 0x2028, 0x2029, 0xfffd):
        pairs.append((chr(point).encode(), chr(point)))
    for raw in (b'\xc0\xaf', b'\xc2', b'\xe0\x9f\xbf', b'\xed\xa0\x80',
                b'\xe2\x82', b'\xf0\x8f\xbf\xbf', b'\xf4\x90\x80\x80',
                b'\xf0\x90\x80', b'\xf5\x80\x80\x80'):
        pairs.append((raw, '\ufffd' * len(raw)))
    statements, outputs = [], []
    for raw, decoded in pairs:
        literal = '"' + ''.join(f'\\x{octet:02x}' for octet in b'"' + raw + b'"') + '"'
        statements.append(f'parse_and_display({literal})')
        outputs.append(quoted(decoded))
    for suffix in ('', '<>&', '\u2028\u2029', '"\\\n\t\x00'):
        value = 'aβ😀' * 256 + suffix
        statements.append(f'display(JSON::Value::String({json.dumps(value, ensure_ascii=False)}))')
        outputs.append(quoted(value))
    declarations = source.split('def probe()')[0].replace('import trb/std/jsonc\n', '').replace('import trb/std/url\n', '')
    main.write_text(declarations + '''
def parse_and_display(text: String)
case JSON.parse(text)
when Result::Ok(value)
display(value)
when Result::Err(error)
puts(error.message)
end
end
def main()
''' + '\n'.join(statements) + '\nend\n')
    run([binary, 'build', '--compile', main, '--outfile', program])
    assert run([program]).stdout == '\n'.join(outputs) + '\n'

    # Decode failures still report escaped JSON Pointer paths after successful
    # traversal, including overwritten keys and nested array/object boundaries.
    pointer_cases = [
        ('9007199254740992', ''),
        ('{"":9007199254740992}', '/'),
        ('{"~/":[0,{"β😀/~/":9007199254740992}]}', '/~0~1/1/β😀~1~0~1'),
        ('{"~1":9007199254740992}', '/~01'),
        ('{"z":9007199254740992,"a/":9007199254740992}', '/a~1'),
        ('{"a":9007199254740992,"a":1}', None),
        ('{"a":1,"a":9007199254740992}', '/a'),
        ('[0,{"/~":[0,9007199254740992]}]', '/1/~1~0/1'),
    ]
    pointer_source = declarations + '''
def report_path(source: String)
case JSON.parse(source)
when Result::Ok(_value)
puts("ok")
when Result::Err(error)
puts(error.path)
puts(error.message)
end
end
def main()
''' + '\n'.join(f'report_path({json.dumps(text, ensure_ascii=False)})' for text, _ in pointer_cases) + '\nend\n'
    main.write_text(pointer_source)
    run([binary, 'build', '--compile', main, '--outfile', program])
    pointer_output = ''.join('ok\n' if path is None else path + '\nJSON integer is outside the portable range\n'
                             for _, path in pointer_cases)
    assert run([program]).stdout == pointer_output

    for declarations in ('import trb/internal/json as Hidden\n',
                         'module JSON\nend\nimport trb/internal/json as Hidden\n'):
        main.write_text(declarations + 'def main()\nputs("unreachable")\nend\n')
        result = run([binary, 'check', main], success=False)
        assert 'internal package imports are reserved for verified standard sources' in result.stderr, result

print('PASS JSON file/project ownership, recursive values, forced collection and retained REPL')
