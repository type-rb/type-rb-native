# Formal Nonnegative Loop-index Result on Linux arm64

The nonnegative loop-index candidate passes every registered correctness,
fixed-point, compactness, build-cost, and runtime condition. On the exact
checked-in `spectral-norm` source at input 5500, it reduces median wall time by
5.00% and median CPU time by 5.00% against the accepted Native baseline.
`fannkuch-redux` and `n-body` remain neutral within their frozen 1.02x
non-regression limits.

This is an implementation result for these exact programs, inputs, compiler
revisions, and toolchains. It is not a language-wide performance claim or a
claim of parity with the separately measured Pure Go programs. Matching or
beating Pure Go remains the minimum Native runtime objective.

## Exact scope

- accepted Native baseline:
  `05d53927d101455c4ead50165a4b028bb39c1cb4`;
- measured candidate:
  `c86f2793dbbfc55074d920feab7381fcb2729b3a`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Native target profile `linux-arm64-v0`, QBE 1.3, GCC 13.3.0,
  LLD 18.1.3, and BenchExec `runexec` 3.35;
- fresh GitHub-hosted `ubuntu-24.04-arm` runner with four available logical
  CPUs and Linux 6.17; and
- successful formal run
  [33569309608](https://github.com/type-rb/type-rb-native/actions/runs/33569309608).

The candidate implements the exact boundary registered by
[issue #188](https://github.com/type-rb/type-rb-native/issues/188). It removes
negative-index normalization only for Array accesses driven by a narrowly
proven zero-based unit-step induction local. The unsigned upper-bound check
and failure path remain. Reassignment, non-unit updates, nested control flow,
dynamic indices, and ordinary negative indexing retain the general path.

Integer and Array semantics, diagnostics, evaluation order, helper ABI,
inline budgets, and unrelated lowering remain unchanged.

## Correctness and fixed points

- all 59 Gate 4 tests passed locally on the exact measured revision;
- the eligible loop and the direct-reassignment, non-unit-update,
  nested-control, and function-scope rejection boundaries are covered
  directly;
- the complete bootstrap semantic corpus passed across candidate generations;
- the baseline and candidate Linux arm64 chains each closed exact B2/B3/B4
  fixed points;
- every registered application returned status zero, empty stderr, and exact
  expected stdout before measurement;
- all eleven retained observations per candidate and case passed, and every
  individual time and memory observation remained within the registered 2.0x
  catastrophic boundary; and
- current Linux amd64 and Linux arm64 regressions, target-neutral QBE
  comparison, persistent-worker memory checks, and static-String compactness
  checks passed on the exact candidate.

The baseline fixed compiler is 254,264 bytes with SHA-256
`0d96b59b57b9581e205a77f831a0a46845603ad05fd94a00815047c21cc10c46`.
The candidate fixed compiler is 254,696 bytes with SHA-256
`e8f8ef230a6342805116e609bd3b01ec127ed9b1fcb63cc4831a0774e6d6bcb7`.
The candidate fixed-point QBE is 887,706 bytes with SHA-256
`2723f404713ba8f765512c2fa2564effb26252bb647d26edbca01a3b72dcaf71`.

## Runtime result

Times are fresh-process medians in seconds from eleven retained alternating
observations on one isolated core. A candidate/baseline ratio below 1 favors
the candidate.

| Case | Metric | Baseline | Candidate | Ratio | Maximum | Result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| fannkuch-redux | wall | 0.514226 | 0.514291 | 1.000126x | 1.02x | pass |
| fannkuch-redux | CPU | 0.512264 | 0.512306 | 1.000082x | 1.02x | pass |
| n-body | wall | 0.264954 | 0.265100 | 1.000551x | 1.02x | pass |
| n-body | CPU | 0.263154 | 0.263210 | 1.000213x | 1.02x | pass |
| spectral-norm | wall | 5.45452 | 5.18187 | 0.950014x | 0.98x | pass |
| spectral-norm | CPU | 5.45232 | 5.17950 | 0.949963x | 0.98x | pass |

Median process-tree memory is 524,288 bytes for both candidates in
`fannkuch-redux` and `n-body`. In `spectral-norm`, it falls from 1,212,416 to
1,204,224 bytes. Every individual memory observation remains within the
registered catastrophic bound.

## Build and compactness results

| Metric | Stage | Baseline | Candidate | Ratio | Maximum | Result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| compiler bytes | fixed point | 254,264 | 254,696 | 1.001699x | 1.01x | pass |
| compiler bytes | absolute | 255,000 | 254,696 | 0.998808x | 1.00x | pass |
| build wall | B2->B3 | 0.90 s | 0.92 s | 1.022222x | 1.05x | pass |
| build CPU | B2->B3 | 0.90 s | 0.92 s | 1.022222x | 1.05x | pass |
| build RSS | B2->B3 | 64,253,952 | 64,380,928 | 1.001976x | 1.05x | pass |
| build wall | B3->B4 | 0.91 s | 0.93 s | 1.021978x | 1.05x | pass |
| build CPU | B3->B4 | 0.91 s | 0.92 s | 1.010989x | 1.05x | pass |
| build RSS | B3->B4 | 64,360,448 | 64,385,024 | 1.000382x | 1.05x | pass |

All generated applications pass their frozen QBE, raw-executable, and
stripped-executable limits. `fannkuch-redux` is byte-neutral. `n-body` QBE
shrinks by 434 bytes and each executable by 64 bytes; `spectral-norm` QBE
shrinks by 140 bytes and each executable by 32 bytes. The emitted
negative-index normalization sequence count falls from 45 to 39 in `n-body`
and from 8 to 6 in `spectral-norm`, while remaining unchanged at 15 in
`fannkuch-redux`.

## Retained evidence

GitHub published artifact `native-runtime-ab-33569309608-1` as artifact ID
9824459713, 444,298 archive bytes, with SHA-256
`56f381ca16ceb5b4d9b6748e4fa31844cb5383215e4a0d507388fc872014f83d`.

This result retains all 666 extracted artifact files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 667 files and excludes only this README and
itself. The tree includes exact workflow and compiler identities, both
bootstrap chains, build metrics, process and dependency inventories,
generated applications, correctness summaries, all raw runtime observations,
independently reproduced medians, catastrophic checks, and final decision
rows. The retained workspace temporary-file inventory is empty.

## Conclusion

A deliberately narrow induction proof removes an impossible negative-index
path without weakening checked Array semantics. It produces a repeatable 5%
improvement in the registered `spectral-norm` workload, preserves the other
two programs, and keeps compiler and application artifacts inside every
frozen limit. A fresh complete cross-language snapshot is still required to
measure the remaining gap to Pure Go. Further optimization continues toward
Pure Go parity or better.
