# Code survey: Flow Nexus and the messenger, as of 2026-10-06

Read-only survey for the books «Flow and Message» and «The code». Every excerpt
below is copied verbatim from the named file at the named lines. Observations
(code read) are kept apart from hypotheses, which are collected at the end and
marked as such.

## 0. What was read, and which version is live

Observed:

- **Flow repository**: `/git/github.com/LiGoldragon/flow`, detached HEAD
  `5e0b1bf` (= `main` = `origin/main`), workspace version **0.24.0**.
- **Deployed Flow**: both `flow-nexus.service` and `flow-nexus-next.service`
  run `/nix/store/v945vrlsi6a79v8bighgglsvlp2qaxsz-flow-0.23.0/bin/flow-nexus`,
  so the live daemon is **0.23.0**. The 0.24.0 bump (`4ad596d`) changed only
  `crates/flow-nexus/ethos/operation.ethos` (adds `Release`) and
  `crates/flow-nexus/src/launching.rs` (calls Release after a refused launch),
  of the files excerpted here. Both versions pin the same `signal-flow` rev.
- **Flow's wire contracts are separate repositories**, pinned by git rev in
  `/git/github.com/LiGoldragon/flow/Cargo.toml`:
  - `signal-flow` rev `f95034de0b203d886ba574fcb513c691c64b8498` (10.0.0). The
    local checkout `/git/github.com/LiGoldragon/signal-flow` is at an older
    commit (`5ca97ce`), so the pinned rev was read with `git archive f95034de`.
    Paths below are given as `signal-flow@f95034d:<path>`.
  - `meta-signal-flow` rev `54eb5618e1433b68520ba9644e0428ea0f9ed75d`, read the
    same way: `meta-signal-flow@54eb561:<path>`.
  - `crates/signal-flow` and `crates/meta-signal-flow` directories inside the
    flow checkout are **untracked** leftovers; the build does not use them.
- **hm-\* commands**: `~/.local/bin/hm-send` is a wrapper that `exec`s babashka
  on `messenger-clj-0.3.0`. Source: `/git/github.com/LiGoldragon/messenger-clj`
  (HEAD `85e71b1`, `nix/package.nix` version 0.3.0). SKILL_VARIABLES.md
  "Repository root" is `/git`, so this is the repository it names.
