# Gate contracts and historical architecture reference

This reference preserves the detailed checkpoint contracts and historical
architecture narrative formerly embedded in the development plan and
architecture page, extracted from revision
`bc5fd034ca33760c067ad2e3a520ab7327f86364` without changing their text.
Historical sizes, future-tense statements, and command boundaries belong to
their recorded checkpoints; they are not a current support claim or a new
acceptance policy. See the [current development plan](experiment-plan.md),
[architecture](architecture.md), and [MIR status](native-mir-optimization-status.md).

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

The next exact-reference revalidation is registered in
[issue #144](https://github.com/type-rb/type-rb-native/issues/144). It advances
the oracle to TypeRB `0.4.4-dev`, replaces all repository-owned uses of the
removed aggregate filesystem facade with bounded scoped-file support, and
keeps recursive directory creation outside the ordinary compiler closure. The
[recorded result](../results/2026-08-31-typerb-0-4-4-compatibility-darwin-linux-arm64/README.md)
passes all selected-reference and target regressions. Darwin/Linux arm64
B2/B3/B4 compilers and target-neutral QBE are exact within the candidate and
against the registered Native baseline; the worst candidate build/RSS median
ratio is 1.0004 and the combined compilers use 567,824 bytes.

The compiler compactness follow-up registered in
[issue #146](https://github.com/type-rb/type-rb-native/issues/146) changes only
the representation of profitable static Strings of at least 256 bytes. A
deterministic bounded-backreference encoder in the self-hosted compiler emits
dependency-free data that expands once into zero-filled static storage before
entry; the decoder and initialization call are omitted when unused. The
[formal Darwin/Linux arm64 result](../results/2026-08-31-static-string-compactness-darwin-linux-arm64/README.md)
passes exact fixed-point and target-neutral-QBE checks, all registered
correctness and process boundaries, and the 5% build-time/RSS caps. The
Darwin/Linux compiler pair decreases from 567,824 to 535,304 bytes, while the
16 KiB application fixture's QBE decreases by 61.62% and its executables by
24.50% and 49.04% respectively.

Independent experimental Native versioning and exact TypeRB compatibility
metadata are defined in
[Decision 0020](decisions/0020-independent-native-versioning.md). Native begins
at `0.1.0-dev`; strict schema version 2 declares only the exact verified TypeRB
version and revision while keeping compiler protocol, bootstrap, Native MIR,
runtime ABI, backend, target profiles, and evidence separate. It also
distinguishes immutable seed assets from independently
[recovered target-chain evidence](decisions/0026-recovered-target-chain-evidence.md).
CI validates the record against canonical repository inputs. Stable
distribution, installation, support ranges, and deprecation guarantees remain
outside this decision.

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

The next persistent-process layer is registered separately in
[issue #150](https://github.com/type-rb/type-rb-native/issues/150). It uses one
authored worker lifecycle for both Native and optimized Go, a bounded 64-entry
state cache, explicit retry/failure/cancellation paths, and a sampled internal
collector trace. CI runs the 40,000-batch smoke on Darwin and Linux arm64. The
manual Linux arm64 workflow runs 921,600,000 original jobs, samples RSS,
descriptors, and threads every 250 ms, and retains ASan/LSan and Valgrind
oracles. This layer verifies a single-threaded persistent worker process; it
does not introduce a public TypeRB service API or stand in for concurrency and
external-resource lifecycle work. See the
[persistent worker harness](../tools/runtime-worker-soak/README.md).

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
improvement. Elapsed time uses a direct monotonic process observer. Each
application-build observation batches eight direct launches, and the roughly
one-millisecond runtime case batches 32; both retain the raw batch duration and
use its per-launch normalization for the registered comparisons. Every launch
must agree in status and output, and build batches must publish the expected
final artifact. Peak RSS uses an independent single-process GNU time
invocation, with complete per-observation status, output, and artifact
evidence. The portable bootstrap harness's legacy
combined time/RSS observations are retained only for its existing profiles;
the Gate 6N adjacent-build decision uses the independent controller series.
The
[recorded Gate 6N result](../results/2026-08-31-gate6n-linux-amd64/README.md)
passes the exact fixed-point, current Linux arm64 regression,
cross-architecture target-neutral QBE, complete corpus, ELF, dependency,
process, measurement, and size criteria. The 240,888-byte compiler is
effectively level with the external compiler recipe, while the bounded
identical-source Native application is faster, lighter, and 99.26% smaller
than optimized Go when stripped. See the
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

## MIR transition history

The 255,000-byte ceiling and similar historical bounds registered for ordinary
local optimization candidates were not silently relaxed. The first structural
MIR issue measured the minimal skeleton before freezing separate ceilings of
302,000 bytes on Darwin arm64, 272,000 bytes on Linux arm64, and 574,000 bytes
combined. The later scalar-connection measurement freezes the next temporary
envelope at 317,000, 290,000, and 607,000 bytes respectively. The first
complete control-flow connection was then measured at 332,696 Darwin arm64
bytes, 308,656 Linux arm64 bytes, and 641,352 bytes combined before issue #225
froze ceilings of 334,000, 310,000, and 644,000 bytes. The exact foundation
transition alone may use its `1.07x` compiler-size and `1.12x` build-time
ratios; the exact scalar-connection transition alone may use `1.07x` and
`1.15x`; and the exact control-flow transition alone may use `1.08x` and
`1.25x`. Later ordinary changes return to `1.05x`. RSS,
fixed-point, generated-QBE/application identity, catastrophic, process, stack,
and cleanup bounds remain independently enforced. The complete temporary
increase must be recovered by the end of portable range, index, and induction
migration, before the next fact family. The long-term Go-competitive build and
generated-artifact objectives remain mandatory. See the
[recorded foundation result](../results/2026-09-02-native-mir-foundation-linux-arm64/README.md),
[scalar-connection freeze](https://github.com/type-rb/type-rb-native/issues/221),
and [control-flow freeze](https://github.com/type-rb/type-rb-native/issues/225).

The accepted ownership and exact-consumption slices reach revision
`993f563e3e4654c62d18b49d147bd3a7f1b6e2f2`. Structured checking derives the
exact literal-zero, checked-unit-step nonnegative induction fact and the active
base plus small nonnegative literal fact into dedicated checked-program
storage. Nested facts depend explicitly on the enclosing verified loop. Each
checked Array-index postfix stores its exact fact origin. A target-independent
resolver follows any enclosing-loop dependency before the QBE adapter requests
only the final fact at that postfix, without source-token proof, a whole-loop
lexical scan, QBE-local dependency traversal, or emitted-value range
propagation. The ordinary static compilers are 299,656 Darwin arm64 bytes and
271,784 Linux arm64 bytes, 571,440 combined. The Linux artifact retains only
40 bytes of structural cost over the accepted MIR foundation. This is still an
incremental connection: general function/block/value MIR lowering, a reusable
expression-origin/range model, and replacement of the broader emitted-value
representation are still due.
See the [current transition status](native-mir-optimization-status.md).

The next vertical slice carries one complete `Array<Integer>` induction helper
through MIR blocks and block parameters. It verifies its zero origin, checked
unit step, loop comparison, exact Array load, backedge, exit, overflow trap,
and bounds trap before MIR-only QBE emission. Unsupported helpers remain
direct. Completion requires deleting the corresponding token fact and emission
ownership; the measured envelope cannot fund another fact family.

## Architecture checkpoint history

The first Native-owned orchestration boundary is the experimental Gate 6B
single-file build. The TypeRB-authored compiler invokes explicit QBE and C
toolchain paths directly with `execv`, never through a shell, and atomically
publishes the finished executable after cleaning its intermediate QBE IL and
assembly. This proves ownership of the ordinary build graph without implying
that toolchain discovery, a stable project command, or a self-contained
distribution has been designed. See
[Decision 0009](decisions/0009-native-single-file-build.md).

Gate 6C closes that ordinary build graph after an initial seed exists. A
Native-built compiler becomes the executable seed for the next complete build,
and repeated same-basename generations must converge to exact bytes while
retaining the fixed-point QBE and full file-command behavior. Recovery may
prepare the first seed during the experiment, but its provenance is recorded
separately and it is not part of the ordinary Native-to-Native chain. See
[Decision 0010](decisions/0010-native-bootstrap-closure.md).

Gate 6D applies the same target-neutral compiler source, QBE IL, runtime
semantics, and Native-to-Native build graph to Linux arm64. Internal versioned
profiles select QBE's `arm64_apple` or `arm64` lowering and the corresponding
external linker policy; they do not fork language behavior or enter the
reference repository. Explicit selection makes the target part of the
reproducibility record and keeps cross-platform builds from depending on silent
host inference. Linux arm64 currently selects LLD through the supplied C driver.
See [Decision 0011](decisions/0011-linux-arm64-target-profile.md) and
[Decision 0022](decisions/0022-linux-arm64-lld-linker.md).

Gate 6E adds a config-free file-root module graph without changing that process
boundary. The TypeRB-authored compiler reads the selected entry and only its
transitive project declaration imports, preserves declaration ownership per
module, and emits one executable after the complete closure checks
successfully. The original gate accepted only named imports; the current
frontend also implements the bounded TypeRB 0.4 declaration-root mapping.
Unrelated siblings, package discovery, configured projects, and the hidden
single-source recovery adapter do not enter the original graph. See
[Decision 0012](decisions/0012-file-root-module-closure.md).

Gate 6F makes that graph reflexive: the canonical TypeRB-authored compiler is
itself a file-root closure with separate storage and path modules. A temporary
flat source may prepare the recovery seed, but every ordinary replacement
generation loads the real closure and reaches exact B2/B3/B4 QBE and bytes.
See [Decision 0013](decisions/0013-multi-file-self-hosted-compiler.md).

Gate 6G derives a deterministic module-qualified function index from the
canonical declaration arrays before resolution. Full key comparison preserves
semantics under collisions, while source-order head insertion preserves the
previous last-match behavior. The index is TypeRB-owned and internal; it is not
a public Hash or serialized compiler format. See
[Decision 0014](decisions/0014-indexed-function-lookup.md).

Gate 6H applies the same internal-derivation rule to file-root module graphs.
An incrementally maintained module-name index and parsed per-module import
spans let loading and resolution follow module-owned ranges, while contiguous
declaration boundaries stop duplicate scans before another module. Canonical
source-order arrays retain ownership. The private bucket and graph
accelerators do not stabilize a project, package, module, Hash, or CLI
contract. See
[Decision 0015](decisions/0015-indexed-module-graph.md).

Gate 6L makes the first durable previous-Native seed handoff without turning
the experiment into a stable release. A one-time registered fixed-point QBE
root produces attested Darwin and Linux arm64 compiler assets in an immutable
date-labelled prerelease. Fresh consumers verify the manifest, digest, and
attestation before an ordinary B1-to-B4 chain that contains no Go or reference
compiler. Compiler binaries stay out of Git history, while QBE, CC, system
libraries, GitHub release retention, and attestation infrastructure remain
explicit dependencies. See
[Decision 0019](decisions/0019-experimental-bootstrap-seed-distribution.md).

Gate 6M introduces two exact portable standard-package roots without making
the project module graph a package manager. Private compiler identities map
`trb/std/process` and `trb/std/math` to their existing `Process` and `Math`
declarations. Managed runtime helpers copy process arguments and implement
checked numeric text and narrowing operations; `Math.sqrt` crosses an explicit
C ABI and system-libm boundary. The portable-entry runtime slice is selected
as one unit when any registered process or conversion primitive is used and is
omitted otherwise, while the Native-owned link command supplies `-lm`
consistently on both registered profiles. These are internal lowering and
dependency choices rather than new TypeRB APIs or stable Native ABI. See
[Decision 0021](decisions/0021-portable-benchmark-entry-primitives.md).

Gate 6N adds an internal Linux amd64 profile behind the same self-hosted
frontend, target-neutral QBE emission, and managed runtime. The immutable
target-neutral root QBE recovers one root-era x86 compiler, followed by two
Go-free current-source transitions and the ordinary exact candidate chain.
The profile selects QBE `amd64_sysv`, the System V ABI, and the existing
explicit Linux LLD/libm link policy. This is a second-architecture experiment,
not a stable target or a target-specific semantic fork. See
[Decision 0025](decisions/0025-linux-amd64-target-profile.md).
