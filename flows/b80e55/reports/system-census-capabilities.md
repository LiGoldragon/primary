# System census capabilities — what can be gathered programmatically

Flow b80e55, subflow report, 2026-09-20.

## Summary

19 data sources probed. Every probe runs non-interactively and can be
scripted on a timer. The cluster is fully observable: pane count, agent
identity, harness type, status, scroll position, terminal output, HM
flow registry, Orchestrate locks, transcript paths, system resources,
and nix-daemon health.

---

## 1. Herdr pane list

**Command:** `herdr --session messaging-build pane list`
**Output:** JSON with one object per pane.
**Fields per pane:** `pane_id`, `tab_id`, `workspace_id`, `terminal_id`,
`agent` (harness type: claude/codex or absent), `agent_status`
(working/idle/done/unknown), `cwd`, `foreground_cwd`, `focused`,
`revision`, `scroll` (`max_offset_from_bottom`, `offset_from_bottom`,
`viewport_rows`), `terminal_title`, `terminal_title_stripped`.
**Current count:** 19 panes across 9 workspaces (wC, wD, wH, wJ, wK, wM, wQ, wS, wY, wZ, w0).
**Timer-safe:** Yes. Pure read.
**Maps to flow:** Via `terminal_id` → HM registry → flow ID.

## 2. Herdr agent list

**Command:** `herdr --session messaging-build agent list`
**Output:** JSON, same fields as pane list plus `name`, `interactive_ready`,
`state_change_seq`.
**Current count:** 15 named agents (some panes have no agent).
**Extra over pane list:** `name` (the HM-registered name), `interactive_ready`,
`state_change_seq` (monotonic counter for state transitions).
**Timer-safe:** Yes.

## 3. Herdr agent explain (verbose)

**Command:** `herdr --session messaging-build agent explain <name> --json --verbose`
**Output:** JSON with detection engine internals.
**Fields:** `agent`, `state`, `cached_remote_version`, `manifest_source`,
`manifest_version`, `remote_update_status`, `remote_update_error`,
`screen_detection_skipped`, `fallback_reason`, `matched_rule` (which rule
determined the state), `evaluated_rules` (full list with per-rule evidence:
`id`, `priority`, `region`, `state`, `matched`, and `evidence` containing
`regex`, `contains`, `line_regex`, `region_bytes`, `region_preview`).
**Useful data:** The `region_preview` field contains recent terminal text
snippets (~2KB) that the detection engine evaluated — this reveals what the
agent was last doing without a full terminal read.
**Timer-safe:** Yes. Pure read.
**Cost:** ~200ms per agent due to screen parsing.

## 4. Herdr agent read

**Command:** `herdr --session messaging-build agent read <name> --lines N --format text`
**Output:** Plain text of the last N non-empty lines from the terminal.
**What it shows:** The actual terminal content — prompt lines, status bars,
recent output. For Codex: model, effort, cwd, context %, weekly quota %,
profile. For Claude: whatever was last printed.
**Example (Codex idle):**
```
gpt-5.6-sol medium · ~/primary · Ready · Context 17% used · weekly 2% left · Main [default]
```
**Context % extraction:** The Codex status line reliably shows `Context NN% used`
and `weekly NN% left`. Claude shows context only via `/context` command output.
**Timer-safe:** Yes. Pure read.
**Maps to flow:** Through agent name → HM registry.

## 5. Transcripts

### Claude
**Location:** `~/.claude/projects/-home-li-primary/<session-uuid>.jsonl`
**Structure:** Each session has a `.jsonl` transcript and a directory with
`custom-title.json` and `subagents/`.
**Mapping:** HM registry `native_thread` field = Claude session UUID.
Path: `~/.claude/projects/-home-li-primary/<native_thread>.jsonl`.
**Timer-safe:** Yes (read-only). Active transcripts grow during sessions.

### Codex
**Location:** `~/.codex/sessions/YYYY/MM/DD/rollout-<timestamp>-<session-uuid>.jsonl`
**Structure:** One JSONL file per session, named with ISO timestamp and UUID.
**Mapping:** HM registry `native_thread` field = Codex session UUID (the last
part of the rollout filename). Find by globbing: `~/.codex/sessions/*/*/*/*<native_thread>*`.
**Timer-safe:** Yes (read-only).

