#!/usr/bin/env python3
import argparse,hashlib,os
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--prompt',required=True);p.add_argument('--sha256',required=True);p.add_argument('--verify',action='store_true');a=p.parse_args()
s=Path(a.prompt).read_text();assert hashlib.sha256(s.encode()).hexdigest()==a.sha256,'prompt checksum mismatch'
w='/nix/store/nmr4py6p0kwwza41l0gkhsa13k9971jb-codex-next-flow-client/bin/codex-next-flow-client'
v=[w,'-m','gpt-6.1-sol','-c','model_reasoning_effort="medium"','-s','danger-full-access','-a','never','--remote','unix:///home/li/.codex-next-8mkkxq293hk2/app-server-control/app-server-control.sock','-C','/home/li/primary',s]
if a.verify:print('VERIFIED',len(s.encode()),a.sha256,'argv',len(v))
else:os.execv(w,v)
