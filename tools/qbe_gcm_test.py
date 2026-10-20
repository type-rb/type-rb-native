#!/usr/bin/env python3
"""Check expression motion, invariant guards and late loop layout."""
import argparse
import os
from pathlib import Path
import platform
import re
import subprocess
import tempfile


GUARD = """export function l $guard(l %a, l %b, l %c, l %n) {
@start
 jmp @loop
@loop
 %i =l phi @start 0, @join %next
 %sum =l phi @start 0, @join %newsum
 %more =w csltl %i, %n
 jnz %more, @body, @done
@body
 %one =w csltl %a, %b
 %two =w cnel %b, %c
 %both =w and %one, %two
 jnz %both, @yes, @no
@yes
 %left =l add %sum, 7
 jmp @join
@no
 %right =l sub %sum, 3
 jmp @join
@join
 %newsum =l phi @yes %left, @no %right
 %next =l add %i, 1
 jmp @loop
@done
 ret %sum
}
"""

SINGLE_GUARD = GUARD.replace("$guard(", "$single_guard(").replace(
    "%both =w and %one, %two", "%both =w copy %one")

SHARED = """export function l $shared(l %a, l %b, l %c, l %which) {
@start
 %one =l csltl %a, %b
 %two =l cnel %b, %c
 %both =l and %one, %two
 %first =w csltl %which, 0
 jnz %first, @branch, @value
@branch
 jnz %both, @yes, @no
@yes
 ret 7
@no
 ret -3
@value
 ret %both
}
"""

ADDRESS = """export function $address(l %p, l %seed, l %n) {
@start
 %masked =l and %seed, 7
 %offset =l shl %masked, 3
 %address =l add %p, %offset
 jmp @loop
@loop
 %i =l phi @start 0, @body %next
 %more =w csltl %i, %n
 jnz %more, @body, @done
@body
 %value =l loadl %address
 %updated =l add %value, 1
 storel %updated, %address
 %next =l add %i, 1
 jmp @loop
@done
 ret
}
"""

CALLED = """export function l $called(l %seed, l %n) {
@start
 jmp @loop
@loop
 %i =l phi @start 0, @body %next
 %value =l phi @start %seed, @body %updated
 %more =w csltl %i, %n
 jnz %more, @body, @done
@body
 %updated =l call $layout_step(l %value, l %i)
 %next =l add %i, 1
 jmp @loop
@done
 ret %value
}
"""

NESTED = """export function l $nested(l %n, l %m) {
@start
 jmp @outer
@outer
 %i =l phi @start 0, @advance %nexti
 %total =l phi @start 0, @advance %sum
 %morei =w csltl %i, %n
 jnz %morei, @prepare, @done
@prepare
 jmp @inner
@inner
 %j =l phi @prepare 0, @body %nextj
 %sum =l phi @prepare %total, @body %added
 %morej =w csltl %j, %m
 jnz %morej, @body, @advance
@body
 %added =l add %sum, %j
 %nextj =l add %j, 1
 jmp @inner
@advance
 %nexti =l add %i, 1
 jmp @outer
@done
 ret %total
}
"""

