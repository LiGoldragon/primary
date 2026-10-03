# signal-flow 9.0.0: Report, Reported, Refused.UnknownFlow

Verdict: **landed on main, green.** signal-flow main is `2cc48792`
(`2cc487923476e3c79899f1da48b03e250ae09c10`), version 9.0.0. It carries
ruling 12: `Report.{ FlowId Event }`, answered `Reported`, or refused with
`Refused.UnknownFlow.FlowId`. Nothing was deployed.

## Versions

- signal-flow 8.0.0 (`c297d987`) became 9.0.0 (`2cc48792`). The bump is
  major because `Query` and `Response` gain variants, a Rust type is renamed,
  and the contract digest changes.
- Generator: ethos-zero 16.0.0 at `0edfc0c3`, the same rev as build.rs. No
  other pin moved: signal 7.0.0 (`66e7b153`), protos 0.32.2 (`15b41da8`),
  datom-codec 0.32.2 (`4dff16b4`).
- Worktree: `~/wt/github.com/LiGoldragon/signal-flow/report-f1c841`. Lock
  11669 named only that checkout. It has been released.

## The ethos additions, verbatim

In the queries section, after `QueueTurnEnd.TurnEndRequest`:

    Report.{ FlowId Event }

In the responses section, after `TurnEndRejected.TurnEndRejection`:

    Reported
    Refused.[ UnknownFlow.FlowId ]

In the types section, last:

    Event.[ Started
            ToolUsed.String
            Stopped ]

`FlowId` is the existing `FlowId.String`. It is reused, not redeclared.
`Report.{ FlowId Event }` prints on one line because all its elements are
leaves. That matches the canonical print and the vision-ethos example.

These generate:

- `Query::Report(Report_Data { flow_id, event })`
- `Response::Reported`
- `Response::Refused(Refused_Data::UnknownFlow(FlowId))`
- `enum Event { Started, ToolUsed(String), Stopped }`

The comment block above `Signal` gains two paragraphs: one on what Report
means, and one on the rename below.

## Deviations, for the psyche seat

1. **Reuse check.** No type in the existing ethos duplicates Event, so
   nothing was reused. `FlowLifecycle.[ Pending Active Stopped Retired
   Exited ]` is Flow's account of a flow. `AgentState` is Herdr's view of a
   pane. `LaunchAttemptPhase` covers launch steps. None of them is a harness
   event.
2. **Name collision. The existing `Started` type is renamed `Launched`.**
   The file already declared `Started.{ FlowId SessionId OriginClue }`, the
   payload of the Start reply. In an enum, the generator reads a bare name
   that matches a declared type as a reference to that type, so the vision's
   `Event.[ Started …]` generated `Started(Started)`. That would make a
   harness Started carry a launch reply's fields. This was witnessed: the
   new test failed to compile, with "expected enum constructor
   `fn(signal_flow::Started) -> Event`".
   - What I did: Event is kept exactly as the vision writes it. The old
     payload type is renamed `Launched`, the vision's own name for what
     Start answers. The lines are now `Started.Launched`,
     `Launched.{ FlowId SessionId OriginClue }` and
     `Replaced.{ FlowId Launched }`.
   - Effect: only Rust names change. `signal_flow::Started` becomes
     `Launched`, and `Replaced.started` becomes `Replaced.launched`. The
     datom text and the rkyv archive of every 8.0.0 value are unchanged.
   - Alternative: rename Event's variant instead. That would change the
     vision's wording and is his call.
3. **The whole file is reprinted vertically.** The additions sit inside
   sections that were each written on one line. vision-ethos says nothing
   that has a next layer sits on one line, so I reprinted the body with
   ethos-zero 16.0.0's own `Printable`. This is a mechanical change: no
   declaration moved or changed except the three additions and the rename.
   - Check: the committed body equals `Printable::print` of itself
     byte-for-byte.
   - The comment header is kept above the body.
   - Nothing else in the file was redesigned. The repin report's vision
     conflicts 2 to 6 still stand.

## UPGRADES.md (9.0.0 entry)

- **What breaks:** the new variants; the `Started` to `Launched` rename; the
  vertical reprint, which changes `ETHOS` and so the contract digest. An
  8.0.0 peer is refused at the greeting with `ContractMismatch`.
- **What flow must implement:**
  1. Store each flow's events in its Memory, on the record of the flow the
     FlowId names.
  2. Answer a stored `Report` with `Reported`.
  3. Refuse a `Report` whose FlowId Flow does not hold with
     `Refused.UnknownFlow.<FlowId>`, and never adopt that flow.
- **The hook:** it calls the Flow CLI with `Report.{ <FlowId> Started }`,
  `Report.{ <FlowId> ToolUsed.<tool_name> }` or `Report.{ <FlowId> Stopped }`.
  It carries the FlowId from the environment Flow launched the flow with
  (`FLOW_ID`), never from the harness's session id.
- **To deploy:** repin, then handle the variants, then restart the Nexus and
  both CLIs together.

## Tests

The new file is `tests/report.rs`.

- The rkyv round-trip of every Report, Reported and Refused runs without
  `datom`.
- Under `datom`, the exact inline datoms are checked. Each expected value is
  taken from the ruling's text, not computed through the tested code:
  - `Report.{ f1c841 Started }`
  - `Report.{ f1c841 ToolUsed.Bash }`
  - `Report.{ f1c841 Stopped }`
  - `Reported`
  - `Refused.UnknownFlow.0a0a0a`
- Also under `datom`, the reader refuses a missing event, an extra field and
  an unknown event (`Paused`).
- It was first seen failing, on the collision above.

Results:

- `cargo test` (no `datom`): green. Greeting 2 and report 1; the rest is
  datom-gated.
- `cargo test --features datom`: green. contract 14, greeting 2,
  presentation_turn_end 3, report 3.
- `cargo fmt --check`: green.
- `nix flake check path:<worktree>`: exit 0, covering test, test-datom,
  fmt and the package. The tree checked is byte-identical to `2cc48792`.
- Freshness: build.rs regenerates `src/generated/signal.rs` with
  ethos-zero 16.0.0 on every build and asserts that the output is
  byte-identical. Every build above passed it.

## Red

- **The ethos-zero CLI did not run.**
  `nix run github:LiGoldragon/ethos-zero/0edfc0c3` failed to build its
  package here with "builder failed with exit code 1", and the build log
  was not kept. The generated Rust was written instead through the
  ethos-zero 16.0.0 library at the same rev: `Potential<File>` then
  `actualize` then `generate`, the path build.rs uses. The freshness
  assertion holds it.
- **Consumers are not repinned.** flow and meta-signal-flow still pin
  8.0.0, as the brief required: not my repositories, and nothing was
  deployed.
- **`nix flake check` was not run against the pushed remote.** It ran on
  the local tree only.

## Sources

- `/git/github.com/LiGoldragon/signal-flow` at `c297d987` and `2cc48792`:
  `ethos/signal.ethos`, `UPGRADES.md`, `tests/`, `build.rs`
- `/git/github.com/LiGoldragon/ethos-zero` at `0edfc0c3`: `README.md`
  (Print, the variant payload rules), `src/printing.rs`
- `/home/li/primary/flows/f1c841/rulings.md`, ruling 12
- `/home/li/primary/flows/f1c841/reports/harness-hook.md`
- `/home/li/primary/flows/f1c841/reports/flow-contracts-repin.md`
- the vision-ethos, knowledge-ethos, vision-flow and vision-nexus skills
