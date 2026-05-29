# Wave B — lojix signal + sema reconciliation (production-track vs schema-deep pilot)

*Research-only audit (system-designer lane, inherited per record 920). Reconciles the PRODUCTION-track lean lojix (`horizon-leaner-shape`, the branch `/34` audited) against the schema-deep pilot tracks (`/35` + `/165` on `schema-deep`, `/37` on `schema-deep-iteration-2`), and quantifies the gap to a real production lojix-on-schema-next. Grounded in `/34/5`, `/37/3`, `/38`. No Spirit captured (record 1024 is the directive).*

## Bottom line

**Verdict: POSSIBLE — largely pilot-proven (6.7/8.0), with a quantified remaining gap concentrated in 4 production-only concerns.** The lojix signal layer and sema layer are both demonstrated schema-driven at pilot scale: the wire `Input`/`Output` enums emit from `schema/lojix.schema`, the SEMA plane is sema-engine-backed durable with schema-emitted `EngineRecord`, and the Nexus mail keeper threads `DatabaseMarker` on every reply. The production-track lean lojix is hand-authored Rust on the same substrates (sema-engine + nota-codec + signal-frame) but with hand-written types and a hand-written `signal_channel!` wire contract. The port is a re-grounding, not a re-architecture. The gap is **not** "can the layers be schema-driven" (proven yes) — it's the four production-realities the pilot stubs: real criome auth, real nspawn activation, the owner-signal triad leg, and the richer production wire surface (Pin/Unpin/Retire + cache-retention + multi-phase observations).

## Q1 — Production-track lean lojix shape TODAY

The lean lojix at `~/wt/github.com/LiGoldragon/lojix/horizon-leaner-shape/` is **entirely hand-authored Rust on the legacy substrate stack**. Per `src/lib.rs:14-30`:

- **Datatypes**: hand-authored. The daemon's domain types (`RuntimeConfiguration`, `DeploymentLedger` records) are hand-written Rust; the wire types come from `signal-lojix` (also hand-authored, Q3). `Cargo.toml:42,45` pulls `nota-codec` (legacy) for the CLI's text boundary, NOT `nota-next`.
- **Signal/wire**: legacy `signal-core` frames (`Cargo.toml:25`) carrying `signal-lojix` records (`Cargo.toml:29`, branch `horizon-leaner-shape`). `src/lib.rs:42` re-exports `signal_lojix as wire`.
- **Storage/sema**: `sema-engine` + `sema` (`Cargo.toml:37-38`) — one redb file owned by the daemon. `src/deploy.rs:46-77` opens an `Engine` and registers four **hand-authored** record families (`DeploymentIdentityRecord`, `DeploymentEventRecord`, `DeploymentObservationSubscriptionRecord`, `GenerationRecord` — `deploy.rs:40-44,48-51`). So production ALREADY uses sema-engine for durable state; it just registers hand-written records, not schema-emitted ones.
- **Projection**: `horizon-lib` (`Cargo.toml:41`, the horizon-rs `horizon-leaner-shape` branch) plus `horizon-nota-codec` (`deploy.rs:17`) — the daemon decodes a horizon proposal and projects per-node config before build (`deploy.rs:10-16` imports `ClusterProposal`, `Horizon`, `HorizonProposal`, `Viewpoint`, `Node`, `System`). Wave A covers the projection layer.

**Critical: the crate does not compile as-pinned (confirms `/34`'s B-0).** The lean lib still references `wire::Request`, `wire::Reply`, `wire::DeploymentSubmission`, `wire::LojixFrame`/`LojixFrameBody`, `wire::ReplyRendering` (`runtime.rs:202,206,214,232,243`; `client.rs:24-89`; `authorization.rs:22,67,122,138`). But the pinned signal-lojix tip `a007e8b6` ("migrate NOTA sum records to bracket strings") renamed these to `LojixOperation`/`LojixReply`/`LojixEvent` via `signal_channel!` and renamed `DeploymentSubmission`→`DeploymentRequest`, replacing the `signal-core` frame with `signal-frame StreamingFrame`. Ten `DeploymentSubmission` references remain in `src/`. **This is `/34/5`'s rank-0 B-0 lock break, still open** — a mechanical rename across ~8 files, independent of the schema-next port but blocking any production-track compile.

- **Criome auth**: `src/authorization.rs:43-49` — production policy is `CriomeAuthorizationPolicy::unavailable_until_criome_socket_lands()` (every production deploy denied); tests use `grant_for_tests()` (`authorization.rs:39-41`). The real authorization shape exists (`authorization.rs:113-152`: canonical digest via `submission.canonical_digest()`, `ObjectDigest`, `AuthorizationScope` from `signal_criome`) — it's wired to the contract but fail-closed pending the criome client.

## Q2 — Schema-deep pilots: what's pilot-proven schema-driven (6.7/8.0)

Per `/37/3`'s orchestrator-audited 8-component fullness table (re-scored independently of the subagent's claim), the pilot at `schema-deep-iteration-2` proves **6.7/8.0 (≈84%)** schema-driven. Per-component, with this audit's confirming evidence:

