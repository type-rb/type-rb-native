# Formal Benchmarks Game Runtime Results on Linux arm64

The first formal cross-language runtime layer passes its complete correctness,
isolation, repetition, and evidence contract. It also finds a substantial
runtime-performance gap: for these three exact numeric kernels, TypeRB Native
uses far less peak memory and produces a roughly 99% smaller raw application
artifact than the optimized TypeRB Go path, but runs 2.44x to 4.68x slower.

Against the fastest pinned context implementation in the one-core lane,
Native is 7.70x to 10.55x slower. The four-core lane is similar for
single-threaded implementations, while the pinned threaded Rust variants of
`fannkuch-redux` and `spectral-norm` widen the contextual gap to about 30x.
These are implementation results for exact programs, inputs, and toolchains,
not a composite language ranking.

## Exact scope

- measured Native revision:
  `266c996668a4c3e0ad6eb833ca646b73ca7e56e1`;
- TypeRB Go semantic reference:
  `0.4.3-dev@2cf63e95b4fc1a92f6094e2c89c47fb75262adae`;
- Benchmarks Game site version `25.03`, revision
  `40296663ed350d5fe4a6ab5e367bab61cb77c219`, source-archive SHA-256
  `aabcf6726cdc14f0f45b99e5daba48584f94bbb48883fd3711a1d040474d1cb4`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- BenchExec `runexec` 3.35, Debian-package SHA-256
  `b6e42daf63a0284b597f1d05f0daf7690381f7ca9ebe21d0b5083495d01bbfe0`;
- three separate fresh GitHub-hosted `ubuntu-24.04-arm` jobs, each reporting
  four Neoverse-N2 logical CPUs and Linux 6.17; and
