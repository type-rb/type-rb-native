# Bootstrap seed updates

A seed is an already-built Native compiler used to build its successor. The
checked-in TypeRB compiler remains the implementation; the seed is neither
generated application code nor a new dependency on Go.

## Keep compatibility current, not the download URL floating

Refresh the seed before compiler implementation source adopts supported syntax
that the pinned seed cannot read, after relevant bootstrap/security fixes, or
at a deliberate stable development checkpoint. Check this boundary when adding
compiler implementation syntax, not only after a fresh checkout fails.

Use the latest **verified, accepted** source at that checkpoint. Do not publish
an unaccepted optimization candidate as a shortcut around its acceptance gates.
Refreshing on every commit is unnecessary: documentation and compatible source
changes do not inherently require a new seed. Expensive publication/verification
jobs remain manually dispatched; ordinary checkout builds always use an exact
immutable tag and digests, never a floating `latest` asset.

## Refresh sequence

The registered refresh is tracked by [issue #320](https://github.com/type-rb/type-rb-native/issues/320).
Preparation tooling alone does not mean that the new release is published or
that checkout pins have switched.

1. Register a new tag, accepted source revision/closure, predecessor identities,
   target matrix and current bounds. Merge the reviewed observer changes first.
2. Dispatch `bootstrap-seed-refresh.yml` on main with `mode=prepare`. It verifies
   predecessor release state, strict manifest, checksums, asset digests and
   source-bound GitHub attestations **before** executing the old compiler.
3. Build setup-only transitions from the previous Native seed. Then verify
   ordinary B2/B3/B4 builds, the complete existing corpus and registered adjacent
   measurement bounds (1.25 for adjacent generation medians, and 2.0 for every
   retained time/RSS/CPU observation against the strongest adjacent median).
   These are seed-generation checks, not the optimizer's 1.05 baseline contract.
   Record each ordinary Linux compiler build with a closed
   process allowlist. Darwin's inventory is boundary-only, not a dynamic trace.
4. Review both target results and paired bounds. Publish the four attested assets
   from that exact successful run as a new immutable experimental prerelease.
   Publication is a separate authorized operation; the preparation workflow
   itself never creates or edits a release.
5. Dispatch `mode=verify` from main. Fresh target jobs check out the release's
   exact source and download its actual published assets. Authenticate before
   execution, rebuild, compare the downloaded seed with the fixed point and
   rerun the corpus/measurement authorities. A failure leaves checkout pins alone.
6. In a separate PR, update checkout tag/digests and tag-scoped cache identity,
   run fresh core/CLI bootstrap on both targets, and update this status. Only
   then use the new syntax in compiler implementation source.

The v2 manifest records the predecessor tag/revision/manifest and target digests,
the source revision, QBE source/build identities and target compiler identities.
Unknown fields, altered identities, duplicate keys, invalid sizes, changed asset
sets, mutable/draft releases and incorrect checksum indexes fail closed.
Attestations bind compilers, manifest and checksums to the preparation workflow,
exact main revision and hosted runners. Manifest validation alone is not an
attestation check.

The first refresh keeps accepted compiler caps of 350,000 bytes on Darwin arm64,
317,000 on Linux arm64 and 667,000 combined. It changes no ordinary optimizer
acceptance limit, measurement baseline or runtime performance claim. The legacy
initial-root manifest/verifier and its historical bounds remain unchanged.

## Retention and failure handling

Keep published tags/assets/attestations immutable and retain the initial root's
provenance. Later ordinary refreshes do not create another root QBE or invoke
the reference compiler. Historical release-integrity jobs keep their source-era
pins. An old target-recovery consumer is not silently repointed to a new release.

Compiler binaries stay outside Git. Retain compact accepted release identities
and durable verification links; temporary workflow packages/logs expire normally.
Never replace a published asset, retry until a favorable measurement hides an
earlier failure, or switch the default pin before post-publication verification.
