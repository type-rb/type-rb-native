#!/bin/sh
set -eu

repository_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cache="$repository_root/.trb/bootstrap"
output="$repository_root/bin"
fail() { printf 'trbn: %s\n' "$1" >&2; exit 1; }
sha256() {
	if command -v sha256sum >/dev/null 2>&1; then
		sha256sum "$1" | cut -d ' ' -f 1
	else
		shasum -a 256 "$1" | cut -d ' ' -f 1
	fi
}
verify() { test "$(sha256 "$1")" = "$2" || fail "checksum mismatch: $1"; }
case "$(uname -s)/$(uname -m)" in
	Darwin/arm64)
		profile=darwin-arm64-v0
		asset=type-rb-native-bootstrap-darwin-arm64
		seed_digest=ef438d13598c534766334b408a39715c56ff1b69db528910ebf7d90ec7720b65
		;;
	Linux/aarch64)
		profile=linux-arm64-v0
		asset=type-rb-native-bootstrap-linux-arm64
		seed_digest=b4307c244edc9e4da620f2a7c1b03a733e575da032efefae615f9edf75048a37
		command -v ld.lld >/dev/null 2>&1 || fail 'Linux builds require lld'
		;;
	*) fail 'checkout bootstrap currently supports Darwin arm64 and Linux arm64' ;;
esac
cc=${TRBN_CC:-/usr/bin/cc}
test -x "$cc" || fail "C toolchain is missing: $cc"
mkdir -p "$cache" "$output"
lock="$cache/build.lock"
lock_wait=0
while ! mkdir "$lock" 2>/dev/null; do
	lock_wait=$((lock_wait + 1))
	test "$lock_wait" -le 120 || fail "another build holds $lock; inspect its owner before removing a stale lock"
	sleep 1
done
printf '%s\n' "$$" > "$lock/pid"
stage=
cleanup() {
	if test -n "$stage"; then rm -rf "$stage"; fi
	rm -f "$lock/pid"
	rmdir "$lock"
}
trap cleanup 0
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
stage=$(mktemp -d "$cache/build.XXXXXX")
revision=$(git -C "$repository_root" rev-parse HEAD 2>/dev/null || printf 'source-archive')
(
	cd "$repository_root"
	find compiler/src compiler/cli -type f -name '*.trb' ! -name '*_test.trb' | LC_ALL=C sort | while IFS= read -r source; do
		printf '%s %s\n' "$(sha256 "$source")" "$source"
	done
	sha256 tools/build-native.sh
	sha256 "$cc"
	if test -n "${TRBN_QBE:-}"; then sha256 "$TRBN_QBE"; fi
	if test -n "${TRBN_BOOTSTRAP_SEED:-}"; then sha256 "$TRBN_BOOTSTRAP_SEED"; fi
	printf '%s\n' "$profile" "$revision" "$cc" "${TRBN_QBE:-bundled}" "${TRBN_BOOTSTRAP_SEED:-published}"
	"$cc" --version
) > "$stage/inputs"
if test -x "$output/trbn" && test -x "$output/qbe" && test -f "$cache/inputs"; then
	if cmp -s "$stage/inputs" "$cache/inputs"; then
		printf '%s\n' "$output/trbn"
		exit 0
	fi
fi
printf '%s\n' 'trbn: bootstrapping the native compiler' >&2
qbe=${TRBN_QBE:-$cache/qbe-1.3/qbe}
if test ! -x "$qbe"; then
	test -z "${TRBN_QBE:-}" || fail "QBE is not executable: $qbe"
	archive="$cache/qbe-1.3.tar.xz"
	if test ! -f "$archive"; then
		curl --fail --location --retry 3 https://c9x.me/compile/release/qbe-1.3.tar.xz -o "$stage/qbe.tar.xz"
		verify "$stage/qbe.tar.xz" d587905d620dc5e1d2bfa7c2cc642b9b837aa89a3188c6e37b53d756cf66e320
		mv "$stage/qbe.tar.xz" "$archive"
	fi
	verify "$archive" d587905d620dc5e1d2bfa7c2cc642b9b837aa89a3188c6e37b53d756cf66e320
	tar -xf "$archive" -C "$stage"
	make -C "$stage/qbe-1.3" >&2
	mkdir -p "$cache/qbe-1.3"
	cp "$stage/qbe-1.3/qbe" "$qbe"
fi
seed=${TRBN_BOOTSTRAP_SEED:-$cache/$asset}
if test ! -f "$seed"; then
	test -z "${TRBN_BOOTSTRAP_SEED:-}" || fail "bootstrap seed is missing: $seed"
	curl --fail --location --retry 3 "https://github.com/type-rb/type-rb-native/releases/download/bootstrap-seed-2026-08-30/$asset" -o "$stage/seed"
	verify "$stage/seed" "$seed_digest"
	mv "$stage/seed" "$seed"
fi
verify "$seed" "$seed_digest"
chmod 0755 "$seed"
mkdir -p "$stage/first" "$stage/runtime" "$stage/core" "$stage/verify" "$stage/source"
source="$repository_root/compiler/src/compiler.trb"
"$seed" build "$source" --output "$stage/first/compiler" --qbe "$qbe" --cc "$cc" --target "$profile"
"$stage/first/compiler" build "$source" --output "$stage/runtime/compiler" --qbe "$qbe" --cc "$cc" --target "$profile"
"$stage/runtime/compiler" build "$source" --output "$stage/core/compiler" --qbe "$qbe" --cc "$cc" --target "$profile"
"$stage/core/compiler" build "$source" --output "$stage/verify/compiler" --qbe "$qbe" --cc "$cc" --target "$profile"
cmp "$stage/core/compiler" "$stage/verify/compiler" || fail 'compiler fixed point differs'
# The core and CLI share one import root in this derived source tree. The
# canonical core project remains independently checkable by the reference tool.
for source in "$repository_root"/compiler/src/*.trb "$repository_root"/compiler/cli/*.trb; do
	case "$source" in *_test.trb) continue ;; esac
	cp "$source" "$stage/source/$(basename -- "$source")"
done
"$stage/core/compiler" build "$stage/source/main.trb" --output "$stage/trbn" --qbe "$qbe" --cc "$cc" --target "$profile"
"$stage/trbn" --version >&2
"$stage/trbn" --internal-driver build "$stage/source/main.trb" --output "$stage/verify/trbn" --qbe "$qbe" --cc "$cc"
cmp "$stage/trbn" "$stage/verify/trbn" || fail 'CLI fixed point differs'
cp "$qbe" "$stage/qbe"
printf '%s\n' "profile=$profile" "revision=$revision" "inputs_sha256=$(sha256 "$stage/inputs")" "compiler_sha256=$(sha256 "$stage/trbn")" "qbe_sha256=$(sha256 "$stage/qbe")" > "$stage/build-info.txt"
mv "$stage/trbn" "$output/trbn"
mv "$stage/qbe" "$output/qbe"
mv "$stage/build-info.txt" "$output/build-info.txt"
mv "$stage/inputs" "$cache/inputs"
printf '%s\n' "$output/trbn"
