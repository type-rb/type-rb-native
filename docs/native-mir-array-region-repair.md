# Array-header proof repair

Status: the first candidate in [PR #246](https://github.com/type-rb/type-rb-native/pull/246)
is rejected. Passing the recorded timing and compactness checks at `ce297d4`
does not establish correctness, and those timings are not accepted performance
evidence.

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

## Remaining acceptance work

The current compiler source SHA-256 is
`1c4cefd0de3b1780eb3007aa790db42f3060d91871c99c438a5ef7602bf2ac48`;
the test source SHA-256 is
`277c96d81a820cb32931ab81c3bf804a920d4cb30cb04036a2dc68c8d741e9fc`.
It passes all eleven runtime-invalid and 22 valid Native fixtures and an
ordinary local Native B1/B2/B3 fixed point. All 33 fixtures emit byte-identical
QBE before and after the shared-builder refactoring. The three benchmark
programs also retain exact QBE and executable bytes. Root formatting, type
checks, all 80 root tests, and all 86 Gate 4 tests pass, including self-parsing
and QBE-backed executable emission. Hosted acceptance remains a separate
requirement.

| Darwin arm64 compiler metric | Initial correctness repair | Current repair | Unchanged ceiling |
| --- | ---: | ---: | ---: |
| Complete executable bytes | 349,224 | 349,224 | 350,000 |
| Code-section bytes | 259,800 | 250,312 | 250,904 |
| Target-neutral QBE bytes | 1,149,251 | 1,119,802 | 1,120,000 |

The shared builders recover 1,184 code-section bytes and 2,799 QBE bytes from
the preceding parameter-only checkpoint. All local compiler-size conditions
now pass without changing a ceiling. Removing the entire fallback cache is
not a valid shortcut: that diagnostic fits the compiler ceilings but emits 52,356
bytes of spectral-norm QBE, exceeding its strict-shrink condition, and 68,784
bytes of n-body QBE, exceeding the control's 1.02 ratio. Keep the shared
fallback implementation; its eventual MIR migration is still due.

The current local input-5500 diagnostic retains exact output over two warmups
and seven alternating retained processes per role: candidate/baseline medians
are approximately `0.884375x` wall time, `0.880079x` CPU time, and `0.980132x`
peak RSS. Its spectral-norm QBE is 52,173 bytes and code section is 10,684
bytes. Those application bytes are unchanged by the builder refactoring.
This is a local selection signal, not formal Linux arm64 evidence or accepted
performance. Hosted target, build-cost, control, and memory limits still need
fresh verification for the current compiler.

The transition marker now identifies this locally eligible corrected compiler
and its fixtures. Its local runtime fields retain the diagnostic above because
the measured application executables are byte-identical. No limit changes, and
the rejected first candidate remains rejected. PR #246 can now request complete
correctness, fixed-point, target, memory, and comparative performance authority.
The accepted Pages snapshot stays unchanged until those requirements pass.

This repair narrows the original issue #245 plan: it makes no new unchecked
access decision, and general source-token-driven emission remains outside this
parameter-header projection. Unsupported operations preserve TypeRB behavior;
the shared header loader may renumber QBE temporaries, and the fallback cache
retains one recent header rather than two. Exact unchanged-program bytes are
therefore a refactoring control, not a universal claim against the original
baseline. The frozen selected-program shrink and control-artifact limits still
apply to the complete change.
