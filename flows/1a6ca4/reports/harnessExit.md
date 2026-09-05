# Harness exit at 04:08 on 2026-09-05

Read-only investigation of why the Claude Code process hosting flow 1a6ca4
(session `1a6ca4f9-e0fa-4f2c-bd6f-a40651590354`) disappeared and stayed gone
until the living resumed it at 10:39. Investigating thread: subagent
`a9cbcf75a4fad0e84` of the resumed process. Times below are local (CEST,
UTC+2); transcript records carry UTC and are given as `Z` where quoted.

## Observations

### Timeline

| Time (CEST) | Event | Source |
|---|---|---|
| 00:52:30 | systemd --user starts `app-ghostty-surface-transient-3762188.scope` (a ghostty terminal surface running zsh 3762188) | `journalctl --user` |
| 00:52:38 | The 1a6ca4 claude process starts (version 2.1.258) | main transcript line 614, `cost-state.startTime` 1788562358035 |
| 03:31:14 | Lock screen unlocked by the living | `journalctl --user` (noctalia, niri) |
| 04:00:17 / 04:00:39 | Background subagents a049784d (ethos-zero second pass) and affd462f (protos/datomic audit) spawned | tasks dir symlink mtimes; subagent transcripts line 1 (`02:00:17Z`, `02:00:39Z`) |
| 04:00:52 | Commit 8516098f7 | `git log` |
| 04:00:59 | Main flow's turn ends (`stop_reason: end_turn`), `turn_duration` with `pendingBackgroundAgentCount: 2` | main lines 609-610 (`02:00:59Z`) |
| 04:03:26 | affd462f starts `nix flake check` in the background (task bbzsywg9d) | affd462f line 98 |
| 04:03:40 / 04:04:06 | bbzsywg9d completion enqueued to main, then removed with reason `absorbed_mid_turn` | main lines 611-612 |
| 04:04:44 | Last a049784d record before the exit: a tool_result (curl to crates.io); no assistant record follows | a049784d line 132 (`02:04:44Z`) |
| 04:05:05 | affd462f writes `scratchpad/adv2/tests/deep.rs` (19 tests nesting 100,000 brackets / chain links / datoms) and runs them one per process in a debug build (`[profile.dev] opt-level = 0`), foreground Bash, 600 s tool timeout, `timeout 300` per test | affd462f line 109 |
| 04:05:06 | Test binary `target/debug/deps/deep-506aa60031e4f38d` built | file mtime in `scratchpad/adv2` |
| 04:05:48 - 04:08:18 | `systemd-journald: Under memory pressure, flushing caches` (11 times) | `journalctl -k` |
| 04:07:22 - 04:08:18 | pipewire buffer underruns; at-spi2 disables an unresponsive app; noctalia frame callback took 63.3 s | `journalctl --user` |
| 04:08:18 | Kernel: `Out of memory: Killed process 3921404 (deep-506aa60031) total-vm:81477184kB, anon-rss:23906524kB`, `task_memcg=/user.slice/user-1001.slice/user@1001.service/app.slice/app-ghostty-surface-transient-3762188.scope`; `Free swap = 0kB` of `Total swap = 41641720kB`; RAM 8258767 pages (about 31.5 GB) | `journalctl -k` |
| 04:08:18 | systemd --user: `app-ghostty-surface-transient-3762188.scope: The kernel OOM killer killed some processes in this unit.` | `journalctl --user` |
| 04:08:18 - 04:08:21 | `claude remote-control` (pid 1637794) redraws its status, `Capacity: 0/32` (it also redrew at 03:08:56) | `journalctl --user _PID=1637794` |
| 04:08:19.262 / 04:08:19.381 | Two `cost-state` records and two `last-prompt` records written by the old process (computed from `startTime + totalDuration`); `totalCostUSD` 206.16 | main lines 613-617 |
| 04:08:19.451 | affd462f tool_result: `Exit code 137`, output ends at `--- d1b` after `d1_` passed in 59.50 s | affd462f line 110 (`02:08:19.451Z`) |
| 04:08:19.479 | affd462f attachment `remote_session_change` with `url: null` -- the last record written by the old process anywhere | affd462f line 111 |
| 04:08:19.484 / 04:08:19.896 | Session `tasks/` dir and `~/.claude/telemetry/` dir modified (an entry created or removed) | dir mtimes |
| 04:09:48 | systemd --user: `Stopping timed out. Killing.`, `Killing process 3762188 (zsh) with signal SIGKILL.`, `Failed with result 'oom-kill'.`, `Consumed 18min 6.610s CPU time over 3h 17min 17.922s wall clock time, 23.5G memory peak, 25.7G memory swap peak.` | `journalctl --user` |
| 04:29 - 05:09 | Codex flow acf06f keeps working (rollout files written until 05:09:14) and commits 1eaec714b 04:49:31, 69c8446a7 05:04:16, fb30f53f0 05:06:18 | `~/.codex/sessions/2026/09/05`, `git log` |
| 04:08 - 10:39 | No record in any Claude transcript under `~/.claude/projects/-home-li-primary/`; the other Claude flows' last records before the exit were 7fba5f 01:13, e996e8 01:09, 58a86d 02:16 (all before the exit) | transcript timestamps |
| 10:39:19 | New claude process 4027731 starts under zsh 4027617 (ghostty), version 2.1.261 | `ps -o lstart`, `~/.claude/sessions/4027731.json` |
| 10:39:26 | Resume notification: `No completion record was found for 2 background agents from the previous session ... they may have been running when the previous Claude Code process exited` | main line 618-620 (`08:39:26Z`) |
| 10:39:54 / 10:39:57 | Both subagents resumed by coordinator message | a049784d line 134, affd462f line 112 |

