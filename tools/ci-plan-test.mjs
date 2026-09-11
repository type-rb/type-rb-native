import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync, renameSync, rmSync, symlinkSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { acceptance, changedPaths, classify, toolingTests, quickToolingTests, compilerTestInputs, cliInputs } from './ci-plan.mjs';

function results(plan) {
  return {
    plan: { result: 'success', outputs: Object.fromEntries(
      Object.entries(plan).map(([key, value]) => [key, String(value)])) },
    ...Object.fromEntries(Object.entries({ quick: plan.quick,
      documentation: plan.documentation, native: plan.code, targets: plan.code,
      memory: plan.memory, performance: plan.performance, tooling: plan.tooling, cli: plan.cli,
    }).map(([key, value]) => [key, { result: value ? 'success' : 'skipped' }])),
  };
}

test('runtime A/B remains manual with separate frozen historical and Boolean contracts', () => {
  const workflow = readFileSync(new URL('../.github/workflows/native-runtime-ab.yml', import.meta.url), 'utf8');
  const entry = readFileSync(new URL('../.github/workflows/pull-request.yml', import.meta.url), 'utf8');
  assert(workflow.includes('  workflow_dispatch:\n'));
  assert(!workflow.includes('  pull_request:') && !workflow.includes('  workflow_call:'));
  assert(!entry.includes('native-runtime-ab.yml'), 'manual experiments must not add an automatic PR job');
  assert(workflow.includes('default: derived-loop-index'));
  assert.match(workflow, /derived-loop-index\)\n\s+BASELINE_REVISION=aad4954c66ae394a5edb836b20498e5a60b769bd/);
  assert.match(workflow, /checked-boolean-branches\)\n\s+BASELINE_REVISION=6f7e3ba10623d40b5b0f7e6cc03b732125607795/);
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

