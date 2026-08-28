# Gate 6A File-Oriented Compiler Entry Results

Gate 6A passes its registered file-entry correctness, ownership, fixed-point,
normalization, direct-time, peak-RSS, stripped-size, adjacent-generation, and
process-inventory criteria. The self-emitted B1 and B2 compilers read the
checked-in compiler source from a file, execute the complete TypeRB-authored
frontend and QBE emitter, and produce the same QBE as the hidden recovery and
differential adapter.

This is the first Gate 6 slice, not the product-feasibility exit. The compiler
still emits QBE to stdout and does not yet provide project discovery,
multi-module resolution, output management, external QBE/linker orchestration,
the production managed runtime, incremental builds, package/native-library
boundaries, a second target, debugging, or release readiness.

## Revisions and environment

- TypeRB reference compiler and recovery snapshot v4 producer:
  `fa9e0503cc681bcaa691f6f11d2f1e19ca8e6453` (`0.3.49-dev`)
- measured TypeRB Native implementation and harness:
  `cf6fabccf8bd799d5457372f93f024687d5e6d13`
- checked-in compiler source SHA-256:
  `6de852d6fee9736d59e08648a9fe2112e2082f914c5a6f0a03afbcdafb7bdb25`
- QBE: release 1.3; measured binary SHA-256
  `03f50f24156449e0df41ef65444add1670d017be822edf4aa99bc8566952592b`
- target profile: `darwin-arm64-v0` / QBE `arm64_apple`
- machine: Apple M2 Pro, 32 GiB RAM
- operating system: macOS 26.6.2 (25G83), arm64
- Go: 1.27.0 darwin/arm64
- C toolchain: Apple clang 21.0.0, target `arm64-apple-darwin25.6.0`

The measured reference `trb` binary SHA-256 is
`af8a0217eb802a17c1b09318532fe9a9577c6b8e0f9cd618942f516fc3539067`.
The generated measurement driver and harness SHA-256 values are respectively
`10143c1830a2c5c3c126d342195c925a295fcb02accfc38ac1dd68ce1c9ab9a8`
and
`fff347528a418e2bc6de865c82f51633cd8de26650fed1b14e79c3e9c0b96881`.

The committed [`raw.csv`](raw.csv) contains 78 measurement rows and no nonzero
measurement status. The 339-line
[`process-inventory.txt`](process-inventory.txt) records revisions, versions,
binary formats, direct command probes, dynamic dependencies, undefined
symbols, the Go metadata probe, and normalized load commands. Its one status-1
command is the required negative probe proving that B1 is not a Go executable.

## Correctness and ownership checks

The repository suites pass with 74 tests. The bootstrap integration test
constructs B0, B1, B2, and B3, retains byte-identical QBE and normalized
executable identity, and sends the compiler source plus every valid, invalid,
and mutation conformance input through both B1/B2 file commands and the hidden
source-content adapter. File diagnostics use stderr and status 1 without
partial QBE. Usage and unreadable paths have exact stderr and status behavior.
A valid file larger than 512 KiB succeeds, proving that source contents are not
transported through argv.

The benchmark independently refuses to record measurements unless B1 and B2
file and hidden checks pass and every emitted compiler QBE matches the fixed
point. B1, B2, and B3 QBE are byte-identical at 379,112 bytes with SHA-256:

```text
e3c117159ad344a29b9907c3e8955a444cf0360f30e6c22aead376375a53d86c
```

The direct B1 file probes both pass:

```text
B1 check compiler/gate4/src/compiler.trb       -> status 0, 3 stdout bytes, 0 stderr bytes
B1 emit-qbe compiler/gate4/src/compiler.trb    -> status 0, 379112 stdout bytes, 0 stderr bytes
```

B1 imports only `calloc`, `exit`, `fclose`, `fopen`, `fread`, `fseek`,
`ftell`, `memcmp`, `memcpy`, `realloc`, `strcmp`, `strlen`, and `write`. It
imports no process-spawn operation, links only to `libSystem`, and has no Go
build metadata. Therefore the direct compiler process reads the source through
libc and emits QBE without invoking Go, the reference `trb`, a shell, QBE, a C
driver, an assembler, a linker, or another child process. Those external tools
appear only in recovery, fixed-point preparation, or normalization.

## Executable normalization

The B1 and B2 assembly outputs remain byte-identical. The existing normalization
policy relinks each unchanged assembly with `-Wl,-dead_strip` and
`-Wl,-no_uuid` under the same basename, removes no code or data, and rejects an
output containing `LC_UUID`.

The complete normalized Mach-O files are byte-identical at 183,656 bytes with
SHA-256:

```text
e669a71d1d830662c6a1677693fd799466984c1d4bddfbcecc9c6a62b337f387
```

## Measurement method

