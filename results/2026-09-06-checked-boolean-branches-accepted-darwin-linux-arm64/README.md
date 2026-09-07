> Lifecycle: [complete source-era record](https://github.com/type-rb/type-rb-native/blob/bd483cfc5b51035d9fac193a74ee9d0eda2419ed/results/2026-09-06-checked-boolean-branches-accepted-darwin-linux-arm64/README.md).
> Historical checksum inventories refer to that full record, not this compact working set.

# Accepted Checked Boolean Branch Verification

[PR #291](https://github.com/type-rb/type-rb-native/pull/291) accepts candidate
`85e8d49bf256aed37332c68ef19cd7dea7afb977`, merged as
`d011df1991b730a68bb21eb852e31631ecdde970`. The registered Linux comparison
reduces spectral-norm wall time by about 7.46% and fannkuch-redux by about 9.02%
relative to the previous Native compiler. This is not a Pure Go comparison or
a replacement for the complete cross-language Pages snapshot.

## Scope and exact authorities

The change mechanically lowers already checked Boolean values without redundant
extension and comparisons to zero. It preserves short-circuiting, failure order,
non-Boolean comparisons and portable Integer checks. It adds no semantic analysis,
new MIR fact family or size allowance. Full MIR ownership migration remains due.

- Baseline: `6f7e3ba10623d40b5b0f7e6cc03b732125607795`.
- [Supplemental runtime run 34016548080](https://github.com/type-rb/type-rb-native/actions/runs/34016548080)
  measures the exact candidate head with the registered `checked-boolean-branches`
  contract, not a replacement for normal acceptance.
- [Normal run 34016545757](https://github.com/type-rb/type-rb-native/actions/runs/34016545757)
  passes current correctness, recovery, both Linux targets, memory, comparative
  cost and acceptance. Its PR merge checkout is
  `c2b0d8e70c40888dcc396ef6a01dcdc7073a0a35`, with parents `a41643b2` and
  `85e8d49b`; it differs from the candidate only in accepted development-skill
  instructions, not compiler, runtime, tests or measurement controllers.
- [Experimental CLI run 34016545717](https://github.com/type-rb/type-rb-native/actions/runs/34016545717)
  passes both arm64 hosts, including fixed points and CLI/REPL/project controls.

The pinned TypeRB reference is `0.4.4-dev@5dc09070cf7f88a569279f5e63982a6de59d692c`.
The immutable `bootstrap-seed-2026-08-30` release is setup provenance;
ordinary replacement generations use the previous Native compiler. QBE 1.3,
CC, assembler, linker and system libraries remain explicit external tools.

## Runtime comparison

BenchExec `runexec` 3.35 measures fresh, already-built processes on one logical
CPU of the Linux arm64 runner. Each case uses two warmup rounds and eleven
alternating retained rounds per role, unchanged isolation/cache policy, and
exact expected outputs. Compilation is not part of these application times.

Times are median seconds. Ratios divide candidate by baseline; lower is better.

| Case / input | Baseline wall | Candidate wall | Wall ratio | CPU ratio | Memory ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| spectral-norm / 5500 | 3.59727 | 3.32893 | 0.925404 | 0.925278 | 1.003356 |
| fannkuch-redux / 10 | 0.514586 | 0.468150 | 0.909760 | 0.909398 | 1.009524 |
| n-body / 1000000 | 0.212841 | 0.209100 | 0.982426 | 0.981884 | 1.000000 |

Ratios use unrounded retained values. All 78 observations, including 12 warmups,
pass. Independent checks verify complete rotating order, statuses, exact output,
clean measurement diagnostics, reproduced medians, the selected 0.98 spectral
limit, 1.02 control limits, 1.05 memory limit and every retained observation's
baseline-relative 2.0 catastrophic bound. The final temporary-file inventory is
empty. Lower CPU time and memory are not an energy measurement or a leak test.

## Compiler cost and correctness

| Target | Complete bytes, before → after | Text bytes, before → after | Build wall ratio | Build RSS ratio |
| --- | ---: | ---: | ---: | ---: |
| Darwin arm64 | 349224 → 332712 | 249804 → 233556 | 0.983834 | 0.997620 |
| Linux arm64 | 315144 → 298752 | 252192 → 235856 | 0.967213 | 1.001493 |

Combined complete compiler size falls from 664368 to 631464 bytes.
Target-neutral compiler QBE falls from 1122621 to 1055831 bytes, with SHA-256
`7714587dfc1e215cdfb69732ef236c70b6c5743af4a8c146ca848820960050d1`.
Both targets pass strict text/QBE shrinkage and complete-compiler non-growth,
ordinary build/RSS limits, existing absolute ceilings and catastrophic checks.
This does not authorize spending the recovered space on another fact family.

The normal recovery-enabled suites pass 90 root and 107 compiler tests.
Their whole-suite durations are 1078.134 and 207.727 seconds respectively;
these are correctness-suite observations, not isolated compiler benchmarks.
Current target regressions, process/cleanup/stack verification and allocation/
persistent-worker memory smoke pass. Long-running resource stability remains
a separate authority and ongoing scope.

## Retained failed attempt

[First supplemental run 34016344055](https://github.com/type-rb/type-rb-native/actions/runs/34016344055)
at `f694737b0512bbc896a0709f5ddcec9ecc20dfbf` closes both compiler chains but
fails before application measurements: a fresh compactness shell omitted
`compiler-project.sh` before loading the MIR policy. Its available evidence is
retained in `first-supplemental-premeasurement`, not counted as a runtime result.

The repair adds that dependency and a fresh-shell positive/negative regression.
All 22 controller tests and actionlint pass; compiler production SHA-256 remains
`fd7e19e9188e8a4d55177925033b9e35f94a9ac3e1d2c282246c5d3844174e2e`.
Runtime measurement code, inputs, baseline, samples and limits do not change.
The repaired head reruns the complete normal authority as well as the supplement.
The earlier local diagnostic and CSV-whitespace preflight history remain in
[the diagnostic record](https://github.com/type-rb/type-rb-native/blob/bd483cfc5b51035d9fac193a74ee9d0eda2419ed/results/2026-09-06-boolean-branches-diagnostic-darwin-arm64/README.md).

## Artifact integrity

All five original archive SHA-256 values were independently verified before
extraction. `EVIDENCE_SHA256SUMS` inventories 758 extracted files, excluding this
README and the inventory itself. Text copies normalize CRLF, trailing horizontal
whitespace and terminal blank lines; measurement values, sample order and binary
bytes are unchanged. Twelve retained binaries are benchmark applications, not
compiler seeds. Original archive identities distinguish these text copies.

| Directory | Artifact ID | Archive bytes | Original SHA-256 |
| --- | ---: | ---: | --- |
| accepted-runtime | 9984125221 | 440671 | `7140aa010eee563a877c5f9ddc1b77fa8c57378365a28ccda1fcc1e6df98c078` |
| darwin-arm64-cost | 9984444894 | 12074 | `5a357c61176d408afca6a9965e14b602a903894da40024f7d18c2d3dd47bdb4d` |
| linux-arm64-cost | 9984421018 | 18587 | `ed582c04700d4392d5475efb28d770408e5f54d3c5abdbbb9e871b1e169d4816` |
| cross-target-cost | 9984448553 | 424 | `ded7eb4b9311ebfaaa071acfd23c94fdf254c8c59b71c381ea118e69acba98f1` |
| first-supplemental-premeasurement | 9984030518 | 16916 | `afd8b870bfdd545390e4e5f40b23af4d73228e704bb797b32b514c38e697d673` |
