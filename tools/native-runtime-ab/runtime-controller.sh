#!/bin/sh

set -eu

BENCH_EXEC_VERSION=3.35
MEMORY_LIMIT=4GB
WARMUP_ROUNDS=2
RETAINED_ROUNDS=11
CATALOG_HEADER='case\tcandidate\tcommand\tinput\texpected'
RAW_HEADER='phase\tround\tretained_index\torder\tcase\tcandidate\tverdict\treturnvalue\texitsignal\tterminationreason\twalltime_seconds\tcputime_seconds\tmemory_bytes'

usage() {
	cat >&2 <<'EOF'
usage: runtime-controller.sh test|formal RUNEXEC CATALOG CASE CORE
       CACHE_CONTROL WORKSPACE EVIDENCE
EOF
	exit 64
}

fail() {
	printf 'native-runtime-ab: %s\n' "$1" >&2
	exit 1
}

measurement_value() {
	key=$1
	path=$2
	awk -F= -v wanted="$key" '
		$1 == wanted {
			count += 1
			value = substr($0, length($1) + 2)
		}
		END {
			if (count > 1) exit 1
			if (count == 1) print value
		}
	' "$path"
}

is_decimal() {
	awk -v value="$1" 'BEGIN { exit !(value ~ /^[0-9]+([.][0-9]+)?$/) }'
}

is_unsigned() {
	case "$1" in
	'' | *[!0-9]*) return 1 ;;
	*) return 0 ;;
	esac
}

sha256() {
	if command -v sha256sum >/dev/null 2>&1; then
		sha256sum "$1" | awk '{ print $1 }'
	else
		shasum -a 256 "$1" | awk '{ print $1 }'
	fi
}

core_is_allowed() {
	awk -v wanted="$1" -v list="$2" 'BEGIN {
		count = split(list, groups, ",")
		for (group_index = 1; group_index <= count; group_index += 1) {
			parts = split(groups[group_index], bounds, "-")
			first = bounds[1] + 0
			last = parts == 1 ? first : bounds[2] + 0
			if (wanted >= first && wanted <= last) exit 0
		}
		exit 1
	}'
}

test "$#" -eq 8 || usage
mode=$1
runexec=$2
catalog=$3
case_name=$4
core=$5
cache_control=$6
workspace=$7
evidence=$8

case "$mode" in
test | formal) ;;
*) usage ;;
esac
case "$case_name" in
fannkuch-redux)
	total_candidates=2
	candidates='baseline candidate'
	walltime_limit=60s
	formal_input=10
	formal_expected_sha256=26f4debed9b9f8db7609e17f35756a3f72c1d85d40977a4377a1ef34ffc4d4c8
	maximum_ratio=0.97
	;;
n-body)
	total_candidates=2
	candidates='baseline candidate'
	walltime_limit=60s
	formal_input=1000000
	formal_expected_sha256=3fb938822f2b87322baee13eea59620bab076cca553f7e01214dbc674bd09387
	maximum_ratio=1.02
	;;
spectral-norm)
	total_candidates=2
	candidates='baseline candidate'
	walltime_limit=120s
	formal_input=5500
	formal_expected_sha256=f9d5b5e3eb7657cf1bbba4cc856651864df9cd9fd9a6be9b9bc5fcbb67150deb
	maximum_ratio=1.02
	;;
worker-literal-concat)
	total_candidates=3
	candidates='baseline candidate typerb-go'
	walltime_limit=120s
	formal_input=worker
	formal_expected_sha256=a9573e85b80396055215ddf53485572f06b4be54c2899b525e614ff023b6f76d
	maximum_ratio=0.70
	maximum_go_ratio=2.00
	;;
worker-managed-alias-roots)
	total_candidates=3
	candidates='baseline candidate typerb-go'
	walltime_limit=120s
	formal_input=worker
	formal_expected_sha256=a9573e85b80396055215ddf53485572f06b4be54c2899b525e614ff023b6f76d
	maximum_ratio=0.80
	maximum_go_ratio=1.25
	;;
worker-managed-array-growth)
	total_candidates=3
	candidates='baseline candidate typerb-go'
	walltime_limit=120s
	formal_input=worker
	formal_expected_sha256=a9573e85b80396055215ddf53485572f06b4be54c2899b525e614ff023b6f76d
	maximum_ratio=0.95
	maximum_go_ratio=1.15
	;;
worker-array-push-fast-path)
	total_candidates=3
	candidates='baseline candidate typerb-go'
	walltime_limit=120s
	formal_input=worker
	formal_expected_sha256=a9573e85b80396055215ddf53485572f06b4be54c2899b525e614ff023b6f76d
	maximum_ratio=0.95
	maximum_go_ratio=1.10
	;;
