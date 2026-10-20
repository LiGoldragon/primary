<!-- to-the-living:start -->
Presentation.{ «Flow as it runs» }

# Flow as it runs

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

## Proposal 1: A flow sleeps only as a Claude flow below Primary · mind-context › knowledge/flow-queue.md

+ A flow is put to sleep only when its turn ends with nothing queued and it is a Claude flow below Primary that Flow started.
+ A Primary, a Codex flow and an adopted flow stay awake in their panes.

```
+------------------+   +------------------+
| a Claude flow    |   | a Primary, a     |
| below Primary,   |   | Codex flow, or   |
| started by Flow  |   | an adopted flow  |
+--------+---------+   +--------+---------+
         |                      |
         | ends its turn        | ends its turn
         | with nothing         | and stays
         | queued and falls     |
         v                      v
+------------------+   +------------------+
| asleep: pane     |   | awake in its     |
| closed, session  |   | pane             |
| kept             |   |                  |
+--------+---------+   +------------------+
         |
         | is woken by an order,
         | a question or the
         | living's words into
         v
+------------------+
| awake: resumed,  |
| or fresh when    |
| too big          |
+------------------+
```

Ruling: land, amend, or reject.

## primary › tools/claude-main-flow-launch.mjs

```js
#!/usr/bin/env node
// Legacy command name; Flow owns context composition, native launch and receipts.
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {parseArgs as parse, launchMain} from './flow-start-adapter.mjs';
export const parseArgs = argv => parse(argv, 'claude');
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try { launchMain(parseArgs(process.argv.slice(2)), 'claude'); }
  catch (error) { console.error(`launch failed: ${error.message}`); process.exitCode = 1; }
}
```

## flow › crates/flow-nexus/ethos/curriculum.ethos

```ethos
; ID-only in-memory composition. No caller paths, source bodies or file projection.
Library
[]
[ ModuleIdentity.String
  RepositoryName.String
  SourceRevision.String
  SourceRoot.String
  SourceRelativePath.String
  ModuleType.String
  ModuleSubject.String
  DeclaredPlacement.String
  SourceSha256.String
  BodySha256.String
  RenderedSha256.String
  Target.[ Claude Codex Pi OpenCode ]
  CallerMetaflow.{ String String String }
  StartupPlacement.[ System User ]
  SystemModules.Vector<ModuleIdentity>
  UserModules.Vector<ModuleIdentity>
  SystemText.String
  UserText.String
  SystemPayloadSha256.String
  UserPayloadSha256.String
  StartupSelection.{ CallerMetaflow Target SystemModules UserModules }
  ContextProvenance.{ ModuleIdentity RepositoryName SourceRevision SourceRelativePath SourceSha256 BodySha256 RenderedSha256 StartupPlacement Integer }
  StartupComposition.{ SystemText UserText SystemPayloadSha256 UserPayloadSha256 Vector<ContextProvenance> }
  ResolvedModule.{ ModuleIdentity RepositoryName SourceRevision SourceRoot SourceRelativePath ModuleType ModuleSubject DeclaredPlacement SourceSha256 BodySha256 String Vector<String> }
  RoleName.String
  ModelId.String
  DescriptionModule.ModuleIdentity
  ContextModules.Vector<ModuleIdentity>
  DescriptionText.String
  ContextText.String
  DescriptionPayloadSha256.String
  ContextPayloadSha256.String
  Permission.[ Restricted Unrestricted ]
  Effort.[ Low Medium High Xhigh ]
  Surface.[ ClaudeAgent CodexAgent PiAgent ]
  RoleTools.[ Inherit Explicit.Vector<String> ]
  RoleCallers.[ Any Only.Vector<CallerMetaflow> ]
  RoleDefinition.{ RoleName Surface ModelId Effort Permission DescriptionModule ContextModules RoleTools RoleCallers }
  Roles.{ Vector<RoleDefinition> }
  RolesDocument.[ Roles.Roles ]
  RoleSelection.{ RoleName Surface }
  RoleComposition.{ RoleName Surface ModelId Effort Permission DescriptionText ContextText RoleTools RoleCallers Vector<ContextProvenance> DescriptionPayloadSha256 ContextPayloadSha256 }
  CliRequest.[ ResolveSkills.Vector<ModuleIdentity>
               ResolveSources.Vector<ModuleIdentity>
               ComposeStartup.StartupSelection
               ComposeRole.RoleSelection ]
  Query.[ ResolveSkills.Vector<ModuleIdentity>
          ResolveSources.Vector<ModuleIdentity>
          ComposeStartup.StartupSelection
          ComposeRole.RoleSelection ]
  Outcome.[ ResolvedSkills.Vector<ModuleIdentity>
            ResolvedSources.Vector<ResolvedModule>
            StartupComposed.StartupComposition
            RoleComposed.RoleComposition
            Rejected.String ] ]
[]
[]
```

