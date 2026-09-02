# Native MIR optimization transition status

Status: experimental, accepted through revision
`a9224bffcd6c28c9cf1dfce85ecb80c1ae096280`.

The self-hosted compiler now moves one existing portable optimization decision
above the QBE adapter. During structured type checking, it recognizes an exact
mutable local initialized to literal zero and updated only by a checked unit
step. It records the resulting nonnegative induction fact in dedicated,
target-neutral checked-program storage. The QBE Array-address adapter consumes
that fact without scanning source tokens and omits only the impossible
negative-index normalization.

This is the first ownership slice, not the completed shared-MIR architecture.
The general function/block/value MIR is not yet the ordinary QBE input. The
derived-index proof still has a lexical path, and the adapter temporarily maps
the checked fact onto the existing emitted-value nonnegative marker. General
control/value lowering, migration of the derived and nested-loop facts, and
removal of the temporary carrier remain the next structural checkpoint.

## Retained boundary

- literal-zero unit-step loops retain their previously accepted optimized QBE;
- reassignment, non-unit updates, conditional nesting that changes the local,
  and loop-external negative indexing retain the general path;
- the existing derived-index optimization remains byte-identical;
- seven focused positive and negative fixtures remain byte-identical against
  the accepted pre-transition QBE;
- Darwin and Linux arm64 emit byte-identical target-neutral compiler QBE; and
- the complete Native gates, Linux amd64 and arm64 regressions, persistent-
  worker checks, fixed points, process boundaries, cleanup checks, and
  executable-stack policy pass.

The accepted static comparison records a 299,656-byte Darwin arm64 compiler, a
271,944-byte Linux arm64 compiler, and 571,600 bytes combined. The portable
compiler QBE is 955,602 bytes with SHA-256
`3559b6d7675dc16eacfbe0ee072c993fc295e9cfcb2721c6877c3c05418550b0`.
The independent persistent-worker paths record 299,696 and 271,936-byte
compilers, 571,632 bytes combined. All values remain below the separately
registered 302,000, 272,000, and 574,000-byte temporary MIR ceilings.

Compared with the accepted pre-slice Linux compiler, the static artifact
retains 200 bytes of structural cost. This does not expand the temporary MIR
allowance: the complete portable range, index, and induction migration must
still recover that allowance before another portable fact family begins. The
final Go-competitive build-time, distribution-size, and generated-code goals
are unchanged.

Public evidence:

- [Decision 0028](decisions/0028-native-mir-optimization-boundary.md)
- [MIR foundation result](../results/2026-09-02-native-mir-foundation-linux-arm64/README.md)
- [ownership issue #201](https://github.com/type-rb/type-rb-native/issues/201)
- [accepted pull request #202](https://github.com/type-rb/type-rb-native/pull/202)
- [static cross-target run](https://github.com/type-rb/type-rb-native/actions/runs/33611741255)
- [target regressions run](https://github.com/type-rb/type-rb-native/actions/runs/33611741346)
- [persistent-worker run](https://github.com/type-rb/type-rb-native/actions/runs/33611741382)
- [complete Native gates run](https://github.com/type-rb/type-rb-native/actions/runs/33611741410)
