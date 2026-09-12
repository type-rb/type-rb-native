# Compiler recovery and bootstrap changes

Read for changes to ordinary compiler source (including moves), recovery,
self-hosting, or seed distribution. Paths below are repository-relative.
Use `docs/compiler-project-layout.md` when source paths or cross-revision
consumers move. Use `docs/bootstrap-seed-updates.md` for a seed refresh or before
compiler self-use adopts syntax beyond the verified checkout seed.

- For self-hosting checks, require runtime-supplied source to pass through the
  checked-in lexer, parser, resolver, checker, and emitter. Reject embedded
  compiler artifacts, source-specific output paths, quines, and hidden host
  fallbacks as bootstrap evidence.
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

## Required compiler-source verification

For compiler-source changes, also enable the recovery and QBE-backed tests:
set `TYPE_RB_NATIVE_REFERENCE_TRB` to the absolute pinned compiler executable
and `TYPE_RB_NATIVE_QBE` to QBE 1.3, together with `TYPE_RB_NATIVE_ROOT`, when
running the root and `compiler` suites. Without those variables, optional
tests report success without exercising recovery; do not count that as complete
bootstrap verification. The recovery snapshot supports a narrower source subset
than the ordinary Native compiler, so ordinary fixed points alone are not a
substitute. See the environment in `.github/workflows/native-validation.yml`.

Treat a published bootstrap tag, release, and asset set as immutable. Keep a
release-integrity re-verification pinned to the release source and fixtures,
and record the exact verifier revision separately. For a later source
compatibility revalidation, verify that immutable seed and its provenance
before execution, then record the newer compiler-source revision and resulting
fixed-point identity separately from the seed's source-era root and compiler
identity. Never replace or relabel the seed merely to align revisions.
