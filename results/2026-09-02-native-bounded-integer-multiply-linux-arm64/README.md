# Formal Bounded Integer-multiply Result on Linux arm64

The bounded Integer-multiply candidate passes every registered correctness,
fixed-point, compactness, build-cost, and runtime condition. On the exact
checked-in `spectral-norm` source at input 5500, it reduces median wall time by
27.82% and median CPU time by 27.83% against the accepted Native baseline.
`fannkuch-redux` and `n-body` remain unchanged within measurement noise.

This is an implementation result for these exact programs, inputs, compiler
revisions, and toolchains. It is not a language-wide performance claim or a
claim of parity with the separately measured Pure Go programs. Matching or
beating Pure Go remains the minimum Native runtime objective.

## Exact scope

- accepted Native baseline:
  `bf4e99ffa8eeb3408cef59c71c0bfbf140466283`;
- measured candidate:
  `8aba57d89abf0fa6f867eae8d8dbfef58d92bb2a`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Native target profile `linux-arm64-v0`, QBE 1.3, GCC 13.3.0,
  LLD 18.1.3, and BenchExec `runexec` 3.35;
- fresh GitHub-hosted `ubuntu-24.04-arm` runner with four Neoverse-N2
  logical CPUs and Linux 6.17; and
- successful formal run
  [33550310116](https://github.com/type-rb/type-rb-native/actions/runs/33550310116).

The candidate implements the exact boundary registered by
[issue #184](https://github.com/type-rb/type-rb-native/issues/184). The shared
checked-Integer multiply entry first tests whether the bitwise union of both
operands fits the nonnegative 26-bit range. When it does, their product is
provably representable and lowers directly to one signed multiply. Every
other operand pair uses the existing exact zero, minimum-Integer, division,
and overflow checks.

Integer semantics, diagnostics, return values, helper ABI, and all unrelated
lowering remain unchanged.

## Correctness and fixed points

- all 80 repository tests and all 57 Gate 4 tests passed;
- exact boundary checks cover zero, positive fast-path limits, negative
  operands, large operands, and overflow diagnostics;
- the complete bootstrap semantic corpus passed across candidate generations;
- the baseline and candidate Linux arm64 chains each closed exact B2/B3/B4
  fixed points;
- every registered application returned status zero, empty stderr, and exact
  expected stdout before measurement;
- every retained observation returned successful metrics and passed the 2.0x
  catastrophic boundary; and
- current Linux amd64 and Linux arm64 regressions, target-neutral QBE
  comparison, persistent-worker memory checks, and static-String compactness
  checks passed on the exact candidate.

The baseline fixed compiler is 254,976 bytes with SHA-256
`07cce7e8fc48289a875e4c5fc4a054f7ab3b252ec41c3edcba8bdd03a17dbcff`.
The candidate remains 254,976 bytes with SHA-256
`7355689ccfde7fec4a4b27c7b1e1a78bd73ff3cd13b98f2d66b966b0dcb1f573`.
The candidate fixed-point QBE is 887,116 bytes with SHA-256
`e42244063d0405f947c7cfb455d32dfa2ed6c3c786f453b8641ecd8127337d7e`.

## Runtime result

Times are fresh-process medians in seconds from eleven retained alternating
observations on one isolated core. A candidate/baseline ratio below 1 favors
the candidate.

| Case | Metric | Baseline | Candidate | Ratio | Maximum | Result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| fannkuch-redux | wall | 0.529415 | 0.529401 | 0.999974x | 1.02x | pass |
| fannkuch-redux | CPU | 0.527455 | 0.527334 | 0.999771x | 1.02x | pass |
| n-body | wall | 0.268868 | 0.268981 | 1.000420x | 1.02x | pass |
| n-body | CPU | 0.266808 | 0.266846 | 1.000142x | 1.02x | pass |
| spectral-norm | wall | 8.325090 | 6.009020 | 0.721796x | 0.95x | pass |
| spectral-norm | CPU | 8.322110 | 6.005800 | 0.721668x | 0.95x | pass |

Median process-tree memory was 438,272 versus 430,080 bytes for
`fannkuch-redux`, 524,288 bytes for both `n-body` executables, and 1,212,416
versus 1,208,320 bytes for `spectral-norm`. Every individual memory
observation remained within the registered catastrophic bound.

## Build and compactness results

| Metric | Stage | Baseline | Candidate | Ratio | Maximum | Result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| compiler bytes | fixed point | 254,976 | 254,976 | 1.000000x | 1.01x | pass |
| compiler bytes | absolute | 255,000 | 254,976 | 0.999906x | 1.00x | pass |
| build wall | B2->B3 | 0.89 s | 0.89 s | 1.000000x | 1.05x | pass |
| build CPU | B2->B3 | 0.88 s | 0.89 s | 1.011364x | 1.05x | pass |
| build RSS | B2->B3 | 64,380,928 | 64,376,832 | 0.999936x | 1.05x | pass |
| build wall | B3->B4 | 0.89 s | 0.89 s | 1.000000x | 1.05x | pass |
| build CPU | B3->B4 | 0.89 s | 0.89 s | 1.000000x | 1.05x | pass |
| build RSS | B3->B4 | 64,380,928 | 64,372,736 | 0.999873x | 1.05x | pass |

All generated applications passed their frozen QBE, raw-executable, and
stripped-executable limits. Each raw and stripped executable is byte-for-byte
the same size as its baseline. Generated QBE shrinks by 115 bytes for each
application: 53,710 to 53,595 bytes for `fannkuch-redux`, 70,948 to 70,833
bytes for `n-body`, and 53,591 to 53,476 bytes for `spectral-norm`.

## Retained evidence

GitHub published artifact `native-runtime-ab-33550310116-1` as artifact ID
9817357915, 446,150 archive bytes, with SHA-256
`3eec983bec5c174fc115a83cfa8f56d76cfd5278c0c89ace4a86399bf1bb7f82`.

This result retains all 665 extracted artifact files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 666 files and excludes only this README and
itself. The tree includes exact workflow and compiler identities, both
bootstrap chains, build metrics, process and dependency inventories,
generated applications, correctness summaries, all raw runtime observations,
independently reproduced medians, catastrophic checks, and final decision
rows. The retained workspace temporary-file inventory is empty.

## Conclusion

A narrow proof before the checked multiply removes expensive overflow-control
work from the common nonnegative numeric path without weakening Integer
semantics or increasing the fixed compiler or application binaries. The
27.82% `spectral-norm` improvement is material, but a fresh complete
cross-language snapshot is still required to measure the remaining gap to
Pure Go. Further optimization continues toward Pure Go parity or better.
