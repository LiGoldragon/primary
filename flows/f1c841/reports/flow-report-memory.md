# flow Report in Memory, and the hook scenario

Verdict: **all three landed on main, in order, and are green.** Nothing was
deployed. No running Nexus or profile was touched.

- meta-signal-flow 13.0.0 is on main at `dd7b7df7`.
- flow 0.21.0 is on main at `480d6b72`.
- flow-test is on main at `b0aa7c08`. Its new scenario, `flow-claude-hook`,
  was green twice: once on the local tree and once from the pushed rev.

One thing goes beyond the brief: meta-signal-flow gained a `ReadEvents`
query. The reason is under "Deviations" below.

## Versions and pins

| repo | before | after | pins |
|---|---|---|---|
| meta-signal-flow | 12.0.0 `69f9c146` | 13.0.0 `dd7b7df7` | signal-flow 9.0.0 `2cc48792`; signal 7.0.0 `66e7b153`; protos and datom-codec 0.32.2; ethos-zero 16.0.0 `0edfc0c3` |
| flow | 0.20.0 `f7230f81` | 0.21.0 `480d6b72` | signal-flow 9.0.0 `2cc48792`; meta-signal-flow 13.0.0 `dd7b7df7` |
| flow-test | `ac986bec` (input flow 0.19.0) | `b0aa7c08` | input flow `480d6b72` (0.21.0); lock updated |

**signal:** I checked main at `/git/github.com/LiGoldragon/signal`. It is
still 7.0.0 (`66e7b153`), with no newer version, and 7.0.0 already builds
on protos and datom-codec 0.32.2. So meta-signal-flow stays on signal 7.0.0.

## What Report maps to

**On the wire (signal-flow 9.0.0, unchanged):** `Report.{ FlowId Event }`
is answered `Reported`, or `Refused.UnknownFlow.FlowId`.

**Operation.** In `crates/flow-nexus/ethos/operation.ethos`, Record gains one
variant, and Failed gains `UnknownFlow`:

    Record.[ …
             Settled.{ LaunchRequestId LaunchOutcome }
             Harness.{ FlowId Event } ]
    Failed.[ … BundleRefused
             UnknownFlow ]

The variant is named `Harness` and not `Event`. A variant named `Event`
would clash with the imported `Event` type. That is the same collision
signal-flow 9.0.0 hit with `Started`.

A Report is performed like this:

1. `RunningNexus::report` performs
   `Operation::Record(Record.Harness.{ flow_id event })`.
2. The outcome becomes the reply:

| Outcome | Reply |
|---|---|
| `Recorded` | `Reported` |
| `Failed.UnknownFlow` | `Refused.UnknownFlow.<FlowId>` |
| anything else | `Refused.UnknownFlow`, and the error is logged (see red items) |

The new code is in `crates/flow-nexus/src/reporting.rs`, plus the
`Record_Data::Harness` arm in `performing.rs`.

**Memory.** New file `crates/flow-nexus/src/store/events.rs`:

- A new sema table, `flow_nexus_flow_events` (schema `flow-nexus-flow-events-v1`).
- One row per flow, keyed by FlowId:
  `FlowEvents { flow_id, event_vector: Vec<signal_flow::Event> }`. This is
  the events half of the vision's `Flow.{ FlowId Voice State Vector<Event> }`.
- An append checks that the flow row exists, then pushes the event onto the
  vector. It runs under a mutex, so two PostToolUse hooks firing at once
  cannot lose an event.
- A FlowId with no flow row gets `UnknownFlow`. No row is written, so the
  flow is not adopted (ruling 12).
- A 0.20.0 store opens unchanged. Its flows start with no events.

**Dispatch.** Report does not take the dispatch gate. A launch can wait on
the very harness whose SessionStart hook is reporting, so taking the gate
could deadlock.

**Seeing the events.** On the owner's (meta) socket:

- `ReadEvents.FlowId` answers `EventsRead.{ FlowId [ events, oldest first ] }`.
- For a flow Flow does not hold, it answers `ReadEventsRejected.UnknownFlow`.

**Stop.** Stop now sends `Report Stopped`. `QueueTurnEnd` is still refused
with `TurnEndRejected.QueueRefused`, and a test asserts it.

## The hook in Flow's launch settings

flow already wrote launch settings: every Claude launch passes
`--settings <json>`, which until now carried only `permissions.defaultMode`.
That JSON now also carries `hooks`: SessionStart, PostToolUse with matcher
`*`, and Stop. Each runs `flow-hook`, found next to the running
`flow-nexus` executable (`HerdrCli::harness_hook`). This is the same hook
configuration the sandbox used, now produced by `claude_flag_settings()`.

`flow-hook` is a new binary in the `flow` crate (`crates/flow/src/hook.rs`):

- It reads the hook's JSON from stdin.
- It builds one datom:
  - `Report.{ «FLOW_ID» Started }` on SessionStart
  - `Report.{ «FLOW_ID» ToolUsed.«tool_name» }` on PostToolUse
  - `Report.{ «FLOW_ID» Stopped }` on Stop
