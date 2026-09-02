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

test "$(native_mir_target_compiler_limit darwin-arm64-v0)" = 334000
test "$(native_mir_target_compiler_limit linux-arm64-v0)" = 310000
test "$(native_mir_target_compiler_limit linux-amd64-v0)" = 310000
test "$NATIVE_MIR_COMBINED_COMPILER_LIMIT" = 644000
if native_mir_target_compiler_limit unknown-target >/dev/null; then
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
test "$(native_mir_transition_mode "$candidate" "$baseline")" = ordinary
test "$(native_mir_compiler_ratio_limit "$candidate" "$baseline")" = 1.05
test "$(native_mir_build_ratio_limit "$candidate" "$baseline")" = 1.05

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

printf 'native MIR transition policy tests passed\n'
