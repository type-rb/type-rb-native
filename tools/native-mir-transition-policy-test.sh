#!/bin/sh

set -eu

script_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$script_directory/native-mir-transition-policy.sh"

test_root=$(mktemp -d "${TMPDIR:-/tmp}/native-mir-policy.XXXXXX")
trap 'rm -rf "$test_root"' 0
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
candidate=$test_root/candidate
baseline=$test_root/baseline
mkdir -p "$candidate/compiler/gate4" "$baseline/compiler/gate4"
cp "$script_directory/../$NATIVE_MIR_INDUCTION_PHI_MARKER" \
	"$candidate/$NATIVE_MIR_INDUCTION_PHI_MARKER"
cp "$script_directory/../$NATIVE_MIR_ARRAY_REDUCTION_MARKER" \
	"$candidate/$NATIVE_MIR_ARRAY_REDUCTION_MARKER"
cp "$script_directory/../$NATIVE_MIR_ARRAY_LOOP_RECOVERY_MARKER" \
	"$candidate/$NATIVE_MIR_ARRAY_LOOP_RECOVERY_MARKER"
cp "$script_directory/../$NATIVE_MIR_FLOAT_ARRAY_REDUCTION_MARKER" \
	"$candidate/$NATIVE_MIR_FLOAT_ARRAY_REDUCTION_MARKER"
cp "$script_directory/../$NATIVE_MIR_GUARDED_MULTIPLY_MARKER" \
	"$candidate/$NATIVE_MIR_GUARDED_MULTIPLY_MARKER"
cp "$script_directory/../$NATIVE_MIR_GUARDED_ADD_MARKER" \
	"$candidate/$NATIVE_MIR_GUARDED_ADD_MARKER"
cp "$script_directory/../$NATIVE_MIR_STABLE_ARRAY_HEADER_MARKER" \
	"$candidate/$NATIVE_MIR_STABLE_ARRAY_HEADER_MARKER"

test "$(native_mir_target_compiler_limit darwin-arm64-v0)" = 350000
test "$(native_mir_target_compiler_limit linux-arm64-v0)" = 317000
test "$(native_mir_target_compiler_limit linux-amd64-v0)" = 310000
test "$NATIVE_MIR_COMBINED_COMPILER_LIMIT" = 667000
test "$(native_mir_target_text_limit darwin-arm64-v0)" = 250904
test "$(native_mir_target_text_limit linux-arm64-v0)" = 253424
test "$NATIVE_MIR_TARGET_NEUTRAL_QBE_LIMIT" = 1120000
test "$NATIVE_MIR_ARRAY_LOOP_QBE_LIMIT" = 1115000
test "$NATIVE_MIR_ARRAY_LOOP_DARWIN_TEXT_LIMIT" = 250100
test "$NATIVE_MIR_ARRAY_LOOP_LINUX_TEXT_LIMIT" = 253424
test "$NATIVE_MIR_GUARDED_MULTIPLY_QBE_LIMIT" = 52950
test "$NATIVE_MIR_GUARDED_MULTIPLY_SELECTED_CODE_RATIO_LIMIT" = 1.01
test "$NATIVE_MIR_GUARDED_MULTIPLY_SELECTED_RUNTIME_RATIO_LIMIT" = 0.90
test "$NATIVE_MIR_GUARDED_MULTIPLY_CONTROL_RATIO_LIMIT" = 1.02
test "$NATIVE_MIR_GUARDED_ADD_QBE_LIMIT" = 52520
test "$NATIVE_MIR_GUARDED_ADD_SELECTED_CODE_RATIO_LIMIT" = 1.02
test "$NATIVE_MIR_GUARDED_ADD_SELECTED_EXECUTABLE_RATIO_LIMIT" = 1.00
test "$NATIVE_MIR_GUARDED_ADD_SELECTED_RUNTIME_RATIO_LIMIT" = 0.95
test "$NATIVE_MIR_GUARDED_ADD_CONTROL_RATIO_LIMIT" = 1.02
test "$NATIVE_MIR_STABLE_ARRAY_HEADER_QBE_LIMIT" = 52342
test "$NATIVE_MIR_STABLE_ARRAY_HEADER_SELECTED_EXECUTABLE_RATIO_LIMIT" = 1.01
test "$NATIVE_MIR_STABLE_ARRAY_HEADER_SELECTED_RUNTIME_RATIO_LIMIT" = 0.90
test "$NATIVE_MIR_STABLE_ARRAY_HEADER_CONTROL_RATIO_LIMIT" = 1.02
if native_mir_target_compiler_limit unknown-target >/dev/null; then
	exit 1
fi
if native_mir_target_text_limit linux-amd64-v0 >/dev/null; then
	exit 1
fi

cp "$script_directory/../$NATIVE_MIR_FOUNDATION_MARKER" \
	"$candidate/$NATIVE_MIR_FOUNDATION_MARKER"
