# TypeRB Compatibility

TypeRB Native follows exact reference revisions while it is experimental. The
current source and semantic oracle is TypeRB
`7fcc1d7f8978d5335368c1d4d3be4c79db86d995` (`0.4.1-dev`), recorded in
`TYPE_RB_REVISION`. This is an exact development pin, not a supported version
range.

The compatibility work is registered in
[issue #97](https://github.com/type-rb/type-rb-native/issues/97). The issue
owns the complete cross-target fixed-point and measurement criteria. This
document records the implementation boundary independently of those results.

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
  remains unchanged. Compatibility is established by building current B2 from
  that previous Native B1 and then proving exact B2/B3/B4 fixed points, not by
  replacing or relabelling the seed.

A later seed is warranted only by a concrete distribution need demonstrated by
the completed compatibility chain. Native SemVer, TypeRB compatibility ranges,
installation policy, and support promises remain deferred.