### Transcript state at the exit

- Main transcript: last timestamped record of the old process is the
  `queue-operation remove` at 04:04:06 (line 612). No assistant, user, or
  API request record exists between 04:00:59 and the resume. No record of
  any kind carries an error, `isApiErrorMessage`, "usage limit", "rate
  limit", "resets at", "You've hit", "overloaded", or a 5xx status. The last
  assistant record (line 609) has `stop_reason: end_turn`, 202,233 cached
  input tokens, normal usage. The `total_tokens` reminder before it read
  14,990,116 tokens left.
- a049784d (ethos-zero): 141 lines; last pre-exit record is a normal
  tool_result at 04:04:44; the turn was open (an API call was owed) when
  the process ended. No error records.
- affd462f (audit): 135 lines; the pre-exit tail is the `Exit code 137`
  tool_result at 04:08:19.451 followed by the `remote_session_change`
  attachment. No API error records.
- The subagent JSONL files under
  `~/.claude/projects/-home-li-primary/1a6ca4f9-.../subagents/` now carry
  post-resume records (mtimes 10:40), so their file mtimes no longer witness
  the exit; the record timestamps do.
- No Claude transcript on the machine contains a usage-limit or rate-limit
  message in the window. The only "rate limit" hits anywhere are quoted
  documentation text (58a86d line 55 at 00:39 local; main line 380 at
  01:27 local) and this brief's own wording (main lines 665-666).

### System state

- One boot since 2026-08-19 20:29; no suspend, resume, or `PM:` entries; no
  systemd-logind session change for user li; no NetworkManager entries
  between 03:50 and 04:20.
- One and only one kernel OOM event on 2026-09-05: the one at 04:08:18.
  Only one process was killed by the kernel: pid 3921404,
  `deep-506aa60031e4f38d` (the kernel truncates the name to 15 chars). The
  oom-killer was invoked by a `tokio-rt-worker` thread of the Codex
  app-server (tgid 3137277) page-faulting; that process was not killed.
- `systemd-oomd` logged nothing.
- The systemd user manager reports `DefaultOOMPolicy=stop` and
  `DefaultTimeoutStopUSec=1min 30s`. A sibling live ghostty scope
  (`app-ghostty-surface-transient-1013091.scope`) shows `OOMPolicy=stop`,
  `KillMode=control-group`, `KillSignal=15`, `TimeoutStopUSec=1min 30s`.
- The old process is gone; `ps` shows twelve other `claude` processes
  started 2026-09-02 to 2026-09-05 00:41 still alive under other ghostty
  surfaces, and the new 1a6ca4 process from 10:39:19.
