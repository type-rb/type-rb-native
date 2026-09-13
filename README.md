# TypeRB Native

> [!NOTE]
> TypeRB Native is in active development toward production use. Language and
> package coverage is incomplete, and current development builds do not yet
> provide stable CLI, ABI, or release-support guarantees.

TypeRB Native develops a self-hosted TypeRB compiler and toolchain for practical
application development. The goal is full TypeRB language, standard-library and
official-package coverage, Go/Ruby/TypeScript emission and execution, and Native
executables. Native runtime performance, application build time and executable
size should outperform equivalent Pure Go programs on representative workloads.

The repository-owned compiler and runtime are written in TypeRB. Ordinary Native
self-hosting and application builds do not require Go or another host language.
Correctness, reproducibility and complete-toolchain measurements guide progress
toward the full implementation; current coverage is described separately below.

The [TypeRB repository](https://github.com/type-rb/type-rb) remains the source
of truth for the language specification, reference compiler, supported
backends, packages, and user documentation. This repository must preserve those
semantics; it does not define a native-only TypeRB dialect.

The current implementation identity is Native `0.1.0-dev`. Native versions are
managed independently from TypeRB versions; the strict
[compatibility manifest](compatibility/current.json) declares only the exact
TypeRB version and revision backed by current evidence. See
[Native versioning and compatibility](docs/versioning.md).

## Try the native executable

On Darwin arm64 or Linux arm64, `./trbn` builds the native executable when
needed and starts a REPL. `./trbn run` runs the example project, and
`./trbn build --compile` creates an executable. The default mode is `trb`;
other explicit modes are rejected. Go is not required for this bootstrap.

See the [CLI guide](docs/native-cli.md) for prerequisites,
commands, limitations, and manually dispatched CI binary artifacts.

## Goals

- Cover the reference language, standard library and official packages, including
  `trb/web`, `trb/orm` and `trb/jobs`, as their platform dependencies are implemented.
- Emit and run Go, Ruby and TypeScript as well as Native executables from the
  TypeRB-authored toolchain, preserving the same language semantics.
- Deliver a practical Native backend with a stable CLI, documented ABI contracts
  where exposed, supported release targets and a release/security maintenance policy.
- Maintain reproducible self-hosting: a native TypeRB compiler builds the next
  equivalent native TypeRB compiler from TypeRB source.
- Keep TypeRB semantic facts and reusable optimizations in verified MIR and
  target-independent passes, with small modules organized by responsibility.
- Outperform equivalent Pure Go programs in Native execution time, application
  build time and executable size across representative workloads. Also compare
  established statically typed implementations and the same-source TypeRB Go path.
- Measure complete toolchains, including code generation, linking, runtime,
  sidecars, distribution size and compiler self-build costs.

These are development targets. The [MIR consolidation roadmap](docs/mir-consolidation.md)
sets the current milestone and the evidence needed to qualify progress.

## Current status

The current TypeRB-authored compiler is self-hosted: ordinary Native-to-Native
builds reproduce compiler artifacts without Go. QBE, an assembler, a system
toolchain driver/linker, and system libraries remain explicit dependencies.
Current internal target profiles cover Darwin arm64, Linux arm64, and Linux amd64.

The ordinary compiler is not a complete implementation of TypeRB. The earlier
snapshot/recovery pipeline and the ordinary compiler have different coverage.
See the [capability map](https://type-rb.github.io/type-rb-native/) for the
current measured boundary.

Current work consolidates supported ordinary features into verified MIR,
completes needed basic language coverage and splits large implementation files
by responsibility. See the [MIR consolidation milestone](docs/mir-consolidation.md)
and [basic language coverage plan](docs/native-language-coverage.md). Detailed
performance qualification follows coherent architecture milestones.
The current spectral-norm result exceeds Pure Go; broader runtime parity remains
a goal. The later [numeric regression recovery](docs/native-numeric-regression-recovery.md)
confirms that accepted main has restored n-body and fannkuch against the former
published baseline while retaining the spectral improvement. Application runtime
and compilation measurements are separate in the
[benchmark explorer](https://type-rb.github.io/type-rb-native/benchmarks/).
See [MIR status](docs/native-mir-optimization-status.md) for the migration and
[development history](https://github.com/type-rb/type-rb-native/blob/7726ff18e9230cd149e9f0c317577f6429f907fc/docs/development-history.md) for dated checkpoints.

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

- `compiler/src/`: the current ordinary self-hosted compiler.
- `src/`: snapshot/MIR adapters, runtime generation, recovery/comparison
  support, and tests; historical names do not mean unused code.
- `tools/` and `corpus/`: verification and measurement drivers and inputs.
- `docs/`: architecture, plans, current status, and historical decisions.
- `results/`: registered active evidence with retirement and size limits;
  `docs/capabilities/` powers Pages.

The [organization plan](docs/repository-organization.md) schedules early
documentation cleanup, dependency-led source organization, and incremental
compiler decomposition. Historical records retain the names from their exact revisions.

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
