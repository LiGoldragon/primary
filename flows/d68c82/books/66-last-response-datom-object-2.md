<!-- to-the-living:start -->
Presentation.{ «The last response as a datom object» }

# The last response as a datom object

## mind-context › knowledge/last-response.md

A flow's last response is the assistant text its harness records at the
end of a turn. It has no type. The book page tooling reads one marked
block inside it. When a turn ends, the Flow Nexus is told only that the
turn stopped.

Verified on 2026-10-17 against Flow `67b80b3` (0.35.11, the version
installed and running), Primary `bda70b5`, and field-context
`compensation/main-flow.md` at `95121c6`.

## How it flows

```
+------------------------------+
| a flow's turn                |
+--------------+---------------+
               |
               | ends in
               v
+------------------------------+
| the last response:           |
| free text, maybe holding     |
| one to-the-living block      |
+------+---------------+-------+
       |               |
       | is scanned    | is not read by
       | by            |
       v               v
+--------------+ +-------------------+
| book-fetch   | | flow-hook: Stop   |
| latestBlock  | | sends only        |
+------+-------+ | Report.Stopped    |
       |         +---------+---------+
       | hands the         |
       | block to          | tells
       v                   v
+--------------+ +-------------------+
| the book     | | the Flow Nexus:   |
| page subflow | | context size,     |
+--------------+ | then sleep or     |
                 | drain the queue   |
                 +-------------------+
```

## The marked block

A presentation meant to become a book sits between two marker lines, and
its first line inside is one datom naming the book (field-context
`compensation/main-flow.md`, line 42):

```markdown
<!-- to-the-living:start -->
Presentation.{ «The last response as a datom object» }

# The last response as a datom object
...
<!-- to-the-living:end -->
```

`Presentation.{ «title» }` is the only datom in it. No ethos type
declares `Presentation`; the title is matched as text. Everything outside
the markers is machine output in prose.

Primary's `tools/book-fetch.mjs` finds the last complete block of the
main thread:

```js
export function latestBlock(records) {
  let latest = null;
  for (const [line, record] of records) {
    if (record.isSidechain || record.type !== "assistant" || !Array.isArray(record.message?.content)) continue;
    for (const block of record.message.content) {
      if (block.type !== "text" || typeof block.text !== "string") continue;
      const start = block.text.lastIndexOf(BLOCK_START);
      if (start < 0) continue;
      const end = block.text.indexOf(BLOCK_END, start);
      if (end < 0) continue;
      latest = { line, text: block.text.slice(start, end + BLOCK_END.length) };
    }
  }
  return latest;
}
```

Usage, from inside the flow whose transcript is read:

```sh
node tools/book-fetch.mjs --block
# stdout: <!-- to-the-living:start --> ... <!-- to-the-living:end -->
```

It reads Claude transcripts only: the session comes from
`CLAUDE_CODE_SESSION_ID` or `--session`, the file from
`~/.claude/projects/<project>/<session>.jsonl`.

## What the Flow Nexus learns at the end of a turn

Flow writes `flow-hook` into every Claude flow it launches. On `Stop` it
reads `hook_event_name` and `FLOW_ID` and sends one datom; it reads
nothing of the response (`crates/flow/src/hook.rs`):

```rust
let event = match self.event_name().as_str() {
    "SessionStart" => "Started".to_owned(),
    "PostToolUse" => match self.input.get("tool_name").and_then(serde_json::Value::as_str) {
        Some(tool_name) => format!("ToolUsed.{}", tool_name.quoted()),
        None => return HookCall::Nothing("PostToolUse without a tool_name"),
    },
    "Stop" => "Stopped".to_owned(),
    _ => return HookCall::Nothing("no Report for this event"),
};
HookCall::Report(format!("Report.{{ {} {event} }}", flow_id.quoted()))
```

```sh
flow 'Report.{ «d68c82» Stopped }'
```

On `Stopped` the Nexus reads the context size from the Claude transcript
(see knowledge-refresh), then types the oldest queued request into the
flow or puts it to sleep (`crates/flow-nexus/src/waking.rs`). No path in
Flow reads, stores or forwards the response text.

## Codex

A Codex rollout records the answer of a completed turn as
`payload.last_agent_message` of its `task_complete` row, and the final
text as a `response_item` with phase `final_answer` (knowledge-codex-rollout).
No Primary tool and no Flow path reads either of them as a response
object.

## field-context › compensation/main-flow.md

