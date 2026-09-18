# Verified callable signatures and indirect calls

Status: implemented internal foundation; integration requires the checks below.
Authored `fn` values and lexical captures remain unsupported. This checkpoint
adds the typed call boundary needed by closure lowering, not complete ordinary
function-value support.

## Parsed anonymous bodies

The frontend now recognizes `fn` as an expression with its own typed positional
parameters, optional result annotation and body terminator. Nested expressions
and declaration defaults retain immutable `LambdaSyntax` regions; their parameter
rows never enter the surrounding named function's parameter/default catalog.
Reparsing unreachable syntax reuses the original region instead of replacing it.
The restricted header grammar rejects defaults, named-only/rest parameters and
generic lambda parameters, following the reference contract.

Resolved signatures live in the concrete `CheckedBody`, so generic instances
sharing the same source region do not share substituted types. Abstract template
validation visits nested header annotations too. The containing name resolver
skips anonymous bodies and excludes their iteration, catch and pattern bindings;
it cannot accidentally expose nested names outside their lexical boundary.
Body checking and capture selection now use the independent frames below.

The REPL collects a complete anonymous body, including nested `fn` and compact
statement separators. Ordinary checking still rejects construction explicitly
until lexical capture lowering and retained REPL environments are implemented.
The rejected ordinary probes remain coverage gaps, with updated diagnostic
evidence. This parser checkpoint does not make function values executable.

## Anonymous lexical checking

Each anonymous body has an independent checked projection, inherited generic
binding and return/transfer scope. Named and anonymous bodies share name
resolution and expression/statement checking. Resolution's permissive name
inventory is separate from the typed environment advanced in source order, so
later declarations cannot become captures or make forward references valid.

The anonymous frame contains a visible inherited prefix followed by its own
parameters and declarations. The checker records actual uses of inherited
bindings, retaining only their stable parent identities, declared types and
mutable capabilities. Nested uses propagate through intermediate closures.
Parameters and declarations can shadow inherited names; ended iteration slots
cannot donate identities, and hidden receiver/cursor bindings are excluded.
Unreferenced inherited values do not become retained captures.

The frame inherits no SSA values, mutable/field nullable proofs, pending Result
obligations, loop targets or interactive submission state. Immutable binding
proofs are copied with the new lexical identity; captured storage keeps its
declared type. Return, try/catch and must-use
checks belong to that body, including unused nested bodies and every completing
return path. Generic instances sharing source tokens retain distinct resolved
projections. Anonymous parameters stay outside the named declaration catalog;
nested expression facts stay in their own body tables, and the parent's path
facts remain unchanged.

This is semantic preparation for executable closure lowering. Ordinary fn
construction still reports the explicit unsupported diagnostic after valid body
analysis; invalid bodies report their actual checking error first. The ordinary
coverage gaps remain. Shared mutable MIR cells, callable body materialization
and retained REPL execution are required before claiming function-value support.

## Ownership and representation

Function annotations use the reference spelling `(A, B) -> R`, including `Void`
results, nested signatures and generic aliases. The frontend canonicalizes them
to a private structural spelling whose leading `$` cannot be an authored name.
Parameters must be value types; only a result slot can be `Void`. Unused callback
bodies receive the same arity, argument and return checks as ordinary functions.

`callable_types.trb` owns this spelling. Each callable MIR type has an independently
verified signature row containing parameter type IDs and its result type ID.
`mir_callables.trb` owns closure construction, indirect calls and validation;
`qbe_callables.trb` adapts only those verified facts. Recursive expression checking
remains in `checked_program.trb` to avoid a checker import cycle.

Instruction 41 binds a captured prefix of an ordinary checked MIR declaration's
parameters. Its argument span contains the captured SSA values; its result type
contains the remaining parameters and the declaration's result. Instruction 42
invokes an available callable SSA value with an exact argument span and result
shape. The verifier rejects invalid catalog ownership, missing bodies, unavailable
captures, wrong capture/argument types or counts, malformed spans and invalid
Void results. Host/runtime adapters cannot be captured through this operation.

The internal value is now a managed closure object, replacing the initial bare
code pointer. After the GC header it holds an adapter address and one word for
each captured value. The verified parameter prefix determines each field's type
and traced status. One adapter per declaration/prefix length loads the captured
arguments and calls the ordinary function with its existing ABI. The remaining
arguments arrive through the callable ABI, preceded by the environment pointer.
Adapters allocate nothing before entering the checked body; the caller roots the
environment and arguments, and the checked body owns its subsequent roots.

Closure construction has allocation/failure effects and roots its captured
managed values. Indirect calls conservatively have allocation, mutation, I/O and
failure effects and root the environment itself. Callable fields/elements are
traced in Array, Hash and record storage, including nested closures and cycles.
Float, Boolean and Integer captures occupy untraced slots. No capture layout or
code association depends on retained frontend declarations or source tokens.

Lexical registration now assigns identities separately from reusable active
slots, through one binding helper for declarations, parameters and synthetic
iteration/catch bindings. Nullable facts carry that identity, so ended or
shadowed bindings cannot donate flow facts to a later occupant of the same slot.
Each checked body owns these identities. This prepares capture selection; it
does not yet lower authored mutable variables to shared cells.

This is not a public callable ABI or completed function-value syntax. Before
accepting authored closures, lowering must materialize the selected captures and checked bodies, preserve
readonly/mutable capabilities in shared mutable cells, and retain closure
bodies/environments across REPL submissions. Named declarations used as values also remain unsupported.

The REPL pool now separates reusable name-lookup slots from capturable binding
identity. Ordinary bindings retain direct value IDs. On first capture, a binding
moves into one internal pool cell; later captures reuse it, and assignment updates
its child value. Reusing a scope slot creates a fresh binding without changing an
escaped cell. Pool compaction follows these cells through the existing identity
map, preserving sharing, cycles and managed rebinding while dropping unreachable
temporaries. An ordinary Native-built internal fixture covers those properties
and fresh iteration cells across repeated compactions.

This is retained-variable infrastructure only. No authored function currently
requests a REPL capture. Checked anonymous-body retention, captured capabilities
and nominal identity across later submissions still need implementation before
ordinary closure cases can be accepted.

## Validation and completion boundary

Internal MIR fixtures explicitly construct entry calls and closure factories,
while callback bodies and consumers use the ordinary checker. They exercise
escaped captures, independent factory calls, shared mutable Array storage, nested
closures, cycles through Array storage, higher-order parameters/returns, Hash and
record storage, mixed Float/Integer/Boolean captures and Void calls. Tests erase
source bodies and frontend function/parameter types, require identical QBE, and
execute with collection forced before calls and allocations. Malformed catalog
and instruction controls independently reject unverifiable MIR. Removing capture
or environment roots is rejected independently of the runtime execution tests.
Repeated scope-slot reuse also verifies binding identity and nullable facts.

The shared ordinary inventory distinguishes unused callback signature checking
from constructing and executing a function value. Its existing `fn`/capture
cases remain rejected and visible as gaps in Capabilities. Internal fixture
execution does not mark those ordinary cases as supported.

The canonical compiler closure contains 96 modules. Integration requires
unchanged-seed ordinary core/CLI fixed points, exact recovery-source validation,
snapshot-v4 compatibility, complete hosted recovery, target and lifetime checks.
Compiler implementation does not use the new function syntax. No seed, reference
pin, runtime ABI promise, benchmark baseline or performance qualification changes.
