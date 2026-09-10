# Ordinary Hash implementation

Status: ordinary implementation accepted in [PR #401](https://github.com/type-rb/type-rb-native/pull/401).
The separate [Hash cost decision](decisions/0033-hash-compiler-budget.md)
records the acceptance budget and required full validation. This subset is not
a claim of complete TypeRB library support.

## Language boundary

Use the pinned TypeRB revision as the semantic authority. This slice supports
homogeneous Integer or String keys and existing scalar, Array, named record,
and recursively typed Hash values. Literals support `key => value`, String
label keys, contextual `Hash<K, V>` annotations, and a fresh mutable empty
binding refined by its first indexed write. Function parameters/results and
record fields carry concrete Hash types. Existing immutable rules remain in
force; copy is shallow and iteration order is unspecified.

Indexed reads and `fetch` require a present key. Indexed writes insert or
replace. The method subset is `size`, `empty?`, `key?`, `delete`, `dup`, `merge`,
`update`, `keys`, `values`, and `fetch`. Deletion also requires a present key.
The returned Arrays must have an already supported ordinary Array element type;
Array-of-Hash values are outside this slice. `try_fetch` awaits ordinary Result
support. Hash iteration blocks await the ordinary closure/block representation.
Those boundaries report unsupported input rather than substitute semantics.

An unresolved empty Hash can survive a REPL submission and answer `size` and
`empty?`; subsequent indexed insertion establishes its key/value type. Ordinary
compiled code needs a concrete type by the end of checking. Aliases of an
untyped binding require an explicit annotation. UTF-8 literals retain the
existing ordinary Native String limitation; Hash does not establish Unicode
API coverage.

## Representation and ownership

`hash_types.trb` owns canonical type decomposition and managed layout
classification. `hash_mir.trb` owns the named `MirHashOperation` carrier,
mutation requirements and literal capacity planning. The checked frontend
publishes one plan per operation; `hash_checked.trb` verifies source boundaries,
operation kinds, key/value metadata and mutation permissions before lowering.
The QBE adapter consumes these plans. Hash effects conservatively stop existing
Array-header proofs where calls, allocation or mutation can intervene. This is
a checked operation region, not complete block/value MIR admission.

The runtime uses open addressing with linear probing, a power-of-two capacity
and a maximum occupied load of three quarters. A compact Hash header references
two word Arrays: one for keys and one for values. Each slot costs two machine
words, with no per-entry box. Integer keys encode the entire portable range;
String keys compare length and bytes. Integer mixing and String hashing are
independent of the frontend representation.

Existing precise GC Array descriptors trace only managed keys/values. The Hash
header is 48 payload bytes plus its descriptor word; the existing collector's
allocation bookkeeping is additional. A removed value cell is cleared at once.
String deletion replaces its key with a static tombstone. An empty Hash drops
both backing Arrays; sparse tables shrink geometrically and accumulated
tombstones are rebuilt during insertion. These operations preserve Hash
identity and shallow aliases. GC reclaims detached backing and unreachable
payloads on collection; clearing a reference does not promise an immediate
reduction in OS resident memory.

The adapter roots the receiver and computed key across the right-hand side.
It finds the destination only after that expression finishes, so an allocating
call that grows or changes the table cannot leave a stale entry address. Reads
and deletion preserve managed results across subsequent allocation. The runtime
uses the existing collector and its cycle handling, without a separate GC kind.

## Stateful REPL

`repl_model.trb` separates value identity/storage from rendering and evaluation.
`repl_hash.trb` implements hash-table buckets containing pool identities, with
content equality for String keys. Its bounded byte scan reuses the internal
CLI byte reader without allocating a String per character. Scalar pool entries
share a read-only empty child list; language aggregate lists remain independent.
Deletion clears both bucket references;
empty tables release their Arrays and sparse ones shrink. `repl_values.trb`
traces live Hash keys/values during the existing between-submission pool
compaction, preserving aliases and cycles. Runtime state is not reconstructed
by replaying previous input.

The REPL's existing value pool retains evaluation temporaries until the current
submission completes. A long loop can therefore use substantially more memory
than its live Hash entries. Bucket reclamation and whole-session RSS are tested
and reported separately. This slice does not introduce collection of active
interpreter stack temporaries.

## Verification and seed boundary

`compiler/src/hash_test.trb` covers typing, immutable rejection, operation
metadata and malformed plans. `tools/native-hash-test.py` runs ordinary and REPL
fixtures, automatic-GC stress, cycles, alias preservation, recoverable missing
keys, and a compiled bucket-storage probe. Pass `--reference /path/to/trb` to
also verify the fixtures against the pinned reference compiler. The ordinary
CLI suite includes Hash fixtures; the recovery closure includes all four new
core modules and verifies their missing/malformed/mutated source boundaries.

The compiler uses `Hash<String, Integer>` for module names, module-qualified
function declarations and project source ordering. Function declarations enter
the index when parsing succeeds. A missing name remains `-1`; replacing an entry
preserves the previous last-declaration lookup rule without changing duplicate
diagnostics. Declaration vectors retain their stable ordering and identities.

This removes `Gate4SymbolIndex` and its bucket/chain/growth/rebuild helpers.
`find_name_index` and `function_index_key` own the small lookup boundary; the
ordinary Hash runtime owns storage and content equality. The key separates the
decimal module identity from the name with `:`. Import-cycle traversal now owns
an invocation-local color array, instead of overwriting function-index storage.

Compiler self-use starts from the verified Hash seed in PR #405. Recovery uses
only its accepted String/Integer Hash subset and existing integer formatting;
ordinary `Integer.to_s` is outside that snapshot subset. No new snapshot
operation or broader source fallback is needed for the indexes.

## Compiler self-use recovery boundary

[Issue #403](https://github.com/type-rb/type-rb-native/issues/403) establishes
the prerequisites for replacing compiler name indexes. The reference pin
`bae19032aa1bb7b263bc827d02606edc6e981c52` supplies internal snapshot-v4 data
for `Hash<String, Integer>` construction, indexed assignment, required lookup
and key presence. It retains source origins and receiver/key/RHS order, with
explicit rejection of other Hash shapes and operations in this recovery path.
Ordinary Hash coverage remains wider.

The recovery MIR checks canonical key layout, Hash receiver identity, operand
types, entry-list arity and source origins. `recovery_hash_runtime.trb` owns
only this snapshot ABI's storage: content-hashed String buckets, Integer values,
geometric growth and the existing precise collector's root frames. It is emitted
only for snapshots containing Hash values; existing snapshots keep their output.
Tests exercise empty and duplicate keys, record/closure aliases, growth, forced
collection, missing-key failure and malformed metadata.

Linux amd64 keeps the immutable initial root and existing setup bridges, then
builds exact accepted Hash source `8a6d9ff73b14a97bca1b010ddaad6a38972b5373`
before reading candidate source. Its process traces, source/compiler identities
and capability probe are setup-only. Ordinary candidate B2/B3/B4 and all existing
bounds remain unchanged. This neither republishes an old seed nor substitutes
snapshot recovery for the ordinary chain. PR #405 pairs this recovery support
with the
[verified checkout seed handoff](bootstrap-seed-updates.md#current-verified-checkout-seed);
compiler index adoption uses these same operations.
