# MIR consolidation milestone

Status: active development direction under [issue #439](https://github.com/type-rb/type-rb-native/issues/439).
This policy supersedes per-slice cost acceptance during the migration phase;
historical decisions and measurements retain their original meanings.

## Long-term objective and current scope

The long-term goal is a TypeRB-authored compiler/toolchain covering the reference
language, Go/Ruby/TypeScript emission and execution, and Native executable
output. Coverage includes the standard library and official packages as their
platform prerequisites are implemented. The reference Go implementation already
provides the three source backends; parity in the TypeRB-authored implementation
is future work. Reference semantics remain independently owned and Native must
not acquire its own dialect.

Production use is the intended destination. This includes official application
packages such as `trb/web`, `trb/orm` and `trb/jobs`, a stable user-facing CLI,
documented ABI compatibility where exposed, supported release targets and a
release/security maintenance policy. Incomplete coverage, internal unstable
interfaces and exact development pins describe the current implementation;
they do not exclude these goals. Support and compatibility claims require the
corresponding implementation, validation and published policies.

Native execution time, generated application size and end-to-end application
build time should outperform equivalent Pure Go programs across representative
workloads. Compare equivalent inputs, outputs, algorithms, concurrency, build
settings and toolchain versions. These are workload-specific measured goals,
not a promise that every possible program or metric already wins. Keep Pure Go
controls separate from TypeRB's generated Go output and from compiler self-build
cost. Include assembly/linking in application builds and account for required
external tools in distribution costs.

Current work covers basic ordinary language features, Native output, verified
MIR, source organization and the optimizations already needed by those programs.
The first consolidation inventory includes scalar expressions, calls, records,
Strings, Arrays, Hash, Range, conditionals, loops and lexical transfers.
[The basic-language contract](native-language-coverage.md), tracked in
[issue #454](https://github.com/type-rb/type-rb-native/issues/454), broadens that
inventory from pinned reference syntax and semantic probes. Complete useful
families together with their MIR dependencies, beginning with ordinary UTF-8
String behavior; do not wait for all existing MIR migration before closing
basic language gaps. The shared tests also generate the public Capabilities
detail view. A completed MIR milestone is not 100% TypeRB language coverage.

Keep checked-program type, origin and high-level semantic information available
for the later source backends. Native-specific layout, ABI and root lowering
belong after that shared semantic boundary. Basic syntax proceeds with MIR
consolidation. Three-language backend parity, wider standard-library and
official-package coverage follow their dependencies; completing one category
list does not establish those capabilities.

## Completion conditions

- Every supported ordinary function follows the verified MIR route, including
  currently direct-lowered functions. Checked operations, traps, origins, values,
  control edges and lexical ownership remain explicit.
- Portable range/index/loop relationships, allocation and mutation effects,
  Array-header stability and root-safety decisions have shared MIR owners.
  Backend adaptation consumes those decisions. The existing optimizations can
  be represented without rediscovering semantics from source/QBE text.
- Superseded ordinary paths and duplicated semantic analysis are removed.
  Retained implementation names describe responsibilities; oversized modules are resolved with their consumers. Independently
  required recovery/snapshot adapters and immutable historical evidence remain.
- Differential behavior, diagnostics, GC safety, REPL execution, ordinary
  self-hosting/fixed points, recovery and supported-target correctness pass.
- A milestone performance assessment records application runtime/build/size,
  compiler build/size/RSS and toolchain distribution. It identifies and pursues
  performance recovery before claiming qualification or refreshing formal Pages.

The previous rough 60% estimate was architecture coverage, not a remaining-effort
estimate. Track the conditions above and explicit coverage gaps instead of
counting small PRs or treating a renamed data structure as full MIR migration.

## Current integration: sole MIR emission

The current ownership change requires a MIR body for every accepted ordinary
function, moves numeric/call expansion selection to verified CFG/SSA plans and
removes the direct body emitter with its token-bound Array/header/assignment
analyses. Function ABI and root-frame emission has its own target module.
Acceptance requires ordinary core/CLI fixed points, snapshot-v4 and full hosted
recovery, portable output/failure order, malformed-plan controls and managed
lifetime tests with erased/reordered MIR. No baseline, language expectation,
seed, pin or timeout is relaxed. Cost observations use the migration policy below;
this integration is not final Pure Go qualification. See the
[current ownership status](native-mir-optimization-status.md) for retained policy
bounds and remaining optimization/coverage work.

## Default initialization checkpoint

Required and default positional/named-only function parameters and record fields
share source-order binding. Each default gets a private, declaration-scoped
initializer with a normal typed MIR signature and body. Call checking evaluates
explicit expressions first, fills omitted slots in declaration order and emits
full-arity calls. The REPL consumes the same private declaration identities.
The [lowering decision](decisions/0040-default-initializer-mir.md) records ownership
and future callable boundaries.

Acceptance includes 108 reference/Native ordinary contracts, wrong-label/order/type
and invalid-scope controls, fresh managed values under forced collection and
source-erased/reordered MIR, ordinary core/CLI fixed points and the synchronized
60-module recovery closure. Compiler self-use of authored defaults waits for an
accepted seed refresh: the current pinned seed cannot parse that syntax. The
implementation itself remains compatible with that seed. No seed, pin, baseline
or performance qualification changes are implied.

## Value-control checkpoint

Value-producing conditionals and scalar case now use typed block arguments,
including Integer/Float joins, managed results and lexical transfer branches.
Conditional transfers share parsed regions with the REPL. The independent
`mir_value_control.trb` builder leaves QBE responsible only for verified MIR
adaptation; source erasure, reordered storage and forced-collection checks cover
that boundary. See [the decision](decisions/0041-value-control-mir.md) and the
shared language inventory for the exact subset and remaining gaps.

That checkpoint contained 61 ordinary compiler modules, including the new
value-join builder. Its acceptance remains historical evidence; each subsequent
integration requires its own complete correctness authorities.

## Current basic-language integration: nominal values and Result control flow

Optional values, nil guards, safe navigation and optional numeric widening now
have typed MIR operations and control edges. Dedicated type, flow-fact and MIR
builders own the semantics; QBE consumes verified operations. Calls, returns,
defaults and managed collections retain optional payloads through shared root
planning. See [decision 0042](decisions/0042-nullable-mir.md) for the private layout
and conservative fact invalidation across assignments and loop backedges.

The ordinary compiler closure contains 82 modules. Implementation syntax stays
within the existing immutable seed and snapshot-v4 boundary; compiler self-use
of the new syntax still depends on an accepted seed refresh. The shared language
contract contains 188 cases with explicit remaining differences. Retained REPL
assignment flow now uses an ordinary checker projection, with conservative
failure/interruption invalidation and explicit replay boundaries; see
[decision 0043](decisions/0043-checked-repl-submissions.md). Ordinary enum payloads and exhaustive cases now have independently verified
nominal catalogs, typed operations and managed roots, including recursive
record/enum fields. [Decision 0044](decisions/0044-enum-mir.md) records the boundary.
Explicit generic records/enums now resolve concrete nominal catalogs before MIR;
[decision 0045](decisions/0045-generic-nominal-mir.md) records recursive identity,
REPL remapping and source erasure. Standard Result construction, prefix try,
statement-value catch and required-use checks now share these concrete enum
operations and ordinary control-flow joins; see
[decision 0046](decisions/0046-result-control-mir.md).
Generic defaults/functions/aliases, structured package propagation boundaries,
raw conversions, wider patterns/unions, full REPL display parity and final
performance qualification remain open. This checkpoint does not imply complete
basic-language coverage.

## Development loop

Use cohesive changes that remove an ownership boundary or complete a useful
family of operations. Within a PR, run focused units, differential cases, ordinary
fixed points and relevant recovery checks as the implementation changes. Run
complete hosted correctness at integration. Keep commits reviewable and preserve
bisectability, but do not require a separate PR and full performance assessment
for each helper extraction, rename or small syntax adoption.

PR and main integration explicitly select `mir-migration` cost mode. They retain
all applicable correctness, target identity, process, recovery, fixed-point,
ASan/LSan, Valgrind, GC-lifetime and cleanup authorities. Failed or missing required
jobs still reject integration. Compiler byte ceilings and smoke-time
ceilings produce retained `within-limit` or `exceeded` observations; an overrun
cannot stop those correctness checks. Invalid modes or malformed observations
are errors. Existing workload timeouts and memory-lifecycle checks remain.

Migration PRs omit the separate interleaved arm64 cost matrix. Linux
amd64 integration retains its compiler generations, binary-format/dependency
checks, application outputs and failure-order controls but omits its repeated
formal timing series. CI workflow/routing and cost-policy changes retain their
synthetic controller checks and all applicable target/recovery/runtime correctness,
without restoring old performance ceilings as a naming-cleanup prerequisite.
Standalone tools/workflows
default to `strict`; their original thresholds and full measurement series are
available and failures remain visible. No admin bypass or blanket failed-job
allowance is used. Green migration CI proves integration correctness, not
performance qualification or a passing cost comparison that did not run.

Existing daily/weekly measurement schedules remain the trend feedback loop.
Their compiler preparation also observes historical byte overruns so that
diagnostic workloads can run; measured programs and repetitions are unchanged.
Use their evidence to detect large regressions and choose investigations, without
repeatedly tuning an unchanged small overrun. A coherent architecture checkpoint
or an unexpected material change warrants a focused measurement; each small
commit does not need a new numeric allowance or investigation registration.
A concrete crash, wrong result or unsafe lifetime is still fixed immediately.

## Baselines and milestone assessment

Freeze the migration-start Native source at
`d568d9e712452f66fc9c48d6025bf73b79659661`. Preserve the earlier cumulative
baseline `ac633935a7f248470c59d22666da14c819a131fa`, existing daily/formal controls,
exact toolchain identities and all previous failed cohorts. They answer different
questions and must not be reset to hide growth. Record feature differences when
comparing compiler self-builds; use same-feature/identical-source controls where
needed. Unsupported new programs cannot be attributed to the old compiler.

At consolidation completion, run the full comparative cost and representative
runtime suites on a frozen candidate and compare with both the pre-migration
Native and equivalent Pure Go controls. Retain all observations and report which
metrics regress or win. Restore or improve existing application performance and
pursue the Pure Go goals with optimizations on the consolidated MIR. Historical
compiler-byte ceilings are reference observations, not an obligation to erase
all cost of useful language coverage. Review the complete trade-off at the
milestone and establish the subsequent acceptance contract explicitly.

The migration policy expires when issue #439's structural conditions and
performance assessment are complete. Closing it requires updating integration
routing and the documented next-phase contract; this mode must not silently
become permanent release qualification. Stable releases and final benchmark
claims cannot rely on migration CI alone. Formal Pages changes require complete
accepted formal measurements; no old result is rewritten as a new observation.
