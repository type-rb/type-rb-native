import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync, renameSync, rmSync, symlinkSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { acceptance, changedPaths, classify } from './ci-plan.mjs';

function results(plan) {
  return {
    plan: { result: 'success', outputs: Object.fromEntries(
      Object.entries(plan).map(([key, value]) => [key, String(value)])) },
    ...Object.fromEntries(Object.entries({ quick: plan.code,
      documentation: plan.documentation, native: plan.code, targets: plan.code,
      memory: plan.memory, performance: plan.performance,
    }).map(([key, value]) => [key, { result: value ? 'success' : 'skipped' }])),
  };
}

test('runtime A/B remains manual with separate frozen optimization contracts', () => {
  const workflow = readFileSync(new URL('../.github/workflows/native-runtime-ab.yml', import.meta.url), 'utf8');
  const entry = readFileSync(new URL('../.github/workflows/pull-request.yml', import.meta.url), 'utf8');
  assert(workflow.includes('  workflow_dispatch:\n'));
  assert(!workflow.includes('  pull_request:') && !workflow.includes('  workflow_call:'));
  assert(!entry.includes('native-runtime-ab.yml'), 'manual experiments must not add an automatic PR job');
  assert(workflow.includes('default: derived-loop-index'));
  assert.match(workflow, /derived-loop-index\)\n\s+BASELINE_REVISION=aad4954c66ae394a5edb836b20498e5a60b769bd/);
  assert.match(workflow, /checked-boolean-branches\)\n\s+BASELINE_REVISION=6f7e3ba10623d40b5b0f7e6cc03b732125607795/);
  assert.match(workflow, /array-loop-bounds\)\n\s+BASELINE_REVISION=1afd60c2c7257ed34fd2a2aa70cb8b9164433009/);
  assert(workflow.includes('build_cost_authority=exact-head-interleaved-compactness-frozen-1afd60c2'));
  assert(workflow.includes('*) exit 64 ;;'), 'unknown contracts must not materialize a baseline');
  assert(workflow.includes('native_compiler_project_directory "$RUNNER_TEMP/baseline-source"'));
  assert(!workflow.includes('baseline-source/compiler/gate4/'));
  assert(workflow.includes('compiler_limit=255000'), 'historical absolute limit remains');
  assert(workflow.includes('compiler_limit=$(native_mir_target_compiler_limit linux-arm64-v0)'));
  assert(workflow.includes('compiler_text_bytes strict-shrink'));
  assert(workflow.includes('compiler_qbe_bytes strict-shrink'));
  assert(workflow.includes('build_cost_authority=normal-exact-head-PR-interleaved-compactness'));
  assert(workflow.includes('if test "$NATIVE_RUNTIME_AB_CONTRACT" = derived-loop-index; then\n            for stage'));
});

test('retained loop CSV accepts original CRLF but rejects other whitespace defects', () => {
  const attributes = readFileSync(new URL('../results/2026-09-06-mir-loop-bounds-diagnostic-darwin-arm64/.gitattributes', import.meta.url), 'utf8');
  const directory = mkdtempSync(join(tmpdir(), 'native-csv-whitespace-test-'));
  const options = { cwd: directory, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] };
  try {
    execFileSync('git', ['init', '-q'], options);
    writeFileSync(join(directory, '.gitattributes'), attributes);
    mkdirSync(join(directory, 'observations'));
    const csv = join(directory, 'observations/raw.csv');
    const command = ['-c', 'core.whitespace=blank-at-eol,blank-at-eof,space-before-tab',
      'diff', '--cached', '--check'];
    writeFileSync(csv, 'metric,value\r\nwall,1.25\r\n');
    execFileSync('git', ['-c', 'core.autocrlf=false', 'add', 'observations/raw.csv'], options);
    assert.equal(execFileSync('git', command, options), '');
    for (const invalid of ['metric,value \r\n', 'metric,value\r\n\r\n']) {
      writeFileSync(csv, invalid);
      execFileSync('git', ['-c', 'core.autocrlf=false', 'add', 'observations/raw.csv'], options);
      assert.throws(() => execFileSync('git', command, options),
        error => error.status !== 0 && /whitespace|blank line/.test(error.stdout));
    }
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
});

