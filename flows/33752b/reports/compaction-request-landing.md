# Compaction request: proposed landing for Mind Core Primary

To Mind Core Primary. A compaction request is the existing Compact command, sent as a signal to the Flow Nexus naming one flow (or a metaflow); today the Nexus types `/compact` into the flow's pane after checking only the route and a writable pane. The proposed guard sits between receiving and typing and refuses, with a typed rejection carrying the observed value, when the flow's context size is unknown or under a configured size, when the flow is younger than a configured age, or when its last compaction is more recent than a configured interval; with no guard configured it refuses every request. The design is in `flows/33752b/books/40-compaction-request.md`; this is the code landing, proposed, nothing implemented.

Open items: the Nexus's knowledge of a flow's transcript path is unchecked (without it occupancy is unknown and the request is refused); the hook `source` values (startup, resume, clear, compact) are a claim from harness hook documentation, unchecked for Codex.

Removed lines are the current source, reflowed to fit the page.

## 1. The request names a flow or a metaflow

File: `meta-signal-flow/ethos/signal.ethos`, line 164.

Removed:

```
CommandRequest.{ FlowId HarnessCommand }
```

Added:

```
CommandTarget.[ Flow.FlowId Metaflow.Address ]
CommandRequest.{ CommandTarget HarnessCommand }
```

## 2. The guard is configuration

File: `meta-signal-flow/ethos/signal.ethos`, after line 93; lines 96-100 changed.

Line 93 stays:

```
ConfigureThreshold.{ Layer Handover.Integer
  Refresh.Integer }
```

Added after it (age and interval in seconds):

```
CompactGuard.{ Size.Integer Age.Integer
  Interval.Integer }
```

Removed:

```
ConfigurationChange.[ Module.ConfigureModule
                       Model.ConfigureModel
                       Threshold.ConfigureThreshold
                       Nexus.ConfigureNexus ]
ConfigurationSnapshot.{ Nexus.ConfigureNexus
  Models.Vector<ConfigureModel>
  Thresholds.Vector<ConfigureThreshold>
  Modules.Vector<ConfigureModule> }
```

Added:

```
ConfigurationChange.[ Module.ConfigureModule
                       Model.ConfigureModel
                       Threshold.ConfigureThreshold
                       Guard.CompactGuard
                       Nexus.ConfigureNexus ]
ConfigurationSnapshot.{ Nexus.ConfigureNexus
  Models.Vector<ConfigureModel>
  Thresholds.Vector<ConfigureThreshold>
  Guard.Option<CompactGuard>
  Modules.Vector<ConfigureModule> }
```

## 3. The refusal is typed

File: `meta-signal-flow/ethos/signal.ethos`, line 167.

Removed:

```
CommandRejection.[ UnknownFlow FlowStopped
  RouteUnavailable RecipientBlocked
  UnsupportedForHarness NotDelivered
  FlowRetired FlowExited ]
```

Added:

```
CommandRejection.[ UnknownFlow FlowStopped
  RouteUnavailable RecipientBlocked
  UnsupportedForHarness NotDelivered
  FlowRetired FlowExited
  GuardUnconfigured ContextUnknown
  ContextSmall.Integer FlowYoung.Integer
  RecentlyCompacted.Integer ]
ContextSeen.{ Occupancy.Option<Integer>
  Age.Integer
  SinceCompaction.Option<Integer> }
```

## 4. The Nexus guards before typing

File: `crates/flow-nexus/src/delivery.rs`, `fn command`, lines 258-259.

Removed:

```rust
HarnessCommand::Compact => {
    let observe = matches!(agent_state,
        AgentState::Idle | AgentState::Done);
```

Added:

```rust
HarnessCommand::Compact => {
    if let Err(rejection) =
        self.compaction_guard(&target)
    {
        return Response::CommandRejected(
            rejection);
    }
    let observe = matches!(agent_state,
        AgentState::Idle | AgentState::Done);
```

Added beside `fn command`; `context_of` reads the transcript in the short term and Flow's own record in the long term:

```rust
fn compaction_guard(&self,
    target: &DeliveryTarget)
    -> Result<(), CommandRejection> {
    let guard = self.store.compact_guard()
        .ok_or(CommandRejection::
            GuardUnconfigured)?;
    guard.admits(&self.context_of(target))
}
```

```rust
impl CompactGuard {
    fn admits(&self, seen: &ContextSeen)
        -> Result<(), CommandRejection> {
        let size = seen.occupancy.ok_or(
            CommandRejection::ContextUnknown)?;
        if size < self.size {
            return Err(CommandRejection::
                ContextSmall(size));
        }
        if seen.age < self.age {
            return Err(CommandRejection::
                FlowYoung(seen.age));
        }
        match seen.since_compaction {
            Some(since)
                if since < self.interval =>
                Err(CommandRejection::
                    RecentlyCompacted(since)),
            _ => Ok(()),
        }
    }
}
```

## 5. Flow keeps how a session began

File: `signal-flow/ethos/signal.ethos`, line 278.

Removed:

```
Event.[ Started
```

Added:

```
SessionSource.[ Startup Resume Clear Compact ]
Event.[ Started.SessionSource
```

File: `crates/flow/src/hook.rs`, line 92.

Removed:

```rust
"SessionStart" => "Started".to_owned(),
```

Added:

```rust
"SessionStart" => match self
    .input
    .get("source")
    .and_then(serde_json::Value::as_str)
{
    Some("startup") =>
        "Started.Startup".to_owned(),
    Some("resume") =>
        "Started.Resume".to_owned(),
    Some("clear") =>
        "Started.Clear".to_owned(),
    Some("compact") =>
        "Started.Compact".to_owned(),
    _ => return HookCall::Nothing(
        "SessionStart without a known source"),
},
```

The Nexus stores the time of each reported start against its flow: the first is the launch, the latest `Started.Compact` the last compaction. With that record, `context_of` reads only occupancy from the transcript.
