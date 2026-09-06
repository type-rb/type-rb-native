# Array-loop proof result diagnostic

Status: the standalone candidate **fails** the unchanged build-cost contract
for [issue #303](https://github.com/type-rb/type-rb-native/issues/303).
This is diagnostic evidence, not an accepted optimization or a Pages update.

The verifier returns a Boolean completion status internally and appends selected
origins into a private result. Its existing Array-returning boundary publishes
the result only after complete verification, or returns `[-1]` on failure.
All 37 structural failure conditions and selection rules remain in place;
repeated managed failure returns become scalar returns. No validation is skipped.

The exact source patch applies to
`ad7cd377c061bc25f3eea7b68fb57a855b180f1d`, which integrates the independent
readonly-binding correction from PR #306. The comparison baseline remains
`1afd60c2c7257ed34fd2a2aa70cb8b9164433009`; it is not moved to absorb that fix.

| Ordinary build metric | Baseline median | Candidate median | Ratio |
| --- | ---: | ---: | ---: |
| Wall (s) | 1.515346416 | 1.595723166 | 1.0530418320 |
| CPU (s) | 1.495862 | 1.580077 | 1.0562986425 |
| Root RSS (bytes) | 40288256 | 40124416 | 0.9959333062 |

Two warmups and seven retained observations per role are interleaved. All 18
builds reproduce their exact-source compiler bytes. Both roles pass every
retained 2.0 catastrophic check. Wall and CPU fail 1.05; RSS passes.
The source was not retried unchanged to rescue this result.

B2/B3/B4 SHA256 is
`d896b323fe058379b90faefa68ba20d9ac3c120c17e3899e7bc6eab70302b0bd`.
Complete compiler size is 349256 bytes, Mach-O text is 247904 bytes, and
target-neutral compiler QBE is 1110140 bytes. The complete compiler suite passes
133 tests; 75 corpus cases pass at all three generations (225 rows), including
invalid check/emit/build diagnostics, no external tool execution for invalid
source, repeated and adjacent QBE identity, runtime failures and cleanup.
The three numeric benchmark QBE outputs equal the prior outlined candidate's
outputs. No new runtime speedup is inferred from that identity.
Current-source full root recovery and hosted acceptance were not run for this
standalone rejected-cost candidate.

The unchanged [observer](../2026-09-06-mir-loop-bounds-diagnostic-darwin-arm64/build-cost-observer.py)
uses monotonic wall time and wait4 CPU/orchestration-root RSS. Each compiler
builds its own source closure using QBE 1.3, `/usr/bin/cc` and
`darwin-arm64-v0`. Owned correctness batches finished before measurement.
Host: Apple M2 Pro, 10 logical CPUs, 32 GiB RAM, macOS 26.6.2; Apple clang
21.0.0 (clang-2100.1.1.101). Reference revision:
`5dc09070cf7f88a569279f5e63982a6de59d692c`. Warm-cache local execution,
without CPU affinity, controlled frequency or host-wide isolation.

The next source-distinct diagnostic investigates repeated allocation of an
already opaque projection row. This result alone does not authorize retaining
the implementation or changing any acceptance threshold.
