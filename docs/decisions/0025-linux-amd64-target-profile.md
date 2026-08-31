# Decision 0025: Linux amd64 Target Profile

## Status

Accepted for the Gate 6N experiment.

## Context

TypeRB Native closes ordinary self-hosted compiler chains on Darwin arm64 and
Linux arm64. Both environments exercise different operating-system and linker
boundaries, but they share one CPU architecture. A second architecture is
needed to expose assumptions in QBE target selection, the C ABI, generated
assembly, the managed runtime, and ELF linking before those assumptions become
harder to change.

QBE 1.3 implements the System V AMD64 ABI through its `amd64_sysv` target. A
fresh GitHub-hosted `ubuntu-24.04` runner provides an x64 environment distinct
from the existing `ubuntu-24.04-arm` runner. The Native compiler already keeps
target selection below its shared TypeRB-authored frontend and target-neutral
QBE emission.

The immutable experimental bootstrap release has no amd64 compiler seed. It
does contain the exact target-neutral root QBE used to create the original
arm64 seeds. A new architecture therefore needs one explicit recovery path
from that root without pretending that recovery is an ordinary previous-Native
release.

## Decision

Gate 6N adds the internal, versioned `linux-amd64-v0` profile beside the two
existing profiles:

| Profile | QBE target | Linker policy |
| --- | --- | --- |
| `darwin-arm64-v0` | `arm64_apple` | Darwin dead stripping |
| `linux-arm64-v0` | `arm64` | LLD and Linux dead stripping |
| `linux-amd64-v0` | `amd64_sysv` | LLD and Linux dead stripping |

The amd64 profile uses the existing explicit build shape, selects LLD through
`-fuse-ld=lld`, retains `-Wl,--gc-sections,--strip-all`, and links the existing
`-lm` boundary. It runs only on a Linux amd64 host in this gate. Automatic host
detection, cross compilation, and a stable target CLI remain deferred.

The compiler's lexer, parser, resolver, checker, diagnostics, target-neutral
QBE, managed runtime semantics, and conformance sources remain shared. The
profile changes only the QBE target and platform linker policy. An unknown
profile still fails before source or external-tool access.

The initial amd64 recovery verifies the immutable release root QBE's registered
size and SHA-256, translates it with QBE `amd64_sysv`, and links one root-era
compiler on the fresh x64 runner. That compiler emits the current compiler
QBE. External QBE and CC then create the first current-source transition. Its
compiler logic owns the new profile, but its executable driver was still
emitted by the root-era compiler and therefore cannot select that profile for
an ordinary build. It emits the compiler once more, and external QBE and CC
create the current-runtime transition whose driver owns the new profile. That
compiler enters the candidate B2/B3/B4 chain.

The root-era compiler and both current-source transitions are setup provenance.
They execute neither Go nor the reference compiler, but they are excluded from
candidate timing, size, and previous-release claims. Candidate B2, B3, and B4
must be exact and each generated compiler must execute the following complete
ordinary build.

The candidate process graph may contain the Native compiler, QBE, the explicit
C driver, assembler, LLD, loader, and system libraries. It must not contain Go,
the reference compiler, a recovery generator, a shell-mediated compiler child,
or hidden source-content input.

This decision is internal to TypeRB Native. It changes no TypeRB syntax,
semantics, package, diagnostic, or reference-repository behavior and does not
declare Linux amd64 supported.

## Consequences

- One target-neutral compiler and runtime must close exact fixed points on two
  CPU architectures and three execution environments.
- The immutable root remains sufficient recovery provenance for a new QBE
  target without adding Go to the ordinary candidate chain.
- Linux amd64 adds QBE, System V ABI, C-driver, LLD, libc, libm, and loader
  identities to the recorded toolchain matrix.
- A future distributed amd64 seed requires a new immutable release decision;
  Gate 6N does not modify the existing two-target bootstrap release.
- Current compatibility metadata may describe the verified profile separately
  from the older seed's target asset set once formal evidence exists.
- A target-specific runtime fork, semantic workaround, or post-link
  normalization cannot satisfy this gate.

## Alternatives considered

### Use the arm64 seed under emulation as the ordinary compiler

Rejected. Emulation can be a diagnostic tool, but keeping it in every compiler
generation would obscure the amd64 executable seed boundary and distort
performance and distribution measurements.

### Recreate a compiler through the Go reference implementation

Rejected for the Gate 6N recovery path. The immutable target-neutral Native
root can establish the architecture without adding a host-language compiler.

### Add automatic host detection with the target

Deferred. Explicit profile selection keeps the ABI and linker recipe visible
in bootstrap evidence. Host defaults and tool discovery require a separate CLI
and distribution decision.

### Publish a Linux amd64 seed immediately

Deferred. The target must first close correctness, reproducibility,
performance, size, and process-boundary evidence. Distribution would require a
new immutable manifest, assets, attestations, and compatibility record.
