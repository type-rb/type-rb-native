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
typerb_go_program=$test_root/typerb-go-program
cat > "$baseline_program" <<'EOF'
#!/bin/sh
printf '%s-output\n' "$1"
EOF
cp "$baseline_program" "$candidate_program"
cp "$baseline_program" "$typerb_go_program"
chmod 0755 "$baseline_program" "$candidate_program" "$typerb_go_program"

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
program_name=$(basename "$1")
candidate=$(printf '%s\n' "$program_name" | sed 's/-worker-program$//; s/-program$//')
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
typerb-go)
	wall=0.100
	cpu=0.095
	memory=1200
	;;
*) exit 64 ;;
esac
case "$program_name" in
*-worker-program)
	case "$candidate" in
	baseline) wall=0.200; cpu=0.190 ;;
	candidate)
		wall=0.120
		cpu=0.115
		if test "${FAKE_ALIAS:-0}" = 1; then
			wall=0.095
			cpu=0.090
		fi
		if test "${FAKE_GROWTH:-0}" = 1; then
			wall=0.085
			cpu=0.080
		fi
		;;
	typerb-go) wall=0.080; cpu=0.075 ;;
	esac
	;;
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
test "$(wc -l < "$test_root/pass-evidence/catastrophic.tsv" | tr -d ' ')" -eq 7 || fail "catastrophic row count differs"
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

worker_expected=$test_root/worker-expected.txt
printf 'native-worker-phase\nnative-worker-ok\n' > "$worker_expected"
for worker_candidate in baseline candidate typerb-go; do
	worker_program=$test_root/$worker_candidate-worker-program
	cat > "$worker_program" <<'EOF'
#!/bin/sh
printf 'native-worker-phase\nnative-worker-ok\n'
EOF
	chmod 0755 "$worker_program"
done
worker_catalog=$test_root/worker-catalog.tsv
printf 'case\tcandidate\tcommand\tinput\texpected\n' > "$worker_catalog"
for worker_candidate in baseline candidate typerb-go; do
	printf 'worker-literal-concat\t%s\t%s\tworker\t%s\n' \
		"$worker_candidate" "$test_root/$worker_candidate-worker-program" "$worker_expected" \
		>> "$worker_catalog"
done
/bin/sh "$script_directory/runtime-controller.sh" \
	test "$fake_runexec" "$worker_catalog" worker-literal-concat 0 "$cache_control" \
	"$test_root/worker-workspace" "$test_root/worker-evidence" \
	> "$test_root/worker.stdout" 2> "$test_root/worker.stderr"
test "$(cat "$test_root/worker.stdout")" = 'native-runtime-ab: worker-literal-concat passed'
test ! -s "$test_root/worker.stderr" || fail "worker controller wrote stderr"
test "$(wc -l < "$test_root/worker-evidence/raw.tsv" | tr -d ' ')" -eq 40 || fail "worker raw row count differs"
test "$(wc -l < "$test_root/worker-evidence/medians.tsv" | tr -d ' ')" -eq 4 || fail "worker median row count differs"
test "$(wc -l < "$test_root/worker-evidence/evaluation.tsv" | tr -d ' ')" -eq 5 || fail "worker evaluation row count differs"
test "$(wc -l < "$test_root/worker-evidence/catastrophic.tsv" | tr -d ' ')" -eq 10 || fail "worker catastrophic row count differs"
test "$(awk -F '\t' '$2 == "walltime" { print $5 }' "$test_root/worker-evidence/evaluation.tsv")" = 0.600000 ||
	fail "worker baseline wall-time ratio differs"
test "$(awk -F '\t' '$2 == "walltime-vs-typerb-go" { print $5 }' "$test_root/worker-evidence/evaluation.tsv")" = 1.500000 ||
	fail "worker Go wall-time ratio differs"

