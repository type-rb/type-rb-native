# Native MIR optimization transition status

Status: experimental, accepted through revision
`1c5120841124405d88d85a0147406216cca8b30b`.

The ordinary self-hosted frontend now builds one compiler-owned Native MIR
module for selected immutable scalar-leaf functions and one exact
`Array<Integer>` induction helper. The structured checker stages typed values,
instructions, blocks, block parameters, and failure edges during its existing
traversal, publishes only complete functions, and verifies the complete module
before QBE emission.
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
block parameter now lowers directly to a QBE `phi`; the former induction
`alloc8`, header `loadl`, and backedge `storel` are absent. Calls, records,
managed values, nested loops, and unsupported helper shapes retain the accepted
direct path without partial MIR publication.

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

The accepted fixed compilers are 332,696 Darwin arm64 bytes and 308,592 Linux
arm64 bytes, 641,288 bytes combined. The QBE-phi recovery leaves the page-aligned
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
- [accepted pull request #220](https://github.com/type-rb/type-rb-native/pull/220)
- [final static comparison](https://github.com/type-rb/type-rb-native/actions/runs/33682830363)
- [Linux target regressions](https://github.com/type-rb/type-rb-native/actions/runs/33682830410)
- [persistent-worker checks](https://github.com/type-rb/type-rb-native/actions/runs/33682830450)
- [complete Native gates](https://github.com/type-rb/type-rb-native/actions/runs/33682830403)
- [induction-phi static comparison](https://github.com/type-rb/type-rb-native/actions/runs/33688825454)
- [induction-phi target regressions](https://github.com/type-rb/type-rb-native/actions/runs/33688825377)
- [induction-phi persistent-worker checks](https://github.com/type-rb/type-rb-native/actions/runs/33688825485)
- [induction-phi complete Native gates](https://github.com/type-rb/type-rb-native/actions/runs/33688825371)
