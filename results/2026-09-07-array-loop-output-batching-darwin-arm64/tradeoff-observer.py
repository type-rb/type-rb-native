"""Bounded Darwin diagnostic; external measurement orchestration, not compiler code."""
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import statistics
import subprocess
import sys
import time

if len(sys.argv) != 8 or sys.platform != 'darwin':
    raise SystemExit('usage (Darwin): observer.py setup|measure CHECKOUT OUTPUT QBE FROZEN_COMPILER MAIN_COMPILER CANDIDATE_COMPILER')
MODE = sys.argv[1]
ROOT = Path(sys.argv[2]).resolve()
OUT = Path(sys.argv[3]).resolve()
QBE = Path(sys.argv[4]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
REVISIONS = {
    'frozen': '1afd60c2c7257ed34fd2a2aa70cb8b9164433009',
    'main': '26bb32a3d3bd085fdae4fc190bf2a14703351a8f',
    'candidate': 'c33b105fee3af3712fe97d938d20167d2f013bdf',
}
COMPILERS = {
    'frozen': Path(sys.argv[5]).resolve(),
    'main': Path(sys.argv[6]).resolve(),
    'candidate': Path(sys.argv[7]).resolve(),
}
PROGRAMS = {'spectral-norm': '5500', 'n-body': '1000000', 'fannkuch-redux': '10'}
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)
def build(compiler, source, output):
    return [str(compiler), 'build', str(source), '--output', str(output), '--qbe', str(QBE), '--cc', '/usr/bin/cc', '--target', 'darwin-arm64-v0']

def setup():
    assert not git('diff', REVISIONS['candidate'], 'HEAD', '--', 'compiler', 'src', 'tools')
    metadata = {'revisions': REVISIONS, 'qbeSha256': sha(QBE), 'roles': {}, 'programs': {}, 'setupOnly': True}
    for role, original in COMPILERS.items():
        directory = OUT / role
        directory.mkdir()
        compiler = directory / 'compiler'
        shutil.copy2(original, compiler)
        source_root = directory / 'source'
        for name in git('ls-tree', '-r', '--name-only', REVISIONS[role], 'compiler/src').decode().splitlines():
            if name.endswith('.trb') and not name.endswith('_test.trb'):
                path = source_root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(git('show', REVISIONS[role] + ':' + name))
        source = source_root / 'compiler/src/compiler.trb'
        verify = directory / 'verify/compiler'
        verify.parent.mkdir()
        subprocess.run(build(compiler, source, verify), check=True, capture_output=True)
        assert sha(verify) == sha(compiler), role
        qbe = subprocess.check_output([str(compiler), 'emit-qbe', str(source)])
        sections = subprocess.check_output(['/usr/bin/size', '-m', str(compiler)], text=True)
        text_line = next(line for line in sections.splitlines() if 'Section __text:' in line)
        text_bytes = int(text_line.split('Section __text:')[1].split()[0])
        metadata['roles'][role] = {'compilerSha256': sha(compiler), 'compilerBytes': compiler.stat().st_size, 'qbeBytes': len(qbe), 'qbeSha256': hashlib.sha256(qbe).hexdigest(), 'textBytes': text_bytes, 'fixedPoint': True}
        for program, input_value in PROGRAMS.items():
            relative = f'benchmarks/benchmarksgame/{program}/src/main.trb'
            assert git('show', REVISIONS[role] + ':' + relative) == (ROOT / relative).read_bytes()
            executable = directory / program
            subprocess.run(build(compiler, ROOT / relative, executable), check=True, capture_output=True)
            actual = subprocess.run([str(executable), input_value], capture_output=True, check=True)
            expected = ROOT / f'benchmarks/benchmarksgame/{program}/expected/{input_value}.txt'
            assert actual.stdout == expected.read_bytes() and not actual.stderr, (role, program)
            metadata['programs'].setdefault(program, {'input': input_value, 'sourceSha256': sha(ROOT / relative), 'expectedSha256': sha(expected), 'roles': {}})['roles'][role] = {'sha256': sha(executable), 'bytes': executable.stat().st_size, 'outputStatus': 'pass'}
        print('preflight:', role, metadata['roles'][role], flush=True)
    save(OUT / 'setup.json', metadata)
    c, b = metadata['roles']['candidate'], metadata['roles']['frozen']
    assert c['compilerBytes'] <= min(350000, b['compilerBytes'] * 1.05)
    assert c['textBytes'] <= 254000 and c['qbeBytes'] <= 1135000

