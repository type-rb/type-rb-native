# Native MIR ownership status

The active [consolidation milestone](mir-consolidation.md) prioritizes complete
verified MIR ownership, removal of the ordinary direct path and cohesive source
organization. Correctness and reproducibility remain required. Detailed
performance qualification follows the architecture milestone; daily and weekly
measurements provide intermediate feedback.

## Implemented ownership

| Area | Current boundary |
| --- | --- |
| Typed scalar values | Integer, Boolean and Float literals, unary/binary operations and numeric conversion have explicit operands, result types, origins and failure edges. Verified numeric plans select bounded operation/call expansion from CFG/SSA facts; straight-line leaves retain verified Integer range guards. |
| Scalar control | Mutable scalar locals and parameters, nested `if`/`elsif`/`else`, `while`, `break`/`next`, early returns and continuing joins publish typed blocks and live-value arguments. Loop transfers carry only the enclosing environment; branch/body locals remain lexical. QBE consumes admitted bodies without rereading their source. |
| Short-circuit expressions | Scalar `&&` and `||` publish conditional RHS blocks and Boolean result joins, including nested call arguments and loop predicates. Dominance preserves earlier expression temporaries; skipped RHS calls and traps stay unexecuted. |
| Calls and declarations | Declaration identities, parameter types/mutability and return types are captured before body checking. Ordinary calls with supported scalar and managed arguments/results, including nominal records and Hash/Range carriers, retain explicit arguments and conservative allocation, mutation, I/O and failure effects, including forward and recursive callees. The verified standard `Math.sqrt` adapter has no managed-memory or observable side effects, so it is not a GC safe point and stable Array loop proofs can cross it. Other calls remain conservative. |
| Function values and lexical capture | Authored `fn` bodies, supported named function values, structural callback signatures, selected captured environments and indirect calls use verified MIR. Mutable captures share cells; the REPL retains checked code, environments and nominal type identities across submissions. |
| Namespaces and constants | Source-owned lexical declarations resolve before lowering. Exact global types, initializer functions, order, guarded reads and persistent managed roots live in MIR; the adapter consumes the verified catalog. Nullable global facts retain declaration identity across lexical scopes. See [decision 0067](decisions/0067-namespaces-and-constant-mir.md). |
| Managed Strings and roots | String literals, concatenation, equality, size, indexing, Integer/String/Float conversions and String/Boolean output use typed operations. Integer output explicitly converts first. Managed parameters, rebinding, returns and control joins use the same value/block path. MIR derives live-before roots at allocating operations and ordinary calls; verification recomputes the complete plan. |
| Managed Arrays | Supported scalar and managed element Arrays, including nominal records and their nesting, retain semantic element identity. Literals, live size, checked indexing, assignment, compound assignment and push use typed operations with allocation/mutation/failure effects. Admitted parameters, returns, rebinding and loop/branch values share managed liveness. Assignment captures its checked logical position before RHS evaluation, then reloads storage for the final store. |
| Nominal records | Declaration identity, authored names/origins and ordered field types live in MIR. Construction consumes an ordered operand span with allocating/failing effects; projections verify nominal owner and result type. Recursive records through containers retain their shells and field references. GC descriptors consume this verified table. |
| Numeric Array induction | Selected zero-based traversal and Integer/Float reductions retain verified induction, address and accumulator relationships. The adapter consumes the established plan. |
| Array effects and headers | CFG dominance, induction identities and conservative operation effects select stable headers. The retired token regions and direct-adapter header caches are removed; checks remain unless the typed plan proves them redundant. |
| Hash | Typed operations cover construction, lookup, update, deletion, copies and collection projections, including empty-Hash inference and managed carriers. Source-bound plans remain for checking and the REPL; QBE consumes only value/block MIR. |
| Range and iteration | Construction, captured bounds/receiver, live Array length, lexical transfers and Array/Range carriers use the general value/block route. Source-bound shapes are shared by checking and the REPL. |
| Assignment and Boolean operations | Typed operations own captured assignment targets, evaluation order and binary/logical result semantics. The retained `checked_operator_plans` projection serves the REPL, not QBE. |

Function adapter kinds distinguish scalar leaves and general scalar/managed
control; independent verifier fixtures retain their separate model kind. The
ordinary checker requires a MIR body for every accepted function. Verification checks their operation and shape
contracts as well as table bounds, value definitions, types, argument availability,
control targets, declaration/call/return types, conservative call effects and source origins. Block arguments are parallel assignments;
QBE adaptation captures edge values before overwriting destinations. Instruction
results retain stable MIR operand names even when block storage is reordered.

