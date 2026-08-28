# Gate 5 Matched Self-Hosted Compiler Baseline

Gate 5 replaces Gate 4's unmatched diagnostic comparison with a functional
optimized Go compiler built from the same TypeRB-authored compiler logic as the
Native executable. Its registered acceptance criteria and performance bounds
live in [issue #29](https://github.com/type-rb/type-rb-native/issues/29), and
the boundary is defined by
[Decision 0007](decisions/0007-matched-self-hosted-compiler-baseline.md).

## Status

Gate 5 is complete at TypeRB Native revision
`a83699d6dd87de0c77a8a8a395ea6e266802bf0a`. The matched corpus, fixed point,
normalization, Go-free process boundary, time, peak-RSS, artifact-size,
distribution, and adjacent-generation criteria all pass. See the
[recorded Darwin arm64 result](../results/2026-08-29-gate5-matched-compiler-darwin-arm64/README.md).

## Comparison boundary

Both candidates receive the same source text and one of the same internal
`check` or `emit-qbe` modes. Both execute the checked-in lexer, parser,
resolver, checker, and QBE emitter.

```text
checked-in TypeRB compiler source
    |                                |
    | Native self-host path          | optimized Go comparison build
    v                                v
B1/B2 Native compiler           generated argv-only driver
    |                                |
    +-------- source + mode ----------+
                     |
                     v
        identical compiler behavior and QBE
```

The generated Go source differs only at the driver boundary: it imports the
existing portable `argv()` operation and replaces the authored empty `main()`
with a call to `compiler_main`. The harness verifies this transformation and
rejects a baseline that omits or dead-strips the compiler entry. The Native
entry remains the Gate 4 repository-internal adapter for this gate.

The first implementation stage performs this transformation in TypeRB, proves
that reversing the import and driver changes recovers the canonical compiler
source byte-for-byte, builds the optimized Go executable with the pinned
reference compiler, and runs it as an additional candidate in the complete
valid, invalid, and mutation corpus. The canonical compiler source is not
modified for the comparison.

This is deliberately not a supported command contract. The ordinary
file-oriented compiler CLI, project discovery, package resolution, direct QBE
and linker orchestration, and production runtime belong to Gate 6.

## Storage work

Gate 4 allocated many token, declaration, local, and output arrays at a size
derived from the complete source length. Gate 5 changed those structures to
grow with the number of stored elements. Tests cover empty storage, initial
growth, repeated growth, exact boundary access, and deterministic rejection at
resource limits.

The gate does not accept lower memory use obtained by skipping a compiler pass,
weakening validation, truncating input, or retaining unchecked fallback data.

## Reproducibility and self-hosting

- B0 remains the recovery seed.
- B1 produces B2 without Go or the reference compiler.
- B2 produces B3 as an additional fixed-point observation.
- B1, B2, and B3 compiler QBE must be byte-identical.
- B1 and B2 executables must be equivalent under a recorded normalization
  policy that preserves all code and data.
- The valid, invalid, mutation, and storage-boundary corpus runs through every
  required Native generation and the functional optimized Go comparison.

### Executable normalization

QBE and assembly remain byte-identical before linking. On Darwin, the remaining
Mach-O variation comes from `LC_UUID` and from the ad-hoc code-signature
identifier derived from the output basename. The registered normalization
therefore relinks each unchanged B1/B2 assembly with the ordinary
`-Wl,-dead_strip` option plus `-Wl,-no_uuid`, using `compiler` as the basename
in two separate directories. It then compares the complete Mach-O files.

This policy does not remove or ignore any code or data section. The automated
[`gate5-normalize.sh`](../tools/gate5-normalize.sh) check also rejects an
output that still contains `LC_UUID`. Under this policy B1 and B2 must be
byte-identical, which is stronger than section-wise equivalence.

### Measurement harness

[`tools/gate5-benchmark`](../tools/gate5-benchmark) constructs B0 through B3
and the matched Go artifact, verifies the fixed point and the direct Go-free
B1-to-B2 recipe, and refuses to record measurements if any compiler output
differs. It records two indexed warmups followed by the requested repetitions,
alternating Native stage order around the matched Go candidate. Direct compiler
and end-to-end build time are separate; compiler, QBE, and link phases remain
visible.

Peak RSS is measured separately with `/usr/bin/time -l` for both direct and
end-to-end paths, up to three repetitions. The same run records raw and
stripped artifacts, distribution components, QBE and artifact hashes, the
deterministic-link result, revisions, tool versions, dynamic dependencies,
undefined symbols, Go metadata probes, and the C driver's assembler/linker
subprocess inventory. The committed result documents the exact command and
requested repetition count.

For a local Darwin arm64 run after preparing the pinned reference `trb` and
QBE 1.3, build the two repository-owned drivers and invoke the harness as
follows. The workspace and output files must be outside a committed result
directory until the run passes and is reviewed.

```sh
trb build --compile --outfile /tmp/type-rb-native-gate5-driver
trb build --compile \
  --config tools/gate5-benchmark/trbconfig.jsonc \
  --outfile /tmp/type-rb-native-gate5-benchmark

/tmp/type-rb-native-gate5-benchmark \
  "$PWD" \
  /path/to/pinned/trb \
  /tmp/type-rb-native-gate5-driver \
  /path/to/qbe-1.3/qbe \
  /usr/bin/cc \
  /path/to/go \
  /tmp/type-rb-native-gate5-workspace \
  7 \
  /tmp/type-rb-native-gate5-raw.csv \
  /tmp/type-rb-native-gate5-process-inventory.txt
```

## Registered performance criteria

The exact pre-registered criteria are in issue #29. In summary, Native direct
compiler time, end-to-end build time, and peak RSS must remain within 25% of
the matched optimized Go executable; stripped compiler and matched compiler
plus QBE distribution sizes must improve by at least 30%; and adjacent Native
generations must remain within 25%. Correctness is all-or-nothing, and a
greater than 2x regression is catastrophic.

The recorded result uses these criteria without relaxing them. Every bound
passes, including conservative maximum-to-maximum peak-RSS comparisons.

## Deferred Gate 6 scope

Gate 6 retains the product-feasibility requirements:

- representative multi-module applications;
- an ordinary file-oriented compiler and project CLI;
- production managed-runtime integration;
- incremental and reproducible project builds;
- package and native-library boundaries;
- at least two primary target environments;
- debugging and operational behavior; and
- total ongoing maintenance cost.

Gate 6 measurements use a previous Native release as the ordinary bootstrap
seed and do not require Go. Promotion remains a separate TypeRB design
decision.
