# 0010: Native-to-Native Bootstrap Closure

## Status

Accepted for Gate 6C.

## Context

Gate 6B proved that self-emitted B1 and B2 compilers can each build a working
compiler executable with their Native-owned `build` command. Its benchmark
compared independent generations prepared by the recovery driver, however. It
did not make one Native-built output the actual seed of the following build.

The intended ordinary release path uses a previously distributed Native
compiler to build the next Native compiler from TypeRB source. Demonstrating
that closure is distinct from proving that an output can check or emit the
source. Each generated artifact must be used as executable compiler input for
the next generation, and recovery provenance must remain visibly outside that
chain.

## Decision

Gate 6C defines this experimental bootstrap chain, with each output named
`compiler` in a separate directory:

```text
recovery setup only: reference compiler -> B0 -> B1 seed

ordinary chain:
B1 seed -> build compiler.trb -> Native B2
Native B2 -> build compiler.trb -> Native B3
Native B3 -> build compiler.trb -> Native B4
```

Every ordinary step uses the existing fixed Gate 6B command and the same
explicit QBE and CC paths. It does not use the reference compiler, recovery
driver, benchmark harness as a child, shell, or hidden source-content adapter.
The harness or test process that starts a measured command is an observer, not
a compiler stage.

B2, B3, and B4 must be byte-identical without normalization. Each must check
the checked-in compiler source, emit the same fixed-point QBE, retain ordinary
file-command behavior across the complete conformance corpus, and leave no
Native-owned intermediate. Feeding B2 and B3 into the next step proves that the
generated executable is a compiler seed rather than merely a runnable artifact.

The initial B1 seed may be produced by the documented Go-backed recovery path
during this experiment. Its exact provenance and hash must be recorded and its
creation excluded from ordinary-chain timing and ownership claims. A future
release may instead supply B1 as a previous Native release; Gate 6C does not
define release publication or trust policy.

This boundary is wholly internal to TypeRB Native. It requires no language,
compiler API, diagnostic, compatibility alias, documentation, or gate reference
in the TypeRB repository.

## Consequences

- Native self-hosting becomes a closed executable regeneration chain after one
  explicit seed handoff.
- Exact same-basename output identity is stronger than a source-level or
  normalized fixed-point claim.
- The recovery compiler remains available without being mistaken for an
  ordinary release dependency.
- Performance can be compared across actual adjacent Native generations rather
  than independently prepared lookalikes.
- QBE, CC, the assembler/linker, SDK, and system libraries remain explicit
  external dependencies.
- A reproducible chain does not by itself establish seed trust, release
  packaging, toolchain discovery, project loading, or production readiness.

## Alternatives considered

### Treat Gate 6B output execution as bootstrap closure

Rejected. Checking source and reproducing QBE demonstrates compiler behavior,
but it does not prove that the output can drive the next complete executable
build and preserve bytes through repeated seed replacement.

### Commit a Native seed binary now

Deferred. The repository remains experimental and has no accepted release,
artifact-signing, provenance, or binary-retention policy. A temporary measured
seed path is sufficient to prove the chain mechanics.

### Recreate B1 from Go for every ordinary generation

Rejected as an ownership claim. Go-backed recovery may produce the first seed,
but it is outside B1-to-B2 and every subsequent ordinary regeneration step.

### Add bootstrap support to TypeRB core

Rejected. The TypeRB-authored Native compiler and existing explicit external
tool boundary already provide the necessary behavior without a
consumer-specific reference-compiler surface.
