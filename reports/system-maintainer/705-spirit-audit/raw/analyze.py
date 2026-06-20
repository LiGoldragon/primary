#!/usr/bin/env python3
import json, re
from collections import Counter, defaultdict

recs = json.load(open('records.json'))
N = len(recs)
print(f"=== {N} active records ===\n")

# --- domain histogram ---
dc = Counter()
for r in recs:
    for d in r['domains']: dc[d]+=1
print("--- domains (top 30) ---")
for d,c in dc.most_common(30): print(f"  {c:4d}  {d}")
print(f"  ...{len(dc)} distinct domains total\n")

# --- length buckets ---
buckets = Counter()
for r in recs:
    L=len(r['desc'])
    b = '0-150' if L<150 else '150-300' if L<300 else '300-500' if L<500 else '500-800' if L<800 else '800-1200' if L<1200 else '1200+'
    buckets[b]+=1
print("--- desc length buckets ---")
for b in ['0-150','150-300','300-500','500-800','800-1200','1200+']:
    print(f"  {b:10s} {buckets[b]:4d}")
essays = [r for r in recs if len(r['desc'])>=800]
print(f"  mini-essays (>=800 chars): {len(essays)}  total chars in them: {sum(len(r['desc']) for r in essays)}\n")

# --- negative-guideline keyword scan ---
NEG = re.compile(r'\b(never|don\'?t|do not|must not|cannot|can\'?t|forbidden|forbid|prohibit|avoid|not a|is not|are not|no longer|instead of|rather than|stop |reject|disallow|illegal|banned?|wrong|violat)\b', re.I)
neg = []
for r in recs:
    hits = NEG.findall(r['desc'])
    if hits: neg.append((r,len(hits)))
neg.sort(key=lambda x:-x[1])
print(f"--- negative-keyword records: {len(neg)} ({100*len(neg)//N}%) ---")
print("    by kind:", dict(Counter(r['kind'] for r,_ in neg)))
# strongly-negative: starts with negation or high hit density
strong = [(r,h) for r,h in neg if h>=3 or re.match(r'\s*(never|don\'?t|do not|no |not |avoid|forbidden)', r['desc'], re.I)]
print(f"    strongly-negative candidates: {len(strong)}\n")

# --- standalone clarifications ---
clar = [r for r in recs if r['kind']=='Clarification']
clar_word = [r for r in clar if re.match(r'\s*clarif', r['desc'], re.I) or 'clarification' in r['desc'][:60].lower()]
print(f"--- Clarification records: {len(clar)};  desc opens with 'clarif': {len(clar_word)} ---\n")

# --- near-duplicate clustering by Jaccard on content words ---
STOP=set('the a an of to in is are be and or for on with that this it as at by from not no into via per its their our we you i an be can will should must may not do does done than then so such each any all one two more most less when where which who what how why if but also only same other new used use using uses'.split())
def words(t):
    return set(w for w in re.findall(r'[a-z0-9\-]+', t.lower()) if len(w)>2 and w not in STOP)
ws=[words(r['desc']) for r in recs]
pairs=[]
for i in range(N):
    wi=ws[i]
    if len(wi)<4: continue
    for j in range(i+1,N):
        wj=ws[j]
        if len(wj)<4: continue
        inter=len(wi&wj)
        if inter<4: continue
        jac=inter/len(wi|wj)
        if jac>=0.45:
            pairs.append((jac,i,j))
pairs.sort(reverse=True)
# connected components
parent=list(range(N))
def find(x):
    while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
    return x
for jac,i,j in pairs:
    parent[find(i)]=find(j)
comp=defaultdict(list)
for i in range(N): comp[find(i)].append(i)
clusters=[v for v in comp.values() if len(v)>1]
clusters.sort(key=len,reverse=True)
inclust=sum(len(c) for c in clusters)
print(f"--- near-dup clusters (Jaccard>=0.45): {len(clusters)} clusters covering {inclust} records ---")
print(f"    high-similarity pairs found: {len(pairs)}")
for c in clusters[:15]:
    print(f"  cluster size {len(c)}: ids {[recs[i]['id'] for i in c][:8]}")
print()

# save artifacts for the workflow
json.dump({
  'neg_ids':[r['id'] for r,_ in neg],
  'strong_neg_ids':[r['id'] for r,h in strong],
  'essay_ids':[r['id'] for r in essays],
  'clar_ids':[r['id'] for r in clar],
  'clusters':[[recs[i]['id'] for i in c] for c in clusters],
}, open('analysis.json','w'), indent=0)
print("wrote analysis.json")
