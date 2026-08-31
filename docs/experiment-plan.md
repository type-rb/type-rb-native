# Development and Validation Plan

## Engineering objective

Build a TypeRB-specific native AOT pipeline that ultimately matches or improves
the optimized Go backend across these primary outcomes:

1. End-to-end application build time.
2. Generated-program execution time.
3. Deployed executable size.

The compiler and runtime are implemented in TypeRB, reproduce themselves, and
must retain competitive build time and generated-code behavior once the
complete self-hosted toolchain is measured. Early gates establish this outcome
incrementally; they are not a sequence of throwaway demonstrations.

Secondary outcomes include compiler and runtime peak memory, startup latency,
toolchain distribution size, portability, diagnostics, correctness risk, and
maintenance cost.

The comparison baseline is an optimized release executable produced by the
reference compiler's Go backend. The experiment does not compare against an
intentionally unstripped, cold, or otherwise disadvantaged Go configuration.

## Principles

- Correctness precedes performance.
- All candidates use the same TypeRB inputs, supported semantics, Native MIR
  corpus, benchmark policy, and, for same-target comparisons, the same target
  ABI profile.
- Unsupported behavior fails explicitly.
- Measurements include serialization, lowering, optimization, code generation,
  assembly, linking, runtime, and required external components.
- Quality and performance targets are recorded before reviewing a result.
- Microbenchmarks diagnose a phase; representative programs determine
  viability.

Before a gate begins, its issue must record metric-specific non-inferiority
bounds, a minimum meaningful primary-metric improvement where the gate is
expected to provide one, and catastrophic-regression limits. A miss identifies
required engineering work or an architectural decision; it does not by itself
end the native implementation. Targets cannot be weakened after results are
reviewed merely to label a gate complete.

## Candidate sequence

Backend candidates are not implemented to production completeness in parallel.
They advance through small shared gates, and only implementations with a clear
role continue to accumulate maintenance cost.

1. Use hand-authored bootstrap and MIR fixtures to validate the boundary.
2. Use QBE for the cheapest runtime and ABI feasibility check.
3. Consider Cranelift only if the QBE result leaves a measured development
   code-generation problem worth testing.
4. Add LLVM only after the corpus is representative enough to measure an
   optimization ceiling.
5. Attempt a direct emitter only if profiling shows codegen or toolchain
   overhead dominates and the MIR, layouts, and ABI have stabilized.

This order is a starting hypothesis, not a compatibility promise.

TinyGo may be measured once as a time-boxed calibration of the optimized Go
baseline. It is not a path to the required Go-independent compiler and is not
a gate deliverable. A C emitter is likewise deferred unless later profiling
shows that it answers a specific question more cheaply than the selected
backend. Neither is built merely to populate a comparison table.

## Gates

### Gate 0: Boundary

Scope:

- a documented versioned, data-only bootstrap snapshot subset;
- a TypeRB implementation of strict snapshot decoding and validation;
- a distinct Native MIR model, lowering, and verifier implemented in TypeRB;
- deterministic diagnostic codes, paths, and messages for malformed,
  unsupported, and structurally invalid input;
- source identity and spans retained on every lowered function, block, and
  instruction; and
- valid and invalid fixtures plus portable tests.

Exit condition: the pinned reference TypeRB compiler can check and test the
Gate 0 implementation, and the implementation can validate and lower all Gate
0 fixtures without importing reference compiler internal objects. Malformed,
unknown, unsupported, and invariant-breaking fixtures fail deterministically;
valid input produces verified Native MIR with unchanged source origins.

### Gate 1: Heap-free execution

Scope:

- functions and direct calls;
- branches and loops;
- Boolean, Integer, and Float values;
- exact checked Integer behavior;
- static strings and observable output; and
- one disposable `darwin-arm64-v0` ABI profile through QBE 1.3.

Records and tagged values begin at Gate 2. Gate 1 does not change the TypeRB
`def main()` contract; its no-argument, `Void` MIR entry is an internal
executable convention rather than new language syntax.

Every backend candidate at this gate runs the same differential corpus against
the reference compiler's Go backend. A mismatch is triaged against the TypeRB
specification and accepted conformance behavior rather than automatically
treating either implementation as correct.

The pre-registered Gate 1 continuation criteria require complete differential
correctness and at least one representative-corpus improvement: end-to-end
build time by 20%, steady-state execution time by 10%, or stripped executable
size by 30%. The other primary outcomes should remain within 25% of the
stronger applicable optimized Go baseline. A regression greater than 2x stops
the gate for review. TinyGo is measured only if the unchanged corpus works and
the calibration costs no more than half a working day; it is not a deliverable.

### Gate 2: Heap-free aggregate value model

Scope:

- nominal records with immutable, statically laid-out fields;
- payloadless and payload-bearing enum variants represented as tagged values;
- aggregate construction, field and payload projection, direct calls, returns,
  block parameters, and exhaustive variant dispatch;
- monomorphized static layouts needed for records and `Result<T, E>` whose
  fields and payloads are themselves heap-free Gate 2 values;
- deterministic snapshots, MIR, QBE output, executables, diagnostics, and
  layout computation; and
- the existing disposable `darwin-arm64-v0` profile and QBE 1.3 path.

