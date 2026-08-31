# Decision 0026: Separate Recovered Target Chains from Seed Assets

## Status

Accepted for experimental development.

## Context

The immutable `bootstrap-seed-2026-08-30` release contains Darwin arm64 and
Linux arm64 compiler executables plus one target-neutral root QBE asset. Gate
6N uses that root QBE to recover and close a current Linux amd64 compiler chain;
the release does not and cannot retroactively contain an amd64 executable.

Compatibility schema version 1 required the current target list to be exactly
the target list in the immutable seed manifest. Keeping that rule would either
omit a fully verified current target or falsely describe an amd64 seed asset.
Both outcomes collapse two different facts: which executable assets a release
contains, and which target chains the current source has independently closed.

## Decision

Compatibility schema version 2 keeps seed and current target identity
separate:

- the immutable seed manifest remains the source of truth for executable seed
  assets and is never rewritten or reclassified;
- `targets` describes the exact current experimental target profiles;
- the seed manifest's targets remain an exact ordered prefix of the current
  target list;
- every additional target requires one exact `evidence.targetChains` entry
  with the same profile, measured Native revision, retained result, and
  successful workflow run; and
- target-chain evidence must exactly cover the additional targets, with no
  missing, duplicate, reordered, or unrelated profile.

Repository validation also requires every current profile and QBE target in
the self-hosted compiler source and every profile-to-OS, architecture, and QBE
mapping in the bootstrap tooling. A result file must contain the profile,
Native revision, and workflow identity declared by its target-chain evidence.

The first recovered target is `linux-amd64-v0`, measured at
`f7e6b02b38c77d0ea6f7da210e91575a4fa1cdf9` in
[Gate 6N](../../results/2026-08-31-gate6n-linux-amd64/README.md).

## Consequences

- Current compatibility metadata can describe a target recovered from a
  target-neutral root without inventing an executable in an older release.
- Seed provenance and current target verification remain independently
  auditable.
- Adding another recovered target requires fresh exact evidence rather than
  only a new manifest row.
- The new row remains experimental; it does not declare support, freeze the
  profile, or publish a distribution asset.
- The Native version and exact TypeRB compatibility identity remain separate
  from this target-evidence change.

## Alternatives considered

### Add amd64 to the old seed manifest

Rejected because the release is immutable and has no amd64 compiler asset.

### Omit amd64 from current compatibility metadata

Rejected because it would leave the machine-readable current target list
behind the exact reviewed result.

### Replace the seed with a new release immediately

Rejected because the verified root-QBE recovery already closes the current
chain. A new seed is justified by a concrete distribution need, not by
metadata convenience.

### Allow arbitrary extra target rows

Rejected because a compiler source mapping alone is weaker than an exact
fixed-point, correctness, process, target, and measurement result.