## flow › crates/flow-nexus/ethos/library.ethos

```ethos
; The process identity supplied at startup. These paths select the
; listeners; they do not come from or mutate the durable Nexus settings.

Library [] [ Start.{ OrdinarySocketPath.String MetaSocketPath.String StorePath.String } ] [] []
```

## flow › crates/flow-nexus/ethos/operation.ethos

```ethos
; Flow Nexus Operation: what the Nexus does. Every effect its launch and
; record paths perform is one operation, and each is answered by one
; Outcome. An effect changes something: Herdr's panes, a harness, the
; or the store. A read of the world (a pane's presence, a transcript
; receipt, a seat's composed context) is not an operation.
;
; Compose has the context composer compose the seat's system and USER
; context from the module identities its profile names, verifies it, and
; composes the system prompt and the first USER message, split into parts
; when it does not fit one message; nothing is written to disk.
; Reserve opens the launch attempt in the journal and, for a Claude launch,
; claims the flow's FlowId for the native session id Flow chooses for it,
; and holds that flow in Memory before any harness runs: Reserved carries
; the FlowId, Spawn starts the harness with it as FLOW_ID and that session
; id, and Bind verifies the harness came up as the flow reserved. A Codex
; launch reserves no FlowId; Bind claims it from the session Codex reports. Record writes one
; journal or lifecycle entry; Record.Harness appends the harness event a
; Report carried to the events Flow's Memory holds for that flow, and a
; flow Flow does not hold fails UnknownFlow and is never adopted.
; Record.Context writes the tokens a flow's native session carried into
; its last turn, read from its transcript when its hook reports Stopped.
; Register binds a flow's row and role. Confirm makes a Pending launch
; Active and records the Address its launch profile names Awake as it, in
; one write, and answers Started; an Address Awake as a live flow fails
; AddressAwake, an Ended one AddressEnded, and the launch stays Pending. Open makes the launch pane; Spawn starts
; the native harness in it. A Codex Spawn first opens the thread through
; the app-server with the system prompt as its base instructions and the
; launch's exclusions in its config, reads them back, and submits the first
; part of the first USER message as the thread's first turn; only then
; does the TUI attach to that thread, and Spawned names it; the thread is
; recorded for the launch request first, so a launch recovered after its
; start binds to it. A start Herdr
; refuses, or one Flow refuses before calling Herdr, fails SpawnRefused with
; its cause and, for Codex, the thread it had opened, archived. Open, a
; Codex thread's opening, a Spawn Flow did not attempt, Bind and Title fail
; LaunchRefused with the stage and the fixed category of the failure. Bind claims the
; flow's identity from the harness's integration report, and for Codex
; requires the thread Spawn opened; Title names the claimed flow; Submit
; types the next part of the first USER message once (the last part
; carries the brief), and for Codex first applies the exclusions to the
; attached thread again and reads them back, a first part being already in
; the thread; Close closes a flow's pane. Release gives back what
; Reserve took for a launch then refused: the held flow and its FlowId
; claim, answered Released.
;
; Sleep, Wake and Drain move a metaflow between Awake and Asleep so a seat
; that is not running keeps no harness. Sleep closes the pane of the flow a
; metaflow is awake as and records it Asleep (Record.Asleep), keeping the
; flow's native session so a later wake can resume it. Wake reads the whole
; queue of an Asleep metaflow, oldest first, and starts a seat that carries
; it in its first prompt: the last flow resumed when its session is under
; its layer's refresh threshold, else a fresh launch composed from the
; configured layer Model and the module identities the seat's last launch
; named. Record.Awoken then names the
; started flow and the count of queued requests it was handed, which leave
; the queue in that same write, so a wake that dies first loses nothing.
; Drain types the oldest queued request into the Awake flow's pane and
; removes it once typed, answering what it typed. Wake runs off the
; dispatch gate and takes it per step.
;
; Record.Refresh marks one Asleep metaflow so its next wake starts a fresh
; launch composed from the modules and leave-outs its last launch named,
; whatever its context size; the mark is a row of its own, keyed by the
; Address, and Record.Awoken retracts it in the write that records the wake.
; A mark already held is left as it is. It fails NotAsleep for a metaflow
; that is not Asleep.
;
; LaunchOutcome and Replacement are the store's own types, imported from
; the Nexus crate until the Memory root is compiled.

Operation
[ signal_flow:[ FlowId LaunchRequestId FlowNode Caller LaunchProfile ComposedLaunch Origin LaunchAttemptReservation HerdrPaneBinding NativeLaunchIntent NativeLaunchBinding RegistrationAcknowledgement PromptDeliveryIntent PromptDeliveryResult Launched Event Address Request QueuedRequest ContextRefusal LeaveOutRefusal NativeSessionId HarnessSpawnRefusal NativeLaunchRefusal ]
  flow_nexus:[ LaunchOutcome Replacement ] ]
[ Compose.LaunchProfile
  Reserve.{ ComposedLaunch Origin }
  Record.[ Intent.NativeLaunchIntent
           Binding.NativeLaunchBinding
           Acknowledgement.RegistrationAcknowledgement
           Delivery.PromptDeliveryIntent
           Delivered.PromptDeliveryResult
           Active.FlowId
           Stopped.FlowId
           Retired.FlowId
           Exited.FlowId
           Replacing.Replacement
           Withdrawn.LaunchRequestId
           Settled.{ LaunchRequestId LaunchOutcome }
           Harness.{ FlowId Event }
           Context.{ FlowId Tokens.Integer }
           Asleep.{ Address FlowId }
           Awoken.{ Address FlowId Delivered.Integer }
           Refresh.Address ]
  Register.{ FlowNode Caller }
  Confirm.FlowId
  Open.ComposedLaunch
  Spawn.PaneLaunch
  Bind.PaneLaunch
  Title.{ ComposedLaunch NativeLaunchBinding }
  Submit.{ ComposedLaunch PromptDeliveryIntent }
  Close.FlowNode
  Release.FlowId
  Sleep.{ Address FlowNode }
  Wake.Address
  Drain.Address ]
[ Composed.ComposedLaunch
  Reserved.{ LaunchAttemptReservation Option<FlowId> }
  Recorded
  Registered.FlowNode
  Started.Launched
  Opened.HerdrPaneBinding
  Spawned.Option<NativeSessionId>
  Bound.NativeLaunchBinding
  Titled
  Submitted.PromptDeliveryResult
  Closed
  Released
  Slept
  Woken.FlowId
  Drained.Vector<QueuedRequest>
  Failed.[ CompositionRefused
           StoreRefused
           ConflictingBinding
           Unstarted
           HerdrRefused
           CodexRefused
           UnknownFlow
           ClaimRefused
           NotAsleep
           NotAwake
           NothingQueued
           AddressAwake
           AddressEnded
           ContextRefused.ContextRefusal
           LeaveOutRefused.LeaveOutRefusal
           SpawnRefused.HarnessSpawnRefusal
           LaunchRefused.NativeLaunchRefusal ] ]
[ PaneLaunch.{ ComposedLaunch HerdrPaneBinding Option<FlowId> Option<NativeSessionId> } ]
```

