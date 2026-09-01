# Rejected Loop-Invariant Array-Length Result on Linux arm64

The bounded loop-preheader candidate is not retained. It preserved every
registered output, control, compactness, build-cost, memory, and application
size condition, but improved the required `spectral-norm` wall and CPU medians
by only about 0.6%. The frozen acceptance condition required at least 3%.

The threshold was not relaxed after observing the result. The implementation
is reverted; this directory retains the complete formal evidence so its code
shape and measured effect can inform a separately registered loop optimization.

## Exact scope

- accepted Native baseline:
  `473a6dee19b637a3009937d9b288c3a91f429a6b`;
- measured candidate:
  `b3e0c879ec376bc37ddd02ecfdf083343c69e762`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Native target profile `linux-arm64-v0`, QBE 1.3, GCC 13.3.0,
  LLD 18.1.3, and BenchExec `runexec` 3.35;
- fresh GitHub-hosted `ubuntu-24.04-arm` runner with four Neoverse-N2
  logical CPUs and Linux 6.17; and
- authoritative formal run
  [33517234091](https://github.com/type-rb/type-rb-native/actions/runs/33517234091).

Two earlier formal revisions were also rejected without changing a threshold.
Run [33509649899](https://github.com/type-rb/type-rb-native/actions/runs/33509649899)
exceeded the `n-body` executable limit. Runs
[33513972583](https://github.com/type-rb/type-rb-native/actions/runs/33513972583)
and [33516012365](https://github.com/type-rb/type-rb-native/actions/runs/33516012365)
kept both the Array length and data pointer live across an existing scalar
helper call; Linux arm64 added callee-saved register traffic and the raw
`spectral-norm` executable remained 32 bytes above the frozen limit. Hoisting
only the length removed that size regression and reached runtime measurement.

## Candidate boundary

The final candidate recognized only a small, non-nested
`while scalar < array.size()` loop over one immutable Array. It rejected high
local pressure, mutation, managed-value or opaque calls, and unknown methods.
It moved the stable length load to the preheader while leaving the data pointer
local to each indexed access so scalar helper calls did not extend that value's
live range.

The authored TypeRB sources, negative-index behavior, bounds checks, portable
Integer checks, and collector were unchanged.

## Correctness and fixed points

- all 55 local Gate 4 frontend tests passed, including mutation,
  managed-call, and high-pressure rejection cases;
- both Linux arm64 compiler chains closed exact B2/B3/B4 fixed points;
- all three applications returned status zero, exact registered stdout, and
  empty stderr before and during timing;
- every retained observation passed the 2.0x catastrophic boundary; and
- `fannkuch-redux` and `n-body` QBE and executables were byte-identical.

The baseline fixed compiler is 254,960 bytes with SHA-256
`65b18c8999e91dbb67e7dabb5d731987daa32076c9e4cd709962dc4b49bb73cb`.
The candidate is 257,472 bytes with SHA-256
`c4a91f54f9e07eb80934899e8f909337bdcbfde0f2ca14d7291b1c6d8b95e1f0`.

## Runtime decision

Times are fresh-process medians in seconds from eleven retained alternating
observations on one isolated core. A candidate/baseline ratio below 1 favors
the candidate.

| Case | Metric | Baseline | Candidate | Ratio | Maximum | Result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| fannkuch-redux | wall | 0.604824 | 0.605038 | 1.000354x | 1.02x | pass |
| fannkuch-redux | CPU | 0.602595 | 0.602599 | 1.000007x | 1.02x | pass |
| n-body | wall | 0.269381 | 0.269168 | 0.999209x | 1.02x | pass |
| n-body | CPU | 0.267200 | 0.267131 | 0.999742x | 1.02x | pass |
| spectral-norm | wall | 8.323370 | 8.271920 | 0.993819x | 0.97x | **fail** |
| spectral-norm | CPU | 8.321060 | 8.269850 | 0.993846x | 0.97x | **fail** |

Candidate median RSS was identical to baseline in all three cases: 524,288
bytes for both controls and 1,208,320 bytes for `spectral-norm`.

## Build and compactness results

| Metric | Stage | Baseline | Candidate | Ratio | Maximum | Result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| compiler bytes | fixed point | 254,960 | 257,472 | 1.009853x | 1.02x | pass |
| compiler bytes | absolute | 260,000 | 257,472 | 0.990277x | 1.00x | pass |
| build wall | B2→B3 | 0.91 s | 0.95 s | 1.043956x | 1.05x | pass |
| build CPU | B2→B3 | 0.90 s | 0.94 s | 1.044444x | 1.05x | pass |
| build RSS | B2→B3 | 64,380,928 | 64,368,640 | 0.999809x | 1.05x | pass |
| build wall | B3→B4 | 0.90 s | 0.94 s | 1.044444x | 1.05x | pass |
| build CPU | B3→B4 | 0.89 s | 0.93 s | 1.044944x | 1.05x | pass |
| build RSS | B3→B4 | 64,315,392 | 64,397,312 | 1.001274x | 1.05x | pass |

| spectral-norm artifact | Baseline | Candidate | Ratio | Maximum | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| QBE | 53,590 | 53,508 | 0.998470x | 1.005x | pass |
| raw executable | 19,888 | 19,888 | 1.000000x | 1.001x | pass |
| stripped executable | 19,880 | 19,880 | 1.000000x | 1.001x | pass |

## Retained evidence

GitHub published artifact `native-runtime-ab-33517234091-1` as artifact ID
9804361567, 446,184 archive bytes, with SHA-256
`561832635f90653d48912eb4d6b4036a58afbc16aeda31b4bf38191e15592def`.

This result retains all 665 extracted files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 666 files and excludes only this README and
itself. The tree includes exact workflow and compiler identities, both
bootstrap chains, build metrics, process and dependency inventories, generated
applications, correctness summaries, all raw runtime observations, medians,
catastrophic checks, failed decision rows, and workspace residue inventories.

## Conclusion

Stable Array length hoisting is correct and compact at this boundary, but it is
too small a standalone improvement to retain. The evidence also shows that
retaining the data pointer across a scalar helper call creates enough register
pressure to erase the compactness margin. Future work should use a separately
registered loop optimization with a stronger source-level proof and measured
runtime signal rather than silently combining unrelated changes into this
failed candidate.
