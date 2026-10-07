#!/usr/bin/env python3
"""Probe the real raw storage runtime with guarded backing allocations.

QBE loads/stores are not sanitizer-instrumented. These checks independently
validate live bytes, owner prefixes, backing bounds and immediate page release.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--qbe', type=Path, required=True)
args = parser.parse_args()
source = Path(__file__).resolve().parent.parent / 'compiler/src/backend/qbe/runtime/managed_storage.trb'
decoded = '\n'.join(json.loads(s) for s in re.findall(r'"(?:[^"\\]|\\.)*"', source.read_text()))
data = re.findall(r'^data \$trbn_storage_available = [^\n]+', decoded, re.M)
assert len(data) == 1
bodies = ['export ' + data[0]]
for name in ['trbn_storage_alloc', 'trbn_storage_free', 'trbn_storage_insert', 'trbn_storage_unlink',
             'trbn_array_buffer_new', 'trbn_array_buffer_free', 'trbn_array_buffer_grow']:
    matches = re.findall(r'^function (?:l )?\$' + name + r'\([^\n]*\) \{.*?^\}', decoded, re.M | re.S)
    assert len(matches) == 1, name
    bodies.append('export ' + matches[0].replace('call $malloc(', 'call $guard_malloc(')
                  .replace('call $free(', 'call $guard_free(')
                  .replace('call $calloc(', 'call $guard_calloc(')
                  .replace('call $realloc(', 'call $guard_realloc('))
observer = r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
extern void *trbn_storage_alloc(int64_t);
extern void trbn_storage_free(void *, int64_t);
extern uintptr_t trbn_storage_available[7];
extern void *trbn_array_buffer_new(int64_t);
extern void trbn_array_buffer_free(void *, int64_t);
extern void *trbn_array_buffer_grow(void *, int64_t, int64_t);
#define LIMIT 2048
struct block { unsigned char *base; size_t size; };
struct object { unsigned char *base; size_t size; unsigned char pattern; };
static struct block blocks[LIMIT];
static struct object objects[LIMIT];
static size_t allocations, releases, last_request;
static int fail_allocation;
static int small(size_t n) { return n >= 16 && n <= 64; }
static void guard(struct block *b) {
    for (unsigned i = 0; i < 32; ++i) {
        assert(b->base[-32 + (int)i] == 0xd7);
        assert(b->base[b->size + i] == 0xd7);
    }
}
void *guard_malloc(size_t size) {
    last_request = size;
    if (fail_allocation) return NULL;
    assert(size <= 8192);
    unsigned char *raw = malloc(size + 64); assert(raw);
    memset(raw, 0xd7, size + 64); memset(raw + 32, 0xa5, size);
    for (unsigned i = 0; i < LIMIT; ++i) if (!blocks[i].base) {
        blocks[i] = (struct block){raw + 32, size}; ++allocations;
        return raw + 32;
    }
    abort();
}
void guard_free(void *pointer) {
    for (unsigned i = 0; i < LIMIT; ++i) if (blocks[i].base == pointer) {
        guard(&blocks[i]);
        memset(blocks[i].base, 0xdd, blocks[i].size);
        free(blocks[i].base - 32); blocks[i].base = NULL; ++releases;
        return;
    }
    abort(); /* Reject an interior, stale or duplicate system free. */
}
static size_t calloc_count, calloc_size, reallocations;
void *guard_calloc(size_t count, size_t size) {
    calloc_count = count; calloc_size = size;
    if (size && count > SIZE_MAX / size) return NULL;
    void *p = guard_malloc(count * size);
    if (p) memset(p, 0, count * size);
    return p;
}
void *guard_realloc(void *pointer, size_t size) {
    ++reallocations;
    for (unsigned i = 0; i < LIMIT; ++i) if (blocks[i].base == pointer) {
        size_t old = blocks[i].size;
        guard(&blocks[i]);
        void *p = guard_malloc(size);
        if (!p) return NULL;
        memcpy(p, pointer, old < size ? old : size);
        guard_free(pointer);
        return p;
    }
    abort(); /* A pooled interior pointer must never reach system realloc. */
}
static void check_object(struct object *o) {
    assert((uintptr_t)o->base % 8 == 0);
    for (size_t i = 0; i < o->size; ++i) assert(o->base[i] == o->pattern);
    if (small(o->size))
        for (size_t i = o->size; i < ((o->size + 7) & ~(size_t)7); ++i)
            assert(o->base[i] == 0xe9);
}
static void put(unsigned index, size_t size) {
    assert(!objects[index].base);
    unsigned char *base = trbn_storage_alloc(size); assert(base);
    for (unsigned i = 0; i < LIMIT; ++i) if (objects[i].base) {
        uintptr_t a = (uintptr_t)objects[i].base, b = (uintptr_t)base;
        assert(a + objects[i].size <= b || b + size <= a);
    }
    unsigned char pattern = (unsigned char)(index % 251 + 1);
    objects[index] = (struct object){base, size, pattern};
    memset(base, pattern, size);
    if (small(size)) memset(base + size, 0xe9, ((size + 7) & ~(size_t)7) - size);
    check_object(&objects[index]);
}
static void drop(unsigned index) {
    struct object *o = &objects[index]; assert(o->base); check_object(o);
    trbn_storage_free(o->base, o->size); o->base = NULL;
}
static void check(void) {
    unsigned live_blocks = 0;
    for (unsigned i = 0; i < LIMIT; ++i) if (objects[i].base) check_object(&objects[i]);
    for (unsigned b = 0; b < LIMIT; ++b) if (blocks[b].base) {
        struct block *block = &blocks[b]; guard(block); ++live_blocks;
        unsigned live = 0, direct = 0;
        size_t stride = 0;
        for (unsigned i = 0; i < LIMIT; ++i) if (objects[i].base) {
            struct object *o = &objects[i];
            if (!small(o->size)) {
                if (o->base == block->base) { assert(o->size == block->size); ++direct; }
                continue;
            }
            uintptr_t owner = ((uintptr_t *)o->base)[-1];
            if (owner != (uintptr_t)block->base) continue;
            size_t expected_stride = ((o->size + 7) & ~(size_t)7) + 8;
            assert(!stride || stride == expected_stride); stride = expected_stride;
            uintptr_t cell = (uintptr_t)o->base - 8;
            assert(cell >= owner + 64 && cell + stride <= owner + 4096);
            assert((cell - owner - 64) % stride == 0);
            ++live;
        }
        assert((live != 0) != (direct != 0)); /* No retained empty pages. */
        if (direct) { assert(direct == 1); continue; }
        assert(block->size == 4096);
        uintptr_t *page = (uintptr_t *)block->base;
        size_t capacity = 4032 / stride;
        assert(page[4] == capacity && page[5] == live && page[6] == stride);
        assert(page[3] >= (uintptr_t)page + 64);
        assert(page[3] <= (uintptr_t)page + 64 + capacity * stride);
        assert((page[3] - (uintptr_t)page - 64) % stride == 0);
        unsigned class_index = (unsigned)(stride / 8 - 3);
        assert(class_index < 7 && page[7] == (uintptr_t)&trbn_storage_available[class_index]);
        unsigned found = 0, traversed = 0;
        uintptr_t previous = 0;
        for (uintptr_t cursor = trbn_storage_available[class_index]; cursor;) {
            assert(++traversed < LIMIT);
            uintptr_t *entry = (uintptr_t *)cursor;
            assert(entry[1] == previous && entry[5] > 0 && entry[5] < entry[4]);
            if (cursor == (uintptr_t)page) ++found;
            previous = cursor; cursor = entry[0];
        }
        assert(found == (live < capacity));
    }
    assert(allocations - releases == live_blocks);
}
static void empty(void) {
    for (unsigned i = 0; i < LIMIT; ++i) if (objects[i].base) drop(i);
    check(); assert(allocations == releases);
    for (unsigned i = 0; i < 7; ++i) assert(!trbn_storage_available[i]);
}
static void array_buffers(void) {
    for (int64_t capacity = 0; capacity <= 12; ++capacity) {
        unsigned char *p = trbn_array_buffer_new(capacity); assert(p);
        for (int64_t i = 0; i < capacity * 8; ++i) assert(p[i] == 0);
        if (capacity < 2 || capacity > 8) {
            assert(calloc_count == (size_t)capacity && calloc_size == 8);
        } else {
            uintptr_t *page = (uintptr_t *)((uintptr_t *)p)[-1];
            assert(page[5] == 1 && page[6] == (uintptr_t)(capacity * 8 + 8));
        }
        trbn_array_buffer_free(p, capacity); empty();
    }
    int64_t invalid[] = {-1, INT64_MIN, INT64_MAX, (INT64_C(1) << 61) + 4};
    for (unsigned i = 0; i < sizeof invalid / sizeof *invalid; ++i) {
        assert(!trbn_array_buffer_new(invalid[i]));
        assert(calloc_count == (size_t)invalid[i] && calloc_size == 8);
        empty(); /* Overflow must not wrap into a 32-byte pool cell. */
    }
    fail_allocation = 1;
    for (int64_t capacity = 2; capacity <= 8; ++capacity)
        assert(!trbn_array_buffer_new(capacity));
    fail_allocation = 0; empty();
    for (int64_t capacity = 1; capacity <= 12; ++capacity) {
        for (int factor = 2; factor <= 4; factor += 2) {
            unsigned char *p = trbn_array_buffer_new(capacity); assert(p);
            memset(p, 0xb6, capacity * 8);
            size_t before = allocations, freed = releases, resized = reallocations;
            fail_allocation = 1;
            assert(!trbn_array_buffer_grow(p, capacity, capacity * factor));
            assert(allocations == before && releases == freed);
            for (int64_t i = 0; i < capacity * 8; ++i) assert(p[i] == 0xb6);
            fail_allocation = 0;
            unsigned char *q = trbn_array_buffer_grow(p, capacity, capacity * factor); assert(q);
            for (int64_t i = 0; i < capacity * 8; ++i) assert(q[i] == 0xb6);
            memset(q, 0xcd, capacity * factor * 8);
            int direct = capacity > 8;
            assert(reallocations - resized == (size_t)(direct ? 2 : 0));
            trbn_array_buffer_free(q, capacity * factor); empty();
        }
    }
    /* A raw 40-byte buffer and managed 40-byte header can share one page.
       Releasing either must not invalidate the other, and recycled buffers
       must clear both stale values and the allocator free-list link. */
    put(0, 40);
    unsigned char *p = trbn_array_buffer_new(5); assert(p);
    assert(((uintptr_t *)p)[-1] == ((uintptr_t *)objects[0].base)[-1]);
    memset(p, 0xbc, 40); trbn_array_buffer_free(p, 5); check_object(&objects[0]);
    unsigned char *q = trbn_array_buffer_new(5); assert(p == q);
    for (unsigned i = 0; i < 40; ++i) assert(q[i] == 0);
    drop(0); memset(q, 0xab, 40); trbn_array_buffer_free(q, 5); empty();
    unsigned char *buffers[500];
    for (unsigned i = 0; i < 500; ++i) {
        buffers[i] = trbn_array_buffer_new(4); assert(buffers[i]);
        for (unsigned j = 0; j < 32; ++j) assert(buffers[i][j] == 0);
        memset(buffers[i], (int)(i % 251 + 1), 32);
    }
    for (unsigned i = 0; i < 500; ++i) {
        for (unsigned j = 0; j < 32; ++j) assert(buffers[i][j] == (unsigned char)(i % 251 + 1));
        trbn_array_buffer_free(buffers[i], 4);
    }
    empty();
}
int main(void) {
    /* Every byte-size boundary, three full pages plus a partial page, then
       full-to-available reuse and head/interior/last page removal. */
    for (size_t size = 16; size <= 64; ++size) {
        unsigned capacity = (unsigned)(4032 / (((size + 7) & ~(size_t)7) + 8));
        unsigned count = capacity * 3 + 1;
        size_t before = allocations;
        for (unsigned i = 0; i < count; ++i) put(i, size);
        check(); assert(allocations == before + 4);
        for (unsigned i = 0; i < count; i += 2) drop(i);
        check();
        before = allocations;
        for (unsigned i = 0; i < count; i += 2) put(i, size);
        check(); assert(allocations == before + ((count - 1) % 2 == 0)); /* Empty pages are freed. */
        for (unsigned i = capacity; i < capacity * 2; ++i) drop(i);
        check();
        for (unsigned i = 0; i < capacity; ++i) drop(i);
        check(); empty();
    }
    /* Sparse retained pages, mixed classes and large direct fallbacks. */
    for (unsigned wave = 0; wave < 8; ++wave) {
        for (unsigned i = 0; i < 1200; ++i) if (!objects[i].base)
            put(i, i % 11 == 0 ? 65 + i % 4097 : 16 + i % 49);
        check();
        for (unsigned i = 0; i < 1200; ++i) if (objects[i].base && (i + wave) % 17) drop(i);
        check();
    }
    empty();
    /* Small invalid sizes retain the direct allocation contract. Large signed
       and wrapping inputs must reach malloc unchanged, never a class index. */
    for (size_t size = 0; size < 16; ++size) { put(0, size); check(); empty(); }
    int64_t invalid[] = {-1, INT64_MIN, INT64_MAX, 65, 8192};
    fail_allocation = 1;
    for (unsigned i = 0; i < sizeof invalid / sizeof *invalid; ++i) {
        assert(!trbn_storage_alloc(invalid[i])); assert(last_request == (size_t)invalid[i]);
    }
    for (int64_t size = 16; size <= 64; ++size) {
        assert(!trbn_storage_alloc(size)); assert(last_request == 4096);
        check();
    }
    fail_allocation = 0;
    for (unsigned i = 0; i < 168; ++i) put(i, 16);
    check(); fail_allocation = 1;
    assert(!trbn_storage_alloc(16)); check();
    drop(73); put(73, 16); check(); /* Reuse needs no system allocation. */
    fail_allocation = 0; empty();
    array_buffers();
    puts("Managed storage boundaries, guarded reuse, sparse pages and failures passed");
}
'''
with tempfile.TemporaryDirectory(prefix='native-managed-storage-') as temporary:
    root = Path(temporary)
    (root / 'runtime.ssa').write_text('\n'.join(bodies))
    (root / 'observer.c').write_text(observer)
    for command in [[str(args.qbe.resolve()), '-o', str(root / 'runtime.s'), str(root / 'runtime.ssa')],
                    ['/usr/bin/cc', '-O2', str(root / 'runtime.s'), str(root / 'observer.c'), '-o', str(root / 'probe')],
                    [str(root / 'probe')]]:
        result = subprocess.run(command, capture_output=True, timeout=30)
        assert result.returncode == 0 and result.stderr == b'', result
print('Managed storage guarded allocation and lifecycle checks passed')
