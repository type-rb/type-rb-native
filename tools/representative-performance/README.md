# Representative application and input coverage

This opt-in diagnostic implements the [performance policy](../../docs/performance-policy.md).
It never modifies daily/weekly schedules, baselines, thresholds or published
victory counts. `suite.json` registers all input variants before measurement.

The single TypeRB executable contains three application workloads and four
sensitivity families. Runtime arguments select workload, count, variant and
batch count. Go uses ordinary standard-library facilities with matching output,
Unicode code-point counts and observable retained lifetimes. A separate Python
oracle checks every batch and final retained-data checksum. Setup is included
in process wall/CPU/RSS, while the `ready` marker separates it from batch-arrival
observations. Input parsing operates in memory; file/network I/O is not measured.

## Run locally

Build the current Native CLI once using the repository's ordinary procedure.
Reuse the pinned reference CLI and a shared Go build cache if comparing controls.
The controller never builds a compiler and deletes all temporary application
binaries/generated Go projects when finished or failed.

```sh
python3 tools/representative-performance/measure.py \
  --native bin/trbn --smoke --evidence /tmp/representative-smoke

python3 tools/representative-performance/measure.py \
  --native bin/trbn --reference /path/to/pinned/trb --go /path/to/go \
  --gc-probes --evidence /tmp/representative-diagnostic

python3 -m unittest discover -s tools/representative-performance -p 'test_*.py'

python3 tools/representative-performance/report.py /tmp/representative-diagnostic/manifest.json
```

`--evidence` must be new. `--case ID` selects registered cases and is repeatable.
`--samples N` fixes 1..100 retained fresh processes before a run; the default is
three, after one first process/warmup per role. All observations remain in the
result. `--smoke` uses 23 items and two batches for each operation/variant,
without warmup or repetition. Smoke wall times do not establish speed claims.

Each binary is built once and reused for the entire matrix. Compilation has a
120-second timeout per role; each application has a 30-second deadline and the
runtime matrix has a 15-minute deadline. The runner supports Darwin and Linux
with `wait4` CPU/RSS accounting. Run without other heavy work. `GOMAXPROCS=1`
and disabled Native instrumentation apply to ordinary observations; record the
machine and tool versions when interpreting local diagnostics. Controls are
optional for correctness smoke; missing controls cannot receive a win.

## Read results

`manifest.json` lists exact input cases, executable/source/tool hashes, per-role
summaries and Native/control median wall ratios (below 1 means shorter wall).
Raw `observation.json`, stdout and stderr remain for every process, including
failure; a failed run retains its partial manifest and exits nonzero. No rerun
or outlier removal happens automatically. Temporary binaries are not evidence.

Process p95 needs at least 20 observations and p99 at least 100; otherwise the
field is null. These are empirical nearest-rank summaries, not significance or
confidence claims. Peak RSS is per process, not a sampled live-heap curve.
Throughput is input items across all batches divided by full process wall time.
It includes preparation and output and is not a maximum service throughput.

Batch completion intervals are observed by the parent when stdout lines arrive.
They include pipes and scheduling, and exclude initial input setup after the
`ready` marker. If multiple lines arrive together, interval summaries are null
with a reason. The medium worker has 100 batches to expose sustained behavior;
its interval p99 is still not request latency or a GC-pause measurement. Request
queueing, cross-language allocation counters, live RSS trajectories, file/network input and
parallelism need dedicated future probes or existing resource-soak harnesses.

`--gc-probes` separately runs medium worker/allocation cases with the existing
Native runtime counters enabled. It retains allocated/reclaimed/live managed
bytes and other available collector counters. These instrumented observations
never enter wall-time comparisons, and Native managed allocations are not
presented as equivalent to Go total heap allocations. Live RSS trajectories and
service pause times still need the dedicated resource/load harnesses.

## CI

The existing Native CLI job reuses its built CLI for `--smoke`, with a two-minute
step deadline. Controller tests run in the existing tooling job. No new workflow,
compiler bootstrap, comparative timing gate or scheduled matrix is added.
Changing the workload/controller still uses the planner's applicable authorities;
this does not waive full validation for this change itself.
