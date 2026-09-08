# Experimental native CLI

`trbn` is the Native experiment's command-line executable. Its default mode is
`trb`, including a standalone file, a configuration without `mode`, and the
REPL. An explicit configuration mode is authoritative. `go`, `ruby`, and
`typescript` report an unsupported-mode error; they never silently run as
native code. The reference `trb` command and its defaults are unchanged.

## Build and run from a checkout

On Darwin arm64, install the Xcode command-line tools. On Linux arm64, install
a C toolchain, `make`, `curl`, `xz`, and `lld`. Then run:

```sh
./trbn --version
./trbn run
./trbn
```

The first invocation downloads a checksum-verified native bootstrap seed and
QBE 1.3, builds the compiler from TypeRB sources, and checks byte-identical
core and CLI rebuilds. It does not invoke Go. Subsequent invocations reuse
`bin/trbn` until the compiler sources or build inputs change. Build messages
go to stderr. Source hashes are computed in batches. Documentation-only
commits and timestamp-only changes reuse the binary. A CLI-only source change
reuses the cached, verified core and performs both CLI builds; core or toolchain
changes still perform the full four-core/two-CLI chain. Test sources are outside
this bootstrap input set. `build-info.txt` records the revision at which the
artifact was built, which can precede the current checkout revision when the
build inputs are unchanged. To build without launching a command:

```sh
tools/build-native.sh
```

The outputs are `bin/trbn`, its `bin/qbe` sidecar, and `bin/build-info.txt`.
Keep the executables together when copying them elsewhere. The system C
driver/linker and system libraries remain runtime build dependencies.
The terminal editor is implemented in TypeRB and uses POSIX terminal I/O on
both systems; it has no libedit or Wasm dependency.
Checkout bootstrap currently supports Darwin arm64 and Linux arm64, even
though the internal compiler also has a Linux amd64 target profile.

The script pins the `bootstrap-seed-2026-09-09-record-arrays` release assets and their SHA-256
digests, and the QBE 1.3 archive digest. Cache files live in `.trb/bootstrap`;
downloaded seeds live under their release tag there. Updating the pin selects
a new cache entry without overwriting an older seed. The changed build script
also invalidates the verified core/CLI cache by content.
See [seed update policy](bootstrap-seed-updates.md) for compatibility-driven
refreshes and the separate pre-/post-publication verification boundary.
`TRBN_BOOTSTRAP_SEED` can select a local copy of that exact pinned seed.
`TRBN_QBE` and `TRBN_CC` select explicit executable paths. Overrides participate
in build invalidation. A lock serializes concurrent checkout builds; a killed
build may leave a lock that must be inspected before removing it.

## Commands and project configuration

```sh
./trbn check examples/main.trb
./trbn build
./trbn build --stdout
./trbn build --compile
./trbn build --compile --outfile bin/example
./trbn run
./trbn /path/to/standalone.trb -- "program argument"
./trbn repl
```

`build` writes QBE source to the configured `outDir` (default `build`), named
`<project-name>.ssa`. `build --compile` writes `bin/<project-name>` by default.
For standalone files, paths are relative to the entry file's directory and
its basename supplies the project name. `--outfile` is for executable builds.
`run` builds in a temporary directory, forwards arguments after `--`, and
returns the program's exit status. Failed builds preserve an existing output.

Configuration discovery searches from the source file/directory, or the
current directory when no source is given, upwards for `trbconfig.jsonc`.
A discovered configuration selects the project. `--config PATH` explicitly
selects one. `--mode` may select a standalone mode; it cannot override a
configured build. `repl --mode trb` can explicitly select a REPL mode.

The checkout root contains a small `mode: trb` example project in `examples/`.
Reference-compiler development checks use the separate
`trbconfig.reference.jsonc` explicitly:

```sh
trb check --config trbconfig.reference.jsonc
trb test --config trbconfig.reference.jsonc
tools/check-native-cli.sh /path/to/trb
```

