# Ordinary Native language coverage

Status: an initial 14-case ordinary-path inventory and regression contract are
available. Basic control syntax is the next implementation checkpoint. This
inventory does not declare additional syntax supported.
Track the first bounded delivery in [issue #326](https://github.com/type-rb/type-rb-native/issues/326).

## Current development priority

The ordinary compiler is self-hosted but implements a bounded TypeRB subset.
Prioritize existing language features that make ordinary programs and the
compiler implementation clearer, without waiting for complete MIR migration
or Pure Go runtime parity. TypeRB at `TYPE_RB_REVISION` remains the semantic
authority; this work does not define a Native-only dialect.

The near-term order is:

1. Wrong results, crashes, unsafe optimization and reference-semantic mismatches.
2. Ordinary-path coverage probes and the basic control syntax: `elsif`, then
   `break` and `next`, with necessary MIR validation in the same feature slice.
3. Needed collection and value representations, selected from concrete compiler
   or application uses. Evaluate Boolean arrays and named typed data before
   extending positional Integer rows merely to work around a missing type.
4. Arguments, nullable values, enums and Result according to actual use and
   prerequisites, not a requirement to finish every feature in one category.
   Evaluate UTF-8 literal output separately from a complete Unicode API.

Existing performance, memory, process and reproducibility checks remain in
force. New benchmark-specific tuning and broad optimizer work are secondary
while these basic language boundaries are being established. Performance goals
remain unchanged; a feature is not required to manufacture a runtime speedup
to justify its existence. A failed cost bound still needs the existing
[trade-off review](optimization-tradeoffs.md), not automatic relaxation.

## Coverage is path-specific

The [generated case matrix](native-language-coverage-matrix.md) comes from
[`tools/native-language-cases.json`](../tools/native-language-cases.json).
Each row describes one bounded example, not complete support for that feature
or a percentage of the TypeRB language. The exact reference revision is pinned
in `TYPE_RB_REVISION` and recorded alongside executable and registry hashes in
each observation report.

The `while` case currently returns the same final value but differs in its
REPL value display (`[mut]` is absent after the loop). This remains an explicit
output difference. A rejected REPL submission can still leave the interactive
session with exit status zero; output and diagnostics, not just exit status,
determine the row. UTF-8 String literals pass `check` but fail ordinary build
and REPL emission. Historical snapshot support does not close that gap.

Maintain one small executable case registry and derive its ordinary coverage
table from checked expectations. Each row needs a feature, authored source,
reference revision, expected output/diagnostic, and separate observations for:

- ordinary `check`;
- ordinary build and execution (a successful build alone is not execution);
- the ordinary REPL, including declaration and expression behavior where relevant.

Report verified, rejected, inconsistent or not yet tested for the exact case,
not for an entire language category. Capture exit status and stdout/stderr;
fail the regression when an observation changes unexpectedly. A known rejection
is a tracked gap, not a passing conformance claim. Unsupported reference input
cannot establish a Native language gap. Check the reference before registering
a fixture as valid.

Keep snapshot/recovery coverage separate. Earlier aggregate/UTF-8/closure
evidence does not establish ordinary `trbn` support. A `check` success followed
by a build rejection must be visible rather than collapsed to "supported".
The first inventory covers scalar/control successes and the reported gaps:
`elsif`, `break`, `next`, default arguments, Boolean arrays, nullable Strings,
ordinary enums and UTF-8 String literals. It is not an exhaustive specification.

### Reproducing and maintaining the inventory

```sh
python3 tools/native-language-coverage-test.py
python3 tools/native-language-coverage.py --native /absolute/path/to/trbn
python3 tools/native-language-coverage.py --reference /absolute/path/to/trb
python3 tools/native-language-coverage.py --check-table docs/native-language-coverage-matrix.md
```

The reference executable must be built from `TYPE_RB_REVISION`. CI validates
every fixture with that compiler in the quick oracle job. Ordinary Native CLI
jobs independently exercise the same cases without invoking a reference
compiler. Reports are short-lived CI artifacts; do not add raw observations
to `results/`. Changing this registry routes to the quick and CLI checks, not
an unchanged compiler's performance matrices.

Use `--case ID` for a bounded probe and `--observe` to inspect changed Native
behavior before reviewing expectations. Observation mode still rejects an
invalid reference fixture and never rewrites expectations. Update a case only
after reviewing all four paths, then regenerate the table with `--table`.
Documentation-only CI checks that the table matches the registry without
building or executing a compiler. Each subprocess has a 30-second safety
timeout with owned-process-group cleanup; these are not performance tests.

## Feature delivery contract

For each bounded slice, register the exact reference and Native baseline,
semantics, coverage cases and existing cost authorities before implementation.
Then deliver parser/checker behavior, checked/MIR representation and validation,
mechanical lowering, CLI/REPL coverage, and reference differential tests.
Preserve source diagnostics, evaluation order, branch-local bindings, portable
failures and managed-root lifetimes. Do not add semantic analysis to QBE text.

For `break` and `next`, explicitly validate loop targets, nested control flow,
backedges, induction updates and root cleanup. Existing bounds/header proofs
must account for each new path; unproved cases retain their checks. General
control-flow MIR need not be completed before the feature, but the affected
semantic ownership and verifier cannot be skipped.

After feature acceptance, follow the [seed update boundary](bootstrap-seed-updates.md)
before using the syntax in compiler implementation source. Add the matching
snapshot recovery coverage when that source begins using it. Then remove the
actual flags, nesting or representation workaround that motivated the feature.
Do not count a parser-only change or a source rewrite without bootstrap tests
as completion. Keep each feature and its self-use adoption independently clear.

## Deferred Array-loop candidate

[PR #307](https://github.com/type-rb/type-rb-native/pull/307) and
[issue #303](https://github.com/type-rb/type-rb-native/issues/303) are deferred,
not accepted or abandoned. Freeze the current candidate at
`96871cce7bf8bcd39717cb2b1af992cebfdb8dcd`; retain its
[adoption review](https://github.com/type-rb/type-rb-native/blob/96871cce7bf8bcd39717cb2b1af992cebfdb8dcd/docs/native-mir-loop-bounds-adoption.md),
failed cost observations and frozen cumulative baseline. Start basic syntax
work from accepted main, not from that unaccepted optimization branch.

Reassess after the first ordinary coverage/control-syntax checkpoint, or when a
concrete representation change can reduce its maintenance or measured cost.
Its merge is not a prerequisite for language coverage. Do not automatically
renew expired measurement budgets, rerun known unchanged failures, relabel the
small gain as a passing earlier criterion, or change Pages performance values.
Any renewed adoption proposal still needs current costs, benefit uncertainty,
explicit policy and all remaining correctness/target/memory authorities.

## Checkpoint reporting

Report the ordinary coverage cases added, remaining gaps, compiler-source
cleanup enabled, MIR invariants verified, bootstrap/recovery status and measured
costs separately. Update the corresponding issue and this coverage record when
a feature passes; keep planned work distinct from accepted behavior. Publish
Pages coverage at accepted checkpoints without rerunning the formal runtime
benchmarks unless accepted runtime evidence has actually changed.
