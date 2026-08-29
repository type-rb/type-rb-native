# Gate 6G Self-hosted Symbol Lookup

Gate 6G restores compiler-build headroom by removing quadratic direct-function
lookup from the self-hosted frontend. Its exact correctness and measurement
boundary is pre-registered in
[issue #59](https://github.com/type-rb/type-rb-native/issues/59), and the
internal ownership model is defined by
[Decision 0014](decisions/0014-indexed-function-lookup.md).

## Status

Implementation is in progress. Formal results are not yet recorded and none of
the registered thresholds may be inferred from diagnostic runs.

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

## Correctness boundary

Permanent tests cover:

- deterministic bucket sizing across its growth boundary;
- same-length collisions, duplicate names, module qualification, and missing
  names;
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

Public Hash semantics, a stronger String hash, configured projects, packages,
incremental builds, tool discovery, source maps, release seed policy, and
further compiler decomposition remain separate slices.
