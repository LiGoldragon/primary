import os,re,json,glob,datetime
R='/git/github.com/LiGoldragon'
rows=[]
for d in sorted(os.listdir(R)):
    p=os.path.join(R,d)
    if not os.path.isfile(os.path.join(p,'Cargo.toml')): continue
    row={'repo':d}
    tc=os.path.join(p,'rust-toolchain.toml')
    m=re.search(r'channel\s*=\s*"([^"]+)"',open(tc).read()) if os.path.exists(tc) else None
    row['toolchain_file']=m.group(1) if m else '-'
    eds=set()
    for c in glob.glob(p+'/**/Cargo.toml',recursive=True):
        if '/target/' in c or '/vendor/' in c: continue
        for e in re.findall(r'^edition\s*=\s*"?(\d+)',open(c,errors='ignore').read(),re.M): eds.add(e)
    row['edition']=','.join(sorted(eds)) or '-'
    rv=os.path.join(p,'Cargo.toml'); mm=re.search(r'rust-version\s*=\s*"([^"]+)"',open(rv).read()); row['msrv']=mm.group(1) if mm else '-'
    fl=os.path.join(p,'flake.nix'); src='-'
    if os.path.exists(fl):
        t=open(fl).read()
        hits=re.findall(r'fenix\.packages\.\$\{[^}]+\}\.(\w+)',t)+re.findall(r'fenix\.packages\.[\w.]+?\.(stable|complete|latest|beta|minimal|default|fromToolchainFile|toolchainOf|combine)',t)
        hits+=['fenix:'+x for x in re.findall(r'\b(fromToolchainFile|toolchainOf)\b',t)]
        ro=re.findall(r'rust-bin\.(\w+)',t)
        if 'rust-build' in t: src='rust-build'
        elif hits: src='fenix:'+'/'.join(sorted(set(h.replace('fenix:','') for h in hits)))
        elif ro: src='rust-overlay:'+'/'.join(sorted(set(ro)))
        elif 'fenix' in t: src='fenix:?'
        elif 'crane' in t or 'rustPlatform' in t or 'rustc' in t or 'cargo' in t: src='nixpkgs'
        else: src='nixpkgs?'
    row['nix_rustc']=src
    lk=os.path.join(p,'flake.lock')
    if os.path.exists(lk):
        L=json.load(open(lk))['nodes']; root=L[L['root']['inputs']['nixpkgs']] if 'nixpkgs' in L['root'].get('inputs',{}) and isinstance(L['root']['inputs']['nixpkgs'],str) else None
        if root and 'locked' in root:
            row['nixpkgs_date']=datetime.datetime.utcfromtimestamp(root['locked'].get('lastModified',0)).strftime('%Y-%m-%d'); row['nixpkgs_rev']=root['locked'].get('rev','')[:12]; row['nixpkgs_owner']=root['locked'].get('owner','')
        fx=L['root']['inputs'].get('fenix')
        if isinstance(fx,str) and 'locked' in L[fx]:
            row['fenix_date']=datetime.datetime.utcfromtimestamp(L[fx]['locked']['lastModified']).strftime('%Y-%m-%d')
    feats=set()
    for f in glob.glob(p+'/**/*.rs',recursive=True):
        if '/target/' in f or '/vendor/' in f: continue
        try: feats|=set(re.findall(r'#!\[feature\(([^)]*)\)',open(f,errors='ignore').read()))
        except: pass
    row['features']=';'.join(sorted(feats)) or '-'
    rows.append(row)
json.dump(rows,open('/home/li/primary/flows/d4ae97/reports/rust-toolchain/census.json','w'),indent=1)
for r in rows: print(r['repo'],r['toolchain_file'],r['edition'],r['msrv'],r['nix_rustc'],r.get('nixpkgs_owner',''),r.get('nixpkgs_date',''),r.get('fenix_date',''),r['features'],sep=' | ')
