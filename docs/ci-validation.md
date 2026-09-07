# Pull request validation stages

The single `Pull request validation` entry workflow classifies every changed
path, including deleted paths and both sides of renames. It has no path filter,
so a documentation-only change can still complete its merge-acceptance check.
Unknown non-documentation paths receive full correctness and target checking.

The changed-path inventory streams Git's NUL-delimited output instead of using
a fixed-size synchronous process buffer. Large evidence snapshots therefore
retain every path, including code changes after the first megabyte. Git errors
and incomplete path records fail planning; they do not authorize partial lists.

The exact static-documentation and evidence tools listed in `tools/ci-plan.mjs`
use the documentation authority, which executes their checks. A snapshot,
generator or evidence-retention-only update does not need compiler matrices.

The two exact planning files, `tools/ci-plan.mjs` and `tools/ci-plan-test.mjs`,
use the unconditional planning tests plus documentation validation. Rebuilding
an unchanged compiler does not test the router's selection contract. The
planning tests instead cover mixed changes, unknown paths, deletions/renames,
large inventories, draft eligibility and failure/missing/skipped-job rejection.
They also require the entry workflow to test and execute the actual router
unconditionally. Neither a label nor a user-supplied skip flag selects this lane.

This is not a blanket CI exemption. Compiler changes, execution workflows
(including the PR entry), suite controllers, benchmark controllers, toolchain
pins, measurement policies and unknown neighboring paths retain their normal
authorities. Adding any such path to planning-only maintenance restores the
compiler checks. Review the exact allowlist and routing-test changes together.

The post-merge Native push trigger ignores that same exact lightweight file
list; its synchronization is tested. Updating only those ignore entries uses
lightweight validation only when the router compares merge-base and head and
proves the rest of `gate-zero.yml` byte-identical. Changes to jobs, permissions,
branches, reusable-workflow entry, unknown patterns or other files retain their
normal checks. Missing/unreadable workflow versions fail toward full checking.
This narrow trigger-maintenance exception does not exempt arbitrary workflow
changes or permit glob-based compiler exclusions.

## Stages

1. **Planning and quick feedback.** Every PR runs routing/acceptance tests and
   whitespace validation. Code changes first check canonical compatibility
   metadata with the already-built pinned reference compiler, then formatting,
   core type checks, root unit tests, transition-policy tests, and a focused
   MIR, Array, scalar, and numeric test selection. These checks do not claim complete
   Native execution or benchmark evidence.
2. **Complete correctness.** A non-draft code PR runs the unchanged Native gate
   and Linux target authorities after quick feedback passes. Applicable
   compiler/runtime changes also run the persistent-memory authority.
3. **Comparative measurement.** Applicable compiler, conformance, transition
   policy, and execution-workflow changes run compactness/performance comparisons only
   after the complete Native, target, and memory authorities succeed. The
   measurement implementations, repetitions, evidence, and limits are unchanged.
4. **Merge acceptance.** `Native CI acceptance` verifies that every applicable
   authority actually succeeded. Failure, cancellation, a missing job, or a
   skipped required job rejects acceptance. Documentation- or planning-only
   ready PRs need only planning and their documentation authority.

Drafts receive quick and documentation feedback but deliberately fail the
merge-acceptance check with `Draft feedback is not merge acceptance`. This is
an eligibility result, not a failed correctness test. Marking the PR ready
triggers the complete pipeline even when no commit changed. Converting it back
to draft cancels the superseded run and revokes acceptance. A newer commit
cancels an obsolete PR run; cancelled measurements are not retained results.

The called authorities no longer launch duplicate standalone PR runs. Their
existing manual and post-merge triggers remain available. Full multi-language
benchmark refreshes and Pages deployment retain their existing manual controls.
Manual measurements do not substitute for the current PR acceptance chain.

The manual Native runtime A/B workflow selects a named, pre-registered contract
and its frozen baseline. The checked-Boolean selection uses the existing
Linux arm64 runtime controller and retains the historical derived-loop-index
selection unchanged. It supplements, rather than replaces, current-head PR
correctness and interleaved build/RSS authority; it adds no automatic runtime
comparison job. See [the controller contract](../tools/native-runtime-ab/README.md).

