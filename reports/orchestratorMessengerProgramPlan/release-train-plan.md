# Messenger–Liveness Release Train — executable program plan

Status: dispatch-ready plan for the manager. Psyche-settled program: "yes,
messenger-first, liveness first". Translates the psyche-ruled designs into
ordered work packets, each sized for a single fresh-context implementer unless
marked otherwise.

Owning lane: `ProgramPlan` (session `OrchestratorMessenger`), 2026-07-17.

Authoritative inputs (this plan decides sequencing and packaging only; design
authority stays with these):

- `reports/coordination-liveliness-messenger/design.md` — B-ruling revision with
  2026-07-17 psyche rulings folded in (§0b, §2g, §3, §7, §7b).
- `reports/orchestrator-messaging-design/orchestrator-messaging-design.md` —
  settled messaging spec, amendments 1–8.
- `reports/messenger-router-ground-truth/messenger-router-ground-truth.md` —
  landed-code ground truth.
- `reports/harness-remote-control-interfaces.md` — per-harness delivery reality.
- Orchestrate-main scout map (manager session, 2026-07-17): present/absent
  capabilities at tip `4c047209` (v0.7.2), extension points, and the two
  recorded debts (no sema-engine family-evolution primitive; store-format stamp
  not atomic with family registration).

Adopted manager leans (psyche: "go with your leans, good enough for me"):
the messenger owns the authoritative process↔ID map with orchestrate discovery
as a feed; terminal-cell acquires the agent ID at launch and delivers it in the
initial prompt. **[Both leans superseded same day — see pending amendment
below.]**

## PENDING AMENDMENT (2026-07-17, third psyche batch — not yet restructured)

This plan predates the psyche's dictated third batch (recorded in
`reports/coordination-liveliness-messenger/design.md` §0d) and two same-day
rulings. The packet structure below is NOT yet reshaped; treat this note as
authoritative over conflicting packet text until a plan revision lands:

1. **Mint authority ruling (supersedes the leans above and reshapes phase 2).**
   Verbatim: "the mint is the orchestrator. he creates an agent id and will
   eventually launch it (through another daemon I think; maybe agent has all
   the harness launching logic - but where is that now? Or was it harness?
   thats fine too)". The orchestrator mints (ID allocated to the process
   before it starts) and launch delegates through the harness component
   (orchestrate→harness via `meta-signal-harness`); terminal-cell keeps
   PTY/session-dir duties beneath it, but is no longer the minter. Packet 2.1
   as built keeps its durable registry as the consumer view of IDs + threads;
   the mint operation relocates orchestrator-side. Reshape scope: packets
   2.1-amend / 2.2 / 2.3 — tracked as bead `primary-sdgy`.
2. **MVP merge ruling.** Verbatim: "we'll build review into that later. first
   MVP doesnt, just merge in main" — a finished feature branch that rebases
   cleanly merges into main automatically, no review gate; review is
   deferred-explicit (bead `primary-njmu`).
3. **New now-scope feature set (bead `primary-qz9l`).** Release-time
   branch-started message to the releasing main-lane holder; automatic
   "repo is taken" contention answer; PascalCase feature-named lane
   registration becomes the feature branch; default auto-worktree in a known
   place; orchestrator-tracked auto-rebase keeping mains clean. Slots into the
   train as new packets (likely phase 2/3 neighbors); not yet numbered.
4. **Subscription primitive** (when-X-happens / when-lane-ends notify): liked,
   explicitly deferred — "That's a cool idea, but for now…". Stays future
   scope; do not build in this train.

## Train overview

Train name: `messenger-liveness`. Intent file:
`release-trains/messenger-liveness.nota` (packet 0.3; follow the existing
release-trains location convention in primary if one already exists).

Repos in the train: `orchestrate` (+ `signal-orchestrate`), `message`
(component "messenger", + `signal-message`), `router`, `terminal-cell`,
`harness` (+ `signal-harness`, delivery leg only), `signal-orchestrator-message`
(existing separate contract crate, integrated in phase 3).
`signal-orchestrator-judge` is NOT in the train (judge shelved per amendment 1).
`spirit` is read-only reference for the short-hash mint discipline
(`repos/spirit/src/store/record_identifier.rs`).

