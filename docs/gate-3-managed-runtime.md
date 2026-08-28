# Gate 3 Managed Runtime

Gate 3 establishes the first cyclic managed-reference graph in the native
pipeline. The registered work and thresholds live in
[issue #13](https://github.com/type-rb/type-rb-native/issues/13); this document
defines the implementation boundary used to satisfy them.

## Implementation status

Gate 3 is complete. The pinned reference compiler produces version 4 snapshots
for all four registered workloads and the two bounds-failure cases. The native
decoder, verifier, exact-root runtime, QBE emitter, and linker path match the
optimized Go executable in stdout, stderr, and exit status. Repeated runs
reproduce byte-identical snapshots, QBE IL, assembly, and executables, while
decoded MIR values compare structurally equal.

The QBE adapter uses one closure-call ABI for both capturing and zero-capture
function bodies. Direct calls to a body that is also used as a closure supply a
null environment, while indirect calls supply the closure's environment. This
keeps ordinary direct calls compact without misaligning authored parameters.

The registered source cycle crosses the normal allocation threshold repeatedly,
reclaims its unreachable closure/Array graphs, and finishes within the live-set
bound. A TypeRB-authored benchmark harness records the build phases, executable
sizes, peak RSS, steady-state runtimes, and collector statistics without
changing source-visible behavior.

All registered correctness, automatic-collection, size, build-time, runtime,
and peak-RSS bounds pass in the
[dated Darwin arm64 result](../results/2026-08-28-gate3-qbe-darwin-arm64/README.md).

## Reference producer pin

`TYPE_RB_REVISION` pins TypeRB commit
`fa9e0503cc681bcaa691f6f11d2f1e19ca8e6453`, which provides the
consumer-neutral version 4 bootstrap snapshot producer. The integration command
owned by this repository is:

```sh
trb compiler bootstrap-snapshot --snapshot-version 4 --config trbconfig.jsonc
```

Version 4 maps to the managed Gate 3 Native MIR described below. That mapping,
the QBE ABI, runtime policy, compatibility expectations, and performance gates
belong only to this repository. The producer remains data-only and contains no
Native MIR layout or backend detail. Remove the version 4 producer once the
self-hosted TypeRB frontend emits equivalent verified Native MIR and no other
consumer requires the snapshot.

## Supported source subset

Gate 3 retains every Gate 2 feature and adds:

- first-class dynamic UTF-8 `String` values;
- String concatenation, equality, code-point `size`, indexed access, and
  dynamic `puts`;
- mutable `Array<Integer>`, `Array<String>`, closure-Array, and recursively
  nested Array literals, reads, writes, growth, `size`, and `push`;
- first-class positional function values, immutable lexical captures, managed
  captures, and indirect calls; and
- records and tagged values whose fields recursively contain the supported
  managed values.

Captured mutable reference values may be mutated through their ordinary
receiver operations. Assignment to a captured lexical binding is deferred with
mutable capture cells. Hash, classes, interfaces, Bytes, StringBuilder,
concurrency, module initialization, and broad standard-library adapters remain
outside this gate.

## Snapshot version 4

Version 4 keeps the existing envelope, source table, origin shape, blocks, and
terminators. Every collection remains an array even when empty. Unknown fields
and operations are rejected.

Type definitions add three target-neutral kinds:

```json
{"kind":"string","id":"String"}
{"kind":"array","id":"Array<Integer>","element":"Integer"}
{"kind":"function","id":"() -> Void","parameters":[],"result":"Void"}
```

Record fields, tagged payloads, parameters, results, and block parameters refer
to these canonical identifiers. Snapshot data does not include byte offsets,
QBE types, heap headers, root slots, or collector descriptors.

Version 4 instructions add:

| Operation | Purpose |
| --- | --- |
| `string_literal` | Produce a valid UTF-8 String value |
| `string_concat` | Concatenate two Strings |
| `string_equal` | Compare two Strings |
| `string_size` | Return the Unicode code-point length |
| `string_index` | Return one code-point String with checked negative indexing |
| `write_string` | Write a dynamic String with optional newline |
| `array_construct` | Allocate and initialize a homogeneous Array |
| `array_size` | Return the element count |
| `array_get` | Read one element with checked negative indexing |
| `array_set` | Replace one element with checked negative indexing |
| `array_push` | Append one element and grow capacity when required |
| `closure_construct` | Pair a function body with ordered captures |
| `closure_call` | Invoke a function value with authored arguments |

Closure bodies appear in the ordinary function table with an explicit ordered
capture list in addition to authored parameters. A closure construction names
that function and supplies exactly the declared captures. The snapshot verifier
checks function signatures, capture types, call arity, value availability, and
origin validity before Native MIR is produced.

## Native MIR and layout

Native MIR distinguishes scalar, heap-free aggregate, and managed-reference
values. It retains semantic operations such as String indexing and Array growth
instead of encoding QBE calls in the MIR.

Layout recursively classifies a type:

- scalars and heap-free Gate 2 aggregates remain stack values;
- String, Array, closure, and reference-containing aggregate values use one
  machine-word managed reference; and
- fixed heap descriptors list the managed fields of boxed aggregates and
  closure environments.

This classification is deterministic and rejects recursive by-value layout,
unsupported element types, duplicate definitions, and descriptor limits before
code generation.

## Collector invariants

The Gate 3 collector follows [Decision 0005](decisions/0005-managed-runtime-and-tracing-gc.md).
Its verifier and runtime tests enforce:

- every allocation has one valid descriptor and checked payload size;
- every managed value live across allocation has a shadow-stack root;
- every root frame is popped on each normal return path;
- mark traversal visits only declared managed fields or managed Array elements;
- sweep releases Array backing storage before its handle;
- immortal String literals are distinguishable from managed objects;
- collection thresholds and counters are deterministic for the same program;
  and
- allocation failure and index failure terminate with stable diagnostics.

The registered source stress case constructs Array/closure/environment cycles,
drops each final root by returning from a helper function, and triggers at
least two collections through ordinary allocation pacing. Its instrumented
executable performs one final reporting collection after `main` returns, so
total and automatic collection counts remain distinguishable. It reports
reclaimed cycles and a final live set under the bound registered in issue #13.

A separate hand-authored MIR fixture forces repeated collections to exercise
the internal operation directly. This is test coverage, not the source-level
acceptance evidence.

Forced collection and counter reads are represented only by test-only Native
MIR instructions. They are intentionally absent from snapshot version 4 and
from the portable TypeRB surface; source programs cannot trigger or observe the
collector through this boundary.

## Implementation order

1. Decode and verify hand-authored version 4 fixtures.
2. Lower them to managed Native MIR and compute descriptors.
3. Emit and execute the String/Array runtime and exact-root collector through
   QBE.
4. Prove cycle reclamation with the hand-authored closure fixture.
5. Add the consumer-neutral version 4 producer to the reference compiler.
6. Connect real TypeRB source, differential tests, reproducibility checks, and
   the registered benchmark corpus.

No producer-side change precedes a working hand-authored executable path.

Steps 1 through 6 are implemented. The source corpus covers ASCII and
multibyte UTF-8, empty and dynamic Strings, scalar and managed Arrays, growth,
element aliasing, nested calls, zero and multiple captures, managed captures,
nested closures, reference-containing records and tagged values, and an
unreachable closure/Array cycle. String and Array bounds failures retain their
distinct TypeRB diagnostics. A broader cross-backend question about Array
growth through aliases and mutable parameters is tracked independently in
[type-rb/type-rb#596](https://github.com/type-rb/type-rb/issues/596); the
registered corpus does not assume an unsettled answer.

## Measurement path

`tools/gate3-benchmark` runs the four registered workloads through the same
pinned source revision and records:

- complete native, optimized Go, and size-optimized Go application build time;
- native snapshot, decode/lower, emit, QBE-to-assembly, and link phase time;
- raw and stripped executable size;
- one warm build and runtime peak-RSS observation per candidate;
- runtime observations after three unrecorded warmups; and
- native collection count, automatic collection count, collection nanoseconds,
  allocated bytes, reclaimed bytes, and final live bytes.

Collector statistics come from a separately built instrumented executable. Its
stdout and exit behavior must still match the ordinary executable; the report
is emitted to stderr only after `main` returns. The timed native executable does
not emit the report. Array backing allocations and growth are included in the
allocation, live, and reclaimed byte totals and in collection pacing.

The QBE adapter applies three semantics-preserving optimizations required by
the registered workloads: common unchanged block parameters reuse their SSA
value and root slot, statically known small scalar closures are devirtualized
under strict shape checks, and String literals plus literal-only concatenations
use immutable static objects. Dynamic closure calls and String concatenation
continue through the general runtime paths.

## Exit evidence

The recorded Darwin arm64 result passes every registered condition:

- all source observations and deterministic failure diagnostics match the
  optimized Go backend;
- snapshots, decoded MIR structure, QBE IL, assembly, and executables reproduce
  byte-for-byte;
- the source cycle workload triggers three automatic collections, reclaims all
  measured allocations by the final reporting collection, and finishes with a
  zero-byte live set;
- stripped executables are 96.82% to 96.83% smaller than the strongest
  size-optimized Go baseline;
- warm builds improve by 13.0% to 22.9%;
- the worst runtime median is 21.1% slower, within the 25% bound; and
- observed runtime peak RSS improves by 32.1% to 66.9%.

Gate 3 passes. Work stops before Gate 4 for maintainer review; this checkpoint
does not select a production backend or claim self-hosted performance.
