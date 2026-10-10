# dc53b4 stable bind — raw receipts

Subflow of dc53b4 (session dc53b4be-338b-4601-ab3c-a0e155fc8fa9, Herdr default w1:pC term_65c6bcb737eabc).
Stable Flow client/nexus 0.12.2 (flow-nexus.service override ExecStart flow-0.12.2), messenger-clj 0.2.5, Herdr 0.8.2.
No flow-id run, no seat started/stopped, no prompt sent into any pane.

## Pre-state (before any write)

- Herdr agent name on w1:pC was `psyche_opus_e167d8` (a predecessor name); unregistered in HM (`-`), not the Flow e167d8 route (that is messaging-build w19:p1).
- `flow 'List.{}'` and `hm-list` had no dc53b4 row.
- Pane title: `Psyche Opus (claim pending)`.

## Commands, verbatim output

```
$ herdr agent rename w1:pC psyche_opus_dc53b4
[2026-09-26T18:21:16-06:00]
{"id":"cli:agent:rename","result":{"agent":{"agent":"claude","agent_session":{"agent":"claude","kind":"id","source":"herdr:claude","value":"dc53b4be-338b-4601-ab3c-a0e155fc8fa9"},"agent_status":"working","cwd":"/home/li/wt/primary/opus-sonnet-56ae53","executable":"claude","focused":false,"foreground_cwd":"/home/li/wt/primary/opus-sonnet-56ae53","interactive_ready":true,"name":"psyche_opus_dc53b4","pane_id":"w1:pC","revision":3,"state_change_seq":82,"tab_id":"w1:tA","terminal_id":"term_65c6bcb737eabc","terminal_title":"◐ Psyche Opus (claim pending)","terminal_title_stripped":"Psyche Opus (claim pending)","workspace_id":"w1"},"type":"agent_info"}}
exit=0

$ herdr agent get w1:pC
[2026-09-26T18:21:16-06:00]
{"id":"cli:agent:get","result":{"agent":{"agent":"claude","agent_session":{"agent":"claude","kind":"id","source":"herdr:claude","value":"dc53b4be-338b-4601-ab3c-a0e155fc8fa9"},"agent_status":"working","cwd":"/home/li/wt/primary/opus-sonnet-56ae53","executable":"claude","focused":false,"foreground_cwd":"/home/li/wt/primary/opus-sonnet-56ae53","interactive_ready":true,"name":"psyche_opus_dc53b4","pane_id":"w1:pC","revision":3,"state_change_seq":82,"tab_id":"w1:tA","terminal_id":"term_65c6bcb737eabc","terminal_title":"◐ Psyche Opus (claim pending)","terminal_title_stripped":"Psyche Opus (claim pending)","workspace_id":"w1"},"type":"agent_info"}}
exit=0

$ flow-meta register-claude dc53b4 dc53b4be-338b-4601-ab3c-a0e155fc8fa9 default psyche_opus_dc53b4 w1:pC term_65c6bcb737eabc
[2026-09-26T18:21:20-06:00]
FlowRegistered.{ dc53b4 dc53b4be-338b-4601-ab3c-a0e155fc8fa9 Claude Unavailable Available.{ default psyche_opus_dc53b4 w1:pC term_65c6bcb737eabc } { dc53b4 dc53b4be-338b-4601-ab3c-a0e155fc8fa9 unavailable } Active }
exit=0

$ hm-register dc53b4 psyche_opus_dc53b4 --session default --native-thread dc53b4be-338b-4601-ab3c-a0e155fc8fa9
[2026-09-26T18:21:24-06:00]
Registered dc53b4: psyche_opus_dc53b4 (default)
exit=0

$ flow 'List.{}'   (full output saved; dc53b4 record extracted)
2026-09-26T18:21:31-06:00
exit=0
{ dc53b4 dc53b4be-338b-4601-ab3c-a0e155fc8fa9 Claude Unavailable Available.{ default psyche_opus_dc53b4 w1:pC term_65c6bcb737eabc } { dc53b4 dc53b4be-338b-4601-ab3c-a0e155fc8fa9 unavailable } Active }

$ hm-list | grep dc53b4
2026-09-26T18:21:31-06:00
exit=0
FLOW	AGENT	SESSION	STATE
dc53b4	psyche_opus_dc53b4	default	working

$ hm-heartbeat-state | jq '[.routes[]|select(.flow=="dc53b4")], [(.retirements//[])[]|select(tostring|test("dc53b4"))]'
2026-09-26T18:21:37-06:00
exit=0
[{"flow":"dc53b4","route":{"session":"default","name":"psyche_opus_dc53b4","pane_id":"w1:pC","terminal_id":"term_65c6bcb737eabc","agent":"claude","state":"Bound","native_thread":"dc53b4be-338b-4601-ab3c-a0e155fc8fa9"}}]
[]

$ herdr pane get w1:pC  (title readback)
2026-09-26T18:21:38-06:00
{"id":"cli:pane:get","result":{"pane":{"agent":"claude","agent_session":{"agent":"claude","kind":"id","source":"herdr:claude","value":"dc53b4be-338b-4601-ab3c-a0e155fc8fa9"},"agent_status":"working","cwd":"/home/li/wt/primary/opus-sonnet-56ae53","focused":false,"foreground_cwd":"/home/li/wt/primary/opus-sonnet-56ae53","pane_id":"w1:pC","revision":3,"scroll":{"max_offset_from_bottom":0,"offset_from_bottom":0,"viewport_rows":44},"tab_id":"w1:tA","terminal_id":"term_65c6bcb737eabc","terminal_title":"◐ Psyche Opus (claim pending)","terminal_title_stripped":"Psyche Opus (claim pending)","workspace_id":"w1"},"type":"pane_info"}}
exit=0
```

## Title gate: NOT performed (stopped per brief)

The only supported Claude title adapter witnessed in this system (flows 752e0f, d8df70, Flow 0.10 G4) is `/rename` submitted into the seat's own pane.
That is typing into this seat's pane, which the brief forbids. No transcript or title was rewritten.
Exact command for the authorized party:

    herdr agent prompt w1:pC "/rename Psyche Opus dc53b4"

Readback command:

    herdr pane get w1:pC   # expect terminal_title_stripped "Psyche Opus dc53b4"

Current readback (above): terminal_title_stripped "Psyche Opus (claim pending)" — title gate unwitnessed.
