import contextlib
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
        self.m.register('test-flow', 'receiver', 'test')
        self.calls.clear()

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


if __name__ == '__main__':
    unittest.main()
