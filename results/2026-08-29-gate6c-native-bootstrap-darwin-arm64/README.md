# Gate 6C Native-to-Native Bootstrap Results

Gate 6C passes its registered bootstrap-closure, correctness, ownership,
fixed-point, reproducibility, elapsed-time, peak-RSS, compiler-size, cleanup,
and process-inventory criteria. Starting from one explicitly separated B1
seed, the compiler built B2, B2 built B3, and B3 built B4 through the ordinary
Native-owned `build` command. Every produced compiler was the actual executable
seed of the next step.

B2, B3, and B4 are byte-identical without normalization. No Go executable,
reference compiler, recovery driver, measurement-harness child, shell, or
hidden source-content adapter appears in the ordinary chain. QBE, CC, the
assembler/linker, and system libraries remain explicit external tools.

This closes the measured Native regeneration chain after a seed exists. It is
not a release, a seed-trust policy, or the complete Gate 6 product-feasibility
exit.

## Revisions and environment

- TypeRB Native implementation and harness:
  `622d5931e677f7b9283c073021ac0ef39fafa1a5`
- TypeRB reference compiler used only for recovery setup:
  `fa9e0503cc681bcaa691f6f11d2f1e19ca8e6453` (`0.3.49-dev`)
- checked-in compiler source: 117,419 bytes, SHA-256
  `861676131a1a83a36285f93c89f7ee6a7165c97d92990fefb79233bfff952b20`
- QBE: release 1.3, SHA-256
  `03f50f24156449e0df41ef65444add1670d017be822edf4aa99bc8566952592b`
- target profile: `darwin-arm64-v0` / QBE `arm64_apple`
- machine: Apple M2 Pro, 32 GiB RAM
- operating system: macOS 26.6.2 (25G83), arm64
- Go inventory tool: 1.27.0 darwin/arm64
- C toolchain: Apple clang 21.0.0, target `arm64-apple-darwin25.6.0`

The TypeRB-authored recovery driver and focused benchmark controller have
SHA-256 values
`7dae6633e61f9b3941e65b5d2b1c2705d19f0c00e2b1f8920c4a16b0bdf73839`
and
`80c6ea13250596eb2532aa49d91ffbaaf795d56a1568b40cba923aef163c204e`.

The committed [`raw.csv`](raw.csv) contains 57 measurement rows and no nonzero
measurement status. The 1,279-line
[`process-inventory.txt`](process-inventory.txt) records 40 commands. Its only
four nonzero statuses are the required negative probes proving that B1, B2,
B3, and B4 contain no Go build metadata. The committed raw and inventory files
have SHA-256 values
`703bd402c4ddc975595cf6920e9f11ec127ee5f69551d8929575727b7421f867`
and
`6dc5f5516279d383d000206895e412e938788c7c81d648a0387404416768181a`.

## Seed provenance and ownership boundary

The initial B1 was prepared once through the documented recovery route:

```text
pinned Go reference trb -> B0 -> B1 seed
```

Its SHA-256 is
`b5c64cedf4b36ecd78ea0e5aeb7867771f49156aebba1469eb4fd19770d10ff7`.
The exact commands, phase output, revisions, and B0/B1 hashes are retained in
[`seed-provenance.txt`](seed-provenance.txt). Seed creation was completed before
the focused harness ran and is absent from every elapsed-time and RSS row.

The measured ordinary chain was:

```text
B1 Native seed -> QBE -> CC -> assembler/linker -> B2/compiler
B2/compiler -> QBE -> CC -> assembler/linker -> B3/compiler
B3/compiler -> QBE -> CC -> assembler/linker -> B4/compiler
```

The harness accepts no reference-compiler or recovery-driver argument. Its
inventory runs another direct three-step chain, records zero stdout/stderr for
each build, and checks each output before using it as the next seed. Undefined
process symbols remain exactly the registered direct boundary: `fork`,
`execv`, and `waitpid`. No `system`, `popen`, `posix_spawn`, or `execve`
fallback is imported. QBE imports no process launcher, and Clang's `-###`
expansion identifies `cc1as` and `/usr/bin/ld`.

B1 through B4 link only to `libSystem`, retain ad-hoc signatures and
content-derived `LC_UUID` load commands, and contain no Go build metadata. No
`*.trbn.*` intermediate remains anywhere in the measured workspace.

## Correctness and fixed point

The repository suite passes with 74 general tests and 11 configured bootstrap
tests. The permanent bootstrap integration test:

- feeds B1 output into B2, B2 output into B3, and B3 output into B4;
- runs the complete valid, invalid, and mutation corpus through the ordinary
  file commands of every chained compiler;
- retains exact failure diagnostics and output-publication behavior;
- requires every compiler to check the checked-in source and emit fixed-point
  QBE; and
- rejects any intermediate leak or executable mismatch.

B2, B3, and B4 are each 202,088 bytes and share SHA-256:

```text
5cd01b87aba0d85cf3b1bb5f6e88905f8ab2d951f9a16342549d5ed98f8176ef
```

Their compiler QBE is 412,513 bytes and retains the established SHA-256:

```text
87b14e4be3ed3eeb299c8848e09c393d135046a770834a9993b578a3ac03abac
```

This is exact executable identity with the common basename `compiler`; no
post-link normalization is involved.

## Measurement method

The TypeRB-authored Gate 6C harness first constructs and verifies the canonical
B1-to-B2-to-B3-to-B4 chain. It then records two warmups (iterations `-2` and
`-1`) and seven elapsed-time observations (iterations `0` through `6`) for
each adjacent generation. Candidate order reverses on alternating iterations.

Peak RSS uses the same two indexed warmups followed by three recorded
observations per candidate through `/usr/bin/time -l`. Every timed observation
starts exactly one seed compiler and includes TypeRB parsing/checking/QBE
emission, QBE, CC, atomic publication, and Native intermediate cleanup.
Correctness probes, byte comparison, hashing, stripping, and inventory work
occur outside the timed interval.

The exact focused command was:

```text
/tmp/type-rb-native-gate6c-tools/benchmark-622d593 \
  /Users/fujita-h/trb/type-rb-native \
  /tmp/type-rb-native-gate6c-final.jTj5Tl/recovery/b1 \
  go-backed-recovery-reference-fa9e050-native-driver-622d593-b0-to-b1 \
  /tmp/type-rb-native-gate6c-tools/benchmark-622d593 \
  /tmp/qbe-1.3/qbe \
  /usr/bin/cc \
  /opt/homebrew/bin/go \
  /tmp/type-rb-native-gate6c-final.jTj5Tl/workspace \
  7 \
  /tmp/type-rb-native-gate6c-final.jTj5Tl/raw.csv \
  /tmp/type-rb-native-gate6c-final.jTj5Tl/process-inventory.txt
```

The Go path is used only for negative metadata inventory probes. It is not
started by a compiler build or otherwise present in the ordinary chain.

## Elapsed-time results

Times are seconds. Median, minimum, and maximum summarize the seven recorded
observations after warmup.

| Native generation | Median | Minimum | Maximum | Versus Gate 6B B1 |
| --- | ---: | ---: | ---: | ---: |
| B1 -> B2 | 0.579261 | 0.574861 | 0.587523 | -1.10% |
| B2 -> B3 | 0.585245 | 0.579036 | 0.596513 | -0.08% |
| B3 -> B4 | 0.587965 | 0.572338 | 0.689204 | +0.39% |

B2-to-B3 is 1.03% above B1-to-B2, and B3-to-B4 is 0.46% above B2-to-B3.
Both adjacent differences are far inside the registered 10% bound. Every
median is within 1.10% of the 0.585709-second Gate 6B baseline, far inside the
registered 25% bound.

The B3-to-B4 maximum contains one visible 0.689204-second observation; the
other six observations range from 0.572338 to 0.593496 seconds. The registered
median remains robust, every command succeeds, and the maximum remains far
below the 2x stop threshold.

## Peak-RSS results

RSS values are bytes. Median, minimum, and maximum summarize three recorded
observations after warmup.

| Native generation | Median | Minimum | Maximum | Versus Gate 6B B1 |
| --- | ---: | ---: | ---: | ---: |
| B1 -> B2 | 36,667,392 | 36,175,872 | 36,864,000 | 0.00% |
| B2 -> B3 | 36,421,632 | 36,405,248 | 36,519,936 | -0.67% |
| B3 -> B4 | 36,503,552 | 36,388,864 | 36,519,936 | -0.45% |

Adjacent medians differ by 0.67% and 0.22%. Every median is within 0.67% of
the 36,667,392-byte Gate 6B baseline. Both registered bounds pass.

## Compiler-size result

The B2/B3/B4 raw outputs are exactly 202,088 bytes. The B1 input is 202,080
bytes because its recovery basename is `b1`; it is not part of the
same-basename identity claim.

All four artifacts strip to 166,824 bytes, exactly the registered Gate 6B
implementation baseline. Raw outputs keep their required names. For the
stripped-code comparison only, the harness writes equal-length `b1.stripped`
through `b4.stripped` outputs. This holds the ad-hoc signature identifier
length constant; writing `compiler.stripped` would add eight non-code bytes due
only to its longer basename.

The Gate 6C bound is therefore met without increasing or weakening the
166,824-byte limit.

## Conclusion and deferred scope

Gate 6C establishes a closed and stable Native-to-Native compiler regeneration
path after an initial seed handoff. Performance and memory remain effectively
flat across actual replacement generations, compiler bytes reach an exact
fixed point, and the ordinary path is Go-free.

It does not yet decide release seed trust, signing, download, retention, or
selection. Project discovery, multiple source modules, toolchain discovery,
production runtime integration, incremental builds, package/native-library
boundaries, a second target, debugging, stable CLI design, and full Gate 6
product feasibility remain open.
