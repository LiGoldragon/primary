<!-- to-the-living:start -->
Presentation.{ «Switching the flows to the new Flow» }

# Switching the flows to the new Flow

## mind-context › knowledge/flow-seats.md

Observed on 2026-10-17 at 12:55 -06:00, against the running Flow Nexus
0.35.11 (Flow `67b80b3`, store
`/home/li/.local/state/flow-production/flow.sema`), messenger-clj 0.4.0
and the Herdr session `default`. A flow's route can change with any
start, bind or retirement; observe again before relying on it.

## How a message picks its route

The target decides the route. `hm-send` asks Flow for the target's
metaflow; an address Flow does not know is typed into its pane by
Herdr, as before Flow. An address Flow knows goes to Message, which
names the sender through Flow and refuses a sender that is no flow.

```
          +------------------------+
          | hm-send to a target    |
          +-----------+------------+
                      |
                      | asks Flow for
                      v
          +------------------------+
          | the target's metaflow  |
          +-----+------------+-----+
                |            |
     not known  |            | known
                v            v
+----------------+    +------------------+
| typed into the |    | Message asks     |
| target's pane  |    | Flow who sent it |
| by Herdr       |    +----+--------+----+
+----------------+         |        |
                    a flow |        | no flow
                           v        v
               +------------+  +------------+
               | queued for |  | refused    |
               | the target |  |            |
               +------------+  +------------+
```

The deployed messenger-clj 0.4.0, `messenger_clj/public.clj` and
`messenger_clj/flow_bridge.clj`:

```clojure
(defn routed-delivery! [target request options legacy]
  (name! target)
  (runtime/validate-request! request)
  (if (bridge/managed? target)
    (bridge/send! target request options)
    (delivery! target legacy)))
```

```clojure
(defn managed? [target]
  (let [query (str "Current." (address! target))
        result (try (*call* "flow" query)
                    (catch Exception _ (runtime/fail "FlowRegistryUnavailable: no legacy fallback")))
        answer (str/trim (or (:out result) ""))]
    (when-not (zero? (or (:exit result) -1))
      (runtime/fail "FlowRegistryUnavailable: no legacy fallback"))
    (cond
      (= answer "Current.Unknown") false
      (contains? #{"Current.Asleep" "Current.Ended"} answer) true
      (re-matches #"Current\.Awake\.(?:[A-Za-z0-9_-]+|«[^«»\\\n]+»)" answer) true
      :else (runtime/fail "FlowRegistryRefused: unexpected or refused Current response; no legacy fallback"))))
```

## What Flow holds

Flow's whole state is its metaflows. Their type, `Metaflow`, is in
Flow's `crates/flow-ethos/ethos/library.ethos`, quoted whole at Flow
`67b80b3`:

```ethos
; Flow's shared types live in this leaf package. Signal and Meta-Signal
; import them here and re-export their original Rust paths. Aspect is one
; nominal type shared by addresses, launch profiles and meta configuration.

Library
[]
[ FlowId.String
  ; ethos-zero 16 cannot express Topic:Name yet; check camelCase at input.
  Topic.String
  ; The design type is Blake3.Bytes<32>; 16.0 uses a 64-hex-character string.
  Blake3.String
  Layer.[ Primary Secondary Tertiary Quaternary ]
  Subaspect.[ Vision Intent Knowledge Operation Trial Compensation ]
  ; Define the component types once. Source refers to these declarations;
  ; inlining Path.String inside Source would redeclare Path globally.
  Repository.String
  Hash.Blake3
  Path.String
  Reason.String
  Source.{ Repository Hash Path }
  Key.{ Subaspect Topic }
  Said.{ Context.String Verbatim.String }
  Request.[ Order.String
            Question.String
            Psyche.Said
            Psyches.Vector<Said>
            Result.String
            Notice.String ]
  Aspect.[ Psyche Mind Field ]
  Address.{ Aspect Topic Layer }
  Recipient.[ Address Up ]
  ; Who a queued request is from: the Address Flow resolved for its sender
  ; (the Lock's Sender of a Deliver, the thread's metaflow of a send-tool
  ; call), or Unknown for a request queued before Flow kept senders.
  SentBy.[ Sender Unknown ]
  QueuedRequest.{ SentBy Request }
  Metaflow.{ Address
             State.[ Awake.FlowId Asleep Ended ]
             Past.Vector<FlowId>
             Queue.Vector<QueuedRequest> }
  Lock.{ Sender Address Until.Integer }
  Process.{ Pid.Integer Started.Integer }
  Sender.Address
  OrdinarySocketPath.String
  MetaSocketPath.String
  StorePath.String
  Start.{ OrdinarySocketPath MetaSocketPath StorePath }
  ; Startup refusal is distinct from the ordinary/meta socket Refusal.Store.String.
  StoreRefusal.{ Path Reason }
  StartRefusal.[ Store.StoreRefusal ]
  SourceRoot.String
  ClientPath.String
  Home.String
  ControlSocketPath.String
  ModelName.String
  CodexEndpoint.{ ClientPath Home ControlSocketPath Vector<ModelName> }
  StableCodex.CodexEndpoint
  NextCodex.CodexEndpoint
  HarnessKind.[ Codex Claude ]
  KeyName.String
  CommandSigil.String
  InterruptKeys.Vector<KeyName>
  SubmitKeys.Vector<KeyName>
  HarnessProfile.{ HarnessKind Vector<CommandSigil> InterruptKeys SubmitKeys }
  HarnessProfiles.Vector<HarnessProfile>
  MetaAspects.Vector<Aspect>
  MessageNexusPath.String
  MessageNexusBinary.String
  Nexus.{ SourceRoot
          StableCodex
          NextCodex
          HarnessProfiles
          MetaAspects
          MessageNexusPath
          MessageNexusBinary
          Lease.Integer } ] ; Lease seconds; 60 before any Nexus payload.
[]
[]
```

```sh
flow 'Metaflows'
# -> Listed.[ … { { Psyche flow Secondary }
#      Awake.17c364 [] [ … ] } … ]
flow 'Current.{ Psyche core Primary }'
# -> Current.Unknown
herdr pane list
```

At the observation, Flow held four Psyche and Field flows that have a
live pane:

| Flow | Address | Harness | How it came under Flow | State |
|---|---|---|---|---|
| d68c82 | Psyche core Secondary | Claude, Opus | adopted: binding imported, then bound from its own process | Awake |
| 17c364 | Psyche flow Secondary | Codex, Astra | started by Flow | Awake |
| 804eb9 | Psyche ethos Secondary | Claude, Opus | started by Flow | Asleep, no pane |
| 75f438 | Field startup-codex-0355 Quaternary | Codex | started by Flow, a Field proof | Awake |

The store also holds rows with no pane: `{ Field message Primary }`
Awake as `flow-0000000000000013`, and five asleep Field proof
metaflows.

Twenty-two live harness panes run on the old route: Flow answers
`Current.Unknown` for their addresses. Their titles at the observation:
Field 42265e and 44cda5; Mind 41fa34, 0c85a3, 0430eb, 47d946, 5b9075,
e4b7d7, 9896d8; Field PrimaryCommitting 89fbc1; Psyche core Primary
39bd0c, core Tertiary 4201a3, Spirit d55c56 and ee57fb, Nexus 058f16,
nexus a275c0, Communication 3960eb, chronos 984e88 and 504f11,
InstructionWitness 19d9f2, and da2038 and 65f93a, which messenger-clj
records as retired while their panes stay open.

