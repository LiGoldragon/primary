# Messaging state, 2026-09-27, subflow of 8904b1

Method: passive read-only listing and pane reads via `herdr`, `hm-list`,
`hm-heartbeat-state`, `systemctl --user status/cat`, and one `hm-send`. No
registry file was edited; no seat was started, stopped, replaced, or reaped.

## Registries present, by systemctl (`systemctl --user status/cat`)

- `flow-nexus.service` (stable): active, running `flow-0.12.2` binary
  (`/nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2/bin/flow-nexus`),
  overriding the unit's own declared `flow-0.14.0` via a drop-in
  `override.conf`. PID 1937, up since 2026-09-26 16:19:37 CST.
- `flow-nexus-next.service`: active, running `flow-0.17.1`
  (`/nix/store/zscrhhfyhkwa0qfvbkpg1piklfaahfa4-flow-0.17.1/bin/flow-nexus`).
  PID 90750, up since 2026-09-26 17:38:33 CST. Journal shows repeated
  "ordinary connection dropped" errors (broken pipe; rancor decode failures)
  from 2026-09-26 18:18 through 2026-09-27 02:50.
- `message-nexus-next.service`: active, running `message-0.17.0`
  (`/nix/store/3v8qs8h4ydmcrjjw29arzb0qk9qxqicq-message-0.17.0/bin/message-nexus`).
  PID 90762, up since 2026-09-26 17:38:33.
- `message-nexus.service` (stable, unprefixed): unit not found by systemd —
  no stable Message Nexus unit is installed under that name.
- `mcp__agent-intercom` (agent-intercom): `intercom_list` call returned
  "Intercom broker exited before startup with code 1" — the tool is
  registered but its broker is not up.

## herdr sessions (`herdr session list --json`)

- `default`: running: true (this flow's own session and most live panes).
- `recovery-56ae53`: running: true.
- `messaging-build`: running: **false** (session directory exists,
  socket not live).
- `--help`: running: false (an artifact session name, not a real target).

## messenger-clj (`hm-list`, `hm-heartbeat-state`) registration rows for
seats named in the brief

- `56ae53` (Mind Sol 56ae53): row present, `session: messaging-build`,
  `pane_id: wM:pJ`, state `Bound`. `messaging-build` is not a running herdr
  session (see above) — this is the refusal condition: the bound session is
  not registered/live, so no target-side delivery is possible over this row
  today. Route also shown STALE in `hm-list`'s own STATE column for this
  session's rows generally.
- `c56100` (Mind Sol successor c56100): row present, `session:
  recovery-56ae53`, `name: mind_sol_c56100`, `pane_id: w1:p3`, `agent:
  codex`, state `idle` in `hm-list`. Cross-checked against `herdr --session
  recovery-56ae53 pane list`: pane `w1:p3` exists, `agent_session.value ==
  01a0e0a1-7075-7cc2-928d-13fc56100504`, matching hm-heartbeat-state's
  `native_thread` for flow `c56100` exactly. Live and bound.
- `6fe957` (Mind Astra): `session: default`, `pane_id: w1:p2`, state `idle`.
  Cross-checked live in `herdr --session default pane list`:
  `agent_session.value == 01a0dfdc-a500-7271-8f54-e446fe9578dd`, matches.
  Live and bound.
- `9ac67c` (Field Sol): `session: default`, `pane_id: w1:p9`, state `idle`.
  Cross-checked live: matches `01a0e029-558a-7852-b5df-1919ac67c6d7`.
- `139366` (Mind Luna): `session: default`, `pane_id: w1:pD`, `hm-list`
  STATE `done` (not idle). Pane still present in `herdr pane list` with
  `agent_status: done`.
- `184bd8` (Field Luna): `session: default`, `pane_id: w1:p7`, state `idle`.
  Cross-checked live: matches `01a0e021-aa68-72a2-a8df-7d6184bd8c00`.

## The one send

`FLOW_ID=8904b1 hm-send c56100 "<body given in the brief, verbatim>"`

Pre-send check: `herdr --session recovery-56ae53 pane read w1:p3 --lines 40`
showed the input line as the unfilled placeholder `› Ask Codex to do
anyth[ing]` — no undimmed unsent draft was present.

Printed receipt: `Transported.{ c56100 idle }`.

Post-send observation (method: `herdr --session recovery-56ae53 pane read
w1:p3`, polled at approx. T+0:00, 0:25, 0:50, 1:15, 1:40, 2:05, 2:30 from
send):
- T+0:04s: pane status flips from idle to `Working (4s ...)` — this is the
  target harness reacting, taken as **Presented**.
- Through T+2:17 the pane continued to show `Working (Nm NNs ...)` with no
  reply text yet visible in the read buffer.
- No target-side read acknowledgment beyond the harness turning to
  `Working`, and no reply text, was observed inside the 3-minute window.
  Grade reached: **Presented**. Not upgraded to Read.
