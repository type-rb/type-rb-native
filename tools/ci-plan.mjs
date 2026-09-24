import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { pathToFileURL } from 'node:url';
import { appendFileSync } from 'node:fs';

const staticDocumentationTools = new Set([
  'tools/capability-map-check.mjs',
  'tools/benchmark-pages-data.mjs',
  'tools/benchmark-pages-check.mjs',
  'tools/result_archive.py',
  'tools/result_archive_test.py',
  'tools/evidence_bundle.py',
  'tools/evidence_bundle_test.py',
  '.github/workflows/documentation.yml',
  '.github/workflows/capability-map-pages.yml',
]);
const documentation = path => staticDocumentationTools.has(path) || path.endsWith('.md') ||
  ['.agents/', 'docs/', 'results/'].some(prefix => path.startsWith(prefix));
// These exact files are exercised by the unconditional planning job. They do
// not build or execute the compiler. Execution workflows/controllers are not
// included: changing those still needs the authorities they orchestrate.
const planningTools = new Set(['tools/ci-plan.mjs', 'tools/ci-plan-test.mjs']);
// Only these synthetic tests can use tooling-only validation. Their production
// controllers and unknown neighboring paths still require the full code lane.
// Tests with a second Linux authority retain it through planning or quick.
export const quickToolingTests = new Set([
  'tools/compiler-project-test.sh',
  'tools/compiler-cost-test.sh',
  'tools/native-mir-transition-policy-test.sh',
]);
export const toolingTests = new Set([
  ...quickToolingTests,
  'tools/ci-run-suites-test.mjs',
  'tools/recovery-workspace-test.mjs',
  'tools/bootstrap-seed-manifest-test.sh',
  'tools/bootstrap-seed-arguments-test.sh',
  'tools/measure-command-test.py',
  'tools/benchmarksgame-formal/runtime-controller-test.sh',
  'tools/native-runtime-ab/runtime-controller-test.sh',
  'tools/benchmarksgame-build-formal/build-controller-test.sh',
  'tools/runtime-memory-soak/analyze-rss-test.sh',
  'tools/runtime-worker-soak/analyze-gc-trace-test.sh',
  'tools/runtime-worker-soak/analyze-process-series-test.sh',
  'tools/recovery_stage_test.py',
]);
// The tooling job discovers this daily measurement suite. Compiler and CLI
// validation do not execute these controllers, even in the complete lane.
export const dailyMeasurementInputs = new Set([
  'tools/daily-performance/measure.py',
  'tools/daily-performance/state.py',
  'tools/daily-performance/test_daily.py',
]);
// These existing test modules are excluded from ordinary compiler builds.
// Keep complete correctness validation; only unchanged-binary measurements
// are unnecessary. New test paths, configurations and fixtures default to code.
export const compilerTestInputs = new Set([
  'compiler/src/checked_binding_test.trb',
  'compiler/src/checked_program_test.trb',
  'compiler/src/compiler_test.trb',
  'compiler/src/literals_test.trb',
  'compiler/src/mir_test.trb',
  'compiler/src/hash_test.trb',
  'compiler/src/parser_test.trb',
  'compiler/src/project_config_test.trb',
  'compiler/src/qbe_output_test.trb',
  'compiler/src/resolution_test.trb',
  'compiler/src/state_test.trb',
]);
// These adapters are outside the ordinary compiler source closure. Core edits
// mixed with them restore all core authorities; new paths default to code.
export const cliInputs = new Set([
  'trbn',
  'tools/build-native.sh',
  'tools/check-native-cli.sh',
  'tools/native-cli-test.py',
  'tools/native-enum-test.py',
  'tools/native-callable-test.py',
  'tools/native-repl-flow-test.py',
  'tools/native-hash-test.py',
  'tools/native-cli-key-test.py',
  'tools/native-puts-test.py',
  'tools/native-diagnostics-test.py',
  'tools/native-interpolation-test.py',
  'tools/native-bootstrap-test.py',
  'tools/native-repl-editor-test.py',
  'tools/native-language-coverage.py',
  'tools/native-language-coverage-test.py',
  'tools/native-language-cases.json',
  'tools/repl-test-requirements.txt',
  'compiler/cli/diagnostics.trb',
  'compiler/cli/host.trb',
  'compiler/cli/main.trb',
  'compiler/cli/repl.trb',
  'compiler/cli/repl_check.trb',
  'compiler/cli/repl_defaults.trb',
  'compiler/cli/repl_project.trb',
  'compiler/cli/repl_editor.trb',
  'compiler/cli/repl_eval.trb',
  'compiler/cli/repl_history.trb',
  'compiler/cli/repl_syntax.trb',
  'compiler/cli/repl_values.trb',
  'compiler/cli/repl_model.trb',
  'compiler/cli/repl_callables.trb',
  'compiler/cli/repl_types.trb',
  'compiler/cli/repl_hash.trb',
]);

