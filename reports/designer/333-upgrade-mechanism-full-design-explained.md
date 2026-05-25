*Kind: Design + Narrative · Topic: full upgrade mechanism — every part, every connection · Date: 2026-05-25 · Lane: designer*

# 333 · The upgrade mechanism, explained end-to-end

## §1 Frame

Per psyche directive 2026-05-25: *"I want to see the whole mechanism. How everything works, how the upgrade mechanism is programmed, where it gets its upgrade. I want to see all the code involved and all the operations, all the method calls. And this ideal upgrade mechanism. I want to see all the parts involved. I want to see where the header is, what it does, how it's used, how the upgrade paths are derived from the schema. I want to convince me that the agents actually understand."* Captured as Spirit intent record 547 (Principle: in-test unblock-the-blocker rule) plus the prior chain (529 cutover deferred; 530 parallel remedy; 535 real-world testing; 539 always-background subagent).

This report shows the whole mechanism — design ideal first, then the implementation gap, then the path the verification subagent will walk to prove the end-to-end story.

## §2 The story in one paragraph

A live component daemon (Spirit v0.1.0) is serving clients. The new version (v0.1.1) needs to take over without breaking those clients. The supervisor (persona-daemon, future) spawns the new daemon alongside the old. The two daemons open a private upgrade socket between them (separate from the public ordinary + owner sockets). They exchange a handshake: the new asks the old "where are you in your write log?" (marker), optionally the old streams in-memory state to the new (mirror), the new declares "I'm ready" (readiness), the old retires its public sockets, the new takes them over (completion). Clients see a brief connection-reset; their client library retries; the new daemon answers. Underneath, all of the wire types, dispatch logic, ShortHeader projection, and (one day) the version projection between old and new shapes — all of it is derived from each component's `<component>.schema` file by a brilliant macro library. That's the whole story. The rest of this report is what's behind each noun.

## §3 The `.schema` file — the single source of truth

Every component carries a `<component>.schema` file at the contract repo root. Six positional fields per `/326-v13` (the canonical schema vision):

```
{imports}
[ordinary header]
[owner header]
[sema header]
{namespace}
[features]
```

- **imports map** (curly): map of binding name → import spec. Two variants: `(ImportAll Path)` and `(Import Path [Vec EnumIdentifier])`. Pulls type names from sibling schemas into this schema's namespace.
- **ordinary header** (square): vector of root verbs each in uniform form `(VerbName [SubVariant ...])` — even single-sub-variant case uses brackets. These are the public client operations.
- **owner header** (square): same shape, for the owner-principal operations.
- **sema header** (square): same shape, for sema-engine effect operations.
- **namespace map** (curly): map of name → type body. Four value forms: `[...]` (enum), `(...)` (struct or newtype), `(Path ...)` (import reference), bare-ident (alias).
- **features** (square): cross-cutting feature blocks. Today: `(Reply ...)`, `(Event ...)`, `(Observable ...)`. Pending: `(Storage ...)`, `(Upgrade VersionRef [...])` per `/329` + operator/175.4.

Example — `signal-persona-spirit/spirit.schema` (truncated):

```
{}

[
  (State [Statement])
  (Record [Entry])
  (Observe [Records Topics])
  (Watch [State Records])
  (Unwatch [SubscriptionToken])
]

[]
[]

{
  Kind [Decision Principle Correction Clarification Constraint]
  Magnitude [Maximum Medium Minimum]
  StatementText (String)
  Statement (StatementText)
  Entry (Topic Kind Summary Context Magnitude Quote)
  ...
}

[
  (Reply RecordAccepted StateObserved RecordsObserved ...)
  (Observable (filter default) (operation_event OperationReceived) (effect_event EffectEmitted))
]

[(Version 0 1 1) (Status Live)]
```

The schema is positional NOTA — fields appear in declared order; no labels inside records. Every component's schema looks like this; the brilliant macro library reads ONE schema per contract.

## §4 The schema engine — from `.schema` text to `AssembledSchema`

`/git/github.com/LiGoldragon/schema/` (created 2026-05-24) is the typed substrate. Two phases:

**Phase 1 — Parse.** `schema/src/parser.rs` reads NOTA text into a `SchemaDocument`: six positional fields populated with `Declaration` / `HeaderRoot` / `TypeExpression` / `Feature` / `Version` records. Not yet semantically resolved (no imports loaded, no UIDs minted).

