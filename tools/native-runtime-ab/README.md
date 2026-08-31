# Native runtime A/B controller

This controller compares two self-hosted Native compiler revisions without a
language or implementation change in the measured source. It exists for
bounded code-generation and runtime optimizations whose effect must be
separated from the broader cross-language benchmark.

## Fixed contract

- candidates in rotation order: `baseline`, then `candidate`, with
  `typerb-go` added only for the literal-String worker comparison;
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
| `fannkuch-redux` | 10 | 0.97 |
| `n-body` | 1,000,000 | 1.02 |
| `spectral-norm` | 5,500 | 1.02 |
| `worker-literal-concat` | one phase, 400,000 batches | 0.70 |

These inputs are the Array-address optimization contract registered in
[issue #140](https://github.com/type-rb/type-rb-native/issues/140). They do not
replace the full cross-language benchmark inputs or its published results.

The `worker-literal-concat` case is registered in
[issue #152](https://github.com/type-rb/type-rb-native/issues/152). It also
requires candidate wall and CPU medians to remain within 2.00x the exact
optimized-Go medians. All three programs use the same authored TypeRB source.

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
