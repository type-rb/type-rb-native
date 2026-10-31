#!/usr/bin/env python3
"""Exercise interfering phi classes, calls, and allocator relocation."""
import argparse
from pathlib import Path
import platform
import subprocess
import tempfile

from qbe_toolchain import ADDRESS_MOTION_PROBE


NESTED = """export function l $nested(l %rounds, l %width, l %seed) {
@start
 %initial =l and %seed, 255
 jmp @outer
@outer
 %round =l phi @start 0, @join %next_round
 %maximum =l phi @start %initial, @join %next_maximum
 %sum =l phi @start 0, @join %next_sum
 %more_rounds =w csltl %round, %rounds
 jnz %more_rounds, @flips, @done
@flips
 %count =l phi @outer 0, @increment %next_count
 %held_maximum =l phi @outer %maximum, @increment %saved_maximum
 %held_sum =l phi @outer %sum, @increment %inner_sum
 %more_flips =w csltl %count, %width
 jnz %more_flips, @inner, @choose
@inner
 %index =l phi @flips 0, @body %next_index
 %saved_count =l phi @flips %count, @body %saved_count
 %saved_maximum =l phi @flips %held_maximum, @body %saved_maximum
 %inner_sum =l phi @flips %held_sum, @body %added
 %more_inner =w csltl %index, %saved_count
 jnz %more_inner, @body, @increment
@body
 %first =l xor %saved_maximum, %saved_count
 %value =l xor %first, %index
 %observed =l call $observe(l %value)
 %added =l add %inner_sum, %observed
 %next_index =l add %index, 1
 jmp @inner
@increment
 %next_count =l add %saved_count, 1
 jmp @flips
@choose
 %larger =w csgtl %count, %held_maximum
 jnz %larger, @replace, @retain
@replace
 jmp @join
@retain
 jmp @join
@join
 %next_maximum =l phi @replace %count, @retain %held_maximum
 %next_sum =l add %held_sum, %next_maximum
 %next_round =l add %round, 1
 jmp @outer
@done
 %answer =l xor %maximum, %sum
 ret %answer
}
"""

ROTATE = """export function d $rotate(d %a, d %b, d %c, l %n) {
@start
 jmp @loop
@loop
 %index =l phi @start 0, @body %next
 %left =d phi @start %a, @body %middle
 %middle =d phi @start %b, @body %right
 %right =d phi @start %c, @body %left
 %more =w csltl %index, %n
 jnz %more, @body, @done
@body
 %next =l add %index, 1
 jmp @loop
@done
 ret %left
}
"""

DRIVER = r"""
#include <stdint.h>
#include <stdio.h>
#include <string.h>
extern uint64_t nested(int64_t, int64_t, uint64_t);
extern uint64_t address_motion(uint64_t *, uint64_t, int64_t);
extern double rotate(double, double, double, int64_t);
static uint64_t trace;
uint64_t observe(uint64_t value) {
    trace ^= value * UINT64_C(6364136223846793005) + 1;
    return (value ^ (value >> 3)) & 15;
}
static uint64_t expected(int64_t rounds, int64_t width, uint64_t seed) {
    uint64_t maximum = seed & 255, sum = 0;
    for (int64_t round = 0; round < rounds; ++round) {
        int64_t count = 0;
        for (; count < width; ++count)
            for (int64_t index = 0; index < count; ++index)
                sum += observe(maximum ^ (uint64_t)count ^ (uint64_t)index);
        if ((uint64_t)count > maximum) maximum = (uint64_t)count;
        sum += maximum;
    }
    return maximum ^ sum;
}
int main(void) {
    uint64_t seeds[] = {0, 1, 7, 255, UINT64_MAX, UINT64_C(0x8000000000000000)};
    int64_t trips[] = {-2, 0, 1, 2, 3, 7, 12};
    unsigned checks = 0;
    for (unsigned a = 0; a < 7; ++a)
    for (unsigned b = 0; b < 7; ++b)
    for (unsigned s = 0; s < 6; ++s) {
        trace = 0;
        uint64_t want = expected(trips[a], trips[b], seeds[s]);
        uint64_t want_trace = trace;
        trace = 0;
        uint64_t actual = nested(trips[a], trips[b], seeds[s]);
        if (actual != want || trace != want_trace) return 1;
        ++checks;
    }
    uint64_t data[] = {0, UINT64_MAX, 17, UINT64_C(0x8000000000000000)};
    for (unsigned i = 0; i < 4; ++i)
    for (unsigned n = 0; n < 7; ++n) {
        uint64_t count = trips[n] > 0 ? (uint64_t)trips[n] : 0;
        if (address_motion(data, i, trips[n]) != data[i] * count) return 2;
        ++checks;
    }
    uint64_t bits[] = {0, UINT64_C(0x8000000000000000), UINT64_C(0x7ff0000000000000),
                       UINT64_C(0xfff0000000000000), UINT64_C(0x7ff8000000001234), 1};
    for (unsigned a = 0; a < 6; ++a)
    for (unsigned b = 0; b < 6; ++b)
    for (unsigned c = 0; c < 6; ++c)
    for (unsigned n = 0; n < 7; ++n) {
        double values[3], actual;
        uint64_t source[] = {bits[a], bits[b], bits[c]}, result;
        memcpy(values, source, sizeof values);
        actual = rotate(values[0], values[1], values[2], trips[n]);
        memcpy(&result, &actual, sizeof result);
        unsigned slot = trips[n] > 0 ? (unsigned)trips[n] % 3 : 0;
        if (result != source[slot]) return 3;
        ++checks;
    }
    printf("phi affinity: %u independent checks passed\n", checks);
    return 0;
}
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qbe", type=Path, required=True)
    args = parser.parse_args()
    qbe = args.qbe.resolve()
    source = NESTED + ROTATE + ADDRESS_MOTION_PROBE
    with tempfile.TemporaryDirectory(prefix="qbe-affinity-test-") as temporary:
        root = Path(temporary)
        program = root / "program.ssa"
        program.write_text(source)
        for target in ("arm64", "arm64_apple", "amd64_sysv", "amd64_apple", "amd64_win", "rv64"):
            subprocess.run([str(qbe), "-t", target, "-o", str(root / (target + ".s")), str(program)], check=True)
        machine = platform.machine().lower()
        if machine in ("arm64", "aarch64"):
            target = "arm64_apple" if platform.system() == "Darwin" else "arm64"
        elif machine in ("x86_64", "amd64"):
            target = "amd64_apple" if platform.system() == "Darwin" else "amd64_sysv"
        else:
            raise SystemExit("native phi oracle requires an arm64 or amd64 host")
        driver = root / "driver.c"
        driver.write_text(DRIVER)
        executable = root / "test"
        subprocess.run(["cc", "-std=c99", "-O2", str(driver), str(root / (target + ".s")), "-o", str(executable)], check=True)
        subprocess.run([str(executable)], check=True)


if __name__ == "__main__":
    main()
