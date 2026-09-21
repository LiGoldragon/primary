#!/usr/bin/env python3
"""Metadata-only seven-day Codex/Claude activity aggregate; never emits content."""
import csv, datetime as D, glob, json, os, pathlib, collections
from zoneinfo import ZoneInfo
OUT=pathlib.Path('/tmp/field-world-20260921/activity')
NOW=D.datetime.now(D.timezone.utc); SINCE=NOW-D.timedelta(days=7); TZ=ZoneInfo('America/Mexico_City')
def stamp(v):
    try:
        if isinstance(v,(int,float)): return D.datetime.fromtimestamp(v/1000 if v>1e11 else v,D.timezone.utc)
        return D.datetime.fromisoformat(v.replace('Z','+00:00')).astimezone(D.timezone.utc)
    except Exception:return None
def add_model(rows,system,t,model,usage,metric='usage_record'):
    z=t.astimezone(TZ); r={'system':system,'model':str(model),'metric':metric,'hour':z.hour,'period':'day_06_18' if 6<=z.hour<18 else 'night_18_06','records':1}
    if usage:
        r.update(input_tokens=int(usage.get('input_tokens',0) or 0),cached_or_cache_read_tokens=int(usage.get('cached_input_tokens',usage.get('cache_read_input_tokens',0)) or 0),cache_write_or_creation_tokens=int(usage.get('cache_write_input_tokens',usage.get('cache_creation_input_tokens',0)) or 0),output_tokens=int(usage.get('output_tokens',0) or 0))
    rows.append(r)
def scan():
    codex_turn={}; codex_model={}; codex_active={}; cfiles=cbytes=cbad=0
    for p in glob.glob('/home/li/.codex/**/*.jsonl',recursive=True):
        try:
            if os.path.getmtime(p)<SINCE.timestamp():continue
            cfiles+=1;cbytes+=os.path.getsize(p)
            with open(p,errors='replace') as f:
                for line in f:
                    try:x=json.loads(line)
                    except Exception:cbad+=1;continue
                    t=stamp(x.get('timestamp'))
                    if not t or t<SINCE:continue
                    q=x.get('payload') if isinstance(x.get('payload'),dict) else {}
                    typ=x.get('type'); tid=q.get('turn_id'); th=q.get('thread_id')
                    if typ=='turn_context' and tid and q.get('model'): codex_model[tid]=q['model']
                    elif typ=='token_usage_record' and tid and isinstance(q.get('turn_token_usage'),dict):
                        k=(th,tid); prev=codex_turn.get(k)
                        if not prev or t>=prev[0]:codex_turn[k]=(t,q['turn_token_usage'])
                    elif typ=='event_msg' and isinstance(q.get('started_at_ms'),(int,float)) and isinstance(q.get('completed_at_ms'),(int,float)):
                        s,e=q['started_at_ms'],q['completed_at_ms']; k=(th,tid,s,e)
                        if e>s:codex_active[k]=(t,min(e-s,900000),e-s>900000)
        except Exception:pass
    claude={}; afiles=abytes=abad=0
    for p in glob.glob('/home/li/.claude/projects/**/*.jsonl',recursive=True):
        try:
            if os.path.getmtime(p)<SINCE.timestamp():continue
            afiles+=1;abytes+=os.path.getsize(p)
            with open(p,errors='replace') as f:
                for line in f:
                    try:x=json.loads(line)
                    except Exception:abad+=1;continue
                    if x.get('type')!='assistant':continue
                    t=stamp(x.get('timestamp'))
                    if not t or t<SINCE:continue
                    m=x.get('message')
                    if not isinstance(m,dict) or not isinstance(m.get('usage'),dict):continue
                    k=m.get('id') or x.get('uuid')
                    if k and (k not in claude or t>=claude[k][0]):claude[k]=(t,m.get('model','unknown'),m['usage'])
        except Exception:pass
    rows=[]
    for (th,tid),(t,u) in codex_turn.items():add_model(rows,'codex',t,codex_model.get(tid,'unknown'),u)
    for t,m,u in claude.values():add_model(rows,'claude',t,m,u)
    for (th,tid,s,e),(t,d,capped) in codex_active.items():
        z=t.astimezone(TZ);rows.append({'system':'codex','model':str(codex_model.get(tid,'unknown')),'metric':'event_active_proxy','hour':z.hour,'period':'day_06_18' if 6<=z.hour<18 else 'night_18_06','records':1,'duration_ms_capped':d,'duration_was_capped':int(capped)})
    coverage={'window_start_utc':SINCE.isoformat(),'window_end_utc':NOW.isoformat(),'timezone':'America/Mexico_City','codex':{'files':cfiles,'bytes':cbytes,'parse_errors':cbad,'usage_dedup_keys':'(thread_id,turn_id), latest event timestamp','active_dedup_keys':'(thread_id,turn_id,started_at_ms,completed_at_ms)','usage_semantics':'last native turn_token_usage snapshot; cached input is reported separately and never added to input'},'claude':{'files':afiles,'bytes':abytes,'parse_errors':abad,'usage_dedup_keys':'assistant message id (or event uuid), latest event timestamp','usage_semantics':'input, cache_read, cache_creation, and output remain separate'},'duration_semantics':'Codex event active proxy is explicit event started/completed duration capped at 900000 ms per deduplicated event. It is not session span, compute time, wall-clock occupancy, or person-hours. Claude explicit generation duration was not found in selected metadata.'}
    sums=collections.defaultdict(lambda:collections.Counter())
    for r in rows:
        k=(r['system'],r['model'],r['metric'],r['period'],r['hour'])
        for a,v in r.items():
            if isinstance(v,int):sums[k][a]+=v
    out=[]
    for (system,model,metric,period,hour),v in sorted(sums.items()):
        row=dict(v); row.update(system=system,model=model,metric=metric,period=period,hour=hour); out.append(row)
    (OUT/'coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')
    (OUT/'activity.json').write_text(json.dumps(out,indent=2)+'\n')
    fields=sorted({k for x in out for k in x})
    with open(OUT/'activity.csv','w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(out)
    (OUT/'METHODS.md').write_text('# Metadata activity methods\n\n'+json.dumps(coverage,indent=2)+'\n')
if __name__=='__main__':scan()
