# Native MIR optimization transition status

Status: experimental, accepted through revision
`cfcb587550b21736173d25ffc3c05adb246fa592`.

The self-hosted compiler now moves two related portable optimization decisions
above the QBE adapter. During structured type checking, it recognizes an exact
mutable local initialized to literal zero and updated only by a checked unit
step. It also derives an active loop base plus a small nonnegative literal and
records that fact with an explicit dependency on its enclosing verified loop.
The facts live in dedicated, target-neutral checked-program storage. The QBE
Array-address adapter consumes the resolved chain without scanning source
tokens and omits only the impossible negative-index normalization.

These are compact ownership slices, not the completed shared-MIR architecture.
The general function/block/value MIR is not yet the ordinary QBE input, and the
adapter temporarily projects the resolved checked fact onto the existing
emitted-value nonnegative state. General control/value lowering, a reusable
expression-origin and range representation, and removal of that temporary
carrier remain the next structural checkpoints.

## Retained boundary

- literal-zero unit-step loops and their proven small nonnegative derived
  indices retain their previously accepted optimized QBE;
- reassignment, non-unit updates, conditional nesting that changes the local,
  and loop-external negative indexing retain the general path;
- invalidating an enclosing induction candidate also invalidates every nested
  fact that depends on it;
- nine focused positive and negative fixtures remain byte-identical against
  the accepted pre-transition QBE;
- Darwin and Linux arm64 emit byte-identical target-neutral compiler QBE; and
- the complete Native gates, Linux amd64 and arm64 regressions, persistent-
  worker checks, fixed points, process boundaries, cleanup checks, and
  executable-stack policy pass.

The accepted static comparison records a 299,656-byte Darwin arm64 compiler, a
271,928-byte Linux arm64 compiler, and 571,584 bytes combined. The portable
compiler QBE is 956,214 bytes with SHA-256
`f90ecf48bfb7a95a03b645130a6891de5b75b7af8ebfc0240996530821481bbd`.
The independent persistent-worker paths record 299,696 and 271,920-byte
compilers, 571,616 bytes combined. All values remain below the separately
registered 302,000, 272,000, and 574,000-byte temporary MIR ceilings.

Compared with the accepted pre-slice Linux compiler, the current static
artifact has recovered 16 bytes and retains 184 bytes of structural cost. This
does not expand the temporary MIR allowance: the complete portable range,
index, and induction migration must still recover that allowance before another
portable fact family begins. The final Go-competitive build-time,
distribution-size, and generated-code goals are unchanged.

Public evidence:

- [Decision 0028](decisions/0028-native-mir-optimization-boundary.md)
- [MIR foundation result](../results/2026-09-02-native-mir-foundation-linux-arm64/README.md)
- [ownership issue #201](https://github.com/type-rb/type-rb-native/issues/201)
- [accepted pull request #202](https://github.com/type-rb/type-rb-native/pull/202)
- [derived ownership issue #204](https://github.com/type-rb/type-rb-native/issues/204)
- [accepted pull request #205](https://github.com/type-rb/type-rb-native/pull/205)
- [static cross-target run](https://github.com/type-rb/type-rb-native/actions/runs/33628051038)
- [target regressions run](https://github.com/type-rb/type-rb-native/actions/runs/33628051031)
- [persistent-worker run](https://github.com/type-rb/type-rb-native/actions/runs/33628051237)
- [complete Native gates run](https://github.com/type-rb/type-rb-native/actions/runs/33628051075)
