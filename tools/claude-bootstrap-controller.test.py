#!/usr/bin/env python3
import importlib.util, json, pathlib, tempfile
p=pathlib.Path(__file__).with_name('claude-bootstrap-controller.py'); s=importlib.util.spec_from_file_location('c',p); c=importlib.util.module_from_spec(s); s.loader.exec_module(c)
with tempfile.TemporaryDirectory() as d:
 d=pathlib.Path(d); src=d/'s'; src.write_text('x'); m={'model':'m','effort':'low','role':'r','skills':['main-flow'],'sources':[{'path':'s','sha256':'a'}],'receipt_path':str(d/'r.json'),'session_id':'uuid'}; (d/'m.json').write_text(json.dumps(m))
 assert '--strict-mcp-config' in c.restricted_args(m,d/'mcp') and c.resolve([{'id':'abc','sessionId':'uuid'}],'abc')['sessionId']=='uuid'
 c.persist(m,{'status':'bootstrap-ready','session_id':'uuid','model':'m','effort':'low'})
 assert c.activation_args(m,json.loads((d/'r.json').read_text()))[1:3]==['--resume','uuid']
 try:c.resolve([{'id':'ax','sessionId':'a1'},{'id':'ay','sessionId':'a2'}],'a')
 except RuntimeError:pass
 else:raise AssertionError('ambiguous prefix accepted')
print('claude-bootstrap-controller fixtures passed')
