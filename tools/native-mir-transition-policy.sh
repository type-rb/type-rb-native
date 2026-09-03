#!/bin/sh

# Frozen by issues #197, #221, #225, #230, #232, #235, #238, #241, and #245 for
# their registered transitions. The allowance is only for the verified MIR
# foundation, scalar connection, and first complete control-flow connection.
# It expires with the complete migration of portable range, index, and
# induction ownership out of the direct emitter.
NATIVE_MIR_FOUNDATION_MARKER=compiler/gate4/native-mir-foundation-v1.txt
NATIVE_MIR_SCALAR_CONNECTION_MARKER=compiler/gate4/native-mir-scalar-connection-v1.txt
NATIVE_MIR_CONTROL_FLOW_MARKER=compiler/gate4/native-mir-control-flow-v1.txt
NATIVE_MIR_INDUCTION_PHI_MARKER=compiler/gate4/native-mir-induction-phi-v1.txt
NATIVE_MIR_ARRAY_REDUCTION_MARKER=compiler/gate4/native-mir-array-reduction-v1.txt
NATIVE_MIR_ARRAY_LOOP_RECOVERY_MARKER=compiler/gate4/native-mir-array-loop-recovery-v1.txt
NATIVE_MIR_FLOAT_ARRAY_REDUCTION_MARKER=compiler/gate4/native-mir-float-array-reduction-v1.txt
NATIVE_MIR_GUARDED_MULTIPLY_MARKER=compiler/gate4/native-mir-guarded-integer-multiply-v1.txt
NATIVE_MIR_GUARDED_ADD_MARKER=compiler/gate4/native-mir-guarded-integer-add-v1.txt
NATIVE_MIR_STABLE_ARRAY_HEADER_MARKER=compiler/gate4/native-mir-stable-array-header-v1.txt
NATIVE_MIR_DARWIN_COMPILER_LIMIT=350000
NATIVE_MIR_LINUX_COMPILER_LIMIT=317000
# Linux amd64 remains below its pre-existing ceiling; the control-flow
# envelope does not grant that target any additional space.
NATIVE_MIR_LINUX_AMD64_COMPILER_LIMIT=310000
NATIVE_MIR_COMBINED_COMPILER_LIMIT=667000
NATIVE_MIR_DARWIN_TEXT_LIMIT=250904
NATIVE_MIR_LINUX_TEXT_LIMIT=253424
NATIVE_MIR_TARGET_NEUTRAL_QBE_LIMIT=1120000
NATIVE_MIR_ARRAY_LOOP_QBE_LIMIT=1115000
NATIVE_MIR_ARRAY_LOOP_DARWIN_TEXT_LIMIT=250100
NATIVE_MIR_ARRAY_LOOP_LINUX_TEXT_LIMIT=253424
NATIVE_MIR_GUARDED_MULTIPLY_QBE_LIMIT=52950
NATIVE_MIR_GUARDED_MULTIPLY_SELECTED_CODE_RATIO_LIMIT=1.01
NATIVE_MIR_GUARDED_MULTIPLY_SELECTED_RUNTIME_RATIO_LIMIT=0.90
NATIVE_MIR_GUARDED_MULTIPLY_CONTROL_RATIO_LIMIT=1.02
NATIVE_MIR_GUARDED_ADD_QBE_LIMIT=52520
NATIVE_MIR_GUARDED_ADD_SELECTED_CODE_RATIO_LIMIT=1.02
NATIVE_MIR_GUARDED_ADD_SELECTED_EXECUTABLE_RATIO_LIMIT=1.00
NATIVE_MIR_GUARDED_ADD_SELECTED_RUNTIME_RATIO_LIMIT=0.95
NATIVE_MIR_GUARDED_ADD_CONTROL_RATIO_LIMIT=1.02
NATIVE_MIR_STABLE_ARRAY_HEADER_QBE_LIMIT=52342
NATIVE_MIR_STABLE_ARRAY_HEADER_SELECTED_EXECUTABLE_RATIO_LIMIT=1.01
NATIVE_MIR_STABLE_ARRAY_HEADER_SELECTED_RUNTIME_RATIO_LIMIT=0.90
NATIVE_MIR_STABLE_ARRAY_HEADER_CONTROL_RATIO_LIMIT=1.02
NATIVE_MIR_FOUNDATION_COMPILER_RATIO_LIMIT=1.07
NATIVE_MIR_FOUNDATION_BUILD_RATIO_LIMIT=1.12
NATIVE_MIR_SCALAR_CONNECTION_COMPILER_RATIO_LIMIT=1.07
NATIVE_MIR_SCALAR_CONNECTION_BUILD_RATIO_LIMIT=1.15
NATIVE_MIR_CONTROL_FLOW_COMPILER_RATIO_LIMIT=1.08
NATIVE_MIR_CONTROL_FLOW_BUILD_RATIO_LIMIT=1.25
NATIVE_MIR_ORDINARY_RATIO_LIMIT=1.05
NATIVE_MIR_RSS_RATIO_LIMIT=1.05
NATIVE_MIR_CATASTROPHIC_RATIO_LIMIT=2.0

