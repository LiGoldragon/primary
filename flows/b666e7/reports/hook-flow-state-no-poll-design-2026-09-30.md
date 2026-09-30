# Hook-fed Flow state without polling

Prepared 2026-09-30 for Psyche Opus `7328f4`. This is an evidence/design
report only. It proposes no implementation or host change.

## Witnessed facts

- `~/.claude/settings.json`, `~/.codex/hooks.json`, and
  `~/.codex-next/hooks.json` each install a Herdr `SessionStart` hook. Their
  respective `herdr-agent-state.sh session` scripts are marked as Herdr-managed
  and call `pane.report_agent_session` with the harness session identity and
  pane identity.
- These are identity reporters only. The inspected scripts do not report
  working, stopped, failed, interrupted, permission, input-needed, or seen
  state; they do not alter a Herdr dot.
- The Claude `UserPromptSubmit` reminder is separate. The Opus launcher
  `tools/claude-main-flow-launch.mjs:102` passes a session-scoped `--settings`
  `main-flow-settings.json`; that configuration invokes the every-20 reminder.
  It is not a Herdr reporter and is not a global Claude hook.
- The existing Flow/Herdr binding source cited by the earlier investigation is
  `flow/crates/flow-nexus/src/herdr.rs:136-147,375-421`.
- Herdr's observed UI facts are separate: red means blocked, yellow working,
  teal idle/unseen, and hollow green idle/seen. Focus determines `seen`; a pane
  read does not clear unread.

The prior report, `herdr-turn-state-hooks-2026-09-30.md`, is corrected to say
the three identity reporters are installed. No turn-state mapping beyond that
was witnessed.

## Design boundary

**Fact.** The psyche asks for flow state through hooks, no polling, and a
visible registry/report for any exceptional periodic polling. `Vision/nexus.md`
sets state observation by subscription and forbids polling when nothing
changes.

**Inference.** A hook adapter is a push producer. Each lifecycle callback
becomes one durable event in a Flow event inlet. Subscribers receive the
current projection when they attach and subsequent events when they occur.

```
harness hook -> harness adapter -> durable Flow event inlet -> projection -> subscriber
Herdr identity / seen observation ------------------------^ separate fact
```

Hook-derived lifecycle and Herdr `seen` must remain separate. A stopped turn
may remain unread, and a terminal read or delivery cannot become a claim that
the living read it. No supported Herdr dot-override API is asserted here.

## Identity, epochs, and ordering

Every inlet event contains `flow_id`, agent kind, native `session_id`,
`binding_epoch`, source event, observed time, adapter sequence, and a delivery
UUID. The flow id comes from the established Flow-to-Herdr binding, never a
prompt. A new accepted `SessionStart` binding, rebinding, or adapter restart
opens a new binding epoch and closes the old epoch for writes.

For Codex, use the documented native `turn_id`. Claude does not document a
native prompt/stop turn id: the adapter mints `turn_correlation_id` at
`UserPromptSubmit`, inside the binding epoch, and attaches later callbacks to
that open correlation. It is explicitly adapter-minted, not a Claude identity.
The adapter accepts an event only when its native session and epoch binding
agree. Source identifiers or delivery UUIDs plus sequence make duplicate and
late callbacks idempotent without letting an old pane update a replacement.

## Proposed event mapping

| Projected event | Source | Scope and limit |
| --- | --- | --- |
| `Working` | `UserPromptSubmit` opens the turn. | Claude and Codex; Codex native turn id, Claude adapter correlation. |
| `TurnStopped` | `Stop` closes the matching turn. | Claude and Codex. |
| `Failed` | `StopFailure` closes the matching turn with failure kind. | Claude. Codex's published hook surface has no `StopFailure`; never infer it from silence or a hook error. |
| `Interrupted` | `Interrupt` closes the stated turn. | Codex main thread. Claude requires separately witnessed support. |
| `PermissionPending` | `PermissionRequest` records a blocked request. | Claude and Codex; it does not establish that a person saw it. |
| `AwaitingLivingInput` | A documented input-needed event carries its reason. | Claude `Notification` may supply `agent_needs_input`. Codex has `PermissionRequest`, but no documented general input-needed hook; do not invent one. |
| `HerdrSeen` | Herdr pane/seen observation with timestamp. | Separate input; installed reporters do not emit it. |

`SessionStart` creates or refreshes identity binding, not `Working` state.
`SessionEnd` may end a binding, but cannot certify the result of a missed turn.

[Claude Code Hooks](https://code.claude.com/docs/en/hooks) documents
`SessionStart`/`SessionEnd`, `UserPromptSubmit`, `Stop`, `StopFailure`,
`PermissionRequest`/`PermissionDenied`, and `Notification`; it also describes
the user-level scope of `~/.claude/settings.json`. [Codex Hooks](https://learn.chatgpt.com/docs/hooks)
documents `SessionStart`/`SessionEnd`, `UserPromptSubmit`, `Stop`, `Interrupt`,
and `PermissionRequest`, and supplies `turn_id` where stated. Its
`transcript_path` is convenience data, not a stable hook interface.

## Gaps, recovery, and reconciliation

**Fact.** A hook proves only a callback delivered to this adapter. It cannot
describe a period in which the hook was missing, the adapter was down, or the
process restarted. Silence is not an idle event.

**Design.** A missing binding, restart, failed durable acknowledgement, or new
epoch replacing an open turn appends `StateUncertain`, retaining the exact
reason and last known event. The projection says “uncertain since …”; it never
turns quiet time into `Idle` or `TurnStopped`.

An explicit on-demand reconciliation may read the current Herdr binding/status
and native harness metadata and append a time-stamped `ReconciledObservation`.
It is a snapshot, not proof of a lost turn outcome, and it must leave that
outcome uncertain. Reading a pane must not set `HerdrSeen`.

Any periodic fallback is an explicit exception. Before it runs, a registry
entry records owner Flow, recipient, purpose, target, cadence, trigger/stop
condition, last/next run, and report destination. Its periodic report lists
every registered fallback, including zero. No periodic fallback is proposed or
enabled by this report.

## Open choices for Psyche Opus

1. Which recipients see which projected transitions: Flow/Herdr only, the
   living surface, Message recipients, or a named combination.
2. Which transitions notify immediately: all, only failure/interruption/input,
   or a policy per flow.
3. Whether `PermissionPending` also means `AwaitingLivingInput`.
4. Whether on-demand reconciliation suffices; if not, the exact fallback
   period, steward, and registry/report recipient.

Until these choices are made, the safe default is durable hook events, a
separate Herdr-seen fact, explicit uncertainty after a gap, and no polling.
