# Short-circuit Boolean expressions — local checkpoint

Status: **implemented, not accepted**. Issue [#308](https://github.com/type-rb/type-rb-native/issues/308)
adds `||` and `&&` together. This candidate also contains the still-unaccepted
Array-loop changes in draft PR #307. The complete candidate misses the frozen
build-cost contract; this report neither isolates the logical feature's cost
nor accepts the earlier optimization.

## Correctness

- All 145 compiler tests pass, including logical precedence, Boolean-only
  plans, skipped-operand checking and forged-plan rejection.
- All 81 conformance cases pass at each of three ordinary file-root generations
  (243 observations). This includes six new positive/negative logical cases.
  Repeated and adjacent application QBE agree; invalid input launches no
  backend tool and leaves no output; runtime failures retain exact diagnostics.
- The published immutable Darwin seed regenerates the core and CLI through
  `tools/build-native.sh`, including both fixed-point comparisons. CLI exit
  guards, REPL plan validation and history-publication guards now use `||`.
  Core source remains accepted by that released seed. The CLI/REPL, scalar
  output and diagnostic integration suites pass.
- Current-source full root recovery, Linux targets, process-trace and memory
  authorities remain pending. Local fixed points are not process-graph proof.
  No application performance cohort or Pages update follows from this work.

The pinned reference `5dc09070cf7f88a569279f5e63982a6de59d692c`
misparses a parenthesized left operand in the managed-RHS fixture, discarding
the logical suffix. Its generated Go executable times out after 180 seconds;
that is a recorded reference failure, not a Native conformance failure or a
reason to rewrite the fixture. [Reference PR #649](https://github.com/type-rb/type-rb/pull/649)
fixes the parser with Go, Ruby, TypeScript and REPL regressions; it merged as
`8220f9c121c836d4c0e01aecbf8e8aeb4dab8ef9` after full local and hosted tests.

The supplemental six-case differential result uses the PR head
`93b6471e9501f42820bd36e787a20723c15b2b2d`, based on
`7a31f3e454781cbf350903e05d88848aae5cb37a`, not the unchanged compatibility
pin. Both implementations match valid output and reject invalid inputs. Array
bounds panic prefixes differ (`index` versus `Array index`); exact Native
stderr and the reference's own expected failure are checked separately.
The compatibility pin is unchanged.

## Build and artifact diagnostic

The existing `build-cost-observer.py` in
`../2026-09-06-mir-loop-bounds-diagnostic-darwin-arm64/` compares each compiler
building its own source closure. Baseline remains
`1afd60c2c7257ed34fd2a2aa70cb8b9164433009`. The candidate is the source recorded
in `source-sha256.txt`, applied over `ed638c9d47099c9e7ad28a18afe737fb1b01d287`.
All 18 builds reproduce their own compiler bytes. There are two warmups and
seven retained observations per role, with alternating order. Raw CSV rows
retain every observation; line endings are normalized to LF.

| Median | Baseline | Candidate | Ratio |
| --- | ---: | ---: | ---: |
| Wall seconds | 1.497339208 | 1.591967167 | 1.0631974094 |
| CPU seconds | 1.482031 | 1.571398 | 1.0603003581 |
| Orchestration-root RSS bytes | 40140800 | 40255488 | 1.0028571429 |

Wall and CPU exceed the unchanged 1.05 limit. RSS and all retained 2.0
catastrophic checks pass. Do not rank this candidate against other dates'
ratios or retry its unchanged source to rescue the failure. A source-distinct
cost reduction is needed before another hosted acceptance attempt.

The fixed compiler is 349256 bytes, with 249436 bytes of Mach-O text. QBE is
1117088 bytes, below the general 1120000 transition ceiling. These absolute
measurements alone do not establish all applicable size/relative authorities.
Compiler SHA256 is
`c8e2e1e93977218d46d9df3d78f3dabe777a157709c44c12733dd949820b35a0`;
QBE SHA256 is
`977793a7087db9e704b904bb05c9909d8cfccf287dbad1625e780ad49d60f313`.
The CLI fixed-point SHA256 is
`6aab00746030e5d70d1f428adf25bc3be5c6b81edf0626ee240549d6dac47517`.

Host: Apple M2 Pro, 10 logical CPUs, 32 GiB RAM, macOS 26.6.2, Darwin arm64.
QBE 1.3 and Apple clang 21.0.0 (`clang-2100.1.1.101`), target
`darwin-arm64-v0`. Monotonic wall time and wait4 CPU/RSS use the existing
observer; RSS is not summed process-tree memory. Warm local caches; no CPU
pinning, frequency control or exclusion of unrelated host activity. Owned
build/test jobs finished before this comparative measurement.

## Rejected setup attempts and scope

Earlier phi/direct-precedence prototypes produced compiler QBE above the
general ceiling (1124250 and 1123959 bytes). The selected form reuses the
operator catalog and an existing Integer-to-String helper, and lowers the
conditional result through a private Boolean slot. A first full test run
reported one stale parser-precedence expectation; the corrected suite passes.

An intermediate implementation used an Integer method absent from the
released seed; fresh bootstrap rejected it before publication. Reusing the
existing helper fixes that source-compatibility failure without changing the
seed or invoking Go.

The published seed SHA256 is
`ef438d13598c534766334b408a39715c56ff1b69db528910ebf7d90ec7720b65`.
It first produces setup compilers of 391416 and 378248 bytes. A helper that
expects an already-converged input correctly rejects equality between these
setup generations. The maintained bootstrap completes the remaining
generations and converges; a separate ordinary chain starting from the latter
setup compiler then produces the identical 349256-byte compiler three times.
Do not relabel setup compilers as the final ordinary fixed point.

Logical control flow currently disables the flat scalar/Array projection for
the affected expression; see [ownership and self-adoption](../../docs/native-logical-expressions.md).
This preserves conditional effects and traps, not full function-CFG MIR
coverage. Core guard cleanup needs an explicitly verified previous-Native
setup transition. No cost ceiling, language rule or recovery obligation changes.
