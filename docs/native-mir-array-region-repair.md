# Array-header proof repair

Status: [PR #246](https://github.com/type-rb/type-rb-native/pull/246) is accepted
at `c131c43c`, merged as `5a231760`. The first candidate, `ce297d4`, fails correctness. Its successor,
`69ff52b5`, passes correctness but fails the n-body runtime control. The
two-entry control repair, `7c72eed7`, then fails recovery-bootstrap source
compatibility. The accepted repair addresses both failures without widening the
proof or changing a limit. The history below retains those rejected candidates;
only the final complete formal run establishes acceptance.

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
| Code-section bytes | 250,312 | 249,956 | 250,904 |
| Target-neutral QBE bytes | 1,119,802 | 1,119,022 | 1,120,000 |

The current compiler source SHA-256 is
`c30a4c09afac71bc6adfe4b226198afdc4fc42a0d4776c72c52e7dc7b11cc6c4`;
the test source SHA-256 is
`5ba3074304c7832563655f26c495546bdf8db7d78b05e1ea370a217595d0d58f`.
The ordinary local B1/B2/B3 executable and QBE fixed points are exact. All 22
valid, three mutation, and eleven runtime-invalid Native programs produce their
expected output, status, and diagnostics, with byte-identical QBE to the
two-entry repair. Root formatting and root/core type checks pass. The 89-test
Gate 4 suite, including self-parsing and QBE-backed execution, passes. All 80
root tests also pass with the pinned reference compiler and QBE environment
explicitly enabled, including recovery, ordinary self-hosted generations, and
the source differential corpus. An earlier run without that environment did
not exercise recovery and is not complete bootstrap evidence.

The three application QBE files and Darwin executables are identical before
and after the compactness refactoring. N-body and fannkuch-redux additionally
match the original baseline executables exactly. Spectral-norm retains the
improved candidate executable. The marker retains the original local
spectral-norm selection diagnostic (`0.884375x` wall, `0.880079x` CPU,
`0.980132x` RSS) because its measured executable remains byte-identical.

The completed local two-warmup, seven-observation comparisons at the registered
inputs retain wall/CPU/RSS ratios of `0.876122/0.877501/1.013423` for
spectral-norm, `1.007125/1.004844/1.000000` for n-body, and
`1.002086/1.001740/1.000000` for fannkuch-redux. All output and
retained-observation bounds pass. These are local diagnostics, not hosted
acceptance evidence.

## Recovery compatibility and earlier CI feedback

The [complete run at `7c72eed7`](https://github.com/type-rb/type-rb-native/actions/runs/33944107173)
passes quick checks, documentation, Darwin/Linux persistent-memory checks, both
Linux target regressions, and cross-target QBE identity. Native correctness
rejects `instruction[4] += literal_base`: snapshot v4 supports a narrower source
subset than the ordinary Native compiler. The performance matrix correctly
does not run after this failure. Ordinary Native fixed points do not establish
recovery compatibility.

The repair spells the relocation as ordinary indexed assignment. Retaining the
module in one local binding inside MIR commit also removes repeated outer
field lookups, keeping compiler QBE below its unchanged limit. No MIR fact or
lowering decision changes. Export of the isolated compiler closure to snapshot
v4 now succeeds. The fully enabled root suite also executes that snapshot
through recovery and ordinary self-hosted generations successfully.

CI now performs the existing snapshot-closure check before the expensive root
suite. Smoke/corpus evidence uploads run only when their producer was not
skipped; attempted experiments still upload on failure and still reject
missing evidence. The development skill explicitly requires the pinned
reference compiler and QBE environment for compiler-source recovery tests.

## Accepted formal verification

The [complete formal run at `c131c43c`](https://github.com/type-rb/type-rb-native/actions/runs/33946793548)
passes every required check, including recovery-enabled correctness, both Linux
target regressions, Darwin/Linux memory checks, adjacent fixed points,
cross-target QBE identity, build costs, compactness, and application controls.
The compiler QBE is 1,119,022 bytes with SHA-256
`55b1f79c8e0362080b4b5076669d7047c19850fb6ae1b8e8f7f47a0208fcb67d`.
Darwin and Linux arm64 compilers are 349,224 and 315,256 bytes respectively,
with code sections of 249,956 and 252,640 bytes. All frozen ceilings remain
unchanged; the combined compiler size is 664,480 bytes.

Linux arm64 uses two warmups and seven alternating retained observations per
role at the registered full inputs. Candidate/baseline wall, CPU, and RSS
ratios are respectively:

| Workload | Wall | CPU | RSS |
| --- | ---: | ---: | ---: |
| spectral-norm, 5500 | 0.881332 | 0.881264 | 1.000000 |
| fannkuch-redux, 12 | 1.000026 | 0.999976 | 1.000000 |
| n-body, 50000000 | 0.999966 | 0.999975 | 1.000000 |

Spectral-norm wall time falls from 4.081215329 to 3.596905668 seconds, an
11.867% reduction against the previous Native baseline. Its generated QBE
shrinks from 52,343 to 52,173 bytes. Both controls retain byte-identical QBE and
complete executables. All exact outputs and catastrophic-observation limits
pass. Darwin provides application correctness and size evidence, not a formal
runtime A/B series. Compiler build-wall/RSS ratios are 1.002688/0.997817 on
Darwin and 1.013216/1.000064 on Linux arm64.

The failed candidates and their measurements remain rejected. A consolidated
cross-language Pages refresh uses new runtime and build measurements at the
accepted merge revision, not the rejected candidate's measurements.

This repair still makes no new unchecked-access decision. General source-token
emission remains outside the parameter-header projection, and the selected
workload's strict-shrink and control-artifact limits apply to the complete
change, not just the restoring refactoring.