Every main flow of every aspect logs the living's vision, intent or notion the moment it is spoken, as the psyche-interraction skill says: verbatim, in its own flow's psyche records, before acting; a question, an order or an acknowledgement is answered or carried out, not logged as psyche. Psyche logging is not the Psyche aspect's alone; a Mind or Field flow that hears the living is a flow that logs psyche.
Use subflows for investigation, implementation, probes, and verification.
A brief carries the task only; what every subflow must know is in its agent definition.
Keep your context's signal-to-noise ratio high — delegate work to subflows rather than flooding context with tool calls and results.
Delegate all task work.
A question from the living about the flow's own conduct, reasons or knowledge is answered in that reply, from the flow's own context, with no subflow and no message to another flow; what the flow does not know it says it does not know.
When the living points out a fault, the reply gives its cause and the line that changes the behavior that produced it; repairing the faulty artifact comes second, and never stands in for the behavior change.
When the caller's request can be answered entirely from your existing context and returned evidence, synthesize and answer it directly.
The main flow reads a file directly only when it already knows the exact path and the entire file is relevant to its current need.
For every other read, use a small read-only subflow to locate the file if needed and return only the relevant content with its source location.
Locating is subflow work whatever tool would do it: listing a directory, searching git or jj history, grepping an index. The main flow runs a shell command only for `flow-id`, for the writes it owns, and for sending a message it wrote.
The main flow synthesizes the subflows' findings. When more information is needed, ask a subflow to obtain it.
Content a subflow already holds, the subflow sends; the main flow sends only what it composed.
Never block on subflows.
Never stop waiting for subflows when the living asks a question.
Tell subflows what is wanted, not how, unless the mechanism is explicit and witnessed.
A flow is liable for its subflows: what a subflow did, the flow did; asked how, it says it did it through a subflow.
Deliver replies to other flows through the messenger. Writing in this transcript does not send them.
{% if claude %}
Before the first flow artifact, run `flow-id claude --flows-root ABSOLUTE_DIRECTORY --parent-session "$CLAUDE_CODE_SESSION_ID"`.
{% endif %}
{% if codex %}
Before the first flow artifact, run `flow-id codex --flows-root` with the explicit absolute flows root.
{% endif %}
Use its normalized hexadecimal alias as the canonical short `FLOW_ID` and its claimed lane as `FLOW_DIRECTORY` for the whole flow tree.
A main flow's canonical title is a Datom struct: `{ <Aspect> <Topic> <Layer> <FLOW_ID> }`, for example `{ Psyche core Primary 6f51ad }`. The layer selects the configured model; `vision-model-roles` defines that correspondence, so use the layer in the title, never the model.
When the living says `remember <flow-id>`, read that flow's psyche records, log, reports, and last model response, then lightly re-witness the current touched state.
Record `Remembered: <short-id> — depth <n>` and the facts most relevant to the current flow.
Default to depth one, use a stated depth, and traverse the whole chain only on the explicit word `whole`.
The main flow creates the flow directory and its index entry.
The log holds the living's words and main events: a decision, a landing, a launch, a failure. Everything else is in the transcript.
Use `compensation-flow-evidence` only for a main-flow-delegated artifact or one a named tool or flow will consume.
Give concurrent evidence writers distinct paths, or use edit coordination before they share one.
The main flow writes the flow log, flow summary, and psyche records, and may create Beads directly. Delegate research needed to formulate them. Leave closure of delegated work to the responsible subflow. No other skill, and no caller instruction or ruling, expands these permissions; work they imply outside them is dispatched, never done.
Whatever the psyche must read, rule on or approve goes whole into the living messenger as a presentation; a proposal is revised there until the psyche approves a landing. Chat is unread.
A presentation meant to become a book, or to change one, sits between `<!-- to-the-living:start -->` and `<!-- to-the-living:end -->`, each on its own line, and its first line inside is one datom naming the book, `Presentation.{ «title» }`; a quoted marker stays inline. Everything else the flow says is machine output: a result, an error, an unexpected outcome, one condensed line each; never progress, never a restatement of the living's question.
The presentation block becomes a message in the living messenger in the same turn it is written.
Never access or search the web directly. Delegate authorized web research.

## Flow summary

When asked to summarize the flow, the main flow writes `summary.md`
in `FLOW_DIRECTORY`. Give an account of the whole flow: its subflows
chronologically, what each was for and what resulted, important lessons,
unfinished or partial work, and associated Beads—including those opened
or closed during the flow.

When work the living ordered waits on another metaflow, the flow tells the living what it waits on in the same turn, and starts the work by another route.
Every location a book's proposal names is checked against the files before the book is published.
A main flow keeps every open order of the living in one list in its flow directory, read at the start of every turn and after every compaction; an order leaves the list only when done or withdrawn.

