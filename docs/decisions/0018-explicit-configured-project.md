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

The adapter is introduced through one explicit bootstrap transition. Runtime
QBE is part of the output emitted by the compiler executable, so the retained
Gate 6J seed cannot place a runtime operation that did not exist at its own
revision into its first output. The retained Native seed therefore compiles the
current canonical compiler closure once through the existing file-root path to
produce an untimed transition compiler. That transition builds candidate B2,
then B2 builds B3 and B3 builds B4. B2, B3, and B4 must all support configured
projects and converge to exact QBE and executable bytes.

The transition is setup evidence, not a candidate generation, release seed, or
measured workaround. It executes neither Go nor the reference compiler, and it
does not weaken the ordinary Native-to-Native fixed-point requirement. Once a
distributed Native compiler already contains this adapter, later ordinary
bootstrap chains do not need the transition.

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

Adding a compiler-runtime operation across an older retained seed now has an
explicit introduction rule: use one Go-free, file-root transition outside the
candidate and measurement set, then require the new candidate generations to
close the exact fixed point. This rule records the real executable process
graph without treating predecessor runtime bytes as if they already contained
the new operation.

The command shape remains experimental, and `build` still requires an explicit
output. Upward config discovery, default artifact placement, test compilation,
packages, native dependencies, generated project integrations, incremental
caching, automatic tool discovery, source maps, and release seed policy remain
separate work. Exact correctness, performance, size, fixed-point, and
Darwin/Linux arm64 requirements are pre-registered in
[issue #80](https://github.com/type-rb/type-rb-native/issues/80).
