# Native MIR Stable Array-Header Verification

This record separates the bounded optimization's correctness and same-host
A/B evidence from the complete cross-language benchmark snapshot.

Status: **not accepted**. The selected spectral-norm improvement passes its
original 10% goal, but the n-body control regresses by 13.2%. This is a
different failure from the near-target local observation retained below.

The candidate is `69ff52b5fe474c87628b132124c7d8e875e627a8`, introduced by
[PR #246](https://github.com/type-rb/type-rb-native/pull/246) under
[issue #245](https://github.com/type-rb/type-rb-native/issues/245). The measured
baseline is the PR base `a001262305d5522b95e1ca67e71fc002e3ad4c61`; its compiler
and benchmark sources are identical to the frozen optimization baseline
`00009fa304a36b9cba70b123120a469347b3882d`.

## Bounded behavior

The pass and verifier independently select an immutable Array parameter from
raw, ordered region operations. QBE lowering loads that parameter's length and
data pointer once at function entry. This is header-only reuse: it does not
remove Array address or bounds checks, infer an unchecked loop index, or assume
benchmark-only operand values. Unproven effects reject the plan. The existing
direct-emitter fallback remains a separately invalidated migration path.

Shared checked MIR instruction and value-row builders recover compiler space
without changing the three generated benchmark applications relative to the
preceding corrected candidate. The broader portable range/index/induction
recovery obligation and the temporary compiler-size ceilings remain unchanged.

## Retained local near-target observation

`local-spectral-recheck` preserves the original raw observations, exact output
files, and failed summary. At input 5500, two warmups and seven alternating
retained processes per role produce these medians:

| Metric | Baseline | Candidate | Candidate / baseline |
| --- | ---: | ---: | ---: |
| Wall seconds | 2.732177958 | 2.462010708 | 0.901116525 |
| CPU seconds | 2.685697 | 2.374400 | 0.884090797 |
| Peak RSS bytes | 2,490,368 | 2,441,216 | 0.980263158 |

Every output passes, and no retained observation exceeds the catastrophic
bound. Wall time improves by 9.888%, but the original wall-ratio goal of 0.90
is missed. The summary therefore still says `status: fail` and
`thresholdsPass: false`; neither the observation nor the original goal is
relabeled as passing.

The [explicit near-target disposition](https://github.com/type-rb/type-rb-native/pull/246#issuecomment-5548866678)
states that this marginal goal miss alone is not grounds to discard this
repaired candidate. It does not waive correctness, memory, build, compactness,
fixed-point, catastrophic, or control-regression requirements, and it is not a
general threshold change for later work. The separately registered hosted run
remains an independent observation, not a retry-until-passing selection from
this local run.

The local candidate executable SHA-256 is
`4614cefcd89fd3421dec04e0fe277104a744c3a90ce1f6069c28c4f3a36c3c04`;
the baseline is
`2cb4826ce5f2e019d905939319d964ea26ae2f9f70f49411162b169339c317a2`.
Both are 50,992 bytes. These local identities are not substituted for the
hosted compilers or the complete Pages benchmark artifacts.

## Complete hosted observation

Ready-PR [run 33939737675](https://github.com/type-rb/type-rb-native/actions/runs/33939737675)
retains the following Linux arm64 medians over two warmups and seven
alternating retained processes per role:

| Workload | Baseline wall seconds | Candidate wall seconds | Wall ratio | CPU ratio | RSS ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| spectral-norm, 5500 | 4.081436718 | 3.592571062 | 0.880222 | 0.880212 | 1.000000 |
| fannkuch-redux, 12 | 84.821020534 | 84.827091202 | 1.000072 | 1.000082 | 0.999620 |
| n-body, 50000000 | 10.448269730 | 11.823397073 | 1.131613 | 1.131557 | 1.000000 |

Spectral-norm reduces wall time by 11.978% and passes the original 0.90 ratio
goal. Fannkuch-redux remains effectively neutral and has byte-identical
baseline/candidate executables. N-body instead increases wall time by 13.161%
and CPU time by 13.156%, exceeding the unchanged 1.02 control limit. Every
output passes, and every retained observation remains below the catastrophic
bound. The final acceptance job correctly reports failure.

Correctness, Linux arm64/amd64 regressions, Darwin/Linux persistent-worker
smoke, fixed points, build cost, artifact limits, and shared target-neutral QBE
checks all pass. This is not fresh full leak-soak evidence or a production
service claim. Both arm64 targets emit identical 1,119,802-byte compiler QBE
with SHA-256
`6efdfdc8a9f6b50789fd0e2b3deef10732218d51e4e1ecad00e8a0e27c36874d`.

| Target | Baseline compiler bytes | Candidate compiler bytes | Build wall ratio | Build RSS ratio |
| --- | ---: | ---: | ---: | ---: |
| Darwin arm64 | 349,208 | 349,224 | 0.995624 | 0.996630 |
| Linux arm64 | 313,224 | 315,368 | 1.034783 | 1.000730 |

Selected spectral QBE shrinks from 52,343 to 52,173 bytes; selected code
sections shrink from 10,732 to 10,684 Darwin bytes and from 11,360 to 11,296
Linux bytes. N-body QBE grows from 67,246 to 67,873 bytes and Linux executable
text from 13,536 to 13,712 bytes. These artifact changes fit their registered
limits but do not excuse the measured runtime regression.

## Disposition

The [formal-result review](https://github.com/type-rb/type-rb-native/pull/246#issuecomment-5549122032)
keeps this candidate unmerged. Explicit acceptance of an approximately 9.9%
local improvement does not waive a separate 13.2% control regression. Do not
publish this revision as the accepted benchmark snapshot, relax the control
limit retrospectively, or select a passing rerun of unchanged code.

The direct fallback changed from two recent Array-header entries to one while
adding a separate verified persistent parameter header. That representation
change is an investigation target, not yet a proved cause. An isolated
diagnostic must separate its effect from other lowering changes before a
replacement candidate is registered and measured.

The retained target artifacts are `9961896682` (Darwin), `9962255906` (Linux),
and `9962258368` (cross-target). Raw observations, summaries, bootstrap
identities, size comparisons, and catastrophic checks remain alongside the
local failed diagnostic. Nothing in this record converts either failed
result into acceptance.

`ARTIFACTS.tsv` records the original hosted archives and their GitHub digests.
Repository text copies normalize CRLF, trailing horizontal whitespace, and
end-of-file blank lines. Observation values and program output content are
unchanged. `EVIDENCE_SHA256SUMS` covers 218 evidence files, excluding only this
README and the checksum file itself.
