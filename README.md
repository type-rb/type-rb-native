# TypeRB Native

> [!WARNING]
> TypeRB Native is an experimental research prototype. It is not a supported
> TypeRB backend, runtime, or release target. Everything in this repository may
> change incompatibly or be removed without notice.

TypeRB Native explores whether a TypeRB-specific native compiler and runtime
can improve end-to-end build time, generated-program performance, and deployed
binary size relative to an optimized release executable produced by the
reference compiler's Go backend.

The [TypeRB repository](https://github.com/type-rb/type-rb) remains the source
of truth for the language specification, reference compiler, supported
backends, packages, and user documentation. This repository must preserve those
semantics; it does not define a native-only TypeRB dialect.

## Goals

- Test a native AOT pipeline without requiring the Go toolchain to compile a
  TypeRB application.
- Design a small Native MIR, target ABI profiles, data layout, and runtime.
- Compare multiple machine-code strategies behind the same MIR and semantics.
- Measure complete toolchains, including code generation, linking, runtime,
  sidecars, and distribution size.
- Keep the experiment removable if it does not improve the practical tradeoff
  offered by the Go backend.

## Current status

The repository currently contains design and experiment policy only. It does
not compile TypeRB programs and does not provide a production runtime, stable
ABI, stable artifact format, or compatibility guarantee.

The first implementation milestone will use a small, heap-free corpus with
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
of the reference compiler's internal typed IR. Native MIR remains internal to
this repository.

See [Architecture](docs/architecture.md) for the ownership and pipeline
boundaries.

## Backend experiments

Candidate strategies under consideration are:

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

The initial experiment does not attempt to:

- replace the Go implementation of the reference compiler;
- port the compiler to Rust, Zig, or another host implementation language;
- make self-hosting a prerequisite for native-code feasibility;
- commit TypeRB to a supported native mode;
- expose mutable compiler internals or backend hooks as a package API;
- support the full standard library, Web, ORM, Jobs, or native package
  ecosystem;
- support every operating system and architecture;
- promise a JIT, VM, Wasm runtime, debugger, or production garbage collector;
- claim an advantage over Go without reproducible end-to-end measurements.

External code generators, assemblers, and linkers may be used as experimental
components. This experiment remains responsible for preserving TypeRB semantics
and for implementing its MIR, ABI profiles, and runtime. Normative semantics
remain in the reference repository.

## Documentation

- [Architecture](docs/architecture.md)
- [Experiment plan](docs/experiment-plan.md)
- [Decision 0001: Experimental native toolchain boundary](docs/decisions/0001-experimental-native-toolchain.md)
- [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md)

## License

TypeRB Native is available under the [MIT License](LICENSE).
