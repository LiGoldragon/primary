# ChatGPT generation-992 restart witness

Method: inspected the existing Niri window and process before acting; closed
the ChatGPT window through Niri; sent `SIGTERM` only to the stale ChatGPT main
PID; launched the configured ChatGPT wrapper in a transient user systemd unit;
then probed the process executable, generation links, ASAR bytes, Niri window,
user systemd owner, Unix socket, and persistent Codex configuration. I also
visually inspected the reopened window. No source, Nix deployment, persistent
Codex owner, conversation database, or configuration file was edited.

Observed:

- The stale ChatGPT main PID was `1440540` (the process that predated
  generation 992). It exited after the targeted graceful termination. No
  second ChatGPT main process was left behind.
- The replacement is ChatGPT main PID `1528465`, started on 2026-09-02 at
  15:09:16 CEST. Its executable is the ChatGPT 26.825.51511 package selected
  by the active `home-manager-992-link`; generations 990 and 991 point to a
  different package instance. The process is supervised by the transient
  `cf0ed9-chatgpt.service`, whose result is `success` and whose main PID is
  `1528465`.
- The active `resources/app.asar` contains each intended byte-preserving patch
  marker exactly once: `getConfigOverrides:()=>[]` at byte offset `5295897`
  and `async function JE(){return[]}` at byte offset `3905233`.
- The package does not start successfully. The visible Niri window (ID 441,
  app ID `ChatGPT`, PID `1528465`) is a 376x118 failure dialog reading
  `ChatGPT failed to start. Unexpected token '}'`. The systemd journal for the
  launch contains only the normal GLib schema assertions and Node URL
  deprecation warning; the parse error is visible in the application dialog.
- The ASAR bytes explain the parse error. After the second marker and its
  padding, the first non-space bytes are `}function YE(`. The current
  `owned-agents/chatgpt/patch-asar.py` replacement for
  `NO_APP_TOOLS_CONFIG_OVERRIDE` emits a function with its own closing `}`,
  while that regex's lookahead leaves the original closing `}` in place. This
  produces the extra brace reported by the running package. The correction
  target is therefore the patch source's boundary/replacement, not the
  persistent owner or MCP transport configuration. This is source evidence
  only; this witness does not edit it.

Owner and persistence:

- `codex-remote-control.service` remains `active/running` with the same
  persistent owner PID `4013983`, working directory `/home/li/primary`, and
  command `codex app-server --remote-control --listen unix://`. The Unix
  control socket remains listening at
  `/home/li/.codex/app-server-control/app-server-control.sock`, owned by that
  PID. The process inventory showed one listener for this app-server service;
  other Codex processes are clients or existing child servers under that
  owner, not replacement owners.
- The active `/home/li/.codex/config.toml` still has no
  `[mcp_servers.codex_app]` section. Its existing MCP sections and the
  persistent Codex SQLite database were not changed by this restart; the
  database's observed mtime was 15:03:45 CEST, before the relaunch.

Thread boundary:

- No new-thread or resumed-thread request was sent during this witness. The
  application stopped at its parse-error dialog before the full ChatGPT UI
  became available, so there is no runtime acceptance evidence for either
  `thread/start` or `thread/resume`, and no claim that either operation now
  succeeds. Existing persistent owner and conversation state remain present,
  but successful preservation/use still needs the package parse correction.
- After an authorized corrected generation is active, the single living
  acceptance action is: perform one harmless New Chat prompt and then open one
  existing conversation to verify both new-thread and resumed-thread paths.

Conclusion: the requested restart did load generation 992 and preserved the
sole persistent Codex app-server owner, but it did not realize the intended
transport correction because generation 992 itself is syntactically invalid.
No further restart should be attempted until the patch-source boundary is
corrected and a replacement generation is built/deployed by the authorized
owner.

## Sources

- `/home/li/.local/state/nix/profiles/home-manager-990-link`,
  `home-manager-991-link`, `home-manager-992-link` (generation-to-package
  mapping inspected during the witness).
- `/git/github.com/LiGoldragon/CriomOS-home/owned-agents/chatgpt/patch-asar.py`
  (patch regex and replacement inspected; current source lines 46-57).
- `/home/li/.codex/config.toml` and
  `/home/li/.codex/sqlite/codex-dev.db` (persistent configuration/state
  presence and metadata).
- `systemctl --user show cf0ed9-chatgpt.service` and
  `journalctl --user -u cf0ed9-chatgpt.service` (replacement lifecycle and
  launch diagnostics).
- `ps`, `niri msg -j windows`, `ss -xlpn`, and direct byte probes of the
  active ChatGPT `resources/app.asar` (process, window, owner/socket, marker,
  and parse-boundary observations).
