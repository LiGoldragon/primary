"""Unrun source fixtures for immutable admission and schema checks."""
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest
import controller


class WiringTests(unittest.TestCase):
    def test_isolated_main_registers_controller_without_import_path_changes(self):
        script = r"""
import pathlib, sys, types
path = pathlib.Path(sys.argv[1])
module = types.ModuleType('__main__')
module.__file__ = str(path)
sys.modules['__main__'] = module
source = path.read_text().split("if __name__ == '__main__':")[0]
exec(compile(source, str(path), 'exec'), module.__dict__)
module.validate = lambda value: {'artifacts': {name: {'path': name} for name in ('bootstrap', 'orchestration', 'matrix')}}
module.verify_admission = lambda value: None
module.verify_artifacts = lambda value: {
    'bootstrap': b'', 'matrix': b'',
    'orchestration': b'from controller import protected_configuration\ndef operator(*args):\n    assert protected_configuration.__module__ == "__main__"\n'}
assert module.main(['controller.py', 'run', sys.argv[2]]) == 0
print('isolated loader PASS')
"""
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / 'manifest.json'
            manifest.write_text('{}')
            result = subprocess.run([sys.executable, '-I', '-B', '-c', script,
                                     str(Path(controller.__file__).resolve()), str(manifest)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('isolated loader PASS', result.stdout)

    def test_initial_turn_ends_require_both_exact_flow_ids(self):
        from unittest import mock
        import matrix
        stream = mock.Mock()
        stream.next_line.side_effect = [
            'TurnEnded.{ { Mind proposalTwoSender Luna } Codex s1 100 }',
            'TurnEnded.{ { Mind proposalTwoReceiver Luna } Codex r1 101 }']
        matrix.await_initial_turns(stream, {'sender': {'flow_id': 's1'}, 'receiver': {'flow_id': 'r1'}}, 1, controller.receipt_tokens)
        self.assertEqual(stream.next_line.call_count, 2)

    def test_matrix_fake_full_lifecycle_order(self):
        from unittest import mock
        import matrix
        owner = mock.Mock(manifest={'root': '/fixture', 'control_timeout_seconds': 1})
        channel = mock.Mock()
        channel.identity = {}
        channel.close_attempts = set()
        initial = {'sender': {'flow_id': 's1'}, 'receiver': {'flow_id': 'r1'}}
        successor = {'flow_id': 'r2'}
        order = []
        names = ('observe_before_launch', 'launch_once', 'verify_bound_inspect', 'snapshot_native',
                 'await_initial_turns', 'collect_phase_a_admissions', 'collect_phase_a_consumption',
                 'collect_phase_a_reply_outcomes', 'kept_answer_case', 'collect_phase_b_admissions',
                 'collect_phase_b_consumption', 'refresh_successor', 'complete_successor_carry', 'close_synthetic_flows')
        with mock.patch.multiple(matrix, **{name: mock.DEFAULT for name in names}) as parts, \
             mock.patch('bootstrap._write'):
            for name, part in parts.items():
                part.side_effect = lambda *a, _name=name, **k: order.append(_name)
            parts['observe_before_launch'].side_effect = lambda *a: (mock.Mock(), mock.Mock())
            parts['launch_once'].side_effect = lambda owner, side, *a: initial[side]
            def admissions(name, label):
                def record(*args):
                    order.append(name)
                    args[2].task_cutoffs[label] = float('inf')
                return record
            parts['collect_phase_a_admissions'].side_effect = admissions('collect_phase_a_admissions', 'T')
            parts['collect_phase_b_admissions'].side_effect = admissions('collect_phase_b_admissions', 'T2')
            parts['collect_phase_a_consumption'].side_effect = lambda *a: (order.append('collect_phase_a_consumption') or ('control', 'unknown'))
            def refresh(*args):
                order.append('refresh_successor')
                channel.identity['receiver'] = successor
                return successor
            parts['refresh_successor'].side_effect = refresh
            matrix.run_matrix(owner, channel, float('inf'), lambda *a: 'Inspected.fixture', object(), object())
        self.assertEqual(order, ['verify_bound_inspect', 'snapshot_native', 'verify_bound_inspect', 'snapshot_native',
                                'await_initial_turns', 'collect_phase_a_admissions', 'collect_phase_a_consumption',
                                'collect_phase_a_reply_outcomes', 'kept_answer_case', 'collect_phase_b_admissions',
                                'collect_phase_b_consumption', 'refresh_successor', 'complete_successor_carry', 'close_synthetic_flows'])

    def test_matrix_failure_attempts_confirmed_flow_cleanup(self):
        from unittest import mock
        import matrix
        owner = mock.Mock(manifest={'root': '/fixture', 'control_timeout_seconds': 1})
        channel = mock.Mock()
        channel.identity = {}
        channel.close_attempts = set()
        streams = (mock.Mock(), mock.Mock())
        with mock.patch.object(matrix, 'observe_before_launch', return_value=streams), \
             mock.patch.object(matrix, 'launch_once', side_effect=[{'flow_id': 's1'}, matrix.MatrixError('refused')]), \
             mock.patch.object(matrix, 'verify_bound_inspect'), mock.patch.object(matrix, 'snapshot_native'), \
             mock.patch.object(matrix, 'close_bound_flow_and_pane') as close, mock.patch('bootstrap._write'):
            with self.assertRaises(matrix.MatrixError):
                matrix.run_matrix(owner, channel, float('inf'), lambda *a: 'Inspected.fixture', object(), object())
        self.assertEqual(close.call_args.args[1], 'sender')
        self.assertEqual(channel.close_attempts, {'sender'})
        for stream in streams:
            stream.close_observer.assert_called_once()

    def test_template_fails_closed(self):
        template = json.loads((Path(__file__).parent / 'provider-manifest.template.json').read_text())
        with self.assertRaises(controller.AdmissionError):
            controller.validate(template)

    def test_manifest_hash_binds_root_and_providers_but_not_review_pointer(self):
        m = {'root': '/one', 'providers': {'flow': 'sha'}, 'admission': {'sha256': 'a'}}
        original = controller.canonical_manifest_hash(m)
        changed = copy.deepcopy(m)
        changed['admission']['sha256'] = 'b'
        self.assertEqual(original, controller.canonical_manifest_hash(changed))
        changed['root'] = '/two'
        self.assertNotEqual(original, controller.canonical_manifest_hash(changed))

    def test_wrong_commit_and_extra_field_rejected(self):
        template = json.loads((Path(__file__).parent / 'provider-manifest.template.json').read_text())
        template['unexpected'] = True
        with self.assertRaises(controller.AdmissionError):
            controller.validate(template)

    def test_workload_wires_review_matrix_and_channel_close(self):
        class Owner:
            manifest = {'contexts': {}, 'root': '/fixture', 'providers': {}, 'control_timeout_seconds': 1}
            def stage(self): pass
            def compile_place(self, receipt): pass
            def start_services(self): pass
            def bind_service_endpoint(self, name, provider, endpoint): pass
        from unittest import mock
        with mock.patch('orchestration.auth_link'), mock.patch('matrix.EvidenceChannel') as channel, \
             mock.patch('matrix.run_matrix') as run, \
             mock.patch.object(controller, 'configure_and_rehearse', return_value={'sender': 'a'*64, 'receiver': 'b'*64}):
            controller.private_workload(Owner(), -1, 'fixture-nonce', 100)
            channel.return_value.review_rehearsals.assert_called_once()
            run.assert_called_once()
            channel.return_value.close.assert_called_once()

    def test_review_failure_prevents_matrix_and_closes_channel(self):
        class Owner:
            manifest = {'contexts': {}, 'root': '/fixture', 'providers': {}, 'control_timeout_seconds': 1}
            def stage(self): pass
            def compile_place(self, receipt): pass
            def start_services(self): pass
            def bind_service_endpoint(self, name, provider, endpoint): pass
        from unittest import mock
        with mock.patch('orchestration.auth_link'), mock.patch('matrix.EvidenceChannel') as channel, \
             mock.patch('matrix.run_matrix') as run, mock.patch.object(controller, 'configure_and_rehearse', return_value={}):
            channel.return_value.review_rehearsals.side_effect = ValueError('refused')
            with self.assertRaises(ValueError):
                controller.private_workload(Owner(), -1, 'fixture-nonce', 100)
            run.assert_not_called()
            channel.return_value.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
