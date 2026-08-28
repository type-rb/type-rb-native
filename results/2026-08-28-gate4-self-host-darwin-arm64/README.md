# Gate 4 Behavioral Self-Hosting Results

Gate 4 passes its registered behavioral self-hosting, correctness,
anti-shortcut, convergence, process-inventory, size, build-time, and memory
criteria. A compiler source closure written in TypeRB crosses B0, B1, B2, and
B3, and ordinary B1-to-B2 regeneration does not require Go or the reference
`trb` compiler.

This is not a production-readiness result. The compiler accepts a bounded
single-source subset, receives its source through an argument adapter, and uses
process-lifetime allocation in self-emitted executables. Gate 5 owns matched
product behavior, full TypeRB compatibility, production runtime integration,
and representative performance.

## Revisions and environment

- TypeRB reference compiler and recovery snapshot v4 producer:
  `57b4ff018cfbc0539c9b4cbbe4c0676afa429857`
- measured TypeRB Native compiler and bootstrap implementation:
  `b48e6b49fadd99f09805cbdefdf85f5dab67494d`
- QBE: release 1.3, corresponding to upstream commit
  `c0818978acec60ebb6167fade60fb7012cbf20ca`
- target profile: `darwin-arm64-v0` / QBE `arm64_apple`
- machine: Apple M2 Pro, 32 GiB RAM
- operating system: macOS 26.6.2 (25G83), arm64
- Go: 1.27.0 darwin/arm64
- C toolchain: Apple clang 21.0.0, target `arm64-apple-darwin25.6.0`

The committed [`raw.csv`](raw.csv) contains 152 measurement rows and no
nonzero status. [`process-inventory.txt`](process-inventory.txt) records the
Go-free regeneration recipe and binary probes.

## Correctness and convergence

The automated bootstrap test performs this complete chain:

```text
pinned reference trb + snapshot v4 + managed Gate 3 path -> B0
B0 + runtime-supplied compiler source                    -> B1 QBE -> B1
B1 + runtime-supplied compiler source                    -> B2 QBE -> B2
B2 + runtime-supplied compiler source                    -> B3 QBE -> B3
```

B1, B2, and B3 QBE are byte-identical:

```text
5faa8c2faed50816eb6afb97d4867da36e00856640a64b5e4dd7f776a8aeb396
```

The linked Mach-O files differ because the linker writes per-link metadata;
raw executable identity was pre-registered as Gate 5 work. Their code input,
raw size, and stripped size converge.

The conformance suite passes for B0, B1, and B2:

- three valid programs covering control flow, records and Arrays, and Strings
  plus direct calls;
- a base program and two independent source mutations, each with distinct QBE
  and runtime output;
- seven exact lexical, syntax, duplicate-declaration, unresolved-call, arity,
  type-mismatch, and unsupported-type diagnostics;
- `check` and `emit-qbe` rejection paths for every invalid source, proving that
  failure precedes code generation; and
- two independent QBE emissions at every compiler stage for every valid input.

The checked-in compiler source itself passes lexing, parsing, resolution,
checking, repeated emission, and regeneration at every required stage. The
repository suites pass with 70 native tests and 10 compiler tests.

## Measurement method

The benchmark first built the recovery B0 three times. It then built B1 once,
ran two unrecorded-index warmup builds for B1 and B2 (retained in `raw.csv` as
iterations -2 and -1), and recorded ten B1-to-B2 and ten B2-to-B3 builds. The
order alternated by iteration. B2 is freshly linked by the preceding B1 build
in half of the observations, so first-launch validation cost remains in the
data instead of being removed.

The harness also recorded:

- one B0-to-B1 build;
- one full-build and one direct-compiler peak-RSS observation for B0, B1, and
  B2 using `/usr/bin/time -l`;
- raw, `strip -x`, and emitted-QBE sizes;
- three recovery-distribution components and two native-distribution
  components; and
- two warmups plus ten size-optimized Go backend builds as a diagnostic,
  unmatched baseline.

The measurement driver is orchestration infrastructure. The separately checked
`tools/gate4-bootstrap.sh` recipe establishes the ordinary Go-free semantic
path directly from B1, QBE, and system tools, and reproduces the recorded B2
QBE hash.

## Build results

Times are seconds. B1 and B2 values are medians of ten observations. Recovery
is the median of three. B0-to-B1 was recorded once because it is a recovery-seed
diagnostic rather than the ordinary self-host path.

