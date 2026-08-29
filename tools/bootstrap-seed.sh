#!/bin/sh

set -eu

ROOT_QBE_SIZE=658639
ROOT_QBE_SHA256=62db3c31527a670c3050051a9fa27bf142b6c5deaab81ef8234104bd467aa95a
MAX_COMPILER_SIZE=310000

usage() {
	cat >&2 <<'EOF'
usage: bootstrap-seed.sh --mode initial|previous --input PATH --qbe PATH --cc PATH
       --profile darwin-arm64-v0|linux-arm64-v0 --runner-image LABEL
       --workspace PATH --output PATH --evidence PATH --metadata PATH
       --asset-name NAME
EOF
	exit 64
}

fail() {
	printf 'bootstrap-seed: %s\n' "$1" >&2
	exit 1
}

sha256() {
	if command -v sha256sum >/dev/null 2>&1; then
		sha256sum "$1" | awk '{print $1}'
	else
		shasum -a 256 "$1" | awk '{print $1}'
	fi
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

expect_status() {
	expected_status=$1
	expected_stdout=$2
	expected_stderr=$3
	shift 3
	actual_stdout=$workspace/expect-status.stdout
	actual_stderr=$workspace/expect-status.stderr
	set +e
	"$@" > "$actual_stdout" 2> "$actual_stderr"
	actual_status=$?
	set -e
	test "$actual_status" -eq "$expected_status" ||
		fail "expected status $expected_status, received $actual_status: $*"
	cmp "$expected_stdout" "$actual_stdout" >/dev/null ||
		fail "stdout differs: $*"
	cmp "$expected_stderr" "$actual_stderr" >/dev/null ||
		fail "stderr differs: $*"
}

mode=
input=
qbe=
cc=
profile=
runner_image=
workspace=
output=
evidence=
metadata=
asset_name=

while test "$#" -gt 0; do
	case "$1" in
	--mode)
		test -z "$mode" || usage
		test "$#" -ge 2 || usage
		mode=$2
		shift 2
		;;
	--input)
		test -z "$input" || usage
		test "$#" -ge 2 || usage
		input=$2
		shift 2
		;;
	--qbe)
		test -z "$qbe" || usage
		test "$#" -ge 2 || usage
		qbe=$2
		shift 2
		;;
	--cc)
		test -z "$cc" || usage
		test "$#" -ge 2 || usage
		cc=$2
		shift 2
		;;
	--profile)
		test -z "$profile" || usage
		test "$#" -ge 2 || usage
		profile=$2
		shift 2
		;;
	--runner-image)
		test -z "$runner_image" || usage
		test "$#" -ge 2 || usage
		runner_image=$2
		shift 2
		;;
	--workspace)
		test -z "$workspace" || usage
		test "$#" -ge 2 || usage
		workspace=$2
		shift 2
		;;
	--output)
		test -z "$output" || usage
		test "$#" -ge 2 || usage
		output=$2
		shift 2
		;;
	--evidence)
		test -z "$evidence" || usage
		test "$#" -ge 2 || usage
		evidence=$2
		shift 2
		;;
	--metadata)
		test -z "$metadata" || usage
		test "$#" -ge 2 || usage
		metadata=$2
		shift 2
		;;
	--asset-name)
		test -z "$asset_name" || usage
		test "$#" -ge 2 || usage
		asset_name=$2
		shift 2
		;;
	*) usage ;;
	esac
done

test "$mode" = initial || test "$mode" = previous || usage
test -n "$input" && test -n "$qbe" && test -n "$cc" || usage
test -n "$profile" && test -n "$runner_image" || usage
test -n "$workspace" && test -n "$output" && test -n "$evidence" || usage
test -n "$metadata" && test -n "$asset_name" || usage
test -f "$input" || fail "input does not exist"
test -x "$qbe" || fail "QBE is not executable"
test -x "$cc" || fail "CC is not executable"
test ! -e "$workspace" || fail "workspace already exists"
test ! -e "$output" || fail "output already exists"
test ! -e "$evidence" || fail "evidence path already exists"
test ! -e "$metadata" || fail "metadata already exists"

case "$profile" in
darwin-arm64-v0)
	os=darwin
	architecture=arm64
	qbe_target=arm64_apple
	expected_runner=macos-15
	;;
linux-arm64-v0)
	os=linux
	architecture=arm64
	qbe_target=arm64
	expected_runner=ubuntu-24.04-arm
	;;
*) usage ;;
esac

