# Message anatomy for the living — order 10

This is an editable design proposal, with the current wire contract identified
separately. The complete proposed Ethos file appears below and is also saved as
`order10-message.ethos`. The proposed additions and worked text are not claimed
to have passed Ethos generation or the production datom parser. Runtime order
10B will have its own exact implementation and parser/delivery receipts.

## What exists, and what should own it

A flow is one node in the cluster graph. Its stable identity, current session,
and observed ability to receive a turn belong to **Flow**. Message asks Flow for
that information, chooses a supported transport, and records delivery evidence.
Message must not create a second independently maintained flow-name registry.

| Existing thing | What it establishes | What it does not establish |
|---|---|---|
| `flow-id` | A session-derived alias and lane claim marker | A route, a live idle state, or authenticated authority from an arbitrary supplied alias |
| Orchestrate | Attribution and ownership of coordinated locks | Which harness session called Message, a cluster roster, or routing authority |
| Message agent registry | Agent identifiers, endpoint/resume/process-pin records | The Flow cluster's session/name/idleness registry |
| Item 35 Flow prototype | Reads `.flow-id` markers, validates unique identities, supports in-memory query/subscription and checked observation publishing | An activated IPC service, automatic route discovery, or process-authenticated callers |
| Current relay environment | Declared executor flow/session and supplied cluster membership; relay checks consistency | Proof that environment variables cannot be forged |

Root read the item 35 implementation at primary checkout
`cf7879-flow-idleness-poc`, revision `2139b80c4d4ec25708eb49150751399d24e59cc5`,
`tools/flow-idleness-registry.mjs`. It validates markers and rejects mismatched
harness/session identities when publishing observations. Its subscription is a
local callback set. The companion `flow-idleness.mjs` reads the last Codex turn
and refuses to equate completed turns with idle when the supplied operational
state is busy, approval-wait, or unknown. None of that is a deployed registry
receipt.

**Proposed one owner:** extend that Flow-owned source into a typed query service.
The Message CLI's `WhoAmI` and `Routes` commands delegate to it. During the
stopgap, a configured snapshot and self-declared caller are labelled `Declared`.
Later the host associates peer PID/start-time/session with its registered Flow;
only a witnessed association earns `ProcessSessionObserved` or `RegistryBound`.
A PID alone is insufficient because it can be reused. An alias is a name, not
an authentication token. This preserves the living's current goodwill model
without representing it as stronger authentication.

## The three identities in one delivery

1. **Caller:** the flow invoking the CLI now, such as cf7879.
2. **Source:** the flow/session whose transcript contains the original words,
   such as efa157. Relaying those words does not make cf7879 their author.
3. **Recipient:** the flow to which a route attempt is addressed.

For a peer-authored note, the source is explicitly a peer note. A temporary
peer-file path and content hash must never be dressed up as a human transcript
turn. For a human transcript relay, locate the original bytes, check the source
record and hash, and preserve those words. The Context is an interpretation
beside the words, not a replacement for them or a claim of human authorship.

## Current ClusterMessage and Context

Message main `fe0d04561051da85292a058ab156e286b7494aa4` selects signal-message
`a9708f3384af18129cb1c983ffed850c4d631e46` in Cargo.lock. This selected dependency,
not whichever branch a local signal-message checkout happens to show, governs
its current relay contract. Root independently observed remote signal-message
main at `65d6e2e2fafebaa246557b61ca786e3f382a1bb4`; its contents were not inspected
for this report, so no assertion that current upstream main lacks the contract
is made.

The selected relay shape is:

```ethos
ClusterTarget.[Primary Secondary Core]
ClusterMember.{FlowIdentifier SessionIdentifier}
ClusterMembers.Vector<ClusterMember>
Context.{FlowIdentifier SourceTurnIdentifier TranscriptPath PromptSha256 WhatLivingSaid ContextAbout ContextAnswered ContextCorrected ContextUncertainties}
ClusterRelay.{FlowIdentifier SessionIdentifier TranscriptPath PromptFirstSixWords PromptLastSixWords PromptSha256 Context TimestampNanos ClusterTarget ClusterMembers}
ClusterMessage.[Relay.ClusterRelay]
```

The identifier names currently wrap/alias String in Ethos. Their names express
intent; they do not by themselves prove UUID/hash grammar or process binding.
Those validations must be implemented and tested. Item 32's stronger identifier
proposal is not silently adopted here.

Current `relay` creates the header with the actual datom/protos codec and appends
the unchanged body. Context is structurally present. Without a context-machine
receipt, the current code fills explicit `unreviewed`/`unavailable` fields and
retains the source words; this is not an inferred analysis. A supplied context
receipt is checked against source identity/hash/words. Current ordinary
`message` parses `signal_message::Query`, not `ClusterMessage`, which is the
concrete CLI gap order 10B must close.

