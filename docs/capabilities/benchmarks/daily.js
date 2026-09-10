const metrics = {
  runtime: { label: 'Runtime', group: 'runtime', key: 'wallSeconds', unit: 's' },
  memory: { label: 'Peak RSS', group: 'runtime', key: 'memoryBytes', unit: 'bytes' },
  build: { label: 'Application build', group: 'build', key: 'wallSeconds', unit: 's' },
  size: { label: 'Stripped application size', key: 'strippedBytes', unit: 'bytes' },
};
const $ = id => document.getElementById(id);
const node = (tag, text, className) => {
  const element = document.createElement(tag);
  if (text !== undefined) element.textContent = text;
  if (className) element.className = className;
  return element;
};
const link = (label, url) => {
  const anchor = node('a', label);
  // Snapshot values never become markup or arbitrary navigations.
  if (typeof url === 'string' && /^https:\/\/github\.com\/type-rb\/type-rb-native\/actions\/runs\/\d+$/.test(url)) anchor.href = url;
  return anchor;
};
const value = (row, metric) => !row || row.status !== 'pass' ? null :
  (metric.group ? row[metric.group]?.[metric.key] : row[metric.key]);
const valid = number => typeof number === 'number' && Number.isFinite(number) && number > 0;
const format = (number, metric) => !valid(number) ? 'Unavailable' : metric.unit === 'bytes' ?
  `${(number / 1024).toLocaleString(undefined, { maximumFractionDigits: 1 })} KiB` :
  number < .1 ? `${(number * 1000).toFixed(2)} ms` : `${number.toFixed(3)} s`;
const rowFor = (snapshot, caseName, role) => snapshot.rows.find(row => row.case === caseName && row.role === role);
const change = (current, control) => valid(current) && valid(control) ? current / control - 1 : null;
const changeCell = difference => {
  if (difference === null) return node('td', 'Unavailable');
  const text = `${difference > 0 ? '+' : ''}${(difference * 100).toFixed(1)}%`;
  return node('td', text, Math.abs(difference) < .05 ? 'neutral' : difference < 0 ? 'better' : 'worse');
};
let state;

function renderCurrent() {
  const metric = metrics[$('metric').value];
  const snapshot = state.latest;
  $('result-body').replaceChildren();
  if (!snapshot) return;
  for (const row of snapshot.rows.filter(row => row.role === 'native')) {
    const tr = node('tr');
    const title = node('td', row.case);
    title.append(node('small', row.area));
    if (row.coverage) title.append(node('small', row.coverage));
    tr.append(title);
    const current = value(row, metric);
    const cell = node('td', row.status === 'pass' ? format(current, metric) : row.status);
    if (metric.group === 'runtime' && metric.key === 'wallSeconds' && row.runtime) {
      cell.append(node('small', `Range ${format(row.runtime.wallMin, metric)}–${format(row.runtime.wallMax, metric)}`));
    }
    tr.append(cell);
    const previous = snapshot.roles.previous.revision === snapshot.roles.native.revision ? null :
      value(rowFor(snapshot, row.case, 'previous'), metric);
    tr.append(changeCell(change(current, previous)));
    tr.append(changeCell(change(current, value(rowFor(snapshot, row.case, 'baseline'), metric))));
    const goValue = value(rowFor(snapshot, row.case, 'typerb-go'), metric);
    const goCell = node('td', format(goValue, metric));
    if (valid(current) && valid(goValue)) goCell.append(node('small', `${(current / goValue).toFixed(2)}× Go backend`));
    tr.append(goCell);
    $('result-body').append(tr);
  }
}

