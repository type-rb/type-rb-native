# Formal Benchmarks Game Build Results on Linux arm64

The formal backend-pair build and distribution layer passes its complete
correctness, isolation, repetition, process-closure, and evidence contract. On
these three byte-identical TypeRB programs, the self-hosted Native compiler is
2.29x to 2.58x faster in wall time than the optimized Go path, uses 6.14x to
6.41x less compiler CPU time, and uses about 51% less peak process-tree memory.

Native's raw application artifacts are 99.21% to 99.34% smaller than the Go
artifacts. Its compiler-plus-QBE controlled payload is 982,816 bytes, compared
with 275,200,753 bytes for reference `trb` plus the complete pinned Go
distribution. These are backend results for exact programs and toolchains, not
a composite language ranking.

## Exact scope

- measured Native revision:
  `fc98cdf7c66f6f58c28b1c09a0deca89b9b3112c`;
- TypeRB Go semantic reference:
  `0.4.3-dev@2cf63e95b4fc1a92f6094e2c89c47fb75262adae`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Native target profile `linux-arm64-v0`, pinned QBE 1.3, GCC 13.3.0,
  LLD 18.1.3, and Go 1.27.0;
- BenchExec `runexec` 3.35 with a 4 GB process-tree limit;
- three separate fresh GitHub-hosted `ubuntu-24.04-arm` jobs, each reporting
  four Neoverse-N2 logical CPUs and Linux 6.17; and