## flow › crates/flow-nexus/ethos/send_tool.ethos

```ethos
; The send tool: every Codex thread Flow opens declares one dynamic tool,
; `send`, and the Nexus answers its calls. A call names a target Address, a
; kind and a body; the sender is never in the call. It is the metaflow
; Flow's records bind to the calling thread, read again each time a call is
; handled, a replayed one included: the thread's flow must be live and its
; metaflow Awake as it, or, while the launch that opened the thread is
; unsettled and no other flow or launch holds its Address, the sender is
; that launching metaflow. The thread is recorded as its launch's before
; the first turn is started, and the connection that started it, subscribed
; to its calls, answers them, so a first turn's call is served while the
; launch still waits for its seat to come to rest. The request is queued for the target under the
; rules a Lock and a Deliver from Message follow, and the call and its
; outcome are recorded in the commit that queues it, keyed by the thread,
; the turn and the call, so a replayed call is answered from the record and
; queued once.
;
; A request queued for an Asleep metaflow wakes it by what Flow's records
; hold, never by what the answer to the call carries: after the commit
; that queues it, after a replayed call is answered from its record, and
; at the Nexus's start, the target is woken when it is Asleep holding work
; that wakes it and no wake runs for it already.
;
; Kinds are the requests a flow may send. The living's words (Psyche,
; Psyches) are not among them: Flow admits a Lock and a Deliver from the
; bound Message process alone, so no route through Flow lets a flow send
; them.
;
; This attributes a call to a thread by Flow's records; it does not
; authenticate who started the turn. Any process of the same user can start
; a turn on a thread through the app-server socket.

Library
[ signal_flow:[ Address Sender ]
  serde_json:JsonValue.Value ]
[ SendKind.[ Order Question Result Notice ]
  Target.Address
  Body.String
  ; What the model passes the tool, typed.
  SendArguments.{ Target SendKind Body }
  ThreadId.String
  TurnId.String
  CallId.String
  ToolName.String
  ; The app-server names a call by its thread, its turn and its call id.
  ToolCallKey.{ ThreadId TurnId CallId }
  ; One item/tool/call as the app-server sent it; Arguments is the JSON
  ; text the model wrote.
  ToolCall.{ ToolCallKey ToolName Arguments.String }
  ; The digest of the tool name and the canonical JSON of its arguments.
  ContentSha256.String
  ; UnknownTool: the call names no tool Flow declared. Malformed: its
  ; arguments are no SendArguments. ThreadUnowned: no flow Flow holds runs
  ; the thread. FlowEnded: the thread's flow is Stopped, Retired or Exited.
  ; NotAwake: its metaflow is not Awake as it (Asleep, or a Refresh or a
  ; fresh wake moved it on). KeyReused: the call's key was recorded with
  ; other content. UnknownRecipient and RecipientEnded: the target is no
  ; metaflow, or an Ended one. Held: Message holds a lock on the target,
  ; about to deliver. Store: the store refused; the Nexus log names why.
  SendRefusal.[ UnknownTool
                Malformed
                ThreadUnowned
                FlowEnded
                NotAwake
                KeyReused
                UnknownRecipient.Target
                RecipientEnded.Target
                Held
                Store ]
  ; Queued is a durable enqueue for the target, never a claim of delivery.
  SendOutcome.[ Queued.{ Sender Target }
                Refused.SendRefusal ]
  ; The record a handled call leaves.
  SendCall.{ ToolCallKey ContentSha256 SendOutcome } ]
[ ; The values the capabilities read, each through the trait that yields it.
  ParamsCarrying.[ params.[ JsonValue ] ]
  ToolCallCarrying.[ tool_call.[ ToolCall ] ]
  ; The tool every Codex thread Flow opens declares.
  DeclaresSendTool.[ tool_name:[ ToolName ]
                     tool_spec:[ JsonValue ] ]
  ; An item/tool/call's params read as a ToolCall; None when they name no
  ; thread, turn, call or tool.
  ReadsToolCall.[ read_tool_call:{ [ ParamsCarrying ] [ Option<ToolCall> ] } ]
  ; A call's arguments read as SendArguments, and the digest of its content.
  ReadsSendArguments.[ send_arguments.[ Option<SendArguments> ]
                       content_sha256.[ ContentSha256 ] ]
  ; The DynamicToolCallResponse a call is answered with: one inputText
  ; item, the outcome as its datom; success only when it was queued.
  AnswersToolCall.[ tool_response.[ JsonValue ] ]
  ; The Nexus handles one call under the dispatch gate. A Queued outcome
  ; names the target whose wake is then decided from Flow's records,
  ; whether or not the answer reaches the app-server. A launch holding the
  ; gate handles its own thread's calls as the gate's holder.
  HandlesSendCall.[ handle_send_call.{ [ ToolCallCarrying ] [ SendOutcome ] }
                    handle_held_send_call.{ [ ToolCallCarrying ] [ SendOutcome ] } ] ]
[]
```

