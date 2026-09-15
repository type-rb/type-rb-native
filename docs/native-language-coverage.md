# Ordinary Native language coverage

Status: the shared contract contains 134 ordinary-path probes and 32 feature
families derived from the pinned reference AST and public language/standard-library
documentation. This is a test inventory with explicit gaps, not complete language
support. [Issue #454](https://github.com/type-rb/type-rb-native/issues/454) owns
basic-language completion; [the generated family inventory](native-language-feature-inventory.md)
records semantic contracts that still need tests. The earlier 19-case inventory
was an initial sample, not a complete list of missing features.

## Current development priority

Complete useful language families together with their MIR dependencies, instead
of waiting for individual unsupported programs to be reported. TypeRB at
`TYPE_RB_REVISION` remains the semantic authority; no Native-only dialect is
introduced. Fix wrong acceptance, wrong results and unsafe behavior as soon as
the shared probes reveal them.

The ordinary String foundation now supports UTF-8 literals, code-point
length/indexing, concatenation, interpolation, allocation/lifetime and source/REPL
handling. Continue with the remaining escapes and String APIs recorded in the
shared inventory. Keep raw byte operations explicit where source decoding or
terminal editing needs them; character indexing and terminal cell widths remain
separate contracts.

Then coordinate the record/Hash/iteration MIR family, arguments and function
values, expression control flow, nullable/enum/Result behavior, and the remaining
basic declaration/type families according to their dependencies. The inventory
keeps wider source interop and package syntax visible as later phases, with
reasons; a retired reference AST node is identified explicitly. Do not count
these phase labels as implemented support.

The [MIR consolidation milestone](mir-consolidation.md) coordinates the shared
ownership work. Correctness, memory safety, process and reproducibility checks
remain required. Temporary performance/size regressions are observed during
integration; detailed qualification occurs at coherent milestones. A feature
need not manufacture a runtime speedup or a separate size budget revision to
justify its existence. Final performance goals remain unchanged.

## Value-producing control and lexical transfers

Full `if`/`elsif`/`else`, Integer/String literal `case`, and ternary expressions
produce checked values through ordinary typed MIR joins. Branches execute lazily;
case evaluates its selector once. Numeric branches widen to Float where needed,
branch-local bindings stay scoped, and managed aliases retain their reference
capabilities. Value-producing full controls currently require an `else`.

Conditional `return`, `break` and `next` evaluate their guard before the guarded
value or transfer. A branch that transfers contributes no join operand. Enclosing
expressions preserve evaluation order and skip subsequent work after an
unconditional transfer. See [the ownership decision](decisions/0041-value-control-mir.md)
for the supported subset, verification and remaining pattern/type boundaries.

## Nullable values and safe navigation

`T?`, explicit `nil`, direct nil guards, returning guards and short-circuit RHS
narrowing lower to verified MIR operations. Safe navigation evaluates its receiver
once and skips member arguments on the absent edge. Optional values retain their
payload identity in calls, defaults, returns, records, Arrays and Hashes, including
zero and false payloads. The private traced layout and remaining flow/REPL gaps
are recorded in [decision 0042](decisions/0042-nullable-mir.md).

## Named/default arguments and record field order

Ordinary functions support positional parameters followed by `*` and named-only
parameters, with optional defaults in either group. Required parameters cannot
follow defaults within a group; the named-only group starts a new boundary. Explicit arguments run in authored order, then
MIR call operands are arranged in declaration order. Named labels resolve through
the selected declaration, including imported aliases. A label cannot supply a
positional-only parameter; duplicate/unknown labels, positional arguments after
named arguments, missing required values and wrong types are rejected.

Record construction remains keyword-only and now accepts reordered fields. Each
initializer uses its selected field's expected type, preserving contextual Float
conversion and managed values across later initializer evaluation. The shared
binding module also serves the REPL. Tests erase source and label metadata,
reverse MIR blocks and force collection before allocation/calls. QBE consumes
only normalized typed operands; it performs no label lookup or evaluation-order
analysis.

Configured REPL imports suppress the corresponding generated project imports.
Authored function and record aliases retain declaration identity across calls,
retained bindings and replay; see the [REPL contracts](native-cli.md#repl).

Default arguments and record initializers run in declaration scope, after all
explicit expressions, in parameter/field order. Only preceding declaration slots
are available; caller locals and later parameters/fields are not. Every default
is resolved and checked even if all callers supply that argument. Each omitted
managed default allocates a fresh value; explicitly passed aliases retain their
normal sharing. Record fields must place required fields before defaults.

Private typed initializer functions share ordinary MIR calls, verification and
root planning; see [the lowering decision](decisions/0040-default-initializer-mir.md).
No absent operand or null placeholder enters the final MIR call. Tests cover
source erasure, reversed block storage, forced collection, imported aliases,
short-circuit defaults and independent REPL evaluation. Nullable defaults preserve
the distinction between an omitted argument and an explicit `nil`; the shared
`nullable-default-presence` case covers both paths. Method/function-value/payload-enum
argument handling remains a gap until the underlying value and callable families
are supported.

## Ordinary UTF-8 String foundation

The shared cases cover Japanese text, two- through four-byte characters,
combining code points, negative indices, concatenation, interpolation, equality,
Hash keys, record/Array storage, embedded NUL and long literals. The additional
`tools/native-utf8-test.py` exercises Unicode paths and argv, rejects malformed
source bytes before token decoding, and forces collection before every String
allocation while indexed values and their owners remain live. Terminal tests
exercise evaluation as well as wide-character and combining-mark editing.

String headers retain UTF-8 byte length and code-point count separately. Size is
constant time; ASCII indexing keeps its bounded static cache and allocates
nothing. Non-ASCII indexing scans code points and creates a managed one-character
String. MIR therefore treats String indexing as potentially allocating and
failing, and verifies the receiver's live root. Positions count code points;
grapheme clusters are not language indices. Terminal cell widths remain a
separate presentation concern. Further non-ASCII indexing optimization can use
this semantic boundary without changing the language contract.

The ordinary compiler serializes literal bytes through the declaration-bound
`compiler_string_bytes` runtime adapter and validates raw source with
`compiler_source_is_utf8`. These are typed compiler internals, like source input
and slicing, not public String APIs. Their source bodies preserve the preceding
ASCII bootstrap boundary. Go-hosted canonical recovery emission remains narrower
than the final ordinary compiler and must not be counted as ordinary UTF-8
evidence. No seed, pin or Go fallback is added to the ordinary chain; acceptance
requires the published seed's full replacement generations and fixed points.

Unicode identifiers, Unicode escapes and the remaining String receiver APIs are
still tracked separately. This foundation does not mark the entire String family,
standard library or basic-language milestone complete.

## Readonly record field correction

Record fields are immutable bindings. Direct and supported compound assignment,
including parenthesized and nested targets, must be rejected even through a
`mut` record binding. Whole-record rebinding remains valid, and Array values
held in fields retain the normal capability rules for indexing, method calls
and mutable arguments. Field immutability does not recursively freeze values.
Mutation syntax follows a binding through field/index projections; fresh Array
values may be passed to mutable parameters but cannot be assigned to or pushed
to directly. Grouping preserves the same binding requirement.

[Issue #350](https://github.com/type-rb/type-rb-native/issues/350) tracks the
checked-frontend correction and its ordinary file/REPL and recovery regressions.
The existing scalar Float fixture now rebinds the whole record to comply with
the reference rule. Ordinary named record Arrays are accepted through PR #352;
the recovery, seed handoff and subsequent MIR self-use are tracked in
[issue #349](https://github.com/type-rb/type-rb-native/issues/349).

## Coverage is path-specific

The [generated case matrix](native-language-coverage-matrix.md), generated family
inventory and the [Capabilities detail view](capabilities/README.md) use
[`tools/native-language-cases.json`](../tools/native-language-cases.json).
Each row describes one bounded example, not full support for a feature or a
percentage of the TypeRB language. The exact reference revision, executable
hashes and registry hash are recorded with observations.

The registry maps every concrete statement/expression node in the pinned
reference AST to a family. The oracle job checks the AST hash and scans all
non-test Go files in its directory for unclassified syntax nodes. This detects
syntax-inventory drift; it does not prove that every grammar combination,
method, type rule or boundary case has been tested. Families therefore also
record uncovered semantic contracts. Review those against public reference
language and standard-library documentation when expanding or changing the pin.

Both compilers execute the same authored sources, including project/import
fixtures. Each implementation has separate reviewed expectations for ordinary
check, build, execution and REPL. Positive cases, static rejection cases and
runtime failures are all intentional. Native acceptance of reference-invalid
record, Array or Hash equality is a bug, not extra support. Some reference REPL
submissions also fail despite successful ordinary execution; those limitations
are visible separately and must not be attributed only to Native.

A rejected REPL submission may leave the interactive session at exit status
zero. Output and diagnostics determine the result, not exit status alone.
UTF-8 literals, code-point size/index, concatenation/interpolation and managed
collection storage now pass ordinary build, execution and REPL checks. Unicode
escapes and additional String APIs remain explicit gaps.
The while probe produces the same final value but lacks the reference's `[mut]`
REPL display. These remain explicit differences. Snapshot/recovery coverage
cannot establish ordinary check/build/run/REPL support.

The regression command checks each implementation against its reviewed outcomes.
It can pass with known gaps; its `parityGaps` field summarizes differences between
those reviewed expectations, and `uncoveredContracts` identifies untested basic
contracts. `--require-parity` additionally rejects both known differences and
untested basic contracts. It requires both compilers, the reference AST and the
complete registry, and is intentionally failing until basic parity is achieved.
Neither mode infers full language coverage from the number of passing examples.

Frontend diagnostic wording is checked exactly for each implementation but need
not match between compilers. Matching rejection does not establish diagnostic
parity. [Issue #455](https://github.com/type-rb/type-rb-native/issues/455) tracks
message detail, real source columns and terminal presentation separately.
The String repetition case preserves the current second-line REPL origin;
dedicated diagnostic tests cover both compact and spaced input.
Runtime-failure fixtures may check the exact first
stderr line, status and stdout, omitting unstable reference panic stack frames.
Invalid UTF-8 output retains normalized raw bytes alongside an escaped display;
it cannot silently compare equal to valid text. Process timeouts always fail.

### Reproducing and maintaining the inventory

```sh
python3 tools/native-language-coverage-test.py
python3 tools/native-language-coverage.py --native /absolute/path/to/trbn --jobs 2
python3 tools/native-language-coverage.py --reference /absolute/path/to/trb \
  --reference-ast /path/to/pinned-reference/internal/ast/ast.go --jobs 2
python3 tools/native-language-coverage.py --native /absolute/path/to/trbn \
  --reference /absolute/path/to/trb \
  --reference-ast /path/to/pinned-reference/internal/ast/ast.go --require-parity
```

Build the reference executable from `TYPE_RB_REVISION`. CI verifies every
reviewed reference outcome in the quick oracle job. Native CLI jobs exercise
the same cases without invoking a reference compiler. Reports are short-lived
CI artifacts; do not add raw observations to `results/`. The suite is a
correctness contract, not a performance benchmark. Each subprocess has a
30-second timeout with owned-process-group cleanup; `--jobs` bounds concurrent
isolated cases and leaves reporting order deterministic.

Use `--case ID` for a focused probe and `--observe` to inspect changed Native
behavior. Observation still checks reference expectations and process failures;
it never rewrites expectations. Review all four paths before accepting a change.
Then regenerate all public views from that same reviewed registry:

```sh
python3 tools/native-language-coverage.py --table > docs/native-language-coverage-matrix.md
python3 tools/native-language-coverage.py --feature-table > docs/native-language-feature-inventory.md
python3 tools/native-language-coverage.py --pages-data > docs/capabilities/ordinary-language.js
```

CI checks exact generated contents with `--check-table`, `--check-feature-table`
and `--check-pages-data`. Review the related broad `capabilities/catalog.js`
entries when behavior changes, preserving their stated scope and separating
snapshot evidence from ordinary support. A Pages capability update needs no
formal benchmark rerun when runtime benchmark evidence has not changed.

## Feature delivery contract

Work within the active milestone and record exact reference/Native identities,
semantics and coverage in each cohesive PR. Register new semantic scope or material
experiments when needed; routine ownership moves do not need individual budgets.
Then deliver parser/checker behavior, checked/MIR representation and validation,
mechanical lowering, CLI/REPL coverage, and reference differential tests.
Preserve source diagnostics, evaluation order, branch-local bindings, portable
failures and managed-root lifetimes. Do not add semantic analysis to QBE text.

For `break` and `next`, explicitly validate loop targets, nested control flow,
backedges, induction updates and root cleanup. Existing bounds/header proofs
must account for each new path; unproved cases retain their checks. General
control-flow MIR need not be completed before the feature, but the affected
semantic ownership and verifier cannot be skipped.

After feature acceptance, follow the [seed update boundary](bootstrap-seed-updates.md)
before using the syntax in compiler implementation source. Add the matching
snapshot recovery coverage when that source begins using it. Then remove the
actual flags, nesting or representation workaround that motivated the feature.
Do not count a parser-only change or a source rewrite without bootstrap tests
as completion. Keep each feature and its self-use adoption independently clear.

## Statement conditional chains

The ordinary compiler and REPL accept ordered `if` / `elsif` chains with an
optional `else`. Every condition must be Boolean, including conditions in a
branch that will not execute. Conditions run in order and stop at the first
match; later effects and failures are skipped. Each branch has its own local
bindings. Nested chains, early returns, managed values, and Array mutation are
covered by `elsif-control` and `elsif-managed` conformance cases, with malformed
chains, scope errors, required traps, and invalidated loop bounds as controls.

This extends the existing checked conditional path. Functions outside the
current complete MIR subset retain direct lowering and their runtime checks;
conditional edges do not introduce new loop-induction or header-stability
proofs. Subsequent [value controls](decisions/0041-value-control-mir.md) and
[nullable MIR](decisions/0042-nullable-mir.md) extend the ordinary expression family.
Compiler implementation source now uses `elsif` in the statement-dispatch chain of `parse_statement_block`, replacing six nested
`else` / `if` wrappers.
This adoption follows the verified Sep8 seed handoff and matching snapshot
recovery coverage. Existing statement conditions, cursor updates, diagnostics
and application output remain unchanged; other parser and checker nesting
remains eligible for separately verified cleanup.

## Ordinary loop transfers

Bare `break` exits the nearest enclosing loop. For `while`, bare `next`
transfers to its header and reevaluates the condition, including its effects;
for Array iteration, it advances the cursor before the next live-length check.
Nested loops own their transfers, while `return` still exits the function. Every statement is
checked, including unreachable transfers. Transfers outside a loop and transfer
values are rejected. Existing contextual `next` bindings remain supported.
Use an ordinary `if` guard in this subset: postfix conditional transfers remain
unsupported. The REPL currently reports incomplete
input for a postfix `break if` submission; it does not execute that submission.

The checker stores the kind and nearest-loop target at the exact statement
origin. A named `MirLoopTransfer` plan verifies origin, kind, token bounds and
nearest target before the code generator or REPL may consume it. Missing,
malformed or cross-loop plans fail closed. Transfers invalidate complete scalar
induction plans, Array-region/header proofs and dependent nonnegative facts;
unproved accesses retain runtime checks. Backedges enter the existing loop
header and its root-compaction boundary; exits retain the loop cleanup path.

`loop-transfer-control`, `loop-transfer-effects` and `loop-transfer-managed`
cover nested targets, skipped updates and traps, condition effects, branch
termination and managed values surviving automatic collection. Negative cases
retain required index/range failures and reject illegal targets and values.
Recovered compilers and ordinary replacement generations exercise these
sources, separately from snapshot support for those source programs.
After loop-transfer snapshot recovery and the verified seed handoff,
`parse_statement_block` uses bare `break` exits instead of a completion flag.
Its dispatch, cursor updates, diagnostics and final result remain unchanged.
The checked block dispatcher also uses bare `break` for terminal tokens, block
tails and diagnostic exits, with `elsif` for statement selection. Its while
checking has an independent helper; current MIR admission and diagnostics remain
unchanged. Other completion flags and `next` self-use remain separate cleanup
opportunities.
Track the full delivery in [issue #334](https://github.com/type-rb/type-rb-native/issues/334).

## Boolean arrays

The ordinary compiler and REPL accept `Array<Boolean>` literals, explicitly
typed empty arrays, indexing, indexed assignment, `push`, `size`, and function
and record carriers. Nested arrays have the same three-level bound as existing
scalar arrays. Negative indexes retain the reference behavior: `-1` addresses
the final element, while indexes outside either end fail. Boolean elements do
not coerce to Integer; existing homogeneous typing, mutable-array invariance
and readonly capabilities apply.

`boolean-array-values`, `boolean-array-effects` and `boolean-array-managed`
cover shared and nested aliases, typed empty arrays, left-to-right evaluation,
growth and arrays surviving automatic collection. Invalid cases reject wrong
element/index types and mutation capabilities; runtime cases retain required
bounds failures. The ordinary coverage row includes REPL value display.

Boolean arrays use the shared scalar-element runtime storage; nested arrays
retain managed-element descriptors and roots. They remain outside the complete
scalar/numeric-reduction MIR type set, with explicit checked/MIR boundary tests,
and retain the existing verified header and checked-access paths. This does not
add numeric reduction permissions or a target-specific Boolean representation.

Snapshot v4 recovery preserves Boolean element types through construction,
reads, writes, growth, nested arrays, record fields and closure captures. The
recovery QBE adapter explicitly widens Boolean values to the shared 8-byte
Array storage and narrows loads to the Boolean scalar ABI. MIR verification
rejects Integer elements, Boolean indices and mismatched Array receivers.
The `boolean-array-recovery` fixture checks RHS reallocation and retained
negative-index positions through snapshot execution and compiler generations.
The separate `fixtures/recovery/programs/boolean-array-closure` case retains
record/closure capture coverage within snapshot recovery; it does not claim
ordinary alias or closure support. Focused runtime tests retain nested arrays
across explicit collection.

After the verified Boolean Array seed handoff, compiler implementation uses
`Array<Boolean>` for the shared `scalar_inline_range_failure_used` and
`array_bounds_failure_used` flags. Their initial values, writes and tests use
Boolean values directly. Other Integer arrays that carry counters or multiple
states retain their existing types. This is typed internal self-use, with
unchanged application QBE and required failure paths, not a runtime speedup.
Track this delivery in
[issue #341](https://github.com/type-rb/type-rb-native/issues/341).

## Named record Arrays

The ordinary subset accepts homogeneous `Array<Entry>` for a visible named
record, with the same three-level nesting bound as scalar Arrays. Typed empty
arrays, inference, read/write, `push`, `size`, function signatures and record
fields preserve canonical declaration identity, including imported aliases.
Identical field shapes do not make distinct records interchangeable. Mixed
record literals can infer union Arrays in the reference; that broader union
subset remains unsupported here.

The `record-array-values`, `record-array-effects` and `record-array-managed`
cases exercise aliases, nested arrays, retained assignment positions across
RHS growth and managed record contents surviving automatic collection.
Diagnostics retain exact element types, bounds and mutation capabilities;
readonly fields remain protected even after indexing a mutable Array.
Record Array parameters remain outside numeric reduction MIR, and elements
use the existing managed aggregate storage and tracing paths.

Snapshot v4 recovery also preserves record Array element identities through
construction, reads, writes, growth, nested Arrays, function returns and closure
captures. Layout analysis boxes a record used as an Array element throughout the
module, including scalar-only records, so an Array never retains its stack
address. Existing managed descriptors and roots trace both the record and its
String or Array fields. Scalar records outside Array storage keep their existing
layout; tagged and Float Array elements remain outside this recovery subset.

The `record-array-recovery` fixture covers retained assignment positions across
RHS growth, three-level nesting and managed records surviving allocation loops.
The separate `record-array-closure` snapshot fixture exercises closure captures
and escaping record Arrays; it does not expand ordinary closure support.
Recursive record Array definitions preserve nominal identity, and the ordinary
recovery fixture retains a self-cycle through allocation pressure while
creating unreachable cycles. Focused
MIR tests reject scalar and nominal element mismatches, invalid indices and
receiver types. A returned-record runtime test checks exact Integer values after
subsequent calls, Array mutation and explicit collection, plus managed children.
Removing the scalar-record boxing makes that lifetime regression test fail.

After the [verified record Array seed handoff](bootstrap-seed-updates.md#current-verified-checkout-seed)
was accepted in PR #356, compiler implementation adopts `Array<MirValue>`
for `MirModule.values` and `CheckedLocals.mir_value_rows`. The named fields
are `function_id`, `id`, `type_id`, `source_id` and `line`; construction, lookup
and verification share that exact carrier. The wrong tuple length is no longer
representable. Identity, type range, origins, uniqueness and definition-count
checks remain, and malformed-value tests replace complete readonly records.
This is the bounded self-use slice in
[issue #349](https://github.com/type-rb/type-rb-native/issues/349).
Other MIR row families and deferred optimization remain separate.

## Retired Array-loop integration branch

[PR #307](https://github.com/type-rb/type-rb-native/pull/307) is closed and
superseded by the [MIR consolidation milestone](mir-consolidation.md).
Its frozen head `96871cce7bf8bcd39717cb2b1af992cebfdb8dcd` preserves the
[implementation and adoption review](https://github.com/type-rb/type-rb-native/blob/96871cce7bf8bcd39717cb2b1af992cebfdb8dcd/docs/native-mir-loop-bounds-adoption.md)
and all historical failed measurements. It is not an accepted optimization.

The independent bounded QBE output batching and byte-preservation tests are
ported to current source, together with valid nested/negative-index and failing
overflow/short-output conformance cases. This does not omit Array bounds checks
or claim a measured application speedup.

[Issue #303](https://github.com/type-rb/type-rb-native/issues/303) retains the
useful dominating-guard, binding-version and Array-identity proof work under
the current milestone. Adapt it to shared verified MIR and current effects;
do not reinstate the old six-cell projection over the newer loop-local header,
iteration, assignment and lifetime owners. Retain producer/verifier adversarial
controls when reconnecting the proof. Old numeric investigation budgets are
historical, not current integration authority.

## Checkpoint reporting

Report the ordinary coverage cases added, remaining gaps, compiler-source
cleanup enabled, MIR invariants verified, bootstrap/recovery status and measured
costs separately. Update the corresponding issue and this coverage record when
a feature passes; keep planned work distinct from accepted behavior. Publish
Pages coverage at accepted checkpoints without rerunning the formal runtime
benchmarks unless accepted runtime evidence has actually changed.

## Ordinary Array iteration

PR #418 accepted the ordinary implementation at
`508f721f8964d67a5893e547d2e2fb3de5b20a63`; PR #423 accepted matching recovery
and seed observers at `d2980f14d1b64e5ce3544dd7133e7f5871644e4e`. Both complete
CI cohorts pass ordinary limits. The [verified seed handoff](bootstrap-seed-updates.md#current-verified-checkout-seed)
records preparation, immutable publication and fresh actual-asset verification.
The subsequent compiler-source adoption uses the verified checkout seed and
accepted-source amd64 bridge for the three read-only traversals below.

The current slice supports statement `Array#each` and `Array#each.with_index`,
with optional empty call parentheses, `do |value[, index]| ... end`, and
single-line brace blocks. Brace statements may be separated by semicolons;
multiline brace blocks are explicitly rejected for now. Block parameters have
the reference's mutable local bindings and lexical shadowing. The receiver is
evaluated once; each step reloads its current length and storage, so `push`
and replacement of a future element are observed. Rebinding the source local
does not retarget an active iteration. `next` advances the internal cursor,
`break` exits the nearest loop, and `return` exits the enclosing function.

The structured `MirIteration` operation connects receiver and element types,
source/body boundaries, and nearest-loop ownership. Ordinary code generation
and the REPL consume the same checked plan. Emission roots both the retained
Array and the current managed element across body allocation, and keeps hidden
local slots aligned with MIR identities used by nested loop-header placement.
The shared shape and checked-plan accessors live in `iteration_checked.trb`;
the compiler, recursive checker and REPL import this single proof owner.
Sparse origin maps share the same absent-entry read with Hash and Array
assignment plans. Existing runtime and compiler performance checks still apply.

The matching reference pin and maintained snapshot-v4 fixtures cover authored
Array iteration through existing recovery operations, including forced and
automatic collection. Float Arrays, Range/Iterable, batches, and value-producing
iteration remain outside the snapshot subset. Compiler source uses `each` for
checked Hash-plan verification and project-key membership, and `each.with_index`
for MIR function lookup. These read-only traversals preserve early return,
first-match ordering, empty/missing behavior and exact String equality.
Range/Iterable, batch iteration, expression-position iteration,
and the remaining Array APIs stay tracked in issue #410. The current Array API
has no removal operation; the live-header implementation does not establish
conformance for a future shrinking operation.

Compiler recovery metadata uses a separate 48 MiB input bound. The managed
Array MIR compiler produces approximately 43.1 MB of recovery JSON, exceeding
the previous 40 MiB boundary. The earlier complete Array iteration snapshot was
34,616,510 bytes and required increasing the original 32 MiB bound to 40 MiB.
These are verbose recovery inputs, not application or shipped compiler binaries.
The ordinary 4 MiB snapshot entry and schema/type/instruction bounds remain
unchanged. Failed smaller-bound recovery attempts remain validation evidence;
a larger decode budget alone does not establish successful recovery.
