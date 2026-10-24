#!/usr/bin/env python3
"""Exercise byte encodings and request ID propagation across modules and forced GC."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('binary', type=Path)
parser.add_argument('--reference', type=Path)
parser.add_argument('--reference-only', action='store_true')
args = parser.parse_args()
if args.reference_only and not args.reference:
    parser.error('--reference-only requires --reference')
binary = args.binary.resolve()

producer = r'''import trb/std/encoding/hex
import trb/std/encoding/base64
import trb/std/secure_random
import trb/std/result
import { Context, ContextKey, Next, Request, Response } from trb/web
import { Body, Headers, HttpMethod } from trb/http
import { RequestID } from trb/web/middleware/request_id
KEY := ContextKey<Bytes>.new("payload")
def make_bytes(): Bytes
case Hex.decode("000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9fa0a1a2a3a4a5a6a7a8a9aaabacadaeafb0b1b2b3b4b5b6b7b8b9babbbcbdbebfc0c1c2c3c4c5c6c7c8c9cacbcccdcecfd0d1d2d3d4d5d6d7d8d9dadbdcdddedfe0e1e2e3e4e5e6e7e8e9eaebecedeeeff0f1f2f3f4f5f6f7f8f9fafbfcfdfeff")
when Result::Ok(value)
return value
when Result::Err(_error)
return "failed".to_bytes()
end
end
INITIAL_BYTES := make_bytes()
def check_bytes(value: Bytes)
puts(value.size() == 256)
puts(Hex.encode(value) == "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9fa0a1a2a3a4a5a6a7a8a9aaabacadaeafb0b1b2b3b4b5b6b7b8b9babbbcbdbebfc0c1c2c3c4c5c6c7c8c9cacbcccdcecfd0d1d2d3d4d5d6d7d8d9dadbdcdddedfe0e1e2e3e4e5e6e7e8e9eaebecedeeeff0f1f2f3f4f5f6f7f8f9fafbfcfdfeff")
case Base64.decode(Base64.encode(value))
when Result::Ok(decoded)
puts(Hex.encode(decoded) == Hex.encode(value))
when Result::Err(_error)
puts(false)
end
case Base64.url_decode(Base64.url_encode(value))
when Result::Ok(decoded)
puts(Hex.encode(decoded) == Hex.encode(value))
when Result::Err(_error)
puts(false)
end
end
class Terminal implements Next
def call(context: Context): Response
case context.fetch(KEY)
when Result::Ok(value)
check_bytes(value)
when Result::Err(_error)
puts("lost bytes")
end
case context.request.header_value("x-request-id")
when Result::Ok(value)
case Hex.decode(value)
when Result::Ok(decoded)
puts(decoded.size() == 16)
when Result::Err(_error)
puts(false)
end
return Response.text(value)
when Result::Err(_error)
return Response.text("missing")
end
end
end
def probe()
check_bytes(INITIAL_BYTES)
value := make_bytes()
context := Context.new(request: Request.new(method: HttpMethod.get(), path: "/example", query_string: "", headers: Headers.new(), body: Body.empty()), path_parameters: {}).with(KEY, value)
response := RequestID.call(context, Terminal.new())
case response.header_value("x-request-id")
when Result::Ok(id)
puts(id == response.body.to_s())
when Result::Err(_error)
puts(false)
end
puts(SecureRandom.bytes(257).size() == 257)
end
'''
expected = "true\n" * 11
retained_input = r'''import { make_bytes, check_bytes } from encoding_values
stored := make_bytes()
record Hex
other: Integer
end
record Base64
other: String
end
check_bytes(stored)
record Later
end
check_bytes(stored)
:quit
'''

with tempfile.TemporaryDirectory(prefix='native-encoding-') as temporary:
    root = Path(temporary)
    environment = dict(os.environ, NO_COLOR='1', TERM='dumb', TRBN_HISTORY=str(root / 'history'))

    def run(command, *, data=None):
        result = subprocess.run(list(map(str, command)), cwd=root, env=environment,
                                input=data, capture_output=True, text=True, timeout=90)
        assert result.returncode == 0, (command, result.stdout, result.stderr)
        return result

    (root / 'encoding_values.trb').write_text(producer)
    main = root / 'main.trb'
    main.write_text('import { probe } from encoding_values\ndef main()\nprobe()\nend\n')
    program = root / 'program'
    if args.reference:
        reference = args.reference.resolve()
        config = root / 'reference.trbconfig.jsonc'
        config.write_text(json.dumps({'name': 'encoding-values', 'mode': 'go',
            'sourceDir': '.', 'go': {'module': 'example.com/encoding-values'}}))
        run([reference, 'check', '--config', config])
        run([reference, 'build', '--config', config, '--compile', '--outfile', program])
        assert run([program]).stdout == expected
    if not args.reference_only:
        assert run([binary, 'check', main]).stdout == 'ok\n'
        run([binary, 'build', '--compile', main, '--outfile', program])
        assert run([program]).stdout == expected

    main.unlink()
    config = root / 'trbconfig.jsonc'
    config.write_text(json.dumps({'name': 'encoding-values',
        'mode': 'go' if args.reference_only else 'trb', 'sourceDir': '.',
        'go': {'module': 'example.com/encoding-values'}}))
    repl_binary = reference if args.reference_only else binary
    retained = run([repl_binary, 'repl', '--config', config], data=retained_input)
    assert not retained.stderr, retained
    assert retained.stdout.endswith('true\n' * 8), retained

    if not args.reference_only:
        main.write_text('import { probe } from encoding_values\ndef main()\n'
                        '(0...8).each do |_index|\nprobe()\nend\nend\n')
        emitted = run([binary, '--internal-driver', 'emit-qbe', main])
        forced, ordinary, hooks = [], False, 0
        for line in emitted.stdout.splitlines():
            if line.startswith('function '):
                ordinary = '$trbnf' in line
            if line == '}':
                ordinary = False
            if ordinary and any(marker in line for marker in (
                    'call $trbn_array_new(', 'call $trbn_array_new_reserved(',
                    'call $trbn_array_push_', 'call $trbn_array_grow_paced(',
                    'call $trbn_gc_alloc(', 'call $trbn_string_concat(')):
                forced.append('\tcall $trbn_gc_collect(w 0)')
                hooks += 1
            forced.append(line)
        assert hooks >= 8, hooks
        il, assembly = root / 'input.ssa', root / 'input.s'
        il.write_text('\n'.join(forced) + '\n')
        run([binary.with_name('qbe'), '-o', assembly, il])
        run(['/usr/bin/cc', assembly, '-lm', '-o', program])
        collected = subprocess.run([str(program)], cwd=root, text=True, capture_output=True,
            env=dict(environment, TYPE_RB_NATIVE_RUNTIME_STATS='1'), timeout=90)
        assert collected.returncode == 0 and collected.stdout == expected * 8, collected
        statistics = {}
        for line in collected.stderr.splitlines():
            prefix, key, value = line.split(',')
            assert prefix == 'type-rb-native-gc-stat-v1' and key not in statistics, line
            statistics[key] = int(value)
        assert statistics['collections'] >= 8, statistics
        assert statistics['live-bytes'] == 0, statistics
        assert statistics['allocated-bytes'] == statistics['reclaimed-bytes'], statistics
        print('Encoding GC hooks:', hooks, 'statistics:', json.dumps(statistics, sort_keys=True))

    if not args.reference_only:
        shim = root / 'entropy-fixture.c'
        shim.write_text(r"""#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
