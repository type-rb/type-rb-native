# Gate 2 QBE Darwin arm64 Results

Gate 2 passes its registered correctness, reproducibility, size, build-time,
runtime, and memory criteria for heap-free static aggregates. This result
supports moving to runtime viability after maintainer review. It does not select
QBE as the production backend or measure the final self-hosted compiler.

## Revisions and environment

- TypeRB reference compiler and snapshot v3 producer:
  `dacd4a20e5f9b841380ba1d03bccc5e2b24ba470`
- measured TypeRB Native implementation:
  `abcfcf7606d7d6d098ae4728bf583a87554857b8`
- QBE: release 1.3, corresponding to upstream commit
  `c0818978acec60ebb6167fade60fb7012cbf20ca`
- QBE archive SHA-256:
  `d587905d620dc5e1d2bfa7c2cc642b9b837aa89a3188c6e37b53d756cf66e320`
- target profile: `darwin-arm64-v0` / QBE `arm64_apple`
- machine: Apple M2 Pro, 32 GiB RAM
- operating system: macOS 26.6.2 (25G83), arm64
- Go: 1.27.0 darwin/arm64
- C toolchain: Apple clang 21.0.0, target `arm64-apple-darwin25.6.0`

The committed [`raw.csv`](raw.csv) contains 726 measurements and no nonzero
measurement status.

## Method

The TypeRB-authored benchmark executable measured three successful projects:
aggregate values, explicit `Result` control flow, and a five-million-iteration
record-state kernel. The correctness suite additionally covers nested records,
payloadless and payload-bearing variants, exhaustive dispatch, aggregate calls
and returns, `try` success and propagation, aggregate swaps across a loop back
edge, and an explicitly unsupported dynamic record field.

For each measured project the harness recorded:

- 10 complete application builds for the native, ordinary Go, and
  size-optimized Go paths;
- native snapshot, decode/lower, emit, QBE-to-assembly, and link phase times;
- raw and stripped executable sizes;
- one warm peak-RSS observation for build and runtime; and
- 50 runtime observations after three unrecorded warmups.

Iteration 0 used an empty, per-project Go build cache. Later iterations reused
that cache. The native path has no application code cache. The workspace began
absent, but operating-system filesystem and page caches were not flushed. The
native and ordinary Go build order alternated; the size-optimized Go build ran
third. Runtime order alternated between native and ordinary Go, followed by the
size-optimized Go executable.

The ordinary baseline command was `trb build --compile`. The size baseline used
the same command with `GOFLAGS=-ldflags=-s -w`. Native application builds used
the TypeRB-authored driver, the process-based snapshot v3 producer in the pinned
reference compiler, QBE 1.3, and `/usr/bin/cc`.

The exact top-level commands were:

```sh
# Run from the pinned TypeRB checkout.
GOCACHE=/tmp/type-rb-go-cache go build \
  -o /tmp/type-rb-reference-trb-dacd4a2 ./cmd/trb

# Run from the TypeRB Native worktree.
/tmp/type-rb-reference-trb-dacd4a2 build --compile \
  --outfile /tmp/type-rb-native-driver-gate2-alias
/tmp/type-rb-reference-trb-dacd4a2 build --compile \
  --config tools/gate2-benchmark/trbconfig.jsonc \
  --outfile /tmp/type-rb-native-gate2-benchmark-final

/tmp/type-rb-native-gate2-benchmark-final \
  /Users/fujita-h/trb/worktrees/type-rb-native/gate2-source-corpus \
  /tmp/type-rb-reference-trb-dacd4a2 \
  /tmp/type-rb-native-driver-gate2-alias \
  /tmp/qbe-1.3/qbe /usr/bin/cc \
  /tmp/type-rb-native-gate2-benchmark-alias-dacd4a2 \
  10 50 \
  /Users/fujita-h/trb/worktrees/type-rb-native/gate2-source-corpus/results/2026-08-28-gate2-qbe-darwin-arm64/raw.csv
```

## Primary results

Times are medians in seconds. Warm build excludes iteration 0. Each percentage
compares native with the stronger applicable Go result in that row.

| Project | Native warm build | Best Go warm build | Build delta | Native runtime | Best Go runtime | Runtime delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| aggregate-values | 0.118734 | 0.168476 | -29.5% | 0.0065895 | 0.0078535 | -16.1% |
| result-control-flow | 0.136165 | 0.189449 | -28.1% | 0.0076820 | 0.0087625 | -12.3% |
| aggregate-kernel | 0.121674 | 0.164383 | -26.0% | 0.0233210 | 0.0198245 | +17.6% |

