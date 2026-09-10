# Daily performance and benchmark strategy

Status: adopted for the daily diagnostic layer. Existing correctness, safety,
self-hosting, compiler cost and optimization acceptance authorities are unchanged.

## Purpose and cadence

The primary benchmark page answers what has changed, which supported workload
areas remain slow, and how the identical TypeRB source compares through the Go
backend. It is not a language ranking. Daily data does not need a new complete
seven-implementation cohort or a manual prose update.

- PRs retain their applicable acceptance checks. A daily snapshot is never a
  dependency of PR acceptance, merge, cleanup, or starting the next task.
- `daily-performance.yml` checks main at 21:23 UTC (06:23 JST) once daily. GitHub
  may delay scheduled jobs. Relevant unchanged sources skip measurement. The
  independent state upload is renewed even on unchanged days.
- Manual dispatch can force an immediate refresh. Only main can measure and
  publish. One run may be active; pending requests coalesce through Actions
  concurrency without cancelling the active cohort.
- Complete Benchmarks Game comparisons remain manual, on a separate page.
  Run one for a concrete cross-language or large-input question, or before a
  performance claim that needs it. There is no required monthly refresh.
- Long-lived memory, worker stability and sanitizer checks keep their own
  existing triggers. Short speed measurements cannot replace them.

The initial target is a 10–15 minute daily update, with a 25-minute job safety
limit. This is an operational budget, not an already measured duration or a
requirement to wait after merging. Calibrate using the first real daily runs;
reduce redundant work before broadening the suite.

## Initial coverage

The machine-readable contract is `tools/daily-performance/suite.json`.
It reuses the existing TypeRB workload bodies and checked-in output oracles:

| Area | Workload | Daily input |
| --- | --- | --- |
| Integer, branches, Array updates | fannkuch-redux | 10 |
| Float operations | n-body | 1,000,000 |
| Numeric loops | spectral-norm | 5,500 |
| Array traversal | Integer reduction | 100,000 elements, 1,000 rounds |
| Allocation and GC | memory workload | one phase, 5,000,000 iterations |
| String/Array/state interactions | worker workload | one phase, 40,000 batches |
| Fresh-process startup | minimal CLI | one output line |

Memory and worker inputs change only their single registered invocation.
Separate untimed Native probes report whether automatic GC actually occurred.
Their runtime observations have instrumentation disabled. A missing GC signal
is a coverage gap, not evidence of healthy collector performance.

These are a bounded first slice. General String processing, Hash, JSON, I/O,
service latency and large working sets are not covered. Add one useful case
at a time as ordinary portable support exists; do not extend language semantics
just to port a suite. The compiler's own bootstrap cost remains separate from
the application's clean-output build timings and sizes shown here.

## Comparison and measurement

Four roles run serially on one logical CPU of a fresh Linux arm64 hosted runner:
current Native, the previously measured Native revision, a frozen Native
baseline, and the exact compatible TypeRB Go revision in `TYPE_RB_REVISION`.
All roles compile the same source bytes. Each Native chain is closed through
the existing bootstrap verifier from an exact published seed. Identical role
revisions share a compiler preparation inside one run. If no compatible previous
snapshot exists, that role uses current Native and the page shows no previous
comparison. The frozen baseline is not automatically advanced.

Runtime uses one warmup and five retained fresh processes. Application builds
use one warmup and three retained clean-output builds with a warm Go build
cache; this is not a cold-cache build claim. Role order rotates each round.
Filesystem caches stay warm, swap is disabled, and measurements do not run
concurrently on the measurement host. Warmup in a separate process does not
warm a later process's JIT or heap.

Wall time includes launcher overhead. GNU time records CPU and maximum RSS;
RSS is not a simultaneous sum of a process tree. Short startup CPU/RSS values
can be below resolution and appear unavailable. Startup wall values are a
launch-inclusive diagnostic, not isolated language startup latency.

Every runtime observation checks exact output, empty stderr and exit status.
Build failures, output differences and timeouts are published as failed cases,
with no passing runtime median. A timeout stops further observations of that
role/case, preserving the failure and continuing other cases. The controller
kills its owned process group on timeout. A complete numeric regression still
publishes normally. Infrastructure failure keeps the last complete snapshot
and publishes the failed attempt when state is available.

Five percent is a visual screening band only. It changes no acceptance bound
and is not a significance test. Small changes require focused, prospectively
bounded A/B confirmation. Preserve all samples; do not repeat until passing.
Minimum/maximum retained wall times help expose noise. Trends show ratios to
the frozen compiler measured in the same cohort, not causal differences between
absolute timings from different hosted machines.

## Publication and retention

The daily workflow has no repository write permission. It uploads a compact
state artifact and raw evidence. The existing Pages workflow runs after the
daily workflow completes, reads data only from this repository's main-branch
daily workflow, validates it, and composes a static deployment. Source changes
still go through PRs; daily measurements do not push to main or create data PRs.
Unrelated Pages updates restore the daily state instead of resetting the page.

The state carries the last snapshot, latest attempt and up to 60 historical
snapshots. Raw measurements, derived source, toolchain identity, compiler closure
and process evidence are retained as Actions artifacts for 90 days. The page
links each run; old raw artifacts expire. Promote evidence through the existing
result archival policy before making a durable formal claim.

Workload/source/oracle/controller changes start a new measurement series.
Only the current series is graphed together. Performance input fingerprints
include compiler/runtime sources, compatible compiler pins, daily tooling and
reused workload sources; prose-only and compiler test-only edits do not require
another timing run. Failed API retrieval does not masquerade as empty history.
If no retained state exists, the page explicitly starts without daily values.

After the first bounded adoption period, review runtime cost, false alarms,
detected regressions and decisions informed. Replay a known regression/fix pair
and use identical-binary comparisons before relying on this diagnostic for small
changes. This calibration is separate from formal acceptance; the daily page
does not claim it has already established a statistical detection guarantee.
