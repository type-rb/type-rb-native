# Gate 6K Explicit Configured-project Results

Gate 6K passes every registered semantic, correctness, performance, memory,
size, ownership, fixed-point, regression, and pinned Linux arm64 criterion.
The ordinary TypeRB-authored compiler now accepts an explicitly named standard
`trbconfig.jsonc`, strictly loads the bounded Go-mode project, checks its
complete production source set, selects its unique top-level `main()`, and
builds the executable without Go or the reference compiler in the Native
chain.

On the fixed 1,025-file project, configured Native check is 2.85% faster and
uses 88.92% less peak RSS than the pinned optimized-Go frontend. Native build
is 85.81% faster with 93.08% less peak RSS; the Native application runs 18.73%
faster with 67.55% less peak RSS. Its 84,856-byte stripped executable is 96.98%
smaller than the 2,809,656-byte optimized-Go executable.

The configured adapter itself remains bounded against the same candidate's
existing file-root path: check, emit, and build medians are respectively
6.41%, 11.01%, and 1.73% higher, all within the registered 15% ceiling.

## Revisions and evidence

- Gate 6J source baseline:
  `e9b00ed946919957fad82b6d2d3ffccfe8cd48d1`
- final Gate 6K compiler implementation:
  `84e2e4a6e2cff9d7fdab46ce4eec33b609a597c4`
- measured TypeRB-authored harness:
  `9d11966a92ca308d4bb84dacc59f47efbb92b6cc`
- pinned TypeRB reference compiler:
  `fa9e0503cc681bcaa691f6f11d2f1e19ca8e6453` (`0.3.49-dev`)
- Darwin QBE 1.3 SHA-256:
  `03f50f24156449e0df41ef65444add1670d017be822edf4aa99bc8566952592b`
- TypeRB-authored benchmark executable SHA-256:
  `252346b751849395829b05d46a08775aa06538613181de18050424f470132f76`

The candidate compiler closure is:

| Source | SHA-256 |
| --- | --- |
| `compiler.trb` | `536dde374815c7c01796be00d445b97591afdadd8cda1a3ca1a6dd4e80a3cdb6` |
| `storage.trb` | `d4c77fec9e5c5e8580cb0b5ee71fbd2c9c714555cbd4fd1457fcd44cc6db1f9d` |
| `path.trb` | `6347003851071b73cb8dbf38622fcc7cf3be6abf81ea253b9aad081fb057510a` |

The checked-in config SHA-256 is
`4ac3c76411dc5ed9a8786b267d734d6744301d56dd4617ba1c4799f419444806`.
The configured corpus manifest remains 600 bytes with SHA-256
`03b741487a4eb338c44cfae1ad2f4d67f88015bca9c2fb24c447530f157cf284`.
The generated scale source manifest remains 94,322 bytes with SHA-256
`db438159189ba944283d8a92a09a1176020522c67d2551065c4010c50858f16b`.

The committed [`raw.csv`](raw.csv) has 568 data rows and no nonzero status.
Each compiler, configured/file-root, and configured Native/Go check or build
series has eleven retained observations; runtime has 31. The 318-line
[`process-inventory.txt`](process-inventory.txt) has exactly four nonzero
statuses, all required negative probes proving that the two Native compilers
and two Native applications contain no Go build metadata. The optimized-Go
application's positive metadata probe succeeds.

The exact seed handoff and formal benchmark command are retained in
[`seed-provenance.txt`](seed-provenance.txt). The pinned Linux commands, ELF
identities, outputs, negative diagnostics, package inventory, and process graph
are retained in [`linux-correctness.txt`](linux-correctness.txt),
[`linux-run.sh`](linux-run.sh), [`linux-run.log`](linux-run.log),
[`linux-process.trace`](linux-process.trace),
[`linux-process-summary.txt`](linux-process-summary.txt), and
[`linux-package-inventory.txt`](linux-package-inventory.txt).

