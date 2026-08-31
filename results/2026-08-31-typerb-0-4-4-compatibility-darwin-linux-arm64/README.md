# TypeRB 0.4.4 Development Compatibility Revalidation Results

TypeRB Native passes the registered exact-revision compatibility revalidation
for TypeRB `0.4.4-dev` on Darwin arm64, Linux arm64, and the existing Linux
amd64 regression path. Repository source uses the current scoped file API,
the previous-Native bootstrap chains remain Go-free, and the canonical
self-hosted compiler is byte-identical to the registered Native baseline.

This is experimental exact-revision evidence. It does not establish a TypeRB
version range, complete language coverage, stable Native compatibility, or
production support.

## Registered scope and revisions

- preregistered scope:
  [issue #144](https://github.com/type-rb/type-rb-native/issues/144)
- selected TypeRB source, formatter, checker, and semantic oracle:
  `5dc09070cf7f88a569279f5e63982a6de59d692c` (`0.4.4-dev`)
- Native baseline:
  `67595e45e566db9e1774e663a3c513c4b710d6db`
- measured Native implementation and workflow revision:
  `8580649852ac4467139a05cc3c1d87a1b987a911`
- immutable seed source revision:
  `0058818314977633c50393796ef9b9f8f1fda50f`
- QBE 1.3 source archive: 281,332 bytes, SHA-256
  `d587905d620dc5e1d2bfa7c2cc642b9b837aa89a3188c6e37b53d756cf66e320`
- successful candidate workflow:
  [Actions run 33384675852](https://github.com/type-rb/type-rb-native/actions/runs/33384675852)
- successful same-toolchain baseline workflow:
  [Actions run 33385121391](https://github.com/type-rb/type-rb-native/actions/runs/33385121391)
- implementation and evidence:
  [PR #145](https://github.com/type-rb/type-rb-native/pull/145)

## Source migration and correctness

The selected TypeRB interval removes `trb/std/filesystem` and requires scoped
file ownership. All 39 affected repository sources in
[`migration-inventory.txt`](migration-inventory.txt) now use repository-owned
support built on `File.open`. Production reads default to a 67,108,864-byte
limit, writes use `FileMode::Write`, and recursive directory creation needed by
tests and benchmark controllers uses exact `/bin/mkdir -p` through shell-free
`Process.run`. Launch and exit failures are returned explicitly. The support is
copied into 19 independent configured source roots and is not imported by the
canonical three-file compiler closure.

Focused tests prove successful bounded reads, `TooLarge` failure, truncating
writes, recursive and idempotent directory creation, and stable nonzero-exit
error fields. The selected reference formats and checks all 46 checked-in
configured projects. With the selected reference and QBE enabled, the root
suite passes all 80 differential, executable, runtime, support, and bootstrap
tests, including the B0-to-B4 Gate 4 chain.

The candidate revision's protected checks also pass the Linux amd64 and Linux
arm64 target regressions, their target-neutral QBE comparison, and the
backend-pair comparison. The final protected source suite is recorded by the
PR checks alongside this retained evidence.

## Baseline identity and fixed points

The baseline and candidate workflows ran the same immutable seed verifier and
hosted-runner profiles. Their complete per-target `identities.txt` files and
combined-size records are byte-identical.

| Target | Exact baseline and candidate B2/B3/B4 compiler |
| --- | --- |
| Darwin arm64 | 299,576 bytes; `359c5a6f732d37189f7c6057ff02d1f628718b33176debbda3ac074a05bf0f0d` |
| Linux arm64 | 268,248 bytes; `6ced62abb82a85088556d849826da97613bdb7b0dfd0860413a0f9672f363e41` |

Every B2, B3, and B4 compiler on one target is exact. Both targets emit the
same 932,951-byte target-neutral QBE with SHA-256
`8fd0be84987bb2103b5e0f49f5ee1a55cc254813980b1cd4d40eb60e4a045f9f`.
That QBE and both target executable identities are also exact against Native
baseline `67595e45e566db9e1774e663a3c513c4b710d6db` on the same registered
toolchain.

The immutable seed still reaches the current compiler through two explicit,
untimed, Go-free setup transitions:

| Target | Published seed | First transition | Current-runtime transition |
| --- | --- | --- | --- |
| Darwin arm64 | 259,032 bytes; `ef438d13598c534766334b408a39715c56ff1b69db528910ebf7d90ec7720b65` | 303,832 bytes; `4b38f7605fa115fe03165418ec77e70ef9fdc2f2fde0a3102cb6632e23e518bd` | 322,536 bytes; `dde50ac327de3d42976332b3d1ca4850719f9d73f21ea50277d14764e0efd820` |
| Linux arm64 | 241,488 bytes; `b4307c244edc9e4da620f2a7c1b03a733e575da032efefae615f9edf75048a37` | 265,160 bytes; `dd2b9b599c77629a676020bac75d208aa2820d0e063fd0a572411a5e078d21d1` | 270,704 bytes; `1e0f5c352be3fcdfa86e21e83c332bdf150738d306cbc106b63e49bfb9106561` |

The transition executable hashes are also unchanged from the baseline run.
The revision label and an unmeasured setup elapsed value are the only expected
differences in transition metadata.

## Measurements

Each workflow performs two warmups followed by seven retained interleaved
observations of B2-to-B3 and B3-to-B4. Setup transitions are excluded. The
candidate-to-baseline ratios compare the same target and stage across the two
back-to-back successful workflows.

| Target and stage | Baseline elapsed | Candidate elapsed | Ratio | Baseline RSS | Candidate RSS | Ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Darwin B2-to-B3 | 1.86 s | 1.67 s | 0.898 | 41,074,688 | 40,960,000 | 0.997 |
| Darwin B3-to-B4 | 1.89 s | 1.69 s | 0.894 | 41,205,760 | 41,025,536 | 0.996 |
| Linux B2-to-B3 | 1.11 s | 1.05 s | 0.946 | 64,421,888 | 64,446,464 | 1.0004 |
| Linux B3-to-B4 | 1.08 s | 1.05 s | 0.972 | 64,380,928 | 64,385,024 | 1.0001 |

The worst candidate median ratio is 1.0004, below the registered 1.05 bound.
Within the candidate run, the worst adjacent-generation elapsed and RSS ratios
are 1.012 and 1.0016. The worst retained candidate observation is 1.004 times
its applicable baseline median, far below the catastrophic 2x threshold. No
observation failed.

## Process and dependency boundary

The Linux ordinary-chain trace records the B4 compiler, pinned QBE, exact
`/usr/bin/cc`, `/usr/bin/as`, GCC `collect2`, and `/usr/bin/ld.lld`. It contains
no Go executable, reference `trb`, recovery compiler, or shell-mediated
compiler child. The generated compiler is PIE with `BIND_NOW`, `RELRO`, one
non-executable `GNU_STACK` segment, and only `libc.so.6` as a dynamic library.

Darwin records the direct Native-to-QBE and Native-to-CC boundary and the
Mach-O dependency on `/usr/lib/libSystem.B.dylib`. Both setup-transition paths
record their compiler, QBE, CC, and forbidden-child boundary separately from
the ordinary measured chain.

## Compiler size

| Target | Candidate bytes | Limit | Headroom |
| --- | ---: | ---: | ---: |
| Darwin arm64 | 299,576 | 310,000 | 3.36% |
| Linux arm64 | 268,248 | 310,000 | 13.47% |
| Combined | 567,824 | 620,000 | 8.42% |

The values are exact against the baseline run. No Native version bump or
replacement seed is warranted by this source-compatibility migration.

## Raw evidence

- [`darwin-arm64`](darwin-arm64) and [`linux-arm64`](linux-arm64) contain the
  candidate measurements, identities, environment, executable inspection,
  release response, attestations, and process evidence.
- [`setup-transition/darwin-arm64`](setup-transition/darwin-arm64) and
  [`setup-transition/linux-arm64`](setup-transition/linux-arm64) contain the
  candidate transition identities, checksums, stdout/stderr, and process
  evidence.
- [`baseline`](baseline) retains the complete same-toolchain baseline evidence
  with the same directory structure.
- [`combined-size.txt`](combined-size.txt) and
  [`baseline/combined-size.txt`](baseline/combined-size.txt) are exact.
- [`EVIDENCE_SHA256SUMS`](EVIDENCE_SHA256SUMS) covers every retained raw file
  and the migration inventory.

The candidate artifacts are GitHub artifact IDs 9755130583, 9755124308,
9755123933, 9755122438, and 9755122054. The baseline artifacts are IDs
9755305526, 9755299766, 9755299261, 9755294064, and 9755293752. Compiler
binaries are intentionally omitted from Git history; their sizes and SHA-256
identities are retained here.
