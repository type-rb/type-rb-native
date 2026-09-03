# Formal Guarded-Multiply Runtime Results on Linux arm64

The complete current-revision snapshot passes the formal fresh-process runtime
contract for all three registered programs, both CPU lanes, and all seven
implementations. Every one of the 462 retained observations completed with
status zero and contributed to its published median.

The accepted Native guarded-multiply optimization improves `spectral-norm`
by 15.35% over the preceding complete snapshot while the other two cases are
effectively unchanged. Native remains slower than Pure Go in this corpus: the
one-core Native/Pure-Go wall ratios are 3.448x for `fannkuch-redux`, 2.904x for
`n-body`, and 1.362x for `spectral-norm`. Pure Go parity or better remains the
minimum runtime objective.

## Exact scope

- measured Native revision:
  `b82d30f4986aa289cedb7bb3392002019bc549f8`;
- TypeRB Go semantic reference:
  `0.4.4-dev@5dc09070cf7f88a569279f5e63982a6de59d692c`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Native target profile `linux-arm64-v0`, pinned QBE 1.3, Go 1.27.1,
  BenchExec `runexec` 3.35, and the pinned context toolchains;
- three fresh GitHub-hosted `ubuntu-24.04-arm` jobs, each reporting four
  Neoverse-N2 logical CPUs and Linux 6.17; and
- successful formal run
  [33730608827](https://github.com/type-rb/type-rb-native/actions/runs/33730608827).

The released compiler performed a setup-only transition. The measured
candidate then closed a byte-identical 313,896-byte B2/B3/B4 fixed point with
SHA-256
`5c0864257d59d517943af817b2b4fd9f8cfd66cd9d65f59cdcbc7465b312eb04`.

## Correctness and measurement integrity

The identical TypeRB sources pass through the optimized Go backend and ordinary
self-hosted Native compiler. The pinned C, C++, Go, Rust, and Java context
programs implement the same published benchmark specifications. Every program
passed an untimed exact-output check before measurement.

Each isolated case ran two warmup rounds and eleven retained rounds in both a
one-core and four-core lane. Candidate order rotated every round. BenchExec
measured each complete fresh process with the registered filesystem, CPU,
memory, network, cache, and process-tree controls. All 42 median rows contain
eleven successful retained observations. Re-running the checked-in summarizer
independently reproduces every committed median byte for byte.

## One-core wall time

Lower is better. Times are medians in seconds. The final column divides Native
by the pinned Pure Go implementation, so values above 1 mean Native is slower.

| Case | Native | TypeRB Go | Pure Go | C | C++ | Rust | Java | Native / Pure Go |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | 84.8603 | 45.9106 | 24.6081 | 27.4093 | 24.9654 | 24.8739 | 24.5982 | 3.448x slower |
| n-body | 10.4497 | 6.17158 | 3.59892 | 2.97583 | 2.73186 | 3.51417 | 5.04616 | 2.904x slower |
| spectral-norm | 4.38424 | 5.63712 | 3.21915 | 1.78837 | 1.83954 | 1.79861 | 1.95809 | 1.362x slower |

Native is 22.2% faster than TypeRB Go on `spectral-norm`, but remains 1.848x
and 1.693x slower on `fannkuch-redux` and `n-body`. Against the fastest pinned
one-core context implementation, Native remains 2.45x to 3.83x slower. These
rows are exact implementation comparisons rather than a composite language
score.

## Four-core context

Native and TypeRB Go remain single-threaded for these sources, so their
four-core results are effectively unchanged. The pinned Rust implementations
use their authored parallel paths for `fannkuch-redux` and `spectral-norm`.
Those results are retained as four-core implementation context rather than
mixed into the one-core ordering.

| Case | Native wall | TypeRB Go wall | Pure Go wall | Rust wall | Fastest wall |
| --- | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | 84.8645 | 45.9789 | 24.6373 | 6.31250 | 6.31250 |
| n-body | 10.4486 | 6.17068 | 3.59847 | 3.51336 | 2.73103 |
| spectral-norm | 4.38347 | 5.63593 | 3.21870 | 0.462834 | 0.462834 |

## CPU and memory

One-core CPU medians track wall time closely: Native/Pure-Go CPU ratios are
3.449x, 2.908x, and 1.364x for the three cases. Native's measured peak
process-tree memory is 524,288 bytes for `fannkuch-redux`, 524,288 bytes for
`n-body`, and 1,462,272 bytes for `spectral-norm`. Those values are 79.68% to
84.06% below TypeRB Go and below Pure Go in every case. Values at 524,288 bytes
sit at the controller's observed measurement granularity, so smaller
differences should not be inferred from them.

## Snapshot change

Compared with the preceding complete accepted snapshot on the same registered
runner class, Native one-core wall medians are effectively unchanged for
`fannkuch-redux` (0.011% higher) and `n-body` (0.007% higher), and 15.35% lower
for `spectral-norm`. This is a complete-snapshot comparison, not the paired
same-host acceptance evidence for the guarded-multiply optimization; the
retained focused A/B result remains its causal evidence.

## Retained evidence

| Artifact | ID | Archive bytes | GitHub SHA-256 |
| --- | ---: | ---: | --- |
| benchmarksgame-runtime-fannkuch-redux | 9887994048 | 392,609 | `5901c35594180e342d951c963afb6edccddc85e4d6358f0813684e90278f34df` |
| benchmarksgame-runtime-n-body | 9884362382 | 388,352 | `6813b6221cd09c5140d57b6592b68e048312ec0c02a6fcdb6a5f946e408f6051` |
| benchmarksgame-runtime-spectral-norm | 9884121395 | 386,338 | `249e9cae15509e89d336c7c9d9f247cd92367902075d9c3c002cc690f6e54f65` |

This result retains all 4,137 extracted files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 4,138 files and excludes only this README and
itself. The tree includes source and toolchain identities, compiler-transition
evidence, correctness records, complete raw observations, independently
reproduced medians, cache state, process metrics, and workflow context.
Repository copies of generated text remove trailing horizontal whitespace and
extra blank lines at end of file; the artifact table records the SHA-256 of each
original GitHub archive.

## Conclusion

The accepted compiler changes materially narrow `spectral-norm`'s gap without
losing Native's low memory, fast build, or compact-artifact advantages. The
remaining 1.36x to 3.45x Pure Go gap, and the larger 2.45x to 3.83x gap to the
fastest one-core context programs, confirms that generated-code and runtime
optimization remain the primary engineering work.
