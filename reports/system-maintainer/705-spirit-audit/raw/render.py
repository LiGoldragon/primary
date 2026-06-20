#!/usr/bin/env python3
"""Render verified structured proposals -> exact `spirit` NOTA commands.

Input:  proposals.json  (the workflow return: {buckets:[...], tally})
        records.json     (original entries, for reword/condense/retire metadata)
Output: plan.json        (one entry per operation: op, targets, nota, reversible, reason, summary)

I (the maintainer) own this encoding so the live intent-layer writes are
provably correct, not trusted to a subagent's NOTA spelling.
"""
import json, re, sys

recs = {r['id']: r for r in json.load(open('records.json'))}
prop = json.load(open('proposals.json'))
buckets = prop['buckets'] if isinstance(prop, dict) else prop

# verbatim psyche authorization (testimony for every maintenance op)
AUTH = "I want its size reduced, negative guidelines removed unless absolutely necessary, and many records agglomerated if they obviously can be worded in a unified record instead of many"
ANT  = "psyche directive: deep audit of the spirit database"

def enc_str(t):
    """Encode a free-text string as NOTA [text] or [|text|]."""
    t = t if t is not None else ""
    if '[' in t or ']' in t:
        return '[|' + t.replace('|]', '\\|]') + '|]'
    return '[' + t + ']'

def enc_ref(r):
    if re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._\-/@]*', r):
        return r
    return enc_str(r)

def enc_refs(refs):
    return '[' + ' '.join(enc_ref(r) for r in refs) + ']'

def enc_domain(dotted):
    parts = [p for p in dotted.split('.') if p]
    if not parts: return None
    acc = parts[-1]
    for p in reversed(parts[:-1]):
        acc = f'({p} {acc})'
    # single-segment domain would be a bare atom, but taxonomy domains are >=2
    return acc if len(parts) > 1 else f'({acc})'

def enc_domains(dotteds):
    return '[' + ' '.join(enc_domain(d) for d in dotteds) + ']'

def enc_entry(domains, kind, desc, certainty, importance, referents, privacy='Zero'):
    return f'({enc_domains(domains)} {kind} {enc_str(desc)} {certainty} {importance} {privacy} {enc_refs(referents)})'

def just(reasoning, antecedent=ANT, quote=AUTH):
    ant = f'(Some {enc_str(antecedent)})' if antecedent else 'None'
    return f'([({enc_str(quote)} {ant})] {enc_str(reasoning)})'

VALID_C = ['Minimum','VeryLow','Low','Medium','High','VeryHigh','Maximum']
def clamp_c(c):
    return c if c in VALID_C else 'Medium'

plan = []
seen = {}   # id -> first op that claimed it (detect conflicts)

def claim(ids, op):
    for i in ids:
        if i in seen:
            return f"CONFLICT {i} already in {seen[i]}"
        seen[i] = op
    return None

# 1) AGGLOMERATIONS -> Supersede(old_ids, [unified_entry], just)
for b in buckets:
    for a in b['agglomerations']:
        ids = a['ids']
        miss = [i for i in ids if i not in recs]
        c = claim(ids, 'agglomeration')
        entry = enc_entry(a['domains'], a['kind'], a['unified_desc'],
                          clamp_c(a['certainty']), a['importance'], a['referents'])
        nota = f'(Supersede ([{ " ".join(ids) }] [{entry}] {just("Agglomeration: "+a["reason"])}))'
        plan.append({'op':'supersede','bucket':b['bucket'],'targets':ids,
                     'reversible':True,'note':a['reason'],
                     'summary':a['unified_desc'][:120],
                     'kind':a['kind'],'warn':c or (f"missing ids {miss}" if miss else ""),
                     'nota':nota})

