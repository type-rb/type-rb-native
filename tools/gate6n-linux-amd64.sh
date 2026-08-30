#!/bin/sh

set -eu

PRE_IMPLEMENTATION_REVISION=266c996668a4c3e0ad6eb833ca646b73ca7e56e1
TYPE_RB_REVISION=2cf63e95b4fc1a92f6094e2c89c47fb75262adae
TYPE_RB_VERSION=0.4.3-dev
ROOT_QBE_SIZE=658639
ROOT_QBE_SHA256=62db3c31527a670c3050051a9fa27bf142b6c5deaab81ef8234104bd467aa95a
MAX_COMPILER_SIZE=310000
PROFILE=linux-amd64-v0
RUNNER_IMAGE=ubuntu-24.04

usage() {
	cat >&2 <<'EOF'
usage: gate6n-linux-amd64.sh CANDIDATE_ROOT ROOT_QBE QBE CC
       REFERENCE_TRB GO WORKSPACE EVIDENCE OUTPUT_COMPILER
EOF
	exit 64
}

fail() {
	printf 'gate6n-linux-amd64: %s\n' "$1" >&2
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
	if find "$1" \( -name '*.trbn.*' -o -name '*.gate6n-external.*' \) -print |
		grep . > /dev/null 2>&1; then
		fail "Native build left an intermediate below $1"
	fi
}

require_clean_revision() {
	root=$1
	label=$2
	test -n "$(git -C "$root" rev-parse HEAD)" || fail "$label has no revision"
	test -z "$(git -C "$root" status --porcelain)" || fail "$label worktree is not clean"
}

require_forbidden_processes_absent() {
	trace=$1
	label=$2
	if grep -E 'execve\("[^"]*/(go|trb|sh|bash|dash|zsh)"|compiler-recovery' "$trace" > /dev/null; then
		fail "$label launched Go, reference trb, a shell, or a recovery generator"
	fi
}

require_tool_observed() {
	trace=$1
	pattern=$2
	label=$3
	grep -E "$pattern" "$trace" > /dev/null || fail "$label was not observed"
}

require_exact_tool_observed() {
	trace=$1
	tool=$2
	label=$3
	grep -F "execve(\"$tool\"" "$trace" > /dev/null || fail "$label was not observed at $tool"
}

require_closed_ordinary_trace() {
	trace=$1
	compiler=$2
	label=$3
	inventory=$trace.executables
	sed -n 's/.*execve("\([^"]*\)".*/\1/p' "$trace" > "$inventory"
	test -s "$inventory" || fail "$label process inventory is empty"
	while IFS= read -r executable; do
		case "$executable" in
		"$compiler" | "$qbe" | "$cc" | */cc1 | */collect2 | */as | */x86_64-linux-gnu-as | */ld.lld) ;;
		*) fail "$label launched an unregistered executable: $executable" ;;
		esac
	done < "$inventory"
	require_exact_tool_observed "$trace" "$qbe" "$label QBE"
	require_exact_tool_observed "$trace" "$cc" "$label CC"
	require_tool_observed "$trace" 'execve\("[^"]*/(as|x86_64-linux-gnu-as)"' "$label assembler"
	require_tool_observed "$trace" 'execve\("[^"]*/ld\.lld"' "$label LLD"
	require_forbidden_processes_absent "$trace" "$label"
	if grep -F -- '--source-content' "$trace" > /dev/null; then
		fail "$label used the hidden source-content adapter"
	fi
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
	expected=$3
	output=$4
	label=$5
	shift 5
	"$@" > "$stdout" 2> "$stderr" || fail "$label failed"
	printf 'executable -> %s\n' "$output" > "$expected"
	cmp "$expected" "$stdout" > /dev/null || fail "$label stdout differs"
	require_empty_file "$stderr" "$label wrote stderr"
	test -x "$output" || fail "$label did not publish an executable"
}

test "$#" -eq 9 || usage

candidate_root=$1
root_qbe=$2
qbe=$3
cc=$4
reference_trb=$5
go_command=$6
workspace=$7
evidence=$8
output_compiler=$9

script_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
verifier_root=$(CDPATH= cd -- "$script_directory/.." && pwd)
external_recipe=$verifier_root/tools/gate6n-external-build.sh

test "$(uname -s)" = Linux || fail "Linux is required"
case "$(uname -m)" in
x86_64 | amd64) ;;
*) fail "Linux amd64 is required" ;;
esac

for command_name in awk cmp cut date file find git grep jq ld.lld ldd nm readelf sed sha256sum strace strings strip; do
	command -v "$command_name" > /dev/null 2>&1 || fail "$command_name is required"
done

