#!/usr/bin/env python3
"""Exercise real checkout cache invalidation in an isolated copy."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

repository = Path(__file__).resolve().parent.parent

with tempfile.TemporaryDirectory(prefix='native bootstrap ') as temporary:
    root = Path(temporary)
    for directory in ['compiler', 'bin', '.trb/bootstrap']:
        shutil.copytree(repository / directory, root / directory)
    (root / 'tools').mkdir()
    for file in ['trbn', 'tools/build-native.sh']:
        shutil.copy2(repository / file, root / file)
    env = {key: value for key, value in os.environ.items()
           if key not in ['TRBN_CC', 'TRBN_QBE', 'TRBN_BOOTSTRAP_SEED']}

    def run(*command):
        return subprocess.run(command, cwd=root, env=env, text=True,
                              capture_output=True, check=True, timeout=120)

    def build():
        return run('./trbn', '--version').stderr

    def snapshot():
        return tuple((root / file).stat().st_mtime_ns for file in
                     ['bin/trbn', '.trb/bootstrap/core/compiler', '.trb/bootstrap/inputs'])

    def edit(file, text):
        path = root / file
        before = path.stat()
        path.write_text(path.read_text() + text)
        # Content changes must invalidate even when timestamps are preserved.
        os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))

    # An old same-name cache must not shadow the immutable release-scoped seed.
    seeds = list((root / '.trb/bootstrap/bootstrap-seed-2026-09-08').glob('type-rb-native-bootstrap-*'))
    assert len(seeds) == 1, seeds
    legacy_seed = root / '.trb/bootstrap' / seeds[0].name
    legacy_seed.write_bytes(b'synthetic stale legacy seed\n')

    build()
    baseline = snapshot()
    invalid_seed = subprocess.run(['./trbn', '--version'], cwd=root,
                                  env={**env, 'TRBN_BOOTSTRAP_SEED': str(legacy_seed)},
                                  text=True, capture_output=True, timeout=120)
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
    assert 'reusing' not in build()
    edit('compiler/src/unused/extra.trb', '# Changed nested input\n')
    assert 'reusing' not in build()
    extra.unlink()
    assert 'reusing' not in build()

    # Failed compilation must leave all published binaries and keys untouched.
    baseline = snapshot()
    cli = root / 'compiler/cli/main.trb'
    valid = cli.read_text()
    cli.write_text(valid + '\ndef broken(\n')
    failure = subprocess.run(['./trbn', '--version'], cwd=root, env=env,
                             text=True, capture_output=True, timeout=120)
    assert failure.returncode != 0 and snapshot() == baseline, failure
    assert not (root / '.trb/bootstrap/build.lock').exists()
    assert not list((root / '.trb/bootstrap').glob('build.*'))
    cli.write_text(valid)
    assert build() == '' and snapshot() == baseline

    # Concurrent callers share one successful build and receive the same binary.
    edit('compiler/cli/main.trb', '\n# Concurrent edit\n')
    children = [subprocess.Popen(['./trbn', '--version'], cwd=root, env=env,
                                 text=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE) for _ in range(2)]
    outputs = [child.communicate(timeout=120) for child in children]
    assert all(child.returncode == 0 for child in children), outputs
    assert outputs[0][0] == outputs[1][0], outputs
    assert sum('bootstrapping' in stderr for _, stderr in outputs) == 1, outputs
    assert build() == ''

print('Native bootstrap content cache, core reuse, failure and concurrency checks passed')
