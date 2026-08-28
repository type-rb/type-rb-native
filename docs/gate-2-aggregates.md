# Gate 2 Heap-Free Aggregate Value Model

Gate 2 extends the verified QBE path from scalar SSA values to heap-free,
static-layout values. It implements existing TypeRB record, payload-enum, and
`Result` semantics without introducing a native-only language feature.

## Implementation status

Gate 2 is complete. The backend-neutral layout model, aggregate Native MIR,
verifier, strict snapshot v3 decoder, source producer, differential corpus,
reproducibility checks, and measured QBE executable path are implemented. The
QBE adapter uses caller-owned result storage, borrowed aggregate parameters,
safe block-parameter copy elision, and checked payload projection. Aggregate
construction initializes padding and inactive payload bytes deterministically.

The final source corpus covers ordinary and nested records, payloadless and
payload-bearing variants, exhaustive dispatch, aggregate direct calls and
returns, `Result`, `try`, loop-carried record state, and parallel aggregate
swaps. See the [Gate 2 result](../results/2026-08-28-gate2-qbe-darwin-arm64/README.md).

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

Aggregate construction zero-initializes its complete slot with explicit stores,
and fixed-size copies use QBE `blit`. Common incoming aggregate values alias
their existing storage. Other block arguments use transfer slots, with staging
only when an edge can overwrite another source. This retains parallel-copy
semantics for aggregate swaps and back edges without unconditional copies.

## Bootstrap snapshot v3

Snapshot v3 adds a required `types` array. A record definition contains its
nominal identifier and declaration-ordered fields. A tagged definition contains
its nominal identifier and declaration-ordered variants, each with
declaration-ordered payload fields. Scalar types use `Boolean`, `Integer`, and
`Float`; every other nonempty type string is a nominal aggregate identifier.
Only function results may use `Void`.

The aggregate instruction set is `record_construct`, `record_project`,
`variant_construct`, `variant_test`, and `variant_project`. Every projection and
constructor names its nominal type explicitly, so strict decoding and MIR
verification do not infer identity from layout shape. Snapshot v2 remains the
Gate 1 scalar fixture format; v3 is an incompatible, temporary bridge rather
than a compatibility extension.

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

All six conditions pass in the recorded Darwin arm64 result. The worst runtime
result is a 17.6% regression on the aggregate kernel, within the 25% limit;
warm build time improves by 26.0% to 29.5%, and stripped executable size
improves by 96.85%. Gate 3 has not started.
