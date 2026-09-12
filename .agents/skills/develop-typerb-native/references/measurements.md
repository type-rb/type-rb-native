# Performance experiments and result retention

Read for optimization acceptance, benchmark claims, diagnostic measurements,
or changes to retained results. Paths below are repository-relative.
Documentation-only edits do not start a new measurement cohort.

- Before choosing an optimization's cost/benefit path, read
  `docs/optimization-tradeoffs.md`. Keep ordinary 1.05 ratios and absolute CI
  ceilings unchanged unless a separate reviewed acceptance decision updates
  their enforcement. A cost miss is not, by itself, a reason to abandon a
  promising optimization or spend indefinitely on size-only refinements.
- Register a candidate-specific diagnostic before measuring beyond an ordinary
  cost bound: exact identities, cumulative and same-feature controls, numeric
  investigation ceilings, runtime benefit/control criteria, run budget,
  correctness prerequisites, expiry and next decision. Do not convert this into
  automatic merge authority or silently reuse a structural transition marker.
- Preserve all earlier failed results. Compare actual application build/size and
  runtime separately from compiler self-build/text/QBE/distribution costs; old
  Go measurements do not establish current or general-purpose spare capacity.
- At coherent checkpoints track incremental and cumulative cost and the next
  action. After two bounded size-only attempts without a current runtime-benefit
  assessment, choose bounded measurement, trade-off review, or justified deferral
  before another such attempt. Keep active evidence in its existing result slot.

Before importing or reorganizing `results/`, read `docs/evidence-retention.md`.
Retain only results with a current purpose in `results/active.json`. Replace
the occupied slot, update consumers and remove superseded directories in the
same PR; do not accumulate dated snapshots or archive every intermediate run.
Preserve active/public measurement cohorts, frozen comparison baselines and
seed consumers. Keep significant rejected-approach reasons in the development
history and link retired evidence to its exact Git revision. Use a verified
public archive only when detailed evidence has a durable purpose. Run the
lifecycle/global-budget check with the actual PR base before publishing results.

For executable gates, run the same differential corpus through the optimized
Go reference baseline and every active native candidate. Count frontend,
serialization, lowering, code generation, assembly, linking, runtime, sidecar,
and distribution costs according to `docs/experiment-plan.md`.

Interleave adjacent comparative measurements on shared runners, write medians
before applying bounds, and retain evidence from failed as well as successful
verification runs.
