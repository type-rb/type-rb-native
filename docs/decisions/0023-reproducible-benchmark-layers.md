# Decision 0023: Reproducible Benchmark Layers

## Status

Accepted for the initial Computer Language Benchmarks Game work.

## Context

One performance comparison cannot answer both whether Native improves the
TypeRB implementation and whether TypeRB programs are competitive with mature
language implementations. Different authored programs, libraries, threading
models, and implementation-specific optimizations would otherwise hide the
backend difference.

The Computer Language Benchmarks Game is useful as a maintained set of small,
validated programs, but the project explicitly describes the programs as
microbenchmarks rather than representative applications. Its current
implementations also mix scalar, threaded, vectorized, and target-specific
techniques. A single aggregate language ranking would therefore overstate the
evidence.

## Decision

Benchmark evidence has two separate layers.

The primary layer compiles byte-identical portable TypeRB sources through the
pinned Go reference implementation and the ordinary self-hosted Native path.
It compares compiler work and generated applications separately. This layer is
authoritative for backend claims.

The context layer compiles exact source variants from a pinned upstream
Benchmarks Game archive on the same Linux arm64 host. It reports C, C++, Go,
Rust, Java, TypeRB-through-Go, and TypeRB-through-Native by case. It is
implementation context, not an intrinsic language ranking. A one-core lane
limits every complete process tree to one selected core; a four-core lane is
separate and makes available parallelism explicit. Missing results, failures,
timeouts, and memory-limit terminations remain visible.

The first admitted specifications are `fannkuch-redux`, `n-body`, and
`spectral-norm`. Each TypeRB program accepts the published input, implements
the published algorithm, and produces the exact published output. Decimal
rendering for the two Float cases is ordinary TypeRB source built from existing
portable numeric and String operations; it is not a Native-only formatting
intrinsic.

Upstream source is pinned to Benchmarks Game revision
`40296663ed350d5fe4a6ab5e367bab61cb77c219`, site version `25.03`. The source
archive SHA-256 is
`aabcf6726cdc14f0f45b99e5daba48584f94bbb48883fd3711a1d040474d1cb4`.
Copied or adapted source retains the upstream Revised BSD terms.

Correctness is mandatory before timing. Formal primary measurements use two
warmups and eleven retained alternating observations. Formal context
measurements use BenchExec on Linux, retain raw per-run results, and record the
host, image, CPU allocation, toolchains, flags, process isolation, cache state,
timeouts, memory limits, source hashes, outputs, and distribution components.
Results remain per case and per metric; no composite score is published.

## Consequences

Native and Go backend differences remain attributable to the backend because
their authored inputs are identical. Cross-language results can still expose
whether TypeRB is in a useful performance range without pretending that unlike
programs prove a universal language ordering.

The benchmark corpus does not add TypeRB syntax or standard-library surface.
Representative Web, Job, allocation, I/O, regular-expression, and persistent
service workloads remain separate work. The selected upstream context variants
and build commands are versioned with the benchmark plan and must be changed
before, not after, collecting a new formal result.
