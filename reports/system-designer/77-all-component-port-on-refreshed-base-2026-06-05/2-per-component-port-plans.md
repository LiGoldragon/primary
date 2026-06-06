# 77.2 — Per-component triad-port plans (all 13 remaining components)

Source-grounded port plan per component, classified against the refreshed recipe
(`77.1`) and its two hard blockers — **B1** (the component's `meta-signal-*` /
`owner-signal-*` contract is a concept-only stub, not a real emitting wire contract) and
**B2** (`sema-engine` has no secondary-index / append-log / predicate-filter /
identified-multi-op-atomic, so a 1:N ledger needs an `ox7e` engine cycle). Full per-agent
detail in workflow transcript `wnrg3eifm` / `wf_b405f67d-ea7`. Already designed in report
75: message, router, orchestrate. Pilot: spirit. Multi-listener worked example: lojix.

## Status table

| Component | Status | Start now? | B1 (meta) | B2 (1:N) | Sockets | Size |
|---|---|---|---|---|---|---|
| cloud | partial-triad | **yes** | cleared | soft (deferred) | 2 (ord+owner) | M — mostly done |
| upgrade | partial-triad | **yes** | cleared | blocker (event-log) | 2 (ord+owner) | L |
| repository-ledger | pre-triad | **yes** | promote stub | soft (composite-key) | 2 (ord+meta) | L |
| domain-criome | pre-triad | **yes** | cleared | soft | 2 (ord+meta) | L |
| introspect | pre-triad | **yes** | shared eng-mgmt | soft (composite-key) | 2 (ord+superv) | L |
| mind | pre-triad | **yes** (Slice-1) | promote stub | blocker (grant ledger) | 2 (ord+owner) | L — biggest |
| terminal | pre-triad | **yes** (Slice-1) | promote BOTH legs | blocker (ledger triple) | 2 signal + 1 raw data | L |
| criome | pre-triad | **yes** (Slice-1) | author from scratch | soft (mostly) | 2 (ord+owner) | L |
| harness | pre-triad | **yes** (Slice-1) | shared eng-mgmt | blocker (transcript) | 2 (ord+superv) | L |
| system | pre-triad | yes (deprioritize) | shared eng-mgmt | none (stateless) | 2 (ord+superv) | M |
| agent | greenfield | partial | **double** stub | blocker (transcript) | 2 (ord+owner) | L |
| terminal-cell | **library, not a triad component** | n/a (not a port) | n/a | none (no Sema) | sockets owned by the library, off the triad shell | n/a |
| persona | special-manager | **no** | absent (author) | blocker (event-log) | multi + FD-handoff | L |

## The plans

### cloud — most advanced; start immediately
Provider API daemon (Cloudflare DNS first). **All three plane schemas authored, both
contracts emit, both engine traits implemented** — `meta-signal-cloud` is a real
`GenerationPlan::wire_contract` (B1 cleared, verified). The only remaining work: wire the
`SchemaRuntime` behind a `MultiListenerDaemon` (copy lojix) over the in-memory state, then
add a `sema-engine` Store. PlanTable is a soft 1:N (deferred). Nexus catalog already in
schema (`SignalArrived`/`SemaReadCompleted`/`SemaWriteCompleted`/`EffectCompleted` +
`CloudflareObserve*` effects). **The fastest visible win — proves engine-track-behind-
MultiListenerDaemon end to end.** Port on a `cloud` `next` worktree.