### Association chain
```
flow_id → HM registry → { native_thread, pane_id, terminal_id, name, agent }
                              ↓                                        ↓
                    transcript path                          Herdr agent/pane
```
This chain is complete: given a flow ID, we can find its transcript,
its Herdr pane, its terminal output, its harness type, and its status.

## 6. HM registry

**Location:** `~/.local/state/hacky-messenger/`
**Structure:** One `<flow-id>.json` per active registration; `retired/<flow-id>.json`
for retired flows.
**Fields per entry:** `session` (Herdr session), `name` (agent name), `pane_id`,
`terminal_id`, `agent` (harness type), `native_thread` (session UUID).
**Current count:** 23 active, 3 retired.
**Timer-safe:** Yes.
**Note:** 23 active registrations but only 15 live agents — 8 registrations
point to flows whose agents have been garbage-collected or whose panes were
recycled. The census can cross-reference HM entries against live agents to
find stale registrations.

## 7. Flow directories

**Location:** `/home/li/primary/flows/`
**Count:** 310 directories.
**Structure:** Each contains some subset of `vision/`, `notion/`, `log.md`,
`reports/`, `witnesses/`, `summary.md`.
**Timer-safe:** Yes (listing). Mapping to live/dead requires HM cross-reference.

## 8. Orchestrate locks

**Command:** `orchestrate 'Observe.Locks'`
**Output:** Datom-typed Lock set with all active locks.
**Fields per lock:** integer ID, LockName, FlowId, paths (absolute), reason.
**Current count:** 42 active locks.
**Timer-safe:** Yes. The current CLI reads one frame and exits.
**Maps to flow:** Each lock carries its owning `FlowId`.

## 9. System resources

**Commands:** `free -h`, `df -h /`, `uptime`, `nproc`
**Current state:**
- RAM: 30Gi total, 15Gi used, 6.5Gi free, 9.3Gi buff/cache, 14Gi available
- Swap: 39Gi total, 19Gi used
- Disk: 916G total, 679G used (79%), 191G available
- Uptime: 10 days 3:21
- CPUs: 14
- Load: 3.15, 3.33, 2.94
**Timer-safe:** Yes.

## 10. Nix daemon

**Command:** `systemctl status nix-daemon`
**Current state:** Active (running), PID 3271724, 10 days uptime,
1017.7M memory (peak 15G), CPU 1h22m. Accepting connections from user li.
Last activity: accepted+reaped at 14:29. The daemon is alive but known to
be very slow on fetches — user-process probes to cache.nixos.org answer in
<1s while daemon copies never move.
**Timer-safe:** Yes.

## 11. Running processes

**Command:** `ps aux | grep -E 'claude|codex|herdr|nix-daemon'`
**Current inventory:**
- 1 Herdr server process
- 1 Codex app-server (with remote-control)
- 1 Codex code-mode-host
- 1 Codex resume session (8565e8)
- 5 agent-intercom MCP server processes
- 10+ Claude Desktop processes (Electron: main, renderer, gpu, zygote, utility, crashpad, cowork-helper)
- 1 nix-daemon
- 2 Claude processes (bg-pty-host, bg-spare)
- 2 Claude remote-control --help (possibly stale)
**Timer-safe:** Yes.

---

## Census script design

A single script can gather all the above in one pass:

```
1. herdr agent list          → agent inventory (name, status, harness, pane)
2. HM registry scan          → flow→agent→transcript mapping
3. herdr agent read (each)   → context %, quota %, last activity
4. orchestrate Observe.Locks  → lock ownership per flow
5. free/df/uptime             → host health
6. systemctl status nix-daemon → daemon health
```

Steps 1+2+5+6 are fast (<1s each). Step 3 scales linearly with agent
count (~200ms × 15 = ~3s). Step 4 is ~500ms. Total: ~5s per census cycle.

**Output shape:** One JSON object per pane/flow with:
```
{ flow_id, agent_name, harness, status, pane_id, context_pct,
  quota_pct, transcript_path, lock_count, locks, last_activity }
```
Plus one system-health object:
```
{ ram_available_gb, disk_avail_gb, disk_pct, uptime_days,
  load_1m, nix_daemon_status, process_count }
```

**Delivery:** Message to Field Low/Ultra Low via `hm-send`.

**Eventual home:** Field Nexus signal contract. The script's queries become
typed Signal queries; the JSON output becomes typed datom answers. Transcript
access could be a separate Transcript Nexus that Field Nexus queries, or
merged into Field Nexus — the living's aggregation/splitting question.