run_formal_evidence() {
record_native_elf() {
	label=$1
	executable=$2
	directory=$evidence/elf/$label
	mkdir -p "$directory"
	file "$executable" > "$directory/file.txt"
	readelf -W -h "$executable" > "$directory/header.txt"
	readelf -W -l "$executable" > "$directory/segments.txt"
	readelf -W -S "$executable" > "$directory/sections.txt"
	readelf -W -d "$executable" > "$directory/dependencies.txt"
	readelf -W -n "$executable" > "$directory/notes.txt"
	readelf -W -s "$executable" > "$directory/symbols.txt"
	nm -D -u "$executable" > "$directory/undefined-symbols.txt"
	ldd "$executable" > "$directory/ldd.txt"
	strings -a "$executable" > "$directory/strings.txt"

	grep -Eq 'Class:[[:space:]]+ELF64' "$directory/header.txt" || fail "$label is not ELF64"
	grep -Eq 'Machine:[[:space:]]+Advanced Micro Devices X86-64' "$directory/header.txt" ||
		fail "$label is not x86-64"
	grep -Eq 'Type:[[:space:]]+DYN' "$directory/header.txt" || fail "$label is not a PIE executable"
	grep -Eq 'INTERP' "$directory/segments.txt" || fail "$label has no ELF interpreter"
	grep -Eq 'GNU_RELRO' "$directory/segments.txt" || fail "$label has no GNU_RELRO segment"
	stack_count=$(awk '$1 == "GNU_STACK" {count += 1} END {print count + 0}' "$directory/segments.txt")
	test "$stack_count" -eq 1 || fail "$label does not have exactly one GNU_STACK segment"
	if awk '$1 == "GNU_STACK" && $(NF - 1) ~ /E/ {found = 1} END {exit !found}' \
		"$directory/segments.txt"; then
		fail "$label requests an executable stack"
	fi
	if grep -Eq '\.go\.buildinfo|\.note\.go\.buildid' "$directory/sections.txt"; then
		fail "$label contains a Go build-information section"
	fi
	set +e
	"$go_command" version -m "$executable" \
		> "$directory/go-version-m.stdout" \
		2> "$directory/go-version-m.stderr"
	go_metadata_status=$?
	set -e
	printf '%s\n' "$go_metadata_status" > "$directory/go-version-m.status"
	test "$go_metadata_status" -ne 0 || fail "$label unexpectedly contains Go build metadata"
}

record_native_elf compiler "$output_compiler"
record_native_elf portable-entry "$native_application"
grep -Eq 'Shared library: \[libm\.so' "$evidence/elf/portable-entry/dependencies.txt" ||
	fail "Native portable-entry executable does not declare libm"
grep -Eq '(^|[[:space:]])sqrt(@|$)' "$evidence/elf/portable-entry/undefined-symbols.txt" ||
	fail "Native portable-entry executable does not retain the external sqrt boundary"

mkdir -p "$evidence/go-elf"
file "$go_application" > "$evidence/go-elf/file.txt"
readelf -W -h "$go_application" > "$evidence/go-elf/header.txt"
readelf -W -l "$go_application" > "$evidence/go-elf/segments.txt"
readelf -W -S "$go_application" > "$evidence/go-elf/sections.txt"
readelf -W -n "$go_application" > "$evidence/go-elf/notes.txt"
set +e
readelf -W -d "$go_application" > "$evidence/go-elf/dependencies.txt" 2> "$evidence/go-elf/dependencies.stderr"
go_dynamic_status=$?
ldd "$go_application" > "$evidence/go-elf/ldd.txt" 2> "$evidence/go-elf/ldd.stderr"
go_ldd_status=$?
set -e
printf '%s\n' "$go_dynamic_status" > "$evidence/go-elf/dependencies.status"
printf '%s\n' "$go_ldd_status" > "$evidence/go-elf/ldd.status"
"$go_command" version -m "$go_application" \
	> "$evidence/go-elf/go-version-m.stdout" \
	2> "$evidence/go-elf/go-version-m.stderr" || fail "optimized Go metadata probe failed"

measurements=$evidence/measurements.csv
measurement_logs=$evidence/measurement-logs
mkdir -p "$measurement_logs"
printf 'stage,candidate,iteration,elapsed_seconds,peak_rss_bytes,status\n' > "$measurements"

measure_command() {
	stage=$1
	candidate=$2
	iteration=$3
	shift 3
	log_prefix=$measurement_logs/$stage-$candidate-$iteration
	started=$(date +%s%N)
	set +e
	/usr/bin/time -f '%M' -o "$log_prefix.rss-kib" \
		"$@" > "$log_prefix.stdout" 2> "$log_prefix.stderr"
	measurement_status=$?
	set -e
	finished=$(date +%s%N)
	measurement_elapsed=$(awk -v started="$started" -v finished="$finished" \
		'BEGIN { printf "%.9f", (finished - started) / 1000000000 }')
	rss_kib=$(tr -d '[:space:]' < "$log_prefix.rss-kib")
	case "$rss_kib" in
	'' | *[!0-9]*) measurement_rss=0 ;;
	*) measurement_rss=$((rss_kib * 1024)) ;;
	esac
	printf '%s,%s,%s,%s,%s,%s\n' \
		"$stage" "$candidate" "$iteration" "$measurement_elapsed" "$measurement_rss" "$measurement_status" \
		>> "$measurements"
}

require_measurement_success() {
	label=$1
	test "$measurement_status" -eq 0 || fail "$label failed with status $measurement_status"
	test "$measurement_rss" -gt 0 || fail "$label did not report peak RSS"
}

compiler_native_directory=$workspace/measured-compiler-native
compiler_external_directory=$workspace/measured-compiler-external
mkdir -p "$compiler_native_directory" "$compiler_external_directory"
compiler_native_output=$compiler_native_directory/compiler
compiler_external_output=$compiler_external_directory/compiler

round=0
while test "$round" -lt 9; do
	if test "$round" -lt 2; then
		iteration=$((round - 2))
	else
		iteration=$((round - 1))
	fi
	order='native external'
	if test $((round % 2)) -ne 0; then
		order='external native'
	fi
	for candidate in $order; do
		if test "$candidate" = native; then
			measure_command compiler-build native "$iteration" \
				"$output_compiler" build "$compiler_entry" \
					--output "$compiler_native_output" \
					--qbe "$qbe" --cc "$cc" --target "$PROFILE"
			require_measurement_success "Native compiler build observation $iteration"
			require_empty_file "$measurement_logs/compiler-build-native-$iteration.stdout" \
				"Native compiler build observation $iteration wrote stdout"
			require_empty_file "$measurement_logs/compiler-build-native-$iteration.stderr" \
				"Native compiler build observation $iteration wrote stderr"
			cmp "$output_compiler" "$compiler_native_output" > /dev/null ||
				fail "Native measured compiler bytes differ at observation $iteration"
		else
			measure_command compiler-build external "$iteration" \
				/bin/sh "$external_recipe" "$output_compiler" "$compiler_entry" \
				"$compiler_external_output" "$qbe" "$cc"
			require_measurement_success "external compiler recipe observation $iteration"
			require_empty_file "$measurement_logs/compiler-build-external-$iteration.stdout" \
				"external compiler recipe observation $iteration wrote stdout"
			require_empty_file "$measurement_logs/compiler-build-external-$iteration.stderr" \
				"external compiler recipe observation $iteration wrote stderr"
			cmp "$output_compiler" "$compiler_external_output" > /dev/null ||
				fail "external measured compiler bytes differ at observation $iteration"
		fi
	done
	round=$((round + 1))
