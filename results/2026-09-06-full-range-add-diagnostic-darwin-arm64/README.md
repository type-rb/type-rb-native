# Full-range Integer-add diagnostic — Darwin arm64

Result: **rejected; no compiler or runtime change adopted**.
[Issue #277](https://github.com/type-rb/type-rb-native/issues/277) registered
both variants and their acceptance requirements before runtime measurement.
Baseline: `3cdcb1592b504e30de26631dc349197d6560c5bf`.

## Question and variants

Could removing a selected returning Integer-add fallback improve a numerical
loop, without weakening TypeRB's portable range? Both variants use verified
Integer operands/results and the original failure edge in scalar MIR plan14:

- Two-sided: reuse the existing upper/lower inline check and a non-returning
  failure edge.
- Biased: for `M = 2^53-1`, compute the signed64 sum and test
  `u64(sum + M) <= 2*M`. Portable operands ensure the sum and bias fit
  signed64. This preserves both endpoints, including valid negative sums.

Neither adds source-pattern analysis, a new fact family or benchmark assumptions.
Call selection, literal proofs and the existing inline budget remain unchanged.
The superseded add branch is removed from the multiply-only adapter.

## Retained results

Ratios are candidate/baseline; values above1 mean more time. Each independent
cohort alternates A/B and B/A and retains seven observations per role after
two warmups. All72 processes across four cohorts have exact expected stdout,
empty stderr and status0. No retained observation exceeds the registered2x
catastrophic limit. RSS median ratios are0.993289 for two-sided and1.0 for biased.

| Variant / cohort | Wall ratio | CPU ratio | Decision |
| --- | ---: | ---: | --- |
| Two-sided1 | 1.103327 | 1.099990 | Fails0.98 runtime limit |
| Two-sided2 | 1.096894 | 1.098475 | Fails0.98 runtime limit |
| Biased1 | 1.056504 | 1.057754 | Fails0.98 runtime limit |
| Biased2 | 1.062515 | 1.062149 | Fails0.98 runtime limit |

| Compiler | Complete bytes | Mach-O text bytes | Compiler QBE bytes |
| --- | ---: | ---: | ---: |
| Baseline | 349224 | 248364 | 1115091 |
| Two-sided, corrected verifier consumers | 349224 | 248156 | 1114757 |
| Biased | 349224 | 248540 | 1116382 |

Two-sided compiler QBE SHA256:
`6ae8c50be44a651485a066f7f570e831491d1fd92a9c0382820f1b4795a664b4`.
Biased compiler QBE SHA256:
`fff7fc481ccf0e137a78a7b40a62256a85ad3ff33de51c6e72d7841efb2acb9c`.
The biased compiler also misses strict compiler-QBE/text shrink. Complete
spectral executables remain50984 bytes. Two-sided spectral QBE grows from
52173 to52353 bytes. Ordinary same-basename B2/B3 binary identity was checked
for the initial two-sided and biased variants; this is not target acceptance.

The initial two-sided patch missed two plan-number consumers in the Array-loop
verifier. The corrected patch fixes both; its spectral QBE is byte-identical
to the measured initial variant. Two stale unit expectations were also repaired:
the removed selected helper call and the now-valid former invalid opcode.
The full compiler suite retained101/102 passes with that stale opcode expectation;
the corrected focused MIR multiply/add/Array suite subsequently passed8/8.
No complete post-correction recovery or cross-target acceptance is claimed.

The three synthetic controls cover upper/lower endpoints, mixed-sign
cancellation, negative results, dynamic operands, three call sites (including
an unselected call), and both overflow directions. Both candidates match the
accepted Native status/stdout/stderr exactly and the pinned reference behavior.
The retained reference observations include the panic first line, not transient
Go stack paths; Native diagnostics are retained in full.

## Reproduction and measurement boundary

- Apple M2 Pro, Darwin arm64, macOS26.6.2; ordinary local process execution,
  no CPU pinning or controlled-frequency claim. No concurrent heavy test/build
  batch ran during these cohorts.
- QBE1.3, target `darwin-arm64-v0`, system `/usr/bin/cc`.
- Reference revision `5dc09070cf7f88a569279f5e63982a6de59d692c` for controls.
- Unmodified `benchmarks/benchmarksgame/spectral-norm/src/main.trb`, input5500.
  Source SHA256 `b85e0d8cecf4e7455bdd34a6a02cb3a9a6e7bbe57ec29bb2f1b99afbbb5312f2`;
  expected-output SHA256 `f9d5b5e3eb7657cf1bbba4cc856651864df9cd9fd9a6be9b9bc5fcbb67150deb`.
- Existing `tools/native-mir-guarded-multiply/measure.py` is reused unchanged
  as the A/B controller. SHA256
  `f03adc024300e0be5d8304ebd1000a5a390d9f8acaceadf3c10375643e27a45e`.
  It uses monotonic wall time and wait4 child CPU/RSS, excluding compilation.

Each `*.patch.json` contains an exact unified diff in its `patch` field,
applicable to the baseline. JSON preserves whitespace without making diff
context look like whitespace errors. Decode outside a configured project and
apply only to a diagnostic checkout. Compile each control as its own file root.

Build baseline and candidate executables through their ordinary Native compiler,
then run (with absolute executable/output paths):

```sh
python3 tools/native-mir-guarded-multiply/measure.py \
  BASELINE_EXECUTABLE CANDIDATE_EXECUTABLE \
  benchmarks/benchmarksgame/spectral-norm/expected/5500.txt \
  UNIQUE_EVIDENCE_DIRECTORY 5500 0.98
```

## Consequence and re-entry

Do not promote either variant, relax bounds, run hosted acceptance to rescue
these misses, or update the accepted Pages snapshot. Fannkuch12/n-body50000000
formal controls were not run because local promotion already failed. This is
not evidence about Pure Go parity or long-running memory behavior.

Assembly inspection shows extra hot-path checks/branches for two-sided and
an extra biased addition for biased despite removal of returning calls. It
does not prove which microarchitectural effect explains the whole regression.
Revisit only with a measured reduction in executed hot-path work (for example,
an owned and verified range proof), not the assumption that fewer helper calls
must be faster. The current accepted guarded path remains in place. Existing
MIR ownership and compactness recovery obligations remain open.
