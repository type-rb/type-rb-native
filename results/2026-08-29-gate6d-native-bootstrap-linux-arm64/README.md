# Gate 6D Linux arm64 Target-Chain Results

Gate 6D passes its registered second-environment correctness, ownership,
bootstrap, reproducibility, elapsed-time, peak-RSS, compiler-size, cleanup, ELF,
and process-inventory criteria. The same TypeRB-authored compiler source and
fixed-point QBE used on Darwin produced a Linux arm64 B1 seed, which built B2;
B2 built B3; and B3 built B4 through the ordinary Native-owned command.

B1, B2, B3, and B4 are byte-identical Linux executables. The complete valid,
mutation, invalid, and build-failure corpus passes at every required generation.
The observed ordinary process graph is Native compiler to QBE to CC to the
assembler and linker. It contains no Go, reference compiler, recovery driver,
measurement-controller child, shell, or hidden source-content adapter.

This completes Gate 6D and establishes a second closed Native target chain. It
does not make either ABI profile, command, runtime, or compiler distribution a
supported TypeRB release.

## Revisions and environment

- measured TypeRB Native implementation and harness:
  `68497f68ed1c3770c2a457790a6519962a2cb921`
- pinned TypeRB recovery/reference compiler:
  `fa9e0503cc681bcaa691f6f11d2f1e19ca8e6453`
- checked-in compiler source: 120,875 bytes, SHA-256
  `69fee8020e1c9c79dd7fe790b65f0a6bbe0f8c1f1fca2343f71e81db389384dd`
- target profile: `linux-arm64-v0` / QBE 1.3 `arm64`
- guest: Debian GNU/Linux 12, LinuxKit 7.0.12, aarch64, 10 virtual CPUs,
  16,353,344 KiB reported memory
- host: Apple M2 Pro, 32 GiB RAM, macOS 26.6.2 (25G83), arm64
- Docker client/server: 29.7.2, native Linux/arm64 server
- C toolchain: Debian GCC 12.2.0-14+deb12u1; binutils 2.40

The digest-pinned Dockerfile produced image
`sha256:cdf6d581bb13fdd7faabf8615f5f132eef7681caf287c822eb56b032debd1cad`
with platform manifest
`sha256:f6382620346530202958bc95cd5528ca3db4384805435af0edccbb9df1065c01`.
The exact base, config, layer identities, package versions, build commands, and
controller hash are retained in
[`environment-provenance.txt`](environment-provenance.txt) and the process
inventory.

The committed [`raw.csv`](raw.csv) has 109 lines including its header and no
nonzero measurement status. The 1,409-line
[`process-inventory.txt`](process-inventory.txt) records 42 commands; all 42
have status 0, and all seven direct output probes match. Their SHA-256 values
are:

```text
raw.csv               150ebf819d2fd76f00b2eb19b8744a1c1db353ae3e4fea470a0458e7b9f0d052
process-inventory.txt  5c87ffef2da8a44322917d804cca6e314e4d393a24c4cc51e78e574f84f0df68
```

## Seed provenance and ownership

Recovery first regenerated the target-neutral compiler QBE from the clean
measured revision, then translated it in the pinned Linux image:

```text
pinned reference TypeRB -> Native recovery path -> fixed-point compiler QBE
fixed-point compiler QBE -> QBE arm64 -> Debian CC -> Linux B1 seed
```

The QBE is 426,689 bytes with SHA-256
`2f4c13bef3040b41e13677b3afc7c0f1d9e2e615b4c42edc9dc3bb8c3f983308`.
The resulting B1 is 175,920 bytes with SHA-256
`fdad3b73240ea0247ead274b95c1a628d5b9f35e0dded6e1893fb8f898c45e00`.
Exact commands and additional hashes are in
[`seed-provenance.txt`](seed-provenance.txt). Recovery completed before the
focused harness started and is absent from every elapsed-time and RSS row.

The ordinary chain was:

```text
B1 Native seed -> QBE -> CC -> assembler/linker -> B2/compiler
B2/compiler -> QBE -> CC -> assembler/linker -> B3/compiler
B3/compiler -> QBE -> CC -> assembler/linker -> B4/compiler
```

An actual `strace -f -e trace=process` inventory observes those executable
boundaries, including `/usr/local/bin/qbe`, `/usr/bin/cc`, `/usr/bin/as`, GCC
`collect2`, and `/usr/bin/ld`. Native compilers import `fork`, `execv`, and
`waitpid`, but not `system`, `popen`, `posix_spawn`, or `execve`. QBE imports no
process launcher. No `*.trbn.*` intermediate remains after success or failure.

## Correctness, ELF, and fixed point

Before measurement, the TypeRB-authored harness requires B1 through B4 to:

