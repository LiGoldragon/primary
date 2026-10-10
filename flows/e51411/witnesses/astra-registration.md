# Astra registration

Witness by Psyche Opus subflow e51411, 2026-09-24, about 14:30-14:42 local (20:30-20:42Z).

## Method

I read Astra's pane and status with `herdr agent get`, `herdr agent read`, and `herdr agent explain` on `wQ:pN`. I read the `register` and `readiness_probe` code in `tools/hacky-messenger/hm.py`, compared it with Mind Sol 00f95a's HM record and rollout, and registered Astra through `hm-register` with its readiness probe. I then delivered the message with `hm-send`. I checked both steps against Astra's native rollout JSONL and its pane.

## Pane state

- `herdr agent get wQ:pN`: codex, `agent_status: working`, name `field-astra-5f38bc`, terminal `term_65c3ff14cafb070`, title `Field Astra 5f38bc | primary`.
- `herdr agent explain`: state working, rule `osc_title_working`, manifest `remote:.../codex.toml 2026.09.15.1`.
- `herdr agent read`: Codex root turn "Working (13m...23m)", waiting on its own subagents (`/root/packet_readiness`, `/root/prometheus_recovery`, `/root/notetaker_theme`).
- At the time I looked, no approval or confirmation prompt was showing. The earlier "[!] Action Required" title was gone, and nothing in the pane needed clearing.

## Cause

`Messenger.register` refuses with "Agent is not interactively ready" whenever `agent.get('interactive_ready')` is falsy and no `--readiness-probe` is given. This Herdr endpoint's `agent list` records have no `interactive_ready` field at all, for Astra or for Mind Sol. So the check fails for every agent on this endpoint, whatever the agent's status. The launcher ran `hm-register 5f38bc field-astra-5f38bc --session messaging-build --native-thread ...` without `--readiness-probe` and `--rollout`, so it was refused. Astra's log calls this "working rather than interactively ready", but "working" was not the cause. Mind Sol 00f95a registered on the same endpoint through the probe path: its record carries `readiness_proof` with marker `HM_READY_00f95a_20260924_2001`.

The probe has a second limit. After prompting, it polls the rollout for about 5 seconds for an exact-marker `AgentMessage` in the thread. A busy Codex root takes longer than that to answer. Mind's rollout shows the same pattern: its first probe was answered in about 5 s and a same-marker retry passed.

## Commands

```
FLOW_ID=e51411 hm-register 5f38bc field-astra-5f38bc --session messaging-build \
  --native-thread 01a0d4f6-6bc6-7530-94d6-1515f38bcb84 \
  --readiness-probe HM_READY_5f38bc_20260924_1440 \
  --rollout /home/li/.codex-next/sessions/2026/09/24/rollout-2026-09-24T13-48-34-01a0d4f6-6bc6-7530-94d6-1515f38bcb84.jsonl
```
First run: `hm: Readiness probe marker was not observed in an exact native assistant reply`. The rollout shows the probe `UserMessage` at 20:40:08.943Z, steered into Astra's running turn `01a0d50f-...`. Astra's `AgentMessage` `HM_READY_5f38bc_20260924_1440` came at 20:40:15.123Z, 6.2 s later and just outside the window. That reply ended the turn (`task_complete`), and the pane went to Ready.

Second run, same command and same marker: `Registered 5f38bc: field-astra-5f38bc (messaging-build)`, exit 0. The existing exact-thread user/assistant marker pair satisfied the probe.

## Readback

`hm-list`:
```
5f38bc	field-astra-5f38bc	messaging-build	done
```
`~/.local/state/hacky-messenger/5f38bc.json`:
```
{"session": "messaging-build", "name": "field-astra-5f38bc", "pane_id": "wQ:pN", "terminal_id": "term_65c3ff14cafb070", "agent": "codex", "readiness_proof": {"thread_id": "01a0d4f6-6bc6-7530-94d6-1515f38bcb84", "rollout": "/home/li/.codex-next/sessions/2026/09/24/rollout-2026-09-24T13-48-34-01a0d4f6-6bc6-7530-94d6-1515f38bcb84.jsonl", "marker": "HM_READY_5f38bc_20260924_1440"}, "native_thread": "01a0d4f6-6bc6-7530-94d6-1515f38bcb84"}
```

## Delivery

`FLOW_ID=e51411 hm-send 5f38bc "<Psyche High 752e0f message, word for word>\nAlready done: Psyche Opus e51411 registered you in HM as 5f38bc (pane wQ:pN, thread 01a0d4f6-6bc6-7530-94d6-1515f38bcb84); skip the registration step."` returned `Transported.{ 5f38bc done }`.

Grade: Transported by hm-send. The message was also witnessed as received: Astra's rollout line 1254 holds the `UserMessage` in thread `01a0d4f6-...` at 20:40:57Z. The pane shows the `Machine.Relay.{ machine e51411 ... [ 5f38bc ] ... }` frame, and Astra answered: "I'll skip registration and verify the existing binding. I'll take Mind's published BindExisting runtime through deployment...". The fallback `herdr agent prompt` was not needed.

## Side effects

- Two probe prompts reached Astra's thread. The first ended Astra's 24-minute root turn early with the marker as its final answer. Its subagents were not touched, and Astra resumed with the delivered message.
- No other pane or seat was touched.
