# Gate 6B Native Single-File Build Results

Gate 6B passes its registered correctness, ownership, fixed-point,
reproducibility, elapsed-time, peak-RSS, executable-size, compiler-size,
cleanup, and process-inventory criteria. A self-emitted Native compiler reads
the checked-in compiler source, emits QBE IL, directly starts the supplied QBE
and C toolchain paths, and atomically publishes another working Native compiler
without Go, the reference compiler, a shell, or the hidden source-content
adapter in the ordinary semantic build graph.

This is a measured single-file orchestration slice, not the complete Gate 6
product-feasibility exit. Project discovery, multi-module resolution,
toolchain discovery and configuration, production runtime integration,
incremental builds, package/native-library boundaries, a second target,
debugging, release bootstrap policy, and a stable CLI remain later work.

## Revisions and environment

- TypeRB reference compiler and recovery snapshot v4 producer:
  `fa9e0503cc681bcaa691f6f11d2f1e19ca8e6453` (`0.3.49-dev`)
- measured TypeRB Native implementation and harness:
  `1038cfe497a96d9d282db55a54d9eea6509f7868`
- checked-in compiler source SHA-256:
  `861676131a1a83a36285f93c89f7ee6a7165c97d92990fefb79233bfff952b20`
- QBE: release 1.3; measured binary SHA-256
  `03f50f24156449e0df41ef65444add1670d017be822edf4aa99bc8566952592b`
- target profile: `darwin-arm64-v0` / QBE `arm64_apple`
- machine: Apple M2 Pro, 32 GiB RAM
- operating system: macOS 26.6.2 (25G83), arm64
- Go: 1.27.0 darwin/arm64
- C toolchain: Apple clang 21.0.0, target `arm64-apple-darwin25.6.0`

The measured reference `trb` binary SHA-256 is
`af8a0217eb802a17c1b09318532fe9a9577c6b8e0f9cd618942f516fc3539067`.
The generated Native driver and Gate 6B harness SHA-256 values are respectively
`0b26ebbd5fabf88f26c26bff733e1182e84c55bfc6e8dc55fa5b00e42e2a633b`
and
`5d18fe7153eb3115e448cc1b6323dab40c134e4aa77ce1b05f7830e49812980f`.

The committed [`raw.csv`](raw.csv) contains 94 measurement rows and no nonzero
measurement status. The 671-line
[`process-inventory.txt`](process-inventory.txt) records revisions, versions,
binary formats, direct command probes, QBE and CC boundaries, assembler/linker
expansion, dynamic dependencies, undefined symbols, Go metadata probes,
Mach-O signing and load commands, fixed-point hashes, and exact executable
comparison. Its two status-1 commands are the required negative probes proving
that B1 and the compiler it builds are not Go executables.

The committed raw and inventory files have SHA-256 values
`8d5a7579995057bc76c38d7c8470136b398a280a300c0288ea0fe01deec4cf8a`
and
`0a10463d717eb2ae5abab2cb4cb230908626c3b77a3e1c475a8052bad090be13`.

## Correctness, output, and ownership checks

The repository suite passes with 74 tests. Its Gate 4 bootstrap integration
constructs B0 through B3; retains byte-identical compiler QBE and normalized
compiler executables; builds every valid and mutation conformance source with
B1 and B2; rejects every invalid source before deliberately unusable external
tools can run; and checks exact usage, read, intermediate, QBE, CC, publication,
child-stderr, output-replacement, space-bearing path, and cleanup behavior.

The benchmark independently refuses to record measurements unless:

- B1, B2, and B3 compiler QBE reach the same fixed point;
- normalized B1 and B2 compiler executables are identical;
- B1 and B2 Native-owned builds and B1 and B2 external recipes all build the
  checked-in compiler source;
- every produced compiler checks the source and emits the same fixed-point
  QBE; and
- all four same-basename application outputs are byte-identical.

