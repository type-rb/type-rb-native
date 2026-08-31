# Formal Native Array Address A/B Result on Linux arm64

The shared Array-address bounds optimization passes its registered
correctness, fixed-point, compactness, build-cost, and runtime contract. A
single target-neutral unsigned comparison replaces the lower-bound,
upper-bound, and combined-invalid predicate after the existing negative-index
adjustment.

Across the exact checked-in programs, median wall time improves by 4.69% to
7.93% and median CPU time improves by 4.67% to 7.97%. QBE IL, compiler, and
application executable sizes all become smaller.

This is an implementation result for these exact programs, inputs, compiler
revisions, and toolchains. It is not a language-wide performance claim.

## Exact scope

- Native baseline commit:
  `80c9575632176b5d591e5036499281d15439c017`;
- candidate implementation commit:
  `ef985cf853d95952a38409c402e5f35a5722bc51`;
- measured pull-request merge commit:
  `7cd9de68d86be7a5f6ed58bdd49f3b536d1bf850`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Native target profile `linux-arm64-v0`, QBE 1.3, GCC 13.3.0, and
  LLD 18.1.3;
- BenchExec `runexec` 3.35 on one pinned Neoverse-N2 logical CPU with a 4 GB
  process-tree limit; and
- successful formal run
  [33370746877](https://github.com/type-rb/type-rb-native/actions/runs/33370746877).

The candidate keeps the existing negative-index adjustment and the same bounds
failure path. For every nonnegative Array length, unsigned `index < length` is
true exactly when the adjusted signed index is neither negative nor greater
than or equal to the length. The bounded inline-address policy and String
indexing remain unchanged.

## Runtime result

Each case alternated baseline and candidate through two warmup rounds and
eleven retained rounds. All 78 processes completed successfully; each retained
candidate has 11/11 passing observations. Every process returned zero, wrote
empty stderr, and matched the checked-in expected stdout exactly.

| Case | Input | Baseline wall | Candidate wall | Ratio | Baseline CPU | Candidate CPU | Ratio | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| fannkuch-redux | 10 | 1.08757 s | 1.03652 s | 0.953060 | 1.08533 s | 1.03462 s | 0.953277 | target passes |
| n-body | 1,000,000 | 0.578926 s | 0.533005 s | 0.920679 | 0.576711 s | 0.530726 s | 0.920263 | control passes |
| spectral-norm | 5,500 | 10.9241 s | 10.3182 s | 0.944535 | 10.9220 s | 10.3162 s | 0.944534 | control passes |

The registered maximum candidate ratio is 0.97 for `fannkuch-redux` and 1.02
for both controls, applied independently to wall and CPU medians. Median
process-tree memory is unchanged at 438,272 bytes for `fannkuch-redux` and
524,288 bytes for `n-body`; `spectral-norm` decreases from 1,200,128 to
1,196,032 bytes.

## Generated code and application size

QBE 1.3 lowers the baseline bounds predicate to `cmp`, `cset`, `cmp`, `cset`,
`orr`, `cmp`, and a conditional branch. The candidate lowers it to one `cmp`
and one unsigned `bcc`. The retained assembly extracts prove the same shared
helper change in all six baseline/candidate applications.

| Case | Baseline QBE | Candidate QBE | Ratio | Baseline raw | Candidate raw | Ratio | Baseline stripped | Candidate stripped | Ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| fannkuch-redux | 49,018 | 48,958 | 0.998776 | 18,512 | 18,480 | 0.998271 | 18,504 | 18,472 | 0.998271 |
| n-body | 63,409 | 63,349 | 0.999054 | 22,344 | 22,312 | 0.998568 | 22,336 | 22,304 | 0.998567 |
| spectral-norm | 48,063 | 48,003 | 0.998752 | 18,920 | 18,888 | 0.998309 | 18,912 | 18,880 | 0.998308 |

Every emitted QBE file shrinks by 60 bytes, and every raw and stripped
executable shrinks by 32 bytes. These results pass the registered no-growth QBE
limit and 1.001 application-size maximum.

## Self-hosted compiler closure

The released seed performed setup-only transitions to each measured compiler.
The baseline closes an exact 268,336-byte B2/B3/B4 fixed point with SHA-256
`ad0f8cf04db33bad796e0c303c04500fa1c30f2a7ef5cf0ea2ee5de8ccaa9090`.
The candidate closes an exact 268,248-byte B2/B3/B4 fixed point with SHA-256
`6ced62abb82a85088556d849826da97613bdb7b0dfd0860413a0f9672f363e41`.
The 0.999672 size ratio passes the registered 1.001 maximum.

The candidate fixed-point QBE SHA-256 is
`8fd0be84987bb2103b5e0f49f5ee1a55cc254813980b1cd4d40eb60e4a045f9f`.
Candidate B2-to-B3 and B3-to-B4 builds take 1.06 and 1.05 seconds, compared
with 1.06 seconds for both baseline generations. Candidate peak RSS differs by
less than 0.07%. Every registered build-time and RSS guardrail passes.

## Measurement integrity and retained evidence

The controller pinned every process to logical CPU 0, dropped the Linux page
cache before every observation, disabled swap and network access, mounted `/`
read-only, and isolated the home directory in a non-persistent overlay. The
evidence contains no nonzero status, signal, timeout, output mismatch, missing
metric, incomplete median, or leftover temporary file.

GitHub published artifact `native-runtime-ab-33370746877-1` as artifact ID
9750165405, 426,711 archive bytes, with archive SHA-256
`84fffc1d2f29de756f27a761fccd8abad92a72b2fba93d55fe6d61359ecb61da`.
This result retains all 662 extracted artifact files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 663 files and excludes only this README and
itself.

- [`compiler-comparison-evidence`](native-runtime-ab-33370746877-1/compiler-comparison-evidence)
  records compiler size, build time, and RSS decisions.
- [`application-evidence`](native-runtime-ab-33370746877-1/application-evidence)
  and [`applications`](native-runtime-ab-33370746877-1/applications) retain
  application sizes, exact hashes, emitted QBE, generated assembly,
  executables, helper-call inventories, and Array-helper assembly extracts.
- Each `runtime-*-evidence` tree retains correctness results, all 26
  observation directories, raw metrics, medians, and threshold evaluations.
- [`baseline-bootstrap-evidence`](native-runtime-ab-33370746877-1/baseline-bootstrap-evidence)
  and [`candidate-bootstrap-evidence`](native-runtime-ab-33370746877-1/candidate-bootstrap-evidence)
  retain fixed-point identities, measurements, process traces, and executable
  inventories.
- [`workflow-evidence`](native-runtime-ab-33370746877-1/workflow-evidence) and
  [`host-evidence`](native-runtime-ab-33370746877-1/host-evidence) retain exact
  workflow, toolchain, runner, isolation, cache, and cleanup evidence.

## Conclusion

One target-neutral predicate removes five AArch64 hot-path instructions while
preserving positive, negative, and failing Array indexing. The shared change
improves all three measured numeric programs and makes every measured artifact
smaller. Further optimization should continue from another measured
generated-code bottleneck rather than expanding Array-address logic at each
call site.
