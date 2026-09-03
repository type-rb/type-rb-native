#!/bin/sh

# Frozen by issues #197, #221, #225, #230, #232, and #235 after their measurement runs. The
# allowance is only for the verified MIR foundation, scalar connection, and
# first complete control-flow connection. It expires with the complete
# migration of portable range, index, and induction ownership out of the
# direct emitter.
NATIVE_MIR_FOUNDATION_MARKER=compiler/gate4/native-mir-foundation-v1.txt
NATIVE_MIR_SCALAR_CONNECTION_MARKER=compiler/gate4/native-mir-scalar-connection-v1.txt
NATIVE_MIR_CONTROL_FLOW_MARKER=compiler/gate4/native-mir-control-flow-v1.txt
NATIVE_MIR_INDUCTION_PHI_MARKER=compiler/gate4/native-mir-induction-phi-v1.txt
NATIVE_MIR_ARRAY_REDUCTION_MARKER=compiler/gate4/native-mir-array-reduction-v1.txt
NATIVE_MIR_ARRAY_LOOP_RECOVERY_MARKER=compiler/gate4/native-mir-array-loop-recovery-v1.txt
NATIVE_MIR_FLOAT_ARRAY_REDUCTION_MARKER=compiler/gate4/native-mir-float-array-reduction-v1.txt
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

native_mir_transition_markers_valid() {
	native_mir_foundation_marker_valid "$1" &&
		native_mir_scalar_connection_marker_valid "$1" &&
		native_mir_control_flow_marker_valid "$1" &&
		native_mir_induction_phi_marker_valid "$1" &&
		native_mir_array_reduction_marker_valid "$1" &&
		native_mir_array_loop_recovery_marker_valid "$1" &&
		native_mir_float_array_reduction_marker_valid "$1"
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
							printf '%s\n' ordinary
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
