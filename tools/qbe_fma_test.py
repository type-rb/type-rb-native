#!/usr/bin/env python3
"""Check explicitly permitted Float contraction against independent libm oracles."""
import argparse
from pathlib import Path
import platform
import re
import subprocess
import tempfile


FORMS = {"add": ("add", "%product, %c"), "reverse_add": ("add", "%c, %product"),
         "subtract": ("sub", "%product, %c"), "reverse_subtract": ("sub", "%c, %product")}


def operations(width):
    functions = []
    for name, (operation, operands) in FORMS.items():
        for prefix, multiply in (("", "mulc"), ("strict_", "mul")):
            functions.append(f"""export function {width} ${width}_{prefix}{name}({width} %a, {width} %b, {width} %c) {{
@start
 %product ={width} {multiply} %a, %b
 %result ={width} {operation} {operands}
 ret %result
}}
""")
    functions.append(f"""export function {width} ${width}_reuse({width} %a, {width} %b, {width} %c, l %out) {{
@start
 %product ={width} mulc %a, %b
 %result ={width} add %product, %c
 store{width} %product, %out
 ret %result
}}
export function {width} ${width}_twice({width} %a, {width} %b) {{
@start
 %product ={width} mulc %a, %b
 %result ={width} add %product, %product
 ret %result
}}
export function {width} ${width}_live({width} %a, {width} %b, {width} %c, l %out) {{
@start
 %product ={width} mulc %a, %b
 %result ={width} add %product, %c
 store{width} %result, %out
 %next =l add %out, {8 if width == "d" else 4}
 store{width} %b, %next
 ret %product
}}
export function {width} ${width}_call({width} %a, {width} %b, {width} %c) {{
@start
 %product ={width} mulc %a, %b
 %other ={width} call $echo_{width}({width} %c)
 %result ={width} add %product, %other
 ret %result
}}
export function {width} ${width}_branch({width} %a, {width} %b, {width} %c, w %which) {{
@start
 %product ={width} mulc %a, %b
 jnz %which, @sum, @product
@sum
 %result ={width} add %product, %c
 ret %result
@product
 ret %product
}}
export function {width} ${width}_constant() {{
@start
 %product ={width} mulc {width}_2.0, {width}_3.0
 %result ={width} add %product, {width}_4.0
 ret %result
}}
""")
    return "".join(functions)


