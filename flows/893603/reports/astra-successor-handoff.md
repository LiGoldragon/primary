# Astra successor handoff

Date: 2026-09-18. Scope: launch and readiness witness only; no integration-path edits.

The supported native launch used the existing app-server Unix WebSocket client (`WS` from `flows/024bc7/tools/codex_wake.py`): initialize, read remote-control status, `thread/start` with `/home/li/primary`, `gpt-6-astra`, and `ephemeral=false`, set the native name `Primary Astra successor · Flow893603`, then `turn/start` with effort `medium` and the ordered successor handoff. The launch returned native thread `01a0b53b-fb0f-7751-95be-e68e26a648b8` and a completed first turn.

The successor's actual native return witnessed Flow `e26a64`, model `gpt-6-astra`, medium effort, lane `/home/li/primary/flows/e26a64`, and persisted native rollout. It reported the working tree clean, preserved the predecessor and all existing sessions, and retained the read-only hardware trace, blocked consumer/Home gate, Message/producer source handoff, pending MS2130/lazy-composition decision, and Fable registration review. The managed Herdr identity was verified as `psyche-mind-astra-refresh` on `messaging-build`, pane `w1:p5`, terminal `term_65bc26ed43be77`, interactive-ready and working. `hm-register e26a64 psyche-mind-astra-refresh --session messaging-build` succeeded; `hm-list` shows the existing `893603,e26a64` registration on that managed identity.

The field reaper was already present and was not duplicated: Flow `33ba2b`, name `field-reaper`, Herdr pane `w1:pG`, terminal `term_65bc3f245852c15`, gpt-5.6-sol medium, interactive-ready. Its registration and native return are owned by `message_receipts`.

The current future-Claude requirement remains unfinished. A future authoritative launcher must set `CLAUDE_CODE_FORCE_SESSION_PERSISTENCE=1` and pass `--remote-control` at creation, then witness an emitted remote endpoint or registered remote status before claiming remote accessibility. No current authoritative launcher was identified here, and no Claude session was launched.

The living's requested latest actual Opus 4.6 Flow remains unresolved. Read-only native/Herdr inspection found preserved Opus panes, including visible Opus 5 output, but no current identity that proves Opus 4.6. The two raw living messages are preserved in `flows/893603/vision/claude-persistence.md`; no message was sent to a guessed Opus target or to the known Opus 5 flow.

No hardware approver was assigned. The consumer gate remains blocked; no activation, service, store, or integration operation was performed.
