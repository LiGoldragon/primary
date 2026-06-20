#!/usr/bin/env python3
"""Render the rebuild plan for the OWNER META-SOCKET BYPASS.

Output:
  import-batches/*.nota   (Import [(id entry) ...])  -> meta-spirit  (writes survivors, guardian-free)
  nominate.txt            ids to ChangeCertainty Zero -> spirit      (removals + merged-away sources, free)

Survivor entry rules (mirror render2):
  source_ids=[x], desc_changed=false -> ORIGINAL entry + new referents (only referents change)
  source_ids=[x], desc_changed=true  -> agent's rewritten entry
  source_ids=[x,y,...]               -> agent's unified entry written at x; y,... -> nominate
"""
import json, re, os
from collections import Counter

recs = {r['id']: r for r in json.load(open('records.json'))}
prop = json.load(open('proposals2.json'))
manifest = {m['bucket']: m for m in json.load(open('buckets/manifest.json'))}
# current active store (freshness): only touch ids still active; prefer current
# entry content for unchanged-desc survivors so concurrent edits aren't reverted.
import os.path as _p
CUR = {r['id']: r for r in json.load(open('records-current.json'))} if _p.exists('records-current.json') else recs

KEBAB = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
def is_bare(t):
    return bool(t) and not re.search(r'[\s()\[\]]', t) and ';;' not in t and '|]' not in t
def enc_str(t):
    t = t if t is not None else ""
    if is_bare(t): return t
    if any(c in t for c in '()[]'): return '[|' + t.replace('|]', '\\|]') + '|]'
    return '[' + t + ']'
def enc_ref(r): return r if KEBAB.match(r) else enc_str(r)
def enc_refs(rs): return '[' + ' '.join(enc_ref(r) for r in rs) + ']'
def enc_domain(d):
    p = [x for x in d.split('.') if x]
    acc = p[-1]
    for x in reversed(p[:-1]): acc = f'({x} {acc})'
    return acc if len(p) > 1 else f'({acc})'
def enc_domains(ds): return '[' + ' '.join(enc_domain(d) for d in ds) + ']'
def enc_entry(domains, kind, desc, cert, imp, refs, priv='Zero'):
    return f'({enc_domains(domains)} {kind} {enc_str(desc)} {cert} {imp} {priv} {enc_refs(refs)})'

VALID = ['Minimum','VeryLow','Low','Medium','High','VeryHigh','Maximum']
def cc(c): return c if c in VALID else 'Medium'

imports = []   # (id, entry_nota)
nominate = []  # ids
claimed = set()
nonkebab = []

skipped_gone = 0
for b in prop['buckets']:
    for s in b['survivors']:
        ids = [i for i in s['source_ids'] if i in recs and i not in claimed]
        if not ids: continue
        # target = first source id still ACTIVE in the current store (skip
        # already-merged/removed ones); if none active, the arrow already
        # landed elsewhere — skip.
        active_ids = [i for i in ids if i in CUR]
        if not active_ids:
            skipped_gone += 1; claimed.update(ids); continue
        claimed.update(ids)
        refs = []
        for r in s['referents']:
            if not KEBAB.match(r): nonkebab.append(r)
            refs.append(r)
        refs = list(dict.fromkeys(refs))
        target = active_ids[0]
        if len(active_ids) >= 2 or s['desc_changed']:
            entry = enc_entry(s['domains'], s['kind'], s['desc'], cc(s['certainty']), s['importance'], refs)
        else:
            o = CUR[target]   # current content (don't revert concurrent edits)
            entry = enc_entry(o['domains'], o['kind'], o['desc'], o['certainty'], o['importance'], refs)
        imports.append((target, entry))
        nominate.extend([i for i in active_ids[1:]])   # merged-away sources still active
    for r in b['removed']:
        if r['id'] in CUR and r['id'] not in claimed:
            claimed.add(r['id']); nominate.append(r['id'])

# write batched import files
os.makedirs('import-batches', exist_ok=True)
for f in os.listdir('import-batches'): os.remove(os.path.join('import-batches', f))
BATCH = 40
batches = [imports[i:i+BATCH] for i in range(0, len(imports), BATCH)]
for n, batch in enumerate(batches):
    body = ' '.join(f'({i} {e})' for i, e in batch)
    with open(f'import-batches/{n:03d}.nota', 'w') as f:
        f.write(f'(Import [{body}])')
with open('nominate.txt', 'w') as f:
    f.write('\n'.join(nominate))

print(f"skipped (already merged/removed): {skipped_gone}"); print(f"imports: {len(imports)} survivors in {len(batches)} batches of {BATCH}")
print(f"nominate: {len(nominate)} ids (merged-away sources + removals)")
print(f"projected active after: {len(imports)} (was 1323)")
print(f"non-kebab referents: {len(nonkebab)} {sorted(set(nonkebab))[:20]}")
print(f"partition check: claimed {len(claimed)} of 1323 ({'OK' if len(claimed)==1323 else 'MISMATCH'})")
