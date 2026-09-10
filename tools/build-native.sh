#!/bin/sh
set -eu

repository_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cache="$repository_root/.trb/bootstrap"
seed_release=bootstrap-seed-2026-09-10-hash
output="$repository_root/bin"
fail() { printf 'trbn: %s\n' "$1" >&2; exit 1; }
sha256_files() {
	if command -v sha256sum >/dev/null 2>&1; then
		sha256sum "$@"
	else
		shasum -a 256 "$@"
	fi
}
source_hashes() {
	if command -v sha256sum >/dev/null 2>&1; then
		find "$1" -type f -name '*.trb' ! -name '*_test.trb' -exec sha256sum {} + > "$stage/source-hashes"
	else
		find "$1" -type f -name '*.trb' ! -name '*_test.trb' -exec shasum -a 256 {} + > "$stage/source-hashes"
	fi
	LC_ALL=C sort "$stage/source-hashes"
}
sha256() { sha256_files "$1" | cut -d ' ' -f 1; }
verify() { test "$(sha256 "$1")" = "$2" || fail "checksum mismatch: $1"; }
case "$(uname -s)/$(uname -m)" in
	Darwin/arm64)
		profile=darwin-arm64-v0
		asset=type-rb-native-bootstrap-darwin-arm64
		seed_digest=13d2b494b5b4864f0f7c823a5c9e2c38850e865725ed8cef87fd487d1358185d
		;;
	Linux/aarch64)
		profile=linux-arm64-v0
		asset=type-rb-native-bootstrap-linux-arm64
		seed_digest=6bae5730fc543c9dc8609a19d4884064b8d363ca038fe75a5b74465eb8b3c7a5
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
# Hash each source set in one process. Paths, additions and deletions remain
# part of the manifest; timestamps and Git revision do not determine freshness.
(
	cd "$repository_root"
	set -- tools/build-native.sh "$cc"
	if test -n "${TRBN_QBE:-}"; then set -- "$@" "$TRBN_QBE"; fi
	if test -n "${TRBN_BOOTSTRAP_SEED:-}"; then set -- "$@" "$TRBN_BOOTSTRAP_SEED"; fi
	sha256_files "$@"
	source_hashes compiler/src
	printf '%s\n' "$profile" "$cc" "${TRBN_QBE:-bundled}" "${TRBN_BOOTSTRAP_SEED:-published}"
	"$cc" --version
) > "$stage/core-inputs"
(
	cat "$stage/core-inputs"
	cd "$repository_root"
	source_hashes compiler/cli
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
seed=${TRBN_BOOTSTRAP_SEED:-$cache/$seed_release/$asset}
if test ! -f "$seed"; then
	test -z "${TRBN_BOOTSTRAP_SEED:-}" || fail "bootstrap seed is missing: $seed"
	curl --fail --location --retry 3 "https://github.com/type-rb/type-rb-native/releases/download/$seed_release/$asset" -o "$stage/seed"
	verify "$stage/seed" "$seed_digest"
	mkdir -p "$cache/$seed_release"
	mv "$stage/seed" "$seed"
fi
verify "$seed" "$seed_digest"
chmod 0755 "$seed"
mkdir -p "$stage/first" "$stage/runtime" "$stage/core" "$stage/verify" "$stage/source"
core="$cache/core/compiler"
if test -x "$core" && test -f "$cache/core/inputs" && cmp -s "$stage/core-inputs" "$cache/core/inputs"; then
	printf '%s\n' 'trbn: reusing the verified core compiler' >&2
else
	source="$repository_root/compiler/src/compiler.trb"
	"$seed" build "$source" --output "$stage/first/compiler" --qbe "$qbe" --cc "$cc" --target "$profile"
	"$stage/first/compiler" build "$source" --output "$stage/runtime/compiler" --qbe "$qbe" --cc "$cc" --target "$profile"
	"$stage/runtime/compiler" build "$source" --output "$stage/core/compiler" --qbe "$qbe" --cc "$cc" --target "$profile"
	"$stage/core/compiler" build "$source" --output "$stage/verify/compiler" --qbe "$qbe" --cc "$cc" --target "$profile"
	cmp "$stage/core/compiler" "$stage/verify/compiler" || fail 'compiler fixed point differs'
	core="$stage/core/compiler"
fi
# The core and CLI share one import root in this derived source tree. The
# canonical core project remains independently checkable by the reference tool.
for source in "$repository_root"/compiler/src/*.trb "$repository_root"/compiler/cli/*.trb; do
	case "$source" in *_test.trb) continue ;; esac
	cp "$source" "$stage/source/$(basename -- "$source")"
done
"$core" build "$stage/source/main.trb" --output "$stage/trbn" --qbe "$qbe" --cc "$cc" --target "$profile"
"$stage/trbn" --version >&2
"$stage/trbn" --internal-driver build "$stage/source/main.trb" --output "$stage/verify/trbn" --qbe "$qbe" --cc "$cc"
cmp "$stage/trbn" "$stage/verify/trbn" || fail 'CLI fixed point differs'
cp "$qbe" "$stage/qbe"
# Publish the verified core only after the CLI fixed point also succeeds.
if test "$core" = "$stage/core/compiler"; then
	mkdir -p "$cache/core"
	rm -f "$cache/core/inputs"
	mv "$stage/core/compiler" "$cache/core/compiler"
	mv "$stage/core-inputs" "$cache/core/inputs"
fi
revision=$(git -C "$repository_root" rev-parse HEAD 2>/dev/null || printf 'source-archive')
printf '%s\n' "profile=$profile" "revision=$revision" "inputs_sha256=$(sha256 "$stage/inputs")" "compiler_sha256=$(sha256 "$stage/trbn")" "qbe_sha256=$(sha256 "$stage/qbe")" > "$stage/build-info.txt"
rm -f "$cache/inputs"
mv "$stage/trbn" "$output/trbn"
mv "$stage/qbe" "$output/qbe"
mv "$stage/build-info.txt" "$output/build-info.txt"
mv "$stage/inputs" "$cache/inputs"
printf '%s\n' "$output/trbn"
