#!/usr/bin/env python3
"""Run the reminder hook as Claude Code would: event JSON on stdin, JSON on stdout."""
import json
import os
import pathlib
import shlex
import subprocess
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
HOOK = HERE / "reminder-hook.py"
DEFINITION = HERE / "reminder-hook.json"
PROJECT = HERE.parent.parent


def event(session):
    return json.dumps({"hook_event_name": "UserPromptSubmit", "session_id": session, "prompt": "hello"})


class ReminderHook(unittest.TestCase):
    def run_hook(self, argv, session, env=None):
        return subprocess.run(["python3", str(HOOK), *argv], input=event(session), text=True,
                              capture_output=True, env={**os.environ, **(env or {})}, timeout=10)

    def test_every_third_prompt_per_session_carries_the_first_four_paragraphs(self):
        with tempfile.TemporaryDirectory() as directory:
            prompt = pathlib.Path(directory) / "prompt.md"
            prompt.write_text("one\n\ntwo\nstill two\n\nthree\n\nfour\n\nfive\n")
            state = pathlib.Path(directory) / "state"
            for session in ("aaaaaaaa-1111", "bbbbbbbb-2222"):
                outputs = [self.run_hook(["--prompt-file", str(prompt), "--state-dir", str(state), "--every", "3"], session)
                           for _ in range(6)]
                self.assertTrue(all(result.returncode == 0 for result in outputs), [r.stderr for r in outputs])
                injected = [index + 1 for index, result in enumerate(outputs) if result.stdout.strip()]
                self.assertEqual(injected, [3, 6])
                context = json.loads(outputs[2].stdout)["hookSpecificOutput"]
                self.assertEqual(context["hookEventName"], "UserPromptSubmit")
                self.assertEqual(context["additionalContext"], "one\n\ntwo\nstill two\n\nthree\n\nfour")

    def test_state_directory_defaults_to_the_seat_job_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_hook(["--every", "1"], "cccccccc-3333", env={"CLAUDE_JOB_DIR": directory})
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((pathlib.Path(directory) / "main-flow-reminder" / "cccccccc-3333.count").is_file())
            self.assertIn("You are a main flow", json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"])

    def test_missing_prompt_fails_without_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_hook(["--prompt-file", f"{directory}/missing.md", "--state-dir", directory, "--every", "1"],
                                   "dddddddd-4444")
            self.assertEqual(result.returncode, 1)
            self.assertIn("main-flow reminder failed", result.stderr)

    def test_definition_command_runs_the_hook_every_twentieth_prompt(self):
        definition = json.loads(DEFINITION.read_text())
        handler = definition["hooks"]["UserPromptSubmit"][0]["hooks"][0]
        self.assertEqual(handler["type"], "command")
        with tempfile.TemporaryDirectory() as directory:
            env = {**os.environ, "CLAUDE_PROJECT_DIR": str(PROJECT), "CLAUDE_JOB_DIR": directory}
            outputs = [subprocess.run(["sh", "-c", handler["command"]], input=event("eeeeeeee-5555"), text=True,
                                      capture_output=True, env=env, timeout=10) for _ in range(20)]
            self.assertEqual([index + 1 for index, r in enumerate(outputs) if r.stdout.strip()], [20])


if __name__ == "__main__":
    unittest.main()
