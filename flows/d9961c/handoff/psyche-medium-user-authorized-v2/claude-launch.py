#!/usr/bin/env python3
import argparse,hashlib,json,subprocess,uuid
from pathlib import Path
P=Path(__file__).parent; a=argparse.ArgumentParser();a.add_argument('--cwd',required=True);a.add_argument('--launch',action='store_true');x=a.parse_args();cwd=Path(x.cwd).resolve();assert (cwd/'.jj/repo').is_dir() and not (cwd/'.jj/repo').is_symlink(),'independent JJ repo required';assert not (cwd/'.git').is_file(),'no linked Git worktree'
for n,h in json.loads((P/'artifact-manifest.json').read_text()).items():assert hashlib.sha256((P/n).read_bytes()).hexdigest()==h,f'hash mismatch: {n}'
assert '--effort' in subprocess.run(['claude','--help'],capture_output=True,text=True,check=True).stdout,'installed Claude lacks --effort; refuse launch'
prompt=(P/'first-prompt.md').read_text();append=str((P/'append-system-prompt.md').resolve());sid=str(uuid.uuid4());av=['claude','--bg','--session-id',sid,'--name','primary-psyche-medium','--remote-control','primary-psyche-medium','--model','claude-opus-4-7[1m]','--effort','medium','--append-system-prompt-file',append,'--',prompt];assert len(' '.join(av).encode())<262144
print(json.dumps({'dryRun':not x.launch,'sessionId':sid,'argv':av[:-1]+['<first-prompt contents>'],'promptBytes':len(prompt.encode()),'artifactsVerified':True,'runtimeModelVerified':False}))
if x.launch:subprocess.run(av,cwd=cwd,stdin=subprocess.DEVNULL,check=True)
