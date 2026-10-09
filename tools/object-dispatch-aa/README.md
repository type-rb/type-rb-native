# Object dispatch adoption: A/A prerequisite

This temporary branch-only diagnostic asks whether the existing Linux runtime
measurement primitive compares identical accepted-main programs within the
unchanged regression bounds. It does not run the held optimization.

The immutable public source is run 37765252069, artifact 11544534599. Only the
three accepted `previous` executables identified by `registration.json` run.
Both labels use the same executable path. No compiler, benchmark input, runtime,
daily measurement primitive, existing workflow or acceptance policy changes.

One push of this frozen branch starts one Linux arm64 job, at most 25 minutes.
There are three blocks in fixed Object/Fannkuch/Array order, two labels, and one
warmup plus five retained observations per label per block: 108 executions.
Adjacent label order alternates deterministically. Both roles run on the same
minimum available CPU, with swap disabled, warm filesystem caches, no runtime
instrumentation, LC_ALL=C and GOMAXPROCS=1. No cache drop or runtime flag tuning.

Each block's symmetric maximum/minimum median ratio must be at most 1.05 for
wall, measurable CPU and maximum RSS. CPU below the existing 0.01-second
resolution remains unknown. Every observation, including warmups, must be at
most twice its role/block retained wall median. Outputs must match the unchanged
oracle exactly, with empty stderr. Preserve all observations and failed setup.

Incomplete setup, identity, output or execution failures stop the job. Assess
the entire fixed cohort once; a failed A/A assessment ends this adoption plan.
No rerun, favorable subset, changed aggregation or candidate timing follows a
failure. Passing is only a prerequisite, not a waiver of earlier failed results
or proof of candidate memory safety. This tooling must not merge as an optimizer
change and does not update Pages, daily state, seeds or releases.

Synthetic assessment tests:

```sh
python3 -m unittest discover -s tools/object-dispatch-aa -p 'test_*.py'
```
