#!/bin/sh

# Frozen by issue #197 after Phase A run 33593947594. The allowance is only
# for the verified MIR foundation and expires with the complete migration of
# portable range, index, and induction ownership out of the direct emitter.
NATIVE_MIR_FOUNDATION_MARKER=compiler/gate4/native-mir-foundation-v1.txt
NATIVE_MIR_DARWIN_COMPILER_LIMIT=302000
NATIVE_MIR_LINUX_COMPILER_LIMIT=272000
NATIVE_MIR_COMBINED_COMPILER_LIMIT=574000
NATIVE_MIR_FOUNDATION_COMPILER_RATIO_LIMIT=1.07
NATIVE_MIR_FOUNDATION_BUILD_RATIO_LIMIT=1.12
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

native_mir_target_compiler_limit() {
	case "$1" in
	darwin-arm64-v0) printf '%s\n' "$NATIVE_MIR_DARWIN_COMPILER_LIMIT" ;;
	linux-arm64-v0) printf '%s\n' "$NATIVE_MIR_LINUX_COMPILER_LIMIT" ;;
	*) return 1 ;;
	esac
}

native_mir_foundation_transition() {
	native_mir_candidate_root=$1
	native_mir_baseline_root=$2
	native_mir_foundation_marker_valid "$native_mir_candidate_root" &&
		test ! -f "$native_mir_baseline_root/$NATIVE_MIR_FOUNDATION_MARKER"
}

native_mir_compiler_ratio_limit() {
	if native_mir_foundation_transition "$1" "$2"; then
		printf '%s\n' "$NATIVE_MIR_FOUNDATION_COMPILER_RATIO_LIMIT"
	else
		printf '%s\n' "$NATIVE_MIR_ORDINARY_RATIO_LIMIT"
	fi
}

native_mir_build_ratio_limit() {
	if native_mir_foundation_transition "$1" "$2"; then
		printf '%s\n' "$NATIVE_MIR_FOUNDATION_BUILD_RATIO_LIMIT"
	else
		printf '%s\n' "$NATIVE_MIR_ORDINARY_RATIO_LIMIT"
	fi
}
