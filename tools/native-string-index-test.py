#!/usr/bin/env python3
"""Verify the actual ordinary String-index runtime and its static values."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--qbe', type=Path, required=True)
parser.add_argument('--source', type=Path)
parser.add_argument('--output', type=Path)
args = parser.parse_args()
repo = Path(__file__).resolve().parent.parent
source = args.source or repo / 'compiler/src/qbe_runtime.trb'
decoded = '\n'.join(json.loads(s) for s in re.findall(r'"(?:[^"\\]|\\.)*"', source.read_text()))
bodies = re.findall(r'^function l \$trbn_string_index\(l %string, l %requested\) \{.*?^\}', decoded, re.M | re.S)
assert len(bodies) == 1
data = re.findall(r'^data \$(?:string_byte_values|trbn_bounds_error) = [^\n]+', decoded, re.M)
assert any(line.startswith('data $trbn_bounds_error ') for line in data)
il = '\n'.join(data) + '\nexport ' + bodies[0] + '\n'
# The observer supplies inputs and counts allocations; String indexing itself
# is extracted from the repository-owned TypeRB runtime, including its checks.
observer = r'''
#include <assert.h>
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
struct string { uint64_t descriptor; int64_t length; unsigned char bytes[]; };
_Static_assert(sizeof(void *) == 8 && offsetof(struct string, bytes) == 16, "String ABI");
extern struct string *trbn_string_index(struct string *, int64_t);
static unsigned allocations;
void *trbn_string_alloc(int64_t size) { ++allocations; return calloc(1, (size_t)size + 8); }
void trbn_fail(const void *message, int64_t size) {
    fwrite(message, 1, (size_t)size, stderr);
    exit(70);
}
int main(int argc, char **argv) {
    struct string *source = calloc(1, 16 + 257);
    assert(source);
    source->length = 256;
    for (unsigned i = 0; i < 256; ++i) source->bytes[i] = (unsigned char)i;
    if (argc == 3) {
        source->length = strtoll(argv[1], NULL, 10);
        trbn_string_index(source, strtoll(argv[2], NULL, 10));
        return 1;
    }
    assert(argc == 1);
    struct string *retained[256];
    for (int i = 0; i < 256; ++i) {
        retained[i] = trbn_string_index(source, i);
        struct string *negative = trbn_string_index(source, i - 256);
        assert(retained[i]->length == 1 && negative->length == 1);
        assert(retained[i]->bytes[0] == i && negative->bytes[0] == i);
        assert(retained[i]->bytes[1] == 0 && negative->bytes[1] == 0);
    }
    memset(source->bytes, 255, 256);
    free(source);
    struct { uint64_t descriptor; int64_t length; unsigned char bytes[2]; } next = {0, 1, {0, 0}};
    for (int round = 0; round < 4; ++round) {
        for (int i = 255; i >= 0; --i) {
            next.bytes[0] = (unsigned char)i;
            struct string *value = trbn_string_index((struct string *)&next, 0);
            assert(value->length == 1 && value->bytes[0] == i && value->bytes[1] == 0);
        }
    }
    for (int i = 0; i < 256; ++i) {
        assert(retained[i]->length == 1 && retained[i]->bytes[0] == i && retained[i]->bytes[1] == 0);
        assert(retained[i]->descriptor == 0); /* Existing collector's static marker. */
    }
    if (allocations != 0) { fprintf(stderr, "unexpected indexing allocations: %u\n", allocations); return 2; }
    puts("256 byte values; 1536 checked reads; zero allocations");
    return 0;
}
'''
observations = []
with tempfile.TemporaryDirectory(prefix='native String index ') as directory:
    root = Path(directory)
    (root / 'index.ssa').write_text(il)
    (root / 'observer.c').write_text(observer)
    subprocess.run([str(args.qbe.resolve()), '-o', str(root / 'index.s'), str(root / 'index.ssa')], check=True, capture_output=True, timeout=30)
    subprocess.run(['/usr/bin/cc', '-O2', str(root / 'index.s'), str(root / 'observer.c'), '-o', str(root / 'probe')], check=True, capture_output=True, timeout=30)
    good = subprocess.run([str(root / 'probe')], capture_output=True, timeout=10)
    assert good.returncode == 0 and good.stderr == b'', good
    assert good.stdout == b'256 byte values; 1536 checked reads; zero allocations\n', good
    observations.append({'case': 'all-bytes-and-lifetime', 'reads': 1536, 'allocations': 0})
    for length, index in [(0, 0), (0, -1), (256, -257), (256, 256), (256, -9007199254740991), (256, 9007199254740991)]:
        result = subprocess.run([str(root / 'probe'), str(length), str(index)], capture_output=True, timeout=10)
        assert result.returncode == 70 and result.stdout == b'', result
        assert result.stderr == b'panic: index is out of bounds\n', result
        observations.append({'case': 'required-bounds-failure', 'length': length, 'index': index})
report = {'sourceSha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'runtimeSha256': hashlib.sha256(il.encode()).hexdigest(), 'observations': observations}
if args.output:
    args.output.write_text(json.dumps(report, indent=2) + '\n')
print('String indexing: all 256 values, retained contents, zero allocations and 6 bounds failures passed')