*) usage ;;
esac

test -x "$runexec" || fail "runexec is not executable"
test -f "$catalog" || fail "catalog does not exist"
test -x "$cache_control" || fail "cache-control command is not executable"
test ! -e "$workspace" || fail "workspace already exists"
test ! -e "$evidence" || fail "evidence path already exists"
case "$core" in
'' | *[!0-9]*) fail "core must be one CPU identifier" ;;
esac

if test "$mode" = formal; then
	test "$(uname -s)" = Linux || fail "formal mode requires Linux"
	case "$(uname -m)" in
	aarch64 | arm64) ;;
	*) fail "formal mode requires Linux arm64" ;;
	esac
	runexec_version=$("$runexec" --version)
	test "$runexec_version" = "runexec $BENCH_EXEC_VERSION" ||
		fail "formal mode requires runexec $BENCH_EXEC_VERSION: $runexec_version"
	allowed_cores=$(awk -F: '$1 == "Cpus_allowed_list" { gsub(/[[:space:]]/, "", $2); print $2 }' /proc/self/status)
	test -n "$allowed_cores" || fail "cannot determine the allowed CPU set"
	core_is_allowed "$core" "$allowed_cores" ||
		fail "CPU $core is outside the allowed CPU set $allowed_cores"
else
	runexec_version=$("$runexec" --version 2>/dev/null || printf 'test-double\n')
	allowed_cores=test-mode
fi

actual_header=$(sed -n '1p' "$catalog")
expected_header=$(printf "$CATALOG_HEADER")
test "$actual_header" = "$expected_header" || fail "catalog header differs"
awk -F '\t' 'NR > 1 && NF != 5 { exit 1 }' "$catalog" || fail "catalog rows must have five fields"
catalog_rows=$(awk -F '\t' -v wanted="$case_name" 'NR > 1 && $1 == wanted { count += 1 } END { print count + 0 }' "$catalog")
test "$catalog_rows" -eq "$total_candidates" ||
	fail "$case_name must have $total_candidates candidates"

mkdir -p "$workspace" "$evidence/correctness" "$evidence/observations"
case_catalog=$workspace/catalog.tsv
awk -F '\t' -v wanted="$case_name" 'NR > 1 && $1 == wanted { print }' "$catalog" > "$case_catalog"

tab=$(printf '\t')
candidate_position=1
for expected_candidate in $candidates; do
	row=$(sed -n "${candidate_position}p" "$case_catalog")
	IFS="$tab" read -r row_case actual_candidate command input expected <<EOF
$row
EOF
	test "$actual_candidate" = "$expected_candidate" ||
		fail "candidate $candidate_position must be $expected_candidate"
	if test "$mode" = formal; then
		test "$input" = "$formal_input" || fail "$actual_candidate formal input differs"
		test -f "$expected" || fail "$actual_candidate expected output is missing"
		test "$(sha256 "$expected")" = "$formal_expected_sha256" ||
			fail "$actual_candidate expected output SHA-256 differs"
	fi
	candidate_position=$((candidate_position + 1))
done

{
	printf 'mode=%s\n' "$mode"
	printf 'case=%s\n' "$case_name"
	printf 'core=%s\n' "$core"
	printf 'memory_limit=%s\n' "$MEMORY_LIMIT"
	printf 'walltime_limit=%s\n' "$walltime_limit"
	printf 'warmup_rounds=%s\n' "$WARMUP_ROUNDS"
	printf 'retained_rounds=%s\n' "$RETAINED_ROUNDS"
	printf 'candidates=%s\n' "$candidates"
	printf 'maximum_candidate_ratio=%s\n' "$maximum_ratio"
	if test "$total_candidates" -eq 3; then
		printf 'maximum_candidate_go_ratio=%s\n' "$maximum_go_ratio"
	fi
	printf 'runexec=%s\n' "$runexec"
	printf 'runexec_version=%s\n' "$runexec_version"
	printf 'allowed_cores=%s\n' "$allowed_cores"
	printf 'cache_control=%s\n' "$cache_control"
	printf 'network_access=disabled-by-default-container-policy\n'
	printf 'root_filesystem=read-only\n'
	printf 'home_filesystem=isolated-overlay\n'
	uname -a | sed 's/^/uname=/'
} > "$evidence/environment.txt"

