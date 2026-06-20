#!/usr/bin/env python3
"""Partition records into balanced topical buckets (each record once).
Group by primary (first) domain's theme segment; split big themes into
~55-record chunks; merge tiny themes into a catch-all. Write per-bucket
compact record files for the analysis agents to read."""
import json, re, os
from collections import defaultdict

recs = json.load(open('records.json'))
by_id = {r['id']: r for r in recs}

def theme(r):
    d = r['domains'][0] if r['domains'] else 'Misc'
    seg = d.split('.')
    # Technology.Software.<Area>.<Leaf> -> use Area.Leaf for finer topical grouping
    if len(seg) >= 4 and seg[0]=='Technology':
        return f"{seg[2]}.{seg[3]}"
    if len(seg) >= 3 and seg[0]=='Technology':
        return seg[2]
    return seg[-1]

groups = defaultdict(list)
for r in recs:
    groups[theme(r)].append(r)

# Keep coherent domains WHOLE (agglomeration needs all same-topic records
# together); only split if truly huge. Merge tiny domains into a catch-all.
CHUNK=150; TINY=14
buckets={}
catchall=[]
for t,rs in sorted(groups.items(), key=lambda x:-len(x[1])):
    if len(rs) < TINY:
        catchall.extend(rs); continue
    if len(rs) <= CHUNK:
        buckets[t]=rs
    else:
        for k in range((len(rs)+CHUNK-1)//CHUNK):
            buckets[f"{t}#{k+1}"]=rs[k*CHUNK:(k+1)*CHUNK]
# pack catchall into chunks
for k in range((len(catchall)+CHUNK-1)//CHUNK):
    buckets[f"Misc#{k+1}"]=catchall[k*CHUNK:(k+1)*CHUNK]

os.makedirs('buckets', exist_ok=True)
manifest=[]
total=0
for name in sorted(buckets):
    rs=buckets[name]
    total+=len(rs)
    safe=re.sub(r'[^A-Za-z0-9]+','_',name)
    path=f"buckets/{safe}.txt"
    with open(path,'w') as f:
        for r in rs:
            f.write(f"ID {r['id']} | {r['kind']} | certainty={r['certainty']} importance={r['importance']} | domains={';'.join(r['domains'])} | referents={','.join(r['referents']) or '(none)'}\n")
            f.write(f"DESC: {r['desc']}\n\n")
    manifest.append({'bucket':name,'file':path,'count':len(rs),'ids':[r['id'] for r in rs]})

json.dump(manifest, open('buckets/manifest.json','w'), indent=1)
print(f"{len(buckets)} buckets, {total} records (expect {len(recs)})")
for m in manifest: print(f"  {m['count']:3d}  {m['bucket']}")
