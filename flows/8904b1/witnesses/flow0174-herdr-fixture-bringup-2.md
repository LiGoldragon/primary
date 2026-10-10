# Witness: Flow 0.17.4 test Herdr fixture bring-up, second attempt — refused at attach

Method: direct shell commands (Bash tool) run interactively against the live
host, in this same working copy, on 2026-09-26, using Field Sol's shorter
recipe (session name `f17-9ac67c`, root `/home/li/.cache/f17-9ac67c`). No
step was simulated; every command shown was actually executed and its real
output captured.

## Step 1 — context, read-only (HELD)

Own-environment Herdr vars (`env | grep -i herdr`): `HERDR_PANE_ID=w1:p8`,
`HERDR_TAB_ID=w1:t6`, `HERDR_WORKSPACE_ID=w1`,
`HERDR_BIN_PATH=/nix/store/9x03bz0q0a978zrzcshrlmmb4fvcmdb6-herdr-0.8.2/bin/herdr`,
`HERDR_ENV=1` (the inside-a-pane marker), `HERDR_SOCKET_PATH=/home/li/.config/herdr/herdr.sock`
(live default socket). `HERDR_CONFIG_PATH` unset. `$HOME=/home/li`.
`script -qec "tty" /dev/null` printed `/dev/pts/15`, exit 0 — `script` supplies
a real pty.

Baseline processes (`ps -eo pid,ppid,lstart,cmd`):
- PID 4957 (ppid 4953) `herdr server`, started Sat Sep 26 16:19:49 2026 —
  the **default** session's server.
- PID 301649 (ppid 1916) `herdr server`, started Sat Sep 26 19:59:03 2026 —
  the **recovery-56ae53** session's server.

Own-env `herdr session list`: `default` (running), `--help` (stopped, the
trap, untouched), `messaging-build` (stopped), `recovery-56ae53` (running).
Own-env `herdr agent list`: 10 agents (counted from the JSON array), matching
the roster seen in this flow's own context (primary, field-luna-19ff9f,
mind-astra-6fe957, field-luna-184bd8, this flow psyche_fable_b7ba00,
field-sol-9ac67c, field-astra-22e12b, psyche_opus_dc53b4, mind-luna-139366,
psyche_sonnet_9c7514).

## Step 2 — scratch directories (HELD)

Root `/home/li/.cache/f17-9ac67c` did not exist. Created `home`, `run`
(mode 0700, verified by `stat -c '%a'` = 700), and `config`, nothing else.
All three absolute and under the root:
`/home/li/.cache/f17-9ac67c/{home,run,config}`. None is, is inside, or
contains: the live config home (`/home/li/.config/herdr`), the live runtime
dir (`/run/user/1001`), any live session directory, or the earlier scratch
root `/home/li/.cache/field-herdr-fixture/flow0174-test-8904b1` (confirmed
to still exist; not read into, not reused, not removed).

## Step 3 — the addressing, witnessed before anything is controlled (HELD)

Under the recipe's environment (`HOME`, `XDG_RUNTIME_DIR`, `XDG_CONFIG_HOME`
set to the three scratch dirs; `HERDR_SOCKET_PATH`/`HERDR_CONFIG_PATH`
unset), `herdr session list` returned only:
```
default   stopped   /home/li/.cache/f17-9ac67c/config/herdr   /home/li/.cache/f17-9ac67c/config/herdr/herdr.sock
```
No live session name or live path appeared. This is the expected
scratch-local auto-materialized `default` record, stopped, wholly under the
scratch root — not a block.

Expected test-session socket path:
`/home/li/.cache/f17-9ac67c/config/herdr/sessions/f17-9ac67c/herdr.sock`.
Exact length by `wc -c`: **70 bytes**, well inside the 107-usable-byte
`sockaddr_un` limit.

## Step 4 — the attach, once (REFUSED, exact block recorded)

Ran, once, under the recipe's environment and a pty from `script`:
```
script -qec "herdr session attach f17-9ac67c" <logfile>
```
in the background, disowned, retaining it by its own process identity.
Full captured output:
```
error: nested herdr is disabled by default.
see configuration if you want to enable it.

"recursive descent denied. there is, in fact, such a thing as too much herdr."
```
Exit code 1. The `script` wrapper itself exited immediately once the
wrapped command exited (confirmed: no `script` or `herdr session attach
f17-9ac67c` process present in `ps` afterward). No test-session server was
ever started; no pty client survives. This is the refusal the brief
anticipated for a caller whose environment marks it as inside a pane
(`HERDR_ENV=1`). Per instruction, `HERDR_ENV` was not removed or altered to
get past it, and the attach was run once, with no retry.

## Steps 5–7 — not reached

No test session came up, so there is nothing to read back (step 5), and
step 6's "unchanged" check applies to the baseline already true throughout
(re-verified below), not to any new state. Step 7: nothing was started that
is still alive; no stop command applies.

## Live sessions: re-verified unchanged after the attempt

`ps` for PID 4957 and 301649: same processes, same `lstart` values as
baseline. Own-env `herdr session list`: identical four rows as baseline.
Own-env `herdr agent list`: still 10 agents. No signal was sent to any
pre-existing process; no file was removed; nothing was edited outside the
three newly created scratch directories under `/home/li/.cache/f17-9ac67c`.

## Disposition

Steps 1–3: held, with the socket length (70 bytes) well under the limit —
no block this time, unlike the first attempt's 110-byte path. Step 4: run
once as instructed; refused by Herdr's own nested-launch guard, in the
exact words above. Steps 5–7: not reached; nothing is left running beyond
what was already running before this task.
