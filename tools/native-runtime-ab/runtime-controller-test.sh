#!/bin/sh

set -eu

fail() {
	printf 'native-runtime-ab-test: %s\n' "$1" >&2
	exit 1
}

script_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
test_root=$(mktemp -d "${TMPDIR:-/tmp}/type-rb-native-runtime-ab.XXXXXX")
trap 'rm -rf "$test_root"' 0
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

baseline_program=$test_root/baseline-program
candidate_program=$test_root/candidate-program
cat > "$baseline_program" <<'EOF'
#!/bin/sh
printf '%s-output\n' "$1"
EOF
cp "$baseline_program" "$candidate_program"
chmod 0755 "$baseline_program" "$candidate_program"

fake_runexec=$test_root/runexec
cat > "$fake_runexec" <<'EOF'
#!/bin/sh
set -eu
if test "${1:-}" = --version; then
	printf 'runexec 3.35-test\n'
	exit 0
fi
output=
while test "$#" -gt 0; do
	case "$1" in
	--quiet) shift ;;
	--memlimit | --walltimelimit | --cores | --read-only-dir | --overlay-dir | --output)
		option=$1
		value=$2
		shift 2
		if test "$option" = --output; then output=$value; fi
		;;
	--) shift; break ;;
	*) exit 64 ;;
	esac
done
test -n "$output"
candidate=$(basename "$1" | sed 's/-program$//')
case "$candidate" in
baseline)
	wall=0.200
	cpu=0.190
	memory=1000
	;;
candidate)
	wall=0.150
	cpu=0.140
	memory=1100
	if test "${FAKE_REGRESSION:-0}" = 1; then
		wall=0.220
		cpu=0.210
	fi
	;;
*) exit 64 ;;
esac
payload=$output.payload
set +e
"$@" > "$payload" 2>&1
actual_status=$?
set -e
if test "${FAKE_FAIL_CANDIDATE:-}" = "$candidate"; then actual_status=9; fi
{
	printf '%s\n\n\n' "$*"
	printf '%s\n\n\n' '--------------------------------------------------------------------------------'
	cat "$payload"
} > "$output"
printf 'starttime=2026-08-31T00:00:00+00:00\n'
printf 'returnvalue=%s\n' "$actual_status"
printf 'walltime=%ss\n' "$wall"
printf 'cputime=%ss\n' "$cpu"
printf 'memory=%sB\n' "$memory"
EOF
chmod 0755 "$fake_runexec"

cache_control=$test_root/cache-control
cat > "$cache_control" <<'EOF'
#!/bin/sh
set -eu
test "$#" -eq 1
printf 'cache_control=test\n' > "$1"
EOF
chmod 0755 "$cache_control"

expected=$test_root/expected.txt
printf 'spectral-norm-output\n' > "$expected"
catalog=$test_root/catalog.tsv
printf 'case\tcandidate\tcommand\tinput\texpected\n' > "$catalog"
printf 'spectral-norm\tbaseline\t%s\tspectral-norm\t%s\n' "$baseline_program" "$expected" >> "$catalog"
printf 'spectral-norm\tcandidate\t%s\tspectral-norm\t%s\n' "$candidate_program" "$expected" >> "$catalog"

/bin/sh "$script_directory/runtime-controller.sh" \
	test "$fake_runexec" "$catalog" spectral-norm 0 "$cache_control" \
	"$test_root/pass-workspace" "$test_root/pass-evidence" \
	> "$test_root/pass.stdout" 2> "$test_root/pass.stderr"
test "$(cat "$test_root/pass.stdout")" = 'native-runtime-ab: spectral-norm passed'
test ! -s "$test_root/pass.stderr" || fail "passing controller wrote stderr"
test "$(wc -l < "$test_root/pass-evidence/raw.tsv" | tr -d ' ')" -eq 27 || fail "raw row count differs"
test "$(wc -l < "$test_root/pass-evidence/medians.tsv" | tr -d ' ')" -eq 3 || fail "median row count differs"
test "$(find "$test_root/pass-evidence/observations" -name runexec.stdout -type f | wc -l | tr -d ' ')" -eq 26 ||
	fail "observation count differs"