printf 'case\tcandidate\tstatus\tstderr_empty\tstdout_exact\n' > "$evidence/correctness/summary.tsv"
correctness_failures=0
while IFS="$tab" read -r row_case candidate command input expected; do
	test -x "$command" || fail "$candidate command is not executable: $command"
	test -f "$expected" || fail "$candidate expected output is missing: $expected"
	correctness_directory=$evidence/correctness/$candidate
	mkdir -p "$correctness_directory"
	set +e
	"$command" "$input" > "$correctness_directory/stdout" 2> "$correctness_directory/stderr"
	correctness_status=$?
	set -e
	stderr_empty=true
	stdout_exact=true
	if test -s "$correctness_directory/stderr"; then
		stderr_empty=false
		correctness_failures=$((correctness_failures + 1))
	fi
	if ! cmp "$expected" "$correctness_directory/stdout" >/dev/null; then
		stdout_exact=false
		correctness_failures=$((correctness_failures + 1))
	fi
	if test "$correctness_status" -ne 0; then
		correctness_failures=$((correctness_failures + 1))
	fi
	printf '%s\t%s\t%s\t%s\t%s\n' \
		"$case_name" "$candidate" "$correctness_status" "$stderr_empty" "$stdout_exact" \
		>> "$evidence/correctness/summary.tsv"
done < "$case_catalog"
test "$correctness_failures" -eq 0 || fail "correctness failed; timing was not started"

raw=$evidence/raw.tsv
printf "$RAW_HEADER\n" > "$raw"
total_rounds=$((WARMUP_ROUNDS + RETAINED_ROUNDS))
measurement_failures=0
round=1
while test "$round" -le "$total_rounds"; do
	if test "$round" -le "$WARMUP_ROUNDS"; then
		phase=warmup
		retained_index=0
	else
		phase=retained
		retained_index=$((round - WARMUP_ROUNDS))
	fi
	order=1
	while test "$order" -le "$total_candidates"; do
		candidate_position=$(((round + order - 2) % total_candidates + 1))
		row=$(sed -n "${candidate_position}p" "$case_catalog")
		IFS="$tab" read -r row_case candidate command input expected <<EOF
$row
EOF
		observation=$evidence/observations/round-$round-order-$order-$candidate
		mkdir -p "$observation"
		"$cache_control" "$observation/cache.txt" \
			> "$observation/cache.stdout" 2> "$observation/cache.stderr" ||
			fail "cache control failed for round $round order $order"

		set +e
		"$runexec" \
			--quiet \
			--memlimit "$MEMORY_LIMIT" \
			--walltimelimit "$walltime_limit" \
			--cores "$core" \
			--read-only-dir / \
			--overlay-dir /home \
			--output "$observation/run.log" \
			-- "$command" "$input" \
			> "$observation/runexec.stdout" \
			2> "$observation/runexec.stderr"
		runexec_status=$?
		set -e
		test "$runexec_status" -eq 0 || fail "runexec infrastructure failed for round $round order $order"
		test -f "$observation/run.log" || fail "runexec did not produce a run log"
		test "$(sed -n '4p' "$observation/run.log")" = '--------------------------------------------------------------------------------' ||
			fail "runexec log header differs for round $round order $order"
		sed '1,6d' "$observation/run.log" > "$observation/payload.stdout"

		returnvalue=$(measurement_value returnvalue "$observation/runexec.stdout") || fail "runexec repeated returnvalue"
		exitsignal=$(measurement_value exitsignal "$observation/runexec.stdout") || fail "runexec repeated exitsignal"
		terminationreason=$(measurement_value terminationreason "$observation/runexec.stdout") || fail "runexec repeated terminationreason"
		walltime=$(measurement_value walltime "$observation/runexec.stdout") || fail "runexec repeated walltime"
		cputime=$(measurement_value cputime "$observation/runexec.stdout") || fail "runexec repeated cputime"
		memory=$(measurement_value memory "$observation/runexec.stdout") || fail "runexec repeated memory"
		walltime=${walltime%s}
		cputime=${cputime%s}
		memory=${memory%B}

		verdict=pass
		if test -z "$walltime" || test -z "$cputime" || test -z "$memory"; then
			verdict=measurement-missing
		elif ! is_decimal "$walltime" || ! is_decimal "$cputime" || ! is_unsigned "$memory"; then
			verdict=measurement-invalid
		elif test -n "$returnvalue" && ! is_unsigned "$returnvalue"; then
			verdict=exit-invalid
		elif test -n "$exitsignal" && ! is_unsigned "$exitsignal"; then
			verdict=exit-invalid
		elif test -n "$returnvalue" && test -n "$exitsignal"; then
			verdict=exit-ambiguous
		elif test -z "$returnvalue" && test -z "$exitsignal"; then
			verdict=exit-missing
		elif test -n "$terminationreason"; then
			verdict=terminated-$terminationreason
		elif test -n "$exitsignal"; then
			verdict=signal-$exitsignal
		elif test "$returnvalue" -ne 0; then
			verdict=return-$returnvalue
		elif ! cmp "$expected" "$observation/payload.stdout" >/dev/null; then
			verdict=output-diff
		fi
		if test "$verdict" != pass; then
			measurement_failures=$((measurement_failures + 1))
		fi
		printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
			"$phase" "$round" "$retained_index" "$order" "$case_name" "$candidate" \
			"$verdict" "$returnvalue" "$exitsignal" "$terminationreason" "$walltime" "$cputime" "$memory" \
			>> "$raw"
		order=$((order + 1))
	done
	round=$((round + 1))
