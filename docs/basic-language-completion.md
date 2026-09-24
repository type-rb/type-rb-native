# Basic-language completion

The next language milestone is completion of the 28 `basic` families in the
[reference-derived inventory](native-language-feature-inventory.md), owned by
[issue #454](https://github.com/type-rb/type-rb-native/issues/454). Finish cohesive
families and their verified MIR dependencies without introducing a new acceptance
milestone for each helper or individual receiver method. Integration PRs remain
reviewable units; they are not separate user decisions to continue.

The pinned reference specification, standard-library declarations and AST define
the inventory. Counts of successful probes do not establish a percentage of the
language. Distinguish a missing implementation, a supported contract needing
broader verification, a diagnostic/display difference, and a reference defect.
Adding tests must not make a known rejection look like implemented support.

## Remaining implementation families

These are work groups, not equal amounts of effort. Their order follows type and
runtime dependencies; independent groups may advance while CI runs.

| Group | Remaining work | Existing foundation |
| --- | --- | --- |
| Builtin values and conversions | Remaining Symbol quote/operator boundaries and malformed-source origins | Portable numbers, strict/safe numeric String conversions, structured Result errors, UTF-8 Strings and Unicode identifiers, nullable values and enums |
| Collection operations | Contextual empty-collection inference and remaining receiver combinations; portable Unicode case contract across reference output modes | Literal String splitting/replacement and simple Unicode case conversion, safe Array/String/Hash retrieval and slicing, checked indexes, stable natural and key-based sorting, safe blocks, streamed sliced iteration, retained receivers, shallow copies and String joining, Hash snapshots, Range materialization, sequential transforms |
| Value declarations and identity | Forward initializer dependencies, qualified namespace binding members and untyped empty collection inference | Nested/reopened modules, lexical privacy, inferred imported constants, qualified aliases, typed runtime constants and lexical file/project/namespace variables, ordered initializer functions, shared REPL cells with lexical declaration identity, and persistent global roots |
| Nominal and union types | Reference common-field visibility and assignment defects; remaining enum attributes and patterns | Literal constraints and literal-union Hash keys, common record/class fields and readonly class discriminants with overlapping narrowing; nominal newtypes with explicit construction/projection and closed factories; general union values and scalar type cases, nominal records, payload/raw enums, checked raw conversions and ordinary enum methods |
| Object declarations | Initialized superclass construction, inherited overrides, class-alias construction and deferred receiver contracts | Classes and generic fields, ordered initialization with MIR definite-assignment checks, instance/class/private methods, field-free inheritance, explicit interfaces and managed witness dispatch |
| Callable and generic completion | Callable equality and remaining nullable-signature combinations; generic interface methods, constraints and remaining alias targets | Anonymous and named function values, shared captures, generic functions/records/enums/classes/interfaces, concrete generic instance methods, receiver-specialized enum methods and transparent aliases |
| Structured runtime dependencies | Import-free bounded `concurrent_map` and its transfer, cancellation and lifetime contract | Sequential structured iteration and function values |

The core API audit includes every import-free receiver declared for the covered
types, including less frequently used safe forms. It must not silently omit an
operation because a benchmark or the compiler does not call it. Wider package
APIs, JSX/package activation and Go/Ruby/TypeScript emission remain visible in
their existing later phases; they are still part of the full project objective.

## Cross-cutting verification work

These boundaries are already substantially implemented. They require systematic
positive, negative and combination coverage before their pending entries close:

- Lexical forms, malformed input, reserved words, source normalization and origins.
- Every operator/assignment form, widening, portable failure limit and lazy RHS.
- Shadowing, duplicate/unused/discard bindings and mutation through projections.
- Calls/defaults/named arguments, all-path returns and mutable argument boundaries.
- Nested value controls and transfers, exhaustive patterns and unreachable cases.
- Nullable/union narrowing, optional calls and common result types.
- Recursive/defaulted/generic nominal values, import identity and initialization.
- Retained collection receivers, shortening/growth, managed aliases and GC roots.
- File check/build/run and retained REPL state, failures, replay and type display.

Diagnostic position, failure class and erroneous acceptance are observable
contracts. Wording, formatting and terminal presentation differences remain
separately visible under [issue #455](https://github.com/type-rb/type-rb-native/issues/455);
do not represent them as missing parser/runtime features or remove their evidence.

## Completion and integration

For each group, extend the executable registry, implement the required typed MIR
operations and independent verifier controls, and regenerate the matrix,
inventory and Capabilities from that registry. Remove a pending entry only after
its named contract has adequate executable coverage. Reference bugs receive
consumer-neutral corrections and an explicit pin/expectation review when adopted.

Completion requires no unexplained or untested basic inventory entries and
passing ordinary-path parity, including boundary and rejection cases. Explicit
reference defects remain blockers to a full parity claim even when Native has
the intended behavior. `--require-parity` must continue to fail while known gaps
or uncovered basic contracts remain. Keep every required correctness, lifetime,
target, recovery and ordinary self-hosting check; qualify performance at the
coherent milestone described in [MIR consolidation](mir-consolidation.md).

The current source adds Unicode identifiers, safe collection retrieval/slicing,
structured number parsing and retained Result values through verified MIR and
shared core/REPL parsing. It also adds lexical namespace-body variables, including same-submission
REPL ordering and earlier outer bindings, shared interactive globals with checked lexical scope,
once-only initializers and explicit replay, optional scalar output through verified
MIR branches, and file/project lowercase bindings with verified mutable
global storage, reference-correct nullable invalidation and source identity,
literal constraints and common record/class fields with verified
widening and readonly discriminant narrowing, nominal newtypes with erased storage and
verified construction policy, callable suffixes, reserved-name checks and nested generic token boundaries,
streamed Array/Range batches, safe collection blocks and nullable literal contexts,
stable natural and key-based Array sorting, raw enum conversions and ordinary/generic enum instance methods,
general union values and scalar type cases,
Float/Boolean String conversion and Float output,
nested/reopened modules and runtime constants with
verified MIR globals, portable Symbol expressions and keyword framing, Unicode
String trimming, named function values, nullable/generic combinations, and
colon-separated Hash key expressions. These extend String
joining, Hash snapshot iteration and scoped numeric value inference, Range materialization, Array search,
uniqueness, concatenation, insertion/removal, edges/copies/slicing, and the String
query, sequence, slice and escape families. Literal-union Hash keys preserve
their semantic identity through lookup, copies, snapshots and collection.
Its 1535 registered cases include
explicit remaining differences; neither this count nor green regression CI
closes #454.
