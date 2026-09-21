# TypeRB Compatibility

TypeRB Native currently follows exact reference revisions during development. The
current source and semantic oracle is TypeRB
`04d5ecf23a546abad5bd72ac283756282edb365f` (the `0.4.9-dev` development identity), recorded
in `TYPE_RB_REVISION`. This declares one exact reference identity during Native
development, without claiming a supported version range.

The machine-readable
[`compatibility/current.json`](../compatibility/current.json) records this
exact mapping beside the independent Native `0.1.0-dev` implementation
identity. Its strict schema and CI validation keep TypeRB, bootstrap, MIR,
runtime ABI, backend, target, and evidence identities separate. The current
target list contains the internal Darwin arm64 and Linux arm64 seed
profiles plus the independently recovered and verified internal Linux
amd64 profile. See
[Native versioning and compatibility](versioning.md) for bump and release
rules.

The declaration-import compatibility work was registered in
[issue #97](https://github.com/type-rb/type-rb-native/issues/97). Its
[Darwin/Linux arm64 result](https://github.com/type-rb/type-rb-native/blob/bd483cfc5b51035d9fac193a74ee9d0eda2419ed/results/2026-08-30-typerb-0-4-compatibility-darwin-linux-arm64/README.md)
passes the selected `0.4.1-dev` reference, previous-seed, exact fixed-point,
process, elapsed-time, peak-RSS, and compiler-size criteria. The `0.4.3-dev`
successor is registered in
[issue #106](https://github.com/type-rb/type-rb-native/issues/106), and its
[Darwin/Linux arm64 result](https://github.com/type-rb/type-rb-native/blob/bd483cfc5b51035d9fac193a74ee9d0eda2419ed/results/2026-08-30-typerb-0-4-3-compatibility-darwin-linux-arm64/README.md)
passes the selected-reference, explicit setup-transition, exact fixed-point,
process, elapsed-time, peak-RSS, and compiler-size criteria. This document
records the implementation boundary independently of those measurements.
The earlier scoped-file successor is registered in
[issue #144](https://github.com/type-rb/type-rb-native/issues/144), and its
[Darwin/Linux arm64 result](https://github.com/type-rb/type-rb-native/blob/5cf61c740aa600c34ed94f1b130ea2ffefd9e783/results/2026-08-31-typerb-0-4-4-compatibility-darwin-linux-arm64/README.md)
passes the selected-reference, migration, exact-baseline, target-regression,
fixed-point, process, resource, and size criteria.

## Builtin values and Unicode reference update

The current pin additionally incorporates
[TypeRB #792](https://github.com/type-rb/type-rb/pull/792). Standard Result and error
types retain canonical identity across local shadows and imported aliases, and
raw-enum conversions no longer select an unrelated same-named record. The shared
raw-enum error case now compiles and executes in both implementations. String
transforms use this accepted reference; Unicode output-mode case differences
remain tracked in [TypeRB #791](https://github.com/type-rb/type-rb/issues/791).

The exact pin incorporates [TypeRB #788](https://github.com/type-rb/type-rb/pull/788),
[#789](https://github.com/type-rb/type-rb/pull/789) and
[#790](https://github.com/type-rb/type-rb/pull/790). Go output preserves distinct
Unicode identifier spellings, unsupported Unicode source characters produce
original-character diagnostics, and safe builtin operations retain imported
Result/error aliases in generated code. These are independent reference compiler
corrections with Go, Ruby, TypeScript and REPL controls.

Native pairs ordinary Unicode names and safe collection/number operations against
this accepted source and exact AST. Recovered Native generations also exercise
Unicode input; the Go-hosted recovery frontend's ASCII fallback remains explicit.
Shared observations preserve remaining Hash/NUL presentation differences and
contextual empty-collection gaps. No release or immutable bootstrap seed changes.

## Namespace binding reference update

The exact pin includes [TypeRB PR #786](https://github.com/type-rb/type-rb/pull/786).
Lowercase namespace declarations retain shared lexical storage across methods,
closures and REPL replay, and calls invalidate stale nullable proofs for mutable
values. Native uses the existing typed global MIR operations and roots. Nested
and reopened namespaces preserve lexical visibility before later inner bindings.
Qualified lowercase member access remains a reference boundary in
[TypeRB #787](https://github.com/type-rb/type-rb/issues/787), and Ruby namespace
collisions are independently tracked in [#785](https://github.com/type-rb/type-rb/issues/785).
The exact accepted source, AST and ordinary paths are checked; no release or
immutable bootstrap seed changes.

## Function binding identity reference update

The exact pin incorporates [TypeRB PR #784](https://github.com/type-rb/type-rb/pull/784).
The REPL resolves checked named-function references by declaration identity, so
later same-named variables do not redirect earlier bodies, defaults or closures.
TypeScript calls preserve the complementary lexical value selection. Shared
ordinary and retained-session cases review both earlier and later references,
including generic bodies and explicit replay. No bootstrap seed or release
version changes.

## Global binding reference update

The exact pin incorporates [TypeRB PR #782](https://github.com/type-rb/type-rb/pull/782).
Lowercase source-module variables keep checked declaration identity across all
three generated targets and the REPL. Ruby methods can read the same storage,
later local declarations cannot capture an earlier global reference, and separate
source modules remain independent. Calls invalidate nullable proofs for writable
globals; fresh guards and immutable values remain valid.

Native follows the file/project contract with typed global reads and writes.
Interactive variables also share cells with later named functions and anonymous
captures, while authored lexical order and initialization effects are retained. The exact AST, ordinary
paths, lifetime checks and recovery are rechecked at this accepted revision;
the immutable bootstrap seed and release versions are unchanged.

## Newtype reference update

The exact pin incorporates [TypeRB PR #777](https://github.com/type-rb/type-rb/pull/777).
Conflicting newtype declarations produce diagnostics without a checker crash.
Transparent aliases retain nominal construction, Integer-to-Float conversion is
explicit in typed IR, and inferred union representations retain their storage
in generated Go. All three portable targets and the REPL have controls. The pin
also incorporates [PR #776](https://github.com/type-rb/type-rb/pull/776), normalizing
successfully decoded String literals before backend emission. The full remaining
single-quote contract is still tracked separately in TypeRB #748.
Shared observations and the reference AST inventory are reviewed at this accepted
revision. This changes neither the release version nor the immutable Native seed.

## Sorting reference update

The exact pin incorporates [TypeRB PR #773](https://github.com/type-rb/type-rb/pull/773).
Descending natural and key-based Array sorting in the REPL now retains NaNs
after ordinary numbers without reversing equal keys or signed zeros. All three
portable modes have compiled/REPL controls. The later safe-block reference update
below resolves [#774](https://github.com/type-rb/type-rb/issues/774).
This changes neither the release version nor the immutable Native bootstrap seed.

## Generic enum alias reference update

The exact pin also incorporates [TypeRB PR #771](https://github.com/type-rb/type-rb/pull/771).
Transparent aliases retain specialized enum methods in Go output and the REPL,
including nested imported generic aliases. Defaults, closures, nullable argument
laziness and lexical privacy are covered across the three reference backends.
This closes [TypeRB #770](https://github.com/type-rb/type-rb/issues/770); remaining
reference defects below stay explicit. The release version and immutable Native
bootstrap seed are unchanged.

## Enum call reference update

The exact pin incorporates [TypeRB PR #767](https://github.com/type-rb/type-rb/pull/767)
for lazy nullable enum calls, receiver-before-argument evaluation, methods returning
functions, and local/imported raw enum aliases. Shared observations use this exact
checkout and AST. Reference REPL initializer replay and canonical error-record
shadowing remain explicit in [#768](https://github.com/type-rb/type-rb/issues/768)
and [#769](https://github.com/type-rb/type-rb/issues/769). This update does not
publish a release or change the immutable Native bootstrap seed.

## Safe collection block reference update

The exact pin incorporates [TypeRB PR #775](https://github.com/type-rb/type-rb/pull/775).
Safe block calls retain their receiver, skip operation arguments and the body
when absent, and preserve nullable transform results. Indexed blocks put the safe
operator before the operation, as in `values&.each.with_index`. Nullable collection
literals and nested Ruby concurrent blocks retain their types and bindings.
The shared AST inventory and old safe-sort rejection probe are reviewed against
this accepted reference; the earlier issue #774 is resolved by that change.

## Union and inferred declaration reference update

The exact pin incorporates [TypeRB PR #761](https://github.com/type-rb/type-rb/pull/761)
for qualified generic alias construction, [PR #762](https://github.com/type-rb/type-rb/pull/762)
for imported inferred constant types, and [PR #763](https://github.com/type-rb/type-rb/pull/763)
for union storage, nullable conversion, discard patterns, generic substitution
and inferred Nil collections. Shared observations are reviewed against this exact
checkout and AST. Remaining grouped and nullable-alternative boundaries are
tracked in TypeRB [#764](https://github.com/type-rb/type-rb/issues/764) and
[#765](https://github.com/type-rb/type-rb/issues/765); nullable literal-union
comparisons are tracked in [#766](https://github.com/type-rb/type-rb/issues/766).

## Namespace and declaration identity reference update

The exact development pin includes [TypeRB PR #753](https://github.com/type-rb/type-rb/pull/753)
for module member and constant identity, [PR #754](https://github.com/type-rb/type-rb/pull/754)
for raw enum ownership, and [PR #757](https://github.com/type-rb/type-rb/pull/757)
for Go type/function name collisions in nested and imported modules. It also
includes [PR #751](https://github.com/type-rb/type-rb/pull/751) for keyword Symbol
literals, and [PR #760](https://github.com/type-rb/type-rb/pull/760) for scalar
constant copies, reopened module scopes, cross-target constant names and
dependency-ordered REPL initialization. Shared observations must be reviewed against this exact checkout and
AST; a reference fix does not silently change an existing expectation.

This is a development reference update. Releases, immutable bootstrap seeds and
historical measurements retain their separate identities.

## Named functions and Hash literal reference update

The exact development pin incorporates [TypeRB PR #743](https://github.com/type-rb/type-rb/pull/743)
for named function values, [PR #744](https://github.com/type-rb/type-rb/pull/744)
for nullable callable rejection and [PR #745](https://github.com/type-rb/type-rb/pull/745)
for callee selection before arguments. Required positional function signatures
retain declaration and nominal identities; defaulted, named-only and generic
functions require explicit typed adapters. Optional record callback calls skip
arguments when their receiver is absent.

[PR #746](https://github.com/type-rb/type-rb/pull/746) preserves Hash literal
key/value evaluation order and duplicate-key overwrites across backends and the
REPL. The pin also includes [PR #741](https://github.com/type-rb/type-rb/pull/741)
for Float negative zero and [PR #742](https://github.com/type-rb/type-rb/pull/742)
for Array edge-method arity. Review all shared observations, including the new
named-function and colon-key cases, against this exact source and AST.
This is a development reference update, not a release or immutable seed refresh.

## Array mutation and library-result reference update

The exact development pin includes [TypeRB PR #740](https://github.com/type-rb/type-rb/pull/740).
Array `push`, `unshift`, `concat` and `join` retain the receiver before argument
effects, then read that Array's current storage. TypeScript `concat` also waits
until the right operand has been evaluated before copying left-hand elements.
Native mutation cases preserve the same rule in ordinary programs and the REPL.

The pin also incorporates [PR #738](https://github.com/type-rb/type-rb/pull/738)
for Function results from library methods and
[PR #739](https://github.com/type-rb/type-rb/pull/739) for outer generic arguments
whose names coincide with bound library parameters. Review the two previously
rejected reference cases and all existing expectations when adopting this pin.
It is an exact development commit, not a release or immutable seed refresh.

## Array lookup reference update

The current development pin includes [TypeRB PR #737](https://github.com/type-rb/type-rb/pull/737).
Array `slice`, `try_slice` and `try_fetch` retain the receiver before evaluating
their argument, then use that Array's current storage. Argument-side rebinding
no longer redirects compiled Go lookup to another Array. The pin also includes
[PR #736](https://github.com/type-rb/type-rb/pull/736) for value queries,
[PR #730](https://github.com/type-rb/type-rb/pull/730) for nested collection
expressions and REPL completion, and
[PR #732](https://github.com/type-rb/type-rb/pull/732) for streamed Range transforms.

This is an exact `0.4.9-dev` commit, not a release. Shared expectations must be
reviewed against the new ordinary execution and REPL observations. Historical
measurements and immutable bootstrap seed identities retain their original pins.

## Sequential Array transform reference update

The current development pin includes [TypeRB PR #729](https://github.com/type-rb/type-rb/pull/729).
It aligns sequential traversal across Go, Ruby, TypeScript and the REPL. Shared
cases review live Array mutations, retained selection values and source/initial
ordering. This is an exact development commit, not a new TypeRB release.

The update also incorporates already merged fixes for nullable interactive
assignments, recursive enum emission, generic imports/defaults, type aliases,
callable defaults and nested brace controls. Their reviewed outcomes replace
stale reference failures; remaining REPL declaration/display differences are
preserved. [Integration evidence](../results/2026-09-07-string-escape-reference-compatibility/README.md)
records the current validation state. Frozen measurements and seed pins are unchanged.

## TypeRB 0.4.7 reference update

The release includes [TypeRB PR #686](https://github.com/type-rb/type-rb/pull/686),
which preserves parameter boundaries after nested generic annotations, and
[PR #687](https://github.com/type-rb/type-rb/pull/687), which completes REPL input
containing conditional transfers. The shared language contract now includes a
nested Hash parameter followed by an Integer parameter through check, build,
execution and REPL. Its conditional-transfer reference REPL expectation changes
from incomplete input to the same output as the compiled program. Native's
unsupported conditional-transfer outcomes remain explicit coverage gaps.

Reference builds use `tools/build-reference.py`. It validates the
compatibility manifest, exact clean checkout and source version, embeds the
declared reference version, and verifies the executable's report. The release
source retains `0.4.7-dev`; the explicit `0.4.7` build identity avoids depending
on whether a shallow checkout has fetched the release tag. Historical experiment
pins, immutable seeds and retained measurements keep their original identities.

## Release integration

Treat a new reference release as a compatibility update through a Native PR.
After the public release workflow succeeds, resolve the stable tag to its exact
merged commit. Update `TYPE_RB_REVISION`, the manifest, maintained current
workflow/controller identities and generated coverage views together. Build
through `tools/build-reference.py` and rerun the shared language cases against
the exact reference AST. Review changed outcomes before editing expectations;
reference fixes can expose Native gaps that must remain visible.

Complete the PR's required correctness, recovery, target and memory authorities
before merging. Preserve frozen experiment pins, immutable seed assets and
historical evidence. A future release detector can prepare this PR, but must
not update the default branch or rewrite conformance expectations automatically.
This consumer-owned procedure requires no Native-specific reference API or
release hook in the TypeRB repository.

## Range endpoint reference update

The pin includes [TypeRB PR #680](https://github.com/type-rb/type-rb/pull/680)
and [PR #681](https://github.com/type-rb/type-rb/pull/681). Go Range construction
retains the evaluated start before evaluating the end expression, including
when the end mutates a captured start binding. Inclusive, exclusive and reversed
ranges share this evaluation rule. ORM range predicates use the same constructor.
[PR #682](https://github.com/type-rb/type-rb/pull/682) changes development guidance;
its compiler source is unchanged from `c030ef671798a10abea01c4ac89fa18ffde79f82`.

The exact pin also includes [TypeRB PR #683](https://github.com/type-rb/type-rb/pull/683),
which checks Range element arguments during assignability. Unsupported Range
annotation lowering remains tracked separately in
[TypeRB #684](https://github.com/type-rb/type-rb/issues/684); Native admits only
`Range<Integer>` in this slice.

The maintained coverage registry now accepts direct ordinary Range iteration.
The captured-endpoint case still requires unsupported function literals and
retains their explicit rejection. [Ordinary Range support](native-range.md)
does not add a snapshot export operation or authorize compiler-source self-use.
Existing immutable seed identities and older compatibility cohorts retain their
original reference and Native identities.

## Collection iteration reference

The pin includes [TypeRB PR #671](https://github.com/type-rb/type-rb/pull/671),
[PR #676](https://github.com/type-rb/type-rb/pull/676), and
[PR #677](https://github.com/type-rb/type-rb/pull/677). Direct and Iterable-bound
Range iteration retain captured bounds and consume values incrementally. Array
`each` retains its receiver and observes current length and elements, including
mutation and reallocation during the block. Batches keep their requested size,
own fresh shallow Arrays, and do not resume an exhausted iterator after the
final partial batch. Reference REPL iteration has no fixed count cap.

These fixes establish the oracle for [ordinary Array iteration](https://github.com/type-rb/type-rb-native/issues/410).
Pinning does not itself add ordinary Native Array/Range iteration. Existing immutable seed identities remain unchanged.

## Array iteration snapshot update

The pin also includes [TypeRB PR #679](https://github.com/type-rb/type-rb/pull/679).
Snapshot v4 lowers direct Array `each` and `each.with_index` to existing Array
operations and control-flow edges. It retains the evaluated receiver, reads
live length and elements, carries outer bindings across edges, and preserves
nearest-loop transfers and method returns. Capture discovery includes iteration
sources and bodies. No snapshot opcode or format version changes.

Maintained `array-iteration-values` and `array-iteration-managed` recovery
fixtures exercise evaluation, mutation, rebinding, lexical shadowing, nested
and mixed loops, empty sources, early return, managed records, function values,
nested Arrays, Boolean and String elements. Collections inserted after Array
access/mutation verify roots; the managed fixture also triggers automatic
collections. Hash recovery shares the same fixture runner without changing its
existing outcomes or collection checks.

Float Arrays, Range/Iterable sources, batches, and result-producing iteration
remain outside this snapshot subset. This source-recovery coverage and the
ordinary iteration implementation remain separate from the immutable seed
handoff required before compiler implementation source adopts `each`.

The [full accepted integration](https://github.com/type-rb/type-rb-native/actions/runs/34630338541)
at `d2980f14d1b64e5ce3544dd7133e7f5871644e4e` validates reference `570bf6f64c7ca2412d0b4ffe06cd186cd53bdf4c`:
109 root and 200 compiler tests, ordinary/recovered generations, managed runtime,
CLI/REPL, all three targets and ordinary cost bounds pass. The parent ordinary
implementation was accepted separately in PR #418. This current CI proof does
not relabel the older retained compatibility cohort or immutable seed evidence
in `compatibility/current.json`. The [verified Array iteration seed handoff](bootstrap-seed-updates.md#current-verified-checkout-seed)
records the separate preparation, immutable publication and fresh actual-asset
verification. Compiler-source adoption follows the checkout and amd64 bridge
handoff; the historical compatibility cohort remains unchanged.

## Record Array snapshot update

The current pin includes [TypeRB PR #663](https://github.com/type-rb/type-rb/pull/663).
Snapshot v4 preserves nominal record Array elements through aliases, nesting,
function returns and closure captures without adding an operation or changing
its schema. The recovery layout boxes records stored in Arrays consistently
throughout the module; roots and descriptors retain scalar-only records and
records containing managed fields after their constructing call returns.
Ordinary record Arrays and their compiler-source self-use remain separate
stages with the prerequisites in [language coverage](native-language-coverage.md#named-record-arrays).

The pin also includes the independent data-field call diagnostic and imported
nominal-contract corrections in [PR #661](https://github.com/type-rb/type-rb/pull/661)
and [PR #662](https://github.com/type-rb/type-rb/pull/662). These resolve the
record Array investigation's checker discrepancies, without claiming broader
same-named declaration code-generation support.

## Stable Array assignment targets

The current pin includes [TypeRB PR #659](https://github.com/type-rb/type-rb/pull/659).
Indexed assignment retains the evaluated Array and validated nonnegative
position before the RHS, then validates that position in current storage at
the final store. Compound assignment uses the old value saved before the RHS.
The checked source projection pairs Array target and store origins; its
verified plan directs owner retention, position capture and final address
resolution. Its tagged slot holds either a binding address or a validated
Array position beside the owner; checked mutability is not copied into
emitter metadata. The adapter no longer writes an element address held across RHS
calls. Managed owners and saved compound values remain rooted across calls.

The ordinary fixtures cover growth, aliasing, index-side mutation, nested owner
replacement, managed old values and initial bounds failure. The separate
`array-assignment-recovery` case verifies the same rule through snapshot v4.
Boolean and named record Arrays are covered by subsequent ordinary slices.
Short-circuit assignment syntax remains outside the ordinary subset; the
assignment repair itself adds no source forms or collection methods.

Validation and acceptance for this correctness slice follow
[issue #342](https://github.com/type-rb/type-rb-native/issues/342), including
full recovery suites, ordinary regeneration, conformance, GC and unchanged
compiler/application cost checks. Reference pinning alone is not acceptance.

## Loop-transfer snapshot update

The current pin includes [TypeRB PR #657](https://github.com/type-rb/type-rb/pull/657).
Snapshot v3/v4 now encode `break`, `next` and early method returns in `while`
with existing jumps and block arguments. The `loop-transfer-recovery` fixture
checks live managed bindings, nested targets, condition effects and returns
through v4 program decoding, recovery QBE generation and execution. The format,
v2 boundary and ordinary language semantics remain unchanged.

The reference update accompanies the separately registered loop-transfer seed
refresh and exact Linux amd64 setup source bridge. Neither registration nor
pinning replaces full acceptance or post-publication seed verification.

## Statement conditional snapshot update

The current pin includes [TypeRB PR #655](https://github.com/type-rb/type-rb/pull/655).
It encodes statement `elsif` with existing v3/v4 branches, jumps and block
parameters, preserving ordered conditions, lexical scopes and terminating
branches. It does not expand conditional expressions or the v2 snapshot subset.
The `elsif-recovery` fixture now runs through v4 encoding, strict decoding,
recovery QBE emission and execution as well as current ordinary generations.

This pin is a prerequisite for compiler-source self-use. Complete recovery,
ordinary fixed points, target, memory and cost acceptance remain required;
updating a reference pin does not replace a verified checkout seed.

## String escape reference update

The pin also includes the portable String escape fix in
[TypeRB PR #651](https://github.com/type-rb/type-rb/pull/651). Merge that
reference PR before this dependent update. Double-quoted source accepts `\#`
as a literal hash, respects backslash parity before interpolation, and rejects
unknown escapes. JSON history data retains its separate JSON escape rules.

Moving the oracle to `0.4.6-dev` also requires typed `Path` arguments in the
repository-owned file adapter and immutable record fields in the CLI. Mutable
editor cells use Arrays; session transitions return replacement records.
These changes preserve the portable rules without adding reference aliases.
The [current validation record](../results/2026-09-07-string-escape-reference-compatibility/README.md)
separates local reference checks from hosted Native CLI and fixed-point checks.
The PR's full recovery, target, memory and performance authorities remain
required before acceptance. Earlier measurements below retain their original
revisions and do not establish performance at the new pin.

## TypeRB 0.4.4 source compatibility revalidation

The selected revision contains the TypeRB 0.4.3 release, the advance to
`0.4.4-dev`, receiver-only canonical built-in ownership, scoped file and
directory APIs, repeated scalar CLI options, corrected safe-navigation
evaluation, CLI application failures, and a focused undeclared-value
diagnostic correction.

At that revision Native did not use the changed CLI or safe-navigation surfaces. Its
direct source break was removal of `trb/std/filesystem`. All 39 affected root,
compiler-test, and historical benchmark-controller sources now use identical
repository-owned support. Reads are scoped and bounded to 67,108,864 bytes by
default, writes use `FileMode::Write`, and recursive test-directory creation
invokes exact `/bin/mkdir -p` through shell-free `Process.run`. This support is
not imported by the canonical self-hosted compiler closure and does not add a
Native compatibility alias to TypeRB.

The selected formatter and checker pass every checked-in configured project.
Executable tests cover successful and oversized bounded reads, truncating
writes, recursive and idempotent directory creation, and deterministic failure
fields. Existing Linux amd64 and arm64 regressions retain exact target-neutral
QBE. The Darwin and Linux arm64 previous-Native chains produce compiler and QBE
identities that are byte-identical to the registered Native baseline.

## TypeRB 0.4.3 semantic revalidation

The selected revision includes the TypeRB 0.4.1 and 0.4.2 releases, owner-
qualified Web API changes outside the current self-hosted subset, shared Array
alias fixes in the Go backend, nested Go runtime-helper propagation, and the
distinction between Nil values and Void results.

`compiler/conformance/valid/array-aliases.trb` turns the relevant Array
change into an executable compiler differential. It grows one Integer Array
through two aliases, mutates it through a mutable parameter, rebinds that
parameter to a different Array, and then mutates the original through the
second caller alias. Recovery and current Native compiler generations plus the
same TypeRB-authored compiler built by the selected Go reference must emit
byte-identical QBE and produce the same output. This preserves three portable
rules:

- assigning or passing an Array preserves its outer reference identity;
- destructive growth and element updates remain visible through every alias;
- rebinding a `mut` parameter changes only that local binding and never writes
  a replacement Array into the caller binding.

The selected reference checker also distinguishes a Nil value from a Void
result. Repository-owned source is formatted, checked, and tested by that
checker. Native does not infer full nullable or Void compatibility from this
pin: unsupported language surface remains outside the self-hosted subset and
must still fail explicitly.

## Current declaration-import mapping

The self-hosted frontend preserves canonical declaration identity for its
implemented declaration families:

| TypeRB behavior | Current Native behavior |
| --- | --- |
| Named import | Selects an exact supported record, enum, function, alias, module or constant declaration |
| Named `as` alias | Changes only the local binding; canonical declaration identity remains exact |
| Bare project import | Selects one matching supported record, enum, generic nominal, alias, module or constant root |
| Bare `as` alias | Selects the same unique declaration first, then changes its local binding |
| Root key | Removes ASCII `_` from the logical final path segment and folds ASCII case; declaration names fold ASCII case without removing `_` |
| Directory entry | A resolved `name/index` module uses `name` as its logical root segment; `name` and `name/index` can resolve to that same module |
| Direct/index conflict | Rejects a resolved graph containing both `name` and `name/index`; there is no precedence between two loaded module identities |
| Duplicate identity | Rejects importing the same declaration identity again, including through a different alias or equivalent index path |
| Binding and usage | Rejects duplicate local bindings, local-declaration collisions, missing exports, and unused aliases under their local names |

Bare imports do not create lowercase namespaces and never import every export.
A top-level function remains available through an exact named import but cannot
become a bare root. Zero matches, multiple matching declaration roots, and a
function-only match produce deterministic diagnostics.

Nested and reopened modules, owned declarations, runtime constants, generic
nominals and transparent aliases retain lexical identity. Classes, interfaces,
newtypes, general package activation and project-aware formatter rewrites remain
coverage work. Selected compiler-owned standard packages have explicit mappings;
unsupported imports do not fall back to a namespace or loaded-identity precedence
model. Repository-owned TypeRB source is still formatted and checked by the
pinned reference compiler.

## Source pins and bootstrap seeds

The quick PR job validates reference checkout configuration before downloading
or building the reference compiler. `tools/compatibility_manifest.py` inventories
all 13 checkouts in 12 maintained workflows, their post-checkout identity checks,
and the Linux amd64 controller pin. Missing, added, or changed consumers require
an explicit validator update. Mutation tests exercise each checkout separately.
The later executable version check remains required before matrix fan-out.

Snapshot validation, PR validation, worker memory, formal runtime/build benchmarks, and
the Linux amd64 workflow follow `TYPE_RB_REVISION`. Daily and weekly workflows
derive it from the checked-out file before their reference checkout. The
Array-push, temporary-push GC, and dynamic-Array-address experiments retain
`bae19032aa1bb7b263bc827d02606edc6e981c52`; both historical portable-entry checkouts retain
`5dc09070cf7f88a569279f5e63982a6de59d692c`. These historical pins are checked
explicitly and must not be advanced with the current development oracle.

This is a strict check of the maintained block-mapping and shell spellings,
not a general YAML or shell interpreter. Post-checkout Git identity and the
reference executable version are still checked when the workflows run.

The reference pin and a Native bootstrap seed answer different questions:

- `TYPE_RB_REVISION` selects the exact syntax, semantics, formatter, and
  differential oracle used for current development.
- A Native seed is an executable predecessor used to compile the current
  TypeRB-authored compiler. Its source-era metadata records provenance; it does
  not constrain the source revision that a later compatible compiler may
  accept.
- The immutable
  [`bootstrap-seed-2026-08-30`](https://github.com/type-rb/type-rb-native/releases/tag/bootstrap-seed-2026-08-30)
  remains unchanged. When its embedded runtime or link policy predates current
  source, compatibility uses separately identified setup-only Native
  transitions before proving exact current B2/B3/B4 fixed points. The
  transitions remain Go-free and outside candidate timing and size claims;
  they do not replace or relabel the seed.

A later seed is warranted only by a concrete distribution need demonstrated by
the compatibility chain. The existing attested seed reaches the exact
`0.4.4-dev` fixed point on both targets through two setup-only transitions.
That confirms bootstrap feasibility without making the older embedded runtime
free: a future seed containing the current runtime can remove both transitions.
Revision alignment alone does not warrant replacing or relabelling the seed.
The Linux amd64 target demonstrates the complementary case: it is recovered
from the immutable seed release's target-neutral root QBE, not from an amd64
seed executable. Its exact current chain and workflow are therefore recorded
as target-chain evidence in compatibility schema version 2, while the
immutable seed manifest remains unchanged. See the
[Historical Linux amd64 result](../results/2026-08-31-gate6n-linux-amd64/README.md) and
[Decision 0026](https://github.com/type-rb/type-rb-native/blob/7726ff18e9230cd149e9f0c317577f6429f907fc/docs/decisions/0026-recovered-target-chain-evidence.md).
Native SemVer is independently defined. TypeRB compatibility ranges, stable
installation and release-support policies remain implementation work toward the
[production-use goal](mir-consolidation.md). The current schema can express only
this exact verified TypeRB revision; broader claims require evidence and an
explicit schema/policy update.
