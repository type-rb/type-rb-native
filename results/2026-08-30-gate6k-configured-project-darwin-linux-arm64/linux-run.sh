#!/bin/sh

set -eux

repo=/repo
run=/run
entry="$repo/compiler/gate4/src/compiler.trb"
small_config="$repo/corpus/gate6k/configured-project/trbconfig.jsonc"
scale_project="$run/scale-project"
scale_config="$scale_project/trbconfig.jsonc"
scale_entry="$scale_project/src/main.trb"
qbe=/usr/local/bin/qbe
cc=/usr/bin/cc

expect_failure() {
	label=$1
	needle=$2
	shift 2
	first_stdout="$run/probes/$label.first.stdout"
	first_stderr="$run/probes/$label.first.stderr"
	second_stdout="$run/probes/$label.second.stdout"
	second_stderr="$run/probes/$label.second.stderr"
	set +e
	"$@" > "$first_stdout" 2> "$first_stderr"
	first_status=$?
	"$@" > "$second_stdout" 2> "$second_stderr"
	second_status=$?
	set -e
	test "$first_status" -ne 0
	test "$first_status" = "$second_status"
	cmp "$first_stdout" "$second_stdout"
	cmp "$first_stderr" "$second_stderr"
	if test -n "$needle"; then
		grep -F "$needle" "$first_stdout" "$first_stderr" > /dev/null
	fi
	printf '%s status=%s\n' "$label" "$first_status" >> "$run/negative-statuses.txt"
}

write_valid_project() {
	project=$1
	mkdir -p "$project/src"
	cat > "$project/trbconfig.jsonc" <<'EOF'
{"name":"probe","mode":"go","sourceDir":"src","go":{"module":"example.com/probe"}}
EOF
	cat > "$project/src/main.trb" <<'EOF'
def main()
	return
end
EOF
}

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

test "$(sha256sum "$run/b1.ssa" | cut -d ' ' -f 1)" = "62db3c31527a670c3050051a9fa27bf142b6c5deaab81ef8234104bd467aa95a"
test "$(sha256sum "$run/configured-small-darwin.ssa" | cut -d ' ' -f 1)" = "ccae60d4c24176880935c8f3d9afb96f7d4e4787aa0033c25a080c54ebf5f774"
test "$(sha256sum "$run/scale-darwin.ssa" | cut -d ' ' -f 1)" = "39f61f19bcd404732848604b568f4a5db3d70990ea233aaf8e337296d5d88874"

"$qbe" -t arm64 -o "$run/b1.s" "$run/b1.ssa"
"$cc" "$run/b1.s" -xassembler -Wl,--gc-sections,--strip-all -o "$run/b1"

mkdir -p \
	"$run/b2" \
	"$run/b3" \
	"$run/b4" \
	"$run/configured-small" \
	"$run/configured-small-repeat" \
	"$run/scale-file-root" \
	"$run/scale-configured" \
	"$run/scale-configured-repeat" \
	"$run/probes" \
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
test "$(sha256sum "$run/b4/compiler" | cut -d ' ' -f 1)" = "955b275e1906f498418b47eedbc8183c565283d9b58754008d8df425dc78399a"
"$run/b4/compiler" emit-qbe "$entry" > "$run/b4.ssa"
cmp "$run/b1.ssa" "$run/b4.ssa"

"$run/b4/compiler" check "$small_config"
"$run/b4/compiler" emit-qbe "$small_config" > "$run/configured-small-linux.ssa"
cmp "$run/configured-small-darwin.ssa" "$run/configured-small-linux.ssa"
"$run/b4/compiler" build "$small_config" --output "$run/configured-small/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
"$run/b4/compiler" build "$small_config" --output "$run/configured-small-repeat/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
cmp "$run/configured-small/program" "$run/configured-small-repeat/program"
test "$(sha256sum "$run/configured-small/program" | cut -d ' ' -f 1)" = "24b5b7a2c532c6c17e3137dfbde232c1d5bdb0d1bb806baeeb0a819e0cae11d1"
"$run/configured-small/program" > "$run/configured-small.stdout"
test "$(cat "$run/configured-small.stdout")" = "configured-project-ok"

