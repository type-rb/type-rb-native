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

The checker now records a bounded backend-independent projection of raw local
bindings and operations. Each operation has four Integer fields: kind, first
operand, second operand, and source-token origin.

| Kind | Raw operation | Operands |
| --- | --- | --- |
| 1 | Binding | Local slot, initializer/type tag |
| 2 | Loop entry | Index slot and Array slot, or `-1, -1` for an unsupported condition |
| 3 | Loop end | `0, 0`, with the matching entry origin |
| 4 | Array access | Array slot, index slot |
| 5 | Integer write | Local slot, exact unit increment (`1`) or other write (`0`) |
| 6 | Opaque operation | Blocks header reuse for the function |

Binding tags encode an immutable Array (`-2`), mutable Array (`-3`), literal
Integer zero (`-4`), unknown initializer (`-1`), or an earlier Integer-local
initializer slot. They describe checked operations, not asserted proof bits.
Binding origins remain unique when lexical slots are reused.

The analysis derives nonnegative induction and the dominating exact Array-length
condition, tracks writes and lexical scope, and rejects malformed rows. An
unknown Integer update invalidates the whole plan, including earlier accesses
whose next iteration could otherwise be unsafe. Conditionals, unproved calls,
growth, Array and record allocation, argument-vector creation, String indexing
and concatenation, and allocating Integer-to-String conversion conservatively
block the function. Only the
already verified scalar leaves and known nonallocating numeric intrinsics are
allowed through the call boundary.

The optimizer publishes the selected binding identity and access origin. The
verifier recomputes the plan from the raw region before QBE emission. Other
statements still use the accepted direct path: this projection does not claim
complete function lowering into the general Native MIR.

## Remaining acceptance work

The repair checkpoint passes focused proof-tampering and source-regression
tests, all eleven runtime-invalid fixtures on Native Darwin arm64, and a local
Native fixed-point check. The 84-test Gate 4 run before the final allocating
String exclusions also passes; those exclusions have separate focused tests.
The compiler source digest is
`7115c75ce67f96349a50151a4b10124749f92cb305d2f593a5cc9a87e3dec316`.
Its complete Darwin compiler is 349,224 bytes, its code section is 259,800
bytes, and its target-neutral QBE is 1,149,251 bytes. The latter two exceed
the unchanged 250,904-byte and 1,120,000-byte ceilings in issue #245. Compact the
representation and remove duplicated analysis before repeating the complete
correctness, fixed-point, target, memory, and comparative performance authority.
Keep the PR in draft and the accepted Pages snapshot unchanged until that
corrected candidate passes every registered condition.

The existing transition marker still identifies the rejected first candidate;
this correctness checkpoint does not register a new performance candidate or
change a limit. A follow-up diagnostic retains the ordinary access check while
reusing the verified header and still shows a useful local runtime signal.
The next implementation should test this narrower proof boundary before
spending more code size on access-check elimination. It must pass the same
registered acceptance conditions, including the formal Linux arm64 comparison.