native_mir_foundation_marker_valid() {
	native_mir_marker=$1/$NATIVE_MIR_FOUNDATION_MARKER
	test -f "$native_mir_marker" &&
		test "$(grep -Fxc 'policy=native-mir-foundation-v1' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'baseline_revision=a36c7417f0c9bc5bc9705c28ef6340a05caa5f27' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'measured_compiled_revision=f1dabd9d14867709fb36e9d43cacb43d5e05644d' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'phase_a_run=33593947594' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'darwin_arm64_fixed_compiler_bytes=299656' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'linux_arm64_fixed_compiler_bytes=271744' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'combined_fixed_compiler_bytes=571400' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'temporary_allowance_bytes_per_target=17000' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'recovery_family=portable-range-index-induction' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'recovery_before=next-portable-fact-family' "$native_mir_marker")" -eq 1
}

native_mir_scalar_connection_marker_valid() {
	native_mir_marker=$1/$NATIVE_MIR_SCALAR_CONNECTION_MARKER
	test -f "$native_mir_marker" &&
		test "$(grep -Fxc 'policy=native-mir-scalar-connection-v1' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'baseline_revision=0d7b41ed8767df97c74a5a6b52a6b2fa550e495f' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'measured_compiled_revision=465ba67f9b3eaa0a2b3cd0472992a6eb2d2c4ca4' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'phase_a_run=33672358939' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'darwin_arm64_fixed_compiler_bytes=316184' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'linux_arm64_fixed_compiler_bytes=289440' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'combined_fixed_compiler_bytes=605624' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'darwin_arm64_compiler_limit=317000' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'linux_arm64_compiler_limit=290000' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'combined_compiler_limit=607000' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'transition_compiler_ratio_limit=1.07' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'transition_build_ratio_limit=1.15' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'rss_ratio_limit=1.05' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'catastrophic_ratio_limit=2.0' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'superseded_ownership=scalar-token-eligibility-and-leaf-emission' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'recovery_family=portable-range-index-induction' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'recovery_before=next-portable-fact-family' "$native_mir_marker")" -eq 1
}

native_mir_control_flow_marker_valid() {
	native_mir_marker=$1/$NATIVE_MIR_CONTROL_FLOW_MARKER
	test -f "$native_mir_marker" &&
		test "$(grep -Fxc 'policy=native-mir-control-flow-v1' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'baseline_revision=2a4120d2115ecf3c6b0139f8873658cca55e829f' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'measured_compiled_revision=06d406c275c47c6c52eba3f1fb24e489a6e777a9' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'phase_a_run=33681594415' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'darwin_arm64_fixed_compiler_bytes=332696' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'linux_arm64_fixed_compiler_bytes=308656' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'linux_amd64_fixed_compiler_bytes=268008' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'combined_fixed_compiler_bytes=641352' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'darwin_arm64_compiler_limit=334000' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'linux_arm64_compiler_limit=310000' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'linux_amd64_compiler_limit=310000' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'combined_compiler_limit=644000' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'transition_compiler_ratio_limit=1.08' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'transition_build_ratio_limit=1.25' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'rss_ratio_limit=1.05' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'catastrophic_ratio_limit=2.0' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'superseded_ownership=array-induction-helper-token-facts-and-emission' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'recovery_family=portable-range-index-induction' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'recovery_before=next-portable-fact-family' "$native_mir_marker")" -eq 1
}

native_mir_induction_phi_marker_valid() {
	native_mir_marker=$1/$NATIVE_MIR_INDUCTION_PHI_MARKER
	test -f "$native_mir_marker" &&
		test "$(grep -Fxc 'policy=native-mir-induction-phi-v1' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'baseline_revision=58836d6177cfa32d32fcb17805f37149de2dc49a' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'diagnostic_revision=746be6fafeb181b92776fc24c887031f80d2dcaa' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_baseline_text_bytes=243648' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_candidate_text_bytes=243568' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'baseline_target_neutral_qbe_bytes=1089635' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'diagnostic_target_neutral_qbe_bytes=1089474' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'complete_compiler_signal=no-growth-per-bounded-slice' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'code_section_signal=strict-shrink-per-arm64-target' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'cumulative_recovery=complete-compiler-artifacts-shrink-before-family-completion' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'recovery_family=portable-range-index-induction' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'recovery_before=next-portable-fact-family' "$native_mir_marker")" -eq 1
}

