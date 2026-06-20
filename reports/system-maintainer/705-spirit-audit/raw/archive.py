#!/usr/bin/env python3
"""Build the human-readable archive of everything the trim touched.

records.json is already the complete pre-audit snapshot (every original
Entry). This produces a focused archive keyed by what happened to each
record: removed, merged-away (superseded), or rewritten/condensed. The
daemon's versioned commit log additionally retains full testimony.
"""
import json, os
recs = {r['id']: r for r in json.load(open('records.json'))}
plan = json.load(open('plan2.json'))
os.makedirs('../archive', exist_ok=True)

def fmt(o):
    return (f"- `{o['id']}` [{o['kind']} | certainty={o['certainty']} importance={o['importance']} "
            f"| domains={';'.join(o['domains'])} | referents={','.join(o['referents']) or '(none)'}]\n"
            f"  > {o['desc']}")

sections = {'remove':[], 'retire':[], 'nominate':[], 'superseded':[], 'rewritten':[]}
arch = {'removed':[], 'merged_away':[], 'rewritten':[]}
for p in plan:
    if p['op'] in ('remove','retire','nominate'):
        for i in p['targets']:
            if i in recs:
                sections[p['op']].append((recs[i], p['note']))
                arch['removed'].append({'id':i,'disposition':p['op'],'reason':p['note'],'original':recs[i]})
    elif p['op']=='supersede':
        for i in p['targets']:
            if i in recs:
                sections['superseded'].append((recs[i], f"merged -> {p['summary']}"))
                arch['merged_away'].append({'id':i,'into_summary':p['summary'],'reason':p['note'],'original':recs[i]})
    elif p['op']=='rewrite':
        for i in p['targets']:
            if i in recs:
                sections['rewritten'].append((recs[i], f"rewritten -> {p['summary']}"))
                arch['rewritten'].append({'id':i,'new_summary':p['summary'],'reason':p['note'],'original':recs[i]})

json.dump(arch, open('../archive/trimmed-records.json','w'), indent=1)

with open('../archive/trimmed-records.md','w') as f:
    f.write("# Spirit audit — archive of trimmed records\n\n")
    f.write("Full original text of every record the trim removed, merged away, or rewrote. "
            "The pre-audit dump (`raw/all-active.nota`, `raw/records.json`) holds all 1323 originals; "
            "the daemon's versioned commit log additionally retains the verbatim psyche testimony.\n\n")
    titles = {'remove':'Hard-removed (irreversible)','retire':'Retired (lineage kept)',
              'nominate':'Nominated for removal (certainty=Zero, recoverable)',
              'superseded':'Merged away into a unified record','rewritten':'Rewritten (condensed / de-negated) — original text'}
    for key in ['remove','retire','nominate','superseded','rewritten']:
        items=sections[key]
        f.write(f"## {titles[key]} ({len(items)})\n\n")
        for o,note in items:
            f.write(fmt(o)+f"\n  — _{note}_\n\n")
print(f"archive: removed={len(arch['removed'])} merged_away={len(arch['merged_away'])} rewritten={len(arch['rewritten'])}")
print("wrote ../archive/trimmed-records.md + .json")
