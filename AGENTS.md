# TypeRB Native

Use English for committed documentation, code comments, commit messages, and
pull request text. This is an experimental research project, not a supported
TypeRB backend or product commitment.

## Scope and completion

Carry the user's requested task through its stated completion point. Use existing
authorization for routine implementation choices, reversible checks, and fixes
within that scope. Ask only for missing information or an unresolved decision
that materially changes the result or requires new authority. A request to
prepare a PR for review ends with an open PR; it does not authorize a merge or
another development slice. Later task and budget limits narrow earlier standing
direction to continue.

Read documents relevant to the affected surface. Use the
[development skill](.agents/skills/develop-typerb-native/SKILL.md) for compiler,
MIR, runtime, recovery, or performance work and its conditional reference map
for specialized constraints. For routine documentation edits, check the changed
text and applicable documentation CI. For code, complete the authorities in
[CI validation](docs/ci-validation.md); avoid redundant runs after they pass
unless a new change, failure, or unresolved concern warrants them.

## Public repository boundary

Keep every outward-facing artifact explainable solely from public information
in this repository or other public sources. Never publish private names, URLs,
local paths, quotations, data, implementation details, or provenance. Use
self-contained generic reproductions, and inspect the complete diff and
outward-facing text before publication.

## Implementation invariants

- `type-rb/type-rb` at `TYPE_RB_REVISION` is the language and conformance source
  of truth. Preserve exact semantics, origins, and deterministic diagnostics;
  reject unsupported input instead of introducing a native-only dialect,
  unchecked fallback, or `Any` escape hatch.
- Keep the reference repository consumer-neutral. Native gate mappings, backend
  plans, pins, bridge compatibility and retirement conditions belong here.
  Reference changes must be justified by reference semantics, without Native
  terminology or consumer aliases. Follow `CONTRIBUTING.md` for that workflow.
- Write repository-owned compiler and runtime implementation in TypeRB.
  External backend/toolchain/system dependencies are allowed with explicit roles
  and costs. Ordinary self-hosting must reproduce from Native source; recovery
  through the Go reference compiler is separate evidence.
- Put TypeRB facts and optimizations in verified Native MIR and target-independent
  passes. Backend adapters consume them; they must not rediscover ranges, index
  validity, loop structure, call effects, Array-header stability, or GC safety.
  Finish registered direct-QBE experiments as migration evidence and remove
  superseded emitter ownership before broadening the fact family.
- Keep snapshots, MIR, ABI profiles, and runtime interfaces internal and unstable
  until an explicit promotion decision. Do not add release/package machinery,
  a second frontend, or another backend without a concrete accepted need.

## Conditional project guidance

- For language coverage, follow `docs/native-language-coverage.md`: pair basic
  syntax with MIR checks and verified compiler self-use. Deferred optimizer
  acceptance does not block language work.
- For source organization, follow `docs/repository-organization.md`, including
  root gate-numbered files and symbols. At accepted optimization checkpoints,
  advance a bounded cleanup or record its concrete blocker within the task's
  scope. Preserve applicable recovery/measurement checks and immutable history.
- Before adopting new syntax in compiler source or changing seeds, follow
  `docs/bootstrap-seed-updates.md`. Verify actual published immutable assets
  before changing exact pins; unaccepted candidates and floating downloads are
  not replacement seeds.
- For optimization or measurement work, follow `docs/optimization-tradeoffs.md`
  and `docs/experiment-plan.md`. Ordinary 1.05 ratios and absolute ceilings remain
  in force. A registered diagnostic is not merge approval. Retain failures and
  compare same-feature and frozen cumulative baselines; report compiler and
  application costs separately, counting all required dependencies.