Expected bases: resolve at intent-authoring time; orchestrate base is
`4c047209` (v0.7.2) or its then-current pushed main. Production note: v0.7.2
deployment is in flight (watcher waiting on the recovery lane); the train
builds on v0.7.2 semantics either way.

```
Phase 0  Foundations         0.1 reply-reliability gate (parallel investigation)
                             0.2 migration safety + Mirror coverage check
                             0.3 train intent authoring
                             0.4 real repo identity (CONDITIONAL — psyche)
        |
Phase 1  Liveness            1.1 pidfd exit watch -> typed Dead/Crashed status
                             1.2 activity read (transcript + child tree)
                             1.3 Suspect+grace fold-in (coordinate w/ existing lane)
        |
Phase 2  Launch identity     2.1 messenger.sema birth: identity/delivery registry
                             2.2 terminal-cell launch mint + initial prompt
                             2.3 orchestrate binds pre-minted ID
        |
Phase 3  Messenger promotion 3.1 messenger.sema: ledger/inbox/thread index
                             3.2a messenger delivery leg (actors move in)
                             3.2b router shrink to host-to-host + stub
                             3.3 orchestrate -> messenger reachability push
                             3.4 Send/triage wire integration
                             3.5 PtySocket end-to-end proof
        |
Phase 4  Cold delivery       4.1 killed mark + resume identity plumbing
                             4.2 respawn-by-resume legs (pi, claude)
                             4.3 dead-agent bounce (interim, primary-pm92)
        |
Phase 5  Rename sweep        5.1 orchestrate->orchestrator, message->messenger
```

Standing constraint on every store-touching packet: any new or changed sema
family MUST (a) ship its consumer-side migration (no engine evolution primitive
exists yet — recorded debt), and (b) be added to the version-handover Mirror
snapshot (`orchestrate/src/handover.rs`) or it silently drops on handover.
Packet 0.2's check makes (b) mechanical.

## Phase 0 — Foundations

### 0.1 Daemon reply reliability (GATE, placeholder)

An agent reported a `ConcludeWorktree` teardown failure: the daemon connection
ended before the complete reply ("failed to fill whole buffer"); teardown was
not confirmed; workspaces were left intact; crash vs broken connection is
undistinguished. Investigation is running in parallel (separate session); this
packet is a placeholder, not dispatchable from this plan.

- Repos: `orchestrate` (likely reply write path or socket lifecycle), possibly
  `signal-orchestrate` framing.
- Dependency edge: gates TRUST in phase 1 — liveness/abandonment must not go
  live on a daemon whose replies can truncate mid-operation, because a
  truncated conclusion is exactly what the abandonment machinery would then
  act on. Phase 1 code may land, but its activation waits on this diagnosis.
- Verification: reproduce or root-cause the truncation; regression test on the
  reply path.
- Single fresh context: yes, once the parallel investigation reports.

### 0.2 Migration safety + Mirror coverage (accepted by psyche)

- Content: automatic pre-migration store backup inside the daemon's migration
  path (before any `OrchestrateStoreMigration` runs, snapshot the store using
  the existing preserve-naming convention); migration tests against captured
  real stores (fixtures from the preserved production copies already on disk);
  a check that every registered sema family is carried by the handover Mirror
  snapshot (protects every later packet mechanically).
- Repos: `orchestrate`. Store families: none added; migration machinery only.
- Depends on: nothing. Everything store-touching depends on it.
- Verification: migration test suite green against at least one captured real
  store; a deliberately-omitted-family fixture fails the Mirror check.
- Single fresh context: yes.

### 0.3 Train intent authoring

- Content: author `release-trains/messenger-liveness.nota` per the
  release-train skill — component selectors, exact expected bases resolved to
  pushed commits, admitted externals (none expected). Candidate branches are
  `train/messenger-liveness` scoped, integration artifacts only.
- Repos: primary (intent file); no component edits.
- Depends on: nothing; must exist before the first cross-repo verification.
- Verification: resolver accepts the intent; closure resolves; loud failure on
  selector drift.
- Single fresh context: yes.

### 0.4 Real repo identity (CONDITIONAL — psyche sequencing open)

`StoredRepository` is name + local path only; the psyche has ruled repo
identity is real identity with path incidental, and the never-fork guard's
repo-level block entries need it. Either an early packet here or deferred to
the never-fork train — psyche's call (open question 3).

