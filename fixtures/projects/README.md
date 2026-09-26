# Project scenarios

`m1-manifest.json` is the frozen initial scenario set for M1 (project
configuration, mode selection, local path packages and bundled official package
sources) from [Decision 0086](../../docs/decisions/0086-production-web-application-path.md).

Each scenario names its public reference source, a fixture directory, the
commands run in `cwd`, the dependencies it exercises, and its `expectation`.
`reference` records the pinned reference outcomes and `nativeBaseline` records
`trbn` before M1. Paths are normalized to `<fixture>`, and a failing step ends
its sequence. Every scenario runs in a fresh copy of its fixture.

Nothing consumes these fixtures yet. M1's implementation adds the runner that
replays them; broader conformance stays in the M1 backlog.
