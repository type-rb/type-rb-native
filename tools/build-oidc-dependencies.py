#!/usr/bin/env python3
"""Build HTTP/HTTPS-only libcurl against the qualified single OpenSSL stack."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import socket
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.error
import urllib.request

from network_artifacts import embed_identity, target_name, verify

crypto_spec = importlib.util.spec_from_file_location('crypto_builder', Path(__file__).with_name('build-crypto-dependencies.py'))
crypto_builder = importlib.util.module_from_spec(crypto_spec)
crypto_spec.loader.exec_module(crypto_builder)

DISABLED = ('ALTSVC', 'COOKIES', 'BEARER_AUTH', 'DIGEST_AUTH', 'KERBEROS_AUTH', 'NEGOTIATE_AUTH',
            'AWS', 'DICT', 'DOH', 'FILE', 'FTP', 'GOPHER', 'HSTS', 'IMAP', 'LDAP', 'LDAPS',
            'MIME', 'FORM_API', 'MQTT', 'NETRC', 'POP3', 'IPFS', 'RTSP', 'SMTP', 'WEBSOCKETS',
            'TELNET', 'TFTP')

SOURCE_MAX_BYTES = 64 * 1024 * 1024
SOURCE_DOWNLOAD_ATTEMPTS = 3


def transient_download_error(error):
    if isinstance(error, urllib.error.HTTPError):
        return error.code in (408, 429, 500, 502, 503, 504)
    reason = error.reason if isinstance(error, urllib.error.URLError) else error
    return isinstance(reason, (socket.gaierror, TimeoutError, ConnectionError))


def download_source(url):
    for attempt in range(1, SOURCE_DOWNLOAD_ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(url, timeout=60) as response:
                return response.read(SOURCE_MAX_BYTES + 1)
        except OSError as error:
            print(f'source download attempt {attempt}/{SOURCE_DOWNLOAD_ATTEMPTS} failed: '
                  f'{url}: {error}', file=sys.stderr)
            if attempt == SOURCE_DOWNLOAD_ATTEMPTS or not transient_download_error(error):
                raise
            # Retry the same pinned URL after one, then two seconds. Certificate
            # failures and archive validation never enter the retry path.
            time.sleep(attempt)

# Compile-time ABI observations, not a repository-owned C runtime.
ABI_CONSTANTS = {
    'OPENSSL_INIT_NO_LOAD_CONFIG': 128, 'EVP_PKEY_PUBLIC_KEY': 134,
    'RSA_PKCS1_PADDING': 1, 'CURL_GLOBAL_DEFAULT': 3, 'CURL_ERROR_SIZE': 256,
    'CURLOPT_URL': 10002, 'CURLOPT_WRITEFUNCTION': 20011, 'CURLOPT_WRITEDATA': 10001,
    'CURLOPT_HEADERFUNCTION': 20079, 'CURLOPT_HEADERDATA': 10029, 'CURLOPT_ERRORBUFFER': 10010,
    'CURLOPT_FOLLOWLOCATION': 52, 'CURLOPT_MAXREDIRS': 68, 'CURLOPT_TIMEOUT_MS': 155,
    'CURLOPT_NOSIGNAL': 99, 'CURLOPT_PROTOCOLS_STR': 10318, 'CURLOPT_REDIR_PROTOCOLS_STR': 10319,
    'CURLOPT_ACCEPT_ENCODING': 10102, 'CURLOPT_USERAGENT': 10018, 'CURLOPT_SSLVERSION': 32,
    'CURL_SSLVERSION_TLSv1_2': 6, 'CURLOPT_SSL_VERIFYPEER': 64, 'CURLOPT_SSL_VERIFYHOST': 81,
    'CURLOPT_SSL_OPTIONS': 216, 'CURLSSLOPT_NATIVE_CA': 16, 'CURLOPT_SSL_CTX_FUNCTION': 20108,
    'CURLOPT_CAINFO': 10065, 'CURLOPT_CAPATH': 10097, 'CURLINFO_RESPONSE_CODE': 2097154,
    'CURLOPT_PROXY': 10004, 'CURLOPT_NOPROXY': 10177, 'CURLOPT_HTTP_CONTENT_DECODING': 158,
    'CURLINFO_REDIRECT_URL': 1048607, 'CURLUPART_URL': 0, 'CURLUPART_SCHEME': 1,
    'CURLUPART_HOST': 5, 'CURLUPART_PORT': 6, 'CURLU_DEFAULT_PORT': 1,
    'CURLU_NON_SUPPORT_SCHEME': 8, 'AF_INET': 2,
    'Z_OK': 0, 'Z_STREAM_END': 1, 'Z_BUF_ERROR': -5, 'Z_NO_FLUSH': 0,
}


def verify_openssl_headers(build, prefix, environment):
    """Check the actual libcurl translation unit, including transitive headers."""
    commands = json.loads((build / 'compile_commands.json').read_text())
    matches = [entry for entry in commands if Path(entry['file']).as_posix().endswith('/vtls/openssl.c')]
    if len(matches) != 1:
        raise ValueError('expected one OpenSSL translation unit')
    entry = matches[0]
    command = entry.get('arguments') or shlex.split(entry['command'])
    # CMake's command database contains the real include order. Preprocess that
    # command instead of an independent probe with a different search path.
    command[command.index('-c')] = '-E'
    command[command.index('-o') + 1] = os.devnull
    result = subprocess.run([*command, '-H'], cwd=entry['directory'], env=environment,
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    if result.returncode:
        raise ValueError('OpenSSL header audit failed:\n' + result.stderr)
    headers = set()
    for line in result.stderr.splitlines():
        match = re.match(r'^\.+ (.+)$', line)
        if match:
            header = Path(match[1]).resolve()
            if 'openssl' in header.parts:
                if not header.is_relative_to((prefix / 'include/openssl').resolve()):
                    raise ValueError('compiler selected an unqualified OpenSSL header: ' + str(header))
                headers.add(header)
    if not headers:
        raise ValueError('compiler did not report any OpenSSL headers')
    return len(headers)


def extract(pin, directory, archives):
    archive = archives / pin['url'].rsplit('/', 1)[-1]
    cached = archive.exists()
    if cached:
        data = archive.read_bytes()
    else:
        data = download_source(pin['url'])
    actual = hashlib.sha256(data).hexdigest()
    if len(data) > SOURCE_MAX_BYTES or actual != pin['sha256']:
        origin = 'cache' if cached else 'download'
        raise ValueError(f"source archive checksum or size differs: {pin['url']}; "
                         f"{origin}, {len(data)} bytes, SHA-256 {actual}, expected {pin['sha256']}")
    if not cached:
        archive.write_bytes(data)
    with tarfile.open(archive) as source:
        total = 0
        for member in source.getmembers():
            path = Path(member.name)
            total += member.size
            if path.is_absolute() or '..' in path.parts or not (member.isdir() or member.isfile()) or total > 512 * 1024 * 1024:
                raise ValueError('unsafe source archive entry')
        source.extractall(directory, filter='data')
    return directory / pin['root']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archives', type=Path, required=True)
    parser.add_argument('--crypto-archives', type=Path, required=True)
    parser.add_argument('--crypto', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    # Subprocesses run inside temporary source directories. Resolve caller
    # paths before changing cwd so relative CLI inputs keep their meaning.
    args.archives = args.archives.resolve()
    args.crypto_archives = args.crypto_archives.resolve()
    args.crypto = args.crypto.resolve()
    output = args.output.resolve()
    if output.exists():
        raise ValueError('use a new installation; accepted artifacts are not replaced')
    output.parent.mkdir(parents=True, exist_ok=True)
    args.archives.mkdir(parents=True, exist_ok=True)
    target = target_name()
    crypto_receipt = verify(args.crypto, target, 'crypto')
    pins = json.loads(Path(__file__).with_name('oidc-dependencies.json').read_text())
    crypto_pins = json.loads(Path(__file__).with_name('crypto-dependencies.json').read_text())
    started = time.monotonic()
    cc = os.environ.get('CC', 'cc')
    with tempfile.TemporaryDirectory(prefix='.oidc-build-', dir=output.parent) as temporary:
        root = Path(temporary)
        openssl = extract(crypto_pins['openssl'], root, args.crypto_archives)
        curl = extract(pins['curl'], root, args.archives)
        zlib = extract(pins['zlib'], root, args.archives)
        flags = '-O2 -fPIC -ffunction-sections -fdata-sections -ffile-prefix-map=' + str(root) + '=.'
        environment = dict(os.environ, CC=cc, CFLAGS=flags, ZERO_AR_DATE='1',
                           SOURCE_DATE_EPOCH=str(crypto_pins['openssl']['source_date_epoch']))
        for name in ('OPENSSL_CONF', 'OPENSSL_MODULES', 'OPENSSL_ENGINES',
                     'CPATH', 'C_INCLUDE_PATH', 'CPLUS_INCLUDE_PATH', 'OBJC_INCLUDE_PATH',
                     'LIBRARY_PATH', 'CPPFLAGS', 'LDFLAGS'):
            environment.pop(name, None)

        def run(*argv, cwd=root):
            subprocess.run(list(map(str, argv)), cwd=cwd, env=environment, check=True, timeout=600)

        run('perl', 'Configure', crypto_builder.TARGETS[target], *crypto_builder.OPTIONS,
            '--prefix=/trbn/openssl', '--openssldir=/trbn/openssl/no-configuration', cwd=openssl)
        run('make', '-j2', 'build_libs', cwd=openssl)
        # Use the already accepted crypto archive everywhere, with headers and
        # libssl from exactly the same source/configuration. No second provider.
        run('make', 'install_dev', 'DESTDIR=' + str(root / 'stage'), cwd=openssl)
        prefix = root / 'stage/trbn/openssl'
        crypto_library = next(prefix.glob('lib*/libcrypto.a'))
        ssl_library = crypto_library.with_name('libssl.a')
        shutil.copy2(args.crypto / 'libcrypto.a', crypto_library)
        zprefix = root / 'zlib-install'
        run('./configure', '--static', '--prefix=' + str(zprefix), cwd=zlib)
        run('make', '-j2', cwd=zlib)
        run('make', 'install', cwd=zlib)
        cmake_options = ['-DBUILD_CURL_EXE=OFF', '-DBUILD_SHARED_LIBS=OFF', '-DBUILD_STATIC_LIBS=ON',
                         '-DCMAKE_EXPORT_COMPILE_COMMANDS=ON', '-DCMAKE_NO_SYSTEM_FROM_IMPORTED=ON',
                         '-DBUILD_TESTING=OFF', '-DBUILD_LIBCURL_DOCS=OFF', '-DBUILD_MISC_DOCS=OFF',
                         '-DCURL_USE_OPENSSL=ON', '-DOPENSSL_USE_STATIC_LIBS=ON',
                         '-DOPENSSL_ROOT_DIR=' + str(prefix), '-DOPENSSL_INCLUDE_DIR=' + str(prefix / 'include'),
                         '-DOPENSSL_SSL_LIBRARY=' + str(ssl_library), '-DOPENSSL_CRYPTO_LIBRARY=' + str(crypto_library),
                         '-DCURL_DISABLE_OPENSSL_AUTO_LOAD_CONFIG=ON',
                         '-DCURL_ZLIB=ON', '-DZLIB_INCLUDE_DIR=' + str(zprefix / 'include'),
                         '-DZLIB_LIBRARY=' + str(zprefix / 'lib/libz.a'),
                         '-DCURL_BROTLI=OFF', '-DCURL_ZSTD=OFF', '-DCURL_USE_LIBPSL=OFF',
                         '-DCURL_USE_LIBSSH2=OFF', '-DCURL_USE_GSSAPI=OFF', '-DUSE_LIBIDN2=OFF',
                         '-DUSE_NGHTTP2=OFF', '-DUSE_NGTCP2=OFF', '-DENABLE_THREADED_RESOLVER=ON',
                         '-DCURL_CA_BUNDLE=none', '-DCURL_CA_PATH=none', '-DCURL_CA_FALLBACK=OFF',
                         '-DCMAKE_C_FLAGS=' + flags, '-DCMAKE_BUILD_TYPE=Release',
                         *['-DCURL_DISABLE_' + name + '=ON' for name in DISABLED]]
        if target.startswith('darwin-'):
            cmake_options.append('-DUSE_APPLE_SECTRUST=ON')
        run('cmake', '-S', curl, '-B', root / 'curl-build', *cmake_options)
        # A host package manager may otherwise supply headers from an OpenSSL
        # build with a different configuration, even with a pinned crypto path.
        cache = {line.split(':', 1)[0]: line.split('=', 1)[1]
                 for line in (root / 'curl-build/CMakeCache.txt').read_text().splitlines()
                 if not line.startswith(('#', '//')) and ':' in line and '=' in line}
        for name, expected in [('OPENSSL_INCLUDE_DIR', prefix / 'include'),
                               ('OPENSSL_SSL_LIBRARY', ssl_library), ('OPENSSL_CRYPTO_LIBRARY', crypto_library)]:
            if name not in cache or Path(cache[name]).resolve() != expected.resolve():
                raise ValueError('CMake selected an unqualified OpenSSL input: ' + name)
        header_count = verify_openssl_headers(root / 'curl-build', prefix, environment)
        run('cmake', '--build', root / 'curl-build', '--target', 'libcurl_static', '--parallel', '2')
        probe = root / 'abi.c'
        probe.write_text('#include <stddef.h>\n#include <string.h>\n#include <dirent.h>\n#include <curl/curl.h>\n'
                         '#include <time.h>\n#include <netinet/in.h>\n#include <zlib.h>\n'
                         '#include <openssl/ssl.h>\n#include <openssl/rsa.h>\n'
                         '_Static_assert(sizeof(void*) == 8 && sizeof(size_t) == 8 && sizeof(long) == 8, "LP64");\n'
                         '_Static_assert(sizeof(int) == 4, "C int");\n' +
                         '_Static_assert(offsetof(struct dirent,d_name) == ' + ('21' if target.startswith('darwin-') else '19') + ', "dirent name");\n' +
                         '_Static_assert(AF_INET6 == ' + ('30' if target.startswith('darwin-') else '10') + ', "IPv6 family");\n' +
                         '_Static_assert(CLOCK_MONOTONIC == ' + ('6' if target.startswith('darwin-') else '1') + ', "monotonic clock");\n' +
                         '_Static_assert(sizeof(z_stream) == 112, "zlib stream");\n'
                         '_Static_assert(sizeof(gz_header) == 80, "gzip header");\n'
                         '_Static_assert(offsetof(gz_header,name) == 40 && offsetof(gz_header,name_max) == 48, "gzip name");\n'
                         '_Static_assert(offsetof(gz_header,comment) == 56 && offsetof(gz_header,comm_max) == 64, "gzip comment");\n'
                         '_Static_assert(offsetof(z_stream,next_in) == 0 && offsetof(z_stream,avail_in) == 8, "zlib input");\n'
                         '_Static_assert(offsetof(z_stream,next_out) == 24 && offsetof(z_stream,avail_out) == 32, "zlib output");\n' +
                         ''.join('_Static_assert(' + name + ' == ' + str(value) + ', "' + name + '");\n'
                                 for name, value in ABI_CONSTANTS.items()) +
                         'int main(void) {\n'
                         'if (!OPENSSL_init_ssl(OPENSSL_INIT_NO_LOAD_CONFIG, NULL)) return 1;\n'
                         'if (curl_global_init(CURL_GLOBAL_DEFAULT)) return 2;\n'
                         'const curl_version_info_data *v = curl_version_info(CURLVERSION_NOW);\n'
                         'if (!v || !v->ssl_version || strncmp(v->ssl_version,"OpenSSL/",8)) return 3;\n'
                         'if (!v->protocols[0] || strcmp(v->protocols[0],"http") || '
                         '!v->protocols[1] || strcmp(v->protocols[1],"https") || v->protocols[2]) return 4;\n'
                         'CURL *h = curl_easy_init(); if (!h) return 5;\n'
                         'curl_easy_cleanup(h); curl_global_cleanup(); return 0; }\n')
        system_flags = (['-framework', 'Security', '-framework', 'CoreFoundation', '-framework', 'SystemConfiguration']
                        if target.startswith('darwin-') else ['-pthread', '-ldl'])
        run(cc, '-std=c11', '-D_POSIX_C_SOURCE=200809L', '-Werror', '-I', curl / 'include',
            '-I', prefix / 'include', '-I', zprefix / 'include', probe,
            root / 'curl-build/lib/libcurl.a', openssl / 'libssl.a', args.crypto / 'libcrypto.a',
            zprefix / 'lib/libz.a', *system_flags, '-o', root / 'abi')
        run(root / 'abi')
        publication = root / 'publication'
        publication.mkdir()
        for source, name in [(root / 'curl-build/lib/libcurl.a', 'libcurl.a'), (openssl / 'libssl.a', 'libssl.a'),
                             (zprefix / 'lib/libz.a', 'libz.a'), (curl / 'COPYING', 'curl-LICENSE'),
                             (zlib / 'LICENSE', 'zlib-LICENSE'), (args.crypto / 'openssl-LICENSE', 'openssl-LICENSE')]:
            shutil.copy2(source, publication / name)
        receipt = {'schema': 2, 'linkage': 'static', 'target': target, 'pins': pins,
                   'configuration': {'protocols': ['http', 'https'], 'resolver': 'threaded',
                                     'openssl': crypto_pins, 'crypto_libraries': crypto_receipt['libraries'],
                                     'crypto_configuration': crypto_receipt['configuration'],
                                     'apple_sectrust': target.startswith('darwin-'),
                                     'openssl_inputs_pinned': True,
                                     'openssl_headers_verified': header_count,
                                     'automatic_ca_paths': False, 'automatic_openssl_configuration': False,
                                     'disabled': list(DISABLED), 'cflags': '-O2 -fPIC -ffunction-sections -fdata-sections -ffile-prefix-map=<build>=.'},
                   'cc': subprocess.check_output([cc, '--version'], text=True).splitlines()[0],
                   'cmake': subprocess.check_output(['cmake', '--version'], text=True).splitlines()[0],
                   'builder_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   'artifact_tool_sha256': hashlib.sha256(Path(__file__).with_name('network_artifacts.py').read_bytes()).hexdigest(),
                   'abi_constants': ABI_CONSTANTS, 'abi_probe_sha256': hashlib.sha256(probe.read_bytes()).hexdigest(),
                   'libraries': {name: hashlib.sha256((publication / (name + '.a')).read_bytes()).hexdigest()
                                 for name in ('libcurl', 'libssl', 'libz')}}
        embed_identity(receipt, root / 'identity.s', 'oidc')
        run(cc, '-c', root / 'identity.s', '-o', publication / 'oidc-identity.o')
        receipt['files'] = {p.name: {'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                            for p in sorted(publication.iterdir())}
        receipt['build_seconds'] = time.monotonic() - started
        (publication / 'oidc-build.json').write_text(json.dumps(receipt, indent=2) + '\n')
        verify(publication, target, 'oidc')
        publication.rename(output)
    print(output)


if __name__ == '__main__':
    main()