Every comment of the living on a book, unless it closes the topic, gets a new edition of that book with the comment applied; every other book the comment affects gets a new edition too.

## Proposal 1: psyche-context › vision/flow.md


+ ## The last response is a datom object
+ A flow's last response is a datom object.
+ Its variant comes first and decides its structure, and that structure may hold further objects, each with its own variant.
+ For example:

```ethos
+ Library.{
+ []
+ [ Title.String
+   Body.String
+   Cause.String
+   Unblock.String
+   Page.{ Title Body }
+   Block.{ Cause Unblock }
+   Kind.[ Presentation Answer Blocker Responses ]
+   Response.[ Presentation.Page
+              Answer.Body
+              Blocker.Block
+              Responses.⟦ Response ⟧ ] ]
+ [ Spelled.[ spelling.[ String ] ]
+   Kinded.[ kind.[ Kind ] ]
+   Presentable.[ presentation.[ String ] ] ]
+ [ Title.[ Spelled ]
+   Body.[ Spelled ]
+   Cause.[ Spelled ]
+   Unblock.[ Spelled ]
+   Kind.[ Spelled ]
+   Page.[ Presentable ]
+   Block.[ Presentable ]
+   Response.[ Kinded Presentable ] ] }
```

```datom
+ Presentation.{ «Refreshing the Illustrator»
+                «One flow does every job.» }
+
+ Answer.«Nine proposals written, none landed.»
+
+ Blocker.{ «No layer has a threshold»
+           «A ruling on the two numbers» }
+
+ Responses.[ Answer.«Modules landed.»
+             Blocker.{ «Fable is asleep»
+                       «Your word to wake it» } ]
```

Ruling: land, amend, or reject.

## Proposal 2: psyche-context › vision/book.md


+ ## Each kind of object has its presentation
+ Each kind of datom object has its own presentation in the user interface.
+ The user interface shows an object in its kind's presentation, and no thinking machine renders a page for it.

Ruling: land, amend, or reject.

## mind-context › knowledge/refresh.md

Two mechanisms carry a context threshold today. The Flow Nexus has two
numbers per layer and reads one of them, only when it wakes a sleeping
metaflow. Primary has a Stop-hook program with a warning size that no
installed hook calls. No flow is refreshed while it is awake.

Verified on 2026-10-17 against Flow `67b80b3` (0.35.11, installed and
running), meta-signal-flow `a918b7d` (the revision Flow pins), Primary
`bda70b5`, and the running Nexus's `Configuration` reply.

## How it flows

```
+----------------------------+
| a Claude flow's turn       |
+-------------+--------------+
              |
              | ends: Report.Stopped
              v
+----------------------------+
| the Flow Nexus             |
+-------------+--------------+
              |
              | reads the last usage of
              v
+----------------------------+
| the transcript: input +    |
| cache read + cache write   |
+-------------+--------------+
              |
              | records it as
              v
+----------------------------+
| Record.Context, per flow   |
+-------------+--------------+
              |
              | nothing queued:
              | the flow sleeps
              v
+----------------------------+
| asleep metaflow            |
+------+--------------+------+
       |              |
       | a request    | Refresh.Address
       | wakes it     | marks it
       v              v
+----------------------------+
| wake plan                  |
+------+--------------+------+
       |              |
       | size under   | size at or over
       | Refresh, or  | Refresh, or
       | unknown      | marked, or Codex
       v              v
+------------+  +------------------+
| resume the |  | fresh launch     |
| session    |  | from the last    |
+------------+  | launch's modules |
                +------------------+
```

## The two numbers per layer

The meta wire declares them in meta-signal-flow `ethos/signal.ethos`
(`ConfigureThreshold` and `ConfigurationChange` are in it), quoted
whole at `a918b7d`, the revision Flow `67b80b3` pins:

