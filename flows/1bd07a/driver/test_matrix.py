"""Unrun pure fixtures; no native launches, tools, services or observers."""
import unittest
import matrix


class MatrixFixtures(unittest.TestCase):
    def test_request_id_exact_lowercase_base36(self):
        for value in ('0000', 'abcd', '9z0a'):
            self.assertTrue(matrix.valid_request_id(value))
        for value in ('abc', 'abcde', 'AB12', 'a-12', 'é123', '', None):
            self.assertFalse(matrix.valid_request_id(value))

    def test_unknown_draw_collision_stops_before_instruction(self):
        from unittest import mock
        ledger = matrix.Evidence()
        ledger.request('O', 'aa01', 'Order'); ledger.request('Q', 'aa02', 'Question'); ledger.request('T', 'aa03', 'Task', 15)
        channel = mock.Mock()
        channel.requests = {'O': 'aa01'}
        channel.controls = {'aaaa': 'sender'}
        with mock.patch.object(matrix.secrets, 'choice', return_value='a'), mock.patch.object(matrix, 'control_question') as question:
            with self.assertRaises(matrix.MatrixError):
                matrix.collect_phase_a_consumption(mock.Mock(), channel, ledger, 1, object(), object())
            question.assert_not_called()

    def test_delivery_state_complete_nested_decode_and_malformed_rejection(self):
        import controller
        valid = ('Queued', 'Attempting', 'Uncertain', 'Delivered', 'Read', 'Withdrawn', 'Archived',
                 'Retryable.HistoryAbsent', 'Retryable.WakeRefused.CompositionRefused.Unconfigured',
                 'Retryable.WakeRefused.HarnessSpawnRefused.{ Herdr.{ None «error» } Some.{ session Answered Archived } }',
                 'Failed.Locked', 'Failed.Held.{ { Mind topic Luna } { Field other Sol } 1 }',
                 'Failed.Unidentified.{ Some.{ session pane } None Some.«native» 123 { 1 2 } }',
                 'Failed.Oversized.{ 5 4 }')
        for value in valid:
            with self.subTest(value=value):
                parsed = matrix.typed_receipt(value, controller.receipt_tokens)
                _, remaining = matrix.consume_typed(matrix.delivery_state_schema(), parsed)
                self.assertEqual(remaining, [])
        for value in ('Retryable.', 'Retryable.HistoryAbsent.extra', 'Failed.', 'Failed.Oversized.{ 5 }',
                      'Failed.Unidentified.[]', 'Failed.Locked.extra', 'Retryable.WakeRefused.Bogus'):
            with self.subTest(value=value), self.assertRaises(matrix.MatrixError):
                parsed = matrix.typed_receipt(value, controller.receipt_tokens)
                _, remaining = matrix.consume_typed(matrix.delivery_state_schema(), parsed)
                if remaining: raise matrix.MatrixError('trailing state input')
        for value in ('Retryable.HistoryAbsent', 'Failed.Locked'):
            with self.assertRaises(matrix.MatrixError):
                matrix.parse_visible_admission('SendAccepted.{ aa01 1 ' + value + ' }', controller.receipt_tokens)

    def test_phase_a_reply_order_and_duplicate_new_calls(self):
        from unittest import mock
        owner = mock.Mock(manifest={'root': '/private', 'providers': {'flow': {'path': '/flow'}}})
        ledger = matrix.Evidence()
        ledger.request('O', 'or01', 'Order')
        ledger.request('Q', 'qu01', 'Question')
        ledger.request('T', 'ta01', 'Task', 15)
        channel = mock.Mock()
        with mock.patch.object(matrix, 'control_question', return_value='control'):
            matrix.collect_phase_a_reply_outcomes(owner, channel, ledger, 'un01', 1, object(), object())
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
                return 'SendAccepted.{ kp01 3 Queued }'
            return 'Answered.{ Sender.{ Mind proposalTwoReceiver Luna } Soft.Result.{ kp01 P2-kept-answer } }'
        with mock.patch.object(matrix, 'control_question', return_value='control'):
            self.assertEqual(matrix.kept_answer_case(owner, channel, ledger, 1, call, controller.receipt_tokens, controller.receipt), 'kp01')
        channel.receive_reply_outcome.assert_called_once()
        channel.receive_consumption.assert_called_once()

    def test_phase_a_collects_admissions_in_order(self):
        from unittest import mock
        owner = mock.Mock(manifest={'root': '/private', 'providers': {'flow': {'path': '/flow'}}})
        channel = mock.Mock()
        def admission(label, kind, marker, deadline, receipt_tokens):
            return {'request_id': {'O':'aa01', 'Q':'aa02', 'T':'aa03', 'N':'aa04', 'L':'aa05'}[label], 'minutes': 15 if kind == 'Task' else None}
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
        evidence.request('Q2', 'aq01', 'Question')
        with self.assertRaises(matrix.MatrixError): evidence.request('T2', 'aq01', 'Task', 123)
        with self.assertRaises(matrix.MatrixError): evidence.request('O2', 'ao01', 'Question')

    def test_carry_and_order_exclusion(self):
        evidence = matrix.Evidence()
        evidence.request('O2', 'oo01', 'Order')
        evidence.request('Q2', 'qq01', 'Question')
        evidence.request('T2', 'tt01', 'Task', 15)
        evidence.successor('qq01 tt01 15 P2-question-carry-required-7a97 P2-task-carry-required-7a97', 'old', 'new', 15)
        evidence.refreshes = 0
        with self.assertRaises(matrix.MatrixError):
            evidence.successor('qq01 tt01 15 P2-question-carry-required-7a97 P2-task-carry-required-7a97 P2-order-carry-excluded-7a97', 'old', 'new', 15)
        evidence.refreshes = 0
        with self.assertRaises(matrix.MatrixError):
            evidence.successor('qq01 tt01 99 P2-task-carry-required-7a97', 'old', 'new', 99)

    def test_budget_and_targets(self):
        evidence = matrix.Evidence()
        for _ in range(12): evidence.instructed_turn('sender')
        with self.assertRaises(matrix.MatrixError): evidence.instructed_turn('sender')
        with self.assertRaises(matrix.MatrixError): matrix.native_send('production', 'Question', 'body')
        with self.assertRaises(matrix.MatrixError): matrix.native_send('proposalTwoReceiver', 'Question', 'body', 'id')

    def test_control_string_quotes_both_guillemets_and_backslashes(self):
        import controller
        for prompt in ('nested «Task.«content»»', 'unmatched «', 'unmatched »',
                       'backslash \\ and \\« edge', 'plain'):
            with self.subTest(prompt=prompt):
                quoted = matrix.quoted_content(prompt)
                self.assertEqual(controller.receipt_tokens('«' + quoted + '»'), [('quoted', prompt)])

    def test_identity_ambiguity_refused(self):
        with self.assertRaises(matrix.MatrixError):
            matrix.identity_binding({'result': {'agents': []}}, {}, {}, {'pane': 'pane'})

    def test_supported_agent_binding_optional_session_and_route(self):
        import copy
        binding = {'agent': 'agent', 'pane': 'pane', 'terminal': 'term', 'native_session': 'native'}
        row = {'name': 'agent', 'pane_id': 'pane', 'terminal_id': 'term'}
        def check(item, rows=None, process_pane='pane'):
            return matrix.identity_binding(
                {'id': 'cli:agent:list', 'result': {'type': 'agent_list', 'agents': [item] if rows is None else rows}},
                {'id': 'cli:agent:get', 'result': {'type': 'agent_info', 'agent': item}},
                {'id': 'cli:pane:process_info', 'result': {'type': 'pane_process_info', 'process_info': {'pane_id': process_pane}}}, binding)
        self.assertEqual(check(row)['pane_id'], 'pane')
        self.assertEqual(check(dict(row, agent_session={'value': 'native'}))['pane_id'], 'pane')
        for changed in (dict(row, agent_session={'value': 'other'}), dict(row, name='other'),
                        dict(row, pane_id='other'), dict(row, terminal_id='other')):
            with self.subTest(changed=changed), self.assertRaises(matrix.MatrixError):
                check(changed)
        with self.assertRaises(matrix.MatrixError):
            check(row, rows=[row, copy.deepcopy(row)])
        with self.assertRaises(matrix.MatrixError):
            check(row, process_pane='other')


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
        self.channel.register_control('ct01', 'sender')
        self.channel.expect('cut-a', 'O', 'sender', 'Order', 'marker', 'ct01')
        with self.assertRaises(matrix.MatrixError):
            self.channel.expect('cut-b', 'O', 'sender', 'Order', 'marker', 'ct01')
        with self.assertRaises(matrix.MatrixError):
            self.channel.expect('cut-b', 'Q', 'receiver', 'Question', 'marker', 'ct01')

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
        invocation = matrix.native_send('proposalTwoSender', 'Result', 'body', 'rq01')
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
        invocation = matrix.native_send('proposalTwoSender', 'Result', 'P2-kept-answer', 'rq01')
        call = json.dumps({'call_id': 'call-kept', 'arguments': invocation}).encode()
        response = json.dumps({'success': True, 'contentItems': [{'type': 'inputText', 'text': 'Kept.{ Sender.{ Mind other Luna } rq01 }'}]}).encode()
        (self.root / 'evidence' / 'call').write_bytes(call)
        (self.root / 'evidence' / 'response').write_bytes(response)
        event = {'cut': 'reply-outcome', 'label': 'kept', 'surface': 'native', 'identity': {'pane': 'r'},
                 'invocation': {'path': 'evidence/call', 'sha256': hashlib.sha256(call).hexdigest()},
                 'response': {'path': 'evidence/response', 'sha256': hashlib.sha256(response).hexdigest()}}
        with mock.patch.object(self.channel, '_next_frame', return_value=json.dumps(event).encode()):
            with self.assertRaises(matrix.MatrixError):
                self.channel.receive_reply_outcome('kept', 'native', invocation, 'kept', 1, controller.receipt_tokens)

    def test_accepted_reply_rejects_another_answered_id_on_both_surfaces(self):
        import hashlib, json
        import controller
        from unittest import mock
        for index, surface in enumerate(('native', 'cli')):
            with self.subTest(surface=surface):
                invocation = (matrix.native_send('proposalTwoSender', 'Result', 'body', 'aa01') if surface == 'native' else
                              matrix.private_cli({'root': '/private', 'providers': {'flow': {'path': '/flow'}}}, 'Send.{ { Mind proposalTwoSender Luna } Soft.Done.{ aa01 «body» } }'))
                call = json.dumps({'call_id': 'case' + str(index), 'arguments' if surface == 'native' else 'command': invocation}).encode()
                text = ('Accepted.{ Sender.{ Mind proposalTwoReceiver Luna } { Mind proposalTwoSender Luna } { aa02 2 Delivered } }'
                        if surface == 'native' else 'SendAccepted.{ aa02 2 Delivered }')
                response = json.dumps({'success': True, 'contentItems': [{'type': 'inputText', 'text': text}]}).encode() if surface == 'native' else text.encode()
                (self.root / 'evidence' / ('call' + str(index))).write_bytes(call)
                (self.root / 'evidence' / ('response' + str(index))).write_bytes(response)
                event = {'cut': 'reply-outcome', 'label': 'wrong-' + surface, 'surface': surface, 'identity': {'pane': 'r'},
                         'invocation': {'path': 'evidence/call' + str(index), 'sha256': hashlib.sha256(call).hexdigest()},
                         'response': {'path': 'evidence/response' + str(index), 'sha256': hashlib.sha256(response).hexdigest()}}
                with mock.patch.object(self.channel, '_next_frame', return_value=json.dumps(event).encode()):
                    with self.assertRaises(matrix.MatrixError):
                        self.channel.receive_reply_outcome('wrong-' + surface, surface, invocation, 'accepted', 1, controller.receipt_tokens, 'aa01')

    def test_control_answer_waits_for_native_kept_evidence(self):
        import hashlib, json
        import controller
        from unittest import mock
        self.channel.register_control('ct01', 'receiver')
        call = json.dumps({'call_id': 'control-call', 'arguments': {'kind': 'Result', 'request': 'ct01'}}).encode()
        response = json.dumps({'success': True, 'contentItems': [{'type': 'inputText', 'text': 'Kept.{ Sender.{ Mind proposalTwoReceiver Luna } ct01 }'}]}).encode()
        (self.root / 'evidence' / 'call').write_bytes(call)
        (self.root / 'evidence' / 'response').write_bytes(response)
        event = {'cut': 'control-completion', 'request_id': 'ct01', 'side': 'receiver', 'identity': {'pane': 'r'},
                 'invocation': {'path': 'evidence/call', 'sha256': hashlib.sha256(call).hexdigest()},
                 'response': {'path': 'evidence/response', 'sha256': hashlib.sha256(response).hexdigest()}}
        def private_call(owner, label, binary, request):
            self.assertIn('control-call', self.channel.invocations)
            return 'Answered.{ Sender.{ Mind proposalTwoReceiver Luna } Soft.Result.{ ct01 «done» } }'
        with mock.patch.object(self.channel, '_next_frame', return_value=json.dumps(event).encode()):
            matrix.close_control_questions(object(), self.channel, 1, private_call, controller.receipt_tokens)
        self.assertEqual(self.channel.closed_controls, {'ct01'})

    def test_missing_transcript_and_in01_id_refused(self):
        import hashlib, json
        from unittest import mock
        receipt = {'success': True, 'contentItems': [{'type': 'inputText', 'text': 'Accepted.{ re01 }'}]}
        data = json.dumps(receipt).encode()
        (self.root / 'evidence' / 'receipt').write_bytes(data)
        self.channel.register_control('ct01', 'sender')
        self.channel.expect('cut-a', 'O', 'sender', 'Order', 'marker', 'ct01')
        event = {'cut':'cut-a','label':'O','side':'sender','kind':'Order','marker':'marker',
                 'control_id':'ct01','request_id':'in01','minutes':None,
                 'receipt':{'path':'evidence/receipt','sha256':hashlib.sha256(data).hexdigest()},
                 'transcript':{'path':'transcripts/missing','sha256':'0'*64},
                 'acknowledgement':'marker in01','identity':{'pane':'s'},
                 'reader_side':'receiver','reader_identity':{'pane':'r'}}
        with mock.patch.object(self.channel, '_next_frame', return_value=json.dumps(event).encode()):
            with self.assertRaises((matrix.MatrixError, OSError)):
                self.channel.receive(1)

    def test_in01_id_not_present_in_receipt(self):
        import hashlib, json
        from unittest import mock
        receipt = json.dumps({'success': True, 'contentItems': [{'type': 'inputText', 'text': 'Accepted.{ re01 }'}]}).encode()
        transcript = b'ack marker in01\n'
        (self.root / 'evidence' / 'receipt').write_bytes(receipt)
        (self.root / 'transcripts' / 'reply').write_bytes(transcript)
        self.channel.register_control('ct01', 'sender')
        self.channel.expect('cut-a', 'O', 'sender', 'Order', 'marker', 'ct01')
        event = {'cut':'cut-a','label':'O','side':'sender','kind':'Order','marker':'marker',
                 'control_id':'ct01','request_id':'in01','minutes':None,
                 'receipt':{'path':'evidence/receipt','sha256':hashlib.sha256(receipt).hexdigest()},
                 'transcript':{'path':'transcripts/reply','sha256':hashlib.sha256(transcript).hexdigest()},
                 'acknowledgement':'ack marker in01','identity':{'pane':'s'},
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

    def test_inspect_unavailable_endpoint_preserves_native_and_herdr_identity(self):
        import controller
        binding = {'flow_id': 'cf5866', 'native_session': '01a1f10f-a0e7-77c1-a6c3-610cf586613c',
                   'herdr_session': 'p2-2b0256fb', 'agent': 'codex-agent', 'pane': 'w1:p1', 'terminal': 'term-bound'}
        text = ('Inspected.{ { { Mind proposalTwoSender Luna } Awake.cf5866 [] [] } '
                '{ Some.{ cf5866 01a1f10f-a0e7-77c1-a6c3-610cf586613c Codex Unavailable '
                'Available.{ p2-2b0256fb codex-agent w1:p1 term-bound } Unbound Active } None } [] [] None Released }')
        matrix.verify_bound_inspect(text, binding, '/private', 'proposalTwoSender', controller.receipt_tokens)
        for original, changed in (('cf5866', 'wrongflow'),
                                  (binding['native_session'], 'wrongnative'),
                                  ('p2-2b0256fb', 'other-session'), ('codex-agent', 'other-agent'),
                                  ('w1:p1', 'w1:p2'), ('term-bound', 'other-terminal'),
                                  ('Active', 'Stopped'), ('Unavailable', 'Unknown')):
            with self.subTest(field=original), self.assertRaises(matrix.MatrixError):
                matrix.verify_bound_inspect(text.replace(original, changed), binding, '/private',
                                            'proposalTwoSender', controller.receipt_tokens)

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
        channel.receive_successor.return_value = (new, 'qq02 tt02 15 P2-question-carry-required-7a97 P2-task-carry-required-7a97')
        ledger = matrix.Evidence()
        ledger.request('O2', 'oo02', 'Order'); ledger.request('Q2', 'qq02', 'Question'); ledger.request('T2', 'tt02', 'Task', 15)
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
        ledger.request('O2', 'oo02', 'Order'); ledger.request('Q2', 'qq02', 'Question'); ledger.request('T2', 'tt02', 'Task', 15)
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
        binding = {'agent': 'bound-agent', 'pane': 'pane1', 'terminal': 'terminal1', 'native_session': 'session1', 'flow_id': 'flow1'}
        with mock.patch.object(matrix, 'snapshot_native') as snapshot, \
             mock.patch.object(matrix, 'close_flow') as close, \
             mock.patch.object(matrix, 'herdr_json', side_effect=[
                 {'id': 'cli:pane:list', 'result': {'type': 'pane_list', 'panes': [
                     {'pane_id': 'pane1', 'terminal_id': 'terminal1'}]}},
                 {'id': 'cli:agent:get', 'result': {'type': 'agent_info', 'agent': {'name': 'bound-agent', 'pane_id': 'pane1', 'terminal_id': 'terminal1'}}},
                 {'id': 'cli:pane:close', 'result': {'type': 'ok'}}]) as herdr:
            matrix.close_bound_flow_and_pane(object(), 'receiver', binding, object(), object())
            snapshot.assert_called_once()
            close.assert_called_once()
            self.assertEqual(herdr.call_args.args[2], ['pane', 'close', 'pane1'])

    def test_graceful_close_refuses_unknown_pane_receipt(self):
        from unittest import mock
        binding = {'agent': 'bound-agent', 'pane': 'pane1', 'terminal': 'terminal1', 'native_session': 'session1', 'flow_id': 'flow1'}
        with mock.patch.object(matrix, 'snapshot_native'), mock.patch.object(matrix, 'close_flow'), \
             mock.patch.object(matrix, 'herdr_json', side_effect=[
                 {'id': 'cli:pane:list', 'result': {'type': 'pane_list', 'panes': [
                     {'pane_id': 'pane1', 'terminal_id': 'terminal1'}]}},
                 {'id': 'cli:agent:get', 'result': {'type': 'agent_info', 'agent': {'name': 'bound-agent', 'pane_id': 'pane1', 'terminal_id': 'terminal1'}}},
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


# Exact attempt4 retained rows, unchanged; source SHA256 84b4321e748467998c64bb944a1a55538798f5be0bde0f646c99c826fc0d3358.
ATTEMPT4_TOOL_ROWS = (
    b'{"timestamp":"2026-11-19T00:33:19.914Z","ordinal":25,"type":"response_item","payload":{"type":"custom_tool_call","id":"ctc_0ead0a0f6abb8f58016afe43cebe1087d2b40281e11fc8a247","status":"completed","call_id":"call_190112e17b334e7484dc59540598b2a2","name":"exec","input":"const r = await tools.send({target:{aspect:\\"Mind\\",topic:\\"proposalTwoReceiver\\",model:\\"Luna\\"},priority:\\"Soft\\",kind:\\"Order\\",body:\\"P2-order-before: record this marker and its request id; give no Result.\\"});\\ntext(JSON.stringify(r));\\n","internal_chat_message_metadata_passthrough":{"turn_id":"01a1f138-d9c1-7040-93ce-9821961375b4","create_time":1795048398.7445085}}}\n',
    b'{"timestamp":"2026-11-19T00:33:20.500Z","ordinal":28,"type":"response_item","payload":{"type":"custom_tool_call_output","id":"ctco_01a1f138-e674-7522-9011-0e8f608d865c","call_id":"call_190112e17b334e7484dc59540598b2a2","output":[{"type":"input_text","text":"Script completed\\nWall time 0.6 seconds\\nOutput:\\n"},{"type":"input_text","text":"\\"Accepted.{ Sender.{ Mind proposalTwoSender Luna } { Mind proposalTwoReceiver Luna } { g9xa 8 Delivered } }\\""}],"internal_chat_message_metadata_passthrough":{"turn_id":"01a1f138-d9c1-7040-93ce-9821961375b4","create_time":1795048400.5002782}},"metadata":{"client_authored":false,"fallback_token_limit_override":12000}}\n',
    b'{"timestamp":"2026-11-19T00:33:22.510Z","ordinal":32,"type":"response_item","payload":{"type":"custom_tool_call","id":"ctc_0ead0a0f6abb8f58016afe43d17ab087d28cea526c36ab1a95","status":"completed","call_id":"call_b2fb805fb70f4a189c9d165f025c587d","name":"exec","input":"const r = await tools.send({target:{aspect:\\"Mind\\",topic:\\"proposalTwoReceiver\\",model:\\"Luna\\"},priority:\\"Soft\\",kind:\\"Question\\",body:\\"P2-question-before: keep unanswered until explicitly authorized in phase A.\\"});\\ntext(JSON.stringify(r));\\n","internal_chat_message_metadata_passthrough":{"turn_id":"01a1f138-d9c1-7040-93ce-9821961375b4","create_time":1795048401.4815857}}}\n',
    b'{"timestamp":"2026-11-19T00:33:22.534Z","ordinal":35,"type":"response_item","payload":{"type":"custom_tool_call_output","id":"ctco_01a1f138-ee66-7bb0-bbac-5685b49cea5f","call_id":"call_b2fb805fb70f4a189c9d165f025c587d","output":[{"type":"input_text","text":"Script completed\\nWall time 0.0 seconds\\nOutput:\\n"},{"type":"input_text","text":"\\"Accepted.{ Sender.{ Mind proposalTwoSender Luna } { Mind proposalTwoReceiver Luna } { ay87 9 Queued } }\\""}],"internal_chat_message_metadata_passthrough":{"turn_id":"01a1f138-d9c1-7040-93ce-9821961375b4","create_time":1795048402.5340507}},"metadata":{"client_authored":false,"fallback_token_limit_override":12000}}\n',
    b'{"timestamp":"2026-11-19T00:33:25.309Z","ordinal":39,"type":"response_item","payload":{"type":"custom_tool_call","id":"ctc_0ead0a0f6abb8f58016afe43d3575c87d2b955e61dba8f1317","status":"completed","call_id":"call_7e58d00730fd4dd8a9c1e56cdd16062e","name":"exec","input":"const r=await tools.exec_command({cmd:\\"XDG_CONFIG_HOME=/tmp/p2-42bb5c51/config /nix/store/76vvsfvdifhplj44d3sp6crc704wkg11-flow-workspace-0.60.1/bin/flow \'Send.{ { Mind proposalTwoReceiver Luna } Soft.Task.{ 15 \xc2\xabP2-task-before: hold until phase A authorization.\xc2\xbb } }\'\\",yield_time_ms:10000});\\ntext(JSON.stringify(r));\\n","internal_chat_message_metadata_passthrough":{"turn_id":"01a1f138-d9c1-7040-93ce-9821961375b4","create_time":1795048403.3429613}}}\n',
    b'{"timestamp":"2026-11-19T00:33:25.376Z","ordinal":42,"type":"response_item","payload":{"type":"custom_tool_call_output","id":"ctco_01a1f138-f980-7363-bf08-da0421bc0d1c","call_id":"call_7e58d00730fd4dd8a9c1e56cdd16062e","output":[{"type":"input_text","text":"Script completed\\nWall time 0.1 seconds\\nOutput:\\n"},{"type":"input_text","text":"{\\"chunk_id\\":\\"0dffbf\\",\\"wall_time_seconds\\":0.000015217,\\"exit_code\\":0,\\"original_token_count\\":8,\\"output\\":\\"SendAccepted.{ jhn8 10 Queued }\\\\n\\"}"}],"internal_chat_message_metadata_passthrough":{"turn_id":"01a1f138-d9c1-7040-93ce-9821961375b4","create_time":1795048405.3760428}},"metadata":{"client_authored":false,"fallback_token_limit_override":12000}}\n',
    b'{"timestamp":"2026-11-19T00:33:27.243Z","ordinal":46,"type":"response_item","payload":{"type":"custom_tool_call","id":"ctc_0ead0a0f6abb8f58016afe43d6316087d2a52bd390ef0d739f","status":"completed","call_id":"call_7731dea816d5467784fc1b67889eb692","name":"exec","input":"const r=await tools.send({target:{aspect:\\"Mind\\",topic:\\"proposalTwoReceiver\\",model:\\"Luna\\"},priority:\\"Soft\\",kind:\\"Notice\\",body:\\"P2-notice-before: record marker; no answer.\\"});\\ntext(JSON.stringify(r));\\n","internal_chat_message_metadata_passthrough":{"turn_id":"01a1f138-d9c1-7040-93ce-9821961375b4","create_time":1795048406.1945813}}}\n',
    b'{"timestamp":"2026-11-19T00:33:27.269Z","ordinal":49,"type":"response_item","payload":{"type":"custom_tool_call_output","id":"ctco_01a1f139-00e5-7ce3-bf46-a0d6abe10bae","call_id":"call_7731dea816d5467784fc1b67889eb692","output":[{"type":"input_text","text":"Script completed\\nWall time 0.0 seconds\\nOutput:\\n"},{"type":"input_text","text":"\\"Accepted.{ Sender.{ Mind proposalTwoSender Luna } { Mind proposalTwoReceiver Luna } { 3az9 11 Queued } }\\""}],"internal_chat_message_metadata_passthrough":{"turn_id":"01a1f138-d9c1-7040-93ce-9821961375b4","create_time":1795048407.269726}},"metadata":{"client_authored":false,"fallback_token_limit_override":12000}}\n',
    b'{"timestamp":"2026-11-19T00:33:30.163Z","ordinal":51,"type":"response_item","payload":{"type":"custom_tool_call","id":"ctc_0ead0a0f6abb8f58016afe43d82bc087d2925dd3e747285c9d","status":"completed","call_id":"call_a377f7596a6e4b90926ab9b46694e416","name":"exec","input":"const r=await tools.exec_command({cmd:\\"XDG_CONFIG_HOME=/tmp/p2-42bb5c51/config /nix/store/76vvsfvdifhplj44d3sp6crc704wkg11-flow-workspace-0.60.1/bin/flow \'Send.{ { Mind proposalTwoReceiver Luna } Soft.Living.{ \xc2\xabProposal 2 isolated matrix\xc2\xbb \xc2\xabP2-living-before: record this statement.\xc2\xbb } }\'\\",yield_time_ms:10000});\\ntext(JSON.stringify(r));\\n","internal_chat_message_metadata_passthrough":{"turn_id":"01a1f138-d9c1-7040-93ce-9821961375b4","create_time":1795048408.1744578}}}\n',
    b'{"timestamp":"2026-11-19T00:33:30.212Z","ordinal":54,"type":"response_item","payload":{"type":"custom_tool_call_output","id":"ctco_01a1f139-0c64-7481-9911-240d9c57c964","call_id":"call_a377f7596a6e4b90926ab9b46694e416","output":[{"type":"input_text","text":"Script completed\\nWall time 0.0 seconds\\nOutput:\\n"},{"type":"input_text","text":"{\\"chunk_id\\":\\"d179e7\\",\\"wall_time_seconds\\":0.000010208,\\"exit_code\\":0,\\"original_token_count\\":8,\\"output\\":\\"SendAccepted.{ 6dis 12 Queued }\\\\n\\"}"}],"internal_chat_message_metadata_passthrough":{"turn_id":"01a1f138-d9c1-7040-93ce-9821961375b4","create_time":1795048410.2124739}},"metadata":{"client_authored":false,"fallback_token_limit_override":12000}}\n',
    b'{"timestamp":"2026-11-19T00:33:33.290Z","ordinal":58,"type":"response_item","payload":{"type":"custom_tool_call","id":"ctc_0ead0a0f6abb8f58016afe43dc5ce487d2a19f6438338f68a8","status":"completed","call_id":"call_82964a17a1c045f58eeb59076b3f95b0","name":"exec","input":"const r=await tools.send({target:{aspect:\\"Mind\\",topic:\\"proposalTwoReceiver\\",model:\\"Luna\\"},priority:\\"Soft\\",kind:\\"Result\\",requestId:\\"ay87\\",body:\\"Actions completed.\\"});\\ntext(JSON.stringify(r));\\n","internal_chat_message_metadata_passthrough":{"turn_id":"01a1f138-d9c1-7040-93ce-9821961375b4","create_time":1795048412.3649058}}}\n',
    b'{"timestamp":"2026-11-19T00:33:33.327Z","ordinal":61,"type":"response_item","payload":{"type":"custom_tool_call_output","id":"ctco_01a1f139-188f-7891-90f5-36cbd9cf06a8","call_id":"call_82964a17a1c045f58eeb59076b3f95b0","output":[{"type":"input_text","text":"Script completed\\nWall time 0.0 seconds\\nOutput:\\n"},{"type":"input_text","text":"\\"Refused.Malformed\\""}],"internal_chat_message_metadata_passthrough":{"turn_id":"01a1f138-d9c1-7040-93ce-9821961375b4","create_time":1795048413.3272636}},"metadata":{"client_authored":false,"fallback_token_limit_override":12000}}\n',
    b'{"timestamp":"2026-11-19T00:33:36.552Z","ordinal":65,"type":"response_item","payload":{"type":"custom_tool_call","id":"ctc_0ead0a0f6abb8f58016afe43e02eb487d2a73b7841a65d0a8b","status":"completed","call_id":"call_5ad52e71d0ee44fea47511b9bb7e94d2","name":"exec","input":"text(JSON.stringify(ALL_TOOLS.filter(x=>x.name===\\"send\\")));\\n","internal_chat_message_metadata_passthrough":{"turn_id":"01a1f138-d9c1-7040-93ce-9821961375b4","create_time":1795048416.1845467}}}\n',
    b'{"timestamp":"2026-11-19T00:33:36.589Z","ordinal":67,"type":"response_item","payload":{"type":"custom_tool_call_output","id":"ctco_01a1f139-254d-7111-9bd9-c5ede0e04900","call_id":"call_5ad52e71d0ee44fea47511b9bb7e94d2","output":[{"type":"input_text","text":"Script completed\\nWall time 0.0 seconds\\nOutput:\\n"},{"type":"input_text","text":"[{\\"name\\":\\"send\\",\\"description\\":\\"Send one request from this flow to the flow at a metaflow Address. Priority determines interruption and whether an asleep recipient wakes. An Order takes no answer. Result answers a Question, naming its id in request. The answer is a durable logical-delivery outcome or a typed refusal.\\\\n\\\\nexec tool declaration:\\\\n```ts\\\\ndeclare const tools: { send(args: unknown): Promise<unknown>; };\\\\n```\\"}]"}],"internal_chat_message_metadata_passthrough":{"turn_id":"01a1f138-d9c1-7040-93ce-9821961375b4","create_time":1795048416.5892587}},"metadata":{"client_authored":false,"fallback_token_limit_override":12000}}\n',
    b'{"timestamp":"2026-11-19T00:33:41.160Z","ordinal":71,"type":"response_item","payload":{"type":"custom_tool_call","id":"ctc_0ead0a0f6abb8f58016afe43e4322887d2bc094755d7664eca","status":"completed","call_id":"call_363b974e2a6a4e31b89d413dba8013f7","name":"exec","input":"const r=await tools.send({target:{aspect:\\"Mind\\",topic:\\"proposalTwoSender\\",model:\\"Luna\\"},priority:\\"Soft\\",kind:\\"Result\\",request:{id:\\"oc59\\"},body:\\"Actions completed.\\"});\\ntext(JSON.stringify(r));\\n","internal_chat_message_metadata_passthrough":{"turn_id":"01a1f138-d9c1-7040-93ce-9821961375b4","create_time":1795048420.1977987}}}\n',
    b'{"timestamp":"2026-11-19T00:33:41.185Z","ordinal":74,"type":"response_item","payload":{"type":"custom_tool_call_output","id":"ctco_01a1f139-3741-7952-88c1-98989947961f","call_id":"call_363b974e2a6a4e31b89d413dba8013f7","output":[{"type":"input_text","text":"Script completed\\nWall time 0.0 seconds\\nOutput:\\n"},{"type":"input_text","text":"\\"Refused.Malformed\\""}],"internal_chat_message_metadata_passthrough":{"turn_id":"01a1f138-d9c1-7040-93ce-9821961375b4","create_time":1795048421.1858928}},"metadata":{"client_authored":false,"fallback_token_limit_override":12000}}\n',
)


class ActualExecRowFixtures(unittest.TestCase):
    def test_actual_five_send_pairs(self):
        import json
        pairs = list(zip(ATTEMPT4_TOOL_ROWS[::2], ATTEMPT4_TOOL_ROWS[1::2]))
        wanted = [(0, 'Order', 'g9xa'), (1, 'Question', 'ay87'), (3, 'Notice', '3az9'),
                  (5, 'Result', None), (7, 'Result', None)]
        for index, kind, request_id in wanted:
            with self.subTest(index=index):
                call_id, arguments, answer, success = matrix.tool_evidence(*pairs[index], 'native')
                self.assertEqual(call_id, json.loads(pairs[index][0])['payload']['call_id'])
                self.assertEqual(arguments['kind'], kind)
                self.assertIsNone(success)  # no invented RPC success field
                if request_id:
                    import controller
                    self.assertEqual(matrix.decode_native_acceptance(answer, 'proposalTwoSender',
                                     'proposalTwoReceiver', controller.receipt_tokens), request_id)
                else:
                    self.assertEqual(answer, 'Refused.Malformed')
                    self.assertNotIsInstance(arguments.get('request'), str)

    def test_actual_two_cli_pairs(self):
        pairs = list(zip(ATTEMPT4_TOOL_ROWS[::2], ATTEMPT4_TOOL_ROWS[1::2]))
        for index, kind, request_id in [(2, 'Task', 'jhn8'), (4, 'Living', '6dis')]:
            with self.subTest(kind=kind):
                call_id, command, answer, success = matrix.tool_evidence(*pairs[index], 'cli')
                self.assertIn('Soft.' + kind + '.', command)
                expected_datom = ('Send.{ { Mind proposalTwoReceiver Luna } Soft.Task.{ 15 «P2-task-before: hold until phase A authorization.» } }' if kind == 'Task' else
                                  'Send.{ { Mind proposalTwoReceiver Luna } Soft.Living.{ «Proposal 2 isolated matrix» «P2-living-before: record this statement.» } }')
                self.assertEqual(command, matrix.private_cli({'root':'/tmp/p2-42bb5c51','providers':{'flow':{'path':'/nix/store/76vvsfvdifhplj44d3sp6crc704wkg11-flow-workspace-0.60.1/bin/flow'}}}, expected_datom))
                import controller
                self.assertEqual(matrix.parse_visible_admission(answer.strip(), controller.receipt_tokens), request_id)
                self.assertIsNone(success)

    def test_actual_catalog_call_is_not_send_evidence(self):
        with self.assertRaises(matrix.MatrixError):
            matrix.tool_evidence(ATTEMPT4_TOOL_ROWS[12], ATTEMPT4_TOOL_ROWS[13], 'native')

    def test_raw_call_id_mismatch_refused(self):
        import json
        reply = json.loads(ATTEMPT4_TOOL_ROWS[1])
        reply['payload']['call_id'] = 'another-call'
        with self.assertRaises(matrix.MatrixError):
            matrix.tool_evidence(ATTEMPT4_TOOL_ROWS[0], json.dumps(reply).encode(), 'native')

    def test_result_instruction_uses_request_string_for_every_control(self):
        from unittest import mock
        owner = mock.Mock()
        ledger = matrix.Evidence()
        captured = []
        def call(owner, label, binary, request):
            captured.append(request)
            return 'Sent.ct01'
        import controller
        matrix.control_question(owner, 'sender', 'Finish this Question.', ledger, call, controller.receipt_tokens)
        self.assertIn('captured RequestId STRING', captured[0])
        self.assertIn('"request":"abcd"', captured[0])


class ActualExecChannelFixtures(unittest.TestCase):
    setUp = ChannelFixtures.setUp
    tearDown = ChannelFixtures.tearDown
    def _pair_event(self, pair, kind, label, request_id, marker):
        import hashlib, json
        call, response = ATTEMPT4_TOOL_ROWS[2*pair:2*pair+2]
        (self.root / 'evidence/call').write_bytes(call)
        (self.root / 'evidence/response').write_bytes(response)
        return {'cut': 'admission', 'label': label, 'kind': kind, 'marker': marker,
                'request_id': request_id, 'minutes': None, 'identity': {'pane': 's'},
                'invocation': {'path': 'evidence/call', 'sha256': hashlib.sha256(call).hexdigest()},
                'receipt': {'path': 'evidence/response', 'sha256': hashlib.sha256(response).hexdigest()}}

    def test_actual_native_admissions_bind_ids_and_reject_reuse(self):
        import json, controller
        from unittest import mock
        for pair, kind, label, request_id, marker in [(0,'Order','O','g9xa','P2-order-before'),
                (1,'Question','Q','ay87','P2-question-before'),(3,'Notice','N','3az9','P2-notice-before')]:
            event = self._pair_event(pair, kind, label, request_id, marker)
            with mock.patch.object(self.channel, '_next_frame', return_value=json.dumps(event).encode()):
                self.channel.receive_admission(label, kind, marker, 1, controller.receipt_tokens)
                self.assertEqual(self.channel.requests[label], request_id)
                with self.assertRaises(matrix.MatrixError):
                    self.channel.receive_admission(label, kind, marker, 1, controller.receipt_tokens)

    def test_actual_native_receipt_rejects_wrong_request_id(self):
        import json, controller
        from unittest import mock
        event = self._pair_event(0, 'Order', 'O', 'nope', 'P2-order-before')
        with mock.patch.object(self.channel, '_next_frame', return_value=json.dumps(event).encode()):
            with self.assertRaises(matrix.MatrixError):
                self.channel.receive_admission('O', 'Order', 'P2-order-before', 1, controller.receipt_tokens)

    def test_raw_control_result_requires_string_and_matches_kept_id(self):
        import json, controller, hashlib
        from unittest import mock
        self.channel.register_control('ct01', 'receiver')
        original = json.loads(ATTEMPT4_TOOL_ROWS[0])
        reply = json.loads(ATTEMPT4_TOOL_ROWS[1])
        args = matrix.native_send('proposalTwoSender', 'Result', 'done', 'ct01')
        original['payload']['input'] = 'const r=await tools.send(' + json.dumps(args) + ');text(JSON.stringify(r));'
        reply['payload']['output'][-1]['text'] = json.dumps('Kept.{ Sender.{ Mind proposalTwoReceiver Luna } ct01 }')
        call_bytes, response_bytes = json.dumps(original).encode(), json.dumps(reply).encode()
        (self.root/'evidence/call').write_bytes(call_bytes)
        (self.root/'evidence/response').write_bytes(response_bytes)
        event = {'cut':'control-completion','request_id':'ct01','side':'receiver','identity':{'pane':'r'},
                 'invocation':{'path':'evidence/call','sha256':hashlib.sha256(call_bytes).hexdigest()},
                 'response':{'path':'evidence/response','sha256':hashlib.sha256(response_bytes).hexdigest()}}
        with mock.patch.object(self.channel,'_next_frame',return_value=json.dumps(event).encode()):
            self.channel.receive_control_completion('ct01','receiver',1,controller.receipt_tokens)

    def test_raw_reply_outcomes_preserve_typed_semantics(self):
        import json, controller, hashlib
        from unittest import mock
        for index, (expected, text) in enumerate([
                ('unresolved', 'Refused.Unresolved'),
                ('accepted', 'Accepted.{ Sender.{ Mind proposalTwoReceiver Luna } { Mind proposalTwoSender Luna } { rq01 12 Delivered } }'),
                ('kept', 'Kept.{ Sender.{ Mind proposalTwoReceiver Luna } rq01 }')]):
            with self.subTest(expected=expected):
                call = json.loads(ATTEMPT4_TOOL_ROWS[0])
                reply = json.loads(ATTEMPT4_TOOL_ROWS[1])
                call_id = 'raw-outcome-' + str(index)
                call['payload']['call_id'] = reply['payload']['call_id'] = call_id
                args = matrix.native_send('proposalTwoSender', 'Result', 'answer', 'rq01')
                call['payload']['input'] = 'const r=await tools.send(' + json.dumps(args) + ');text(JSON.stringify(r));'
                reply['payload']['output'][-1]['text'] = json.dumps(text)
                call_bytes, response_bytes = json.dumps(call).encode(), json.dumps(reply).encode()
                (self.root/'evidence/call').write_bytes(call_bytes)
                (self.root/'evidence/response').write_bytes(response_bytes)
                event = {'cut':'reply-outcome','label':expected,'surface':'native','identity':{'pane':'r'},
                         'invocation':{'path':'evidence/call','sha256':hashlib.sha256(call_bytes).hexdigest()},
                         'response':{'path':'evidence/response','sha256':hashlib.sha256(response_bytes).hexdigest()}}
                with mock.patch.object(self.channel,'_next_frame',return_value=json.dumps(event).encode()):
                    self.assertEqual(self.channel.receive_reply_outcome(expected,'native',args,expected,1,
                                     controller.receipt_tokens,'rq01' if expected=='accepted' else None),text)

    def test_actual_malformed_result_arguments_cannot_close_control(self):
        import json, controller, hashlib
        from unittest import mock
        for pair, request_id in [(5,'ay87'),(7,'oc59')]:
            with self.subTest(pair=pair):
                self.channel.controls[request_id] = 'sender'
                call, response = ATTEMPT4_TOOL_ROWS[2*pair:2*pair+2]
                (self.root/'evidence/call').write_bytes(call)
                (self.root/'evidence/response').write_bytes(response)
                event = {'cut':'control-completion','request_id':request_id,'side':'sender','identity':{'pane':'s'},
                         'invocation':{'path':'evidence/call','sha256':hashlib.sha256(call).hexdigest()},
                         'response':{'path':'evidence/response','sha256':hashlib.sha256(response).hexdigest()}}
                with mock.patch.object(self.channel,'_next_frame',return_value=json.dumps(event).encode()):
                    with self.assertRaises(matrix.MatrixError):
                        self.channel.receive_control_completion(request_id,'sender',1,controller.receipt_tokens)