There is no special directory exemption in Native configuration discovery.
The core and benchmark subprojects retain their explicit reference-validation
configurations; opening one with `trbn` honors its configured mode too.

## REPL

No arguments start a REPL when stdin and stdout are terminals. Noninteractive
no-argument invocations print usage; use `trbn repl` to read a piped session.

The REPL uses the ordinary compiler's parser, name resolution and type checker.
A TypeRB-authored evaluator retains bindings and aggregate identities between
submissions. It executes only the new input, so earlier I/O is not replayed.
Functions, records, imports, multiline control flow, scalar values and the
ordinary compiler's supported arrays can be explored interactively.

```text
mut values := [1, 2]
values.push(3)
values
:type values
```

`:type EXPRESSION` checks without evaluating. `:load FILE` adds declarations or
statements and replays the session,
`:reload` reloads the project and replays the session, `:help` shows help, and
`:quit` (`:q` / `:exit`) or Ctrl-D exits. Explicit `:load` and `:reload`
replay earlier side effects; ordinary submissions do not. Ctrl-C cancels input or evaluation.
An interactive terminal provides:

- Live syntax colors for keywords, strings, numbers, comments, types and calls,
  with unfinished strings marked separately. `NO_COLOR=1` disables colors.
- A single editable multiline buffer, two-space indentation on Enter, and
  dedenting when the complete submission is accepted. Up/Down move between
  buffer lines and then through history at the first/last line.
- Bracketed paste, retained as one submission until Enter. Pasted control
  sequences are not interpreted as editing commands.
- Tab completion of session/project names, record fields and supported methods,
  filtered at type positions. Tab/Shift-Tab cycle ambiguous candidates with a
  type/signature description; Enter accepts a selected candidate before a
  subsequent Enter submits the buffer.
- Ctrl-R reverse history search; another Ctrl-R finds an older match. Enter
  accepts the match for editing, and Ctrl-G restores the draft.
- Left/Right, Home/End, Delete/Backspace, Ctrl-A/E/B/F/P/N, Ctrl-K/U/W to kill
  text, Ctrl-L to clear the screen, Ctrl-Y to yank it, and Ctrl-_ to undo up to 64 edits.
- UTF-8 codepoint movement and deletion, combining-mark attachment, wide
  character cell widths, and a cursor-following viewport for long input.
  Resize starts a fresh display region so old terminal reflow cannot corrupt
  cursor placement. Terminal settings are restored before evaluation and exit.

Project history is `.trb/repl_history`; standalone
history is `~/.cache/trbn/repl_history_trb`. `TRBN_HISTORY` overrides that file.
History uses the reference REPL's JSON string-array format.

This is a bounded experimental implementation, not complete `trb` parity.
See the [ordinary coverage plan](native-language-coverage.md) for path-specific
tracking; snapshot/recovery capabilities do not establish ordinary CLI support.
The ordinary compiler's language and package restrictions still apply,
including its current ASCII String-literal boundary.
Formatting, tests, language-server and package-management commands are not
implemented by `trbn`.
The editor does not yet provide the reference formatter's full canonical
spacing, every readline/vi binding, import-repair and argument-aware completion,
or full Unicode grapheme-cluster segmentation (for example joined emoji).
Completion follows the executable Native subset; editing Unicode does not lift
the compiler's ASCII String-literal restriction. Submissions are bounded to
64 KiB, including paste; overflow is rejected without evaluating a prefix.
The evaluator has a 256-call depth bound and
retains reachable session values; it is not a sandbox or a production runtime.

## CI artifacts and validation

Run the **Experimental native CLI** workflow with `workflow_dispatch`, selecting
the desired revision. The same checkout launcher builds Darwin arm64 and
Linux arm64, verifies fixed points, runs CLI and real-terminal tests, and
uploads `trbn-<platform>` artifacts containing a tarball and checksum. Each
archive includes `trbn`, QBE, build metadata, this guide, and the project
license. Artifacts are experimental CI outputs, not supported releases.

