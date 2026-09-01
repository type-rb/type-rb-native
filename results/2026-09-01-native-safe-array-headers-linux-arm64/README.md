# Formal Safe Array-Header Reuse Result on Linux arm64

The combined safe-point-aware root-elision and bounded Array-header reuse
candidate passes every registered correctness, fixed-point, compactness,
build-cost, and runtime condition. On the exact checked-in `n-body` source at
1,000,000 iterations, it reduces median wall time by 28.36% and median CPU
time by 28.50% against the accepted Native baseline. `fannkuch-redux` becomes
7.46% faster, and `spectral-norm` remains unchanged within measurement noise.

This is an implementation result for these exact programs, inputs, compiler
revisions, and toolchains. It is not a language-wide performance claim or a
claim of parity with the separately measured Pure Go programs.

## Exact scope

- accepted Native baseline:
  `c562d56b8fdafcd7b9a679eeac58932b3023267d`;
- measured candidate:
  `9ad801a6ed2e67285b65a0767323d3610a9edda9`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Native target profile `linux-arm64-v0`, QBE 1.3, GCC 13.3.0,
  LLD 18.1.3, and BenchExec `runexec` 3.35;
- fresh GitHub-hosted `ubuntu-24.04-arm` runner with four Neoverse-N2
  logical CPUs and Linux 6.17; and
- successful formal run
  [33502265052](https://github.com/type-rb/type-rb-native/actions/runs/33502265052).

The candidate implements the exact boundary registered by
[issue #176](https://github.com/type-rb/type-rb-native/issues/176). Functions
without a collection safe point omit redundant managed-root frame work.
Inside loops that own a managed local, generated code reuses the two most
recently used Array length and backing-data header pairs. The two entries are
rotated by reference and invalidated conservatively at mutation, rebinding,
ordinary calls, branches, and loop boundaries.

Negative indexing, bounds checks, Array mutation, evaluation order, the
managed-runtime ABI, and collector behavior remain unchanged.

## Correctness and fixed points

- all 80 repository tests and all 54 Gate 4 tests passed locally;
- the complete bootstrap semantic corpus passed across the candidate
  generations;
- the baseline and candidate Linux arm64 chains each closed exact B2/B3/B4
  fixed points;
- every registered application returned status zero, empty stderr, and exact
  expected stdout before measurement;
- every retained observation returned successful metrics and passed the 2.0x
  catastrophic boundary; and
- the current Linux amd64 and Linux arm64 regressions, target-neutral QBE
  comparison, persistent-worker memory checks, and static-String compactness
  checks passed on the exact candidate.

The baseline fixed compiler is 252,816 bytes with SHA-256
`09a30ee2c58f2398a71d210dfb4235cc31af73984da44d0f5bf01bfe87d1b443`.
The candidate is 254,960 bytes with SHA-256
`65b18c8999e91dbb67e7dabb5d731987daa32076c9e4cd709962dc4b49bb73cb`.

## Runtime result

Times are fresh-process medians in seconds from eleven retained alternating
observations on one isolated core. A candidate/baseline ratio below 1 favors
the candidate.

| Case | Metric | Baseline | Candidate | Ratio | Maximum | Result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| fannkuch-redux | wall | 0.653363 | 0.604606 | 0.925375x | 1.02x | pass |
| fannkuch-redux | CPU | 0.651349 | 0.602693 | 0.925300x | 1.02x | pass |
| n-body | wall | 0.375727 | 0.269156 | 0.716361x | 0.85x | pass |
| n-body | CPU | 0.373427 | 0.267009 | 0.715023x | 0.85x | pass |
| spectral-norm | wall | 8.324220 | 8.323230 | 0.999881x | 1.02x | pass |
| spectral-norm | CPU | 8.321530 | 8.320870 | 0.999921x | 1.02x | pass |

Median process-tree memory was 524,288 bytes for both `fannkuch-redux`
executables, 524,288 versus 684,032 bytes for `n-body`, and 1,454,080 versus
1,462,272 bytes for `spectral-norm`. Every individual memory observation
remained within the registered catastrophic bound.

## Build and compactness results

| Metric | Stage | Baseline | Candidate | Ratio | Maximum | Result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| compiler bytes | fixed point | 252,816 | 254,960 | 1.008480x | 1.03x | pass |
| compiler bytes | absolute | 255,000 | 254,960 | 0.999843x | 1.00x | pass |
| build wall | B2→B3 | 0.93 s | 0.92 s | 0.989247x | 1.05x | pass |
| build CPU | B2→B3 | 0.93 s | 0.92 s | 0.989247x | 1.05x | pass |
| build RSS | B2→B3 | 64,356,352 | 64,380,928 | 1.000382x | 1.05x | pass |
| build wall | B3→B4 | 0.93 s | 0.93 s | 1.000000x | 1.05x | pass |
| build CPU | B3→B4 | 0.92 s | 0.92 s | 1.000000x | 1.05x | pass |
| build RSS | B3→B4 | 64,364,544 | 64,376,832 | 1.000191x | 1.05x | pass |

All generated applications passed their frozen QBE, raw-executable, and
stripped-executable limits. `n-body` QBE shrank from 76,382 to 71,090 bytes;
its raw executable shrank from 24,032 to 22,912 bytes and its stripped
executable from 24,024 to 22,904 bytes. The two control cases remained within
1.001x of the baseline for every artifact.

## Retained evidence

GitHub published artifact `native-runtime-ab-33502265052-1` as artifact ID
9798379819, 449,018 archive bytes, with SHA-256
`30e76f239eeab26f5f8ec1e53087a811ea30f7126abc0324eed8e6a1c2362479`.

This result retains all 665 extracted artifact files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 666 files and excludes only this README and
itself. The tree includes exact workflow and compiler identities, both
bootstrap chains, build metrics, process and dependency inventories, generated
applications, correctness summaries, all raw runtime observations,
independently reproduced medians, catastrophic checks, and final decision
rows.

## Conclusion

Conservative two-entry Array-header reuse is a material generated-code
improvement for an Array-heavy numeric kernel and composes successfully with
safe-point-aware root elision. It is retained without changing TypeRB
semantics or any preregistered threshold. Future optimization should continue
from fresh profiles and the explicit minimum objective of matching or beating
Pure Go runtime on representative workloads while preserving the existing
build-time, memory, and compactness advantages.
