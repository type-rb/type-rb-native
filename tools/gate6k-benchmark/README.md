# Gate 6K Benchmark Harness

This TypeRB-authored controller verifies and measures the explicit
configured-project path under the boundary pre-registered in
[issue #80](https://github.com/type-rb/type-rb-native/issues/80).

It accepts the exact Gate 6J source baseline, the Gate 6K implementation
checkout, and the retained Gate 6J B4 compiler. Recovery never runs inside the
controller. The harness:

1. verifies the baseline and candidate revisions, compiler-closure source
   hashes, retained seed, checked-in configured-project fixture, and generated
   1,025-file scale project before measurement;
2. closes a fresh ordinary Gate 6J B2/B3/B4 chain, introduces the new physical
   directory adapter through one untimed Go-free transition, then closes the
   configured-project-capable Gate 6K B2/B3/B4 chain;
3. requires exact B2/B3/B4 compiler bytes and fixed-point QBE within each
   chain, and exact registered compiler, application, manifest, and QBE hashes;
4. requires configured and file-root Native inputs to emit identical scale
   QBE, build byte-identical same-basename applications, and print exactly
   `module-scale-ok`;
5. exercises deterministic ordering, exclusions, direct/index precedence,
   spaces, unreadable inputs, symlinks, invalid complete-source projects,
   entrypoint cardinality, missing imports, cycles, tool-launch suppression,
   atomic output preservation, and intermediate cleanup;
6. rebuilds the registered Gate 6E representative, Gate 6I scalar Float, and
   Gate 6J Float Array applications and requires their exact bytes and behavior;
7. records two warmups and eleven alternating observations for configured and
   file-root Native check, emit, and complete build time, then records an
   independent peak-RSS series;
8. alternates configured Native check and build against the pinned optimized-Go
   configured-project path, and records three warmups plus 31 retained
   alternating Native/Go runtime observations; and
9. records raw observations, medians, source and artifact hashes, exact
   commands, tool versions, dependencies, sizes, and intermediate cleanup.

The registered Darwin thresholds keep configured Native check, emit, and build
time and RSS within 15% of the same candidate's file-root path. Configured
Native check and build time and RSS, plus application runtime and runtime RSS,
must remain within 25% of optimized Go. The stripped Native application must
be at least 80% smaller than the optimized-Go application. Candidate canonical
compiler emit/build time and RSS must stay within 15% of the fresh Gate 6J
baseline, and the stripped candidate compiler must not exceed 248,000 bytes.

Build it with the pinned TypeRB compiler:

```text
trb build --compile \
  --config tools/gate6k-benchmark/trbconfig.jsonc \
  --outfile /tmp/gate6k-benchmark
```

Run it with a clean temporary workspace:

```text
gate6k-benchmark \
  CANDIDATE_ROOT BASELINE_ROOT SEED SEED_PROVENANCE BENCHMARK \
  REFERENCE_TRB QBE CC GO WORKSPACE RAW_CSV INVENTORY
```

`BASELINE_ROOT` must be an exact checkout of
`e9b00ed946919957fad82b6d2d3ffccfe8cd48d1`. `CANDIDATE_ROOT` must be an exact
checkout of `196741058ef85f68b98f08f7371015367e059768`. `SEED` must be the retained
Gate 6J B4 artifact. `REFERENCE_TRB` is the pinned Go implementation and uses
one inherited Go cache policy for every warmup and observation.

The controller is an observer compiled from TypeRB source. It is not a child
of either ordinary Native compiler chain. The pinned Linux arm64 correctness
run remains separate because this Darwin controller uses `/usr/bin/time -l`,
Mach-O inspection, and the Darwin linker policy.
