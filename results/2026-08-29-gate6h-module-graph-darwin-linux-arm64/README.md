# Gate 6H Scalable File-root Module Graph Results

Gate 6H passes every registered correctness, performance, memory, size,
optimized-Go comparison, ownership, and pinned Linux arm64 criterion. The
self-hosted compiler now scales its existing file-root path through a
deterministic internal module index, module-owned import spans, bounded
declaration scans, and unchanged private lexer character sets.

On the exact 1,025-file project, direct checking improves by 41.96%, direct
QBE emission by 39.92%, and the complete Native build by 16.16%. Scale-project
RSS is lower for check and emit and effectively flat for the complete build.
The candidate also remains inside every canonical compiler guardrail.

## Revisions and evidence

- Gate 6G baseline:
  `0796e39558f6c28995c9b4c03defded4b4bd6123`
- final Gate 6H compiler implementation:
  `0efbc695e3b88b4117a3238329a056f1fbcbf3be`
- measured implementation and TypeRB-authored harness:
  `e39f774237a6306d7cd46b09941367c42816c628`
- pinned TypeRB reference compiler:
  `fa9e0503cc681bcaa691f6f11d2f1e19ca8e6453` (`0.3.49-dev`)
- Darwin QBE 1.3 SHA-256:
  `03f50f24156449e0df41ef65444add1670d017be822edf4aa99bc8566952592b`
- TypeRB-authored benchmark executable SHA-256:
  `0e579c4e1af685051a82cdc56d8afe1cbad916b4d2dc986668a545c3d53d513e`

The candidate compiler closure is:

| Source | Bytes | SHA-256 |
| --- | ---: | --- |
| `compiler.trb` | 154,725 | `7c4df4a7876c5bc81090d520ae93bceec676166445bef07170660f54549e2396` |
| `storage.trb` | 2,588 | `d4c77fec9e5c5e8580cb0b5ee71fbd2c9c714555cbd4fd1457fcd44cc6db1f9d` |
| `path.trb` | 1,644 | `6347003851071b73cb8dbf38622fcc7cf3be6abf81ea253b9aad081fb057510a` |

The generated graph contains exactly `main.trb` plus `m0000.trb` through
`m1023.trb`. Its 94,322-byte ordered content manifest has SHA-256
`db438159189ba944283d8a92a09a1176020522c67d2551065c4010c50858f16b`.
Both compilers emit its exact 124,139-byte QBE program with SHA-256
`39f61f19bcd404732848604b568f4a5db3d70990ea233aaf8e337296d5d88874`.

The committed [`raw.csv`](raw.csv) has 374 data rows and no nonzero status.
Each of its twelve paired measurement series has exactly eleven retained
observations per candidate.
The 302-line [`process-inventory.txt`](process-inventory.txt) has three
nonzero statuses, all required negative probes proving that the two Native
compilers and Native scale application contain no Go build metadata. The Go
application's positive metadata probe is recorded separately.

The exact out-of-chain seed handoff and benchmark invocation are retained in
[`seed-provenance.txt`](seed-provenance.txt). The fixed Linux image, commands,
ELF identities, application runs, package inventory, and process graph are
retained in [`linux-correctness.txt`](linux-correctness.txt),
[`linux-run.sh`](linux-run.sh), [`linux-run.log`](linux-run.log),
[`linux-process.trace`](linux-process.trace),
[`linux-process-summary.txt`](linux-process-summary.txt), and
[`linux-package-inventory.txt`](linux-package-inventory.txt).

```text
3d442057fd5b2e8fd7e6f64d7fffa4e87b420700bdc23169a7f971feccbae7b8  raw.csv
2dcf387031151ebd3f191d6bcff147fd89f92992268f984efb66c235fe013026  process-inventory.txt
087d50522ac050643926dbd2489504945931e5faf8d7630d95b50040ac185386  seed-provenance.txt
16b83b45cbea6592ff974ff7db5fab6e57b0815ee221135e9468beab13c252ed  linux-correctness.txt
d9d3076fc8f699de2e6dd3b2ab672b319ef4134b28cc48cf0f5915a94d82d083  linux-run.sh
cb7b5232dca866954e466ef07a3dab391bef9246ae75a110e28f36b19f3dff0e  linux-run.log
2e24d5e95f2c7b8f425a9790d60ca32e03b72a0b17651c252e381424be3d9f2f  linux-process.trace
499c715f6b5db69b56f00afc8196068ed76426129a05e028aa17b71444807ca9  linux-process-summary.txt
1bd5e28921141a78d3d103f6c3e9f7b82625967866de868685526d67199f16d1  linux-package-inventory.txt
```

## Correctness and ownership boundary

PR #66 introduced the indexed file-root graph. PR #67 added the fixed
TypeRB-authored measurement controller. Permanent coverage proves:

- deterministic module-index sizing, growth, full-key collision handling,
  duplicate behavior, successful lookup, and missing lookup;
