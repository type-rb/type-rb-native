# Gate 6G Self-hosted Symbol Lookup Results

Gate 6G passes every registered correctness, performance, memory, size,
application-identity, ownership, and pinned Linux arm64 criterion. The
self-hosted compiler now derives a deterministic module-qualified function
index before resolution and stops bounded lexer character membership at the
first exact match.

On the canonical compiler, direct QBE emission improves by 30.80% and the
complete build improves by 5.95%. On the exact generated 6,000-function
workload, direct QBE emission improves by 53.49%. All three changes exceed the
registered minimums without a material RSS or binary-size regression.

## Revisions and evidence

- Gate 6F baseline:
  `7cb7e85c0b5bff14157dc1a686829c010d095b70`
- final Gate 6G implementation:
  `b2dc1ac1fb24126c5bded038ccefe24d60b7fff0`
- measured TypeRB Native implementation and benchmark harness:
  `8bcc2a6e1c5ecede5f07c2dda63a4d4d82631375`
- pinned TypeRB reference compiler:
  `fa9e0503cc681bcaa691f6f11d2f1e19ca8e6453` (`0.3.49-dev`)
- Darwin QBE 1.3 SHA-256:
  `03f50f24156449e0df41ef65444add1670d017be822edf4aa99bc8566952592b`
- TypeRB-authored benchmark executable SHA-256:
  `0819584dd3406bb481f1faf1e378443317fe672a5c2d850b06a29e2dcf5b10c6`

The candidate compiler closure is:

| Source | Bytes | SHA-256 |
| --- | ---: | --- |
| `compiler.trb` | 151,457 | `ebba63420e0cee349f0abf2726686b161712ef3f8a9d5399bdea8e23d0940dc0` |
| `storage.trb` | 2,588 | `d4c77fec9e5c5e8580cb0b5ee71fbd2c9c714555cbd4fd1457fcd44cc6db1f9d` |
| `path.trb` | 1,644 | `6347003851071b73cb8dbf38622fcc7cf3be6abf81ea253b9aad081fb057510a` |

The generated 6,000-function source is 363,815 bytes with SHA-256
`c989f3957552118ff86d6b7433959b6c120ad4cccdcc27a5bc7b84796974afde`.
Both compilers emit its exact 787,266-byte QBE program with SHA-256
`05fc4203f253c341ac4bab441a3d9c06320e36ad2c40e4ef56ce0b39b4479559`.

The committed [`raw.csv`](raw.csv) has 195 data rows and no nonzero status.
The 246-line [`process-inventory.txt`](process-inventory.txt) has two nonzero
statuses, both required negative probes proving that baseline and candidate
compilers contain no Go build metadata.

```text
87ddafcb6a244e305d3f3ff54098a60167515288e9dc9d560af979bc11c3212a  raw.csv
e4c89d13aa13c5d1eda58e4e34259135c9f8f04b72595aaf300231ef62cb978b  process-inventory.txt
4a97c91fdb64f1827f597176b0174894890c4bf5aa6513ff069ddd3ab9017d1c  seed-provenance.txt
1241d3df7a3e1592d55f98012d99642a36185af420128205567b2d6c0f581943  linux-correctness.txt
1070c9d8ad606eff0342384589aea9f0b5100d2315660ac4e4821400d1bcfbbb  linux-run.sh
4e0d637b51b2febceadd4f4551324e8fb93a53ac30ba1d02b6aee82d6a31c8a9  linux-run.log
55843785bfe67320cf8a3f83fa0ace346c9e463cf4f54970e96e613ac439ae04  linux-process.trace
```

The exact out-of-chain seed handoff and benchmark invocation are retained in
[`seed-provenance.txt`](seed-provenance.txt). The fixed Linux image, complete
commands, ELF identities, and application run are retained in
[`linux-correctness.txt`](linux-correctness.txt),
[`linux-run.sh`](linux-run.sh), [`linux-run.log`](linux-run.log), and
[`linux-process.trace`](linux-process.trace).

## Correctness and ownership boundary

PR #60 introduced the source-ordered function index. PR #61 retained that
model and added the bounded character-membership early return. PR #62 added
the fixed TypeRB-authored controller. Permanent coverage proves:

- deterministic bucket sizing across its growth boundary;
- full module and String comparison after a bucket match;
- same-length collisions, duplicate names, module qualification, missing
  names, and the existing last-match behavior;
- exact character membership for successful and missing matches;
- generated 128- and 6,000-function predecessor-call chains;
- the complete valid, invalid, mutation, file-root, and build-failure corpus;
  and
- exact replacement generations and application identity on Darwin and
  Linux arm64.

The parser's source-ordered arrays remain canonical. The index is derived once
before resolution, uses demand-sized TypeRB storage, and is internal to the
compiler. No public Hash, String hash intrinsic, snapshot field, Native MIR
field, syntax, CLI, runtime, target, or external-tool boundary changed.

The formal ordinary Darwin chains are:

```text
B1 -> Gate 6F baseline B2 -> baseline B3 -> baseline B4
B1 -> Gate 6G candidate B2 -> candidate B3 -> candidate B4
```

Within each chain, B2, B3, and B4 are byte-identical. The baseline compiler is
244,696 bytes with SHA-256:

```text
2b63bd297e2e049f51c54b59299385aabf05d93ff218c701a5c6a54307358e12
```

The candidate compiler is 244,872 bytes with SHA-256:

```text
0c3c8c2d59a416aeb2165079a3e14ea83f2624aed3ea3deb750b7e47c3271cd7
```