Dynamic strings, arrays, hashes, closures, captured environments, escaping
values, heap allocation, and a memory manager remain outside Gate 2. A static
string literal may still be used only for the existing observable-output
operation; it is not yet a first-class aggregate field or payload.

Exit condition: the pinned reference compiler and native path produce identical
observable results for the registered source corpus covering records, nested
records, payload enums, exhaustive `case`, explicit `Result` handling, and
`try` propagation. Invalid snapshot and MIR inputs fail deterministically,
layout boundary tests pass, and repeated builds reproduce the same snapshot,
MIR, QBE IL, and executable. On the registered aggregate workloads, stripped
native executable size remains at least 30% below the stronger applicable Go
baseline, while warm end-to-end build time and runtime each remain within 25%
and no primary metric regresses by more than 2x. A target miss keeps Gate 2 open
for diagnosis and improvement.

### Gate 3: Runtime viability

Gate 3 is registered in
[issue #13](https://github.com/type-rb/type-rb-native/issues/13) and specified
by [Decision 0005](decisions/0005-managed-runtime-and-tracing-gc.md). Its scope
is:

- managed UTF-8 Strings and mutable homogeneous Arrays;
- first-class function values, captured environments, and indirect calls;
- reference-containing records and tagged values;
- an exact-root, non-moving mark-sweep collector that reclaims cycles; and
- the existing `darwin-arm64-v0` profile and QBE 1.3 path.

Hash, Bytes, StringBuilder, classes, interfaces, concurrency, module
initialization, and broad runtime adapters remain deferred until this common
managed-reference boundary is measured. They are still prerequisites where
the Gate 4 compiler source uses them.

Exit condition: the pinned reference compiler and native path produce identical
observable output and failure behavior for the registered String, Array, and
closure source corpus. Invalid snapshot and MIR inputs fail deterministically,
repeated builds are byte-reproducible, and the registered stress case proves
that unreachable closure/Array cycles are reclaimed within the live-set bound.
Stripped native executables remain at least 30% smaller than the stronger
optimized Go baseline; warm end-to-end build time, every registered steady-state
runtime, and peak runtime RSS remain within 25%. No primary metric may regress
by more than 2x. A miss keeps Gate 3 open for diagnosis and improvement.

Only QBE advances through Gate 3. A second candidate requires a distinct,
measured development or release role.

### Gate 4: Self-hosting compiler completeness

Gate 4 is registered in
[issue #20](https://github.com/type-rb/type-rb-native/issues/20) and specified
by [Decision 0006](decisions/0006-behavioral-self-hosting-boundary.md). Scope
expands to a TypeRB-authored lexer, parser, resolver, checker, QBE emitter, and
compiler driver sufficient to compile this repository's documented compiler
source closure. The Go reference compiler remains a semantic oracle and
recovery bootstrap but is not linked into the native compiler.

The compiler receives source at runtime and must compile mutations and the
registered corpus through the same passes. An embedded source-specific QBE
artifact, quine, unchecked fallback, or compiler for a non-TypeRB demonstration
language cannot satisfy the gate.

Exit condition: a Go-bootstrapped B0 compiler produces B1 from the TypeRB
compiler sources, B1 produces B2 without executing or linking Go, and all three
stages match observable compiler behavior on the valid and invalid conformance
corpus. Repeated QBE emission is byte-identical and source-mutation checks prove
that the frontend and code generator are active. B1/B2 executable identity
remains a Gate 5 requirement; representative full-product performance remains
a Gate 6 requirement.

Gate 4 completed at TypeRB Native revision
`b48e6b49fadd99f09805cbdefdf85f5dab67494d`. B1, B2, and B3 QBE converge
byte-for-byte; every conformance and mutation check passes; and the direct
B1-to-B2 harness contains no Go or reference compiler. Build time, RSS, and
stripped size are within the registered B1/B2 convergence bounds, while the
native compiler-plus-QBE distribution is 99.827% smaller than recovery. See
the [Gate 4 result](../results/2026-08-28-gate4-self-host-darwin-arm64/README.md).

### Gate 5: Matched self-hosted compiler baseline

Gate 5 is registered in
[issue #29](https://github.com/type-rb/type-rb-native/issues/29) and specified
by
[Decision 0007](decisions/0007-matched-self-hosted-compiler-baseline.md). It
first replaces Gate 4's unmatched diagnostic comparison with functional Native
and optimized Go compiler executables that run the same checked-in
TypeRB-authored compiler logic through the same source-content and mode
interface.

The optimized Go comparison uses a deterministic generated driver that invokes
`compiler_main` through the existing portable `argv()` contract. The Native
compiler keeps its repository-internal Gate 4 entry adapter for this bounded
comparison. The harness must prove that both executables retain and execute the
lexer, parser, resolver, checker, and QBE emitter; an empty or dead-stripped
entry cannot pass.

Gate 5 also replaces source-sized parallel compiler storage with demand-sized
storage where practical, keeps B0 -> B1 -> B2 -> B3 behavioral self-hosting,
requires byte-identical B1/B2/B3 QBE, and requires B1/B2 executable equivalence
under a documented normalization policy that preserves code and data. The
ordinary B1-to-B2 process graph remains free of Go and the reference compiler.

Exit condition: the matched Go and Native compilers pass the complete valid,
invalid, mutation, and storage-boundary corpus with identical observable
behavior. Native direct compiler time, end-to-end build time, and peak RSS each
remain within 25% of the matched optimized Go baseline; stripped compiler and
complete toolchain distribution sizes improve by at least 30%; and adjacent
Native-generation build time, RSS, and stripped size remain within 25%. A
greater than 2x regression is catastrophic. Exact registered measurement rules
remain in issue #29.

Gate 5 completed at TypeRB Native revision
`a83699d6dd87de0c77a8a8a395ea6e266802bf0a`. The matched behavior and
anti-shortcut checks pass; B1/B2/B3 QBE and normalized B1/B2 executables
converge; Native direct compilation and end-to-end building are substantially
faster than the matched Go artifact; all RSS bounds pass; and stripped compiler
and compiler-plus-QBE sizes improve by 94.46% and 82.18%. See the
[Gate 5 result](../results/2026-08-29-gate5-matched-compiler-darwin-arm64/README.md).

### Gate 6: Self-hosted product feasibility

Gate 6 begins with the separately measurable Gate 6A file-entry slice
registered in
[issue #35](https://github.com/type-rb/type-rb-native/issues/35) and specified
by [Decision 0008](decisions/0008-file-oriented-compiler-entry.md). B1 and later
compiler generations first replace the ordinary source-content argv adapter
with `check SOURCE` and `emit-qbe SOURCE` file commands, exact stderr and exit
behavior, and TypeRB-owned direct file I/O. B0 retains an explicit hidden
source-content adapter for recovery. Gate 6A retains the complete compiler and
conformance corpus, the B1/B2/B3 fixed point, and normalized executable
identity, then measures the file boundary against the same-generation hidden
path before broader product work proceeds.

Gate 6A completed at TypeRB Native revision
`cf6fabccf8bd799d5457372f93f024687d5e6d13`. File input matches the complete
registered behavior and fixed point, direct time and RSS improve over the
same-generation hidden path, adjacent B1/B2 measurements converge, stripped
size grows by 0.16%, and the direct process imports no spawn operation. See the
[Gate 6A result](../results/2026-08-29-gate6a-file-entry-darwin-arm64/README.md).

Gate 6B is the separately measurable Native-owned single-file build slice
registered in
[issue #39](https://github.com/type-rb/type-rb-native/issues/39) and specified
by [Decision 0009](decisions/0009-native-single-file-build.md). B1 and B2 accept
the fixed experimental `build SOURCE --output OUTPUT --qbe QBE --cc CC`
command, emit their own QBE IL, directly invoke the explicit QBE and C
toolchain paths without a shell, atomically publish the executable, and clean
all intermediates. Every existing valid, mutation, and invalid input, the
compiler fixed point, deterministic application output, failure contracts, and
the ordinary Go-free process graph remain required.

Gate 6B compares the Native-owned command with the existing external
file-emission/QBE/CC recipe after two warmups and seven alternating
observations. Time and orchestration-root peak RSS must remain within 25%, B1
and B2 must remain within 25%, application behavior and size must not regress,
and the stripped Native compiler must remain within 15% of the 149,784-byte
Gate 6A baseline. See the
[Gate 6B single-file build plan](gate-6-single-file-build.md).

Gate 6B completed at measured TypeRB Native revision
`1038cfe497a96d9d282db55a54d9eea6509f7868`. Native-owned B1/B2 builds match
the external recipe's application bytes and behavior, retain the compiler
fixed point, clean every intermediate, and contain only the registered
Native-to-QBE-to-CC process graph. Median time is 1.41% and 3.13% above the
same-generation external recipe, median RSS is 0.63% and 0.27% above it,
adjacent Native generations converge within 0.42%, and stripped compiler
growth is 11.38%. All registered bounds pass. See the
[Gate 6B result](../results/2026-08-29-gate6b-single-file-build-darwin-arm64/README.md).

Gate 6C is the Native-to-Native bootstrap-closure slice registered in
[issue #43](https://github.com/type-rb/type-rb-native/issues/43) and specified
by [Decision 0010](decisions/0010-native-bootstrap-closure.md). One recovered or
previously distributed B1 seed is setup input. B1 builds B2, generated B2 builds
B3, and generated B3 builds B4 through the ordinary Native-owned command. The
three same-basename outputs must be byte-identical, retain the compiler QBE
fixed point and complete file-command corpus, and leave no intermediate.

The focused measurement records two warmups and seven alternating observations
for each adjacent Native generation plus peak RSS. Adjacent medians must remain
within 10%, each step must remain within 25% of the Gate 6B B1 Native baselines,
and compiler bytes and stripped size must not change. See the
[Gate 6C Native bootstrap plan](gate-6-native-bootstrap.md).

Gate 6C completed at measured TypeRB Native revision
`622d5931e677f7b9283c073021ac0ef39fafa1a5`. B2/B3/B4 executable bytes are
identical, adjacent median time and RSS differ by at most 1.03% and 0.67%,
every median remains within 1.10% of its Gate 6B baseline, and stripped code
remains exactly 166,824 bytes. All registered bounds pass. See the
[Gate 6C result](../results/2026-08-29-gate6c-native-bootstrap-darwin-arm64/README.md).

Gate 6D is the second-environment target slice registered in
[issue #47](https://github.com/type-rb/type-rb-native/issues/47) and specified
by [Decision 0011](decisions/0011-linux-arm64-target-profile.md). The same
TypeRB-authored compiler source, target-neutral QBE IL, runtime semantics, and
conformance corpus close a B1-to-B2-to-B3-to-B4 chain under the explicit
internal `linux-arm64-v0` profile. Only the QBE target, system ABI, and linker
artifact policy differ from Darwin.

The Linux harness records its pinned environment and recovery provenance,
requires exact B2/B3/B4 executable bytes, exercises the complete valid,
mutation, invalid, and failure corpus, and inventories ELF dependencies and the
ordinary process graph. Two warmups and seven alternating observations compare
the Native-owned build with the external QBE/CC recipe. Median time and peak RSS
must remain within 25% of the stronger external path, adjacent Native
generations within 10%, and stripped compiler size within 208,530 bytes. See
the [Gate 6D Linux arm64 plan](gate-6-linux-arm64.md).

Gate 6D completed at measured TypeRB Native revision
`68497f68ed1c3770c2a457790a6519962a2cb921`. B1/B2/B3/B4 Linux compiler bytes
are exact; the complete corpus, failures, ELF and process inventory pass;
Native/external median time differs by at most 2.55%; adjacent Native medians
differ by at most 0.88%; median RSS differs by at most 0.35%; and compiler size
is 15.64% below its registered ceiling. See the
[Gate 6D result](../results/2026-08-29-gate6d-native-bootstrap-linux-arm64/README.md).

Gate 6E is the file-root multi-module slice registered in
[issue #51](https://github.com/type-rb/type-rb-native/issues/51) and specified
by [Decision 0012](decisions/0012-file-root-module-closure.md). The existing
file commands load the entry plus its transitive named project-import closure,
retain module-local identity, and build one representative five-module
executable through the ordinary Native chain. The hidden recovery entry remains
single-source, while configured projects, packages, and public CLI design stay
deferred.

After two warmups, seven alternating application builds and 50 alternating
runs compare the self-hosted Native result with the pinned optimized Go
reference. Time and peak RSS must remain within 25% of the stronger Go result,
the Native application must remain at least 80% smaller, the compiler must stay
within 208,530 stripped bytes, and B1-to-B2 time and RSS must remain within 25%
of the Gate 6C baseline. See the
[Gate 6E file-root plan](gate-6-file-root-modules.md).

Gate 6E completed at measured TypeRB Native revision
`b2b4740f39571dc35af9199dae817d94912b7a47`. Native application build time
and RSS improve on optimized Go by 44.89% and 48.22%; runtime is 13.70% slower
and runtime RSS 65.32% lower; stripped output is 97.82% smaller and equal to
the flattened Native size. B1-to-B2 time is 23.80% above the Gate 6C baseline,
RSS is effectively flat, the compiler strips to 199,992 bytes, and Darwin and
pinned Linux arm64 fixed points pass. See the
[Gate 6E result](../results/2026-08-29-gate6e-file-root-darwin-linux-arm64/README.md).

Gate 6F is the reflexive multi-file compiler slice registered in
[issue #55](https://github.com/type-rb/type-rb-native/issues/55) and specified
by [Decision 0013](decisions/0013-multi-file-self-hosted-compiler.md). The
canonical compiler entry imports pure storage and path modules; recovery may
derive one temporary flat B1 source, but every ordinary B1-to-B4 generation
must compile the real source closure.

The split compiler retains the Gate 6E absolute build-time, RSS, and size
bounds. Alternating multi-file/flat self-build observations add a 10% source
organization bound, exact B2/B3/B4 bytes and QBE remain mandatory, and the
pinned Linux image rebuilds both the compiler and representative application.
See the [Gate 6F plan](gate-6-multifile-compiler.md).

Gate 6F is complete at measured revision
`7cb7e85c0b5bff14157dc1a686829c010d095b70`. The real multi-file compiler
builds 0.37% faster and uses 0.09% less RSS than its temporary flat comparator;
it remains within the Gate 6C absolute bounds, strips to the same 199,992
bytes, preserves the Gate 6E application hash, and closes exact Darwin and
Linux arm64 B2/B3/B4 chains. See the
[Gate 6F result](../results/2026-08-29-gate6f-multifile-compiler-darwin-linux-arm64/README.md).

Gate 6G is the self-hosted symbol-lookup scalability slice registered in
[issue #59](https://github.com/type-rb/type-rb-native/issues/59) and specified
by [Decision 0014](decisions/0014-indexed-function-lookup.md). It keeps
source-ordered declarations canonical and derives a deterministic
module-qualified function index before resolution. No public Hash, new runtime
intrinsic, source behavior, target behavior, or external-tool boundary is
introduced.

Two warmups and eleven alternating Darwin observations compare the Gate 6F
baseline and candidate on canonical direct QBE emission, complete self-builds,
and a generated 6,000-function chain. The registered minimum improvements are
5%, 3%, and 25% respectively; RSS, stripped compiler size, exact fixed points,
application identity, and pinned Linux arm64 correctness remain bounded. See
the [Gate 6G plan](gate-6-symbol-lookup.md).

Gate 6G is complete at measured revision
`8bcc2a6e1c5ecede5f07c2dda63a4d4d82631375`. Canonical direct QBE emission
improves by 30.80%, the complete build improves by 5.95%, and 6,000-function
emission improves by 53.49%; median RSS changes by +1.31%, 0.00%, and +0.12%
respectively. The candidate strips to 200,008 bytes, retains the representative
application exactly, and closes exact Darwin and Linux arm64 replacement
chains. See the
[Gate 6G result](../results/2026-08-29-gate6g-symbol-lookup-darwin-linux-arm64/README.md).

Gate 6H is the file-root module-graph scalability slice registered in
[issue #64](https://github.com/type-rb/type-rb-native/issues/64) and specified
by [Decision 0015](decisions/0015-indexed-module-graph.md). Canonical module
and import arrays retain source order while a deterministic internal
module-name index and per-module import spans remove quadratic whole-table
scans from loading, import resolution, and duplicate validation. Contiguous
declaration boundaries stop duplicate scans at the preceding module. No
configured project, package, public Hash, syntax, runtime, CLI, snapshot, MIR,
target, or external-tool contract is introduced.

Two warmups and eleven alternating Darwin observations compare the fixed Gate
6G baseline and candidate on a generated entry plus 1,024 imported modules.
The registered minimum improvements are 35% for direct checking, 25% for QBE
emission, and 10% for a complete Native build. RSS, Native-versus-Go build
time and memory, application size and behavior, canonical self-build time and
memory, stripped compiler size, exact fixed points, representative application
identity, and pinned Linux arm64 correctness remain bounded. See the
[Gate 6H plan](gate-6-module-graph.md).

Gate 6H is complete at measured revision
`e39f774237a6306d7cd46b09941367c42816c628`. On the exact 1,025-file project,
direct checking improves by 41.96%, QBE emission by 39.92%, and the complete
Native build by 16.16%; median RSS is lower in all three comparisons. The
candidate remains within the canonical Gate 6G guardrails, builds the same
project 85.79% faster and with 92.93% less peak RSS than the pinned optimized
Go path, produces a 97.00% smaller stripped application, and closes exact
Darwin and Linux arm64 chains. See the
[Gate 6H result](../results/2026-08-29-gate6h-module-graph-darwin-linux-arm64/README.md).

Gate 6I is the self-hosted Float scalar slice registered in
[issue #69](https://github.com/type-rb/type-rb-native/issues/69) and specified
by
[Decision 0016](decisions/0016-self-hosted-float-scalar-path.md). It adds the
reference language's finite decimal binary64 literals, Float storage and
function ABI, arithmetic and comparisons, signed-zero/infinity/NaN behavior,
and safe Integer-to-Float widening to the ordinary TypeRB-authored compiler.
No Native-only syntax, semantic rule, or compiler-runtime intrinsic is added.

The registered five-million-iteration Float workload is built and run through
Native and the pinned optimized Go backend. Native build time, build RSS,
runtime, and runtime RSS must remain within 25%, while stripped application
size must improve by at least 80%. A fresh Gate 6H comparison bounds canonical
compiler time and RSS to +10% and stripped size to 220,000 bytes. Exact
candidate B2/B3/B4 bytes, fixed-point QBE, representative application identity,
and a pinned Linux arm64 correctness chain remain mandatory. See the
[Gate 6I plan](gate-6-float.md).

Gate 6I is complete at measured implementation revision
`cd2335e6472b4daca8d631b17b889a094959c2f2` with the harness at revision
`073504790b930157b48c1bc6743bc0102f5fe014`. Native builds the fixed workload
41.37% faster and with 48.35% less peak RSS than optimized Go, runs 10.60%
slower with 65.60% less peak RSS, and produces a 96.80% smaller stripped
executable. All four Go-parity metrics remain within the registered 25%
ceiling. The candidate also remains within every canonical compiler guardrail,
strips to 216,552 bytes, and closes exact Darwin and Linux arm64 replacement
chains. See the
[Gate 6I result](../results/2026-08-29-gate6i-float-darwin-linux-arm64/README.md).

Gate 6J is the self-hosted Float Array slice registered in
[issue #74](https://github.com/type-rb/type-rb-native/issues/74) and specified
by [Decision 0017](decisions/0017-self-hosted-float-arrays.md). It adds the
reference language's homogeneous binary64 Array storage, safe Integer element
widening, common numeric literal inference, growth, indexing, mutation, and
bounded nested forms to the ordinary TypeRB-authored compiler and runtime. No
Native-only syntax, collection method, snapshot or MIR field, configured
project, or public CLI contract is added.

The registered five-million-element Float Array workload is built and run
through Native and the pinned optimized Go backend. Native build time, build
RSS, runtime, and runtime RSS must remain within 25%, while stripped
application size must improve by at least 80%. A fresh Gate 6I comparison
bounds canonical compiler time and RSS to +10% and stripped size to 224,000
bytes. Exact candidate B2/B3/B4 bytes, fixed-point QBE, representative and
scalar Float application identity, and a pinned Linux arm64 correctness chain
remain mandatory. See the [Gate 6J plan](gate-6-float-arrays.md).

Gate 6J is complete at measured implementation revision
`914f4f592f344111b7a790aac00aecbf0d411d11` with the harness at revision
`328f93ea348fe569c56d7737206246c7df42eb9c`. Native builds the fixed workload
42.00% faster and with 48.25% less peak RSS than optimized Go, runs 18.02%
slower with 58.18% less peak RSS, and produces a 96.80% smaller stripped
executable. All four Go-parity metrics remain within the registered 25%
ceiling. The candidate also remains within every canonical compiler guardrail,
strips to 216,552 bytes, preserves the exact representative and scalar Float
applications, and closes exact Darwin and Linux arm64 replacement chains. See
the [Gate 6J result](../results/2026-08-29-gate6j-float-arrays-darwin-linux-arm64/README.md).

Gate 6K is the explicit configured-project slice registered in
[issue #80](https://github.com/type-rb/type-rb-native/issues/80) and specified
by [Decision 0018](decisions/0018-explicit-configured-project.md). It lets the
ordinary self-hosted compiler accept a directly named standard
`trbconfig.jsonc`, strictly decode a bounded Go-mode projection, enumerate and
check the complete production `sourceDir`, preserve root-relative module
identity, and build the unique top-level runnable `main()`.

The command remains experimental and continues to require explicit config,
output, QBE, and CC paths. Upward discovery, packages, native dependencies,
default output placement, test compilation, and stable CLI behavior are not
part of this slice. Directory enumeration uses a narrow internal physical
compiler-runtime boundary; it does not add a public TypeRB API or modify the
reference repository.

The retained Gate 6J seed predates that runtime boundary. One untimed Go-free
transition compiler may therefore introduce the adapter through the existing
file-root path before candidate B2. The transition is setup-only and does not
count as a candidate, measurement, or release seed. B2, B3, and B4 must all be
configured-project-capable and converge to exact QBE and executable bytes; no
Go or reference-compiler execution enters this transition or the ordinary
candidate chain.

The exact Gate 6H 1,025-file graph runs through configured Native, file-root
Native, and pinned optimized-Go project paths. Configured Native check, emit,
and build time and RSS must remain within 15% of the candidate file-root path.
Configured Native check and build plus Native application runtime and RSS must
remain within 25% of optimized Go, and the stripped Native application must be
at least 80% smaller. A fresh Gate 6J comparison bounds canonical compiler time
and RSS to +15% and stripped size to 248,000 bytes. Exact candidate B2/B3/B4,
fixed-point QBE, retained applications, full corpus, and pinned Linux arm64
correctness remain mandatory. See the
[Gate 6K plan](gate-6-configured-project.md).

Gate 6K is complete at measured implementation revision
`84e2e4a6e2cff9d7fdab46ce4eec33b609a597c4` with the reviewed harness at
revision `9d11966a92ca308d4bb84dacc59f47efbb92b6cc`. On the registered scale
project, configured Native check, emit, and build medians are 6.41%, 11.01%,
and 1.73% above the same candidate's file-root path. Against optimized Go,
Native configured check is 2.85% faster, build is 85.81% faster, and runtime is
18.73% faster, with materially lower peak RSS and a 96.98% smaller stripped
application. The fresh Gate 6J comparison remains within every canonical
compiler guardrail, and exact Darwin and Linux arm64 candidate chains close.
See the
[Gate 6K result](../results/2026-08-30-gate6k-configured-project-darwin-linux-arm64/README.md).

Gate 6L is the experimental bootstrap seed distribution slice registered in
[issue #90](https://github.com/type-rb/type-rb-native/issues/90) and specified
by
[Decision 0019](decisions/0019-experimental-bootstrap-seed-distribution.md).
It publishes one registered target-neutral root QBE plus attested Darwin and
Linux arm64 compiler seeds as immutable assets of a date-labelled prerelease.
The root translation is one-time setup provenance. Fresh post-publication jobs
must verify the actual release manifest, SHA-256 digest, and artifact
attestation before closing an ordinary B1/B2/B3/B4 chain without Go or the
reference compiler.

Two warmups and seven observations measure every adjacent compiler generation
on each target. Adjacent time and peak-RSS medians remain within 25%, a
greater-than-2x regression is catastrophic, each raw compiler asset remains at
or below 310,000 bytes, and the two compiler assets together remain at or below
620,000 bytes. Exact fixed points, the compiler and configured-project corpus,
failure and cleanup behavior, target inspection, process inventory, and
external tool accounting remain mandatory. This distribution slice registers
no application primary-metric improvement; stable versions, compatibility,
installation, tool bundling, and support remain deferred. See the
[Gate 6L plan](gate-6-bootstrap-seed-distribution.md).

The first post-seed source compatibility revalidation is registered in
[issue #97](https://github.com/type-rb/type-rb-native/issues/97). It advances
the exact TypeRB reference to `0.4.1-dev`, migrates repository source and the
self-hosted declaration-import subset, then uses the immutable Gate 6L seed to
close current Darwin/Linux arm64 B1/B2/B3/B4 chains. The seed identity and
current fixed-point identity remain separate. The
[recorded result](../results/2026-08-30-typerb-0-4-compatibility-darwin-linux-arm64/README.md)
passes the same two-warmup, seven-observation, 25%, 2x, 310,000-byte, and
620,000-byte bounds without publishing a replacement seed.

The successor revalidation is registered in
[issue #106](https://github.com/type-rb/type-rb-native/issues/106). It advances
the exact reference to TypeRB `0.4.3-dev`, adds an executable differential for
shared Array identity and parameter-local rebinding, and reruns the complete
selected-reference corpus plus previous-seed fixed points on Darwin and Linux
arm64. Because the immutable seed predates the current embedded runtime and
link policy, two separately identified Go-free setup transitions carry current
source and runtime before candidate B2. Candidate B2/B3/B4 exactness and all
registered time, RSS, process, and size boundaries remain unchanged and
independent of the reference revision.
The
[recorded result](../results/2026-08-30-typerb-0-4-3-compatibility-darwin-linux-arm64/README.md)
passes both targets: candidate B2/B3/B4 and cross-target QBE are exact, all
adjacent candidate spreads remain below 1.89%, and the combined compilers use
544,712 of the registered 620,000 bytes.

Independent experimental Native versioning and exact TypeRB compatibility
metadata are defined in
[Decision 0020](decisions/0020-independent-native-versioning.md). Native begins
at `0.1.0-dev`; strict schema version 1 declares only the exact verified TypeRB
version and revision while keeping compiler protocol, bootstrap, Native MIR,
runtime ABI, backend, target profiles, and evidence separate. CI validates the
record against canonical repository inputs. Stable distribution, installation,
support ranges, and deprecation guarantees remain outside this decision.

The ordinary-path runtime memory stability stage is registered in
[issue #104](https://github.com/type-rb/type-rb-native/issues/104). It replaces
process-lifetime allocation for supported Strings, Arrays, and managed records
with the existing exact-root non-moving collector, without adding ownership or
collection semantics to TypeRB. A reviewed CI smoke performs 5,000,000
allocation iterations. A separate manual Linux arm64 workflow closes the
current Go-free compiler chain, runs 300,000,000 iterations with 250 ms RSS
sampling, and retains ASan/LSan and Valgrind evidence. Final live managed bytes,
allocation accounting, a 4 MiB managed-heap ceiling, 64 MiB RSS ceiling, both
registered RSS-trend limits, the 5x calibration guardrail, compiler sizes, and
existing fixed points are mandatory. See the
[runtime memory stability plan](runtime-memory-stability.md). The
[recorded result](../results/2026-08-30-runtime-memory-stability-darwin-linux-arm64/README.md)
passes every frozen Stage 1 criterion: 42,300,000,000 managed bytes are
allocated and reclaimed, final live bytes and both RSS trend values are zero,
and ASan/LSan, Valgrind, exact fixed-point, process, and compiler-size checks
pass. Persistent Web and Job resource lifecycles remain deferred.

Gate 6M is the portable benchmark-entry primitive slice registered in
[issue #113](https://github.com/type-rb/type-rb-native/issues/113) and
specified by
[Decision 0021](decisions/0021-portable-benchmark-entry-primitives.md). It
implements the existing `Process.argv()`, `String#to_i()`, `Integer#to_s()`,
`Float#to_i()`, and `Math.sqrt()` contracts in the ordinary self-hosted
frontend and runtime. Exact standard-package roots are compiler-owned internal
identities; `sqrt` uses an explicitly linked system libm dependency.

The shared successful and failing corpus compares Native with the pinned
optimized Go backend. It fixes process-argument freshness, decimal syntax and
portable boundaries, canonical text, finite truncation, NaN and infinity
rejection, widening, and negative square root. Candidate Darwin and Linux
arm64 B2/B3/B4 chains and target-neutral QBE must converge from the immutable
previous-Native seed without Go in the ordinary chain.

Two warmups and seven alternating compiler observations bound candidate time
and RSS to +15% of the fixed current-main baseline and retain the 310,000-byte
per-target and 620,000-byte combined ceilings. Two warmups and at least eleven
application observations bound Native build time, build RSS, runtime, and
runtime RSS to within 25% of optimized Go while requiring an 80% stripped-size
improvement. See the
[Gate 6M plan](gate-6-portable-benchmark-entry.md). This prerequisite does not
stand in for the later cross-language benchmark result.

The
[recorded Darwin/Linux arm64 result](../results/2026-08-31-gate6m-portable-benchmark-entry-darwin-linux-arm64/README.md)
passes every frozen criterion. Candidate compiler time and RSS are 7.93% and
13.77% above the fixed baseline; both remain below the 15% ceiling. The
identical-source Native application is faster and lighter than optimized Go on
all four primary medians and at least 98.19% smaller when stripped. Exact
fixed points, the 573,720-byte combined compiler size, LLD, libm, failure
classes, and process boundaries are retained with the raw evidence.

Gate 6N is the Linux amd64 target-chain slice registered in
[issue #128](https://github.com/type-rb/type-rb-native/issues/128) and
specified by
[Decision 0025](decisions/0025-linux-amd64-target-profile.md). The internal
`linux-amd64-v0` profile maps to QBE `amd64_sysv`, the System V AMD64 ABI, and
the existing explicit Linux LLD/libm policy without forking the shared
frontend, target-neutral QBE, managed runtime, or TypeRB behavior.

Because the immutable experimental seed release has no amd64 compiler asset,
the registered recovery verifies its exact 658,639-byte target-neutral root
QBE, creates one root-era x86 compiler, and performs two Go-free current-source
transitions before entering the ordinary B2/B3/B4 candidate chain. Setup
identities and processes remain separate from candidate claims and candidate
measurements.

Two warmups and seven interleaved compiler observations compare the
Native-owned build with the equivalent external emit-QBE/QBE/CC recipe under a
25% time and RSS bound, while adjacent candidate medians remain within 10% and
each compiler stays at or below 310,000 bytes. Two warmups and at least eleven
interleaved application observations apply the existing 25% build/runtime
time/RSS bounds against optimized Go and require at least an 80% stripped-size
improvement. Elapsed time uses a direct monotonic process observer and peak RSS
uses an independent direct GNU time invocation, with complete per-observation
status, output, and artifact evidence. The portable bootstrap harness's legacy
combined time/RSS observations are retained only for its existing profiles;
the Gate 6N adjacent-build decision uses the independent controller series.
Exact fixed-point, current Linux arm64 regression, cross-architecture
target-neutral QBE, complete corpus, ELF, dependency, and process evidence
remain mandatory before Linux amd64 is recorded as a result. See the
[Gate 6N plan](gate-6-linux-amd64.md).

This gate is not authorization to ship. It evaluates:

- broader configured and packaged multi-module applications beyond the
  file-root slice;
- at least two primary target environments;
- incremental and reproducible builds;
- package and native-library boundaries;
- debugging and operational behavior; and
- total ongoing maintenance cost.

It also requires all build-time, memory, runtime, binary-size, and
toolchain-size measurements to use the self-hosted path.

The ordinary compiler accepts files and projects rather than the Gate 5
source-content adapter, uses the ordinary managed runtime, and performs
external-tool orchestration through explicit measured boundaries. A previous
Native release is the ordinary bootstrap seed; Go is not required.

Promotion requires a separate TypeRB design decision.

## Correctness checks

Each supported feature requires:

- reference-backend differential tests;
- valid and invalid MIR fixtures;
- boundary-value tests for layout and arithmetic;
- deterministic diagnostics for unsupported input;
- reproducible output checks; and
- randomized or fuzz validation when a verifier or encoder accepts structured
  untrusted input.

A candidate fails correctness if it obtains performance by weakening TypeRB
integer ranges, Unicode behavior, failure semantics, initialization order,
source attribution, or another portable guarantee.

## Measurements

### Build measurements

Report separately:

- reference frontend and snapshot production;
- snapshot validation and Native MIR lowering;
- optimization;
- backend code generation;
- assembly and object writing;
- linking; and
- total cold, warm, and incremental build time.

Also record peak compiler RSS and every process executed by the build.

### Runtime measurements

Depending on the workload, report:

- startup latency;
- steady-state throughput or completion time;
- latency distribution rather than only the best result;
- allocation count where available; and
- peak runtime RSS.

### Size measurements

Report:

- raw and stripped executable size;
- compressed artifact size when relevant;
- static and dynamic runtime dependencies;
- backend sidecars, assembler, linker, and required SDK components; and
- complete toolchain distribution size.

An executable that relies on a shared VM or uncounted runtime is not directly
comparable to a standalone binary without reporting both views.

## Benchmark record

Every published result should include:

- TypeRB, native repository, runtime, and backend revisions;
- exact commands, release flags, stripping, path metadata, and configuration;
- hardware, operating system, architecture, and toolchain versions;
- cache state and environment constraints;
- input corpus revision;
- warmup, repetition count, aggregation, and variance; and
- raw machine-readable results.

Store results under a date- and experiment-specific directory only after the
first executable benchmark exists. Do not commit placeholder result files.

## Backend selection policy

A backend implementation remains active only when it:

- passes the current correctness and reproducibility gates;
- satisfies the pre-registered non-inferiority and catastrophic-regression
  limits;
- achieves the pre-registered minimum improvement in at least one primary
  outcome before product feasibility, or has a concrete diagnostic role in
  reaching that outcome;
- has a credible path for the next required target and runtime feature;
- does not impose disproportionate distribution, security, or maintenance
  costs.

One production default is preferred. Separate development and release backends
remain possible only when their end-to-end advantages are both material and
stable. Experimental backends should not become user-visible configuration
merely because they win a microbenchmark.

A secondary improvement may justify a bounded diagnostic experiment, but it
does not pass product feasibility when all three primary outcomes miss their
registered gates.

## Reassessment policy

A missed checkpoint triggers diagnosis of the MIR, runtime, backend, or build
pipeline and a recorded plan to close the gap. Backend adapters may be replaced
or removed when another implementation serves their role better. The native
implementation itself is reconsidered only when evidence exposes a fundamental
conflict with portable TypeRB semantics, safe implementation, or sustainable
self-hosting—not merely because an early implementation needs optimization.

Temporary bootstrap surfaces still have no compatibility guarantee. Remove
them when the independent frontend replaces them, and retain generally useful
benchmark methodology, conformance tests, and architectural findings.
