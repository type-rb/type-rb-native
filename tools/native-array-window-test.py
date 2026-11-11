#!/usr/bin/env python3
"""Check generated Array growth under moving realloc, OOM and overflow."""
import argparse
import os
from pathlib import Path
import re
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('binary', type=Path)
binary = parser.parse_args().binary.resolve()

HARNESS = r'''
#include <assert.h>
#include <setjmp.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

typedef struct { uint64_t descriptor, length, capacity, *data, *base; } Array;
uint64_t trbn_gc_heap_bytes, trbn_gc_allocated_bytes;
const char trbn_allocation_error[] = "allocation";
const char trbn_array_empty_error[] = "empty";
static size_t allocation_bytes, collections, reallocations, live_allocations;
static int fail_realloc;
static jmp_buf failure;
extern void trbn_array_push(Array *, uint64_t);
extern void trbn_array_push_paced(Array *, uint64_t);
extern void trbn_array_push_d(Array *, double);
extern void trbn_array_unshift(Array *, uint64_t);
extern uint64_t trbn_array_remove(Array *, int);
extern void *trbn_array_make_room(Array *, uint64_t, uint64_t, uint64_t, int);
void trbn_gc_maybe_collect(uint64_t growth) { assert(growth > 0); ++collections; }
void trbn_gc_update_peak(uint64_t bytes) { assert(bytes == trbn_gc_heap_bytes); }
void trbn_fatal(const char *message, uint64_t length) {
    (void)length; assert(message == trbn_allocation_error); longjmp(failure, 1);
}
void trbn_fail(const char *message, uint64_t length) {
    (void)length; assert(message == trbn_array_empty_error); longjmp(failure, 2);
}
void *moving_realloc(void *old, size_t bytes) {
    ++reallocations;
    if (fail_realloc) return NULL;
    assert(bytes > allocation_bytes);
    void *fresh = malloc(bytes);
    assert(fresh && fresh != old);
    memset(fresh, 0xcd, bytes);
    memcpy(fresh, old, allocation_bytes);
    free(old);
    allocation_bytes = bytes;
    return fresh;
}
static Array create(void) {
    allocation_bytes = 32;
    uint64_t *base = calloc(4, 8);
    assert(base);
    ++live_allocations;
    trbn_gc_heap_bytes = trbn_gc_allocated_bytes = allocation_bytes;
    return (Array){0, 0, 4, base, base};
}
static void inspect(Array *a) {
    assert(a->base && a->data >= a->base);
    size_t prefix = a->data - a->base;
    assert((prefix + a->capacity) * 8 == allocation_bytes);
    assert(a->length <= a->capacity);
    assert(trbn_gc_heap_bytes == allocation_bytes);
    for (size_t i = 0; i < prefix; ++i) assert(a->base[i] == 0);
}
static void destroy(Array *a) { inspect(a); free(a->base); --live_allocations; }
int main(void) {
    Array a = create();
    for (uint64_t i = 0; i < 4; ++i) trbn_array_push_paced(&a, i);
    size_t moves = reallocations;
    for (uint64_t i = 0; i < 1000; ++i) {
        assert(trbn_array_remove(&a, 2) == i);
        inspect(&a);
        trbn_array_push_paced(&a, i + 4);
        inspect(&a);
        assert(a.data[0] == i + 1 && a.data[3] == i + 4);
    }
    /* The first small-prefix push grows; subsequent FIFO cycles compact. */
    assert(reallocations == moves + 1);
    uint64_t *before = a.data;
    assert(trbn_array_remove(&a, 2) == 1000);
    trbn_array_unshift(&a, 1000);
    assert(a.data == before && a.length == 4);
    for (uint64_t i = 1004; i < 1100; ++i) trbn_array_push_paced(&a, i);
    for (uint64_t i = 1000; i < 1100; ++i) assert(trbn_array_remove(&a, 2) == i);
    inspect(&a); assert(a.data == a.base && a.length == 0);
    trbn_array_unshift(&a, 42);
    assert(trbn_array_remove(&a, 1) == 42);
    assert(a.data == a.base);
    int empty = setjmp(failure);
    if (!empty) { trbn_array_remove(&a, 2); abort(); }
    assert(empty == 2);
    destroy(&a);

    a = create();
    size_t before_collections = collections;
    for (uint64_t i = 0; i < 5; ++i) trbn_array_push(&a, i);
    assert(a.data == a.base && a.capacity == 8);
    assert(collections == before_collections);
    inspect(&a); destroy(&a);

    a = create();
    uint64_t bits[] = {UINT64_C(0x8000000000000000), UINT64_C(0x7ff8000000001234),
                       UINT64_C(0x7ff0000000000000), UINT64_C(0x3ff4000000000000)};
    for (int i = 0; i < 4; ++i) {
        double value; memcpy(&value, &bits[i], 8); trbn_array_push_d(&a, value);
    }
    assert(trbn_array_remove(&a, 2) == bits[0]);
    double value; memcpy(&value, &bits[0], 8); trbn_array_push_d(&a, value);
    for (int i = 1; i < 4; ++i) assert(trbn_array_remove(&a, 2) == bits[i]);
    assert(trbn_array_remove(&a, 2) == bits[0]);
    destroy(&a);

    a = create();
    for (uint64_t i = 0; i < 4; ++i) trbn_array_push_paced(&a, i);
    assert(trbn_array_remove(&a, 2) == 0);
    fail_realloc = 1;
    int oom = setjmp(failure);
    if (!oom) { trbn_array_push_paced(&a, 4); abort(); }
    assert(oom == 1 && a.length == 3 && a.data[0] == 1);
    inspect(&a); fail_realloc = 0;
    size_t calls = reallocations, collects = collections;
    int overflow = setjmp(failure);
    if (!overflow) {
        trbn_array_make_room(&a, UINT64_C(288230376151711744),
                            UINT64_C(288230376151711744), 2, 1);
        abort();
    }
    assert(overflow == 1 && reallocations == calls && collections == collects);
    destroy(&a);
    assert(live_allocations == 0);
    return 0;
}
'''

