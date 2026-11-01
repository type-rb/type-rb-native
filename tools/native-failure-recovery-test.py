#!/usr/bin/env python3
"""Qualify the private recovery trampoline against the host libc and callback ABI."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--qbe', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
runtime = root / 'compiler/src/backend/qbe/runtime'
def decoded(path):
    return '\n'.join(json.loads(s) for s in re.findall(r'"(?:[^"\\]|\\.)*"', path.read_text()))
# Include the same cleanup dependency as the production recovery emitter.
il = decoded(runtime / 'resource_cleanup.trb') + '\n' + decoded(runtime / 'failure_recovery.trb')
fatal = re.findall(r'^function \$trbn_fatal\([^\n]*\) \{.*?^\}', decoded(runtime / 'system.trb'), re.M | re.S)
assert len(fatal) == 1
il += '\n' + fatal[0]
il = re.sub(r'^(function|data) ', r'export \1 ', il, flags=re.M)
observer = r'''
#include <assert.h>
#include <errno.h>
#include <fcntl.h>
#include <setjmp.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
_Static_assert(sizeof(jmp_buf) <= 1024, "recovery jump environment capacity");
_Static_assert(_Alignof(jmp_buf) <= 16, "recovery jump environment alignment");
_Static_assert(sizeof(void *) == 8, "recovery pointer ABI");
int64_t trbn_gc_temp_count = 7;
extern uintptr_t trbn_recovery_scope;
extern uintptr_t trbn_resource_scope;
extern void trbn_resource_push(void *, int);
extern int trbn_resource_close(void *);
extern int64_t trbn_runtime_recover_l(void *, int64_t);
extern double trbn_runtime_recover_d(void *, double);
extern void trbn_fail(const void *, int64_t);
extern void trbn_fatal(const void *, int64_t);
struct closure { uintptr_t descriptor; int64_t (*code)(void *); int64_t captured; };
struct float_closure { uintptr_t descriptor; double (*code)(void *); double captured; };
struct resource_scope { uintptr_t previous; int descriptor; int kind; };
typedef void (*failure_notice)(uintptr_t, const void *, int64_t, int64_t, uintptr_t, int64_t, int64_t);
struct recovery_frame {
    uintptr_t previous;
    int64_t roots;
    uintptr_t context;
    uintptr_t action;
    unsigned char environment[1024];
    uintptr_t resources;
    failure_notice notice;
};
_Static_assert(offsetof(struct closure, code) == 8, "closure code offset");
_Static_assert(sizeof(struct resource_scope) == 16, "file cleanup frame size");
_Static_assert(offsetof(struct resource_scope, descriptor) == 8, "cleanup descriptor offset");
_Static_assert(offsetof(struct resource_scope, kind) == 12, "cleanup kind offset");
_Static_assert(offsetof(struct recovery_frame, environment) == 32, "jump environment offset");
_Static_assert(offsetof(struct recovery_frame, resources) == 1056, "recovery cleanup offset");
_Static_assert(offsetof(struct recovery_frame, notice) == 1064, "optional notice offset");
_Static_assert(sizeof(struct recovery_frame) == 1072, "recovery frame size");
static int side_effects;
static int failed_descriptor;
static int notices;
static int push_pipe(struct resource_scope *scope) {
    int descriptors[2];
    assert(pipe(descriptors) == 0);
    assert(close(descriptors[1]) == 0);
    trbn_resource_push(scope, descriptors[0]);
    assert(trbn_resource_scope == (uintptr_t)scope);
    return descriptors[0];
}
static void expect_closed(int descriptor) {
    errno = 0;
    assert(fcntl(descriptor, F_GETFD) == -1 && errno == EBADF);
}
static int64_t failed(void *value) {
    struct closure *closure = value;
    struct resource_scope scope;
    failed_descriptor = push_pipe(&scope);
    side_effects += (int)closure->captured;
    trbn_gc_temp_count = 500;
    trbn_fail("synthetic failure\n", 18);
    assert(0); return -1;
}
static int64_t fatal_failure(void *value) {
    (void)value;
    trbn_fatal("fatal failure\n", 14);
    assert(0); return -1;
}
static int64_t nested(void *value) {
    struct closure *closure = value;
    struct resource_scope scope;
    int outer_descriptor = push_pipe(&scope);
    struct closure child = {0, failed, 1};
    int64_t result = trbn_runtime_recover_l(&child, 41);
    assert(trbn_gc_temp_count == 7 && trbn_recovery_scope != 0);
    expect_closed(failed_descriptor);
    assert(trbn_resource_scope == (uintptr_t)&scope);
    assert(fcntl(outer_descriptor, F_GETFD) >= 0);
    assert(trbn_resource_close(&scope) == 0);
    expect_closed(outer_descriptor);
    return result + closure->captured;
}
static double success_float(void *value) {
    return ((struct float_closure *)value)->captured;
}
static double failed_float(void *value) {
    (void)value;
    struct resource_scope scope;
    failed_descriptor = push_pipe(&scope);
    trbn_fail("float failure\n", 14);
    assert(0); return -1;
}
static void notified(uintptr_t context, const void *message, int64_t size,
                     int64_t raw, uintptr_t path, int64_t line, int64_t column) {
    assert(context == 77 && raw == 1 && path == 0 && line == 0 && column == 0);
    assert(size == 18 && !memcmp(message, "synthetic failure\n", 18));
    /* Notification happens before cleanup and can still inspect the live frame. */
    assert(trbn_resource_scope != 0 && fcntl(failed_descriptor, F_GETFD) >= 0);
    ++notices;
}
static int64_t notifying(void *value) {
    struct recovery_frame *frame = (void *)trbn_recovery_scope;
    assert(frame && frame->notice == NULL);
    frame->notice = notified;
    struct closure child = {0, failed, 0};
    int before = notices;
    assert(trbn_runtime_recover_l(&child, 41) == 41);
    assert(notices == before); /* The nearer ordinary frame suppresses notices. */
    struct float_closure floating = {0, failed_float, 0};
    assert(trbn_runtime_recover_d(&floating, 9.5) == 9.5);
    assert(notices == before);
    return failed(value);
}
int main(int argc, char **argv) {
    if (argc > 1) {
        if (!strcmp(argv[1], "outside")) {
            trbn_fail("outside failure\n", 16);
        } else {
            struct closure fatal = {0, fatal_failure, 0};
            trbn_runtime_recover_l(&fatal, 99);
        }
        return 90;
    }
    struct closure outer = {0, nested, 1};
    struct float_closure good = {0, success_float, 2.5};
    struct float_closure bad = {0, failed_float, 0};
    struct closure notice = {0, notifying, 0};
    for (int i = 0; i < 10000; ++i) {
        assert(trbn_runtime_recover_l(&outer, 99) == 42);
        assert(trbn_runtime_recover_d(&good, 9.5) == 2.5);
        assert(trbn_runtime_recover_d(&bad, 9.5) == 9.5);
        expect_closed(failed_descriptor);
        assert(trbn_gc_temp_count == 7 && trbn_recovery_scope == 0);
        assert(trbn_resource_scope == 0);
        assert(trbn_runtime_recover_l(&notice, 77) == 77);
        expect_closed(failed_descriptor);
        assert(notices == i + 1 && trbn_gc_temp_count == 7);
        assert(trbn_recovery_scope == 0 && trbn_resource_scope == 0);
    }
    assert(side_effects == 10000);
    printf("recovery ABI: jmp_buf=%zu alignment=%zu; 10000 nested/Float/resource/notice cycles\n",
        sizeof(jmp_buf), _Alignof(jmp_buf));
}
'''
with tempfile.TemporaryDirectory(prefix='native-recovery-abi-') as temporary:
    work = Path(temporary)
    (work / 'runtime.ssa').write_text(il + '\n')
    (work / 'observer.c').write_text(observer)
    subprocess.run([str(args.qbe.resolve()), '-o', str(work / 'runtime.s'), str(work / 'runtime.ssa')], check=True)
    subprocess.run(['cc', '-std=c11', '-O2', str(work / 'observer.c'), str(work / 'runtime.s'), '-o', str(work / 'probe')], check=True)
    for mode, code, error in [([], 0, ''), (['outside'], 2, 'outside failure\n'), (['fatal'], 2, 'fatal failure\n')]:
        result = subprocess.run([str(work / 'probe'), *mode], capture_output=True, text=True, timeout=30)
        assert result.returncode == code and result.stderr == error, result
        if not mode:
            print(result.stdout, end='')
        else:
            assert not result.stdout, result
print('Out-of-scope and process-fatal failures remain terminal')
