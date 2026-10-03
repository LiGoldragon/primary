# Flow and Message on signal 8, FLOW_ID at launch

Subflow of f1c841, 2026-10-03. Everything landed on main and was pushed,
in dependency order, and all of it is green. Nothing was deployed. No running
Nexus, profile, or other subflow's repository was touched (signal,
the orchestrate and lojix families, horizon-lib, Curriculum). The work was
done in `~/wt/github.com/LiGoldragon/<repo>/signal8-f1c841`. Orchestrate
lock 11689 named only those seven checkouts. It has been released.

## Versions

| Repository | Before | After | Main commit |
| --- | --- | --- | --- |
| signal-flow | 9.0.0 `2cc48792` | 10.0.0 | `f95034de0b20` |
| meta-signal-flow | 13.0.0 `dd7b7df7` | 14.0.0 | `54eb5618e143` |
| signal-message | 9.0.0 `0f5c0f0d` | 10.0.0 | `b94d907c4c02` |
| meta-signal-message | 0.9.0 `f8ca09fc` | 0.10.0 | `81e12b235476` |
| flow | 0.21.0 `480d6b72` | 0.22.0 | `2fa51db8d793` |
| message | 0.18.0 `64ea9eb9` | 0.19.0 | `ce3eb6c65a02` |
| flow-test | `b0aa7c08` | | `36c8d2caaaa9` |

## Pins

- **All four contracts** pin signal 8.0.0 `f35460de`, protos and datom-codec
  0.32.2 (`15b41da8`, `4dff16b4`), and ethos-zero 16.0.0 at `c2653dd8`.
  `c2653dd8` is the rev signal 8.0.0 builds with. It is one commit past
  `0edfc0c3` and changes nothing in generation. Each lock now holds exactly
  one signal, one ethos-zero, one protos and one datom-codec. Before this
  change, protos 0.31, datom-codec 0.31 and ethos-zero 10 were in the locks
  through signal 7's build script.
- **Chain:** meta-signal-flow 14.0.0 pins signal-flow `f95034de`.
  signal-message 10.0.0 pins signal-flow `f95034de` and meta-signal-flow
  `54eb5618`. meta-signal-message 0.10.0 pins those two plus signal-message
  `b94d907c`.
- **flow 0.22.0** pins signal-flow `f95034de` and meta-signal-flow
  `54eb5618`. flow-nexus's build-dependency is ethos-zero `c2653dd8`.
  sema-engine is unchanged at `516f01fe`.
- **message 0.19.0** pins exactly the revisions flow 0.22.0 holds, plus
  signal-message `b94d907c` and meta-signal-message `81e12b23`.
- **flow-test** takes flow `2fa51db8` and adds the input
  `github:LiGoldragon/harness` (locked at main `8604a073`) for its real
  `flow-id`. Both inputs follow its nixpkgs.

## The contracts (1)

- **Generated Rust is fresh and byte-identical.** Every build.rs
  regenerates from its ethos with ethos-zero 16.0.0 and asserts equality.
  `jj diff` touches only `Cargo.toml`, `Cargo.lock` and `UPGRADES.md`. So
  `ETHOS`, the contract digests, the datom text and the rkyv archives are
  unchanged. A peer on the previous release still greets this one.
- **The bump is still major,** because the re-exported signal traits
  (`Contracted`, `Signal`, …) are now signal 8.0.0's.
- **Each `datom` feature enables `signal/datom` again.** The 8.0.0 repin had
  removed it only because signal 7 bound datom-codec 0.31. signal 8 binds
  the same 0.32.2, so `cargo tree -d` still shows one codec.
- **Tests:**
  - `cargo test` (no datom) and `cargo test --all-features` were green in
    all four:
    - signal-flow: contract 14, greeting 2, presentation 3, report 3
    - meta-signal-flow: contract 9, events 2, greeting 3
    - signal-message: generated_contract 5, greeting 3
    - meta-signal-message: contract 3, greeting 3
  - `cargo fmt --check` was clean in all four.
  - `nix flake check path:.` reported "all checks passed" in each.
  - `cargo clippy --all-targets --all-features -D warnings` was clean in
    meta-signal-flow, signal-message and meta-signal-message.
- `UPGRADES.md` gained an entry in each repository.

## How FLOW_ID reaches the environment (2)

