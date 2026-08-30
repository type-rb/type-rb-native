# Ordinary Runtime Memory Stability Results

The first bounded ordinary-runtime memory stage passes every preregistered
correctness, collector, production-soak, independent-oracle, fixed-point, and
compiler-size criterion on Darwin arm64 and Linux arm64.

The ordinary self-hosted emitter now uses a non-moving tracing collector for
dynamic Strings, Arrays, and managed records. The 300,000,000-iteration Linux
production soak allocates and reclaims 42,300,000,000 managed bytes, finishes
with zero live managed bytes, and records a flat 2,347,008-byte RSS series. The
dedicated ASan/LSan link reports no sanitizer finding, while Valgrind reports no
lost or possibly lost allocation and no memory error.

This is a Stage 1 runtime result, not proof for a persistent Web server or Job
worker. Resource-owning service lifecycles, cancellation, retry, connection
churn, descriptors, threads, and graceful shutdown remain later work under the
staged scope of issue #104.

## Registered scope and identities

- preregistered scope and thresholds:
  [issue #104](https://github.com/type-rb/type-rb-native/issues/104#issuecomment-5466205494)
- exact-root representation amendment, with thresholds unchanged:
  [issue comment](https://github.com/type-rb/type-rb-native/issues/104#issuecomment-5466923757)
- ordinary managed-runtime integration:
  [PR #105](https://github.com/type-rb/type-rb-native/pull/105)
- removal of the retired root-frame path after the first formal size failure:
  [PR #107](https://github.com/type-rb/type-rb-native/pull/107)
- final measured Native revision:
  `efa0b515ba9631c65e04174a495fa7c78a67cf17`
- pinned TypeRB source and semantic oracle:
  `7fcc1d7f8978d5335368c1d4d3be4c79db86d995` (`0.4.1-dev`)
- immutable predecessor seed:
  [`bootstrap-seed-2026-08-30`](https://github.com/type-rb/type-rb-native/releases/tag/bootstrap-seed-2026-08-30)
- QBE 1.3 source archive SHA-256:
  `d587905d620dc5e1d2bfa7c2cc642b9b837aa89a3188c6e37b53d756cf66e320`
- final workflow:
  [Actions run 33298302181](https://github.com/type-rb/type-rb-native/actions/runs/33298302181)
- targets: `darwin-arm64-v0` on `macos-15` and `linux-arm64-v0` on
  `ubuntu-24.04-arm`

The workload source is shared by every mode. The harness changes only the
registered phase and iteration constants for smoke and independent-oracle
runs, and records the resulting source, QBE, executable, and tool identities.

## Correctness and collector result

The reviewed pull-request workflow passes the complete 76-test suite, the
31-test self-hosted frontend suite, the retained source differential and
application corpora, snapshot closure, deterministic failure and cleanup
checks, and the Go-free bootstrap harness. Both production-linked smoke runs
emit the exact expected workload output.

| Target and mode | Iterations | Allocated bytes | Reclaimed bytes | Final live bytes | Peak managed heap | Elapsed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Darwin production smoke | 5,000,000 | 705,000,000 | 705,000,000 | 0 | 1,048,513 | 0.76 s |
| Linux production smoke | 5,000,000 | 705,000,000 | 705,000,000 | 0 | 1,048,513 | 0.72 s |
| Linux ASan/LSan oracle | 50,000 | 7,050,000 | 7,050,000 | 0 | 1,048,513 | 0.07 s |
| Linux Valgrind oracle | 50,000 | 7,050,000 | 7,050,000 | 0 | 1,048,513 | recorded by Memcheck |
| Linux formal production soak | 300,000,000 | 42,300,000,000 | 42,300,000,000 | 0 | 1,048,513 | 43.99 s |

The formal run completes 40,345 collections, of which 40,344 are automatic.
Every mode has positive reclamation and satisfies
`allocated_bytes = reclaimed_bytes + live_bytes`. The final reporting
collection occurs after the authored `main` frame returns. Peak managed heap is
below the registered 4 MiB ceiling with approximately 75% headroom.

The Darwin candidate smoke is also below the 4.25-second 5x calibration limit
derived from the preregistered 0.85-second process-lifetime baseline. This is an
allocator-stress guardrail result, not a general application-performance claim.

## Production RSS trend

The formal Linux run uses 60 phases of 5,000,000 allocations and an
allocation-idle Integer loop after every phase. RSS is sampled every 250 ms;
the first six phases are excluded from trend analysis.

| Metric | Result | Registered limit |
| --- | ---: | ---: |
| Samples | 170 | retain every sample |
| Post-warmup samples | 153 | positive sample set |
| Maximum RSS | 2,347,008 bytes | 67,108,864 bytes |
| First post-warmup temporal-quartile median | 2,347,008 bytes | reported independently |
| Last post-warmup temporal-quartile median | 2,347,008 bytes | at most first + 8 MiB |
| Quartile-median growth | 0 bytes | at most 8 MiB |
| Fitted RSS slope | 0.000000 bytes/minute | at most 1 MiB/minute |

Every retained RSS sample has the same 2,347,008-byte value. The absolute
ceiling, temporal-quartile comparison, and fitted slope therefore pass
independently rather than one metric substituting for another.

## Independent memory oracles

The Linux ASan/LSan path links the dedicated QBE output with Clang and runs with
leak detection and nonzero error exit codes enabled. It exits cleanly with no
invalid-access, double-free, or leak report. As preregistered, this establishes
allocator interception and instrumented C/toolchain behavior; it does not claim
that Clang instruments QBE instructions.

Valgrind 3.22.0 observes 200,001 allocations and 200,000 frees covering
7,050,512 bytes. Its complete summary is:

| Memcheck class | Result |
| --- | ---: |
| Definitely lost | 0 bytes in 0 blocks |
| Indirectly lost | 0 bytes in 0 blocks |
| Possibly lost | 0 bytes in 0 blocks |
| Still reachable | 512 bytes in 1 block |
| Error summary | 0 errors |
| Suppressed | 0 bytes in 0 blocks |

The one reachable allocation is the exact-root stack's initial 64-word backing
buffer. Its capacity follows maximum logical root depth, it does not grow with
cumulative allocation, and it remains globally reachable until process exit.
The result enumerates it explicitly without a suppression; all managed objects
and Array backing allocations are reclaimed.

## Exact self-hosted fixed points

The immutable predecessor seed first builds two separately identified,
setup-only current-source transitions. The second transition then enters the
measured ordinary chain:

```text
current-runtime transition -> B2 -> B3 -> B4
```

B2, B3, and B4 executable bytes are exact within each target. Both targets
also emit the exact same 853,095-byte fixed-point QBE program with SHA-256
`06157dcfc29157657df8749e28ad0f58b4459663d8f9319bcdfa0f94154625cf`.

| Target | Exact B2/B3/B4 bytes | SHA-256 | B2-to-B3 elapsed/RSS median | B3-to-B4 elapsed/RSS median |
| --- | ---: | --- | ---: | ---: |
| Darwin arm64 | 283,048 | `cf10c78817dee3889faba263155e6157a403167a1e67034bc780b21c663a1730` | 1.40 s / 36,110,336 B | 1.40 s / 36,093,952 B |
| Linux arm64 | 261,664 | `be0a11356ecbffc214d6e4983dc44b4a823a35c404dbb4aeac20e9c79665c57e` | 1.04 s / 15,007,744 B | 1.02 s / 15,007,744 B |

The largest adjacent elapsed spread is 1.96%, and the largest adjacent RSS
spread is 0.05%, both below the registered 25% bound and far below the 2x
catastrophic threshold.

The size workflow independently strips the candidate copies before enforcing
the aggregate bound:

| Target | Stripped bytes | Per-target limit | Headroom |
| --- | ---: | ---: | ---: |
| Darwin arm64 | 283,088 | 310,000 | 26,912 |
| Linux arm64 | 261,664 | 310,000 | 48,336 |
| Combined | 544,752 | 620,000 | 75,248 |

The ordinary Linux process inventory contains the Native B4 compiler, QBE,
the explicit system CC, assembler lookup and execution, `collect2`, and the
linker. It contains no Go, reference `trb`, recovery compiler, or
shell-mediated compiler child. The separately recorded setup transitions are
also Go-free but are excluded from candidate timing and size claims.

## Threshold integrity

The first merged formal attempt,
[Actions run 33297050527](https://github.com/type-rb/type-rb-native/actions/runs/33297050527),
stopped before the Linux memory oracles because its 328,384-byte compiler
exceeded the frozen 310,000-byte limit. Its fixed-point QBE was correct; the
hosted arm64 linker's 64 KiB segment alignment exposed an obsolete root-frame
path just across an ELF layout boundary.

PR #107 removed the unreferenced pre-exact-root path and required its symbols
to be absent from emitted QBE. No workload, iteration, sample, memory, runtime,
fixed-point, or compiler-size threshold was relaxed. The complete workflow was
then rerun from the new merged revision, producing the passing result recorded
here.

## Scope boundary

This result establishes bounded managed allocation for the current ordinary
self-hosted String, Array, and managed-record subset. It does not establish a
production garbage collector or complete leak freedom for future runtime
surface.

The following remain separate evidence work:

- a persistent Web lifecycle with success, error, cancellation, timeout,
  connection churn, descriptors, threads, and graceful shutdown;
- a persistent Job lifecycle with success, retry, failure, cancellation, queue
  state, and graceful shutdown;
- closure-cycle shapes once the ordinary self-hosted source subset can express
  them;
- concurrent mutation, finalizers, weak references, and non-memory resource
  ownership; and
- broader application and cross-language benchmark suites.

## Raw evidence

- [`darwin-arm64`](darwin-arm64) contains bootstrap identities and timings,
  executable inspection, transition provenance, production-smoke source,
  output, collector statistics, and workflow context.
- [`linux-arm64`](linux-arm64) contains the same material plus the complete
  process trace, ELF segments, ASan/LSan evidence, Valgrind report, formal
  workload output, 170 raw RSS samples, and trend analysis.
- [`combined-size.txt`](combined-size.txt) records the independently stripped
  cross-target aggregate.
- [`EVIDENCE_SHA256SUMS`](EVIDENCE_SHA256SUMS) covers every retained raw
  evidence file.

Compiler and application binaries are intentionally not committed. Their exact
sizes and SHA-256 identities are retained, while the predecessor compilers
remain available from the immutable release.
