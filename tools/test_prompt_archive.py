#!/usr/bin/env python3
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


TOOL = Path(__file__).with_name("prompt-archive.py")


class PromptArchiveTests(unittest.TestCase):
    def run_tool(self, archive, *args, check=True):
        return subprocess.run([sys.executable, str(TOOL), "--archive", str(archive), *args], capture_output=True, check=check)

    def test_materializes_retrieves_and_verifies_a_chain(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); archive = root / "archive"
            base = root / "base"; patch1 = root / "first.diff"; patch2 = root / "second.diff"
            base.write_text("alpha\nbeta\n")
            patch1.write_text("--- base\n+++ next\n@@ -1,2 +1,2 @@\n alpha\n-beta\n+bravo\n")
            first = json.loads(self.run_tool(archive, "materialize", "--base", str(base), "--diff", str(patch1)).stdout)
            next_base = root / "next"; self.run_tool(archive, "get", "--id", first["id"], "--output", str(next_base))
            patch2.write_text("--- next\n+++ last\n@@ -1,2 +1,3 @@\n alpha\n bravo\n+charlie\n")
            second = json.loads(self.run_tool(archive, "materialize", "--base", str(next_base), "--diff", str(patch2), "--parent", first["id"]).stdout)
            fetched = self.run_tool(archive, "get", "--id", second["id"]).stdout
            self.assertEqual(fetched, b"alpha\nbravo\ncharlie\n")
            self.assertEqual(json.loads(self.run_tool(archive, "verify", "--id", second["id"]).stdout)["chain"], [second["id"], first["id"], first["parent_id"]])
            raw_digest = bytes.fromhex(second["prompt_sha256"])
            self.assertEqual((archive / "objects" / "sha256" / second["prompt_sha256"][:2] / second["prompt_sha256"] / "sha256").read_bytes(), raw_digest)

    def test_refuses_wrong_base_and_detects_corruption(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); archive = root / "archive"; base = root / "base"; patch = root / "bad.diff"
            base.write_text("alpha\n")
            patch.write_text("--- base\n+++ next\n@@ -1 +1 @@\n-beta\n+bravo\n")
            bad = self.run_tool(archive, "materialize", "--base", str(base), "--diff", str(patch), check=False)
            self.assertNotEqual(bad.returncode, 0)
            good = root / "good.diff"
            good.write_text("--- base\n+++ next\n@@ -1 +1 @@\n-alpha\n+bravo\n")
            record = json.loads(self.run_tool(archive, "materialize", "--base", str(base), "--diff", str(good)).stdout)
            content = archive / "objects" / "sha256" / record["prompt_sha256"][:2] / record["prompt_sha256"] / "content"
            content.write_bytes(b"tampered\n")
            verified = self.run_tool(archive, "verify", "--id", record["id"], check=False)
            self.assertNotEqual(verified.returncode, 0)


if __name__ == "__main__":
    unittest.main()
