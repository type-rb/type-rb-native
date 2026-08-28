# Gate 5 Matched Self-Hosted Compiler Baseline

Gate 5 replaces Gate 4's unmatched diagnostic comparison with a functional
optimized Go compiler built from the same TypeRB-authored compiler logic as the
Native executable. Its registered acceptance criteria and performance bounds
live in [issue #29](https://github.com/type-rb/type-rb-native/issues/29), and
the boundary is defined by
[Decision 0007](decisions/0007-matched-self-hosted-compiler-baseline.md).

## Status

Gate 5 is in progress. Results are not yet available.

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

This is deliberately not a supported command contract. The ordinary
file-oriented compiler CLI, project discovery, package resolution, direct QBE
and linker orchestration, and production runtime belong to Gate 6.

## Storage work

Gate 4 allocated many token, declaration, local, and output arrays at a size
derived from the complete source length. Gate 5 changes those structures to
grow with the number of stored elements, or records why a remaining fixed
allocation is required. Tests cover empty storage, initial growth, repeated
growth, exact boundary access, and deterministic rejection at resource limits.

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

## Registered performance criteria

The exact pre-registered criteria are in issue #29. In summary, Native direct
compiler time, end-to-end build time, and peak RSS must remain within 25% of
the matched optimized Go executable; stripped compiler and matched compiler
plus QBE distribution sizes must improve by at least 30%; and adjacent Native
generations must remain within 25%. Correctness is all-or-nothing, and a
greater than 2x regression is catastrophic.

Targets will not be relaxed after results are observed merely to complete the
gate. A miss keeps Gate 5 open for diagnosis and implementation work.

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
