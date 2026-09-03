# Formal Native-MIR Induction-Phi Runtime Results on Linux arm64

The complete current-revision snapshot passes the formal fresh-process runtime
contract for all three registered programs, both CPU lanes, and all seven
implementations. Every one of the 462 retained observations completed with
status zero and contributed to its published median.

The current Native revision improves `n-body` over the preceding complete
snapshot while the other two cases are effectively unchanged. It remains
slower than Pure Go in this corpus: the one-core Native/Pure-Go wall ratios are
3.448x for `fannkuch-redux`, 2.903x
for `n-body`, and 1.609x for `spectral-norm`. Pure Go parity or better remains
the minimum runtime objective.

## Exact scope

- measured Native revision:
  `9dcae126e036d335344907ed4ea091a7f11a2198`;
- TypeRB Go semantic reference:
  `0.4.4-dev@5dc09070cf7f88a569279f5e63982a6de59d692c`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Native target profile `linux-arm64-v0`, pinned QBE 1.3, Go 1.27.0,
  BenchExec `runexec` 3.35, and the pinned context toolchains;
- three fresh GitHub-hosted `ubuntu-24.04-arm` jobs, each reporting four
  Neoverse-N2 logical CPUs and Linux 6.17; and
- successful formal run
  [33693165413](https://github.com/type-rb/type-rb-native/actions/runs/33693165413).

The released compiler performed a setup-only transition. The measured
candidate then closed a byte-identical 308,592-byte B2/B3/B4 fixed point with
SHA-256
`9ac205db950d445db668f72d18fe05ed111fc66f677c68d275d8b7811ea2a440`.

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
| fannkuch-redux | 84.8512 | 46.0490 | 24.6113 | 27.4129 | 24.9746 | 24.8723 | 24.5689 | 3.448x slower |
| n-body | 10.4490 | 6.17184 | 3.59886 | 2.97580 | 2.73214 | 3.52515 | 5.04426 | 2.903x slower |
| spectral-norm | 5.17923 | 5.63885 | 3.21826 | 1.78815 | 1.83934 | 1.79892 | 1.93303 | 1.609x slower |

Native is 8.2% faster than TypeRB Go on `spectral-norm`, but remains 1.843x
and 1.693x slower on `fannkuch-redux` and `n-body`. Against the fastest pinned
one-core context implementation, Native remains 2.90x to 3.82x slower. These
rows are exact implementation comparisons rather
than a composite language score.

## Four-core context

Native and TypeRB Go remain single-threaded for these sources, so their
four-core results are effectively unchanged. The pinned Rust implementations
use their authored parallel paths for `fannkuch-redux` and `spectral-norm`.
Those results are retained as four-core implementation context rather than
mixed into the one-core ordering.

| Case | Native wall | TypeRB Go wall | Pure Go wall | Rust wall | Fastest wall |
| --- | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | 84.8572 | 46.1058 | 24.6244 | 6.30923 | 6.30923 |
| n-body | 10.4502 | 6.17359 | 3.59918 | 3.51362 | 2.73674 |
| spectral-norm | 5.17883 | 5.63533 | 3.21981 | 0.461390 | 0.461390 |

## CPU and memory

One-core CPU medians track wall time closely: Native/Pure-Go CPU ratios are
3.448x, 2.908x, and 1.611x for the three cases. Native's measured peak
process-tree memory is 524,288 bytes
for `fannkuch-redux`, 524,288 bytes for `n-body`, and 1,220,608 bytes for
`spectral-norm`. Those values are 82.63% to 83.90% below TypeRB Go and
below Pure Go in every case. Values at 524,288 bytes sit at the controller's
observed measurement granularity, so smaller differences should not be
inferred from them.

## Snapshot change

Compared with the preceding complete accepted snapshot on the same registered
runner class, Native one-core wall medians are effectively unchanged for
`fannkuch-redux` (0.020% lower), 8.87% lower for
`n-body`, and effectively unchanged for `spectral-norm` (0.014% lower). This is
a complete-snapshot comparison, not the paired same-host acceptance evidence
for each intervening optimization; the retained optimization A/B results
remain the causal evidence for those individual changes.

## Retained evidence

| Artifact | ID | Archive bytes | GitHub SHA-256 |
| --- | ---: | ---: | --- |
| benchmarksgame-runtime-fannkuch-redux | 9873901677 | 392,640 | `fa706eb8b150b5d694f1fa9520a2c09f85108d09c1037e184f92be69b311a8aa` |
| benchmarksgame-runtime-n-body | 9871346454 | 388,436 | `43843908f87ac3b73470aa8d48b325906de4309d26d6ae42a2a0c06bb34f3276` |
| benchmarksgame-runtime-spectral-norm | 9871167760 | 386,413 | `c26386abe6a543080ecbdad7a2785feea8e68ae0a1526973194335a67c52f75f` |

This result retains all 4,137 extracted files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 4,138 files and excludes only this README and
itself. The tree includes source and toolchain identities, compiler-transition
evidence, correctness records, complete raw observations, independently
reproduced medians, cache state, process metrics, and workflow context.

## Conclusion

The accepted compiler changes improve `n-body` without losing Native's low
memory, fast build, or compact-artifact advantages. The remaining 1.61x to
3.45x Pure Go gap, and the larger 2.90x to 3.82x gap to
the fastest one-core context programs, confirms that generated-code and runtime
optimization remain the primary engineering work.