- Repos: `orchestrate` (+ `signal-orchestrate` if the repo vocabulary is on the
  wire). Store family change: `StoredRepository` gains real identity (remote
  URL/identity); migration + Mirror addition required.
- Depends on: 0.2.
- Verification: migration test from a captured store; identity round-trip.
- Single fresh context: yes.

## Phase 1 — Liveness (liveness-first per ruling)

### 1.1 Kernel exit watch + typed death

- Content: `HarnessLivenessWatch` IO actor epolls `pidfd`s opened from
  reachability records (`harness_pid` verified against `harness_start_time` to
  defeat pid reuse); harness exit re-enters the daemon via the Signal socket
  (the `LaneReclaimer` pattern); the owning agent gets a TYPED dead/crashed
  status — no longer indistinguishable from idle. Store change: agent status
  vocabulary gains the death state (this is also the "killed mark" source that
  phase 4 consumes).
- Repos: `orchestrate`; `signal-orchestrate` only if status is wire-visible in
  observations.
- Depends on: 0.2 (family change). Activation trust gated by 0.1.
- Verification: spawn a real process, register reachability at it, kill it,
  witness the typed transition via `Observe`; pid-reuse fixture (same pid, new
  start time) does NOT fire.
- Single fresh context: yes.

### 1.2 Activity read (psyche-ruled §3.3)

- Content: on the `Active→Suspect` transition (never on a clock), read the
  agent's REAL latest activity: harness transcript/output recency and the
  harness pid's live child-process tree. A live busy child (e.g. an hours-long
  build) is positive liveness; output silence alone never judges Suspect/dead.
  Concrete activity sources are implementer matter per the design.
- Repos: `orchestrate`.
- Depends on: 1.1 (transition machinery), 1.3 (Suspect state exists — see
  coordination note).
- Verification: fixture with a long-running child process reads alive under
  output silence; fixture with no output and no children reads Suspect.
- Single fresh context: yes.

### 1.3 Suspect + grace unified abandonment (COORDINATE FIRST)

The design doc records companion lane `LaneAbandonmentMachinery` (session
`WorktreeLifecycle`) as implementing §4 against landed `ConcludeWorktree` —
status today unknown. This packet begins by observing that lane's state and
its landed commits; it folds in only what is missing:

- §4c last-resource-release rule (last claim released or last worktree
  concluded → immediate `Suspect`, accelerated grace entry, no hard cascade).
- Durations as tunable constants: idle backstop 6h, grace 15min, terminal
  retention 1h.
- Detection wiring from 1.1/1.2 signals into `Active→Suspect`.
- Repos: `orchestrate`.
- Depends on: 1.1; coordination check on the in-flight lane (do not duplicate
  or collide — if that lane is live, this packet routes additions through it).
- Verification: grace expiry runs the §4a terminal sequence (release claims →
  `ConcludeWorktree` branch on `PushedState` → retire lane); voluntary
  conclusion re-enters `Active` on touch within grace.
- Single fresh context: yes, given the coordination check.

## Phase 2 — Launch-minted identity (psyche-ruled §7)

### 2.1 messenger.sema birth: identity + delivery registry family

- Content: the messenger's first durable family — the process↔ID map and local
  delivery registry (one family per §2g: agent ID → live endpoint, harness
  resume identity, killed/dead mark, pid + start time). A messenger operation
  for launch-time identity acquisition (e.g. `AssignAgentIdentity`: pid, start
  time, resume identity in → new or reused ID out), using spirit's mint
  discipline (random base36, 4 chars growing on conflict; uniqueness domain =
  this map). This honors both adopted leans: terminal-cell acquires at launch;
  the messenger owns the map and therefore the uniqueness check. If the
  implementer finds a materially simpler local-mint-with-conflict-retry shape,
  that is implementer matter INSIDE the invariant "messenger owns the
  authoritative map".
- Repos: `message`, `signal-message` (new operation + reply vocabulary).
- Store: `messenger.sema` created (flips the "SEMA honestly empty" invariant in
  the message ARCHITECTURE — rewrite it in this packet).
- Depends on: 0.2 discipline (new store; messenger has no Mirror equivalent —
  confirm whether messenger participates in any handover snapshot; if not,
  note that in ARCHITECTURE).
- Verification: mint round-trip; conflict growth; resume reuse; registry
  persistence across daemon restart (the durability the router registry never
  had).
- Single fresh context: yes.

