# Validation by changed surface

The `Pull request validation` entry has no path filter. Its planning job tests
and executes `tools/ci-plan.mjs` against the complete merge-base-to-head delta,
including deletions and both sides of renames. Git output is streamed with NUL
separators; large evidence inventories, unusual filenames and unknown paths
cannot silently truncate or bypass validation. Git failures reject planning.

## Required authorities

| Changed surface | Required PR validation |
| --- | --- |
| Markdown, development metadata, static documentation, registered results and exact documentation generators | Planning and documentation |
| The two exact planning files | Their unconditional planning tests and documentation |
| Exact synthetic tool-test files listed in `toolingTests` | Planning and tooling controls |
| Exact CLI adapter, launcher, build helper and CLI-test inputs listed in `cliInputs` | Planning, quick checks and Darwin/Linux CLI artifacts |
| Ordinary compiler, conformance, execution workflows and measurement policy | Full applicable correctness, tooling, CLI, target, memory and comparative authorities |
| Other code or unknown files | Complete Native correctness, tooling and CLI/target checks; memory and performance according to the conservative rules in the planner |
| Mixed changes | The union of applicable authorities, with core changes restoring the core lane |

These are exact allowlists for executable exceptions, not filename suffix rules
for arbitrary tests. A new CLI file or neighboring tool defaults to the code
lane until its consumers and executing authority are reviewed. Production
measurement controllers, toolchain pins, suite controllers and stage-recording
code retain code validation. Tool-test-only routing is valid because the
independent tooling job actually executes each listed test. Compiler tests
and conformance fixtures retain their existing compiler authorities. Project
and transition-policy shell tests also retain their Linux quick-check authority
in addition to the macOS tooling checks.

CLI adapters are outside the ordinary compiler source closure. Their dedicated
workflow builds the current core from the pinned Native seed, verifies fixed
points, tests the CLI/REPL and packages Darwin/Linux artifacts. CLI-only changes
still run reference formatting/type checks and quick tests. Changing core
source alongside an adapter restores core and comparative checks. Documentation
under `compiler/` no longer accidentally triggers a separate CLI matrix.

The documentation authority checks evidence retention, skill metadata, public
path hygiene, the capability catalog and benchmark explorer. Pages does not
repeat those checks in a separate PR workflow. Its main-push deployment and
manual publication workflow retain verification before upload/deploy. Changing
the Pages workflow requires documentation validation, not compiler benchmarks.

## Scheduling and acceptance

1. **Plan and quick feedback.** Planning tests are unconditional. Code or CLI
   changes build the pinned reference compiler, validate canonical compatibility
   metadata, formatting/core types and root/focused MIR units. No complete
   recovery or comparative claim comes from quick feedback.
2. **Independent tooling.** The former Native `Verify bootstrap seed tooling`
   step runs unchanged on macOS in the separate `CI tooling controls` workflow.
   Its synthetic checks need no compiled candidate, so it can start after
   planning without waiting for quick feedback. This removes it from the serial
   path before recovery. Historical TypeRB tool suites and recovery-artifact
   consumers remain in the Native job after recovery joins.
3. **Correctness and CLI.** Complete Native, target and applicable memory jobs
   start after quick succeeds on non-draft core PRs. The CLI authority runs after
   quick for applicable changes, including drafts as before.
4. **Comparative measurement.** Applicable non-draft changes wait for Native,
   targets, memory, tooling and CLI success before starting comparisons. Existing
   repetitions, interleaving, baseline identities, raw evidence and limits stay
   unchanged. Diagnostic stage recording never runs inside measured chains.
5. **Acceptance.** `Native CI acceptance` checks every planned authority,
   including tooling and CLI. Failed, cancelled, missing or skipped required
   jobs reject acceptance. Unexpected execution of a disabled authority also
   rejects the plan/result mismatch.

Drafts receive quick, applicable tooling/CLI and documentation feedback but
reject merge acceptance with `Draft feedback is not merge acceptance`. Marking
ready triggers complete validation; converting back to draft cancels the old
run. New commits cancel superseded PR work. Cancelled measurements are not
accepted results.

