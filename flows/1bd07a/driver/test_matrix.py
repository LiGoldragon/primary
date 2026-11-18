"""Unrun pure fixtures; no native launches, tools, services or observers."""
import unittest
import matrix


class MatrixFixtures(unittest.TestCase):
    def test_phase_a_reply_order_and_duplicate_new_calls(self):
        from unittest import mock
        owner = mock.Mock(manifest={'root': '/private', 'providers': {'flow': {'path': '/flow'}}})
        ledger = matrix.Evidence()
        ledger.request('O', 'order1', 'Order')
        ledger.request('Q', 'question1', 'Question')
        ledger.request('T', 'task1', 'Task', 15)
        channel = mock.Mock()
        with mock.patch.object(matrix, 'control_question', return_value='control'):
            matrix.collect_phase_a_reply_outcomes(owner, channel, ledger, 'unknown1', 1, object(), object())
        outcomes = channel.receive_reply_outcome.call_args_list
        self.assertEqual([c.args[0] for c in outcomes], ['result-order', 'result-task', 'done-question', 'result-unknown', 'result-question', 'done-task', 'duplicate-result', 'duplicate-done'])
        self.assertEqual([c.args[3] for c in outcomes], ['unresolved', 'unresolved', 'unresolved', 'unresolved', 'accepted', 'accepted', 'unresolved', 'unresolved'])
        self.assertEqual(channel.receive_routed_consumption.call_count, 2)

    def test_kept_answer_binds_original_id_and_sender(self):
        from unittest import mock
        import controller
        owner = mock.Mock(manifest={})
        channel = mock.Mock()
        channel.requests = {}
        channel.controls = {}
        channel.minutes = {}
        ledger = matrix.Evidence()
        def call(owner, label, binary, request):
            if label == 'kept-question':
                return 'SendAccepted.{ kept1 3 Queued }'
            return 'Answered.{ Sender.{ Mind proposalTwoReceiver Luna } Soft.Result.{ kept1 «P2-kept-answer» } }'
        with mock.patch.object(matrix, 'control_question', return_value='control'):
            self.assertEqual(matrix.kept_answer_case(owner, channel, ledger, 1, call, controller.receipt_tokens, controller.receipt), 'kept1')
        channel.receive_reply_outcome.assert_called_once()
        channel.receive_consumption.assert_called_once()

    def test_phase_a_collects_admissions_in_order(self):
        from unittest import mock
        owner = mock.Mock(manifest={'root': '/private', 'providers': {'flow': {'path': '/flow'}}})
        channel = mock.Mock()
        def admission(label, kind, marker, deadline, receipt_tokens):
            return {'request_id': 'id' + label, 'minutes': 15 if kind == 'Task' else None}
        channel.receive_admission.side_effect = admission
        ledger = matrix.Evidence()
        def call(owner, label, binary, request):
            return 'DeliveryDebugged.{ fixture }'
        with mock.patch.object(matrix, 'control_question', return_value='control'):
            matrix.collect_phase_a_admissions(owner, channel, ledger, 10, call, object())
        self.assertEqual(list(ledger.requests), ['O', 'Q', 'T', 'N', 'L'])
        self.assertEqual(channel.receive_admission.call_count, 5)
        self.assertEqual(ledger.requests['T']['minutes'], 15)

    def test_typed_visible_admission_extracts_only_request_id(self):
        import controller
        self.assertEqual(matrix.parse_visible_admission('SendAccepted.{ req1 8 Queued }', controller.receipt_tokens), 'req1')
        self.assertEqual(matrix.parse_visible_admission('Sent.req2', controller.receipt_tokens), 'req2')
        for bad in ('SendRefused.Unresolved', 'SendAccepted.{ req3 x Queued }',
                    'SendAccepted.{ req3 8 Unknown }', 'SendAccepted.{ req3 8 Delivered.{ x }'):
            with self.assertRaises((matrix.MatrixError, controller.AdmissionError)):
                matrix.parse_visible_admission(bad, controller.receipt_tokens)

    def test_request_ids_are_dynamic_unique_and_kind_bound(self):
        evidence = matrix.Evidence()
        evidence.request('Q2', 'actual-q', 'Question')
        with self.assertRaises(matrix.MatrixError): evidence.request('T2', 'actual-q', 'Task', 123)
        with self.assertRaises(matrix.MatrixError): evidence.request('O2', 'actual-o', 'Question')

    def test_carry_and_order_exclusion(self):
        evidence = matrix.Evidence()
        evidence.request('O2', 'o_actual', 'Order')
        evidence.request('Q2', 'q_actual', 'Question')
        evidence.request('T2', 't_actual', 'Task', 15)
        evidence.successor('q_actual t_actual 15 P2-question-carry-required-7a97 P2-task-carry-required-7a97', 'old', 'new', 15)
        evidence.refreshes = 0
        with self.assertRaises(matrix.MatrixError):
            evidence.successor('q_actual t_actual 15 P2-question-carry-required-7a97 P2-task-carry-required-7a97 P2-order-carry-excluded-7a97', 'old', 'new', 15)
        evidence.refreshes = 0
        with self.assertRaises(matrix.MatrixError):
            evidence.successor('q_actual t_actual 99 P2-task-carry-required-7a97', 'old', 'new', 99)

    def test_budget_and_targets(self):
        evidence = matrix.Evidence()
        for _ in range(12): evidence.instructed_turn('sender')
        with self.assertRaises(matrix.MatrixError): evidence.instructed_turn('sender')
        with self.assertRaises(matrix.MatrixError): matrix.native_send('production', 'Question', 'body')
        with self.assertRaises(matrix.MatrixError): matrix.native_send('proposalTwoReceiver', 'Question', 'body', 'id')

    def test_identity_ambiguity_refused(self):
        with self.assertRaises(matrix.MatrixError):
            matrix.identity_binding({'result': {'agents': []}}, {}, {}, 'pane', 'session')


