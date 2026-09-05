#!/bin/sh

# Source this file from the controller checkout. Resolve each source checkout
# independently; the historical alternative is not a production compatibility
# alias. Incomplete or duplicate projects must not silently select a baseline.
native_compiler_project_directory() (
	if test "$#" -ne 1 || test ! -d "$1"; then
		printf '%s\n' 'compiler-project: expected one existing repository root' >&2
		exit 1
	fi
	project=$1/compiler
	if test -e "$project/gate4" || test -L "$project/gate4"; then
		if test -e "$project/src" || test -L "$project/src" ||
			test -e "$project/trbconfig.jsonc" || test -L "$project/trbconfig.jsonc"; then
			printf '%s\n' 'compiler-project: ambiguous current and historical layouts' >&2
			exit 1
		fi
		project=$project/gate4
	fi
	if test ! -f "$project/src/compiler.trb" || test ! -f "$project/trbconfig.jsonc"; then
		printf '%s\n' 'compiler-project: incomplete compiler project' >&2
		exit 1
	fi
	printf '%s\n' "$project"
)