The baseline fixed-point QBE SHA-256 is
`626bcdfb28c6517c50b86851edf76f4ab5b0d8ada7d28e73209ff10e193bae67`.
The candidate fixed-point QBE SHA-256 is
`7f67262117dfdcd8f075cb9273fe5843051a53ceddcff71bc8c633ce262fe402`.

The same registered B1 seed starts both chains. Recovery is not a child,
argument, or timed phase. Candidate compiler artifacts link only to
`libSystem` on Darwin, contain no Go metadata, and retain the direct
`fork`/`execv`/`waitpid` boundary to explicit QBE and CC paths. No Native
intermediate remains.

## Measurement method

The TypeRB-authored controller first closes and verifies both independent
B1-to-B4 chains, exact fixed points, the generated scale program, and the Gate
6E application. For each workload it records two indexed warmups and eleven
alternating baseline/candidate elapsed observations, then repeats the same
policy in a separate peak-RSS series. Correctness, hashing, stripping, and
inventory occur outside timed intervals. Medians below exclude iterations
`-2` and `-1`.

The exact formal command is retained in
[`seed-provenance.txt`](seed-provenance.txt). The Darwin host was an Apple M2
Pro with 32 GiB RAM, macOS 26.6.2 (25G83), Go 1.27.0 as an inventory-only
metadata probe, and Apple clang 21.0.0. Both candidates use the same B1, QBE,
CC, output basename, alternating order, and cache policy.

## Time results

Elapsed values are seconds. Each row summarizes eleven recorded observations
after warmup.

| Workload | Candidate | Median | Minimum | Maximum | Improvement |
| --- | --- | ---: | ---: | ---: | ---: |
| canonical `emit-qbe` | Gate 6F baseline | 0.151819 | 0.148394 | 0.154965 | baseline |
| canonical `emit-qbe` | Gate 6G candidate | 0.105062 | 0.103206 | 0.109651 | 30.80% |
| canonical full `build` | Gate 6F baseline | 0.720448 | 0.717420 | 1.067921 | baseline |
| canonical full `build` | Gate 6G candidate | 0.677568 | 0.665781 | 0.688911 | 5.95% |
| 6,000-function `emit-qbe` | Gate 6F baseline | 4.720143 | 4.708978 | 4.753498 | baseline |
| 6,000-function `emit-qbe` | Gate 6G candidate | 2.195483 | 2.185745 | 2.216060 | 53.49% |

The respective registered minimum improvements were 5%, 3%, and 25%. All
three pass. The one baseline full-build maximum is retained as observed; the
pre-registered comparison applies to the median and is not changed after
measurement.

## Peak RSS results

RSS values are bytes. Each row summarizes eleven recorded observations after
warmup.

| Workload | Candidate | Median | Minimum | Maximum | Change |
| --- | --- | ---: | ---: | ---: | ---: |
| canonical `emit-qbe` | Gate 6F baseline | 21,266,432 | 21,233,664 | 21,299,200 | baseline |
| canonical `emit-qbe` | Gate 6G candidate | 21,544,960 | 21,528,576 | 21,577,728 | +1.31% |
| canonical full `build` | Gate 6F baseline | 36,765,696 | 36,552,704 | 37,093,376 | baseline |
| canonical full `build` | Gate 6G candidate | 36,765,696 | 36,487,168 | 37,257,216 | 0.00% |
| 6,000-function `emit-qbe` | Gate 6F baseline | 169,115,648 | 169,099,264 | 169,148,416 | baseline |
| 6,000-function `emit-qbe` | Gate 6G candidate | 169,312,256 | 169,230,336 | 169,361,408 | +0.12% |

The direct and full-build caps are +5%; the scale cap is +10%. All pass with
at least 3.69, 5.00, and 9.88 percentage points of headroom respectively.

## Compiler and application identity

| Artifact | Raw bytes | Stripped bytes | Versus Gate 6F stripped |
| --- | ---: | ---: | ---: |
| Gate 6F baseline B4 | 244,696 | 199,992 | baseline |
| Gate 6G candidate B4 | 244,872 | 200,008 | +16 bytes (+0.008%) |

The candidate is 8,522 bytes, or 4.09%, below the registered 208,530-byte
absolute cap.

Candidate B4 builds the representative Gate 6E five-module application twice
to exact 53,288-byte executables. They print `file-root-ok` and retain the
registered Darwin SHA-256:

```text
413d97fd8a3f26e1086795b1fd5306ad5817613e7080ddba410eb8264c0a67b9
```

## Pinned Linux arm64 result

The unchanged Gate 6D image translated the exact Darwin candidate fixed-point
QBE and closed an ordinary `linux-arm64-v0` compiler chain. Linux B1, B2, B3,
and B4 are byte-identical at 182,384 bytes with SHA-256:

```text
57c7859fb3b276117f6eccd081f19ac93f2256f6964f7c01dc3c617ef039a87a
```

B4 emits the exact Darwin candidate QBE and builds the five-module application
twice to identical 68,568-byte ELF executables. The application prints
`file-root-ok` and retains SHA-256
`6f27705eca2c8666951503b082dc1d05600808d81ecab66b2ac4419ac3ea7073`.
The repository mount was read-only, the process trace exposes QBE, CC,
assembler, collect2, and linker execution, and no intermediate remained.
Linux timing is not part of the Darwin-only registered performance claim.

## Conclusion and deferred scope

Gate 6G establishes that deterministic compiler-internal indexing can recover
substantial self-hosted frontend headroom without changing the language,
public runtime, snapshots, Native MIR, generated application, or external-tool
model. The improvement remains meaningful in the complete build even though
QBE and linking are unchanged.

Public Hash semantics, a stronger String hash, configured projects, packages,
incremental builds, tool discovery, source maps, release seed policy, and
further compiler decomposition remain separately bounded work.