- `~/.claude/debug/` has no log newer than 2026-09-04 21:33; nothing under
  `~/.cache/claude*` or `~/.local/state/claude*`. `~/.claude/sessions/` has
  no entry for the old pid.
- The claude binary is `claude-code-2.1.261` from the nix profile; the old
  process reported 2.1.258 in every record until its end, the new process
  2.1.261.

## Inferences (the flow's own)

1. The chain of causation, in order:
   the affd462f audit ran a debug-build test (`d1b_brackets_99999_delineate`,
   `brackets(99_998).protosize()`) whose live allocation exceeded RAM and
   the whole 41.6 GB of swap; the kernel killed that test binary at
   04:08:18; because the binary lived inside the ghostty surface's transient
   scope, and that scope has `OOMPolicy=stop`, the systemd user manager
   began stopping the whole scope, which with `KillMode=control-group`
   means SIGTERM to every process in it -- the zsh, the claude process, the
   agent-intercom node, the running cargo/bash tree; the claude process
   handled the signal as a graceful shutdown (the two `cost-state` /
   `last-prompt` pairs at 04:08:19.26-.38, the telemetry directory touched
   at 04:08:19.90, the `Exit code 137` synthesised for the tool it was
   tearing down, the bridge detach attachment) and exited within about two
   seconds; the interactive zsh ignored SIGTERM and was SIGKILLed when the
   90 s stop timeout expired at 04:09:48. `Failed with result 'oom-kill'`
   is systemd's own label for this path.
2. The two background subagents died with the process; nothing on the
   machine restarts an interactive Claude Code session, so the flow stayed
   dead until the living started a new process at 10:39 and resumed the
   session, at which point the harness reported both agents as without a
   completion record.
3. The seven-hour gap is explained by 1 and 2 alone. It is not a
   machine-wide event: Codex flow acf06f worked and committed at 04:49,
   05:04, 05:06; the other Claude processes survived (they were idle only
   because their flows had finished their turns before 02:17).
4. The `Exit code 137` at 04:08:19 is most plausibly the harness killing its
   own child tree during shutdown (137 = SIGKILL), since the kernel killed
   only the test binary and systemd's first signal is SIGTERM (143);
   either way it is a symptom of the shutdown, not its cause.
5. The `remote_session_change` attachment with `url: null` at 04:08:19.479
   reads as the bridge detaching on shutdown; the `claude remote-control`
   status redraw at 04:08:18-21 is consistent with that but also with an
   hourly redraw (it redrew at 03:08:56), so it is not by itself evidence.
6. The 2.1.258 to 2.1.261 version change is incidental: the nix profile
   was updated at some point, and the new process picked up the new store
   path; no auto-update or restart happened inside the old process.

## Hypotheses, ranked

| Rank | Hypothesis | Supports | Contradicts |
|---|---|---|---|
| 1 | Kernel OOM kill of the audit's deep-nesting test binary, then systemd `OOMPolicy=stop` stopping the whole ghostty scope (SIGTERM to claude, SIGKILL to zsh after 90 s) | Kernel OOM record naming the binary and the scope; systemd "OOM killer killed some processes in this unit" / "Stopping timed out. Killing." / "Failed with result 'oom-kill'"; scope peak 23.5G RSS + 25.7G swap; the test command and `Exit code 137` in affd462f at the same second; graceful-shutdown records in the main transcript at 04:08:19; `OOMPolicy=stop` on sibling scopes and `DefaultOOMPolicy=stop`; the resumed harness's own diagnosis ("running when the previous Claude Code process exited") | Nothing found |
| 2 | The living closed the terminal surface or killed the process | The living was at the machine at 03:31 | The stop was initiated by systemd at the OOM second; a manual close would not be logged as `oom-kill`; no evidence of input at 04:08 |
| 3 | Usage or rate limit, overloaded API, context-window limit | -- | No such message in any transcript; last assistant records end normally; the resumed process worked at once; 14.99 M tokens left |
| 4 | Machine suspend, reboot, or network loss | -- | Single boot since 08-19; no suspend, logind, or NetworkManager entries; Codex kept working and committing 04:29-05:09 |
| 5 | Harness self-update or crash (2.1.258 to 2.1.261) | Version differs between old and new process | Version change is only visible in the new process; no crash log in `~/.claude/debug`; the exit records are orderly, not a crash |

