# Formal Safe-point-free Loop Root Result on Linux arm64

The safe-point-free loop-root candidate passes every registered correctness,
fixed-point, compactness, build-cost, and runtime condition. On the exact
checked-in `fannkuch-redux` source at input 10, it reduces median wall time by
12.46% and median CPU time by 12.47% against the accepted Native baseline.
`n-body` and `spectral-norm` remain unchanged within measurement noise.

This is an implementation result for these exact programs, inputs, compiler
revisions, and toolchains. It is not a language-wide performance claim or a
claim of parity with the separately measured Pure Go programs.

## Exact scope

- accepted Native baseline:
  `55d428b05d6ad8841a3fe23d52cfc4b0d98eb4fa`;
- measured candidate:
  `0392bb40b761749dee4d0fd8eac1378820959c5c`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Native target profile `linux-arm64-v0`, QBE 1.3, GCC 13.3.0,
  LLD 18.1.3, and BenchExec `runexec` 3.35;
- fresh GitHub-hosted `ubuntu-24.04-arm` runner with four Neoverse-N2
  logical CPUs and Linux 6.17; and
- successful formal run
  [33536377612](https://github.com/type-rb/type-rb-native/actions/runs/33536377612).

The candidate implements the exact boundary registered by
[issue #182](https://github.com/type-rb/type-rb-native/issues/182). While
lowering a loop that owns managed locals, the compiler observes every emitted
operation that can start collection. If neither the condition nor any body
path contains such an operation, the existing root-publication block moves
from the loop header to the loop exit. Allocation, Array growth,
managed-result production, opaque calls, and nested safe points conservatively
keep publication at the header.

Root capacity reservation, root publication for loops that can collect,
function-return cleanup, managed-return rooting, mutation behavior, and every
existing collection boundary remain unchanged.

## Correctness and fixed points

- all 80 repository tests and all 56 Gate 4 tests passed;
- exact generated-QBE checks cover eligible loops plus Array growth,
  allocation, managed-result, opaque-call, nested-loop, zero-iteration,
  early-return, and post-loop-allocation paths;
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

The baseline fixed compiler is 254,960 bytes with SHA-256
`65b18c8999e91dbb67e7dabb5d731987daa32076c9e4cd709962dc4b49bb73cb`.
The candidate is 254,976 bytes with SHA-256
`07cce7e8fc48289a875e4c5fc4a054f7ab3b252ec41c3edcba8bdd03a17dbcff`.
The candidate fixed-point QBE is 887,244 bytes with SHA-256
`873b592df18267a47ff88d8c1c67d61614468495dd7fd75922841d789af9305c`.

## Runtime result

Times are fresh-process medians in seconds from eleven retained alternating
observations on one isolated core. A candidate/baseline ratio below 1 favors
the candidate.

| Case | Metric | Baseline | Candidate | Ratio | Maximum | Result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| fannkuch-redux | wall | 0.604774 | 0.529404 | 0.875375x | 0.95x | pass |
| fannkuch-redux | CPU | 0.602512 | 0.527349 | 0.875251x | 0.95x | pass |
| n-body | wall | 0.268753 | 0.268960 | 1.000770x | 1.02x | pass |
| n-body | CPU | 0.266569 | 0.266672 | 1.000386x | 1.02x | pass |
| spectral-norm | wall | 8.323950 | 8.323580 | 0.999956x | 1.02x | pass |
| spectral-norm | CPU | 8.320950 | 8.320210 | 0.999911x | 1.02x | pass |

Median process-tree memory was 524,288 bytes for both `fannkuch-redux`
executables, 524,288 bytes for both `n-body` executables, and 1,208,320 versus
1,212,416 bytes for `spectral-norm`. Every individual memory observation
remained within the registered catastrophic bound.

## Build and compactness results

| Metric | Stage | Baseline | Candidate | Ratio | Maximum | Result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| compiler bytes | fixed point | 254,960 | 254,976 | 1.000063x | 1.02x | pass |
| compiler bytes | absolute | 260,000 | 254,976 | 0.980677x | 1.00x | pass |
| build wall | B2→B3 | 0.91 s | 0.90 s | 0.989011x | 1.05x | pass |
| build CPU | B2→B3 | 0.91 s | 0.90 s | 0.989011x | 1.05x | pass |
| build RSS | B2→B3 | 64,290,816 | 64,471,040 | 1.002803x | 1.05x | pass |
| build wall | B3→B4 | 0.91 s | 0.90 s | 0.989011x | 1.05x | pass |
| build CPU | B3→B4 | 0.90 s | 0.90 s | 1.000000x | 1.05x | pass |
| build RSS | B3→B4 | 64,385,024 | 64,335,872 | 0.999237x | 1.05x | pass |

All generated applications passed their frozen QBE, raw-executable, and
stripped-executable limits. `fannkuch-redux` is byte-identical at 53,710 QBE
bytes and 19,176 raw executable bytes. `n-body` QBE shrinks from 71,090 to
70,948 bytes while its 22,912-byte raw executable remains identical.
`spectral-norm` QBE changes from 53,590 to 53,591 bytes while its 19,888-byte
raw executable remains identical.

## Retained evidence

GitHub published artifact `native-runtime-ab-33536377612-1` as artifact ID
9812021809, 446,220 archive bytes, with SHA-256
`0885e729a31fae7fd74ad6be022337d03cc372ca2401c59f9928525d85b24132`.

This result retains all 665 extracted artifact files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 666 files and excludes only this README and
itself. The tree includes exact workflow and compiler identities, both
bootstrap chains, build metrics, process and dependency inventories, generated
applications, correctness summaries, all raw runtime observations,
independently reproduced medians, catastrophic checks, and final decision
rows. The retained workspace temporary-file inventory is empty.

## Conclusion

Moving root publication out of proven safe-point-free loop iterations is a
material generated-code improvement for the Array-intensive permutation
kernel and composes with the previous safe Array-header optimization. It is
retained without changing TypeRB semantics or any preregistered threshold.
Future optimization continues from fresh profiles and the explicit minimum
objective of matching or beating Pure Go runtime on representative workloads
while preserving the existing build-time, memory, and compactness advantages.
