#!/usr/bin/env python3
"""UserPromptSubmit hook: re-inject the main-flow-mode core every Nth prompt.

The core is the first four paragraphs of the replacing system prompt.  The
prompt count is kept per native session, in the session's state directory:
``--state-dir`` when given, else ``$CLAUDE_JOB_DIR`` (the per-seat job
directory the seat launcher exports).  A failure exits 1, which Claude Code
treats as a non-blocking hook error: the living's prompt still goes through.
"""

import argparse
import fcntl
import json
import os
import pathlib
import re
import sys

PROMPT = pathlib.Path(__file__).resolve().with_name("system-prompt.md")
SESSION = re.compile(r"^[A-Za-z0-9-]{8,128}$")
PARAGRAPHS = 4


def core(prompt_file: pathlib.Path) -> str:
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", prompt_file.read_text()) if part.strip()]
    if len(paragraphs) < PARAGRAPHS:
        raise ValueError(f"main-flow prompt has fewer than {PARAGRAPHS} paragraphs: {prompt_file}")
    return "\n\n".join(paragraphs[:PARAGRAPHS])


def state_directory(given):
    if given is not None:
        return given
    job = os.environ.get("CLAUDE_JOB_DIR")
    if not job:
        raise ValueError("no session state directory: pass --state-dir or export CLAUDE_JOB_DIR")
    return pathlib.Path(job) / "main-flow-reminder"


def count_prompt(state_dir: pathlib.Path, session_id: str) -> int:
    if not SESSION.fullmatch(session_id or ""):
        raise ValueError("hook input has an invalid native session_id")
    state_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (state_dir / f"{session_id}.count").open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        handle.seek(0)
        previous = handle.read().strip()
        value = int(previous) + 1 if previous else 1
        handle.seek(0)
        handle.truncate()
        handle.write(f"{value}\n")
        handle.flush()
        os.fsync(handle.fileno())
        return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt-file", type=pathlib.Path, default=PROMPT)
    parser.add_argument("--state-dir", type=pathlib.Path)
    parser.add_argument("--every", type=int, default=20)
    args = parser.parse_args()
    if args.every < 1:
        raise ValueError("--every must be positive")
    event = json.load(sys.stdin)
    if event.get("hook_event_name") != "UserPromptSubmit":
        raise ValueError("main-flow reminder only accepts UserPromptSubmit")
    count = count_prompt(state_directory(args.state_dir), event.get("session_id", ""))
    if count % args.every == 0:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": core(args.prompt_file),
        }}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"main-flow reminder failed: {error}", file=sys.stderr)
        raise SystemExit(1)