### 2.2 terminal-cell launch mint + initial-prompt delivery

- Content: at session spawn, terminal-cell acquires the agent ID from the
  messenger (2.1 operation) — or reuses the session's existing ID on resume —
  writes it into the session directory (alongside `child.pid`/`data.sock`),
  injects it into the agent's initial prompt ("you are agent <id>"), and the
  registration also records the session's resume identity. Resume detection and
  ID persistence live in the session directory.
- Repos: `terminal-cell`.
- Depends on: 2.1.
- Verification: launch → agent's initial prompt carries the ID; relaunch with
  resume → same ID; messenger map shows the live pid for the ID.
- Single fresh context: yes.

### 2.3 orchestrate binds the pre-minted ID

- Content: registration BINDS the already-minted ID; it no longer mints
  (amendment 8). Orchestrate's reachability discovery already walks to the
  terminal-cell session directory — it now also reads the launch-minted ID
  there and binds the registration to it. Whether `RegisterAgent` additionally
  carries the ID on the wire is a contract decision for the implementer (the
  discovery-read path needs no request change and keeps the no-caller-supplied
  -reachability rule; a wire slot would need `signal-orchestrate` vocabulary) —
  decide inside the packet, record in ARCHITECTURE.
- Repos: `orchestrate` (+ `signal-orchestrate` if the wire slot is chosen).
- Depends on: 2.2.
- Verification: register from a terminal-cell session → registry keyed by the
  launch ID; the minted-at-registration path is gone.
- Single fresh context: yes.

## Phase 3 — Messenger promotion (B1)

### 3.1 Message families: ledger, inbox, thread index

- Content: `messenger.sema` gains the message ledger (slots + commit time),
  per-recipient inbox, and thread index (threads are plain sender-chosen
  names; membership is transport-level; no thread field in the semantic
  payload).
- Repos: `message`.
- Depends on: 2.1 (store exists), 0.2 discipline.
- Verification: submit → ledger row + inbox row; thread listing; restart
  persistence.
- Single fresh context: yes.

### 3.2a Messenger delivery leg

- Content: the local delivery actors move INTO the messenger: delivery attempt
  (PtySocket `'P'` frame to terminal-cell `data.sock`; HarnessSocket
  `MessageDelivery` to the harness daemon), pending/backpressure queue, local
  routing decision. Resolution now reads the messenger's OWN durable registry
  (2.1), not the router's in-memory map. Delivery subscription surface (harness
  subscribes once; messenger pushes inbox + deltas) lands here or is stubbed
  typed — implementer sizing call.
- Repos: `message` (+ `signal-message`, `signal-harness` read-only contract
  use).
- Depends on: 2.1, 3.1.
- Verification: local Send lands in a live terminal-cell PTY via the messenger
  path with the router NOT in the loop; queue drains on endpoint appearance.
- Single fresh context: borderline — the heaviest code packet; keep 3.2b out
  of it deliberately.

### 3.2b Router shrink + external-host stub

- Content: remove the local-delivery reducer from the router
  (`harness_delivery.rs`, `harness_registry.rs`, `delivery.rs`, `route.rs`,
  local `message.rs`, local tables); router keeps only the host-to-host trust
  plane (peer sessions, attestation, adjudication set). The messenger's Nexus
  gains the `ExternalHost` escalation, stubbed as typed
  `RequestUnimplemented(NotInPrototypeScope)`. No local traffic touches the
  router. Rewrite both ARCHITECTUREs (messenger: stateful owner; router:
  host-to-host only).
- Repos: `router`, `message`.
- Depends on: 3.2a (delivery must live in messenger before it leaves router).
- Verification: router builds and runs with no local-delivery surface; remote
  vocabulary intact; messenger local delivery still green (3.2a tests).
- Single fresh context: yes.

### 3.3 Orchestrate → messenger reachability push

- Content: per push-not-pull, orchestrate is the producer and PUSHES agent
  registration + reachability (terminal-cell endpoint or remote-host marker)
  into the messenger's delivery registry via a subscription; the messenger
  never polls. Replaces the router `RegisterActor` propagation leg
  (`router_registration.rs`) — that leg retires with it. Death/killed
  transitions (1.1) ride the same push (consumed in 4.1).
- Repos: `orchestrate`, `message`, `signal-message` (subscription vocabulary).
- Depends on: 2.1; 1.1 for the death events (can land with a stub death event
  if phase 1 activation is still gated by 0.1).
