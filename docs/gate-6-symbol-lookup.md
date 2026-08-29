# Gate 6G Self-hosted Symbol Lookup

Gate 6G restores compiler-build headroom by removing quadratic direct-function
lookup from the self-hosted frontend. Its exact correctness and measurement
boundary is pre-registered in
[issue #59](https://github.com/type-rb/type-rb-native/issues/59), and the
internal ownership model is defined by
[Decision 0014](decisions/0014-indexed-function-lookup.md).

## Status

Complete at measured revision
`8bcc2a6e1c5ecede5f07c2dda63a4d4d82631375`. The formal Darwin and pinned
Linux arm64 evidence is retained in the
[Gate 6G result](../results/2026-08-29-gate6g-symbol-lookup-darwin-linux-arm64/README.md).

Canonical direct QBE emission improves by 30.80%, the complete compiler build
improves by 5.95%, and 6,000-function direct QBE emission improves by 53.49%.
The respective registered minimums were 5%, 3%, and 25%. Median RSS changes by
+1.31%, 0.00%, and +0.12%; the candidate strips to 200,008 bytes; exact Darwin
and Linux replacement chains pass; and the representative application retains
exact bytes and behavior.

## Indexed boundary

The parser retains source-ordered declaration arrays. Immediately before
resolution, it derives a deterministic module-qualified function index backed
by demand-sized TypeRB storage. Source-order insertion and head linking preserve
the previous last-match behavior; full module and String comparisons preserve
correctness under bucket collisions.

The index is compiler-internal. It does not add a public Hash, a String hash
intrinsic, a snapshot or Native MIR field, new syntax, or CLI behavior. Records,
imports, fields, modules, and locals remain canonical-array data and retain
their existing observable behavior.

The lexer also stops bounded character-set membership at the first exact
match. The checked-in ASCII identifier sets, tokenization, and diagnostics are
unchanged; only the already-determined suffix scan is removed. This lookup is
kept as a direct scan rather than acquiring persistent index state.

## Correctness boundary

Permanent tests cover:

- deterministic bucket sizing across its growth boundary;
- same-length collisions, duplicate names, module qualification, and missing
  names;
- successful and missing bounded character-set membership;
- the exact last-match behavior of every existing lookup family;
- a generated 128-function chain in ordinary tests and a 6,000-function chain
  in formal measurement;
- the complete valid, invalid, mutation, file-root, and build-failure corpus;
  and
- exact B2/B3/B4 bytes, application identity, and Darwin/Linux arm64 behavior.

## Registered measurement

The Gate 6F measured compiler and source are the fixed baseline. Two warmups
precede eleven alternating observations of baseline and candidate on the same
Darwin arm64 host, QBE 1.3, system CC, seed, output basename, and cache policy.

- canonical direct `emit-qbe` median time must improve by at least 5%;
- canonical end-to-end `build` median time must improve by at least 3%, with
  candidate peak RSS within 5%;
- 6,000-function direct `emit-qbe` median time must improve by at least 25%,
  retain byte-identical QBE, and keep peak RSS within 10%;
- the stripped candidate compiler must remain at or below 208,530 bytes; and
- the representative Gate 6E application must retain exact bytes and behavior.

The pinned Gate 6D Linux arm64 image closes a correctness-only B1-to-B4 chain
and rebuilds the representative application. Formal evidence records raw
observations, exact source and artifact hashes, seed provenance, process and
dependency boundaries, and retained external tools.

## Deferred scope

Gate 6H separately registers a private TypeRB-authored rolling bucket for its
compiler-internal module index; the Gate 6G function bucket remains unchanged.
Public Hash and String hash semantics, configured projects, packages,
incremental builds, tool discovery, source maps, release seed policy, and
further compiler decomposition remain separate slices.
