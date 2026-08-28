# Contributing to TypeRB Native

TypeRB Native is an evidence-driven experiment. Contributions should help
answer a defined correctness, performance, portability, runtime, or tooling
question without implying that a production native backend has been accepted.

## Proposing work

Open an issue before a material experiment. Record durable architectural
decisions under `docs/decisions/`; keep scoped implementation work and its
acceptance gate in the issue.

The proposal should record:

- the hypothesis;
- the supported TypeRB and Native MIR subset;
- the reference compiler revision;
- the baseline and candidate configurations;
- the measurements and acceptance or removal gate; and
- the parts intentionally left unsupported.

Small fixes and documentation corrections do not need a separate experiment
proposal.

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
gate verification. A revision update is a reviewed compatibility change, not
an incidental tool upgrade.

## Cross-repository changes

Keep the reference TypeRB repository independent of this project. When a
temporary producer change is required upstream:

- define and name it only in terms of reference-compiler behavior;
- keep it internal, narrow, versioned, data-only, and removable;
- do not mention TypeRB Native, gate numbers, native-backend plans, or
  consumer-specific aliases in upstream code, diagnostics, tests,
  documentation, changelog entries, commits, or pull requests; and
- record the integration command, gate mapping, exact merged revision,
  compatibility note, and removal condition in this repository.

Before opening the upstream pull request, audit both its diff and proposed
title and body for project terminology. Update `TYPE_RB_REVISION` and CI only
after the upstream change is merged, then run the complete native checks with
the exact pinned compiler.

Run the Gate 0 checks from the repository root:

```sh
trb fmt --check .
trb check
TYPE_RB_NATIVE_ROOT="$PWD" trb test
```

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