```ethos
; Flow privileged Signal.
;
; Flow is the only pane writer. Deliver and Command are the only ways
; anything is typed into a flow's pane, and both run under Flow's own
; per-pane lease: an exclusive hold over the whole key sequence, never
; handed out on the wire.
;
; Deliver carries a typed Message addressed by FlowId; Flow renders it,
; so the pane text always begins with its Priority head (HardAbrupt.,
; MiddleAbrupt. or Soft.). A Letter names its MessageId first: the id the
; sender's Message Nexus minted, carried through untouched so the
; recipient reading the pane can Acknowledge it. Flow never interprets it. The Content may hold no control character but
; LF and TAB (ControlCharacter carries the byte offset in the rendered
; pane text), and a first line that is a harness command (a sigil of the
; recipient's HarnessProfile, then a command word) is refused as
; HarnessCommand: harness commands go through Command. Vet answers what
; Deliver would refuse and types nothing. Deliver is idempotent on its
; DeliveryId: a repeat answers the stored Delivery and types nothing. A
; delivery a crash left under the lease settles Uncertain and is never
; retried.
;
; Soft needs the recipient Idle or Done; every tier refuses a Blocked
; recipient and a composer that already holds text. Transported means
; Herdr accepted the text for the exact binding; Presented means the
; recipient was seen reacting on the exact pane. InterruptWitness says
; whether a HardAbrupt interrupt was seen to leave Working.
;
; Every query on this socket answers MetaRefused unless the peer is the
; configured Message Nexus executable, a process in no flow's pane (the
; owner), or a flow whose aspect is in MetaAspects.
;
; MessageNexusBinary is the executable identity used by Bind as Message on
; the ordinary socket. A payload PID does not establish that identity.
;
; ResolvePeer names the flow a process runs in, as ResolveCaller does for
; an ordinary connection's own peer.
;
; ReadEvents answers the harness events Flow holds in its Memory for one
; flow, in the order its Reports were recorded: EventsRead, or
; ReadEventsRejected.UnknownFlow for a FlowId Flow does not hold.
;
; Configure declares one configuration family whole: Models, Thresholds,
; LeaveOuts or Nexus. The declared value replaces that family's committed
; value in one atomic commit, so the family's effective value is always its
; last declaration; an entry absent from the declaration is removed. It
; answers Configured.Replaced, or Configured.Unchanged when the committed
; value already equals the declaration and nothing is written. Each family
; holds one entry per key: Models and Thresholds one per Layer, LeaveOuts
; one per Address (the default leave-outs of one metaflow, which a Start
; naming its own replaces). ConfigureRejected changes nothing:
; DuplicateEntry when a declaration names one key twice, CodexModelsOverlap
; when a Nexus names one model under both Codex endpoints. Configuration
; reads the committed Nexus and the committed model, threshold and leave-out
; vectors; it never returns defaults, and answers Unconfigured while no
; Nexus has been declared. A seat's context is named by its launch, never
; configured here.
; Configure.Nexus names the actual Message executable in MessageNexusBinary.
; Lease is the lock duration in seconds; a fresh, unconfigured default is 60.
; A running Nexus reads its Codex endpoints when it opens, so a replaced
; endpoint is served from the next start.

; Refresh names one metaflow whose next wake starts a fresh native session,
; composed from the module identities and leave-outs its last launch
; recorded, instead of resuming the last flow's session. It marks that one
; metaflow only; no model or threshold changes, and the mark clears when
; the metaflow is recorded Awoken. It answers Refreshed with the Address,
; and a second Refresh while the metaflow is marked answers the same.
; RefreshRejected: Unknown (no metaflow at the Address), Awake, Ended,
; NoLaunchProfile (its last flow has no recorded launch profile to compose
; from), StoreRefused. Only an Asleep metaflow is accepted.

; MetaBindExisting verifies each binding against Herdr before it is stored:
; PaneAbsent (the container's Herdr session shows no agent of the binding's
; harness at its workspace, pane and terminal), ProcessMismatch (the pane's
; foreground processes do not include the binding's process), SessionMismatch
; (Herdr reports another native session for the pane), SessionUnreported (a
; Claude pane reports no native session), SessionUnproven (a Codex pane
; reports none and no rollout whose session_meta names the session exists),
; HerdrUnreadable (the session's snapshot or the pane's processes could not
; be read).

Signal
[ signal_flow:[ FlowNode FlowId Aspect PowerLevel ModelName HarnessKind NativeSessionId HerdrSessionName HerdrAgentName HerdrWorkspaceId HerdrPaneId HerdrTerminalId Caller CallerResolutionRejection Event LeaveOuts ]
  flow_ethos:[ OrdinarySocketPath MetaSocketPath SourceRoot ClientPath Home ControlSocketPath CodexEndpoint StableCodex NextCodex KeyName CommandSigil InterruptKeys SubmitKeys HarnessProfile HarnessProfiles MetaAspects MessageNexusPath MessageNexusBinary Lease Subaspect Topic Layer Address ] ]
[ Configuration
  Configure.ConfigurationChange
  ConsumeReset.ResetRequest
  RegisterFlow.FlowNode
  MetaBindExisting.MetaBindExisting
  Retire.FlowId
  Deliver.DeliveryRequest
  Vet.DeliveryRequest
  Command.CommandRequest
  ResolvePeer.ProcessIdentity
  ReadEvents.FlowId
  Refresh.Address ]
[ Configured.ConfigureOutcome
  Configuration.ConfigurationSnapshot
  Unconfigured
  ResetConsumed.ResetOutcome
  FlowRegistered.FlowNode
  ConfigureRejected.ConfigureRejection
  ResetRejected.ResetRejection
  FlowRegistrationRejected.FlowRegistrationRejection
  BoundExisting.BoundExisting
  BindExistingRejected.BindExistingRejection
  FlowRetired.FlowNode
  RetireRejected.RetireRejection
  Delivered.Delivery
  DeliveryRejected.DeliveryRejection
  Vetted.FlowId
  Commanded.CommandOutcome
  CommandRejected.CommandRejection
  PeerResolved.Caller
  PeerResolutionRejected.CallerResolutionRejection
  MetaRefused.MetaRefusal
  Refused.Refusal
  EventsRead.{ FlowId Vector<Event> }
  ReadEventsRejected.[ UnknownFlow StoreRefused ]
  Refreshed.Address
  RefreshRejected.RefreshRejection ]
[ ; Flow Library owns the shared configuration field types.
  ; This record exists only for Flow's current internal launch defaults.
  ; The process sockets are separately supplied by Library.Start; this
  ; record is not a Configure wire payload.
  NexusRuntimeSettings.{ OrdinarySocketPath MetaSocketPath SourceRoot StableCodex NextCodex Vector<HarnessProfile> MetaAspects MessageNexusPath MessageNexusBinary Lease }
  ConfigureModel.{ Layer Native.String }
  ConfigureThreshold.{ Layer Handover.Integer Refresh.Integer }
  ; The leave-outs a metaflow's Start takes when it names none.
  ConfigureLeaveOut.{ Address LeaveOuts }
  ConfigureNexus.{ SourceRoot StableCodex NextCodex HarnessProfiles MetaAspects MessageNexusPath MessageNexusBinary Lease }
  ; Keep the payload type distinct from the unit Query.Configuration variant.
  ConfigurationChange.[ Models.Vector<ConfigureModel>
                         Thresholds.Vector<ConfigureThreshold>
                         LeaveOuts.Vector<ConfigureLeaveOut>
                         Nexus.ConfigureNexus ]
  ConfigureOutcome.[ Replaced Unchanged ]
  ConfigurationSnapshot.{ Nexus.ConfigureNexus Models.Vector<ConfigureModel> Thresholds.Vector<ConfigureThreshold> DefaultLeaveOuts.Vector<ConfigureLeaveOut> }
  IdempotencyKey.String
  CreditId.String
  CreditSelection.[ Next
                    Specific.CreditId ]
  ResetRequest.{ IdempotencyKey CreditSelection }
  ResetOutcome.[ Reset NothingToReset NoCredit AlreadyRedeemed ]
  ConfigureRejection.[ StoreRefused DuplicateEntry CodexModelsOverlap ]
  RefreshRejection.[ Unknown Awake Ended NoLaunchProfile StoreRefused ]
  ResetRejection.[ AdapterUnavailable ProtocolRefused ]
  FlowRegistrationRejection.[ StoreRefused UnknownOrUnclaimedIdentity ConflictingBinding ]
  ProcessId.Integer
  ProcessUserId.Integer
  ProcessStartToken.String
  ProcessIdentity.{ ProcessId ProcessUserId ProcessStartToken }
  HerdrServerSocketPath.String
  HerdrServerProcessIdentity.ProcessIdentity
  MetaFlowOwnerId.FlowId
  HerdrTabId.String
  WorkingDirectory.String
  FlowLifecycle.[ RegisteredUnconfirmed ]
  FlowContainer.{ HerdrSessionName HerdrServerSocketPath HerdrServerProcessIdentity MetaFlowOwnerId }
  FlowBinding.{ FlowId Aspect PowerLevel ModelName HarnessKind NativeSessionId HerdrWorkspaceId HerdrPaneId HerdrTabId HerdrTerminalId HerdrAgentName ProcessIdentity WorkingDirectory }
  MetaBindExisting.{ FlowContainer Vector<FlowBinding> }
  BoundFlowBinding.{ FlowId FlowLifecycle }
  FlowBindingRefusalReason.[ AmbiguousPane DeadProcess DuplicateFlowId AnatomyMismatch PaneAbsent ProcessMismatch SessionMismatch SessionUnreported SessionUnproven HerdrUnreadable ]
  RefusedFlowBinding.{ FlowId FlowBindingRefusalReason }
  FlowBindingResult.[ Bound.BoundFlowBinding
                      Refused.RefusedFlowBinding ]
  BoundExisting.{ FlowContainer Vector<FlowBindingResult> }
  BindExistingRejection.[ ContainerUnavailable ContainerIdentityMismatch StoreRefused ]
  RetireRejection.[ UnknownFlow AlreadyGone StoreRefused ]
  DeliveryId.String
  MessageId.String
  CommandLine.String
  ByteOffset.Integer
  Sender.[ Flow.FlowId
           Owner ]
  PsycheContext.String
  PsycheVerbatim.String
  Content.[ Text.String
            Psyche.{ PsycheContext PsycheVerbatim } ]
  Letter.{ MessageId Sender Content }
  Message.[ HardAbrupt.Letter
            MiddleAbrupt.Letter
            Soft.Letter ]
  DeliveryRequest.{ DeliveryId FlowId Message }
  InterruptWitness.[ NotRequested Observed Unobserved ]
  DeliveryGrade.[ Transported Presented Uncertain ]
  Delivery.{ DeliveryId FlowId InterruptWitness DeliveryGrade }
  BodyRefusal.[ EmptyBody
                HarnessCommand.CommandLine
                ControlCharacter.ByteOffset ]
  DeliveryRejection.[ UnknownFlow
                      FlowStopped
                      RouteUnavailable
                      RecipientWorking
                      RecipientBlocked
                      ComposerOccupied
                      BodyRefused.BodyRefusal
                      NotDelivered
                      PersistenceRefused
                      FlowRetired
                      FlowExited ]
  HarnessCommand.[ Compact Interrupt ]
  CommandRequest.{ FlowId HarnessCommand }
  CommandGrade.[ Transported Observed Uncertain ]
  CommandOutcome.{ FlowId HarnessCommand CommandGrade }
  CommandRejection.[ UnknownFlow FlowStopped RouteUnavailable RecipientBlocked UnsupportedForHarness NotDelivered FlowRetired FlowExited ]
  MetaRefusal.[ PeerUnknown
                PeerNotAuthorized.Caller ]
  Refusal.[ Store.String ]
  ]
```

