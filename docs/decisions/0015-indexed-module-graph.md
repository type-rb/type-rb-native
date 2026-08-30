# Decision 0015: Indexed file-root module graph

## Status

Accepted for the Gate 6H experiment.

This decision records the original measured graph semantics. The current
module index retains this ownership, candidate ordering, and scaling design
while also following the later
[TypeRB 0.4 compatibility mapping](../type-rb-compatibility.md), which rejects
two loaded direct/index peer identities.

## Context

Gate 6E established a correct config-free file-root closure, and Gate 6F made
that path self-hosting. The representative application contains five modules.
At larger module counts, three correct implementation choices become
quadratic: module-name lookup scans every loaded module, each module rescans
the complete import table to process its own imports, and graph reachability
rescans that same table for every visited module.

Configured projects and packages would introduce additional contracts without
first proving that the existing graph representation scales. A public Hash or
String hash API is likewise unnecessary for a compiler-internal ownership
problem.

## Decision

The source-ordered module, import, and declaration arrays remain canonical.
The file-root loader and resolver derive and maintain two internal
accelerators:

- a module-name index whose power-of-two bucket table is rebuilt only at
  deterministic growth boundaries; and
- a contiguous import start and count for every parsed module.

The module index prepends source-order entries, performs full String comparison
after bucket selection, and therefore preserves the previous last-match result
for duplicate internal input. A private TypeRB-authored rolling bucket
calculation distributes fixed-width names using the existing private ASCII
conversion helper. It is not a public String API, snapshot operation, MIR
instruction, or package intrinsic. The existing module-qualified function
index retains its independently measured Gate 6G bucket policy.

Parsing already appends a module's imports contiguously. Recording that span
allows file-root processing and cycle reachability to traverse only owned
edges. Newly discovered modules have no parsed outgoing edges and therefore do
not require a reachability traversal. Existing-target traversals retain a
local visited set while following only the recorded spans. Import binding
lookup and duplicate validation use the same module-owned span, and declaration
duplicate checks stop at the preceding module boundary because parsing appends
each module's declarations contiguously. These rules do not reorder imports,
change resolution, or create a serialized graph format.

The lexer keeps the same ASCII sets but orders its private membership tables by
the compiler workload. This is a TypeRB-source implementation detail; Gate 6H
does not change emitted runtime policy or introduce a compiler-only runtime
adapter. Preserving that boundary is required for exact B2/B3/B4 replacement.

## Consequences

The ordinary compiler can load large file-root closures without quadratic
whole-table scans. Direct-file precedence, index fallback, one-read ownership,
module-local declarations, exact diagnostics, entry-only `main`, QBE output,
and the explicit external QBE/CC boundary remain unchanged.

The index, bucket function, import and declaration boundaries, lexer ordering,
and scale generator are internal and unstable. This decision does not add
configured projects, packages, namespace imports, incremental caching, public
module identity, a stable CLI, source maps, tool discovery, or a TypeRB
reference-repository dependency on Native.
