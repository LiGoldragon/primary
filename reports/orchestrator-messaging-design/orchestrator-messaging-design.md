# Orchestrator messaging + decision seat — design (amended)

Status: authoritative pickup for implementation workers. Session-wide design,
psyche-approved. This report is the settled specification for the
orchestrator-messaging build. The "Settled Decisions" section is closed; do not
reopen its choices without a new psyche-level decision.

## Orientation

The orchestrator is a decision seat and addressee inside the `orchestrate`
component. It is the agent-facing coordination surface: agents register, are
seated on topics, and become addressable at their minted identity. The router
stays the invisible local delivery daemon; the message component stays a
stateless ingress that mints threads. This build adds the wire vocabulary for
registration, topic/agent observation, the semantic message payload, and the
orchestrator judge (topic assignment + triage).

Three wire-contract surfaces carry the design:

1. Additions to the existing `signal-orchestrate` crate — registration, topic,
   and agent vocabulary plus request/reply additions.
2. New `signal-orchestrator-message` crate — the semantic payload contract
   carried inside the opaque message body.
3. New `signal-orchestrator-judge` crate — the typed request/reply contract
   between orchestrate and the orchestrator judge adapter (topic assignment and
   message triage).

## Settled Decisions

- Orchestrator = decision seat and addressee inside the orchestrate component;
  router stays the (invisible, local) delivery daemon; message stays a stateless
  ingress. Local traffic is default-authorized — NO per-agent-pair channel
  grants in this build; grant/attestation ceremony is reserved for future
  network-crossing delivery. The previously-designed `channel_grants` table and
  `GrantDirectMessage` ordering are DROPPED from this build.
- The minted registration ID (Spirit's mint: random base36, 4–7 chars starting
  at length 4, uniqueness-checked, length grows on saturation — reference
  `/home/li/primary/repos/spirit/src/store/record_identifier.rs`) is the
  canonical agent address: orchestrate identifier = router `ActorIdentifier` =
  message recipient.
- Registration has two modes: Automatic (judge assigns topics from the mission)
  and Explicit (agent names its topics; no judge call). The mission description
  is MANDATORY in both modes — the judge and every future orchestrator function
  use it. If the topic judge is unavailable in Automatic mode, registration
  returns a typed rejection CARRYING the current topic list so the caller can
  retry explicitly. There is no catch-all fallback seating. The catch-all topic
  exists only as the coordinator's home and escalation target.
- Message kinds are semantic only and live in the NOTA payload: `Guidance`
  (magnitude Soft | Standard | Hard; the default kind, fold in at next natural
  turn), `Interruption` (semantically urgent, not a transport interrupt),
  `Report` (raise for attention; normal destination the orchestrator). There is
  NO `Question` kind: threads are explicit, and a question is an ordinary thread
  message whose body asks something. `HardInterruption` is reserved-absent
  (documented in the crate).
- Threads: a new thread is minted by the message daemon (context-cheap short
  name, same mint discipline) and returned in the acceptance reply; replies name
  the existing thread. The message-component changes are a separate lane; the
  message payload contract here carries NO thread field (threading is
  transport-level).
- Reachability is discovered at registration (SO_PEERCRED pid + /proc ancestry
  walk + terminal-cell session-dir matching), not declared by the caller. The
  registration request therefore carries NO caller-supplied reachability field.
  The discovery mechanism is a separate lane; this contract only keeps a
  reachability slot out of the request.
- Triage: a message addressed to the orchestrator may be routed as-is, retyped,
  rewritten, fanned out to multiple recipients, or escalated to the coordinator.
  The verdict type makes spawning inexpressible — no spawn/new-session variant
  exists.
- Registration sits on the ordinary `signal-orchestrate` contract tier (the
  registering agent is a peer, no meta authority).

## Contract Shapes

