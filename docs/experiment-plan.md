# Experiment Plan

## Research question

Can a TypeRB-specific native AOT pipeline improve at least one of these primary
outcomes without unacceptable regressions in the others?

1. End-to-end application build time.
2. Generated-program execution time.
3. Deployed executable size.

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
- Thresholds and removal rules are recorded before reviewing a result.
- Microbenchmarks diagnose a phase; representative programs determine
  viability.

Before a gate begins, its issue must record metric-specific non-inferiority
bounds, a minimum meaningful primary-metric improvement, catastrophic-regression
limits, and a time or engineering-effort budget. These values cannot be revised
after results are reviewed merely to keep a candidate alive.

## Candidate sequence

The candidates are not implemented to production completeness in parallel.
They advance through small shared gates and can be removed early.

1. Use hand-authored bootstrap and MIR fixtures to validate the boundary.
2. Use QBE or a similarly small path for the cheapest runtime feasibility
   check.
3. Use Cranelift as the first balanced AOT candidate.
4. Add LLVM only after the corpus is representative enough to measure an
   optimization ceiling.
5. Attempt a direct emitter only if profiling shows codegen or toolchain
   overhead dominates and the MIR, layouts, and ABI have stabilized.

This order is a starting hypothesis, not a compatibility promise.

## Gates

### Gate 0: Boundary

Scope:

- versioned, data-only fixtures;
- strict snapshot and MIR verification;
- deterministic diagnostics for malformed and unsupported input; and
- source identity retained through lowering.

Exit condition: the experiment can validate and lower fixtures without
importing the reference compiler's internal objects.

### Gate 1: Heap-free execution

Scope:

- functions and direct calls;
- branches and loops;
- Boolean, Integer, and Float values;
- exact checked Integer behavior;
- static strings and observable output; and
- simple static-layout records or tagged values.

Every backend candidate at this gate runs the same differential corpus against
the reference compiler's Go backend. A mismatch is triaged against the TypeRB
specification and accepted conformance behavior rather than automatically
treating either implementation as correct.

### Gate 2: Portable value model

Scope may expand to:

- records and payload enums;
- `Result` representation and propagation;
- arrays and dynamic strings;
- closures and captured environments; and
- deterministic observable behavior, defined allocation failure, and
  reproducible artifacts.

Only candidates that pass Gate 1 correctness and comparability continue.

### Gate 3: Runtime viability

Scope may expand to:

- memory-management strategy and cycles;
- classes, interfaces, unions, and nullable values;
- source-mapped failures and unwind behavior;
- module initialization; and
- selected filesystem, process, time, and JSON operations.

At most one default candidate should normally reach broad runtime work. A
second candidate requires a distinct, measured development or release role.

### Gate 4: Product feasibility

This gate is not authorization to ship. It evaluates:

- representative multi-module applications;
- at least two primary target environments;
- incremental and reproducible builds;
- package and native-library boundaries;
- debugging and operational behavior; and
- total ongoing maintenance cost.

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

## Selection policy

A candidate remains only when it:

- passes the current correctness and reproducibility gates;
- satisfies the pre-registered non-inferiority and catastrophic-regression
  limits;
- achieves the pre-registered minimum improvement in at least one primary
  outcome before product feasibility;
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

## Abandonment policy

Archive or remove the native path if time-boxed milestones show that:

- no candidate improves the practical tradeoff over an optimized release
  executable produced by the reference compiler's Go backend;
- a candidate exceeds its registered time or engineering-effort budget without
  passing the current gate;
- gains disappear after linking, runtime, sidecars, and distribution are
  counted;
- correctness requires a competing dialect or weaker semantics;
- the boundary repeatedly duplicates or leaks the reference frontend;
- source mapping, runtime safety, or package interoperability requires
  backend-specific language APIs;
- a second primary target requires divergent language semantics, a separate
  frontend or runtime, or disproportionate target-specific maintenance; or
- maintenance and security costs outweigh the demonstrated benefit.

If abandoned, retain generally useful benchmark methodology, conformance tests,
and architectural findings. Remove experimental bootstrap surfaces that have no
remaining consumer rather than preserving compatibility for a failed
experiment.
