# Gate 6M Portable Benchmark-entry Primitives

Gate 6M implements the smallest existing portable TypeRB surface needed to run
deterministic numeric benchmark specifications through the ordinary
self-hosted Native application path. Its correctness and measurement boundary
is pre-registered in
[issue #113](https://github.com/type-rb/type-rb-native/issues/113), and its
internal package, runtime, and external-library choices are fixed by
[Decision 0021](decisions/0021-portable-benchmark-entry-primitives.md). The
current Linux arm64 linker recipe is fixed by
[Decision 0022](decisions/0022-linux-arm64-lld-linker.md).

## Status

Gate 6M is complete. The measured portable compiler/runtime slice is TypeRB
Native revision `97b3ac2aa1d88cbb7782602589ad70686593ddab`; the final evidence
tooling is revision `c326b52d4bb2ce72602a6e33839883c94fd30f1d`. The reviewed
[Darwin and Linux arm64 result](../results/2026-08-31-gate6m-portable-benchmark-entry-darwin-linux-arm64/README.md)
passes every registered correctness, fixed-point, process, performance,
memory, and size criterion.

The fixed compiler baseline is TypeRB Native main revision
`71495bbf18f0820891ea086104ca7da808bfd25f`. The semantic oracle is TypeRB
`0.4.3-dev` at revision
`2cf63e95b4fc1a92f6094e2c89c47fb75262adae`, as declared by the compatibility
manifest.

## Included portable surface

The slice includes only:

- bare `import trb/std/process`, optional aliasing of its `Process` root, and
  `Process.argv(): Array<String>`;
- strict `String#to_i()` over the complete portable Integer range;
- canonical base-10 `Integer#to_s()`;
- truncating, checked `Float#to_i()`; and
- bare `import trb/std/math`, optional aliasing of its `Math` root, and
  `Math.sqrt(Float): Float` with existing Integer widening.

`Process.argv()` excludes the executable name and returns a fresh managed
Array and fresh managed Strings on every call. Integer parsing accepts only a
complete ASCII decimal with an optional sign. Float narrowing rejects NaN,
infinity, and finite values outside TypeRB's portable Integer range.
`Math.sqrt` retains IEEE 754 binary64 behavior, including NaN for a negative
argument.

General package resolution, named standard-package members, environment
access, more math operations, Float formatting, benchmark-specific syntax,
automatic tool discovery, and a stable Native library ABI remain outside this
gate.

## Implementation boundary

The resolver maps the two exact package paths to private standard-package
identities instead of pretending that they are project files. The checker
accepts only the registered declaration-root calls. QBE emission uses the
existing managed runtime for process argument copies and String results, emits
conversion helpers only when referenced, and calls the external C ABI `sqrt`
symbol for square root.

Every Native-owned C-toolchain invocation supplies `-lm` explicitly. The
`linux-arm64-v0` profile additionally selects LLD through the supplied C
driver; `darwin-arm64-v0` retains its existing linker behavior. Formal
evidence must identify QBE, the C toolchain, the selected linker, libc, and
libm as external components and must observe LLD in the Linux process graph.
No Go package or generated-Go helper enters the ordinary Native application
path.

## Correctness evidence

The checked-in `corpus/gate6m` sources are shared with the pinned optimized Go
backend. The successful application covers real arguments, repeated
`Process.argv()` freshness, zero and signed zero, both portable Integer
boundaries, canonical formatting, Integer widening, square root, negative
square-root NaN, and finite truncation. The failure application covers invalid
and sign-only decimal input, parsed Integer overflow, NaN, infinity, and finite
Float overflow.

Go and Native must produce byte-identical successful stdout. Each failure must
be nonzero in both implementations and retain the same runtime-failure class;
backend-specific stack text and exact nonzero status may differ. Unsupported
packages, members, arities, and types also require deterministic compiler
diagnostics.

Existing valid, invalid, mutation, configured-project, Float, Float Array, and
managed-runtime tests remain mandatory. Candidate B2, B3, and B4 compilers and
their target-neutral QBE must converge exactly on Darwin arm64 and Linux arm64
after explicitly recorded Go-free setup transitions from the immutable
previous-Native seed. Go and the reference compiler are prohibited from the
ordinary candidate chain.

## Registered measurements

Two warmups and seven alternating observations compare the candidate canonical
compiler with the fixed Native baseline. Two warmups and at least eleven
alternating observations compare the same successful TypeRB workload built by
Native and the pinned optimized Go backend.

The candidate compiler's median time and peak RSS may be at most 15% above the
baseline. Each target compiler asset may be at most 310,000 bytes and their
combined size at most 620,000 bytes. Native application build time, build peak
RSS, runtime, and runtime peak RSS must remain within 25% of optimized Go, and
the stripped Native application must be at least 80% smaller. Adjacent Native
generation medians must remain within 25%. A greater-than-2x primary-metric
regression is catastrophic.

Formal evidence records raw observations, exact source and artifact hashes,
fixed points, commands, compiler and tool versions, target inspection,
external dependencies, process boundaries, and intermediate cleanup. Gate 6M
claims capability and non-inferiority only; cross-language benchmark results
remain a later independently registered experiment.

## Result

The successful formal
[run 33321032161](https://github.com/type-rb/type-rb-native/actions/runs/33321032161)
closed exact candidate B2/B3/B4 fixed points on both targets. The candidate
compiler is 299,576 bytes on Darwin and 274,144 bytes on Linux; the
573,720-byte total is below the 620,000-byte bound. Against the fixed Darwin
compiler baseline, candidate build time is 7.93% higher and peak RSS is 13.77%
higher, both below the 15% ceiling.

On the identical portable TypeRB workload, Native build time is 59.23% lower,
build peak RSS is 46.81% lower, runtime is 28.89% lower, and runtime peak RSS
is 71.54% lower than optimized Go. The stripped Native application is 98.19%
smaller on Darwin and 99.15% smaller on Linux. The Linux process evidence
observes the explicit LLD and dynamic libm boundaries. Detailed measurements,
correction history, and all retained raw artifacts are in the
[recorded result](../results/2026-08-31-gate6m-portable-benchmark-entry-darwin-linux-arm64/README.md).

The TypeRB-authored
[Gate 6M benchmark controller](../tools/gate6m-benchmark/README.md) owns the
Darwin fixed-point, differential, timing, RSS, size, dependency, and process
inventory procedure. The manually dispatched
[formal Gate 6M workflow](../.github/workflows/gate6m-formal.yml) runs that
controller on `macos-15`, runs the separate
[Linux arm64 verifier](../tools/gate6m-linux.sh) on `ubuntu-24.04-arm`, and
enforces the combined target-size bound. The workflow and verifier remain
pinned to the registered candidate, TypeRB oracle, QBE source release, and
immutable previous-Native seed. The reviewed successful artifacts are retained
with the recorded result rather than relying on the workflow status alone.
