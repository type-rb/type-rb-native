# Current reference compatibility

The current development pin is TypeRB `0.4.6-dev` at
`6cbd4025545d44a1de211335f9197772077bb478`, the merged
[record Array snapshot extension](https://github.com/type-rb/type-rb/pull/663) and
[recursive record registration correction](https://github.com/type-rb/type-rb/pull/664).
It retains canonical record element identities through aliases, nesting,
function signatures and closure captures. Snapshot v4 remains data-only and
keeps the existing operations/schema. Boolean Array support from
[PR #660](https://github.com/type-rb/type-rb/pull/660) and stable assignment
positions from [PR #659](https://github.com/type-rb/type-rb/pull/659) remain.
The new pin also includes the independent scalar-field call diagnostic and
imported nominal-contract fixes in PRs #661 and #662. Earlier observations
below retain their original reference pin and outcomes.

The accepted Boolean Array ordinary implementation is Native
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

The [verified Boolean Array seed handoff](https://github.com/type-rb/type-rb-native/blob/db48f64f6c3f6ce3fb904b2d28c95fa46522ebfc/docs/bootstrap-seed-updates.md#current-verified-checkout-seed)
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

The [readonly-field repair](https://github.com/type-rb/type-rb-native/pull/351)
is accepted at `f1d65b96d659f68376c7ec937be98ef95e02a838`, with all 17 checks
passing at `2d917d2e8feed1e0054edfe8f9c9958cedcab0c7` in
[run 34232237613](https://github.com/type-rb/type-rb-native/actions/runs/34232237613).
Field-binding rejection belongs to the checked frontend, while Array contents
retain their mutation capability. Its source-era reference pin `202cea8`
missed `(box.value)()` during checking; the current pin includes that separate
checker repair. The original mismatch remains a source-era observation.

The initial local enabled cohort passed compiler 131/131 but failed one of
99 root tests: the old `float-scalars` valid fixture assigned to a readonly
record field. The ordinary CLI also retained that obsolete expectation. The
fixture now rebinds the complete record, and REPL coverage checks both rejected
field replacement and valid complete rebinding. Those original failures remain
separate from the corrected-source cohort. All 378 corrected deterministic
check/QBE observations and the complete ordinary CLI/REPL/terminal suite pass.
Corrected enabled suites passed root 99/99 and compiler 131/131; hosted
acceptance is recorded above.

The accepted ordinary named-record Array implementation in
[issue #349](https://github.com/type-rb/type-rb-native/issues/349) follows that
readonly correction. Three execution cases match the reference, covering
typed and inferred arrays, nested aliases, RHS growth and automatic collection.
Ten diagnostic fixtures retain nominal types and mutation capabilities; depth
four remains an explicit unsupported subset. Both runtime bounds cases retain
panic exit 2. Full ordinary CLI/REPL/terminal checks and 423 deterministic check/QBE
observations pass; existing cases match the readonly control. Imported record aliases
preserve identity; a same-named local record and an inferred imported record
remain distinct. The source-era `202cea8` reference incorrectly accepted that latter check
and then failed generated Go with a duplicate declaration. Preserve that
failed comparison; the current pin rejects the nominal contract mismatch and
does not claim broader same-name code-generation support. Different names with identical shapes are
rejected by both compilers.

The initial Darwin prototype is 365,768 bytes versus its 349,256-byte control.
Its text section grows from 259,136 to 260,804 bytes and crosses a 16 KiB
segment boundary. This exceeded the source-era 350,000-byte Darwin ceiling and remains
a failed cost observation. The source after the readonly prerequisite
also produces 365,768 bytes locally (text 260,964 bytes) and requires its
own complete target/cost cohort. The first hosted cohort failed Darwin worker
and managed-runtime size guards at 365,808 bytes; Linux worker size was 327,736.
The separate budget PR #353 is accepted at
`8dc08fbd8e18a4b161460ccf5c3a2c0aefd7f2ec`, with all 17 checks at
`3cb5e159beff9d802981885878f94545599ca604` in
[run 34238461767](https://github.com/type-rb/type-rb-native/actions/runs/34238461767).
Decision 0030 changes only Darwin/combined ceilings to 366,000/694,000 bytes;
relative and all other acceptance requirements remain unchanged. Ordinary
record Arrays are accepted at `566d00d67172460df0f57dff6d5fe03db3b67cdc` from
[PR #352](https://github.com/type-rb/type-rb-native/pull/352), after all 17
selected authorities passed at `9e8a6f6149323a87710b2be33f9b39e7b71077e7`.
The failed first cost attempt and bounded confirmation are retained below.
No compiler implementation uses record Arrays yet.

The accepted record Array recovery implementation pins the reference above.
Local recovery-enabled root 102/102 and compiler 133/133 tests pass, including
the ordinary recovery fixture and a separate escaping closure fixture.
The complete ordinary CLI/REPL/terminal suite and both 15-case language
registries pass. Focused MIR tests reject seven element/index/receiver errors;
the lifetime test retains exact record Integer values after two constructing
calls, nested aliases, mutation and explicit collection, and traces dynamic
String and Integer-Array fields owned by another returned record. Removing
scalar-record boxing fails the exact-value lifetime test. An earlier Boolean-only
oracle did not expose that invalid stack storage and was strengthened; both
observations are retained separately. The recovery changes no ordinary compiler
source; exact-head hosted acceptance and its retained first failure are recorded
below.

No runtime-performance or Pure Go claim, benchmark-value update or seed change
is made by this recovery update. The cumulative baseline remains
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

## Record Array diagnostic assessment

The [prospectively registered local cohort](https://github.com/type-rb/type-rb-native/pull/352#issuecomment-5586493243)
completed all [105 raw observations](record-array-cost-diagnostic.csv), including
two warmups and five retained rotating rounds. The [identities and all medians](record-array-cost-diagnostic.json)
retain source/compiler/application hashes, exact inputs, toolchain and hardware.
All outputs and repeated artifacts matched. The old cumulative compiler was
reclosed through equal same-basename generations after the newer seed's initial
output; the initial bootstrap binary was not treated as the frozen compiler.

Spectral-norm(5500) wall medians were 2.373460 / 2.385774 / 2.367373 seconds for
cumulative / accepted control / candidate, with 50,984-byte applications.
Compiler self-build medians were 1.596516 / 1.657213 / 1.660604 seconds; candidate
ratios are 1.040143 cumulative and 1.002047 incremental. Both selected applications
retain byte-identical control/candidate QBE and executables. This establishes
neither a runtime gain nor a new Go comparison.

The cohort also exposes a cumulative regression: n-body(1000000) runtime medians
are 0.273365 / 0.472791 / 0.476320 seconds, a candidate/cumulative ratio of
1.742429. The immediate control already has that difference. Its cumulative
build wall ratio 1.054824 also crosses the 1.05 alarm; coarse runtime CPU medians
are 0.10 / 0.30 / 0.30 seconds. These observations are retained as regression
alarms, not omitted or relabeled as passing results. Static QBE Array-address
call counts rise from 4 to 16 before this candidate; that is a follow-up lead,
not a proven attribution. [Issue #354](https://github.com/type-rb/type-rb-native/issues/354)
tracks that cumulative investigation. No diagnostic budget is renewed by this assessment.

Hosted cohort [34234062970](https://github.com/type-rb/type-rb-native/actions/runs/34234062970)
passed enabled recovery suites and CLI/target controls, then failed both Darwin
managed-runtime smoke and worker size guards at 365,808 bytes. Linux worker
size is 327,736 bytes; the 693,544-byte sum is arithmetic because combined and
comparative checks were skipped. The separate [budget decision](https://github.com/type-rb/type-rb-native/pull/353)
was subsequently accepted; this source-era failed cohort remains unchanged.

## Ordinary record Array hosted acceptance

[Run 34241831590](https://github.com/type-rb/type-rb-native/actions/runs/34241831590)
at `9e8a6f6149323a87710b2be33f9b39e7b71077e7` first failed Darwin self-build
wall ratio 1.053299 (1.970 / 2.075 seconds). Correctness, recovery, both CLI
and target controls, worker/combined size and memory, and Linux comparative
cost passed. The Darwin comparison exited before writing cross-target
identities; the downstream failure does not establish a code mismatch.

A [separately preregistered single confirmation](https://github.com/type-rb/type-rb-native/pull/352#issuecomment-5587645688)
kept the exact source, ordinary 1.05 limits, two warmups and seven retained
rounds. Attempt 2 passed all 17 authorities, including cross-target identity.
Darwin self-build medians were 2.560 / 2.420 seconds (0.945312). The additional
preregistered check pooled all 28 retained observations per role from both
attempts: medians 2.300 / 2.360 seconds, ratio 1.026087. Pooled peak RSS ratio
is 0.996429. The first failed attempt is preserved and the one-run confirmation
budget is expired.

The [complete two-attempt Darwin observations](record-array-hosted-confirmation.json)
include every warmup and retained measurement, source/compiler/toolchain
identities, measurement policy, environments and original comparisons. Linux
self-build ratio was 1.011364. Persistent-worker compiler sizes were 365,808
Darwin and 327,736 Linux, with the verified 693,544-byte combined total below
694,000. Comparative fixed-point filenames produce separately recorded sizes
of 365,768 and 327,744 bytes; do not substitute one observer's artifact identity
for another. This checkpoint supports ordinary incremental acceptance only.
The frozen cumulative cohort and n-body alarm above remain; no runtime speedup
or Pure Go comparison is inferred.

## Recursive record Array recovery correction

A self-referential `Node` with `children: Array<Node>` executes correctly in
both ordinary compilers, including a retained cycle and 20,000 discarded cycles,
but the first v4 producer rejected its Array element while `Node` was still
being registered. [TypeRB #664](https://github.com/type-rb/type-rb/pull/664)
registers the record kind before traversing fields and completes the same field
slice. Self-recursive and mutually recursive type graphs retain complete fields,
unique nominal definitions and deterministic snapshots. The exact accepted
reference is `6cbd4025545d44a1de211335f9197772077bb478`; full Go tests, source
formatting and [hosted validation](https://github.com/type-rb/type-rb/actions/runs/34249335045)
passed at `6f344860f35337126b20d2dad38f2754df67f0c7`.

The existing ordinary recovery fixture now retains a cycle across allocation
pressure and creates unreachable record/Array cycles. Ordinary execution and
a focused real v4 snapshot/decoder/MIR/QBE execution pass. The final enabled local suites passed 102 root and 133 compiler tests with
this stronger fixture and the exact accepted reference.
The earlier recovery candidate CI was cancelled for this correction after
CLI, target/QBE and worker/combined checks passed; its cancelled root suite
and unrun comparative checks establish no acceptance. That earlier candidate
did not publish a seed.


## Record Array recovery hosted acceptance

[PR #355](https://github.com/type-rb/type-rb-native/pull/355) was accepted at
`b8133a3df537d3d8af5531fbd235322d87519d3f` and merged as
`db48f64f6c3f6ce3fb904b2d28c95fa46522ebfc`. Its first
[hosted attempt](https://github.com/type-rb/type-rb-native/actions/runs/34250207907/attempts/1)
passed correctness, recovery, both CLI and target controls, worker/combined
size and memory, and Linux comparative cost (0.992424), but failed Darwin
self-build wall ratio 1.065539 (2.365 / 2.520 seconds). Baseline and candidate
Darwin compilers were byte-identical at 365,768 bytes, SHA-256
`a95b8758af7d45ccbd40100cf00e15f2783a381b66a253a21fe683c06968e9bd`.

A [separate single confirmation](https://github.com/type-rb/type-rb-native/pull/355#issuecomment-5588686720)
retained the exact candidate and baseline, commands, observations and ordinary
limits. Attempt 2 passed all 17 authorities; Darwin medians were 2.040 / 1.995
seconds (0.977941). The additional preregistered pool of all 28 retained
observations per role gave 2.185 / 2.215 seconds (1.013730), with RSS ratio
0.998611. The [complete two-attempt evidence](record-array-recovery-hosted-confirmation.json)
retains all 72 warmup/retained observations, identities, environments, policies
and original failures. QBE binaries were identical between roles within each
attempt; fresh builds on separate runners had different tool binary digests,
which remain recorded separately. The confirmation budget is exhausted and
expired. This accepts the recovery prerequisite without changing any ordinary
limit or renewing a runtime diagnostic.


## Record Array bootstrap handoff

The [current seed record](../../docs/bootstrap-seed-updates.md#current-verified-checkout-seed)
pins immutable `bootstrap-seed-2026-09-09-record-arrays` at accepted
`db48f64f6c3f6ce3fb904b2d28c95fa46522ebfc`. Preparation 34254120749 passed both
targets and all 28 retained observations; actual-published verification 34255257731
passed both targets, seed/B1/B2/B3/B4 equality, the corpus and all 42 retained
observations. All four published asset attestations bind to that accepted source
and hosted preparation workflow. Compiler sizes are 365,768 Darwin and 327,744
Linux bytes, 693,512 combined. Exact hashes and asset IDs remain in the linked
handoff record. Historical releases and their source-era bounds are unchanged.

Checkout core/CLI bootstrap and active CI consumers now select that exact seed.
The historical Linux amd64 setup also builds accepted record-capable 566d00d6
before candidate source; this setup-only bridge retains separate source,
compiler/QBE and process identities. Compiler implementation has not adopted
record Arrays yet. The subsequent five-field MIR value carrier migration followed this
accepted checkout handoff. Frozen benchmark baselines and the
cumulative n-body alarm are unchanged; no runtime/Pure Go gain is claimed.


## Named MIR value carrier self-use

The [registered slice](https://github.com/type-rb/type-rb-native/issues/349#issuecomment-5589325244)
follows accepted seed handoff `2f503f993ca93e5d50ad3151755fc739039d1bb5` (PR #356),
whose [exact-head validation](https://github.com/type-rb/type-rb-native/actions/runs/34256015371)
passed all 17 authorities. Only `Gate4MirModule.values` and local staging use
`Array<Gate4MirValue>`, with named function/value/type/source/line fields.
Construction, lookup and verification share that type; other MIR row families
and semantic pass ownership remain unchanged. Wrong tuple lengths become
unrepresentable, while identity, type range, origins, uniqueness and exact
value-definition checks remain. Two pre-migration characterization tests retain
those diagnostics, and existing Integer/Float malformed-MIR tests replace whole
readonly records.

The [local correctness record](mir-value-carrier-correctness.json) binds all six
changed source files to the same-feature control, compiler identities and 426
ordinary check/repeated-QBE observations. Every observation equals the control.
Spectral-norm (100) and n-body (1000) retain byte-identical QBE and executables
and the exact expected output. Fresh verified-seed core/CLI fixed points and
full CLI/REPL/terminal checks pass. Local compiler and CLI sizes remain 365,768
and 499,144 bytes respectively; their contents change as expected for the new
internal representation. Formatting and both source checks pass. Full enabled local recovery suites passed root 102/102 and compiler 135/135.
The owned recovery workspace was removed after terminal completion. Exact-head
hosted acceptance and the retained first failure follow.

No application runtime measurement or speedup is claimed. The cumulative
`ac633935a7f248470c59d22666da14c819a131fa` baseline, n-body alarm and expired
measurement budgets above remain unchanged.


## MIR value carrier acceptance

[PR #357](https://github.com/type-rb/type-rb-native/pull/357) is accepted at
`89a35c16de504ffb9c2ad926867ff277f6bf529d`, merged as
`3bde3e0a06d764789fc478e68255ffe47c209e33`, after all 17 authorities in
[run 34258862533](https://github.com/type-rb/type-rb-native/actions/runs/34258862533)
and the separately registered additional check passed.

The first amd64 attempt failed one retained adjacent-generation observation:
B2-to-B3 took 1.978962366 seconds, 2.05398157 times its strongest adjacent
median. The B2-to-B3/B3-to-B4 medians were 0.963476204/0.966003788 seconds;
all three compilers were byte-identical at 280,608 bytes, SHA-256
`fc325b7998a704c69f8b48da49239e99ad5ce7dae38c95043eba1f1670518426`.
The unchanged 2.0 guard correctly failed that cohort. Its 88 observations
(16 warmups and 72 retained measurements) are preserved, including the outlier.
Environmental variation motivated investigation but is not proven attribution.

A [single fixed-input confirmation](https://github.com/type-rb/type-rb-native/pull/357#issuecomment-5589567975)
kept the exact source, compiler identity, observer, workloads, repetitions,
ordering and all ordinary limits. The new amd64 cohort passed every guard;
its adjacent medians were 1.283581789/1.270438763 seconds (spread 1.01034527).
Both hosts report the same CPU model, but absolute times differ and both
host environments remain recorded. The additional pool of all 14 retained
observations per generation role gave medians 1.253844056/1.255019547 seconds,
spread 1.00093751; RSS spread is 1.00043349. The original catastrophic failure
remains a separate failed cohort, not a rewritten passing observation.
The one-run budget is exhausted and expired, with no third cohort authorized.

The [complete hosted acceptance record](mir-value-hosted-acceptance.json)
retains all 176 amd64 observations and both environments, source/compiler/tool
identities, original failure, registration and pooled calculation. It also
retains the subsequent ordinary arm64 compiler A/B observations and bounds.
Darwin self-build medians were 1.960/1.985 seconds (1.012755), with RSS ratio
1.002785. Linux medians were 1.350/1.370 seconds (1.014815), with RSS ratio
0.999557. All ordinary 1.05 limits passed. Darwin compiler size remains
365,768 bytes; Linux falls from 327,744 to 327,448 bytes, for 693,216 combined.
Compiler QBE falls from 1,151,452 to 1,150,705 bytes. These are compiler costs,
not application runtime improvements. The frozen cumulative baseline and prior
n-body alarm remain; no new cumulative timing or Pure Go comparison is claimed.

This closes the named record Array slice through ordinary support, matching
recovery, verified immutable seed handoff and actual compiler self-use. Other
MIR carriers and optimization facts remain independently bounded follow-ups.

## Named MIR function carrier and structural validation

[Issue #359](https://github.com/type-rb/type-rb-native/issues/359) registers the
next bounded self-use slice against `923f4bd31c70f1e83979034916bf4f781523dcc0`.
`Gate4MirFunction` replaces the eight-cell function row with named identity,
entry, source origin, and parameter/block ranges. Construction, verifier and
pass helpers, adapter consumers and strict recovery imports move together.
Other row families and optimization admission are unchanged.

Pre-migration characterization exposed a verifier defect: malformed ranges and
short rows could be indexed while counting value definitions before their
structural validation. A standalone malformed function range raised an Array
bounds error, and four of five expanded tests failed with bounds errors or the
wrong diagnostic. Structural checks now run before value and cross-block
consumers. The existing identity, origin, type, uniqueness, definition and
control-flow checks remain required; malformed function row length becomes
unrepresentable through the named carrier.

The [local correctness record](mir-function-carrier-correctness.json) binds the
candidate sources and includes all 426 ordinary check/repeated-QBE observations.
Fresh published-seed core/CLI fixed points, the language registry and full
CLI/REPL/terminal suite pass. Enabled recovery/QBE suites pass root 102/102 and
compiler 140/140; focused MIR tests pass 17/17. The new malformed-MIR tests also
pass in an ordinary Native-compiled harness. Its first preparation used an
unsupported core-command package import and was rejected; the corrected harness
uses the existing `puts` builtin without a compiler change. The owned recovery
workspace was removed only after both suites terminated.

Spectral-norm at input 100 and n-body at input 1000 retain byte-identical QBE,
executables and outputs against the accepted same-feature control. The local
Darwin compiler shrinks from 365,768 to 349,256 bytes; CLI size stays 499,144.
This does not establish application runtime improvement. Earlier cumulative
n-body alarms remain unresolved, and no new cumulative timing, Pure Go parity,
or benchmark/Pages-value update is claimed.

[PR #360](https://github.com/type-rb/type-rb-native/pull/360) is accepted at
`f4ef0986678ad0870dea48cdeb28decc6eed4e30` and merged as
`a714f9b20b1b2d9ddec29878a1982a18ed110a6e`.
All 17 authorities pass on the first attempt in
[run 34309605826](https://github.com/type-rb/type-rb-native/actions/runs/34309605826).
The [hosted record](mir-function-hosted-acceptance.json) retains all 88 amd64
observations (16 warmups and 72 retained), both arm64 bootstrap and interleaved
comparison cohorts, environment/toolchain/identity records, and cross-target
results. The PR merge-ref checkout has the same tree as the candidate head.

| Metric | Darwin arm64 | Linux arm64 |
| --- | ---: | ---: |
| Complete compiler bytes, before → after | 365,768 → 349,256 | 327,448 → 327,264 |
| Code text bytes, before → after | 260,700 → 260,512 | 263,280 → 263,120 |
| Self-build wall ratio | 0.988201 | 0.978417 |
| Self-build peak RSS ratio | 0.999405 | 0.999842 |

Combined compiler size is 676,520 bytes within the existing 694,000-byte bound.
Compiler QBE grows by 701 bytes to 1,151,406 while both code sections shrink;
its target-neutral SHA-256 is
`11f58bff93f3b9290e19a5c935735793cbd7958b5f17cff3d8b8965f3d30cbb0`.
The amd64 compiler is 279,976 bytes within its unchanged 310,000-byte bound.
No special confirmation, threshold revision or historical failure relabeling
was used. The generated applications remain unchanged as recorded above.
