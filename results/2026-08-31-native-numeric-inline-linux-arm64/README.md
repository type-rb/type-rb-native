# Formal Native Numeric Inline A/B Result on Linux arm64

The bounded non-loop numeric inline reserve passes its registered correctness,
fixed-point, compactness, build-cost, and runtime contract. On the exact
checked-in `spectral-norm` source at input 5,500, the candidate reduces median
wall time by 20.61% and median CPU time by 20.62%. The two registered control
programs are unchanged within measurement noise and do not regress.

This is an implementation result for these exact programs, inputs, compiler
revisions, and toolchains. It is not a language-wide performance claim.

## Exact scope

- Native baseline commit:
  `ae9b9d6dffa963413369285f7812286ada707df2`;
- candidate implementation commit:
  `9a0803926c515aed5354878c7eb7e64fd88865cc`;
- measured pull-request merge commit:
  `0fbd1afea0782808d719016cf333d3638be25058`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Native target profile `linux-arm64-v0`, QBE 1.3, GCC 13.3.0, and
  LLD 18.1.3;
- BenchExec `runexec` 3.35 on one pinned Neoverse-N2 logical CPU with a 4 GB
  process-tree limit; and
- successful formal run
  [33362034586](https://github.com/type-rb/type-rb-native/actions/runs/33362034586).

The candidate keeps the existing program-wide loop-local inline budget and
adds a separate numeric-only reserve of six operations for programs with at
most 32 functions and three operations for programs with 33 through 96
functions. Larger programs keep zero inline capacity. Array addressing outside
lexical loops remains on its helper path. The policy does not inspect source
names, function names, benchmark identities, paths, or inputs.

## Runtime result

Each case alternated baseline and candidate through two warmup rounds and
eleven retained rounds. All 78 processes completed successfully; each retained
candidate has 11/11 passing observations. Every process returned zero, wrote
empty stderr, and matched the checked-in expected stdout exactly.

| Case | Input | Baseline wall | Candidate wall | Ratio | Baseline CPU | Candidate CPU | Ratio | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| fannkuch-redux | 10 | 1.08839 s | 1.08746 s | 0.999146 | 1.08660 s | 1.08542 s | 0.998914 | control passes |
| n-body | 1,000,000 | 0.581677 s | 0.579375 s | 0.996042 | 0.579938 s | 0.576969 s | 0.994880 | control passes |
| spectral-norm | 5,500 | 13.7585 s | 10.9227 s | 0.793887 | 13.7565 s | 10.9199 s | 0.793799 | target passes |

The registered maximum candidate ratio is 1.05 for both control programs and
0.80 for `spectral-norm`, applied independently to wall and CPU medians.
Median process-tree memory was 438,272 versus 442,368 bytes for
`fannkuch-redux`, 524,288 bytes for both `n-body` candidates, and 1,204,224
versus 1,216,512 bytes for `spectral-norm`.

## Generated code and application size

The candidate preserves all Array-address helper counts. It removes the one
outlined Integer divide in `n-body`. In `spectral-norm`, it removes three of
four outlined Integer adds and both outlined Integer divides; the remaining
multiply and add retain their helper paths after eligibility and budget rules
are applied.

| Case | Baseline QBE | Candidate QBE | Ratio | Baseline raw | Candidate raw | Ratio | Baseline stripped | Candidate stripped | Ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fannkuch-redux | 49,018 | 49,018 | 1.000000 | 18,512 | 18,512 | 1.000000 | 18,504 | 18,504 | 1.000000 |
| n-body | 63,254 | 63,409 | 1.002450 | 22,360 | 22,344 | 0.999284 | 22,352 | 22,336 | 0.999284 |
| spectral-norm | 47,360 | 48,063 | 1.014844 | 18,840 | 18,920 | 1.004246 | 18,832 | 18,912 | 1.004248 |

Every value passes the registered maximum of 1.03 for QBE and 1.01 for raw and
stripped executables.

## Self-hosted compiler closure

The released seed performed a setup-only transition to each measured compiler.
The baseline then closed an exact 268,176-byte B2/B3/B4 fixed point with
SHA-256
`749c4aa6313c13054b459be382cb95e546cbbdd9ffa04067c3c92547db5d1904`.
The candidate closed an exact 268,336-byte B2/B3/B4 fixed point with SHA-256
`ad0f8cf04db33bad796e0c303c04500fa1c30f2a7ef5cf0ea2ee5de8ccaa9090`.
The 1.000597 size ratio passes the registered 1.001 maximum.

The candidate's B2-to-B3 and B3-to-B4 builds each took 1.05 seconds, compared
with 1.04 and 1.05 seconds for the baseline. Candidate peak RSS was equal for
the first retained generation and slightly lower for the second. All build
wall-time and RSS ratios pass the registered 1.05 maximum.

## Measurement integrity and retained evidence

The controller pinned every process to logical CPU 0, dropped the Linux page
cache before every observation, disabled swap and network access, mounted `/`
read-only, and isolated the home directory in a non-persistent overlay. The
evidence contains no nonzero status, signal, timeout, output mismatch, missing
metric, incomplete median, or leftover temporary file.

GitHub published artifact `native-runtime-ab-33362034586-1` as artifact ID
9747159814, 364,043 archive bytes, with archive SHA-256
`91d5c6971a524dbabb4188bc51f018b637cd70b24c38eccec255a81c4d9962b6`.
This result retains all 650 extracted artifact files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 651 files and excludes only this README and
itself.

- [`compiler-comparison-evidence`](native-runtime-ab-33362034586-1/compiler-comparison-evidence)
  records the compiler size, build-time, and RSS decisions.
- [`application-evidence`](native-runtime-ab-33362034586-1/application-evidence)
  and [`applications`](native-runtime-ab-33362034586-1/applications) retain
  application sizes, exact hashes, emitted QBE, executables, and helper-call
  inventories.
- Each `runtime-*-evidence` tree retains correctness results, all 26
  observation directories, raw metrics, medians, and threshold evaluations.
- [`baseline-bootstrap-evidence`](native-runtime-ab-33362034586-1/baseline-bootstrap-evidence)
  and [`candidate-bootstrap-evidence`](native-runtime-ab-33362034586-1/candidate-bootstrap-evidence)
  retain fixed-point identities, measurements, process traces, and executable
  inventories.
- [`workflow-evidence`](native-runtime-ab-33362034586-1/workflow-evidence) and
  [`host-evidence`](native-runtime-ab-33362034586-1/host-evidence) retain exact
  workflow, toolchain, runner, isolation, cache, and cleanup evidence.

## Conclusion

A small deterministic compiler policy closes a measured part of the Native
numeric-runtime gap without weakening Integer semantics, specializing for a
benchmark, or materially increasing compiler or application size. Further
optimization should continue from another measured generated-code bottleneck;
this result does not imply that all numeric workloads receive the same gain.
