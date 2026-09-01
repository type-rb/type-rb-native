# Rejected No-GC-Safe-Point Root-Publication Result on Linux arm64

The safe-point-aware root-publication candidate is not retained. It improved
the registered `n-body` wall and CPU medians by about 12.7%, kept the measured
control byte-identical, reduced the `n-body` QBE and executable, and passed all
compiler build and compactness limits. However, its wall and CPU ratios were
`0.873593x` and `0.872943x`, outside the frozen `0.85x` maximum.

The threshold was not relaxed after observing the result. The implementation
was reverted; this directory retains the complete formal evidence so the
mechanism and its measured effect remain available to future work.

## Exact scope

- accepted Native baseline:
  `769233b05203937e9f8986b7a8558df6e2f98c5c`;
- measured candidate:
  `ba94f0b8a034dd25d8e5d9c8ab16425d9b87927c`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Native target profile `linux-arm64-v0`, QBE 1.3, GCC 13.3.0,
  LLD 18.1.3, and BenchExec `runexec` 3.35;
- fresh GitHub-hosted `ubuntu-24.04-arm` runner with four Neoverse-N2
  logical CPUs and Linux 6.17; and
- authoritative formal run
  [33484444996](https://github.com/type-rb/type-rb-native/actions/runs/33484444996).

An earlier run
[33484172894](https://github.com/type-rb/type-rb-native/actions/runs/33484172894)
stopped before application construction because the exact baseline's older
bootstrap observer had no CPU evidence column. The measured candidate changed
only the observer boundary for the authoritative rerun: both exact compiler
source trees were measured by the same current observer. No decision threshold
changed.

## Candidate boundary

The experiment distinguished managed aliases from operations that can start
Native collection. Functions with no allocation, managed result, Array growth,
or ordinary user call omitted temporary-root reservation, loop publication,
and root-count restoration. All ordinary user calls remained conservative safe
points, as did every directly or transitively allocating runtime operation.

The `n-body` hot functions retain managed Array aliases but do not allocate or
make opaque user calls. The candidate removed their redundant loop-header root
rewrites without changing authored TypeRB source, negative-index semantics,
bounds checks, arithmetic, or the collector.

## Correctness and fixed points

- all 52 local Gate 4 frontend tests passed, including paired no-safe-point,
  Array-growth, and opaque-user-call fixtures;
- the complete local bootstrap semantic corpus passed before the expected
  sandbox denial of the Darwin `/usr/bin/time -l` system query;
- both Linux arm64 compiler chains closed exact B2/B3/B4 fixed points;
- `fannkuch-redux` and `n-body` returned status zero, empty stderr, and exact
  registered output before timing;
- all retained observations returned successful metrics and passed the 2.0x
  catastrophic boundary; and
- `fannkuch-redux` QBE plus raw and stripped executables were byte-identical.

The baseline fixed compiler is 252,816 bytes with SHA-256
`09a30ee2c58f2398a71d210dfb4235cc31af73984da44d0f5bf01bfe87d1b443`.
The candidate is 253,336 bytes with SHA-256
`5c12c946e44a0c7dd9f8ba84a68031b26445c1c96ee3d716482407fed18d42c7`.

## Runtime decision

Times are fresh-process medians in seconds from eleven retained alternating
observations on one isolated core. A candidate/baseline ratio below 1 favors
the candidate.

| Case | Metric | Baseline | Candidate | Ratio | Maximum | Result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| fannkuch-redux | wall | 0.653591 | 0.653479 | 0.999829x | 1.02x | pass |
| fannkuch-redux | CPU | 0.651303 | 0.651200 | 0.999842x | 1.02x | pass |
| n-body | wall | 0.376015 | 0.328484 | 0.873593x | 0.85x | **fail** |
| n-body | CPU | 0.373802 | 0.326308 | 0.872943x | 0.85x | **fail** |

The workflow stopped at that failed decision, so `spectral-norm` has no formal
runtime A/B result in this record. Its constructed QBE and application were
byte-identical, but they are artifact controls rather than runtime evidence.

## Build and compactness results

| Metric | Stage | Baseline | Candidate | Ratio | Maximum | Result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| compiler bytes | fixed point | 252,816 | 253,336 | 1.002057x | 1.03x | pass |
| compiler bytes | absolute | 262,000 | 253,336 | 0.966931x | 1.00x | pass |
| build wall | B2→B3 | 0.91 s | 0.92 s | 1.010989x | 1.05x | pass |
| build CPU | B2→B3 | 0.91 s | 0.92 s | 1.010989x | 1.05x | pass |
| build RSS | B2→B3 | 64,368,640 | 64,372,736 | 1.000064x | 1.05x | pass |
| build wall | B3→B4 | 0.92 s | 0.92 s | 1.000000x | 1.05x | pass |
| build CPU | B3→B4 | 0.91 s | 0.91 s | 1.000000x | 1.05x | pass |
| build RSS | B3→B4 | 64,315,392 | 64,339,968 | 1.000382x | 1.05x | pass |

| n-body artifact | Baseline | Candidate | Ratio | Maximum | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| QBE | 76,382 | 72,648 | 0.951114x | 1.01x | pass |
| raw executable | 24,032 | 23,136 | 0.962716x | 1.01x | pass |
| stripped executable | 24,024 | 23,128 | 0.962704x | 1.01x | pass |

## Retained evidence

GitHub published artifact `native-runtime-ab-33484444996-1` as artifact ID
9791260707, 391,108 archive bytes, with SHA-256
`21a4d82713bc3ac6ea13bc878227b1f08d872d9fc1774ce70906d6af0b6bc01b`.

This result retains all 473 extracted files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 474 files and excludes only this README and
itself. The tree includes exact workflow and compiler identities, both
bootstrap chains, build metrics, process and dependency inventories, generated
applications, correctness summaries, raw runtime observations, independently
reproduced medians, catastrophic checks, and the failed decision rows.

## Conclusion

The result proves that root publication is a material cost in safe-point-free
numeric functions, but removal alone does not meet the preregistered signal.
Future work should treat it as supporting evidence rather than silently retain
it. A separate bounded optimization may combine independently justified range,
Array-header, or generated-code improvements under its own baseline and frozen
decision contract; it must not retroactively change this result.

