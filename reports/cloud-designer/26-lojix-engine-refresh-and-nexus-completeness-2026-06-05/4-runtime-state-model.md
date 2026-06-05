# lojix runtime database-state model — audit + target shape

Lens: the psyche wants us to "properly identify what kind of database runtime
state it needs to have." This file audits the SEMA plane
(`triad-port/schema/sema.schema`) and the in-memory engine impl
(`triad-port/src/schema_runtime.rs` + the `Store` in `triad-port/src/lib.rs`)
against the functionality inventory drawn from legacy Stack A
(`lojix-cli/src/*.rs`), the wire contracts (`signal-lojix` ordinary +
`meta-signal-lojix` meta), and the lojix `ARCHITECTURE.md` §1 owned-surface
list. It produces a target runtime-state model and a gap list.

Anchor intents grounding this audit:

- `z6qu` (VeryHigh) — the nexus schema IS the engine's internal feature
  catalog: every internal feature, every conditional write, every filter is a
  declared Nexus verb+object. A durable-state condition the engine enforces
  (slot transitions, pin-label uniqueness, rollback-ring eviction) is an engine
  feature; if it is not visible in the schema it is hidden inline logic.
- `a2t4` (VeryHigh) — minimal on TWO axes: minimal at the semantic boundary,
  and minimal in type count — input and output types do not needlessly repeat;
  where one type can serve both, reuse it.
- `fosp` / `[6ry9]` / `[0fdy]` — SEMA means database work through sema-engine
  ONLY; the real SEMA plane writes durable state to a `.sema` (redb) file; no
  component daemon makes direct redb calls. The current in-memory `Vec`-backed
  `Store` is explicitly a placeholder for sema-engine-backed tables.
- `[3d5z]` (VeryHigh) — strict triad separation: the SEMA engine owns ALL
  durable-state code. Slot-transition rules and pin bookkeeping are SEMA-plane
  concerns, not Nexus decision logic; today they live in `apply_sema` arms on
  `SchemaRuntime`, which is the SEMA engine impl — correct placement.
- `tvbn` / `fe2j` — port-first to PARITY before cutover; Stack A is the
  functionality reference for "what durable state the inventory requires."

## 1. The four declared tables, and how operations map onto them

`sema.schema` declares four durable table records (the lojix state plane,
`ARCHITECTURE.md:44-65`). The current write/read operation roots map onto them
as follows.

### LiveSetTable

`LiveSetTable { entries (Vec LiveGeneration) }`, where `LiveGeneration` carries
`DeploymentIdentifier GenerationIdentifier ClusterName NodeName DeploymentKind
ActivationKind GenerationSlot ClosurePath`. ARCHITECTURE.md:44 frames this as
`BTreeMap<(ClusterName, NodeName, Kind), Generation>` — "source of truth for
what's running on every node right now."

- Written by: `RecordGenerationActivated` (`record_generation_activated`,
  `schema_runtime.rs:639-683`) — pushes one `LiveGeneration`.
- Read by: `QueryGenerations` (`query_generations`,
  `schema_runtime.rs:822-839`) — linear scan + filter.

Home table for the activation commit: clear. But two structural defects:

1. The table is an append-only `Vec`, not the keyed `BTreeMap` ARCHITECTURE
   names. `record_generation_activated` always PUSHES; it never replaces the
   prior `Current` generation for the same `(cluster, node, kind)` key. After
   two switch-deploys to the same node, `QueryGenerations` returns TWO rows both
   in slot `Current`. There is no "the live generation for this key is now X,
   the old one demotes to a rollback slot" transition. This is the single
   largest correctness gap in the live-set model (detail §4).
2. `DeploymentKind` is part of the live-set identity per ARCHITECTURE
   (`(ClusterName, NodeName, Kind)`), and `LiveGeneration` carries it — but the
   write derives `deployment_kind` from the in-flight `active_deploy` pipeline
   cursor (`schema_runtime.rs:649-652`), defaulting to `FullOs` when the cursor
   is gone. The kind belongs in the `ActivationCommit` so the SEMA write is
   self-contained and does not reach into Nexus pipeline state (a `[3d5z]`
   separation smell — see §3 type list).

