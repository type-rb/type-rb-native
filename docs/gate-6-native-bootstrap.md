# Gate 6C Native-to-Native Bootstrap Closure

Gate 6C turns the measured single-file build into an actual Native compiler
seed chain. Its correctness and measurement bounds were registered before
implementation in
[issue #43](https://github.com/type-rb/type-rb-native/issues/43). The recovery
and ordinary ownership boundary is defined by
[Decision 0010](decisions/0010-native-bootstrap-closure.md).

## Status

The implementation candidate is active. Gate 6C does not close until its
focused Native-chain benchmark, raw observations, seed provenance, process
inventory, and summarized result pass the registered bounds. This is not a
release and does not create a supported compiler distribution.

## Bootstrap roles

The experiment may prepare one B1 seed through the existing recovery path:

```text
reference TypeRB -> B0 -> B1 seed
```

That preparation is recorded but is not part of the ordinary chain. Starting
from B1, only generated Native compilers perform compilation:

```text
B1 seed build compiler.trb -> B2/compiler
B2/compiler build compiler.trb -> B3/compiler
B3/compiler build compiler.trb -> B4/compiler
```

Every command supplies QBE 1.3 and `/usr/bin/cc` explicitly through the Gate 6B
fixed command. The outputs live in distinct directories but use the same
basename so Darwin signatures and executable bytes can be compared directly.

## Correctness evidence

The permanent bootstrap integration test now requires:

- B1 to produce B2, the generated B2 to produce B3, and generated B3 to
  produce B4 through ordinary `build` commands;
- successful source checking and fixed-point QBE emission by every chained
  compiler;
- byte-identical B2, B3, and B4 executable files without normalization;
- no `*.trbn.*` artifact after any generation; and
- ordinary file-command agreement across the complete valid, invalid, and
  mutation corpus for B2, B3, and B4 in addition to the earlier generations.

The output is therefore used as the next compiler seed rather than accepted
only because it executes one probe.

## Ownership boundary

Each ordinary generation has this semantic process graph:

```text
Native seed compiler
    -> QBE
    -> CC
        -> assembler/linker
```

It contains no Go executable, reference `trb`, Native recovery driver,
measurement harness child, shell, or hidden source-content input. The process
that starts a test or timed command remains an observer outside the semantic
chain. The initial B1 provenance is reported separately and is not described as
a Go-free build.

## Registered measurement

After two warmups, seven alternating observations measure B1-to-B2,
B2-to-B3, and B3-to-B4 over the complete checked-in compiler source. The run
also records two RSS warmups followed by up to three observations per step.

Adjacent-generation median time and observed orchestration-root peak RSS must
remain within 10%. Each step must remain within 25% of the same-machine Gate 6B
B1 Native baselines: 0.585709 seconds and 36,667,392 bytes. B2/B3/B4 output
size and SHA-256 must be identical, stripped compiler code must not grow from
166,824 bytes, and any mismatch, leaked intermediate, unexpected process, or
greater-than-2x regression stops the slice for diagnosis.

The TypeRB-authored
[`gate6c-benchmark`](../tools/gate6c-benchmark/README.md) accepts a prepared B1
seed rather than invoking recovery. It constructs and verifies the chained
fixed point before recording indexed warmups, alternating elapsed-time and RSS
observations, executable/QBE hashes and sizes, seed provenance, and the exact
process inventory. The complete source conformance corpus remains enforced by
the permanent bootstrap integration test; the focused harness independently
checks the full compiler source and executable chain used for measurement.
Raw executable identity is measured on the same-basename `compiler` outputs.
The stripped-code measurement uses equal-length `b1.stripped` through
`b4.stripped` names, matching Gate 6B so ad-hoc signature identifier length is
not counted as compiler-code growth.

## Deferred scope

Gate 6C proves regeneration closure after a seed exists. It does not define how
a release seed is signed, audited, downloaded, retained, or selected. Project
loading, multiple source modules, toolchain discovery, production managed
runtime integration, incremental builds, package/native-library boundaries, a
second target, debugging, stable CLI design, and release policy remain later
Gate 6 work.
