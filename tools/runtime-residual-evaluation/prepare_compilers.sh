#!/bin/sh
# Same ordinary preparation chain with an explicit backend for prior sources.
set -eu
test "$#" -eq 6 || exit 64
seed=$1
qbe=$2
previous=$3
previous_qbe=$4
workspace=$5
baseline_seed=$6
for executable in "$seed" "$qbe" "$previous_qbe" "$baseline_seed"; do test -x "$executable"; done
root=$(pwd)
mkdir -p "$workspace"
baseline=$(python3 -c 'import json; print(json.load(open("tools/daily-performance/suite.json"))["baseline"])')
current=$(git rev-parse HEAD)

for revision in "$current" "$previous" "$baseline"; do
  # Reuse identical revisions inside this run, never a floating compiler binary.
  test ! -f "$workspace/$revision/compiler" || continue
  git merge-base --is-ancestor "$revision" HEAD
  role_qbe=$qbe
  if test "$revision" != "$current"; then role_qbe=$previous_qbe; fi
  preparation_started=$(date +%s)
  printf 'Preparing compiler %s\n' "$revision"
  directory="$workspace/$revision"
  mkdir -p "$directory/first" "$directory/transition"
  git worktree add --detach "$directory/source" "$revision"
  source="$directory/source/compiler/src/compiler.trb"
  input_seed=$seed
  # The frozen source uses historical compiler intrinsic names. A newer seed
  # can compile it without preserving its compiler runtime entry adapters.
  if test "$revision" = "$baseline"; then
    input_seed=$baseline_seed
  fi
  python3 - "$input_seed" "$directory/seed-input.json" <<'PY'
import hashlib, json, pathlib, sys
seed, output = map(pathlib.Path, sys.argv[1:])
output.write_text(json.dumps({"sha256": hashlib.sha256(seed.read_bytes()).hexdigest()}) + "\n")
PY
  for generation in first transition; do
    if test "$generation" = first; then compiler=$input_seed; else compiler="$directory/first/compiler"; fi
    status=0
    strace -f -e trace=process -o "$directory/$generation.trace" \
      "$compiler" build "$source" --output "$directory/$generation/compiler" \
      --qbe "$role_qbe" --cc /usr/bin/cc --target linux-arm64-v0 \
      > "$directory/$generation.stdout" 2> "$directory/$generation.stderr" || status=$?
    if test "$status" -ne 0; then
      printf 'Compiler preparation failed: revision=%s generation=%s status=%s\n' "$revision" "$generation" "$status" >&2
      cat "$directory/$generation.stdout" "$directory/$generation.stderr" >&2
      exit "$status"
    fi
    test ! -s "$directory/$generation.stdout"
    test ! -s "$directory/$generation.stderr"
    if grep -E 'execve\("[^"]*/(go|trb|sh|bash|zsh)"' "$directory/$generation.trace"; then exit 1; fi
  done
  /bin/sh "$root/tools/bootstrap-seed.sh" \
    --mode previous --input "$directory/transition/compiler" --input-role transition \
    --measurement-policy diagnostic \
    --repository-root "$directory/source" --qbe "$role_qbe" --cc /usr/bin/cc \
    --profile linux-arm64-v0 --runner-image ubuntu-24.04-arm \
    --workspace "$directory/bootstrap" --output "$directory/compiler" \
    --evidence "$directory/evidence" --metadata "$directory/metadata.json" \
    --asset-name daily-performance-linux-arm64
  preparation_elapsed=$(($(date +%s) - preparation_started))
  printf 'revision=%s\nelapsed_seconds=%s\nscope=transition-and-correctness-preparation\n' \
    "$revision" "$preparation_elapsed" > "$directory/evidence/preparation.txt"
  printf 'Prepared compiler %s in %s seconds\n' "$revision" "$preparation_elapsed"
done

python3 - "$workspace" "$current" "$previous" "$baseline" "$RUNNER_TEMP/trb" <<'PY'
import json, pathlib, sys
workspace, current, previous, baseline, reference = sys.argv[1:]
roles = {role: {"revision": revision, "path": f"{workspace}/{revision}/compiler"}
         for role, revision in [("native", current), ("previous", previous), ("baseline", baseline)]}
roles["typerb-go"] = {"revision": pathlib.Path("TYPE_RB_REVISION").read_text().strip(), "path": reference}
pathlib.Path(workspace, "compilers.json").write_text(json.dumps(roles, indent=2) + "\n")
PY
