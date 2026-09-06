# Readonly reference initialization — local Darwin arm64 verification

Candidate source: `dbde1d6e31e3f77436fb2d31a0da1b3f0d4e799e`,
[PR #306](https://github.com/type-rb/type-rb-native/pull/306),
[issue #305](https://github.com/type-rb/type-rb-native/issues/305).

Status: local correctness and cost checks pass. Hosted full acceptance is
separate and pending at this checkpoint. No runtime speedup or Pages update
is claimed.

## Boundary and correctness

Direct immutable record/Array local and parameter reads cannot initialize a
mutable binding. Grouping retains that checked provenance. Fresh construction,
function results, mutable aliases, scalar/String values, and shallow field or
nested Array reads preserve the pinned reference behavior. This is not a new
deep-readonly rule.

The recovery/QBE-enabled suites pass: root 95 tests (929.36 s), compiler 112
tests (164.92 s). These correctness durations are not comparative performance
measurements. Two focused tests cover 15 binding cases. Every one of the 72
corpus cases passes at B2/B3/B4 (216 rows), including repeated/adjacent QBE
identity and exact check/emit/build rejection before external tools, without
publication or temporary residue. Four negative fixtures are independently
rejected by the reference. The positive executable has exact matching output
on Native and both the Go and Ruby reference paths.

The preliminary positive fixture attempted record-field writes. That is not a
valid portability oracle: the pinned checker accepts them despite the
immutable-field specification, Go executes them, and Ruby fails. The final
fixture instead rebinds record variables to fresh values. The separate
discrepancy is retained in
[TypeRB #647](https://github.com/type-rb/type-rb/issues/647); this patch does not
fix or authorize record-field writes.

All three ordinary same-basename compiler generations have SHA256
`359986de042da34af54214cec9fc3e8d451918478649b53e82da7b15581384dc`.
The complete compiler remains 332712 bytes; Mach-O text is 235356 bytes and
compiler QBE is 1063233 bytes. All remain within unchanged absolute ceilings.

The three benchmark QBE outputs are byte-identical to the previous Native
baseline. Their SHA256 values are:

| Program | QBE SHA256 |
| --- | --- |
| fannkuch-redux | `bf8585e7658c7e3044e576ae568f0bcbb3bef15545bb8bdaab7094785a02ae50` |
| n-body | `7f33397e45878ab95e51801fd29a1393c7283a6f92e053030657a65ec808bfc2` |
| spectral-norm | `d2002cbc354f9c30382559860722e03b80c583351080a971eed65aa361f3529c` |

## Ordinary compiler build cost

The comparison baseline is
`1afd60c2c7257ed34fd2a2aa70cb8b9164433009`, compiler SHA256
`2c5bf4e9530473fe24e368d30f6add504c4c7e18b18fa621f5b4a26e41480d1d`.
Each compiler builds its own source closure, retaining two warmups and seven
interleaved observations per role. Every output reproduces its input compiler.
Measurements began after all owned correctness batches completed.

| Metric | Baseline median | Candidate median | Ratio |
| --- | ---: | ---: | ---: |
| Wall time (s) | 1.502029 | 1.51772775 | 1.0104516957 |
| CPU time (s) | 1.490326 | 1.494286 | 1.0026571368 |
| Root peak RSS (bytes) | 40157184 | 40189952 | 1.0008159935 |

All three ratios pass 1.05. Every retained observation for both roles passes
the 2.0 catastrophic bound. No allowance was changed. This baseline predates
the independently accepted scalar-output implementation in PR #300; its cost
is not removed from this comparison.

Host: Apple M2 Pro, 10 logical CPUs, 32 GiB RAM, macOS 26.6.2, Darwin arm64.
Reference: `5dc09070cf7f88a569279f5e63982a6de59d692c`; QBE 1.3; Apple clang
21.0.0 (`clang-2100.1.1.101`); target profile `darwin-arm64-v0`.
Warm-cache local execution, no CPU affinity, controlled frequency or
host-wide isolation claim. Unrelated host activity was not excluded.

The observer is the unchanged
[retained monotonic/wait4 controller](https://github.com/type-rb/type-rb-native/blob/dadb26a30552df1c01548d94ac54e5b8a79a57ec/results/2026-09-06-mir-loop-bounds-diagnostic-darwin-arm64/build-cost-observer.py)
at `dadb26a30552df1c01548d94ac54e5b8a79a57ec`. Its file belongs to a separate
unmerged diagnostic branch; use that exact revision to retrieve it.
It measures wall time with `time.monotonic_ns`, CPU including waited
descendants, and orchestration-root peak RSS rather than summed process memory.

```sh
python3 build-cost-observer.py CANDIDATE_CHECKOUT UNIQUE_EVIDENCE_PARENT \
  BASELINE_COMPILER CANDIDATE_COMPILER QBE
```

The observer runs each same-basename seed with `build ENTRY --output compiler
--qbe QBE --cc /usr/bin/cc --target darwin-arm64-v0`. Raw warmup and retained
rows, fixed-point/status fields and both-role catastrophic checks are retained
alongside this report.
