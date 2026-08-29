# Gate 6I Self-hosted Float Scalar Results

Gate 6I passes every registered semantic, correctness, performance, memory,
size, ownership, fixed-point, and pinned Linux arm64 criterion. The ordinary
TypeRB-authored compiler now accepts and emits the reference language's scalar
binary64 Float path without a Native-only dialect or a Go dependency in the
compiler and generated Native applications.

On the fixed five-million-iteration TypeRB workload, Native builds 41.37%
faster and with 48.35% less peak RSS than the pinned optimized-Go backend. The
Native program runs 10.60% slower but uses 65.60% less peak RSS, remaining
inside the registered 25% runtime ceiling. Its 50,808-byte stripped executable
is 96.80% smaller than the 1,587,730-byte size-optimized Go executable.

## Revisions and evidence

- Gate 6H source baseline:
  `1311dfccee379dcf2dd3a70a525bc188d195981d`
- final Gate 6I compiler implementation:
  `cd2335e6472b4daca8d631b17b889a094959c2f2`
- measured TypeRB-authored harness:
  `073504790b930157b48c1bc6743bc0102f5fe014`
- pinned TypeRB reference compiler:
  `fa9e0503cc681bcaa691f6f11d2f1e19ca8e6453` (`0.3.49-dev`)
- Darwin QBE 1.3 SHA-256:
  `03f50f24156449e0df41ef65444add1670d017be822edf4aa99bc8566952592b`
- TypeRB-authored benchmark executable SHA-256:
  `e66599fefec967f1039452a005678d3fd437120d16a6a159d1bc48ac11edfd38`

The candidate compiler closure is:

| Source | SHA-256 |
| --- | --- |
| `compiler.trb` | `fb6b1719e545d4af1d80392c75ef03253b517e684b305459c64ef698445602dc` |
| `storage.trb` | `d4c77fec9e5c5e8580cb0b5ee71fbd2c9c714555cbd4fd1457fcd44cc6db1f9d` |
| `path.trb` | `6347003851071b73cb8dbf38622fcc7cf3be6abf81ea253b9aad081fb057510a` |

The permanent Float conformance source has SHA-256
`12604e39c9f626bd0e1a887b3450530d2b253eeb10cf3327578390bde7c31b47`.
The fixed workload source retains its registered SHA-256
`7d5125967da5a740faf62c0cc3a89d04bdaade54a475c2649d82892847e77dfe`.

The committed [`raw.csv`](raw.csv) has 341 data rows and no nonzero status.
Each compiler/build series has eleven retained observations per candidate;
each runtime series has 31. The 319-line
[`process-inventory.txt`](process-inventory.txt) has exactly three nonzero
statuses, all required negative probes proving that both Native compilers and
the Native Float application contain no Go build metadata. The optimized-Go
application's positive metadata probe succeeds.

The exact seed handoff and formal benchmark command are retained in
[`seed-provenance.txt`](seed-provenance.txt). The pinned Linux commands, ELF
identities, outputs, invalid diagnostics, package inventory, and process graph
are retained in [`linux-correctness.txt`](linux-correctness.txt),
[`linux-run.sh`](linux-run.sh), [`linux-run.log`](linux-run.log),
[`linux-process.trace`](linux-process.trace),
[`linux-process-summary.txt`](linux-process-summary.txt), and
[`linux-package-inventory.txt`](linux-package-inventory.txt).

```text
fd277c423203044283699ca6ece5b4924b1d15bcc16e9a809021f68387736bfb  raw.csv
c741fca84b9ee115d48b7e2ec24aea8fb1246bb1a230ea75ffeaa085ef02e18f  process-inventory.txt
67532c8ba9d6f532a10f1ff9439fa38ae09d91110f867264bf93809bee883339  seed-provenance.txt
593d80a92b4373b8057e124a76a1ed9461b8375df754349b40ee6a36c921df96  linux-correctness.txt
c9e7fd3b1f707f856f22c3a4c43cc2bc8da1d4726dbc9e1db0d95086ad58ee25  linux-run.sh
749ee86f18d412c23847c18ae7e556b3780b5bb2412b3e445894ab64e0a6a2e4  linux-run.log
d773607408b2ab83ff00aac86e07eab9787be1706100d4949f052481f2a0b2f0  linux-process.trace
9cec0b57bde90cc83084bb1decddb4e2c12a6854aca2ba7d256758442bdd5c73  linux-process-summary.txt
1bd5e28921141a78d3d103f6c3e9f7b82625967866de868685526d67199f16d1  linux-package-inventory.txt
```

