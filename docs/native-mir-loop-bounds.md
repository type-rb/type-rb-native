# Array-loop bounds proof diagnostic

Status: local ordinary-connection candidate for [issue #303](https://github.com/type-rb/type-rb-native/issues/303),
not an accepted optimization or performance result. The accepted baseline is
`1afd60c2c7257ed34fd2a2aa70cb8b9164433009`. The earlier isolated proof checkpoint
is `98eb48e0261853aec4b03c541eb6617f8995a93e`; this candidate connects its
successor to structured checking, MIR verification and address lowering.

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
copy remains. The obsolete header-only wrapper has been removed, and identical
cold failure-result construction has one shared implementation.

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

The [retained local diagnostic](../results/2026-09-06-mir-loop-bounds-diagnostic-darwin-arm64/README.md)
passes both runtime cohorts with about 2.1–2.3% less spectral-norm wall time.
It is still **not accepted**: the current build wall ratio is 1.0505660577,
above the unchanged 1.05 ceiling. All failed candidate observations remain
retained. Do not round the ratio down or update Pages from this result.

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
