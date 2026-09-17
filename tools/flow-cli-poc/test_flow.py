import json,os,sqlite3,subprocess,sys,tempfile,threading,unittest,time
from pathlib import Path
HERE=Path(__file__).parent;CMD=[sys.executable,str(HERE/'flow.py')]
class TestFlow(unittest.TestCase):
 def setUp(self):self.t=tempfile.TemporaryDirectory();self.db=str(Path(self.t.name)/'flow.db')
 def tearDown(self):self.t.cleanup()
 def call(self,*x,env={}):
  e=os.environ.copy();e.pop('FLOW_BRIDGE',None);e.update(env);r=subprocess.run([*CMD,'--db',self.db,'--fixture',*x],text=True,capture_output=True,env=e);return r.returncode,[json.loads(x) for x in r.stdout.splitlines()]
 def new(self,typ='ordinary',model=None):
  a=['start','g','--type',typ]+(['--model',model] if model else []);return self.call(*a)[1][-1]
 def bridge(self,x,key='k',flow=None,session=None):
  p=Path(self.t.name)/key;p.write_text(json.dumps({'flow_id':flow or x['flow_id'],'session':session or x['session'],'turn':'turn-7','request_key':key,'transcript_ref':'mind://fixture/7'}));return {'FLOW_BRIDGE':str(p)}
 def test_start_ready_default_and_explicit_model(self):
  self.assertEqual(self.new()['model'],'claude-sonnet-4-20250514');self.assertEqual(self.new(model='codex:high')['model'],'codex:high')
 def test_restart_all_types_exact_provenance(self):
  for typ in ('ordinary','origin-reader'):
   x=self.new(typ);rc,rows=self.call('restart',x['flow_id'],env=self.bridge(x,typ));self.assertEqual(rc,0);self.assertEqual(rows[-1]['status'],'running');self.assertEqual(rows[-1]['generation'],2)
 def test_mismatch_missing_and_failure_keeps_old(self):
  x=self.new();self.assertNotEqual(self.call('restart',x['flow_id'])[0],0);self.assertNotEqual(self.call('restart',x['flow_id'],env=self.bridge(x,'bad',flow='other'))[0],0)
  self.assertNotEqual(self.call('--fail-next','restart',x['flow_id'],env=self.bridge(x,'fail'))[0],0)
  d=sqlite3.connect(self.db);self.assertEqual(d.execute("select count(*) from attempts where state='running'").fetchone()[0],1)
 def test_concurrent_duplicate_one_successor(self):
  x=self.new();e=self.bridge(x,'same');results=[]
  ts=[threading.Thread(target=lambda:results.append(self.call('restart',x['flow_id'],env=e)[1][-1])) for _ in range(2)]
  [t.start() for t in ts];[t.join() for t in ts];self.assertEqual({r['generation'] for r in results},{2})
 def test_session_binding_refuses_lie(self):
  x=self.new();y=self.new();self.assertNotEqual(self.call('restart',x['flow_id'],env=self.bridge(x,'lie',flow=x['flow_id'],session=y['session']))[0],0)
  self.assertNotEqual(self.call('restart',x['flow_id'],env=self.bridge(x,'unknown',session='not-a-bound-session'))[0],0)
 def test_fixture_self_issued_restart(self):
  rc,rows=self.call('--self-restart','start','self');x=rows[-1]
  deadline=time.time()+3
  while time.time()<deadline:
   shown=self.call('show',x['flow_id'])[1][-1]
   if len(shown['attempts'])==2:break
   time.sleep(.05)
  self.assertEqual(len(shown['attempts']),2);self.assertEqual(shown['attempts'][1]['generation'],2)
if __name__=='__main__':unittest.main()
