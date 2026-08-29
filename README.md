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

## Goals

- Test a native AOT pipeline without requiring the Go toolchain to compile a
  TypeRB application.
- Reach reproducible self-hosting: a native TypeRB compiler builds the next
  equivalent native TypeRB compiler from TypeRB source.
- Design a small Native MIR, target ABI profiles, data layout, and runtime.
- Compare multiple machine-code strategies behind the same MIR and semantics.
- Measure complete toolchains, including code generation, linking, runtime,
  sidecars, and distribution size.
- Preserve a credible path to a native implementation that is at least as
  practical as the Go backend, and use measured regressions to direct
  optimization work rather than treating early gates as disposable demos.

## Current status

Gate 0 implements the experimental boundary in TypeRB: strict decoding of
versioned, data-only bootstrap snapshots, lowering to Native MIR, MIR
verification, deterministic diagnostics, and source-origin preservation.

Gate 1 is complete at its experimental checkpoint. A pinned, process-based
reference producer now connects real TypeRB source to snapshot v2, verified
heap-free scalar MIR, TypeRB-authored QBE emission, and working `darwin/arm64`
executables. The differential corpus covers functions, direct calls, block
parameters, branches, loops, Boolean, portable Integer including checked power,
binary64 Float, static UTF-8 output, and deterministic arithmetic failure.

On the recorded Apple M2 Pro Gate 1 run, native warm build time improved by
30.5% to 36.3%, stripped executable size improved by 96.85%, and the worst
runtime result was a 16.0% regression. See the
[Gate 1 result](results/2026-08-28-gate1-qbe-darwin-arm64/README.md).

Gate 2 is also complete. Snapshot v3 connects real TypeRB records, nested
records, tagged values, `Result`, `try`, aggregate calls and returns, and
parallel aggregate block arguments to the native path. The measured
five-million-iteration record kernel is 17.6% slower than the stronger Go
baseline, within the registered 25% bound; the two smaller cases are faster.
Warm build time improves by 26.0% to 29.5%, stripped executable size improves
by 96.85%, and observed build and runtime peak RSS remain below both Go paths.
See the [Gate 2 result](results/2026-08-28-gate2-qbe-darwin-arm64/README.md).