- successful formal run
  [33356350386](https://github.com/type-rb/type-rb-native/actions/runs/33356350386).

The released compiler performed a setup-only transition to the measured
candidate. In every job, that candidate then closed a byte-identical
268,176-byte B2/B3/B4 fixed point with SHA-256
`749c4aa6313c13054b459be382cb95e546cbbdd9ffa04067c3c92547db5d1904`.
No successful Go or reference-compiler process occurs in those transitions.

## Correctness and measurement integrity

Both backends checked, built, and ran each authored TypeRB source correctly
before timing. Every measured build then returned status zero, produced an
application, and passed an untimed small-input execution with status zero,
empty stderr, and exact published stdout.

Each case alternated the two backends through two warmup rounds and eleven
retained rounds. All 12 warmup and all 66 retained observations passed across
the three jobs. Every retained candidate has 11/11 successful samples; there
are no missing metrics, nonzero exits, signals, timeouts, output differences,
or incomplete medians.

Every compiler process tree ran under BenchExec on the same four logical CPUs
with `/` read-only, `/home` isolated in a non-persistent overlay, and only the
registered workspace and BenchExec temporary directory writable. The output
was deleted and the Linux page cache was dropped before every observation.
Swap was disabled. The Go build and module caches were explicit and remained
warm after the two registered warmups.

The checked-in `summarize.awk` was unchanged from the measured revision.
Re-running it independently over all three `raw.tsv` files reproduces every
retained `medians.tsv` byte for byte.

## Compiler measurements

Times are medians in seconds for the complete compiler process tree. RSS is
peak process-tree memory in bytes. The speedup columns divide Go by Native, so
a value above 1 favors Native.

| Case | Native wall | Go wall | Native speedup | Native CPU | Go CPU | Native CPU advantage | Native RSS | Go RSS | Native RSS reduction |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | 0.150626 | 0.389000 | 2.583x | 0.052509 | 0.322228 | 6.137x | 78,168,064 | 159,309,824 | 50.93% |
| n-body | 0.166934 | 0.421855 | 2.527x | 0.065420 | 0.406177 | 6.209x | 78,249,984 | 162,283,520 | 51.78% |
| spectral-norm | 0.210722 | 0.482205 | 2.288x | 0.054968 | 0.352088 | 6.405x | 78,233,600 | 160,534,528 | 51.27% |

The retained wall-time ranges remain separated:

| Case | Native retained min-max | Go retained min-max |
| --- | ---: | ---: |
| fannkuch-redux | 0.147355610-0.157281307 | 0.369499166-0.460598963 |
| n-body | 0.161110130-0.173970361 | 0.400638529-0.468877754 |
| spectral-norm | 0.195486618-0.226193717 | 0.466620177-0.556700037 |

## Application artifacts and reproducibility

Raw values below are retained medians and ranges. Each Native build reproduced
one byte-identical artifact across all eleven retained observations. Each Go
case produced eleven distinct byte variants; all remained correct, and the
variation is retained as evidence instead of invalidating its timing result.

| Case | Native raw median | Go raw median | Native reduction | Native range | Go range | Native variants | Go variants |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | 18,512 | 2,808,692 | 99.341% | 18,512-18,512 | 2,808,692-2,808,836 | 1 | 11 |
| n-body | 22,360 | 2,815,362 | 99.206% | 22,360-22,360 | 2,815,306-2,815,362 | 1 | 11 |
| spectral-norm | 18,840 | 2,809,898 | 99.330% | 18,840-18,840 | 2,809,826-2,809,898 | 1 | 11 |

The separately retained final correct artifacts have these stripped sizes:

| Case | Native stripped | Go stripped | Native reduction |
| --- | ---: | ---: | ---: |
| fannkuch-redux | 18,504 | 1,887,832 | 99.020% |
| n-body | 22,352 | 1,887,832 | 98.816% |
| spectral-norm | 18,832 | 1,887,832 | 99.002% |

The raw and stripped applications and their dynamic-library inventories are
deploy evidence. They are not included in either compiler distribution total.

## Controlled distribution and external boundaries

The controlled payload deliberately separates repository-selected build
components from platform prerequisites:

| Scope | Raw bytes | Alternate view | Bytes |
| --- | ---: | --- | ---: |
| Native compiler plus QBE | 982,816 | both stripped | 615,400 |
| reference `trb` plus complete Go root | 275,200,753 | stripped `trb` plus unchanged Go root | 264,986,006 |

This is a 99.6429% raw controlled-payload reduction and a 99.7678% reduction
in the alternate stripped view. The Go root contains 15,637 files and accounts
for 238,458,102 of the raw Go-controlled bytes.

Native does not require Go to build these applications. It does still require
the recorded external QBE binary and platform C toolchain. Representative
process traces observe the Native compiler, QBE, assembler, C driver, LLD, and
`collect2`; the Go path observes reference `trb`, `go`, `asm`, `compile`, and
`link`. Every successfully executed tool has its own resolved path, hash where
applicable, and dynamic-dependency record. The host assembler, C driver,
linker, and shared libraries remain explicit prerequisites rather than being
misreported as TypeRB-controlled payload.

## Retained evidence and independent audit

GitHub published these exact archives:

| Artifact | ID | Archive bytes | GitHub SHA-256 |
| --- | ---: | ---: | --- |
| benchmarksgame-build-fannkuch-redux | 9745285263 | 2,504,730 | `4b523a55965a40653308e33b1312d2c31002af286ad8b8cfd9c4e16349ed0147` |
| benchmarksgame-build-n-body | 9745286117 | 2,520,024 | `b23f49ee677ac596c8a9016cd6127f8d76721017eaf837da60dfdf5e71afc43c` |
| benchmarksgame-build-spectral-norm | 9745285647 | 2,506,453 | `684cedaad400e12ae23e74e8e588ed8b1b917804c01b2fef799c303852037399` |

The result retains all 891 extracted raw files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 892 files and excludes only this README and
itself.

- Each [`workflow-evidence`](benchmarksgame-build-fannkuch-redux/workflow-evidence)
  tree records exact revisions, runner, kernel, CPU, toolchains, packages,
  release metadata, and pinned archive hashes.
- Each [`bootstrap-evidence`](benchmarksgame-build-fannkuch-redux/bootstrap-evidence)
  and [`transition-evidence`](benchmarksgame-build-fannkuch-redux/transition-evidence)
  tree records the fixed point and the setup-only Go-free transition boundary.
- Each [`build-evidence`](benchmarksgame-build-fannkuch-redux/build-evidence)
  tree retains preflight correctness, all 26 observation directories, raw and
  independently reproduced medians, artifacts, process traces, dependencies,
  and complete distribution inventories.

## Conclusion and remaining work

For these exact sources, the self-hosted Native compiler already exceeds the
optimized Go path on build wall time, compiler CPU, peak RSS, application size,
controlled distribution size, and retained artifact reproducibility. It also
meets the intended no-Go application-build boundary while keeping QBE and the
platform toolchain explicit.

This does not erase the separate runtime result: Native remains 2.44x to 4.68x
slower than TypeRB Go on the three long numeric kernels. Generated-code and
runtime optimization therefore remain the primary measured performance work.
Persistent Web and Job behavior, long-running leak detection, package and
native-library boundaries, and incremental builds remain separate workloads.
