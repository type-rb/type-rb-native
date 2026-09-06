# Conservative MIR workspace diagnostic

Status: **rejected and reverted**. This refinement of the pending
[Array-loop connection](https://github.com/type-rb/type-rb-native/issues/303)
does not pass the unchanged 1.05 compiler-build limits.

The candidate avoided binding/read/region/stack workspaces for an empty stream
or a fully validated singleton opaque stream. Every singleton field was
checked, and longer streams used the complete verifier. This was a distinct
source candidate on the direct-row/shared-result implementation, not a retry
of the earlier flat-row opaque shortcut. It did not produce a measured benefit
sufficient for acceptance; the optimization is not retained. The added
malformed conservative-stream controls remain useful independently.

The exact patch applies to `cd2ff931b4846e8c467a0a9a55612b315f57c58e`.
The ordinary compiler B2/B3/B4 SHA256 is
`74274048e1d7709dbeb3465673f80f52d32360f5e58fc73de5dba9c4bd682af6`.
Compiler size is 349256 bytes, text 247856 bytes, and QBE 1112259 bytes.
The source candidate passes 129 compiler tests and all 70 corpus cases at
B2/B3/B4 (210 rows), with identical repeated/adjacent QBE. Its three benchmark
QBE outputs match the previously measured connection exactly. These are not
current-source full recovery, hosted target/process/memory acceptance, or a
new application runtime measurement.

| Ordinary build metric | Baseline median | Candidate median | Ratio |
| --- | ---: | ---: | ---: |
| Wall (s) | 1.506784583 | 1.592150792 | 1.0566545543 |
| CPU (s) | 1.483701 | 1.572843 | 1.0600808384 |
| Root RSS (bytes) | 40157184 | 40304640 | 1.0036719706 |

The baseline remains `1afd60c2c7257ed34fd2a2aa70cb8b9164433009`.
All 18 builds (two warmups and seven retained per role, interleaved) reproduce
their own exact-source compiler. Both roles pass every retained 2.0 catastrophic
bound. Wall and CPU exceed 1.05; RSS passes. The result is not rounded or
retried unchanged.

The unchanged [observer](../2026-09-06-mir-loop-bounds-diagnostic-darwin-arm64/build-cost-observer.py)
uses monotonic wall time and wait4 CPU/root RSS. Each same-basename compiler
builds its own source closure with QBE 1.3, /usr/bin/cc and
`darwin-arm64-v0`. Measurements start after owned correctness batches end.
Host: Apple M2 Pro, 10 logical CPUs, 32 GiB RAM, macOS 26.6.2; Apple clang
21.0.0 (clang-2100.1.1.101); pinned reference
`5dc09070cf7f88a569279f5e63982a6de59d692c`. Warm-cache local execution, no
affinity/frequency or host-isolation claim. Unrelated host activity was not
excluded. Raw results, source patch and correctness logs are retained here.

This diagnostic does not include the separate readonly-binding correction in
PR #306. Neither that correction nor this rejected refinement changes the
frozen comparison baseline or grants an additional allowance.
