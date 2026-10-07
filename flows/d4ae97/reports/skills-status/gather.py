import os, re, json, subprocess, glob, hashlib, collections, datetime
G='/git/github.com/LiGoldragon'; P='/home/li/primary'
def sh(c,cwd=None): return subprocess.run(c,shell=True,cwd=cwd,capture_output=True,text=True).stdout.strip()
roles=open(f'{G}/Curriculum/roles.datom').read()
standing=re.findall(r'\[([^\[\]]*)\]\s*\}\s*$',roles.strip())[0].split()
kinds=['spirit','vision','intent','knowledge','operation','trial','compensation']
def kind(n):
    for k in kinds:
        if n==k or n.startswith(k+'-'): return k
    return 'other'
def project(b,target):
    out=[];stack=[];raw=False
    for line in b.decode().split('\n'):
        st=line.strip()
        if st=='{% raw %}': raw=True; continue
        if st=='{% endraw %}': raw=False; continue
        if not raw:
            m=re.match(r'^\{% if (\w+) %\}$',st)
            if m: stack.append(m.group(1)==target); continue
            if st=='{% else %}': stack[-1]=not stack[-1]; continue
            if st=='{% endif %}': stack.pop(); continue
        if all(stack): out.append(line)
    t='\n'.join(out)
    if target=='claude': t=t.replace('\nuser-only: true\n','\ndisable-model-invocation: true\n',1)
    return t.encode()
TARGET={'claude':'claude','agents':'codex','codex':'codex','pi':'pi'}
trees={'claude':'.claude/skills/{}/SKILL.md','agents':'.agents/skills/{}/SKILL.md','codex':'.codex/skills/{}/SKILL.md','pi':'.pi/skills/{}/SKILL.md'}
skills=[]; sources=[]
for repo in ['psyche-skills','mind-skills','field-skills']:
    for f in sorted(glob.glob(f'{G}/{repo}/skills/*.md')):
        name=os.path.basename(f)[:-3]; b=open(f,'rb').read(); t=b.decode()
        m=re.search(r'^description:\s*(.*)$',t,re.M)
        gen={}
        for h,pat in trees.items():
            p=os.path.join(P,pat.format(name))
            gen[h]=('match' if open(p,'rb').read()==project(b,TARGET[h]) else 'differs') if os.path.exists(p) else 'missing'
        srcs=[]
        sm=re.search(r'^## Sources\n(.*?)(?=^## |\Z)',t,re.M|re.S)
        if sm:
            for line in sm.group(1).splitlines():
                mm=re.match(r'^(\S+) (\S+)$',line.strip())
                if mm: srcs.append([mm.group(1),mm.group(2)])
        sources+= [[name]+s for s in srcs]
        skills.append(dict(name=name,kind=kind(name),repo=repo,description=m.group(1).strip() if m else '',bytes=len(b),tokens=round(len(b)/4),standing=name in standing,generated=gen,sources=len(srcs)))
names={s['name'] for s in skills}
treecounts={h:len(glob.glob(os.path.join(P,pat.format('*')))) for h,pat in trees.items()}
extra={h:sorted(set(os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(P,pat.format('*'))))-names) for h,pat in trees.items()}
# deployment
svc=sh('systemctl --user is-active curriculum-nexus.service'); since=sh("systemctl --user show curriculum-nexus.service -p ActiveEnterTimestamp --value")
cur_skills=glob.glob(f'{G}/Curriculum/skills/*') ; review_unapproved=len(glob.glob(f'{G}/Curriculum/review/unapproved/*.md')); review_retired=len(glob.glob(f'{G}/Curriculum/review/retired/*.md'))
# vc
def repo_vc(path,branch='main'):
    return dict(head=sh('git rev-parse --short=9 HEAD',path),main=sh(f'git rev-parse --short=9 {branch}',path),origin_main_tracking=sh('git rev-parse --short=9 origin/main',path),origin_main_remote=sh('git ls-remote origin main',path)[:9],ahead_behind=sh('git rev-list --left-right --count HEAD...origin/main',path),dirty=len([l for l in sh('git status --porcelain',path).splitlines() if l]),last=sh(f"git log -1 --format='%ad|%s' --date=iso {branch}",path))
vc={r:repo_vc(f'{G}/{r}') for r in ['psyche-skills','mind-skills','field-skills','Curriculum']}
pv=repo_vc(P); pv['branch']=sh('git branch --show-current',P) or '(detached HEAD)'
pv['last5']=[dict(zip(['hash','date','subject'],l.split('|',2))) for l in sh("git log origin/main -5 --format='%h|%ad|%s' --date=iso",P).splitlines()]
por=[l for l in sh('git status --porcelain',P).splitlines() if l]
top=collections.Counter()
for l in por:
    path=l[3:].split(' -> ')[-1].strip('"'); top[path.split('/')[0]]+=1
pv['dirty_by_top']=dict(top.most_common())
gt={}
for h in ['.claude','.agents','.codex','.pi','.opencode']:
    tracked=len([x for x in sh(f'git ls-files {h}/skills',P).splitlines() if x])
    d=[l for l in por if (l[3:].split(' -> ')[-1].strip('"')).startswith(h+'/') or l[3:].startswith(h+'/')]
    gt[h]=dict(tracked_files=tracked,uncommitted_entries=len(d))
