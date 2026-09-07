# Array-loop cost and runtime trade-off diagnostic

Not accepted. The current named-field verifier candidate reduces compiler QBE
and text but still exceeds both absolute limits. Its first named-field build
cohort fails wall time; later trade-off cohorts pass and are reported separately.
The earlier batching-only cohort passes local time/RSS, not absolute size.
The later bounded runtime evaluation is recorded below separately from ordinary
acceptance. Corrected-source full local recovery now passes; hosted Linux arm64
target/memory authorities stop at the unchanged compiler-size limit. There is
no Pure Go or Pages performance claim.

## Identities and scope

The fixed comparison remains `1afd60c2c7257ed34fd2a2aa70cb8b9164433009`.
Integrated control `1e4ace11` includes accepted main `3ae51bbf`, exact reference
`47a160cae05ddc2035c7430735c4762d36bbc9c4`, Boolean support and current
retention/CI policy. It is not a new acceptance baseline. Candidate
[source hashes](source-identities.json) identify the current named-field verifier
source and tests. Batching-only identities remain at
[`ffd99fa3`](https://github.com/type-rb/type-rb-native/blob/ffd99fa3aa06a84a5e8158e9c2311039c70f02ab/results/2026-09-07-array-loop-output-batching-darwin-arm64/source-identities.json);
application semantics are unchanged.
The [registration](https://github.com/type-rb/type-rb-native/issues/303#issuecomment-5566332134)
preceded the batching implementation.

The driver previously called puts for every stored QBE line. A TypeRB helper
now combines complete lines up to 4096 characters before each puts; one longer
line remains intact. Embedded/empty lines and the final newline are preserved.
No runtime API, compiler intrinsic, MIR proof, target rule or threshold changes.

## Local verification

- Integrated control: source checks, 149 compiler tests and previous-Native
  core/CLI fixed points pass. These compiler tests did not enable recovery.
- Batching: root/compiler checks, three focused output tests, previous-Native
  core/CLI fixed points and CLI/REPL/terminal tests pass.
- All 81 corpus cases pass, with exact repeated QBE/diagnostics and unchanged
  QBE/diagnostics against the integrated control. Valid cases execute with exact
  output; required failures preserve status class and diagnostics.
  [Inventory](corpus-status.json).
- 23 routing tests, 13 archival tests and unchanged Pages data pass for the
  integration. New-source full recovery and hosted acceptance are still required.

## Cost observations

Apple M2 Pro, macOS 26.6.2 (25G83), Darwin arm64, QBE 1.3, Apple clang
21.0.0 through `/usr/bin/cc`, `darwin-arm64-v0`. Warm caches, no CPU affinity or
host-wide isolation. All other owned builds/tests completed before timing.
Use the unchanged [observer](https://github.com/type-rb/type-rb-native/blob/ba065229c96555cc968c3ed8e6797ce91991afa7/results/2026-09-06-mir-loop-bounds-diagnostic-darwin-arm64/build-cost-observer.py)
with each exact candidate checkout, its compiler, the frozen baseline compiler
and QBE. Each role builds its own source; two warmups and seven retained builds
per role alternate order. The clock is monotonic; wait4 CPU/root RSS are not
summed process-tree memory. All 18 builds in each valid cohort reproduce their
own compiler. The cohorts are separate, not one interleaved control/batching A/B.

| Candidate / frozen baseline | Wall ratio | CPU ratio | RSS ratio | Time/RSS |
| --- | ---: | ---: | ---: | --- |
| Integrated control | 1.0784632 | 1.0772980 | 1.0065601 | fail |
| Bounded batching | 1.0177125 | 1.0226662 | 1.0016293 | pass |

All retained observations in the valid cohorts pass the 2.0 catastrophic check.
[Control raw rows](control-raw.csv), [batching raw rows](batched-raw.csv) and
[complete summaries](summary.json) preserve both outcomes.

| Artifact | Integrated control | Batching | Absolute limit |
| --- | ---: | ---: | ---: |
| Complete compiler bytes | 349256 | 349256 | 350000 |
| Mach-O text bytes | 253768 | 254468 | 250904 |
| Target-neutral QBE bytes | 1129861 | 1132120 | 1120000 |

Integration already exceeds the text/QBE limits. Batching adds 700 text bytes
and 2259 QBE bytes without crossing another executable alignment boundary.
Retain it only as a draft diagnostic; reduce the remaining compiler/projection
code cost before dispatching full hosted acceptance. File-size equality alone
does not prove compactness.

An initial invocation used the newer cache path for the old baseline, which
does not retain its core there. Baseline executions failed with status 127;
[all invalid rows](invalid-setup-raw.csv) remain explicitly excluded from
performance conclusions. A setup-only CLI invocation also rejected an explicit
target option unsupported by that old CLI. The corrected old CLI regenerated
the baseline core, whose next ordinary build reproduced it byte-for-byte,
before the two valid cohorts above. These are setup failures, not slow baselines.

## Verifier-size refinement

The [registered follow-up](https://github.com/type-rb/type-rb-native/issues/303#issuecomment-5566937365)
names five immutable instruction fields after the existing row-shape and origin
validation. The verifier retains every predicate, diagnostic and independent
Array proof recomputation; it no longer repeatedly indexes the same row fields.
This does not add MIR facts or move semantics into QBE emission.

| Artifact | Batching only | Named instruction fields | Absolute limit |
| --- | ---: | ---: | ---: |
| Complete compiler bytes | 349256 | 349256 | 350000 |
| Mach-O text bytes | 254468 | 253180 | 250904 |
| Target-neutral QBE bytes | 1132120 | 1129223 | 1120000 |

The remaining excess is 2,276 text bytes and 9,223 QBE bytes. Previous-Native
core/CLI builds reach fixed points. All 81 corpus cases execute or reject as
required, and their repeated QBE/diagnostics are byte-identical to `ffd99fa3`.
All 152 compiler tests and root/compiler source checks pass. Recovery was not
enabled in this suite; full recovery remains required. No generated-application
speedup follows from this compiler-only refinement.

The same frozen-baseline observer, machine/toolchain and 2-warmup/7-retained
protocol produced the [new raw cohort](named-fields-raw.csv). All other owned
tests/checks completed before timing, and all 18 builds reproduce their own
compiler. Wall ratio **1.1047821 fails 1.05**; CPU **1.0374060** and RSS
**1.0004095** pass. All retained catastrophic values remain below 2.0.
The full summary includes the failure. This is a separate cohort, not proof
that naming fields caused a specific slowdown or that the earlier batching
time pass transfers to this source. Do not discard it or substitute the earlier
timing result for current acceptance. Full hosted/runtime acceptance remains
deferred while the absolute code-size bounds fail.

Two earlier bounded size trials were reverted: a shared checked-value
constructor reduced text by 36 bytes but increased QBE by 252 bytes; a flat
output container increased text by 296 bytes and QBE by 1,272 bytes. Neither
justified changing the current representation. Their size diagnostics do not
alter any allowance or constitute runtime evidence.

## Bounded trade-off protocol

The [prospective registration](https://github.com/type-rb/type-rb-native/issues/303#issuecomment-5567395291)
uses the policy adopted in PR #319. Candidate production source remains
`c33b105fee3af3712fe97d938d20167d2f013bdf`; integrating the policy as `1309ce32`
changes no compiler, runtime or tool code. The cumulative control stays
`1afd60c2c7257ed34fd2a2aa70cb8b9164433009`; accepted main
`26bb32a3d3bd085fdae4fc190bf2a14703351a8f` is the additional same-feature
control. This measures the whole pending candidate, not a causal ablation of
each compiler-cost refinement.

The candidate-specific investigation ceilings are 350,000 complete compiler
bytes and 1.05 times the cumulative compiler, 254,000 text bytes and 1,135,000
QBE bytes. Self-build wall/CPU/root RSS limits are 1.20/1.10/1.05 against each
same-run control; retained catastrophic observations remain limited to 2.0.
Ordinary 250,904 text, 1,120,000 QBE and 1.05 cost ratios are unchanged and
reported separately. This is not an acceptance allowance.

Runtime measurements use unchanged sources and inputs: spectral-norm/5500 has
two separately executed cohorts against each control, with wall and CPU ratios
at most 0.98. The n-body/1000000 and fannkuch-redux/10 controls have one cohort
per comparison and 1.02 wall/CPU limits. All have 1.05 median root RSS and 2.0
retained catastrophic limits. Each cohort contains two warmups and seven
retained observations per role, alternating baseline/candidate order by round.
The smaller control inputs are bounded diagnostic coverage, not replacements
for full formal controls. No observations are retried or selected out.

Use the [external observer](tradeoff-observer.py) in `setup` then `measure`
mode, passing the candidate checkout, a fresh output directory, QBE, and the
frozen/main/candidate compilers. Its public version exposes those paths as
arguments; the locally executed version supplied them as configuration
constants, with identical setup and measurement functions. Setup snapshots
each compiler's exact own source from Git, checks compiler fixed points and
source equality, builds all nine applications, and checks expected stdout and
empty stderr before timing. Measurement uses monotonic fork/exec/wait4 timing,
records every row before proceeding, validates outputs or compiler fixed points,
and imposes a single 20-minute deadline on the eight runtime and at most two
self-build cohorts. Timeout kills the observed process group and records failure.
Catastrophic and median budget checks occur when a cohort's medians are available;
wrong output or timeout stops immediately. A missed minimum runtime benefit is
retained as a failed criterion, not retried for a more favorable sample.

The same Apple M2 Pro/macOS 26.6.2/QBE 1.3/Apple clang 21.0.0 environment is
used, with warm caches and no CPU affinity or host-wide isolation. Other owned
builds/tests finish before timing. Application sizes here are ordinary unstripped
Mach-O executables, not the published stripped Linux sizes. External QBE and
system tool dependencies remain unchanged and are not included in app bytes.
Application builds in setup are untimed correctness preparation; this diagnostic
does not establish application build-time ratios or current TypeRB Go headroom.

## Trade-off evaluation outcome

All ten registered cohorts completed in 241.94 seconds, without retries. All
144 runtime observations have exact expected output and all 36 self-build
observations reproduce their respective compiler. The three setup fixed points,
nine application preflights, complete identities and sizes are in
[tradeoff-identities.json](tradeoff-identities.json); all 180 warmup/retained
rows are in [tradeoff-raw.csv](tradeoff-raw.csv), with unrounded medians,
limits and statuses in [tradeoff-summary.json](tradeoff-summary.json).

| Runtime comparison | Wall ratio | CPU ratio | RSS ratio | Registered runtime criterion |
| --- | ---: | ---: | ---: | --- |
| spectral / frozen, cohort 1 | 0.965287 | 0.977927 | 1.020134 | pass |
| spectral / same-feature main, cohort 1 | 0.968476 | 0.980209 | 1.000000 | fail |
| spectral / frozen, cohort 2 | 0.987201 | 0.984294 | 1.006711 | fail |
| spectral / same-feature main, cohort 2 | 0.983861 | 0.981890 | 1.000000 | fail |
| n-body / frozen | 0.993625 | 0.998898 | 1.000000 | pass |
| n-body / same-feature main | 1.005596 | 0.996651 | 1.000000 | pass |
| fannkuch / frozen | 1.007068 | 1.004224 | 1.011765 | pass |
| fannkuch / same-feature main | 1.000677 | 0.997116 | 1.011765 | pass |

The spectral CPU reduction is 1.57--2.21%, and wall reduction 1.28--3.47%.
This is encouraging but **does not meet the repeated 2% wall-and-CPU criterion**:
three of four cohorts miss it. Do not round 0.980209 down to 0.98 or pool away
the failed cohorts. Every control and every retained 2.0 catastrophic check
passes. Median RSS meets its bound throughout. These are single-process local
Darwin results, not a new formal Linux or Pure Go comparison.

| Own-source compiler comparison | Wall ratio | CPU ratio | RSS ratio | Ordinary time/RSS | Investigation time/RSS |
| --- | ---: | ---: | ---: | --- | --- |
| Candidate / frozen | 0.992742 | 0.996871 | 1.004499 | pass | pass |
| Candidate / same-feature main | 0.944879 | 0.954142 | 1.006127 | pass | pass |

The new cohorts pass both cost budgets. They do **not** cancel the earlier
1.1047821 wall-time failure or establish stable universal self-build gains.
Sources are exact per-role Git snapshots, with each compiler building its own
source; this includes source-volume/shape differences. Different sessions and
non-isolated scheduling produce different observations. This preregistered
diagnostic is not an unchanged-source acceptance retry.

| Compiler artifact | Frozen | Same-feature main | Candidate |
| --- | ---: | ---: | ---: |
| Complete bytes | 332712 | 332728 | 349256 |
| Mach-O text bytes | 233536 | 241600 | 253180 |
| Target-neutral QBE bytes | 1056552 | 1086338 | 1129223 |

Complete compiler growth is 16,528 bytes versus same-feature main and 16,544
versus the frozen baseline (about 4.97% in either case). Text grows by 11,580
and 19,644 bytes respectively; QBE by 42,885 and 72,671. The investigation
size budget passes; ordinary absolute text and QBE limits still fail. All
three application file sizes remain equal across roles: spectral 50,992,
n-body 50,984 and fannkuch 50,960 bytes. Both controls are byte-identical across
all three compilers; spectral differs only between the candidate and the two
byte-identical baseline applications.

Decision: keep the candidate draft and expire this diagnostic budget. Do not
request a larger acceptance envelope on the strength of this small, incompletely
repeated benefit alone, and do not return automatically to size-only polishing.
Next inspect the remaining hot-loop checked arithmetic and the facts needed for
a larger general-purpose MIR benefit. The currently verified Array-read proof
does not authorize removing induction/arithmetic checks; any extension needs a
new bounded registration, independent proof and failure/overflow controls. Keep
the current implementation and failed evidence available for that investigation.
Full recovery, hosted target/process/memory checks, formal full-input runtime
acceptance and matched application build/Go comparisons remain pending. Pages
continues to show the last complete accepted result.

## Subsequent small-gain adoption review

The [adoption review](../../docs/native-mir-loop-bounds-adoption.md) revisits the
decision to require a larger benefit before adoption consideration. The above
diagnostic and every failed threshold remain unchanged; a small reproducible
improvement can still warrant adoption if its maintenance and measured costs
are acceptable. No acceptance limit changes follow automatically.

The recovery-enabled review found indexed compound assignment in output batching
outside the snapshot v4 subset. The corrected spelling preserves cursor behavior
and all three measured application binaries byte-for-byte. The compiler itself
changes: text 253,180 to 253,220 and QBE 1,129,223 to 1,129,392 bytes, complete
compiler 349,256 unchanged. Earlier compiler-time cohorts must not be presented
as measurements of this corrected source.

Corrected candidate `70fe5c0b29560490e4c49a0b5e67d8d14a86fe19` passes the full
97-test root and 152-test compiler suites with recovery/QBE enabled. All thirteen
recovery stages complete, including generation and conformance controls. Both
owned recovery workspaces are removed; the first failed run remains recorded.
[Compact identities and verification outcomes](adoption-review.json) preserve
the corrected application hashes and distinguish each authority.

The [hosted target run](https://github.com/type-rb/type-rb-native/actions/runs/34101454030)
passes Linux amd64. Linux arm64 reaches identical B2/B3/B4 compilers at 319,440
bytes, then fails the 317,000 limit before completing its corpus authority.
The [worker run](https://github.com/type-rb/type-rb-native/actions/runs/34101457007)
passes the Darwin smoke, with 175 collections, all 182,400,576 allocated bytes
reclaimed and final live bytes zero. Linux fails before worker execution at
319,432 stripped bytes against 317,000. Neither is long-running soak evidence.

Worker compiler sizes are 349,296 Darwin and 319,432 Linux, manually totaling
668,728 against 667,000; the combined workflow job is skipped. Their compiler
QBE hashes agree with the local corrected 1,129,392-byte QBE. This manual
identity check does not turn either failed workflow into a pass. Distinct
basename/toolchain artifacts must not be conflated with the local 349,256-byte
compiler. Quick, documentation, tooling and both CLI jobs pass in the
[draft PR run](https://github.com/type-rb/type-rb-native/actions/runs/34101416130);
its acceptance guard correctly fails while required authorities are skipped.

The review finds one localized proof owner, no retained superseded header-only
owner, and moderate maintenance cost from positional rows and central dispatch.
It keeps small-gain adoption eligible, without assuming useful optimizer code
must be free. Before broadening the proof, check large-function scaling and
review responsibility-based structure. Complete the candidate-scoped cost and
repeatability decision before new formal measurement or threshold changes;
original failures remain failures. No additional comparative timing was run
for this checkpoint. Full acceptance and Pages updates remain pending.
