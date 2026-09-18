import importlib.util, importlib.machinery, json, pathlib, subprocess, sys, tempfile, unittest
p=pathlib.Path(__file__).with_name('messaging.py'); s=importlib.util.spec_from_file_location('messaging',p); m=importlib.util.module_from_spec(s); sys.modules['messaging']=m; s.loader.exec_module(m)
class Contract(unittest.TestCase):
 def test_root_is_not_a_substring(self):
  with self.assertRaises(m.ParseError): m.relay('note MACHINE.{ Relay.{ { a b «2026-01-01T00:00:00Z» unknown [ c ] } «x» «» } }')
 def test_backslash_is_preserved(self):
  x='MACHINE.Relay.{ a b «2026-01-01T00:00:00Z» unknown [ c ] «a\\qb» «» }'
  self.assertEqual(m.relay(x)['quote'],'a\\qb')
 def test_machine_is_the_only_terminal_producer(self):
  with self.assertRaises(m.ParseError):
   m.relay('LIVING.Relay.{ a b «2026-01-01T00:00:00Z» typed [ c ] «x» «» }')
 def test_machine_builder_is_one_root_value(self):
  event=m.relay(m.make_machine('a','b','c','Task.{ ready }'))
  self.assertEqual(event['quote'],'Task.{ ready }')
 def test_watcher_marks_absence_stale_without_deleting(self):
  with tempfile.TemporaryDirectory() as d:
   state=pathlib.Path(d)/'state.json'; roster=pathlib.Path(d)/'roster.json'; watcher=pathlib.Path(__file__).with_name('field-watcher')
   roster.write_text(json.dumps({'a':{'pane_id':'p','status':'working'}})); subprocess.run([sys.executable,watcher,'--state',state,'--roster',roster],check=True,capture_output=True)
   roster.write_text('{}'); subprocess.run([sys.executable,watcher,'--state',state,'--roster',roster],check=True,capture_output=True)
   saved=json.loads(state.read_text()); self.assertEqual(saved['endpoints']['a']['state'],'stale'); self.assertGreaterEqual(len(saved['events']),2)
 def test_ledger_is_bounded_fifo_and_preserves_failed_attempt(self):
  with tempfile.TemporaryDirectory() as d:
   ledger=m.Ledger(pathlib.Path(d)/'ledger.json'); ids=[]
   for n in range(10): ids.append(ledger.enqueue({'quote':str(n)})['queue_id'])
   refused=ledger.enqueue({'quote':'overflow'}); self.assertFalse(refused['accepted'])
   attempt=ledger.attempt(ids[0],{'flow':'f','pane':'p','terminal':'t'},False)
   self.assertEqual(attempt['grade'],'Submitted'); self.assertEqual(len(ledger.data['queue']),10)
   with self.assertRaises(ValueError): ledger.acknowledge(ids[1])
   ledger.acknowledge(ids[0]); self.assertEqual(ledger.data['queue'][0]['id'],ids[1])
 def test_watcher_status_matrix(self):
  loader=importlib.machinery.SourceFileLoader('field_watcher',str(pathlib.Path(__file__).with_name('field-watcher'))); spec=importlib.util.spec_from_loader('field_watcher',loader); watcher=importlib.util.module_from_spec(spec); loader.exec_module(watcher)
  state={'version':1,'endpoints':{},'events':[]}
  watcher.observe(state,{'a':{'status':'working'},'b':{'status':'suspect'},'c':{'status':'unreachable'},'d':{'status':'done'},'e':{'status':'other'}})
  self.assertEqual({k:v['state'] for k,v in state['endpoints'].items()},{'a':'healthy','b':'suspect','c':'unreachable','d':'exited','e':'unknown'})
 def test_real_codec_is_the_machine_boundary(self):
  root=pathlib.Path(__file__).parents[1]; codec=root/'tools'/'messaging-codec'
  packet=m.make_machine('a','b','c','Task.{ ready }')
  got=subprocess.run(['cargo','run','--quiet','--offline'],cwd=codec,input=packet,text=True,capture_output=True,check=True)
  self.assertEqual(json.loads(got.stdout)['claimed_from'],'a')
  refused=subprocess.run(['cargo','run','--quiet','--offline'],cwd=codec,input='LIVING.Relay.{ a b «2026-01-01T00:00:00Z» typed [ c ] «x» «» }',text=True,capture_output=True)
  self.assertNotEqual(refused.returncode,0)
 def test_msg_rejects_newline_before_transport(self):
  command=[str(pathlib.Path(__file__).with_name('msg')),'c','first\nsecond']
  result=subprocess.run(command,env={**__import__('os').environ,'FLOW_ID':'a'},text=True,capture_output=True)
  self.assertEqual(result.returncode,2)
if __name__=='__main__': unittest.main()