The order is flow's Operation root:
`Compose → Reserve → Record.Intent → Open → Spawn → Bind → …`.

1. **Reserve.** This is `PerformsInParts::reserve` in `performing.rs`. For a
   newly reserved Claude attempt, Flow chooses the Claude session id itself.
   - The id is UUIDv5-shaped (version nibble 5, RFC 4122 variant), taken
     from `SHA-256("flow-claude-session-v1\0" + launch_request_id)`. This is
     `ChoosesNativeSession`, in the new `herdr/reservation.rs`.
   - Flow then runs `flow-id claude --flows-root <root> --parent-session
     <session>` (`ReservesFlowIdentity`). That claims the FlowId and writes
     the claim marker before any pane or harness exists.
   - Flow holds the flow in Memory by writing its empty events row
     (`hold_reserved_flow` in `store/events.rs`). `record_event` and
     `events` now accept a flow that has either an events row or a flow row.
     That is why the hook's first `Started` is `Reported` even before
     Register.
   - The outcome is `Reserved.{ LaunchAttemptReservation Option<FlowId> }`.
   - If the claim fails, the outcome is `Failed.ClaimRefused`, answered
     `StartRejected.BindingRefused` before any pane is opened.
   - An `Existing` or `Conflict` attempt reserves nothing and is never
     spawned again.
