"""Source-only unit fixtures. No runtime or native actions are exercised."""
import os
import pathlib
import tempfile
import unittest
from unittest import mock

import controller


class ReceiptTests(unittest.TestCase):
    def test_complete_matching_receipt(self):
        controller.receipt('Configured.{ «a\\»b» [ x ] }',
                           'Configured.{ «a\\»b» [ x ] }')

    def test_unmatched_guillemets_are_rejected(self):
        for text in ('Unconfigured »', 'Unconfigured «', '«bad « nested»', '«bad\\q»'):
            with self.subTest(text=text), self.assertRaises(controller.AdmissionError):
                controller.receipt(text, 'Unconfigured')

    def test_quoted_and_atom_are_distinct(self):
        with self.assertRaises(controller.AdmissionError):
            controller.receipt('«Unconfigured»', 'Unconfigured')

    def test_expected_strings_use_pinned_canonical_bare_rule(self):
        controller.receipt('Compiled./tmp/place.signal', 'Compiled.«/tmp/place.signal»')
        controller.receipt('Configured.Nexus.{ /tmp/root ! }', 'Configured.Nexus.{ «/tmp/root» «!» }')
        controller.receipt('Configured.HarnessHook./nix/store/hook', 'Configured.HarnessHook.«/nix/store/hook»')
        controller.receipt('Answered.{ P2-kept-answer }', 'Answered.{ «P2-kept-answer» }')
        controller.receipt('Compiled.«/tmp/path with space»', 'Compiled.«/tmp/path with space»')
        with self.assertRaises(controller.AdmissionError):
            controller.receipt('Configured.Nexus.{ /tmp/other ! }', 'Configured.Nexus.{ «/tmp/root» «!» }')


class CustodyTests(unittest.TestCase):
    def setUp(self):
        self.identity = dict(Id='proposal2-test.service', InvocationID='abc',
                             ControlGroup='/user.slice/user-1.slice/test', MainPID='123',
                             ExecMainStartTimestampMonotonic='456', ExecStart='driver')

    def test_stop_is_bound_to_saved_unit_and_absolute_provider(self):
        command = controller.unit_stop_command(self.identity, self.identity,
                                               'proposal2-test.service', '/nix/store/x/systemctl')
        self.assertEqual(command[0], '/nix/store/x/systemctl')
        with self.assertRaises(controller.AdmissionError):
            controller.unit_stop_command(self.identity, self.identity,
                                         'proposal2-other.service', '/nix/store/x/systemctl')
        with self.assertRaises(controller.AdmissionError):
            controller.unit_stop_command(self.identity, self.identity,
                                         'proposal2-test.service', 'systemctl')

    def test_unit_mismatch_and_unproved_cgroup_rejected(self):
        changed = dict(self.identity, InvocationID='different')
        with self.assertRaises(controller.AdmissionError):
            controller.unit_guard(self.identity, changed)
        with self.assertRaises(controller.AdmissionError):
            controller.cgroup_guard('same', 'same')

    def test_auth_symlink_is_not_regular_file(self):
        with tempfile.TemporaryDirectory() as directory:
            target = pathlib.Path(directory, 'target')
            target.write_text('fixture')
            indirect = pathlib.Path(directory, 'indirect')
            indirect.symlink_to(target)
            with self.assertRaises(controller.AdmissionError):
                controller.metadata_record(indirect, pathlib.Path(directory, 'auth'))

    def test_prompt_inserts_captured_identifier(self):
        prompts = controller.render_prompts('/private', '/package', 'ab12')
        self.assertIn('Done.{ ab12 ', prompts[2])
        self.assertNotIn('<captured-T>', prompts[2])
        with self.assertRaises(controller.AdmissionError):
            controller.render_prompts('/private', '/package', 'x } injected')



if __name__ == '__main__':
    unittest.main()