## Reading the proposed types

- `CallerIdentity` keeps a declared identity distinct from a checked binding.
- `FlowNode` joins flow, session, harness, role, idleness evidence and routes.
- `RouteListing` is one observed registry revision. `ValidUntil` is a freshness
  deadline, not a prediction that a session stays idle. The PTY gate still checks
  at delivery time. Approval-wait never becomes idle by timeout.
- `DeliveryRequest` keeps the caller outside the source-bearing message.
- `ClusterMessage.Peer` is an additive proposal so peer notes cannot masquerade
  as human `Relay` records. It does not change the existing Relay field order.
- `ReceiptKind` distinguishes acceptance, observed transcript content, durable
  parking and file-only reporting. `Pending` explains why no delivery exists.

A recipient transcript containing the exact datom is the acceptance test for
order 10B. Queue acceptance is useful but weaker. `FileOnly` says that a report
was written; it does not say anyone read it. `Parked` requires a real persisted
outbox entry; an in-memory intention to send is not parked.

## Complete proposed Ethos

```ethos
Signal
[]
[ Routes.RouteQuery WhoAmI.IdentityProbe Deliver.DeliveryRequest DeliveryStatus.DeliveryStatusQuery ]
[ RoutesListed.RouteListing IdentityResolved.CallerIdentity DeliveryRecorded.DeliveryReport Refused.RouteFailure ]
[
  FlowIdentifier.String
  SessionIdentifier.String
  SourceTurnIdentifier.String
  SourceEventIdentifier.String
  TranscriptPath.String
  PromptFirstSixWords.String
  PromptLastSixWords.String
  PromptSha256.String
  TimestampNanos.Integer
  WhatLivingSaid.String
  ContextAbout.String
  ContextAnswered.String
  ContextCorrected.String
  ContextUncertainties.Vector<String>
  ClusterTarget.[Primary Secondary Core]
  ClusterMember.{FlowIdentifier SessionIdentifier}
  ClusterMembers.Vector<ClusterMember>
  Context.{FlowIdentifier SourceTurnIdentifier TranscriptPath PromptSha256 WhatLivingSaid ContextAbout ContextAnswered ContextCorrected ContextUncertainties}
  ClusterRelay.{FlowIdentifier SessionIdentifier TranscriptPath PromptFirstSixWords PromptLastSixWords PromptSha256 Context TimestampNanos ClusterTarget ClusterMembers}

  HarnessKind.[Codex Claude]
  IdentityEvidence.[Declared ProcessSessionObserved RegistryBound]
  CallerIdentity.{FlowIdentifier SessionIdentifier HarnessKind IdentityEvidence}
  PeerBody.String
  PeerSourcePath.String
  PeerSha256.String
  PeerProvenance.{PeerSourcePath PeerSha256}
  PeerMessage.{SourceEventIdentifier CallerIdentity PeerProvenance PeerBody}
  ClusterMessage.[Relay.ClusterRelay Peer.PeerMessage]

  ProcessId.Integer
  ProcessStartedAt.Integer
  ProcessObservation.{ProcessId ProcessStartedAt}
  ProcessSelection.[Known.ProcessObservation Unknown]
  ClaimedIdentity.[Claimed.CallerIdentity None]
  IdentityProbe.{ProcessSelection ClaimedIdentity}

  IdleState.[Idle Busy ApprovalWait Unknown Concluded]
  IdleEvidence.[HarnessTurn DaemonRoster TranscriptEnd Unavailable]
  ObservedAt.Integer
  ValidUntil.Integer
  Observation.{IdleState IdleEvidence ObservedAt ValidUntil}
  RouteKind.[CodexQueue CodexTurnStart ClaudePromptRelay MessageOutbox LaneFile]
  Endpoint.String
  Route.{RouteKind Endpoint}
  Routes.Vector<Route>
  FlowRole.[Primary Secondary Core Successor]
  FlowNode.{FlowIdentifier SessionIdentifier HarnessKind FlowRole Observation Routes}
  Nodes.Vector<FlowNode>
  NodeSelection.[All Cluster.ClusterTarget One.FlowIdentifier]
  RouteQuery.{CallerIdentity NodeSelection}
  RegistryRevision.String
  RouteListing.{RegistryRevision ObservedAt Nodes}

  TargetFlows.Vector<FlowIdentifier>
  DeliveryRequest.{CallerIdentity ClusterMessage TargetFlows}
  DeliveryStatusQuery.SourceEventIdentifier
  ByteCount.Integer
  TransportReceiptId.String
  TranscriptRecordId.String
  ReportPath.String
  OutboxEntryId.String
  AcceptedReceipt.{TransportReceiptId ObservedAt}
  TranscriptReceipt.{TranscriptPath TranscriptRecordId PromptSha256 ByteCount ObservedAt}
  ParkedReceipt.{OutboxEntryId ObservedAt}
  FileReceipt.{ReportPath ObservedAt}
  PendingReason.[Busy ApprovalWait UnknownRoute StaleObservation TransportUnavailable WitnessPending]
  PendingReceipt.{PendingReason ObservedAt}
  ReceiptKind.[Accepted.AcceptedReceipt TranscriptWitnessed.TranscriptReceipt Parked.ParkedReceipt FileOnly.FileReceipt Pending.PendingReceipt]
  RecipientReceipt.{SourceEventIdentifier FlowIdentifier RouteKind ReceiptKind}
  RecipientReceipts.Vector<RecipientReceipt>
  DeliveryReport.{SourceEventIdentifier RecipientReceipts}
  RouteFailureReason.[UnknownCaller IdentityMismatch UnknownFlow StaleObservation InvalidDatom SourceMismatch UnsupportedRoute]
  RouteFailure.{RouteFailureReason}
]
```