### upgrade — B1 cleared, schema authored; keyed slice now, ledger waits on B2
Runtime leg of the upgrade triad (migration orchestration + handover driver +
catalogue/policy/active-version state). `meta-signal-upgrade` is a **real emitting
contract** (B1 cleared — this contradicts 75/3's gap-table guess). Unsplit
`component_runtime_compatibility` schema already carries all three planes. Nexus is
already declared as `NexusWork`/`SignalArrived` routing (not inline match), incl.
`CommandEffect(CallHandoverPeer)` for the outbound driver. **Start the keyed
catalogue/policy read slice now**; the active-version event-log + atomic flip-and-record
hits **B2**. Open: `UpgradeFrom`/`AcceptPrevious` (emitted, unimpl) vs `version-projection`
— a psyche call.

### repository-ledger — furthest-along daemon on the oldest stack; keyed, no B2
Records Gitolite pushes into a `sema-engine` DB. **Store already on the modern keyed API**
(5 tables, `register_table`); the 1:N (commits per push) is carried by a **composite key
prefix** (`{seq:020}-{objectid}-{refname}`) — so it **dodges B2 entirely** (the proven
interim workaround). Hits **B1**: `meta-signal-repository-ledger` is an
`owner-signal-*.concept.schema` stub to promote (vocabulary already proven — transcription).
Nexus catalog: `RecordHookNotification`/`RecordPushObservation` (1:N fan-out) /
`ReadEvents`/`ReadRecentRepositories`/`ReadChangedFiles`. Work is the runtime rewrite onto
triad-runtime + transport swap to signal-frame.

### domain-criome — meta contract already real; one self-inflicted nexus gate
Criome-domain registry / resolution / projection (owns domain *meaning*; cloud owns
execution). `meta-signal-domain-criome` is a **real `lib.schema`** (B1 cleared). `sema.schema`
already emits the `SemaEngine` trait. **The one hard blocker is self-inflicted**: the
checked-in `nexus.schema` action vocabulary is incomplete so `NexusEngine`/
`NexusRunnerAdapter` are NOT emitted (runner-shape gate) — the author fixes it by reshaping
the vocabulary to the exhaustive runner shape. Delegations are a soft 1:N. Add
`NotAuthoritative` content-addressed authority per Spirit 312. Two legacy `signal_channel!`
contracts → `wire_contract` emission.

### introspect — read-only inspection; first slice fully clear
Fans out to peer daemons over Signal, persists an observation/delivery-trace audit trail,
projects NOTA at the edge. **Slice-1 (4 read verbs + 2 keyed tables, single ordinary
socket) starts now.** `delivery_trace_events` is a 1:N ledger but **pre-solved porter-side
via composite string key** (soft B2). No `meta-signal-introspect` — its second listener is
the **shared `signal-engine-management`** supervision contract (so its B1 is the shared
owner-contract promotion, not a unique stub). Nexus: `ObserveEngineSnapshot`/
`ObserveComponentSnapshot`/`ReadDeliveryTrace`/`ObservePrototypeWitness`/`RecordObservation`.
Tap/subscribe streaming is the last slice. Clean up free-function rust-discipline misses.

### mind — biggest port; ordinary slice now, owner on B1, grant ledger on B2
Persona's central state daemon (Thought/Relation graph, work/memory, durable
subscriptions) AND the channel-grant **adjudication authority** router obeys.
**Slice-1 (ordinary `signal-mind` plane, single listener + daemon-layer push) starts now**
— `thoughts`/`relations` are keyed tables already on `sema-engine` with the supported
`engine.subscribe` keyed-delta path. **Slice-2** (owner `Configure`/`Inspect`) waits on
**B1** (`owner-signal-mind` has a real hand-derived `signal_channel!` but a `.concept.schema`
build pipeline — promote it). **Slice-3** (durable adjudication-log + channel-grant ledger,
grants-by-channel) waits on **B2**. Must fix: `--socket/--store/--actor` flags violate
single-NOTA-arg; raw `storage_kernel()` access violates no-raw-redb. 11-verb Nexus catalog
incl. `decide AdjudicationRequest → CommandEffect(call orchestrate)`. Owner interaction
with orchestrate is an **outbound client, not a third listener** → two-listener daemon.

### terminal — three contracts (two stub) + a raw data carve-out
Terminal-session owner (named sessions around terminal-cell, control plane, viewer policy,
6 observation tables). **Slice-1 (3 keyed session tables, read/registry) starts now.**
Hits **B1 on BOTH legs** — ordinary `signal-terminal` AND `owner-signal-terminal` are
concept stubs to promote — and **B2** on the `delivery_attempts`/`terminal_events`/
`viewer_attachments` ledger triple. Rich 18-verb Nexus catalog (`Connect`/`DeliverInput`/
`MutateGeometry`/`DetachViewer`/`CaptureTranscript`…). **Carve-out:** the per-session raw-byte
viewer DATA socket must stay hand-written beside the daemon (off the signal-frame
MultiListenerDaemon) — shares terminal-cell's data-plane decision.

### criome — BLS auth daemon; ordinary slice now, owner from scratch
Spartan BLS12-381 auth/attestation (verifies signatures, holds identity/revocation/
attestation state, signs attestations). **Slice-1 (ordinary `signal-criome` request/reply +
daemon-layer subscribe) starts now.** 9 tables exist but on the **OLD `sema` library** →
must migrate onto `sema-engine` (mostly keyed → soft B2). **B1 is author-from-scratch**:
`owner-signal-criome` repo is **absent** — must be authored, plus an encrypted owner session.
Nexus absent today (inline match across `root.rs`) → declare the catalog. Real BLS crypto
is a parallel workstream.

