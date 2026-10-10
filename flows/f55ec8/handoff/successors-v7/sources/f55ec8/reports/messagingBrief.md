# Messaging brief — the material for the idea book

Gathered by subflow f55ec8 on 2026-09-16 for the main flow's idea book of the
messaging system in its final design. Everything below is quoted or cited; where
a thing does not exist it is said so. Nothing here is a receipt of its own.

Sources read: `flows/efa157/vision/{messages,transcriptReporting,callerIdentity,heartbeat,domains,layers,mcp,cloudHosts}.md`;
`flows/f55ec8/vision/{networking,cloud,quota,layers}.md`; `Vision/{nexus,signal,datom}.md` on main;
`flows/efa157/reports/ordersToCodex-2026-09-16.md` (orders 3, 4, 9, 10, 13, 15);
`flows/cf7879/reports/{to-efa157.md,to-secondary.md,order10-message.ethos}`.
`order10-message.ethos` is byte-identical to the Ethos block inside to-efa157.md.

---

## (a) The final-design picture

1. **A message is a typed value, and the typed value is what a recipient reads** —
   one datom object arrives in the user prompt, never a JSON envelope.
   *Source:* the living, `efa157/vision/messages.md`: "let's use the message CLI so
   that that's the prompt that people see. I don't want to see JSON anymore … I want
   to see that system go live and test it so that I see actual Datom objects coming
   in and coming into the user prompts when Flow wants to message others."
   Order 10B makes it the acceptance test: "Datom in the prompt is the acceptance test."

2. **The CLI is the only place text exists; the Nexus thinks only in signal.**
   *Source:* `Vision/signal.md`: "The textual form is datom; a CLI actualizes it and
   sends signal; a Nexus never textualizes." `Vision/nexus.md`: "Every client speaks to
   a Nexus in pure signal, fully binary." The `nexus` skill: "Every Nexus CLI process
   takes exactly one positional argument: a typed input object in datom textual data
   format. No flags, no subcommands."

3. **Every flow is one node in one graph, and the CLI can list the nodes and the
   routes to them**, each node carrying its harness, session, role, and an observed
   idleness with the evidence that observed it and a freshness deadline.
   *Source:* the living, `messages.md`: "It can also get a list of the available routes
   through the CLI of the current flow nodes, or the flow is a node right in this graph."
   Shape: `FlowNode`, `Observation`, `RouteListing` in order 10A (`to-efa157.md`).

4. **Identity is observed through the socket, not asserted in the payload**, and it
   rides as a standard, optional part of the signal library so every caller knows to
   declare whether it has a process id.
   *Source:* the living, `efa157/vision/callerIdentity.md`: "have I checked the socket
   of the process? Can I identify the process that used this CLI, so we can know for
   sure? The Nexus can know if it's Flow … It would have to be added in the signal
   library, because then whoever talks to that socket needs to know to tell it if it
   has the process ID or not, right?"

5. **Identity has exactly one owner, and Message is not it.**
   *Source:* cf7879, order 10A: "A flow is one node in the cluster graph. Its stable
   identity, current session, and observed ability to receive a turn belong to **Flow**.
   Message asks Flow for that information, chooses a supported transport, and records
   delivery evidence. Message must not create a second independently maintained
   flow-name registry." (The living left the home open — see fork 1.)

6. **Three identities travel in one delivery — caller, source, recipient — and a
   relay never becomes an author.**
   *Source:* order 10A: "1. **Caller:** the flow invoking the CLI now … 2. **Source:**
   the flow/session whose transcript contains the original words … Relaying those words
   does not make cf7879 their author. 3. **Recipient:** the flow to which a route
   attempt is addressed." And: "A temporary peer-file path and content hash must never
   be dressed up as a human transcript turn."

