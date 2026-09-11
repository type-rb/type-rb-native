#!/bin/sh

set -eu

script_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$script_directory/compiler-project.sh"
. "$script_directory/native-mir-transition-policy.sh"

test_root=$(mktemp -d "${TMPDIR:-/tmp}/native-mir-policy.XXXXXX")
trap 'rm -rf "$test_root"' 0
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
candidate=$test_root/candidate
baseline=$test_root/baseline
mkdir -p "$candidate/compiler/src" "$baseline/compiler/src"
: > "$candidate/compiler/src/compiler.trb"
: > "$candidate/compiler/trbconfig.jsonc"
: > "$baseline/compiler/src/compiler.trb"
: > "$baseline/compiler/trbconfig.jsonc"
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

test "$(native_mir_target_compiler_limit darwin-arm64-v0)" = 417000
test "$(native_mir_target_compiler_limit linux-arm64-v0)" = 388000
test "$(native_mir_target_compiler_limit linux-amd64-v0)" = 332000
test "$NATIVE_MIR_COMBINED_COMPILER_LIMIT" = 805000
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

# Ordinary Hash-capable successors do not receive a feature-transition allowance.
mkdir -p "$test_root/ordinary/compiler/src"
printf '{}\n' > "$test_root/ordinary/compiler/trbconfig.jsonc"
: > "$test_root/ordinary/compiler/src/compiler.trb"
test "$(native_mir_transition_mode "$test_root/ordinary" "$test_root/ordinary")" = ordinary
test "$(native_mir_compiler_ratio_limit "$test_root/ordinary" "$test_root/ordinary")" = 1.05
test "$(native_mir_build_ratio_limit "$test_root/ordinary" "$test_root/ordinary")" = 1.05
printf '%s\n' 'Ordinary compiler policy checks passed'

# Test filesystem cleanliness with a real isolated Git project. Documentation
# changes do not change compiler inputs; dirty, staged and extra source do.
source_tree=$test_root/source-tree
mkdir -p "$source_tree/compiler/src"
printf '{}\n' > "$source_tree/compiler/trbconfig.jsonc"
printf 'def main()\nend\n' > "$source_tree/compiler/src/compiler.trb"
git -C "$source_tree" init -q
git -C "$source_tree" add compiler
git -C "$source_tree" -c user.name=Test -c user.email=test@example.invalid -c commit.gpgsign=false commit -qm initial
source_identity=$(git -C "$source_tree" rev-parse HEAD:compiler/src)
test "$(native_mir_clean_compiler_tree "$source_tree")" = "$source_identity"
printf 'note\n' > "$source_tree/note.md"
test "$(native_mir_clean_compiler_tree "$source_tree")" = "$source_identity"
printf '# change\n' >> "$source_tree/compiler/src/compiler.trb"
if native_mir_clean_compiler_tree "$source_tree" >/dev/null; then exit 1; fi
git -C "$source_tree" add compiler/src/compiler.trb
if native_mir_clean_compiler_tree "$source_tree" >/dev/null; then exit 1; fi
git -C "$source_tree" restore --source=HEAD --staged --worktree compiler/src/compiler.trb
printf 'extra\n' > "$source_tree/compiler/src/extra.trb"
if native_mir_clean_compiler_tree "$source_tree" >/dev/null; then exit 1; fi
printf 'extra.trb\n' > "$source_tree/.gitignore"
if native_mir_clean_compiler_tree "$source_tree" >/dev/null; then exit 1; fi
rm "$source_tree/compiler/src/extra.trb"
test "$(native_mir_clean_compiler_tree "$source_tree")" = "$source_identity"
if native_mir_clean_compiler_tree "$source_tree/compiler" >/dev/null; then exit 1; fi
if native_mir_clean_compiler_tree "$test_root/ordinary" >/dev/null; then exit 1; fi

# Isolate the exact identity selector from Git. No production environment
# override or mutable marker can supply these identities.
(
 native_mir_clean_compiler_tree() {
  case "$1" in
   "$test_root/ordinary/candidate") printf '%s\n' bc4cdfd82560401970e07ef7ef965d8bdb22b612 ;;
   "$test_root/ordinary/control") printf '%s\n' 47e078f2d8b38429e52935db8a46c00ccb5a6efb ;;
   *) return 1 ;;
  esac
 }
 for role in candidate control other; do
  mkdir -p "$test_root/ordinary/$role/compiler/src"
  printf '{}\n' > "$test_root/ordinary/$role/compiler/trbconfig.jsonc"
  : > "$test_root/ordinary/$role/compiler/src/compiler.trb"
 done
 pair_candidate=$test_root/ordinary/candidate
 pair_control=$test_root/ordinary/control
 for profile in darwin-arm64-v0 linux-arm64-v0; do
  test "$(native_mir_build_ratio_limit "$pair_candidate" "$pair_control" "$profile")" = 1.08
 done
 for profile in linux-amd64-v0 unknown ''; do
  test "$(native_mir_build_ratio_limit "$pair_candidate" "$pair_control" "$profile")" = 1.05
 done
 test "$(native_mir_build_ratio_limit "$pair_candidate" "$pair_control")" = 1.05
 test "$(native_mir_build_ratio_limit "$pair_control" "$pair_candidate" linux-arm64-v0)" = 1.05
 test "$(native_mir_build_ratio_limit "$pair_candidate" "$pair_candidate" linux-arm64-v0)" = 1.05
 test "$(native_mir_build_ratio_limit "$test_root/ordinary/other" "$pair_control" linux-arm64-v0)" = 1.05
 test "$(native_mir_build_ratio_limit "$pair_candidate" "$test_root/ordinary/other" linux-arm64-v0)" = 1.05
 test "$(native_mir_compiler_ratio_limit "$pair_candidate" "$pair_control")" = 1.05
)
printf '%s\n' 'Source-bound Array self-build policy checks passed'