| # | Component | `/37` score | Pilot-proven? | This audit's evidence |
|---|---|---|---|---|
| 1 | NOTA structure | 0.7 | partial | `nota-next` consumed transitively (`Cargo.toml` dep); `StructureHeader` not yet load-bearing |
| 2 | Schema macro lowering | 0.9 | YES | `build.rs:11-27` lowers `schema/lojix.schema` via `schema_next::SchemaEngine`, asserts registry-macro coverage (`SchemaStructDefinition`/`SchemaEnumDefinition`) or panics |
| 3 | Assembled schema | 0.8 | YES | Asschema consumed through the lowering→emission pipeline (`build.rs:13-28`) |
| 4 | Rust emission | 1.0 | YES | `schema_rust_next::RustEmitter::default().emit_file(&asschema)` (`build.rs:28`) emits the full type set to `OUT_DIR/lojix_next_generated.rs` |
| 5 | Generated signal | 0.7 | YES (partial) | `Input`/`Output` enums emit from schema (`schema/lojix.schema:2-14`); methods on schema-emitted nouns (`codec.rs:57-178`); `DatabaseMarker` stamped on every Output variant (`codec.rs:155-168`) |
| 6 | Nexus mail keeper | 0.85 | YES | `NexusMailKeeper` actor (`nexus.rs:167-200`); typed `MailEntry` with `MailLifecycle::{Sent,Queued,Processing,Replied,Failed}` (`nexus.rs:67-104`, schema `lojix.schema:58`); push hooks fire (`nexus.rs:141-156`) |
| 7 | SEMA state handling | 0.85 | YES | sema-engine `Engine` + per-family `TableReference` (`store.rs:128-138`); schema-emitted records impl `EngineRecord` directly (`store.rs:81-122`); `DatabaseMarker` from `current_commit_sequence` + `latest_snapshot` (`store.rs:272-287`); durable counters via `CounterRow` (`store.rs:346-368`) |
| 8 | Spirit runtime | 0.9 | YES | single-NOTA-arg daemon binary + thin CLI unchanged |

**The signal layer (5) and sema layer (6+7) — Wave B's mandate — are the load-bearing lifts:** `/37` moved component 5 from 0.3→0.7, component 6 from 0.2→0.85, component 7 from 0.3→0.85. The schema (`schema/lojix.schema`, 91 lines) is the single source of truth: it declares the wire surface (`Input`/`Output` roots, lines 2-14), the SEMA command/response surface (`SemaCommand`/`SemaResponse`, lines 59-72), the durable records (`PlanRecord`/`BuildRecord`/`CopyRecord`/`ActivationRecord`/`ObservationRecord`/`GenerationRecord`, lines 47-52), and the marker (`DatabaseMarker`, line 36). All Rust for these emits via `build.rs`; agents write only methods on the emitted nouns (`codec.rs`, `store.rs`).

`/35` baseline (5.0/8.0) + `/165` width (source-staging plane, +0.1→5.1) + `/37` depth (6.7/8.0) are three iterations on a common parent (`rnwxqrlzmrmm`); `/37/3` Decision C flags branch convergence (`schema-deep` carrying `/165` + `schema-deep-iteration-2` carrying `/37`) as operator-amalgamation work.

## Q3 — The signal-lojix wire contract: hand-authored vs schema-derivable

**The production signal-lojix wire contract is hand-authored Rust — ~680 lines on branch `horizon-leaner-shape`** (the `/git` checkout is a docs-only skeleton; the crate source lives on the branch, tip `a007e8b6`). Its shape:

- **Validated newtypes via `macro_rules!`** (hand-written): `validated_identifier!` (lib.rs:30-101), `validated_single_line_text!` (lib.rs:103-167), `validated_store_path!` (lib.rs:169-243). These declare `ClusterName`, `NodeName`, `DeploymentId`, `GenerationId`, `StorePath`, `DerivationPath`, etc. (lib.rs:245-269) with `NotaTryTransparent` + rkyv derives.
- **Records via `#[derive(NotaRecord)]`/`#[derive(NotaEnum)]`** (hand-written): `DeploymentRequest` (lib.rs ~415, nested: `DeploymentPlan` enum-with-data + `BuilderSelection` enum-with-data + `Vec<NodeName>`), `Generation`, `DeploymentPhase` (7-variant enum-with-data: `DeploymentSubmitted`…`DeploymentFailed`), `DeploymentObservation`, the `CacheRetention*` family, `GenerationQuery`/`GenerationListing`.
- **Channel via `signal_channel!`** (hand-written, lib.rs tail): `channel Lojix` with 9 operations (`Deploy`, `Pin`, `Unpin`, `Retire`, `Query`, `WatchDeployments`, `UnwatchDeployments`, `WatchCacheRetention`, `UnwatchCacheRetention`), `reply LojixReply` (9 variants), `event LojixEvent` (2 variants), and 2 streams with `opens`/`belongs`/`token`/`close` cross-references the macro enforces at compile time.

**Schema-derivable? YES — the pilot already proves the pattern.** The pilot's `schema/lojix.schema` declares the equivalent operation roots (`Input` lines 2-7), reply roots (`Output` lines 8-14), records, enums-with-data (`SemaCommand`/`ActorRequest`/`ActorReply` lines 59-90), and plain enums (`Phase`/`Status`/`ActivationKind` lines 53-57), and emits all the Rust via schema-next + schema-rust-next. What porting signal-lojix to schema-emitted Signal schemas entails:

1. **Move the type declarations from hand-written Rust into `signal-lojix`'s `.schema`** — the newtypes (`ClusterName`…), the records (`DeploymentRequest` with its nested `DeploymentPlan`/`BuilderSelection`), the phase enum-with-data, the cache-retention family. The pilot proves enum-with-data (`SemaCommand`), nested records, and plain enums all lower + emit cleanly (`build.rs:11-28` + `store.rs`/`codec.rs` consuming the output).
2. **Express the channel topology in schema** — this is the **one genuine substrate gap for the wire**: the production `signal_channel!` carries stream-relation metadata (`opens DeploymentObservationStream`, `belongs`, `token`, `close`) that the pilot's flat `Input`/`Output` roots do NOT yet express. The pilot has no streaming-channel-with-stream-witnesses schema construct; it threads observations as `Output::Observation(ObservedReply)` (codec.rs:129-132) without the typed open/close/belongs witnesses. **Porting the full streaming-channel wire requires either schema-next growing a `signal_channel!`-equivalent schema construct, OR the schema-derived-signal-frame work `/390` describes (which `/37/3` ranks as iteration-3 substrate work I-1, lifting component 5 from 0.7→~0.9).**
3. **Validation newtypes** — the pilot uses bare `[Text]`/`[Integer]` schema newtypes (`lojix.schema:16-35`) without the construction-time validation the production `from_text` methods carry. Validation methods would attach as methods-on-schema-emitted-nouns (the schema-at-heart pattern), which is straightforward, but the validation logic itself is hand-written method bodies, not schema-expressed.

So: **the type vocabulary is fully schema-derivable today; the streaming-channel topology (stream witnesses) is the wire-specific gap that gates a FULL port** and is exactly `/390`'s schema-derived-signal-frame direction.

## Q4 — The GAP between pilot and a real production lojix-on-schema-next

What's pilot-only that production needs real (each cited, ranked by production-blocking weight):

