# Checked postfix copy diagnostic

Status: **rejected and reverted** under the unchanged
[Array-loop connection](https://github.com/type-rb/type-rb-native/issues/303)
build-cost contract. This result does not supersede the retained connection
candidate or authorize a Pages update.

The candidate returned an unchanged checked operand when no call, member, or
index postfix followed. A real postfix chain still used a separately rebound
local record. This avoided the previously rejected immutable-to-mutable alias:
the source remained legal under the pinned reference. Tests retain all checked
value fields, cursor position, and independence of an actual postfix result.

The exact patch applies to `cd2ff931b4846e8c467a0a9a55612b315f57c58e`.
B2/B3/B4 compiler SHA256:
`16d9d11c065762acd07e5c2ad1a1c41c644be1b6389b8e48ac331104196f618e`.
Compiler size is 349256 bytes, text 248208 bytes, and compiler QBE 1111309
bytes. The source candidate passes 131 compiler tests, 21 focused
postfix/Array-loop tests, and the full 70-case corpus at B2/B3/B4 (210 rows).
Repeated/adjacent QBE and the three previously measured application QBE outputs
are unchanged. Current-source full recovery and hosted acceptance were not run
for this rejected cost candidate.

| Ordinary build metric | Baseline median | Candidate median | Ratio |
| --- | ---: | ---: | ---: |
| Wall (s) | 1.50244825 | 1.583444292 | 1.0539093723 |
| CPU (s) | 1.487649 | 1.569997 | 1.0553544553 |
| Root RSS (bytes) | 40402944 | 40075264 | 0.9918896999 |

The baseline remains `1afd60c2c7257ed34fd2a2aa70cb8b9164433009`.
All 18 builds (two warmups and seven retained per role, interleaved) reproduce
their own exact-source compiler. Every retained value for both roles passes
2.0; RSS passes 1.05, while wall and CPU fail 1.05. The source change was
reverted, not retried unchanged. Small differences among independently measured
rejected variants do not establish a performance ranking.

The unchanged [observer](../2026-09-06-mir-loop-bounds-diagnostic-darwin-arm64/build-cost-observer.py)
uses monotonic wall time and wait4 CPU/root RSS. Each same-basename compiler
builds its own source closure with QBE 1.3, /usr/bin/cc and
`darwin-arm64-v0`. All owned correctness batches completed before measurement.
Host: Apple M2 Pro, 10 logical CPUs, 32 GiB RAM, macOS 26.6.2; Apple clang
21.0.0 (clang-2100.1.1.101); pinned reference
`5dc09070cf7f88a569279f5e63982a6de59d692c`. Warm-cache local execution, without
CPU affinity, controlled frequency or host-wide isolation. Unrelated host
activity was not excluded; retrieval of small hosted verification artifacts
also began during this observation batch.

Raw results, exact source patch, corpus statuses and test log are retained.
The added ownership and malformed-stream tests remain independently useful.
The separate readonly-binding correction in PR #306 is not included in this
candidate and does not move the frozen comparison baseline.
