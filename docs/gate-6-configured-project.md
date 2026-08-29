# Gate 6K Explicit Configured-project Executables

Gate 6K adds the smallest explicit configured-project path to the ordinary
self-hosted compiler. Its exact correctness and measurement boundary is
pre-registered in
[issue #80](https://github.com/type-rb/type-rb-native/issues/80), and its
ownership model is defined by
[Decision 0018](decisions/0018-explicit-configured-project.md).

## Status

Gate 6K is complete. The strict configuration projection, complete-source
project loading, physical collection adapter, permanent TypeRB-authored
harness, registered Darwin measurements, exact fixed points and regressions,
and pinned Linux arm64 evidence all pass the pre-registered boundary. The
measured compiler implementation is
`84e2e4a6e2cff9d7fdab46ce4eec33b609a597c4`; the reviewed harness is
`9d11966a92ca308d4bb84dacc59f47efbb92b6cc`. See the
[recorded result](../results/2026-08-30-gate6k-configured-project-darwin-linux-arm64/README.md).

The fixed source baseline is TypeRB Native main revision
`e9b00ed946919957fad82b6d2d3ffccfe8cd48d1`. Both baseline and candidate
ordinary chains start from the retained 264,904-byte Gate 6J Darwin B4 compiler
with SHA-256
`caf3d213559382376bb87b1555e832c0efd7321c0a930ffa23e88d5bc1e55c77`.
The pinned TypeRB semantic oracle remains revision
`fa9e0503cc681bcaa691f6f11d2f1e19ca8e6453` (`0.3.49-dev`).

## Command boundary

The existing experimental command shapes accept either their existing `.trb`
file-root input or an explicit config:

```text
compiler check INPUT
compiler emit-qbe INPUT
compiler build INPUT --output OUTPUT --qbe QBE --cc CC [--target PROFILE]
```

Only the exact basename `trbconfig.jsonc` selects project input. No upward
discovery, implicit current-directory selection, default executable location,
or automatic QBE/CC lookup is introduced. File-root behavior remains exact.

Configuration parsing, source enumeration, entrypoint selection, and
diagnostics remain TypeRB-authored compiler logic. The only new system boundary
is a narrow internal physical-directory adapter for Darwin and Linux arm64. It
must not run a shell or helper process, follow symlinks, enter the reference
repository, or become a public language API.

## Bootstrap introduction boundary

The retained Gate 6J compiler predates the physical-directory runtime adapter.
Because runtime QBE is emitted by the executable seed, that seed cannot include
the new adapter in its first output. Gate 6K therefore uses this explicit
Go-free introduction graph:

```text
retained Gate 6J Native seed -> untimed file-root transition
transition                   -> candidate B2
candidate B2                 -> candidate B3
candidate B3                 -> candidate B4
```

The transition compiles the current canonical compiler closure through the
existing ordinary file-root command. It is setup-only, is not required to
accept configured input, and is excluded from candidate timing and fixed-point
claims. It executes neither Go nor the reference compiler. Candidate B2, B3,
and B4 must all accept the registered configured projects and must converge to
exact QBE and executable bytes. A future Native seed that already contains the
adapter starts the ordinary chain directly and needs no transition.

## Configuration boundary

The registered JSONC projection supports comments without trailing commas and
strictly decodes:

- `$schema`, `name`, `version`, `mode`, `sourceDir`, `outDir`, `copyFiles`,
  `packageManagement`, and `go` at the root;
- `module`, `version`, and `rootPackage` below `go`;
- the reference defaults for omitted optional values; and
- only a nonblank project name, Go mode, and a nonblank Go module.

`sourceDir` and `outDir` must remain relative to the config directory without
escaping it. `packageManagement` must be `managed` or `external`, and the Go
version must be 1.27 or later. Unknown and duplicate fields, wrong JSON types,
malformed comments or JSON, unsupported modes, and every configuration field
that requires packages, native dependencies, database, jobs, lint, Ruby, or
TypeScript behavior fail deterministically.

`copyFiles`, `packageManagement`, and `outDir` are parsed and validated so the
project is interpreted consistently. They do not add file copying, package
synchronization, or implicit output placement to this slice.

## Production source boundary

The compiler recursively enumerates physical entries below `sourceDir`, sorts
root-relative paths bytewise, and checks every production source. It excludes
case-insensitive `_test.trb` files and prunes `.git`, `.trb`, `node_modules`,
and the configured `outDir`. Symlinked directories are not followed; a
symlinked `.trb` source is rejected; other non-source symlinks are ignored.

Every module retains its slash-normalized root-relative identity. Project
imports prefer `name.trb` over `name/index.trb`, preserve the current missing
import and cycle diagnostics, and cannot escape the source root. Exactly one
collected module must own a top-level runnable `def main()`. The source filename
does not select the entrypoint.

Permanent coverage must include defaults, JSONC string/comment boundaries,
strict config fields and types, root-contained paths, spaces, deterministic
ordering, exclusions, direct/index precedence, unimported invalid sources,
zero and duplicate entrypoints, missing imports, cycles, unreadable inputs,
symlinks, tool-launch suppression after compiler errors, atomic publication,
and intermediate cleanup.

## Registered corpus and scale workload

The checked-in
[`configured-project`](../corpus/gate6k/configured-project/trbconfig.jsonc)
fixture places `main()` in `application.trb`, proves root-relative direct-file
precedence, retains an unimported production source, and includes a test-only
module that must not enter the Native executable. It prints exactly
`configured-project-ok`. Its ordered seven-file manifest is 600 bytes with
SHA-256:

```text
03b741487a4eb338c44cfae1ad2f4d67f88015bca9c2fb24c447530f157cf284
```

Each manifest line is lowercase file SHA-256, two spaces, a `./`-prefixed
relative path, and LF, sorted bytewise by relative path. The manifest itself is
not part of the seven-file bundle.

The scale workload regenerates the exact Gate 6H graph below `src/`: one entry
plus 1,024 imported modules. Its ordered 94,322-byte source-content manifest
has SHA-256
`db438159189ba944283d8a92a09a1176020522c67d2551065c4010c50858f16b`.
The config is the exact checked-in Gate 6K config with SHA-256
`4ac3c76411dc5ed9a8786b267d734d6744301d56dd4617ba1c4799f419444806`.

Configured and file-root Native inputs must both emit the exact 124,139-byte
Gate 6H QBE program with SHA-256
`39f61f19bcd404732848604b568f4a5db3d70990ea233aaf8e337296d5d88874`,
build byte-identical same-basename applications, and print
`module-scale-ok`.

## Registered measurements

On the Gate 6J Darwin host, the controller records two warmups and eleven
alternating observations for check, emit, and build time, then an independent
peak-RSS series. Runtime uses three warmups and 31 retained alternating
observations. Correctness, hashing, stripping, execution validation, and
inventory remain outside timed intervals.

For the scale workload:

- configured Native check, emit, and build time and RSS must remain within 15%
  of the same candidate's file-root path;
- configured Native check and build time and RSS must remain within 25% of the
  pinned optimized-Go configured-project path;
- Native runtime and runtime RSS must remain within 25% of optimized Go;
- the stripped Native application must be at least 80% smaller; and
- output, QBE, repeated Native executables, and exit status must match exactly.

A fresh same-seed Gate 6J baseline bounds candidate canonical compiler emit
and build time and RSS to +15%. The stripped candidate compiler may not exceed
248,000 bytes. Candidate B2/B3/B4 compiler and QBE bytes must converge exactly,
and the Gate 6E representative, Gate 6I scalar Float, Gate 6J Float Array, and
full existing corpus must remain exact.

The pinned Gate 6D Linux arm64 image closes an ordinary exact B1/B2/B3/B4
candidate chain, re-emits the Darwin fixed-point QBE, builds the configured
small and scale projects twice, checks exact cross-target QBE and ELF identity,
runs both applications, and retains the negative and cleanup evidence. Linux
timing is diagnostic only.

## Exit condition

Gate 6K completes only after the implementation, permanent TypeRB-authored
measurement controller, raw Darwin and pinned Linux arm64 evidence, exact
fixed points and retained regressions, process/dependency inventory, and
reviewed result all pass issue #80 without weakening its registered workload
or thresholds.

The recorded result satisfies that condition with the original workload and
thresholds unchanged.

Config discovery, packages, native dependencies, stable CLI design, default
output placement, incremental caching, automatic tool discovery, source maps,
and release seed policy remain deferred.
