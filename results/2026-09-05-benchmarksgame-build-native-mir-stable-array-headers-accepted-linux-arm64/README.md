# Accepted Stable-Array-Header Build Results on Linux arm64

All 66 retained builds and 12 warmups pass at accepted Native revision
`5a23176040fee3541ed8578115622ffcd7aa2733`. On these three identical TypeRB
sources, Native needs 39.7% to 44.8% of the optimized Go backend's build wall
time, 15.7% to 16.9% of its compiler CPU time, and about 51% less peak
process-tree memory. These are complete compiler-process-tree measurements;
application runtime is measured separately.

## Exact scope

- successful [formal run 33949401013](https://github.com/type-rb/type-rb-native/actions/runs/33949401013);
- Native revision `5a23176040fee3541ed8578115622ffcd7aa2733`;
- TypeRB Go reference `0.4.4-dev@5dc09070cf7f88a569279f5e63982a6de59d692c`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Linux arm64, QBE 1.3, GCC 13.3.0, LLD 18.1.3, Go 1.27.1, and
  BenchExec `runexec` 3.35; and
- three fresh `ubuntu-24.04-arm` jobs, each with four Neoverse-N2 logical CPUs.

A setup-only transition from the released compiler precedes the ordinary
B2/B3/B4 chain. Its byte-identical 315,256-byte compiler has SHA-256
`11276336cdf558bce26e0a53dcbf935db4cfa3ae81a96353a2856327467bcd4f`.
Target-neutral compiler QBE is 1,119,022 bytes, SHA-256
`55b1f79c8e0362080b4b5076669d7047c19850fb6ae1b8e8f7f47a0208fcb67d`.
The ordinary Native compiler chain does not use Go or the reference compiler.

## Measurements

Times are medians in seconds; memory and artifacts are bytes. Lower is better.
The two backends alternate through two warmups and eleven retained builds per
case, with the same authored source, warm compiler caches, clean output,
page-cache reset, CPU allocation, memory limit, and process isolation.

| Case | Native wall | TypeRB Go wall | Native CPU | TypeRB Go CPU | Native memory | TypeRB Go memory |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | 0.204561 | 0.456613 | 0.055081 | 0.344847 | 78,077,952 | 159,281,152 |
| n-body | 0.215788 | 0.507726 | 0.067501 | 0.399412 | 78,094,336 | 162,295,808 |
| spectral-norm | 0.156149 | 0.393715 | 0.055139 | 0.350821 | 78,065,664 | 160,374,784 |

Every retained build succeeds and every produced application passes its
untimed exact-output execution. Independently rerunning the checked-in
summarizer reproduces all six median rows byte for byte. All observations,
including warmups, remain in the raw evidence. This fresh snapshot is not an
interleaved A/B comparison with an earlier Native revision; absolute changes
between snapshot dates do not isolate an optimization's effect.

| Case | Native raw median | TypeRB Go raw median | Native stripped | TypeRB Go stripped |
| --- | ---: | ---: | ---: | ---: |
| fannkuch-redux | 18,888 | 2,808,692 | 18,880 | 1,887,832 |
| n-body | 22,128 | 2,815,362 | 22,120 | 1,887,832 |
| spectral-norm | 19,552 | 2,809,882 | 19,544 | 1,887,832 |

Each Native case reproduces one byte-identical application in all eleven
retained builds. Each TypeRB Go case has eleven correct byte variants; the
variation is retained, not filtered. Native's raw applications are at least
99.21% smaller for this corpus.

## Distribution boundary

| Controlled payload | Raw bytes | Alternate form | Bytes |
| --- | ---: | --- | ---: |
| Native compiler plus QBE | 1,029,896 | Both stripped | 662,480 |
| Reference compiler plus complete Go root | 275,388,970 | Stripped compiler, unchanged Go root | 265,130,813 |

QBE, the platform C driver, assembler, LLD, dynamic linker, and shared libraries
remain explicit Native prerequisites. Process traces and dependency inventories
retain their identities and roles. The controlled payload is not a complete
operating-system or SDK distribution, nor a claim that external tools vanished.

## Retained evidence

| Artifact | ID | Archive bytes | GitHub SHA-256 |
| --- | ---: | ---: | --- |
| benchmarksgame-build-fannkuch-redux | 9964347228 | 2,506,061 | `4313e41650496c2b52a24bd4d5262afe6e9e28424cb3949a09143c39d6af9ef6` |
| benchmarksgame-build-n-body | 9964347206 | 2,520,012 | `407a08a02f2f9532c1ceb30dd43d95ec4218a9015ede1c06b66e1aa6252600f6` |
| benchmarksgame-build-spectral-norm | 9964347079 | 2,507,432 | `97f300e33ab1e033b30954775e168eb195835d8bd25710e0d41958b2eea79d44` |

`EVIDENCE_SHA256SUMS` inventories every extracted file, excluding only this
README and the checksum inventory itself. Repository text copies normalize
trailing horizontal whitespace and end-of-file blank lines; binary artifacts
remain unchanged. The table identifies the original GitHub archives.

The earlier `69ff52b5` build result remains separate rejected-candidate history.
This accepted result does not establish runtime parity with Pure Go, measure
a production service, or replace long-running memory-soak evidence.
