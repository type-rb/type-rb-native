import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { pathToFileURL } from 'node:url';

const documentation = path => path.endsWith('.md') ||
  ['.agents/', 'docs/', 'results/'].some(prefix => path.startsWith(prefix));

export function classify(paths, draft) {
  const code = paths.some(path => !documentation(path));
  const routing = paths.some(path => path.startsWith('.github/workflows/') ||
    path.startsWith('tools/ci-'));
  const compiler = paths.some(path => path.startsWith('compiler/gate4/') &&
    !documentation(path));
  const policy = paths.some(path => path.startsWith('tools/native-mir-'));
  const performance = code && (routing || compiler || policy);
  const memory = code && (performance || paths.some(path =>
    path.startsWith('tools/runtime-worker-soak/')));
  return {
    code, documentation: routing || paths.some(documentation),
    memory, performance, draft,
  };
}

export function acceptance(needs) {
  if (needs.plan?.result !== 'success') return ['CI planning did not succeed'];
  const plan = needs.plan.outputs;
  if (!plan || ['code', 'documentation', 'memory', 'performance', 'draft']
    .some(key => !['true', 'false'].includes(plan[key]))) {
    return ['CI planning outputs are missing or malformed'];
  }
  if (plan.draft === 'true') return ['Draft feedback is not merge acceptance'];
  const required = {
    quick: plan.code, documentation: plan.documentation,
    native: plan.code, targets: plan.code,
    memory: plan.memory, performance: plan.performance,
  };
  return Object.entries(required).flatMap(([job, enabled]) => {
    const expected = enabled === 'true' ? 'success' : 'skipped';
    return needs[job]?.result === expected ? [] :
      [`${job}: expected ${expected}, got ${needs[job]?.result ?? 'missing'}`];
  });
}

export async function changedPaths(base, head, cwd) {
  // Stream the NUL-delimited list: full evidence snapshots can exceed the
  // synchronous child-process buffer, and truncation could hide a code change.
  const child = spawn('git', ['diff', '--no-renames', '--name-only', '-z',
    `${base}...${head}`, '--'], { cwd, stdio: ['ignore', 'pipe', 'inherit'] });
  const completion = once(child, 'close');
  child.stdout.setEncoding('utf8');
  const paths = [];
  const read = async () => {
    let pending = '';
    for await (const chunk of child.stdout) {
      const parts = (pending + chunk).split('\0');
      pending = parts.pop();
      paths.push(...parts);
    }
    if (pending !== '') throw new Error('Git path list is not NUL-terminated');
  };
  const [, [status, signal]] = await Promise.all([read(), completion]);
  if (status !== 0) throw new Error(`Git path inventory failed: ${signal ?? status}`);
  return paths;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  if (process.argv[2] === 'accept') {
    const errors = acceptance(JSON.parse(process.env.NEEDS_JSON ?? '{}'));
    for (const error of errors) console.error(error);
    process.exitCode = errors.length ? 1 : 0;
  } else {
    const [base, head, draft] = process.argv.slice(2);
    if (!/^[a-f0-9]{40}$/.test(base ?? '') ||
        !/^[a-f0-9]{40}$/.test(head ?? '') || !['true', 'false'].includes(draft)) {
      throw new Error('Usage: ci-plan.mjs BASE_SHA HEAD_SHA true|false');
    }
    // Include both sides of renames, and preserve arbitrary path characters.
    const paths = await changedPaths(base, head);
    for (const [key, value] of Object.entries(classify(paths, draft === 'true'))) {
      console.log(`${key}=${value}`);
    }
  }
}