done
require_no_intermediates "$compiler_native_directory"
require_no_intermediates "$compiler_external_directory"

mkdir -p "$workspace/external-trace"
strace -f -e trace=process -o "$evidence/external-recipe-process.trace" \
	/bin/sh "$external_recipe" "$output_compiler" "$compiler_entry" \
	"$workspace/external-trace/compiler" "$qbe" "$cc" \
	> "$evidence/external-recipe.stdout" \
	2> "$evidence/external-recipe.stderr" || fail "traced external compiler recipe failed"
require_empty_file "$evidence/external-recipe.stdout" "traced external compiler recipe wrote stdout"
require_empty_file "$evidence/external-recipe.stderr" "traced external compiler recipe wrote stderr"
cmp "$output_compiler" "$workspace/external-trace/compiler" > /dev/null ||
	fail "traced external compiler bytes differ"
grep execve "$evidence/external-recipe-process.trace" > "$evidence/external-recipe-process-inventory.txt"

application_native_directory=$workspace/measured-application-native
application_go_directory=$workspace/measured-application-go
mkdir -p "$application_native_directory" "$application_go_directory"
application_native_output=$application_native_directory/program
application_go_output=$application_go_directory/program

round=0
while test "$round" -lt 13; do
	if test "$round" -lt 2; then
		iteration=$((round - 2))
	else
		iteration=$((round - 1))
	fi
	order='native go'
	if test $((round % 2)) -ne 0; then
		order='go native'
	fi
	for candidate in $order; do
		if test "$candidate" = native; then
			measure_command application-build native "$iteration" \
				"$output_compiler" build "$portable_config" \
					--output "$application_native_output" \
					--qbe "$qbe" --cc "$cc" --target "$PROFILE"
			require_measurement_success "Native application build observation $iteration"
			require_empty_file "$measurement_logs/application-build-native-$iteration.stdout" \
				"Native application build observation $iteration wrote stdout"
			require_empty_file "$measurement_logs/application-build-native-$iteration.stderr" \
				"Native application build observation $iteration wrote stderr"
			cmp "$native_application" "$application_native_output" > /dev/null ||
				fail "Native measured application bytes differ at observation $iteration"
		else
			measure_command application-build go "$iteration" \
				"$reference_trb" build --compile --config "$portable_config" \
				--outfile "$application_go_output"
			require_measurement_success "optimized Go application build observation $iteration"
			printf 'executable -> %s\n' "$application_go_output" \
				> "$measurement_logs/application-build-go-$iteration.expected"
			cmp "$measurement_logs/application-build-go-$iteration.expected" \
				"$measurement_logs/application-build-go-$iteration.stdout" > /dev/null ||
				fail "optimized Go build stdout differs at observation $iteration"
			require_empty_file "$measurement_logs/application-build-go-$iteration.stderr" \
				"optimized Go application build observation $iteration wrote stderr"
		fi
		executable=$application_native_output
		if test "$candidate" = go; then
			executable=$application_go_output
		fi
		"$executable" 144 \
			> "$measurement_logs/application-build-$candidate-$iteration.runtime.stdout" \
			2> "$measurement_logs/application-build-$candidate-$iteration.runtime.stderr" ||
			fail "$candidate measured application failed at observation $iteration"
		cmp "$expected_stdout" "$measurement_logs/application-build-$candidate-$iteration.runtime.stdout" > /dev/null ||
			fail "$candidate measured application stdout differs at observation $iteration"
		require_empty_file "$measurement_logs/application-build-$candidate-$iteration.runtime.stderr" \
			"$candidate measured application wrote runtime stderr at observation $iteration"
	done
	round=$((round + 1))
done
require_no_intermediates "$application_native_directory"

round=0
while test "$round" -lt 13; do
	if test "$round" -lt 2; then
		iteration=$((round - 2))
	else
		iteration=$((round - 1))
	fi
	order='native go'
	if test $((round % 2)) -ne 0; then
		order='go native'
	fi
	for candidate in $order; do
		executable=$native_application
		if test "$candidate" = go; then
			executable=$go_application
		fi
		measure_command application-runtime "$candidate" "$iteration" "$executable" 144
		require_measurement_success "$candidate application runtime observation $iteration"
		cmp "$expected_stdout" "$measurement_logs/application-runtime-$candidate-$iteration.stdout" > /dev/null ||
			fail "$candidate runtime stdout differs at observation $iteration"
		require_empty_file "$measurement_logs/application-runtime-$candidate-$iteration.stderr" \
			"$candidate runtime observation $iteration wrote stderr"
	done
	round=$((round + 1))
done

retained_count() {
	csv=$1
	stage=$2
	candidate=$3
	awk -F, -v stage="$stage" -v candidate="$candidate" \
		'NR > 1 && $1 == stage && $2 == candidate && $3 > 0 && $6 == 0 {count += 1} END {print count + 0}' \
		"$csv"
}

median_value() {
	csv=$1
	stage=$2
	candidate=$3
	column=$4
	count=$(retained_count "$csv" "$stage" "$candidate")
	test "$count" -gt 0 || fail "no retained $stage $candidate measurements"
	position=$(((count + 1) / 2))
	awk -F, -v stage="$stage" -v candidate="$candidate" -v column="$column" \
		'NR > 1 && $1 == stage && $2 == candidate && $3 > 0 && $6 == 0 {print $column}' \
		"$csv" | LC_ALL=C sort -n | sed -n "${position}p"
}

bootstrap_median() {
	stage=$1
	column=$2
	awk -F, -v stage="$stage" -v column="$column" \
		'NR > 1 && $1 == stage && $5 == 0 {print $column}' "$evidence/bootstrap/measurements.csv" |
		LC_ALL=C sort -n | sed -n '4p'
}

require_native_within_strongest() {
	label=$1
	native=$2
	comparison=$3
	percent=$4
	awk -v native="$native" -v comparison="$comparison" -v percent="$percent" 'BEGIN {
		strongest = native
		if (comparison < strongest) strongest = comparison
		exit !(native * 100 <= strongest * percent)
	}' || fail "$label exceeds the registered bound: native=$native comparison=$comparison"
}