DRIVER = r"""
#include <stdint.h>
#include <stdio.h>
extern int64_t guard(int64_t, int64_t, int64_t, int64_t);
extern int64_t single_guard(int64_t, int64_t, int64_t, int64_t);
extern int64_t shared(int64_t, int64_t, int64_t, int64_t);
extern void address(uint64_t *, uint64_t, int64_t);
extern uint64_t called(uint64_t, int64_t);
extern int64_t nested(int64_t, int64_t);
static unsigned calls;
uint64_t layout_step(uint64_t value, uint64_t index) {
    ++calls;
    return value * UINT64_C(1664525) + index + UINT64_C(1013904223);
}
int main(void) {
    int64_t values[] = {INT64_MIN, -1, 0, 1, 17, INT64_MAX};
    int64_t trips[] = {-3, 0, 1, 2, 31, 65};
    unsigned checks = 0;
    for (unsigned a = 0; a < 6; ++a)
    for (unsigned b = 0; b < 6; ++b)
    for (unsigned c = 0; c < 6; ++c) {
        int condition = values[a] < values[b] && values[b] != values[c];
        for (unsigned n = 0; n < 6; ++n) {
            int64_t count = trips[n] < 0 ? 0 : trips[n];
            int64_t expected = count * (condition ? 7 : -3);
            if (guard(values[a], values[b], values[c], trips[n]) != expected)
                return 1;
            if (single_guard(values[a], values[b], values[c], trips[n])
                != count * (values[a] < values[b] ? 7 : -3))
                return 4;
            checks += 2;
        }
        if (shared(values[a], values[b], values[c], -1) != (condition ? 7 : -3)
            || shared(values[a], values[b], values[c], 1) != condition)
            return 2;
        checks += 2;
    }
    for (uint64_t seed = 0; seed < 33; ++seed)
    for (unsigned n = 0; n < 6; ++n) {
        uint64_t data[8];
        for (unsigned i = 0; i < 8; ++i) data[i] = 100 + i;
        address(data, seed, trips[n]);
        for (unsigned i = 0; i < 8; ++i) {
            uint64_t delta = i == (seed & 7) && trips[n] > 0 ? trips[n] : 0;
            if (data[i] != 100 + i + delta) return 3;
            ++checks;
        }
    }
    for (unsigned a = 0; a < 6; ++a)
    for (unsigned n = 0; n < 6; ++n) {
        uint64_t expected = (uint64_t)values[a];
        for (int64_t i = 0; i < trips[n]; ++i)
            expected = expected * UINT64_C(1664525) + i + UINT64_C(1013904223);
        calls = 0;
        if (called((uint64_t)values[a], trips[n]) != expected) return 5;
        if (calls != (trips[n] > 0 ? (unsigned)trips[n] : 0)) return 6;
        checks += 2;
        int64_t total = 0;
        for (int64_t i = 0; i < trips[a]; ++i)
        for (int64_t j = 0; j < trips[n]; ++j) total += j;
        if (nested(trips[a], trips[n]) != total) return 7;
        ++checks;
    }
    printf("%u control-flow semantic checks passed\n", checks);
    return 0;
}
"""


def check_motion(qbe, target):
    for name, source in (("guard", GUARD), ("single", SINGLE_GUARD),
                         ("shared", SHARED), ("address", ADDRESS)):
        result = subprocess.run([str(qbe), "-t", target, "-d", "G"], input=source,
                                text=True, capture_output=True, check=True)
        moved = result.stderr.split("> After GCM:", 1)[1]
        for value in re.findall(r"(%snk\.\d+)\s*=", moved):
            if len(re.findall(re.escape(value) + r"(?!\d)", moved)) == 1:
                raise AssertionError(f"{target} {name}: unused sunk operand {value}")
        if name == "guard":
            # The induction comparison stays in the loop, while the compound
            # predicate depends only on immutable function arguments.
            body = moved.split("@body\n", 1)[1].split("@yes\n", 1)[0]
            if re.search(r"\b(?:csltl|cnel|and)\b", body):
                raise AssertionError(f"{target}: invariant predicate was sunk into the loop")
        elif name == "address":
            body = moved.split("@body\n", 1)[1].split("@done\n", 1)[0]
            if not re.search(r"\bload %snk\.\d+", body):
                raise AssertionError(f"{target}: cheap address rematerialization was disabled")
        elif name == "single":
            body = moved.split("@body\n", 1)[1].split("@yes\n", 1)[0]
            if "csltl" not in body:
                raise AssertionError(f"{target}: single comparison rematerialization was disabled")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qbe", type=Path, required=True)
    args = parser.parse_args()
    qbe = args.qbe.resolve()
    targets = ("arm64", "arm64_apple", "amd64_sysv", "amd64_apple", "amd64_win", "rv64")
    with tempfile.TemporaryDirectory(prefix="qbe-gcm-") as temporary:
        root = Path(temporary)
        source = root / "input.ssa"
        source.write_text(GUARD + SINGLE_GUARD + SHARED + ADDRESS + CALLED + NESTED)
        for target in targets:
            check_motion(qbe, target)
            subprocess.run([str(qbe), "-t", target, "-o", str(root / (target + ".s")),
                            str(source)], check=True)
        machine = platform.machine()
        native = "arm64" if machine in ("arm64", "aarch64") else "amd64"
        native += "_apple" if platform.system() == "Darwin" else ("_sysv" if native == "amd64" else "")
        driver = root / "driver.c"
        driver.write_text(DRIVER)
        program = root / "program"
        subprocess.run([os.environ.get("CC", "cc"), str(driver), str(root / (native + ".s")),
                        "-o", str(program)], check=True)
        result = subprocess.run([str(program)], capture_output=True, text=True, check=True)
        assert result.stdout == "4716 control-flow semantic checks passed\n", result.stdout
        assert not result.stderr, result.stderr
        print(result.stdout, end="")
        print("Expression motion, invariant guards and loop layout verified for six targets")


if __name__ == "__main__":
    main()
