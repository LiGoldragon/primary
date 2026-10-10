import json,os,re,subprocess,datetime
R='/git/github.com/LiGoldragon'
rows=json.load(open('census.json'))
# release cadence: 1.85 on 2025-02-20, every 42 days
base=datetime.date(2025,2,20)
def stable_at(d): return 85+((d-base).days//42)
def ver(kind,date):
    d=datetime.date.fromisoformat(date)
    s=stable_at(d)
    return f"1.{s}" if kind=='stable' else f"1.{s+2}-nightly"
cache={}
def fenix_dates(rev):
    if rev in cache: return cache[rev]
    F=f"github:nix-community/fenix/{rev}"; out={}
    for c in ['stable','complete','latest']:
        r=subprocess.run(['nix','eval','--raw',f'{F}#packages.x86_64-linux.{c}.rustc.name'],capture_output=True,text=True)
        m=re.search(r'(\d{4}-\d{2}-\d{2})$',r.stdout.strip()); out[c]=m.group(1) if m else None
    cache[rev]=out; return out
def fenix_rev(L,node):
    return L[node]['locked']['rev']
res=[]
for r in rows:
    d=r['repo']; p=os.path.join(R,d); lk=os.path.join(p,'flake.lock'); src=r['nix_rustc']; eff='no Nix build'; how=src
    L=json.load(open(lk))['nodes'] if os.path.exists(lk) else None
    try:
      if src=='rust-build':
        rb=L['root']['inputs']['rust-build']; rev=L[rb]['locked']['rev']
        newer=subprocess.run(['git','-C',R+'/rust-build','merge-base','--is-ancestor','56d1873',rev]).returncode==0
        fx=fenix_rev(L,L[rb]['inputs']['fenix'])
        if newer: eff=ver('nightly',fenix_dates(fx)['complete']); how='rust-build (nightly)'
        else:
            how='rust-build (old, file)'
            ch=r['toolchain_file']
            eff=ch if re.match(r'1\.',ch) else ver('stable',fenix_dates(fx)['stable'])+' (sha-frozen)'
      elif src.startswith('fenix'):
        fx=fenix_rev(L,L['root']['inputs']['fenix'])
        if 'complete' in src or d in ('hexis','brightness-ctl'): eff=ver('nightly',fenix_dates(fx)['complete']); how='fenix nightly'
        elif 'latest' in src: eff=ver('nightly',fenix_dates(fx)['latest']); how='fenix nightly'
        elif 'fromToolchainFile' in src: eff=r['toolchain_file']; how='fenix file'
        else: eff=ver('stable',fenix_dates(fx)['stable']); how='fenix stable'
      elif src.startswith('nixpkgs') and d=='whisrs': eff='nixpkgs rustc'; how='nixpkgs'
    except Exception as e: eff='?'+str(e)
    r['effective']=eff; r['how']=how; res.append(r)
    print(d,r['toolchain_file'],how,eff,sep=' | ',flush=True)
json.dump(res,open('effective.json','w'),indent=1)
