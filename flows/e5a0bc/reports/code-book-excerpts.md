# The code: bounded excerpts for «The code»

Excerpts for the book «The code», on Flow Nexus and the messenger as they are
on 2026-10-06. They are in reading order. Each one is copied from the named
file at the named lines. A line holding only `…` marks lines left out. Under
each excerpt is a list of every identifier it uses that is declared in
another place, with the path and line of that declaration. When a
declaration is already shown in an earlier excerpt, the list gives the
location and, where it helps, its signature, without copying it again. The
list leaves out the Rust standard library and Clojure core.

## Revisions read

| Name used below | Repository | Revision | Note |
|---|---|---|---|
| `flow` | `/git/github.com/LiGoldragon/flow` | `5e0b1bf` (workspace 0.24.0) | The deployed daemon is 0.23.0. The only differences in these excerpts are `Operation::Release` / `Outcome::Released` and launching.rs:139-144, all marked "0.24.0". |
| `signal-flow` | `/git/github.com/LiGoldragon/signal-flow` | `f95034d` (10.0.0) | The revision pinned by flow and message, read with `git archive`. |
| `meta-signal-flow` | `/git/github.com/LiGoldragon/meta-signal-flow` | `54eb561` (14.0.0) | The revision pinned by flow and message. |
| `messenger-clj` | `/git/github.com/LiGoldragon/messenger-clj` | `85e71b1` (0.3.0) | This is what `hm-*` runs. |
| `message` | `/git/github.com/LiGoldragon/message` | `6fa4d0c` (0.19.1, `origin/main`) | The running binary is 0.19.0. |
| `signal-message` | `/git/github.com/LiGoldragon/signal-message` | `b94d907` | The revision pinned by message. |
| `sema-engine` | `/git/github.com/LiGoldragon/sema-engine` | `9884905` (0.18.0) | The revision pinned by flow (Cargo.lock). |

Paths under `flow` are relative to the repository root. In the generated
files (`signal.rs`, `operation.rs`), each type has three attribute lines
(`#[rustfmt::skip]`, `#[derive(rkyv::Archive, …)]`, `#[cfg_attr(feature =
"datom", …)]`). They are kept when they fall inside a quoted range, and cut
with `…` when they fall between two quoted ranges.

---

## 1. The hook

Claude Code runs `flow-hook`. `flow-hook` turns the event into one
`Report.{ FlowId Event }` datom and runs the `flow` CLI. The CLI sends the
datom over Flow's ordinary socket.

#### 1.1 Flow tells Claude Code to run the hook

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/herdr/launch.rs`, lines 159-183

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
            "hooks": [{
                "type": "command",
                "command": self.harness_hook.to_string_lossy(),
            }]
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

Declared elsewhere:
- `self`: `HerdrCli`, `crates/flow-nexus/src/herdr.rs:86` (excerpt 2.9)
- `PreparesClaudePane`, trait, `crates/flow-nexus/src/herdr/launch.rs:119` (`fn claude_flag_settings(&self) -> String;` at :149)
- `harness_hook: PathBuf`, field of `HerdrCli`, `crates/flow-nexus/src/herdr.rs:100`
- `serde_json::json!`, crate `serde_json`

#### 1.2 Flow puts FLOW_ID and FLOW_SOCKET in the pane before the harness starts

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/herdr/launch.rs`, lines 618-643

```rust
/// The shell line typed into a Claude launch pane before the harness: it
/// removes the inherited Claude identity, exports `FLOW_SOCKET` as the
/// ordinary socket of the Nexus launching the flow, and, for a launch
/// Reserve gave a FlowId, exports that FlowId as FLOW_ID. The harness Herdr
/// starts at that prompt, and every hook it runs, carries both, so
/// `flow-hook`'s `flow` reports to this Nexus whatever runtime directory
/// the pane's shell has. The FlowId is a claim alias, lowercase hex, so it
/// needs no quoting; the socket path is quoted for the shell.
pub(crate) trait PreparesClaudeEnvironment {
    fn claude_environment_preparation(&self, reserved: Option<&str>, socket: &Path) -> String;
}

impl PreparesClaudeEnvironment for str {
    fn claude_environment_preparation(&self, reserved: Option<&str>, socket: &Path) -> String {
        let marker_suffix = self;
        let flow_id = reserved
            .map(|flow_id| format!(" && export FLOW_ID={flow_id}"))
            .unwrap_or_default();
        format!(
            "unset {} && export FLOW_SOCKET={}{flow_id} && printf 'FLOW_CLAUDE_ENV_READY_%s\\n' {}",
            HerdrCli::CLAUDE_INHERITED_ENVIRONMENT.join(" "),
            socket.to_string_lossy().shell_quoted(),
            marker_suffix
        )
    }
}
```