B1, B2, and B3 QBE are byte-identical at 412,513 bytes with SHA-256:

```text
87b14e4be3ed3eeb299c8848e09c393d135046a770834a9993b578a3ac03abac
```

The normalized B1/B2 compiler executables are byte-identical at 202,088 bytes
with SHA-256:

```text
7ae2f8a3aec551d0dfae778b71fba9f207d168afac33e323d98467fdbfd844fe
```

The four application outputs are also byte-identical at 202,088 bytes without
normalization. Their shared SHA-256 is:

```text
5cd01b87aba0d85cf3b1bb5f6e88905f8ab2d951f9a16342549d5ed98f8176ef
```

The ordinary B1 build probe exits 0 with no stdout or stderr, leaves no
`*.trbn.*` artifact, and produces a compiler that checks the source with
`ok`. Its undefined process symbols are exactly the registered direct boundary:
`fork`, `execv`, and `waitpid`; no `system`, `popen`, `posix_spawn`, or `execve`
fallback is imported. QBE imports no process-launch function. The explicit CC
`-###` expansion records Clang's `cc1as` assembler and `/usr/bin/ld` linker.

B1 and the built compiler link only to `libSystem` and contain no Go build
metadata. The built compiler retains an ad-hoc linker signature with identifier
`compiler` and a required content-derived `LC_UUID`. The normalized
fixed-point comparison remains separate and intentionally removes its UUID.

## Measurement method

The TypeRB-authored Gate 6B harness first constructs and verifies B0 through
B3. It then performs two indexed warmups and seven measured elapsed-time
observations for four candidates:

- B1 Native-owned `build`;
- B1 external file-emission/QBE/CC recipe;
- B2 Native-owned `build`; and
- B2 external file-emission/QBE/CC recipe.

Candidate order alternates by iteration. Warmups remain in `raw.csv` as
iterations -2 and -1 but are excluded from medians. Peak RSS uses the same two
indexed warmups followed by three measured alternating observations per
candidate through `/usr/bin/time -l`.

Every observation compiles the complete 117,419-byte checked-in compiler
source. A Native observation starts `B1` or `B2` with the fixed experimental
`build` command and includes QBE emission, QBE, CC, atomic publication, and
cleanup. The comparison observation starts the Go-linked TypeRB benchmark
harness in `external-build` mode, which runs file-oriented `emit-qbe`, writes
the IL, starts the same QBE and CC binaries, and retains its `.ssa` and `.s`
files. This gives the external recipe the lighter artifact policy. Correctness
probes, comparisons, hashing, and size inspection occur after the recorded
elapsed interval.

The exact command was:

```text
/tmp/type-rb-native-gate6b-tools/benchmark-1038cfe \
  /Users/fujita-h/trb/type-rb-native \
  /tmp/type-rb-native-gate5-tools/trb-fa9e050 \
  /tmp/type-rb-native-gate6b-tools/driver-1038cfe \
  /tmp/type-rb-native-gate6b-tools/benchmark-1038cfe \
  /tmp/qbe-1.3/qbe \
  /usr/bin/cc \
  /opt/homebrew/bin/go \
  /tmp/type-rb-native-gate6b-final.IC8hf7/workspace \
  7 \
  /tmp/type-rb-native-gate6b-final.IC8hf7/raw.csv \
  /tmp/type-rb-native-gate6b-final.IC8hf7/process-inventory.txt
```

The reference compiler, Native driver, and benchmark harness are recovery,
fixed-point, or measurement controllers. The ordinary semantic application
build begins at the self-emitted Native compiler and contains only Native,
QBE, CC, the assembler/linker, and system libraries.

## Elapsed-time results

Times are seconds. Median, minimum, and maximum summarize the seven measured
observations after warmup.

