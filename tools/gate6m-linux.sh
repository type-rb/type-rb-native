#!/bin/sh

set -eu

CANDIDATE_REVISION=97b3ac2aa1d88cbb7782602589ad70686593ddab
TYPE_RB_REVISION=2cf63e95b4fc1a92f6094e2c89c47fb75262adae
TYPE_RB_VERSION=0.4.3-dev
PUBLISHED_SEED_SIZE=241488
PUBLISHED_SEED_SHA256=b4307c244edc9e4da620f2a7c1b03a733e575da032efefae615f9edf75048a37
CANDIDATE_FIXED_POINT_QBE_SHA256=7018b68a348cd73e8268dd2e610e0e82308c58c6bd688266e98b4089f5448d9f
PORTABLE_ENTRY_QBE_SHA256=9e885e1d7dc973e2b28ed04fedf56f166465ac3d00ffb727348c6fc5467763c3
MAX_COMPILER_SIZE=310000

usage() {
	cat >&2 <<'EOF'
usage: gate6m-linux.sh CANDIDATE_ROOT PUBLISHED_SEED QBE CC
       REFERENCE_TRB GO WORKSPACE EVIDENCE OUTPUT_COMPILER
EOF
	exit 64
}

fail() {
	printf 'gate6m-linux: %s\n' "$1" >&2
	exit 1
}

sha256() {
	sha256sum "$1" | awk '{print $1}'
}

file_size() {
	wc -c < "$1" | tr -d ' '
}

require_empty_file() {
	test ! -s "$1" || fail "$2"
}

require_no_intermediates() {
	if find "$1" -name '*.trbn.*' -print | grep . > /dev/null 2>&1; then
		fail "Native build left an intermediate below $1"
	fi
}

require_clean_revision() {
	root=$1
	expected=$2
	label=$3
	test "$(git -C "$root" rev-parse HEAD)" = "$expected" ||
		fail "$label revision differs"
	test -z "$(git -C "$root" status --porcelain)" ||
		fail "$label worktree is not clean"
}

require_successful_command() {
	stdout=$1
	stderr=$2
	label=$3
	shift 3
	"$@" > "$stdout" 2> "$stderr" || fail "$label failed"
	require_empty_file "$stdout" "$label wrote stdout"
	require_empty_file "$stderr" "$label wrote stderr"
}

require_go_build() {
	stdout=$1
	stderr=$2
	expected_stdout=$3
	output=$4
	label=$5
	shift 5
	"$@" > "$stdout" 2> "$stderr" || fail "$label failed"
	printf 'executable -> %s\n' "$output" > "$expected_stdout"
	cmp "$expected_stdout" "$stdout" > /dev/null || fail "$label stdout differs"
	require_empty_file "$stderr" "$label wrote stderr"
	test -x "$output" || fail "$label did not publish an executable"
}

require_forbidden_processes_absent() {
	trace=$1
	label=$2
	if grep -E 'execve\("[^"]*/(go|trb|sh|bash|dash|zsh)"|compiler-recovery' "$trace" > /dev/null; then
		fail "$label launched Go, reference trb, a shell, or a recovery compiler"
	fi
}

require_lld_observed() {
	trace=$1
	label=$2
	grep -E 'execve\("[^"]*/ld\.lld"' "$trace" > /dev/null ||
		fail "$label did not launch ld.lld"
}

test "$#" -eq 9 || usage

candidate_root=$1
published_seed=$2
qbe=$3
cc=$4
reference_trb=$5
go_command=$6
workspace=$7
evidence=$8
output_compiler=$9

script_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
verifier_root=$(CDPATH= cd -- "$script_directory/.." && pwd)

test "$(uname -s)" = Linux || fail "Linux is required"
case "$(uname -m)" in
aarch64 | arm64) ;;
*) fail "Linux arm64 is required" ;;
esac

for command_name in awk cmp cut find git grep jq ld.lld nm readelf sed sha256sum strace strip; do
	command -v "$command_name" > /dev/null 2>&1 || fail "$command_name is required"
done

test -d "$candidate_root" || fail "candidate root does not exist"
test -f "$published_seed" || fail "published seed does not exist"
test -x "$published_seed" || fail "published seed is not executable"
test -x "$qbe" || fail "QBE is not executable"
test -x "$cc" || fail "CC is not executable"
test -x "$reference_trb" || fail "reference trb is not executable"
test -x "$go_command" || fail "Go is not executable"
test "$(command -v go)" = "$go_command" || fail "Go command does not match PATH"
test ! -e "$workspace" || fail "workspace already exists"
test ! -e "$evidence" || fail "evidence path already exists"
test ! -e "$output_compiler" || fail "output compiler already exists"

