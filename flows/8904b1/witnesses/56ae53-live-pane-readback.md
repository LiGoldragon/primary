# 56ae53 live-pane readback — subflow of 8904b1, 2026-09-26

Read-only. Method: `herdr session list`, `herdr agent list --session default`,
`herdr agent get w1:p1 --session default`; process identification via
`ps -ef | grep codex` plus `/proc/7554/cwd` and `/proc/7554/environ`
(HERDR_PANE_ID, HERDR_SOCKET_PATH, HERDR_WORKSPACE_ID, HERDR_TAB_ID); the
Codex thread's persisted record at
`/home/li/.codex-next/sessions/2026/09/26/rollout-2026-09-26T09-18-59-01a0de4c-554d-7343-bbc5-e4256ae5366f.jsonl`
(matched to the process by the thread id in its argv, `01a0de4c-554d-7343-bbc5-e4256ae5366f`,
and cross-checked by cwd `/home/li/primary`); registry reads via
`hm-list` (messenger) and `flow 'List.{}'` / `flow 'ResolveRecipient.56ae53'` (Flow).
Nothing was started, attached, stopped, prompted, sent, or focused.

## 1. Herdr, pane w1:p1, session default (`herdr agent get w1:p1 --session default`)
- Exact name: none — the `name` key is absent from the agent record.
- Terminal identity: `terminal_id term_65c6a3b37c3011`; `terminal_title` seen as
  `⠸ primary` / `⠼ primary` (an animating spinner glyph), `terminal_title_stripped primary`.
- Harness Herdr records: `agent codex`.
- Agent session value: absent — no `agent_session` key at all.
- Interactive-ready: absent — no `interactive_ready` key (other panes in the same
  listing carry `interactive_ready:true` explicitly; this one omits the field).
- Status: `agent_status working`.
- Working directory: `cwd /home/li/primary` (also `foreground_cwd`).
- Pane title as displayed: same as terminal_title above.

## 2. Native side
- Process: PID 7554, tty pts/1, started 2026-09-26 16:22:08, cmd
  `/home/li/.nix-profile/bin/codex resume --remote unix:///home/li/.codex-next/app-server-control/app-server-control.sock -m gpt-6-sol -c model_reasoning_effort=medium -C /home/li/primary -a never -s danger-full-access --dangerously-bypass-hook-trust 01a0de4c-554d-7343-bbc5-e4256ae5366f`.
- Tie to the pane: `/proc/7554/environ` carries `HERDR_PANE_ID=w1:p1`,
  `HERDR_WORKSPACE_ID=w1`, `HERDR_TAB_ID=w1:t1`, `HERDR_SOCKET_PATH=/home/li/.config/herdr/herdr.sock`
  (the `default` session's socket) — the process names its own pane.
- Codex thread identity: `01a0de4c-554d-7343-bbc5-e4256ae5366f`, taken from the
  process argv (the trailing `resume` argument).
- Harness's persisted session record: rollout file
  `/home/li/.codex-next/sessions/2026/09/26/rollout-2026-09-26T09-18-59-01a0de4c-554d-7343-bbc5-e4256ae5366f.jsonl`,
  whose `session_meta.id`/`session_meta.payload.id` equal that same thread id,
  and whose `cwd` (`/home/li/primary`) matches the process's `-C` and the pane's cwd.
  Tie made by thread id first, cwd second — not by Herdr's word (Herdr held no
  `agent_session` for this pane at all).
- Herdr's agent session value for this Codex seat: empty, confirmed above (no
  `agent_session` key) — consistent with the flow's earlier record that Herdr 0.8.2
  does not fill it for Codex.

## 3. Agreement
- Thread `01a0de4c-554d-7343-bbc5-e4256ae5366f`, process PID 7554, and pane `w1:p1`
  in session `default` agree: one seat, one pane, one thread.
- Checked `ps -ef` (whole host) and `herdr agent list` on every running session
  (`default`, `recovery-56ae53`) for this thread id or this pane id: no other
  process or pane carries it. (The `--help`-named session was seen as `stopped`
  in the session list and was not queried further or named in any command.)

## 4. Old binding
- `herdr session list`: session `messaging-build` shows `status stopped`.
- No pane `wM:pJ` is live: `messaging-build` is stopped, and neither running
  session (`default`, `recovery-56ae53`) lists a `wM:pJ` pane.
- Messenger registry (`hm-list`, read-only list): row for Flow `56ae53` —
  Agent `mind-sol-of-00f95a-56ae53`, Session `messaging-build`, State `STALE`.
  (This listing has no Pane/Terminal column.)
- Flow's registry (`flow 'List.{}'`, read-only): row for `56ae53` —
  `{ 56ae53 01a0de4c-554d-7343-bbc5-e4256ae5366f Codex Unavailable
  Available.{ messaging-build mind-sol-of-00f95a-56ae53 wM:pJ term_65c6462fe47809b }
  { 38de5b messaging-build meta-bind-existing } Active }`
  — native session id `01a0de4c-554d-7343-bbc5-e4256ae5366f`, harness `Codex`,
  Herdr session `messaging-build`, agent name `mind-sol-of-00f95a-56ae53`,
  pane `wM:pJ`, terminal `term_65c6462fe47809b`, lifecycle `Active`.
  `flow 'ResolveRecipient.56ae53'` returns the same, Herdr route `Unavailable`.

## 5. Differences, field by field
| Field | Live (w1:p1, session default) | Messenger registry | Flow registry |
|---|---|---|---|
| Session | default (running) | messaging-build (stopped) | messaging-build (stopped) |
| Pane | w1:p1 | (not carried) | wM:pJ |
| Agent name | (none set) | mind-sol-of-00f95a-56ae53 | mind-sol-of-00f95a-56ae53 |
| Terminal | term_65c6a3b37c3011 | (not carried) | term_65c6462fe47809b |
| Native/thread id | 01a0de4c-554d-7343-bbc5-e4256ae5366f (from process argv + rollout) | (not carried) | 01a0de4c-554d-7343-bbc5-e4256ae5366f (agrees) |
| State | agent_status: working (Herdr) | STALE | Active |

Everything but the thread id itself is stale in both registries; the thread id
is the one field that already agrees.

## 6. Native readiness witnessed
- Model and effort, from the persisted rollout record: `model gpt-6-sol`,
  `effort`/`reasoning_effort medium` — matching the process argv
  (`-m gpt-6-sol -c model_reasoning_effort=medium`).
- Startup record exists: yes — `session_meta` is the first line of the rollout
  file, timestamped 2026-09-26T15:18:59.665Z.
- Not witnessed / unknown: Herdr's own `interactive_ready` state for this pane
  (the field is simply absent, not set false); the guardian/safety layer's state;
  anything about the pane's visible on-screen content beyond its title (no
  `herdr agent read` was run, since it was not asked for and this task avoids
  unnecessary reads).

## Sources
- `herdr session list`; `herdr agent list --session default`; `herdr agent get w1:p1 --session default`
- `ps -ef`; `/proc/7554/cwd`; `/proc/7554/environ`
- `/home/li/.codex-next/sessions/2026/09/26/rollout-2026-09-26T09-18-59-01a0de4c-554d-7343-bbc5-e4256ae5366f.jsonl`
- `hm-list`; `flow 'List.{}'`; `flow 'ResolveRecipient.56ae53'`
- `/home/li/wt/primary/56ae53/flows/38de5b/receipts/flow-bind-56ae53.md` (prior receipt, for query syntax and the last-known binding's own evidence, read only)
