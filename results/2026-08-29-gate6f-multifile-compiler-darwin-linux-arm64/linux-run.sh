#!/bin/sh

set -eux

repo=/repo
run=/run
entry="$repo/compiler/gate4/src/compiler.trb"
application_entry="$repo/compiler/gate4/conformance/file-root/main.trb"
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
dpkg-query -W -f='${binary:Package}\t${Version}\n' > "$run/package-inventory.txt"
wc -l "$run/package-inventory.txt"
sha256sum "$run/package-inventory.txt"

"$qbe" -t arm64 -o "$run/b1.s" "$run/b1.ssa"
"$cc" "$run/b1.s" -Wl,--gc-sections,--strip-all -o "$run/b1"

mkdir -p "$run/b2" "$run/b3" "$run/b4" "$run/application" "$run/application-repeat" "$run/trace"

"$run/b1" check "$entry"
"$run/b1" build "$entry" --output "$run/b2/compiler" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
"$run/b2/compiler" check "$entry"
"$run/b2/compiler" build "$entry" --output "$run/b3/compiler" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
"$run/b3/compiler" check "$entry"
"$run/b3/compiler" build "$entry" --output "$run/b4/compiler" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
"$run/b4/compiler" check "$entry"

cmp "$run/b2/compiler" "$run/b3/compiler"
cmp "$run/b3/compiler" "$run/b4/compiler"
"$run/b4/compiler" emit-qbe "$entry" > "$run/b4.ssa"
cmp "$run/b1.ssa" "$run/b4.ssa"

"$run/b4/compiler" check "$application_entry"
"$run/b4/compiler" build "$application_entry" --output "$run/application/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
"$run/b4/compiler" build "$application_entry" --output "$run/application-repeat/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
cmp "$run/application/program" "$run/application-repeat/program"
"$run/application/program" > "$run/application.stdout"
test "$(cat "$run/application.stdout")" = "file-root-ok"

/usr/bin/strace -f -e trace=process -o "$run/process.trace" \
	"$run/b1" build "$entry" --output "$run/trace/compiler" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
cmp "$run/b2/compiler" "$run/trace/compiler"
grep -E 'execve|clone|vfork|wait' "$run/process.trace" > "$run/process-summary.txt"

find "$run" -name '*.trbn.*' -print > "$run/intermediates.txt"
test ! -s "$run/intermediates.txt"

stat -c '%s %n' "$run/b1.ssa" "$run/b1.s" "$run/b1" "$run/b2/compiler" "$run/b3/compiler" "$run/b4/compiler" "$run/application/program"
sha256sum "$entry" "$repo/compiler/gate4/src/storage.trb" "$repo/compiler/gate4/src/path.trb"
sha256sum "$run/b1.ssa" "$run/b1.s" "$run/b1" "$run/b2/compiler" "$run/b3/compiler" "$run/b4/compiler" "$run/application/program"
file "$run/b1" "$run/b2/compiler" "$run/b3/compiler" "$run/b4/compiler" "$run/application/program"
readelf -l "$run/b4/compiler"
readelf -d "$run/b4/compiler"
readelf -l "$run/application/program"
readelf -d "$run/application/program"
cat "$run/application.stdout"
cat "$run/process-summary.txt"