`hm-list` printed `MetaflowMetadataRequired: registration lacks aspect,
topic or layer` and listed nothing, so the old route's own registry was
not read.

## field-context › compensation/messenger-clj.md

The `hm-*` shorthands are provided by the standalone messenger-clj repository under `Repository root`, on its default branch. Use `hm-send` for flow-to-flow messages, never a shell script, paste, or another intercom.

`FLOW_ID=<self> hm-send TARGET BODY` sends one complete machine body as `#msg [sender machine-prose]`. Use `--stdin` in place of `BODY` for a large or multiline body. `FLOW_ID=<self> hm-send TARGET --psyche CONTEXT VERBATIM` sends the living's words, context first, as one `#psyche [sender context whole-verbatim]`; `--psyche CONTEXT --stdin` reads the verbatim from standard input. `FLOW_ID=<self> hm-send TARGET --psyches --stdin` reads one EDN vector of `[context verbatim]` pairs and sends them as one `#psyches` envelope. Pass message fields, never a prebuilt envelope. `hm-send-abrupt` takes the same arguments and interrupts the target's active turn first. Flows refer to one another by the registered, space-separated meta-flow identifier, such as `Psyche Core Secondary`. Quote it as one TARGET argument. Internal flow IDs remain accepted transport and audit keys. The origin of every live `#msg`, `#psyche` and `#psyches` is the sender registration's aspect, topic and layer with spaces, never dots, a model, a guessed title or a truncated native UUID. Missing sender registration or any required metadata refuses the send; missing or ambiguous named TARGET refuses it.

The living's words travel only as psyche, never quoted, paraphrased or summarized inside a `#msg` body. A message that rests on his words sends two messages: the psyche, then the flow's own `#msg`. Write the recipient-facing body only.

Work goes straight to the flow that acts on it next. A flow that finishes a package hands it directly to the flow that turns it into the deliverable, such as a Tertiary book subflow that publishes it. The ordering flow hears only about a blocker, a needed ruling, or a finished deliverable it must itself act on.

Before sending, establish that the recipient holds the work and is live. A Codex delivery is relied on once hm-send prints Presented; nothing more is sought from the recipient.

The typed reply is what hm-send itself prints; a flow never waits on or watches the target for an answer. What hm-send prints stays with the sender: it is acted on and logged, never forwarded. `Transported` is Herdr's acceptance for the checked binding. `Presented` includes the observed reaction of the target. `Held` means nothing was typed and the whole body is pending until an explicit supported delivery action; its printed reason names the refusal. `RepairRequired` means the recorded candidates must be judged and the route repaired with `hm-repair`. `Uncertain` means the envelope may have arrived: inspect the target and never retry blindly. A refused or undelivered send is reported to the sending flow and its route is mended.

Registration validates one exact live Herdr identity and stores its native binding immediately; send readiness is checked separately. Supply qualified `--aspect ASPECT --topic TOPIC --layer LAYER` together through normal `hm-register`; do not infer them from the harness or model. Re-registration without these flags preserves existing metadata. After a route is removed, registration must supply its qualified metadata again. Historical ID-bearing envelopes remain readable evidence, not an origin fallback for new sends.

`FLOW_ID=<self> hm-retire FLOW` takes only the flow id: it reads the route and live Herdr identity itself, writes the evidence file, and prints its path. A refusal prints `RetireRefused.{ FLOW Reason }` and changes nothing.

A message carries something the recipient must act on or a blocker; a flow never asks for, or sends, a receipt, a commit id or an acknowledgement on its own.

## field-context › compensation/launch.md

Launch a subflow through the harness's own flow mechanism. Do not
nested-launch another harness to reach a model. A Primary starts only
after a live Secondary for the same aspect and topic is verified; when
none exists, the launcher starts that Secondary first and verifies its
native binding before starting the Primary.

A flow that hands work to a Primary, or to any flow above it, first gathers through its own subflows everything that work needs: the living's words whole, his comments on the books, the records and the files. It sends all of it in one message. It never sends a pointer or an instruction to go and fetch.

A book the living asks for goes to a flow that can start it now; no launch, refresh or regeneration holds it.

Herdr is third-party software that we never modify.

Before reporting a launch as ready, verify its named Herdr session,
colour, title, remote control, and its remote listing. Every spirit-*
module and every intent-* module selected at launch goes in the flow
system prompt, never the startup user prompt. Each subagent carries
every spirit-* body in its own instruction layer.

A flow at or above its layer's configured refresh threshold receives no
further work. A Fable flow receives no further work at 15% of its observed context window, or 100,000 observed tokens. Its secretary orders its successor started at once; the successor takes its topics from the handover. Read that threshold from the layer configuration. When
the configuration or a supported context observation is unavailable,
report that absence rather than inventing a value. Retire a predecessor only after its fresh successor has
answered on a supported route and its native role and binding have
been verified; then never reuse or message it.

Launch with the required permission mode. A permission prompt reaching
the living is a launch failure. Escalate laterally at the same layer,
then one layer up.

A lower layer that is unsure asks the layer above and admits what it
does not know.

Psyche core Secondary is the hub: it decides what reaches a topic flow, and only matters of that topic do. Messages pass between Secondaries; a topic Secondary publishes its Primary's books. A flow that receives noise tells the sender it is noise and why; the sender finds why it misjudged, and that finding is proposed as a skill change.

A flow messages only whom its aspect, layer and topic allow, and refuses the rest.

A launched flow's startup task is never to reply READY. Its first response is a presentation of its context: subflows first reinforce that context, then the flow proposes how to make things better in its role, as named by the skills for its aspect, layer and topic. Psyche crystallizes its context into vision, intent and spirit; Mind for knowledge, questions and implementation; Field for its own roles.

## Proposal 1: psyche-context › vision/flow.md

+ Every flow runs under Flow.
+ A flow that Flow did not start is replaced by a fresh flow that Flow starts, and the old one is retired.
- Flow deploys first and is used raw to send messages, until Message sends through Flow's socket.

Ruling:

a. As shown.

b. The first added line only; live flows are adopted where they stand.

c. Neither.

## mind-context › knowledge/flow-caller.md

Read on 2026-10-17 in Flow `67b80b3` (0.35.11, installed and running)
and its pinned signal-flow `6a49664`.

## How a caller is named

Flow names a caller from the process on the other end of its socket.
It walks up that process's ancestors to the Herdr pane it runs in, and
asks its own store which flow is bound in that pane. Exactly one live
bound flow is the caller; none, or more than one, is no flow. A flow
never states its own id.

```
+--------------------------+
| the calling process      |
+------------+-------------+
             |
             | runs, through its ancestors, in
             v
+--------------------------+
| a Herdr pane             |
+------------+-------------+
             |
             | is looked up in
             v
+--------------------------+
| Flow's store of bound    |
| flows                    |
+------+-------------+-----+
       |             |
  one  |             | none, or
  flow |             | more than one
       v             v
+-------------+ +-------------+
| that flow,  | | no flow:    |
| its id and  | | Unbound, or |
| session     | | CallerUnknown|
+-------------+ +-------------+
```

`crates/flow-nexus/src/caller.rs`:

```rust
impl BindsCallerPane for RunningNexus {
    fn bound_caller(&self, pane: &CallerPane) -> Result<Caller, CallerResolutionRejection> {
        let unknown = |_: StoreError| CallerResolutionRejection::CallerUnknown;
        let mut present = self
            .store
            .flows_in_pane(&pane.herdr_session_name, &pane.herdr_pane_id)
            .map_err(unknown)?
            .into_iter()
            .filter(|node: &FlowNode| self.herdr.pane_presence(node) == PanePresence::Present);
        // No binding, or more than one, names no caller.
        let (Some(node), None) = (present.next(), present.next()) else {
            return Err(CallerResolutionRejection::CallerUnknown);
        };
        self.store
            .role(&node.flow_id)
            .map_err(unknown)?
            .ok_or(CallerResolutionRejection::CallerUnknown)
    }
}
```

What a launch or a message records as its origin is one of two
variants, `Origin`, and the `Caller` and its refusal are in signal-flow
`ethos/signal.ethos`, quoted whole at `6a49664`:

```ethos
; Presentation names the living-directed output's book; it carries no body
; or sender. Transcript content ownership is deliberately not declared.
;
; QueueTurnEnd is a pre-end wakeup, not evidence that the turn completed.
; Stop may precede the final native record or repeat while a turn continues.
; TurnEndQueued acknowledges durable enqueue only and must return without
; waiting for the final transcript record. The Nexus verifies completion and
; deduplicates actual native (SessionId, TurnId) before any downstream work.
; A missing transcript path is None, never an invented empty path.
; No handler, hook or state subscription is implemented by this vocabulary.
;
; Flow ordinary Signal.
;
; Start and Replace carry a LaunchProfile; a Replace's profile names the
; replaced flow as its predecessor. Neither carries its origin: the Nexus
; derives it from the calling process as Identify does (its pane's bound
; flow and that flow's native session), and a caller that is no bound flow,
; such as a deploy script, is an Unbound origin, recorded, never refused.
; A launch's power is its Address layer's and its harness is the one whose
; configured endpoint serves its model (Codex), else Claude; neither is
; named in the profile. The successor is launched; once it has
; Started, the predecessor is Stopped and taken out of receiving, and
; only then is the successor routable. Reaping belongs to the refresh
; event: no state holds both flows routable. Replaced carries the
; stopped predecessor's FlowId and the successor's Started.
; ReplaceRejection names why no replacement took place; after
; ReapRefused the successor is not routable.
;
; LaunchStatus answers a known LaunchRequestId with one LaunchInspected
; snapshot: its LaunchAttempt, its optional settled outcome, and the
; FlowNode actually recorded for the launched flow, if one exists. A
; pending attempt has no outcome. A replacement's FlowNode is its
; successor, never the predecessor named in LaunchProfile. An unknown
; request has neither attempt nor outcome; an outcome without an attempt
; is InconsistentRecords. If the rows change while read, the answer is
; ReadViewChanged. The snapshot is marker-consistent, not a transaction.
;
; Observe.Launch opens an exchange that goes on answering: on open it
; sends what LaunchStatus would, then one LaunchInspected frame for
; every later phase change, and it ends after the inspection carrying
; the outcome. Nothing is re-read on a timer; a launch that does not
; move sends nothing. Every other query is answered with exactly one
; frame.
;
; Nothing on this socket writes into a pane. Flow is the only pane writer,
; and it writes only through the privileged Deliver and Command of the
; meta contract, under its own per-pane lease.
;
; Observe.Agent opens an exchange that goes on answering: on open it
; sends the flow's agent state as Herdr shows it now, then one
; AgentObserved frame for every later change Herdr announces, and it
; ends after the frame carrying Gone, when the flow's bound pane has left
; Herdr or the flow is no longer live. Nothing is re-read on a timer. A
; flow Flow does not hold answers one Gone frame. Unknown is Herdr's own
; word for an agent it cannot read.
;
; A Pending flow becomes Active when it is witnessed live: on a
; Presented Deliver, or when List finds its bound pane present in Herdr.
; Nothing else promotes it.
;
; A flow's lifecycle is what List reports of it. Pending and Active are
; live: a bound native seat answers. Pending is a seat not yet witnessed
; live; Active is one that has been.
;
; The three ways a flow stops being live are distinct, and each names
; who ended it. Stopped is Flow's own act: Stop, or a replacement's
; reap, closed a pane Flow was holding. Exited is the seat's own act or
; its accident: its pane is gone from Herdr and Flow never closed it, so
; nothing can be sent to it. Retired is an owner's act: the flow is
; taken out of Flow's receiving deliberately, through the privileged
; Retire, whatever its pane is doing. A pane going away never makes a
; flow Retired — an exit retains the flow's record and says only that it
; Exited; retirement comes from authority, never from an observation.
;
; None of the three is a deletion: every one of them keeps the flow's
; row, its origin and its history, and none is ever reported with an
; Available route. Only Pending and Active ever are.
;
; ResolveCaller names the flow bound to the process that called: the
; Nexus reads the caller from its own socket, never from the payload.
; The optional FlowId is the caller's claim, checked against the
; binding: CallerMismatch carries the Caller the binding names.
;
; Bind binds the calling process to an Address. A Bind for { Field message
; Primary } is accepted only when the kernel-reported executable is the
; configured MessageNexusBinary; an unconfigured Nexus answers
; NotConfigured and another executable answers NotMessage. The Process in
; the request is not proof of the caller's executable.
;
; Lock, Deliver and Release are accepted only from the exact bound Message
; process (PID and start time). Message's Identify result supplies the
; distinct Sender Address in Lock; Flow trusts that bound Message peer's
; assertion and does not independently resolve the Sender's origin. A
; Sender must name an existing Awake metaflow. The request is queued with
; that Sender (QueuedRequest.{ SentBy Request }), and a woken or drained
; flow reads each queued request with who sent it; a request queued before
; senders were kept reads SentBy Unknown. Unknown addresses are not
; created; an Asleep Sender is refused as Asleep and an Ended Sender as
; Ended.Address.
;
; Report carries one harness event of a flow Flow holds, sent by the
; harness's hook through the Flow CLI with the FlowId the flow was
; launched with. Flow stores the event in that flow's Memory and answers
; Reported. A FlowId Flow does not hold is refused, Refused.Unknown.FlowId,
; never adopted: a flow Flow did not launch is a flow Flow does not know.
;
; A LaunchProfile names the Address of the seat it launches. When the
; launch is confirmed, the Nexus records that Address's metaflow Awake as
; the launched flow, under the rules Bind applies: a metaflow Awake as a
; live flow is refused (AddressAwake), an Ended one is refused
; (AddressEnded), and an Asleep one, or one Awake as a flow no longer live,
; is taken over, a displaced flow joining Past. A replacement takes over
; the metaflow of the predecessor its profile names. A Start whose Address
; would be refused is refused before anything launches.
;
; Launched is what Start answers, carried by the Started reply; it was
; named Started until 9.0.0, when Event's Started took that name. It names
; the flow, its native session and the Herdr route it runs in (Available
; while its pane is held, Unavailable once it is gone), so the caller can
; register the seat with its messenger.
;
; A LaunchProfile names its seat's context only by module identity:
; SystemModules for the system prompt and UserModules for the first USER
; message. Flow has the context composer resolve those identities in the
; context repositories and verifies the answer; no path and no context
; text travels in a Start. The only text a Start carries is the seat's
; first brief, InstructionPrompt.
;
; The first USER message is the composed modules followed by the brief,
; sent once. When it does not fit one message it is split on module
; boundaries into PromptParts, each naming itself part k of n; the brief is
; in the last. A part after the first is sent only after the seat finished
; its answer to the one before. The durable PromptDeliveryIntent holds
; every part's SHA-256 in order, how many parts were submitted, and the
; count of Stop reports seen when the last one was. The receipt is every
; part observed in order as a user turn, then the seat's first answer at
; the intended model and effort.

Signal
[
  flow_ethos:[ Aspect Address FlowId Request SentBy QueuedRequest Lock Sender Process Metaflow Key Recipient Layer Topic Subaspect OrdinarySocketPath MetaSocketPath Start ModelName HarnessKind ] ]
[ Start.LaunchProfile
  Restart.FlowId
  ResolveRecipient.RecipientResolutionRequest
  Stop.FlowId
  Replace.LaunchProfile
  LaunchStatus.LaunchRequestId
  Observe.ObserveSelection
  ResolveCaller.Option<FlowId>
  QueueTurnEnd.TurnEndRequest
  Report.{ FlowId Event }
  Lock.{ Sender Recipient }
  Bind.{ Address Process }
  Identify.Process
  Deliver.{ Lock Request }
  Release.Lock
  End.Address
  Current.Address
  Metaflows ]
[ Started.Launched
  LaunchPending.LaunchAttempt
  StartAmbiguous.PromptDeliveryIntent
  Restarted.Restarted
  RecipientResolved.FlowNode
  Stopped.FlowId
  Listed.Vector<Metaflow>
  StartRejected.StartRejection
  RestartRejected.RestartRejection
  RecipientResolutionRejected.RecipientResolutionRejection
  StopRejected.StopRejection
  Replaced.Replaced
  ReplaceRejected.ReplaceRejection
  LaunchInspected.LaunchInspection
  LaunchStatusRejected.LaunchStatusRejection
  CallerResolved.Caller
  CallerResolutionRejected.CallerResolutionRejection
  AgentObserved.AgentObservation
  TurnEndQueued.TurnEndRequest
  TurnEndRejected.TurnEndRejection
  Reported
  Locked.Lock
  Bound.FlowId
  Identified.Address
  Delivered
  Queued
  Woken.FlowId
  Released
  Ended
  Current.[ Awake.FlowId Asleep Ended Unknown ]
  Refused.Refusal ]
[
  SessionId.String
  TurnId.String
  FlowType.String
  Generation.Integer
  EndpointPath.String
  HerdrSessionName.String
  HerdrAgentName.String
  HerdrWorkspaceId.String
  HerdrPaneId.String
  HerdrTerminalId.String
  LaunchRequestId.String
  ModuleIdentity.String
  SystemModules.Vector<ModuleIdentity>
  UserModules.Vector<ModuleIdentity>
  Effort.String
  RememberingDepth.Integer
  SystemPromptText.String
  SystemPromptSha256.String
  InstructionPrompt.String
  FirstPromptBody.String
  PromptPartText.String
  PromptSha256.String
  NativeSessionId.String
  NativeTurnId.String
  ReceiptSha256.String
  TranscriptDevice.String
  TranscriptInode.String
  TranscriptByteOffset.Integer
  TranscriptPrefixSha256.String
  TranscriptRootDevice.String
  TranscriptRootInode.String
  PartsSubmitted.Integer
  StopsReported.Integer
  PowerLevel.[ High Medium Low UltraLow ]
  RememberedFlow.{ FlowId RememberingDepth }
  ; A leave-out names one part of a harness's start that a flow goes
  ; without: a tool or tool group, an instruction block, or a harness
  ; feature. Each turns into the harness's own flag, environment variable
  ; or setting. ToolSearch and BashTool are named so that leaving them out
  ; is refused: without ToolSearch every deferred tool's schema loads, and
  ; without Bash the flow cannot message, commit or build. SkillTool and
  ; BundledSkills are refused unless WorkflowTool is left out too, since
  ; Workflow then inlines its authoring reference. A Claude leave-out is
  ; refused for a Codex start, and a Codex one for a Claude start.
  LeaveOut.[ ClaudeAiConnectors ConfiguredMcpServers AgentTool ExplorePlanAgents FileTools WorkflowTool ScheduleWakeupTool ReportFindingsTool ListAgentsTool CronTools WebTools DeferredTools SkillTool BundledSkills ClaudeMd GitInstructions AttributionReminder UserSettings ToolSearch BashTool CodexSkillListing CodexAgentsMd CodexCollaborationMode CodexEnvironmentContext CodexPermissions CodexDeveloperInstructions ]
  LeaveOuts.Vector<LeaveOut>
  ; A Start's leave-outs, when it names them, replace the default its
  ; metaflow's configuration names; None takes that default.
  LaunchProfile.{ LaunchRequestId SystemModules UserModules Address ModelName Effort Option<FlowId> Vector<RememberedFlow> HerdrSessionName Option<LeaveOuts> InstructionPrompt }
  TargetReceiptRequest.{ LaunchRequestId PromptSha256 }
  PromptPart.{ PromptPartText PromptSha256 }
  FirstPromptPayload.{ FirstPromptBody PromptSha256 Vector<PromptPart> }
  SystemPrompt.{ SystemPromptText SystemPromptSha256 }
  ; The harness the Nexus derived for the launch's model, and the effective
  ; leave-outs: the Start's, else its metaflow's default.
  ComposedLaunch.{ LaunchProfile HarnessKind SystemPrompt FirstPromptPayload TargetReceiptRequest LeaveOuts }
  HerdrPaneBinding.{ LaunchRequestId HerdrSessionName HerdrAgentName HerdrWorkspaceId HerdrPaneId HerdrTerminalId }
  NativeLaunchIntent.{ LaunchRequestId PromptSha256 SystemPromptSha256 HarnessKind ModelName Effort Vector<PromptSha256> }
  NativeLaunchBinding.{ LaunchRequestId FlowId NativeSessionId HarnessKind HerdrPaneBinding }
  RegistrationAcknowledgement.{ LaunchRequestId FlowId NativeSessionId HerdrPaneBinding }
  NativeTranscriptCursor.{ NativeSessionId HarnessKind TranscriptDevice TranscriptInode TranscriptByteOffset TranscriptPrefixSha256 }
  NativeTranscriptAbsence.{ NativeSessionId HarnessKind TranscriptRootDevice TranscriptRootInode }
  NativeTranscriptBoundary.[ Existing.NativeTranscriptCursor
                             Absent.NativeTranscriptAbsence ]
  PromptDeliveryIntent.{ LaunchRequestId PromptSha256 FlowId NativeSessionId HarnessKind ModelName Effort Vector<PromptSha256> PartsSubmitted StopsReported LeaveOuts HerdrPaneBinding NativeTranscriptBoundary }
  NativeTargetReceipt.{ LaunchRequestId PromptSha256 FlowId NativeSessionId NativeTurnId ReceiptSha256 ModelName Effort Vector<PromptSha256> }
  PromptDeliveryResult.[ Observed.NativeTargetReceipt
                         Ambiguous.PromptDeliveryIntent ]
  LaunchAttemptPhase.[ Reserved NativeLaunchIntentRecorded NativeBound RegistrationAcknowledged PromptIntentRecorded PromptObserved PromptAmbiguous ]
  LaunchAttempt.{ LaunchRequestId LaunchProfile PromptSha256 Origin LaunchAttemptPhase Option<NativeLaunchIntent> Option<NativeLaunchBinding> Option<RegistrationAcknowledgement> Option<PromptDeliveryIntent> Option<PromptDeliveryResult> }
  LaunchStatusOutcome.[ Started.Launched Replaced.Replaced StartRejected.StartRejection ReplaceRejected.ReplaceRejection ]
  LaunchInspection.{ LaunchAttempt Option<LaunchStatusOutcome> Option<FlowNode> }
  LaunchAttemptReservation.[ Reserved.LaunchAttempt
                             Existing.LaunchAttempt
                             Conflict ]
  ; Where a launch or a flow came from: the bound flow that asked, with its
  ; native session, or Unbound for a caller that is no bound flow.
  FlowOrigin.{ FlowId SessionId }
  Origin.[ Flow.FlowOrigin Unbound ]
  RecipientResolutionRequest.FlowId
  StopRequest.FlowId
  RouteReadiness.[ Ready Parked ]
  EndpointSelection.[ Available.{ EndpointPath RouteReadiness }
                      Unavailable ]
  HerdrRoute.{ HerdrSessionName HerdrAgentName HerdrPaneId HerdrTerminalId }
  HerdrRouteSelection.[ Available.HerdrRoute
                        Unavailable ]
  FlowLifecycle.[ Pending Active Stopped Retired Exited ]
  FlowNode.{ FlowId SessionId HarnessKind EndpointSelection HerdrRouteSelection Origin FlowLifecycle }
  Launched.{ FlowId SessionId HerdrRouteSelection Origin }
  Restarted.{ FlowId SessionId Generation }
  ; BindingRefusal names one checked native-binding failure without raw adapter text.
  ; PaneMismatch covers the agent name, workspace, or pane check.
  ; TerminalMismatch covers the terminal check.
  ; HarnessMismatch covers the reported harness and official session source check.
  ; NotReady covers interactive readiness.
  ; ReservedIdentityMismatch covers selected, observed, or claimed identity conflicts.
  ; ClaimUnavailable covers Flow identity claim and claim readback failures.
  ; ObservationRefused covers a missing or malformed agent/session observation.
  ; TransportRefused covers the Herdr request or response transport boundary.
  ; Unclassified marks a stored v10 unit refusal whose stage was not kept.
  BindingRefusal.[ PaneMismatch TerminalMismatch HarnessMismatch NotReady ReservedIdentityMismatch ClaimUnavailable ObservationRefused TransportRefused Unclassified ]
  ; ContextRefusal names why a seat's context was not composed for its
  ; Start: the composer could not be reached or rejected the request; its
  ; answer named another metaflow; a payload's text differs from its
  ; SHA-256; a requested module is missing from the composed provenance;
  ; the system text exceeds one argument; or one module with its part
  ; header does not fit one message.
  ; LeaveOutRefusal names why a Start's effective leave-outs were refused:
  ; a part a flow cannot go without, a skill leave-out with Workflow kept,
  ; or a leave-out of the other harness.
  LeaveOutRefusal.[ Indispensable.LeaveOut NeedsWorkflowLeftOut.LeaveOut NotForHarness.LeaveOut ]
  ContextRefusal.[ ComposerUnavailable ComposerRejected MetaflowMismatch PayloadMismatch ModuleMissing SystemTooLarge ModuleTooLarge ]
  ; HerdrRefusal is Herdr's own answer to a refused agent start, kept whole:
  ; the error code and message of its JSON error body, or no code and the
  ; whole text Herdr printed when it printed no such body.
  HerdrErrorCode.String
  HerdrErrorMessage.String
  HerdrRefusal.{ Option<HerdrErrorCode> HerdrErrorMessage }
  ; SpawnRefusalCause names why the harness start in the launch pane was
  ; refused: Herdr refused it, or Flow refused it before Herdr was called
  ; because an argument carries a control character or the typed command
  ; is longer than one terminal line holds.
  SpawnRefusalCause.[ Herdr.HerdrRefusal ControlCharacter CommandTooLong ]
  ; OpenedThread accounts for the Codex thread Flow opened through the
  ; app-server before a refused harness start: its id, what its first turn
  ; had come to when the start was refused, and whether the app-server
  ; archived it.
  FirstTurn.[ Answered InProgress Unanswered Unread ]
  ThreadArchive.[ Archived ArchiveRefused ]
  OpenedThread.{ NativeSessionId FirstTurn ThreadArchive }
  HarnessSpawnRefusal.{ SpawnRefusalCause Option<OpenedThread> }
  ; NativeTargetRefusal names why Herdr's report of a launch pane is not the
  ; bound native target: Herdr could not be read, the pane is another one,
  ; a Claude pane reports no native session, or the reported harness or
  ; session is not exactly the one bound.
  NativeTargetRefusal.[ HerdrUnreadable PaneMismatch NoNativeSession IdentityInexact ]
  ; RegistrationRefusal names the stage at which a launched flow's
  ; registration was refused: its Herdr route was not verified under its
  ; FlowId claim; its row and role conflict with a flow Flow holds, or were
  ; not written; the pane binding belongs to another launch request; the
  ; acknowledgement is not the native binding; the composed first prompt is
  ; not canonical; the native target is not the one bound; the transcript
  ; boundary could not be captured; or a Codex transcript does not begin by
  ; naming the thread Flow opened. Unclassified marks a stored 18.0.0 unit
  ; refusal whose stage was not kept.
  RegistrationRefusal.[ RouteUnverified RoleConflict RoleUnrecorded PaneBindingForeign AcknowledgementMismatch PromptNotCanonical NativeTarget.NativeTargetRefusal TranscriptBoundary ThreadNotNamed Unclassified ]
  ; NativeLaunchStage names the step of a launch that failed once Flow had
  ; begun it natively: opening the launch pane, opening the Codex thread,
  ; starting the harness before Herdr was asked, binding the started
  ; harness, naming the claimed flow (its title), reading the launch
  ; receipt, or confirming the received flow Active. Unclassified, in stage
  ; and category, marks a stored 18.0.0 unit refusal whose stage was not
  ; kept.
  NativeLaunchStage.[ Open CodexThread Spawn Bind Naming Receipt Confirm Unclassified ]
  ; NativeLaunchFailure is the fixed category of that failure; no adapter
  ; text is carried. The receipt's own: the transcript boundary is not the
  ; intent's, the Codex transcript does not begin by naming the thread
  ; bound, a user turn differs from the startup parts, the session shows a
  ; part its leave-outs removed, or the model or effort differs from the
  ; intent. The confirmation's own: the received flow is not held with its
  ; native session. SendToolUnsupported, at CodexThread: the Codex
  ; app-server was not shown to accept Flow's send tool behind its
  ; experimental API, so no thread was opened.
  NativeLaunchFailure.[ PaneTargetMismatch NativeSessionMissing NativeIdentityConflict FlowClaimUnavailable HarnessMismatch HerdrUnreadable ForeignBinding InvalidFlowId NotReady TranscriptUnreadable TitleReadbackDiffers CodexNamingRefused PaneLabelRefused AdapterRefused BoundaryMismatch ThreadNotNamed PartDiffers LeaveOutShown ModelOrEffortDiffers SessionUnrecorded Unclassified SendToolUnsupported ]
  NativeLaunchRefusal.{ NativeLaunchStage NativeLaunchFailure }
  ; StartRejection preserves a typed BindingRefused result at the public wire.
  ; AddressAwake: the profile's Address is Awake as a live flow, or another
  ; unsettled launch names it. AddressEnded: the Address was ended.
  ; NativeLaunchRefused: a native step of the launch failed, at its stage.
  ; RegistrationRefused: the started flow was not registered, at its stage.
  ; HarnessSpawnRefused: the harness start itself was refused.
  StartRejection.[ CompositionRefused LaunchRequestConflict LaunchPersistenceRefused NativeLaunchRefused.NativeLaunchRefusal BindingRefused.BindingRefusal RegistrationRefused.RegistrationRefusal IntentPersistenceRefused OriginUnavailable AddressAwake AddressEnded ContextRefused.ContextRefusal LeaveOutRefused.LeaveOutRefusal HarnessSpawnRefused.HarnessSpawnRefusal ]
  RestartRejection.[ ProvenanceMismatch UnknownFlow ResumeRefused ]
  RecipientResolutionRejection.[ UnknownFlow FlowUnavailable ]
  StopRejection.[ UnknownFlow AlreadyStopped RouteUnavailable CloseRefused PersistenceRefused ]
  Replaced.{ FlowId Launched }
  ReplaceRejection.[ PredecessorAbsent
                     UnknownPredecessor
                     PredecessorStopped
                     LaunchRefused.StartRejection
                     ReapRefused.StopRejection ]
  ObserveSelection.[ Launch.LaunchRequestId
                     Agent.FlowId ]
  AgentState.[ Idle Working Blocked Done Unknown Gone ]
  AgentObservation.{ FlowId AgentState }
  LaunchStatusRejection.[ UnknownLaunchRequest PersistenceRefused ReadViewChanged InconsistentRecords ]
  Caller.{ FlowId Aspect PowerLevel ModelName }
  CallerResolutionRejection.[ CallerUnknown
                              CallerMismatch.Caller ]
  Title.String
  Presentation.{ Title }
  TranscriptPath.String
  TurnEndRequest.{ SessionId TurnId Option<TranscriptPath> }
  TurnEndRejection.[ UnknownSession SessionMismatch InvalidTurnId InvalidTranscriptPath QueueRefused ]
  Refusal.[ Locked
            Held.Lock
            Awake.FlowId
            Asleep
            Lapsed
            Unknown.[ Address.Address Lock.Lock FlowId.FlowId Key.Key ]
            NoLayer
            NotConfigured
            Ended.Address
            OffRoute
            NoneAbove
            NotMessage
            Taken.Address
            Unidentified.Process
            Store.String ]
  Event.[ Started
          ToolUsed.String
          Stopped ] ]
```