```sh
flow-meta 'Configure.Thresholds.[ { Secondary 128000 200000 } ]'
# -> Configured.Replaced
flow-meta 'Configuration'
# -> Configuration.{ { … } [ { Primary claude-fable-5-1 } … ] [] [ … ] }
```

The running Nexus answered `Configuration` on 2026-10-17 with an empty
threshold vector, the third position: no layer has a number.
`Handover` is stored and read nowhere in Flow. `Refresh` is read by
`refresh_threshold` and used only by the wake plan.

## Measuring

Only Claude flows are measured, once, when the Stop report arrives
(`crates/flow-nexus/src/claude.rs`): the last main-thread usage entry of
the transcript, its input, cache-read and cache-write tokens added.

```rust
let usage = entry.get("message")?.get("usage")?;
let tokens = |key: &str| usage.get(key).and_then(Value::as_i64).unwrap_or(0);
usage.get("input_tokens")?;
Some(tokens("input_tokens") + tokens("cache_read_input_tokens") + tokens("cache_creation_input_tokens"))
```

`record_context_at_stop` returns at once for a Codex flow, so a Codex
flow has no recorded size.

## Resume or fresh

`crates/flow-nexus/src/waking.rs`:

```rust
fn resumes(context_tokens: Option<i64>, refresh_threshold: Option<i64>) -> bool {
    match (context_tokens, refresh_threshold) {
        (Some(tokens), Some(threshold)) => tokens < threshold,
        _ => true,
    }
}
```

