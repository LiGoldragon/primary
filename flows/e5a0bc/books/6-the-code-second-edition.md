<!-- to-the-living:start -->
Presentation.{ «The code», second edition }

Flow and the messenger as they are in the checkouts. Types are read in ethos; Rust appears only where behaviour is. Every Rust block says what `self` is and where each name is declared. Flow 0.24.0 checked out at 5e0b1bf, 0.23.0 running; signal-flow pinned at f95034d; meta-signal-flow at 54eb561; message 0.19.0; messenger-clj 0.3.0.

## 1. The hook: how Flow hears a flow

Drawing: a terminal pane with a running model; three arrows out of it labelled `SessionStart`, `PostToolUse`, `Stop`, each into a small box `flow-hook`, which hands one datom to the `flow` CLI, which hands it over a socket to the Flow Nexus.

What the hook sends, on the ordinary wire:

```
Report.{
  FlowId             ; String today
  Event.[
    Started
    ToolUsed.String
    Stopped ] }      ; no size: the hook
                     ; cannot say how full
```

The hook is a Rust binary; `self` is `HarnessHook`, `crates/flow/src/hook.rs:28`:

```rust
impl ReportsThroughCli
    for HarnessHook {
    fn run(&self) -> String {
        let datom = match self
            .call() {
            HookCall::Report(datom) =>
                datom,
            HookCall::Nothing(
                reason) =>
                return format!(
                "{}\t-\t-\t{reason}",
                self.event_name()),
        };
        let client =
            env::current_exe()
            .ok()
            .and_then(|path| path
                .parent().map(
                |directory| directory
                .join("flow")))
            .filter(|path| path
                .is_file())
            .unwrap_or_else(||
                PathBuf::from(
                "flow"));
        match Command::new(client)
            .arg(&datom).output() {
…
fn main() -> ExitCode {
    eprintln!("{}",
        HarnessHook
        ::from_environment().run());
    ExitCode::SUCCESS
}
```

Names: `call`, `event_name` from `ChoosesHookCall`, `hook.rs:45`; `from_environment` from `ReadsHookInput`, `hook.rs:41`. Flow installs the hook into Claude Code through the settings it passes at launch, `herdr/launch.rs:159`.

## 2. What Flow does: the Operation root

Flow's own ethos, `crates/flow-nexus/ethos/operation.ethos:29-81`, laid out by the rule of «Ethos: inline, layout, expansion»; the text is the file's:

```
Operation
[ signal_flow:[ FlowId … Event ]
  flow_nexus:[ LaunchOutcome
               Replacement ] ]
[ Compose.LaunchProfile
  Reserve.{
    ComposedLaunch
    OriginClue }
  Record.[
    Intent.NativeLaunchIntent
    Binding.NativeLaunchBinding
    …
    Active.FlowId
    Stopped.FlowId
    Replacing.Replacement
    Harness.{ FlowId Event } ]
  Register.{ FlowNode Caller }
  Confirm.FlowId
  Open.ComposedLaunch    ; the pane
  Spawn.PaneLaunch       ; the harness
  Bind.PaneLaunch        ; its session
  Title.{
    ComposedLaunch
    NativeLaunchBinding }
  Submit.{               ; first prompt
    ComposedLaunch
    PromptDeliveryIntent }
  Continue.FlowId
  Close.FlowNode
  Prune.LaunchRequestId
  Release.FlowId ]       ; 0.24.0 only
[ Composed.ComposedLaunch
  Reserved.{
    LaunchAttemptReservation
    Option<FlowId> }
  Recorded
  Registered.FlowNode
  Started.Launched
  Opened.HerdrPaneBinding
  Spawned
  Bound.NativeLaunchBinding
  Titled
  Submitted.PromptDeliveryResult
  Continued
  Closed
  Pruned
  Released
  Failed.[
    CompositionRefused
    StoreRefused
    ConflictingBinding
    Unstarted
    HerdrRefused
    CodexRefused
    BundleRefused
    UnknownFlow
    ClaimRefused ] ]
[ PaneLaunch.{
    ComposedLaunch
    HerdrPaneBinding
    Option<FlowId> } ]
```

The Nexus that performs them; `self` in every launch step is `RunningNexus`, `lib.rs:68`, holding `store`, `herdr`, `composer`, `codex_endpoints`; it is the Nexus by `impl LaunchesFlows for RunningNexus`, `launching.rs:72`. One `perform`, `performing.rs:126`:

```rust
pub trait Performs {
    fn perform(&self,
        operation: Operation)
        -> Outcome;
}
impl Performs for RunningNexus {
    fn perform(&self,
        operation: Operation)
        -> Outcome {
        match operation {
            Operation::Compose(
                profile) => match self
                .composer.compose(
                &profile) {
                Ok(launch) =>
                    Outcome::Composed(
                    launch),
                Err(_) =>
                Outcome::Failed(
                Failed_Data
                ::CompositionRefused),
            },
            Operation::Reserve(
                reserve) => self
                .reserve(reserve),
```

