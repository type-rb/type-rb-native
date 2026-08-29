# Gate 6J Benchmark Harness

This TypeRB-authored controller verifies and measures the self-hosted Float
Array path under the boundary pre-registered in
[issue #74](https://github.com/type-rb/type-rb-native/issues/74).

It accepts the exact Gate 6I baseline checkout, the Gate 6J implementation
checkout, and the registered Gate 6I B4 compiler as the shared B1 seed.
Recovery never runs inside the controller. The harness:

1. verifies both revisions, clean source closures, the fixed Float Array workload,
   and the shared seed before measurement;
2. closes independent baseline and candidate B1-to-B2-to-B3-to-B4 chains and
   requires exact B2/B3/B4 bytes and fixed-point QBE within each chain;
3. requires deterministic Float Array conformance and workload QBE, direct
   binary64 cell ABI evidence, repeated Native application bytes, and exact
   `float-array-ok` behavior from Native and optimized Go applications;
4. rebuilds the Gate 6E representative and Gate 6I scalar Float applications
   and requires their registered bytes and behavior to remain unchanged;
5. records two warmups and eleven alternating observations for fresh baseline
   and candidate compiler `emit-qbe` and complete Native `build` time and peak
   RSS;
6. records two warmups and eleven alternating observations for candidate
   Native and pinned optimized-Go Float Array build time and peak RSS;
7. records three warmups and 31 alternating observations for Native and Go
   Float Array runtime time and peak RSS; and
8. records raw observations, medians, source and artifact hashes, exact
   commands, tool versions, dependencies, sizes, and intermediate cleanup.

The registered Darwin thresholds keep candidate compiler emit/build time and
RSS within 10% of the fresh Gate 6I baseline. Native Float Array build time, build
RSS, runtime, and runtime RSS must remain within 25% of optimized Go. The
stripped Native application must be at least 80% smaller than the separately
size-optimized Go application, and the stripped compiler must not exceed
224,000 bytes.

Build it with the pinned TypeRB compiler:

```text
trb build --compile \
  --config tools/gate6j-benchmark/trbconfig.jsonc \
  --outfile /tmp/gate6j-benchmark
```

Run it with a clean temporary workspace:

```text
gate6j-benchmark \
  CANDIDATE_ROOT BASELINE_ROOT SEED SEED_PROVENANCE BENCHMARK \
  REFERENCE_TRB QBE CC GO WORKSPACE RAW_CSV INVENTORY
```

`BASELINE_ROOT` must be an exact checkout of
`5ff3da39c8c41a30596bbeed3b6fcffc207a43ed`. `CANDIDATE_ROOT` must be an exact
checkout of `914f4f592f344111b7a790aac00aecbf0d411d11`. `SEED` must be the
registered Gate 6I B4 artifact. `REFERENCE_TRB` is the pinned Go implementation
and uses one inherited Go cache policy for every warmup and observation.

The controller is an observer compiled from TypeRB source. It is not a child
of either ordinary Native compiler chain. The pinned Linux arm64 correctness
run remains separate because this Darwin controller uses `/usr/bin/time -l`,
Mach-O inspection, and the Darwin linker policy.
