# Array-header proof repair

Status: [PR #246](https://github.com/type-rb/type-rb-native/pull/246) remains
unaccepted. The first candidate, `ce297d4`, fails correctness. Its successor,
`69ff52b5`, passes correctness but fails the n-body runtime control. The current
repair restores that control without widening the proof or changing a limit.

## Review findings

The initial implementation copied a producer-selected binding/access pair into
optimization facts and compared the two. This did not independently prove
header stability, index range, or dominance. Three executable regressions also
showed that the direct fallback could omit a required bounds panic: an index
increment before the access, an Array-length bound extended by one, and a later
decrement that invalidated the next iteration's nonnegative premise.

## Repair boundary

The current repair proves only header reuse for an immutable Array parameter.
It does not infer an index range or remove an access check. A parameter already
dominates its uses and remains in scope for the complete function, so this
boundary needs neither a second lexical-binding table nor an induction
interpreter. Local aliases remain outside the new proof.

The checker records a backend-independent projection with three Integer cells
per operation: kind, operand, and origin. Parameters form an ordered prefix;
their position supplies their function-local ordinal. Parameter origins are
indexes into the checked declaration table; other origins identify tokens.

| Kind | Raw operation | Operand |
| --- | --- | --- |
| 1 | Parameter | `0` non-Array, `1` immutable Array, `2` mutable Array |
| 4 | Parameter Array access | Parameter ordinal |
| 6 | Opaque effect or control | `0`; blocks header reuse for the function |

The analysis validates row shape, the parameter prefix and origins, access
references, and known operation kinds. It selects the first accessed immutable
Array parameter only when no blocking operation is present. The optimizer
publishes one parameter ordinal per function, or `-1` for no plan. The verifier
recomputes that result from the raw region; it does not trust a copied producer
selection. A collapsed opaque region is sufficient to reject the function.

Conditionals, unproved calls, growth, Array and record allocation,
argument-vector creation, String indexing and concatenation, and allocating
Integer-to-String conversion block the function. Only already verified scalar
leaves and known nonallocating numeric intrinsics cross the call boundary.
Element mutation alone does not change the header. This projection does not
claim complete function lowering into the general Native MIR.

The QBE adapter loads the selected parameter's length and data pointer in the
function prologue. Its ordinary index normalization and upper-bounds test stay
in place; separate previously accepted MIR index proofs remain unchanged.
Header field loading is shared by induction lowering and the direct adapter,
and one MIR parameter-registration path supplies both representations.
Checked instruction construction now has one builder instead of seven copies
of the same eight-cell layout. Parameters and expressions also share value-ID
allocation and value-row construction while retaining their distinct source
tables. This removes duplicated representation ownership without adding a new
optimization or moving analysis into QBE.

The remaining direct-path cache is not a function-wide invariant. Entering a
nested loop must discard it: a later append on that loop's backedge can change
the previously loaded header. A new executable regression first reads an
Array in an outer loop and then grows it inside an inner loop. The faulty
candidate panics; the repaired candidate produces the exact expected total.
Only the separately verified immutable-parameter header survives invalidation.

## Rejected control candidate

The [complete comparison at `69ff52b5`](https://github.com/type-rb/type-rb-native/actions/runs/33939737675)
passes correctness, fixed points, target regressions, memory smoke, and compiler
compactness. On Linux arm64, spectral-norm improves from 4.081436718 to
3.592571062 seconds, an 11.978% reduction. Fannkuch-redux is byte-identical and
its runtime is effectively unchanged. However, n-body increases from
10.448269730 to 11.823397073 seconds: a 1.131613 ratio, outside the 1.02 control
limit. The retained ranges do not overlap. This separate regression prevents
acceptance even though the selected workload passes its 10% improvement goal.

That candidate reduced the recent-header fallback from two entries to one.
The separately verified parameter header does not replace a second recent
entry for functions operating on multiple record-field Arrays. Restoring only
the two-entry fallback reproduces the baseline's complete 67,246-byte n-body
QBE, while preserving the improved 52,173-byte spectral-norm QBE. The local
two-warmup, seven-observation diagnostic against the rejected executable has
wall/CPU/RSS ratios of `0.861576`, `0.865986`, and `1.0`. This isolates recovery
from the rejected candidate; it is not an improvement claim over the baseline.

Removing the entire fallback is also rejected: that diagnostic emits 52,356
bytes of spectral-norm QBE, exceeding its strict-shrink condition, and 68,784
bytes of n-body QBE, exceeding its control limit. The eventual migration of the
remaining fallback into MIR is still due.

## Two-entry repair and compactness

The fallback again keeps two most-recently-used headers, independent of the
verified parameter tuple. Both fallback entries are invalidated together at
the existing boundaries, including nested-loop entry. Focused tests cover
alternating length/data reuse, least-recently-used eviction, invalidation of
both entries, and preservation of the independently verified tuple.

The direct restoration initially emits 1,121,231 compiler-QBE bytes, above the
unchanged 1,120,000-byte ceiling. The repair recovers that space through shared
tuple construction and transfer of completed function-owned MIR instruction
rows instead of copying their eight fields into another allocation. Commit is
called once after checking; the caller discards its local state immediately
afterward. Only literal-table operands are relocated, and no subsequent checker
mutation shares ownership with the optimizer. Value rows already follow this
transfer pattern. A regression test checks distinct function literals and
their original source lines. The instruction count is fixed before transfer,
avoiding repeated length loads from an unchanged collection.

| Darwin arm64 compiler metric | Rejected `69ff52b5` | Current repair | Unchanged ceiling |
| --- | ---: | ---: | ---: |
| Complete executable bytes | 349,224 | 349,224 | 350,000 |
| Code-section bytes | 250,312 | 250,248 | 250,904 |
| Target-neutral QBE bytes | 1,119,802 | 1,119,987 | 1,120,000 |

The current compiler source SHA-256 is
`d2706bf577782c7e7693b116deba2fab12575a89a5f597ec081536611260abf1`;
the test source SHA-256 is
`5ba3074304c7832563655f26c495546bdf8db7d78b05e1ea370a217595d0d58f`.
The ordinary local B1/B2/B3 executable and QBE fixed points are exact. All 22
valid, three mutation, and eleven runtime-invalid Native programs produce their
expected output, status, and diagnostics. Root formatting, type checks, and all
80 root tests pass. The 89-test Gate 4 suite, including self-parsing and
QBE-backed execution, passes; a final six-test header/relocation rerun also
passes.

The three application QBE files and Darwin executables are identical before
and after the compactness refactoring. N-body and fannkuch-redux additionally
match the original baseline executables exactly. Spectral-norm retains the
improved candidate executable. The marker retains the original local
spectral-norm selection diagnostic (`0.884375x` wall, `0.880079x` CPU,
`0.980132x` RSS) because its measured executable remains byte-identical.

## Remaining acceptance work

The marker registers the corrected source identity and local sizes before
hosted verification; every numerical limit remains unchanged. Fresh complete
correctness, target, fixed-point, memory, build-cost, and runtime-control checks
must pass for this compiler before acceptance. The failed candidates and their
measurements remain rejected. The accepted Pages snapshot stays unchanged.

This repair still makes no new unchecked-access decision. General source-token
emission remains outside the parameter-header projection, and the selected
workload's strict-shrink and control-artifact limits apply to the complete
change, not just the restoring refactoring.