require_clean_revision "$candidate_root" "$CANDIDATE_REVISION" "Gate 6M candidate"
test "$(tr -d '\n' < "$candidate_root/TYPE_RB_REVISION")" = "$TYPE_RB_REVISION" ||
	fail "candidate TypeRB revision pin differs"
test "$("$reference_trb" version)" = "$TYPE_RB_VERSION" ||
	fail "reference TypeRB version differs"
"$go_command" version > /dev/null 2>&1 || fail "Go toolchain probe failed"
test "$(file_size "$published_seed")" -eq "$PUBLISHED_SEED_SIZE" ||
	fail "published Linux seed size differs"
test "$(sha256 "$published_seed")" = "$PUBLISHED_SEED_SHA256" ||
	fail "published Linux seed digest differs"

compiler_entry=$candidate_root/compiler/gate4/src/compiler.trb
portable_config=$candidate_root/corpus/gate6m/portable-entry/trbconfig.jsonc
portable_source=$candidate_root/corpus/gate6m/portable-entry/src/main.trb
failure_config=$candidate_root/corpus/gate6m/runtime-failures/trbconfig.jsonc
failure_source=$candidate_root/corpus/gate6m/runtime-failures/src/main.trb

test "$(sha256 "$compiler_entry")" = d36afd8dbc399af25087edabfc4505bd4f18442255b0ffbd0b12b28856829727 ||
	fail "candidate compiler entry digest differs"
test "$(sha256 "$portable_config")" = 4b81aaacced57409eeaa8494c45ecba6fd67868f74075e768e287815cf7c6519 ||
	fail "portable-entry config digest differs"
test "$(sha256 "$portable_source")" = 67d89532214e49f0a574cc031f33ca0e91f414a63e3185e274d260f80b243f66 ||
	fail "portable-entry source digest differs"
test "$(sha256 "$failure_config")" = b9511ce4e0c9e6fcc18fbbdddbcbe1645f3701eb7e10fb6ab5be125eb6b288cc ||
	fail "runtime-failure config digest differs"
test "$(sha256 "$failure_source")" = dc9e4ec4667c09fe1392a64b22cad5727568b7b08954d3fc09640847bb60a086 ||
	fail "runtime-failure source digest differs"

mkdir -p \
	"$workspace/setup/first" \
	"$workspace/setup/current-runtime" \
	"$evidence/setup" \
	"$(dirname -- "$output_compiler")"

first_transition=$workspace/setup/first/compiler
runtime_transition=$workspace/setup/current-runtime/compiler

strace -f -e trace=process -o "$evidence/setup/first-process.trace" \
	"$published_seed" build "$compiler_entry" \
		--output "$first_transition" \
		--qbe "$qbe" \
		--cc "$cc" \
		--target linux-arm64-v0 \
		> "$evidence/setup/first.stdout" \
		2> "$evidence/setup/first.stderr" || fail "first setup transition failed"
test -x "$first_transition" || fail "first setup transition did not publish a compiler"
require_empty_file "$evidence/setup/first.stdout" "first setup transition wrote stdout"
require_empty_file "$evidence/setup/first.stderr" "first setup transition wrote stderr"
require_forbidden_processes_absent "$evidence/setup/first-process.trace" "first setup transition"

strace -f -e trace=process -o "$evidence/setup/current-runtime-process.trace" \
	"$first_transition" build "$compiler_entry" \
		--output "$runtime_transition" \
		--qbe "$qbe" \
		--cc "$cc" \
		--target linux-arm64-v0 \
		> "$evidence/setup/current-runtime.stdout" \
		2> "$evidence/setup/current-runtime.stderr" || fail "current-runtime setup transition failed"
test -x "$runtime_transition" || fail "current-runtime setup transition did not publish a compiler"
require_empty_file "$evidence/setup/current-runtime.stdout" "current-runtime setup transition wrote stdout"
require_empty_file "$evidence/setup/current-runtime.stderr" "current-runtime setup transition wrote stderr"
require_forbidden_processes_absent "$evidence/setup/current-runtime-process.trace" "current-runtime setup transition"

