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
- left-to-right, exactly-once argument evaluation through a bounded scalar
  leaf call in `valid/scalar-leaf-inline.trb`; and
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
failures plus checked Integer overflow through an inlined scalar leaf; status,
empty stdout, and panic text must agree across the updated B2/B3/B4 compilers.

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