test "$runner_image" = "$expected_runner" || fail "runner image does not match profile"
if test "$os" = darwin; then
	test "$(uname -s)" = Darwin || fail "Darwin profile requires Darwin"
	test "$(uname -m)" = arm64 || fail "Darwin profile requires arm64"
else
	test "$(uname -s)" = Linux || fail "Linux profile requires Linux"
	case "$(uname -m)" in
	aarch64 | arm64) ;;
	*) fail "Linux profile requires arm64" ;;
	esac
fi

script_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repository_root=$(CDPATH= cd -- "$script_directory/.." && pwd)
compiler_entry=$repository_root/compiler/gate4/src/compiler.trb
configured_project=$repository_root/corpus/gate6k/configured-project/trbconfig.jsonc

test -f "$compiler_entry" || fail "compiler entry is missing"
test -f "$configured_project" || fail "configured-project fixture is missing"
command -v jq >/dev/null 2>&1 || fail "jq is required"

mkdir -p "$workspace" "$evidence" "$(dirname -- "$output")" "$(dirname -- "$metadata")"
mkdir -p "$workspace/b1" "$workspace/b2" "$workspace/b3" "$workspace/b4"

b1=$workspace/b1/compiler
b2=$workspace/b2/compiler
b3=$workspace/b3/compiler
b4=$workspace/b4/compiler

if test "$mode" = initial; then
	test "$(file_size "$input")" -eq "$ROOT_QBE_SIZE" || fail "root QBE size differs"
	test "$(sha256 "$input")" = "$ROOT_QBE_SHA256" || fail "root QBE digest differs"
	assembly=$workspace/b1/compiler.s
	"$qbe" -t "$qbe_target" -o "$assembly" "$input"
	if test "$os" = darwin; then
		"$cc" -x assembler "$assembly" -Wl,-dead_strip -o "$b1"
	else
		"$cc" -x assembler "$assembly" -Wl,--gc-sections,--strip-all -o "$b1"
	fi
else
	cp "$input" "$b1"
	chmod 0755 "$b1"
fi

"$b1" build "$compiler_entry" --output "$b2" --qbe "$qbe" --cc "$cc" --target "$profile"
"$b2" build "$compiler_entry" --output "$b3" --qbe "$qbe" --cc "$cc" --target "$profile"
"$b3" build "$compiler_entry" --output "$b4" --qbe "$qbe" --cc "$cc" --target "$profile"

if test "$mode" = initial; then
	cmp "$b1" "$b2" >/dev/null || fail "root B1 and generated B2 differ"
fi
cmp "$b2" "$b3" >/dev/null || fail "B2 and B3 differ"
cmp "$b3" "$b4" >/dev/null || fail "B3 and B4 differ"

for compiler in "$b2" "$b3" "$b4"; do
	"$compiler" check "$compiler_entry"
	"$compiler" emit-qbe "$compiler_entry" > "$compiler.fixed-point.ssa"
	test "$(file_size "$compiler.fixed-point.ssa")" -eq "$ROOT_QBE_SIZE" ||
		fail "compiler fixed-point QBE size differs"
	test "$(sha256 "$compiler.fixed-point.ssa")" = "$ROOT_QBE_SHA256" ||
		fail "compiler fixed-point QBE digest differs"
done
cmp "$b2.fixed-point.ssa" "$b3.fixed-point.ssa" >/dev/null || fail "B2/B3 QBE differs"
cmp "$b3.fixed-point.ssa" "$b4.fixed-point.ssa" >/dev/null || fail "B3/B4 QBE differs"

verify_program_case() {
	compiler=$1
	source=$2
	expected=$3
	case_directory=$4
	mkdir -p "$case_directory"
	"$compiler" check "$source"
	"$compiler" emit-qbe "$source" > "$case_directory/first.ssa"
	"$compiler" emit-qbe "$source" > "$case_directory/second.ssa"
	cmp "$case_directory/first.ssa" "$case_directory/second.ssa" >/dev/null ||
		fail "repeated QBE differs for $source"
	"$compiler" build "$source" --output "$case_directory/program" --qbe "$qbe" --cc "$cc" --target "$profile"
	"$case_directory/program" > "$case_directory/stdout" 2> "$case_directory/stderr"
	cmp "$expected" "$case_directory/stdout" >/dev/null || fail "runtime output differs for $source"
	require_empty_file "$case_directory/stderr" "runtime stderr differs for $source"
	require_no_intermediates "$case_directory"
}

