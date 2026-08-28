# Gate 6B Benchmark Harness

This TypeRB-authored harness records the Gate 6B Native-owned single-file build
measurements registered in
[issue #39](https://github.com/type-rb/type-rb-native/issues/39). It is a
measurement and external-recipe orchestrator, not part of the ordinary Native
compiler process. The harness is deliberately specific to the registered
Darwin arm64 observation.

The harness:

1. builds B0 through B3 and rejects a compiler-QBE fixed-point mismatch;
2. rejects a normalized B1/B2 compiler-executable mismatch;
3. preflights B1 and B2 Native-owned builds and the matching external
   file-emission/QBE/CC recipes;
4. requires byte-identical same-basename application outputs and checks that
   every built compiler executes the fixed-point source correctly;
5. records two indexed warmups and the requested alternating elapsed-time
   observations for Native B1/B2 and external B1/B2 builds;
6. records two indexed warmups and up to three alternating peak-RSS
   observations through `/usr/bin/time -l`;
7. strips B1/B2 and rejects either compiler above the registered 172,251-byte
   ceiling derived from the 149,784-byte Gate 6A baseline; and
8. writes an exact process inventory covering explicit child paths, undefined
   symbols, dynamic libraries, absent Go metadata, output identity, Mach-O
   metadata, and intermediate cleanup.

The external recipe is a subcommand of this same TypeRB harness. It starts a
self-emitted compiler with `emit-qbe SOURCE`, writes the returned IL, invokes
QBE, and invokes CC. It deliberately retains its `.ssa` and `.s` files; Native
`build` is measured with its stronger required cleanup. Neither elapsed-time
path includes correctness probes, hashing, or size inspection.

Build the repository driver and this harness with the pinned reference
compiler:

```sh
trb build --compile --outfile /tmp/type-rb-native-gate6b-driver
trb build --compile \
  --config tools/gate6b-benchmark/trbconfig.jsonc \
  --outfile /tmp/type-rb-native-gate6b-benchmark
```

Then run seven recorded observations. Pass the harness executable itself as
`BENCHMARK` so the parent can start its external-recipe subcommand. Keep the
workspace and outputs outside a committed result directory until the run
passes and is reviewed.

```sh
/tmp/type-rb-native-gate6b-benchmark \
  "$PWD" \
  /path/to/pinned/trb \
  /tmp/type-rb-native-gate6b-driver \
  /tmp/type-rb-native-gate6b-benchmark \
  /path/to/qbe-1.3/qbe \
  /usr/bin/cc \
  /path/to/go \
  /tmp/type-rb-native-gate6b-workspace \
  7 \
  /tmp/type-rb-native-gate6b-raw.csv \
  /tmp/type-rb-native-gate6b-process-inventory.txt
```

Darwin may restrict the `sysctl` calls used by `/usr/bin/time -l` inside an
application sandbox. Run the benchmark in an environment that permits those
read-only counters; a run without maximum resident set size is rejected.

CSV iterations `-2` and `-1` are warmups; medians use only iterations `0` and
later. The process inventory distinguishes recovery and fixed-point preparation
from the ordinary command. The latter is the Native compiler directly starting
the supplied QBE and CC paths with `execv`; it contains no Go, reference
compiler, benchmark harness, shell, or hidden source-content adapter.
