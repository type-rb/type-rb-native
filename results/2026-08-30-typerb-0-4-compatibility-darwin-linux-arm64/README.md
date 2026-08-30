# TypeRB 0.4 Compatibility Revalidation Results

The TypeRB 0.4 declaration-import compatibility slice passes its registered
source, semantic, previous-seed, fixed-point, target, process-boundary,
elapsed-time, peak-RSS, and compiler-size criteria on Darwin arm64 and Linux
arm64.

The existing immutable
[`bootstrap-seed-2026-08-30`](https://github.com/type-rb/type-rb-native/releases/tag/bootstrap-seed-2026-08-30)
successfully builds the current TypeRB-authored Native compiler. The generated
B2, B3, and B4 compilers are exact within each target, and both targets emit
the same fixed-point QBE. No replacement seed is required merely because the
TypeRB source pin advanced.

This remains an experimental subset result. It does not establish Native
SemVer, a supported TypeRB version range, complete TypeRB 0.4 language
coverage, or production support.

## Registered scope and revisions

- preregistered scope:
  [issue #97](https://github.com/type-rb/type-rb-native/issues/97)
- selected TypeRB source and semantic oracle:
  `7fcc1d7f8978d5335368c1d4d3be4c79db86d995` (`0.4.1-dev`)
- measured Native compiler source and workflow revision:
  `1c5e7df8436c7c0d6c9fef575af69dd88b37d27d`
- immutable seed source revision:
  `0058818314977633c50393796ef9b9f8f1fda50f`
- QBE 1.3 source archive: 281,332 bytes, SHA-256
  `d587905d620dc5e1d2bfa7c2cc642b9b837aa89a3188c6e37b53d756cf66e320`
- final cross-target workflow:
  [Actions run 33286460410](https://github.com/type-rb/type-rb-native/actions/runs/33286460410)
- source migration:
  [PR #98](https://github.com/type-rb/type-rb-native/pull/98)
- self-hosted declaration-import semantics:
  [PR #99](https://github.com/type-rb/type-rb-native/pull/99)
- seed/current-source identity and measurement tooling:
  [PR #100](https://github.com/type-rb/type-rb-native/pull/100)

The workflow first checks out the immutable release tag and separately checks
out the exact current compiler-source revision. It verifies release state,
manifest, checksums, and GitHub artifact attestations before making the
downloaded seed executable. The old seed identity and new compiler fixed point
therefore remain distinct and auditable.

## Source and semantic result

Repository-owned TypeRB source is in the selected 0.4 declaration-root form.
The reference compiler formats and checks it, while focused differential
fixtures exercise exact named imports, aliases, unique bare record roots, the
ASCII root-key rule, directory-index identity, loaded peer conflicts,
canonical declaration identity, collisions, unused bindings, and unsupported
forms.

The full QBE-enabled suite passes 76 tests. The focused self-hosted frontend
passes 30 tests. Native and the selected Go/reference compiler build the same
declaration-import application and print `declaration-imports-ok`; both reject
the direct/index conflict. Snapshot v4, the retained valid, invalid, mutation,
runtime-invalid, Float, Float Array, file-root, and configured-project paths
remain covered by the ordinary CI and previous-seed harnesses.

The implemented mapping remains intentionally smaller than TypeRB 0.4.
Package imports, capability activation, modules, classes, enums, interfaces,
aliases, newtypes, constants, owned nested declarations, and project-aware
formatter rewriting remain explicit unsupported surface rather than falling
back to pre-0.4 import behavior.

## Previous-seed fixed point

The ordinary target chain is:

```text
verified immutable platform seed B1
    -> current TypeRB-authored compiler source -> B2
B2  -> current TypeRB-authored compiler source -> B3
B3  -> current TypeRB-authored compiler source -> B4
```

Go, the reference `trb`, a recovery compiler, and the one-time root QBE are
absent from this chain. QBE, the explicit system CC, assembler, linker, system
libraries, and the workflow observer remain external recorded components.

| Target | B1 bytes and SHA-256 | Exact B2/B3/B4 bytes and SHA-256 |
| --- | --- | --- |
| Darwin arm64 | 259,032; `ef438d13598c534766334b408a39715c56ff1b69db528910ebf7d90ec7720b65` | 276,296; `d74b89057f694da13672ef30aef465e9a19fb8e50ad35c6e9d4b7058d853eae4` |
| Linux arm64 | 241,488; `b4307c244edc9e4da620f2a7c1b03a733e575da032efefae615f9edf75048a37` | 242,048; `3f937a873de0e267c0a947f4413da2d56ee9930369318aff8f7a78e43c94093a` |

B2, B3, and B4 on both targets emit the exact same 684,995-byte QBE program
with SHA-256
`e01dd77129bbfc293e834a653cbe9b5b9e697916c147690113d7b1bd62037ee4`.
Platform executable bytes are required to be exact within one pinned target
run; they are not claimed to be identical across different executable formats
or system linker versions.

Every generated compiler checks and emits its own canonical source closure.
The harness also checks and executes the retained conformance cases, proves
mutation sensitivity, checks deterministic invalid diagnostics, preserves
existing outputs across QBE and CC failures, rejects unknown targets before
tool execution, accepts paths containing spaces, and leaves no Native
intermediate after success or failure. The configured application prints
exactly `configured-project-ok`.

## Process and dependency boundary

The Linux `strace` inventory contains 18 process-execution records covering
the B4 compiler, QBE, `/usr/bin/cc`, assembler lookup and execution,
`collect2`, and the linker. It contains no Go, reference `trb`, recovery
compiler, or shell-mediated Native compiler child. The generated Linux
compiler is a PIE executable with `BIND_NOW` and `RELRO` and depends on
`libc.so.6`.

Darwin records the same direct Native-to-QBE and Native-to-CC boundary. The
generated Mach-O arm64 compiler depends on `/usr/lib/libSystem.B.dylib`.

## Measurements

Each target uses two warmups followed by seven retained interleaved
observations of B1-to-B2, B2-to-B3, and B3-to-B4. Elapsed values are seconds;
peak RSS is bytes.

| Target and metric | B1-to-B2 | B2-to-B3 | B3-to-B4 | Largest spread |
| --- | ---: | ---: | ---: | ---: |
| Darwin elapsed | 1.13 | 1.16 | 1.17 | 3.54% |
| Darwin peak RSS | 36,126,720 | 36,175,872 | 36,159,488 | 0.14% |
| Linux elapsed | 0.39 | 0.38 | 0.39 | 2.63% |
| Linux peak RSS | 20,619,264 | 20,692,992 | 20,692,992 | 0.36% |

Every spread is below the registered 25% bound and far below the catastrophic
2x threshold. This compatibility slice registered no new application-speed
improvement claim; its performance criterion is stable adjacent Native
regeneration while preserving retained behavior.

## Compiler size

| Target | Current compiler bytes | Per-target limit | Headroom |
| --- | ---: | ---: | ---: |
| Darwin arm64 | 276,296 | 310,000 | 10.87% |
| Linux arm64 | 242,048 | 310,000 | 21.92% |
| Combined | 518,344 | 620,000 | 16.40% |

Every B1, B2, B3, and B4 generation also satisfies the per-target limit. The
current compiler is 6.66% larger than the previous Darwin seed and 0.23% larger
than the previous Linux seed while adding the selected source and semantic
compatibility; both remain within the preregistered distribution bounds.

## Seed decision

The old, attested platform seeds are sufficient to cross the TypeRB 0.4 source
and import-semantics change and reach exact current fixed points. The immutable
release remains unchanged. Publishing another seed solely to align source
revision strings would add distribution and trust work without improving
bootstrap feasibility, so this result does not do so.

A later seed remains appropriate only when a concrete distribution need is
defined, such as an independent Native version, installation path, supported
compatibility policy, additional target, or recovery requirement. Those are
separate design and evidence tasks.

## Raw evidence

- [`darwin-arm64`](darwin-arm64) contains measurements, identities,
  environment, executable inspection, release response, and attestation
  verification output.
- [`linux-arm64`](linux-arm64) contains the same evidence plus the complete
  process trace and ELF inspection.
- [`combined-size.txt`](combined-size.txt) records the cross-target aggregate.
- [`EVIDENCE_SHA256SUMS`](EVIDENCE_SHA256SUMS) covers all 39 retained raw
  evidence files.

Compiler binaries are intentionally not committed to Git history. The input
seed remains available from the immutable release, while generated compiler
identity is retained by size and SHA-256.
