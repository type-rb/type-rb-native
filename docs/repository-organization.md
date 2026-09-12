# Repository ownership and decomposition

Current source names describe responsibilities. The supported recovery paths stay
separate from ordinary compilation and share implementation where their semantics
agree. Completed naming and extraction history is available in the
[historical documentation](history.md); it is not the current decomposition plan.

## Current ownership map

| Current area | Responsibility |
| --- | --- |
| `compiler/src/` | Ordinary compiler: `CompilerState`, `CheckedLocals`, `CheckedValue`, `QbeEmitContext`, and `QbeValue` use role names. MIR records, construction, analysis, rewrites, verification and QBE adaptation have separate modules; see the [architecture map](architecture.md). |
| `src/snapshot_validation.trb` and shared snapshot/diagnostic/MIR modules | Snapshot boundary validation and shared support. |
| `src/recovery_scalar_*`, `recovery_aggregate_*`, `recovery_managed_*` | Retained scalar, aggregate and managed snapshot recovery, including layout, QBE, runtime and differential tests. These paths cover distinct supported capabilities. |
| `src/recovery_driver.trb`, `recovery_generation.trb`, `matched_go_driver.trb`, `compiler_recovery_source.trb`, `compiler_recovery_layout.trb` | Recovery orchestration, comparison and strict derivation from the canonical compiler modules. Ordinary builds keep their file-root closure. |
| `compiler/conformance/`, `corpus/`, `fixtures/` | Active correctness cases, grouped by feature or recovery capability. Names and callers move together. |
| `tools/recovery-bootstrap.sh`, `normalize-compiler.sh`, `linux-amd64-targets.sh`, `external-qbe-build.sh`, `measure-command.py` | Recovery, deterministic linking, target validation and external measurement. |
| `.github/workflows/native-validation.yml`, `linux-amd64-targets.yml` | Current correctness/recovery and target authorities. |
| `results/`, dated plans/decisions, immutable seeds | Historical evidence with original names, commands, hashes and revisions. |

The compiler's private generated QBE symbols use `trbn` rather than an experiment
number. Current recovery driver commands and GC report prefixes describe their
roles. No stable public protocol or snapshot version is changed by this rename.

## Remaining consolidation

The [MIR milestone](mir-consolidation.md) owns the remaining structural work.
Route supported ordinary functions through verified typed values, operations and
control flow. Move semantic effects, Array-header validity and root-safety decisions
above the backend; remove the superseded direct path as its consumers migrate.
Split the large checker, MIR and emitter modules by those responsibilities, with
explicit dependencies rather than copied helpers or forwarding aliases.

Keep source moves and their recovery derivation, imports, tests and operational
consumers together. Useful shared code remains one implementation. Complete
cohesive ownership changes without requiring another performance qualification
for each helper extraction. Required correctness and reproducibility remain blocking.

## Current source and historical consumers

The [compiler-name seed handoff](bootstrap-seed-updates.md) removed the predecessor
intrinsic declarations, wrappers and dual recognition. Intrinsic emission uses
actual declaration identity, independent of declaration order. The source-name
check covers current paths, implementation names, comments and visible Markdown; immutable history links and result records remain reproduction evidence.

Cross-revision measurement tools retain a historical project-layout resolver and
explicit deletion/rename tests. Frozen standalone comparisons and the historical
portable-entry workflow use their exact old source paths. Initial-root metadata,
immutable seeds and recorded results retain their authenticated identities.
These are reproduction inputs, not alternate current implementation owners.

See [compiler layout](compiler-project-layout.md), [retired controllers](retired-experiment-tools.md)
and [validation](ci-validation.md) for those boundaries.
