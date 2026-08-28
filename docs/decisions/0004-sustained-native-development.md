# 0004: Sustained Native Development and a Staged Gate 2

## Status

Accepted.

## Context

The initial plan described the repository primarily as a sequence of bounded
experiments whose native path could be abandoned after an early performance
miss. Gate 1 instead established a useful executable baseline: the QBE path was
correct on its scalar corpus, substantially reduced build time and executable
size, and kept runtime within the registered bound.

The project's intent is now stronger. It should make a sustained engineering
effort toward a better native implementation, ultimately self-hosted in TypeRB,
rather than treating each incomplete stage as a reason to stop. Measurements
remain essential, but their main purpose is to locate work and guide backend or
runtime choices.

Gate 2 previously grouped static aggregates with dynamic strings, arrays,
closures, allocation, and failure behavior. Those features answer different
architectural questions. Implementing them together would obscure whether a
problem belongs to value layout or memory ownership.

## Decision

TypeRB Native is a sustained implementation effort with experimental stability.
Gates are correctness, architecture, and whole-toolchain performance
checkpoints. Missing a target keeps the gate open for diagnosis and improvement
unless the evidence reveals a fundamental conflict with TypeRB semantics,
safety, or sustainable self-hosting.

Gate 2 is restricted to heap-free aggregate values:

- nominal, immutable records;
- payloadless and payload-bearing enum variants;
- the static tagged representation needed for `Result`;
- aggregate construction, projection, dispatch, direct calls, block parameters,
  and returns; and
- monomorphized layouts composed only from Gate 1 scalars and other Gate 2
  aggregates.

Dynamic strings, collections, closures, escaping values, allocation, and memory
management move to Gate 3. This is a staging decision only; those capabilities
remain required for the eventual native compiler and runtime.

The bootstrap snapshot, Native MIR, `darwin-arm64-v0` ABI profile, and QBE
adapter remain internal and disposable. Their instability lets the
implementation improve without creating a native-only TypeRB dialect or a
public compiler API.

## Consequences

- Gate 2 can establish deterministic layout and tagged-value semantics without
  prematurely selecting ownership or garbage collection.
- Records, payload enums, and `Result` use the existing TypeRB language contract;
  this decision adds no syntax or user-visible semantic variation.
- Performance misses produce optimization work or a backend decision rather
  than automatic project abandonment.
- The Go reference compiler remains an early bootstrap producer and semantic
  oracle until the later TypeRB-authored frontend and reproducible self-hosting
  gates replace it in the ordinary path.
- Experimental adapters can still be removed when they no longer have a
  distinct measured role.