class ChannelFixtures(unittest.TestCase):
    def setUp(self):
        import tempfile
        from pathlib import Path
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / 'evidence').mkdir()
        (self.root / 'transcripts').mkdir()
        self.channel = object.__new__(matrix.EvidenceChannel)
        self.channel.root = self.root
        self.channel.providers = {'flow': {'path': '/fixture-flow'}}
        self.channel.directory = self.root / 'evidence'
        self.channel.expected = []
        self.channel.requests = {}
        self.channel.consumed = set()
        self.channel.minutes = {}
        self.channel.invocations = set()
        self.channel.closed_controls = set()
        self.channel.close_attempts = set()
        self.channel.controls = {}
        self.channel.identity = {'sender': {'pane': 's'}, 'receiver': {'pane': 'r'}}
        self.channel.counter = 0

    def tearDown(self):
        self.temp.cleanup()

    def test_path_escape_and_symlink_rejected(self):
        import hashlib
        digest = hashlib.sha256(b'x').hexdigest()
        with self.assertRaises(matrix.MatrixError):
            self.channel._source({'path': '../elsewhere', 'sha256': digest})
        (self.root / 'evidence' / 'link').symlink_to('/etc/passwd')
        with self.assertRaises((matrix.MatrixError, OSError)):
            self.channel._source({'path': 'evidence/link', 'sha256': digest})

    def test_duplicate_and_spurious_cut_rejected(self):
        self.channel.register_control('control1', 'sender')
        self.channel.expect('cut-a', 'O', 'sender', 'Order', 'marker', 'control1')
        with self.assertRaises(matrix.MatrixError):
            self.channel.expect('cut-b', 'O', 'sender', 'Order', 'marker', 'control1')
        with self.assertRaises(matrix.MatrixError):
            self.channel.expect('cut-b', 'Q', 'receiver', 'Question', 'marker', 'control1')

    def test_dynamic_rehearsal_review_binds_both_actual_hashes(self):
        import json
        from unittest import mock
        hashes = {'sender': 'a'*64, 'receiver': 'b'*64}
        response = {'cut': 'rehearsal-review', 'sha256': hashes, 'decision': 'approved'}
        with mock.patch.object(self.channel, '_next_frame', return_value=json.dumps(response).encode()):
            self.channel.review_rehearsals(hashes, 1)

    def test_rehearsal_review_refuses_other_bytes(self):
        import json
        from unittest import mock
        hashes = {'sender': 'a'*64, 'receiver': 'b'*64}
        response = {'cut': 'rehearsal-review', 'sha256': {'sender': 'c'*64, 'receiver': 'b'*64}, 'decision': 'approved'}
        with mock.patch.object(self.channel, '_next_frame', return_value=json.dumps(response).encode()):
            with self.assertRaises(matrix.MatrixError):
                self.channel.review_rehearsals(hashes, 1)

    def test_admission_and_consumption_are_separate_cuts(self):
        import hashlib, json
        from unittest import mock
        receipt = json.dumps({'success': True, 'contentItems': [{'type': 'inputText', 'text': 'Accepted.{ Sender.{ Mind proposalTwoSender Luna } { Mind proposalTwoReceiver Luna } { req1 1 Queued } }'}]}).encode()
        call = json.dumps({'call_id': 'call-o', 'arguments': matrix.native_send('proposalTwoReceiver', 'Order', 'P2-order-before: record this marker and its request id; give no Result.')}).encode()
        transcript = b'receiver read marker req1\n'
        (self.root / 'evidence' / 'receipt').write_bytes(receipt)
        (self.root / 'evidence' / 'call').write_bytes(call)
        (self.root / 'transcripts' / 'reply').write_bytes(transcript)
        admission = {'cut': 'admission', 'label': 'O', 'kind': 'Order', 'marker': 'marker', 'request_id': 'req1',
                     'minutes': None, 'invocation': {'path': 'evidence/call', 'sha256': hashlib.sha256(call).hexdigest()},
                     'receipt': {'path': 'evidence/receipt', 'sha256': hashlib.sha256(receipt).hexdigest()},
                     'identity': {'pane': 's'}}
        consumption = {'cut': 'consumption', 'label': 'O', 'request_id': 'req1', 'marker': 'marker',
                       'identity': {'pane': 'r'}, 'reply': 'receiver read marker req1',
                       'transcript': {'path': 'transcripts/reply', 'sha256': hashlib.sha256(transcript).hexdigest()}}
        with mock.patch.object(self.channel, '_next_frame', side_effect=[json.dumps(admission).encode(), json.dumps(consumption).encode()]):
            import controller
            self.channel.receive_admission('O', 'Order', 'marker', 1, controller.receipt_tokens)
            self.assertEqual(self.channel.requests['O'], 'req1')
            self.channel.receive_consumption('O', 'marker', 1)

    def test_unresolved_reply_and_reused_call_id(self):
        import hashlib, json
        import controller
        from unittest import mock
        invocation = matrix.native_send('proposalTwoSender', 'Result', 'body', 'request1')
        call = json.dumps({'call_id': 'call1', 'arguments': invocation}).encode()
        response = json.dumps({'success': False, 'contentItems': [{'type': 'inputText', 'text': 'Refused.Unresolved'}]}).encode()
        (self.root / 'evidence' / 'call').write_bytes(call)
        (self.root / 'evidence' / 'response').write_bytes(response)
        event = {'cut': 'reply-outcome', 'label': 'wrong', 'surface': 'native', 'identity': {'pane': 'r'},
                 'invocation': {'path': 'evidence/call', 'sha256': hashlib.sha256(call).hexdigest()},
                 'response': {'path': 'evidence/response', 'sha256': hashlib.sha256(response).hexdigest()}}
        with mock.patch.object(self.channel, '_next_frame', return_value=json.dumps(event).encode()):
            self.channel.receive_reply_outcome('wrong', 'native', invocation, 'unresolved', 1, controller.receipt_tokens)
            with self.assertRaises(matrix.MatrixError):
                self.channel.receive_reply_outcome('wrong', 'native', invocation, 'unresolved', 1, controller.receipt_tokens)

    def test_kept_receipt_rejects_wrong_sender_or_request(self):
        import hashlib, json
        import controller
        from unittest import mock
        invocation = matrix.native_send('proposalTwoSender', 'Result', 'P2-kept-answer', 'request1')
        call = json.dumps({'call_id': 'call-kept', 'arguments': invocation}).encode()
        response = json.dumps({'success': True, 'contentItems': [{'type': 'inputText', 'text': 'Kept.{ Sender.{ Mind other Luna } request1 }'}]}).encode()
        (self.root / 'evidence' / 'call').write_bytes(call)
        (self.root / 'evidence' / 'response').write_bytes(response)
        event = {'cut': 'reply-outcome', 'label': 'kept', 'surface': 'native', 'identity': {'pane': 'r'},
                 'invocation': {'path': 'evidence/call', 'sha256': hashlib.sha256(call).hexdigest()},
                 'response': {'path': 'evidence/response', 'sha256': hashlib.sha256(response).hexdigest()}}
        with mock.patch.object(self.channel, '_next_frame', return_value=json.dumps(event).encode()):
            with self.assertRaises(matrix.MatrixError):
                self.channel.receive_reply_outcome('kept', 'native', invocation, 'kept', 1, controller.receipt_tokens)

    def test_control_answer_waits_for_native_kept_evidence(self):
        import hashlib, json
        import controller
        from unittest import mock
        self.channel.register_control('control1', 'receiver')
        call = json.dumps({'call_id': 'control-call', 'arguments': {'kind': 'Result', 'request': 'control1'}}).encode()
        response = json.dumps({'success': True, 'contentItems': [{'type': 'inputText', 'text': 'Kept.{ Sender.{ Mind proposalTwoReceiver Luna } control1 }'}]}).encode()
        (self.root / 'evidence' / 'call').write_bytes(call)
        (self.root / 'evidence' / 'response').write_bytes(response)
        event = {'cut': 'control-completion', 'request_id': 'control1', 'side': 'receiver', 'identity': {'pane': 'r'},
                 'invocation': {'path': 'evidence/call', 'sha256': hashlib.sha256(call).hexdigest()},
                 'response': {'path': 'evidence/response', 'sha256': hashlib.sha256(response).hexdigest()}}
        def private_call(owner, label, binary, request):
            self.assertIn('control-call', self.channel.invocations)
            return 'Answered.{ Sender.{ Mind proposalTwoReceiver Luna } Soft.Result.{ control1 «done» } }'
        with mock.patch.object(self.channel, '_next_frame', return_value=json.dumps(event).encode()):
            matrix.close_control_questions(object(), self.channel, 1, private_call, controller.receipt_tokens)
        self.assertEqual(self.channel.closed_controls, {'control1'})

    def test_missing_transcript_and_invented_id_refused(self):
        import hashlib, json
        from unittest import mock
        receipt = {'success': True, 'contentItems': [{'type': 'inputText', 'text': 'Accepted.{ real-id }'}]}
        data = json.dumps(receipt).encode()
        (self.root / 'evidence' / 'receipt').write_bytes(data)
        self.channel.register_control('control1', 'sender')
        self.channel.expect('cut-a', 'O', 'sender', 'Order', 'marker', 'control1')
        event = {'cut':'cut-a','label':'O','side':'sender','kind':'Order','marker':'marker',
                 'control_id':'control1','request_id':'invented','minutes':None,
                 'receipt':{'path':'evidence/receipt','sha256':hashlib.sha256(data).hexdigest()},
                 'transcript':{'path':'transcripts/missing','sha256':'0'*64},
                 'acknowledgement':'marker invented','identity':{'pane':'s'},
                 'reader_side':'receiver','reader_identity':{'pane':'r'}}
        with mock.patch.object(self.channel, '_next_frame', return_value=json.dumps(event).encode()):
            with self.assertRaises((matrix.MatrixError, OSError)):
                self.channel.receive(1)

    def test_invented_id_not_present_in_receipt(self):
        import hashlib, json
        from unittest import mock
        receipt = json.dumps({'success': True, 'contentItems': [{'type': 'inputText', 'text': 'Accepted.{ real-id }'}]}).encode()
        transcript = b'ack marker invented\n'
        (self.root / 'evidence' / 'receipt').write_bytes(receipt)
        (self.root / 'transcripts' / 'reply').write_bytes(transcript)
        self.channel.register_control('control1', 'sender')
        self.channel.expect('cut-a', 'O', 'sender', 'Order', 'marker', 'control1')
        event = {'cut':'cut-a','label':'O','side':'sender','kind':'Order','marker':'marker',
                 'control_id':'control1','request_id':'invented','minutes':None,
                 'receipt':{'path':'evidence/receipt','sha256':hashlib.sha256(receipt).hexdigest()},
                 'transcript':{'path':'transcripts/reply','sha256':hashlib.sha256(transcript).hexdigest()},
                 'acknowledgement':'ack marker invented','identity':{'pane':'s'},
                 'reader_side':'receiver','reader_identity':{'pane':'r'}}
        with mock.patch.object(self.channel, '_next_frame', return_value=json.dumps(event).encode()):
            with self.assertRaises(matrix.MatrixError):
                self.channel.receive(1)


