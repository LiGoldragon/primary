# Flow launcher dry-run proposal

This is a renderer and fixture test only. It never spawns Ghostty, Claude, a
service, or a remote-control session. It is reusable component-library work,
not the final standalone launcher architecture. The temporary Home Flow
component / Persona Q77 stopgap is limited to rendering an authorized launch
plan until the Flow component has an approved home and command surface.

The renderer requires a supplied, validated user environment and preserves only
`HOME`, `PATH`, and the display/XDG values (`DISPLAY`, `WAYLAND_DISPLAY`,
`XDG_CURRENT_DESKTOP`, `XDG_SESSION_TYPE`, and `XDG_RUNTIME_DIR`). It does not
read ambient secrets. The planned scoped command places `env -i` *inside* the
transient scope, removing `NO_COLOR`, `CODEX_CI`, and all `CODEX_*` variables
before Ghostty or Claude begins. This responds to Codex unified-exec's forced
`NO_COLOR=1` and `CODEX_CI=1` environment at
`/tmp/codex-source.cT7Ro4/codex-rs/core/src/unified_exec/process_manager.rs:89-100`
and its environment construction at `exec_env.rs:13-40`.

The proposed argv is `systemd-run --user --scope --unit=flow-<id>.scope
--collect env -i ... ghostty ... bash -lc ...`. The scope surrounds Ghostty and
therefore its Claude child; scoping Claude alone would leave the terminal and
PTY in `codex-remote-control.service`, where a control-group kill can still
terminate the interactive session. The scope is a sibling in the user manager's
app slice, separate from the current `codex-remote-control.service`; it is not a
durable unit and no unit is installed.

Claude is planned with the exact session UUID, explicit `--name` and
`--remote-control <name>`, `--effort medium`,
`--dangerously-skip-permissions`, `--append-system-prompt-file <system-file>`,
and exactly one positional argument read from the user-prompt file. Postflight
is pure and requires the exact planned UUID, a nonempty `bridgeSessionId` in the
session record, and one remote-list entry matching both that bridge ID and the
planned name. A window is deliberately ignored. Fixtures include the earlier
false-positive shape: window present but bridge absent, plus wrong-name and
wrong-UUID records.

Known source: the local Claude help exposes `--session-id`, `--name`,
`--remote-control`, `--effort`, `--dangerously-skip-permissions`, and
`--append-system-prompt-file`. Unknown: whether a newly started Claude session
will create the required bridge registration in the actual remote transport.
The bridge/name postflight gate remains required before any launch can be called
successful.

## Source proposal, not an authorized Curriculum landing

`Session lifecycle is independent of a transport server: a Flow-owned session
scope owns its terminal and harness, while a transport server may attach,
observe, or relay without becoming the session's lifetime owner.`

This text is a proposal for a later Curriculum landing. It does not change
Curriculum, install a unit, create a component repository, or authorize a live
flow launch.