**Phase 2 — Lower.** `schema/src/document.rs::assemble()` walks the document and dispatches each node to a `BuiltinMacroVariant` lowerer (per `/329` + operator/175.4). Each lowerer accumulates `AssembledFragment` entries into an `AssembledSchemaBuilder`. Result: an `AssembledSchema` with:

```rust
pub struct AssembledSchema {
    pub imports: Vec<AssembledImport>,
    pub routes: Vec<Route>,            // (leg, root_slot, root, endpoint_slot, endpoint, body_type)
    pub types: Vec<AssembledType>,     // local + imported (qualified by binding)
    pub features: Vec<AssembledFeature>,
}
```

Routes are the canonical dispatch table: leg ∈ {ordinary, owner, sema}, root_slot is the first ShortHeader byte (0-7 typically), endpoint_slot is the second byte (0-255).

The 4 builtin lowerers today: `ImportMacro` / `HeaderMacro` / `TypeMacro` / `FeatureMacro`. Three more proposed but not landed: `NewtypeDefinition` / `FieldType` (separate from generic Type) / `UpgradeRule` (per /329 + nota-designer/8).

`schema/src/reader.rs::LoadedSchema::read_path()` is the entry point: takes a `.schema` path, recursively resolves imports (loads sibling schemas via the same reader), assembles, returns `AssembledSchema`.

## §5 The brilliant macro library — from `AssembledSchema` to Rust code

`signal-frame/macros/src/schema_reader.rs` is the proc_macro side. Today it has its own parser (a bridge, soon to be replaced by `schema::LoadedSchema::read_path` per nota-designer/8). The invocation is `signal_channel!([schema])` — invoked once per contract at `src/lib.rs` (e.g., `signal-persona-spirit/src/lib.rs:435`).

The macro reads the schema, assembles, then emits (today, per operator/176 audit + my /332):

| Emission | Status | Implemented in |
|---|---|---|
| `Operation` enum (per-leg) | wired | emit.rs ~line 99 |
| `Reply` enum | wired | emit.rs |
| `Event` enum | wired | emit.rs |
| `OperationHandler` trait (async methods per variant) | wired | emit.rs line 389 |
| `OperationDispatch` blanket impl (matches operation to handler call) | wired, test-only consumer | emit.rs line 442 |
| `LogVariant` impl (the 64-bit ShortHeader) | wired outbound | emit.rs line 348 |
| Frame / FrameBody / Request / RequestBuilder type aliases | wired | emit.rs |
| `NotaEncode` / `NotaDecode` codecs | wired | emit.rs line 995 |
| `ObserverSet` runtime + `ObserverFilterMatch` | wired | emit.rs (Observable feature) |
| Storage descriptors (`TableName`, `TableDescriptor<T>`) | NOT IMPLEMENTED | (`(Storage ...)` feature pending) |
| `VersionProjection` derives | NOT IMPLEMENTED | (`(Upgrade ...)` macro variant pending) |
| Per-contract CLI dispatcher | partial (frame builders only) | emit.rs |

So the macro emits the **wire types + the codec + the dispatcher** end-to-end. It does NOT emit storage glue or version projections yet — those are operator's `primary-ezqx.1` next slice.

Each emitted symbol is a real Rust item that compiles into the contract crate. There is no runtime schema parsing on the hot path; everything is compile-time emit.

## §6 The ShortHeader — what flows on the wire

Every frame on every socket starts with a 64-bit `ShortHeader`. Bytes 0-7 carry the operation route:

```
byte 0: root_slot     — which root variant of the Operation enum (0..7 typically)
byte 1: endpoint_slot — which sub-variant under that root
bytes 2-7: reserved   — currently zero
```

**Outbound use** (`LogVariant::log_variant`): when a client sends `Operation::State(Statement{ ... })`, the macro-emitted `log_variant()` method returns `0x_00_00_00_00_00_00_00_00` (State is root_slot 0, sole endpoint is endpoint_slot 0). The frame writer prepends this header to the rkyv-encoded body.

**Receive-side use** (`OperationDispatch::dispatch_operation`): the daemon peeks the first byte (the root_slot), classifies the route, and dispatches to the matching handler. Per operator/176 audit: this dispatch is **generated and tested but NOT yet on the daemon's production ingress path**. Today daemon ingress decodes the full Operation body first, then matches; the generated peek-first dispatch is a future slice (operator/176 §"Highest-Value Next Work" item 1).

