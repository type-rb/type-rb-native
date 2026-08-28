# Gate 3 QBE Darwin arm64 Results

Gate 3 passes its registered correctness, reproducibility, managed-runtime,
size, build-time, runtime, and memory criteria. The result establishes a viable
exact-root tracing runtime for the current String, Array, closure, and managed
aggregate subset. It does not select QBE as the production backend or measure
the final self-hosted compiler.

## Revisions and environment

- TypeRB reference compiler and snapshot v4 producer:
  `57b4ff018cfbc0539c9b4cbbe4c0676afa429857`
- measured TypeRB Native implementation:
  `ec06cd245c48d34b8d9c74f62db24a3f529219d4`
- QBE: release 1.3, corresponding to upstream commit
  `c0818978acec60ebb6167fade60fb7012cbf20ca`
- measured QBE executable SHA-256:
  `03f50f24156449e0df41ef65444add1670d017be822edf4aa99bc8566952592b`
- target profile: `darwin-arm64-v0` / QBE `arm64_apple`
- machine: Apple M2 Pro, 32 GiB RAM
- operating system: macOS 26.6.2 (25G83), arm64
- Go: 1.27.0 darwin/arm64
- C toolchain: Apple clang 21.0.0, target `arm64-apple-darwin25.6.0`

The committed [`raw.csv`](raw.csv) contains 992 measurements and no nonzero
measurement status.

## Method

The TypeRB-authored benchmark executable measured the four registered source
projects:

- `utf8-strings`: literal construction, concatenation, code-point length,
  negative indexing, equality, and 200,000 traversal iterations;
- `array-values`: 500,000 Integer pushes and reduction plus scalar and managed
  element mutation, growth, aliases, and nested calls;
- `closure-values`: five million captured-Integer closure applications plus
  managed captures, nested closures, records, and tagged values; and
- `cycle-stress`: 20,000 unreachable Array/closure/environment cycles.

For each project the harness recorded:

- 10 complete application builds for the native, ordinary Go, and
  size-optimized Go paths;
- native snapshot, decode/lower, emit, QBE-to-assembly, and link phase times;
- raw and stripped executable sizes;
- one warm peak-RSS observation for build and runtime;
- one separately instrumented native run with six GC statistics; and
- 50 runtime observations after three unrecorded warmups.

Iteration 0 used an empty, per-project Go build cache. Later iterations reused
that cache. The native path has no application code cache. The workspace began
absent, but operating-system filesystem and page caches were not flushed. The
native and ordinary Go build order alternated; the size-optimized Go build ran
third. Runtime order alternated between native and ordinary Go, followed by the
size-optimized Go executable.

The ordinary baseline command was `trb build --compile`. The size baseline used
the same command with `GOFLAGS=-ldflags=-s -w`. Native application builds used
the TypeRB-authored driver, the process-based snapshot v4 producer in the pinned
reference compiler, QBE 1.3, and `/usr/bin/cc`.

The exact top-level commands were:

```sh
# Run from the pinned TypeRB checkout.
GOCACHE=/tmp/type-rb-go-cache go build \
  -o /tmp/type-rb-gate3-reference-57b4ff0 ./cmd/trb

# Run from the TypeRB Native worktree at ec06cd2.
/tmp/type-rb-gate3-reference-57b4ff0 build --compile \
  --config trbconfig.jsonc \
  --outfile /tmp/type-rb-native-driver-gate3-ec06cd2
/tmp/type-rb-gate3-reference-57b4ff0 build --compile \
  --config tools/gate3-benchmark/trbconfig.jsonc \
  --outfile /tmp/type-rb-native-gate3-benchmark-final-ec06cd2

/tmp/type-rb-native-gate3-benchmark-final-ec06cd2 \
  /Users/fujita-h/trb/worktrees/type-rb-native/gate3-results \
  /tmp/type-rb-gate3-reference-57b4ff0 \
  /tmp/type-rb-native-driver-gate3-ec06cd2 \
  /tmp/qbe-1.3/qbe /usr/bin/cc \
  /tmp/type-rb-native-gate3-benchmark-ec06cd2 \
  10 50 \
  /Users/fujita-h/trb/worktrees/type-rb-native/gate3-results/results/2026-08-28-gate3-qbe-darwin-arm64/raw.csv
```

## Primary results

Times are medians in seconds. Warm build excludes iteration 0. Each percentage
compares native with the faster applicable Go result in that row.

