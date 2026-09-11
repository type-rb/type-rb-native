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

## Registered record Array refresh

[Issue #349](https://github.com/type-rb/type-rb-native/issues/349#issuecomment-5588804137)
activated `bootstrap-seed-2026-09-09-record-arrays` from accepted source
`db48f64f6c3f6ce3fb904b2d28c95fa46522ebfc`. Ordinary record Arrays were accepted
at `566d00d67172460df0f57dff6d5fe03db3b67cdc` through PR #352; matching snapshot
recovery and reviewed observers followed in PR #355. Both source-era failed
hosted cost cohorts and their separate bounded confirmations remain recorded.
The compiler source is unchanged between those two accepted implementations.

The predecessor is the immutable Boolean Array release. Only the new tag uses
Decision 0030 manifest ceilings: 366,000 Darwin arm64, 328,000 Linux arm64 and
694,000 combined bytes. All four earlier refreshes retain their own predecessor
and size contracts. Unknown tags and cross-tag provenance fail closed.
Adjacent-generation ratios, every retained observation, the complete corpus,
process allowlists, attestations and immutable-release requirements are unchanged.
The syntax checks include record Array values, RHS effects, managed lifetimes
and the recursive ordinary recovery fixture.

Preparation, attested immutable publication and fresh actual-asset verification
passed. The checkout handoff below precedes compiler-source adoption of record
Arrays. The five-field MIR value carrier is the bounded subsequent self-use slice;
no runtime speedup or benchmark-value change is claimed here.

## Registered Hash refresh

[Issue #403](https://github.com/type-rb/type-rb-native/issues/403) registers
`bootstrap-seed-2026-09-10-hash` from the accepted compiler closure at
`8a6d9ff73b14a97bca1b010ddaad6a38972b5373` (PR #401). Reviewed preparation
observers precede dispatch; the run records its exact main revision and closure.
The predecessor is the verified record Array release recorded in the history below. Only the new tag
uses Decision 0033 manifest ceilings: 400,000 Darwin arm64, 370,000 Linux arm64
and 770,000 combined bytes. Every historical release retains its identities
and source-era bounds. Generation, retained-observation, corpus, process and
attestation checks remain unchanged; preparation checks ordinary Hash fixtures.

Preparation, immutable publication and fresh actual-asset verification passed.
PR #405 supplies the separate checkout pin handoff, matching snapshot recovery
and the accepted-source Linux amd64 setup bridge. Compiler Hash self-use follows
this prerequisite; no compiler/application speedup is claimed by the handoff.

## Registered Array iteration refresh

[The accepted-source registration](https://github.com/type-rb/type-rb-native/issues/410#issuecomment-5638961656)
activates `bootstrap-seed-2026-09-11-array-iteration` from accepted implementation
`508f721f8964d67a5893e547d2e2fb3de5b20a63` (PR #418). Its compiler tree is
`2c5449437f0b1b216bdc9aa810c00804a1f76cae`: 17 canonical modules, 455,536 source
bytes and 12,762 lines. Compiler entry SHA-256 is
`5fce7c0bbd795a49a903dbb65260736749c7c4833e7cc76c86df5dcc364d6f8c`.

PR #423 adds matching snapshot recovery and reviewed observers at
`d2980f14d1b64e5ce3544dd7133e7f5871644e4e`, with the identical compiler tree.
Both [ordinary acceptance](https://github.com/type-rb/type-rb-native/actions/runs/34630185576)
and [recovery integration](https://github.com/type-rb/type-rb-native/actions/runs/34630338541)
passed all 17 authorities before merging to main. Preparation retains the exact
immutable Hash predecessor below and adds the three ordinary Array probes.
The run records the exact accepted main source/observer revision it uses.
Registration and observer acceptance do not mean a seed has been published.

Only this new tag uses the complete-compiler ceilings from Decision 0035:
417,000 Darwin arm64 bytes, 388,000 Linux arm64 bytes and 805,000 combined.
All earlier tags retain their exact predecessor identities and size contracts.
Adjacent-generation, retained-observation, corpus, process, attestation and
immutable-publication checks remain unchanged. Decisions 0036 and 0039 have
failed, exhausted feature/control cohorts; neither changes seed-generation bounds.

Preparation, separate attested immutable publication and fresh actual-asset
verification passed. The verified checkout handoff below updates current
consumers and the accepted-source Linux amd64 bridge. Compiler-source self-use
is a subsequent verified source change.

## Current verified checkout seed

Checkout builds pin [bootstrap-seed-2026-09-11-array-iteration](https://github.com/type-rb/type-rb-native/releases/tag/bootstrap-seed-2026-09-11-array-iteration),
an immutable experimental prerelease from accepted source
`b4a1b383e5678907649334203f534ae62fa42af6`. Its compiler source tree is
`2c5449437f0b1b216bdc9aa810c00804a1f76cae`, unchanged from accepted PR #418;
PR #423 supplied matching recovery and reviewed preparation observers, and
PR #430 recorded the accepted source handoff.

- [Preparation and attestations](https://github.com/type-rb/type-rb-native/actions/runs/34634652111) passed both arm64 targets and all 28 retained observations. All four original assets were authenticated against the exact source and hosted preparation workflow before publication.
- [Fresh published-asset verification](https://github.com/type-rb/type-rb-native/actions/runs/34635238685) passed both targets, including equality of each downloaded seed with B1/B2/B3/B4, the complete corpus, all 42 retained generation observations and ordinary Linux process boundaries. Darwin retains its explicit boundary-only inventory.
- Darwin compiler: 415,480 bytes, SHA-256 `7ba29a5897782366569be9b2be3461f59fcf3e8feccfe41694ae4a29c457d19a` (asset 557804544).
- Linux compiler: 387,984 bytes, SHA-256 `8c9d2ea099880ebbce4f4e91230b1cfab40e3fce4c145adacba36718ddbc5852` (asset 557804541).
- Combined: 803,464 bytes, below the registered 805,000-byte bound.
- Manifest: SHA-256 `3e3c71b9921a81d58224e67833957dcd281840dd80204cb114f54700332b39b0` (asset 557804540).
- Checksum index: SHA-256 `fdf1d868b8827934d0011fd765026fb173b7ec459bb000b5939721d36bd5e956` (asset 557804542).

The immutable [Hash predecessor](https://github.com/type-rb/type-rb-native/releases/tag/bootstrap-seed-2026-09-10-hash)
remains at `79f699e9245f79131646ebf43207f6b7526c4f68`. Its exact identities,
preparation/verification runs and earlier predecessor history remain in the
[source-era handoff record](https://github.com/type-rb/type-rb-native/blob/b4a1b383e5678907649334203f534ae62fa42af6/docs/bootstrap-seed-updates.md#current-verified-checkout-seed).
Every historical tag retains its exact predecessor and size contracts.

Compiler binaries and detailed run artifacts remain outside Git. This compact
handoff record does not introduce another retained benchmark result directory
or claim a runtime speedup.

## Active CI consumers versus historical recovery

Current compiler-cost, worker-memory, formal runtime/build benchmark, daily/weekly
performance and Linux arm64 regression workflows use the exact Array iteration
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
transfer and managed-value fixtures before reading **candidate** source. The subsequent
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
