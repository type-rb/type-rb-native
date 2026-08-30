# Decision 0020: Independent Native Versioning and Exact TypeRB Compatibility

## Status

Accepted for experimental development.

## Context

TypeRB Native has a durable previous-Native seed and an ordinary Go-free
bootstrap path. It has also revalidated the current TypeRB-authored compiler
against an exact TypeRB `0.4.3-dev` reference revision on Darwin and Linux
arm64. The implementation, runtime, target profiles, and distribution can
change without a TypeRB language release, while TypeRB syntax or semantics can
advance without requiring the same Native implementation version.

One shared or compound version would collapse source compatibility, compiler
protocol, bootstrap format, Native MIR, runtime ABI, target ABI, external
backend, and artifact identity into a value that cannot state which boundary
was actually verified. A documentation-only table would also let tooling
silently drift from repository constants.

## Decision

TypeRB Native uses independent SemVer beginning at `0.1.0-dev`. Major version
zero denotes experimental development; this decision does not establish a
stable release or support promise.

The implementation version is stored in `NATIVE_VERSION`. TypeRB compatibility
is declared separately in strict versioned JSON. Schema version 1 permits only
one exact TypeRB version and full Git revision. It has no range syntax.

The record separates compiler protocol, bootstrap snapshot and seed formats,
Native MIR, runtime ABI, backend, target profiles, and evidence. Unversioned
internal surfaces use an explicit unstable status and `null` version instead
of an invented compatibility promise. CI rejects duplicate, unknown, missing,
or inconsistent members and checks repository-owned identities plus the
pinned reference compiler's reported version.

The tracked record does not contain its own source revision. Immutable release
metadata adds the exact Git revision, manifest digest, artifact and sidecar
checksums, target toolchain identity, and attestations. Released artifacts and
bootstrap seeds are never overwritten.

A TypeRB advance requires a new exact pin and evidence, but does not copy its
version into Native SemVer. A distributed Native compatibility change receives
an independently chosen Native bump. Compatibility ranges, stable CLI output,
package-manager installation, long-term support, and deprecation guarantees
require later decisions.

## Consequences

- Users and tooling can distinguish the Native implementation identity from
  the exact TypeRB semantics it has demonstrated.
- No unsupported TypeRB revision is inferred from a nearby version number.
- MIR, runtime ABI, target, bootstrap, and backend changes remain visible
  instead of being hidden inside Native SemVer.
- Development metadata is useful before a stable release without converting
  the experimental bootstrap seed into a supported distribution.
- A release process must combine the tracked compatibility record with
  immutable source and artifact identity; the tracked file alone is not an
  artifact attestation.
- Go and the reference compiler remain differential and CI inputs, not
  ordinary Native release or bootstrap dependencies.

## Alternatives considered

### Reuse the TypeRB version

Rejected because TypeRB language releases and Native implementation releases
have independent triggers and evidence.

### Use one compound version

Rejected because it is difficult to order and cannot accurately represent
independent protocol, runtime, target, backend, and artifact boundaries.

### Keep only a documentation table

Rejected because CI and future release tooling need strict data that fails on
drift rather than a convention that can become stale silently.

### Declare a TypeRB version range now

Rejected. Only exact `0.4.3-dev` evidence exists for the current record. A
range would imply unmeasured support at its boundaries.