| Build | Total | Compiler / emit | QBE | Link |
| --- | ---: | ---: | ---: | ---: |
| reference snapshot path -> B0 | 2.516418 | 1.439077 emit | 0.276286 | 0.582553 |
| B0 -> B1 | 12.088024 | 11.682360 | 0.077851 | 0.314482 |
| B1 -> B2 | 0.711847 | 0.301406 | 0.077136 | 0.318424 |
| B2 -> B3 | 0.809224 | 0.399853 | 0.077075 | 0.321527 |
| optimized Go backend diagnostic | 0.314782 | not separated | n/a | included |

B1-to-B2 is 12.0% faster than B2-to-B3. It therefore satisfies the registered
25% convergence bound. The B2 observations range from 0.672173 to 1.062318
seconds, and no stage-to-stage observation approaches the catastrophic 2x
threshold.

The B0 compiler is deliberately expensive: it is emitted through the general
Gate 3 managed runtime and takes 11.68 seconds for compiler emission. Once the
self-emitted compiler crosses to B1, compiler emission falls to a 0.301-second
median.

## Memory and artifact sizes

Peak RSS is one warm observation in bytes.

| Candidate | Full build RSS | Compiler RSS | Raw compiler | Stripped compiler | Emitted QBE |
| --- | ---: | ---: | ---: | ---: | ---: |
| B0 | 91,537,408 | 94,699,520 | 379,584 | 347,864 | 333,181 |
| B1 | 294,207,488 | 294,502,400 | 162,448 | 133,016 | 333,181 |
| B2 | 294,895,616 | 294,486,016 | 162,448 | 133,016 | 333,181 |
| optimized Go diagnostic | 101,089,280 | not separated | 1,366,130 | 1,366,184 | n/a |

B1 and B2 full-build RSS differ by 0.23%, direct compiler RSS differs by
0.006%, and stripped compiler sizes are identical. All are well inside the
registered 25% bound and far from 2x.

The unusually high B1/B2 RSS is real. The bounded Gate 4 compiler preallocates
source-sized storage for many parallel tables and uses process-lifetime
allocation. This is acceptable for the behavioral checkpoint but is a primary
Gate 5 optimization and runtime-integration target.

## Distribution size

System components shared by both paths are excluded.

| Component | Bytes | Distribution |
| --- | ---: | --- |
| stripped B2 compiler | 133,016 | native |
| QBE 1.3 | 403,424 | native and recovery |
| size-optimized pinned reference `trb` | 26,885,874 | recovery |
| Go 1.27 root | 283,246,592 | recovery |

The ordinary native distribution is 536,440 bytes (0.51 MiB). The recovery
distribution is 310,535,890 bytes (296.15 MiB). The native path is therefore
99.827% smaller, well beyond the registered 30% reduction.

## Go-free process inventory

The direct B1-to-B2 recipe executes:

```text
/bin/sh
  /bin/cat
  B1 native compiler
  QBE 1.3
  /usr/bin/cc
    clang -cc1
    clang -cc1as
    ld
```

B1 imports only `calloc`, `exit`, `memcmp`, `memcpy`, `realloc`, `strlen`, and
`write`. It has no process-spawn symbol, no Go build metadata, and dynamically
loads only `libSystem.B.dylib`. QBE likewise has no process-spawn import. The
system `cc` driver reports the listed Clang assembler and linker subprocesses.

Neither `go`, the reference `trb`, the Go-built measurement driver, nor a
semantic fallback appears in this ordinary chain. The reference compiler and
Go toolchain occur only in the separately measured recovery B0 construction.

## Diagnostic comparison with Go

The self-hosted B1-to-B2 median is 126.1% slower than the optimized Go backend
diagnostic, and its full-build RSS is 191.0% higher. The native compiler file is
90.3% smaller.

This is not a matched product comparison. The Go-built artifact uses the
source's ordinary empty `main`, so its linker may discard compiler entry code;
the native artifact uses the Gate 4 adapter and is a working compiler. The
native compiler also implements only the registered subset and still uses a
high-allocation bootstrap representation. These results are retained because
they identify the most important Gate 5 work, not because they satisfy product
non-inferiority.

## Gate evaluation

- Genuine TypeRB-authored compiler passes and runtime-supplied source: pass.
- B0 -> B1 -> B2 behavioral self-hosting: pass, with a B3 fixed-point check.
- Valid and invalid compiler conformance: pass with exact cross-stage output.
- Source sensitivity and anti-shortcut mutations: pass.
- Repeated deterministic QBE emission: pass at every required compiler stage.
- Go-free B1-to-B2 process inventory: pass.
- B1/B2 build-time convergence: pass at a 12.0% difference.
- B1/B2 peak-RSS convergence: pass at a 0.23% full-build difference.
- B1/B2 stripped size convergence: pass with identical sizes.
- Distribution reduction: pass at 99.827%.
- Catastrophic regression guard: pass; no required comparison reaches 2x.

Gate 4 therefore passes. Development stops before Gate 5 for maintainer review.
