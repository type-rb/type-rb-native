import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { pathToFileURL } from 'node:url';

// Correctness suites only. Performance authorities run after the joined job.
export async function runSuites({ executable, suites, evidence, cwd = process.cwd(), env = process.env, graceMs = 1000 }) {
  if (process.platform === 'win32' || suites.length !== 2 ||
      suites.some(s => !/^[a-z]+$/.test(s.name) || !Array.isArray(s.args) || s.args.some(a=>typeof a !== 'string')) ||
      suites[0].name === suites[1].name || !Number.isInteger(graceMs) || graceMs < 1 || graceMs > 10000) {
    throw new Error('Expected exactly two distinct POSIX suite names');
  }
  fs.mkdirSync(evidence, { recursive: true });
  // Prepare every log before starting either process. A bad evidence path
  // must not leave the first suite running while setup of the second fails.
  const files = [];
  try {
    for (const suite of suites) {
      for (const stream of ['stdout', 'stderr']) {
        files.push(fs.openSync(path.join(evidence, `${suite.name}.${stream}`), 'wx'));
      }
    }
  } catch (error) {
    for (const fd of files) fs.closeSync(fd);
    throw error;
  }
  const records = suites.map(s => ({ name: s.name, args: s.args, state: 'pending' }));
  const groups = new Set();
  let cancellation = null;
  let evidenceError = null;
  let terminated = Promise.resolve();
  const save = () => {
    try { fs.writeFileSync(path.join(evidence, 'status.json'), JSON.stringify({ cancellation, suites: records }, null, 2) + '\n'); }
    catch (error) {
      evidenceError ??= error;
      console.error(`Cannot write suite status: ${error.message}`);
    }
  };
  const signalGroup = (pid, signal) => {
    try { process.kill(-pid, signal); return true; }
    catch (error) { if (error.code !== 'ESRCH') throw error; return false; }
  };
  const cancel = signal => {
    if (cancellation) return;
    cancellation = signal;
    save();
    for (const pid of groups) signalGroup(pid, 'SIGTERM');
    // Retain owned group IDs until the grace period ends: a parent can exit
    // before a descendant that inherited the group and ignored SIGTERM.
    terminated = new Promise(resolve => setTimeout(() => {
      for (const pid of groups) signalGroup(pid, 'SIGKILL');
      resolve();
    }, graceMs));
  };
  const onInt = () => cancel('SIGINT');
  const onTerm = () => cancel('SIGTERM');
  save();
  if (evidenceError) {
    for (const fd of files) fs.closeSync(fd);
    throw evidenceError;
  }
  process.on('SIGINT', onInt);
  process.on('SIGTERM', onTerm);
  try {
    await Promise.all(suites.map((suite, index) => new Promise(resolve => {
      const record = records[index];
      const out = files[index * 2];
      const err = files[index * 2 + 1];
      const start = performance.now();
      record.state = 'running';
      record.startedAt = new Date().toISOString();
      console.log(`Starting ${suite.name} suite`);
      const child = spawn(executable, suite.args, { cwd, env, detached: true, stdio: ['ignore', out, err] });
      if (child.pid) groups.add(child.pid);
      child.on('error', error => { record.launchError = error.message; });
      child.on('close', async (code, signal) => {
        fs.closeSync(out);
        fs.closeSync(err);
        record.state = 'closing';
        record.code = code;
        record.signal = signal;
        if (!cancellation && child.pid) {
          if (signalGroup(child.pid, 0)) {
            // A successful parent must not silently leave detached work for
            // later smoke or performance steps, nor escape cancellation.
            record.orphanedDescendants = true;
            signalGroup(child.pid, 'SIGTERM');
            await new Promise(resolve => setTimeout(resolve, graceMs));
            signalGroup(child.pid, 'SIGKILL');
          }
          if (!cancellation) groups.delete(child.pid);
        }
        record.state = 'completed';
        record.elapsedSeconds = (performance.now() - start) / 1000;
        save();
        console.log(`Finished ${suite.name}: code=${code}, signal=${signal}, seconds=${record.elapsedSeconds.toFixed(3)}`);
        resolve();
      });
      save();
    })));
    await terminated;
    save();
  } finally {
    process.off('SIGINT', onInt);
    process.off('SIGTERM', onTerm);
  }
  if (cancellation) return cancellation === 'SIGINT' ? 130 : 143;
  if (evidenceError) return 1;
  return records.every(r => r.code === 0 && !r.signal && !r.launchError && !r.orphanedDescendants) ? 0 : 1;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    const [executable, evidence] = process.argv.slice(2);
    if (!executable || !path.isAbsolute(executable) || !evidence || process.argv.length !== 4 ||
        !process.env.TYPE_RB_NATIVE_ROOT || !process.env.TYPE_RB_NATIVE_REFERENCE_TRB || !process.env.TYPE_RB_NATIVE_QBE) {
      throw new Error('Usage: ci-run-suites.mjs ABSOLUTE_TRB EVIDENCE (with all recovery/QBE environment variables)');
    }
    process.exitCode = await runSuites({ executable, evidence, suites: [
      { name: 'root', args: ['test'] },
      { name: 'compiler', args: ['test', '--config', 'compiler/gate4/trbconfig.jsonc'] },
    ] });
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
