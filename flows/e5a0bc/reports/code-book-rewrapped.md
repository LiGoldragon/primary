Presentation.{ «The code», rewrapped blocks }

Every code block of «The code» (`2-the-code.md`) rewrapped to at most 38 columns, in book order, each under its heading line; then two blocks from the canonical Flow checkout (revision 5e0b1bf).

### Block 1

Flow installs the hook into Claude Code when it opens the pane (`crates/flow-nexus/src/herdr/launch.rs:159`):

```rust
impl PreparesClaudePane for HerdrCli {
    fn claude_flag_settings(&self)
        -> String {
        let hook = serde_json::json!(
            [{
            "hooks": [{
                "type": "command",
                "command": self
                .harness_hook
                .to_string_lossy(),
            }]
        }]);
        let every_tool =
            serde_json::json!([{
            "matcher": "*",
            "hooks": [{
                "type": "command",
                "command": self
                    .harness_hook
                    .to_string_lossy()
                    }]
        }]);
        serde_json::json!({
            "permissions": {
                "defaultMode":
                "bypassPermissions" },
            "hooks": {
                "SessionStart": hook,
                "PostToolUse":
                    every_tool,
                "Stop": hook,
            }
        })
        .to_string()
    }
```

### Block 2

The hook is a Rust binary. It reads the event from its environment, makes a `Report` datom, and runs the `flow` CLI beside it (`crates/flow/src/hook.rs:108`):

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

### Block 3

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

### Block 4

`self` in every launch step is the running Nexus (`crates/flow-nexus/src/lib.rs:68`):

```rust
pub struct RunningNexus {
    pub store: FlowStore,
    pub codex_endpoints:
        CodexEndpoints,
    pub herdr: herdr::HerdrCli,
    pub composer: LaunchComposer,
    /// Serializes dispatch; see
    /// `dispatch_serially`.
    pub dispatch_gate: Mutex<()>,
    /// The exclusive hold on each
    /// pane Flow is writing.
    pub pane_leases:
        delivery::lease::PaneLeases,
}
```

### Block 5

Everything the Nexus does is one `perform` (`performing.rs:126`):

```rust
/// The Nexus acting: one Operation
/// in, one Outcome out.
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

### Block 6

The operations and outcomes, generated from Flow's own `operation.ethos` (`src/generated/operation.rs:73, 113`):

```rust
pub enum Operation {
    Compose(
        signal_flow::LaunchProfile),
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
    Prune(
        signal_flow::LaunchRequestId),
    Release(signal_flow::FlowId),
}
pub enum Outcome {
    Composed(
        signal_flow::ComposedLaunch),
    Reserved(Reserved_Data),
    Recorded,
    Registered(signal_flow::FlowNode),
    Started(signal_flow::Launched),
    Opened(
        signal_flow
        ::HerdrPaneBinding),
    Spawned,
    Bound(
        signal_flow
        ::NativeLaunchBinding),
    Titled,
    Submitted(
        signal_flow
        ::PromptDeliveryResult),
    Continued,
    Closed,
    Pruned,
    Released,
    Failed(Failed_Data),
}
pub struct PaneLaunch {
    pub composed_launch:
        signal_flow::ComposedLaunch,
    pub herdr_pane_binding:
        signal_flow::HerdrPaneBinding,
    pub flow_id_option:
        std::option
        ::Option<signal_flow::FlowId>,
}
```

### Block 7

The Start path: record the intent, open the pane, spawn the harness, bind (`launching.rs:162`):

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

### Block 8

Bind is where Flow learns which native session the harness opened (`performing.rs:246`, `herdr/launch.rs:51`):

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

/// With a `reserved` FlowId, the
/// observed native session must be
/// the one Flow chose and the claim
/// must name that FlowId.
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

### Block 9

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
PowerLevel.[ High Medium Low
             UltraLow ]
HarnessKind.[ Codex Claude ]
LaunchSource.{ SourcePath
               SourceSha256 }
RememberedFlow.{ FlowId
                 RememberingDepth }
```

