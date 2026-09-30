# Compiler source responsibilities

The ordinary compiler entry is `compiler/src/compiler.trb`. Other production
modules live under the following responsibility owners. Existing module
basenames and function names remain descriptive source identities; their full
module paths include the owner. `compiler/cli` composes the core with CLI and
REPL adapters. `recovery/src` contains the independent recovery implementation.

| Owner under `compiler/src` | Responsibility | Permitted other owners |
| --- | --- | --- |
| `frontend/syntax` | Scanning, escape decoding, parsed declarations and source regions | types, resolution, state, support |
| `frontend/types` | Language type models, nominal identities and substitutions | resolution, state, support; the two projection exceptions below |
| `frontend/resolution` | Import and declaration lookup, specialization and argument binding | types, syntax, state, support, MIR, project |
| `frontend/checking` | Expression, statement and body checking; checked operation construction | types, resolution, syntax, state, support, MIR, project |
| `state` | Compilation state and function-owned checked projections | types, support, MIR; the parsed-iteration exception below |
| `mir` | Target-independent IR, construction, proofs, passes and verification | checking, types, syntax, resolution, state, support |
| `backend/qbe` | QBE serialization and emitted runtime and data routines | MIR, state, support, types; the intrinsic-identity exception below |
| `project` | Configuration, packages, standard-library source catalog and host files | support, syntax, state |
| `support` | Storage, path and literal helpers, Unicode identifier data | none |

Owners may import themselves. The entry composes core owners. Reciprocal
frontend/MIR imports are permitted; a directory cycle is not an error. These
rules constrain architecture independently of the language's compilation-unit
and initialization rules.

Four declaration-specific edges supplement the table:

- `backend/qbe/qbe_constants` imports `frontend/resolution/entry_resolution`
  for declaration-bound intrinsic identity.
- `frontend/types/transform_model` imports `frontend/syntax/iteration_syntax`
  and `mir/iteration_mir` for its shared parsed and checked projections.
- `state/source_state` imports `frontend/syntax/iteration_syntax` for the parsed
  iteration regions retained by `CompilerParsedProgram`.

The exceptions do not grant other modules access to those whole layers.
Core modules cannot import CLI adapters. Production modules cannot import test
modules, `testing` helpers or `trb/std/test`. Unit tests live beside their owner
as `<filename>_test.trb` for `<filename>.trb`, even when preparing an input uses
other components. Tests may exercise the complete core pipeline and share
explicit helpers under `testing`, but cannot import another test file.
The whole-compiler suite remains in `compiler/src/compiler_test.trb`. CLI tests
can exercise the composed CLI and core. All discovered `.trb` files, including
modules outside the entry's reachable closure, participate in the ownership
check; unknown directories, unresolved imports and composed path collisions fail.

Test placement follows the contract being verified, not the number of imports
or whether setup runs QBE. Feature contracts spanning checking, MIR and execution
belong in `tests/<family>` using the shared language registry's family ids.
System contracts belong with their subsystem. Local invariants remain colocated;
move unit tests with their production owner when splitting a directory. A large
local suite may have concern-specific `<filename>_<concern>_test.trb` companions.
Do not create tests merely to match every implementation file.

`testing` contains fixtures, pipeline adapters and execution helpers without
test-case registration. Dependencies run from tests to helpers to production;
production cannot import helpers, and helpers cannot import test cases. These
are repository roles, not new TypeRB directory semantics. Staging and content
keys exclude `testing`, `tests` and `_test.trb` files using the same selection.
The ordinary compiler import closure and recovery inventories contain no test
helpers. CLI and recovery-specific helpers belong with those subsystems.

## Recursive checking

`frontend/checking/checked_program.trb` owns primary and precedence-based
expression checking. Calls, collections, member access, statements, control flow
and iteration have separate `checked_*` owners. Lambda body checking lives in
`lambda_checking.trb`. Their explicit imports may be mutually recursive; there
are no forwarding copies. Checking still constructs independently verified MIR,
and the QBE backend consumes those facts.

## Checking and repeating the migration

`python3 tools/compiler_layout.py` checks the ownership rules in preflight and
quick CI. Its synthetic tests demonstrate that permitted cycles pass and that
forbidden ownership edges still fail. The complete compiler unit runner discovers
nested tests dynamically.

For a branch based on the earlier flat layout, rebase onto the accepted source
and run:

```sh
python3 tools/migrate_compiler_layout.py --write
python3 tools/migrate_compiler_layout.py
python3 tools/recovery_layout_sync.py --check
python3 tools/compiler_layout.py
```

The migration manifest records module assignments, checker function ownership
and explicit current tooling consumers. A newly added flat module or checker
function needs a reviewed assignment before migration. The tool validates all
assignments and destinations before writing, retains function bodies, rewrites
leading imports and updates the registered current consumers. Repeating it is
idempotent. It also regenerates the canonical recovery inventories with the
shared synchronization tool, preserving reviewed mutation needles when their
module paths change and the needles still match exactly once.

Embedded test programs, recovery imports, immutable evidence and historical
cross-revision consumers are outside general import rewriting. Current probes
that deliberately import the compiler and own-frontend identity assertions have
explicit replacements. Frozen source paths retain their original identities;
`tools/compiler-project.sh` continues to resolve historical project layouts.

Source migration requires the accepted cycle-capable checkout seed and its
historical consumer handoff. Validate the resulting source with the exact pinned
reference, ordinary core/CLI fixed points, shared language contracts, and complete
hosted recovery and target checks. The count of production modules at the root
is a layout metric; passing ownership and execution checks establish the result.
