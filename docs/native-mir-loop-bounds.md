# Array-loop bounds proof diagnostic

Status: local proof-core checkpoint for [issue #303](https://github.com/type-rb/type-rb-native/issues/303),
not an ordinary-compiler optimization or a performance result. The accepted
baseline is `1afd60c2c7257ed34fd2a2aa70cb8b9164433009`. The compiler entry does
not import `mir_loop_bounds.trb`, and no adapter consumes its result yet.

## Proof boundary

The diagnostic verifies a structured projection of an already checked function.
It derives candidate read origins from immutable Array identity, a zero-origin
Integer induction value, a dominating strict length guard, and exactly one
checked unit increment. It does not accept supplied optimization facts. The
ordinary checked arithmetic, including the induction increment, remains
required even for a selected read.

Each operation has six Integer cells: kind, binding, operand, input version,
region, and source origin. Definitions have distinct identities, independent of
authored names or reusable local slots. Origins are strictly increasing. Region
entry/exit is structured and must balance; nested reads may use an ancestor
guard only for the same Array, index, and pre-update version.

| Kind | Meaning | Operand |
| --- | --- | --- |
| 1 | Array parameter | 1 immutable, 2 mutable |
| 2 | Integer definition | Initial value |
| 3 | Strict index less than Array length loop | Array identity |
| 4 | Array read | Index identity |
| 5 | Checked unit increment | 1 |
| 6 | Unknown Integer write | 0 |
| 7 | Loop close | Array identity |
| 8 | Opaque control or effect | 0 |

The verifier returns `[-1]` for malformed input or `[0, read origins...]` for a
verified stream, possibly without any selected reads. Mutable Arrays, nonzero
initializers, reads after an update, missing or repeated increments, and
unproved effects remain conservative. Input rows are not mutated.

Index writes invalidate closed regions too: a later write inside an enclosing
loop may affect the next invocation of an inner loop. Checking only the active
region stack would not cover that case. Conversely, malformed input must still
be rejected after an opaque event; disabling optimization is not permission to
stop structural verification.

The producer must record unsupported conditionals and loop shapes, unproved
calls, growth, rebinding, and uncertain aliases as opaque. This projection cannot
detect an effect omitted by its producer. It is therefore not an independent
authorization to remove a source-level bounds check.

## Local verification

The pinned reference compiler checks the compiler project and runs 13 focused
tests, including 252 single-field boundary mutations. The suite checks malformed
rows, stale identities and versions, nesting, post-update accesses, conservative
effects, input preservation, and repeatability:

```sh
trb fmt --check compiler/src/mir_loop_bounds.trb compiler/src/mir_loop_bounds_test.trb
trb check --config compiler/trbconfig.jsonc
trb test --config compiler/trbconfig.jsonc --test-name-pattern 'MIR Array loop proof core'
```

These focused checks are not the recovery-enabled full compiler/root suites,
ordinary replacement fixed points, cross-target evidence, or runtime acceptance.

## Remaining vertical connection

1. Extend the checked function's existing Array-region ownership to retain the
   raw declaration, guard, update, access, and effect relationship. Do not retain
   a second permanent producer or optimization-fact table. Scope identity must
   survive local-slot reuse; an Array-length result must not masquerade as a
   literal, namespace, mutable lvalue, or existing scalar MIR value.
2. Verify the complete projection before publishing a source-origin-indexed
   access decision. Recompute optimized decisions when verifying the MIR; reject
   forged or stale decisions. Keep Array-header reuse distinct from bounds
   authority.
3. Connect only verified decisions to mechanical address lowering. Remove
   superseded metadata for the selected subset and keep the conservative path
   for unsupported control and values. Do not add emitter-side source analysis.
4. Run executable differential controls, recovery, ordinary fixed points,
   target/process/memory authorities and the registered compiler cost bounds.
   Measure the smallest complete candidate before hosted performance acceptance.
5. Retain all same-run spectral-norm and control observations. A successful
   proof-core test does not establish an application speedup or Pure Go parity;
   Pages changes require complete accepted measurements.

No compiler allowance, benchmark condition, supported language feature, or
existing acceptance threshold changes at this checkpoint.