The compatibility preflight runs the existing validator and its regression
tests before the Native, target, and memory matrices can start. A mismatch
therefore fails quick feedback without spending those jobs. The standalone
Native workflow retains its own identical validation; no new reference build,
validator, skip option, or relaxed acceptance rule is introduced. See
[issue #287](https://github.com/type-rb/type-rb-native/issues/287).

## Correctness-suite scheduling

The Native gate runs the recovery-enabled root and compiler suites concurrently
through `tools/ci-run-suites.mjs`, with exactly two process groups. Their project
output directories are distinct. Every enabled root recovery invocation allocates
a fresh workspace atomically with `mktemp -d`; it never reuses a shared path.
All seven historical tool suites, allocation/worker smoke checks, and language-corpus verification
remain after the successful join. Comparative performance measurements never
overlap these correctness suites.

Both suites keep their full commands and all three recovery/QBE environment
variables. A failure does not skip the other suite's evidence: each gets its
own stdout/stderr log, exit code or signal, and elapsed time in `status.json`.
The job uploads `native-suite-evidence` even when a suite fails or is cancelled.
Cancellation terminates only owned process groups, escalating after a bounded
grace period. A parent that exits while leaving descendants causes cleanup and
failure rather than allowing background work into subsequent measurements.
Log-file setup completes before either process starts.

The controller tests use a mutual-start barrier to prove actual concurrency,
exercise one/both failures and missing executables, reject absent recovery
variables, and check cancellation and orphan-descendant cleanup. They run with
the routing tests, without launching compiler suites for documentation-only
changes. The scheduling change is registered in
[issue #263](https://github.com/type-rb/type-rb-native/issues/263); it changes no
test coverage, benchmark contract, threshold, or draft acceptance rule.

### Recovery workspace ownership

`src/compiler_recovery_workspace.trb` owns the test-only allocation contract.
The optional `TYPE_RB_NATIVE_RECOVERY_RECEIPT` names an evidence file, not a
workspace supplied by the caller. Give each invocation its own receipt file.
CI sets it inside the job's `native-suite-evidence`;
direct recovery-enabled tests can omit it and inspect the reported retained
workspace. Allocation or receipt publication failure fails the test, without
falling back to a shared directory. No ordinary Native compiler dependency or
production source closure is changed.

The versioned receipt contains exactly the generated `/tmp/trbn-recovery.` path
with its six-character suffix. The workspace carries an identical owner marker.
`tools/recovery-workspace.mjs` checks both regular files, the exact path shape,
and the non-symlink directory before providing the path to later smoke, corpus,
and shell-bootstrap consumers. After those consumers, an always-run step removes
only that validated directory and keeps both the receipt and cleanup outcome in
the uploaded suite evidence. Missing allocation produces `not-created`; an
invalid or foreign receipt is refused and fails cleanup. A killed runner can
still prevent an always-run step; this is not an orphan-reaper or a security
boundary against hostile processes with the same user privileges.

Focused tests cover overlapping allocations with a mutual-start barrier,
peer preservation, malformed/foreign ownership, symlinks, non-regular files,
and retained evidence. The existing suite process-group controller, cancellation
rules, complete test coverage, and all benchmark limits remain unchanged.
This is the workspace-isolation part of
[issue #295](https://github.com/type-rb/type-rb-native/issues/295); stage-level
timing instrumentation is a separate pending change.

## Protection and review

The main ruleset requires the uniquely named `Native CI acceptance` check from
GitHub Actions. It was activated after
[the complete hosted verification](https://github.com/type-rb/type-rb-native/actions/runs/33931154436)
passed at `85a6771f7256594d767bfcc36fab4a803d74b78b`. The existing PR-only,
no-force-push, and no-deletion rules remain unchanged, with no bypass actors.
Do not require conditionally omitted workflow names individually, and do not
interpret a green skipped job as an accepted compiler. GitHub documents that
skipped jobs otherwise count as
[successful checks](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-jobs-with-conditions).

The ruleset does not force an up-to-date branch after every unrelated main
change. Review the base delta before merging; update and revalidate a candidate
when that delta affects its correctness, measurement baseline, or CI contract.
This avoids requiring another complete measurement solely for an unrelated
documentation merge, without treating stale relevant evidence as current.

Tests and an acceptance check cannot replace review of the proof boundary.
Before requesting the comparative stage, inspect raw MIR, its independent
verification, mutation/effect exclusions, negative cases, and local compactness.
Prefer a separately measurable narrow optimization over combining header reuse
with access-check elimination. If local correctness or a registered size limit
fails, keep the candidate in draft and repair it before running long benchmarks.