1. **Criome authorization — pilot is an in-memory 3-mode enum; production needs the real signal-criome client.** Pilot: `AuthorizationPolicy::{AllowAll, CriomeBackedRequired, DenyAll}` (`authorization.rs:19-24`), a local enum that doesn't talk to criome. Production: real `signal_criome::{ObjectDigest, AuthorizationScope}` integration with `submission.canonical_digest()` (production `authorization.rs:124-130`), currently fail-closed via `unavailable_until_criome_socket_lands()` (production `authorization.rs:43-49`). The schema-emitted `CriomeAuthorization (Bypass OperatorAllowlist Criome)` enum exists in the pilot schema (`lojix.schema:55`) — matching `/34/5` Decision 3's recommended typed config — but the `Criome { socket_path }` variant's real client is unbuilt in BOTH tracks. This is the same gap on both sides; it's not made worse by the schema-next port, but it's a real production prerequisite.

2. **nspawn activation — pilot is a sandbox marker; production needs real `systemd-nspawn` boot.** `/37/3` I-8 names this: the pilot's activation is `nspawn-sandbox-activate` (a `DatabaseMarker` placeholder); real activation needs root + cgroups that `nix flake check`'s chroot lacks, requiring CriomOS-test-cluster-style remote-runner plumbing. This is `/34/5`'s B-10 (end-to-end nspawn lojix smoke) and is explicitly operator-amalgamation work, not designer-pilot territory.

3. **Owner-signal triad leg — pilot ships only the ordinary signal surface.** `/37/3` I-7: lojix-next has `signal-lojix`-equivalent (the `Input`/`Output` schema) but no `owner-signal-lojix` (owner-only policy signal — builder registry, nix-config defaults). Per `skills/component-triad.md`, a full component triad is daemon + working signal + policy signal. This is `/34/5`'s B-16. The schema-next port doesn't change this — it's a net-new triad leg either way — but a "real production lojix" needs it.