The wake plan resumes only a Claude flow that can be resumed, is not
marked fresh, and `resumes`; otherwise it launches fresh from the module
identities and leave-outs of the metaflow's last launch. With no
threshold configured, every resumable Claude flow resumes.

`Refresh.Address` marks one asleep metaflow so its next wake is fresh:

```sh
flow-meta 'Refresh.{ Psyche core Secondary }'
# -> Refreshed.{ Psyche core Secondary }
# or RefreshRejected.[ Unknown Awake Ended NoLaunchProfile StoreRefused ]
```

An awake metaflow is refused. Nothing tells a flow it is near a
threshold, and nothing asks it for a handover.

## Primary's Stop-hook program

`tools/context-refresh-hook.mjs` reads one native Stop JSON object,
measures the session through `tools/field-census`, and compares it with
`config/context-refresh.json`:

```json
{ "version": 1, "warningWindowFraction": 0.5,
  "claude": { "warningTokens": 200000 },
  "codex": { "models": { "gpt-6.1-sol": 373000, "gpt-6-astra": 272000,
                         "gpt-6-sol": 272000, "gpt-6-luna": 272000 } },
  "recipients": { "field": "Field Core Secondary" } }
```

A Claude session warns at 200,000 tokens; a Codex session at half its
model's window. Over it, the program sends a `ContextRefreshHandover`
JSON body by `hm-send` to Field Core Secondary and to the session's own
flow, once per session, and only for a session listed in the file's
`bindings` (one Psyche Core Primary session today).

