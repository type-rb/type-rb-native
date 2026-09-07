# Array-loop small-gain adoption review

Status: in review, not accepted. This is the follow-up to the
[bounded assessment](../results/2026-09-07-array-loop-output-batching-darwin-arm64/README.md#trade-off-evaluation-outcome)
and its [review registration](https://github.com/type-rb/type-rb-native/issues/303#issuecomment-5567705631).
It does not change the original 2% contract, failed observations or ordinary
cost limits. No new optimization is a prerequisite to evaluating this candidate.

## Why review a small gain

All four local spectral cohorts improved directionally, but three missed the
registered 2% wall-and-CPU criterion. That establishes neither a passing 2%
result nor a useless optimization. A repeatable smaller benefit can justify a
modest, maintainable implementation. Sampling uncertainty, correctness and
actual cost still need review; future reuse alone is not sufficient value.

The existing candidate has unchanged application file sizes, passing diagnostic
controls and RSS, and roughly 16.5 kB of complete-compiler growth. The local
compiler-time observations differ between cohorts; retain their failures as well
as passes. Current application-build cost and cross-target formal acceptance
remain separate work, not inferred from the small compiler or old Go results.

## Ownership and maintenance review

The production diff from accepted same-feature main to `c33b105f` is about 504
net lines. This includes the 362-line proof module and separate lexer, output
batching and verifier-field refinements; it is not 504 lines devoted solely to
the Array proof. Test growth is excluded from that count.

| Responsibility | Owner | Review finding |
| --- | --- | --- |
| Checked identity, guard, writes and effects | `checked_program.trb` | Records raw checked operands; they are not optimization permissions |
| Structural proof and read selection | `mir_loop_bounds.trb` | Backend-independent, one module; replaces the old header-only analysis |
| Transformation and independent verification | `mir.trb` | Recomputes the plan and rejects forged or missing optimized marks |
| Address lowering | `compiler.trb` | Consumes verified mode 3; does not rediscover the loop from backend text |
| Recovery integration | `compiler_recovery_source.trb` | Canonical module is included in strict closure and derived recovery input |

There is one persistent Array-region owner, not parallel old/new fact tables.
The old 72-line header-only verifier is removed. Repeated plan computation at
optimization and verification is an intentional validation boundary, not a
second implementation to delete for compactness. The retained output batching,
immutable field names and two-character token recognition have independent
responsibilities and regression tests; they do not special-case a benchmark.

The principal maintenance costs are positional Integer rows, eleven operation
kinds, and a deeply nested central dispatcher. Their current layouts and
invariants are documented together and exercised by focused tests. This is
moderate, localized complexity, not a trivial peephole; it does not by itself
justify discarding a measured small gain or demand a speculative framework.
Do not expand this dispatcher with another fact family before reviewing named
carriers or responsibility-based handlers, their recovery compatibility and
cumulative cost. Any later refactor must preserve validation ordering and the
independent proof boundary, not trade them for fewer lines.

## Correctness review checklist

- Live local lookup rejects redeclaration of a still-visible name. Reused slots
  obtain new declaration-token identities; parameter ordinals occupy a distinct
  prefix. This matters because row lookup must not inherit a dead local's proof.
- Reads match the same immutable Array, index identity, version and dominating
  region. Mutable Arrays, nonzero origins, unrelated or extended bounds and
  derived indices keep their checks.
- Selection requires exactly one checked unit update. Later writes invalidate
  closed inner regions too, protecting their next invocation in an outer loop.
- Unknown effects invalidate header and bounds selection; unknown induction
  alone may retain the independent header proof. Malformed rows still fail
  after a proof has become ineligible.
- The verifier derives its expected selections independently of kind-10 marks.
  Publication occurs after verification and only for the checked source origin.
- Induction increments and other Integer arithmetic remain checked. A shorter
  output Array never inherits the input Array's bounds proof.

Existing core/connection controls cover nested loops, mutation/version changes,
truncated and forged rows, conservative effects, malformed origins and exact
diagnostics. The 252 single-field mutation cases check deterministic handling
and input preservation; they are not an exhaustive proof of soundness.

## Recovery finding and correction

The first recovery-enabled review of `c33b105f` passed all 152 compiler tests,
but the root suite failed at snapshot generation: `qbe_output_chunk` used indexed
`+=`, outside the recovery snapshot v4 subset. Ordinary Native fixed points did
not expose this distinct boundary. The failed 97-test root run remains evidence,
not a passing recovery result.

Replace both `position[0] += 1` statements with `position[0] = position[0] + 1`.
The receiver and index are side-effect-free, so this preserves the checked
increment and cursor behavior without expanding the snapshot protocol or
changing the reference language. Existing chunk tests cover exact ordering,
empty/embedded newlines, boundaries, oversized lines and repeated cursor use.
Require full recovery again on this corrected source, not just the inexpensive
ordinary fixed point. Retain distinct compiler identities and costs even if
generated applications remain byte-identical.

## Remaining adoption decision

1. Complete corrected-source recovery, target/process/cleanup and memory checks.
   Resolve any correctness or ownership blocker before performance acceptance.
2. Assess repeatability of the small runtime benefit with explicit uncertainty
   and current application artifacts. Register any new measurement before it
   runs; do not retry the expired diagnostic until a favorable cohort appears.
3. If ordinary acceptance criteria still fail, propose a separately reviewed,
   candidate-scoped small-gain/cost decision and fail-closed enforcement before
   relying on it. Do not replace the old 2% result or raise every limit together.
4. Merge only after every required authority passes the approved contract.
   Pages continues to show the previous accepted evidence until then.

The review keeps this candidate eligible for adoption; it does not require a
larger optimization first and does not grant acceptance merely because its
observed medians are lower.