## flow › crates/flow-nexus/ethos/starter.ethos

```ethos
; The direct-text starter: a launch names its flow's context by module
; identity; the context composer composes it and Flow verifies it; the
; first USER message is the composed USER text then the brief, sent whole
; through Herdr's socket or the Codex app-server, or in parts split where
; modules begin, each part after the first sent once the flow has answered
; the one before; the receipt is every part seen in order, then the flow's
; first answer.
;
; A capability takes traits, never concrete values: each value a starter
; capability reads (a text, a profile, a request, a transcript row) reaches
; it through the trait that yields it, which the concrete type implements.
;
; VerifiedContext is the guard: its fields are private and its one
; constructor is VerifiesContext.verified, so no text but the composer's
; verified answer reaches a prompt. It stays a Rust type of its own because
; a generated type's fields are public.

Library
[ signal_flow:[ Address HarnessKind PowerLevel LaunchProfile PromptDeliveryIntent NativeTargetReceipt FlowId SessionId Origin SystemModules UserModules HerdrSessionName LeaveOuts LeaveOutRefusal ComposedLaunch ContextRefusal SystemPrompt HerdrPaneBinding PromptDeliveryResult Response Launched NativeLaunchFailure ]
  flow_nexus:[ StartupSelection StartupComposition ContextProvenance CurriculumQuery CurriculumOutcome CompositionError VerifiedContext OperationOutcome CallerProcess ]
  serde_json:JsonValue.Value ]
[ ; What a launch asks of the context composer.
  ContextRequest.{ Address HarnessKind SystemModules UserModules }
  ; A launch profile with the harness the Nexus derived for its model.
  HarnessedProfile.{ LaunchProfile HarnessKind }
  ; What a fresh wake takes from the metaflow's last launch.
  FreshContext.{ HerdrSessionName SystemModules UserModules Option<LeaveOuts> }
  ; A Started launch as its outcome row keeps it; the flow's route is read
  ; from the flow's own row when the reply is made.
  LaunchedRecord.{ FlowId SessionId Origin }
  ReplacedRecord.{ FlowId LaunchedRecord }
  ; What a launch attempt's row knows of the context its seat started with.
  ; Modules: its profile names that context by module identity.
  ; BeforeModules: Flow kept the launch before 0.35.0, when a launch named
  ; its context by skill sources and a system-prompt bundle file. Its profile
  ; names no module and leaves nothing out, its native intent names no
  ; system-prompt hash, its one first message is its one part, and the Stop
  ; count at that part was not kept; what it named instead is kept here
  ; whole, with the origin clue its caller named and the skill names its
  ; native launch intent recorded.
  LaunchSource.{ SourcePath.String SourceSha256.String }
  LaunchSources.Vector<LaunchSource>
  NativeSkill.{ SkillName.String SkillPath.String SkillSha256.String }
  NativeSkills.Vector<NativeSkill>
  OriginClue.{ FlowId SessionId TurnId.String }
  ContextBeforeModules.{ LaunchSources Skills.Vector<String> PowerLevel HarnessKind BundleFile.String OriginClue LaunchIntentSkills.Option<Vector<String>> IntentSkills.Option<NativeSkills> ResultSkills.Option<NativeSkills> }
  LaunchContext.[ Modules
                  BeforeModules.ContextBeforeModules ]
  ; What the native transcript shows of a first USER message: Received is
  ; every part in order then the first answer; Waiting is not yet; and
  ; PartAnswered is every submitted part seen, the last answered, and parts
  ; left to send.
  StartupProgress.[ Received.NativeTargetReceipt
                    Waiting.PromptDeliveryIntent
                    PartAnswered.PromptDeliveryIntent ]
  ; Where one reading of the transcript stands.
  SeenParts.Integer
  LastPartAnswered.Boolean
  NativeTurn.String
  PartTurn.String
  StartupReading.{ SeenParts LastPartAnswered Option<NativeTurn> Option<PartTurn> }
  ; A harness start and the parts it leaves out.
  LeanStart.{ HarnessKind LeaveOuts } ]
[ ; The values capabilities read, each through the trait that yields it.
  Textual.[ text.[ String ] ]
  Profiled.[ profile.[ LaunchProfile ]
             harness_kind.[ HarnessKind ] ]
  LeaveOutListing.[ leave_outs.[ LeaveOuts ] ]
  ContextRequesting.[ context_request.[ ContextRequest ] ]
  StartupComposing.[ composition.[ StartupComposition ] ]
  CurriculumQuerying.[ query.[ CurriculumQuery ] ]
  ProvenanceListing.[ provenance.[ Vector<ContextProvenance> ] ]
  SegmentListing.[ segments.[ Vector<String> ] ]
  PartNumbering.[ part_number.[ Integer ]
                  part_count.[ Integer ] ]
  SystemPrompted.[ system_prompt.[ SystemPrompt ] ]
  PaneBound.[ pane.[ HerdrPaneBinding ] ]
  JsonRow.[ row.[ JsonValue ] ]
  DeliveryIntended.[ intent.[ PromptDeliveryIntent ] ]
  Progressing.[ progress.[ StartupProgress ] ]
  OutcomeCarrying.[ outcome.[ OperationOutcome ] ]
  LaunchedRecording.[ launched_record.[ LaunchedRecord ] ]
  CallerProcessing.[ caller_process.[ Option<CallerProcess> ] ]
  ; The starter's capabilities.
  ComposesFlowContext.[ compose_flow_context.{ [ ContextRequesting ] [ Result<StartupComposition ContextRefusal> ] } ]
  OpensCurriculumComposer.[ at:{ [ Textual ] [ Self ] }
                            from_environment:[ Self ] ]
  SelectsStartup.[ startup_selection.[ StartupSelection ] ]
  ExchangesCurriculumFrames.[ exchange.{ [ CurriculumQuerying ] [ Result<CurriculumOutcome String> ] } ]
  VerifiesContext.[ verified:{ [ ContextRequesting StartupComposing ] [ Result<Self ContextRefusal> ] } ]
  ReadsVerifiedContext.[ address.[ Address ]
                         system_text.[ String ]
                         user_segments.[ Vector<String> ] ]
  CutsRenderedText.[ rendered_segments.{ [ ProvenanceListing ] [ Option<Vector<String>> ] } ]
  FitsOneMessage.[ fits_one_message.{ [ Textual ] [ Boolean ] }
                   system_argument.{ [ Textual ] [ String ] }
                   fits_one_argument.{ [ Textual ] [ Boolean ] } ]
  SplitsStartupMessage.[ part_header:{ [ PartNumbering ] [ String ] }
                         startup_parts.{ [ SegmentListing Textual ] [ Result<Vector<String> ContextRefusal> ] } ]
  JoinsContextAndBrief.[ joined_with.{ [ Textual ] [ Vector<String> ] } ]
  RendersBrief.[ brief.[ String ] ]
  ResolvesLeaveOuts.[ effective_leave_outs.{ [ LeaveOutListing ] [ Result<LeaveOuts CompositionError> ] } ]
  ComposesVerifiedContext.[ verified_context.{ [ Profiled ] [ Result<VerifiedContext CompositionError> ] }
                            launch_system_prompt.{ [ Profiled ReadsVerifiedContext ] [ Result<SystemPrompt ContextRefusal> ] } ]
  AssemblesComposedLaunch.[ assembled:{ [ Profiled SystemPrompted Textual SegmentListing LeaveOutListing ] [ ComposedLaunch ] } ]
  ComposesLaunch.[ compose.{ [ Profiled LeaveOutListing ] [ Result<ComposedLaunch CompositionError> ] }
                   resumption.{ [ Profiled LeaveOutListing Textual ] [ Result<ComposedLaunch CompositionError> ] } ]
  ProfilesFreshSeat.[ fresh_profile.[ LaunchProfile ] ]
  PromptsThroughHerdrSocket.[ herdr_session_socket.{ [ Textual ] [ Result<String String> ] }
                              prompt_through_socket.{ [ PaneBound Textual ] [ Result<JsonValue String> ] } ]
  ReadsStartupRecord.[ read_record!{ [ JsonRow DeliveryIntended ] [ Result<Option<String> NativeLaunchFailure> ] }
                       read_part!{ [ Textual DeliveryIntended ] [ Result<Integer NativeLaunchFailure> ] } ]
  ReadsTypedUserText.[ claude_typed_text.[ Option<String> ] ]
  RendersLeanStart.[ refusal.[ Option<LeaveOutRefusal> ]
                     arguments.[ Vector<String> ]
                     environment.[ Vector<String> ]
                     disallowed_tools.[ Vector<String> ]
                     attribution_off.[ Boolean ]
                     skill_listing_off.[ Boolean ] ]
  SettlesStartupProgress.[ settle_progress.{ [ Profiled DeliveryIntended Progressing ] [ Response ] }
                           advance_startup.{ [ Profiled DeliveryIntended ] [ Response ] }
                           stops_reported.{ [ Textual ] [ Integer ] }
                           composition_refused:{ [ OutcomeCarrying ] [ Response ] } ]
  NamesLaunchedRoute.[ launched.{ [ LaunchedRecording ] [ Launched ] } ]
  DerivesOrigin.[ origin_of.{ [ CallerProcessing ] [ Origin ] } ]
  DerivesHarness.[ harness_for.{ [ Textual ] [ HarnessKind ] } ] ]
[]
```

