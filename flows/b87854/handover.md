# Flow handover — Psyche Medium b87854

This seat has to be relaunched because it cannot persist. It was started from inside another Claude session's Bash tool and inherited `CLAUDE_CODE_CHILD_SESSION=1`. So Claude Code writes no transcript, no session-registry record and no remote title for it; the remote title shows another seat's name. Details: receipts/remote-title.md. The handover is in this file because there is no transcript to hold it.

Its successor starts from e51411's handover (Claude session e5141130-9a4a-4b8f-b405-67d941a7b320, the latest "# Flow handover — Psyche Medium e51411") plus this file and flows/b87854/log.md.

## New since e51411's handover

- Survey at 15:10 (log.md): Flow 149120f8 is built but not activated, and the running nexus is 4560453. Nothing is bound. Send, Stop and List exist only in Mind Sol 00f95a's uncommitted worktree flow/mind-sol-00f95a-flow-basics. Prometheus is on kernel 7.1.8, generation 54, and its cache answers. Wi-Fi A is applied at runtime only, not in CriomOS source; Yggdrasil over the cable is unconfirmed. Field Sol and Field Luna were not launched: the launcher's coherent-flow-deployment-required gate is still on.
- Sent: to 5f38bc, what blocks activation and binding, and the HM gap; to 00f95a, what is left before Send, Stop and List go to Astra; to e51411, to cede the seat and log the living's words since its handover. All three came back Transported; no answers seen.
- Presented to the living, with no reply yet:
  - the proposed basic Flow scope (start, stop and send through Flow, Message on top, a successful Send makes a flow Active; no List, no title);
  - the Prometheus fork, (a) turn off its access point now or (b) keep it and fix the mt7925 driver, with (a) recommended.
- HM registration is blocked for Claude seats: the pane never shows interactive_ready, and `--readiness-probe` needs a Codex-shaped `--rollout` (hm.py since 3a4161141). receipts/seat.md.
- The living asked whether this is the new Opus, because they are still talking to the old one, and said the remote-control title says Sonnet. Answer: yes, and e51411 was asked to cede. The Sonnet title is 9c7514's name leaking across, because this session cannot persist.

## Launch fix for the successor

Start Claude with `env -u CLAUDE_CODE_CHILD_SESSION -u CLAUDE_CODE_SESSION_ID -u CLAUDE_PID CLAUDE_CODE_FORCE_SESSION_PERSISTENCE=1 claude ...`. Before claiming, titling or registering, check that `~/.claude/sessions/<pid>.json` and the transcript exist.
