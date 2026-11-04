#!/usr/bin/env python3
"""Extract the living's typed messages from a Claude Code transcript.

Usage:
    extract-living-words.py [TRANSCRIPT.jsonl] [OUTPUT.md]

Defaults: the transcript of session 019YVikvizVxNuXqEtxEmg8C (flow 04df39),
written to flows/a53796/vision-raw/living-words-04df39.md.

The output is rebuilt in full from the transcript on every run, so rerunning
it after the session grows appends the new messages and changes nothing else.
Each entry is headed by its local timestamp, verbatim, and entries are in
chronological order.

Kept, three kinds:
  - typed messages: user entries whose origin is "human" and that are not
    isMeta. Heading: "## <local time>".
  - queued messages: the living's messages typed mid-turn. Claude Code
    delivers them as attachment entries of type "queued_command" whose origin
    is "human" (the matching queue-operation "enqueue" carries the same text
    and time, so the attachment is the single source). Heading:
    "## <local time> (queued)".
  - relays: the living's comments carried by another session. Two shapes:
    cross-session peer messages (user entries whose origin kind is "peer"),
    and a relay Flow re-delivered as a human-origin pasted block whose
    datom has a Sender.{ ... } head. Heading:
    "## <local time> (relayed by <from-name>)". Only the relayed text is
    written: for a peer message the origin body, without the envelope.

Dropped: tool results, task notifications, harness markers such as
"[Request interrupted by user]", <system-reminder> blocks, and the launch
brief (a pasted block opening with the skill list).
"""

import json
import os
import re
import sys
from datetime import datetime

SESSION_TAG = "019YVikvizVxNuXqEtxEmg8C"
FLOW_ID = "04df39"
DEFAULT_TRANSCRIPT = os.path.expanduser(
    "~/.claude/projects/-home-li-primary/04df3910-b654-5c9d-a32d-b5cd5449dbce.jsonl"
)
DEFAULT_OUTPUT = "/home/li/primary/flows/a53796/vision-raw/living-words-04df39.md"

SYSTEM_REMINDER = re.compile(r"<system-reminder>.*?</system-reminder>\s*", re.S)
LAUNCH_BRIEF_OPENING = "<pasted_content"
LAUNCH_BRIEF_MARK = "These are your skills, given here; do not reload them."
PASTED_OPEN = re.compile(r'^<pasted_content id="[^"]*">\n?', re.S)
PASTED_CLOSE = re.compile(r"\n?</pasted_content[^>]*>\s*$", re.S)
RELAY_SENDER = re.compile(r"Sender\.(\{[^{}]*\})")


def parse_time(stamp):
    return datetime.fromisoformat(stamp.replace("Z", "+00:00"))


def message_text(entry):
    content = entry["message"]["content"]
    if isinstance(content, str):
        return content
    # A list here is a tool result or a multi-block turn; only text blocks count.
    return "\n".join(
        block.get("text", "")
        for block in content
        if isinstance(block, dict) and block.get("type") == "text"
    )


def is_launch_brief(text):
    stripped = text.strip()
    return stripped.startswith(LAUNCH_BRIEF_OPENING) and LAUNCH_BRIEF_MARK in stripped


def is_living_message(entry):
    if entry.get("type") != "user" or entry.get("isMeta"):
        return False
    origin = entry.get("origin")
    return isinstance(origin, dict) and origin.get("kind") == "human"


def is_peer_message(entry):
    # Peer messages are marked isMeta by the harness; that flag is not a reason to drop them.
    if entry.get("type") != "user":
        return False
    origin = entry.get("origin")
    return isinstance(origin, dict) and origin.get("kind") == "peer"


def is_queued_message(entry):
    attachment = entry.get("attachment")
    if entry.get("type") != "attachment" or not isinstance(attachment, dict):
        return False
    if attachment.get("type") != "queued_command":
        return False
    origin = attachment.get("origin")
    return isinstance(origin, dict) and origin.get("kind") == "human"


def relay_from_pasted(prompt):
    """A Flow-delivered relay: a pasted datom whose head names a Sender."""
    match = RELAY_SENDER.search(prompt)
    if not match or not prompt.lstrip().startswith(LAUNCH_BRIEF_OPENING):
        return None
    body = PASTED_CLOSE.sub("", PASTED_OPEN.sub("", prompt.strip(), count=1))
    return match.group(1), body.strip("\n")


def extract(transcript):
    found = []  # (moment, label, text); label is "" for a typed message
    with open(transcript, encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            entry = json.loads(line)
            moment = parse_time(entry["timestamp"]) if "timestamp" in entry else None

            if is_peer_message(entry):
                body = entry["origin"].get("body", "").strip("\n")
                if body:
                    name = entry["origin"].get("name", "unknown")
                    found.append((moment, f" (relayed by {name})", body))
                continue

            if is_queued_message(entry):
                prompt = entry["attachment"].get("prompt", "")
                if is_launch_brief(prompt):
                    continue
                relay = relay_from_pasted(prompt)
                if relay is not None:
                    name, body = relay
                    if body:
                        found.append((moment, f" (relayed by {name})", body))
                    continue
                text = prompt.strip("\n")
                if text.strip():
                    found.append((moment, " (queued)", text))
                continue

            if not is_living_message(entry):
                continue
            text = SYSTEM_REMINDER.sub("", message_text(entry))
            stripped = text.strip()
            if not stripped or is_launch_brief(stripped):
                continue
            found.append((moment, "", text.strip("\n")))
    found.sort(key=lambda triple: triple[0])
    return found


def local_stamp(moment):
    # Local wall-clock time, whole seconds, as in "## 2026-11-03T14:02:11".
    return moment.astimezone().strftime("%Y-%m-%dT%H:%M:%S")


def main(argv):
    transcript = argv[1] if len(argv) > 1 else DEFAULT_TRANSCRIPT
    output = argv[2] if len(argv) > 2 else DEFAULT_OUTPUT
    messages = extract(transcript)
    now = datetime.now().astimezone().isoformat(timespec="seconds")

    parts = [
        f"The living's messages in session {SESSION_TAG} (flow {FLOW_ID}), "
        f"verbatim, with queued messages and relays of them, extracted {now}.\n"
    ]
    for moment, label, text in messages:
        parts.append(f"\n## {local_stamp(moment)}{label}\n\n{text}\n")
    body = "".join(parts)

    os.makedirs(os.path.dirname(output), exist_ok=True)
    temp = output + ".tmp"
    with open(temp, "w", encoding="utf-8") as handle:
        handle.write(body)
    os.replace(temp, output)

    queued = sum(1 for _, label, _ in messages if label == " (queued)")
    relayed = sum(1 for _, label, _ in messages if label.startswith(" (relayed"))
    print(f"messages: {len(messages)}")
    print(f"typed: {len(messages) - queued - relayed}")
    print(f"queued: {queued}")
    print(f"relayed: {relayed}")
    if messages:
        print(f"first: {local_stamp(messages[0][0])}")
        print(f"last: {local_stamp(messages[-1][0])}")
    print(f"bytes: {len(body.encode('utf-8'))}")
    print(f"output: {output}")


if __name__ == "__main__":
    main(sys.argv)
