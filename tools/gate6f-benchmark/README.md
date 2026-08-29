# Gate 6F Benchmark Harness

This TypeRB-authored controller verifies and measures the multi-file
self-hosted compiler boundary registered in
[issue #55](https://github.com/type-rb/type-rb-native/issues/55) and specified
by [Decision 0013](../../docs/decisions/0013-multi-file-self-hosted-compiler.md).

It accepts an already prepared B1 Native seed. Seed recovery is never run by
the controller and remains outside every ordinary compiler build and measured
observation. The harness:

1. reads the canonical compiler entry, storage, and path modules and validates
   the exact import boundary before deriving one temporary flat comparison
   source;
2. constructs the actual multi-file B1-to-B2-to-B3-to-B4 chain and requires
   exact B2/B3/B4 executable bytes and fixed-point QBE;
3. records two warmups and seven alternating B1 builds of the multi-file and
   flat sources, using the same seed and `compiler` output basename, with a
   separate identically ordered peak-RSS series;
4. enforces the absolute compiler-size cap and the relative flat-size cap;
5. rebuilds the Gate 6E file-root application twice with B4, requiring exact
   observable behavior, repeated bytes, and the registered Darwin SHA-256; and
6. inventories revisions, source and derived-source hashes, artifacts,
   dependencies, process imports, exact command boundaries, retained QBE/CC
   tools, and intermediate cleanup.

Build it with the pinned TypeRB compiler:

```text
trb build --compile \
  --config tools/gate6f-benchmark/trbconfig.jsonc \
  --outfile /tmp/gate6f-benchmark
```

Run it with a clean temporary workspace:

```text
gate6f-benchmark \
  ROOT SEED SEED_PROVENANCE BENCHMARK QBE CC GO \
  WORKSPACE RAW_CSV INVENTORY
```

`SEED_PROVENANCE` is a concise inventory label. The published result must also
retain the exact out-of-chain recovery commands, revisions, source hashes, and
seed hash. The benchmark executable is an observer built from TypeRB source;
it is not a child in the ordinary Native compiler graph.
