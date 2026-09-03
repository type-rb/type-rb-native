# Gate 4 Compiler Conformance Corpus

This corpus fixes the behavioral boundary of the self-hosted compiler. Every
source is passed to the compiler at runtime. The harness runs each applicable
valid source through `check` and two independent `emit-qbe` invocations at
every required generation, requires byte-identical QBE, links that QBE, and
compares the program output with the checked-in `.out` file. The original
cases remain shared by recovery B0/B1 and every later generation. Feature
fixtures added after the retained snapshot begin at their first updated Native
B2 and do not retroactively widen recovery.

The valid cases cover:

- typed direct calls, mutable locals, conditionals, loops, and checked Integer
  arithmetic in `valid/control-flow.trb`;
- nominal record construction and projection plus homogeneous Integer Array
  construction, indexing, growth, and mutation in `valid/records-arrays.trb`;
- managed String concatenation and content inequality in
  `valid/strings-calls.trb`;
- compile-time literal-only String concatenation, dynamic controls, decoded
  escapes, chains, and postfix binding in `valid/literal-string-concat.trb`;
- deterministic dependency-free compression, initialization, indexing,
  escapes, terminating zero, and equality
  for multiple long static Strings in `valid/static-strings.trb`;
- finite binary64 literals, signed zero, subnormal and underflow behavior,
  infinity, NaN, mixed Integer widening, arithmetic, comparisons, calls,
  mutable locals, and record fields in `valid/float-scalars.trb`;
- contextual and inferred Float Arrays, Integer element widening, parameters,
  results, records, aliases, growth, positive and negative indexing, mutation,
  compound arithmetic, and nested Float Arrays in
  `valid/float-arrays.trb`, starting at its updated Native B2;
- shared outer Integer Array identity across aliases and mutable parameters,
  including growth, element mutation, and parameter-local rebinding in
  `valid/array-aliases.trb`;
- managed record-field and Array-element aliases retained through owner
  reassignment, lexical-block exit, loop-root compaction, and forced
  collection in `valid/managed-alias-roots.trb`;
- safe-point-free zero-iteration, nested, and early-return loops followed by
  collection pressure in `valid/safe-point-free-loop-roots.trb`;
- managed Array element order, positive and negative indexing, mutation,
  nesting, and forced collection across geometric growth boundaries in
  `valid/managed-array-growth.trb`, with scalar Array growth as a control;
- Integer Array order, aliases, nested retention, mutation, append, negative
  indexing, and forced collection across scalar geometric growth
  boundaries in `valid/scalar-array-growth.trb`;
- repeated Array-header reads in an owned-managed loop, with exact invalidation
  after an opaque mutating call and local Array rebinding in
  `valid/array-header-cache-invalidation.trb`;
- verified stable Array-header reuse in nested loops, including empty input,
  ordinary positive and negative indexes, growth, parameter rebinding,
  allocation, ordinary calls, and element mutation through a possible alias in
  `valid/stable-array-header-mir.trb`;
- zero-based and bounded-derived unit-step induction loops whose nested Array
  reads retain the unsigned upper-bounds check, followed by a reset and
  ordinary negative indexing in `valid/nonnegative-loop-index.trb`;
- verified two-phi `Array<Integer>` reduction, including the empty identity,
  in `valid/integer-array-reduction.trb`;
- left-to-right, exactly-once argument evaluation through a bounded scalar
  leaf call in `valid/scalar-leaf-inline.trb`;
- checked Integer multiplication at the bounded nonnegative fast-entry
  threshold, its safe slow path, negative operands, zero, and the portable
  extrema in `valid/integer-multiply-fast-path.trb`;
- one-sided checked Integer addition for bounded nonnegative literals on
  either side, including the classifier boundary, its dynamic fallback, zero,
  and the portable extrema in `valid/integer-literal-add-one-sided.trb`; and
- the compiler source closure itself, exercised by the bootstrap test outside
  this directory.

Each invalid `.source` file has an exact `.diag` result. The non-`.trb`
extension keeps intentionally malformed programs out of repository-wide source
formatting. Together they require the
lexer, parser, resolver, and checker to remain active and cover unsupported
characters, unfinished syntax, duplicate declarations, unresolved calls,
arity errors, type mismatches, unsupported types, malformed and overflowing
Float literals, narrowing, remainder, and unavailable methods. `emit-qbe` must
return the same diagnostic without emitting an executable function, proving
that the failure occurs before code generation. The Integer and Float boundary
cases keep the self-hosted compiler aligned with TypeRB's portable ranges
rather than target or QBE fallback behavior.

The candidate-only Float Array diagnostics additionally preserve incompatible
element rejection, mutable Array invariance, immutable mutation rejection, and
unsupported-method rejection. Each source in `runtime-invalid` has an exact
`.stderr` sidecar. The directory covers positive and too-negative Array bounds
failures, checked Integer overflow through an inlined scalar leaf, and the
bounded nonnegative multiplication entry at its exact power-of-two threshold.
Negative, zero, maximum, safe slow-path, and overflow behavior are fixed by
`valid/integer-multiply-fast-path.trb` and
`runtime-invalid/integer-multiply-fast-path-overflow.trb`; status, empty
stdout, and panic text must agree across the updated B2/B3/B4 compilers.
The bounded literal-addition entry is likewise paired with
`runtime-invalid/integer-literal-add-one-sided-overflow.trb` so the removed
lower check cannot weaken the retained upper-bound failure.
The verified reduction accumulator is paired with
`runtime-invalid/integer-array-reduction-overflow.trb` so its phi lowering
cannot weaken checked Integer addition.

The `mutations` directory contains a base program and two independently changed
sources. All three must produce distinct QBE and distinct runtime output. This
guards against an embedded artifact, a source-insensitive generator, or a
compiler path that bypasses its runtime input.

The `file-root` directory is the representative Gate 6E import closure used by
the permanent bootstrap differential tests. `file-root-flattened.trb` preserves
the same workload and observable output in one source file so the benchmark can
isolate file-root module overhead from ordinary Native code generation.

This is an experimental subset corpus, not the TypeRB language conformance
suite. Full language and package compatibility remains outside Gate 4.
