# Accepted scalar Integer range guards

[PR #372](https://github.com/type-rb/type-rb-native/pull/372) adds bounded scalar
range proofs to MIR. One guard covers a region of Integer arithmetic; other
inputs retain the original checked operations and evaluation order. This is a
general scalar optimization with no benchmark names, inputs or source-text
recognition in the compiler.

The measured source is `2841cb9311fd0e3e4a6a84e5157745590dbc5765`, merged as
`a604adcffe0cc34ff217ff84d73911c85ceb0a00` with an identical tree. The local
runtime cohort used the first candidate `854d79ec`; after its recovery fix,
all three generated application QBE files and executables remain byte-identical.
No replacement local timing was taken. Compiler identity changes are retained
separately from application identity.

## Correctness and compiler costs

All 17 selected authorities pass in [CI run 34329271544](https://github.com/type-rb/type-rb-native/actions/runs/34329271544).
This includes root/compiler recovery suites, all 13 recovery stages, ordinary
fixed points, CLI/REPL and terminal controls, language coverage, reference
compatibility, Linux arm64/amd64 targets, target-neutral QBE, persistent-worker
memory and both platform compiler comparisons. Local recovery-enabled suites
also pass all 102 root and 149 compiler tests, with 24 focused MIR tests,
five Native proof/decoder groups and 435 corpus observations. Correctness-suite
durations are not performance measurements.

CI's merge-ref `7d2e1bf2a2771469d8df0969cde1309adecb57b3` has the same tree as
the candidate: `d92b858edd7a2e1058bf63a4434c0cddf4bf8f62`. Target recipes retain
older gate baselines in their metadata; adjacent-generation rows are not a
comparison with that historic source. The actual same-feature source control
for this change is `5cb44a7ad8d0802368a2fbdf4c433e0c5acf5c16`.

| Compiler cost | Darwin arm64 baseline | Candidate | Linux arm64 baseline | Candidate |
| --- | ---: | ---: | ---: | ---: |
| Executable bytes | 349272 | 365784 | 323280 | 329680 |
| Text bytes | 256560 | 262808 | 259168 | 265440 |
| Interleaved build wall median, seconds | 1.835 | 1.845 | 1.340 | 1.345 |
| Interleaved build peak RSS median, bytes | 41238528 | 41213952 | 64620544 | 64733184 |

All ordinary 1.05 comparison bounds pass. Combined executable size is 695464
bytes under the independently accepted 697000-byte ceiling. Linux uses 329680
of its 331000-byte ceiling; Darwin's 366000-byte ceiling is unchanged.
[PR #373](https://github.com/type-rb/type-rb-native/pull/373) and
[Decision 0031](../../docs/decisions/0031-scalar-guard-compiler-budget.md)
record the bounded size trade separately. Build/RSS ratios, catastrophic bounds,
application limits and all other authorities were not relaxed.

The 1170832-byte target-neutral compiler QBE has SHA-256
`d9ba3ab9ad8cfae846e212f43908fa8b722f986811089fc3fbd4099403193495`.
Darwin's compiler SHA-256 is
`510f43dcae2765cc470a4a8d7cc0ba6a7a4b0237730cd832345891a95da20d95`;
Linux's is `52d92576f5f1601f332eeb4b95bd8585797af1f5d9aa2311fd04f7d8d0760524`.
Compiler and application costs remain separate.

## Interleaved local application comparison

The Apple M2 Pro / macOS 26.6.2 preflight has two warmup and seven retained
rotating rounds for each of three roles and three cases: 18 warmups and 63
retained observations. `local-raw.json` preserves all 81 observations, outputs'
digests, status, CPU, wall and RSS metrics. `local-context.json` and
`local-identities.json` record commands, inputs, platform and artifact hashes.
This uncontrolled-host preflight measures already-built fresh processes with
`wait4`; it is not a formal Linux result or a comparison with Pure Go.

| Case and input | Immediate control wall | Candidate wall | Candidate/control wall | Candidate/control CPU | Candidate/cumulative wall |
| --- | ---: | ---: | ---: | ---: | ---: |
| spectral-norm 5500 | 2.219038541 | 1.622029 | 0.730960 | 0.728420 | 0.731911 |
| n-body 1000000 | 0.319844583 | 0.320218708 | 1.001170 | 0.999369 | 2.809720 |
| fannkuch-redux 10 | 0.800297375 | 0.795223875 | 0.993660 | 0.994938 | 2.244872 |

The registered spectral improvement, control, RSS and catastrophic criteria
pass. The frozen cumulative source remains
`ac633935a7f248470c59d22666da14c819a131fa`; its Darwin compiler is 349240 bytes.
The current 365784-byte compiler is 4.737% larger than that compiler. The large
cumulative n-body and fannkuch regressions remain present in the immediate
control; this scalar guard does not fix them or justify compounding allowances.
[Issue #354](https://github.com/type-rb/type-rb-native/issues/354) tracks the
Array/effect investigation. No general runtime parity is claimed.

## Rejected attempts and recovery

The first candidate's local runtime benefit did not make it acceptable.
[CI run 34326478178](https://github.com/type-rb/type-rb-native/actions/runs/34326478178)
failed because snapshot recovery did not support its String conversion and
Linux's 330496-byte compiler exceeded the then-current 328000-byte ceiling.
Some authorities were skipped; they are not passing evidence.
Initial formal runtime/build runs 34326755971 and 34326758994 were canceled
after bootstrap failures. Every measurement step was skipped, so they contain
no runtime or build observations and are not discarded outliers.

The corrected implementation uses named interval records and a strict decimal
decoder composed of recovery-supported operations. A second attempt to merge
emitter control flow grew text by 632 bytes and was discarded. Failed test
observer setup used an unsupported conversion, a duplicate local and an unused
import; these were corrected before the relevant successful observations.
All cohort decisions and the corrected registration remain in
[issue #371](https://github.com/type-rb/type-rb-native/issues/371).

## Complete published cohort

The [formal runtime result](../2026-09-09-benchmarksgame-runtime-scalar-range-guards-linux-arm64/README.md)
and [formal build result](../2026-09-09-benchmarksgame-build-scalar-range-guards-linux-arm64/README.md)
retain the full current schedules and distribution boundaries. Their exact
measured compiler is not relabelled after later source changes. The previous
accepted checkpoint remains at its
[historical revision](https://github.com/type-rb/type-rb-native/blob/a604adcffe0cc34ff217ff84d73911c85ceb0a00/results/2026-09-06-checked-boolean-branches-accepted-darwin-linux-arm64/README.md).


## Subsequent Integer-literal verifier correction

A generic malformed-MIR probe found that the old length/range helper could
accept `"x"` with a zero operand fact when no scalar guard was admitted.
The range proof itself rejected it. [PR #375](https://github.com/type-rb/type-rb-native/pull/375)
reuses the strict decimal decoder at the verifier boundary and adds nine
malformed spelling regressions without changing source-language syntax.

Source `bffd4efd9a7ceb381658b8bbb000f7a62954d6ae`, merged as `c986f5e6`, passes
all 16 selected CI authorities; the unselected documentation job is explicitly
skipped. Local recovery-enabled suites pass 102 root and 150 compiler tests,
all 13 stages complete, and owned cleanup succeeds. The six focused tests and
Native-executed rejection probe pass. `verifier-correction.json` retains the
source identities, complete authority outcomes, raw interleaved cost rows and
application equivalence report.

The corrected Darwin compiler remains 365784 bytes with a distinct SHA-256
`eb3c65153450f119df512b4d207ec818081b15664def5e383c80a06959b5ae1e`.
All three Darwin benchmark QBE files and executables are byte-identical to
the measured candidate and produce the exact expected outputs. This check
contains no replacement timing. Formal runtime/build tables continue to
identify their actual `2841cb93` compiler rather than relabelling it as this
later verifier correction.

## Subsequent checked-assignment effect regions

[PR #376](https://github.com/type-rb/type-rb-native/pull/376), source
`bbfb7a472108ef215ad7b7a575592c5dfe563319`, merged as `ade252f7`, subsequently
derives address reuse and owner-root lifetimes from a checked MIR assignment
region. Effectful index/RHS paths preserve the existing semantics. This is
not part of the `2841cb93` formal cohort above.

All 17 selected authorities pass in [CI run 34346760731](https://github.com/type-rb/type-rb-native/actions/runs/34346760731).
The initial Linux memory job failed before measurement on a GitHub seed-asset
HTTP 500; its retry and dependent authorities then passed. The initial draft
feedback run intentionally skipped merge authorities. Local corrected suites
pass 102 root and 155 compiler tests, all 13 recovery stages and owned cleanup.

The separately preregistered local 81-observation comparison reports wall
ratios of 0.348266 for n-body, 0.433188 for fannkuch and 0.999850 for spectral
against the immediate `c986f5e6` control. N-body/fannkuch QBE and executables
match the frozen cumulative control exactly and their local performance returns
to that baseline. These are not replacement Linux measurements or new Pure Go
claims. The linked PR reports the bounded conclusions and validation; the
[complete local records](https://github.com/type-rb/type-rb-native/issues/354#issuecomment-5603477828)
retain all observations, context, identities and acceptance criteria.

CI compiler sizes are 349272 bytes on Darwin and 323896 on Linux, combined
673168 under the unchanged 697000-byte ceiling. Build and peak-RSS ratios
remain below 1.05. Target-neutral compiler QBE is 1159329 bytes, SHA-256
`9fea06cb77abc2fc60075bf367914969ad385d83d56edf8f89cb92630137d09b`.
