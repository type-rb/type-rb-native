# Persistent worker memory lifecycle harness

This harness verifies the ordinary self-hosted Native compiler and the managed
runtime against the persistent-process criteria registered in
[issue #150](https://github.com/type-rb/type-rb-native/issues/150). It does not
introduce a public worker API or Native-only TypeRB source behavior.

`workload.trb` is the single authored source for both Native and optimized Go
executables. A persistent state retains a bounded 64-entry recent-payload
cache. Every batch starts with 128 dynamic jobs and deterministically completes
with 112 successes (including eight retry successes), eight retries, eight
terminal failures, eight cancellations, and 136 processed attempts. Retry
handling appends a dynamic payload and attempt to parallel Arrays. The harness
derives smaller inputs only by replacing the one registered invocation; it
never duplicates or generates the workload body.

The harness has four modes:

- `smoke` runs 40,000 batches in one phase, compares exact Native and Go
  output, and checks collector accounting, the 4 MiB managed-heap bound, and
  the sampled internal trace;
- `formal` runs 60 phases of 120,000 batches on Linux arm64, allocating exactly
  32,832,000,576 managed bytes after literal-only String concatenation has
  moved out of the runtime. It samples Native and Go RSS, descriptors, and
  threads every 250 ms. Native RSS must remain below 64 MiB, temporal-quartile
  growth below 8 MiB, fitted growth below 1 MiB per minute, and post-warmup
  descriptor and thread counts must not grow;
- `asan` links a 400-batch Linux arm64 oracle with Clang ASan/LSan; and
- `valgrind` runs that oracle under Memcheck with every leak class visible.

`TYPE_RB_NATIVE_RUNTIME_TRACE` is an internal evidence switch, read once at
startup. It does not change normal output or the existing runtime-stats v1
format. When enabled, every 64th automatic collection and the final manual
collection report the collection number, role, post-sweep live bytes, next
target, logical-root count, and root capacity. The analyzer requires complete
ordered observations, a fixed 64-word root capacity, at most 128 KiB live at
sampled automatic collections, and zero live bytes and roots after the final
manual collection. Formal evidence must contain at least 400 observations.

All modes require a current self-hosted Native compiler, QBE 1.3, a system C
driver, a target profile, and fresh workspace and evidence paths. Smoke and
formal modes also require the pinned reference TypeRB compiler:

```text
/bin/sh tools/runtime-worker-soak/runtime-worker-soak.sh \
  smoke COMPILER QBE CC REFERENCE_TRB darwin-arm64-v0 WORKSPACE EVIDENCE
```

The CI workflow runs smoke on Darwin and Linux arm64, proves an adjacent Native
compiler fixed point, compares target-neutral compiler and workload QBE across
targets, and enforces the structural Native MIR transition limits from
`tools/native-mir-transition-policy.sh`. The current combined stripped-compiler
ceiling is 574,000 bytes. Its 17,000-byte-per-target allowance is temporary and
must be recovered when portable range, index, and induction ownership has moved
out of the direct emitter, before the next portable fact family begins. A
manual formal run additionally executes the sanitizer, Memcheck, and long-lived
Linux process oracles. Every Linux setup and ordinary compiler generation is
process-traced; the verifier requires the exact Native compiler, QBE, C driver,
assembler, `collect2`, and registered linker paths. Setup transitions may use
the published seed's system linker, while every B2/B3/B4 generation requires
LLD. The verifier rejects any other successful executable and rejects Go,
reference TypeRB, shell, recovery-generator, and hidden source-content paths.
Compiler build/RSS comparison with current main remains the responsibility of
the companion static-compactness workflow whenever the compiler source changes.
