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

### Gate 6: Self-hosted product feasibility

This gate is not authorization to ship. It evaluates:

- representative multi-module applications;
- at least two primary target environments;
- incremental and reproducible builds;
- package and native-library boundaries;
- debugging and operational behavior; and
- total ongoing maintenance cost.

It also requires all build-time, memory, runtime, binary-size, and
toolchain-size measurements to use the self-hosted path.

The ordinary compiler accepts files and projects rather than the Gate 5
source-content adapter, uses the production managed runtime, and performs
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