done

script_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
awk -v candidates="$candidates" -v retained_rounds="$RETAINED_ROUNDS" \
	-f "$script_directory/summarize.awk" "$raw" > "$evidence/medians.tsv" ||
	fail "measurement summary could not be generated"

catastrophic=$evidence/catastrophic.tsv
printf 'case\tcandidate\tmetric\tmedian\tmaximum_observation\tmaximum_median_ratio\tmaximum_ratio\tstatus\n' \
	> "$catastrophic"
catastrophic_failures=0
for measured_candidate in $candidates; do
	for metric in walltime cputime memory; do
		case "$metric" in
		walltime) raw_column=11; median_column=5 ;;
		cputime) raw_column=12; median_column=6 ;;
		memory) raw_column=13; median_column=7 ;;
		esac
		median=$(awk -F '\t' -v column="$median_column" -v wanted="$measured_candidate" \
			'$2 == wanted && $8 == "pass" { print $column }' "$evidence/medians.tsv")
		maximum=$(awk -F '\t' -v column="$raw_column" -v wanted="$measured_candidate" \
			'$1 == "retained" && $6 == wanted && $7 == "pass" {
				if (!found || $column + 0 > maximum + 0) maximum = $column
				found = 1
			} END { if (found) print maximum }' "$raw")
		status=pass
		ratio=
		if test -z "$median" || test -z "$maximum"; then
			status=incomplete
			catastrophic_failures=$((catastrophic_failures + 1))
		else
			ratio=$(awk -v median="$median" -v maximum="$maximum" \
				'BEGIN { printf "%.6f", maximum / median }')
			if ! awk -v ratio="$ratio" 'BEGIN { exit !(ratio <= 2.00) }'; then
				status=fail
				catastrophic_failures=$((catastrophic_failures + 1))
			fi
		fi
		printf '%s\t%s\t%s\t%s\t%s\t%s\t2.00\t%s\n' \
			"$case_name" "$measured_candidate" "$metric" "$median" "$maximum" "$ratio" "$status" \
			>> "$catastrophic"
	done
done

evaluation=$evidence/evaluation.tsv
printf 'case\tmetric\treference\tsubject\tsubject_reference_ratio\tmaximum_ratio\tstatus\n' > "$evaluation"
evaluation_failures=0
references=baseline
if test "$total_candidates" -eq 3; then
	references='baseline typerb-go'
fi
for metric in walltime cputime; do
	case "$metric" in
	walltime) column=5 ;;
	cputime) column=6 ;;
	esac
	candidate=$(awk -F '\t' -v column="$column" '$2 == "candidate" && $8 == "pass" { print $column }' "$evidence/medians.tsv")
	for reference in $references; do
		baseline=$(awk -F '\t' -v column="$column" -v wanted="$reference" \
			'$2 == wanted && $8 == "pass" { print $column }' "$evidence/medians.tsv")
		comparison_maximum=$maximum_ratio
		metric_label=$metric
		if test "$reference" = typerb-go; then
			comparison_maximum=$maximum_go_ratio
			metric_label=$metric-vs-typerb-go
		fi
		status=pass
		ratio=
		if test -z "$baseline" || test -z "$candidate"; then
			status=incomplete
			evaluation_failures=$((evaluation_failures + 1))
		else
			ratio=$(awk -v baseline="$baseline" -v candidate="$candidate" 'BEGIN { printf "%.6f", candidate / baseline }')
			if ! awk -v ratio="$ratio" -v maximum="$comparison_maximum" 'BEGIN { exit !(ratio <= maximum) }'; then
				status=fail
				evaluation_failures=$((evaluation_failures + 1))
			fi
		fi
		printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
			"$case_name" "$metric_label" "$baseline" "$candidate" "$ratio" \
			"$comparison_maximum" "$status" >> "$evaluation"
	done
done

test "$measurement_failures" -eq 0 || fail "$measurement_failures measured runs failed; raw evidence is retained"
test "$catastrophic_failures" -eq 0 || fail "$case_name catastrophic observation threshold failed"
test "$evaluation_failures" -eq 0 || fail "$case_name performance threshold failed"
printf 'native-runtime-ab: %s passed\n' "$case_name"
