# Witness: Flow 0.17.4 test Herdr fixture bring-up — blocked at socket-length check

Method: direct shell commands (Bash tool) run interactively against the live
host, in this same working copy, on 2026-09-26. No file simulated; every
command shown was actually executed and its real output captured. This
witness stops before step 4 of the recipe (the attach) because step 3's
socket-length check did not hold.

## Step 1 — context, read-only (HELD)

Own-environment Herdr variables, from `env | grep -i herdr`:
- `HERDR_PANE_ID=w1:p8`, `HERDR_TAB_ID=w1:t6`, `HERDR_WORKSPACE_ID=w1`
- `HERDR_BIN_PATH=/nix/store/9x03bz0q0a978zrzcshrlmmb4fvcmdb6-herdr-0.8.2/bin/herdr`
- `HERDR_ENV=1` — the "inside a pane" marker referenced by the brief.
- `HERDR_SOCKET_PATH=/home/li/.config/herdr/herdr.sock` (live default socket)
- `HERDR_CONFIG_PATH`: unset
- `$HOME=/home/li`

`script` is present at `/run/current-system/sw/bin/script` and supplies a
real pty: `script -qec "tty" /dev/null` printed `/dev/pts/15`, exit 0.

Baseline processes (`ps -eo pid,ppid,lstart,cmd | grep -i herdr`):
- PID 4953 (ppid 4736, a login zsh) = `herdr session attach default`, started
  Sat Sep 26 16:19:49 2026.
- PID 4957 (ppid 4953) = `herdr server`, started Sat Sep 26 16:19:49 2026 —
  the **default** session's server. `/proc/4957/cwd` -> `/home/li`;
  `/proc/4957/environ` has no `HERDR_SESSION` (default).
- PID 301649 (ppid 1916, the user systemd) = `herdr server`, started Sat Sep
  26 19:59:03 2026 — the **recovery-56ae53** session's server, confirmed by
  `/proc/301649/environ` containing `HERDR_SESSION=recovery-56ae53` and
  `/proc/301649/cwd` -> `/home/li/primary`.

`herdr session list` (own env):
```
name                 status   directory                                        socket
default              running  /home/li/.config/herdr                           /home/li/.config/herdr/herdr.sock
--help               stopped  /home/li/.config/herdr/sessions/--help           /home/li/.config/herdr/sessions/--help/herdr.sock
messaging-build      stopped  /home/li/.config/herdr/sessions/messaging-build  /home/li/.config/herdr/sessions/messaging-build/herdr.sock
recovery-56ae53      running  /home/li/.config/herdr/sessions/recovery-56ae53  /home/li/.config/herdr/sessions/recovery-56ae53/herdr.sock
```
Confirms the live `--help` trap session exists, stopped; not touched.

`herdr agent list` (own env): returned 10 agents (counted from the JSON
`agents` array): pane w1:p1 codex "primary" (working); w1:p3 codex
field-luna-19ff9f (done); w1:p2 codex mind-astra-6fe957 (done); w1:p7 codex
field-luna-184bd8 (done); w1:p8 claude psyche_fable_b7ba00 — this flow
(working); w1:p9 codex field-sol-9ac67c (idle, focused); w1:pA codex
field-astra-22e12b (done); w1:pC claude psyche_opus_dc53b4 (done); w1:pD
codex mind-luna-139366 (done); w1:pF claude psyche_sonnet_9c7514 (done).

## Step 2 — scratch directories (HELD)

Root `/home/li/.cache/field-herdr-fixture/flow0174-test-8904b1` did not
exist (`ls` returned "No such file or directory"). Created:
- `/home/li/.cache/field-herdr-fixture/flow0174-test-8904b1/home`
- `/home/li/.cache/field-herdr-fixture/flow0174-test-8904b1/run` (mode 0700)
- `/home/li/.cache/field-herdr-fixture/flow0174-test-8904b1/config`

All three are absolute, all three sit under the scratch root, and none of
them is, contains, or is contained by: the live config home
(`/home/li/.config/herdr`), the live runtime dir (`/run/user/1001`, from
the pre-existing `$XDG_RUNTIME_DIR`), or any live session directory
(`/home/li/.config/herdr/sessions/{--help,messaging-build,recovery-56ae53}`).
No path-prefix overlap in either direction.

## Step 3 — the addressing, witnessed before anything is controlled (BLOCKED)

Under the recipe's environment (`HOME`, `XDG_RUNTIME_DIR`, `XDG_CONFIG_HOME`
set to the three scratch dirs above; `HERDR_SOCKET_PATH` and
`HERDR_CONFIG_PATH` unset), `herdr session list` returned:
```
name                 status   directory                                        socket
default              stopped  .../flow0174-test-8904b1/config/herdr           .../flow0174-test-8904b1/config/herdr/herdr.sock
```
(paths abbreviated; full root shown above). This is not `default` the live
session — its directory and socket are both freshly created under the
scratch `config/`, not under `/home/li/.config/herdr`. No live session name
(`default`, `recovery-56ae53`, `--help`, `messaging-build`) with a live path
appeared. The addressing check on its own holds: the recipe environment
reaches only scratch configuration, auto-materialized on first read by
Herdr itself, empty of anything but its own scratch-native "default" entry.

**However**, the socket-path-length half of step 3 does not hold. Herdr's
own naming scheme, read back from this same listing and from the live
listing's pattern for a named session (`.../herdr/sessions/<name>/herdr.sock`,
seen live for `recovery-56ae53` and `messaging-build`), gives the test
session's socket path as:
```
/home/li/.cache/field-herdr-fixture/flow0174-test-8904b1/config/herdr/sessions/flow0174-test-8904b1/herdr.sock
```
Length: **110 characters**. The brief's own limit is "about a hundred
characters"; the standard Linux `sockaddr_un.sun_path` capacity is 108
bytes including the terminating NUL, i.e. at most 107 usable characters.
110 exceeds both. Per the brief's explicit instruction — "if a socket path
under it would exceed the limit, that is a block to report, not to work
round by choosing another root" — this is a block, not a thing to route
around.

**Stopped here.** Steps 4 through 7 (the attach, the readback, the
live-unchanged check, and what-is-left-running) were **not reached**. No
`herdr session attach` was run under the recipe environment. No pty client,
no test-session server, no shell in it was started. Nothing was signaled,
removed, or altered outside the three freshly created (empty, unpopulated
beyond Herdr's own auto-write) scratch directories.

## Live sessions: unaffected

Only read-only commands (`session list`, `agent list`, `ps`, `/proc` reads)
were run against the live configuration at any point; the one write
performed anywhere was `mkdir`/`chmod` strictly under the scratch root, and
the one non-read Herdr invocation was `herdr session list` under the
*scratch* environment, which by Herdr's own behavior appears to have
lazily written a fresh scratch-local `config/herdr` directory and a
stopped scratch-local `default` entry — entirely inside the scratch root,
never touching `/home/li/.config/herdr`. No signal was sent to PID 4957,
301649, 4953, or any live agent pane.

## Disposition

Step 1: held. Step 2: held. Step 3: held on the addressing half, did not
hold on the socket-length half — **block**. Steps 4–7: not reached, per the
brief's own instruction to stop at the first thing that does not hold.

Nothing is left running beyond what was already running before this task
(the pre-existing default and recovery-56ae53 servers, and this flow's own
pane/session). No stop command applies because no test-session server was
ever started.