`mir_flow.trb` derives reachability, reverse postorder, immediate dominators and
value definition sites and a function-local Hash type index after structural/identity validation.
Its predecessor and incoming-argument indexes retain both arms when a branch
targets the same block. Array-loop alias propagation and natural-loop traversal
reuse these derived edges instead of rescanning every block for every parameter.
The verifier rebuilds this information from current MIR; it is not a persistent
cache or an input optimization fact. Type indexes are rebuilt from current rows,
so later raw-MIR edits cannot reuse stale types. Function parameters
are available everywhere; reachable blocks may use dominating definitions, while
unreachable blocks may only use function parameters and their own earlier
values. Same-block instruction uses must follow their definitions. Sparse
identity indexes and block/edge arrays avoid storage proportional to the largest
value ID or a quadratic dominance matrix. Instruction failure edges must end in
empty traps; they cannot carry a value into an ordinary continuation. This is
verifier analysis, not caller-supplied optimization metadata.

`control_mir_test.trb` checks mutable branches, loops, lexical transfers, malformed
edges and adapter selection. `call_mir_test.trb` checks recursive/forward/Void calls,
missing callees, argument availability/types and forged effects or declarations. It also changes checked body tokens and requires identical generated
output. The `scalar-branches` differential fixture exercises Integer/Float/Boolean
branches and an unexecuted division-by-zero path across compiler generations.
The `scalar-loop-calls` differential fixture adds loop-carried parallel copies,
nested transfers, early returns, mutable parameters, Float arithmetic, ordered
nested call arguments, recursion and Void calls. Call overflow/division fixtures
retain the portable failure classes. The `scalar-short-circuit` fixture covers
ordered effects, earlier call/binary operands, skipped division, and loop
predicates. `logical_test.trb` also executes it with reversed MIR block storage
and erased admitted source bodies. `flow_mir_test.trb` compares dominance with an
independent node-removal reachability oracle over all 343 three-block graphs
with at most two successors, and rejects unavailable return/edge operands.
The `managed-string-mir` fixture adds managed calls/returns, loop rebinding,
short-circuit String operations, negative indexing, conversion and nested calls
that grow the root buffer. `managed_mir_test.trb` erases all admitted bodies,
reverses block storage and executes the result with a test-only collection before
every String allocation. Independent expectations require the first call argument
to survive later argument allocation and discard undemanded branch bindings.
Tampered roots, capacity, instruction identities and String operations reject.
Existing induction, managed-lifetime and target controls remain. All ordinary
function bodies now use MIR. `numeric_mir_test.trb` rejects missing or forged
numeric/call plans and retains decisions after source erasure, physical block
reordering and repeated optimization. No performance improvement is inferred.

The `managed-array-mir` fixture adds nested managed Arrays, owner replacement
during compound assignment, growth across a retained negative-index target,
mixed Float literals, Boolean elements, managed call arguments/returns and
branch/loop joins. `array_mir_test.trb` executes erased/reordered MIR with
collection immediately before every allocating operation and call in ordinary
functions. Malformed element graphs, Array operations and omitted roots reject.

## Responsibility boundaries

- `mir.trb`: typed module, function, block, instruction and value records, with
  shared scalar encodings and identity/range queries, plus portable declarations
  and conservative call records.
- `mir_analysis.trb`, `mir_numeric.trb`, `mir_flow.trb`, `mir_passes.trb`: portable numeric proofs, expansion selection, CFG/dominance
  and rewrites. `mir_verifier.trb` checks structure/edges; `mir_instructions.trb`
  checks typed instruction contracts.
- `checked_values.trb`, `mir_construction.trb`, `mir_builder.trb`, `mir_control.trb`:
  checked value projection, block construction and function publication.
- `mir_identities.trb`: fresh sparse function/value identities and definition counts, avoiding whole-module pairwise comparisons.
- `mir_types.trb`: canonical composite type identities and shared managed/element
  classification, with unique container identities and predeclared nominal shells for recursive record fields.
- `mir_arrays.trb`: typed Array construction, selection, load/store and push
  contracts; no backend address is retained across a right-hand side.
- `mir_records.trb`, `qbe_records.trb`: nominal construction/projection contracts and their ABI adaptation. Readonly field bindings remain distinct from SSA IDs and mutable projected values.
- `qbe_arrays.trb`: ABI adaptation of verified Array operations.
- `mir_calls.trb`: declaration capture, checked calls and their verification.
- `mir_strings.trb`: String, conversion and output construction/contracts.
- `mir_roots.trb`: operation effects, backward managed-value liveness and exact
  safe-point root plans. Block parameters transfer only demanded values.
- `qbe_strings.trb`, `qbe_roots.trb`: runtime adaptation of those operations and
  publication of the verified root lists, without backend lifetime analysis.
- `mir_logical.trb`: conditional RHS and expression-result join construction.
- `checked_types.trb`: assignability, operator result types and diagnostics.
- `argument_binding.trb`: shared required positional/named slots and record labels; authored evaluation precedes operand reordering.
- `checked_program.trb`: recursive source checking; it invokes these owners.
- `qbe_context.trb`, `qbe_functions.trb`, `qbe_numeric.trb`, `qbe_constants.trb`:
  target operands/labels, function ABI and MIR-selected root-frame prologues,
  selected numeric spelling and static data. No lexical local/header/root analysis.
- `qbe_mir.trb`, `qbe_control.trb`: existing optimized MIR, explicit calls and scalar-block
  adaptation, sharing one scalar operation adapter.

