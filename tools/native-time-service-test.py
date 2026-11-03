#!/usr/bin/env python3
"""Qualify the frozen application payload/time slice, including process inputs."""
import argparse
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import signal
import struct
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / 'tools/native-time-services.json'


def tzif(offset):
    return (b'TZif\0' + bytes(15) + struct.pack('>6I', 0, 0, 0, 0, 1, 5)
            + struct.pack('>iBB', offset, 0, 0) + b'TEST\0')


def fixtures(root):
    for directory, content in [('zones', tzif(20700)), ('malformed', b'not TZif'),
                               ('v4', tzif(0)[:4] + b'4' + tzif(0)[5:])]:
        for name in ['Example/Native', 'Asia/Tokyo']:
            path = root / directory / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    for name, method in [('stored.zip', zipfile.ZIP_STORED), ('compressed.zip', zipfile.ZIP_DEFLATED)]:
        with zipfile.ZipFile(root / name, 'w', compression=method) as archive:
            archive.writestr('Example/Native', tzif(20700))
            archive.writestr('Asia/Tokyo', tzif(20700))
    (root / 'invalid.zip').write_bytes(b'not a zip')
    (root / 'truncated.zip').write_bytes((root / 'stored.zip').read_bytes()[:-12])
    (root / 'local.tzif').write_bytes(tzif(3600))


def invoke(binary, arguments, root, environment, source=None):
    child = subprocess.Popen([str(binary), *map(str, arguments)], cwd=root, env=environment,
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             start_new_session=True)
    try:
        stdout, stderr = child.communicate(source.encode() if source is not None else None, timeout=120)
        code = child.returncode
    except subprocess.TimeoutExpired:
        os.killpg(child.pid, signal.SIGKILL)
        stdout, stderr = child.communicate()
        code = 124
    except BaseException:
        if child.poll() is None:
            os.killpg(child.pid, signal.SIGKILL)
        child.communicate()
        raise
    return {'code': code,
            'stdout': stdout.decode('utf-8', 'backslashreplace').replace(str(root), '<fixture>'),
            'stderr': stderr.decode('utf-8', 'backslashreplace').replace(str(root), '<fixture>')}