```sh
flow 'ResolveCaller.None'
# from any process in d68c82's pane, 2026-10-17:
# -> CallerResolved.{ d68c82 Psyche Medium
#      claude-opus-5-5 }
```

## Why an old-route flow is no flow

A flow started before Flow, or by the old launchers, has no binding in
Flow's store, so every process in its pane is no flow. Message asks
Flow to identify the sending process; Flow answers
`Refused.Unidentified`, and `hm-send` prints it as:

```sh
FLOW_ID=d68c82 hm-send "Psyche flow Secondary" \
  --psyches --stdin < psyches.edn
# -> MessageRefused.{ «Psyche flow Secondary»
#      Unidentified }
```

That reply is recorded in
`/home/li/primary/flows/d68c82/receipts/launch-flow-ethos-2026-10-17.md`,
from before d68c82 was adopted.

## Adopting a live flow

Adoption was run once, for d68c82, by Field on 2026-10-17
(`/home/li/private-repos/flow-evidence/42265e/direct-starter-retry-20261017/d68c82-sender-binding/`).
It has two steps. The meta socket imports the live flow's native
binding:

```sh
flow-meta 'MetaBindExisting.{ { «default» «/home/li/.config/herdr/herdr.sock» { 4957 1001 «5988» } «42265e» } [ { «d68c82» Psyche Medium «claude-opus-5-5» Claude  «d68c8272-6db0-47dd-9c8e-538d95ff12a6» «w1» «w1:p33» «w1:t2N» «term_65d7bf0f16c9b65» «psyche_core_secondary_d68c82» { 1960918 1001 «117563436» } «/home/li/primary» } ] }'
# -> BoundExisting.{ { default /home/li/.config/herdr/herdr.sock { 4957 1001 5988 } 42265e } [ Bound.{ d68c82 RegisteredUnconfirmed } ] }
```

