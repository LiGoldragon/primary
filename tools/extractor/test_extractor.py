from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
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

    def test_archive_fails_closed_without_matching_extract(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base / "source.jsonl"
            extract = base / "extract.md"
            source.write_text("source", encoding="utf-8")
            extract.write_text("wrong digest", encoding="utf-8")
            run = subprocess.run([
                "python3", str(ROOT / "extractor.py"), "archive", str(source), str(extract),
                "--archive-root", str(base / "archive"),
            ], text=True, capture_output=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertTrue(source.exists())

    def test_archive_moves_only_after_digest_attestation(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = base / "source.jsonl"
            extract = base / "extract.md"
            source.write_text("source", encoding="utf-8")
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            extract.write_text(f"Source SHA-256: `{digest}`\n", encoding="utf-8")
            run = subprocess.run([
                "python3", str(ROOT / "extractor.py"), "archive", str(source), str(extract),
                "--archive-root", str(base / "archive"),
            ], text=True, capture_output=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertFalse(source.exists())
            self.assertTrue((base / "archive" / source.relative_to(source.anchor)).exists())


if __name__ == "__main__":
    unittest.main()
