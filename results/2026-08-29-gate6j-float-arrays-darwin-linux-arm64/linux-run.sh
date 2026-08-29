#!/bin/sh

set -eux

repo=/repo
run=/run
entry="$repo/compiler/gate4/src/compiler.trb"
representative="$repo/compiler/gate4/conformance/file-root/main.trb"
scalar_float="$repo/corpus/gate6i/float-kernel/src/main.trb"
float_array_conformance="$repo/compiler/gate4/conformance/valid/float-arrays.trb"
float_array="$repo/corpus/gate6j/float-array/src/main.trb"
float_array_bounds="$repo/compiler/gate4/conformance/runtime-invalid/float-array-bounds.trb"
qbe=/usr/local/bin/qbe
cc=/usr/bin/cc

uname -a
cat /etc/os-release
getconf _NPROCESSORS_ONLN
getconf _PHYS_PAGES
getconf PAGE_SIZE
"$cc" --version
"$qbe" -h
sha256sum "$qbe"
cp /usr/local/share/gate6d-packages.txt "$run/package-inventory.txt"
wc -l "$run/package-inventory.txt"
sha256sum "$run/package-inventory.txt"

test "$(sha256sum "$run/b1.ssa" | cut -d ' ' -f 1)" = "95aba97d9aa07b8eac651336648b7fe53d33e88fa4411edf3f4dad76f8aea4ee"
test "$(sha256sum "$run/float-scalar-darwin.ssa" | cut -d ' ' -f 1)" = "828a9c092f157402aa48d42c81bb3774b19a9945e0bfe1b88cf35fc82873a3fb"
test "$(sha256sum "$run/float-array-conformance-darwin.ssa" | cut -d ' ' -f 1)" = "b8c37290d477049248e861d590b4c1af281fdb75b6ba24b67aae41aa8f367266"
test "$(sha256sum "$run/float-array-darwin.ssa" | cut -d ' ' -f 1)" = "a994fecd55f47b5249955a919ad435de0c250b0a642514a726b445cb9b0d93da"

"$qbe" -t arm64 -o "$run/b1.s" "$run/b1.ssa"
"$cc" "$run/b1.s" -Wl,--gc-sections,--strip-all -o "$run/b1"

mkdir -p \
	"$run/b2" \
	"$run/b3" \
	"$run/b4" \
	"$run/representative" \
	"$run/representative-repeat" \
	"$run/float-scalar" \
	"$run/float-scalar-repeat" \
	"$run/float-array-conformance" \
	"$run/float-array-conformance-repeat" \
	"$run/float-array" \
	"$run/float-array-repeat" \
	"$run/float-array-bounds" \
	"$run/trace"

"$run/b1" check "$entry"
"$run/b1" build "$entry" --output "$run/b2/compiler" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
"$run/b2/compiler" check "$entry"
"$run/b2/compiler" build "$entry" --output "$run/b3/compiler" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
"$run/b3/compiler" check "$entry"
"$run/b3/compiler" build "$entry" --output "$run/b4/compiler" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
"$run/b4/compiler" check "$entry"

cmp "$run/b1" "$run/b2/compiler"
cmp "$run/b2/compiler" "$run/b3/compiler"
cmp "$run/b3/compiler" "$run/b4/compiler"
"$run/b4/compiler" emit-qbe "$entry" > "$run/b4.ssa"
cmp "$run/b1.ssa" "$run/b4.ssa"

"$run/b4/compiler" check "$representative"
"$run/b4/compiler" build "$representative" --output "$run/representative/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
"$run/b4/compiler" build "$representative" --output "$run/representative-repeat/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
cmp "$run/representative/program" "$run/representative-repeat/program"
"$run/representative/program" > "$run/representative.stdout"
test "$(cat "$run/representative.stdout")" = "file-root-ok"
test "$(sha256sum "$run/representative/program" | cut -d ' ' -f 1)" = "6f27705eca2c8666951503b082dc1d05600808d81ecab66b2ac4419ac3ea7073"

"$run/b4/compiler" check "$scalar_float"
"$run/b4/compiler" emit-qbe "$scalar_float" > "$run/float-scalar-linux.ssa"
cmp "$run/float-scalar-darwin.ssa" "$run/float-scalar-linux.ssa"
"$run/b4/compiler" build "$scalar_float" --output "$run/float-scalar/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
"$run/b4/compiler" build "$scalar_float" --output "$run/float-scalar-repeat/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
cmp "$run/float-scalar/program" "$run/float-scalar-repeat/program"
"$run/float-scalar/program" > "$run/float-scalar.stdout"
test "$(cat "$run/float-scalar.stdout")" = "float-kernel-ok"
test "$(sha256sum "$run/float-scalar/program" | cut -d ' ' -f 1)" = "14ce8bf6371687d3c433fccd61a4a3356d61bc91f13a8132ef0868572c4af7f6"

