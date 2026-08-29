# Gate 6J Self-hosted Float Arrays

Gate 6J extends the real self-hosted frontend, Array runtime, and QBE emitter
with the existing portable TypeRB `Array<Float>` semantics. Its exact
correctness and measurement boundary is pre-registered in
[issue #74](https://github.com/type-rb/type-rb-native/issues/74), and the
representation and ownership model is defined by
[Decision 0017](decisions/0017-self-hosted-float-arrays.md).

## Status

Registered. Implementation and formal measurement have not begun.

The fixed source baseline is TypeRB Native main revision
`5ff3da39c8c41a30596bbeed3b6fcffc207a43ed`. Both baseline and candidate begin
from the retained 264,264-byte Gate 6I Darwin B4 compiler with SHA-256
`849f5d6c6fc0738735c84b9240e8f87a477e8d978b0c64a995a5cae5944d8f8d`.

## Semantic boundary

The reference TypeRB repository remains the semantic oracle. This repository
does not define a Native Float Array dialect.

The registered slice includes:

- `Array<Float>` parameters, results, locals, calls, records, and aliases;
- contextual empty and non-empty literals plus safe common numeric inference
  for fresh literals such as `[1, 2.5]`;
- Integer-to-Float widening at element construction, `push`, assignment,
  argument, return, and record boundaries;
- `size`, mutable `push`, positive and negative indexing, indexed assignment,
  indexed compound arithmetic, growth, and bounds failure; and
- the existing bounded two- and three-level nested Array forms with Float as
  the innermost payload.

Mutable Arrays remain invariant. An existing `Array<Integer>` does not widen
to `Array<Float>`. Direct Float cells use QBE `d`, `loadd`, and `stored` behind
a dedicated Float push path; outer nested Array cells remain `l` references.
The 24-byte header, eight-byte cells, allocation and growth policy, and bounds
normalization remain shared with the existing TypeRB-owned runtime.

Float formatting and predicates, explicit narrowing, exponentiation, math
packages, configured projects, public CLI design, incremental caching, tool
discovery, source maps, and release seed policy remain deferred. Unsupported
uses must still fail explicitly.

## Correctness boundary

Permanent evidence must cover contextual and inferred Float Arrays, mixed
numeric literal inference, widening at every element and typed boundary,
parameters and returns, record fields, aliasing, growth, `size`, both index
directions, mutation and compound arithmetic, nested Arrays, and bounds
failure. It must reject incompatible elements, immutable mutation, invariant
Array widening, and unsupported methods deterministically.

The result also retains the complete existing compiler corpus, exact candidate
B2/B3/B4 bytes and fixed-point QBE, repeated Float Array QBE and application
bytes, exact Gate 6E representative and Gate 6I scalar Float applications,
intermediate cleanup, and a pinned Linux arm64 correctness chain.

## Registered workload and measurement

The checked-in [`main.trb`](../corpus/gate6j/float-array/src/main.trb) builds an
`Array<Float>` with five million values, transforms every element in place,
mutates the first and negative-last elements, and reduces the full Array. It
accepts only a total strictly between `253500200.0` and `253500300.0` and
prints `float-array-ok`. Its fixed SHA-256 is:

```text
ed874d688f0faf8cdcc56e8a6992bd25be1826bc909093cdd485699dbd3b75cf
```

On Darwin arm64, Native and the pinned optimized Go backend build and run the
same source. After the registered warmups and alternating observations:

- Native build time, build RSS, runtime, and runtime RSS must each remain
  within 25% of optimized Go;
- the stripped Native application must be at least 80% smaller than the
  size-optimized Go application; and
- observable output, status, element count, indexed values, and numeric range
  must match exactly.

A fresh alternating Gate 6I baseline guards the canonical compiler. Candidate
direct QBE emission, complete build time, and their peak RSS must remain within
10%; the stripped compiler must not exceed 224,000 bytes. Exact fixed-point
identity and unchanged representative and scalar Float applications remain
mandatory. Linux performance is diagnostic, but its correctness-only B1-to-B4
and application runs must pass.

Formal evidence records raw observations, workload and source hashes, artifact
identity, seed provenance, exact commands, sizes, process and dependency
boundaries, external tools, and cleanup.
