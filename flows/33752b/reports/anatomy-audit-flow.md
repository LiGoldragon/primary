# Anatomy audit, part 2: Flow, Nexus and Orchestrate sources

Completes anatomy-audit.md for 33752b, 2026-10-12. Read-only. Abbreviations:
`FL` /git/github.com/LiGoldragon/flow (HEAD ac6ab64 plus an uncommitted
diff of 29 files, workspace version 0.26.0), `OR` .../orchestrate (bc5cd36),
`NX` .../nexus (ec097e3, untracked `ethos/`), `HA` .../harness (45eb38c),
`SF` .../signal-flow (ecdce22, dirty), `SO` .../signal-orchestrate (4e68345),
`MC` messenger-clj (85e71b1), `PR` /home/li/primary. Judged against
vision-nexus.md "Three parts and one path" (Signal, Operation, Memory, "each
its own ethos specification"; "A signal reaches memory only through
operation"), its CLI line ("a Nexus knows its caller by the process, never
by a claim"), and VF lines 20-30 and 50-58 as cited in part 1.

## Sources found
- FL: Flow Nexus (`flow-nexus`, `flow`, `flow-meta`, `flow-hook`); README 1-4.
  Wire in SF and meta-signal-flow. `flow-data` holds only a README.
- OR: "a durable Lock Nexus" (README 3); wire in SO and meta-signal-orchestrate.
- NX: shared library for Nexus components (ConfigurationState, SocketAuthority,
  Situation); README 3-5. Not a running component.
- HA: Rust crate "Typed harness abstraction for Persona" plus the `flow-id`
  helper (README 3-20).
- Also present, not audited: PR/flow and PR/orchestrate (older copies in
  Primary), /home/li/wt/signal-flow, flow-test, orchestrate-test.
- Not found: any repository named `orchestrator` holding flow concepts
  (orchestrator-judge and signal-orchestrator-* exist; not read).
- Deployed (witnessed): `systemctl --user` runs flow-nexus 0.14.0
  (/nix/store/j689l7...-flow-0.14.0, up since 2026-10-08). On PATH: `flow`
  0.23.0 (~/.local/bin), flow 0.12.2 (~/.nix-profile). No `flow-hook` on PATH.
  `flow 'List.{}'` with the 0.23.0 client printed `Replaced.{ { { } } }`; the
  0.14.0 client listed 27 rows (10 Active, 8 Exited, 9 Pending).

## B1-B5 against Flow's own source

### B1 launch in Primary scripts: stands, as a bypass, not a missing capability (witnessed)
Flow implements launch: SF signal.ethos 189 `LaunchProfile.{ ... Vector<SkillName>
Aspect PowerLevel HarnessKind ModelName Effort ... SystemPromptBundleFile
InstructionPrompt }`; FL operation.ethos 33-57 (Compose, Reserve, Open, Spawn,
Bind, Title, Submit, Continue). The Primary launchers do not call it:
PR/tools/claude-main-flow-launch.mjs 277-297 mint the id with `flow-id`, open
the Herdr pane and run `claude` themselves; no launcher contains a `flow`
invocation (grep of the four launchers). Breaks: walk, turn.

### B2 layer to model: stands; Flow holds no such mapping (witnessed)
FL store.rs 96-105 `Configuration` has sockets, source root, two Codex
endpoints, harness profiles, meta aspects, message nexus path; no layer or
power to model entry. The model arrives from the caller in LaunchProfile
(SF 189; FL README 89-92). FL flow-defaults lib.rs 103 and 106 hard-code
Codex model lists per endpoint, a fourth place model names live. Breaks: turn.

### B3 lifecycle and delivery in the messenger: stands, as a parallel path (witnessed)
Flow has Stop, Retire, Exited/Retired lifecycles, Deliver under a per-pane
lease, and says "is the only writer into their panes" (FL README 4, 36).
MC writes into panes directly: core.clj 198 `(apply shell ... "herdr" args)`,
and takes its delivery lock from orchestrate (core.clj 455, 473). MC has no
call to Flow. So two pane writers and two lock homes exist. Breaks: run, stop.

### B4 identity as a FLOW_ID claim: stands, and Flow itself carries it (witnessed)
Flow resolves callers by process: FL caller.rs 1-12 (`SO_PEERCRED`, then
`HERDR_SESSION`/`HERDR_PANE_ID` read from /proc). But Flow still mints the id
through HA's `flow-id` (FL herdr.rs 133 `PathBuf::from("flow-id")`, 176), sets
it as `FLOW_ID` in the harness (operation.ethos 11; herdr/launch.rs 125-132),
and its hook reports by that claim (see N3). The pane marks are themselves
environment values a process can set when it execs (inference, not tested).
Breaks: run.

### B5 hooks not calling the Flow CLI: stands for every live flow (witnessed)
Flow writes `flow-hook` into the settings of the Claude flows it launches,
on SessionStart, PostToolUse and Stop (FL herdr/launch.rs 146-180). Report
arrived in 0.21.0 (FL UPGRADES.md 145-164); the running Nexus is 0.14.0 and
`flow-hook` is not installed. Primary's launcher installs its own hooks
(claude-main-flow-launch.mjs 154-161). Codex launches get no hook (UPGRADES
94). Breaks: run.

## New findings inside the sources

### N1. Launch policy decided by the caller, not by Flow (witnessed)
- Concept: system prompt, skill set, model, effort of a launch. Held in: the
  `Start` signal's LaunchProfile, filled by the caller (SF 189). Should be:
  Flow's Operation from the Voice alone (vision-nexus.md sample `Launch.{ Voice
  Brief.String }`; VF 26-30). Breaks: walk, turn; every caller re-decides
  policy, which is why the Primary launchers exist (B1).

### N2. The Flow CLI resolves and reorders skills (witnessed)
- Held in: FL crates/flow/src/main.rs 181-224: runs `curriculum` as a
  subprocess, refuses duplicates, moves `operation-main-flow` to the front.
  Should be: the Nexus Operation (a CLI "turns text into Signal and nothing
  more"). Breaks: turn; a Start sent without this CLI carries an unresolved
  skill list. Added in ac6ab64, 2026-10-07.

### N3. Report trusts a FlowId in the payload (witnessed)
- Held in: FL flow-nexus lib.rs 511-513 `Query::Report(report) =>
  nexus.report(report)` with no peer check, beside 515-519 where ResolveCaller
  reads the peer; reporting.rs 23-28 records under `report.flow_id`;
  flow/src/hook.rs 11-13 "The FlowId is the `FLOW_ID` the flow claimed".
  Should be: the caller resolved from the connection. Same shape: `Stop` on the
  ordinary socket checks no caller authority (lib.rs 140-170, read; no peer
  use). Breaks: run; any process can report or stop as any flow.

### N4. Flow has no Memory specification (witnessed)
- FL crates/flow-nexus/ethos holds library.ethos and operation.ethos only;
  operation.ethos 27-28: "LaunchOutcome and Replacement are the store's own
  types, imported from the Nexus crate until the Memory root is compiled."
  Memory is hand-written in store.rs (5638 lines, +2187 uncommitted, adding
  metaflow and metaflow-lock tables, store.rs 59-61). Breaks: walk; the ethos
  does not show the whole path.

### N5. Orchestrate's store holds lock policy and speaks Signal (witnessed)
- OR core.rs 142-143 hands Signal queries straight to the store
  (`self.store.lock(request)?`, `self.store.release(lock_id)?`); store
  transition.rs 52-62 decides DuplicateName and PathOverlap and returns
  `OrdinaryResponse`. OR/ethos is empty: no Operation or Memory part. Should be:
  an Operation between Signal and Memory. Breaks: walk.

### N6. Lock holder is a claim in orchestrate (witnessed)
- SO ethos 56 `LockRequest.{ LockName FlowId Vector<LockPath> LockReason }`;
  `Release.LockId` releases any lock; OR transport reads only the peer uid
  (socket.rs 125). Should be: holder from the calling process. Breaks: run.

### Checked, not misplaced
- Orchestrate carries no launch, model, Herdr or retirement concept (grep).
- Flow store.rs runs no subprocess (no `Command::new`); effects go through
  `perform(Operation::...)`, e.g. Stop: lib.rs 158-165.
- Flow holding metaflow locks matches the living's "Flow could have the lock
  on the flows" (flows/01e496/vision/flowNexus.md 7); it duplicates
  orchestrate's role only while MC still locks there (B3).
- NX holds shared configuration and socket types only.

## Welds
- W1. HA Cargo.toml 91-92 `[patch.crates-io] kameo = { git =
  ".../LiGoldragon/kameo.git", branch = "main" }`; the fork carries five local
  lifecycle commits over upstream tqwewe/kameo (f491b45 "fix lifecycle fork
  after upstream rebase", da0f64a, 1325f6a, 1980e34, 8ea1e3f). Whether
  flow-id is built with it was not checked. Witnessed.
- FL Cargo.toml 24 patches only its own `flow-ethos`; not a weld.
- Flow types into Claude panes, renames with `/rename`, reads Claude
  transcripts and passes `--settings` (FL README); these use the harness's
  outside surface, patch nothing, but depend on Claude's private transcript
  format. Lead.

## Unknowns
- Whether the uncommitted FL diff is the intended next deployment; the gap
  between running 0.14.0, PATH 0.23.0 and source 0.26.0 is unexplained.
- Whether Herdr pane marks can be forged in practice (N3, B4) was not tested.
- PR/flow and PR/orchestrate copies, signal-flow worktree, orchestrator-judge
  repositories: not read.
- No Skill tool, so `flow-evidence` was not loaded; `FLOW_ID` and
  `FLOW_DIRECTORY` were empty; no provenance receipt is available.
