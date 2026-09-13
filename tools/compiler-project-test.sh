#!/bin/sh

set -eu
script_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$script_directory/compiler-project.sh"
. "$script_directory/native-mir-transition-policy.sh"
test_root=$(mktemp -d "${TMPDIR:-/tmp}/native-compiler-project.XXXXXX")
trap 'rm -r "$test_root"' 0
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

make_project() {
	mkdir -p "$1/src"
	printf 'def main()\n\treturn\nend\n' > "$1/src/compiler.trb"
	printf '{}\n' > "$1/trbconfig.jsonc"
	for marker in "$script_directory"/../compiler/native-mir-*.txt; do
		cp "$marker" "$1/"
	done
}

current=$test_root/current
historical=$test_root/historical
spaced=$test_root/'source with spaces'
make_project "$current/compiler"
make_project "$historical/compiler/gate4"
make_project "$spaced/compiler"
test "$(native_compiler_project_directory "$current")" = "$current/compiler"
test "$(native_compiler_project_directory "$historical")" = "$historical/compiler/gate4"
test "$(native_compiler_project_directory "$spaced")" = "$spaced/compiler"
test "$(cd "$test_root" && native_compiler_project_directory current)" = current/compiler

# An existing historical marker is not a newly introduced allowance, in either
# layout direction. Validate actual marker contents, not just path existence.
for candidate_root in "$current" "$historical"; do
	native_mir_transition_markers_valid "$candidate_root"
	for baseline_root in "$current" "$historical"; do
		test "$(native_mir_transition_mode "$candidate_root" "$baseline_root")" = ordinary
		test "$(native_mir_compiler_ratio_limit "$candidate_root" "$baseline_root")" = 1.05
		test "$(native_mir_build_ratio_limit "$candidate_root" "$baseline_root")" = 1.05
	done
done

assert_rejected() {
	if native_compiler_project_directory "$1" > "$test_root/output" 2> "$test_root/error"; then
		printf '%s\n' 'accepted an invalid project layout' >&2
		exit 1
	fi
	test ! -s "$test_root/output"
	test -s "$test_root/error"
	for operation in native_mir_transition_mode native_mir_compiler_ratio_limit native_mir_build_ratio_limit; do
		if "$operation" "$current" "$1" > "$test_root/output" 2> "$test_root/error"; then
			printf '%s\n' 'interpreted an invalid baseline as a valid policy comparison' >&2
			exit 1
		fi
		test ! -s "$test_root/output"
		if "$operation" "$1" "$current" > "$test_root/output" 2> "$test_root/error"; then
			printf '%s\n' 'interpreted an invalid candidate as a valid policy comparison' >&2
			exit 1
		fi
		test ! -s "$test_root/output"
	done
}

assert_rejected "$test_root/missing"
mkdir -p "$test_root/empty"
assert_rejected "$test_root/empty"
make_project "$test_root/missing-entry/compiler"
rm "$test_root/missing-entry/compiler/src/compiler.trb"
assert_rejected "$test_root/missing-entry"
make_project "$test_root/missing-config/compiler"
rm "$test_root/missing-config/compiler/trbconfig.jsonc"
assert_rejected "$test_root/missing-config"
make_project "$test_root/duplicate/compiler"
make_project "$test_root/duplicate/compiler/gate4"
assert_rejected "$test_root/duplicate"
make_project "$test_root/broken-legacy/compiler"
ln -s missing "$test_root/broken-legacy/compiler/gate4"
assert_rejected "$test_root/broken-legacy"

# A genuinely absent marker in a valid historical source project may select
# its registered transition; an invalid but present marker must not do so.
make_project "$test_root/pre-foundation/compiler/gate4"
rm "$test_root/pre-foundation/compiler/gate4/native-mir-foundation-v1.txt"
test "$(native_mir_transition_mode "$current" "$test_root/pre-foundation")" = foundation-transition
test "$(native_mir_build_ratio_limit "$current" "$test_root/pre-foundation")" = 1.12
printf 'invalid\n' > "$test_root/pre-foundation/compiler/gate4/native-mir-foundation-v1.txt"
test "$(native_mir_transition_mode "$current" "$test_root/pre-foundation")" = ordinary
test "$(native_mir_build_ratio_limit "$current" "$test_root/pre-foundation")" = 1.05
if native_mir_transition_markers_valid "$test_root/pre-foundation"; then
	exit 1
fi
rm "$test_root/pre-foundation/compiler/gate4/native-mir-foundation-v1.txt"
ln -s missing "$test_root/pre-foundation/compiler/gate4/native-mir-foundation-v1.txt"
test "$(native_mir_transition_mode "$current" "$test_root/pre-foundation")" = ordinary
test "$(native_mir_build_ratio_limit "$current" "$test_root/pre-foundation")" = 1.05
printf '%s\n' 'compiler project layout and mixed-baseline policy tests passed'

make_fixture() {
	mkdir -p "$1/configured-project"
	printf '{}\n' > "$1/configured-project/trbconfig.jsonc"
}

make_fixture "$current/corpus/configured-project"
make_fixture "$historical/corpus/gate6k"
make_fixture "$spaced/corpus/configured-project"
test "$(native_configured_fixture_directory "$current")" = "$current/corpus/configured-project/configured-project"
test "$(native_configured_fixture_directory "$historical")" = "$historical/corpus/gate6k/configured-project"
test "$(native_configured_fixture_directory "$spaced")" = "$spaced/corpus/configured-project/configured-project"
test "$(cd "$test_root" && native_configured_fixture_directory historical)" = historical/corpus/gate6k/configured-project

reject_fixture() {
	if native_configured_fixture_directory "$1" > "$test_root/output" 2> "$test_root/error"; then
		printf '%s\n' 'accepted an invalid configured fixture layout' >&2
		exit 1
	fi
	test ! -s "$test_root/output"
	test -s "$test_root/error"
}

reject_fixture "$test_root/missing"
reject_fixture "$test_root/empty"
make_fixture "$test_root/missing-fixture-config/corpus/configured-project"
rm "$test_root/missing-fixture-config/corpus/configured-project/configured-project/trbconfig.jsonc"
reject_fixture "$test_root/missing-fixture-config"
make_fixture "$test_root/duplicate-fixture/corpus/configured-project"
make_fixture "$test_root/duplicate-fixture/corpus/gate6k"
reject_fixture "$test_root/duplicate-fixture"
mkdir -p "$test_root/broken-current-fixture/corpus"
ln -s missing "$test_root/broken-current-fixture/corpus/configured-project"
make_fixture "$test_root/broken-current-fixture/corpus/gate6k"
reject_fixture "$test_root/broken-current-fixture"
make_fixture "$test_root/broken-historical-fixture/corpus/configured-project"
ln -s missing "$test_root/broken-historical-fixture/corpus/gate6k"
reject_fixture "$test_root/broken-historical-fixture"
printf '%s\n' 'configured fixture layout tests passed'
