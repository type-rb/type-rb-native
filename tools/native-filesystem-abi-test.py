#!/usr/bin/env python3
"""Qualify libc layouts used by the scoped filesystem adapter, not its semantics."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import tempfile


def abi_profile(target):
    if target not in ('darwin-arm64', 'darwin-amd64', 'linux-arm64', 'linux-amd64'):
        raise ValueError('unsupported filesystem ABI target: ' + target)
    darwin = target.startswith('darwin-')
    arm = target.endswith('arm64')
    return {
        'sizeof(struct stat)': 144 if darwin or not arm else 128,
        'sizeof(mode_t)': 2 if darwin else 4,
        'sizeof(off_t)': 8, 'sizeof(ssize_t)': 8, 'sizeof(void *)': 8,
        'offsetof(struct stat, st_mode)': 4 if darwin else (16 if arm else 24),
        'offsetof(struct stat, st_size)': 96 if darwin else 48,
        'offsetof(struct dirent, d_name)': 21 if darwin else 19,
        'offsetof(struct dirent, d_type)': 20 if darwin else 18,
        'O_RDONLY': 0, 'O_WRONLY': 1, 'O_RDWR': 2,
        'O_CREAT': 512 if darwin else 64, 'O_EXCL': 2048 if darwin else 128,
        'O_NONBLOCK': 4 if darwin else 2048, 'O_NOCTTY': 131072 if darwin else 256,
        'O_CLOEXEC': 16777216 if darwin else 524288,
        'AT_SYMLINK_NOFOLLOW': 32 if darwin else 256,
        'S_IFMT': 61440, 'S_IFREG': 32768, 'S_IFDIR': 16384, 'S_IFLNK': 40960,
        'EINTR': 4, 'ENOENT': 2, 'EACCES': 13, 'EEXIST': 17,
        'ENOTDIR': 20, 'EISDIR': 21, 'EINVAL': 22,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    system = platform.system().lower()
    machine = {'aarch64': 'arm64', 'x86_64': 'amd64'}.get(platform.machine(), platform.machine())
    target = system + '-' + machine
    profile = abi_profile(target)
    source = ('#define _GNU_SOURCE\n#define _DARWIN_C_SOURCE\n'
              '#include <stddef.h>\n#include <sys/stat.h>\n#include <fcntl.h>\n'
              '#include <unistd.h>\n#include <dirent.h>\n#include <errno.h>\n')
    source += ''.join('_Static_assert(' + name + ' == ' + str(value) + ', "' + name + '");\n'
                      for name, value in profile.items())
    # Compiler-owned test declarations keep prototypes and actual link symbols
    # visible. They are not a C implementation of the TypeRB runtime.
    source += '''int (*volatile stat_handle)(int, struct stat *) = &fstat;
int (*volatile truncate_handle)(int, off_t) = &ftruncate;
int (*volatile acquire)(const char *, int, ...) = &open;
int (*volatile release)(int) = &close;
ssize_t (*volatile read_bytes)(int, void *, size_t) = &read;
ssize_t (*volatile write_bytes)(int, const void *, size_t) = &write;
DIR *(*volatile open_directory)(const char *) = &opendir;
struct dirent *(*volatile next_entry)(DIR *) = &readdir;
int (*volatile close_directory)(DIR *) = &closedir;
int (*volatile directory_handle)(DIR *) = &dirfd;
int (*volatile entry_info)(int, const char *, struct stat *, int) = &fstatat;
int (*volatile create_directory)(const char *, mode_t) = &mkdir;
int main(void) { return 0; }
'''
    compiler = os.environ.get('CC', 'cc')
    with tempfile.TemporaryDirectory(prefix='native-filesystem-abi-') as temporary:
        root = Path(temporary)
        probe = root / 'probe.c'
        executable = root / 'probe'
        probe.write_text(source)
        subprocess.run([compiler, '-std=c11', '-Werror', str(probe), '-o', str(executable)],
                       check=True, timeout=60)
        subprocess.run([str(executable)], check=True, timeout=10)
        symbols = subprocess.check_output(['nm', '-u', str(executable)], text=True, timeout=10).splitlines()
    receipt = {'target': target, 'scope': 'libc ABI only; Native filesystem semantics require separate execution',
               'assertions': profile, 'source_sha256': hashlib.sha256(source.encode()).hexdigest(),
               'compiler': subprocess.check_output([compiler, '--version'], text=True).splitlines()[0],
               'undefined_symbols': [line.strip() for line in symbols]}
    if args.receipt:
        args.receipt.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
