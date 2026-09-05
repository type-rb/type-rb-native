# Native MIR optimization transition status

The stable-Array-header work is not accepted: the first candidate failed
independent proof validation and three bounds checks; the `69ff52b5`
correctness repair subsequently improved spectral-norm by 11.978% on Linux
arm64 but regressed n-body by 13.161%. See
[the proof and control repair](native-mir-array-region-repair.md).
Neither candidate may replace the accepted benchmark snapshot.
The current repair retains access checks and narrows the new proof to immutable
Array parameters. Shared header loads, MIR parameter registration, and common
value/instruction builders remove duplicate implementation. Restoring the
two-entry recent-header fallback recovers exact baseline n-body output code,
while function-owned MIR instruction transfer avoids redundant row copies.
The local compiler fits the unchanged executable, code-section, and QBE
ceilings. PR #246 is ready for full correctness, target, memory, and formal
comparative verification; this local eligibility is not accepted performance
evidence.

Status: experimental. The checked-in scope includes the accepted induction-phi
recovery, the measured `Array<Integer>` reduction slice from issue #230, the
first target-independent optimization pass registered by issue #232, and the
exact `Array<Float>` reduction extension registered by issue #235. Issue #238
now also selects a target-independent guarded fast path for checked Integer
multiplication while retaining the exact helper fallback, and issue #241
applies the same verified decision boundary to checked Integer addition.

The ordinary self-hosted frontend now builds one compiler-owned Native MIR
module for selected immutable scalar-leaf functions and one exact
`Array<Integer>` induction/reduction helper family plus its zero-initialized
`Array<Float>` reduction counterpart. The structured checker
stages typed values, instructions, blocks, block parameters, and failure edges
during its existing traversal, publishes only complete functions, and verifies
the complete module before QBE emission.
The verified subset covers `Integer`, `Float`, and `Boolean` parameters and
results, exact scalar literals, unary operations, numeric and comparison binary
operations, checked Integer failure edges, and Integer-to-Float conversion.

Both ordinary function emission and bounded loop-local inlining consume these
verified rows. Exact call arguments bind their checked literal facts before
entering the MIR adapter. The adapter assigns QBE temporaries and uses the
existing ABI, but it no longer scans a scalar function body or parses an
emitted operand to recover the selected TypeRB semantics. The former
token-body eligibility scan and token-driven scalar-leaf emitter have been
removed.

This is an ordinary frontend-to-MIR replacement boundary, not complete compiler
lowering. The selected helper carries entry, loop header, body, backedge, exit,
checked-Integer failure, and Array-bounds failure through verified MIR. Its
canonical zero-origin/unit-step induction proof authorizes omission of negative
index normalization without a token-side fact carrier. Its verified header
block parameters lower directly to QBE `phi` instructions for both the index
and reduction accumulator. The former induction and accumulator `alloc8`,
`loadl`, and `storel` traffic is absent. The new pass marks only a
verifier-proven complete induction plan. The QBE adapter then hoists the
immutable Array length and data pointer, consumes the header's true edge
instead of repeating the bounds branch, and emits the unit-step induction
update without a redundant Integer-range branch. Checked accumulator addition
retains its explicit Integer failure edge; the Float reduction lowers a typed
Float phi, load, addition, and store without changing binary64 semantics.
Calls, records, managed values,
nested loops, and unsupported helper shapes retain the accepted direct path
without partial MIR publication.

## Retained boundary

- selected scalar leaves produce the accepted QBE for ordinary calls and
  inlining while their semantics come only from verified Native MIR;
- unsupported candidates retain the direct path without a second analyzer or
  partial MIR publication;
- forged literal facts, value identities, types, origins, failure targets, and
  operation shapes are rejected deterministically;
- checked Integer overflow, Float behavior, Boolean results, diagnostics,
  source order, and evaluation order remain unchanged;
- adjacent self-hosted generations emit byte-identical target-neutral compiler
  QBE on Darwin arm64 and Linux arm64; and