- check the complete compiler source and emit the same fixed-point QBE;
- pass three valid and three source-mutation programs with identical QBE,
  executable bytes, runtime stdout, stderr, and status;
- pass seven invalid inputs with exact diagnostics for `check`, `emit-qbe`, and
  `build`, using false tool paths to prove frontend rejection comes first;
- preserve exact unknown-target, missing-source, missing-QBE, missing-CC,
  missing-parent, and publication-failure contracts;
- build and execute paths containing spaces; and
- clean every Native-owned intermediate.

B1, B2, B3, and B4 are each 175,920 bytes and share SHA-256:

```text
fdad3b73240ea0247ead274b95c1a628d5b9f35e0dded6e1893fb8f898c45e00
```

They are stripped ELF64 PIE executables for AArch64, request
`/lib/ld-linux-aarch64.so.1`, require `libc.so.6`, and share Build ID
`28738836d8aa8de886cabf63270d7287629ce94d`. Static symbol tables and Go build
metadata are absent. This is exact ordinary-link output identity; no post-link
normalization is used.

## Measurement method

The harness constructs and verifies the canonical chain, then compares each
Native-owned build with an external recipe that starts the corresponding Native
compiler's `emit-qbe`, writes the IL, and directly invokes the same QBE and CC.
The external controller is a comparison root and never enters the ordinary
Native chain.

Each candidate has two warmups (iterations `-2` and `-1`) and seven recorded
elapsed-time observations (iterations `0` through `6`). Six candidate commands
run in forward order on even iterations and reverse order on odd iterations.
RSS has the same two warmups and three recorded observations through GNU
`time -v`. Correctness probes, hashing, stripping, and inventory work occur
outside timed intervals.

The measurement workspace was container-local Linux storage. Only the seed,
controller, and final reports used a Docker bind mount. A preliminary smoke run
showed that placing the workspace on a macOS bind mount disproportionately
penalized the Native compiler's many small IL writes; that invalid placement was
discarded before this formal run and is not present in the committed data.

## Elapsed-time results

Times are seconds. Median, minimum, and maximum summarize seven observations
after warmup. The comparison column is Native relative to the matching external
recipe; negative is faster.

| Generation | Native median | Native min | Native max | External median | Native vs external |
| --- | ---: | ---: | ---: | ---: | ---: |
| B1 -> B2 | 0.224224 | 0.222154 | 0.229858 | 0.230093 | -2.55% |
| B2 -> B3 | 0.226195 | 0.220309 | 0.233069 | 0.224672 | +0.68% |
| B3 -> B4 | 0.225320 | 0.223425 | 0.227725 | 0.230474 | -2.24% |

The worst Native/external median is 0.68% slower, far inside the registered
25% limit. Adjacent Native medians differ by at most 0.88%, inside the 10%
limit. No observation approaches the 2x stop threshold.

## Peak-RSS results

RSS values are bytes. Median, minimum, and maximum summarize three observations
after warmup.

| Generation | Native median | Native min | Native max | External median | Native vs external |
| --- | ---: | ---: | ---: | ---: | ---: |
| B1 -> B2 | 17,399,808 | 17,395,712 | 17,403,904 | 17,403,904 | -0.02% |
| B2 -> B3 | 17,457,152 | 17,403,904 | 17,469,440 | 17,399,808 | +0.33% |
| B3 -> B4 | 17,399,808 | 17,399,808 | 17,403,904 | 17,338,368 | +0.35% |

The worst Native/external median is 0.35% higher, and adjacent Native medians
differ by at most 0.33%. Both registered bounds pass.

## Size and distribution result

Linux link-time `--strip-all` makes each raw compiler distribution-shaped.
Reapplying GNU `strip --strip-all` leaves all four files byte-identical at
175,920 bytes. The generated compiler is 5.45% larger than the 166,824-byte
Darwin Gate 6C reference but 15.64% below the registered 208,530-byte ceiling.

The installed QBE sidecar is 714,904 bytes, or 347,552 bytes after
`strip --strip-all`. Therefore the current compiler-plus-QBE components total
890,824 bytes as installed and 523,472 bytes when both are distribution
stripped. System CC, assembler, linker, loader, and libc remain explicit
external dependencies and are not claimed as bundled bytes.

## Conclusion and deferred scope

Gate 6D proves that the current self-hosted compiler is not accidentally tied
to Darwin. One shared TypeRB implementation, QBE IL fixed point, semantic
corpus, and ordinary Go-free regeneration graph work on both Darwin arm64 and
Linux arm64. Linux Native orchestration is performance-equivalent to the
external recipe and remains stable across generated compiler generations.

Automatic host/tool discovery, a stable target CLI, cross compilation,
x86-64, static or musl artifacts, release seed trust, multi-module projects,
package/native-library integration, debugging, and production runtime breadth
remain later product-feasibility work.
