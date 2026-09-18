import importlib.util, pathlib, sys, unittest
p=pathlib.Path(__file__).with_name('messaging.py'); s=importlib.util.spec_from_file_location('messaging',p); m=importlib.util.module_from_spec(s); sys.modules['messaging']=m; s.loader.exec_module(m)
class Contract(unittest.TestCase):
 def test_root_is_not_a_substring(self):
  with self.assertRaises(m.ParseError): m.relay('note MACHINE.{ Relay.{ { a b «2026-01-01T00:00:00Z» unknown [ c ] } «x» «» } }')
 def test_backslash_is_preserved(self):
  x='MACHINE.{ Relay.{ { a b «2026-01-01T00:00:00Z» unknown [ c ] } «a\\qb» «» } }'
  self.assertEqual(m.relay(x)['quote'],'a\\qb')
if __name__=='__main__': unittest.main()