- the complete Native suite, Linux amd64 and arm64 regressions, process and
  cleanup boundaries, executable-stack policy, persistent-worker memory, and
  managed-runtime allocation smoke pass.

## Measured transition envelope

The induction-phi recovery fixed compilers are 332,696 Darwin arm64 bytes and
308,592 Linux arm64 bytes, 641,288 bytes combined. It leaves the page-aligned
Darwin artifact unchanged, reduces the Linux artifact by 64 bytes, and reduces
the same-run Mach-O `__text` section from 243,648 to 243,568 bytes and ELF
`.text` section from 246,240 to 246,144 bytes. The target-neutral fixed compiler
QBE decreases from 1,089,635 to 1,089,474 bytes with SHA-256
`575cb66c6b894650a2c89f9d5bb1abd9b11d1ec919ab89acecca88c532566979`.
Linux amd64 remains below its unchanged ceiling.
Issue #225 freezes temporary ceilings of 334,000, 310,000, and 644,000 bytes for
Darwin arm64, Linux arm64, and their combined size. Only the exact
control-flow-marker transition may use 1.08 compiler-size and 1.25 build-time
ratios. The final exact-head comparison records Darwin compiler/build/RSS
ratios of 1.052223/1.067669/1.000199 and Linux arm64 ratios of
1.066390/1.076923/0.999461. They pass the registered transition limits. Later
ordinary changes return to the 1.05 compiler/build/RSS ratios; every retained
observation remains subject to the unchanged 2.0 catastrophic bound.

Issue #230 then measures the accepted compact two-phi reduction candidate at
349,224 Darwin arm64 bytes and 314,544 Linux arm64 bytes, 663,768 bytes
combined. Its Mach-O `__text` and ELF `.text` sections are 249,488 and 252,032
bytes. Both targets emit byte-identical target-neutral compiler QBE of
1,112,077 bytes with
SHA-256
`8067fe279941819eb7b3a788cbb0fee9ec33e8e8c1aaec0e6a53f7bc43d36207`.
The checked-in marker freezes ceilings of 350,000, 317,000, 667,000, and
1,120,000 bytes respectively. It grants no relative-ratio exception: the
ordinary 1.05 compiler/build/RSS limits and 2.0 catastrophic bound remain in
force.

Issue #232 registers the first explicit optimization pass over this verified
graph. The compact local Darwin arm64 fixed compiler remains 349,224 bytes.
After removing the adapter's redundant reads of verifier-proven canonical
zero and unit values, the compiler itself removes 1,377 bytes of
target-neutral QBE and 208 bytes of compiler `__text`; the selected generated
workload removes another 335 bytes of QBE and 72 bytes of `__text`. On 21 alternating
retained direct-process observations, the selected workload records
candidate/baseline ratios of 0.599452 wall time, 0.561763 CPU time, and
0.992754 peak RSS. Formal CI requires both arm64 compilers to remain
non-growing, generated QBE and both generated code sections to shrink
strictly, wall and CPU ratios to remain at most 0.75, and RSS to remain at most
1.05. The broader temporary MIR envelope remains subject to the existing
range/index/induction recovery obligation; this pass adds no new allowance.

Issue #235 extends that same graph to one exact `Array<Float>` sum without a
new fact family or a larger envelope. The accepted fixed compiler remains
349,224 bytes on Darwin arm64 and shrinks from 314,336 to 314,280 bytes on
Linux arm64. Compiler code sections shrink from 249,280 to 249,172 bytes and
from 251,824 to 251,792 bytes respectively. Both targets emit byte-identical
1,110,817-byte compiler QBE, 117 bytes above the accepted baseline and below
the unchanged 1,115,000-byte limit. Each focused workload removes 614 bytes of
generated QBE; generated code shrinks by 88 Darwin and 80 Linux bytes. The
hot-small-Array wall/CPU ratios are 0.450223/0.448325 on Darwin and
0.427436/0.426565 on Linux. The equal-visit streaming ratios are
0.746350/0.746166 and 0.385098/0.383475. Median RSS is unchanged for every
workload and target. This distinction is intentional: it exposes the recovered
per-element control cost without hiding the smaller gain when memory traffic
dominates. The frozen 0.75 hot, 0.90 streaming, 1.05 RSS, and 2.0 catastrophic
bounds all pass.

