# Gate 6E File-root Multi-module Results

Gate 6E passes its registered file-root closure, correctness, self-hosting,
Darwin performance, memory, executable-size, compiler-size, ownership, and
pinned Linux arm64 criteria. The ordinary TypeRB-authored compiler loads only
the selected entry and its transitive named project imports, then checks and
builds the complete closure without Go.

The representative application spans five reachable modules, one unreachable
invalid sibling, records, direct calls, loops, Arrays, Strings, a diamond, and
directory-index fallback. Native and optimized Go print the same
`file-root-ok` result. The equivalent flattened Native source produces an
executable with the same stripped size.

This remains an internal compiler slice. It does not promote the experimental
commands or module rules to a public TypeRB interface.

## Revisions and evidence

- TypeRB Native implementation and harness:
  `b2b4740f39571dc35af9199dae817d94912b7a47`
- pinned TypeRB reference compiler:
  `fa9e0503cc681bcaa691f6f11d2f1e19ca8e6453` (`0.3.49-dev`)
- checked-in compiler source: 153,301 bytes, SHA-256
  `2bca01ee448ca3f8177fd98b80b0f7e48d6c0459374e7ec7213fccd30c327d46`
- Darwin QBE 1.3 SHA-256:
  `03f50f24156449e0df41ef65444add1670d017be822edf4aa99bc8566952592b`
- TypeRB-authored benchmark executable SHA-256:
  `bcd53a3f02ed8d2138ab725d4404f90b55729fc05a6754d64ddce9b8d8aeab02`

The committed [`raw.csv`](raw.csv) contains 193 measurement rows and no
nonzero status. The 207-line
[`process-inventory.txt`](process-inventory.txt) has one nonzero command status:
the required negative probe proving that the Native application has no Go
build metadata. Their SHA-256 values are:

```text
3e93cb999cfe168c5f9818182c774e8b2ae57a6043a64dc3aead9db33eb56d12  raw.csv
e1bfea76b393f3a3a982386bf8cda4b4f1dfa94b1901f1cc3cacbd4b29999712  process-inventory.txt
```

The exact Go-backed B0/B1 recovery commands and hashes are separate in
[`seed-provenance.txt`](seed-provenance.txt). The fixed Linux image, target
seed, B1-to-B4 chain, ELF identity, and application run are retained in
[`linux-correctness.txt`](linux-correctness.txt).

```text
68a2fdd05cab0e72f7be330efb32b1a60ce733005642e9384b13e47d997604a1  seed-provenance.txt
e241a2cf732dda8c1e354db4f000c4019bbbe3221c57cf04f1944e97c4ad949f  linux-correctness.txt
```

## Correctness and ownership boundary

PR #53 passed the full configured CI path: 74 general tests and 13 compiler
tests, including the complete earlier valid, mutation, invalid, build-failure,
Darwin, and Linux-profile corpus. Gate 6E coverage additionally requires:

- reachable-only file loading and an unrelated malformed sibling;
- direct-file/index precedence, optional suffixes, diamonds, cycles, and paths
  containing spaces;
- module-local identity, imported records and functions, duplicate and unused
  bindings, entry-owned `main`, and every registered loader failure;
- failures before QBE or CC, exact diagnostics, atomic output publication,
  and complete intermediate cleanup;
- repeated byte-identical Native application builds and optimized Go behavior;
  and
- an actual B1-to-B2-to-B3-to-B4 ordinary compiler chain.

The formal Darwin chain produced byte-identical B2, B3, and B4 compilers with
SHA-256:

```text
7579c11e50e14edda6df5968a7d6df54c4523fcaf1c1028e0436f38694aa501b
```

The benchmark accepts one previously prepared B1 seed. Recovery is not a
child, argument, or timed phase in the ordinary chain. Each generated compiler
is the executable seed of the next build. Ordinary Native builds invoke the
explicit QBE and CC paths directly; the B4 undefined process symbols retain
the `fork`/`execv`/`waitpid` boundary, with no shell launcher. Native artifacts
link only to `libSystem` on Darwin and contain no Go build metadata.

The pinned Linux arm64 correctness run went further than the minimum one-app
probe: Linux B1, B2, B3, and B4 are all byte-identical, B4 built the same
five-module graph, and the ELF application printed `file-root-ok`. No Native
intermediate remained. Linux measurements were not added to the Darwin-only
registered performance claim.

## Measurement method

The TypeRB-authored controller first constructs and verifies canonical Native,
optimized Go, and flattened Native applications and the exact B1-to-B4
compiler chain. It then records:

- two indexed warmups and seven alternating end-to-end application builds;
- a separate two-warmup, seven-observation build peak-RSS series;
- two runtime warmups and 50 alternating runtime observations;
- a separate two-warmup, seven-observation runtime peak-RSS series; and
- two warmups and seven B1-to-B2 compiler time and peak-RSS observations.

