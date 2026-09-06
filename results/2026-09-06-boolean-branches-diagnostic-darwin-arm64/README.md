# Checked Boolean branches — local Darwin arm64 diagnostic

Result: both registered local cohorts pass; **formal acceptance remains pending**.
[Issue #288](https://github.com/type-rb/type-rb-native/issues/288) records the
candidate and unchanged limits before implementation and timing.

## Change

QBE comparisons can directly produce canonical long 0/1 Boolean values, and
`jnz` can consume their low word. Remove word-result extension and the repeated
comparison with zero from checked conditions. Scalar MIR negation and direct
lowering share this representation without changing the Boolean ABI, arithmetic
or Array guards, GC roots, call selection, inline budget or TypeRB semantics.
No new fact family, source-pattern analysis or benchmark-specific rule is added.

For example, the spectral inner-loop branch changes from a comparison,
`cset`, redundant word move, comparison with zero and branch into one comparison
and branch. This is a generated-code observation, not a claim that instruction
count alone explains every measured difference.

## Retained runtime observations

Ratios are candidate/baseline; below 1 means less time or memory. Each of two
cohorts has two warmups and seven retained observations per role, alternating
retained A/B and B/A order. All 108 processes produce exact expected stdout,
empty stderr and status zero. All registered bounds pass, including each
role's retained wall/CPU/RSS observations <=2x the respective baseline median.

| Case / cohort | Input | Wall ratio | CPU ratio | RSS ratio |
| --- | ---: | ---: | ---: | ---: |
| spectral-norm / 1 | 5500 | 0.941097 | 0.940508 | 1.013423 |
| spectral-norm / 2 | 5500 | 0.941907 | 0.942553 | 1.006757 |
| fannkuch-redux / 1 | 10 | 0.912380 | 0.914216 | 1.011765 |
| fannkuch-redux / 2 | 10 | 0.927814 | 0.915527 | 1.011765 |
| n-body / 1 | 1000000 | 1.007511 | 0.970688 | 0.988372 |
| n-body / 2 | 1000000 | 0.981032 | 0.976193 | 0.988372 |

Spectral wall medians are 2.355919167 -> 2.217148833 and
2.354310000 -> 2.217542167 seconds, about 5.8-5.9% less time. The required
wall/CPU ratios are <=0.98 for spectral and <=1.02 for both controls; median RSS
must be <=1.05. Short control inputs do not replace full cross-language inputs.
In particular, local n-body lasts about 0.11 seconds and includes process-launch
overhead, so these controls are not headline full-workload scores.

## Correctness, compactness and integration

Measured baseline: `8b29b45d69c2006e13d997dfee507c3e6b1e93a9`.
Measured candidate `compiler.trb` SHA256:
`1ced840d875e1e1feb3561d5dc936d94aea19b33583d59049bcace30986d4690`.
The exact production patch is retained in `candidate.patch.json`.

| Compiler / measured source pair | Complete bytes | Mach-O text | Compiler QBE |
| --- | ---: | ---: | ---: |
| Baseline | 349224 | 248368 | 1115716 |
| Candidate | 332712 | 232240 | 1049453 |

Ordinary B2/B3 executables are identical. Recovery-enabled root/compiler suites
pass 90/106 tests, with 192 passes across 64 corpus cases and three ordinary
generations. Repeated and adjacent corpus QBE agree. GC and persistent-worker
smoke checks close allocation accounting with final managed live bytes zero;
they do not establish the absence of every long-running resource leak.

Retained development failures were invalid fixture assumptions and stale
output-shape assertions, not changes to the frozen production candidate:
Boolean Arrays are unsupported by both Native revisions; supported records and
bindings replace them in the valid fixture while an explicit unsupported-type
unit remains. Call controls now respect the shared inline budget. Two exact GC
temporary-number expectations and six Float comparison-width expectations were
updated without removing root-order or arithmetic-safety checks. The corrected
full suites pass; the initial joined suite did not. A local invocation of the
hosted bootstrap harness was rejected before setup because the local runner
label is not a hosted image; the all-corpus check is explicitly local evidence.

After PR #286, the implementation was integrated with main
`6f7e3ba10623d40b5b0f7e6cc03b732125607795`. Integrated compiler source SHA256:
`fd7e19e9188e8a4d55177925033b9e35f94a9ac3e1d2c282246c5d3844174e2e`.
Both new compiler chains reach exact B2/B3 fixed points. Their complete sizes
remain 349224 -> 332712, text is 249804 -> 233556 and QBE 1122621 -> 1055831.
Both integrated roles produce byte-identical QBE **and executables** to their
measured counterparts for all three workloads. This preserves the measured
application identities; it does not relabel old compiler-build observations as
current-main measurements. The integrated recovery-enabled root/compiler suites
also pass 90/107 tests. Hosted checks remain separate and pending.

## Measurement scope and reproduction

Apple M2 Pro, macOS 26.6.2, Darwin arm64; QBE 1.3, `/usr/bin/cc`, target
`darwin-arm64-v0`. The pinned reference for differential controls is
`5dc09070cf7f88a569279f5e63982a6de59d692c`.

The diagnostic's heavy correctness/build batches finished before timing. Host-wide
CPU isolation was not enforced; unrelated activity, frequency and scheduling
effects were not excluded. These observations do not isolate one hardware cause.

The existing `tools/native-mir-guarded-multiply/measure.py` is reused unchanged
(SHA256 `f03adc024300e0be5d8304ebd1000a5a390d9f8acaceadf3c10375643e27a45e`).
Its legacy success label does not describe this Boolean candidate. It measures
monotonic wall time and wait4 child CPU/RSS, excluding compilation. Each retained
`raw.csv` includes warmups and every observation; `summary.json` records binary
hashes, exact medians, bounds and output-verification results.

Build both revisions' programs from the identical authored source, then run
the controller twice with unique evidence directories and the registered input
and ratio for each program:

```sh
python3 tools/native-mir-guarded-multiply/measure.py \
  BASELINE_EXECUTABLE CANDIDATE_EXECUTABLE EXPECTED_STDOUT \
  UNIQUE_EVIDENCE_DIRECTORY INPUT RUNTIME_RATIO_LIMIT
```

Use absolute executable, oracle and output paths. Decode the patch JSON outside
a configured project when reproducing the original source pair.
The named formal Linux arm64 contract is documented in
[the A/B controller](../../tools/native-runtime-ab/README.md).
This local result does not establish Pure Go parity or update Pages.
