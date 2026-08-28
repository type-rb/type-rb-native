# Gate 5 Matched Self-Hosted Compiler Results

Gate 5 passes its registered matched-compiler correctness, anti-shortcut,
self-hosting, normalization, performance, memory, artifact-size, distribution,
and adjacent-generation criteria. The Native and optimized Go candidates run
the same TypeRB-authored lexer, parser, resolver, checker, and QBE emitter
through the same source-content and mode interface.

This remains a bounded compiler-core result. It does not establish an ordinary
file-oriented CLI, multi-module and incremental builds, a production managed
runtime, package or native-library integration, a second target, or release
readiness. Those remain Gate 6 work.

## Revisions and environment

- TypeRB reference compiler and recovery snapshot v4 producer:
  `fa9e0503cc681bcaa691f6f11d2f1e19ca8e6453` (`0.3.49-dev`)
- measured TypeRB Native implementation:
  `a83699d6dd87de0c77a8a8a395ea6e266802bf0a`
- QBE: release 1.3; measured binary SHA-256
  `03f50f24156449e0df41ef65444add1670d017be822edf4aa99bc8566952592b`
- target profile: `darwin-arm64-v0` / QBE `arm64_apple`
- machine: Apple M2 Pro, 32 GiB RAM
- operating system: macOS 26.6.2 (25G83), arm64
- Go: 1.27.0 darwin/arm64
- C toolchain: Apple clang 21.0.0, target `arm64-apple-darwin25.6.0`

The committed [`raw.csv`](raw.csv) contains 193 measurement rows and no
nonzero measurement status. The 405-line
[`process-inventory.txt`](process-inventory.txt) records revisions, versions,
binary formats, dynamic dependencies, undefined symbols, Go metadata probes,
and the C driver's assembler and linker subprocesses. Its one status-1 command
is the required negative probe proving that B1 is not a Go executable.

## Correctness and anti-shortcut checks

The automated path constructs B0, B1, B2, B3, and a functional optimized Go
compiler from the checked-in compiler source. B0, B1, B2, and matched Go
execute the complete valid, invalid, and mutation corpus in both `check` and
`emit-qbe` modes; B3 provides the additional fixed-point observation. The
generated Go driver is reversible to the canonical source and may change only
the `argv()` import and otherwise empty entry driver.

The repository suites pass with 74 Native tests and 11 compiler tests. They
include empty, growth, exact-boundary, negative-index, and beyond-limit storage
cases. The benchmark additionally refuses to record data unless all compiler
source checks and every measured QBE output match the fixed point.

B1, B2, and B3 QBE are byte-identical at 367,814 bytes with SHA-256:

```text
68382671b72bc19c6995f1c1ad818f517bad8c8085c00c088357f17b626e7329
```

The direct `/bin/sh` bootstrap recipe reproduced B2 from B1 in 0.644734
seconds without invoking Go, the reference `trb`, or a Go-linked compiler
component. B1 imports only `calloc`, `exit`, `memcmp`, `memcpy`, `realloc`,
`strlen`, and `write`; QBE also has no process-spawn import. B1 has no Go build
metadata, while the matched comparison has the expected Go 1.27 metadata.

## Executable normalization

The raw B1 and B2 Mach-O files differ only in link metadata. Normalization
relinks each unchanged, byte-identical assembly with `-Wl,-dead_strip` and
`-Wl,-no_uuid`, using the same `compiler` basename in separate directories.
It removes no code or data section and rejects any result containing
`LC_UUID`.

The complete normalized Mach-O files are byte-identical at 182,888 bytes with
SHA-256:

```text
4e914a10c0a1108b5a09a940a6e3bca319885ac9b5699083f7d0d21e4fba156a
```

This satisfies the executable-equivalence requirement with a stronger full
file comparison rather than a section allowlist.

## Measurement method

The harness performed two indexed warmups and seven measured repetitions for
direct compilation and end-to-end building. It alternated candidate order as
B1 / matched Go / B2 and B2 / matched Go / B1. Warmups remain in `raw.csv` as
iterations -2 and -1 but are excluded from the medians below.

Each direct measurement runs the candidate with the complete compiler source
and `emit-qbe`. Each end-to-end measurement then writes that output, runs QBE
1.3, and links through the same `/usr/bin/cc` configuration. Compiler, QBE,
and link phases are recorded separately. Peak RSS uses three additional
alternating observations per direct and full-build candidate via
`/usr/bin/time -l`.

The exact command was:

