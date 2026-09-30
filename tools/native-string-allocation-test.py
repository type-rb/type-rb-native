#!/usr/bin/env python3
"""Check managed initialization with poisoned allocation and real String helpers."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--qbe', type=Path, required=True)
args = parser.parse_args()
repo = Path(__file__).resolve().parent.parent
sources = [repo / 'compiler/src/backend/qbe/runtime/system.trb',
           repo / 'compiler/src/backend/qbe/emit/strings.trb']
decoded = '\n'.join(json.loads(s) for source in sources
                    for s in re.findall(r'"(?:[^"\\]|\\.)*"', source.read_text()))
names = ['trbn_gc_alloc', 'trbn_string_alloc', 'trbn_string_from_bytes',
         'trbn_string_concat', 'trbn_integer_to_string', 'trbn_string_from_codepoint',
         'trbn_utf8_width', 'trbn_utf8_count']
bodies = []
for name in names:
    matches = re.findall(r'^function l \$' + name + r'\([^\n]*\) \{.*?^\}', decoded, re.M | re.S)
    assert len(matches) == 1, name
    bodies.append('export ' + matches[0].replace('call $malloc(', 'call $poison_malloc('))
error = re.findall(r'^data \$trbn_allocation_error = [^\n]+', decoded, re.M)
assert len(error) == 1
il = 'export ' + error[0] + '\n' + '\n'.join(bodies)
observer = r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
struct string { uintptr_t descriptor; int64_t length, points; unsigned char bytes[]; };
extern void *trbn_gc_alloc(void *, int64_t, int64_t);
extern struct string *trbn_string_from_bytes(const void *, int64_t);
extern struct string *trbn_string_concat(struct string *, struct string *);
extern struct string *trbn_integer_to_string(int64_t);
extern struct string *trbn_string_from_codepoint(int64_t);
int64_t trbn_desc_string[3], other_descriptor[3];
void *trbn_gc_heap;
int64_t trbn_gc_heap_bytes, trbn_gc_allocated_bytes;

static int64_t projected, peak, published;
static int fail_allocation;
void *poison_malloc(size_t size) {
    if (fail_allocation) return NULL;
    void *p = malloc(size); assert(p); memset(p, 0xa5, size); return p;
}
void trbn_gc_maybe_collect(int64_t size) { projected = size; }
void trbn_gc_update_peak(int64_t size) { if (peak < size) peak = size; }
void trbn_gc_temp_push(struct string *s) {
    /* Publication must see the valid initialized header, even before the
       constructor fills the immutable bytes. It must also see accounting. */
    assert((unsigned char *)s == (unsigned char *)trbn_gc_heap + 8);
    assert(peak == trbn_gc_heap_bytes);
    if (s->descriptor == (uintptr_t)trbn_desc_string)
        assert(s->length == 0 && s->points == 0);
    ++published;
}
void trbn_fail(const void *message, int64_t size) {
    const char expected[] = "panic: allocation failed\n";
    assert(size == 26 && !memcmp(message, expected, sizeof expected - 1));
    fputs(expected, stderr); exit(70);
}
static void clear(void) {
    while (trbn_gc_heap) {
        void *next = *(void **)trbn_gc_heap; free(trbn_gc_heap); trbn_gc_heap = next;
    }
    trbn_gc_heap_bytes = trbn_gc_allocated_bytes = peak = published = 0;
}
static void expect(struct string *s, const void *bytes, size_t size, int64_t points) {
    assert(s->descriptor == (uintptr_t)trbn_desc_string);
    assert(s->length == (int64_t)size && s->points == points);
    assert(!memcmp(s->bytes, bytes, size) && s->bytes[size] == 0);
}
int main(int argc, char **argv) {
    if (argc > 1) {
        fail_allocation = 1;
        trbn_gc_alloc(argv[1][0] == 's' ? trbn_desc_string : other_descriptor, 17, 0);
        return 1;
    }
    for (int64_t size = 0; size <= 4096; ++size) {
        unsigned char *object = trbn_gc_alloc(other_descriptor, size, 31);
        assert(*(uintptr_t *)object == (uintptr_t)other_descriptor);
        for (int64_t i = 0; i < size; ++i) assert(object[8 + i] == 0);
        assert(projected == size + 16 + 31);
        assert(trbn_gc_heap_bytes == size + 16);
        assert(trbn_gc_allocated_bytes == size + 16 && published == 1);
        clear();
    }
    /* A managed String keeps a zero header but its bytes remain owned by its
       constructor. This distinguishes the optimized path from blanket clearing. */
    for (int64_t size = 17; size <= 4096; ++size) {
        unsigned char *object = trbn_gc_alloc(trbn_desc_string, size, 0);
        for (int64_t i = 0; i < 16; ++i) assert(object[8 + i] == 0);
        for (int64_t i = 16; i < size; ++i) assert(object[8 + i] == 0xa5);
        assert(projected == size + 16 && trbn_gc_allocated_bytes == size + 16);
        clear();
    }
    unsigned char bytes[256];
    for (unsigned i = 0; i < 256; ++i) bytes[i] = i;
    for (int64_t size = 0; size <= 256; ++size) {
        /* Ascending byte values contain no valid multi-byte sequence. */
        struct string *s = trbn_string_from_bytes(bytes, size);
        expect(s, bytes, size, size);
        assert(trbn_gc_allocated_bytes == size + 33);
        clear();
    }
    const unsigned char left[] = {0xe3, 0x81}, right[] = {0x82, 0, 'a'};
    struct string *a = trbn_string_from_bytes(left, sizeof left);
    struct string *b = trbn_string_from_bytes(right, sizeof right);
    struct string *empty = trbn_string_from_bytes("", 0);
    expect(a, left, sizeof left, 2); expect(b, right, sizeof right, 3);
    expect(trbn_string_concat(a, b), "\xe3\x81\x82\0a", 5, 3);
    assert(trbn_string_concat(empty, a) == a && trbn_string_concat(b, empty) == b);
    clear();
    int64_t values[] = {-9007199254740991LL, -123, 0, 9, 123, 9007199254740991LL};
    for (unsigned i = 0; i < sizeof values / sizeof *values; ++i) {
        char buffer[32]; int size = snprintf(buffer, sizeof buffer, "%lld", (long long)values[i]);
        expect(trbn_integer_to_string(values[i]), buffer, size, size); clear();
    }
    expect(trbn_string_from_codepoint(0), "\0", 1, 1);
    expect(trbn_string_from_codepoint(0x7ff), "\xdf\xbf", 2, 1);
    expect(trbn_string_from_codepoint(0x3042), "\xe3\x81\x82", 3, 1);
    expect(trbn_string_from_codepoint(0x10ffff), "\xf4\x8f\xbf\xbf", 4, 1);
    expect(trbn_string_from_codepoint(0xd800), "\xef\xbf\xbd", 3, 1);
    clear();
    puts("Managed initialization and poisoned String construction passed");
    return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='native-string-allocation-') as temporary:
    root = Path(temporary)
    (root / 'runtime.ssa').write_text(il)
    (root / 'observer.c').write_text(observer)
    subprocess.run([str(args.qbe.resolve()), '-o', str(root / 'runtime.s'), str(root / 'runtime.ssa')],
                   check=True, capture_output=True, timeout=30)
    subprocess.run(['/usr/bin/cc', '-O2', str(root / 'runtime.s'), str(root / 'observer.c'),
                    '-o', str(root / 'probe')], check=True, capture_output=True, timeout=30)
    result = subprocess.run([str(root / 'probe')], capture_output=True, timeout=30)
    assert result.returncode == 0 and result.stderr == b'', result
    for descriptor in ['string', 'other']:
        failure = subprocess.run([str(root / 'probe'), descriptor], capture_output=True, timeout=10)
        assert failure.returncode == 70 and failure.stdout == b'', failure
        assert failure.stderr == b'panic: allocation failed\n', failure
print('Managed initialization, poisoned String constructors and allocation failures passed')
