import { test } from 'node:test';
import assert from 'node:assert/strict';
import { assessment, change, value, metrics } from '../../docs/capabilities/benchmarks/daily-model.mjs';
test('verdicts distinguish speed, memory, build time and size without inverting ratios', () => {
  assert.deepEqual(assessment(change(80, 100), 'runtime'), { tone: 'better', label: 'Faster', detail: '20.0% less time' });
  assert.equal(assessment(change(120, 100), 'runtime').label, 'Slower');
  assert.equal(assessment(change(80, 100), 'memory').label, 'Less memory');
  assert.equal(assessment(change(120, 100), 'size').label, 'Larger');
  assert.equal(assessment(change(80, 100), 'build').label, 'Faster build');
  for (const ratio of [.96, 1, 1.04]) assert.equal(assessment(change(ratio, 1), 'runtime').label, 'About the same');
});
test('missing, failed and below-resolution comparisons never look favorable', () => {
  for (const v of [null, undefined, 0, NaN, Infinity]) {
    assert.equal(assessment(change(v, 1), 'runtime').label, 'Not comparable');
    assert.equal(assessment(change(1, v), 'runtime').tone, 'missing');
  }
  assert.equal(value({ status: 'timeout', runtime: { wallSeconds: 1 } }, metrics.runtime), null);
});
test('language areas use geometric means, keep the weakest workload and count missing values', async () => {
  const { areaSummary, familyCoverage } = await import('../../docs/capabilities/benchmarks/daily-model.mjs');
  const row = (name, area, wall, family) => ({ case: name, area, family, status: 'pass', runtime: { wallSeconds: wall } });
  const rows = [row('a', 'Strings', 2, 'strings'), row('b', 'Strings', .5, 'strings'), row('c', 'Hash', 3, 'hashes'), row('d', 'Hash', 1)];
  const controls = { a: 1, b: 1, c: 1 };
  const summary = areaSummary(rows, r => controls[r.case] ? { status: 'pass', runtime: { wallSeconds: controls[r.case] } } : undefined, metrics.runtime);
  const strings = summary.areas.find(area => area.area === 'Strings');
  assert.equal(strings.ratio, 1);
  assert.deepEqual(strings.weakest, { case: 'a', ratio: 2 });
  const hash = summary.areas.find(area => area.area === 'Hash');
  assert.ok(Math.abs(hash.ratio - 3) < 1e-12);
  assert.deepEqual([hash.compared, hash.missing, hash.family], [1, 1, 'hashes']);
  assert.equal(summary.overall.compared, 3);
  assert.ok(Math.abs(summary.overall.ratio - Math.cbrt(3)) < 1e-12);
  assert.equal(areaSummary([row('e', 'Empty', 1)], () => undefined, metrics.runtime).areas[0].ratio, null);
  const language = { features: [{ id: 'strings', title: 'Strings and UTF-8', cases: ['x', 'y'], pending: ['p'] }],
    cases: [{ id: 'x', gaps: [] }, { id: 'y', gaps: ['repl'] }] };
  assert.deepEqual(familyCoverage(language, 'strings'), { title: 'Strings and UTF-8', probes: 2, differing: 1, pending: 1 });
  assert.equal(familyCoverage(language, 'missing'), null);
});
