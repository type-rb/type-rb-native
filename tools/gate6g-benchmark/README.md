# Gate 6G Benchmark Harness

This TypeRB-authored controller verifies and measures self-hosted compiler
symbol lookup under the boundary pre-registered in
[issue #59](https://github.com/type-rb/type-rb-native/issues/59) and specified
by [Decision 0014](../../docs/decisions/0014-indexed-function-lookup.md).

It accepts the exact Gate 6F source checkout, the Gate 6G candidate checkout,
and one already prepared Gate 6F B1 seed. Recovery never runs inside the
controller. The harness:

1. verifies the baseline revision, candidate/baseline source hashes, and B1
   seed hash before measurement;
2. closes separate baseline and candidate B1-to-B2-to-B3-to-B4 chains and
   requires exact bytes and fixed-point QBE within each chain;
3. generates the exact 6,000-function predecessor-call source and requires
   byte-identical baseline/candidate QBE;
4. records two warmups and eleven alternating observations for canonical
   direct QBE emission, complete compiler builds, and scale-source QBE
   emission, then repeats that policy for peak RSS;
5. enforces the registered 5%, 3%, and 25% time improvements, 5%, 5%, and 10%
   RSS bounds, and 208,530-byte stripped compiler ceiling;
6. rebuilds the Gate 6E application with baseline and candidate B4, requiring
   exact repeated bytes, SHA-256, and behavior; and
7. records raw observations, medians, source/artifact hashes, exact process
   commands, tool versions, dependencies, and intermediate cleanup.

Build it with the pinned TypeRB compiler:

```text
trb build --compile \
  --config tools/gate6g-benchmark/trbconfig.jsonc \
  --outfile /tmp/gate6g-benchmark
```

Run it with a clean temporary workspace:

```text
gate6g-benchmark \
  CANDIDATE_ROOT BASELINE_ROOT SEED SEED_PROVENANCE BENCHMARK \
  QBE CC GO WORKSPACE RAW_CSV INVENTORY
```

`BASELINE_ROOT` must be an exact checkout of
`7cb7e85c0b5bff14157dc1a686829c010d095b70`. `SEED` must be the registered
Gate 6F B1 artifact. `SEED_PROVENANCE` is a concise inventory label; the formal
result also retains the complete out-of-chain recovery commands and hashes.

The controller is an observer compiled from TypeRB source. It is not a child
of either ordinary Native compiler chain. The pinned Linux arm64 correctness
run remains separate because this Darwin controller uses `/usr/bin/time -l`,
Mach-O inspection, and the Darwin linker policy.
