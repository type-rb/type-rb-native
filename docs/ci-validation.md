# Validation by changed surface

The `Pull request validation` entry has no path filter. Its planning job tests
and executes `tools/ci-plan.mjs` against the complete merge-base-to-head delta,
including deletions and both sides of renames. Git output is streamed with NUL
separators; large evidence inventories, unusual filenames and unknown paths
cannot silently truncate or bypass validation. Git failures reject planning.

## Active MIR integration mode

[Issue #439](mir-consolidation.md) establishes an explicit `mir-migration` mode
for PR/main integration. All applicable correctness, recovery, target identity,
process, memory-lifetime, sanitizer and cleanup jobs remain required. Compiler
size and smoke-time limits write observations with their actual exceeded
status; they do not stop correctness verification. Standalone tools and workflows
default to `strict`, and unknown modes or malformed measurements fail.

Migration changes omit the separate arm64 comparison and the amd64
repeated formal timing series. Binary-format, dependency, generation, output and
failure checks still execute. CI workflow/routing/policy changes also retain
controller tests and applicable integration correctness, without restoring the
strict cost matrix. Daily/weekly diagnostic schedules remain.
The matrix and historical scheduling below describe the strict contract; green
migration CI must not be reported as a performance-qualified result.

## Required authorities

| Changed surface | Required PR validation |
| --- | --- |
| Markdown, development metadata, static documentation, registered results and exact documentation generators | Planning and documentation |
| The two exact planning files | Their unconditional planning tests and documentation |
| Exact synthetic tool-test files listed in `toolingTests` | Planning and macOS tooling; project/policy shell tests also run Linux quick tooling |
| Existing compiler unit-test modules listed in `compilerTestInputs` | Complete quick, Native, CLI, tooling and target correctness; no unchanged-binary performance or worker-memory measurements |
| Exact CLI adapter, launcher, build helper and CLI-test inputs listed in `cliInputs` | Planning, quick checks and Darwin/Linux CLI artifacts |
| Ordinary compiler, conformance, execution workflows and measurement policy | Full applicable correctness, tooling, CLI, target, memory and comparative authorities |
| Other code or unknown files | Complete Native correctness, tooling and CLI/target checks; memory and performance according to the conservative rules in the planner |
| Mixed changes | The union of applicable authorities, with core changes restoring the core lane |

These are exact allowlists for executable exceptions, not filename suffix rules
for arbitrary tests. A new CLI file or neighboring tool defaults to the code
lane until its consumers and executing authority are reviewed. Production
measurement controllers, toolchain pins, suite controllers and stage-recording
code retain code validation. Tool-test-only routing is valid because the
independent tooling job actually executes each listed test. Suite-controller
and workspace-ownership tests run on Linux in unconditional planning and on
macOS in tooling, moving the former Native step without duplicating it.
Project and transition-policy shell tests also retain their Linux quick-check
authority in addition to the macOS tooling checks. For changes limited to those
tests, quick skips reference checkout/build, compatibility, formatting/types and
TypeRB units; the Linux shell tests need none of those compiler inputs.

The ten reviewed compiler unit-test modules are excluded from ordinary
reference/Native compiler builds and CLI source staging. Changing only those
modules cannot change the measured compiler or worker binary. Full correctness
and target checks still execute; only comparative and worker-memory measurements
are omitted. Conformance fixtures, new test paths, project configurations,
production source and measurement policies retain conservative routing. A mixed
non-exempt code change restores the previous compiler measurement requirements;
changing routing/execution workflows still exercises the full graph.

CLI adapters are outside the ordinary compiler source closure. Their dedicated
workflow builds the current core from the pinned Native seed, verifies fixed
points, tests the CLI/REPL and packages Darwin/Linux artifacts. CLI-only changes
still run reference formatting/type checks and quick tests. Changing core
source alongside an adapter restores core and comparative checks. Documentation
under `compiler/` no longer accidentally triggers a separate CLI matrix.
The extracted `compiler/cli/repl_project.trb`, `repl_check.trb` and
`repl_defaults.trb` are explicit CLI inputs: the
builder stages every CLI module, and both target CLI authorities execute the
project/import, retained-record, replay and shared-language controls that use them.
The callable environment and type-context adapters (`repl_callables.trb` and
`repl_types.trb`) are also staged in every CLI build. `native-callable-test.py`
is invoked by the CLI authority on both targets and covers retained calls,
nominal remapping, cyclic captures, failure recovery and replay.
`repl_globals.trb` retains runtime constants and is staged with the CLI modules.
`native-constants-test.py` runs in both CLI authorities and checks persistent GC
roots, initializer order, retained values, failed initialization and replay.
`native-scalar-strings-test.py` runs in both CLI authorities and independently
checks Float String conversion across every binary64 binade and adjacent values,
including subnormals, plus retained callbacks, optional calls and session replay.

`native-sliced-iteration-test.py` runs in both CLI authorities. It checks fresh
managed batches under forced collection, exact reclamation, bounded first-batch
execution over the full portable Range, and retained REPL failure/replay.

`native-union-hash-test.py` runs in both CLI authorities. It checks Integer and
String literal-union keys through growth, deletion, copies and snapshots under
forced GC, including Unicode/NUL payloads, exact reclamation, and retained
snapshot closures across declaration remapping and replay.

The CLI cache test gives each complete core/CLI fixed-point rebuild a bounded
600-second watchdog and records its elapsed time; the whole CLI job allows
90 minutes for the repeated invalidation controls. Literal-union Hash integration
completed Linux rebuilds in 272 and 289 seconds before another rebuild exceeded
the earlier 300-second deadline. The ordinary fixed point and CLI/GC controls
had passed. The previous 30-minute job
limit expired on Linux during the generic-enum integration after the CLI,
UTF-8 and GC checks had passed. A 120-second rebuild watchdog
expired during nullable integration after the ordinary build and functional
controls had passed. These are execution deadlines, separate from the performance
acceptance contracts. Timeout remains a failure and terminates the owned builder
process group. Cache reuse, failure atomicity and concurrent-caller assertions
remain required.

Concurrent callers share the same 600-second rebuild deadline, including the
launcher's bounded lock wait. Key-based sorting CI exposed a remaining
120-second concurrent-call timeout after ordinary rebuilds and functional checks
had passed. The concurrent test records elapsed time and still requires both
callers to succeed, identical output, exactly one builder and subsequent reuse.

The documentation authority checks evidence retention, skill metadata, public
path hygiene, the capability catalog and benchmark explorer. Pages does not
repeat those checks in a separate PR workflow. Its main-push deployment and
manual publication workflow retain verification before upload/deploy. Changing
the Pages workflow requires documentation validation, not compiler benchmarks.

## Scheduling and acceptance

1. **Plan and quick feedback.** Planning tests are unconditional. Code or CLI
   changes build the pinned reference compiler, validate canonical compatibility
   metadata, formatting/core types and root/focused MIR units. No complete
   recovery or comparative claim comes from quick feedback. The explicit `quick`
   output also selects Linux-only tooling steps for project/policy test edits;
   code and CLI plans must always require complete quick feedback.
2. **Independent tooling.** The former Native `Verify bootstrap seed tooling`
   commands run unchanged on macOS in the separate `CI tooling controls` workflow.
   Its synthetic checks need no compiled candidate, so it can start after
   planning without waiting for quick feedback. This removes it from the serial
   path before recovery. Recovery-artifact consumers remain in the Native job after recovery joins.
   The retired source-era benchmark controllers are no longer rebuilt or tested
   against current source; see [their preserved versions](retired-experiment-tools.md).
3. **Correctness and CLI.** Complete Native, target and applicable memory jobs
   start after quick succeeds on non-draft core PRs. Complete CLI validation,
   including bootstrap-cache invalidation, also starts only when the applicable
   PR is ready. Development drafts retain the source/CLI checks in quick feedback.
4. **Comparative measurement.** Applicable non-draft changes wait for Native,
   targets, memory, tooling and CLI success before starting comparisons. Existing
   repetitions, interleaving, baseline identities, raw evidence and limits stay
   unchanged. Diagnostic stage recording never runs inside measured chains.
5. **Acceptance.** `Native CI acceptance` checks every planned authority,
   including tooling and CLI. Failed, cancelled, missing or skipped required
   jobs reject acceptance. Unexpected execution of a disabled authority also
   rejects the plan/result mismatch.

Drafts receive quick, applicable tooling and documentation feedback but
reject merge acceptance with `Draft feedback is not merge acceptance`. Marking
ready triggers complete validation; converting back to draft cancels the old
run. New commits cancel superseded PR work. Cancelled measurements are not
accepted results.

Develop complete language families with focused local units, reference/Native
positive and negative cases, MIR ownership and retained REPL checks. Include an
ordinary Native build when compiler source changes. Hosted CI is the complete
integration authority by default; full local recovery is additionally required
for bootstrap or validation-orchestration changes and recovery/platform diagnosis.
Optional local suites without recovery variables remain partial evidence. Do
not mark a language family complete or merge while required CI is pending.
Larger cohesive PRs may combine syntax through execution and REPL; keep one
ready candidate and one subsequent development batch instead of repeatedly
revalidating a stack of small dependent PRs.

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
During MIR migration they supply milestone qualification separately from
integration correctness; ordinary compiler edits do not wait for detailed costs.

## Focused compiler preflight feedback

Before making a compiler PR ready, use the existing standalone workflows when
a target-size or compiler-cost question needs earlier feedback. Do not dispatch
another copy of a comparison that is already running for that exact candidate.
[Issue #425](https://github.com/type-rb/type-rb-native/issues/425) tracks this path;
it changes no acceptance dependency or measurement limit.

Start from a clean, committed and pushed PR branch. Record its exact commit and
the baseline chosen in the registered comparison; do not replace that baseline
with a newer main revision between observations. The baseline must be an ancestor
of the candidate. Local ordinary fixed points and relevant correctness checks
remain prerequisites; record which full authorities are still pending.

```sh
test -z "$(git status --porcelain)"
candidate_ref=$(git symbolic-ref --short HEAD)
candidate_revision=$(git rev-parse HEAD)
test "$(git ls-remote --heads origin "refs/heads/$candidate_ref" | cut -f1)" = "$candidate_revision"
```

For a cost comparison, set `baseline_revision` to its registered full commit ID
and verify `git merge-base --is-ancestor "$baseline_revision" "$candidate_revision"`.

For the Linux amd64 artifact and its arm64 target-neutral control, dispatch the
existing target controller:

```sh
gh workflow run linux-amd64-targets.yml --ref "$candidate_ref"
```

For a separately registered compiler-cost comparison, the existing compactness
workflow accepts an explicit baseline instead of its historical default:

```sh
gh workflow run static-string-compactness.yml --ref "$candidate_ref" \
  -f "baseline_revision=$baseline_revision"
```

Select the newly created dispatch by its run ID, then use
`gh run view RUN_ID --json event,headBranch,headSha,status,conclusion` to verify
that it is a manual run of the expected candidate commit. If the branch moved
or several runs are ambiguous, resolve the identity before interpreting results;
do not dispatch again merely to obtain an easier match. Retain the run ID,
verifier/policy revision, baseline and toolchain identities with the evidence.

Inspect completed target artifacts as soon as they are available. Report actual
fixed-point executable sizes and their enforced limits: shorter source or QBE
Strings can compress less well and produce a larger compiler. For latency work,
record the first actionable failure time separately from full-suite completion.
Host-local or emulated checks are diagnostics, not hosted runtime comparisons.

Retain failed and partial evidence and clean only owned workspaces. Apply the
registered run budget rather than retrying an unchanged failure. Passing this
preflight does not make a draft mergeable or replace fresh complete PR acceptance;
the formal multi-language benchmark remains a separate manual operation.

## Further latency boundaries

Standalone strict acceptance limits remain unchanged by the
[trade-off policy](optimization-tradeoffs.md). Active migration integration
instead follows the explicit observation contract above. A registered bounded diagnostic
may use standalone measurement controllers when ordinary compactness fails;
label that evidence diagnostic and retain the ordinary failed status. This
does not enable a hidden CI skip, a force-merge path, or a new benchmark on every
PR. No generic diagnostic-to-acceptance switch exists. A future candidate-scoped
acceptance budget requires a reviewed enforcement change and fail-closed tests
before it can affect CI acceptance.

Generation controls check the recovery source through B0, B1 and B2 and compare
repeated QBE emission against each previously built generation. Those repeated
commands test distinct seed/command behavior and deterministic output; deleting
them would remove coverage. Ordinary B1-to-B4 regeneration also preserves its
sequential seed dependencies. No generation check or benchmark repetition is
removed by test-only routing.

Quick checks retain their ordering for compiler/CLI changes. Independent recovery
controls use bounded concurrency within the existing runner, as described below.
Comparative performance still follows complete correctness acceptance.

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

After generation production and ordinary fixed points complete, the thirteen
independent generation commands run with bounded concurrency. Each retains its
exact executable, arguments and expected stdout, zero exit status and empty
stderr. All results are collected in input order, including failures after a
peer fails. Empty batches, duplicate labels, launch failures and output mismatches
reject acceptance. The B0-to-B3 recovery and B1-to-B4 ordinary generation chains
remain sequential; no dependent producer/consumer pair runs concurrently.

Module-boundary controls use the same limit across modules. Each module owns
separate mutation, missing-module and malformed-module directories; shared
compiler inputs are read-only. Every module still checks changed QBE, diagnostic
and exit behavior, failure before external tools, and absent output/intermediate
files. Hidden-import and unrelated-sibling controls also remain required. Both
control groups fully join before their stage-end receipt is written. Their
descendants stay in the root suite's owned process group for cancellation.

`TYPE_RB_NATIVE_RECOVERY_JOBS` defaults to `2`; explicit values `1` through `4`
are accepted, with `1` available for serial diagnosis. Other values fail before
workspace allocation. The limit is per root invocation; the compiler suite
continues independently. This is test orchestration through the pinned Go
reference's `concurrent_map`, not a Native concurrency-support claim or a new
ordinary compiler dependency. Synthetic subprocess tests check bounded overlap,
exactly-once admission/completion and complete, ordered failure collection at
limits 1, 2 and 4. Record phase durations and runner resource costs when evaluating
the change; do not present an estimated speedup as a measurement.

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

Callable suffix and lexical-boundary changes retain the shared ordinary/REPL
registry, source-erased and reordered MIR under forced GC, and the Symbol CLI
retained-session checks. Those checks exercise reserved-name failures, Unicode/NUL
function returns and replay. Maximal operator tokenization is independently
checked with nested generic annotations/applications and later default origins;
it does not qualify unimplemented executable operators.
