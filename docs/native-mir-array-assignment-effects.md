# Checked Array assignment effect regions

This bounded MIR projection retains target capture, initial index validation,
conservative call/allocation barriers, and the final store for one assignment.
It applies to ordinary indexed assignment and compound assignment, including
Arrays projected from record fields. It does not admit those records or the
whole enclosing function into complete control-flow MIR.

The source contract remains unchanged: evaluate the receiver and index once,
validate and normalize the selected position before the RHS, then perform the
store after the RHS. Effects may replace or reallocate Array storage and may
collect managed objects. They must not leave a stale address or unrooted owner.

`mir_array_assignment_plan` derives three mechanical lowering choices from the
checked region:

| Region effects | Owner lifetime | Final address |
| --- | --- | --- |
| No index or RHS barrier | No additional temporary root | Reuse the initial checked address |
| Index barrier, no RHS barrier | Root before evaluating the index | Reuse the address checked after the index |
| RHS barrier | Root owner; retain a managed old value for compound assignment | Retain the normalized position and check current storage again |

Unknown calls and allocating primitives remain conservative barriers. Existing
verified scalar leaves and the non-allocating square-root primitive retain
their established effect facts; evaluating their arguments still records any
nested effects. Header stability is not inferred from record-field readonly
bindings. Integer failures and initial bounds failures preserve their order.

The checker attaches capture, check and store origins to the region and retains
its operation sequence. Both target and store map to the same region. The MIR
query rejects malformed operations, missing or reordered target phases, foreign
origins and mismatched store bindings. The backend revalidates before consuming
the plan and makes no source-text or benchmark-specific effect inference.
Completed region arrays are detached from subsequent checking; a later condition
must not append operations to an already published assignment region.

This replaces the old pair-only target projection with a checked operation
region. General call-effect summaries, complete Array assignment instructions,
record projections and loop-wide bounds proofs remain separate work. The
existing effectful path and its managed/reallocation regressions remain required.

[Issue #354](https://github.com/type-rb/type-rb-native/issues/354) records the
bounded investigation and prospective measurement contracts. Current candidate
validation, failed attempts and exact-source evidence are recorded there; a
local diagnostic does not replace a complete published runtime cohort.
