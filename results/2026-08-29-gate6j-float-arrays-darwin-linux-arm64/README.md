# Gate 6J Self-hosted Float Array Results

Gate 6J passes every registered semantic, correctness, performance, memory,
size, ownership, fixed-point, and pinned Linux arm64 criterion. The ordinary
TypeRB-authored compiler and runtime now accept and execute the reference
language's `Array<Float>` path without a Native-only dialect, a widened
snapshot, or a Go dependency in the compiler and generated Native
applications.

On the fixed five-million-element TypeRB workload, Native builds 42.00% faster
and with 48.25% less peak RSS than the pinned optimized-Go backend. The Native
program runs 18.02% slower but uses 58.18% less peak RSS, remaining inside the
registered 25% runtime ceiling. Its 50,824-byte stripped executable is 96.80%
smaller than the 1,587,730-byte size-optimized Go executable.

## Revisions and evidence

- Gate 6I source baseline:
  `5ff3da39c8c41a30596bbeed3b6fcffc207a43ed`
- final Gate 6J compiler implementation:
  `914f4f592f344111b7a790aac00aecbf0d411d11`
- measured TypeRB-authored harness:
  `328f93ea348fe569c56d7737206246c7df42eb9c`
- pinned TypeRB reference compiler:
  `fa9e0503cc681bcaa691f6f11d2f1e19ca8e6453` (`0.3.49-dev`)
- Darwin QBE 1.3 SHA-256:
  `03f50f24156449e0df41ef65444add1670d017be822edf4aa99bc8566952592b`
- TypeRB-authored benchmark executable SHA-256:
  `30d453abdb8873d5a69f63d00f8b6804f225e4bb5140e19fec88005c0b700850`

The candidate compiler closure is:

| Source | SHA-256 |
| --- | --- |
| `compiler.trb` | `9a90b1ca0a3fd77e2215fb744f288c5d006e08a56be81b6be6124c795a013a81` |
| `storage.trb` | `d4c77fec9e5c5e8580cb0b5ee71fbd2c9c714555cbd4fd1457fcd44cc6db1f9d` |
| `path.trb` | `6347003851071b73cb8dbf38622fcc7cf3be6abf81ea253b9aad081fb057510a` |

The permanent Float Array conformance source has SHA-256
`8ffca0e572a577778145e414eb5f24b0b3838b0954a7c3833602e943e2997304`.
The fixed workload retains its registered SHA-256
`ed874d688f0faf8cdcc56e8a6992bd25be1826bc909093cdd485699dbd3b75cf`.

The committed [`raw.csv`](raw.csv) has 342 data rows and no nonzero status.
Each compiler and application-build series has eleven retained observations
per candidate; each runtime series has 31. The 323-line
[`process-inventory.txt`](process-inventory.txt) has exactly three nonzero
statuses, all required negative probes proving that both Native compilers and
the Native Float Array application contain no Go build metadata. The
optimized-Go application's positive metadata probe succeeds.

The exact seed handoff and formal benchmark command are retained in
[`seed-provenance.txt`](seed-provenance.txt). The pinned Linux commands, ELF
identities, outputs, bounds failure, invalid diagnostics, package inventory,
and process graph are retained in
[`linux-correctness.txt`](linux-correctness.txt),
[`linux-run.sh`](linux-run.sh), [`linux-run.log`](linux-run.log),
[`linux-process.trace`](linux-process.trace),
[`linux-process-summary.txt`](linux-process-summary.txt), and
[`linux-package-inventory.txt`](linux-package-inventory.txt).

```text
1f3f19b74e14e69f39a6119fc530574a6af839875b991e82e44a51786c2bc972  raw.csv
4c571654a1ca9383ed0ec989d577e9e4fb67969c343b90ed341d831b4066ce67  process-inventory.txt
ea98ca75105e32bc08794311cfad12bc7af3a163250f3f6776efc3ed442191b6  seed-provenance.txt
a93dbd6f99a9594bbc5686736fe67781be79bd4a49ce930598f4643df41b2e42  linux-correctness.txt
8ea020966d4ed703a8d7bfb5edfd021dc55ae1288227e99a30eb4a3504f60029  linux-run.sh
7bb48d51fadd64d5b034c2888d70f811e308e4920657b262a13b29fe7c35a09d  linux-run.log
21ad7cd0d4de522dd5bad114330f09daeeb9218ea7b2a8a0ca13f73f043ae925  linux-process.trace
99c0ef90ee5e605f8dbf6f2199e64a68ff40ef5e7173e828c1a2d6c33782c40d  linux-process-summary.txt
1bd5e28921141a78d3d103f6c3e9f7b82625967866de868685526d67199f16d1  linux-package-inventory.txt
```

