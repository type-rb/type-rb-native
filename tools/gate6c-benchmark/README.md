# Gate 6C Benchmark Harness

This TypeRB-authored harness measures the Native-to-Native bootstrap closure
defined by [Decision 0010](../../docs/decisions/0010-native-bootstrap-closure.md).
It accepts an already prepared B1 Native compiler and never creates a recovery
compiler itself.

The harness first constructs the actual B1-to-B2-to-B3-to-B4 chain, feeding
each produced compiler into the next ordinary `build`. It requires exact B2,
B3, and B4 bytes, fixed-point QBE, source checks, and complete intermediate
cleanup before recording two warmups and the requested measured observations.
It also records a separate seed-provenance label, executable hashes and sizes,
peak RSS, tool versions, process imports, dynamic dependencies, signatures,
load commands, and the external QBE/CC boundary.

Raw B2/B3/B4 artifacts all retain the required `compiler` basename. For the
registered stripped-code comparison only, the harness writes `b1.stripped`
through `b4.stripped`; their equal-length basenames match the Gate 6B stripping
policy and prevent ad-hoc signature identifier length from masquerading as
compiler-code growth.

Build it with the pinned TypeRB compiler used by the experiment:

```text
trb build --compile \
  --config tools/gate6c-benchmark/trbconfig.jsonc \
  --outfile /tmp/gate6c-benchmark
```

Run it as:

```text
gate6c-benchmark \
  ROOT SEED SEED_PROVENANCE BENCHMARK QBE CC GO \
  WORKSPACE REPETITIONS RAW_CSV INVENTORY
```

`SEED_PROVENANCE` is a single recorded label. Result documentation must still
state the exact recovery or previous-release command, revisions, and seed hash.
The benchmark executable is a measurement controller; it is not a child in any
ordinary compiler-build semantic graph.
