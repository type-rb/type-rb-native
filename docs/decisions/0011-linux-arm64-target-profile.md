# 0011: Linux arm64 Target Profile

## Status

Accepted for Gate 6D. The current Linux linker selection is amended by
[Decision 0022](0022-linux-arm64-lld-linker.md).

## Context

The closed Native bootstrap chain initially emits and links only Darwin arm64
executables. Product feasibility needs a second primary environment before the
compiler accumulates more platform assumptions. Linux arm64 is the smallest
useful next step: QBE 1.3 supports its AArch64 target, a native Linux arm64
environment is available, and the compiler's frontend, QBE IL, and runtime
semantics should remain shared with Darwin.

Target selection must not turn into a Native-only language feature or leak
into the reference TypeRB repository. The current `build` command is still an
experimental internal interface, but it also needs an unambiguous profile so a
compiler running on one platform does not silently choose another platform's
ABI or linker policy.

## Decision

Gate 6D adds the internal, versioned `linux-arm64-v0` profile beside
`darwin-arm64-v0`. The fixed experimental command accepts an explicit suffix:

```text
compiler build SOURCE --output OUTPUT --qbe QBE --cc CC --target PROFILE
```

The existing nine-argument command remains a Darwin compatibility shape during
this gate. It is not a host-detection rule or a stable CLI promise. An unknown
profile fails with status 64 and a deterministic diagnostic before source I/O
or an external tool is attempted.

The two profile adapters select only target-specific backend and linker policy:

| Profile | QBE target | Linker policy |
| --- | --- | --- |
| `darwin-arm64-v0` | `arm64_apple` | `-Wl,-dead_strip` |
| `linux-arm64-v0` | `arm64` | `-Wl,--gc-sections,--strip-all` |

Linux link-time stripping removes the non-runtime ELF symbol and string tables.
In addition to reducing the shipped artifact, this excludes a random temporary
object name that the system compiler driver otherwise records in `.strtab`.
It does not normalize code or data after linking: repeated generations must
still produce exact executable bytes.

The compiler's lexer, parser, resolver, checker, QBE emitter, QBE IL, language
semantics, and runtime implementation remain shared. File `check` and
`emit-qbe` commands are target-neutral. Gate 6D does not introduce target
conditionals in TypeRB source or fork the conformance corpus.

Linux recovery may translate the target-neutral B1 QBE through QBE and the
Linux system C toolchain. Once that seed exists, the ordinary B1 to B2 to B3 to
B4 chain uses only Native compiler executables plus the explicit QBE and CC
boundaries. Recovery provenance remains outside the ordinary chain.

This decision is wholly internal to TypeRB Native. It requires no TypeRB
language change, reference-compiler API, documentation, diagnostic, or
compatibility alias.

## Consequences

- The same self-hosted compiler source can close a Native seed chain on Darwin
  arm64 and Linux arm64.
- Profile names version the experimental OS, architecture, ABI, backend, and
  linker contract without making it public or stable.
- External QBE, assembler, linker, libc, and Linux loader dependencies remain
  visible and count toward measurement and distribution reports.
- Link-time stripping is part of the Linux artifact recipe and must be reported
  when Linux size is compared with Darwin or another toolchain.
- Adding another profile requires its own target mapping, ABI/runtime audit,
  deterministic failure behavior, executable inspection, and full Native
  regeneration evidence.
- This slice does not add automatic host discovery, cross compilation,
  packaging, static linking, musl support, or a stable target-selection CLI.

## Alternatives considered

### Infer the profile from the compiler host

Deferred. Silent host inference would hide the target contract from the
bootstrap record and make cross compilation ambiguous. A later product CLI may
offer a host default after discovery and configuration are designed.

### Duplicate the compiler or runtime for Linux

Rejected. Platform-specific lowering and linking belong below the shared
frontend, MIR semantics, and runtime behavior. A fork would weaken the value of
the second-environment test.

### Compare executables only after external normalization

Rejected. Gate 6D requires the ordinary linker recipe itself to emit stable
bytes. Link-time removal of non-runtime symbol tables is explicit artifact
policy; an after-the-fact comparison rewrite would conceal output differences.

### Add the target to the reference TypeRB repository

Rejected. Target profiles, QBE orchestration, and this gate's compatibility
shape are owned entirely by TypeRB Native.