{
	grep execve "$evidence/setup/first-process.trace"
	grep execve "$evidence/setup/current-runtime-process.trace"
} > "$evidence/setup/process-inventory.txt"
{
	printf 'published_seed_size=%s\n' "$(file_size "$published_seed")"
	printf 'published_seed_sha256=%s\n' "$(sha256 "$published_seed")"
	printf 'first_transition_size=%s\n' "$(file_size "$first_transition")"
	printf 'first_transition_sha256=%s\n' "$(sha256 "$first_transition")"
	printf 'current_runtime_transition_size=%s\n' "$(file_size "$runtime_transition")"
	printf 'current_runtime_transition_sha256=%s\n' "$(sha256 "$runtime_transition")"
} > "$evidence/setup/identities.txt"

/bin/sh "$verifier_root/tools/bootstrap-seed.sh" \
	--mode previous \
	--input "$runtime_transition" \
	--input-role transition \
	--qbe "$qbe" \
	--cc "$cc" \
	--profile linux-arm64-v0 \
	--runner-image ubuntu-24.04-arm \
	--workspace "$workspace/bootstrap" \
	--output "$output_compiler" \
	--evidence "$evidence/bootstrap" \
	--metadata "$evidence/bootstrap-metadata.json" \
	--asset-name gate6m-candidate-linux-arm64 \
	--repository-root "$candidate_root" \
	> "$evidence/bootstrap.stdout" \
	2> "$evidence/bootstrap.stderr" || fail "candidate compiler chain failed"
printf 'bootstrap-seed: previous linux-arm64-v0 passed\n' > "$evidence/bootstrap.expected"
cmp "$evidence/bootstrap.expected" "$evidence/bootstrap.stdout" > /dev/null ||
	fail "candidate compiler chain stdout differs"
require_empty_file "$evidence/bootstrap.stderr" "candidate compiler chain wrote stderr"
require_lld_observed "$evidence/bootstrap/process.trace" "closed candidate ordinary build"

fixed_point_qbe_sha256=$(awk -F= '$1 == "fixed_point_qbe_sha256" {print $2}' "$evidence/bootstrap/identities.txt")
test "$fixed_point_qbe_sha256" = "$CANDIDATE_FIXED_POINT_QBE_SHA256" ||
	fail "candidate fixed-point QBE digest differs"
compiler_size=$(file_size "$output_compiler")
test "$compiler_size" -le "$MAX_COMPILER_SIZE" || fail "candidate compiler exceeds the size bound"
{
	printf 'platform=linux-arm64\n'
	printf 'raw_compiler_bytes=%s\n' "$compiler_size"
	printf 'raw_compiler_limit_bytes=%s\n' "$MAX_COMPILER_SIZE"
} > "$evidence/compiler-size.txt"

mkdir -p \
	"$workspace/native-first" \
	"$workspace/native-second" \
	"$workspace/native-trace" \
	"$workspace/native-failure" \
	"$workspace/go" \
	"$workspace/go-failure" \
	"$evidence/applications"

native_application=$workspace/native-first/program
native_application_repeat=$workspace/native-second/program
native_application_traced=$workspace/native-trace/program
native_failure_application=$workspace/native-failure/program
go_application=$workspace/go/program
go_failure_application=$workspace/go-failure/program

require_successful_command \
	"$evidence/applications/native-first.stdout" \
	"$evidence/applications/native-first.stderr" \
	"first Native portable-entry build" \
	"$output_compiler" build "$portable_config" \
		--output "$native_application" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
require_successful_command \
	"$evidence/applications/native-second.stdout" \
	"$evidence/applications/native-second.stderr" \
	"repeated Native portable-entry build" \
	"$output_compiler" build "$portable_config" \
		--output "$native_application_repeat" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
cmp "$native_application" "$native_application_repeat" > /dev/null ||
	fail "repeated Native portable-entry bytes differ"

"$output_compiler" emit-qbe "$portable_config" \
	> "$evidence/applications/portable-entry-first.ssa" \
	2> "$evidence/applications/portable-entry-first.stderr" || fail "portable-entry QBE emission failed"
"$output_compiler" emit-qbe "$portable_config" \
	> "$evidence/applications/portable-entry-second.ssa" \
	2> "$evidence/applications/portable-entry-second.stderr" || fail "repeated portable-entry QBE emission failed"
