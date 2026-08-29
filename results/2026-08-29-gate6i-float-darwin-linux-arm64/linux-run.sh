#!/bin/sh

set -eux

repo=/repo
run=/run
entry="$repo/compiler/gate4/src/compiler.trb"
representative="$repo/compiler/gate4/conformance/file-root/main.trb"
float_conformance="$repo/compiler/gate4/conformance/valid/float-scalars.trb"
float_kernel="$repo/corpus/gate6i/float-kernel/src/main.trb"
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

test "$(sha256sum "$run/b1.ssa" | cut -d ' ' -f 1)" = "da3ba99a19f023c8d227a58e77d748ce77e64bfc650d0963aefb3f1512d4217e"
test "$(sha256sum "$run/float-conformance-darwin.ssa" | cut -d ' ' -f 1)" = "5644fe251dd49027848fc191d811532b3f37c4a6a5f146beec66c5f7bb131245"
test "$(sha256sum "$run/float-kernel-darwin.ssa" | cut -d ' ' -f 1)" = "828a9c092f157402aa48d42c81bb3774b19a9945e0bfe1b88cf35fc82873a3fb"

"$qbe" -t arm64 -o "$run/b1.s" "$run/b1.ssa"
"$cc" "$run/b1.s" -Wl,--gc-sections,--strip-all -o "$run/b1"

mkdir -p \
	"$run/b2" \
	"$run/b3" \
	"$run/b4" \
	"$run/representative" \
	"$run/representative-repeat" \
	"$run/float-conformance" \
	"$run/float-conformance-repeat" \
	"$run/float-kernel" \
	"$run/float-kernel-repeat" \
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

"$run/b4/compiler" check "$float_conformance"
"$run/b4/compiler" emit-qbe "$float_conformance" > "$run/float-conformance-linux.ssa"
cmp "$run/float-conformance-darwin.ssa" "$run/float-conformance-linux.ssa"
"$run/b4/compiler" build "$float_conformance" --output "$run/float-conformance/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
"$run/b4/compiler" build "$float_conformance" --output "$run/float-conformance-repeat/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
cmp "$run/float-conformance/program" "$run/float-conformance-repeat/program"
"$run/float-conformance/program" > "$run/float-conformance.stdout"
test "$(cat "$run/float-conformance.stdout")" = "float-scalars-ok"

"$run/b4/compiler" check "$float_kernel"
"$run/b4/compiler" emit-qbe "$float_kernel" > "$run/float-kernel-linux.ssa"
cmp "$run/float-kernel-darwin.ssa" "$run/float-kernel-linux.ssa"
"$run/b4/compiler" build "$float_kernel" --output "$run/float-kernel/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
"$run/b4/compiler" build "$float_kernel" --output "$run/float-kernel-repeat/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
cmp "$run/float-kernel/program" "$run/float-kernel-repeat/program"
"$run/float-kernel/program" > "$run/float-kernel.stdout"
test "$(cat "$run/float-kernel.stdout")" = "float-kernel-ok"

for case_name in float-overflow float-narrowing float-remainder float-method float-malformed; do
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
	"$run/float-conformance-darwin.ssa" \
	"$run/float-conformance-linux.ssa" \
	"$run/float-conformance/program" \
	"$run/float-kernel-darwin.ssa" \
	"$run/float-kernel-linux.ssa" \
	"$run/float-kernel/program"
sha256sum \
	"$entry" \
	"$repo/compiler/gate4/src/storage.trb" \
	"$repo/compiler/gate4/src/path.trb" \
	"$float_conformance" \
	"$float_kernel"
sha256sum \
	"$run/b1.ssa" \
	"$run/b1.s" \
	"$run/b1" \
	"$run/b2/compiler" \
	"$run/b3/compiler" \
	"$run/b4/compiler" \
	"$run/representative/program" \
	"$run/float-conformance-darwin.ssa" \
	"$run/float-conformance-linux.ssa" \
	"$run/float-conformance/program" \
	"$run/float-kernel-darwin.ssa" \
	"$run/float-kernel-linux.ssa" \
	"$run/float-kernel/program"
file \
	"$run/b1" \
	"$run/b2/compiler" \
	"$run/b3/compiler" \
	"$run/b4/compiler" \
	"$run/representative/program" \
	"$run/float-conformance/program" \
	"$run/float-kernel/program"
readelf -l "$run/b4/compiler"
readelf -d "$run/b4/compiler"
readelf -l "$run/representative/program"
readelf -d "$run/representative/program"
readelf -l "$run/float-conformance/program"
readelf -d "$run/float-conformance/program"
readelf -l "$run/float-kernel/program"
readelf -d "$run/float-kernel/program"
cat "$run/representative.stdout"
cat "$run/float-conformance.stdout"
cat "$run/float-kernel.stdout"
cat "$run/process-summary.txt"