## Unknowns

- Direct proof that the claude process received SIGTERM from the scope
  stop. systemd logs only the final SIGKILL of the scope leader; the old
  claude pid is not recorded anywhere that survived. Would be settled by:
  systemd user manager debug logging (`systemd.log_level=debug` or
  `LogLevel=debug` in user.conf) during a reproduction; or an audit rule on
  signal delivery; or reproducing with `OOMPolicy=continue` on the ghostty
  scope and seeing the session survive an OOM-killed child.
- What the main flow was doing between 04:00:59 and 04:08:19: no API
  request record exists in the interval, yet the bbzsywg9d notification was
  removed as `absorbed_mid_turn` at 04:04:06. Whether a turn was open with
  no request written, or the harness uses that reason for a notification
  consumed while background agents are pending, is not visible in the
  transcript.
- What entry was created or removed in the session `tasks/` directory at
  04:08:19.484 and in `~/.claude/telemetry/` at 04:08:19.896.
- Whether the ghostty surface closed, or stayed open showing a dead shell;
  only the living's observation settles that.
- Whether the `claude remote-control` redraw at 04:08:18 was reactive or
  hourly; more redraw timestamps from earlier days would settle it.

## Possible remedies (not decided here)

- `OOMPolicy=continue` for ghostty surface scopes (or
  `DefaultOOMPolicy=continue` in the user manager), so an OOM-killed child
  no longer takes the session with it.
- Running memory-hungry test binaries under a memory cap
  (`systemd-run --user --scope -p MemoryMax=...`, or `ulimit -v`) or in a
  release build, so the kernel kills the test early rather than after the
  whole machine has swapped 41 GB.

## Sources

- `/home/li/.claude/projects/-home-li-primary/1a6ca4f9-e0fa-4f2c-bd6f-a40651590354.jsonl`, lines 605-621 (exit and resume), 380, 665-666
- `/home/li/.claude/projects/-home-li-primary/1a6ca4f9-e0fa-4f2c-bd6f-a40651590354/subagents/agent-a049784d240489e32.jsonl`, lines 115-141, and its `.meta.json`
- `/home/li/.claude/projects/-home-li-primary/1a6ca4f9-e0fa-4f2c-bd6f-a40651590354/subagents/agent-affd462f4f7fb88d7.jsonl`, lines 89-135, and its `.meta.json`
- `/tmp/claude-1001/-home-li-primary/1a6ca4f9-e0fa-4f2c-bd6f-a40651590354/tasks/` (symlink and directory mtimes)
- `/tmp/claude-1001/-home-li-primary/1a6ca4f9-e0fa-4f2c-bd6f-a40651590354/scratchpad/adv2/` (`Cargo.toml`, `target/debug/deps/deep-506aa60031e4f38d` mtime)
- `journalctl --user --since "2026-09-05 03:30" --until "2026-09-05 04:30"`; `journalctl --user _PID=1637794`; `journalctl -k --since "2026-09-05 00:00" --until "2026-09-05 11:00"`; `journalctl --list-boots`; `journalctl -u systemd-logind`, `-u NetworkManager`, `-u systemd-oomd`
- `systemctl --user show -p DefaultOOMPolicy -p DefaultTimeoutStopUSec`; `systemctl --user show app-ghostty-surface-transient-1013091.scope`
- `ps -eo pid,ppid,lstart,etime,cmd` for claude, zsh, ghostty, systemd --user
- `/home/li/.claude/sessions/4027731.json`; `/home/li/.claude/debug/`, `/home/li/.claude/telemetry/` listings; `readlink -f $(which claude)`
- `git -C /home/li/primary log --since "2026-09-05 03:30" --until "2026-09-05 11:00"`
- `/home/li/.codex/sessions/2026/09/05/` rollout file mtimes; `/home/li/primary/flows/acf06f/log.md`
- Other Claude transcripts under `/home/li/.claude/projects/-home-li-primary/` (7fba5fce, e996e87c, 58a86d99, fd99506c, 7b4d4ce2, b9a334a4, 77cca2bc, 78c93ce0, c0c52797): record timestamps only