### GcRootsTable

`GcRootsTable { roots (Vec GcRoot) }`, `GcRoot { GenerationIdentifier
ClusterName NodeName GenerationSlot ClosurePath label (Optional PinLabel) }`.
ARCHITECTURE.md:47-55 is the richest owned surface: per-`kind` slots `current`,
`boot-pending`, `rollback/<n>` (last N, default 4), `pinned/<label>`,
`recent/<timestamp>` (short-grace builds protecting freshly-built closures from
cache eviction), two-phase deletion respecting narinfo TTL.

- Written by: `RecordGenerationActivated` (pushes a root with `label None`),
  `PinGeneration`, `UnpinGeneration`, `RetireGeneration`.
- Read by: nothing directly — there is no `SemaReadInput` that returns GC-roots
  state. `QueryGenerations` reads `LiveSetTable`, not `GcRootsTable`. So the
  retention tree the daemon's whole reason-for-being is built around is
  WRITE-ONLY from the read surface (gap, §4).

`GcRoot` duplicates almost all of `LiveGeneration` (same cluster/node/slot/
closure/generation), differing only by `DeploymentIdentifier`+kind+activation
present on `LiveGeneration` and `label` present on `GcRoot`. This is the central
type-reuse finding (§3): live-set and gc-roots are two projections of one
generation fact and should share the generation record.

### EventLogTable

`EventLogTable { entries (Vec EventLogEntry) }`, `EventLogEntry {
EventLogPosition record LoggedEvent }`, `LoggedEvent [(Deployment
DeploymentPhaseEvent) (CacheRetention CacheRetentionTransitionEvent) (Container
ContainerLifecycleRecord)]`. ARCHITECTURE.md:57-62 names the typed events
`BuildRealized CachePublished ActivationSucceeded GenerationRetired
ContainerStarted ContainerStopped`.

- Written by: `RecordPhaseTransition` (appends `Deployment` events),
  `RecordContainerTransition` (appends `Container` events).
- Read by: `ReadEventLog` (`read_event_log`, `schema_runtime.rs:874-897`) —
  range scan returning `deployment_events` + `retention_events`.

Three defects:

1. The `CacheRetention` variant of `LoggedEvent` is NEVER WRITTEN. Pin/Unpin/
   Retire mutate `GcRootsTable` but emit no `CacheRetentionTransitionEvent` into
   the log (`pin_generation`/`unpin_generation`/`retire_generation`,
   `schema_runtime.rs:685-775` — none push to `event_log`). So
   `WatchCacheRetention` subscribers and `ReadEventLog`'s `retention_events`
   lane will always be empty. The retention transitions the schema models
   (`CacheRetentionTransition [Pinned Unpinned Promoted Demoted Retired
   Evicted]`) have no producer. By `z6qu` this is a declared engine feature
   (cache-retention observation) with no implementation behind the schema verb.
2. `ReadEventLog` is reachable from SEMA but UNREACHABLE from the wire:
   `decide_ordinary_input` (`schema_runtime.rs:254-267`) routes `Query` and
   `CheckHostKeyMaterial`, but the `ByEventLog` selection variant
   (`Selection [... (ByEventLog EventLogRange)]`) falls into `QueryGenerations`,
   and `decide_read_completion` treats an `EventLogRead` reply as a malformed
   selector (`schema_runtime.rs:329-331`). So the event-log read path is dead
   code from the client's perspective. Either wire `ByEventLog` → `ReadEventLog`
   or drop the dead arm.
3. `EventLogPosition` is computed as `event_log.0.len()` BEFORE the push
   (`next_event_log_position`, `lib.rs:149-151`), but `record_phase_transition`
   calls `next_event_log_position` AFTER possibly other concurrent appends only
   under one lock, so positions are dense 0..N — acceptable in-memory, but redb
   will need a monotonic counter table, not a `len()` (deferred, §5).

### ContainerLifecycleTable