7. **Delivery is proven by receipts of graded strength, and the grades are
   vocabulary**: accepted, transcript-witnessed, parked, file-only, pending.
   *Source:* order 10 in `ordersToCodex-2026-09-16.md`: "the delivery receipt kinds
   (accepted, transcript-witnessed, parked, file-only)". Order 10A on their meaning:
   "A recipient transcript containing the exact datom is the acceptance test … Queue
   acceptance is useful but weaker. `FileOnly` says that a report was written; it does
   not say anyone read it. `Parked` requires a real persisted outbox entry; an
   in-memory intention to send is not parked."

8. **A message carries a priority head, and the top grade may enter a session that is
   already working.**
   *Source:* order 15: "a prioritized message that interrupts a model with a change of
   priority without scaring it: a typed Priority head on the cluster message (Routine,
   Priority, Urgent) with the rule that an Urgent message may be pasted into a busy
   session's next turn and says what to keep running and what to start."

9. **Priority is also what a flow declares when it meets a limit, and when no decision
   can be made at that level the state unwinds upward until one is.**
   *Source:* the living, `f55ec8/vision/quota.md`: "Every codex flow enters into a quota
   check, right? Depending on its priority, if it's a subflow, it has low priority. If
   it's going into low-power mode, it has to say, 'Maybe this would take too long, and
   we don't have enough quota' … then the main flow can take decisions, unlike unwinding
   or sending the state up, final response, seeing how far back up the primary they go
   until a decision is made."

10. **Something that happened and was not propagated becomes a message on its own, and
    that message names who received it.**
    *Source:* the living, `efa157/vision/heartbeat.md`: "use a luna model wake-check that
    decides if something major has happened that wasnt propagated and propagates the
    message to the best likely list of recipients. the message should also say which
    flows received it". Order 9 binds that to the receipt kinds: "the message carries the
    list of flows that received it, with the route and the receipt kind for each
    (accepted, transcript-witnessed, file only)."

11. **The main flow does not interact; it speaks to Nexus CLIs and its transcript is the
    reporting device**, typed responses picked out of it by the opener symbol, the
    variant name and the delimiter, with no logging step.
    *Source:* the living, `efa157/vision/transcriptReporting.md`: "use their transcript as
    their reporting device. They're going to create Datom responses that give them a type
    that is then recovered easily by parsing for that opener symbol, variant name, and
    delimiter … He doesn't have to log." And: "Ideally, we want the main flow to interact
    just with a certain number of Nexus CLIs, whether Meta or whatever."

12. **Past the cluster the same typed message becomes an encrypted chime on the living's
    phone**, from a Prosody on Prometheus named `xmpp.goldragon.criome` inside and
    `xmpp.goldragon.criome.net` outside.
    *Source:* the living, `efa157/vision/domains.md`: "It would be like xmpp.goldragon.criome
    internally. You could do that, but for public access, you put .net."
    `efa157/vision/cloudHosts.md`: "I guess we can use Prometheus for right now to run the
    messaging now, but we're going to want to make it reliable." Order 13 fixes the two
    accounts: `li@xmpp.goldragon.criome.net` and `persona@xmpp.goldragon.criome.net`.

---

## (b) The types

### What the Ethos already proposes

cf7879's order 10A is an explicitly **editable proposal**, not a shipped contract:
"This is an editable design proposal, with the current wire contract identified
separately … The proposed additions and worked text are not claimed to have passed
Ethos generation or the production datom parser."

The complete file, quoted whole (`flows/cf7879/reports/order10-message.ethos`, and
identical inside `to-efa157.md`):

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