```sh
echo '{"session_id":"…","transcript_path":"…"}' | node tools/context-refresh-hook.mjs
```

No Claude settings file in `~/.claude` or Primary's `.claude`, and no
file in CriomOS-home, names it, and its state directory does not exist:
it has not run as a hook.

## The compensation that stands in

field-context `compensation/launch.md`, lines 24 to 28: a flow at or
above its layer's configured refresh threshold receives no further work;
a Fable flow stops receiving work at 15% of its observed window or
100,000 tokens; its secretary has its successor started and the
successor takes its topics from the handover (knowledge-handover).

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

## Proposal 3: psyche-context › vision/flow.md


- Every harness event reaches Flow through the harness's hooks calling the Flow CLI, so Flow knows each flow's state without polling; a marked block landing in a transcript becomes an action, a book among them, with no tool call by the flow; a flow nearing its context limit is told, writes its handover, and is refreshed as it goes idle.
+ Every harness event reaches Flow through the harness's hooks calling the Flow CLI, so Flow knows each flow's state without polling; a marked block landing in a transcript becomes an action, a book among them, with no tool call by the flow; a flow nearing its context limit is told and is refreshed as it goes idle.
- A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event.
+ A flow is refreshed at its layer's two thresholds: at the first it is told, and at the second it is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event.
- Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.

Ruling: land, amend, or reject.

## mind-context › knowledge/handover.md

A handover today is a Markdown file a flow writes by its own judgment,
`flows/<flow-id>/handover.md` in Primary. Nothing types it, nothing
generates it, and the Flow Nexus neither asks for one nor delivers one.
A successor started by Primary's native launcher receives text in the
`{{handover}}` slot of its first prompt; a successor woken fresh by the
Flow Nexus receives its modules and the queued requests.

Verified on 2026-10-17 against Primary `bda70b5`, Flow `67b80b3`
(0.35.11), meta-signal-flow `a918b7d` and field-context `95121c6`.

## How it flows

```
+-----------------------------+
| a flow near its limit       |
+--------------+--------------+
               |
               | writes by judgment
               v
+-----------------------------+
| flows/<id>/handover.md      |
| free Markdown               |
+--------------+--------------+
               |
               | is read by
               v
+-----------------------------+
| the secretary, or the       |
| successor itself            |
+--------------+--------------+
               |
               | starts through
               v
+-----------------------------+
| the native launcher         |
+-------+-------------+-------+
        |             |
        | fills       | writes
        v             v
+-------------+ +-------------------+
| first       | | continuation.json |
| prompt:     | | flowId,           |
| {{handover}}| | predecessor,      |
+-------------+ | topic, metaflow   |
                +-------------------+

+-----------------------------+
| the Flow Nexus fresh wake   |
+--------------+--------------+
               |
               | hands the new flow
               v
+-----------------------------+
| modules of the last launch  |
| and the queued requests;    |
| no handover                 |
+-----------------------------+
```

## The file

Primary holds 33 `flows/*/handover.md` files on 2026-10-17. Their
sections are chosen by each writer and differ from file to file: among
them the seat, open decisions waiting on the living, judgments to carry,
next bounded work and references. No ethos type and no checker covers
them.

## The first prompt

`config/main-flow/shared.edn` holds the template; `{{handover}}`,
`{{modules}}` and `{{raw-psyche}}` must be present, and
`tools/main-flow-mode/launch-config.mjs` refuses an empty handover:

```clojure
{:first-prompt-template "{{modules}}\n\n# Handover and topic context\n{{handover}}\n\n# Raw psyche records with context\n{{raw-psyche}}\n\n{{topic-context}}\n\n…"}
```

```js
if (!handover?.trim()) throw new Error('first prompt handover or topic context is required');
const values = {modules, handover, 'raw-psyche': sources.join('\n'), 'topic-context': metaflow['topic-context'] ?? '', metaflow: `${metaflow.aspect} ${metaflow.topic} ${metaflow.layer}`};
```