- exact zero-, one-, and multi-import ownership spans;
- unchanged private lexer classification;
- generated 64-module replacement chains in CI and the exact 1,024-imported-
  module formal project;
- direct-file precedence, index fallback, shared dependencies, unrelated
  siblings, module-local names, duplicate diagnostics, and direct/deep cycles;
- the complete valid, invalid, mutation, build-failure, file-root, Darwin, and
  Linux-profile corpus; and
- exact replacement generations, QBE, representative application identity,
  scale application behavior, and intermediate cleanup.

Source-ordered module, import, and declaration arrays remain canonical. The
module index and spans are derived TypeRB-owned compiler internals. No public
Hash or String API, compiler-only runtime adapter, snapshot field, Native MIR
field, syntax, CLI, configured-project, package, target, or external-tool
boundary changed.

The formal ordinary Darwin chains are:

```text
B1 -> Gate 6G baseline B2 -> baseline B3 -> baseline B4
B1 -> Gate 6H candidate B2 -> candidate B3 -> candidate B4
```

Within each chain, B2, B3, and B4 are byte-identical. The baseline compiler is
244,872 bytes with SHA-256:

```text
0c3c8c2d59a416aeb2165079a3e14ea83f2624aed3ea3deb750b7e47c3271cd7
```

The candidate compiler is 244,968 bytes with SHA-256:

```text
b66d65c4ddb729f71afa6ab2c6bca38f6be65eda2433ebb160058d15377891b2
```

The baseline fixed-point QBE SHA-256 is
`7f67262117dfdcd8f075cb9273fe5843051a53ceddcff71bc8c633ce262fe402`.
The candidate fixed-point QBE SHA-256 is
`cc3b7322158dd9cb369368c0d3008b531b2cec16e007e0c46089389023dd8753`.

The same registered Gate 6G B4 starts both chains. Recovery is not a child,
argument, or timed phase. Candidate compiler artifacts link only to
`libSystem` on Darwin, contain no Go metadata, and retain the direct
`fork`/`execv`/`waitpid` boundary to explicit QBE and CC paths. No Native
intermediate remains.

## Measurement method

The TypeRB-authored controller first closes and verifies both independent
B1-to-B4 chains, exact fixed points, the 1,025-file project, byte-identical
scale QBE, repeated Native application bytes, the representative Gate 6E
application, and optimized-Go behavior. For each workload it records two
indexed warmups and eleven alternating observations, then repeats that policy
in a separate peak-RSS series. Correctness, execution, hashing, stripping, and
inventory occur outside timed intervals. Medians below exclude iterations
`-2` and `-1`.

The exact formal command is retained in
[`seed-provenance.txt`](seed-provenance.txt). The Darwin host was an Apple M2
Pro with 32 GiB RAM, macOS 26.6.2 (25G83), Go 1.27.0, and Apple clang 21.0.0.
Both Native candidates use the same B1, QBE, CC, output basename, alternating
order, and cache policy. The optimized-Go series uses the pinned reference
`trb build --compile` on the exact same generated TypeRB project and inherited
cache policy.

## Scale-project time results

Elapsed values are seconds. Each row summarizes eleven recorded observations
after warmup.

| Operation | Candidate | Median | Minimum | Maximum | Improvement |
| --- | --- | ---: | ---: | ---: | ---: |
| `check` | Gate 6G baseline | 0.106010 | 0.100445 | 0.119093 | baseline |
| `check` | Gate 6H candidate | 0.061530 | 0.056613 | 0.068557 | 41.96% |
| `emit-qbe` | Gate 6G baseline | 0.127945 | 0.125421 | 0.138584 | baseline |
| `emit-qbe` | Gate 6H candidate | 0.076873 | 0.070999 | 0.111001 | 39.92% |
| complete Native `build` | Gate 6G baseline | 0.363621 | 0.338236 | 0.383587 | baseline |
| complete Native `build` | Gate 6H candidate | 0.304852 | 0.283622 | 0.331990 | 16.16% |

The registered minimum improvements were 35%, 25%, and 10%. All pass with
6.96, 14.92, and 6.16 percentage points of headroom respectively.

## Scale-project peak RSS results

RSS values are bytes. Each row summarizes eleven recorded observations after
warmup.

| Operation | Candidate | Median | Minimum | Maximum | Change |
| --- | --- | ---: | ---: | ---: | ---: |
| `check` | Gate 6G baseline | 12,533,760 | 12,484,608 | 12,550,144 | baseline |
| `check` | Gate 6H candidate | 6,455,296 | 6,422,528 | 6,488,064 | -48.50% |
| `emit-qbe` | Gate 6G baseline | 15,138,816 | 15,089,664 | 15,171,584 | baseline |
| `emit-qbe` | Gate 6H candidate | 9,076,736 | 9,043,968 | 9,109,504 | -40.04% |
| complete Native `build` | Gate 6G baseline | 36,405,248 | 36,159,488 | 36,683,776 | baseline |
| complete Native `build` | Gate 6H candidate | 36,339,712 | 36,175,872 | 36,601,856 | -0.18% |