Pseudo-NOTA, angle-bracket placeholders, `?` marks an optional-as-typed-data
field, `|` separates enum variants. Field types are adapted to each crate's real
codec conventions (see Integration Seams).

### signal-orchestrate additions

Shared vocabulary:

- `OrchestratorAgentIdentifier` — string newtype, the minted canonical address.
- `OrchestratorTopicPath` — string newtype, slash-separated topic path.
- `TopicName` — string newtype, short topic label.
- `MissionDescription` — non-empty prose, mandatory in both registration modes.
- `OrchestratorTopic { path.OrchestratorTopicPath name.TopicName parent.(Optional OrchestratorTopicPath) }`
- `OrchestratorAgentStatus [ Active Retired ]`
- `OrchestratorAgentSummary { agent-id.OrchestratorAgentIdentifier mission.MissionDescription topics.(Vector OrchestratorTopicPath) status.OrchestratorAgentStatus }`
- `TopicAssignmentSource [ Judge Explicit ]`

Request additions:

- `(RegisterAgent (OrchestratorAgentRegistration <session> <mission> <harness> <topic-selection>))`
  where `<topic-selection>` is `TopicSelection [ Automatic (Explicit (Vector OrchestratorTopicPath)) ]` —
  strict positional, no omitted slots, no caller-supplied reachability slot.
- Topic/agent observation folds into the existing `Observe(Observation)`
  operation as new `Observation` variants: `Topics`, `(Topic OrchestratorTopicPath)`,
  `Agents`. This dissolves topic/agent reads into the crate's established
  observation normal case rather than adding parallel operation heads (see
  "Deviations" below); it is the design-quality-correct expression of the brief's
  `(ObserveTopics)`, `(QueryTopic <topic-path>)`, `(ObserveAgents)`.

Reply additions:

- `(AgentRegistered <agent-id> <assigned-topics> <assignment-source>)` —
  `assigned-topics.(Vector OrchestratorTopic)`, `assignment-source.TopicAssignmentSource`.
- `(AgentRegistrationRejected <reason> <available-topics>)` with
  `AgentRegistrationRejectionReason [ MissionEmpty MissionTooVague UnknownTopic JudgeUnavailable JudgeMalformed JudgeTimedOut ]`.
  The `available-topics.(Vector OrchestratorTopic)` vector is always present so a
  judge-down caller can retry explicitly.
- `(TopicTree <topics>)` — `topics.(Vector OrchestratorTopic)`.
- `(TopicDetail <topic> <member-agent-ids>)` —
  `topic.OrchestratorTopic`, `member-agent-ids.(Vector OrchestratorAgentIdentifier)`.
- `(AgentDirectory <agents>)` — `agents.(Vector OrchestratorAgentSummary)`.

`OperationKind` gains `RegisterAgent`. `Observe` remains a single operation head.

### signal-orchestrator-message

The semantic payload carried inside the opaque message body:

- `(OrchestratorMessage <kind> <subject> <content>)`
- `OrchestratorMessageKind [ (Guidance GuidanceMagnitude) Interruption Report ]`
- `GuidanceMagnitude [ Soft Standard Hard ]`
- `MessageSubject` — short single line.
- `MessageContent` — prose or nested NOTA body text.

`HardInterruption` is deliberately absent/reserved — documented in the crate.
No thread field: threading is transport-level.

### signal-orchestrator-judge

Mirrors `signal-spirit-judge`'s shape (hand-written rkyv + NOTA, `ExchangeFrame`,
`JudgmentScope`/`JudgeDiagnostic`, request-rejection split).

