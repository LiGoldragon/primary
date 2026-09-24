#!/usr/bin/env python3
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import threading
import unittest

TOOL = Path("tools/herdr-prompt-file").resolve()


class FakeHerdr:
    def __init__(self, root, response=None):
        self.path = str(Path(root) / "herdr.sock")
        self.response = response
        self.request = None
        self.ready = threading.Event()
        self.thread = threading.Thread(target=self.serve, daemon=True)

    def serve(self):
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
            server.bind(self.path)
            server.listen(1)
            self.ready.set()
            peer, _ = server.accept()
            with peer:
                wire = b""
                while not wire.endswith(b"\n"):
                    wire += peer.recv(65536)
                self.request = json.loads(wire.decode("utf-8"))
                if self.response is not None:
                    peer.sendall(json.dumps(self.response, ensure_ascii=False).encode("utf-8") + b"\n")

    def start(self):
        self.thread.start()
        self.assert_ready()

    def assert_ready(self):
        if not self.ready.wait(2):
            raise AssertionError("fake Unix server did not start")

    def join(self):
        self.thread.join(2)


class HerdrPromptFileTests(unittest.TestCase):
    def run_tool(self, *args):
        return subprocess.run([str(TOOL), *args], text=True, capture_output=True, timeout=5)

    def test_submits_exact_utf8_file_without_argv_prompt(self):
        with tempfile.TemporaryDirectory() as root:
            prompt = Path(root) / "prompt.txt"
            data = "hello 🌱\r\nsecond line".encode("utf-8")
            prompt.write_bytes(data)
            fake = FakeHerdr(root, {"id": "x", "result": {"agent": "target"}})
            fake.start()
            result = self.run_tool("target", str(prompt), "--socket", fake.path)
            fake.join()
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(fake.request["method"], "agent.prompt")
            self.assertEqual(fake.request["params"]["target"], "target")
            self.assertEqual(fake.request["params"]["text"].encode("utf-8"), data)
            receipt = json.loads(result.stdout)
            self.assertEqual(receipt["grade"], "submitted")
            self.assertEqual(receipt["prompt_bytes"], len(data))
            self.assertNotIn("hello", result.stdout)

    def test_wait_timeout_is_forwarded(self):
        with tempfile.TemporaryDirectory() as root:
            prompt = Path(root) / "prompt.txt"
            prompt.write_text("wait", encoding="utf-8")
            fake = FakeHerdr(root, {"id": "x", "result": {}})
            fake.start()
            result = self.run_tool("pane", str(prompt), "--socket", fake.path, "--wait-timeout-ms", "17")
            fake.join()
            self.assertEqual(result.returncode, 0)
            self.assertEqual(fake.request["params"]["wait"], {"until": ["idle", "done"], "timeout_ms": 17})
            self.assertEqual(json.loads(result.stdout)["grade"], "wait_observed")

    def test_invalid_utf8_is_rejected_before_connecting(self):
        with tempfile.TemporaryDirectory() as root:
            prompt = Path(root) / "invalid.txt"
            prompt.write_bytes(b"\xff")
            result = self.run_tool("target", str(prompt), "--socket", str(Path(root) / "absent.sock"))
            self.assertEqual(result.returncode, 2)
            receipt = json.loads(result.stdout)
            self.assertEqual(receipt["grade"], "not_submitted")
            self.assertEqual(receipt["request_bytes"], 0)

    def test_missing_response_after_write_is_uncertain_and_single_attempt(self):
        with tempfile.TemporaryDirectory() as root:
            prompt = Path(root) / "prompt.txt"
            prompt.write_text("one attempt", encoding="utf-8")
            fake = FakeHerdr(root)
            fake.start()
            result = self.run_tool("target", str(prompt), "--socket", fake.path)
            fake.join()
            self.assertEqual(result.returncode, 3)
            self.assertEqual(json.loads(result.stdout)["grade"], "uncertain")
            self.assertEqual(fake.request["params"]["text"], "one attempt")


if __name__ == "__main__":
    unittest.main()