### harness — actor-rich; Kameo-vs-engine-trait reconciliation
Models AI harnesses (Codex/Claude/Pi/Fixture) as addressable runtime objects (identity,
lifecycle FSM, transcript stream, terminal delivery). **Slice-1 (request/reply + stream,
no meta, no sema) starts now.** Second listener reuses the **shared `signal-engine-
management`** supervision contract (already two-listener in behavior via raw threads — the
port consolidates onto MultiListenerDaemon, a simplification). Durable transcript
append-log hits **B2**. **Novel question no prior port faced:** does the Nexus engine drive
the existing Kameo actors via `ask()`, or do actors collapse into the Store? Recommend
actors stay live-state owners driven by `ask()`. Contract authored from a live
`signal_channel!` tree. Nexus: `Decide HarnessRequest`/`Gate MessageDelivery`/`Select
TerminalEndpoint`/`Run TerminalDelivery`/`Project HarnessStatus`.

### system — stateless, paused; deprioritize
OS/window-focus observation boundary (Niri focus events + status). **Stateless** (no sema
plane → no B2). Second listener reuses shared `signal-engine-management` (no own
meta-signal → no unique B1). Contract on the **legacy `signal-core`** substrate — the whole
triad must be authored. **Explicitly paused** (`INTENT.md:11`) and self-superseding —
technically startable but low priority. Small Nexus (`ClassifyRequest`/`DecideObservation`/
`DecideSubscription`/`DecideRetraction`/`DecideStatus`).

### agent — greenfield; double-B1 then scaffold
The backend abstraction (persona-claude/-codex/-gemini/-pi/-open-code as BACKENDS; router
talks to agent not harness — `w4jp`/`gdbf`). **Daemon repo is ABSENT** (verified) — cannot
start the daemon today. First move is **DOUBLE B1**: promote BOTH `signal-agent` AND
`owner-signal-agent` concept stubs, then scaffold the repo. The first `run_effect` driving
**outbound backend sockets** is novel, plus a coordinated **router cutover** (router stops
calling harness directly). Transcript ledger hits **B2**. Tail of the roadmap.

### terminal-cell — NOT a triad component; it is a library (corrected 2026-06-06)
**Reclassified after psyche feedback.** terminal-cell is the low-level PTY/transcript
**library** that `terminal-daemon` consumes in-process — NOT a triad daemon to port. Both
`terminal/INTENT.md` and `terminal-cell/INTENT.md` state production consumes it as a
library inside `terminal-daemon`; the standalone `terminal-cell-daemon` is explicitly a
dev/test harness, "not the Persona runtime boundary." Its deps are
`kameo`/`signal-core`/`signal-terminal` only — no `triad-runtime`/`schema-rust-next`/
`sema-engine`, and no Sema DB (forbidden by INTENT). So it does **not** get a triad port:
no plane schemas, no Nexus/Sema engine, no MultiListenerDaemon shell. Its only
modernization is migrating its control surface to the current `signal-terminal`/
`signal-frame` contract and cleaning up the dev daemon + the 12 `--flags`/1-byte-tag CLI
ergonomics — library work, not a component port. **The "carve-out" is gone from the triad
roadmap:** the per-session raw `data.sock` is bound and pumped by the embedded
terminal-cell library, off the triad shell, and raw bytes never cross terminal's
signal-frame socket — so there is no raw listener to fit into `MultiListenerDaemon`. See
report 78's correction banner.

### persona — the apex supervisor; port LAST
The privileged engine-manager (launches/retires engines, starts/stops/observes the whole
set, owns FD-handoff cutover). Per `tq18`/`mazv`: persona is the manager; orchestrate is
the runtime that runs engines. **Gated on BOTH blockers simultaneously** — `meta-signal-
persona` is **entirely absent** (author from scratch; `owner-signal-persona` is the current
owner lane), and `manager.engine-events` is a 1:N append-log with atomic event-append +
snapshot-reduce (**B2**). Still on the **OLD `sema` crate + raw redb** → migrate. 13-verb
Nexus (`Engine.Launch`/`Engine.Retire`/`Component.Start`/`Component.Stop`/`Engine.Query`…).
FD-handoff (`SCM_RIGHTS`) + systemd glue has **no triad analog** — stays hand-written.
Consumes every component's engine-management contract, so it must land **last**, after
router/orchestrate prove the shared `ox7e` ledger primitive.

## How this extends report 75

Report 75 ported the **delivery spine** (message/router/orchestrate). This sweep shows the
**same recipe carries the whole fleet**, with the work cleanly partitioned by the two
blockers and three special-shape decisions (`3-cross-component-roadmap.md`). The
keyed/stateless components (cloud, upgrade-readpath, repository-ledger, domain-criome,
introspect-slice1) are a safe first wave that needs neither blocker cleared; the 1:N
components share one `ox7e` fix; the manager/greenfield/carve-out trio (persona, agent,
terminal-cell) need psyche decisions before they start.
