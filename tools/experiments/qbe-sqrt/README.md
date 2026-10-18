# QBE square-root instruction experiment

This is an isolated diagnostic for Task #1073 under Initiative #931. It does
not change the ordinary compiler, dependency pins, or shipped QBE acquisition.

The patch applies to the unmodified QBE 1.3 release archive from
<https://c9x.me/compile/release/qbe-1.3.tar.xz>, SHA-256
`d587905d620dc5e1d2bfa7c2cc642b9b837aa89a3188c6e37b53d756cf66e320`.
Upstream licensing remains applicable. The patch adds one floating-only unary
`sqrt` operation, with arm64, amd64 and rv64 instruction selection. Constant
folding is deliberately disabled. It does not recognize or rewrite libm calls.

`operation.ssa` and `edge-driver.c` test explicit operations against host libm,
including signed zeros, subnormals, infinities, NaNs, deterministic bit patterns
and all four standard rounding modes. The C file is an external-backend test
driver, not repository-owned compiler or runtime implementation. Cross-target
assembly is not runtime validation.

`rewrite.py` and `qbe-wrapper.py` are a diagnostic ablation over QBE produced by
the accepted Native compiler. Only the registered typed canonical sqrt call
shape is replaced. All other text remains unchanged. This text transform must
never be promoted to a production optimizer: ordinary integration would consume
the independently verified standard Math intrinsic identity in the Native QBE
adapter, including callable use, without matching emitted symbol text.

The wrapper requires `SQRT_MODE` (`upstream` or `candidate`), `SQRT_QBE`,
`SQRT_EXPECTED_CALLS`, and `SQRT_EVIDENCE_PREFIX`. It saves original and selected
QBE before executing the explicit backend. `observable.trb` checks ordinary
reference-visible edge behavior. Fixed backend comparisons retain all raw
observations and keep first executions separate from steady observations only
under the registered local diagnostic protocol.

Adoption would also need a versioned patched-backend identity, a single audited
source/patch acquisition owner used by all callers, unsupported-backend
rejection, ordinary bootstrap and recovery compatibility, complete target tests,
the full unchanged performance contract, and a maintenance decision based on
the measured benefit. No result from this prototype establishes a formal Go win.
