# Gate 6I Benchmark Harness

This TypeRB-authored controller verifies and measures the self-hosted Float
scalar path under the boundary pre-registered in
[issue #69](https://github.com/type-rb/type-rb-native/issues/69).

It accepts the exact Gate 6H baseline checkout, the Gate 6I implementation
checkout, and the registered Gate 6H B4 compiler as the shared B1 seed.
Recovery never runs inside the controller. The harness:

1. verifies both revisions, clean source closures, the fixed Float workload,
   and the shared seed before measurement;
2. closes independent baseline and candidate B1-to-B2-to-B3-to-B4 chains and
   requires exact B2/B3/B4 bytes and fixed-point QBE within each chain;
3. requires deterministic Float conformance and workload QBE, the binary64
   QBE instruction families, repeated Native application bytes, and exact
   `float-kernel-ok` behavior from Native and optimized Go applications;
4. rebuilds the Gate 6E representative application and requires its registered
   bytes and behavior to remain unchanged;
5. records two warmups and eleven alternating observations for fresh baseline
   and candidate compiler `emit-qbe` and complete Native `build` time and peak
   RSS;
6. records two warmups and eleven alternating observations for candidate
   Native and pinned optimized-Go Float build time and peak RSS;
7. records three warmups and 31 alternating observations for Native and Go
   Float runtime time and peak RSS; and
8. records raw observations, medians, source and artifact hashes, exact
   commands, tool versions, dependencies, sizes, and intermediate cleanup.

The registered Darwin thresholds keep candidate compiler emit/build time and
RSS within 10% of the fresh Gate 6H baseline. Native Float build time, build
RSS, runtime, and runtime RSS must remain within 25% of optimized Go. The
stripped Native application must be at least 80% smaller than the separately
size-optimized Go application, and the stripped compiler must not exceed
220,000 bytes.

Build it with the pinned TypeRB compiler:

```text
trb build --compile \
  --config tools/gate6i-benchmark/trbconfig.jsonc \
  --outfile /tmp/gate6i-benchmark
```

Run it with a clean temporary workspace:

```text
gate6i-benchmark \
  CANDIDATE_ROOT BASELINE_ROOT SEED SEED_PROVENANCE BENCHMARK \
  REFERENCE_TRB QBE CC GO WORKSPACE RAW_CSV INVENTORY
```

`BASELINE_ROOT` must be an exact checkout of
`1311dfccee379dcf2dd3a70a525bc188d195981d`. `CANDIDATE_ROOT` must be an exact
checkout of `cd2335e6472b4daca8d631b17b889a094959c2f2`. `SEED` must be the
registered Gate 6H B4 artifact. `REFERENCE_TRB` is the pinned Go implementation
and uses one inherited Go cache policy for every warmup and observation.

The controller is an observer compiled from TypeRB source. It is not a child
of either ordinary Native compiler chain. The pinned Linux arm64 correctness
run remains separate because this Darwin controller uses `/usr/bin/time -l`,
Mach-O inspection, and the Darwin linker policy.
