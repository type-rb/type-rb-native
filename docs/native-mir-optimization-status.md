# Native MIR ownership status

The active [consolidation milestone](mir-consolidation.md) prioritizes complete
verified MIR ownership, removal of the ordinary direct path and cohesive source
organization. Correctness and reproducibility remain required. Detailed
performance qualification follows the architecture milestone; daily and weekly
measurements provide intermediate feedback.

## Implemented ownership

| Area | Current boundary |
| --- | --- |
| Typed scalar values | Integer, Boolean and Float literals, unary/binary operations and numeric conversion have explicit operands, result types, origins and failure edges. Straight-line leaves retain bounded inlining and verified Integer range guards. |
| Scalar conditional control | Immutable scalar bindings, nested `if`/`elsif`/`else`, early returns and continuing joins publish typed blocks and live-value arguments. QBE consumes these blocks without rereading the admitted function body. |
| Numeric Array induction | Selected zero-based traversal and Integer/Float reductions retain verified induction, address and accumulator relationships. The adapter consumes the established plan. |
| Array effects and headers | Ordered regions retain bindings, aliases, accesses, scope boundaries and conservative effect barriers. Verified function/loop plans select stable headers; element checks remain unless a separate induction proof permits removal. |
| Hash | Checked typed operation plans retain key/value layout, operands' source bindings and effects. They are still a projection alongside general control/value MIR. |
| Range and iteration | Checked construction and Array/Range traversal plans retain captured bounds/receiver, live Array length, lexical transfers and source bindings. Their execution is not yet unified with the general value/block path. |
| Assignment and Boolean operations | Checked plans own assignment evaluation order and binary/logical result semantics; remaining direct adaptation still consumes some source-indexed plans. |

Function adapter kinds explicitly distinguish scalar leaves, verified induction
and scalar conditional control. Verification checks their operation and shape
contracts as well as table bounds, value definitions, types, argument availability,
control targets and source origins. Block arguments are parallel assignments;
QBE adaptation captures edge values before overwriting destinations.

`control_mir_test.trb` checks nested branches and joins, malformed edges and adapter
selection. It also changes checked body tokens and requires identical generated
output. The `scalar-branches` differential fixture exercises Integer/Float/Boolean
branches and an unexecuted division-by-zero path across compiler generations.
Existing induction, arithmetic-failure, managed-lifetime and target controls remain.

## Responsibility boundaries

- `mir.trb`: typed module, function, block, instruction and value records, with
  shared identity/range queries.
- `mir_analysis.trb`, `mir_passes.trb`, `mir_verifier.trb`: proofs, rewrites and
  validation respectively.
- `checked_values.trb`, `mir_construction.trb`, `mir_builder.trb`, `mir_control.trb`:
  checked value projection, block construction and function publication.
- `checked_program.trb`: recursive source checking; it invokes the builders.
- `qbe_context.trb`, `qbe_memory.trb`, `qbe_numeric.trb`, `qbe_constants.trb`:
  backend context, memory adaptation, numeric lowering and static data.
- `qbe_mir.trb`, `qbe_control.trb`: existing optimized MIR and conditional-block
  adaptation, sharing one scalar operation adapter.

The [architecture map](architecture.md) records the complete ordinary closure.
Recovery uses an exact module/import inventory and the same source bodies; no
extracted implementation is copied or kept behind an old-name wrapper.

## Remaining work

General calls, mutable locals, arbitrary loops, managed values and complete
allocation/mutation/root-safety ownership still need the unified control/value
route. Their current checked operations and conservative GC protections remain
in force. The direct body emitter remains for those functions and must retire as
its consumers migrate. QBE memory adaptation still contains lifetime decisions
that belong above the backend; moving those helpers into a file does not complete
that ownership change.

The entry and recursive checker remain substantial modules. Further decomposition
should follow the remaining semantic ownership moves, preserving source origins,
recovery and ordinary fixed points. This status is not a percentage of full
TypeRB language or source-backend coverage.

## Measurements and history

The accepted [numeric regression recovery](native-numeric-regression-recovery.md)
and [formal runtime measurements](../results/2026-09-10-benchmarksgame-runtime-loop-local-headers-linux-arm64/README.md)
retain their exact source identities and observations. They do not qualify later
MIR migration candidates. No new Pure Go comparison or formal Pages performance
claim follows from this structural change.

Earlier extraction narratives, rejected variants and measurement links remain in
[the immutable prior status](https://github.com/type-rb/type-rb-native/blob/7726ff18e9230cd149e9f0c317577f6429f907fc/docs/native-mir-optimization-status.md).
Original evidence and the fixed migration/cumulative baselines are unchanged.
