# Ordinary Native language coverage

Status: an initial 15-case ordinary-path inventory and regression contract are
available. Statement `elsif` and bare `break` / `next` in `while` are covered by ordinary
compiler and REPL regressions. The ordinary Boolean-array case is also covered.
The inventory remains a bounded set of examples, not complete language support.
Track the first bounded delivery in [issue #326](https://github.com/type-rb/type-rb-native/issues/326).

## Current development priority

The ordinary compiler is self-hosted but implements a bounded TypeRB subset.
Prioritize existing language features that make ordinary programs and the
compiler implementation clearer, without waiting for complete MIR migration
or Pure Go runtime parity. TypeRB at `TYPE_RB_REVISION` remains the semantic
authority; this work does not define a Native-only dialect.

The near-term order is:

1. Wrong results, crashes, unsafe optimization and reference-semantic mismatches.
2. Ordinary-path coverage probes and the basic control syntax: `elsif`, then
   `break` and `next`, with necessary MIR validation in the same feature slice.
3. Needed collection and value representations, selected from concrete compiler
   or application uses. Evaluate Boolean arrays and named typed data before
   extending positional Integer rows merely to work around a missing type.
4. Arguments, nullable values, enums and Result according to actual use and
   prerequisites, not a requirement to finish every feature in one category.
   Evaluate UTF-8 literal output separately from a complete Unicode API.

Existing performance, memory, process and reproducibility checks remain in
force. New benchmark-specific tuning and broad optimizer work are secondary
while these basic language boundaries are being established. Performance goals
remain unchanged; a feature is not required to manufacture a runtime speedup
to justify its existence. A failed cost bound still needs the existing
[trade-off review](optimization-tradeoffs.md), not automatic relaxation.

## Readonly record field correction

Record fields are immutable bindings. Direct and supported compound assignment,
including parenthesized and nested targets, must be rejected even through a
`mut` record binding. Whole-record rebinding remains valid, and Array values
held in fields retain the normal capability rules for indexing, method calls
and mutable arguments. Field immutability does not recursively freeze values.

[Issue #350](https://github.com/type-rb/type-rb-native/issues/350) tracks the
checked-frontend correction and its ordinary file/REPL and recovery regressions.
The existing scalar Float fixture now rebinds the whole record to comply with
the reference rule. Ordinary named record Arrays are accepted through PR #352; the remaining
recovery, seed and MIR self-use work is tracked in
[issue #349](https://github.com/type-rb/type-rb-native/issues/349).

## Coverage is path-specific

The [generated case matrix](native-language-coverage-matrix.md) comes from
[`tools/native-language-cases.json`](../tools/native-language-cases.json).
Each row describes one bounded example, not complete support for that feature
or a percentage of the TypeRB language. The exact reference revision is pinned
in `TYPE_RB_REVISION` and recorded alongside executable and registry hashes in
each observation report.

The `while` case currently returns the same final value but differs in its
REPL value display (`[mut]` is absent after the loop). This remains an explicit
output difference. A rejected REPL submission can still leave the interactive
session with exit status zero; output and diagnostics, not just exit status,
determine the row. UTF-8 String literals pass `check` but fail ordinary build
and REPL emission. Historical snapshot support does not close that gap.

Maintain one small executable case registry and derive its ordinary coverage
table from checked expectations. Each row needs a feature, authored source,
reference revision, expected output/diagnostic, and separate observations for:

- ordinary `check`;
- ordinary build and execution (a successful build alone is not execution);
- the ordinary REPL, including declaration and expression behavior where relevant.

Report verified, rejected, inconsistent or not yet tested for the exact case,
not for an entire language category. Capture exit status and stdout/stderr;
fail the regression when an observation changes unexpectedly. A known rejection
is a tracked gap, not a passing conformance claim. Unsupported reference input
cannot establish a Native language gap. Check the reference before registering
a fixture as valid.

Keep snapshot/recovery coverage separate. Earlier aggregate/UTF-8/closure
evidence does not establish ordinary `trbn` support. A `check` success followed
by a build rejection must be visible rather than collapsed to "supported".
The first inventory covers scalar/control successes and the reported gaps:
`elsif`, `break`, `next`, default arguments, Boolean arrays, nullable Strings,
ordinary enums and UTF-8 String literals. It is not an exhaustive specification.

### Reproducing and maintaining the inventory

```sh
python3 tools/native-language-coverage-test.py
python3 tools/native-language-coverage.py --native /absolute/path/to/trbn
python3 tools/native-language-coverage.py --reference /absolute/path/to/trb
python3 tools/native-language-coverage.py --check-table docs/native-language-coverage-matrix.md
```

The reference executable must be built from `TYPE_RB_REVISION`. CI validates
every fixture with that compiler in the quick oracle job. Ordinary Native CLI
jobs independently exercise the same cases without invoking a reference
compiler. Reports are short-lived CI artifacts; do not add raw observations
to `results/`. Changing this registry routes to the quick and CLI checks, not
an unchanged compiler's performance matrices.

Use `--case ID` for a bounded probe and `--observe` to inspect changed Native
behavior before reviewing expectations. Observation mode still rejects an
invalid reference fixture and never rewrites expectations. Update a case only
after reviewing all four paths, then regenerate the table with `--table`.
Documentation-only CI checks that the table matches the registry without
building or executing a compiler. Each subprocess has a 30-second safety
timeout with owned-process-group cleanup; these are not performance tests.

## Feature delivery contract

For each bounded slice, register the exact reference and Native baseline,
semantics, coverage cases and existing cost authorities before implementation.
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
proofs. This does not add conditional expressions or nullable narrowing.
Compiler implementation source now uses `elsif` in the statement-dispatch chain of `parse_statement_block`, replacing six nested
`else` / `if` wrappers.
This adoption follows the verified Sep8 seed handoff and matching snapshot
recovery coverage. Existing statement conditions, cursor updates, diagnostics
and application output remain unchanged; other parser and checker nesting
remains eligible for separately verified cleanup.

## Ordinary loop transfers

Bare `break` exits the nearest enclosing `while`; bare `next` transfers to its
header and reevaluates the condition, including its effects. Nested loops own
their transfers, while `return` still exits the function. Every statement is
checked, including unreachable transfers. Transfers outside a loop and transfer
values are rejected. Existing contextual `next` bindings remain supported.
Use an ordinary `if` guard in this subset: postfix conditional transfers and
iteration blocks remain unsupported. The REPL currently reports incomplete
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
Other completion flags and `next` self-use remain separate cleanup opportunities.
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
The separate `fixtures/gate3/programs/boolean-array-closure` case retains
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

Compiler implementation has not adopted record Arrays. The
[bounded delivery](https://github.com/type-rb/type-rb-native/issues/349) still
requires verified published bootstrap assets and an accepted checkout handoff
before replacing the five-position MIR value carrier with a named record.
Other MIR row families and deferred optimization remain separate.

## Deferred Array-loop candidate

[PR #307](https://github.com/type-rb/type-rb-native/pull/307) and
[issue #303](https://github.com/type-rb/type-rb-native/issues/303) are deferred,
not accepted or abandoned. Freeze the current candidate at
`96871cce7bf8bcd39717cb2b1af992cebfdb8dcd`; retain its
[adoption review](https://github.com/type-rb/type-rb-native/blob/96871cce7bf8bcd39717cb2b1af992cebfdb8dcd/docs/native-mir-loop-bounds-adoption.md),
failed cost observations and frozen cumulative baseline. Start basic syntax
work from accepted main, not from that unaccepted optimization branch.

Reassess after the first ordinary coverage/control-syntax checkpoint, or when a
concrete representation change can reduce its maintenance or measured cost.
Its merge is not a prerequisite for language coverage. Do not automatically
renew expired measurement budgets, rerun known unchanged failures, relabel the
small gain as a passing earlier criterion, or change Pages performance values.
Any renewed adoption proposal still needs current costs, benefit uncertainty,
explicit policy and all remaining correctness/target/memory authorities.

## Checkpoint reporting

Report the ordinary coverage cases added, remaining gaps, compiler-source
cleanup enabled, MIR invariants verified, bootstrap/recovery status and measured
costs separately. Update the corresponding issue and this coverage record when
a feature passes; keep planned work distinct from accepted behavior. Publish
Pages coverage at accepted checkpoints without rerunning the formal runtime
benchmarks unless accepted runtime evidence has actually changed.
