#!/bin/sh

# Frozen by issues #197, #221, #225, and #230 after their measurement runs. The
# allowance is only for the verified MIR foundation, scalar connection, and
# first complete control-flow connection. It expires with the complete
# migration of portable range, index, and induction ownership out of the
# direct emitter.
NATIVE_MIR_FOUNDATION_MARKER=compiler/gate4/native-mir-foundation-v1.txt
NATIVE_MIR_SCALAR_CONNECTION_MARKER=compiler/gate4/native-mir-scalar-connection-v1.txt
NATIVE_MIR_CONTROL_FLOW_MARKER=compiler/gate4/native-mir-control-flow-v1.txt
NATIVE_MIR_INDUCTION_PHI_MARKER=compiler/gate4/native-mir-induction-phi-v1.txt
NATIVE_MIR_ARRAY_REDUCTION_MARKER=compiler/gate4/native-mir-array-reduction-v1.txt
NATIVE_MIR_DARWIN_COMPILER_LIMIT=350000
NATIVE_MIR_LINUX_COMPILER_LIMIT=317000
# Linux amd64 remains below its pre-existing ceiling; the control-flow
# envelope does not grant that target any additional space.
NATIVE_MIR_LINUX_AMD64_COMPILER_LIMIT=310000
NATIVE_MIR_COMBINED_COMPILER_LIMIT=667000
NATIVE_MIR_DARWIN_TEXT_LIMIT=250904
NATIVE_MIR_LINUX_TEXT_LIMIT=253424
NATIVE_MIR_TARGET_NEUTRAL_QBE_LIMIT=1120000
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

native_mir_transition_markers_valid() {
	native_mir_foundation_marker_valid "$1" &&
		native_mir_scalar_connection_marker_valid "$1" &&
		native_mir_control_flow_marker_valid "$1" &&
		native_mir_induction_phi_marker_valid "$1" &&
		native_mir_array_reduction_marker_valid "$1"
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
					printf '%s\n' ordinary
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
