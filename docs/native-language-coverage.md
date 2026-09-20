# Ordinary Native language coverage

Status: the shared contract contains 913 ordinary-path probes and 32 feature
families derived from the pinned reference AST and public language/standard-library
documentation. This is a test inventory with explicit gaps, not complete language
support. [Issue #454](https://github.com/type-rb/type-rb-native/issues/454) owns
basic-language completion; [the generated family inventory](native-language-feature-inventory.md)
records semantic contracts that still need tests. The earlier 19-case inventory
was an initial sample, not a complete list of missing features.

## Stable natural Array ordering

`sort()` and `sort_descending()` return independent Arrays of non-nullable
Integer, Float or String elements. Stable merging, run bounds and element stores
use ordinary verified MIR blocks and Array instructions. NaNs follow numbers in
both directions; signed zero and equal values retain their order. String order
is bounded and byte-preserving, agreeing with Unicode code-point order for UTF-8.
The internal String comparison does not permit authored `String < String`.

Shared cases cover empty/odd runs, portable Integer limits, infinities/NaNs,
Unicode/NUL/invalid bytes, aliases, optional calls, effects and rejected element
types. Independent MIR erasure/reordering, forced GC, a 68-length oracle and
retained REPL replay complement them. The pinned reference incorporates
[type-rb#773](https://github.com/type-rb/type-rb/pull/773), fixing descending NaN
placement in the REPL; presentation and inline callable-array differences remain
visible. Safe collection APIs remain open. See
[decision 0072](decisions/0072-array-sorting-mir.md).

## Key-based Array ordering

`sort_by` and `sort_by_descending` accept a single block parameter and a portable
Integer, Float or String key. They evaluate the receiver once, visit the retained
Array's live contents and evaluate each visited element's key once. Source growth
is visited; parameter reassignment or source replacement does not replace the
retained value. The result owns fresh Array storage and keeps shallow aliases.

Typed MIR collects values and keys in separate rooted Arrays and stably merges
paired buffers. Equal keys keep their input order in both directions; NaNs are
last. The comparison phase never calls the block. Ordinary nullable narrowing,
union elements, records, callbacks, nested transforms, captures and readonly
receivers use the same machinery. Non-Array sources, non-orderable keys, extra
arguments, `with_index`, wrong block arity and escaping transfers are rejected.

Shared cases, source-erased/reordered MIR, missing-root controls, forced GC,
an independent 68-length stable-identity oracle and retained REPL replay cover
these contracts. The reference loses safe navigation on block iteration and
can dereference `nil`; [type-rb#774](https://github.com/type-rb/type-rb/issues/774)
and an explicit shared gap preserve that boundary. See
[decision 0073](decisions/0073-keyed-array-sorting-mir.md).

## Raw enums and instance methods

Explicit String/Integer raw values, `raw_value()` and `from_raw()` use canonical
Result/error identities and existing verified enum/record/union/control MIR.
Ordinary enum instance methods use checked function calls, including defaults,
privacy, nullable receivers and returned closures. Shared cases and independent
MIR/GC and retained-session tests cover these combinations; see
[decision 0070](decisions/0070-raw-enum-and-method-mir.md).

Generic enum methods inherit the receiver's type arguments through defaults,
recursive/private calls and returned closures. Abstract checking still rejects
invalid unused templates, and concrete methods are discovered before MIR catalogs
freeze. Source/template-erased MIR tests and retained-session checks cover the
boundary; see [decision 0071](decisions/0071-generic-enum-method-mir.md).

Method-specific type parameters and enum attributes remain open. Reference
initializer replay and REPL type/display differences remain explicit parity gaps.

## Union values and scalar type cases

General unions now compose with Array/Hash inference, generic applications,
aliases, records, enum payloads, optional values, Results, defaults and closures.
Canonical alternatives and injection/test/extraction belong to verified MIR;
scalar type cases check exact alternatives, exhaustive coverage and binding scope.
Independent source-erased, reordered and forced-GC controls complement shared
ordinary/REPL probes and retained-session tests. See
[decision 0069](decisions/0069-union-value-mir.md).

Literal types, discriminated unions and composite type patterns are not covered
by this implementation. Reference boundaries for grouped annotations and
nullable alternatives remain visible in the shared contract.

## Declaration namespaces and runtime constants

Nested and reopened modules preserve lexical methods, nominal types, aliases,
defaults, visibility and import identity. Top-level/module constants lower to
checked initializer functions and verified MIR globals, with explicit order,
persistent GC roots and retained REPL values. Nullable constant reads narrow by
stable declaration identity. Shared cases distinguish immutable bindings from
mutable scalar copies and source-function parameter bindings. See
[decision 0067](decisions/0067-namespaces-and-constant-mir.md).

Imported inferred constant types and qualified generic aliases are covered by
the updated reference. Forward initialization dependencies and untyped empty
collection inference remain explicit gaps.
This does not complete the module/binding families or the whole basic language.

## Symbol expressions

Unquoted and double-quoted Symbol spellings use the reference String semantics.
Quoted interpolation-looking contents remain literal; actual String interpolation,
Hash labels and named arguments retain their separate syntax. Existing String
MIR covers values, defaults, nullable results, captures and managed storage, with
source-erased/reordered/forced-GC and retained-session checks. Keyword Symbols also retain their literal identity in REPL framing. Single-quote,
operator spelling and multiline interpolation boundaries remain explicit; see
[decision 0066](decisions/0066-symbol-literal-syntax.md).

## Unicode String trimming

`String.strip`, `lstrip` and `rstrip` use the reference Unicode White_Space set
and preserve the retained bytes, including NUL and malformed UTF-8. Typed MIR
owns the direction, operand types, allocation effects and live roots. Shared
ordinary/REPL cases and independent source-erased, reordered, forced-GC and
negative verifier controls are described in
[decision 0065](decisions/0065-string-trimming-mir.md). The REPL itself uses these
ordinary methods; remaining String transforms stay open in the inventory.

## Hash key expressions

Colon-separated Hash entries accept quoted String, Integer and computed keys.
Parenthesized identifier labels retain their literal String name; other key
expressions are evaluated before their value in authored order. Boolean and nil
keys are rejected by the ordinary Hash type checker. This is the same typed Hash
MIR as the arrow spelling, with no new operation or runtime representation.
Ordinary execution and retained REPL probes include Unicode, NUL, interpolation,
duplicate labels and side effects. An independent managed fixture erases source
and reorders blocks before executing with forced collection.

## Current development priority

The [basic-language completion plan](basic-language-completion.md) groups the
remaining implementation and verification work into one completion milestone.

Complete useful language families together with their MIR dependencies, instead
of waiting for individual unsupported programs to be reported. TypeRB at
`TYPE_RB_REVISION` remains the semantic authority; no Native-only dialect is
introduced. Fix wrong acceptance, wrong results and unsafe behavior as soon as
the shared probes reveal them.

The ordinary String foundation now supports UTF-8 literals, code-point
length/indexing, concatenation, interpolation, allocation/lifetime and source/REPL
handling. Continue with the remaining String APIs recorded in the
shared inventory. Keep raw byte operations explicit where source decoding or
terminal editing needs them; character indexing and terminal cell widths remain
separate contracts.

Then coordinate the record/Hash/iteration MIR family, arguments and function
values, expression control flow, nullable/enum/Result behavior, and the remaining
basic declaration/type families according to their dependencies. The inventory
keeps wider source interop and package syntax visible as later phases, with
reasons; a retired reference AST node is identified explicitly. Do not count
these phase labels as implemented support.

The [MIR consolidation milestone](mir-consolidation.md) coordinates the shared
ownership work. Correctness, memory safety, process and reproducibility checks
remain required. Temporary performance/size regressions are observed during
integration; detailed qualification occurs at coherent milestones. A feature
need not manufacture a runtime speedup or a separate size budget revision to
justify its existence. Final performance goals remain unchanged.

## Array edges and shallow copies

Array `empty?`, `first`, `last`, `dup`, `reverse` and checked Range slicing now
work through ordinary MIR and the REPL. Copies retain a fresh outer buffer and
shared managed elements, including callable and nullable values. Slice evaluates
its captured receiver before the Range and observes mutations to that same Array
without following a rebound source variable. Optional absence skips arguments;
empty edge access and invalid slice bounds fail explicitly.

[Decision 0059](decisions/0059-array-copy-mir.md) records the checked copy operation,
element descriptors, independent lifetime verification and storage accounting.
The exact reference includes the retained receiver and library-result fixes in
TypeRB PRs [#737](https://github.com/type-rb/type-rb/pull/737),
[#738](https://github.com/type-rb/type-rb/pull/738),
[#739](https://github.com/type-rb/type-rb/pull/739) and
[#740](https://github.com/type-rb/type-rb/pull/740). The previously recorded generic
and Function-result checker gaps now pass both ordinary execution and the REPL.

## Array insertion and removal

Array `unshift`, `pop` and `shift` now use a closed, verified MIR mutation
operation and the retained REPL evaluator. Each requires a mutable binding.
Insertion captures the Array before evaluating its argument; removal returns
the selected element with its exact type and fails on empty storage. Managed
results can outlive their former Array, and removed slots do not retain values.

Live traversal observes insertion and removal through aliases. Existing pending
assignments retain their previously normalized position and recheck bounds after
RHS effects, including shortening and rebuilding storage. Loop-header proofs
cannot retain Array data or length across these mutations. Shared cases cover
these combinations, argument effects, optional calls, lexical transfers and
invalid capabilities/arity. [Decision 0060](decisions/0060-array-mutation-mir.md)
records verifier, liveness, storage and GC controls.

## Array String joining

`Array<String>.join(separator)` retains its receiver before argument evaluation,
then assembles the resulting current elements in one allocation. Byte-preserving
Unicode/NUL behavior, boundary re-decoding, optional calls, managed lifetimes and
REPL self-use are covered by [decision 0063](decisions/0063-array-join-mir.md).
Sorting and safe collection APIs remain explicit inventory gaps.

## Array queries and concatenation

Array `include?`, `count`, `index`, `uniq` and `concat` now lower through existing
typed MIR comparisons, loops, nullable construction and Array operations. Search
uses portable primitive/payloadless-enum equality; `index` returns `Integer?`.
Uniqueness retains first occurrences, including the first signed zero, while NaN
remains unequal to itself. Concatenation and uniqueness allocate fresh outer
storage and retain managed element identity. Arguments run once after capturing
the receiver, and before reading its current contents.

The shared contract covers Unicode/NUL, nullable calls, managed aliases, generic
concatenation, receiver mutation/rebinding, lexical transfers and rejection
boundaries. Source-erased/reordered MIR and forced-GC checks verify loop and root
ownership; see [decision 0061](decisions/0061-array-query-loops.md). Sorting and safe
collection forms remain open.

## Hash snapshot iteration and Range materialization

`Hash.each` binds the key and value from a shallow snapshot taken before its
body. Additions, deletions, scalar replacements and receiver rebinding do not
change the entries visited; mutations inside shared managed values remain
visible. Enumeration order remains unspecified. The checker requires two
parameters and rejects `Hash.each.with_index` and Hash transforms.

`Range<Integer>.to_a()` creates a fresh Array with the same inclusive/exclusive,
equal-bound and reversed-range behavior as `each`. Endpoint expressions run
once, and the inclusive maximum exits before incrementing. Existing typed Hash,
Array, Range and loop MIR instructions cover these operations in files and the
REPL, including retained values, managed snapshots, transfers and optional calls.
Source erasure, reordered blocks, forged checked plans/root maps and forced GC
are independently checked; see [decision 0062](decisions/0062-hash-range-collection-loops.md).

## Integer receiver operations

Integer `abs`, sign/zero/parity predicates, `min`, `max`, `clamp` and `to_f`
now work in ordinary files and the REPL. Arguments follow source order; invalid
clamp intervals fail after both limits have been evaluated. Numeric extrema,
negative parity, chaining, safe navigation and captured calls share the reference
contract. [Decision 0053](decisions/0053-integer-receiver-mir.md) records the
existing scalar/CFG lowering and independently verified failure guard. Float
receiver operations are described below; wider numeric standard-library coverage
stays open.

## Float receiver operations

Float `abs`, `floor`, `ceil`, `round`, `finite?`, `infinite?` and `nan?` now work
in ordinary programs and the REPL. Rounding produces checked portable Integers,
with halfway values rounded away from zero. Absolute value normalizes negative
zero, and classification distinguishes finite values, infinities and NaN.
Optional calls, aliases, managed captures and failure classes share the reference
contract. The REPL's existing `to_i` now also distinguishes non-finite inputs from
finite out-of-range values. [Decision 0054](decisions/0054-float-receiver-mir.md)
records the existing-operation lowering and boundary proofs. Wider numeric
package coverage remains open.

Float and Boolean `to_s` now return ordinary Strings in files and the REPL.
Float `puts` uses the same conversion. Finite values use shortest-roundtrip fixed
decimal notation, with `.0` for whole values and both signed zeros. NaN and
infinities preserve the reference spelling. Conversion mode, exact operand/result
types and allocation effects belong to verified MIR; Boolean text is static.
[Decision 0068](decisions/0068-scalar-string-conversion.md) records the bounded
runtime, asymmetric rounding intervals and ordinary compiler self-use. Shared
cases cover extreme values, optional calls, constants, receiver effects and
rejections; the CLI authority checks 8,392 binary64 boundaries and retained calls.
General REPL value-display formatting remains separate from `to_s` parity.

## Callable signatures and MIR foundation

Function type annotations, including nested signatures and generic aliases, now
reach verified MIR. Unused callback bodies check required positional arity,
argument types, return types and Void restrictions. Six shared probes cover this
boundary without constructing a function value.

[The callable MIR foundation](decisions/0051-callable-mir-foundation.md) independently
verifies internal captured environments, indirect calls and their root/ABI contracts.
Its fixtures cover escaped/nested closures and cyclic container storage. Ordinary
files now analyze captures before generating MIR, materialize concrete anonymous
bodies and signatures, and preserve shared mutable bindings across calls and
control flow. Shared probes cover higher-order calls, nested factories, iteration
cells, generics/defaults, nullable proofs and managed captures. Unknown calls
invalidate nullable proofs for mutable captured bindings.

The REPL now retains checked code and selected captures across submissions,
including shared cells, nested callbacks and cyclic containers. Nominal values keep
their originating type catalog when later declarations change local IDs. Typed
witnesses never execute initializers or anonymous bodies; recursive callable results
need no eager constructor. CLI controls cover declaration changes, failures, replay
and collection of unreachable code contexts. Local and explicitly imported named
functions now use the same verified callable MIR with an empty captured environment.
Required positional signatures retain nominal identity, lexical shadowing, managed
results and mutable parameter bindings. Generic/default/named-only declarations
require an explicit typed `fn` wrapper. Nullable functions must be narrowed before
calling, and function types can be direct generic arguments. Record callback fields
use the same retained REPL call path, including optional receivers.
[Decision 0064](decisions/0064-named-function-values.md) records the ownership and
validation. Other callable boundaries remain listed in the inventory. Capabilities
records each ordinary path separately; forced-GC internal fixtures supplement
rather than replace those observations. The updated reference passes `closure-generic-defaults` through check, build,
execution and REPL; the registry now records those matching paths.

## Value-producing control and lexical transfers

Full `if`/`elsif`/`else`, Integer/String literal `case`, and ternary expressions
produce checked values through ordinary typed MIR joins. Branches execute lazily;
case evaluates its selector once. Numeric branches widen to Float where needed,
branch-local bindings stay scoped, and managed aliases retain their reference
capabilities. Scalar value-producing full controls currently require an `else`; enum cases
may instead cover every variant.

Conditional `return`, `break` and `next` evaluate their guard before the guarded
value or transfer. A branch that transfers contributes no join operand. Enclosing
expressions preserve evaluation order and skip subsequent work after an
unconditional transfer. See [the ownership decision](decisions/0041-value-control-mir.md)
for the supported subset, verification and remaining pattern/type boundaries.

## Nullable values and safe navigation

`T?`, explicit `nil`, direct nil guards, returning guards and short-circuit RHS
narrowing lower to verified MIR operations. Safe navigation evaluates its receiver
once and skips member arguments on the absent edge. Optional values retain their
payload identity in calls, defaults, returns, records, Arrays and Hashes, including
zero and false payloads. The private traced layout and remaining flow gaps
are recorded in [decision 0042](decisions/0042-nullable-mir.md).

Retained REPL assignments now preserve checked narrowing and assignment display
types across inputs. Static rejection preserves facts; partial runtime failure
and interruption discard them. Explicit replay retains checking boundaries while
rebuilding accepted runtime effects. [Decision 0043](decisions/0043-checked-repl-submissions.md)
records ownership, import/record identity and independent CLI controls. The new
conditional/failure probes expose known reference defects: successful branch
replacement is tracked in [TypeRB #699](https://github.com/type-rb/type-rb/issues/699),
and [TypeRB PR #698](https://github.com/type-rb/type-rb/pull/698) fixes partial
failure. The exact reference pin and its reviewed expectations remain unchanged.

## Enum payloads and exhaustive case

Ordinary nominal enums support payloadless and required positional/named payload
variants, exhaustive case statements and expressions, immutable lexical bindings,
import aliases and recursive fields. Optional values, Arrays, Hashes and records
retain managed enum payloads. The REPL uses the same checked bindings and preserves
nominal identity through declarations and reload. Payloadless equality requires
the same enum type. [Decision 0044](decisions/0044-enum-mir.md) records the verified
operations, traced layout and source-independent backend boundary.

Raw values/conversions, instance methods and nested module declarations now have
the separate coverage described above. Attributes and wider patterns remain
explicit gaps. Supporting these families does not
complete all pattern, enum or basic-language contracts.
Inline recursive payloads now pass file compilation and execution in both
implementations; their shared cases retain the regression coverage.
Mutually recursive REPL declarations still require a project/import boundary;
separate interactive declarations cannot refer to a not-yet-declared type.

## Concrete generic nominal types

Explicit required-field record and enum applications share one canonical
instantiation path: `Box<String>.new(value: "held")` and
`Item<Integer>::Value(7)`. Nested and recursive type arguments, imported templates
and type arguments, invariance and selector-derived enum pattern arguments are
covered through checking, MIR, execution and retained REPL values. The compiler
resolves complete concrete catalogs before MIR construction; backend output does
not consult generic templates or source spellings. See
[decision 0045](decisions/0045-generic-nominal-mir.md).

Enum receiver methods are covered above; method-specific type parameters and
generic classes/interfaces remain separate gaps. The shared
imported-generic-enum case now passes against the updated reference containing
[TypeRB PR #704](https://github.com/type-rb/type-rb/pull/704). Compiler self-use
of generic syntax awaits a seed that supports it.

## Transparent type aliases

Ordinary top-level aliases and explicit generic aliases expand in their defining
module to canonical scalar, container, nullable, record, enum and Result types.
Constructors, defaults, nested/reordered enum pattern arguments and recursive
nominal targets reuse the existing checked and verified MIR operations. Cyclic
aliases and invalid unused declarations are rejected before MIR publication.
REPL binding projections preserve canonical types; replay reconstructs visible
aliases when their underlying declarations are hidden.

[Decision 0050](decisions/0050-transparent-alias-mir.md) records ownership and
verification. Callable aliases now reach concrete MIR, including nullable payloads.
Union targets and nested module aliases now preserve their canonical identity.
Literal and class/interface targets remain gaps. REPL display currently uses the
underlying type rather than always retaining the authored alias. Alias record
construction and generic identity aliases now execute in the reference. Its
[same-package nominal-name collision](https://github.com/type-rb/type-rb/issues/708)
remains an explicit failure in the shared expectations.

## Generic functions and parameter defaults

Explicit top-level function applications now instantiate ordinary concrete MIR
signatures and independent checked bodies. Scalar and managed instances,
recursion, nested nominal/container types, nullable/Result values, import aliases,
iteration and declaration-scoped defaults use the same checking and call path.
Unused templates and defaults are checked with abstract parameter identities;
concrete call sites cannot legalize operations on unconstrained `T`.

Source/template erasure preserves verified QBE, and forced collection covers
managed generic calls. See [decision 0048](decisions/0048-generic-function-mir.md)
for ownership and remaining boundaries. Other generic declaration families remain
gaps. Both implementations reject local values used with generic type arguments;
[TypeRB PR #705](https://github.com/type-rb/type-rb/pull/705) fixed the reference checker.

## Generic record field defaults

Generic record defaults now share ordinary record parsing and private typed
initializer functions. Substitution covers preceding fields, nested nominal
values, Array/Hash, nullable and Result values, generic calls and value-producing
controls. Explicit fields run first in authored order, followed by omitted
defaults in declaration order. Omitted managed defaults allocate independently.

Every default is checked even on unused declarations or explicitly supplied
fields. Caller locals, current/later fields and unsupported operations on an
unconstrained type parameter remain errors. Function and record declarations own
distinct abstract parameter identities; concrete MIR, roots and QBE do not need
those bindings or source templates. See
[decision 0049](decisions/0049-generic-record-default-mir.md).

Full control expressions in record defaults and ternaries referring to earlier
fields now pass against the updated reference containing
[TypeRB PR #706](https://github.com/type-rb/type-rb/pull/706). Remaining Hash REPL
display differences stay explicit in the shared contract.

## Standard Result and typed control flow

`trb/std/result` and `trb/std/unit` load ordinary compiler-owned declarations.
Explicit Result construction, exhaustive cases, prefix `try`, statement-value
`catch` and required-use checks share concrete generic enum MIR. Error
propagation preserves ordinary numeric/optional conversions; catch handlers
produce a success value or use their lexical return/break/next owner. Both
paths evaluate the Result once, and ordinary each remains transparent to try.
User enums with the same name retain ordinary enum behavior.

Native emission uses existing verified enum operations and control-flow joins;
the REPL consumes checked Result projections and retained nominal identities.
Managed and nested payloads, scope-specific required-use checks, invalid
boundaries and unsupported catch composition have executable controls. See
[decision 0046](decisions/0046-result-control-mir.md). Transparent aliases,
general unions and compiler-declared structured package boundaries remain
separate dependencies, not newly supported forms.

The fixed reference compiler cannot build or evaluate optional Integer-to-Float
error propagation correctly. The current reference repository handles both nil
and present errors correctly; the shared case retains the pinned difference
rather than changing the pin or hiding Native's accepted behavior.

## Named/default arguments and record field order

Ordinary functions support positional parameters followed by `*` and named-only
parameters, with optional defaults in either group. Required parameters cannot
follow defaults within a group; the named-only group starts a new boundary. Explicit arguments run in authored order, then
MIR call operands are arranged in declaration order. Named labels resolve through
the selected declaration, including imported aliases. A label cannot supply a
positional-only parameter; duplicate/unknown labels, positional arguments after
named arguments, missing required values and wrong types are rejected.

Record construction remains keyword-only and now accepts reordered fields. Each
initializer uses its selected field's expected type, preserving contextual Float
conversion and managed values across later initializer evaluation. The shared
binding module also serves the REPL. Tests erase source and label metadata,
reverse MIR blocks and force collection before allocation/calls. QBE consumes
only normalized typed operands; it performs no label lookup or evaluation-order
analysis.

Configured REPL imports suppress the corresponding generated project imports.
Authored function and record aliases retain declaration identity across calls,
retained bindings and replay; see the [REPL contracts](native-cli.md#repl).

Default arguments and record initializers run in declaration scope, after all
explicit expressions, in parameter/field order. Only preceding declaration slots
are available; caller locals and later parameters/fields are not. Every default
is resolved and checked even if all callers supply that argument. Each omitted
managed default allocates a fresh value; explicitly passed aliases retain their
normal sharing. Record fields must place required fields before defaults.

Private typed initializer functions share ordinary MIR calls, verification and
root planning; see [the lowering decision](decisions/0040-default-initializer-mir.md).
No absent operand or null placeholder enters the final MIR call. Tests cover
source erasure, reversed block storage, forced collection, imported aliases,
short-circuit defaults and independent REPL evaluation. Nullable defaults preserve
the distinction between an omitted argument and an explicit `nil`; the shared
`nullable-default-presence` case covers both paths. Function values use required
positional signatures and reject named/default declaration conversion without an
explicit adapter. Method argument handling awaits the object declaration families. Required payload-enum arguments use the same
source-order binding rules.

## Ordinary UTF-8 String foundation

String `codepoints`, `chars` and `reverse` also work in ordinary files and the
REPL. They preserve code-point units, NUL, optional receivers and independent
result Arrays; readonly bindings keep their existing restrictions. Ordinary
runtime traversal is linear and retains managed sources/results through
collection. [Decision 0056](decisions/0056-string-sequence-mir.md) records the
typed operation, lifetime controls and the retained REPL boundary.

String `empty?`, `include?`, `start_with?`, `end_with?`, `index` and `rindex`
work in ordinary files and the REPL. First/last search returns an optional
code-point offset, including overlapping matches; empty patterns match at zero
or size. Literal predicates do not normalize text. Receiver retention, argument
order, aliases, nullable calls and lexical transfers use the common checked/MIR
pipeline. [Decision 0055](decisions/0055-string-query-mir.md) records the search
instruction, allocation-free runtime and external-byte semantics. The combined
String query and slicing case now passes; other String APIs stay explicitly open.

The shared cases cover Japanese text, two- through four-byte characters,
combining code points, negative indices, concatenation, interpolation, equality,
Hash keys, record/Array storage, embedded NUL and long literals. The additional
`tools/native-utf8-test.py` exercises Unicode paths and argv, rejects malformed
source bytes before token decoding, and forces collection before every String
allocation while indexed values and their owners remain live. Terminal tests
exercise evaluation as well as wide-character and combining-mark editing.
Query controls also cover allocating arguments, embedded NUL and malformed
external byte input against the pinned reference semantics.

String headers retain UTF-8 byte length and code-point count separately. Size is
constant time; ASCII indexing keeps its bounded static cache and allocates
nothing. Non-ASCII indexing scans code points and creates a managed one-character
String. MIR therefore treats String indexing as potentially allocating and
failing, and verifies the receiver's live root. Positions count code points;
grapheme clusters are not language indices. Terminal cell widths remain a
separate presentation concern. Further non-ASCII indexing optimization can use
this semantic boundary without changing the language contract.

The ordinary compiler serializes literal bytes through the declaration-bound
`compiler_string_bytes` runtime adapter and validates raw source with
`compiler_source_is_utf8`. These are typed compiler internals, like source input
and slicing, not public String APIs. Their source bodies preserve the preceding
ASCII bootstrap boundary. Go-hosted canonical recovery emission remains narrower
than the final ordinary compiler and must not be counted as ordinary UTF-8
evidence. No seed, pin or Go fallback is added to the ordinary chain; acceptance
requires the published seed's full replacement generations and fixed points.

Unicode identifiers and the remaining String receiver APIs are
still tracked separately. This foundation does not mark the entire String family,
standard library or basic-language milestone complete.

## Readonly record field correction

Record fields are immutable bindings. Direct and supported compound assignment,
including parenthesized and nested targets, must be rejected even through a
`mut` record binding. Whole-record rebinding remains valid, and Array values
held in fields retain the normal capability rules for indexing, method calls
and mutable arguments. Field immutability does not recursively freeze values.
Mutation syntax follows a binding through field/index projections; fresh Array
values may be passed to mutable parameters but cannot be assigned to or pushed
to directly. Grouping preserves the same binding requirement.

[Issue #350](https://github.com/type-rb/type-rb-native/issues/350) tracks the
checked-frontend correction and its ordinary file/REPL and recovery regressions.
The existing scalar Float fixture now rebinds the whole record to comply with
the reference rule. Ordinary named record Arrays are accepted through PR #352;
the recovery, seed handoff and subsequent MIR self-use are tracked in
[issue #349](https://github.com/type-rb/type-rb-native/issues/349).

## Coverage is path-specific

The [generated case matrix](native-language-coverage-matrix.md), generated family
inventory and the [Capabilities detail view](capabilities/README.md) use
[`tools/native-language-cases.json`](../tools/native-language-cases.json).
Each row describes one bounded example, not full support for a feature or a
percentage of the TypeRB language. The exact reference revision, executable
hashes and registry hash are recorded with observations.

The registry maps every concrete statement/expression node in the pinned
reference AST to a family. The oracle job checks the AST hash and scans all
non-test Go files in its directory for unclassified syntax nodes. This detects
syntax-inventory drift; it does not prove that every grammar combination,
method, type rule or boundary case has been tested. Families therefore also
record uncovered semantic contracts. Review those against public reference
language and standard-library documentation when expanding or changing the pin.

Both compilers execute the same authored sources, including project/import
fixtures. Each implementation has separate reviewed expectations for ordinary
check, build, execution and REPL. Positive cases, static rejection cases and
runtime failures are all intentional. Native acceptance of reference-invalid
record, Array or Hash equality is a bug, not extra support. Some reference REPL
submissions also fail despite successful ordinary execution; those limitations
are visible separately and must not be attributed only to Native.

A rejected REPL submission may leave the interactive session at exit status
zero. Output and diagnostics determine the result, not exit status alone.
UTF-8 literals, code-point size/index, concatenation/interpolation and managed
collection storage now pass ordinary build, execution and REPL checks. Additional String APIs remain explicit gaps.
The while probe produces the same final value but lacks the reference's `[mut]`
REPL display. These remain explicit differences. Snapshot/recovery coverage
cannot establish ordinary check/build/run/REPL support.

The regression command checks each implementation against its reviewed outcomes.
It can pass with known gaps; its `parityGaps` field summarizes differences between
those reviewed expectations, and `uncoveredContracts` identifies untested basic
contracts. `--require-parity` additionally rejects both known differences and
untested basic contracts. It requires both compilers, the reference AST and the
complete registry, and is intentionally failing until basic parity is achieved.
Neither mode infers full language coverage from the number of passing examples.

Frontend diagnostic wording is checked exactly for each implementation but need
not match between compilers. Matching rejection does not establish diagnostic
parity. [Issue #455](https://github.com/type-rb/type-rb-native/issues/455) tracks
message detail, real source columns and terminal presentation separately.
The String repetition case preserves the current second-line REPL origin;
dedicated diagnostic tests cover both compact and spaced input.
Runtime-failure fixtures may check the exact first
stderr line, status and stdout, omitting unstable reference panic stack frames.
Invalid UTF-8 output retains normalized raw bytes alongside an escaped display;
it cannot silently compare equal to valid text. Process timeouts always fail.

### Reproducing and maintaining the inventory

```sh
python3 tools/native-language-coverage-test.py
python3 tools/native-language-coverage.py --native /absolute/path/to/trbn --jobs 2
python3 tools/native-language-coverage.py --reference /absolute/path/to/trb \
  --reference-ast /path/to/pinned-reference/internal/ast/ast.go --jobs 2
python3 tools/native-language-coverage.py --native /absolute/path/to/trbn \
  --reference /absolute/path/to/trb \
  --reference-ast /path/to/pinned-reference/internal/ast/ast.go --require-parity
```

Build the reference executable from `TYPE_RB_REVISION`. CI verifies every
reviewed reference outcome in the quick oracle job. Native CLI jobs exercise
the same cases without invoking a reference compiler. Reports are short-lived
CI artifacts; do not add raw observations to `results/`. The suite is a
correctness contract, not a performance benchmark. Each subprocess has a
30-second timeout with owned-process-group cleanup; `--jobs` bounds concurrent
isolated cases and leaves reporting order deterministic.

Use `--case ID` for a focused probe and `--observe` to inspect changed Native
behavior. Observation still checks reference expectations and process failures;
it never rewrites expectations. Review all four paths before accepting a change.
Then regenerate all public views from that same reviewed registry:

```sh
python3 tools/native-language-coverage.py --table > docs/native-language-coverage-matrix.md
python3 tools/native-language-coverage.py --feature-table > docs/native-language-feature-inventory.md
python3 tools/native-language-coverage.py --pages-data > docs/capabilities/ordinary-language.js
```

CI checks exact generated contents with `--check-table`, `--check-feature-table`
and `--check-pages-data`. Review the related broad `capabilities/catalog.js`
entries when behavior changes, preserving their stated scope and separating
snapshot evidence from ordinary support. A Pages capability update needs no
formal benchmark rerun when runtime benchmark evidence has not changed.

## Feature delivery contract

Work within the active milestone and record exact reference/Native identities,
semantics and coverage in each cohesive PR. Register new semantic scope or material
experiments when needed; routine ownership moves do not need individual budgets.
Then deliver parser/checker behavior, checked/MIR representation and validation,
mechanical lowering, CLI/REPL coverage, and reference differential tests.
Preserve source diagnostics, evaluation order, branch-local bindings, portable
failures and managed-root lifetimes. Do not add semantic analysis to QBE text.

For `break` and `next`, explicitly validate loop targets, nested control flow,
backedges, induction updates and root cleanup. Existing bounds/header proofs
must account for each new path; unproved cases retain their checks. General
control-flow MIR need not be completed before the feature, but the affected
semantic ownership and verifier cannot be skipped.

After feature acceptance, follow the [seed update boundary](bootstrap-seed-updates.md)
before using the syntax in compiler implementation source. Add the matching
snapshot recovery coverage when that source begins using it. Then remove the
actual flags, nesting or representation workaround that motivated the feature.
Do not count a parser-only change or a source rewrite without bootstrap tests
as completion. Keep each feature and its self-use adoption independently clear.

## Statement conditional chains

The ordinary compiler and REPL accept ordered `if` / `elsif` chains with an
optional `else`. Every condition must be Boolean, including conditions in a
branch that will not execute. Conditions run in order and stop at the first
match; later effects and failures are skipped. Each branch has its own local
bindings. Nested chains, early returns, managed values, and Array mutation are
covered by `elsif-control` and `elsif-managed` conformance cases, with malformed
chains, scope errors, required traps, and invalidated loop bounds as controls.

This extends the existing checked conditional path. Functions outside the
current complete MIR subset retain direct lowering and their runtime checks;
conditional edges do not introduce new loop-induction or header-stability
proofs. Subsequent [value controls](decisions/0041-value-control-mir.md) and
[nullable MIR](decisions/0042-nullable-mir.md) extend the ordinary expression family.
Compiler implementation source now uses `elsif` in the statement-dispatch chain of `parse_statement_block`, replacing six nested
`else` / `if` wrappers.
This adoption follows the verified Sep8 seed handoff and matching snapshot
recovery coverage. Existing statement conditions, cursor updates, diagnostics
and application output remain unchanged; other parser and checker nesting
remains eligible for separately verified cleanup.

## Ordinary loop transfers

Bare `break` exits the nearest enclosing loop. For `while`, bare `next`
transfers to its header and reevaluates the condition, including its effects;
for Array iteration, it advances the cursor before the next live-length check.
Nested loops own their transfers, while `return` still exits the function. Every statement is
checked, including unreachable transfers. Transfers outside a loop and transfer
values are rejected. Existing contextual `next` bindings remain supported.
Use an ordinary `if` guard in this subset: postfix conditional transfers remain
unsupported. The REPL currently reports incomplete
input for a postfix `break if` submission; it does not execute that submission.

The checker stores the kind and nearest-loop target at the exact statement
origin. A named `MirLoopTransfer` plan verifies origin, kind, token bounds and
nearest target before the code generator or REPL may consume it. Missing,
malformed or cross-loop plans fail closed. Transfers invalidate complete scalar
induction plans, Array-region/header proofs and dependent nonnegative facts;
unproved accesses retain runtime checks. Backedges enter the existing loop
header and its root-compaction boundary; exits retain the loop cleanup path.

`loop-transfer-control`, `loop-transfer-effects` and `loop-transfer-managed`
cover nested targets, skipped updates and traps, condition effects, branch
termination and managed values surviving automatic collection. Negative cases
retain required index/range failures and reject illegal targets and values.
Recovered compilers and ordinary replacement generations exercise these
sources, separately from snapshot support for those source programs.
After loop-transfer snapshot recovery and the verified seed handoff,
`parse_statement_block` uses bare `break` exits instead of a completion flag.
Its dispatch, cursor updates, diagnostics and final result remain unchanged.
The checked block dispatcher also uses bare `break` for terminal tokens, block
tails and diagnostic exits, with `elsif` for statement selection. Its while
checking has an independent helper; current MIR admission and diagnostics remain
unchanged. Other completion flags and `next` self-use remain separate cleanup
opportunities.
Track the full delivery in [issue #334](https://github.com/type-rb/type-rb-native/issues/334).

## Boolean arrays

The ordinary compiler and REPL accept `Array<Boolean>` literals, explicitly
typed empty arrays, indexing, indexed assignment, `push`, `size`, and function
and record carriers. Nested arrays have the same three-level bound as existing
scalar arrays. Negative indexes retain the reference behavior: `-1` addresses
the final element, while indexes outside either end fail. Boolean elements do
not coerce to Integer; existing homogeneous typing, mutable-array invariance
and readonly capabilities apply.

`boolean-array-values`, `boolean-array-effects` and `boolean-array-managed`
cover shared and nested aliases, typed empty arrays, left-to-right evaluation,
growth and arrays surviving automatic collection. Invalid cases reject wrong
element/index types and mutation capabilities; runtime cases retain required
bounds failures. The ordinary coverage row includes REPL value display.

Boolean arrays use the shared scalar-element runtime storage; nested arrays
retain managed-element descriptors and roots. They remain outside the complete
scalar/numeric-reduction MIR type set, with explicit checked/MIR boundary tests,
and retain the existing verified header and checked-access paths. This does not
add numeric reduction permissions or a target-specific Boolean representation.

Snapshot v4 recovery preserves Boolean element types through construction,
reads, writes, growth, nested arrays, record fields and closure captures. The
recovery QBE adapter explicitly widens Boolean values to the shared 8-byte
Array storage and narrows loads to the Boolean scalar ABI. MIR verification
rejects Integer elements, Boolean indices and mismatched Array receivers.
The `boolean-array-recovery` fixture checks RHS reallocation and retained
negative-index positions through snapshot execution and compiler generations.
The separate `fixtures/recovery/programs/boolean-array-closure` case retains
record/closure capture coverage within snapshot recovery; it does not claim
ordinary alias or closure support. Focused runtime tests retain nested arrays
across explicit collection.

After the verified Boolean Array seed handoff, compiler implementation uses
`Array<Boolean>` for the shared `scalar_inline_range_failure_used` and
`array_bounds_failure_used` flags. Their initial values, writes and tests use
Boolean values directly. Other Integer arrays that carry counters or multiple
states retain their existing types. This is typed internal self-use, with
unchanged application QBE and required failure paths, not a runtime speedup.
Track this delivery in
[issue #341](https://github.com/type-rb/type-rb-native/issues/341).

## Named record Arrays

The ordinary subset accepts homogeneous `Array<Entry>` for a visible named
record, with the same three-level nesting bound as scalar Arrays. Typed empty
arrays, inference, read/write, `push`, `size`, function signatures and record
fields preserve canonical declaration identity, including imported aliases.
Identical field shapes do not make distinct records interchangeable. Mixed
record literals can infer union Arrays in the reference; that broader union
subset remains unsupported here.

The `record-array-values`, `record-array-effects` and `record-array-managed`
cases exercise aliases, nested arrays, retained assignment positions across
RHS growth and managed record contents surviving automatic collection.
Diagnostics retain exact element types, bounds and mutation capabilities;
readonly fields remain protected even after indexing a mutable Array.
Record Array parameters remain outside numeric reduction MIR, and elements
use the existing managed aggregate storage and tracing paths.

Snapshot v4 recovery also preserves record Array element identities through
construction, reads, writes, growth, nested Arrays, function returns and closure
captures. Layout analysis boxes a record used as an Array element throughout the
module, including scalar-only records, so an Array never retains its stack
address. Existing managed descriptors and roots trace both the record and its
String or Array fields. Scalar records outside Array storage keep their existing
layout; tagged and Float Array elements remain outside this recovery subset.

The `record-array-recovery` fixture covers retained assignment positions across
RHS growth, three-level nesting and managed records surviving allocation loops.
The separate `record-array-closure` snapshot fixture exercises closure captures
and escaping record Arrays; it does not expand ordinary closure support.
Recursive record Array definitions preserve nominal identity, and the ordinary
recovery fixture retains a self-cycle through allocation pressure while
creating unreachable cycles. Focused
MIR tests reject scalar and nominal element mismatches, invalid indices and
receiver types. A returned-record runtime test checks exact Integer values after
subsequent calls, Array mutation and explicit collection, plus managed children.
Removing the scalar-record boxing makes that lifetime regression test fail.

After the [verified record Array seed handoff](bootstrap-seed-updates.md#current-verified-checkout-seed)
was accepted in PR #356, compiler implementation adopts `Array<MirValue>`
for `MirModule.values` and `CheckedLocals.mir_value_rows`. The named fields
are `function_id`, `id`, `type_id`, `source_id` and `line`; construction, lookup
and verification share that exact carrier. The wrong tuple length is no longer
representable. Identity, type range, origins, uniqueness and definition-count
checks remain, and malformed-value tests replace complete readonly records.
This is the bounded self-use slice in
[issue #349](https://github.com/type-rb/type-rb-native/issues/349).
Other MIR row families and deferred optimization remain separate.

## Retired Array-loop integration branch

[PR #307](https://github.com/type-rb/type-rb-native/pull/307) is closed and
superseded by the [MIR consolidation milestone](mir-consolidation.md).
Its frozen head `96871cce7bf8bcd39717cb2b1af992cebfdb8dcd` preserves the
[implementation and adoption review](https://github.com/type-rb/type-rb-native/blob/96871cce7bf8bcd39717cb2b1af992cebfdb8dcd/docs/native-mir-loop-bounds-adoption.md)
and all historical failed measurements. It is not an accepted optimization.

The independent bounded QBE output batching and byte-preservation tests are
ported to current source, together with valid nested/negative-index and failing
overflow/short-output conformance cases. This does not omit Array bounds checks
or claim a measured application speedup.

[Issue #303](https://github.com/type-rb/type-rb-native/issues/303) retains the
useful dominating-guard, binding-version and Array-identity proof work under
the current milestone. Adapt it to shared verified MIR and current effects;
do not reinstate the old six-cell projection over the newer loop-local header,
iteration, assignment and lifetime owners. Retain producer/verifier adversarial
controls when reconnecting the proof. Old numeric investigation budgets are
historical, not current integration authority.

## Checkpoint reporting

Report the ordinary coverage cases added, remaining gaps, compiler-source
cleanup enabled, MIR invariants verified, bootstrap/recovery status and measured
costs separately. Update the corresponding issue and this coverage record when
a feature passes; keep planned work distinct from accepted behavior. Publish
Pages coverage at accepted checkpoints without rerunning the formal runtime
benchmarks unless accepted runtime evidence has actually changed.

## Ordinary Array iteration

PR #418 accepted the ordinary implementation at
`508f721f8964d67a5893e547d2e2fb3de5b20a63`; PR #423 accepted matching recovery
and seed observers at `d2980f14d1b64e5ce3544dd7133e7f5871644e4e`. Both complete
CI cohorts pass ordinary limits. The [verified seed handoff](bootstrap-seed-updates.md#current-verified-checkout-seed)
records preparation, immutable publication and fresh actual-asset verification.
The subsequent compiler-source adoption uses the verified checkout seed and
accepted-source amd64 bridge for the three read-only traversals below.

The current slice supports statement `Array#each` and `Array#each.with_index`,
with optional empty call parentheses, `do |value[, index]| ... end`, and
single- or multiline brace blocks. Both block forms share ordinary statement
parsing, including nested conditions, cases, loops and iteration. Statements may
be separated by newlines or semicolons. Block parameters have
the reference's mutable local bindings and lexical shadowing. The receiver is
evaluated once; each step reloads its current length and storage, so `push`
and replacement of a future element are observed. Rebinding the source local
does not retarget an active iteration. `next` advances the internal cursor,
`break` exits the nearest loop, and `return` exits the enclosing function.

The brace probes cover multiline statements and nested controls. Both now
pass against the updated reference containing
[TypeRB PR #723](https://github.com/type-rb/type-rb/pull/723).

The structured `MirIteration` operation connects receiver and element types,
source/body boundaries, and nearest-loop ownership. Ordinary code generation
and the REPL consume the same checked plan. Emission roots both the retained
Array and the current managed element across body allocation, and keeps hidden
local slots aligned with MIR identities used by nested loop-header placement.
The shared shape and checked-plan accessors live in `iteration_checked.trb`;
the compiler, recursive checker and REPL import this single proof owner.
Sparse origin maps share the same absent-entry read with Hash and Array
assignment plans. Existing runtime and compiler performance checks still apply.

The matching reference pin and maintained snapshot-v4 fixtures cover authored
Array iteration through existing recovery operations, including forced and
automatic collection. Float Arrays, Range/Iterable, batches, and value-producing
iteration remain outside the snapshot subset. Compiler source uses `each` for
checked Hash-plan verification and project-key membership, and `each.with_index`
for MIR function lookup. These read-only traversals preserve early return,
first-match ordering, empty/missing behavior and exact String equality.
Range/Iterable, batch iteration, expression-position iteration,
and the remaining Array APIs stay tracked in issue #410. The original Array
iteration checkpoint did not include removal operations. Ordinary shortening
behavior is now covered by the [Array mutation contract](#array-insertion-and-removal).

Compiler recovery metadata uses a separate 80 MiB input bound. Namespace and
constant integration produces 69,813,214 bytes of recovery JSON, exceeding the
previous 64 MiB boundary; the new bound leaves about 20% headroom. The earlier
managed Array MIR compiler produced approximately 43.1 MB, exceeding 40 MiB.
The earlier complete Array iteration snapshot was 34,616,510 bytes and required increasing the original 32 MiB bound to 40 MiB.
These are verbose recovery inputs, not application or shipped compiler binaries.
Enum integration contains 515 compiler functions, so the compiler-only function
bound is now 1,024, with boundary tests; ordinary snapshots retain their
512-function limit. The ordinary 4 MiB snapshot entry and remaining schema/type/
instruction bounds remain unchanged. Failed smaller-bound recovery attempts remain validation evidence;
a larger decode budget alone does not establish successful recovery.

## Array and Range transformations

`map`, `select` and `reduce(initial)` produce values through ordinary MIR loops;
`map` and `select` support `with_index`. Brace and `do` blocks, chained results,
empty/reversed ranges, portable maximum endpoints, readonly aliases, live Array
appends/replacements, receiver rebinding and reduction evaluation order have
shared check/build/execution/REPL probes. Selection retains the visited value,
and managed results and captured block parameters survive forced collection.
Invalid result types, readonly source mutation and nonlocal transfers have
explicit rejection cases. See [decision 0052](decisions/0052-collection-transform-mir.md).

Array and Range `any?`, `all?` and `none?` use Boolean loop-carried results and
ordinary MIR exit edges. Shared probes cover empty sources, short-circuit
effects and failures, retained live sources, Range extrema, nested predicates,
generic callbacks and captured managed values. The REPL consumes the same
checked plans. Indexed predicates and non-Boolean results are rejected.
`find` and `find_index` share the same short-circuit edges and add typed nullable
results. Their probes distinguish absence from zero/false, cover nullable
elements and Range positions, and retain visited managed values after source
replacement or parameter reassignment. Generic callbacks, captures and forced
collection use the ordinary nullable and closure MIR contracts.
Safe lookup/conversion APIs and broader expression-context
boundaries remain visible in the inventory; this coverage is not the entire collection API.

String slicing now accepts checked `Range<Integer>` bounds in ordinary programs
and the REPL. Shared probes cover retained receiver identity, inclusive/exclusive
limits, Unicode, NUL, optional calls and lexical transfers. Invalid ranges remain
explicit runtime failures; `try_slice` and other unimplemented APIs remain open.
See [the MIR contract](decisions/0057-string-slice-mir.md).

Control, octal, hexadecimal and scalar Unicode escapes now preserve exact bytes
in ordinary file and REPL literals. Malformed digit counts and invalid Unicode
scalars reject before construction. Escaped hash/quote values do not re-enter
source interpolation, and byte joins retain accurate code-point counts. See
[the decoder and bootstrap boundary](decisions/0058-string-escape-decoding.md).
