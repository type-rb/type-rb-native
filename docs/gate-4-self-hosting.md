# Gate 4 Behavioral Self-Hosting

Gate 4 establishes the first Go-independent compiler regeneration step. Its
registered acceptance criteria and performance bounds live in
[issue #20](https://github.com/type-rb/type-rb-native/issues/20), and the
bootstrap boundary is defined by
[Decision 0006](decisions/0006-behavioral-self-hosting-boundary.md).

## Status

Gate 4 is complete. B0, B1, B2, and the additional B3 fixed-point stage pass
the registered correctness and convergence checks. See the
[recorded result](../results/2026-08-28-gate4-self-host-darwin-arm64/README.md).

## Compiler source closure

The Gate 4 compiler is repository-owned executable source written in TypeRB.
It contains distinct passes for:

1. ASCII source lexical analysis and ASCII String literal payloads;
2. syntax parsing into a deterministic internal program model;
3. lexical and declaration name resolution;
4. static type checking for the registered subset; and
5. deterministic QBE IL emission plus a native entry adapter.

The supported closure must be large enough to compile every checked-in compiler
source file through those same passes. The first closure supports top-level
functions and nominal records; typed positional parameters and results; local
bindings and assignment; direct calls; record construction and projection;
Boolean, portable Integer, String, and homogeneous Array values; conditionals;
loops; and observable output.

The completed closure accepts one ASCII source unit containing nominal records
and top-level functions; positional typed parameters and results; mutable and
immutable local bindings; direct calls; record construction and projection;
Boolean, portable Integer, ASCII String, and homogeneous `Array<Integer>` /
`Array<String>` values; assignment; conditionals; loops; checked Integer
arithmetic; comparisons; String concatenation and content equality; Array
indexing, size, and push; and `puts` output. Non-ASCII literals, Float, tagged
values, closures, packages, multiple source units, filesystem discovery, and
the rest of the portable language remain outside this gate.

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
- **B3** is emitted by B2 as an additional fixed-point observation.

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
managed-runtime integration, and a second target remain Gate 6 work. Gate 5
owns the matched compiler baseline and release artifact normalization.

## Result

The compiler passes the checked-in valid, invalid, and mutation corpus at B0,
B1, and B2. B1, B2, and B3 emit byte-identical QBE. A direct system-shell
harness reproduces B2 using only B1, QBE, Clang's assembler/linker path, and
inspected system helpers; B1 has no process-spawn import or Go metadata.

Warm B1-to-B2 and B2-to-B3 medians are 0.711847 and 0.809224 seconds, a 12.0%
difference. Full-build RSS differs by 0.23%, stripped B1/B2 sizes are both
133,016 bytes, and the 536,440-byte native compiler-plus-QBE distribution is
99.827% smaller than the 310,535,890-byte recovery distribution.

The diagnostic Go backend build is substantially faster and uses less RSS.
The self-hosted compiler's process-lifetime allocator and parallel
source-sized tables are the clearest next optimization targets. These are Gate
5 concerns because the Go artifact and native adapter are not yet behaviorally
matched product compilers.
