#!/usr/bin/env python3
import argparse,json,os,signal,time,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('--ready-fd',type=int,required=True);p.add_argument('--generation',required=True);p.add_argument('--fail',action='store_true');p.add_argument('--real',action='store_true');p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args()
if a.fail: raise SystemExit(19)
event={'event':'ready','pid':os.getpid(),'generation':a.generation}
if a.real:
 child=subprocess.Popen(a.command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 native=None;observed=None;answered=False
 for line in child.stdout:
  try:x=json.loads(line)
  except ValueError:continue
  native=native or x.get('session_id') or x.get('thread_id')
  observed=observed or x.get('model')
  # Claude stream-json assistant / Codex item.completed both prove bounded work.
  answered=answered or x.get('type') in ('assistant','item.completed','result')
 if child.wait()!=0 or not answered: raise SystemExit(20)
 event.update(native_session=native,observed_model=observed,turn_complete=True)
os.write(a.ready_fd,(json.dumps(event)+'\n').encode());os.close(a.ready_fd)
signal.signal(signal.SIGTERM,lambda *_:exit())
while True: time.sleep(.2)
