# Decision 0019: Experimental Bootstrap Seed Distribution

## Status

Accepted for the Gate 6L experiment.

## Context

Gate 6C proved that an existing Native compiler can build the next compiler,
and Gate 6K retained exact Darwin and Linux arm64 B2/B3/B4 fixed points while
building configured projects. Those gates deliberately kept their first seed
in a measurement workspace. A fresh checkout still has no durable previous
Native compiler to fetch, authenticate, and use without rebuilding recovery
artifacts through Go.

Committing platform compiler binaries would make a checkout self-contained,
but it would also place opaque, target-specific artifacts permanently in Git
history. Publishing an ordinary release would imply version, compatibility,
support, and installation contracts that the experiment has not designed.
Release bootstrap therefore needs a narrower experimental distribution and
trust boundary.

## Decision

Gate 6L publishes the first Darwin arm64 and Linux arm64 compiler seeds as raw
assets of a date-labelled GitHub prerelease. The exact initial tag is
`bootstrap-seed-2026-08-30`. It is a bootstrap identifier, not Native SemVer or
a stable compatibility promise. Compiler binaries do not enter Git history.

The release contains two distinct provenance classes:

1. A one-time target-neutral root QBE artifact whose exact size and SHA-256
   were registered by the completed Gate 6K result.
2. Platform compiler seeds built from that root on fresh target runners and
   verified through an exact B1/B2/B3/B4 fixed point.

The root QBE enters a draft release before any platform build. Target jobs
download it by authenticated release-asset identity, require the registered
658,639-byte size and
`62db3c31527a670c3050051a9fa27bf142b6c5deaab81ef8234104bd467aa95a`
digest, translate it with pinned QBE 1.3, and link it through an explicit
system CC. Root translation is setup and recovery provenance; it is not an
ordinary Native release chain.

Each generated compiler asset receives a GitHub artifact attestation. A strict
versioned JSON manifest records the release tag and Native revision, the root
QBE and pinned QBE source identities, and the asset name, target profile,
runner, QBE target, size, and SHA-256 for each platform. `SHA256SUMS` provides a
simple independent digest index. Release asset digests exposed by GitHub are
also recorded and compared.

After every draft asset has been reviewed, repository release immutability is
enabled and the draft is published as a prerelease. A published seed is never
replaced in place. Any correction or later compiler requires a new tag,
manifest, assets, and attestations.

Fresh post-publication jobs must download the actual release assets, verify the
manifest digest and artifact attestation before execution, restore executable
mode, and close the ordinary chain:

```text
previous Native B1 -> current TypeRB compiler source -> B2
B2                 -> current TypeRB compiler source -> B3
B3                 -> current TypeRB compiler source -> B4
```

The ordinary chain installs or executes neither Go nor the reference compiler.
It contains only the Native seed, current TypeRB-owned compiler source, pinned
QBE, explicit system CC/assembler/linker, system libraries, and an observer
that records the process and measurement evidence. The Native compiler still
invokes QBE and CC directly without a shell child.

The platform compiler assets are raw executables rather than archives. This
keeps their bytes equal to the fixed-point outputs and avoids adding an archive
format and metadata normalization policy. The manifest records mode `0755`;
consumers apply it only after digest and attestation verification.

## Consequences

- A fresh checkout can start from a durable previous-Native compiler without
  Go in the ordinary bootstrap path.
- The first root handoff remains auditable rather than being retroactively
  described as an ordinary Native release.
- GitHub, its public attestation infrastructure, and release retention become
  explicit distribution dependencies of this experiment.
- QBE, the system toolchain, SDK or loader, and dynamic libraries remain
  external and are measured or identified; seed publication does not make the
  compiler distribution self-contained.
- Published assets are immutable. Reproducibility is checked within each
  pinned target runner/toolchain; byte equality across different SDK or linker
  revisions is not assumed.
- This decision changes no TypeRB syntax, semantics, reference-compiler API,
  package contract, or reference-repository documentation.
- Stable Native versions, TypeRB compatibility ranges, signing-key custody,
  package-manager installation, target support, and production recovery remain
  deferred.

## Alternatives considered

### Commit compiler seeds to Git

Rejected for the initial distribution. It would make raw checkout bootstrap
simple, but every target update would permanently expand source history and
blur the review boundary between maintained TypeRB source and opaque binaries.

### Publish a stable Native release now

Rejected. Bootstrap durability is the immediate need. Stable versioning,
compatibility, support, and installation policy require separate evidence and
design.

### Rebuild the first seed through Go on every fresh checkout

Rejected as the ordinary path. Go-backed recovery remains useful, but making
it routine would fail the intended previous-Native release/bootstrap boundary.

### Bundle QBE and the system toolchain with the seed

Deferred. The current explicit external boundary is already measured and is
sufficient to test durable Native bootstrap. Bundling introduces independent
licensing, update, security, portability, and distribution-size work.