// A tiered PR gate integrates ordinary compiler, CLI and conformance edits with
// the pre-merge lanes; main then runs the complete lanes. Cache and bootstrap
// inputs, recovery sources, workflows and unknown paths still need the complete
// lanes before merge because only those lanes execute them.
const completeCliInputs = new Set(['trbn', 'tools/build-native.sh', 'tools/native-bootstrap-test.py']);
const pullRequestLane = path =>
  ['compiler/src/', 'compiler/cli/', 'compiler/conformance/'].some(prefix => path.startsWith(prefix)) ||
  ['compiler/trbconfig.jsonc', 'src/compiler_recovery_layout.trb', 'src/compiler_recovery_mutations.trb',
    'tools/check-conformance-sources.py'].includes(path) ||
  (cliInputs.has(path) && !completeCliInputs.has(path)) || toolingTests.has(path);
export const gates = ['complete', 'tiered'];

export function classify(paths, draft, costMode = 'strict', gate = 'complete') {
  if (!['strict', 'mir-migration'].includes(costMode)) throw new Error('Invalid compiler cost mode');
  if (!gates.includes(gate)) throw new Error('Invalid CI gate');
  const executable = paths.filter(path => !documentation(path) && !planningTools.has(path));
  const toolingInput = path => toolingTests.has(path) || dailyMeasurementInputs.has(path);
  const codePaths = executable.filter(path => !toolingInput(path) && !cliInputs.has(path));
  const code = codePaths.length > 0;
  const routing = paths.some(path => path.startsWith('.github/workflows/') || path.startsWith('tools/ci-'));
  const compiler = codePaths.some(path => path.startsWith('compiler/')) &&
    !codePaths.every(path => compilerTestInputs.has(path));
  const policy = codePaths.some(path => path.startsWith('tools/native-mir-') ||
    path.startsWith('tools/compiler-project') || path.startsWith('tools/compiler-cost'));
  const performance = code && costMode === 'strict' && (routing || policy || compiler);
  const memory = code && (routing || compiler || policy || codePaths.some(path => path.startsWith('tools/runtime-worker-soak/')));
  const cli = code || executable.some(path => cliInputs.has(path));
  const complete = cli && (gate === 'complete' || executable.some(path => !pullRequestLane(path)));
  return {
    code, quick: code || executable.some(path => cliInputs.has(path) || quickToolingTests.has(path)),
    documentation: routing || paths.some(documentation),
    memory, performance: performance && complete, draft,
    tooling: code || executable.some(toolingInput),
    cli, complete,
  };
}

