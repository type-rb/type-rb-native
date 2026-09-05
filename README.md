# TypeRB Native

> [!WARNING]
> TypeRB Native is an experimental research prototype. It is not a supported
> TypeRB backend, runtime, or release target. Everything in this repository may
> change incompatibly or be removed without notice.

TypeRB Native develops a TypeRB-specific native compiler and runtime intended
to improve end-to-end build time, generated-program performance, and deployed
binary size relative to an optimized release executable produced by the
reference compiler's Go backend. Its long-term objective is a self-hosted
compiler whose repository-owned implementation is written in TypeRB and whose
ordinary release/bootstrap path does not require Go or another host language.
The repository remains experimental while that implementation is incomplete;
the gates are engineering checkpoints that keep correctness and whole-toolchain
performance visible as the implementation grows.

The [TypeRB repository](https://github.com/type-rb/type-rb) remains the source
of truth for the language specification, reference compiler, supported
backends, packages, and user documentation. This repository must preserve those
semantics; it does not define a native-only TypeRB dialect.

The current implementation identity is Native `0.1.0-dev`. Native versions are
managed independently from TypeRB versions; the strict
[compatibility manifest](compatibility/current.json) declares only the exact
TypeRB version and revision backed by current evidence. See
[Native versioning and compatibility](docs/versioning.md).

## Goals

- Test a native AOT pipeline without requiring the Go toolchain to compile a
  TypeRB application.
- Reach reproducible self-hosting: a native TypeRB compiler builds the next
  equivalent native TypeRB compiler from TypeRB source.
- Design a small Native MIR, target ABI profiles, data layout, and runtime.
- Keep TypeRB semantic facts and reusable optimization decisions in Native MIR
  rather than in a particular backend emitter.
- Compare multiple machine-code strategies behind the same MIR and semantics.
- Measure complete toolchains, including code generation, linking, runtime,
  sidecars, and distribution size.
- Match or exceed established statically typed language implementations on
  representative portable runtime workloads, while keeping the same-source Go
  path as a backend control rather than the final execution-performance ceiling.
- Preserve a credible path to a native implementation that is at least as
  practical as the Go backend, and use measured regressions to direct
  optimization work rather than treating early gates as disposable demos.

## Current status

The bounded TypeRB-authored compiler is self-hosted: ordinary Native-to-Native
builds reproduce compiler artifacts without Go. QBE, an assembler, a system
toolchain driver/linker, and system libraries remain explicit dependencies.
Experimental target profiles cover Darwin arm64, Linux arm64, and Linux amd64.

The ordinary compiler is not a complete implementation of TypeRB. The earlier
snapshot/recovery pipeline and the ordinary compiler have different coverage.
See the [capability map](https://type-rb.github.io/type-rb-native/) for the
measured boundary, not the highest completed gate number.

Current work moves portable optimization ownership from the direct QBE emitter
into verified Native MIR and improves representative runtime performance.
Pure Go parity remains a goal, not an achieved general result. Runtime and
compiler-build measurements are separate in the
[benchmark explorer](https://type-rb.github.io/type-rb-native/benchmarks/).
See [MIR status](docs/native-mir-optimization-status.md) for the migration and
[development history](docs/development-history.md) for dated checkpoints.

## Intended boundary

The ordinary path is TypeRB source → the TypeRB-authored compiler → QBE →
the explicit target toolchain → an executable. Within the compiler, verified
MIR is progressively replacing direct-emitter semantic ownership; it is not
yet the sole path for every supported operation.

The reference compiler remains the language oracle and a recovery tool.
Its versioned snapshot bridge is separate from ordinary Native builds.
See [Architecture](docs/architecture.md) for these boundaries.

## Backend experiments

QBE is the active adapter. Other adapters are measured alternatives, not
promised production backends. LLVM comparison remains deferred until shared
MIR and representative tests cover scalar, Array, allocation, and I/O behavior.
See the [development and validation plan](docs/experiment-plan.md).

## Repository layout

- `compiler/gate4/src/`: the current ordinary self-hosted compiler, not a
  frozen Gate 4 implementation.
- `src/`: snapshot/MIR adapters, runtime generation, recovery/comparison
  support, and tests; gate-numbered names do not mean unused code.
- `tools/` and `corpus/`: verification and measurement drivers and inputs.
- `docs/`: architecture, plans, current status, and historical decisions.
- `results/`: dated measurement evidence; `docs/capabilities/` powers Pages.

The [organization plan](docs/repository-organization.md) schedules early
documentation cleanup, dependency-led source organization, and incremental
compiler decomposition. Gate names will remain in historical evidence, not
serve as the permanent organization of active implementation code.

## Non-goals

This experiment does not promise full language or standard-library coverage,
production Web/Job support, a stable CLI or ABI, or a supported release target.
It does not replace external tools merely to claim self-hosting, introduce a
Native-only language dialect, or port repository-owned implementation to
another host language.

## Documentation

- [Documentation catalog](docs/README.md)
- [Architecture](docs/architecture.md)
- [Development and validation plan](docs/experiment-plan.md)
- [Repository organization and cleanup schedule](docs/repository-organization.md)
- [Current MIR status](docs/native-mir-optimization-status.md)
- [Native versioning and compatibility](docs/versioning.md)
- [TypeRB compatibility mapping](docs/type-rb-compatibility.md)
- [Contributing](CONTRIBUTING.md) and [Security](SECURITY.md)

## License

TypeRB Native is available under the [MIT License](LICENSE).
