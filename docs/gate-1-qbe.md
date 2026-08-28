# Gate 1 QBE Vertical Slice

Gate 1 tests whether a TypeRB-authored, heap-free scalar pipeline can produce a
correct native executable cheaply enough to justify connecting it to the
reference frontend. It is an experimental checkpoint, not a supported TypeRB
target or a measurement of the final self-hosted compiler.

## Current pipeline

```text
snapshot v2 JSON
  -> strict TypeRB decoder
  -> verified Gate 1 Native MIR
  -> TypeRB QBE emitter
  -> QBE 1.3 (`arm64_apple`)
  -> system assembler and linker
  -> Darwin arm64 executable
```

The repository owns the decoder, MIR, verifier, QBE lowering, scalar runtime,
and toolchain driver. QBE and the system C toolchain are external dependencies
and must be counted in build and distribution measurements.

## Pinned backend

- QBE release: `1.3`
- release commit: `c0818978acec60ebb6167fade60fb7012cbf20ca`
- release archive SHA-256:
  `d587905d620dc5e1d2bfa7c2cc642b9b837aa89a3188c6e37b53d756cf66e320`
- QBE target: `arm64_apple`
- experimental ABI profile: `darwin-arm64-v0`

The ABI profile is disposable and internal. It may change without an adapter.

## Snapshot v2

Snapshot v2 keeps the Gate 0 envelope and adds `entryFunction`. A function has
`id`, `name`, `parameters`, `result`, `entry`, `origin`, and `blocks`. A block
has `id`, `parameters`, `origin`, `instructions`, and one separate
`terminator`.

Supported scalar types are `Void`, `Boolean`, `Integer`, and `Float`. `Void` is
valid only as a function result. The selected entry function takes no
parameters and returns `Void`. This is an internal executable convention; it
does not add `def main(): Integer` or otherwise change the TypeRB source
contract.

Supported instructions are:

- `boolean_literal`, `integer_literal`, and `float_literal`;
- `integer_binary` with `add`, `subtract`, `multiply`, `divide`, or `remainder`;
- `float_binary` with `add`, `subtract`, `multiply`, or `divide`;
- `integer_compare` and `float_compare` with the six ordered comparison names;
- `boolean_not`;
- `call` with a nullable result and direct function identifier; and
- `write_static` for heap-free UTF-8 output.

Supported terminators are `jump`, `branch`, and `return`. Jump and branch edges
carry typed block arguments. Unknown fields and operations fail explicitly,
and the decoder applies resource limits before code generation.

## Scalar semantics

Portable Integer values remain within `-9007199254740991` through
`9007199254740991`. Arithmetic is checked before an out-of-range result can be
observed. Divide-by-zero, remainder-by-zero, and range failures write a fixed
diagnostic to standard error and exit with status 70 in this temporary runtime.
The exact failure text remains experimental until the source-connected
differential corpus establishes the reference behavior.

Boolean values use QBE words, Integer values use QBE longs, and Float values
use QBE doubles. Non-entry block parameters are lowered through typed stack
slots so the initial emitter does not depend on backend-specific SSA phi
construction. Static UTF-8 output is emitted as QBE data and written without a
heap allocation.

Every MIR origin is emitted as a deterministic QBE comment containing the
source-table index and span. Runtime source traces are outside Gate 1.

## Toolchain workspace

`build_gate1_executable` writes `module.ssa` and `module.s` into a caller-owned
workspace and writes the executable to the requested output path. The caller
owns cleanup. Tests use gate-specific directories under `/tmp`; automation and
benchmark scripts must remove those exact directories after collecting
artifacts.

## Gate 1B deletion condition

The reference snapshot producer is temporary. Remove it when the native
TypeRB-authored frontend produces the same verified MIR corpus, or when the
native experiment is abandoned. It must remain process-based and data-only and
must not expose Go compiler objects as an API.

Records, tagged values, dynamic strings, arrays, allocation, garbage
collection, a stable ABI, and additional targets begin no earlier than Gate 2.
