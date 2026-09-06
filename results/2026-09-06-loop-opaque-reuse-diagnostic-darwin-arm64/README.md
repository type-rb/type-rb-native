# Repeated opaque-row allocation diagnostic

Status: **not accepted**. The combined candidate still fails the unchanged
build-cost limits for [issue #303](https://github.com/type-rb/type-rb-native/issues/303).
It remains unfinished engineering work, not a merge or Pages authority.

The candidate combines the preceding
[proof-result refactoring](../2026-09-06-loop-proof-result-diagnostic-darwin-arm64/README.md)
with reuse of an already opaque producer row. A first opaque effect still
replaces the prior projection; later effects update only its latest origin.
Subsequent candidate operations remain suppressed. No effect is reclassified,
and the verifier still validates all row fields before granting a proof.

The exact patch applies to `ad7cd377c061bc25f3eea7b68fb57a855b180f1d`, including
readonly-binding correction PR #306. The frozen baseline remains
`1afd60c2c7257ed34fd2a2aa70cb8b9164433009`.

| Ordinary build metric | Baseline median | Candidate median | Ratio |
| --- | ---: | ---: | ---: |
| Wall (s) | 1.5061125 | 1.584054917 | 1.0517507271 |
| CPU (s) | 1.488797 | 1.566238 | 1.0520158222 |
| Root RSS (bytes) | 40206336 | 40124416 | 0.9979625102 |

Two warmups and seven retained observations per role are interleaved. All 18
builds reproduce their exact-source compiler. Both roles pass every retained
2.0 catastrophic check. Wall and CPU miss 1.05; memory passes. Differences
between separate failed batches do not establish a runtime ranking.

B2/B3/B4 SHA256:
`cab53295394482523f0bb881ea525fdc82192dbbd3bc2faffcf24821cef9a4b5`.
Complete compiler: 349256 bytes; Mach-O text: 248004 bytes; target-neutral
compiler QBE: 1110541 bytes. The full compiler suite passes 134 tests, including
the repeated-effect regression; the focused proof/connection suite passes 20.
All 75 corpus cases pass at B2/B3/B4 (225 rows), with exact invalid diagnostics,
no tool launch for invalid builds, repeated/adjacent QBE identity, expected
runtime failures and no temporary residue. The three numeric benchmark QBE
outputs equal the previous outlined candidate's outputs. Current full root
recovery, cross-target and hosted performance acceptance remain pending.

The unchanged [build observer](../2026-09-06-mir-loop-bounds-diagnostic-darwin-arm64/build-cost-observer.py)
uses monotonic wall time and wait4 CPU/orchestration-root RSS. Each compiler
builds its own canonical source closure with QBE 1.3, `/usr/bin/cc` and
`darwin-arm64-v0`. Owned correctness processes finished before measurement.
Host: Apple M2 Pro, 10 logical CPUs, 32 GiB RAM, macOS 26.6.2; Apple clang
21.0.0 (clang-2100.1.1.101); reference revision
`5dc09070cf7f88a569279f5e63982a6de59d692c`. Warm caches, no CPU affinity,
controlled frequency, or host-wide isolation.

## Separate source-volume diagnostic

The crossed check/emit observations use each compiler on both source closures.
They are not ordinary fixed-point builds or an acceptance retry. The observer
takes baseline compiler, candidate compiler, baseline entry, candidate entry,
and a new output directory as positional arguments. It retains two warmups and
seven observations per cell, rotates/reverses cell order, and verifies status,
empty stderr and repeated per-cell stdout hashes. `check` must print `ok`.
Different compiler/source cells need not emit identical QBE.

| Stage | Compiler | Source | Median wall (s) |
| --- | --- | --- | ---: |
| Check | Baseline | Baseline | 0.373104666 |
| Check | Baseline | Candidate | 0.392128417 |
| Check | Candidate | Baseline | 0.380297875 |
| Check | Candidate | Candidate | 0.394467916 |
| Emit QBE | Baseline | Baseline | 0.593793375 |
| Emit QBE | Baseline | Candidate | 0.626092458 |
| Emit QBE | Candidate | Baseline | 0.599457625 |
| Emit QBE | Candidate | Candidate | 0.629984375 |

On candidate source, changing compiler adds about 0.60% check / 0.62% emit wall
time in this diagnostic. With the baseline compiler fixed, changing source adds
about 5.10% / 5.44%. This suggests source-volume and source-shape work is a larger
component than the new analysis's execution overhead in these stages. It does
not isolate individual functions, separate parsing from checking, or explain
assembly/link time. These medians are not a statistical significance claim.
Follow-up should target duplicate compiler/projection code and obtain finer
phase evidence, rather than retrying unchanged near-threshold builds.

The allocation files are separate, untimed `check` observations of the same
candidate source under `TYPE_RB_NATIVE_RUNTIME_STATS=1`. `control` is the
proof-result-only compiler d896b323; `candidate` is cab53295; `frozen-baseline`
is the compiler at 1afd60c2. Reusing the opaque row reduces cumulative managed
allocation from 252008640 to 251239200 bytes (769440 bytes, about 0.3%). All
three report zero final live bytes for this invocation, not universal leak
freedom. Peak managed heap does not improve (7508297 to 7568972 bytes).
The small allocation reduction alone does not establish a meaningful speedup.
