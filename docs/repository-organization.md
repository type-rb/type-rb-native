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
| `compiler/src/compiler.trb` and its storage/path/MIR/literal/state/parser/resolution/checked-program/QBE-output/runtime imports | Ordinary self-hosted compiler closure. Shared state/indexes, syntax, resolution, typed checking/MIR construction, MIR model/verifier/passes, QBE output and runtime generation have distinct owners; continue splitting adapter and driver responsibilities and remove checkpoint-derived names incrementally. |
| `src/gate0.trb`, `snapshot.trb`, `json_boundary.trb`, `diagnostic.trb`, `native_mir.trb` | Initial snapshot validation/MIR boundary and shared support. Classify callers before separating shared code from recovery-only code. |
| `src/gate1_*`, `gate2_*`, `gate3_*`, `qbe.trb`, `qbe2.trb`, `qbe3.trb` | Versioned snapshot, MIR, layout, QBE, and managed-runtime paths with differential tests. These are not three successive unused compiler copies. Name retained paths by format/capability and role. |
| `src/recovery_generation.trb`, `matched_go_driver.trb`, `compiler_recovery_source.trb` and associated tests | Recovery generation, matched reference comparison, and strict compiler-source flattening support. Keep them visibly separate from the ordinary compiler. |
| `src/*_test.trb`, `compiler/conformance/`, `corpus/` | Active correctness evidence. Relocate with their owners and preserve discovery, negative cases, and coverage. |
| `tools/`, `.github/workflows/`, compatibility and transition metadata | Current consumers of source paths, names, runtime output, and exact identities. Move references atomically with implementation changes. |
| `results/`, dated gate plans and accepted decisions | Historical evidence. Preserve gate labels, recorded commands, hashes, and revisions rather than rewriting history to resemble the current layout. |

In particular, `trbconfig.reference.jsonc` selects root `src/`, and recovery
helpers validate the compiler's exact imports. The runtime-generation path also feeds
bootstrap tooling. A filename search alone cannot establish dead code.

## Active consolidation cadence

The [MIR consolidation milestone](mir-consolidation.md) supersedes the old
per-slice scheduling below. Combine connected ownership moves and retire their
superseded code within cohesive PRs. Keep recovery/consumer updates atomic, but
do not require an independent full performance cohort for each helper or module.
Historical checkpoints below explain completed work, not mandatory work sizing.

## Ordered checkpoints

| Checkpoint | Start condition | Deliverable / completion condition |
| --- | --- | --- |
| O1 — Documentation entry points | Now, independently of compiler work | Short root README; historical narrative and reference catalog moved into `docs/`; this schedule linked from development guidance. No code, measurement, or Pages-data change. |
| O2 — Dependency inventory and first support-source cleanup | Immediately after O1, before implementing the pending checked-binary slice #254 | Record every root source file's role, imports/callers, test/CI consumers, proposed destination, and keep/move/retire decision. Then complete one small role-based move/rename of support code with its callers and tests. Start outside the ordinary compiler's hot implementation. |
| O3 — Incremental compiler decomposition | At the next accepted checked-binary ownership checkpoint, or earlier for a demonstrably independent module | Extract the first cohesive checked-program/MIR or compiler-support module with explicit imports and tests. Update recovery derivation in the same change. Continue one responsibility at a time alongside optimization; do not wait for the whole MIR migration to finish. |
| O4 — Active path and symbol naming | As each O2/O3 responsibility is verified | Remove its gate-derived file/type/helper names and update live consumers. Move the ordinary compiler out of `compiler/gate4/` once its entry, recovery, and test references can move together. Do not wait for all source modules to be decomposed. |
| O5 — Retire superseded implementation | When a replacement covers the old path's actual consumers | Delete only proven-unused implementation and compatibility shims after dependency and coverage checks. Preserve useful regression inputs and immutable historical evidence. |