- `OrchestratorJudgeRequest [ (AssignTopic TopicAssignmentPacket) (TriageMessage TriagePacket) ]`
- `OrchestratorJudgeReply [ (TopicAssigned TopicAssignmentResponse) (MessageTriaged TriageResponse) (RequestRejected OrchestratorJudgeRequestRejection) ]`
- `(TopicAssignmentPacket <scope> <mission> <existing-topics>)`
- `TopicAssignmentVerdict [ (Assign TopicAssignment) (Reject TopicAssignmentRejectionReason) ]`
- `(TopicAssignment <reuse-topics> <create-topics>)` with `(NewTopic <parent-path?> <name>)`
- `TopicAssignmentRejectionReason [ MissionTooVague MissionEmpty ]`
- `(TriagePacket <scope> <incoming> <sender> <topic-directory> <agent-directory>)`
- `TriageVerdict [ (Route TriageRouting) (Escalate EscalationNote) (Reject TriageRejectionReason) ]`
- `(TriageRouting <recipients> <retyped-kind?> <rewritten-message?>)` — optionality
  as typed positional data, never omitted slots.
- `(EscalationNote <coordinator-reason> <detail>)`
- `TriageRejectionReason [ NoEligibleRecipient SenderNotRegistered MalformedPayload ]`
- Shared: `JudgmentScope [ Public (Private ...) ]`, `JudgeDiagnostic` with
  redaction, `OrchestratorJudgeRequestRejection` with reasons
  `[ InvalidRequest ConfigurationUnavailable ProviderUnavailable ProviderRejected ResponseFormatFailure ]`
  — mirroring the spirit-judge equivalents exactly.

The caller-side fail-closed reasons (`JudgeUnavailable`/`JudgeMalformed`/
`JudgeTimedOut`) live in `signal-orchestrate`'s registration rejection and in
orchestrate's triage handling — NOT in this crate's model-facing verdicts,
matching how spirit separates transport failure from model verdicts.

## Storage

The orchestrate daemon (separate lane) persists:

- A topic tree: each `OrchestratorTopic` (path, name, optional parent). The
  catch-all topic is the coordinator's home and escalation target; it is not a
  fallback seat for ordinary registration.
- An agent registry: each registered agent keyed by minted
  `OrchestratorAgentIdentifier`, carrying mission, seated topics, and status
  (`Active`/`Retired`).
- No `channel_grants` table — dropped from this build. Local delivery is
  default-authorized.

The minted identity is the join key across orchestrate (registry), router
(`ActorIdentifier`), and message (recipient).

## Flows

Registration (Automatic):

1. Agent sends `RegisterAgent` with session, mission, harness, `Automatic`.
2. Daemon mints the identity, discovers reachability (separate lane), calls the
   orchestrator judge `AssignTopic` with scope, mission, existing topics.
3. Judge returns `TopicAssigned` (reuse + create topics) or a rejection.
4. On success the daemon persists the seating and replies `AgentRegistered` with
   `assignment-source = Judge`.
5. If the judge is unavailable/malformed/timed-out, the daemon replies
   `AgentRegistrationRejected` with the transport reason and the current topic
   list, so the caller can retry with `Explicit`.

Registration (Explicit):

1. Agent sends `RegisterAgent` with `Explicit [topic-paths]`; mission still
   mandatory.
2. Daemon validates the named topics; unknown topic → `AgentRegistrationRejected
   UnknownTopic` with the available topics.
3. On success replies `AgentRegistered` with `assignment-source = Explicit`. No
   judge call.

Message triage:

1. A message addressed to the orchestrator arrives (payload =
   `OrchestratorMessage`).
2. Orchestrate calls the judge `TriageMessage` with scope, incoming message,
   sender, topic directory, agent directory.
3. Judge returns `Route` (recipients, optional retyped kind, optional rewritten
   message), `Escalate` (to coordinator with reason + detail), or `Reject`.
4. Spawning is inexpressible in the verdict type.

Observation: agents/tools read the topic tree (`Observe Topics` →
`TopicTree`), a single topic with members (`Observe (Topic path)` →
`TopicDetail`), or the agent directory (`Observe Agents` → `AgentDirectory`).

## Integration Seams