test('manual Boolean compactness loads its dependencies in a fresh step shell', () => {
  const root = fileURLToPath(new URL('../', import.meta.url));
  const workflow = readFileSync(new URL('../.github/workflows/native-runtime-ab.yml', import.meta.url), 'utf8');
  const setup = workflow.match(/          compiler_maximum=1\.01\n[\s\S]*?(?=            for role in baseline candidate; do)/)?.[0];
  assert(setup, 'the actual compactness setup must be exercised');
  const directory = mkdtempSync(join(tmpdir(), 'native-runtime-policy-test-'));
  try {
    symlinkSync(root, join(directory, 'baseline-source'), 'dir');
    const script = `set -eu\n${setup}\nfi\nprintf '%s %s\\n' "$compiler_maximum" "$compiler_limit"\n`;
    const options = { cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], env: {
      PATH: process.env.PATH,
      GITHUB_WORKSPACE: root,
      RUNNER_TEMP: directory,
      NATIVE_RUNTIME_AB_CONTRACT: 'checked-boolean-branches',
    } };
    for (const shell of ['/bin/sh', '/bin/bash']) {
      assert.equal(execFileSync(shell, ['-c', script], options).trim(), '1.00 370000');
      // A previous workflow step's functions do not survive in a new shell.
      assert.throws(() => execFileSync(shell, ['-c', script.replace(
        '. tools/compiler-project.sh', ': missing-project-helper')], options),
      error => error.status !== 0 && /native_compiler_project_directory/.test(error.stderr));
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
  const checkout = quick.indexOf('repository: type-rb/type-rb');
  const preflight = quick.indexOf('Validate every reference checkout before toolchain setup');
  assert(preflight >= 0 && preflight < checkout && checkout < build);
  for (const command of ['python3 -m unittest tools/compatibility_manifest_test.py',
    'python3 tools/compatibility_manifest.py\n']) {
    const check = quick.indexOf(command, preflight);
    assert(check > preflight && check < checkout, 'static pin checks precede reference checkout');
  }
  for (const command of [
    'python3 -m unittest tools/compatibility_manifest_test.py',
    'python3 tools/compatibility_manifest.py --reference-trb "$RUNNER_TEMP/trb"',
  ]) {
    const check = quick.indexOf(command, build);
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
  assert.deepEqual(plan, { code: false, quick: false, documentation: true,
    memory: false, performance: false, draft: false, tooling: false, cli: false });
  assert.deepEqual(acceptance(results(plan)), []);
});
test('ordinary language cases use a separate reference oracle and Go-free CLI checks', () => {
  const entry = readFileSync(new URL('../.github/workflows/pull-request.yml', import.meta.url), 'utf8');
  const cli = readFileSync(new URL('../.github/workflows/native-cli.yml', import.meta.url), 'utf8');
  const docs = readFileSync(new URL('../.github/workflows/documentation.yml', import.meta.url), 'utf8');
  assert(entry.includes('tools/native-language-coverage.py --reference "$RUNNER_TEMP/trb"'));
  assert(cli.includes('tools/native-language-coverage.py --native bin/trbn'));
  assert(!cli.includes('tools/native-language-coverage.py --reference'));
  assert(docs.includes('tools/native-language-coverage.py --check-table docs/native-language-coverage-matrix.md'));
  for (const path of ['tools/native-language-cases.json', 'tools/native-language-coverage.py',
    'tools/native-language-coverage-test.py']) {
    const plan = classify([path], false);
    assert.equal(plan.quick, true);
    assert.equal(plan.cli, true);
    assert.equal(plan.code, false);
    assert.equal(plan.performance, false);
    assert.deepEqual(acceptance(results(plan)), []);
    assert.equal(classify([path, 'compiler/src/compiler.trb'], false).performance, true);
  }
});
test('compiler, conformance and execution workflows retain the full authority', () => {
  for (const path of ['compiler/src/storage.trb', 'compiler/trbconfig.jsonc',
    'compiler/conformance/runtime-invalid/new.trb',
    'tools/compiler-project.sh',
    'compiler/gate4/src/storage.trb',
    'compiler/gate4/conformance/runtime-invalid/new.trb',
    '.github/workflows/pull-request.yml', '.github/workflows/gate-zero.yml',
    '.github/workflows/static-string-compactness.yml', 'tools/ci-run-suites.mjs',
    'tools/native-mir-transition-policy.sh']) {
    const plan = classify([path], false);
    assert.equal(plan.code, true);
    assert.equal(plan.memory, true);
    assert.equal(plan.performance, true);
    assert.deepEqual(acceptance(results(plan)), []);
  }
});
test('static documentation and evidence tools do not run compiler matrices', () => {
  for (const tool of ['tools/capability-map-check.mjs',
    'tools/benchmark-pages-data.mjs', 'tools/benchmark-pages-check.mjs',
    'tools/result_archive.py', 'tools/result_archive_test.py',
    'tools/evidence_bundle.py', 'tools/evidence_bundle_test.py',
    '.github/workflows/documentation.yml']) {
    const plan = classify([tool, 'docs/capabilities/benchmarks/data.js'], false);
    assert.deepEqual(plan, { code: false, quick: false, documentation: true,
      memory: false, performance: false, draft: false, tooling: false, cli: false });
    assert.deepEqual(acceptance(results(plan)), []);
    assert.equal(classify([`${tool}.unknown`], false).code, true);
    assert.equal(classify([tool, 'compiler/gate4/src/compiler.trb'], false).performance, true);
    assert.equal(classify([tool, 'tools/ci-plan.mjs'], false).performance, false);
  }
  assert.equal(classify(['tools/benchmarksgame-formal/run.sh'], false).code, true);
});
test('planning-only maintenance uses its unconditional tests, not compiler matrices', () => {
  const workflow = readFileSync(new URL('../.github/workflows/pull-request.yml', import.meta.url), 'utf8');
  const planning = workflow.match(/^  plan:\n([\s\S]*?)(?=^  quick:)/m)?.[1];
  assert(planning);
  assert(!/^\s+if:/m.test(planning), 'planning tests cannot be conditional on their own outputs');
  for (const command of ['node --test tools/ci-plan-test.mjs tools/ci-run-suites-test.mjs tools/recovery-workspace-test.mjs',
    'node tools/ci-plan.mjs "$BASE_SHA" "$HEAD_SHA" "$IS_DRAFT"']) {
    assert(planning.includes(command), 'test and execute the actual router on every PR');
  }
  for (const path of ['tools/ci-plan.mjs', 'tools/ci-plan-test.mjs']) {
    const plan = classify([path, 'docs/evidence-retention.md', 'results/historical/raw.tsv'], false);
    assert.deepEqual(plan, { code: false, quick: false, documentation: true,
      memory: false, performance: false, draft: false, tooling: false, cli: false });
    assert.deepEqual(acceptance(results(plan)), []);
    for (const failure of ['failure', 'cancelled', 'skipped', undefined]) {
      const needs = results(plan);
      needs.plan.result = failure;
      assert.notDeepEqual(acceptance(needs), [], 'no acceptance without successful planning');
    }
    for (const other of ['compiler/src/compiler.trb', 'src/runtime.trb', 'TYPE_RB_REVISION',
      'tools/ci-run-suites.mjs', '.github/workflows/pull-request.yml',
      'tools/native-mir-transition-policy.sh', `${path}.unknown`, 'unknown/file']) {
      const mixed = classify([path, other], false);
      assert.equal(mixed.code, true, other);
      assert.equal(mixed.performance, true, other);
    }
  }
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
  for (const job of ['quick', 'documentation', 'native', 'targets', 'memory', 'performance', 'tooling', 'cli']) {
    for (const state of ['failure', 'cancelled', 'skipped', 'pending', undefined]) {
      const needs = results(classify(['compiler/gate4/src/compiler.trb', 'README.md'], false));
      needs[job] = state ? { result: state } : undefined;
      assert.notDeepEqual(acceptance(needs), [], `${job}: ${state}`);
    }
  }
});
test('missing or malformed planning never authorizes skipped validation', () => {
  assert.notDeepEqual(acceptance({}), []);
  for (const key of Object.keys(classify(['README.md'], false))) {
    for (const value of ['', undefined, true]) {
      const needs = results(classify(['README.md'], false));
      needs.plan.outputs[key] = value;
      assert.notDeepEqual(acceptance(needs), [], `${key}: ${value}`);
    }
  }
  const needs = results(classify(['README.md'], false));
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
      { code: 'true', quick: 'true', documentation: 'true', memory: 'true', performance: 'true', draft: 'false', tooling: 'true', cli: 'true' });
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

test('exact CLI inputs run quick and CLI authorities without core measurements', () => {
  for (const file of cliInputs) {
    const plan = classify([file], false);
    assert.equal(plan.code, false, file);
    assert.equal(plan.cli, true, file);
    assert.equal(plan.memory, false, file);
    assert.equal(plan.performance, false, file);
    assert.deepEqual(acceptance(results(plan)), []);
    for (const state of ['skipped', 'failure', 'cancelled', undefined]) {
      const needs = results(plan);
      needs.cli = { result: state };
      assert.notDeepEqual(acceptance(needs), [], file);
    }
    assert.equal(classify([file + '.unknown'], false).code, true);
    assert.equal(classify([file, 'compiler/src/compiler.trb'], false).performance, true);
  }
  const workflow = readFileSync(new URL('../.github/workflows/native-cli.yml', import.meta.url), 'utf8');
  assert(workflow.includes('  workflow_call:'));
  assert(!workflow.includes('  pull_request:'), 'one shared PR planner, no separate path-filtered run');
  assert.equal(classify(['compiler/conformance/README.md'], false).cli, false);
});

test('synthetic tooling tests have an executable authority without compiler rebuilds', () => {
  const workflow = readFileSync(new URL('../.github/workflows/ci-tooling.yml', import.meta.url), 'utf8');
  for (const file of toolingTests) {
    assert(workflow.includes(file), `the tooling authority must execute ${file}`);
    const plan = classify([file], false);
    assert.equal(plan.code, false, file);
    assert.equal(plan.cli, false, file);
    assert.equal(plan.tooling, true, file);
    assert.deepEqual(acceptance(results(plan)), []);
    const needs = results(plan);
    needs.tooling.result = 'skipped';
    assert.notDeepEqual(acceptance(needs), []);
    assert.equal(classify([file + '.unknown'], false).code, true);
    assert.equal(classify([file, 'compiler/src/compiler.trb'], false).performance, true);
  }
  for (const file of ['tools/benchmarksgame-build-formal/build-controller.sh',
    'tools/recovery-stage.py', 'tools/ci-run-suites.mjs', '.github/workflows/ci-tooling.yml']) {
    assert.equal(classify([file], false).code, true, file);
  }
  const native = readFileSync(new URL('../.github/workflows/gate-zero.yml', import.meta.url), 'utf8');
  assert(!native.includes('Verify bootstrap seed tooling'));
  const entry = readFileSync(new URL('../.github/workflows/pull-request.yml', import.meta.url), 'utf8');
  assert(entry.includes('needs: [plan, native, targets, memory, tooling, cli]'));
  assert(entry.includes("needs.tooling.result == 'success'"));
  assert(entry.includes('needs: [plan, quick, documentation, native, targets, memory, performance, tooling, cli]'));
});

test('main uses the same complete path classifier and Pages PR checks are not duplicated', () => {
  const main = readFileSync(new URL('../.github/workflows/push-validation.yml', import.meta.url), 'utf8');
  assert(main.includes('node tools/ci-plan.mjs "$BASE_SHA" "$HEAD_SHA" false push'));
  assert(main.includes('BASE_SHA: ${{ github.event.before }}'));
  for (const job of ['native', 'memory', 'tooling', 'documentation']) assert(main.includes(`  ${job}:`));
  for (const name of ['gate-zero', 'runtime-worker-memory', 'documentation']) {
    const source = readFileSync(new URL(`../.github/workflows/${name}.yml`, import.meta.url), 'utf8');
    assert(!source.includes('  push:'), `${name} must not independently rerun the same main validation`);
    assert(source.includes('  workflow_call:'));
  }
  const pages = readFileSync(new URL('../.github/workflows/capability-map-pages.yml', import.meta.url), 'utf8');
  assert(!pages.includes('  pull_request:'));
  assert(pages.includes('  push:') && pages.includes('  workflow_dispatch:'));
  assert.equal(classify(['.github/workflows/capability-map-pages.yml'], false).code, false);
  const doc = readFileSync(new URL('../.github/workflows/documentation.yml', import.meta.url), 'utf8');
  for (const command of ['node tools/capability-map-check.mjs', 'node tools/benchmark-pages-data.mjs --check', 'node tools/benchmark-pages-check.mjs']) assert(doc.includes(command));
});

test('mixed lightweight surfaces require the union and never skip a failed authority', () => {
  const plan = classify(['compiler/cli/main.trb', 'tools/recovery_stage_test.py', 'README.md'], false);
  assert.equal(plan.code, false);
  assert.equal(plan.cli, true);
  assert.equal(plan.tooling, true);
  assert.equal(plan.documentation, true);
  assert.deepEqual(acceptance(results(plan)), []);
  for (const job of ['quick', 'cli', 'tooling', 'documentation']) {
    for (const result of ['failure', 'cancelled', 'skipped', undefined]) {
      const needs = results(plan);
      needs[job] = { result };
      assert.notDeepEqual(acceptance(needs), []);
    }
  }
  for (const key of ['cli', 'tooling']) {
    const needs = results(plan);
    delete needs.plan.outputs[key];
    assert.notDeepEqual(acceptance(needs), []);
  }
});

test('push comparison includes changes against the actual before revision, not its merge base', async () => {
  const directory = mkdtempSync(join(tmpdir(), 'native-ci-push-test-'));
  const git = (args, input) => execFileSync('git', [
    '-c', 'user.name=CI Test', '-c', 'user.email=ci-test@example.invalid',
    '-c', 'commit.gpgsign=false', ...args,
  ], { cwd: directory, encoding: 'utf8', input }).trim();
  try {
    git(['init']);
    const empty = git(['mktree'], '');
    const base = git(['commit-tree', empty], 'Base\n');
    const blob = git(['hash-object', '-w', '--stdin'], 'Synthetic\n');
    const codeTree = git(['mktree'], `100644 blob ${blob}\tcore.trb\n`);
    const before = git(['commit-tree', codeTree, '-p', base], 'Earlier code\n');
    const docsTree = git(['mktree'], `100644 blob ${blob}\tREADME.md\n`);
    const head = git(['commit-tree', docsTree, '-p', base], 'Documentation on another lineage\n');
    assert.deepEqual(await changedPaths(before, head, directory), ['README.md']);
    assert.deepEqual(await changedPaths(before, head, directory, true), ['README.md', 'core.trb']);
    const output = execFileSync(process.execPath, [fileURLToPath(new URL('./ci-plan.mjs', import.meta.url)),
      before, head, 'false', 'push'], { cwd: directory, encoding: 'utf8' });
    assert.match(output, /^code=true$/m);
    assert.throws(() => execFileSync(process.execPath, [fileURLToPath(new URL('./ci-plan.mjs', import.meta.url)),
      before, head, 'false', 'unknown'], { cwd: directory, stdio: 'pipe' }));
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
});

test('known compiler test modules retain correctness without unchanged-binary measurements', () => {
  assert.equal(compilerTestInputs.size, 11);
  for (const file of compilerTestInputs) {
    const plan = classify([file], false);
    assert.deepEqual(plan, { code: true, quick: true, documentation: false,
      memory: false, performance: false, draft: false, tooling: true, cli: true });
    assert.deepEqual(acceptance(results(plan)), []);
    for (const job of ['quick', 'native', 'targets', 'tooling', 'cli']) {
      for (const state of ['failure', 'cancelled', 'skipped', undefined]) {
        const needs = results(plan);
        needs[job] = { result: state };
        assert.notDeepEqual(acceptance(needs), [], `${file}: ${job}: ${state}`);
      }
    }
    for (const other of ['compiler/src/compiler.trb', 'compiler/conformance/new.source',
      'compiler/trbconfig.jsonc', 'compiler/src/new_test.trb', 'src/decoder.trb',
      'TYPE_RB_REVISION', 'tools/native-mir-transition-policy.sh',
      '.github/workflows/pull-request.yml', 'tools/ci-plan.mjs', 'unknown/file']) {
      assert.equal(classify([file, other], false).performance, true, other);
      assert.equal(classify([file, other], false).memory, true, other);
    }
    assert.equal(classify([file + '.unknown'], false).performance, true);
    assert.equal(classify([file, 'README.md'], false).performance, false);
  }
});

test('synthetic project and policy tests retain Linux without building the reference compiler', () => {
  const entry = readFileSync(new URL('../.github/workflows/pull-request.yml', import.meta.url), 'utf8');
  const quick = entry.match(/^  quick:\n([\s\S]*?)(?=^  documentation:)/m)?.[1];
  assert(quick.includes("if: needs.plan.outputs.quick == 'true'"));
  assert(entry.includes('quick: ${{ steps.plan.outputs.quick }}'));
  const steps = quick.split('      - ').slice(1);
  const compilerCondition = "if: needs.plan.outputs.code == 'true' || needs.plan.outputs.cli == 'true'";
  for (const step of steps) {
    if (step.includes('repository: type-rb/type-rb') || step.includes('actions/setup-go') ||
      step.startsWith('name: Build the pinned') || step.startsWith('name: Check ') ||
      step.startsWith('name: Run root')) assert(step.includes(compilerCondition), step);
  }
  const toolingStep = steps.find(step => step.startsWith('name: Verify project'));
  assert(toolingStep && !toolingStep.includes('if:'), 'Linux controls cannot depend on compiler setup');
  for (const file of quickToolingTests) {
    assert(toolingStep.includes(`sh ${file}`));
    const plan = classify([file], false);
    assert.deepEqual(plan, { code: false, quick: true, documentation: false,
      memory: false, performance: false, draft: false, tooling: true, cli: false });
    assert.deepEqual(acceptance(results(plan)), []);
    for (const job of ['quick', 'tooling']) {
      for (const state of ['failure', 'cancelled', 'skipped', undefined]) {
        const needs = results(plan);
        needs[job] = { result: state };
        assert.notDeepEqual(acceptance(needs), []);
      }
    }
  }
  const invalid = results(classify(['compiler/src/compiler.trb'], false));
  invalid.plan.outputs.quick = 'false';
  invalid.quick.result = 'skipped';
  assert.notDeepEqual(acceptance(invalid), [], 'code cannot bypass quick through inconsistent outputs');
});

test('controller-only test edits keep both Linux and macOS execution', () => {
  const pr = readFileSync(new URL('../.github/workflows/pull-request.yml', import.meta.url), 'utf8');
  const main = readFileSync(new URL('../.github/workflows/push-validation.yml', import.meta.url), 'utf8');
  const tooling = readFileSync(new URL('../.github/workflows/ci-tooling.yml', import.meta.url), 'utf8');
  const native = readFileSync(new URL('../.github/workflows/gate-zero.yml', import.meta.url), 'utf8');
  for (const file of ['tools/ci-run-suites-test.mjs', 'tools/recovery-workspace-test.mjs']) {
    assert(pr.split('\n  quick:\n')[0].includes(file));
    assert(main.split('  native:')[0].includes(file));
    assert(tooling.includes(file));
    assert(!native.includes(file), 'the old macOS execution moved without duplication');
    const plan = classify([file], false);
    assert.equal(plan.code, false);
    assert.equal(plan.quick, false);
    assert.equal(plan.tooling, true);
    assert.deepEqual(acceptance(results(plan)), []);
  }
});
