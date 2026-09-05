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

The remaining direct-path cache is not a function-wide invariant. Entering a
nested loop must discard it: a later append on that loop's backedge can change
the previously loaded header. A new executable regression first reads an
Array in an outer loop and then grows it inside an inner loop. The faulty
candidate panics; the repaired candidate produces the exact expected total.
Only the separately verified immutable-parameter header survives invalidation.

## Remaining acceptance work

The current compiler source SHA-256 is
`68e26d25c3d9a071b189b9a852c67cf21dee0a7ff6835c333e53cf8820edc5f9`;
the test source SHA-256 is
`277c96d81a820cb32931ab81c3bf804a920d4cb30cb04036a2dc68c8d741e9fc`.
It passes 40 focused MIR/numeric/Array tests, all eleven runtime-invalid and
22 valid Native fixtures, and an ordinary local Native B1/B2/B3 fixed point.
The preceding shared-load checkpoint also passed all 86 Gate 4 tests and the
80 root tests; the final parameter-registration consolidation has the focused
tests and Native executions above, not a new complete hosted acceptance run.

| Darwin arm64 compiler metric | Initial correctness repair | Current repair | Unchanged ceiling |
| --- | ---: | ---: | ---: |
| Complete executable bytes | 349,224 | 349,224 | 350,000 |
| Code-section bytes | 259,800 | 251,496 | 250,904 |
| Target-neutral QBE bytes | 1,149,251 | 1,122,601 | 1,120,000 |

The current repair still exceeds the code-section ceiling by 592 bytes and
the QBE ceiling by 2,601 bytes. Removing the entire fallback cache is not a
valid shortcut: that diagnostic fits the compiler ceilings but emits 52,356
bytes of spectral-norm QBE, exceeding its strict-shrink condition, and 68,784
bytes of n-body QBE, exceeding the control's 1.02 ratio. Keep the shared
fallback implementation while removing further duplicated ownership.

The current local input-5500 diagnostic retains exact output over two warmups
and seven alternating retained processes per role: candidate/baseline medians
are approximately `0.884375x` wall time, `0.880079x` CPU time, and `0.980132x`
peak RSS. Its spectral-norm QBE is 52,173 bytes and code section is 10,684
bytes. This is a local selection signal, not formal Linux arm64 evidence or
accepted performance: compiler compactness still fails.

The existing transition marker still identifies the rejected first candidate;
this checkpoint does not change a limit or register a new formal candidate.
Keep PR #246 in draft and the accepted Pages snapshot unchanged. After local
eligibility, record the exact corrected identity and repeat complete
correctness, fixed-point, target, memory, and comparative performance authority
before acceptance.
