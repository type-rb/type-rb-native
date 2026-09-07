# Current reference compatibility

The current development pin is TypeRB `0.4.6-dev` at
`f6229c5657a5acb40194cde71785a63754d00355`, the merged
[statement conditional snapshot correction](https://github.com/type-rb/type-rb/pull/655).
Snapshot v3/v4 encode ordered `elsif` conditions with existing control flow;
conditional expressions and the v2 subset remain unchanged. The new
`elsif-recovery` regression exercises snapshot encoding, strict decoding,
recovery emission and execution, plus ordinary current compiler generations.

The Native implementation remains accepted
`21f507e7ee7de2577f4137f6dfb9f732c14c1640` from PR #329.
[Exact-head acceptance](https://github.com/type-rb/type-rb-native/actions/runs/34153242015)
passed recovery, ordinary CLI, both target/cost/memory comparisons and combined
size at the preceding reference pin. It does not establish acceptance of the
new reference by itself. This update requires fresh recovery-enabled suites
and every applicable hosted authority before merge. Seed preparation does not
mean a new seed has been published, verified or selected by checkout builds.

The preceding logical-condition reference pin was
`6d130b3cd89044d4f54cc983555e0a3d340793c7` from
[TypeRB PR #653](https://github.com/type-rb/type-rb/pull/653).
Its [source-era compatibility record](https://github.com/type-rb/type-rb-native/blob/21f507e7ee7de2577f4137f6dfb9f732c14c1640/results/2026-09-07-string-escape-reference-compatibility/README.md)
remains available at the exact accepted revision.

## Previous String-escape checkpoint

The preceding experimental update selected TypeRB `0.4.6-dev` at
`47a160cae05ddc2035c7430735c4762d36bbc9c4`, the source revision of
[TypeRB PR #651](https://github.com/type-rb/type-rb/pull/651).
The dependent Native update requires that reference PR to merge first.

Native implementation `07fc9af5e4d8b099865297820068140222ade47e` passed
[Native CLI workflow 34081476080](https://github.com/type-rb/type-rb-native/actions/runs/34081476080)
on Darwin arm64 and Linux arm64. Both jobs build from the unchanged pinned
Native seed, verify core and CLI fixed points, run CLI and typed REPL cases,
exercise escape and interpolation errors, render terminal editing and history,
and verify unchanged checkout inputs reuse the executable.

Local Darwin arm64 checks with the exact selected reference also pass:

- reference checks for the root, compiler and isolated CLI source projects;
- String escape and interpolation file/REPL differential tests;
- shared reference/Native REPL screen and history tests.

The implementation accepts escaped hashes in source while keeping JSON history
validation separate. The new reference requires typed filesystem paths and
immutable record fields; adapters construct `Path` values and CLI state uses
mutable Array elements or replacement session records.

This is bounded source, String and CLI compatibility evidence. It is not a
version range, complete language conformance claim or performance measurement.
Full recovery, target, memory and performance checks on the final PR revision
remain the required acceptance authorities. Published bootstrap assets and
previous measurement contracts retain their original revisions.

The [previous compatibility record](https://github.com/type-rb/type-rb-native/blob/5cf61c740aa600c34ed94f1b130ea2ffefd9e783/results/2026-08-31-typerb-0-4-4-compatibility-darwin-linux-arm64/README.md)
remains available at its exact archived revision.
