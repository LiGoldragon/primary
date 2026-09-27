# Witness: 9ac67c held-send binding check

Method: read-only. `FLOW_ID=8904b1 hm-heartbeat-state` (typed routes/retirements,
no mutation) for the stored route; `herdr agent list` (default session, no
subcommand help option, no session named by its forbidden name) for the live
binding; `ps -eo pid,lstart,etimes,cmd` for process continuity; `stat` for
receipt/witness ordering; read of messenger-clj source at
`/git/github.com/LiGoldragon/messenger-clj/src/messenger_clj/core.clj`
(default-branch checkout) for what triggers `RepairRequired`. No send,
repair, bind, register, or Herdr command that creates/attaches/stops/closes/
prompts/focuses anything was run.

## Stored vs live, now

Stored (`hm-heartbeat-state`, flow 9ac67c): session default, name
field-sol-9ac67c, pane_id w1:p9, terminal_id term_65c6ba21c74059, agent
codex, state Bound, native_thread 01a0e029-558a-7852-b5df-1919ac67c6d7.

Live (`herdr agent list`, same pane): agent codex, agent_session.value
01a0e029-558a-7852-b5df-1919ac67c6d7 (kind id, source herdr:codex), name
field-sol-9ac67c, terminal_id term_65c6ba21c74059, pane_id w1:p9, workspace
w1, tab w1:t7, agent_status idle, focused true, interactive_ready true.

Every field messenger checks for a normal send (session, pane_id,
terminal_id, agent, and the native_thread/agent_session compared by
`process-matches!`) matches, right now, exactly.

## Process continuity

`ps` shows PID 116098 (`codex resume 01a0e029-558a-7852-b5df-1919ac67c6d7`),
started Sat Sep 26 18:00:31 2026, still running; its native_thread equals
both the stored route's native_thread and the live agent_session value
throughout. No restart of this process is evidenced between the earlier
delivered send and now.

## Timing against the accidental session

Receipt/witness mtimes: census send 23:10:45; lifecycle-ruling send
23:12:15 (Transported, 9ac67c working) — both while the accidental
two-hyphens-help session was still running (created 23:03:35). The stop
witness (`accidental-help-session-stop.md`) records the stop completed and
confirmed by 23:16:00, with the default session's server (PID 4957)
unchanged before and after. The held witness receipt is timestamped
23:17:44 — roughly ninety seconds after the stop was confirmed.

## Source reading: what produces RepairRequired

`send-request!` (core.clj ~L884-931): `exact-live-agent` and
`process-matches!` are wrapped in bare `catch Exception` at L899-906; *any*
exception while enumerating live agents — not only one about 9ac67c's own
binding — is caught and routed to `hold-repair-required!`.
`shell-live-agents` (~L383-387) enumerates every Herdr session flagged
`:running` in `herdr session list --json` and calls `agent list` on each; an
error from any one running session's socket (e.g. one mid-shutdown) throws
before 9ac67c's own entry is ever reached.

## Other five targets (`hm-heartbeat-state` / `hm-list`, read-only)

6fe957 mind-astra-6fe957 default done; 184bd8 field-luna-184bd8 default
done; 139366 mind-luna-139366 default done; dc53b4 psyche_opus_dc53b4
default done; 38f337 psyche_sonnet_9c7514 default done; c56100
mind_sol_c56100 recovery-56ae53 idle. None shown STALE; no held state is
visible for any through this read-only listing.
