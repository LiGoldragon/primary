#!/usr/bin/env python3
"""Render the aggressive REBUILD output (survivors + removed) -> spirit NOTA.

Validates the per-bucket partition (every original id appears exactly once),
flags gaps, kebab-normalizes referents, and emits plan2.json.

  survivor source_ids=[x], desc_changed=false -> ChangeRecord(x, orig entry + referents)  [referents only]
  survivor source_ids=[x], desc_changed=true  -> ChangeRecord(x, new entry)
  survivor source_ids=[x,y,...]               -> Supersede([x,y...],[new entry])
  removed nominate/retire/remove              -> ChangeCertainty Zero / Retire / Remove
"""
import json, re, sys
from collections import Counter

recs = {r['id']: r for r in json.load(open('records.json'))}
prop = json.load(open(sys.argv[1] if len(sys.argv)>1 else 'proposals2.json'))
buckets = prop['buckets']
manifest = {m['bucket']: m for m in json.load(open('buckets/manifest.json'))}

AUTH = "you have green light to do a massive trim-down. put all the trimmed bits somewhere and when youre done give me a summary of what you took out. and assign referents to everything. also make sure referent strings only accept uncapitalized kebab-case"
ANT  = "psyche green light: massive spirit DB trim-down with referents on everything"

KEBAB = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
SPECIAL = {  # canonical lowercase proper nouns + the 16 existing capitalized referents
 'CriomOS':'criomos','CriomOS-home':'criomos-home','criomos':'criomos','criome':'criome',
 'nota':'nota','rkyv':'rkyv','lojix':'lojix','NOTA':'nota','DigitalOcean':'digital-ocean',
 'TypeReference':'type-reference','Horizon':'horizon','Android':'android','DJI-mic':'dji-mic',
 'Whisrs':'whisrs','VmHost':'vm-host','Hetzner':'hetzner','Syncthing':'syncthing','Immich':'immich',
 'Cloudflare':'cloudflare','BookOfGoldragon':'book-of-goldragon','Nexus':'nexus',
 'CredentialHandle':'credential-handle',
}
def kebabize(s):
    if s in SPECIAL: return SPECIAL[s]
    if KEBAB.match(s): return s
    t = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', s)
    t = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1-\2', t)
    t = t.replace('_','-').replace(' ','-').replace('.','-').replace('/','-')
    t = re.sub(r'-+','-',t).strip('-').lower()
    t = re.sub(r'[^a-z0-9-]','',t)
    return t

# ---- NOTA encoders ----
# Plain [text] tolerates whitespace and most punctuation but NOT ()[]; any of
# those forces the bracket-safe [|text|] form. Single bare-eligible tokens must
# stay bare (the daemon rejects redundant brackets).
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
    p=[x for x in d.split('.') if x]
    if not p: return None
    acc=p[-1]
    for x in reversed(p[:-1]): acc=f'({x} {acc})'
    return acc if len(p)>1 else f'({acc})'
def enc_domains(ds): return '[' + ' '.join(enc_domain(d) for d in ds) + ']'
def enc_entry(domains,kind,desc,cert,imp,refs,priv='Zero'):
    return f'({enc_domains(domains)} {kind} {enc_str(desc)} {cert} {imp} {priv} {enc_refs(refs)})'
def just(reason):
    return f'([({enc_str(AUTH)} (Some {enc_str(ANT)}))] {enc_str(reason)})'

VALID=['Minimum','VeryLow','Low','Medium','High','VeryHigh','Maximum']
def cc(c): return c if c in VALID else 'Medium'

