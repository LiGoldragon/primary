"""Unrun synthetic bootstrap fixtures; no daemons or credentials involved."""
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import bootstrap


class BootstrapTests(unittest.TestCase):
    def test_cgroup_must_be_owned(self):
        with mock.patch('builtins.open', mock.mock_open(read_data='0::/user.slice/user-1.slice/owned\n')):
            bootstrap.check_membership('/user.slice/user-1.slice/owned')
            with self.assertRaises(bootstrap.BootstrapError):
                bootstrap.check_membership('/user.slice/user-1.slice/other')

    def test_owner_is_required_before_child_or_stage(self):
        instance = bootstrap.Bootstrap({}, {})
        with self.assertRaises(bootstrap.BootstrapError):
            instance.command('example', ['/not-executed'])
        with self.assertRaises(bootstrap.BootstrapError):
            instance.stage()

    def test_inputs_reject_missing_provider_set(self):
        with self.assertRaises(bootstrap.BootstrapError):
            bootstrap.verify_inputs({'providers': {}})

    def test_exclusive_write_refuses_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'file'
            bootstrap._write(path, 'first')
            with self.assertRaises(FileExistsError):
                bootstrap._write(path, 'second')
            self.assertEqual(path.read_text(), 'first')

    def test_wrong_context_refused_before_child(self):
        instance = bootstrap.Bootstrap({'contexts': {}}, {})
        with mock.patch.object(instance, '_require_owner'), mock.patch.object(instance, 'command') as command:
            with self.assertRaises(bootstrap.BootstrapError):
                instance.archive_context('mind-belief', '/repo', '0' * 40)
            command.assert_not_called()


if __name__ == '__main__':
    unittest.main()
