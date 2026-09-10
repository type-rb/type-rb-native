# Numeric regression recovery

At accepted Native `bb262222279cb18741f8cfd47001020a276af25c`, the large
checked-assignment regressions in n-body and fannkuch-redux have been removed.
Fannkuch's generated program is byte-identical to the former published baseline;
n-body improves beyond that baseline. The spectral-norm guard improvement remains.
The historical proof below identifies that accepted recovery checkpoint. The
subsequent formal refresh and loop-local improvement are recorded separately
below; historical artifact identities are not relabelled as current source.

## Compare the right revisions

The [previous published snapshot](https://github.com/type-rb/type-rb-native/blob/5ad55a4b92070aad74e32933aded4888c553badc/docs/capabilities/benchmarks/data.js)
used Native `85e8d49bf256aed37332c68ef19cd7dea7afb977`, with one-core
Linux medians of 10.2644 seconds for n-body(50000000) and 77.1176 seconds for
fannkuch-redux(12). The later snapshot at `2841cb93` recorded 26.2869 and
202.325 seconds. Those cross-date numbers exposed the regression but cannot
attribute it on their own.

The [assignment-effect investigation](https://github.com/type-rb/type-rb-native/issues/354#issuecomment-5603477828)
compares generated artifacts as well as matched timings. The regressed n-body
and fannkuch programs match the original checked-assignment compiler
`90435186fc5c06b662c06cb80584575e28d9d064`. Conservative lowering added redundant
address validation/recalculation and temporary GC roots even for assignments
without relevant effects. The regression was present before the scalar guard
and the later MIR carrier reorganizations.

[PR #376](https://github.com/type-rb/type-rb-native/pull/376) uses verified MIR
assignment effects to remove that redundant work while retaining receiver/index
evaluation, pre-RHS failure ordering, reallocation safety and owner lifetime.
It restores both generated programs to pre-assignment source
`ac633935a7f248470c59d22666da14c819a131fa`; it does not revert safe assignment
semantics. [PR #379](https://github.com/type-rb/type-rb-native/pull/379) and
[PR #381](https://github.com/type-rb/type-rb-native/pull/381) then extend verified
stable-header reuse to local and multiple bindings, improving n-body further.
A subsequent description of fannkuch as unchanged refers to this already
restored program, not the slower 202.325-second snapshot.

## Direct verification against the former Pages source

[Issue #382](https://github.com/type-rb/type-rb-native/issues/382) closes the
remaining baseline-identity question. The exact former published compiler was
rebuilt through Native generations with QBE 1.3 and the same Darwin arm64 system
linker; the second and third same-basename compiler generations match. All three
benchmark source files are unchanged between the former and current revisions.

The former published source and pre-assignment cumulative source produce
identical complete QBE and application executable bytes for all three cases.
The current artifacts likewise match the exact candidates in the accepted local
comparison. This identity links the existing observations to the former source;
it is not a new timing cohort or a relabeling of those observations.

| Case | Former published QBE bytes | Current QBE bytes | Executable relationship |
| --- | ---: | ---: | --- |
| n-body | 66,802 | 65,544 | Improved current program; old program equals the measured cumulative control |
| fannkuch-redux | 52,507 | 52,507 | Entire executable byte-identical before and after |
| spectral-norm | 51,699 | 52,331 | Current guarded program retains the measured runtime gain |

The [accepted local full-input reassessment](https://github.com/type-rb/type-rb-native/issues/380#issuecomment-5604737714)
retains two warmups and eleven measured rotating rounds for three roles and
three cases. Its cumulative-control comparison is now tied to the exact former
published executable:

| Case / input | Former-equivalent control wall | Current wall | Current/control wall | Current/control CPU |
| --- | ---: | ---: | ---: | ---: |
| n-body / 50000000 | 5.051732 s | 3.674917 s | 0.727457 | 0.727804 |
| fannkuch-redux / 10 | 0.347810 s | 0.345888 s | 0.994474 | 0.996483 |
| spectral-norm / 5500 | 2.212641 s | 1.621309 s | 0.732748 | 0.730068 |

These are uncontrolled local Darwin measurements. Fannkuch's equal executable
identity applies to every input; its row here uses 10, whereas the old Linux
Pages row uses 12. All full published inputs (n-body 50000000, fannkuch 12,
spectral 5500) also pass a fresh untimed exact-output check on the current
programs. No local seconds are substituted for Linux Pages results and no new
Pure Go timing is claimed.

The earlier [short-input cohort](https://github.com/type-rb/type-rb-native/issues/380#issuecomment-5604644549)
failed its within-role wall outlier limit and remains failed, with every row
retained. The separately preregistered full-input reassessment passes its entire
contract. Both are preserved; neither is filtered or pooled with this identity
verification. The accepted compiler passes all 17 selected CI authorities and
unchanged compiler, build, memory and correctness limits.

## Subsequent loop-local improvement and formal refresh

[PR #389](https://github.com/type-rb/type-rb-native/pull/389) supplies the checked
loop-region proof needed for narrower header reuse. Its local fannkuch wall
ratio is 0.883322 against the already restored immediate control, while n-body
and spectral remain within their registered bounds. This is an additional
improvement, separate from the completed assignment regression repair above.

The [complete formal refresh](../results/2026-09-10-benchmarksgame-runtime-loop-local-headers-linux-arm64/README.md)
measures source `8980b597` and replaces the older regression snapshot in Pages.
One-core n-body is 7.87414 seconds and fannkuch is 61.8302 seconds, both below the
pre-regression published medians of 10.2644 and 77.1176. Spectral-norm is 2.25684
seconds versus Pure Go's 3.21985; the other two cases remain slower than Pure Go.
All observations are retained. Cross-date values confirm the refreshed published
state, while the local comparisons above provide separate causal evidence.
