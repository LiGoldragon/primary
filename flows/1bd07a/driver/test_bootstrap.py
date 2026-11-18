"""Unrun synthetic bootstrap fixtures; no daemons or credentials involved."""
import tempfile
import shutil
import subprocess
import unittest
from pathlib import Path
from unittest import mock

import bootstrap


class BootstrapTests(unittest.TestCase):
    def archive_fixture(self, directory, *, bad_revision=False, bad_extractor=False):
        root = Path(directory)
        repository = root / 'repository'
        repository.mkdir()
        git = shutil.which('git')
        subprocess.run([git, 'init', '-q', str(repository)], check=True)
        (repository / 'fixture').write_text('archive content\n')
        subprocess.run([git, '-C', str(repository), 'add', 'fixture'], check=True)
        subprocess.run([git, '-C', str(repository), '-c', 'user.name=Fixture',
                        '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'fixture'], check=True)
        revision = subprocess.check_output([git, '-C', str(repository), 'rev-parse', 'HEAD'], text=True).strip()
        if bad_revision:
            revision = '0' * 40
        (root / 'contexts').mkdir()
        manifest = {'root': str(root), 'contexts': {'mind-belief': {
            'repository': str(repository), 'revision': revision}}, 'providers': {
                'git': {'path': git}, 'tar': {'path': shutil.which('false') if bad_extractor else shutil.which('tar')}}}
        instance = bootstrap.Bootstrap(manifest, {})
        def command(name, argv, **kwargs):
            process = subprocess.Popen(argv, stderr=subprocess.DEVNULL, **kwargs)
            instance.children.append(process)
            return process
        with mock.patch.object(instance, '_require_owner'), mock.patch.object(instance, 'command', side_effect=command):
            if bad_revision or bad_extractor:
                with self.assertRaises(bootstrap.BootstrapError):
                    instance.archive_context('mind-belief', str(repository), revision)
            else:
                instance.archive_context('mind-belief', str(repository), revision)
                self.assertEqual((root / 'contexts/mind-belief/fixture').read_text(), 'archive content\n')
        self.assertEqual(len(instance.children), 2)
        self.assertTrue(all(child.returncode is not None for child in instance.children))
        self.assertTrue(instance.children[0].stdout.closed)
        if bad_revision:
            self.assertNotEqual(instance.children[0].returncode, 0)
        elif bad_extractor:
            self.assertNotEqual(instance.children[1].returncode, 0)
        else:
            self.assertEqual([child.returncode for child in instance.children], [0, 0])

    def test_real_archive_closed_pipe_reaps_both_children(self):
        with tempfile.TemporaryDirectory() as directory:
            self.archive_fixture(directory)

    def test_failed_archive_reaps_both_children(self):
        with tempfile.TemporaryDirectory() as directory:
            self.archive_fixture(directory, bad_revision=True)

    def test_failed_extractor_reaps_both_children(self):
        with tempfile.TemporaryDirectory() as directory:
            self.archive_fixture(directory, bad_extractor=True)

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
