> Lifecycle: [complete source-era record](https://github.com/type-rb/type-rb-native/blob/bd483cfc5b51035d9fac193a74ee9d0eda2419ed/results/2026-09-06-benchmarksgame-runtime-checked-boolean-branches-linux-arm64/README.md).
> Historical checksum inventories refer to that full record, not this compact working set.

> Storage update: detailed files are preserved in the verified public archive
> identified by [ARCHIVE.json](ARCHIVE.json). Tables and measurements remain in Git.
> Original reports and every archived file are included unchanged in that archive.

# Accepted Checked-Boolean-Branch Runtime Results on Linux arm64

All 462 retained observations and 84 warmups pass at accepted Native revision
`85e8d49bf256aed37332c68ef19cd7dea7afb977`. Spectral-norm takes 3.3282 seconds
against Pure Go's 3.21923 seconds in the one-core lane: Native still needs
about 3.4% more time. Fannkuch-redux and n-body remain about 3.13x and 2.85x
Pure Go's time. The objective of matching or exceeding Pure Go is not met yet.

Against identical-source TypeRB Go, Native uses about 41.0% less wall time on
spectral-norm, but still needs about 1.66x to 1.68x the time for the other two
programs. Native uses substantially less peak process-tree memory in all six
comparisons. Memory and CPU time do not establish an energy or power claim.

## Exact scope

- successful [formal run 34016843633](https://github.com/type-rb/type-rb-native/actions/runs/34016843633), attempt 1;
- Native revision `85e8d49bf256aed37332c68ef19cd7dea7afb977`, accepted in
  [PR #291](https://github.com/type-rb/type-rb-native/pull/291);
- TypeRB reference `0.4.4-dev@5dc09070cf7f88a569279f5e63982a6de59d692c`;
- Benchmarks Game revision `40296663ed350d5fe4a6ab5e367bab61cb77c219`;
- inputs: fannkuch-redux 12, n-body 50,000,000 and spectral-norm 5,500;
- three fresh `ubuntu-24.04-arm` jobs, each with four Neoverse-N2 logical CPUs;
- pinned BenchExec `runexec` 3.35, QBE 1.3, complete commands, flags, versions,
  source hashes and host inventories retained per case; and
- one-core and four-core process-tree CPU allocations, two warmup rounds,
  eleven retained rotating rounds and exact published-output checks.

These are already-built application executions, including process startup and
Java JIT activity, not compilation time. Swap is disabled and the page cache
is dropped before each observation. Each process tree uses the registered
isolated container and 4 GB memory ceiling. This is not a persistent-service,
steady-state or memory-leak test.

## Runtime medians

Wall times are seconds; lower is better. Pure Go uses its separately pinned
upstream implementation. Only the TypeRB Native/Go pair holds the authored
TypeRB source and portable semantics constant.

| Case | Lane | Native wall | TypeRB Go wall | Pure Go wall | Native / Pure Go |
| --- | --- | ---: | ---: | ---: | ---: |
| fannkuch-redux | one core | 77.1176 | 45.9879 | 24.6115 | 3.13x |
| n-body | one core | 10.2644 | 6.17486 | 3.5998 | 2.85x |
| spectral-norm | one core | 3.3282 | 5.6367 | 3.21923 | 1.03x |
| fannkuch-redux | four cores | 77.0986 | 46.1178 | 24.6375 | 3.13x |
| n-body | four cores | 10.2655 | 6.17567 | 3.59885 | 2.85x |
| spectral-norm | four cores | 3.32774 | 5.63608 | 3.22078 | 1.03x |

| Case | One-core Native CPU seconds | Native peak memory bytes | TypeRB Go peak memory bytes |
| --- | ---: | ---: | ---: |
| fannkuch-redux | 77.1093 | 524,288 | 3,244,032 |
| n-body | 10.2619 | 524,288 | 3,035,136 |
| spectral-norm | 3.32588 | 1,212,416 | 7,188,480 |

All seven implementations, including C, C++, Rust and Java, remain in the six
median tables and the [benchmark explorer](https://type-rb.github.io/type-rb-native/benchmarks/).
Four-core allocation does not parallelize a single-threaded program. Selected
upstream implementations can exploit multiple cores and must not have their
four-core results substituted into a one-core comparison. There is no aggregate
language score, and these three numeric kernels do not cover web or job workloads.

## Attribution and MIR scope

This revision includes the accepted checked-Boolean branch optimization on top
of guarded Integer arithmetic and immutable-parameter Array-header reuse.
Its [same-run Native A/B evidence](https://github.com/type-rb/type-rb-native/actions/runs/34016548080)
records spectral-norm wall time 3.59727 to 3.32893 seconds, about 7.46% less,
and the smaller-input fannkuch control 0.514586 to 0.468150 seconds, about 9.02%
less. Those comparisons establish the optimization's effect against previous
Native, not parity with Pure Go. This complete rerun measures every language
afresh; differences between snapshot dates alone are not causal evidence.

MIR remains a partial migration: selected scalar leaves, Integer/Float Array
reductions, checked arithmetic/Boolean plans and bounded header facts are
implemented, while general control flow, allocation and I/O remain incomplete.
Later compiler-only source organization preserves generated programs but is
not relabelled as this measured revision. Rejected diagnostics and failed
premeasurement attempts remain separate from accepted measurements in the
[focused evidence](../2026-09-06-checked-boolean-branches-accepted-darwin-linux-arm64/README.md).

## Bootstrap and retained evidence

The immutable `bootstrap-seed-2026-08-30` supplies setup provenance. After the
setup-only transition, ordinary B2/B3/B4 generations have byte-identical
298,752-byte compilers, SHA-256
`56e239c94847999c482dc57b99ae36df80b976322253cdcfa242ef203ec2949d`.
Target-neutral compiler QBE is 1,055,831 bytes, SHA-256
`7714587dfc1e215cdfb69732ef236c70b6c5743af4a8c146ca848820960050d1`.
QBE, CC, assembler, linker and system libraries remain explicit prerequisites;
Go is a separate comparison control, not an ordinary regeneration dependency.

| Runtime artifact | ID | Archive bytes | GitHub SHA-256 |
| --- | ---: | ---: | --- |
| fannkuch-redux | 9985861453 | 392,610 | `a3c58ab4b4f5b717d8aad16cfb4bb3b912b741cb6ed95cf7c41f35dd00555704` |
| n-body | 9984440178 | 388,297 | `bd4734b9bba1efdb30b4493e5b3e5979a5a32cc9f4c18ccbfec37554ba8a850c` |
| spectral-norm | 9984333013 | 386,399 | `ef913697e772380154a20701d6389c87bda460e0d0f9ba112d213a1f1c89c3b8` |

Downloaded archive hashes match the GitHub digests. Independent checks verify
all 546 raw observations, rotating order, process status/metrics and exact
output, plus the untimed controls. The checked-in summarizer reproduces all six
median tables byte for byte, both before and after text normalization. All
42 adjacent-generation rows, medians and fixed-point identities are checked.
No failure or outlier is filtered from the retained runs.

`EVIDENCE_SHA256SUMS` inventories all 4,137 extracted files. Text copies normalize
CRLF, trailing horizontal whitespace and end-of-file blank lines; metric values
remain unchanged. Original archive identities are retained above.

See the [same-revision build result](../2026-09-06-benchmarksgame-build-checked-boolean-branches-linux-arm64/README.md)
for compilation time, memory, application size and distribution boundaries.
