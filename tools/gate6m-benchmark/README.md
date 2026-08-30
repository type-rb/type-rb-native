# Gate 6M Benchmark Harness

This TypeRB-authored Darwin controller verifies and measures the portable
benchmark-entry primitives under the boundary pre-registered in
[issue #113](https://github.com/type-rb/type-rb-native/issues/113).

It accepts exact checkouts of the fixed pre-Gate-6M baseline and the merged
Gate 6M implementation, plus the immutable Darwin arm64 compiler from
`bootstrap-seed-2026-08-30`. Recovery never runs inside the controller. The
harness:

1. verifies the revisions, clean compiler closures, seed, portable success and
   failure corpora, and pinned TypeRB `0.4.3-dev` oracle;
2. raises the published seed into each source revision through two explicit,
   untimed, Go-free setup transitions, then closes independent B2/B3/B4 chains;
3. requires exact B2/B3/B4 bytes and registered target-neutral fixed-point QBE
   within each chain;
4. builds the same successful and failing TypeRB projects with candidate Native
   and optimized Go, requiring byte-identical successful output and matching
   runtime-failure classes;
5. records two warmups and seven alternating baseline/candidate compiler build
   observations and independent peak-RSS observations;
6. records the same series for adjacent candidate generations and enforces a
   25% median-spread ceiling;
7. records two warmups and eleven alternating Native/Go application build and
   runtime observations, with independent peak-RSS series; and
8. records raw observations, medians, source and artifact hashes, exact
   commands, versions, dependencies, libm linkage, sizes, and cleanup.

Candidate compiler build time and RSS may be at most 15% above the fixed
baseline. Native application build time, build RSS, runtime, and runtime RSS
may be at most 25% above optimized Go. The stripped Native application must be
at least 80% smaller than the stripped optimized-Go application. The raw
Darwin compiler must not exceed 310,000 bytes. Thresholds are checked only
after raw evidence and the process inventory have been written.

Build the observer with the pinned TypeRB compiler:

```text
trb build --compile \
  --config tools/gate6m-benchmark/trbconfig.jsonc \
  --outfile /tmp/gate6m-benchmark
```

Run it with a new workspace:

```text
gate6m-benchmark \
  CANDIDATE_ROOT BASELINE_ROOT SEED SEED_PROVENANCE BENCHMARK \
  REFERENCE_TRB QBE CC GO WORKSPACE RAW_CSV INVENTORY
```

`BASELINE_ROOT` must be a clean exact checkout of
`71495bbf18f0820891ea086104ca7da808bfd25f`. `CANDIDATE_ROOT` must be a clean
exact checkout of `4a34ad49052cacd0b5a411b2d0846a5afe09aa97`. `SEED` must be the
259,032-byte Darwin asset from the immutable experimental bootstrap release,
with SHA-256
`ef438d13598c534766334b408a39715c56ff1b69db528910ebf7d90ec7720b65`.
`REFERENCE_TRB` must report `0.4.3-dev`; one inherited Go cache policy applies
to every warmup and observation.

The controller is an observer compiled from TypeRB source, not a child of
either ordinary compiler chain. Linux arm64 correctness and asset-size
evidence run separately because this controller intentionally uses Darwin's
`/usr/bin/time -l`, Mach-O inspection, and linker policy.
