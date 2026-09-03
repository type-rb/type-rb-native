# Native MIR stable Array-header measurement

This transition uses the monotonic A/B controller in
`tools/native-mir-guarded-multiply/measure.py`. The selected workload is
`spectral-norm` at input `5500`; wall and CPU medians must each be at most 0.90
times the same-run baseline, while median RSS must be at most 1.05 times the
baseline. Generated QBE and each target's code section must shrink, and the
complete executable may grow by no more than 1.01 times.

`fannkuch-redux` and `n-body` remain exact-output controls. Their wall, CPU,
RSS, generated QBE, code section, and complete executable ratios must stay at
or below 1.02. Compiler build wall and RSS retain their 1.05 limits, and every
retained observation remains subject to the shared 2.0 catastrophic bound.