require_empty_file "$evidence/applications/portable-entry-first.stderr" "portable-entry QBE emission wrote stderr"
require_empty_file "$evidence/applications/portable-entry-second.stderr" "repeated portable-entry QBE emission wrote stderr"
cmp "$evidence/applications/portable-entry-first.ssa" "$evidence/applications/portable-entry-second.ssa" > /dev/null ||
	fail "portable-entry QBE is not deterministic"
test "$(sha256 "$evidence/applications/portable-entry-first.ssa")" = "$PORTABLE_ENTRY_QBE_SHA256" ||
	fail "portable-entry QBE digest differs"

require_go_build \
	"$evidence/applications/go.stdout" \
	"$evidence/applications/go.stderr" \
	"$evidence/applications/go.expected" \
	"$go_application" \
	"optimized Go portable-entry build" \
	"$reference_trb" build --compile --config "$portable_config" --outfile "$go_application"

strace -f -e trace=process -o "$evidence/applications/native-build-process.trace" \
	"$output_compiler" build "$portable_config" \
		--output "$native_application_traced" \
		--qbe "$qbe" \
		--cc "$cc" \
		--target linux-arm64-v0 \
		> "$evidence/applications/native-trace.stdout" \
		2> "$evidence/applications/native-trace.stderr" || fail "traced Native portable-entry build failed"
require_empty_file "$evidence/applications/native-trace.stdout" "traced Native portable-entry build wrote stdout"
require_empty_file "$evidence/applications/native-trace.stderr" "traced Native portable-entry build wrote stderr"
require_forbidden_processes_absent "$evidence/applications/native-build-process.trace" "ordinary Native application build"
require_lld_observed "$evidence/applications/native-build-process.trace" "ordinary Native application build"
grep execve "$evidence/applications/native-build-process.trace" \
	> "$evidence/applications/native-build-process-inventory.txt"
cmp "$native_application" "$native_application_traced" > /dev/null ||
	fail "traced Native portable-entry bytes differ"

expected_stdout=$evidence/applications/portable-entry.expected
cat > "$expected_stdout" <<'EOF'
2
1
144
12
0
0
0
9007199254740991
-9007199254740991
-2
nan
EOF

for candidate_pair in "native:$native_application" "go:$go_application"; do
	candidate_label=$(printf '%s\n' "$candidate_pair" | cut -d: -f1)
	executable=$(printf '%s\n' "$candidate_pair" | cut -d: -f2-)
	"$executable" 144 \
		> "$evidence/applications/$candidate_label-runtime.stdout" \
		2> "$evidence/applications/$candidate_label-runtime.stderr" ||
		fail "$candidate_label portable-entry runtime failed"
	cmp "$expected_stdout" "$evidence/applications/$candidate_label-runtime.stdout" > /dev/null ||
		fail "$candidate_label portable-entry stdout differs"
	require_empty_file "$evidence/applications/$candidate_label-runtime.stderr" \
		"$candidate_label portable-entry runtime wrote stderr"
done
cmp "$evidence/applications/native-runtime.stdout" "$evidence/applications/go-runtime.stdout" > /dev/null ||
	fail "Native and Go portable-entry stdout differ"

require_successful_command \
	"$evidence/applications/native-failure-build.stdout" \
	"$evidence/applications/native-failure-build.stderr" \
	"Native runtime-failure build" \
	"$output_compiler" build "$failure_config" \
		--output "$native_failure_application" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
require_go_build \
	"$evidence/applications/go-failure-build.stdout" \
	"$evidence/applications/go-failure-build.stderr" \
	"$evidence/applications/go-failure-build.expected" \
	"$go_failure_application" \
	"optimized Go runtime-failure build" \
	"$reference_trb" build --compile --config "$failure_config" --outfile "$go_failure_application"

