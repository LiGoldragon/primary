#!/usr/bin/env python3
import json
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent
HOOK = ROOT / "claude-main-flow-reminder.py"
PROMPT = ROOT / "main-flow-system-prompt.md"


class ReminderTest(unittest.TestCase):
    def invoke(self, state, session, every=3, prompt=PROMPT):
        return subprocess.run(
            ["python3", str(HOOK), "--prompt-file", str(prompt),
             "--state-dir", str(state), "--every", str(every)],
            input=json.dumps({"hook_event_name": "UserPromptSubmit", "session_id": session}),
            text=True, capture_output=True,
        )

    def test_cadence_is_independent_per_native_session(self):
        with tempfile.TemporaryDirectory() as directory:
            state = pathlib.Path(directory)
            for session in ("session-aaaaaaaa", "session-bbbbbbbb"):
                first = self.invoke(state, session)
                second = self.invoke(state, session)
                third = self.invoke(state, session)
                self.assertEqual(json.loads(first.stdout), {})
                self.assertEqual(json.loads(second.stdout), {})
                output = json.loads(third.stdout)
                self.assertIn("delegate the work itself", output["hookSpecificOutput"]["additionalContext"])

    def test_missing_prompt_fails_on_reminder_turn(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.invoke(pathlib.Path(directory), "session-aaaaaaaa", every=1,
                                 prompt=pathlib.Path(directory) / "missing.md")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("main-flow reminder failed", result.stderr)


if __name__ == "__main__":
    unittest.main()
