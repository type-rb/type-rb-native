#!/bin/sh
# Run the pull request quick checks that need only the pinned reference
# compiler, cheapest first, and stop at the first failure. The CI planner
# selects documentation-only checks when no code or CLI input changed.
#
# usage: tools/preflight.sh /path/to/pinned/trb [--full]
#
# Build the pinned reference once from a clean checkout at TYPE_RB_REVISION:
#   python3 tools/build-reference.py /path/to/type-rb "$TMPDIR/trb"
# --full adds the reference language fixtures and every root and compiler
# unit. Set TYPE_RB_CHECKOUT to that checkout to also verify the reference AST,
# and TYPE_RB_NATIVE_QBE to a QBE binary for QBE-backed compiler units.
set -eu

reference=${1:?usage: tools/preflight.sh /path/to/pinned/trb [--full]}
full=${2:-}
if [ "$#" -gt 2 ] || { [ -n "$full" ] && [ "$full" != "--full" ]; }; then
	printf 'usage: tools/preflight.sh /path/to/pinned/trb [--full]\n' >&2
	exit 2
fi
case "$reference" in /*) ;; *) reference="$PWD/$reference" ;; esac
test -x "$reference" || { printf 'preflight: %s is not an executable reference compiler\n' "$reference" >&2; exit 2; }
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root"

log=$(mktemp "${TMPDIR:-/tmp}/native-preflight.XXXXXX")
trap 'rm -f "$log"' 0
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

# Each step's output is shown only when it fails; tests may print expected errors.
step() {
	name=$1
	shift
	started=$(date +%s)
	if ! "$@" > "$log" 2>&1; then
		cat "$log" >&2
		printf 'preflight: failed: %s\n' "$name" >&2
		exit 1
	fi
	printf 'ok  %-40s %ss\n' "$name" "$(( $(date +%s) - started ))"
}

base=$(git merge-base HEAD origin/main 2>/dev/null || git rev-parse HEAD)
changed=$( { git diff --name-only "$base"; git ls-files --others --exclude-standard; } | sort -u)
plan=$(printf '%s\n' "$changed" | node --input-type=module -e '
	import { classify } from "./tools/ci-plan.mjs";
	const paths = (await new Promise(resolve => { let data = ""; process.stdin.on("data", chunk => data += chunk); process.stdin.on("end", () => resolve(data)); }))
		.split("\n").filter(Boolean);
	const plan = classify(paths, false, "tiered");
	console.log(plan.code || plan.cli ? "code" : "documentation");
')
printf 'preflight: %s change set against %s\n' "$plan" "$(git rev-parse --short "$base")"

step "whitespace" git diff --check "$base"
step "generated coverage views" sh -c '
	python3 tools/native-language-coverage.py --check-feature-table docs/native-language-feature-inventory.md &&
	python3 tools/native-language-coverage.py --check-pages-data docs/capabilities/ordinary-language.js'
if [ "$plan" = documentation ]; then
	printf 'preflight: documentation checks passed\n'
	exit 0
fi

step "CI planner" node --test tools/ci-plan-test.mjs tools/ci-run-suites-test.mjs tools/recovery-workspace-test.mjs
step "recovery import boundaries" sh -c '
	python3 tools/recovery_layout_sync_test.py &&
	python3 tools/recovery_layout_sync.py --check'
step "reference identity" sh -c '
	python3 -m unittest tools/compatibility_manifest_test.py &&
	python3 tools/compatibility_manifest.py --reference-trb "$1"' preflight "$reference"
step "Unicode data" sh -c 'python3 tools/unicode-identifier-data.py --check && python3 tools/unicode-case-data.py --check'
step "formatting" "$reference" fmt --check src compiler corpus tools benchmarks
step "root types" "$reference" check --config trbconfig.reference.jsonc
step "compiler types" "$reference" check --config compiler/trbconfig.jsonc
step "CLI and core closure" sh tools/check-native-cli.sh "$reference"
step "bootstrap snapshot v4 closure" sh tools/check-bootstrap-snapshot.sh "$reference"
if [ -f tools/project-scenarios.py ]; then
	# Scenarios run with an isolated HOME; share the Go build cache as CI does.
	if [ -z "${GOCACHE:-}" ] && command -v go > /dev/null 2>&1; then
		GOCACHE=$(go env GOCACHE)
		export GOCACHE
	fi
	step "project scenarios against the reference" sh -c '
		python3 tools/project-scenarios-test.py &&
		python3 tools/project-scenarios.py --reference "$1" --jobs 4 > /dev/null' preflight "$reference"
fi

if [ "$full" = --full ]; then
	if [ -n "${TYPE_RB_CHECKOUT:-}" ]; then
		step "language fixtures against the reference" sh -c '
			python3 tools/native-language-coverage.py --reference "$1" --reference-ast "$2/internal/ast/ast.go" --jobs 4 > /dev/null' \
			preflight "$reference" "$TYPE_RB_CHECKOUT"
	else
		step "language fixtures against the reference" sh -c '
			python3 tools/native-language-coverage.py --reference "$1" --jobs 4 > /dev/null' preflight "$reference"
	fi
	step "root units" env TYPE_RB_NATIVE_ROOT="$root" "$reference" test --config trbconfig.reference.jsonc
	step "compiler units" env TYPE_RB_NATIVE_ROOT="$root" "$reference" test --config compiler/trbconfig.jsonc
fi
printf 'preflight: passed\n'