`ContainerLifecycleTable { records (Vec ContainerLifecycleRecord) }`,
`ContainerLifecycleRecord { ClusterName NodeName container ContainerName state
ContainerState EventLogPosition }`. ARCHITECTURE.md:63-65 — systemd dbus
subscriptions mirror into the event log.

- Written by: `RecordContainerTransition` (`schema_runtime.rs:777-804`) — pushes
  the record AND a mirrored `LoggedEvent::Container` into the event log.
- Read by: nothing. There is no `SemaReadInput` that reads container state, and
  `read_event_log` explicitly SKIPS `Container` events
  (`schema_runtime.rs:889`). So `ContainerLifecycleTable` is, like GcRoots,
  write-only from the read surface.

There is also no wire INPUT that produces a `RecordContainerTransition`: it is
not in `SemaWriteInput`'s caller set from `decide_*` — it would be driven by the
systemd-dbus observer, which is unbuilt (`ARCHITECTURE.md:63` "container
lifecycle observation" — no effect command, no signal verb). So the whole
container plane is modeled but has no producer AND no consumer wired today.
Carry it, but mark it not-yet-load-bearing.

## 2. Audit answer (1): does every operation have a home table, and every
table the writes/reads it needs?

Operation→table coverage matrix (W = writes, R = reads):

| Operation (SemaWriteInput / SemaReadInput) | LiveSet | GcRoots | EventLog | Container |
|---|---|---|---|---|
| RecordDeploySubmitted | — | — | — | — |
| RecordPhaseTransition | — | — | W | — |
| RecordGenerationActivated | W | W | — | — |
| PinGeneration | — | W | (should W) | — |
| UnpinGeneration | — | W | (should W) | — |
| RetireGeneration | — | W | (should W) | — |
| RecordContainerTransition | — | — | W | W |
| QueryGenerations | R | — | — | — |
| ReadEventLog | — | — | R | (skips) |
| CheckKeyMaterial | — | — | — | — |

Findings from the matrix:

- `RecordDeploySubmitted` touches NO table. It only mints identifiers and stows
  the deploy in the Nexus `active_deploy` cursor (`schema_runtime.rs:590-616`).
  That means a submitted-but-not-yet-activated deploy has ZERO durable
  representation: if the daemon restarts mid-pipeline, the deploy is lost with
  no record it was ever accepted. This is the missing-table finding §2b below —
  there is no deploy/pipeline table.
- `Pin/Unpin/Retire` write GcRoots but write no event-log entry — the
  cache-retention event producer gap from §1.
- `CheckKeyMaterial` touches no table and is a hardcoded empty-mismatch stub
  (`check_key_material`, `schema_runtime.rs:899-906` returns `mismatches:
  Vec::new()`). There is no key-material table; the check is meant to compare
  expected (proposal/horizon) vs actual (clavifaber/host) public material
  (`KeyMaterialMismatch` with `SecureShellPublicKey YggdrasilPublicKey
  YggdrasilAddress`). Whether key material is DURABLE STATE or a live effect
  (ssh to host + read horizon) is the open question §2c.

## 2b. Durable state the inventory requires that has NO table

The audit's core finding. Five categories of required durable state with no
home table today:

1. **Deploy proposals / in-flight pipeline state (highest priority).** Stack A
   ran deploy as one synchronous async fn (`deploy.rs:89-148`); the new model
   runs it as a chain of effect continuations across `decide` hops with the
   pipeline cursor held in `active_deploy: Option<DeployPipeline>` — IN MEMORY
   on `SchemaRuntime` (`schema_runtime.rs:27`, `lib.rs` not involved). On daemon
   restart, every in-flight deploy evaporates with no durable trace. A
   `DeployPipelineTable` is needed: one row per accepted-but-not-finished
   deploy, keyed by `DeploymentIdentifier`, carrying the resolved
   cluster/node/kind/flake/source/builder/substituters + the current
   `DeployStage` + resolved `closure_path` once known + `accepted_marker`. This
   makes `RecordDeploySubmitted` actually write a table, makes
   `advance_after_phase` read the durable stage instead of the in-memory cursor,
   and lets a restarted daemon resume or fail-and-clean in-flight deploys. By
   `z6qu` the deploy stages are already a declared feature (the `EffectStage` /
   `DeployStage` ladder); the durable cursor is the SEMA-plane mirror of that
   ladder.

2. **The rollback ring / generation-slot history.** ARCHITECTURE.md:51 names
   `rollback/<n>` (last N rolled-back generations, default 4). There is no
   table, no counter, and no eviction logic: `GenerationSlot::Rollback` is a
   declared enum variant (`signal-lojix lib.schema:57`) that is NEVER PRODUCED
   anywhere in the runtime (confirmed: grep finds zero `GenerationSlot::Rollback`
   constructions). When a new generation activates, the prior `Current` should
   demote to `Rollback`, the ring should evict the oldest beyond N, and evicted
   roots become GC-eligible. None of that exists. The `GcRootsTable` row's
   `GenerationSlot` field is the natural home, but the ring DEPTH (N=4) and the
   demotion/eviction transition are unmodeled. This is a real engine feature
   (`z6qu`) — "demote current to rollback, evict ring tail" — that must become a
   declared Nexus verb + SEMA write, not inline.

3. **Pin labels.** Partially present: `GcRoot.label (Optional PinLabel)` is the
   storage, and `pin_generation` enforces label uniqueness by scanning all roots
   (`schema_runtime.rs:689-696`). So pin labels HAVE a home (the GcRoots table)
   — this is adequate as data. The gap is only the missing retention-event
   emission (§1) and the O(roots) uniqueness scan that a real index would make
   O(1). Not a missing table; a missing index + missing event. Acceptable for
   parity.

4. **Recent / narinfo-TTL grace.** ARCHITECTURE.md:54-55 — `recent/<timestamp>`
   short-grace builds protecting freshly-built closures from cache eviction, and
   two-phase deletion respecting narinfo TTL. `GenerationSlot::Recent` exists and
   IS produced (Test activations + unpin demotion → `Recent`,
   `schema_runtime.rs:731,994`), but there is NO timestamp stored (the slot is a
   bare enum with no `<timestamp>`), so the "short grace" window cannot be
   computed — the daemon cannot tell a 5-minute-old recent build from a 5-day-old
   one. A `recorded_at` / TTL field is needed on the gc-root (or a dedicated
   grace column) for the two-phase-deletion + TTL logic to exist. Today this is
   purely a slot label with no temporal data. Gap.

5. **Key-material check results (open — may not be a table).** §2c.

## 2c. Open question — is key material durable state or a live effect?

`CheckHostKeyMaterial` → `CheckKeyMaterial` → empty stub. The check compares
expected public material (from the proposal source / horizon) against actual
(from the host via clavifaber). ARCHITECTURE.md:90-94 says per-host key material
is clavifaber's (not lojix's) and the cluster trust runtime is a separate,
today-missing component. So key material is NOT lojix durable state — the check
is a LIVE EFFECT (read horizon + ssh/clavifaber the host, diff). That means:

- `CheckKeyMaterial` should NOT be a `SemaReadInput` at all (it touches no
  table); it should be a Nexus `EffectCommand` (a read-only effect like a
  one-shot `nix`/`ssh` probe) whose `EffectResult` carries the mismatches, then
  Nexus replies `KeyMaterialChecked`. Routing it through SEMA is a category
  error: SEMA is durable state (`[6ry9]`), key-material diffing is host IO.

Recommendation: move `CheckKeyMaterial` off the SEMA read root and onto a new
`EffectCommand::CheckKeyMaterial` in the nexus catalog. Flag to the synthesis
agent — this is a SEMA-vs-Nexus boundary correction, not just a stub-to-fill.

## 3. Audit answer (3): type-reuse minimalism (a2t4) — redundant type pairs

`a2t4`'s second axis: types do not needlessly repeat across input/output; reuse
one where it can serve both. Concrete redundant pairs found:

1. **`LiveGeneration` vs `GcRoot` vs wire `Generation`.** Three near-identical
   records describing one generation:
   - wire `Generation` (signal-lojix lib.schema:60-69): id, deployment-id,
     cluster, node, kind, activation, slot, closure.
   - `LiveGeneration` (sema): identical eight fields.
   - `GcRoot` (sema): cluster, node, slot, closure, generation-id, + `label`,
     − deployment-id/kind/activation.
   These are one durable generation fact with two slot/label projections.
   Target: ONE durable `Generation` record (reuse the wire `Generation` shape
   plus an `Optional PinLabel`), and let the live-set and gc-roots tables both
   be views/queries over it rather than two physical copies with duplicated
   fields. `project_generation` (`schema_runtime.rs:861-872`) already proves the
   live→wire projection is a field-for-field copy — a textbook `impl From` /
   shared type, not two parallel structs.