printf 'mode,native_status,go_status,failure_class\n' > "$evidence/applications/runtime-failures.csv"
for failure_case in \
	"invalid-format:panic: invalid Integer" \
	"sign-only:panic: invalid Integer" \
	"integer-range:panic: Integer is outside the portable range" \
	"nan:panic: Float cannot be converted to Integer" \
	"infinity:panic: Float cannot be converted to Integer" \
	"float-range:panic: Integer is outside the portable range"; do
	mode=$(printf '%s\n' "$failure_case" | cut -d: -f1)
	expected_class=$(printf '%s\n' "$failure_case" | cut -d: -f2-)
	for candidate_pair in "native:$native_failure_application" "go:$go_failure_application"; do
		candidate_label=$(printf '%s\n' "$candidate_pair" | cut -d: -f1)
		executable=$(printf '%s\n' "$candidate_pair" | cut -d: -f2-)
		set +e
		"$executable" "$mode" \
			> "$evidence/applications/$candidate_label-$mode.stdout" \
			2> "$evidence/applications/$candidate_label-$mode.stderr"
		status=$?
		set -e
		test "$status" -ne 0 || fail "$candidate_label $mode unexpectedly succeeded"
		require_empty_file "$evidence/applications/$candidate_label-$mode.stdout" \
			"$candidate_label $mode wrote stdout"
		actual_class=$(sed -n '1p' "$evidence/applications/$candidate_label-$mode.stderr")
		test "$actual_class" = "$expected_class" ||
			fail "$candidate_label $mode failure class differs"
		if test "$candidate_label" = native; then
			native_status=$status
			native_class=$actual_class
		else
			go_status=$status
			go_class=$actual_class
		fi
	done
	test "$native_class" = "$go_class" || fail "Native and Go $mode failure classes differ"
	printf '%s,%s,%s,%s\n' "$mode" "$native_status" "$go_status" "$native_class" \
		>> "$evidence/applications/runtime-failures.csv"
done

readelf -h "$output_compiler" > "$evidence/compiler-elf-header.txt"
readelf -l "$output_compiler" > "$evidence/compiler-elf-segments.txt"
readelf -d "$output_compiler" > "$evidence/compiler-elf-dependencies.txt"
readelf -h "$native_application" > "$evidence/applications/native-elf-header.txt"
readelf -l "$native_application" > "$evidence/applications/native-elf-segments.txt"
readelf -d "$native_application" > "$evidence/applications/native-elf-dependencies.txt"
nm -u "$native_application" > "$evidence/applications/native-undefined-symbols.txt"
grep -Eq 'Shared library: \[libm\.so' "$evidence/applications/native-elf-dependencies.txt" ||
	fail "Native portable-entry executable does not declare libm"
grep -Eq '(^|[[:space:]])sqrt(@|$)' "$evidence/applications/native-undefined-symbols.txt" ||
	fail "Native portable-entry executable does not retain the external sqrt boundary"

strip --strip-all -o "$workspace/native-first/program.stripped" "$native_application"
strip --strip-all -o "$workspace/go/program.stripped" "$go_application"

{
	printf 'candidate_revision=%s\n' "$CANDIDATE_REVISION"
	printf 'type_rb_revision=%s\n' "$TYPE_RB_REVISION"
	printf 'type_rb_version=%s\n' "$TYPE_RB_VERSION"
	printf 'published_seed_sha256=%s\n' "$(sha256 "$published_seed")"
	printf 'qbe_binary_sha256=%s\n' "$(sha256 "$qbe")"
	printf 'candidate_compiler_sha256=%s\n' "$(sha256 "$output_compiler")"
	printf 'candidate_fixed_point_qbe_sha256=%s\n' "$fixed_point_qbe_sha256"
	printf 'portable_entry_qbe_sha256=%s\n' "$(sha256 "$evidence/applications/portable-entry-first.ssa")"
	printf 'native_application_sha256=%s\n' "$(sha256 "$native_application")"
	printf 'go_application_sha256=%s\n' "$(sha256 "$go_application")"
	printf 'native_application_raw_bytes=%s\n' "$(file_size "$native_application")"
	printf 'native_application_stripped_bytes=%s\n' "$(file_size "$workspace/native-first/program.stripped")"
	printf 'go_application_raw_bytes=%s\n' "$(file_size "$go_application")"
	printf 'go_application_stripped_bytes=%s\n' "$(file_size "$workspace/go/program.stripped")"
} > "$evidence/identities.txt"

{
	printf 'verifier_revision=%s\n' "$(git -C "$verifier_root" rev-parse HEAD)"
	printf 'candidate_revision=%s\n' "$(git -C "$candidate_root" rev-parse HEAD)"
	printf 'profile=linux-arm64-v0\n'
	printf 'runner_image=ubuntu-24.04-arm\n'
	uname -a
	"$reference_trb" version
	"$go_command" version
	"$cc" --version
	ld.lld --version
	"$qbe" -h
} > "$evidence/environment.txt" 2>&1

require_clean_revision "$candidate_root" "$CANDIDATE_REVISION" "Gate 6M candidate after verification"
require_no_intermediates "$workspace"
printf 'gate6m-linux: passed\n'