Run the same integration tests locally after building:

```sh
python3 tools/native-cli-test.py bin/trbn
python3 -m venv .trb/repl-tests
.trb/repl-tests/bin/pip install -r tools/repl-test-requirements.txt
.trb/repl-tests/bin/python tools/native-repl-editor-test.py bin/trbn
# Optional: run the shared screen scenarios against the reference REPL too.
.trb/repl-tests/bin/python tools/native-repl-editor-test.py bin/trbn --reference /path/to/trb
```

Compiler implementation stays in `compiler/src`; CLI, terminal integration
and evaluation live in `compiler/cli`. The bootstrap stages a shared import
root without changing those canonical source trees. Typed host declarations
are backed by a compiler-owned POSIX QBE template only at the CLI compiler
entry. This is internal bootstrap machinery, not a public FFI facility.

## Builtin output

Like the reference prelude, `puts` takes one value and writes its text followed
by a newline. The Native subset accepts String, Integer and Boolean in both
compiled programs and the REPL. Integer uses decimal digits; Boolean uses
`true` or `false`. Arguments are evaluated once. This builtin output conversion
does not invoke user-defined `to_s` methods or make ordinary String parameters
accept other types. Float, collection and record output remain explicitly
unsupported; their portable formatting requires separate coverage.

`python3 tools/native-puts-test.py bin/trbn --reference /path/to/trb` compares
compiled and REPL output with the reference compiler. After a normal checkout
build, `python3 tools/native-bootstrap-test.py` checks cache invalidation, core
reuse, failed-build preservation and concurrent callers in an isolated copy.

## Diagnostics

File checking, QBE emission, executable builds and execution report frontend
errors on stderr as `path:line: error[CODE]: message`, using the actual entry or
imported file. REPL diagnostics use `(trb)` and the cumulative authored line
number of accepted submissions; generated imports, the entry function and
stored bindings do not add visible lines. Failed submissions do not advance
that line count. REPL runtime failures use `error: message` at the invoking
statement, including division by zero.

This follows the pinned reference CLI's location/severity/code presentation.
The experimental frontend currently retains line origins, so it omits columns
instead of estimating them. Its `TRBN` diagnostic codes and detailed messages
remain distinct where its supported subset and diagnosis differ from the
reference frontend. It reports the first error rather than accumulating the
reference compiler's complete diagnostic set. Compiled-program runtime
failures and external tool diagnostics retain their existing runtime/tool
contracts. The internal core compiler protocol remains unchanged.

Run `python3 tools/native-diagnostics-test.py bin/trbn --reference /path/to/trb`
to compare file, imported-module and cumulative REPL origins against the pinned
reference executable. The artifact workflow runs the same Native assertions
on both supported checkout platforms.

## String interpolation

Double-quoted Strings evaluate `#{expression}` through the shared Native
frontend in both compiled programs and the REPL. Expressions must return
String; use an explicit supported conversion such as `value.to_s()` for an
Integer. Multiple expressions run once each, from left to right. Grouping
preserves expression precedence and postfix operations on the resulting String.
Nested quoted Strings and nested interpolation are supported within the
existing expression and ASCII String subset.

Use `\#` to suppress interpolation: `"\#{name}"` produces the literal text
`#{name}`. With two backslashes, `"\\#{name}"` produces one backslash followed
by the value of `name`. Undefined escapes such as `\{` and `\q` are errors,
including in literal segments next to interpolation. Escaped markers retain
literal coloring in the REPL and round-trip unchanged through its history.

The REPL colors interpolation delimiters and embedded expressions separately
from literal text, including while input is incomplete. JSON history retains
interpolation as source text and never interprets it while loading.

`python3 tools/native-interpolation-test.py bin/trbn --reference /path/to/trb`
compares evaluation, side effects and type rejection with the pinned reference.
Empty interpolation markers remain literal as in that reference. Malformed
nonempty expressions and unterminated interpolation receive diagnostics; no
implicit conversion or unchecked evaluation is introduced.
