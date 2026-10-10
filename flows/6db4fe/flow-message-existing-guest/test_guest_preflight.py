import importlib.util
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("guest_preflight", HERE / "guest_preflight.py")
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class Result:
    def __init__(self, code=0, output=""):
        self.returncode = code
        self.stdout = output


class PreflightTests(unittest.TestCase):
    def test_wrong_host_refuses_before_unit_or_image_read(self):
        calls = []

        def fake_remote(argv):
            calls.append(argv)
            return Result(0, "ouranos\n")

        with self.assertRaises(module.GuardError):
            module.guarded_snapshot(fake_remote)
        self.assertEqual(calls, [("hostname", "--short")])

    def test_unreachable_host_refuses_before_unit_or_image_read(self):
        calls = []

        def fake_remote(argv):
            calls.append(argv)
            return Result(255, "")

        with self.assertRaises(module.GuardError):
            module.guarded_snapshot(fake_remote)
        self.assertEqual(calls, [("hostname", "--short")])

    def test_exact_host_allows_only_declared_state_reads(self):
        calls = []

        def fake_remote(argv):
            calls.append(argv)
            if argv == ("hostname", "--short"):
                return Result(0, "prometheus\n")
            if argv[0] == "test":
                return Result(1, "")
            return Result(0, "observed\n")

        snapshot = module.guarded_snapshot(fake_remote)
        self.assertEqual(snapshot["host"], "prometheus")
        self.assertFalse(snapshot["runner"])
        self.assertEqual(len(calls), 7)
        self.assertEqual(calls[0], ("hostname", "--short"))
        self.assertTrue(all("vm-testing" in " ".join(call) for call in calls[1:]))

    def test_manifest_unset_graph_is_blocked_and_wrong_guest_rejected(self):
        data = module.load_manifest(HERE / "manifest.example.json")
        self.assertEqual(len(module.blocked_reasons(data)), 9)
        data["guest_unit"] = "microvm@other.service"
        with TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.json"
            path.write_text(json.dumps(data))
            with self.assertRaises(module.GuardError):
                module.load_manifest(path)

    def test_exact_remote_transport_has_host_key_and_no_forwarding(self):
        self.assertIn("StrictHostKeyChecking=yes", module.SSH)
        self.assertIn("ForwardAgent=no", module.SSH)
        self.assertIn("ClearAllForwardings=yes", module.SSH)
        self.assertEqual(module.SSH[-1], "root@prometheus.goldragon.criome")


if __name__ == "__main__":
    unittest.main()