2. **`ActivationCommit` vs `LiveGeneration`.** `ActivationCommit` (the SEMA
   write input for `RecordGenerationActivated`) carries generation/cluster/node/
   slot/closure, then the apply REACHES INTO the Nexus pipeline for kind +
   deployment-id + activation (`schema_runtime.rs:646-656`). The input is a
   strict subset of `LiveGeneration` minus exactly the three fields it then
   smuggles from pipeline state. Target: make `ActivationCommit` carry the FULL
   generation fact (add deployment-id, kind, activation) so the SEMA write is
   self-contained (`[3d5z]` — SEMA must not depend on Nexus cursor state), at
   which point `ActivationCommit` and the durable `Generation` record converge
   to one type.

3. **`StateMarker` (sema) vs `DatabaseMarker` (wire).** `StateMarker {
   CommitSequence StateDigest }` and `DatabaseMarker { CommitSequence
   StateDigest }` are byte-identical (sema.schema:67-69 vs signal-lojix
   lib.schema:58). The runtime constantly converts between them
   (`marker` vs `sema_marker`, `schema_runtime.rs:231-243`, and the
   `Self::marker(report.marker.commit_sequence)` re-wraps at
   `schema_runtime.rs:334,449`). Per `a2t4` these should be ONE type:
   `DatabaseMarker` is the wire-facing name and the SEMA plane can import it
   (the sema.schema already imports many `signal-lojix:lib:*` types — adding
   `DatabaseMarker` and dropping the local `StateMarker`/`CommitSequence`/
   `StateDigest` declarations removes a triple-redundant pair plus two convert
   methods).

4. **`RejectionReason` (sema) vs the three wire rejection enums.** Sema's
   `RejectionReason` (sema.schema:66) is a 10-variant superset that
   `deploy_reason` (`schema_runtime.rs:453-462`) lossily collapses into
   `meta::DeployRejectionReason`, and `query_rejection` separately maps to
   `QueryRejectionReason`. There is real impedance: the SEMA reason set and the
   wire reason sets overlap heavily (`GenerationUnknown NodeUnknown
   ClusterUnknown` appear in both). This one is harder to fully unify because the
   wire enums are authored per-operation (deploy vs query vs pin), but the SEMA
   superset duplicates names that already exist on the wire. Worth a follow-on:
   either the SEMA plane imports the wire reason enums, or the wire enums are
   derived from one shared reason vocabulary. Lower priority than 1-3.

5. **`PhaseReceipt` vs `ContainerReceipt`.** Both are `{ EventLogPosition
   StateMarker }` — byte-identical (sema.schema:61,63). One `EventLogReceipt {
   EventLogPosition StateMarker }` serves both write replies. Trivial merge.

Net: items 1, 2, 3, 5 are clear `a2t4` violations with a one-type target each;
item 4 is a flagged follow-on.

## 4. Audit answer (4): the StateMarker / CommitSequence / StateDigest
optimistic-concurrency model — is it coherent?

Partially. The model's INTENT (per `hzrq`, `qvod`, `z821` — replies carry a
durable state counter/hash so clients know what state their reply reflects) is
sound and the marker is threaded onto every reply. But the current realization
is degenerate:

- `state_digest` is just set equal to `commit_sequence` everywhere (`marker` and
  `sema_marker`, `schema_runtime.rs:231-243`; `lib.rs:133` comment
  "state digest is modeled as the commit sequence"). So the digest carries ZERO
  independent information — it is a second copy of the sequence. A real digest
  must be a content hash (or Merkle root) of table state so two daemons / a
  daemon-and-its-snapshot can detect divergence the sequence alone cannot
  (e.g. same sequence count reached via different write orders). Until the
  digest is a real hash, optimistic concurrency reduces to "compare sequence
  numbers," which is fine for single-writer single-instance (which lojix is —
  `ARCHITECTURE.md:166` one instance per operator) but means the `StateDigest`
  type is dead weight (and per §3.3 it should not exist as a separate field
  until it carries real content).

- No write operation TAKES an expected marker as a precondition. True optimistic
  concurrency is "write IFF current marker == expected marker, else reject with
  `EventLogPositionOutOfRange`/conflict." The rejection enum even has
  `EventLogPositionOutOfRange`, but no write checks an inbound marker — every
  write unconditionally bumps the sequence. So the model is currently
  WRITE-WINS, not optimistic-concurrency. For a single-writer daemon this is
  acceptable for parity, but the schema SHOULDN'T advertise a concurrency model
  it doesn't enforce. Decision needed: either (a) keep single-writer and DROP
  the digest (sequence-only marker), or (b) commit to real optimistic
  concurrency (digest = content hash + writes carry an expected marker). Given
  `ARCHITECTURE.md:166` (single instance) and `opvx` (concurrency is a
  deployment choice, the contract shouldn't encode how parallel a daemon runs),
  recommendation is (a) for parity now, with (b) as the noted follow-on when
  multi-writer becomes real.

## 5. Audit answer (5): deferred-work list — what real sema-engine persistence
needs

The current `Store` (`lib.rs:104-182`) is `Mutex<StoreState>` over four
`Vec`-backed tables plus four `u64` counters — entirely in-memory; `daemon.rs`
constructs `SchemaRuntime::new()` with a fresh empty `Store` on every start
(confirmed: no redb/Engine/register_table anywhere in `daemon.rs`). The
generated `*Table` types in `src/schema/sema.rs` carry only NOTA codec
impls (`from_nota_block`/`to_nota`), no redb mapping. Real sema-engine
persistence (per `fosp` — through sema-engine, never raw redb; `[0fdy]` — `.sema`
file extension) needs, as a deferred-work list:

1. **Open the engine handle.** `ARCHITECTURE.md:147` —
   `Engine::open(EngineOpen::new(path, SchemaVersion))` at daemon startup, path
   = the daemon's `.sema` file (per `[0fdy]`, not `.redb`). The
   `DaemonConfiguration` (`lib.rs:91-97`) currently has no state-file path field
   — ADD one (`state_file_path: String`).

2. **Register each table family.** `ARCHITECTURE.md:124-128,147` —
   `Engine::register_table` for live-set, gc-roots, event-log, container — plus
   the new deploy-pipeline table (§2b.1). Each registration needs the table's
   key type and value type; today the tables are keyless `Vec`s. Define the keys:
   live-set keyed by `(ClusterName, NodeName, DeploymentKind)` (the
   ARCHITECTURE `BTreeMap` key); gc-roots keyed by `GenerationIdentifier` (with a
   secondary index on `PinLabel` for the uniqueness check, §2b.3); event-log
   keyed by `EventLogPosition` (monotonic); container keyed by `(ClusterName,
   NodeName, ContainerName)`; deploy-pipeline keyed by `DeploymentIdentifier`.

3. **Replace the four `Vec` scans with engine queries.** `query_generations`
   (linear filter), `pin/unpin/retire` (linear `find`), `read_event_log` (range
   filter) all become sema-engine `match`/range operations against the keyed
   tables. The `BTreeMap` key on live-set turns the duplicate-`Current`-rows bug
   (§1) into a key-overwrite (correct demotion) for free.

4. **Move the counters into the engine.** `commit_sequence`,
   `deployment_sequence`, `generation_sequence`, `event_log_position`,
   `subscription_sequence` are currently in-process `u64`s reset on restart. They
   must persist (a sequence/metadata table) so identifiers don't collide after a
   restart and the marker is meaningful across restarts. `event_log_position`
   especially must be a stored monotonic counter, not `Vec::len()` (§1.3).

5. **Atomic multi-table commit.** `record_generation_activated` writes BOTH
   live-set AND gc-roots under one `Store` lock today (`schema_runtime.rs:657-674`);
   sema-engine must apply both in ONE commit transaction so the two tables never
   diverge (`ARCHITECTURE.md:152` "tables registered... one redb file owned by
   the daemon"). The `[3d5z]` SEMA-owns-all-durable-state rule means the
   transaction boundary lives in the SEMA engine, not Nexus.

6. **Subscription delivery downstream of commit.** `ARCHITECTURE.md:60-62,153` —
   the subscription bridge (`SubscriptionSink`) delivers deltas AFTER the commit;
   delta delivery cannot roll back the write. The current `open_subscription`
   just mints a token (`schema_runtime.rs:269-284`); the real bridge is unbuilt
   and depends on the schema-next event-frame-emission follow-on (carried in
   report 25 §6 GAP). Deferred, tracked there.

## 6. Target runtime-state model — tables + key columns

The clean target. Five tables (four existing + deploy-pipeline), each keyed,
with the redundant types collapsed per §3.

### Generation (one durable record, replaces LiveGeneration + GcRoot duplication)

One record per generation fact; the live-set and gc-roots become two KEYED
VIEWS over it rather than two physical tables with copied fields. Reuse the wire
`Generation` shape plus retention fields:

- key columns: `GenerationIdentifier` (primary), `(ClusterName, NodeName,
  DeploymentKind)` (live-set index — at most one row per key in slot `Current`),
  `PinLabel` (unique secondary index, when present).
- value columns: `DeploymentIdentifier`, `ClusterName`, `NodeName`,
  `DeploymentKind`, `ActivationKind`, `GenerationSlot`, `ClosurePath`,
  `label (Optional PinLabel)`, `recorded_at` (for the Recent/TTL grace, §2b.4),
  `rollback_ordinal (Optional Integer)` (position in the rollback ring, §2b.2).
- the live-set view = rows where slot ∈ {Current, BootPending}; the gc-roots
  view = all rows (every retained generation is a gc root). This kills the
  LiveGeneration/GcRoot duplication (`a2t4` §3.1) and the slot-overwrite gives
  correct demotion (§1).

### DeployPipelineTable (NEW — §2b.1)

One row per accepted-not-finished deploy.

- key column: `DeploymentIdentifier`.
- value columns: `GenerationIdentifier`, `ClusterName`, `NodeName`,
  `DeploymentKind`, `ActivationKind`, `ProposalSource`, `FlakeReference`,
  `builder (Optional NodeName)`, `substituters (Vec ExtraSubstituter)`,
  `closure_path (Optional ClosurePath)`, `stage DeployStage`,
  `accepted_marker DatabaseMarker`.
- this is the durable mirror of the in-memory `DeployPipeline` cursor; written
  by `RecordDeploySubmitted`, advanced by each `RecordPhaseTransition`, deleted
  by the final activation-record write or a failure.

### EventLogTable (kept, monotonic-keyed)

- key column: `EventLogPosition` (stored monotonic counter, not `len()`).
- value column: `LoggedEvent [(Deployment ...) (CacheRetention ...) (Container
  ...)]` — and the `CacheRetention` arm MUST get a producer (pin/unpin/retire
  emit it, §1).

### ContainerLifecycleTable (kept, keyed; carry as not-yet-load-bearing)

- key column: `(ClusterName, NodeName, ContainerName)` (current state per
  container).
- value columns: `state ContainerState`, `EventLogPosition` (last transition).
- needs both a producer (systemd-dbus observer effect, unbuilt) and a consumer
  (a `SemaReadInput` for container state, or surface via `ReadEventLog` instead
  of skipping `Container` events).

### Sequence/metadata table (NEW, implicit — §5.4)

- the five persisted counters + the current `DatabaseMarker`.

### Shared types after collapse (§3)

- `DatabaseMarker` is the ONE marker type (drop sema `StateMarker`/`CommitSequence`/
  `StateDigest`); `StateDigest` dropped entirely until it carries a real content
  hash (§4).
- one `EventLogReceipt { EventLogPosition DatabaseMarker }` (merge
  `PhaseReceipt` + `ContainerReceipt`).
- `ActivationCommit` carries the full generation fact and converges with the
  durable `Generation` record.

## 7. Gap list against the current schema (priority-ordered)

Priority for PARITY-then-cutover (`tvbn`/`fe2j`). C = correctness, F = feature,
T = type-minimalism, P = persistence.

1. (C, high) **Live-set is append-only, never demotes.** `RecordGenerationActivated`
   pushes; two switch-deploys to one node = two `Current` rows. Needs keyed
   overwrite + demote-prior-to-Rollback. `schema_runtime.rs:657`.
2. (C/F, high) **Rollback ring entirely absent.** `GenerationSlot::Rollback`
   never produced; no N=4 ring, no eviction. A real engine feature (`z6qu`) with
   no implementation.
3. (C, high) **In-flight deploy is non-durable.** `active_deploy` cursor is
   in-memory only; restart loses accepted deploys. Needs `DeployPipelineTable`.
   `schema_runtime.rs:27,590-616`.
4. (F, high) **Cache-retention events have no producer.** `LoggedEvent::CacheRetention`
   never written; pin/unpin/retire emit no event. `WatchCacheRetention` /
   `retention_events` always empty. `schema_runtime.rs:685-775`.
5. (C, med) **`ReadEventLog` unreachable from the wire.** `ByEventLog` routes to
   `QueryGenerations`; `EventLogRead` reply treated as malformed.
   `schema_runtime.rs:329-331`. Either wire it or drop the dead arm.
6. (Boundary, med) **`CheckKeyMaterial` is on the wrong plane.** It is host IO
   (a Nexus effect), not SEMA durable state; today it's a SEMA read returning an
   empty stub. Move to `EffectCommand::CheckKeyMaterial`. §2c.
7. (T, med) **LiveGeneration/GcRoot/Generation triplication** — collapse to one
   durable `Generation` record with slot/label projections. §3.1.
8. (T, med) **`ActivationCommit` reaches into Nexus cursor for kind/deployment-id/
   activation** — carry the full fact; converge with `Generation`. §3.2, `[3d5z]`.
9. (T, low) **`StateMarker` == `DatabaseMarker`; `PhaseReceipt` == `ContainerReceipt`** —
   merge each pair; import `DatabaseMarker` into the SEMA plane. §3.3, §3.5.
10. (F, low) **Recent slot has no timestamp** — `GenerationSlot::Recent` carries
    no `recorded_at`, so the short-grace / narinfo-TTL window
    (`ARCHITECTURE.md:54-55`) is uncomputable. §2b.4.
11. (Coherence, low) **StateDigest is a fake** (= commit_sequence); no write
    takes an expected marker, so the advertised optimistic-concurrency model is
    actually write-wins. Decide: drop digest (single-writer parity) or build
    real content-hash + precondition checks. §4.
12. (P, deferred) **Whole `Store` is in-memory** — the §5 deferred-work list
    (engine open, table registration with keys, query replacement, persisted
    counters, atomic multi-table commit, post-commit subscription bridge).
    Tracked as the noted follow-on; not a parity blocker for an in-memory GREEN
    build but IS a blocker for real cutover (a deploy daemon that forgets every
    generation on restart cannot run production).

## 8. Container plane and key-material — carry notes

- **ContainerLifecycleTable**: modeled, has a write path
  (`RecordContainerTransition`) but NO wire producer (systemd-dbus observer
  unbuilt) and NO read consumer (`read_event_log` skips `Container`). Carry as
  not-yet-load-bearing; do not delete (it is real owned surface,
  `ARCHITECTURE.md:63-65`), but mark it explicitly unwired so it is not mistaken
  for complete.
- **Key material**: per §2c, NOT lojix durable state (clavifaber owns per-host
  material, `ARCHITECTURE.md:90-94`); the check is a live effect. No table; move
  the verb to Nexus.
