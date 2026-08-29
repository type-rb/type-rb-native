#!/bin/sh

set -eux

repo=/repo
run=/run
entry="$repo/compiler/gate4/src/compiler.trb"
application_entry="$repo/compiler/gate4/conformance/file-root/main.trb"
scale_project="$run/scale-project"
scale_entry="$scale_project/main.trb"
scale_manifest="$run/scale-project.manifest"
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

set +x
mkdir -p "$scale_project"
: > "$scale_manifest"
i=0
while [ "$i" -lt 1024 ]; do
	name=$(printf '%04d' "$i")
	file="m$name.trb"
	if [ "$i" -eq 0 ]; then
		printf 'def f%s(): Integer\n\treturn 1\nend\n' "$name" > "$scale_project/$file"
	else
		previous=$(printf '%04d' "$((i - 1))")
		printf 'import { f%s } from m%s\n\ndef f%s(): Integer\n\treturn f%s() + 1\nend\n' \
			"$previous" "$previous" "$name" "$previous" > "$scale_project/$file"
	fi
	printf '=== %s ===\n' "$file" >> "$scale_manifest"
	cat "$scale_project/$file" >> "$scale_manifest"
	i=$((i + 1))
done
printf 'import { f1023 } from m1023\n\ndef main()\n\tif f1023() == 1024\n\t\tputs("module-scale-ok")\n\telse\n\t\tputs("module-scale-bad")\n\tend\n\treturn\nend\n' > "$scale_entry"
printf '=== main.trb ===\n' >> "$scale_manifest"
cat "$scale_entry" >> "$scale_manifest"
test "$(find "$scale_project" -type f -name '*.trb' | wc -l | tr -d ' ')" = "1025"
test "$(sha256sum "$scale_manifest" | cut -d ' ' -f 1)" = "db438159189ba944283d8a92a09a1176020522c67d2551065c4010c50858f16b"
set -x

"$qbe" -t arm64 -o "$run/b1.s" "$run/b1.ssa"
"$cc" "$run/b1.s" -Wl,--gc-sections,--strip-all -o "$run/b1"

mkdir -p \
	"$run/b2" \
	"$run/b3" \
	"$run/b4" \
	"$run/application" \
	"$run/application-repeat" \
	"$run/scale-application" \
	"$run/scale-application-repeat" \
	"$run/trace"

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
test "$(sha256sum "$run/application/program" | cut -d ' ' -f 1)" = "6f27705eca2c8666951503b082dc1d05600808d81ecab66b2ac4419ac3ea7073"

"$run/b4/compiler" check "$scale_entry"
"$run/b4/compiler" emit-qbe "$scale_entry" > "$run/scale-linux.ssa"
cmp "$run/scale-darwin.ssa" "$run/scale-linux.ssa"
"$run/b4/compiler" build "$scale_entry" --output "$run/scale-application/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
"$run/b4/compiler" build "$scale_entry" --output "$run/scale-application-repeat/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
cmp "$run/scale-application/program" "$run/scale-application-repeat/program"
"$run/scale-application/program" > "$run/scale-application.stdout"
test "$(cat "$run/scale-application.stdout")" = "module-scale-ok"

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
	"$run/application/program" \
	"$run/scale-darwin.ssa" \
	"$run/scale-linux.ssa" \
	"$run/scale-application/program"
sha256sum "$entry" "$repo/compiler/gate4/src/storage.trb" "$repo/compiler/gate4/src/path.trb" "$scale_manifest"
sha256sum \
	"$run/b1.ssa" \
	"$run/b1.s" \
	"$run/b1" \
	"$run/b2/compiler" \
	"$run/b3/compiler" \
	"$run/b4/compiler" \
	"$run/application/program" \
	"$run/scale-darwin.ssa" \
	"$run/scale-linux.ssa" \
	"$run/scale-application/program"
file \
	"$run/b1" \
	"$run/b2/compiler" \
	"$run/b3/compiler" \
	"$run/b4/compiler" \
	"$run/application/program" \
	"$run/scale-application/program"
readelf -l "$run/b4/compiler"
readelf -d "$run/b4/compiler"
readelf -l "$run/application/program"
readelf -d "$run/application/program"
readelf -l "$run/scale-application/program"
readelf -d "$run/scale-application/program"
cat "$run/application.stdout"
cat "$run/scale-application.stdout"
cat "$run/process-summary.txt"
