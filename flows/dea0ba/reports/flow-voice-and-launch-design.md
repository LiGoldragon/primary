# Flow: voice addressing and one launch route

Status: proposed implementation design for Mind Sol review and Field Sol build. No launch, hook runtime, generated wire, or deployment is claimed. Scope: voice registry/addressing, Codex native lifecycle integration, and Flow Start as the only launch coordinator. Shared-workspace publication is separate.

## Baseline and what stays

The supplied Fable report names Flow0.23 main636214e5; it was unavailable in the inspected checkout. Direct source evidence is Flow0.24.0 at4ad596d466a45de56239c55d415474f8b35ab163, with next-f1c841 at an empty child2cb4df. It pins signal-flow f95034de0… and meta-signal-flow54eb5618e…. Build on that immutable source and reconcile later commits before implementation; do not recreate existing features.

Keep StartRequest's LaunchProfile/OriginClue, durable request-id attempt ledger, exact-repeat idempotency, differing-request conflict rejection, launch status/observation, first-turn delivery controller and replacement/reaping machinery. Keep0.24's Claude pre-spawn reservation and protected release of only an empty unregistered claim. Codex extends this coordinator, not a second launcher.

Current Report has only FlowId+Event, validates a held ID and appends without deduplication or native-session correlation. Current Event is Started/ToolUsed(String)/Stopped. Claude Stop maps to Stopped, but the wire commentary warns Stop can precede a final native record or repeat while a turn continues. It is not flow-end evidence. QueueTurnEnd is refused; this design does not rely on it.

## Identity and authority

A voice is persistent Aspect.Rank. Aspects are Psyche, Mind, Field; ranks Primary, Secondary, Tertiary: nine slots. This is settled vision. Rank differs from PowerLevel (High/Medium/Low/UltraLow), model, and harness. Models may change behind an address. FlowId identifies a run for ledger/transcript lookup; a native session identifies its harness thread. They are not interchangeable.

A side flow is a finite job owned by OriginClue's caller, has a FlowId, and occupies no voice slot. Finishing a turn is not finishing its job. Its controller explicitly completes/stops it when its mission ends. A message to a terminal job receives an ended notice; it is never silently redirected to another job or a parent voice.

Flow owns the registry, not Herdr titles, Messenger nickname files, or model names. Each slot stores current FlowId, binding generation, and optional pending launch request. Ordinary launchers cannot overwrite bindings. Start/Replace owns normal transitions; a privileged compare-and-set exists only for explicit bootstrap/adoption of already-running flows. It validates run aspect/routability, slot generation and uniqueness. Never infer Rank from model or PowerLevel. Opus supplies explicit initial nine-slot adoption assignments; unknown slots stay unbound.

## Proposed wire delta, in Ethos

These are target declaration fragments in current Signal grammar, not complete generator input or compiled contracts. Merge into ordinary/meta contracts, regenerate consumers together, and test full contracts. Keep unmentioned variants.

```ethos
[ Rank.[ Primary Secondary Tertiary ]
  Voice.{ FlowAspect Rank }
  LaunchRole.[ Voice.Rank Job ]
  StartRequest.{ LaunchProfile OriginClue LaunchRole }
  RecipientResolutionRequest.[ Voice.Voice Flow.FlowId ]
  VoiceBinding.{ Voice Generation Option<FlowId> Option<LaunchRequestId> } ]
```

LaunchRole.Voice supplies Rank; LaunchProfile.FlowAspect supplies Aspect. LaunchRole.Job uses OriginClue.FlowId as owner. Start and Replace use extended StartRequest; role joins request-id equality, so a role difference conflicts. Keep predecessor semantics and no parallel launch endpoint.

