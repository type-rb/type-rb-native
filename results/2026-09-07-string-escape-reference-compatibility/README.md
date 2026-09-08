# Current reference compatibility

The current development pin is TypeRB `0.4.6-dev` at
`202cea85e8ceffd91cfc3ceb69d6f4d8a7acfd7b`, the merged
[Boolean Array snapshot extension](https://github.com/type-rb/type-rb/pull/660).
Snapshot v4 retains exact Boolean element types through construction, reads,
writes, push, nested arrays, records and captures, without adding operations
or changing the schema. The existing stable Array-assignment behavior from
[PR #659](https://github.com/type-rb/type-rb/pull/659) remains: capture and validate
the receiver/index/position before the RHS, then check current storage at write.

The current accepted ordinary implementation is Native
`57cb41ad6be91716e31fa555ed8ea8c8ce7a5f51` from
[PR #345](https://github.com/type-rb/type-rb-native/pull/345). All 17 selected
checks passed at `06aedd81c291d732fe74afc88a9e131d3608765a` in
[run 34213179434](https://github.com/type-rb/type-rb-native/actions/runs/34213179434).
Hosted worker sizes are 349,296 Darwin arm64 and 325,864 Linux arm64 bytes,
675,160 combined. Local full recovery-enabled suites passed root 97/97 and
compiler 130/130, alongside 348 deterministic check/QBE observations, both
14-case language registries and ordinary CLI/REPL/automatic-GC checks.

Boolean Array snapshot recovery and its seed preparation observers are accepted
at Native `e99df93e81c36c765ead99526fe58b2c2a978ced` from
[PR #346](https://github.com/type-rb/type-rb-native/pull/346). All 17 checks passed
at `d33ec5e55362ef1ac3c685de8c536bc3cf01f6ff` in
[run 34215915536](https://github.com/type-rb/type-rb-native/actions/runs/34215915536).
Corrected local full suites passed root 99/99 and compiler 130/130; all 351
check/QBE observations passed. A fixture initially mixed snapshot-supported
alias/closure syntax with ordinary coverage. The shared case now uses supported
named functions, while a separate snapshot case retains closure coverage.
The original failed observation remains separate from the corrected cohort.
The ordinary compiler source and local binary are unchanged from PR #345.

The [verified Boolean Array seed handoff](../../docs/bootstrap-seed-updates.md#current-verified-checkout-seed)
records immutable assets, exact source and successful fresh published-asset
verification. The checkout handoff is accepted at
`65ab856abe55b4816ec6cc8e7e4cc91ce98293bd` from
[PR #347](https://github.com/type-rb/type-rb-native/pull/347). All 17 checks passed
at `c6b98d25483d766c09e5695a8c315e210f1111de` in
[run 34219868383](https://github.com/type-rb/type-rb-native/actions/runs/34219868383),
including the separate Linux amd64 Boolean-capability setup bridge.

The bounded Boolean flag self-use is accepted at
`4a594bc6562262502b6f901cae63c5288a705f5b` from
[PR #348](https://github.com/type-rb/type-rb-native/pull/348). All 17 selected
checks passed at `62860e4d45691aff6d5002db9715d150042eabbb` in
[run 34222798465](https://github.com/type-rb/type-rb-native/actions/runs/34222798465).
Both failure-flag carriers use Boolean elements; local enabled suites passed
root 99/99 and compiler 130/130, with unchanged application QBE observations.

The current [readonly-field repair](https://github.com/type-rb/type-rb-native/issues/350)
starts from that accepted implementation. Field-binding assignment rejection
belongs to the checked frontend, while Array contents retain their existing
mutation capability. Direct calls of scalar fields remain rejected. The pinned
reference already rejects field assignments; its `check` currently misses the
separate `(box.value)()` scalar-field call error, which its Go backend rejects.
That probe is a preserved Native diagnostic, not a claim of equal reference
check output.

The initial local enabled cohort passed compiler 131/131 but failed one of
99 root tests: the old `float-scalars` valid fixture assigned to a readonly
record field. The ordinary CLI also retained that obsolete expectation. The
fixture now rebinds the complete record, and REPL coverage checks both rejected
field replacement and valid complete rebinding. Those original failures remain
separate from the corrected-source cohort. All 378 corrected deterministic
check/QBE observations and the complete ordinary CLI/REPL/terminal suite pass.
Full corrected enabled suites and all exact-head hosted authorities are still
required before acceptance.

No runtime-performance or Pure Go claim, benchmark-value update, seed change
or acceptance-budget change is made. The cumulative baseline remains
`ac633935a7f248470c59d22666da14c819a131fa`.

The accepted assignment prerequisite is Native
`1baf5ad2cb6cc2bd6158c20f837a3479bfa3360d` from
[PR #343](https://github.com/type-rb/type-rb-native/pull/343). All 17 selected
checks passed at `ea58fd0391d4a252d26acf3ee284ad908b8c68f5` in
[run 34209892000](https://github.com/type-rb/type-rb-native/actions/runs/34209892000)
after the separately accepted budget [PR #344](https://github.com/type-rb/type-rb-native/pull/344).
Its worker sizes are 349,296 Darwin arm64 and 325,600 Linux arm64 bytes,
674,896 combined. Its Linux compiler comparison reports 313,248 baseline and
325,608 candidate bytes (1.039458), build median ratio 1.010417 and RSS ratio
1.000413. All original failures below retain their source-era status. The
cumulative implementation baseline remains
`ac633935a7f248470c59d22666da14c819a131fa`; acceptance does not establish a
Pure Go speedup.

Earlier assignment-repair observations follow.
Local ordinary Integer, Float, nested-owner and managed String assignment
cases match the selected reference, including actual RHS growth and an
initial bounds failure that skips RHS effects. The managed case records five
automatic collections and zero live bytes after final collection. The formerly
crashing Integer growth probe succeeds under GuardMalloc. The pinned published
seed builds the current core and CLI fixed points; ordinary CLI and REPL tests
passed with those cases. Its complete acceptance is recorded above.

Compiler recovery authoring failures are retained separately: an unsynchronized
exact import prefix, a helper initially placed after the required empty driver,
and logical expressions outside snapshot v4's supported source subset. The
candidate uses the existing statement forms and preserves the exact recovery
boundaries. Earlier tests that counted only initial bounds checks now account
for the independent final store check; their induction and inline-budget
assertions remain in place. No cost limit or failed measurement was waived.

## First assignment candidate and bounded carrier cleanup

The first full cohort for Native
`90435186fc5c06b662c06cb80584575e28d9d064` is
[run 34199705462](https://github.com/type-rb/type-rb-native/actions/runs/34199705462).
Recovery, both ordinary CLI targets, Darwin worker memory and the Linux amd64
target passed. Linux arm64 failed its unchanged 317,000-byte compiler ceiling:
the target chain reports 326,312 bytes, and the worker's stripped compiler
reports 326,304 bytes. The combined and performance authorities therefore did
not run; this candidate was not accepted. Keep that cohort and its failures.

The first bounded follow-up removes emitter-only mutability transport, whose
checks already belong to the checked frontend, and removes the redundant
Array-position carrier field. A tagged slot represents a binding address or
a validated Array position beside its owner. All internal callers change
directly. Required bounds, owner/old-value roots and target/store verification
remain. This is one revised-source correctness and cost cohort, not an
unchanged-head retry or a larger acceptance budget. Reassess any remaining
cost miss before another size-only attempt.

## Compact candidate and accepted budget decision

The compact source `885414012e0aa891d1af99f30069e60da300a6cb` completed
[run 34202210192](https://github.com/type-rb/type-rb-native/actions/runs/34202210192).
Recovery, both CLI targets, Darwin worker memory and Linux amd64 passed.
Linux worker size was 325,600 bytes; the Linux target chain was 325,608 bytes.
Both failed the source-era 317,000-byte ceiling. Combined, target-neutral
comparison and performance authorities were skipped, and acceptance failed.
This cohort and the earlier failure remain failures.

The [complete local diagnostic observations](array-assignment-diagnostic.csv)
include both warmups and all retained rounds; their
[identities and method](array-assignment-diagnostic-identities.json) distinguish
cumulative baseline, same-feature control and compact candidate. All 216
observations retained expected outputs and reproducible artifacts. A sandbox
restriction prevented the first timer invocation from reading `kern.clockrate`
before any valid observation; that stopped infrastructure record is separate
from this complete cohort. No failed performance sample was replaced.

[Decision 0029](../../docs/decisions/0029-array-assignment-compiler-budget.md)
records the cost assessment and accepted Linux 328,000 / combined 678,000-byte
budgets. [PR #344](https://github.com/type-rb/type-rb-native/pull/344) implements
that policy separately. Its compiler source is unchanged from cumulative
baseline `ac633935a7f248470c59d22666da14c819a131fa`; this budget revision does
not reset the cumulative comparison. The repair includes the policy for fresh
full validation and cannot merge before that policy is accepted and every
selected authority passes at the repair's exact head. Pages measurements and
all other acceptance requirements remain unchanged.

# Previous loop-transfer reference checkpoint

The current development pin is TypeRB `0.4.6-dev` at
`4e1327c9af1b4caec9963756e6ffbc0e2ef56341`, the merged
[loop-transfer snapshot update](https://github.com/type-rb/type-rb/pull/657).
Snapshot v3/v4 encode nearest-while transfers and early method returns with
existing jumps and live block arguments. The format and v2 boundary remain
unchanged. Both `elsif-recovery` and `loop-transfer-recovery` run through
snapshot encoding, strict program decoding, recovery QBE emission and execution.

The Native implementation is accepted
`4e1d0b4aee97b9a5bd73a98f918b31d47985da25` from PR #337.
[Exact-head acceptance](https://github.com/type-rb/type-rb-native/actions/runs/34166076931)
passed all selected recovery, ordinary CLI, target, memory and comparative-cost
authorities at the preceding reference pin. That is the implementation baseline,
not acceptance of this reference update. Fresh enabled suites and every
applicable hosted authority are required before merge. Seed registration is
separate from publication, actual published-asset verification and checkout pins.

The preceding pin was `f6229c5657a5acb40194cde71785a63754d00355` from
[TypeRB PR #655](https://github.com/type-rb/type-rb/pull/655).
Its [source-era compatibility record](https://github.com/type-rb/type-rb-native/blob/4e1d0b4aee97b9a5bd73a98f918b31d47985da25/results/2026-09-07-string-escape-reference-compatibility/README.md)
retains the earlier conditional and logical-condition checkpoint identities.

## Previous String-escape checkpoint

The preceding experimental update selected TypeRB `0.4.6-dev` at
`47a160cae05ddc2035c7430735c4762d36bbc9c4`, the source revision of
[TypeRB PR #651](https://github.com/type-rb/type-rb/pull/651).
The dependent Native update requires that reference PR to merge first.

Native implementation `07fc9af5e4d8b099865297820068140222ade47e` passed
[Native CLI workflow 34081476080](https://github.com/type-rb/type-rb-native/actions/runs/34081476080)
on Darwin arm64 and Linux arm64. Both jobs build from the unchanged pinned
Native seed, verify core and CLI fixed points, run CLI and typed REPL cases,
exercise escape and interpolation errors, render terminal editing and history,
and verify unchanged checkout inputs reuse the executable.

Local Darwin arm64 checks with the exact selected reference also pass:

- reference checks for the root, compiler and isolated CLI source projects;
- String escape and interpolation file/REPL differential tests;
- shared reference/Native REPL screen and history tests.

The implementation accepts escaped hashes in source while keeping JSON history
validation separate. The new reference requires typed filesystem paths and
immutable record fields; adapters construct `Path` values and CLI state uses
mutable Array elements or replacement session records.

This is bounded source, String and CLI compatibility evidence. It is not a
version range, complete language conformance claim or performance measurement.
Full recovery, target, memory and performance checks on the final PR revision
remain the required acceptance authorities. Published bootstrap assets and
previous measurement contracts retain their original revisions.

The [previous compatibility record](https://github.com/type-rb/type-rb-native/blob/5cf61c740aa600c34ed94f1b130ea2ffefd9e783/results/2026-08-31-typerb-0-4-4-compatibility-darwin-linux-arm64/README.md)
remains available at its exact archived revision.
