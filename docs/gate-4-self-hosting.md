# Gate 4 Behavioral Self-Hosting

Gate 4 establishes the first Go-independent compiler regeneration step. Its
registered acceptance criteria and performance bounds live in
[issue #20](https://github.com/type-rb/type-rb-native/issues/20), and the
bootstrap boundary is defined by
[Decision 0006](decisions/0006-behavioral-self-hosting-boundary.md).

## Status

Gate 4 is in progress. Gate 3 remains the latest completed checkpoint.

## Compiler source closure

The Gate 4 compiler is repository-owned executable source written in TypeRB.
It will contain distinct passes for:

1. ASCII-delimited lexical analysis with decoded UTF-8 String literal payloads;
2. syntax parsing into a deterministic internal program model;
3. lexical and declaration name resolution;
4. static type checking for the registered subset; and
5. deterministic QBE IL emission plus a native entry adapter.

The supported closure must be large enough to compile every checked-in compiler
source file through those same passes. The first closure supports top-level
functions and nominal records; typed positional parameters and results; local
bindings and assignment; direct calls; record construction and projection;
Boolean, portable Integer, String, and homogeneous Array values; conditionals;
loops; and observable output. Exact syntax and deferred constructs will be
listed here after the implementation corpus is fixed.

Unsupported declarations, expressions, types, member operations, or runtime
services fail with a stable Gate 4 diagnostic. There is no dynamic fallback,
unchecked `Any` representation, embedded compiler artifact, or source-specific
emission branch.

## Bootstrap ABI

The checked-in source exposes this repository-internal function:

```trb
def compiler_main(source: String, mode: String)
```

The native executable entry receives two host arguments, converts them to
managed Strings, and invokes that function. `mode` selects deterministic check
or QBE-emission behavior. This is an internal bootstrap ABI rather than a
portable TypeRB `main` signature. The authored `def main()` contract remains
unchanged, and no reference-repository or standard-library API is added.

QBE and the system assembler/linker remain outside the compiler executable.
The bootstrap harness records each process and counts these external tools.

## Stage contract

- **B0** is built from the TypeRB compiler sources by the pinned Go reference
  frontend, snapshot v4, and the existing native QBE path.
- **B1** is emitted by B0 from those same runtime-supplied sources.
- **B2** is emitted by B1 from those same runtime-supplied sources.

B1-to-B2 must not execute or link Go. B0, B1, and B2 must agree on all valid
outputs and invalid diagnostics in the registered corpus. Repeated QBE emission
at each stage must be byte-identical. Compiler executable equivalence is
measured but becomes mandatory only under Gate 5's normalization policy.

## Validation order

1. Fix the subset, bootstrap ABI, diagnostics, conformance inputs, and bounds.
2. Implement and test the TypeRB lexer, parser, resolver, and checker under the
   pinned reference compiler.
3. Implement QBE emission for the same checked model and execute representative
   programs.
4. Build B0 through snapshot v4 and the Gate 3 runtime.
5. Run B0-to-B1 and B1-to-B2, then compare the entire conformance corpus.
6. Run source-mutation and process-inventory checks.
7. Record timing, RSS, executable and toolchain sizes, revisions, and raw data.

The gate stops for review after every registered condition passes. Full
language coverage, project filesystem loading, package resolution, production
managed-runtime integration, a second target, and release artifact equivalence
remain later work.
