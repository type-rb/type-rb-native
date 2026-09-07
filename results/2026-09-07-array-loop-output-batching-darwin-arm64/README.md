# Array-loop output-batching diagnostic

Not accepted. The output-batching candidate passes local compiler time/RSS
selection but exceeds the unchanged absolute compiler QBE and text limits.
The Array runtime benefit, full recovery and hosted authorities remain unverified
for this exact candidate. There is no Pure Go or Pages performance claim.

## Identities and scope

The fixed comparison remains `1afd60c2c7257ed34fd2a2aa70cb8b9164433009`.
Integrated control `1e4ace11` includes accepted main `3ae51bbf`, exact reference
`47a160cae05ddc2035c7430735c4762d36bbc9c4`, Boolean support and current
retention/CI policy. It is not a new acceptance baseline. Candidate
[source hashes](source-identities.json) identify only the subsequent bounded
QBE stdout batching change and its tests; application semantics are unchanged.
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
