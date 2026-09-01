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

Gate 6J is complete at measured implementation revision
`914f4f592f344111b7a790aac00aecbf0d411d11`. The existing self-hosted Array
runtime now carries `Array<Float>`, including safe Integer element widening,
common numeric literal inference, growth, indexing, mutation, nested Arrays,
and binary64 payload operations. On the fixed workload, Native builds 42.00%
faster and with 48.25% less peak RSS than optimized Go, runs 18.02% slower with
58.18% less peak RSS, and produces a 96.80% smaller stripped executable. It
remains within every registered Go-parity and canonical compiler guardrail and
closes exact Darwin and Linux arm64 replacement chains. See the
[Gate 6J Float Array plan](docs/gate-6-float-arrays.md),
[Decision 0017](docs/decisions/0017-self-hosted-float-arrays.md), and
[recorded result](results/2026-08-29-gate6j-float-arrays-darwin-linux-arm64/README.md).

Gate 6K is complete at measured implementation revision
`84e2e4a6e2cff9d7fdab46ce4eec33b609a597c4`. The ordinary self-hosted compiler
now accepts an explicit standard `trbconfig.jsonc`, strictly loads the bounded
Go-mode configuration, deterministically checks the complete production source
set, and builds the project's unique top-level `main()`. On the fixed
1,025-file project, Native build is 85.81% faster with 93.08% less peak RSS
than optimized Go, runtime is 18.73% faster with 67.55% less peak RSS, and the
stripped executable is 96.98% smaller. Configured-input overhead remains within
the registered file-root bounds, every canonical compiler guardrail passes,
and exact Darwin/Linux arm64 replacement chains close. See the
[Gate 6K configured-project plan](docs/gate-6-configured-project.md),
[Decision 0018](docs/decisions/0018-explicit-configured-project.md), and
[recorded result](results/2026-08-30-gate6k-configured-project-darwin-linux-arm64/README.md).

