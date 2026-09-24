#!/usr/bin/env python3
"""UserPromptSubmit hook that reminds one main seat on a per-session cadence."""

import argparse
import fcntl
import json
import os
import pathlib
import re
import sys

START = "<!-- MAIN_FLOW_REMINDER_START -->"
END = "<!-- MAIN_FLOW_REMINDER_END -->"
SESSION = re.compile(r"^[A-Za-z0-9-]{8,128}$")


def reminder(prompt_file: pathlib.Path) -> str:
    body = prompt_file.read_text()
    if body.count(START) != 1 or body.count(END) != 1:
        raise ValueError("main-flow prompt must contain one reminder block")
    value = body.split(START, 1)[1].split(END, 1)[0].strip()
    if not value:
        raise ValueError("main-flow reminder block is empty")
    return value


def count_prompt(state_dir: pathlib.Path, session_id: str) -> int:
    if not SESSION.fullmatch(session_id):
        raise ValueError("hook input has an invalid native session_id")
    state_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    state_file = state_dir / f"{session_id}.count"
    with state_file.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        handle.seek(0)
        old = handle.read().strip()
        value = int(old) + 1 if old else 1
        handle.seek(0)
        handle.truncate()
        handle.write(f"{value}\n")
        handle.flush()
        os.fsync(handle.fileno())
        return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt-file", required=True, type=pathlib.Path)
    parser.add_argument("--state-dir", required=True, type=pathlib.Path)
    parser.add_argument("--every", required=True, type=int)
    args = parser.parse_args()
    if args.every < 1:
        raise ValueError("--every must be positive")
    event = json.load(sys.stdin)
    if event.get("hook_event_name") != "UserPromptSubmit":
        raise ValueError("main-flow reminder only accepts UserPromptSubmit")
    current = count_prompt(args.state_dir, event.get("session_id", ""))
    if current % args.every:
        print("{}")
    else:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": reminder(args.prompt_file),
        }}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"main-flow reminder failed: {error}", file=sys.stderr)
        raise SystemExit(1)