- successful formal run
  [33335773466](https://github.com/type-rb/type-rb-native/actions/runs/33335773466).

The self-hosted compiler closed the same 267,264-byte B2/B3/B4 fixed point in
all three jobs, with SHA-256
`7639b7a01bf8b286f86a0067a8592b852bd82433a866a0ee00a37e584dd54b29`.
The setup transitions contain no Go, reference TypeRB compiler, or shell child.

## Correctness and measurement integrity

Each case contains exactly seven candidates in the registered rotation order:
the identical TypeRB source through Native and optimized Go, followed by pinned
C, C++, Go, Rust, and Java implementations. Before timing, every candidate
returned status zero, produced empty stderr, and matched the published
performance-output oracle byte for byte in both lanes.

Each one-core and four-core lane retained all two warmup rounds and eleven
retained rounds, for 91 observations per lane. Across the six lanes, all 84
warmup and all 462 retained observations passed. Every retained candidate has
11/11 successful samples; there are no missing metrics, nonzero exits,
signals, timeouts, output differences, or incomplete medians.

Every process tree ran under BenchExec with a 4 GB limit, explicit CPU IDs,
network disabled by the container policy, `/` read-only, and `/home` isolated
in a non-persistent overlay. Swap was disabled and the Linux page cache was
dropped before every observation. All 546 observation-specific cache,
command, payload, result, status, wall-time, CPU-time, and peak-memory records
are retained.

The checked-in `summarize.awk` was unchanged from the measured revision.
Re-running it independently over every `raw.tsv` reproduces all six retained
`medians.tsv` files byte for byte.

## Primary identical-TypeRB comparison

Times are whole fresh-process medians in seconds. RSS is process-tree peak
memory in bytes. A ratio above 1 means Native is slower.

| Case | Lane | Native wall | Go wall | Native/Go | Native CPU | Go CPU | Native RSS | Go RSS | Native RSS reduction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | one core | 193.352 | 45.9903 | 4.204x | 193.353 | 45.9846 | 524,288 | 3,084,288 | 83.00% |
| fannkuch-redux | four core | 194.201 | 46.1221 | 4.211x | 194.207 | 46.2458 | 524,288 | 3,899,392 | 86.55% |
| n-body | one core | 28.8874 | 6.17209 | 4.680x | 28.8818 | 6.16454 | 524,288 | 3,022,848 | 82.66% |
| n-body | four core | 28.9154 | 6.17493 | 4.683x | 28.9087 | 6.18657 | 524,288 | 3,801,088 | 86.21% |
| spectral-norm | one core | 13.7670 | 5.63428 | 2.443x | 13.7653 | 5.62850 | 1,216,512 | 6,934,528 | 82.46% |
| spectral-norm | four core | 13.7652 | 5.63817 | 2.441x | 13.7589 | 5.64438 | 1,216,512 | 7,864,320 | 84.53% |

The primary retained wall-time ranges are narrow and do not explain the gap:

| Case | Lane | Native retained min-max | Go retained min-max |
| --- | --- | ---: | ---: |
| fannkuch-redux | one core | 193.268731-194.287106 | 45.789742-46.428841 |
| fannkuch-redux | four core | 193.257109-194.432484 | 45.722742-46.400051 |
| n-body | one core | 28.859849-28.915869 | 6.169444-6.175781 |
| n-body | four core | 28.853045-29.008898 | 6.171387-6.182868 |
| spectral-norm | one core | 13.757161-13.772178 | 5.632719-5.649705 |
| spectral-norm | four core | 13.756140-13.771266 | 5.631778-5.648930 |

The same authored TypeRB source and published output are used by both paths.
The difference is therefore a backend/runtime implementation result, not a
different algorithm or benchmark-specific semantic relaxation.

## Cross-language implementation context

The following tables contain medians for the exact pinned context programs.
They are not an intrinsic ordering of languages. Some upstream programs use
threads; the separate four-core lane deliberately preserves that authored
behavior.

### Wall time in seconds

| Case | Lane | TypeRB Native | TypeRB Go | C | C++ | Go | Rust | Java |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | one core | 193.352 | 45.9903 | 27.4815 | 24.9730 | 24.5942 | 24.8688 | 24.4682 |
| fannkuch-redux | four core | 194.201 | 46.1221 | 27.4797 | 24.9772 | 24.6680 | 6.30883 | 23.9841 |
| n-body | one core | 28.8874 | 6.17209 | 2.97637 | 2.73763 | 3.59968 | 3.50754 | 5.06426 |
| n-body | four core | 28.9154 | 6.17493 | 2.97606 | 2.73734 | 3.60070 | 3.51001 | 5.00111 |
| spectral-norm | one core | 13.7670 | 5.63428 | 1.78764 | 1.83909 | 3.21757 | 1.79822 | 1.92955 |
| spectral-norm | four core | 13.7652 | 5.63817 | 1.78711 | 1.83844 | 3.21887 | 0.460849 | 1.89495 |

### CPU time in seconds

| Case | Lane | TypeRB Native | TypeRB Go | C | C++ | Go | Rust | Java |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | one core | 193.353 | 45.9846 | 27.4799 | 24.9716 | 24.5899 | 24.8662 | 24.4314 |
| fannkuch-redux | four core | 194.207 | 46.2458 | 27.4777 | 24.9762 | 24.7323 | 24.8237 | 23.9794 |
| n-body | one core | 28.8818 | 6.16454 | 2.97374 | 2.73444 | 3.59345 | 3.50477 | 5.00167 |
| n-body | four core | 28.9087 | 6.18657 | 2.97370 | 2.73491 | 3.60522 | 3.50698 | 4.95774 |
| spectral-norm | one core | 13.7653 | 5.62850 | 1.78541 | 1.83695 | 3.21295 | 1.79503 | 1.88695 |
| spectral-norm | four core | 13.7589 | 5.64438 | 1.78543 | 1.83678 | 3.22089 | 1.80067 | 1.88132 |

Rust's four-core wall time for two threaded variants falls while its CPU time
remains near the one-core value. That is expected parallel implementation
context and is not a backend-pair comparison.

### Peak RSS in MiB

| Case | Lane | TypeRB Native | TypeRB Go | C | C++ | Go | Rust | Java |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | one core | 0.50 | 2.94 | 0.50 | 0.65 | 2.52 | 1.15 | 47.31 |
| fannkuch-redux | four core | 0.50 | 3.72 | 0.50 | 0.65 | 3.41 | 1.90 | 49.25 |
| n-body | one core | 0.50 | 2.88 | 0.50 | 0.64 | 2.51 | 0.91 | 46.48 |
| n-body | four core | 0.50 | 3.63 | 0.50 | 0.67 | 3.27 | 0.91 | 48.20 |
| spectral-norm | one core | 1.16 | 6.61 | 0.66 | 0.65 | 3.52 | 1.38 | 47.73 |
| spectral-norm | four core | 1.16 | 7.50 | 0.66 | 0.66 | 4.25 | 1.88 | 49.77 |

## Raw application artifacts

These are unstripped application artifacts prepared for the runtime run. Java
is the sum of the retained application class files. These values do not include
required runtime or toolchain distributions.

| Case | TypeRB Native | TypeRB Go | C | C++ | Go | Rust | Java classes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | 18,480 | 2,808,692 | 70,648 | 70,912 | 2,381,555 | 4,664,888 | 3,839 |
| n-body | 22,328 | 2,815,362 | 70,856 | 71,336 | 2,382,167 | 4,651,312 | 4,019 |
| spectral-norm | 18,808 | 2,809,898 | 70,696 | 71,952 | 2,382,139 | 4,673,736 | 1,428 |

The Native artifact is 99.34%, 99.21%, and 99.33% smaller than its matching
TypeRB Go artifact for the three cases, respectively. A later formal build
layer must still record stripped size, compiler time and RSS, shared libraries,
linkers, generators, language runtimes, and complete distribution size.

## Retained evidence and independent audit

GitHub published these exact archives:

| Artifact | ID | Archive bytes | GitHub SHA-256 |
| --- | ---: | ---: | --- |
| benchmarksgame-runtime-fannkuch-redux | 9741303668 | 392,359 | `6d00613983a413469ded782a321bad05c80087fea3e294f1abc32a35c0118b17` |
| benchmarksgame-runtime-n-body | 9739357920 | 388,088 | `38f265c32dd1cde243de698ca630529712b01cca84c1f7d60f80255efcd76139` |
| benchmarksgame-runtime-spectral-norm | 9739204857 | 386,152 | `9e5292ea082e5de400c3c6e79df33a2047ce8ab4159cea75a50bc1f2cb094c1c` |

The result retains all 4,134 extracted raw files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 4,135 files and excludes only this README
and itself.

- Each [`workflow-evidence`](benchmarksgame-runtime-fannkuch-redux/workflow-evidence)
  tree records exact revisions, runner, kernel, CPU, toolchains, packages,
  release metadata, and pinned archive hashes.
- Each [`prepare-evidence`](benchmarksgame-runtime-fannkuch-redux/prepare-evidence)
  tree records the complete seven-candidate catalog, correctness, source,
  commands, toolchains, artifact sizes, and artifact hashes.
- Each one-core and four-core tree retains
  [`raw.tsv`](benchmarksgame-runtime-fannkuch-redux/one-core-evidence/raw.tsv),
  [`medians.tsv`](benchmarksgame-runtime-fannkuch-redux/one-core-evidence/medians.tsv),
  pre-timing correctness, environment, and all 91 observation directories.

## Conclusion and remaining work

The runtime controller and self-hosted chain are reliable enough to expose an
unfavorable result without losing the Native implementation's size and memory
advantages. The small startup-dominated Gate 6N application result does not
generalize to these long numeric kernels: generated-code and runtime
optimization remain material work before Native can claim Go-equivalent
runtime performance.

The next optimization work should be driven by profiles of these exact
portable programs and must preserve their output, self-hosted fixed point, and
general language behavior. This result alone does not identify one safe cause
or authorize benchmark-specific intrinsics.

Issue [#103](https://github.com/type-rb/type-rb-native/issues/103) remains
open. Its separate formal build layer still needs compiler wall/CPU/RSS,
stripped artifacts, linker/generator/shared-library boundaries, and complete
runtime/toolchain distribution inventories. Persistent Web and Job behavior
remains a different workload under
[issue #104](https://github.com/type-rb/type-rb-native/issues/104).
