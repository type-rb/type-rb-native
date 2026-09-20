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
| Builtin values and conversions | Remaining Symbol quote/operator boundaries; Unicode identifiers; safe numeric/index/range conversions and structured errors | Portable numbers and scalar String conversions, UTF-8 Strings and portable Symbol spelling, nullable values, enums and Result MIR |
| Collection operations | Remaining String transforms; key-based Array sorting; safe collection lookup and conversion | Checked indexes, stable natural-order sorting, retained receivers, shallow copies and String joining, Hash snapshots, Range materialization, sequential transforms |
| Value declarations and identity | Forward initializer dependencies, top-level lowercase bindings and untyped empty collection inference | Nested/reopened modules, lexical privacy, inferred imported constants, qualified aliases, typed runtime constants, ordered initializer functions and persistent global roots |
| Nominal and union types | Newtypes/constructors; literal types and discriminated unions; remaining enum attributes and patterns | General union values and scalar type cases, nominal records, payload/raw enums, checked raw conversions and ordinary enum methods |
| Object declarations | Classes, initialization, fields, privacy, inheritance and dispatch; interfaces and conformance | Nominal layouts, calls, receiver capabilities and managed values |
| Callable and generic completion | Callable equality and remaining nullable-signature combinations; method-specific type parameters, generic classes/interfaces, constraints and remaining alias targets | Anonymous and named function values, shared captures, generic functions/records/enums, receiver-specialized enum methods and transparent aliases |
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

The current source adds stable natural-order Array sorting, raw enum conversions and ordinary/generic enum instance methods,
general union values and scalar type cases,
Float/Boolean String conversion and Float output,
nested/reopened modules and runtime constants with
verified MIR globals, portable Symbol expressions and keyword framing, Unicode
String trimming, named function values, nullable/generic combinations, and
colon-separated Hash key expressions. These extend String
joining, Hash snapshot iteration and Range materialization, Array search,
uniqueness, concatenation, insertion/removal, edges/copies/slicing, and the String
query, sequence, slice and escape families. Its 881 registered cases include
explicit remaining differences; neither this count nor green regression CI
closes #454.