require_spread() {
	label=$1
	first=$2
	second=$3
	percent=$4
	awk -v first="$first" -v second="$second" -v percent="$percent" 'BEGIN {
		minimum = first
		if (second < minimum) minimum = second
		maximum = first
		if (second > maximum) maximum = second
		exit !(maximum * 100 <= minimum * percent)
	}' || fail "$label exceeds the registered spread: $first, $second"
}

require_observations_below_catastrophic() {
	stage=$1
	candidate=$2
	column=$3
	baseline=$4
	awk -F, -v stage="$stage" -v candidate="$candidate" -v column="$column" -v baseline="$baseline" \
		'NR > 1 && $1 == stage && $2 == candidate && $3 > 0 && $column > baseline * 2 {exit 1}' \
		"$measurements" || fail "$stage $candidate observation exceeds the catastrophic bound"
}

require_bootstrap_observations_below_catastrophic() {
	column=$1
	baseline=$2
	awk -F, -v column="$column" -v baseline="$baseline" \
		'NR > 1 && ($1 == "b2-b3" || $1 == "b3-b4") && $2 > 0 && $5 == 0 && $column > baseline * 2 {exit 1}' \
		"$evidence/bootstrap/measurements.csv" ||
		fail "adjacent compiler observation exceeds the catastrophic bound"
}

test "$(retained_count "$measurements" compiler-build native)" -eq 7 ||
	fail "Native compiler measurement count differs"
test "$(retained_count "$measurements" compiler-build external)" -eq 7 ||
	fail "external compiler measurement count differs"
test "$(retained_count "$measurements" application-build native)" -eq 11 ||
	fail "Native application build measurement count differs"
test "$(retained_count "$measurements" application-build go)" -eq 11 ||
	fail "Go application build measurement count differs"
test "$(retained_count "$measurements" application-runtime native)" -eq 11 ||
	fail "Native application runtime measurement count differs"
test "$(retained_count "$measurements" application-runtime go)" -eq 11 ||
	fail "Go application runtime measurement count differs"

compiler_native_time=$(median_value "$measurements" compiler-build native 4)
compiler_external_time=$(median_value "$measurements" compiler-build external 4)
compiler_native_rss=$(median_value "$measurements" compiler-build native 5)
compiler_external_rss=$(median_value "$measurements" compiler-build external 5)
application_native_build_time=$(median_value "$measurements" application-build native 4)
application_go_build_time=$(median_value "$measurements" application-build go 4)
application_native_build_rss=$(median_value "$measurements" application-build native 5)
application_go_build_rss=$(median_value "$measurements" application-build go 5)
application_native_runtime_time=$(median_value "$measurements" application-runtime native 4)
application_go_runtime_time=$(median_value "$measurements" application-runtime go 4)
application_native_runtime_rss=$(median_value "$measurements" application-runtime native 5)
application_go_runtime_rss=$(median_value "$measurements" application-runtime go 5)
adjacent_b2_b3_time=$(bootstrap_median b2-b3 3)
adjacent_b3_b4_time=$(bootstrap_median b3-b4 3)
adjacent_b2_b3_rss=$(bootstrap_median b2-b3 4)
adjacent_b3_b4_rss=$(bootstrap_median b3-b4 4)

require_native_within_strongest "compiler build time" \
	"$compiler_native_time" "$compiler_external_time" 125
require_native_within_strongest "compiler build RSS" \
	"$compiler_native_rss" "$compiler_external_rss" 125
require_spread "adjacent compiler build time" "$adjacent_b2_b3_time" "$adjacent_b3_b4_time" 110
require_spread "adjacent compiler build RSS" "$adjacent_b2_b3_rss" "$adjacent_b3_b4_rss" 110
require_native_within_strongest "application build time" \
	"$application_native_build_time" "$application_go_build_time" 125
require_native_within_strongest "application build RSS" \
	"$application_native_build_rss" "$application_go_build_rss" 125
require_native_within_strongest "application runtime time" \
	"$application_native_runtime_time" "$application_go_runtime_time" 125
require_native_within_strongest "application runtime RSS" \
	"$application_native_runtime_rss" "$application_go_runtime_rss" 125

adjacent_strongest_time=$(awk -v a="$adjacent_b2_b3_time" -v b="$adjacent_b3_b4_time" \
	'BEGIN {if (a < b) print a; else print b}')
adjacent_strongest_rss=$(awk -v a="$adjacent_b2_b3_rss" -v b="$adjacent_b3_b4_rss" \
	'BEGIN {if (a < b) print a; else print b}')

require_observations_below_catastrophic compiler-build native 4 "$compiler_external_time"
require_observations_below_catastrophic compiler-build native 5 "$compiler_external_rss"
require_observations_below_catastrophic compiler-build external 4 "$compiler_external_time"
require_observations_below_catastrophic compiler-build external 5 "$compiler_external_rss"
require_observations_below_catastrophic application-build native 4 "$application_go_build_time"
require_observations_below_catastrophic application-build native 5 "$application_go_build_rss"
require_observations_below_catastrophic application-build go 4 "$application_go_build_time"
require_observations_below_catastrophic application-build go 5 "$application_go_build_rss"
require_observations_below_catastrophic application-runtime native 4 "$application_go_runtime_time"
require_observations_below_catastrophic application-runtime native 5 "$application_go_runtime_rss"
require_observations_below_catastrophic application-runtime go 4 "$application_go_runtime_time"
require_observations_below_catastrophic application-runtime go 5 "$application_go_runtime_rss"
require_bootstrap_observations_below_catastrophic 3 "$adjacent_strongest_time"
require_bootstrap_observations_below_catastrophic 4 "$adjacent_strongest_rss"

strip --strip-all -o "$workspace/native-first/program.stripped" "$native_application"
strip --strip-all -o "$workspace/go/program.stripped" "$go_application"
native_stripped_size=$(file_size "$workspace/native-first/program.stripped")
go_stripped_size=$(file_size "$workspace/go/program.stripped")
test "$((native_stripped_size * 5))" -le "$go_stripped_size" ||
	fail "Native portable-entry application is not at least 80% smaller than optimized Go"