| Project | Native warm build | Best Go warm build | Build delta | Native runtime | Best Go runtime | Runtime delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| utf8-strings | 0.132436 | 0.168318 | -21.3% | 0.0186835 | 0.0154340 | +21.1% |
| array-values | 0.145817 | 0.173628 | -16.0% | 0.0131550 | 0.0142360 | -7.6% |
| closure-values | 0.152051 | 0.174806 | -13.0% | 0.0164365 | 0.0157550 | +4.3% |
| cycle-stress | 0.134181 | 0.173944 | -22.9% | 0.0095580 | 0.0087435 | +9.3% |

All warm builds are faster than both Go paths. Every steady-state runtime is
within the registered 25% non-inferiority bound; UTF-8 traversal is the worst
result at +21.1%.

| Project | Native stripped | Best size-optimized Go | Size delta |
| --- | ---: | ---: | ---: |
| utf8-strings | 50,400 B | 1,587,730 B | -96.83% |
| array-values | 50,400 B | 1,587,730 B | -96.83% |
| closure-values | 50,416 B | 1,587,730 B | -96.82% |
| cycle-stress | 50,400 B | 1,587,794 B | -96.83% |

The size-optimized Go value is the smaller `-s -w` output before a subsequent
`strip -x`; on this toolchain that second operation added a small amount of
Mach-O metadata. The native reduction is well beyond the registered 30%
improvement requirement.

## Runtime distribution

Times are seconds across the 50 recorded observations. P95 uses nearest rank.
The complete ordered observations remain in `raw.csv`.

| Project | Candidate | Minimum | Median | P95 | Maximum |
| --- | --- | ---: | ---: | ---: | ---: |
| utf8-strings | native | 0.0141820 | 0.0186835 | 0.0243910 | 0.1101250 |
| utf8-strings | Go | 0.0106890 | 0.0154340 | 0.0213570 | 0.0359890 |
| utf8-strings | Go size | 0.0116100 | 0.0158595 | 0.0211690 | 0.0240400 |
| array-values | native | 0.0082870 | 0.0131550 | 0.0145910 | 0.0150950 |
| array-values | Go | 0.0094770 | 0.0142360 | 0.0157580 | 0.0162610 |
| array-values | Go size | 0.0096240 | 0.0144130 | 0.0153900 | 0.0159150 |
| closure-values | native | 0.0118530 | 0.0164365 | 0.0203840 | 0.0216260 |
| closure-values | Go | 0.0107670 | 0.0157830 | 0.0181920 | 0.0216220 |
| closure-values | Go size | 0.0109150 | 0.0157550 | 0.0188240 | 0.0217250 |
| cycle-stress | native | 0.0073000 | 0.0095580 | 0.0128230 | 0.0133540 |
| cycle-stress | Go | 0.0069730 | 0.0087435 | 0.0131140 | 0.0133290 |
| cycle-stress | Go size | 0.0068360 | 0.0102860 | 0.0127350 | 0.0158910 |

One native UTF-8 observation was a 110 ms outlier. Its 24.4 ms P95 remains
15.2% above the better Go P95 and within the registered bound; the outlier is
retained rather than filtered.

## Build phases and memory

Warm native phase medians are milliseconds:

| Project | Snapshot | Decode/lower | Emit | QBE/assembly | Link | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| utf8-strings | 16.381 | 1.560 | 1.664 | 13.262 | 86.657 | 132.436 |
| array-values | 19.997 | 1.805 | 1.914 | 13.431 | 92.248 | 145.817 |
| closure-values | 17.441 | 2.866 | 3.554 | 16.425 | 94.964 | 152.051 |
| cycle-stress | 16.970 | 0.583 | 0.207 | 10.958 | 83.787 | 134.181 |

Snapshot time includes the reference frontend and data-only serialization. QBE
time produces target assembly, while link time includes system assembly and
linking. The unassigned difference includes process startup, file writes, and
benchmark observation overhead. The system assembler/linker remains the
largest recorded native phase.

Peak RSS is one warm observation, in bytes. The Go column is the lower of the
ordinary and size-optimized observations.

| Project | Native build | Best Go build | Native runtime | Best Go runtime | Runtime delta |
| --- | ---: | ---: | ---: | ---: | ---: |
| utf8-strings | 35,831,808 | 60,932,096 | 2,768,896 | 4,079,616 | -32.1% |
| array-values | 35,815,424 | 60,653,568 | 7,634,944 | 16,826,368 | -54.6% |
| closure-values | 35,815,424 | 61,227,008 | 1,392,640 | 4,210,688 | -66.9% |
| cycle-stress | 35,962,880 | 61,358,080 | 2,637,824 | 5,816,320 | -54.6% |

