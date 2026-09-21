import contextlib
import hashlib
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
import hm


class MessengerTests(unittest.TestCase):
    def setUp(self):
        env = patch.dict('os.environ', {'FLOW_ID': 'sender'})
        env.start()
        self.addCleanup(env.stop)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.m = hm.Messenger(self.temp.name)
        self.agent = dict(session='test', name='receiver', pane_id='w1:p2',
                          terminal_id='original', agent='codex', interactive_ready=True,
                          agent_status='working')
        self.calls = []
        self.lock = patch.object(self.m, 'reservation', lambda flow: contextlib.nullcontext())
        self.lock.start()
        self.addCleanup(self.lock.stop)
        self.api = patch('hm.herdr', self.herdr)
        self.api.start()
        self.addCleanup(self.api.stop)
        self.native_thread = '11111111-2222-3333-4444-555555555555'
        self.m.register('test-flow', 'receiver', 'test', native_thread=self.native_thread)
        self.calls.clear()

    def evidence(self):
        path = Path(self.temp.name) / 'retirement-receipt.md'
        path.write_text('exact retained lifecycle evidence\n')
        return path, hashlib.sha256(path.read_bytes()).hexdigest()

    def retire(self, flow='test-flow', native_thread=None, allow_absent=False):
        evidence, digest = self.evidence()
        return self.m.retire(flow, 'test', 'w1:p2', 'original', 'receiver', 'codex',
                             native_thread or self.native_thread, evidence, digest, allow_absent)

    def herdr(self, *args):
        self.calls.append(args)
        if args[-2:] == ('agent', 'list'):
            return {'agents': [self.agent]}
        return {'type': 'ok'}

    def test_plain_text_is_one_unchanged_argument(self):
        body = 'Notice.{ «hello 世界» }\n$(touch /not-executed)'
        self.m.send('test-flow', body)
        self.assertEqual(self.calls[-1], ('--session', 'test', 'agent', 'prompt', 'w1:p2', body))
        self.assertEqual(len(self.calls), 2)

    def test_abrupt_orders_escape_before_prompt(self):
        self.m.send('test-flow', 'hello', abrupt=True)
        self.assertEqual(self.calls[1:], [('--session', 'test', 'agent', 'send-keys', 'w1:p2', 'esc'),
                                        ('--session', 'test', 'agent', 'prompt', 'w1:p2', 'hello')])

    def test_probe_registration_requires_exact_assistant_turn(self):
        self.agent['interactive_ready'] = False
        marker = 'HM_READY_test1234'; native_thread = '11111111-2222-3333-4444-555555555555'
        rollout = Path(self.temp.name) / 'rollout.jsonl'
        rows = [
            {'type':'event_msg','payload':{'thread_id':native_thread,'item':{'type':'UserMessage','content':[{'text':f'Reply exactly {marker}'}]}}},
            {'type':'event_msg','payload':{'thread_id':native_thread,'item':{'type':'AgentMessage','content':[{'text':marker}]}}},
        ]
        rollout.write_text('\n'.join(__import__('json').dumps(r) for r in rows)+'\n')
        def probe_run(argv):
            if argv == ['herdr', '--session', 'test', 'agent', 'prompt', 'w1:p2', f'Reply exactly {marker} to confirm this explicit HM readiness probe.']:
                return '{"error":{"code":"agent_prompt_stalled"}}'
            raise AssertionError(argv)
        with patch('hm.run', probe_run):
            self.m.register('probed-flow', 'receiver', 'test', marker, native_thread, rollout)
        self.assertEqual(self.m.read('probed-flow')['readiness_proof']['thread_id'], native_thread)

    def test_probe_rejects_echo_only_or_wrong_thread(self):
        self.agent['interactive_ready'] = False
        marker = 'HM_READY_test1234'; native_thread = '11111111-2222-3333-4444-555555555555'
        rollout = Path(self.temp.name) / 'echo.jsonl'
        rows = [{'type':'event_msg','payload':{'thread_id':native_thread,'item':{'type':'UserMessage','content':[{'text':marker}]}}},
                {'type':'event_msg','payload':{'thread_id':'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee','item':{'type':'AgentMessage','content':[{'text':marker}]}}}]
        rollout.write_text('\n'.join(__import__('json').dumps(r) for r in rows)+'\n')
        with patch('hm.run', return_value='{"error":{"code":"agent_prompt_stalled"}}'):
            with self.assertRaisesRegex(hm.Failure, 'assistant reply'):
                self.m.register('echo-flow', 'receiver', 'test', marker, native_thread, rollout)


    def test_replaced_terminal_refuses_send(self):
        self.agent['terminal_id'] = 'replacement'
        with self.assertRaisesRegex(hm.Failure, 'stale'):
            self.m.send('test-flow', 'hello')
        self.assertEqual(len(self.calls), 1)

    def test_conflicting_registration_preserves_original(self):
        self.agent['terminal_id'] = 'replacement'
        with self.assertRaisesRegex(hm.Failure, 'different terminal'):
            self.m.register('test-flow', 'receiver', 'test')
        self.assertEqual(self.m.read('test-flow')['terminal_id'], 'original')

    def test_rebind_renames_the_verified_same_target_and_preserves_native_thread(self):
        self.agent['name'] = 'renamed-receiver'
        result = self.m.rebind('test-flow', 'receiver', 'renamed-receiver', 'test',
                               'w1:p2', 'original', 'codex', self.native_thread)
        self.assertEqual(result, 'Rebound test-flow: receiver -> renamed-receiver (test/w1:p2/original)')
        record = self.m.read('test-flow')
        self.assertEqual(record['name'], 'renamed-receiver')
        self.assertEqual(record['native_thread'], self.native_thread)
        self.assertEqual(record['session'], 'test')
        self.assertEqual(record['pane_id'], 'w1:p2')
        self.assertEqual(record['terminal_id'], 'original')

    def test_rebind_refuses_changed_pane_or_native_thread_without_replacing_record(self):
        self.agent['name'] = 'renamed-receiver'
        self.agent['pane_id'] = 'w1:p2'
        with self.assertRaisesRegex(hm.Failure, 'old binding'):
            self.m.rebind('test-flow', 'receiver', 'renamed-receiver', 'test',
                          'w1:p3', 'original', 'codex', self.native_thread)
        self.assertEqual(self.m.read('test-flow')['name'], 'receiver')

    def test_rebind_refuses_a_name_already_registered_in_its_session(self):
        self.agent['name'] = 'renamed-receiver'
        self.m.register('other-flow', 'renamed-receiver', 'test',
                        native_thread='aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee')
        with self.assertRaisesRegex(hm.Failure, 'already registered'):
            self.m.rebind('test-flow', 'receiver', 'renamed-receiver', 'test',
                          'w1:p2', 'original', 'codex', self.native_thread)
        self.assertEqual(self.m.read('test-flow')['name'], 'receiver')
        with self.assertRaisesRegex(hm.Failure, 'native thread'):
            self.m.rebind('test-flow', 'receiver', 'renamed-receiver', 'test',
                          'w1:p2', 'original', 'codex',
                          'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee')
        self.assertEqual(self.m.read('test-flow')['name'], 'receiver')

    def test_invalid_body_has_no_side_effect(self):
        for text in ('', '\x1b[1mhi', 'hello\x7f'):
            with self.assertRaises(hm.Failure):
                self.m.send('test-flow', text, abrupt=True)
        self.assertEqual(self.calls, [])

    def test_unknown_and_traversal_refuse(self):
        for flow in ('absent', '../escape'):
            with self.assertRaises(hm.Failure):
                self.m.send(flow, 'hello')
        self.assertEqual(self.calls, [])

    def test_escape_failure_never_prompts(self):
        original = self.herdr
        def fail(*args):
            if 'send-keys' in args:
                raise hm.Failure('Escape unavailable')
            return original(*args)
        with patch('hm.herdr', fail), self.assertRaises(hm.Failure):
            self.m.send('test-flow', 'hello', abrupt=True)
        self.assertFalse(any('prompt' in c for c in self.calls))

    def test_prompt_failure_reports_partial_abrupt(self):
        original = self.herdr
        def fail(*args):
            if 'prompt' in args:
                raise hm.Failure('lost connection')
            return original(*args)
        with patch('hm.herdr', fail), self.assertRaisesRegex(hm.Failure, 'Escape was sent'):
            self.m.send('test-flow', 'hello', abrupt=True)

    def test_blocked_refuses_before_escape(self):
        self.agent['agent_status'] = 'blocked'
        with self.assertRaisesRegex(hm.Failure, 'blocked'):
            self.m.send('test-flow', 'hello', abrupt=True)
        self.assertEqual(len(self.calls), 1)

    def test_success_exit_with_error_json_is_failure(self):
        with patch('hm.run', return_value='{"error":{"code":"agent_not_found"}}'):
            with self.assertRaises(hm.Failure):
                self.api.stop()
                try:
                    hm.herdr('agent', 'prompt', 'missing', 'hello')
                finally:
                    self.api.start()

    def test_retired_flow_refuses_before_any_herdr_call(self):
        self.retire()
        self.calls.clear()
        with self.assertRaisesRegex(hm.Failure, 'retired'):
            self.m.send('test-flow', 'must not arrive')
        self.assertEqual(self.calls, [])

    def test_malformed_retirement_marker_fails_closed_before_any_herdr_call(self):
        marker = self.m.retired_path('test-flow')
        marker.parent.mkdir()
        marker.write_text('{not json')
        self.calls.clear()
        with self.assertRaisesRegex(hm.Failure, 'unavailable or malformed'):
            self.m.send('test-flow', 'must not arrive')
        self.assertEqual(self.calls, [])

    def test_import_retirement_accepts_absent_route_without_contacting_herdr(self):
        self.m.path('test-flow').unlink()
        self.calls.clear()
        self.retire(allow_absent=True)
        self.assertEqual(self.calls, [])
        self.assertEqual(self.m.retirement('test-flow')['native_thread'], self.native_thread)

    def test_retired_native_thread_cannot_be_registered_as_another_flow(self):
        self.retire()
        self.calls.clear()
        with self.assertRaisesRegex(hm.Failure, 'Native thread'):
            self.m.register('replacement-flow', 'receiver', 'test', native_thread=self.native_thread)
        self.assertEqual(self.calls, [])


if __name__ == '__main__':
    unittest.main()
