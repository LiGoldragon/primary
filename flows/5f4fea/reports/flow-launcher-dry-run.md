# Flow launcher dry-run proposal

This is a renderer and fixture test only. It never spawns Ghostty, Claude, a
service, or a remote-control session. The proposed command uses an explicit
Ghostty title and working directory, runs `bash -lc 'cd ... && exec claude ...'`,
and carries the planned session UUID and display name.

The renderer preserves only discovered display/session variables (`DISPLAY`,
`WAYLAND_DISPLAY`, `XDG_CURRENT_DESKTOP`, `XDG_SESSION_TYPE`, and
`XDG_RUNTIME_DIR`). It marks `NO_COLOR`, `TERM`, and every `CODEX_*` variable for
removal from the interactive user environment, based on the Codex process
manager source at `/tmp/codex-source.cT7Ro4/codex-rs/core/src/unified_exec/process_manager.rs`.

Remote-control is an explicit proposal flag and is off by default. Postflight
must verify the exact session record, bridge ID, and remote-list name; no window
or process is considered successful without those records. The flow remains
owned by the transport/process scope rather than by a transport server. A
future systemd-run --user per-flow unit is a proposal only.
