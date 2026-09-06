# Experimental native CLI

`trbn` is the Native experiment's command-line executable. Its default mode is
`trb`, including a standalone file, a configuration without `mode`, and the
REPL. An explicit configuration mode is authoritative. `go`, `ruby`, and
`typescript` report an unsupported-mode error; they never silently run as
native code. The reference `trb` command and its defaults are unchanged.

## Build and run from a checkout

On Darwin arm64, install the Xcode command-line tools. On Linux arm64, install
a C toolchain, `make`, `curl`, `xz`, `lld`, and `libedit2`. Then run:

```sh
./trbn --version
./trbn run
./trbn
```

The first invocation downloads a checksum-verified native bootstrap seed and
QBE 1.3, builds the compiler from TypeRB sources, and checks byte-identical
core and CLI rebuilds. It does not invoke Go. Subsequent invocations reuse
`bin/trbn` until the compiler sources or build inputs change. Build messages
go to stderr. To build without launching a command:

```sh
tools/build-native.sh
```

The outputs are `bin/trbn`, its `bin/qbe` sidecar, and `bin/build-info.txt`.
Keep the executables together when copying them elsewhere. The system C
driver/linker and system libraries remain runtime build dependencies. Darwin
ships the terminal editor; interactive Linux sessions require `libedit2`.
Checkout bootstrap currently supports Darwin arm64 and Linux arm64, even
though the internal compiler also has a Linux amd64 target profile.

The script pins the `bootstrap-seed-2026-08-30` release assets and their SHA-256
digests, and the QBE 1.3 archive digest. Cache files live in `.trb/bootstrap`.
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

`:type EXPRESSION` checks without evaluating. `:load FILE` adds declarations,
`:reload` reloads the project and clears session state, `:help` shows help, and
`:quit` or Ctrl-D exits. Ctrl-C cancels input or evaluation. An interactive
terminal supports cursor editing, Up/Down history, and Tab completion of
session/project names. Project history is `.trb/repl_history`; standalone
history is `~/.cache/trbn/repl_history_trb`. `TRBN_HISTORY` overrides that file.
History uses the reference REPL's JSON string-array format.

This is a bounded experimental implementation, not complete `trb` parity.
The ordinary compiler's language and package restrictions still apply,
including its current ASCII String-literal boundary.
Formatting, tests, language-server and package-management commands are not
implemented by `trbn`. REPL completion and diagnostics do not yet reproduce
all reference editor behavior. The evaluator has a 256-call depth bound and
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
```

Compiler implementation stays in `compiler/src`; CLI, terminal integration
and evaluation live in `compiler/cli`. The bootstrap stages a shared import
root without changing those canonical source trees. Typed host declarations
are backed by a compiler-owned POSIX QBE template only at the CLI compiler
entry. This is internal bootstrap machinery, not a public FFI facility.
