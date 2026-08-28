# 0009: Native-Owned Single-File Executable Build

## Status

Accepted for Gate 6B.

## Context

Gate 6A gave self-emitted Native compiler generations an ordinary file input,
but producing an executable still required a host-side recipe to capture QBE
IL, invoke QBE, and invoke the C toolchain. That recipe was useful for isolating
source ingress, but it was not an ordinary Go-free application-build path.

Gate 6 product feasibility needs the TypeRB-authored compiler to own the build
sequence while keeping QBE, the assembler, linker, SDK, and system libraries as
explicit external components. The first orchestration slice should remain
small enough to compare directly with the established external recipe. It must
not introduce project discovery, toolchain discovery, a permanent command
contract, or a shell wrapper.

## Decision

Self-emitted B1 and later compiler generations accept this fixed-order,
repository-internal command:

```text
compiler build SOURCE --output OUTPUT --qbe QBE --cc CC
```

The compiler reads `SOURCE`, runs the checked TypeRB frontend and QBE emitter,
and writes QBE IL to `OUTPUT.trbn.ssa`. It directly invokes the supplied `QBE`
path for the `arm64_apple` target and writes `OUTPUT.trbn.s`, then directly
invokes the supplied `CC` path with `-Wl,-dead_strip`. The implementation uses
`fork`, `execv`, and `waitpid`; it never invokes a shell, Go, or the reference
compiler.

The fixed flag order is deliberate. It makes exact usage and phase behavior
measurable without prematurely designing the eventual project CLI or
toolchain-configuration model. Existing `check SOURCE`, `emit-qbe SOURCE`, and
the hidden recovery adapter keep their Gate 6A roles.

The build command has these process contracts:

- success writes no stdout or stderr and returns status 0;
- compiler diagnostics are written to stderr and return status 1 before an
  external tool is launched;
- invalid command shape returns status 64 with exact usage;
- unreadable source returns status 66 with the existing path-bearing error;
- intermediate creation or final publication failure returns status 73;
- a QBE or CC failure preserves inherited child stderr, appends one exact
  Native phase diagnostic, cleans all build artifacts, and returns status 70.

The driver redirects only its own successful QBE stream. It restores stdout
before launching children or returning, so compiler diagnostics remain on
stderr and child streams retain ordinary process behavior.

Final publication is atomic on the output filesystem. The driver creates an
adjacent `OUTPUT.trbn.XXXXXX` directory with `mkdtemp`, links a temporary
executable inside it using the same basename as `OUTPUT`, and renames the
finished file over `OUTPUT`. The matching basename is significant on Darwin:
the arm64 linker creates an ad-hoc code signature whose identifier includes the
output basename. Keeping it stable makes Native-owned and external-recipe
outputs byte-identical without disabling required executable metadata. The
driver removes the QBE IL, assembly, temporary executable, and temporary
directory on every post-creation exit path.

This command is an implementation boundary in TypeRB Native, not a TypeRB
language feature or supported CLI. It requires no API, diagnostic, test,
documentation, or compatibility change in the reference TypeRB repository.

## Consequences

- A self-emitted Native compiler can build a single-file executable without Go
  or a host-language wrapper.
- QBE and the platform C toolchain remain explicit, caller-supplied external
  dependencies whose time, memory, and distribution size must be measured.
- Existing output survives compiler, QBE, and CC failure; a successful build
  replaces it atomically.
- Output paths and explicit tool paths may contain spaces because no shell
  command is assembled.
- Child exit and signal status is observed internally, while the experimental
  command exposes stable phase status 70.
- Darwin arm64 remains the only target in this slice.
- Project loading, multi-module compilation, toolchain discovery, production
  runtime integration, incremental builds, and a supported user-facing build
  command remain later Gate 6 work.

## Alternatives considered

### Keep the external orchestration recipe

Rejected as the ordinary path. It would leave executable construction owned by
the test or benchmark host and would not demonstrate a Go-free Native compiler
driver.

### Invoke a shell command

Rejected. Quoting would become part of correctness, paths containing spaces
would be fragile, child identity would be obscured, and the ordinary process
graph would contain an unnecessary host dependency.

### Link directly to the requested output

Rejected because a failed link could truncate or replace an existing output.
An adjacent temporary directory permits an atomic final rename while retaining
the requested basename for deterministic Darwin code signing.

### Disable the Mach-O UUID or ad-hoc signature

Rejected after direct execution checks. Removing the ad-hoc signature causes
arm64 execution to be killed, and removing the UUID produces a dyld rejection
on the measured macOS environment. Stable naming preserves reproducibility
without stripping metadata required by the platform.

### Add build APIs or toolchain configuration to TypeRB core

Rejected. This experimental orchestration belongs entirely to TypeRB Native;
the reference repository remains consumer-neutral.
