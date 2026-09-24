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
an unaccepted optimization candidate as a shortcut around its acceptance checks.
Refreshing on every commit is unnecessary: documentation and compatible source
changes do not inherently require a new seed. Expensive publication/verification
jobs remain manually dispatched; ordinary checkout builds always use an exact
immutable tag and digests, never a floating `latest` asset.

## Refresh sequence

The registered refresh is tracked by [issue #320](https://github.com/type-rb/type-rb-native/issues/320).
Preparation tooling alone does not mean that a release is published or that
checkout pins have switched. The current accepted handoff is recorded below.

1. Register a new tag, accepted source revision/closure, predecessor identities,
   target matrix and current bounds. Merge the reviewed observer changes first.
2. Dispatch `bootstrap-seed-refresh.yml` on main with `mode=prepare`. It verifies
   predecessor release state, strict manifest, checksums, asset digests and
   source-bound GitHub attestations **before** executing the old compiler.
3. Build two setup-only transitions from the previous Native seed, matching the
   existing worker-memory authority: the first generated compiler still carries
   the predecessor runtime. Both transitions permit the registered system linker;
   they remain process-traced and outside ordinary measurements. Then verify
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

The three earlier published refreshes retain their source-era manifest caps of
350,000 bytes on Darwin arm64, 317,000 on Linux arm64 and 667,000 combined.
Current-source ordinary compiler validation uses the revised complete-compiler
budgets in [Decision 0029](decisions/0029-array-assignment-compiler-budget.md)
and [Decision 0030](decisions/0030-record-array-compiler-budget.md).
A future refresh must register its own exact source and manifest limits; this
decision does not republish a seed or alter historical release verification.
Refreshes change no ordinary relative limit, measurement baseline or runtime
performance claim. The legacy initial-root verifier remains unchanged.

## Retention and failure handling

Keep published tags/assets/attestations immutable and retain the initial root's
provenance. Later ordinary refreshes do not create another root QBE or invoke
the reference compiler. Historical release-integrity jobs keep their source-era
pins. An old target-recovery consumer is not silently repointed to a new release.

Compiler binaries stay outside Git. Retain compact accepted release identities
and durable verification links; temporary workflow packages/logs expire normally.
Never replace a published asset, retry until a favorable measurement hides an
earlier failure, or switch the default pin before post-publication verification.

## Earlier verified refreshes

Earlier registrations, preparation results, predecessor identities and exact
source-era limits remain in the [immutable handoff history](https://github.com/type-rb/type-rb-native/blob/f864151fa53a99a9491ca0268198d5ec914124fd/docs/bootstrap-seed-updates.md#registered-conditional-syntax-refresh).
The release manifests and verification runs remain the authority for each tag.
The current checkout handoff and refresh procedure are below and above.

## Current verified checkout seed

Checkout builds pin [bootstrap-seed-2026-09-12-compiler-names](https://github.com/type-rb/type-rb-native/releases/tag/bootstrap-seed-2026-09-12-compiler-names),
an immutable experimental prerelease from accepted source
`d7ffb9384229125216696a220c7f370422472178`. Its compiler source tree is
`4fc8da9eedafadda9dce7fb80357d8db2594b382` from PR #442.

- [Preparation and attestations](https://github.com/type-rb/type-rb-native/actions/runs/34694042015) passed both arm64 targets and all 28 retained observations. All four assets were authenticated against the exact source and hosted preparation workflow before publication.
- [Fresh published-asset verification](https://github.com/type-rb/type-rb-native/actions/runs/34694464071) passed both targets, including equality of each downloaded seed with B1/B2/B3/B4, the complete corpus, all 42 retained generation observations and ordinary Linux process boundaries. Darwin retains its explicit boundary-only inventory.
- Darwin compiler: 432,008 bytes, SHA-256 `28d1b5a3aa42013ea8876173dbf760f7e71ee221a69bf16c915e485ccf60bdd9` (asset 559250651).
- Linux compiler: 394,352 bytes, SHA-256 `40cf35282750792c60dee1efdbdf331681ee7b5dd7efb5fae7a551824db4221c` (asset 559250648).
- Combined: 826,360 bytes. These are authenticated MIR migration observations, not a passing historical size comparison.
- Manifest: SHA-256 `04a0242b06818641e72d65ccbe4ece79380d875768772e60500fa36f05559c83` (asset 559250654).
- Checksum index: SHA-256 `fb66a448d3aaf1f590c7495fa456f1ed68013990367b06ff0adab04530f3267e` (asset 559250647).

The immutable [Array-iteration predecessor](https://github.com/type-rb/type-rb-native/releases/tag/bootstrap-seed-2026-09-11-array-iteration)
remains at `b4a1b383e5678907649334203f534ae62fa42af6`. Its exact identities,
preparation/verification runs and earlier predecessor history remain in the
[source-era handoff record](https://github.com/type-rb/type-rb-native/blob/d7ffb9384229125216696a220c7f370422472178/docs/bootstrap-seed-updates.md#current-verified-checkout-seed).
Every historical tag retains its exact predecessor and size contracts.

Compiler binaries and detailed run artifacts remain outside Git. This compact
handoff record does not introduce another retained benchmark result directory
or claim a runtime speedup.

## Active CI consumers versus historical recovery

Current compiler-cost, worker-memory, formal runtime/build benchmark, daily/weekly
performance and Linux arm64 regression workflows use the exact compiler-name
seed and the shared strict download/authentication helper. Their manual seed input must match the recorded
source revision; an older or unknown tag fails rather than bypassing provenance.
Changing a setup seed does not move a frozen benchmark baseline or change any
measurement/acceptance bound. Full benchmark jobs remain manually dispatched.

Linux amd64 retains the original immutable root QBE. Its first setup compiler
builds exact accepted source `21f507e7ee7de2577f4137f6dfb9f732c14c1640` and must
accept logical-condition and `elsif` fixtures. That compiler then builds exact
accepted loop-transfer source `4e1d0b4aee97b9a5bd73a98f918b31d47985da25`; the new
bridge must accept the loop-transfer fixture. It then builds exact accepted
Boolean-capable source `57cb41ad6be91716e31fa555ed8ea8c8ce7a5f51` and checks the
Boolean Array fixture. It then builds exact accepted record-capable source
`566d00d67172460df0f57dff6d5fe03db3b67cdc` and checks the record Array fixture. It then builds accepted Hash source
`8a6d9ff73b14a97bca1b010ddaad6a38972b5373` and checks the Hash fixture.
It next builds accepted Array iteration source
`508f721f8964d67a5893e547d2e2fb3de5b20a63` and checks live iteration, control
transfer and managed-value fixtures. It then builds the accepted compiler-name
bridge `6ca79d22cde2ddba5fe836c66899b6e08a6511dc`, verifies its exact entry digest,
and checks the **candidate** source with that bridge. Only this setup transition
retains the predecessor declaration spellings. The subsequent
candidate-runtime transition stays separate so a future runtime change still
precedes ordinary B2/B3/B4. These ordinary and measured generations remain the
candidate.

These compatibility bridges are setup-only. Exact clean source revisions and entry digests,
compiler/QBE identities, emission/QBE/link traces and capability-check output
are retained separately. It creates neither a new root asset nor Go recovery.
The arm64 comparison authenticates its verified seed independently. Optional
source arguments accept only their exact registered revisions. The Boolean
source requires both earlier sources, the record source requires all three,
the Hash source requires all four, and the Array iteration source requires all
five; omitted later arguments retain the earlier setup shapes. Omitting every source argument retains the historical
direct-current-source setup.

Initial publication/release-integrity workflows, retained manifests and earlier
results keep their source-era identities. Refreshing checkout bootstrap alone
does not establish that every historical recovery compiler understands newly
adopted implementation syntax; inspect these consumers before adopting it.
