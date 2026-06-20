#!/usr/bin/env python3
"""Execute rendered plan against the live spirit daemon with guardian-reply
capture. Concurrency speeds up the guardian (DeepSeek) round-trips, which are
the bottleneck. Filters by op type and reversibility; dry-run available.

  python3 execute.py --dry
  python3 execute.py --ops nominate                  # free, no guardian
  python3 execute.py --ops supersede,rewrite,referent --concurrency 10
  python3 execute.py --ops referent --limit 8 --concurrency 8   # throughput probe
"""
import json, subprocess, argparse, time
from concurrent.futures import ThreadPoolExecutor, as_completed

ap = argparse.ArgumentParser()
ap.add_argument('--dry', action='store_true')
ap.add_argument('--ops', default='')
ap.add_argument('--reversible', action='store_true')
ap.add_argument('--limit', type=int, default=0)
ap.add_argument('--skip-warn', action='store_true')
ap.add_argument('--concurrency', type=int, default=1)
ap.add_argument('--plan', default='plan2.json')
ap.add_argument('--out', default='exec-log.jsonl')
a = ap.parse_args()

plan = json.load(open(a.plan))
ops = set(x for x in a.ops.split(',') if x)
sel = []
done_targets = set()
# skip ops whose targets were already handled in a prior run (idempotent resume)
try:
    for line in open(a.out):
        r = json.loads(line)
        if r['status'] == 'OK':
            done_targets.update(r['targets'])
except FileNotFoundError:
    pass

for p in plan:
    if ops and p['op'] not in ops: continue
    if a.reversible and not p['reversible']: continue
    if a.skip_warn and p.get('warn'): continue
    if not p.get('nota'): continue
    if any(t in done_targets for t in p['targets']): continue
    sel.append(p)
if a.limit: sel = sel[:a.limit]

print(f"selected {len(sel)} ops  filter={ops or 'ALL'} concurrency={a.concurrency} dry={a.dry}")

def run(p):
    t0 = time.time()
    r = subprocess.run(['spirit', p['nota']], capture_output=True, text=True)
    dt = time.time() - t0
    reply = (r.stdout or r.stderr).strip()
    ok = r.returncode == 0 and any(k in reply for k in
        ('Accepted','Superseded','Changed','Retired','Removed','Clarified','RecordChanged'))
    status = 'OK' if ok else ('REJECT' if r.returncode == 0 else 'ERR')
    return p, status, reply, dt

if a.dry:
    for i, p in enumerate(sel):
        print(f"[{i+1}] {p['op']} {p['targets']} rev={p['reversible']}\n    {p['nota'][:240]}")
    raise SystemExit

accepted = rejected = errored = 0
logf = open(a.out, 'a')
t_start = time.time()
with ThreadPoolExecutor(max_workers=a.concurrency) as ex:
    futs = [ex.submit(run, p) for p in sel]
    for n, fut in enumerate(as_completed(futs), 1):
        p, status, reply, dt = fut.result()
        if status == 'OK': accepted += 1
        elif status == 'REJECT': rejected += 1
        else: errored += 1
        logf.write(json.dumps({'op':p['op'],'targets':p['targets'],'status':status,
                               'reply':reply[:600],'dt':round(dt,1),'nota':p['nota']})+'\n')
        logf.flush()
        print(f"[{n}/{len(sel)}] {status:6s} {p['op']:10s} {p['targets']} {dt:5.1f}s -> {reply[:80]}")
logf.close()
el = time.time() - t_start
print(f"\naccepted={accepted} rejected={rejected} errored={errored}  wall={el:.0f}s  rate={len(sel)/el*60:.1f}/min" if sel else "nothing to do")
