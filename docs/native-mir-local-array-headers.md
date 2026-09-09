# Stable Array binding headers

The checked Array-header region selects all accessed stable parameter and local
Array bindings. This includes mutable bindings and locals initialized from
record fields. Mutability permits element updates; the proof requires that no
Array binding is reassigned and no operation can invalidate a header.

The checker records local declaration origins, local Array accesses and lexical
scope exits alongside parameter accesses and conservative barriers. MIR selects
unique declaration operation indexes in first-access order and independently
rederives the complete list during verification. Missing, duplicate, reordered
and forged selections are rejected. Access before declaration, access after
scope exit and mismatched local ordinals are also rejected. A selected local
that leaves scope disables the function-wide proof; recycling its local ordinal
cannot transfer the old proof to a later binding.

The QBE adapter installs each selected parameter header at entry and each
selected local header after its initializer and binding store. Parameter and
local installation share one helper. The named MIR `array_headers` field replaces
the previous single-selection fact table, and the adapter replaces its single
header tuple with the corresponding operand list. It does not infer readonly
status, effects, alias relationships or loop bounds from source text.

No element value is cached, so element writes through aliases remain visible.
Every indexed access retains normalization and its own bounds check, including
negative indices, empty Arrays and Arrays of different lengths. Selecting two
bindings does not assert that their Arrays are disjoint or equally sized.

Any Array binding reassignment disables all stable headers in the function.
Unknown calls, allocation, Array growth, conditional control, loop transfers
and escaping local scopes retain their conservative barriers. A readonly alias
alone cannot establish header stability when another alias can grow the Array.
The same established nonallocating scalar-call and square-root facts remain
available; nested argument effects still block the proof. Complete control-flow
MIR, general alias analysis and removal of redundant bounds checks are separate
work.

[Issue #378](https://github.com/type-rb/type-rb-native/issues/378) records the
initial immutable-local slice. [Issue #380](https://github.com/type-rb/type-rb-native/issues/380)
records the bounded multiple-binding extension. Local comparison evidence is
distinct from published Linux runtime tables and does not establish a new Pure
Go result.
