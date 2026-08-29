# Decision 0016: Self-hosted Float scalar path

## Status

Accepted for the Gate 6I experiment.

## Context

The ordinary self-hosted compiler supports the Integer, Boolean, String,
Array, and record subset needed to reproduce itself, but it still rejects
`Float`. The lower Native MIR and QBE path already established binary64 scalar
operations in Gate 1. The missing boundary is now the real TypeRB-authored
lexer, checker, emitter, file command, and replacement chain rather than QBE
feasibility.

Configured-project parsing would widen product policy before the compiler can
handle one of TypeRB's existing scalar types. Adding Float is reusable language
coverage and also creates a numeric runtime workload that can be compared with
the optimized Go backend without adding a Native-only syntax or runtime API.

## Decision

The self-hosted source frontend accepts the reference grammar's decimal Float
literals and treats `Float` as IEEE 754 binary64. Source literals remain finite;
underflow rounds to signed zero, while runtime division and arithmetic may
produce infinity and NaN. Unary and binary operators, comparisons, calls,
locals, returns, and record fields follow the existing TypeRB specification.

Integer-to-Float widening is explicit in emitted QBE at every accepted typed
boundary. QBE `d` values use `sltof`, `loadd`, `stored`, `d` parameters and
results, and floating arithmetic and comparison instructions. A Float never
travels through the compiler's existing `l` value convention merely because
both representations occupy eight bytes.

The compiler continues to retain source text for a numeric literal until QBE
emission. Its TypeRB-authored validator decides whether the positive decimal
magnitude can round to a finite binary64 value; QBE is not invoked to validate
`check` input. Unary negation emits a binary64 sign-correct operation, including
negative zero.

The first slice does not add `Array<Float>`, Float formatting, predicates,
explicit narrowing, exponentiation, or math packages. Those need separate
runtime and library boundaries. Their absence is an explicit incomplete
compiler surface, not an alternative TypeRB meaning.

## Consequences

Float applications can pass through the ordinary file-oriented Native build,
Darwin and Linux arm64 target profiles, and Native-to-Native replacement chain.
The feature uses QBE instructions rather than a compiler-private runtime
adapter and does not change external tool discovery, target selection, project
configuration, package behavior, or TypeRB's reference repository.

Every existing non-Float input must retain its behavior and application bytes.
The larger self-hosted compiler is bounded by the pre-registered canonical
time, RSS, and stripped-size guardrails in
[issue #69](https://github.com/type-rb/type-rb-native/issues/69).

