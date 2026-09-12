# Root source ownership

This table names the current root source and its direct source consumers. Tests
are discovered independently of imports. A module with no direct importer can be
an executable/controller entry; that is not a reason to delete it.

The [recovery guide](snapshot-recovery.md) describes the scalar, aggregate and
managed boundaries. Ordinary compiler modules live separately under `compiler/src/`.
Earlier inventories and renaming history remain in the [historical record](history.md).

| Source | Responsibility | Direct consumers |
| --- | --- | --- |
| [aggregate_layout.trb](../src/aggregate_layout.trb) | Heap-free aggregate recovery | `aggregate_layout_test.trb`, `recovery_aggregate_mir.trb`, `recovery_aggregate_mir_test.trb`, `recovery_aggregate_qbe.trb`, `recovery_aggregate_snapshot.trb` |
| [aggregate_layout_test.trb](../src/aggregate_layout_test.trb) | Regression tests | Root test discovery |
| [compiler_recovery_layout.trb](../src/compiler_recovery_layout.trb) | Exact recovery module and import inventory | `compiler_recovery_source.trb`, `compiler_recovery_source_test.trb` |
| [compiler_recovery_mutations.trb](../src/compiler_recovery_mutations.trb) | Recovery module mutation controls | `compiler_recovery_test.trb` |
| [compiler_recovery_source.trb](../src/compiler_recovery_source.trb) | Compiler/program recovery orchestration | `compiler_recovery_source_test.trb`, `compiler_recovery_test.trb`, `recovery_driver.trb` |
| [compiler_recovery_source_test.trb](../src/compiler_recovery_source_test.trb) | Regression tests | Root test discovery |
| [compiler_recovery_test.trb](../src/compiler_recovery_test.trb) | Regression tests | Root test discovery |
| [compiler_recovery_workspace.trb](../src/compiler_recovery_workspace.trb) | Compiler/program recovery orchestration | `compiler_recovery_test.trb`, `compiler_recovery_workspace_test.trb`, `recovery_fixture.trb` |
| [compiler_recovery_workspace_test.trb](../src/compiler_recovery_workspace_test.trb) | Regression tests | Root test discovery |
| [diagnostic.trb](../src/diagnostic.trb) | Shared diagnostics | `aggregate_layout.trb`, `json_boundary.trb`, `native_mir.trb`, `qbe.trb`, `recovery_aggregate_mir.trb`, `recovery_aggregate_qbe.trb`, `recovery_aggregate_snapshot.trb`, `recovery_managed_layout.trb`, `recovery_managed_mir.trb`, `recovery_managed_qbe.trb`, `recovery_managed_snapshot.trb`, `recovery_scalar_mir.trb`, `recovery_scalar_snapshot.trb`, `snapshot.trb`, `snapshot_validation.trb` |
| [json_boundary.trb](../src/json_boundary.trb) | Snapshot validation and shared representation | `recovery_aggregate_snapshot.trb`, `recovery_managed_snapshot.trb`, `recovery_scalar_snapshot.trb` |
| [matched_go_driver.trb](../src/matched_go_driver.trb) | Reference comparison adapter | `compiler_recovery_test.trb`, `matched_go_driver_test.trb`, `recovery_driver.trb` |
| [matched_go_driver_test.trb](../src/matched_go_driver_test.trb) | Regression tests | Root test discovery |
| [native_file_system.trb](../src/native_file_system.trb) | Reference-side test file/process operations | `compiler_recovery_source.trb`, `compiler_recovery_test.trb`, `compiler_recovery_workspace.trb`, `compiler_recovery_workspace_test.trb`, `matched_go_driver.trb`, `native_file_system_test.trb`, `recovery_aggregate_differential_test.trb`, `recovery_aggregate_mir_test.trb`, `recovery_aggregate_snapshot_test.trb`, `recovery_aggregate_toolchain.trb`, `recovery_driver.trb`, `recovery_fixture.trb`, `recovery_generation.trb`, `recovery_managed_aggregate_test.trb`, `recovery_managed_boolean_array_test.trb`, `recovery_managed_capture_test.trb`, `recovery_managed_differential_test.trb`, `recovery_managed_gc_test.trb`, `recovery_managed_integer_array_test.trb`, `recovery_managed_qbe_alias_test.trb`, `recovery_managed_qbe_test.trb`, `recovery_managed_record_array_test.trb`, `recovery_managed_snapshot_test.trb`, `recovery_managed_toolchain.trb`, `recovery_scalar_differential_test.trb`, `recovery_scalar_test.trb`, `recovery_scalar_toolchain.trb`, `snapshot_validation_test.trb` |
| [native_file_system_test.trb](../src/native_file_system_test.trb) | Regression tests | Root test discovery |
| [native_mir.trb](../src/native_mir.trb) | Snapshot validation and shared representation | `recovery_aggregate_mir.trb`, `recovery_aggregate_mir_test.trb`, `recovery_aggregate_snapshot.trb`, `recovery_hash_test.trb`, `recovery_managed_aggregate_test.trb`, `recovery_managed_boolean_array_test.trb`, `recovery_managed_capture_test.trb`, `recovery_managed_gc_test.trb`, `recovery_managed_integer_array_test.trb`, `recovery_managed_mir.trb`, `recovery_managed_mir_test.trb`, `recovery_managed_qbe_alias_test.trb`, `recovery_managed_record_array_test.trb`, `recovery_managed_snapshot.trb`, `recovery_scalar_mir.trb`, `recovery_scalar_snapshot.trb`, `recovery_scalar_test.trb`, `snapshot_validation.trb`, `snapshot_validation_test.trb` |
| [qbe.trb](../src/qbe.trb) | Shared QBE formatting and checked arithmetic | `recovery_aggregate_qbe.trb`, `recovery_hash_runtime.trb`, `recovery_managed_qbe.trb`, `recovery_managed_runtime.trb`, `recovery_scalar_test.trb`, `recovery_scalar_toolchain.trb` |
| [recovery_aggregate_differential_test.trb](../src/recovery_aggregate_differential_test.trb) | Regression tests | Root test discovery |
| [recovery_aggregate_mir.trb](../src/recovery_aggregate_mir.trb) | Heap-free aggregate recovery | `recovery_aggregate_mir_test.trb`, `recovery_aggregate_qbe.trb`, `recovery_aggregate_snapshot.trb`, `recovery_aggregate_toolchain.trb` |
| [recovery_aggregate_mir_test.trb](../src/recovery_aggregate_mir_test.trb) | Regression tests | Root test discovery |
| [recovery_aggregate_qbe.trb](../src/recovery_aggregate_qbe.trb) | Heap-free aggregate recovery | `recovery_aggregate_mir_test.trb`, `recovery_aggregate_snapshot_test.trb`, `recovery_aggregate_toolchain.trb` |
| [recovery_aggregate_snapshot.trb](../src/recovery_aggregate_snapshot.trb) | Heap-free aggregate recovery | `recovery_aggregate_differential_test.trb`, `recovery_aggregate_snapshot_test.trb`, `recovery_driver.trb` |
| [recovery_aggregate_snapshot_test.trb](../src/recovery_aggregate_snapshot_test.trb) | Regression tests | Root test discovery |
| [recovery_aggregate_toolchain.trb](../src/recovery_aggregate_toolchain.trb) | Heap-free aggregate recovery | `recovery_aggregate_differential_test.trb`, `recovery_aggregate_mir_test.trb`, `recovery_aggregate_snapshot_test.trb`, `recovery_driver.trb` |
| [recovery_driver.trb](../src/recovery_driver.trb) | Compiler/program recovery orchestration | Executable or controller entry |
| [recovery_fixture.trb](../src/recovery_fixture.trb) | Compiler/program recovery orchestration | `recovery_hash_test.trb`, `recovery_iteration_test.trb` |
| [recovery_generation.trb](../src/recovery_generation.trb) | Compiler/program recovery orchestration | `compiler_recovery_test.trb`, `recovery_driver.trb` |
| [recovery_hash_runtime.trb](../src/recovery_hash_runtime.trb) | Managed snapshot recovery | `recovery_managed_qbe.trb` |
| [recovery_hash_test.trb](../src/recovery_hash_test.trb) | Regression tests | Root test discovery |
| [recovery_iteration_test.trb](../src/recovery_iteration_test.trb) | Regression tests | Root test discovery |
| [recovery_managed_aggregate_test.trb](../src/recovery_managed_aggregate_test.trb) | Regression tests | Root test discovery |
| [recovery_managed_boolean_array_test.trb](../src/recovery_managed_boolean_array_test.trb) | Regression tests | Root test discovery |
| [recovery_managed_capture_test.trb](../src/recovery_managed_capture_test.trb) | Regression tests | Root test discovery |
| [recovery_managed_differential_test.trb](../src/recovery_managed_differential_test.trb) | Regression tests | Root test discovery |
| [recovery_managed_gc_test.trb](../src/recovery_managed_gc_test.trb) | Regression tests | Root test discovery |
| [recovery_managed_integer_array_test.trb](../src/recovery_managed_integer_array_test.trb) | Regression tests | Root test discovery |
| [recovery_managed_layout.trb](../src/recovery_managed_layout.trb) | Managed snapshot recovery | `recovery_hash_test.trb`, `recovery_managed_aggregate_test.trb`, `recovery_managed_boolean_array_test.trb`, `recovery_managed_capture_test.trb`, `recovery_managed_gc_test.trb`, `recovery_managed_integer_array_test.trb`, `recovery_managed_layout_test.trb`, `recovery_managed_mir.trb`, `recovery_managed_mir_test.trb`, `recovery_managed_qbe.trb`, `recovery_managed_qbe_alias_test.trb`, `recovery_managed_record_array_test.trb`, `recovery_managed_snapshot.trb` |
| [recovery_managed_layout_test.trb](../src/recovery_managed_layout_test.trb) | Regression tests | Root test discovery |
| [recovery_managed_mir.trb](../src/recovery_managed_mir.trb) | Managed snapshot recovery | `recovery_fixture.trb`, `recovery_hash_test.trb`, `recovery_managed_aggregate_test.trb`, `recovery_managed_boolean_array_test.trb`, `recovery_managed_capture_test.trb`, `recovery_managed_gc_test.trb`, `recovery_managed_integer_array_test.trb`, `recovery_managed_mir_test.trb`, `recovery_managed_qbe.trb`, `recovery_managed_qbe_alias_test.trb`, `recovery_managed_record_array_test.trb`, `recovery_managed_snapshot.trb`, `recovery_managed_toolchain.trb` |
| [recovery_managed_mir_test.trb](../src/recovery_managed_mir_test.trb) | Regression tests | Root test discovery |
| [recovery_managed_qbe.trb](../src/recovery_managed_qbe.trb) | Managed snapshot recovery | `recovery_managed_differential_test.trb`, `recovery_managed_qbe_test.trb`, `recovery_managed_toolchain.trb` |
| [recovery_managed_qbe_alias_test.trb](../src/recovery_managed_qbe_alias_test.trb) | Regression tests | Root test discovery |
| [recovery_managed_qbe_test.trb](../src/recovery_managed_qbe_test.trb) | Regression tests | Root test discovery |
| [recovery_managed_record_array_test.trb](../src/recovery_managed_record_array_test.trb) | Regression tests | Root test discovery |
| [recovery_managed_runtime.trb](../src/recovery_managed_runtime.trb) | Managed snapshot recovery | `recovery_managed_qbe.trb` |
| [recovery_managed_snapshot.trb](../src/recovery_managed_snapshot.trb) | Managed snapshot recovery | `compiler_recovery_test.trb`, `recovery_driver.trb`, `recovery_fixture.trb`, `recovery_managed_differential_test.trb`, `recovery_managed_qbe_test.trb`, `recovery_managed_snapshot_test.trb` |
| [recovery_managed_snapshot_test.trb](../src/recovery_managed_snapshot_test.trb) | Regression tests | Root test discovery |
| [recovery_managed_toolchain.trb](../src/recovery_managed_toolchain.trb) | Managed snapshot recovery | `compiler_recovery_test.trb`, `recovery_driver.trb`, `recovery_fixture.trb`, `recovery_managed_aggregate_test.trb`, `recovery_managed_boolean_array_test.trb`, `recovery_managed_capture_test.trb`, `recovery_managed_differential_test.trb`, `recovery_managed_gc_test.trb`, `recovery_managed_integer_array_test.trb`, `recovery_managed_qbe_alias_test.trb`, `recovery_managed_qbe_test.trb`, `recovery_managed_record_array_test.trb` |
| [recovery_scalar_differential_test.trb](../src/recovery_scalar_differential_test.trb) | Regression tests | Root test discovery |
| [recovery_scalar_mir.trb](../src/recovery_scalar_mir.trb) | Scalar snapshot recovery | `aggregate_layout.trb`, `aggregate_layout_test.trb`, `qbe.trb`, `recovery_aggregate_mir.trb`, `recovery_aggregate_mir_test.trb`, `recovery_aggregate_qbe.trb`, `recovery_aggregate_snapshot.trb`, `recovery_hash_test.trb`, `recovery_managed_boolean_array_test.trb`, `recovery_managed_capture_test.trb`, `recovery_managed_gc_test.trb`, `recovery_managed_integer_array_test.trb`, `recovery_managed_layout.trb`, `recovery_managed_layout_test.trb`, `recovery_managed_mir.trb`, `recovery_managed_mir_test.trb`, `recovery_managed_qbe.trb`, `recovery_managed_qbe_alias_test.trb`, `recovery_managed_record_array_test.trb`, `recovery_managed_snapshot.trb`, `recovery_scalar_snapshot.trb`, `recovery_scalar_test.trb`, `recovery_scalar_toolchain.trb` |
| [recovery_scalar_snapshot.trb](../src/recovery_scalar_snapshot.trb) | Scalar snapshot recovery | `recovery_driver.trb`, `recovery_scalar_differential_test.trb`, `recovery_scalar_test.trb` |
| [recovery_scalar_test.trb](../src/recovery_scalar_test.trb) | Regression tests | Root test discovery |
| [recovery_scalar_toolchain.trb](../src/recovery_scalar_toolchain.trb) | Scalar snapshot recovery | `recovery_driver.trb`, `recovery_scalar_differential_test.trb`, `recovery_scalar_test.trb` |
| [snapshot.trb](../src/snapshot.trb) | Snapshot validation and shared representation | `native_mir.trb`, `qbe.trb`, `recovery_aggregate_mir.trb`, `recovery_aggregate_mir_test.trb`, `recovery_aggregate_qbe.trb`, `recovery_aggregate_snapshot.trb`, `recovery_hash_test.trb`, `recovery_managed_aggregate_test.trb`, `recovery_managed_boolean_array_test.trb`, `recovery_managed_capture_test.trb`, `recovery_managed_gc_test.trb`, `recovery_managed_integer_array_test.trb`, `recovery_managed_mir.trb`, `recovery_managed_mir_test.trb`, `recovery_managed_qbe.trb`, `recovery_managed_qbe_alias_test.trb`, `recovery_managed_record_array_test.trb`, `recovery_managed_snapshot.trb`, `recovery_scalar_mir.trb`, `recovery_scalar_snapshot.trb`, `recovery_scalar_test.trb`, `snapshot_validation.trb`, `snapshot_validation_test.trb` |
| [snapshot_validation.trb](../src/snapshot_validation.trb) | Snapshot validation and shared representation | `snapshot_validation_test.trb` |
| [snapshot_validation_test.trb](../src/snapshot_validation_test.trb) | Regression tests | Root test discovery |

Recovery-enabled suites require the pinned reference executable and QBE. Their
workspace receipts enforce cleanup ownership; see [CI validation](ci-validation.md).
Canonical compiler-source derivation validates its exact imports and modules,
while ordinary fixed-point builds always use the file-root closure.