| Generation and orchestration | Median | Minimum | Maximum |
| --- | ---: | ---: | ---: |
| B1 Native build | 0.585709 | 0.583161 | 0.592160 |
| B1 external recipe | 0.577538 | 0.564303 | 0.583666 |
| B2 Native build | 0.588153 | 0.571446 | 0.593641 |
| B2 external recipe | 0.570311 | 0.549746 | 0.875136 |

The B1 Native median is 1.41% higher than its same-generation external recipe;
the B2 Native median is 3.13% higher. Both are well inside the registered 25%
non-inferiority bound and far from the 2x stop threshold. B1 and B2 Native
medians differ by only 0.42%.

External B2 observation 3 is a visible 0.875136-second outlier. The registered
median is robust to it; the other six external B2 observations range from
0.549746 to 0.579943 seconds. No command failed, and the Native maxima remain
below 0.594 seconds.

The small positive Native delta is consistent with the additional cleanup and
atomic-publication work in the Native path. It establishes that moving
orchestration into the compiler does not introduce a material build-time
penalty; it does not claim a speed improvement over the deliberately simpler
external recipe.

## Memory results

RSS values are bytes. Median and maximum each summarize three observations
after the two RSS warmups.

| Generation and orchestration | Median | Maximum |
| --- | ---: | ---: |
| B1 Native build | 36,667,392 | 36,814,848 |
| B1 external recipe | 36,438,016 | 36,798,464 |
| B2 Native build | 36,519,936 | 36,618,240 |
| B2 external recipe | 36,421,632 | 36,913,152 |

B1 Native median RSS is 0.63% higher than the external root; B2 Native median
RSS is 0.27% higher. B1 and B2 Native medians differ by 0.40%. Every comparison
is inside the registered 25% bound and far from the 2x stop threshold.

These are observed orchestration-root values reported by `/usr/bin/time -l`
for the complete command and its toolchain work. They are not presented as the
standalone frontend RSS measured in Gate 6A.

## Artifact size

| Artifact | Raw bytes | Stripped bytes |
| --- | ---: | ---: |
| Gate 6A Native B1 baseline | 183,648 | 149,784 |
| Gate 6B Native B1 | 202,080 | 166,824 |
| Gate 6B Native B2 | 202,080 | 166,824 |
| registered stripped ceiling | n/a | 172,251 |

The Native-owned build implementation grows the stripped compiler by 17,040
bytes, or 11.38%, leaving 5,427 bytes of headroom under the registered 15%
ceiling. B1 and B2 sizes are identical.

Every same-basename application output is exactly 202,088 bytes. Native output
therefore has no size or behavior regression from the corresponding external
recipe.

## Gate evaluation

- B1/B2 build every valid and mutation input with registered runtime behavior:
  pass.
- B1/B2 reject every invalid input before external launch and leave no
  artifact: pass.
- Usage, unreadable source, intermediate, child status/stderr, QBE, CC,
  publication, output replacement, spaces, and cleanup contracts: pass.
- B1/B2/B3 QBE fixed point and normalized B1/B2 compiler identity: pass.
- Native and external same-basename application output identity: pass, exact
  size and SHA-256.
- Ordinary graph is Native -> QBE -> CC -> assembler/linker, with no Go,
  reference compiler, shell, or hidden input: pass.
- Native median elapsed time within 25% of the external recipe: pass; 1.41% and
  3.13% higher.
- Native observed peak RSS within 25% of the external recipe: pass; median RSS
  0.63% and 0.27% higher.
- B1/B2 Native time and RSS convergence within 25%: pass; median differences
  are 0.42% and 0.40%.
- Produced executable size and runtime behavior do not regress: pass; outputs
  are byte-identical.
- Stripped compiler growth no greater than 15%: pass; 11.38% growth.
- Greater-than-2x catastrophic-regression guards: pass.

Gate 6B therefore passes. Subsequent Gate 6 work can build project and runtime
capabilities on a measured Native-owned external-tool boundary without treating
this fixed-order experimental command as a supported TypeRB CLI.
