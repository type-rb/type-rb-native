# Formal Bounded Literal Integer-add Result on Linux arm64

The bounded literal Integer-add candidate passes every registered correctness,
fixed-point, compactness, build-cost, and runtime condition. On the exact
checked-in `spectral-norm` source at input 5500, it reduces median wall time by
9.25% and median CPU time by 9.26% against the accepted Native baseline. It
also reduces `fannkuch-redux` wall and CPU time by 2.85% and 2.86%, and
`n-body` wall and CPU time by 1.26% and 1.23%.

This is an implementation result for these exact programs, inputs, compiler
revisions, and toolchains. It is not a language-wide performance claim or a
claim of parity with the separately measured Pure Go programs. Matching or
beating Pure Go remains the minimum Native runtime objective.

## Exact scope

- accepted Native baseline:
  `586a679813af89cd63cd4196bee4fcb8905306cc`;
- measured candidate:
  `75e99417772fbafe7d93995b31263c29c4c77188`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Native target profile `linux-arm64-v0`, QBE 1.3, GCC 13.3.0,
  LLD 18.1.3, and BenchExec `runexec` 3.35;
- fresh GitHub-hosted `ubuntu-24.04-arm` runner with four available logical
  CPUs and Linux 6.17; and
- successful formal run
  [33559692874](https://github.com/type-rb/type-rb-native/actions/runs/33559692874).

The candidate implements the exact boundary registered by
[issue #186](https://github.com/type-rb/type-rb-native/issues/186). When the
existing inline budget selects a checked Integer addition and either emitted
operand is an unsigned decimal literal no greater than 1024, lowering moves
that literal to the right and omits the portable-range lower-bound check that
cannot fail. The upper-bound check remains. Dynamic operands and literals
outside the classifier retain the complete existing path.

Integer semantics, diagnostics, evaluation order, helper ABI, inline budgets,
and unrelated lowering remain unchanged.

## Correctness and fixed points

- all 80 repository tests and all 58 Gate 4 tests passed;
- either-side canonicalization, the 1024 boundary, outside literals, dynamic
  operands, exact output, and overflow diagnostics are covered directly;
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

The baseline fixed compiler is 254,976 bytes with SHA-256
`7355689ccfde7fec4a4b27c7b1e1a78bd73ff3cd13b98f2d66b966b0dcb1f573`.
The candidate fixed compiler is 254,264 bytes with SHA-256
`0d96b59b57b9581e205a77f831a0a46845603ad05fd94a00815047c21cc10c46`.
The candidate fixed-point QBE is 885,554 bytes with SHA-256
`d0ab7cdcdab570e6eeee5f57248372f5ea506285c74e608f43b9f618e583a681`.

## Runtime result

Times are fresh-process medians in seconds from eleven retained alternating
observations on one isolated core. A candidate/baseline ratio below 1 favors
the candidate.

| Case | Metric | Baseline | Candidate | Ratio | Maximum | Result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| fannkuch-redux | wall | 0.529986 | 0.514906 | 0.971546x | 1.02x | pass |
| fannkuch-redux | CPU | 0.527712 | 0.512618 | 0.971397x | 1.02x | pass |
| n-body | wall | 0.268854 | 0.265455 | 0.987357x | 1.02x | pass |
| n-body | CPU | 0.266697 | 0.263412 | 0.987683x | 1.02x | pass |
| spectral-norm | wall | 6.00765 | 5.45203 | 0.907515x | 0.95x | pass |
| spectral-norm | CPU | 6.00471 | 5.44871 | 0.907406x | 0.95x | pass |

Median process-tree memory is 524,288 bytes for both candidates in
`fannkuch-redux` and `n-body`, and 1,204,224 bytes for both candidates in
`spectral-norm`. Every individual memory observation remains within the
registered catastrophic bound.

## Build and compactness results

| Metric | Stage | Baseline | Candidate | Ratio | Maximum | Result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| compiler bytes | fixed point | 254,976 | 254,264 | 0.997208x | 1.01x | pass |
| compiler bytes | absolute | 255,000 | 254,264 | 0.997114x | 1.00x | pass |
| build wall | B2->B3 | 0.93 s | 0.97 s | 1.043011x | 1.05x | pass |
| build CPU | B2->B3 | 0.92 s | 0.96 s | 1.043478x | 1.05x | pass |
| build RSS | B2->B3 | 64,352,256 | 64,364,544 | 1.000191x | 1.05x | pass |
| build wall | B3->B4 | 0.94 s | 0.97 s | 1.031915x | 1.05x | pass |
| build CPU | B3->B4 | 0.94 s | 0.97 s | 1.031915x | 1.05x | pass |
| build RSS | B3->B4 | 64,380,928 | 64,335,872 | 0.999300x | 1.05x | pass |

All generated applications passed their frozen QBE, raw-executable, and
stripped-executable limits. Candidate QBE is 0.86% to 1.73% smaller, raw
executables are 0.42% to 0.72% smaller, and stripped executables are 0.42% to
0.72% smaller than their exact baseline counterparts.

## Retained evidence

GitHub published artifact `native-runtime-ab-33559692874-1` as artifact ID
9820923318, 445,252 archive bytes, with SHA-256
`638512ea9e48828625fca55adca1378e982788d1b4cca4fdedd4f82bf71cd446`.

This result retains all 665 extracted artifact files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 666 files and excludes only this README and
itself. The tree includes exact workflow and compiler identities, both
bootstrap chains, build metrics, process and dependency inventories,
generated applications, correctness summaries, all raw runtime observations,
independently reproduced medians, catastrophic checks, and final decision
rows. The retained workspace temporary-file inventory is empty.

## Conclusion

A proof attached to one already budgeted literal addition removes an
impossible lower-bound branch without weakening checked Integer semantics. It
improves all three registered programs, with the largest effect in
`spectral-norm`, while shrinking the compiler and generated artifacts. A fresh
complete cross-language snapshot is still required to measure the remaining
gap to Pure Go. Further optimization continues toward Pure Go parity or
better.