4. **Wire surface breadth — pilot covers 4 operations; production needs ~9 + cache-retention + multi-phase observations.** Pilot `Input`: `Submit`/`Cancel`/`Query`/`Help` (`lojix.schema:2-7`). Production `signal_channel!`: `Deploy`/`Pin`/`Unpin`/`Retire`/`Query`/`WatchDeployments`/`UnwatchDeployments`/`WatchCacheRetention`/`UnwatchCacheRetention` + the 7-phase `DeploymentPhase` observation stream + the cache-retention pin/unpin/retire ledger. The pilot proves the PATTERN on a narrower surface; widening it to production breadth is mechanical schema-authoring EXCEPT for the streaming-channel witnesses (Q3 gap #2).

5. **Production already-durable vs pilot-now-durable — converged in `/37`.** A key reconciliation finding: the pilot's earlier in-memory-`Vec` SEMA shortcut (`/35` baseline, `/165`) is **already closed** in `/37` (sema-engine-backed, `store.rs:128-138`, restart-survival test #13). Production lean lojix was always sema-engine-backed (`deploy.rs:46-77`). So on the durability axis, pilot and production now MATCH — the difference is hand-authored records (production) vs schema-emitted `EngineRecord` (pilot, `store.rs:81-122`). This is the cleanest convergence point: porting production's `DeploymentEventRecord`/`GenerationRecord` to schema-emitted records is a like-for-like swap on the same engine.

6. **Schema-next capability gaps the wire/sema specifically hit** (per `/37/3` iteration-3 queue): vectors in SemaResponse (I-6, `GenerationLedger(Vec<GenerationRecord>)` — Spirit 883-authorized, pilot uses one-record-per-response workaround); schema upgrade traits (I-5, record 950, for wire schema bumps); streaming-channel witnesses (Q3, the `signal_channel!`-equivalent). The production wire's `Vec<NodeName>` (substituters), `Vec<Generation>` (listing), `Option<ClusterName>` (query filters) all need vector + option schema support — the pilot's `lojix.schema` uses no `Vec`/`Option` at schema positions, so this is untested at pilot scale and is a real gate for the production wire breadth.

## Q5 — Feasibility verdict: lojix signal + sema layer

**POSSIBLE — largely pilot-proven, with a bounded, quantified remaining gap.**

Evidence for POSSIBLE:
- **Signal layer schema-driven: proven.** `Input`/`Output` emit from schema; methods-on-nouns realize the lowering (`codec.rs`); `DatabaseMarker` stamped on every reply (component 5 at 0.7, `/37/3`).
- **Sema layer schema-driven AND durable: proven.** sema-engine Engine + schema-emitted `EngineRecord` + restart-survival (component 7 at 0.85, `store.rs`). This is the strongest result — it matches production's existing durability while removing the hand-authored records.
- **Nexus mail keeper: proven** (component 6 at 0.85, `nexus.rs`).
- **The port is re-grounding, not re-architecture** — both tracks sit on the same conceptual substrate (sema-engine storage, NOTA text, signal-frame wire); the pilot just makes the types schema-emitted. Production already does the hard runtime parts (real sema-engine ledger, real projection via horizon-lib, real criome digest plumbing).

Quantified remaining gap (the PARTIAL-leaning residue inside the POSSIBLE):
- **Wire streaming-channel witnesses** — the one schema-language gap specific to the signal layer (Q3 #2). Schema-next has no `signal_channel!`-equivalent for `opens`/`belongs`/`token`/`close` stream relations. Gates a FULL wire port; `/390`'s schema-derived-signal-frame (I-1) closes it. **This is the single most load-bearing schema-next capability gap for the lojix WIRE.**
- **Vectors + options at schema positions** — production wire breadth needs them (Q4 #6); pilot hasn't exercised them; Spirit 883 authorizes vectors. Incremental, not architectural.
- **Production-realities orthogonal to the port** — criome client, real nspawn, owner-signal leg (Q4 #1-3). These are production prerequisites on EITHER stack (legacy or schema-next); the schema-next port neither closes nor worsens them. They belong to `/34/5`'s bead queue (B-4/B-8 criome, B-10 nspawn, B-16 owner-signal), not to the schema-next feasibility question.

**Net:** the signal + sema LAYERS port cleanly (proven at 6.7/8.0); the wire CONTRACT ports cleanly for the type vocabulary but needs schema-next to grow streaming-channel witnesses for the full observation-stream topology; the production-realities are independent prerequisites. No blocker — the verdict is POSSIBLE with the streaming-channel-witness gap as the one schema-next capability that gates a full (not pilot-scope) wire port.

## Reconciliation summary — production-track vs pilot-track

| Axis | Production (`horizon-leaner-shape`) | Pilot (`schema-deep-iteration-2`) | Port action |
|---|---|---|---|
| Datatypes | hand-authored Rust | schema-emitted (`build.rs`) | move declarations into `.schema` |
| Wire vocab | hand-authored `signal-lojix` (~680 lines) | schema-emitted `Input`/`Output` | move into `.schema`; add validation methods |
| Wire channel/streams | `signal_channel!` w/ stream witnesses | flat `Input`/`Output`, no stream witnesses | **needs schema-next streaming-channel construct (gap)** |
| Storage | sema-engine + hand-authored records | sema-engine + schema-emitted `EngineRecord` | like-for-like record swap (same engine) |
| Text codec | `nota-codec` (legacy) | `nota-next` | substrate bump |
| Criome | real signal-criome digest, fail-closed | in-memory 3-mode enum | production prerequisite (both tracks) |
| Activation | designed; build-only today | nspawn sandbox marker | production prerequisite (both tracks) |
| Owner-signal | absent | absent | net-new triad leg (both tracks) |
| Compile state | **BROKEN** (B-0 lock break) | passes `nix flake check` | fix B-0 rename (independent of port) |

## See also

- `0-frame-and-method.md` — orchestrator frame + this Wave B brief.
- `1-horizon-datatype-and-projection-state.md` — Wave A (datatype + projection crux).
- `/34/5-overview.md` — production-track bead queue (B-0 lock break, B-4/B-8 criome, B-10 nspawn, B-16 owner-signal).
- `/37/3-overview.md` — pilot at 6.7/8.0; iteration-3 queue (I-1 schema-derived-signal-frame, I-5 upgrade traits, I-6 vectors, I-7 owner-signal, I-8 nspawn).
- `/38-source-staging-prototype-audit.md` — `/165` width iteration + three-track convergence.
- `~/wt/.../lojix/horizon-leaner-shape/src/{lib,runtime,deploy,authorization,client}.rs` — production-track source.
- `~/wt/.../lojix/schema-deep-iteration-2/{schema/lojix.schema,build.rs,src/runtime/{store,codec,nexus,authorization}.rs}` — pilot source.
- signal-lojix branch `horizon-leaner-shape` tip `a007e8b6` `src/lib.rs` — hand-authored wire contract.