## Correctness and ownership boundary

Permanent coverage proves finite decimal literals, signed underflow and
negative zero, Float storage and mutation, function and record ABI, unary and
binary arithmetic, all six comparisons, Integer-to-Float widening at typed
boundaries and in both mixed operand orders, and runtime infinity and NaN.
It also proves deterministic rejection of overflow literals, narrowing,
unsupported remainder and methods, and malformed syntax.

QBE output keeps Float values in `d` parameters, results, loads, stores,
arithmetic, and comparisons, using `sltof` only for safe widening. The checker
rejects non-finite source literals before QBE. The full existing valid,
invalid, mutation, build-failure, file-root, Darwin, and Linux-profile corpus
continues to pass, and the representative application remains byte-identical.

No syntax, reference semantics, public runtime or standard-library API,
compiler-only runtime adapter, snapshot field, Native MIR field, CLI,
configured-project, package, target, or external-tool contract changed. The
reference TypeRB implementation remains the semantic oracle.

## Measurement method

The TypeRB-authored controller first closes and verifies two independent
ordinary chains, their exact fixed points, Float QBE instruction families,
conformance and workload behavior, repeated application bytes, the existing
representative application, and optimized-Go behavior. It then records two
warmups and eleven alternating observations for compiler emit/build and Float
application build time and peak RSS. Runtime uses three warmups and 31
alternating observations. Correctness, execution validation, hashing,
stripping, and inventory occur outside timed intervals.

The formal Darwin host was an Apple M2 Pro with 32 GiB RAM, macOS 26.6.2
(25G83), Go 1.27.0, and Apple clang 21.0.0. Both Native candidates use the
same registered Gate 6H B1, QBE, CC, output basename, alternating order, and
cache policy. Native and optimized Go build and execute the exact same
checked-in TypeRB source.

## Native versus optimized Go

Elapsed values are seconds and RSS values are bytes. Medians exclude all
registered warmups.

| Metric | Native | Optimized Go | Native change |
| --- | ---: | ---: | ---: |
| build time median | 0.107871 s | 0.183994 s | -41.37% |
| build time min/max | 0.094753 / 0.145445 s | 0.173164 / 0.204167 s | — |
| build peak RSS median | 35,913,728 B | 69,533,696 B | -48.35% |
| build RSS min/max | 35,651,584 / 36,061,184 B | 68,763,648 / 70,893,568 B | — |
| runtime median | 0.069359 s | 0.062714 s | +10.60% |
| runtime min/max | 0.068281 / 0.074313 s | 0.060589 / 0.094024 s | — |
| runtime peak RSS median | 1,409,024 B | 4,096,000 B | -65.60% |
| runtime RSS min/max | 1,409,024 / 1,409,024 B | 3,899,392 / 4,227,072 B | — |

Every registered time and RSS ceiling allowed Native to be up to 25% above
optimized Go. All pass; runtime is the only median above Go and retains 14.40
percentage points of headroom.

| Artifact | Raw bytes | Stripped/size-optimized bytes | Native reduction |
| --- | ---: | ---: | ---: |
| Native Float workload | 53,080 | 50,808 | baseline |
| Go Float workload | — | 1,587,730 | 96.80% |

The registered size criterion required an 80% reduction. Native passes with
16.80 percentage points of headroom. The Darwin Native application SHA-256 is
`a24b8bf40013e75cabb9d1b508c594388a8cecd73f68b0f3f2add9afc5a4bede`;
the measured optimized-Go artifact is
`6a71f81cec787d698b4df476983daac618b447a5284fef0c83fa705c69270a86`.

## Canonical compiler guardrail

The Float result does not trade away ordinary compiler behavior. Fresh
alternating Gate 6H and Gate 6I chains produced:

