#!/bin/sh
# Check the canonical compiler source against the recovery snapshot subset.
set -eu

reference=${1:?usage: check-bootstrap-snapshot.sh /path/to/pinned/trb [snapshot.json]}
output=${2:-}
if [ "$#" -gt 2 ]; then
	printf 'usage: check-bootstrap-snapshot.sh /path/to/pinned/trb [snapshot.json]\n' >&2
	exit 2
fi

repository_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
stage=$(mktemp -d "${TMPDIR:-/tmp}/native-bootstrap-snapshot.XXXXXX")
trap 'rm -rf "$stage"' 0
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
mkdir "$stage/compiler"
for source in "$repository_root"/compiler/src/*.trb; do
	case "$source" in *_test.trb) continue ;; esac
	cp "$source" "$stage/compiler/$(basename -- "$source")"
done

"$reference" compiler bootstrap-snapshot --snapshot-version 4 \
	"$stage/compiler/compiler.trb" > "$stage/snapshot.json"
test -s "$stage/snapshot.json"
if [ -n "$output" ]; then
	cp "$stage/snapshot.json" "$output"
fi
