# Verified callable signatures and indirect calls

Status: implemented internal foundation; integration requires the checks below.
Authored `fn` values and lexical captures remain unsupported. This checkpoint
adds the typed call boundary needed by closure lowering, not complete ordinary
function-value support.

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
accepting authored closures, lowering must select lexical captures, preserve
readonly/mutable capabilities, share mutable capture cells, enforce independent
return/transfer scopes, and retain closure bodies/environments across REPL
submissions. Named declarations used as values also remain unsupported.

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

The canonical compiler closure remains 93 modules. Integration requires
unchanged-seed ordinary core/CLI fixed points, exact recovery-source validation,
snapshot-v4 compatibility, complete hosted recovery, target and lifetime checks.
Compiler implementation does not use the new function syntax. No seed, reference
pin, runtime ABI promise, benchmark baseline or performance qualification changes.