```text
5039573bee24f095e1cb05ca75e623df09c4ab3bd8e3eb7a8b6b4a41a1a245d6  raw.csv
d800917595478da7c28f2fa97a56999ddb6b55ff7c7a6c3aadaac9801323548d  process-inventory.txt
32872fade5790d0cf5a67f993e05259fc102bf0c25bfb494faca4245fc672d0d  seed-provenance.txt
4053e869e591db007978391b55ce75dae6f3c283abde7b6cd72c7d6fc7b5c4ed  linux-correctness.txt
7a0ed4de915f94157165444d75de61b46e1fec70b1d2e531376f5531259d4a1b  linux-run.sh
e3b10c33b6a196fa125354eeb9355a83770e4d72173ccfd1a84587b5c931dd69  linux-run.log
480755835730c9e2d7f8c9d252347c267a20438e34e1694aa129d8d1c53345a8  linux-process.trace
60212e702c38be23d98ed731e04f07ed10945e67b4ef407321314b2e4456c5ce  linux-process-summary.txt
1bd5e28921141a78d3d103f6c3e9f7b82625967866de868685526d67199f16d1  linux-package-inventory.txt
```

## Correctness and ownership boundary

Permanent coverage proves strict JSONC comments, strings, defaults, duplicate
and unknown fields, configuration types and versions, root-contained paths,
deterministic physical enumeration, exclusions, spaces, unreadable files,
symlink policy, direct/index precedence, complete-source checking, unique
entrypoint selection, missing imports, cycles, tool-launch suppression, atomic
publication, and intermediate cleanup.

The directory adapter is an internal, versioned compiler-runtime boundary. It
uses physical traversal without a shell or helper process, does not follow
symlinked directories, and does not become a public TypeRB API. Configuration,
module ownership, checking, entrypoint selection, and diagnostics remain
TypeRB-authored compiler logic.

Configured and file-root input emit byte-identical 124,139-byte QBE with
SHA-256
`39f61f19bcd404732848604b568f4a5db3d70990ea233aaf8e337296d5d88874`,
build byte-identical same-basename applications, and print
`module-scale-ok`. The checked-in configured corpus emits the registered QBE
and builds the registered application that prints `configured-project-ok`.

The Gate 6E representative, Gate 6I scalar Float, and Gate 6J Float Array
applications remain byte-identical with SHA-256 values
`413d97fd8a3f26e1086795b1fd5306ad5817613e7080ddba410eb8264c0a67b9`,
`a24b8bf40013e75cabb9d1b508c594388a8cecd73f68b0f3f2add9afc5a4bede`,
and `53ca1dbdb87a373ff177796a4ff358d5acf8f5163f1dfc4df73b72f41dac8e6d`.
No language syntax, reference semantics, public runtime or standard-library
API, snapshot field, Native MIR field, stable CLI, package contract, target,
or external-tool contract changed. The reference TypeRB repository remains the
semantic oracle and has no Native-specific dependency.

## Measurement method

The TypeRB-authored controller first closes and verifies the fresh Gate 6J
baseline and the Go-free Gate 6K transition/candidate chain, exact fixed
points, configured corpus, generated scale project, retained applications,
negative behavior, repeated application bytes, and cleanup. It then records
two warmups and eleven alternating observations for canonical compiler
emit/build and project check/emit/build time, followed by independent peak-RSS
series. Runtime uses three warmups and 31 alternating observations.
Correctness, hashing, stripping, execution validation, and inventory occur
outside timed intervals.

The formal Darwin host was an Apple M2 Pro with 32 GiB RAM, macOS 26.6.2
(25G83), Go 1.27.0, and Apple clang 21.0.0. Native comparisons use the same
candidate, source graph, QBE, CC, output basename, alternating order, and cache
policy. Native and optimized Go build and execute the same TypeRB project.

## Configured input versus file-root input

Elapsed values are seconds and RSS values are bytes. Medians exclude both
warmups.

