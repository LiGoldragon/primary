from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

from formats import read_rollout


ROOT = Path(__file__).parent


class ExtractorTest(unittest.TestCase):
    def test_codex_provenance_and_mandatory_psyche(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "rollout-12345678-1234-1234-1234-123456789abc.jsonl"
            rows = [
                {"timestamp": "t0", "type": "session_meta", "payload": {"session_id": "12345678-1234-1234-1234-123456789abc"}},
                {"timestamp": "t1", "type": "response_item", "payload": {"type": "message", "role": "user", "content": [{"type": "input_text", "text": "psyche words"}]}},
            ]
            path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
            rollout = read_rollout(path)
            self.assertEqual(rollout.session_id, "12345678-1234-1234-1234-123456789abc")
            self.assertEqual(rollout.blocks[0].text, "psyche words")
            self.assertTrue(rollout.blocks[0].mandatory)
            self.assertEqual(rollout.blocks[0].line, 2)
            self.assertGreater(rollout.blocks[0].byte_end, rollout.blocks[0].byte_start)

    def test_claude_send_message_is_mandatory_communication(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa.jsonl"
            row = {
                "type": "assistant", "timestamp": "t1",
                "message": {"role": "assistant", "content": [{
                    "type": "tool_use", "name": "SendMessage", "input": {"recipient": "peer", "content": "result"}
                }]},
            }
            path.write_text(json.dumps(row) + "\n", encoding="utf-8")
            block = read_rollout(path).blocks[0]
            self.assertEqual(block.kind, "communication")
            self.assertTrue(block.mandatory)

    def test_archive_fails_closed_without_matching_extract(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base / "source.jsonl"
            extract = base / "extract.md"
            source.write_text("source", encoding="utf-8")
            os.utime(source, (time.time() - 172800, time.time() - 172800))
            extract.write_text("wrong digest", encoding="utf-8")
            run = subprocess.run([
                "python3", str(ROOT / "extractor.py"), "archive", str(source), str(extract),
                "--archive-root", str(base / "archive"),
            ], text=True, capture_output=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertTrue(source.exists())

    def test_archive_refuses_explicitly_protected_source(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base / "source.jsonl"
            extract = base / "extract.md"
            source.write_text("source", encoding="utf-8")
            os.utime(source, (time.time() - 172800, time.time() - 172800))
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            extract.write_text(f"Source SHA-256: `{digest}`\n", encoding="utf-8")
            run = subprocess.run([
                "python3", str(ROOT / "extractor.py"), "archive", str(source), str(extract),
                "--archive-root", str(base / "archive"), "--protect", str(source),
            ], text=True, capture_output=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertTrue(source.exists())

    def test_archive_moves_only_after_digest_attestation(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base / "source.jsonl"
            extract = base / "extract.md"
            source.write_text("source", encoding="utf-8")
            os.utime(source, (time.time() - 172800, time.time() - 172800))
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            extract.write_text(f"Source SHA-256: `{digest}`\n", encoding="utf-8")
            run = subprocess.run([
                "python3", str(ROOT / "extractor.py"), "archive", str(source), str(extract),
                "--archive-root", str(base / "archive"),
            ], text=True, capture_output=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertFalse(source.exists())
            self.assertTrue((base / "archive" / source.relative_to(source.anchor)).exists())

    def test_permanent_role_session_cannot_be_archived(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            session = "01a0aacb-ac84-71a1-88a0-05ed9961ca9d"
            source = base / f"rollout-{session}.jsonl"
            extract = base / "extract.md"
            source.write_text("source", encoding="utf-8")
            os.utime(source, (time.time() - 172800, time.time() - 172800))
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            extract.write_text(f"Source SHA-256: `{digest}`\n", encoding="utf-8")
            run = subprocess.run([
                "python3", str(ROOT / "extractor.py"), "archive", str(source), str(extract),
                "--archive-root", str(base / "archive"),
            ], text=True, capture_output=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn("protected role", run.stderr)
            self.assertTrue(source.exists())

    def test_sensitive_selected_text_is_detected(self):
        from extractor import SENSITIVE

        self.assertIsNotNone(SENSITIVE.search("api_key=abcdefghijklmnop1234"))
        self.assertIsNone(SENSITIVE.search("The design mentions an API key without a value."))


if __name__ == "__main__":
    unittest.main()