The ShortHeader is what makes routing cheap: a daemon can decide "this is a State request" without decoding the Statement body. That matters for fan-out subscribers (every Mind-tap that subscribes to a stream peeks the header to filter without paying the body-decode cost).

## §7 The three sockets — public + public + private

Every component daemon binds three Unix sockets under its per-version state directory (e.g., `/home/li/.local/state/persona-spirit/v0.1.0/`):

1. **`spirit.sock` — ordinary**. Public. Clients use this. Carries `Operation` requests from the ordinary header. Permissions 0600 to the daemon user.
2. **`owner.sock` — owner**. Public to the owner principal only. Carries owner-only operations from the owner header.
3. **`upgrade.sock` — private upgrade**. Supervisor-only. Carries `signal-version-handover::Operation` (AskHandoverMarker / Mirror / Divergence / etc.). NOT public; only the supervisor (or its delegate) can dial it during cutover. Permissions 0600.

The unsuffixed `spirit` command is a thin shell wrapper (`spirit-v0.1.0` or `spirit-v0.1.1` selected by `criomosHome.personaSpirit.currentDefault`) that sets the right socket env vars + execs the right CLI binary. The selector flip changes which wrapper `spirit` symlinks to.

Per-version sockets means BOTH daemon versions can run concurrently (each in its own state dir) without socket-name collision. That's the entire premise of the side-by-side deployment.

## §8 The handover ceremony — the new daemon talks to the old daemon

