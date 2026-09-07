# Array-loop batching and verifier-size diagnostic

Not accepted. The current named-field verifier candidate reduces compiler QBE
and text but still exceeds both absolute limits and misses local build wall time.
The earlier batching-only cohort passes local time/RSS, not absolute size.
The Array runtime benefit, full recovery and hosted authorities remain unverified
for the current source. There is no Pure Go or Pages performance claim.

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
