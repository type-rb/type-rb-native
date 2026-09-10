#!/bin/sh
set -eu

test "$#" -eq 4 || { test "$#" -eq 5 && test "$5" = --current-only; } || exit 64
seed=$1
qbe=$2
previous=$3
workspace=$4
root=$(pwd)
mkdir -p "$workspace"
baseline=$(python3 -c 'import json; print(json.load(open("tools/daily-performance/suite.json"))["baseline"])')
current=$(git rev-parse HEAD)
if test "${5:-}" = --current-only; then previous=$current; baseline=$current; fi

for revision in "$current" "$previous" "$baseline"; do
  # Reuse identical revisions inside this run, never a floating compiler binary.
  test ! -f "$workspace/$revision/compiler" || continue
  git merge-base --is-ancestor "$revision" HEAD
  directory="$workspace/$revision"
  mkdir -p "$directory/first" "$directory/transition"
  git worktree add --detach "$directory/source" "$revision"
  source="$directory/source/compiler/src/compiler.trb"
  for generation in first transition; do
    if test "$generation" = first; then compiler=$seed; else compiler="$directory/first/compiler"; fi
    strace -f -e trace=process -o "$directory/$generation.trace" \
      "$compiler" build "$source" --output "$directory/$generation/compiler" \
      --qbe "$qbe" --cc /usr/bin/cc --target linux-arm64-v0 \
      > "$directory/$generation.stdout" 2> "$directory/$generation.stderr"
    test ! -s "$directory/$generation.stdout"
    test ! -s "$directory/$generation.stderr"
    if grep -E 'execve\("[^"]*/(go|trb|sh|bash|zsh)"' "$directory/$generation.trace"; then exit 1; fi
  done
  /bin/sh "$root/tools/bootstrap-seed.sh" \
    --mode previous --input "$directory/transition/compiler" --input-role transition \
    --repository-root "$directory/source" --qbe "$qbe" --cc /usr/bin/cc \
    --profile linux-arm64-v0 --runner-image ubuntu-24.04-arm \
    --workspace "$directory/bootstrap" --output "$directory/compiler" \
    --evidence "$directory/evidence" --metadata "$directory/metadata.json" \
    --asset-name daily-performance-linux-arm64
done

python3 - "$workspace" "$current" "$previous" "$baseline" "$RUNNER_TEMP/trb" <<'PY'
import json, pathlib, sys
workspace, current, previous, baseline, reference = sys.argv[1:]
roles = {role: {"revision": revision, "path": f"{workspace}/{revision}/compiler"}
         for role, revision in [("native", current), ("previous", previous), ("baseline", baseline)]}
roles["typerb-go"] = {"revision": pathlib.Path("TYPE_RB_REVISION").read_text().strip(), "path": reference}
pathlib.Path(workspace, "compilers.json").write_text(json.dumps(roles, indent=2) + "\n")
PY
