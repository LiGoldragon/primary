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

**Revision 2 (2026-07-18).** The 2026-07-17 PENDING AMENDMENT is folded into
the packet structure below; this plan now matches the rulings in design §0d
and the fourth-batch blessing in design §0e ("go with your leans, and report
back with visuals"). Superseded lean history lives in design §0c/§0d; the
governing identity shape here is: **the orchestrator mints the agent ID
before the process starts and PUSHES identities into the messenger's
registry; launch delegates through the harness component
(orchestrate→harness via `meta-signal-harness`); terminal-cell keeps
PTY/session-dir duties beneath; the messenger holds the consumer view — IDs
and threads — and "gets the list" by reading its own pushed-to registry**
(push-vs-pull reconciliation recorded in design §0e, manager-applied,
flagged). The subscription primitive (when-X-happens / when-lane-ends notify)
remains liked-but-deferred — not in this train.

Parallel-dispatch note: the mint-relocation implementer (bead `primary-sdgy`,
packet 2.1a) and the contention-flow MVP implementer (bead `primary-qz9l`,
phase 2b) are dispatched in parallel with this revision; those beads' briefs
are authoritative for their packet scope.

**Integration status (2026-07-17 integration pass + 2026-07-18 deploy):**
packets 0.1 (both halves), 0.2, 1.1, and 2.1-as-built are LANDED on all
mains — schema-rust 0.9.0 (backport line `bc964c4f` published for current
consumers), signal-orchestrate 0.6.0, meta-signal-orchestrate 0.5.0,
orchestrate 0.8.0 (`e86502a1`), signal-message 0.5.0, message 0.7.0.
Production: v0.7.2 deployed 2026-07-17 18:16; v0.8.0 deployment dispatched
2026-07-18 under the blessing.

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

Expected bases: resolve at intent-authoring time; orchestrate base is now
`e86502a1` (v0.8.0 on main). Production: v0.7.2 live since 2026-07-17 18:16;
v0.8.0 deployment dispatched 2026-07-18.

```
Phase 0  Foundations         0.1 reply-reliability + teardown fix     [LANDED]
                             0.2 migration safety + Mirror coverage   [LANDED]
                             0.3 train intent authoring
                             0.4 real repo identity                   (primary-9wxr)
                             0.5 sema-engine evolution primitive      (primary-rlg7)
        |
Phase 1  Liveness            1.1 pidfd exit watch -> typed Dead       [LANDED]
                             1.2 activity read (transcript + child tree)
                             1.3 Suspect+grace fold-in (coordinate w/ existing lane)
        |
Phase 2  Launch identity     2.1 messenger.sema identity/delivery registry [LANDED,
                                 as-built mint pending 2.1a relocation]
                             2.1a mint relocation -> orchestrator     (primary-sdgy)
                             2.2 orchestrator pre-launch mint + launch via
                                 harness; terminal-cell session-dir + initial
                                 prompt beneath
                             2.3 registration binds the pre-minted ID
        |
Phase 2b Contention-flow MVP 2b.1 repo-taken automatic answer         (primary-qz9l)
                             2b.2 feature-named lane -> auto-worktree + branch
                             2b.3 release-time branch-started message
                             2b.4 tracked auto-rebase; MVP auto-merge to main
                                  (review deferred: primary-njmu)
        |
Phase 3  Messenger promotion 3.1 messenger.sema: ledger/inbox/thread index
                             3.2a messenger delivery leg (actors move in)
                             3.2b router shrink to host-to-host + stub
                             3.3 orchestrate -> messenger identity/reachability push
                             3.4 Send/triage wire integration
                             3.5 PtySocket end-to-end proof
        |
Phase 4  Cold delivery       4.1 killed mark + resume identity plumbing
                             4.2 respawn-by-resume legs (pi, claude — posture
                                 primary-vpdx; codex deferred primary-ohrb)
                             4.3 dead-agent bounce (interim, primary-pm92)
                             4.4 harness lifecycle push event stream
                                 (post-messenger-core, primary-s4ep)
        |
Phase 5  Rename sweep        5.1 orchestrate->orchestrator, message->messenger
```

Standing constraint on every store-touching packet: any new or changed sema
family MUST (a) ship its consumer-side migration (no engine evolution primitive
exists yet — recorded debt), and (b) be added to the version-handover Mirror
snapshot (`orchestrate/src/handover.rs`) or it silently drops on handover.
Packet 0.2's check makes (b) mechanical.

## Phase 0 — Foundations

### 0.1 Daemon reply reliability + teardown fix — RESOLVED, LANDED

Diagnosed 2026-07-17 (bead `primary-p4h7`): two stacked defects, neither a
crash. (1) The schema-rust-emitted daemon spine closed the socket with no
reply frame on any engine error — clients read EOF ("failed to fill whole
buffer") and could not distinguish domain error from daemon death. Fixed in
the emitter: every decoded request now answers with a complete frame; engine
failures carry a typed `EngineRefusal` under a reserved header
(schema-rust 0.7.1 backport `bc964c4f` for the deployable line; 0.9.0 on
main). (2) Rejected-worktree teardown deterministically failed on an empty
undescribed working-copy commit (jj push refusal); fixed with the salvage
revset + bookmark cleanup. Both landed on all mains in the 2026-07-17
integration pass; the phase-1 trust gate is OPEN.

### 0.2 Migration safety + Mirror coverage — LANDED (bead `primary-4khu`)

Landed 2026-07-17: automatic pre-migration preserve (typed fail-closed
`Error::PreMigrationPreserve`; preserve taken before the first repair) and the
fixture-gated migration harness (`tests/store_migration_fixtures.rs`, loading
captured real stores from `ORCHESTRATE_MIGRATION_FIXTURE_DIRECTORY`, skipping
cleanly when absent — privacy gate: no real store content in the public repo).
Proven: the captured outage store migrates to the exact promised counts and
its preserve replays to identical counts (rollback property); pre-v5 stores
fail closed typed. Recorded residue: the daemon writes no operator-visible
log line when a preserve is taken (candidate small follow-up).

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

### 0.4 Real repo identity — BUILD NOW (bead `primary-9wxr`)

Sequencing settled by the 2026-07-18 blessing (design §0e): early train
packet, so messenger-era records are born carrying real identity.
`StoredRepository` is name + local path only; the psyche's ruling is repo =
real identity with path incidental, and both the never-fork guard's
repo-level block entries and phase 2b's contention flow need the identity
key.

- Repos: `orchestrate` (+ `signal-orchestrate` if the repo vocabulary is on the
  wire). Store family change: `StoredRepository` gains real identity (remote
  URL/identity); migration + Mirror addition required (0.2 discipline; use the
  landed fixture harness).
- Depends on: 0.2 (landed).
- Verification: migration test from a captured store; identity round-trip.
- Single fresh context: yes.

### 0.5 Sema-engine evolution primitive (bead `primary-rlg7`)

Adopted by the 2026-07-18 blessing: each table family registers how to read
its older shapes; the engine applies the chain at store open — replacing
hand-written raw-catalog migrations (the recorded layering-violation debt).

- Repos: `sema-engine`; consumers `orchestrate` + `message` adopt after.
- Depends on: 0.2's fixture harness (acceptance runs against captured stores).
  Not on the critical path; store-touching packets may land hand-written
  migrations until it exists, then convert.
- Verification: orchestrate's v7→v9 agent-registry migration re-expressed
  through the primitive, green against the captured fixtures; no raw catalog
  edits remain in consumers.
- Single fresh context: yes.

## Phase 1 — Liveness (liveness-first per ruling)

### 1.1 Kernel exit watch + typed death — LANDED

Landed 2026-07-17 (orchestrate 0.8.0, schema v9): `HarnessLivenessWatch`
holds pidfds on every Active agent's pin (start-time-verified against pid
reuse; the wake is never trusted — transitions derive from `/proc`);
exit re-enters the daemon and the agent gets typed
`OrchestratorAgentStatus::Dead`, distinct from idle, with death re-stamping
`last_activity` so terminal retention runs from the observation. End-to-end
witnessed (kill a real process → Active→Dead through the wire `Observe`);
pid-reuse fixture refuses to bind. Dead is the killed-mark source phase 4
consumes. Note for 1.3: the branch already carries safe passthrough arms for
the abandonment train's `LaneStatus::Suspect`, holding Suspect on the
Active-sized reaper window until 1.3 sets the 15-min grace.

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

## Phase 2 — Launch identity (psyche-ruled §7 + §0d Q2: the orchestrator is the mint)

### 2.1 messenger.sema birth: identity + delivery registry — LANDED as built

Landed 2026-07-17 (signal-message 0.5.0, message 0.7.0): `messenger.sema`
born with the `agent-registry` family (agent ID → endpoint, resume identity,
killed mark, pid + start-time pin), spirit's mint algorithm verbatim, wire
ops `AssignAgentIdentity`/`BindAgentEndpoint`/`QueryAgentRegistry`, registry
persistence across reopen proven. **As-built mint semantics are superseded**
by the §0d Q2 ruling — the messenger-side mint relocates in 2.1a; the durable
registry itself stands as the messenger's consumer view of IDs (+ threads in
3.1).

