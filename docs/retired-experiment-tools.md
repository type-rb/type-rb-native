# Retired experiment controllers

The completed gate1–gate6m benchmark projects are no longer part of the current
checkout or ordinary CI. They compare fixed source-era implementations, seeds,
and oracles; they are not additional authorities over the current compiler.
The current recovery, conformance, target, memory and measurement controllers
remain required under the active MIR milestone.

The complete pre-retirement inventory is preserved at
[`d568d9e712452f66fc9c48d6025bf73b79659661`](https://github.com/type-rb/type-rb-native/tree/d568d9e712452f66fc9c48d6025bf73b79659661/tools).
Use a detached checkout of the exact experiment's registered revision when
reproducing its results; do not run those fixed contracts against current main.
No old result or failed cohort is relabeled by removing its controller from
current development.

| Historical projects | Original purpose |
| --- | --- |
| gate1, gate2, gate3 | Scalar, aggregate and managed snapshot/recovery experiments |
| gate4, gate5 | Compiler recovery and executable normalization experiments |
| gate6a, gate6b | File entry and Native-owned single-file builds |
| gate6c, gate6d | Ordinary Native bootstrap closure and Linux arm64 introduction |
| gate6e, gate6f | File-root modules and multi-file compiler self-hosting |
| gate6g, gate6h | Symbol lookup, module loading and reachability comparisons |
| gate6i, gate6j | Float scalar and Float Array introduction |
| gate6k | Configured projects and the source-era scale workload |
| gate6m | Portable benchmark-entry primitives |

The retained
[historical portable-entry workflow](../.github/workflows/historical-portable-entry.yml)
checks out its exact tooling revision `5cf61c740aa600c34ed94f1b130ea2ffefd9e783`
before accessing the old benchmark project and Linux controller. Its old paths
are explicit historical reproduction inputs, not live implementation owners.
Its source/oracle/seed pins and measurement contracts remain unchanged.
