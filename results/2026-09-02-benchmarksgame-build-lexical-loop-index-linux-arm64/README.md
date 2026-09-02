# Formal Lexical-Loop-Index Build Results on Linux arm64

The accepted self-hosted Native compiler passes the complete formal backend-pair
build and distribution contract on all three registered TypeRB programs. It
builds the same sources 2.34x to 2.43x faster than the optimized Go path,
requires only 15.8% to 17.6% of its compiler CPU time, and uses about 51% less
peak process-tree memory.

Native raw applications are 99.20% to 99.32% smaller. Its compiler-plus-QBE
controlled payload is 969,512 bytes, compared with 275,375,323 bytes for
reference `trb` plus the complete pinned Go root. These are exact backend
results, not a composite language ranking.

## Exact scope

- measured Native revision:
  `aad4954c66ae394a5edb836b20498e5a60b769bd`;
- TypeRB Go semantic reference:
  `0.4.4-dev@5dc09070cf7f88a569279f5e63982a6de59d692c`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Native target profile `linux-arm64-v0`, pinned QBE 1.3, GCC 13.3.0,
  LLD 18.1.3, Go 1.27.0, and BenchExec `runexec` 3.35;
- three fresh GitHub-hosted `ubuntu-24.04-arm` jobs, each reporting four
  Neoverse-N2 logical CPUs and Linux 6.17; and
- successful formal run
  [33576121564](https://github.com/type-rb/type-rb-native/actions/runs/33576121564).

The released compiler performed a setup-only transition. The measured
candidate then closed a byte-identical 254,872-byte B2/B3/B4 fixed point with
SHA-256
`84354b9dace7d981fc1ba36c356e7c7db7e691daf43e1b1437c8faa365b8a5d9`.
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
| fannkuch-redux | 0.195676 | 0.457659 | 2.339x | 0.053922 | 0.333591 | 6.187x | 78,229,504 | 159,215,616 | 50.87% |
| n-body | 0.163579 | 0.396998 | 2.427x | 0.065314 | 0.370288 | 5.669x | 78,303,232 | 162,263,040 | 51.74% |
| spectral-norm | 0.191597 | 0.452079 | 2.360x | 0.053530 | 0.339280 | 6.338x | 78,364,672 | 159,916,032 | 51.00% |

## Application artifacts

Each Native build reproduced one byte-identical application across all eleven
observations. Each Go case produced eleven correct byte variants, retained as
evidence rather than hidden.

| Case | Native raw median | Go raw median | Native reduction | Native variants | Go variants |
| --- | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | 19,080 | 2,808,692 | 99.321% | 1 | 11 |
| n-body | 22,496 | 2,815,362 | 99.201% | 1 | 11 |
| spectral-norm | 19,680 | 2,809,898 | 99.300% | 1 | 11 |

The separately retained correct artifacts have these stripped sizes:

| Case | Native stripped | Go stripped | Native reduction |
| --- | ---: | ---: | ---: |
| fannkuch-redux | 19,072 | 1,887,832 | 98.990% |
| n-body | 22,488 | 1,887,832 | 98.809% |
| spectral-norm | 19,672 | 1,887,832 | 98.958% |

## Controlled distribution and external boundaries

| Scope | Raw bytes | Alternate view | Bytes |
| --- | ---: | --- | ---: |
| Native compiler plus QBE | 969,512 | both stripped | 602,096 |
| reference `trb` plus complete Go root | 275,375,323 | stripped `trb` plus unchanged Go root | 265,117,558 |

This is a 99.6479% raw controlled-payload reduction and a 99.7729% reduction
in the alternate stripped view. Native does not require Go to build these
applications. QBE, the platform C driver, assembler, LLD, dynamic linker, and
shared libraries remain explicit external prerequisites and appear in the
retained process and dependency inventories.

## Retained evidence

| Artifact | ID | Archive bytes | GitHub SHA-256 |
| --- | ---: | ---: | --- |
| benchmarksgame-build-fannkuch-redux | 9826719972 | 2,505,496 | `aca8b947ea717d9a7ce4f6d44c3f2915fd7cbc7729766905e6015fbb5458979f` |
| benchmarksgame-build-n-body | 9826722494 | 2,519,988 | `d8415d9cb4ac58e00a5b26d93d3cd35c0c576cefe96b22b88583c8120bcfadb1` |
| benchmarksgame-build-spectral-norm | 9826725564 | 2,506,865 | `6ee2d8edf81443fe07b7b5e658794b6300c8ac4fb06ee93aa8989b1f36a8ffda` |

This result retains all 891 extracted files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 892 files and excludes only this README and
itself. The tree includes complete identities, fixed-point evidence, process
traces, dependencies, correctness records, all raw observations, independently
reproduced medians, application artifacts, and distribution inventories.

## Conclusion

For these exact sources, the accepted self-hosted Native compiler exceeds the
optimized Go backend on build wall time, compiler CPU, peak RSS, application
size, controlled distribution size, and artifact reproducibility. Runtime is a
separate result: Pure Go parity or better remains the minimum target, and
generated-code and runtime optimization remain the primary measured work.
