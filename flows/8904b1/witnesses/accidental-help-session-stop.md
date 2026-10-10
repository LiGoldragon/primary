# Witness: stopping the accidental `--help` Herdr session

Method: read-only observation before and after one control command. Step 1
readback used `stat`, `ss -xlp`, `ps`, `herdr agent list` and `env`, no
Herdr command naming the accidental session. Step 2 ran three read-only
Herdr commands (`herdr status`, `herdr agent list`, `herdr workspace list`)
under `env -u HERDR_SESSION -u HERDR_CLIENT_SOCKET_PATH
HERDR_SOCKET_PATH=/home/li/.config/herdr/sessions/--help/herdr.sock`, full
path only, no session name as an argument. Step 3 ran exactly one control
command, once, under the same environment, with a 60s timeout. Step 4
repeated read-only observation. Nothing was signaled; no file was removed;
no other Herdr command (start/attach/delete/close/prompt/focus) was run.

## Step 1 — baseline readback
- `/home/li/.config/herdr/sessions/--help/herdr.sock` and the companion
  `herdr-client.sock`: confirmed Unix sockets (`stat`), both srw-------,
  owner li:users, in the same directory.
- `ss -xlp`: both sockets listened on by PID 528364 (`herdr server`),
  started `Sat Sep 26 23:03:35 2026`. One child, PID 528406 (`zsh`), same
  start time, itself childless — matches the census exactly.
- Baseline recorded: default session server PID 4957, started
  `Sat Sep 26 16:19:49 2026`; recovery-56ae53 server PID 301649, started
  `Sat Sep 26 19:59:03 2026`. Both listening on their own sockets
  (`/home/li/.config/herdr/herdr.sock`, `.../recovery-56ae53/herdr.sock`).
- `herdr agent list` (own environment): 10 agents, matching census identity
  list (codex/claude agents including field-sol-9ac67c, psyche_fable_b7ba00,
  etc.), all under workspace `w1`.
- Own environment's Herdr variables: `HERDR_SOCKET_PATH=/home/li/.config/herdr/herdr.sock`
  (default session), `HERDR_PANE_ID=w1:p8`, `HERDR_TAB_ID=w1:t6`,
  `HERDR_WORKSPACE_ID=w1`, `HERDR_BIN_PATH=...`, `HERDR_ENV=1`.
  `HERDR_SESSION` and `HERDR_CLIENT_SOCKET_PATH` were not set.
- No mismatch from the census. Proceeded.

## Step 2 — addressing witness, read-only, under the stop environment
All three run under
`env -u HERDR_SESSION -u HERDR_CLIENT_SOCKET_PATH HERDR_SOCKET_PATH=/home/li/.config/herdr/sessions/--help/herdr.sock`:

- `herdr status` → server socket reported as
  `/home/li/.config/herdr/sessions/--help/herdr.sock` (exit 0).
- `herdr agent list` → `{"agents":[],"type":"agent_list"}` (exit 0) — zero
  agents.
- `herdr workspace list` → one workspace `w1`, one tab, one pane, label
  `field-packet-56ae53` (exit 0) — matches the census's single bare pane.

Unmistakably the accidental session's server answered: zero agents, one
bare workspace, and the socket path itself echoed back in `status` matches
`/home/li/.config/herdr/sessions/--help/herdr.sock`. Not the default
session's 10-agent answer, not recovery's. Proceeded to step 3.

## Step 3 — the one control command
Ran once, exactly:

    env -u HERDR_SESSION -u HERDR_CLIENT_SOCKET_PATH HERDR_SOCKET_PATH=/home/li/.config/herdr/sessions/--help/herdr.sock herdr server stop

Under a 60-second timeout. Output: empty stdout/stderr. Exit status: `0`.
No retry.

## Step 4 — witness afterward
- `ps -p 528364,528406`: no such processes — both gone.
- `ss -xlp | grep sessions/--help`: no listener on either target socket.
- Default session server: PID 4957, started `Sat Sep 26 16:19:49 2026` —
  unchanged. Recovery session server: PID 301649, started
  `Sat Sep 26 19:59:03 2026` — unchanged. Both match the step 1 baseline
  exactly.
- `herdr agent list` (own environment): 10 agents, same identities as
  baseline (field-luna-19ff9f, mind-astra-6fe957, field-luna-184bd8,
  psyche_fable_b7ba00, field-sol-9ac67c, field-astra-22e12b,
  psyche_opus_dc53b4, mind-luna-139366, psyche_sonnet_9c7514, plus one
  unnamed codex agent) — unchanged.
- `herdr session list`:
  - `default` — running — `/home/li/.config/herdr`
  - `--help` — **stopped** — `/home/li/.config/herdr/sessions/--help`
  - `messaging-build` — stopped (unchanged)
  - `recovery-56ae53` — running — unchanged
- `/home/li/.config/herdr/sessions/--help/` directory: still present.
  Contents after stop: `herdr-client.log`, `herdr-server.log`,
  `session.json` (the two socket files were removed by the server's own
  clean shutdown, not by this witness — nothing was deleted by this flow).
  Nothing was removed by this flow.
