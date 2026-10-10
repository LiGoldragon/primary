import json,glob,re,os,sys
src=open('source.md').read()
qs=re.findall(r'^> "(.*)"$',src,re.M)
files=glob.glob('/home/li/.claude/projects/-home-li-primary/*.jsonl')
def txt(r):
    c=r.get('message',{}).get('content')
    if isinstance(c,str): return c
    if isinstance(c,list): return ''.join(b.get('text','') for b in c if isinstance(b,dict))
    return ''
recs=[]
for f in files:
    for i,l in enumerate(open(f),1):
        try:r=json.loads(l)
        except: continue
        if r.get('type')=='user':
            t=txt(r)
            if t: recs.append((os.path.basename(f)[:6],i,r.get('timestamp'),re.sub(r'\s+',' ',t)))
for q in qs:
    segs=[s.strip() for s in re.split(r'\s*\.\.\.\s*',q) if s.strip()]
    segs=[s.replace('[a fresh flow]','') for s in segs]
    print('Q:',q[:70])
    for s in segs:
        s=re.sub(r'\s+',' ',s).strip()
        hits=[(a,b,c) for a,b,c,t in recs if s in t]
        print('   seg',repr(s[:50]),'->',hits[:4])