The two small runtime cases remain startup observations. The aggregate kernel
constructs, projects, and carries record state through five million loop
iterations. Its regression remains within the registered 25% non-inferiority
bound and below the 2x catastrophic limit.

| Project | Native stripped | Best size-optimized Go | Size delta |
| --- | ---: | ---: | ---: |
| aggregate-values | 50,032 B | 1,587,730 B | -96.85% |
| result-control-flow | 50,032 B | 1,587,730 B | -96.85% |
| aggregate-kernel | 50,032 B | 1,587,730 B | -96.85% |

The size-optimized Go value is the smaller `-s -w` output before a subsequent
`strip -x`; on this toolchain that second operation added a small amount of
Mach-O metadata.

## Build phases and memory

Warm native phase medians are milliseconds:

| Project | Snapshot | Decode/lower | Emit | QBE/assembly | Link | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| aggregate-values | 16.234 | 1.216 | 0.455 | 8.807 | 77.195 | 118.734 |
| result-control-flow | 18.092 | 0.856 | 0.245 | 11.167 | 91.431 | 136.165 |
| aggregate-kernel | 17.991 | 0.669 | 0.168 | 7.896 | 85.078 | 121.674 |

Snapshot time includes the reference frontend and data-only serialization. The
adapter has no separate MIR optimization process; verifier-guided copy elision
is included in emit time. QBE time produces target assembly, while link time
includes system assembly and linking. The unassigned difference includes
process startup, file writes, and benchmark observation overhead. The system
assembler/linker remains the largest recorded native phase.

Peak RSS is one warm observation, in bytes:

| Project | Native build | Best Go build | Native runtime | Best Go runtime |
| --- | ---: | ---: | ---: | ---: |
| aggregate-values | 35,897,344 | 59,752,448 | 1,359,872 | 4,063,232 |
| result-control-flow | 35,880,960 | 60,948,480 | 1,359,872 | 3,981,312 |
| aggregate-kernel | 35,733,504 | 60,768,256 | 1,359,872 | 4,096,000 |

## Toolchain and dynamic dependencies

Required application-build components measured locally:

| Component | Bytes | Role |
| --- | ---: | --- |
| pinned reference `trb` | 37,275,938 | temporary snapshot producer and Go baseline compiler |
| TypeRB-authored native driver | 5,802,242 | snapshot validation, MIR, QBE emission, and tool orchestration |
| QBE executable | 403,424 | native backend sidecar |
| Go 1.27 root | 283,246,592 | required only by the Go application-build baseline |

The provisional native application-build path totals 43,481,604 bytes
(41.47 MiB) before system tools. The Go path totals 320,522,530 bytes
(305.67 MiB) before system libraries. The 3,816,882-byte benchmark executable
is measurement infrastructure and is not included. The native compiler driver
itself was bootstrapped through Go for Gate 2; this is not a measurement of the
final self-hosted compiler distribution.

Native builds require `/usr/bin/cc`, the Apple assembler/linker, and the SDK.
Generated native executables dynamically load only
`/usr/lib/libSystem.B.dylib` in this corpus. The Go size baseline loads
`libSystem.B.dylib` and `libresolv.9.dylib`.

## Optimization finding

A pre-final diagnostic kernel exposed that calling `memcpy` and `memset` for
every fixed-size aggregate operation, followed by unconditional block-parameter
copies, missed the runtime target. The final adapter uses QBE `blit`, explicit
deterministic zero stores, common-incoming-value aliases, and staged copies only
when an edge can overwrite another aggregate argument. The aggregate-swap
source case locks down the parallel-copy behavior.

The primary kernel measures aggregate construction, projection, and loop-carried
state. It does not measure a non-inlined aggregate-returning call on every
iteration. QBE 1.3 does not provide interprocedural inlining, and the disposable
borrowed-parameter/caller-owned-result ABI remains a performance risk to revisit
as function optimization and the stable native ABI develop.

## Gate evaluation

- Strict snapshot, layout, and MIR validation: pass, including malformed
  layouts, nominal mismatches, invalid projections, and dynamic storage.
- Differential correctness: pass for records, nested records, tagged values,
  `Result`, `try`, aggregate calls and returns, and parallel aggregate swaps.
- Reproducibility: pass for snapshot v3, decoded MIR-derived QBE IL, assembly,
  and Mach-O executable artifacts.
- Executable size: pass with a 96.85% reduction.
- Warm end-to-end build time: pass with a 26.0% to 29.5% improvement.
- Runtime: pass; the worst result is a 17.6% regression, within the 25% bound.
- Peak memory and catastrophic regression: pass; native uses less observed RSS,
  and no primary result approaches 2x.

Gate 2 therefore passes. Development stops before Gate 3 for maintainer review.
