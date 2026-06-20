#!/usr/bin/env python3
"""Execute rendered plan.json against the live spirit daemon, capturing the
guardian's reply for every operation. Supports op-type and reversibility
filters and a dry-run so the irreversible Remove ops can be held back.

Usage:
  python3 execute.py --dry                     # print what would run
  python3 execute.py --ops reword,condense     # run only these op types
  python3 execute.py --reversible              # everything except hard remove
  python3 execute.py --ops remove              # run hard removes (after review)
  python3 execute.py --limit 5 --ops supersede # batch test
"""
import json, subprocess, sys, argparse

ap = argparse.ArgumentParser()
ap.add_argument('--dry', action='store_true')
ap.add_argument('--ops', default='')
ap.add_argument('--reversible', action='store_true')
ap.add_argument('--limit', type=int, default=0)
ap.add_argument('--skip-warn', action='store_true', help='skip ops with conflict/missing-id warnings')
ap.add_argument('--out', default='exec-log.jsonl')
a = ap.parse_args()

plan = json.load(open('plan.json'))
ops = set(x for x in a.ops.split(',') if x)
sel = []
for p in plan:
    if ops and p['op'] not in ops: continue
    if a.reversible and not p['reversible']: continue
    if a.skip_warn and p.get('warn'): continue
    if not p.get('nota'): continue
    sel.append(p)
if a.limit: sel = sel[:a.limit]

print(f"selected {len(sel)} / {len(plan)} ops  ops-filter={ops or 'ALL'} reversible={a.reversible} dry={a.dry}")
accepted=rejected=errored=0
logf = open(a.out, 'a') if not a.dry else None
for i, p in enumerate(sel):
    if a.dry:
        print(f"\n[{i+1}] {p['op']} {p['targets']}  rev={p['reversible']} warn={p.get('warn','')}")
        print("   ", p['nota'][:300])
        continue
    r = subprocess.run(['spirit', p['nota']], capture_output=True, text=True)
    reply = (r.stdout or r.stderr).strip()
    ok = r.returncode == 0 and ('Accepted' in reply or 'Superseded' in reply or 'Changed' in reply
                                or 'Retired' in reply or 'Removed' in reply or 'Clarified' in reply
                                or 'CertaintyChanged' in reply or 'RecordChanged' in reply)
    head = reply.split('(')[1].split()[0].rstrip(')') if '(' in reply else reply[:40]
    status = 'OK' if ok else ('REJECT' if r.returncode==0 else 'ERR')
    if ok: accepted+=1
    elif r.returncode==0: rejected+=1
    else: errored+=1
    rec = {'op':p['op'],'targets':p['targets'],'status':status,'reply':reply[:600],'nota':p['nota']}
    logf.write(json.dumps(rec)+'\n'); logf.flush()
    print(f"[{i+1}/{len(sel)}] {status:6s} {p['op']:10s} {p['targets']}  -> {reply[:90]}")
if logf: logf.close()
if not a.dry:
    print(f"\naccepted={accepted} rejected={rejected} errored={errored}")
