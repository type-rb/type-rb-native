# TypeRB 0.4.3 Development Compatibility Revalidation Results

The TypeRB `0.4.3-dev` compatibility successor passes its registered exact-
reference, source, semantic, previous-seed, fixed-point, target, process,
elapsed-time, peak-RSS, and compiler-size criteria on Darwin arm64 and Linux
arm64.

The existing immutable
[`bootstrap-seed-2026-08-30`](https://github.com/type-rb/type-rb-native/releases/tag/bootstrap-seed-2026-08-30)
reaches the current TypeRB-authored Native compiler without Go or the reference
compiler. Because that seed predates the current emitter, embedded managed
runtime, and link policy, each target uses two separately identified setup-only
Native transitions before candidate B2. Candidate B2, B3, and B4 are exact
within each target, and both targets emit the same fixed-point QBE.

This remains an experimental subset result. It does not establish Native
SemVer, a supported TypeRB version range, complete TypeRB `0.4.3-dev` language
coverage, Web compatibility, or production support.

## Registered scope and revisions

- preregistered scope:
  [issue #106](https://github.com/type-rb/type-rb-native/issues/106)
- selected TypeRB source and semantic oracle:
  `2cf63e95b4fc1a92f6094e2c89c47fb75262adae` (`0.4.3-dev`)
- measured Native compiler source and workflow revision:
  `0b5429c2cf415d5db8bc4672ef3d4e6855fe5e2c`
- immutable seed source revision:
  `0058818314977633c50393796ef9b9f8f1fda50f`
- QBE 1.3 source archive: 281,332 bytes, SHA-256
  `d587905d620dc5e1d2bfa7c2cc642b9b837aa89a3188c6e37b53d756cf66e320`
- successful cross-target workflow:
  [Actions run 33301130958](https://github.com/type-rb/type-rb-native/actions/runs/33301130958)
- exact pin, compatibility mapping, and executable differential:
  [PR #109](https://github.com/type-rb/type-rb-native/pull/109)
- explicit setup-transition verifier:
  [PR #110](https://github.com/type-rb/type-rb-native/pull/110)

The initial
[Actions run 33300217968](https://github.com/type-rb/type-rb-native/actions/runs/33300217968)
is retained as negative evidence. It put the published seed directly before
candidate B2 and failed the B2/B3 comparison on both targets. The first output
carried the seed runtime while the next carried the current runtime, so those
unlike setup generations could not honestly be candidate fixed points. PR #110
made both Go-free transitions explicit without changing any candidate
exactness, performance, process, or size criterion.

## Source and semantic result

The selected reference range contains the TypeRB 0.4.1 and 0.4.2 releases,
owner-qualified Web API changes outside the current self-hosted subset, shared
Array alias fixes in the Go backend, nested Go runtime-helper propagation, and
the distinction between Nil values and Void results.

`compiler/gate4/conformance/valid/array-aliases.trb` fixes the representable
semantic change as executable evidence. It grows one Integer Array through two
aliases, mutates it through a mutable parameter, rebinds that parameter to a
different Array, and then mutates the original through the caller alias. This
requires outer Array identity and destructive growth to remain shared while
parameter rebinding stays local.

The protected PR run
[33299800304](https://github.com/type-rb/type-rb-native/actions/runs/33299800304)
passes all selected-reference formatting and source checks, 76 root tests, 25
Gate 6F through Gate 6K policy tests, and 31 focused self-hosted frontend tests.
Recovery B0/B1/B2, current Native B2/B3/B4, and the same TypeRB-authored
compiler built by the selected Go reference emit byte-identical QBE for the
new fixture and produce `array-aliases-ok`.

Repository-owned source also passes the selected checker's Nil/Void boundary.
Native does not infer full nullable, Void, owner-qualified Web, or broader
language compatibility from that success. Unsupported source remains outside
the self-hosted subset and must fail explicitly.

## Previous-seed transition and fixed point

The verified chain on each target is:

```text
verified immutable platform seed
    -> current compiler source -> first current-source transition
first transition
    -> current compiler source -> current-runtime transition
current-runtime transition
    -> current compiler source -> candidate B2
B2  -> current compiler source -> candidate B3
B3  -> current compiler source -> candidate B4
```

The first two generated compilers are setup evidence, not candidates or
release seeds, and are excluded from candidate timing and size claims. Go, the
reference `trb`, a recovery compiler, and the one-time root QBE are absent.
QBE, the explicit system CC, assembler, linker, system libraries, and workflow
observer remain external recorded components.

| Target | Published seed | First transition | Current-runtime transition |
| --- | --- | --- | --- |
| Darwin arm64 | 259,032 bytes; `ef438d13598c534766334b408a39715c56ff1b69db528910ebf7d90ec7720b65` | 269,448 bytes; `8291cd31d8926fab554935626252f69a7d953f160c572f94ed071c7d4aab04f8` | 304,392 bytes; `b0a554aea3d05bc068f832a126188bdaa2dfdd16bec1bef331a0ee4bc90bd3d4` |
| Linux arm64 | 241,488 bytes; `b4307c244edc9e4da620f2a7c1b03a733e575da032efefae615f9edf75048a37` | 256,552 bytes; `2c90a72fea09b8746ea920ff5b5f0dbcd786cf0f88e05b17b53c138ffa9271e4` | 261,664 bytes; `be0a11356ecbffc214d6e4983dc44b4a823a35c404dbb4aeac20e9c79665c57e` |

| Target | Exact candidate B2/B3/B4 bytes and SHA-256 |
| --- | --- |
| Darwin arm64 | 283,048; `cf10c78817dee3889faba263155e6157a403167a1e67034bc780b21c663a1730` |
| Linux arm64 | 261,664; `be0a11356ecbffc214d6e4983dc44b4a823a35c404dbb4aeac20e9c79665c57e` |

Every candidate compiler emits the exact same 853,095-byte target-neutral QBE
program with SHA-256
`06157dcfc29157657df8749e28ad0f58b4459663d8f9319bcdfa0f94154625cf`.
Platform executable bytes are required to be exact within one pinned target
run; they are not claimed to be identical across executable formats or system
linker versions.

The harness checks each candidate against the canonical compiler source and
the complete valid, invalid, mutation, runtime-invalid, Float, Float Array,
managed-root, file-root, and configured-project corpus. It proves repeated QBE
determinism, mutation sensitivity, exact diagnostics, failure output
preservation, unknown-target rejection before tool execution, paths containing
spaces, intermediate cleanup, and the exact `configured-project-ok` result.

## Process and dependency boundary

The Linux setup-transition trace contains 30 process-execution attempts across
the two builds; the candidate B4 trace contains 15. They cover Native
compilers, QBE, `/usr/bin/cc`, assembler lookup and execution, `collect2`, and
the linker. Neither trace contains Go, reference `trb`, a recovery compiler,
or a shell-mediated compiler child. The generated Linux compiler is a PIE
executable with `BIND_NOW` and `RELRO` and depends on `libc.so.6`.

Darwin records the direct Native-to-QBE and Native-to-CC boundary for both
setup transitions and the candidate chain. The generated Mach-O arm64 compiler
depends on `/usr/lib/libSystem.B.dylib`.

## Measurements

Each target performs two warmups followed by seven retained interleaved
observations of candidate B2-to-B3 and B3-to-B4. Setup transitions are excluded.
Elapsed values are seconds; peak RSS is bytes.

| Target and metric | B2-to-B3 | B3-to-B4 | Spread |
| --- | ---: | ---: | ---: |
| Darwin elapsed | 2.16 | 2.12 | 1.89% |
| Darwin peak RSS | 36,126,720 | 36,061,184 | 0.18% |
| Linux elapsed | 1.03 | 1.02 | 0.98% |
| Linux peak RSS | 15,007,744 | 15,007,744 | 0.00% |

Every spread is below the registered 25% bound and far below the catastrophic
2x threshold. This compatibility revalidation registers no application-speed
improvement claim; its performance criterion is stable adjacent Native
regeneration while preserving retained behavior.

## Compiler size

| Target | Candidate compiler bytes | Limit | Headroom |
| --- | ---: | ---: | ---: |
| Darwin arm64 | 283,048 | 310,000 | 8.69% |
| Linux arm64 | 261,664 | 310,000 | 15.59% |
| Combined | 544,712 | 620,000 | 12.14% |

Every candidate generation satisfies the per-target limit. Setup transition
sizes are reported separately and are not substituted for candidate size.

## Seed decision

The attested platform seeds remain sufficient to reach exact current fixed
points, but their older embedded runtime requires two setup transitions. A
future published seed containing the current runtime can remove that setup
cost. Publishing a new seed solely to align the TypeRB revision string remains
unnecessary; independent Native versioning, installation, recovery, and seed
distribution policy are separate decisions.

## Raw evidence

- [`darwin-arm64`](darwin-arm64) contains candidate measurements, identities,
  environment, executable inspection, release response, and attestation
  verification output.
- [`linux-arm64`](linux-arm64) contains the same candidate evidence plus the
  complete process trace and ELF inspection.
- [`setup-transition/darwin-arm64`](setup-transition/darwin-arm64) and
  [`setup-transition/linux-arm64`](setup-transition/linux-arm64) contain
  transition identities, checksums, stdout/stderr, and process evidence.
- [`combined-size.txt`](combined-size.txt) records the cross-target aggregate.
- [`EVIDENCE_SHA256SUMS`](EVIDENCE_SHA256SUMS) covers all 55 retained raw
  evidence files.

Compiler binaries are intentionally not committed to Git history. The input
seed remains available from the immutable release, while transition and
candidate identities are retained by size and SHA-256.