### Block 10

For a Claude launch the first prompt is one line (`composition.rs:630`):

```rust
fn render_claude_line(
    &self,
    profile: &LaunchProfile,
    bundle_file: &Path,
    sources: &[PathBuf],
) -> String {
    let mut line = self
        .render_native_head(profile,
        None);
    line.push_str(
    &format!(
    "Read {} for your launch mode",
    bundle_file.display()));
    let unstacked = profile
        .skill_name_vector
        .claude_unstacked();
    if !unstacked.is_empty() {
        line.push_str(&format!(
", load {} through the Skill tool in this order",
            unstacked.join(", ")
        ));
    }
    line.push_str(", then: ");
    line.push_str(&profile
        .instruction_prompt);
    if !sources.is_empty() {
        line.push_str(" Sources: ");
        line.push_str(&sources.iter()
            .map(|source| source
                .to_string_lossy())
            .collect::<Vec<_>>().join(
                ", "));
        line.push('.');
    }
    line
}
```

### Block 11

`crates/flow-nexus/src/title.rs:65`:

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

### Block 12

`store.rs:738`:

```rust
/// The role each flow was bound or
/// launched in, and the flows a Herdr
/// pane holds: what ResolveCaller
/// reads.
pub trait ReadsFlowRoles {
    fn role(&self, flow_id: &str)
        -> Result<Option<Caller>,
        StoreError>;
    fn flows_in_pane(&self,
        herdr_session_name: &str,
        herdr_pane_id: &str)
        -> Result<Vec<FlowNode>,
            StoreError>;
}
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

### Block 13

messenger-clj, `src/messenger_clj/core.clj:906, 161, 191, 2114`:

```clojure
(let [sender (or *flow-id*
    (System/getenv "FLOW_ID")
                 (fail
"Set FLOW_ID to your own flow ID before sending"))]

(defn message-envelope
    [sender request]
  (flow-id! sender)
  (let [{:keys [variant context body]}
      (request! request)
        [tag value reader]
        (case variant
          :msg    ["#msg"
              (read-msg [sender body])
              read-pane-message]
          :psyche ["#psyche"
              (read-psyche
              [sender context body])
              read-psyche-message]
          …)
        envelope (str tag " "
            (pr-str value))]
    envelope))

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

### Block 14

The Rust Message Nexus, `crates/message-nexus/src/peer.rs:1`, `flow_edge.rs:113`:

```rust
//! Message never takes a sender from
//! a payload. It reads its peer's
//! credentials (`SO_PEERCRED`) and
//! the process's start time, and asks
//! Flow (`ResolvePeer`) which flow
//! that exact process runs in.

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

### Block 15

Extra (a). Canonical Flow checkout 5e0b1bf. `crates/flow-nexus/src/launching.rs:72` with the trait it implements, declared at `launching.rs:45`:

```rust
/// The launch verbs of the running
/// Nexus. `start` is the one Start
/// path; `settle` records what a
/// launch came to and, for a
/// replacement, stops and reaps the
/// predecessor before the successor
/// becomes routable.
pub trait LaunchesFlows {
    /// Runs or resumes the launch a
    /// StartRequest names.
    fn start(&self,
        request: StartRequest)
        -> Response;
    /// Looks again at the native
    /// transcript of a launch whose
    /// first prompt was not yet seen,
    /// promoting it when the receipt
    /// is there.
    fn promote_ambiguous(&self,
        attempt: LaunchAttempt)
        -> Response;
    /// The recorded outcome of a
    /// request already settled, or
    /// None.
    fn settled(&self,
        request: &StartRequest)
        -> Option<Response>;
    /// Records what a Start-path
    /// response settles, completing a
    /// replacement.
    fn settle(&self,
        launch_request_id: &str,
        response: Response)
        -> Response;
    /// Starts the successor through
    /// the Start path, then replaces.
    fn replace(&self,
        request: StartRequest)
        -> Response;
    /// Stops the predecessor, then
    /// closes its pane; only then is
    /// the successor routable.
    fn reap(&self,
        replacement: Replacement,
        launched: Launched)
        -> Response;
    /// Answers once: the outcome,
    /// else the pending attempt.
    fn launch_status(&self,
        launch_request_id: &str)
        -> Response;
    /// Everything a new launch does
    /// after Reserve, from the native
    /// intent to the confirmed
    /// receipt.
    fn launch_reserved(
        &self,
        launch: ComposedLaunch,
        origin: OriginClue,
        reserved: Option<String>,
    ) -> Response;
}

impl LaunchesFlows for RunningNexus {
```

Names: `LaunchesFlows` the trait, `launching.rs:45`; `RunningNexus` `lib.rs:68`; `StartRequest` signal-flow `signal.rs:302`, `Response` :582, `LaunchAttempt` :269, `ComposedLaunch` :137, `OriginClue` :294, `Launched` :392 (signal-flow rev f95034d, the one Flow pins); `Replacement` `store.rs:527`; `Option`, `String`, `&str` std.

### Block 16

Extra (b). Canonical Flow checkout 5e0b1bf. The Submit arm of `perform`, `crates/flow-nexus/src/performing.rs:268-294` (the brief said 268-293; the arm closes at 294); the Codex path of its first turn returns `PromptDeliveryResult::Ambiguous` (the line from `codex.rs:869` follows the arm):

```rust
Operation::Submit(Submit_Data {
    composed_launch,
    prompt_delivery_intent,
}) => {
    let submission =
        match composed_launch
        .launch_profile.harness_kind {
        HarnessKind::Codex => self
            .codex_endpoints
            .adapter_for(
                &composed_launch
                .launch_profile
                .model_name)
            .map_err(
                |_|
                Failed_Data
                ::CodexRefused)
            .and_then(|adapter| {
                adapter
 .submit_bound_codex_first_turn(
     &composed_launch,
     &prompt_delivery_intent,
 )
 .map_err(|_|
     Failed_Data
     ::CodexRefused)
            }),
        HarnessKind::Claude => self
            .herdr
            .submit_first_prompt_once(
            &composed_launch,
            &prompt_delivery_intent)
            .map_err(
                |_|
                Failed_Data
                ::HerdrRefused),
    };
    match submission {
        Ok(result) =>
            Outcome::Submitted(
            result),
        Err(failure) =>
            Outcome::Failed(failure),
    }
}

Ok(PromptDeliveryResult::Ambiguous(
    intent.clone()))
```

Names: `self` is `RunningNexus`, `lib.rs:68`, inside `impl Performs for RunningNexus`, `performing.rs:207`; `Operation` `generated/operation.rs:73`, `Outcome` :113, `Submit_Data` :66 (`composed_launch`, `prompt_delivery_intent`), `Failed_Data` :99 (`CodexRefused`, `HerdrRefused`); `HarnessKind` signal-flow `signal.rs:324`; `codex_endpoints` field of `RunningNexus`, type `CodexEndpoints` `codex.rs:49`; `adapter_for` from `SelectsCodexEndpoint`, `codex.rs:56` (fn :61), returning `CodexAdapter` `codex.rs:30`; `submit_bound_codex_first_turn` from `SubmitsBoundCodexFirstTurn`, `codex.rs:175` (fn :176, implemented for `CodexAdapter` :817); `herdr` field, type `HerdrCli` `herdr.rs:86`; `submit_first_prompt_once` from `SubmitsFirstPromptOnce`, `herdr/launch.rs:99` (fn :100, implemented for `HerdrCli` :1618); `launch_profile`, `model_name` fields of signal-flow `ComposedLaunch` :137 / `LaunchProfile` :104; `PromptDeliveryResult` signal-flow `signal.rs:250`, its `Ambiguous(PromptDeliveryIntent)` :252, built at `codex.rs:869`; `Observed.NativeTargetReceipt` the other variant.