class ObserverDrainFixtures(unittest.TestCase):
    def make_stream(self):
        import os, selectors, threading
        from unittest import mock
        data_read, data_write = os.pipe2(os.O_NONBLOCK | os.O_CLOEXEC)
        exit_read, exit_write = os.pipe2(os.O_NONBLOCK | os.O_CLOEXEC)
        observed = threading.Event()
        chunks = []
        output = mock.Mock()
        output.write.side_effect = lambda value: (chunks.append(value), observed.set())
        stream = object.__new__(matrix.Stream)
        stream.name = 'observe-sends'
        stream.fd = data_read
        stream.pidfd = exit_read
        stream.selector = selectors.DefaultSelector()
        stream.selector.register(data_read, selectors.EVENT_READ, 'output')
        stream.selector.register(exit_read, selectors.EVENT_READ, 'exit')
        stream.output = output
        stream.process = mock.Mock()
        stream.process.stdout.close.side_effect = lambda: os.close(data_read)
        stream.drain_thread = None
        stream.drain_failure = None
        stream.stop_read = stream.stop_write = stream.failure_read = stream.failure_write = None
        return stream, data_write, exit_write, observed, chunks

    def test_drain_retains_data_and_joins_at_stop_event(self):
        import os, time
        stream, writer, exit_writer, observed, chunks = self.make_stream()
        try:
            stream.start_drain(time.monotonic() + 5)
            os.write(writer, b'SendChanged.fixture\n')
            self.assertTrue(observed.wait(2))
            stream.close_observer(2)
            self.assertEqual(b''.join(chunks), b'SendChanged.fixture\n')
            self.assertIsNone(stream.drain_thread)
        finally:
            os.close(writer)
            os.close(exit_writer)

    def test_drain_eof_is_reported_and_joined(self):
        import os, select, time
        stream, writer, exit_writer, observed, chunks = self.make_stream()
        try:
            failure = stream.start_drain(time.monotonic() + 5)
            os.close(writer)
            writer = None
            self.assertTrue(select.select([failure], [], [], 2)[0])
            with self.assertRaises(matrix.MatrixError):
                stream.close_observer(2)
            self.assertIsNone(stream.drain_thread)
        finally:
            if writer is not None: os.close(writer)
            os.close(exit_writer)


