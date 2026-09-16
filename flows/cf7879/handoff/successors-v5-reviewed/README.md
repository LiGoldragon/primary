# Reviewed successor packets, 2026-09-16

Both harnesses receive complete replacement base instructions: claude-base.md through --system-prompt-file; codex-base.md through thread/start.baseInstructions. Sources include Spirit, Intent, relevant Vision, current efa157 records, paired Codex report, complete named/location skill blocks and historical ten turns/decisions. Source and artifact manifests freeze exact content. Historical records do not reactivate old commands or adopt proposals.

Root verification: both dry-runs succeeded from /tmp; first prompt 779 bytes; bases 236277 (Claude) and 235942 (Codex) bytes. Complete skill bodies were extracted from each block and compared byte-exact to frozen sources. A corrupted Codex base was refused before transport. No claim of child context inheritance follows.

Claude: python3 claude-launch.py --cwd /absolute/independent-jj-clone defaults to dry-run. Add --launch only on efa157’s launch word. Structured arguments, fable, NO_COLOR unset, TERM set, stdin detached. JSON envelope plus environment and 64KiB reserve is a conservative size model, not an actual daemon-record receipt. Post-launch roster, own scope, remote control and prompt user-turn checks remain required.

Codex: node codex-launch.mjs --cwd /absolute/independent-jj-clone defaults to dry-run. --launch --socket /absolute/socket creates a durable Astra thread with the full base, names it and starts the first turn. It requires connected remote status. Partial failure after thread creation prints its ID: inspect that ID, never blindly relaunch. Runtime readiness, exact identity and context receipt still must be verified.

Host remote witness: supported app-server remoteControl/status/read with experimentalApi capability returned connected, serverName ouranos, environmentId env_e_6a6a1cede71c8326a96f12cb2b467b06. ChatGPT desktop processes exist locally. This is not laptop pairing/visibility proof. Official desktop SSH route: https://learn.chatgpt.com/docs/remote-connections — configure a concrete host alias, verify SSH, ensure remote codex PATH/auth, then select the host/project in desktop Settings > Connections > SSH. Same durable remote store is expected to expose the thread; direct desktop receipt is still needed.

Order 5 lifts the pace hold. Read-only quota at 2026-09-16T15:12:54.221Z: 19% weekly remaining, reset 2026-09-19T15:05:28Z, three reset credits available. No credit consumed. The living decides when.
