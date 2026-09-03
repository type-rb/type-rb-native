# Native MIR guarded Integer add measurement

This transition reuses the monotonic A/B controller in
`tools/native-mir-guarded-multiply/measure.py`. The controller is arithmetic
operation independent: it compares two exact executables, enforces output and
stderr equality, records two warmups and seven retained alternating processes,
and applies the supplied runtime-ratio limit plus the shared RSS and
catastrophic limits.

The selected workload is `spectral-norm` at input `5500`. Both wall and CPU
medians must be at most 0.95 times the same-run baseline, median RSS at most
1.05 times baseline, and all output must remain exact. `fannkuch-redux` and
`n-body` remain controls with 1.02 limits.