mkdir -p "$scale_project/src"
cp "$repo/corpus/gate6k/configured-project/trbconfig.jsonc" "$scale_config"
cp "$repo/corpus/gate6k/configured-project/go.mod" "$scale_project/go.mod"
: > "$run/scale-project.manifest"
set +x
index=0
while test "$index" -lt 1024; do
	name=$(printf '%04d' "$index")
	module="$scale_project/src/m$name.trb"
	if test "$index" -eq 0; then
		printf 'def f%s(): Integer\n\treturn 1\nend\n' "$name" > "$module"
	else
		previous=$(printf '%04d' "$((index - 1))")
		printf 'import { f%s } from m%s\n\ndef f%s(): Integer\n\treturn f%s() + 1\nend\n' "$previous" "$previous" "$name" "$previous" > "$module"
	fi
	printf '=== m%s.trb ===\n' "$name" >> "$run/scale-project.manifest"
	cat "$module" >> "$run/scale-project.manifest"
	index=$((index + 1))
done
cat > "$scale_entry" <<'EOF'
import { f1023 } from m1023

def main()
	if f1023() == 1024
		puts("module-scale-ok")
	else
		puts("module-scale-bad")
	end
	return
end
EOF
printf '=== main.trb ===\n' >> "$run/scale-project.manifest"
cat "$scale_entry" >> "$run/scale-project.manifest"
set -x
test "$(find "$scale_project/src" -type f -name '*.trb' | wc -l | tr -d ' ')" = "1025"
test "$(sha256sum "$run/scale-project.manifest" | cut -d ' ' -f 1)" = "db438159189ba944283d8a92a09a1176020522c67d2551065c4010c50858f16b"

"$run/b4/compiler" check "$scale_entry"
"$run/b4/compiler" check "$scale_config"
"$run/b4/compiler" emit-qbe "$scale_entry" > "$run/scale-file-root-linux.ssa"
"$run/b4/compiler" emit-qbe "$scale_config" > "$run/scale-configured-linux.ssa"
cmp "$run/scale-file-root-linux.ssa" "$run/scale-configured-linux.ssa"
cmp "$run/scale-darwin.ssa" "$run/scale-configured-linux.ssa"
"$run/b4/compiler" build "$scale_entry" --output "$run/scale-file-root/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
"$run/b4/compiler" build "$scale_config" --output "$run/scale-configured/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
"$run/b4/compiler" build "$scale_config" --output "$run/scale-configured-repeat/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
cmp "$run/scale-file-root/program" "$run/scale-configured/program"
cmp "$run/scale-configured/program" "$run/scale-configured-repeat/program"
test "$(sha256sum "$run/scale-configured/program" | cut -d ' ' -f 1)" = "79c27953c1bce1c9523cf491003ca39536559c5ec81fca186943c10ccfd9e9ce"
"$run/scale-configured/program" > "$run/scale-configured.stdout"
test "$(cat "$run/scale-configured.stdout")" = "module-scale-ok"

config_probe="$run/probes/configuration"
write_valid_project "$config_probe"
cat > "$config_probe/trbconfig.jsonc" <<'EOF'
{"name":"probe","mode":"go","sourceDir":"src","packages":[],"go":{"module":"example.com/probe"}}
EOF
expect_failure configuration "unsupported project configuration field packages" "$run/b4/compiler" check "$config_probe/trbconfig.jsonc"

collection_probe="$run/probes/collection"
write_valid_project "$collection_probe"
ln -s "$collection_probe/src/main.trb" "$collection_probe/src/linked.trb"
expect_failure collection "cannot collect project source" "$run/b4/compiler" check "$collection_probe/trbconfig.jsonc"

entrypoint_probe="$run/probes/entrypoint"
write_valid_project "$entrypoint_probe"
cat > "$entrypoint_probe/src/main.trb" <<'EOF'
def helper(): Integer
	return 1
end
EOF
expect_failure entrypoint "project must declare exactly one top-level main function" "$run/b4/compiler" check "$entrypoint_probe/trbconfig.jsonc"

