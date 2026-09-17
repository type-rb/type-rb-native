# Architecture

## Purpose

TypeRB Native develops a TypeRB-specific native compiler and runtime while
keeping the supported language and reference compiler independent. Its
engineering objective is a self-hosted implementation that removes Go from the
ordinary bootstrap and application-build path while matching or improving the
practical tradeoff among build time, execution performance, and deployed binary
size after all required tooling is counted.

The implementation is written in TypeRB. Native execution
and self-hosting are separate checkpoints, but both belong to the intended
path. The Go reference compiler bootstraps early artifacts and remains a
differential oracle. The completed compiler and runtime owned by this
repository are written in TypeRB and reproduce themselves without Go in the
ordinary release/bootstrap path.

## Complete toolchain goal

The [MIR consolidation roadmap](mir-consolidation.md) records the longer goal:
full TypeRB behavior, Go/Ruby/TypeScript emission and execution, standard-library
and official-package coverage, and Native output outperforming equivalent Pure
Go applications in measured runtime, application size and build time. Current
Native coverage remains partial. Preserve high-level checked semantics for the
source backends while lowering Native layout/ABI details through its MIR path.

## Ownership boundary

The [reference TypeRB repository](https://github.com/type-rb/type-rb) owns:

- syntax and normative language semantics;
- parsing, name resolution, type checking, and diagnostics;
- package resolution and portable standard-library contracts;
- the reference typed IR and supported Go, Ruby, and TypeScript backends; and
- the canonical cross-backend conformance behavior.

This repository owns the TypeRB-authored implementation and its development:

- the independent TypeRB-authored frontend, growing toward full reference coverage;
- Go/Ruby/TypeScript emission and execution in that implementation as future work;
- bootstrap snapshot validation and lowering;
- Native MIR and its verifier;
- native data layout and target ABI profiles;
- optimization and backend adapters;
- object emission and linker integration;
- the Native runtime and platform support for the standard library and packages; and
- native correctness, portability, and performance measurements.

The normal reference TypeRB build, test, and release paths must not depend on
this repository. A language-level change discovered here belongs in the
reference repository's normal design and review process. The reference
implementation's narrow snapshot producer remains a recovery and differential
surface, not part of ordinary Native compilation.

### Reference-repository independence

The reference repository is consumer-neutral. A temporary producer there must
be justified, named, documented, tested, and diagnosed solely as a
reference-compiler capability; it must be understandable without knowing that
TypeRB Native exists. Reference code, documentation, changelog entries, commit
messages, and pull requests must not contain this repository's name, experimental
checkpoint names, backend or runtime roadmap, consumer-specific aliases, integration
commands, revision pins, or bridge retirement policy.

This repository owns the other side of that boundary: the exact producer
command it invokes, the snapshot version used by each checkpoint, the pinned merged
reference revision, compatibility coordination, and the condition for removing
the bridge. An upstream change remains narrow, internal, versioned, data-only,
and removable; downstream urgency does not turn it into a public TypeRB API.

## Implementation-language boundary

Repository-owned executable compiler and runtime source is written in TypeRB.
Go, Rust, Zig, C, or another existing implementation language is not introduced
as the permanent host for those components. Generated C, assembly, object
files, or backend IR are outputs rather than maintained implementation source.

External tools remain allowed and must be accounted for. QBE or LLVM, an
assembler, a linker, an SDK, and system libraries do not violate self-hosting;
they are explicit dependencies of a TypeRB-authored compiler in the same way a
linker can be a dependency of another self-hosted language implementation.

## Pipeline

```text
TypeRB source
    -> Native file/project loader, lexer, parser, resolver, checker
    -> verified Native MIR and target-independent passes (supported slices)
       or the remaining checked direct path (migration work)
    -> QBE adapter and generated managed runtime
    -> external QBE, assembler, and linker
    -> executable
```

Each boundary must preserve source origins so diagnostics and runtime failures
can eventually refer to authored TypeRB source.

Every accepted ordinary function now requires a verified MIR body; the ordinary
direct expression/body emitter has been removed. The
[MIR status](native-mir-optimization-status.md) distinguishes implemented
vertical slices from remaining ownership.

### Current compiler source ownership

The ordinary entry is [compiler/src/compiler.trb](../compiler/src/compiler.trb).
Its explicit transitive import closure contains 93 canonical implementation modules:

| Modules in `compiler/src/` | Current responsibility |
| --- | --- |
| `storage.trb`, `path.trb`, `literals.trb` | Shared storage, path predicates, and numeric/ASCII predicates. |
| `state.trb` | Compiler state, symbol indexes, shared locals, and diagnostics. |
| `parser.trb`, `syntax_tokens.trb`, `resolution.trb` | Syntax/token boundaries, import/declaration orchestration and body name resolution. |
| `declaration_lookup.trb`, `type_resolution.trb` | Visible declaration identity, semantic type resolution and concrete nominal instantiation. |
| `generic_model.trb`, `generic_arguments.trb`, `generic_syntax.trb`, `generic_validation.trb` | Authored generic templates, recursive type substitution, explicit applications and template validation; see [generic nominal MIR](decisions/0045-generic-nominal-mir.md). |
| `generic_functions.trb`, `generic_bindings.trb`, `generic_program.trb`, `generic_check.trb` | Concrete function instances, shared function/record initializer bindings, isolated abstract template checking and declaration-owned parameter identities; see [generic record defaults](decisions/0049-generic-record-default-mir.md). |
| `alias_model.trb`, `alias_syntax.trb`, `alias_patterns.trb` | Transparent/generic aliases, declaration-owned expansion and structural pattern identity. |
| `callable_types.trb`, `mir_callables.trb`, `qbe_callables.trb` | Structural callback types, verified captured environments/indirect calls and managed ABI adaptation; the [callable foundation](decisions/0051-callable-mir-foundation.md) precedes authored closures. |
| `checked_body.trb` | Function-owned concrete checking and REPL projections; [checked body ownership](decisions/0047-checked-body-ownership.md) separates shared syntax from instantiated semantic facts. |
| `standard_library.trb`, `result_model.trb`, `result_checked.trb` | Compiler-owned portable declarations, checked Result operations, propagation and required-use boundaries; see [Result control MIR](decisions/0046-result-control-mir.md). |
| `enum_model.trb`, `enum_types.trb`, `enum_syntax.trb`, `enum_checked.trb`, `enum_mir.trb`, `qbe_enums.trb` | Nominal variants/payloads, patterns, verified operations and layout adaptation. |
| `argument_binding.trb`, `default_arguments.trb` | Shared argument slots, duplicate/order rejection, private declaration-scoped default identities and typed prefix bindings for checking and the REPL; see [default lowering](decisions/0040-default-initializer-mir.md). |
| `checked_program.trb`, `checked_values.trb`, `checked_types.trb` | Recursive expression/body checking, typed checked values and shared type/operator rules. |
| `nullable_types.trb`, `nullable_flow.trb`, `nullable_mir.trb`, `qbe_nullable.trb` | Optional type identity, lexical and stable-field facts, typed storage/test/extraction and numeric conversion blocks, and representation adaptation; see [nullable MIR](decisions/0042-nullable-mir.md). |
| `mir.trb`, `mir_types.trb`, `mir_analysis.trb`, `mir_numeric.trb`, `mir_array_loops.trb`, `mir_flow.trb`, `mir_identities.trb`, `mir_roots.trb`, `mir_passes.trb`, `mir_verifier.trb`, `mir_instructions.trb` | MIR model, semantic composite types and queries, reusable proofs, CFG/dominance, operation effects/liveness/root plans, rewrites, structural verification and instruction contracts. |
| `mir_construction.trb`, `mir_builder.trb`, `mir_control.trb`, `mir_value_control.trb`, `mir_calls.trb`, `mir_intrinsics.trb`, `mir_logical.trb`, `mir_strings.trb`, `mir_arrays.trb`, `mir_records.trb`, `mir_hashes.trb`, `mir_hash_inference.trb`, `mir_ranges.trb`, `mir_iteration_control.trb` | Declaration-bound ordinary/runtime/host and standard-package call contracts, checked ABI shapes, block construction and publication of scalar and mutable scalar/managed control/value, Array, nominal record, Hash and Range operations, checked empty-Hash type constraints, live Array/streaming Range loops, conversion/I/O and short-circuit MIR. |
| `qbe_context.trb`, `qbe_functions.trb`, `qbe_numeric.trb`, `qbe_constants.trb` | Target context, function ABI/root-frame emission, MIR-selected numeric lowering and static data. |
| `qbe_calls.trb`, `qbe_mir.trb`, `qbe_control.trb`, `qbe_strings.trb`, `qbe_arrays.trb`, `qbe_records.trb`, `qbe_hashes.trb`, `qbe_ranges.trb`, `qbe_roots.trb` | Shared typed scalar/call adaptation, verified Array loop plans, general scalar/managed blocks and MIR-selected root publication. |
| `hash_types.trb`, `hash_mir.trb`, `hash_checked.trb` | Hash types and value layout, operation plans, and their checked source bindings. |
| `iteration_mir.trb`, `iteration_checked.trb` | Range construction and Array/Range iteration plans, structural validation, and checked source bindings. |
| `qbe_output.trb`, `qbe_runtime.trb`, `hash_runtime.trb` | Ordered QBE output and runtime generation, including the Hash runtime. |
| `project_config.trb` | Project configuration records, JSONC parsing, and validation. |
| `checked_functions.trb` | Parameter binding, body checking and module finalization. |
| `compiler.trb` | Final checking orchestration, declaration-bound runtime hooks, QBE adaptation, emission temporary-storage lifetimes, and the remaining driver code. |

The [shared iteration proof module](../compiler/src/iteration_checked.trb)
serves the checker, compiler entry, and REPL without importing the recursive
checker or emitter. Recursive expression/body checking stays in `checked_program.trb`; the independent
[value-join builder](decisions/0041-value-control-mir.md) owns typed result edges.
The current iteration plans cover Array and `Range<Integer>` statement `each`
and `each.with_index`. Checked Range construction retains the two Integer endpoint
regions and exclusivity; the same source-proof module validates construction
before MIR construction and REPL evaluation. Admitted functions lower Hash values,
Range values and iteration entirely from verified MIR; the backend does not
read their source proofs. Compiler runtime and typed host calls use the same MIR
call instruction as ordinary functions. The checked declaration retains its name,
source identity, adapter and parameter/result types. Verification checks runtime
signatures and the project-source record layout; runtime and host adapters cannot
be interchanged. Shared QBE call adaptation consumes these declarations, including
Void and Float ABI handling. Calls conservatively retain allocation, mutation, I/O
and failure effects, with MIR-selected live roots at every call.

Resolved `Math.sqrt` and `Process.argv` calls also use typed MIR signatures,
with a distinct standard-package adapter kind. Import aliases preserve package
identity; ordinary same-spelled functions remain ordinary declarations. Argument
widening and managed argv results use the shared call and live-root machinery.
Unreachable tails retain language diagnostics without discarding scalar or CFG
MIR ownership. Static strings in those tails are not emitted. Once a whole body
has committed to MIR, its token-bound Array region is discarded; legacy region
verification and QBE header setup are reserved for the retained direct adapter.

Every declaration in the actual compiler source closure is required to have MIR
by its self-use test. Numeric Array functions now share the general typed CFG;
the positional induction builder is removed. The direct adapter and remaining
token-bound analyses still await retirement. Retained direct-adapter tests explicitly disable their selected
builder before body checking through the shared checker stages; they do not rely
on an otherwise supported language operation as an opt-out. The CLI runtime
literal remains compile-time backend data, separate from runtime call operands.
See [Range coverage](native-range.md) and the [MIR milestone](mir-consolidation.md).

The CLI/REPL under `compiler/cli/` consumes these modules but is outside this
ordinary core closure. Snapshot recovery derives a temporary flattened source
from the canonical modules using
[strict closure validation](../src/compiler_recovery_source.trb); it does not
replace file-root imports in ordinary self-hosting. The
[organization schedule](repository-organization.md) tracks further extraction
and removal of superseded implementation.

The ordinary self-hosting sequence
starts from a previous Native seed, records any setup-only transitions, and
then compares repeated full Native-built generations:

```text
previous Native seed -> setup transitions -> B2 -> B3 -> B4
compare(B2, B3, B4)   -> exact same-basename compiler and QBE bytes
```

Published native releases use a previously released native compiler as their
seed. Building the bootstrap seed from Go is a recovery/development path, not
an ordinary release requirement. Recovery and differential tests use the
reference frontend's versioned snapshot, strict validation, and the separate
snapshot-MIR/QBE path. They are mandatory coverage but do not substitute for
ordinary Native-to-Native generation.

## Bootstrap snapshot

The bootstrap snapshot is a deterministic, versioned, target-neutral, data-only
interchange for the experiment. It is distinct from both the reference typed IR
and Native MIR.

It may eventually contain:

- normalized control flow and typed values;
- stable symbol and module identities;
- target-independent literals and semantic operations;
- explicit traps and required runtime capabilities; and
- source identifiers and spans.

It must not contain:

- parser, resolver, or mutable compiler objects;
- Go pointers, interfaces, callbacks, or process-local identities;
- unchecked or unresolved source;
- filesystem, network, environment, or process capabilities;
- backend-native instructions; or
- an implicit package-extension mechanism.

The consumer validates schema versions, resource limits, required features, and
all structural invariants. Unknown or unsupported input fails explicitly. While
experimental, producer and consumer revisions may be pinned exactly and the
format may change without compatibility adapters.

Hand-authored fixtures and the producer bridge established this boundary in
the early checks. Their [contracts](https://github.com/type-rb/type-rb-native/blob/7726ff18e9230cd149e9f0c317577f6429f907fc/docs/gate-reference.md#gates) remain available;
they are not unfinished prerequisites for today's ordinary frontend.

## Native MIR

Native MIR is an internal control-flow and value representation designed for
verification, optimization, layout, and code generation. It is owned by this
repository and is not a public TypeRB API or serialized package protocol.

The MIR should expose TypeRB semantics explicitly rather than relying on a
backend to infer them. Examples include checked integer operations, nullable or
tagged representations, failure traps, direct and indirect calls, allocation,
source origins, and runtime capability requirements.

Backend-specific instructions, object-format details, and linker behavior stay
below the MIR boundary. Existing backends must not force backend-specific
concepts into portable TypeRB source.

### Optimization ownership

Native MIR owns facts whose validity follows from TypeRB semantics and verified
control flow. This includes Integer ranges and nonnegativity, index validity,
loop induction and bounds, call allocation and mutation effects, Array-header
stability, and GC safe-point requirements. Target-independent passes consume
those facts to retain, move, combine, or remove semantic operations such as
range checks, negative-index normalization, bounds checks, header loads, and
root publication.

A backend adapter consumes verified MIR after those decisions. It may legalize
operations for a target ABI, choose backend instructions, assign backend
temporaries, and apply a backend-local peephole that does not require recovering
TypeRB semantics. It must not inspect source tokens or emitted backend text to
rediscover portable facts. Adding a second adapter before this boundary exists
would duplicate optimizer behavior and make a backend comparison ambiguous.

Numeric Array functions now use the same general typed CFG as other managed
functions. The former signature-selected induction/reduction builders, positional
six-block adapter and dedicated emitter are removed. `mir_array_loops.trb`
derives natural-loop membership, SSA forwarding, checked unit-step induction,
Array identity and stable storage from verified edges and instructions. Plans name
the preheader, owner, size operation and proved reads; verification re-derives
those plans before `qbe_arrays.trb` may reuse headers or omit access checks.
Block storage order and source tokens are not proof inputs. Unknown aliases,
changed guards or indexes, calls and allocation/mutation outside the admitted
operation set retain checks. Integer arithmetic overflow checks remain explicit.

This admits nonzero and subtracting reductions, multiple parameters, branches
and lexical transfers without a special Array function shape. Legacy direct-path
range/header tables and direct emission still serve their remaining consumers;
retiring those owners and broadening the CFG facts remain part of consolidation.
The independent low-level verifier fixtures are not an ordinary emission route.

The self-hosted compiler initially reached fixed-point closure with analysis
interleaved into direct QBE emission. That implementation remains valuable
migration and benchmark evidence, but it is not the target organization. The
migration proceeds as bounded vertical slices: define and verify a minimal MIR
operation/fact subset, lower it through the existing QBE ABI, move the matching
optimization ownership above the adapter, and remove the superseded emitter
logic before broadening the subset.

The [trade-off policy](optimization-tradeoffs.md) distinguishes ordinary
acceptance from bounded runtime-benefit investigation after a cost miss. It
retains cumulative budgets and removes superseded ownership, while allowing
useful optimizer code to have an explicitly justified cost. QBE text alone is
not a deployed-artifact objective. Existing ordinary CI limits remain unchanged.

Ordinary optimization acceptance keeps its pre-registered compactness caps.
A structural MIR slice may use a distinct temporary compiler-size envelope
only after the smallest useful skeleton has been measured and the envelope,
build/RSS limits, removal condition, and final compactness target have been
registered publicly. This temporary allowance does not weaken the end goal of
matching or improving the Go backend's build time and generated artifact size.
Each successive structural slice uses a validated marker that names its exact
accepted baseline, measured candidate identity, and one-time relative limits.
Before a candidate has a public revision, exact compiler and compiler-test
source digests identify the measured implementation without making the policy
retrospective. Once that marker exists in the baseline, later changes
automatically return to the ordinary limits.
Remove superseded Array induction token facts and direct emission as the
control-flow slice migrates. Assess outstanding migration debt and cumulative
cost before expanding the fact family; useful verified passes are not required
to have zero net code cost as a prerequisite to bounded investigation.

The first complete `Array<Integer>` reduction slice extends that same family
with verified induction and accumulator block parameters. Its measured
one-time ceilings are 350,000 Darwin arm64 bytes, 317,000 Linux arm64 bytes,
667,000 bytes combined, and 1,120,000 bytes of target-neutral compiler QBE.
The measured code-section ceilings are 250,904 Mach-O `__text` bytes and
253,424 ELF `.text` bytes. Ordinary 1.05 compiler/build/RSS ratios and the 2.0
catastrophic bound remain in force for ordinary acceptance. Retain these
historical ceilings and apply the trade-off policy to future cost decisions.
See [Decision 0028](decisions/0028-native-mir-optimization-boundary.md).

The current complete-compiler limits account for safe Array assignment
retention under [Decision 0029](decisions/0029-array-assignment-compiler-budget.md):
350,000 Darwin arm64 bytes, 328,000 Linux arm64 bytes and 678,000 bytes combined.
Linux amd64 remains at 310,000 bytes. Historical transition markers and all
relative, code-section, QBE and correctness requirements retain their contracts.

## Backend adapters

Candidate adapters consume the same verified, target-neutral MIR subset. QBE
is the current backend; the other entries below describe possible experiments,
not implemented adapters.
Target lowering selects a versioned ABI profile for an operating system and
architecture. Backend comparisons on the same target use the same profile.

| Candidate | Experimental role |
| --- | --- |
| Cranelift | Balanced fast-codegen candidate for development and AOT builds |
| LLVM | Optimizing ceiling for release-oriented measurements |
| QBE | Compact-backend and small-toolchain comparison |
| Direct emitter | Limited lower-bound experiment for compile time and size |

The architecture permits comparison; it does not promise long-term support for
multiple backends. A production decision should prefer one default. A second
backend remains only if a distinct use case demonstrates a durable advantage
large enough to justify its correctness and maintenance matrix.

An ABI profile defines calling conventions, symbol identity, data layout,
unwind behavior, and GC metadata for one target. Small backend-specific shims
may implement the profile, but they must not fork runtime or language semantics.
Objects from different backend implementations could be linked only after they
conform to the same profile. Per-function mixed code generation and tiered JIT
compilation are therefore deferred.

## Runtime and ABI

A machine-code backend does not provide TypeRB's runtime. The full-language,
production-use goal requires implemented and validated solutions for:

- strings, bytes, arrays, hashes, records, enums, unions, and nullable values;
- classes, interfaces, closures, and generic representation;
- allocation, ownership, garbage collection, and stack maps;
- failure traps, stack unwinding, and TypeRB source traces;
- module initialization and symbol visibility;
- filesystem, process, time, networking, and other portable runtime services;
- cancellation, scheduling, and concurrency; and
- native package integration, lifecycle, and error conversion through a
  separately accepted TypeRB design.

The initial runtime covered static data, scalar values, simple aggregate layout,
observable output and deterministic process failure. The current ordinary runtime
also manages Strings, Arrays, records and Hash values; remaining coverage is
tracked in the [ordinary language plan](native-language-coverage.md). Ordinary
Strings store byte length and code-point count separately, with UTF-8 data after
the managed header. I/O and Hash equality use bytes; language size/index use code
points. Non-ASCII indexing can allocate, with its lifetime effects owned by MIR.
Snapshot
aggregate recovery retains a separate heap-free layer, keeping record and
tagged-value semantics independent of allocation strategy.

Managed snapshot recovery uses an exact-root, non-moving tracing collector for dynamic Strings,
Arrays, closures, and recursively reference-containing aggregates.
Heap-free snapshot aggregates remain unboxed. Managed roots use compiler-emitted
shadow-stack frames, and heap descriptors identify managed fields without
placing target layouts in the bootstrap snapshot. See
[Decision 0005](https://github.com/type-rb/type-rb-native/blob/7726ff18e9230cd149e9f0c317577f6429f907fc/docs/decisions/0005-managed-runtime-and-tracing-gc.md).

The first collector is single-threaded and stop-the-world. Concurrency,
generational or moving collection, finalizers, and weak references are deferred
implementation choices rather than new language promises.

The ordinary self-hosted emitter reuses that collector for its supported
dynamic Strings, Arrays, and reference-containing records. Its current root
representation is one exact managed-reference stack with per-function
watermarks, loop compaction, alias roots, and managed-return preservation.
Managed values loaded from containers retain independent roots across later
allocation: replacing an element may remove the owner's last reference to a
still-used alias. The retained direct path omits those publications only when
its function has no following collection point; general MIR supplies explicit
live-before sets. Record field identities and types have one verified MIR owner, also consumed
by GC descriptors. Constructor operands and returned projections participate
in the same live-before analysis. The collector does not conservatively scan the machine stack. Fixed descriptors,
Array-backing reclamation, and deterministic pacing are therefore shared by
compiler-generated applications rather than being confined to the earlier
snapshot adapter. Versioned statistics remain an internal
environment-controlled test path; they do not add a portable TypeRB API. See
the [runtime memory stability plan](runtime-memory-stability.md).

Runtime semantics are shared across backend candidates. Target-specific ABI
profiles and small shims may differ, but the runtime must not be independently
reimplemented for every code generator.

## Linking and toolchain independence

Removing the Go toolchain does not automatically produce a self-contained
toolchain. An experiment may still use an assembler, system linker, bundled
linker, SDK, C ABI library, or backend sidecar. Reports must distinguish:

- no Go toolchain requirement;
- no external compiler requirement;
- no external linker requirement; and
- a single self-contained `trb` distribution.

Every required component counts toward build time and toolchain distribution
size. Dynamically supplied system libraries must be identified rather than
silently excluded from comparisons.

The ordinary compiler invokes explicit QBE and C-toolchain paths directly,
without a shell, and publishes the executable only after successful code
production and cleanup. Every replacement generation loads the canonical
TypeRB file-root closure; a derived flat compiler is recovery-only. Repeated
same-basename generations must reach exact compiler and QBE bytes.

Internal profiles cover Darwin arm64, Linux arm64, and Linux amd64. They select
QBE lowering and explicit linker/libm policy without forking frontend or
runtime semantics. The experimental immutable seed release supplies verified
previous-Native assets for arm64; the registered amd64 recovery starts from its
verified target-neutral root QBE and separately records setup transitions.
Neither boundary constitutes stable target or distribution support.

File-root and configured-project loading preserve explicit declaration
ownership and load only the supported closure. Internal indexes accelerate
lookup without becoming public collections or package APIs. Portable process
and math roots remain a bounded integration, not a general package manager.
The [capability map](https://type-rb.github.io/type-rb-native/) records exact
coverage; [historical architecture checkpoints](https://github.com/type-rb/type-rb-native/blob/7726ff18e9230cd149e9f0c317577f6429f907fc/docs/gate-reference.md#architecture-checkpoint-history)
retain the original experiment-to-decision mapping and seed provenance.

## Source organization

Superseded implementation names reflect development history rather than
architectural layers. The [organization schedule](repository-organization.md)
separates ordinary compiler responsibilities from snapshot/recovery adapters,
runtime generation, and verification support. It starts with documentation and
root support-code cleanup, then decomposes the compiler alongside MIR work.
The schedule preserves the canonical closure, explicit recovery boundary, and
historical evidence; it does not create a second compiler or wait for promotion.

## Stability and promotion

No MIR, ABI profile, snapshot, object, cache, command, or runtime API in this
repository is stable. Official TypeRB packages must not depend on it.

Promotion to a supported TypeRB target is a separate decision. It would require
representative portable conformance, source-mapped diagnostics and failures,
runtime and package boundaries, reproducible builds, primary-platform support,
an end-to-end advantage after the complete toolchain is counted, and a
reproducible self-hosted compiler build whose ordinary path does not use Go.

The bootstrap bridge remains recovery-only and removable when its retained
consumers have replacements, not because removal is the default project outcome.
Checks expose correctness, performance, and maintenance problems early enough to
improve the shared MIR, runtime, backend, or build pipeline before those choices
become public contracts.
