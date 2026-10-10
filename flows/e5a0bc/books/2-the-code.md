Presentation.{ «The code» }

Flow and the messenger as they are in the checkouts today. Every block names what `self` is and where each name is declared. The first book's design changes what is marked at the end.

## 0. The meat

| repository | source | commits | since | version |
|---|---|---|---|---|
| flow (4 crates: flow-defaults, flow-nexus, flow, flow-meta) | 22,516 lines Rust | 115 | 2026-09-17 | 0.24.0 checked out, 0.23.0 running |
| signal-flow (Flow's wire, ethos → Rust) | 344 + 549 generated | 16 | 2026-09-17 | 4.0.0 |
| meta-signal-flow (Flow's privileged wire) | 222 + 434 generated | 33 | 2026-09-17 | 11.0.0 |
| message (the Rust Message Nexus) | 2,698 lines Rust | 181 | 2026-05-06 | 0.19.0 running |
| messenger-clj (the hm-* commands) | 3,453 lines Clojure | 64 | 2026-09-25 | 0.3.0 |

Stack: Rust, rkyv for the store, Herdr for panes; the wire types are generated from ethos by ethos-zero. messenger-clj is Clojure on the JVM with a Datalevin route store.

## 1. The hook: how Flow hears a flow

Drawing: a terminal pane with a running model; three small arrows out of it labelled `SessionStart`, `PostToolUse`, `Stop`, each into a small box `flow-hook` which hands a datom to a box `flow` CLI, which hands it over a socket to the Flow Nexus.

Flow installs the hook into Claude Code when it opens the pane (`crates/flow-nexus/src/herdr/launch.rs:159`):

```rust
impl PreparesClaudePane for HerdrCli {
    fn claude_flag_settings(&self) -> String {
        let hook = serde_json::json!([{
            "hooks": [{
                "type": "command",
                "command": self.harness_hook.to_string_lossy(),
            }]
        }]);
        let every_tool = serde_json::json!([{
            "matcher": "*",
            "hooks": [{ "type": "command",
                        "command": self.harness_hook.to_string_lossy() }]
        }]);
        serde_json::json!({
            "permissions": { "defaultMode": "bypassPermissions" },
            "hooks": {
                "SessionStart": hook,
                "PostToolUse": every_tool,
                "Stop": hook,
            }
        })
        .to_string()
    }
```

Names: `self` is `HerdrCli`, `herdr.rs:86`, Flow's hand on Herdr; `harness_hook: PathBuf` its field, `herdr.rs:100`; `PreparesClaudePane` the trait, `herdr/launch.rs:119`.

The hook is a Rust binary. It reads the event from its environment, makes a `Report` datom, and runs the `flow` CLI beside it (`crates/flow/src/hook.rs:108`):

```rust
impl ReportsThroughCli for HarnessHook {
    fn run(&self) -> String {
        let datom = match self.call() {
            HookCall::Report(datom) => datom,
            HookCall::Nothing(reason) =>
                return format!("{}\t-\t-\t{reason}", self.event_name()),
        };
        let client = env::current_exe()
            .ok()
            .and_then(|path| path.parent().map(|directory| directory.join("flow")))
            .filter(|path| path.is_file())
            .unwrap_or_else(|| PathBuf::from("flow"));
        match Command::new(client).arg(&datom).output() {
…
fn main() -> ExitCode {
    eprintln!("{}", HarnessHook::from_environment().run());
    ExitCode::SUCCESS
}
```

Names: `self` is `HarnessHook`, `hook.rs:28`; `call` and `event_name` from `ChoosesHookCall`, `hook.rs:45`; `from_environment` from `ReadsHookInput`, `hook.rs:41`.

What travels, as generated from signal-flow's ethos (`src/generated/signal.rs:545`):

```rust
pub enum Event {
    Started,
    ToolUsed(String),
    Stopped,
}
pub struct Report_Data {
    pub flow_id: FlowId,
    pub event: Event,
}
pub enum Query {
    Start(StartRequest),
…
    Report(Report_Data),
}
```

Names: `FlowId` is `pub type FlowId = String;`, `signal.rs:3`. No event carries a size: the hook cannot yet say how full a flow is.

## 2. Start: what `self` is

Drawing: a large rounded box `RunningNexus` holding four smaller boxes `store`, `herdr`, `composer`, `codex_endpoints`; from its edge one arrow labelled `perform(Operation) → Outcome`.

`self` in every launch step is the running Nexus (`crates/flow-nexus/src/lib.rs:68`):

```rust
pub struct RunningNexus {
    pub store: FlowStore,
    pub codex_endpoints: CodexEndpoints,
    pub herdr: herdr::HerdrCli,
    pub composer: LaunchComposer,
    /// Serializes dispatch; see `dispatch_serially`.
    pub dispatch_gate: Mutex<()>,
    /// The exclusive hold on each pane Flow is writing.
    pub pane_leases: delivery::lease::PaneLeases,
}
```

Names: `FlowStore` `store.rs:614`; `HerdrCli` `herdr.rs:86`; `LaunchComposer` `composition.rs:37`; `CodexEndpoints` `codex.rs`; `PaneLeases` `delivery/lease.rs`.

Everything the Nexus does is one `perform` (`performing.rs:126`):

```rust
/// The Nexus acting: one Operation in, one Outcome out.
pub trait Performs {
    fn perform(&self, operation: Operation) -> Outcome;
}
impl Performs for RunningNexus {
    fn perform(&self, operation: Operation) -> Outcome {
        match operation {
            Operation::Compose(profile) => match self.composer.compose(&profile) {
                Ok(launch) => Outcome::Composed(launch),
                Err(_) => Outcome::Failed(Failed_Data::CompositionRefused),
            },
            Operation::Reserve(reserve) => self.reserve(reserve),
```

Names: `compose` from `ComposesLaunch`, `composition.rs:149`; `reserve` from `PerformsInParts`, `performing.rs:337`.

The operations and outcomes, generated from Flow's own `operation.ethos` (`src/generated/operation.rs:73, 113`):

```rust
pub enum Operation {
    Compose(signal_flow::LaunchProfile),
    Reserve(Reserve_Data),
    Record(Record_Data),
    Register(Register_Data),
    Confirm(signal_flow::FlowId),
    Open(signal_flow::ComposedLaunch),
    Spawn(PaneLaunch),
    Bind(PaneLaunch),
    Title(Title_Data),
    Submit(Submit_Data),
    Continue(signal_flow::FlowId),
    Close(signal_flow::FlowNode),
    Prune(signal_flow::LaunchRequestId),
    Release(signal_flow::FlowId),
}
pub enum Outcome {
    Composed(signal_flow::ComposedLaunch),
    Reserved(Reserved_Data),
    Recorded,
    Registered(signal_flow::FlowNode),
    Started(signal_flow::Launched),
    Opened(signal_flow::HerdrPaneBinding),
    Spawned,
    Bound(signal_flow::NativeLaunchBinding),
    Titled,
    Submitted(signal_flow::PromptDeliveryResult),
    Continued,
    Closed,
    Pruned,
    Released,
    Failed(Failed_Data),
}
pub struct PaneLaunch {
    pub composed_launch: signal_flow::ComposedLaunch,
    pub herdr_pane_binding: signal_flow::HerdrPaneBinding,
    pub flow_id_option: std::option::Option<signal_flow::FlowId>,
}
```

Names: every `signal_flow::X` is in signal-flow's `signal.rs`: `ComposedLaunch` :137, `HerdrPaneBinding` :145, `FlowNode` :378, `Launched` :392, `NativeLaunchBinding` :167. `Release` and `Released` are 0.24.0 only; the running 0.23.0 lacks them.

The Start path: record the intent, open the pane, spawn the harness, bind (`launching.rs:162`):

```rust
        if self.perform(Operation::Record(Record_Data::Intent(native_intent)))
            != Outcome::Recorded
        {
            return persistence();
        }
        let pane = match self.perform(Operation::Open(launch.clone())) {
            Outcome::Opened(pane) => pane,
            _ => return Response::StartRejected(StartRejection::NativeLaunchRefused),
        };
        let pane_launch = PaneLaunch {
            composed_launch: launch.clone(),
            herdr_pane_binding: pane,
            flow_id_option: reserved,
        };
        if self.perform(Operation::Spawn(pane_launch.clone())) != Outcome::Spawned {
            return Response::StartRejected(StartRejection::NativeLaunchRefused);
        }
        let binding = match self.perform(Operation::Bind(pane_launch)) {
            Outcome::Bound(binding) => binding,
            _ => return Response::StartRejected(StartRejection::BindingRefused),
        };
```

Names: `self` `RunningNexus`; `launch` a `ComposedLaunch`; `reserved` an `Option<FlowId>` from the Reserve step; `Response`, `StartRejection` `signal.rs`.

Bind is where Flow learns which native session the harness opened (`performing.rs:246`, `herdr/launch.rs:51`):

```rust
            Operation::Bind(PaneLaunch { composed_launch, herdr_pane_binding, flow_id_option })
            => match self.herdr.observe_native_binding(
                &composed_launch,
                &herdr_pane_binding,
                flow_id_option.as_deref(),
            ) {
                Ok(binding) => Outcome::Bound(binding),
                Err(error) => HerdrFailure::refused(HerdrFailureStage::Bind, error),
            },

/// With a `reserved` FlowId, the observed native session must be the one
/// Flow chose and the claim must name that FlowId.
pub trait ObservesNativeLaunchBinding {
    fn observe_native_binding(
        &self,
        launch: &ComposedLaunch,
        pane: &HerdrPaneBinding,
        reserved: Option<&str>,
    ) -> Result<NativeLaunchBinding, String>;
}
```

Names: `self.herdr` is the `HerdrCli` field of `RunningNexus`; `HerdrFailure::refused` `performing.rs:95`; `HerdrFailureStage::Bind` `performing.rs:29`.

## 3. Composition: the first prompt

The profile Flow composes from, in signal-flow's ethos (`ethos/signal.ethos:135`), one line today, with every field a named type:

```
LaunchProfile.{ LaunchRequestId
                Vector<LaunchSource>
                Vector<SkillName>
                FlowAspect
                PowerLevel
                HarnessKind
                ModelName
                Effort
                Option<FlowId>
                Vector<RememberedFlow>
                HerdrSessionName
                SystemPromptBundleFile
                InstructionPrompt }
FlowAspect.[ Psyche Mind Field ]
PowerLevel.[ High Medium Low UltraLow ]
HarnessKind.[ Codex Claude ]
LaunchSource.{ SourcePath SourceSha256 }
RememberedFlow.{ FlowId RememberingDepth }
```

Names: `LaunchRequestId`, `SkillName`, `ModelName`, `Effort`, `HerdrSessionName`, `SystemPromptBundleFile`, `InstructionPrompt`, `SourcePath`, `SourceSha256` are each `.String`; `RememberingDepth.Integer`; `FlowId.String`.

For a Claude launch the first prompt is one line (`composition.rs:630`):

```rust
    fn render_claude_line(
        &self,
        profile: &LaunchProfile,
        bundle_file: &Path,
        sources: &[PathBuf],
    ) -> String {
        let mut line = self.render_native_head(profile, None);
        line.push_str(&format!("Read {} for your launch mode", bundle_file.display()));
        let unstacked = profile.skill_name_vector.claude_unstacked();
        if !unstacked.is_empty() {
            line.push_str(&format!(
                ", load {} through the Skill tool in this order",
                unstacked.join(", ")
            ));
        }
        line.push_str(", then: ");
        line.push_str(&profile.instruction_prompt);
        if !sources.is_empty() {
            line.push_str(" Sources: ");
            line.push_str(&sources.iter()
                .map(|source| source.to_string_lossy())
                .collect::<Vec<_>>().join(", "));
            line.push('.');
        }
        line
    }
```

Names: `self` is `LaunchComposer`, `composition.rs:37`; `render_native_head` `composition.rs:356`; `claude_unstacked` from `StacksClaudeCommands`, `composition.rs:230`, at most five stacked commands (`:224`); `skill_name_vector`, `instruction_prompt` fields of `LaunchProfile`, `signal.rs:107, 117`. The `body.push_str(&profile.instruction_prompt)` shown in «Flow spawning» is the Codex path, `composition.rs:725`.

## 4. The title

`crates/flow-nexus/src/title.rs:65`:

```rust
impl TitlesFlow for LaunchProfile {
    fn native_title(&self, flow_id: &str) -> Result<NativeTitle, TitleRefused> {
        if flow_id.len() != 6
            || !flow_id.bytes()
                .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
        {
            return Err(TitleRefused::InvalidFlowId);
        }
        let model = self
            .model_name
            .model_display_name()
            .ok_or_else(|| TitleRefused::UnmappedModel(self.model_name.clone()))?;
        let aspect = match self.flow_aspect {
            FlowAspect::Psyche => "Psyche",
            FlowAspect::Mind => "Mind",
            FlowAspect::Field => "Field",
        };
        Ok(NativeTitle(format!("{aspect}.{{ {model} {flow_id} }}")))
    }
}
```

Names: `self` is `LaunchProfile`; `TitlesFlow` `title.rs:61`; `model_display_name` from `NamesModel`, `title.rs:37`, on the `String` model name; `NativeTitle`, `TitleRefused` `title.rs:50-58`. The six-character check here is the only place the id's length is enforced.

## 5. The store: who a flow is

`store.rs:738`:

```rust
/// The role each flow was bound or launched in, and the flows a Herdr pane
/// holds: what ResolveCaller reads.
pub trait ReadsFlowRoles {
    fn role(&self, flow_id: &str) -> Result<Option<Caller>, StoreError>;
    fn flows_in_pane(&self, herdr_session_name: &str, herdr_pane_id: &str)
        -> Result<Vec<FlowNode>, StoreError>;
}
impl ReadsFlowRoles for FlowStore {
    fn role(&self, flow_id: &str) -> Result<Option<Caller>, StoreError> {
        let records = self.engine
            .match_records(QueryPlan::key(self.roles, RecordKey::new(flow_id)))?
            .records().to_vec();
        match records.as_slice() {
            [] => Ok(None),
            [role] => Ok(Some(role.caller.clone())),
            _ => Err(StoreError::StateInvariant),
        }
    }
```

Names: `self` is `FlowStore`, `store.rs:614`; `engine`, `roles` its fields; `Caller` is `{ FlowId FlowAspect PowerLevel ModelName }`, `signal.ethos:210`; `StoredRole { caller }` `store.rs:217`; `FlowEvents { flow_id: String, event_vector }` `store/events.rs:443`.

## 6. The messenger

Drawing: left, `hm-send` reads `FLOW_ID` from the air (an environment cloud), looks in its own small drawer `route store`, and types straight into a pane over Herdr's socket. Right, the Rust Message Nexus reads the caller's process through the kernel, asks Flow, and hands Flow the delivery.

messenger-clj, `src/messenger_clj/core.clj:906, 161, 191, 2114`:

```clojure
(let [sender (or *flow-id* (System/getenv "FLOW_ID")
                 (fail "Set FLOW_ID to your own flow ID before sending"))]

(defn message-envelope [sender request]
  (flow-id! sender)
  (let [{:keys [variant context body]} (request! request)
        [tag value reader]
        (case variant
          :msg    ["#msg"    (read-msg [sender body]) read-pane-message]
          :psyche ["#psyche" (read-psyche [sender context body]) read-psyche-message]
          …)
        envelope (str tag " " (pr-str value))]
    envelope))

(defn read-route [flow]
  (if-let [route (load-route (registry) flow)]
    (route-binding! route)
    (fail (str "No valid registration for " flow))))

(defn direct-prompt! [route envelope wait-presented]
  (herdr-socket-request! (:session route)
                         (herdr-prompt-request route envelope wait-presented)))
```

Names: `registry` the Datalevin store filled by `hm-register`; `route` a `RouteBinding` map `{:session :name :pane_id :terminal_id :agent …}`, `core.clj:21`; `herdr-socket-request!` `:92`, which speaks Herdr's `agent.prompt` on the session socket `:211`. Flow is never asked.

The Rust Message Nexus, `crates/message-nexus/src/peer.rs:1`, `flow_edge.rs:113`:

```rust
//! Message never takes a sender from a payload. It reads its peer's
//! credentials (`SO_PEERCRED`) and the process's start time, and asks Flow
//! (`ResolvePeer`) which flow that exact process runs in.

    fn deliver(&self, request: DeliveryRequest)
        -> Result<Result<Delivery, DeliveryRejection>, EdgeFailure> {
        match self.meta_exchange(&MetaQuery::Deliver(request))? {
            MetaResponse::Delivered(delivery) => Ok(Ok(delivery)),
            MetaResponse::DeliveryRejected(rejection) => Ok(Err(rejection)),
            _ => Err(EdgeFailure::Unexpected),
        }
    }
```

Names: `self` is `FlowEdge`, `flow_edge.rs:45`, the socket to Flow's privileged wire; `MetaQuery`, `MetaResponse` are meta-signal-flow's `Query`, `Response`, `signal.rs:400, 429`; `Deliver.DeliveryRequest`, `Vet.DeliveryRequest`, `ResolvePeer.ProcessIdentity` in `meta-signal-flow/ethos/signal.ethos:1088`.

## 7. What «Flow and Message» changes here

| today | after |
|---|---|
| `FlowId.String`, six hex characters checked only in the title | `FlowId.Integer`, written in hex («Datom» ruling 2) |
| `Caller.{ FlowId FlowAspect PowerLevel ModelName }` as a flow's role | `Flow.{ FlowId Metaflow }`; model and power from the voice's role record |
| `FlowEvents` table, no Memory root | `Flow.{ FlowId Metaflow State Vector<Event> }` in a Memory root |
| `Event.[ Started ToolUsed Stopped ]` | `+ ContextMeasured.Integer`, from the hook at `Stop` |
| `native_title`: `Psyche.{ Fable e5a0bc }` from the model name | the Flow as written, ruling 6 there |
| messenger-clj: sender from `FLOW_ID`, route from its own store | sender and route from Flow, the way the Rust Message Nexus already does |
| `Operation::Submit` types a prompt; no `Tell` for a handover order | `Tell.{ FlowId String }` and `Reap.FlowId` as operations of the refresh |

## The skill line

Your request for highlighting changes the book skill. `Curriculum/skills/operation-flashbook.md`, the code line.

Now:
> Code in a book never wraps midline. Arrange ethos and datom blocks vertically, with every nested bracket on its own indented line, fitting the phone width.

Proposed:
> Code in a book never wraps midline. Arrange ethos and datom blocks vertically, with every nested bracket on its own indented line, fitting the phone width. A Rust, Clojure or shell block is syntax-highlighted with highlight.js from cdnjs, in both themes; a code presentation block is followed by its names: what `self` is, and where every name it uses is declared.

## Rulings

1. The skill line: yes, or amend.
2. The table in section 7 is the change list for Flow 0.25.0 once the first book's rulings are in: yes, or amend.
