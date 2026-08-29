# Decision 0018: Explicit Configured-project Executables

## Status

Accepted for the Gate 6K experiment.

## Context

Gate 6E introduced executable file-root import closures, and Gate 6H proved
that the same self-hosted module graph scales beyond one thousand files. A
file-root build deliberately ignores unrelated source files and requires its
entrypoint in the selected root module. A normal TypeRB project instead owns a
standard `trbconfig.jsonc`, checks its complete production source set, derives
module identity from `sourceDir`, and selects the project's unique runnable
entrypoint regardless of filename.

Configured projects are therefore the smallest remaining boundary between the
ordinary self-hosted compiler and a representative TypeRB application build.
The complete TypeRB project model also includes config discovery, packages,
native dependencies, generated integrations, output policy, and other product
behavior. Taking all of that at once would mix independent language,
distribution, and performance questions.

## Decision

The experimental `check`, `emit-qbe`, and `build` commands accept a path whose
exact basename is `trbconfig.jsonc`. The config's directory is the project
root. The compiler parses a strict, bounded projection of the reference
configuration, validates Go mode and root-contained paths, and collects every
production `.trb` file below `sourceDir` in deterministic order.

The projection includes project identity, version, source and output
directories, copy and package-management policy, and the portable Go module,
version, and root-package fields. Reference defaults are preserved. Fields
that would require package, database, jobs, lint, Ruby, TypeScript, or native
dependency behavior are rejected explicitly rather than ignored. Unknown,
duplicate, malformed, or incorrectly typed members also fail. Duplicate-key
rejection is an unambiguous unsupported-input boundary for this first slice;
it does not assign a different meaning to an accepted TypeRB program.

Collection is physical and does not invoke a shell or a source-discovery
subprocess. It prunes the reference build directories and production test
files, never follows directory symlinks, and rejects a symlinked `.trb` source
rather than reading through it. A narrow internal, versioned compiler-runtime
adapter may expose directory entries and file kinds on Darwin and Linux arm64.
It is not a public TypeRB filesystem API.

Every collected production source is parsed and checked, including unimported
files. Module names are root-relative, direct files retain precedence over
`index.trb`, cycles retain their existing diagnostics, and the complete
project must contain exactly one portable top-level `def main()`. The existing
file-root path and all language, Native MIR, runtime, QBE, target, and explicit
external-tool behavior remain unchanged.

## Consequences

A self-hosted compiler can build a representative project directly from its
explicit standard config without Go in the ordinary Native chain. The same
1,025-file source graph can measure config parsing and deterministic physical
collection against both the existing file-root path and the pinned optimized
Go compiler.

The command shape remains experimental, and `build` still requires an explicit
output. Upward config discovery, default artifact placement, test compilation,
packages, native dependencies, generated project integrations, incremental
caching, automatic tool discovery, source maps, and release seed policy remain
separate work. Exact correctness, performance, size, fixed-point, and
Darwin/Linux arm64 requirements are pre-registered in
[issue #80](https://github.com/type-rb/type-rb-native/issues/80).
