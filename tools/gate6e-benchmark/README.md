# Gate 6E Benchmark Harness

This TypeRB-authored controller verifies and measures the file-root
multi-module boundary registered in
[issue #51](https://github.com/type-rb/type-rb-native/issues/51) and specified
by [Decision 0012](../../docs/decisions/0012-file-root-module-closure.md).

It accepts an already prepared B1 Native seed. Recovery is never run by the
controller and remains outside every ordinary compiler or application build.
The harness:

1. copies the checked-in five-module project to a config-free workspace and
   verifies Native, optimized Go, and flattened Native behavior;
2. constructs the actual B1-to-B2-to-B3-to-B4 compiler chain and requires
   exact B2/B3/B4 bytes and fixed-point QBE;
3. records two indexed warmups and seven alternating Native/Go application
   builds, with a separate seven-observation peak-RSS series;
4. records two runtime warmups and 50 alternating runtime observations, plus
   seven peak-RSS observations after two RSS warmups;
5. records two warmups and seven B1-to-B2 compiler build and RSS observations;
6. enforces the registered application and compiler size limits; and
7. inventories revisions, source-graph hashes, tools, artifacts, dynamic
   dependencies, Go metadata, process imports, and intermediate cleanup.

Build it with the pinned TypeRB compiler:

```text
trb build --compile \
  --config tools/gate6e-benchmark/trbconfig.jsonc \
  --outfile /tmp/gate6e-benchmark
```

Run it with a clean temporary workspace:

```text
gate6e-benchmark \
  ROOT SEED SEED_PROVENANCE BENCHMARK REFERENCE_TRB QBE CC GO \
  WORKSPACE RAW_CSV INVENTORY
```

`SEED_PROVENANCE` is a concise label in the inventory. The result must also
retain the exact recovery commands, revisions, and seed hashes separately.
The benchmark executable is an out-of-chain observer built from TypeRB source;
it is not a child in the ordinary Native compiler graph.
