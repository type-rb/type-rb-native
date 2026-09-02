# TypeRB Native

Keep committed documentation, code comments, commit messages, and pull request
text in English.

## Public repository boundary

- Keep every repository artifact, issue, pull request, and release note
  explainable solely from public information in this repository or other public
  sources.
- Never include names, URLs, local paths, quotations, descriptions, or
  provenance from private repositories, applications, data, or discussions.
- Reproduce externally discovered problems with generic synthetic examples and
  a self-contained public rationale that does not reveal private provenance.

Treat this repository as an experimental research project, not as a supported
TypeRB backend or product commitment.

- Use `type-rb/type-rb` as the source of truth for TypeRB syntax, semantics,
  diagnostics, packages, and conformance behavior.
- Do not introduce native-only language semantics or silently weaken portable
  behavior to improve a benchmark.
- Keep Native MIR, target ABI profiles, and backend details internal and explicitly
  unstable until a separate promotion decision is accepted.
- Keep the reference TypeRB repository consumer-neutral and independent of this
  experiment. Its code, diagnostics, tests, documentation, changelog, commits,
  and pull requests must not name TypeRB Native, this repository's gates,
  native-backend plans, or consumer-specific compatibility aliases.
- Any temporary bootstrap capability added to the reference repository must be
  justified and named only by reference-compiler semantics. Keep it narrow,
  versioned, data-only, internal, and removable.
- Keep all Native integration commands, revision pins, gate mappings, bridge
  compatibility notes, and retirement conditions in this repository.
- Put backend-specific lowering behind a common verified Native MIR boundary.
  Same-target comparisons use the same ABI profile. Do not duplicate the
  frontend or runtime semantics for each backend candidate.
- Put TypeRB semantic facts and optimization decisions in Native MIR analysis
  and target-independent passes. Backend adapters may legalize and select
  instructions, but must not rediscover Integer ranges, index validity, loop
  structure, call effects, Array-header stability, or GC safety from source or
  backend text.
- Treat the current self-hosted direct-QBE path as migration evidence rather
  than the target optimizer architecture. Finish already registered narrow
  experiments, but do not add new non-trivial semantic analysis to its emitter.
- Keep ordinary optimization candidates inside their registered compactness
  bounds. A Native MIR foundation may use a separately pre-registered,
  temporary compiler-size envelope only after measuring the smallest useful
  skeleton; record build time, RSS, and size throughout, remove superseded
  emitter logic, and preserve the final Go-competitive build and artifact
  goals. Register each successive structural transition with an exact validated
  marker before changing its limits. After the marker reaches the baseline,
  ordinary relative limits apply again; do not begin another fact family until
  the registered direct-emitter recovery is complete.
- For a bounded removal slice whose complete compiler is unchanged only by
  executable-format alignment, require strict same-run code-section and
  target-neutral-QBE shrinkage plus complete-compiler non-growth on every
  registered target. Keep cumulative complete-artifact shrinkage mandatory
  before the current MIR fact family is declared recovered.
- Record benchmark inputs, commands, revisions, hardware, operating system,
  toolchain versions, cache state, repetitions, and raw results. Include every
  required sidecar, linker, and runtime in size comparisons.
- Prefer explicit unsupported-feature diagnostics to fallback semantics,
  unchecked lowering, or `Any`-shaped escape hatches.
- Add only the structure required by the current experiment gate. Do not add
  release, package, or compatibility machinery before a real consumer needs it.
- Write repository-owned compiler and runtime implementation source in TypeRB.
  External code generators, assemblers, linkers, SDKs, and system libraries are
  allowed when their role and cost are explicit.
- Treat reproducible TypeRB self-hosting as a required promotion outcome. The
  Go reference compiler is an early bootstrap and differential oracle, not part
  of the ordinary final release path.