native_mir_array_reduction_marker_valid() {
	native_mir_marker=$1/$NATIVE_MIR_ARRAY_REDUCTION_MARKER
	test -f "$native_mir_marker" &&
		test "$(grep -Fxc 'policy=native-mir-array-reduction-v1' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'baseline_revision=9dcae126e036d335344907ed4ea091a7f11a2198' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'compiler_source_sha256=e04072866919cc4bc36c51601103e8c0e76a8bb282071a5f3a56d839cafc6f89' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'compiler_test_source_sha256=6e7270182cfed988a3dbe6528eea9538d19a897264ead710f0a1112741d6622b' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'darwin_arm64_fixed_compiler_bytes=349232' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'linux_arm64_fixed_compiler_bytes=314544' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'combined_fixed_compiler_bytes=663776' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'target_neutral_qbe_bytes=1112077' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'target_neutral_qbe_sha256=8067fe279941819eb7b3a788cbb0fee9ec33e8e8c1aaec0e6a53f7bc43d36207' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'darwin_arm64_text_bytes=249488' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'linux_arm64_text_bytes=252032' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'darwin_arm64_compiler_limit=350000' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'linux_arm64_compiler_limit=317000' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'combined_compiler_limit=667000' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'target_neutral_qbe_limit=1120000' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'transition_compiler_ratio_limit=1.05' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'transition_build_ratio_limit=1.05' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'rss_ratio_limit=1.05' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'catastrophic_ratio_limit=2.0' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'superseded_ownership=array-reduction-token-control-and-mutable-stack-emission' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'recovery_family=portable-range-index-induction' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'recovery_before=next-portable-fact-family' "$native_mir_marker")" -eq 1
}

native_mir_array_loop_recovery_marker_valid() {
	native_mir_marker=$1/$NATIVE_MIR_ARRAY_LOOP_RECOVERY_MARKER
	test -f "$native_mir_marker" &&
		test "$(grep -Fxc 'policy=native-mir-array-loop-recovery-v1' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'baseline_revision=05a35fc355fa5e08cea1c0bfb2ea0face0864746' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'compiler_source_sha256=94d37d0ff9b3d9eade169e52579805e985d322edc78cf220c10dedc2ea84d211' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'compiler_test_source_sha256=9948921b2df5daae631ee9885a892d8ff5e044bce5ff8cd6c2238f612cd6d89b' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'workload_sha256=8d44d0c770dddf80fcf28a59be23ca357ca6ad6239fd00973e1291e7646537ca' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'expected_stdout_sha256=9fd097355fb6760a1f6b0a5ebb7648aff35896da9dccaeea40e03f72eaa94ece' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_baseline_compiler_bytes=349224' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_candidate_compiler_bytes=349224' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'baseline_target_neutral_qbe_bytes=1112077' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_candidate_target_neutral_qbe_bytes=1110700' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_baseline_text_bytes=249488' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_candidate_text_bytes=249280' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'target_neutral_qbe_limit=1115000' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'darwin_arm64_text_limit=250100' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'linux_arm64_text_limit=253424' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'runtime_wall_ratio_limit=0.75' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'runtime_cpu_ratio_limit=0.75' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'runtime_rss_ratio_limit=1.05' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'catastrophic_ratio_limit=2.0' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'complete_compiler_signal=no-growth-per-arm64-target' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'generated_qbe_signal=strict-shrink' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'generated_code_section_signal=strict-shrink-per-arm64-target' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'superseded_ownership=qbe-array-header-bounds-and-induction-check-decisions' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'recovery_family=portable-range-index-induction' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'recovery_before=next-portable-fact-family' "$native_mir_marker")" -eq 1
}

