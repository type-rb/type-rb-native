# Gate 6N Linux amd64 Target Chain

Gate 6N extends the ordinary self-hosted compiler to Linux amd64. Its
correctness and measurement bounds were registered before implementation in
[issue #128](https://github.com/type-rb/type-rb-native/issues/128). The target
and recovery boundary is defined by
[Decision 0025](decisions/0025-linux-amd64-target-profile.md).

## Status

In progress. The registered profile and permanent target-selection tests are
implemented. No Linux amd64 fixed-point or performance result is claimed until
the fresh hosted workflow and raw evidence pass every frozen condition.

## Target boundary

The internal build profile is selected explicitly:

```text
compiler build SOURCE --output OUTPUT --qbe QBE --cc CC \
  --target linux-amd64-v0
```

`linux-amd64-v0` maps to QBE 1.3 `amd64_sysv`, the System V AMD64 ABI, an
explicit GCC- or Clang-compatible C driver, LLD selected with
`-fuse-ld=lld`, Linux dead-code and symbol stripping, and the existing dynamic
libm boundary. The initial environment is a fresh GitHub-hosted
`ubuntu-24.04` x64 runner.

Target selection does not fork TypeRB source behavior, the self-hosted
frontend, target-neutral QBE, managed runtime semantics, or the conformance
corpus. Existing Darwin and Linux arm64 profiles retain their exact mappings.

## Recovery and candidate roles

The existing experimental seed release contains no amd64 executable. Its
target-neutral root QBE is therefore the one-time recovery input:

```text
setup only:
immutable root QBE -> QBE amd64_sysv + CC/LLD -> root-era amd64 compiler
root-era compiler  -> emit current compiler QBE -> external QBE + CC/LLD -> first transition
first transition   -> emit current compiler QBE -> external QBE + CC/LLD -> current-runtime transition

candidate chain:
current-runtime transition -> ordinary Native build -> B2
B2                         -> ordinary Native build -> B3
B3                         -> ordinary Native build -> B4
```

The root asset must match its registered 658,639-byte size and
`62db3c31527a670c3050051a9fa27bf142b6c5deaab81ef8234104bd467aa95a`
SHA-256 before execution. Setup compilers remain separately identified and
excluded from candidate measurements. Setup is Go-free but is not described as
a previous Native release. The second external translation is required because
the first transition contains current compiler logic but still has the
root-era executable driver's target dispatch. Only the current-runtime
transition can execute an ordinary `linux-amd64-v0` build.

## Correctness requirements

The hosted verifier must require:

- exact B2/B3/B4 compiler bytes and target-neutral fixed-point QBE;
- each candidate compiler as the executable seed of the next ordinary build;
- the canonical multi-file compiler closure, complete file-command corpus,
  configured project, portable-entry primitives, managed runtime, mutations,
  failures, atomic publication, and intermediate cleanup;
- exact portable application output and failure classes against the pinned
  optimized Go oracle;
- deterministic rejection of unknown profiles before source and tool access;
- ELF64 x86-64 architecture, interpreter, segment, hardening, dependency,
  undefined-symbol, and absent-Go-metadata inventories;
- process traces that include QBE, the explicit C driver, assembler, and LLD
  but exclude Go, the reference compiler, recovery generators, and shell
  children from the ordinary Native chain; and
- unchanged Darwin arm64 and Linux arm64 regression evidence.

## Registered measurements

All primary comparisons occur on one pinned fresh x64 runner. Cross-target
absolute values are context only.

After two warmups and seven interleaved observations, Native-owned compiler
build time and orchestration-root peak RSS must remain within 25% of the
equivalent external emit-QBE/QBE/CC recipe. Adjacent B2-to-B3 and B3-to-B4
medians must remain within 10%. A time or RSS value above 2x the strongest
applicable same-runner baseline is catastrophic. Each candidate compiler must
remain at or below 310,000 raw bytes.

One unchanged portable application uses two warmups and at least eleven
interleaved Native/optimized-Go observations. Native build time, build peak
RSS, runtime, and runtime peak RSS must each remain within 25% of the stronger
result, and the stripped Native application must remain at least 80% smaller.
The complete Native, QBE, C-driver, LLD, dynamic-library, Go toolchain, and Go
runtime boundaries are reported separately.

The bounds remain frozen after formal observation. A miss keeps the gate open
for diagnosis and optimization.

## Delivery sequence

1. Add the internal profile mapping, decision, and permanent static tests.
2. Add the immutable-root recovery and current-source transition harness.
3. Close exact candidates and the complete Linux amd64 correctness corpus.
4. Run and audit the frozen compiler and application measurements.
5. Commit raw evidence and a reviewed result before closing issue #128.

## Deferred scope

Gate 6N does not publish an amd64 seed, add automatic host or toolchain
discovery, promise cross compilation, define a stable target CLI, add musl or
static linking, introduce a target-specific runtime, or establish production
support.
