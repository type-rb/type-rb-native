---
name: develop-typerb-native
description: Implement and review TypeRB Native compiler, MIR, runtime, bootstrap, gate, fixture, and benchmark work. Use for changes in type-rb/type-rb-native, especially when deciding the current gate scope, preserving TypeRB semantics, or updating the pinned reference compiler.
---

# Develop TypeRB Native

Work on one recorded experiment gate or independently measurable gate slice at
a time.

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
- Keep ordinary compiler input file- or project-oriented once that boundary is
  available. Source-content argv adapters must be explicitly hidden, limited
  to recovery or differential tests, and kept distinct from ordinary command
  shapes. Test stdout, stderr, exit status, unreadable input, and inputs beyond
  conservative argv limits.
- For file-root compilation, follow the pinned reference compiler's explicit
  import closure: root imports at the entry directory, load only reachable
  declaration imports, retain canonical module and declaration identity, and
  require `main` from the entry module. Resolve a unique directory `index`
  through either equivalent authored path, but reject a resolved graph that
  contains both `name.trb` and `name/index.trb`; never restore direct-file
  precedence between two loaded identities. Test named and bare aliases,
  declaration identity, the ASCII root-key rule, unrelated invalid siblings,
  diamonds, cycles, duplicate and unused bindings, missing exports, path
  escape, optional suffixes, and paths containing spaces. Do not silently turn
  this experimental boundary into package, namespace, or public CLI behavior.
- Treat the canonical compiler as a real file-root closure. Keep extracted
  declarations in one TypeRB source only, require explicit imports, and run
  every ordinary replacement generation from the entry path. A temporary
  flattened equivalent is recovery-only: derive it deterministically from the
  canonical modules, verify and record its inputs, never commit it, and never
  substitute it for an ordinary self-hosted build.
- Record B0, B1, and B2 roles explicitly, plus B3 when a fixed-point check is
  required. Verify the ordinary regeneration process graph rather than
  inferring Go independence from the output binary. Keep recovery compilers and
  measurement orchestrators out of the ordinary semantic chain, and inspect
  executable imports and external-tool subprocesses when recording the graph.
- When claiming Native bootstrap closure, use each produced compiler as the
  executable seed of the following full build. Record the initial seed
  provenance separately, compare same-basename output bytes across repeated
  generations, and never count recovery seed creation as part of the ordinary
  Go-free chain.
- When distributing an experimental bootstrap seed, keep compiler binaries out
  of Git history. Record one-time root provenance separately, publish raw
  target compilers with a strict versioned SHA-256 manifest and artifact
  attestations, make the completed release immutable, and verify the actual
  published assets from fresh target runners before calling the handoff
  durable. Later ordinary chains start only from a previous Native compiler;
  they must not quietly recreate recovery through Go or the reference
  compiler. Do not infer stable version, compatibility, installation, signing,
  or support promises from an experimental bootstrap tag.
- Allow external code generators, assemblers, linkers, SDKs, and system
  libraries only behind explicit boundaries whose time and distribution cost
  can be measured.
- For every target addition, use an internal versioned profile and keep the
  frontend, Native MIR semantics, runtime behavior, and backend IL shared.
  Record the QBE/backend target, ABI, linker policy, external dependencies,
  executable format and imports, deterministic-output policy, and recovery
  provenance. Reject unknown profiles before source or tool access, and keep
  all Native target and gate terminology out of the reference repository.
- When the Native compiler owns external-tool orchestration, execute explicit
  tool paths directly rather than assembling a shell command. Preserve child
  diagnostics, decode child completion deterministically, publish output only
  after every phase succeeds, and remove intermediates after success and every
  failure. Test paths containing spaces, existing-output replacement, each
  phase failure, and that compiler diagnostics launch no external tool.
- Preserve source origins and exact TypeRB semantics through every lowering.
- Treat the portable Integer range and its failure classes as correctness
  constraints. Backend optimization may inline or outline checks under a
  deterministic code-size policy, but it must not substitute machine-word
  overflow or omit division and range failures to meet a measurement bound.
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

Treat a published bootstrap tag, release, and asset set as immutable. When its
verification procedure must advance, keep compiler source and fixtures pinned
to the release tag, record the exact verifier revision separately, and never
replace the seed in place. Interleave adjacent comparative measurements on
shared runners, write medians before applying bounds, and retain evidence from
failed as well as successful verification runs.

When the active gate or slice passes, record and report the implemented subset,
evidence for every exit condition, measurements, known limitations, discarded
paths, and decisions that need maintainer discussion. If the maintainer has
given standing direction to continue, pre-register the next bounded slice and
proceed; gate completion alone is not a reason to stop. Stop before work that
requires an unresolved language, ownership, release, or product decision.

Use GitHub issue-closing keywords only in the reviewed result pull request that
actually completes a gate. Never put a closing keyword next to the gate issue
even in a negated sentence: GitHub does not interpret the negation and will
close the issue when the intermediate pull request merges.
