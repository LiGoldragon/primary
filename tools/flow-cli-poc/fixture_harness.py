#!/usr/bin/env python3
import argparse,json,os,signal,time,subprocess,sys,tempfile,uuid
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--ready-fd',type=int,required=True);p.add_argument('--generation',required=True);p.add_argument('--fail',action='store_true');p.add_argument('--real',action='store_true');p.add_argument('--self-restart',action='store_true');p.add_argument('--flow');p.add_argument('--db');p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args()
if a.fail: raise SystemExit(19)
 event={'event':'ready','pid':os.getpid(),'generation':a.generation,'native_session':'fixture-'+uuid.uuid4().hex}
if a.real:
 child=subprocess.Popen(a.command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 native=None;observed=None;answered=False
 for line in child.stdout:
  try:x=json.loads(line)
  except ValueError:continue
  native=native or x.get('session_id') or x.get('thread_id')
  observed=observed or x.get('model')
  if native and observed and not event.get('native_started'):
   event.update(native_session=native,observed_model=observed,native_pid=child.pid,native_started=True)
   os.write(a.ready_fd,(json.dumps(event)+'\n').encode());os.close(a.ready_fd)
  # Claude stream-json assistant / Codex item.completed both prove bounded work.
  answered=answered or x.get('type') in ('assistant','item.completed','result')
 if child.wait()!=0 or not answered or not event.get('native_started'):
  subprocess.run([sys.executable,str(Path(__file__).with_name('flow.py')),'--db',a.db,'complete',a.flow,a.generation,'failed'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);raise SystemExit(20)
 subprocess.run([sys.executable,str(Path(__file__).with_name('flow.py')),'--db',a.db,'complete',a.flow,a.generation,'completed'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
if not a.real: os.write(a.ready_fd,(json.dumps(event)+'\n').encode());os.close(a.ready_fd)
if a.self_restart and a.generation=='1':
 time.sleep(.25)
 fd,path=tempfile.mkstemp(prefix='flow-bridge-',text=True);os.write(fd,json.dumps({'flow_id':a.flow,'session':event['native_session'],'turn':'fixture-turn','request_key':'fixture-self','transcript_ref':'mind://fixture/self'}).encode());os.close(fd)
 env=os.environ.copy();env['FLOW_BRIDGE']=path
 subprocess.run([sys.executable,str(Path(__file__).with_name('flow.py')),'--db',a.db,'--fixture','restart',a.flow],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
signal.signal(signal.SIGTERM,lambda *_:exit())
while True: time.sleep(.2)
