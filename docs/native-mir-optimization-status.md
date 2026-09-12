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
| Scalar control | Mutable scalar locals and parameters, nested `if`/`elsif`/`else`, `while`, `break`/`next`, early returns and continuing joins publish typed blocks and live-value arguments. Loop transfers carry only the enclosing environment; branch/body locals remain lexical. QBE consumes admitted bodies without rereading their source. |
| Calls and declarations | Declaration identities, parameter types/mutability and return types are captured before body checking. Ordinary calls with scalar arguments and scalar/Void results retain explicit arguments and conservative allocation, mutation, I/O and failure effects, including forward, recursive and direct-path callees. |
| Numeric Array induction | Selected zero-based traversal and Integer/Float reductions retain verified induction, address and accumulator relationships. The adapter consumes the established plan. |
| Array effects and headers | Ordered regions retain bindings, aliases, accesses, scope boundaries and conservative effect barriers. Verified function/loop plans select stable headers; element checks remain unless a separate induction proof permits removal. |
| Hash | Checked typed operation plans retain key/value layout, operands' source bindings and effects. They are still a projection alongside general control/value MIR. |
| Range and iteration | Checked construction and Array/Range traversal plans retain captured bounds/receiver, live Array length, lexical transfers and source bindings. Their execution is not yet unified with the general value/block path. |
| Assignment and Boolean operations | Checked plans own assignment evaluation order and binary/logical result semantics; remaining direct adaptation still consumes some source-indexed plans. |

Function adapter kinds explicitly distinguish scalar leaves, verified induction
and general scalar control. Verification checks their operation and shape
contracts as well as table bounds, value definitions, types, argument availability,
control targets, declaration/call/return types, conservative call effects and source origins. Block arguments are parallel assignments;
QBE adaptation captures edge values before overwriting destinations.

`control_mir_test.trb` checks mutable branches, loops, lexical transfers, malformed
edges and adapter selection. `call_mir_test.trb` checks recursive/forward/Void calls,
missing callees, argument availability/types and forged effects or declarations. It also changes checked body tokens and requires identical generated
output. The `scalar-branches` differential fixture exercises Integer/Float/Boolean
branches and an unexecuted division-by-zero path across compiler generations.
The `scalar-loop-calls` differential fixture adds loop-carried parallel copies,
nested transfers, early returns, mutable parameters, Float arithmetic, ordered
nested call arguments, recursion and Void calls. Call overflow/division fixtures
retain the portable failure classes. Existing induction, managed-lifetime and
target controls remain. Direct managed callers retain bounded scalar inlining;
general scalar MIR calls currently remain explicit until the existing policy
has a verified interprocedural owner. No performance improvement is inferred.

## Responsibility boundaries

- `mir.trb`: typed module, function, block, instruction and value records, with
  shared scalar encodings and identity/range queries, plus portable declarations
  and conservative call records.
- `mir_analysis.trb`, `mir_passes.trb`, `mir_verifier.trb`: proofs, rewrites and
  validation respectively.
- `checked_values.trb`, `mir_construction.trb`, `mir_builder.trb`, `mir_control.trb`:
  checked value projection, block construction and function publication.
- `mir_calls.trb`: declaration capture, checked calls and their verification.
- `checked_types.trb`: assignability, operator result types and diagnostics.
- `checked_program.trb`: recursive source checking; it invokes these owners.
- `qbe_context.trb`, `qbe_memory.trb`, `qbe_numeric.trb`, `qbe_constants.trb`:
  backend context, memory adaptation, numeric lowering and static data.
- `qbe_mir.trb`, `qbe_control.trb`: existing optimized MIR, explicit calls and scalar-block
  adaptation, sharing one scalar operation adapter.

The [architecture map](architecture.md) records the complete ordinary closure.
Recovery uses an exact module/import inventory and the same source bodies; no
extracted implementation is copied or kept behind an old-name wrapper.

## Remaining work

Managed arguments/results and values, structured short-circuit expressions,
Array/Range iteration and complete allocation/mutation/root-safety ownership
still need the unified control/value route. Runtime/host intrinsics retain their
existing adapters. The new call effects are conservative barriers, not precise
interprocedural no-allocation or liveness summaries. Their current checked operations and conservative GC protections remain
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
