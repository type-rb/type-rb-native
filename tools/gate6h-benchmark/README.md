# Gate 6H Benchmark Harness

This TypeRB-authored controller verifies and measures module loading and
reachability under the boundary pre-registered in
[issue #64](https://github.com/type-rb/type-rb-native/issues/64).

It accepts the exact Gate 6G source checkout, the Gate 6H candidate checkout,
and the registered Gate 6G B4 compiler as the shared B1 seed. Recovery never
runs inside the controller. The harness:

1. verifies the baseline revision, compiler-closure source hashes, and shared
   seed hash before measurement;
2. closes independent baseline and candidate B1-to-B2-to-B3-to-B4 chains and
   requires exact B2/B3/B4 bytes and fixed-point QBE within each chain;
3. generates exactly 1,025 TypeRB files: `main.trb` plus 1,024 fixed-width
   `m0000.trb` through `m1023.trb` modules in a predecessor import chain;
4. requires identical baseline/candidate scale-project QBE, repeated Native
   executable bytes, and `module-scale-ok` behavior from Native and optimized
   Go builds of that same project;
5. records two warmups and eleven alternating observations for scale-project
   `check`, `emit-qbe`, and complete Native `build` time and peak RSS;
6. alternates the candidate Native build against the pinned current Go-backed
   `trb build --compile` path for the same project and cache policy;
7. repeats the registered Gate 6G canonical compiler-source emit/build series
   to guard against regression; and
8. records raw observations, medians, source/artifact hashes, exact commands,
   tool versions, dependencies, sizes, and intermediate cleanup.

The registered Darwin thresholds require at least 35%, 25%, and 10% time
improvements for scale-project check, emit, and build respectively; scale RSS
must remain within 10% of Gate 6G. Candidate Native build time and RSS must be
within 25% of optimized Go, its stripped application must be at least 80%
smaller, canonical compiler emit/build time and RSS must stay within 5% of the
Gate 6G medians, and the stripped compiler must not exceed 208,530 bytes.

Build it with the pinned TypeRB compiler:

```text
trb build --compile \
  --config tools/gate6h-benchmark/trbconfig.jsonc \
  --outfile /tmp/gate6h-benchmark
```

Run it with a clean temporary workspace:

```text
gate6h-benchmark \
  CANDIDATE_ROOT BASELINE_ROOT SEED SEED_PROVENANCE BENCHMARK \
  REFERENCE_TRB QBE CC GO WORKSPACE RAW_CSV INVENTORY
```

`BASELINE_ROOT` must be an exact checkout of
`0796e39558f6c28995c9b4c03defded4b4bd6123`. `SEED` must be the registered
Gate 6G B4 artifact. `REFERENCE_TRB` is the pinned current Go implementation;
it compiles the exact generated TypeRB project used by Native. The formal run
uses one inherited Go cache policy for both warmups and observations.

The controller is an observer compiled from TypeRB source. It is not a child
of either ordinary Native compiler chain. The pinned Linux arm64 correctness
run remains separate because this Darwin controller uses `/usr/bin/time -l`,
Mach-O inspection, and the Darwin linker policy.
