# Compaction request: where it lands, what it can observe

Research for 33752b's proposal book on a compaction request that refuses a
small, young, or just-compacted flow. Every item is marked **witnessed** (read
or run here, 2026-10-13) or **claimed** (someone's report). Inference by this
research flow is marked **inference**.

## (a) The short-term Flow / Flow Nexus prototype

- **witnessed** Report: `/home/li/primary/flows/0c85a3/reports/flow-prototype-assumptions-20261013.md`.
  It names no path; `flows/0c85a3/log.md:37` names `/git/github.com/LiGoldragon/flow`.
  The report says the prototype is not passed or deployed: "No real Flow Start
  or unified deployment is claimed" (a **claim** by 0c85a3 about its own state).
- **witnessed** Repository `/git/github.com/LiGoldragon/flow`, HEAD `ac6ab6`
  "Flow: resolve launch skill dependencies", workspace version 0.24.0 at HEAD,
  0.26.0 in a dirty working copy (29 changed paths, `delivery.rs` unchanged).
  Wire repositories: `/git/github.com/LiGoldragon/signal-flow` (`ecdce2`),
  `/git/github.com/LiGoldragon/meta-signal-flow` (`5d1774`).
- **witnessed** Running service: `flow-nexus` from
  `/nix/store/j689l77...-flow-0.14.0/bin/flow-nexus` (pid 2884570). `strings`
  finds no `/compact` in that binary, so the deployed 0.14.0 very likely lacks
  the `Command` path below (**inference** from a string search).
- Main module: `crates/flow-nexus/src/lib.rs` (meta dispatch); pane writes in
  `crates/flow-nexus/src/delivery.rs`.

Requests accepted today (**witnessed**, ethos sources):

- Ordinary socket, `signal-flow/ethos/signal.ethos:104-121`: `Start Restart
  ResolveRecipient Stop Replace LaunchStatus Observe ResolveCaller
  QueueTurnEnd Report Lock Bind Identify Deliver Release End Current
  Metaflows`.
- Meta socket, `meta-signal-flow/ethos/signal.ethos:52-62`: `Configure
  ConsumeReset RegisterFlow MetaBindExisting Retire Deliver Vet Command
  ResolvePeer ReadEvents`.

A compaction command already exists on the meta socket (**witnessed**):

```
; meta-signal-flow/ethos/signal.ethos:163-167
HarnessCommand.[ Compact Interrupt ]
CommandRequest.{ FlowId HarnessCommand }
CommandGrade.[ Transported Observed Uncertain ]
CommandOutcome.{ FlowId HarnessCommand
  CommandGrade }
CommandRejection.[ UnknownFlow FlowStopped
  RouteUnavailable RecipientBlocked
  UnsupportedForHarness NotDelivered
  FlowRetired FlowExited ]
```

Dispatch, `crates/flow-nexus/src/lib.rs:384` (working copy; `:386` at HEAD):

```rust
meta_signal_flow::Query::Command(request) =>
    self.command(request),
```

Landing point, `crates/flow-nexus/src/delivery.rs:230-275`,
`impl DeliversMessages for RunningNexus`, `fn command`; the compaction arm is
lines 258-268:

```rust
HarnessCommand::Compact => {
    let observe = matches!(agent_state,
        AgentState::Idle | AgentState::Done);
    match self.herdr.place(&target.route,
            "/compact", observe) {
        Placement::Refused => {
            return Response::CommandRejected(
                CommandRejection::NotDelivered);
        }
        Placement::Uncertain =>
            CommandGrade::Uncertain,
        ...
```

It checks only route and pane state (`delivery_target` at `delivery.rs:84`,
`writable_state` at `:159`); nothing about occupancy, age, or last compaction.
README usage (**witnessed**, `flow/README.md:41`):
`flow-meta 'Command.{ 00f95a Compact }'`.

Thresholds (**witnessed**): `meta-signal-flow/ethos/signal.ethos:93`
`ConfigureThreshold.{ Layer Handover.Integer Refresh.Integer }` is accepted by
`Configure` and stored (`crates/flow-nexus/src/store.rs:66,310`); no other
non-generated Nexus source reads it. `/git/github.com/LiGoldragon/flow-data`
holds no threshold value.

Metaflow addressing: `Command` takes a `FlowId` only; ordinary `Lock`/`Deliver`
and `Current.Address` speak metaflows. A metaflow target would resolve through
`Current.Address` to the awake `FlowId` before the guard (**inference**).

## (b) How a flow is compacted today, and what is observable

Senders (**witnessed** unless marked):

- The living types `/compact` in the pane (Herdr terminal or remote control).
  The transcript records no sender: both `/compact` records carry
  `userType":"external","entrypoint":"cli"`.
- Field Core Secondary 42265e's `/compact` at 18:10:27Z: **claimed** in
  `flows/d68c82/log.md:541`; Field's own `flows/42265e/log.md` has no
  compaction entry; the mechanism (direct Herdr pane input) is not witnessed.
- `hm-send`/`hm-send-abrupt` and Flow `Deliver`/`Vet` refuse a body whose first
  line is a harness command (`BodyRefusal.HarnessCommand`,
  `meta-signal-flow/ethos/signal.ethos:149-151`; tests
  `crates/flow-nexus/src/tests/delivery.rs:261`).
- `tools/field-luna-heartbeat.mjs` (96 lines): archive and route cleanup only;
  never compacts.
- `tools/claude-main-flow-launch.mjs:159-165`: installs a `UserPromptSubmit`
  reminder hook and, with a committer, a `Stop` hook to
  `tools/primary-committer/turn-end.mjs`; no compaction or threshold hook.
  33752b's own `~/.claude/jobs/native-33752bfb-.../main-flow-settings.json`
  holds only the `UserPromptSubmit` hook.
- `tools/context-refresh-hook.mjs` (266 lines) is a Stop-hook warner: it
  measures occupancy, compares it with
  `/home/li/primary/config/context-refresh.json` (`claude.warningTokens:
  200000`; Codex windows × `warningWindowFraction 0.5`), and sends a
  `ContextRefreshHandover` through `hm-send` to `Field Core Secondary` and the
  seat. It never compacts. Its handover text (line 105) already says "Before
  compaction or restart, Field must freshly re-read exact occupancy and
  last-compaction state". It is wired into no settings file found here and
  `~/.local/state/context-refresh-hook` does not exist.

Observations:

| observation | source today | in Flow? |
|---|---|---|
| context tokens | transcript `message.usage` | no |
| launch time | transcript first timestamp | no |
| last compaction | transcript `compact_boundary` | no |

- Occupancy: `tools/field-census/claude-context.mjs:32-73` sums
  `input_tokens + cache_creation_input_tokens + cache_read_input_tokens` of the
  last `assistant` record; any later `user`, `summary`, or `system`
  compact/clear record marks it `superseded` (lines 64-66), so right after a
  compaction the collector answers unknown. A statusline snapshot
  (`context_window.total_input_tokens`, `context_window_size`,
  `used_percentage`) is read when a path is given (lines 76-97); no statusline
  path is configured by the launcher. Codex:
  `tools/field-census/codex-context.mjs:161-164` recognises
  `compaction`/`context_compacted`/`contextCompaction` records.
- Launch time: Herdr `agent list` and `pane get` carry no time field
  (witnessed for `psyche_core_primary_33752b`, pane `w1:p37`); `hm-heartbeat-state`
  route has none; `signal-flow` `FlowNode.{ FlowId SessionId HarnessKind
  EndpointSelection HerdrRouteSelection OriginClue FlowLifecycle }` has none;
  Flow's `Event.[ Started ToolUsed.String Stopped ]` carries no time.
- Last compaction: Flow's hook `crates/flow/src/hook.rs:92` maps every
  `SessionStart` to `Started` and never reads the hook input's `source`, so a
  compaction is not distinguishable in Flow memory. Claude Code's
  `SessionStart` input carries `source` (`startup|resume|clear|compact`) and a
  `PreCompact` hook exists (**claimed**, Claude Code hook documentation, not
  read here).

## (c) The witnessed case, 33752b transcript

File `/home/li/.claude/projects/-home-li-primary/33752bfb-ebba-4e2d-ba66-be84b318e939.jsonl`
(8,682,596 bytes). **Witnessed**, with one correction to the reported times:

| line | timestamp (Z) | record |
|---|---|---|
| 4994 | 10-13 18:07:07 | last assistant, usage 460,350 |
| 4996 | 10-13 18:07:45.122 | queue enqueue `/compact ` |
| 4999 | 10-13 18:07:45.148 | user `/compact` |
| 5008 | 10-13 18:09:14.370 | `compact_boundary` manual 460,965 → 18,781 |
| 5009 | 10-13 18:09:14.238 | `isCompactSummary: true` |
| 5030 | 10-13 18:10:27.845 | user `/compact` (not queued) |
| 5039 | 10-13 18:11:21.414 | `compact_boundary` manual 18,892 → 18,865 |
| 5068 | 10-13 18:14:29 | next assistant, usage 54,096 |

The second compaction was requested at 18:10:27Z and its boundary is
timestamped 18:11:21Z (durationMs 53,497), 73 seconds after the first
finished. The first ran 89,078 ms. An earlier automatic compaction sits at
line 2146: 2026-10-12T18:27:55Z, trigger `auto`, 321,583 → 19,888.
The transcript's first timestamp is 2026-10-10T19:12:15.155Z.

The boundary record a tool would read:

```
{"type":"system","subtype":"compact_boundary",
 "timestamp":"2026-10-13T18:09:14.370Z",
 "compactMetadata":{"trigger":"manual",
  "preTokens":460965,"postTokens":18781,
  "durationMs":89078,
  "cumulativeDroppedTokens":743879, ...}}
```

Fields that let a tool observe the three facts: `compact_boundary.timestamp`
and `compactMetadata.{trigger,preTokens,postTokens}` (last compaction and
post-compaction occupancy, exact); the last `assistant`
`message.usage.{input_tokens,cache_creation_input_tokens,cache_read_input_tokens}`
after it (current occupancy); the first record's `timestamp` (session age).

Tension in the records about who sent the first `/compact`
(both **claimed**): `flows/33752b/log.md:193` "The living compacted this seat
himself"; `flows/d68c82/log.md:541` "nobody knows who ran it". The transcript
cannot settle it.

## (d) Psyche records

Most recent and most explicit first; verbatim.

- `flows/d68c82/vision/flow.md:52` and `flows/33752b/vision/flow.md:7`,
  2026-10-13: "I want you to make sure that we have a system in place on the
  short-term flow solution that lets us easily ask for a certain flow to be
  compacted or certain meta flows. It would refuse if the context is below a
  certain threshold. That way we could guard against the compacting request
  being routed to a brand-new flow, which we didn't know was being started, or
  if the flow is not a certain age, even in time terms."
- `flows/d68c82/vision/flow.md:60`, 2026-10-13: "I don't like compacted flows
  because they still have a lot of noise. ... I still use compaction right now
  because we just really can't afford to run these huge massive context
  windows, which just end up being full of noise and resulting in very poor
  output."
- `flows/d68c82/vision/flow.md:29-31`, 2026-10-13: "We need a hook that sends a
  warning to Field to either recompact or restart a flow when it reaches a
  certain threshold. / For Claude, you would get a preemptive warning at
  200,000 tokens, at which point we're basically not forcefully trying to
  refresh but are actively taking measures to, first of all, warn the flow
  that we've started a refresh procedure."
- `flows/f5a6e9/vision/flow.md:55-57`, 2026-10-07: "If, let's say, something
  asked for a certain flow to be compacted, then the logic for how this would
  unfold, or how that metaflow would be refreshed in terms of routing, would be
  very different than a message. / Obviously if the flow is brand new, the last
  thing we want to do is compact it."
- `flows/8904b1/vision/skills.md:114`, 2026-09-28: "I eventually don't want
  flows to compact because compacting is a short-term remedy to a problem that
  requires a much more refined approach to reorganize the context in a new
  flow."
- `flows/88475f/vision/message.md:65`, 2026-09-25: "We need to check to make
  sure that it's not just sending a command like `/compact`. ... I guess
  compact could probably be meta level."
- `flows/e51411/vision/refresh.md:49`, 2026-09-25: "If we can't refresh the
  flow, we can just compact and then reload the main skills we want and give it
  a new prompt."
- `flows/6cc91b/vision/flowLifecycle.md:5`, 2026-09-14: "we shouldn't let the
  models compact. There's no need. They're better off rebootstrapping on with a
  really good first prompt on a new flow."
- Distilled, `/git/github.com/LiGoldragon/psyche-context/skills/vision-flow.md:58`:
  "A flow is refreshed when its context passes the layer's threshold: it is
  told, writes its handover, and is replaced as it goes idle; while the refresh
  runs the metaflow is locked, and the predecessor is reaped in the same
  event." No vision-* or intent-* skill mentions compaction.

The f5a6e9 date is the date of comment 1 on the same book (2026-10-07 18:32);
comment 9 is timed 19:09 without its own date.

## (e) Task af8c40b5f8d345a0b

**Witnessed** from its output file (a claim by that subflow about its own
work): it published flow 33752b's `log.md` and `books/1-psyche-honesty.md` to
`origin/main` as commit `55e826` under PrimaryPublish locks 17993 and 18022
(both released), with no conflicts and no `flows/index.md` change because the
line was already there.
