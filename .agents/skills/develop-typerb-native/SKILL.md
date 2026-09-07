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
5. Read `docs/native-language-coverage.md` when selecting a new feature or
   changing coverage claims. Prefer the current basic-language slices and
   their necessary MIR work over further benchmark tuning. Keep ordinary
   check/build/execution/REPL evidence distinct from recovery, and complete
   the seed/recovery prerequisites before compiler source adopts new syntax.

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
- Keep semantic analysis above backend emission. Represent proven Integer
  ranges, index properties, loop structure, call effects, Array-header
  stability, and GC safety as verified Native MIR facts or analysis results;
  target-independent passes consume those facts, and backend adapters consume
  the resulting MIR. Do not add new non-trivial source-pattern analysis to the
  QBE emitter. An already registered narrow emitter experiment may be completed
  as migration evidence, but follow-on generalization belongs in MIR.
- Migrate the current direct-QBE self-hosted path through bounded vertical
  slices. Define the smallest useful MIR operation and fact subset, verify it,
  lower it through the existing QBE ABI, and remove the superseded emitter
  ownership before expanding the subset. Do not build a general optimizer or a
  second production backend ahead of the measured workload.
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
- Before choosing an optimization's cost/benefit path, read
  `docs/optimization-tradeoffs.md`. Keep ordinary 1.05 ratios and absolute CI
  ceilings unchanged unless a separate reviewed acceptance decision updates
  their enforcement. A cost miss is not, by itself, a reason to abandon a
  promising optimization or spend indefinitely on size-only refinements.
- Register a candidate-specific diagnostic before measuring beyond an ordinary
  cost bound: exact identities, cumulative and same-feature controls, numeric
  investigation ceilings, runtime benefit/control criteria, run budget,
  correctness prerequisites, expiry and next decision. Do not convert this into
  automatic merge authority or silently reuse a structural transition marker.
- Preserve all earlier failed results. Compare actual application build/size and
  runtime separately from compiler self-build/text/QBE/distribution costs; old
  Go measurements do not establish current or general-purpose spare capacity.
- At coherent checkpoints track incremental and cumulative cost and the next
  action. After two bounded size-only attempts without a current runtime-benefit
  assessment, choose bounded measurement, trade-off review, or justified deferral
  before another such attempt. Keep active evidence in its existing result slot.
- Remove duplicate and superseded direct-emitter ownership as MIR slices migrate.
  Useful verified optimization code need not be cost-free: propose its retained
  cost explicitly. Before another fact family, account for outstanding migration
  debt and cumulative cost; do not add a second semantic owner or broaden LLVM
  work merely because an investigation budget exists.

## Verify

Before importing or reorganizing `results/`, read `docs/evidence-retention.md`.
Retain only results with a current purpose in `results/active.json`. Replace
the occupied slot, update consumers and remove superseded directories in the
same PR; do not accumulate dated snapshots or archive every intermediate run.
Preserve active/public measurement cohorts, frozen comparison baselines and
seed consumers. Keep significant rejected-approach reasons in the development
history and link retired evidence to its exact Git revision. Use a verified
public archive only when detailed evidence has a durable purpose. Run the
lifecycle/global-budget check with the actual PR base before publishing results.

From the repository root, use the compiler revision in `TYPE_RB_REVISION` and
run:

```sh
trb fmt --check .
trb check --config trbconfig.reference.jsonc
TYPE_RB_NATIVE_ROOT="$PWD" trb test --config trbconfig.reference.jsonc
```

The default root configuration is the runnable Native example, not the
reference-validation project. Select `trbconfig.reference.jsonc` explicitly
for the root reference checks and tests; use `compiler/trbconfig.jsonc` for the
compiler suite. See `CONTRIBUTING.md` for the maintained project commands.

For compiler-source changes, also enable the recovery and QBE-backed tests:
set `TYPE_RB_NATIVE_REFERENCE_TRB` to the absolute pinned compiler executable
and `TYPE_RB_NATIVE_QBE` to QBE 1.3, together with `TYPE_RB_NATIVE_ROOT`, when
running the root and `compiler` suites. Without those variables, optional
tests report success without exercising recovery; do not count that as complete
bootstrap verification. The recovery snapshot supports a narrower source subset
than the ordinary Native compiler, so ordinary fixed points alone are not a
substitute. See the environment in `.github/workflows/gate-zero.yml`.

For executable gates, run the same differential corpus through the optimized
Go reference baseline and every active native candidate. Count frontend,
serialization, lowering, code generation, assembly, linking, runtime, sidecar,
and distribution costs according to `docs/experiment-plan.md`.

Treat a published bootstrap tag, release, and asset set as immutable. Keep a
release-integrity re-verification pinned to the release source and fixtures,
and record the exact verifier revision separately. For a later source
compatibility revalidation, verify that immutable seed and its provenance
before execution, then record the newer compiler-source revision and resulting
fixed-point identity separately from the seed's source-era root and compiler
identity. Never replace or relabel the seed merely to align revisions.
Interleave adjacent comparative measurements on shared runners, write medians
before applying bounds, and retain evidence from failed as well as successful
verification runs.

When the active gate or slice passes, record and report the implemented subset,
evidence for every exit condition, measurements, known limitations, discarded
paths, and decisions that need maintainer discussion. If the maintainer has
given standing direction to continue, pre-register the next bounded slice and
proceed; gate completion alone is not a reason to stop. Stop before work that
requires an unresolved language, ownership, release, or product decision.

Do not add LLVM merely to continue local optimization work. First cover scalar,
Array, allocation, and I/O behavior through the shared MIR and benchmark corpus;
then use a bounded LLVM adapter as an optimization-ceiling comparison unless a
different measured backend question has become more important.

Use GitHub issue-closing keywords only in the reviewed result pull request that
actually completes a gate. Never put a closing keyword next to the gate issue
even in a negated sentence: GitHub does not interpret the negation and will
close the issue when the intermediate pull request merges.
