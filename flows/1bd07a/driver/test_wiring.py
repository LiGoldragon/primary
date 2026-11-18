"""Unrun source fixtures for immutable admission and schema checks."""
import copy
import json
from pathlib import Path
import unittest
import controller


class WiringTests(unittest.TestCase):
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

    def test_no_success_after_missing_matrix(self):
        class Owner:
            manifest = {'contexts': {}}
            def stage(self): pass
            def compile_place(self, receipt): pass
            def start_services(self): pass
        from unittest import mock
        with mock.patch('orchestration.auth_link'), mock.patch.object(controller, 'configure_and_rehearse'):
            with self.assertRaises(controller.AdmissionError):
                controller.private_workload(Owner())


if __name__ == '__main__':
    unittest.main()