cycle_probe="$run/probes/cycle"
write_valid_project "$cycle_probe"
cat > "$cycle_probe/src/main.trb" <<'EOF'
import { a } from a

def main()
	a()
	return
end
EOF
cat > "$cycle_probe/src/a.trb" <<'EOF'
import { b } from b

def a()
	b()
	return
end
EOF
cat > "$cycle_probe/src/b.trb" <<'EOF'
import { a } from a

def b()
	a()
	return
end
EOF
expect_failure cycle "import cycle through" "$run/b4/compiler" check "$cycle_probe/trbconfig.jsonc"

tool_marker="$run/probes/tool-launched"
probe_tool="$run/probes/probe-tool"
cat > "$probe_tool" <<EOF
#!/bin/sh
/usr/bin/touch "$tool_marker"
exit 91
EOF
chmod 755 "$probe_tool"
printf 'preserve-compiler\n' > "$run/probes/compiler-output"
expect_failure tool-suppression "project must declare exactly one top-level main function" "$run/b4/compiler" build "$entrypoint_probe/trbconfig.jsonc" --output "$run/probes/compiler-output" --qbe "$probe_tool" --cc "$probe_tool" --target linux-arm64-v0
test ! -e "$tool_marker"
test "$(cat "$run/probes/compiler-output")" = "preserve-compiler"

printf 'preserve-qbe\n' > "$run/probes/qbe-output"
expect_failure qbe-cleanup "" "$run/b4/compiler" build "$small_config" --output "$run/probes/qbe-output" --qbe /usr/bin/false --cc "$cc" --target linux-arm64-v0
test "$(cat "$run/probes/qbe-output")" = "preserve-qbe"

printf 'preserve-cc\n' > "$run/probes/cc-output"
expect_failure cc-cleanup "" "$run/b4/compiler" build "$small_config" --output "$run/probes/cc-output" --qbe "$qbe" --cc /usr/bin/false --target linux-arm64-v0
test "$(cat "$run/probes/cc-output")" = "preserve-cc"

/usr/bin/strace -f -e trace=process -o "$run/process.trace" \
	"$run/b4/compiler" build "$small_config" --output "$run/trace/program" --qbe "$qbe" --cc "$cc" --target linux-arm64-v0
cmp "$run/configured-small/program" "$run/trace/program"
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
	"$run/configured-small-darwin.ssa" \
	"$run/configured-small-linux.ssa" \
	"$run/configured-small/program" \
	"$run/scale-darwin.ssa" \
	"$run/scale-file-root-linux.ssa" \
	"$run/scale-configured-linux.ssa" \
	"$run/scale-file-root/program" \
	"$run/scale-configured/program"
sha256sum \
	"$entry" \
	"$repo/compiler/gate4/src/storage.trb" \
	"$repo/compiler/gate4/src/path.trb" \
	"$small_config" \
	"$run/scale-project.manifest"
sha256sum \
	"$run/b1.ssa" \
	"$run/b1.s" \
	"$run/b1" \
	"$run/b2/compiler" \
	"$run/b3/compiler" \
	"$run/b4/compiler" \
	"$run/configured-small-darwin.ssa" \
	"$run/configured-small-linux.ssa" \
	"$run/configured-small/program" \
	"$run/scale-darwin.ssa" \
	"$run/scale-file-root-linux.ssa" \
	"$run/scale-configured-linux.ssa" \
	"$run/scale-file-root/program" \
	"$run/scale-configured/program"
file \
	"$run/b1" \
	"$run/b2/compiler" \
	"$run/b3/compiler" \
	"$run/b4/compiler" \
	"$run/configured-small/program" \
	"$run/scale-configured/program"
readelf -l "$run/b4/compiler"
readelf -d "$run/b4/compiler"
readelf -l "$run/configured-small/program"
readelf -d "$run/configured-small/program"
readelf -l "$run/scale-configured/program"
readelf -d "$run/scale-configured/program"
cat "$run/configured-small.stdout"
cat "$run/scale-configured.stdout"
cat "$run/negative-statuses.txt"
cat "$run/process-summary.txt"