test('manual optimization compactness loads its dependencies in a fresh step shell', () => {
  const root = fileURLToPath(new URL('../', import.meta.url));
  const workflow = readFileSync(new URL('../.github/workflows/native-runtime-ab.yml', import.meta.url), 'utf8');
  const setup = workflow.match(/          compiler_maximum=1\.01\n[\s\S]*?(?=            for role in baseline candidate; do)/)?.[0];
  assert(setup, 'the actual compactness setup must be exercised');
  const directory = mkdtempSync(join(tmpdir(), 'native-runtime-policy-test-'));
  try {
    symlinkSync(root, join(directory, 'baseline-source'), 'dir');
    const script = `set -eu\nevidence="$RUNNER_TEMP"\n${setup}\nfi\nprintf '%s %s\\n' "$compiler_maximum" "$compiler_limit"\n`;
    const options = { cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], env: {
      PATH: process.env.PATH,
      GITHUB_WORKSPACE: root,
      RUNNER_TEMP: directory,
      NATIVE_RUNTIME_AB_CONTRACT: 'checked-boolean-branches',
    } };
    for (const [contract, expected] of [
      ['checked-boolean-branches', '1.00 317000'],
      ['array-loop-bounds', '1.05 317000'],
    ]) {
      options.env.NATIVE_RUNTIME_AB_CONTRACT = contract;
      for (const shell of ['/bin/sh', '/bin/bash']) {
        assert.equal(execFileSync(shell, ['-c', script], options).trim(), expected);
        // Remove every occurrence so the selected branch loses its dependency.
        // A previous workflow step's functions do not survive in a new shell.
        for (const [helper, missingFunction] of [
          ['compiler-project.sh', /native_compiler_project_directory/],
          ['native-mir-transition-policy.sh', /native_mir_transition_markers_valid/],
        ]) {
          assert.throws(() => execFileSync(shell, ['-c', script.replaceAll(
            `. tools/${helper}`, ': missing-helper')], options),
          error => error.status !== 0 && missingFunction.test(error.stderr));
        }
      }
    }
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
});

test('compatibility checks precede matrix fan-out and remain in standalone validation', () => {
  const workflow = readFileSync(new URL('../.github/workflows/pull-request.yml', import.meta.url), 'utf8');
  const standalone = readFileSync(new URL('../.github/workflows/gate-zero.yml', import.meta.url), 'utf8');
  const quick = workflow.match(/^  quick:\n([\s\S]*?)(?=^  documentation:)/m)?.[1];
  assert(quick, 'quick stage must exist');
  const build = quick.indexOf('go build -C .type-rb');
  const formatting = quick.indexOf('Check formatting and core types');
  for (const command of [
    'python3 -m unittest tools/compatibility_manifest_test.py',
    'python3 tools/compatibility_manifest.py --reference-trb "$RUNNER_TEMP/trb"',
  ]) {
    const check = quick.indexOf(command);
    assert(build >= 0 && check > build && formatting > check,
      `${command} must run after reference build and before later quick checks`);
    assert(standalone.includes(command), 'standalone validation must retain the same check');
  }
  for (const job of ['native', 'targets', 'memory']) {
    assert(workflow.includes(`  ${job}:\n    needs: [plan, quick]\n`),
      `${job} must wait for successful quick feedback`);
  }
});

