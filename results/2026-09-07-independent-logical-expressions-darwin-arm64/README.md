# Independent short-circuit Boolean candidate

Local selection passes; full hosted acceptance is still required. This is the
independent #308 feature extracted from draft #307, without its Array-loop
proof or bounds-check optimization. It neither accepts #303 nor changes its
frozen baseline. The exact production/test source hashes are in
[source-identities.json](source-identities.json).

## Boundary and correctness

Baseline: `450ed9d1bd8a43b85cb5cfb653326d0eee42d6ec`. Both use exact reference
`47a160cae05ddc2035c7430735c4762d36bbc9c4` (0.4.6-dev). The feature includes
Boolean-only checked plans, short-circuit QBE/REPL evaluation, paired precedence,
managed RHS and failure controls, and CLI exit/history guard adoption.

- Formatting, root/compiler/CLI source checks, root units and 119 compiler
  unit tests pass. These local suites did not enable full recovery/QBE tests.
- The maintained checkout bootstrap starts from the immutable published seed
  and verifies core and CLI fixed points; the CLI/REPL/terminal suite passes.
- 78 corpus cases pass, including six added valid/invalid/runtime-failure
  cases. Every repeated QBE/diagnostic agrees, and all 72 existing cases retain
  exact baseline QBE/diagnostics. [Case inventory](corpus-status.json).
- Nine compatibility and 48 CI-routing/controller/workspace tests pass.
- Production-only snapshot-v4 generation passes. An initial invocation against
  the whole source project also selected test declarations and was rejected;
  the corrected invocation stages exactly the twelve production modules used
  by the existing CI preflight. This is not complete recovery execution.
- Extraction review reproduced a REPL precedence bug: `-1 + 2` returned `-3`
  after binary precedence changed. Unary operands now use precedence 7; new
  compiled and REPL regressions preserve `1`, grouped negation and mixed operators.

## Local ordinary compiler cost

Apple M2 Pro, macOS 26.6.2 (25G83) arm64, QBE 1.3 and Apple clang
21.0.0 (`clang-2100.1.1.101`) through `/usr/bin/cc`, target
`darwin-arm64-v0`. Warm local caches; no affinity, controlled frequency or
host-wide isolation. Other owned builds/tests finished before measurement;
unrelated host activity was not excluded. This is local selection, not a
replacement for hosted multi-target acceptance.

Reuse the [existing observer](https://github.com/type-rb/type-rb-native/blob/ba065229c96555cc968c3ed8e6797ce91991afa7/results/2026-09-06-mir-loop-bounds-diagnostic-darwin-arm64/build-cost-observer.py),
changing only its baseline revision to the independent baseline above. Each
role's compiler builds its own exact production source into the same output
basename. Two warmups and seven retained observations per role alternate order.
All 18 builds reproduce their own compiler bytes. The clock is monotonic;
wait4 records CPU and orchestration-root RSS, not summed process-tree RSS.
[All observations](build-raw.csv) and [summary](build-summary.json) are retained.

| Metric | Baseline | Candidate | Ratio |
| --- | ---: | ---: | ---: |
| Wall seconds | 1.565003458 | 1.597615625 | 1.0208384 |
| CPU seconds | 1.531564 | 1.558175 | 1.0173750 |
| Root RSS bytes | 40,157,184 | 40,189,952 | 1.0008160 |
| Complete compiler bytes | 332,728 | 332,728 | 1.0000000 |
| Mach-O text bytes | 239,932 | 241,600 | 1.00695197 |
| Compiler QBE bytes | 1,078,790 | 1,086,338 | 1.00699673 |

All ordinary 1.05 relative limits and retained 2.0 catastrophic observations
pass. The absolute transition ceilings are unchanged. Code/QBE grow modestly
to implement a language capability; no strict shrinkage or runtime speedup is
claimed. Complete file equality alone does not mean generated code is identical.

Candidate compiler SHA-256:
`27e9b31aa836bb1924ccaa995317d7f9b471e735400e8f6156e8ae60e9cdd36c`.
Candidate compiler QBE SHA-256:
`831d0ac4af8eb150c3783cfe959c1d29d9d36b3adeb41270a21e29b1c2214ed7`.
Baseline compiler SHA-256:
`e72fa28597cdb5e88520756c7e98e67f9e0bce90f5561c96767cae6fad62f180`.

Before merging, require exact-head recovery, target/process/memory, CLI and
hosted cost authorities. No Pure Go comparison or Pages performance refresh is
authorized by these feature-selection results.
