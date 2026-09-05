# Root source inventory

## Scope and reading the inventory

This inventories all 45 root `src/*.trb` files for the first support-code
organization slice, [issue #258](https://github.com/type-rb/type-rb-native/issues/258),
against baseline `2522a995fdf48985745ccf9cfef945da6e7f17b1`.
Rows show the candidate names after the two matched-driver file moves.
No file has been classified for retirement: every implementation has callers
or an explicit recovery/verification role, and every test remains discovered.

Names in dependency columns are root module stems (append `.trb`).
Imports list local project dependencies; `trb/std/*` imports remain in source.
Consumers list direct root importers, not all transitive callers.
Every test row is consumed by root test discovery even without an importer.
An empty direct-consumer list is therefore not a dead-code finding.

The proposed names below are destinations within `src/`, not additional
directories or committed moves. Except for `matched_go_driver{,_test}.trb`,
they require separate reviewed slices. Shared source identities, scalar types,
JSON helpers, and QBE helpers must remain one implementation; naming proposals
do not authorize merging the snapshot and ordinary self-hosted MIRs.

## File inventory

| File in `src/` | Responsibility | Local imports | Direct consumers | Disposition / proposed destination |
| --- | --- | --- | --- | --- |
| [diagnostic.trb](../src/diagnostic.trb) | Shared deterministic diagnostics | — | `gate0`, `gate1_mir`, `gate1_snapshot`, `gate2_layout`, `gate2_mir`, `gate2_snapshot`, `gate3_layout`, `gate3_mir`, `gate3_snapshot`, `json_boundary`, `native_mir`, `qbe`, `qbe2`, `qbe3`, `snapshot` | Keep: `diagnostic.trb` |
| [gate0.trb](../src/gate0.trb) | Snapshot v1 validate/lower entry | `diagnostic`, `native_mir`, `snapshot` | `gate0_test` | Keep; rename later: `snapshot_boundary.trb` |
| [gate0_test.trb](../src/gate0_test.trb) | Test: Gate 0 boundary | `gate0`, `native_mir`, `snapshot`, `native_file_system` | Root test discovery | Keep; rename later: `snapshot_boundary_test.trb` |
| [gate1_differential_test.trb](../src/gate1_differential_test.trb) | Test: Gate 1 source-connected differential corpus | `gate1_snapshot`, `gate1_toolchain`, `native_file_system` | Root test discovery | Keep; rename later: `scalar_differential_test.trb` |
| [gate1_driver.trb](../src/gate1_driver.trb) | Snapshot/recovery/comparison CLI entry | `gate1_snapshot`, `gate1_toolchain`, `gate2_snapshot`, `gate2_toolchain`, `gate3_snapshot`, `gate3_toolchain`, `gate4_toolchain`, `matched_go_driver`, `gate6f_compiler_source`, `native_file_system` | Root executable CLI | Keep; rename later: `bootstrap_driver.trb` |
| [gate1_mir.trb](../src/gate1_mir.trb) | Scalar MIR and shared scalar operators | `diagnostic`, `native_mir`, `snapshot` | `gate1_snapshot`, `gate1_test`, `gate1_toolchain`, `gate2_layout`, `gate2_layout_test`, `gate2_mir`, `gate2_mir_test`, `gate2_snapshot`, `gate3_capture_test`, `gate3_gc_test`, `gate3_integer_array_test`, `gate3_layout`, `gate3_layout_test`, `gate3_mir`, `gate3_mir_test`, `gate3_snapshot`, `qbe`, `qbe2`, `qbe3` | Keep; rename later: `scalar_mir.trb` |
| [gate1_snapshot.trb](../src/gate1_snapshot.trb) | Snapshot v2 scalar decoder | `diagnostic`, `gate1_mir`, `native_mir`, `json_boundary`, `snapshot` | `gate1_differential_test`, `gate1_driver`, `gate1_test` | Keep; rename later: `scalar_snapshot.trb` |
| [gate1_test.trb](../src/gate1_test.trb) | Test: Gate 1 scalar QBE path | `gate1_mir`, `gate1_toolchain`, `gate1_snapshot`, `native_mir`, `qbe`, `snapshot`, `native_file_system` | Root test discovery | Keep; rename later: `scalar_qbe_test.trb` |
| [gate1_toolchain.trb](../src/gate1_toolchain.trb) | Scalar QBE tool invocation | `gate1_mir`, `qbe`, `native_file_system` | `gate1_differential_test`, `gate1_driver`, `gate1_test` | Keep; rename later: `scalar_toolchain.trb` |
| [gate2_differential_test.trb](../src/gate2_differential_test.trb) | Test: Gate 2 source-connected differential corpus | `gate2_snapshot`, `gate2_toolchain`, `native_file_system` | Root test discovery | Keep; rename later: `aggregate_differential_test.trb` |
| [gate2_layout.trb](../src/gate2_layout.trb) | Heap-free aggregate layout | `diagnostic`, `gate1_mir` | `gate2_layout_test`, `gate2_mir`, `gate2_mir_test`, `gate2_snapshot`, `qbe2` | Keep; rename later: `aggregate_layout.trb` |
| [gate2_layout_test.trb](../src/gate2_layout_test.trb) | Test: Gate 2 static aggregate layout | `gate2_layout`, `gate1_mir` | Root test discovery | Keep; rename later: `aggregate_layout_test.trb` |
| [gate2_mir.trb](../src/gate2_mir.trb) | Heap-free aggregate MIR/verifier | `diagnostic`, `gate1_mir`, `gate2_layout`, `native_mir`, `snapshot` | `gate2_mir_test`, `gate2_snapshot`, `gate2_toolchain`, `qbe2` | Keep; rename later: `aggregate_mir.trb` |
| [gate2_mir_test.trb](../src/gate2_mir_test.trb) | Test: Gate 2 aggregate MIR | `gate1_mir`, `gate2_layout`, `gate2_mir`, `gate2_toolchain`, `native_mir`, `qbe2`, `snapshot`, `native_file_system` | Root test discovery | Keep; rename later: `aggregate_mir_test.trb` |
| [gate2_snapshot.trb](../src/gate2_snapshot.trb) | Snapshot v3 aggregate decoder | `diagnostic`, `gate1_mir`, `gate2_mir`, `gate2_layout`, `native_mir`, `json_boundary`, `snapshot` | `gate1_driver`, `gate2_differential_test`, `gate2_snapshot_test` | Keep; rename later: `aggregate_snapshot.trb` |
| [gate2_snapshot_test.trb](../src/gate2_snapshot_test.trb) | Test: Gate 2 snapshot v3 | `gate2_snapshot`, `gate2_toolchain`, `qbe2`, `native_file_system` | Root test discovery | Keep; rename later: `aggregate_snapshot_test.trb` |
| [gate2_toolchain.trb](../src/gate2_toolchain.trb) | Aggregate QBE tool invocation | `gate2_mir`, `qbe2`, `native_file_system` | `gate1_driver`, `gate2_differential_test`, `gate2_mir_test`, `gate2_snapshot_test` | Keep; rename later: `aggregate_toolchain.trb` |
| [gate3_capture_test.trb](../src/gate3_capture_test.trb) | Test: Gate 3 closure capture runtime | `gate1_mir`, `gate3_layout`, `gate3_mir`, `gate3_toolchain`, `native_mir`, `snapshot`, `native_file_system` | Root test discovery | Keep; rename later: `closure_capture_test.trb` |
| [gate3_differential_test.trb](../src/gate3_differential_test.trb) | Test: Gate 3 source-connected differential corpus | `gate3_snapshot`, `gate3_toolchain`, `qbe3`, `native_file_system` | Root test discovery | Keep; rename later: `managed_differential_test.trb` |
| [gate3_gc_test.trb](../src/gate3_gc_test.trb) | Test: Gate 3 tracing collector | `gate1_mir`, `gate3_layout`, `gate3_mir`, `gate3_toolchain`, `native_mir`, `snapshot`, `native_file_system` | Root test discovery | Keep; rename later: `managed_gc_test.trb` |
| [gate3_integer_array_test.trb](../src/gate3_integer_array_test.trb) | Test: Gate 3 Integer Array runtime | `gate1_mir`, `gate3_layout`, `gate3_mir`, `gate3_toolchain`, `native_mir`, `snapshot`, `native_file_system` | Root test discovery | Keep; rename later: `managed_integer_array_test.trb` |
| [gate3_layout.trb](../src/gate3_layout.trb) | Managed-reference aggregate layout | `diagnostic`, `gate1_mir` | `gate3_capture_test`, `gate3_gc_test`, `gate3_integer_array_test`, `gate3_layout_test`, `gate3_managed_aggregate_test`, `gate3_mir`, `gate3_mir_test`, `gate3_snapshot`, `qbe3` | Keep; rename later: `managed_layout.trb` |
| [gate3_layout_test.trb](../src/gate3_layout_test.trb) | Test: Gate 3 static aggregate layout | `gate3_layout`, `gate1_mir` | Root test discovery | Keep; rename later: `managed_layout_test.trb` |
| [gate3_managed_aggregate_test.trb](../src/gate3_managed_aggregate_test.trb) | Test: Gate 3 managed aggregate runtime | `gate3_layout`, `gate3_mir`, `gate3_toolchain`, `native_mir`, `snapshot`, `native_file_system` | Root test discovery | Keep; rename later: `managed_aggregate_test.trb` |
| [gate3_mir.trb](../src/gate3_mir.trb) | Managed MIR/verifier | `diagnostic`, `gate1_mir`, `gate3_layout`, `native_mir`, `snapshot` | `gate3_capture_test`, `gate3_gc_test`, `gate3_integer_array_test`, `gate3_managed_aggregate_test`, `gate3_mir_test`, `gate3_snapshot`, `gate3_toolchain`, `qbe3` | Keep; rename later: `managed_mir.trb` |
| [gate3_mir_test.trb](../src/gate3_mir_test.trb) | Test: Gate 3 aggregate MIR | `gate1_mir`, `gate3_layout`, `gate3_mir`, `native_mir`, `snapshot` | Root test discovery | Keep; rename later: `managed_mir_test.trb` |
| [gate3_runtime.trb](../src/gate3_runtime.trb) | Managed QBE runtime generation | `qbe` | `qbe3` | Keep; rename later: `managed_runtime.trb` |
| [gate3_snapshot.trb](../src/gate3_snapshot.trb) | Snapshot v4 decoder, including compiler recovery | `diagnostic`, `gate1_mir`, `gate3_mir`, `gate3_layout`, `native_mir`, `json_boundary`, `snapshot` | `gate1_driver`, `gate3_differential_test`, `gate3_snapshot_test`, `gate4_bootstrap_test`, `qbe3_test` | Keep; rename later: `managed_snapshot.trb` |
| [gate3_snapshot_test.trb](../src/gate3_snapshot_test.trb) | Test: Gate 3 snapshot v4 | `gate3_snapshot`, `native_file_system` | Root test discovery | Keep; rename later: `managed_snapshot_test.trb` |
| [gate3_toolchain.trb](../src/gate3_toolchain.trb) | Managed executable and recovery builds | `gate3_mir`, `qbe3`, `native_file_system` | `gate1_driver`, `gate3_capture_test`, `gate3_differential_test`, `gate3_gc_test`, `gate3_integer_array_test`, `gate3_managed_aggregate_test`, `gate4_bootstrap_test`, `qbe3_test` | Keep; rename later: `managed_toolchain.trb` |
| [gate4_bootstrap_test.trb](../src/gate4_bootstrap_test.trb) | Test: Gate 4 reference bootstrap | `gate3_snapshot`, `gate3_toolchain`, `gate4_toolchain`, `matched_go_driver`, `gate6f_compiler_source`, `native_file_system` | Root test discovery | Keep; rename later: `compiler_recovery_test.trb` |
| [gate4_toolchain.trb](../src/gate4_toolchain.trb) | Hidden-input recovery generation runner | `native_file_system` | `gate1_driver`, `gate4_bootstrap_test` | Keep; rename later: `recovery_generation.trb` |
| [gate6f_compiler_source.trb](../src/gate6f_compiler_source.trb) | Strict recovery source closure/flattening | `native_file_system` | `gate1_driver`, `gate4_bootstrap_test`, `gate6f_compiler_source_test` | Keep; rename later: `compiler_source.trb` |
| [gate6f_compiler_source_test.trb](../src/gate6f_compiler_source_test.trb) | Test: Gate 6F compiler source closure | `gate6f_compiler_source` | Root test discovery | Keep; rename later: `compiler_source_test.trb` |
| [json_boundary.trb](../src/json_boundary.trb) | Shared strict JSON field decoding | `diagnostic` | `gate1_snapshot`, `gate2_snapshot`, `gate3_snapshot` | Keep: `json_boundary.trb` |
| [matched_go_driver.trb](../src/matched_go_driver.trb) | Matched Go comparison source/build adapter | `native_file_system` | `gate1_driver`, `gate4_bootstrap_test`, `matched_go_driver_test` | Moved in this slice: `matched_go_driver.trb` |
| [matched_go_driver_test.trb](../src/matched_go_driver_test.trb) | Test: Matched Go compiler comparison driver | `matched_go_driver` | Root test discovery | Moved in this slice: `matched_go_driver_test.trb` |
| [native_file_system.trb](../src/native_file_system.trb) | Reference-side file/process test support | — | `gate0_test`, `gate1_differential_test`, `gate1_driver`, `gate1_test`, `gate1_toolchain`, `gate2_differential_test`, `gate2_mir_test`, `gate2_snapshot_test`, `gate2_toolchain`, `gate3_capture_test`, `gate3_differential_test`, `gate3_gc_test`, `gate3_integer_array_test`, `gate3_managed_aggregate_test`, `gate3_snapshot_test`, `gate3_toolchain`, `gate4_bootstrap_test`, `gate4_toolchain`, `gate6f_compiler_source`, `matched_go_driver`, `native_file_system_test`, `qbe3_test` | Keep: `native_file_system.trb` |
| [native_file_system_test.trb](../src/native_file_system_test.trb) | Test: Native filesystem support | `native_file_system` | Root test discovery | Keep: `native_file_system_test.trb` |
| [native_mir.trb](../src/native_mir.trb) | Snapshot v1 MIR and shared source identities | `diagnostic`, `snapshot` | `gate0`, `gate0_test`, `gate1_mir`, `gate1_snapshot`, `gate1_test`, `gate2_mir`, `gate2_mir_test`, `gate2_snapshot`, `gate3_capture_test`, `gate3_gc_test`, `gate3_integer_array_test`, `gate3_managed_aggregate_test`, `gate3_mir`, `gate3_mir_test`, `gate3_snapshot` | Keep; rename later: `snapshot_mir.trb` |
| [qbe.trb](../src/qbe.trb) | Scalar QBE plus shared emission helpers | `diagnostic`, `gate1_mir`, `snapshot` | `gate1_test`, `gate1_toolchain`, `gate3_runtime`, `qbe2`, `qbe3` | Keep; rename later: `scalar_qbe.trb` |
| [qbe2.trb](../src/qbe2.trb) | Aggregate QBE adapter | `diagnostic`, `gate1_mir`, `gate2_layout`, `gate2_mir`, `qbe`, `snapshot` | `gate2_mir_test`, `gate2_snapshot_test`, `gate2_toolchain` | Keep; rename later: `aggregate_qbe.trb` |
| [qbe3.trb](../src/qbe3.trb) | Managed/recovery QBE adapter | `diagnostic`, `gate1_mir`, `gate3_layout`, `gate3_runtime`, `gate3_mir`, `qbe`, `snapshot` | `gate3_differential_test`, `gate3_toolchain`, `qbe3_test` | Keep; rename later: `managed_qbe.trb` |
| [qbe3_test.trb](../src/qbe3_test.trb) | Test: Gate 3 managed QBE runtime | `gate3_snapshot`, `gate3_toolchain`, `qbe3`, `native_file_system` | Root test discovery | Keep; rename later: `managed_qbe_test.trb` |
| [snapshot.trb](../src/snapshot.trb) | Snapshot v1 schema and shared source origins | `diagnostic` | `gate0`, `gate0_test`, `gate1_mir`, `gate1_snapshot`, `gate1_test`, `gate2_mir`, `gate2_mir_test`, `gate2_snapshot`, `gate3_capture_test`, `gate3_gc_test`, `gate3_integer_array_test`, `gate3_managed_aggregate_test`, `gate3_mir`, `gate3_mir_test`, `gate3_snapshot`, `native_mir`, `qbe`, `qbe2`, `qbe3` | Keep; rename later: `snapshot_v1.trb` |

## Non-import consumers and verification

- Root `trbconfig.jsonc` selects `src/`; reference `trb check` checks the
  root project, and `trb test` discovers all `*_test.trb` files. Production
  root builds include the reachable CLI implementation, not test definitions.
  Both `pull-request.yml` quick checks and `gate-zero.yml` exercise this
  project; the latter enables recovery and QBE-backed tests. Preserve these
  paths and environment controls when moving any row.
- `gate1_driver.trb` is the multi-mode root executable, despite its name.
  `tools/gate1-benchmark`, `gate2-benchmark`, and `gate3-benchmark` invoke
  its snapshot paths; `tools/gate4-benchmark` and `gate5-benchmark` invoke
  recovery and matched comparison modes. These process callers are not
  TypeRB module import edges.
- `gate4_bootstrap_test.trb` calls the managed snapshot/toolchain, generation,
  matched Go adapter, and strict flattening helper. It is an active full
  recovery/differential/mutation test, not disposable Gate 4 scaffolding.
- `gate3_snapshot.trb` is also read by
  `tools/compatibility_manifest.py` to check supported snapshot versions.
  Its moved path must update that consumer atomically.
- The ordinary compiler closure is `compiler/gate4/src/compiler.trb` plus its
  explicit storage/path/MIR/literal/state/parser imports. State depends on the
  MIR model and shared storage/literal helpers; the parser depends on state and
  storage, never back on the compiler entry. Root helpers do not become ordinary compiler
  modules just because the reference root project compiles them.
  `gate6f_compiler_source.trb` validates the entry, MIR, state and parser import prefixes
  and derives a recovery-only flat source from seven canonical inputs. Compiler module extraction must
  update this derivation and its tests together.
- `tools/bootstrap-seed.sh` and current target/memory/performance workflows
  build the ordinary closure through explicit paths. `tools/gate6*-benchmark`
  also retain closure/path assumptions and historical command shapes.
  Do not infer that those consumers are updated by changing root imports.
- The root managed-runtime emitter and QBE adapters are exercised by recovery
  and their respective differential/layout/runtime tests. The ordinary runtime
  embedded in the compiler has a separate maintenance surface; this inventory
  does not claim they are already physically unified.
- Frozen result directories, source manifests, and dated gate plans may retain
  old names. They are historical references, not executable consumers to edit
  with a global replacement. Before each later move, repeat a repository-wide
  caller/path search; this inventory is a reviewed starting point, not a
  substitute for current dependency analysis.

## First actual move and retained protocol

| Previous path | Current path |
| --- | --- |
| `src/gate5_matched_driver.trb` | `src/matched_go_driver.trb` |
| `src/gate5_matched_driver_test.trb` | `src/matched_go_driver_test.trb` |

The record is now `MatchedGoDriverError`; source transformation and driver
helpers use `matched_go_*`, and the build entry is
`build_matched_go_compiler`. Root dispatch and recovery-test imports/calls
move with them. There is no compatibility alias or copied implementation.

The command/output prefix `gate5-matched-go` and basenames
`gate5-matched-go-compiler{,.trb}` remain unchanged because the retained
measurement controller consumes them. The generated comparison source,
diagnostics, process arguments, and empty-entry transformation are unchanged.
These protocol exceptions are deliberate and do not justify gate-derived
names for new implementation modules.

## Next review

After this slice passes, resume the independently registered checked-binary
ownership work. The next organization checkpoint considers
`gate6f_compiler_source.trb` and its test as a cohesive support module, or a
proven independent compiler module if that is the smaller safe change.
Register its exact baseline and recovery/identity checks first. Do not combine
a compiler-source split, broad namespace renaming, and optimization in one PR.
