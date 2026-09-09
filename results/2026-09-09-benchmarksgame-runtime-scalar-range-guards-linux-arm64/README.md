# Scalar range guard runtime results on Linux arm64

All 462 retained observations and 84 warmups pass. Native exceeds the pinned
Pure Go implementation on spectral-norm: one-core wall medians are 2.30664
versus 3.21933 seconds, 28.35% less time. CPU medians are 2.30419 versus
3.21303 seconds, 28.29% less. This satisfies the registered spectral-norm
objective; the other two numeric kernels remain slower. It is not general
language parity or a claim about arbitrary Go programs.

## Exact scope and bootstrap

- [Formal run 34329333035](https://github.com/type-rb/type-rb-native/actions/runs/34329333035), attempt 1, three successful jobs.
- Measured Native source `2841cb9311fd0e3e4a6a84e5157745590dbc5765`, accepted in [PR #372](https://github.com/type-rb/type-rb-native/pull/372).
- TypeRB reference `0.4.6-dev@6cbd4025545d44a1de211335f9197772077bb478`.
- Benchmarks Game revision `40296663ed350d5fe4a6ab5e367bab61cb77c219`.
- Three fresh `ubuntu-24.04-arm` runners, each with four Neoverse-N2 logical CPUs.
- QBE 1.3, GCC 13.3.0, LLD 18.1.3, Go 1.27.1 and BenchExec `runexec` 3.35; the complete host/toolchain inventories are retained per case in `context.json`.

The immutable `bootstrap-seed-2026-09-09-record-arrays` supplies setup provenance.
After the setup-only transition, ordinary B2/B3/B4 generations reproduce the
same 329680-byte compiler, SHA-256
`52d92576f5f1601f332eeb4b95bd8585797af1f5d9aa2311fd04f7d8d0760524`.
The 1170832-byte target-neutral compiler QBE has SHA-256
`d9ba3ab9ad8cfae846e212f43908fa8b722f986811089fc3fbd4099403193495`.
All 42 generation observations for these three jobs pass. The reference Go
compiler is a comparison control, not an ordinary regeneration dependency.
Later source changes are not relabelled as this measured compiler.

## Runtime medians

Inputs are fannkuch-redux 12, n-body 50000000 and spectral-norm 5500. Seven
implementations rotate through two warmup and eleven retained rounds in each
of the one-core and four-core lanes. Every complete process includes startup
and any Java JIT activity. Swap is disabled; cache control runs before every
observation. The isolated process tree has a 4 GB memory ceiling. This is not
a persistent-service, steady-state or memory-leak measurement.

| Case | Lane | Native wall | TypeRB Go wall | Pure Go wall | Native / Pure Go |
| --- | --- | --- | --- | --- | --- |
| fannkuch-redux | one-core | 202.325 | 53.6337 | 24.5975 | 8.2254x |
| n-body | one-core | 26.2869 | 7.5405 | 3.60047 | 7.3010x |
| spectral-norm | one-core | 2.30664 | 5.63682 | 3.21933 | 0.7165x |
| fannkuch-redux | four-core | 202.303 | 53.5534 | 24.636 | 8.2117x |
| n-body | four-core | 26.3049 | 7.54039 | 3.59955 | 7.3078x |
| spectral-norm | four-core | 2.3053 | 5.6366 | 3.21846 | 0.7163x |

| Case | Lane | Native CPU | Pure Go CPU | Native peak memory bytes | Pure Go peak memory bytes |
| --- | --- | --- | --- | --- | --- |
| fannkuch-redux | one-core | 202.302 | 24.5893 | 524288 | 2904064 |
| n-body | one-core | 26.2826 | 3.59343 | 524288 | 2899968 |
| spectral-norm | one-core | 2.30419 | 3.21303 | 1220608 | 3952640 |
| fannkuch-redux | four-core | 202.284 | 24.6846 | 524288 | 3694592 |
| n-body | four-core | 26.3016 | 3.60281 | 524288 | 3694592 |
| spectral-norm | four-core | 2.30349 | 3.22199 | 1220608 | 4726784 |

Times are seconds; lower is better. All seven implementations, including C,
C++, Rust and Java, remain in the median tables and the
[benchmark explorer](https://type-rb.github.io/type-rb-native/benchmarks/).
Pure Go uses its separately pinned upstream implementation. Only the TypeRB
Native/Go pair holds authored source and portable semantics constant.
Four-core allocation does not parallelize single-threaded programs; selected
upstream implementations do use multiple cores. Keep the lanes separate.
There is no aggregate language score or energy/power claim.

## Attribution and limitations

The MIR scalar guard's local interleaved Native comparison reduced spectral
wall time by 26.90% against the immediate control, while its two control cases
met their registered bounds. That is separate from this fresh Linux seven-
implementation cohort. Differences between publication dates are not causal
A/B evidence. The [accepted checkpoint](../2026-09-09-scalar-range-guards-accepted-darwin-linux-arm64/README.md)
retains exact local compiler/application identities, the corrected recovery
implementation, all failed approaches and compiler cost acceptance.

N-body and fannkuch remain slower than Pure Go, and the local cumulative
comparison shows large regressions already present in the immediate control.
These are not removed from the refreshed tables. In the previous published
one-core cohort, Native n-body took 10.2644 seconds; it now takes 26.2869
seconds, 2.5610 times as long (156.10% more). Pure Go changed from 3.5998 to
3.60047 seconds. Both cohorts use input 50000000 and eleven retained rounds
on the same named runner class. Dates and compiler/toolchain revisions differ,
so this is a published-result regression comparison, not a controlled attribution
to one change. The local immediate-control comparison above shows that the
regression predates this scalar guard. The subsequent accepted
[assignment-effect improvement](https://github.com/type-rb/type-rb-native/pull/376)
restores n-body and fannkuch generated programs to the cumulative baseline,
with matching local performance. Its
[complete local comparison](https://github.com/type-rb/type-rb-native/issues/354#issuecomment-5603477828)
is separate from this earlier formal cohort; these tables do not substitute
local results for fresh Linux measurements.

Fannkuch-redux likewise increased from the previous published one-core median
of 77.1176 to 202.325 seconds, 2.6236 times as long (162.36% more), at input
12 with eleven retained rounds. Its current Pure Go median is 24.5975 seconds.
The same cross-date attribution limitation applies. Neither regression is
excluded from the published explorer.

Independent checks verify all 546 rows, rotating order, original process
metrics, exit status, cache controls and exact output, along with all untimed
controls. The canonical summarizer reproduces all six median tables byte for
byte. No partial schedule, earlier compiler result or favorable subset is mixed
into this cohort.

## Retained evidence

| Artifact | ID | Original zip bytes | GitHub SHA-256 |
| --- | --- | --- | --- |
| benchmarksgame-runtime-fannkuch-redux | 10101750312 | 392982 | `aefd0b3e25985cb37e2a5f4a597d0622e0122bf8b3d27572d937a1b35eb4db8a` |
| benchmarksgame-runtime-n-body | 10096138929 | 388769 | `76655ce28cd6583b7c5ff042d8bf216353066e6ac7fe51b9776ce355c93f7022` |
| benchmarksgame-runtime-spectral-norm | 10095548659 | 386728 | `8ca77c72a5e6c7c3d732c3023b3c3f19e16cc2f9ae4de6e30aa9cd59bec2acc4` |

All downloaded zip hashes match the GitHub digests. Raw observations, median
tables, source/artifact hashes and distribution tables remain in Git. Text
inventories are consolidated into per-case `context.json` without changing
their contents. `EVIDENCE_SHA256SUMS` inventories the retained machine-readable
working set, not every file in the original artifact.

[ARCHIVE.json](ARCHIVE.json) identifies the freshly downloaded and verified
public archive containing every original extracted file, including observation
output/status/metrics, cache evidence, process traces and application artifacts.
Its `MANIFEST.json` verifies every member's bytes and SHA-256. The archive was
constructed directly from CI artifacts before Git import; `SOURCE.json`
records that provenance and the measured source revision. No raw payload was
temporarily committed to bypass the retention policy. No observation or
outlier was filtered, and the old accepted reports remain available at their
[exact historical revision](https://github.com/type-rb/type-rb-native/tree/a604adcffe0cc34ff217ff84d73911c85ceb0a00/results).

See the [same-revision build cohort](../2026-09-09-benchmarksgame-build-scalar-range-guards-linux-arm64/README.md)
for compiler time, memory, application artifacts and distribution boundaries.
