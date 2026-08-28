# 0003: Use QBE 1.3 and a Disposable Darwin arm64 Profile for Gate 1

## Status

Accepted for Gate 1 only.

## Context

The first executable gate needs to test TypeRB scalar semantics, runtime
behavior, and native toolchain costs before investing in a broad backend or
stable ABI. Building several complete backends would spend effort before the
shared MIR and runtime questions are understood.

The maintainer also rejected adding a public `def main(): Integer` form merely
to simplify the bootstrap. Temporary implementation structure is acceptable,
but the experiment must not leave an unnatural language feature behind.

## Decision

Gate 1 uses QBE 1.3 at release commit
`c0818978acec60ebb6167fade60fb7012cbf20ca`, verified by release archive SHA-256
`d587905d620dc5e1d2bfa7c2cc642b9b837aa89a3188c6e37b53d756cf66e320`.
The only target is QBE `arm64_apple`, behind the internal and disposable
`darwin-arm64-v0` ABI profile.

The TypeRB-authored emitter supplies an exported C `main` wrapper around a
no-argument, `Void` Native MIR entry function. That wrapper is below the
language boundary and does not change TypeRB `main` syntax or semantics.

Gate 1 is restricted to heap-free scalar execution. Static-layout records and
tagged values move to Gate 2. LLVM, Cranelift, direct machine-code emission, C
emission, and additional targets remain out of scope until Gate 1 measurements
identify a concrete reason to test them.

## Consequences

- QBE and the system assembler/linker remain explicit external dependencies.
- The initial ABI and runtime failure surface can be replaced incompatibly.
- A small hand-authored snapshot corpus must execute before a producer is added
  to the reference repository.
- Passing this decision's vertical slice justifies Gate 1B integration; it does
  not select QBE for production or demonstrate final self-hosted performance.