native_mir_float_array_reduction_marker_valid() {
	native_mir_marker=$1/$NATIVE_MIR_FLOAT_ARRAY_REDUCTION_MARKER
	test -f "$native_mir_marker" &&
		test "$(grep -Fxc 'policy=native-mir-float-array-reduction-v1' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'baseline_revision=833fa2d22272a12e080bbce34de33054eefe43aa' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'compiler_source_sha256=4692bcfdf0999afcace96c2bbf6af4b70fa0b9c1e4a960d9e4cb527afa7f1078' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'compiler_test_source_sha256=f3f02da96678361a680c40d96c9cf32f23cf3b0f29113414cace7c47d05c4028' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'measure_source_sha256=033322b2f5deec71b50d77d6f5b6628da65524b490c75591cf49080d69b7764c' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'hot_workload_sha256=b9ae59064616fca0135746108cb21fc684cd8eda89c3c616e920c7707c70b982' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'hot_expected_stdout_sha256=420002158111bff8adb3347d84029e480f45e60e1869b454b6adac3345f9f7d4' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'streaming_workload_sha256=fa9ae5f333a314ac509ea8ba1578b36f2008d8d3e0ece27bccda83624794a0fd' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'streaming_expected_stdout_sha256=cae66fe5c887c748f61eb482722559bba8b3e960fff741c840c5bbb19ead7fd7' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'empty_source_sha256=93111736a86d9732d8fda6c21fbe67ad52ac8491e1abe432a1410d2a8d424b2e' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'empty_expected_stdout_sha256=9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'nonfinite_source_sha256=135ba9118480879b412401fad424e7f16288d1cbc45a2dc8e6d36f53cb1fc0c3' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'nonfinite_expected_stderr_sha256=f0eab2436850da43b2aa44124ff3c5f549827d783991eb3200bb343f7627882b' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'unsupported_source_sha256=7f91ce71b2cc025446422dca71fe04d71f356783a4ac38e9231b8c83c17238af' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'unsupported_expected_stdout_sha256=2451e722f881c88d56d145dd4d7953045b2798fb9a0beee6319b8ebbfdd47873' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_baseline_compiler_bytes=349224' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_candidate_compiler_bytes=349224' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'baseline_target_neutral_qbe_bytes=1110700' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_candidate_target_neutral_qbe_bytes=1110817' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_baseline_text_bytes=249280' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_candidate_text_bytes=249172' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'target_neutral_qbe_limit=1115000' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'darwin_arm64_text_limit=250100' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'linux_arm64_text_limit=253424' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'hot_runtime_wall_ratio_limit=0.75' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'hot_runtime_cpu_ratio_limit=0.75' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'streaming_runtime_wall_ratio_limit=0.90' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'streaming_runtime_cpu_ratio_limit=0.90' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'runtime_rss_ratio_limit=1.05' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'catastrophic_ratio_limit=2.0' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'complete_compiler_signal=no-growth-per-arm64-target' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'generated_qbe_signal=strict-shrink-per-workload' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'generated_code_section_signal=strict-shrink-per-workload-and-arm64-target' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'superseded_ownership=float-array-reduction-direct-stack-and-check-emission' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'recovery_family=portable-range-index-induction' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'recovery_before=next-portable-fact-family' "$native_mir_marker")" -eq 1
}

native_mir_guarded_multiply_marker_valid() {
	native_mir_marker=$1/$NATIVE_MIR_GUARDED_MULTIPLY_MARKER
	test -f "$native_mir_marker" &&
		test "$(grep -Fxc 'policy=native-mir-guarded-integer-multiply-v1' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'baseline_revision=538742551ac1c6d030e772abd49a273e6cb783eb' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'first_hosted_compiler_source_sha256=9ebc687c285bd3693be0f1d8dc7e48f6de0ee783d57771e4467da6857d53a9e8' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'first_hosted_linux_arm64_candidate_compiler_bytes=315336' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'replacement_reason=first-hosted-candidate-exceeded-no-growth' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'compiler_source_sha256=0a7c221de131df6159443eaea5c908bae5973e0368abfe6cfeaac09dcc96c75d' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'compiler_test_source_sha256=baf0bec7c802c0aa34a2e54c71fe5a9ce1787dfa7bfc2f415c92f996bc2ac9e4' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'valid_source_sha256=96faedf7c940df525cfcf2eacb654088dad5e83f06936c1257c0f5c63739158b' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'valid_expected_stdout_sha256=0985f550314d08663a0d829b2bf6cb8fe671b2e81d9b77f535165696de6801f8' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'overflow_source_sha256=b8772c170dc3cadd3c227fe664295c15aff6e839694ae5737d44c6f4b430cfe0' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'overflow_expected_stderr_sha256=a8e248bcb823b1d6710097f5c88b63fc79c73fa052aefcde3c468cc69d10edec' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'measure_source_sha256=f03adc024300e0be5d8304ebd1000a5a390d9f8acaceadf3c10375643e27a45e' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'spectral_source_sha256=b85e0d8cecf4e7455bdd34a6a02cb3a9a6e7bbe57ec29bb2f1b99afbbb5312f2' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'spectral_expected_stdout_sha256=f9d5b5e3eb7657cf1bbba4cc856651864df9cd9fd9a6be9b9bc5fcbb67150deb' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'fannkuch_source_sha256=6fa788a62edda1755f05bf493f0cebe9903b97be176359b9ceeadea0b1bef92d' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'fannkuch_expected_stdout_sha256=4265a65135c506a68d90d6474003fb9030b7ee244a06c046bd89b3932a28ce20' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'nbody_source_sha256=796fc08a4747102e1ca08fc75cb81cb0a69b65666c11e45baeafcae2a1064b20' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'nbody_expected_stdout_sha256=3e6c9ef9d26cfe312a4cd8e1b81b3f671b88fbce84de543e8c23c206a942504d' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_baseline_compiler_bytes=349224' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_candidate_compiler_bytes=349224' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'baseline_target_neutral_qbe_bytes=1110817' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_candidate_target_neutral_qbe_bytes=1109629' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_baseline_spectral_qbe_bytes=52272' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_candidate_spectral_qbe_bytes=52520' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_baseline_spectral_text_bytes=10620' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_candidate_spectral_text_bytes=10684' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'target_neutral_qbe_limit=1115000' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'spectral_qbe_limit=52950' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'darwin_arm64_text_limit=250100' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'linux_arm64_text_limit=253424' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'selected_code_section_ratio_limit=1.01' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'selected_runtime_wall_ratio_limit=0.90' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'selected_runtime_cpu_ratio_limit=0.90' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'control_code_section_ratio_limit=1.02' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'control_runtime_wall_ratio_limit=1.02' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'control_runtime_cpu_ratio_limit=1.02' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'runtime_rss_ratio_limit=1.05' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'catastrophic_ratio_limit=2.0' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'complete_compiler_signal=no-growth-per-arm64-target' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'superseded_ownership=loop-local-checked-integer-multiply-helper-selection' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'recovery_family=portable-range-index-induction' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'recovery_before=next-portable-fact-family' "$native_mir_marker")" -eq 1
}

