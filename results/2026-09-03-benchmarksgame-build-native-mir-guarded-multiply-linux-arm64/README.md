# Formal Guarded-Multiply Build Results on Linux arm64

The current accepted self-hosted Native compiler passes the complete formal
backend-pair build and distribution contract on all three registered TypeRB
programs. It builds the same sources 2.22x to 2.53x faster than the optimized
Go path, requires only 16.3% to 16.9% of its compiler CPU time, and uses about
51% less peak process-tree memory.

Native raw applications are 99.21% to 99.32% smaller. Its compiler-plus-QBE
controlled payload is 1,028,536 bytes, compared with 275,388,970 bytes for
reference `trb` plus the complete pinned Go root. These are exact backend
results, not a composite language ranking.

## Exact scope

- measured Native revision:
  `b82d30f4986aa289cedb7bb3392002019bc549f8`;
- TypeRB Go semantic reference:
  `0.4.4-dev@5dc09070cf7f88a569279f5e63982a6de59d692c`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Native target profile `linux-arm64-v0`, pinned QBE 1.3, GCC 13.3.0,
  LLD 18.1.3, Go 1.27.1, and BenchExec `runexec` 3.35;
- three fresh GitHub-hosted `ubuntu-24.04-arm` jobs, each reporting four
  Neoverse-N2 logical CPUs and Linux 6.17; and
- successful formal run
  [33730616644](https://github.com/type-rb/type-rb-native/actions/runs/33730616644).

The released compiler performed a setup-only transition. The measured
candidate then closed a byte-identical 313,896-byte B2/B3/B4 fixed point with
SHA-256
`5c0864257d59d517943af817b2b4fd9f8cfd66cd9d65f59cdcbc7465b312eb04`.
Its target-neutral compiler QBE is 1,109,629 bytes with SHA-256
`09505badac860dc72518b6cb3d099fbba542b6756d9de378322a7ad689b8fd83`.
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
| fannkuch-redux | 0.158973 | 0.393291 | 2.474x | 0.056306 | 0.345209 | 6.131x | 78,147,584 | 159,551,488 | 51.02% |
| n-body | 0.223112 | 0.494295 | 2.215x | 0.067188 | 0.397255 | 5.913x | 78,278,656 | 162,615,296 | 51.86% |
| spectral-norm | 0.239746 | 0.605701 | 2.526x | 0.076195 | 0.452291 | 5.936x | 78,065,664 | 160,428,032 | 51.34% |

## Application artifacts

Each Native build reproduced one byte-identical application across all eleven
observations. Each Go case produced eleven correct byte variants, retained as
evidence rather than hidden.

| Case | Native raw median | Go raw median | Native reduction | Native variants | Go variants |
| --- | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | 19,080 | 2,808,692 | 99.321% | 1 | 11 |
| n-body | 22,320 | 2,815,354 | 99.207% | 1 | 11 |
| spectral-norm | 19,744 | 2,809,882 | 99.297% | 1 | 11 |

The separately retained correct artifacts have these stripped sizes:

| Case | Native stripped | Go stripped | Native reduction |
| --- | ---: | ---: | ---: |
| fannkuch-redux | 19,072 | 1,887,832 | 98.990% |
| n-body | 22,312 | 1,887,832 | 98.818% |
| spectral-norm | 19,736 | 1,887,832 | 98.955% |

## Controlled distribution and external boundaries

| Scope | Raw bytes | Alternate view | Bytes |
| --- | ---: | --- | ---: |
| Native compiler plus QBE | 1,028,536 | both stripped | 661,120 |
| reference `trb` plus complete Go root | 275,388,970 | stripped `trb` plus unchanged Go root | 265,130,813 |

This is a 99.6265% raw controlled-payload reduction and a 99.7506% reduction
in the alternate stripped view. Native does not require Go to build these
applications. QBE, the platform C driver, assembler, LLD, dynamic linker, and
shared libraries remain explicit external prerequisites and appear in the
retained process and dependency inventories.

## Retained evidence

| Artifact | ID | Archive bytes | GitHub SHA-256 |
| --- | ---: | ---: | --- |
| benchmarksgame-build-fannkuch-redux | 9883757557 | 2,506,011 | `53bad11a1ae70b688a2304717bffbc73e0cd064c9fc6c3e0b19dee428d4de38e` |
| benchmarksgame-build-n-body | 9883758026 | 2,519,952 | `1242ea79059cc48158bea22933737d81f50bbd7278baca280c9b0f4bf1ca9993` |
| benchmarksgame-build-spectral-norm | 9883761125 | 2,507,542 | `9e57835626534d1e4b03af747d979e6ffd6c154d6b89fcde6d376c0f209d9b75` |

This result retains all 891 extracted files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 892 files and excludes only this README and
itself. The tree includes complete identities, fixed-point evidence, process
traces, dependencies, correctness records, all raw observations,
independently reproduced medians, application artifacts, and distribution
inventories.
Repository copies of generated text remove trailing horizontal whitespace and
extra blank lines at end of file; the artifact table records the SHA-256 of each
original GitHub archive.

## Conclusion

For these exact sources, the accepted self-hosted Native compiler exceeds the
optimized Go backend on build wall time, compiler CPU, peak RSS, application
size, controlled distribution size, and artifact reproducibility. Runtime is
a separate result: Pure Go parity or better remains the minimum target, and
generated-code and runtime optimization remain the primary measured work.
