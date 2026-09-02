# Formal Lexical-Loop-Index Runtime Results on Linux arm64

The complete current-revision snapshot passes the formal fresh-process runtime
contract for all three registered programs, both CPU lanes, and all seven
implementations. Every one of the 462 retained observations completed with
status zero and contributed to its published median.

The accepted Native revision materially improves all three numeric kernels over
the preceding complete snapshot. It remains slower than Pure Go in this corpus:
the one-core Native/Pure-Go wall ratios are 3.446x for `fannkuch-redux`, 3.185x
for `n-body`, and 1.609x for `spectral-norm`. Pure Go parity or better remains
the minimum runtime objective.

## Exact scope

- measured Native revision:
  `aad4954c66ae394a5edb836b20498e5a60b769bd`;
- TypeRB Go semantic reference:
  `0.4.4-dev@5dc09070cf7f88a569279f5e63982a6de59d692c`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Native target profile `linux-arm64-v0`, pinned QBE 1.3, Go 1.27.0,
  BenchExec `runexec` 3.35, and the pinned context toolchains;
- three fresh GitHub-hosted `ubuntu-24.04-arm` jobs, each reporting four
  Neoverse-N2 logical CPUs and Linux 6.17; and
- successful formal run
  [33576119574](https://github.com/type-rb/type-rb-native/actions/runs/33576119574).

The released compiler performed a setup-only transition. The measured
candidate then closed a byte-identical 254,872-byte B2/B3/B4 fixed point with
SHA-256
`84354b9dace7d981fc1ba36c356e7c7db7e691daf43e1b1437c8faa365b8a5d9`.

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
| fannkuch-redux | 84.8680 | 45.9831 | 24.6288 | 27.4857 | 24.9779 | 24.8743 | 24.5620 | 3.446x slower |
| n-body | 11.4655 | 6.17297 | 3.59940 | 2.97666 | 2.73493 | 3.51068 | 5.03789 | 3.185x slower |
| spectral-norm | 5.17995 | 5.63669 | 3.22025 | 1.78808 | 1.83940 | 1.79872 | 1.93306 | 1.609x slower |

Native is 8.1% faster than TypeRB Go on `spectral-norm`, but remains 1.846x
and 1.857x slower on `fannkuch-redux` and `n-body`. Against the fastest pinned
one-core context implementation, Native remains 2.90x to 4.19x slower. These
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
| fannkuch-redux | 84.8499 | 46.1071 | 24.6356 | 6.31089 | 6.31089 |
| n-body | 11.4610 | 6.17263 | 3.59886 | 3.51357 | 2.73238 |
| spectral-norm | 5.17863 | 5.63641 | 3.21905 | 0.461023 | 0.461023 |

## CPU and memory

One-core CPU medians track wall time closely: Native/Pure-Go CPU ratios are
3.447x, 3.190x, and 1.612x for the three cases. Native's measured peak
process-tree memory is 524,288 bytes for `fannkuch-redux` and `n-body`, and
1,220,608 bytes for `spectral-norm`. Those values are 82.65% to 83.07% below
TypeRB Go and below Pure Go in every case. The 524,288-byte values sit at the
controller's observed measurement granularity, so smaller differences should
not be inferred from them.

## Snapshot change

Compared with the preceding complete accepted snapshot on the same registered
runner class, Native one-core wall medians are lower by 15.77% for
`fannkuch-redux`, 13.44% for `n-body`, and 37.78% for `spectral-norm`. This is a
complete-snapshot comparison, not the paired same-host acceptance evidence for
each intervening optimization; the retained optimization A/B results remain
the causal evidence for those individual changes.

## Retained evidence

| Artifact | ID | Archive bytes | GitHub SHA-256 |
| --- | ---: | ---: | --- |
| benchmarksgame-runtime-fannkuch-redux | 9829420974 | 392,574 | `77ac0f8715aea825ea6d2cccfd706fe286029d267f9317c7b2523741465c5f97` |
| benchmarksgame-runtime-n-body | 9827159042 | 388,330 | `55c2155e4cc2c6cbb05a4815c03df063670dd1881ad01b1928fa76fd3ef88e55` |
| benchmarksgame-runtime-spectral-norm | 9826987651 | 386,283 | `77fbd3c2d6ae5b5886c021a420dac2e99ed3f13d33200e9638839745590f42cb` |

This result retains all 4,137 extracted files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 4,138 files and excludes only this README and
itself. The tree includes source and toolchain identities, compiler-transition
evidence, correctness records, complete raw observations, independently
reproduced medians, cache state, process metrics, and workflow context.

## Conclusion

The accepted compiler changes substantially improve all three runtime cases
without losing Native's low memory, fast build, or compact-artifact advantages.
The remaining 1.61x to 3.45x Pure Go gap, and the larger 2.90x to 4.19x gap to
the fastest one-core context programs, confirms that generated-code and runtime
optimization remain the primary engineering work.