cat > "$evidence/medians.csv" <<EOF
metric,native,comparison,limit_percent
compiler-build-time,$compiler_native_time,$compiler_external_time,125
compiler-build-rss,$compiler_native_rss,$compiler_external_rss,125
adjacent-build-time,$adjacent_b2_b3_time,$adjacent_b3_b4_time,110
adjacent-build-rss,$adjacent_b2_b3_rss,$adjacent_b3_b4_rss,110
application-build-time,$application_native_build_time,$application_go_build_time,125
application-build-rss,$application_native_build_rss,$application_go_build_rss,125
application-runtime-time,$application_native_runtime_time,$application_go_runtime_time,125
application-runtime-rss,$application_native_runtime_rss,$application_go_runtime_rss,125
EOF

{
	printf 'pre_implementation_revision=%s\n' "$PRE_IMPLEMENTATION_REVISION"
	printf 'candidate_revision=%s\n' "$(git -C "$candidate_root" rev-parse HEAD)"
	printf 'type_rb_revision=%s\n' "$TYPE_RB_REVISION"
	printf 'type_rb_version=%s\n' "$TYPE_RB_VERSION"
	printf 'root_qbe_sha256=%s\n' "$(sha256 "$root_qbe")"
	printf 'qbe_binary_sha256=%s\n' "$(sha256 "$qbe")"
	printf 'candidate_compiler_sha256=%s\n' "$(sha256 "$output_compiler")"
	printf 'candidate_fixed_point_qbe_sha256=%s\n' \
		"$(awk -F= '$1 == "fixed_point_qbe_sha256" {print $2}' "$evidence/bootstrap/identities.txt")"
	printf 'portable_entry_qbe_sha256=%s\n' \
		"$(sha256 "$evidence/applications/portable-entry-first.ssa")"
	printf 'native_application_sha256=%s\n' "$(sha256 "$native_application")"
	printf 'go_application_sha256=%s\n' "$(sha256 "$go_application")"
	printf 'native_application_raw_bytes=%s\n' "$(file_size "$native_application")"
	printf 'native_application_stripped_bytes=%s\n' "$native_stripped_size"
	printf 'go_application_raw_bytes=%s\n' "$(file_size "$go_application")"
	printf 'go_application_stripped_bytes=%s\n' "$go_stripped_size"
} > "$evidence/identities.txt"

{
	printf 'verifier_revision=%s\n' "$(git -C "$verifier_root" rev-parse HEAD)"
	printf 'candidate_revision=%s\n' "$(git -C "$candidate_root" rev-parse HEAD)"
	printf 'profile=%s\n' "$PROFILE"
	printf 'qbe_target=amd64_sysv\n'
	printf 'runner_image=%s\n' "$RUNNER_IMAGE"
	uname -a
	"$reference_trb" version
	"$go_command" version
	"$go_command" env GOCACHE GOENV GOOS GOARCH
	"$cc" --version
	ld.lld --version
	"$qbe" -h
} > "$evidence/environment.txt" 2>&1

"$cc" -### -xassembler "$first_assembly" \
	-fuse-ld=lld -Wl,--gc-sections,--strip-all -lm -o "$workspace/cc-expansion-output" \
	> "$evidence/cc-expansion.stdout" 2> "$evidence/cc-expansion.stderr" ||
	fail "CC expansion probe failed"
require_empty_file "$evidence/cc-expansion.stdout" "CC expansion probe wrote stdout"

require_clean_revision "$candidate_root" "Gate 6N candidate after verification"
require_no_intermediates "$workspace"
printf 'gate6n-linux-amd64: passed\n'
}

test -x /usr/bin/time || fail "/usr/bin/time is required"

test -d "$candidate_root" || fail "candidate root does not exist"
test -f "$root_qbe" || fail "root QBE does not exist"
test -x "$qbe" || fail "QBE is not executable"
test -x "$cc" || fail "CC is not executable"
test -x "$reference_trb" || fail "reference trb is not executable"
test -x "$go_command" || fail "Go is not executable"
test -x "$external_recipe" || fail "external comparison recipe is not executable"
file -L "$qbe" | grep -F 'ELF ' > /dev/null || fail "QBE must be a direct ELF executable"
file -L "$cc" | grep -F 'ELF ' > /dev/null || fail "CC must be a direct ELF executable"
test "$(command -v go)" = "$go_command" || fail "Go command does not match PATH"
test ! -e "$workspace" || fail "workspace already exists"
test ! -e "$evidence" || fail "evidence path already exists"
test ! -e "$output_compiler" || fail "output compiler already exists"

record_temporary_inventory() {
	mkdir -p "$evidence"
	if test -d "$workspace"; then
		find "$workspace" \( -name '*.trbn.*' -o -name '*.gate6n-external.*' \) -print \
			> "$evidence/final-temporary-inventory.txt" 2>&1 || true
	else
		: > "$evidence/final-temporary-inventory.txt"
	fi
}
trap record_temporary_inventory 0
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

require_clean_revision "$candidate_root" "Gate 6N candidate"
test "$(tr -d '\n' < "$candidate_root/TYPE_RB_REVISION")" = "$TYPE_RB_REVISION" ||
	fail "candidate TypeRB revision pin differs"
test "$("$reference_trb" version)" = "$TYPE_RB_VERSION" || fail "reference TypeRB version differs"
"$go_command" version > /dev/null 2>&1 || fail "Go toolchain probe failed"
test "$(file_size "$root_qbe")" -eq "$ROOT_QBE_SIZE" || fail "root QBE size differs"
test "$(sha256 "$root_qbe")" = "$ROOT_QBE_SHA256" || fail "root QBE digest differs"

compiler_entry=$candidate_root/compiler/gate4/src/compiler.trb
portable_config=$candidate_root/corpus/gate6m/portable-entry/trbconfig.jsonc
portable_source=$candidate_root/corpus/gate6m/portable-entry/src/main.trb
failure_config=$candidate_root/corpus/gate6m/runtime-failures/trbconfig.jsonc
failure_source=$candidate_root/corpus/gate6m/runtime-failures/src/main.trb

