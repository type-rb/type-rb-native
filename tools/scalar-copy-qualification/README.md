# Scalar Array copy Linux diagnostic

This temporary branch-only harness measures the fixed candidate registered in
[Task 1013](https://github.com/type-rb/type-rb-native/issues/1013).
It does not change the daily suite, preparation graph, measurement controller,
workload, reference, seeds, Pages data, or adoption requirements.

One Linux arm64 attempt permits 67 case/role rows and 674 timed observations.
Fannkuch is the primary runtime beneficiary. The verifier checks raw
counts, output status, workload and tool identities, summaries, runtime/memory
bounds, reproducibility, and measured application-build competitor advantages.
Missing comparators and below-resolution observations remain explicit. Increased
build cost does not imply adoption. Matched compiler cost, full GC accounting,
platform authorities and PR acceptance remain separate outstanding obligations.

The workflow checks out the immutable candidate separately from this tooling
commit. Remove this diagnostic tooling before implementation PR acceptance.
Failures and unused allowance remain recorded; do not rerun the workflow.

Run the verifier's synthetic checks with:

```sh
python3 -m unittest discover -s tools/scalar-copy-qualification -p test_qualify.py
```