pv['generated_trees']=gt
# vision migration
vis=dict(Vision_exists=os.path.isdir(f'{P}/Vision'),Vision_files=sh(f'find {P}/Vision -type f | wc -l') if os.path.isdir(f'{P}/Vision') else 0,Intent_exists=os.path.isdir(f'{P}/Intent'),vision_raw_files=int(sh(f'find {P}/vision-raw -type f -name "*.md" | wc -l') or 0))
vis['Vision_listing']=sh(f'cd {P}/Vision && find . -type f | sort').splitlines() if vis['Vision_exists'] else []
raw=[]
added={}
out=sh("git log --diff-filter=A --format='@@%ad' --date=short --name-only -- 'flows/*/vision/*' 'flows/*/notion/*' 'vision-raw/*'",P)
d=None
for l in out.splitlines():
    if l.startswith('@@'): d=l[2:]
    elif l.strip(): added[l.strip()]=d  # git log newest-first; last write wins => oldest add
for f in sorted(glob.glob(f'{P}/flows/*/vision/*.md')+glob.glob(f'{P}/flows/*/notion/*.md')+glob.glob(f'{P}/vision-raw/*.md')):
    rel=os.path.relpath(f,P); parts=rel.split('/')
    if parts[0]=='vision-raw': flow,cat='vision-raw','vision-raw'
    else: flow,cat=parts[1],parts[2]
    t=open(f,errors='replace').read(); entries=len(re.findall(r'^## ',t,re.M))
    dates=re.findall(r'^--.*?(20\d\d-\d\d)-\d\d',t,re.M)
    rec=os.path.basename(f)[:-3]
    if rel not in added: added[rel]=(sh(f"git log --follow --diff-filter=A --format=%ad --date=short -- '{rel}'",P).splitlines() or [None])[-1]
    raw.append(dict(path=rel,flow=flow,dir=cat,record=rec,archive=rec.startswith('archive-'),entries=entries,dated_entries=len(dates),entry_months=dict(collections.Counter(dates)),added=added.get(rel)))
srcset={(a,b) for _,a,b in sources}
for r in raw: r['distilled']=(r['flow'],r['record']) in srcset or (r['record'].startswith('archive-') and (r['flow'],r['record'][8:]) in srcset)
matched={(r['flow'],r['record']) for r in raw}|{(r['flow'],r['record'][8:]) for r in raw if r['archive']}
unresolved=sorted({f'{a} {b}' for a,b in srcset if (a,b) not in matched})
bym=collections.defaultdict(lambda: dict(files=0,entries=0,distilled_files=0,distilled_entries=0))
for r in raw:
    m=r['added'][:7] if r['added'] else 'uncommitted'; x=bym[m]; x['files']+=1; x['entries']+=r['entries']
    if r['distilled']: x['distilled_files']+=1; x['distilled_entries']+=r['entries']
data=dict(measured_at=datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
 skills=skills,standing_set=standing,tree_counts=treecounts,tree_extra=extra,
 deployment=dict(service=svc,active_since=since,curriculum_skills_dir_entries=len(cur_skills),curriculum_review_unapproved=review_unapproved,curriculum_review_retired=review_retired),
 vc=dict(primary=pv,repos=vc,repair_pause='Primary commit/JJ/index operations paused by d4ae97 while Field 42265e repairs malformed trees and index duplicates (flows/0c85a3/summary.md); no all-clear recorded.'),
 vision=dict(**vis,raw=raw,by_month=dict(sorted(bym.items())),sources=[dict(skill=a,flow=b,record=c) for a,b,c in sources],unresolved_sources=unresolved))
json.dump(data,open('/home/li/primary/flows/d4ae97/reports/skills-status/data.json','w'),indent=1)
S=skills
print(len(S),collections.Counter(s['repo'] for s in S),collections.Counter(s['kind'] for s in S))
print('standing',[s for s in standing if s not in names], sum(s['standing'] for s in S))
for h in trees: print(h,treecounts[h],collections.Counter(s['generated'][h] for s in S),extra[h])
print([ (s['name'],s['generated']) for s in S if set(s['generated'].values())!={'match'}])
print(svc,since,len(cur_skills),review_unapproved,review_retired)
print(json.dumps(pv,indent=0)[:1500]); print(vc)
print({k:v for k,v in vis.items()})
print('raw files',len(raw),'entries',sum(r['entries'] for r in raw),'archive',sum(r['archive'] for r in raw),'distilled',sum(r['distilled'] for r in raw),'entries distilled',sum(r['entries'] for r in raw if r['distilled']),'dirs',collections.Counter(r['dir'] for r in raw))
print('sources lines',len(sources),'unique',len(srcset),'unresolved',len(unresolved),unresolved[:15])
print(dict(sorted(bym.items())))
print('no added date',sum(1 for r in raw if not r['added']), 'dated entries',sum(r['dated_entries'] for r in raw))
