# Gate 6H Scalable File-root Module Graph

Gate 6H expands the existing real file-root path from a representative
five-module application to a deterministic 1,025-file closure. Its exact
correctness and measurement boundary is pre-registered in
[issue #64](https://github.com/type-rb/type-rb-native/issues/64), and its
ownership model is defined by
[Decision 0015](decisions/0015-indexed-module-graph.md).

## Status

Complete at measured revision
`e39f774237a6306d7cd46b09941367c42816c628`. The reviewed Darwin and pinned
Linux arm64 evidence is retained in the
[Gate 6H result](../results/2026-08-29-gate6h-module-graph-darwin-linux-arm64/README.md).

On the exact 1,025-file closure, direct checking improves by 41.96%, direct QBE
emission by 39.92%, and the complete Native build by 16.16%. Median scale RSS
falls by 48.50%, 40.04%, and 0.18% respectively. Canonical compiler guards,
exact replacement, optimized-Go comparison, application size and identity,
and pinned Linux arm64 correctness all pass.

## Indexed graph boundary

Source-ordered module and import arrays remain canonical. Module addition
maintains a deterministic internal name index, rebuilding only when the
power-of-two bucket count grows. Full String comparison preserves exact lookup
under same-length collisions, and head insertion preserves the previous last
match for duplicate internal input.

Parsing records each module's contiguous import start and count. File-root
loading and cycle reachability traverse those spans rather than repeatedly
scanning all imports. Newly discovered targets skip a vacuous reachability
walk, while existing-target walks retain local visited state and follow only
owned edges. Import binding lookup and duplicate validation use the same span;
declaration duplicate scans stop at the preceding module boundary because
module declarations are contiguous. A private bounded rolling bucket
distributes fixed-width module names; the independently measured Gate 6G
function bucket remains unchanged. Frequency-ordered ASCII lexer tables reduce
the remaining source scan without changing their accepted character sets.

All of these changes are ordinary TypeRB source. Gate 6H adds no
compiler-private runtime adapter and does not change emitted runtime policy.
The structures add no public Hash or String API, snapshot field, Native MIR
instruction, package intrinsic, syntax, or CLI behavior.

## Correctness boundary

Permanent evidence covers:

- empty lookup, same-length collisions, duplicates, missing names, and the
  deterministic index growth boundary;
- zero-, one-, and multiple-import spans;
- a generated 64-module predecessor chain during ordinary CI and a
  1,024-imported-module chain during formal measurement;
- direct-file precedence, index fallback, shared dependencies, unrelated
  siblings, module-local names, and direct and deep cycles;
- the complete valid, invalid, mutation, build-failure, file-root, Darwin, and
  Linux-profile corpus;
- exact candidate B2/B3/B4 bytes and QBE, representative application identity,
  and no leaked Native intermediates; and
- matching optimized-Go and Native behavior for the scale application.

## Registered measurement

Gate 6G at main revision
`0796e39558f6c28995c9b4c03defded4b4bd6123` is the fixed baseline. The same
Gate 6G fixed-point seed, QBE 1.3, system CC, output basename, cache policy,
and alternating order are used for baseline and candidate. Two warmups precede
eleven observations per candidate.

On the generated 1,025-file closure:

- direct `check` median time must improve by at least 35%;
- direct `emit-qbe` median time must improve by at least 25%;
- complete Native `build` median time must improve by at least 10%;
- candidate median peak RSS must remain within 10% for each operation;
- QBE and repeated candidate executable bytes must remain exact;
- candidate Native build time and RSS must remain within 25% of pinned
  optimized Go; and
- the stripped Native application must remain at least 80% smaller than the
  optimized Go application with matching behavior.

Canonical compiler direct emission and full build must remain within 5% of the
registered Gate 6G time and RSS medians. The candidate compiler must strip to
at most 208,530 bytes and retain exact replacement generations and the Gate 6E
application. The pinned Gate 6D Linux arm64 image closes a correctness-only
compiler chain and runs both representative and scale applications.

Formal evidence records raw observations, generator and graph hashes, exact
commands, source and artifact identities, seed provenance, file counts,
process and dependency boundaries, retained tools, and cleanup.

## Deferred scope

Configured projects, packages, namespace imports, public Hash and module
identity, incremental caching, a stable CLI, automatic tool discovery, source
maps, release seed policy, and further compiler decomposition remain separate
slices.
