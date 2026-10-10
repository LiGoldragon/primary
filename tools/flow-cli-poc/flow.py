#!/usr/bin/env python3
"""Local Flow start/restart POC; fixture supervisor is deliberately not Nexus/Sema/Signal."""
import argparse,hashlib,json,os,select,shutil,signal,sqlite3,subprocess,sys,time,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent; DEFAULT=os.environ.get('FLOW_POC_DB',str(Path('/tmp')/'flow-poc.sqlite3'))
def emit(**x): print(json.dumps(x,sort_keys=True))
def db(path):
 d=sqlite3.connect(path,timeout=10,isolation_level=None);d.row_factory=sqlite3.Row;d.executescript('''PRAGMA journal_mode=WAL;
 CREATE TABLE IF NOT EXISTS flows(id TEXT PRIMARY KEY,goal,type,model,created);
 CREATE TABLE IF NOT EXISTS attempts(flow_id,generation,session,pid,proc_start,state,created,native_session,observed_model,PRIMARY KEY(flow_id,generation));
 CREATE TABLE IF NOT EXISTS origins(flow_id PRIMARY KEY,requesting_flow,session,turn,request_key,transcript_ref,kind);
 CREATE TABLE IF NOT EXISTS restart_requests(flow_id,request_key,generation,result,PRIMARY KEY(flow_id,request_key));
 CREATE TABLE IF NOT EXISTS jobs(flow_id,name,PRIMARY KEY(flow_id,name));''');return d
def stamp(pid):
 try:return Path('/proc/%s/stat'%pid).read_text().split()[21]
 except OSError:return None
def live(a): return a and a['pid'] and stamp(a['pid'])==a['proc_start']
def bridge():
 try:
  x=json.loads(Path(os.environ['FLOW_BRIDGE']).read_text())
  if all(x.get(k) for k in ('flow_id','session','request_key','transcript_ref')):return x
 except (KeyError,OSError,json.JSONDecodeError):pass
 return None
def run_child(a,gen):
 r,w=os.pipe();cmd=[sys.executable,str(HERE/'fixture_harness.py'),'--ready-fd',str(w),'--generation',str(gen)]
 if a.self_restart: cmd += ['--self-restart','--flow',a.flow_id,'--db',a.db]
 if not a.fixture:
  runtime=a.runtime or ('claude' if shutil.which('claude') else 'codex')
  if not shutil.which(runtime): raise RuntimeError('no Claude/Codex executable; use --fixture')
  prompt=a.goal if hasattr(a,'goal') else 'Resume this flow and acknowledge the requested restart.'
  # Claude/Codex receive the resolved binding, never ambient model selection.
  real=([runtime,'-p',prompt,'--output-format','stream-json','--verbose','--model',a.model,'--permission-mode','plan','--permission-prompts','none','--tools',''] if Path(runtime).name=='claude' else [runtime,'exec','--json','--model',a.model,prompt])
  cmd += ['--real',*real,*a.runtime_arg]
 if a.fail_next:cmd+=['--fail']
 p=subprocess.Popen(cmd,start_new_session=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,pass_fds=(w,));started=stamp(p.pid);os.close(w)
 ready=select.select([r],[],[],a.handshake_timeout)[0];data=os.read(r,4096) if ready else b'';os.close(r)
 try: event=json.loads(data); ok=event['event']=='ready' and event['pid']==p.pid and (a.fixture or event.get('turn_complete'))
 except (ValueError,KeyError):ok=False
 if not ok:
  if stamp(p.pid)==started:
   try:os.killpg(p.pid,signal.SIGTERM)
   except ProcessLookupError:pass
  raise RuntimeError('readiness handshake failed')
 return p.pid,started,event
def retire(a):
 if live(a):
  try:os.killpg(a['pid'],signal.SIGTERM)
  except ProcessLookupError:pass
def launch(d,a,flow,gen):
 pid,ps,event=run_child(a,gen);session=event.get('native_session') or uuid.uuid4().hex
 state='running'
 d.execute('INSERT INTO attempts VALUES(?,?,?,?,?,?,?,?,?)',(flow,gen,session,pid,ps,state,time.time(),event.get('native_session'),event.get('observed_model')));return pid,session,event.get('observed_model'),state
