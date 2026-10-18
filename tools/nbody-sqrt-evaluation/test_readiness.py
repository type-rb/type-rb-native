import copy
import unittest
import json
import hashlib
from pathlib import Path
import tempfile
from unittest.mock import patch
import readiness


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.ir = {case: {role: readiness.expected_ir(case, role) for role in ('previous', 'native')}
                   for case in readiness.CASES}

    def test_expected_sqrt_lowering_and_control(self):
        readiness.validate_ir(self.ir)

    def test_changed_calls_stop_before_timing(self):
        for case in readiness.CASES:
            for role in ('previous', 'native'):
                for field in self.ir[case][role]:
                    changed = copy.deepcopy(self.ir)
                    changed[case][role][field] += 1
                    with self.assertRaises(ValueError): readiness.validate_ir(changed)

    def test_inspection_separates_consumer_from_other_functions(self):
        other = 'function d $trbnf9(d %x) {\n %r =d call $sqrt(d %x)\n ret %r\n}\n'
        body = 'function $trbnf4(d %x) {\n %r =d sqrt %x\n ret\n}\n'
        self.assertEqual(readiness.inspect_ir(body + other, 'n-body'), self.ir['n-body']['native'])
        body = 'function $trbnf0() {\n ret\n}\n'
        self.assertEqual(readiness.inspect_ir(body + other, 'string-building'), self.ir['string-building']['native'])
        with self.assertRaises(ValueError): readiness.inspect_ir(other, 'n-body')

    def stats(self, allocated=100):
        return dict(collections=2, **{'automatic-collections':1,'allocated-bytes':allocated,
                    'reclaimed-bytes':allocated,'live-bytes':0,'peak-heap-bytes':100})

    def encode(self, values):
        return ''.join(f'type-rb-native-gc-stat-v1,{k},{n}\n' for k,n in values.items()).encode()

    def test_n_body_zero_automatic_collections_still_requires_full_reclamation(self):
        values = self.stats(); values['automatic-collections'] = 0
        self.assertEqual(readiness.gc_stats(self.encode(values), require_automatic=False), values)
        with self.assertRaises(ValueError): readiness.gc_stats(self.encode(values))
        for field, value in [('collections',0),('allocated-bytes',0),('reclaimed-bytes',99),('live-bytes',1)]:
            changed = dict(values); changed[field] = value
            with self.assertRaises(ValueError): readiness.gc_stats(self.encode(changed), require_automatic=False)

    def test_gc_requires_complete_real_reclamation(self):
        values = self.stats()
        self.assertEqual(readiness.gc_stats(self.encode(values)), values)
        for field, value in [('automatic-collections',0),('reclaimed-bytes',99),('live-bytes',1)]:
            changed = dict(values); changed[field] = value
            with self.assertRaises(ValueError): readiness.gc_stats(self.encode(changed))
        with self.assertRaises(ValueError): readiness.gc_stats(self.encode(values) + b'unexpected\n')
        with self.assertRaises(ValueError): readiness.gc_stats(b'')

    def test_gc_remains_identical_in_both_cases(self):
        rows = [dict(case=case,role=role,gc=self.stats())
                for case in readiness.CASES for role in ('native','previous')]
        self.assertEqual(readiness.validate_gc(rows)['unchangedCases'], ['n-body','string-building'])
        for case in readiness.CASES:
            for field in self.stats():
                changed = copy.deepcopy(rows)
                next(r for r in changed if r['case']==case and r['role']=='native')['gc'][field] += 1
                with self.assertRaises(ValueError): readiness.validate_gc(changed)
        del rows[0]['gc']
        with self.assertRaises(ValueError): readiness.validate_gc(rows)


class BackendPrerequisiteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.directory = self.root / 'tools/nbody-sqrt-evaluation'
        self.directory.mkdir(parents=True)
        self.qbe = self.root / 'qbe'
        self.qbe.write_bytes(b'synthetic qbe')
        self.backend = {'variant': 'synthetic-test'}
        self.receipt = {'inputs': {'backend': self.backend}, 'binarySHA256': readiness.digest(self.qbe)}
        self.write(self.root / 'build-info.json', self.receipt)
        self.roles, identities, rows, cases = {}, {}, [], []
        for role in ('previous', 'baseline'):
            binary = self.root / role
            binary.write_bytes(role.encode())
            self.roles[role] = {'path': str(binary)}
            identities[role] = {'sha256': readiness.digest(binary), 'bytes': binary.stat().st_size}
        for i in range(16):
            source = self.root / f'case{i}.trb'
            source.write_text('synthetic source')
            case = {'id': f'case{i}', 'source': source.name}
            cases.append(case)
            for target in ('arm64_apple', 'arm64', 'amd64_sysv'):
                rows.append(dict(case=case['id'], target=target, identical=True,
                                 sourceSHA256=readiness.digest(source)))
        self.suite = {'cases': cases}
        self.proof = {'status': 'pass', 'sourceRevision': 'a'*40, 'rows': rows}
        self.write(self.directory / 'backend-compatibility.json', self.proof)
        self.registration = {'comparison': 'a'*40, 'backend': self.backend,
                             'priorLinuxCompilers': identities,
                             'backendCompatibilitySHA256': readiness.digest(self.directory / 'backend-compatibility.json')}
        self.write(self.directory / 'registration.json', self.registration)

    def write(self, path, value):
        path.write_text(json.dumps(value))

    def run_gate(self):
        with patch.object(readiness, 'ROOT', self.root):
            return readiness.backend_preflight(str(self.qbe), self.roles, self.suite)

    def test_complete_matching_backend_is_admitted(self):
        self.assertEqual(self.run_gate(), self.proof)

    def test_tampered_backend_or_compiler_blocks_before_products(self):
        for path in (self.qbe, self.root / 'previous', self.root / 'baseline'):
            original = path.read_bytes()
            path.write_bytes(original + b'changed')
            with self.assertRaises(ValueError): self.run_gate()
            path.write_bytes(original)

    def test_incomplete_or_changed_source_proof_is_rejected(self):
        for changed in (dict(self.proof, rows=self.proof['rows'][:-1]),
                        dict(self.proof, sourceRevision='b'*40)):
            path = self.directory / 'backend-compatibility.json'
            self.write(path, changed)
            self.registration['backendCompatibilitySHA256'] = readiness.digest(path)
            self.write(self.directory / 'registration.json', self.registration)
            with self.assertRaises(ValueError): self.run_gate()
        self.write(self.directory / 'backend-compatibility.json', self.proof)
        self.registration['backendCompatibilitySHA256'] = readiness.digest(self.directory / 'backend-compatibility.json')
        self.write(self.directory / 'registration.json', self.registration)
        (self.root / 'case0.trb').write_text('changed source')
        with self.assertRaises(ValueError): self.run_gate()


if __name__ == '__main__': unittest.main()