- Verification: register an agent → messenger registry row appears without any
  messenger poll; kill → killed mark arrives.
- Single fresh context: yes.

### 3.4 Send/triage wire integration

- Content: orchestrate's message-facing wire goes live: integrate the existing
  `signal-orchestrator-message` payload crate (Guidance Soft|Standard|Hard,
  Interruption, Report); the stored triage vocabulary
  (`StoredOrchestratorTriageRecord`) gains its wire driver on the ordinary
  tier following the `RegisterAgent` dispatch pattern
  (`execution.rs` ordinary arm + `schema/nexus.schema`). Judge stays shelved:
  triage without a judge routes as-is; escalation with no registered
  coordinator returns the typed missing-coordinator error (amendment 2).
  Spawning stays inexpressible.
- Repos: `orchestrate`, `signal-orchestrate`, `signal-orchestrator-message`
  (dependency integration; crate itself already built).
- Depends on: 3.2a (a Send must deliver), 3.3 (resolution data present).
- Verification: contract round-trip tests; a Send from a registered agent to
  another lands via messenger delivery; triage record persisted and bounded.
- Single fresh context: yes.

### 3.5 PtySocket end-to-end proof

- Content: the ground-truth report's named gap — the orchestrate-discovered
  PtySocket → terminal-cell path has NO end-to-end test (harness e2e tests
  exercise the HarnessSocket topology only). Build the e2e: real terminal-cell
  session, real registration + discovery, real Send, message renders in the
  live PTY. Also settles by test which topology is default for a real
  registered agent (discovery hard-maps to PtySocket today).
- Repos: `message` or a cross-repo test home per the testing skill (stateful
  test, named resources, socket under a short `/tmp/<lane>/` run root).
- Depends on: 3.2a, 3.3.
- Verification: the e2e itself, in the flake's stateful test outputs.
- Single fresh context: yes.

## Phase 4 — Cold-session delivery (psyche-ruled §2g)

### 4.1 Killed mark + resume identity plumbing

- Content: the delivery registry's killed/dead mark is fed by liveness (1.1 via
  3.3 push); resume identity captured at launch (2.2) is confirmed present for
  every registered agent. The three-way delivery decision becomes data-driven:
  live endpoint → deliver; cold + not killed → respawn; killed → bounce.
- Repos: `message`, `orchestrate` (push side).
- Depends on: 1.1, 2.2, 3.3.
- Verification: kill a registered harness → registry shows killed within the
  push latency; resumed session shows same ID with fresh endpoint.
- Single fresh context: yes.

### 4.2 Respawn-by-resume legs (pi, claude first)

- Content: for a cold (not-killed) target, the messenger records the message in
  inbox/ledger as always AND respawns the harness by its stored resume
  identity with the message arriving as the resumed session's next turn.
  Respawn is mechanically per-harness: pi via the harness daemon or
  terminal-cell relaunch with resume; claude via `claude --resume <session-id>`
  (a NEW process appending a turn to the persisted transcript — the
  industry-standard Traycer-shape mechanism; there is no live-TUI reattach for
  a plainly-launched claude). Codex leg deferred (controller-owned sessions
  only upstream; see open question 6). The spawn effect executes through
  terminal-cell so the respawned session gets a session directory, its
  existing ID (2.2 resume path), and future reachability.
- Repos: `message`, `terminal-cell` (spawn surface), `harness` (pi leg if the
  harness daemon owns the pi resume).
- Depends on: 4.1, 2.2.
- Verification: send to a cold pi session → session resumes and the message is
  its next turn; same for claude; ledger marks delivered-on-resume.
- Single fresh context: borderline — if the two harness legs prove heavy,
  split per harness; the decision shape is one packet.

### 4.3 Dead-agent bounce (interim; hedge primary-pm92)

- Content: killed target → no respawn; the message bounces to the sender with
  a dead-agent notice. Interim per the psyche's verbatim "for now" (tracked as
  bead `primary-pm92`); implement minimally, mark the bounce reply type as the
  interim surface so the permanent disposition can replace it cleanly.
- Repos: `message`, `signal-message` (bounce reply vocabulary).
- Depends on: 4.1.
- Verification: send to a killed agent → sender receives the typed bounce; no
  respawn attempted.