## Correctness and ownership boundary

Permanent coverage proves contextual and inferred Float Arrays, mixed numeric
literal inference, safe Integer element widening at construction and every
typed boundary, parameters and results, records, aliases, growth, `size`,
positive and negative indexing, mutation, compound arithmetic, and bounded
nested Arrays. It also proves deterministic rejection of incompatible
elements, invariant Array widening, immutable mutation, unsupported methods,
and the exact runtime bounds failure.

QBE output keeps direct Float cells in `d` parameters, `loadd`, and `stored`
operations behind a dedicated push path. Outer nested Array cells remain `l`
references, and Integer-to-Float widening uses `sltof` before a value enters a
binary64 cell. The full existing valid, invalid, mutation, build-failure,
file-root, Darwin, and Linux-profile corpus continues to pass. The Gate 6E
representative and Gate 6I scalar Float applications remain byte-identical.

No syntax, reference semantics, public runtime or standard-library API,
compiler-only runtime adapter, snapshot field, Native MIR field, CLI,
configured-project, package, target, or external-tool contract changed. The
reference TypeRB implementation remains the semantic oracle.

## Measurement method

The TypeRB-authored controller first closes and verifies two independent
ordinary chains, their exact fixed points, direct binary64 Array QBE,
conformance and workload behavior, repeated application bytes, and exact Gate
6E and Gate 6I regression applications. It then records two warmups and eleven
alternating observations for compiler emit/build and Float Array application
build time and peak RSS. Runtime uses three warmups and 31 alternating
observations. Correctness, execution validation, hashing, stripping, and
inventory occur outside timed intervals.

The formal Darwin host was an Apple M2 Pro with 32 GiB RAM, macOS 26.6.2
(25G83), Go 1.27.0, and Apple clang 21.0.0. Both Native candidates use the same
registered Gate 6I B1, QBE, CC, output basename, alternating order, and cache
policy. Native and optimized Go build and execute the exact same checked-in
TypeRB source.

## Native versus optimized Go

Elapsed values are seconds and RSS values are bytes. Medians exclude all
registered warmups.

| Metric | Native | Optimized Go | Native change |
| --- | ---: | ---: | ---: |
| build time median | 0.111052 s | 0.191468 s | -42.00% |
| build time min/max | 0.095904 / 0.124152 s | 0.173227 / 0.327765 s | — |
| build peak RSS median | 35,815,424 B | 69,206,016 B | -48.25% |
| build RSS min/max | 35,569,664 / 36,208,640 B | 68,468,736 / 70,402,048 B | — |
| runtime median | 0.051562 s | 0.043691 s | +18.02% |
| runtime min/max | 0.050074 / 0.057077 s | 0.040710 / 0.052607 s | — |
| runtime peak RSS median | 43,597,824 B | 104,251,392 B | -58.18% |
| runtime RSS min/max | 43,581,440 / 43,630,592 B | 81,428,480 / 109,035,520 B | — |

Every registered time and RSS ceiling allowed Native to be up to 25% above
optimized Go. All pass; runtime is the only median above Go and retains 6.98
percentage points of headroom.

| Artifact | Raw bytes | Stripped/size-optimized bytes | Native reduction |
| --- | ---: | ---: | ---: |
| Native Float Array workload | 53,160 | 50,824 | baseline |
| Go Float Array workload | — | 1,587,730 | 96.80% |

The registered size criterion required an 80% reduction. Native passes with
16.80 percentage points of headroom. The Darwin Native application SHA-256 is
`53ca1dbdb87a373ff177796a4ff358d5acf8f5163f1dfc4df73b72f41dac8e6d`;
the measured optimized-Go artifact is
`2d6d71ee7356b8e7dc8940f589dd464f46a5f9eef11daa4606e28aef0142f64f`.

## Canonical compiler guardrail

The Float Array result does not trade away ordinary compiler behavior. Fresh
alternating Gate 6I and Gate 6J chains produced:

