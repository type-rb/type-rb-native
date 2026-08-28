# Gate 4 Compiler Conformance Corpus

This corpus fixes the behavioral boundary shared by B0, B1, and B2. Every
source is passed to the compiler at runtime. The harness runs each valid source
through `check` and two independent `emit-qbe` invocations at every generation,
requires byte-identical QBE, links that QBE, and compares the program output
with the checked-in `.out` file.

The valid cases cover:

- typed direct calls, mutable locals, conditionals, loops, and checked Integer
  arithmetic in `valid/control-flow.trb`;
- nominal record construction and projection plus homogeneous Integer Array
  construction, indexing, growth, and mutation in `valid/records-arrays.trb`;
- managed String concatenation and content inequality in
  `valid/strings-calls.trb`; and
- the compiler source closure itself, exercised by the bootstrap test outside
  this directory.

Each invalid `.source` file has an exact `.diag` result. The non-`.trb`
extension keeps intentionally malformed programs out of repository-wide source
formatting. Together they require the
lexer, parser, resolver, and checker to remain active and cover unsupported
characters, unfinished syntax, duplicate declarations, unresolved calls,
arity errors, type mismatches, and unsupported types. `emit-qbe` must return
the same diagnostic without emitting an executable function, proving that the
failure occurs before code generation. The Integer boundary case also keeps
the self-hosted compiler aligned with TypeRB's portable range rather than the
wider machine-word range.

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
