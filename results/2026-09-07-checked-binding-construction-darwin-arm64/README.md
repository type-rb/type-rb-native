# Single-construction checked binding checkpoint

Status: **local build-cost prefilter passes** for
[issue #303](https://github.com/type-rb/type-rb-native/issues/303).
Full current-source recovery and hosted acceptance are still required. This is
not an accepted runtime result, Pure Go parity claim, or Pages authority.

Checked local reads now derive scalar category and loop operands before creating
one complete checked record. The duplicate scalar/non-scalar construction sites
and construction-then-copy path are removed. Type, capability, source origin,
scalar MIR state and loop identity remain independent. A 48-case regression
matrix covers their combinations, including opaque regions and absent scalar
values. No readonly binding is upgraded, and missing scalar metadata still
disables that scalar MIR path.

The exact compiler/test patch applies to
`691eb197bcb29a50c7d03e229094f06c9415acff`, including correction #306 and the
preceding unpublished-for-acceptance loop candidate. The frozen comparison
baseline remains `1afd60c2c7257ed34fd2a2aa70cb8b9164433009`.

| Ordinary build metric | Baseline median | Candidate median | Ratio |
| --- | ---: | ---: | ---: |
| Wall (s) | 1.516522292 | 1.588239042 | 1.0472902709 |
| CPU (s) | 1.499007 | 1.565954 | 1.0446608988 |
| Root RSS (bytes) | 40173568 | 40157184 | 0.9995921697 |

The unchanged [observer](../2026-09-06-mir-loop-bounds-diagnostic-darwin-arm64/build-cost-observer.py)
retains two warmups and seven interleaved observations per role. All 18 builds
reproduce their exact-source compiler, all three median ratios pass 1.05, and
every retained value for both roles passes the 2.0 catastrophic bound.
Small differences between separately measured candidates do not establish a
ranking or statistical significance; this is the first completed cost batch
for this source-distinct variant, not an unchanged acceptance retry.

B2/B3/B4 SHA256:
`646871f4b1d9c903c7503cee4a933f58547049f4a74c1c95eab2011e4e771796`.
Complete compiler: 349256 bytes; Mach-O text: 247992 bytes; target-neutral QBE:
1110446 bytes. The compiler suite passes 135 tests and the corpus passes all
75 cases at B2/B3/B4 (225 rows), including exact invalid diagnostics and no tool
execution/output publication for invalid source. Repeated/adjacent QBE is exact.
The three numeric benchmark QBE outputs equal the prior loop candidate's
outputs. Earlier runtime cohorts remain historical evidence, not a new timed
runtime claim for this checkpoint.

Separate untimed same-source checks report 251134607 allocated bytes for this
compiler versus 251147023 for the previous cab53295 compiler: only 12416 bytes
less. Peak managed heap increases slightly. Both report zero final live bytes
for that invocation; neither establishes general leak freedom. The factory
cleanup is not presented as a large allocation improvement.

Owned correctness batches finished before timing. Each compiler builds its own
canonical source with QBE 1.3, `/usr/bin/cc`, and `darwin-arm64-v0`; wall time is
monotonic and CPU/RSS use wait4 orchestration-root accounting. Host: Apple M2 Pro,
10 logical CPUs, 32 GiB RAM, macOS 26.6.2; Apple clang 21.0.0
(clang-2100.1.1.101). Reference revision:
`5dc09070cf7f88a569279f5e63982a6de59d692c`. Warm caches, no CPU affinity,
controlled frequency or host-wide isolation. The longer joined recovery suites
were started only after the measurement completed.

The manual `array-loop-bounds` runtime contract retains the registered full
schedule and frozen baseline. Its result, the same-head frozen-baseline
interleaved compiler comparison, and all normal PR authorities must pass before
this candidate can be accepted. No limit or transition marker changes.