native_mir_guarded_add_marker_valid() {
	native_mir_marker=$1/$NATIVE_MIR_GUARDED_ADD_MARKER
	test -f "$native_mir_marker" &&
		test "$(grep -Fxc 'policy=native-mir-guarded-integer-add-v1' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'baseline_revision=b82d30f4986aa289cedb7bb3392002019bc549f8' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'first_hosted_compiler_source_sha256=77dd9290f43705e0135c136bf58f8148223d75e6062c03624f05efe69c5e4e59' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'first_hosted_linux_arm64_candidate_compiler_bytes=314848' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'replacement_reason=first-hosted-candidate-exceeded-no-growth' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'second_hosted_compiler_source_sha256=8b03fdd9f88645981eea147c5d7627b250ef6b5ccc6b5277742e7567599d30af' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'second_hosted_linux_arm64_candidate_compiler_bytes=313424' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'second_hosted_linux_arm64_baseline_spectral_executable_bytes=19744' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'second_hosted_linux_arm64_candidate_spectral_executable_bytes=19872' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'second_replacement_reason=selected-linux-executable-exceeded-no-growth' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'third_hosted_compiler_source_sha256=1b8d3adf443a1b6574c3d48b8ece7639338bded9763136952da73dbae18a7c4c' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'third_hosted_linux_arm64_candidate_compiler_bytes=313320' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'third_hosted_selected_wall_ratio=0.9574107988170045' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'third_hosted_selected_cpu_ratio=0.9574217854202888' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'third_replacement_reason=selected-runtime-missed-five-percent-improvement' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'compiler_source_sha256=1837220fa4c2e39796ebfa7df54ec89e64d97b3e81f3a385c5c0e88525a4e863' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'compiler_test_source_sha256=5161674fb0f05bce3334b9938b3497b0e521cf9deb17443e50a8cc36bcdcf891' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'valid_source_sha256=8900e0581feb661f13bd7056d7aa43bf2c83f83a8d44d29afa2ca47b9744ef8c' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'valid_expected_stdout_sha256=d0167719b266092d77a3ce397f144c77def07868c731dc8d88e225120af154f6' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'overflow_source_sha256=efa2ff79bc8b61d1f1bb464fb5e1ed361092c6c19aa8d1ff5f5832e17a8e4531' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'overflow_expected_stderr_sha256=a8e248bcb823b1d6710097f5c88b63fc79c73fa052aefcde3c468cc69d10edec' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'measure_source_sha256=f03adc024300e0be5d8304ebd1000a5a390d9f8acaceadf3c10375643e27a45e' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'spectral_source_sha256=b85e0d8cecf4e7455bdd34a6a02cb3a9a6e7bbe57ec29bb2f1b99afbbb5312f2' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'spectral_expected_stdout_sha256=f9d5b5e3eb7657cf1bbba4cc856651864df9cd9fd9a6be9b9bc5fcbb67150deb' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'fannkuch_source_sha256=6fa788a62edda1755f05bf493f0cebe9903b97be176359b9ceeadea0b1bef92d' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'fannkuch_expected_stdout_sha256=4265a65135c506a68d90d6474003fb9030b7ee244a06c046bd89b3932a28ce20' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'nbody_source_sha256=796fc08a4747102e1ca08fc75cb81cb0a69b65666c11e45baeafcae2a1064b20' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'nbody_expected_stdout_sha256=3e6c9ef9d26cfe312a4cd8e1b81b3f671b88fbce84de543e8c23c206a942504d' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_baseline_compiler_bytes=349224' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_candidate_compiler_bytes=349200' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_baseline_compiler_text_bytes=248716' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_candidate_compiler_text_bytes=248192' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_linux_arm64_candidate_compiler_bytes=313224' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_linux_arm64_candidate_compiler_text_bytes=250720' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'baseline_target_neutral_qbe_bytes=1109629' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_candidate_target_neutral_qbe_bytes=1108565' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_baseline_spectral_qbe_bytes=52520' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_candidate_spectral_qbe_bytes=52343' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_baseline_spectral_text_bytes=10684' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_candidate_spectral_text_bytes=10732' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_baseline_spectral_executable_bytes=55656' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_candidate_spectral_executable_bytes=50984' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_linux_arm64_candidate_spectral_text_bytes=11360' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_linux_arm64_candidate_spectral_executable_bytes=19616' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'linux_linker_compactness=no-eh-frame-header' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'target_neutral_qbe_limit=1115000' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'spectral_qbe_limit=52520' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'darwin_arm64_text_limit=250100' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'linux_arm64_text_limit=253424' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'selected_code_section_ratio_limit=1.02' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'selected_executable_ratio_limit=1.00' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'selected_runtime_wall_ratio_limit=0.95' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'selected_runtime_cpu_ratio_limit=0.95' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'control_code_section_ratio_limit=1.02' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'control_executable_ratio_limit=1.02' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'control_runtime_wall_ratio_limit=1.02' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'control_runtime_cpu_ratio_limit=1.02' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'runtime_rss_ratio_limit=1.05' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'catastrophic_ratio_limit=2.0' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'complete_compiler_signal=no-growth-per-arm64-target' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'superseded_ownership=loop-local-checked-integer-add-helper-selection' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'recovery_family=portable-range-index-induction' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'recovery_before=next-portable-fact-family' "$native_mir_marker")" -eq 1
}