alias_catalog=$test_root/alias-catalog.tsv
sed 's/worker-literal-concat/worker-managed-alias-roots/g' "$worker_catalog" > "$alias_catalog"
FAKE_ALIAS=1 /bin/sh "$script_directory/runtime-controller.sh" \
	test "$fake_runexec" "$alias_catalog" worker-managed-alias-roots 0 "$cache_control" \
	"$test_root/alias-workspace" "$test_root/alias-evidence" \
	> "$test_root/alias.stdout" 2> "$test_root/alias.stderr"
test "$(cat "$test_root/alias.stdout")" = 'native-runtime-ab: worker-managed-alias-roots passed'
test ! -s "$test_root/alias.stderr" || fail "managed-alias controller wrote stderr"
test "$(awk -F= '$1 == "maximum_candidate_ratio" { print $2 }' "$test_root/alias-evidence/environment.txt")" = 0.80 ||
	fail "managed-alias baseline threshold differs"
test "$(awk -F= '$1 == "maximum_candidate_go_ratio" { print $2 }' "$test_root/alias-evidence/environment.txt")" = 1.25 ||
	fail "managed-alias Go threshold differs"
test "$(awk -F '\t' '$2 == "walltime-vs-typerb-go" { print $5 }' "$test_root/alias-evidence/evaluation.tsv")" = 1.187500 ||
	fail "managed-alias Go wall-time ratio differs"

growth_catalog=$test_root/growth-catalog.tsv
sed 's/worker-literal-concat/worker-managed-array-growth/g' "$worker_catalog" > "$growth_catalog"
FAKE_GROWTH=1 /bin/sh "$script_directory/runtime-controller.sh" \
	test "$fake_runexec" "$growth_catalog" worker-managed-array-growth 0 "$cache_control" \
	"$test_root/growth-workspace" "$test_root/growth-evidence" \
	> "$test_root/growth.stdout" 2> "$test_root/growth.stderr"
test "$(cat "$test_root/growth.stdout")" = 'native-runtime-ab: worker-managed-array-growth passed'
test ! -s "$test_root/growth.stderr" || fail "managed-growth controller wrote stderr"
test "$(awk -F= '$1 == "maximum_candidate_ratio" { print $2 }' "$test_root/growth-evidence/environment.txt")" = 0.95 ||
	fail "managed-growth baseline threshold differs"
test "$(awk -F= '$1 == "maximum_candidate_go_ratio" { print $2 }' "$test_root/growth-evidence/environment.txt")" = 1.15 ||
	fail "managed-growth Go threshold differs"
test "$(awk -F '\t' '$2 == "walltime" { print $5 }' "$test_root/growth-evidence/evaluation.tsv")" = 0.425000 ||
	fail "managed-growth baseline wall-time ratio differs"
test "$(awk -F '\t' '$2 == "walltime-vs-typerb-go" { print $5 }' "$test_root/growth-evidence/evaluation.tsv")" = 1.062500 ||
	fail "managed-growth Go wall-time ratio differs"

push_path_catalog=$test_root/push-path-catalog.tsv
sed 's/worker-literal-concat/worker-array-push-fast-path/g' "$worker_catalog" > "$push_path_catalog"
FAKE_GROWTH=1 /bin/sh "$script_directory/runtime-controller.sh" \
	test "$fake_runexec" "$push_path_catalog" worker-array-push-fast-path 0 "$cache_control" \
	"$test_root/push-path-workspace" "$test_root/push-path-evidence" \
	> "$test_root/push-path.stdout" 2> "$test_root/push-path.stderr"
test "$(cat "$test_root/push-path.stdout")" = 'native-runtime-ab: worker-array-push-fast-path passed'
test ! -s "$test_root/push-path.stderr" || fail "push-path controller wrote stderr"
test "$(awk -F= '$1 == "maximum_candidate_ratio" { print $2 }' "$test_root/push-path-evidence/environment.txt")" = 0.95 ||
	fail "push-path baseline threshold differs"
