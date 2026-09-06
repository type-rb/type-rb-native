"""Local selection diagnostic: exact-source ordinary Native build costs."""
import csv
import hashlib
import json
import os
from pathlib import Path
import statistics
import subprocess
import sys
import time

if len(sys.argv) != 6 or sys.platform != 'darwin':
    raise SystemExit('usage (Darwin): build-cost-observer.py CHECKOUT EVIDENCE BASELINE_COMPILER CANDIDATE_COMPILER QBE')
root = Path(sys.argv[1]).resolve()
evidence = Path(sys.argv[2]).resolve()
output = evidence / 'build-cost'
output.mkdir(exist_ok=False)
baseline = output / 'baseline-source'
baseline.mkdir()
revision = '1afd60c2c7257ed34fd2a2aa70cb8b9164433009'
paths = subprocess.check_output(['git','ls-tree','-r','--name-only',revision,'compiler/src'],cwd=root,text=True).splitlines()
for relative in paths:
    if relative.endswith('.trb') and not relative.endswith('_test.trb'):
        target = baseline / relative
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(subprocess.check_output(['git','show',f'{revision}:{relative}'],cwd=root))
roles = {
    'baseline': (str(Path(sys.argv[3]).resolve()), baseline / 'compiler/src/compiler.trb'),
    'candidate': (str(Path(sys.argv[4]).resolve()), root / 'compiler/src/compiler.trb'),
}
sha = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
rows = []
for phase, rounds in [('warmup',2),('retained',7)]:
    for round_index in range(1,rounds+1):
        order = ['baseline','candidate'] if round_index % 2 else ['candidate','baseline']
        for position,role in enumerate(order,1):
            directory = output / f'{phase}-{round_index}-{position}-{role}'
            directory.mkdir()
            compiler,source = roles[role]
            binary = directory / 'compiler'
            command = [compiler,'build',str(source),'--output',str(binary),'--qbe',str(Path(sys.argv[5]).resolve()),'--cc','/usr/bin/cc','--target','darwin-arm64-v0']
            (directory / 'command.json').write_text(json.dumps(command)+'\n')
            stdout = os.open(directory/'stdout',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o644)
            stderr = os.open(directory/'stderr',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o644)
            start = time.monotonic_ns()
            child = os.fork()
            if child == 0:
                try:
                    os.dup2(stdout,1); os.dup2(stderr,2)
                    os.close(stdout); os.close(stderr)
                    os.execve(compiler,command,dict(os.environ))
                except BaseException as error:
                    os.write(2,str(error).encode()); os._exit(127)
            os.close(stdout); os.close(stderr)
            _,wait_status,usage = os.wait4(child,0)
            end = time.monotonic_ns()
            status = os.waitstatus_to_exitcode(wait_status)
            valid = status == 0 and binary.is_file() and sha(binary) == sha(compiler) and not (directory/'stderr').read_bytes()
            row = dict(phase=phase,round=round_index,order=position,role=role,wall=(end-start)/1e9,cpu=usage.ru_utime+usage.ru_stime,rss=usage.ru_maxrss,status=status,fixedPoint=valid)
            rows.append(row)
            with (output/'raw.csv').open('w',newline='') as target:
                writer = csv.DictWriter(target,fieldnames=list(row)); writer.writeheader(); writer.writerows(rows)
            print(role,phase,round_index,valid,flush=True)
retained = [row for row in rows if row['phase']=='retained']
medians = {role:{metric:statistics.median(row[metric] for row in retained if row['role']==role) for metric in ['wall','cpu','rss']} for role in roles}
ratios = {metric:medians['candidate'][metric]/medians['baseline'][metric] for metric in medians['baseline']}
catastrophic = {role:{metric:max(row[metric] for row in retained if row['role']==role)/medians['baseline'][metric] for metric in medians['baseline']} for role in roles}
passed = all(row['fixedPoint'] for row in rows) and all(value<=1.05 for value in ratios.values()) and all(value<=2 for values in catastrophic.values() for value in values.values())
summary = dict(clock='time.monotonic_ns',rssScope='wait4 orchestration-root ru_maxrss, Darwin bytes',warmups=2,retained=7,medians=medians,ratios=ratios,maximumToBaselineMedianRatios=catastrophic,relativeLimit=1.05,catastrophicLimit=2,status='pass' if passed else 'fail')
(output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
raise SystemExit(0 if passed else 1)