native_mir_stable_array_header_marker_valid() {
	native_mir_marker=$1/$NATIVE_MIR_STABLE_ARRAY_HEADER_MARKER
	test -f "$native_mir_marker" &&
		test "$(grep -Fxc 'policy=native-mir-stable-array-header-v1' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'baseline_revision=00009fa304a36b9cba70b123120a469347b3882d' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'compiler_source_sha256=1304342068fa3507e3817c8cbe6b7d88cba70cca338880d6ef2ef0ca70a45f3a' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'compiler_test_source_sha256=d3edc5d720079b32fc3b673277cf507b550e68bfa2e61c76b7603054802ed0a8' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'valid_source_sha256=194afa0b18286c3555010bf63827a5b7da6c40d1abf8816347ed16e8be2ccdaf' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'valid_expected_stdout_sha256=7ab27073a8c012277824faf4e80bed5760f565ec435cc04bb82749baa122b1d8' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'measure_source_sha256=f03adc024300e0be5d8304ebd1000a5a390d9f8acaceadf3c10375643e27a45e' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'spectral_source_sha256=b85e0d8cecf4e7455bdd34a6a02cb3a9a6e7bbe57ec29bb2f1b99afbbb5312f2' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'spectral_expected_stdout_sha256=f9d5b5e3eb7657cf1bbba4cc856651864df9cd9fd9a6be9b9bc5fcbb67150deb' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'fannkuch_source_sha256=6fa788a62edda1755f05bf493f0cebe9903b97be176359b9ceeadea0b1bef92d' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'fannkuch_expected_stdout_sha256=4265a65135c506a68d90d6474003fb9030b7ee244a06c046bd89b3932a28ce20' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'nbody_source_sha256=796fc08a4747102e1ca08fc75cb81cb0a69b65666c11e45baeafcae2a1064b20' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'nbody_expected_stdout_sha256=3e6c9ef9d26cfe312a4cd8e1b81b3f671b88fbce84de543e8c23c206a942504d' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_baseline_compiler_bytes=349200' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_candidate_compiler_bytes=349208' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_candidate_compiler_text_bytes=250508' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'baseline_target_neutral_qbe_bytes=1108565' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_candidate_target_neutral_qbe_bytes=1117994' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_baseline_spectral_qbe_bytes=52343' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_candidate_spectral_qbe_bytes=52219' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_baseline_spectral_text_bytes=10732' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_candidate_spectral_text_bytes=10668' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_baseline_spectral_executable_bytes=50984' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_darwin_arm64_candidate_spectral_executable_bytes=51000' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_selected_wall_ratio=0.845114' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_selected_cpu_ratio=0.845031' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'local_selected_rss_ratio=1.000000' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'darwin_arm64_compiler_limit=350000' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'linux_arm64_compiler_limit=317000' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'target_neutral_qbe_limit=1120000' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'darwin_arm64_text_limit=250904' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'linux_arm64_text_limit=253424' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'spectral_qbe_limit=52342' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'selected_executable_ratio_limit=1.01' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'selected_runtime_wall_ratio_limit=0.90' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'selected_runtime_cpu_ratio_limit=0.90' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'selected_runtime_rss_ratio_limit=1.05' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'control_ratio_limit=1.02' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'compiler_build_ratio_limit=1.05' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'catastrophic_ratio_limit=2.0' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'superseded_ownership=direct-emitter-array-header-cache-and-bounds-selection' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'recovery_family=portable-range-index-induction' "$native_mir_marker")" -eq 1 &&
		test "$(grep -Fxc 'recovery_before=next-portable-fact-family' "$native_mir_marker")" -eq 1
}

