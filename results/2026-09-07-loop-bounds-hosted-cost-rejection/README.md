# Array-loop bounds: first hosted cost rejection

Status: **rejected compiler-cost candidate**, not runtime acceptance.

[Run 34064721027, attempt 1](https://github.com/type-rb/type-rb-native/actions/runs/34064721027)
compares candidate `1adc9377d5e729bd1047e22b89ab3f8128d68299` with frozen
baseline `1afd60c2c7257ed34fd2a2aa70cb8b9164433009`. The workflow and measurement
policy are unchanged from that exact candidate. Original interleaved observations,
completed comparison rows, code sections and generation identities are retained
here byte-for-byte from the two public artifacts. Full process inventories and
bootstrap metadata remain attached to the linked run.

| Target | Compiler bytes ratio | Build wall ratio | Result |
| --- | ---: | ---: | --- |
| Darwin arm64 | 1.049725 | 1.039886 | Target job passes |
| Linux arm64 | 1.049881 | 1.060729 | Build wall exceeds 1.05 |

Linux retained baseline/candidate medians are 1.235/1.310 seconds. Its comparison
step stops at that failure: RSS and catastrophic evaluation files must not be
interpreted as complete passing evaluations. All interleaved raw observations
are retained, including warmups. The combined target authority also fails.
Darwin records build RSS ratio 1.003591 and completes its later controls.

Both targets reproduce B2/B3/B4 compiler bytes. Their target-neutral compiler
QBE SHA-256 is `b1cc65898073be8f816b8ef8b72cf3e129687c6713f6a631461fcc377e81a941`,
1,110,446 bytes. This identity does not override the failed cost bound.

The [local prefilter](../2026-09-07-checked-binding-construction-darwin-arm64/README.md)
passes on a different Darwin host; it is not a substitute for the failed Linux
authority. Full local recovery subsequently passes 95 root and 135 compiler
tests. CLI run [34064706224](https://github.com/type-rb/type-rb-native/actions/runs/34064706224)
passes both arm64 targets. None establishes runtime improvement or Pure Go parity.

Runtime run [34064719389](https://github.com/type-rb/type-rb-native/actions/runs/34064719389)
stops before measurement because its synthetic test suite inherited the job's
selected contract. PR validation [34064706363](https://github.com/type-rb/type-rb-native/actions/runs/34064706363)
stops at whitespace validation of the original CSV CRLF bytes. These setup
failures are corrected separately; no numerical result is discarded or retried.
The runtime suite now selects its own default contract before testing explicit
contracts. Scoped Git attributes preserve original CSV bytes and checksums while
still rejecting actual trailing spaces and blank-at-EOF defects.

PR #307 remains draft. Further compiler cost reduction is required before new
hosted acceptance. No threshold, marker, benchmark input or Pages result changes.
