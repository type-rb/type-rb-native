# Ordinary compiler project layout

The project relocation registered in [issue #274](https://github.com/type-rb/type-rb-native/issues/274)
moves `compiler/gate4/` to `compiler/`. The checkpoint number is not a permanent
compiler responsibility. There is one canonical tree, without an old-path
copy, symlink or compatibility alias.

| Previous path prefix | Current path prefix |
| --- | --- |
| `compiler/gate4/src/` | `compiler/src/` |
| `compiler/gate4/conformance/` | `compiler/conformance/` |
| `compiler/gate4/trbconfig.jsonc` | `compiler/trbconfig.jsonc` |
| `compiler/gate4/go.mod` | `compiler/go.mod` |
| `compiler/gate4/native-mir-*.txt` | `compiler/native-mir-*.txt` |

At the relocation checkpoint, all nine ordinary source modules, import/declaration identities, conformance
inputs/expectations and transition-marker contents are unchanged. The moved
compiler integration test and root recovery tests use the new repository
paths. The recovery Go module identity is unchanged; the Go project is a
reference/recovery tool, not an ordinary bootstrap dependency.

Subsequent responsibility extraction adds `qbe_output.trb` and `qbe_runtime.trb`
to the canonical closure; current recovery validates eleven modules. See the
[organization schedule](repository-organization.md) for the later ownership
changes rather than treating the relocation's nine-module count as permanent.

## Current consumers and historical checkouts

Current configuration, source discovery, recovery, compatibility validation,
target/memory harnesses, CI and live documentation use the new path. CI
classifies all non-documentation changes under `compiler/`, including old-path
deletions, as compiler work. Project-layout and policy helper changes retain
the full authority set too.

Cross-revision controllers source `tools/compiler-project.sh` from the
controller checkout and call `native_compiler_project_directory` for each
source root separately. The helper recognizes the current project or the
historical `compiler/gate4/` project, requires its entry and configuration, and
rejects missing or ambiguous layouts before compilation. A historical checkout
does not need to contain the new helper. Resolve the path before timing;
the helper is test/measurement orchestration, not a child in the ordinary
compiler's external-tool process graph.

Source `tools/compiler-project.sh` before `tools/native-mir-transition-policy.sh`.
Policy uses that same project resolver for marker validity and baseline
presence. A marker moved with an existing baseline remains present: it cannot
grant a foundation/scalar/control-flow transition allowance again. Missing or
ambiguous projects fail policy comparison without printing an allowance.
Marker values, historical hashes and all size/build/RSS thresholds are unchanged.

## Deliberately retained old-path references

- Source-era `tools/gate4-benchmark`, `gate5-benchmark`, and `gate6a` through
  `gate6k` plus `gate6m` benchmark controllers keep their registered snapshot,
  import-closure and digest contracts. Their tests remain enabled. They operate
  on their historical source roots, not a compatibility copy of today's compiler.
- `tools/gate6m-linux.sh` likewise retains its exact `97b3ac2` source/digest
  contract and historical path. Current Linux regressions use the newer target
  workflow and harness, not a relabelled Gate 6M measurement.
- The five fixed-baseline workflows (`native-mir-foundation`,
  `native-runtime-ab`, `array-push-fast-path`, `dynamic-array-address`, and
  `gc-temp-push-fast-path`) retain old paths for their exact historical baseline
  revisions; candidate-side paths move. The configurable current compactness
  comparison resolves both roots rather than assuming either layout.
- Recorded results, accepted decisions and historical gate narratives keep
  their commands, paths, hashes and source-era meaning. The former tree is
  available at the [last pre-move baseline](https://github.com/type-rb/type-rb-native/tree/b90feae452ae7819f8173475e37ba7dcbc3dd7f8/compiler/gate4).
- Negative layout and CI-routing tests intentionally mention both names.

This is a project relocation, not broader MIR coverage, a runtime optimization,
or completion of the [remaining organization work](repository-organization.md).
Root snapshot/runtime names and gate-derived implementation symbols remain
separate bounded naming work; immutable evidence labels can remain permanently.
