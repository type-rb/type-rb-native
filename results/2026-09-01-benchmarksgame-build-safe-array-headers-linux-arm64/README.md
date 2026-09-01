# Formal Safe-Array-Header Build Results on Linux arm64

The accepted self-hosted Native compiler passes the complete formal backend-pair
build and distribution contract on all three registered TypeRB programs. It
builds the same sources 2.34x to 2.62x faster than the optimized Go path,
requires only 15.8% to 17.0% of its compiler CPU time, and uses about 51% less
peak process-tree memory.

Native raw applications are 99.19% to 99.32% smaller. Its compiler-plus-QBE
controlled payload is 969,600 bytes, compared with 275,375,323 bytes for
reference `trb` plus the complete pinned Go root. These are exact backend
results, not a composite language ranking.

## Exact scope

- measured Native revision:
  `473a6dee19b637a3009937d9b288c3a91f429a6b`;
- TypeRB Go semantic reference:
  `0.4.4-dev@5dc09070cf7f88a569279f5e63982a6de59d692c`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Native target profile `linux-arm64-v0`, pinned QBE 1.3, GCC 13.3.0,
  LLD 18.1.3, Go 1.27.0, and BenchExec `runexec` 3.35;
- three fresh GitHub-hosted `ubuntu-24.04-arm` jobs, each reporting four
  Neoverse-N2 logical CPUs and Linux 6.17; and
- successful formal run
  [33505007570](https://github.com/type-rb/type-rb-native/actions/runs/33505007570).

The released compiler performed a setup-only transition. The measured
candidate then closed a byte-identical 254,960-byte B2/B3/B4 fixed point with
SHA-256
`65b18c8999e91dbb67e7dabb5d731987daa32076c9e4cd709962dc4b49bb73cb`.
No successful Go or reference-compiler process occurs in those transitions.

## Correctness and measurement integrity

Both backends checked, built, and ran each authored TypeRB source correctly
before timing. Each case alternated the two backends through two warmups and
eleven retained observations. All 66 retained builds returned status zero,
produced an application, and passed an untimed exact-output execution. No
sample, metric, or artifact is missing.

Every compiler process tree ran under BenchExec with the registered filesystem,
CPU, memory, network, cache, and process-closure controls. Re-running the
checked-in summarizer independently reproduces every retained median byte for
byte.

## Compiler measurements

Times are complete compiler-process-tree medians in seconds. RSS is peak
process-tree memory in bytes. Speedup divides Go by Native, so values above 1
favor Native.

| Case | Native wall | Go wall | Native speedup | Native CPU | Go CPU | Native CPU advantage | Native RSS | Go RSS | Native RSS reduction |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | 0.157492 | 0.391868 | 2.488x | 0.055614 | 0.348023 | 6.258x | 78,303,232 | 159,662,080 | 50.96% |
| n-body | 0.223244 | 0.521892 | 2.338x | 0.069758 | 0.411103 | 5.893x | 78,495,744 | 162,316,288 | 51.64% |
| spectral-norm | 0.160257 | 0.420169 | 2.622x | 0.055886 | 0.353016 | 6.317x | 78,336,000 | 160,571,392 | 51.21% |

## Application artifacts

Each Native build reproduced one byte-identical application across all eleven
observations. Each Go case produced eleven correct byte variants, retained as
evidence rather than hidden.

| Case | Native raw median | Go raw median | Native reduction | Native variants | Go variants |
| --- | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | 19,176 | 2,808,692 | 99.317% | 1 | 11 |
| n-body | 22,912 | 2,815,362 | 99.186% | 1 | 11 |
| spectral-norm | 19,888 | 2,809,898 | 99.292% | 1 | 11 |

The separately retained correct artifacts have these stripped sizes:

| Case | Native stripped | Go stripped | Native reduction |
| --- | ---: | ---: | ---: |
| fannkuch-redux | 19,168 | 1,887,832 | 98.985% |
| n-body | 22,904 | 1,887,832 | 98.787% |
| spectral-norm | 19,880 | 1,887,832 | 98.947% |

## Controlled distribution and external boundaries

| Scope | Raw bytes | Alternate view | Bytes |
| --- | ---: | --- | ---: |
| Native compiler plus QBE | 969,600 | both stripped | 602,184 |
| reference `trb` plus complete Go root | 275,375,323 | stripped `trb` plus unchanged Go root | 265,117,558 |

This is a 99.6479% raw controlled-payload reduction and a 99.7729% reduction
in the alternate stripped view. Native does not require Go to build these
applications. QBE, the platform C driver, assembler, LLD, dynamic linker, and
shared libraries remain explicit external prerequisites and appear in the
retained process and dependency inventories.

## Retained evidence

| Artifact | ID | Archive bytes | GitHub SHA-256 |
| --- | ---: | ---: | --- |
| benchmarksgame-build-fannkuch-redux | 9799297947 | 2,505,942 | `aa965ed884b8cbefcd9d3e701d632faa2a78eeb3900303252df66c96f2412064` |
| benchmarksgame-build-n-body | 9799293484 | 2,521,150 | `0fa32ea1dd0cad6f9e429b887a6b3977214bccf39c16bf569ea48a3f55f10be7` |
| benchmarksgame-build-spectral-norm | 9799293853 | 2,507,435 | `ba12af6eaa069a977216d18610c70d633cf7a1774f624935908ec0219d7830d1` |

This result retains all 891 extracted files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 892 files and excludes only this README and
itself. The tree includes complete identities, fixed-point evidence, process
traces, dependencies, correctness records, all raw observations, independently
reproduced medians, application artifacts, and distribution inventories.

## Conclusion

For these exact sources, the accepted self-hosted Native compiler exceeds the
optimized Go backend on build wall time, compiler CPU, peak RSS, application
size, controlled distribution size, and artifact reproducibility. Runtime is a
separate result: Pure Go parity remains the minimum target, and generated-code
and runtime optimization remain the primary measured work.