| Metric | File-root Native | Configured Native | Configured change |
| --- | ---: | ---: | ---: |
| check time median | 0.058722 s | 0.062485 s | +6.41% |
| check time min/max | 0.054613 / 0.061374 s | 0.059583 / 0.071306 s | — |
| check peak RSS median | 5,619,712 B | 6,275,072 B | +11.66% |
| check RSS min/max | 5,603,328 / 5,668,864 B | 6,225,920 / 6,307,840 B | — |
| `emit-qbe` time median | 0.069623 s | 0.077287 s | +11.01% |
| `emit-qbe` time min/max | 0.062864 / 0.081602 s | 0.069357 / 0.120805 s | — |
| `emit-qbe` peak RSS median | 8,290,304 B | 8,929,280 B | +7.71% |
| `emit-qbe` RSS min/max | 8,290,304 / 8,372,224 B | 8,896,512 / 8,978,432 B | — |
| build time median | 0.277383 s | 0.282170 s | +1.73% |
| build time min/max | 0.270259 / 0.289178 s | 0.270227 / 0.303141 s | — |
| build peak RSS median | 36,421,632 B | 36,405,248 B | -0.04% |
| build RSS min/max | 36,159,488 / 36,847,616 B | 35,831,808 / 36,732,928 B | — |

Every registered configured-input ceiling was +15%. All six time and RSS
medians pass. `emit-qbe` time is the closest result and retains 3.99 percentage
points of headroom.

## Native versus optimized Go

| Metric | Native | Optimized Go | Native change |
| --- | ---: | ---: | ---: |
| configured check time median | 0.065073 s | 0.066985 s | -2.85% |
| check time min/max | 0.060182 / 0.067970 s | 0.060283 / 0.072504 s | — |
| configured check peak RSS median | 6,275,072 B | 56,623,104 B | -88.92% |
| check RSS min/max | 6,225,920 / 6,307,840 B | 54,722,560 / 57,442,304 B | — |
| configured build time median | 0.270535 s | 1.906694 s | -85.81% |
| build time min/max | 0.239638 / 0.295994 s | 1.860658 / 2.072619 s | — |
| configured build peak RSS median | 36,208,640 B | 522,928,128 B | -93.08% |
| build RSS min/max | 35,913,728 / 36,651,008 B | 492,339,200 / 549,044,224 B | — |
| application runtime median | 0.006300 s | 0.007752 s | -18.73% |
| runtime min/max | 0.004835 / 0.011025 s | 0.006308 / 0.011446 s | — |
| application peak RSS median | 1,409,024 B | 4,341,760 B | -67.55% |
| runtime RSS min/max | 1,409,024 / 1,409,024 B | 4,177,920 / 4,472,832 B | — |

Every registered time and RSS ceiling allowed Native to be up to 25% above
optimized Go. Native is below Go on all six medians.

| Artifact | Raw bytes | Stripped/size-optimized bytes | Native reduction |
| --- | ---: | ---: | ---: |
| Native scale application | 111,816 | 84,856 | baseline |
| Go scale application | 2,937,346 | 2,809,656 | 96.98% |

The registered size criterion required an 80% reduction. Native passes with
16.98 percentage points of headroom. The Darwin Native application SHA-256 is
`428f28c3dd3592ad45bcfeed12c44135686b44103cc244f270472f14c5676094`;
the measured optimized-Go artifact is
`b1989e836f69446de71fd1314392157d829a748f471cfae0e12ae2409c4e3bb1`.

## Canonical compiler guardrail

The configured-project result does not trade away ordinary compiler behavior.
Fresh alternating Gate 6J and Gate 6K chains produced:

| Metric | Gate 6J baseline | Gate 6K candidate | Change |
| --- | ---: | ---: | ---: |
| direct `emit-qbe` median | 0.105179 s | 0.117643 s | +11.85% |
| direct `emit-qbe` min/max | 0.101640 / 0.120073 s | 0.114971 / 0.139813 s | — |
| complete `build` median | 0.718206 s | 0.806129 s | +12.24% |
| complete `build` min/max | 0.703647 / 0.773663 s | 0.788612 / 0.856462 s | — |
| direct `emit-qbe` RSS median | 23,625,728 B | 19,857,408 B | -15.95% |
| direct RSS min/max | 23,576,576 / 23,642,112 B | 19,841,024 / 19,906,560 B | — |
| complete `build` RSS median | 36,732,928 B | 36,503,552 B | -0.62% |
| complete RSS min/max | 36,667,392 / 37,011,456 B | 36,192,256 / 36,700,160 B | — |

Every registered upper bound was +15%. All pass. The candidate strips to
233,320 bytes, 14,680 bytes below the fixed 248,000-byte cap.

The formal ordinary Darwin paths are:

```text
B1 -> Gate 6J baseline B2 -> baseline B3 -> baseline B4
B1 -> untimed file-root transition -> Gate 6K candidate B2
candidate B2 -> candidate B3 -> candidate B4
```

Within each ordinary chain, B2, B3, and B4 are byte-identical. The baseline
compiler is 264,904 raw / 216,552 stripped bytes with SHA-256
`caf3d213559382376bb87b1555e832c0efd7321c0a930ffa23e88d5bc1e55c77`.
The candidate is 259,032 raw / 233,320 stripped bytes with SHA-256
`f57975e61e80e9535d60adf41bfa68f0e4f68bc2b1be2bc47a6b7d557340fa56`.
Their fixed-point QBE SHA-256 values are respectively
`95aba97d9aa07b8eac651336648b7fe53d33e88fa4411edf3f4dad76f8aea4ee`
and `62db3c31527a670c3050051a9fa27bf142b6c5deaab81ef8234104bd467aa95a`.

Candidate compiler and Native application artifacts link only to `libSystem`
on Darwin and contain no Go metadata. CC expands the registered direct
assembler input to `cc1as` and the linker, without a C frontend. No Native
intermediate remains.

## Pinned Linux arm64 result

The unchanged Gate 6D measurement image translates the exact Darwin candidate
fixed-point QBE and closes an ordinary `linux-arm64-v0` chain. Linux B1, B2,
B3, and B4 are byte-identical at 241,832 bytes with SHA-256
`955b275e1906f498418b47eedbc8183c565283d9b58754008d8df425dc78399a`.
B4 re-emits the exact Darwin QBE.

The configured small project emits byte-identical Darwin/Linux QBE and builds
twice to the same 68,568-byte ELF with SHA-256
`24b5b7a2c532c6c17e3137dfbde232c1d5bdb0d1bb806baeeb0a819e0cae11d1`.
The file-root and configured scale paths emit byte-identical Darwin/Linux QBE;
one file-root and two configured builds produce the same 68,560-byte ELF with
SHA-256
`79c27953c1bce1c9523cf491003ca39536559c5ec81fca186943c10ccfd9e9ce`.
They print `configured-project-ok` and `module-scale-ok`.

All registered negative cases are deterministic. Compiler errors suppress
tool launch; QBE and CC failures preserve the existing output and clean their
intermediates. The repository mount was read-only, the process trace exposes
QBE, CC, assembler, collect2, and linker execution, and no intermediate
remained. Linux timing is not part of the Darwin-only performance claim.

## Conclusion and deferred scope

Gate 6K establishes that the ordinary self-hosted compiler can consume a
useful standard configured project while retaining exact file-root behavior,
fixed points, cross-target output, compiler bounds, and application
regressions. On this large module graph, the configured Native path is already
faster and substantially lighter than optimized Go while producing a much
smaller executable.

Upward config discovery, implicit current-directory input, default output
placement, packages, native dependencies, test compilation, stable CLI design,
incremental caching, automatic tool discovery, source maps, release seed
policy, broader production applications, and additional target profiles remain
separately bounded work.