## flow › crates/flow-nexus/ethos/startup.ethos

```ethos
; Startup paths are one explicit input to this Flow process. Refusal carries
; the path and reason without turning a foreign or older store into an empty
; database.
Library
[]
[ OrdinarySocketPath.String
  MetaSocketPath.String
  StorePath.String
  Start.{ OrdinarySocketPath MetaSocketPath StorePath }
  Path.String
  Reason.String
  StoreRefusal.{ Path Reason }
  StartRefusal.[ Store.StoreRefusal ] ]
[]
[]
```

## mind-context › knowledge/flow.md

Before launching, naming, claiming, reaching, or reporting a Flow, read
the matching deployed source and obtain the target's explicit response
through the current ordinary or meta socket. Do not infer protocol,
caller identity, store state, or runtime bindings from a source version
or client path.

## Stated configuration and launch contract

These are the authorized contracts; this section does not establish deployed runtime behavior while the configuration rewrite is pending.

The tool that starts flows merges its configuration files in order, shared, aspect, metaflow, map into map, so a later file's value wins at each key.

A context is young while it stays under half the layer's refresh threshold.

A launch that needs a Primary starts its Secondary first.

## Proposal 2: Primary's launch commands go through Flow · mind-context › knowledge/flow.md

+ Primary's `tools/claude-main-flow-launch.mjs` and `tools/codex-main-flow-launch.mjs` start a flow by sending Flow a `Start` through `tools/flow-start-adapter.mjs`, since Primary `8307d45` of 2026-10-16.
+ Before that commit they started the harness in Herdr themselves, and Flow does not know a flow started that way until it is adopted: it answers `Current.Unknown` for its address.

