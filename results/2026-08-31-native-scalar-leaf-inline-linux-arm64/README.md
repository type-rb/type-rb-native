# Rejected Native Scalar-Leaf Inlining Result on Linux arm64

The bounded scalar-leaf inliner did not satisfy its preregistered compiler
compactness contract and is not retained. Correctness, target-neutral QBE, and
all three current target regressions passed, but the self-hosted compiler grew
from 268,248 to 274,160 bytes. The 1.022039 candidate/baseline ratio exceeds
the frozen 1.001 maximum.

The workflow stopped at the first failed decision bound, before building or
timing the benchmark applications. Local Darwin observations showed that the
mechanism could remove the intended hot calls, but there is no formal Linux
arm64 runtime conclusion. The implementation was reverted without weakening
the registered threshold.

## Exact scope

- Native baseline commit:
  `0f47644a448190a05bac2710f1e080b4d618ea78`;
- candidate implementation commit:
  `be5488f2634886ae0677a2277320e2a41d3ec054`;
- measured pull-request merge commit:
  `43fc547bfe4250fc0371ecfbb5d74943a6fdfc01`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Native target profile `linux-arm64-v0`, QBE 1.3, GCC 13.3.0, and
  LLD 18.1.3; and
- failed formal run
  [33379548760](https://github.com/type-rb/type-rb-native/actions/runs/33379548760).

The candidate implemented the exact boundary registered by
[issue #142](https://github.com/type-rb/type-rb-native/issues/142): programs
with at most 32 user functions, scalar-only immutable leaf bodies, lexical
loop call sites, and a deterministic two-site program-wide budget. Arguments
were evaluated once from left to right, and the normal outlined function
remained emitted.

## Verification that passed

- the Gate 4 frontend suite passed all 43 tests;
- the valid and runtime-invalid conformance corpus passed across candidate
  B2, B3, and B4;
- Darwin arm64 and Linux arm64 bootstrap chains reached exact fixed points;
- the current Linux amd64 and Linux arm64 target-neutral compiler QBE matched
  byte for byte;
- the current Darwin arm64, Linux amd64, and Linux arm64 regression jobs
  passed; and
- formatter, project checker, shell syntax, and measurement-controller tests
  passed.

These results establish that the rejection is a compactness decision, not a
known correctness or portability failure.

## Failed compactness bound

| Artifact | Baseline | Candidate | Ratio | Maximum | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| self-hosted compiler | 268,248 bytes | 274,160 bytes | 1.022039 | 1.001 | fail |
| fixed-point compiler QBE | 932,951 bytes | 955,863 bytes | 1.024559 | not a separate decision bound | recorded |

The baseline B2/B3/B4 compiler SHA-256 is
`6ced62abb82a85088556d849826da97613bdb7b0dfd0860413a0f9672f363e41`.
The candidate B2/B3/B4 SHA-256 is
`dcb0636ad1d6564757590671a6c6a137166a741d6a21534ee466ecf715ceb0ca`.

The retained bootstrap observations also stayed within the build-cost limits:
candidate/baseline wall ratios were 1.038835 and 1.029126 for B2-to-B3 and
B3-to-B4, while peak-RSS ratios were 0.999427 and 0.999364. The workflow did
not add these rows to `comparison.tsv` because the preceding compiler-size
check terminated the decision step immediately.

## Retained evidence

GitHub published artifact `native-runtime-ab-33379548760-1` as artifact ID
9753226959, 16,735 archive bytes, with SHA-256
`f35424069025946e20627b5507f32cab56ff7a0997497af424e0f428303f66b4`.
This result retains all 28 extracted artifact files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 29 files and excludes only this README and
itself.

- [`compiler-comparison-evidence`](native-runtime-ab-33379548760-1/compiler-comparison-evidence)
  records the failed compiler-size decision.
- [`baseline-bootstrap-evidence`](native-runtime-ab-33379548760-1/baseline-bootstrap-evidence)
  and [`candidate-bootstrap-evidence`](native-runtime-ab-33379548760-1/candidate-bootstrap-evidence)
  retain fixed-point identities, raw measurements, process traces, and
  executable inventories.
- [`workflow-evidence`](native-runtime-ab-33379548760-1/workflow-evidence)
  retains the exact measured revision, toolchain, workflow hashes, and clean
  temporary-file inventory.

## Conclusion

Inlining these two hot scalar call sites can improve the selected kernel, but
the general mechanism adds materially more compiler code than the registered
compactness budget permits. Future work should prefer smaller shared lowering
improvements or a substantially more compact inlining representation rather
than retaining this implementation or relaxing its threshold.
