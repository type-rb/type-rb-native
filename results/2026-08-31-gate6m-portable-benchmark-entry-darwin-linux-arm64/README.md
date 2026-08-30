# Gate 6M Portable Benchmark-entry Results

Gate 6M passes every registered semantic, differential, fixed-point,
compiler-regression, application-parity, memory, size, process-boundary, and
external-library criterion on Darwin arm64 and Linux arm64. The ordinary
self-hosted application path now supports the existing portable
`Process.argv()`, `String#to_i()`, `Integer#to_s()`, `Float#to_i()`, and
`Math.sqrt()` contracts without Go or the reference compiler in the Native
chain.

On the identical TypeRB workload, the Darwin Native application builds 59.23%
faster with 46.81% less peak RSS than the pinned optimized-Go backend. It runs
28.89% faster with 71.54% less peak RSS. Its stripped executable is 98.19%
smaller on Darwin; the independently verified Linux executable is 99.15%
smaller than its optimized-Go counterpart.

The candidate canonical compiler remains within the stricter registered
guardrail against the fixed pre-Gate-6M Native baseline: Darwin median build
time is 7.93% higher and peak RSS is 13.77% higher, both below the 15% ceiling.
Its Darwin and Linux compiler assets total 573,720 bytes, 7.46% below the
620,000-byte combined limit.

## Revisions and public evidence

- fixed pre-Gate-6M Native baseline:
  `71495bbf18f0820891ea086104ca7da808bfd25f`
- measured Gate 6M compiler implementation:
  `97b3ac2aa1d88cbb7782602589ad70686593ddab`
- final evidence-tooling revision:
  `c326b52d4bb2ce72602a6e33839883c94fd30f1d`
- pinned TypeRB semantic reference:
  `2cf63e95b4fc1a92f6094e2c89c47fb75262adae` (`0.4.3-dev`)
