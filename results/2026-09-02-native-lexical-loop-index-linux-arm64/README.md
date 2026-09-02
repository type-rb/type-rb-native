# Formal Lexical Loop-index Result on Linux arm64

The lexical loop-index candidate passes every registered correctness,
fixed-point, compactness, build-cost, and runtime condition. On the exact
checked-in `n-body` source at input 1,000,000, it reduces median wall time by
12.21% and median CPU time by 12.22% against the accepted Native baseline.
`fannkuch-redux` and `spectral-norm` remain neutral within their frozen 1.02x
non-regression limits.

This is an implementation result for these exact programs, inputs, compiler
revisions, and toolchains. It is not a language-wide performance claim or a
claim of parity with the separately measured Pure Go programs. Matching or
beating Pure Go remains the minimum Native runtime objective.

## Exact scope

- accepted Native baseline:
  `ba8dfd0b881c8fa2ed7aca166f1bab2af4859bbb`;
- measured candidate:
  `e54c6898afb59cce63a68f82907d233006a92b1f`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Native target profile `linux-arm64-v0`, QBE 1.3, GCC 13.3.0,
  LLD 18.1.3, and BenchExec `runexec` 3.35;
- fresh GitHub-hosted `ubuntu-24.04-arm` runner with four available logical
  CPUs and Linux 6.17; and
- successful formal run
  [33574109663](https://github.com/type-rb/type-rb-native/actions/runs/33574109663).

The candidate implements the exact boundary registered by
[issue #190](https://github.com/type-rb/type-rb-native/issues/190). It limits
the existing zero-based unit-step proof to the matching lexical loop. Safe
nested control flow and mutations after that loop no longer discard the fact.
Direct reassignment, non-unit updates, shadowing, derived indices, and all
unproved accesses retain the general path. Every access keeps the unsigned
upper-bound check and failure path.

Integer and Array semantics, diagnostics, evaluation order, helper ABI,
inline budgets, and unrelated lowering remain unchanged.

## Correctness and fixed points

- all 59 Gate 4 tests and all 80 repository tests passed on the exact measured
  revision;
- safe nested loops, later resets, direct reassignment, non-unit updates,
  duplicate bindings, and function boundaries are covered directly;
- the complete bootstrap semantic corpus passed across candidate generations;
- the baseline and candidate Linux arm64 chains each closed exact B2/B3/B4
  fixed points;
- every registered application returned status zero, empty stderr, and exact
  expected stdout before measurement;
- all eleven retained observations per candidate and case passed, and every
  individual time and memory observation remained within the registered 2.0x
  catastrophic boundary; and
- current Linux amd64 and Linux arm64 regressions, target-neutral QBE
  comparison, persistent-worker memory checks, static-String compactness, and
  the full Native gate passed on the exact candidate.

The baseline fixed compiler is 254,696 bytes with SHA-256
`e8f8ef230a6342805116e609bd3b01ec127ed9b1fcb63cc4831a0774e6d6bcb7`.
The candidate fixed compiler is 254,872 bytes with SHA-256
`84354b9dace7d981fc1ba36c356e7c7db7e691daf43e1b1437c8faa365b8a5d9`.
The candidate fixed-point QBE is 888,266 bytes with SHA-256
`cac7a377acf0797733078ab67dcc85935c5b87907257bebca8bafb430cc638b6`.

## Runtime result

Times are fresh-process medians in seconds from eleven retained alternating
observations on one isolated core. A candidate/baseline ratio below 1 favors
the candidate.

| Case | Metric | Baseline | Candidate | Ratio | Maximum | Result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| fannkuch-redux | wall | 0.514740 | 0.514648 | 0.999821x | 1.02x | pass |
| fannkuch-redux | CPU | 0.512694 | 0.512550 | 0.999719x | 1.02x | pass |
| n-body | wall | 0.265954 | 0.233486 | 0.877919x | 0.95x | pass |
| n-body | CPU | 0.263600 | 0.231393 | 0.877819x | 0.95x | pass |
| spectral-norm | wall | 5.18285 | 5.18145 | 0.999730x | 1.02x | pass |
| spectral-norm | CPU | 5.18011 | 5.17848 | 0.999685x | 1.02x | pass |

Median process-tree memory is 524,288 bytes for both candidates in
`fannkuch-redux` and `n-body`, and 1,204,224 bytes for both candidates in
`spectral-norm`. Every individual memory observation remains within the
registered catastrophic bound.

## Build and compactness results

| Metric | Stage | Baseline | Candidate | Ratio | Maximum | Result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| compiler bytes | fixed point | 254,696 | 254,872 | 1.000691x | 1.01x | pass |
| compiler bytes | absolute | 255,000 | 254,872 | 0.999498x | 1.00x | pass |
| build wall | B2->B3 | 0.96 s | 1.00 s | 1.041667x | 1.05x | pass |
| build CPU | B2->B3 | 0.96 s | 0.99 s | 1.031250x | 1.05x | pass |
| build RSS | B2->B3 | 64,364,544 | 64,253,952 | 0.998282x | 1.05x | pass |
| build wall | B3->B4 | 0.96 s | 0.99 s | 1.031250x | 1.05x | pass |
| build CPU | B3->B4 | 0.96 s | 0.99 s | 1.031250x | 1.05x | pass |
| build RSS | B3->B4 | 64,450,560 | 64,356,352 | 0.998538x | 1.05x | pass |

All generated applications pass their frozen QBE, raw-executable, and
stripped-executable limits. `fannkuch-redux` is byte-neutral. `n-body` QBE
shrinks by 1,545 bytes, its raw executable by 256 bytes, and its stripped
executable by 256 bytes. `spectral-norm` QBE shrinks by 140 bytes, and each
executable shrinks by 32 bytes. The emitted negative-index normalization
sequence count falls from 39 to 19 in `n-body` and from 6 to 4 in
`spectral-norm`, while remaining unchanged at 15 in `fannkuch-redux`.

## Retained evidence

GitHub published artifact `native-runtime-ab-33574109663-1` as artifact ID
9826098674, 442,337 archive bytes, with SHA-256
`5060ae6c3ef92c97bdd1fbeb6cc7b859b3554b7978d65534198e4f9e3dfb5edb`.

This result retains all 666 extracted artifact files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 667 files and excludes only this README and
itself. The tree includes exact workflow and compiler identities, both
bootstrap chains, build metrics, process and dependency inventories,
correctness summaries, all raw runtime observations, independently reproduced
medians, catastrophic checks, and final decision rows. The retained workspace
temporary-file inventory is empty.

## Conclusion

Scoping the induction proof to its lexical loop removes twenty additional
impossible negative-index normalization paths from `n-body` without weakening
checked Array semantics. It produces a repeatable 12.2% improvement in that
registered workload, preserves both controls, and keeps compiler and
application artifacts inside every frozen limit. A fresh complete
cross-language snapshot is still required to measure the remaining gap to
Pure Go. Further optimization continues toward Pure Go parity or better.