with tempfile.TemporaryDirectory(prefix='native-array-window-') as temporary:
    root = Path(temporary)
    env = dict(os.environ, NO_COLOR='1', TERM='dumb')

    def run(args):
        result = subprocess.run(list(map(str, args)), cwd=root, env=env,
                                capture_output=True, text=True, timeout=60)
        assert result.returncode == 0, (args, result.stdout, result.stderr)
        return result

    source = root / 'main.trb'
    source.write_text('def main()\nmut values := [1.0]\nvalues.push(2.0)\nvalues.unshift(0.0)\nvalues.shift()\nend\n')
    generated = run([binary, '--internal-driver', 'emit-qbe', source]).stdout
    names = ['push', 'make_room', 'push_paced', 'grow_paced', 'push_d', 'unshift', 'remove']
    functions = []
    for name in names:
        pattern = r'function (?:[lwd] )?\$trbn_array_' + name + r'\([^\n]*\) \{\n.*?\n}'
        matches = re.findall(pattern, generated, re.S)
        assert len(matches) == 1, name
        functions.append('export ' + matches[0].replace('call $realloc(', 'call $moving_realloc('))
    il, assembly, c, executable = [root / p for p in ['test.ssa', 'test.s', 'test.c', 'test']]
    il.write_text('\n\n'.join(functions) + '\n')
    c.write_text(HARNESS)
    run([binary.with_name('qbe'), '-o', assembly, il])
    run(['/usr/bin/cc', '-O2', '-Wall', '-Wextra', '-Werror', assembly, c, '-o', executable])
    assert run([executable]).stderr == ''
print('Array window moving realloc, amortization, bit preservation, OOM and overflow passed')