export function acceptance(needs) {
  if (needs.plan?.result !== 'success') return ['CI planning did not succeed'];
  const plan = needs.plan.outputs;
  if (!plan || ['code', 'documentation', 'memory', 'performance', 'draft', 'tooling', 'cli', 'quick', 'complete']
    .some(key => !['true', 'false'].includes(plan[key]))) {
    return ['CI planning outputs are missing or malformed'];
  }
  if ((plan.code === 'true' || plan.cli === 'true') && plan.quick !== 'true') {
    return ['Code and CLI validation require quick feedback'];
  }
  const draft = plan.draft === 'true';
  const required = {
    quick: plan.quick, documentation: plan.documentation,
    native: draft || plan.complete === 'false' ? 'false' : plan.code, targets: draft ? 'false' : plan.code,
    memory: draft ? 'false' : plan.memory, performance: draft ? 'false' : plan.performance,
    tooling: plan.tooling, cli: draft ? 'false' : plan.cli,
  };
  return Object.entries(required).flatMap(([job, enabled]) => {
    const expected = enabled === 'true' ? 'success' : 'skipped';
    return needs[job]?.result === expected ? [] :
      [`${job}: expected ${expected}, got ${needs[job]?.result ?? 'missing'}`];
  });
}

// Main validation owns the complete lanes after a tiered PR merge. Its planner
// compares against the last fully validated main commit, not the push delta.
export function mainAcceptance(needs) {
  if (needs.plan?.result !== 'success') return ['Main planning did not succeed'];
  const plan = needs.plan.outputs;
  if (!plan || ['code', 'documentation', 'memory', 'tooling', 'cli']
    .some(key => !['true', 'false'].includes(plan[key]))) {
    return ['Main planning outputs are missing or malformed'];
  }
  const required = {
    documentation: plan.documentation, tooling: plan.tooling, memory: plan.memory,
    native: plan.code, targets: plan.code, cli: plan.cli,
  };
  return Object.entries(required).flatMap(([job, enabled]) => {
    const expected = enabled === 'true' ? 'success' : 'skipped';
    return needs[job]?.result === expected ? [] :
      [`${job}: expected ${expected}, got ${needs[job]?.result ?? 'missing'}`];
  });
}

export async function changedPaths(base, head, cwd, direct = false) {
  // Stream the NUL-delimited list: full evidence snapshots can exceed the
  // synchronous child-process buffer, and truncation could hide a code change.
  const child = spawn('git', ['diff', '--no-renames', '--name-only', '-z',
    `${base}${direct ? '..' : '...'}${head}`, '--'], { cwd, stdio: ['ignore', 'pipe', 'inherit'] });
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
  if (process.argv[2] === 'accept' || process.argv[2] === 'accept-main') {
    const needs = JSON.parse(process.env.NEEDS_JSON ?? '{}');
    const errors = process.argv[2] === 'accept' ? acceptance(needs) : mainAcceptance(needs);
    for (const error of errors) console.error(error);
    const outputs = needs.plan?.outputs ?? {};
    const message = errors.length || process.argv[2] !== 'accept' ? '' :
      outputs.draft === 'true' ? 'Draft feedback only: complete validation runs when the PR is marked ready.' :
      outputs.complete === 'false' && outputs.cli === 'true' ?
        'Pre-merge lanes passed: Native recovery, CLI cache and arm64 regression run on main after merge.' : '';
    if (message) {
      console.log(message);
      if (process.env.GITHUB_STEP_SUMMARY) appendFileSync(process.env.GITHUB_STEP_SUMMARY,
        `### ${message}\n`);
    }
    process.exitCode = errors.length ? 1 : 0;
  } else {
    const [base, head, draft, mode] = process.argv.slice(2);
    if (!/^[a-f0-9]{40}$/.test(base ?? '') ||
        !/^[a-f0-9]{40}$/.test(head ?? '') || !['true', 'false'].includes(draft) || (mode !== undefined && mode !== 'push') || process.argv.length > 6) {
      throw new Error('Usage: ci-plan.mjs BASE_SHA HEAD_SHA true|false [push]');
    }
    // Include both sides of renames, and preserve arbitrary path characters.
    const paths = await changedPaths(base, head, undefined, mode === 'push');
    // Main always plans the complete lanes; only PRs may use the tiered gate.
    const gate = mode === 'push' ? 'complete' : process.env.NATIVE_CI_GATE ?? 'complete';
    for (const [key, value] of Object.entries(classify(paths, draft === 'true',
      process.env.NATIVE_MIR_COST_MODE ?? 'strict', gate))) {
      console.log(`${key}=${value}`);
    }
  }
}
