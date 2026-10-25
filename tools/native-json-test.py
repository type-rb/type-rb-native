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
parser.add_argument('--reference', type=Path)
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
    # A decoded escape can precede raw UTF-8 octets in the same join. Cached
    # code-point counts must not mistake these split bytes for separate runes.
    pairs.extend([
        (b'\\u00e9' + 'β😀'.encode(), 'éβ😀'),
        (b'\\ud83d\\ude00' + 'éβ'.encode(), '😀éβ'),
        (b'\\u00e9' + b'\xf0\x90\x80' + 'β'.encode(), 'é' + '\ufffd' * 3 + 'β'),
    ])
    statements, outputs = [], []
    for raw, decoded in pairs:
        literal = '"' + ''.join(f'\\x{octet:02x}' for octet in b'"' + raw + b'"') + '"'
        statements.append(f'parse_and_display({literal})')
        outputs.append(quoted(decoded))
    # Encoding raw String bytes must preserve the same replacement boundaries
    # without relying on the parser to have normalized invalid UTF-8 first.
    encoded_pairs = [(bytes([octet]), chr(octet) if octet < 128 else '\ufffd')
                     for octet in range(256)]
    encoded_pairs.extend((raw, decoded) for raw, decoded in pairs
                         if len(raw) > 1 and not raw.startswith(b'\\'))
    for raw, decoded in encoded_pairs:
        literal = '"' + ''.join(f'\\x{octet:02x}' for octet in raw) + '"'
        statements.append(f'display(JSON::Value::String({literal}))')
        outputs.append(quoted(decoded))
    # Exercise accumulated fragments across long ASCII/Unicode/escaped strings.
    for unit, count, tail, decoded in [
            (b'a', 8192, b'\xf0\x90\x80', 'a' * 8192 + '\ufffd' * 3),
            (b'\\ud83d\\ude00', 512, b'', '😀' * 512),
            (b'\\ud800x', 512, b'', '\ufffdx' * 512)]:
        def octets(raw):
            return '"' + ''.join(f'\\x{octet:02x}' for octet in raw) + '"'
        delimiter = bytes([34])
        expression = f'{octets(delimiter)} + repeated({octets(unit)}, {count}) + {octets(tail + delimiter)}'
        statements.append(f'parse_and_display({expression})')
        outputs.append(quoted(decoded))
    for suffix in ('', '<>&', '\u2028\u2029', '"\\\n\t\x00'):
        value = 'aβ😀' * 256 + suffix
        statements.append(f'display(JSON::Value::String({json.dumps(value, ensure_ascii=False)}))')
        outputs.append(quoted(value))
        statements.append(f'parse_and_display({json.dumps(quoted(value), ensure_ascii=False)})')
        outputs.append(quoted(value))
    # Force collection while a failed Unicode escape reconstructs its raw
    # diagnostic. Earlier object members must remain rooted across that join.
    for digits in ("x000", "0x00", "00x0", "000x", "12xz"):
        sequence = "\\u" + digits
        document = '{"held":"aβ😀","bad":"' + sequence + '"}'
        statements.append(f'parse_and_display({json.dumps(document, ensure_ascii=False)})')
        outputs.append("invalid escape sequence `" + sequence + "` in string")
    # Sibling containers and scalar variants must remain independent while the
    # parser stores their raw nodes and the conversion stack revisits parents.
    structures = [
        [{"id": index, "name": "β😀", "items": [index, None, index % 2 == 0],
          "empty": {}} for index in range(256)],
        {f"key-{index}": "aβ😀\n<>&" for index in range(256)},
        {"left": [[], {}, [False, True]], "right": {"nested": [{}, [], None]}},
    ]
    # Exercise longer multibyte text beside escapes and in object keys.
    for width in (15, 16, 17, 31, 32, 33):
        structures.extend([
            'a' * width + 'β😀' + 'z' * width,
            'a' * width + '\n"<>&\u2028' + 'β😀' * width,
            {'a' * width + 'β/~/😀': ['β😀' * width, 'a' * width]},
        ])
    nested = 0
    for _ in range(128):
        nested = {"z": nested, "a": []}
    structures.append(nested)
    for value in structures:
        document = json.dumps(value, ensure_ascii=False)
        statements.append(f'parse_and_display({json.dumps(document, ensure_ascii=False)})')
        encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
        for character in ('<', '>', '&', '\u2028', '\u2029'):
            encoded = encoded.replace(character, f'\\u{ord(character):04x}')
        outputs.append(encoded)
    item = json.dumps('"aβ😀",', ensure_ascii=False)
    last = json.dumps('"aβ😀"]', ensure_ascii=False)
    statements.append(f'parse_and_display("[" + repeated({item}, 2047) + {last})')
    outputs.append('[' + ','.join(['"aβ😀"'] * 2048) + ']')
    for prefix, unit, count, suffix, expected_document in [
            ('/*', 'β😀* ', 1024, '*/["aβ😀",true]', '["aβ😀",true]'),
            ('// ', 'β😀', 1024, '\r\n{"value":"a\\nβ😀"}', '{"value":"a\\nβ😀"}'),
            ('{"slashes":"/* text */ // text",/*', 'x', 4096, '*/"z":0}',
             '{"slashes":"/* text */ // text","z":0}')]:
        expression = (f'{json.dumps(prefix, ensure_ascii=False)} + repeated({json.dumps(unit, ensure_ascii=False)}, {count})'
                      f' + {json.dumps(suffix, ensure_ascii=False)}')
        statements.append(f'parse_jsonc_and_display({expression})')
        outputs.append(expected_document)
    declarations = source.split('def probe()')[0].replace('import trb/std/url\n', '')
    main.write_text(declarations + '''
# Construct large runtime inputs without embedding large compiler constants.
def repeated(text: String, count: Integer): String
mut parts: Array<String> := []
mut index := 0
while index < count
parts.push(text)
index += 1
end
return parts.join("")
end
def parse_jsonc_and_display(text: String)
case JSONC.parse(text)
when Result::Ok(value)
display(value)
when Result::Err(error)
puts(error.message)
end
end
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
    actual = run([program]).stdout
    assert actual == '\n'.join(outputs) + '\n', {
        'expectedLines': len(outputs), 'actualLines': len(actual.splitlines()),
        'differences': [(index + 1, expected[:160], observed[:160])
                        for index, (expected, observed) in enumerate(zip(outputs, actual.splitlines()))
                        if expected != observed][:3],
    }
    emitted = run([binary, '--internal-driver', 'emit-qbe', main]).stdout
    join = re.search(r'^function l \$trbn_array_join\([^\n]*\) \{.*?^\}', emitted, re.M | re.S)
    assert join
    assert join[0].count('@start\n') == 1
    forced = emitted.replace(join[0], join[0].replace('@start\n', '@start\n call $trbn_gc_collect(w 0)\n'))
    # Collect during parser-owned pool and object-member creation as well as
    # joins. Partially initialized state and retained ancestors must stay live.
    for allocator in ('trbn_array_new', 'trbn_hash_new'):
        allocation = re.search(r'^function l \$' + allocator + r'\([^\n]*\) \{.*?^\}', forced, re.M | re.S)
        assert allocation and allocation[0].count('@start\n') == 1
        forced = forced.replace(allocation[0], allocation[0].replace('@start\n', '@start\n call $trbn_gc_collect(w 0)\n'))
    ssa.write_text(forced)
    run([binary.with_name('qbe'), '-o', assembly, ssa])
    run(['/usr/bin/cc', assembly, '-lm', '-o', forced_program])
    assert run([forced_program]).stdout == '\n'.join(outputs) + '\n'
    if args.reference:
        assert run([args.reference.resolve(), 'run', main]).stdout == '\n'.join(outputs) + '\n'

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
        ('{"z":{"a":9007199254740992},"a":[{"z":9007199254740992,"a":9007199254740992}]}', '/a/0/a'),
        ('{"a":{"z":9007199254740992},"a":{"b":1},"b":{"a":9007199254740992}}', '/b/a'),
        ('[' + '0,' * 64 + '9007199254740992]', '/64'),
        ('{"old":[{"bad":9007199254740992}],"old":0,"live":[0,{"~/":9007199254740992}]}', '/live/1/~0~1'),
        ('{"old":{"bad":[9007199254740992]},"old":{"ok":[]}}', None),
    ]
    pointer_source = declarations.replace('import trb/std/jsonc\n', '') + '''
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

    # Path metadata can be constructed lazily after discovering an invalid
    # number. Retain the original traversal order, mixed keys and array indexes.
    encoding_source = '''import trb/std/json
import trb/std/result
def report_encoding(value: JSON::Value)
case JSON.stringify(value)
when Result::Ok(_text)
puts("ok")
when Result::Err(error)
puts(error.path)
puts(error.message)
end
end
def main()
bad := JSON::Value::Float(1.0 / 0.0)
negative := JSON::Value::Float(-1.0 / 0.0)
nan := JSON::Value::Float(0.0 / 0.0)
report_encoding(bad)
report_encoding(JSON::Value::Array([JSON::Value::Integer(0), negative, nan]))
report_encoding(JSON::Value::Object({"~/β😀" => JSON::Value::Array([JSON::Value::Null, bad])}))
report_encoding(JSON::Value::Array([JSON::Value::Object({"" => nan}), bad]))
mut items: Array<JSON::Value> := []
mut index := 0
while index < 64
items.push(JSON::Value::Integer(index))
index += 1
end
items.push(bad)
report_encoding(JSON::Value::Array(items))
report_encoding(JSON::Value::Object({"valid" => JSON::Value::Array([JSON::Value::Float(-0.0), JSON::Value::Null])}))
end
'''
    encoding_output = ''.join(path + '\nJSON Float must be finite\n'
                              for path in ('', '/1', '/~0~1β😀/1', '/0/', '/64')) + 'ok\n'
    main.write_text(encoding_source)
    run([binary, 'build', '--compile', main, '--outfile', program])
    assert run([program]).stdout == encoding_output
    if args.reference:
        # These objects contain only one failing member, avoiding the separate
        # unresolved multi-member precedence and REPL-message specifications.
        assert run([args.reference.resolve(), 'run', main]).stdout == encoding_output

    for regression_source, regression_output in ((pointer_source, pointer_output),
                                                  (encoding_source, encoding_output)):
        main.write_text(regression_source)
        emitted = run([binary, '--internal-driver', 'emit-qbe', main]).stdout
        conversion = re.search(r'^function l \$trbn_integer_to_string\([^\n]*\) \{.*?^\}', emitted, re.M | re.S)
        assert conversion and conversion[0].count('@start\n') == 1
        forced = emitted.replace(conversion[0], conversion[0].replace(
            '@start\n', '@start\n call $trbn_gc_collect(w 0)\n'))
        ssa.write_text(forced)
        run([binary.with_name('qbe'), '-o', assembly, ssa])
        run(['/usr/bin/cc', assembly, '-lm', '-o', forced_program])
        assert run([forced_program]).stdout == regression_output

    # Loading JSON's shared octets must not grant authored modules access to
    # the internal dependency, even after the verified provider has loaded it.
    for declarations in ('import trb/internal/encoding_bytes as Hidden\n',
                         'import trb/std/json\nimport trb/internal/encoding_bytes as Hidden\n',
                         'module EncodingBytes\nend\nimport trb/internal/encoding_bytes as Hidden\n'):
        main.write_text(declarations + 'def main()\nputs("unreachable")\nend\n')
        result = run([binary, 'check', main], success=False)
        assert 'internal encoding and entropy sources are reserved for verified standard sources' in result.stderr, result

    for declarations in ('import trb/internal/json as Hidden\n',
                         'module JSON\nend\nimport trb/internal/json as Hidden\n'):
        main.write_text(declarations + 'def main()\nputs("unreachable")\nend\n')
        result = run([binary, 'check', main], success=False)
        assert 'internal package imports are reserved for verified standard sources' in result.stderr, result

print('PASS JSON file/project ownership, recursive values, forced collection and retained REPL')
