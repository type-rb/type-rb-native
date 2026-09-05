# Architecture

## Purpose

TypeRB Native develops a TypeRB-specific native compiler and runtime while
keeping the supported language and reference compiler independent. Its
engineering objective is a self-hosted implementation that removes Go from the
ordinary bootstrap and application-build path while matching or improving the
practical tradeoff among build time, execution performance, and deployed binary
size after all required tooling is counted.

The experiment is not a port to a different host language. Native execution
and self-hosting are separate checkpoints, but both belong to the intended
path. The Go reference compiler bootstraps early artifacts and remains a
differential oracle. The completed compiler and runtime owned by this
repository are written in TypeRB and reproduce themselves without Go in the
ordinary release/bootstrap path.

## Ownership boundary

The [reference TypeRB repository](https://github.com/type-rb/type-rb) owns:

- syntax and normative language semantics;
- parsing, name resolution, type checking, and diagnostics;
- package resolution and portable standard-library contracts;
- the reference typed IR and supported Go, Ruby, and TypeScript backends; and
- the canonical cross-backend conformance behavior.

This repository owns only experimental native concerns:

- an independent TypeRB-authored frontend when the self-hosting gates reach it;
- bootstrap snapshot validation and lowering;
- Native MIR and its verifier;
- native data layout and target ABI profiles;
- optimization and backend adapters;
- object emission and linker integration;
- the experimental runtime; and
- native correctness, portability, and performance measurements.

The normal reference TypeRB build, test, and release paths must not depend on
this repository. A language-level change discovered here belongs in the
reference repository's normal design and review process. Until the independent
frontend exists, the reference implementation may provide a narrow snapshot
producer on a short-lived, removable experimental surface.

### Reference-repository independence

The reference repository is consumer-neutral. A temporary producer there must
be justified, named, documented, tested, and diagnosed solely as a
reference-compiler capability; it must be understandable without knowing that
TypeRB Native exists. Reference code, documentation, changelog entries, commit
messages, and pull requests must not contain this repository's name, gate
numbers, backend or runtime roadmap, consumer-specific aliases, integration
commands, revision pins, or bridge retirement policy.

This repository owns the other side of that boundary: the exact producer
command it invokes, the snapshot version used by each gate, the pinned merged
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
                         reference repository
TypeRB source
    -> lossless tokens
    -> syntax AST
    -> resolver and type checker
    -> typed IR
    -> experimental bootstrap snapshot
                         native repository
    -> snapshot verifier
    -> Native MIR lowering
    -> MIR verifier
    -> target-independent optimization
    -> backend adapter
    -> object files
    -> linker + native runtime
    -> executable
```

Each boundary must preserve source origins so diagnostics and runtime failures
can eventually refer to authored TypeRB source.

The bootstrap snapshot is intentionally transitional. After native execution
and runtime viability are established, the repository gains its own
TypeRB-authored parser, resolver, checker, and lowering. The reproducible
self-hosting sequence is:

```text
reference Go compiler -> B0 from TypeRB compiler sources
B0                    -> B1
B1                    -> B2
compare(B1, B2)       -> equivalent under the reproducibility policy
```

Published native releases use a previously released native compiler as their
seed. Building the bootstrap seed from Go is a recovery/development path, not
an ordinary release requirement.

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

The first backend experiments should use hand-authored fixtures. A producer-side
bridge should be added to the reference compiler only after those fixtures prove
that code generation and the minimal runtime are worth connecting.

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

The self-hosted compiler initially reached fixed-point closure with analysis
interleaved into direct QBE emission. That implementation remains valuable
migration and benchmark evidence, but it is not the target organization. The
migration proceeds as bounded vertical slices: define and verify a minimal MIR
operation/fact subset, lower it through the existing QBE ABI, move the matching
optimization ownership above the adapter, and remove the superseded emitter
logic before broadening the subset.

Ordinary optimization experiments keep their pre-registered compactness caps.
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
The first complete control-flow slice must delete its superseded Array
induction token facts and direct emission before the migration expands beyond
the portable range, index, and induction family.

The first complete `Array<Integer>` reduction slice extends that same family
with verified induction and accumulator block parameters. Its measured
one-time ceilings are 350,000 Darwin arm64 bytes, 317,000 Linux arm64 bytes,
667,000 bytes combined, and 1,120,000 bytes of target-neutral compiler QBE.
The measured code-section ceilings are 250,904 Mach-O `__text` bytes and
253,424 ELF `.text` bytes. Ordinary 1.05 compiler/build/RSS ratios and the 2.0
catastrophic bound remain in force. This slice must help recover the complete
family's temporary increase before any new portable fact family begins.
See [Decision 0028](decisions/0028-native-mir-optimization-boundary.md).

## Backend adapters

Candidate adapters consume the same verified, target-neutral MIR subset. QBE
is tried first to minimize the cost of the initial executable experiment.
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

A machine-code backend does not provide TypeRB's runtime. A promoted
full-language target would require accepted solutions for:

- strings, bytes, arrays, hashes, records, enums, unions, and nullable values;
- classes, interfaces, closures, and generic representation;
- allocation, ownership, garbage collection, and stack maps;
- failure traps, stack unwinding, and TypeRB source traces;
- module initialization and symbol visibility;
- filesystem, process, time, networking, and other portable runtime services;
- cancellation, scheduling, and concurrency; and
- native package integration, lifecycle, and error conversion through a
  separately accepted TypeRB design.

The initial runtime remains deliberately smaller: static data, scalar values,
simple aggregate layout, observable output, and deterministic process failure.
Gate 2 completes the heap-free aggregate layer before heap ownership and memory
management are added. This separation keeps record and tagged-value semantics
independent of the later allocation strategy.

Gate 3 adds an exact-root, non-moving tracing collector for dynamic Strings,
Arrays, closures, and recursively reference-containing aggregates. Heap-free
Gate 2 aggregates remain unboxed. Managed roots use compiler-emitted
shadow-stack frames, and heap descriptors identify managed fields without
placing target layouts in the bootstrap snapshot. See
[Decision 0005](decisions/0005-managed-runtime-and-tracing-gc.md).

The first collector is single-threaded and stop-the-world. Concurrency,
generational or moving collection, finalizers, and weak references are deferred
implementation choices rather than new language promises.

The ordinary self-hosted emitter reuses that collector for its supported
dynamic Strings, Arrays, and reference-containing records. Its current root
representation is one exact managed-reference stack with per-function
watermarks, loop compaction, alias roots, and managed-return preservation. It
does not conservatively scan the machine stack. Fixed descriptors,
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

The first Native-owned orchestration boundary is the experimental Gate 6B
single-file build. The TypeRB-authored compiler invokes explicit QBE and C
toolchain paths directly with `execv`, never through a shell, and atomically
publishes the finished executable after cleaning its intermediate QBE IL and
assembly. This proves ownership of the ordinary build graph without implying
that toolchain discovery, a stable project command, or a self-contained
distribution has been designed. See
[Decision 0009](decisions/0009-native-single-file-build.md).

Gate 6C closes that ordinary build graph after an initial seed exists. A
Native-built compiler becomes the executable seed for the next complete build,
and repeated same-basename generations must converge to exact bytes while
retaining the fixed-point QBE and full file-command behavior. Recovery may
prepare the first seed during the experiment, but its provenance is recorded
separately and it is not part of the ordinary Native-to-Native chain. See
[Decision 0010](decisions/0010-native-bootstrap-closure.md).

Gate 6D applies the same target-neutral compiler source, QBE IL, runtime
semantics, and Native-to-Native build graph to Linux arm64. Internal versioned
profiles select QBE's `arm64_apple` or `arm64` lowering and the corresponding
external linker policy; they do not fork language behavior or enter the
reference repository. Explicit selection makes the target part of the
reproducibility record and keeps cross-platform builds from depending on silent
host inference. Linux arm64 currently selects LLD through the supplied C driver.
See [Decision 0011](decisions/0011-linux-arm64-target-profile.md) and
[Decision 0022](decisions/0022-linux-arm64-lld-linker.md).

Gate 6E adds a config-free file-root module graph without changing that process
boundary. The TypeRB-authored compiler reads the selected entry and only its
transitive project declaration imports, preserves declaration ownership per
module, and emits one executable after the complete closure checks
successfully. The original gate accepted only named imports; the current
frontend also implements the bounded TypeRB 0.4 declaration-root mapping.
Unrelated siblings, package discovery, configured projects, and the hidden
single-source recovery adapter do not enter the original graph. See
[Decision 0012](decisions/0012-file-root-module-closure.md).

Gate 6F makes that graph reflexive: the canonical TypeRB-authored compiler is
itself a file-root closure with separate storage and path modules. A temporary
flat source may prepare the recovery seed, but every ordinary replacement
generation loads the real closure and reaches exact B2/B3/B4 QBE and bytes.
See [Decision 0013](decisions/0013-multi-file-self-hosted-compiler.md).

Gate 6G derives a deterministic module-qualified function index from the
canonical declaration arrays before resolution. Full key comparison preserves
semantics under collisions, while source-order head insertion preserves the
previous last-match behavior. The index is TypeRB-owned and internal; it is not
a public Hash or serialized compiler format. See
[Decision 0014](decisions/0014-indexed-function-lookup.md).

Gate 6H applies the same internal-derivation rule to file-root module graphs.
An incrementally maintained module-name index and parsed per-module import
spans let loading and resolution follow module-owned ranges, while contiguous
declaration boundaries stop duplicate scans before another module. Canonical
source-order arrays retain ownership. The private bucket and graph
accelerators do not stabilize a project, package, module, Hash, or CLI
contract. See
[Decision 0015](decisions/0015-indexed-module-graph.md).

Gate 6L makes the first durable previous-Native seed handoff without turning
the experiment into a stable release. A one-time registered fixed-point QBE
root produces attested Darwin and Linux arm64 compiler assets in an immutable
date-labelled prerelease. Fresh consumers verify the manifest, digest, and
attestation before an ordinary B1-to-B4 chain that contains no Go or reference
compiler. Compiler binaries stay out of Git history, while QBE, CC, system
libraries, GitHub release retention, and attestation infrastructure remain
explicit dependencies. See
[Decision 0019](decisions/0019-experimental-bootstrap-seed-distribution.md).

Gate 6M introduces two exact portable standard-package roots without making
the project module graph a package manager. Private compiler identities map
`trb/std/process` and `trb/std/math` to their existing `Process` and `Math`
declarations. Managed runtime helpers copy process arguments and implement
checked numeric text and narrowing operations; `Math.sqrt` crosses an explicit
C ABI and system-libm boundary. The portable-entry runtime slice is selected
as one unit when any registered process or conversion primitive is used and is
omitted otherwise, while the Native-owned link command supplies `-lm`
consistently on both registered profiles. These are internal lowering and
dependency choices rather than new TypeRB APIs or stable Native ABI. See
[Decision 0021](decisions/0021-portable-benchmark-entry-primitives.md).

Gate 6N adds an internal Linux amd64 profile behind the same self-hosted
frontend, target-neutral QBE emission, and managed runtime. The immutable
target-neutral root QBE recovers one root-era x86 compiler, followed by two
Go-free current-source transitions and the ordinary exact candidate chain.
The profile selects QBE `amd64_sysv`, the System V ABI, and the existing
explicit Linux LLD/libm link policy. This is a second-architecture experiment,
not a stable target or a target-specific semantic fork. See
[Decision 0025](decisions/0025-linux-amd64-target-profile.md).

## Source organization

Gate-derived implementation names reflect development history rather than
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

The bootstrap bridge remains removable because the independent frontend will
eventually replace it, not because removal is the default project outcome.
Gates expose correctness, performance, and maintenance problems early enough to
improve the shared MIR, runtime, backend, or build pipeline before those choices
become public contracts.
