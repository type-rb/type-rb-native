# TypeRB Native

> [!WARNING]
> TypeRB Native is an experimental research prototype. It is not a supported
> TypeRB backend, runtime, or release target. Everything in this repository may
> change incompatibly or be removed without notice.

TypeRB Native explores whether a TypeRB-specific native compiler and runtime
can improve end-to-end build time, generated-program performance, and deployed
binary size relative to an optimized release executable produced by the
reference compiler's Go backend. Its long-term objective is a self-hosted
compiler whose repository-owned implementation is written in TypeRB and whose
ordinary release/bootstrap path does not require Go or another host language.

The [TypeRB repository](https://github.com/type-rb/type-rb) remains the source
of truth for the language specification, reference compiler, supported
backends, packages, and user documentation. This repository must preserve those
semantics; it does not define a native-only TypeRB dialect.

## Goals

- Test a native AOT pipeline without requiring the Go toolchain to compile a
  TypeRB application.
- Reach reproducible self-hosting: a native TypeRB compiler builds the next
  equivalent native TypeRB compiler from TypeRB source.
- Design a small Native MIR, target ABI profiles, data layout, and runtime.
- Compare multiple machine-code strategies behind the same MIR and semantics.
- Measure complete toolchains, including code generation, linking, runtime,
  sidecars, and distribution size.
- Keep the experiment removable if it does not improve the practical tradeoff
  offered by the Go backend.

## Current status

Gate 0 implements the experimental boundary in TypeRB: strict decoding of
versioned, data-only bootstrap snapshots, lowering to Native MIR, MIR
verification, deterministic diagnostics, and source-origin preservation. It
does not yet generate or execute machine code and provides no production
runtime, stable ABI, stable artifact format, or compatibility guarantee.

Gate 1 will use a small, heap-free corpus with
functions, direct calls, control flow, scalar values, exact TypeRB integer and
failure behavior, simple static-layout values, and observable output.

## Intended boundary

```text
TypeRB source
    |
    v
reference TypeRB frontend
parse -> resolve -> check -> typed IR
    |
    v
experimental, versioned bootstrap snapshot
    |
    v
type-rb-native
validate -> Native MIR -> optimize -> codegen -> object -> link
    |                                                  |
    +---------------- TypeRB native runtime -----------+
```

The bootstrap snapshot is a temporary, data-only bridge. It is not the public
compiler tooling protocol, a package-extension API, or a stable serialization
of the reference compiler's internal typed IR. During early gates the Go
reference compiler may produce that bridge. Later gates replace the bridge's
frontend side with a TypeRB implementation in this repository. Native MIR
remains internal here.

The intended bootstrap sequence is:

```text
Go reference compiler -> B0 native compiler from TypeRB source
B0 native compiler    -> B1 native compiler
B1 native compiler    -> B2 native compiler
B1 and B2             -> reproducibly equivalent artifacts
```

The Go compiler remains a differential oracle, but it is not part of the
ordinary self-hosted release/bootstrap chain. External code generators,
assemblers, linkers, SDKs, and system libraries may remain explicit toolchain
dependencies.

See [Architecture](docs/architecture.md) for the ownership and pipeline
boundaries.

## Backend experiments

QBE is the first planned executable path because it gives the lowest-cost test
of the TypeRB runtime and ABI hypothesis. Candidate roles under consideration
are:

- [Cranelift](https://cranelift.dev/) as a balanced fast-codegen candidate;
- [LLVM](https://llvm.org/) as a high-optimization comparison;
- [QBE](https://c9x.me/compile/) as a compact-backend comparison; and
- a limited direct emitter as a compile-time and toolchain-size lower bound.

These are experimental adapters, not four promised production backends. Every
candidate must consume the same supported MIR subset and, for a same-target
comparison, the same target ABI profile. A candidate may be removed when it
fails a correctness, performance, distribution, portability, or maintenance
gate. More than one implementation may remain only when distinct development,
release, or target use cases show a durable benefit that justifies the
maintenance cost.

See the [experiment plan](docs/experiment-plan.md) for correctness gates,
measurement rules, and abandonment criteria.

## Non-goals

The initial gates do not attempt to:

- port the compiler to Rust, Zig, or another host implementation language;
- replace external code generators, assemblers, linkers, SDKs, or system
  libraries merely to claim self-hosting;
- implement the full TypeRB frontend before native execution feasibility has
  passed its earlier gates;
- commit TypeRB to a supported native mode;
- expose mutable compiler internals or backend hooks as a package API;
- support the full standard library, Web, ORM, Jobs, or native package
  ecosystem;
- support every operating system and architecture;
- promise a JIT, VM, Wasm runtime, debugger, or production garbage collector;
- claim an advantage over Go without reproducible end-to-end measurements.

External code generators, assemblers, and linkers may be used as experimental
components. Repository-owned compiler, MIR, ABI, and runtime implementation
source is written in TypeRB. Normative semantics remain in the reference
repository.

## Documentation

- [Architecture](docs/architecture.md)
- [Experiment plan](docs/experiment-plan.md)
- [Decision 0001: Experimental native toolchain boundary](docs/decisions/0001-experimental-native-toolchain.md)
- [Decision 0002: TypeRB-owned self-hosting](docs/decisions/0002-typerb-owned-self-hosting.md)
- [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md)

## License

TypeRB Native is available under the [MIT License](LICENSE).