function renderHistory() {
  const caseName = $('case').value;
  const metric = metrics[$('metric').value];
  const history = state.history.filter(snapshot => snapshot.series === state.latest?.series);
  const points = [];
  $('history-body').replaceChildren();
  for (const snapshot of history.toReversed()) {
    const current = value(rowFor(snapshot, caseName, 'native'), metric);
    const baseline = value(rowFor(snapshot, caseName, 'baseline'), metric);
    const ratio = change(current, baseline);
    const tr = node('tr');
    tr.append(node('td', new Date(snapshot.at).toLocaleString()), node('td', snapshot.revision.slice(0, 8)),
      node('td', format(current, metric)), changeCell(ratio));
    const evidence = node('td');
    evidence.append(link('Measurement', snapshot.runUrl));
    tr.append(evidence);
    $('history-body').append(tr);
    if (ratio !== null) points.unshift(ratio * 100);
  }
  const svg = $('trend-chart');
  svg.replaceChildren();
  $('trend-context').textContent = '';
  if (points.length < 2) {
    svg.hidden = true;
    return;
  }
  svg.hidden = false;
  const low = Math.min(0, ...points) - 5, high = Math.max(0, ...points) + 5;
  const xy = points.map((point, index) => `${30 + index * 640 / (points.length - 1)},${230 - (point - low) * 200 / (high - low)}`);
  const line = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
  line.setAttribute('points', xy.join(' '));
  line.setAttribute('fill', 'none'); line.setAttribute('stroke', '#2872b5'); line.setAttribute('stroke-width', '3');
  svg.append(line);
  $('trend-context').textContent = `Oldest to newest · same-host baseline changes range from ${Math.min(...points).toFixed(1)}% to ${Math.max(...points).toFixed(1)}%. Exact values below.`;
}

async function main() {
  const response = await fetch('./daily-state.json', { cache: 'no-store' });
  if (!response.ok) throw new Error('Could not load the last daily measurement.');
  state = await response.json();
  if (state.schemaVersion !== 1 || !Array.isArray(state.history)) throw new Error('Unsupported measurement data.');
  const snapshot = state.latest;
  $('status').replaceChildren();
  if (snapshot) {
    $('status').append(node('strong', `Measured ${new Date(snapshot.at).toLocaleString()} · ${snapshot.revision.slice(0, 8)}`));
    $('status').append(node('div', state.pendingChanges ? 'Performance changes are waiting for the next daily measurement.' : 'No unmeasured performance changes at the last update.'));
    $('evidence').replaceChildren(link('Open measurement and raw evidence', snapshot.runUrl));
    $('context').textContent = `${snapshot.platform} · one logical CPU · ${snapshot.samples} retained runtime samples · ${snapshot.buildSamples} retained build samples. Lower values are better.`;
    $('identity').textContent = `Frozen Native: ${snapshot.roles.baseline.revision.slice(0, 8)} · Previous Native: ${snapshot.roles.previous.revision.slice(0, 8)} · TypeRB Go: ${snapshot.roles['typerb-go'].revision.slice(0, 8)}`;
  } else {
    $('status').append(node('strong', 'First daily measurement pending'));
    $('status').append(node('div', 'The detailed comparison remains available. Daily values will appear after the first completed run.'));
    $('results').hidden = true;
  }
  const attempt = state.attempt;
  if (attempt && ['infrastructure-failure', 'measured-with-failures', 'running'].includes(attempt.status)) {
    $('status').classList.add('warning');
    $('status').append(node('div', `Latest attempt: ${attempt.status} · ${attempt.revision.slice(0, 8)}. Failed or missing measurements are not passing results.`));
    $('status').append(link('Inspect latest attempt', attempt.runUrl));
  }
  for (const [key, metric] of Object.entries(metrics)) {
    const option = node('option', metric.label); option.value = key; $('metric').append(option);
  }
  const history = document.body.dataset.view === 'history';
  if (history) {
    for (const row of snapshot?.rows.filter(row => row.role === 'native') ?? []) {
      const option = node('option', row.case); option.value = row.case; $('case').append(option);
    }
    $('case').addEventListener('change', renderHistory);
  }
  const render = history ? renderHistory : renderCurrent;
  $('metric').addEventListener('change', render);
  render();
}
main().catch(error => { $('status').textContent = error.message; $('status').classList.add('warning'); });
