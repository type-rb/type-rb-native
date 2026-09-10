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
