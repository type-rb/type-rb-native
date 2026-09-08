# Current reference compatibility

The current development pin is TypeRB `0.4.6-dev` at
`caf6aadb9493ca69290ab0dc22d420b5f574df14`, the merged
[stable Array assignment update](https://github.com/type-rb/type-rb/pull/659).
It captures the Array receiver, requested index and validated nonnegative
position before the RHS. Compound assignments retain their old value, while
the final write checks the position against current storage. Snapshot v4
represents the initial check and normalization with existing operations.

The implementation baseline remains accepted Native
`ac633935a7f248470c59d22666da14c819a131fa` from PR #340, with
[unchanged-head acceptance attempt 2](https://github.com/type-rb/type-rb-native/actions/runs/34172032048/attempts/2).
That acceptance does not cover this assignment candidate. The first attempt's
retained failure remains part of its source-era evidence.

Local ordinary Integer, Float, nested-owner and managed String assignment
cases match the selected reference, including actual RHS growth and an
initial bounds failure that skips RHS effects. The managed case records five
automatic collections and zero live bytes after final collection. The formerly
crashing Integer growth probe succeeds under GuardMalloc. The pinned published
seed builds the current core and CLI fixed points; ordinary CLI and REPL tests
pass with the new cases. Full recovery and hosted target, memory and cost
acceptance on the final PR head remain required before merge.

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
