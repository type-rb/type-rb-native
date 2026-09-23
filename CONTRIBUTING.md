# Contributing to TypeRB Native

TypeRB Native targets a production-ready TypeRB-authored compiler and toolchain.
Contributions advance complete language and package coverage, practical tooling,
correctness, portability and measured performance. The
[MIR consolidation roadmap](docs/mir-consolidation.md) defines the active milestone.
Report implemented coverage and validation separately from the eventual goals.

## Proposing work

Use an existing milestone issue or open one for material feature or architecture
work. Record durable architectural decisions under `docs/decisions/`; keep scoped
implementation work and its acceptance conditions in the issue.

Record the behavior or ownership change, relevant reference revision, validation
and remaining gaps. Performance or backend experiments also record the hypothesis,
baseline and candidate configurations, measurements and acceptance or removal
conditions. Feature coverage does not need an experimental hypothesis to be useful.

Small fixes and documentation corrections do not need a separate experiment
proposal. Current MIR work follows the larger
[consolidation milestone](docs/mir-consolidation.md), including its explicit
temporary cost policy; individual helper moves do not need a new proposal.

Follow the [repository organization schedule](docs/repository-organization.md)
for source moves and naming cleanup. Inventory consumers before removing
recovery and ordinary compiler code, keep mechanical changes separate from optimization, and
preserve recovery and measurement coverage. Keep routine checkpoint narratives
out of the root README; link to the owning status page or dated evidence.

Keep implementation drafts in the quick-feedback stage. After focused local
proof and negative-case review, mark cohesive PRs ready for complete correctness.
During basic-language completion, organize changes by complete language families:
syntax, checking, MIR ownership, execution, REPL and shared conformance belong
in the same integration candidate. Large PRs are appropriate when they close
that coherent contract; keep their commits and acceptance evidence reviewable.
Prefer one ready integration candidate and one subsequent development batch
over a stack of small PRs that repeatedly run complete validation. Measure
progress by completed language contracts and remaining gaps, not PR count.
During MIR consolidation, detailed comparative cost qualification belongs at
milestones; costs observed during migration do not establish qualification. See the
[CI validation stages](docs/ci-validation.md) for routing, manual runs, and
the fail-closed merge-acceptance check.

## Correctness

The TypeRB specification and accepted conformance behavior define expected
language semantics. The reference implementation is the bootstrap compiler and
a differential oracle; a discrepancy may reveal a bug on either side and must
be triaged against the specification. Unsupported behavior must produce a
deterministic diagnostic rather than a fallback with different semantics.

Performance does not justify changing portable integer behavior, Unicode
behavior, failure behavior, initialization order, source attribution, or other
TypeRB guarantees.

Repository-owned compiler and runtime implementation source must be TypeRB.
External backend and platform tools are allowed when their revisions, licenses,
invocations, and distribution costs are explicit. Do not introduce a permanent
Go, Rust, Zig, or C host implementation as an intermediate shortcut.

Use the pinned reference compiler revision recorded in `TYPE_RB_REVISION` for
checkpoint verification. A revision update is a reviewed compatibility change, not
an incidental tool upgrade.

Build a clean checkout of that revision with the declared executable version:

```sh
python3 tools/build-reference.py /path/to/type-rb /path/to/trb
```

This verifies the source identity and embeds the exact version in
`compatibility/current.json`, including for shallow release-source checkouts.
See the [release integration procedure](docs/type-rb-compatibility.md#release-integration)
when advancing the reference after a TypeRB release.

## Cross-repository changes

Keep the reference TypeRB repository independent of this project. When a
temporary producer change is required upstream:

- define and name it only in terms of reference-compiler behavior;
- keep it internal, narrow, versioned, data-only, and removable;
- do not mention TypeRB Native, experimental checkpoint names, native-backend plans, or
  consumer-specific aliases in upstream code, diagnostics, tests,
  documentation, changelog entries, commits, or pull requests; and
- record the integration command, snapshot compatibility mapping, exact merged revision,
  compatibility note, and removal condition in this repository.

Before opening the upstream pull request, audit both its diff and proposed
title and body for project terminology. Update `TYPE_RB_REVISION` and CI only
after the upstream change is merged, then run the complete native checks with
the exact pinned compiler.

## Validation scope

Choose checks using [CI validation](docs/ci-validation.md) and the actual changed
paths. Documentation-only corrections need text, link, metadata and applicable
documentation checks; they do not require compiler recovery or benchmark runs.
Code changes retain their required correctness, recovery, target, memory and
cost authorities. After relevant checks pass, repeat or expand them for new
changes, failures or unresolved concerns rather than by default.

For compiler-source changes, also enable the recovery/QBE environment described
in [the compiler recovery guidance](.agents/skills/develop-typerb-native/references/bootstrap.md).
An optional test that skips recovery does not count as recovery evidence.
Hosted CI owns complete integration verification by default. Locally, run the
affected units, positive/negative reference comparisons, MIR and REPL checks,
and the ordinary Native build when compiler source changes. A second full local
recovery run is required when changing bootstrap or validation orchestration,
or when diagnosing a recovery or platform failure; it is not a prerequisite
for every intermediate language edit. Record pending CI authorities explicitly
and merge only after all applicable checks accept the candidate.

Keep the edit loop local and narrow. For example, after a MIR Array change,
run its QBE-backed compiler tests with the pinned reference compiler and QBE:

```sh
TYPE_RB_NATIVE_ROOT="$PWD" TYPE_RB_NATIVE_QBE=/path/to/qbe \
  /path/to/pinned/trb test --config compiler/trbconfig.jsonc \
  -t 'Array loop CFG MIR'
```

Use the matching test name for another feature family. Run formatting, type
checking, reference/Native behavior cases and the ordinary Native fixed point
as the batch becomes coherent; leave the full cross-platform recovery, target,
CLI and memory authorities to the one ready PR. Start the next local batch while
that PR validates instead of waiting for each hosted job to finish.

For source and compatibility validation, run the maintained root checks:

```sh
trb fmt --check .
trb check --config trbconfig.reference.jsonc
tools/check-native-cli.sh /path/to/trb
TYPE_RB_NATIVE_ROOT="$PWD" trb test --config trbconfig.reference.jsonc
python3 -m unittest tools/compatibility_manifest_test.py
python3 tools/compatibility_manifest.py --reference-trb /path/to/pinned/trb
```

`NATIVE_VERSION` identifies this implementation independently from TypeRB.
When changing it, `TYPE_RB_REVISION`, the compatibility manifest, bootstrap or
target identities, or their evidence, keep the canonical files consistent and
follow the bump rules in [Native versioning and compatibility](docs/versioning.md).

## Backend changes

Backend candidates share Native MIR, conformance inputs, and benchmark policy.
Same-target comparisons share a versioned target ABI profile. Keep
candidate-specific code behind the backend boundary. Do not add language syntax
or expose a backend name in a user-facing TypeRB API solely for an experiment.

## Benchmark claims

Benchmark pull requests must include enough information to reproduce the
result:

- repository revisions and exact commands;
- hardware, operating system, and toolchain versions;
- cold, warm, or incremental cache state;
- repetitions, aggregation method, and raw measurements;
- phase timings where available; and
- executable, runtime, linker, library, and sidecar sizes.

Compare against an optimized Go release baseline. A backend-only microbenchmark
may diagnose code generation, but it does not establish an end-to-end TypeRB
advantage.

## Language and workflow

Use English for committed documentation, code comments, commit messages, and
pull request text. Submit changes through focused pull requests and keep the
default branch passing its documented checks.
