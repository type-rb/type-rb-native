import { readFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { benchmarkData } from '../docs/capabilities/benchmarks/data.js';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const failures = [];
const fail = (message) => failures.push(message);

if (benchmarkData.schemaVersion !== 1) fail('unsupported benchmark data schema');
if (benchmarkData.runtime.records.length !== 42) fail('expected 42 runtime median rows');
if (benchmarkData.build.records.length !== 6) fail('expected 6 build median rows');
if (benchmarkData.runtime.retained !== 462) fail('expected 462 retained runtime samples');
if (benchmarkData.build.retained !== 66) fail('expected 66 retained build samples');

for (const row of [...benchmarkData.runtime.records, ...benchmarkData.build.records]) {
  if (row.status !== 'pass') fail(`${row.case}/${row.candidate} does not pass`);
  if (row.retained !== row.passed) fail(`${row.case}/${row.candidate} has missing samples`);
  for (const field of ['wallSeconds', 'cpuSeconds', 'memoryBytes']) {
    if (!Number.isFinite(row[field]) || row[field] <= 0) fail(`${row.case}/${row.candidate} has invalid ${field}`);
  }
  if (!row.evidence.startsWith('https://github.com/type-rb/type-rb-native/blob/main/results/')) {
    fail(`${row.case}/${row.candidate} has a non-public evidence URL`);
  }
}

const html = await readFile(resolve(root, 'docs/capabilities/benchmarks/index.html'), 'utf8');
for (const required of ['TypeRB Native Benchmarks', 'id="runtime-chart"', 'id="build-grid"', './app.js']) {
  if (!html.includes(required)) fail(`benchmark page is missing ${required}`);
}

if (failures.length > 0) {
  failures.forEach((message) => console.error(`FAIL ${message}`));
  process.exitCode = 1;
} else {
  console.log('PASS benchmark Pages structure and evidence');
}