`Main validation` replaces the separate Native, memory and documentation push
triggers. It executes the same planner using the complete **before-to-head**
push delta (two-dot, rather than a PR merge-base delta), then selects those
post-merge authorities and tooling controls. It does not add a second full PR
performance/target/CLI pipeline. Removed inputs and multi-commit pushes remain
visible. Unknown or invalid revisions fail planning rather than skip checks.
Main memory routing now covers the current compiler modules consistently rather
than maintaining a separate list of old entry paths. Manual workflow controls
remain available. Main pushes do not cancel earlier validations: a later
documentation-only delta must not erase an unfinished code validation.

Full multi-language benchmark refreshes and Native runtime A/B remain manual.
Manual measurements supplement rather than replace current PR acceptance.

## Recovery scheduling and stage evidence

`tools/ci-run-suites.mjs` runs exactly two recovery-enabled process groups: root
and compiler. Both retain their complete commands and recovery/QBE variables,
independent stdout/stderr logs, exit code/signal and monotonic elapsed duration
in `status.json`. A failure does not discard the peer's evidence. Cancellation
terminates only owned process groups, with a bounded grace period; orphaned
descendants fail validation. Log setup finishes before either process starts.

The root test also records thirteen ordered phases:

- source preparation and matched-Go comparison build;
- snapshot generation and B0 recovery;
- recovery generations, ordinary Native fixed point and generation controls;
- module-boundary mutations;
- file CLI, build CLI and project/module controls;
- normalization and differential conformance.

The controller gives only the root suite an invocation-local
`TYPE_RB_NATIVE_RECOVERY_STAGES` path. The test calls `tools/recovery-stage.py`
at phase boundaries; this external test observer uses Python's monotonic clock
and closes each JSONL receipt before returning. It adds no ordinary compiler or
runtime dependency. Direct recovery tests can omit this optional variable.
The receipt includes test-observer overhead and is a diagnostic phase duration,
not a replacement for controlled build/runtime measurements.

The controller finalizes `recovery-stages.summary.json` after root termination.
An unfinished phase is failed/cancelled/incomplete, never completed. Missing,
malformed, reordered, repeated or incomplete evidence rejects an otherwise
successful suite. Previously completed phases remain visible when a later
phase fails, but the summary cannot claim successful recovery. Both raw receipts
and the summary live in the always-uploaded suite evidence directory.

The source-mutation helper uses the reference compiler's code-point `index`,
`rindex` and `slice` operations. Comparing the first and last match preserves
strict uniqueness, including overlapping needles; prefix/suffix slices preserve
all surrounding source bytes. This removes repeated per-character scans and
string reconstruction from module-boundary setup without removing a mutation,
missing-module, malformed-module or generated-output check. Focused tests cover
Unicode, empty/missing needles, overlaps and replacements at both boundaries.

Stage instrumentation completes the remaining observability scope of
[issue #295](https://github.com/type-rb/type-rb-native/issues/295). Use measured
phase costs to select later bounded scheduling changes; do not remove generation
identity, mutation or differential checks merely because they are slow.

### Recovery workspace ownership

Each root invocation allocates a fresh workspace with `mktemp -d` through
`src/compiler_recovery_workspace.trb`. `TYPE_RB_NATIVE_RECOVERY_RECEIPT` names
an evidence file, not a caller-supplied workspace. The exact generated path and
owner marker are checked by `tools/recovery-workspace.mjs` before later smoke,
corpus and shell-bootstrap consumers use it. The always-run cleanup removes
only that validated directory and uploads the receipt and outcome. Invalid or
foreign ownership fails cleanup; absence before allocation is `not-created`.
A killed runner can still prevent an always-run step. This is not an orphan
reaper or a boundary against hostile processes with the same user privileges.

Tests cover actual suite concurrency, failures, cancellation/descendants,
stage receipt order and completeness, workspace isolation and ownership,
large/deleted/renamed/mixed path inventories, selective routing and acceptance.
The bounded CI changes are recorded in
[issue #313](https://github.com/type-rb/type-rb-native/issues/313).

## Protection and review

The main ruleset requires the uniquely named `Native CI acceptance` check from
GitHub Actions. Existing PR-only, no-force-push and no-deletion rules remain.
Do not require conditionally omitted workflow names individually or interpret
a green skipped job as accepted compiler evidence. Review relevant base changes
before merging; update and revalidate when correctness, measurement baseline
or the CI contract changes. An unrelated documentation merge alone does not
invalidate the compiler evidence.

Routing and tests cannot replace review of semantic proof boundaries. Preserve
raw MIR verification, mutation/effect exclusions, negative cases, compactness
and measured thresholds before accepting a compiler optimization.