The registered cap was +10% for every operation. All three pass without an RSS
increase at the median.

## Canonical compiler guardrail

Gate 6H does not use the scale workload to hide a normal compiler regression.
The candidate is compared directly with the registered Gate 6G Darwin medians:

| Operation | Gate 6G registered | Gate 6H candidate | Change |
| --- | ---: | ---: | ---: |
| direct `emit-qbe` time | 0.105062 s | 0.101733 s | -3.17% |
| complete `build` time | 0.677568 s | 0.680946 s | +0.50% |
| direct `emit-qbe` RSS | 21,544,960 B | 21,839,872 B | +1.37% |
| complete `build` RSS | 36,765,696 B | 36,831,232 B | +0.18% |

Every registered upper bound was +5%. All pass. The raw file also retains the
alternating Gate 6G baseline series collected during the same run.

## Native versus optimized Go

This comparison compiles the same generated TypeRB project and verifies the
same `module-scale-ok` output. It does not substitute a handwritten Go
workload.

| Metric | Native candidate | Optimized Go | Native change |
| --- | ---: | ---: | ---: |
| build time median | 0.290969 s | 2.047228 s | -85.79% |
| build time min/max | 0.260407 / 0.317801 s | 1.951901 / 2.109200 s | — |
| peak RSS median | 36,323,328 B | 513,490,944 B | -92.93% |
| peak RSS min/max | 35,995,648 / 36,782,080 B | 498,597,888 / 528,302,080 B | — |
| raw application | 111,816 B | 2,953,858 B | -96.21% |
| stripped application | 84,856 B | 2,826,168 B | -97.00% |

The registered build-time and RSS ceiling allowed Native to be up to 25%
above optimized Go; Native is substantially below both comparators. The size
criterion required at least an 80% reduction; the measured reduction is
97.00%.

The Darwin Native scale application SHA-256 is:

```text
428f28c3dd3592ad45bcfeed12c44135686b44103cc244f270472f14c5676094
```

The formal optimized-Go application SHA-256 is:

```text
c74acb5d21589fdbe0abc01e74ffe8355220502b4dd787d9986b3bcf44479c86
```

## Compiler and representative application identity

| Artifact | Raw bytes | Stripped bytes | Versus Gate 6G stripped |
| --- | ---: | ---: | ---: |
| Gate 6G baseline B4 | 244,872 | 200,008 | baseline |
| Gate 6H candidate B4 | 244,968 | 200,008 | 0 bytes |

The candidate is 8,522 bytes, or 4.09%, below the registered 208,530-byte
absolute cap.

Candidate B4 builds the representative Gate 6E five-module application twice
to exact 53,288-byte executables. They print `file-root-ok` and retain the
registered Darwin SHA-256:

```text
413d97fd8a3f26e1086795b1fd5306ad5817613e7080ddba410eb8264c0a67b9
```

## Pinned Linux arm64 result

The unchanged Gate 6D image independently regenerates all 1,025 source files
and rejects them unless their ordered manifest matches the Darwin SHA-256. It
then translates the exact Darwin candidate fixed-point QBE and closes an
ordinary `linux-arm64-v0` compiler chain. Linux B1, B2, B3, and B4 are
byte-identical at 182,416 bytes with SHA-256:

```text
dc60465abc2157088ade9b7749ef57c12071adaa15f2c9c21811b8c6d310b8cb
```

B4 emits the exact Darwin candidate QBE and retains the representative
68,568-byte application SHA-256
`6f27705eca2c8666951503b082dc1d05600808d81ecab66b2ac4419ac3ea7073`.
It also emits the exact Darwin scale QBE and builds two identical 68,560-byte
scale applications that print `module-scale-ok`, with SHA-256:

```text
79c27953c1bce1c9523cf491003ca39536559c5ec81fca186943c10ccfd9e9ce
```

The repository mount was read-only, the process trace exposes QBE, CC,
assembler, collect2, and linker execution, and no intermediate remained.
Linux timing is not part of the Darwin-only registered performance claim.

## Conclusion and deferred scope

Gate 6H establishes that the existing self-hosted file-root compiler can scale
past a thousand modules while becoming materially faster and lighter, without
changing language behavior, public runtime, Native MIR, snapshots, external
tools, or the ordinary Go-free compiler chain. It also shows that this
self-hosted Native build is already comfortably ahead of the pinned current
Go-backed build for the same TypeRB project on the registered host.

Configured projects, packages, namespace imports, public Hash and module
identity, incremental caching, stable CLI and diagnostics, tool discovery,
source maps, release seed policy, broader applications, and further compiler
decomposition remain separately bounded work.