Names: `compose` from `ComposesLaunch`, `composition.rs:149`; `reserve` from `PerformsInParts`, `performing.rs:337`.

## 3. Start: open, spawn, bind

Drawing: a flowchart top to bottom: `Record intent` → `Open` a pane → `Spawn` the harness → `Bind` to the session it reports → `Submit` the first prompt; a dashed branch from Submit labelled `Ambiguous until the receipt is seen`.

`launching.rs:162`, inside `launch_reserved`; `launch` a `ComposedLaunch`, `reserved` the `Option<FlowId>` from Reserve:

```rust
if self.perform(
    Operation::Record(
    Record_Data::Intent(
    native_intent)))
    != Outcome::Recorded
{
    return persistence();
}
let pane = match self.perform(
    Operation::Open(launch.clone())) {
    Outcome::Opened(pane) => pane,
    _ =>
        return Response
        ::StartRejected(
        StartRejection
        ::NativeLaunchRefused),
};
let pane_launch = PaneLaunch {
    composed_launch: launch.clone(),
    herdr_pane_binding: pane,
    flow_id_option: reserved,
};
if self.perform(
    Operation::Spawn(pane_launch
    .clone())) != Outcome::Spawned {
    return Response::StartRejected(
        StartRejection
        ::NativeLaunchRefused);
}
let binding = match self.perform(
    Operation::Bind(pane_launch)) {
    Outcome::Bound(binding) =>
        binding,
    _ =>
        return Response
        ::StartRejected(
        StartRejection
        ::BindingRefused),
};
```

Bind, `performing.rs:246` and `herdr/launch.rs:51`; `self.herdr` is `HerdrCli`, `herdr.rs:86`:

```rust
Operation::Bind(PaneLaunch {
    composed_launch,
    herdr_pane_binding,
    flow_id_option })
=> match self.herdr
    .observe_native_binding(
    &composed_launch,
    &herdr_pane_binding,
    flow_id_option.as_deref(),
) {
    Ok(binding) => Outcome::Bound(
        binding),
    Err(error) =>
        HerdrFailure::refused(
        HerdrFailureStage::Bind,
        error),
},

pub trait ObservesNativeLaunchBinding
    {
    fn observe_native_binding(
        &self,
        launch: &ComposedLaunch,
        pane: &HerdrPaneBinding,
        reserved: Option<&str>,
    ) -> Result<NativeLaunchBinding,
        String>;
}
```

A first turn on Codex is submitted as `PromptDeliveryResult::Ambiguous`, `codex.rs:869`; only a later receipt observation makes it `Observed`. Submit is not first-turn success.

## 4. Who a flow is, and the title

The role today, on the ordinary wire:

```
Caller.{             ; stored per FlowId
  FlowId
  FlowAspect.[ Psyche Mind Field ]
  PowerLevel.[ High Medium Low
               UltraLow ]
  ModelName }        ; String
FlowNode.{
  FlowId
  SessionId
  HarnessKind.[ Codex Claude ]
  EndpointSelection
  HerdrRouteSelection
  OriginClue
  FlowLifecycle.[ Pending Active
                  Stopped Retired
                  Exited ] }
```

`store.rs:738`; `self` is `FlowStore`, `store.rs:614`:

```rust
impl ReadsFlowRoles for FlowStore {
    fn role(&self, flow_id: &str)
        -> Result<Option<Caller>,
        StoreError> {
        let records = self.engine
            .match_records(
                QueryPlan::key(self
                .roles,
                RecordKey::new(
                flow_id)))?
            .records().to_vec();
        match records.as_slice() {
            [] => Ok(None),
            [role] => Ok(
                Some(role.caller
                .clone())),
            _ => Err(
                StoreError
                ::StateInvariant),
        }
    }
```

The title, `title.rs:65`; `self` is `LaunchProfile`; `model_display_name` from `NamesModel`, `title.rs:37`:

```rust
impl TitlesFlow for LaunchProfile {
    fn native_title(&self,
        flow_id: &str)
        -> Result<NativeTitle,
        TitleRefused> {
        if flow_id.len() != 6
            || !flow_id.bytes()
                .all(|byte| byte
                    .is_ascii_digit()
                    || (b'a'..=b'f')
                    .contains(&byte))
        {
            return Err(
                TitleRefused
                ::InvalidFlowId);
        }
        let model = self
            .model_name
            .model_display_name()
            .ok_or_else(||
                TitleRefused
                ::UnmappedModel(self
                .model_name
                .clone()))?;
        let aspect = match self
            .flow_aspect {
            FlowAspect::Psyche =>
                "Psyche",
            FlowAspect::Mind =>
                "Mind",
            FlowAspect::Field =>
                "Field",
        };
        Ok(NativeTitle(
 format!(
 "{aspect}.{{ {model} {flow_id} }}")))
    }
}
```

## 5. Replace

On the ordinary wire:

```
Replace.StartRequest.{
  LaunchProfile      ; names the
  OriginClue }       ; predecessor
Replaced.{
  FlowId             ; stopped
  Launched }         ; the successor
ReplaceRejection.[
  PredecessorAbsent
  UnknownPredecessor
  PredecessorStopped
  LaunchRefused.StartRejection
  ReapRefused.StopRejection ]
```

`reap` records the predecessor `Stopped` before the successor is routable, `launching.rs:488`; no voice is handed over, because no voice exists in the code.

## 6. The messenger

Drawing: left, `hm-send` reads `FLOW_ID` from an environment cloud, opens its own small drawer `route store`, and types straight into a pane over Herdr's socket. Right, the Rust Message Nexus reads the caller's process through the kernel, asks Flow who it is, and hands Flow the delivery.

messenger-clj, `src/messenger_clj/core.clj:191, 2114`; `registry` its Datalevin store, `route` a map of session, pane and terminal:

```clojure
(defn read-route [flow]
  (if-let [route
      (load-route (registry) flow)]
    (route-binding! route)
    (fail (str
        "No valid registration for "
        flow))))

(defn direct-prompt!
    [route envelope wait-presented]
  (herdr-socket-request!
      (:session route)
      (herdr-prompt-request
          route
          envelope
          wait-presented)))
```

The sender is the `FLOW_ID` environment variable, `core.clj:906`. Flow is never asked.

The privileged wire the Rust Message Nexus speaks to Flow, meta-signal-flow `ethos/signal.ethos`:

```
Deliver.DeliveryRequest
Vet.DeliveryRequest
ResolvePeer.ProcessIdentity

DeliveryRequest.{
  DeliveryId
  FlowId             ; the recipient
  Message }
ProcessIdentity.{    ; from the kernel
  ProcessId
  ProcessUserId
  ProcessStartToken }
Letter.{
  MessageId
  Sender
  Content }
Sender.[
  Flow.FlowId        ; by ResolvePeer
  Owner ]
Content.[
  Text.String
  Psyche.{
    PsycheContext
    PsycheVerbatim } ]
DeliveryRejection.[
  UnknownFlow
  FlowStopped
  RouteUnavailable
  RecipientWorking
  RecipientBlocked
  ComposerOccupied
  BodyRefused.BodyRefusal
  NotDelivered
  PersistenceRefused ]
```

`crates/message-nexus/src/flow_edge.rs:113`; `self` is `FlowEdge`, `flow_edge.rs:45`, the socket to Flow:

```rust
fn deliver(&self,
    request: DeliveryRequest)
    -> Result<Result<Delivery,
        DeliveryRejection>,
        EdgeFailure> {
    match self.meta_exchange(
        &MetaQuery::Deliver(
        request))? {
        MetaResponse::Delivered(
            delivery) => Ok(
            Ok(delivery)),
        MetaResponse
            ::DeliveryRejected(
            rejection) => Ok(
            Err(rejection)),
        _ => Err(
            EdgeFailure::Unexpected),
    }
}
```

Names: `MetaQuery`, `MetaResponse` are meta-signal-flow's `Query` and `Response`, `signal.rs:400, 429`.

## 7. What «Flow and Message» changes here

| today | after |
|---|---|
| `FlowId.String`, length checked only in the title | `FlowId.Integer`, written in hex |
| `Caller.{ FlowId FlowAspect PowerLevel ModelName }` | `Flow.{ FlowId Metaflow }`; model and power from the voice's role record |
| events table, no Memory root | `Flow.{ FlowId Metaflow State Vector<Event> }` in a Memory root |
| `Event.[ Started ToolUsed Stopped ]` | `+ ContextMeasured.Integer` at `Stop` |
| title from the model name | the Flow as written, ruling 6 there |
| messenger-clj: sender from `FLOW_ID`, route from its own store | sender and route from Flow, as the Rust Message Nexus already does |
| `Submit` only | `+ Tell.{ FlowId String }` and `Reap.FlowId`, the refresh's operations |

## The agent lines

`subagents/book.md`, the code paragraph.

Proposed:
> A type is shown in ethos, laid out by the new-line style with its comment column, never as generated Rust. A code line is at most 38 characters, rewrapped at the language's own break points, never inside a token or a string; a string that cannot be wrapped is the one line that scrolls in its box. A Rust block says what `self` is and where every name is declared.

`Curriculum/skills/operation-flashbook.md`, two lines.

Now:
> A message is read on a phone: few points, much drawing, short text under each heading.
> Make one fresh artifact for every presentation and every comment, each published from its own new file path, never a path an earlier artifact was published from. Preserve every older artifact, whether it has comments or not.

Proposed:
> A message is read on a phone: much drawing, short text under each heading, every section ending in what it proposes.
> Make one fresh artifact for every presentation; a page with comments is never changed. The book's source is saved in the flow's books folder and published to main by the flow; the agent commits nothing.

## Rulings

1. The book agent's code paragraph: yes, or amend.
2. The two operation-flashbook lines: yes, or amend.
3. Section 7 as the change list for Flow 0.25.0 once «Flow and Message» is ruled: yes, or amend.
<!-- to-the-living:end -->
