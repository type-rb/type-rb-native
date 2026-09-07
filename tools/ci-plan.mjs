import { execFileSync, spawn } from 'node:child_process';
import { once } from 'node:events';
import { pathToFileURL } from 'node:url';

const staticDocumentationTools = new Set([
  'tools/capability-map-check.mjs',
  'tools/benchmark-pages-data.mjs',
  'tools/benchmark-pages-check.mjs',
  'tools/result_archive.py',
  'tools/result_archive_test.py',
  '.github/workflows/documentation.yml',
]);
const documentation = path => staticDocumentationTools.has(path) || path.endsWith('.md') ||
  ['.agents/', 'docs/', 'results/'].some(prefix => path.startsWith(prefix));
// These exact files are exercised by the unconditional planning job. They do
// not build or execute the compiler. Execution workflows/controllers are not
// included: changing those still needs the authorities they orchestrate.
const planningTools = new Set(['tools/ci-plan.mjs', 'tools/ci-plan-test.mjs']);
export const lightweightPushPaths = [...staticDocumentationTools, ...planningTools];
const nativeWorkflow = '.github/workflows/gate-zero.yml';

export function nativePushFilterOnly(before, after) {
  // Only remove exact, already-lightweight entries from the push ignore block.
  // Compare everything else byte-for-byte, including jobs, permissions and
  // workflow_call. Unknown patterns or edits elsewhere keep full validation.
  const normalize = text => {
    const match = text.match(/^([\s\S]*?    paths-ignore:\n)((?:      - [^\n]+\n)+)([\s\S]*)$/);
    if (!match || !match[1].includes('\non:\n  workflow_call:\n  push:\n') ||
        !match[3].startsWith('\npermissions:\n')) return null;
    const ignored = new Set(lightweightPushPaths.map(path => `      - ${path}`));
    return match[1] + match[2].split('\n').filter(line => !ignored.has(line)).join('\n') + match[3];
  };
  const normalized = normalize(before);
  return normalized !== null && normalized === normalize(after);
}

export function classify(paths, draft, pushFilterOnly = false) {
  const code = paths.some(path => !documentation(path) && !planningTools.has(path) &&
    !(pushFilterOnly && path === nativeWorkflow));
  const routing = paths.some(path => path.startsWith('.github/workflows/') ||
    path.startsWith('tools/ci-'));
  const compiler = paths.some(path => path.startsWith('compiler/') &&
    !documentation(path));
  const policy = paths.some(path => path.startsWith('tools/native-mir-') ||
    path.startsWith('tools/compiler-project'));
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
    let pushFilterOnly = false;
    if (paths.includes(nativeWorkflow)) {
      try {
        const ancestor = execFileSync('git', ['merge-base', base, head], { encoding: 'utf8' }).trim();
        const source = revision => execFileSync('git', ['show', `${revision}:${nativeWorkflow}`],
          { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
        pushFilterOnly = nativePushFilterOnly(source(ancestor), source(head));
      } catch {
        // Missing, new, unreadable or oversized workflow: require full checks.
      }
    }
    for (const [key, value] of Object.entries(classify(paths, draft === 'true', pushFilterOnly))) {
      console.log(`${key}=${value}`);
    }
  }
}
