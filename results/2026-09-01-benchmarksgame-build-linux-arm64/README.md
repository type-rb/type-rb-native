# Formal Benchmarks Game Build Results on Linux arm64

The current self-hosted Native compiler passes the complete formal backend-pair
build and distribution contract on all three registered TypeRB programs. It
builds the same sources 2.32x to 2.48x faster than the optimized Go path,
requires only 15.9% to 17.8% of its compiler CPU time, and uses about 51% less
peak process-tree memory.

Native raw applications are 99.15% to 99.31% smaller. Its compiler-plus-QBE
controlled payload is 967,456 bytes, compared with 275,375,323 bytes for
reference `trb` plus the complete pinned Go root. These are exact backend
results, not a composite language ranking.

## Exact scope

- measured Native revision:
  `769233b05203937e9f8986b7a8558df6e2f98c5c`;
- TypeRB Go semantic reference:
  `0.4.4-dev@5dc09070cf7f88a569279f5e63982a6de59d692c`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Native target profile `linux-arm64-v0`, pinned QBE 1.3, GCC 13.3.0,
  LLD 18.1.3, Go 1.27.0, and BenchExec `runexec` 3.35;
- three fresh GitHub-hosted `ubuntu-24.04-arm` jobs, each reporting four
  Neoverse-N2 logical CPUs and Linux 6.17; and
- successful formal run
  [33483042446](https://github.com/type-rb/type-rb-native/actions/runs/33483042446).

The released compiler performed a setup-only transition. The measured
candidate then closed a byte-identical 252,816-byte B2/B3/B4 fixed point with
SHA-256
`09a30ee2c58f2398a71d210dfb4235cc31af73984da44d0f5bf01bfe87d1b443`.
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
| fannkuch-redux | 0.195099 | 0.452610 | 2.320x | 0.055194 | 0.343156 | 6.217x | 78,118,912 | 160,092,160 | 51.20% |
| n-body | 0.190360 | 0.449181 | 2.360x | 0.070957 | 0.399289 | 5.627x | 78,491,648 | 162,095,104 | 51.58% |
| spectral-norm | 0.156238 | 0.387358 | 2.479x | 0.055352 | 0.348735 | 6.300x | 78,557,184 | 160,256,000 | 50.98% |

The retained wall-time ranges remain separated:

| Case | Native retained min-max | Go retained min-max |
| --- | ---: | ---: |
| fannkuch-redux | 0.190355549-0.203657824 | 0.444190155-0.485806143 |
| n-body | 0.180637575-0.199046845 | 0.419333730-0.465957795 |
| spectral-norm | 0.148624762-0.162493827 | 0.382859082-0.400960154 |

## Application artifacts

Each Native build reproduced one byte-identical application across all eleven
observations. Each Go case produced eleven correct byte variants, retained as
evidence rather than hidden.

| Case | Native raw median | Go raw median | Native reduction | Native variants | Go variants |
| --- | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | 19,272 | 2,808,692 | 99.314% | 1 | 11 |
| n-body | 24,032 | 2,815,362 | 99.146% | 1 | 11 |
| spectral-norm | 19,888 | 2,809,898 | 99.292% | 1 | 11 |

The separately retained correct artifacts have these stripped sizes:

| Case | Native stripped | Go stripped | Native reduction |
| --- | ---: | ---: | ---: |
| fannkuch-redux | 19,264 | 1,887,832 | 98.980% |
| n-body | 24,024 | 1,887,832 | 98.727% |
| spectral-norm | 19,880 | 1,887,832 | 98.947% |

## Controlled distribution and external boundaries

| Scope | Raw bytes | Alternate view | Bytes |
| --- | ---: | --- | ---: |
| Native compiler plus QBE | 967,456 | both stripped | 600,040 |
| reference `trb` plus complete Go root | 275,375,323 | stripped `trb` plus unchanged Go root | 265,117,558 |

This is a 99.6487% raw controlled-payload reduction and a 99.7737% reduction
in the alternate stripped view. Native does not require Go to build these
applications. QBE, the platform C driver, assembler, LLD, dynamic linker, and
shared libraries remain explicit external prerequisites and appear in the
retained process and dependency inventories.

## Retained evidence

| Artifact | ID | Archive bytes | GitHub SHA-256 |
| --- | ---: | ---: | --- |
| benchmarksgame-build-fannkuch-redux | 9790734946 | 2,506,236 | `a2c8ab1f21cade740bee2c017eed6328b62f74da520e6cbd2dc7f544bddc7599` |
| benchmarksgame-build-n-body | 9790732660 | 2,521,655 | `a639d581cb9269e6420e50a0c7697ef91a8f17650d5dae494ffd608ecebd0314` |
| benchmarksgame-build-spectral-norm | 9790729042 | 2,506,580 | `e3f55c1bf9d4f06b425b40a057c402452d5eec245edafec8a6db282c4a63889b` |

This result retains all 891 extracted files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 892 files and excludes only this README and
itself. The tree includes complete identities, fixed-point evidence, process
traces, dependencies, correctness records, all raw observations, independently
reproduced medians, application artifacts, and distribution inventories.

## Conclusion

For these exact sources, the current self-hosted Native compiler exceeds the
optimized Go backend on build wall time, compiler CPU, peak RSS, application
size, controlled distribution size, and artifact reproducibility. Runtime is
a separate result: generated-code and runtime optimization remain the primary
measured performance work.
