# Native MIR Foundation Measurement on Linux arm64

This is the Phase A measurement registered by
[issue #197](https://github.com/type-rb/type-rb-native/issues/197). It measures
the smallest unconnected self-hosted Native MIR skeleton before selecting a
temporary structural envelope. It does not by itself accept a larger compiler
or relax the final compactness objective.

## Exact scope

- accepted Native baseline:
  `a36c7417f0c9bc5bc9705c28ef6340a05caa5f27`;
- measured candidate:
  `f1dabd9d14867709fb36e9d43cacb43d5e05644d`;
- immutable previous-Native release `bootstrap-seed-2026-08-30`;
- Native target profile `linux-arm64-v0`, QBE 1.3, GCC 13.3.0, and
  LLD 18.1.3; and
- successful manual workflow run
  [33593947594](https://github.com/type-rb/type-rb-native/actions/runs/33593947594)
  on `ubuntu-24.04-arm`.

The candidate adds compact fixed-layout Integer rows for functions, blocks,
values, instructions, block arguments, and an empty input-fact carrier. Its
independent verifier covers origins, unique identities, definitions, local
availability, operand and result types, block targets and argument types,
checked failure edges, terminators, and rejection of supplied optimization
facts. It models one synthetic checked scalar/Array loop but is not connected
to ordinary QBE emission.

## Structural result

Each build metric is the median of seven successful adjacent-generation
observations. Ratios are candidate divided by the same-run baseline.

| Metric | Stage | Baseline | Candidate | Delta | Ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| compiler bytes | fixed point | 254,816 | 271,744 | +16,928 | 1.066432x |
| build wall | B2->B3 | 0.92 s | 0.98 s | +0.06 s | 1.065217x |
| build CPU | B2->B3 | 0.91 s | 0.98 s | +0.07 s | 1.076923x |
| build RSS | B2->B3 | 64,376,832 | 64,487,424 | +110,592 | 1.001718x |
| build wall | B3->B4 | 0.91 s | 0.99 s | +0.08 s | 1.087912x |
| build CPU | B3->B4 | 0.90 s | 0.98 s | +0.08 s | 1.088889x |
| build RSS | B3->B4 | 64,327,680 | 64,503,808 | +176,128 | 1.002738x |

The baseline closes at 254,816 bytes with SHA-256
`9ddf4069f2fb5c3599047541d8b331ca25e321ea45c47168e1cf72eaed0295db`.
The candidate closes at 271,744 bytes with SHA-256
`d920331e3769aaa6703744a0b5244205352869cdd16fe113c6f15d937863fa7c`.
The candidate B2, B3, and B4 executables are byte-identical, and its fixed-point
QBE is 955,157 bytes with SHA-256
`2793416d5d55976488d9ad9a292dca92849aac30b846ecc870553bd55b76fff5`.

## Existing application identity

The baseline and candidate produce byte-identical QBE, raw executables, and
stripped executables for all three registered programs:

| Case | QBE bytes | Raw bytes | Stripped bytes |
| --- | ---: | ---: | ---: |
| fannkuch-redux | 53,046 | 19,080 | 19,072 |
| n-body | 67,233 | 22,320 | 22,312 |
| spectral-norm | 52,272 | 19,680 | 19,672 |

Every application returned exact expected stdout and empty stderr. This
confirms that the foundation remains disconnected from ordinary lowering and
makes no runtime-performance claim.

## Correctness and boundary evidence

- all 62 Gate 4 tests and all 80 repository tests pass on the measured source;
- both Linux arm64 compiler chains close exact self-hosted fixed points;
- all fourteen retained build observations per candidate have status zero;
- the retained process traces contain the Native compiler, pinned QBE, exact
  system C driver, assembler, and LLD boundary and no Go or recovery compiler;
- both compilers are AArch64 PIE ELF executables with non-executable GNU stack
  segments and the registered libc dependency; and
- the retained workspace temporary-file inventory is empty.

## Retained evidence

GitHub published artifact `native-mir-foundation-33593947594-1` as artifact ID
9832751086, 450,489 archive bytes, with SHA-256
`533d16bd13af0d50fab8765b442606910aac35c05b25f127cc81f82ce4665d54`.

This result retains all 73 extracted artifact files plus `ARTIFACTS.tsv`.
`EVIDENCE_SHA256SUMS` covers those 74 files and excludes only this README and
itself. Independent verification reproduced every build median, compiler size
and identity, application comparison row, retained application checksum and
expected output, workflow-source digest, ELF boundary, process inventory, and
the empty temporary-file inventory.

## Conclusion

The minimum useful verified MIR foundation costs 16,928 Linux arm64 compiler
bytes, about 6.5% to 8.9% adjacent-build wall/CPU time, and less than 0.3% peak
RSS in this run. Phase B must now freeze a numeric temporary structural
envelope and its recovery checkpoint before this candidate can be judged or
merged. The final Go-competitive build and artifact objectives remain
unchanged.