`tools/claude-native-seat-refresh.py` fills the slot from its manifest:
the role, topic, model, effort and predecessor as JSON, then each listed
source file's body.

```python
def role_brief(manifest, sources, effort_observed=True):
    metadata = {key: manifest.get(key) for key in ("role", "topic", "model", "effort", "predecessor")}
    return json.dumps(metadata, ensure_ascii=False) + "\n\n" + "\n\n".join(
        f"## Source: `{item['path']}`\n\n{item['body']}" for item in sources
    )
```

The lineage is written apart, by `tools/native-main-flow-launch-shared.mjs`:

```json
{"flowId":"d68c82","predecessor":null,"topic":"Core","metaflow":"Psyche core Secondary: successor of 445410"}
```

## In the Flow Nexus

`hand_over` in `crates/flow-nexus/src/waking.rs` types queued work into a
live pane; it carries no handover. A fresh wake composes the last
launch's system and user modules again and hands over the queue. The
`Handover` number of `ConfigureThreshold` is read nowhere
(knowledge-refresh).

## The request for a handover

The only program that asks for a handover is
`tools/context-refresh-hook.mjs`, which has not run (knowledge-refresh).
Its body, sent as JSON:

```js
{ kind: 'ContextRefreshHandover',
  instruction: 'The refresh procedure has started. … Write a judgment-only handover of decisions and unresolved reasons, name the context topics to split to existing or new topic flows, and include no facts that tools can look up. …',
  observedTokens, thresholdTokens, measurementQuality, action: 'refresh-started',
  decisions: [], unresolvedReasons: […], contextSplit: {…}, windowTokens }
```

## The compensation that stands in

field-context `compensation/launch.md`, lines 24 to 28: the secretary of
a flow at its threshold orders its successor started at once; the
successor takes its topics from the handover; the predecessor is retired
only after the successor has answered on a supported route.

## Proposal 4: psyche-context › vision/flow.md


+ ## A handover is made from objects
+ A successor's handover is found among its predecessor's datom objects, or generated from them: the last object of a kind, or every object of a kind.
+ What is looked for, and whether what is found becomes the handover or generates it, depends on the kinds of objects, on the flow's aspect, and on whether the flow had direct input from the living.
+ For example:

```ethos
+ Library.{
+ [ response:[ Response Kind
+              Spelled Kinded Presentable ] ]
+ [ Aspect.[ Psyche Mind Field ]
+   Living.Boolean
+   Search.[ Last.Kind Every.Kind ]
+   Searches.⟦ Search ⟧
+   Found.⟦ Response ⟧
+   Handover.{ Aspect Living Searches Found } ]
+ [ Counted.[ count.[ Integer ] ] ]
+ [ Aspect.[ Spelled ]
+   Living.[ Spelled ]
+   Search.[ Kinded ]
+   Searches.[ Counted ]
+   Found.[ Counted ]
+   Handover.[ Presentable ] ] }
```

```datom
+ ; a Psyche flow the living spoke to
+ { Psyche
+   True
+   [ Last.Presentation Every.Blocker ]
+   [ Presentation.{ «Refreshing the Illustrator»
+                    «One flow does every job.» }
+     Blocker.{ «Fable is asleep»
+               «Your word to wake it» } ] }
+
+ ; a Mind flow he did not speak to
+ { Mind
+   False
+   [ Last.Answer ]
+   [ Answer.«Modules landed.» ] }
```

Ruling: land, amend, or reject.

## Proposal 5: psyche-context › vision/flow.md


+ A handover carries judgment, never what a tool can look up in one call.

Ruling: land, amend, or reject.

## Proposal 6: psyche-context › vision/flow.md


+ For now, a small model judges which objects make a flow's handover, as one judges whether to wake a topic.

Ruling: land, amend, or reject; one of this, Proposal 7 or Proposal 8.

## Proposal 7: psyche-context › vision/flow.md


+ For now, a flow judges which of its own objects make its handover, when it is told at its layer's first threshold.

Ruling: land, amend, or reject; one of this, Proposal 6 or Proposal 8.

## Proposal 8: psyche-context › vision/flow.md


+ For now, the Field Quaternary flow that checks the questions and requests a flow ends with also judges which of the flow's objects make its handover.

Ruling: land, amend, or reject; one of this, Proposal 6 or Proposal 7.

## Proposal 9: psyche-context › vision/flow.md


+ ## Where the living types
+ For now, the living reaches flows through the harnesses themselves.
+ Once the user interface is ours, the system knows where the living types.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
