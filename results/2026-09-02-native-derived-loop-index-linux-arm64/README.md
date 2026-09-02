# Formal Derived Loop-index Result on Linux arm64

The derived loop-index candidate passes every registered correctness,
fixed-point, compactness, build-cost, and runtime condition. On the exact
checked-in `n-body` source at input 1,000,000, it reduces median wall time by
8.68% and median CPU time by 8.71% against the accepted Native baseline.
`fannkuch-redux` and `spectral-norm` remain neutral within their frozen 1.02x
non-regression limits.

This is an implementation result for these exact programs, inputs, compiler
revisions, and toolchains. It is not a language-wide performance claim or a
claim of parity with the separately measured Pure Go programs. Matching or
beating Pure Go remains the minimum Native runtime objective.

## Exact scope

- accepted Native baseline:
  `aad4954c66ae394a5edb836b20498e5a60b769bd`;
- measured candidate:
  `6488a5308ed85fb9cd7780f97880979bf8f1ce09`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Native target profile `linux-arm64-v0`, QBE 1.3, GCC 13.3.0,
  LLD 18.1.3, and BenchExec `runexec` 3.35;
- fresh GitHub-hosted `ubuntu-24.04-arm` runner with four available logical
  CPUs and Linux 6.17; and
- successful formal run
  [33589001047](https://github.com/type-rb/type-rb-native/actions/runs/33589001047).

The candidate implements the exact boundary registered by
[issue #192](https://github.com/type-rb/type-rb-native/issues/192). It carries
an active nonnegative lexical loop-index fact through checked addition of a
small nonnegative literal into an immediately declared derived unit-step loop
local. Ordinary mutable locals, negative or dynamic additions, overflow,
reassignment, non-unit updates, shadowing, and unproved indices retain the
general path. Every access keeps the unsigned upper-bound check and failure
path.

Integer and Array semantics, diagnostics, evaluation order, helper ABI,
inline budgets, and unrelated lowering remain unchanged.

## Correctness and fixed points

- all 59 Gate 4 tests and all 80 repository tests passed on the exact measured
  revision;
- safe derived loops, negative and dynamic additions, overflow, reassignment,
  non-unit updates, shadowing, and ordinary negative indices are covered
  directly;
- the complete bootstrap semantic corpus passed across candidate generations;
- the baseline and candidate Linux arm64 chains each closed exact B2/B3/B4
  fixed points;
- every registered application returned status zero, empty stderr, and exact
  expected stdout before measurement;
- all eleven retained observations per candidate and case passed, and every
  individual time and memory observation remained within the registered 2.0x
  catastrophic boundary; and
- Darwin arm64, Linux arm64, Linux amd64, cross-target QBE,
  persistent-worker memory, static-String compactness, and the full Native
  gate passed on the exact candidate.

The baseline fixed compiler is 254,872 bytes with SHA-256
`84354b9dace7d981fc1ba36c356e7c7db7e691daf43e1b1437c8faa365b8a5d9`.
The candidate fixed compiler is 254,816 bytes with SHA-256
`9ddf4069f2fb5c3599047541d8b331ca25e321ea45c47168e1cf72eaed0295db`.
The candidate fixed-point QBE is 888,636 bytes with SHA-256
`b35aeacce1540a7fc08b5898b97703c9a686ffad98c40e19b4df2509c37fba58`.

## Runtime result

Times are fresh-process medians in seconds from eleven retained alternating
observations on one isolated core. A candidate/baseline ratio below 1 favors
the candidate.

| Case | Metric | Baseline | Candidate | Ratio | Maximum | Result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| fannkuch-redux | wall | 0.514175 | 0.514279 | 1.000202x | 1.02x | pass |
| fannkuch-redux | CPU | 0.512145 | 0.512188 | 1.000084x | 1.02x | pass |
| n-body | wall | 0.232929 | 0.212704 | 0.913171x | 0.96x | pass |
| n-body | CPU | 0.230767 | 0.210657 | 0.912856x | 0.96x | pass |
| spectral-norm | wall | 5.17877 | 5.17954 | 1.000149x | 1.02x | pass |
| spectral-norm | CPU | 5.17659 | 5.17705 | 1.000089x | 1.02x | pass |

Median process-tree memory is 524,288 bytes for both candidates in
`fannkuch-redux` and `n-body`. In `spectral-norm`, it is 1,216,512 bytes for
the baseline and 1,200,128 bytes for the candidate. Every individual memory
observation remains within the registered catastrophic bound.

## Build and compactness results

| Metric | Stage | Baseline | Candidate | Ratio | Maximum | Result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| compiler bytes | fixed point | 254,872 | 254,816 | 0.999780x | 1.01x | pass |
| compiler bytes | absolute | 255,000 | 254,816 | 0.999278x | 1.00x | pass |
| build wall | B2->B3 | 0.89 s | 0.89 s | 1.000000x | 1.05x | pass |
| build CPU | B2->B3 | 0.89 s | 0.88 s | 0.988764x | 1.05x | pass |
| build RSS | B2->B3 | 64,253,952 | 64,380,928 | 1.001976x | 1.05x | pass |
| build wall | B3->B4 | 0.89 s | 0.89 s | 1.000000x | 1.05x | pass |
| build CPU | B3->B4 | 0.89 s | 0.89 s | 1.000000x | 1.05x | pass |
| build RSS | B3->B4 | 64,356,352 | 64,380,928 | 1.000382x | 1.05x | pass |

All generated applications pass their frozen QBE, raw-executable, and
stripped-executable limits. Both controls are byte-neutral. `n-body` QBE
shrinks by 1,008 bytes, its raw executable by 176 bytes, and its stripped
executable by 176 bytes. Its emitted negative-index normalization sequence
count falls from 19 to 6, the exact required reduction of thirteen.

## Retained evidence

GitHub published artifact `native-runtime-ab-33589001047-1` as artifact ID
9831169406, 440,149 archive bytes, with SHA-256
`d1036ecb48b9da27ea3e06dba17672f65d1f8e65987728ce0e3fc1e96bd1e8c4`.

This result retains all 666 extracted artifact files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 667 files and excludes only this README and
itself. The tree includes exact workflow and compiler identities, both
bootstrap chains, build metrics, process and dependency inventories,
correctness summaries, all raw runtime observations, independently reproduced
medians, catastrophic checks, and final decision rows. The retained workspace
temporary-file inventory is empty.

Independent verification reproduced every runtime median and ratio, checked
all retained observation statuses, recalculated every catastrophic ratio,
matched application sizes and normalization counts to the retained files,
verified every application digest and workflow-source digest available in the
artifact, and confirmed the compiler identities and process boundary.

## Conclusion

Bounded propagation through checked addition removes the remaining thirteen
targeted impossible negative-index normalization paths from `n-body` without
weakening checked Array semantics. It produces a repeatable 8.7% improvement
in that registered workload, preserves both controls, shrinks the fixed
compiler, and keeps every application artifact inside its frozen limit.

This closes the last preregistered direct-emitter semantic-analysis experiment.
Further portable range, induction, Array-header, allocation, and GC-safety
optimization moves to verified Native MIR analysis and target-independent
passes under [Decision 0028](../../docs/decisions/0028-native-mir-optimization-boundary.md).
