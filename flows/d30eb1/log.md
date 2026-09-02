# ChatGPT Desktop new-chat diagnosis

Working instruction: remember the prior work on making ChatGPT Desktop operate correctly, then determine why it still cannot create a new chat. The supplied screenshot reports: `failed to load configuration: invalid transport in mcp_servers.codex_app`.

`FLOW_ID`: `d30eb1`. `FLOW_DIRECTORY`: `/home/li/primary/flows/d30eb1`.

This request rules investigation. It does not add a Vision entry.

Remembered: `01a047d2`, `01a05487`, `01a05c80`, `01a05e53`, `cf0ed9`, `01a05d17`, and `d05776` — depth 1. The written record separates the missing packaged Codex executable, the later malformed `codex_app` per-thread configuration, the ASAR syntax correction, the Full Access preference, and the still-running coupled upgrade. The prior corrected-live flow witnessed Desktop startup and a healthy WebSocket initialize, not successful new-thread or resume behavior.

Settled diagnosis: both the previously active ChatGPT `26.825.51511` ASAR and the newly activated `26.831.21537` ASAR contain the intended no-op patches for startup overrides and the private App Tools transport producer, but retain a separate local-thread preparation branch. Because a local host makes `usesDesktopMcp` true, that branch writes only `mcp_servers.codex_app.enabled_tools`. With the base producer removed, Codex receives a partial `codex_app` table with neither `command` nor `url` and rejects `thread/start` as `invalid transport`. Disposable app-server probes containing only that flat key reproduced the exact error under both Codex `0.151.0` and `0.152.1`. Static Codex configuration contains no `codex_app` server, and the installed plugin manifests themselves contain valid stdio transports.

Why the prior correction passed: its durable check asserted the two ASAR patch markers and exercised a bare app-server `thread/start`/`thread/resume`; it never exercised the Desktop-generated `enabled_tools` configuration. The corrected-live process itself logged the same automatic prewarm failure six seconds after launch, but the acceptance report stopped at startup and WebSocket initialization.

Runtime correction: the parent initially said it was still running after the living observed a crash. That was false. The pending Home activation stopped the persistent Codex `0.151.0` owner at 18:06:47, the owner failed to exit within the stop timeout, and systemd killed it with `SIGKILL` at 18:08:18 before starting Codex `0.152.1`. The living restarted this flow; restored conversation context is not process continuity.

No product source or deployment was changed in this investigation. The correct realization boundary is the user environment's ChatGPT ASAR patch and its test: under the settled ordinary-client topology, every private `codex_app` configuration emission, including the surviving `enabled_tools` leaf, must be removed and the actual Desktop-produced new/resumed-thread payload must be witnessed.