O1 supplied the initial documentation cleanup. O2's
[root source inventory](root-source-inventory.md) covers all 54 source files
and records the first matched-Go driver move under
[issue #258](https://github.com/type-rb/type-rb-native/issues/258). The subsequent
[recovery naming slice](https://github.com/type-rb/type-rb-native/issues/272)
moves four source/test paths to `compiler_recovery_source{,_test}.trb`,
`recovery_generation.trb`, and `compiler_recovery_test.trb`, and replaces their
gate-derived implementation helpers. Its path map distinguishes the retained
measurement protocols from active implementation names. The next [heap-free aggregate layout slice](https://github.com/type-rb/type-rb-native/issues/279)
moves `gate2_layout{,_test}.trb` to `aggregate_layout{,_test}.trb` and replaces
its owned symbols, with exact diagnostic and generated-output preservation.
Other root destinations remain proposals rather than completed moves.
The first O3 slice, registered in
[issue #262](https://github.com/type-rb/type-rb-native/issues/262), extracts the
ordinary compiler's MIR model, verifier, and target-independent passes into
`mir.trb`. Six shared numeric helpers live in `literals.trb`, avoiding a
compiler/MIR import cycle and duplicate semantic predicates. The entry shrinks
from 9,965 to 8,546 lines; the remaining size is still a decomposition target,
not a maintainability goal. Eleven pure tests move with their owners while
frontend/adapter integration tests remain at the entry. Runtime intrinsics
stay at the entry boundary. Recovery validates the exact entry and MIR imports,
then derives storage/path/literals/MIR/entry declarations deterministically;
ordinary self-hosting still uses the canonical file-root closure.

The accepted O3 slice in [PR #268](https://github.com/type-rb/type-rb-native/pull/268)
moves shared compiler state, symbol/name indexes and diagnostics to `state.trb`,
and syntax parsing, cursor primitives and operator mapping to `parser.trb`.
The entry decreases from 8,550 to 7,485 lines. Their dependencies do not point
back to the entry; lexer source slicing and the first five runtime intrinsics
stay there. Focused state/parser tests have their own modules, while full
frontend/adapter integration remains separate. Recovery validates all imported
boundaries and derives storage/path/literals/MIR/state/parser/entry in that order.

The subsequent [semantic frontend slice](https://github.com/type-rb/type-rb-native/issues/269)
extracts declaration/import/type resolution to `resolution.trb` and typed
checking/MIR construction to `checked_program.trb`. Shared locals move into
state and Integer spelling into literals. The entry decreases from 7,485 to
4,723 lines; the two new modules have 858 and 1,827 lines and no entry dependency.
Pure block-row and checked-plan tests move with their owner. Per-function and
whole-program check orchestration remain at the entry to preserve the exact
temporary-storage intrinsic/lifetime boundary. Nine-module recovery adds
resolution/checked-program before entry, with all strict prefixes and tests.

The QBE boundary in [issue #284](https://github.com/type-rb/type-rb-native/issues/284)
moves the output record/four helpers to `qbe_output.trb` and eight runtime
generation/selection helpers to `qbe_runtime.trb`. Their implementation names
describe their responsibility, without an entry dependency or compatibility
aliases. All quoted runtime QBE and declaration logic remain unchanged.
The entry decreases from 4,724 to 4,577 lines and from 196,720 to 142,907 bytes;
the large runtime literals now have a separate owner. Strict eleven-module
recovery includes missing/malformed/mutated-module tests and the current CI
source-copy boundary. Typed compiler-runtime intrinsics remain at the entry.

The project configuration slice in
[issue #293](https://github.com/type-rb/type-rb-native/issues/293) moves two
records and sixteen parsing/validation helpers into `project_config.trb`, with
five focused tests in `project_config_test.trb`. These declarations have
responsibility-based names and no dependency on the compiler entry. The driver,
experimental CLI and REPL import the parser directly, without aliases. Sixteen
lexer calls to the former configuration cursor helper now use the already
imported parser unit-advance helper; its operation is identical for those
unit-step calls. Configuration keeps its variable-step cursor helper.
The entry decreases from 4,606 to 3,830 lines. Strict twelve-module recovery
includes the new owner in source copies, missing/malformed boundaries and
observable source-mutation coverage. This is organization, not a runtime
optimization or completion of frontend decomposition.

The [statement-parser naming slice](https://github.com/type-rb/type-rb-native/issues/326#issuecomment-5575420238)
following ordinary `elsif` self-use replaces
four parser-owned helpers: `gate4_parse_block_syntax` becomes
`parse_statement_block`, `gate4_parse_declaration_syntax` becomes
`parse_declaration_statement`, `gate4_parse_simple_statement_syntax` becomes
`parse_simple_statement`, and `gate4_finish_statement` becomes `finish_statement`.
The parser, entry/checker callers and exact recovery import prefixes move
together, without aliases. Existing application QBE and diagnostics remain
unchanged; compiler source/symbol identities can change and retain all ordinary
fixed-point, recovery, target, memory and cost checks. Other parser helpers and
shared state types remain separate O4 work.

The subsequent [parser loop self-use](https://github.com/type-rb/type-rb-native/issues/334#issuecomment-5576987963)
replaces the completion flag and its four assignments in `parse_statement_block`
with ordinary `break` exits. This uses the verified loop-transfer seed and
matching snapshot recovery support. The statement parser retains one owner;
other parser/checker/emitter flags remain separate source-cleanup work.

O3 continues incrementally; O4–O5 are not complete. Next, audit the remaining
lexer and driver dependencies alongside active gate-derived naming. The
recovery harness also needs independent workspace isolation and stage-level
cost visibility, tracked in
[issue #295](https://github.com/type-rb/type-rb-native/issues/295).
Do not move the remaining entry into another catch-all module or claim the
compiler is fully decomposed. The remaining QBE adapter is also a decomposition
target while checked/MIR ownership replaces its semantic analysis.

The ordinary compiler project move under
[issue #274](https://github.com/type-rb/type-rb-native/issues/274) relocates
`compiler/gate4/` to `compiler/`, including configuration, tests, conformance
inputs and unchanged transition markers. Current entry/recovery/CI consumers
move together. The [layout migration map](compiler-project-layout.md) records
the retained historical exceptions and fail-closed cross-revision resolution.
This removes the checkpoint from the project path, not the remaining `Gate4`
implementation symbols or the snapshot/runtime families in root `src/`.

Follow with the architecture/development-plan documentation cleanup below and
an evidence-based audit of open issues. Record a concrete dependency or reopen
condition for deferred work; close a rejected bounded experiment only with its
retained result, not as though the optimization had shipped. Then resume
general-purpose MIR optimization toward repeatable spectral-norm performance
at least matching Pure Go. Independent documentation and issue maintenance
may proceed while code authorities run. Improve a measured CI bottleneck
without weakening the acceptance authorities or running formal benchmarks for
documentation-only changes.

Use the active milestone issue and cohesive PRs to record scope, identities,
expected generated-output effects and relevant validation. Register a separate
issue when scope or a real design question changes, not for every code slice. If O2 encounters a
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
[PR #261](https://github.com/type-rb/type-rb-native/pull/261) moved detailed
gate contracts and completed-gate narrative from the development plan and
architecture into the gate reference, preserving old anchors and exact
historical content. Maintain that separation; do not trade one oversized
README for multiple competing descriptions of current status.

Documentation-only changes use the existing lightweight documentation CI.
Source moves still run their applicable code authorities; do not misclassify a
move as documentation merely because its intended behavior is unchanged.


## Named MIR value carrier

After ordinary record Arrays, matching recovery and verified checkout handoff
PR #356, the first positional MIR carrier becomes `Gate4MirValue` in `mir.trb`.
Only the value table and its local staging table use the named five-field
record. Construction, lookup and semantic validation remain in their existing
owners; exact recovery imports change alongside the canonical source.
Malformed value identity, type, origin, uniqueness and definition counts still
fail verification. Other row families retain their current layouts and remain
separate bounded cleanup slices. This changes representation without adding an
optimization pass, backend semantic owner or application runtime claim.


## Scalar range checkpoint

The scalar Integer guard slice uses named `MirScalarRange` records for its
transient proof state and keeps proof construction and independent validation
in MIR. Backend emission consumes the verified bound and retains only the
checked/unchecked instruction selection. This advances the named-carrier
cleanup without moving an active compiler-source closure during its frozen
measurement cohort. The remaining positional MIR tables and Array assignment
ownership need separately bounded changes with recovery and cost checks.

## Local Array-header installation

The header slice extends the existing checked region rather than adding a
second fact store. MIR owns the complete unique list of accessed stable
parameter/local declarations and rejects missing or forged entries. Parameter
and local lowering share `gate4_install_stable_array_header`; the adapter stores
only the corresponding operand tuples. Mutable bindings use the same path,
with Array rebinding recorded as a conservative barrier by the checker. The
previous single-header representation has been removed. Broader control-flow
migration remains a separate measured slice.

The conditional Array-region slice in
[issue #384](https://github.com/type-rb/type-rb-native/issues/384) extracts
conditional statement checking from the large block checker into one helper
inside `checked_program.trb`. It owns condition checks, arm-local scope
restoration and checked MIR control markers. The block checker delegates the
statement while retaining loop dispatch. No second semantic owner, new module
boundary or source-flattening exception is introduced.

The follow-up in
[issue #386](https://github.com/type-rb/type-rb-native/issues/386) separates
`checked_while` from block dispatch. It retains the existing scalar induction
admission, condition checks, fallback nonnegative invalidation and lexical
scope restoration. The dispatcher uses the accepted `elsif` and bare `break`
syntax to replace its completion flag and nested statement-selection chain.
Conditional checking remains in its existing helper, unchanged. This is one
checked-program owner with clearer control structure, not a new MIR fact or
loop-local effect proof. Recovery still derives the same module boundary.

## Hash index self-use slice

[Issue #403](https://github.com/type-rb/type-rb-native/issues/403) replaces the
compiler's bespoke module/function indexes with ordinary Hash collections after
the verified seed and snapshot handoff. The slice removes `Gate4SymbolIndex`
and nine gate-prefixed index helpers, including whole-index rebuilding.
Project source ordering also releases its redundant name vector. The two
project import-cycle helpers use responsibility names and a separate local color
array; cycle checking no longer borrows symbol-table storage. Canonical imports,
strict recovery prefixes and index/graph tests move together. Dense token/MIR
vectors and active recovery families remain outside this bounded change.

Decision 0033's expired source-tree-specific Hash transition hook is removed.
Subsequent compiler changes use ordinary ratios; accepted absolute ceilings,
frozen baselines and historical marker contracts remain unchanged.

## Ordinary MIR model names

The bounded O4 slice in [issue #408](https://github.com/type-rb/type-rb-native/issues/408)
replaces the six active `Gate4Mir...` record names with `MirArrayOperation`,
`MirInstruction`, `MirBlock`, `MirFunction`, `MirValue`, and `MirModule`.
Fields, declaration order, verification, optimization, and backend behavior
remain unchanged. Frontend/state consumers, focused tests, and the exact
recovery import boundary use the same canonical names, without aliases.
Historical accounts above retain their source-era identifiers. Gate-derived
helper names and the separate snapshot model remain subsequent ownership work.

The first compiler-authored Array traversal slice follows the verified Array
seed and checkout handoff. `checked_hash_verify` and `project_config_has_key`
replace their manual cursors with `each`; MIR function lookup uses
`each.with_index` and is renamed from `gate4_mir_function_index` to
`mir_function_index`. Current callers, tests and strict recovery import prefixes
change together, without an alias. The same tables, first-match/early-return
behavior and MIR facts remain. This removes one active gate-derived helper name;
it does not change lookup representation or claim an application speedup.

## Shared iteration proofs

The shared iteration proof boundary now lives in
`compiler/src/iteration_checked.trb`. It owns `checked_iteration_shape` and
`checked_iteration_require`, originally extracted from `checked_program.trb`,
and now also validates checked Range construction and iteration source kinds.
The recursive checker, compiler entry and REPL import this one implementation;
the proof module never imports the recursive checker or emitter. The canonical
compiler bundle and strict recovery closure include the new eighteenth module,
with matching import validation, deterministic flattening and mutation tests.
Array and Range share `emit_iteration` and REPL body/transfer ownership. The
source-kind verifier is used by both plan retrieval and loop-transfer checks.
The old `emit_array_iteration` entry is removed. `syntax_expression_precedence`
replaces the gate-prefixed binary-precedence helper because Range construction
is an expression operation with its own precedence and proof, not scalar arithmetic.

## Recovery program fixtures

The active authored-program recovery fixtures now live in
`fixtures/recovery/programs/`. Boolean and record Array closure programs retain
their exact inputs and outputs; Hash programs share the same runner with the
new Array iteration cases. The runner owns snapshot export, decoding, selected
collection probes, build, and execution, while each test keeps its expected
outcome. This removes the gate-numbered path for these live programs without
moving historical snapshots, changing their protocols, or claiming that other
gate-derived source names have been retired.