## Collector evidence

Each row comes from a separately built instrumented executable. Total
collections include one final reporting collection after `main` returns;
automatic collections count only allocation-paced collections. Time covers all
collections in that run.

| Project | Automatic / total | GC time | Allocated | Reclaimed | Final live |
| --- | ---: | ---: | ---: | ---: | ---: |
| utf8-strings | 9 / 10 | 4.101 ms | 10,000,099 B | 10,000,099 B | 0 B |
| array-values | 3 / 4 | 0.006 ms | 4,194,480 B | 4,194,480 B | 0 B |
| closure-values | 0 / 1 | 0.003 ms | 572 B | 572 B | 0 B |
| cycle-stress | 3 / 4 | 1.117 ms | 4,160,000 B | 4,160,000 B | 0 B |

The source cycle workload triggers three automatic collections, exceeding the
required two, and reclaims all 4,160,000 allocated bytes by the final reporting
collection. Its zero-byte final live set is within the warm-live-set allowance
of 10% plus 64 KiB. For every workload, `allocated = reclaimed + final live`.
Array backing storage and growth are included in these byte totals and in GC
pacing.

## Toolchain and dynamic dependencies

Required application-build components measured locally:

| Component | Bytes | Role |
| --- | ---: | --- |
| pinned reference `trb` | 37,413,506 | temporary snapshot producer and Go baseline compiler |
| TypeRB-authored native driver | 6,738,690 | snapshot validation, MIR, QBE emission, runtime emission, and tool orchestration |
| QBE executable | 403,424 | native backend sidecar |
| Go 1.27 root | 283,246,592 | required only by the Go application-build baseline |

The provisional native application-build path totals 44,555,620 bytes
(42.49 MiB) before system tools. The Go path totals 320,660,098 bytes
(305.81 MiB) before system libraries. The 3,816,930-byte benchmark executable
is measurement infrastructure and is not included. The native compiler driver
itself was bootstrapped through Go for Gate 3; this is not a measurement of the
final self-hosted compiler distribution.

Native builds require `/usr/bin/cc`, the Apple assembler/linker, and the SDK.
Generated native executables dynamically load only
`/usr/lib/libSystem.B.dylib` in this corpus. The Go size baseline loads
`libSystem.B.dylib` and `libresolv.9.dylib`.

## Optimization findings

Initial diagnostic runs missed the runtime bound on UTF-8 Strings and closures.
The final QBE adapter:

- reuses unchanged loop/block SSA values and exact-root slots instead of
  unconditional transfer stores and loads;
- devirtualizes only statically known, shape-checked identity and one-operation
  scalar closures, including the registered forwarding wrapper; and
- represents String literals and literal-only concatenations as immutable
  static objects, matching the optimization opportunity available to Go.

Dynamic concatenation and general indirect calls retain their runtime paths.
The closure workload still creates and exercises managed nested closures outside
the throughput loop, and the UTF-8 loop still performs code-point indexing and
String equality. These optimizations reduced the diagnostic worst cases without
changing TypeRB semantics or weakening the registered workloads.

Array growth through aliases and mutable parameters has a broader cross-backend
semantic discrepancy tracked in
[type-rb/type-rb#596](https://github.com/type-rb/type-rb/issues/596). Gate 3
covers growth, alias element mutation, and nested mutation independently and
does not assume an unsettled answer.

## Gate evaluation

- Strict snapshot, layout, and MIR validation: pass, including malformed
  managed types, capture mismatches, unsupported operations, and bounds.
- Differential correctness: pass for all four registered source workloads and
  both distinct bounds-failure cases.
- Reproducibility: pass for snapshot v4, decoded MIR structure, QBE IL,
  assembly, and Mach-O executables.
- Automatic cycle collection: pass with three automatic collections, complete
  reclamation, and a zero-byte final live set.
- Executable size: pass with a 96.82% to 96.83% reduction.
- Warm end-to-end build time: pass with a 13.0% to 22.9% improvement.
- Runtime: pass; the worst median result is a 21.1% regression, within 25%.
- Peak runtime RSS: pass with a 32.1% to 66.9% improvement.
- Catastrophic regression: pass; no primary median or peak-RSS result approaches
  2x.

Gate 3 therefore passes. Development stops before Gate 4 for maintainer review.
