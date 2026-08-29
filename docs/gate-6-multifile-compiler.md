# Gate 6F Multi-file Self-hosted Compiler

Gate 6F applies the Gate 6E file-root loader to the compiler itself. Its exact
correctness and measurement boundary is pre-registered in
[issue #55](https://github.com/type-rb/type-rb-native/issues/55), and source
ownership is defined by
[Decision 0013](decisions/0013-multi-file-self-hosted-compiler.md).

## Status

Gate 6F is complete at measured revision
`7cb7e85c0b5bff14157dc1a686829c010d095b70`. The canonical compiler is a
three-module TypeRB closure, and ordinary B2/B3/B4 executables are
byte-identical on Darwin and pinned Linux arm64. Darwin multi-file median time
is 0.712012 seconds, 21.56% above the Gate 6C baseline and 0.37% faster than the
temporary flat source; median RSS is 36,716,544 bytes, and both compilers strip
to 199,992 bytes. The Gate 6E application retains exact bytes and behavior.
See the [TypeRB-authored benchmark controller](../tools/gate6f-benchmark/README.md)
and [recorded result](../results/2026-08-29-gate6f-multifile-compiler-darwin-linux-arm64/README.md).

## Compiler closure

`compiler/gate4/src/compiler.trb` remains the entry. It explicitly imports
chunked storage records and helpers from `storage.trb` and pure path helpers
from `path.trb`. The split moves declarations without changing frontend,
runtime, emitter, optimization, command, or target behavior.

Permanent tests run the complete compiler closure through the pinned reference
snapshot and through the self-hosted parser, resolver, checker, emitter, and
ordinary build command. Independent mutations to storage and path sources must
change compiler QBE. Missing and malformed compiler modules must fail before
QBE or CC, while an invalid unrelated sibling must stay outside the closure.

## Recovery and ordinary ownership

Recovery derives a temporary flat equivalent from the three canonical inputs
only to prepare B1 for the hidden single-source adapter. The derivation checks
the exact import boundary and is not stored in the repository.

```text
pinned reference snapshot of real closure -> B0
B0 + temporary flat recovery source       -> B1 seed

B1 build compiler.trb closure -> B2/compiler
B2 build compiler.trb closure -> B3/compiler
B3 build compiler.trb closure -> B4/compiler
```

Only the last three commands form the ordinary chain. They use explicit QBE
and CC paths, load the real TypeRB module graph, and must produce exact B2/B3/B4
QBE and executable bytes.

## Registered measurement

Darwin arm64 keeps the existing absolute compiler bounds: median B1-to-B2
build time and peak RSS must remain within 25% of 0.585709 seconds and
36,667,392 bytes. Two warmups and seven alternating observations also compare
the multi-file source with its mechanically equivalent temporary flat source;
multi-file time and RSS must remain within 10% of the stronger flat result.

The stripped compiler remains capped at 208,530 bytes and at 5% over the flat
equivalent. The Gate 6E representative application must retain exact behavior
and bytes. One correctness run in the pinned Gate 6D Linux arm64 image must
rebuild both the multi-file compiler fixed point and that application.

## Deferred scope

Further compiler decomposition, configured projects, public module identity,
packages, standard-library Native imports, incremental builds, tool discovery,
source maps, and release seed policy remain separate slices.
