---
name: develop-typerb-native
description: Implement and review TypeRB Native compiler, MIR, runtime, bootstrap, gate, fixture, and benchmark work. Use for changes in type-rb/type-rb-native, especially when deciding the current gate scope, preserving TypeRB semantics, or updating the pinned reference compiler.
---

# Develop TypeRB Native

Work on one recorded experiment gate at a time.

## Establish the boundary

1. Read `README.md`, `docs/architecture.md`, and `docs/experiment-plan.md`.
2. Read the decisions relevant to the change.
3. Treat `type-rb/type-rb` at `TYPE_RB_REVISION` as the language, compiler, and
   conformance source of truth.
4. State the current gate and its exit condition before expanding scope.

## Preserve repository ownership

- Gate names, Native MIR, backend and runtime plans, integration commands,
  revision pins, compatibility notes, and bridge retirement conditions belong
  only in this repository.
- Keep the reference TypeRB repository consumer-neutral. Never add TypeRB
  Native, gate numbering, native-backend plans, or consumer-specific aliases to
  its code, diagnostics, tests, documentation, changelog, commits, or pull
  requests.
- If this project requires a temporary reference-compiler surface, justify and
  name it only by reference-compiler semantics. It must remain narrow,
  versioned, data-only, internal, removable, and independently understandable
  without this repository.
- Before submitting a reference-repository change, audit both the diff and pull
  request text for leaked project terminology. Record the consumer command,
  exact merged revision, gate mapping, and removal plan here instead.

## Implement

- Write repository-owned executable compiler and runtime source in TypeRB.
- For self-hosting gates, require runtime-supplied source to pass through the
  checked-in lexer, parser, resolver, checker, and emitter. Reject embedded
  compiler artifacts, source-specific output paths, quines, and hidden host
  fallbacks as bootstrap evidence.
- Record B0, B1, and B2 roles explicitly. Verify the ordinary regeneration
  process graph rather than inferring Go independence from the output binary.
- Allow external code generators, assemblers, linkers, SDKs, and system
  libraries only behind explicit boundaries whose time and distribution cost
  can be measured.
- Preserve source origins and exact TypeRB semantics through every lowering.
- Reject unknown, malformed, unsupported, or unverifiable input with stable,
  deterministic diagnostics. Never add a semantic fallback or `Any` escape
  hatch to improve a benchmark.
- Keep bootstrap snapshots, Native MIR, ABI profiles, and runtime interfaces
  internal and unstable until a decision explicitly promotes them.
- Add only the feature set required by the active gate. Record a new decision
  before changing language semantics, ownership boundaries, self-hosting
  criteria, or backend selection policy.

## Verify

From the repository root, use the compiler revision in `TYPE_RB_REVISION` and
run:

```sh
trb fmt --check .
trb check
TYPE_RB_NATIVE_ROOT="$PWD" trb test
```

For executable gates, run the same differential corpus through the optimized
Go reference baseline and every active native candidate. Count frontend,
serialization, lowering, code generation, assembly, linking, runtime, sidecar,
and distribution costs according to `docs/experiment-plan.md`.

When the active gate passes, stop before starting the next gate. Report the
implemented subset, evidence for every exit condition, measurements, known
limitations, discarded paths, and decisions that need maintainer discussion.
