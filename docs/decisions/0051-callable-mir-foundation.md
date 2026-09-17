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
`mir_callables.trb` owns code references, indirect-call construction and validation;
`qbe_callables.trb` adapts only those verified facts. Recursive expression checking
remains in `checked_program.trb` to avoid a checker import cycle.

Instruction 41 references an ordinary MIR declaration with an exact matching
signature. Instruction 42 invokes an available callable SSA value with an exact
argument span and matching result shape. The verifier rejects invalid catalog
ownership, missing or mismatched code references, unavailable values, wrong
argument types/arity, malformed spans and invalid Void results. Host/runtime
adapters cannot be addressed through this operation.

The current internal code reference is a static, unmanaged address. It can cross
parameters, returns, joins and existing Array/Hash/record storage. An indirect call
conservatively carries allocation, mutation, I/O and failure effects. Shared MIR
liveness keeps its managed arguments and later-used values rooted. The backend
uses the verified signature for Integer, Float, managed-pointer and Void ABI
selection; it does not inspect frontend declarations or source tokens.

This representation is not a public callable ABI. Before authored closures are
accepted, lowering must add explicit captured environments, managed layouts and
roots, shared mutable capture cells, independent lexical return/transfer scopes,
and retained REPL identity. Parameter capability rules also belong in that
checked boundary. No plain code pointer may stand in for a captured environment.
Named declarations used as values are not enabled by this checkpoint.

## Validation and completion boundary

Internal MIR fixtures explicitly construct the entry calls, while callback bodies
use the ordinary checker. They exercise higher-order parameters/returns, Array,
Hash and record storage, mixed Float/Integer calls and Void calls. Tests erase
source bodies and frontend function/parameter types, require identical QBE, and
execute with collection forced before calls and allocations. Malformed catalog
and instruction controls independently reject unverifiable MIR.

The shared ordinary inventory distinguishes unused callback signature checking
from constructing and executing a function value. Its existing `fn`/capture
cases remain rejected and visible as gaps in Capabilities. Internal fixture
execution does not mark those ordinary cases as supported.

The canonical compiler closure grows from 90 to 93 modules. Integration requires
unchanged-seed ordinary core/CLI fixed points, exact recovery-source validation,
snapshot-v4 compatibility, complete hosted recovery, target and lifetime checks.
Compiler implementation does not use the new function syntax. No seed, reference
pin, runtime ABI promise, benchmark baseline or performance qualification changes.