- It runs the `flow` CLI next to it with that datom.
- It writes one tab-separated record to stderr.
- It always exits 0.
- It takes the FlowId only from `FLOW_ID` in its environment. If there is
  none, it sends nothing.

`FLOW_ID` was added to the variables the Claude pane preparation unsets, so
a launched flow can never report under a FlowId it inherited.

## Tests

**meta-signal-flow:**
- New `tests/events.rs`: an rkyv round-trip of the new values, plus the
  exact datoms `ReadEvents.f1c841`,
  `EventsRead.{ f1c841 [ Started ToolUsed.Bash Stopped ] }` and
  `ReadEventsRejected.UnknownFlow`.
- The freshness guard was seen failing once: with the old generated module
  and the new ethos, the build script failed.
- `cargo test`, with and without `datom`: green.
- `nix flake check path:.`: green.

**flow:**
- `store::events::tests::a_flow_keeps_its_reported_events_in_order_across_a_reopen`
- `tests::a_report_is_recorded_for_a_held_flow_and_refused_for_an_unknown_one`
  covers dispatch: Report, Refused, ReadEvents, and QueueTurnEnd still refused.
- Three `flow-hook` tests: the datom for each event; no FLOW_ID means no
  call; the datom reads back as a signal-flow `Report`.
- Both store and dispatch tests were seen failing once, under a mutation
  that appended at the front instead of the back:
  `left: [Stopped, ToolUsed("Bash"), Started]`.
- The launch test now asserts the exact `--settings` JSON, written out by
  hand.
- `cargo test --workspace` (168 flow-nexus lib tests), clippy with
  `-D warnings`, and fmt: green.
- `nix flake check path:.`: all checks passed. That includes the three new
  exact checks (`flow-report-recorded-or-refused`,
  `flow-events-kept-across-reopen`, `flow-hook-reports-each-event`) and the
  no-free-functions and no-inherent-methods checks.

**flow-test:**
- `nix flake check` passed on the local tree and on
  `github:LiGoldragon/flow-test/b0aa7c08`: lint, flow, flow-populated-store,
  and the builds of both runners.
- `FLOW_TEST_LIVE=1 nix run …#flow-claude-hook` was green twice, from
  `path:.` and from the pushed rev.

## The scenario

`packages/flow-claude-hook.nix` uses three components:

- `lib/components/claude.nix`: claude-code 2.1.228 from the pinned nixpkgs.
- `lib/components/flow-hook.nix`: `flow-hook` from the pinned flow, and the
  same hook settings Flow writes.
- `lib/components/herdr-fixture.nix`: new, a fixture Herdr.

What the runner does:

1. Starts a fresh root and copies in only the credentials.
2. Starts a flow-nexus on the root, with the fixture Herdr first on its
   PATH.
3. Claims a random FlowId for a fresh session UUID (a `.<id>.flow-id`
   marker under `$HOME/primary/flows`).
4. Registers that flow over meta `RegisterFlow` at the fixture pane.
5. Asserts that `ReadEvents` answers no events, and that a Report for
   `0a0a0a` answers `Refused.UnknownFlow.0a0a0a`.
6. Runs haiku `claude -p --session-id <uuid>` with `FLOW_ID=<id>`, bounded
   as before (2G scope, 300 s, 4 turns, `Bash(echo:*)` only).
7. Checks every hook call and the events afterwards.

It also unsets every `HERDR_*` and `FLOW_*` variable from the caller's
environment.

Excerpt from the second run (pushed rev `b0aa7c08`). The full first run is
in `witnesses/flow-claude-hook-report.run.txt`:

    green: register answers FlowRegistered.{ 98845d abcec146-… Claude Unavailable Available.{ flow-hook-sandbox sandbox-claude fh:p1 fh-terminal-1 } { 98845d abcec146-… unavailable } Active }
    green: events-before-run answers EventsRead.{ 98845d [] }
    green: unknown-report answers Refused.UnknownFlow.0a0a0a
    run: exit 0, session abcec146-b906-43af-a75a-452577f2955c
    SessionStart  Report.{ «2ce2a5» Started }           0  Reported      (first run)
    PostToolUse   Report.{ «2ce2a5» ToolUsed.«Bash» }   0  Reported
    Stop          Report.{ «2ce2a5» Stopped }           0  Reported
    green: SessionStart: Report Started answered Reported
    green: PostToolUse: Report ToolUsed.Bash answered Reported
    green: Stop: Report Stopped answered Reported
    ReadEvents.98845d after the run: EventsRead.{ 98845d [ Started ToolUsed.Bash Stopped ] }
    green: the Nexus holds Started first, ToolUsed.Bash, Stopped last for 98845d
    green: unknown-still-unknown answers ReadEventsRejected.UnknownFlow
    flow-claude-hook: green

The same scenario was red on flow 0.19.0 (`witnesses/flow-claude-hook.run.txt`).
Those were its first failing runs.

