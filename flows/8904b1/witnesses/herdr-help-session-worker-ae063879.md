## Method

Read the stopped worker's transcript (`agent-ae063879897c3608c.jsonl`, resolved
from the linked `.output` path) with `python3`/`grep`, extracting only
`tool_use`/`tool_result` records and `attachment` records by line number —
never the file whole. Cross-checked with one live `herdr session list` (no
other Herdr command run; no session subcommand run with any argument).

## 1. Every Herdr command the worker ran, in order

All times UTC, worker cwd throughout was `/home/li/wt/primary/56ae53`.

1. `05:03:12.139` `herdr` (bare, tool-check only, `commandName":"herdr"`, no output captured) — anything else / setup.
2. `05:03:22.184` `herdr --help; herdr session --help; herdr session attach --help` — help on top-level, then parent `session`, then **subcommand `attach` that takes a free name, with the help option**. Returned: top-level usage; `herdr session` subcommand list; and the **attach-specific** usage (`Usage: herdr session attach <NAME>`) — i.e. `--help` was parsed as the flag, not as a name.
3. `05:03:29.268` `herdr server --help; herdr status --help; herdr session list --help; herdr session stop --help; herdr session delete --help` — help on parent `server`/`status`, and on subcommands `stop`/`delete` that take a free name, with the help option. Each returned its own specific usage banner (`Usage: herdr session stop [OPTIONS] <NAME>`, etc.) — again flag-parsed, not name-parsed.
4. `05:03:31.265` `herdr workspace --help; herdr api --help; herdr agent --help` — help on parents. Returned proper listings.
5. `05:03:35.675` `herdr --skill | grep ...` — reading the skill file. Anything else / reading.
6. `05:03:36.720` `herdr --version; herdr session list --json; herdr status server --json; herdr status client --json` — version, listing, status. Returned session list already showing `--help` as a running session.
7. `05:04:13.376` `stat .../sessions/--help; ls .../sessions/; date` — anything else / reading (filesystem, not Herdr binary).
8. `05:04:33.688` `ps ...herdr...; ls .../sessions/--help/` — anything else / reading.
9. `05:04:41.011` `cat .../sessions/--help/herdr-server.log, herdr-client.log, session.json` — anything else / reading logs.
10. `05:05:03.841` `herdr --skill | grep ...; find / -iname "*agent-guide*"...` — reading.
11. `05:05:19.140` `herdr session list --json` — listing (run after the warning, as instructed by it).
12. `05:05:24.145` `env | grep -i herdr | sed 's/=.*/=<redacted>/'` — anything else / reading env names only.

## 2. Attach or any session subcommand with an argument, help option included

Yes: item 2 ran `herdr session attach --help`, and item 3 ran `herdr session stop --help` and `herdr session delete --help`. All three at `05:03:22.184`–`05:03:29.268`. In every case the returned banner was the **specific subcommand's own usage**, not the parent `herdr session` listing — the signature the main flow's warning gives for the bug (Sol 9ac67c's report: the buggy run got back the **parent `herdr session` listing**, not `attach`'s own text). This worker's runs show `--help` was recognized as the help flag in each case, not swallowed as `<NAME>`.

## 3. The seat's warning, before or after

Warning (`queued_command`, "Urgent correction from main flow 8904b1...") arrived at `05:05:14.136`. All the help-with-argument commands (item 2 and 3 above) ran at `05:03:22`–`05:03:29`, i.e. **before** the warning, under the original brief that called such reads safe. After the warning the worker ran only one more `herdr session list --json` (05:05:19) and an env-name grep (05:05:24), then was interrupted/stopped at `05:06:25.137` — it did not run any further session subcommand with an argument.

## 4. Sessions now (`herdr session list`, one call, run by this witness)

    name              status    directory
    default           running   /home/li/.config/herdr
    --help            running   /home/li/.config/herdr/sessions/--help
    messaging-build   stopped   /home/li/.config/herdr/sessions/messaging-build
    recovery-56ae53   running   /home/li/.config/herdr/sessions/recovery-56ae53

Only `--help` is a name that is a help option. Not acted on. No creation timestamp in the listing itself.

## 5. When the accidental session was made, and attribution

The worker itself read `stat` on the session directory (05:04:13): birth
`2026-09-26 23:03:35.494236451 -0600` = `2026-09-27T05:03:35.494Z`. The
session's own `herdr-server.log` (read by the worker at 05:04:41) confirms:
`2026-09-27T05:03:35.496153Z INFO ... api server listening path=.../sessions/--help/herdr.sock`, and
`2026-09-27T05:03:35.557122Z INFO herdr::server::headless: created startup workspace cwd=/home/li/wt/primary/field-packet-56ae53`.

**Observation:** this creation time (05:03:35.49x) falls inside the stopped
worker's run window (05:03:07–05:06:25), so time alone does not clear it.

**Observation:** the session's own startup log records its workspace `cwd` as
`/home/li/wt/primary/field-packet-56ae53`. The stopped worker's transcript
shows `"cwd":"/home/li/wt/primary/56ae53"` on every single record, with no
other cwd value anywhere in the file (grep confirms only one distinct cwd
across the whole transcript) and no `cd` to, or other reference to, a
`field-packet-56ae53` checkout except the three appearances of that string
inside the server-log text the worker later `cat`-read (i.e. text it observed
about someone else's process, not text describing its own).

**Inference:** the session directory's workspace `cwd` records where the
process that created it was running from. The stopped worker never ran from
`field-packet-56ae53`. A different process, in a different working copy,
created the `--help` session at essentially the same time this worker was
independently running its own (correctly-flag-parsed) help commands.

**Inference, from item 2/3 above:** this worker's own `attach`/`stop`/`delete`
`--help` invocations each returned the specific subcommand's own usage text,
not the parent `herdr session` listing that Sol 9ac67c's report says the
triggering run returned. That is the opposite signature from the one
attributed to the bug.

**Unknown:** which of the other two named helpers (or some third process
entirely) ran the buggy `field-packet-56ae53`-cwd command, and its exact
text/time — outside this transcript, not investigated here per scope.

## 6. Anything else not reading

None found. No `Write`, `WebFetch`, or process-start tool call appears in the
transcript (only `Bash`, `Read`, `Skill`, `TodoWrite` tool names occur); the
`Bash` calls are all either `herdr` invocations or local read-only inspection
(`stat`, `ls`, `ps`, `cat` of logs, `find`, `env|grep`, `date`). No file
written by the worker other than this witness (written by the investigating
flow, not the worker itself).

## Verdict

The stopped worker did **not** bring the accidental `--help` session into
being. Its own three help-with-argument invocations (`attach`, `stop`,
`delete`, each with `--help`) all returned the correct subcommand-specific
usage text — the opposite of the parent-listing signature reported for the
actual trigger — and its transcript shows only one cwd
(`/home/li/wt/primary/56ae53`) throughout, never the `field-packet-56ae53`
cwd recorded in the accidental session's own startup log. The creation time
does fall inside the worker's run window, so time of day alone cannot clear
it; the cwd mismatch and the correct help-parsing are what clear it.
