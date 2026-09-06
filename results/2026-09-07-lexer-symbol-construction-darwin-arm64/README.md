# Lexer symbol construction: local cost checkpoint

Status: **local prefilter passes; hosted acceptance remains required**.
This follows the [first hosted cost rejection](../2026-09-07-loop-bounds-hosted-cost-rejection/README.md)
for [issue #303](https://github.com/type-rb/type-rb-native/issues/303), not an
unchanged-source retry or a new performance allowance.

The lexer recognizes its ten two-character symbols from the two existing
characters and materializes the pair only when it becomes the emitted token.
The previous implementation allocated a pair for every symbol with lookahead
and compared it against all ten spellings. No supported token, failure class,
source position, language semantics or MIR optimization permission changes.
The implementation removes 24 net lines from the compiler entry module.

The exact compiler/test patch applies to
`0af0da7e2756742da5033a6c8b7e082b97433ac1`. Three new tests cover all 841 pairs
in a 29-character symbol/control alphabet, 540 symbol/lookahead or EOF cases,
and unsupported-punctuation diagnostics. The full compiler suite passes 138
tests. All 75 corpus cases pass at B2/B3/B4 (225 observations), with exact
invalid diagnostics, repeated/adjacent QBE and invalid-source tool boundaries.

| Ordinary build metric | Baseline median | Candidate median | Ratio |
| --- | ---: | ---: | ---: |
| Wall (s) | 1.506968584 | 1.575096709 | 1.0452087228 |
| CPU (s) | 1.48919 | 1.55852 | 1.0465555100 |
| Root RSS (bytes) | 40206336 | 40337408 | 1.0032599837 |

The unchanged [observer](../2026-09-06-mir-loop-bounds-diagnostic-darwin-arm64/build-cost-observer.py)
uses frozen baseline `1afd60c2c7257ed34fd2a2aa70cb8b9164433009`, two warmups and
seven interleaved retained observations per role. All 18 builds reproduce their
source compiler. All median ratios pass the unchanged 1.05 bound and every
retained observation passes 2.0 of the baseline median. These separate batches
do not establish a statistically significant improvement over the preceding
candidate, and the remaining margin is small.

B2/B3/B4 SHA-256:
`78c9ef8a1bb012728f63262355093e02855079ec49f30b671ef8494d8d8a68e2`.
Complete compiler: 349256 bytes; Mach-O text: 247740 bytes; compiler QBE:
1109322 bytes, SHA-256
`aa76fdfad01c5cfdda1fc481c653dd56014ca3c9e5e52153dad378b5d694afd8`.
All three numeric application QBE outputs are byte-identical to the preceding
checked-binding candidate; no new runtime measurement is claimed.

An untimed same-source check allocates 250564267 bytes with the candidate versus
250944318 with the preceding compiler, 380051 bytes fewer. Peak managed heap
increases; both report zero final live bytes for that invocation only. This is
not general leak-freedom evidence.

Host: Apple M2 Pro, 10 logical CPUs, 32 GiB RAM, macOS 26.6.2; Apple clang 21.0.0
(clang-2100.1.1.101), QBE 1.3, `/usr/bin/cc`, `darwin-arm64-v0`. Reference revision:
`5dc09070cf7f88a569279f5e63982a6de59d692c`. Warm caches; no CPU affinity,
controlled frequency or host-wide isolation. Wall time is monotonic; CPU/RSS
use wait4 orchestration-root accounting. Owned correctness jobs finished before
timing. Current-source full root recovery and hosted authorities remain pending.
Run the inexpensive hosted compiler comparison before another long recovery or
runtime batch; all normal acceptance checks remain mandatory before merge.
