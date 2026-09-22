import contextlib
import hashlib
import importlib.machinery
import importlib.util
import io
import json
import pathlib
import sys
import tempfile
import unittest


def load_module():
    loader = importlib.machinery.SourceFileLoader("reap_flow", "tools/reap-flow")
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class ReapFlowFailClosedTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        self.flows = self.root / "flows"
        self.registry = self.root / "registry"
        self.flows.mkdir()
        self.registry.mkdir()
        self.module.ROOT = self.root
        self.module.FLOWS = self.flows
        self.module.ARCHIVE = self.root / "archive"
        self.module.HM_REGISTRY = self.registry

    def tearDown(self):
        self.temp.cleanup()

    def marker(self, flow="obsolete"):
        lane = self.flows / flow
        lane.mkdir()
        evidence = lane / "retirement.md"
        evidence.write_text("exact retirement evidence\n")
        marker = self.registry / "retired" / f"{flow}.json"
        marker.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "session": "messaging-build", "name": "old-agent",
            "pane_id": "wZ:p1", "terminal_id": "term-old", "agent": "codex",
        }
        marker.write_text(json.dumps({
            "version": 1, "state": "retired", "flow": flow,
            "record": record, "native_thread": "11111111-2222-3333-4444-555555555555",
            "evidence": {"path": str(evidence), "sha256": hashlib.sha256(evidence.read_bytes()).hexdigest()},
        }))
        return lane, marker

    def test_apply_blocks_when_roster_is_unavailable_before_examine_or_archive(self):
        (self.flows / "obsolete").mkdir()
        self.module.live_flow_ids = lambda: None
        self.module.examine = lambda flow: self.fail("examine must not run")
        old = sys.argv
        sys.argv = ["reap-flow", "--flow", "obsolete", "--apply"]
        try:
            with self.assertRaisesRegex(SystemExit, "roster"):
                self.module.main()
        finally:
            sys.argv = old

    def test_archive_requires_retirement_marker_and_no_active_registration(self):
        lane, _ = self.marker()
        finding = {"lane": lane, "files": []}
        gate = self.module.retirement_gate("obsolete", set(), [], self.registry)
        self.assertTrue(gate["eligible"], gate)
        active = self.registry / "obsolete.json"
        active.write_text(json.dumps({"native_thread": "11111111-2222-3333-4444-555555555555"}))
        blocked = self.module.retirement_gate("obsolete", set(), [], self.registry)
        self.assertFalse(blocked["eligible"])
        self.assertIn("active-registration", blocked["reasons"])
        with self.assertRaisesRegex(SystemExit, "active-registration"):
            self.module.archive("obsolete", finding, True, blocked)

    def test_malformed_marker_and_changed_evidence_block_archive(self):
        lane, marker = self.marker()
        marker.write_text("{not-json")
        blocked = self.module.retirement_gate("obsolete", set(), [], self.registry)
        self.assertEqual(blocked["reasons"], ["invalid-retirement-marker"])
        _, marker = self.marker("changed")
        evidence = self.flows / "changed" / "retirement.md"
        evidence.write_text("changed after marker\n")
        blocked = self.module.retirement_gate("changed", set(), [], self.registry)
        self.assertEqual(blocked["reasons"], ["invalid-retirement-marker"])
        with self.assertRaisesRegex(SystemExit, "invalid-retirement-marker"):
            self.module.archive("changed", {"lane": self.flows / "changed", "files": []}, True, blocked)

    def test_live_target_blocks_even_with_valid_marker(self):
        lane, _ = self.marker()
        blocked = self.module.retirement_gate("obsolete", {"obsolete"}, [], self.registry)
        self.assertFalse(blocked["eligible"])
        self.assertIn("live-target", blocked["reasons"])

    def test_valid_marker_path_allows_archive_stage_only(self):
        lane, _ = self.marker("eligible")
        gate = self.module.retirement_gate("eligible", set(), [], self.registry)
        self.assertTrue(gate["eligible"], gate)
        calls = []
        self.module.shutil.move = lambda *args: calls.append(args)
        result = self.module.archive("eligible", {"lane": lane, "files": []}, True, gate)
        self.assertTrue(result["applied"])
        self.assertEqual(len(calls), 1)

    def test_discovery_does_not_emit_unknown_or_retained_nonlive_lanes(self):
        (self.flows / "retained").mkdir()
        (self.flows / "unknown").mkdir()
        self.module.live_flow_ids = lambda: set()
        self.module.held_locks = lambda flow: []
        old = sys.argv
        sys.argv = ["reap-flow", "--list-candidates"]
        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                self.assertEqual(self.module.main(), 0)
        finally:
            sys.argv = old
        self.assertEqual(output.getvalue(), "")

    def test_discovery_emits_only_marker_bound_route_free_candidate(self):
        self.marker("eligible")
        self.module.live_flow_ids = lambda: set()
        self.module.held_locks = lambda flow: []
        old = sys.argv
        sys.argv = ["reap-flow", "--list-candidates"]
        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                self.assertEqual(self.module.main(), 0)
        finally:
            sys.argv = old
        self.assertEqual(output.getvalue(), "eligible\n")


if __name__ == "__main__":
    unittest.main()
