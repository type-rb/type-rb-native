# Native MIR Float Array-reduction workload

These focused workloads measure the exact verified `Array<Float>` reduction
plan. They are not language benchmarks.

`workload.trb` keeps 10 finite Float values hot while calling the selected
reduction 10,000,000 times, exposing redundant per-element control overhead.
`streaming.trb` traverses 100,000 values 1,000 times, retaining the same total
element visits while giving memory traffic more weight. Both must print their
checked-in expected output. The existing Array-loop measurement controller
runs each direct executable twice for warmup, retains 21 alternating
observations, uses an in-process monotonic clock and per-process resource usage,
and rejects output or diagnostic differences.

Acceptance requires hot-workload candidate/baseline wall and CPU medians at or
below 0.75, streaming-workload medians at or below 0.90, peak-RSS medians at or
below 1.05, and every retained wall, CPU, and RSS value for both executables
below 2.0 times the corresponding baseline median. Formal CI also requires the
fixed compiler not to grow and keeps the recovered target-neutral QBE and arm64
code-section ceilings unchanged.

`empty.trb`, `nonfinite.trb`, and `unsupported.trb` retain empty-input,
non-finite-result, and direct-fallback behavior outside the timed observations.