test('documentation-only PRs do not run compiler or performance matrices', () => {
  const plan = classify(['README.md', 'docs/index.html', 'results/a.json',
    'tools/native-mir-guarded-add/README.md'], false);
  assert.deepEqual(plan, { code: false, documentation: true,
    memory: false, performance: false, draft: false });
  assert.deepEqual(acceptance(results(plan)), []);
});
test('compiler, conformance and CI-routing changes retain the full authority', () => {
  for (const path of ['compiler/src/storage.trb', 'compiler/trbconfig.jsonc',
    'compiler/conformance/runtime-invalid/new.trb',
    'tools/compiler-project.sh', 'tools/compiler-project-test.sh',
    'compiler/gate4/src/storage.trb',
    'compiler/gate4/conformance/runtime-invalid/new.trb',
    '.github/workflows/pull-request.yml', 'tools/ci-plan.mjs',
    'tools/native-mir-transition-policy.sh']) {
    const plan = classify([path], false);
    assert.equal(plan.code, true);
    assert.equal(plan.memory, true);
    assert.equal(plan.performance, true);
    assert.deepEqual(acceptance(results(plan)), []);
  }
});
test('static Pages generators use documentation checks, not compiler matrices', () => {
  for (const tool of ['tools/capability-map-check.mjs',
    'tools/benchmark-pages-data.mjs', 'tools/benchmark-pages-check.mjs']) {
    const plan = classify([tool, 'docs/capabilities/benchmarks/data.js'], false);
    assert.deepEqual(plan, { code: false, documentation: true,
      memory: false, performance: false, draft: false });
    assert.deepEqual(acceptance(results(plan)), []);
    assert.equal(classify([`${tool}.unknown`], false).code, true);
    assert.equal(classify([tool, 'compiler/gate4/src/compiler.trb'], false).performance, true);
    assert.equal(classify([tool, 'tools/ci-plan.mjs'], false).performance, true);
  }
  assert.equal(classify(['tools/benchmarksgame-formal/run.sh'], false).code, true);
});
test('other executable changes retain complete correctness and target checks', () => {
  const plan = classify(['src/decoder.trb'], false);
  assert.equal(plan.code, true);
  assert.equal(plan.performance, false);
  assert.deepEqual(acceptance(results(plan)), []);
});
test('deletions, renames, mixed changes and unknown paths fail toward more checking', () => {
  assert.equal(classify(['README.md', 'compiler/gate4/src/old.trb'], false).performance, true);
  assert.equal(classify(['new-directory/file'], false).code, true);
  assert.equal(classify(['compiler/gate4/src/with\na newline.trb'], false).code, true);
});
test('draft feedback cannot be accepted even when all jobs happen to succeed', () => {
  assert.notDeepEqual(acceptance(results(classify(['README.md'], true))), []);
});
test('failed, cancelled, skipped, missing and pending required jobs reject acceptance', () => {
  for (const job of ['quick', 'documentation', 'native', 'targets', 'memory', 'performance']) {
    for (const state of ['failure', 'cancelled', 'skipped', 'pending', undefined]) {
      const needs = results(classify(['compiler/gate4/src/compiler.trb', 'README.md'], false));
      needs[job] = state ? { result: state } : undefined;
      assert.notDeepEqual(acceptance(needs), [], `${job}: ${state}`);
    }
  }
});
test('missing or malformed planning never authorizes skipped validation', () => {
  assert.notDeepEqual(acceptance({}), []);
  const needs = results(classify(['README.md'], false));
  needs.plan.outputs.code = '';
  assert.notDeepEqual(acceptance(needs), []);
  needs.plan.result = 'failure';
  assert.notDeepEqual(acceptance(needs), []);
});

