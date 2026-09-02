# Native MIR optimization transition status

Status: experimental, accepted through revision
`c958426eb4a778f9019120b0f540bc9590f7db85`.

The self-hosted compiler now derives and consumes two related portable
optimization decisions above the QBE adapter. During structured type checking,
it recognizes an exact mutable local initialized to literal zero and updated
only by a checked unit step. It also derives an active loop base plus a small
nonnegative literal and records that fact with an explicit dependency on its
enclosing verified loop. The facts live in dedicated, target-neutral checked-
program storage. Every checked Array-index postfix stores its exact fact origin.
The QBE Array-address adapter resolves that origin at the same postfix without
scanning source tokens or carrying range state through emitted expression
values, and omits only the impossible negative-index normalization.

These are compact derivation and consumption slices, not the completed shared-
MIR architecture. The general function/block/value MIR is not yet the ordinary
QBE input. General control/value lowering, a reusable expression-origin and
range representation, and replacement of the broader emitted-value
representation remain the next structural checkpoints. The former emitted-
value range-fact propagation is no longer part of that remaining work.

## Retained boundary

- literal-zero unit-step loops and their proven small nonnegative derived
  indices retain their previously accepted optimized QBE;
- reassignment, non-unit updates, conditional nesting that changes the local,
  and loop-external negative indexing retain the general path;
- invalidating an enclosing induction candidate also invalidates every nested
  fact that depends on it;
- focused positive and negative controls plus 24 current conformance, mutation,
  and benchmark programs remain byte-identical against accepted QBE;
- Darwin and Linux arm64 emit byte-identical target-neutral compiler QBE; and
- the complete Native gates, Linux amd64 and arm64 regressions, persistent-
  worker checks, fixed points, process boundaries, cleanup checks, and
  executable-stack policy pass.

The accepted static comparison records a 299,656-byte Darwin arm64 compiler, a
271,928-byte Linux arm64 compiler, and 571,584 bytes combined. The portable
compiler QBE decreases by 1,025 bytes to 955,189 bytes with SHA-256
`c8e9a392f5e6ca093c1508a3a9ece4f25cdcdc44057c1e5f0a2a5f0756ce9199`.
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
- [exact index-consumption issue #209](https://github.com/type-rb/type-rb-native/issues/209)
- [accepted pull request #210](https://github.com/type-rb/type-rb-native/pull/210)
- [static cross-target run](https://github.com/type-rb/type-rb-native/actions/runs/33636579318)
- [target regressions run](https://github.com/type-rb/type-rb-native/actions/runs/33636579388)
- [persistent-worker run](https://github.com/type-rb/type-rb-native/actions/runs/33636579344)
- [complete Native gates run](https://github.com/type-rb/type-rb-native/actions/runs/33636579379)