## Worked datom examples

All examples below are **illustrative values, not live receipts or commands
that have been submitted**. They use real flow names for orientation but
synthetic source paths/record IDs and timestamps. The sample body hash is
computed from the displayed UTF-8 sentence; that computation does not create
a transcript witness. Production examples must be rendered and parsed by the
selected generated types.

Enum values begin with the variant. Struct values are positional braces; a
standalone Context does **not** gain a `Context.` constructor. String values
are shown with guillemets, even where a bare atom could be accepted.

### Current Context, ClusterMember and Relay

Context fields in order: source flow, source turn, transcript, body hash, exact
words, topic, answered, corrected, uncertainties.

```datom
{ «efa157» «demo-source-turn» «/example/efa157.jsonl» «ce7edacab893549dd4220bd4a65669667cc013bcfc8e39d1552b3aaafae1bb94» «The successor package is ready for review.» «Successor package review» «A request for readiness» «No correction asserted» [ «Example context, not a model receipt» ] }
```

One ClusterMember:

```datom
{ «d9961c» «01a0aacb-ac84-71a1-88a0-05ed9961ca9d» }
```

Current Relay, with that Context and one destination member:

```datom
Relay.{ «efa157» «efa15708-dc5d-42ce-af62-8ffb84c9815e» «/example/efa157.jsonl» «The successor package is ready for» «successor package is ready for review.» «ce7edacab893549dd4220bd4a65669667cc013bcfc8e39d1552b3aaafae1bb94» { «efa157» «demo-source-turn» «/example/efa157.jsonl» «ce7edacab893549dd4220bd4a65669667cc013bcfc8e39d1552b3aaafae1bb94» «The successor package is ready for review.» «Successor package review» «A request for readiness» «No correction asserted» [ «Example context, not a model receipt» ] } 1789574400000000000 Primary [ { «d9961c» «01a0aacb-ac84-71a1-88a0-05ed9961ca9d» } ] }
```

The existing relay wire text appends the exact original sentence after this
header. Do not relabel the source flow as the CLI executor.

### CallerIdentity, IdentityProbe and IdentityResolved

Self-declared caller value:

```datom
{ «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared }
```

The caller asks Flow to resolve a PID/start-time observation and declared
identity; these numbers are demonstration values, not a live process claim.

```datom
WhoAmI.{ Known.{ 1234 5678 } Claimed.{ «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared } }
IdentityResolved.{ «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared }
```

If Flow cannot witness a stronger binding, it returns Declared or refuses. It
must not upgrade the evidence merely because the strings agree.

### PeerMessage and DeliveryRequest

The peer variant has a distinct provenance path and body:

```datom
Peer.{ «demo-peer-1» { «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared } { «/example/peer.txt» «ce7edacab893549dd4220bd4a65669667cc013bcfc8e39d1552b3aaafae1bb94» } «The successor package is ready for review.» }
```

Deliver it, keeping the caller separate from the source-bearing message:

```datom
Deliver.{ { «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared } Peer.{ «demo-peer-1» { «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared } { «/example/peer.txt» «ce7edacab893549dd4220bd4a65669667cc013bcfc8e39d1552b3aaafae1bb94» } «The successor package is ready for review.» } [ «efa157» «d9961c» ] }
```

### RouteQuery and RouteListing, including all six present nodes

```datom
Routes.{ { «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared } All }
Routes.{ { «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared } Cluster.Primary }
Routes.{ { «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared } One.«efa157» }
```

