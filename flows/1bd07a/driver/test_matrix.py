"""Unrun pure fixtures; no native launches, tools, services or observers."""
import unittest
import matrix


class MatrixFixtures(unittest.TestCase):
    def test_request_ids_are_dynamic_unique_and_kind_bound(self):
        evidence = matrix.Evidence()
        evidence.request('Q2', 'actual-q', 'Question')
        with self.assertRaises(matrix.MatrixError): evidence.request('T2', 'actual-q', 'Task', 123)
        with self.assertRaises(matrix.MatrixError): evidence.request('O2', 'actual-o', 'Question')

    def test_carry_and_order_exclusion(self):
        evidence = matrix.Evidence()
        evidence.request('O2', 'o_actual', 'Order')
        evidence.request('Q2', 'q_actual', 'Question')
        evidence.request('T2', 't_actual', 'Task', 12345)
        evidence.successor('q_actual t_actual 12345', 'old', 'new', 12345)
        evidence.refreshes = 0
        with self.assertRaises(matrix.MatrixError):
            evidence.successor('q_actual t_actual 12345 P2-order-carry-excluded-7a97', 'old', 'new', 12345)
        evidence.refreshes = 0
        with self.assertRaises(matrix.MatrixError):
            evidence.successor('q_actual t_actual 99999', 'old', 'new', 99999)

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
        self.channel.directory = self.root / 'evidence'
        self.channel.expected = []
        self.channel.requests = {}
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

    def test_missing_transcript_and_invented_id_refused(self):
        import hashlib, json
        from unittest import mock
        receipt = {'success': True, 'contentItems': [{'type': 'inputText', 'text': 'Accepted.{ real-id }'}]}
        data = json.dumps(receipt).encode()
        (self.root / 'evidence' / 'receipt').write_bytes(data)
        self.channel.register_control('control1', 'sender')
        self.channel.expect('cut-a', 'O', 'sender', 'Order', 'marker', 'control1')
        event = {'cut':'cut-a','label':'O','side':'sender','kind':'Order','marker':'marker',
                 'control_id':'control1','request_id':'invented','deadline':None,
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
                 'control_id':'control1','request_id':'invented','deadline':None,
                 'receipt':{'path':'evidence/receipt','sha256':hashlib.sha256(receipt).hexdigest()},
                 'transcript':{'path':'transcripts/reply','sha256':hashlib.sha256(transcript).hexdigest()},
                 'acknowledgement':'ack marker invented','identity':{'pane':'s'},
                 'reader_side':'receiver','reader_identity':{'pane':'r'}}
        with mock.patch.object(self.channel, '_next_frame', return_value=json.dumps(event).encode()):
            with self.assertRaises(matrix.MatrixError):
                self.channel.receive(1)


class LaunchFixtures(unittest.TestCase):
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
