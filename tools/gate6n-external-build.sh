#!/bin/sh

set -eu

usage() {
	printf '%s\n' \
		'usage: gate6n-external-build.sh COMPILER SOURCE OUTPUT QBE CC' >&2
	exit 64
}

fail() {
	printf 'gate6n-external-build: %s\n' "$1" >&2
	exit 1
}

test "$#" -eq 5 || usage

compiler=$1
source=$2
output=$3
qbe=$4
cc=$5

test -x "$compiler" || fail "compiler is not executable"
test -f "$source" || fail "source does not exist"
test -x "$qbe" || fail "QBE is not executable"
test -x "$cc" || fail "CC is not executable"
test -d "$(dirname -- "$output")" || fail "output directory does not exist"

temporary_directory=$(mktemp -d "${output}.gate6n-external.XXXXXX")
trap 'rm -rf "$temporary_directory"' EXIT HUP INT TERM

qbe_source=$temporary_directory/output.ssa
assembly=$temporary_directory/output.s
temporary_output=$temporary_directory/$(basename -- "$output")

"$compiler" emit-qbe "$source" > "$qbe_source"
"$qbe" -t amd64_sysv -o "$assembly" "$qbe_source"
"$cc" -xassembler "$assembly" \
	-fuse-ld=lld \
	-Wl,--gc-sections,--strip-all \
	-lm \
	-o "$temporary_output"
mv "$temporary_output" "$output"
