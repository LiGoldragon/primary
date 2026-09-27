# Witness: census of the accidental `--help` Herdr session

Method: read-only. Ran only `herdr session list`, `herdr status`, `herdr agent
list`, `herdr workspace list` (no session name given to any of them). Located
the session's on-disk directory by listing its parent
`/home/li/.config/herdr/sessions/` and then reading files under the exact
path `/home/li/.config/herdr/sessions/--help/` given as a full path (never a
bare word), using `stat`/`ls`/`Read`, never a Herdr command. Identified its
server/client/pane processes from its own log files, then looked those PIDs
up in the process table (`ps`) and the listening-socket table (`ss -xlp`),
read-only. Checked `journalctl --user` for the creation window and the
default session's own `herdr-server.log` for the same UTC window, read-only.
No socket was opened for writing; no Herdr session/attach/stop/delete command
was run; nothing was signaled, stopped, or messaged.

## 1. Session listing
`herdr session list` output, verbatim names:
- `default` — running — dir `/home/li/.config/herdr` — socket `/home/li/.config/herdr/herdr.sock`
- `--help` — running — dir `/home/li/.config/herdr/sessions/--help` — socket `.../--help/herdr.sock`
  (spelled out: two hyphens followed by the word "help")
- `messaging-build` — stopped — dir `.../sessions/messaging-build`
- `recovery-56ae53` — running — dir `.../sessions/recovery-56ae53`

## 2. Identity on disk
Directory `/home/li/.config/herdr/sessions/--help/`: mode 0700, owner `li:users`,
birth 2026-09-26 23:03:35.494 -0600, modify 2026-09-26 23:03:40.558 -0600.
Contents: `herdr-client.log` (368B, file), `herdr-client.sock` (0B, socket),
`herdr-server.log` (2882B, file), `herdr.sock` (0B, socket, exists), `session.json`
(816B, file, birth 23:03:40.558). All files mode 0600 except sockets (0600 srw).

## 3. Server
`ss -xlp` shows `herdr.sock` and `herdr-client.sock` both listened on by
PID 528364 (`herdr server`), a **separate** server process from the default
session's server (PID 4957) and from `recovery-56ae53`'s server (PID 301649).
PID 528364 started 2026-09-26 23:03:35, parent PID 1916 (`systemd --user`) —
same reparenting pattern as `recovery-56ae53`'s server, i.e. an ordinary
detached daemon, not evidence of anomaly by itself.

## 4. What it holds
One child of 528364: PID 528406, `/run/current-system/sw/bin/zsh`, started
23:03:35, itself childless (idle shell, no agent attached). Its own
`session.json` records exactly one workspace (`w1`), one tab, one pane, cwd
`/home/li/wt/primary/field-packet-56ae53` — a bare pane, no agent record.
`herdr agent list` (run against the default session) attributes zero agents
to it; all 10 listed agents belong to `default`'s workspace `w1`.
Seats: none. Workspaces: one bare pane (no agent). Processes: one idle shell only.

## 5. Creation time and correlation
Session birth 2026-09-26 23:03:35.494 -0600 (=2026-09-27T05:03:35.494Z per
its own log). The default session's own server log has no request logged in
that exact second (nearest entries 05:02:56 and 05:03:40, both ordinary
`agent.prompt` calls) — the accidental session was not created through the
default server's API. `journalctl --user` in that window shows only an
unrelated, already-failing `opencode-testing.service` restart loop and gpg-agent
ssh-handler noise; nothing names a process or user. No shell history was read.
**Unknown**: which flow/process actually invoked `herdr session ... --help`.

## 6. Real sessions, unchanged
`default`: running. `recovery-56ae53`: running. `messaging-build`: stopped.
`default` agent count (`herdr agent list`): 10 agents.