```text
/tmp/type-rb-native-gate5-main-benchmark \
  /Users/fujita-h/trb/type-rb-native \
  /tmp/type-rb-native-gate5-tools/trb-fa9e050 \
  /tmp/type-rb-native-gate5-main-driver \
  /tmp/qbe-1.3/qbe \
  /usr/bin/cc \
  /opt/homebrew/bin/go \
  /tmp/type-rb-native-gate5-final.yPN8wF/work \
  7 \
  /tmp/type-rb-native-gate5-final.yPN8wF/raw.csv \
  /tmp/type-rb-native-gate5-final.yPN8wF/process-inventory.txt
```

## Time results

Times are medians of the seven measured observations in seconds.

| Candidate | Direct compiler | End to end | Build compiler phase | QBE | Link |
| --- | ---: | ---: | ---: | ---: | ---: |
| Native B1 | 0.158580 | 0.606238 | 0.170372 | 0.080547 | 0.342947 |
| Native B2 | 0.164893 | 0.611093 | 0.169746 | 0.081358 | 0.348685 |
| matched Go | 31.524057 | 32.134388 | 31.685505 | 0.085252 | 0.356111 |

Native B1 is 198.8x faster for direct compilation and 53.0x faster end to end
than the matched Go compiler. Its measured ranges are 0.151748–0.178566 seconds
direct and 0.601023–0.620384 seconds end to end; the matched Go ranges are
31.422810–31.694947 and 32.032963–32.656541 seconds respectively.

B1 and B2 direct medians differ by 3.98%, and their end-to-end medians differ
by 0.80%. Both are inside the registered 25% adjacent-generation bound and far
from the catastrophic 2x threshold.

## Memory results

RSS values are bytes. Median and maximum each summarize three peak-RSS
observations.

| Candidate | Direct median | Direct max | Full-build median | Full-build max |
| --- | ---: | ---: | ---: | ---: |
| Native B1 | 11,354,112 | 11,354,112 | 36,814,848 | 36,847,616 |
| Native B2 | 11,354,112 | 11,370,496 | 36,585,472 | 36,765,696 |
| matched Go | 13,860,864 | 14,729,216 | 36,274,176 | 36,487,168 |

Native B1 direct median RSS is 18.09% lower than matched Go. Its full-build
median is 1.49% higher, and its conservative maximum-to-maximum comparison is
0.99% higher. Both remain well inside the registered 25% bound. B1/B2 direct
RSS medians are identical, their full-build medians differ by 0.63%, and no
adjacent-stage observation approaches 2x.

## Artifact and distribution size

| Candidate or component | Raw bytes | Stripped bytes |
| --- | ---: | ---: |
| Native B1 compiler | 182,880 | 149,544 |
| Native B2 compiler | 182,880 | 149,544 |
| matched Go compiler | 2,808,338 | 2,699,776 |
| QBE 1.3 | 403,424 | n/a |

The stripped Native compiler is 94.46% smaller than the matched Go compiler.
The ordinary Native compiler-plus-QBE distribution is 552,968 bytes; the
matched Go compiler-plus-QBE distribution is 3,103,200 bytes. Native is
therefore 82.18% smaller, beyond the registered 30% requirement. B1 and B2 raw
and stripped sizes are identical.

The Go toolchain is recorded as recovery/bootstrap infrastructure but is not
charged to ordinary matched compiler execution, exactly as pre-registered.
System components common to both candidates are excluded.

## Gate evaluation

- Exact matched behavior across valid, invalid, mutation, and storage cases:
  pass.
- Complete TypeRB-authored frontend and QBE emitter retained in both artifacts:
  pass.
- B1/B2/B3 QBE fixed point and source sensitivity: pass.
- Full normalized B1/B2 executable identity without dropping code or data:
  pass.
- Ordinary B1-to-B2 process graph free of Go and reference `trb`: pass.
- Native direct compiler time within 25% of matched Go: pass, 99.50% lower.
- Native end-to-end build time within 25% of matched Go: pass, 98.11% lower.
- Native direct and full-build peak RSS within 25% of matched Go: pass.
- Stripped Native compiler at least 30% smaller: pass, 94.46% smaller.
- Native compiler-plus-QBE distribution at least 30% smaller: pass, 82.18%
  smaller.
- B1/B2 time, RSS, and stripped-size convergence within 25%: pass.
- Greater-than-2x catastrophic-regression guards: pass.

Gate 5 therefore passes. Gate 6 may now evaluate the broader self-hosted
product path; this result alone does not authorize a supported Native release.
