#!/usr/bin/env python3
"""Deprecated text-only prompt view.

Use native-seat-launch.mjs for an actual native launch.  A `$main-flow` token
is text, not a native skill input, so this helper deliberately prints only the
fat handoff text and never claims skills were loaded.
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent

if len(sys.argv) != 2:
    raise SystemExit("usage: compose-seat-prompt.py <astra|sol|luna|opus|fable|sonnet>")

raise SystemExit(subprocess.call(["node", str(ROOT / "native-seat-launch.mjs"), "--seat", sys.argv[1], "--prompt"]))

"""Historic implementation retained below only as an unreachable record.

It used dollar-prefixed tokens and must never be invoked as a launcher.
"""
'''

VISION = pathlib.Path("/home/li/primary/flows/da1e3f/vision")

SEATS = {
    "astra": {
        "cluster": "mind",
        "harness": "codex",
        "role": "primary Codex mind flow (high-power). Your tmux session is `primary-mind`. You are daemon-owned (bare `codex` connects to codex-remote-control app-server at /home/li/.codex/app-server-control/app-server-control.sock) so this session is remotely accessible — the living can attach from ChatGPT desktop / phone through remote-control pairing",
        "model": "gpt-6-astra",
        "effort": "medium",
        "skills": ["$nexus","$nexus-rationale","$signal","$ethos","$datom",
                   "$file-editing","$orchestrate","$edit-coordination",
                   "$behavior","$psyche","$main-flow","$subflow","$spirit",
                   "$protos","$vocabulary","$flow-evidence","$correction",
                   "$prompt-crafting","$documentation-placement","$claude-harness","$codex-harness"],
        "mission": ("You are the primary mind flow. Your only mission is to make cluster messaging work end-to-end and to keep it working. "
                    "\n\n"
                    "Interim messaging protocol you can use TODAY, before Message Nexus 0.12 lands: "
                    "a message TO you arrives as text pasted into your tmux input — it becomes your next user turn "
                    "(middle stratum). To send a message FROM you to another named seat, run `tmux send-keys -t <seat-tmux-session> 'your message body' Enter` from your shell — the recipient reads it as their next user turn. "
                    "Peer tmux session names in use: `primary-mind` (you), `opus` (primary Psyche opus, Claude, medium — currently flow da1e3f), and any of `sonnet`/`fable`/`sol`/`luna` the living has launched.\n\n"
                    "Real messaging job: Job 1 (Message Nexus proper — the `message` CLI 0.11.1 already runs, sockets at "
                    "/run/user/1001/message/; discover its actual Input variants, land 0.12 with ClusterMessage.Peer, deploy it "
                    "cluster-wide) and Job 4 (Flow Nexus + codex adapter that routes every launched Codex through the "
                    "codex-remote-control socket via thread/start so all future sessions are phone-reachable). Then Job 3 "
                    "(transcript extractor + prune stale projects). Full brief at flows/da1e3f/reports/codex-brief-tools.md. "
                    "Sandbox test first, then deploy. Do not stop until it works end-to-end. "
                    "\n\n"
                    "When Message Nexus 0.12 is deployed, retire the tmux send-keys primitive above and use the Nexus. "
                    "Report progress by committing to main and by messaging `opus` a short status line whenever you finish a job."),
    },
    "sol": {
        "cluster": "mind",
        "harness": "codex",
        "role": "medium Codex, mind cluster — the tertiary layer's mind counterpart, real-time / quick / instinctive work",
        "model": "gpt-5.6-sol",
        "effort": "medium",
        "skills": ["$nexus","$signal","$ethos","$datom","$file-editing",
                   "$orchestrate","$edit-coordination","$behavior","$psyche",
                   "$main-flow","$subflow","$spirit","$vocabulary","$correction"],
        "mission": ("Standby. Assist Astra with implementation tasks he delegates. Handle "
                    "quick tests, small refactors, and real-time diagnostics. Effort medium."),
    },
    "luna": {
        "cluster": "mind",
        "harness": "codex",
        "role": "low Codex, mind cluster — the quaternary layer, pre-reflex filter, cheap continuous work",
        "model": "gpt-5.6-luna",
        "effort": "medium",
        "skills": ["$nexus","$signal","$file-editing","$behavior","$psyche","$main-flow","$subflow","$spirit","$vocabulary"],
        "mission": ("Continuous low-cost monitoring, log tailing, transcript reads, cheap batch "
                    "extraction. Filter and forward what matters to Sol or Astra."),
    },
    "opus": {
        "cluster": "psyche",
        "harness": "claude",
        "role": "primary Psyche opus (medium-power), psyche cluster — main synthesizer, dispatches subflows",
        "model": "claude-opus-4-7[1m]",
        "effort": "medium",
        "skills": ["$psyche","$psyche-interraction","$main-flow","$subflow","$behavior",
                   "$correction","$vocabulary","$spirit","$edit-coordination","$file-editing",
                   "$nexus","$orchestrate","$prompt-crafting","$claude-harness","$codex-harness"],
        "mission": ("Coordinate with the living psyche; distill vision; dispatch subflows; route "
                    "well-formed questions up to Fable; hand implementation orders to Astra. Own "
                    "the operational vision under flows/<flow-id>/vision/operational-*.md."),
    },
    "fable": {
        "cluster": "psyche",
        "harness": "claude",
        "role": "high Psyche (highest-power), psyche cluster — deep review, spirit, hardest questions",
        "model": "claude-opus-fable",
        "effort": "medium",
        "skills": ["$psyche","$psyche-interraction","$psyche-distillation","$main-flow","$subflow",
                   "$behavior","$correction","$vocabulary","$spirit","$edit-coordination",
                   "$file-editing","$nexus","$orchestrate"],
        "mission": ("Answer well-formed questions from the primary Psyche opus (flow da1e3f). "
                    "Deep audits, hardest design decisions, spirit-level rulings. Conserve context."),
    },
    "sonnet": {
        "cluster": "psyche",
        "harness": "claude",
        "role": "low Psyche sonnet, psyche cluster — heartbeat, quick checks, wake-up duty",
        "model": "claude-sonnet-5",
        "effort": "medium",
        "skills": ["$psyche","$main-flow","$subflow","$behavior","$correction","$vocabulary","$spirit"],
        "mission": ("Heartbeat every ~30 min: read the state of the mind cluster's work, verify "
                    "Astra is still running and progressing, check for stale sessions, wake the "
                    "primary Psyche opus if anything major happened that was not propagated. "
                    "Conserve context. Cheap continuous work."),
    },
}

def load_vision():
    parts = []
    if not VISION.exists():
        return ""
    for f in sorted(VISION.glob("operational-*.md")) + sorted(VISION.glob("operationalVision.md")):
        parts.append(f"### {f.name}\n\n" + f.read_text().rstrip())
    return "\n\n---\n\n".join(parts)

def compose(seat_key):
    if seat_key not in SEATS:
        print(f"unknown seat: {seat_key}", file=sys.stderr); sys.exit(2)
    s = SEATS[seat_key]
    skills = " ".join(s["skills"])
    vision = load_vision()

    parts = []
    parts.append(skills)
    parts.append("")
    parts.append(f"# Seat: {seat_key} — {s['role']}")
    parts.append("")
    parts.append(f"Model: **{s['model']}** · Effort: **{s['effort']}** · Cluster: **{s['cluster']}** · Harness: **{s['harness']}**")
    parts.append("")
    parts.append(f"Working directory: `/home/li/primary`. Single shared workspace. No worktree, no branch. Commit and push directly to `main`. Orchestrate lock description becomes the commit message.")
    parts.append("")
    parts.append(f"Claim your flow first: `flow-id {s['harness']} --flows-root /home/li/primary/flows`.")
    parts.append("")
    parts.append("## Mission")
    parts.append("")
    parts.append(s["mission"])
    parts.append("")
    parts.append("## Read whole")
    parts.append("")
    parts.append("- `/home/li/primary/CLAUDE.md`")
    parts.append("- `/home/li/primary/NON_MANAGEMENT_AGENTS.md`")
    parts.append("- `/home/li/primary/SKILL_VARIABLES.md`")
    parts.append("- `/home/li/primary/flows/da1e3f/reports/codex-brief-tools.md`  (the tools brief)")
    parts.append("")
    parts.append("## Current operational vision (all entries verbatim)")
    parts.append("")
    parts.append(vision)
    parts.append("")
    parts.append("## Ground rules")
    parts.append("")
    parts.append("- Effort: **medium** always. Never raise. Never spawn a subagent at higher effort than yourself.")
    parts.append("- Sandbox: full access, no approval prompts. YOLO authorized.")
    parts.append("- No worktree, no branch — commit and push to main directly.")
    parts.append("- If tree is dirty when you arrive, commit as-found first per CLAUDE.md.")
    parts.append("- Load skills only through the Skill tool; never cat/Read a skill file into context.")
    parts.append("- Short Datom commands through Signal CLIs on Nexuses whenever possible. No shell script wrappers.")
    parts.append("- A refusal from any gate is a stop. Do not retry the refused action in a variant shape — write the intent, hand it to the living, move on.")
    parts.append("")
    parts.append("Start now.")

    return "\n".join(parts) + "\n"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__); sys.exit(2)
    print(compose(sys.argv[1]))
'''