### 2.1a Mint relocation to the orchestrator (bead `primary-sdgy`; implementer dispatched)

- Content: the ORCHESTRATOR becomes the mint — it creates the agent ID
  (spirit mint discipline moves/is invoked orchestrator-side; uniqueness
  domain = the orchestrator's registry) and PUSHES minted identities into the
  messenger's registry (§0e reconciliation: the messenger never polls; it
  reads its own pushed-to registry). The messenger's `AssignAgentIdentity`
  either retires or becomes the push-ingestion arm — implementer contract
  call, recorded in both ARCHITECTUREs.
- Repos: `orchestrate` (+ `signal-orchestrate` if mint is wire-visible),
  `message`, `signal-message` (op reshape).
- Depends on: 2.1 (landed). Bead brief is authoritative.
- Verification: mint happens orchestrator-side before launch; messenger
  registry row appears by push with no messenger-side mint; uniqueness holds
  across both stores' views.
- Single fresh context: yes.

### 2.2 Pre-launch mint + launch through the harness component

- Content: the spawn chain per §0d — the orchestrator allocates the ID
  **before the process starts**, then launches through the harness component
  (the existing orchestrate→harness `meta-signal-harness` authority chain);
  terminal-cell, beneath, writes the ID into the session directory (alongside
  `child.pid`/`data.sock`), injects it into the agent's initial prompt ("you
  are agent <id>"), and records the session's resume identity. Resume
  detection reuses the session's existing ID (mint reuse, not re-mint).
