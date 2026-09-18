import importlib.util, json, pathlib, subprocess, sys, tempfile, unittest
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
if __name__=='__main__': unittest.main()