test('CLI classifies real historical-to-documentation and current-project renames', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'native-ci-plan-test-'));
  const git = (...args) => execFileSync('git', [
    '-c', 'user.name=CI Test', '-c', 'user.email=ci-test@example.invalid',
    '-c', 'commit.gpgsign=false', '-c', 'core.hooksPath=/dev/null', ...args,
  ], { cwd: directory, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
  try {
    git('init');
    mkdirSync(join(directory, 'compiler/gate4/src'), { recursive: true });
    const source = join(directory, 'compiler/gate4/src/old\nname.trb');
    writeFileSync(source, 'def main()\n\treturn\nend\n');
    git('add', '.');
    git('commit', '-m', 'Initial synthetic fixture');
    const base = git('rev-parse', 'HEAD');
    mkdirSync(join(directory, 'docs'));
    renameSync(source, join(directory, 'docs/example.md'));
    git('add', '-A');
    git('commit', '-m', 'Move synthetic fixture');
    const head = git('rev-parse', 'HEAD');
    const output = execFileSync(process.execPath,
      [fileURLToPath(new URL('./ci-plan.mjs', import.meta.url)), base, head, 'false'],
      { cwd: directory, encoding: 'utf8' });
    assert.deepEqual(Object.fromEntries(output.trim().split('\n').map(row => row.split('='))),
      { code: 'true', documentation: 'true', memory: 'true', performance: 'true', draft: 'false' });
    mkdirSync(join(directory, 'compiler/src'), { recursive: true });
    renameSync(join(directory, 'docs/example.md'), join(directory, 'compiler/src/current.trb'));
    git('add', '-A');
    git('commit', '-m', 'Move synthetic fixture to current project');
    const movedPaths = await changedPaths(base, git('rev-parse', 'HEAD'), directory);
    assert.deepEqual(movedPaths.sort(), ['compiler/gate4/src/old\nname.trb', 'compiler/src/current.trb']);
    const movedPlan = classify(movedPaths, false);
    assert.equal(movedPlan.memory, true);
    assert.equal(movedPlan.performance, true);
    assert.deepEqual(acceptance(results(movedPlan)), []);
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
});

test('large evidence inventories retain every path and a final code change', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'native-ci-plan-large-test-'));
  const git = (args, input) => execFileSync('git', [
    '-c', 'user.name=CI Test', '-c', 'user.email=ci-test@example.invalid',
    '-c', 'commit.gpgsign=false', '-c', 'core.hooksPath=/dev/null', ...args,
  ], { cwd: directory, encoding: 'utf8', input, stdio: ['pipe', 'pipe', 'pipe'] }).trim();
  try {
    git(['init']);
    const emptyTree = git(['mktree'], '');
    const base = git(['commit-tree', emptyTree], 'Empty synthetic baseline\n');
    const blob = git(['hash-object', '-w', '--stdin'], 'Synthetic observation\n');
    const names = Array.from({ length: 7000 }, (_, i) =>
      `${String(i).padStart(5, '0')}-${'観測-'.repeat(25)}.txt`);
    const evidenceTree = git(['mktree'],
      names.map(name => `100644 blob ${blob}\t${name}\n`).join(''));
    const docsTree = git(['mktree'], `040000 tree ${evidenceTree}\tresults\n`);
    const docsHead = git(['commit-tree', docsTree, '-p', base], 'Synthetic evidence\n');
    const paths = await changedPaths(base, docsHead, directory);
    assert.equal(paths.length, names.length);
    assert(Buffer.byteLength(paths.join('\0')) > 1024 * 1024);
    assert.deepEqual(paths, names.map(name => `results/${name}`));
    assert.equal(classify(paths, false).code, false);

    // This path sorts after the entire >1 MiB evidence list.
    const codeTree = git(['mktree'],
      `040000 tree ${evidenceTree}\tresults\n100644 blob ${blob}\tzz-final-code.trb\n`);
    const codeHead = git(['commit-tree', codeTree, '-p', base], 'Final synthetic code change\n');
    const complete = await changedPaths(base, codeHead, directory);
    assert.equal(complete.length, names.length + 1);
    assert.equal(complete.at(-1), 'zz-final-code.trb');
    assert.equal(classify(complete, false).code, true);
    await assert.rejects(changedPaths(base, '0'.repeat(40), directory), /Git path inventory failed/);
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
});
