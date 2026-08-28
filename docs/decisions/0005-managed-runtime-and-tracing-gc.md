# 0005: Managed References and a Tracing Collector for Gate 3

## Status

Accepted for Gate 3.

## Context

Gate 2 deliberately stops at heap-free scalars, records, and tagged values.
Gate 3 must establish a representation for dynamic Strings, mutable Arrays,
first-class function values, captured environments, and reference cycles before
the project can credibly expand toward a self-hosted compiler.

Portable TypeRB does not expose ownership, weak-reference, destructor, or
capture-list syntax. Adding any of those merely to simplify this backend would
change the language around one experimental implementation. Automatic
reference counting would therefore either leak ordinary closure/container
cycles or require a new user-visible cycle-breaking contract. Tracing
collection instead preserves the existing unrestricted strong-reference model.

Ruby and the standard Go implementation both demonstrate tracing collection
for language-managed object graphs. Go also separates stack allocation from
escaping heap allocation and uses a non-moving collector. Swift demonstrates
that ARC can provide prompt reclamation, but its weak and unowned references
and closure capture lists are part of the programming model needed to resolve
strong cycles. Gate 3 should not import that requirement into TypeRB.

## Decision

Gate 3 uses a single-threaded, stop-the-world, non-moving mark-sweep collector.
It is an internal implementation choice, not a TypeRB language contract.

The compiler emits exact roots and heap descriptors:

- each function has a shadow-stack frame containing every managed reference
  that can be live across an allocation;
- calls leave the caller frame linked while the callee executes;
- fixed-layout heap descriptors list managed-reference offsets;
- dynamic Array descriptors identify the element stride and whether elements
  contain managed references; and
- stack aggregates remain unboxed only when their recursively computed layout
  contains no managed reference. Reference-containing records and tagged values
  are heap objects.

The collector obtains raw storage from the platform allocator, links every
allocation into a runtime-owned heap list, marks from the shadow stack and
runtime globals, scans objects according to their descriptors, and frees every
unmarked object during sweep. Objects never move, so QBE values, captured
environments, and foreign-call arguments do not require forwarding updates.

Collection is triggered before an allocation would exceed a deterministic heap
target. The next target is at least 1 MiB and otherwise twice the post-sweep
live heap plus 64 KiB. Gate 3 records collection count, collection time,
allocated bytes, and post-collection live bytes through a test-only internal
reporting path. Those counters are not a portable TypeRB API.

Gate 3 managed values use these representations:

- A String is an immutable managed object containing UTF-8 byte length,
  Unicode code-point length, and bytes. Equality compares bytes after valid
  UTF-8 ingress; indexing counts code points.
- An Array is a stable managed handle containing length, capacity, element
  layout, and a resizable backing allocation. The collector scans managed
  elements and the sweep path releases backing storage.
- A function value is a managed closure containing a code pointer and a
  managed environment. The environment stores captured values according to a
  fixed descriptor. An indirect call passes the environment before authored
  positional arguments.

String literals may use immortal read-only objects with the same observable
payload shape. They are never inserted into the managed heap and therefore do
not add collection work. Dynamic results always use managed storage.

The collector has no finalizers, weak references, or non-memory resource
cleanup. External resources require deterministic package/runtime contracts in
a later decision. Gate 3 also excludes concurrent mutation and collection;
parallel collection can replace this implementation later without changing
portable source.

The bootstrap snapshot advances to version 4. It remains target-neutral and
data-only. It adds managed type definitions, String and Array operations,
closure construction, and indirect calls without serializing addresses,
layouts, roots, or collector details. Native lowering derives those details and
rejects unknown or unverifiable input.

## Consequences

- Ordinary TypeRB code does not need ownership or cycle-breaking annotations.
- Closure/Array cycles can be reclaimed and tested before class semantics are
  added to the native path.
- Non-moving collection keeps the initial QBE ABI and foreign-call boundary
  small, at the cost of fragmentation and stop-the-world pauses.
- Exact roots and descriptors increase compiler work but avoid conservative
  false retention and form a reusable boundary for later optimization.
- Keeping heap-free aggregates unboxed preserves the Gate 2 performance path;
  only recursively managed aggregates change representation.
- The initial collector is intentionally single-threaded and non-generational.
  Gate 3 measurements determine whether pacing, allocation, or scanning needs
  improvement before runtime scope expands.

## Alternatives considered

### Automatic reference counting

Rejected for Gate 3 because portable TypeRB currently has no weak/unowned edge
or capture-list contract. Hidden ARC would leak valid closure/container cycles;
adding such syntax would make the language accommodate an experimental backend.

### Conservative stack scanning

Rejected because it can retain objects accidentally, depends on target stack
and register details, and makes cycle-reclamation evidence less deterministic.
Exact shadow roots are more compiler work but a better long-term boundary.

### Moving or generational collection

Deferred. Either can improve allocation throughput or fragmentation, but both
add forwarding, barriers, and more target/runtime complexity before the basic
managed-value model is measured.

### Process-lifetime arenas

Rejected as the Gate 3 completion strategy. Arenas are useful for compiler
phases and may be added later, but process-lifetime retention does not establish
cycle reclamation or bounded memory for long-running programs.