corpus_root=$repository_root/compiler/gate4/conformance
mkdir -p "$workspace/corpus"
for compiler_pair in "b2:$b2" "b3:$b3" "b4:$b4"; do
	compiler_label=$(printf '%s\n' "$compiler_pair" | cut -d: -f1)
	compiler=$(printf '%s\n' "$compiler_pair" | cut -d: -f2-)
	for source in "$corpus_root"/valid/*.trb "$corpus_root"/mutations/*.trb; do
		case_name=$(basename -- "$source" .trb)
		case_group=$(basename -- "$(dirname -- "$source")")
		expected=$(printf '%s\n' "$source" | sed 's/\.trb$/.out/')
		verify_program_case \
			"$compiler" "$source" "$expected" \
			"$workspace/corpus/$compiler_label-$case_group-$case_name"
	done
done

"$b4" emit-qbe "$corpus_root/mutations/base.trb" > "$workspace/corpus/mutation-base.ssa"
"$b4" emit-qbe "$corpus_root/mutations/literal.trb" > "$workspace/corpus/mutation-literal.ssa"
"$b4" emit-qbe "$corpus_root/mutations/control.trb" > "$workspace/corpus/mutation-control.ssa"
cmp -s "$workspace/corpus/mutation-base.ssa" "$workspace/corpus/mutation-literal.ssa" &&
	fail "base and literal mutations emit equal QBE"
cmp -s "$workspace/corpus/mutation-base.ssa" "$workspace/corpus/mutation-control.ssa" &&
	fail "base and control mutations emit equal QBE"
cmp -s "$workspace/corpus/mutation-literal.ssa" "$workspace/corpus/mutation-control.ssa" &&
	fail "literal and control mutations emit equal QBE"

empty_file=$workspace/empty
: > "$empty_file"
probe_tool=$workspace/probe-tool
tool_marker=$workspace/tool-launched
cat > "$probe_tool" <<EOF
#!/bin/sh
/usr/bin/touch "$tool_marker"
exit 91
EOF
chmod 0755 "$probe_tool"

for compiler_pair in "b2:$b2" "b3:$b3" "b4:$b4"; do
	compiler_label=$(printf '%s\n' "$compiler_pair" | cut -d: -f1)
	compiler=$(printf '%s\n' "$compiler_pair" | cut -d: -f2-)
	for source in "$corpus_root"/invalid/*.source; do
		case_name=$(basename -- "$source" .source)
		expected=$(printf '%s\n' "$source" | sed 's/\.source$/.diag/')
		case_directory=$workspace/corpus/$compiler_label-invalid-$case_name
		mkdir -p "$case_directory"
		expect_status 1 "$empty_file" "$expected" "$compiler" check "$source"
		expect_status 1 "$empty_file" "$expected" "$compiler" emit-qbe "$source"
		expect_status 1 "$empty_file" "$expected" \
			"$compiler" build "$source" --output "$case_directory/program" \
			--qbe "$probe_tool" --cc "$probe_tool" --target "$profile"
		test ! -e "$case_directory/program" || fail "invalid source published an executable"
		test ! -e "$tool_marker" || fail "invalid source launched an external tool"
		require_no_intermediates "$case_directory"
	done
done

runtime_invalid=$corpus_root/runtime-invalid/float-array-bounds.trb
runtime_expected=$workspace/runtime-invalid.expected
printf 'panic: index is out of bounds\n' > "$runtime_expected"
for compiler_pair in "b2:$b2" "b3:$b3" "b4:$b4"; do
	compiler_label=$(printf '%s\n' "$compiler_pair" | cut -d: -f1)
	compiler=$(printf '%s\n' "$compiler_pair" | cut -d: -f2-)
	case_directory=$workspace/corpus/$compiler_label-runtime-invalid
	mkdir -p "$case_directory"
	"$compiler" build "$runtime_invalid" --output "$case_directory/program" --qbe "$qbe" --cc "$cc" --target "$profile"
	set +e
	"$case_directory/program" > "$case_directory/stdout" 2> "$case_directory/stderr"
	runtime_status=$?
	set -e
	test "$runtime_status" -eq 2 || fail "runtime failure status differs"
	require_empty_file "$case_directory/stdout" "runtime failure stdout differs"
	cmp "$runtime_expected" "$case_directory/stderr" >/dev/null || fail "runtime failure stderr differs"
	require_no_intermediates "$case_directory"
done

mkdir -p "$workspace/configured/b2" "$workspace/configured/b3" "$workspace/configured/b4"
for compiler_pair in "b2:$b2" "b3:$b3" "b4:$b4"; do
	compiler_label=$(printf '%s\n' "$compiler_pair" | cut -d: -f1)
	compiler=$(printf '%s\n' "$compiler_pair" | cut -d: -f2-)
	"$compiler" check "$configured_project"
	"$compiler" emit-qbe "$configured_project" > "$workspace/configured/$compiler_label/program.ssa"
	"$compiler" build "$configured_project" \
		--output "$workspace/configured/$compiler_label/program" \
		--qbe "$qbe" --cc "$cc" --target "$profile"
done
cmp "$workspace/configured/b2/program.ssa" "$workspace/configured/b3/program.ssa" >/dev/null ||
	fail "configured B2/B3 QBE differs"
cmp "$workspace/configured/b3/program.ssa" "$workspace/configured/b4/program.ssa" >/dev/null ||
	fail "configured B3/B4 QBE differs"
cmp "$workspace/configured/b2/program" "$workspace/configured/b3/program" >/dev/null ||
	fail "configured B2/B3 executable differs"
cmp "$workspace/configured/b3/program" "$workspace/configured/b4/program" >/dev/null ||
	fail "configured B3/B4 executable differs"
"$workspace/configured/b4/program" > "$workspace/configured/stdout" 2> "$workspace/configured/stderr"
printf 'configured-project-ok\n' > "$workspace/configured/expected"
cmp "$workspace/configured/expected" "$workspace/configured/stdout" >/dev/null ||
	fail "configured-project output differs"
require_empty_file "$workspace/configured/stderr" "configured-project stderr differs"

failure_directory=$workspace/failures
mkdir -p "$failure_directory"
printf 'preserve-qbe\n' > "$failure_directory/qbe-output"
set +e
"$b4" build "$configured_project" --output "$failure_directory/qbe-output" \
	--qbe /usr/bin/false --cc "$cc" --target "$profile" \
	> "$failure_directory/qbe.stdout" 2> "$failure_directory/qbe.stderr"
qbe_failure_status=$?
set -e
test "$qbe_failure_status" -ne 0 || fail "QBE failure succeeded"
printf 'preserve-qbe\n' > "$failure_directory/qbe.expected"
cmp "$failure_directory/qbe.expected" "$failure_directory/qbe-output" >/dev/null ||
	fail "QBE failure replaced output"

printf 'preserve-cc\n' > "$failure_directory/cc-output"
set +e
"$b4" build "$configured_project" --output "$failure_directory/cc-output" \
	--qbe "$qbe" --cc /usr/bin/false --target "$profile" \
	> "$failure_directory/cc.stdout" 2> "$failure_directory/cc.stderr"
cc_failure_status=$?
set -e
test "$cc_failure_status" -ne 0 || fail "CC failure succeeded"
printf 'preserve-cc\n' > "$failure_directory/cc.expected"
cmp "$failure_directory/cc.expected" "$failure_directory/cc-output" >/dev/null ||
	fail "CC failure replaced output"

unsupported_expected=$failure_directory/unsupported.expected
printf 'compiler: unsupported target profile\n' > "$unsupported_expected"
expect_status 64 "$empty_file" "$unsupported_expected" \
	"$b4" build "$configured_project" --output "$failure_directory/unsupported" \
	--qbe "$probe_tool" --cc "$probe_tool" --target unknown-v0
test ! -e "$tool_marker" || fail "unsupported target launched an external tool"
require_no_intermediates "$failure_directory"

space_directory=$workspace/path-with-spaces/'configured project'
mkdir -p "$space_directory"
cp -R "$repository_root/corpus/gate6k/configured-project/." "$space_directory/"
"$b4" build "$space_directory/trbconfig.jsonc" \
	--output "$space_directory/program with spaces" \
	--qbe "$qbe" --cc "$cc" --target "$profile"
"$space_directory/program with spaces" > "$space_directory/stdout" 2> "$space_directory/stderr"
cmp "$workspace/configured/expected" "$space_directory/stdout" >/dev/null ||
	fail "space-bearing project output differs"
require_empty_file "$space_directory/stderr" "space-bearing project stderr differs"
require_no_intermediates "$space_directory"

measurements=$evidence/measurements.csv
printf 'stage,iteration,elapsed_seconds,peak_rss_bytes\n' > "$measurements"

measure_build() {
	stage=$1
	iteration=$2
	seed=$3
	expected_compiler=$4
	measurement_directory=$workspace/measure-$stage-$iteration
	mkdir -p "$measurement_directory"
	measured_output=$measurement_directory/compiler
	time_log=$measurement_directory/time.txt
	stdout_log=$measurement_directory/stdout
	if test "$os" = darwin; then
		/usr/bin/time -p -l \
			"$seed" build "$compiler_entry" --output "$measured_output" \
			--qbe "$qbe" --cc "$cc" --target "$profile" \
			> "$stdout_log" 2> "$time_log"
		elapsed=$(awk '$1 == "real" { print $2; exit }' "$time_log")
		rss=$(awk '/maximum resident set size/ { print $1; exit }' "$time_log")
	else
		/usr/bin/time -f '%e %M' -o "$time_log" \
			"$seed" build "$compiler_entry" --output "$measured_output" \
			--qbe "$qbe" --cc "$cc" --target "$profile" \
			> "$stdout_log" 2> "$measurement_directory/stderr"
		elapsed=$(awk '{ print $1 }' "$time_log")
		rss_kib=$(awk '{ print $2 }' "$time_log")
		rss=$((rss_kib * 1024))
		require_empty_file "$measurement_directory/stderr" "measured build stderr differs"
	fi
	test -n "$elapsed" && test -n "$rss" || fail "could not parse time output"
	require_empty_file "$stdout_log" "measured build stdout differs"
	cmp "$expected_compiler" "$measured_output" >/dev/null || fail "measured compiler bytes differ"
	require_no_intermediates "$measurement_directory"
	printf '%s,%s,%s,%s\n' "$stage" "$iteration" "$elapsed" "$rss" >> "$measurements"
}

for stage_pair in "b1-b2:$b1:$b2" "b2-b3:$b2:$b3" "b3-b4:$b3:$b4"; do
	stage=$(printf '%s\n' "$stage_pair" | cut -d: -f1)
	seed=$(printf '%s\n' "$stage_pair" | cut -d: -f2)
	expected_compiler=$(printf '%s\n' "$stage_pair" | cut -d: -f3)
	warmup=1
	while test "$warmup" -le 2; do
		warmup_directory=$workspace/warmup-$stage-$warmup
		mkdir -p "$warmup_directory"
		"$seed" build "$compiler_entry" --output "$warmup_directory/compiler" \
			--qbe "$qbe" --cc "$cc" --target "$profile"
		cmp "$expected_compiler" "$warmup_directory/compiler" >/dev/null ||
			fail "warmup compiler bytes differ"
		warmup=$((warmup + 1))
	done
	iteration=1
	while test "$iteration" -le 7; do
		measure_build "$stage" "$iteration" "$seed" "$expected_compiler"
		iteration=$((iteration + 1))
	done
done

median_value() {
	stage=$1
	column=$2
	awk -F, -v wanted="$stage" -v selected="$column" \
		'NR > 1 && $1 == wanted { print $selected }' "$measurements" |
		LC_ALL=C sort -n | sed -n '4p'
}

median_b1_b2_time=$(median_value b1-b2 3)
median_b2_b3_time=$(median_value b2-b3 3)
median_b3_b4_time=$(median_value b3-b4 3)
median_b1_b2_rss=$(median_value b1-b2 4)
median_b2_b3_rss=$(median_value b2-b3 4)
median_b3_b4_rss=$(median_value b3-b4 4)

require_within_25_percent() {
	label=$1
	first=$2
	second=$3
	third=$4
	awk -v first="$first" -v second="$second" -v third="$third" 'BEGIN {
		minimum = first
		if (second < minimum) minimum = second
		if (third < minimum) minimum = third
		maximum = first
		if (second > maximum) maximum = second
		if (third > maximum) maximum = third
		exit !(maximum <= minimum * 1.25 && maximum <= minimum * 2.0)
	}' || fail "$label adjacent medians exceed the registered bound"
}

require_within_25_percent elapsed \
	"$median_b1_b2_time" "$median_b2_b3_time" "$median_b3_b4_time"
require_within_25_percent rss \
	"$median_b1_b2_rss" "$median_b2_b3_rss" "$median_b3_b4_rss"

cat > "$evidence/medians.txt" <<EOF
b1-b2 elapsed_seconds=$median_b1_b2_time peak_rss_bytes=$median_b1_b2_rss
b2-b3 elapsed_seconds=$median_b2_b3_time peak_rss_bytes=$median_b2_b3_rss
b3-b4 elapsed_seconds=$median_b3_b4_time peak_rss_bytes=$median_b3_b4_rss
EOF

trace_directory=$workspace/trace
mkdir -p "$trace_directory"
if test "$os" = linux; then
	command -v strace >/dev/null 2>&1 || fail "strace is required on Linux"
	strace -f -e trace=process -o "$evidence/process.trace" \
		"$b4" build "$configured_project" --output "$trace_directory/program" \
		--qbe "$qbe" --cc "$cc" --target "$profile"
	grep 'execve' "$evidence/process.trace" > "$evidence/process-inventory.txt"
	if grep -E 'execve\("[^"]*/(go|trb|sh|bash|zsh)"' "$evidence/process.trace" > /dev/null; then
		fail "ordinary Linux trace contains a forbidden executable"
	fi
	readelf -h "$b4" > "$evidence/executable-header.txt"
	readelf -l "$b4" > "$evidence/executable-segments.txt"
	readelf -d "$b4" > "$evidence/executable-dependencies.txt"