class LaunchFixtures(unittest.TestCase):
    def test_successor_inspect_binds_flow_session_route_and_private_endpoint(self):
        import controller
        binding = {'flow_id': 'new', 'native_session': 'sess2', 'herdr_session': 'private', 'agent': 'agent', 'pane': 'pane2', 'terminal': 'term2'}
        text = ('Inspected.{ { { Mind proposalTwoReceiver Luna } Awake.new [] [] } '
                '{ Some.{ new sess2 Codex Available.{ /private/runtime/codex/control.sock Ready } '
                'Available.{ private agent pane2 term2 } Unbound Active } None } [] [] None None }')
        matrix.verify_successor_inspect(text, binding, '/private', controller.receipt_tokens)
        with self.assertRaises(matrix.MatrixError):
            matrix.verify_successor_inspect(text.replace('pane2', 'other'), binding, '/private', controller.receipt_tokens)
        with self.assertRaises(matrix.MatrixError):
            matrix.verify_successor_inspect(text.replace('/private/runtime', '/foreign/runtime'), binding, '/private', controller.receipt_tokens)

    def test_refresh_queued_waits_for_real_changed_successor(self):
        from unittest import mock
        import controller
        old = {'flow_id': 'old', 'native_session': 'sess1', 'herdr_session': 'private', 'agent': 'agent1', 'pane': 'pane1', 'terminal': 'term1'}
        new = {'flow_id': 'new', 'native_session': 'sess2', 'herdr_session': 'private', 'agent': 'agent2', 'pane': 'pane2', 'terminal': 'term2'}
        owner = mock.Mock(manifest={'root': '/private', 'session': 'private'})
        channel = mock.Mock()
        channel.identity = {'receiver': old}
        channel.controls = {}
        channel.closed_controls = set()
        channel.receive_successor.return_value = (new, 'q2 t2 15 P2-question-carry-required-7a97 P2-task-carry-required-7a97')
        ledger = matrix.Evidence()
        ledger.request('O2', 'o2', 'Order'); ledger.request('Q2', 'q2', 'Question'); ledger.request('T2', 't2', 'Task', 15)
        replies = {'receiver-refresh': 'RefreshQueued.{ { Mind proposalTwoReceiver Luna } old }',
                   'successor-current': 'Current.Awake.new',
                   'successor-inspect': 'Inspected.fixture'}
        def call(owner, label, binary, request): return replies[label]
        stream = mock.Mock()
        stream.next_line.return_value = 'MetaflowChanged.{ { Mind proposalTwoReceiver Luna } Awake.new [] [] }'
        panes = {'id': 'cli:pane:list', 'result': {'type': 'pane_list', 'panes': []}}
        with mock.patch.object(matrix, 'Stream', return_value=stream), mock.patch.object(matrix, 'snapshot_native'), \
             mock.patch.object(matrix, 'verify_successor_inspect'), mock.patch.object(matrix, 'herdr_json', return_value=panes):
            self.assertEqual(matrix.refresh_successor(owner, channel, ledger, old, 99, call, controller.receipt_tokens, controller.receipt), new)
            with self.assertRaises(matrix.MatrixError):
                matrix.refresh_successor(owner, channel, ledger, old, 99, call, controller.receipt_tokens, controller.receipt)
        self.assertEqual(channel.identity['receiver'], new)
        self.assertEqual(ledger.refreshes, 1)

    def test_successor_reply_order_and_closure_pair(self):
        from unittest import mock
        ledger = matrix.Evidence()
        ledger.request('O2', 'o2', 'Order'); ledger.request('Q2', 'q2', 'Question'); ledger.request('T2', 't2', 'Task', 15)
        ledger.task_cutoffs['T2'] = float('inf')
        owner = mock.Mock(manifest={'root': '/private', 'providers': {'flow': {'path': '/flow'}}})
        channel = mock.Mock()
        with mock.patch.object(matrix, 'control_question', side_effect=['inspect', 'authorize', 'sender']):
            matrix.complete_successor_carry(owner, channel, ledger, 1, object(), object())
        self.assertEqual([c.args[0] for c in channel.receive_reply_outcome.call_args_list],
                         ['carry-result', 'carry-done', 'carry-duplicate-result', 'carry-duplicate-done', 'carry-order-result'])
        self.assertEqual(channel.receive_routed_consumption.call_count, 2)

    def test_closure_attempts_only_captured_pair_even_if_first_fails(self):
        from unittest import mock
        bindings = {'sender': {'flow_id': 'send1'}, 'receiver': {'flow_id': 'recv2'}}
        channel = mock.Mock()
        channel.identity = dict(bindings)
        channel.close_attempts = set()
        def call(owner, label, binary, request): return 'Inspected.fixture'
        with mock.patch.object(matrix, 'close_control_questions'), \
             mock.patch.object(matrix, 'close_bound_flow_and_pane', side_effect=[matrix.MatrixError('failed'), None]) as close:
            with self.assertRaises(matrix.MatrixError):
                matrix.close_synthetic_flows(object(), channel, bindings, 1, call, object(), object())
        self.assertEqual([item.args[1] for item in close.call_args_list], ['receiver', 'sender'])

    def test_graceful_close_requires_bound_snapshot_and_typed_pane_success(self):
        from unittest import mock
        binding = {'pane': 'pane1', 'terminal': 'terminal1', 'native_session': 'session1', 'flow_id': 'flow1'}
        with mock.patch.object(matrix, 'snapshot_native') as snapshot, \
             mock.patch.object(matrix, 'close_flow') as close, \
             mock.patch.object(matrix, 'herdr_json', side_effect=[
                 {'id': 'cli:pane:list', 'result': {'type': 'pane_list', 'panes': [
                     {'pane_id': 'pane1', 'terminal_id': 'terminal1'}]}},
                 {'id': 'cli:agent:get', 'result': {'type': 'agent_info', 'agent': {'agent_session': {'value': 'session1'}}}},
                 {'id': 'cli:pane:close', 'result': {'type': 'ok'}}]) as herdr:
            matrix.close_bound_flow_and_pane(object(), 'receiver', binding, object(), object())
            snapshot.assert_called_once()
            close.assert_called_once()
            self.assertEqual(herdr.call_args.args[2], ['pane', 'close', 'pane1'])

    def test_graceful_close_refuses_unknown_pane_receipt(self):
        from unittest import mock
        binding = {'pane': 'pane1', 'terminal': 'terminal1', 'native_session': 'session1', 'flow_id': 'flow1'}
        with mock.patch.object(matrix, 'snapshot_native'), mock.patch.object(matrix, 'close_flow'), \
             mock.patch.object(matrix, 'herdr_json', side_effect=[
                 {'id': 'cli:pane:list', 'result': {'type': 'pane_list', 'panes': [
                     {'pane_id': 'pane1', 'terminal_id': 'terminal1'}]}},
                 {'id': 'cli:agent:get', 'result': {'type': 'agent_info', 'agent': {'agent_session': {'value': 'session1'}}}},
                 {'result': {'type': 'ok'}}]):
            with self.assertRaises(matrix.MatrixError):
                matrix.close_bound_flow_and_pane(object(), 'receiver', binding, object(), object())

    def test_started_complete_shape_and_private_session(self):
        import controller
        row = matrix.parse_started('Started.{ a1b2c3 «native-1» Available.{ private agent pane terminal } Unbound }', 'private', controller.receipt_tokens)
        self.assertEqual(row['flow_id'], 'a1b2c3')
        self.assertEqual(row['native_session'], 'native-1')
        for bad in ('Started.{ a1b2c3 native Available.{ public agent pane terminal } Unbound }',
                    'Started.{ a1b2c3 native Available.{ private agent pane terminal } Unbound } junk',
                    'Started.{ a1b2c3 native Unavailable Unbound }'):
            with self.assertRaises(matrix.MatrixError):
                matrix.parse_started(bad, 'private', controller.receipt_tokens)


if __name__ == '__main__':
    unittest.main()