Then the address is bound with `Bind`, and the process the `Bind` names
must be the process on the socket, alive. The store refuses anything
else (`crates/flow-nexus/src/store/metaflow.rs`):

```rust
if binding.process != *peer || !FlowStore::process_is_live(peer) {
    return Ok(Response::Refused(Refusal::Unidentified(binding.process)));
}
```

So the `Bind` has to be sent from inside the adopted flow's own process
tree. Field's helper checked that its ancestry reached d68c82's Claude
process, then replaced itself with `flow`, keeping its own process id:

```python
pid=os.getpid();parent,started=process(pid)
query='Bind.{ { Psyche core Secondary } { '+str(pid)+' '+started+' } }'
cli=os.path.realpath(shutil.which('flow'))
os.execv(cli,[cli,query])
```

After it, Flow recorded `{ Psyche core Secondary }` as `Awake.d68c82`,
and d68c82's sends were queued with `Sender.{ Psyche core Secondary }`.

An adopted flow keeps the hooks it was started with. d68c82's settings
file carries only a `UserPromptSubmit` reminder hook, no `flow-hook`,
so it never reports `Stopped` to Flow; knowledge-flow-queue says what
that leaves undelivered.

No flow other than d68c82 has been adopted, and no tool adopts flows
in bulk.

## Proposal 2: psyche-context › vision/flow.md

