# Decision 0021: Portable Benchmark-entry Primitives

## Status

Accepted for the Gate 6M experiment.

## Context

The ordinary self-hosted compiler can build explicit configured projects with
portable Integer, Float, String, Array, and record operations. Deterministic
numeric benchmark programs still cannot receive their input from the process,
render an Integer result, explicitly narrow a computed Float, or call the
portable square-root operation. These are existing TypeRB language and
standard-library contracts, not benchmark-specific behavior.

The reference compiler already defines bare declaration-root imports for
`trb/std/process` and `trb/std/math`, fresh `Process.argv()` results, strict
String-to-Integer conversion, canonical Integer text, checked Float narrowing,
and binary64 square root. Native must implement that behavior without making
its package representation, runtime operations, or external-library choices
part of TypeRB's public surface.

## Decision

The self-hosted resolver recognizes exactly the bare package imports
`trb/std/process` and `trb/std/math` in this slice. It creates their existing
`Process` and `Math` declaration-root bindings, including an explicit source
alias. Internal negative module identities distinguish these compiler-owned
packages from project modules. Those identities are private implementation
details; no package file, serialized format, Native-only import spelling, or
reference-repository hook is introduced.

The checker exposes only `Process.argv()` and `Math.sqrt(Float)`. Existing
Integer-to-Float widening applies to `Math.sqrt`. Unsupported package paths,
named package imports, members, arities, and receiver or argument types fail
deterministically rather than falling through to an external symbol.

`Process.argv()` copies C `argv[1...]` into a newly allocated managed
`Array<String>` on every call. The executable name is omitted. Both the Array
and every String use the existing exact-root collector and managed Array
representation; the host argument vector is retained only as two scalar
process-entry values.

The TypeRB-owned runtime implements complete ASCII `[+-]?[0-9]+` validation,
portable-range accumulation, canonical base-10 Integer formatting, and Float
truncation toward zero. Float narrowing rejects NaN and both infinities before
the portable Integer range check. These related helper bodies form one
conditionally emitted runtime slice: using any registered conversion or
process primitive includes the slice, while unrelated applications omit it
entirely. This keeps feature selection compact inside the self-hosted compiler
without enlarging its baseline runtime.

`Math.sqrt` lowers to the platform C ABI `sqrt` symbol with a binary64
argument and result. Native-owned C-toolchain invocations pass `-lm`
explicitly on both registered target profiles. The system math library is
therefore an external dependency recorded in build and distribution evidence;
it is not hidden inside a TypeRB package or reimplemented with different
semantics. The link flag is supplied consistently even for programs whose
conditionally emitted QBE does not reference `sqrt`.

## Consequences

One portable TypeRB source can receive conventional benchmark parameters and
produce deterministic integer output through both the optimized Go backend
and the ordinary Native build path. Numeric kernels can use the existing
binary64 square-root contract while retaining TypeRB's exact Integer boundary
and runtime-failure classes.

The self-hosted frontend remains intentionally incomplete. This decision does
not add general package loading, member imports, environment access, Float
formatting, additional math functions, benchmark-specific APIs, automatic
tool discovery, or stable runtime and linker ABIs. The exact correctness,
fixed-point, performance, memory, and size requirements remain pre-registered
in [issue #113](https://github.com/type-rb/type-rb-native/issues/113).