The two existing scenarios, `flow` and `flow-populated-store`, are still
green on flow 0.21.0.

## Deviations, for the psyche seat

1. **ReadEvents on the meta wire.** The brief asked that "List or the
   existing observation shows the events". On signal-flow 9.0.0 neither can:
   `Listed` is a `Vector<FlowNode>`, `AgentObservation` is
   `{ FlowId AgentState }`, and neither has an events field. The brief pins
   signal-flow at 9.0.0, so I added the read to meta-signal-flow 13.0.0,
   which I was moving anyway.
   - The read belongs on the ordinary wire. Reading events is not
     privileged.
   - The vision (vision-nexus) has state observed by subscription. That
     means `AgentObservation` or `FlowNode` carrying the events in a
     signal-flow 10.0.0. It is a proposal only.
2. **The flow is registered against a fixture Herdr.** meta `RegisterFlow`
   requires a claimed identity and the pane's binding in a Herdr snapshot.
   The sandbox has no Herdr, so a fixture `herdr` answers the snapshot, the
   way flow-nexus's own tests do.
   - The flow Flow holds is real and registered. Only the pane is a
     stand-in.
   - A Flow-launched sandbox flow is still the `flow-claude` runner's
     unbuilt step.
3. **meta-signal-flow's ethos is printed vertically.** I reprinted it with
   ethos-zero 16.0.0 `Printable`. Its sections had been single lines, and
   the new inline payloads would otherwise sit on one line. The
   declarations are unchanged apart from the additions. The generated diff
   is only the three new items.

## Red, and open

- **A launched flow has no `FLOW_ID` in its harness environment.** Flow
  claims the id at Bind, after the harness has started, and spawn passes no
  `FLOW_ID`. In a real launch, the hook Flow now writes will send nothing
  until the launch carries its FlowId. And if the id is claimed only after
  SessionStart, `Started` would be refused as `UnknownFlow`. Fixing this
  needs the id claimed before spawn and passed in the pane's environment.
  That is a design change to Bind. Not done.
- **No truthful refusal for a store failure.** signal-flow 9.0.0 has only
  `Refused.UnknownFlow`. A store failure during a Report is answered with
  that and logged. A `Refused.PersistenceRefused` belongs in signal-flow.
- **Not checked against the pushed remote:** `nix flake check` was run only
  on the local trees for meta-signal-flow and flow. flow-test was checked
  against its pushed rev.
- **ethos-zero CLI:** `nix run` of it is still broken. As earlier tonight,
  I generated through the 16.0.0 library: a scratch crate calling
  `Potential<File>::actualize`, then `generate` and `print`. The build-time
  freshness checks hold the output.
- **Not deployed:** the living's flow-nexus is still on 0.20.0 or older.
  The 0.21.0 `UPGRADES.md` entry says how to deploy.

## Vision conflicts seen

- The vision-ethos Memory keeps `Vector<Event>` inside `Flow.{ FlowId Voice
  State … }`. flow keeps it in a separate table. Merging it into the flow
  row would change the v5 flow-row schema and need an upgrade.
- vision-flow says hooks reach Flow for "each flow's state without
  polling". Here the hook reaches Flow, but nothing streams events onward:
  ReadEvents is a point read, not a subscription.
- vision-flow says Flow chooses a flow's entry files. The hook now rides in
  Flow's `--settings` flag, not in an entry file. That is the surface flow
  already wrote.
- The psyche's open question still stands: is the transcript's content
  Flow's, or Transcript's? Ruling 12 sends only the event names to Flow.

## Sources

- `/git/github.com/LiGoldragon/meta-signal-flow` at `69f9c146` and
  `dd7b7df7`: `ethos/signal.ethos`, `tests/events.rs`, `UPGRADES.md`
- `/git/github.com/LiGoldragon/flow` at `f7230f81` and `480d6b72`:
  `crates/flow-nexus/{ethos/operation.ethos, src/reporting.rs,
  src/store/events.rs, src/performing.rs, src/lib.rs, src/herdr.rs,
  src/herdr/launch.rs}`, `crates/flow/src/hook.rs`, `UPGRADES.md`,
  `DESIGN.md`, `flake.nix`
- `/git/github.com/LiGoldragon/flow-test` at `ac986bec` and `b0aa7c08`
- `/git/github.com/LiGoldragon/signal` main `66e7b153`
- `/git/github.com/LiGoldragon/signal-flow` at `2cc48792`
- `/home/li/primary/flows/f1c841/reports/{signal-flow-report,harness-hook,operation-root-flow}.md`
- `/home/li/primary/flows/f1c841/rulings.md`, ruling 12
- `/home/li/primary/flows/f1c841/witnesses/flow-claude-hook/` and
  `flow-claude-hook.run.txt`
- `/home/li/primary/flows/f1c841/witnesses/flow-claude-hook-report.run.txt`
- Skills: vision-flow, vision-nexus, vision-ethos, knowledge-ethos,
  knowledge-flow, claude-harness, compensation-nix
