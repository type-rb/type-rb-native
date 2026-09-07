> Storage update: detailed files are preserved in the verified public archive
> identified by [ARCHIVE.json](ARCHIVE.json). Tables and measurements remain in Git.
> Original reports and every archived file are included unchanged in that archive.

# Accepted Checked-Boolean-Branch Build Results on Linux arm64

All 66 retained builds and 12 warmups pass at accepted Native revision
`85e8d49bf256aed37332c68ef19cd7dea7afb977`. On these three identical TypeRB
sources, Native uses 38.7% to 44.0% of the optimized Go backend's build wall
time, 15.9% to 16.7% of its compiler CPU time, and 47.9% to 48.6% of its peak
process-tree memory. Application execution time is a separate measurement;
this is not a build comparison against handwritten Pure Go programs.

## Exact scope

- successful [formal run 34016844616](https://github.com/type-rb/type-rb-native/actions/runs/34016844616), attempt 1;
- Native revision `85e8d49bf256aed37332c68ef19cd7dea7afb977`, accepted in
  [PR #291](https://github.com/type-rb/type-rb-native/pull/291);
- TypeRB reference `0.4.4-dev@5dc09070cf7f88a569279f5e63982a6de59d692c`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Linux arm64, QBE 1.3, GCC 13.3.0, LLD 18.1.3, Go 1.27.1 and
  BenchExec `runexec` 3.35; and
- three fresh `ubuntu-24.04-arm` jobs, each with four Neoverse-N2 logical CPUs.

The setup-only transition precedes the ordinary B2/B3/B4 chain, whose three
compilers have identical 298,752-byte artifacts and SHA-256
`56e239c94847999c482dc57b99ae36df80b976322253cdcfa242ef203ec2949d`.
The compiler's target-neutral QBE is 1,055,831 bytes, SHA-256
`7714587dfc1e215cdfb69732ef236c70b6c5743af4a8c146ca848820960050d1`.
The reference compiler remains a comparison control, not an ordinary Native
regeneration dependency. Later source-organization revisions are not relabelled
as the compiler measured here.

## Measurements

Times are medians in seconds; memory and artifacts are bytes. Lower is better.
The backends alternate through two warmups and eleven retained builds per
case, with identical authored TypeRB source, warm compiler caches, clean
output, page-cache reset, CPU allocation, memory ceiling and process isolation.
The untimed correctness executions use inputs 7, 1,000 and 100 respectively.

| Case | Native wall | TypeRB Go wall | Native CPU | TypeRB Go CPU | Native memory | TypeRB Go memory |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | 0.212226 | 0.482819 | 0.056087 | 0.350922 | 77,852,672 | 160,239,616 |
| n-body | 0.238483 | 0.554823 | 0.067157 | 0.402026 | 78,028,800 | 162,816,000 |
| spectral-norm | 0.155511 | 0.402228 | 0.054197 | 0.341067 | 77,803,520 | 160,514,048 |

Every build and every untimed exact-output application execution passes.
Independent checks verify all 78 raw observations, their rotating schedule,
status, raw process metrics and output; the checked-in summarizer reproduces
all six median rows byte for byte. Warmups are retained but do not enter the
medians. This fresh cross-language snapshot is not an interleaved comparison
against a previous Native revision, so cross-date differences do not isolate
the effect of an optimization.

| Case | Native raw median | TypeRB Go raw median | Native stripped | TypeRB Go stripped |
| --- | ---: | ---: | ---: | ---: |
| fannkuch-redux | 18,760 | 2,808,692 | 18,752 | 1,887,832 |
| n-body | 22,032 | 2,815,354 | 22,024 | 1,887,832 |
| spectral-norm | 19,424 | 2,809,882 | 19,416 | 1,887,832 |

All eleven Native builds per case reproduce one identical application. Each
TypeRB Go case has eleven correct byte variants, retained without filtering.
All twelve archived raw/stripped application binaries match their recorded
sizes and hashes. Native's raw applications are at least 99.21% smaller in
this corpus; that is not a claim about every program or a complete distribution.

## Distribution boundary

| Controlled payload | Raw bytes | Alternate form | Bytes |
| --- | ---: | --- | ---: |
| Native compiler plus QBE | 1,013,392 | Both stripped | 645,976 |
| Reference compiler plus complete Go root | 275,388,970 | Stripped compiler, unchanged Go root | 265,130,813 |

The C driver, assembler, LLD, dynamic linker and shared libraries remain
explicit Native prerequisites. Dependency inventories and process traces
retain their roles. This controlled payload is not a complete operating-system
or SDK distribution, and no external tools have been hidden or replaced.

## Retained evidence

| Artifact | ID | Archive bytes | GitHub SHA-256 |
| --- | ---: | ---: | --- |
| benchmarksgame-build-fannkuch-redux | 9984190504 | 2,506,564 | `b49fa47dfa0c1c6016cfd569484dd7e2437d87b5835874e205ff0f7bd4270c93` |
| benchmarksgame-build-n-body | 9984194900 | 2,520,033 | `5ed1b9f08dd6b2ed7e6632ce8b96883b792cbd40328c931946643f59656e96d2` |
| benchmarksgame-build-spectral-norm | 9984193880 | 2,507,386 | `1e1d27fb1b961de0de0730b7d26aeb2a7d2253aa3982e1e2ae78f20089fc752b` |

Downloaded archive hashes match the GitHub digests. `EVIDENCE_SHA256SUMS`
inventories all 891 extracted files, excluding only this README and the
inventory itself. Text copies normalize CRLF, trailing horizontal whitespace
and end-of-file blank lines without changing metric values; application
binaries remain unchanged. Original archive identities are retained above.

This result establishes neither runtime parity with Pure Go nor long-running
service or leak behavior. See the [same-revision runtime result](../2026-09-06-benchmarksgame-runtime-checked-boolean-branches-linux-arm64/README.md)
for the execution-time comparison.