static int calls;
int getentropy(void *buffer, size_t length) {
    ++calls;
    fprintf(stderr, "entropy-chunk:%zu\n", length);
    if (length == 0 || length > 256) abort();
    if (getenv("ENTROPY_FIXTURE_FAIL") && calls == 2) return -1;
    unsigned char *bytes = buffer;
    for (size_t i = 0; i < length; ++i) bytes[i] = (unsigned char)i;
    return 0;
}
""")
        for length in (0, 1, 256, 257, 513, 65536, -1, 65537):
            main.write_text('import trb/std/secure_random\ndef main()\n'
                            f'puts(SecureRandom.bytes({length}).size())\nend\n')
            il.write_text(run([binary, '--internal-driver', 'emit-qbe', main]).stdout)
            run([binary.with_name('qbe'), '-o', assembly, il])
            run(['/usr/bin/cc', assembly, shim, '-lm', '-o', program])
            observed = subprocess.run([str(program)], cwd=root, env=environment,
                                      text=True, capture_output=True, timeout=30)
            if 0 <= length <= 65536:
                chunks = [256] * (length // 256) + ([length % 256] if length % 256 else [])
                assert observed.returncode == 0 and observed.stdout == str(length) + '\n', observed
                assert observed.stderr == ''.join(f'entropy-chunk:{n}\n' for n in chunks), observed
                if length == 513:
                    failed = subprocess.run([str(program)], cwd=root, text=True, capture_output=True,
                        env=dict(environment, ENTROPY_FIXTURE_FAIL='1'), timeout=30)
                    assert failed.returncode != 0 and not failed.stdout, failed
                    assert failed.stderr.splitlines() == ['entropy-chunk:256', 'entropy-chunk:256',
                        'panic: secure_random.bytes could not read operating system entropy'], failed
            else:
                assert observed.returncode != 0 and not observed.stdout, observed
                assert observed.stderr == 'panic: secure_random.bytes length must be between 0 and 65536\n', observed
        print('Entropy OS chunk bounds and failure checks passed.')

print('Encoding, request ID, retained-session and storage checks passed.')
