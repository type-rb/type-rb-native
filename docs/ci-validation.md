# Pull request validation stages

The single `Pull request validation` entry workflow classifies every changed
path, including deleted paths and both sides of renames. It has no path filter,
so a documentation-only change can still complete its merge-acceptance check.
Unknown non-documentation paths receive full correctness and target checking.

## Stages

1. **Planning and quick feedback.** Every PR runs routing/acceptance tests and
   whitespace validation. Code changes also run formatting, core type checks,
   root unit tests, transition-policy tests, and a focused Gate 4 MIR, Array,
   scalar, and numeric test selection. These checks do not claim complete
   Native execution or benchmark evidence.
2. **Complete correctness.** A non-draft code PR runs the unchanged Native gate
   and Linux target authorities after quick feedback passes. Applicable
   compiler/runtime changes also run the persistent-memory authority.
3. **Comparative measurement.** Applicable compiler, conformance, transition
   policy, and CI-routing changes run compactness/performance comparisons only
   after the complete Native, target, and memory authorities succeed. The
   measurement implementations, repetitions, evidence, and limits are unchanged.
4. **Merge acceptance.** `Native CI acceptance` verifies that every applicable
   authority actually succeeded. Failure, cancellation, a missing job, or a
   skipped required job rejects acceptance. Documentation-only ready PRs need
   only planning and their documentation authority.

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

## Protection and review

Require the uniquely named `Native CI acceptance` check in the main ruleset
after its first successful hosted verification. Preserve the existing PR-only,
no-force-push, and no-deletion rules. Do not require conditionally omitted
workflow names individually, and do not interpret a green skipped job as an
accepted compiler. GitHub documents that skipped jobs otherwise count as
[successful checks](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-jobs-with-conditions).

Tests and an acceptance check cannot replace review of the proof boundary.
Before requesting the comparative stage, inspect raw MIR, its independent
verification, mutation/effect exclusions, negative cases, and local compactness.
Prefer a separately measurable narrow optimization over combining header reuse
with access-check elimination. If local correctness or a registered size limit
fails, keep the candidate in draft and repair it before running long benchmarks.