```ethos
[ ResolveRecipient.RecipientResolutionRequest
  Voices
  Report.{ FlowId SessionId ReportId Event } ]
[ RecipientResolved.{ FlowNode Option<VoiceBinding> }
  VoicesListed.Vector<VoiceBinding>
  Reported
  Refused.[ UnknownFlow.FlowId
            SessionMismatch.{ FlowId SessionId }
            ReportConflict.ReportId ] ]
[ RecipientResolutionRejection.[ UnknownFlow
                                 FlowUnavailable
                                 VoiceUnbound.Voice
                                 VoiceUnavailable.Voice
                                 FlowEnded.FlowId ]
  StartRejection.[ VoiceConflict.Voice ]
  ReportId.String
  Activity.[ Unknown Idle Working ]
  TurnOutcome.[ Completed Interrupted Failed ]
  EndReason.[ Completed Cancelled Failed Superseded NativeExit ]
  Event.[ SessionStarted
          TurnStarted.TurnId
          TurnCompleted.{ TurnId TurnOutcome }
          ActivityObserved.Activity
          ToolUsed.String
          StopObserved
          SessionEnded.EndReason ] ]
```

VoiceBinding's FlowId is current run; LaunchRequestId is pending handover/start. Generation changes only with current binding. Voice resolution returns binding snapshot; direct FlowId lookup may omit it. Voices lists all nine slots, including unbound. A parser renders/parses Mind.Primary into Voice; arbitrary aliases are no second registry.

```ethos
[ AssignVoice.{ Voice Generation FlowId } ]
[ VoiceAssigned.VoiceBinding
  VoiceAssignmentRejected.[ UnknownFlow AspectMismatch NotRoutable
                            StaleGeneration SlotBusy AlreadyAssignedElsewhere ] ]
```

Assignment compares generation; it cannot route an unreaped successor. No permanent old/new wire path. Move all callers, CLI parsers, emitters, and bindings together. Preserve historic launch records; registry/role indexes must not fabricate old ranks. Bootstrap records explicit assignments; settle/reconcile active pre-upgrade attempts before request-schema change. Wire/version/storage migration is implementation work, never authority to replay launches.

## Start, replacement and routing transitions

For voice Start, atomically admit against its slot before native effects. An unbound slot reserves one pending request; occupied requires Replace with exact current predecessor. Same ID reuses its attempt; competition gets typed VoiceConflict, not ambiguous launch. Persist attempt/role/slot reservation before spawn. A successor becomes routable only after launch readiness and confirmed predecessor reaping. Commit new binding and clear pending atomically with that routing gate. Old-session reports cannot move a name or revive a retired predecessor. Ambiguous launches retain their attempt and reconcile; never relaunch under a new ID. Definitive rejection releases only its slot reservation and uses protected claim release.

ResolveRecipient(Voice) consults slot and current routability. During handover/recovery without a routable run, return VoiceUnavailable. FlowId remains ledger-oriented; terminal job resolution returns FlowEnded. Resolution is a snapshot, not delivery lease. Messenger preserves message identity and returned run/binding, reports an ended/stale destination if it ends before acceptance, and never redirects a stale job message to successor. It may resolve a voice again only after definite stale-binding rejection, never ambiguous delivery. This adds neither exactly-once delivery nor a second Flow queue.

## State, hooks and restart

Keep FlowLifecycle separate from turn activity/observations. Active+Idle is live. StopObserved is a hint; it cannot retire a run or prove a final turn. SessionStarted does not route a successor. Existing launch/reaping gate alone does. Terminal lifecycle comes from confirmed native end, explicit Stop/job completion, or replacement; connection loss yields unknown activity, not invented exit. An ended lifecycle cannot be revived by later hints. TurnCompleted updates only its matching TurnId: a late completion cannot mark a newer active turn idle.

Report correlates to held attempt's reserved/bound native SessionId. Pre-registration reports require both reserved identities. Deduplicate `(FlowId,SessionId,ReportId)`: identical replay returns Reported; different content under an ID returns ReportConflict. Append order is receipt order, not global native chronology. This does not claim stronger authentication than local transport. Only designated adapter/controller produces authoritative completion; raw hook hints do not gain that authority.

ReportId deduplication covers retries that reuse an ID; it does not invent a native durable replay identity for hooks or notifications that lack one.

