# Project scenarios

Each `m<N>-manifest.json` freezes the initial scenario set for one milestone of
[Decision 0086](../../docs/decisions/0086-production-web-application-path.md).
Fixture directories are named by scenario ID. At most 20 scenarios are frozen
per milestone before activation; broader conformance stays in that milestone's
backlog.

Each scenario records:

- its public reference source;
- a fixture directory, and the commands run in `cwd`;
- the dependencies it exercises;
- its `expectation`.

`reference` records the outcomes from the pinned reference, and
`nativeBaseline` records `trbn` before the milestone. Paths are normalized to
`<fixture>`. A failing step ends its sequence, and every scenario runs in a
fresh copy of its fixture.

Nothing consumes these fixtures yet. The milestone implementation adds the
runner that replays them.
