# TypeRB Compatibility

TypeRB Native follows exact reference revisions while it is experimental. The
current source and semantic oracle is TypeRB
`5dc09070cf7f88a569279f5e63982a6de59d692c` (`0.4.4-dev`), recorded in
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
[Darwin/Linux arm64 result](../results/2026-08-30-typerb-0-4-compatibility-darwin-linux-arm64/README.md)
passes the selected `0.4.1-dev` reference, previous-seed, exact fixed-point,
process, elapsed-time, peak-RSS, and compiler-size criteria. The `0.4.3-dev`
successor is registered in
[issue #106](https://github.com/type-rb/type-rb-native/issues/106), and its
[Darwin/Linux arm64 result](../results/2026-08-30-typerb-0-4-3-compatibility-darwin-linux-arm64/README.md)
passes the selected-reference, explicit setup-transition, exact fixed-point,
process, elapsed-time, peak-RSS, and compiler-size criteria. This document
records the implementation boundary independently of those measurements.
The current scoped-file successor is registered in
[issue #144](https://github.com/type-rb/type-rb-native/issues/144), and its
[Darwin/Linux arm64 result](../results/2026-08-31-typerb-0-4-4-compatibility-darwin-linux-arm64/README.md)
passes the selected-reference, migration, exact-baseline, target-regression,
fixed-point, process, resource, and size criteria.

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

`compiler/gate4/conformance/valid/array-aliases.trb` turns the relevant Array
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