Gate 3 is complete under the pre-registered scope in
[issue #13](https://github.com/type-rb/type-rb-native/issues/13). It adds
managed UTF-8 Strings, mutable Arrays, closures, and cycle-reclaiming tracing
collection before broader runtime and self-hosting work. The pinned version 4
producer is now connected to a differential source corpus, and repeated builds
reproduce the snapshot, decoded MIR structure, QBE IL, assembly, and executable.
The registered source cycle triggers three automatic collections and satisfies
the reclamation and live-set checks. Warm builds improve by 13.0% to 22.9%,
stripped executable size improves by 96.82% to 96.83%, every runtime remains
within 21.1% of the stronger Go result, and observed runtime RSS is lower. See
the [Gate 3 result](results/2026-08-28-gate3-qbe-darwin-arm64/README.md).
These results do not select QBE for production or measure the final self-hosted
compiler. The current path provides no production runtime, stable ABI, stable
artifact format, or compatibility guarantee.

Gate 4 is complete. The bounded TypeRB-authored lexer, parser, resolver,
checker, emitter, and driver reach a byte-identical B1/B2/B3 QBE fixed point;
the valid, invalid, and mutation corpus passes at every required stage; and the
ordinary B1-to-B2 process path contains no Go or reference compiler. Registered
build-time, RSS, size, and distribution bounds pass. See the
[Gate 4 implementation boundary](docs/gate-4-self-hosting.md) and
[recorded result](results/2026-08-28-gate4-self-host-darwin-arm64/README.md).

Gate 5 is complete under the pre-registered scope in
[issue #29](https://github.com/type-rb/type-rb-native/issues/29). The functional
Native and optimized Go artifacts execute the same TypeRB-authored compiler
logic; demand-sized storage reduces Native direct RSS below matched Go; and
Native improves direct time by 99.50%, end-to-end build time by 98.11%,
stripped compiler size by 94.46%, and compiler-plus-QBE distribution size by
82.18%. B1/B2/B3 QBE and normalized B1/B2 executables converge. See the
[Gate 5 result](results/2026-08-29-gate5-matched-compiler-darwin-arm64/README.md).

Gate 6A is complete under the pre-registered scope in
[issue #35](https://github.com/type-rb/type-rb-native/issues/35). Its first
self-emitted compiler entry reads a source file directly for `check` and
`emit-qbe`, routes diagnostics and operational errors to stderr with distinct
statuses, and retains the source-content form only as an explicit hidden
recovery and differential adapter. Correctness coverage includes the compiler
source, every existing valid, invalid, and mutation input, and a source file
larger than 512 KiB. File-input median time improves by 38.69% for B1 and
36.72% for B2 versus hidden input, median RSS is lower, B1/B2 time and RSS
differ by 0.14%, and stripped size grows by 0.16%. See the
[Gate 6A file entry](docs/gate-6-file-cli.md) and
[recorded result](results/2026-08-29-gate6a-file-entry-darwin-arm64/README.md).

Gate 6B is complete under the pre-registered scope in
[issue #39](https://github.com/type-rb/type-rb-native/issues/39). Its
single-file `build` entry owns QBE emission, directly invokes explicitly
supplied QBE and C toolchain paths without a shell, atomically publishes the
requested executable, and cleans every intermediate. Native median build time
is only 1.41% higher for B1 and 3.13% higher for B2 than the external recipe;
median RSS is 0.63% and 0.27% higher; B1/B2 time and RSS converge within 0.42%;
and all four application outputs are byte-identical. The stripped compiler
grows by 11.38%, within its 15% bound. See the
[Gate 6B single-file build](docs/gate-6-single-file-build.md) and
[recorded result](results/2026-08-29-gate6b-single-file-build-darwin-arm64/README.md).

Gate 6C is complete at measured revision
`622d5931e677f7b9283c073021ac0ef39fafa1a5`. Each Native-built compiler is the
actual executable seed of the next ordinary build, and B2, B3, and B4 are
byte-identical. Adjacent median time and RSS differ by at most 1.03% and 0.67%,
every median remains within 1.10% of its Gate 6B baseline, and stripped code
does not grow. Recovery provenance remains outside the ordinary Go-free chain.
See the [Gate 6C Native bootstrap closure](docs/gate-6-native-bootstrap.md) and
[recorded result](results/2026-08-29-gate6c-native-bootstrap-darwin-arm64/README.md).

Gate 6D is complete at measured revision
`68497f68ed1c3770c2a457790a6519962a2cb921`. The same TypeRB-authored compiler,
QBE IL fixed point, runtime semantics, and conformance corpus close an exact
B1-to-B2-to-B3-to-B4 chain under `linux-arm64-v0`. The generated compilers are
byte-identical at 175,920 bytes. Native median time differs from the equivalent
external recipe by at most 2.55%, adjacent Native generations by at most 0.88%,
and median RSS by at most 0.35%. See the
[Gate 6D Linux arm64 plan](docs/gate-6-linux-arm64.md),
[measurement harness](tools/gate6d-benchmark/README.md), and
[recorded result](results/2026-08-29-gate6d-native-bootstrap-linux-arm64/README.md).

Gate 6E is complete at measured revision
`b2b4740f39571dc35af9199dae817d94912b7a47`. Its TypeRB-authored file
commands load the entry module plus the transitive closure of explicit named
project imports and preserve per-module declaration identity. The
representative Native executable builds 44.89% faster, uses 48.22% less build
RSS, runs 13.70% slower, uses 65.32% less runtime RSS, and is 97.82% smaller
than optimized Go. B2/B3/B4 are byte-identical on Darwin and Linux arm64. See
the [Gate 6E file-root plan](docs/gate-6-file-root-modules.md) and
[recorded result](results/2026-08-29-gate6e-file-root-darwin-linux-arm64/README.md).

Gate 6F is complete at measured revision
`7cb7e85c0b5bff14157dc1a686829c010d095b70`. The canonical TypeRB-authored
compiler is an explicit three-module closure, and ordinary multi-file B2, B3,
and B4 outputs are byte-identical on Darwin and Linux arm64. Darwin multi-file
self-build time is 21.56% above the Gate 6C baseline but 0.37% faster than the
temporary flat comparator; RSS is effectively flat in both comparisons, and
both compilers strip to 199,992 bytes. The Gate 6E application retains exact
bytes and behavior. See the
[Gate 6F multi-file compiler plan](docs/gate-6-multifile-compiler.md),
[measurement harness](tools/gate6f-benchmark/README.md), and
[recorded result](results/2026-08-29-gate6f-multifile-compiler-darwin-linux-arm64/README.md).

Gate 6G is complete at measured revision
`8bcc2a6e1c5ecede5f07c2dda63a4d4d82631375`. Canonical direct QBE emission
improves by 30.80%, complete build time by 5.95%, and 6,000-function emission
by 53.49%, with bounded RSS and a 200,008-byte stripped compiler. Exact Darwin
and Linux arm64 replacement chains and representative application identity
pass. See the [Gate 6G symbol-lookup plan](docs/gate-6-symbol-lookup.md),
[Decision 0014](docs/decisions/0014-indexed-function-lookup.md), and
[recorded result](results/2026-08-29-gate6g-symbol-lookup-darwin-linux-arm64/README.md).

Gate 6H is complete at measured revision
`e39f774237a6306d7cd46b09941367c42816c628`. On the exact 1,025-file project,
direct checking improves by 41.96%, QBE emission by 39.92%, and the complete
Native build by 16.16%, with lower median RSS. The candidate builds the same
project 85.79% faster and with 92.93% less peak RSS than the pinned optimized
Go path, and its stripped application is 97.00% smaller. Exact Darwin and
Linux arm64 replacement chains pass without widening the language, runtime,
CLI, project, package, or external-tool contract. See the
[Gate 6H module-graph plan](docs/gate-6-module-graph.md),
[Decision 0015](docs/decisions/0015-indexed-module-graph.md), and
[recorded result](results/2026-08-29-gate6h-module-graph-darwin-linux-arm64/README.md).

Gate 6I is complete at measured implementation revision
`cd2335e6472b4daca8d631b17b889a094959c2f2`. The existing TypeRB binary64
`Float` scalar path now runs through the ordinary self-hosted frontend and QBE
emitter, including safe Integer widening and signed-zero, infinity, and NaN
behavior. On the fixed workload, Native builds 41.37% faster and with 48.35%
less peak RSS than optimized Go, runs 10.60% slower with 65.60% less peak RSS,
and produces a 96.80% smaller stripped executable. It remains within every
registered Go-parity and canonical compiler guardrail and closes exact Darwin
and Linux arm64 replacement chains. See the
[Gate 6I Float plan](docs/gate-6-float.md),
[Decision 0016](docs/decisions/0016-self-hosted-float-scalar-path.md), and
[recorded result](results/2026-08-29-gate6i-float-darwin-linux-arm64/README.md).

Gate 6J is registered in
[issue #74](https://github.com/type-rb/type-rb-native/issues/74). It extends
the existing self-hosted Array runtime with `Array<Float>`, including safe
Integer element widening, common numeric literal inference, growth, indexing,
mutation, nested Arrays, and binary64 payload operations. The fixed five-
million-element workload must remain competitive with optimized Go for build
time, runtime, memory, and executable size while the compiler fixed point and
existing applications stay exact. See the
[Gate 6J Float Array plan](docs/gate-6-float-arrays.md) and
[Decision 0017](docs/decisions/0017-self-hosted-float-arrays.md).

Configured project discovery, production runtime integration,
package/native-library boundaries, incremental builds, toolchain discovery,
debugging, maintenance evaluation, and additional primary targets remain in
the broader Gate 6 product-feasibility scope.

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

See the [development and validation plan](docs/experiment-plan.md) for
correctness gates, measurement rules, and backend selection criteria.

## Non-goals

The initial gates do not attempt to:

- port the compiler to Rust, Zig, or another host implementation language;
- replace external code generators, assemblers, linkers, SDKs, or system
  libraries merely to claim self-hosting;
- implement the full TypeRB frontend before the shared native value model and
  runtime boundaries are concrete enough to support it;
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
- [Development and validation plan](docs/experiment-plan.md)
- [Gate 1 QBE vertical slice](docs/gate-1-qbe.md)
- [Gate 1 QBE Darwin arm64 result](results/2026-08-28-gate1-qbe-darwin-arm64/README.md)
- [Gate 2 heap-free aggregate value model](docs/gate-2-aggregates.md)
- [Gate 2 QBE Darwin arm64 result](results/2026-08-28-gate2-qbe-darwin-arm64/README.md)
- [Gate 3 managed runtime](docs/gate-3-managed-runtime.md)
- [Gate 4 behavioral self-hosting](docs/gate-4-self-hosting.md)
- [Gate 5 matched self-hosted compiler baseline](docs/gate-5-matched-compiler.md)
- [Gate 5 matched compiler Darwin arm64 result](results/2026-08-29-gate5-matched-compiler-darwin-arm64/README.md)
- [Gate 6A file-oriented compiler entry](docs/gate-6-file-cli.md)
- [Gate 6A file-entry Darwin arm64 result](results/2026-08-29-gate6a-file-entry-darwin-arm64/README.md)
- [Gate 6B Native single-file build](docs/gate-6-single-file-build.md)
- [Gate 6B Native single-file build Darwin arm64 result](results/2026-08-29-gate6b-single-file-build-darwin-arm64/README.md)
- [Gate 6C Native-to-Native bootstrap closure](docs/gate-6-native-bootstrap.md)
- [Gate 6C Native-to-Native bootstrap Darwin arm64 result](results/2026-08-29-gate6c-native-bootstrap-darwin-arm64/README.md)
- [Gate 6D Linux arm64 target chain](docs/gate-6-linux-arm64.md)
- [Gate 6D Linux arm64 target-chain result](results/2026-08-29-gate6d-native-bootstrap-linux-arm64/README.md)
- [Gate 6E file-root multi-module executables](docs/gate-6-file-root-modules.md)
- [Gate 6E file-root Darwin/Linux arm64 result](results/2026-08-29-gate6e-file-root-darwin-linux-arm64/README.md)
- [Gate 6F multi-file self-hosted compiler](docs/gate-6-multifile-compiler.md)
- [Gate 6F multi-file self-hosted compiler Darwin/Linux arm64 result](results/2026-08-29-gate6f-multifile-compiler-darwin-linux-arm64/README.md)
- [Gate 6G indexed function lookup](docs/gate-6-symbol-lookup.md)
- [Gate 6G indexed function-lookup Darwin/Linux arm64 result](results/2026-08-29-gate6g-symbol-lookup-darwin-linux-arm64/README.md)
- [Gate 6H scalable file-root module graph](docs/gate-6-module-graph.md)
- [Gate 6H scalable module-graph Darwin/Linux arm64 result](results/2026-08-29-gate6h-module-graph-darwin-linux-arm64/README.md)
- [Gate 6I self-hosted Float scalar path](docs/gate-6-float.md)
- [Gate 6I self-hosted Float Darwin/Linux arm64 result](results/2026-08-29-gate6i-float-darwin-linux-arm64/README.md)
- [Gate 6J self-hosted Float Arrays](docs/gate-6-float-arrays.md)
- [Decision 0001: Experimental native toolchain boundary](docs/decisions/0001-experimental-native-toolchain.md)
- [Decision 0002: TypeRB-owned self-hosting](docs/decisions/0002-typerb-owned-self-hosting.md)
- [Decision 0003: Gate 1 QBE and Darwin arm64 profile](docs/decisions/0003-gate-1-qbe-target.md)
- [Decision 0004: Sustained native implementation and staged Gate 2](docs/decisions/0004-sustained-native-development.md)
- [Decision 0005: Managed references and tracing GC](docs/decisions/0005-managed-runtime-and-tracing-gc.md)
- [Decision 0006: Behavioral self-hosting boundary](docs/decisions/0006-behavioral-self-hosting-boundary.md)
- [Decision 0007: Matched self-hosted compiler baseline](docs/decisions/0007-matched-self-hosted-compiler-baseline.md)
- [Decision 0008: File-oriented Native compiler entry](docs/decisions/0008-file-oriented-compiler-entry.md)
- [Decision 0009: Native-owned single-file executable build](docs/decisions/0009-native-single-file-build.md)
- [Decision 0010: Native-to-Native bootstrap closure](docs/decisions/0010-native-bootstrap-closure.md)
- [Decision 0011: Linux arm64 target profile](docs/decisions/0011-linux-arm64-target-profile.md)
- [Decision 0012: File-root module closure](docs/decisions/0012-file-root-module-closure.md)
- [Decision 0013: Multi-file self-hosted compiler closure](docs/decisions/0013-multi-file-self-hosted-compiler.md)
- [Decision 0014: Indexed self-hosted function lookup](docs/decisions/0014-indexed-function-lookup.md)
- [Decision 0015: Indexed file-root module graph](docs/decisions/0015-indexed-module-graph.md)
- [Decision 0016: Self-hosted Float scalar path](docs/decisions/0016-self-hosted-float-scalar-path.md)
- [Decision 0017: Self-hosted Float Arrays](docs/decisions/0017-self-hosted-float-arrays.md)
- [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md)

## License

TypeRB Native is available under the [MIT License](LICENSE).