- **Message Nexus** (the Rust messenger that is Flow's meta peer):
  `/nix/store/np57gg4bqhln3qf1j68q2njxh0p3ckqj-message-0.19.0/bin/message-nexus`
  is running. Local checkout `/git/github.com/LiGoldragon/message` is detached at
  0.17.0; `origin/main` (`6fa4d0c`, 0.19.1) was read with `git archive` and is
  cited as `message@6fa4d0c:<path>`.
- **ethos-zero**: `/git/github.com/LiGoldragon/ethos-zero` HEAD `c2653dd` is
  exactly the rev flow-nexus pins in `crates/flow-nexus/Cargo.toml:29`.

Paths without a repository prefix below are under
`/git/github.com/LiGoldragon/flow/crates/flow-nexus/`.

---

## 1. The types that name a flow today

### 1.1 FlowId: a `String`

`signal-flow@f95034d:ethos/signal.ethos:116`

```
[ FlowId.String
```

`signal-flow@f95034d:src/generated/signal.rs:3`

```rust
pub type FlowId = String;
```

How its value is minted (observed): Flow does not mint the six-hex alias
itself. It runs the external `flow-id` executable and reads its stdout.
`src/herdr/launch.rs:337-376` (abridged at the marked gap):

```rust
    fn claim_flow_identity(
        &self,
        harness: &HarnessKind,
        native_session_id: &str,
    ) -> Result<String, String> {
        let harness_name = harness.expected_harness();
        let mut command = Command::new(&self.flow_id_executable);
        command
            .arg(harness_name)
            .arg("--flows-root")
            .arg(&self.flows_root);
        // ... (env/arg per harness, run, check exit) ...
        let flow_id = String::from_utf8(output.stdout)
            .map_err(|_| "flow-id claim helper returned non-UTF-8 output".to_owned())?;
        let flow_id = flow_id.trim_end_matches(['\r', '\n']);
        if flow_id.is_empty()
            || flow_id.contains(char::is_whitespace)
            || !flow_id
                .bytes()
                .all(|byte| byte.is_ascii_hexdigit() && !byte.is_ascii_uppercase())
        {
            return Err("flow-id claim helper returned an invalid alias".into());
        }
        Ok(flow_id.into())
    }
```

The claim lives on disk as a marker `flows/.<FlowId>.flow-id` plus a lane
directory `flows/<FlowId>/` (`src/herdr/reservation.rs:91-115`;
`FlowClaim` decoder at `src/herdr.rs:590-640`, fields `harness_kind`,
`identity`, `alias`).

A second, older minting path still exists in the store, reachable only from a
legacy/test reservation (`src/store.rs:1052-1056`, `"legacy-test-start"`):
`src/store.rs:2298`

```rust
        let flow_id = format!("flow-{:016x}", state.next_flow_number);
```

The title code is the place that *requires* six lowercase hex characters:
`src/title.rs:65-86`

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

`self` here is a `LaunchProfile` (1.2). The declarations it uses:
`src/title.rs:50-58`

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
```

`src/title.rs:60-63`

```rust
/// The title a launch profile gives the Flow it starts.
pub trait TitlesFlow {
    fn native_title(&self, flow_id: &str) -> Result<NativeTitle, TitleRefused>;
}
```

`model_display_name` is the `NamesModel` trait, implemented for `str`
(`src/title.rs:16-47`), with a const table `MODEL_DISPLAY_NAMES` of
`(identifier, display)` pairs, e.g. `("claude-fable-5-1", "Fable")`.

Contrast (observed, not live code): ethos-zero's Flow *fixture* types FlowId as
an Integer. `/git/github.com/LiGoldragon/ethos-zero/fixtures/print/flow-library.ethos:1-12`

```
Library
[]
[ FlowId.Integer
  Voice.[ Psyche.Rank
          Mind.Rank
          Field.Rank ]
  Rank.[ Primary Secondary Tertiary ]
  Event.[ Started
          ToolUsed.String
          Stopped ] ]
[]
[]
```

The messenger's own FlowId is a looser string schema:
`/git/github.com/LiGoldragon/messenger-clj/src/messenger_clj/core.clj:17`

```clojure
(def FlowId [:and [:string {:min 1 :max 96}] [:re #"^[A-Za-z0-9][A-Za-z0-9_-]*$"]])
```

### 1.2 LaunchProfile

`signal-flow@f95034d:ethos/signal.ethos:150-154`

```
  FlowAspect.[ Psyche Mind Field ]
  PowerLevel.[ High Medium Low UltraLow ]
  LaunchSource.{ SourcePath SourceSha256 }
  RememberedFlow.{ FlowId RememberingDepth }
  LaunchProfile.{ LaunchRequestId Vector<LaunchSource> Vector<SkillName> FlowAspect PowerLevel HarnessKind ModelName Effort Option<FlowId> Vector<RememberedFlow> HerdrSessionName SystemPromptBundleFile InstructionPrompt }
```

`signal-flow@f95034d:src/generated/signal.rs:73-118`

```rust
pub enum FlowAspect {
    Psyche,
    Mind,
    Field,
}
// ...
pub enum PowerLevel {
    High,
    Medium,
    Low,
    UltraLow,
}
// ...
pub struct LaunchSource {
    pub source_path: SourcePath,
    pub source_sha256: SourceSha256,
}
// ...
pub struct RememberedFlow {
    pub flow_id: FlowId,
    pub remembering_depth: RememberingDepth,
}
// ...
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

(Each type carries `#[rustfmt::skip]` and
`#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq, Hash)]`
plus `#[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Composing))]`;
the `// ...` gaps are those attribute lines and unrelated types.) Every leaf name
(`LaunchRequestId`, `SkillName`, `ModelName`, `Effort`, `HerdrSessionName`,
`SystemPromptBundleFile`, `InstructionPrompt`, `SourcePath`, `SourceSha256`) is a
`pub type ... = String;` and `RememberingDepth` is `i64`, declared at
`signal.ethos:116-149`. `HarnessKind` is `[ Codex Claude ]` (`signal.ethos:182`).

`flow_id_option` is the predecessor for Replace (see 1.6).

### 1.3 Role / Voice / Aspect / Layer / Job / Seat types

Observed:

- **Aspect**: `FlowAspect.[ Psyche Mind Field ]` (above). It is the only
  "who is this flow" enum on the wire.
- **Power**: `PowerLevel.[ High Medium Low UltraLow ]` (above).
- **Role**: there is no `Role` type. "Role" in code is the `Caller` struct,
  stored per flow as `StoredRole`:

  `signal-flow@f95034d:ethos/signal.ethos:210`

  ```
    Caller.{ FlowId FlowAspect PowerLevel ModelName }
  ```

  `signal-flow@f95034d:src/generated/signal.rs:501-506`

  ```rust
  pub struct Caller {
      pub flow_id: FlowId,
      pub flow_aspect: FlowAspect,
      pub power_level: PowerLevel,
      pub model_name: ModelName,
  }
  ```

  `src/store.rs:217-223`

  ```rust
  /// A flow's role: its aspect, power and model, keyed by its FlowId. It is
  /// exactly what ResolveCaller answers, so the Caller is stored as it is.
  #[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
  struct StoredRole {
      caller: Caller,
  }
  ```

  The composer also has a private `NamesRole` trait for `LaunchProfile`
  (`src/composition.rs:287-309`) that renders `aspect_name()` and
  `power_name()` (e.g. `"Ultra Low"`).
- **Voice**: no type in Flow code. One doc-comment mention (see section 7). It
  exists only in the ethos-zero fixtures (`Voice.[ Psyche.Rank Mind.Rank Field.Rank ]`,
  above).
- **Layer, Job, Seat**: no types. See section 7 for where the words occur.

### 1.4 Memory / record structs

The store (`src/store.rs`) uses sema-engine tables. Its flow row:

`src/store.rs:167-187`

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
struct FlowRecord {
    flow_id: String,
    flow_type: String,
    origin: OriginClue,
    thread_id: Option<String>,
    harness_kind: HarnessKind,
    endpoint_selection: EndpointSelection,
    lifecycle: FlowLifecycle,
    generation: u64,
}

#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
#[rkyv(derive(Debug))]
enum FlowLifecycle {
    Pending,
    Active,
    Stopped,
    Retired,
    Exited,
}
```

Note: the store has its **own private** `FlowLifecycle`, parallel to the wire
one, imported as `SignalFlowLifecycle`; both implement `NamesLiveFlow`
(`src/store.rs:195-209`):

```rust
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

Route row and counter, `src/store.rs:230-246`:

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
struct FlowHerdrRouteRecord {
    flow_id: String,
    route: HerdrRoute,
}
// ...
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
#[rkyv(derive(Debug))]
struct FlowStoreState {
    next_flow_number: u64,
}
```

The store itself, `src/store.rs:614-634`:

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

Launch outcome and replacement, `src/store.rs:478-484` and `526-530`:

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq, Hash)]
pub enum LaunchOutcome {
    Started(Launched),
    Replaced(Replaced),
    StartRejected(StartRejection),
    ReplaceRejected(ReplaceRejection),
}
```

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq, Hash)]
pub struct Replacement {
    pub launch_request_id: String,
    pub predecessor: String,
}
```

`src/store.rs:648-652`

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum FlowRegistration {
    Registered(Box<FlowNode>),
    ConflictingBinding,
}
```

"Memory" today is the per-flow events row. `src/store/events.rs:1-12, 25-31`:

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
```

```rust
/// One flow's harness events, oldest first.
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub struct FlowEvents {
    pub flow_id: String,
    pub event_vector: Vec<Event>,
}
```

The Memory root is *not* compiled: `src/lib.rs:3-4`

```rust
// The generated Operation root names the store's own types by this crate's
// name, as `flow_nexus::LaunchOutcome`; the Memory root is not compiled yet.
```

The only Memory-root ethos that exists is the ethos-zero fixture
`/git/github.com/LiGoldragon/ethos-zero/fixtures/print/flow-memory.ethos:1-6`:

```
Memory
[ flow:[ FlowId Voice Event ] ]
[ Flow.{ FlowId
         Voice
         State.[ Running Ended ]
         Vector<Event> } ]
```

and its generated Rust `ethos-zero/tests/generated/flow-memory.rs:5-17`:

```rust
pub enum State {
    Running,
    Ended,
}
// ...
pub struct Flow {
    pub flow_id: flow::FlowId,
    pub voice: flow::Voice,
    pub state: State,
    pub event_vector: std::vec::Vec<flow::Event>,
}
```

### 1.5 Wire node, binding, lifecycle

`signal-flow@f95034d:ethos/signal.ethos:176, 186-192`

```
  OriginClue.{ FlowId SessionId TurnId }
  ...
  HerdrRoute.{ HerdrSessionName HerdrAgentName HerdrPaneId HerdrTerminalId }
  HerdrRouteSelection.[ Available.HerdrRoute
                        Unavailable ]
  FlowLifecycle.[ Pending Active Stopped Retired Exited ]
  FlowNode.{ FlowId SessionId HarnessKind EndpointSelection HerdrRouteSelection OriginClue FlowLifecycle }
  FlowList.Vector<FlowNode>
  Launched.{ FlowId SessionId OriginClue }
```

`signal-flow@f95034d:src/generated/signal.rs:368-396`

```rust
pub enum FlowLifecycle {
    Pending,
    Active,
    Stopped,
    Retired,
    Exited,
}
// ...
pub struct FlowNode {
    pub flow_id: FlowId,
    pub session_id: SessionId,
    pub harness_kind: HarnessKind,
    pub endpoint_selection: EndpointSelection,
    pub herdr_route_selection: HerdrRouteSelection,
    pub origin_clue: OriginClue,
    pub flow_lifecycle: FlowLifecycle,
}
#[rustfmt::skip]
pub type FlowList = std::vec::Vec<FlowNode>;
// ...
pub struct Launched {
    pub flow_id: FlowId,
    pub session_id: SessionId,
    pub origin_clue: OriginClue,
}
```

`OriginClue` (`signal.rs:294-298`) has `flow_id`, `session_id`, `turn_id`: the
originating flow of a launch is carried as a FlowId plus its native session and
turn.

Bindings (launch-side), `signal.ethos:158-161`:

```
  HerdrPaneBinding.{ LaunchRequestId HerdrSessionName HerdrAgentName HerdrWorkspaceId HerdrPaneId HerdrTerminalId }
  NativeLaunchIntent.{ LaunchRequestId PromptSha256 HarnessKind ModelName Effort Vector<SkillName> }
  NativeLaunchBinding.{ LaunchRequestId FlowId NativeSessionId HarnessKind HerdrPaneBinding }
  RegistrationAcknowledgement.{ LaunchRequestId FlowId NativeSessionId HerdrPaneBinding }
```

Bindings (privileged import of an existing seat), `meta-signal-flow@54eb561:ethos/signal.ethos:106-118`:

```
  MetaFlowOwnerId.FlowId
  HerdrTabId.String
  WorkingDirectory.String
  FlowLifecycle.[ RegisteredUnconfirmed ]
  FlowContainer.{ HerdrSessionName HerdrServerSocketPath HerdrServerProcessIdentity MetaFlowOwnerId }
  FlowBinding.{ FlowId FlowAspect PowerLevel ModelName HarnessKind NativeSessionId HerdrWorkspaceId HerdrPaneId HerdrTabId HerdrTerminalId HerdrAgentName ProcessIdentity WorkingDirectory }
  MetaBindExisting.{ FlowContainer Vector<FlowBinding> }
  BoundFlowBinding.{ FlowId FlowLifecycle }
  FlowBindingRefusalReason.[ AmbiguousPane DeadProcess DuplicateFlowId AnatomyMismatch ]
  RefusedFlowBinding.{ FlowId FlowBindingRefusalReason }
  FlowBindingResult.[ Bound.BoundFlowBinding
                      Refused.RefusedFlowBinding ]
```

Note that meta-signal-flow declares a **third** `FlowLifecycle` with the single
variant `RegisteredUnconfirmed`. Its checks live in `src/binding.rs`
(`ChecksFlowContainer`, `ChecksFlowBinding`, `RefusesBinding`, lines 55-106).

There is no type named `Node` alone; the node is `FlowNode`.

### 1.6 `self` in launching.rs: `RunningNexus`

All launch verbs are a trait on `RunningNexus`. `src/lib.rs:68-78`:

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

`src/launching.rs:42-70`

```rust
/// The launch verbs of the running Nexus. `start` is the one Start path;
/// `settle` records what a launch came to and, for a replacement, stops and
/// reaps the predecessor before the successor becomes routable.
pub trait LaunchesFlows {
    /// Runs or resumes the launch a StartRequest names.
    fn start(&self, request: StartRequest) -> Response;
    /// Looks again at the native transcript of a launch whose first prompt
    /// was not yet seen, promoting it when the receipt is there.
    fn promote_ambiguous(&self, attempt: LaunchAttempt) -> Response;
    /// The recorded outcome of a request already settled, or None.
    fn settled(&self, request: &StartRequest) -> Option<Response>;
    /// Records what a Start-path response settles, completing a replacement.
    fn settle(&self, launch_request_id: &str, response: Response) -> Response;
    /// Starts the successor through the Start path, then replaces.
    fn replace(&self, request: StartRequest) -> Response;
    /// Stops the predecessor, then closes its pane; only then is the
    /// successor routable.
    fn reap(&self, replacement: Replacement, launched: Launched) -> Response;
    /// Answers once: the outcome, else the pending attempt.
    fn launch_status(&self, launch_request_id: &str) -> Response;
    /// Everything a new launch does after Reserve, from the native intent
    /// to the confirmed receipt.
    fn launch_reserved(
        &self,
        launch: ComposedLaunch,
        origin: OriginClue,
        reserved: Option<String>,
    ) -> Response;
}
```

`impl LaunchesFlows for RunningNexus` begins at `src/launching.rs:72`. Its
`start` (lines 73-147) composes, reserves, calls `launch_reserved`, and on
refusal releases (0.24.0 only):

`src/launching.rs:98-146` (abridged at the marked gap)

```rust
        let launch = match self.perform(Operation::Compose(request.launch_profile)) {
            Outcome::Composed(launch) => launch,
            _ => return Response::StartRejected(StartRejection::CompositionRefused),
        };
        // ... (Codex endpoint check) ...
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
            // ... (Existing / Conflict / ClaimRefused arms) ...
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

**Bind** is not its own method in launching.rs; it is one `Operation` inside
`launch_reserved`. `src/launching.rs:171-182`

```rust
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

The rest of `launch_reserved` (lines 183-310) records the binding, builds a
`FlowNode` with `FlowLifecycle::Pending`, builds the `Caller` (role) from the
profile's aspect/power/model, registers, titles, resolves native skills,
submits the first prompt, and confirms.

`perform` is the `Performs` trait, also on `RunningNexus`.
`src/performing.rs:126-142`

```rust
/// The Nexus acting: one Operation in, one Outcome out.
pub trait Performs {
    /// What a seat is told the moment its launch receipt is confirmed.
    /// ...
    const BRIEF_CONTINUATION: &'static str =
        "Launch receipt confirmed. Begin the brief in your first prompt now.";

    fn perform(&self, operation: Operation) -> Outcome;
}
```

The Bind arm, `src/performing.rs:246-257`:

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

whose `self.herdr` is a `HerdrCli`, `src/herdr.rs:85-110`:

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
    /// This Nexus's own ordinary socket, ...
    pub(crate) ordinary_socket: PathBuf,
    /// Where each launch's own bundle copy lives, the one a Claude launch
    /// receives as `--system-prompt-file`.
    launch_bundles: LaunchBundles,
}
```

and the trait, `src/herdr/launch.rs:51-62`:

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
```

(`impl ObservesNativeLaunchBinding for HerdrCli` at `src/herdr/launch.rs:1402`.)

**Replace / reap**, `src/launching.rs:425-435` (head of `replace`):

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
```

`src/launching.rs:477-486` (tail of `replace`):

```rust
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

`src/launching.rs:488-552` is `reap`: it records the predecessor `Stopped`,
reads `self.herdr.pane_presence(&node)` (`Absent | Unknown | Present`), closes a
present pane, prunes bundles, records `LaunchOutcome::Replaced`, then performs
`Operation::Continue` on the successor. Its key lines, `505-515`:

```rust
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

### 1.7 `self` in composition.rs: `LaunchComposer` (and `LaunchProfile`)

`src/composition.rs:37-40`

```rust
pub struct LaunchComposer {
    source_root: PathBuf,
    launch_bundles: LaunchBundles,
}
```

`src/composition.rs:62-65`

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LaunchBundles {
    directory: PathBuf,
}
```

The trailing "launch section" of the system prompt is rendered with `self` a
`LaunchProfile`: `src/composition.rs:104-128`

```rust
/// The trailing section a launch appends to its bundle: `Predecessor:` when
/// the profile names one, `Remembered:` when it remembers any flows, and
/// nothing otherwise. Each line ends with a newline.
pub trait RendersLaunchSection {
    fn launch_section(&self) -> String;
}

impl RendersLaunchSection for LaunchProfile {
    fn launch_section(&self) -> String {
        let mut section = String::new();
        if let Some(predecessor) = &self.flow_id_option {
            section.push_str(&format!("Predecessor: {predecessor}\n"));
        }
        if !self.remembered_flow_vector.is_empty() {
            let remembered = self
                .remembered_flow_vector
                .iter()
                .map(|flow| flow.flow_id.as_str())
                .collect::<Vec<_>>()
                .join(", ");
            section.push_str(&format!("Remembered: {remembered}\n"));
        }
        section
    }
}
```

System prompt: the caller supplies a bundle file
(`LaunchProfile.system_prompt_bundle_file`); Flow copies it per launch and
appends the section. `src/composition.rs:576-597`

```rust
impl WritesLaunchBundle for LaunchComposer {
    fn write_launch_bundle(&self, profile: &LaunchProfile) -> Result<PathBuf, CompositionError> {
        let mut bytes = fs::read(&profile.system_prompt_bundle_file)
            .map_err(|_| CompositionError::InvalidProfileField("system_prompt_bundle_file"))?;
        let section = profile.launch_section();
        if !section.is_empty() {
            if !bytes.is_empty() && !bytes.ends_with(b"\n") {
                bytes.push(b'\n');
            }
            bytes.push(b'\n');
            bytes.extend_from_slice(section.as_bytes());
        }
        let file = self.launch_bundles.file_for(profile);
        let unwritable =
            |error: std::io::Error| CompositionError::LaunchBundleUnwritable(error.to_string());
        fs::create_dir_all(&self.launch_bundles.directory).map_err(unwritable)?;
        let partial = file.with_extension("md.partial");
        fs::write(&partial, &bytes).map_err(unwritable)?;
        fs::rename(&partial, &file).map_err(unwritable)?;
        Ok(file)
    }
}
```

First prompt: `src/composition.rs:737-772`

```rust
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
        if profile.harness_kind == HarnessKind::Claude {
            let candidate = format!("{}{}", body, profile.harness_kind.receipt_footer());
            if !candidate.fits_claude_paste() {
                let LaunchBundleText::File(bundle_file) = &bundle else {
                    unreachable!("Claude launches always receive a bundle file")
                };
                body = self.render_claude_direct(profile, bundle_file, &sources);
            }
        }
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

The traits it relies on are declared in the same file: `ComposesLaunch`
(148-150), `ValidatesLaunchProfile` (324-326), `ReadsLaunchSource` (328-340),
`ReadsSystemPromptBundle` (345-347), `WritesLaunchBundle` (351-353),
`RendersLaunchProfile` (355-382), `HashesPromptBody` (384-386),
`AsksForLaunchReceipt` (168-174, const `LAUNCH_RECEIPT = "FLOW_LAUNCH_RECEIPT_V2"`),
`FitsClaudePaste` (194-201), and the private enum `LaunchBundleText` (379,
variants `File(PathBuf)` and `Inline(String)`). The output type:
`signal.ethos:156-157`

```
  FirstPromptPayload.{ FirstPromptBody PromptSha256 FirstPromptText }
  ComposedLaunch.{ LaunchProfile FirstPromptPayload TargetReceiptRequest }
```

For Codex the body also carries a `# Flow launch` block naming
`Role: {aspect} {power}`, Harness, Model, Effort, Herdr session and Remote
control (`src/composition.rs:699-735`). For Claude, role/model/effort reach the
harness only through argv (`src/composition.rs:630-634`).

### 1.8 title.rs `native_title`

Shown in 1.1. `self` is `LaunchProfile`; it reads only `self.model_name` and
`self.flow_aspect`. The result type is `NativeTitle(String)`, format
`<Aspect>.{ <Model> <FlowId> }`. It is applied by
`impl TitlesNativeFlow for HerdrCli` (`src/herdr/launch.rs:1234-1263`), which
sets the Claude session name or Codex thread name and the Herdr pane label.

---

## 2. Signal / Operation / Memory enums as declared

### 2.1 Ordinary Signal (Request/Response)

`signal-flow@f95034d:ethos/signal.ethos:81-115`

```
Signal
[]
[ Start.StartRequest
  Restart.RestartRequest
  ResolveRecipient.RecipientResolutionRequest
  Stop.StopRequest
  List.ListRequest
  Replace.StartRequest
  LaunchStatus.LaunchRequestId
  Observe.ObserveSelection
  ResolveCaller.Option<FlowId>
  QueueTurnEnd.TurnEndRequest
  Report.{ FlowId Event } ]
[ Started.Launched
  LaunchPending.LaunchAttempt
  StartAmbiguous.PromptDeliveryIntent
  Restarted.Restarted
  RecipientResolved.FlowNode
  Stopped.FlowId
  Listed.FlowList
  StartRejected.StartRejection
  RestartRejected.RestartRejection
  RecipientResolutionRejected.RecipientResolutionRejection
  StopRejected.StopRejection
  ListRejected.ListRejection
  Replaced.Replaced
  ReplaceRejected.ReplaceRejection
  LaunchStatusRejected.LaunchStatusRejection
  CallerResolved.Caller
  CallerResolutionRejected.CallerResolutionRejection
  AgentObserved.AgentObservation
  TurnEndQueued.TurnEndRequest
  TurnEndRejected.TurnEndRejection
  Reported
  Refused.[ UnknownFlow.FlowId ] ]
```

Generated: `signal-flow@f95034d:src/generated/signal.rs:560-605`

```rust
pub enum Query {
    Start(StartRequest),
    Restart(RestartRequest),
    ResolveRecipient(RecipientResolutionRequest),
    Stop(StopRequest),
    List(ListRequest),
    Replace(StartRequest),
    LaunchStatus(LaunchRequestId),
    Observe(ObserveSelection),
    ResolveCaller(std::option::Option<FlowId>),
    QueueTurnEnd(TurnEndRequest),
    Report(Report_Data),
}
// ...
pub enum Response {
    Started(Launched),
    LaunchPending(LaunchAttempt),
    StartAmbiguous(PromptDeliveryIntent),
    Restarted(Restarted),
    RecipientResolved(FlowNode),
    Stopped(FlowId),
    Listed(FlowList),
    StartRejected(StartRejection),
    RestartRejected(RestartRejection),
    RecipientResolutionRejected(RecipientResolutionRejection),
    StopRejected(StopRejection),
    ListRejected(ListRejection),
    Replaced(Replaced),
    ReplaceRejected(ReplaceRejection),
    LaunchStatusRejected(LaunchStatusRejection),
    CallerResolved(Caller),
    CallerResolutionRejected(CallerResolutionRejection),
    AgentObserved(AgentObservation),
    TurnEndQueued(TurnEndRequest),
    TurnEndRejected(TurnEndRejection),
    Reported,
    Refused(Refused_Data),
}
```

The harness event, `signal.ethos:218-220` / `signal.rs:545-549`:

```rust
pub enum Event {
    Started,
    ToolUsed(String),
    Stopped,
}
```

The contract is identified by the digest of its ethos source,
`signal-flow@f95034d:src/lib.rs:6-13`:

```rust
pub const ETHOS: &str = include_str!("../ethos/signal.ethos");
pub const WIRE_VERSION: &str = env!("CARGO_PKG_VERSION");

/// The contract is identified on the wire by the digest of its authored
/// Ethos source; the querying side greets with it.
impl signal::Contracted for Query {
    const CONTRACT_SOURCE: &'static str = ETHOS;
}
```

Dispatch lives on `RunningNexus` via `trait Dispatches` (`src/lib.rs:80-83`,
`fn dispatch(&self, query: Query) -> Response;` and
`fn dispatch_meta(&self, query: meta_signal_flow::Query) -> meta_signal_flow::Response;`),
implemented from `src/lib.rs:85`. Two arms are stubs today: `Restart` always
answers `RestartRejected(ResumeRefused)` (lines 103-119) and `QueueTurnEnd`
always answers `TurnEndRejected(QueueRefused)` (lines 176-180).

### 2.2 Privileged (meta) Signal

`meta-signal-flow@54eb561:ethos/signal.ethos:39-70`

```
Signal
[ signal_flow:[ FlowNode FlowId FlowAspect PowerLevel ModelName HarnessKind NativeSessionId HerdrSessionName HerdrAgentName HerdrWorkspaceId HerdrPaneId HerdrTerminalId Caller CallerResolutionRejection Event ] ]
[ Configure.ConfigureRequest
  ConsumeReset.ResetRequest
  RegisterFlow.FlowNode
  MetaBindExisting.MetaBindExisting
  Retire.FlowId
  Deliver.DeliveryRequest
  Vet.DeliveryRequest
  Command.CommandRequest
  ResolvePeer.ProcessIdentity
  ReadEvents.FlowId ]
[ Configured.Configured
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
  EventsRead.{ FlowId Vector<Event> }
  ReadEventsRejected.[ UnknownFlow StoreRefused ] ]
```

Its message types, `meta-signal-flow@54eb561:ethos/signal.ethos:121-135, 153`:

```
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
  ...
  HarnessCommand.[ Compact Interrupt ]
```

### 2.3 Operation / Outcome (the Nexus's own acts)

`crates/flow-nexus/ethos/operation.ethos:29-81` (0.24.0; `Release` and
`Released` are new since the deployed 0.23.0)

```
Operation
[ signal_flow:[ FlowId LaunchRequestId FlowNode Caller LaunchProfile ComposedLaunch OriginClue LaunchAttemptReservation HerdrPaneBinding NativeLaunchIntent NativeLaunchBinding RegistrationAcknowledgement PromptDeliveryIntent PromptDeliveryResult Launched Event ]
  flow_nexus:[ LaunchOutcome Replacement ] ]
[ Compose.LaunchProfile
  Reserve.{ ComposedLaunch OriginClue }
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
           Harness.{ FlowId Event } ]
  Register.{ FlowNode Caller }
  Confirm.FlowId
  Open.ComposedLaunch
  Spawn.PaneLaunch
  Bind.PaneLaunch
  Title.{ ComposedLaunch NativeLaunchBinding }
  Submit.{ ComposedLaunch PromptDeliveryIntent }
  Continue.FlowId
  Close.FlowNode
  Prune.LaunchRequestId
  Release.FlowId ]
[ Composed.ComposedLaunch
  Reserved.{ LaunchAttemptReservation Option<FlowId> }
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
  Failed.[ CompositionRefused
           StoreRefused
           ConflictingBinding
           Unstarted
           HerdrRefused
           CodexRefused
           BundleRefused
           UnknownFlow
           ClaimRefused ] ]
[ PaneLaunch.{ ComposedLaunch HerdrPaneBinding Option<FlowId> } ]
```

Generated: `src/generated/operation.rs:5-9, 73-88, 113-129`

```rust
pub struct PaneLaunch {
    pub composed_launch: signal_flow::ComposedLaunch,
    pub herdr_pane_binding: signal_flow::HerdrPaneBinding,
    pub flow_id_option: std::option::Option<signal_flow::FlowId>,
}
// ...
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
// ...
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

### 2.4 Memory

No Memory root is compiled in Flow (see 1.4). The only Memory ethos is the
ethos-zero fixture `fixtures/print/flow-memory.ethos` (shown in 1.4). The
fixture set also holds a vision-shaped Signal and Operation for Flow, which do
not match the live contracts:

`ethos-zero/fixtures/print/flow-signal.ethos:1-10`

```
Signal
[ flow:[ FlowId Voice Event ] ]
[ Launch.{ Voice
           Brief.String }
  Report.{ FlowId Event } ]
[ Launched.FlowId
  Refused.[ NoCapsule
            VoiceBusy.Voice ]
  Reported ]
[]
```

`ethos-zero/fixtures/print/flow-operation.ethos:1-9`

```
Operation
[ flow:[ FlowId Voice Event ] ]
[ Start.{ Voice Capsule }
  Record.{ FlowId Event } ]
[ Started.FlowId
  Recorded
  Failed.String ]
[ Capsule.{ Home.String
            Login.Vector<String> } ]
```

---

## 3. Flow's ethos files and the generator entry point

Ethos files found (`find -name '*.ethos'`, excluding `target/`):

| File | Root | Status |
|---|---|---|
| `/git/github.com/LiGoldragon/flow/crates/flow-nexus/ethos/operation.ethos` | Operation | live; generated into `src/generated/operation.rs` |
| `signal-flow@f95034d:ethos/signal.ethos` | Signal | live; generated into `src/generated/signal.rs` of that crate |
| `meta-signal-flow@54eb561:ethos/signal.ethos` | Signal | live |
| `/git/github.com/LiGoldragon/ethos-zero/fixtures/print/flow-{library,signal,operation,memory}.ethos` | all four | test fixtures only |

There is no `ethos/` directory for Flow's Memory, and none in
`/git/github.com/LiGoldragon/flow-data`.

How flow-nexus calls the generator: `crates/flow-nexus/build.rs:1-23`

```rust
//! The Operation root is generated from `ethos/operation.ethos` by
//! ethos-zero; the committed module must equal a fresh generation, so a
//! stale `src/generated/operation.rs` fails the build.

use ethos_zero::{Actualizing, File, Generating, Potential};

fn main() {
    let root = std::path::PathBuf::from(std::env::var_os("CARGO_MANIFEST_DIR").expect("manifest"));
    println!("cargo:rerun-if-changed=ethos/operation.ethos");
    println!("cargo:rerun-if-changed=src/generated/operation.rs");
    let source = std::fs::read_to_string(root.join("ethos/operation.ethos")).expect("source");
    let file = Potential::<File>::from(source)
        .actualize()
        .unwrap_or_else(|_| panic!("read Operation"));
    let generated = file
        .generate()
        .unwrap_or_else(|_| panic!("generate Operation"));
    assert_eq!(
        generated,
        std::fs::read_to_string(root.join("src/generated/operation.rs")).expect("generated"),
        "src/generated/operation.rs is stale; regenerate it from ethos/operation.ethos"
    );
}
```

The names it uses, declared in ethos-zero (rev `c2653dd`):

`/git/github.com/LiGoldragon/ethos-zero/src/lib.rs:400`

```rust
pub struct Potential<T>(pub String, PhantomData<fn() -> T>);
```

`/git/github.com/LiGoldragon/ethos-zero/src/lib.rs:540-543, 560-563`

```rust
pub trait Generating {
    /// The formatted Rust text, or the whole-file error that prevents generation.
    fn generate(&self) -> Result<String, Error>;
}
// ...
pub trait Actualizing<T> {
    type Error;
    fn actualize(&self) -> Result<T, Self::Error>;
}
```

`/git/github.com/LiGoldragon/ethos-zero/src/actualization.rs:10-13`

```rust
impl Actualizing<File> for Potential<File> {
    type Error = Error;

    fn actualize(&self) -> Result<File, Self::Error> {
```

`/git/github.com/LiGoldragon/ethos-zero/src/generation.rs:1234-1235`

```rust
impl Generating for File {
    fn generate(&self) -> Result<String, crate::Error> {
```

The CLI binary entry (`Cargo.toml` `[[bin]] name = "ethos-zero"`, `path = "src/main.rs"`):
`/git/github.com/LiGoldragon/ethos-zero/src/main.rs:208-210`

```rust
fn main() -> ExitCode {
    std::env::args().skip(1).collect::<Vec<_>>().invoke()
}
```

The CLI's own contract names the four roots,
`/git/github.com/LiGoldragon/ethos-zero/ethos-zero.ethos:5-10`:

```
; The files read are of four roots, each section in this order:
;   Library    [ imports ] [ types ] [ kinds ] [ associations ]
;   Signal     [ imports ] [ queries ] [ responses ] [ types ]
;   Operation  [ imports ] [ operations ] [ outcomes ] [ types ]   ; proposed, pending the living's word
;   Memory     [ imports ] [ record types ]
; A file headed Sema is refused as Renamed.Memory.
```

---

## 4. How the messenger names a sender and finds a target

There are two messengers. Observed facts for each.

### 4.1 messenger-clj (the hm-\* commands, deployed 0.3.0)

**Sender**: taken from the process environment `FLOW_ID` (or a test-bound
dynamic var); never asked of Flow.
`/git/github.com/LiGoldragon/messenger-clj/src/messenger_clj/core.clj:906`
(in `send-request!`; the same line occurs at 849 in `send-abrupt-request!`)

```clojure
   (let [sender (or *flow-id* (System/getenv "FLOW_ID") (fail "Set FLOW_ID to your own flow ID before sending"))]
```

`core.clj:101`

```clojure
(def ^:dynamic *flow-id* nil)
```

`core.clj:42-45`

```clojure
(defn flow-id! [value]
  (when-not (and (string? value) (re-matches #"[A-Za-z0-9][A-Za-z0-9_-]{0,95}" value))
    (fail "Flow ID must contain only letters, digits, underscores, or hyphens"))
  (valid! FlowId value "FlowId"))
```

(`FLOW_ID` in a launched Claude pane is exported by Flow at Spawn; see
`src/herdr/reservation.rs:1-9` and `src/herdr/launch.rs:37-41`.)

**Envelope**: the sender is the first element of a tagged EDN tuple.
`core.clj:28-31`

```clojure
(def PaneMessage [:tuple FlowId MessageBody])
(def PsycheMessage [:tuple FlowId MessageBody MessageBody])
(def PsychesMessage [:vector {:min 1} PsycheMessage])
(def PsychesInput [:vector {:min 1} [:tuple MessageBody MessageBody]])
```

`core.clj:161-176`

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

So the pane text is `#msg ["<sender>" "<body>"]` or
`#psyche ["<sender>" "<context>" "<verbatim>"]`. The tag readers are bound in
`/git/github.com/LiGoldragon/messenger-clj/src/data_readers.clj`:

```clojure
{msg messenger-clj.core/read-msg
 psyche messenger-clj.core/read-psyche
 psyches messenger-clj.core/read-psyches}
```

**Target to Herdr binding**: the messenger's **own** route store, a Datalevin
database at `~/.local/state/messenger-clj` (or `$HM_REGISTRY`), keyed by flow
id. `core.clj:21`

```clojure
(def RouteBinding [:map {:closed true} [:session :string] [:name :string] [:pane_id :string] [:terminal_id :string] [:agent :string] [:native_thread {:optional true} NativeThread] [:route_hold {:optional true} :string] [:transition {:optional true} :boolean] [:state {:optional true} :string]])
```

`core.clj:84, 96-99`

```clojure
(defprotocol Registry (load-route [this flow]) (save-route! [this flow route]))
;; ...
(defrecord DatalevinRegistry [state-root]
  Registry
  (load-route [_ flow] (store/route-for state-root (flow-id! flow)))
  (save-route! [_ flow route] (store/put-route! state-root (flow-id! flow) (route-binding! route))))
```

`core.clj:191-196`

```clojure
(defn read-route [flow]
  (try
    (if-let [route (load-route (registry) flow)]
      (route-binding! route)
      (fail (str "No valid registration for " flow)))
    (catch Exception e (fail (str "No valid registration for " flow ": " (.getMessage e))))))
```

`/git/github.com/LiGoldragon/messenger-clj/src/messenger_clj/typed_store.clj:216-217`

```clojure
(defn route-for [root flow]
  (when-not (retirement-for root flow) (stored-route-for root flow)))
```

Routes are written by `hm-register` (`core.clj:512-`), which finds exactly one
live Herdr agent by name via `herdr agent list` and stores its session, name,
pane id, terminal id, agent kind and native thread. Delivery then talks to
Herdr directly (`herdr` CLI and Herdr's socket, `core.clj:197-274`). Every send
and register holds an Orchestrate lock named after the sender (`reserve!`,
`core.clj:446-475`, shelling out to `orchestrate`).

**Does it ask Flow anything?** No. A grep of `src/messenger_clj/*.clj` for
`flow-nexus`, `ResolveCaller`, `ResolveRecipient`, `signal`, or an invocation
of the `flow` CLI finds nothing; the only external programs are `herdr`,
`orchestrate`, and the Datalevin pod.

### 4.2 Message Nexus (`message-nexus`, deployed 0.19.0)

This one does ask Flow. Observed in `message@6fa4d0c` (0.19.1):

`crates/message-nexus/src/peer.rs:1-6`

```rust
//! The process at the other end of a connection, as the kernel names it.
//!
//! Message never takes a sender from a payload. It reads its peer's
//! credentials (`SO_PEERCRED`) and the process's start time, and asks Flow
//! (`ResolvePeer`) which flow that exact process runs in. The start time
//! makes the identity name one process, never a reused process ID.
```

`crates/message-nexus/src/service.rs:23-48`

```rust
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

The sender written into the Letter is `meta_signal_flow::Sender`
(`Flow(FlowId)` for a resolved peer on the ordinary socket,
`crates/message-nexus/src/listener.rs:124`; `Owner` on the meta socket,
`listener.rs:184`). Generated in `meta-signal-flow@54eb561:src/generated/signal.rs:252-281`:

```rust
pub enum Sender {
    Flow(signal_flow::FlowId),
    Owner,
}
// ...
pub struct Letter {
    pub message_id: MessageId,
    pub sender: Sender,
    pub content: Content,
}
```

Message does not hold routes: it hands Flow a `Deliver` addressed by FlowId
(`crates/message-nexus/src/flow_edge.rs:3-5, 52-60`; queries `ResolvePeer`,
`Vet`, `Deliver`), and Flow renders the `Message` as its own datom into the
pane (`crates/flow-nexus/src/delivery/body.rs:50-54`, text begins
`HardAbrupt.`, `MiddleAbrupt.` or `Soft.`). Flow resolves the target route from
its own store, `FlowNode.herdr_route_selection`, refreshed against Herdr
(`src/lib.rs:121-133`, `src/store.rs:2158`).

On the Flow side, `ResolvePeer` and `ResolveCaller` read the peer from the
kernel and find its pane by the `HERDR_SESSION` / `HERDR_PANE_ID` environment
the process inherited, `crates/flow-nexus/src/caller.rs:1-15`:

```rust
//! Who called: ResolveCaller names the flow bound to the process at the
//! other end of an ordinary connection.
//!
//! The kernel names the peer process (`SO_PEERCRED`); the caller's word is
//! never read. Herdr's snapshot carries no process IDs, so the pane is found
//! the way Herdr itself marks it: every process Herdr starts in a pane
//! inherits `HERDR_SESSION` and `HERDR_PANE_ID`. The peer's environment is
//! read from `/proc`, and when the peer does not carry them (an environment
//! the harness scrubbed) its ancestors are read in turn. The pane found must
//! hold exactly one routable flow in the registry, and the live Herdr
//! snapshot must still show that flow's binding (session, pane, terminal and
//! harness), so a pane ID Herdr reused for a new terminal names no one.
//!
//! ResolvePeer (meta) answers the same question for a process named by
//! Message, which reads its own peer from the kernel.
```

---

## 5. Does anything monitor a flow's context size today?

Observed: **nothing in Flow, messenger-clj or Message Nexus measures context
size, token counts, or transcript size, or triggers a handover on them.**

Method: `grep -rniE 'context[_ -]?(size|window|limit|usage)|token|handover|hand-over|compact|transcript.{0,10}(size|len|bytes)'`
over `flow/crates` (`*.rs`, `*.ethos`), plus `context_window|used_percentage|PreCompact|handover|context[_ -]?(size|limit)`
over `messenger-clj/src`, `message/crates` and `CriomOS-home`. All "token"
hits in Flow are process start tokens or the restart authorization; the
`handover` hits are a test turn id (`src/store.rs:2474`) and Herdr *server*
handover in `CriomOS-home/modules/home/profiles/min/herdr.nix`.

What exists nearby:

- **Flow's harness hook** reports only three events.
  `/git/github.com/LiGoldragon/flow/crates/flow/src/hook.rs:1-13`

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

  The hook settings Flow injects are `SessionStart`, `PostToolUse`, `Stop`
  only (`crates/flow-nexus/src/herdr/launch.rs:177-179`). No `PreCompact`.
- **Flow can send `/compact`** to a pane, but only on request:
  `HarnessCommand.[ Compact Interrupt ]` in meta-signal-flow, performed at
  `crates/flow-nexus/src/delivery.rs:258-260`. Nothing in Flow decides to send it.
- **Flow watches transcripts** only to witness the launch receipt
  (`TranscriptWatch`, `src/launching.rs:654-710`; transcript cursor fields
  `TranscriptByteOffset` etc. in `signal.ethos:142-147`), not their size.
- **Claude Code status line** (outside Flow, user-level) displays
  `context_window.used_percentage` with colour thresholds 60/85, but only
  draws it. `/home/li/.claude/statusline.sh:14-19, 38-42`

  ```bash
  read -r ctxpct weekused weekreset effort think <<<"$(printf '%s' "$input" | jq -r '
    [ ((.context_window.used_percentage // 0) | floor)
    , ((.rate_limits.seven_day.used_percentage // 0) | floor)
    , ((.rate_limits.seven_day.resets_at // 0) | floor)
    , (.effort.level // "?")
    , (.thinking.enabled // false) ] | @tsv')"
  ```

  ```bash
  # Context: green < 60%, yellow < 85%, red beyond.
  if   [ "$ctxpct" -lt 60 ]; then ccol=32
  elif [ "$ctxpct" -lt 85 ]; then ccol=33
  else ccol=31
  fi
  ```
- User-level Claude hooks (`/home/li/.claude/settings.json`): `SessionStart`
  runs `herdr-agent-state.sh`; `PermissionRequest` runs a permission hook. The
  project `.claude/settings.json` has no hooks. Neither reads context size.
- The only `contextSize` in Nix is the local-model option of
  `CriomOS-home/modules/home/profiles/min/opencode-harness.nix:65,112,168`, a
  model configuration value, not a monitor.

---

## 6. "metaflow" / "meta_flow" / "Metaflow" in code

Observed occurrences (case-insensitive `meta_?flow|metaflow|meta-flow` over
Flow, signal-flow, meta-signal-flow, messenger-clj, message):

- `meta-signal-flow@54eb561:ethos/signal.ethos:106` `MetaFlowOwnerId.FlowId`
- `meta-signal-flow@54eb561:ethos/signal.ethos:110`
  `FlowContainer.{ HerdrSessionName HerdrServerSocketPath HerdrServerProcessIdentity MetaFlowOwnerId }`
- `meta-signal-flow@54eb561:src/generated/signal.rs:143`
  `pub type MetaFlowOwnerId = signal_flow::FlowId;` and `:161`
  `pub meta_flow_owner_id: MetaFlowOwnerId,`
- `crates/flow-nexus/src/binding.rs:64`
  `&& !self.meta_flow_owner_id.is_empty()` (in `ChecksFlowContainer::is_well_formed`)
- `crates/flow-nexus/src/lib.rs:345`
  `flow_id: container.meta_flow_owner_id.clone(),` — the owner id becomes the
  `OriginClue.flow_id` of every flow imported by `MetaBindExisting`, with
  `turn_id: "meta-bind-existing"`:

  `crates/flow-nexus/src/lib.rs:344-348`

  ```rust
                          origin_clue: signal_flow::OriginClue {
                              flow_id: container.meta_flow_owner_id.clone(),
                              session_id: container.herdr_session_name.clone(),
                              turn_id: "meta-bind-existing".into(),
                          },
  ```
- `crates/flow-nexus/src/lib.rs:935` test fixture `meta_flow_owner_id: "field-owner".into(),`
- `message@6fa4d0c:crates/message-nexus/tests/support/fake_flow.rs:65,68`
  a local variable `meta_flow` (the fake Flow's meta socket handle).

No type, module, or concept named "Metaflow" exists in code. The nearest
relatives are `MetaFlowOwnerId` (the FlowId that owns a Herdr container in a
bind-existing import) and the configuration value `MetaAspects`
(`meta-signal-flow ethos:85`; defaults to `[Psyche]` at
`crates/flow-nexus/src/store.rs:84-96`), which decides which aspects may use
Flow's meta socket.

---

## 7. "Job" and "Seat" (and Voice/Layer/Role) in Flow code

Method: `grep -rniw '<word>s\?'` over `flow/crates/{flow,flow-nexus/src,flow-nexus/ethos,flow-meta/src,flow-defaults/src}`
and the two pinned contract ethos files.

- **Job** (11 hits): only Claude Code's own job directory, never a Flow concept.
  `crates/flow-nexus/src/claude.rs:12-15, 35, 57` (`ClaudeDaemon.jobs`,
  `claude_home.join("jobs")`, `self.jobs.join(short).join("state.json")`) and
  `crates/flow-nexus/src/herdr/launch.rs:122-124` (`CLAUDE_JOB_DIR`), plus
  tests.
- **Seat** (43 hits): prose only, in doc comments and the signal-flow ethos
  commentary; no type, field, or variant. Representative:
  `signal-flow@f95034d:ethos/signal.ethos:49-51`

  ```
  ; A flow's lifecycle is what List reports of it. Pending and Active are
  ; live: a bound native seat answers. Pending is a seat not yet witnessed
  ; live; Active is one that has been.
  ```

  and `crates/flow-nexus/src/store.rs:84-86`

  ```rust
      /// Psyche seats deploy and manage flows, so they alone among flows
      /// reach the meta socket by default. No Message Nexus executable is
      /// admitted by path until one is configured.
  ```

  Other places: `src/performing.rs:128-131, 331-332, 476`,
  `src/composition.rs:163-166`, `src/delivery.rs:91`, `src/store.rs:189-192, 759`,
  `src/lib.rs:145, 226, 257, 564-573, 622-637, 2058-2117, 2207, 2229, 3178-3283`
  (many in tests), `src/herdr/launch.rs:2983`, `crates/flow/tests/hook_socket.rs:4`.
- **Voice** (1 hit): `crates/flow-nexus/src/store/events.rs:3`, quoting the
  vision's Memory shape in a doc comment.
- **Layer** (3 hits): unrelated uses ("three layers" of body refusal at
  `src/delivery/body.rs:4,13`; "integration layer" at `src/herdr/launch.rs:75`).
- **Role** (94 hits): the stored `Caller` (see 1.3), e.g.
  `operation.ethos:17` "Register binds a flow's row and role",
  `src/caller.rs:131`, `src/lib.rs:331-357`.

---

## Hypotheses (not observed; for the author to weigh)

1. FlowId's shape is enforced in three different strengths: `String` on the
   wire, lowercase-hex of any length by the `flow-id` claim parser
   (`launch.rs:368-374`), exactly six hex in `native_title`. A legacy path
   still mints `flow-{:016x}`. The ethos-zero fixture's `FlowId.Integer` looks
   like the vision's target, not today's.
2. "Role" today is `Caller = { FlowId FlowAspect PowerLevel ModelName }`; the
   vision's `Voice.[ Psyche.Rank ... ]` would appear to replace the
   `FlowAspect` + `PowerLevel` pair, with `Rank` standing where `PowerLevel`
   stands. Not confirmed by any code.
3. Three distinct `FlowLifecycle` types (wire, store-private, meta
   `RegisteredUnconfirmed`) plus the fixture's `State.[ Running Ended ]` may be
   worth one presentation block in «The code», since the same name means three
   things.
4. The messenger-clj sender is self-declared (`FLOW_ID` env), while Message
   Nexus derives it from the kernel via Flow's `ResolvePeer`. Both coexist in
   deployment; which one carries hm-send traffic is messenger-clj.
5. A "metaflow" at the centre of the design has, in code, only the seed
   `MetaFlowOwnerId` (an owner FlowId for a Herdr container) and the
   `MetaAspects` gate on the privileged socket.
6. Context-size monitoring would have no hook to stand on in Flow today: the
   injected hook covers SessionStart/PostToolUse/Stop and `Event` has no
   variant carrying a size. Claude Code's status-line input does carry
   `context_window.used_percentage`, which is the only live source observed.

## Sources

- `/git/github.com/LiGoldragon/flow` at `5e0b1bf` (0.24.0); deployed binary
  `flow-0.23.0` per `systemctl --user cat flow-nexus.service flow-nexus-next.service`.
- `signal-flow` at `f95034de0b203d886ba574fcb513c691c64b8498` and
  `meta-signal-flow` at `54eb5618e1433b68520ba9644e0428ea0f9ed75d`, read with
  `git archive` from the local clones.
- `/git/github.com/LiGoldragon/messenger-clj` at `85e71b1` (0.3.0);
  `~/.local/bin/hm-send` wrapper.
- `/git/github.com/LiGoldragon/message` `origin/main` at `6fa4d0c` (0.19.1);
  running binary `message-0.19.0`.
- `/git/github.com/LiGoldragon/ethos-zero` at `c2653dd`.
- `/home/li/.claude/statusline.sh`, `/home/li/.claude/settings.json`,
  `/home/li/primary/.claude/settings.json`.
- `/home/li/primary/SKILL_VARIABLES.md` ("Repository root: /git").
- Provenance receipt: unavailable (no PROVENANCE handoff was supplied).
