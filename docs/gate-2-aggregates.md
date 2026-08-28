# Gate 2 Heap-Free Aggregate Value Model

Gate 2 extends the verified QBE path from scalar SSA values to heap-free,
static-layout values. It implements existing TypeRB record, payload-enum, and
`Result` semantics without introducing a native-only language feature.

## Implementation status

The backend-neutral layout model, aggregate Native MIR, verifier, and
hand-authored QBE vertical slice are implemented. The QBE adapter uses
caller-owned result storage, borrowed aggregate parameters, separate transfer
and value slots for aggregate block parameters, and checked payload projection.
It initializes aggregate storage before construction so padding and inactive
payload bytes never carry indeterminate data.

The source snapshot producer, strict version 3 decoder, source differential
corpus, and Gate 2 measurements remain active work. This document records the
complete checkpoint rather than treating the hand-authored vertical slice as
the gate result.

## Checkpoint boundary

The supported value graph is finite and known at compile time:

- `Boolean`, portable `Integer`, and binary64 `Float`;
- nominal records whose fields are supported Gate 2 values; and
- nominal tagged values whose variant payload fields are supported Gate 2
  values.

Recursive-by-value declarations, dynamic strings, arrays, hashes, closures,
escaping references, and heap allocation are rejected explicitly. Static UTF-8
output remains available as an observable operation but is not a first-class
field or payload value.

The source corpus must cover record construction and projection, nested
records, payloadless and payload-bearing variants, exhaustive variant dispatch,
explicit `Result` matching, `try` propagation, and aggregate values crossing
direct-call, return, and control-flow-block boundaries.

## Representation direction

Native MIR keeps nominal aggregate types and semantic construction/projection
operations. The `darwin-arm64-v0` lowering computes deterministic size,
alignment, field offsets, tag values, and payload offsets. QBE-specific memory
operations remain below that boundary.

The first implementation uses caller-owned stack storage for non-escaping
aggregate values. Aggregate parameters are borrowed for the duration of a
direct call, and aggregate results use caller-provided result storage. The MIR
semantics remain value semantics even though the disposable target ABI passes
addresses internally. A later allocation strategy can therefore add escaping
storage without changing TypeRB record or enum behavior.

Aggregate construction zero-initializes its complete slot and uses the system
`memcpy`/`memset` ABI for fixed-size copies and initialization. These dynamic
system-library dependencies are counted with the executable in Gate 2 reports.
Block arguments use distinct transfer and value slots so control-flow edges
retain parallel-copy semantics, including aggregate swaps and back edges.

## Exit evidence

Gate 2 completes when:

1. strict snapshot and MIR validation reject malformed types, layouts,
   constructors, projections, tags, and control-flow edges deterministically;
2. layout tests cover alignment, padding, nesting, maximum configured size, and
   distinct nominal types with identical shapes;
3. the registered TypeRB source corpus matches the optimized Go backend in
   stdout, stderr, and exit status;
4. repeated builds reproduce snapshot, MIR, QBE IL, and executable artifacts;
5. stripped executable size improves by at least 30%, warm end-to-end build time
   and runtime remain within 25%, and no primary metric regresses by more than
   2x against the stronger applicable optimized Go baseline; and
6. the result report counts frontend, snapshot, decode, emit, QBE, assembly,
   linking, runtime, peak memory, and distribution costs under the shared
   measurement policy.

Missing an engineering target leaves Gate 2 open for diagnosis and improvement.
Gate 3 does not start until this checkpoint is reported.