| Metric | Gate 6I baseline | Gate 6J candidate | Change |
| --- | ---: | ---: | ---: |
| direct `emit-qbe` median | 0.111834 s | 0.113444 s | +1.44% |
| direct `emit-qbe` min/max | 0.108562 / 0.121756 s | 0.111164 / 0.134113 s | — |
| complete `build` median | 0.745122 s | 0.754470 s | +1.25% |
| complete `build` min/max | 0.724021 / 0.909479 s | 0.733002 / 0.854080 s | — |
| direct `emit-qbe` RSS median | 23,199,744 B | 23,609,344 B | +1.77% |
| direct RSS min/max | 23,183,360 / 23,232,512 B | 23,592,960 / 23,691,264 B | — |
| complete `build` RSS median | 36,831,232 B | 36,782,080 B | -0.13% |
| complete RSS min/max | 36,405,248 / 37,044,224 B | 36,585,472 / 37,076,992 B | — |

Every registered upper bound was +10%. All pass. The candidate strips to
216,552 bytes, 7,448 bytes below the fixed 224,000-byte absolute cap.

The formal ordinary Darwin chains are:

```text
B1 -> Gate 6I baseline B2 -> baseline B3 -> baseline B4
B1 -> Gate 6J candidate B2 -> candidate B3 -> candidate B4
```

Within each chain, B2, B3, and B4 are byte-identical. The baseline compiler is
264,264 raw / 216,552 stripped bytes with SHA-256
`849f5d6c6fc0738735c84b9240e8f87a477e8d978b0c64a995a5cae5944d8f8d`.
The candidate is 264,904 raw / 216,552 stripped bytes with SHA-256
`caf3d213559382376bb87b1555e832c0efd7321c0a930ffa23e88d5bc1e55c77`.
Their fixed-point QBE SHA-256 values are respectively
`da3ba99a19f023c8d227a58e77d748ce77e64bfc650d0963aefb3f1512d4217e`
and `95aba97d9aa07b8eac651336648b7fe53d33e88fa4411edf3f4dad76f8aea4ee`.

Candidate B4 rebuilds the representative and scalar Float applications to
their exact registered SHA-256 values
`413d97fd8a3f26e1086795b1fd5306ad5817613e7080ddba410eb8264c0a67b9`
and `a24b8bf40013e75cabb9d1b508c594388a8cecd73f68b0f3f2add9afc5a4bede`.
Candidate compiler and Native application artifacts link only to `libSystem`
on Darwin and contain no Go metadata. No Native intermediate remains.

## Pinned Linux arm64 result

The unchanged Gate 6D measurement image translates the exact Darwin candidate
fixed-point QBE and closes an ordinary `linux-arm64-v0` chain. Linux B1, B2,
B3, and B4 are byte-identical at 250,152 bytes with SHA-256
`ae521ea4c1a2cc70585c141b69affe340bd07d5e6631f54f85b25dd7ab2de491`.
B4 re-emits the exact Darwin QBE.

The Gate 6I scalar and both Gate 6J Float Array programs emit byte-identical
QBE on Darwin and Linux. The scalar workload retains its exact 68,632-byte
Linux executable and SHA-256. The Float Array conformance and workload QBE
SHA-256 values are respectively
`b8c37290d477049248e861d590b4c1af281fdb75b6ba24b67aae41aa8f367266`
and `a994fecd55f47b5249955a919ad435de0c250b0a642514a726b445cb9b0d93da`.
Repeated ELF builds are byte-identical and print `float-arrays-ok` and
`float-array-ok`. The representative application retains its registered
68,568-byte Linux identity.

The bounds executable exits 2 with exact panic text and no stdout. All nine
registered invalid cases return exact diagnostics and status 1. The repository
mount was read-only, the process trace exposes QBE, CC, assembler, collect2,
and linker execution, and no intermediate remained. Linux timing is not part
of the Darwin-only registered performance claim.

## Conclusion and deferred scope

Gate 6J establishes that the self-hosted compiler and managed runtime can carry
a useful `Array<Float>` path while remaining within every Go-parity and
compiler-regression bound. Native is materially better for build time, memory,
and executable size. Its measured Float Array runtime is competitive but not
faster than optimized Go, so continued runtime optimization remains useful
without blocking broader language and project coverage.

Float formatting and predicates, explicit Float-to-Integer conversion,
exponentiation, math packages, configured projects, public CLI design,
incremental caching, tool discovery, source maps, release seed policy, broader
applications, and additional target profiles remain separately bounded work.