The **currently selected** contract — Message main `fe0d0456…`, selecting
signal-message `a9708f3384af18129cb1c983ffed850c4d631e46` in Cargo.lock ("This selected
dependency, not whichever branch a local signal-message checkout happens to show,
governs its current relay contract") — is the smaller subset:

```ethos
ClusterTarget.[Primary Secondary Core]
ClusterMember.{FlowIdentifier SessionIdentifier}
ClusterMembers.Vector<ClusterMember>
Context.{FlowIdentifier SourceTurnIdentifier TranscriptPath PromptSha256 WhatLivingSaid ContextAbout ContextAnswered ContextCorrected ContextUncertainties}
ClusterRelay.{FlowIdentifier SessionIdentifier TranscriptPath PromptFirstSixWords PromptLastSixWords PromptSha256 Context TimestampNanos ClusterTarget ClusterMembers}
ClusterMessage.[Relay.ClusterRelay]
```

**The Peer variant** — `ClusterMessage.[Relay.ClusterRelay Peer.PeerMessage]` — is
published as an additive contract on signal-message branch
`proposal/cf7879-peer-cluster-message` at **`926dcc9447a1b047ef514c98782b9858f55616a4`**,
"with generated PeerEnvelope and codec round trips (worker check receipt; root consumer
integration remains underway)". Order 10A's reason for it: "`ClusterMessage.Peer` is an
additive proposal so peer notes cannot masquerade as human `Relay` records. It does not
change the existing Relay field order."

Caveat carried with the file: "The identifier names currently wrap/alias String in Ethos.
Their names express intent; they do not by themselves prove UUID/hash grammar or process
binding. Those validations must be implemented and tested."

Worked datom examples, quoted from order 10A ("illustrative values, not live receipts"):

```datom
; CallerIdentity, self-declared
{ «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared }

; IdentityProbe and its reply
WhoAmI.{ Known.{ 1234 5678 } Claimed.{ «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared } }
IdentityResolved.{ «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared }

; Peer variant of ClusterMessage
Peer.{ «demo-peer-1» { «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared } { «/example/peer.txt» «ce7edaca…bb94» } «The successor package is ready for review.» }

; DeliveryRequest, caller kept outside the source-bearing message
Deliver.{ { «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared } Peer.{ … } [ «efa157» «d9961c» ] }

; RouteQuery, three selections
Routes.{ { «cf7879» «01a0a715-…» Codex Declared } All }
Routes.{ { «cf7879» «01a0a715-…» Codex Declared } Cluster.Primary }
Routes.{ { «cf7879» «01a0a715-…» Codex Declared } One.«efa157» }

; RouteListing, one FlowNode row of six
{ «efa157» «efa15708-dc5d-42ce-af62-8ffb84c9815e» Claude Primary { Unknown Unavailable 1789574400000000000 1789574400000000000 } [ { ClaudePromptRelay «efa15708-…» } { LaneFile «flows/efa157/log.md» } ] }

; DeliveryReport, one of each receipt kind
DeliveryRecorded.{ «demo-peer-1» [
  { «demo-peer-1» «cf7879» CodexQueue Accepted.{ «demo-transport-ack» 1789574400000000000 } }
  { «demo-peer-1» «efa157» ClaudePromptRelay TranscriptWitnessed.{ «/example/efa157.jsonl» «demo-recipient-record» «ce7edaca…bb94» 42 1789574401000000000 } }
  { «demo-peer-1» «57a7aa» MessageOutbox Parked.{ «demo-outbox-row» 1789574402000000000 } }
  { «demo-peer-1» «e43002» LaneFile FileOnly.{ «/example/core-report.md» 1789574403000000000 } }
  { «demo-peer-1» «348e7b» CodexQueue Pending.{ WitnessPending 1789574404000000000 } }
] }

; Typed refusal
Refused.{ UnknownCaller }
```

### What the vision adds and the Ethos does not yet carry

- **A Priority head.** Order 15: "a typed Priority head on the cluster message
  (Routine, Priority, Urgent)". No `Priority` type exists in the file above.
- **Socket-observed identity as a signal-library element**, not a Message type.
  `callerIdentity.md`: "a standard macro or object … a standard part of this, which
  is a signal. There's this optional part of the signal library to let us add that to
  it." The proposal instead models identity inside signal-message's own vocabulary.
