# Gate 6I Self-hosted Float Scalar Path

Gate 6I extends the real self-hosted frontend and QBE emitter with the existing
portable TypeRB `Float` semantics. Its exact correctness and measurement
boundary is pre-registered in
[issue #69](https://github.com/type-rb/type-rb-native/issues/69), and the ABI
and ownership model is defined by
[Decision 0016](decisions/0016-self-hosted-float-scalar-path.md).

## Status

Implementation and the TypeRB-authored
[benchmark controller](../tools/gate6i-benchmark/README.md) are complete;
formal measurement is pending. The ordinary Darwin B1-to-B4 smoke chain is
byte-identical, the permanent Float corpus executes, and the existing
representative application retains exact bytes. These are pre-measurement
correctness checks rather than the registered result.

The fixed source baseline is TypeRB Native main revision
`1311dfccee379dcf2dd3a70a525bc188d195981d`. Both baseline and candidate begin
from the retained 244,968-byte Gate 6H Darwin B4 compiler with SHA-256
`b66d65c4ddb729f71afa6ab2c6bca38f6be65eda2433ebb160058d15377891b2`.

## Semantic boundary

The reference TypeRB repository remains the semantic oracle. This repository
does not define a Native Float dialect.

The registered slice includes:

- finite decimal binary64 literals using the existing reference grammar;
- signed-zero underflow and runtime infinity and NaN behavior;
- Float parameters, results, locals, mutation, calls, and record fields;
- unary `+` and `-`, arithmetic `+`, `-`, `*`, and `/`, and all six numeric
  comparisons; and
- safe Integer-to-Float widening across typed values and mixed numeric
  expressions.

The QBE contract uses `d` parameters, results, loads, stores, arithmetic, and
comparisons plus `sltof` for widening. Float values are never reclassified as
Integer-shaped `l` values. Literal range checking belongs to the self-hosted
checker, so `check` does not delegate semantics to QBE.

Float formatting and predicates, explicit Float-to-Integer conversion,
`Array<Float>`, `**`, math packages, configured projects, public CLI design,
incremental caching, tool discovery, source maps, and release seed policy are
deferred. Unsupported expressions must still fail explicitly.

## Correctness boundary

Permanent evidence must cover literal range and underflow, negative zero,
arithmetic, comparisons, widening in both operand orders and every typed
boundary, function ABI, records, mutable storage, infinity, NaN, deterministic
diagnostics, and repeated application identity. It also retains the complete
existing compiler corpus, exact candidate B2/B3/B4 bytes and fixed-point QBE,
the Gate 6E representative application, intermediate cleanup, and a pinned
Linux arm64 correctness chain.

## Registered workload and measurement

The numeric workload starts at `1.0` and performs five million dependent
iterations of four fixed Float expressions:

```trb
value = value * 1.0000001 + 0.0000003
value = value / 1.00000005 - 0.0000001
value = value * 0.99999998 + 0.0000002
value = value / 1.00000001 - 0.00000005
```

It accepts only a final value strictly between `2.9456` and `2.9457` and prints
`float-kernel-ok`. The checked-in
[`main.trb`](../corpus/gate6i/float-kernel/src/main.trb) SHA-256 is
`7d5125967da5a740faf62c0cc3a89d04bdaade54a475c2649d82892847e77dfe`.
It is fixed before formal results.

On Darwin arm64, Native and the pinned optimized Go backend build and run the
same TypeRB source. After the registered warmups and alternating observations:

- Native build time, build RSS, runtime, and runtime RSS must each remain
  within 25% of optimized Go;
- the stripped Native application must be at least 80% smaller than the
  size-optimized Go application; and
- observable output and status must match exactly.

A fresh alternating Gate 6H baseline guards the canonical compiler. Candidate
direct QBE emission, complete build time, and their peak RSS must remain within
10%; the stripped compiler must not exceed 220,000 bytes; fixed-point identity
and the representative application remain mandatory. Linux performance is
diagnostic, but its correctness-only B1-to-B4 and application runs must pass.

Formal evidence records raw observations, workload and source hashes, artifact
identity, seed provenance, exact commands, sizes, process and dependency
boundaries, external tools, and cleanup.
