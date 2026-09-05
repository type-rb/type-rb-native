# Accepted Native MIR Stable Array-Header Verification

The complete [formal run 33946793548](https://github.com/type-rb/type-rb-native/actions/runs/33946793548)
passes at `c131c43c71c516706db99508cee796adff33ec05`. It is accepted in
[PR #246](https://github.com/type-rb/type-rb-native/pull/246), merged as
`5a23176040fee3541ed8578115622ffcd7aa2733`.

The measured baseline is `a001262305d5522b95e1ca67e71fc002e3ad4c61`, whose
compiler and benchmark sources equal the frozen optimization baseline
`00009fa304a36b9cba70b123120a469347b3882d`. This focused same-host A/B series
isolates the bounded optimization; it is not the cross-language Pages snapshot.

## Accepted scope and runtime

The independent MIR pass and verifier select header reuse only for an
immutable Array parameter with no blocking operation. Ordinary bounds checks
remain. The separate two-entry recent-header fallback retains its invalidation
rules and is still migration work. No new unchecked access or general alias
analysis is claimed. See the [proof and repair record](../../docs/native-mir-array-region-repair.md).

Linux arm64 uses two warmups and seven alternating retained processes per role
at the registered full inputs. Times are medians in seconds; ratios divide
candidate by the previous Native baseline, so lower is better.

| Workload | Baseline wall | Candidate wall | Wall ratio | CPU ratio | RSS ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| spectral-norm, 5500 | 4.081215329 | 3.596905668 | 0.881332 | 0.881264 | 1.000000 |
| fannkuch-redux, 12 | 84.829409112 | 84.831578976 | 1.000026 | 0.999976 | 1.000000 |
| n-body, 50000000 | 10.450687271 | 10.450329743 | 0.999966 | 0.999975 | 1.000000 |

Spectral-norm wall time falls by 11.867%. Its generated QBE shrinks from 52,343
to 52,173 bytes. Both controls retain byte-identical generated QBE and complete
executables. All output, 0.90 selected-runtime, 1.02 control, RSS, and 2.0
catastrophic bounds pass. Darwin provides application correctness and size
checks, not a separate formal runtime A/B series.

## Compiler and correctness

| Target | Complete compiler bytes | Code-section bytes | Build wall ratio | Build RSS ratio |
| --- | ---: | ---: | ---: | ---: |
| Darwin arm64 | 349,224 | 249,956 | 1.002688 | 0.997817 |
| Linux arm64 | 315,256 | 252,640 | 1.013216 | 1.000064 |

Both targets emit identical 1,119,022-byte compiler QBE, SHA-256
`55b1f79c8e0362080b4b5076669d7047c19850fb6ae1b8e8f7f47a0208fcb67d`.
The combined 664,480-byte compiler stays below 667,000 bytes. No numerical
limit changed. Recovery-enabled correctness, fixed points, both Linux target
regressions, process/cleanup checks, Darwin/Linux memory smoke, compactness,
and the required acceptance job pass. Full MIR migration and cumulative
compiler-size recovery are still due; memory smoke is not production leak-soak
or service evidence.

## Retained artifacts

| Artifact | ID | Archive bytes | GitHub SHA-256 |
| --- | ---: | ---: | --- |
| static-string-compactness-darwin-arm64 | 9963943549 | 12,699 | `62b0f1f21bb4d7f1f1e82e12c5bcfbc00d99af4146f3f753c7e2ea76dc856dab` |
| static-string-compactness-linux-arm64 | 9964243726 | 55,682 | `b97a6fa17ccfa9d819101ac942726fd67802f0c0732bbb4f24083322e31272c0` |
| static-string-compactness-cross-target | 9964246385 | 456 | `6bca69f1210c755cfdc5f496453c3ebd029343599054a90cf68a3f2c85b0bc10` |

`EVIDENCE_SHA256SUMS` inventories the three extracted artifacts, excluding only
this README and itself. Repository text copies normalize trailing horizontal
whitespace and end-of-file blank lines. The table identifies the original
GitHub archives. The [rejected `69ff52b5` result](../2026-09-05-native-mir-stable-array-headers-darwin-linux-arm64/README.md)
retains its failed n-body control and is not relabeled as accepted.
