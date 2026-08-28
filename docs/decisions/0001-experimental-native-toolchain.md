# 0001: Experimental Native Toolchain Boundary

Status: accepted for the initial experiment

Self-hosting scope is amended by
[Decision 0002](0002-typerb-owned-self-hosting.md). This decision still defines
the repository and experimental compiler boundary.

## Context

The reference TypeRB compiler emits Go, Ruby, and TypeScript from one checked
typed IR. The Go target already provides a mature native runtime and toolchain,
but compiling a TypeRB application currently relies on the Go toolchain and
inherits Go's runtime, layout, linking, and binary-size tradeoffs.

TypeRB may be able to use its closed type information and portable semantics to
reduce end-to-end build time, generated-program execution time, or deployed
binary size. That outcome is not known. Rewriting the existing frontend or
committing the main repository to a native mode before measuring code generation
and runtime feasibility would create a large compatibility and maintenance
burden.

## Decision

Create `type-rb/type-rb-native` as a separate, public, experimental research
repository.

The reference `type-rb` repository remains authoritative for language syntax,
semantics, checking, diagnostics, packages, supported backends, and conformance.
It must not depend on this experiment for ordinary builds or releases.

The native repository owns an internal Native MIR, target ABI profiles, data layout,
backend adapters, object and linker integration, the experimental runtime, and
native-specific measurements.

Initial work begins with hand-authored data-only fixtures. If that vertical
slice succeeds, the reference compiler may add a narrow, explicitly
experimental bootstrap snapshot producer. The snapshot is versioned and may
be exact-revision pinned, but it is not a public package-extension API or a
stable serialization of internal typed IR.

LLVM, Cranelift, QBE, and a limited direct emitter may be compared behind one
verified Native MIR. Same-target comparisons use the same versioned ABI profile.
These candidates are not promised production backends. A candidate may be
removed when it fails a correctness, performance, distribution, portability,
or maintenance gate.

The experiment may use external backend or linker components. It is a
TypeRB-specific native implementation, not a port of the reference compiler to
another host language.

## Consequences

- Native compiler and runtime work can evolve without destabilizing supported
  TypeRB releases.
- The Go implementation remains the bootstrap compiler and differential oracle;
  the TypeRB specification and accepted conformance behavior remain normative.
- Native MIR and runtime design can be discarded without preserving a public
  compatibility surface if the experiment fails.
- Cross-repository coordination requires an explicit bootstrap snapshot and
  exact version pinning while the boundary is unstable.
- Correctness and benchmark infrastructure must compare native behavior against
  the reference implementation.
- This repository remains responsible for its experimental runtime, ABI
  profiles, GC, source mapping, and linking even when a third-party code
  generator is used. Package interoperability requires a separate TypeRB
  design decision.
- Promotion to a supported mode requires a later, separate decision.

## Alternatives considered

### Long-lived branch in `type-rb`

Rejected for the main experiment because native runtime, code generation,
benchmarking, bootstrap, and release concerns may evolve for an extended period
without being ready to merge. Focused producer-side changes still belong in
short-lived feature branches in the reference repository.

### Rewrite the complete compiler before code generation

Rejected because it duplicates a working parser, resolver, checker, diagnostics,
and tooling before answering the native runtime and backend feasibility
question.

This rejection concerns sequencing, not the final implementation boundary.
Decision 0002 requires a TypeRB-authored frontend after earlier native
execution and runtime gates have justified that investment.

### Publish the existing typed IR as a stable API

Rejected because it would freeze reference compiler implementation details and
couple packages or tools to invariants they cannot safely maintain.

### Select one backend before measurement

Rejected because LLVM, Cranelift, QBE, and direct emission occupy different
build-time, runtime-performance, distribution-size, portability, and
maintenance tradeoffs. Small common-gate experiments can narrow the choice
without implementing every candidate to production completeness.
