# Decision 0024: BenchExec Fresh-process Runtime Controller

## Status

Accepted for the initial formal language-benchmark runtime measurements.

## Context

The capability corpus proves that the selected TypeRB and upstream programs
compile and produce the required output. Ordinary shell timing would not
reliably account for child processes, memory, CPU allocation, timeouts, or
network isolation, and stopping at the first failed candidate would bias the
published set.

Build measurements and program runtime also have different cache, output, and
failure boundaries. Combining them in one first controller would make a build
toolchain failure capable of invalidating otherwise inspectable runtime raw
data.

## Decision

Fresh-process runtime uses BenchExec
[`runexec` `3.35`](https://github.com/sosy-lab/benchexec/releases/tag/3.35),
pinned by official release asset and SHA-256. `runexec` measures the complete
process tree under Linux cgroups. Its default container has no external network
access. The controller exposes `/` read-only and overrides `/home` with an
isolated overlay so BenchExec can create its container home without changing
the host filesystem. The formal path rejects any other BenchExec version,
non-Linux-arm64 host, or requested CPU outside the delegated set.

Each case has exactly seven candidates: identical TypeRB source through Native
and Go, then the pinned C, C++, Go, Rust, and Java context implementations.
Correctness is checked before timing. One-core and four-core lanes are separate.
Each lane performs two warmup rounds and eleven retained rounds, rotating the
candidate that runs first on every round. Swap is disabled and the Linux page
cache is dropped before every measured process. The process-tree memory limit
is 4 GB; wall-time limits are 300 seconds for fannkuch-redux and n-body and 600
seconds for spectral-norm.

Every warmup, retained observation, command log, output payload, diagnostic,
return value or exit signal, termination reason, wall time, CPU time, memory
value, CPU list, and cache record is retained. Failed measurements remain in
the raw table. A candidate receives medians only when all eleven retained
observations pass; the complete schedule still runs before the controller
returns failure.

## Consequences

The result can compare these exact whole-process implementations on one
declared host without turning missing or failed programs into an advantage.
Threaded implementations retain their authored behavior, while one-core
process-tree confinement makes its overhead visible.

The result includes process startup and Java JIT activity and therefore is not
a persistent-service steady-state claim. Compiler time, build peak RSS,
artifact size, runtime/toolchain distribution inventory, formal candidate
preparation, and result publication remain separate layers built on the same
source and correctness pins.