awk -F '\t' '
	NR == 2 && !($1 == "warmup" && $2 == 1 && $4 == 1 && $6 == "baseline") { exit 1 }
	NR == 4 && !($2 == 2 && $4 == 1 && $6 == "candidate") { exit 1 }
' "$test_root/pass-evidence/raw.tsv" || fail "rotation order differs"
awk -F '\t' '
	$2 == "candidate" {
		found += 1
		if (!($3 == 11 && $4 == 11 && $5 == 0.15 && $6 == 0.14 && $7 == 1100 && $8 == "pass")) exit 1
	}
	END { exit !(found == 1) }
' "$test_root/pass-evidence/medians.tsv" || fail "median values differ"
test "$(awk -F '\t' '$2 == "walltime" { print $5 }' "$test_root/pass-evidence/evaluation.tsv")" = 0.750000 ||
	fail "wall-time ratio differs"

set +e
FAKE_REGRESSION=1 /bin/sh "$script_directory/runtime-controller.sh" \
	test "$fake_runexec" "$catalog" spectral-norm 0 "$cache_control" \
	"$test_root/regression-workspace" "$test_root/regression-evidence" \
	> "$test_root/regression.stdout" 2> "$test_root/regression.stderr"
regression_status=$?
set -e
test "$regression_status" -ne 0 || fail "threshold regression passed"
test "$(find "$test_root/regression-evidence/observations" -name runexec.stdout -type f | wc -l | tr -d ' ')" -eq 26 ||
	fail "threshold failure stopped observations"
test "$(awk -F '\t' '$7 == "fail" { count += 1 } END { print count + 0 }' "$test_root/regression-evidence/evaluation.tsv")" -eq 2 ||
	fail "threshold failures were not recorded"

set +e
FAKE_FAIL_CANDIDATE=candidate /bin/sh "$script_directory/runtime-controller.sh" \
	test "$fake_runexec" "$catalog" spectral-norm 0 "$cache_control" \
	"$test_root/failure-workspace" "$test_root/failure-evidence" \
	> "$test_root/failure.stdout" 2> "$test_root/failure.stderr"
failure_status=$?
set -e
test "$failure_status" -ne 0 || fail "measured failure passed"
test "$(awk -F '\t' '$1 == "retained" && $6 == "candidate" && $7 == "return-9" { count += 1 } END { print count + 0 }' "$test_root/failure-evidence/raw.tsv")" -eq 11 ||
	fail "retained failures differ"
test "$(find "$test_root/failure-evidence/observations" -name runexec.stdout -type f | wc -l | tr -d ' ')" -eq 26 ||
	fail "measured failure stopped observations"

incorrect_candidate=$test_root/incorrect-candidate
cat > "$incorrect_candidate" <<'EOF'
#!/bin/sh
printf 'unexpected diagnostic\n' >&2
printf '%s-output\n' "$1"
EOF
chmod 0755 "$incorrect_candidate"
incorrect_catalog=$test_root/incorrect-catalog.tsv
printf 'case\tcandidate\tcommand\tinput\texpected\n' > "$incorrect_catalog"
printf 'spectral-norm\tbaseline\t%s\tspectral-norm\t%s\n' "$baseline_program" "$expected" >> "$incorrect_catalog"
printf 'spectral-norm\tcandidate\t%s\tspectral-norm\t%s\n' "$incorrect_candidate" "$expected" >> "$incorrect_catalog"
set +e
/bin/sh "$script_directory/runtime-controller.sh" \
	test "$fake_runexec" "$incorrect_catalog" spectral-norm 0 "$cache_control" \
	"$test_root/incorrect-workspace" "$test_root/incorrect-evidence" \
	> "$test_root/incorrect.stdout" 2> "$test_root/incorrect.stderr"
incorrect_status=$?
set -e
test "$incorrect_status" -ne 0 || fail "incorrect program reached timing"
test ! -e "$test_root/incorrect-evidence/raw.tsv" || fail "timing data exists after correctness failure"
test "$(find "$test_root/incorrect-evidence/observations" -name runexec.stdout -type f | wc -l | tr -d ' ')" -eq 0 ||
	fail "runexec started after correctness failure"

printf 'native-runtime-ab-test: passed\n'