native_mir_transition_markers_valid() {
	native_mir_foundation_marker_valid "$1" &&
		native_mir_scalar_connection_marker_valid "$1" &&
		native_mir_control_flow_marker_valid "$1" &&
		native_mir_induction_phi_marker_valid "$1" &&
		native_mir_array_reduction_marker_valid "$1" &&
		native_mir_array_loop_recovery_marker_valid "$1" &&
		native_mir_float_array_reduction_marker_valid "$1" &&
		native_mir_guarded_multiply_marker_valid "$1" &&
		native_mir_guarded_add_marker_valid "$1" &&
		native_mir_stable_array_header_marker_valid "$1"
}

native_mir_target_compiler_limit() {
	case "$1" in
	darwin-arm64-v0) printf '%s\n' "$NATIVE_MIR_DARWIN_COMPILER_LIMIT" ;;
	linux-arm64-v0) printf '%s\n' "$NATIVE_MIR_LINUX_COMPILER_LIMIT" ;;
	linux-amd64-v0) printf '%s\n' "$NATIVE_MIR_LINUX_AMD64_COMPILER_LIMIT" ;;
	*) return 1 ;;
	esac
}

native_mir_target_text_limit() {
	case "$1" in
	darwin-arm64-v0) printf '%s\n' "$NATIVE_MIR_DARWIN_TEXT_LIMIT" ;;
	linux-arm64-v0) printf '%s\n' "$NATIVE_MIR_LINUX_TEXT_LIMIT" ;;
	*) return 1 ;;
	esac
}

native_mir_foundation_transition() {
	native_mir_candidate_root=$1
	native_mir_baseline_root=$2
	native_mir_foundation_marker_valid "$native_mir_candidate_root" &&
		test ! -f "$native_mir_baseline_root/$NATIVE_MIR_FOUNDATION_MARKER"
}

native_mir_scalar_connection_transition() {
	native_mir_candidate_root=$1
	native_mir_baseline_root=$2
	native_mir_scalar_connection_marker_valid "$native_mir_candidate_root" &&
		test ! -f "$native_mir_baseline_root/$NATIVE_MIR_SCALAR_CONNECTION_MARKER"
}

native_mir_control_flow_transition() {
	native_mir_candidate_root=$1
	native_mir_baseline_root=$2
	native_mir_control_flow_marker_valid "$native_mir_candidate_root" &&
		test ! -f "$native_mir_baseline_root/$NATIVE_MIR_CONTROL_FLOW_MARKER"
}

native_mir_induction_phi_recovery() {
	native_mir_candidate_root=$1
	native_mir_baseline_root=$2
	native_mir_induction_phi_marker_valid "$native_mir_candidate_root" &&
		test ! -f "$native_mir_baseline_root/$NATIVE_MIR_INDUCTION_PHI_MARKER"
}

native_mir_array_reduction_transition() {
	native_mir_candidate_root=$1
	native_mir_baseline_root=$2
	native_mir_array_reduction_marker_valid "$native_mir_candidate_root" &&
		test ! -f "$native_mir_baseline_root/$NATIVE_MIR_ARRAY_REDUCTION_MARKER"
}