- Repos: `orchestrate` (spawn/mint seam), `harness` (+ `meta-signal-harness`
  if the launch op needs vocabulary), `terminal-cell` (session-dir + prompt
  injection).
- Depends on: 2.1a.
- Verification: orchestrator-initiated launch → agent's initial prompt
  carries the pre-allocated ID; relaunch with resume → same ID; messenger
  registry shows the live pid for the ID via the push.
- Single fresh context: borderline (three repos); split harness-launch from
  terminal-cell-injection if heavy — the decision shape is one packet.

### 2.3 Registration binds the pre-minted ID

- Content: registration BINDS the already-minted ID; it no longer mints
  (amendment 8). Orchestrate's reachability discovery already walks to the
  terminal-cell session directory — it now also reads the launch ID there and
  binds the registration to it. Whether `RegisterAgent` additionally carries
  the ID on the wire is a contract decision for the implementer (the
  discovery-read path needs no request change and keeps the
  no-caller-supplied-reachability rule) — decide inside the packet, record in
  ARCHITECTURE.
- Repos: `orchestrate` (+ `signal-orchestrate` if the wire slot is chosen).
- Depends on: 2.2.
- Verification: register from a terminal-cell session → registry keyed by the
  launch ID; no minted-at-registration path remains.
- Single fresh context: yes.

## Phase 2b — Contention-flow MVP (bead `primary-qz9l`; implementer dispatched)

Psyche-dictated now-scope (design §0d a–e) with the Q1 ruling: MVP merges
clean branches into main automatically — "we'll build review into that later.
first MVP doesnt, just merge in main" (review gate = deferred packet, bead
`primary-njmu`). The bead brief is authoritative for packet scope; the split
below is the expected acceptance-boundary shape:

- **2b.1 Repo-taken automatic answer** — an agent claiming a taken repo's
  main is answered automatically with the typed contention reply instead of a
  bare refusal.
- **2b.2 Feature-named lane → auto-worktree + branch** — lane registration's
  PascalCase feature name becomes the feature branch; orchestrate creates the
  worktree in the known place by default (the existing `RequestWorktree`
  scaffold becomes the contention default rather than an explicit request).
- **2b.3 Release-time branch-started message** — the new message type to the
  agent releasing a repo's main lane: a feature branch was started off this
  repo while you held it. (Delivery leg: parks on phase 3 for real messenger
  delivery; until 3.2a lands, surface it in the release reply.)
- **2b.4 Tracked auto-rebase + MVP auto-merge** — orchestrate tracks what it
  created; first finished work lands on latest main (simple rebase), later
  branches auto-rebase; clean rebase → merge into main, no review gate.
  Conflicted or unfinished branches park for the (deferred) review flow.
- Repos: `orchestrate`, `signal-orchestrate` (contention reply + message
  vocabulary), touches the worktree registry machinery landed with
  `ConcludeWorktree`.
- Depends on: 0.4 (real repo identity — the contention key), 1.1 (landed);
  2b.3's delivery leg on phase 3.
- Verification: two-agent contention fixture — second claimant gets the typed
  answer + auto-worktree; release emits the branch-started notice; a clean
  branch auto-merges to main; a conflicted branch parks.

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

### 3.3 Orchestrate → messenger identity/reachability push

