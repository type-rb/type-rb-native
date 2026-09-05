# Rejected Native MIR Integer-halving diagnostic

Status: rejected local diagnostic for [issue #251](https://github.com/type-rb/type-rb-native/issues/251).
No compiler change from this experiment is accepted. This result does not
replace the formal cross-language benchmark snapshot.

The preregistered candidate replaced verified Integer division by the exact
same-block literal `2` with logical sign extraction, bias addition, and signed
right shift. Independent MIR checks retained operand identity, Integer types,
the same-block definition, and the failure edge. A mechanical consolidation of
Float arithmetic and Integer division/remainder dispatch reduced its cost,
but the complete candidate still fails both compactness and local runtime.

The retained CSV uses LF line endings; numeric fields and observations are
unchanged. `EVIDENCE_SHA256SUMS` covers all 42 retained support files and excludes
only this README and the inventory itself.

## Identity and scope

- Baseline: accepted `a1c5177583d26bea264b288ca1d8ea54af40afc6` (PR #250).
- Candidate: apply [candidate.patch](candidate.patch) to that revision in a
  disposable checkout. No candidate compiler binary is retained in Git.
- Compiler source SHA-256:
  `5bc9824079ad6b384aada8158b47d380d17073dd474f920a432f53dcdf916662`.
- Compiler-test source SHA-256:
  `83ecd21b15a3fcf971f16bb60be1f9c093b95eeb7cc12e5a531bcc0e3006ca1e`.
- Patch SHA-256:
  `d0e120c79c3f43d9b559c82c18379c5ee8c5adf8f9ac26f6a8e1e0693b25714b`.
- Darwin arm64, Apple M2 Pro, macOS 26.6.2, QBE 1.3 and Apple clang 21.
- TypeRB reference: `5dc09070cf7f88a569279f5e63982a6de59d692c`.

The accepted Native compiler built the diagnostic through the ordinary
file-root interface. Candidate-emitted compiler QBE matches the accepted
compiler's emission of the same source byte for byte. This is not a complete
three-generation or cross-target acceptance claim.

## Compiler cost

| Metric | Accepted baseline | Final diagnostic | Delta |
| --- | ---: | ---: | ---: |
| Complete compiler bytes | 349,224 | 349,232 | +8 |
| Mach-O code bytes | 248,800 | 249,440 | +640 |
| Portable compiler QBE bytes | 1,116,173 | 1,120,287 | +4,114 |

The initial shape before the shared Float-dispatch refactor was larger still:
1,121,650 QBE bytes and 249,948 code bytes. Neither shape satisfies the frozen
strict recovery conditions. The final compiler QBE SHA-256 is
`e836b2aaf0ae12e6b78268d5c3748818012333f2ca06d200981a7aec73c54ad0`.

## Local runtime diagnostic

The unchanged `spectral-norm` source at input 5500 was measured using the
existing `tools/native-mir-guarded-multiply/measure.py` controller: two warmups
and seven alternating retained fresh-process observations per role. The script
uses `time.monotonic_ns` and child `wait4` CPU/RSS measurements. Build time is
not included. This is an ordinary local-host diagnostic, not the isolated
Linux BenchExec contract used for the public language comparison; host cache
state is not explicitly controlled.

| Metric | Baseline median | Candidate median | Candidate / baseline |
| --- | ---: | ---: | ---: |
| Wall seconds | 2.347475583 | 2.492212875 | 1.061657 |
| CPU seconds | 2.327917 | 2.474612 | 1.063016 |
| Peak RSS bytes | 2,441,216 | 2,441,216 | 1.000000 |
| Application QBE bytes | 52,173 | 52,067 | 0.997968 |
| Application code bytes | 10,684 | 10,716 | 1.002995 |
| Complete application bytes | 50,992 | 50,992 | 1.000000 |

All 18 fresh processes return the exact expected result with empty stderr and
status zero. Every retained catastrophic observation remains below 2.0, but
both runtime ratios fail the registered 0.95 limit. The candidate uses about
6.2% more wall time. Shorter QBE is not evidence of faster machine code; this
whole-candidate observation is not a universal instruction-latency claim.

The baseline application is byte-identical to the accepted header-reuse
application: PR #250 changes compiler representation only. Both executable
digests and the complete decision inputs are in [summary.json](summary.json).
The application source SHA-256 is
`b85e0d8cecf4e7455bdd34a6a02cb3a9a6e7bbe57ec29bb2f1b99afbbb5312f2`;
the measurement-controller SHA-256 is
`f03adc024300e0be5d8304ebd1000a5a390d9f8acaceadf3c10375643e27a45e`.

## Correctness checked and work deliberately not run

Root/core source checking and formatting pass. The two focused MIR tests pass,
covering ordinary and inline lowering, other/dynamic/Float divisors, forged
literal and operand identities, a missing failure edge, and a definition from
a preceding function that must not be reused. The [boundary program](boundaries.trb)
matches [the expected output](boundaries.expected) through both the diagnostic
Native compiler and the pinned optimized Go reference, including zero, signed
odd/even operands, and both portable Integer limits.

The full suite, hosted target/fixed-point/memory checks, and long control
benchmarks were not run after the local rejection. This result cannot claim
those acceptance conditions. The patch is retained only to make the rejected
diagnostic inspectable and reproducible; it is not active compiler source.

No threshold is relaxed. Any subsequent attempt needs a materially different
verified lowering or range proof and replacement of enough existing compiler
logic; simply resubmitting this bias-and-shift sequence is not justified.
