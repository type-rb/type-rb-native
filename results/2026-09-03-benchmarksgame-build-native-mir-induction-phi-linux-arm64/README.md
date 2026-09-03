# Formal Native-MIR Induction-Phi Build Results on Linux arm64

The current accepted self-hosted Native compiler passes the complete formal
backend-pair build and distribution contract on all three registered TypeRB
programs. It builds the same sources 2.42x to 2.61x faster than the optimized
Go path, requires only 15.6% to 17.2% of its compiler CPU time, and uses about
51% less peak process-tree memory.

Native raw applications are 99.21% to 99.32% smaller. Its compiler-plus-QBE
controlled payload is 1,023,232 bytes, compared with 275,388,970 bytes for
reference `trb` plus the complete pinned Go root. These are exact backend
results, not a composite language ranking.

## Exact scope

- measured Native revision:
  `9dcae126e036d335344907ed4ea091a7f11a2198`;
- TypeRB Go semantic reference:
  `0.4.4-dev@5dc09070cf7f88a569279f5e63982a6de59d692c`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Native target profile `linux-arm64-v0`, pinned QBE 1.3, GCC 13.3.0,
  LLD 18.1.3, Go 1.27.0, and BenchExec `runexec` 3.35;
- three fresh GitHub-hosted `ubuntu-24.04-arm` jobs, each reporting four
  Neoverse-N2 logical CPUs and Linux 6.17; and
- successful formal run
  [33693165396](https://github.com/type-rb/type-rb-native/actions/runs/33693165396).

The released compiler performed a setup-only transition. The measured
candidate then closed a byte-identical 308,592-byte B2/B3/B4 fixed point with
SHA-256
`9ac205db950d445db668f72d18fe05ed111fc66f677c68d275d8b7811ea2a440`.
Its target-neutral compiler QBE is 1,089,474 bytes with SHA-256
`575cb66c6b894650a2c89f9d5bb1abd9b11d1ec919ab89acecca88c532566979`.
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
| fannkuch-redux | 0.162426 | 0.393125 | 2.420x | 0.055483 | 0.338976 | 6.110x | 78,143,488 | 159,027,200 | 50.86% |
| n-body | 0.167797 | 0.408114 | 2.432x | 0.066575 | 0.387330 | 5.818x | 78,286,848 | 163,000,320 | 51.97% |
| spectral-norm | 0.161074 | 0.420914 | 2.613x | 0.055435 | 0.356331 | 6.428x | 78,254,080 | 160,256,000 | 51.17% |

## Application artifacts

Each Native build reproduced one byte-identical application across all eleven
observations. Each Go case produced eleven correct byte variants, retained as
evidence rather than hidden.

| Case | Native raw median | Go raw median | Native reduction | Native variants | Go variants |
| --- | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | 19,080 | 2,808,692 | 99.321% | 1 | 11 |
| n-body | 22,320 | 2,815,354 | 99.207% | 1 | 11 |
| spectral-norm | 19,680 | 2,809,882 | 99.300% | 1 | 11 |

The separately retained correct artifacts have these stripped sizes:

| Case | Native stripped | Go stripped | Native reduction |
| --- | ---: | ---: | ---: |
| fannkuch-redux | 19,072 | 1,887,832 | 98.990% |
| n-body | 22,312 | 1,887,832 | 98.818% |
| spectral-norm | 19,672 | 1,887,832 | 98.958% |

## Controlled distribution and external boundaries

| Scope | Raw bytes | Alternate view | Bytes |
| --- | ---: | --- | ---: |
| Native compiler plus QBE | 1,023,232 | both stripped | 655,816 |
| reference `trb` plus complete Go root | 275,388,970 | stripped `trb` plus unchanged Go root | 265,130,813 |

This is a 99.6284% raw controlled-payload reduction and a 99.7526% reduction
in the alternate stripped view. Native does not require Go to build these
applications. QBE, the platform C driver, assembler, LLD, dynamic linker, and
shared libraries remain explicit external prerequisites and appear in the
retained process and dependency inventories.

## Retained evidence

| Artifact | ID | Archive bytes | GitHub SHA-256 |
| --- | ---: | ---: | --- |
| benchmarksgame-build-fannkuch-redux | 9870863890 | 2,504,951 | `fb0c4273d700c2e2afdb1aa4e9950fd73e89d20a069be39562a3699ae875a182` |
| benchmarksgame-build-n-body | 9870860890 | 2,519,633 | `ae514450c4e2840078c00532fddbbcd13036056240148f9f0e0a9125a3df7178` |
| benchmarksgame-build-spectral-norm | 9870860370 | 2,507,581 | `44a8399a564105ae5ffad0555341751431334356b3875b287b1bb4b26f7e6eda` |

This result retains all 891 extracted files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 892 files and excludes only this README and
itself. The tree includes complete identities, fixed-point evidence, process
traces, dependencies, correctness records, all raw observations,
independently reproduced medians, application artifacts, and distribution
inventories.

## Conclusion

For these exact sources, the accepted self-hosted Native compiler exceeds the
optimized Go backend on build wall time, compiler CPU, peak RSS, application
size, controlled distribution size, and artifact reproducibility. Runtime is
a separate result: Pure Go parity or better remains the minimum target, and
generated-code and runtime optimization remain the primary measured work.