The [architecture map](architecture.md) records the complete ordinary closure.
Recovery uses an exact module/import inventory and the same source bodies; no
extracted implementation is copied or kept behind an old-name wrapper.

## Nominal record validation

`record_mir_test.trb` rejects forged nominal identities, field owners/types and
origins, wrong constructor arguments and missing initializer roots. Same-shaped
records remain distinct. Grouping must retain readonly field bindings while
projected mutable Array values remain usable. The `managed-record-mir` fixture
covers recursive and cyclic record Arrays, ordered initializer calls, Float
conversion, branches, retained aliases and allocation pressure. Its test erases
admitted source bodies and the old checked field metadata, requires identical
QBE, reorders blocks, then runs with collection before allocating operations.

Constructors evaluate authored fields once in source order, store their operands
by declaration slot and publish a
fully initialized object from explicit MIR operands. Managed initializers remain
live across later initializers and the allocation itself; no partially initialized
record escapes the operation. The backend's function-local operand types and the
verifier's Hash index avoid repeating whole-module type searches as admission
grows. These are derived lookup structures, not unverified optimization facts.

## Sole MIR emission and numeric selection

The checker rejects an accepted function without a MIR body. QBE uses the verified
signature for parameter/result ABI and the MIR root plan for frame capacity.
The direct expression/body emitter, token Array regions and assignment-effect
analyses, backend numeric budgets, lexical local slots, header caches and textual
root-publication filtering are removed. `qbe_functions.trb` owns function emission;
`compiler.trb` retains orchestration and declaration-bound runtime hooks. Output
storage grows with emitted lines instead of imposing a source-token size guess.

`mir_numeric.trb` derives natural-loop membership through dominance and selects
expansion in function/block identity order. Modules with at most 32 bodies have
64 loop operations, six outside operations and two leaf-call expansions; modules
with at most 96 bodies have 32 loop and three outside operations. Larger modules
use shared numeric helpers. This retains a bounded policy while removing the
old backend's lexical-loop and deferred-function budget state. Every ordinary
function definition is emitted; call expansion no longer decides definition
omission implicitly. A future use-graph pass can select dead bodies explicitly.

Small-operand facts mean Integer values in `[0, 1024]`, not arbitrary nonnegative
values. This bound permits a checked multiply without overflowing the machine
intermediate. Selected additions keep the required upper/lower checks; other
operations retain shared helpers, explicit zero checks or guarded fallback.
Inline leaf copies can use verified caller argument bounds. Their emitted literal
operands do not silently become new caller proofs. Optimized-module verification
recomputes the entire plan, including owners, sites, operations and modes, only
after validating MIR structure, types and operands. Input MIR cannot supply plans.

## Remaining work

The ordinary emission route is unified; this does not establish full TypeRB
language, standard-library or source-backend coverage. Those gaps remain in the
[language coverage contract](native-language-coverage.md) and Capabilities.
General constant/range propagation, call-effect summaries, broader inlining and
explicit dead-body elimination still need shared MIR passes. Ordinary call
effects remain conservative allocation/mutation barriers; managed liveness is
intraprocedural. Root publication rewrites the frame segment from its live-before
plan, reloads root-buffer addresses across calls and preserves managed-return ABI.

The recursive checker and compiler driver still need responsibility-based
splitting. Preserve source origins, recovery and ordinary fixed points during
that work. Full milestone acceptance also requires measurement and improvement
against the fixed Native/Pure Go baselines; structural completion alone does not
establish runtime, build-time or binary-size parity.

## Measurements and history

The accepted [numeric regression recovery](native-numeric-regression-recovery.md)
and [formal runtime measurements](../results/2026-09-10-benchmarksgame-runtime-loop-local-headers-linux-arm64/README.md)
retain their exact source identities and observations. They do not qualify later
MIR migration candidates. No new Pure Go comparison or formal Pages performance
claim follows from this structural change.

Earlier extraction narratives, rejected variants and measurement links remain in
[the immutable prior status](https://github.com/type-rb/type-rb-native/blob/7726ff18e9230cd149e9f0c317577f6429f907fc/docs/native-mir-optimization-status.md).
Original evidence and the fixed migration/cumulative baselines are unchanged.

## Function values and lexical capture

Structural callback signatures, closure construction and indirect calls share
verified MIR type, effect and root ownership. Ordinary `fn` bodies analyze selected
captures and lower through the same checked body and MIR pipeline as named
functions. Mutable captures share cells, and unknown calls invalidate their
nullable proofs. The backend consumes verified capture layouts and exact
parameter/result types, including Float and Void. The REPL retains checked code,
environments and originating nominal types across submissions. See
[decision 0051](decisions/0051-callable-mir-foundation.md).

Shared ordinary-file and REPL probes cover higher-order calls, nested closures,
managed captures and mutable cells. Internal fixtures add source erasure,
reordered MIR storage, forced collection and malformed type/operand controls.
Named declarations used as values and the remaining signature/capability
boundaries stay open in the [language inventory](native-language-feature-inventory.md).
This does not establish complete function-value coverage or a public callable ABI.
