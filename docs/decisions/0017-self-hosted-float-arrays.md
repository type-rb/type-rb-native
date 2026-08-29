# Decision 0017: Self-hosted Float Arrays

## Status

Accepted for the Gate 6J experiment.

## Context

Gate 6I carries scalar binary64 values through the ordinary self-hosted
frontend, QBE emitter, and Darwin/Linux replacement chains. Numeric programs
still cannot retain those values in the existing homogeneous Array runtime.
The reference language supports `Array<Float>`, safe Integer element widening,
common numeric literal inference, and mutable indexed operations.

Configured-project parsing is now a credible next product slice, but closing
the Float collection gap first produces reusable language and runtime coverage
and a realistic memory-bound workload. It also tests whether the compact
Native runtime remains competitive with optimized Go once binary64 values move
through allocation, growth, indexing, mutation, and reduction rather than only
scalar registers.

## Decision

The self-hosted compiler accepts `Array<Float>` wherever its current bounded
Array subset accepts an element type. Contextual literals and non-empty literal
inference follow the reference language. Integer values widen explicitly to
Float within a fresh Float Array; mutable `Array<Integer>` and `Array<Float>`
remain invariant after construction.

Direct Float elements occupy the existing eight-byte cell width but use QBE
`d`, `loadd`, and `stored`. They never cross the existing `l` element helper.
A dedicated Float push path shares the TypeRB-owned Array header, allocation,
growth, bounds, and publication policy. Nested Arrays retain `l` reference
cells, including when their innermost payload is Float.

The registered surface includes parameters, results, locals, records,
aliasing, `size`, `push`, positive and negative indexing, indexed assignment,
and indexed compound arithmetic. The existing bounded two- and three-level
nested Array forms extend symmetrically to Float. No new method, syntax,
compiler-runtime adapter, snapshot field, Native MIR field, CLI behavior, or
project configuration is introduced.

## Consequences

Numeric applications can allocate and process homogeneous binary64 storage
through ordinary Native builds. Existing Integer, String, and nested reference
Array paths retain their representation and behavior. The new direct payload
path is portable across the registered QBE Darwin and Linux arm64 profiles.

Float formatting, predicates and explicit narrowing, exponentiation, math
packages, broader collection APIs, configured projects, package behavior,
incremental builds, tool discovery, source maps, and release seed policy remain
separate work. The larger compiler and generated workload are bounded by the
pre-registered correctness, Go-parity, compiler-regression, and size criteria
in [issue #74](https://github.com/type-rb/type-rb-native/issues/74).