Every application build starts the selected compiler, parses and checks the
same source graph, emits QBE, invokes QBE and CC, atomically publishes the
executable, and cleans intermediates. Correctness checks, hashing, stripping,
and inventory occur outside timed intervals. Medians below exclude iterations
`-2` and `-1`.

The exact formal command was:

```text
/tmp/type-rb-native-gate6e-final.QQfCBI/tools/benchmark-b2b4740 \
  /Users/fujita-h/trb/worktrees/type-rb-native-gate6e-result \
  /tmp/type-rb-native-gate6e-final.QQfCBI/recovery/b1 \
  go-backed-recovery-reference-fa9e050-native-driver-b2b4740-b0-to-b1 \
  /tmp/type-rb-native-gate6e-final.QQfCBI/tools/benchmark-b2b4740 \
  /tmp/type-rb-native-gate5-tools/trb-fa9e050 \
  /tmp/qbe-1.3/qbe \
  /usr/bin/cc \
  /opt/homebrew/bin/go \
  /tmp/type-rb-native-gate6e-final.QQfCBI/darwin/workspace \
  /tmp/type-rb-native-gate6e-final.QQfCBI/darwin/raw.csv \
  /tmp/type-rb-native-gate6e-final.QQfCBI/darwin/process-inventory.txt
```

The Darwin host was an Apple M2 Pro with 32 GiB RAM, macOS 26.6.2 (25G83),
Go 1.27.0, and Apple clang 21.0.0.

## Application build results

Elapsed values are seconds; RSS values are bytes. Each row summarizes seven
recorded observations after warmup.

| Candidate | Median time | Minimum | Maximum | Versus Go median |
| --- | ---: | ---: | ---: | ---: |
| Native file-root | 0.117782 | 0.096977 | 0.123796 | -44.89% |
| optimized Go | 0.213718 | 0.207297 | 0.227387 | baseline |

| Candidate | Median RSS | Minimum | Maximum | Versus Go median |
| --- | ---: | ---: | ---: | ---: |
| Native file-root | 35,897,344 | 35,586,048 | 36,208,640 | -48.22% |
| optimized Go | 69,320,704 | 68,255,744 | 71,352,320 | baseline |

Both Native build medians improve on optimized Go and therefore pass the 25%
non-inferiority limits with substantial margin.

## Application runtime results

Elapsed time summarizes 50 recorded observations. Peak RSS summarizes seven.

| Candidate | Median time | Minimum | Maximum | Versus Go median |
| --- | ---: | ---: | ---: | ---: |
| Native file-root | 0.021596 | 0.017253 | 0.031822 | +13.70% |
| optimized Go | 0.018994 | 0.014525 | 0.025878 | baseline |

| Candidate | Median RSS | Minimum | Maximum | Versus Go median |
| --- | ---: | ---: | ---: | ---: |
| Native file-root | 1,409,024 | 1,409,024 | 1,409,024 | -65.32% |
| optimized Go | 4,063,232 | 3,915,776 | 4,128,768 | baseline |

Native runtime is 13.70% slower than optimized Go, inside the registered 25%
bound and far below the 2x diagnostic threshold. Native runtime RSS is 65.32%
lower.

## Compiler regeneration results

| Metric | Native B1 -> B2 median | Gate 6C baseline | Difference |
| --- | ---: | ---: | ---: |
| elapsed time | 0.725117 s | 0.585709 s | +23.80% |
| peak RSS | 36,683,776 bytes | 36,667,392 bytes | +0.04% |

The compiler-time result is the narrowest passing comparison. Its registered
25% ceiling is 0.732136 seconds; all seven observations, including the
0.730293-second maximum, remain below that value. The median RSS is effectively
flat and far below its 45,834,240-byte ceiling.

## Executable sizes

| Artifact | Raw bytes | Stripped bytes |
| --- | ---: | ---: |
| Native file-root application | 53,288 | 50,824 |
| flattened Native application | 53,288 | 50,824 |
| optimized Go application | 2,429,810 | 2,330,792 |
| Native B4 compiler | 244,728 | 199,992 |

The Native file-root application is 97.82% smaller than optimized Go, exceeding
the required 80% reduction, and has zero size overhead relative to the
flattened Native application. The fixed-point compiler is 4.09% below its
208,530-byte ceiling.

## Conclusion and deferred scope

Gate 6E establishes that representative multi-file program loading need not
sacrifice the existing self-hosted compiler closure, compact output, or
competitive end-to-end behavior. The Native path is much smaller, uses less
memory, builds faster, and runs within the registered non-inferiority band.
The compiler remains exact across replacement generations on both Darwin and
the pinned Linux arm64 environment.

Configured projects, namespace imports, external packages, stable module
identity, incremental caching, automatic tool discovery, production runtime
integration, source maps, and public CLI design remain deferred. Those require
new bounded slices; this result does not silently promote them.
