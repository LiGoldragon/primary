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
  x='MACHINE.Relay.{ event a b «2026-01-01T00:00:00Z» unknown [ c ] «a\\qb» «» }'
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
   roster.write_text(json.dumps({'a':{'pane_id':'p','status':'working','kind':'production'}})); subprocess.run([sys.executable,watcher,'--state',state,'--roster',roster],check=True,capture_output=True)
   roster.write_text('{}'); subprocess.run([sys.executable,watcher,'--state',state,'--roster',roster],check=True,capture_output=True)
   saved=json.loads(state.read_text()); self.assertEqual(saved['endpoints']['a']['state'],'stale'); self.assertGreaterEqual(len(saved['events']),2)
 def test_ledger_is_bounded_fifo_and_preserves_failed_attempt(self):
  with tempfile.TemporaryDirectory() as d:
   ledger=m.Ledger(pathlib.Path(d)/'ledger.json'); ids=[]
   for n in range(10): ids.append(ledger.enqueue({'ingress_id':'e'+str(n),'quote':str(n)})['queue_id'])
   refused=ledger.enqueue({'ingress_id':'overflow','quote':'overflow'}); self.assertFalse(refused['accepted'])
   attempt=ledger.attempt(ids[0],{'flow':'f','pane':'p','terminal':'t'},False)
   self.assertIsNone(attempt['grade']); self.assertEqual(len(ledger.data['queue']),10)
   with self.assertRaises(ValueError): ledger.acknowledge(ids[1])
   ledger.acknowledge(ids[0]); self.assertEqual(ledger.data['queue'][0]['id'],ids[1]); ledger.close(); self.assertEqual(m.Ledger(pathlib.Path(d)/'ledger.json').data['queue'][0]['id'],ids[1]); self.assertIn('held-backpressure',[e['kind'] for e in ledger.data['events']])
 def test_watcher_status_matrix(self):
  loader=importlib.machinery.SourceFileLoader('field_watcher',str(pathlib.Path(__file__).with_name('field-watcher'))); spec=importlib.util.spec_from_loader('field_watcher',loader); watcher=importlib.util.module_from_spec(spec); loader.exec_module(watcher)
  state={'version':1,'endpoints':{},'events':[]}
  watcher.observe(state,{'a':{'status':'working'},'b':{'status':'suspect'},'c':{'status':'unreachable'},'d':{'status':'done'},'e':{'status':'other'}})
  self.assertEqual({k:v['state'] for k,v in state['endpoints'].items()},{'a':'healthy','b':'suspect','c':'unreachable','d':'exited','e':'unknown'})
  watcher.unreachable(state,'roster command failed')
  self.assertEqual({k:v['state'] for k,v in state['endpoints'].items()},{'a':'unreachable','b':'unreachable','c':'unreachable','d':'exited','e':'unreachable'})
  self.assertIn('heartbeat-failed',[x['kind'] for x in state['events']])
 def test_ingress_id_dedup_conflict_and_crash_hold(self):
  with tempfile.TemporaryDirectory() as d:
   ledger=m.Ledger(pathlib.Path(d)/'ledger.json'); event={'ingress_id':'event','quote':'Task.{ ready }'}
   first=ledger.enqueue(event); self.assertTrue(first['accepted']); self.assertTrue(ledger.enqueue(event)['duplicate'])
   self.assertTrue(ledger.enqueue({'ingress_id':'event','quote':'Task.{ changed }'})['conflict'])
   ledger.attempt_started(first['queue_id'],{'flow':'c','pane':'p','terminal':'t'}); ledger.close()
   reopened=m.Ledger(pathlib.Path(d)/'ledger.json'); reopened.recover()
   self.assertEqual(reopened.data['attempts'][0]['outcome'],'uncertain_crash'); self.assertTrue(reopened.enqueue(event)['duplicate'])
 def test_prompt_crash_replay_never_resends(self):
  with tempfile.TemporaryDirectory() as d:
   d=pathlib.Path(d); fake=d/'herdr'; calls=d/'calls'; packet='MACHINE.Relay.{ crashid a seat «2026-01-01T00:00:00Z» unknown [ c ] «Task.{ ready }» «» }'; import base64
   fake.write_text('''#!/bin/sh
if [ "$1 $2" = "agent list" ]; then echo '{"agents":[{"name":"c","status":"working","pane_id":"p","terminal_id":"t"}]}' ; exit 0; fi
if [ "$1 $2" = "agent get" ]; then echo '{"result":{"agent":{"name":"c","pane_id":"p","terminal_id":"t","interactive_ready":true,"agent_status":"working"}}}' ; exit 0; fi
if [ "$1 $2 $3" = "agent prompt p" ]; then printf x >> "$HERDR_CALLS"; kill -9 "$PPID"; fi
exit 1
'''); fake.chmod(0o755)
   env={**__import__('os').environ,'PATH':str(d)+':'+__import__('os').environ['PATH'],'XDG_STATE_HOME':str(d/'state'),'MESSAGING_CODEC':str(self.codec),'HERDR_CALLS':str(calls)}
   frame='FRAME.'+base64.b64encode(packet.encode()).decode()
   first=subprocess.run([str(pathlib.Path(__file__).with_name('messenger')),'m'],input=frame+'\n',text=True,capture_output=True,env=env,timeout=30)
   self.assertNotEqual(first.returncode,0); self.assertEqual(calls.read_text(),'x')
   second=subprocess.run([str(pathlib.Path(__file__).with_name('messenger')),'m'],input=frame+'\n',text=True,capture_output=True,env=env,timeout=30)
   ledger=json.loads((d/'state'/'messenger'/'ledger.json').read_text())
   self.assertEqual(second.returncode,0); self.assertEqual(calls.read_text(),'x'); self.assertEqual(ledger['attempts'][0]['outcome'],'uncertain_crash'); self.assertIn('relay ingress already recorded',second.stdout)
 def test_watcher_excludes_fixture_but_preserves_protected(self):
  loader=importlib.machinery.SourceFileLoader('field_watcher',str(pathlib.Path(__file__).with_name('field-watcher'))); spec=importlib.util.spec_from_loader('field_watcher',loader); watcher=importlib.util.module_from_spec(spec); loader.exec_module(watcher)
  state={'version':1,'endpoints':{'fixture':{'state':'healthy','kind':'fixture'}},'events':[]}; watcher.observe(state,{'fixture':{'kind':'fixture','status':'working'},'test':{'kind':'test','status':'working'},'protected':{'kind':'protected','status':'working'}})
  self.assertNotIn('fixture',state['endpoints']); self.assertNotIn('test',state['endpoints']); self.assertEqual(state['endpoints']['protected']['state'],'healthy')
  state['endpoints']['oldfixture']={'state':'healthy','kind':'fixture'}; watcher.unreachable(state,'offline')
  self.assertNotIn('oldfixture',state['endpoints']); self.assertNotIn('oldfixture',[e['endpoint'] for e in state['events']])
 def test_watcher_fake_notification_file(self):
  with tempfile.TemporaryDirectory() as d:
   d=pathlib.Path(d); state=d/'state.json'; roster=d/'roster.json'; notice=d/'notice.json'; watcher=pathlib.Path(__file__).with_name('field-watcher')
   roster.write_text(json.dumps({'a':{'pane_id':'p','status':'working','kind':'production'}}))
   subprocess.run([sys.executable,watcher,'--state',state,'--roster',roster,'--fake-notification-file',notice],check=True,capture_output=True)
   self.assertEqual(json.loads(notice.read_text())[0]['endpoint'],'a')
 def test_notification_projection_filters_persisted_test_fixture_history(self):
  with tempfile.TemporaryDirectory() as d:
   d=pathlib.Path(d); state=d/'state.json'; roster=d/'roster.json'; notice=d/'notice.json'; watcher=pathlib.Path(__file__).with_name('field-watcher'); fake=d/'herdr'
   events=[
    {'id':'test','kind':'endpoint-state','endpoint':'testseat','detail':{},'provenance':{'endpoint_kind':'test'}},
    {'id':'fixture','kind':'endpoint-state','endpoint':'fixtureseat','detail':{},'provenance':{'endpoint_kind':'fixture'}},
    {'id':'protected','kind':'endpoint-state','endpoint':'protected','detail':{},'provenance':{'endpoint_kind':'protected'}},
    {'id':'production','kind':'endpoint-state','endpoint':'ordinary','detail':{},'provenance':{'endpoint_kind':'production'}},
    {'id':'legacy','kind':'endpoint-state','endpoint':'unclassified','detail':{}},
   ]
   state.write_text(json.dumps({'version':1,'endpoints':{'testseat':{'state':'healthy','kind':'test'},'fixtureseat':{'state':'healthy','kind':'fixture'},'protected':{'state':'healthy','kind':'protected'},'ordinary':{'state':'healthy','kind':'production'}},'events':events}))
   fake.write_text('#!/bin/sh\nexit 1\n'); fake.chmod(0o755)
   env={**__import__('os').environ,'PATH':str(d)+':'+__import__('os').environ['PATH']}
   # Restarted heartbeat failure preserves old evidence but projects only proven
   # production/protected history and the newly-proven watcher heartbeat event.
   subprocess.run([sys.executable,watcher,'--state',state,'--heartbeat','--fake-notification-file',notice],check=True,capture_output=True,env=env)
   projected=json.loads(notice.read_text()); names={x['endpoint'] for x in projected}
   self.assertNotIn('testseat',names); self.assertNotIn('fixtureseat',names); self.assertNotIn('unclassified',names)
   self.assertIn('protected',names); self.assertIn('ordinary',names); self.assertIn('watcher',names)
   retained=json.loads(state.read_text())['events']; self.assertEqual({x['id'] for x in events}, {x['id'] for x in retained if x['id'] in {'test','fixture','protected','production','legacy'}})
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
   packet='MACHINE.Relay.{ event a seat «2026-01-01T00:00:00Z» unknown [ c d ] «Task.{ ready }» «» }'; import base64
   env={**__import__('os').environ,'PATH':str(d)+':'+__import__('os').environ['PATH'],'XDG_STATE_HOME':str(d/'state'),'MESSAGING_CODEC':str(self.codec)}
   run=subprocess.run([str(pathlib.Path(__file__).with_name('messenger')),'m'],input='FRAME.'+base64.b64encode(packet.encode()).decode()+'\n',text=True,capture_output=True,env=env,timeout=30)
   ledger=json.loads((d/'state'/'messenger'/'ledger.json').read_text())
   self.assertEqual(run.returncode,0); self.assertEqual(len(ledger['queue']),1); self.assertEqual(len(ledger['attempts']),2); self.assertEqual([x['grade'] for x in ledger['attempts']],[None,None])
 def test_held_head_blocks_later_relay_and_protected_seat(self):
  with tempfile.TemporaryDirectory() as d:
   d=pathlib.Path(d); fake=d/'herdr'; touched=d/'touched'
   fake.write_text('#!/bin/sh\nif [ "$1 $2" = "agent list" ]; then echo "{\\"agents\\":[{\\"name\\":\\"c\\",\\"status\\":\\"working\\",\\"pane_id\\":\\"pc\\"},{\\"name\\":\\"d\\",\\"status\\":\\"working\\",\\"pane_id\\":\\"pd\\"},{\\"name\\":\\"e\\",\\"status\\":\\"working\\",\\"pane_id\\":\\"pe\\"},{\\"name\\":\\"testseat\\",\\"kind\\":\\"test\\",\\"status\\":\\"working\\",\\"pane_id\\":\\"pt\\"}]}"; exit 0; fi\nif [ "$1 $2 $3" = "agent prompt c" ]; then exit 0; fi\nif [ "$1 $2 $3" = "agent prompt d" ]; then exit 1; fi\nprintf "%s" "$3" >> "$HERDR_TOUCHED"; exit 0\n'); fake.chmod(0o755)
   env={**__import__('os').environ,'PATH':str(d)+':'+__import__('os').environ['PATH'],'XDG_STATE_HOME':str(d/'state'),'MESSAGING_CODEC':str(self.codec),'HERDR_TOUCHED':str(touched)}; import base64
   first='MACHINE.Relay.{ eventa a seat «2026-01-01T00:00:00Z» unknown [ c d ] «Task.{ ready }» «» }'; second='MACHINE.Relay.{ eventb a seat «2026-01-01T00:00:00Z» unknown [ e ] «Task.{ later }» «» }'
   run=subprocess.run([str(pathlib.Path(__file__).with_name('messenger')),'m'],input='\n'.join('FRAME.'+base64.b64encode(x.encode()).decode() for x in [first,second])+'\n',text=True,capture_output=True,env=env,timeout=30)
   ledger=json.loads((d/'state'/'messenger'/'ledger.json').read_text())
   self.assertEqual(run.returncode,0); self.assertEqual(len(ledger['queue']),1); self.assertNotIn('e',touched.read_text() if touched.exists() else ''); self.assertIn('prior relay remains pending',run.stdout)
 def test_concurrent_messenger_cannot_duplicate_attempt(self):
  with tempfile.TemporaryDirectory() as d:
   d=pathlib.Path(d); fake=d/'herdr'; calls=d/'calls'; release=d/'release'; import base64, time
   fake.write_text('#!/bin/sh\nif [ "$1 $2" = "agent list" ]; then echo \'{"agents":[{"name":"c","status":"working","pane_id":"p","terminal_id":"t"}]}\' ; exit 0; fi\nif [ "$1 $2" = "agent get" ]; then echo \'{"result":{"agent":{"name":"c","pane_id":"p","terminal_id":"t","interactive_ready":true,"agent_status":"working"}}}\' ; exit 0; fi\nif [ "$1 $2 $3" = "agent prompt p" ]; then printf x >> "$HERDR_CALLS"; while [ ! -e "$HERDR_RELEASE" ]; do sleep .05; done; exit 0; fi\nexit 1\n'); fake.chmod(0o755)
   env={**__import__('os').environ,'PATH':str(d)+':'+__import__('os').environ['PATH'],'XDG_STATE_HOME':str(d/'state'),'MESSAGING_CODEC':str(self.codec),'HERDR_CALLS':str(calls),'HERDR_RELEASE':str(release)}
   packet='MACHINE.Relay.{ concurrentid a seat «2026-01-01T00:00:00Z» unknown [ c ] «Task.{ ready }» «» }'; frame='FRAME.'+base64.b64encode(packet.encode()).decode()+'\n'; command=[str(pathlib.Path(__file__).with_name('messenger')),'m']
   first=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=env); first.stdin.write(frame); first.stdin.close()
   for _ in range(100):
    if calls.exists(): break
    time.sleep(.05)
   self.assertTrue(calls.exists())
   second=subprocess.run(command,input=frame,text=True,capture_output=True,env=env,timeout=30)
   self.assertEqual(second.returncode,75); self.assertEqual(calls.read_text(),'x')
   release.touch(); self.assertEqual(first.wait(timeout=30),0); first.stdout.close(); first.stderr.close()
 def test_completed_ingress_replay_and_conflict_do_not_prompt_again(self):
  with tempfile.TemporaryDirectory() as d:
   d=pathlib.Path(d); fake=d/'herdr'; calls=d/'calls'; import base64
   fake.write_text('#!/bin/sh\nif [ "$1 $2" = "agent list" ]; then echo \'{"agents":[{"name":"c","status":"working","pane_id":"p","terminal_id":"t"}]}\' ; exit 0; fi\nif [ "$1 $2" = "agent get" ]; then echo \'{"result":{"agent":{"name":"c","pane_id":"p","terminal_id":"t","interactive_ready":true,"agent_status":"working"}}}\' ; exit 0; fi\nif [ "$1 $2 $3" = "agent prompt p" ]; then printf x >> "$HERDR_CALLS"; exit 0; fi\nexit 1\n'); fake.chmod(0o755)
   env={**__import__('os').environ,'PATH':str(d)+':'+__import__('os').environ['PATH'],'XDG_STATE_HOME':str(d/'state'),'MESSAGING_CODEC':str(self.codec),'HERDR_CALLS':str(calls)}
   packet='MACHINE.Relay.{ completeid a seat «2026-01-01T00:00:00Z» unknown [ c ] «Task.{ ready }» «» }'
   changed=packet.replace('ready','changed')
   def run(x): return subprocess.run([str(pathlib.Path(__file__).with_name('messenger')),'m'],input='FRAME.'+base64.b64encode(x.encode()).decode()+'\n',text=True,capture_output=True,env=env,timeout=30)
   self.assertEqual(run(packet).returncode,0); self.assertEqual(calls.read_text(),'x')
   duplicate=run(packet); conflict=run(changed)
   self.assertEqual(duplicate.returncode,0); self.assertEqual(conflict.returncode,0); self.assertEqual(calls.read_text(),'x')
   self.assertIn('already recorded',duplicate.stdout); self.assertIn('conflicts with recorded payload',conflict.stdout)
 def test_bound_pane_route_handles_replacement_races(self):
  packet='MACHINE.Relay.{ event a seat «2026-01-01T00:00:00Z» unknown [ c ] «Task.{ ready }» «» }'
  import base64
  def run_case(mode):
   with tempfile.TemporaryDirectory() as d:
    d=pathlib.Path(d); fake=d/'herdr'; prompt=d/'prompt'; count=d/'get-count'
    fake.write_text('''#!/bin/sh
if [ "$1 $2" = "agent list" ]; then echo '{"agents":[{"name":"c","status":"working","pane_id":"p","terminal_id":"t"}]}' ; exit 0; fi
if [ "$1 $2" = "agent get" ]; then n=0; [ -e "$HERDR_COUNT" ] && n=$(cat "$HERDR_COUNT"); n=$((n+1)); printf '%s' "$n" > "$HERDR_COUNT"; term=t; status=working; [ "$HERDR_MODE" = pre ] && term=replacement; [ "$HERDR_MODE" = post ] && [ "$n" -gt 1 ] && term=replacement; [ "$HERDR_MODE" = done ] && [ "$n" -gt 1 ] && status=done; [ "$HERDR_MODE" = pre_done ] && status=done; printf '{"result":{"agent":{"name":"c","pane_id":"p","terminal_id":"%s","interactive_ready":true,"agent_status":"%s"}}}\n' "$term" "$status"; exit 0; fi
if [ "$1 $2 $3" = "agent prompt p" ]; then printf '%s' "$4" > "$HERDR_PROMPT"; exit 0; fi
exit 1
'''); fake.chmod(0o755)
    env={**__import__('os').environ,'PATH':str(d)+':'+__import__('os').environ['PATH'],'XDG_STATE_HOME':str(d/'state'),'MESSAGING_CODEC':str(self.codec),'HERDR_PROMPT':str(prompt),'HERDR_COUNT':str(count),'HERDR_MODE':mode}
    run=subprocess.run([str(pathlib.Path(__file__).with_name('messenger')),'m'],input='FRAME.'+base64.b64encode(packet.encode()).decode()+'\n',text=True,capture_output=True,env=env,timeout=30)
    return run,prompt.read_text() if prompt.exists() else None,json.loads((d/'state'/'messenger'/'ledger.json').read_text())
  stable,prompt_text,ledger=run_case('done')
  self.assertEqual(stable.returncode,0); self.assertEqual(prompt_text,packet); self.assertEqual(ledger['attempts'][0]['grade'],'Transported'); self.assertEqual(ledger['queue'],[])
  pre,prompt_text,ledger=run_case('pre')
  self.assertEqual(pre.returncode,0); self.assertIsNone(prompt_text); self.assertIsNone(ledger['attempts'][0]['grade']); self.assertEqual(len(ledger['queue']),1)
  post,prompt_text,ledger=run_case('post')
  self.assertEqual(post.returncode,0); self.assertEqual(prompt_text,packet); self.assertIsNone(ledger['attempts'][0]['grade']); self.assertEqual(len(ledger['queue']),1)
  pre_done,prompt_text,ledger=run_case('pre_done')
  self.assertEqual(pre_done.returncode,0); self.assertEqual(prompt_text,packet); self.assertEqual(ledger['attempts'][0]['grade'],'Transported'); self.assertEqual(ledger['queue'],[])
if __name__=='__main__': unittest.main()