2. **Spawn.** `PaneLaunch` carries `Option<FlowId>`.
   - The line Flow types at the pane's shell prompt still unsets the
     inherited `CLAUDE_*` variables and `FLOW_ID`. It then runs
     `export FLOW_ID=<FlowId>` (`claude_environment_preparation`).
   - `herdr agent start` starts the harness at that prompt ("the pane must be
     at its interactive shell prompt"). Claude and every hook it runs inherit
     the export.
   - Claude also gets `--session-id <session>`, so it runs as the session
     the claim names.
3. **Bind.** With a reserved FlowId, Bind refuses in two cases:
   - the session Herdr's integration reports is not the chosen one;
   - flow-id's claim names another alias.

   Both are answered `BindingRefused`.
4. **Codex, and unreserved launches.** A Codex launch reserves nothing: its
   session comes from its app server, and it binds as before. With
   `reserved` set to `None`, no FLOW_ID is exported and no `--session-id` is
   passed. The test `a_reserved_claude_launch_that_came_up_as_another_session_is_not_bound`
   asserts this. A harness without FLOW_ID gets nothing from `flow-hook`, as
   before.

Operation ethos changes:

- `Reserved.{ LaunchAttemptReservation Option<FlowId> }`
- `Failed.[ … UnknownFlow ClaimRefused ]`
- `PaneLaunch.{ ComposedLaunch HerdrPaneBinding Option<FlowId> }`

These were regenerated through the ethos-zero 16.0.0 library: a scratch
crate calling `Potential<File>::actualize` and then `generate`, the same
path build.rs uses. build.rs keeps the result fresh.

**Tests.** Each new test was first seen failing under a mutation:
- with the export removed:
  `left: "FLOW_CLAUDE_ENV_READY_test-marker\n" right: "…\n5a4d0b"`;
- with the events check put back to "flow row only":
  `left: Refused(UnknownFlow("a8a9da")) right: Reported`.

The new tests:
- `tests::reservation::a_claude_launch_holds_its_flow_id_from_reserve_before_any_harness`
- `tests::reservation::a_claude_launch_whose_flow_id_cannot_be_claimed_is_refused_before_any_pane`
- `tests::reservation::a_codex_launch_reserves_no_flow_id`
- `herdr::launch::tests::claude_environment_preparation_exports_the_reserved_flow_id`
- `herdr::launch::tests::a_reserved_claude_launch_starts_as_its_session_with_its_flow_id`
- `herdr::launch::tests::a_reserved_claude_launch_that_came_up_as_another_session_is_not_bound`

Three of them became exact flake checks:
- `flow-reserve-holds-the-flow-id`
- `flow-reserved-flow-id-reaches-the-harness`
- `flow-reserved-flow-id-in-the-environment`

`launch_status_answers_pending_and_every_outcome_once` now installs a
`flow-id` stand-in. Its Claude launch now claims at Reserve, so it can still
fail at Open as the test intends.

**Results:**
- `cargo test --workspace` was green (flow-nexus lib 174).
- `cargo clippy --workspace --all-targets -D warnings` and
  `cargo fmt --check` were clean.
- `nix flake check path:.` reported "all checks passed".
- `DESIGN.md` and `UPGRADES.md` (0.22.0) record the change.

## Message (3)

No Message source changed. The `Started`→`Launched` rename (signal-flow 9)
and `ReadEvents` (meta-signal-flow 13) touch nothing Message names.

- `cargo test --workspace` was green: message 2, defaults 1, meta 1,
  configuration_lives_in_the_store 4, message_through_flow 13.
- clippy `-D warnings` and fmt were clean.
- `nix flake check path:<copy of the tracked tree>` reported "all checks
  passed". A copy was used because of the stray `.git` above the worktree,
  as noted before.

**Live witness.** The 0.22.0 flow-nexus and the 0.19.0 message-nexus (both
debug builds) ran in a fresh HOME and XDG_RUNTIME_DIR:

- `message 'Send.{ [ 7d41e0 ] Soft Text.hello }'` answered
  `SendRejected.SenderUnknown`.
- `message-meta …` answered `SendRejected.UnknownRecipient.7d41e0`.

Both are Flow replies, decoded over the real sockets.

## flow-test (4) and scenario output

- **Pure checks.** `nix flake check` passed on the local tree and on
  `github:LiGoldragon/flow-test/36c8d2caaaa9`: lint, `flow`,
  `flow-populated-store`, and the runner builds.
- **The live scenario.** `FLOW_TEST_LIVE=1 nix run …#flow-claude-hook` was
  green twice: once from `path:.` and once from the pushed rev.
- **What step 7 drives.**
  - The sandbox Flow gets an ordinary `Start` for a Claude haiku launch.
  - The fixture Herdr answers the launch stages:
    - `workspace create`;
    - `pane run` (it keeps the typed line);
    - `wait-output`;
    - `agent start`: a shell that inherited `FLOW_ID=0c0c0c` runs the
      typed line, records `env`, and runs Claude with Flow's own agent
      arguments as `-p` with one probe prompt, bounded by a 2G scope,
      300 s and 4 turns;
    - `agent get`, reporting the passed session;
    - a snapshot that includes the launched agent.
  - The claim is made by the real `flow-id`.

Excerpt (the full first run is in `witnesses/flow-claude-hook-launch.run.txt`):

    --- step 7: a flow Flow launches
    start: StartRejected.BindingRefused
    green: the Start stops where the stand-in stops (Title): StartRejected.BindingRefused
    launched: session aa4ca62b-1baf-5207-96d8-0020546b18a8, flow aa4ca6
    green: Flow passed a --session-id
    green: the flow-id claim of aa4ca6 names that session
    --- the line Flow typed at the pane's prompt
    unset CLAUDE_CODE_CHILD_SESSION CLAUDE_JOB_DIR CLAUDE_CODE_SESSION_ID CLAUDE_CODE_SESSION_KIND FLOW_ID && export FLOW_ID=aa4ca6 && printf 'FLOW_CLAUDE_ENV_READY_%s\n' 5583b297…
    harness: exit 0, FLOW_ID aa4ca6, session aa4ca62b-1baf-5207-96d8-0020546b18a8
    green: the harness Flow launched exited 0
    green: the harness's FLOW_ID is the FlowId Flow reserved (aa4ca6), not the inherited 0c0c0c
    green: the harness ran as the session Flow chose
    ReadEvents.aa4ca6 after the launched run: EventsRead.{ aa4ca6 [ Started ToolUsed.Bash Stopped ] }
    green: the Nexus holds Started first, ToolUsed.Bash, Stopped last for the launched aa4ca6
    flow-claude-hook: green

Steps 1 to 6 (the hand-run `claude -p`) stayed green in the same run:
`EventsRead.{ 560407 [ Started ToolUsed.Bash Stopped ] }`.

**Where the stand-in stops, exactly.**
- **No Herdr server.** Herdr's real agent start, and the interactive Claude
  it would start, are not exercised. The stand-in runs Claude as `-p` with
  its own probe prompt.
- **Dropped flag.** It drops `--remote-control <name>`, which is
  interactive only.
- **Title.** It refuses the title `agent prompt … /rename`, so Title fails
  and the Start answers `StartRejected.BindingRefused`. Bind, Record
  Binding, the registration check and Register have run by then.
- **Not reached:** skill resolution, the first-prompt Submit, receipt
  observation, and the brief continuation.
- **List.** `List` shows the launched `aa4ca6` row `Active`. List projects a
  row as Herdr shows it, and the stand-in's snapshot shows the agent idle.
- Everything up to Title, and all three hook Reports, ran for real.

## Red and open

- **Codex launches get no FLOW_ID at launch.** Their session id is named by
  the app server after the harness starts, so Flow cannot claim the FlowId
  first. The hook is Claude-only today, so nothing reports for Codex. A fix
  would need Codex to accept a chosen thread id, or the FlowId minted apart
  from the session.
- **Collision with a reused launch request id.** The session id is a pure
  function of the launch request id. Within one store a request is never
  spawned twice. But another store (another Capsule or a fresh sandbox)
  launching the same request id on the same `~/.claude` would ask Claude
  for a session that already exists. Callers must keep request ids unique.
- **A refused launch keeps its held flow.** A launch refused after Reserve
  keeps its empty events row and its flow-id claim. That is a ledger record
  with no flow row; nothing removes it.
- **Not checked against the pushed remote:** `nix flake check` on the
  contracts, flow and message ran on local trees only. flow-test was
  checked from its pushed rev.
- **Clippy on signal-flow.** It fails on `large_enum_variant` in its own
  generated module. This was already true before this change, and its
  flake has no clippy gate.
- **ethos-zero CLI.** `nix run` was not attempted again; the library path
  was used.

## Vision conflicts

1. **Flow mints the FlowId, but not by naming the flow.** vision-flow says
   Flow launches a flow and names it, and that a flow id is for the ledger
   and is written in words. Here the id is still flow-id's six-hex prefix of
   a session UUID Flow chose. Flow now owns the moment of minting (Reserve,
   before Spawn). It does not yet own the name, and the name is not words.
2. **Memory shape.** A reserved flow is held by an events row with no
   `Flow` row. vision-ethos's Memory is
   `Flow.{ FlowId Voice State Vector<Event> }`, one record per flow. Folding
   the events into the flow row would need a v5→v6 flow-row upgrade.
3. **The Operation sections are still marked proposed.** I extended
   `Reserved`, `Failed` and `PaneLaunch` within a root whose sections the
   living has not yet ruled.
4. **Datom in the Nexus.** vision-nexus says datom is compiled out of a
   Nexus. flow-nexus already enables meta-signal-flow's `datom` for one
   rendering. Because the contracts' `datom` now enables `signal/datom`,
   signal's derives also compile into flow-nexus. The surface grows
   slightly; it is not a new kind of breach.
5. **The scenario polls.** It waits on the launched harness with
   `tail --pid`, which polls inside coreutils, bounded at 330 s. A hook or
   unit end would be the event-driven wait.
6. Still standing from earlier tonight:
   - the hook rides in `--settings`, not in an entry file;
   - `ReadEvents` is a point read, not a subscription;
   - the contracts' ethos holder types and the missing Library root
     (`flow-contracts-repin.md`, `message-repin.md`).

## Sources

- Repositories under `/git/github.com/LiGoldragon/`, at the main commits
  above, and their worktrees `~/wt/github.com/LiGoldragon/*/signal8-f1c841`:
  - flow: `crates/flow-nexus/{ethos/operation.ethos, src/herdr/reservation.rs, src/herdr/launch.rs, src/performing.rs, src/launching.rs, src/store/events.rs, src/tests/reservation.rs}`, `DESIGN.md`, `UPGRADES.md`, `flake.nix`;
  - flow-test: `packages/flow-claude-hook.nix`, `lib/components/{herdr-fixture,flow-id}.nix`.
- signal `UPGRADES.md` at `f35460de` (8.0.0).
- harness `src/flow_id.rs` at `8604a073`: the claim alias is the shortest
  free prefix of the identity, and a Claude identity is a v4 or v5 UUID.
- `herdr agent start --help`: "The pane must be at its interactive shell
  prompt".
- `flows/f1c841/reports/{flow-contracts-repin,message-repin,signal-flow-report,flow-report-memory}.md`.
- `flows/f1c841/witnesses/flow-claude-hook-launch.run.txt`, the first live
  run.
- Skills: vision-flow, vision-nexus, vision-ethos, knowledge-ethos,
  knowledge-flow, claude-harness, compensation-nix, testing, versioning,
  breaking-upgrades.