Issue #238 adds the first checked scalar-arithmetic fast path selected in
Native MIR. When both operands fit the verified nonnegative 26-bit guard, the
QBE adapter emits a direct multiplication; negative, large, and overflowing
operands retain the exact checked helper and failure edge. On Linux arm64,
spectral-norm at input 5500 records candidate/baseline ratios of 0.846622 wall
time, 0.846633 CPU time, and 0.999619 median peak RSS across two warmups and
seven alternating retained observations. The two control workloads remain
effectively unchanged and emit byte-identical generated QBE and executable
text. Spectral-norm grows by 248 bytes of target-neutral QBE and by 64 bytes of
executable text on both arm64 targets. The fixed compiler instead shrinks by
384 bytes on Linux arm64, remains page-size neutral on Darwin arm64, and emits
1,109,629 bytes of byte-identical target-neutral compiler QBE across both
targets. All registered runtime, RSS, fixed-point, build, compactness,
cross-target, and catastrophic limits pass.

Issue #241 adds a checked Integer-add fast path without assuming benchmark-only
operand values. Portable Integer operands cannot overflow native signed 64-bit
addition, so the selected MIR operation computes the sum once and accepts it
when an unsigned result check proves it remains below `2^53`; negative or
out-of-range results retain the exact checked helper and failure behavior. On
Linux arm64, `spectral-norm` at input 5500 records candidate/baseline ratios of
0.932780 wall time, 0.932749 CPU time, and 1.000000 median peak RSS across two
warmups and seven alternating retained observations. `fannkuch-redux` and
`n-body` controls remain within 0.999964--1.000891 wall and
0.999974--1.000890 CPU ratios. The fixed compiler shrinks from 313,896 to
313,224 bytes on Linux arm64 and from 349,224 to 349,208 bytes on Darwin arm64;
both targets emit byte-identical 1,108,565-byte compiler QBE. The selected
application shrinks by 177 QBE bytes and 128 executable bytes while its Linux
code section grows by 64 bytes, remaining within the frozen 1.02 limit. Every
registered runtime, RSS, control, compactness, fixed-point, cross-target,
conformance, and process boundary passes without changing a threshold.

The earlier managed-runtime smoke records a 332,736-byte stripped Darwin
compiler, 0.70-second runtime, zero final live managed bytes, and a
1,048,513-byte peak managed heap. Current persistent-worker checks record
332,736 and 308,584 stripped compiler bytes on Darwin and Linux arm64, reclaim
all 182,400,576 allocated bytes, finish at zero live managed bytes with a
1,047,808-byte peak managed heap, and share identical target-neutral workload
QBE.

The temporary MIR allowance is migration space, not a new final size target.
It must be recovered by deleting superseded direct-emitter ownership by the end
of portable range, index, and induction migration. The final Go-competitive
build-time and generated-artifact objectives and the Pure Go-or-better
generated-program runtime objective remain unchanged.

Public evidence:

- [Decision 0028](decisions/0028-native-mir-optimization-boundary.md)
- [scalar connection issue #218](https://github.com/type-rb/type-rb-native/issues/218)
- [measured envelope issue #221](https://github.com/type-rb/type-rb-native/issues/221)
- [control-flow transition issue #223](https://github.com/type-rb/type-rb-native/issues/223)
- [control-flow envelope issue #225](https://github.com/type-rb/type-rb-native/issues/225)
- [control-flow pull request #224](https://github.com/type-rb/type-rb-native/pull/224)
- [induction-phi recovery issue #227](https://github.com/type-rb/type-rb-native/issues/227)
- [induction-phi pull request #228](https://github.com/type-rb/type-rb-native/pull/228)
- [Array reduction issue #230](https://github.com/type-rb/type-rb-native/issues/230)
- [Array reduction pull request #231](https://github.com/type-rb/type-rb-native/pull/231)
- [Array-loop recovery issue #232](https://github.com/type-rb/type-rb-native/issues/232)
- [Float Array-reduction issue #235](https://github.com/type-rb/type-rb-native/issues/235)
- [Float Array-reduction pull request #236](https://github.com/type-rb/type-rb-native/pull/236)
- [Float Array-reduction static and focused-runtime evidence](https://github.com/type-rb/type-rb-native/actions/runs/33717461388)
- [Float Array-reduction target regressions](https://github.com/type-rb/type-rb-native/actions/runs/33717461392)
- [Float Array-reduction persistent-memory checks](https://github.com/type-rb/type-rb-native/actions/runs/33717461375)
- [Float Array-reduction complete Native gates](https://github.com/type-rb/type-rb-native/actions/runs/33717461364)
- [guarded Integer multiply issue #238](https://github.com/type-rb/type-rb-native/issues/238)
- [guarded Integer multiply pull request #239](https://github.com/type-rb/type-rb-native/pull/239)
- [guarded Integer multiply focused evidence](https://github.com/type-rb/type-rb-native/actions/runs/33726990585)
- [guarded Integer multiply target regressions](https://github.com/type-rb/type-rb-native/actions/runs/33726990510)
- [guarded Integer multiply persistent-memory checks](https://github.com/type-rb/type-rb-native/actions/runs/33726990515)
- [guarded Integer multiply complete Native gates](https://github.com/type-rb/type-rb-native/actions/runs/33726990493)
- [guarded Integer add issue #241](https://github.com/type-rb/type-rb-native/issues/241)
- [guarded Integer add pull request #242](https://github.com/type-rb/type-rb-native/pull/242)
- [guarded Integer add static and focused-runtime evidence](https://github.com/type-rb/type-rb-native/actions/runs/33749003298)
- [guarded Integer add target regressions](https://github.com/type-rb/type-rb-native/actions/runs/33749003348)
- [guarded Integer add persistent-memory checks](https://github.com/type-rb/type-rb-native/actions/runs/33749003544)
- [guarded Integer add complete Native gates](https://github.com/type-rb/type-rb-native/actions/runs/33749003526)
- [accepted pull request #220](https://github.com/type-rb/type-rb-native/pull/220)
- [final static comparison](https://github.com/type-rb/type-rb-native/actions/runs/33682830363)
- [Linux target regressions](https://github.com/type-rb/type-rb-native/actions/runs/33682830410)
- [persistent-worker checks](https://github.com/type-rb/type-rb-native/actions/runs/33682830450)
- [complete Native gates](https://github.com/type-rb/type-rb-native/actions/runs/33682830403)
- [induction-phi static comparison](https://github.com/type-rb/type-rb-native/actions/runs/33688825454)
- [induction-phi target regressions](https://github.com/type-rb/type-rb-native/actions/runs/33688825377)
- [induction-phi persistent-worker checks](https://github.com/type-rb/type-rb-native/actions/runs/33688825485)
- [induction-phi complete Native gates](https://github.com/type-rb/type-rb-native/actions/runs/33688825371)
- [Array reduction static comparison](https://github.com/type-rb/type-rb-native/actions/runs/33697599532)
- [Array reduction target regressions](https://github.com/type-rb/type-rb-native/actions/runs/33697599529)
- [Array reduction persistent-worker checks](https://github.com/type-rb/type-rb-native/actions/runs/33697599556)
- [Array reduction complete Native gates](https://github.com/type-rb/type-rb-native/actions/runs/33697599531)
- [current complete formal runtime result](../results/2026-09-03-benchmarksgame-runtime-native-mir-guarded-multiply-linux-arm64/README.md)
- [current complete formal build result](../results/2026-09-03-benchmarksgame-build-native-mir-guarded-multiply-linux-arm64/README.md)
