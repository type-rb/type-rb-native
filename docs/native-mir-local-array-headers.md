# Immutable local Array headers

The existing checked Array-header region can now select an immutable local
Array binding as well as an immutable parameter. This includes a local binding
initialized from a record field. It does not treat a readonly record or an
Array element as a recursively immutable value.

The checker records local declaration origins, local Array accesses and lexical
scope exits alongside parameter accesses and existing conservative barriers.
MIR selects the first eligible accessed declaration and independently rederives
that choice during verification. Access before declaration, access after scope
exit, mismatched local ordinals and forged optimized selections are rejected.
A selected local that leaves scope disables the function-wide proof; recycling
its local ordinal cannot transfer the old proof to a later binding.

The QBE adapter installs the existing single stable header at the selected
local declaration, after evaluating its initializer and storing the binding.
Parameter and local installation share one helper. The adapter does not infer
readonly status, effects, alias relationships or loop bounds from source text.
No element value is cached, so element writes through aliases remain visible.
Every indexed access retains normalization and its own bounds check, including
negative indices, empty Arrays and Arrays of different lengths.

Unknown calls, allocation, Array growth, conditional control and loop transfers
retain their conservative barriers. Mutable local bindings remain outside this
proof. A readonly alias alone cannot establish header stability in the presence
of another alias that can grow the Array. The same established nonallocating
scalar-call and square-root facts remain available; nested argument effects
still block the proof. Complete control-flow MIR, general alias analysis,
multiple stable headers and removal of redundant bounds checks are separate
work.

[Issue #378](https://github.com/type-rb/type-rb-native/issues/378) records the
bounded experiment. Local comparison evidence is distinct from published Linux
runtime tables and does not establish a new Pure Go result.
