# Array-loop bounds proof diagnostic

Status: local ordinary-connection candidate for [issue #303](https://github.com/type-rb/type-rb-native/issues/303),
not an accepted optimization or performance result. The accepted baseline is
`1afd60c2c7257ed34fd2a2aa70cb8b9164433009`. The earlier isolated proof checkpoint
is `98eb48e0261853aec4b03c541eb6617f8995a93e`; this candidate connects its
successor to structured checking, MIR verification and address lowering.

## Current integration checkpoint

The draft now integrates accepted main `3ae51bbf`, including independent Boolean
support from #317, its REPL unary-precedence correction, the exact reference
`47a160cae05ddc2035c7430735c4762d36bbc9c4`, and current CI/retention policy.
This integration is not a passing cost result. The original frozen baseline
above and every earlier rejection remain binding. Revalidate the complete
source before measuring a source-distinct compiler-cost reduction.

Superseded diagnostic folders are no longer part of the active checkout.
The pinned historical links below retain their full observations and patches;
no raw observations are selected out of a published measurement cohort.
The [output-batching checkpoint](../results/2026-09-07-array-loop-output-batching-darwin-arm64/README.md)
passes local compiler time/RSS selection: wall 1.0177125, CPU 1.0226662 and
RSS 1.0016293 versus the unchanged frozen baseline. Its integrated control
fails at wall 1.0784632 and CPU 1.0772980. These are separate frozen-baseline
cohorts, not a direct same-run percentage gain between control and batching.

The subsequent immutable instruction-field cleanup reduces compiler QBE from
1,132,120 to 1,129,223 bytes and Mach-O text from 254,468 to 253,180 bytes.
The candidate is still not accepted: both remain above the existing
1,120,000/250,904 ceilings. Every verifier predicate and diagnostic remains.
Integration already exceeded both ceilings before batching. The complete
349,256-byte compiler remains within its absolute limit, but file alignment
does not waive section/QBE bounds. All 81 corpus QBE/diagnostic outputs remain
identical to the integrated control, and ordinary core/CLI fixed points and
CLI regressions pass for the batching checkpoint; the field cleanup repeats
core/CLI fixed points and all 81 exact corpus comparisons and passes 152 compiler
tests without recovery. Next reduce compiler/projection representation before
full recovery and hosted acceptance; do not dispatch long runtime acceptance
while these cost bounds fail.

The named-field candidate's separate frozen-baseline cohort fails wall time at
1.1047821, while CPU 1.0374060 and RSS 1.0004095 pass. All 18 ordinary builds
reach fixed points and retained values pass the 2.0 catastrophic bound. Keep
the failed cohort; the earlier batching timing pass does not transfer to this
source, and the current candidate still needs size and time improvement.

## Proof boundary

The diagnostic verifies a structured projection of an already checked function.
It derives candidate read origins from immutable Array identity, a zero-origin
Integer induction value, a dominating strict length guard, and exactly one
checked unit increment. It does not accept supplied optimization facts. The
ordinary checked arithmetic, including the induction increment, remains
required even for a selected read.

Each operation has six Integer cells: kind, binding, operand, input version,
region, and source origin. Definitions have distinct identities, independent of
authored names or reusable local slots. Origins are strictly increasing. Region
entry/exit is structured and must balance; nested reads may use an ancestor
guard only for the same Array, index, and pre-update version.

| Kind | Meaning | Operand |
| --- | --- | --- |
| 1 | Parameter | 0 other, 1 immutable Array, 2 mutable Array |
| 2 | Integer definition | Zero, or a conservative nonzero/unknown value |
| 3 | Strict index less than Array length loop | Array identity |
| 4 | Array read | Index identity |
| 5 | Checked unit increment | 1 |
| 6 | Unknown Integer write | 0 |
| 7 | Loop close | Array identity |
| 8 | Opaque control or effect | 0 |
| 9 | Array access without an identified index binding | 0 |
| 10 | Optimized Array read | Index identity |
| 11 | Unproved loop shape, blocking bounds but not header reuse | 0 |

The verifier returns `[-1]` for malformed input or `[0, read origins...]` for a
verified stream, possibly without any selected reads. Mutable Arrays, nonzero
initializers, reads after an update, missing or repeated increments, and
unproved effects remain conservative. Input rows are not mutated.

Index writes invalidate closed regions too: a later write inside an enclosing
loop may affect the next invocation of an inner loop. Checking only the active
region stack would not cover that case. Conversely, malformed input must still
be rejected after an opaque event; disabling optimization is not permission to
stop structural verification.

The producer records unsupported conditionals, unproved calls, growth, and
uncertain aliases as opaque. An unproved loop shape blocks bounds selection
without discarding the independently valid immutable-parameter header. This
projection cannot detect an effect omitted by its producer. It is therefore not an independent
authorization to remove a source-level bounds check.

## Ordinary connection

The existing per-function `array_regions` owns the raw six-cell rows directly;
there is no second permanent region or bounds-fact table. Parameters use their
ordinal, while Integer declarations use distinct source-token identities.
Source checking resolves each use in its live scope before recovering that
declaration identity, so a reused local slot cannot inherit an earlier proof.
The producer's row objects pass directly to this owner; no flatten/reconstruct
copy remains. The obsolete header-only wrapper has been removed. The current
diagnostic separates Boolean verification completion from result publication,
so structural failures do not each return a managed result. An already opaque
producer row is reused while retaining its latest origin; its verification and
conservative effect classification are unchanged.

Checked values carry explicit `loop_index` and `loop_array` operands, separate
from their source origin, scalar MIR value, callable category and mutability.
A strict Integer comparison propagates the index and Array-length relationship.
Other expressions do not silently inherit it. Shared constructors preserve this
boundary within the narrower recovery snapshot's supported source subset.

The optimizer changes only selected kind-4 reads to kind 10. The MIR verifier
recomputes the selection and rejects supplied, missing, forged or stale marks.
After complete verification, non-scalar functions publish those read origins
through the existing source-indexed lowering-plan storage. That selected subset
replaces its older normalization-only metadata. The adapter consumes a verified
mode and performs address arithmetic without reconstructing the guard or
binding relationship. All other accesses keep their checked lowering; an
independently shorter output Array never inherits the input Array's proof.

Recovery includes the new responsibility-named module in its strict canonical
closure, flattened source, regenerated file set and snapshot preflight. The
ordinary path continues to load the real imported source closure.

## Local verification boundary

The proof-core suite includes 13 focused tests and 252 single-field boundary
mutations. Connection tests exercise actual checked source, changed indices,
extended and unrelated bounds, aliases, opaque calls, and forged optimized
marks. Executable corpus controls include empty/singleton inputs, nested loops,
local-slot reuse with negative indexing, a shorter output, and checked overflow.
The suite checks malformed rows, stale identities and versions, nesting,
post-update accesses, conservative
effects, input preservation, and repeatability:

```sh
trb fmt --check compiler/src/mir_loop_bounds.trb compiler/src/mir_loop_bounds_test.trb
trb check --config compiler/trbconfig.jsonc
trb test --config compiler/trbconfig.jsonc --test-name-pattern 'MIR Array loop proof core'
```

These focused checks are not the recovery-enabled full compiler/root suites,
ordinary replacement fixed points, cross-target evidence, or runtime acceptance.

## Remaining acceptance

The [retained local diagnostic](https://github.com/type-rb/type-rb-native/blob/ba065229c96555cc968c3ed8e6797ce91991afa7/results/2026-09-06-mir-loop-bounds-diagnostic-darwin-arm64/README.md)
passes both runtime cohorts with about 2.1–2.3% less spectral-norm wall time.
It is still **not accepted**: that outlined candidate's build wall ratio is 1.0505660577,
above the unchanged 1.05 ceiling. All failed candidate observations remain
retained. Do not round the ratio down or update Pages from this result.

Two later local cost refinements were also rejected and reverted:
[conservative-stream workspaces](https://github.com/type-rb/type-rb-native/blob/ba065229c96555cc968c3ed8e6797ce91991afa7/results/2026-09-06-mir-loop-workspace-diagnostic-darwin-arm64/README.md)
and [checked postfix copies](https://github.com/type-rb/type-rb-native/blob/ba065229c96555cc968c3ed8e6797ce91991afa7/results/2026-09-06-checked-postfix-copy-diagnostic-darwin-arm64/README.md).
Their full observations and source patches are retained; the additional
malformed-stream and checked-value ownership tests remain. Neither changes
the current compiler implementation or the frozen comparison baseline.
The restored production closure at that checkpoint reproduced the prior compiler
bytes and passed 131 compiler tests, including the additional boundary tests.

The subsequent candidates integrate the readonly-binding correction from PR #306
without moving the frozen baseline. Its
[proof-result-only diagnostic](https://github.com/type-rb/type-rb-native/blob/ba065229c96555cc968c3ed8e6797ce91991afa7/results/2026-09-06-loop-proof-result-diagnostic-darwin-arm64/README.md)
misses the build limits. The subsequent
[opaque-row reuse diagnostic](https://github.com/type-rb/type-rb-native/blob/ba065229c96555cc968c3ed8e6797ce91991afa7/results/2026-09-06-loop-opaque-reuse-diagnostic-darwin-arm64/README.md)
passes 134 compiler tests and 75 corpus cases at B2/B3/B4, but still misses wall
and CPU limits at 1.0517507271 and 1.0520158222. That remains a failed cost result,
not an accepted optimization. Its three numeric application QBE outputs are
unchanged; no new runtime or Pure Go claim is made.

Crossed compiler/source measurements suggest that added source volume and shape
account for more of the check/emit overhead than the implementation change on
fixed source. The allocation reduction is measured but small. Next reduce
duplicate compiler/projection code and obtain finer phase evidence; do not
rerun an unchanged near-threshold candidate or relax a limit. Current-source
full root recovery and hosted cross-target acceptance remain pending.

The subsequent [plan-fusion diagnostic](https://github.com/type-rb/type-rb-native/blob/ba065229c96555cc968c3ed8e6797ce91991afa7/results/2026-09-07-loop-plan-fusion-darwin-arm64/README.md)
combines ordinal validation and header selection with structural verification,
removing two separate row scans and moving a test-only wrapper out of production.
The optimizer and final verifier still independently derive their plans.
It passes 148 compiler tests, 95 root units and 243 ordinary corpus observations;
1530 old/new planner mutations agree. Compiler QBE and text shrink, but wall
1.0577499943 and CPU 1.0554374884 still miss the unchanged 1.05 limit.
This is a retained draft simplification, not accepted performance evidence.

The [single-construction checked binding checkpoint](https://github.com/type-rb/type-rb-native/blob/ba065229c96555cc968c3ed8e6797ce91991afa7/results/2026-09-07-checked-binding-construction-darwin-arm64/README.md)
now passes the local build-cost prefilter: wall 1.0472902709, CPU 1.0446608988,
RSS 0.9995921697. It removes duplicate construction sites without changing
checked metadata or generated numeric application QBE. Its compiler suite
passes 135 tests, with 225 corpus observations and exact B2/B3/B4 compiler
bytes. This is not complete acceptance: source is frozen for joined recovery
and formal target/runtime checks. The manual `array-loop-bounds` contract and
same-head frozen-baseline compiler comparison are described in the
[runtime controller guide](../tools/native-runtime-ab/README.md).

The first hosted compiler comparison at `1adc9377d5e729bd1047e22b89ab3f8128d68299`
([run 34064721027](https://github.com/type-rb/type-rb-native/actions/runs/34064721027))
rejects this candidate: Linux build wall time is 1.060729 of the frozen baseline,
above 1.05; Darwin passes at 1.039886. Both compiler-size ratios pass. Linux
stops at the failed build comparison, so its later comparisons and the combined
authority are incomplete. Do not replace this failure with the local pass.
The full local recovery suites subsequently pass 95 root and 135 compiler tests.
The first runtime dispatch fails during test setup, before any measurements;
no runtime acceptance or Pages update results. The next bounded cost reduction
will avoid constructing unused two-character lexer symbols, with exhaustive
symbol recognition and tokenization controls before new cost measurements.

The [lexer-symbol construction checkpoint](https://github.com/type-rb/type-rb-native/blob/ba065229c96555cc968c3ed8e6797ce91991afa7/results/2026-09-07-lexer-symbol-construction-darwin-arm64/README.md)
passes 138 compiler tests and 225 corpus observations, preserves numeric
application QBE, and passes the local cost prefilter (wall 1.0452087228, CPU
1.0465555100, RSS 1.0032599837). Its source differs from the rejected hosted
candidate; the earlier failure remains recorded. The margin is small, so first
run the frozen-baseline hosted compiler comparison before another long recovery
or runtime batch. This ordering does not waive any merge acceptance checks.

The [hosted lexer refinement](https://github.com/type-rb/type-rb-native/blob/ba065229c96555cc968c3ed8e6797ce91991afa7/results/2026-09-07-lexer-symbol-hosted-cost-rejection/README.md)
also fails the unchanged build limit: Darwin 1.050992, Linux 1.057471. The
long recovery/runtime batches were not dispatched. Keep both source-distinct
failures; next obtain finer compiler phase evidence and reduce the representation
within the supported Native source subset. A Boolean-OR guard grouping cannot
bootstrap under that subset and was reverted before publication. No limit,
language capability, acceptance result or Pages snapshot changes.

1. Complete executable differential controls, recovery, ordinary fixed points,
   target/process/memory authorities and the registered compiler cost bounds.
   Measure the smallest complete candidate before hosted performance acceptance.
2. Retain all same-run spectral-norm and control observations. A successful
   proof-core test does not establish an application speedup or Pure Go parity;
   Pages changes require complete accepted measurements.

The [pre-timing registration](https://github.com/type-rb/type-rb-native/issues/303#issuecomment-5559049058)
requires spectral-norm wall and CPU medians at most 0.98 of the baseline at
input 5500. The two numeric controls remain at most 1.02; median memory remains
at most 1.05, with every retained observation subject to the 2.0 catastrophic
bound. Local selection uses two independent cohorts of two warmups and seven
retained observations per role. Hosted acceptance retains the existing full
formal observation schedule. Compiler, build and RSS ratios remain at most
1.05 and all absolute transition ceilings are unchanged.

No compiler allowance, benchmark condition, supported language feature, or
existing acceptance threshold changes at this checkpoint.
