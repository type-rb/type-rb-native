# Repository organization and cleanup schedule

## Decision and scope

Accepted maintenance direction, starting at the post-#256 correctness baseline.
Gate numbers identify engineering checkpoints, not permanent implementation
layers. Active directories, source filenames, types, and helper names should
describe their responsibility. This includes `src/gateN_*`, `qbe2.trb`,
`qbe3.trb`, `compiler/gate4/`, and `Gate4`/`gate4_` implementation names.

Cleanup starts during development, not after full MIR migration, Pure Go parity,
or product promotion. It is not a rewrite or permission to remove still-used
recovery and conformance coverage. The initial inventory below is a routing
guide, not a finding that every gate-numbered file is obsolete.

## Current ownership map

| Current area | Role and treatment |
| --- | --- |
| `compiler/gate4/src/compiler.trb`, `storage.trb`, `path.trb` | Ordinary self-hosted compiler closure. Split by responsibility and eventually remove checkpoint-derived names; retain one canonical implementation. |
| `src/gate0.trb`, `snapshot.trb`, `json_boundary.trb`, `diagnostic.trb`, `native_mir.trb` | Initial snapshot validation/MIR boundary and shared support. Classify callers before separating shared code from recovery-only code. |
| `src/gate1_*`, `gate2_*`, `gate3_*`, `qbe.trb`, `qbe2.trb`, `qbe3.trb` | Versioned snapshot, MIR, layout, QBE, and managed-runtime paths with differential tests. These are not three successive unused compiler copies. Name retained paths by format/capability and role. |
| `src/gate4_toolchain.trb`, `matched_go_driver.trb`, `gate6f_compiler_source.trb` and associated tests | Recovery generation, matched reference comparison, and strict compiler-source flattening support. Keep them visibly separate from the ordinary compiler. |
| `src/*_test.trb`, `compiler/gate4/conformance/`, `corpus/` | Active correctness evidence. Relocate with their owners and preserve discovery, negative cases, and coverage. |
| `tools/`, `.github/workflows/`, compatibility and transition metadata | Current consumers of source paths, names, runtime output, and exact identities. Move references atomically with implementation changes. |
| `results/`, dated gate plans and accepted decisions | Historical evidence. Preserve gate labels, recorded commands, hashes, and revisions rather than rewriting history to resemble the current layout. |

In particular, the root project config compiles `src/`, and recovery helpers
validate the compiler's exact imports. The runtime-generation path also feeds
bootstrap tooling. A filename search alone cannot establish dead code.

## Ordered checkpoints

| Checkpoint | Start condition | Deliverable / completion condition |
| --- | --- | --- |
| O1 — Documentation entry points | Now, independently of compiler work | Short root README; historical narrative and reference catalog moved into `docs/`; this schedule linked from development guidance. No code, measurement, or Pages-data change. |
| O2 — Dependency inventory and first support-source cleanup | Immediately after O1, before implementing the pending checked-binary slice #254 | Record every root source file's role, imports/callers, test/CI consumers, proposed destination, and keep/move/retire decision. Then complete one small role-based move/rename of support code with its callers and tests. Start outside the ordinary compiler's hot implementation. |
| O3 — Incremental compiler decomposition | At the next accepted checked-binary ownership checkpoint, or earlier for a demonstrably independent module | Extract the first cohesive checked-program/MIR or compiler-support module with explicit imports and tests. Update recovery derivation in the same change. Continue one responsibility at a time alongside optimization; do not wait for the whole MIR migration to finish. |
| O4 — Active path and symbol naming | As each O2/O3 responsibility is verified | Remove its gate-derived file/type/helper names and update live consumers. Move the ordinary compiler out of `compiler/gate4/` once its entry, recovery, and test references can move together. Do not wait for all source modules to be decomposed. |
| O5 — Retire superseded implementation | When a replacement covers the old path's actual consumers | Delete only proven-unused implementation and compatibility shims after dependency and coverage checks. Preserve useful regression inputs and immutable historical evidence. |

O1 supplied the initial documentation cleanup. O2's
[root source inventory](root-source-inventory.md) covers all 45 source files
and records the first matched-Go driver move under
[issue #258](https://github.com/type-rb/type-rb-native/issues/258). Only that
support module and its test have moved; the other destinations are proposals.
O3–O5 remain planned, not completed.
Before each code slice, register its exact files, baseline, expected generated
identity effects, and acceptance checks in a public issue. If O2 encounters a
correctness or recovery blocker, publish the precise blocker and next repair,
then choose another independent support slice when possible. Do not silently
postpone organization until an unspecified final cleanup phase. Revisit the
next organization slice at every accepted optimization checkpoint.

## Target responsibilities, not a parallel implementation

The intended separation is frontend (lexing, parsing, resolution, checking),
checked-program/Native MIR (model, verifier, analysis, passes), backend adapters,
runtime generation, and compiler driver. Recovery/snapshot adapters and test
support remain distinct from the ordinary compiler path. Final folder names
are selected in the owning move PR; the responsibility map does not prescribe
empty directories or a duplicate compiler to populate later.

Do not merge the snapshot MIR and self-hosted MIR merely because both are named
MIR. Compare semantics, callers, recovery requirements, and verification first.
Shared runtime or utility code must retain one owner where it is genuinely
shared; copy-and-rename is not a completed extraction.

## Verification and evidence preservation

- Keep mechanical relocation separate from optimizer or language changes. New
  active implementation names should be responsibility-based; historical gate
  fixtures and frozen protocols are legitimate exceptions.
- For every move, audit imports, source discovery, entry paths, generators,
  flattening assumptions, tests, CI routing, manifests, live documentation,
  transition-policy validators, and benchmark controllers. Preserve fail-closed
  validation; never weaken marker/digest checks to accommodate a rename.
- Run pinned-reference formatting/checks and root/compiler tests with recovery
  and QBE explicitly enabled. Compiler/runtime/source-closure changes also
  require ordinary fixed points, current target regressions, cross-target QBE,
  process/cleanup/stack checks, and applicable memory/performance authorities.
- Preserve exact application behavior, failures, and generated output for a
  pure organization change. If symbol or module identities necessarily change,
  preregister the exact expected effect and comparison before implementation;
  arbitrary output normalization must not conceal a semantic change. Candidate
  ordinary generations must still reach exact same-basename fixed points.
- Keep all current size/build/RSS and catastrophic bounds. Organization is not
  a new MIR allowance, an optimization claim, or relief from emitter-removal
  obligations. Record build and artifact costs of module extraction.
- Do not modify immutable seeds, release assets, historical measurements, or
  source hashes. Preserve historical links with revision-pinned references or
  a migration map where needed. A gate-labelled evidence record may remain
  permanently even after every active implementation name has changed.

## Documentation maintenance

The root README is an orientation page, not an append-only progress log. Keep
its overview, limits, current architecture, and primary navigation concise;
do not add one paragraph for each merged experiment. Use the capability map
for coverage, the benchmark explorer and dated results for performance, the
MIR status page for active ownership, and issues/decisions for scoped plans.

The historical narrative and documentation catalog now have separate homes.
The development plan and architecture also contain historical detail: after
O1, move duplicated completed-gate narrative to the history/reference layer in
a documentation-only follow-up, retaining normative policy and old anchors or
explicit migration links. Do not trade one oversized README for multiple
competing descriptions of current status.

Documentation-only changes use the existing lightweight documentation CI.
Source moves still run their applicable code authorities; do not misclassify a
move as documentation merely because its intended behavior is unchanged.
