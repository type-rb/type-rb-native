# Formal Benchmarks Game Runtime Results on Linux arm64

The current self-hosted Native compiler passes the complete formal runtime
correctness, isolation, repetition, and evidence contract on all three
registered numeric kernels. Relative to the previous formal snapshot, Native
wall time improved by 42.8% for `fannkuch-redux`, 35.6% for `n-body`, and 39.5%
for `spectral-norm`.

A material runtime gap remains. For these exact identical-TypeRB programs,
Native is 1.48x to 3.01x slower than the optimized TypeRB Go path. Against the
fastest pinned context implementation in the one-core lane, Native is 4.52x to
6.80x slower. These are implementation results for exact programs, inputs,
and toolchains, not a composite language ranking.

## Exact scope

- measured Native revision:
  `769233b05203937e9f8986b7a8558df6e2f98c5c`;
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
  [33483039685](https://github.com/type-rb/type-rb-native/actions/runs/33483039685).

The self-hosted compiler closed the same 252,816-byte B2/B3/B4 fixed point in
all three jobs, with SHA-256
`09a30ee2c58f2398a71d210dfb4235cc31af73984da44d0f5bf01bfe87d1b443`.

## Correctness and measurement integrity

Each case contains exactly seven candidates: the identical TypeRB source
through Native and optimized Go, followed by pinned C, C++, Go, Rust, and Java
implementations. Before timing, every candidate returned status zero, produced
empty stderr, and matched the published performance-output oracle byte for
byte in both lanes.

Each one-core and four-core lane retained all two warmup rounds and eleven
retained rounds. Every process tree ran under BenchExec with explicit CPU,
memory, filesystem, network, cache, and process-closure controls. The complete
raw observations and generated medians are retained below.

## Primary identical-TypeRB comparison

Times are whole fresh-process medians in seconds. RSS is process-tree peak
memory in bytes. A ratio above 1 means Native is slower.

| Case | Lane | Native wall | Go wall | Native/Go | Native CPU | Go CPU | Native RSS | Go RSS | Native RSS reduction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | one core | 110.507 | 46.0980 | 2.397x | 110.507 | 46.0879 | 524,288 | 3,256,320 | 83.90% |
| fannkuch-redux | four core | 110.446 | 45.8801 | 2.407x | 110.449 | 45.9671 | 524,288 | 4,050,944 | 87.06% |
| n-body | one core | 18.5895 | 6.17365 | 3.011x | 18.5872 | 6.16527 | 524,288 | 3,092,480 | 83.05% |
| n-body | four core | 18.5771 | 6.17461 | 3.009x | 18.5757 | 6.18470 | 524,288 | 3,801,088 | 86.21% |
| spectral-norm | one core | 8.32380 | 5.63649 | 1.477x | 8.32048 | 5.62954 | 1,257,472 | 7,192,576 | 82.52% |
| spectral-norm | four core | 8.32438 | 5.63477 | 1.477x | 8.32154 | 5.64395 | 1,212,416 | 7,974,912 | 84.80% |

## Cross-language implementation context

The following values are wall-time medians for the exact pinned programs. They
are not an intrinsic ordering of languages. Some upstream programs use threads;
the separate four-core lane preserves that authored behavior.

| Case | Lane | TypeRB Native | TypeRB Go | C | C++ | Go | Rust | Java |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | one core | 110.507 | 46.0980 | 27.4043 | 24.9504 | 24.6151 | 24.8784 | 24.4530 |
| fannkuch-redux | four core | 110.446 | 45.8801 | 27.4076 | 24.9789 | 24.6702 | 6.30918 | 23.9750 |
| n-body | one core | 18.5895 | 6.17365 | 2.97646 | 2.73169 | 3.60000 | 3.50778 | 5.04152 |
| n-body | four core | 18.5771 | 6.17461 | 2.97588 | 2.73713 | 3.60166 | 3.50752 | 4.97827 |
| spectral-norm | one core | 8.32380 | 5.63649 | 1.78810 | 1.83952 | 3.21884 | 1.79780 | 1.94590 |
| spectral-norm | four core | 8.32438 | 5.63477 | 1.78778 | 1.83894 | 3.21847 | 0.460991 | 1.91433 |

## Raw application artifacts

These are unstripped artifacts prepared for the runtime run. Java is the sum
of the retained application class files. Required runtime and toolchain
distributions are outside this table.

| Case | TypeRB Native | TypeRB Go | C | C++ | Go | Rust | Java classes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | 19,272 | 2,808,692 | 70,648 | 70,912 | 2,381,555 | 4,664,888 | 3,839 |
| n-body | 24,032 | 2,815,314 | 70,856 | 71,336 | 2,382,167 | 4,651,312 | 4,019 |
| spectral-norm | 19,888 | 2,809,866 | 70,696 | 71,952 | 2,382,139 | 4,673,736 | 1,428 |

## Retained evidence

GitHub published these exact archives:

| Artifact | ID | Archive bytes | GitHub SHA-256 |
| --- | ---: | ---: | --- |
| benchmarksgame-runtime-fannkuch-redux | 9795122502 | 392,471 | `585e61866a2b4228af667f9322449cf32d26e6c11624abc1d75705677c4babca` |
| benchmarksgame-runtime-n-body | 9791388014 | 388,279 | `d00a30d420fa93061d6ed6ba0d8eb05fc1240110da7c3665f7ed7b64498c3743` |
| benchmarksgame-runtime-spectral-norm | 9791107605 | 386,294 | `be45f7c88c30afd22b079a49772b8641d97e49d79ccd79d6ad0448fe0ba9a55b` |

Each artifact retains bootstrap, workflow, preparation, correctness,
environment, raw observation, median, and process-control evidence. The root
`EVIDENCE_SHA256SUMS` covers every extracted file and `ARTIFACTS.tsv`, excluding
only this README and the checksum file itself.

## Conclusion

Recent generated-code improvements materially reduced all three Native runtime
medians while preserving the self-hosted fixed point, very small applications,
and low peak memory. Native has not yet reached the project goal of matching or
exceeding established statically typed implementations. Further work remains
profile-driven and must preserve general language behavior rather than add
benchmark-specific shortcuts.