The TypeRB-authored Gate 6A harness first constructed and verified B0 through
B3. It then performed two indexed warmups and seven measured direct-compilation
observations for four candidates: B1 file, B1 hidden source-content, B2 file,
and B2 hidden source-content. Candidate order alternated by iteration. Warmups
remain in `raw.csv` as iterations -2 and -1 but are excluded from the medians.

Each direct observation runs `emit-qbe` over the complete 110,027-byte checked-in
compiler source and requires exact fixed-point output. The file candidate passes
only the source path; the hidden candidate receives the same source contents
through the explicit recovery adapter. Peak RSS uses three additional
alternating observations per candidate through `/usr/bin/time -l`.

The exact command was:

```text
/tmp/type-rb-native-gate6a-final.9MQ56P/gate6a-benchmark \
  /Users/fujita-h/trb/type-rb-native \
  /tmp/type-rb-native-gate5-tools/trb-fa9e050 \
  /tmp/type-rb-native-gate6a-final.9MQ56P/type-rb-native-driver \
  /tmp/qbe-1.3/qbe \
  /usr/bin/cc \
  /opt/homebrew/bin/go \
  /tmp/type-rb-native-gate6a-final.9MQ56P/workspace \
  7 \
  /tmp/type-rb-native-gate6a-final.9MQ56P/raw.csv \
  /tmp/type-rb-native-gate6a-final.9MQ56P/process-inventory.txt
```

The Go-linked harness and Native driver are measurement and recovery
orchestrators. `/usr/bin/time` wraps only the measured Native compiler process,
and the direct process inventory distinguishes that command from setup.

## Time results

Times are seconds. Median, minimum, and maximum summarize the seven measured
observations after warmup.

| Native generation and entry | Median | Minimum | Maximum |
| --- | ---: | ---: | ---: |
| B1 file | 0.100543 | 0.095998 | 0.103701 |
| B1 hidden source-content | 0.163988 | 0.136489 | 0.177794 |
| B2 file | 0.100399 | 0.095260 | 0.107471 |
| B2 hidden source-content | 0.158665 | 0.147127 | 0.174433 |

The B1 file median is 38.69% lower than its same-generation hidden path; the
B2 file median is 36.72% lower. This is an improvement rather than a regression
against the registered 25% non-inferiority bound. B1 and B2 file medians differ
by 0.14%; even their independently observed maxima differ by only 3.64%.

The result is plausible because the file path avoids copying the complete
source into the parent process argument vector while adding one sequential
file read. The comparison does not claim that filesystem input is intrinsically
faster on every machine; it establishes that the ordinary boundary adds no
measured compiler-time penalty here.

## Memory results

RSS values are bytes. Median and maximum each summarize three peak-RSS
observations.

| Native generation and entry | Median | Maximum |
| --- | ---: | ---: |
| B1 file | 11,698,176 | 11,698,176 |
| B1 hidden source-content | 11,812,864 | 11,845,632 |
| B2 file | 11,714,560 | 11,730,944 |
| B2 hidden source-content | 11,812,864 | 11,845,632 |

B1 file median RSS is 0.97% lower than hidden; B2 file median RSS is 0.83%
lower. B1 and B2 file medians differ by 0.14%, and their maxima differ by
0.28%. Every comparison is inside the registered 25% bound and far from the
2x catastrophic threshold.

## Artifact size

| Artifact | Raw bytes | Stripped bytes |
| --- | ---: | ---: |
| Gate 5 Native B1 baseline | 182,880 | 149,544 |
| Gate 6A Native B1 | 183,648 | 149,784 |
| Gate 6A Native B2 | 183,648 | 149,784 |
| registered stripped ceiling | n/a | 164,498 |

The file entry grows the stripped compiler by 240 bytes, or 0.16%, well below
the registered 10% ceiling. B1 and B2 sizes are identical. The implementation
keeps this result compact by storing the added runtime QBE in multi-line blocks
rather than paying one compiled array operation and object header per emitted
line.

## Gate evaluation

- B1/B2 file behavior equals the hidden path for the compiler and complete
  conformance/mutation corpus: pass.
- Exact stderr, exit status, unreadable path, and no-partial-QBE behavior: pass.
- Valid file beyond conservative argv payload limits: pass, larger than
  512 KiB.
- B1/B2/B3 QBE fixed point and normalized B1/B2 executable identity: pass.
- Direct file command free of Go, reference `trb`, shell, QBE, linker, and
  process spawning: pass.
- File median time within 25% of same-generation hidden input: pass; 38.69% and
  36.72% lower.
- File peak RSS within 25% of same-generation hidden input: pass; median RSS
  0.97% and 0.83% lower.
- B1/B2 file time and RSS convergence within 25%: pass; median differences are
  0.14%.
- Stripped compiler growth no greater than 10%: pass; 0.16% growth.
- Greater-than-2x catastrophic-regression guards: pass.

Gate 6A therefore passes. Subsequent Gate 6 slices can now build output and
project behavior on a measured Go-free file ingress without treating this
experimental command shape as a supported TypeRB interface.