- **A propagation message naming its recipients as a first-class type.**
  `heartbeat.md`: "the message should also say which flows received it." The proposal's
  `DeliveryReport` is a reply to the sender, not a field of the message the recipients see.
- **A quota-check request bearing the caller's priority, and an unwind-upward reply.**
  `f55ec8/vision/quota.md`; the living also placed its seat: "No, that would be in the
  Codex bridge component," which "mirror[s] the interface to the codec [Codex] server
  that we have here (basically the subscription)."
- **A meta socket.** `Vision/nexus.md`: "A Nexus opens at least two sockets … The meta
  socket is privileged — the root user of the Nexus." The proposed Ethos is one Signal
  root with no meta counterpart; per `Vision/nexus.md` "A component has three
  repositories: its main repository … and two signal repositories."
- **A Notify/chime type reaching outside the cluster.** Already exists separately as
  `NotifyEnvelope.[Notify.Notify]` (see (d)); it is not joined to `ClusterMessage`.

---

## (c) The delivery path, step by step

From a flow's typed response to a recipient's user prompt. **E** = exists today,
**P** = partly exists, **N** = does not exist.

1. **N — The flow writes a typed datom response in its own transcript, and the type is
   recovered by parsing for the opener symbol, variant name and delimiter.**
   `transcriptReporting.md` is the living's instruction; no parser or harness tool
   implementing it is reported anywhere in the sources read. Order 17 assigns it; no
   receipt.

