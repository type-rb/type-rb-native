# Gate 3 Managed Runtime

Gate 3 establishes the first cyclic managed-reference graph in the native
pipeline. The registered work and thresholds live in
[issue #13](https://github.com/type-rb/type-rb-native/issues/13); this document
defines the implementation boundary used to satisfy them.

## Supported source subset

Gate 3 retains every Gate 2 feature and adds:

- first-class dynamic UTF-8 `String` values;
- String concatenation, equality, code-point `size`, indexed access, and
  dynamic `puts`;
- mutable `Array<Integer>`, `Array<String>`, and closure-Array literals, reads,
  writes, growth, `size`, and `push`;
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

The internal GC stress fixture constructs an Array/closure/environment cycle,
drops its final root by returning from a helper function, and forces repeated
collections. The collector must report reclaimed cycles and a stable warm live
set under the bound registered in issue #13.

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