- No flow declares its id: every call to Flow is identified by the calling process.
+ No flow declares its id: Flow finds the flow a call comes from through the calling process and its ancestors.
+ Identifying a caller yields a flow, with its flow ID, or no flow.

Ruling: land, amend, or reject.

## mind-context › knowledge/flow-queue.md

Read on 2026-10-17 in Flow `67b80b3` (0.35.11, installed and running);
the queues were observed through the running Nexus at 12:55 -06:00.

## How a queued request reaches its flow

Every request is queued first. An asleep metaflow is woken by a work
request and gets its whole queue in its first prompt. An awake
metaflow's queue waits for its flow to report the end of a turn
(`Stopped`); Flow then types the oldest request into its pane. Only a
Claude flow that Flow started carries the hook that reports `Stopped`.
A Codex flow, which runs no hook, and an adopted flow, started without
Flow's hook, never report it, so their queue stays.

```
+--------------------------+
| a request queued for a   |
| metaflow                 |
+------+-------------+-----+
       |             |
asleep |             | awake
       v             v
+------------+ +--------------+
| woken: the | | waits for    |
| whole      | | its flow to  |
| queue in   | | report a     |
| one prompt | | turn's end   |
+------------+ +--+--------+--+
                  |        |
 a Claude flow    |        | a Codex flow,
 Flow started     |        | or an adopted
                  |        | flow
                  v        v
         +------------+ +------------+
         | typed in,  | | stays      |
         | oldest     | | queued     |
         | first      | |            |
         +------------+ +------------+
```

A Primary is the exception: it is never woken and never put to sleep,
so what is queued for an asleep Primary waits.

## The code

The request kinds and which of them wake, in
`crates/flow-ethos/ethos/library.ethos` (quoted whole at Flow `67b80b3`;
`Request` and `QueuedRequest` are in it) and
`crates/flow-nexus/src/waking.rs`:

