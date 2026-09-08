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
budgets in [Decision 0029](decisions/0029-array-assignment-compiler-budget.md).
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

## Registered conditional-syntax refresh

[Issue #326](https://github.com/type-rb/type-rb-native/issues/326#issuecomment-5574765145)
registers `bootstrap-seed-2026-09-08`. Its implementation source is accepted
`21f507e7ee7de2577f4137f6dfb9f732c14c1640` from PR #329, with reviewed observer
changes applied before preparation. The workflow records the exact main source
and compiler tree used by that invocation. The predecessor is the verified
Sep7 release recorded below; both known refresh tags retain their exact
predecessor validation. Unknown tags and cross-tag manifests fail closed.

Darwin arm64 and Linux arm64 retain the same target, combined-size, generation,
retained-observation, corpus and process bounds. The preparation and actual
published-asset verification both passed, including logical-condition and
`elsif` fixtures. The verified checkout handoff follows.

## Registered loop-transfer refresh

[Issue #334](https://github.com/type-rb/type-rb-native/issues/334#issuecomment-5576325728)
registers the distinct `bootstrap-seed-2026-09-08-loop-transfers` tag from accepted
implementation `4e1d0b4aee97b9a5bd73a98f918b31d47985da25`, with reviewed observer
changes before preparation. Its predecessor is the verified Sep8 release below.
All three registered refresh tags keep their exact predecessor validation.
Preparation, attested publication and fresh actual-asset verification have passed;
the verified checkout handoff is recorded below.

Darwin arm64 and Linux arm64 retain all target, combined-size, corpus, process,
adjacent-generation and retained-observation bounds. The reference pin includes
loop-transfer snapshot support and the corresponding program recovery case.
The separate checkout-pin change follows those checks. Compiler implementation
self-use remains a subsequent verified source change.

## Registered Boolean Array refresh

[Issue #341](https://github.com/type-rb/type-rb-native/issues/341) registers the
new `bootstrap-seed-2026-09-08-boolean-arrays` tag. Its ordinary compiler source
is accepted `57cb41ad6be91716e31fa555ed8ea8c8ce7a5f51` from PR #345, with the
matching snapshot recovery and reviewed preparation observers merged before
preparation. The workflow records its exact accepted main source and compiler
closure. Its predecessor is the verified loop-transfer release below.

Only the new tag registers the approved Decision 0029 manifest budgets:
350,000 Darwin arm64, 328,000 Linux arm64 and 678,000 combined bytes. The three
earlier tags retain their exact previous limits and predecessor validation;
unknown tags and cross-tag identities fail closed. Adjacent-generation ratios,
every retained observation, corpus, process and attestation bounds are unchanged.
Preparation includes the Boolean Array fixtures alongside earlier syntax checks.

Preparation, immutable publication and fresh actual-asset verification have
passed. The verified checkout handoff and its historical Linux amd64 Boolean
source bridge are recorded below. Compiler flag self-use remains a subsequent
verified source change.

## Current verified checkout seed

Checkout builds pin [bootstrap-seed-2026-09-08-boolean-arrays](https://github.com/type-rb/type-rb-native/releases/tag/bootstrap-seed-2026-09-08-boolean-arrays),
an immutable experimental prerelease from accepted source
`e99df93e81c36c765ead99526fe58b2c2a978ced`. Its ordinary compiler implementation
is unchanged from accepted PR #345; PR #346 supplied matching snapshot recovery
and reviewed preparation observers.

- [Preparation and attestations](https://github.com/type-rb/type-rb-native/actions/runs/34218109921) passed both arm64 targets and all 28 retained observations.
- [Fresh published-asset verification](https://github.com/type-rb/type-rb-native/actions/runs/34218869691) passed both targets, including equality of each downloaded seed with B1/B2/B3/B4, the corpus, all 42 retained generation observations and ordinary Linux process boundaries.
- Darwin compiler: 349,256 bytes, SHA-256 `1c8fdd630b3e129b9e121abce34c6d6dbd928b844cbfc1cff5f20a53b6ccaec7` (asset 550345113).
- Linux compiler: 325,872 bytes, SHA-256 `af5549d42390d3ac3ec74c646ddd37c5930b411f706e5cf2dfd4ca7258bb09fd` (asset 550345122).
- Combined: 675,128 bytes, below the registered 678,000-byte bound.
- Manifest: SHA-256 `faf866e10a4b1f3ca45fcf2c85db0efb01fbed9f02f44876ade0b4037f28da92` (asset 550345114).
- Checksum index: SHA-256 `324ce4e05f0a2124431e2405ec12211a423a5e32d70c02146d11ea37b47b275c` (asset 550345115).

The immutable [loop-transfer predecessor](https://github.com/type-rb/type-rb-native/releases/tag/bootstrap-seed-2026-09-08-loop-transfers)
remains at `1d53ed0f5b9471335c913dd9d148ff3b9eb1b483`. Its exact identities and
earlier predecessor history remain in the
[source-era handoff record](https://github.com/type-rb/type-rb-native/blob/e99df93e81c36c765ead99526fe58b2c2a978ced/docs/bootstrap-seed-updates.md#current-verified-checkout-seed).
Its [preparation](https://github.com/type-rb/type-rb-native/actions/runs/34169810365)
and [published verification](https://github.com/type-rb/type-rb-native/actions/runs/34170169680)
remain the authorities for that historical release. Every registered tag keeps
its exact predecessor and size contracts.

Compiler binaries and detailed run artifacts remain outside Git. This compact
handoff record does not introduce another retained benchmark result directory
or claim a runtime speedup.

## Active CI consumers versus historical recovery

Current compiler-cost, worker-memory, formal runtime/build benchmark and Linux
arm64 regression workflows use the exact Boolean Array seed and the shared strict
download/authentication helper. Their manual seed input must match the recorded
source revision; an older or unknown tag fails rather than bypassing provenance.
Changing a setup seed does not move a frozen benchmark baseline or change any
measurement/acceptance bound. Full benchmark jobs remain manually dispatched.

Linux amd64 retains the original immutable root QBE. Its first setup compiler
builds exact accepted source `21f507e7ee7de2577f4137f6dfb9f732c14c1640` and must
accept logical-condition and `elsif` fixtures. That compiler then builds exact
accepted loop-transfer source `4e1d0b4aee97b9a5bd73a98f918b31d47985da25`; the new
bridge must accept the loop-transfer fixture. It then builds exact accepted
Boolean-capable source `57cb41ad6be91716e31fa555ed8ea8c8ce7a5f51` and checks the
Boolean Array fixture before reading **candidate** source. The subsequent
candidate-runtime transition stays separate so a future runtime change still
precedes ordinary B2/B3/B4. These ordinary and measured generations remain the
candidate.

These compatibility bridges are setup-only. Exact clean source revisions and entry digests,
compiler/QBE identities, emission/QBE/link traces and capability-check output
are retained separately. It creates neither a new root asset nor Go recovery.
The arm64 comparison authenticates its verified seed independently. Optional
source arguments accept only their exact registered revisions. The Boolean
source requires both earlier sources; omitted later arguments retain the
earlier setup shapes. Omitting every source argument retains the historical
direct-current-source setup.

Initial publication/release-integrity workflows, retained manifests and earlier
results keep their source-era identities. Refreshing checkout bootstrap alone
does not establish that every historical recovery compiler understands newly
adopted implementation syntax; inspect these consumers before adopting it.