else
	"$b4" build "$configured_project" --output "$trace_directory/program" \
		--qbe "$qbe" --cc "$cc" --target "$profile"
	cat > "$evidence/process-inventory.txt" <<EOF
observer: /bin/sh tools/bootstrap-seed.sh
ordinary compiler stages: B1, B2, B3
Native compiler child boundary: $qbe
Native compiler child boundary: $cc
system assembler/linker: selected by $cc
forbidden ordinary stages: Go, reference trb, recovery compiler, shell child
EOF
	file "$b4" > "$evidence/executable-header.txt"
	otool -L "$b4" > "$evidence/executable-dependencies.txt"
fi
cmp "$workspace/configured/b4/program" "$trace_directory/program" >/dev/null ||
	fail "traced configured executable differs"
require_no_intermediates "$trace_directory"

{
	printf 'mode=%s\n' "$mode"
	printf 'profile=%s\n' "$profile"
	printf 'runner_image=%s\n' "$runner_image"
	printf 'repository_revision=%s\n' "$(git -C "$repository_root" rev-parse HEAD)"
	uname -a
	"$cc" --version
	"$qbe" -h
} > "$evidence/environment.txt" 2>&1

{
	printf '%s  %s\n' "$(sha256 "$input")" input
	printf '%s  %s\n' "$(sha256 "$qbe")" qbe
	printf '%s  %s\n' "$(sha256 "$b1")" b1/compiler
	printf '%s  %s\n' "$(sha256 "$b2")" b2/compiler
	printf '%s  %s\n' "$(sha256 "$b3")" b3/compiler
	printf '%s  %s\n' "$(sha256 "$b4")" b4/compiler
	printf '%s  %s\n' "$(sha256 "$b4.fixed-point.ssa")" b4/fixed-point.ssa
} > "$evidence/SHA256SUMS"