native_mir_foundation_marker_valid "$candidate"
native_mir_foundation_transition "$candidate" "$baseline"
test "$(native_mir_transition_mode "$candidate" "$baseline")" = foundation-transition
test "$(native_mir_compiler_ratio_limit "$candidate" "$baseline")" = 1.07
test "$(native_mir_build_ratio_limit "$candidate" "$baseline")" = 1.12

cp "$candidate/$NATIVE_MIR_FOUNDATION_MARKER" \
	"$baseline/$NATIVE_MIR_FOUNDATION_MARKER"
if native_mir_foundation_transition "$candidate" "$baseline"; then
	exit 1
fi
cp "$script_directory/../$NATIVE_MIR_SCALAR_CONNECTION_MARKER" \
	"$candidate/$NATIVE_MIR_SCALAR_CONNECTION_MARKER"
native_mir_scalar_connection_marker_valid "$candidate"
native_mir_scalar_connection_transition "$candidate" "$baseline"
test "$(native_mir_transition_mode "$candidate" "$baseline")" = scalar-connection-transition
test "$(native_mir_compiler_ratio_limit "$candidate" "$baseline")" = 1.07
test "$(native_mir_build_ratio_limit "$candidate" "$baseline")" = 1.15

cp "$candidate/$NATIVE_MIR_SCALAR_CONNECTION_MARKER" \
	"$baseline/$NATIVE_MIR_SCALAR_CONNECTION_MARKER"
if native_mir_scalar_connection_transition "$candidate" "$baseline"; then
	exit 1
fi
cp "$script_directory/../$NATIVE_MIR_CONTROL_FLOW_MARKER" \
	"$candidate/$NATIVE_MIR_CONTROL_FLOW_MARKER"
native_mir_transition_markers_valid "$candidate"
native_mir_control_flow_transition "$candidate" "$baseline"
test "$(native_mir_transition_mode "$candidate" "$baseline")" = control-flow-transition
test "$(native_mir_compiler_ratio_limit "$candidate" "$baseline")" = 1.08
test "$(native_mir_build_ratio_limit "$candidate" "$baseline")" = 1.25

cp "$candidate/$NATIVE_MIR_CONTROL_FLOW_MARKER" \
	"$baseline/$NATIVE_MIR_CONTROL_FLOW_MARKER"
if native_mir_control_flow_transition "$candidate" "$baseline"; then
	exit 1
fi
native_mir_array_reduction_marker_valid "$candidate"
native_mir_array_reduction_transition "$candidate" "$baseline"
test "$(native_mir_transition_mode "$candidate" "$baseline")" = array-reduction-transition
test "$(native_mir_compiler_ratio_limit "$candidate" "$baseline")" = 1.05
test "$(native_mir_build_ratio_limit "$candidate" "$baseline")" = 1.05

cp "$candidate/$NATIVE_MIR_ARRAY_REDUCTION_MARKER" \
	"$baseline/$NATIVE_MIR_ARRAY_REDUCTION_MARKER"
if native_mir_array_reduction_transition "$candidate" "$baseline"; then
	exit 1
fi
native_mir_array_loop_recovery_marker_valid "$candidate"
native_mir_array_loop_recovery_transition "$candidate" "$baseline"
test "$(native_mir_transition_mode "$candidate" "$baseline")" = array-loop-recovery-transition
test "$(native_mir_compiler_ratio_limit "$candidate" "$baseline")" = 1.05
test "$(native_mir_build_ratio_limit "$candidate" "$baseline")" = 1.05

cp "$candidate/$NATIVE_MIR_ARRAY_LOOP_RECOVERY_MARKER" \
	"$baseline/$NATIVE_MIR_ARRAY_LOOP_RECOVERY_MARKER"
if native_mir_array_loop_recovery_transition "$candidate" "$baseline"; then
	exit 1
fi
native_mir_float_array_reduction_marker_valid "$candidate"
native_mir_float_array_reduction_transition "$candidate" "$baseline"
test "$(native_mir_transition_mode "$candidate" "$baseline")" = float-array-reduction-transition
test "$(native_mir_compiler_ratio_limit "$candidate" "$baseline")" = 1.05
test "$(native_mir_build_ratio_limit "$candidate" "$baseline")" = 1.05

cp "$candidate/$NATIVE_MIR_FLOAT_ARRAY_REDUCTION_MARKER" \
	"$baseline/$NATIVE_MIR_FLOAT_ARRAY_REDUCTION_MARKER"
if native_mir_float_array_reduction_transition "$candidate" "$baseline"; then
	exit 1
fi
native_mir_guarded_multiply_marker_valid "$candidate"
native_mir_guarded_multiply_transition "$candidate" "$baseline"
test "$(native_mir_transition_mode "$candidate" "$baseline")" = guarded-multiply-transition
test "$(native_mir_compiler_ratio_limit "$candidate" "$baseline")" = 1.05
test "$(native_mir_build_ratio_limit "$candidate" "$baseline")" = 1.05

cp "$candidate/$NATIVE_MIR_GUARDED_MULTIPLY_MARKER" \
	"$baseline/$NATIVE_MIR_GUARDED_MULTIPLY_MARKER"