def observe(command, directory, deadline):
    directory.mkdir(parents=True)
    stdout = os.open(directory / 'stdout', os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    stderr = os.open(directory / 'stderr', os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    started = time.monotonic_ns()
    child = os.fork()
    if child == 0:
        try:
            os.setpgid(0, 0)
            os.dup2(stdout, 1)
            os.dup2(stderr, 2)
            os.close(stdout)
            os.close(stderr)
            os.execve(command[0], command, dict(os.environ))
        except BaseException as error:
            os.write(2, str(error).encode())
            os._exit(127)
    os.close(stdout)
    os.close(stderr)
    timed_out = False
    def timeout(signum, frame):
        nonlocal timed_out
        timed_out = True
        try:
            os.killpg(child, signal.SIGKILL)
        except ProcessLookupError:
            pass
    previous = signal.signal(signal.SIGALRM, timeout)
    signal.setitimer(signal.ITIMER_REAL, max(0.001, deadline - time.monotonic()))
    try:
        _, status, usage = os.wait4(child, 0)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)
    return {'wall': (time.monotonic_ns() - started) / 1e9, 'cpu': usage.ru_utime + usage.ru_stime, 'rss': usage.ru_maxrss, 'exitStatus': os.waitstatus_to_exitcode(status), 'timedOut': timed_out}

def measure():
    setup_record = json.loads((OUT / 'setup.json').read_text())
    deadline = time.monotonic() + 1200
    started = time.monotonic()
    schedule = [(baseline, 'spectral-norm', cohort, 0.98) for cohort in (1, 2) for baseline in ('frozen', 'main')]
    schedule += [(baseline, program, 1, 1.02) for program in ('n-body', 'fannkuch-redux') for baseline in ('frozen', 'main')]
    schedule += [(baseline, 'self-build', 1, 1.05) for baseline in ('frozen', 'main')]
    summaries = []
    for baseline, program, cohort, runtime_limit in schedule:
        name = f'{program}-{baseline}-{cohort}'
        directory = OUT / name
        directory.mkdir()
        rows = []
        for phase, rounds in [('warmup', 2), ('retained', 7)]:
            for round_index in range(1, rounds + 1):
                roles = ['baseline', 'candidate'] if round_index % 2 else ['candidate', 'baseline']
                for order, role in enumerate(roles, 1):
                    actual_role = baseline if role == 'baseline' else 'candidate'
                    observation = directory / f'{phase}-{round_index}-{order}-{role}'
                    if program == 'self-build':
                        command = build(OUT / actual_role / 'compiler', OUT / actual_role / 'source/compiler/src/compiler.trb', observation / 'compiler')
                    else:
                        command = [str(OUT / actual_role / program), PROGRAMS[program]]
                    row = {'phase': phase, 'round': round_index, 'order': order, 'role': role, **observe(command, observation, deadline)}
                    if program == 'self-build':
                        valid = (observation / 'compiler').is_file() and sha(observation / 'compiler') == setup_record['roles'][actual_role]['compilerSha256']
                    else:
                        valid = (observation / 'stdout').read_bytes() == (ROOT / f'benchmarks/benchmarksgame/{program}/expected/{PROGRAMS[program]}.txt').read_bytes()
                    row['outputStatus'] = 'pass' if valid and not (observation / 'stderr').read_bytes() and row['exitStatus'] == 0 and not row['timedOut'] else 'fail'
                    rows.append(row)
                    with (directory / 'raw.csv').open('w', newline='') as target:
                        writer = csv.DictWriter(target, fieldnames=list(row))
                        writer.writeheader()
                        writer.writerows(rows)
                    if row['outputStatus'] != 'pass' or time.monotonic() >= deadline:
                        raise RuntimeError(f'stop: invalid output or time budget: {name}')
        retained = [r for r in rows if r['phase'] == 'retained']
        medians = {role: {metric: statistics.median(r[metric] for r in retained if r['role'] == role) for metric in ('wall', 'cpu', 'rss')} for role in ('baseline', 'candidate')}
        ratios = {metric: medians['candidate'][metric] / medians['baseline'][metric] for metric in ('wall', 'cpu', 'rss')}
        catastrophic = {role: {metric: max(r[metric] for r in retained if r['role'] == role) / medians['baseline'][metric] for metric in ('wall', 'cpu', 'rss')} for role in ('baseline', 'candidate')}
        limits = {'wall': 1.20, 'cpu': 1.10, 'rss': 1.05} if program == 'self-build' else {'wall': runtime_limit, 'cpu': runtime_limit, 'rss': 1.05}
        catastrophic_pass = all(value <= 2.0 for metrics in catastrophic.values() for value in metrics.values())
        summary = {'name': name, 'baseline': baseline, 'program': program, 'cohort': cohort, 'medians': medians, 'ratios': ratios, 'limits': limits, 'maximumToBaselineMedianRatios': catastrophic, 'catastrophicPass': catastrophic_pass, 'thresholdsPass': all(ratios[k] <= limits[k] for k in limits), 'outputsPass': True}
        if program == 'self-build':
            summary['ordinaryCostPass'] = all(value <= 1.05 for value in ratios.values())
        save(directory / 'summary.json', summary)
        summaries.append(summary)
        save(OUT / 'measurement.json', {'summaries': summaries, 'elapsedSeconds': time.monotonic() - started, 'complete': len(summaries) == len(schedule)})
        print(name, json.dumps(ratios), 'thresholds:', summary['thresholdsPass'], flush=True)
        if not catastrophic_pass or ratios['rss'] > 1.05 or (program == 'self-build' and not summary['thresholdsPass']):
            raise RuntimeError(f'stop: investigation budget: {name}')

if __name__ == '__main__':
    if MODE == 'setup':
        setup()
    elif MODE == 'measure':
        measure()
    else:
        raise SystemExit('mode must be setup or measure')
