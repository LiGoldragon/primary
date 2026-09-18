#!/usr/bin/env python3
import importlib.util, json, pathlib, tempfile
p=pathlib.Path(__file__).with_name('claude-bootstrap-controller.py'); s=importlib.util.spec_from_file_location('c',p); c=importlib.util.module_from_spec(s); s.loader.exec_module(c)
with tempfile.TemporaryDirectory() as d:
 d=pathlib.Path(d); src=d/'s'; src.write_text('x'); m={'model':'m','effort':'low','role':'r','skills':['main-flow'],'sources':[{'path':'s','sha256':'a'}],'receipt_path':str(d/'r.json'),'session_id':'uuid'}; (d/'m.json').write_text(json.dumps(m))
 args=c.restricted_args(m,d/'mcp'); assert '--strict-mcp-config' in args and c.INITIAL_GUARD_PROMPT in args and c.resolve([{'id':'abc','sessionId':'uuid'}],'abc')['sessionId']=='uuid'
 plan=c.bootstrap_plan(m,d/'mcp2'); assert plan['cwd']=='/home/li/primary' and plan['env']['CLAUDE_CODE_FORCE_SESSION_PERSISTENCE']=='1'
 c.persist(m,{'status':'bootstrap-ready','session_id':'uuid','model':'m','effort':'low'})
 assert c.activation_args(m,json.loads((d/'r.json').read_text()))[:2]==['--resume','uuid']
 assert '--bg' not in c.continuation_args(m,'uuid',d/'mcp3') and '--tools' in c.continuation_args(m,'uuid',d/'mcp3')
 try:c.resolve([{'id':'ax','sessionId':'a1'},{'id':'ay','sessionId':'a2'}],'a')
 except RuntimeError:pass
 else:raise AssertionError('ambiguous prefix accepted')
print('claude-bootstrap-controller fixtures passed')
