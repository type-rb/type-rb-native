# Formal Static String Compactness A/B Result on Darwin and Linux arm64

Dependency-free compression of profitable long static Strings passes the
registered correctness, exact fixed-point, build-cost, RSS, target-neutrality,
application, and compiler-size contract. The self-hosted compiler pair is
32,520 bytes, or 5.73%, smaller than current main while the source QBE
templates remain readable TypeRB text.

This result applies to the exact revisions, targets, compiler source, and
toolchains below. It is not a general compression ratio or application-size
claim.

## Exact scope

- preregistered scope:
  [issue #146](https://github.com/type-rb/type-rb-native/issues/146);
- exact current-main baseline:
  `22c2c488dd8cfd946d6c7b16bf7c301012f17e44`;
- measured candidate head:
  `de0973298a1e1cf4b408dc73b5ae36f4463b1cd2`;
- measured pull-request merge ref:
  `65e2d7fc9abd8ab796b018c532a018b90bb67745`;
- TypeRB semantic oracle:
  `5dc09070cf7f88a569279f5e63982a6de59d692c` (`0.4.4-dev`);
- immutable previous-Native seed `bootstrap-seed-2026-08-30`;
- Native target profiles `darwin-arm64-v0` and `linux-arm64-v0` with QBE
  1.3, Apple Clang 17.0.0 or GCC 13.3.0, and Linux LLD 18.1.3; and
- successful formal workflow
  [33400136834](https://github.com/type-rb/type-rb-native/actions/runs/33400136834).

The candidate converts each ASCII static String to bytes once. Literals of at
least 256 bytes use a deterministic bounded-backreference encoding only when
the encoded payload is smaller. Matches are between 4 and 130 bytes with a
maximum 65,535-byte distance and a fixed 512-entry encoder table. Encoded data
is expanded once into zero-filled writable static String storage before
program or compiler code runs. No heap allocation, compression library,
generated source blob, Go process, or new runtime dependency is introduced.

A program without a profitable long literal emits neither compressed data nor
the decoder or initialization call. Compiler-shaped input retains value-based
literal deduplication, so equal long templates share one decoded object.

## Compiler compactness and fixed points

| Target | Baseline | Candidate | Reduction | Candidate limit | Headroom |
| --- | ---: | ---: | ---: | ---: | ---: |
| Darwin arm64 | 299,576 B | 283,080 B | 5.51% | 285,000 B | 1,920 B |
| Linux arm64 | 268,248 B | 252,224 B | 5.97% | 255,000 B | 2,776 B |
| Combined | 567,824 B | 535,304 B | 5.73% | 540,000 B | 4,696 B |

After the documented two setup-only Go-free transitions, candidate B2, B3,
and B4 are byte-identical on each target. The Darwin compiler SHA-256 is
`cf76dfc7832f0252522c042e53d52213a61b1dfda4236167665ebf23dae7b66b`;
the Linux compiler SHA-256 is
`e01775f5fe48eb5bfd536bf13fb133505e8527b6c41ad319231416c1a3f26d5e`.

Both targets repeatedly emit the same 869,699-byte target-neutral QBE with
SHA-256
`7c5205da0eadfaae81ed53bb0653fbd0df38d8462046ecc33fab6a545580d7e8`.
The changed QBE is the exact self-representation of the smaller compiler; it
is byte-identical across targets and repeated generations.

## Interleaved build cost

Each target used two warmup rounds and seven retained rounds. Baseline and
candidate alternated first position on each round independently for B2-to-B3
and B3-to-B4. The bootstrap harness's grouped legacy observations remain
closure evidence but do not decide this A/B comparison.

| Target and stage | Baseline time | Candidate time | Ratio | Baseline RSS | Candidate RSS | Ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Darwin B2-to-B3 | 1.40 s | 1.31 s | 0.935714 | 41,140,224 B | 41,058,304 B | 0.998009 |
| Darwin B3-to-B4 | 1.38 s | 1.35 s | 0.978261 | 41,189,376 B | 41,172,992 B | 0.999602 |
| Linux B2-to-B3 | 1.02 s | 0.88 s | 0.862745 | 64,385,024 B | 64,376,832 B | 0.999873 |
| Linux B3-to-B4 | 1.03 s | 0.89 s | 0.864078 | 64,380,928 B | 64,385,024 B | 1.000064 |

Every median passes the frozen 1.05 maximum. All 56 retained processes return
status zero. The worst retained elapsed/RSS observation is 1.142857 times its
applicable baseline median, below the unchanged 2x catastrophic bound.

## Conditional output and long-literal application

The no-profitable-long-literal control remains byte-identical between baseline
and candidate, including the linked executable. It contains no decoder symbol.

The generated 16 KiB long-literal application emits deterministic QBE,
contains one initialization call, returns status zero with exact stdout, and
has no stderr. Its reductions are:

| Target | Artifact | Baseline | Candidate | Reduction |
| --- | --- | ---: | ---: | ---: |
| both | QBE | 99,865 B | 38,330 B | 61.62% |
| Darwin arm64 | executable | 67,464 B | 50,936 B | 24.50% |
| Linux arm64 | executable | 31,928 B | 16,272 B | 49.04% |

The Linux executable remains PIE with BIND_NOW and RELRO, has exactly one
non-executable GNU_STACK segment, and depends only on `libc.so.6`. Darwin
depends only on `/usr/lib/libSystem.B.dylib`. QBE and the configured system C
driver/assembler/linker remain the only ordinary backend tools.

Focused tests cover the 255/256-byte threshold, an incompressible 256-byte
value, overlapping matches, escapes and newlines, multiple distinct compressed
literals, terminating zero, conditional decoder emission, deterministic QBE,
execution, and compiler-literal value deduplication. The 42-test compiler suite
and expanded executable conformance case pass.

## Retained evidence

The three GitHub artifact archives are listed with their IDs, sizes, and
SHA-256 values in [`ARTIFACTS.tsv`](ARTIFACTS.tsv). Extracted evidence is
retained without compiler binaries:

- [`darwin-arm64`](darwin-arm64) and [`linux-arm64`](linux-arm64) contain the
  complete baseline and candidate bootstrap identities, measurements,
  environments, dependencies, process evidence, and metadata;
- each target's [`comparison-evidence`](darwin-arm64/comparison-evidence)
  retains all 36 warmup/retained rows, median decisions, catastrophic checks,
  and fixed-point identities;
- each target's [`application-evidence`](darwin-arm64/application-evidence)
  retains the exact short/long size decision and executable segment inventory;
  and
- [`cross-target.txt`](cross-target.txt) retains the combined size and exact
  target-neutral QBE decision.

[`EVIDENCE_SHA256SUMS`](EVIDENCE_SHA256SUMS) covers every extracted evidence
file and `ARTIFACTS.tsv`, excluding this README and the checksum file itself.

## Conclusion

Long static templates no longer consume nearly all remaining compiler-size
headroom. The kept representation is self-hosted, deterministic,
dependency-free, target-neutral, and cheaper to build in the measured runs.
Future compactness work can start from the 535,304-byte combined compiler pair
without weakening the established per-target or combined limits.
