#!/usr/bin/env python3
"""Shared ordinary/REPL contract for ambient scoped File and Dir operations."""
import argparse
import errno
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


SOURCE = r'''import trb/std/path
import trb/std/file
import { FileMode } from trb/std/file
import trb/std/dir
import { DirEntryKind } from trb/std/dir
import { FileSystemError, FileSystemErrorKind, FileSystemTarget } from trb/std/errors
import trb/std/result
import trb/std/unit
import trb/std/process

def error_kind(kind: FileSystemErrorKind): String
case kind
when FileSystemErrorKind::Other
return "Other"
when FileSystemErrorKind::AlreadyExists
return "AlreadyExists"
when FileSystemErrorKind::NotFound
return "NotFound"
when FileSystemErrorKind::PermissionDenied
return "PermissionDenied"
when FileSystemErrorKind::InvalidPath
return "InvalidPath"
when FileSystemErrorKind::InvalidLimit
return "InvalidLimit"
when FileSystemErrorKind::TooLarge
return "TooLarge"
when FileSystemErrorKind::InvalidEncoding
return "InvalidEncoding"
when FileSystemErrorKind::UnsupportedName
return "UnsupportedName"
when FileSystemErrorKind::Busy
return "Busy"
when FileSystemErrorKind::Unsupported
return "Unsupported"
end
end

def show_error(error: FileSystemError)
case error.target
when FileSystemTarget::Host(path)
puts("error|" + error.operation + "|" + error_kind(error.kind) + "|" + path.to_s())
when FileSystemTarget::Relative(path)
puts("unexpected relative|" + path.to_s())
when FileSystemTarget::Root
puts("unexpected root")
end
return
end

def borrowed(file: File, depth: Integer, limit: Integer): Result<String, FileSystemError>
borrowed_file := file
if depth > 0
return borrowed(borrowed_file, depth - 1, limit)
end
return borrowed_file.read_text(max_bytes: limit)
end

def read_text(path: Path, limit: Integer): Result<String, FileSystemError>
return File.open(path) do |file|
try borrowed(file, 2, limit)
end
end

def write_text(path: Path, mode: FileMode, text: String): Result<Unit, FileSystemError>
return File.open(path, mode: mode) do |file|
try file.write_text(text)
end
end

def copy_bytes(source: Path, target: Path): Result<Unit, FileSystemError>
bytes := try File.open(source) do |file|
try file.read(max_bytes: 1048576)
end
return File.open(target, mode: FileMode::CreateNew) do |file|
try file.write(bytes)
end
end

def show_unit(result: Result<Unit, FileSystemError>)
case result
when Result::Ok(_value)
puts("ok")
when Result::Err(error)
show_error(error)
end
return
end

def main()
args := Process.argv()
path := Path.new(args[1])
case args[0]
when "read"
case read_text(path, args[2].to_i())
when Result::Ok(value)
puts("ok|" + value)
when Result::Err(error)
show_error(error)
end
when "write"
show_unit(write_text(path, FileMode::Write, args[2]))
when "create"
show_unit(write_text(path, FileMode::CreateNew, args[2]))
when "copy"
show_unit(copy_bytes(path, Path.new(args[2])))
when "mkdir"
show_unit(Dir.create_all(path))
when "children"
case Dir.children(path, max_entries: args[2].to_i())
when Result::Ok(entries)
entries.each do |entry|
mut kind := "Other"
case entry.kind
when DirEntryKind::File
kind = "File"
when DirEntryKind::Directory
kind = "Directory"
when DirEntryKind::Other
kind = "Other"
end
puts(entry.name + "|" + kind + "|" + entry.path.to_s())
end
when Result::Err(error)
show_error(error)
end
when "nested-result"
result := File.open(path) do |_file|
Result<String, String>::Err("domain-value")
end
case result
when Result::Err(error)
show_error(error)
when Result::Ok(inner)
case inner
when Result::Ok(value)
puts("unexpected|" + value)
when Result::Err(value)
puts("ok|" + value)
end
end
end
return
end
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('binary', type=Path)
    parser.add_argument('--reference', action='store_true')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    binary = args.binary.resolve()
    passed = []
    not_exercised = []
    with tempfile.TemporaryDirectory(prefix='scoped-filesystem-') as directory:
        root = Path(directory)
        (root / 'src').mkdir()
        (root / 'src/main.trb').write_text(SOURCE)
        config = root / 'trbconfig.jsonc'
        config.write_text(json.dumps({'name': 'scoped-filesystem-acceptance',
                                     'mode': 'go' if args.reference else 'trb',
                                     'sourceDir': 'src', 'outDir': 'out',
                                     'go': {'module': 'example.com/scoped-filesystem'}}))
        program = root / 'program'
        environment = dict(os.environ, NO_COLOR='1', TERM='dumb', TRBN_HISTORY=str(root / 'history'))
        built = subprocess.run([str(binary), 'build', '--config', str(config), '--compile',
                                '--outfile', str(program)], cwd=root, env=environment,
                               capture_output=True, timeout=120)
        assert built.returncode == 0, (built.stdout.decode(), built.stderr.decode())

        def expect(name, operation, path, *arguments, output):
            result = subprocess.run([str(program), operation, str(path), *map(str, arguments)],
                                    cwd=root, env=environment, capture_output=True, timeout=5)
            wanted = output.encode() if isinstance(output, str) else output
            assert (result.returncode, result.stdout, result.stderr) == (0, wanted, b''), (name, result)
            passed.append(name)

        def error(operation, kind, path):
            return f'error|{operation}|{kind}|{path}\n'

        data = root / 'data'
        data.mkdir()
        text = data / 'text'
        text.write_bytes(b'hello')
        expect('bounded read with recursive borrowed aliases', 'read', text, 5, output='ok|hello\n')
        expect('one byte beyond limit', 'read', text, 4, output=error('read_text', 'TooLarge', text))
        expect('negative read limit', 'read', text, -1, output=error('read_text', 'InvalidLimit', text))
        expect('zero read limit observes overflow', 'read', text, 0, output=error('read_text', 'TooLarge', text))
        empty = data / 'empty'
        empty.touch()
        expect('empty file with zero limit', 'read', empty, 0, output='ok|\n')
        invalid = data / 'invalid'
        invalid.write_bytes(b'\xff\x00\xc0\x80')
        expect('strict UTF-8', 'read', invalid, 10, output=error('read_text', 'InvalidEncoding', invalid))
        bom = data / 'bom'
        bom.write_bytes(b'\xef\xbb\xbfhello')
        expect('preserve UTF-8 BOM', 'read', bom, 8, output=b'ok|\xef\xbb\xbfhello\n')
        target = data / 'copied'
        expect('binary read and exclusive write', 'copy', invalid, target, output='ok\n')
        assert target.read_bytes() == invalid.read_bytes()
        expect('exclusive create preserves existing bytes', 'create', target, 'replacement',
               output=error('open', 'AlreadyExists', target))
        assert target.read_bytes() == invalid.read_bytes()
        expect('write truncates validated regular file', 'write', text, 'x', output='ok\n')
        assert text.read_bytes() == b'x'
        link = data / 'link'
        link.symlink_to(text.name)
        expect('ambient read follows symlink', 'read', link, 1, output='ok|x\n')
        expect('exclusive create rejects symlink', 'create', link, 'y', output=error('open', 'AlreadyExists', link))
        expect('ambient write follows symlink', 'write', link, 'y', output='ok\n')
        assert text.read_bytes() == b'y' and link.is_symlink()
        missing = data / 'missing'
        expect('missing path', 'read', missing, 1, output=error('open', 'NotFound', missing))
        expect('empty path', 'read', '', 1, output=error('open', 'InvalidPath', ''))
        expect('directory is not a regular file', 'write', data, 'x', output=error('open', 'Other', data))
        fifo = data / 'fifo'
        os.mkfifo(fifo)
        expect('FIFO read does not wait for peer', 'read', fifo, 1, output=error('open', 'Other', fifo))
        expect('FIFO write does not wait for peer', 'write', fifo, 'x', output=error('open', 'Other', fifo))
        expect('Result-valued body is nested success', 'nested-result', text, output='ok|domain-value\n')
        entries = root / 'entries'
        entries.mkdir()
        (entries / 'b').mkdir()
        (entries / 'a').write_text('a')
        (entries / 'c').symlink_to('a')
        (entries / '猫').write_text('utf8')
        names = [('a', 'File'), ('b', 'Directory'), ('c', 'Other'), ('猫', 'File')]
        expected = ''.join(f'{name}|{kind}|{entries}/{name}\n' for name, kind in names)
        expect('sorted immediate UTF-8 directory entries and symlink classification', 'children', entries, 4, output=expected)
        expect('directory limit during iteration', 'children', entries, 2, output=error('children', 'TooLarge', entries))
        expect('negative directory limit', 'children', entries, -1, output=error('children', 'InvalidLimit', entries))
        spelled = str(entries) + '/./'
        expected = ''.join(f'{name}|{kind}|{spelled}{name}\n' for name, kind in names)
        expect('directory child paths preserve parent spelling', 'children', spelled, 4, output=expected)
        invalid_name = os.fsencode(entries) + b'/\xff'
        try:
            with open(invalid_name, 'wb') as file:
                file.write(b'x')
        except OSError as failure:
            if sys.platform != 'darwin' or failure.errno != errno.EILSEQ:
                raise
            not_exercised.append({'case': 'directory rejects lossy names',
                                  'reason': 'Host filesystem rejects invalid UTF-8 names with EILSEQ; Linux coverage remains required.'})
        else:
            expect('directory rejects lossy names', 'children', entries, 10, output=error('children', 'UnsupportedName', entries))
        nested = root / 'parents' / 'nested'
        expect('create ancestors', 'mkdir', nested, output='ok\n')
        assert nested.is_dir()
        expect('existing directory succeeds', 'mkdir', nested, output='ok\n')
        expect('existing file cannot become directory', 'mkdir', text, output=error('create_all', 'Other', text))
        # The resource is closed before the returned value enters REPL history.
        session = '''import trb/std/path
import trb/std/file
import trb/std/result
import { FileSystemError } from trb/std/errors
def read_kept(path: Path): Result<String, FileSystemError>
return File.open(path) do |file|
try file.read_text(max_bytes: 1)
end
end
result := read_kept(Path.new(PATH))
case result
when Result::Ok(value)
puts("retained|" + value)
when Result::Err(error)
puts(error.operation)
end
puts(7)
'''.replace('PATH', json.dumps(str(text)))
        result = subprocess.run([str(binary), 'repl', '--config', str(config)], input=session,
                                cwd=root, env=environment, text=True, capture_output=True, timeout=30)
        assert result.returncode == 0 and not result.stderr and 'retained|y\n' in result.stdout and '7\n' in result.stdout, result
        passed.append('REPL retains ordinary value after resource closure')
    report = {'mode': 'reference' if args.reference else 'native', 'passed': passed,
              'not_exercised': not_exercised}
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