- Single fresh context: yes.

## Phase 5 — Rename sweep (B4, last)

### 5.1 Both renames, one mechanical sweep

- Content: exactly as design §6, only after everything above is merged and the
  tree quiescent: `orchestrate→orchestrator` and `message→messenger` — crates,
  identifiers, binaries, sockets, env names, contracts
  (`signal-orchestrate→signal-orchestrator`,
  `signal-message→signal-messenger`, meta variants), repo directories, GitHub
  remotes (auto-redirect), ghq paths, workspace links. Rename-propagator
  rewrites every `Cargo.toml` dep and `use` path atomically; no shim unless a
  crates.io external dependant is found (check first; default: none).
- Repos: all train repos + primary links.
- Depends on: phases 1–4 merged + quiescent.
- Verification: whole-train build + checks green post-sweep; no old-name
  references (`rg` sweep); sockets come up under new names.
- Single fresh context: one accountable generalist with the propagator; large
  but mechanical.

## Dependency edges (compact)

```
0.2 -> {0.4, 1.1, 2.1, 3.1, 4.1}          (store-touching discipline)
0.1 -> activation of {1.1, 1.2, 1.3}       (trust gate, code may land)
0.3 -> first cross-repo train verification
1.1 -> 1.2 -> (1.3 wiring)                 1.1 -> 4.1
2.1 -> {2.2, 3.1, 3.2a, 3.3}               2.2 -> {2.3, 4.2}
3.1 -> 3.2a -> {3.2b, 3.5}                 3.3 -> {3.4, 3.5, 4.1}
3.2a -> 3.4                                4.1 -> {4.2, 4.3}
{all} -> 5.1
```

Parallelizable from day one: 0.2, 0.3, 1.1, 2.1 (four independent starts).
The critical path to a working messenger is 2.1 → 3.1 → 3.2a → 3.4.

## Never-fork guard attachment points (not built here; not precluded)

- Repo-level block entries: a new sema family neighboring the worktree
  registry (`repository|branch`, `owning_lane`, status), trigger point at the
  claim/lane release path (`src/claim.rs` / `src/lane.rs`) — nothing in this
  train occupies or reshapes those seams.
- Requires real repo identity (packet 0.4 / open question 3).
- The liveness machinery (phase 1) is the guard's release valve for
  crashed-agent wedges — this train delivers it.

## Open questions — psyche authority, NOT decided here

1. Claude subagents in the ID model (§7b, psyche's own open question): how do
   subagents running inside a harness process — with no separate process for
   the messenger to map — fit the launch-minted ID scheme? Manager proposal on
   file (parent's ID/endpoint, parent relays, optional hierarchical suffix);
   contracts must not bake subagent addressing until ruled.
2. Sema-engine family-evolution primitive: recorded debt says the raw-catalog
   migration workaround "needs a psyche design decision". This train ships
   hand-written migrations under 0.2 discipline either way; whether to invest
   in the engine primitive (and its shape) is the open design decision.
3. Real repo identity sequencing: early train packet (0.4) or deferred to the
   never-fork guard train?
4. Harness lifecycle push subscription (design §3 open producer question):
   should the harness daemon grow a push lifecycle event stream
   (idle/stalled/resumed/exited) so liveness stops depending on exit-push +
   activity reads alone? Scope and priority are the psyche's.
5. Claude Code live-session delivery posture: pushing into a LIVE claude TUI
   requires launching sessions with the cooperative Channels flag (unverified
   on the installed build); otherwise claude delivery is cold-respawn only
   (4.2). Is requiring a launch flag on claude sessions acceptable, and is the
   cloud Remote Control path off-limits? (Carried from the harness report's
   decision items.)
6. Codex delivery leg: upstream supports controller-owned sessions only (no
   attach to a human-launched TUI). Defer the codex leg, or adopt
   spawn-through-app-server for codex sessions so they are drivable from birth?

## Unknowns for implementers (not psyche-blocking)

- `LaneAbandonmentMachinery` lane status (packet 1.3 checks first).
- Whether the messenger participates in any version-handover snapshot (2.1
  records the answer in ARCHITECTURE).
- Which prior proof "RPC steer verified" used (intercom vs `--mode rpc`) —
  affects nothing in this plan; pi leg specifics settle inside 4.2.
- The 0.1 truncation root cause (parallel investigation owns it).
