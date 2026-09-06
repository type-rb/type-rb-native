"""Cross source/compiler identity diagnostic; not an acceptance authority."""
import csv
import hashlib
import json
import os
from pathlib import Path
import statistics
import sys
import time

baseline_compiler, candidate_compiler, baseline_source, candidate_source, output = sys.argv[1:]
out = Path(output)
out.mkdir(exist_ok=False)
compilers = {'baseline': baseline_compiler, 'candidate': candidate_compiler}
sources = {'baseline': baseline_source, 'candidate': candidate_source}
cells = [(compiler, source) for compiler in compilers for source in sources]
rows = []
digests = {}
for stage in ['check', 'emit-qbe']:
    for iteration in range(9):
        order = cells[iteration % 4:] + cells[:iteration % 4]
        if iteration % 2:
            order = list(reversed(order))
        for position, (compiler, source) in enumerate(order):
            stem = f'{stage}-{iteration}-{position}-{compiler}-{source}'
            command = [compilers[compiler], stage, sources[source]]
            stdout = os.open(out / (stem + '.stdout'), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
            stderr = os.open(out / (stem + '.stderr'), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
            started = time.monotonic_ns()
            child = os.fork()
            if child == 0:
                try:
                    os.dup2(stdout, 1); os.dup2(stderr, 2)
                    os.close(stdout); os.close(stderr)
                    os.execve(command[0], command, dict(os.environ))
                except BaseException as error:
                    os.write(2, str(error).encode()); os._exit(127)
            os.close(stdout); os.close(stderr)
            _, wait_status, usage = os.wait4(child, 0)
            finished = time.monotonic_ns()
            status = os.waitstatus_to_exitcode(wait_status)
            digest = hashlib.sha256((out / (stem + '.stdout')).read_bytes()).hexdigest()
            key = (stage, compiler, source)
            valid = status == 0 and not (out / (stem + '.stderr')).read_bytes()
            valid = valid and digest == digests.setdefault(key, digest)
            if stage == 'check':
                valid = valid and (out / (stem + '.stdout')).read_bytes() == b'ok\n'
            rows.append(dict(stage=stage, phase='warmup' if iteration < 2 else 'retained',
                             iteration=iteration, order=position, compiler=compiler, source=source,
                             wall=(finished-started)/1e9, cpu=usage.ru_utime+usage.ru_stime,
                             rss=usage.ru_maxrss, status=status, valid=valid, sha256=digest))
            with (out / 'raw.csv').open('w', newline='') as target:
                writer = csv.DictWriter(target, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
            if not valid:
                raise RuntimeError(stem + ' failed')
summary = []
for stage in ['check', 'emit-qbe']:
    for compiler, source in cells:
        selected = [row for row in rows if row['stage'] == stage and row['compiler'] == compiler
                    and row['source'] == source and row['phase'] == 'retained']
        summary.append(dict(stage=stage, compiler=compiler, source=source,
                            **{metric: statistics.median(row[metric] for row in selected)
                               for metric in ['wall', 'cpu', 'rss']}))
(out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