- `signal-orchestrate` is the hand-written-`src/lib.rs` + schema-mirror crate:
  types carry `rkyv` archive derives and NOTA codecs, operations/replies are
  declared in the `signal_channel!` macro, and `schema/lib.schema` is authored to
  match with the generated `src/schema/lib.rs` mirror regenerated through
  `SIGNAL_ORCHESTRATE_UPDATE_SCHEMA_ARTIFACTS`. New vocabulary follows the
  existing newtype macros (`validated_token_type!`) and struct-with-rkyv style.
- `signal-orchestrator-message` is a payload-only contract (no request/reply
  channel), so it follows the hand-written `signal-spirit-judge` codec style
  (rkyv + optional NOTA derives, `thiserror` boundary error, non-empty text
  newtypes) rather than `signal-message`'s generated channel scaffold, which
  assumes an ingress operation set this payload does not have.
- `signal-orchestrator-judge` mirrors `signal-spirit-judge` directly:
  hand-written `src/lib.rs`, `ExchangeFrame` request/reply aliases,
  `JudgmentScope`, `JudgeDiagnostic`, and a concept schema sketch under
  `schema/`. It depends on `signal-orchestrate` for topic/agent vocabulary and on
  `signal-orchestrator-message` for the message type.
- The minted-identity discipline, reachability discovery, thread minting, and
  daemon storage are separate lanes; these contracts only fix the wire vocabulary
  and deliberately keep those concerns off the wire.

## Deviations from the brief's literal shape

- The brief lists `(ObserveTopics)`, `(QueryTopic <topic-path>)`,
  `(ObserveAgents)` as request forms. The existing crate already carries an
  `Observe(Observation)` operation whose enum selects Roles/Sessions/Lanes/
  Worktrees and returns distinct reply types. Topic/agent reads are expressed as
  new `Observation` variants (`Topics`, `(Topic OrchestratorTopicPath)`,
  `Agents`) so the special case dissolves into the crate's established normal
  case, exactly matching the parameterized `(SessionLanes SessionIdentifier)`
  precedent. This preserves the brief's semantics while fitting local patterns.

## Prompt-Pack Outlines

Two model-facing prompt packs will be authored by the daemon/adapter lane, not
here. This report fixes the typed surface they must produce:

- Topic-assignment pack: input is scope + mission + existing topics; the model
  must answer a `TopicAssignmentVerdict` — either `Assign` (naming reuse topics
  and new topics with optional parent) or `Reject` (`MissionTooVague` |
  `MissionEmpty`). Include the `signal-orchestrator-judge` schema/help projection
  or concrete NOTA examples in the prompt; provide the diagnostic branch for
  explainable ambiguity.
- Triage pack: input is scope + incoming message + sender + topic directory +
  agent directory; the model must answer a `TriageVerdict` — `Route` (recipients,
  optional retyped kind, optional rewritten message), `Escalate` (coordinator
  reason + detail), or `Reject`. Spawning is not expressible. Include the schema
  projection and the diagnostic branch.

Both packs answer expression-only NOTA except the diagnostic branch, which may
carry prose, matching spirit-judge prompt discipline.

## Slice Plan

1. Slice A — `signal-orchestrate` vocabulary + request/reply additions + schema
   mirror regenerate + round-trip tests. (This lane.)
2. Slice B — `signal-orchestrator-message` payload crate + round-trip tests.
   (This lane.)
3. Slice C — `signal-orchestrator-judge` crate depending on A and B + round-trip
   tests. (This lane.)
4. Slice D — orchestrate daemon: minted identity, reachability discovery, topic
   tree + agent registry storage, judge calls, triage handling. (Separate lane.)
5. Slice E — message component: thread minting, `OrchestratorMessage` payload
   carriage in the message body. (Separate lane.)
6. Slice F — prompt packs + judge adapter wiring. (Separate lane.)

New repos `signal-orchestrator-message` and `signal-orchestrator-judge` are
created local-only; GitHub publication is a separately gated step and is not
performed by this lane.
