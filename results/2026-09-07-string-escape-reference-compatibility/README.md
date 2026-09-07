# Current reference compatibility

The current development pin is TypeRB `0.4.6-dev` at
`6d130b3cd89044d4f54cc983555e0a3d340793c7`, the merged
[short-circuit snapshot-condition correction](https://github.com/type-rb/type-rb/pull/653).
Snapshot v3/v4 lower logical `if`/`while` condition trees through ordinary
branches while preserving short-circuit evaluation. General logical values
and call arguments remain outside that recovery subset; this does not change
the ordinary Native language boundary.

The Native compiler implementation is unchanged from accepted
`d8fb20925e8eade09ea964c0f0c574083f68684b`. Its independent
[checkout CLI verification](https://github.com/type-rb/type-rb-native/actions/runs/34114320082)
passed Darwin/Linux arm64 with the Sep7 seed. That workflow verifies the
unchanged Native executable chain, **not** the new reference revision.
The reference-pin PR separately requires fresh recovery-enabled root/compiler
tests, exact-reference compatibility validation and every applicable hosted
acceptance authority before merge. This is not evidence for adopting the
pending Array-loop optimization or expanding a compatibility range.

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
