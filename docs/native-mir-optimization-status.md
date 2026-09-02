# Native MIR optimization transition status

Status: experimental. The scalar connection is accepted through revision
`1ec464ec3794b11945b3cc5333a7d9f7d2975619`; the first complete control-flow
connection is measured and under review in pull request #224.

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
index normalization without a token-side fact carrier. Calls, records, managed
values, nested loops, and unsupported helper shapes retain the accepted direct
path without partial MIR publication.

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

The accepted fixed compiler QBE is 1,022,022 bytes with SHA-256
`41e6092c341116fd17d390a1904d19a6d46e117626d6bfd7bc49ad0d14bc5832`.
The fixed compilers are 316,184 bytes on Darwin arm64 and 289,440 bytes on
Linux arm64, 605,624 bytes combined. These remain below the pre-registered
317,000, 290,000, and 607,000-byte temporary ceilings.

In the final exact-head comparison, Darwin compiler/build/RSS ratios are
1.055157/1.055882/1.000397 and Linux arm64 ratios are
1.065371/1.105263/1.001748. They remain below the one-time scalar-connection
limits of 1.07 compiler size, 1.15 build time, and 1.05 RSS. Later ordinary
changes return to the 1.05 compiler/build/RSS ratios; every retained
observation remains subject to the unchanged 2.0 catastrophic bound.

The control-flow candidate was measured before changing these limits. Its fixed
compilers are 332,696 Darwin arm64 bytes and 308,656 Linux arm64 bytes, 641,352
bytes combined. Linux amd64 is 268,008 bytes and needs no additional allowance.
Its fixed compiler QBE is 1,089,635 bytes with SHA-256
`a1b26e9ed6d40edf1a1da2cab4de7cd18847e2d0bbe7917b178887f929e38c30`.
Issue #225 freezes temporary ceilings of 334,000, 310,000, and 644,000 bytes for
Darwin arm64, Linux arm64, and their combined size. Only the exact
control-flow-marker transition may use 1.08 compiler-size and 1.25 build-time
ratios; its maximum measured build ratio is 1.233645. RSS, catastrophic,
fixed-point, application, process, cleanup, and target-neutral requirements do
not change.

The managed-runtime smoke records a 316,224-byte stripped Darwin compiler,
0.77-second runtime, zero final live managed bytes, and a 1,048,513-byte peak
managed heap. Independent persistent-worker checks pass on Darwin arm64 and
Linux arm64.

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
- [accepted pull request #220](https://github.com/type-rb/type-rb-native/pull/220)
- [final static comparison](https://github.com/type-rb/type-rb-native/actions/runs/33676174683)
- [Linux target regressions](https://github.com/type-rb/type-rb-native/actions/runs/33676174697)
- [persistent-worker checks](https://github.com/type-rb/type-rb-native/actions/runs/33676174785)
- [complete Native gates](https://github.com/type-rb/type-rb-native/actions/runs/33676174660)
