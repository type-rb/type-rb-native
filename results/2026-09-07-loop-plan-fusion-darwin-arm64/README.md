# Array-loop plan fusion diagnostic

Status: **build-cost limit still missed; not accepted**. This is a distinct
maintenance candidate for [#303](https://github.com/type-rb/type-rb-native/issues/303)
over `31201da6186cf5b2161fb8e0c94c304cc18bd087`, including its unaccepted
short-circuit Boolean implementation. It does not move the frozen baseline,
relax a limit, establish a runtime speedup, or authorize a Pages update.

## Change

The structural Array-loop verifier now validates parameter ordinals and selects
the first eligible immutable Array header in the same traversal. The two
subsequent whole-stream scans are removed. Opaque effects invalidate earlier
header selections and prevent later selections; unknown induction alone still
retains header authority. Malformed suffixes remain errors even after an
opaque effect. Partial results stay private until full validation succeeds.

The optimizer and post-optimization verifier still independently recompute the
plan. No verification boundary or malformed-input check has been skipped.
The generic-ID proof wrapper moves to its test file, and the now-unshared
failure-result helper is removed. Production source shrinks by 34 lines.
No new source analysis is added to the QBE adapter.

## Exact candidate

`candidate.patch.json` contains the exact patch over that revision. `source-sha256.txt` identifies
the complete compiler and test sources used for the final observations.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| B2 / B3 / B4 compiler | 349256 | `f4ba57c1f0ef01288883fb73881f1c121bd79b57d6583154bfc62fa8f25443c8` |
| Compiler QBE | 1114304 | `b7ef3351492a6d963645803c83ea4d42d503a6391d4c43f219bc1e136803d1ed` |
| Mach-O text | 249192 | — |

Compared with the preceding logical-expression checkpoint, QBE shrinks by
2784 bytes and text by 244 bytes; the complete executable is unchanged.
The source remains inside the existing absolute ceilings, but this does not
override the relative build-cost failure below.

The maintained published-seed bootstrap reproduces the same core, then builds
the CLI with SHA-256
`f05c5ccc4976cead737eeea4735f48bfa5c68c3b191f553c709759fc73a7f664`.
Its immutable Darwin seed remains
`ef438d13598c534766334b408a39715c56ff1b69db528910ebf7d90ec7720b65`.
The setup generations are distinct from the final steady ordinary chain.

## Correctness

- 148 compiler tests and 95 root units pass. Optional recovery/QBE environment
  variables were not enabled: these are not complete recovery evidence.
- All 81 conformance cases pass at B2, B3 and B4 (243 retained status rows).
  Repeated and adjacent QBE and same-basename compiler bytes match. Invalid
  inputs retain exact diagnostics and launch no probe tool; executable cases
  retain output, failure status, and temporary-file checks.
- Three new connection tests cover all header access kinds, first-eligible
  ordering, mutable parameters, opaque/unknown-induction distinctions, malformed
  suffixes, and canonical parameter ordinals.
- `plan-differential.trb` compares old and new planners on 1530 single-cell
  mutations spanning valid loops, unknown induction and opaque effects. It
  prints `1530`, with no mismatch. To reproduce, place this driver next to
  `old_bounds.trb` extracted from the parent revision and `new_bounds.trb` from
  this candidate, then build it with the preceding verified Native compiler.
- The maintained published-seed core/CLI build, CLI/REPL/terminal tests,
  38 orchestration tests, formatting, both reference type checks, and compiler
  project/layout policy checks pass.
- The three numeric benchmark QBE outputs are byte-identical to those emitted
  by the preceding logical-expression compiler. There is no new application
  runtime measurement or Pure Go claim.

On identical current source, both compilers' opt-in check statistics report
251424131 allocated bytes, 162 collections and 7748691 peak managed-heap
bytes. This removes traversals and code, not allocations. These internal
statistics are not a whole-process leak or peak-RSS test.

An earlier signature placed the Boolean argument after a nested Array type;
the pinned reference rejected that spelling while Native accepted it. The
final signature keeps the nested Array argument last and passes both checkers.
Earlier prototypes are not included in the final cost cohort or substituted
for the exact candidate above. The compatibility pin remains unchanged.

## Build cost

The unchanged [observer](../2026-09-06-mir-loop-bounds-diagnostic-darwin-arm64/build-cost-observer.py)
uses monotonic wall time and wait4 CPU/orchestration-root RSS. Each compiler
builds its own exact source with QBE 1.3, `/usr/bin/cc`, `darwin-arm64-v0`
and the same output basename. Baseline:
`1afd60c2c7257ed34fd2a2aa70cb8b9164433009`.

Two warmups and seven retained observations per role alternate build order.
All 18 builds reproduce their respective compilers. All owned correctness and
bootstrap jobs completed before measurement. Host: Apple M2 Pro, 10 logical
CPUs, 32 GiB RAM, macOS 26.6.2, Apple clang 21.0.0
(`clang-2100.1.1.101`). Warm local caches; no CPU affinity, controlled frequency
or host-wide isolation. Unrelated host activity was not excluded. Reference:
`5dc09070cf7f88a569279f5e63982a6de59d692c`.

| Metric | Baseline median | Candidate median | Ratio |
| --- | ---: | ---: | ---: |
| Wall (s) | 1.504252667 | 1.591123250 | 1.0577499943 |
| CPU (s) | 1.493971 | 1.576793 | 1.0554374884 |
| Root RSS (bytes) | 40091648 | 40239104 | 1.0036779730 |

Wall and CPU miss 1.05; RSS and every retained observation's 2.0 catastrophic
bound pass. Numerical differences from earlier independently measured failed
candidates do not prove a speed ranking. The simplification remains an
unaccepted draft candidate; full current-source recovery, hosted cross-target
process/memory checks, and runtime acceptance remain pending. Further work
must change the implementation substantively, not retry the same source or
round the failure into a pass.
