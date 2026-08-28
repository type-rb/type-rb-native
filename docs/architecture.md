# Architecture

## Purpose

TypeRB Native develops a TypeRB-specific native compiler and runtime while
keeping the supported language and reference compiler independent. Its
engineering objective is a self-hosted implementation that removes Go from the
ordinary bootstrap and application-build path while matching or improving the
practical tradeoff among build time, execution performance, and deployed binary
size after all required tooling is counted.

The experiment is not a port to a different host language. Native execution
and self-hosting are separate checkpoints, but both belong to the intended
path. The Go reference compiler bootstraps early artifacts and remains a
differential oracle. The completed compiler and runtime owned by this
repository are written in TypeRB and reproduce themselves without Go in the
ordinary release/bootstrap path.

## Ownership boundary

The [reference TypeRB repository](https://github.com/type-rb/type-rb) owns:

- syntax and normative language semantics;
- parsing, name resolution, type checking, and diagnostics;
- package resolution and portable standard-library contracts;
- the reference typed IR and supported Go, Ruby, and TypeScript backends; and
- the canonical cross-backend conformance behavior.

This repository owns only experimental native concerns:

- an independent TypeRB-authored frontend when the self-hosting gates reach it;
- bootstrap snapshot validation and lowering;
- Native MIR and its verifier;
- native data layout and target ABI profiles;
- optimization and backend adapters;
- object emission and linker integration;
- the experimental runtime; and
- native correctness, portability, and performance measurements.

The normal reference TypeRB build, test, and release paths must not depend on
this repository. A language-level change discovered here belongs in the
reference repository's normal design and review process. Until the independent
frontend exists, the reference implementation may provide a narrow snapshot
producer on a short-lived, removable experimental surface.

## Implementation-language boundary

Repository-owned executable compiler and runtime source is written in TypeRB.
Go, Rust, Zig, C, or another existing implementation language is not introduced
as the permanent host for those components. Generated C, assembly, object
files, or backend IR are outputs rather than maintained implementation source.

External tools remain allowed and must be accounted for. QBE or LLVM, an
assembler, a linker, an SDK, and system libraries do not violate self-hosting;
they are explicit dependencies of a TypeRB-authored compiler in the same way a
linker can be a dependency of another self-hosted language implementation.

## Pipeline

```text
                         reference repository
TypeRB source
    -> lossless tokens
    -> syntax AST
    -> resolver and type checker
    -> typed IR
    -> experimental bootstrap snapshot
                         native repository
    -> snapshot verifier
    -> Native MIR lowering
    -> MIR verifier
    -> target-independent optimization
    -> backend adapter
    -> object files
    -> linker + native runtime
    -> executable
```

Each boundary must preserve source origins so diagnostics and runtime failures
can eventually refer to authored TypeRB source.

The bootstrap snapshot is intentionally transitional. After native execution
and runtime viability are established, the repository gains its own
TypeRB-authored parser, resolver, checker, and lowering. The reproducible
self-hosting sequence is:

```text
reference Go compiler -> B0 from TypeRB compiler sources
B0                    -> B1
B1                    -> B2
compare(B1, B2)       -> equivalent under the reproducibility policy
```

Published native releases use a previously released native compiler as their
seed. Building the bootstrap seed from Go is a recovery/development path, not
an ordinary release requirement.

## Bootstrap snapshot

The bootstrap snapshot is a deterministic, versioned, target-neutral, data-only
interchange for the experiment. It is distinct from both the reference typed IR
and Native MIR.

It may eventually contain:

- normalized control flow and typed values;
- stable symbol and module identities;
- target-independent literals and semantic operations;
- explicit traps and required runtime capabilities; and
- source identifiers and spans.

It must not contain:

- parser, resolver, or mutable compiler objects;
- Go pointers, interfaces, callbacks, or process-local identities;
- unchecked or unresolved source;
- filesystem, network, environment, or process capabilities;
- backend-native instructions; or
- an implicit package-extension mechanism.

The consumer validates schema versions, resource limits, required features, and
all structural invariants. Unknown or unsupported input fails explicitly. While
experimental, producer and consumer revisions may be pinned exactly and the
format may change without compatibility adapters.

The first backend experiments should use hand-authored fixtures. A producer-side
bridge should be added to the reference compiler only after those fixtures prove
that code generation and the minimal runtime are worth connecting.

## Native MIR

Native MIR is an internal control-flow and value representation designed for
verification, optimization, layout, and code generation. It is owned by this
repository and is not a public TypeRB API or serialized package protocol.

The MIR should expose TypeRB semantics explicitly rather than relying on a
backend to infer them. Examples include checked integer operations, nullable or
tagged representations, failure traps, direct and indirect calls, allocation,
source origins, and runtime capability requirements.

Backend-specific instructions, object-format details, and linker behavior stay
below the MIR boundary. Existing backends must not force backend-specific
concepts into portable TypeRB source.

## Backend adapters

Candidate adapters consume the same verified, target-neutral MIR subset. QBE
is tried first to minimize the cost of the initial executable experiment.
Target lowering selects a versioned ABI profile for an operating system and
architecture. Backend comparisons on the same target use the same profile.

| Candidate | Experimental role |
| --- | --- |
| Cranelift | Balanced fast-codegen candidate for development and AOT builds |
| LLVM | Optimizing ceiling for release-oriented measurements |
| QBE | Compact-backend and small-toolchain comparison |
| Direct emitter | Limited lower-bound experiment for compile time and size |

The architecture permits comparison; it does not promise long-term support for
multiple backends. A production decision should prefer one default. A second
backend remains only if a distinct use case demonstrates a durable advantage
large enough to justify its correctness and maintenance matrix.

An ABI profile defines calling conventions, symbol identity, data layout,
unwind behavior, and GC metadata for one target. Small backend-specific shims
may implement the profile, but they must not fork runtime or language semantics.
Objects from different backend implementations could be linked only after they
conform to the same profile. Per-function mixed code generation and tiered JIT
compilation are therefore deferred.

## Runtime and ABI

A machine-code backend does not provide TypeRB's runtime. A promoted
full-language target would require accepted solutions for:

- strings, bytes, arrays, hashes, records, enums, unions, and nullable values;
- classes, interfaces, closures, and generic representation;
- allocation, ownership, garbage collection, and stack maps;
- failure traps, stack unwinding, and TypeRB source traces;
- module initialization and symbol visibility;
- filesystem, process, time, networking, and other portable runtime services;
- cancellation, scheduling, and concurrency; and
- native package integration, lifecycle, and error conversion through a
  separately accepted TypeRB design.

The initial runtime remains deliberately smaller: static data, scalar values,
simple aggregate layout, observable output, and deterministic process failure.
Gate 2 completes the heap-free aggregate layer before heap ownership and memory
management are added. This separation keeps record and tagged-value semantics
independent of the later allocation strategy.

Runtime semantics are shared across backend candidates. Target-specific ABI
profiles and small shims may differ, but the runtime must not be independently
reimplemented for every code generator.

## Linking and toolchain independence

Removing the Go toolchain does not automatically produce a self-contained
toolchain. An experiment may still use an assembler, system linker, bundled
linker, SDK, C ABI library, or backend sidecar. Reports must distinguish:

- no Go toolchain requirement;
- no external compiler requirement;
- no external linker requirement; and
- a single self-contained `trb` distribution.

Every required component counts toward build time and toolchain distribution
size. Dynamically supplied system libraries must be identified rather than
silently excluded from comparisons.

## Stability and promotion

No MIR, ABI profile, snapshot, object, cache, command, or runtime API in this
repository is stable. Official TypeRB packages must not depend on it.

Promotion to a supported TypeRB target is a separate decision. It would require
representative portable conformance, source-mapped diagnostics and failures,
runtime and package boundaries, reproducible builds, primary-platform support,
an end-to-end advantage after the complete toolchain is counted, and a
reproducible self-hosted compiler build whose ordinary path does not use Go.

The bootstrap bridge remains removable because the independent frontend will
eventually replace it, not because removal is the default project outcome.
Gates expose correctness, performance, and maintenance problems early enough to
improve the shared MIR, runtime, backend, or build pipeline before those choices
become public contracts.
