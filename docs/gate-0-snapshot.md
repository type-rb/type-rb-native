# Gate 0 Bootstrap Snapshot

Gate 0 accepts a deliberately small, versioned JSON snapshot. The format is a
temporary bootstrap boundary, not a public compiler API. Producer and consumer
revisions are pinned exactly while the experiment is active.

## Envelope

The root object has exactly these fields:

- `format`: `"type-rb-bootstrap-snapshot"`
- `version`: `1`
- `module`: a non-empty stable module identifier
- `sources`: an array of `{ "id", "path" }` objects
- `functions`: an array of function objects

Unknown or missing fields are errors at every object level. Limits are checked
before lowering: 1 MiB of JSON text, 128 sources, 256 functions, 256 blocks per
function, 4,096 instructions per block, and 256 Unicode code points per stable
identifier.

## Gate 0 function subset

A function has `id`, `name`, `result`, `entry`, `origin`, and `blocks`. Gate 0
accepts only the `Integer` result type and exactly one block, identified by
`entry`. The envelope retains an explicit block array so Gate 1 can add control
flow without replacing the data boundary. Each block has `id`, `origin`, and
`instructions`.

Every origin contains:

```json
{
  "source": "main",
  "startLine": 1,
  "startColumn": 1,
  "endLine": 1,
  "endColumn": 5
}
```

The source identifier must exist. Lines and columns are positive, and the end
position cannot precede the start position.

Gate 0 instructions are:

- `integer_literal`: `op`, `result`, `value`, and `origin`
- `integer_add_checked`: `op`, `result`, `left`, `right`, and `origin`
- `return`: `op`, `value`, and `origin`

Value identifiers are single-assignment within a function. Operands must name
previously defined values. A block has exactly one terminator, and `return`
must be its final instruction. These constraints intentionally describe only
the boundary corpus needed before Gate 1 adds executable control flow.

## Diagnostics

Validation stops at the first error in deterministic document order. A
diagnostic has a stable code, JSON-style path, message, and optional authored
source coordinates:

| Code | Meaning |
| --- | --- |
| `TRBN0001` | malformed JSON syntax |
| `TRBN0002` | schema type, missing field, or unknown field |
| `TRBN0003` | unsupported format version, type, or operation |
| `TRBN0004` | snapshot or MIR invariant violation |
| `TRBN0005` | resource limit exceeded |

Messages remain experimental; tests and integrations may rely on the code and
path only after a later decision explicitly stabilizes them.
