# Formal Safe-Array-Header Runtime Results on Linux arm64

The accepted self-hosted Native compiler passes the complete formal runtime
correctness, isolation, repetition, and evidence contract on all three
registered numeric kernels. Relative to the preceding complete snapshot,
Native wall time improved by 8.82% for `fannkuch-redux` and 28.74% for
`n-body`; `spectral-norm` remained neutral within 0.02%.

A material runtime gap remains. For these exact identical-TypeRB programs,
Native is 1.48x to 2.19x slower than the optimized TypeRB Go path. Against the
separately pinned Pure Go implementations, Native is 2.59x to 4.09x slower.
These are implementation results for exact programs, inputs, and toolchains,
not a composite language ranking. Pure Go parity or better remains the minimum
Native runtime objective.

## Exact scope

- measured Native revision:
  `473a6dee19b637a3009937d9b288c3a91f429a6b`;
- TypeRB Go semantic reference:
  `0.4.4-dev@5dc09070cf7f88a569279f5e63982a6de59d692c`;
- Benchmarks Game site version `25.03`, revision
  `40296663ed350d5fe4a6ab5e367bab61cb77c219`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- BenchExec `runexec` 3.35, TypeRB Go 0.4.4-dev, Go 1.27.0, Rust
  1.98.0, GCC 13.3.0, Clang 18.1.3, OpenJDK 17.0.20, and QBE 1.3;
- three separate fresh GitHub-hosted `ubuntu-24.04-arm` jobs, each reporting
  four Neoverse-N2 logical CPUs and Linux 6.17; and
- successful formal run
  [33505024195](https://github.com/type-rb/type-rb-native/actions/runs/33505024195).

The self-hosted compiler closed the same 254,960-byte B2/B3/B4 fixed point in
all three jobs, with SHA-256
`65b18c8999e91dbb67e7dabb5d731987daa32076c9e4cd709962dc4b49bb73cb`.

## Correctness and measurement integrity

Each case contains exactly seven candidates: the identical TypeRB source
through Native and optimized Go, followed by pinned C, C++, Go, Rust, and Java
implementations. Before timing, every candidate returned status zero, produced
empty stderr, and matched the published performance-output oracle byte for byte
in both lanes.

Each one-core and four-core lane retained all two warmup rounds and eleven
retained rounds. Every process tree ran under BenchExec with explicit CPU,
memory, filesystem, network, cache, and process-closure controls. The complete
raw observations and generated medians are retained below.

## Primary identical-TypeRB comparison

Times are whole fresh-process medians in seconds. RSS is process-tree peak
memory in bytes. A ratio above 1 means Native is slower.

| Case | Lane | Native wall | Go wall | Native/Go | Native CPU | Go CPU | Native RSS | Go RSS | Native RSS reduction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | one core | 100.755 | 46.0809 | 2.186x | 100.745 | 46.0729 | 524,288 | 3,031,040 | 82.70% |
| fannkuch-redux | four core | 100.739 | 46.0605 | 2.187x | 100.729 | 46.1806 | 524,288 | 4,001,792 | 86.90% |
| n-body | one core | 13.2462 | 6.17322 | 2.146x | 13.2434 | 6.16531 | 524,288 | 3,215,360 | 83.69% |
| n-body | four core | 13.2575 | 6.17396 | 2.147x | 13.2547 | 6.18305 | 524,288 | 3,805,184 | 86.22% |
| spectral-norm | one core | 8.32536 | 5.63768 | 1.477x | 8.32194 | 5.63098 | 1,216,512 | 6,938,624 | 82.47% |
| spectral-norm | four core | 8.32395 | 5.63691 | 1.477x | 8.32118 | 5.64857 | 1,212,416 | 7,979,008 | 84.80% |

## Cross-language implementation context

The following values are wall-time medians for the exact pinned programs. They
are not an intrinsic ordering of languages. Some upstream programs use threads;
the separate four-core lane preserves that authored behavior.

| Case | Lane | TypeRB Native | TypeRB Go | C | C++ | Go | Rust | Java |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | one core | 100.755 | 46.0809 | 27.4883 | 24.9627 | 24.6214 | 24.8713 | 24.5494 |
| fannkuch-redux | four core | 100.739 | 46.0605 | 27.4042 | 24.9589 | 24.6271 | 6.30938 | 23.9821 |
| n-body | one core | 13.2462 | 6.17322 | 2.97591 | 2.73213 | 3.60129 | 3.52761 | 5.03290 |
| n-body | four core | 13.2575 | 6.17396 | 2.97536 | 2.73346 | 3.59792 | 3.53115 | 4.97078 |
| spectral-norm | one core | 8.32536 | 5.63768 | 1.78873 | 1.83991 | 3.21947 | 1.79955 | 1.95723 |
| spectral-norm | four core | 8.32395 | 5.63691 | 1.78784 | 1.83900 | 3.21836 | 0.460238 | 1.91745 |

## Raw application artifacts

These are unstripped artifacts prepared for the runtime run. Java is the sum
of the retained application class files. Required runtime and toolchain
distributions are outside this table.

| Case | TypeRB Native | TypeRB Go | C | C++ | Go | Rust | Java classes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | 19,176 | 2,808,692 | 70,648 | 70,912 | 2,381,555 | 4,664,888 | 3,839 |
| n-body | 22,912 | 2,815,362 | 70,856 | 71,336 | 2,382,167 | 4,651,312 | 4,019 |
| spectral-norm | 19,888 | 2,809,866 | 70,696 | 71,952 | 2,382,139 | 4,673,736 | 1,428 |

## Retained evidence

GitHub published these exact archives:

| Artifact | ID | Archive bytes | GitHub SHA-256 |
| --- | ---: | ---: | --- |
| benchmarksgame-runtime-fannkuch-redux | 9804197649 | 392,568 | `e58aca67a18a49153158fbd6e79a0194ccf6c27b88dea1badf339a181403eff5` |
| benchmarksgame-runtime-n-body | 9799949810 | 388,379 | `e1e0335e840f88cb6525383a72980134f2b44a55895e4e42bd447bded0510793` |
| benchmarksgame-runtime-spectral-norm | 9799727036 | 386,345 | `15b987f2837a3b92468375af59fc0c471bbe6668ee198336fd2aeb7236849497` |

This result retains all 4,137 extracted files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 4,138 files and excludes only this README and
itself. Each artifact retains bootstrap, workflow, preparation, correctness,
environment, raw observation, median, and process-control evidence.

## Conclusion

Accepted generated-code improvements materially reduced `fannkuch-redux` and
`n-body` while preserving the self-hosted fixed point, very small applications,
and low peak memory. Native remains 2.59x to 4.09x slower than Pure Go across
this initial three-kernel corpus. Further work remains profile-driven and must
preserve general language behavior rather than add benchmark-specific paths.
