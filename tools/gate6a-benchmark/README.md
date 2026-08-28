# Gate 6A Benchmark Harness

This TypeRB-authored harness records the Gate 6A file-entry measurements
registered in
[issue #35](https://github.com/type-rb/type-rb-native/issues/35). It is a
measurement orchestrator, not part of the ordinary compiler process.
The current harness is deliberately specific to the registered Darwin arm64
observation; a second target remains later Gate 6 work.

The harness:

1. builds B0 through B3 and rejects a QBE fixed-point mismatch;
2. rejects a normalized B1/B2 executable mismatch;
3. checks file and hidden source-content behavior before measuring;
4. records two indexed warmups and the requested alternating observations for
   B1/B2 file and hidden QBE emission;
5. records up to three alternating peak-RSS observations through
   `/usr/bin/time -l`;
6. strips B1/B2 and rejects either artifact above the registered 164,498-byte
   limit derived from the 149,544-byte Gate 5 baseline; and
7. writes a process inventory that verifies direct file checking and emission,
   dynamic dependencies, undefined symbols, absent Go metadata, and normalized
   load commands.

Build the repository driver and this harness with the pinned reference
compiler:

```sh
trb build --compile --outfile /tmp/type-rb-native-gate6a-driver
trb build --compile \
  --config tools/gate6a-benchmark/trbconfig.jsonc \
  --outfile /tmp/type-rb-native-gate6a-benchmark
```

Then run seven recorded observations. Keep the workspace and outputs outside a
committed result directory until the run passes and is reviewed.

```sh
/tmp/type-rb-native-gate6a-benchmark \
  "$PWD" \
  /path/to/pinned/trb \
  /tmp/type-rb-native-gate6a-driver \
  /path/to/qbe-1.3/qbe \
  /usr/bin/cc \
  /path/to/go \
  /tmp/type-rb-native-gate6a-workspace \
  7 \
  /tmp/type-rb-native-gate6a-raw.csv \
  /tmp/type-rb-native-gate6a-process-inventory.txt
```

Darwin may restrict the `sysctl` calls used by `/usr/bin/time -l` inside an
application sandbox. Run the benchmark in an environment that permits those
read-only counters; a run without the maximum resident set size is rejected.

The CSV keeps warmups as iterations `-2` and `-1`; reported medians use only
iterations `0` and later. The process inventory distinguishes recovery and
fixed-point preparation from the direct file command. The latter consists of
the measurement parent launching one Native compiler, which reads through
libc and writes QBE to stdout without spawning Go, the reference compiler, a
shell, QBE, a linker, or another child.