The conversation flows on the private upgrade socket. Today both Spirit v0.1.0.1 (operator's just-landed retrofit per operator/178) and v0.1.1 bind it. Earlier they didn't.

Four message families, defined in `signal-version-handover::Operation`:

```rust
pub enum Operation {
    AskHandoverMarker(MarkerRequest),       // wired both sides
    ReadyToHandover(ReadinessReport),       // wired both sides
    HandoverCompleted(CompletionReport),    // wired both sides
    Mirror(MirrorPayload),                  // typed, orchestrate payload landed (per second-operator/185), wire pending
    Divergence(DivergencePayload),          // typed, not wired
    RecoverFromFailure(RecoveryRequest),    // typed, not wired
}
```

**The marker phase** (wired, used by Spirit MVP):

1. New daemon connects to old's upgrade socket.
2. New: `AskHandoverMarker(MarkerRequest { ... })`. Old replies: `HandoverMarker { commit_sequence, write_counter, last_record_identifier }`. The marker is "I have written up to here."
3. New: `ReadyToHandover(ReadinessReport { marker })` — echoing the marker back as proof of receipt. Old: `HandoverAcceptance(accepted_marker)`.
4. New: `HandoverCompleted(CompletionReport)`. Old removes `spirit.sock` + `owner.sock` and replies `HandoverFinalization`. Old then exits.

Clients connected to the old daemon get `ECONNRESET`. Their client library retries against the (now-removed) `spirit.sock`, which immediately fails again — until the new daemon (which has already bound `spirit.sock` in its own state dir) gets matched by the selector flip. Then retries hit new and succeed.

**The mirror phase** (typed, orchestrate payload landed, wire pending):

For components with critical in-memory state (orchestrate has in-flight lane claims; Spirit does NOT), an extra exchange between marker and readiness:

5b. Old: `Mirror(MirrorPayload)` — encodes the in-memory state as a typed snapshot. Per second-operator/185 commit `72105447`, orchestrate's `MirrorPayload` carries claims + lanes as a `MirrorSnapshot` rkyv record.
6b. New: `MirrorAcknowledgement` — applies the snapshot to its own DB (or in-memory).

For Spirit, this phase is skipped — there's nothing in memory to transfer (writes are sync to redb).

**The divergence path** (typed, not wired):

At any phase, either daemon can send `Divergence(DivergencePayload { reason: DivergenceReason })` to abort. Reasons (typed): `SchemaIncompatible`, `MarkerConflict`, `MirrorPayloadInvalid`, etc. The other side ACKs and aborts; the supervisor is notified; old keeps serving.

**The recovery path** (typed, not wired):

If either daemon crashes mid-ceremony, the supervisor (persona-daemon, primary-a5hu) detects it via process supervision and either restarts the new daemon to retry from marker, or signals the old daemon to abandon the in-progress handover.

State machines per `/175` (second-designer's design):
- Old: `Serving → MarkerOffered → [MirrorStreaming →] Acknowledging → ReadinessAcknowledged → Draining → Completing → SocketsRetired → Exiting`
- New: `Spawning → DatabaseOpened → ConnectingToOld → RequestingMarker → [MirrorReceiving →] ReadyToCommit → ReadinessSent → SocketBinding → Completing → Serving`

## §9 The version projection — between schema-shape revisions

When v0.1.0's record shape differs from v0.1.1's (e.g., Spirit's `Certainty` enum widened to universal `signal-sema::Magnitude`), data must be re-encoded during cutover. Two patterns:

**Today — hand-written `historical` + `current_shape` modules** per the spirit-cli skill canonical pattern. Inside the migration crate:

```rust
mod historical {
    // private rkyv reproduction of the deployed old types — every leaf
    #[derive(rkyv::Archive, ...)] pub struct Entry { ..., pub certainty: Certainty }
    #[derive(rkyv::Archive, ...)] pub enum Certainty { Maximum, Medium, Minimum }
    // ...
}
mod current_shape {
    // current types with explicit From impls for the changed fields
    impl From<historical::Entry> for signal_persona_spirit::Entry { ... }
    impl From<historical::Certainty> for signal_sema::Magnitude { ... }
}
```

Live example: `/git/github.com/LiGoldragon/upgrade/src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs:102-318` (six From impls; per /332 audit).

**Ideal — schema-diff-derived `(Upgrade ...)` macro variant**. The v0.1.1 `.schema` would carry an `(Upgrade (FromVersion 0 1 0) (Migrate Certainty Magnitude CertaintyToMagnitude) (RenamedFrom ...) (Drop ...) ...)` section. The brilliant macro library would lower this section into the same `historical` + `current_shape` + `From`-chain pattern automatically. Pending — bead `primary-cklr` (land UpgradeRule in schema crate) + `primary-ezqx.1` (proc_macro emission).

The schema-diff approach is the long-term play because hand-written migration cost compounds per component per version-step.

## §10 The migration driver — where the projection actually runs

Today: `/git/github.com/LiGoldragon/upgrade/src/bin/upgrade-spirit-sandbox-test.rs`. Takes one argument — a path to a v0.1.0 redb. Copies the source to a sandbox temp dir. Runs `MigrationCatalogue::prototype().migrate_database(...)` which walks the v0.1.0 records, applies the `From`-chain projections, writes to a v0.1.1-shape target redb. Reads back the target through the current crate's reader. Prints `(SandboxUpgradeSucceeded <records-migrated> <records-readable> [source] [target])`.

This is **offline migration**: the daemon doesn't drive it; an external Rust binary does. Designer's spirit-nspawn worktrees wrap this binary inside an nspawn container.

For the **live** cutover, this binary moves INSIDE the new daemon's startup sequence:
1. New daemon spawned with the source redb path (from spawn envelope per persona-daemon supervisor).
2. New daemon COPIES the source redb (or, per second-designer's update to /175 — takes a snapshot via marker).
3. New daemon MIGRATES the copy in-place (applies the `From`-chain).
4. New daemon opens its migrated DB as authoritative.
5. New daemon dials old daemon's upgrade socket → starts the handover ceremony.

The "freeze writes during migration" question is what /331 settled with the brief-outage MVP: old daemon stops accepting writes at AskHandoverMarker; resumes only if the handover aborts.

## §11 The supervisor + the selector — persona-daemon's role

Today the supervisor is **systemd** (user services per CriomOS-home `modules/home/profiles/min/spirit.nix`) + **manual selector flip** (edit `criomosHome.personaSpirit.currentDefault` from `"v0.1.0"` to `"v0.1.1"`, run `home-manager switch`).

Tomorrow (`primary-a5hu`) the supervisor is `persona-daemon`:
- Owns the spawn envelope (`signal-engine-management::SpawnEnvelope`) — when it spawns the new daemon, the envelope carries the upgrade socket path, the source DB location, the current contract version marker, and the supervisor's authority token.
- Owns the ceremony orchestration — calls AskHandoverMarker, watches for divergence, handles Recovery on either daemon's crash.
- Owns the selector flip — atomically updates the active-version pointer (replacing CriomOS-home's symlink mechanism) so the unversioned `spirit` command immediately resolves to the new wrapper.

The supervisor is the only party that survives every failure mode (old crash, new crash, ceremony stall, network partition). Recovery is supervisor-driven. Confirmed in the most recent chat exchange: persona-daemon is the supervisor; no alternative.

## §12 Per-component variation — Spirit minimal vs orchestrate full

| Component | DB write semantics | In-memory critical state | Ceremony shape | Status |
|---|---|---|---|---|
| **Spirit** | sync-to-redb per request; acked == durable (proven by probe) | none | marker-only (3 steps) | **WIRED** — v0.1.0.1 + v0.1.1 both bind upgrade socket; designer probe + nspawn test cover the durability story |
| **Orchestrate** | mixed (lane claims in-memory before persist) | in-flight claims + lane registry | marker + **mirror** + completion | mirror PAYLOAD landed (second-operator/185), wire pending |
| **Mind** | mostly persistent, some async buffers | possibly buffered thoughts | likely marker + mirror | per-component assessment pending |
| **Persona-introspect, terminal, router, message, harness, …** | varies | varies | per-component assessment | not started — these still use hand-written `signal_channel!`, no schema yet |

The MECHANISM is uniform (same socket topology, same message family); the PHASE SET enabled per component varies (Spirit skips Mirror; orchestrate requires it; others TBD).

## §13 Implementation status matrix — what's wired, what's typed-only, what's hand-written, what's missing

| Piece | Status | Where | Bead |
|---|---|---|---|
| Schema file authoring | wired (75 concept + spirit.schema + orchestrate.schema + version-handover.schema) | `<component>/<name>.schema` | n/a |
| `schema` crate (parse + assemble) | wired | `/git/.../schema/src/` | n/a |
| `BuiltinMacroVariant` (4 of 7) | wired | `schema/src/engine.rs` | `primary-cklr` adds UpgradeRule |
| Proc_macro `signal_channel!([schema])` for ordinary | wired (Spirit only) | `signal-frame/macros/` | `primary-ezqx.1` |
| Same for owner signal Spirit | NOT — owner-signal-persona-spirit still hand-written | (operator/176 §"Coverage Matrix") | follow-on bead |
| `signal_channel!([schema])` for non-Spirit contracts | NOT — orchestrate has schema authored, port pending macro extension (multi-endpoint + unit payload); version-handover converted in `primary-ekxx` with field-naming gap (`primary-zfxx`) | `signal-frame/macros/src/schema_reader.rs` | macro extension |
| LogVariant outbound | wired | emit.rs | n/a |
| OperationDispatch receive-side | generated + tested but NOT on daemon ingress | (operator/176 §1) | next operator slice |
| ShortHeader-peek-before-decode at ingress | NOT | n/a | operator |
| Three-socket topology (ordinary + owner + upgrade) | wired both Spirit versions | persona-spirit daemon.rs | `primary-wdl6` (just landed) |
| AskHandoverMarker / ReadyToHandover / HandoverCompleted | wired both Spirit sides | persona-spirit + handover-driver | done |
| Mirror payload (orchestrate) | wired | `/git/.../orchestrate/src/handover.rs` | second-operator/185 commit `72105447` |
| Mirror wire (any component) | NOT — daemon socket dispatcher pending | n/a | second-operator next slice |
| Divergence + Recovery wire | NOT — typed only | `signal-version-handover/src/lib.rs` | designer-named Q6 |
| Hand-written V010ToV011 projection | wired | `upgrade/src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs` | n/a |
| Schema-diff-derived projection | NOT — needs UpgradeRule + proc_macro | n/a | `primary-cklr` + `primary-ezqx.1` |
| Migration driver (in-process) | wired | `upgrade/src/bin/upgrade-spirit-sandbox-test.rs` | n/a |
| Daemon-driven snapshot+migrate+handover | NOT — current path is offline-migrate-then-cutover | n/a | future |
| Supervisor = persona-daemon | NOT — `primary-a5hu` blocked on persona-engine deploy | n/a | `primary-a5hu` |
| Selector flip via persona-daemon | NOT — currently CriomOS-home `currentDefault` + manual home-manager switch | `modules/home/profiles/min/spirit.nix` | `primary-a5hu` |
| nspawn sandbox single-sided | wired | `spirit-nspawn-handover-socket` branch | `primary-dlut` |
| nspawn sandbox two-sided | NOT — `primary-wdl6` just landed but nspawn-side not rerun against v0.1.0.1 | n/a | this report's subagent |
| In-transition probe | wired + empirically validated "acked == durable" | `spirit-nspawn-in-transition-probe` | `primary-1jql` |

## §14 What the verification subagent will do — the "unblock blockers in the test" mission

Per spirit record 547 (just captured): the verification subagent has license to BUILD whatever blockers it hits, inside the test fixture. It is not asked to refuse a test because a dependency is missing. It is asked to make the test work, even if that means stubbing a supervisor, hand-coding a Mirror handler for Spirit (even though Spirit doesn't need one in production), or whatever the test demands.

Concrete mission:
1. Read this report. Identify what's wired vs missing per §13.
2. On a fresh feature branch under `~/wt/github.com/LiGoldragon/CriomOS-test-cluster/`, build an end-to-end test of the FULL upgrade ceremony for Spirit:
   - Use operator's just-landed v0.1.0.1 (per operator/178) — both Spirit versions now bind the upgrade socket
   - Drive the marker ceremony with both daemons concurrently
   - Build a STUB persona-daemon (just enough to drive the ceremony, kill old, flip selector) inside the test fixture — don't wait for `primary-a5hu`
   - Build a STUB Mirror handler for Spirit (even though Spirit's mirror payload is empty, exercise the wire) — surfaces whether the protocol surface is complete
   - Build a Divergence path (force a marker mismatch) to validate the abort flow
   - Run on Prometheus via criomos-nspawn (real-world conditions per record 535)
3. Report back: which probes pass, which surface gaps, what the implementation actually shows when exercised end-to-end. Real findings.

This is the "trust but verify" pass on this design narrative. If §3-§12 are right, the subagent will validate the story. If they're wrong, the subagent will surface the deviation.

## §15 References

- `reports/second-designer/175-upgrade-mechanism-full-design-2026-05-25.md` — second-designer's parallel design, with state machines + sequence diagram for the full ceremony
- `reports/operator/176-schema-macro-upgrade-integration-audit/5-overview.md` — operator's audit of what's wired vs aspirational
- `reports/operator/178-primary-wdl6-spirit-v0-1-0-protocol-build-2026-05-25.md` — operator landed v0.1.0.1 with upgrade socket
- `reports/second-operator/185-orchestrate-mirror-handover-implementation-2026-05-25.md` — orchestrate Mirror payload landed
- `reports/operator/161-spirit-private-handover-socket-2026-05-22.md` — v0.1.1 upgrade socket original work
- `reports/operator/160-spirit-smart-handover-sandbox-test-2026-05-22.md` — 8 probe outputs reference
- `reports/designer/330-parallel-implementation-pivot-and-spirit-nspawn-plan.md` — nspawn substrate + in-transition analysis
- `reports/designer/332-schema-macro-coverage-audit.md` — implementation-vs-vision audit
- `reports/designer/331-spirit-cutover-mvp-proposal.md` — brief-outage cutover MVP script (deferred per record 529)
- `reports/nota-designer/8-nota-schema-lowering-deviation-audit.md` — schema-engine ownership audit + lowering pipeline shape
- `reports/designer/326-v13-spirit-complete-schema-vision.md` — canonical six-position schema
- `reports/designer/329-schema-macro-component-extensibility.md` — BuiltinSchemaMacro extension shape
- `/git/github.com/LiGoldragon/schema/` — typed schema crate (parse + assemble)
- `/git/github.com/LiGoldragon/signal-frame/macros/` — brilliant macro library substrate (proc_macro emit side)
- `/git/github.com/LiGoldragon/signal-version-handover/src/lib.rs` — handover protocol contract
- `/git/github.com/LiGoldragon/persona-spirit/src/daemon.rs` — three-socket binding
- `/git/github.com/LiGoldragon/upgrade/src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs` — hand-written projection (the reference output)
- `/git/github.com/LiGoldragon/upgrade/src/bin/upgrade-spirit-sandbox-test.rs` — migration driver
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix` — side-by-side deployment + selector
- `~/wt/github.com/LiGoldragon/CriomOS-test-cluster/spirit-nspawn-handover-socket/` — single-sided handover test (subagent A, commit `efa557c0`)
- `~/wt/github.com/LiGoldragon/CriomOS-test-cluster/spirit-nspawn-in-transition-probe/` — durability probe (subagent B, commit `36877421`)
- Spirit records: 508 (parallel implementation), 512 (nspawn acceptance gate), 518 (designer feature branches), 527 (no /nix/store paths), 528 (in-transition test), 529 (cutover deferred), 535 (real-world testing), 539 (always-background subagent), 547 (in-test unblock-the-blocker)
