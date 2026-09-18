import importlib.util, importlib.machinery, json, pathlib, subprocess, sys, tempfile, unittest
p=pathlib.Path(__file__).with_name('messaging.py'); s=importlib.util.spec_from_file_location('messaging',p); m=importlib.util.module_from_spec(s); sys.modules['messaging']=m; s.loader.exec_module(m)
class Contract(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.root=pathlib.Path(__file__).parents[1]
  packaged=__import__('os').environ.get('MESSAGING_CODEC')
  if packaged: cls.codec=pathlib.Path(packaged)
  else:
   cls.codec=cls.root/'tools'/'messaging-codec'/'target'/'debug'/'messaging-codec'
   subprocess.run(['cargo','build','--offline'],cwd=cls.root/'tools'/'messaging-codec',check=True,capture_output=True)
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
   self.assertIsNone(attempt['grade']); self.assertEqual(len(ledger.data['queue']),10)
   with self.assertRaises(ValueError): ledger.acknowledge(ids[1])
   ledger.acknowledge(ids[0]); self.assertEqual(ledger.data['queue'][0]['id'],ids[1]); self.assertEqual(m.Ledger(pathlib.Path(d)/'ledger.json').data['queue'][0]['id'],ids[1]); self.assertIn('held-backpressure',[e['kind'] for e in ledger.data['events']])
 def test_watcher_status_matrix(self):
  loader=importlib.machinery.SourceFileLoader('field_watcher',str(pathlib.Path(__file__).with_name('field-watcher'))); spec=importlib.util.spec_from_loader('field_watcher',loader); watcher=importlib.util.module_from_spec(spec); loader.exec_module(watcher)
  state={'version':1,'endpoints':{},'events':[]}
  watcher.observe(state,{'a':{'status':'working'},'b':{'status':'suspect'},'c':{'status':'unreachable'},'d':{'status':'done'},'e':{'status':'other'}})
  self.assertEqual({k:v['state'] for k,v in state['endpoints'].items()},{'a':'healthy','b':'suspect','c':'unreachable','d':'exited','e':'unknown'})
  watcher.unreachable(state,'roster command failed')
  self.assertEqual({k:v['state'] for k,v in state['endpoints'].items()},{'a':'unreachable','b':'unreachable','c':'unreachable','d':'exited','e':'unreachable'})
  self.assertIn('heartbeat-failed',[x['kind'] for x in state['events']])
 def test_watcher_fake_notification_file(self):
  with tempfile.TemporaryDirectory() as d:
   d=pathlib.Path(d); state=d/'state.json'; roster=d/'roster.json'; notice=d/'notice.json'; watcher=pathlib.Path(__file__).with_name('field-watcher')
   roster.write_text(json.dumps({'a':{'pane_id':'p','status':'working'}}))
   subprocess.run([sys.executable,watcher,'--state',state,'--roster',roster,'--fake-notification-file',notice],check=True,capture_output=True)
   self.assertEqual(json.loads(notice.read_text())[0]['endpoint'],'a')
 def test_real_codec_is_the_machine_boundary(self):
  packet=m.make_machine('a','b','c','Task.{ ready }')
  got=subprocess.run([self.codec],input=packet,text=True,capture_output=True,check=True)
  self.assertEqual(json.loads(got.stdout)['claimed_from'],'a')
  refused=subprocess.run([self.codec],input='LIVING.Relay.{ a b «2026-01-01T00:00:00Z» typed [ c ] «x» «» }',text=True,capture_output=True)
  self.assertNotEqual(refused.returncode,0)
  heard=packet.split('«',2)[1][:10]
  self.assertNotEqual(subprocess.run([self.codec],input=packet.replace(heard,'2026-99-99'),text=True,capture_output=True).returncode,0)
  self.assertNotEqual(subprocess.run([self.codec],input=m.make_machine('a','b','c','ordinary prose'),text=True,capture_output=True).returncode,0)
 def test_msg_accepts_multiline_before_transport(self):
  command=[str(pathlib.Path(__file__).with_name('msg')),'c','first\nsecond']
  result=subprocess.run(command,env={**__import__('os').environ,'FLOW_ID':'a'},text=True,capture_output=True)
  self.assertEqual(result.returncode,1)
  self.assertNotIn('multiline payloads are not supported',result.stderr)
 def test_messenger_e2e_real_codec_preserves_full_envelope(self):
  with tempfile.TemporaryDirectory() as d:
   d=pathlib.Path(d); fake=d/'herdr'; delivered=d/'delivered'
   fake.write_text('#!/bin/sh\nif [ "$1 $2" = "agent list" ]; then echo "{\\"agents\\":[{\\"name\\":\\"c\\",\\"status\\":\\"working\\",\\"pane_id\\":\\"p\\"}]}"; exit 0; fi\nif [ "$1 $2" = "agent prompt" ]; then printf "%s" "$4" > "$HERDR_LOG"; exit 0; fi\nexit 1\n'); fake.chmod(0o755)
   packet=m.make_machine('a','seat','c','Task.{ «back\\\\slash λ\nsecond line» }')
   env={**__import__('os').environ,'PATH':str(d)+':'+__import__('os').environ['PATH'],'XDG_STATE_HOME':str(d/'state'),'HERDR_LOG':str(delivered),'MESSAGING_CODEC':str(self.codec)}
   import base64
   frame='FRAME.'+base64.b64encode(packet.encode()).decode()
   run=subprocess.run([str(pathlib.Path(__file__).with_name('messenger')),'m'],input=frame+'\n',text=True,capture_output=True,env=env,timeout=30)
   self.assertEqual(run.returncode,0); self.assertFalse(delivered.exists()); self.assertIn('bound endpoint changed or refused',run.stdout)
 def test_msg_multiline_to_messenger_to_agent(self):
  with tempfile.TemporaryDirectory() as d:
   d=pathlib.Path(d); frame=d/'frame'; delivered=d/'delivered'; fake=d/'herdr'; state=d/'state'/'messenger'; state.mkdir(parents=True); (state/'pane_id').write_text('m')
   fake.write_text('#!/bin/sh\nif [ "$1 $2" = "pane send-text" ]; then printf "%s" "$4" > "$HERDR_FRAME"; exit 0; fi\nif [ "$1 $2" = "pane send-keys" ]; then exit 0; fi\nif [ "$1 $2" = "agent list" ]; then echo "{\\"agents\\":[{\\"name\\":\\"c\\",\\"status\\":\\"working\\",\\"pane_id\\":\\"p\\"}]}"; exit 0; fi\nif [ "$1 $2" = "agent prompt" ]; then printf "%s" "$4" > "$HERDR_LOG"; exit 0; fi\nexit 1\n'); fake.chmod(0o755)
   env={**__import__('os').environ,'PATH':str(d)+':'+__import__('os').environ['PATH'],'XDG_STATE_HOME':str(d/'state'),'HERDR_FRAME':str(frame),'HERDR_LOG':str(delivered),'MESSAGING_CODEC':str(self.codec),'FLOW_ID':'a'}
   send=subprocess.run([str(pathlib.Path(__file__).with_name('msg')),'c','Task.{ «line one\nline two λ» }'],text=True,capture_output=True,env=env)
   self.assertEqual(send.returncode,0,send.stderr); self.assertTrue(frame.read_text().startswith('FRAME.'))
   run=subprocess.run([str(pathlib.Path(__file__).with_name('messenger')),'m'],input=frame.read_text()+'\n',text=True,capture_output=True,env=env,timeout=30)
   self.assertEqual(run.returncode,0); self.assertFalse(delivered.exists()); self.assertIn('bound endpoint changed or refused',run.stdout)
 def test_bad_frames_and_pane_only_target_are_held(self):
  with tempfile.TemporaryDirectory() as d:
   d=pathlib.Path(d); fake=d/'herdr'; touched=d/'touched'
   fake.write_text('#!/bin/sh\nif [ "$1 $2" = "agent list" ]; then echo "{\\"agents\\":[]}"; exit 0; fi\nprintf x > "$HERDR_TOUCHED"; exit 0\n'); fake.chmod(0o755)
   env={**__import__('os').environ,'PATH':str(d)+':'+__import__('os').environ['PATH'],'XDG_STATE_HOME':str(d/'state'),'HERDR_TOUCHED':str(touched),'MESSAGING_CODEC':str(self.codec)}
   packet=m.make_machine('a','seat','pane','Task.{ ready }'); import base64
   frames=['FRAME.','FRAME.%%%%','FRAME.'+base64.b64encode(b'not datom').decode(),'FRAME.'+base64.b64encode((packet+' extra').encode()).decode(),'FRAME.'+('A'*87385), 'FRAME.'+base64.b64encode(packet.encode()).decode()]
   run=subprocess.run([str(pathlib.Path(__file__).with_name('messenger')),'m'],input='\n'.join(frames)+'\n',text=True,capture_output=True,env=env,timeout=30)
   self.assertEqual(run.returncode,0); self.assertFalse(touched.exists()); self.assertIn('Held.{ pane',run.stdout)
 def test_fanout_partial_failure_holds_one_source_event(self):
  with tempfile.TemporaryDirectory() as d:
   d=pathlib.Path(d); fake=d/'herdr'
   fake.write_text('#!/bin/sh\nif [ "$1 $2" = "agent list" ]; then echo "{\\"agents\\":[{\\"name\\":\\"c\\",\\"status\\":\\"working\\",\\"pane_id\\":\\"pc\\"},{\\"name\\":\\"d\\",\\"status\\":\\"working\\",\\"pane_id\\":\\"pd\\"}]}"; exit 0; fi\nif [ "$1 $2 $3" = "agent prompt c" ]; then exit 0; fi\nexit 1\n'); fake.chmod(0o755)
   packet='MACHINE.Relay.{ a seat «2026-01-01T00:00:00Z» unknown [ c d ] «Task.{ ready }» «» }'; import base64
   env={**__import__('os').environ,'PATH':str(d)+':'+__import__('os').environ['PATH'],'XDG_STATE_HOME':str(d/'state'),'MESSAGING_CODEC':str(self.codec)}
   run=subprocess.run([str(pathlib.Path(__file__).with_name('messenger')),'m'],input='FRAME.'+base64.b64encode(packet.encode()).decode()+'\n',text=True,capture_output=True,env=env,timeout=30)
   ledger=json.loads((d/'state'/'messenger'/'ledger.json').read_text())
   self.assertEqual(run.returncode,0); self.assertEqual(len(ledger['queue']),1); self.assertEqual(len(ledger['attempts']),2); self.assertEqual([x['grade'] for x in ledger['attempts']],[None,None])
 def test_held_head_blocks_later_relay_and_protected_seat(self):
  with tempfile.TemporaryDirectory() as d:
   d=pathlib.Path(d); fake=d/'herdr'; touched=d/'touched'
   fake.write_text('#!/bin/sh\nif [ "$1 $2" = "agent list" ]; then echo "{\\"agents\\":[{\\"name\\":\\"c\\",\\"status\\":\\"working\\",\\"pane_id\\":\\"pc\\"},{\\"name\\":\\"d\\",\\"status\\":\\"working\\",\\"pane_id\\":\\"pd\\"},{\\"name\\":\\"e\\",\\"status\\":\\"working\\",\\"pane_id\\":\\"pe\\"},{\\"name\\":\\"testseat\\",\\"kind\\":\\"test\\",\\"status\\":\\"working\\",\\"pane_id\\":\\"pt\\"}]}"; exit 0; fi\nif [ "$1 $2 $3" = "agent prompt c" ]; then exit 0; fi\nif [ "$1 $2 $3" = "agent prompt d" ]; then exit 1; fi\nprintf "%s" "$3" >> "$HERDR_TOUCHED"; exit 0\n'); fake.chmod(0o755)
   env={**__import__('os').environ,'PATH':str(d)+':'+__import__('os').environ['PATH'],'XDG_STATE_HOME':str(d/'state'),'MESSAGING_CODEC':str(self.codec),'HERDR_TOUCHED':str(touched)}; import base64
   first='MACHINE.Relay.{ a seat «2026-01-01T00:00:00Z» unknown [ c d ] «Task.{ ready }» «» }'; second='MACHINE.Relay.{ a seat «2026-01-01T00:00:00Z» unknown [ e ] «Task.{ later }» «» }'
   run=subprocess.run([str(pathlib.Path(__file__).with_name('messenger')),'m'],input='\n'.join('FRAME.'+base64.b64encode(x.encode()).decode() for x in [first,second])+'\n',text=True,capture_output=True,env=env,timeout=30)
   ledger=json.loads((d/'state'/'messenger'/'ledger.json').read_text())
   self.assertEqual(run.returncode,0); self.assertEqual(len(ledger['queue']),1); self.assertNotIn('e',touched.read_text() if touched.exists() else ''); self.assertIn('prior relay remains pending',run.stdout)
if __name__=='__main__': unittest.main()