```
+----------------------+  +----------------------+
| Primary's launch     |  | Primary's launch     |
| commands, before     |  | commands, since      |
| 8307d45              |  | 8307d45              |
+----------+-----------+  +----------+-----------+
           |                         |
           | start in Herdr          | send Start to
           v                         v
+----------------------+  +----------------------+
| a flow Flow does     |  | Flow, which starts   |
| not know             |  | the flow in Herdr    |
+----------------------+  +----------+-----------+
                                     |
                                     | records
                                     v
                          +----------------------+
                          | its metaflow, which  |
                          | Flow puts to sleep,  |
                          | wakes and messages   |
                          +----------------------+
```

Ruling: land, amend, or reject.

## Proposal 3: How a flow's session is named · mind-context › knowledge/flow.md

+ Flow's starter names a flow's Herdr workspace and agent `claude-` or `codex-` followed by the first 24 hexadecimal characters of the SHA-256 of its launch request id.
+ The flow's proper name, such as `{ Psyche ethos Secondary 804eb9 }`, is only its title.
+ Primary's launch commands before `8307d45` named the Herdr agent from the title in snake_case, cut to Herdr's 32 characters, such as `psyche_core_secondary_d68c82`.
+ The Herdr workspaces and agents of 804eb9, 17c364 and 75f438, which Flow started, carry names set by hand on 2026-10-18: `psyche_ethos_secondary_804eb9`, `psyche_flow_secondary_17c364` and `field_startup_0355_quat_75f438`.