- Content: per push-not-pull, orchestrate is the producer and PUSHES minted
  identities (2.1a), agent registration, and reachability (terminal-cell
  endpoint or remote-host marker) into the messenger's delivery registry via
  a subscription; the messenger never polls — "the messenger can get a list
  of existing agent IDs" is satisfied by reading its own pushed-to registry
  (§0e reconciliation). Replaces the router `RegisterActor` propagation leg
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
  a plainly-launched claude). Claude posture per bead `primary-vpdx`
  (blessing-adopted): launcher-launched claude sessions carry the cooperative
  channel flag for LIVE reach (flag verification is that bead's pre-task);
  plain launches stay cold-respawn-only; the cloud remote-control path is
  off-limits by default. Codex leg deferred-by-lean (bead `primary-ohrb`).
  The spawn effect executes through terminal-cell so the respawned session
  gets a session directory, its existing ID (2.2 resume path), and future
  reachability.
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

### 4.4 Harness lifecycle push event stream (bead `primary-s4ep`; post-messenger-core)

- Content: the harness daemon grows a push lifecycle event stream
  (turn-started/idle/stalled/resumed/exited); the orchestrator subscribes
  once; liveness consumes the events as enrichment alongside pidfd exit-push
  and the §3.3 activity read — "alive but stuck" finally has an event.
  Blessing-adopted with explicit sequencing: after the messenger core
  (phases 2–3), never displacing the critical path.
- Repos: `harness` (+ `signal-harness` vocabulary), `orchestrate`
  (subscription side).
- Depends on: phase 3 core landed; 1.1 (status vocabulary).
- Verification: events arrive pushed with no polling; a stalled-but-alive
  fixture is distinguishable from busy and from dead.
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
[LANDED: 0.1, 0.2, 1.1, 2.1]               (trust gate OPEN)
0.2 -> {0.4, 0.5, 3.1, 4.1}                (store-touching discipline)
0.3 -> first cross-repo train verification
0.4 -> 2b                                  0.5 -> (conversion, off critical path)
1.1 -> 1.2 -> (1.3 wiring)                 1.1 -> 4.1
2.1 -> 2.1a -> 2.2 -> {2.3, 4.2}           2.1 -> {3.1, 3.2a, 3.3}
2b.3 delivery leg -> 3.2a                  3.1 -> 3.2a -> {3.2b, 3.5}
3.3 -> {3.4, 3.5, 4.1}                     3.2a -> 3.4
4.1 -> {4.2, 4.3}                          phase 3 -> 4.4
{all} -> 5.1
```

Dispatchable now, independent: 0.3, 0.4, 0.5, 1.2, 1.3 (after its
coordination check), 2.1a (dispatched), 2b.1/2b.2 (dispatched under
`primary-qz9l`), 3.1. Critical path to a working messenger:
2.1(landed) → 3.1 → 3.2a → 3.4.

## Never-fork guard attachment points (not built here; not precluded)

- Repo-level block entries: a new sema family neighboring the worktree
  registry (`repository|branch`, `owning_lane`, status), trigger point at the
  claim/lane release path (`src/claim.rs` / `src/lane.rs`) — nothing in this
  train occupies or reshapes those seams.
- Requires real repo identity (packet 0.4 / open question 3).
- The liveness machinery (phase 1) is the guard's release valve for
  crashed-agent wedges — this train delivers it.

## Former open questions — all resolved (2026-07-17/18)

All six now carry resolution states; none block dispatch. Lean-adopted items
keep their psyche-review flags (design §0e).

1. Claude subagents: RESOLVED — parent-only working model adopted via general
   blessing (§7b); threads give the group-addressing surface; no
   subagent-suffix vocabulary in contracts pending psyche review.
2. Sema-engine evolution primitive: RESOLVED-TO-BUILD by the 2026-07-18
   blessing → packet 0.5, bead `primary-rlg7`.
3. Real repo identity sequencing: RESOLVED — build now as packet 0.4, bead
   `primary-9wxr`.
4. Harness lifecycle push stream: RESOLVED — build post-messenger-core →
   packet 4.4, bead `primary-s4ep`.
5. Claude live-delivery posture: RESOLVED — launcher + cooperative flag for
   live reach (flag verification is the bead's pre-task), plain launches
   cold-only, cloud remote-control off-limits by default → bead
   `primary-vpdx`.
6. Codex leg: RESOLVED — deferred-by-lean → bead `primary-ohrb`.

## Unknowns for implementers (not psyche-blocking)

- `LaneAbandonmentMachinery` lane status (packet 1.3 checks first).
- Whether the messenger participates in any version-handover snapshot (2.1
  records the answer in ARCHITECTURE).
- Which prior proof "RPC steer verified" used (intercom vs `--mode rpc`) —
  affects nothing in this plan; pi leg specifics settle inside 4.2.
- ~~The 0.1 truncation root cause~~ — resolved and landed (see 0.1; bead
  `primary-p4h7`).