def local_expected(expected, environment):
    # Local-unset intentionally uses host data. Qualify that row against the
    # same-host reference when supplied; a Native-only lane records this
    # independent OS localtime probe instead of claiming a reference replay.
    script = ('import datetime,time; time.tzset(); '
              'print(datetime.datetime.fromtimestamp(1704132000).isoformat())')
    value = subprocess.check_output([sys.executable, '-c', script], env=environment,
                                    text=True, timeout=10).strip()
    result = json.loads(json.dumps(expected))
    for outcome in result.values():
        lines = outcome['stdout'].splitlines(keepends=True)
        lines[0] = 'ok|Local|' + value + '\n'
        outcome['stdout'] = ''.join(lines)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native', type=Path)
    parser.add_argument('--reference', type=Path)
    parser.add_argument('--report', required=True, type=Path)
    args = parser.parse_args()
    if not args.native and not args.reference:
        parser.error('at least one compiler is required')
    compilers = {name: path.resolve() for name, path in [('reference', args.reference), ('native', args.native)] if path}
    manifest = json.loads(MANIFEST.read_text())
    if manifest['referenceRevision'] != (ROOT / 'TYPE_RB_REVISION').read_text().strip():
        parser.error('service expectations require the pinned reference revision')
    spec = importlib.util.spec_from_file_location('language', ROOT / 'tools/native-language-coverage.py')
    language = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(language)
    registry = json.loads((ROOT / 'tools/native-language-cases.json').read_text())
    report = {'schemaVersion': 1, 'scope': manifest['scope'],
              'referenceRevision': manifest['referenceRevision'],
              'manifestSha256': language.digest(MANIFEST),
              'compilers': {name: {'sha256': language.digest(binary)} for name, binary in compilers.items()},
              'registry': [], 'environment': [], 'builds': [], 'complete': False}

    def save():
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')

    failures = []
    try:
        with tempfile.TemporaryDirectory(prefix='native-time-services-') as temporary:
            root = Path(temporary).resolve()
            for entry in manifest['registry']:
                case = next(c for c in registry['cases'] if c['id'] == entry['id'])
                digest = hashlib.sha256(json.dumps(case, sort_keys=True).encode()).hexdigest()
                if digest != entry['caseSha256'] or language.parity_gaps(case):
                    raise ValueError('frozen registry case changed: ' + entry['id'])
                target = root / entry['id']
                target.mkdir()
                observed = language.collect(case, compilers.get('native'), compilers.get('reference'), target)
                matches = {role: language.outcomes_match(result, case[role]) for role, result in observed.items()}
                report['registry'].append({'id': entry['id'], 'matches': matches, 'observations': observed})
                save()
                if not all(matches.values()):
                    failures.append(entry['id'])
                print(entry['id'], matches, flush=True)

            data = root / 'fixtures'
            data.mkdir()
            fixtures(data)
            base_env = dict(os.environ, TZ='UTC', NO_COLOR='1', TERM='dumb', TRBN_HISTORY=str(root / 'history.json'))
            base_env.pop('ZONEINFO', None)
            built = {}
            for kind, program in manifest['programs'].items():
                target = root / ('program-' + kind)
                target.mkdir()
                (target / 'main.trb').write_text(program['declarations'] + '\ndef main()\n' + program['body'] + '\nend\n')
                for role, compiler in compilers.items():
                    executable = target / role
                    checked = invoke(compiler, ['check', 'main.trb'], target, base_env)
                    result = invoke(compiler, ['build', '--compile', '--outfile', executable, 'main.trb'], target, base_env)
                    report['builds'].append({'program': kind, 'role': role, 'check': checked, 'build': result})
                    save()
                    if checked['code'] != 0 or result['code'] != 0 or not executable.is_file():
                        raise ValueError('service program did not check/build: ' + kind + '/' + role)
                    built[kind, role] = executable
            for group in manifest['environment']:
                kind = 'cache' if group['id'] == 'local-lifetime' else 'invalid' if group['id'] == 'zone-invalid-name' else 'zones'
                row = {'id': group['id'], 'variants': []}
                report['environment'].append(row)
                for variant in group['variants']:
                    env = dict(base_env)
                    for key, value in variant['environment'].items():
                        if value is None:
                            env.pop(key, None)
                        else:
                            env[key] = value.replace('<fixture>', str(data))
                    expected = variant['reference']
                    if group['id'] == 'local-unset':
                        expected = local_expected(expected, env)
                    result = {'environment': variant['environment'], 'expected': expected, 'observations': {}, 'matches': {}}
                    if group['id'] == 'local-unset':
                        result['hostOracle'] = 'same-host reference and OS localtime' if args.reference else 'OS localtime; no reference replay'
                    row['variants'].append(result)
                    for role, compiler in compilers.items():
                        (data / 'local.tzif').write_bytes(tzif(3600))
                        executed = invoke(built[kind, role], [], data, env)
                        (data / 'local.tzif').write_bytes(tzif(3600))
                        program = manifest['programs'][kind]
                        source = program['declarations'] + '\ndef probe()\n' + program['body'] + '\nend\nprobe()\n:quit\n'
                        repl = invoke(compiler, ['repl'], data, env, source)
                        observed = {'execute': executed, 'repl': repl}
                        result['observations'][role] = observed
                        result['matches'][role] = observed == expected
                        if observed != expected:
                            failures.append(group['id'] + '/' + role)
                        save()
                print(group['id'], [v['matches'] for v in row['variants']], flush=True)
            report['failures'] = failures
            report['complete'] = not failures
            save()
    except BaseException as error:
        report['error'] = type(error).__name__ + ': ' + str(error)
        raise
    finally:
        save()
    if failures:
        raise SystemExit('service contract differences: ' + ', '.join(failures))
    print('20 application service groups qualified for ' + ', '.join(compilers))


if __name__ == '__main__':
    main()