"$run/b4/compiler" check "$float_array_conformance"
"$run/b4/compiler" emit-qbe "$float_array_conformance" > "$run/float-array-conformance-linux.ssa"
cmp "$run/float-array-conformance-darwin.ssa" "$run/float-array-conformance-linux.ssa"
"$run/b4/compiler" build "$float_array_conformance" --output "$run/float-array-conformance/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
"$run/b4/compiler" build "$float_array_conformance" --output "$run/float-array-conformance-repeat/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
cmp "$run/float-array-conformance/program" "$run/float-array-conformance-repeat/program"
"$run/float-array-conformance/program" > "$run/float-array-conformance.stdout"
test "$(cat "$run/float-array-conformance.stdout")" = "float-arrays-ok"

"$run/b4/compiler" check "$float_array"
"$run/b4/compiler" emit-qbe "$float_array" > "$run/float-array-linux.ssa"
cmp "$run/float-array-darwin.ssa" "$run/float-array-linux.ssa"
"$run/b4/compiler" build "$float_array" --output "$run/float-array/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
"$run/b4/compiler" build "$float_array" --output "$run/float-array-repeat/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
cmp "$run/float-array/program" "$run/float-array-repeat/program"
"$run/float-array/program" > "$run/float-array.stdout"
test "$(cat "$run/float-array.stdout")" = "float-array-ok"

"$run/b4/compiler" check "$float_array_bounds"
"$run/b4/compiler" build "$float_array_bounds" --output "$run/float-array-bounds/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
set +e
"$run/float-array-bounds/program" > "$run/float-array-bounds.stdout" 2> "$run/float-array-bounds.stderr"
bounds_status=$?
set -e
test "$bounds_status" = "2"
test ! -s "$run/float-array-bounds.stdout"
test "$(cat "$run/float-array-bounds.stderr")" = "panic: index is out of bounds"

for case_name in float-overflow float-narrowing float-remainder float-method float-malformed float-array-element float-array-immutable float-array-invariance float-array-method; do
	set +e
	actual=$("$run/b4/compiler" check "$repo/compiler/gate4/conformance/invalid/$case_name.source" 2>&1)
	status=$?
	set -e
	test "$status" = "1"
	test "$actual" = "$(cat "$repo/compiler/gate4/conformance/invalid/$case_name.diag")"
done

/usr/bin/strace -f -e trace=process -o "$run/process.trace" \
	"$run/b1" build "$entry" --output "$run/trace/compiler" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
cmp "$run/b2/compiler" "$run/trace/compiler"
grep -E 'execve|clone|vfork|wait' "$run/process.trace" > "$run/process-summary.txt"

find "$run" -name '*.trbn.*' -print > "$run/intermediates.txt"
test ! -s "$run/intermediates.txt"

stat -c '%s %n' \
	"$run/b1.ssa" \
	"$run/b1.s" \
	"$run/b1" \
	"$run/b2/compiler" \
	"$run/b3/compiler" \
	"$run/b4/compiler" \
	"$run/representative/program" \
	"$run/float-scalar-darwin.ssa" \
	"$run/float-scalar-linux.ssa" \
	"$run/float-scalar/program" \
	"$run/float-array-conformance-darwin.ssa" \
	"$run/float-array-conformance-linux.ssa" \
	"$run/float-array-conformance/program" \
	"$run/float-array-darwin.ssa" \
	"$run/float-array-linux.ssa" \
	"$run/float-array/program" \
	"$run/float-array-bounds/program"
sha256sum \
	"$entry" \
	"$repo/compiler/gate4/src/storage.trb" \
	"$repo/compiler/gate4/src/path.trb" \
	"$scalar_float" \
	"$float_array_conformance" \
	"$float_array" \
	"$float_array_bounds"
sha256sum \
	"$run/b1.ssa" \
	"$run/b1.s" \
	"$run/b1" \
	"$run/b2/compiler" \
	"$run/b3/compiler" \
	"$run/b4/compiler" \
	"$run/representative/program" \
	"$run/float-scalar-darwin.ssa" \
	"$run/float-scalar-linux.ssa" \
	"$run/float-scalar/program" \
	"$run/float-array-conformance-darwin.ssa" \
	"$run/float-array-conformance-linux.ssa" \
	"$run/float-array-conformance/program" \
	"$run/float-array-darwin.ssa" \
	"$run/float-array-linux.ssa" \
	"$run/float-array/program" \
	"$run/float-array-bounds/program"
file \
	"$run/b1" \
	"$run/b2/compiler" \
	"$run/b3/compiler" \
	"$run/b4/compiler" \
	"$run/representative/program" \
	"$run/float-scalar/program" \
	"$run/float-array-conformance/program" \
	"$run/float-array/program" \
	"$run/float-array-bounds/program"
readelf -l "$run/b4/compiler"
readelf -d "$run/b4/compiler"
readelf -l "$run/representative/program"
readelf -d "$run/representative/program"
readelf -l "$run/float-scalar/program"
readelf -d "$run/float-scalar/program"
readelf -l "$run/float-array-conformance/program"
readelf -d "$run/float-array-conformance/program"
readelf -l "$run/float-array/program"
readelf -d "$run/float-array/program"
readelf -l "$run/float-array-bounds/program"
readelf -d "$run/float-array-bounds/program"
cat "$run/representative.stdout"
cat "$run/float-scalar.stdout"
cat "$run/float-array-conformance.stdout"
cat "$run/float-array.stdout"
cat "$run/float-array-bounds.stderr"
cat "$run/process-summary.txt"