native_mir_array_loop_recovery_transition() {
	native_mir_candidate_root=$1
	native_mir_baseline_root=$2
	native_mir_array_loop_recovery_marker_valid "$native_mir_candidate_root" &&
		test ! -f "$native_mir_baseline_root/$NATIVE_MIR_ARRAY_LOOP_RECOVERY_MARKER"
}

native_mir_float_array_reduction_transition() {
	native_mir_candidate_root=$1
	native_mir_baseline_root=$2
	native_mir_float_array_reduction_marker_valid "$native_mir_candidate_root" &&
		test ! -f "$native_mir_baseline_root/$NATIVE_MIR_FLOAT_ARRAY_REDUCTION_MARKER"
}

native_mir_guarded_multiply_transition() {
	native_mir_candidate_root=$1
	native_mir_baseline_root=$2
	native_mir_guarded_multiply_marker_valid "$native_mir_candidate_root" &&
		test ! -f "$native_mir_baseline_root/$NATIVE_MIR_GUARDED_MULTIPLY_MARKER"
}

native_mir_guarded_add_transition() {
	native_mir_candidate_root=$1
	native_mir_baseline_root=$2
	native_mir_guarded_add_marker_valid "$native_mir_candidate_root" &&
		test ! -f "$native_mir_baseline_root/$NATIVE_MIR_GUARDED_ADD_MARKER"
}

native_mir_stable_array_header_transition() {
	native_mir_candidate_root=$1
	native_mir_baseline_root=$2
	native_mir_stable_array_header_marker_valid "$native_mir_candidate_root" &&
		test ! -f "$native_mir_baseline_root/$NATIVE_MIR_STABLE_ARRAY_HEADER_MARKER"
}

native_mir_transition_mode() {
	if native_mir_foundation_transition "$1" "$2"; then
		printf '%s\n' foundation-transition
	else
		if native_mir_scalar_connection_transition "$1" "$2"; then
			printf '%s\n' scalar-connection-transition
		else
			if native_mir_control_flow_transition "$1" "$2"; then
				printf '%s\n' control-flow-transition
			else
				if native_mir_array_reduction_transition "$1" "$2"; then
					printf '%s\n' array-reduction-transition
				else
					if native_mir_array_loop_recovery_transition "$1" "$2"; then
						printf '%s\n' array-loop-recovery-transition
					else
						if native_mir_float_array_reduction_transition "$1" "$2"; then
							printf '%s\n' float-array-reduction-transition
						else
							if native_mir_guarded_multiply_transition "$1" "$2"; then
								printf '%s\n' guarded-multiply-transition
							else
								if native_mir_guarded_add_transition "$1" "$2"; then
									printf '%s\n' guarded-add-transition
								else
									if native_mir_stable_array_header_transition "$1" "$2"; then
										printf '%s\n' stable-array-header-transition
									else
										printf '%s\n' ordinary
									fi
								fi
							fi
						fi
					fi
				fi
			fi
		fi
	fi
}

native_mir_compiler_ratio_limit() {
	if native_mir_foundation_transition "$1" "$2"; then
		printf '%s\n' "$NATIVE_MIR_FOUNDATION_COMPILER_RATIO_LIMIT"
	else
		if native_mir_scalar_connection_transition "$1" "$2"; then
			printf '%s\n' "$NATIVE_MIR_SCALAR_CONNECTION_COMPILER_RATIO_LIMIT"
		else
			if native_mir_control_flow_transition "$1" "$2"; then
				printf '%s\n' "$NATIVE_MIR_CONTROL_FLOW_COMPILER_RATIO_LIMIT"
			else
				printf '%s\n' "$NATIVE_MIR_ORDINARY_RATIO_LIMIT"
			fi
		fi
	fi
}

native_mir_build_ratio_limit() {
	if native_mir_foundation_transition "$1" "$2"; then
		printf '%s\n' "$NATIVE_MIR_FOUNDATION_BUILD_RATIO_LIMIT"
	else
		if native_mir_scalar_connection_transition "$1" "$2"; then
			printf '%s\n' "$NATIVE_MIR_SCALAR_CONNECTION_BUILD_RATIO_LIMIT"
		else
			if native_mir_control_flow_transition "$1" "$2"; then
				printf '%s\n' "$NATIVE_MIR_CONTROL_FLOW_BUILD_RATIO_LIMIT"
			else
				printf '%s\n' "$NATIVE_MIR_ORDINARY_RATIO_LIMIT"
			fi
		fi
	fi
}
