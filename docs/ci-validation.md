# Pull request validation stages

The single `Pull request validation` entry workflow classifies every changed
path, including deleted paths and both sides of renames. It has no path filter,
so a documentation-only change can still complete its merge-acceptance check.
Unknown non-documentation paths receive full correctness and target checking.

The changed-path inventory streams Git's NUL-delimited output instead of using
a fixed-size synchronous process buffer. Large evidence snapshots therefore
retain every path, including code changes after the first megabyte. Git errors
and incomplete path records fail planning; they do not authorize partial lists.

The three exact static-documentation tools (`tools/capability-map-check.mjs`,
`tools/benchmark-pages-data.mjs`, and `tools/benchmark-pages-check.mjs`) use the
documentation authority, which already executes those checks. A snapshot or
generator-only update does not need compiler or performance matrices. Mixed
compiler changes, CI-routing changes, and unknown neighboring paths retain the
normal full authority. Formal benchmark controllers are not documentation tools.

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