if native_mir_guarded_multiply_transition "$candidate" "$baseline"; then
	exit 1
fi
native_mir_guarded_add_marker_valid "$candidate"
native_mir_guarded_add_transition "$candidate" "$baseline"
test "$(native_mir_transition_mode "$candidate" "$baseline")" = guarded-add-transition
test "$(native_mir_compiler_ratio_limit "$candidate" "$baseline")" = 1.05
test "$(native_mir_build_ratio_limit "$candidate" "$baseline")" = 1.05

cp "$candidate/$NATIVE_MIR_GUARDED_ADD_MARKER" \
	"$baseline/$NATIVE_MIR_GUARDED_ADD_MARKER"
if native_mir_guarded_add_transition "$candidate" "$baseline"; then
	exit 1
fi
native_mir_stable_array_header_marker_valid "$candidate"
native_mir_stable_array_header_transition "$candidate" "$baseline"
test "$(native_mir_transition_mode "$candidate" "$baseline")" = stable-array-header-transition
test "$(native_mir_compiler_ratio_limit "$candidate" "$baseline")" = 1.05
test "$(native_mir_build_ratio_limit "$candidate" "$baseline")" = 1.05

cp "$candidate/$NATIVE_MIR_STABLE_ARRAY_HEADER_MARKER" \
	"$baseline/$NATIVE_MIR_STABLE_ARRAY_HEADER_MARKER"
if native_mir_stable_array_header_transition "$candidate" "$baseline"; then
	exit 1
fi

native_mir_transition_markers_valid "$candidate"
native_mir_induction_phi_recovery "$candidate" "$baseline"
test "$(native_mir_transition_mode "$candidate" "$baseline")" = ordinary
test "$(native_mir_compiler_ratio_limit "$candidate" "$baseline")" = 1.05
test "$(native_mir_build_ratio_limit "$candidate" "$baseline")" = 1.05

cp "$candidate/$NATIVE_MIR_INDUCTION_PHI_MARKER" \
	"$baseline/$NATIVE_MIR_INDUCTION_PHI_MARKER"
if native_mir_induction_phi_recovery "$candidate" "$baseline"; then
	exit 1
fi

rm -f "$candidate/$NATIVE_MIR_FOUNDATION_MARKER"
if native_mir_foundation_transition "$candidate" "$baseline"; then
	exit 1
fi

printf 'policy=native-mir-foundation-v1\n' \
	> "$candidate/$NATIVE_MIR_FOUNDATION_MARKER"
if native_mir_foundation_marker_valid "$candidate"; then
	exit 1
fi

printf 'policy=native-mir-scalar-connection-v1\n' \
	> "$candidate/$NATIVE_MIR_SCALAR_CONNECTION_MARKER"
if native_mir_scalar_connection_marker_valid "$candidate"; then
	exit 1
fi

printf 'policy=native-mir-control-flow-v1\n' \
	> "$candidate/$NATIVE_MIR_CONTROL_FLOW_MARKER"
if native_mir_control_flow_marker_valid "$candidate"; then
	exit 1
fi

printf 'policy=native-mir-induction-phi-v1\n' \
	> "$candidate/$NATIVE_MIR_INDUCTION_PHI_MARKER"
if native_mir_induction_phi_marker_valid "$candidate"; then
	exit 1
fi

printf 'policy=native-mir-array-reduction-v1\n' \
	> "$candidate/$NATIVE_MIR_ARRAY_REDUCTION_MARKER"
if native_mir_array_reduction_marker_valid "$candidate"; then
	exit 1
fi

printf 'policy=native-mir-array-loop-recovery-v1\n' \
	> "$candidate/$NATIVE_MIR_ARRAY_LOOP_RECOVERY_MARKER"
if native_mir_array_loop_recovery_marker_valid "$candidate"; then
	exit 1
fi

printf 'policy=native-mir-float-array-reduction-v1\n' \
	> "$candidate/$NATIVE_MIR_FLOAT_ARRAY_REDUCTION_MARKER"
if native_mir_float_array_reduction_marker_valid "$candidate"; then
	exit 1
fi

printf 'policy=native-mir-guarded-integer-multiply-v1\n' \
	> "$candidate/$NATIVE_MIR_GUARDED_MULTIPLY_MARKER"
if native_mir_guarded_multiply_marker_valid "$candidate"; then
	exit 1
fi

printf 'policy=native-mir-guarded-integer-add-v1\n' \
	> "$candidate/$NATIVE_MIR_GUARDED_ADD_MARKER"
if native_mir_guarded_add_marker_valid "$candidate"; then
	exit 1
fi

printf 'policy=native-mir-stable-array-header-v1\n' \
	> "$candidate/$NATIVE_MIR_STABLE_ARRAY_HEADER_MARKER"
if native_mir_stable_array_header_marker_valid "$candidate"; then
	exit 1
fi

printf 'native MIR transition policy tests passed\n'
