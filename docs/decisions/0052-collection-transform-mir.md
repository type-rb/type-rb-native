# Value-producing collection blocks in MIR

Status: implemented; integration validation is recorded with the reference update.

## Contract

`Array<T>` and `Range<Integer>` support `map`, `select` and `reduce(initial)`
with brace or `do` blocks. `map` and `select` also support `with_index`.
Their block parameters are mutable lexical bindings. Each completing block
must supply a result expression; selection requires Boolean, and reduction
preserves the initial accumulator's type. A return, escaping loop transfer or
prefix `try` cannot cross a transformation block. Nested loops and functions
retain their own control boundaries.

The source expression runs once. Array traversal retains that object and reads
its current length and next element for each invocation. Appends and future-slot
replacements are observed; rebinding the source variable does not retarget the
traversal. Selection retains the visited value before evaluating the predicate,
even if the predicate changes its parameter or the source slot. A readonly
source binding does not freeze an object reachable through mutable aliases.
Reduction evaluates its source before its initializer, then traverses the
retained source after initializer effects. Empty reductions return the initial
value. Range traversal streams its bounds and never computes inclusive end + 1.

These are the reference language's sequential traversal rules. The integration
uses TypeRB PR #729; it does not introduce another mutation policy. Operations
that shorten/reorder Arrays remain separately tracked receiver-API gaps.

## Ownership

`TransformSyntax` records parser-owned suffix and block boundaries. Suffix
origins distinguish chained transformations on already evaluated receivers.
The checker validates those boundaries and binds a `MirIteration` to the source
and element types in each concrete `CheckedBody`. Analysis resolves map result
types before lowering, sharing the existing closure analysis pass. Generic
bodies and anonymous functions retain their own checked projections.

The result Array or reducer accumulator is an explicit loop-carried binding
before the receiver/cursor exit boundary. Existing iteration builders emit
ordinary typed blocks, live Array size/load operations and Range comparisons.
Map appends the yielded value; selection conditionally appends the retained
visited value; reduction replaces the accumulator. No new backend instruction,
source-specific QBE path or external helper implements transformation semantics.

REPL execution consumes the checked projection and retains values in its normal
store. Native execution depends only on verified MIR: erasing source tokens,
syntax origins, inferred types and checked transform projections leaves the
output unchanged. Reordered-block execution and forced collection cover managed
selection values, nested Arrays, accumulators and captured block parameters.

Compiler self-use of transformation syntax requires a future compatible
immutable seed. This change keeps compiler implementation syntax within the
current seed and preserves the independent recovery chain.
