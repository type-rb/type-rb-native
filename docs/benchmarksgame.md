# Reproducible Language Benchmark Plan

This plan implements the bounded benchmark work registered in
[issue #103](https://github.com/type-rb/type-rb-native/issues/103). It follows
[Decision 0023](decisions/0023-reproducible-benchmark-layers.md) and keeps the
identical-TypeRB comparison separate from cross-language implementation
context.

## Status

The capability corpus and the first formal runtime and build/distribution
layers are complete. All three performance inputs pass through the pinned Go
reference compiler, ordinary self-hosted Native compiler, and five pinned
context implementations with exact published output. The
[recorded Linux arm64 result](../results/2026-08-31-benchmarksgame-runtime-linux-arm64/README.md)
retains every registered observation and finds that Native is substantially
smaller and lighter than TypeRB Go but 2.44x to 4.68x slower on these numeric
kernels. The independent
[build result](../results/2026-08-31-benchmarksgame-build-linux-arm64/README.md)
finds that Native compiles the same sources 2.29x to 2.58x faster, uses about
51% less compiler RSS, and reduces the controlled raw build payload by 99.64%.

## Pinned upstream boundary

- project: [The Computer Language Benchmarks Game](https://benchmarksgame-team.pages.debian.net/benchmarksgame/);
- site version: `25.03`;
- repository revision:
  [`40296663ed350d5fe4a6ab5e367bab61cb77c219`](https://salsa.debian.org/benchmarksgame-team/benchmarksgame/-/commit/40296663ed350d5fe4a6ab5e367bab61cb77c219);
- source archive path: `public/download/benchmarksgame-sourcecode.zip` at that
  revision;
- source archive SHA-256:
  `aabcf6726cdc14f0f45b99e5daba48584f94bbb48883fd3711a1d040474d1cb4`;
- measurement procedure:
  [How programs are measured](https://benchmarksgame-team.pages.debian.net/benchmarksgame/how-programs-are-measured.html);
- license: [Revised BSD](https://benchmarksgame-team.pages.debian.net/benchmarksgame/license.html).

The repository retains the two upstream license instances that cover the
adapted TypeRB programs in [`benchmarks/benchmarksgame/licenses`](../benchmarks/benchmarksgame/licenses).

## Admitted TypeRB cases

| Case | Correctness input | Performance input | Published performance output |
| --- | ---: | ---: | --- |
| `fannkuch-redux` | `7` | `12` | `3968050`, then `Pfannkuchen(12) = 65` |
| `n-body` | `1000` | `50000000` | `-0.169075164`, then `-0.169059907` |
| `spectral-norm` | `100` | `5500` | `1.274224153` |

The sources and complete correctness/performance expected outputs are under
[`benchmarks/benchmarksgame`](../benchmarks/benchmarksgame). Their admission
does not weaken a specification:

- `fannkuch-redux` uses mutable Integer Arrays, remainder, permutation
  generation, process arguments, and exact Integer output;
- `n-body` uses binary64 Arrays grouped in a record, the published symplectic
  integration order, square root, and exact nine-place output; and
- `spectral-norm` keeps the four published matrix functions, ten power-method
  iterations, square root, and exact nine-place output.

The Float programs render nine decimal places in user source by rounding a
finite value to an Integer-scaled billionth and padding the fractional digits.
The published values are far inside the portable Integer range and are not
halfway cases. This uses only existing portable TypeRB behavior and remains
identical in both backend paths.

## Primary backend-pair procedure

For each case:

1. hash the authored source and expected output;
2. check the source with both compilers;
3. build the same source with the pinned optimized Go path and with the
   canonical self-hosted Native compiler;
4. run the correctness input and require zero status, empty stderr, exact
   published stdout, and byte identity between backends;
5. perform two untimed compiler warmups, then retain eleven alternating clean
   builds for compiler wall time, CPU time, and peak RSS;
6. validate the performance output before timing runtime, perform two runtime
   warmups, and retain eleven alternating observations for wall time, CPU time,
   and peak RSS; and
7. record raw and stripped executable size plus the complete compiler,
   generator, linker, runtime, shared-library, and required distribution
   inventory.

The first run is never reported. Alternation order changes each observation so
one backend is not systematically favored by thermal or host drift. Failures,
timeouts, and memory-limit outcomes remain in raw data. Medians and the full
per-case distribution are reported; no aggregate score is calculated.

[`tools/benchmarksgame-verify.sh`](../tools/benchmarksgame-verify.sh) owns the
fast correctness boundary and is run by ordinary pull-request CI. The formal
measurement controllers extend this boundary without changing its sources or
oracles.

## Cross-language context selection

The initial arm64-compatible context uses these exact paths from the pinned
archive:

| Case | C | C++ | Go | Rust | Java |
| --- | --- | --- | --- | --- | --- |
| `fannkuch-redux` | `fannkuchredux.gcc` | `fannkuchredux.gpp-3.gpp` | `fannkuchredux.go-8.go` | `fannkuchredux.rust-2.rust` | `fannkuchredux.java-3.java` |
| `n-body` | `nbody.gcc` | `nbody.gpp-2.gpp` | `nbody.go-8.go` | `nbody.rust` | `nbody.java-4.java` |
| `spectral-norm` | `spectralnorm.gcc-8.gcc` | `spectralnorm.gpp` | `spectralnorm.go-8.go` | `spectralnorm.rust-3.rust` | `spectralnorm.java-8.java` |

These variants compile on Darwin arm64 and reproduce every small published
oracle with the locally recorded toolchains. They avoid x86-only SIMD
requirements; Linux arm64 remains part of the formal run rather than an
inference from that check. Some upstream implementations create threads, so
the one-core and four-core lanes are published separately. The one-core lane
does not rewrite source to remove threading; BenchExec constrains the complete
process tree and records the resulting overhead.

[`context-sources.tsv`](../benchmarks/benchmarksgame/context-sources.tsv) pins
each archive path and source hash.
[`tools/benchmarksgame-context-verify.sh`](../tools/benchmarksgame-context-verify.sh)
refuses a different archive, extracts only those 15 sources, compiles them,
records the complete commands and tool versions, and requires exact published
output for every small input. This is a correctness and toolchain-capability
check, not a performance result.

The preregistered
[`formal runtime controller`](../tools/benchmarksgame-formal/README.md) pins
BenchExec `runexec` 3.35, runs correctness before timing, rotates all seven
candidates through two warmup and eleven retained rounds, and preserves every
failure and raw process-tree metric. One-core and four-core lanes are separate.
This controller measures complete fresh processes only. Its first
[formal result](../results/2026-08-31-benchmarksgame-runtime-linux-arm64/README.md)
publishes all one-core and four-core raw observations, independently reproduced
medians, and exact artifact identities. Compiler measurements and complete
artifact/distribution inventory use the separate
[formal build controller](../tools/benchmarksgame-build-formal/README.md). It
measures alternating clean outputs through both TypeRB backends, verifies every
measured artifact, process-traces representative builds, and separates
controlled payloads from platform prerequisites and deploy artifacts. Its
first
[formal result](../results/2026-08-31-benchmarksgame-build-linux-arm64/README.md)
publishes all raw observations, independently reproduced medians, artifact
variants, process closure, dynamic dependencies, and distribution totals. See
[Decision 0024](decisions/0024-benchexec-runtime-controller.md) and
[Decision 0027](decisions/0027-formal-build-distribution-controller.md). The
dispatch-only [runtime workflow](../.github/workflows/benchmarksgame-formal.yml)
and [build workflow](../.github/workflows/benchmarksgame-build-formal.yml)
isolate each case on a fresh runner and retain complete result trees even when
an observation fails.

## Native optimization A/B procedure

The cross-language result is a durable reference point, not a convenient
same-host baseline for each compiler optimization. The separate
[`native-runtime-ab` controller](../tools/native-runtime-ab/README.md) compares
one exact Native baseline with one Native candidate on the same fresh Linux
arm64 host. It keeps the authored TypeRB source identical, alternates the two
executables for two warmups and eleven retained observations, and retains the
same status, output, wall-time, CPU-time, peak-memory, cache, and process
evidence used by the broader runtime layer.

The initial contract is registered by
[issue #138](https://github.com/type-rb/type-rb-native/issues/138). It uses the
full `spectral-norm` performance input and bounded `fannkuch-redux` and
`n-body` non-regression controls. It also closes both self-hosted compiler
chains, compares compiler build cost and size, and enforces QBE plus raw and
stripped application-size limits before runtime timing. This optimization A/B
contract does not replace or revise the published cross-language inputs or
results.

The first [formal optimization result](../results/2026-08-31-native-numeric-inline-linux-arm64/README.md)
passes that contract. Its bounded numeric-only reserve reduces the exact
`spectral-norm` wall and CPU medians by 20.61% and 20.62%, keeps both control
programs slightly faster than the frozen Native baseline, closes an exact
self-hosted fixed point, and remains within every registered compiler, QBE,
and application-size limit.

Builds use release optimization without unsafe fast-math substitutions: C and
C++ use `-O3`, Go uses `go build -trimpath`, Rust uses `rustc -C opt-level=3`,
and Java uses `javac` followed by the same recorded JVM for every run. The
selected n-body C++ source additionally needs `-include cstdlib` with current
Clang because it uses `std::size_t` without including that header. This is a
recorded compiler-compatibility flag, not a source rewrite. Exact compiler
versions and complete command lines are result inputs. Raw and stripped
artifacts are distinct; Java application size and required JRE distribution
size are both explicit.

Formal context runs use pinned BenchExec `runexec` 3.35 on an otherwise idle
Linux arm64 host. The harness checks cgroup support, validates all output
before timing, drops the Linux page cache before every measured process, uses
two warmup and eleven retained rounds, prevents network access during
execution, and records every timeout or failure. One-core and four-core results
use the same binaries and inputs.

## Interpretation limits

These cases have insignificant I/O and primarily test tight numeric kernels.
They do not represent application architecture, package ecosystems, latency
under load, persistent services, allocation behavior, or developer
productivity. The primary layer supports backend claims only. The context layer
supports statements about these exact implementations, inputs, host, and
toolchains only.
