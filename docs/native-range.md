# Ordinary Range values and iteration

The ordinary compiler and REPL support finite `Range<Integer>` values created
with inclusive `start..finish` or exclusive `start...finish` expressions. The
start is evaluated and retained before evaluating the finish, once each.
Arithmetic and comparisons bind more tightly than construction; logical
operators bind less tightly. Non-Integer endpoints are rejected.

Values can be retained in locals, parameters, results, named record fields,
supported nested Arrays (up to three Array levels) and String/Integer-keyed Hash
values. A Range is an immutable value with captured endpoints: reassigning its
original binding or replacing an aggregate entry does not retarget an active
iteration. The REPL displays `start..finish` or `start...finish`.

## Statement iteration

`each` binds the element; `each.with_index` also binds a zero-based ordinal.
Both support single-line braces and `do` / `end`, as Array iteration does.
The receiver is evaluated once. Reversed bounds and equal exclusive bounds
produce no elements. The implementation streams values without allocating an
Array of the range, calculating its length, or imposing a repetition limit.
Inclusive portable MAX terminates before incrementing its cursor. Full portable
spans can terminate early with `break` or `return`.

Internal cursor and ordinal state are independent of reassignment to the block
parameters. Lexical `break`, `next`, method `return`, nested Array/Range/while
loops, block scope and GC roots use the shared checked iteration boundary.
Array iteration continues to observe its live header before each element.

## MIR and representation

`MirRangeConstruction` binds the endpoint expression regions, exact construction
origin, Integer endpoint types and exclusivity. `MirIteration` carries a checked
source kind in addition to receiver/element identity and lexical body/parent
ownership. Both retrieval and transfer consumers reject stale, missing or
malformed plans. The QBE adapter consumes these facts; it does not infer range
semantics from emitted instructions.

The first representation is a managed object with three scalar payload words:
start, finish and exclusion bit. A precise descriptor marks no child pointers;
record fields, Array elements, Hash values and local/temporary roots retain its
identity. Future allocation elimination is a separate MIR optimization.

## Explicit boundaries

Range comparisons, indexing, Range methods other than the statement iteration
forms above, non-Integer Range elements, retained Iterable adapters, batching,
and result-producing iteration are unsupported. Function literals remain a
separate gap. Snapshot Range export and a verified seed handoff are separate
prerequisites before the compiler implementation can adopt Range syntax.
Ordinary compiler-source recovery uses the existing supported implementation
subset; it does not establish authored Range-program snapshot support.

The `range-*` conformance cases and ordinary CLI/REPL runner cover endpoint
side effects, values/carriers, precedence, lexical transfers, portable extrema,
GC pressure, and 1,000,001 streamed elements. These are correctness regressions,
not formal runtime performance results or complete Range API coverage.