| Metric | Gate 6H baseline | Gate 6I candidate | Change |
| --- | ---: | ---: | ---: |
| direct `emit-qbe` median | 0.105956 s | 0.113938 s | +7.53% |
| direct `emit-qbe` min/max | 0.101275 / 0.116244 s | 0.109350 / 0.122445 s | — |
| complete `build` median | 0.697980 s | 0.726816 s | +4.13% |
| complete `build` min/max | 0.677565 / 0.757844 s | 0.721253 / 0.757524 s | — |
| direct `emit-qbe` RSS median | 21,856,256 B | 23,216,128 B | +6.22% |
| direct RSS min/max | 21,823,488 / 21,905,408 B | 23,183,360 / 23,248,896 B | — |
| complete `build` RSS median | 36,765,696 B | 36,765,696 B | 0.00% |
| complete RSS min/max | 36,667,392 / 36,945,920 B | 36,569,088 / 36,978,688 B | — |

Every registered upper bound was +10%. All pass. The candidate strips to
216,552 bytes, 3,448 bytes below the fixed 220,000-byte absolute cap.

The formal ordinary Darwin chains are:

```text
B1 -> Gate 6H baseline B2 -> baseline B3 -> baseline B4
B1 -> Gate 6I candidate B2 -> candidate B3 -> candidate B4
```

Within each chain, B2, B3, and B4 are byte-identical. The baseline compiler is
244,968 raw / 200,008 stripped bytes with SHA-256
`b66d65c4ddb729f71afa6ab2c6bca38f6be65eda2433ebb160058d15377891b2`.
The candidate is 264,264 raw / 216,552 stripped bytes with SHA-256
`849f5d6c6fc0738735c84b9240e8f87a477e8d978b0c64a995a5cae5944d8f8d`.
Their fixed-point QBE SHA-256 values are respectively
`cc3b7322158dd9cb369368c0d3008b531b2cec16e007e0c46089389023dd8753`
and `da3ba99a19f023c8d227a58e77d748ce77e64bfc650d0963aefb3f1512d4217e`.

Candidate B4 rebuilds the representative application twice to exact
53,288-byte executables that print `file-root-ok` and retain SHA-256
`413d97fd8a3f26e1086795b1fd5306ad5817613e7080ddba410eb8264c0a67b9`.
Candidate compiler and Native application artifacts link only to `libSystem`
on Darwin and contain no Go metadata. No Native intermediate remains.

## Pinned Linux arm64 result

The unchanged Gate 6D measurement image translates the exact Darwin candidate
fixed-point QBE and closes an ordinary `linux-arm64-v0` chain. Linux B1, B2,
B3, and B4 are byte-identical at 249,944 bytes with SHA-256
`591238c939196a834a2009a1b6c7ac3c2e99567fa538feb4f2bf2525ab793cc6`.
B4 re-emits the exact Darwin QBE.

Both Float programs emit byte-identical QBE on Darwin and Linux. The
conformance QBE SHA-256 is
`5644fe251dd49027848fc191d811532b3f37c4a6a5f146beec66c5f7bb131245`;
the workload QBE SHA-256 is
`828a9c092f157402aa48d42c81bb3774b19a9945e0bfe1b88cf35fc82873a3fb`.
Repeated ELF builds are byte-identical and print `float-scalars-ok` and
`float-kernel-ok`. The representative application retains its registered
68,568-byte Linux identity.

The repository mount was read-only, all invalid diagnostics matched exactly,
the process trace exposes QBE, CC, assembler, collect2, and linker execution,
and no intermediate remained. Linux timing is not part of the Darwin-only
registered performance claim.

## Conclusion and deferred scope

Gate 6I establishes that the self-hosted compiler can carry a useful Float
scalar path while remaining within every Go-parity and compiler-regression
bound. Native is materially better for build time, memory, and executable
size; its measured Float runtime is competitive but not faster than optimized
Go, leaving runtime optimization as useful evidence rather than a prerequisite
for continuing language coverage.

Float formatting and predicates, explicit Float-to-Integer conversion,
`Array<Float>`, exponentiation, math packages, configured projects, public CLI
design, incremental caching, tool discovery, source maps, release seed policy,
broader applications, and additional target profiles remain separately
bounded work.