This example deliberately uses Unknown/Unavailable idleness for every node.
It is an anatomy of known identities and possible routes, not a claim that
these routes are currently eligible. Successor d9961c stays Successor until
cf7879's explicit handoff; Claude's unlaunched successor has no invented ID.

```datom
RoutesListed.{ «demo-registry-revision» 1789574400000000000 [
  { «efa157» «efa15708-dc5d-42ce-af62-8ffb84c9815e» Claude Primary { Unknown Unavailable 1789574400000000000 1789574400000000000 } [ { ClaudePromptRelay «efa15708-dc5d-42ce-af62-8ffb84c9815e» } { LaneFile «flows/efa157/log.md» } ] }
  { «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Primary { Unknown Unavailable 1789574400000000000 1789574400000000000 } [ { CodexQueue «01a0a715-2d5d-7342-b278-1dbcf78795bd» } { LaneFile «flows/cf7879/log.md» } ] }
  { «d9961c» «01a0aacb-ac84-71a1-88a0-05ed9961ca9d» Codex Successor { Unknown Unavailable 1789574400000000000 1789574400000000000 } [ { CodexQueue «01a0aacb-ac84-71a1-88a0-05ed9961ca9d» } { LaneFile «flows/d9961c/log.md» } ] }
  { «57a7aa» «57a7aa02-e52d-4266-8746-6770ff770d11» Claude Secondary { Unknown Unavailable 1789574400000000000 1789574400000000000 } [ { ClaudePromptRelay «57a7aa02-e52d-4266-8746-6770ff770d11» } { LaneFile «flows/57a7aa/log.md» } ] }
  { «348e7b» «01a0a11f-6130-70e2-80b1-796348e7b086» Codex Secondary { Unknown Unavailable 1789574400000000000 1789574400000000000 } [ { CodexQueue «01a0a11f-6130-70e2-80b1-796348e7b086» } { LaneFile «flows/348e7b/log.md» } ] }
  { «e43002» «01a0a792-2d0e-7a53-ac0b-9b3e43002941» Codex Core { Unknown Unavailable 1789574400000000000 1789574400000000000 } [ { CodexQueue «01a0a792-2d0e-7a53-ac0b-9b3e43002941» } { LaneFile «flows/e43002/log.md» } ] }
] }
```

Each row demonstrates FlowNode, Observation and Route. MessageOutbox is a
different route: it becomes eligible only when the live Nexus can durably park
and later drain that recipient. A route being listed never proves it works.

### ReceiptKind, RecipientReceipt, DeliveryReport and DeliveryStatus

```datom
DeliveryRecorded.{ «demo-peer-1» [
  { «demo-peer-1» «cf7879» CodexQueue Accepted.{ «demo-transport-ack» 1789574400000000000 } }
  { «demo-peer-1» «efa157» ClaudePromptRelay TranscriptWitnessed.{ «/example/efa157.jsonl» «demo-recipient-record» «ce7edacab893549dd4220bd4a65669667cc013bcfc8e39d1552b3aaafae1bb94» 42 1789574401000000000 } }
  { «demo-peer-1» «57a7aa» MessageOutbox Parked.{ «demo-outbox-row» 1789574402000000000 } }
  { «demo-peer-1» «e43002» LaneFile FileOnly.{ «/example/core-report.md» 1789574403000000000 } }
  { «demo-peer-1» «348e7b» CodexQueue Pending.{ WitnessPending 1789574404000000000 } }
] }
DeliveryStatus.«demo-peer-1»
```

The byte count above refers to the 42-byte sample sentence, not an entire
recipient record including its header. The final contract must specify which
byte range each hash/count covers. Prefer separate body hash and delivered
payload hash if both are needed, never switch their meanings silently.

### Typed refusal

```datom
Refused.{ UnknownCaller }
Refused.{ IdentityMismatch }
Refused.{ StaleObservation }
Refused.{ SourceMismatch }
```

## Implementation and adoption boundaries

The anatomy is intended for editing with the living. Existing Relay compatibility
is preserved in the proposal; Peer, route queries, identity replies and richer
receipts are additions. Adding variants or fields is not automatically archive
or wire compatible. Each adoption needs a contract version and typed upgrade
operation, generated-code check, parser fixtures and old-record/migration tests
where stored data changes. This report does not apply the deployed Message
schema-3 migration or claim its pending row recovered.

For the first live loop, a configured Flow-owned route snapshot is acceptable
if its provenance/freshness and caller declaration are explicit. Do not block
a working datom relay on inventing a new authentication system. Conversely, do
not call that configuration an activated Flow registry or a live Routes query.
The report below will name exactly what order 10B actually implements and which
recipient transcripts contain its datom.