- immutable previous-Native seed:
  [`bootstrap-seed-2026-08-30`](https://github.com/type-rb/type-rb-native/releases/tag/bootstrap-seed-2026-08-30)
- QBE 1.3 source SHA-256:
  `d587905d620dc5e1d2bfa7c2cc642b9b837aa89a3188c6e37b53d756cf66e320`
- successful formal evidence:
  [Actions run 33321032161](https://github.com/type-rb/type-rb-native/actions/runs/33321032161)
- preregistered scope:
  [issue #113](https://github.com/type-rb/type-rb-native/issues/113)

The Darwin QBE executable had SHA-256
`38338135bd9d9201c83e66cb8a58abed03096af3ccfd4ecc63b907369cc28fcc`;
Linux reproduced the existing runner-specific QBE executable SHA-256
`510f15a1c724c204141d0b7531fe1641b983fe41dd008f5806470709a79a746c`.
Both were built from the exact pinned source archive and emitted the same
registered candidate compiler QBE.

## Correctness and fixed points

The successful corpus exercises real process arguments, fresh argument Arrays
and Strings, both portable Integer boundaries, strict decimal parsing,
canonical formatting, Float truncation, Integer widening, positive square
root, and negative-square-root NaN behavior. Native and optimized Go produced
byte-identical output on both formal targets.

The six runtime-failure modes also agreed on failure class:

| Case | Native status | Go status | Failure class |
| --- | ---: | ---: | --- |
| invalid decimal format | 2 | 2 | `panic: invalid Integer` |
| sign without digits | 2 | 2 | `panic: invalid Integer` |
| parsed Integer overflow | 2 | 2 | `panic: Integer is outside the portable range` |
| NaN to Integer | 2 | 2 | `panic: Float cannot be converted to Integer` |
| infinity to Integer | 2 | 2 | `panic: Float cannot be converted to Integer` |
| finite Float overflow | 2 | 2 | `panic: Integer is outside the portable range` |

The candidate compiler reached exact B2/B3/B4 fixed points from the immutable
previous-Native seed after explicitly recorded setup-only Native transitions:

| Target | B2/B3/B4 bytes | B2/B3/B4 SHA-256 |
| --- | ---: | --- |
| Darwin arm64 | 299,576 | `6ec0c58a91857ef390d6801018a556d7319414c26de98b1fa4fb936b30694d06` |
| Linux arm64 | 274,144 | `93a4a2c72ac58db3eb344b182be818b3233103229bf9f4976e57bf4e440f97aa` |

Both targets emitted the exact 898,333-byte target-neutral fixed-point QBE
with SHA-256
`7018b68a348cd73e8268dd2e610e0e82308c58c6bd688266e98b4089f5448d9f`.
The portable-entry application QBE was also byte-identical across targets,
with SHA-256
`9e885e1d7dc973e2b28ed04fedf56f166465ac3d00ffb727348c6fc5467763c3`.

The Linux process traces expose the Native compiler, QBE, explicit system CC,
assembler, `collect2`, and `/usr/bin/ld.lld` boundaries. The application
records `libm.so.6`, `libc.so.6`, and the dynamic `sqrt@GLIBC_2.17` reference;
the compiler itself does not acquire a libm dependency. The produced ELF files
retain PIE, RELRO, `BIND_NOW`, and the registered 64 KiB maximum segment
alignment. QBE and CC failure probes preserve the existing output, successful
and failed builds clean Native intermediates, and no Go package or generated-Go
helper enters the ordinary Native chain.

## Measurement method

The TypeRB-authored Darwin controller closed and verified fresh baseline and
candidate chains before measuring. It used two warmups and seven alternating
retained observations for canonical compiler builds, followed by two warmups
and eleven alternating observations for the same successful TypeRB application
built and run through Native and the pinned optimized-Go backend. Elapsed-time
and peak-RSS series were collected independently under one inherited Go-cache
policy. Correctness, hashing, target inspection, and stripping remained outside
the timed intervals.

The Darwin host was an Apple M1 virtual machine with 7 GiB RAM, macOS 15.7.7,
Go 1.27.0, Apple clang 17.0.0, and QBE 1.3. Linux used the GitHub-hosted
`ubuntu-24.04-arm` image, GCC 13's driver and binutils boundary, Ubuntu LLD
18.1.3, Go 1.27.0, and QBE 1.3. Linux performance was not used for the
Darwin-only median claims; it independently verified semantics, fixed points,
tool boundaries, target properties, and artifact sizes.

## Canonical compiler guardrail

Elapsed values are seconds and RSS values are bytes. Medians exclude both
warmups.

| Metric | Fixed baseline | Gate 6M candidate | Candidate change |
| --- | ---: | ---: | ---: |
| canonical build time | 1.650858 s | 1.781807 s | +7.93% |
| canonical build peak RSS | 36,061,184 B | 41,025,536 B | +13.77% |
| raw Darwin compiler size | 283,048 B | 299,576 B | +5.84% |

The registered time and RSS ceiling was +15%; both pass. RSS is the closest
result and retains 1.23 percentage points of headroom. Candidate B2-to-B3 and
B3-to-B4 medians were 1.594822 and 1.616133 seconds, a 1.34% spread. Their peak
RSS medians were 41,041,920 and 41,123,840 bytes, a 0.20% spread. Both are far
inside the registered 25% adjacent-generation bound.

## Native versus optimized Go

| Metric | Native | Optimized Go | Native change |
| --- | ---: | ---: | ---: |
| application build time median | 0.074774 s | 0.183402 s | -59.23% |
| application build peak RSS median | 40,566,784 B | 76,267,520 B | -46.81% |
| application runtime median | 0.001863 s | 0.002620 s | -28.89% |
| application runtime peak RSS median | 1,179,648 B | 4,145,152 B | -71.54% |

The registered non-inferiority ceiling allowed Native to be up to 25% above
optimized Go. Native is below Go on all four primary medians.

| Target and artifact | Native raw | Native stripped | Go raw | Go stripped | Stripped Native reduction |
| --- | ---: | ---: | ---: | ---: | ---: |
| Darwin arm64 application | 50,968 B | 51,000 B | 2,943,650 B | 2,820,376 B | 98.19% |
| Linux arm64 application | 16,096 B | 16,088 B | 2,808,224 B | 1,887,800 B | 99.15% |

The registered size criterion required at least an 80% reduction. Both targets
pass with more than 18 percentage points of headroom. Darwin's size-optimized
Mach-O is 32 bytes larger than the raw observation because the platform strip
operation rewrote aligned metadata; the comparison uses the recorded outputs
without silently selecting the smaller Native number.

The compiler distribution sizes are:

| Target | Raw compiler bytes | Per-target limit | Headroom |
| --- | ---: | ---: | ---: |
| Darwin arm64 | 299,576 | 310,000 | 10,424 |
| Linux arm64 | 274,144 | 310,000 | 35,856 |
| Combined | 573,720 | 620,000 | 46,280 |

## Recorded evidence corrections

Four formal runs remain visible in the public history:

- [run 33316156337](https://github.com/type-rb/type-rb-native/actions/runs/33316156337)
  established the exact Linux fixed point but showed that the GNU linker
  exceeded the unchanged 310,000-byte limit. The target profile adopted the
  explicit LLD boundary in
  [Decision 0022](../../docs/decisions/0022-linux-arm64-lld-linker.md) rather
  than weakening the limit.
- [run 33318347353](https://github.com/type-rb/type-rb-native/actions/runs/33318347353)
  exposed an evidence assertion that required the final LLD boundary one
  setup-only generation too early. The measured candidate did not change.
- [run 33319250310](https://github.com/type-rb/type-rb-native/actions/runs/33319250310)
  passed Darwin and reached the exact Linux fixed point, size, and LLD boundary,
  then exposed two verifier contracts: the shared bootstrap checker emits its
  successful `ok` lines before the final marker, and stripped ELF dynamic
  imports require the dynamic symbol table. PR
  [#119](https://github.com/type-rb/type-rb-native/pull/119) corrected those
  evidence checks without changing the candidate or any threshold.
- [run 33321032161](https://github.com/type-rb/type-rb-native/actions/runs/33321032161)
  is the fresh successful run recorded here.

This history is part of the result: implementation failures and evidence-tool
failures are distinguished rather than discarded or retroactively hidden.

## Raw evidence

The result retains all 106 files downloaded from the successful workflow:

- [`darwin-arm64/raw.csv`](darwin-arm64/raw.csv) contains 230 successful data
  rows, including every warmup, retained observation, median, threshold,
  artifact identity, source identity, and fixed point.
- [`darwin-arm64/process-inventory.txt`](darwin-arm64/process-inventory.txt)
  records exact commands, environment, tool versions, hashes, dependencies,
  outputs, runtime failures, cleanup, and boundary probes.
- [`linux-arm64`](linux-arm64) retains the bootstrap generations, process
  traces, ELF inspection, exact application QBE, success and failure outputs,
  LLD observation, libm boundary, workflow context, and controller contract.
- [`combined-size.txt`](combined-size.txt) records the independently enforced
  cross-target compiler-size bound.
- [`EVIDENCE_SHA256SUMS`](EVIDENCE_SHA256SUMS) covers every retained raw
  evidence file; it excludes this explanatory README and itself.

## Conclusion and deferred scope

Gate 6M establishes that the self-hosted Native implementation can add the
portable numeric and process primitives needed by deterministic benchmark
programs while preserving exact bootstrap fixed points and remaining within a
strict compiler-regression budget. For this bounded identical-source workload,
the resulting Native application is faster, lighter, and substantially smaller
than the optimized-Go output on every registered primary metric.

This is not a general language-performance ranking. Broader TypeRB-versus-Go
and established-language benchmark cases remain independently registered in
[issue #103](https://github.com/type-rb/type-rb-native/issues/103). Persistent
Web and Job resource-lifecycle evidence remains independently registered in
[issue #104](https://github.com/type-rb/type-rb-native/issues/104). General
package resolution, additional standard-library primitives, more targets,
stable target/runtime ABI promises, and automatic external-tool discovery also
remain outside this result.
