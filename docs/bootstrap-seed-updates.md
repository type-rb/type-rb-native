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

## Registered conditional-syntax refresh

[Issue #326](https://github.com/type-rb/type-rb-native/issues/326#issuecomment-5574765145)
registers `bootstrap-seed-2026-09-08`. Its implementation source is accepted
`21f507e7ee7de2577f4137f6dfb9f732c14c1640` from PR #329, with reviewed observer
changes applied before preparation. The workflow records the exact main source
and compiler tree used by that invocation. The predecessor is the verified
Sep7 release recorded below; both known refresh tags retain their exact
predecessor validation. Unknown tags and cross-tag manifests fail closed.

Darwin arm64 and Linux arm64 retain the same target, combined-size, generation,
retained-observation, corpus and process bounds. The preparation verifies the
logical-condition and `elsif` fixtures. Publication, fresh published-asset
verification and a separate checkout pin PR are still required. No Sep8 seed
is claimed published or verified by these preparation changes.

## Current verified checkout seed

Checkout builds pin [bootstrap-seed-2026-09-07](https://github.com/type-rb/type-rb-native/releases/tag/bootstrap-seed-2026-09-07),
an immutable experimental prerelease from accepted source
`1f7e8a110bbb2b13f0609709deb6fc8f09dc8b44`. The compiler tree is unchanged from
accepted `26bb32a3d3bd085fdae4fc190bf2a14703351a8f`; no pending optimization
candidate was included. The predecessor remains immutable and unchanged.

- [Preparation and attestations](https://github.com/type-rb/type-rb-native/actions/runs/34113420518) passed both arm64 targets.
- [Fresh published-asset verification](https://github.com/type-rb/type-rb-native/actions/runs/34113836522) passed both targets, including equality of each downloaded seed with its regenerated fixed point, corpus, all retained generation observations and ordinary Linux process boundaries.
- Darwin compiler: 332,728 bytes, SHA-256 `b960d8720ad6bb256fb019d04cd6ab80e86870228bed16776bba9fbe78f5769f` (asset 548637192).
- Linux compiler: 307,544 bytes, SHA-256 `ff3bc9a2409e91eba0e2ef5109bf72a10aa16d4f360bc32aceafc50baa96a580` (asset 548637194).
- Combined: 640,272 bytes, below the unchanged 667,000-byte bound.
- Manifest: SHA-256 `330e59e08bb1173b5865e782a7c578a556942ba5174422434cc56ab4fedfeed5` (asset 548637191).
- Checksum index: SHA-256 `a36b347714285cc4e80597987c2863b7595e5e72a7b082f4787a628c49d194fe` (asset 548637193).

The [first preparation](https://github.com/type-rb/type-rb-native/actions/runs/34111463383)
passed Darwin but stopped Linux at its second setup transition, before ordinary
measurements: the observer mislabeled that compatibility build `ordinary`.
[PR #322](https://github.com/type-rb/type-rb-native/pull/322) corrected the role to
match the existing worker authority; it did not relax ordinary LLD or numerical
requirements. No release was produced from the failed paired run.

Compiler binaries and detailed run artifacts remain outside Git. This compact
handoff record does not introduce another retained benchmark result directory
or claim a runtime speedup.

## Active CI consumers versus historical recovery

Current compiler-cost, worker-memory, formal runtime/build benchmark and Linux
arm64 regression workflows use the exact Sep7 seed and the shared strict
download/authentication helper. Their manual seed input must match the recorded
source revision; an older or unknown tag fails rather than bypassing provenance.
Changing a setup seed does not move a frozen benchmark baseline or change any
measurement/acceptance bound. Full benchmark jobs remain manually dispatched.

Linux amd64 retains the original immutable root QBE. Before reading candidate
syntax, its setup compiler builds the exact clean accepted source revision
`21f507e7ee7de2577f4137f6dfb9f732c14c1640`. That generated compiler must accept
the logical-condition and `elsif` conformance fixtures, then reads the
**candidate** source for the current-runtime transition. Ordinary B2/B3/B4 and measured inputs remain
the candidate. The setup source revision/entry digest and all existing process
traces are retained separately. No new root asset or Go recovery is introduced.
The arm64 comparison still authenticates the Sep7 seed independently of this
amd64 setup-source revision. The optional setup-source argument accepts only
the exact clean setup revision; omission retains the historical direct-current-source setup shape.

Initial publication/release-integrity workflows, retained manifests and earlier
results keep their source-era identities. Refreshing checkout bootstrap alone
does not establish that every historical recovery compiler understands newly
adopted implementation syntax; inspect these consumers before adopting it.