2. **P — The flow calls the message CLI with one inline datom.** The pure form —
   one positional datom, no flags (`nexus` skill; `Vision/datom.md`: "a CLI takes its
   whole configuration from its datom input") — does not exist. What ran is:
   `message cluster DATOM --body-file BODY --route-config FLOW_ROUTES --to FLOW@SESSION`
   (order 10 receipts), with flags, a body file and a route-config file beside the datom.

3. **N — The CLI asks Flow who is calling (`WhoAmI.{ Known.{ pid started } Claimed.{…} }`)
   and Flow answers with witnessed evidence.** "Caller attribution remains declared, not
   authenticated." Order 10A: "If Flow cannot witness a stronger binding, it returns
   Declared or refuses. It must not upgrade the evidence merely because the strings agree."
   Scope limitations of order 10B name "no … activated Flow registry".

4. **N — The CLI asks Flow for the routes (`Routes.{ caller All }` → `RoutesListed.{…}`).**
   Order 10B scope limitations: "no global install, activated Flow registry, route-list
   CLI, busy-Nexus parking, or main/deployment move." What substituted: "Route
   configuration is an explicitly observed setup snapshot, not an activated Flow registry."

5. **P — The CLI actualizes the datom into signal and sends it to the Message Nexus's
   ordinary socket.** The sockets exist: "message-daemon.service is active/running at
   installed 0.11.1; sockets /run/user/1001/message/message.sock and message-owner.sock
   exist" — an ordinary and an owner (meta) socket, as `Vision/nexus.md` requires. But
   the gap is explicit: "Current ordinary `message` parses `signal_message::Query`, not
   `ClusterMessage`, which is the concrete CLI gap order 10B must close." The live proof
   used "locally built binaries", and the installed daemon is 0.11.1 while the contract
   is 0.12.

6. **E — Message fans out per route, choosing by the recipient's observed state.**
   "Current fanout invokes ClaudePromptRelay for an explicitly idle configured Claude
   route and NexusFlowDeliver for an explicitly busy configured Nexus route."

7. **N — The busy recipient's message is durably parked in the Nexus outbox
   (`FlowDeliver` → `Parked.{ OutboxEntryId ObservedAt }`) and drained later.**
   "Full reviewed relay lane includes the durable FlowDeliver park support" in Message
   main `fe0d0456`, but: "Proposal 0.12 FlowDeliver compatibility is not established by
   socket existence. No delivery was attempted against it; compatible daemon packaging/
   activation must be explicit before enabling parking." And "Nexus parking uses
   FlowDeliver; parking is not eventual harness delivery." The one live Parked receipt
   shown anywhere is an illustrative example, not a receipt.

8. **E — The Codex leg writes the datom into the recipient Codex session as a user
   record.** Four live witnesses, order 10: identical 3904-byte payload,
   SHA-256 `d041d799b8de4e7bfd8781a92c368b83f34db0748b79bbdb5ba8ed95a7e16c4f`, from a
   1385-byte living source body SHA-256 `3da491b2…70b30`. "The payload starts Relay.{,
   with no JSON recipient header." Recipients cf7879, d9961c, 348e7b, e43002, with record
   ids, timestamps and rollout file line numbers. A separate Peer witness to d9961c:
   record `msg_01a0ab2d-1959-7301-99d4-68d2a0f20c04`, 1996 bytes, SHA-256 `f761ea84…7bfb`.
   Ten queued Codex messages were later pushed "unchanged into the active turn using
   turn/steer, witnessed as native user record msg_01a0ab3f-…" — the closest existing
   thing to the Urgent rule, but done by hand, not by a Priority head.

9. **P — The Claude leg writes the datom into the Claude session through prompt-relay,
   gated on a uniquely witnessed idle.** The gate is real and refused: "Actual Claude
   delivery attempts at 2026-09-16T17:00:18Z both exited 2 with `not uniquely witnessed
   idle`: efa157 and 57a7aa … No idle gate was bypassed." One later delivery did land:
   "The launch note reached efa157 as exact native user record
   82a6b176-9ded-47c5-8125-56232781cc7a at 2026-09-16T17:31:10.618Z, through the Datom
   prompt-relay route." Prompt-relay also recognizes Peer and refuses to re-relay it
   (Primary `19823799…`). Note the Claude leg "invokes the Node peer-file path, bounds
   its subprocess and checks the matching PTY-write receipt; that is not itself a
   recipient transcript receipt."

10. **E — The recipient sees the datom head in its user prompt, no JSON.** Proven for
    the Codex leg by the four witnesses in step 8; proven once for the Claude leg by the
    record in step 9. This is the living's acceptance test, met.

11. **N — The sender receives `DeliveryRecorded.{ source [ receipts ] }` as a typed reply,
    and can ask `DeliveryStatus.«source-event»` later.** No such reply exists; the
    receipts of steps 8–9 were assembled by root into report prose by hand. The order 10A
    caveat on the receipt data is open: "The final contract must specify which byte range
    each hash/count covers. Prefer separate body hash and delivered payload hash if both
    are needed, never switch their meanings silently."

12. **N — A Priority head decides whether the message waits for idle or enters the busy
    turn.** Order 15 is a design item assigned to d9961c, unproposed at the time of these
    reports.

---

## (d) The chime path, from a Notify to the living's phone

1. **P — A producer emits a Notify.** `NotifyEnvelope.[Notify.Notify]` is the current
   contract; "the current CLI accepts `Notify.{ bob@example.org «body» }`", and
   "validation results now serialize contract variants; they are no longer println
   literals." Proof: producer `aec96bf4…`, source `8c3d4aac…`, remote build on Prometheus
   exit 0, drv `/nix/store/z0a2w1hy…-prometheus-notify-proof.drv`. "Packaged CLI emitted
   typed success, malformed/body/input-too-large rejections".

2. **P — The body is encrypted with OMEMO.** "real offline OMEMO roundtrip/tamper case
   passed"; the library fixture is `urn:xmpp:omemo:2`. Offline only.

3. **N — A consumer joins Notify to XMPP and sends the stanza.** Still needed: "A
   consumer joining Notify to XMPP; persistent device/session storage; stanza transport;
   delivery/error receipts; bounded retries."

4. **N — The bot's account sends as `persona@xmpp.goldragon.criome.net`.** Accounts:
   "Registration disabled; no living/bot account provisioned." Order 13 fixes the two
   accounts and the secret path: "Their passwords are minted by the secondary into the
   goldragon sops store under `prosody/li` and `prosody/persona`, never read by an agent;
   the living's password reaches them by the push channel once, then their phone."

5. **P — Prosody on Prometheus routes it.** "Enabled configuration evaluates; PEP/mam/
   carbons/smacks; self-signed setup; client TCP 5222 firewall source". One virtual host,
   public name `xmpp.goldragon.criome.net`, "which is what the phone resolves; the
   internal name `xmpp.goldragon.criome` is a certificate SAN and a DNS alias to the same
   host, not a second virtual host" (order 13). Missing: "Actual guest boot and startup
   test (bounded attempt timed out before VM), then secondary activation and external
   reachability." The VM check exited 124 while still constructing remote closures:
   "only VM test source/evaluation is established; actual activation remains unwitnessed."

6. **N — The device trust that makes the encryption real.** Needed: "PEP device-list/
   bundle publication, device enrollment and trust policy, account/client
   interoperability; online encrypted recipient receipt."

7. **N — DNS and TLS reach the public name.** "Scoped provider proposal exists
   separately"; needed: "Domain/zone selection and scoped credential provision; records
   and TLS issuance integrated into the service, with apply receipts." TLS today is
   "Seven-day renewal threshold, atomic self-signed pair, persistent weekly timer;
   SOPS-owned shared-group 0440 declarations" — self-signed, no runtime renewal witness.
   Order 5 fixes the credential rule: "the token reaching the program through gopass and
   never an agent; develop on the cloud Nexus, then use the cloud Nexus to apply."

8. **N — The living's phone signs in as `li@xmpp.goldragon.criome.net` and chimes.**
   "No installed or paired client receipt." Needed: "Living's client choice/install,
   account sign-in, device verification, encrypted test message and acknowledgement."

Summary blocker, quoted: "No end-to-end connection of account provisioning, bot,
persistent OMEMO/device trust, PEP bundles, stanza transport, Prosody and Notify consumer
exists. The adapter remains a proposal pin."

---

## (e) The open forks the spec must leave visibly open

**1. Where identity lives.** Three homes are on the table and the living did not choose.
- *Message:* "Let's just put it in message right now if we want, or if we have a place
  for identity, let's use it" (`messages.md`).
- *A harness Nexus or the Flow Nexus:* "we could have a harness nexus that keeps track of
  what Flow ID is in the harness, or maybe he gets that from the Flow Nexus. Whoever has
  that data already can provide it, and we just operate on full trust right now"
  (`transcriptReporting.md`).
- *Flow, per cf7879:* "Its stable identity, current session, and observed ability to
  receive a turn belong to **Flow** … **Proposed one owner:** extend that Flow-owned
  source into a typed query service."
- A fourth cut crosses all three: `callerIdentity.md` puts the *carrying* of identity in
  the **signal library** as an optional standard part, independent of which Nexus *answers*
  for it. Also open: which component identifies the caller — "do we have a way to identify
  which flow calls the CLI? That could be with the flow component or the orchestrate
  component, whatever maybe has that function already" (`messages.md`). And the evidence
  ladder is unbuilt: `IdentityEvidence.[Declared ProcessSessionObserved RegistryBound]`,
  with "A PID alone is insufficient because it can be reused. An alias is a name, not an
  authentication token."

**2. The Urgent-message rule for a busy session.** Order 15 states the intent — "an Urgent
message may be pasted into a busy session's next turn and says what to keep running and
what to start" — and assigns it to d9961c as a *design item*, unproposed. It stands directly
against the live behavior: the idle gate refused both Claude routes with `not uniquely
witnessed idle`, and `PendingReason.[Busy ApprovalWait …]` exists precisely to say no. Also
unresolved: order 10A's "Approval-wait never becomes idle by timeout" versus interrupting a
working session. The living's framing — "interrupts a model with a change of priority
without scaring it" — is a requirement on the *wording* of an Urgent message, not just its
routing, and nothing has been written for it.

**3. The public door for XMPP.** Three doors are described, none chosen.
- *Internal only, through our own DNS:* "Our own domain name servers that are configured
  locally are going to route us internally with our messenger and everything else … even
  through a foreign router as an intermediary" (`f55ec8/vision/networking.md`), over the
  mesh protocol on the house's foreign router.
- *A Cloudflare tunnel:* "he can have a feature that uses the Cloudflare tunnel for hosting
  your own services on Prometheus and turns on that feature … then the cloud component tries
  to make sure that the records at Cloudflare are routing for this tunneled server"
  (`f55ec8/vision/cloud.md`).
- *A port-forward:* implied by Prosody's open client TCP 5222, against the reachability
  witness that found "prometheus behind a foreign router 192.168.1.1 with the site's single
  public IPv4 and no IPv6" (`networking.md` context) — a router not configured for us.
- Underneath: is Prometheus the permanent seat at all? "I guess we can use Prometheus for
  right now to run the messaging now, but we're going to want to make it reliable. That gets
  you a token that you can use to spin up servers easily" (`cloudHosts.md`).

**4. Federation policy.** The shape is named, the policy is not written.
"There's a federation of different domains that are controlled by these clusters.
Essentially, we're going to get DNS from each other, right? … I would probably firewall all
of the web by default, except for some XMPP domains, and it would be per cluster"
(`domains.md`). Open: which domains a cluster admits, how a fork's domain enters the
federation, and — flagged by cf7879 — "A transport-port rule alone is not a domain allowlist;
keep the protocol/domain policy and network enforcement distinction explicit during
implementation." Order 4 records the abstraction requirement: "The domain part of the
configuration is abstracted so a fork brings its own."

**5. Whether MCP exists at all.** "Do we even want an MCP? Does it give us some capabilities
that are difficult or more costly to do through the shell or through whatever tool these
harnesses have? … If we make a simple MCP, maybe we save all the MCP calls through our own
bridge. Anything that we were using MCP for before, we just put it in our own language, and
then we make the MCP stack smaller" (`efa157/vision/mcp.md`). The only shape proposed:
"If selected, the proposed sole MCP surface is one bridge tool accepting a single datom
string. This does not adopt or install MCP, and does not settle the earlier component-enum
proposal, dispatch contract, validation, or result type. Preserve these as design decisions
for the living." Note the live agent intercom today *is* an MCP surface with JSON tools —
the fork is live, not hypothetical.

### Two further forks the sources leave open, worth naming

**6. Contract evolution.** "Adding variants or fields is not automatically archive or wire
compatible. Each adoption needs a contract version and typed upgrade operation,
generated-code check, parser fixtures and old-record/migration tests where stored data
changes." The concrete blocker: "The Message 0.11.1 (schema 3) to 0.12 (schema 5) migration
with the pending outbox row restored is primary work and blocks relay activation" (order 13).

**7. Where quota priority is accounted, and where the message enters it.** The living placed
the accounting — "No, that would be in the Codex bridge component" — but the Priority head of
order 15 rides the *cluster message*, and the unwind of `quota.md` runs up the flow tree.
Whether these are one type or two is unstated.

---

## Provenance of this brief

Read-only. No commit, no send, no edit outside `flows/f55ec8/reports/`. Branch tips read
through the scratch clone `/tmp/f55ec8-delta/p` at `origin/flow/efa157`, `origin/flow/cf7879`,
`origin/flow/d9961c`, `origin/main` as fetched 2026-09-16. Every quotation above is verbatim
from those trees or from the f55ec8 worktree's own `flows/f55ec8/vision/` files. Nothing here
claims a build, a deployment or a delivery of its own.
