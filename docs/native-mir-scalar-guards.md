# Guarded scalar Integer regions

Status: accepted through [PR #372](https://github.com/type-rb/type-rb-native/pull/372).
The complete formal cohort confirms the spectral-norm objective below.

A complete straight-line scalar MIR function can describe several checked
Integer operations even when its caller remains on the direct path. Checking
each operation separately leaves multiple branches in small inlined numeric
helpers. The pass proves a common nonnegative parameter range for the
whole region and guards that range once at an existing inline call site.

`Gate4MirFunction.integer_guard` is zero in input MIR. A nonzero value is an
exclusive power-of-two upper bound for every parameter. The pass tries the
existing multiplication fast-path domain, 2^26, then successively halves it.
An unsigned comparison of the bitwise union of the parameters against this
bound rejects negative inputs and any input outside the common domain.

The proof is disabled above the existing 32-function inline budget. It accepts
one to four Integer parameters, a scalar entry returning its
result directly, and at most 32 instructions. It propagates inclusive lower
and upper bounds through nonnegative literals, addition, multiplication and
division with a strictly positive divisor. Before calculating bounds, it checks
addition against the remaining portable maximum and multiplication against the
maximum divided by the other upper bound. The analysis itself cannot overflow. Named range records keep each lower/upper
pair together; a checked decimal decoder uses recovery-supported basic operations.
Float arithmetic and conversions retain their original order and operations.
Unsupported instructions disable the plan. At least three checked Integer
operations must be removed to amortize the entry guard.

The verifier first validates the original function, blocks, values and
instructions, then independently recomputes the plan. Input facts, widened or
noncanonical bounds, missing optimized facts and stale proofs are rejected.
The adapter consumes only that verified plan. It emits the existing checked
body for rejected inputs and a body with proved-safe Integer operations for
accepted inputs. Arguments are evaluated once before the branch; neither body
contains calls, managed access, allocation or other effects. Failure behavior
and portable Integer bounds remain unchanged outside the guarded domain.

Specialization is restricted to the existing bounded scalar inline policy.
Standalone functions retain their checked body. No benchmark names, fixed
workload dimensions, source patterns or emitted-QBE analysis select the plan.
The range analysis and its fact remain in MIR; the adapter only lowers the
validated branch and arithmetic. Deferred Array-loop work and remaining
record-field/Array-effect migration are separate questions.

Acceptance requires the issue's prospective runtime/control comparison and
unchanged compiler, recovery, target and memory authorities. Compiler size,
self-build costs and generated application costs are reported separately
against both immediate and cumulative controls. Current formal cross-language
runtime/build evidence is required before changing Pages performance claims.


## Evidence and remaining scope

The [accepted checkpoint](../results/2026-09-09-scalar-range-guards-accepted-darwin-linux-arm64/README.md)
records safety/recovery checks, compiler costs, the local interleaved comparison
and earlier rejected attempts. The [complete formal runtime cohort](../results/2026-09-09-benchmarksgame-runtime-scalar-range-guards-linux-arm64/README.md)
uses revision `2841cb93` on Linux arm64. Its one-core spectral-norm median is
2.30664 seconds versus Pure Go's 3.21933 seconds; CPU time also improves.
The two other kernels remain slower, and the local cumulative comparison
retains their earlier regressions. These results do not establish broad parity.

The new named `MirScalarRange` record keeps transient lower/upper bounds
explicit within MIR analysis. It avoids adding a positional carrier or a
second semantic owner in the emitter. General Array assignment and call-effect
ownership remain separate work, with no change to source evaluation order.