```ethos
; Flow's shared types live in this leaf package. Signal and Meta-Signal
; import them here and re-export their original Rust paths. Aspect is one
; nominal type shared by addresses, launch profiles and meta configuration.

Library
[]
[ FlowId.String
  ; ethos-zero 16 cannot express Topic:Name yet; check camelCase at input.
  Topic.String
  ; The design type is Blake3.Bytes<32>; 16.0 uses a 64-hex-character string.
  Blake3.String
  Layer.[ Primary Secondary Tertiary Quaternary ]
  Subaspect.[ Vision Intent Knowledge Operation Trial Compensation ]
  ; Define the component types once. Source refers to these declarations;
  ; inlining Path.String inside Source would redeclare Path globally.
  Repository.String
  Hash.Blake3
  Path.String
  Reason.String
  Source.{ Repository Hash Path }
  Key.{ Subaspect Topic }
  Said.{ Context.String Verbatim.String }
  Request.[ Order.String
            Question.String
            Psyche.Said
            Psyches.Vector<Said>
            Result.String
            Notice.String ]
  Aspect.[ Psyche Mind Field ]
  Address.{ Aspect Topic Layer }
  Recipient.[ Address Up ]
  ; Who a queued request is from: the Address Flow resolved for its sender
  ; (the Lock's Sender of a Deliver, the thread's metaflow of a send-tool
  ; call), or Unknown for a request queued before Flow kept senders.
  SentBy.[ Sender Unknown ]
  QueuedRequest.{ SentBy Request }
  Metaflow.{ Address
             State.[ Awake.FlowId Asleep Ended ]
             Past.Vector<FlowId>
             Queue.Vector<QueuedRequest> }
  Lock.{ Sender Address Until.Integer }
  Process.{ Pid.Integer Started.Integer }
  Sender.Address
  OrdinarySocketPath.String
  MetaSocketPath.String
  StorePath.String
  Start.{ OrdinarySocketPath MetaSocketPath StorePath }
  ; Startup refusal is distinct from the ordinary/meta socket Refusal.Store.String.
  StoreRefusal.{ Path Reason }
  StartRefusal.[ Store.StoreRefusal ]
  SourceRoot.String
  ClientPath.String
  Home.String
  ControlSocketPath.String
  ModelName.String
  CodexEndpoint.{ ClientPath Home ControlSocketPath Vector<ModelName> }
  StableCodex.CodexEndpoint
  NextCodex.CodexEndpoint
  HarnessKind.[ Codex Claude ]
  KeyName.String
  CommandSigil.String
  InterruptKeys.Vector<KeyName>
  SubmitKeys.Vector<KeyName>
  HarnessProfile.{ HarnessKind Vector<CommandSigil> InterruptKeys SubmitKeys }
  HarnessProfiles.Vector<HarnessProfile>
  MetaAspects.Vector<Aspect>
  MessageNexusPath.String
  MessageNexusBinary.String
  Nexus.{ SourceRoot
          StableCodex
          NextCodex
          HarnessProfiles
          MetaAspects
          MessageNexusPath
          MessageNexusBinary
          Lease.Integer } ] ; Lease seconds; 60 before any Nexus payload.
[]
[]
```

```rust
/// Work and the living's words wake a seat; a Result or a Notice waits
/// queued for its next wake.
fn wakes_for(request: &Request) -> bool {
    matches!(
        request,
        Request::Order(_) | Request::Question(_) | Request::Psyche(_) | Request::Psyches(_)
    )
}

/// A Primary is never woken automatically: what is queued for it waits.
fn wakes_layer(layer: &Layer) -> bool {
    *layer != Layer::Primary
}
```

A wake is due only for an asleep metaflow:

```rust
fn wake_is_due(&self, metaflow: &Metaflow) -> bool {
    metaflow.state == flow_ethos::State::Asleep
        && Self::wakes_layer(&metaflow.address.layer)
        && (metaflow
            .queue
            .iter()
            .any(|queued| Self::wakes_for(&queued.request))
            || metaflow.past.last().is_some_and(|flow_id| {
                matches!(
                    self.store.flow_node(flow_id),
                    Ok(Some(node)) if node.flow_lifecycle.is_live()
                )
            }))
}
```

An awake flow's queue is typed in by `settle_stopped`, which runs when a
`Report` of `Stopped` arrives. The report comes from `flow-hook`, which
Flow puts in the settings of each Claude flow it launches
(`crates/flow-nexus/src/herdr/launch.rs`):

```rust
let mut settings = serde_json::json!({
    "permissions": { "defaultMode": "bypassPermissions" },
    "hooks": {
        "SessionStart": hook,
        "PostToolUse": every_tool,
        "Stop": hook,
    }
});
```

## What the queues held

At 12:55 -06:00, `flow 'Metaflows'` showed two awake metaflows with
work waiting:

| Metaflow | Flow | Waiting |
|---|---|---|
| Psyche flow Secondary | 17c364, Codex, its pane idle | two Orders from Psyche ethos Secondary |
| Psyche core Secondary | d68c82, adopted Claude | one Notice from Psyche flow Secondary |

Earlier that day Field delivered 17c364's queued requests by hand: it
sent Flow a `Report` of `Stopped` after each turn 17c364 had really
finished, and Flow typed the oldest request. That is recorded in
`/home/li/primary/flows/42265e/log.md` and
`/home/li/private-repos/flow-evidence/42265e/direct-starter-retry-20261017/idle-drain-17c364/`.

## The repair, not deployed

Flow 0.35.14, branch `flow-da2038-codex-drain` at `10ced18` (pushed,
not merged to main, not installed), reads each Codex thread's
`turn/started`, `turn/completed` and `thread/status/changed` events
from its app-server, and settles a resting Codex flow the way a
`Stopped` report settles a Claude flow
(`crates/flow-nexus/src/codex_turns.rs`):

```rust
pub enum ThreadTurn {
    /// No event has shown the thread in a turn or at rest.
    Unknown,
    /// In a turn: the one named, or one whose id no event has given.
    Running(Option<String>),
    /// Flow typed work into the seat and no turn has started since.
    Delivered,
    /// Its last turn ended and no other has started.
    Resting,
}
```

Its commit message names Codex flows only; it says nothing of an adopted
Claude flow without `flow-hook`.

## Proposal 3: psyche-context › vision/flow.md

+ Core keeps one flow always open in each aspect: Psyche, Mind and Field.
+ A core flow is restarted fresh when it reaches a set age.
+ Any other flow may be down; it is reached through core.

Ruling: land, amend, or reject.

## mind-context › knowledge/flow-configuration.md

Read on 2026-10-17 in Flow `67b80b3` (0.35.11, installed and running);
the configuration was read from the running Nexus with
`flow-meta 'Configuration'` at 12:55 -06:00.

## How a launch is configured

A Start names its own model. A fresh wake has none to name, so it takes
the one model Flow keeps for its layer. The model then decides the
harness: Codex when a configured Codex endpoint serves it, Claude
otherwise. A Start that names no leave-outs takes its address's
default list, and a list naming another harness's leave-out is
refused.

