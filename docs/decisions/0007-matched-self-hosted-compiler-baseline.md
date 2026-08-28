# 0007: Matched Self-Hosted Compiler Baseline Before Product Feasibility

## Status

Accepted for Gate 5.

## Context

Gate 4 established behavioral self-hosting, but its diagnostic Go comparison
did not execute the compiler. The checked-in compiler source still declared an
empty ordinary `main()`, so an optimized Go build could discard the compiler
entry path while the Native executable received a repository-internal entry
adapter and performed real lexing, parsing, resolution, checking, and QBE
emission. The resulting time and memory numbers identify possible work, but
they are not a valid implementation comparison.

The existing Gate 5 description also combined that unresolved comparison with
multi-module loading, a production CLI, the managed runtime, incremental
builds, package and native-library integration, a second target, debugging,
and maintenance evaluation. A miss would not identify which boundary caused
it. The project needs a smaller checkpoint that makes compiler performance
measurable before expanding the semantic and platform surface.

This is an internal compiler-experiment decision. It does not add TypeRB
syntax, change `def main()`, expose a compiler API, or promote a Native command.
The optimized Go comparison driver uses the existing portable
`trb/std/process.argv()` contract only in a generated comparison source.

## Decision

Gate 5 establishes a **matched self-hosted compiler baseline**.

The Native and optimized Go comparison executables use the same checked-in
TypeRB-authored compiler implementation and accept the same runtime source and
mode arguments. For the Go comparison, the measurement harness constructs a
deterministic source copy whose otherwise empty `main()` reads `argv()` and
calls the existing repository-internal `compiler_main(source, mode)` function.
The copy may change only the import and entry-driver surface. An automated
source comparison and executable behavior check must prove that every compiler
pass remains identical and active.

The Native executable retains the Gate 4 entry adapter during this gate. Both
adapters are reported explicitly, and driver-only time is kept visible where
it can be separated. This is a matched compiler-core comparison, not yet the
ordinary user-facing compiler command.

Gate 5 also replaces the Gate 4 compiler's source-sized parallel storage with
demand-sized storage where possible. The change must preserve checked bounds,
deterministic diagnostics, repeated QBE identity, behavioral self-hosting, and
the Go-free B1-to-B2 process graph. Process-lifetime allocation remains
permitted for this bounded one-shot compiler only if the registered peak-RSS
bound passes; it is not accepted as the production runtime.

The fixed-point policy has two levels:

1. B1, B2, and B3 must emit byte-identical QBE for identical compiler source.
2. B1 and B2 executables must compare equal after a documented normalization
   that removes only identified nondeterministic linker metadata. Code and data
   sections may not be excluded.

The broader **self-hosted product feasibility** checkpoint becomes Gate 6. It
retains representative multi-module applications, the ordinary file-oriented
CLI, production managed-runtime integration, incremental and reproducible
project builds, package and native-library boundaries, at least two primary
target environments, debugging and operational behavior, and maintenance
cost. A previous Native release remains its ordinary seed, and promotion still
requires a separate TypeRB design decision.

## Consequences

- Compiler build time and RSS can be compared without the Gate 4 dead-strip
  asymmetry.
- Storage optimization is evaluated against both a matched Go executable and
  adjacent Native generations before the compiler surface becomes broader.
- Gate 5 can diagnose the TypeRB-authored compiler, Native code generation,
  and runtime representation without pretending that a single-source argument
  adapter is a production CLI.
- Gate 6 remains the product-level decision point; moving it does not weaken or
  remove any of its requirements.
- The reference TypeRB repository remains unchanged and consumer-neutral.
- The matched Go distribution counts its prebuilt compiler executable and QBE,
  just as the Native distribution counts its prebuilt compiler and QBE. The Go
  toolchain used to create the comparison executable is recorded as bootstrap
  infrastructure, not charged to ordinary matched compiler execution.

## Alternatives considered

### Keep the original broad Gate 5

Rejected as an ordering choice. It would mix an invalid comparison baseline
with several independent frontend, runtime, package, target, and operations
questions, making misses expensive to diagnose.

### Compare the current Native compiler directly with the full reference compiler

Rejected for this checkpoint because they accept different language and
project surfaces and do different work. That comparison remains mandatory at
product feasibility, after the Native implementation can process the same
representative applications.

### Add a comparison-only entry API to the reference compiler

Rejected. The existing portable `argv()` contract can construct a functional
Go comparison without adding a consumer-specific reference-repository surface.

### Treat source-content arguments as the final compiler CLI

Rejected. They are useful for a controlled matched comparison, but ordinary
product use requires file and project loading, package resolution, output
management, external-tool orchestration, and stable diagnostics. Gate 6 owns
that complete boundary.
