"""Unrun synthetic fixtures: no systemd, native or production invocation."""
import tempfile
import unittest
from pathlib import Path
from unittest import mock
import orchestration as o


class CustodyFixtures(unittest.TestCase):
    def test_identity_rejects_wrong_id_or_group(self):
        value = dict(Id='a', InvocationID='b', ControlGroup='/user.slice/a', MainPID='3',
                     ExecMainStartTimestampMonotonic='4', ExecStart='x')
        for key in ('Id', 'ControlGroup'):
            changed = dict(value, **{key: 'other'})
            with self.subTest(key=key), self.assertRaises(o.CustodyError):
                o.compare_unit(value, changed)

    def test_changed_cgroup_inode_refuses_empty_claim(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)
            (path / 'cgroup.events').write_text('populated 0\n')
            saved = {'unit': {'ControlGroup': '/user.slice/test'}, 'cgroup': {'device': -1, 'inode': -1}}
            with mock.patch.object(o, 'cgroup_path', return_value=path):
                with self.assertRaises(o.CustodyError):
                    o.cgroup_empty(saved)

    def test_changed_production_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            evidence = Path(d) / 'evidence'
            evidence.mkdir()
            for part in ('configuration.datom', 'fable-current.datom', 'services', 'clients'):
                (evidence / ('production-before.' + part)).write_text('same')
                (evidence / ('production-after.' + part)).write_text('same')
            (evidence / 'production-after.clients').write_text('changed')
            with self.assertRaises(o.CustodyError):
                o.production_compare(d)

    def test_handshake_rejects_bad_envelope(self):
        with mock.patch.object(o.selectors, 'DefaultSelector') as factory, \
             mock.patch.object(o.os, 'read', return_value=b'{}\n{}\n'):
            factory.return_value.select.return_value = [object()]
            with self.assertRaises(o.CustodyError):
                o.read_fifo(1, o.time.monotonic() + 1)

    def test_parse_show_duplicate_refused(self):
        with self.assertRaises(o.CustodyError):
            o.parse_show(b'Id=x\nId=y\n')


if __name__ == '__main__':
    unittest.main()