Gate 6L is complete under
[issue #90](https://github.com/type-rb/type-rb-native/issues/90). The immutable
experimental prerelease
[`bootstrap-seed-2026-08-30`](https://github.com/type-rb/type-rb-native/releases/tag/bootstrap-seed-2026-08-30)
contains attested Darwin and Linux arm64 compilers plus a strict manifest and
checksum index. Fresh post-publication jobs verified the exact release,
digests, signer workflow, source revision/ref, and hosted-runner identity, then
closed byte-identical B1/B2/B3/B4 chains without downloading the root QBE or
executing Go or the reference compiler. The two compiler assets total 500,520
bytes; final adjacent-generation elapsed and RSS spreads are at most 4.63% and
0.68%. This date-labelled seed is not Native SemVer or a stable support
promise. See the
[Gate 6L bootstrap seed plan](docs/gate-6-bootstrap-seed-distribution.md),
[Decision 0019](docs/decisions/0019-experimental-bootstrap-seed-distribution.md),
and
[recorded result](results/2026-08-30-gate6l-bootstrap-seed-darwin-linux-arm64/README.md).

Current development pins TypeRB `0.4.4-dev` at an exact revision. All 39 uses
of the removed aggregate filesystem package now use bounded scoped files and
shell-free test support for recursive directory creation. The immutable
previous-Native seed reaches byte-identical current B2/B3/B4 fixed points on
Darwin and Linux arm64 through two setup-only Go-free transitions. The
canonical compiler and target-neutral QBE are also exact against the previous
Native baseline. The worst candidate build/RSS median ratio is 1.0004, and the
current platform compilers total 567,824 bytes. The seed and independent Native
version remain unchanged; this does not imply a stable TypeRB compatibility
range. See the
[TypeRB compatibility mapping](docs/type-rb-compatibility.md),
[registered revalidation](https://github.com/type-rb/type-rb-native/issues/144),
and
[recorded result](results/2026-08-31-typerb-0-4-4-compatibility-darwin-linux-arm64/README.md).

Profitable static Strings of at least 256 bytes now use a deterministic,
dependency-free bounded-backreference representation. They expand once into
zero-filled static storage before entry, require no heap allocation, and emit
no decoder for programs without a profitable literal. The exact Darwin/Linux
arm64 compiler pair decreases from 567,824 to 535,304 bytes, build-time and RSS
medians remain within their registered 5% bound, and both targets emit the same
869,699-byte fixed-point QBE. See the
[registered compactness scope](https://github.com/type-rb/type-rb-native/issues/146)
and
[formal static String compactness result](results/2026-08-31-static-string-compactness-darwin-linux-arm64/README.md).

The ordinary self-hosted runtime now reclaims dynamic Strings, Arrays, and
managed records through an exact-root non-moving collector. The registered
300,000,000-iteration Linux soak allocates and reclaims 42,300,000,000 managed
bytes, ends with zero live managed bytes, and records a flat 2,347,008-byte RSS
series. ASan/LSan and Valgrind report no lost allocation or memory error, and
the exact Darwin/Linux compiler chains remain below the registered size bounds.
This bounded Stage 1 result is not proof for persistent Web or Job resource
lifecycles. See the
[runtime memory design](docs/runtime-memory-stability.md) and
[recorded result](results/2026-08-30-runtime-memory-stability-darwin-linux-arm64/README.md).

A second layer now exercises one single-threaded persistent worker lifecycle
without adding Native-only TypeRB syntax or a public Web/Job API. One identical
TypeRB source drives Native and optimized Go through success, retry, terminal
failure, cancellation, and a bounded 64-entry retained-payload cache. CI runs a
40,000-batch smoke on Darwin and Linux arm64. The formal Linux run processes
460,800,000 original jobs, allocates and reclaims 33,926,400,576 managed bytes,
ends with zero live bytes, keeps a 1,048,574-byte peak, and records flat
2,338,816-byte RSS quartiles with stable descriptors and threads. ASan/LSan and
Memcheck report no leak or memory error. Native takes 46.37 seconds versus
14.67 seconds for the exact optimized-Go control in this allocation-heavy
workload. This is a bounded single-threaded non-I/O worker result, not a general
persistent-service claim. See [issue #150](https://github.com/type-rb/type-rb-native/issues/150),
the [persistent worker harness](tools/runtime-worker-soak/README.md), and the
[recorded result](results/2026-09-01-persistent-worker-memory-darwin-linux-arm64/README.md).

Gate 6M is complete under
[issue #113](https://github.com/type-rb/type-rb-native/issues/113). The
ordinary self-hosted application path now implements the existing portable
`Process.argv()`, strict String-to-Integer conversion, canonical Integer
formatting, checked Float narrowing, and `Math.sqrt()` contracts. Exact
Darwin/Linux B2/B3/B4 fixed points close, the two compiler assets total 573,720
bytes, and the canonical Darwin compiler remains within its strict 15% time
and RSS guardrails. On the identical portable TypeRB workload, Native builds
59.23% faster with 46.81% less peak RSS and runs 28.89% faster with 71.54% less
peak RSS than optimized Go; stripped binaries are at least 98.19% smaller. The
Linux evidence observes the explicit LLD and dynamic libm boundaries. See the
[Gate 6M plan](docs/gate-6-portable-benchmark-entry.md),
[Decision 0021](docs/decisions/0021-portable-benchmark-entry-primitives.md),
[Decision 0022](docs/decisions/0022-linux-arm64-lld-linker.md), and
[recorded result](results/2026-08-31-gate6m-portable-benchmark-entry-darwin-linux-arm64/README.md).

The current formal language-benchmark runtime result retains all 462 registered
samples for `fannkuch-redux`, `n-body`, and `spectral-norm`. The exact same
TypeRB sources pass through pinned Go and self-hosted Native paths. Native is
1.48x to 2.19x slower than TypeRB Go and 2.59x to 4.09x slower than the pinned
Pure Go implementations on these numeric kernels. It simultaneously uses
82.47% to 86.90% less peak RSS than TypeRB Go and produces raw applications at
least 99.19% smaller. Pure Go parity or better is the minimum Native runtime
objective. Pinned C, C++, Go, Rust, and Java programs remain separate
one-core/four-core implementation context; no composite language score is
claimed. See the
[recorded runtime result](results/2026-09-01-benchmarksgame-runtime-safe-array-headers-linux-arm64/README.md),
[benchmark plan](docs/benchmarksgame.md),
[Decision 0023](docs/decisions/0023-reproducible-benchmark-layers.md), and
[Decision 0024](docs/decisions/0024-benchexec-runtime-controller.md).

The current formal backend-pair build result retains all 66 registered
compiler samples. Native compiles the same three TypeRB sources 2.34x to 2.62x
faster than the optimized Go path, uses 5.89x to 6.32x less compiler CPU and
about 51% less peak RSS, and produces raw applications at least 99.19% smaller.
The Native compiler-plus-QBE controlled payload is 969,600 bytes, 99.65% below
reference `trb` plus the complete pinned Go root. Successful process traces
retain QBE, assembler, C driver, LLD, and shared-library boundaries. See the
[recorded build result](results/2026-09-01-benchmarksgame-build-safe-array-headers-linux-arm64/README.md),
[formal build controller](tools/benchmarksgame-build-formal/README.md), and
[Decision 0027](docs/decisions/0027-formal-build-distribution-controller.md).

The first formal Native-to-Native optimization A/B result retains all 78
registered processes for the same three programs. A bounded numeric-only
reserve outside lexical loops reduces `spectral-norm` wall and CPU medians by
20.61% and 20.62%, while `fannkuch-redux` and `n-body` remain slightly faster
than the frozen Native baseline. The candidate preserves exact self-hosted
fixed-point closure, stays within a 0.1% compiler-size cap, and keeps every QBE
and application artifact within its registered compactness limit. See the
[recorded optimization result](results/2026-08-31-native-numeric-inline-linux-arm64/README.md)
and [formal A/B controller](tools/native-runtime-ab/README.md).

The second formal Native-to-Native optimization A/B result collapses the
shared Array-address bounds predicate to one unsigned comparison after the
existing negative-index adjustment. Exact source behavior and fixed-point
closure pass; wall and CPU medians improve by 4.67% to 7.97% across all three
registered numeric programs; and compiler, QBE, and application artifacts all
shrink. See the
[recorded Array-address result](results/2026-08-31-native-array-address-linux-arm64/README.md).

A subsequent bounded scalar-leaf inlining candidate passed correctness,
fixed-point, and target-neutral-QBE regressions but was rejected before formal
runtime timing. Its Linux arm64 self-hosted compiler grew by 2.20%, exceeding
the preregistered 0.1% maximum. The implementation was reverted and the bound
was not weakened. See the
[recorded rejected result](results/2026-08-31-native-scalar-leaf-inline-linux-arm64/README.md).

A redesigned one-site scalar-leaf inliner then passed every frozen condition.
On the registered `spectral-norm` signal, wall and CPU medians improved by
11.81% and 11.82%; both control programs stayed within their non-regression
bounds, the fixed compiler remained 252,816 bytes, and build plus application
compactness limits passed. The accepted implementation is the baseline for
the next complete cross-language snapshot. See the
[authoritative formal run](https://github.com/type-rb/type-rb-native/actions/runs/33481712297).

A following safe-point-aware root-publication candidate removed redundant
managed-root updates from numeric functions that cannot start collection.
It improved `n-body` wall and CPU medians by about 12.7%, reduced its QBE and
executable, and passed correctness, fixed-point, build, and compactness limits,
but missed the preregistered 15% performance signal. The threshold was not
relaxed and the implementation was reverted. See the
[recorded rejected result](results/2026-09-01-rejected-no-gc-root-publication-linux-arm64/README.md).

The subsequent combined candidate retains safe-point-aware root elision and
adds conservative reuse of the two most recent Array-header pairs in owned
loops. It passes every frozen condition: `n-body` wall and CPU medians improve
by 28.36% and 28.50%, `fannkuch-redux` improves by 7.46%, and `spectral-norm`
remains neutral. Exact fixed-point, build-cost, compiler-size, application-size,
correctness, and catastrophic limits all pass. See the
[recorded safe Array-header result](results/2026-09-01-native-safe-array-headers-linux-arm64/README.md).

A bounded follow-up moved one stable Array length into a loop preheader. It
passed correctness, fixed-point, build-cost, compiler-size, application-size,
memory, and control limits, but improved the required `spectral-norm` wall and
CPU medians by only about 0.6% against a frozen 3% requirement. The threshold
was not relaxed and the implementation was reverted. See the
[recorded rejected result](results/2026-09-01-rejected-loop-invariant-array-length-linux-arm64/README.md).

The next accepted candidate moves managed-root publication from a loop header
to its exit only when emitted-code analysis proves that no path through the
condition or body can start collection. It passes every frozen condition:
`fannkuch-redux` wall and CPU medians improve by 12.46% and 12.47%, while
`n-body` and `spectral-norm` remain neutral. Exact fixed-point, build-cost,
compiler-size, application-size, correctness, and catastrophic limits all
pass. See the
[recorded safe-point-free loop-root result](results/2026-09-02-native-safe-point-free-loop-roots-linux-arm64/README.md).

The following accepted candidate adds a bounded fast entry to checked Integer
multiplication. Nonnegative operands that fit 26 bits multiply directly;
every other pair keeps the exact existing overflow path. On the registered
`spectral-norm` signal, wall and CPU medians improve by 27.82% and 27.83%,
while `fannkuch-redux` and `n-body` remain neutral. The fixed compiler and all
three executable sizes remain unchanged, generated QBE shrinks, and every
correctness, fixed-point, build, memory, compactness, and catastrophic limit
passes. See the
[recorded bounded Integer-multiply result](results/2026-09-02-native-bounded-integer-multiply-linux-arm64/README.md).

The next accepted candidate specializes one already budgeted checked Integer
addition when either emitted operand is an unsigned decimal literal no greater
than 1024. It canonicalizes that literal to the right and removes only the
lower portable-range check that cannot fail; the upper check and all general
paths remain. Median wall time improves by 2.85% for `fannkuch-redux`, 1.26%
for `n-body`, and 9.25% for `spectral-norm`. The fixed compiler and all three
applications become smaller, while every correctness, fixed-point, build,
memory, compactness, and catastrophic limit passes. See the
[recorded bounded literal Integer-add result](results/2026-09-02-native-bounded-literal-integer-add-linux-arm64/README.md).

The next accepted candidate removes negative-index normalization only for
Array accesses driven by a narrowly proven zero-based unit-step induction
local. The unsigned upper-bounds comparison remains, while reassignment,
non-unit updates, nested control flow, dynamic indices, and ordinary negative
indexing retain the general path. On the registered `spectral-norm` signal,
wall and CPU medians improve by 5.00%; `fannkuch-redux` and `n-body` remain
neutral. The fixed compiler stays below its absolute and relative limits, all
three applications are byte-neutral or smaller, and every correctness,
fixed-point, build, memory, compactness, and catastrophic limit passes. See
the
[recorded nonnegative loop-index result](results/2026-09-02-native-nonnegative-loop-index-linux-arm64/README.md).

The following registered candidate keeps that proof only through the matching
lexical loop rather than scanning to the containing function. Safe nested
loops and unrelated later resets may therefore retain the outer nonnegative
fact, while every direct reassignment, non-unit update, shadowing declaration,
derived index, and unproved access remains on the general path. The Linux
arm64 contract requires at least a 5% `n-body` wall-time and CPU-time
improvement, byte-neutral or smaller application QBE, and every existing
correctness, compactness, fixed-point, build, memory, and catastrophic bound.
The contract is registered in
[issue #190](https://github.com/type-rb/type-rb-native/issues/190); formal
evidence is required before this candidate can become an accepted baseline.

Gate 6N passes every frozen condition for the internal
`linux-amd64-v0` profile. The exact merged compiler closes a 240,888-byte
Go-free B2/B3/B4 fixed point, emits byte-identical target-neutral compiler and
portable-application QBE across Linux amd64 and arm64, and retains explicit
QBE, system CC, assembler, LLD, libm, and dynamic-library boundaries. On the
registered identical-source application, Native builds 77.60% faster with
21.00% less peak RSS, runs 53.22% faster with 73.84% less peak RSS, and is
99.26% smaller when stripped than optimized Go. Linux amd64 remains
experimental and unsupported. See the
[recorded result](results/2026-08-31-gate6n-linux-amd64/README.md),
[Gate 6N plan](docs/gate-6-linux-amd64.md), and
[Decision 0025](docs/decisions/0025-linux-amd64-target-profile.md).

Upward configured project discovery, persistent service runtime integration,
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

- [Capability map](https://type-rb.github.io/type-rb-native/) ([source and maintenance](docs/capabilities/README.md))
- [Benchmark explorer](docs/capabilities/benchmarks/README.md)
- [Architecture](docs/architecture.md)
- [Development and validation plan](docs/experiment-plan.md)
- [Native versioning and compatibility](docs/versioning.md)
- [TypeRB compatibility mapping](docs/type-rb-compatibility.md)
- [TypeRB 0.4 compatibility Darwin/Linux arm64 result](results/2026-08-30-typerb-0-4-compatibility-darwin-linux-arm64/README.md)
- [Gate 1 QBE vertical slice](docs/gate-1-qbe.md)
- [Gate 1 QBE Darwin arm64 result](results/2026-08-28-gate1-qbe-darwin-arm64/README.md)
- [Gate 2 heap-free aggregate value model](docs/gate-2-aggregates.md)
- [Gate 2 QBE Darwin arm64 result](results/2026-08-28-gate2-qbe-darwin-arm64/README.md)
- [Gate 3 managed runtime](docs/gate-3-managed-runtime.md)
- [Ordinary runtime memory stability](docs/runtime-memory-stability.md)
- [Ordinary runtime memory stability Darwin/Linux arm64 result](results/2026-08-30-runtime-memory-stability-darwin-linux-arm64/README.md)
- [Persistent worker memory lifecycle harness](tools/runtime-worker-soak/README.md)
- [Persistent worker memory lifecycle Darwin/Linux arm64 result](results/2026-09-01-persistent-worker-memory-darwin-linux-arm64/README.md)
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
- [Gate 6J self-hosted Float Array Darwin/Linux arm64 result](results/2026-08-29-gate6j-float-arrays-darwin-linux-arm64/README.md)
- [Gate 6K explicit configured-project executables](docs/gate-6-configured-project.md)
- [Gate 6K configured-project Darwin/Linux arm64 result](results/2026-08-30-gate6k-configured-project-darwin-linux-arm64/README.md)
- [Gate 6L experimental bootstrap seed distribution](docs/gate-6-bootstrap-seed-distribution.md)
- [Gate 6L durable bootstrap seed Darwin/Linux arm64 result](results/2026-08-30-gate6l-bootstrap-seed-darwin-linux-arm64/README.md)
- [Gate 6M portable benchmark-entry primitives](docs/gate-6-portable-benchmark-entry.md)
- [Gate 6M portable benchmark-entry Darwin/Linux arm64 result](results/2026-08-31-gate6m-portable-benchmark-entry-darwin-linux-arm64/README.md)
- [Gate 6N Linux amd64 target-chain result](results/2026-08-31-gate6n-linux-amd64/README.md)
- [Gate 6N Linux amd64 target chain](docs/gate-6-linux-amd64.md)
- [Reproducible language benchmark plan](docs/benchmarksgame.md)
- [Current formal Benchmarks Game runtime result on Linux arm64](results/2026-09-01-benchmarksgame-runtime-safe-array-headers-linux-arm64/README.md)
- [Current formal Benchmarks Game build result on Linux arm64](results/2026-09-01-benchmarksgame-build-safe-array-headers-linux-arm64/README.md)
- [Formal Native numeric-inline A/B result on Linux arm64](results/2026-08-31-native-numeric-inline-linux-arm64/README.md)
- [Formal Native Array-address A/B result on Linux arm64](results/2026-08-31-native-array-address-linux-arm64/README.md)
- [Rejected Native scalar-leaf inlining result on Linux arm64](results/2026-08-31-native-scalar-leaf-inline-linux-arm64/README.md)
- [Rejected no-GC-safe-point root-publication result on Linux arm64](results/2026-09-01-rejected-no-gc-root-publication-linux-arm64/README.md)
- [Formal safe Array-header reuse result on Linux arm64](results/2026-09-01-native-safe-array-headers-linux-arm64/README.md)
- [Rejected loop-invariant Array-length result on Linux arm64](results/2026-09-01-rejected-loop-invariant-array-length-linux-arm64/README.md)
- [Formal safe-point-free loop-root result on Linux arm64](results/2026-09-02-native-safe-point-free-loop-roots-linux-arm64/README.md)
- [Formal bounded Integer-multiply result on Linux arm64](results/2026-09-02-native-bounded-integer-multiply-linux-arm64/README.md)
- [Formal bounded literal Integer-add result on Linux arm64](results/2026-09-02-native-bounded-literal-integer-add-linux-arm64/README.md)
- [Formal nonnegative loop-index result on Linux arm64](results/2026-09-02-native-nonnegative-loop-index-linux-arm64/README.md)
- [Formal static String compactness A/B result on Darwin/Linux arm64](results/2026-08-31-static-string-compactness-darwin-linux-arm64/README.md)
- [Formal TypeRB backend-pair build controller](tools/benchmarksgame-build-formal/README.md)
- [Formal Native runtime optimization A/B controller](tools/native-runtime-ab/README.md)
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
- [Decision 0018: Explicit configured-project executables](docs/decisions/0018-explicit-configured-project.md)
- [Decision 0019: Experimental bootstrap seed distribution](docs/decisions/0019-experimental-bootstrap-seed-distribution.md)
- [Decision 0020: Independent Native versioning and exact TypeRB compatibility](docs/decisions/0020-independent-native-versioning.md)
- [Decision 0021: Portable benchmark-entry primitives](docs/decisions/0021-portable-benchmark-entry-primitives.md)
- [Decision 0022: Linux arm64 LLD linker](docs/decisions/0022-linux-arm64-lld-linker.md)
- [Decision 0023: Reproducible benchmark layers](docs/decisions/0023-reproducible-benchmark-layers.md)
- [Decision 0024: BenchExec fresh-process runtime controller](docs/decisions/0024-benchexec-runtime-controller.md)
- [Decision 0025: Linux amd64 target profile](docs/decisions/0025-linux-amd64-target-profile.md)
- [Decision 0026: Separate recovered target chains from seed assets](docs/decisions/0026-recovered-target-chain-evidence.md)
- [Decision 0027: Formal build and distribution controller](docs/decisions/0027-formal-build-distribution-controller.md)
- [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md)

## License

TypeRB Native is available under the [MIT License](LICENSE).
