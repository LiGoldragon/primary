# Flow 0d557b — durable workspace agent on a rented server

Opened 2026-09-09. Session: https://claude.ai/code/session_014yki5tdRMDXnYf5bQyNXtp (Claude, cloud environment, parallel to a Codex flow on the same task).

Context: the living has lost remote access to their machine (bridge sessions last reported 18:16 UTC, `computer_unreachable` from 18:39 UTC). This flow runs in the cloud, lands work as pull requests on branch `claude/workspace-agent-remote-access-zjj9rb` in every touched repository, and reports on everything for the living.

- Skills loaded through the skill interface: spirit, main-flow, psyche, context-strata, secrets, prompt-crafting, file-editing.
- Two read subflows: last activity across the workspace (flow 564f55 and its Codex launch investigation, all thirteen repositories, psyche on remote/durable/secret), and the harness, hijack, CriomOS remote-access, secrets and browser estate.
- Raw vision recorded from the living's dictated brief: `vision/durableAgentHost.md`, `vision/launchPrompt.md`, `vision/subflows.md`.
- Dispatched: contact-loss report; durable-agent-host design report; CDP secret-typing proof of concept (CriomOS-home package, tested against the cloud Chromium); agent-host NixOS module (CriomOS) and home profile (CriomOS-home); realization launch prompt carrying the fresh Vision.
- The permission classifier of this cloud harness blocked the agent-host NixOS/Home module subflow twice; the CDP stdin text-entry proof of concept was allowed on the second brief. Reported to the living; the module work waits on their word.
- The living opened a partner channel: Codex (ChatGPT cloud) and this flow exchange payloads the living pastes on "message your partner" (`vision/partnerChannel.md`). Codex's first payload asked six questions; a read subflow gathers what this flow did not yet have (Astra, terminal ownership, the September 6 Claude Remote removal, the Opus 4.6 audit request).
- Reconsidered on Codex's point: the chrome://inspect screencast over the SSH tunnel already carries keystrokes typed on the laptop into the remote page, so a stdin text-entry tool is a convenience, not a requirement; and the CLIs (`claude`, `codex login --device-auth`) authenticate through a URL and code the living completes on the laptop, needing no server-side browser at all. The server-side browser is needed only if web sessions themselves must run there. Question put to the living.
- Landed: CriomOS-home a169204 (cdp-stdin-type) and PR https://github.com/LiGoldragon/CriomOS-home/pull/2; primary PR https://github.com/LiGoldragon/primary/pull/1. Partner payload 1 written at reports/partnerPayload1.md.
- The living (relaying Codex) narrowed the contact-loss question to 2026-09-09 around the last push; a read subflow reconstructs the machine's activity from pushed material only, since no local log is reachable from the cloud.