for required_file in "$compiler_entry" "$portable_config" "$portable_source" "$failure_config" "$failure_source"; do
	test -f "$required_file" || fail "required source is missing: $required_file"
done
test "$(sha256 "$portable_config")" = 4b81aaacced57409eeaa8494c45ecba6fd67868f74075e768e287815cf7c6519 ||
	fail "portable-entry config digest differs"
test "$(sha256 "$portable_source")" = 67d89532214e49f0a574cc031f33ca0e91f414a63e3185e274d260f80b243f66 ||
	fail "portable-entry source digest differs"
test "$(sha256 "$failure_config")" = b9511ce4e0c9e6fcc18fbbdddbcbe1645f3701eb7e10fb6ab5be125eb6b288cc ||
	fail "runtime-failure config digest differs"
test "$(sha256 "$failure_source")" = dc9e4ec4667c09fe1392a64b22cad5727568b7b08954d3fc09640847bb60a086 ||
	fail "runtime-failure source digest differs"

mkdir -p \
	"$workspace/setup/root-era" \
	"$workspace/setup/first" \
	"$workspace/setup/current-runtime" \
	"$evidence/setup" \
	"$(dirname -- "$output_compiler")"

root_assembly=$workspace/setup/root-era/compiler.s
root_compiler=$workspace/setup/root-era/compiler
first_qbe=$workspace/setup/first/compiler.ssa
first_assembly=$workspace/setup/first/compiler.s
first_transition=$workspace/setup/first/compiler
runtime_qbe=$workspace/setup/current-runtime/compiler.ssa
runtime_assembly=$workspace/setup/current-runtime/compiler.s
runtime_transition=$workspace/setup/current-runtime/compiler

strace -f -e trace=process -o "$evidence/setup/root-qbe-process.trace" \
	"$qbe" -t amd64_sysv -o "$root_assembly" "$root_qbe" \
	> "$evidence/setup/root-qbe.stdout" \
	2> "$evidence/setup/root-qbe.stderr" || fail "root QBE translation failed"
require_empty_file "$evidence/setup/root-qbe.stdout" "root QBE translation wrote stdout"
require_empty_file "$evidence/setup/root-qbe.stderr" "root QBE translation wrote stderr"
test -s "$root_assembly" || fail "root QBE translation did not produce assembly"

strace -f -e trace=process -o "$evidence/setup/root-link-process.trace" \
	"$cc" -xassembler "$root_assembly" \
		-fuse-ld=lld \
		-Wl,--gc-sections,--strip-all \
		-lm \
		-o "$root_compiler" \
	> "$evidence/setup/root-link.stdout" \
	2> "$evidence/setup/root-link.stderr" || fail "root-era compiler link failed"
require_empty_file "$evidence/setup/root-link.stdout" "root-era compiler link wrote stdout"
require_empty_file "$evidence/setup/root-link.stderr" "root-era compiler link wrote stderr"
test -x "$root_compiler" || fail "root-era compiler was not produced"
require_tool_observed "$evidence/setup/root-link-process.trace" 'execve\("[^"]*/(as|x86_64-linux-gnu-as)"' \
	"root-era assembler"
require_tool_observed "$evidence/setup/root-link-process.trace" 'execve\("[^"]*/ld\.lld"' \
	"root-era LLD"

strace -f -e trace=process -o "$evidence/setup/root-emit-process.trace" \
	"$root_compiler" emit-qbe "$compiler_entry" \
	> "$first_qbe" \
	2> "$evidence/setup/root-emit.stderr" || fail "root-era current-source emission failed"
require_empty_file "$evidence/setup/root-emit.stderr" "root-era current-source emission wrote stderr"
test -s "$first_qbe" || fail "root-era compiler emitted empty current-source QBE"
require_forbidden_processes_absent "$evidence/setup/root-emit-process.trace" \
	"root-era current-source emission"

strace -f -e trace=process -o "$evidence/setup/first-qbe-process.trace" \
	"$qbe" -t amd64_sysv -o "$first_assembly" "$first_qbe" \
	> "$evidence/setup/first-qbe.stdout" \
	2> "$evidence/setup/first-qbe.stderr" || fail "first-transition QBE translation failed"
require_empty_file "$evidence/setup/first-qbe.stdout" "first-transition QBE translation wrote stdout"
require_empty_file "$evidence/setup/first-qbe.stderr" "first-transition QBE translation wrote stderr"
test -s "$first_assembly" || fail "first-transition QBE translation did not produce assembly"

strace -f -e trace=process -o "$evidence/setup/first-link-process.trace" \
	"$cc" -xassembler "$first_assembly" \
		-fuse-ld=lld \
		-Wl,--gc-sections,--strip-all \
		-lm \
		-o "$first_transition" \
	> "$evidence/setup/first-link.stdout" \
	2> "$evidence/setup/first-link.stderr" || fail "first-transition link failed"
require_empty_file "$evidence/setup/first-link.stdout" "first-transition link wrote stdout"
require_empty_file "$evidence/setup/first-link.stderr" "first-transition link wrote stderr"
test -x "$first_transition" || fail "first current-source transition was not produced"
require_tool_observed "$evidence/setup/first-link-process.trace" 'execve\("[^"]*/ld\.lld"' \
	"first-transition LLD"

strace -f -e trace=process -o "$evidence/setup/current-runtime-emit-process.trace" \
	"$first_transition" emit-qbe "$compiler_entry" \
	> "$runtime_qbe" \
	2> "$evidence/setup/current-runtime-emit.stderr" || fail "current-runtime QBE emission failed"
require_empty_file "$evidence/setup/current-runtime-emit.stderr" "current-runtime QBE emission wrote stderr"
test -s "$runtime_qbe" || fail "first transition emitted empty current-runtime QBE"
require_forbidden_processes_absent "$evidence/setup/current-runtime-emit-process.trace" \
	"current-runtime QBE emission"

