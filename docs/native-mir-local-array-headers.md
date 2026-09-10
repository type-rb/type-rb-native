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

Any Array binding reassignment disables the function-wide stable-header proof.
Unknown calls, allocation, Array growth, loop transfers and escaping local
scopes retain their conservative barriers. A readonly alias
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

Checked `if`, `elsif`, `else` and joins now retain parameter and outer-local
headers when the complete function preserves their identities. The existing
Array-region operation family records each marker's token origin and entry
local count. MIR validates nesting, arm order, matching scope-exit counts and
origins, increasing marker origins and balanced joins before selecting headers.
Malformed control rejects the region, including an arm after `else`, a missing
scope restoration or an unmatched join. Opaque effects are retained in order and still disable the function-wide proof.

Conditional statement checking has a dedicated helper in the checked-program
owner. Scalar branch/range facts remain conservative, and the backend receives
only the existing verified header list. This is a bounded control projection,
not general control-flow MIR or branch-sensitive effect analysis. Conditional
allocation or rebinding still blocks the entire function, and an accessed
branch-local Array that leaves scope remains ineligible.
[Issue #384](https://github.com/type-rb/type-rb-native/issues/384) records this
structural and checker-organization extension and its verification evidence.

## Loop-local lifetimes

The checker retains the complete effect projection, including loop starts (11)
and exits (12). Both carry the entry local count; the exit follows a matching
scope restoration at the same token origin. The same MIR control stack verifies
conditional/loop nesting and rejects mismatched kinds, scopes, origins and joins.

When the function-wide proof is unavailable, MIR selects independent loop-local
headers. A selected loop has no opaque effect anywhere in its condition or body,
including nested control flow. Its bindings must be alive before the loop starts.
Initialization and later effects outside the loop do not invalidate this proof.
The pass prefers an eligible enclosing loop to duplicate nested placements; a
blocked outer loop still permits independently safe inner loops. Local bindings
created inside the selected loop are not hoisted. This is conservative effect
isolation, not general alias analysis or partial-path effect reasoning.

The named `array_loop_headers` plan contains ordered triples of start operation,
end operation and declaration indexes. The verifier independently derives the
complete plan and rejects missing, duplicated, reordered or forged placements.
Input MIR cannot supply either global or loop-local optimization facts.

The QBE adapter loads each selected header before the first loop condition. Its
active header stack is restored on lexical loop exit, so adjacent loops and later
growth cannot consume a stale cached header. Existing GC roots remain responsible
for Array reachability. Unknown calls, allocation, rebinding, growth and loop
transfers inside the selected lifetime disqualify it. Element updates through
aliases remain observable; all bounds and negative-index checks are retained.
The ordinary compiler and CLI source use this same verified implementation.

[Issue #388](https://github.com/type-rb/type-rb-native/issues/388) records the
bounded slice. Runtime gains, full target acceptance and published performance
remain separate evidence; this representation alone makes no speed claim.
