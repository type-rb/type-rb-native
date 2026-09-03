# Native MIR guarded Integer multiply measurement

This directory contains the monotonic A/B controller for the guarded checked
`Integer` multiply transition. The workflow builds the unchanged Benchmark
Game sources with the exact baseline and candidate compilers, then uses this
controller for interleaved same-run comparisons.

The selected workload is `spectral-norm` at its formal input `5500`. It must
improve both median wall and CPU time by at least 10%. `fannkuch-redux` at `12`
and `n-body` at `50000000` are controls and may not regress either median by
more than 2%. Every run must preserve exact stdout and empty stderr. Median RSS
may not exceed 1.05 times the baseline, and no retained wall, CPU, or RSS
observation may exceed twice the corresponding baseline median.

The workflow uses two warmups and seven retained observations per executable.
Only the Linux arm64 lane makes runtime decisions; both arm64 lanes check
portable QBE, executable code size, fixed points, and the focused conformance
cases.
