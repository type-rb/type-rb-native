# Repository ownership and decomposition

Current source names describe responsibilities. The supported recovery paths stay
separate from ordinary compilation and share implementation where their semantics
agree. Completed naming and extraction history is available in the
[historical documentation](history.md); it is not the current decomposition plan.

## Current ownership map

| Current area | Responsibility |
| --- | --- |
| `compiler/src/` | Ordinary compiler: `CompilerState`, `CheckedLocals`, `CheckedValue`, `QbeEmitContext`, and `QbeValue` use role names. Lexing and source slicing live in `lexer.trb`; MIR records, construction, analysis, rewrites, verification and QBE adaptation have separate modules; see the [architecture map](architecture.md). |
| `compiler/src/checked_body.trb` | Concrete function-owned checked projections; shared parsed syntax stays in the program, and backend emission needs only verified MIR. |
| `compiler/src/mir_value_control.trb` | Typed branch exits, common result blocks and numeric join conversions; recursive source checking and REPL evaluation consume shared frontend regions. |
| `compiler/src/default_arguments.trb` | Private initializer declaration identities and preceding typed slots; ordinary checked functions and MIR own their bodies and calls. |
| `compiler/cli/repl_project.trb` | REPL project discovery, generated-import filtering and visible nominal type names. Session checking/evaluation remains in the REPL adapters. |
| `compiler/src/checked_submission.trb`, `compiler/cli/repl_check.trb` | Ordinary checked entry/exit facts and result types, plus REPL source loading and boundary mapping. Session completion and replay own fact persistence; QBE consumes only verified MIR. |
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
Accepted ordinary functions now require verified typed values, operations and
control flow. The direct emitter and its token Array/header/assignment analyses
are removed. Numeric expansion, Array-header validity and root plans are selected
and verified above QBE; function ABI emission lives in `qbe_functions.trb`.
Split the large checker, MIR and emitter modules by those responsibilities, with
explicit dependencies rather than copied helpers or forwarding aliases.
The value-join builder and nullable type, flow-fact, MIR, QBE and REPL helpers
have been extracted. Expression/body checking remains
mutually recursive; separating it into modules requires removing that dependency
cycle because ordinary Native module imports must be acyclic.

The checked-body ownership change moves type applications, nullable, enum, Result,
Hash, Range and control projections together. Its exit criteria are independent
facts at identical source origins, caller restoration in the REPL, unchanged
emission after projection erasure, and complete ordinary/recovery checks.
See [decision 0047](decisions/0047-checked-body-ownership.md).

Generic function orchestration is split into instance declaration, an isolated
semantic program fork, and template checking. Shared syntax stays immutable;
concrete body facts and MIR remain function-owned. These modules extend the same
source-erasure and ordinary/recovery checks without a second backend path; see
[decision 0048](decisions/0048-generic-function-mir.md). Generic record defaults
reuse the ordinary record parser and private initializer path. The shared
`generic_bindings.trb` owns declaration-scoped substitutions for functions and
record defaults; separate function/nominal abstract identities prevent accidental
capture. See [decision 0049](decisions/0049-generic-record-default-mir.md).

Keep source moves and their recovery derivation, imports, tests and operational
consumers together. Useful shared code remains one implementation. Complete
cohesive ownership changes without requiring another performance qualification
for each helper extraction. Required correctness and reproducibility remain blocking.

## Current source and historical consumers

The [compiler-name seed handoff](bootstrap-seed-updates.md) removed the predecessor
intrinsic declarations, wrappers and dual recognition. MIR admission, intrinsic
calls and ordinary body omission share declaration-bound identity. Extracted helpers and imported aliases resolve to the same owner; unrelated
same-named functions retain ordinary calls. CLI adapters follow the imported core
compiler for that ownership. The source-name
check covers current paths, implementation names, comments and visible Markdown; immutable history links and result records remain reproduction evidence.

Cross-revision measurement tools retain a historical project-layout resolver and
explicit deletion/rename tests. Frozen standalone comparisons and the historical
portable-entry workflow use their exact old source paths. Initial-root metadata,
immutable seeds and recorded results retain their authenticated identities.
These are reproduction inputs, not alternate current implementation owners.

See [compiler layout](compiler-project-layout.md), [retired controllers](retired-experiment-tools.md)
and [validation](ci-validation.md) for those boundaries.