test "$(awk -F= '$1 == "maximum_candidate_go_ratio" { print $2 }' "$test_root/push-path-evidence/environment.txt")" = 1.10 ||
	fail "push-path Go threshold differs"
test "$(awk -F '\t' '$2 == "walltime" { print $5 }' "$test_root/push-path-evidence/evaluation.tsv")" = 0.425000 ||
	fail "push-path baseline wall-time ratio differs"
test "$(awk -F '\t' '$2 == "walltime-vs-typerb-go" { print $5 }' "$test_root/push-path-evidence/evaluation.tsv")" = 1.062500 ||
	fail "push-path Go wall-time ratio differs"

root_push_catalog=$test_root/root-push-catalog.tsv
sed 's/worker-literal-concat/worker-gc-temp-push-fast-path/g' "$worker_catalog" > "$root_push_catalog"
FAKE_GROWTH=1 /bin/sh "$script_directory/runtime-controller.sh" \
	test "$fake_runexec" "$root_push_catalog" worker-gc-temp-push-fast-path 0 "$cache_control" \
	"$test_root/root-push-workspace" "$test_root/root-push-evidence" \
	> "$test_root/root-push.stdout" 2> "$test_root/root-push.stderr"
test "$(cat "$test_root/root-push.stdout")" = 'native-runtime-ab: worker-gc-temp-push-fast-path passed'
test ! -s "$test_root/root-push.stderr" || fail "root-push controller wrote stderr"
test "$(awk -F= '$1 == "maximum_candidate_ratio" { print $2 }' "$test_root/root-push-evidence/environment.txt")" = 0.985 ||
	fail "root-push baseline threshold differs"
test "$(awk -F= '$1 == "maximum_candidate_go_ratio" { print $2 }' "$test_root/root-push-evidence/environment.txt")" = 1.10 ||
	fail "root-push Go threshold differs"
test "$(awk -F '\t' '$2 == "walltime" { print $5 }' "$test_root/root-push-evidence/evaluation.tsv")" = 0.425000 ||
	fail "root-push baseline wall-time ratio differs"
test "$(awk -F '\t' '$2 == "walltime-vs-typerb-go" { print $5 }' "$test_root/root-push-evidence/evaluation.tsv")" = 1.062500 ||
	fail "root-push Go wall-time ratio differs"

initialization_catalog=$test_root/initialization-catalog.tsv
sed 's/worker-literal-concat/worker-managed-initialization/g' "$worker_catalog" > "$initialization_catalog"
FAKE_GROWTH=1 /bin/sh "$script_directory/runtime-controller.sh" \
	test "$fake_runexec" "$initialization_catalog" worker-managed-initialization 0 "$cache_control" \
	"$test_root/initialization-workspace" "$test_root/initialization-evidence" \
	> "$test_root/initialization.stdout" 2> "$test_root/initialization.stderr"
test "$(cat "$test_root/initialization.stdout")" = 'native-runtime-ab: worker-managed-initialization passed'
test ! -s "$test_root/initialization.stderr" || fail "managed-initialization controller wrote stderr"
test "$(awk -F= '$1 == "maximum_candidate_ratio" { print $2 }' "$test_root/initialization-evidence/environment.txt")" = 0.995 ||
	fail "managed-initialization baseline threshold differs"
test "$(awk -F= '$1 == "maximum_candidate_go_ratio" { print $2 }' "$test_root/initialization-evidence/environment.txt")" = 1.10 ||
	fail "managed-initialization Go threshold differs"
test "$(awk -F '\t' '$2 == "walltime" { print $5 }' "$test_root/initialization-evidence/evaluation.tsv")" = 0.425000 ||
	fail "managed-initialization baseline wall-time ratio differs"
test "$(awk -F '\t' '$2 == "walltime-vs-typerb-go" { print $5 }' "$test_root/initialization-evidence/evaluation.tsv")" = 1.062500 ||
	fail "managed-initialization Go wall-time ratio differs"

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
