#!/bin/sh

set -eu

if [ "$#" -ne 6 ]; then
	echo "usage: gate4-bootstrap.sh SEED COMPILER_SOURCE QBE CC WORKSPACE GENERATION" >&2
	exit 64
fi

seed=$1
compiler_source=$2
qbe=$3
cc=$4
workspace=$5
generation=$6

mkdir -p "$workspace"
source_text=$(command cat "$compiler_source"; printf x)
source_text=${source_text%x}

"$seed" --source-content emit-qbe "$source_text" > "$workspace/$generation.ssa"
"$qbe" -t arm64_apple "$workspace/$generation.ssa" > "$workspace/$generation.s"
"$cc" "$workspace/$generation.s" -Wl,-dead_strip -o "$workspace/$generation"
