# Gate 6L Experimental Bootstrap Seed Distribution

Gate 6L turns the completed Gate 6K compiler fixed point into a durable,
attested previous-Native bootstrap handoff for Darwin arm64 and Linux arm64.
The scope and bounds were registered before implementation in
[issue #90](https://github.com/type-rb/type-rb-native/issues/90). The trust and
ownership boundary is defined by
[Decision 0019](decisions/0019-experimental-bootstrap-seed-distribution.md).

## Status

Pre-registered. No bootstrap seed release has been published yet.

## Public baseline

- TypeRB Native main: `24dc4876cc71a4ee56ceb9ba995841e7791da9ff`
- Gate 6K implementation:
  `84e2e4a6e2cff9d7fdab46ce4eec33b609a597c4`
- Gate 6K harness: `9d11966a92ca308d4bb84dacc59f47efbb92b6cc`
- pinned TypeRB semantic reference:
  `fa9e0503cc681bcaa691f6f11d2f1e19ca8e6453`
- compiler fixed-point QBE: 658,639 bytes, SHA-256
  `62db3c31527a670c3050051a9fa27bf142b6c5deaab81ef8234104bd467aa95a`
- QBE 1.3 source archive SHA-256:
  `d587905d620dc5e1d2bfa7c2cc642b9b837aa89a3188c6e37b53d756cf66e320`

The recorded
[Gate 6K result](../results/2026-08-30-gate6k-configured-project-darwin-linux-arm64/README.md)
owns the initial fixed-point evidence. Gate 6L does not regenerate or rename
that provenance.

## Release assets

The exact initial experimental tag is `bootstrap-seed-2026-08-30`. Its raw
assets are:

| Asset | Role |
| --- | --- |
| `type-rb-native-bootstrap-root-qbe-v1.ssa` | one-time registered target-neutral root |
| `type-rb-native-bootstrap-darwin-arm64` | previous-Native seed for `darwin-arm64-v0` |
| `type-rb-native-bootstrap-linux-arm64` | previous-Native seed for `linux-arm64-v0` |
| `type-rb-native-bootstrap-manifest-v1.json` | strict target and digest contract |
| `SHA256SUMS` | independent digest index for every release asset except itself |

The manifest has these required top-level members and rejects unknown or
missing members:

```json
{
  "schemaVersion": 1,
  "status": "experimental",
  "releaseTag": "bootstrap-seed-2026-08-30",
  "nativeRevision": "FULL_GIT_SHA",
  "root": {},
  "backend": {},
  "targets": []
}
```

`root` fixes the asset name, `kind`, size, and SHA-256. `backend` fixes QBE
1.3, its source URL, source SHA-256, and the measured built QBE size and digest
for each runner. Each of the two ordered `targets` entries fixes its profile,
OS, architecture, runner image, QBE target, CC boundary, asset, mode, size,
SHA-256, and artifact-attestation subject digest.

The manifest is a release/bootstrap schema owned only by this experimental
repository. It is not a TypeRB compiler API, package format, stable ABI, or
general artifact standard.

## Initial root ceremony

The initial root path is intentionally different from all later ordinary
bootstrap paths:

```text
registered root QBE
    -> pinned QBE 1.3 on target runner
    -> explicit system CC/assembler/linker
    -> platform B1/compiler
    -> B2/compiler
    -> B3/compiler
    -> B4/compiler
```

The root enters a draft GitHub release and is fetched by release asset
identity. Both target jobs require its registered size and digest before QBE
runs. Darwin uses fresh `macos-15`, QBE target `arm64_apple`, and
`darwin-arm64-v0`; Linux uses fresh `ubuntu-24.04-arm`, QBE target `arm64`, and
`linux-arm64-v0`.

Within each job B1, B2, B3, and B4 use the same basename, target runner, QBE,
CC, SDK/system libraries, and linker policy. Their raw bytes must be exact. B4
must re-emit the registered fixed-point QBE, check the canonical compiler
closure, and build and run the configured Gate 6K application.

The setup graph and tool versions are recorded, but the root-built B1 is not
called a previous Native release. Its artifact attestation proves which public
workflow, repository revision, and event produced the platform seed from the
registered root; it does not erase the root's earlier Gate 6K provenance.

## Ordinary previous-Native verification

After publication, fresh target jobs use only the released platform seed:

```text
download B1 + manifest + SHA256SUMS
    -> verify GitHub asset digest
    -> verify SHA-256 manifest
    -> verify GitHub artifact attestation
    -> chmod 0755
    -> B1 builds B2
    -> B2 builds B3
    -> B3 builds B4
```

Go, reference `trb`, recovery artifacts, and the root QBE are absent from this
ordinary graph. The workflow observer and digest tools do not compile TypeRB
source. The Native compiler invokes the explicit QBE and CC paths directly and
must leave no intermediate after success or failure.

## Correctness and measurement

Both initial and post-publication jobs enforce:

- exact B1/B2/B3/B4 bytes and B4 fixed-point QBE;
- compiler-closure and configured-project checking;
- `configured-project-ok` application behavior;
- registered valid, invalid, mutation, tool-failure, atomic-output, and cleanup
  probes;
- Mach-O or ELF architecture and dependency inspection;
- complete command inventory on Darwin and a process trace on Linux; and
- absence of Go, reference, recovery, and shell-mediated compiler children
  from the ordinary chain.

Two warmups and seven observations record each adjacent compiler build's
elapsed time and orchestration-root peak RSS. Adjacent medians must remain
within 25%, and a value above 2x the strongest adjacent median is catastrophic.
The gate expects no application primary-metric improvement; it preserves Gate
6K behavior while adding distribution and trust work.

Each raw platform seed must remain at or below 310,000 bytes, and the two
compiler assets together at or below 620,000 bytes. Reports separately record
the root, compiler assets, manifest, checksums, attestations, QBE source and
binaries, and system-provided toolchain/runtime boundaries. Download and
verification latency is advisory because it includes external services.

## Publication sequence

1. Merge the reviewed decision and plan.
2. Merge the root/previous-seed workflows, manifest validation, harness, and
   permanent tests.
3. Create a draft prerelease and upload only the exact registered root QBE.
4. Run both initial target jobs, review their artifacts and attestations, and
   complete the manifest and checksum set in the draft.
5. Enable repository release immutability, then publish the complete draft.
6. Run fresh post-publication target jobs against the actual release assets.
7. Commit raw evidence and a result review before closing issue #90.

No incomplete draft is described as a distributed seed, and no published
asset is replaced in place.

## Deferred scope

Gate 6L does not define Native SemVer, TypeRB compatibility ranges, stable
target support, signing-key custody, package-manager installation, automatic
tool discovery, bundled QBE or linker, static linking, x86-64, production
support, or a recovery guarantee. It changes nothing in the reference TypeRB
repository.
