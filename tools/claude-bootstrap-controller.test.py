#!/usr/bin/env python3
import hashlib, importlib.util, json, pathlib, tempfile
p=pathlib.Path(__file__).with_name('claude-bootstrap-controller.py'); s=importlib.util.spec_from_file_location('c',p); c=importlib.util.module_from_spec(s); s.loader.exec_module(c)
with tempfile.TemporaryDirectory() as d:
 d=pathlib.Path(d); src=d/'s'; src.write_text('x'); m={'model':'m','effort':'low','role':'r','name':'fable-of-b05237','skills':['main-flow'],'sources':[{'path':'s','sha256':'a'}],'system_sources':[{'path':'s','sha256':hashlib.sha256(src.read_bytes()).hexdigest()}],'receipt_path':str(d/'r.json'),'refresh_manifest_path':str(d/'refresh.json'),'cwd':str(d)}; (d/'m.json').write_text(json.dumps(m))
 args=c.restricted_args(m,d/'mcp'); assert '--strict-mcp-config' in args and c.INITIAL_GUARD_PROMPT in args and c.resolve([{'id':'abc','sessionId':'uuid'}],'abc')['sessionId']=='uuid'
 plan=c.bootstrap_plan(m,d/'mcp2'); assert plan['cwd']==str(d) and plan['env']['CLAUDE_CODE_FORCE_SESSION_PERSISTENCE']=='1' and plan['env']['CLAUDE_CODE_CHILD_SESSION'] is None and 'fable-of-b05237' in plan['argv'] and 'SOURCE s' in plan['argv']
 old_run=c.subprocess.run; old_env=dict(c.os.environ)
 def fake_run(argv, cwd, env, capture_output, text):
  assert env['CLAUDE_CODE_FORCE_SESSION_PERSISTENCE']=='1' and 'CLAUDE_CODE_CHILD_SESSION' not in env
  return type('Done',(),{'returncode':0,'stdout':'started 01234567-0000-4000-8000-000000000000','stderr':''})()
 c.os.environ['CLAUDE_CODE_CHILD_SESSION']='1'; c.subprocess.run=fake_run
 receipt=c.run_bootstrap(m,d/'mcp4'); assert receipt['status']=='bootstrap-created' and json.loads((d/'r.json').read_text())['session_id']==receipt['session_id'] and json.loads((d/'refresh.json').read_text())['session_id']==receipt['session_id']
 c.subprocess.run=old_run; c.os.environ.clear(); c.os.environ.update(old_env)
 payload={'session_id':receipt['session_id'],'model':'m','effort':'low','role':'r','skills':['main-flow'],'sources':[{'path':'s','sha256':'a'}]}; ack='BOOTSTRAP_READY '+hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 native=d/'native.json'; native.write_text(json.dumps({'session_id':receipt['session_id'],'model':'m','effort':'low','native_main_flow':{'observed':True},'generation':{'acknowledged':ack,'skills':[{'skill':'main-flow'}]}}))
 assert c.record_native_refresh(m,native)['status']=='bootstrap-ready' and c.activation_args(m,json.loads((d/'r.json').read_text()))[:2]==['--resume',receipt['session_id']]
 c.persist(m,{'status':'bootstrap-ready','session_id':'uuid','model':'m','effort':'low'})
 assert c.activation_args(m,json.loads((d/'r.json').read_text()))[:2]==['--resume','uuid']
 assert '--bg' not in c.continuation_args(m,'uuid',d/'mcp3') and '--tools' in c.continuation_args(m,'uuid',d/'mcp3')
 try:c.resolve([{'id':'ax','sessionId':'a1'},{'id':'ay','sessionId':'a2'}],'a')
 except RuntimeError:pass
 else:raise AssertionError('ambiguous prefix accepted')
print('claude-bootstrap-controller fixtures passed')
