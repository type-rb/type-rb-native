# Development and Validation Plan

## Engineering objective

Build a TypeRB-specific native AOT pipeline with these primary outcomes:

1. End-to-end application build time that matches or improves the optimized Go
   backend.
2. Generated-program execution time that matches or improves established
   statically typed language implementations across representative portable
   workloads.
3. Deployed executable size that matches or improves the optimized Go backend.

The compiler and runtime are implemented in TypeRB, reproduce themselves, and
must retain competitive build time and generated-code behavior once the
complete self-hosted toolchain is measured. Early gates establish this outcome
incrementally; they are not a sequence of throwaway demonstrations.

Secondary outcomes include compiler and runtime peak memory, startup latency,
toolchain distribution size, portability, diagnostics, correctness risk, and
maintenance cost.

The identical-source comparison baseline is an optimized release executable
produced by the reference compiler's Go backend. It isolates backend and
runtime changes, but it is not the final execution-performance ceiling.
Cross-language runtime context uses pinned established implementations without
an intentionally unoptimized, unstripped, cold, or otherwise disadvantaged
configuration.

## Principles

- Correctness precedes performance.
- All candidates use the same TypeRB inputs, supported semantics, Native MIR
  corpus, benchmark policy, and, for same-target comparisons, the same target
  ABI profile.
- Unsupported behavior fails explicitly.
- Measurements include serialization, lowering, optimization, code generation,
  assembly, linking, runtime, and required external components.
- TypeRB semantic analysis and reusable optimization decisions belong to
  verified Native MIR and target-independent passes, not to a backend emitter.
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

## Self-hosted MIR optimization transition

The early bootstrap path proved a distinct Native MIR. The compact self-hosted
compiler later reached closure through direct QBE emission, with several local
semantic facts represented in emitter state. Before adding broader range,
alias, effect, or loop optimization, the self-hosted path restores the intended
MIR boundary described by
[Decision 0028](decisions/0028-native-mir-optimization-boundary.md).

The transition is incremental but has one target architecture:

1. Complete already registered narrow emitter experiments and preserve their
   accepted or rejected evidence.
2. Define the smallest Native MIR value, block, operation, origin, and verifier
   subset that can carry one current hot scalar/Array loop vertically.
3. Represent only the facts needed by that slice, beginning with Integer range
   or nonnegativity, index validity, loop induction/bounds, call allocation and
   mutation effects, Array-header stability, and GC safety.
4. Run target-independent transforms over verified MIR and lower the result
   through the existing QBE ABI without source-pattern discovery in the
   adapter.
5. Move existing optimization families into this path and remove their
   superseded emitter ownership before adding broader analysis.

Each slice retains source origins, exact TypeRB behavior, deterministic output,
self-hosted fixed points, the complete conformance corpus, and registered
application outputs. A no-optimization or unchanged region must remain a useful
differential control while the slice is introduced.

For the first explicit pass in an already measured fact family, pre-register
both sides of the trade: any small compiler-QBE or code-section cost must fit
the existing temporary envelope with no complete-compiler growth, while the
selected generated workload must strictly shrink and improve materially in
wall and CPU time without an RSS regression. The pass cost remains recoverable
migration space, not permission to expand the envelope or enter another fact
family.

Historical MIR transition measurements and their exact source-era bounds are
preserved in the [gate reference](gate-reference.md#mir-transition-history).
The [current MIR status](native-mir-optimization-status.md) records accepted
ownership and the remaining direct path; it is not complete general-purpose
MIR lowering. The [transition policy](../tools/native-mir-transition-policy.sh)
and its exact validated markers remain the executable source for current
limits. Only a preregistered marker introduction may use its one-time ratios;
later ordinary changes return to 1.05. Recovery, generated-code and application
identity, catastrophic, process, stack, and cleanup bounds remain independent.
Recover the temporary compiler increase by the end of the portable range,
index, and induction migration before beginning another fact family. This
reorganization neither changes a limit nor marks that recovery complete.

LLVM remains deferred until the shared path and benchmark corpus cover scalar,
Array, allocation, and I/O behavior. Its first role is a bounded
optimization-ceiling comparison over the same MIR and ABI, not a second copy of
TypeRB semantic analysis.

## Repository organization checkpoints

Repository maintenance is scheduled alongside the MIR transition, not deferred
until performance parity or product promotion. Follow the
[organization schedule](repository-organization.md): shorten documentation
entry points now, inventory and complete the first support-source cleanup
before the pending checked-binary implementation, then extract compiler
responsibilities incrementally at accepted ownership checkpoints. The scope
includes root `src/gateN_*` files, numbered QBE adapters, tests, tooling, and
implementation symbols as well as `compiler/gate4/`.

Keep these changes independently reviewable and preserve every applicable
recovery, fixed-point, correctness, measurement, and compactness requirement.
Historical gate evidence remains intact. A passed optimization checkpoint
must identify the next bounded organization slice or its explicit blocker.

## Gates

The detailed gate contracts and their recorded measurements are preserved in
[the gate reference](gate-reference.md). They describe successive engineering
checkpoints, not active source layers or current product support. Use the
[current capability map](https://type-rb.github.io/type-rb-native/) and
[MIR status](native-mir-optimization-status.md) for current coverage.

### Gate 0: Boundary

See the [preserved contract](gate-reference.md#gate-0-boundary).

### Gate 1: Heap-free execution

See the [preserved contract](gate-reference.md#gate-1-heap-free-execution).

### Gate 2: Heap-free aggregate value model

See the [preserved contract](gate-reference.md#gate-2-heap-free-aggregate-value-model).

### Gate 3: Runtime viability

See the [preserved contract](gate-reference.md#gate-3-runtime-viability).

### Gate 4: Self-hosting compiler completeness

See the [preserved contract](gate-reference.md#gate-4-self-hosting-compiler-completeness).

### Gate 5: Matched self-hosted compiler baseline

See the [preserved contract](gate-reference.md#gate-5-matched-self-hosted-compiler-baseline).

### Gate 6: Self-hosted product feasibility

See the [preserved contract](gate-reference.md#gate-6-self-hosted-product-feasibility).

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
