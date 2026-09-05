# Accepted Stable-Array-Header Runtime Results on Linux arm64

All 462 retained observations and 84 warmups pass at accepted Native revision
`5a23176040fee3541ed8578115622ffcd7aa2733`. Native needs 1.12x to 3.45x the
wall time of the pinned Pure Go programs across these three numeric kernels.
Spectral-norm is closer to parity; fannkuch-redux and n-body still have large
gaps. Pure Go parity or better remains the minimum runtime objective.

Against the identical-source TypeRB Go control, Native uses about 36.1% less
wall time on spectral-norm and needs 1.69x to 1.84x the time on the other two
programs. Its peak process-tree memory is 82.68% to 87.28% lower across both
CPU lanes. Memory and time are separate metrics, not a measured energy claim.

## Exact scope

- successful [formal run 33949399906](https://github.com/type-rb/type-rb-native/actions/runs/33949399906), attempt 1;
- Native revision `5a23176040fee3541ed8578115622ffcd7aa2733`;
- TypeRB reference `0.4.4-dev@5dc09070cf7f88a569279f5e63982a6de59d692c`;
- Benchmarks Game revision `40296663ed350d5fe4a6ab5e367bab61cb77c219`;
- inputs: fannkuch-redux 12, n-body 50,000,000, spectral-norm 5,500;
- three fresh `ubuntu-24.04-arm` jobs, each with four Neoverse-N2 logical CPUs;
- pinned BenchExec `runexec` 3.35, QBE 1.3, and the complete compiler commands,
  flags, versions, source hashes, and host inventories retained per case; and
- separate one-core and four-core process-tree CPU allocations, two warmup
  rounds, eleven retained rotating rounds, and exact published-output checks.

This measures already-built application processes, including process startup
and Java JIT activity. It does **not** include compilation. Swap is disabled,
the page cache is dropped before each observation, and every process tree uses
the registered isolated container and 4 GB memory ceiling. This is not a
persistent-service steady-state or leak test.

## Runtime medians

Wall times are seconds; lower is better. Pure Go uses its separately pinned
upstream program. Only the TypeRB Go/Native pair holds the authored TypeRB
source and portable semantics constant.

| Case | Lane | Native wall | TypeRB Go wall | Pure Go wall | Native / Pure Go |
| --- | --- | ---: | ---: | ---: | ---: |
| fannkuch-redux | one core | 84.8518 | 46.1186 | 24.6002 | 3.45x |
| n-body | one core | 10.4556 | 6.17429 | 3.59937 | 2.90x |
| spectral-norm | one core | 3.59797 | 5.63518 | 3.21855 | 1.12x |
| fannkuch-redux | four cores | 84.8546 | 46.0818 | 24.6671 | 3.44x |
| n-body | four cores | 10.4544 | 6.17244 | 3.60003 | 2.90x |
| spectral-norm | four cores | 3.59643 | 5.63432 | 3.21763 | 1.12x |

| Case | One-core Native CPU seconds | Native peak memory bytes | TypeRB Go peak memory bytes |
| --- | ---: | ---: | ---: |
| fannkuch-redux | 84.8501 | 524,288 | 3,026,944 |
| n-body | 10.4521 | 524,288 | 3,260,416 |
| spectral-norm | 3.5955 | 1,228,800 | 7,184,384 |

All seven implementations, including C, C++, Rust, and Java, remain in the six
`medians.tsv` tables and the [benchmark explorer](https://type-rb.github.io/type-rb-native/benchmarks/).
The four-core allocation does not rewrite single-threaded programs to use
parallelism. The selected Rust fannkuch-redux and spectral-norm programs do
exploit multiple cores; their four-core medians must not be substituted into
the one-core comparison. There is no aggregate language score.

## Attribution and MIR scope

The measured revision includes accepted guarded Integer arithmetic and the
immutable-parameter Array-header optimization from
[PR #246](https://github.com/type-rb/type-rb-native/pull/246). The
[focused same-host A/B run](https://github.com/type-rb/type-rb-native/actions/runs/33946793548)
is its causal acceptance evidence: spectral-norm wall time falls by 11.867%
against the previous Native baseline with unchanged median RSS and effectively
neutral controls. This complete rerun measures every implementation afresh;
changes between snapshot dates do not independently isolate that optimization.

MIR still covers selected scalar leaves, exact Integer/Float Array reductions,
guarded arithmetic, and bounded region facts. General control flow, allocation,
I/O, and complete removal of direct-emitter ownership remain unfinished. The
later compiler-only [PR #250](https://github.com/type-rb/type-rb-native/pull/250)
preserves generated applications; its smaller compiler is not relabelled as
the compiler measured here. Rejected `69ff52b5` measurements and the rejected
Integer-halving diagnostic remain separate history, not this accepted result.

## Bootstrap and retained evidence

The immutable `bootstrap-seed-2026-08-30` compiler supplies setup provenance.
The ordinary B2/B3/B4 chain closes to one byte-identical 315,256-byte compiler,
SHA-256 `11276336cdf558bce26e0a53dcbf935db4cfa3ae81a96353a2856327467bcd4f`.
Its target-neutral compiler QBE has SHA-256
`55b1f79c8e0362080b4b5076669d7047c19850fb6ae1b8e8f7f47a0208fcb67d`.
Go is an independent correctness/build control, not part of this ordinary
Native compiler chain. QBE, CC, assembler, linker, and system libraries remain
explicit external prerequisites.

| Runtime artifact | ID | Archive bytes | GitHub SHA-256 |
| --- | ---: | ---: | --- |
| fannkuch-redux | 9966042090 | 392,584 | `73c88a25fd1242f94dc3c66e82696ebcd9393949d89023a29df5c0d4e1068870` |
| n-body | 9964603361 | 388,384 | `c2cac42517283de5e1aa8d3805c2f280439c23d373cf394c8ab6baabcccc79f7` |
| spectral-norm | 9964491688 | 386,390 | `6e11ae69e33e524b2cf9f3cc830e4c477487f10c4878184c8fb9b574ebe49bfb` |

Downloaded archive hashes match the published digests. Independent local
checks verify all 546 process rows, the complete rotating schedule, successful
statuses, and all six byte-reproduced median tables using the checked-in
summarizer. No outlier or failure is omitted. Logs, process metrics, output
payloads, environments, and bootstrap identities remain in the extracted
trees. `EVIDENCE_SHA256SUMS` inventories all 4,137 extracted files. Text copies
normalize CRLF, trailing horizontal whitespace, and end-of-file blank lines;
metric values are unchanged. The original archive identities remain above.

See the [separate same-revision build result](../2026-09-05-benchmarksgame-build-native-mir-stable-array-headers-accepted-linux-arm64/README.md)
for compiler time, memory, application size, and complete distribution
boundaries. Long-running memory evidence remains a separate lifecycle layer.
