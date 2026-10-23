export const families = {
  'json-document': { title: 'JSON document width', description: 'Long ASCII, Unicode and escaped strings, plus wide arrays and objects; count measures units within one document.' },
  'json-transform': { title: 'JSON transformation', description: 'Parse, transform and serialize Unicode documents, including invalid inputs.' },
  'log-pipeline': { title: 'Log processing', description: 'Parse and aggregate valid records and mixed malformed input.' },
  worker: { title: 'Persistent worker', description: 'Repeated batches with retained state; process throughput includes setup.' },
  hash: { title: 'Hash lookup', description: 'Working-set sizes with hits and predominantly missing keys.' },
  strings: { title: 'String processing', description: 'Short and long Unicode strings across input sizes.' },
  arrays: { title: 'Array sorting', description: 'Random, sorted, reversed and duplicate-heavy inputs.' },
  allocation: { title: 'Allocation and lifetime', description: 'Short-lived and retained objects across working-set sizes.' },
};
export const metrics = {
  wallSeconds: { label: 'Runtime', unit: 's', description: 'Fresh-process wall time, including setup and output. Less is better.', better: 'Faster', worse: 'Slower' },
  cpuSeconds: { label: 'CPU time', unit: 's', description: 'CPU time per process. Zero or unavailable observations are not comparable.', better: 'Less CPU', worse: 'More CPU' },
  peakRssBytes: { label: 'Peak RSS', unit: 'bytes', description: 'Peak resident memory of each process. Less is better.', better: 'Less memory', worse: 'More memory' },
  unitsPerSecond: { label: 'Throughput', unit: 'items/s', description: 'Items across all batches divided by process wall time. Includes setup and output; higher is better.', higher: true, better: 'Higher throughput', worse: 'Lower throughput' },
};
export const roles = { 'pure-go': 'Pure Go', 'typerb-go': 'TypeRB Go' };
export const positive = value => typeof value === 'number' && Number.isFinite(value) && value > 0;
export const sameInput = (a, b) => a && b && ['id', 'workload', 'count', 'variant', 'batches', 'size'].every(key => a[key] === b[key]);

export const invalidRss = snapshot => snapshot?.platform?.startsWith('Linux') && snapshot.environment?.peakRssMethod !== 'gnu-time-child-v1';
export function metricValue(snapshot, row, role, metric) {
  if (metric === 'peakRssBytes' && invalidRss(snapshot)) return undefined;
  return row?.summaries[role]?.[metric];
}

export function resultFor(snapshot, input) {
  if (!sameInput(snapshot?.inputs.find(item => item.id === input.id), input)) return undefined;
  return snapshot.rows.find(row => row.case === input.id);
}

export function verdict(current, control, key) {
  if (!positive(current) || !positive(control)) return { tone: 'missing', label: 'Not comparable', detail: '' };
  const difference = current / control - 1, metric = metrics[key];
  const tone = Math.abs(difference) < .05 ? 'neutral' : (metric.higher ? difference > 0 : difference < 0) ? 'better' : 'worse';
  return { tone, label: tone === 'neutral' ? 'About the same' : metric[tone],
    detail: `${Math.abs(difference * 100).toFixed(1)}% ${difference < 0 ? 'less' : 'more'}` };
}

export function groupResults(cases, snapshot, role, metric) {
  return Object.entries(families).map(([id, family]) => {
    const inputs = cases.filter(input => input.workload === id);
    const counts = { better: 0, worse: 0, neutral: 0, missing: 0 };
    for (const input of inputs) {
      const row = resultFor(snapshot, input);
      counts[verdict(metricValue(snapshot, row, 'native', metric), metricValue(snapshot, row, role, metric), metric).tone]++;
    }
    return { id, ...family, inputs, counts };
  });
}
