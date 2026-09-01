# Native runtime A/B controller

This controller compares two self-hosted Native compiler revisions without a
language or implementation change in the measured source. It exists for
bounded code-generation and runtime optimizations whose effect must be
separated from the broader cross-language benchmark.

## Fixed contract

- candidates in rotation order: `baseline`, then `candidate`, with
  `typerb-go` added for registered worker comparisons;
- BenchExec `runexec` 3.35 on Linux arm64;
- one explicitly selected logical CPU;
- two warmup rounds followed by eleven retained rounds;
- alternating first position on every round;
- `4GB` process-tree memory limit;
- cache control before every measured process;
- exact status-zero, empty-stderr, and stdout-oracle checks before and during
  timing; and
- raw wall time, CPU time, process-tree peak memory, exit state, and output for
  every observation; and
- every role's retained wall, CPU, and peak-memory observation at no more than
  2.00x that role's retained median.

The five-column TSV catalog is:

```text
case  candidate  command  input  expected
```

Fields are tab-separated. Every case contains exactly the `baseline` and
`candidate` rows in that order. Commands are executed directly.

The currently registered cases and thresholds are:

| Case | Input | Maximum candidate/baseline wall and CPU ratio |
| --- | ---: | ---: |
| `fannkuch-redux` | 10 | 1.02 |
| `n-body` | 1,000,000 | 1.02 |
| `spectral-norm` | 5,500 | 0.97 |
| `worker-literal-concat` | one phase, 400,000 batches | 0.70 |
| `worker-managed-alias-roots` | one phase, 400,000 batches | 0.80 |
| `worker-managed-array-growth` | one phase, 400,000 batches | 0.95 |
| `worker-array-push-fast-path` | one phase, 400,000 batches | 0.95 |
| `worker-dynamic-array-address` | one phase, 400,000 batches | 0.95 |
| `worker-gc-temp-push-fast-path` | one phase, 400,000 batches | 0.985 |

The three numeric inputs apply the bounded loop-invariant Array-header contract
registered in
[issue #179](https://github.com/type-rb/type-rb-native/issues/179).
They do not replace the full cross-language benchmark inputs or its published
results. The same experiment limits the fixed-point Linux arm64 compiler to
1.02x the exact baseline and 260,000 bytes; adjacent bootstrap wall time, CPU
time, and peak RSS to 1.05x; each application's QBE to 1.005x; and raw plus
stripped executables to 1.001x.

Both compiler revisions are closed from their exact source trees, while one
candidate-revision bootstrap observer measures both chains. This keeps the
wall, CPU, and RSS columns identical across the A/B pair even when the frozen
baseline predates a newly added evidence column; the observer does not replace
either compiler or source tree.

Each worker case is registered by its linked public experiment and also
compares candidate wall and CPU medians with an exact optimized-Go control.
All three programs use the same authored TypeRB source. The temporary-root
push split is registered in
[issue #162](https://github.com/type-rb/type-rb-native/issues/162).
The dynamic Array-address split is registered in
[issue #166](https://github.com/type-rb/type-rb-native/issues/166).

## Invocation

```text
/bin/sh tools/native-runtime-ab/runtime-controller.sh \
  formal RUNEXEC CATALOG CASE CORE \
  tools/benchmarksgame-formal/cache-control-linux.sh WORKSPACE EVIDENCE
```

`raw.tsv` retains warmups and measurements, `medians.tsv` contains only the
eleven retained observations, and `evaluation.tsv` applies the registered
ratio. Any measured failure completes the schedule before returning failure.
The deterministic fake-`runexec` regression is:

```text
/bin/sh tools/native-runtime-ab/runtime-controller-test.sh
```