# ---- partition validation ----
plan=[]
report={'buckets':[], 'missing_total':0, 'dup_total':0, 'nonkebab_fixed':0}
for b in buckets:
    name=b['bucket']
    orig=set(manifest[name]['ids'])
    seen=Counter()
    for s in b['survivors']:
        for i in s['source_ids']: seen[i]+=1
    for r in b['removed']: seen[r['id']]+=1
    covered=set(seen)
    missing=sorted(orig-covered)
    extra=sorted(covered-orig)
    dups=sorted([i for i,n in seen.items() if n>1])
    report['buckets'].append({'bucket':name,'orig':len(orig),'survivors':len(b['survivors']),
                              'removed':len(b['removed']),'missing':missing,'dups':dups,'extra':extra})
    report['missing_total']+=len(missing); report['dup_total']+=len(dups)

    claimed=set()
    def take(ids):
        out=[i for i in ids if i in recs and i not in claimed]
        claimed.update(out); return out

    # survivors
    for s in b['survivors']:
        ids=take(s['source_ids'])
        if not ids: continue
        refs=[]
        for r in s['referents']:
            k=kebabize(r)
            if k!=r: report['nonkebab_fixed']+=1
            if k: refs.append(k)
        refs=list(dict.fromkeys(refs))  # dedup, keep order
        if len(ids)>=2:
            entry=enc_entry(s['domains'],s['kind'],s['desc'],cc(s['certainty']),s['importance'],refs)
            plan.append({'op':'supersede','bucket':name,'targets':ids,'reversible':True,
                         'desc_changed':True,'summary':s['desc'][:110],'referents':refs,
                         'note':s['reason'],'nota':f'(Supersede ([{" ".join(ids)}] [{entry}] {just("Merge: "+s["reason"])}))'})
        else:
            x=ids[0]; o=recs[x]
            if not s['desc_changed']:
                # keep original desc/kind/domains/certainty/importance; only add referents
                if refs == o['referents']:
                    continue  # nothing to change
                entry=enc_entry(o['domains'],o['kind'],o['desc'],o['certainty'],o['importance'],refs)
                plan.append({'op':'referent','bucket':name,'targets':[x],'reversible':True,
                             'desc_changed':False,'summary':o['desc'][:110],'referents':refs,
                             'note':'add referents','nota':f'(ChangeRecord ({x} {entry} {just("Assign kebab referents: "+", ".join(refs))}))'})
            else:
                entry=enc_entry(s['domains'],s['kind'],s['desc'],cc(s['certainty']),s['importance'],refs)
                plan.append({'op':'rewrite','bucket':name,'targets':[x],'reversible':True,
                             'desc_changed':True,'summary':s['desc'][:110],'referents':refs,
                             'note':s['reason'],'nota':f'(ChangeRecord ({x} {entry} {just("Rewrite (condense/de-negate)+referents: "+s["reason"])}))'})
    # removed
    for r in b['removed']:
        i=r['id']
        if i in claimed or i not in recs: continue
        claimed.add(i)
        o=recs[i]; act=r['action']; summ=o['desc'][:110]
        if act=='nominate':
            plan.append({'op':'nominate','bucket':name,'targets':[i],'reversible':True,'summary':summ,
                         'note':r['reason'],'nota':f'(ChangeCertainty ({i} Zero))'})
        elif act=='retire':
            plan.append({'op':'retire','bucket':name,'targets':[i],'reversible':True,'summary':summ,
                         'note':r['reason'],'nota':f'(Retire ({i} {just("Retire: "+r["reason"])}))'})
        else:
            plan.append({'op':'remove','bucket':name,'targets':[i],'reversible':False,'summary':summ,
                         'note':r['reason'],'nota':f'(Remove ({i} {just("Hard remove: "+r["reason"])}))'})

json.dump(plan, open('plan2.json','w'), indent=1)
json.dump(report, open('partition-report.json','w'), indent=1)

opc=Counter(p['op'] for p in plan)
content_writes=opc['supersede']+opc['rewrite']+opc['referent']
absorbed=sum(len(p['targets']) for p in plan if p['op']=='supersede')
removed=opc['nominate']+opc['retire']+opc['remove']
# active after = survivors that remain. each supersede->1, each rewrite/referent->1, plus untouched(missing) kept
survivors_active = opc['supersede']+opc['rewrite']+opc['referent']
# records neither in plan nor removed (missing) stay active unchanged
print("ops:", dict(opc))
print(f"content writes (guardian-judged): {content_writes}  (supersede {opc['supersede']}, rewrite {opc['rewrite']}, referent-only {opc['referent']})")
print(f"merges absorb {absorbed} source records into {opc['supersede']} unified records")
print(f"removed: {removed} (nominate {opc['nominate']}, retire {opc['retire']}, remove {opc['remove']})")
print(f"partition: missing total={report['missing_total']} dup total={report['dup_total']} nonkebab fixed={report['nonkebab_fixed']}")
bad=[x for x in report['buckets'] if x['missing'] or x['dups'] or x['extra']]
for x in bad[:40]: print(f"  {x['bucket']}: missing={x['missing']} dups={x['dups']} extra={x['extra']}")
print("wrote plan2.json + partition-report.json")
