# Gate 1 QBE Darwin arm64 Results

Gate 1 passes its pre-registered continuation criteria on this provisional,
heap-free corpus. This is evidence for continuing the experiment, not evidence
that QBE is the production backend or that the final self-hosted compiler has
the same performance.

## Revisions and environment

- TypeRB reference compiler: `fc4c511a4ebed28cc83fbca56af0d31fb481010c`
- measured TypeRB Native implementation: `d751d60466a0bf78a1368088689955fa384201bc`
- QBE: release 1.3, commit `c0818978acec60ebb6167fade60fb7012cbf20ca`
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
static output, scalar calls/control flow, and a five-million-iteration checked
Integer kernel. The correctness suite separately covers range failure,
division by zero, Integer power overflow, negative Integer exponent, and an
explicitly unsupported dynamic-output source.

For each successful project the harness recorded:

- 10 complete application builds for the native, ordinary Go, and
  size-optimized Go paths;
- native snapshot, decode/lower, emit, QBE, and link phase times;
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
the TypeRB-authored driver, the process-based snapshot producer in the pinned
reference compiler, QBE 1.3, and `/usr/bin/cc`.

The exact top-level commands were:

```sh
# Run from the pinned TypeRB checkout.
GOCACHE=/tmp/type-rb-go-cache go build \
  -o /tmp/type-rb-reference-trb-fc4c511 ./cmd/trb

# Run from the TypeRB Native worktree.
GOCACHE=/tmp/type-rb-go-cache /Users/fujita-h/trb/type-rb/trb \
  build --compile --outfile /tmp/type-rb-native-driver-d751d60
GOCACHE=/tmp/type-rb-go-cache /Users/fujita-h/trb/type-rb/trb \
  build --compile --config tools/gate1-benchmark/trbconfig.jsonc \
  --outfile /tmp/type-rb-native-benchmark-d751d60

/tmp/type-rb-native-benchmark-d751d60 \
  /Users/fujita-h/trb/worktrees/type-rb-native/gate-one-differential \
  /tmp/type-rb-reference-trb-fc4c511 \
  /tmp/type-rb-native-driver-d751d60 \
  /tmp/qbe-1.3/qbe /usr/bin/cc \
  /tmp/type-rb-native-gate1-benchmark-d751d60 \
  10 50 \
  /Users/fujita-h/trb/worktrees/type-rb-native/gate-one-differential/results/2026-08-28-gate1-qbe-darwin-arm64/raw.csv
```

## Primary results

Times are medians in seconds. Warm build excludes iteration 0. Each percentage
compares native with the stronger applicable Go result in that row.

| Project | Native warm build | Best Go warm build | Build delta | Native runtime | Best Go runtime | Runtime delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| static-output | 0.112686 | 0.176782 | -36.3% | 0.0064065 | 0.0075675 | -15.3% |
| scalar-control-flow | 0.108581 | 0.169988 | -36.1% | 0.0067520 | 0.0074730 | -9.6% |
| integer-kernel | 0.116422 | 0.167608 | -30.5% | 0.0223165 | 0.0192430 | +16.0% |

The kernel regression remains within the registered 25% non-inferiority bound
and below the 2x catastrophic limit. Process launch noise dominates the two
small runtime cases, so they are startup observations rather than throughput
claims.

| Project | Native stripped | Best size-optimized Go | Size delta |
| --- | ---: | ---: | ---: |
| static-output | 50,032 B | 1,587,714 B | -96.85% |
| scalar-control-flow | 50,032 B | 1,587,730 B | -96.85% |
| integer-kernel | 50,032 B | 1,587,730 B | -96.85% |

The size-optimized Go value is the smaller `-s -w` output before a subsequent
`strip -x`; on this toolchain that second operation added a small amount of
Mach-O metadata.

## Build phases and memory

Warm native phase medians are milliseconds:

| Project | Snapshot | Decode/lower | Emit | QBE | Link | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| static-output | 15.489 | 0.189 | 0.039 | 6.958 | 75.293 | 112.686 |
| scalar-control-flow | 16.065 | 1.086 | 0.159 | 7.949 | 73.561 | 108.581 |
| integer-kernel | 16.143 | 0.577 | 0.100 | 7.809 | 76.057 | 116.422 |

The unassigned difference includes process startup, data-only serialization,
file writes, and benchmark observation overhead. The system assembler/linker
is the largest recorded native phase.

Peak RSS is one warm observation, in bytes:

| Project | Native build | Best Go build | Native runtime | Best Go runtime |
| --- | ---: | ---: | ---: | ---: |
| static-output | 35,749,888 | 60,358,656 | 1,376,256 | 4,030,464 |
| scalar-control-flow | 35,569,664 | 59,342,848 | 1,359,872 | 3,932,160 |
| integer-kernel | 35,684,352 | 59,686,912 | 1,376,256 | 4,128,768 |

## Toolchain and dynamic dependencies

Required application-build components measured locally:

| Component | Bytes | Role |
| --- | ---: | --- |
| pinned reference `trb` | 37,071,922 | temporary snapshot producer and Go baseline compiler |
| TypeRB-authored native driver | 5,250,050 | snapshot validation, MIR, QBE emission, and tool orchestration |
| QBE executable | 403,424 | native backend sidecar |
| Go 1.27 root | 283,246,592 | required only by the Go application-build baseline |

The provisional native application-build path totals 42,725,396 bytes
(40.75 MiB) before system tools. The Go path totals 320,318,514 bytes
(305.48 MiB) before system libraries. The benchmark executable is measurement
infrastructure and is not included. The native compiler driver itself was
bootstrapped through Go for Gate 1; this is not a measurement of the final
self-hosted compiler distribution.

Both paths use system-supplied components. Native builds require
`/usr/bin/cc`, the Apple assembler/linker, and the SDK. Generated native
executables dynamically load only `/usr/lib/libSystem.B.dylib` in this corpus.
The Go size baseline loads `libSystem.B.dylib` and `libresolv.9.dylib`.

## Gate evaluation

- Differential correctness: pass for all supported corpus programs, including
  exact stdout, stderr, and process status.
- Unsupported input: pass; dynamic output fails explicitly at the snapshot
  producer.
- Minimum primary improvement: pass. Warm end-to-end build improves by
  30.5% to 36.3%, and executable size improves by 96.85%.
- Other primary outcomes: pass. The worst runtime result is a 16.0% regression,
  within the 25% bound.
- Catastrophic regression: none in the final measurements.
- TinyGo calibration: omitted. TinyGo was not installed, is not a Gate 1
  deliverable, and the QBE result already resolves the continuation decision.

Gate 1 therefore passes. Development stops before Gate 2 for maintainer review.