# Compile at -O0 with contraction disabled. Volatile products are independent
# rounding barriers; the fused oracle calls libm rather than a generated QBE op.
DRIVER = r"""
#include <float.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef @TYPE@ Scalar;
typedef @BITS@ Bits;
extern Scalar @W@_add(Scalar, Scalar, Scalar);
extern Scalar @W@_reverse_add(Scalar, Scalar, Scalar);
extern Scalar @W@_subtract(Scalar, Scalar, Scalar);
extern Scalar @W@_reverse_subtract(Scalar, Scalar, Scalar);
extern Scalar @W@_strict_add(Scalar, Scalar, Scalar);
extern Scalar @W@_strict_reverse_add(Scalar, Scalar, Scalar);
extern Scalar @W@_strict_subtract(Scalar, Scalar, Scalar);
extern Scalar @W@_strict_reverse_subtract(Scalar, Scalar, Scalar);
extern Scalar @W@_reuse(Scalar, Scalar, Scalar, Scalar *);
extern Scalar @W@_twice(Scalar, Scalar);
extern Scalar @W@_live(Scalar, Scalar, Scalar, Scalar *);
extern Scalar @W@_call(Scalar, Scalar, Scalar);
extern Scalar @W@_branch(Scalar, Scalar, Scalar, int);
extern Scalar @W@_constant(void);
Scalar echo_@W@(Scalar value) { return value; }
static int same(Scalar a, Scalar b) {
    Bits left, right;
    if (isnan(a) && isnan(b)) return 1;
    memcpy(&left, &a, sizeof left);
    memcpy(&right, &b, sizeof right);
    return left == right;
}
static int check(Scalar a, Scalar b, Scalar c) {
    volatile Scalar product = a * b;
    Scalar separate[] = {product + c, c + product, product - c, c - product};
    Scalar fused[] = {@FMA@(a, b, c), @FMA@(a, b, c),
                      @FMA@(a, b, -c), @FMA@(-a, b, c)};
    Scalar (*permitted[])(Scalar, Scalar, Scalar) = {
        @W@_add, @W@_reverse_add, @W@_subtract, @W@_reverse_subtract};
    Scalar (*strict[])(Scalar, Scalar, Scalar) = {
        @W@_strict_add, @W@_strict_reverse_add, @W@_strict_subtract,
        @W@_strict_reverse_subtract};
    for (unsigned i = 0; i < 4; ++i) {
        Scalar expected = HOST_FUSES ? fused[i] : separate[i];
        if (!same(permitted[i](a, b, c), expected)) return 10 + i;
        if (!same(strict[i](a, b, c), separate[i])) return 20 + i;
    }
    Scalar observed = 0;
    Scalar result = @W@_reuse(a, b, c, &observed);
    if (!same(observed, product)) return 30;
    if (!same(result, separate[0]) && !same(result, fused[0])) return 31;
    if (!same(@W@_twice(a, b), product + product)) return 32;
    result = @W@_call(a, b, c);
    if (!same(result, separate[0]) && !same(result, fused[0])) return 33;
    if (!same(@W@_branch(a, b, c, 0), product)) return 34;
    result = @W@_branch(a, b, c, 1);
    if (!same(result, separate[0]) && !same(result, fused[0])) return 35;
    Scalar live[2];
    result = @W@_live(a, b, c, live);
    if (!same(result, product)) return 37;
    if (!same(live[0], HOST_FUSES ? fused[0] : separate[0])) return 38;
    if (!same(live[1], b)) return 39;
    return 0;
}
int check_@W@(void) {
    if (@W@_constant() != 10.0) return 36;
    Scalar values[] = {0.0, -0.0, 1.0, -1.0, 2.0, -2.0, INFINITY,
        -INFINITY, NAN, @MAX@, -@MAX@, @MIN@, -@MIN@, @TRUE_MIN@,
        @NEXT_ONE@, -@NEXT_TWO@};
    unsigned count = sizeof values / sizeof *values, checks = 1;
    for (unsigned a = 0; a < count; ++a)
    for (unsigned b = 0; b < count; ++b)
    for (unsigned c = 0; c < count; ++c) {
        int status = check(values[a], values[b], values[c]);
        if (status) {
            fprintf(stderr, "@W@ edge %u/%u/%u failed check %d\n", a, b, c, status);
            return status;
        }
        checks += 17;
    }
    uint64_t state = UINT64_C(0x384028ccab71e107);
    for (unsigned n = 0; n < 4096; ++n) {
        Scalar inputs[3];
        for (unsigned i = 0; i < 3; ++i) {
            state ^= state << 13; state ^= state >> 7; state ^= state << 17;
            Bits bits = state;
            memcpy(&inputs[i], &bits, sizeof bits);
        }
        int status = check(inputs[0], inputs[1], inputs[2]);
        if (status) {
            fprintf(stderr, "@W@ random %u failed check %d\n", n, status);
            return status;
        }
        checks += 17;
    }
    printf("@W@ contraction: %u checks passed\n", checks);
    return 0;
}
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qbe", required=True, type=Path)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--previous-contraction", type=Path)
    args = parser.parse_args()
    qbe = args.qbe.resolve()
    source = operations("d") + operations("s")
    with tempfile.TemporaryDirectory(prefix="native-qbe-fma-") as temporary:
        root = Path(temporary)
        targets = ("arm64", "arm64_apple", "amd64_sysv", "amd64_apple", "amd64_win", "rv64")
        for target in targets:
            result = subprocess.run([str(qbe), "-t", target], input=source,
                                    text=True, capture_output=True, check=True)
            (root / (target + ".s")).write_text(result.stdout)
            for width in ("d", "s"):
                for name in FORMS:
                    for prefix in ("", "strict_"):
                        symbol = width + "_" + prefix + name
                        body = re.split(rf"(?m)^_?{symbol}:\s*$", result.stdout)[1]
                        body = body.split("/* end function")[0]
                        fused = bool(re.search(r"\bf(?:madd|msub|nmsub)\b", body))
                        assert fused == (target.startswith("arm64") and not prefix), (target, symbol)
                body = re.split(rf"(?m)^_?{width}_live:\s*$", result.stdout)[1]
                body = body.split("/* end function")[0]
                fused = bool(re.search(r"\bfmadd\b", body))
                assert fused == target.startswith("arm64"), (target, width, "live product")
                if fused:
                    assert re.search(r"\bfmul\b", body), (target, width, "missing rounded product")
                body = re.split(rf"(?m)^_?{width}_reuse:\s*$", result.stdout)[1]
                body = body.split("/* end function")[0]
                assert not re.search(r"\bfmadd\b", body), (target, width, "input alias")
        machine = platform.machine()
        arm64 = machine in ("arm64", "aarch64")
        if arm64:
            target = "arm64_apple" if platform.system() == "Darwin" else "arm64"
        elif machine in ("x86_64", "AMD64"):
            target = "amd64_apple" if platform.system() == "Darwin" else "amd64_sysv"
        else:
            raise ValueError(f"unsupported test host: {machine}")
        for width, kind, bits, fma, limits, one, two in (
                ("d", "double", "uint64_t", "fma", "DBL", "0x1.0000000000001p0", "0x1.0000000000002p0"),
                ("s", "float", "uint32_t", "fmaf", "FLT", "0x1.000002p0f", "0x1.000004p0f")):
            text = DRIVER
            replacements = {"W": width, "TYPE": kind, "BITS": bits, "FMA": fma,
                            "MAX": limits + "_MAX", "MIN": limits + "_MIN",
                            "TRUE_MIN": limits + "_TRUE_MIN", "NEXT_ONE": one, "NEXT_TWO": two}
            for key, value in replacements.items():
                text = text.replace("@" + key + "@", value)
            (root / (width + ".c")).write_text(text)
        (root / "main.c").write_text("int check_d(void); int check_s(void);\n"
                                    "int main(void) { int result = check_d(); return result ? result : check_s(); }\n")
        binary = root / "edges"
        subprocess.run(["cc", "-std=c11", "-O0", "-ffp-contract=off", "-fno-builtin",
                        f"-DHOST_FUSES={int(arm64)}", str(root / "d.c"), str(root / "s.c"),
                        str(root / "main.c"), str(root / (target + ".s")), "-lm",
                        "-o", str(binary)], check=True)
        subprocess.run([str(binary)], check=True)
    for operation in ("%y =w mulc %x, %x", "%y =l mulc %x, %x", "%y =d mulc %x"):
        result = subprocess.run([str(qbe)], input="function d $bad(d %x) {\n@start\n " +
                                operation + "\n ret %x\n}\n", text=True, capture_output=True)
        assert result.returncode != 0, operation
    if args.baseline:
        result = subprocess.run([str(args.baseline.resolve())], input=source, text=True, capture_output=True)
        assert result.returncode != 0 and "mulc" in result.stderr, "previous backend accepted the new opcode"
    if args.previous_contraction:
        result = subprocess.run([str(args.previous_contraction.resolve()), "-t", "arm64"],
                                input=source, text=True, capture_output=True, check=True)
        body = re.split(r"(?m)^d_live:\s*$", result.stdout)[1].split("/* end function")[0]
        assert not re.search(r"\bfmadd\b", body), "previous variant already preserves fused live products"
    print("QBE Float contraction, strict multiplication, reuse, calls and branches passed on six emission targets")


if __name__ == "__main__":
    main()