```
+------------+      +----------------+
| a Start    |      | a fresh wake   |
+-----+------+      +-------+--------+
      |                     |
      | names               | takes its
      | its model           | layer's model
      v                     v
+-----------------------------------+
| the model                         |
+-----------------+-----------------+
                  |
                  | decides
                  v
+-----------------------------------+
| the harness: Codex when a Codex   |
| endpoint serves the model         |
+-----------------+-----------------+
                  |
                  | is checked against
                  v
+-----------------------------------+
| the leave-outs: the Start's own,  |
| or the address's default list     |
+--------+-----------------+--------+
         |                 |
  all of |                 | one of
  this   |                 | another
 harness |                 | harness
         v                 v
+---------------+  +---------------+
| launched      |  | refused       |
+---------------+  +---------------+
```

## One model per layer

The models are keyed by layer alone. The running Nexus holds four, all
Claude:

```sh
flow-meta 'Configuration'
# -> Configuration.{ { … }
#      [ { Primary claude-fable-5-1 }
#        { Quaternary claude-haiku-5-5 }
#        { Secondary claude-opus-5-5 }
#        { Tertiary claude-sonnet-5-5 } ] [] [ … ] }
```

A fresh wake looks up its layer's model
(`crates/flow-nexus/src/waking.rs`, `start_fresh`):

```rust
let Some(model) = snapshot
    .models
    .iter()
    .find(|model| model.layer == address.layer)
else {
    return Err(Failed_Data::CompositionRefused);
};
```

and the harness follows the model (`crates/flow-nexus/src/codex.rs`):

```rust
fn harness_for<N: crate::generated::starter::Textual>(&self, input: N) -> HarnessKind {
    match self.adapter_for(&input.text()) {
        Ok(_) => HarnessKind::Codex,
        Err(_) => HarnessKind::Claude,
    }
}
```

A Codex flow is never resumed, only woken fresh: the wake plan resumes
a Claude flow alone. So, read from the code and not witnessed, a fresh
wake of any Mind, Field or Codex Psyche metaflow starts on the Claude
model of its layer; for `{ Psyche flow Secondary }`, now Astra, that
is `claude-opus-5-5`.

No branch gives a metaflow its own model. Flow 0.35.12, branch
`da2038-model-identity` at `437aa3d` (pushed, not merged, not
installed), refuses a model name that is not exact for its harness; it
keeps one model per layer.

## Default leave-outs per address

The defaults are one list per address, whatever the harness. The running
Nexus holds Claude-only lists for every Psyche address it names and
for the Field illustrator and publisher, and Codex-only lists for
Field core Primary and the Mind core and prototyping addresses:

```sh
flow-meta 'Configuration'
# -> … { { Psyche flow Secondary }
#        [ ClaudeAiConnectors ExplorePlanAgents
#          WorkflowTool SkillTool BundledSkills
#          ScheduleWakeupTool ReportFindingsTool
#          ListAgentsTool CronTools DeferredTools
#          ClaudeMd GitInstructions ] } …
```

A Start that names none takes that list
(`crates/flow-nexus/src/composition.rs`):

```rust
let leave_outs = self
    .launch_profile
    .leave_outs_option
    .clone()
    .unwrap_or_else(|| input.leave_outs());
```

and each leave-out must belong to the launch's harness
(`crates/flow-nexus/src/lean.rs`):

```rust
if leave_out.harness() != self.harness_kind {
    return Some(LeaveOutRefusal::NotForHarness(leave_out.clone()));
}
```

So a Codex Start at a Psyche address, naming no leave-outs, is refused.
The second attempt to start 17c364 on Astra was:

```sh
# /home/li/primary/flows/d68c82/launch/
#   flow-ethos-2026-10-17/flow-start-02.out
# -> StartRejected.LeaveOutRefused.NotForHarness
#      .ClaudeAiConnectors
```

The third attempt named the six Codex leave-outs itself and started.

Flow 0.35.13, branch `flow-da2038-leaveout-harness` at `0a65ff1`
(pushed, not merged, not installed), keeps one default list per
address and harness, and a Start naming none takes the list for its
own harness, or none.

## Proposal 4: psyche-context › vision/flow.md

- A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket.
+ A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the aspect and the layer decide the model, declared once in Flow as configuration and changed only over its meta socket.
+ A metaflow may name its own model, which overrides its aspect and layer.

Ruling:

a. Both lines as shown.

b. The changed line only; Psyche flow Secondary returns to Opus.

c. Neither.

## mind-context › knowledge/flow-receipt.md

Read on 2026-10-17 in Flow `67b80b3` (0.35.11, installed and running).

## How a start is confirmed

Flow records the SHA-256 of every part it types into a new flow: the
modules and the task. It then reads the flow's own transcript. Each
user text there must hash to the next expected part; any other text
refuses the start with `PartDiffers`, and Flow closes the pane. Claude
records a pasted part inside a paste wrapper, which Flow takes off
before hashing.

```
+--------------------------+
| the parts Flow types:    |
| modules, then the task   |
+------------+-------------+
             |
             | each part's hash is kept in
             v
+--------------------------+
| the launch intent        |
+------------+-------------+
             |
             | is compared with
             v
+--------------------------+
| the transcript's user    |
| texts, wrapper taken off |
+------+-------------+-----+
       |             |
 every |             | one
 hash  |             | differs
 equal |             |
       v             v
+------------+ +--------------+
| started    | | refused:     |
|            | | PartDiffers; |
|            | | pane closed  |
+------------+ +--------------+
```

`crates/flow-nexus/src/herdr/launch.rs`:

```rust
fn text_sha256(&self) -> String {
    format!("{:x}", Sha256::digest(self.as_bytes()))
}

fn claude_pasted_content(&self) -> Option<&str> {
    let rest = self.strip_prefix("\n\n<pasted_content id=\"")?;
    let (identifier, rest) = rest.split_once("\">\n")?;
    if identifier.is_empty()
        || identifier.contains(|c: char| c == '"' || c == '<' || c == '>' || c.is_whitespace())
    {
        return None;
    }
    rest.strip_suffix(&format!("\n</pasted_content id=\"{identifier}\">\n"))
}
```

```rust
if expected.is_some_and(|hash| &text.text_sha256() == hash) {
    self.seen_parts += 1;
    self.last_part_answered = false;
    return Ok(self.seen_parts);
}
Err(NativeLaunchFailure::PartDiffers)
```

## A task that ends in a newline

The deployed unwrapping always takes a newline off before the closing
tag. By the commit message of the repair below, Claude Code 2.1.294
writes that newline only when the part does not already end in one;
so a part ending in a newline loses its own last newline, and its hash
differs. d68c82 recorded the same by hash for its first start of
804eb9 (`/home/li/primary/flows/d68c82/receipts/launch-flow-ethos-2026-10-17.md`):

```sh
# flows/d68c82/launch/flow-ethos-2026-10-17/
#   ethos-start.out
# -> StartRejected.NativeLaunchRefused.{ Receipt
#      PartDiffers }
```

The start that followed trimmed the task's trailing whitespace and was
accepted:

```js
brief: `Address.{ Psyche ${spec.topic} Secondary }\n\n` + fs.readFileSync(new URL(spec.brief, import.meta.url), "utf8").trimEnd(),
```

Primary's `tools/flow-start-adapter.mjs` passes the task as given; it
does not trim it.

## The repair, not deployed

Flow 0.35.15, branch `flow-da2038-receipt` at `517ea88` (pushed, not
merged, not installed), rebuilds Claude's paste element from the part
under the recorded id and accepts the part only when the rebuilt
element equals the transcript row byte for byte.

<!-- to-the-living:end -->