Ruling: land, amend, or reject.

## psyche-context › vision/flow.md

## What it does

The Flow Nexus sets up and starts a model flow: its working
directory, system prompt, training files and instruction prompt. It
takes the place of the abandoned training daemon.

Flow is the Nexus that manages flows. A flow is one run of a voice; the component is named for what it manages. A flow the living asks for is launched, properly and surely. Flow holds the lock on flows.

Flow is for starting flows cheaply: clean lean flows, specialized flows and refreshed flows, each with a clean on-point context, which yields higher-quality output. A flow is taken down as easily as it is started. Starting flows is the cornerstone of the system. Flow is probably the most important component to bootstrap, designed together with the Nexus architecture and Ethos.

A flow is one LLM chat, linear and very limited; an agent is a whole being, a lot more than that. Many flows, properly structured and orchestrated, together resemble a synthetic intelligence, synthesized from human knowledge and mathematical probability.

The Capsule is the component that makes where a flow runs. Its first embodiment is the semi-sandbox: only the credential files are copied, everything else is recreated, with its own sockets and store, running light models. Later it encrypts the sensitive parts of the filesystem under a volatile key.

Flow manages metaflows. A metaflow is one address, { Aspect Topic Layer }, that continues through several flows one after another; the flow is its current run, and what is addressed is always the metaflow, never a flow. The default topic is core: the permanent topic, the thing that keeps the machine going, the last topic to stand.

Psyche, Mind and Field have similar payloads, and they go under one: the metaflow, whose aspect is Psyche, Mind or Field.

A topic never dies; it goes idle, its flows turned off. When the living touches on it again, whether to wake a flow for it, and at which layer, is a judgment, made by a small model; a topic is bound to its context modules, so Flow knows what to start it with, together with the new input that warrants it.

A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, kept to six characters and lengthened when two collide, so a transcript is found from the flow id. Where the harness lets Flow choose the session id, Flow chooses it before the flow starts and the flow reads it in its prompt; where the harness assigns it, Flow learns it when the flow binds. No flow declares its id: every call to Flow is identified by the calling process. Anybody may call Flow, a flow for its own refresh among them: because the CLI checks the calling process, a flow refreshes itself safely.

A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context. A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started. A metaflow a request needs is started whether or not it is running; with no working transcript to reawaken, it is fed the metaflow's context modules and the prompt it is to get now.

What has been queued for an idle metaflow, the vision touching its topic among it, is injected with the request that wakes it, so the flow knows it as soon as it wakes.
A metaflow is not woken each time something touching its topic accumulates.

Flow exposes everything from the harness, the bare input: a flow is started, stopped and sent a message through Flow, and Message makes use of it. Flow deploys first and is used raw to send messages, until Message sends through Flow's socket.

## Starting flows

A Nexus component decides the system prompt and everything about a
launch, replacing the harness's subagents with specialized harnesses
launched with specialized system prompts.

A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry.

To the Nexus, a module's location is nothing but its registry entry.

The system prompt is not one thing: it is composed of modules of several types, and what a harness calls a skill overlaps with them.
Its anatomy is drawn up in ethos from a study of system prompts of every kind, each line placed by what it is and by the kind of guidance it belongs to.
Where the harness allows it, a part of a main flow's system prompt is the main flow's alone and is not passed down to its subagents.

Every flow has a topic; a flow with no special topic has the topic core, the heart of its aspect. A topic is a core:Name, a camelCaseExpression checked when created. A flow's title is one datom struct of its aspect, topic, layer and flow id: { Psyche core Secondary <id> }.

Who speaks to whom, within an aspect and across aspects at the same layer in a shared topic, is the vision-aspects skill's. Flow refuses a request that leaves those routes.

## Long term: modules checked by hash

Long term, every module composed into a prompt is checked against its source by its hash, once hashes update efficiently as edits are made; short term, no check is made.

## Repository and context modules

The flow repository holds the machinery of the Flow Nexus and is a runtime repository.
Every context module lives outside it, the basic modules included, so that a change to a module causes no Nix rebuild.
The basic modules give our own take on how an agent behaves in a harness, replacing the prompt the harnesses build in.

## A session is named after its direct ancestor

## A replaced session is reaped by the refresh itself

Reaping belongs to the refresh event, not to a later sweep. A refreshed flow
takes the replaced end out of receiving messages, so a dead end is never
left registered and addressable.