strace -f -e trace=process -o "$evidence/setup/current-runtime-qbe-process.trace" \
	"$qbe" -t amd64_sysv -o "$runtime_assembly" "$runtime_qbe" \
	> "$evidence/setup/current-runtime-qbe.stdout" \
	2> "$evidence/setup/current-runtime-qbe.stderr" || fail "current-runtime QBE translation failed"
require_empty_file "$evidence/setup/current-runtime-qbe.stdout" "current-runtime QBE translation wrote stdout"
require_empty_file "$evidence/setup/current-runtime-qbe.stderr" "current-runtime QBE translation wrote stderr"
test -s "$runtime_assembly" || fail "current-runtime QBE translation did not produce assembly"

strace -f -e trace=process -o "$evidence/setup/current-runtime-link-process.trace" \
	"$cc" -xassembler "$runtime_assembly" \
		-fuse-ld=lld \
		-Wl,--gc-sections,--strip-all \
		-lm \
		-o "$runtime_transition" \
	> "$evidence/setup/current-runtime-link.stdout" \
	2> "$evidence/setup/current-runtime-link.stderr" || fail "current-runtime setup link failed"
require_empty_file "$evidence/setup/current-runtime-link.stdout" "current-runtime link wrote stdout"
require_empty_file "$evidence/setup/current-runtime-link.stderr" "current-runtime link wrote stderr"
test -x "$runtime_transition" || fail "current-runtime transition was not produced"
require_tool_observed "$evidence/setup/current-runtime-link-process.trace" 'execve\("[^"]*/ld\.lld"' \
	"current-runtime LLD"

{
	grep execve "$evidence/setup/root-qbe-process.trace"
	grep execve "$evidence/setup/root-link-process.trace"
	grep execve "$evidence/setup/root-emit-process.trace"
	grep execve "$evidence/setup/first-qbe-process.trace"
	grep execve "$evidence/setup/first-link-process.trace"
	grep execve "$evidence/setup/current-runtime-emit-process.trace"
	grep execve "$evidence/setup/current-runtime-qbe-process.trace"
	grep execve "$evidence/setup/current-runtime-link-process.trace"
} > "$evidence/setup/process-inventory.txt"
{
	printf 'root_qbe_size=%s\n' "$(file_size "$root_qbe")"
	printf 'root_qbe_sha256=%s\n' "$(sha256 "$root_qbe")"
	printf 'root_era_compiler_size=%s\n' "$(file_size "$root_compiler")"
	printf 'root_era_compiler_sha256=%s\n' "$(sha256 "$root_compiler")"
	printf 'first_transition_qbe_size=%s\n' "$(file_size "$first_qbe")"
	printf 'first_transition_qbe_sha256=%s\n' "$(sha256 "$first_qbe")"
	printf 'first_transition_size=%s\n' "$(file_size "$first_transition")"
	printf 'first_transition_sha256=%s\n' "$(sha256 "$first_transition")"
	printf 'current_runtime_qbe_size=%s\n' "$(file_size "$runtime_qbe")"
	printf 'current_runtime_qbe_sha256=%s\n' "$(sha256 "$runtime_qbe")"
	printf 'current_runtime_transition_size=%s\n' "$(file_size "$runtime_transition")"
	printf 'current_runtime_transition_sha256=%s\n' "$(sha256 "$runtime_transition")"
} > "$evidence/setup/identities.txt"

/bin/sh "$verifier_root/tools/bootstrap-seed.sh" \
	--mode previous \
	--input "$runtime_transition" \
	--input-role transition \
	--qbe "$qbe" \
	--cc "$cc" \
	--profile "$PROFILE" \
	--runner-image "$RUNNER_IMAGE" \
	--workspace "$workspace/bootstrap" \
	--output "$output_compiler" \
	--evidence "$evidence/bootstrap" \
	--metadata "$evidence/bootstrap-metadata.json" \
	--asset-name gate6n-candidate-linux-amd64 \
	--repository-root "$candidate_root" \
	> "$evidence/bootstrap.stdout" \
	2> "$evidence/bootstrap.stderr" || fail "candidate compiler chain failed"
printf 'bootstrap-seed: previous linux-amd64-v0 passed\n' > "$evidence/bootstrap.expected"
sed -n '$p' "$evidence/bootstrap.stdout" > "$evidence/bootstrap-marker.actual"
cmp "$evidence/bootstrap.expected" "$evidence/bootstrap-marker.actual" > /dev/null ||
	fail "candidate compiler chain success marker differs"
sed '$d' "$evidence/bootstrap.stdout" > "$evidence/bootstrap-checks.stdout"
test -s "$evidence/bootstrap-checks.stdout" || fail "candidate compiler chain reported no checks"
if grep -v '^ok$' "$evidence/bootstrap-checks.stdout" > /dev/null; then
	fail "candidate compiler chain reported unexpected checker output"
fi
require_empty_file "$evidence/bootstrap.stderr" "candidate compiler chain wrote stderr"
require_forbidden_processes_absent "$evidence/bootstrap/process.trace" \
	"closed candidate ordinary build"
require_tool_observed "$evidence/bootstrap/process.trace" 'execve\("[^"]*/ld\.lld"' \
	"closed candidate LLD"

ordinary_trace_directory=$workspace/ordinary-chain-traces
mkdir -p "$ordinary_trace_directory" "$evidence/ordinary-chain"
trace_ordinary_build() {
	label=$1
	seed=$2
	expected=$3
	build_directory=$ordinary_trace_directory/$label
	trace=$evidence/ordinary-chain/$label.process.trace
	mkdir -p "$build_directory"
	strace -f -e trace=process -o "$trace" \
		"$seed" build "$compiler_entry" \
			--output "$build_directory/compiler" \
			--qbe "$qbe" --cc "$cc" --target "$PROFILE" \
		> "$evidence/ordinary-chain/$label.stdout" \
		2> "$evidence/ordinary-chain/$label.stderr" || fail "$label traced ordinary build failed"
	require_empty_file "$evidence/ordinary-chain/$label.stdout" "$label traced ordinary build wrote stdout"
	require_empty_file "$evidence/ordinary-chain/$label.stderr" "$label traced ordinary build wrote stderr"
	cmp "$expected" "$build_directory/compiler" > /dev/null || fail "$label traced compiler bytes differ"
	require_closed_ordinary_trace "$trace" "$seed" "$label ordinary build"
	require_no_intermediates "$build_directory"
}

