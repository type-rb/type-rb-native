#!/usr/bin/env python3
"""Check actual compiler link helpers, including path-specific syscall failures."""
import argparse
import errno
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


FAMILIES = {
    'network': ('libuv.a', 'libllhttp.a', 'network-identity.o'),
    'compression': ('libdeflate.a', 'compression-identity.o'),
    'crypto': ('libcrypto.a', 'crypto-identity.o'),
    'oidc': ('libcurl.a', 'libssl.a', 'libz.a', 'oidc-identity.o'),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--qbe', type=Path, required=True)
    parser.add_argument('--source', type=Path, help='Runtime directory for a recorded regression control')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    source = args.source or root / 'compiler/src/backend/qbe/runtime'
    chunks = []
    for family in FAMILIES:
        text = (source / (family + '_link.trb')).read_text()
        chunks.extend(json.loads(match.group()) for match in re.finditer(r'"(?:[^"\\]|\\.)*"', text))
    il = '\n'.join(chunks) + '\ndata $trbn_project_selected_linker = align 8 { l 0 }\n'
    il = re.sub(r'^(function(?: [lw])?|data) ', r'export \1 ', il, flags=re.M)
    # Intercept only the two libc boundaries. All path selection, argv ownership,
    # failure propagation and diagnostics remain the production QBE functions.
    il = il.replace('call $realpath(', 'call $test_realpath(').replace('call $access(', 'call $test_access(')
    helper = r'''
#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#define FAMILY(name) extern int64_t trbn_##name##_link_required; \
 extern void *trbn_##name##_link_arguments(void *, const char *); \
 extern void trbn_##name##_link_cleanup(void *);
FAMILY(network) FAMILY(compression) FAMILY(crypto) FAMILY(oidc)
static const char *scenario;
static int resolutions, reads;
char *test_realpath(const char *path, char *buffer) {
 resolutions++;
 if (!strcmp(scenario, "resolve-denied")) { errno=EACCES; return NULL; }
 return realpath(path,buffer);
}
int test_access(const char *path, int mode) {
 reads++;
 if (!strcmp(scenario,"access-io")) { errno=EIO; return -1; }
 return access(path,mode);
}
int main(int argc,char **argv) {
 if(argc!=4)return 64;
 scenario=argv[2];
 void *slots[48]={0}; void *tail=NULL;
#define RUN(name) if(!strcmp(argv[1],#name)) { \
 trbn_##name##_link_required=strcmp(scenario,"unused")!=0; \
 tail=trbn_##name##_link_arguments(slots,argv[3]); \
 if(tail)trbn_##name##_link_cleanup(slots); }
 RUN(network) RUN(compression) RUN(crypto) RUN(oidc)
 printf("%d %d\n",resolutions,reads);
 return tail?0:78;
}
'''
    with tempfile.TemporaryDirectory(prefix='native link paths ') as temporary:
        work = Path(temporary)
        (work / 'test.ssa').write_text(il)
        (work / 'helper.c').write_text(helper)
        subprocess.run([str(args.qbe.resolve()), '-o', str(work / 'test.s'), str(work / 'test.ssa')], check=True)
        subprocess.run(['/usr/bin/cc', '-Wall', '-Wextra', '-Werror', str(work / 'test.s'), str(work / 'helper.c'), '-o', str(work / 'test')], check=True)
        count = 0
        for family, files in FAMILIES.items():
            directory = work / family
            directory.mkdir()
            for name in files:
                (directory / name).write_bytes(b'fixture\n')
            env = dict(os.environ, LC_ALL='C')
            for other in FAMILIES:
                env.pop('TRBN_' + other.upper() + '_LIB_DIR', None)
            variable = 'TRBN_' + family.upper() + '_LIB_DIR'

            def check(scenario, expected_code=0, environment=env, error_path=None, error_number=None):
                nonlocal count
                result = subprocess.run([str(work / 'test'), family, scenario, str(work / 'qbe')], env=environment, capture_output=True, text=True, timeout=10)
                assert result.returncode == expected_code, (family, scenario, result)
                if error_path is None:
                    assert result.stderr == '', (family, scenario, result)
                else:
                    assert str(error_path) + ': ' + os.strerror(error_number) in result.stderr, (family, scenario, result)
                    assert 'compiler: pinned static ' in result.stderr, (family, scenario, result)
                if scenario == 'unused':
                    assert result.stdout == '0 0\n', result
                count += 1

            check('adjacent')
            check('empty', environment=dict(env, **{variable: ''}))
            check('explicit', environment=dict(env, **{variable: str(directory)}))
            link = work / (family + ' alias')
            link.symlink_to(directory, target_is_directory=True)
            check('explicit-link', environment=dict(env, **{variable: str(link)}))
            missing = work / 'missing'
            check('unused', environment=dict(env, **{variable: str(missing)}))
            check('missing', 78, dict(env, **{variable: str(missing)}), missing, errno.ENOENT)
            check('resolve-denied', 78, error_path=directory, error_number=errno.EACCES)
            check('access-io', 78, error_path=directory / files[0], error_number=errno.EIO)
            for name in files:
                path = directory / name
                path.unlink()
                check('missing-file', 78, error_path=path, error_number=errno.ENOENT)
                path.write_bytes(b'fixture\n')
        print(f'{count} compiler link-path and syscall-failure checks passed')


if __name__ == '__main__':
    main()