def start(d,a,types):
 if a.type not in types:raise RuntimeError('unknown type')
 flow=uuid.uuid4().hex;model=a.model or types[a.type]['default_model_policy']['default'];a.model=model;a.flow_id=flow;d.execute('INSERT INTO flows VALUES(?,?,?,?,?)',(flow,a.goal,a.type,model,time.time()))
 b=bridge();known=os.environ.get('FLOW_SESSION') or os.environ.get('CODEX_SESSION_ID') or os.environ.get('CLAUDE_SESSION_ID')
 kind=('bridge' if b and b.get('turn') else 'missing-turn') if b else ('missing-bridge' if known else 'terminal')
 d.execute('INSERT INTO origins VALUES(?,?,?,?,?,?,?)',(flow,b and b['flow_id'],b and b['session'] or known,b and b['turn'],b and b['request_key'],b and b['transcript_ref'],kind))
 pid,session,observed,state=launch(d,a,flow,1);emit(status=state,flow_id=flow,generation=1,session=session,pid=pid,model=model,observed_model=observed)
def restart(d,a):
 b=bridge()
 if not b:raise RuntimeError('missing origin')
 d.execute('BEGIN IMMEDIATE');target=a.flow_id or b['flow_id'];match=d.execute('SELECT flow_id FROM attempts WHERE session=?',(b['session'],)).fetchone()
 if not match: d.execute('ROLLBACK');raise RuntimeError('refused: unknown bridge session')
 if match['flow_id']!=b['flow_id']:d.execute('ROLLBACK');raise RuntimeError('refused: bridge session/flow mismatch')
 if target!=match['flow_id']:d.execute('ROLLBACK');raise RuntimeError('refused: provenance flow != target')
 a.model=d.execute('SELECT model FROM flows WHERE id=?',(target,)).fetchone()['model']
 old=d.execute("SELECT * FROM attempts WHERE flow_id=? ORDER BY generation DESC LIMIT 1",(target,)).fetchone();gen=(old['generation'] if old else 0)+1
 prior=d.execute('SELECT * FROM restart_requests WHERE flow_id=? AND request_key=?',(target,b['request_key'])).fetchone()
 if prior:d.execute('COMMIT');emit(status=prior['result'],flow_id=target,generation=prior['generation'],idempotent=True);return
 d.execute('INSERT INTO restart_requests VALUES(?,?,?,?)',(target,b['request_key'],gen,'accepted'));d.execute('COMMIT');emit(status='accepted',flow_id=target,generation=gen)
 try:pid,sess,observed,state=launch(d,a,target,gen)
 except RuntimeError:d.execute("UPDATE restart_requests SET result='failed' WHERE flow_id=? AND request_key=?",(target,b['request_key']));raise
 if old:retire(old);d.execute("UPDATE attempts SET state='retired' WHERE flow_id=? AND generation=?",(target,old['generation']))
 d.execute("UPDATE restart_requests SET result=? WHERE flow_id=? AND request_key=?",(state,target,b['request_key']));emit(status=state,flow_id=target,generation=gen,session=sess,pid=pid,observed_model=observed,predecessor_retired=bool(old))
def show(d,a):
 f=d.execute('SELECT * FROM flows WHERE id=?',(a.flow_id,)).fetchone();ats=[]
 for x in d.execute('SELECT * FROM attempts WHERE flow_id=? ORDER BY generation',(a.flow_id,)):
  z=dict(x);z['supervisor_live']=bool(live(x));ats.append(z)
 emit(flow=dict(f) if f else None,attempts=ats)
def complete(d,a):
 d.execute('UPDATE attempts SET state=? WHERE flow_id=? AND generation=?',(a.state,a.flow_id,int(a.generation)));emit(status=a.state,flow_id=a.flow_id,generation=int(a.generation))
def main():
 p=argparse.ArgumentParser();p.add_argument('--db',default=DEFAULT);p.add_argument('--fixture',action='store_true');p.add_argument('--runtime');p.add_argument('--runtime-arg',action='append',default=[]);p.add_argument('--handshake-timeout',type=float,default=2);p.add_argument('--fail-next',action='store_true');p.add_argument('--self-restart',action='store_true');s=p.add_subparsers(dest='op',required=True);q=s.add_parser('start');q.add_argument('goal');q.add_argument('--type',default='ordinary');q.add_argument('--model');q=s.add_parser('restart');q.add_argument('flow_id',nargs='?');q=s.add_parser('show');q.add_argument('flow_id');q=s.add_parser('complete');q.add_argument('flow_id');q.add_argument('generation');q.add_argument('state',choices=['completed','failed']);a=p.parse_args();d=db(a.db)
 try:
  if a.op=='start':start(d,a,json.loads((HERE/'types.json').read_text()))
  elif a.op=='restart':restart(d,a)
  elif a.op=='show':show(d,a)
  else:complete(d,a)
 except RuntimeError as e:emit(status='failed',error=str(e));return 2
if __name__=='__main__':raise SystemExit(main() or 0)
