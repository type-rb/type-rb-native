import contextlib
import copy
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import readiness


def stats(allocated=100):
    return dict(collections=2, **{'automatic-collections':1,'allocated-bytes':allocated,'reclaimed-bytes':allocated,'live-bytes':0,'peak-heap-bytes':100})


def encode(values):
    return ''.join(f'type-rb-native-gc-stat-v1,{k},{n}\n' for k,n in values.items()).encode()


class ReadinessTests(unittest.TestCase):
    def test_frozen_compiler_identity_cannot_change(self):
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/'compiler';path.write_bytes(b'fixed')
            roles={role:dict(path=str(path)) for role in ('previous','baseline')}
            expected={role:dict(sha256=readiness.digest(path),bytes=path.stat().st_size) for role in roles}
            readiness.validate_prior_compilers(roles,expected)
            for field,value in [('sha256','0'*64),('bytes',0)]:
                changed=copy.deepcopy(expected);changed['previous'][field]=value
                with self.assertRaises(ValueError): readiness.validate_prior_compilers(roles,changed)

    def test_codegen_matrix_rejects_missing_and_changed_entries(self):
        ir={case:{role:readiness.expected_ir(case,role) for role in ('previous','native')} for case in readiness.CASES}
        readiness.validate_ir(ir)
        for case in readiness.CASES:
            changed=copy.deepcopy(ir);del changed[case]
            with self.assertRaises(ValueError): readiness.validate_ir(changed)
            for role in ('previous','native'):
                for field in ir[case][role]:
                    changed=copy.deepcopy(ir);changed[case][role][field]+=1
                    with self.assertRaises(ValueError):readiness.validate_ir(changed)

    def test_ir_counts_only_application_calls_and_registered_helpers(self):
        text='function l $trbnf0() {\n call $trbn_array_grow_paced(l 0)\n ret 0\n}\nfunction $runtime() {\n call $trbn_array_grow_paced(l 0)\n ret\n}\n'
        self.assertEqual(readiness.inspect_ir(text,'closures')['pushGrowth'],1)
        with self.assertRaises(ValueError):readiness.inspect_ir('function $runtime() {}','closures')

    def test_allocation_changes_are_costs_but_reclamation_is_required(self):
        rows=[dict(case=case,role=role,gc=stats(200 if role=='native' else 100)) for case in readiness.CASES for role in ('previous','native')]
        self.assertEqual(readiness.validate_gc(rows)['ratios']['closures']['allocated-bytes'],2.)
        for field,value in [('live-bytes',1),('reclaimed-bytes',99),('automatic-collections',0)]:
            changed=copy.deepcopy(rows)
            next(row for row in changed if row['case']=='closures' and row['role']=='native')['gc'][field]=value
            with self.assertRaises(ValueError):readiness.validate_gc(changed)

    def test_scalar_control_can_have_no_automatic_gc(self):
        values=stats();values['automatic-collections']=0
        readiness.gc_stats(encode(values),require_automatic=False)
        with self.assertRaises(ValueError):readiness.gc_stats(encode(values))
        with self.assertRaises(ValueError):readiness.gc_stats(encode(values)+b'unexpected\n')

    def exercise_matrix(self,missing_pure=False):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);output=root/'observations'
            daily=root/'tools/daily-performance';daily.mkdir(parents=True)
            cases=[dict(id=case,args=[],pureGoSource=case+'.go') for case in readiness.CASES]
            for case in cases:(root/case['pureGoSource']).write_text('package main\n')
            if missing_pure:cases[0].pop('pureGoSource')
            (daily/'suite.json').write_text(json.dumps(dict(cases=cases)))
            compilers=root/'compilers.json';compilers.write_text(json.dumps({role:dict(path=role+'-tool') for role in ('native','previous','typerb-go','baseline')}))
            seen=[]
            def source(case,directory):
                (directory/'src').mkdir(parents=True);(directory/'src/main.trb').write_text('def main()\nend\n');return b'expected\n'
            def run(command,cwd,env,**unused):
                seen.append(command);stdout,stderr=b'',b''
                if len(command)>1 and command[1]=='emit-qbe':
                    case=Path(command[2]).parents[1].name;role=command[0].removesuffix('-tool')
                    wanted=readiness.expected_ir(case,role)
                    body='function l $trbnf0() {\n'
                    for key,token in readiness.IR_TOKENS.items():
                        if not key.endswith('Probe'):body+=(' '+token+'l 0)\n')*wanted[key]
                    body+=' ret 0\n}\n'
                    for key,token in readiness.IR_TOKENS.items():
                        if key.endswith('Probe'):body+=(token+'l %table) {\n ret 0\n}\n')*wanted[key]
                    stdout=body.encode()
                elif len(command)>1 and command[1]=='build':
                    flag=next(x for x in ('--output','--outfile','-o') if x in command)
                    executable=Path(command[command.index(flag)+1]);executable.write_bytes((executable.parents[1].name+'/'+executable.parent.name).encode())
                else:
                    stdout=b'expected\n'
                    if env.get('TYPE_RB_NATIVE_RUNTIME_STATS')=='1':stderr=encode(stats())
                return subprocess.CompletedProcess(command,0,stdout,stderr)
            argv=['readiness.py','--compilers',str(compilers),'--qbe','qbe','--output',str(output)]
            with patch.object(readiness,'ROOT',root),patch.object(readiness,'source_case',side_effect=source),patch.object(readiness,'validate_prior_compilers'),patch.object(readiness.shutil,'which',return_value='pure-go-tool'),patch.object(readiness.subprocess,'run',side_effect=run),patch.object(readiness.subprocess,'check_output',return_value='go version test'),patch.object(readiness.sys,'argv',argv),contextlib.redirect_stdout(io.StringIO()):
                readiness.main()
            result=json.loads((output/'readiness.json').read_text())
            self.assertEqual(result['status'],'pass');self.assertEqual(len(seen),90);self.assertEqual(len(result['rows']),20)

    def test_complete_twenty_role_matrix_uses_exactly_ninety_commands(self):
        self.exercise_matrix()

    def test_missing_comparator_does_not_shrink_the_registered_budget(self):
        with self.assertRaisesRegex(ValueError,'Incomplete readiness command budget'):self.exercise_matrix(missing_pure=True)


if __name__ == '__main__': unittest.main()