Update Claude consumers to SessionStarted/ToolUsed/StopObserved, including native session and report ID. Stored Started/Stopped migrate to SessionStarted/StopObserved without upgrading certainty. Cut over every emitter together. If authoritative Claude final-turn source is unavailable, expose Unknown after Stop hint, not false completion. Confirmed process/session exit still ends run.

Codex's Flow-owned app-server connection consumes thread/started, thread/status/changed, turn/started, turn/completed and correlated errors. Schema states idle/active/notLoaded/systemError and completed/interrupted/failed/inProgress. Map deliberately; notLoaded, disconnect and systemError are not terminal. `willRetry` error does not end a turn. Reconnect performs one native read/reconciliation, retains request/message IDs, resumes notifications, and does not poll. Notifications lack a proven durable replay sequence: promise no lossless historical replay. Persist outcomes before projected state; expose unknown if reconciliation cannot establish truth.

## Codex launch sequence on the existing coordinator

Current adapter opens/spawns TUI, discovers/binds session, then sends first turn; it does not pass FLOW_SOCKET/FLOW_ID into remote tools. Existing direct thread/start can set shell_environment_policy, and first-turn delivery checks empty thread, resolves native skills/list, sends skill objects, then composed text. Reuse that controller.

1. Persist Start attempt; connect and initialize once. `thread/start` creates an empty thread with known FLOW_SOCKET and no turn. Persist returned UUID before side effects. Lost response is ambiguous; never create another blindly.
2. Claim FlowId from UUID, create held Flow row and binding candidate; then `thread/resume` same UUID with shell_environment_policy.set for FLOW_ID, FLOW_DIRECTORY, FLOW_SOCKET. Set/read name through adapter. Do not substitute prose or pane-only environment.
3. Open Herdr pane and attach `codex resume <thread-id> --remote unix://<app-server-socket>`. Require bound identity equal persisted UUID; mismatch refuses, never adopts another.
4. Run first-turn admission/skill resolution. Send one durable intent with native skill objects then text. Required launch skills include user-only trial-contact-discipline in first native user turn; generation/installation alone is not delivery evidence.
5. Release routing only after acknowledgement and, for Replace, predecessor reaping. Bridge reports against this FlowId/thread whether TUI is connected.

Installed Codex0.158.0-alpha.9 permits config overrides on thread/resume and documents rejoining thread, but does not prove policy reaches running tool environment. Semi-sandbox must witness harmless tool exact three values and prove attach neither creates a second thread nor implicit first turn. If resume ignores policy, stop that claim and report it: pre-native FlowId reservation/bind design is then needed. Do not invent caller-chosen Codex UUID or silently use text-only injection. This is acceptance, not naming policy.

A Codex failure after thread creation retains the native UUID and claim as evidence. Current protected Release is Claude-only and must not be represented as implemented Codex cleanup: do not delete a nonempty or unidentified session, and do not blindly recreate after ambiguous `thread/start`.

## Sole launch route and delivery boundaries

Flow Start owns allocation, claim, native creation, pane attachment, registration/title, and first-turn submission. Standalone Claude/Codex callers become Start clients; they may assemble validated inputs but perform none of those effects. Remove standalone implementation only once both harness routes pass acceptance witnesses and consumers/tests migrate. No launcher retires before replacement is witnessed.

Admission is only readable working directory/harness/prompt/first-turn inputs and correct configured CLI/socket pair. No ancestry, parent-tree equality, clean checkout, implicit JJ snapshot, or publication repair belongs in Start. An actively replaced workspace may temporarily refuse; unpublished flow records alone do not.

## Implementation slices and acceptance

A. Contracts/registry: generate/compile all consumers; test nine values, rank/power separation, unknown/unbound resolution, assignment generation/aspect checks, simultaneous Start conflict, role-mismatch replay, exact-predecessor Replace and routing only after reaping; test terminal-job resolution and end-between-resolution/message acceptance in messaging consumer.

