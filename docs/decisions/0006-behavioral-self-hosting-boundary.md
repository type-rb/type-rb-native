# 0006: Behavioral Self-Hosting Boundary for Gate 4

## Status

Accepted for Gate 4.

## Context

Gate 3 proves that QBE can execute the managed values and closures needed by a
compiler, but the executable path still receives typed snapshots from the Go
reference frontend. Self-hosting requires a repository-owned frontend and
driver written in TypeRB. It must be possible to distinguish a compiler from a
source-specific generator or a fixed-point artifact that merely reproduces
itself.

Gate 4 is the first completeness checkpoint, not the product-feasibility gate.
Requiring the complete language, package system, production CLI, multiple
targets, and byte-equivalent compiler artifacts at once would hide which
frontend or bootstrap invariant failed. Conversely, accepting a quine,
embedded QBE, or a compiler for a non-TypeRB demonstration language would not
advance the intended implementation.

The checked-in compiler source needs a runtime input boundary. Adding a
consumer-specific operation to the reference compiler would couple TypeRB to
this experiment. The native executable already owns its entry ABI, so it can
adapt host arguments to an ordinary TypeRB function without changing the
language or the reference repository.

## Decision

Gate 4 establishes **behavioral self-hosting** for a documented TypeRB subset.
The repository contains a compiler source closure written only in TypeRB with
separate lexical, parsing, resolution, checking, and QBE-emission passes. The
subset is deliberately bounded, but every construct used by that compiler
must be accepted through the same frontend that compiles conformance inputs.

The bootstrap stages are:

```text
pinned Go reference frontend + snapshot v4 + native QBE adapter -> B0
B0 compiling the checked-in TypeRB compiler source             -> B1
B1 compiling the same TypeRB compiler source                   -> B2
```

B0 is a recovery seed. The B1-to-B2 process graph must contain no Go tool,
reference `trb` executable, Go-linked compiler component, or semantic fallback.
QBE, the platform assembler/linker, the SDK, and system libraries remain
explicit external dependencies.

The TypeRB source declares `compiler_main(source: String, mode: String)` as an
ordinary repository-internal function. The Gate 4 native entry adapter converts
two host arguments to managed Strings and calls that function. Source text is
therefore supplied at runtime while snapshot v4 continues to see only ordinary
functions and values. This adapter is an unstable executable ABI owned by this
repository; it is not TypeRB syntax, a standard-library API, or a reference
snapshot feature.

The initial driver accepts one complete source unit as an argument and either
checks it or emits deterministic QBE to standard output. A shell-free bootstrap
harness may feed the emitted QBE to QBE and the system linker. File discovery,
multi-module loading, and direct process orchestration are deferred until the
frontend can represent their full portable contracts.

Gate 4 compares observable compiler behavior across B0, B1, and B2. Every
stage must agree on successful output and on stable lexical, syntax, resolution,
arity, and type diagnostics. Repeated emission must be byte-identical. At least
two source mutations must change the generated program and its runtime result.
B1/B2 executable identity remains a Gate 5 requirement so that normalization,
linker metadata, and release-seed policy are decided with representative
artifacts.

The compiler-emitted bootstrap runtime may use process-lifetime allocation for
compiler processes during this gate. It must retain checked bounds and portable
value behavior for the supported subset. This does not replace or weaken the
Gate 3 tracing runtime: it is a bounded compiler-process implementation that
must be integrated with the managed runtime before product feasibility.

## Consequences

- Gate 4 demonstrates an actual parser, resolver, checker, and code generator
  compiling their own TypeRB source, rather than a quine or another language.
- The reference repository and snapshot version remain unchanged.
- B1 and B2 need no Go dependency, while B0 remains reproducible as a recovery
  route.
- Passing this gate does not imply full TypeRB source compatibility or a
  supported native compiler CLI.
- The source-content argument adapter and process-lifetime compiler allocator
  are explicit temporary product boundaries. Gate 5 measures and improves the
  matched compiler core; Gate 6 replaces them before product feasibility can
  pass.
- QBE remains the active backend because Gate 4 asks a frontend/self-hosting
  question; adding another backend would not answer it more directly.

## Alternatives considered

### Embed the compiler source or a precomputed artifact

Rejected. It could produce a fixed point without exercising source input,
parsing, resolution, checking, or general code generation.

### Add argv or filesystem operations to the reference snapshot

Rejected for this gate. The native entry adapter supplies the required runtime
input without expanding a temporary cross-repository surface.

### Require the complete language before the first bootstrap

Deferred to Gate 6 product-feasibility progression. A documented subset that
genuinely compiles its own compiler exposes the bootstrap invariants earlier
while unsupported portable behavior continues to fail explicitly.

### Switch to generated C for self-hosting

Rejected for Gate 4 because QBE already passed the runtime gates and the
frontend question does not justify introducing another backend and toolchain
comparison. Generated C remains a future measured option only if profiling
identifies a concrete role.