Every harness event reaches Flow through the harness's hooks calling the Flow CLI, so Flow knows each flow's state without polling; a marked block landing in a transcript becomes an action, a book among them, with no tool call by the flow; a flow nearing its context limit is told, writes its handover, and is refreshed as it goes idle. Polling is forbidden; a poller that must exist is registered and reported.

A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.

## Subflows replace the harness subagent facility

The harness subagent facility is replaced. It puts two flows into one
synchronous user interface and locks them both into a single main
flow. A subflow is instead an independent flow with its own system
prompt, which can reply to the successor of whoever it was meant to
answer; that makes the system asynchronous. Subflows run under their
own system prompts because they need different prompts.

## Subflows are created from the questions and requests a flow ends with

Creating a subflow is a routing job: whether there is already a flow
that should simply get this message or this question. A Field
Quaternary flow checks every question and every
request a flow ends with, and, according to the ending flow's
authority, spawns subflows given those questions and requests to
answer or fulfill.

## The requester holds only a request ID

The requester holds nothing of the subflow itself. It is assigned a
request ID, by which it asks later for status, asks for more detail
about what that subflow is doing, and sends the subflow messages
while it is alive. When the subflow is done, the requester receives a
message if it is still the flow in charge.

## Proposal 4: Flow names the session after the flow · psyche-context › vision/flow.md

+ Flow names a flow's Herdr workspace and agent from its title in snake_case, cut to Herdr's 32 characters: `psyche_core_secondary_d68c82`.

Ruling: land, amend, or reject. Landed, it goes to the Flow owner to build; Flow sets the title once the flow id is claimed, and sets these names then too.

## Proposal 5: A metaflow may set its own refresh threshold · psyche-context › vision/flow.md

- A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event.
+ A flow is refreshed when its context passes its metaflow's threshold, or its layer's where the metaflow sets none: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event.

```
+------------------+   +------------------+
| a metaflow with  |   | a metaflow with  |
| a threshold of   |   | none of its own, |
| its own, such as |   | such as Psyche   |
| the Illustrator  |   | core Secondary   |
+--------+---------+   +--------+---------+
         |                      |
         | is refreshed at      | is refreshed at
         v                      v
+------------------+   +------------------+
| its own          |   | its layer's      |
| threshold        |   | threshold        |
+------------------+   +------------------+
```

Ruling: land, amend, or reject.

## psyche-context › vision/book.md

## Books

A book is a proposal into context modules, and the whole of it is its crystallization: a line removed shows in red, a line added in green, and a figure in it is a figure proposed for a module.

A book carries the proposals; it shows no verbatim quote, and the records it draws from are not shown.

The records a proposal draws from live in an unrendered reference file, one per book, in a references/ directory beside the books; they are archived with the landing when some or all of the proposal is accepted.

The first edition of a book is mostly questions.

The book is the center of development: it is the evolution of an idea, and the list of unknowns lives in it.

A figure shows how a thing moves, one question per figure, readable in seconds. Its grammar: a box is a thing or a collection; an arrow is a one-way relation carrying a verb, so that box, verb, box reads as a sentence; nearness and enclosure are kinship; top to bottom is order; colour carries a role or is absent. A list in boxes, a tally, or a sentence in a rectangle is not a figure. A diagram in a book's source is ASCII in that grammar, laid out vertically and no wider than 52 characters so a phone shows it; a sketch without arrows is rewritten before it is sent. The published book never shows the ASCII, but a figure drawn from it by a Tertiary or Quaternary subflow that is given the grammar with the sketch, keeps every box, label and arrow, and adds nothing the source does not say; a figure that lost an arrow is returned. A sizable book carries several figures.

Markdown is never shown in a code block: a module written in Markdown is shown as rendered text.

## Pictures

An idea reaches the living as a picture first. A figure shows one thing, where the idea has a shape, and its colours and marks mean the same in every book.

A proposal is drawn as well as written: what it adds, removes and keeps, in one frame.

A proposal that touches a code component shows the code it changes or adds.

Every comment of his redoes the book it is on, unless the comment closes the topic; a book his comment affects is redone as well. A comment that opens a topic of its own gets a book of its own.

## Proposal 6: An exception is a branch · psyche-context › vision/book.md

+ An exception in a figure is its own branch: an arrow from the box it departs from, carrying its condition, to where it goes.
+ Every box in a figure is joined to the figure by an arrow.
+ Boxes and arrows are drawn solid.

Ruling: land, amend, or reject.

## Proposal 7: Ordered books stay in view · psyche-context › vision/book.md

+ The index of open books lists every book the living has ordered, with the flow that holds it, until it is published.

Ruling: land, amend, or reject. Held now: the whole-Flow book with all its Ethos, drafted by Psyche ethos Secondary with 21 proposals, owned by Psyche flow Secondary, not published.

<!-- to-the-living:end -->
