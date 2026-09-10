export const metrics = {
  runtime: { label: 'Runtime', group: 'runtime', key: 'wallSeconds', unit: 's', quantity: 'time', description: 'Time to finish the workload, including process launch. Less time is better.' },
  memory: { label: 'Memory', group: 'runtime', key: 'memoryBytes', unit: 'bytes', quantity: 'memory', description: 'Peak resident memory (RSS). Less memory is better; this is separate from runtime speed.' },
  build: { label: 'Build time', group: 'build', key: 'wallSeconds', unit: 's', quantity: 'build time', description: 'Application build time with clean outputs and a warm Go cache. Less time is better.' },
  size: { label: 'Binary size', key: 'strippedBytes', unit: 'bytes', quantity: 'space', description: 'Stripped application size. Smaller is better; compiler and shared system libraries are outside this value.' },
};
export const comparisons = { 'pure-go': 'Pure Go', 'typerb-go': 'TypeRB Go', previous: 'Previous Native', baseline: 'Frozen Native' };
export const value = (row, metric) => !row || row.status !== 'pass' ? null :
  (metric.group ? row[metric.group]?.[metric.key] : row[metric.key]);
export const valid = number => typeof number === 'number' && Number.isFinite(number) && number > 0;
export const change = (current, control) => valid(current) && valid(control) ? current / control - 1 : null;
export function assessment(difference, metricKey) {
  if (difference === null || !Number.isFinite(difference)) return { tone: 'missing', label: 'Not comparable', detail: '' };
  const tone = Math.abs(difference) < .05 ? 'neutral' : difference < 0 ? 'better' : 'worse';
  const words = { runtime: ['Faster', 'Slower'], memory: ['Less memory', 'More memory'], build: ['Faster build', 'Slower build'], size: ['Smaller', 'Larger'] }[metricKey];
  return { tone, label: tone === 'neutral' ? 'About the same' : words[tone === 'better' ? 0 : 1],
    detail: `${Math.abs(difference * 100).toFixed(1)}% ${difference <= 0 ? 'less' : 'more'} ${metrics[metricKey].quantity}` };
}
