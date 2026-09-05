import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, writeFileSync, renameSync, rmSync } from 'node:fs';
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

test('documentation-only PRs do not run compiler or performance matrices', () => {
  const plan = classify(['README.md', 'docs/index.html', 'results/a.json',
    'tools/native-mir-guarded-add/README.md'], false);
  assert.deepEqual(plan, { code: false, documentation: true,
    memory: false, performance: false, draft: false });
  assert.deepEqual(acceptance(results(plan)), []);
});
test('compiler, conformance and CI-routing changes retain the full authority', () => {
  for (const path of ['compiler/gate4/src/storage.trb',
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

test('CLI classifies a real source-to-documentation rename and unusual filename', () => {
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
