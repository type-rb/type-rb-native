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

Follow `docs/native-language-coverage.md` for current feature selection. Keep
ordinary check/build/execution/REPL claims separate from snapshot recovery.
Pair basic syntax with its MIR safety checks and verified compiler self-use;
do not make deferred optimization acceptance a prerequisite for language work.

Follow `docs/repository-organization.md` for staged source and documentation
cleanup. Include root gate-numbered files and symbols, not just directories.
At accepted optimization checkpoints, advance the next bounded organization
slice or record its concrete blocker; do not defer all cleanup until promotion.
Keep the README concise and historical evidence immutable. Source moves must
retain their applicable code/recovery/measurement checks.

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
- Follow `docs/optimization-tradeoffs.md`: ordinary cost limits remain the
  default acceptance gate, while a preregistered candidate-specific diagnostic
  may measure runtime benefit despite a cost miss. Never infer merge approval
  from a diagnostic budget or rewrite historical failures. Preserve correctness,
  safety, self-hosting and full acceptance authorities.
- Track both a same-feature control and the frozen cumulative Native baseline;
  do not compound successive 5% allowances or infer current Go headroom from an
  older small-program snapshot. Report compiler and application costs separately.
- Remove superseded emitter ownership, but distinguish duplicate migration code
  from the justified cost of useful MIR passes. QBE text is a diagnostic signal,
  not a shipped artifact; its ordinary CI limit is unchanged. After two bounded
  size-only attempts without a current benefit assessment, explicitly reassess
  whether to measure the benefit, review the trade, or defer before continuing.
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
- Follow `docs/bootstrap-seed-updates.md` before using newly supported syntax
  in compiler implementation source. Refresh from accepted main when needed;
  retain immutable historical seeds and verify actual published assets before
  switching exact checkout pins. Do not use an unaccepted candidate as a seed
  or add a floating latest download to bypass this boundary.