Declared elsewhere:
- `self`: `str` (the launch's marker suffix)
- `HerdrCli::CLAUDE_INHERITED_ENVIRONMENT`, associated const of `PreparesClaudePane`, `crates/flow-nexus/src/herdr/launch.rs:127` (list starting `"FLOW_ID"` at :132)
- `shell_quoted`, `QuotesForShell::shell_quoted`, `crates/flow-nexus/src/herdr/launch.rs:647-648`

#### 1.3a What the hook is

`flow` @ `5e0b1bf` — `crates/flow/src/hook.rs`, lines 1-14

```rust
//! `flow-hook`: the Claude Code command hook Flow writes into every Claude
//! flow it launches. Claude Code runs it on SessionStart, PostToolUse and
//! Stop with the event as JSON on stdin; it turns the event into one
//! `Report.{ FlowId Event }` datom and hands it to the `flow` CLI beside it,
//! which is the only thing here that speaks Signal.
//!
//!   SessionStart -> Report.{ «FLOW_ID» Started }
//!   PostToolUse  -> Report.{ «FLOW_ID» ToolUsed.«tool_name» }
//!   Stop         -> Report.{ «FLOW_ID» Stopped }
//!
//! The FlowId is the `FLOW_ID` the flow claimed, read from the harness's
//! environment, never derived from the harness's session id (ruling 12 of
//! flow f1c841). With no FLOW_ID, or on any other event, it reports
//! nothing.
```

Declared elsewhere: none. The doc comment names `Report.{ FlowId Event }`, which is shown in excerpt 1.7.

#### 1.3b The hook reads the event and its FLOW_ID

`flow` @ `5e0b1bf` — `crates/flow/src/hook.rs`, lines 27-38, 59-70

```rust
/// One hook invocation: the event Claude Code wrote, and the flow it ran in.
struct HarnessHook {
    input: serde_json::Value,
    flow_id: Option<String>,
}

/// What the hook does with one event.
#[derive(Debug, PartialEq, Eq)]
enum HookCall {
    Report(String),
    Nothing(&'static str),
}
…
impl ReadsHookInput for HarnessHook {
    fn from_environment() -> Self {
        let mut text = String::new();
        let _ = std::io::stdin().read_to_string(&mut text);
        Self {
            input: serde_json::from_str(&text).unwrap_or(serde_json::Value::Null),
            flow_id: env::var("FLOW_ID")
                .ok()
                .filter(|flow_id| !flow_id.is_empty()),
        }
    }
}
```

Declared elsewhere:
- `ReadsHookInput`, trait, `crates/flow/src/hook.rs:40-42`
- `serde_json::Value`, `serde_json::from_str`, crate `serde_json`

#### 1.4 The event becomes a Report datom

`flow` @ `5e0b1bf` — `crates/flow/src/hook.rs`, lines 72-105

```rust
impl QuotesDatomString for str {
    fn quoted(&self) -> String {
        format!("«{}»", self.replace('»', "\\»"))
    }
}

impl ChoosesHookCall for HarnessHook {
    fn event_name(&self) -> String {
        self.input
            .get("hook_event_name")
            .and_then(serde_json::Value::as_str)
            .unwrap_or("-")
            .to_owned()
    }

    fn call(&self) -> HookCall {
        let Some(flow_id) = &self.flow_id else {
            return HookCall::Nothing("no FLOW_ID in the harness environment");
        };
        let event = match self.event_name().as_str() {
            "SessionStart" => "Started".to_owned(),
            "PostToolUse" => match self
                .input
                .get("tool_name")
                .and_then(serde_json::Value::as_str)
            {
                Some(tool_name) => format!("ToolUsed.{}", tool_name.quoted()),
                None => return HookCall::Nothing("PostToolUse without a tool_name"),
            },
            "Stop" => "Stopped".to_owned(),
            _ => return HookCall::Nothing("no Report for this event"),
        };
        HookCall::Report(format!("Report.{{ {} {event} }}", flow_id.quoted()))
    }
```

Declared elsewhere:
- `self` (first impl): `str`. `self` (second impl): `HarnessHook`, `crates/flow/src/hook.rs:28` (excerpt 1.3b)
- `QuotesDatomString`, trait, `crates/flow/src/hook.rs:49-53`
- `ChoosesHookCall`, trait, `crates/flow/src/hook.rs:44-47`
- `HookCall::{Report, Nothing}`, `crates/flow/src/hook.rs:35-38` (excerpt 1.3b)
- `self.input`, `self.flow_id`, fields of `HarnessHook`, `crates/flow/src/hook.rs:29-30`
- `quoted`, `QuotesDatomString::quoted`, `crates/flow/src/hook.rs:52`

#### 1.5 The hook runs the flow CLI beside it

`flow` @ `5e0b1bf` — `crates/flow/src/hook.rs`, lines 108-120, 139-142

```rust
impl ReportsThroughCli for HarnessHook {
    fn run(&self) -> String {
        let datom = match self.call() {
            HookCall::Report(datom) => datom,
            HookCall::Nothing(reason) => return format!("{}\t-\t-\t{reason}", self.event_name()),
        };
        // The `flow` CLI installed beside this executable, else on PATH.
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

Declared elsewhere:
- `self`: `HarnessHook`, `crates/flow/src/hook.rs:28`
- `ReportsThroughCli`, trait, `crates/flow/src/hook.rs:55-57`
- `call`, `event_name`, `ChoosesHookCall`, `crates/flow/src/hook.rs:45-46` (excerpt 1.4)
- `from_environment`, `ReadsHookInput::from_environment`, `crates/flow/src/hook.rs:41` (excerpt 1.3b)

#### 1.6a The flow CLI parses the datom and sends it over the socket

`flow` @ `5e0b1bf` — `crates/flow/src/main.rs`, lines 11-13, 30-31, 38-56

```rust
struct FlowClient {
    socket: String,
}
…
impl ParsesFlowCommand for FlowClient {
    fn parse_command(&self, mut arguments: impl Iterator<Item = String>) -> Result<Query, String> {
…
        let mut budget = Budget {
            remaining: 65_536,
            reader: ReaderBudget { remaining: 65_536 },
            depth: 0,
            maximum_depth: 1_024,
        };
        Potential::<Query>::from(value)
            .actualize(&mut budget)
            .map_err(|error| format!("invalid Flow query: {error:?}"))
    }
}

impl CallsFlowNexus for FlowClient {
    fn call(&self, query: &Query, each: &mut dyn FnMut(Response)) -> Result<(), String> {
        let mut peer = UnixStream::connect(&self.socket).map_err(|error| error.to_string())?;
        let bytes = rkyv::to_bytes::<rkyv::rancor::Error>(query).map_err(|e| e.to_string())?;
        peer.write_all(&(bytes.len() as u32).to_be_bytes())
            .map_err(|e| e.to_string())?;
        peer.write_all(&bytes).map_err(|e| e.to_string())?;
```


#### 1.6b The flow CLI's main

`flow` @ `5e0b1bf` — `crates/flow/src/main.rs`, lines 106-128

```rust
fn main() {
    let arguments = env::args().skip(1).collect::<Vec<_>>();
    if let Some(version) = arguments.version_answer() {
        println!("{version}");
        return;
    }
    // The Nexus's default ordinary socket under this caller's runtime
    // directory, unless the caller names another Nexus's socket.
    let client = FlowClient {
        socket: env::var("FLOW_SOCKET").unwrap_or_else(|_| {
            DefaultConfiguration::from_environment()
                .ordinary_socket_path()
                .to_string_lossy()
                .into_owned()
        }),
    };
    match client
        .parse_command(arguments.into_iter())
        .and_then(|query| {
            client.call(&query, &mut |reply| {
                println!("{}", client.textualize_reply(&reply))
            })
        }) {
```

Declared elsewhere:
- `self`: `FlowClient`, `crates/flow/src/main.rs:11` (shown)
- `ParsesFlowCommand`, `CallsFlowNexus`, traits, `crates/flow/src/main.rs:15-17, 19-24`
- `Query`, `Response`: signal-flow `src/generated/signal.rs:560, 582` (excerpt 1.8), imported at `crates/flow/src/main.rs:4`
- `Query::Observe`, `signal-flow@f95034d:src/generated/signal.rs:568`
- `Budget`, `Potential`, `Actualizing::actualize`: crate `datom_codec` (imported at `crates/flow/src/main.rs:1`)
- `ReaderBudget`: crate `protos` (imported at `crates/flow/src/main.rs:3`)
- `rkyv::to_bytes`, `rkyv::from_bytes`: crate `rkyv`
- `version_answer`, `AnswersVersion`, `crates/flow/src/main.rs:93-95`
- `textualize_reply`, `TextualizesFlowReply`, `crates/flow/src/main.rs:26-28`
- `DefaultConfiguration`, `crates/flow-defaults/src/lib.rs:15`. `from_environment` is `ReadsAnchors::from_environment`, `crates/flow-defaults/src/lib.rs:69`. `ordinary_socket_path` is `LaysOutDefaults::ordinary_socket_path`, `crates/flow-defaults/src/lib.rs:130` (trait at :93)

#### 1.7 The wire: Report and Event in the contract source

`signal-flow` @ `f95034d` — `ethos/signal.ethos`, lines 72-76, 81-82, 93, 114-115, 218-220

```
; Report carries one harness event of a flow Flow holds, sent by the
; harness's hook through the Flow CLI with the FlowId the flow was
; launched with. Flow stores the event in that flow's Memory and answers
; Reported. A FlowId Flow does not hold is refused, Refused.UnknownFlow,
; never adopted: a flow Flow did not launch is a flow Flow does not know.
…
Signal
[]
…
  Report.{ FlowId Event } ]
…
  Reported
  Refused.[ UnknownFlow.FlowId ] ]
…
  Event.[ Started
          ToolUsed.String
          Stopped ] ]
```

Declared elsewhere:
- `FlowId`, `signal-flow@f95034d:ethos/signal.ethos:116` (`FlowId.String`)

#### 1.8 The wire: Report and Event as generated Rust

`signal-flow` @ `f95034d` — `src/generated/signal.rs`, lines 545-556, 560-561, 571-572, 576-578, 582, 603-605

```rust
pub enum Event {
    Started,
    ToolUsed(String),
    Stopped,
}
#[rustfmt::skip]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq, Hash)]
#[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Composing))]
pub struct Report_Data {
    pub flow_id: FlowId,
    pub event: Event,
}
…
pub enum Query {
    Start(StartRequest),
…
    Report(Report_Data),
}
…
pub enum Refused_Data {
    UnknownFlow(FlowId),
}
…
pub enum Response {
…
    Reported,
    Refused(Refused_Data),
}
```

Declared elsewhere:
- `FlowId`, `signal-flow@f95034d:src/generated/signal.rs:3` (`pub type FlowId = String;`)
- `StartRequest`, `signal-flow@f95034d:src/generated/signal.rs:302-305` (`pub struct StartRequest { pub launch_profile: LaunchProfile, pub origin_clue: OriginClue }`)

#### 1.9 The Nexus answers Report without waiting behind a launch

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/lib.rs`, lines 478-480, 494-496

```rust
    fn serve_ordinary(mut self, nexus: &RunningNexus) -> Result<(), String> {
        let query = self.peer.read_query()?;
        let response = match query {
…
            // A hook's Report never waits behind a running launch: the
            // launch may itself be waiting on the harness whose hook this is.
            Query::Report(report) => nexus.report(report),
```

Declared elsewhere:
- `self`: `Connection`, `crates/flow-nexus/src/lib.rs:458` (impl `ServesConnection` :470). `nexus: &RunningNexus`, `crates/flow-nexus/src/lib.rs:68` (excerpt 2.1)
- `read_query`, `crates/flow-nexus/src/lib.rs:731` (impl :761)
- `report`, `RecordsReports::report`, `crates/flow-nexus/src/reporting.rs:18` (excerpt 1.10)

#### 1.10 The Report becomes one Operation

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/reporting.rs`, lines 1-6, 17-43

```rust
//! A harness event reaches Flow as `Report.{ FlowId Event }`, sent by the
//! flow's hook through the Flow CLI. It is one Operation, Record.Harness,
//! which appends the event to the events Flow's Memory holds for that flow.
//! A FlowId Flow does not hold is refused as `Refused.UnknownFlow`, never
//! adopted. The owner reads the events back over the meta socket with
//! `ReadEvents`.
…
pub trait RecordsReports {
    fn report(&self, report: Report_Data) -> Response;
    fn read_events(&self, flow_id: FlowId) -> meta_signal_flow::Response;
}

impl RecordsReports for RunningNexus {
    fn report(&self, report: Report_Data) -> Response {
        let Report_Data { flow_id, event } = report;
        match self.perform(Operation::Record(Record_Data::Harness(
            Record_Data_Harness_Data {
                flow_id: flow_id.clone(),
                event,
            },
        ))) {
            Outcome::Recorded => Response::Reported,
            Outcome::Failed(Failed_Data::UnknownFlow) => {
                Response::Refused(Refused_Data::UnknownFlow(flow_id))
            }
            // signal-flow 9.0.0 names no persistence refusal for Report, so
            // a store that fails is answered as a flow Flow cannot vouch
            // for, and logged.
            outcome => {
                eprintln!("flow-nexus: Report for {flow_id} not recorded: {outcome:?}");
                Response::Refused(Refused_Data::UnknownFlow(flow_id))
            }
        }
    }
```

Declared elsewhere:
- `self`: `RunningNexus`, `crates/flow-nexus/src/lib.rs:68` (excerpt 2.1)
- `Report_Data`, `Response`, `Refused_Data::UnknownFlow`: `signal-flow@f95034d:src/generated/signal.rs:553, 582, 576` (excerpt 1.8)
- `FlowId`, `signal-flow@f95034d:src/generated/signal.rs:3`
- `meta_signal_flow::Response`, `meta-signal-flow@54eb561:src/generated/signal.rs:429`
- `perform`, `Performs::perform`, `crates/flow-nexus/src/performing.rs:141` (excerpt 2.2)
- `Operation::Record`, `Outcome::Recorded`, `Outcome::Failed`, `Failed_Data::UnknownFlow`: `crates/flow-nexus/src/generated/operation.rs:76, 116, 128, 107` (excerpt 2.3)
- `Record_Data::Harness`, `Record_Data_Harness_Data`: `crates/flow-nexus/src/generated/operation.rs:47, 27-30` (excerpt 5.6)
- The arm that performs `Record.Harness`: `crates/flow-nexus/src/performing.rs:432-439` calls `FlowStore::record_event` (excerpt 6.2)

---

## 2. Start

A `Start.{ LaunchProfile OriginClue }` arrives. It is dispatched to
`RunningNexus::start`. That runs Compose and Reserve, then `launch_reserved`:
Intent, Open, Spawn, **Bind**, Record.Binding, Register, Acknowledge, Title,
Submit, and finally Confirm. Confirm answers `Started(Launched)`.

#### 2.1 `RunningNexus`: the `self` of every Start step

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/lib.rs`, lines 68-78

```rust
pub struct RunningNexus {
    pub store: FlowStore,
    pub codex_endpoints: CodexEndpoints,
    pub herdr: herdr::HerdrCli,
    pub composer: LaunchComposer,
    /// Serializes dispatch; see `dispatch_serially`.
    pub dispatch_gate: Mutex<()>,
    /// The exclusive hold on each pane Flow is writing; see
    /// `delivery::lease`.
    pub pane_leases: delivery::lease::PaneLeases,
}
```

Declared elsewhere:
- `FlowStore`, `crates/flow-nexus/src/store.rs:614` (excerpt 6.5)
- `CodexEndpoints`: `crate::codex`, `crates/flow-nexus/src/codex.rs`
- `herdr::HerdrCli`, `crates/flow-nexus/src/herdr.rs:86` (excerpt 2.9)
- `LaunchComposer`, `crates/flow-nexus/src/composition.rs:37` (excerpt 3.1)
- `delivery::lease::PaneLeases`, `crates/flow-nexus/src/delivery/lease.rs`
- `Mutex`, std

#### 2.2 `perform`: one Operation in, one Outcome out

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/performing.rs`, lines 126-127, 138-142, 207-214

```rust
/// The Nexus acting: one Operation in, one Outcome out.
pub trait Performs {
…
    const BRIEF_CONTINUATION: &'static str =
        "Launch receipt confirmed. Begin the brief in your first prompt now.";

    fn perform(&self, operation: Operation) -> Outcome;
}
…
impl Performs for RunningNexus {
    fn perform(&self, operation: Operation) -> Outcome {
        match operation {
            Operation::Compose(profile) => match self.composer.compose(&profile) {
                Ok(launch) => Outcome::Composed(launch),
                Err(_) => Outcome::Failed(Failed_Data::CompositionRefused),
            },
            Operation::Reserve(reserve) => self.reserve(reserve),
```

Declared elsewhere:
- `self` (impl): `RunningNexus`, `crates/flow-nexus/src/lib.rs:68` (excerpt 2.1)
- `Operation`, `Outcome`, `Failed_Data`: `crates/flow-nexus/src/generated/operation.rs:73, 113, 99` (excerpt 2.3)
- `self.composer`: field, `crates/flow-nexus/src/lib.rs:72`. `compose`: `ComposesLaunch::compose`, `crates/flow-nexus/src/composition.rs:149` (excerpt 3.5)
- `self.reserve`: a `PerformsInParts` method on `RunningNexus`, `crates/flow-nexus/src/performing.rs:337`

#### 2.3a The `Operation` enum (generated)

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/generated/operation.rs`, lines 5-9, 13-16, 73-88

```rust
pub struct PaneLaunch {
    pub composed_launch: signal_flow::ComposedLaunch,
    pub herdr_pane_binding: signal_flow::HerdrPaneBinding,
    pub flow_id_option: std::option::Option<signal_flow::FlowId>,
}
…
pub struct Reserve_Data {
    pub composed_launch: signal_flow::ComposedLaunch,
    pub origin_clue: signal_flow::OriginClue,
}
…
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
```


#### 2.3b The `Outcome` enum (generated)

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/generated/operation.rs`, lines 92-95, 113-129

```rust
pub struct Reserved_Data {
    pub launch_attempt_reservation: signal_flow::LaunchAttemptReservation,
    pub flow_id_option: std::option::Option<signal_flow::FlowId>,
}
…
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
```

`Release` (:87) and `Released` (:127) are new in 0.24.0. The deployed 0.23.0
does not have them.

Declared elsewhere (each `signal_flow::X` is in `signal-flow@f95034d:src/generated/signal.rs`):
- `ComposedLaunch` :137; `HerdrPaneBinding` :145; `FlowId` :3; `OriginClue` :294; `LaunchProfile` :104 (excerpt 3.3); `FlowNode` :378 (excerpt 2.7); `LaunchRequestId` :25; `Launched` :392 (excerpt 2.8a); `NativeLaunchBinding` :167 (excerpt 2.10); `PromptDeliveryResult` :250; `LaunchAttemptReservation` :286-290 (`Reserved(LaunchAttempt)`, `Existing(LaunchAttempt)`, `Conflict`)
- `Record_Data` :34, `Register_Data` :52, `Title_Data` :59, `Submit_Data` :66, `Failed_Data` :99: same file, `crates/flow-nexus/src/generated/operation.rs` (`Record_Data` in excerpt 5.6)
- Source: `crates/flow-nexus/ethos/operation.ethos:29-81`, generated by `crates/flow-nexus/build.rs` through ethos-zero `c2653dd`

#### 2.4 The request reaches `start`

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/lib.rs`, lines 85-96

```rust
impl Dispatches for RunningNexus {
    fn dispatch(&self, query: Query) -> Response {
        match query {
            Query::Start(request) => {
                let launch_request_id = request.launch_profile.launch_request_id.clone();
                if let Some(settled) = self.settled(&request) {
                    return settled;
                }
                let response = self.start(request);
                self.settle(&launch_request_id, response)
            }
            Query::Replace(request) => self.replace(request),
```

Declared elsewhere:
- `self`: `RunningNexus`, `crates/flow-nexus/src/lib.rs:68`
- `Dispatches`, trait, `crates/flow-nexus/src/lib.rs:80-83`
- `Query::Start`, `Query::Replace`, `signal-flow@f95034d:src/generated/signal.rs:561, 566`
- `launch_profile.launch_request_id`, `signal-flow@f95034d:src/generated/signal.rs:303, 105`
- `settled`, `start`, `settle`, `replace`, `launch_status`: `LaunchesFlows`, `crates/flow-nexus/src/launching.rs:52, 48, 54, 56, 61` (trait at :45). Bodies: `start` 2.5, `settle` 2.8b, `replace` 5.1

#### 2.5 `start`: Compose, then Reserve

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/launching.rs`, lines 72-76, 97-101, 112-121, 134-146

```rust
impl LaunchesFlows for RunningNexus {
    fn start(&self, request: StartRequest) -> Response {
        let origin = request.origin_clue.clone();
        let launch_request_id = request.launch_profile.launch_request_id.clone();
        let existing = match self.store.launch_attempt(&launch_request_id) {
…
        let persistence = || Response::StartRejected(StartRejection::LaunchPersistenceRefused);
        let launch = match self.perform(Operation::Compose(request.launch_profile)) {
            Outcome::Composed(launch) => launch,
            _ => return Response::StartRejected(StartRejection::CompositionRefused),
        };
…
        // A Claude launch's FlowId is claimed here, before its harness
        // exists; the harness is spawned with it.
        let reserved = match self.perform(Operation::Reserve(Reserve_Data {
            composed_launch: launch.clone(),
            origin_clue: origin.clone(),
        })) {
            Outcome::Reserved(Reserved_Data {
                launch_attempt_reservation: LaunchAttemptReservation::Reserved(_),
                flow_id_option,
            }) => flow_id_option,
…
            Outcome::Failed(Failed_Data::ClaimRefused) => {
                return Response::StartRejected(StartRejection::BindingRefused);
            }
            _ => return persistence(),
        };
        let response = self.launch_reserved(launch, origin, reserved.clone());
        // A launch refused after Reserve gives back the flow it held and
        // the FlowId it claimed; the refusal stands whatever Release does.
        if let (Response::StartRejected(_), Some(flow_id)) = (&response, reserved) {
            let _ = self.perform(Operation::Release(flow_id));
        }
        response
    }
```

Lines 139-144 (Release after refusal) are 0.24.0. In the deployed 0.23.0,
`start` returns `self.launch_reserved(…)` directly.

Declared elsewhere:
- `self`: `RunningNexus`, `crates/flow-nexus/src/lib.rs:68`
- `StartRequest { launch_profile, origin_clue }`, `signal-flow@f95034d:src/generated/signal.rs:302-305`
- `Response::StartRejected`, `StartRejection::{CompositionRefused, BindingRefused, LaunchPersistenceRefused}`: `signal-flow@f95034d:src/generated/signal.rs:582, 408-417`
- `self.store.launch_attempt`: `ReadsLaunchAttempt::launch_attempt`, `crates/flow-nexus/src/store.rs:816`
- `perform`: excerpt 2.2. `Operation::{Compose, Reserve, Release}`, `Outcome::{Composed, Reserved, Failed}`, `Reserve_Data`, `Reserved_Data`, `Failed_Data::ClaimRefused`: excerpt 2.3
- `LaunchAttemptReservation::Reserved`, `signal-flow@f95034d:src/generated/signal.rs:286-290`
- `launch_reserved`, `LaunchesFlows::launch_reserved`, `crates/flow-nexus/src/launching.rs:64-69` (excerpt 2.6)

#### 2.6 `launch_reserved`: Intent, Open, Spawn, Bind

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/launching.rs`, lines 148-155, 162-187

```rust
    fn launch_reserved(
        &self,
        launch: ComposedLaunch,
        origin: OriginClue,
        reserved: Option<String>,
    ) -> Response {
        let persistence = || Response::StartRejected(StartRejection::LaunchPersistenceRefused);
        let native_intent = NativeLaunchIntent {
…
        };
        if self.perform(Operation::Record(Record_Data::Intent(native_intent))) != Outcome::Recorded
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
        if self.perform(Operation::Record(Record_Data::Binding(binding.clone())))
            != Outcome::Recorded
        {
            return persistence();
        }
```

Declared elsewhere:
- `self`: `RunningNexus`, `crates/flow-nexus/src/lib.rs:68`
- `ComposedLaunch`, `OriginClue`, `NativeLaunchIntent`: `signal-flow@f95034d:src/generated/signal.rs:137-141, 294-298, 156-163`
- `Operation::{Record, Open, Spawn, Bind}`, `Outcome::{Recorded, Opened, Spawned, Bound}`, `PaneLaunch`: excerpt 2.3. `Record_Data::{Intent, Binding}`: excerpt 5.6
- The Bind arm of `perform`: excerpt 2.10
- `StartRejection::{NativeLaunchRefused, BindingRefused}`, `signal-flow@f95034d:src/generated/signal.rs:412-413`

#### 2.7 `launch_reserved`: the node, the role, Register

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/launching.rs`, lines 188-217

```rust
        let node = FlowNode {
            flow_id: binding.flow_id.clone(),
            session_id: binding.native_session_id.clone(),
            harness_kind: binding.harness_kind.clone(),
            endpoint_selection: EndpointSelection::Unavailable,
            herdr_route_selection: HerdrRouteSelection::Available(HerdrRoute {
                herdr_session_name: binding.herdr_pane_binding.herdr_session_name.clone(),
                herdr_agent_name: binding.herdr_pane_binding.herdr_agent_name.clone(),
                herdr_pane_id: binding.herdr_pane_binding.herdr_pane_id.clone(),
                herdr_terminal_id: binding.herdr_pane_binding.herdr_terminal_id.clone(),
            }),
            origin_clue: origin,
            flow_lifecycle: FlowLifecycle::Pending,
        };
        if !self.herdr.validate_registration(&node) {
            return Response::StartRejected(StartRejection::RegistrationRefused);
        }
        let caller = signal_flow::Caller {
            flow_id: binding.flow_id.clone(),
            flow_aspect: launch.launch_profile.flow_aspect.clone(),
            power_level: launch.launch_profile.power_level.clone(),
            model_name: launch.launch_profile.model_name.clone(),
        };
        let registered = match self.perform(Operation::Register(Register_Data {
            flow_node: node,
            caller,
        })) {
            Outcome::Registered(node) => node,
            _ => return Response::StartRejected(StartRejection::RegistrationRefused),
        };
```

Declared elsewhere:
- `binding`: `NativeLaunchBinding`, `signal-flow@f95034d:src/generated/signal.rs:167-173` (fields `flow_id`, `native_session_id`, `harness_kind`, `herdr_pane_binding`)
- `FlowNode`, `signal-flow@f95034d:src/generated/signal.rs:378-386`; `EndpointSelection::Unavailable` :345; `HerdrRouteSelection::Available` :361; `HerdrRoute` :352; `FlowLifecycle::Pending` :368 (excerpt 5.4)
- `HerdrPaneBinding` fields, `signal-flow@f95034d:src/generated/signal.rs:145-152`
- `self.herdr.validate_registration`: `ReadsHerdrPanes::validate_registration`, `crates/flow-nexus/src/herdr.rs:393`
- `signal_flow::Caller`, `signal-flow@f95034d:src/generated/signal.rs:501-506` (excerpt 6.3)
- `launch.launch_profile.{flow_aspect, power_level, model_name}`, `signal-flow@f95034d:src/generated/signal.rs:108, 109, 111`
- `Operation::Register`, `Register_Data { flow_node, caller }`, `Outcome::Registered`: `crates/flow-nexus/src/generated/operation.rs:77, 52-55, 117`. Performed by `FlowStore::register_flow_in_role` (`crates/flow-nexus/src/performing.rs:216-217`), which writes `StoredRole` (excerpt 6.4)

#### 2.8a Confirm answers `Started(Launched)`

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/launching.rs`, lines 300-310, 631-639

```rust
            PromptDeliveryResult::Observed(receipt) => {
                if self.perform(Operation::Record(Record_Data::Delivered(
                    PromptDeliveryResult::Observed(receipt),
                ))) != Outcome::Recorded
                {
                    return persistence();
                }
                self.confirmed(&binding.flow_id)
            }
        }
    }
…
    fn confirmed(&self, flow_id: &str) -> Response {
        match self.perform(Operation::Confirm(flow_id.into())) {
            Outcome::Started(started) => Response::Started(started),
            Outcome::Failed(Failed_Data::Unstarted) => {
                Response::StartRejected(StartRejection::NativeLaunchRefused)
            }
            _ => Response::StartRejected(StartRejection::LaunchPersistenceRefused),
        }
    }
```


#### 2.8b `settle`: a Start that replaces nothing continues; a replacement reaps

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/launching.rs`, lines 377-395

```rust
    fn settle(&self, launch_request_id: &str, response: Response) -> Response {
        let replacement = match self.store.replacement(launch_request_id) {
            Ok(replacement) => replacement,
            Err(_) => return response,
        };
        match response {
            Response::Started(started) => match replacement {
                Some(replacement) => self.reap(replacement, started),
                None => {
                    // A Started flow stays Started; a failed outcome write
                    // only leaves LaunchStatus to answer from the attempt.
                    let _ = self.perform(Self::settled_as(
                        launch_request_id,
                        LaunchOutcome::Started(started.clone()),
                    ));
                    let _ = self.perform(Operation::Continue(started.flow_id.clone()));
                    Response::Started(started)
                }
            },
```

Lines 218-299, which are left out, record the acknowledgement, perform
`Title` (excerpt 4.1), resolve native skills, and `Submit` the first prompt.

Declared elsewhere:
- `self`: `RunningNexus`, `crates/flow-nexus/src/lib.rs:68`
- `PromptDeliveryResult::Observed`, `signal-flow@f95034d:src/generated/signal.rs:250-253`
- `Record_Data::Delivered`, `Settled`: excerpt 5.6
- `self.store.replacement`, `crates/flow-nexus/src/store.rs:811`. `Replacement`: excerpt 5.3
- `reap`, `crates/flow-nexus/src/launching.rs:488` (excerpts 5.2a-b)
- `settled_as`, `confirmed`: `ResumesReplacement`, `crates/flow-nexus/src/launching.rs:596, 598` (trait at :592)
- `LaunchOutcome::Started`, `crates/flow-nexus/src/store.rs:479-484` (excerpt 5.3)
- `Operation::{Confirm, Continue}`, `Outcome::Started`, `Failed_Data::Unstarted`: excerpt 2.3. The Confirm arm is `crates/flow-nexus/src/performing.rs:225-229` → `FlowStore::confirm_started` → `confirm_start`, `crates/flow-nexus/src/store.rs:1083-1085, 2353-2376`, which builds `Launched { flow_id, session_id, origin_clue }` at :2371-2375
- `Launched`, `signal-flow@f95034d:src/generated/signal.rs:392-396`: `pub struct Launched { pub flow_id: FlowId, pub session_id: SessionId, pub origin_clue: OriginClue }`

#### 2.9 `HerdrCli`: the `self.herdr` that Bind calls

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/herdr.rs`, lines 85-110

```rust
/// The production Herdr roster reader.
pub struct HerdrCli {
    pub(crate) executable: PathBuf,
    flow_id_executable: PathBuf,
    flows_root: PathBuf,
    codex_endpoints: CodexEndpoints,
    claude_transcript_root: PathBuf,
    /// The Claude daemon's records, read for a daemon-owned session's
    /// readiness.
    pub(crate) claude_daemon: crate::claude::ClaudeDaemon,
    /// Native Claude skill catalogs, highest-precedence first.
    claude_skill_roots: Vec<PathBuf>,
    /// The `flow-hook` Claude Code runs on SessionStart, PostToolUse and
    /// Stop in every Claude flow Flow launches: the one installed beside
    /// this Nexus's own executable.
    pub(crate) harness_hook: PathBuf,
    /// This Nexus's own ordinary socket, the one it serves: every Claude
    /// pane it launches gets it as `FLOW_SOCKET`, so the `flow` CLI that
    /// `flow-hook` runs reports to the Nexus that launched the flow, not to
    /// whatever Nexus the default path under the pane's runtime directory
    /// names.
    pub(crate) ordinary_socket: PathBuf,
    /// Where each launch's own bundle copy lives, the one a Claude launch
    /// receives as `--system-prompt-file`.
    launch_bundles: LaunchBundles,
}
```

Declared elsewhere:
- `CodexEndpoints`, `crates/flow-nexus/src/codex.rs`
- `crate::claude::ClaudeDaemon`, `crates/flow-nexus/src/claude.rs`
- `LaunchBundles`, `crates/flow-nexus/src/composition.rs:63-65` (excerpt 3.1)

#### 2.10 Bind: the arm in `perform` and `observe_native_binding`

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/performing.rs`, lines 246-257; `crates/flow-nexus/src/herdr/launch.rs`, lines 51-62, 1402-1410

```rust
            Operation::Bind(PaneLaunch {
                composed_launch,
                herdr_pane_binding,
                flow_id_option,
            }) => match self.herdr.observe_native_binding(
                &composed_launch,
                &herdr_pane_binding,
                flow_id_option.as_deref(),
            ) {
                Ok(binding) => Outcome::Bound(binding),
                Err(error) => HerdrFailure::refused(HerdrFailureStage::Bind, error),
            },
```

```rust
/// Observes an official Herdr integration report and binds it to an exact
/// native identity claim. Screen detection and caller metadata are rejected.
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
…
impl ObservesNativeLaunchBinding for HerdrCli {
    fn observe_native_binding(
        &self,
        launch: &ComposedLaunch,
        pane: &HerdrPaneBinding,
        reserved: Option<&str>,
    ) -> Result<NativeLaunchBinding, String> {
        launch.binding_matches_launch(pane)?;
        let expected_harness = launch.launch_profile.harness_kind.expected_harness();
```

Declared elsewhere:
- `self` (performing.rs): `RunningNexus`; `self.herdr`: `HerdrCli` (excerpt 2.9). `self` (launch.rs impl): `HerdrCli`
- `PaneLaunch { composed_launch, herdr_pane_binding, flow_id_option }`, `crates/flow-nexus/src/generated/operation.rs:5-9` (excerpt 2.3)
- `HerdrFailure::refused`, `HerdrFailureStage::Bind`: `crates/flow-nexus/src/performing.rs:95, 29`
- `ComposedLaunch`, `HerdrPaneBinding`, `NativeLaunchBinding`: `signal-flow@f95034d:src/generated/signal.rs:137, 145, 167`
- `binding_matches_launch`, a `ComposedLaunch` method in `crates/flow-nexus/src/herdr/launch.rs`
- `expected_harness`, a `HarnessKind` method in `crates/flow-nexus/src/herdr/launch.rs`
- `run_json`, a `HerdrCli` method in `crates/flow-nexus/src/herdr.rs`

---

## 3. Composition

#### 3.1 `LaunchComposer`: the `self` of composition

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/composition.rs`, lines 37-40, 62-65

```rust
pub struct LaunchComposer {
    source_root: PathBuf,
    launch_bundles: LaunchBundles,
}
…
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LaunchBundles {
    directory: PathBuf,
}
```

Declared elsewhere: none apart from `PathBuf` (std). `RunningNexus.composer`
holds the composer (`crates/flow-nexus/src/lib.rs:72`). It is built by
`OpensLaunchComposer::at`, `crates/flow-nexus/src/composition.rs:388-394`.

#### 3.2 `LaunchProfile` in the contract source

`signal-flow` @ `f95034d` — `ethos/signal.ethos`, lines 116, 127-135, 150-154, 182

```
[ FlowId.String
…
  LaunchRequestId.String
  SourcePath.String
  SourceSha256.String
  SkillName.String
  ModelName.String
  Effort.String
  RememberingDepth.Integer
  SystemPromptBundleFile.String
  InstructionPrompt.String
…
  FlowAspect.[ Psyche Mind Field ]
  PowerLevel.[ High Medium Low UltraLow ]
  LaunchSource.{ SourcePath SourceSha256 }
  RememberedFlow.{ FlowId RememberingDepth }
  LaunchProfile.{ LaunchRequestId Vector<LaunchSource> Vector<SkillName> FlowAspect PowerLevel HarnessKind ModelName Effort Option<FlowId> Vector<RememberedFlow> HerdrSessionName SystemPromptBundleFile InstructionPrompt }
…
  HarnessKind.[ Codex Claude ]
```

Declared elsewhere: none. Every name is declared in this file, and the
excerpt shows each line that declares a field type. The leaf types not
shown (`HerdrSessionName.String` :122) are also `String`.

#### 3.3 `LaunchProfile` as generated Rust

`signal-flow` @ `f95034d` — `src/generated/signal.rs`, lines 73-77, 81-86, 90-93, 97-100, 104-118

```rust
pub enum FlowAspect {
    Psyche,
    Mind,
    Field,
}
…
pub enum PowerLevel {
    High,
    Medium,
    Low,
    UltraLow,
}
…
pub struct LaunchSource {
    pub source_path: SourcePath,
    pub source_sha256: SourceSha256,
}
…
pub struct RememberedFlow {
    pub flow_id: FlowId,
    pub remembering_depth: RememberingDepth,
}
…
pub struct LaunchProfile {
    pub launch_request_id: LaunchRequestId,
    pub launch_source_vector: std::vec::Vec<LaunchSource>,
    pub skill_name_vector: std::vec::Vec<SkillName>,
    pub flow_aspect: FlowAspect,
    pub power_level: PowerLevel,
    pub harness_kind: HarnessKind,
    pub model_name: ModelName,
    pub effort: Effort,
    pub flow_id_option: std::option::Option<FlowId>,
    pub remembered_flow_vector: std::vec::Vec<RememberedFlow>,
    pub herdr_session_name: HerdrSessionName,
    pub system_prompt_bundle_file: SystemPromptBundleFile,
    pub instruction_prompt: InstructionPrompt,
}
```

Declared elsewhere (same file):
- `LaunchRequestId` :25, `SourcePath` :27, `SourceSha256` :29, `SkillName` :31, `ModelName` :33, `Effort` :35, `RememberingDepth` :37 (`i64`), `SystemPromptBundleFile` :39, `InstructionPrompt` :41, `HerdrSessionName` :15. All are `pub type … = String;` except `RememberingDepth`.
- `FlowId` :3. `HarnessKind` :324-327 (`Codex`, `Claude`).

#### 3.4 `render_body`: the `body.push_str(&profile.instruction_prompt)` site (Codex)

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/composition.rs`, lines 699-735

```rust
    fn render_body(
        &self,
        profile: &LaunchProfile,
        bundle: &LaunchBundleText,
        sources: &[PathBuf],
    ) -> String {
        let bundle = match bundle {
            LaunchBundleText::File(file) => {
                return self.render_claude_line(profile, file, sources);
            }
            LaunchBundleText::Inline(text) => Some(text.as_str()),
        };
        // Predecessor and remembered flows are in the bundle text's trailing
        // section, which opens this block; the launch record does not repeat
        // them.
        let mut body = self.render_native_head(profile, bundle);
        body.push_str(&format!(
            "# Flow launch\n\nRole: {} {}\nHarness: Codex\nModel: {}\nEffort: {}\nHerdr session: {}\nRemote control: {}\n",
            profile.aspect_name(),
            profile.power_name(),
            profile.model_name,
            profile.effort,
            profile.herdr_session_name,
            profile.remote_control_record(),
        ));
        body.push('\n');
        body.push_str(&profile.instruction_prompt);
        if !sources.is_empty() {
            body.push_str("\n\nSources:");
            for source in sources {
                body.push_str("\n- ");
                body.push_str(&source.to_string_lossy());
            }
        }
        body
    }
}
```

Declared elsewhere:
- `self`: `LaunchComposer`, `crates/flow-nexus/src/composition.rs:37` (excerpt 3.1)
- `RendersLaunchProfile` (declares `render_body`), `crates/flow-nexus/src/composition.rs:355-375` (`fn render_body(&self, profile: &LaunchProfile, bundle: &LaunchBundleText, sources: &[PathBuf]) -> String;` at :369-374)
- `LaunchBundleText::{File, Inline}`, `crates/flow-nexus/src/composition.rs:379-382`
- `render_claude_line`, `crates/flow-nexus/src/composition.rs:635` (excerpt 3.6)
- `render_native_head`, `crates/flow-nexus/src/composition.rs:600-628`
- `aspect_name`, `power_name`: `NamesRole`, `crates/flow-nexus/src/composition.rs:287-290` (impl for `LaunchProfile` :292-309)
- `remote_control_record`: `NamesRemoteControl`, `crates/flow-nexus/src/composition.rs:260` (impl :311-322)
- `profile.{model_name, effort, herdr_session_name, instruction_prompt}`: `LaunchProfile`, `signal-flow@f95034d:src/generated/signal.rs:111, 112, 115, 117` (excerpt 3.3)

#### 3.5 `compose`: builds the first prompt

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/composition.rs`, lines 148-150, 737-775

```rust
pub trait ComposesLaunch {
    fn compose(&self, profile: &LaunchProfile) -> Result<ComposedLaunch, CompositionError>;
}
…
impl ComposesLaunch for LaunchComposer {
    fn compose(&self, profile: &LaunchProfile) -> Result<ComposedLaunch, CompositionError> {
        self.validate(profile)?;
        let sources = profile
            .launch_source_vector
            .iter()
            .map(|source| self.read(source))
            .collect::<Result<Vec<_>, _>>()?;
        let bundle = match profile.harness_kind {
            HarnessKind::Codex => LaunchBundleText::Inline(self.read_bundle(profile)?),
            HarnessKind::Claude => LaunchBundleText::File(self.write_launch_bundle(profile)?),
        };
        let mut body = self.render_body(profile, &bundle, &sources);
…
        let prompt_sha256 = self.sha256(body.as_bytes());
        let target_receipt_request = TargetReceiptRequest {
            launch_request_id: profile.launch_request_id.clone(),
            prompt_sha256: prompt_sha256.clone(),
        };
        let first_prompt_text = format!("{}{}", body, profile.harness_kind.receipt_footer());
        Ok(ComposedLaunch {
            launch_profile: profile.clone(),
            first_prompt_payload: FirstPromptPayload {
                first_prompt_body: body,
                prompt_sha256,
                first_prompt_text,
            },
            target_receipt_request,
        })
    }
}
```

Lines 750-758, which are left out, re-render a Claude body that would not
fit Claude's paste shape through `render_claude_direct`
(`crates/flow-nexus/src/composition.rs:673`). That function also writes
`profile.instruction_prompt`, at :683.

Declared elsewhere:
- `self`: `LaunchComposer`, `crates/flow-nexus/src/composition.rs:37`
- `CompositionError`, `crates/flow-nexus/src/composition.rs:15`
- `validate`: `ValidatesLaunchProfile`, `crates/flow-nexus/src/composition.rs:325`
- `read`: `ReadsLaunchSource`, `crates/flow-nexus/src/composition.rs:339`
- `read_bundle`: `ReadsSystemPromptBundle`, `crates/flow-nexus/src/composition.rs:346`
- `write_launch_bundle`: `WritesLaunchBundle`, `crates/flow-nexus/src/composition.rs:352` (impl :576-597)
- `render_body`: excerpt 3.4
- `sha256`: `HashesPromptBody`, `crates/flow-nexus/src/composition.rs:385` (impl :401-405)
- `receipt_footer`: `AsksForLaunchReceipt`, `crates/flow-nexus/src/composition.rs:173`. Its impl for `HarnessKind` is at :176-189, with `LAUNCH_RECEIPT = "FLOW_LAUNCH_RECEIPT_V2"` at :169.
- `ComposedLaunch`, `FirstPromptPayload`, `TargetReceiptRequest`: `signal-flow@f95034d:src/generated/signal.rs:137-141, 129-133, 122-125`

#### 3.6 `render_claude_line`: the same instruction in a Claude launch

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/composition.rs`, lines 630-667

```rust
    /// Claude's one line: the stacked commands, then one sentence naming
    /// the per-launch bundle to read, the skills past the stack, the goal,
    /// and the sources. Predecessor and remembered flows are in that bundle;
    /// role, model, effort and remote control reach Claude through its argv
    /// and stay in the store.
    fn render_claude_line(
        &self,
        profile: &LaunchProfile,
        bundle_file: &Path,
        sources: &[PathBuf],
    ) -> String {
        let mut line = self.render_native_head(profile, None);
        line.push_str(&format!(
            "Read {} for your launch mode",
            bundle_file.display()
        ));
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
            line.push_str(
                &sources
                    .iter()
                    .map(|source| source.to_string_lossy())
                    .collect::<Vec<_>>()
                    .join(", "),
            );
            line.push('.');
        }
        line
    }
```

Declared elsewhere:
- `self`: `LaunchComposer`
- `render_native_head`, `crates/flow-nexus/src/composition.rs:356` (impl :600-628)
- `claude_unstacked`: `StacksClaudeCommands`, `crates/flow-nexus/src/composition.rs:230` (impl for `[Skill]` :233-243, limit 5 at :224)
- `profile.skill_name_vector`, `profile.instruction_prompt`, `signal-flow@f95034d:src/generated/signal.rs:107, 117`

---

## 4. Title

#### 4.1 `native_title`, whole

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/title.rs`, lines 65-85

```rust
impl TitlesFlow for LaunchProfile {
    fn native_title(&self, flow_id: &str) -> Result<NativeTitle, TitleRefused> {
        if flow_id.len() != 6
            || !flow_id
                .bytes()
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

Declared elsewhere:
- `self`: `LaunchProfile`, `signal-flow@f95034d:src/generated/signal.rs:104` (excerpt 3.3)
- `TitlesFlow`, `crates/flow-nexus/src/title.rs:61-63` (excerpt 4.3)
- `self.model_name`: `pub model_name: ModelName`, `signal-flow@f95034d:src/generated/signal.rs:111`. `ModelName` is `pub type ModelName = String;`, :33. So `.model_display_name()` runs on `str` through auto-deref.
- `model_display_name`: `NamesModel::model_display_name`, `crates/flow-nexus/src/title.rs:37` (excerpt 4.2)
- `self.flow_aspect`: `pub flow_aspect: FlowAspect`, `signal-flow@f95034d:src/generated/signal.rs:108`. `FlowAspect::{Psyche, Mind, Field}`, :73-77
- `TitleRefused::{InvalidFlowId, UnmappedModel}`, `NativeTitle`: `crates/flow-nexus/src/title.rs:50-58` (excerpt 4.3)

#### 4.2 `NamesModel` and `model_display_name`

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/title.rs`, lines 9, 16-18, 24-26, 33-47

```rust
use signal_flow::{FlowAspect, LaunchProfile};
…
pub trait NamesModel {
    const MODEL_DISPLAY_NAMES: &'static [(&'static str, &'static str)] = &[
        ("gpt-6-astra", "Astra"),
…
        ("claude-fable-5-1", "Fable"),
        ("claude-fable-5-1[1m]", "Fable"),
        ("claude-opus-5-5", "Opus"),
…
        ("claude-haiku-4-5-20251001", "Haiku 4.5"),
    ];

    /// The display name of this exact model identifier.
    fn model_display_name(&self) -> Option<&'static str>;
}

impl NamesModel for str {
    fn model_display_name(&self) -> Option<&'static str> {
        Self::MODEL_DISPLAY_NAMES
            .iter()
            .find(|(identifier, _)| *identifier == self)
            .map(|(_, name)| *name)
    }
}
```

Declared elsewhere: `FlowAspect`, `LaunchProfile` (the `use` line), at
`signal-flow@f95034d:src/generated/signal.rs:73, 104`.

#### 4.3 `TitleRefused`, `NativeTitle`, `TitlesFlow`

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/title.rs`, lines 49-63

```rust
#[derive(Debug, Error, PartialEq, Eq)]
pub enum TitleRefused {
    #[error("unmapped exact native model identifier: {0}")]
    UnmappedModel(String),
    #[error("a title requires the exact six-character Flow ID")]
    InvalidFlowId,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct NativeTitle(String);

/// The title a launch profile gives the Flow it starts.
pub trait TitlesFlow {
    fn native_title(&self, flow_id: &str) -> Result<NativeTitle, TitleRefused>;
}
```

Declared elsewhere: `Error` (the derive macro and `#[error]`), crate
`thiserror` (`crates/flow-nexus/src/title.rs:10`).

#### 4.4 Where the title is applied

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/performing.rs`, lines 258-266; `crates/flow-nexus/src/herdr/launch.rs`, lines 1234-1262

```rust
            Operation::Title(Title_Data {
                composed_launch,
                native_launch_binding,
            }) => match self
                .herdr
                .title_native_flow(&composed_launch, &native_launch_binding)
            {
                Ok(_) => Outcome::Titled,
                Err(error) => HerdrFailure::refused(HerdrFailureStage::Title, error),
```

```rust
impl TitlesNativeFlow for HerdrCli {
    fn title_native_flow(
        &self,
        launch: &ComposedLaunch,
        binding: &NativeLaunchBinding,
    ) -> Result<NativeTitle, String> {
        launch.binding_matches_launch(&binding.herdr_pane_binding)?;
        if binding.launch_request_id != launch.launch_profile.launch_request_id
            || binding.harness_kind != launch.launch_profile.harness_kind
        {
            return Err("native binding does not belong to this launch".into());
        }
        let title = launch
            .launch_profile
            .native_title(&binding.flow_id)
            .map_err(|refusal| refusal.to_string())?;
        match binding.harness_kind {
            HarnessKind::Claude => self.title_claude_session(binding, &title)?,
            HarnessKind::Codex => self
                .codex_endpoints
                .adapter_for(&launch.launch_profile.model_name)
                .and_then(|adapter| {
                    adapter.name_bound_thread(&binding.native_session_id, title.as_str())
                })
                .map_err(|error| error.to_string())?,
        }
        self.label_herdr_pane(&binding.herdr_pane_binding, &title)?;
        Ok(title)
    }
```

Declared elsewhere:
- `Title_Data { composed_launch, native_launch_binding }`, `crates/flow-nexus/src/generated/operation.rs:59-62`
- `TitlesNativeFlow`, `crates/flow-nexus/src/herdr/launch.rs:66-72`
- `native_title`: excerpt 4.1. `as_str`: `ShowsNativeTitle`, `crates/flow-nexus/src/title.rs:88-90`
- `title_claude_session`, `label_herdr_pane`: `HerdrCli` methods in `crates/flow-nexus/src/herdr/launch.rs`. `adapter_for`, `name_bound_thread`: `crates/flow-nexus/src/codex.rs`

---

## 5. Replace

#### 5.1 `replace`: the decisive lines

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/launching.rs`, lines 425-435, 469-486

```rust
    fn replace(&self, request: StartRequest) -> Response {
        let refused = |rejection| Response::ReplaceRejected(rejection);
        let persistence = || {
            Response::ReplaceRejected(ReplaceRejection::LaunchRefused(
                StartRejection::LaunchPersistenceRefused,
            ))
        };
        let launch_request_id = request.launch_profile.launch_request_id.clone();
        let Some(predecessor) = request.launch_profile.flow_id_option.clone() else {
            return refused(ReplaceRejection::PredecessorAbsent);
        };
…
        match self.store.flow_node(&predecessor) {
            Ok(None) => return refused(ReplaceRejection::UnknownPredecessor),
            Ok(Some(node)) if node.flow_lifecycle == FlowLifecycle::Stopped => {
                return refused(ReplaceRejection::PredecessorStopped);
            }
            Ok(Some(_)) => {}
            Err(_) => return persistence(),
        }
        if self.perform(Operation::Record(Record_Data::Replacing(Replacement {
            launch_request_id: launch_request_id.clone(),
            predecessor,
        }))) != Outcome::Recorded
        {
            return persistence();
        }
        let response = self.start(request);
        Self::as_replacement(self.settle(&launch_request_id, response))
    }
```

Lines 436-468, which are left out, resume a replacement that is already
recorded and refuse a launch request that conflicts.

Declared elsewhere:
- `self`: `RunningNexus`, `crates/flow-nexus/src/lib.rs:68`
- `request.launch_profile.flow_id_option`: `pub flow_id_option: std::option::Option<FlowId>`, `signal-flow@f95034d:src/generated/signal.rs:113`. This field names the predecessor.
- `ReplaceRejection::{PredecessorAbsent, UnknownPredecessor, PredecessorStopped, LaunchRefused}`, `signal-flow@f95034d:src/generated/signal.rs:459-465`
- `self.store.flow_node`, `crates/flow-nexus/src/store.rs:825` (answers `Option<FlowNode>`)
- `FlowLifecycle::Stopped`: the wire `FlowLifecycle` (excerpt 5.4), imported at `crates/flow-nexus/src/launching.rs:31`
- `Record_Data::Replacing` (excerpt 5.6); `Replacement` (excerpt 5.3)
- `start` (excerpt 2.5), `settle` (excerpt 2.8b), `as_replacement` (`crates/flow-nexus/src/launching.rs:641-648`)

#### 5.2a `reap` (launching.rs:488): the predecessor stops first

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/launching.rs`, lines 488-515

```rust
    fn reap(&self, replacement: Replacement, launched: Launched) -> Response {
        let refuse = |rejection: ReplaceRejection| {
            let _ = self.perform(Self::settled_as(
                &replacement.launch_request_id,
                LaunchOutcome::ReplaceRejected(rejection.clone()),
            ));
            Response::ReplaceRejected(rejection)
        };
        let node = match self.store.flow_node(&replacement.predecessor) {
            Ok(Some(node)) => node,
            Ok(None) => return refuse(ReplaceRejection::UnknownPredecessor),
            Err(_) => {
                return refuse(ReplaceRejection::ReapRefused(
                    StopRejection::PersistenceRefused,
                ));
            }
        };
        // The predecessor stops receiving first: Stopped is what
        // ResolveRecipient and Deliver refuse.
        if node.flow_lifecycle != FlowLifecycle::Stopped
            && self.perform(Operation::Record(Record_Data::Stopped(
                replacement.predecessor.clone(),
            ))) != Outcome::Recorded
        {
            return refuse(ReplaceRejection::ReapRefused(
                StopRejection::PersistenceRefused,
            ));
        }
```


#### 5.2b `reap`: close the pane, record `Replaced`, continue the successor

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/launching.rs`, lines 520-532, 535-552

```rust
        match self.herdr.pane_presence(&node) {
            PanePresence::Absent => {}
            PanePresence::Unknown => {
                return refuse(ReplaceRejection::ReapRefused(
                    StopRejection::RouteUnavailable,
                ));
            }
            PanePresence::Present => {
                if self.perform(Operation::Close(node)) != Outcome::Closed {
                    return refuse(ReplaceRejection::ReapRefused(StopRejection::CloseRefused));
                }
            }
        }
…
        self.prune_launch_bundles_of(&replacement.predecessor);
        let replaced = Replaced {
            flow_id: replacement.predecessor.clone(),
            launched,
        };
        // The Replaced outcome is what releases the successor to routing.
        if self.perform(Self::settled_as(
            &replacement.launch_request_id,
            LaunchOutcome::Replaced(replaced.clone()),
        )) != Outcome::Recorded
        {
            return Response::ReplaceRejected(ReplaceRejection::ReapRefused(
                StopRejection::PersistenceRefused,
            ));
        }
        let _ = self.perform(Operation::Continue(replaced.launched.flow_id.clone()));
        Response::Replaced(replaced)
    }
```


Declared elsewhere:
- `self`: `RunningNexus`
- `Replacement { launch_request_id, predecessor }`, `crates/flow-nexus/src/store.rs:527-530` (excerpt 5.3)
- `Launched`, `Replaced { flow_id, launched }`: `signal-flow@f95034d:src/generated/signal.rs:392-396, 452-455`
- `settled_as`, `crates/flow-nexus/src/launching.rs:596` (impl :624-629: `Operation::Record(Record_Data::Settled(…))`)
- `LaunchOutcome::{ReplaceRejected, Replaced}`, `crates/flow-nexus/src/store.rs:479-484` (excerpt 5.3)
- `StopRejection::{PersistenceRefused, RouteUnavailable, CloseRefused}`, `signal-flow@f95034d:src/generated/signal.rs:436-442`
- `node.flow_lifecycle`, `FlowLifecycle::Stopped`: the wire type, excerpt 5.4
- `Record_Data::Stopped`: excerpt 5.6. `Operation::{Close, Continue}`, `Outcome::{Recorded, Closed}`: excerpt 2.3
- `pane_presence`: `ReadsHerdrPanes::pane_presence`, `crates/flow-nexus/src/herdr.rs:396`. `PanePresence::{Present, Absent, Unknown}`, `crates/flow-nexus/src/herdr.rs:41-51`
- `prune_launch_bundles_of`: `PrunesLaunchBundles`, `crates/flow-nexus/src/launching.rs:572-574`

#### 5.3 `LaunchOutcome` and `Replacement` (the store's own types)

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/store.rs`, lines 476-484, 524-530

```rust
/// How a launch request settled. It is kept beside the attempt so a
/// LaunchStatus or an Observe.Launch answers it without re-running the launch.
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq, Hash)]
pub enum LaunchOutcome {
    Started(Launched),
    Replaced(Replaced),
    StartRejected(StartRejection),
    ReplaceRejected(ReplaceRejection),
}
…
/// A launch request that replaces a predecessor. While it stands without a
/// Replaced outcome, the flow its launch binds is held out of routing.
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq, Hash)]
pub struct Replacement {
    pub launch_request_id: String,
    pub predecessor: String,
}
```

Declared elsewhere:
- `Archive`, `RkyvSerialize`, `RkyvDeserialize`: crate `rkyv`
- `Launched`, `Replaced`, `StartRejection`, `ReplaceRejection`: `signal-flow@f95034d:src/generated/signal.rs:392, 452, 408, 459`
- The generated Operation names them as `flow_nexus::LaunchOutcome` and `flow_nexus::Replacement`. That works because of `extern crate self as flow_nexus;` and `pub use store::{LaunchOutcome, Replacement};`, `crates/flow-nexus/src/lib.rs:5, 13`.

#### 5.4 `FlowLifecycle`: the wire one

`signal-flow` @ `f95034d` — `ethos/signal.ethos`, lines 189-190; `src/generated/signal.rs`, lines 368-374

```
  FlowLifecycle.[ Pending Active Stopped Retired Exited ]
  FlowNode.{ FlowId SessionId HarnessKind EndpointSelection HerdrRouteSelection OriginClue FlowLifecycle }
```

```rust
pub enum FlowLifecycle {
    Pending,
    Active,
    Stopped,
    Retired,
    Exited,
}
```

Declared elsewhere: none. For contrast, there are two other types with
the same name. The store has its own private `FlowLifecycle` with the same
five variants, at `crates/flow-nexus/src/store.rs:181-187`. That file
imports the wire type as `SignalFlowLifecycle`, at
`crates/flow-nexus/src/store.rs:25`. Separately,
`meta-signal-flow@54eb561:src/generated/signal.rs:151` declares
`FlowLifecycle` with the single variant `RegisteredUnconfirmed`.

#### 5.5 The store-private `FlowLifecycle` (for contrast)

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/store.rs`, lines 179-209

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
#[rkyv(derive(Debug))]
enum FlowLifecycle {
    Pending,
    Active,
    Stopped,
    Retired,
    Exited,
}

/// Whether a lifecycle on the wire still names a reachable seat.
///
/// Stopped, Exited and Retired are all gone, and each names who ended the
/// flow: Flow closed a pane it held, the seat's own pane went away, or an
/// owner retired it. None can be sent to, resolved as a recipient, stopped
/// or replaced, and none is a deletion.
pub trait NamesLiveFlow {
    fn is_live(&self) -> bool;
}

impl NamesLiveFlow for SignalFlowLifecycle {
    fn is_live(&self) -> bool {
        matches!(self, Self::Pending | Self::Active)
    }
}

impl NamesLiveFlow for FlowLifecycle {
    fn is_live(&self) -> bool {
        matches!(self, Self::Pending | Self::Active)
    }
}
```

Declared elsewhere: `SignalFlowLifecycle` is
`signal_flow::FlowLifecycle as SignalFlowLifecycle`
(`crates/flow-nexus/src/store.rs:25`), shown in excerpt 5.4.

#### 5.6 `Record_Data` (generated)

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/generated/operation.rs`, lines 20-23, 27-30, 34-48

```rust
pub struct Record_Data_Settled_Data {
    pub launch_request_id: signal_flow::LaunchRequestId,
    pub launch_outcome: flow_nexus::LaunchOutcome,
}
…
pub struct Record_Data_Harness_Data {
    pub flow_id: signal_flow::FlowId,
    pub event: signal_flow::Event,
}
…
pub enum Record_Data {
    Intent(signal_flow::NativeLaunchIntent),
    Binding(signal_flow::NativeLaunchBinding),
    Acknowledgement(signal_flow::RegistrationAcknowledgement),
    Delivery(signal_flow::PromptDeliveryIntent),
    Delivered(signal_flow::PromptDeliveryResult),
    Active(signal_flow::FlowId),
    Stopped(signal_flow::FlowId),
    Retired(signal_flow::FlowId),
    Exited(signal_flow::FlowId),
    Replacing(flow_nexus::Replacement),
    Withdrawn(signal_flow::LaunchRequestId),
    Settled(Record_Data_Settled_Data),
    Harness(Record_Data_Harness_Data),
}
```

Declared elsewhere (`signal_flow::X` in `signal-flow@f95034d:src/generated/signal.rs`):
- `LaunchRequestId` :25, `FlowId` :3, `Event` :545 (excerpt 1.8), `NativeLaunchIntent` :156, `NativeLaunchBinding` :167, `RegistrationAcknowledgement` :177, `PromptDeliveryIntent` :221, `PromptDeliveryResult` :250
- `flow_nexus::LaunchOutcome`, `flow_nexus::Replacement`: excerpt 5.3
- Source: `crates/flow-nexus/ethos/operation.ethos:34-47` (`Record.[ Intent.NativeLaunchIntent … Harness.{ FlowId Event } ]`)

---

## 6. Store

#### 6.1 `FlowEvents`: what Flow remembers of a harness

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/store/events.rs`, lines 1-12, 20, 25-36

```rust
//! What Flow remembers of each flow's harness: the events its hooks
//! reported, in the order Flow recorded them, one row per flow keyed by its
//! FlowId (the vision's Memory `Flow.{ FlowId Voice State Vector<Event> }`,
//! the events half). The row lives in its own table, so a store written
//! before events existed opens unchanged and its flows simply hold none.
//!
//! An event is recorded only for a flow Flow holds: a FlowId with no flow
//! row is refused, never adopted (ruling 12 of flow f1c841). Flow holds a
//! flow from the moment Reserve claims its FlowId, before its harness
//! starts and so before it is registered: Reserve writes the flow's empty
//! events row, and that row is what lets the harness's first `Started`
//! land.
…
use signal_flow::Event;
…
/// One flow's harness events, oldest first.
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub struct FlowEvents {
    pub flow_id: String,
    pub event_vector: Vec<Event>,
}

impl EngineRecord for FlowEvents {
    fn record_key(&self) -> RecordKey {
        RecordKey::new(self.flow_id.clone())
    }
}
```

Declared elsewhere:
- `Event`, `signal-flow@f95034d:src/generated/signal.rs:545-549` (excerpt 1.8)
- `EngineRecord`, `RecordKey`: crate `sema-engine`, `sema-engine@9884905:src/record.rs:149-151, 59`

#### 6.2 `record_event`: the store end of a Report

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/store/events.rs`, lines 108-139

```rust
impl RecordsHarnessEvents for FlowStore {
    fn record_event(&self, flow_id: &str, event: Event) -> Result<EventRecording, StoreError> {
        let _append = self
            .event_tables
            .append_gate
            .lock()
            .unwrap_or_else(|poisoned| poisoned.into_inner());
        let row = self.event_row(flow_id)?;
        if row.is_none() && self.flow(flow_id)?.is_none() {
            return Ok(EventRecording::UnknownFlow);
        }
        match row {
            Some(mut row) => {
                row.event_vector.push(event);
                self.engine.mutate_keyed(KeyedMutation::new(
                    self.event_tables.events,
                    RecordKey::new(flow_id),
                    row,
                ))?;
            }
            None => {
                self.engine.assert(Assertion::new(
                    self.event_tables.events,
                    FlowEvents {
                        flow_id: flow_id.into(),
                        event_vector: vec![event],
                    },
                ))?;
            }
        }
        Ok(EventRecording::Recorded)
    }
```

Declared elsewhere:
- `self`: `FlowStore`, `crates/flow-nexus/src/store.rs:614` (excerpt 6.5)
- `EventRecording::{Recorded, UnknownFlow}`, `crates/flow-nexus/src/store/events.rs:65-69`
- `RecordsHarnessEvents`, `crates/flow-nexus/src/store/events.rs:71-84` (`fn record_event(&self, flow_id: &str, event: Event) -> Result<EventRecording, StoreError>;` at :80)
- `self.event_tables.append_gate`, `.events`: `EventTables`, `crates/flow-nexus/src/store/events.rs:41-44`. The field `event_tables` is at `crates/flow-nexus/src/store.rs:628`.
- `event_row`: `ReadsEventRow`, `crates/flow-nexus/src/store/events.rs:86-88` (impl :90-106)
- `self.flow`, `crates/flow-nexus/src/store.rs:846` (`fn flow(&self, flow_id: &str) -> Result<Option<FlowRecord>, StoreError>;`)
- `self.engine`: `Engine`, `sema-engine@9884905:src/engine.rs:85`. `mutate_keyed`: :737. `assert`: :611. `KeyedMutation`, `Assertion` (`src/mutation.rs:9`), `RecordKey`: crate `sema-engine`
- `StoreError`, `crates/flow-nexus/src/store.rs:607-612`

#### 6.3 `Caller`: the role on the wire

`signal-flow` @ `f95034d` — `ethos/signal.ethos`, lines 210-212; `src/generated/signal.rs`, lines 501-506, 510-513

```
  Caller.{ FlowId FlowAspect PowerLevel ModelName }
  CallerResolutionRejection.[ CallerUnknown
                              CallerMismatch.Caller ]
```

```rust
pub struct Caller {
    pub flow_id: FlowId,
    pub flow_aspect: FlowAspect,
    pub power_level: PowerLevel,
    pub model_name: ModelName,
}
…
pub enum CallerResolutionRejection {
    CallerUnknown,
    CallerMismatch(Caller),
}
```

Declared elsewhere: `FlowId` :3, `FlowAspect` :73, `PowerLevel` :81,
`ModelName` :33 (all in `signal-flow@f95034d:src/generated/signal.rs`).

#### 6.4 `StoredRole` and where it is written

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/store.rs`, lines 217-228, 1268-1279

```rust
/// A flow's role: its aspect, power and model, keyed by its FlowId. It is
/// exactly what ResolveCaller answers, so the Caller is stored as it is.
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
struct StoredRole {
    caller: Caller,
}

impl EngineRecord for StoredRole {
    fn record_key(&self) -> RecordKey {
        RecordKey::new(self.caller.flow_id.clone())
    }
}
…
            if let Some(role) = role {
                match self.role(&flow_node.flow_id)? {
                    Some(existing) if existing != role => {
                        return Ok(FlowRegistration::ConflictingBinding);
                    }
                    Some(_) => {}
                    None => {
                        self.engine
                            .assert(Assertion::new(self.roles, StoredRole { caller: role }))?;
                    }
                }
            }
```

Declared elsewhere:
- `Caller`: excerpt 6.3
- `EngineRecord`, `RecordKey`, `Assertion`: crate `sema-engine`
- The second fragment is inside `register_flow_as`, `crates/flow-nexus/src/store.rs:1232`. It is reached from `register_flow_in_role` (`crates/flow-nexus/src/store.rs:722-726`, impl :1551-1561), which `Operation::Register` performs (excerpt 2.7).
- `self.roles: TableReference<StoredRole>`, `crates/flow-nexus/src/store.rs:624`. `self.role`: excerpt 6.7
- `FlowRegistration::{ConflictingBinding, Registered}`, `crates/flow-nexus/src/store.rs:649-652`

#### 6.5 `FlowStore`: the `self` of the store functions

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/store.rs`, lines 614-634

```rust
pub struct FlowStore {
    engine: Engine,
    flows: TableReference<FlowRecord>,
    state: TableReference<FlowStoreState>,
    configuration: TableReference<FlowStoreConfiguration>,
    runtime_configuration: TableReference<RuntimeConfiguration>,
    herdr_routes: TableReference<FlowHerdrRouteRecord>,
    launch_attempts: TableReference<StoredLaunchAttempt>,
    launch_outcomes: TableReference<StoredLaunchOutcome>,
    replacements: TableReference<Replacement>,
    roles: TableReference<StoredRole>,
    unread_launch_attempts: TableReference<UnreadLaunchAttempt>,
    quarantined_launch_attempts: TableReference<QuarantinedLaunchAttempt>,
    delivery_tables: DeliveryTables,
    event_tables: events::EventTables,
    pub launch_changes: LaunchChanges,
    /// What opening did with launch-attempt rows that no longer read in the
    /// current shape; each is also logged.
    pub opening_settlements: Vec<LaunchAttemptSettlement>,
}

```

Declared elsewhere:
- `Engine`, `TableReference`: `sema-engine@9884905:src/engine.rs:85`, `src/table.rs:225`
- `FlowRecord` `crates/flow-nexus/src/store.rs:168`; `FlowStoreState` :244; `FlowHerdrRouteRecord` :231; `StoredLaunchOutcome` :513; `Replacement` :527; `StoredRole` :220; `DeliveryTables` `crates/flow-nexus/src/store/delivery.rs`; `events::EventTables` `crates/flow-nexus/src/store/events.rs:41`; the rest are in `crates/flow-nexus/src/store.rs`

#### 6.6a ResolveCaller: from the socket to `resolve_caller`

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/lib.rs`, lines 497-503; `crates/flow-nexus/src/caller.rs`, lines 30-35, 109-128

```rust
            // The caller is the peer of this connection, read from the kernel.
            Query::ResolveCaller(claim) => nexus.resolve_caller(
                self.peer
                    .peer_process()
                    .and_then(|process| process.caller_pane()),
                claim,
            ),
```

```rust
/// The Herdr pane a process runs in, as Herdr marked it.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CallerPane {
    pub herdr_session_name: String,
    pub herdr_pane_id: String,
}
…
/// Answers ResolveCaller for the pane a connection's peer runs in.
pub trait ResolvesCaller {
    fn resolve_caller(&self, pane: Option<CallerPane>, claim: Option<FlowId>) -> Response;
}

impl ResolvesCaller for RunningNexus {
    fn resolve_caller(&self, pane: Option<CallerPane>, claim: Option<FlowId>) -> Response {
        let caller = pane
            .ok_or(CallerResolutionRejection::CallerUnknown)
            .and_then(|pane| self.bound_caller(&pane));
        match (caller, claim) {
            (Err(rejection), _) => Response::CallerResolutionRejected(rejection),
            (Ok(caller), Some(claimed)) if claimed != caller.flow_id => {
                Response::CallerResolutionRejected(CallerResolutionRejection::CallerMismatch(
                    caller,
                ))
            }
            (Ok(caller), _) => Response::CallerResolved(caller),
        }
    }
```


#### 6.6b `bound_caller`: the one flow a pane holds

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/caller.rs`, lines 131-154

```rust
/// The one flow a pane holds, with its role.
trait BindsCallerPane {
    fn bound_caller(&self, pane: &CallerPane) -> Result<Caller, CallerResolutionRejection>;
}

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


Declared elsewhere:
- `self` (caller.rs impls): `RunningNexus`, `crates/flow-nexus/src/lib.rs:68`
- `self.peer.peer_process()`: `IdentifiesPeer::peer_process`, `crates/flow-nexus/src/caller.rs:39` (impl :43)
- `caller_pane`: `LocatesCallerPane::caller_pane`, `crates/flow-nexus/src/caller.rs:92`. It reads `HERDR_SESSION` and `HERDR_PANE_ID` from `/proc`.
- `FlowId`, `Caller`, `CallerResolutionRejection::{CallerUnknown, CallerMismatch}`, `Response::{CallerResolved, CallerResolutionRejected}`: `signal-flow@f95034d:src/generated/signal.rs:3, 501, 510, 582`
- `self.store.flows_in_pane`, `self.store.role`: `ReadsFlowRoles`, `crates/flow-nexus/src/store.rs:740-748` (excerpt 6.7)
- `self.herdr.pane_presence`, `PanePresence::Present`: `crates/flow-nexus/src/herdr.rs:396, 41`
- `StoreError`, `crates/flow-nexus/src/store.rs:607`
- `FlowNode`, `signal-flow@f95034d:src/generated/signal.rs:378`

#### 6.7a The store function that answers ResolveCaller: `role`

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/store.rs`, lines 738-748, 1587-1599

```rust
/// The role each flow was bound or launched in, and the flows a Herdr pane
/// holds: what ResolveCaller reads.
pub trait ReadsFlowRoles {
    fn role(&self, flow_id: &str) -> Result<Option<Caller>, StoreError>;
    /// The routable flows whose recorded route names this session and pane.
    fn flows_in_pane(
        &self,
        herdr_session_name: &str,
        herdr_pane_id: &str,
    ) -> Result<Vec<FlowNode>, StoreError>;
}
…
impl ReadsFlowRoles for FlowStore {
    fn role(&self, flow_id: &str) -> Result<Option<Caller>, StoreError> {
        let records = self
            .engine
            .match_records(QueryPlan::key(self.roles, RecordKey::new(flow_id)))?
            .records()
            .to_vec();
        match records.as_slice() {
            [] => Ok(None),
            [role] => Ok(Some(role.caller.clone())),
            _ => Err(StoreError::StateInvariant),
        }
    }
```


#### 6.7b `flows_in_pane`: the live, routable flows of one pane

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/store.rs`, lines 1601-1621

```rust
    fn flows_in_pane(
        &self,
        herdr_session_name: &str,
        herdr_pane_id: &str,
    ) -> Result<Vec<FlowNode>, StoreError> {
        let mut nodes = Vec::new();
        for node in self.flow_nodes()? {
            let HerdrRouteSelection::Available(route) = &node.herdr_route_selection else {
                continue;
            };
            if route.herdr_session_name != herdr_session_name
                || route.herdr_pane_id != herdr_pane_id
                || !node.flow_lifecycle.is_live()
                || self.held_successor(&node.flow_id)?
            {
                continue;
            }
            nodes.push(node);
        }
        Ok(nodes)
    }
```


Declared elsewhere:
- `self`: `FlowStore`, `crates/flow-nexus/src/store.rs:614` (excerpt 6.5)
- `self.engine.match_records`: `sema-engine@9884905:src/engine.rs:1128`. `QueryPlan::key`: `sema-engine@9884905:src/query.rs:40`. `RecordKey`: `src/record.rs:59`
- `self.roles`, `crates/flow-nexus/src/store.rs:624`. `role.caller`: `StoredRole`, `crates/flow-nexus/src/store.rs:220-222` (excerpt 6.4)
- `StoreError::StateInvariant`, `crates/flow-nexus/src/store.rs:611`
- `self.flow_nodes`, `crates/flow-nexus/src/store.rs:826`. `self.held_successor`, :812 (a successor whose `Replacement` has no `Replaced` outcome yet)
- `HerdrRouteSelection::Available`, `route.{herdr_session_name, herdr_pane_id}`: `signal-flow@f95034d:src/generated/signal.rs:361, 352-357`
- `is_live`: `NamesLiveFlow`, `crates/flow-nexus/src/store.rs:195-203` (excerpt 5.5)

---

## 7. Messenger

There are two messengers. **messenger-clj**, which runs the `hm-*`
commands, keeps its own route store and types into Herdr itself. It never
asks Flow anything. The Rust **Message Nexus** asks Flow who the sender is,
through `ResolvePeer`. It also hands every pane write to Flow, through `Vet`
and `Deliver`.

### messenger-clj

#### 7.1 `RouteBinding` and the message schemas

`messenger-clj` @ `85e71b1` — `src/messenger_clj/core.clj`, lines 17, 19-21, 28-32

```clojure
(def FlowId [:and [:string {:min 1 :max 96}] [:re #"^[A-Za-z0-9][A-Za-z0-9_-]*$"]])
…
(def MessageBody [:string {:min 1}])
(def MessageVariant [:enum :msg :psyche :psyches])
(def RouteBinding [:map {:closed true} [:session :string] [:name :string] [:pane_id :string] [:terminal_id :string] [:agent :string] [:native_thread {:optional true} NativeThread] [:route_hold {:optional true} :string] [:transition {:optional true} :boolean] [:state {:optional true} :string]])
…
(def PaneMessage [:tuple FlowId MessageBody])
(def PsycheMessage [:tuple FlowId MessageBody MessageBody])
(def PsychesMessage [:vector {:min 1} PsycheMessage])
(def PsychesInput [:vector {:min 1} [:tuple MessageBody MessageBody]])
(def MessageRequest [:map {:closed true} [:variant MessageVariant] [:body MessageBody] [:context {:optional true} [:maybe MessageBody]]])
```

Declared elsewhere: `NativeThread` is on line 18, which is cut. It reads
`(def NativeThread [:and [:string {:min 16 :max 96}] [:re #"^[A-Za-z0-9][A-Za-z0-9-]+$"]])`.
The schema vocabulary (`:map`, `:tuple`, `:enum`, …) is from the library
`malli.core`, required as `m` at `src/messenger_clj/core.clj:12`.

#### 7.2 `message-envelope`: the sender is the first field

`messenger-clj` @ `85e71b1` — `src/messenger_clj/core.clj`, lines 161-175

```clojure
(defn message-envelope [sender request]
  (flow-id! sender)
  (let [{:keys [variant context body]} (request! request)
        [tag value reader] (case variant
                             :msg ["#msg" (read-msg [sender body]) read-pane-message]
                             :psyche ["#psyche" (read-psyche [sender context body]) read-psyche-message]
                             :psyches ["#psyches"
                                       (read-psyches (mapv (fn [[record-context verbatim]]
                                                             [sender record-context verbatim])
                                                           (read-psyches-input body)))
                                       read-psyches-message])
        envelope (str tag " " (pr-str value))]
    (when-not (= value (reader envelope))
      (fail (str tag " EDN round trip failed; message held")))
    envelope))
```

Declared elsewhere (all `src/messenger_clj/core.clj`):
- `flow-id!` :42-45; `request!` :150-160; `read-msg` :120-123; `read-psyche` :124-125; `read-psyches` :126-127; `read-psyches-input` :148-149; `read-pane-message` :136-139; `read-psyche-message` :140-143; `read-psyches-message` :144-147; `fail` :35
- `sender` is supplied by the caller. In `send-request!` it is `(or *flow-id* (System/getenv "FLOW_ID") …)`, at `src/messenger_clj/core.clj:906` (excerpt 7.5). `*flow-id*` is at :101.

#### 7.3 `read-route`: the messenger's own route store

`messenger-clj` @ `85e71b1` — `src/messenger_clj/core.clj`, lines 84, 96-99, 112-117, 191-196; `src/messenger_clj/typed_store.clj`, lines 216-217

```clojure
(defprotocol Registry (load-route [this flow]) (save-route! [this flow route]))
…
(defrecord DatalevinRegistry [state-root]
  Registry
  (load-route [_ flow] (store/route-for state-root (flow-id! flow)))
  (save-route! [_ flow route] (store/put-route! state-root (flow-id! flow) (route-binding! route))))
…
(defn root []
  ;; The deployment migrates the typed database here while holding both state
  ;; roots and replacing every launcher in the same activation.
  (fs/absolutize (or *root* (System/getenv "HM_REGISTRY")
                     (str (fs/path (System/getProperty "user.home") ".local/state/messenger-clj")))))
(defn registry [] (or *registry* (->DatalevinRegistry (root))))
…
(defn read-route [flow]
  (try
    (if-let [route (load-route (registry) flow)]
      (route-binding! route)
      (fail (str "No valid registration for " flow)))
    (catch Exception e (fail (str "No valid registration for " flow ": " (.getMessage e))))))
```

```clojure
(defn route-for [root flow]
  (when-not (retirement-for root flow) (stored-route-for root flow)))
```

Declared elsewhere:
- `store/route-for`: `src/messenger_clj/typed_store.clj:216` (shown). `store/put-route!`: `src/messenger_clj/typed_store.clj:200`. `stored-route-for` :208; `retirement-for` :361.
- `route-binding!` `src/messenger_clj/core.clj:73-79`; `flow-id!` :42; `fail` :35; `*root*`, `*registry*` :100, :103
- `fs/absolutize`, `fs/path`: library `babashka.fs`

#### 7.4 The function that types into the Herdr pane

`messenger-clj` @ `85e71b1` — `src/messenger_clj/core.clj`, lines 219-224, 235-258, 266-267, 274

```clojure
(defn herdr-prompt-request [route envelope wait-presented]
  {:id "messenger-clj:agent:prompt"
   :method "agent.prompt"
   :params (cond-> {:target (:pane_id route) :text envelope}
             wait-presented (assoc :wait {:until ["working" "idle" "done" "blocked"]
                                           :timeout_ms 10000}))})
…
(defn herdr-socket-request! [session request]
  (let [request (ensure-herdr-request-fits! request)
        socket-path (herdr-socket-path session)]
    (try
      (with-open [channel (SocketChannel/open (UnixDomainSocketAddress/of socket-path))
                  writer (OutputStreamWriter. (Channels/newOutputStream channel) StandardCharsets/UTF_8)
                  reader (BufferedReader. (InputStreamReader. (Channels/newInputStream channel) StandardCharsets/UTF_8))]
        (.write writer ^String (herdr-request-line request))
        (.write writer "\n")
        (.flush writer)
        (let [line (.readLine reader)]
          (when (str/blank? line)
            (fail "Herdr socket returned an empty response; do not blindly retry a send"))
          (let [reply (json/parse-string line true)]
            (when (:error reply) (fail (str "Herdr: " (:error reply))))
            (let [result (or (:result reply) reply)]
              (when-not (map? result)
                (fail "Herdr socket returned malformed result; do not blindly retry a send"))
              result))))
      (catch clojure.lang.ExceptionInfo error (throw error))
      (catch Exception error
        (fail (str "Herdr socket request failed or is uncertain: " (.getMessage error)))))))
(defn direct-prompt! [route envelope wait-presented]
  (herdr-socket-request! (:session route) (herdr-prompt-request route envelope wait-presented)))
…
(defrecord ShellHerdr []
  HerdrTransport
…
  (prompt!* [_ route envelope wait?] (direct-prompt! route envelope wait?)))
```

Declared elsewhere (all `src/messenger_clj/core.clj`):
- `HerdrTransport` (protocol, with `prompt!*` at :92), :85-92
- `herdr-request-line` :225-226; `ensure-herdr-request-fits!` :229-234; `herdr-socket-path` :211-218 (asks `herdr session list --json` for the session's `socket_path`)
- `route`: a `RouteBinding` map (excerpt 7.1). `:session`, `:pane_id` are its keys.
- `json/generate-string`, `json/parse-string`: library `cheshire.core`. `SocketChannel`, `UnixDomainSocketAddress`, `Channels`, `OutputStreamWriter`, `BufferedReader`, `InputStreamReader`, `StandardCharsets`: JDK, imported at :2-5

#### 7.5 `send-request!`: the sender, the route, the envelope, the prompt

`messenger-clj` @ `85e71b1` — `src/messenger_clj/core.clj`, lines 901-911, 924-926, 937-942

```clojure
(defn send-request!
  ([flow request wait-presented pane] (send-request! flow request wait-presented pane 10))
  ([flow request wait-presented pane hold-seconds]
   (flow-id! flow)
   (let [request (validate-request! request)]
   (let [sender (or *flow-id* (System/getenv "FLOW_ID") (fail "Set FLOW_ID to your own flow ID before sending"))]
     (with-reservation flow
       (fn []
         (assert-not-retired! flow)
         (let [raw-stored (try (load-route (registry) flow) (catch Exception _ nil))
               stored (try (when raw-stored (route-binding! raw-stored)) (catch Exception _ nil))]
…
                 route (refresh-route-snapshot route live)
                 envelope (message-envelope sender request)
                 _ (try (prompt-request! route envelope wait-presented)
…
             (try
               (let [waited? wait-presented
                     reply (prompt!* (transport) route envelope waited?)]
                 (when waited? (presented! route reply)))
               (verify-target! route)
               (record-sent! flow grade route submission live request envelope)
```

Declared elsewhere (all `src/messenger_clj/core.clj`):
- `flow-id!` :42; `*flow-id*` :101; `fail` :35; `load-route` / `registry` :84 / :117 (excerpt 7.3); `route-binding!` :73; `message-envelope` :161 (excerpt 7.2); `prompt!*` / `transport` :92 / :275 (excerpt 7.4); `presented!` :259-265
- `validate-request!` :836; `with-reservation` :476 (the Orchestrate lock; it uses `reserve!`, :446-475, which shells out to `orchestrate`); `assert-not-retired!` :289; `refresh-route-snapshot` :352; `verify-target!` :319; `prompt-request!` :382 (checks the request against Herdr's size limit; it does not send); `record-sent!` :892
- `live` (:918), `submission` (:931) and `grade` (:936) are bound in the lines that are cut.

### The Rust Message Nexus

#### 7.6 `peer.rs`: the sender is read from the kernel

`message` @ `6fa4d0c` — `crates/message-nexus/src/peer.rs`, lines 1-31

```rust
//! The process at the other end of a connection, as the kernel names it.
//!
//! Message never takes a sender from a payload. It reads its peer's
//! credentials (`SO_PEERCRED`) and the process's start time, and asks Flow
//! (`ResolvePeer`) which flow that exact process runs in. The start time
//! makes the identity name one process, never a reused process ID.

use meta_signal_flow::ProcessIdentity;
use std::{fs, os::unix::net::UnixStream};

/// Names the peer process of a connection.
pub trait IdentifiesPeer {
    fn peer_identity(&self) -> Option<ProcessIdentity>;
}

impl IdentifiesPeer for UnixStream {
    fn peer_identity(&self) -> Option<ProcessIdentity> {
        let credentials = rustix::net::sockopt::socket_peercred(self).ok()?;
        let process_id = i64::from(credentials.pid.as_raw_nonzero().get());
        let process_user_id = i64::from(credentials.uid.as_raw());
        let stat = fs::read_to_string(format!("/proc/{process_id}/stat")).ok()?;
        // Field 22 of /proc/<pid>/stat, counted after the command name.
        let (_, fields) = stat.rsplit_once(") ")?;
        let process_start_token = fields.split_whitespace().nth(19)?.to_owned();
        Some(ProcessIdentity {
            process_id,
            process_user_id,
            process_start_token,
        })
    }
}
```

Declared elsewhere:
- `self`: `UnixStream` (std)
- `ProcessIdentity { process_id, process_user_id, process_start_token }`, `meta-signal-flow@54eb561:src/generated/signal.rs:133-137` (`ProcessId`/`ProcessUserId` are `i64`, :125/:127; `ProcessStartToken` is `String`, :129)
- `rustix::net::sockopt::socket_peercred`: crate `rustix`

#### 7.7 `Sender`, `Content`, `Letter`, `Message`, `DeliveryRequest` in the contract source

`meta-signal-flow` @ `54eb561` — `ethos/signal.ethos`, lines 121-122, 125-135

```
  DeliveryId.String
  MessageId.String
…
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
```

Declared elsewhere: `FlowId`, imported from signal-flow on
`meta-signal-flow@54eb561:ethos/signal.ethos:40`.

#### 7.8 The same types, generated

`meta-signal-flow` @ `54eb561` — `src/generated/signal.rs`, lines 242-244, 252-255, 263-266, 270-273, 277-281, 285-289, 293-297

```rust
pub type DeliveryId = String;
#[rustfmt::skip]
pub type MessageId = String;
…
pub enum Sender {
    Flow(signal_flow::FlowId),
    Owner,
}
…
pub struct Psyche_Data {
    pub psyche_context: PsycheContext,
    pub psyche_verbatim: PsycheVerbatim,
}
…
pub enum Content {
    Text(String),
    Psyche(Psyche_Data),
}
…
pub struct Letter {
    pub message_id: MessageId,
    pub sender: Sender,
    pub content: Content,
}
…
pub enum Message {
    HardAbrupt(Letter),
    MiddleAbrupt(Letter),
    Soft(Letter),
}
…
pub struct DeliveryRequest {
    pub delivery_id: DeliveryId,
    pub flow_id: signal_flow::FlowId,
    pub message: Message,
}
```

Declared elsewhere: `signal_flow::FlowId`,
`signal-flow@f95034d:src/generated/signal.rs:3`. `PsycheContext` and
`PsycheVerbatim` are `pub type … = String;` at :257 and :259.

#### 7.9 `Deliver`, `Vet`, `ResolvePeer`: request and reply declarations

`meta-signal-flow` @ `54eb561` — `ethos/signal.ethos`, lines 39-41, 46-50, 61-63, 66-67; `src/generated/signal.rs`, lines 400, 406-411, 429, 440-442, 445-446, 450

```
Signal
[ signal_flow:[ FlowNode FlowId FlowAspect PowerLevel ModelName HarnessKind NativeSessionId HerdrSessionName HerdrAgentName HerdrWorkspaceId HerdrPaneId HerdrTerminalId Caller CallerResolutionRejection Event ] ]
[ Configure.ConfigureRequest
…
  Deliver.DeliveryRequest
  Vet.DeliveryRequest
  Command.CommandRequest
  ResolvePeer.ProcessIdentity
  ReadEvents.FlowId ]
…
  Delivered.Delivery
  DeliveryRejected.DeliveryRejection
  Vetted.FlowId
…
  PeerResolved.Caller
  PeerResolutionRejected.CallerResolutionRejection
```

```rust
pub enum Query {
…
    Deliver(DeliveryRequest),
    Vet(DeliveryRequest),
    Command(CommandRequest),
    ResolvePeer(ProcessIdentity),
    ReadEvents(signal_flow::FlowId),
}
…
pub enum Response {
…
    Delivered(Delivery),
    DeliveryRejected(DeliveryRejection),
    Vetted(signal_flow::FlowId),
…
    PeerResolved(signal_flow::Caller),
    PeerResolutionRejected(signal_flow::CallerResolutionRejection),
…
}
```

Declared elsewhere:
- `DeliveryRequest` (excerpt 7.8); `ProcessIdentity` `meta-signal-flow@54eb561:src/generated/signal.rs:133`; `Delivery` :317-322; `DeliveryRejection` :334-346; `CommandRequest` :357
- `signal_flow::Caller`, `signal_flow::CallerResolutionRejection`, `signal_flow::FlowId`: `signal-flow@f95034d:src/generated/signal.rs:501, 510, 3` (excerpt 6.3)

#### 7.10 The code that calls Flow: `FlowEdge`

`message` @ `6fa4d0c` — `crates/message-nexus/src/flow_edge.rs`, lines 1-6, 32-41, 45-47, 51-60

```rust
//! The Message→Flow edge.
//!
//! Message is a client of Flow's meta socket (ResolvePeer, Vet, Deliver) and
//! of its ordinary socket (Observe.Agent). Flow is the only pane writer:
//! Message hands it a typed Deliver addressed by FlowId and never runs
//! Herdr, never resolves a pane, never types.
…
/// Whom Flow says a peer process is.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PeerName {
    /// The process runs in this flow's pane.
    Flow(Caller),
    /// The process runs in no flow's pane: the owner.
    NotAFlow,
    /// Flow knows the process's pane but not as the flow it names.
    Mismatched,
}
…
pub struct FlowEdge {
    pub flow_socket_path: String,
    pub flow_meta_socket_path: String,
…
pub trait CallsFlowMeta {
    fn resolve_peer(&self, identity: ProcessIdentity) -> Result<PeerName, EdgeFailure>;
    fn vet(
        &self,
        request: DeliveryRequest,
    ) -> Result<Result<FlowId, DeliveryRejection>, EdgeFailure>;
    fn deliver(
        &self,
        request: DeliveryRequest,
    ) -> Result<Result<Delivery, DeliveryRejection>, EdgeFailure>;
```

Declared elsewhere:
- `Caller`, `FlowId`: signal-flow (excerpt 6.3). `ProcessIdentity`, `DeliveryRequest`, `DeliveryRejection`, `Delivery`: meta-signal-flow (excerpts 7.6-7.9)
- `EdgeFailure`, `crates/message-nexus/src/flow_edge.rs:21-30`

#### 7.11a The code that calls Flow: one exchange over the meta socket

`message` @ `6fa4d0c` — `crates/message-nexus/src/flow_edge.rs`, lines 73-86

```rust
impl ExchangesWithFlowMeta for FlowEdge {
    fn meta_exchange(&self, query: &MetaQuery) -> Result<MetaResponse, EdgeFailure> {
        let mut stream = UnixStream::connect(&self.flow_meta_socket_path)
            .map_err(|_| EdgeFailure::Unreachable)?;
        stream
            .write_frame(query)
            .map_err(|_| EdgeFailure::Unreachable)?;
        match stream.read_frame::<MetaResponse>() {
            Ok(MetaResponse::MetaRefused(refusal)) => Err(EdgeFailure::Refused(refusal)),
            Ok(response) => Ok(response),
            Err(_) => Err(EdgeFailure::Broken),
        }
    }
}
```


#### 7.11b The code that calls Flow: ResolvePeer, Vet, Deliver

`message` @ `6fa4d0c` — `crates/message-nexus/src/flow_edge.rs`, lines 88-100, 102-111, 113-122

```rust
impl CallsFlowMeta for FlowEdge {
    fn resolve_peer(&self, identity: ProcessIdentity) -> Result<PeerName, EdgeFailure> {
        match self.meta_exchange(&MetaQuery::ResolvePeer(identity))? {
            MetaResponse::PeerResolved(caller) => Ok(PeerName::Flow(caller)),
            MetaResponse::PeerResolutionRejected(CallerResolutionRejection::CallerUnknown) => {
                Ok(PeerName::NotAFlow)
            }
            MetaResponse::PeerResolutionRejected(CallerResolutionRejection::CallerMismatch(_)) => {
                Ok(PeerName::Mismatched)
            }
            _ => Err(EdgeFailure::Unexpected),
        }
    }
…
    fn vet(
        &self,
        request: DeliveryRequest,
    ) -> Result<Result<FlowId, DeliveryRejection>, EdgeFailure> {
        match self.meta_exchange(&MetaQuery::Vet(request))? {
            MetaResponse::Vetted(flow_id) => Ok(Ok(flow_id)),
            MetaResponse::DeliveryRejected(rejection) => Ok(Err(rejection)),
            _ => Err(EdgeFailure::Unexpected),
        }
    }
…
    fn deliver(
        &self,
        request: DeliveryRequest,
    ) -> Result<Result<Delivery, DeliveryRejection>, EdgeFailure> {
        match self.meta_exchange(&MetaQuery::Deliver(request))? {
            MetaResponse::Delivered(delivery) => Ok(Ok(delivery)),
            MetaResponse::DeliveryRejected(rejection) => Ok(Err(rejection)),
            _ => Err(EdgeFailure::Unexpected),
        }
    }
```


Declared elsewhere:
- `self`: `FlowEdge`, `crates/message-nexus/src/flow_edge.rs:45-48` (excerpt 7.10)
- `ExchangesWithFlowMeta`, `crates/message-nexus/src/flow_edge.rs:69-71`. `CallsFlowMeta`: excerpt 7.10
- `MetaQuery`, `MetaResponse`: `meta_signal_flow::Query as MetaQuery`, `Response as MetaResponse`, imported at `crates/message-nexus/src/flow_edge.rs:9-12`. Declared at `meta-signal-flow@54eb561:src/generated/signal.rs:400, 429` (excerpt 7.9)
- `MetaResponse::MetaRefused`, `meta-signal-flow@54eb561:src/generated/signal.rs:447`. `MetaRefusal` :393-396
- `write_frame`, `read_frame`: `FramedStream`, `crates/message-nexus/src/frame.rs:32-45`
- `PeerName`, `EdgeFailure`: `crates/message-nexus/src/flow_edge.rs:34-41, 21-30`

#### 7.12 Who the sender is: `peer_flow`, and the Sender it becomes

`message` @ `6fa4d0c` — `crates/message-nexus/src/service.rs`, lines 22-48; `crates/message-nexus/src/listener.rs`, lines 121-125

```rust
/// Whom a connection's peer is, as a message's sender or recipient.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PeerFlow {
    Flow(FlowId),
    NotAFlow,
    FlowUnreachable,
}

pub trait NamesPeerFlow {
    fn peer_flow(&self, identity: Option<ProcessIdentity>) -> PeerFlow;
}

impl NamesPeerFlow for MessageNexus {
    fn peer_flow(&self, identity: Option<ProcessIdentity>) -> PeerFlow {
        let Some(identity) = identity else {
            return PeerFlow::NotAFlow;
        };
        let Ok(edge) = self.flow_edge() else {
            return PeerFlow::FlowUnreachable;
        };
        match edge.resolve_peer(identity) {
            Ok(PeerName::Flow(caller)) => PeerFlow::Flow(caller.flow_id),
            Ok(PeerName::NotAFlow | PeerName::Mismatched) => PeerFlow::NotAFlow,
            Err(_) => PeerFlow::FlowUnreachable,
        }
    }
}
```

```rust
        let query = stream.read_frame::<Query>()?;
        let peer = || self.peer_flow(stream.peer_identity());
        let response = match query {
            Query::Send(request) => match peer() {
                PeerFlow::Flow(flow_id) => match self.send(Sender::Flow(flow_id), request) {
```

Declared elsewhere:
- `self` (service.rs impl): `MessageNexus`, `crates/message-nexus/src/nexus.rs:27-40`. `flow_edge`: `HoldsNexusState::flow_edge`, `crates/message-nexus/src/nexus.rs:84` (impl :104-110)
- `resolve_peer`, `PeerName`: excerpts 7.10-7.11
- `FlowId`: signal-flow :3. `ProcessIdentity`: meta-signal-flow :133. `Sender::Flow`: excerpt 7.8 (the meta socket's `MetaQuery::Send` uses `Sender::Owner`, `crates/message-nexus/src/listener.rs:184`)
- `peer_identity`: excerpt 7.6. `self.send`: `ServesMessages::send`, `crates/message-nexus/src/service.rs:52-56`

#### 7.13 The Letter and DeliveryRequest Message builds; where it vets and delivers

`message` @ `6fa4d0c` — `crates/message-nexus/src/delivery.rs`, lines 39-60, 150-155; `crates/message-nexus/src/service.rs`, lines 127-131

```rust
impl RequestsFlowDelivery for MessageRecord {
    fn flow_message(&self) -> Message {
        let letter = Letter {
            message_id: self.message_id.clone(),
            sender: self.sender.clone(),
            content: self.content.clone(),
        };
        match self.priority {
            Priority::HardAbrupt => Message::HardAbrupt(letter),
            Priority::MiddleAbrupt => Message::MiddleAbrupt(letter),
            Priority::Soft => Message::Soft(letter),
        }
    }

    fn delivery_request(&self, delivery_id: DeliveryId, flow_id: &str) -> DeliveryRequest {
        DeliveryRequest {
            delivery_id,
            flow_id: flow_id.to_owned(),
            message: self.flow_message(),
        }
    }
}
…
        let request = message.delivery_request(delivery_id.clone(), &addressee.flow_id);
        let grading = match self.flow_edge() {
            Ok(edge) => edge.deliver(request),
            Err(_) => Err(EdgeFailure::Unreachable),
        }
        .grading(delivery_id);
```

```rust
        for addressee in &addressees {
            let request = message.delivery_request(addressee.delivery_id(0), &addressee.flow_id);
            match edge.vet(request) {
                Ok(Ok(_)) => {}
                Ok(Err(DeliveryRejection::UnknownFlow)) => {
```

Declared elsewhere:
- `self` (delivery.rs impl): `MessageRecord`, `message@6fa4d0c:crates/message-nexus/src/store.rs:38-45` (`message_id: MessageId`, `sender: Sender`, `flow_id_vector: Vec<FlowId>`, `priority: Priority`, `content: Content`, `stamped_at: i64`)
- `RequestsFlowDelivery`, `crates/message-nexus/src/delivery.rs:30-37`
- `Letter`, `Message`, `DeliveryRequest`, `DeliveryId`: excerpt 7.8
- `Priority::{HardAbrupt, MiddleAbrupt, Soft}`, `signal-message@b94d907:src/generated/signal.rs:5-9`. `MessageId` is a re-export of `meta_signal_flow::MessageId`, `signal-message@b94d907:src/lib.rs:22`
- `edge.deliver`, `edge.vet`: excerpt 7.11. `grading`: `Grading`, `crates/message-nexus/src/ledger.rs`
- `addressee`: `Addressee { message_id, flow_id }`, `crates/message-nexus/src/nexus.rs:22-25`. `delivery_id`: `AddressesAttempts`, `crates/message-nexus/src/delivery.rs:63-65`

#### 7.14 Flow's side of the three calls

`flow` @ `5e0b1bf` — `crates/flow-nexus/src/lib.rs`, lines 384-387; `crates/flow-nexus/src/peer.rs`, lines 23-47

```rust
            meta_signal_flow::Query::Deliver(request) => self.deliver(request),
            meta_signal_flow::Query::Vet(request) => self.vet(&request),
            meta_signal_flow::Query::Command(request) => self.command(request),
            meta_signal_flow::Query::ResolvePeer(identity) => self.resolve_peer(&identity),
```

```rust
/// Names the flow a process runs in.
pub trait ResolvesPeer {
    fn resolve_peer(&self, identity: &ProcessIdentity) -> Response;
}

impl ResolvesPeer for RunningNexus {
    fn resolve_peer(&self, identity: &ProcessIdentity) -> Response {
        // The identity must still name the same live process (user and start
        // time), so a reused process ID names no one.
        if !identity.is_live_process() {
            return Response::PeerResolutionRejected(CallerResolutionRejection::CallerUnknown);
        }
        let Ok(process_id) = u32::try_from(identity.process_id) else {
            return Response::PeerResolutionRejected(CallerResolutionRejection::CallerUnknown);
        };
        let pane = CallerProcess { process_id }.caller_pane();
        match self.resolve_caller(pane, None) {
            signal_flow::Response::CallerResolved(caller) => Response::PeerResolved(caller),
            signal_flow::Response::CallerResolutionRejected(rejection) => {
                Response::PeerResolutionRejected(rejection)
            }
            _ => Response::PeerResolutionRejected(CallerResolutionRejection::CallerUnknown),
        }
    }
}
```

Declared elsewhere:
- `self`: `RunningNexus`, `crates/flow-nexus/src/lib.rs:68`
- `deliver`, `vet`, `command`: `DeliversMessages`, `crates/flow-nexus/src/delivery.rs:190-194` (impl from :196). Flow renders the `Message` as its own datom into the pane: `RendersPaneText::pane_text`, `crates/flow-nexus/src/delivery/body.rs:45-55`
- `is_live_process`, a `ProcessIdentity` trait method, `crates/flow-nexus/src/binding.rs:17` (impl :23). `CallerProcess`, `caller_pane`: `crates/flow-nexus/src/caller.rs:26, 92`
- `resolve_caller`: excerpt 6.6. `Response::{PeerResolved, PeerResolutionRejected}`: excerpt 7.9
- `read_events`: `RecordsReports::read_events`, `crates/flow-nexus/src/reporting.rs:19`

---

## Not found, or found in a different shape

- **Bind** has no method of its own in `launching.rs`. It is the single
  line `self.perform(Operation::Bind(pane_launch))`, at launching.rs:179.
  The work is done by the `Operation::Bind` arm in performing.rs:246-257,
  which calls `HerdrCli::observe_native_binding` (herdr/launch.rs:1402).
  Excerpts 2.6 and 2.10 show all three.
- **The hook script** is the Rust binary `flow-hook`
  (`crates/flow/src/hook.rs`), not a shell script. It runs the `flow` CLI
  (`crates/flow/src/main.rs`). Flow names the hook in Claude Code's
  `--settings` JSON (excerpt 1.1). The user-level `~/.claude/settings.json`
  hooks are separate and do not reach Flow.
- **The first prompt's instruction** is written in three places.
  `body.push_str(&profile.instruction_prompt)` (composition.rs:725) is the
  **Codex** path. A Claude launch writes it with `line.push_str` in
  `render_claude_line` (:654) or with `format!` in `render_claude_direct`
  (:683). Excerpts 3.4-3.6 show these.
- **`LaunchProfile` in "signal-flow ethos"**: it is in the separate
  signal-flow repository at the pinned rev `f95034d`. The untracked
  `crates/signal-flow` directory in the flow checkout is not built.
- **messenger-clj has no Deliver/Vet/ResolvePeer.** Those three exist only
  in the Rust Message Nexus. messenger-clj's pane write is `direct-prompt!`
  (excerpt 7.4), a JSON `agent.prompt` request on Herdr's own socket.
- **Lengths**: every code block is under 40 lines, counting `…` lines.
  Excerpts that would have been longer are split into parts a and b.
- Cited without an excerpt, because the brief did not ask for them:
  `HerdrFailure` (performing.rs:95), `binding_matches_launch`,
  `expected_harness`, `run_json`, `title_claude_session`,
  `label_herdr_pane`, and the Message Nexus `Grading`. This list gives
  their files only, not their exact lines.

## Sources

- `/home/li/primary/flows/e5a0bc/reports/code-survey.md` (the starting
  survey: checkouts and revisions).
- `/git/github.com/LiGoldragon/flow` at `5e0b1bf11f453a9b2857e39d5cd5dda0bf90f130`,
  with a clean working tree for the files cited.
- `signal-flow` `f95034de0b203d886ba574fcb513c691c64b8498`,
  `meta-signal-flow` `54eb5618e1433b68520ba9644e0428ea0f9ed75d`, `message`
  `6fa4d0c1ba19232132081be228c418c667fff120`, `signal-message` `b94d907c`,
  and `sema-engine` `9884905f`. Each was read through `git archive` from its
  local clone under `/git/github.com/LiGoldragon/`. The pins were confirmed
  in `flow/Cargo.toml`, `flow/Cargo.lock`, and `message/Cargo.toml` /
  `Cargo.lock`.
- `/git/github.com/LiGoldragon/messenger-clj` at `85e71b15a93360507cdcce8c2605f6479d650426`.
- Method: every excerpt was cut by line number with `sed -n` from the files
  named above. No excerpt was typed by hand.
- Provenance receipt: unavailable, because no PROVENANCE handoff was
  supplied.
