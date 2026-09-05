# Formal Stable-Array-Header Build Results on Linux arm64

The self-hosted Native compiler passes the complete formal backend-pair build
and distribution contract on all three registered TypeRB programs. In this
same-run comparison, Native needs 36.8% to 47.6% of the optimized Go backend's
build wall time, 15.4% to 18.0% of its compiler CPU time, and about 51% less peak
process-tree memory. These are build measurements, not application runtime.

Native raw applications are 99.21% to 99.33% smaller. Its compiler-plus-QBE
controlled payload is 1,030,008 bytes, compared with 275,388,970 bytes for
reference `trb` plus the complete pinned Go root. These exact workload results
are not a composite language ranking or a promise about arbitrary projects.

## Exact scope

- Native revision: `69ff52b5fe474c87628b132124c7d8e875e627a8`;
- TypeRB Go semantic reference:
  `0.4.4-dev@5dc09070cf7f88a569279f5e63982a6de59d692c`;
- immutable previous-Native release: `bootstrap-seed-2026-08-30`;
- target profile `linux-arm64-v0`, QBE 1.3, GCC 13.3.0, LLD 18.1.3,
  Go 1.27.1, and BenchExec `runexec` 3.35;
- three fresh GitHub-hosted `ubuntu-24.04-arm` jobs, each reporting four
  Neoverse-N2 logical CPUs and Linux 6.17; and
- successful formal run
  [33940299777](https://github.com/type-rb/type-rb-native/actions/runs/33940299777).

After a setup-only transition from the released seed, the candidate closes a
byte-identical 315,368-byte B2/B3/B4 fixed point with SHA-256
`54272506c86851443c07521618da6937084f0fa2cd81ce962dfb363eb2fc113f`.
Its target-neutral compiler QBE is 1,119,802 bytes with SHA-256
`6efdfdc8a9f6b50789fd0e2b3deef10732218d51e4e1ecad00e8a0e27c36874d`.
The ordinary Native compiler chain does not use Go or the reference compiler.

## Correctness and measurement integrity

Both backends checked, built, and ran each authored TypeRB source correctly
before timing. Each case alternated the two backends through two warmups and
eleven retained observations. All 66 retained builds returned status zero,
produced an application, and passed an untimed exact-output execution. All
12 warmup builds also passed. No sample, metric, or artifact is missing.

Every compiler process tree ran under BenchExec with the registered filesystem,
CPU, memory, network, cache, and process-closure controls. Independently
rerunning the checked-in summarizer reproduces all six median rows byte for
byte. The retained raw and stripped application files match their recorded
byte counts and SHA-256 values; each original GitHub archive was also checked
against its published digest.

## Compiler measurements

Times are complete compiler-process-tree medians in seconds. RSS is peak
process-tree memory in bytes. The ratio divides Go build wall time by Native
build wall time; a value above one favors Native.

| Case | Native wall | Go wall | Go / Native wall | Native CPU | Go CPU | Native RSS | Go RSS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | 0.274102 | 0.575304 | 2.099 | 0.061248 | 0.396291 | 78,090,240 | 159,735,808 |
| n-body | 0.276702 | 0.664091 | 2.400 | 0.088601 | 0.493573 | 78,237,696 | 162,435,072 |
| spectral-norm | 0.218023 | 0.593057 | 2.720 | 0.057494 | 0.374197 | 78,049,280 | 160,260,096 |

These fresh jobs are not an interleaved comparison with an earlier Native
revision. Changes in absolute times between snapshot dates do not establish
an optimization's causal effect; use focused same-host A/B evidence for that.

## Application artifacts

Each Native case reproduced one byte-identical application across all eleven
retained builds. Each Go case produced eleven correct byte variants, retained
as evidence rather than hidden. The raw medians and separately verified
stripped artifacts are:

| Case | Native raw median | Go raw median | Native stripped | Go stripped |
| --- | ---: | ---: | ---: | ---: |
| fannkuch-redux | 18,888 | 2,808,692 | 18,880 | 1,887,832 |
| n-body | 22,304 | 2,815,354 | 22,296 | 1,887,832 |
| spectral-norm | 19,552 | 2,809,882 | 19,544 | 1,887,832 |

## Controlled distribution and external boundaries

| Scope | Raw bytes | Alternate view | Bytes |
| --- | ---: | --- | ---: |
| Native compiler plus QBE | 1,030,008 | both stripped | 662,592 |
| reference `trb` plus complete Go root | 275,388,970 | stripped `trb` plus unchanged Go root | 265,130,813 |

Native does not require Go to build these applications. QBE, the platform C
driver, assembler, LLD, dynamic linker, and shared libraries remain explicit
external prerequisites. Their identities and roles appear in the retained
process and dependency inventories; they are not claimed to have disappeared.

## Retained evidence

| Artifact | ID | Archive bytes | GitHub SHA-256 |
| --- | ---: | ---: | --- |
| benchmarksgame-build-fannkuch-redux | 9961614730 | 2,506,415 | `2c3c2386459229eb90ac3aa73aa8500f61b94981d8fcabbb64e098985fd54747` |
| benchmarksgame-build-n-body | 9961616081 | 2,520,065 | `15c2cf906896ff9d1f7e0c55af7e7e33e6276bc519d9d21946e150806b6927e1` |
| benchmarksgame-build-spectral-norm | 9961615219 | 2,507,465 | `16728231ff9788554db84d3e0cb8165eb7a1e22a8e9ee7e53a1042ffd52ce0eb` |

This result retains all 891 extracted files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 892 files and excludes only this README and
itself. The tree contains identities, fixed-point evidence, process traces,
dependencies, correctness records, raw observations, independently reproduced
medians, application artifacts, and distribution inventories.

Repository copies of generated text remove trailing horizontal whitespace and
extra blank lines at end of file. Binary application artifacts are unchanged;
the artifact table records the SHA-256 of each original GitHub archive.

## Conclusion

For these exact sources, Native improves on the optimized Go backend's build
wall time, compiler CPU, peak memory, application size, controlled distribution
size, and artifact reproducibility. This does not establish runtime parity
with Pure Go, nor does it measure a full long-running service or memory-leak
soak. Application execution remains a separate benchmark result.
