#!/bin/sh

# Frozen by issues #197, #221, and #225 after their measurement runs. The
# allowance is only for the verified MIR foundation, scalar connection, and
# first complete control-flow connection. It expires with the complete
# migration of portable range, index, and induction ownership out of the
# direct emitter.
NATIVE_MIR_FOUNDATION_MARKER=compiler/gate4/native-mir-foundation-v1.txt
NATIVE_MIR_SCALAR_CONNECTION_MARKER=compiler/gate4/native-mir-scalar-connection-v1.txt
NATIVE_MIR_CONTROL_FLOW_MARKER=compiler/gate4/native-mir-control-flow-v1.txt
NATIVE_MIR_DARWIN_COMPILER_LIMIT=334000
NATIVE_MIR_LINUX_COMPILER_LIMIT=310000
# Linux amd64 remains below its pre-existing ceiling; the control-flow
# envelope does not grant that target any additional space.
NATIVE_MIR_LINUX_AMD64_COMPILER_LIMIT=310000
NATIVE_MIR_COMBINED_COMPILER_LIMIT=644000
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

native_mir_transition_markers_valid() {
	native_mir_foundation_marker_valid "$1" &&
		native_mir_scalar_connection_marker_valid "$1" &&
		native_mir_control_flow_marker_valid "$1"
}

native_mir_target_compiler_limit() {
	case "$1" in
	darwin-arm64-v0) printf '%s\n' "$NATIVE_MIR_DARWIN_COMPILER_LIMIT" ;;
	linux-arm64-v0) printf '%s\n' "$NATIVE_MIR_LINUX_COMPILER_LIMIT" ;;
	linux-amd64-v0) printf '%s\n' "$NATIVE_MIR_LINUX_AMD64_COMPILER_LIMIT" ;;
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
				printf '%s\n' ordinary
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
