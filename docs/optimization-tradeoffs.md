# Optimization costs and trade-off evaluation

Status: adopted on 2026-09-07. This policy governs future decisions; it does
not relabel any earlier failed measurement or accept an existing candidate.

## Separate the goals from the regression alarms

The product goals remain competitive end-to-end application build time and
deployed application size against the optimized TypeRB Go backend, and runtime
performance competitive with established static languages. Self-hosted compiler
cost, toolchain distribution, memory, and maintenance remain measured costs.

An application's build time is not the compiler's self-build time. Compiler
executable size, compiler text, compiler QBE, generated application size and
complete toolchain distribution are separate columns. A small-program Go
comparison is not a general budget for future features or a Pure Go build result.
Report the exact revision, coverage and age of every Go comparison; missing
matched measurements remain unknown, not inferred spare capacity.

There are two routes:

| Route | Purpose | Outcome |
| --- | --- | --- |
| Ordinary acceptance | Detect regressions against the registered Native baseline using existing limits and all correctness authorities | Eligible for normal review only when the complete contract passes |
| Bounded trade-off evaluation | Learn a promising candidate's runtime benefit even when an ordinary cost limit fails | Diagnostic evidence and an explicit decision, never automatic acceptance |

The ordinary 1.05 ratios and current absolute limits in
[`native-mir-transition-policy.sh`](../tools/native-mir-transition-policy.sh)
govern acceptance. An explicit complete-compiler budget revision for safe Array
assignment is recorded in
[Decision 0029](decisions/0029-array-assignment-compiler-budget.md); it changes
no relative limit or historical result. The separately validated
[record Array budget](decisions/0030-record-array-compiler-budget.md) retains
the ordinary structured-data implementation cost without changing those ratios.
The separately validated [scalar guard budget](decisions/0031-scalar-guard-compiler-budget.md)
retains its bounded range-analysis cost without changing those ratios.
A cost failure blocks ordinary acceptance, not necessarily
further investigation. There is no general relaxed percentage or automatic
conversion from an evaluation budget to a merge budget.

Correctness, portable semantics, memory safety, failure ordering, MIR ownership,
reproducible self-hosting, target/process/cleanup requirements and evidence
integrity cannot be traded for performance. A diagnostic may stage expensive
authorities, but must say which remain unrun; acceptance still requires them.

## Register a bounded evaluation

Before new measurements, put a public record in the candidate issue or PR with:

1. **Question and identity:** expected general-purpose benefit, exact candidate
   revision/source digests, backend/target, and any already known failures.
2. **Comparisons:** the frozen cumulative Native baseline; a same-feature
   control or narrowly described ablation to isolate the optimization; and the
   applicable Go comparison, or the explicit missing measurement needed before
   a Go-competitive claim. Retain both baselines when compatibility work moves on.
3. **Limits:** list the ordinary cost limits that fail and a numeric,
   candidate-specific investigation ceiling for each affected cost. Keep other
   limits unchanged. Include absolute bytes as well as ratios and resource/time
   limits. Explain the chosen headroom; do not inflate all limits together.
4. **Measurements:** selected and control programs, full input sizes, runtime
   wall/CPU/RSS, application build/size, compiler self-build/size and relevant
   external tools. Register repetitions, ordering, minimum useful runtime gain,
   permitted control regressions, and a bounded number of cohorts/runs.
5. **Prerequisites and stops:** correctness checks required before execution,
   remaining acceptance authorities, and explicit stops for wrong output,
   unsafe behavior, catastrophic regressions, budget exhaustion or expiry.
6. **Decision checkpoint:** expiry at a named coherent result or date, expected
   evidence, and whether to improve, propose a reviewed cost budget, defer with
   a concrete revisit trigger, or reject. Record maintenance cost and superseded
   code removal separately from unavoidable useful optimizer code.

Standing development authorization permits registering and running an in-scope
bounded diagnostic. It does not authorize silently changing ordinary CI,
acceptance thresholds, benchmark conditions, or the project's product goals.
Existing observations may motivate the registration, but retain their original
failure status and distinguish them from the prospectively measured cohort.
An expired budget is not renewed automatically. Reassessment requires a stated
question and justification, not repeated attempts until a favorable sample wins.

## Evaluate the whole trade

Report incremental cost against the same-feature control and cumulative cost
against the frozen baseline. Never reset the cumulative baseline merely to fit
the next 5% increase. Separate source growth from compiler implementation cost
where self-build comparisons compile different-sized compiler sources.

Prefer a candidate that improves representative runtime without worsening
other dimensions. If dimensions conflict, show their absolute and relative
changes without hiding them in a weighted score. Consider rebuild frequency,
runtime workload, memory, generated artifacts, portability and maintainability.
For example, a repeatable 20% runtime reduction with a 10% build-time increase
may warrant review; it is not an automatic exchange rate or acceptance rule.

QBE text size is a diagnostic signal, not a deployed artifact. Preserve its
ordinary CI check and historical values until a reviewed policy change, but do
not reject a bounded evaluation solely for QBE growth. Prioritize actual code,
complete compiler/application sizes, runtime, build costs and distribution.

Distinguish removal of duplicate/superseded emitter logic from the cost of a
useful verifier or optimization pass. Remove superseded ownership as a slice
migrates; do not require every useful new pass to become free before its value
can be investigated. A later fact-family proposal must account for outstanding
duplication and cumulative cost, rather than treating return to the exact
pre-MIR byte count as its sole eligibility condition. This does not authorize
another semantic owner, an unbounded optimizer, or premature LLVM expansion.

## Avoid both missed opportunities and budget drift

At each coherent checkpoint, record the next action and why. After two bounded
size-only attempts without a current runtime-benefit assessment, explicitly
choose a bounded benefit measurement, a cost/benefit review, or deferral with a
concrete reason before another size-only attempt. Do not let polishing a tiny
overrun become the default indefinitely. This is a reassessment trigger, not a
requirement to run expensive benchmarks for every speculative idea.

Keep a compact candidate assessment in the existing issue/result slot:
ordinary status, diagnostic budget status, runtime benefit (or unmeasured),
incremental and cumulative costs, remaining coverage, and next decision.
Retain complete active cohorts, including failures and warmups, under the
[evidence lifecycle](evidence-retention.md); do not create permanent dated
folders for each attempt. Expensive formal benchmarks remain explicitly
dispatched, not added to every PR's CI.

## Acceptance after evaluation

If ordinary bounds still fail, a successful diagnostic is insufficient to merge
the optimization. Propose a separate, candidate-scoped acceptance decision with
the measured benefit, justified budget, cumulative limits, review/retirement
conditions, and all remaining authorities. Implement any approved enforcement
change through a reviewed PR with fail-closed tests before relying on it.
Do not use an admin bypass or a diagnostic exit status to turn failed acceptance
green. Full correctness and the registered performance contract must pass under
the approved policy. Preserve the original failure and the later decision.

Pages performance values change only with complete accepted evidence. Compiler
size cleanup, a diagnostic runtime gain, and a revised policy alone do not
establish application speedup or Pure Go parity.
