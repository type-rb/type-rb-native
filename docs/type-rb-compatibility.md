# TypeRB Compatibility

TypeRB Native follows exact reference revisions while it is experimental. The
current source and semantic oracle is TypeRB
`caf6aadb9493ca69290ab0dc22d420b5f574df14` (`0.4.6-dev`), recorded in
`TYPE_RB_REVISION`. This is an exact development pin, not a supported version
range.

The machine-readable
[`compatibility/current.json`](../compatibility/current.json) records this
exact mapping beside the independent Native `0.1.0-dev` implementation
identity. Its strict schema and CI validation keep TypeRB, bootstrap, MIR,
runtime ABI, backend, target, and evidence identities separate. The current
target list contains the experimental Darwin arm64 and Linux arm64 seed
profiles plus the independently recovered and verified experimental Linux
amd64 profile. See
[Native versioning and compatibility](versioning.md) for bump and release
rules.

The declaration-import compatibility work was registered in
[issue #97](https://github.com/type-rb/type-rb-native/issues/97). Its
[Darwin/Linux arm64 result](https://github.com/type-rb/type-rb-native/blob/bd483cfc5b51035d9fac193a74ee9d0eda2419ed/results/2026-08-30-typerb-0-4-compatibility-darwin-linux-arm64/README.md)
passes the selected `0.4.1-dev` reference, previous-seed, exact fixed-point,
process, elapsed-time, peak-RSS, and compiler-size criteria. The `0.4.3-dev`
successor is registered in
[issue #106](https://github.com/type-rb/type-rb-native/issues/106), and its
[Darwin/Linux arm64 result](https://github.com/type-rb/type-rb-native/blob/bd483cfc5b51035d9fac193a74ee9d0eda2419ed/results/2026-08-30-typerb-0-4-3-compatibility-darwin-linux-arm64/README.md)
passes the selected-reference, explicit setup-transition, exact fixed-point,
process, elapsed-time, peak-RSS, and compiler-size criteria. This document
records the implementation boundary independently of those measurements.
The earlier scoped-file successor is registered in
[issue #144](https://github.com/type-rb/type-rb-native/issues/144), and its
[Darwin/Linux arm64 result](https://github.com/type-rb/type-rb-native/blob/5cf61c740aa600c34ed94f1b130ea2ffefd9e783/results/2026-08-31-typerb-0-4-4-compatibility-darwin-linux-arm64/README.md)
passes the selected-reference, migration, exact-baseline, target-regression,
fixed-point, process, resource, and size criteria.

## Stable Array assignment targets

The current pin includes [TypeRB PR #659](https://github.com/type-rb/type-rb/pull/659).
Indexed assignment retains the evaluated Array and validated nonnegative
position before the RHS, then validates that position in current storage at
the final store. Compound assignment uses the old value saved before the RHS.
The checked source projection pairs Array target and store origins; its
verified plan directs owner retention, position capture and final address
resolution. Its tagged slot holds either a binding address or a validated
Array position beside the owner; checked mutability is not copied into
emitter metadata. The adapter no longer writes an element address held across RHS
calls. Managed owners and saved compound values remain rooted across calls.

The ordinary fixtures cover growth, aliasing, index-side mutation, nested owner
replacement, managed old values and initial bounds failure. The separate
`array-assignment-recovery` case verifies the same rule through snapshot v4.
Boolean Arrays and short-circuit assignment syntax remain outside the current
ordinary subset; this change does not add source forms or collection methods.

Validation and acceptance for this correctness slice follow
[issue #342](https://github.com/type-rb/type-rb-native/issues/342), including
full recovery suites, ordinary regeneration, conformance, GC and unchanged
compiler/application cost gates. Reference pinning alone is not acceptance.

## Loop-transfer snapshot update

The current pin includes [TypeRB PR #657](https://github.com/type-rb/type-rb/pull/657).
Snapshot v3/v4 now encode `break`, `next` and early method returns in `while`
with existing jumps and block arguments. The `loop-transfer-recovery` fixture
checks live managed bindings, nested targets, condition effects and returns
through v4 program decoding, recovery QBE generation and execution. The format,
v2 boundary and ordinary language semantics remain unchanged.

The reference update accompanies the separately registered loop-transfer seed
refresh and exact Linux amd64 setup source bridge. Neither registration nor
pinning replaces full acceptance or post-publication seed verification.

## Statement conditional snapshot update

The current pin includes [TypeRB PR #655](https://github.com/type-rb/type-rb/pull/655).
It encodes statement `elsif` with existing v3/v4 branches, jumps and block
parameters, preserving ordered conditions, lexical scopes and terminating
branches. It does not expand conditional expressions or the v2 snapshot subset.
The `elsif-recovery` fixture now runs through v4 encoding, strict decoding,
recovery QBE emission and execution as well as current ordinary generations.

This pin is a prerequisite for compiler-source self-use. Complete recovery,
ordinary fixed points, target, memory and cost acceptance remain required;
updating a reference pin does not replace a verified checkout seed.

## String escape reference update

The pin also includes the portable String escape fix in
[TypeRB PR #651](https://github.com/type-rb/type-rb/pull/651). Merge that
reference PR before this dependent update. Double-quoted source accepts `\#`
as a literal hash, respects backslash parity before interpolation, and rejects
unknown escapes. JSON history data retains its separate JSON escape rules.

Moving the oracle to `0.4.6-dev` also requires typed `Path` arguments in the
repository-owned file adapter and immutable record fields in the CLI. Mutable
editor cells use Arrays; session transitions return replacement records.
These changes preserve the portable rules without adding reference aliases.
The [current validation record](../results/2026-09-07-string-escape-reference-compatibility/README.md)
separates local reference checks from hosted Native CLI and fixed-point checks.
The PR's full recovery, target, memory and performance authorities remain
required before acceptance. Earlier measurements below retain their original
revisions and do not establish performance at the new pin.

## TypeRB 0.4.4 source compatibility revalidation

The selected revision contains the TypeRB 0.4.3 release, the advance to
`0.4.4-dev`, receiver-only canonical built-in ownership, scoped file and
directory APIs, repeated scalar CLI options, corrected safe-navigation
evaluation, CLI application failures, and a focused undeclared-value
diagnostic correction.

Native does not currently use the changed CLI or safe-navigation surfaces. Its
direct source break was removal of `trb/std/filesystem`. All 39 affected root,
compiler-test, and historical benchmark-controller sources now use identical
repository-owned support. Reads are scoped and bounded to 67,108,864 bytes by
default, writes use `FileMode::Write`, and recursive test-directory creation
invokes exact `/bin/mkdir -p` through shell-free `Process.run`. This support is
not imported by the canonical self-hosted compiler closure and does not add a
Native compatibility alias to TypeRB.

The selected formatter and checker pass every checked-in configured project.
Executable tests cover successful and oversized bounded reads, truncating
writes, recursive and idempotent directory creation, and deterministic failure
fields. Existing Linux amd64 and arm64 regressions retain exact target-neutral
QBE. The Darwin and Linux arm64 previous-Native chains produce compiler and QBE
identities that are byte-identical to the registered Native baseline.

## TypeRB 0.4.3 semantic revalidation

The selected revision includes the TypeRB 0.4.1 and 0.4.2 releases, owner-
qualified Web API changes outside the current self-hosted subset, shared Array
alias fixes in the Go backend, nested Go runtime-helper propagation, and the
distinction between Nil values and Void results.

`compiler/conformance/valid/array-aliases.trb` turns the relevant Array
change into an executable compiler differential. It grows one Integer Array
through two aliases, mutates it through a mutable parameter, rebinds that
parameter to a different Array, and then mutates the original through the
second caller alias. Recovery and current Native compiler generations plus the
same TypeRB-authored compiler built by the selected Go reference must emit
byte-identical QBE and produce the same output. This preserves three portable
rules:

- assigning or passing an Array preserves its outer reference identity;
- destructive growth and element updates remain visible through every alias;
- rebinding a `mut` parameter changes only that local binding and never writes
  a replacement Array into the caller binding.

The selected reference checker also distinguishes a Nil value from a Void
result. Repository-owned source is formatted, checked, and tested by that
checker. Native does not infer full nullable or Void compatibility from this
pin: unsupported language surface remains outside the self-hosted subset and
must still fail explicitly.

## Current declaration-import mapping

The self-hosted frontend implements the part of TypeRB 0.4 declaration imports
that has a representation in its current record-and-function subset:

| TypeRB behavior | Current Native behavior |
| --- | --- |
| Named import | Selects an exact top-level record or function declaration |
| Named `as` alias | Changes only the local binding; canonical declaration identity remains exact |
| Bare project import | Selects one matching record root; records are the only root-eligible kind in the current subset |
| Bare `as` alias | Selects the same unique record first, then changes its local binding |
| Root key | Removes ASCII `_` from the logical final path segment and folds ASCII case; declaration names fold ASCII case without removing `_` |
| Directory entry | A resolved `name/index` module uses `name` as its logical root segment; `name` and `name/index` can resolve to that same module |
| Direct/index conflict | Rejects a resolved graph containing both `name` and `name/index`; there is no precedence between two loaded module identities |
| Duplicate identity | Rejects importing the same declaration identity again, including through a different alias or equivalent index path |
| Binding and usage | Rejects duplicate local bindings, local-declaration collisions, missing exports, and unused aliases under their local names |

Bare imports do not create lowercase namespaces and never import every export.
A top-level function remains available through an exact named import but cannot
become a bare root. Zero matches, multiple matching record roots, and a
function-only match produce deterministic diagnostics.

Package imports, `activate`, modules, classes, enums, interfaces, aliases,
newtypes, constants, owned nested declarations, and project-aware formatter
rewrites remain outside the self-hosted subset. Relevant source forms are
rejected explicitly; they do not fall back to the pre-0.4 namespace or
loaded-identity precedence model. Repository-owned TypeRB source is still
formatted and checked by the pinned reference compiler.

## Source pins and bootstrap seeds

The reference pin and a Native bootstrap seed answer different questions:

- `TYPE_RB_REVISION` selects the exact syntax, semantics, formatter, and
  differential oracle used for current development.
- A Native seed is an executable predecessor used to compile the current
  TypeRB-authored compiler. Its source-era metadata records provenance; it does
  not constrain the source revision that a later compatible compiler may
  accept.
- The immutable
  [`bootstrap-seed-2026-08-30`](https://github.com/type-rb/type-rb-native/releases/tag/bootstrap-seed-2026-08-30)
  remains unchanged. When its embedded runtime or link policy predates current
  source, compatibility uses separately identified setup-only Native
  transitions before proving exact current B2/B3/B4 fixed points. The
  transitions remain Go-free and outside candidate timing and size claims;
  they do not replace or relabel the seed.

A later seed is warranted only by a concrete distribution need demonstrated by
the compatibility chain. The existing attested seed reaches the exact
`0.4.4-dev` fixed point on both targets through two setup-only transitions.
That confirms bootstrap feasibility without making the older embedded runtime
free: a future seed containing the current runtime can remove both transitions.
Revision alignment alone does not warrant replacing or relabelling the seed.
The Linux amd64 target demonstrates the complementary case: it is recovered
from the immutable seed release's target-neutral root QBE, not from an amd64
seed executable. Its exact current chain and workflow are therefore recorded
as target-chain evidence in compatibility schema version 2, while the
immutable seed manifest remains unchanged. See the
[Gate 6N result](../results/2026-08-31-gate6n-linux-amd64/README.md) and
[Decision 0026](decisions/0026-recovered-target-chain-evidence.md).
Native SemVer is now independently defined for experimental development, but
TypeRB compatibility ranges, stable installation policy, and support promises
remain deferred. The current schema can express only this exact verified
TypeRB revision.