B. Report/bridge: test reserved-session correlation, duplicate/conflicting IDs, Stop never retiring voice, old session never changing successor, ended never revived, disconnect→unknown, and one reconciliation without polling. Failures invent no Started/Ended fact.

C. Codex: isolated app server/socket/store and disposable thread; verify UUID, environment policy before first tool, exact attachment, skill objects in first turn, one submission under retry, failure/ambiguity, lifecycle notifications, and wrong CLI/socket rejection. These are non-production witnesses; actual voice launch/restart is separately assigned.

D. Sole Start: witness Claude and Codex semi-sandbox Starts and a replacement where predecessor is unavailable before successor routing. Inspect transcript/native input/ledger, not command exit. Inventory/migrate launcher consumers, then retire duplicate logic. Guard-removal can land independently; it does not prove sole Start.

Use existing0.24 reservation/prompt-intent fixtures; add missing behavior, not parallel infrastructure. Mind Sol reviews contract/design and candidate; Field builds/witnesses. No new living ruling: naming and finite-job semantics are settled. Initial slots are explicit operational input, never guesses from model names.

## Sources

- Supplied [Fable Flow report](/home/li/primary/flows/f1c841/reports/flow-next.md:1): it attributes 0.23 `636214e5`; direct source is 0.24 `4ad596d466a45de56239c55d415474f8b35ab163`, and `next-f1c841` is empty child `2cb4df5b6d7b119209c9a0dd4602f99d8d026413`.
- 0.24 pins: [Cargo.toml](/home/li/wt/github.com/LiGoldragon/flow/next-f1c841/Cargo.toml:17), [ordinary Signal](/home/li/.cargo/git/checkouts/signal-flow-688d1620dbb6a864/f95034d/ethos/signal.ethos:82), [meta Signal](/home/li/.cargo/git/checkouts/meta-signal-flow-d6ff5e00f45b353b/54eb561/ethos/signal.ethos:31).
- [Start/release](/home/li/wt/github.com/LiGoldragon/flow/next-f1c841/crates/flow-nexus/src/launching.rs:77), [claim release](/home/li/wt/github.com/LiGoldragon/flow/next-f1c841/crates/flow-nexus/src/herdr/reservation.rs:76), [event append](/home/li/wt/github.com/LiGoldragon/flow/next-f1c841/crates/flow-nexus/src/store/events.rs:103), [Report](/home/li/wt/github.com/LiGoldragon/flow/next-f1c841/crates/flow-nexus/src/reporting.rs:22), [Claude hook](/home/li/wt/github.com/LiGoldragon/flow/next-f1c841/crates/flow/src/hook.rs:1), [roles](/home/li/wt/github.com/LiGoldragon/flow/next-f1c841/crates/flow-nexus/src/store.rs:217).
- [Vision Flow](/home/li/primary/.agents/skills/vision-flow/SKILL.md:6), [knowledge Flow](/home/li/primary/.agents/skills/knowledge-flow/SKILL.md:6). Codex evidence: installed `codex-cli0.158.0-alpha.9`; offline generated schema/TS at `/tmp/codex-app-server-schema-dea0ba.uhcC1A/{v2/ThreadResumeParams.json,ts/v2/ThreadResumeParams.ts,v2/ThreadStartParams.json,ServerNotification.json,v2/ThreadStatusChangedNotification.json,v2/TurnStartedNotification.json,v2/TurnCompletedNotification.json,v2/ErrorNotification.json}`. Generation ran installed binary because wrapper injected `--remote`; no server was contacted. Relevant Flow source: [codex.rs](/home/li/wt/github.com/LiGoldragon/flow/next-f1c841/crates/flow-nexus/src/codex.rs:238), [Herdr launch](/home/li/wt/github.com/LiGoldragon/flow/next-f1c841/crates/flow-nexus/src/herdr/launch.rs:1311), [reservation](/home/li/wt/github.com/LiGoldragon/flow/next-f1c841/crates/flow-nexus/src/herdr/reservation.rs:67).