# 2) NEGATIVES
for b in buckets:
    for n in b['negatives']:
        i = n['id']; r = recs.get(i)
        if n['action'] == 'keep':
            continue
        c = claim([i], 'negative')
        if n['action'] == 'retire':
            nota = f'(Retire ({i} {just("Negative guideline retired (covered affirmatively elsewhere): "+n["reason"])}))'
            plan.append({'op':'retire','bucket':b['bucket'],'targets':[i],'reversible':True,
                         'note':n['reason'],'summary':(r['desc'][:120] if r else '?'),
                         'warn':c or ('' if r else 'missing id'),'nota':nota})
        else:  # reword -> ChangeRecord (desc + referents, keep domains/kind/certainty/importance)
            if not r:
                plan.append({'op':'reword','targets':[i],'warn':'missing id','nota':'','bucket':b['bucket'],'note':n['reason'],'reversible':True,'summary':'?'})
                continue
            refs = n['new_referents'] if n.get('new_referents') else r['referents']
            entry = enc_entry(r['domains'], r['kind'], n['new_desc'],
                              clamp_c(r['certainty']), r['importance'], refs)
            nota = f'(ChangeRecord ({i} {entry} {just("Affirmative rewrite of negative guideline: "+n["reason"])}))'
            plan.append({'op':'reword','bucket':b['bucket'],'targets':[i],'reversible':True,
                         'note':n['reason'],'summary':n['new_desc'][:120],
                         'warn':c,'nota':nota})

# 3) CONDENSE -> ChangeRecord (desc + referents, keep rest)
for b in buckets:
    for cd in b['condense']:
        i = cd['id']; r = recs.get(i)
        c = claim([i], 'condense')
        if not r:
            plan.append({'op':'condense','targets':[i],'warn':'missing id','nota':'','bucket':b['bucket'],'note':cd['reason'],'reversible':True,'summary':'?'})
            continue
        refs = cd['new_referents'] if cd.get('new_referents') else r['referents']
        entry = enc_entry(r['domains'], r['kind'], cd['new_desc'],
                          clamp_c(r['certainty']), r['importance'], refs)
        nota = f'(ChangeRecord ({i} {entry} {just("Condense mini-essay to terse arrow: "+cd["reason"])}))'
        plan.append({'op':'condense','bucket':b['bucket'],'targets':[i],'reversible':True,
                     'note':cd['reason'],'summary':cd['new_desc'][:120],
                     'warn':c,'nota':nota})

# 4) REMOVALS
for b in buckets:
    for rm in b['removals']:
        i = rm['id']; r = recs.get(i)
        c = claim([i], 'removal')
        act = rm['action']
        summ = (r['desc'][:120] if r else '?')
        if act == 'nominate':
            nota = f'(ChangeCertainty ({i} Zero))'
            plan.append({'op':'nominate','bucket':b['bucket'],'targets':[i],'reversible':True,
                         'note':rm['reason'],'summary':summ,'warn':c or ('' if r else 'missing id'),'nota':nota})
        elif act == 'retire':
            nota = f'(Retire ({i} {just("Retire stale/superseded record: "+rm["reason"])}))'
            plan.append({'op':'retire','bucket':b['bucket'],'targets':[i],'reversible':True,
                         'note':rm['reason'],'summary':summ,'warn':c or ('' if r else 'missing id'),'nota':nota})
        else:  # remove (hard, irreversible)
            dup = rm.get('duplicate_of') or ''
            nota = f'(Remove ({i} {just("Hard remove "+("(exact duplicate of "+dup+") " if dup else "(mis-logged task-state) ")+rm["reason"])}))'
            plan.append({'op':'remove','bucket':b['bucket'],'targets':[i],'reversible':False,
                         'note':rm['reason'],'summary':summ,'duplicate_of':dup,
                         'warn':c or ('' if r else 'missing id'),'nota':nota})

json.dump(plan, open('plan.json','w'), indent=1)

# stats
from collections import Counter
opc = Counter(p['op'] for p in plan)
warns = [p for p in plan if p.get('warn')]
src_removed = sum(len(p['targets']) for p in plan if p['op']=='supersede')
new_from_agg = sum(1 for p in plan if p['op']=='supersede')
gross_removed = (sum(len(p['targets']) for p in plan if p['op'] in ('supersede','retire','remove','nominate')))
net_active_delta = -(src_removed - new_from_agg) - opc['retire'] - opc['remove'] - opc['nominate']
print("operations:", dict(opc))
print(f"agglomerations: {new_from_agg} unified records absorbing {src_removed} source records (net -{src_removed-new_from_agg})")
print(f"retire={opc['retire']} remove={opc['remove']} nominate={opc['nominate']} reword={opc['reword']} condense={opc['condense']}")
print(f"projected active-set change: {net_active_delta} (from {len(recs)} -> {len(recs)+net_active_delta})")
print(f"warnings/conflicts: {len(warns)}")
for w in warns[:20]: print("  WARN", w['op'], w['targets'], w['warn'])
print("wrote plan.json")
