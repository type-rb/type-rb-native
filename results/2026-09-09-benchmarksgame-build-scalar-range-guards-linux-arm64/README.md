# Scalar range guard build results on Linux arm64

All 66 retained builds and 12 warmups pass. For the three identical authored
TypeRB sources, Native uses 33.9% to 40.7% of TypeRB Go's build wall time and
15.5% to 16.8% of its compiler CPU time. This is a backend build comparison,
not compilation of handwritten Pure Go programs or an application runtime claim.

## Exact scope and bootstrap

- [Formal run 34329336652](https://github.com/type-rb/type-rb-native/actions/runs/34329336652), attempt 1, three successful jobs.
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

## Measurements

Times are median seconds; memory and artifacts are bytes. The two backends
alternate through two warmup and eleven retained rounds with warm compiler
caches, clean output paths, cache reset, fixed CPU allocation, 4 GB memory
ceiling and process isolation. Untimed output checks use inputs 7, 1000 and
100 for fannkuch-redux, n-body and spectral-norm respectively.

| Case | Native wall | TypeRB Go wall | Native CPU | TypeRB Go CPU | Native peak memory | TypeRB Go peak memory |
| --- | --- | --- | --- | --- | --- | --- |
| fannkuch-redux | 0.150834 | 0.44473 | 0.053791 | 0.329522 | 78004224 | 160837632 |
| n-body | 0.210298 | 0.516784 | 0.07017 | 0.417461 | 78135296 | 162930688 |
| spectral-norm | 0.172223 | 0.443142 | 0.057264 | 0.368824 | 78213120 | 161292288 |

All 78 raw rows match their original process metrics, successful exit status,
empty diagnostics and exact application output. The canonical summarizer
reproduces all median tables byte for byte. Warmups remain in the raw tables
but do not enter medians. Cross-date changes do not isolate optimization effects.

| Case | Native raw median | TypeRB Go raw median | Native stripped | TypeRB Go stripped |
| --- | --- | --- | --- | --- |
| fannkuch-redux | 19288 | 2810092 | 19280 | 1887832 |
| n-body | 23104 | 2817378 | 23096 | 1887832 |
| spectral-norm | 19808 | 2810658 | 19800 | 1887832 |

Every Native case has one byte-identical application across eleven retained
builds. Each TypeRB Go case has eleven correct variants; all are counted.
All twelve archived raw/stripped representative binaries match their recorded
size and hash. These application sizes do not represent complete distributions.

## Distribution boundary

| Controlled payload | Raw bytes | Alternate form | Bytes |
| --- | ---: | --- | ---: |
| Native compiler plus QBE | 1044320 | Both stripped | 676904 |
| Reference compiler plus complete Go root | 276002107 | Stripped compiler, unchanged Go root | 265589917 |

The Native C driver, assembler, linker, dynamic loader and shared libraries
remain explicit platform prerequisites. Process/dependency inventories retain
their roles. This is not a complete operating-system or SDK distribution.
Go tools remain included in the reference backend's observed build closure.

## Retained evidence

| Artifact | ID | Original zip bytes | GitHub SHA-256 |
| --- | --- | --- | --- |
| benchmarksgame-build-fannkuch-redux | 10095181742 | 2508284 | `dcaf07dae26c245f6d40d17f85aaa73d29b45dc1c6d59cad961ae44e5d4b550b` |
| benchmarksgame-build-n-body | 10095181658 | 2525010 | `805711393e07244daa2c5f8eaff9ea0875b175b68e4ec31651b386e82409c4ed` |
| benchmarksgame-build-spectral-norm | 10095197957 | 2509151 | `be82150861cae15d3cadf818140f47446c8ad5ada46bd08834aca1abff0022d7` |

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

See the [same-revision runtime cohort](../2026-09-09-benchmarksgame-runtime-scalar-range-guards-linux-arm64/README.md)
for the separate Pure Go execution comparison.
