# Gate 6D Linux arm64 Target Chain

Gate 6D closes the existing self-hosted product slice in a second primary
environment. Its correctness and measurement bounds were registered before
implementation in
[issue #47](https://github.com/type-rb/type-rb-native/issues/47). The target
boundary is defined by
[Decision 0011](decisions/0011-linux-arm64-target-profile.md).

## Status

Gate 6D is active. The target implementation and permanent Darwin regression
coverage landed at TypeRB Native revision
`2a72c048a835804a2fd1bd35e5f2788ddf7a6892`. The TypeRB-authored
[`gate6d-benchmark`](../tools/gate6d-benchmark/README.md) now provides the
pinned Linux verification and measurement controller; a reviewed seven-run
result remains required to complete the gate. This is not a release and does
not create a supported TypeRB target.

## Target boundary

The experimental build command selects the Linux profile explicitly:

```text
compiler build SOURCE --output OUTPUT --qbe QBE --cc CC --target linux-arm64-v0
```

`linux-arm64-v0` maps to QBE 1.3 `arm64`, the Linux AArch64 system ABI, and the
system C driver's ELF link using `-Wl,--gc-sections,--strip-all`. The existing
target-less command remains only a `darwin-arm64-v0` compatibility shape while
this internal CLI evolves. An unsupported profile must fail before reading the
source or invoking either supplied tool path.

Target selection changes neither the checked-in compiler source nor its
target-neutral QBE IL. The lexer, parser, resolver, checker, emitter, runtime
semantics, diagnostics, and conformance inputs are common to both environments.

## Bootstrap roles

The Linux experiment may recover one B1 seed by translating the same
target-neutral compiler QBE used by the Darwin integration test:

```text
recovery setup only:
reference TypeRB -> B0 -> compiler QBE -> Linux QBE + CC -> B1 seed

ordinary Linux chain:
B1 seed -> Native build -> B2/compiler
B2/compiler -> Native build -> B3/compiler
B3/compiler -> Native build -> B4/compiler
```

The ordinary chain invokes only the current Native seed, the explicit QBE
binary, the explicit C toolchain driver, and their assembler/linker children.
Go, the reference `trb`, recovery helpers, a shell, and the measurement harness
as a child are forbidden. Initial seed preparation is recorded separately.

## Correctness requirements

The permanent Linux verification must require:

- successful `check` and byte-identical `emit-qbe` for the compiler source at
  B1, B2, B3, and B4;
- actual B1 to B2 to B3 to B4 Native-owned ordinary builds;
- exact B2, B3, and B4 executable bytes from the link recipe, without
  post-link normalization;
- the complete existing valid, mutation, and invalid file-command corpus with
  identical diagnostics and observable behavior;
- deterministic executable behavior for every valid and mutation application;
- exact failure behavior for unsupported profiles, invalid source, missing or
  failing tools, publication errors, and paths containing spaces;
- no leaked `*.trbn.*` intermediate after success or failure;
- ELF identity, architecture, interpreter, imported-library, dynamic-symbol,
  and process-graph inventories; and
- an unchanged Darwin arm64 default path plus an explicit Darwin profile that
  produces the same executable bytes.

The Linux result uses a pinned, reproducible arm64 environment and records the
container or machine image identity, libc, system compiler, linker, QBE, host,
and repository revisions.

## Registered measurement

After two warmups, seven alternating observations compare each Native-owned
Linux build with the equivalent external QBE and CC recipe. Focused bootstrap
measurements also cover each adjacent B1-to-B2, B2-to-B3, and B3-to-B4 step.
Elapsed time and orchestration-root peak RSS are recorded for every observation.

The Native-owned command must remain within 25% of the stronger external recipe
for median time and observed peak RSS. Adjacent Native generation medians must
remain within 10%. A greater-than-2x regression stops the slice for diagnosis.
B2, B3, and B4 raw bytes and SHA-256 must match exactly. Reapplying the standard
strip tool must leave equal generation sizes, and the Linux stripped compiler
must not exceed 208,530 bytes, 25% above the 166,824-byte Darwin Gate 6C
baseline.

These bounds are Linux feasibility checks, not a claim that unlike operating
systems have directly comparable absolute performance. Results report both the
compiler alone and the required QBE sidecar; system linker and dynamically
provided libraries remain identified.

## Delivery sequence

1. Add the explicit profile boundary and preserve Darwin behavior. Complete.
2. Add a reproducible Linux arm64 verification and measurement harness.
   Complete when its implementation PR lands.
3. Record raw measurements, artifacts, provenance, and the process inventory.
4. Close the gate only after every registered correctness and performance
   condition passes.

## Deferred scope

Gate 6D does not design automatic tool discovery, a stable `--target` option,
cross compilation, x86-64, static or musl releases, multi-module projects,
package/native-library integration, debugging, signing, or release seed trust.
Those remain later product-feasibility slices.
