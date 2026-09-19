#!/usr/bin/env python3
"""Verify ordinary String indexing and bounded, allocation-free queries."""
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
helpers = source.with_name('qbe_strings.trb')
decoded += '\n' + '\n'.join(json.loads(s) for s in re.findall(r'"(?:[^"\\]|\\.)*"', helpers.read_text()))
queries = source.with_name('qbe_string_queries.trb')
decoded += '\n' + '\n'.join(json.loads(s) for s in re.findall(r'"(?:[^"\\]|\\.)*"', queries.read_text()))
names = ['trbn_string_index', 'trbn_utf8_width', 'trbn_utf8_count', 'trbn_utf8_span',
         'trbn_string_offset', 'trbn_string_from_codepoint', 'trbn_utf8_scalar', 'trbn_source_slice',
         'trbn_string_is_utf8', 'trbn_string_query', 'trbn_string_codepoint_query']
bodies = []
for name in names:
    matches = re.findall(r'^function l \$' + name + r'\([^\n]*\) \{.*?^\}', decoded, re.M | re.S)
    assert len(matches) == 1, name
    bodies.append('export ' + matches[0])
data = re.findall(r'^data \$(?:string_byte_values|trbn_bounds_error) = [^\n]+', decoded, re.M)
assert any(line.startswith('data $trbn_bounds_error ') for line in data)
il = '\n'.join(data + bodies) + '\n'
# The observer supplies inputs and counts allocations; String indexing itself
# is extracted from the repository-owned TypeRB runtime, including its checks.
observer = r'''
#include <assert.h>
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
struct string { uint64_t descriptor; int64_t length, points; unsigned char bytes[]; };
_Static_assert(sizeof(void *) == 8 && offsetof(struct string, bytes) == 24, "String ABI");
extern struct string *trbn_string_index(struct string *, int64_t);
extern struct string *trbn_string_from_codepoint(int64_t);
extern struct string *trbn_source_slice(struct string *, int64_t, int64_t);
extern int64_t trbn_utf8_count(const unsigned char *, int64_t);
extern int64_t trbn_utf8_scalar(const unsigned char *, int64_t);
extern int64_t trbn_string_query(struct string *, struct string *, int64_t);
static unsigned allocations;
void *trbn_string_alloc(int64_t size) { ++allocations; return calloc(1, (size_t)size + 8); }
void trbn_fail(const void *message, int64_t size) {
    fwrite(message, 1, (size_t)size, stderr);
    exit(70);
}
static struct string *make(const unsigned char *data, size_t size) {
    struct string *s = calloc(1, 25 + size); assert(s);
    s->length = size; s->points = trbn_utf8_count(data, size);
    memcpy(s->bytes, data, size); return s;
}
struct guarded { void *region; size_t size; struct string *value; };
static struct guarded guard(const unsigned char *data, size_t size) {
    size_t page = (size_t)sysconf(_SC_PAGESIZE);
    assert(size % 8 == 0 && size + 24 < page);
    unsigned char *region = mmap(NULL, page * 2, PROT_READ | PROT_WRITE,
                                MAP_PRIVATE | MAP_ANON, -1, 0);
    assert(region != MAP_FAILED);
    assert(mprotect(region + page, page, PROT_NONE) == 0);
    struct string *s = (struct string *)(region + page - size - 24);
    s->length = size; s->points = trbn_utf8_count(data, size);
    if (size) memcpy(s->bytes, data, size);
    return (struct guarded){region, page * 2, s};
}
static void expect_query(struct string *value, const unsigned char *part, size_t size,
                         int64_t first, int64_t last, int64_t prefix, int64_t suffix, int64_t contains) {
    struct string *pattern = make(part, size);
    const int64_t expected[] = {first, last, prefix, suffix, contains};
    for (int mode = 0; mode < 5; ++mode)
        assert(trbn_string_query(value, pattern, mode) == expected[mode]);
    free(pattern);
}
int main(int argc, char **argv) {
    unsigned char ascii[128];
    for (unsigned i = 0; i < 128; ++i) ascii[i] = (unsigned char)i;
    struct string *source = make(ascii, sizeof ascii);
    if (argc == 3) {
        source->points = strtoll(argv[1], NULL, 10);
        trbn_string_index(source, strtoll(argv[2], NULL, 10));
        return 1;
    }
    assert(argc == 1);
    struct string *retained[128];
    for (int i = 0; i < 128; ++i) {
        retained[i] = trbn_string_index(source, i);
        assert(retained[i] == trbn_string_index(source, i - 128));
    }
    memset(source->bytes, 255, 128); free(source);
    for (int i = 0; i < 128; ++i) {
        assert(retained[i]->length == 1 && retained[i]->points == 1);
        assert(retained[i]->bytes[0] == i && retained[i]->bytes[1] == 0);
        assert(retained[i]->descriptor == 0);
    }
    assert(allocations == 0);
    const unsigned char unicode[] = "A\xc2\xa2\xe3\x81\x82\xf0\x9f\x98\x80";
    const int64_t points[] = {65, 162, 12354, 128512};
    source = make(unicode, sizeof unicode - 1);
    assert(source->length == 10 && source->points == 4);
    struct string *values[4];
    for (int i = 0; i < 4; ++i) {
        values[i] = trbn_string_index(source, i);
        struct string *negative = trbn_string_index(source, i - 4);
        assert(values[i]->points == 1 && values[i]->length == i + 1);
        assert(trbn_utf8_scalar(values[i]->bytes, values[i]->length) == points[i]);
        assert(negative->length == values[i]->length);
        assert(!memcmp(negative->bytes, values[i]->bytes, values[i]->length + 1));
        if (i) free(negative);
    }
    assert(allocations == 6);
    struct string *slice = trbn_source_slice(source, 1, 4);
    assert(slice->length == 9 && slice->points == 3);
    assert(!memcmp(slice->bytes, unicode + 1, 10)); free(slice);
    memset(source->bytes, 0, source->length); free(source);
    for (int i = 0; i < 4; ++i) {
        assert(values[i]->bytes[values[i]->length] == 0);
        assert(trbn_utf8_scalar(values[i]->bytes, values[i]->length) == points[i]);
        if (i) free(values[i]);
    }
    const int64_t boundaries[] = {0, 127, 128, 2047, 2048, 55295, 57344, 65535, 65536, 1114111,
                                  -1, 55296, 57343, 1114112};
    for (unsigned i = 0; i < sizeof boundaries / sizeof boundaries[0]; ++i) {
        int64_t expected = i < 10 ? boundaries[i] : 65533;
        struct string *value = trbn_string_from_codepoint(boundaries[i]);
        assert(value->points == 1 && value->bytes[value->length] == 0);
        assert(trbn_utf8_count(value->bytes, value->length) == 1);
        assert(trbn_utf8_scalar(value->bytes, value->length) == expected);
        free(value);
    }
    const unsigned char *invalid[] = {(const unsigned char *)"\x80", (const unsigned char *)"\xc0\xaf",
        (const unsigned char *)"\xed\xa0\x80", (const unsigned char *)"\xf4\x90\x80\x80",
        (const unsigned char *)"\xe3\x81", (const unsigned char *)"\xf0\x90\x80"};
    for (unsigned i = 0; i < sizeof invalid / sizeof invalid[0]; ++i) {
        size_t length = strlen((const char *)invalid[i]);
        source = make(invalid[i], length);
        assert(source->points == (int64_t)length);
        struct string *value = trbn_string_index(source, 0);
        assert(value->length == 3 && value->points == 1);
        assert(!memcmp(value->bytes, "\xef\xbf\xbd", 4));
        free(value); free(source);
    }
    unsigned before_queries = allocations;
    source = make((const unsigned char *)"ababa", 5);
    expect_query(source, (const unsigned char *)"aba", 3, 0, 2, 0, 0, 0);
    expect_query(source, (const unsigned char *)"", 0, 0, 5, 0, 0, 0);
    expect_query(source, (const unsigned char *)"ababab", 6, -1, -1, -1, -1, -1);
    free(source);
    source = make((const unsigned char *)"a\0ba\0", 5);
    expect_query(source, (const unsigned char *)"a\0", 2, 0, 3, 0, 0, 0);
    free(source);
    source = make((const unsigned char *)"\xc2\xa2", 2);
    expect_query(source, (const unsigned char *)"\xa2", 1, -1, -1, -1, 0, 0);
    free(source);
    /* These Strings have no terminator: the first byte beyond the stored length
       is inaccessible, for both the receiver and the pattern. */
    struct guarded value = guard((const unsigned char *)"ab\xf0\x9f\x98\x80" "cd", 8);
    expect_query(value.value, (const unsigned char *)"\xf0\x9f\x98\x80", 4, 2, 2, -1, -1, 0);
    expect_query(value.value, (const unsigned char *)"cd", 2, 3, 3, -1, 0, 0);
    expect_query(value.value, (const unsigned char *)"ce", 2, -1, -1, -1, -1, -1);
    for (int mode = 0; mode < 5; ++mode) assert(trbn_string_query(value.value, value.value, mode) == 0);
    struct guarded invalid_value = guard((const unsigned char *)"abcdef\xe3\x81", 8);
    expect_query(invalid_value.value, (const unsigned char *)"\xef\xbf\xbd", 3, 6, 7, -1, -1, -1);
    expect_query(invalid_value.value, (const unsigned char *)"\xe3\x81", 2, 6, 6, -1, 0, 0);
    struct guarded empty = guard((const unsigned char *)"", 0);
    for (int mode = 0; mode < 5; ++mode) {
        assert(trbn_string_query(empty.value, empty.value, mode) == 0);
        assert(trbn_string_query(empty.value, value.value, mode) == -1);
        assert(trbn_string_query(value.value, empty.value, mode) == (mode == 1 ? 5 : 0));
    }
    assert(munmap(value.region, value.size) == 0);
    assert(munmap(invalid_value.region, invalid_value.size) == 0);
    assert(munmap(empty.region, empty.size) == 0);
    assert(allocations == before_queries);
    puts("String indexing, Unicode lifetime, allocation-free queries and guarded bounds passed");
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
    assert good.stdout == b'String indexing, Unicode lifetime, allocation-free queries and guarded bounds passed\n', good
    observations.append({'case': 'ascii-cache', 'reads': 256, 'allocations': 0})
    observations.append({'case': 'string-queries', 'modes': 5, 'allocations': 0,
                         'controls': ['overlap', 'nul', 'invalid-utf8', 'guarded-spans', 'empty', 'oversized']})
    for length, index in [(0, 0), (0, -1), (128, -129), (128, 128), (128, -9007199254740991), (128, 9007199254740991)]:
        result = subprocess.run([str(root / 'probe'), str(length), str(index)], capture_output=True, timeout=10)
        assert result.returncode == 70 and result.stdout == b'', result
        assert result.stderr == b'panic: index is out of bounds\n', result
        observations.append({'case': 'required-bounds-failure', 'length': length, 'index': index})
report = {'sourceSha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'helpersSha256': hashlib.sha256(helpers.read_bytes()).hexdigest(), 'queriesSha256': hashlib.sha256(queries.read_bytes()).hexdigest(), 'runtimeSha256': hashlib.sha256(il.encode()).hexdigest(), 'observations': observations}
if args.output:
    args.output.write_text(json.dumps(report, indent=2) + '\n')
print('String indexing and queries: ASCII cache, UTF-8, zero-allocation queries, guarded spans and 6 bounds failures passed')