bootstrap_b1=$workspace/bootstrap/b1/compiler
bootstrap_b2=$workspace/bootstrap/b2/compiler
bootstrap_b3=$workspace/bootstrap/b3/compiler
bootstrap_b4=$workspace/bootstrap/b4/compiler
trace_ordinary_build b1-to-b2 "$bootstrap_b1" "$bootstrap_b2"
trace_ordinary_build b2-to-b3 "$bootstrap_b2" "$bootstrap_b3"
trace_ordinary_build b3-to-b4 "$bootstrap_b3" "$bootstrap_b4"
{
	cat "$evidence/ordinary-chain/b1-to-b2.process.trace.executables"
	cat "$evidence/ordinary-chain/b2-to-b3.process.trace.executables"
	cat "$evidence/ordinary-chain/b3-to-b4.process.trace.executables"
} > "$evidence/ordinary-chain/process-inventory.txt"

failure_order_directory=$workspace/gate6n-failure-order
mkdir -p "$failure_order_directory"
probe_tool=$failure_order_directory/probe-tool
probe_marker=$failure_order_directory/probe-launched
cat > "$probe_tool" <<EOF
#!/bin/sh
/usr/bin/touch "$probe_marker"
exit 91
EOF
chmod 0755 "$probe_tool"
printf 'compiler: unsupported target profile\n' > "$failure_order_directory/unsupported.expected"
set +e
"$output_compiler" build "$failure_order_directory/missing-source.trb" \
	--output "$failure_order_directory/unsupported-output" \
	--qbe "$probe_tool" --cc "$probe_tool" --target unknown-v0 \
	> "$failure_order_directory/unsupported.stdout" \
	2> "$failure_order_directory/unsupported.stderr"
unsupported_status=$?
set -e
test "$unsupported_status" -eq 64 || fail "unknown target did not fail with status 64"
require_empty_file "$failure_order_directory/unsupported.stdout" "unknown target wrote stdout"
cmp "$failure_order_directory/unsupported.expected" "$failure_order_directory/unsupported.stderr" > /dev/null ||
	fail "unknown target diagnostic differs"
test ! -e "$probe_marker" || fail "unknown target launched an external tool"
test ! -e "$failure_order_directory/unsupported-output" || fail "unknown target published output"

publication_output=$failure_order_directory/publication-output
mkdir "$publication_output"
printf 'preserve-publication-directory\n' > "$publication_output/sentinel"
printf 'compiler: cannot publish output\n' > "$failure_order_directory/publication.expected"
set +e
"$output_compiler" build "$portable_config" \
	--output "$publication_output" \
	--qbe "$qbe" --cc "$cc" --target "$PROFILE" \
	> "$failure_order_directory/publication.stdout" \
	2> "$failure_order_directory/publication.stderr"
publication_status=$?
set -e
test "$publication_status" -eq 73 || fail "publication failure did not return status 73"
require_empty_file "$failure_order_directory/publication.stdout" "publication failure wrote stdout"
cmp "$failure_order_directory/publication.expected" "$failure_order_directory/publication.stderr" > /dev/null ||
	fail "publication failure diagnostic differs"
test "$(cat "$publication_output/sentinel")" = preserve-publication-directory ||
	fail "publication failure did not preserve the destination directory"
require_no_intermediates "$failure_order_directory"

compiler_size=$(file_size "$output_compiler")
test "$compiler_size" -le "$MAX_COMPILER_SIZE" || fail "candidate compiler exceeds the size bound"
{
	printf 'platform=linux-amd64\n'
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
		--output "$native_application" --qbe "$qbe" --cc "$cc" --target "$PROFILE"
require_successful_command \
	"$evidence/applications/native-second.stdout" \
	"$evidence/applications/native-second.stderr" \
	"repeated Native portable-entry build" \
	"$output_compiler" build "$portable_config" \
		--output "$native_application_repeat" --qbe "$qbe" --cc "$cc" --target "$PROFILE"
cmp "$native_application" "$native_application_repeat" > /dev/null ||
	fail "repeated Native portable-entry bytes differ"

"$output_compiler" emit-qbe "$portable_config" \
	> "$evidence/applications/portable-entry-first.ssa" \
	2> "$evidence/applications/portable-entry-first.stderr" || fail "portable-entry QBE emission failed"
"$output_compiler" emit-qbe "$portable_config" \
	> "$evidence/applications/portable-entry-second.ssa" \
	2> "$evidence/applications/portable-entry-second.stderr" || fail "repeated portable-entry QBE emission failed"
require_empty_file "$evidence/applications/portable-entry-first.stderr" \
	"portable-entry QBE emission wrote stderr"
require_empty_file "$evidence/applications/portable-entry-second.stderr" \
	"repeated portable-entry QBE emission wrote stderr"
cmp "$evidence/applications/portable-entry-first.ssa" \
	"$evidence/applications/portable-entry-second.ssa" > /dev/null ||
	fail "portable-entry QBE is not deterministic"

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
		--target "$PROFILE" \
	> "$evidence/applications/native-trace.stdout" \
	2> "$evidence/applications/native-trace.stderr" || fail "traced Native portable-entry build failed"
require_empty_file "$evidence/applications/native-trace.stdout" \
	"traced Native portable-entry build wrote stdout"
require_empty_file "$evidence/applications/native-trace.stderr" \
	"traced Native portable-entry build wrote stderr"
require_forbidden_processes_absent "$evidence/applications/native-build-process.trace" \
	"ordinary Native application build"
require_tool_observed "$evidence/applications/native-build-process.trace" 'execve\("[^"]*/ld\.lld"' \
	"ordinary Native application LLD"
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
		--output "$native_failure_application" --qbe "$qbe" --cc "$cc" --target "$PROFILE"
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
		test "$actual_class" = "$expected_class" || fail "$candidate_label $mode failure class differs"
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

run_formal_evidence
