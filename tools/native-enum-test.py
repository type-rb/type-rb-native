#!/usr/bin/env python3
"""Exercise enum identity, lexical payloads and retained REPL values."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('binary', type=Path)
binary = parser.parse_args().binary.resolve()

with tempfile.TemporaryDirectory(prefix='native enum ') as temporary:
    root = Path(temporary)
    env = dict(os.environ, NO_COLOR='1', TERM='dumb', TRBN_HISTORY=str(root / 'history'))

    def repl(source, expected, errors=()):
        result = subprocess.run([str(binary), 'repl'], input=source + '\n:quit\n',
                                text=True, capture_output=True, cwd=root, env=env, timeout=30)
        assert result.returncode == 0, result
        assert result.stdout == expected, (source, result.stdout, result.stderr)
        assert len(result.stderr.splitlines()) == len(errors), result.stderr
        for message in errors:
            assert message in result.stderr, (message, result.stderr)

    declaration = 'enum Token\nText(value: String)\nEOF\nend\n'
    held = 'Token::Text(value: "held") : Token\n'
    repl(declaration + 'value := Token::Text("held")\n:type value\n'
         'enum Earlier\nFirst\nend\nvalue\n:reload\nvalue',
         held + 'Token\n' + held + 'reloaded\n' + held)

    chain = 'Chain::Link(value: 1, tail: Chain::End) : Chain\n'
    repl('enum Chain\nLink(value: Integer, tail: Chain)\nEnd\nend\n'
         'value := Chain::Link(1, Chain::End)\nenum Extra\nFirst\nend\n'
         'value\n:reload\nvalue', chain + chain + 'reloaded\n' + chain)

    (root / 'token.trb').write_text(declaration)
    alias = 'Token::Text(value: "held") : Item\n'
    repl('import { Token as Item } from token\nvalue := Item::Text("held")\n'
         'enum Earlier\nFirst\nend\nvalue\n:type value\n:reload\nvalue',
         alias + alias + 'Item\nreloaded\n' + alias)

    # Constructor arguments run in authored order; pattern labels select fields.
    repl('enum Change\nPair(id: Integer, *, before: String, after: String)\nend\n'
         'def mark(text: String): String\nputs(text)\nreturn text\nend\n'
         'value := Change::Pair(1, after: mark("new"), before: mark("old"))\n'
         'case value\nwhen Change::Pair(id, after: next_value, before: previous)\n'
         'puts(id)\nputs(previous)\nputs(next_value)\nend',
         'new\nold\nChange::Pair(id: 1, before: "old", after: "new") : Change\n'
         '1\nold\nnew\n')

    repl(declaration + 'text := "outer"\ncase Token::Text("inner")\n'
         'when Token::Text(text)\nputs(text)\nwhen Token::EOF\nputs("end")\nend\ntext',
         '"outer" : String\ninner\n"outer" : String\n')
    repl(declaration + 'value := Token::Text("kept")\n'
         'case value\nwhen Token::Text(text)\ntext = "invalid"\n'
         'when Token::EOF\nend\nvalue',
         'Token::Text(value: "kept") : Token\nToken::Text(value: "kept") : Token\n',
         ('assignment target is immutable',))

    # Named and bare imports preserve one nominal identity through file roots.
    for imported, name in (('import { Token as Item } from token', 'Item'),
                           ('import token', 'Token')):
        source = imported + '\ndef label(value: ' + name + '): String\ncase value\n'
        source += 'when ' + name + '::Text(text)\nreturn text\n'
        source += 'when ' + name + '::EOF\nreturn "end"\nend\nend\n'
        source += 'def main()\nputs(label(' + name + '::Text("imported")))\nend\n'
        (root / 'main.trb').write_text(source)
        result = subprocess.run([str(binary), 'run', str(root / 'main.trb')],
                                capture_output=True, text=True, cwd=root, env=env, timeout=30)
        assert (result.returncode, result.stdout, result.stderr) == (0, 'imported\n', ''), result

print('PASS enum payloads, labels, immutable scopes, recursive witnesses and nominal imports/replay')