compiler_size=$(file_size "$b4")
test "$compiler_size" -le "$MAX_COMPILER_SIZE" || fail "compiler asset exceeds size bound"
compiler_sha256=$(sha256 "$b4")
qbe_size=$(file_size "$qbe")
qbe_sha256=$(sha256 "$qbe")

cp "$b4" "$output"
chmod 0755 "$output"

jq -n -S \
	--arg profile "$profile" \
	--arg os "$os" \
	--arg architecture "$architecture" \
	--arg runnerImage "$runner_image" \
	--arg qbeTarget "$qbe_target" \
	--arg ccBoundary system-cc \
	--arg asset "$asset_name" \
	--arg mode 0755 \
	--arg sha256 "$compiler_sha256" \
	--arg attestationSubjectSha256 "$compiler_sha256" \
	--arg qbeBinarySha256 "$qbe_sha256" \
	--argjson size "$compiler_size" \
	--argjson qbeBinarySize "$qbe_size" \
	'{
		profile: $profile,
		os: $os,
		architecture: $architecture,
		runnerImage: $runnerImage,
		qbeTarget: $qbeTarget,
		ccBoundary: $ccBoundary,
		asset: $asset,
		mode: $mode,
		size: $size,
		sha256: $sha256,
		attestationSubjectSha256: $attestationSubjectSha256,
		qbeBinarySize: $qbeBinarySize,
		qbeBinarySha256: $qbeBinarySha256
	}' > "$metadata"

require_no_intermediates "$workspace"
printf 'bootstrap-seed: %s %s passed\n' "$mode" "$profile"
