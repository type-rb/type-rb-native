#!/usr/bin/env python3
"""Exercise real checkout cache invalidation in an isolated copy."""
import os
from pathlib import Path
import shutil
import signal
import subprocess
import tempfile
import time

repository = Path(__file__).resolve().parent.parent
BUILD_TIMEOUT_SECONDS = 600

def stop_on_signal(signum, _frame):
    # Let the active build's finally block reap its whole process group.
    raise SystemExit(128 + signum)

signal.signal(signal.SIGTERM, stop_on_signal)

with tempfile.TemporaryDirectory(prefix='native bootstrap ') as temporary:
    root = Path(temporary)
    for directory in ['compiler', 'bin', '.trb/bootstrap']:
        shutil.copytree(repository / directory, root / directory)
    (root / 'tools').mkdir()
    for file in ['trbn', 'tools/build-native.sh']:
        shutil.copy2(repository / file, root / file)
    env = {key: value for key, value in os.environ.items()
           if key not in ['TRBN_CC', 'TRBN_QBE', 'TRBN_BOOTSTRAP_SEED']}

    def stop_owned(child):
        if child.poll() is not None:
            return
        try:
            os.killpg(child.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            child.wait(timeout=5)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(child.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            child.wait()

    def communicate(child, timeout):
        try:
            return child.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            # The launcher waits for a shell builder and compiler descendants.
            # Terminating just the launcher would leave them in the test copy.
            try:
                os.killpg(child.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                stdout, stderr = child.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(child.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                stdout, stderr = child.communicate()
            print(stdout, stderr, flush=True)
            raise

    def run(*command, timeout=120, check=True, environment=env, directory=root):
        child = subprocess.Popen(command, cwd=directory, env=environment, text=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 start_new_session=True)
        try:
            stdout, stderr = communicate(child, timeout)
        except BaseException:
            stop_owned(child)
            raise
        result = subprocess.CompletedProcess(command, child.returncode, stdout, stderr)
        if check:
            if result.returncode != 0:
                print(stdout, stderr, flush=True)
            result.check_returncode()
        return result

    def build(directory=root, label=''):
        start = time.monotonic()
        # This watchdog bounds a complete core/CLI fixed-point rebuild, not a
        # performance acceptance measurement. Retain the elapsed observation.
        result = run('./trbn', '--version', timeout=BUILD_TIMEOUT_SECONDS,
                     directory=directory).stderr
        print(f'Native cache build{(" " + label) if label else ""}: '
              f'{time.monotonic() - start:.2f}s', flush=True)
        return result

    def snapshot(directory=root):
        return tuple((directory / file).stat().st_mtime_ns for file in
                     ['bin/trbn', '.trb/bootstrap/core/compiler', '.trb/bootstrap/inputs'])

    def edit(file, text, directory=root):
        path = directory / file
        before = path.stat()
        path.write_text(path.read_text() + text)
        # Content changes must invalidate even when timestamps are preserved.
        os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))

    # An old same-name cache must not shadow the immutable release-scoped seed.
    seeds = list((root / '.trb/bootstrap/bootstrap-seed-2026-09-12-compiler-names').glob('type-rb-native-bootstrap-*'))
    assert len(seeds) == 1, seeds
    legacy_seed = root / '.trb/bootstrap' / seeds[0].name
    legacy_seed.write_bytes(b'synthetic stale legacy seed\n')

    build()
    baseline = snapshot()
    invalid_seed = run('./trbn', '--version', check=False,
                       environment={**env, 'TRBN_BOOTSTRAP_SEED': str(legacy_seed)})
    assert invalid_seed.returncode != 0 and 'checksum mismatch' in invalid_seed.stderr
    assert snapshot() == baseline
    assert not (root / '.trb/bootstrap/build.lock').exists()
    assert not list((root / '.trb/bootstrap').glob('build.*'))
    assert build() == '' and snapshot() == baseline
    (root / 'compiler/cli/main.trb').touch()
    (root / 'compiler/cli/ignored_test.trb').write_text('invalid test source\n')
    assert build() == '' and snapshot() == baseline
    run('git', 'init', '--quiet')
    for message in ['first', 'documentation-only']:
        run('git', '-c', 'user.name=Cache Test', '-c', 'user.email=cache@example.com',
            '-c', 'commit.gpgsign=false', 'commit', '--quiet', '--allow-empty', '-m', message)
        assert build() == '' and snapshot() == baseline

    edit('compiler/cli/main.trb', '\n# CLI edit\n')
    assert 'reusing the verified core' in build()
    changed = snapshot()
    assert changed[0] != baseline[0] and changed[1] == baseline[1]
    assert build() == '' and snapshot() == changed

    added = root / 'compiler/cli/extra.trb'
    added.write_text('# Added input\n')
    assert 'reusing the verified core' in build()
    added.unlink()
    assert 'reusing the verified core' in build()

    edit('compiler/src/compiler.trb', '\n# Core edit\n')
    result = build()
    assert 'bootstrapping' in result and 'reusing' not in result
    assert snapshot()[1] != baseline[1]
    assert legacy_seed.read_bytes() == b'synthetic stale legacy seed\n'

    nested = root / 'compiler/src/unused'
    nested.mkdir()
    extra = nested / 'extra.trb'
    extra.write_text('# Nested input\n')
    assert 'reusing' not in build(label='nested addition')
    # Modification and removal both start from the verified added-input cache.
    # They need independent checkouts so each real rebuild checks its own key.
    with tempfile.TemporaryDirectory(prefix='native bootstrap nested ') as temporary_nested:
        modified_root = Path(temporary_nested)
        shutil.copytree(root, modified_root, dirs_exist_ok=True)
        assert snapshot(modified_root) == snapshot()
        assert build(modified_root, 'relocated cache hit') == ''
        edit('compiler/src/unused/extra.trb', '# Changed nested input\n', modified_root)
        extra.unlink()
        started = time.monotonic()
        with tempfile.TemporaryFile(mode='w+t') as changed_log, \
             tempfile.TemporaryFile(mode='w+t') as removed_log:
            children = []
            cases = [(modified_root, 'nested modification', changed_log),
                     (root, 'nested removal', removed_log)]
            try:
                for directory, _label, log in cases:
                    children.append(subprocess.Popen(
                        ['./trbn', '--version'], cwd=directory, env=env,
                        stdout=log, stderr=subprocess.STDOUT,
                        start_new_session=True))
                deadline = started + BUILD_TIMEOUT_SECONDS
                finished = [0.0, 0.0]
                while any(child.poll() is None for child in children):
                    for index, child in enumerate(children):
                        if finished[index] == 0.0 and child.poll() is not None:
                            finished[index] = time.monotonic() - started
                    if time.monotonic() >= deadline:
                        raise subprocess.TimeoutExpired('./trbn --version', BUILD_TIMEOUT_SECONDS)
                    time.sleep(0.1)
                outputs = []
                for index, (directory, label, log) in enumerate(cases):
                    child = children[index]
                    if finished[index] == 0.0:
                        finished[index] = time.monotonic() - started
                    log.seek(0)
                    output = log.read()
                    print(f'Native cache build {label}: {finished[index]:.2f}s', flush=True)
                    if child.returncode != 0:
                        print(output, flush=True)
                        raise subprocess.CalledProcessError(child.returncode,
                                                            ['./trbn', '--version'], output)
                    outputs.append(output)
                changed_result, removed_result = outputs
            finally:
                for child in children:
                    stop_owned(child)
        assert 'reusing' not in changed_result
        assert 'reusing' not in removed_result
        print(f'Native parallel nested invalidation: '
              f'{time.monotonic() - started:.2f}s', flush=True)

    # Failed compilation must leave all published binaries and keys untouched.
    baseline = snapshot()
    cli = root / 'compiler/cli/main.trb'
    valid = cli.read_text()
    cli.write_text(valid + '\ndef broken(\n')
    failure = run('./trbn', '--version', check=False)
    assert failure.returncode != 0 and snapshot() == baseline, failure
    assert not (root / '.trb/bootstrap/build.lock').exists()
    assert not list((root / '.trb/bootstrap').glob('build.*'))
    cli.write_text(valid)
    assert build() == '' and snapshot() == baseline

    # Concurrent callers share one successful build and receive the same binary.
    edit('compiler/cli/main.trb', '\n# Concurrent edit\n')
    started = time.monotonic()
    deadline = started + BUILD_TIMEOUT_SECONDS
    children = [subprocess.Popen(['./trbn', '--version'], cwd=root, env=env,
                                 text=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, start_new_session=True)
                for _ in range(2)]
    try:
        outputs = [communicate(child, max(0.001, deadline - time.monotonic()))
                   for child in children]
    finally:
        for child in children:
            if child.poll() is None:
                try:
                    os.killpg(child.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                communicate(child, 5)
    assert all(child.returncode == 0 for child in children), outputs
    assert outputs[0][0] == outputs[1][0], outputs
    assert sum('bootstrapping' in stderr for _, stderr in outputs) == 1, outputs
    print(f'Native concurrent cache build: {time.monotonic() - started:.2f}s', flush=True)
    assert build() == ''

print('Native bootstrap content cache, core reuse, failure and concurrency checks passed')
