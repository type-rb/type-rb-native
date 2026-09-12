---
name: develop-typerb-native
description: Implement or review TypeRB Native compiler, runtime, recovery, and performance changes.
---

# Develop TypeRB Native

Complete the requested Native change with evidence appropriate to its affected
surface. Work within the task's stated endpoint and budget. A review-only request
stays read-only; a PR-only request includes the requested implementation and
verification, then stops before merge or a next experiment.
For documentation edits, use this skill only when its Native-specific boundaries
or validation guidance are needed.

## Choose the relevant guidance

`AGENTS.md` owns repository-wide constraints. Read the matching guidance below
when the change needs it; do not load every reference before routine work.
All `docs/` and configuration paths below are relative to the repository root.

| Changed surface | Read when needed |
| --- | --- |
| Feature selection or coverage claims | `docs/native-language-coverage.md`; preserve ordinary check/build/execution/REPL versus recovery distinctions. |
| Compiler, MIR, runtime, driver, or target implementation | [Compiler constraints](references/compiler.md) and the decisions for the affected boundary. |
| Ordinary compiler source, recovery, self-hosting, or seed handoff | [Bootstrap and recovery](references/bootstrap.md), including recovery-enabled suites for compiler-source changes. |
| Source decomposition, names, or removal | `docs/repository-organization.md` and the affected consumer inventory; applicable recovery and cost checks still apply. |
| Performance experiments or retained results | [Measurements and retention](references/measurements.md); use `docs/experiment-plan.md` when defining a material experiment. |
| Reference pin or compatibility | `docs/type-rb-compatibility.md`, `docs/versioning.md`, and the cross-repository procedure in `CONTRIBUTING.md`. |
| Documentation, instructions, or metadata only | Check changed text, links, metadata and the applicable documentation CI. Compiler/bootstrap/benchmark runs are not implied. |

Read `docs/mir-consolidation.md` for the current larger milestone, permitted
intermediate cost regressions and integration/qualification distinction.
Use `README.md` for orientation when project context is missing. Small fixes and
documentation corrections do not need a new experiment proposal. For material
experiments and source-organization slices, use the owning plan's registration
requirements and establish scope and exit criteria before implementation.

## Verify the affected surface

Use `docs/ci-validation.md` and the maintained commands in `CONTRIBUTING.md`.
The CI plan for the actual changed paths determines required authorities; do
not skip them because a change looks small. Complete focused local checks and
the required CI, fixing failures caused by the change. After they pass, repeat
or broaden checks only for new edits, failures, or unresolved concerns.

For root TypeRB source checks, use the exact `TYPE_RB_REVISION` compiler:

```sh
trb fmt --check .
trb check --config trbconfig.reference.jsonc
TYPE_RB_NATIVE_ROOT="$PWD" trb test --config trbconfig.reference.jsonc
```

The default root configuration runs the example; root verification explicitly
uses `trbconfig.reference.jsonc`, and the compiler suite uses
`compiler/trbconfig.jsonc`. For compiler-source changes, load the bootstrap
reference above: successful optional tests without the recovery/QBE environment
do not establish recovery coverage.

## Finish within the requested scope

Report the implemented subset, meaningful validation, relevant measurements,
and remaining limitations. Fix routine issues within the authorized task
without introducing a new approval checkpoint. If a skill instruction requires
a pause, identify the exact file and instruction, and explain the unresolved
decision; do not turn an optional recommendation into a mandatory approval.

When the user has authorized continued development, pursue the active milestone
through cohesive ownership changes within that authorization and budget. Avoid
turning each helper move or size overrun into a separate acceptance milestone.
Honor later limits such as one small task or stopping with an open PR. Use issue-closing keywords
only when the reviewed PR actually completes the issue; even a negated closing
keyword can close it on merge.
