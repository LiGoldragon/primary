# Post-stray-start check on the live stable Flow service and store

Subflow of 8904b1, read-only, 2026-09-26. Method: `systemctl --user
status`/`show` (read-only), `journalctl --user`/`journalctl` (read-only),
`ps -ef`, `ls -la`/`stat`/`sha256sum` on store/socket files (content of
`flow.sema` never opened, only size/mtime/hash), one ordinary read-only
`flow 'List.{ }'` client query against the live stable socket, and
`grep`/`Read` of already-fetched source at
`/git/github.com/LiGoldragon/flow` (`crates/flow-nexus/src/main.rs`) — no
Flow or Message service binary executed with any argument. Labels: **O**
observed, **I** inference.

## 1. The service (O)

`flow-nexus.service` (user unit): active/running since **2026-09-26
16:19:37 CST**, invocation `e772cdb5...`, `NRestarts=0`, Main PID **1937**
running `/nix/store/.../flow-0.12.2/bin/flow-nexus`. This start predates
the worker's stray attempt (~half hour before this check, i.e. ~21:48) by
over 5 hours; no restart is recorded across that window. `ps -ef` shows
exactly one `flow-nexus` process for the stable service (PID 1937) — no
stray second process from the worker's attempt remains running.

## 2. The stray attempt (O, then I)

No entry for it appears in `journalctl --user -u flow-nexus.service`
(only the original "Started Flow Nexus" line) or in the system journal
searched for "flow" since 21:30. Inference (I): the stray process was run
directly in the worker's own shell, not under systemd, so its stdout
("Database already open. Cannot acquire lock.") went to that pane, not to
journald — its absence from the journal is expected, not evidence it
didn't happen. Both live sockets' mtimes (below) predate the stray
window, so it did not reach a bind/replace attempt on either socket.

## 3. The store (O)

`/home/li/.local/state/flow/flow.sema`: **1,056,768 bytes**, mtime
**2026-09-26 18:22:10**, SHA-256 **f03f610a9832...c78c0f03** — byte-for-byte
matching Sol 56ae53's earlier-today record (size and hash prefix exact).
Mtime is well before the stray attempt window and unchanged since; the
attempt's own "lock refused" exit is consistent with no write. Directory
listing shows only `flow.sema`, `launch-bundles/` (mtime 11:24, unrelated),
`recovery-gcroots/` (mtime 19:14, unrelated) — no `.tmp`, `.lock`, `-wal`,
`-journal`, or other stray file beside the store.

## 4. The rows (O)

`flow 'List.{ }'` answered live with `Listed.[ ... ]`: **25** top-level
rows — matching 56ae53's earlier count today.

## 5. The next service and store, briefly (O)

`flow-nexus-next.service`: active/running, one process, PID 90750,
`flow-0.17.1`, started 17:38. Sockets
`/run/user/1001/flow-next/flow/{flow,flow-meta}.sock` mtime 17:38 (start
time, unchanged). Store
`/home/li/.local/state/flow-next/.local/state/flow/flow.sema`: 581,632
bytes, mtime 20:30 (ordinary write, well before the stray window). No
stray file beside it. The stray attempt used only the default
stable-store paths (per its own account and source below) and did not
reach the next instance's paths.

## 6. How the binary decides to start (O, from source)

`crates/flow-nexus/src/main.rs`, `version_answer`: only the exact
single-argument vector `["--version"]` short-circuits (prints the crate
version, exits 0, no configuration read). Every other argument vector —
including `--help`, no arguments, or `--version` plus anything else —
falls through to `DefaultConfiguration::from_environment()` and starts
the Nexus (opens/creates the default store, binds the default sockets).

## Verdict

**Unharmed.** The live stable `flow-nexus.service` (PID 1937, running
since 16:19:37, zero restarts) and its store (`flow.sema`, size and
SHA-256 prefix identical to this morning's record, mtime 18:22, no stray
file beside it) show no effect from the stray attempt: its own
"Database already open. Cannot acquire lock." exit is corroborated by
the store's unchanged mtime/hash and the live sockets' unchanged mtimes
(the stray process never got far enough to touch either). No stray
`flow-nexus` process remains. The read-only List query answers with the
expected 25 rows. The next service and store are likewise untouched and
were never in the stray attempt's default path.

## Sources

- `systemctl --user status flow-nexus.service`, `systemctl --user show
  flow-nexus.service -p ActiveEnterTimestamp,MainPID,...` (read-only).
- `journalctl --user -u flow-nexus.service --since "2026-09-26 16:00"`;
  `journalctl --since "2026-09-26 21:30"` filtered for "flow" (read-only).
- `ps -ef | grep flow-nexus` (read-only).
- `stat`, `sha256sum`, `ls -la` on `/home/li/.local/state/flow/flow.sema`
  and its directory; on `/run/user/1001/flow/` and
  `/run/user/1001/flow-next/flow/`; on
  `/home/li/.local/state/flow-next/.local/state/flow/flow.sema` and its
  directory.
- `flow 'List.{ }'` (ordinary client, read-only List request).
- `/git/github.com/LiGoldragon/flow/crates/flow-nexus/src/main.rs`
  (`version_answer`, already-fetched local clone).
- `flows/8904b1/witnesses/flow-0174-stage-one-readiness.md` (worker's own
  account, used only for the stray attempt's claimed time/paths, not
  taken as proof of the store/service state — that is independently
  checked above).
