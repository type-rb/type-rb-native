#!/usr/bin/env python3
"""Exercise actual compiler header selection in the OIDC dependency builder."""
import hashlib
import importlib.util
import io
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('oidc_builder', Path(__file__).with_name('build-oidc-dependencies.py'))
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class OidcBuilderTest(unittest.TestCase):
    def test_invalid_download_reports_identity_without_caching_it(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            rejected = b'upstream response is not the pinned archive\n'
            pin = {'url': 'https://example.invalid/source.tar.gz', 'sha256': '0' * 64}
            with patch.object(builder.urllib.request, 'urlopen', return_value=io.BytesIO(rejected)):
                with self.assertRaises(ValueError) as error:
                    builder.extract(pin, root / 'unpacked', root)
            message = str(error.exception)
            for expected in (pin['url'], 'download', str(len(rejected)) + ' bytes',
                             hashlib.sha256(rejected).hexdigest(), pin['sha256']):
                self.assertIn(expected, message)
            self.assertEqual(list(root.iterdir()), [])

    def test_invalid_cache_is_preserved_and_identified(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / 'source.tar.gz'
            rejected = b'invalid cached archive\n'
            archive.write_bytes(rejected)
            pin = {'url': 'https://example.invalid/source.tar.gz', 'sha256': '0' * 64}
            with patch.object(builder.urllib.request, 'urlopen') as download:
                with self.assertRaises(ValueError) as error:
                    builder.extract(pin, root / 'unpacked', root)
            self.assertIn('cache', str(error.exception))
            self.assertIn(hashlib.sha256(rejected).hexdigest(), str(error.exception))
            download.assert_not_called()
            self.assertEqual(archive.read_bytes(), rejected)

    def test_host_header_cannot_replace_qualified_headers(self):
        with tempfile.TemporaryDirectory(prefix='oidc header fixture ') as temporary:
            root = Path(temporary)
            prefix = root / 'qualified'
            ambient = root / 'ambient'
            for directory in (prefix / 'include', ambient):
                (directory / 'openssl').mkdir(parents=True)
                (directory / 'openssl/probe.h').write_text('#define OIDC_FIXTURE 1\n')
            (root / 'vtls').mkdir()
            (root / 'vtls/openssl.c').write_text('#include <openssl/probe.h>\nint fixture = OIDC_FIXTURE;\n')
            (root / 'CMakeLists.txt').write_text('''cmake_minimum_required(VERSION 3.16)
project(header_fixture C)
add_library(pinned INTERFACE IMPORTED)
set_target_properties(pinned PROPERTIES INTERFACE_INCLUDE_DIRECTORIES "${CMAKE_CURRENT_SOURCE_DIR}/qualified/include")
add_library(fixture OBJECT vtls/openssl.c)
target_link_libraries(fixture PRIVATE pinned)
''')
            environment = dict(os.environ, CPATH=str(ambient))
            for system in ('ON', 'OFF'):
                build = root / system
                subprocess.run(['cmake', '-S', str(root), '-B', str(build),
                                '-DCMAKE_EXPORT_COMPILE_COMMANDS=ON',
                                '-DCMAKE_NO_SYSTEM_FROM_IMPORTED=' + system], env=environment,
                               check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
                if system == 'ON':
                    self.assertEqual(builder.verify_openssl_headers(build, prefix, environment), 1)
                else:
                    with self.assertRaisesRegex(ValueError, 'unqualified OpenSSL header'):
                        builder.verify_openssl_headers(build, prefix, environment)


if __name__ == '__main__':
    unittest.main()
