---
title: "71.1 — Stack rewrite study: triad-engine + schema substrate and lojix/horizon adoption"
role: system-designer
variant: Research
date: 2026-06-04
topics: [schema, triad-engine, lojix, horizon-rs, signal-lojix, component-shape, schema-rust-next, spirit, rewrite]
description: |
  Deep map of the stack rewrite: the stabilizing triad-engine + schema substrate
  architecture; the reference component shape (spirit pilot); lojix's current
  hand-written shape and the concrete adoption path; horizon-rs's "hack" status
  and what the regular component shape would require; the two deploy stacks and
  their relationship to the rewrite. Load-bearing facts for the psyche.
---

# 71.1 — Stack Rewrite Study

## A. The Triad-Engine + Schema Substrate (Stabilizing)

### A.1 Architecture Overview

The schema-derived component architecture (records 1574/1581, 2560, 2563, 2564)
rests on three coupled systems:

1. **Schema composition** (schema-next + schema-rust-next): author a `.schema` file
   in NOTA; schema-next lowers it to assembled `Asschema` data; schema-rust-next
   emits Rust source code.

2. **Three-engine triad** (SEMA + Nexus + Signal): three generated trait interfaces
   that partition all daemon logic strictly—SEMA (database), Nexus (decisions),
   Signal (communication)—with no leakage across planes.

3. **Runtime runner** (triad-runtime): shared generic mechanics for socket lifecycle,
   frame transport, and the recursive Nexus loop, so components write only domain
   logic.

The current state:

- **Schema-next** (operator-owned `main`): consumes `.schema` files, resolves macros,
  emits `Asschema` data. Known bug: dual lowering engines at `lower_source` (drops
  bare-header payloads) vs the source path (resolves them)—upstream of every
  component (record 1586, reported in designer/500).

- **Schema-rust-next** (operator-owned `main`): consumes `Asschema`, emits Rust
  source. Data-before-text discipline applies only to type declarations; the impl
  layer remains 504 hand-indented `self.line()` calls (unchanged since audit 495).
  The `RustItem`/`RustImplBlock`/`RustMatch` token model is ratified (1576/1584)
  but not landed.

- **Triad-runtime** (library): owns `LengthPrefixedCodec`, `ComponentCommand`,
  `Runner` (recursive Nexus loop over typed `NextStep`), `TraceLog`, and
  `TraceSocketListener`. The generic `TriadComponent::serve()` daemon runner
  (1574/1581) is **not yet built**—most-repeated missing noun. Components
  hand-write their accept loops and transport today.

### A.2 The Three Engine Traits (Structural Separation)

**Signal, Nexus, and SEMA engine traits are emitted by schema-rust-next and
enforced by Rust's type system.**

From `schema-rust-next/ARCHITECTURE.md` and the spirit pilot audit (501):

**SignalEngine** (`signal::Signal` envelope):
- Owns all wire communication: admission (route/identifier minting, validation),
  triage by short header, frame encode/decode (generated on Signal types).
- Signature: `impl SignalEngine for SignalActor` (spirit/src/engine.rs:180-231).
- Schema-emitted frame codec: `Input::encode_signal_frame`, `Input::decode_signal_frame`
  (spirit/src/schema/lib.rs:1145, 1154); same for `Output` (1213, 1222).
- Constraint (record 2560): Signal logic cannot touch durable state or make domain
  decisions; all logic is admission, validation, framing.

**NexusEngine** (`nexus::Nexus` envelope):
- Owns all domain decisions: the decide loop (step_decide), per-fact deciders
  (decide_signal_arrival, decide_sema_write_completion, decide_sema_read_completion,
  decide_effect_completion), and the Observe→Stash→Reply recursion.
- Signature: `impl NexusEngine for Nexus` (spirit/src/nexus.rs:222-268).
- The `ContinuationBudget` policy (nexus.rs:22-47) gates recursive continuation
  depth (default 32).
- Constraint (record 2560): Nexus owns typed decisions only; it cannot call the
  Signal/SEMA planes directly (type error if attempted)—the mail keeper is
  Nexus's only bridge to durable state.

**SemaEngine** (`sema::Sema` envelope):
- Owns ALL durable database code: redb transactions, rkyv archive/dearchive,
  table operations (record, observe, lookup, count, remove, commit).
- Signature: `impl SemaEngine for Store` (spirit/src/store.rs:194-332).
- Production components use `sema-engine` (the typed database engine library);
  spirit pilot **incorrectly uses raw redb** (report 63, bead `primary-w42y`).
- Constraint (record 2563): no component daemon makes direct `redb::Database`
  calls; all durable work routes through `sema-engine` (the intended exclusive
  database boundary).

### A.3 What Schema Emits

From `schema-rust-next/ARCHITECTURE.md` and the "schema-in-action" demonstration
(designer/500 entry 1):

**Type declarations** (Rust equivalents of schema nouns):
- Aliases: `Topic String` → `pub type Topic = String;`
- Newtypes: `Record { Entry }` → `pub struct Record(pub Entry);`
- Structs: `Entry { Topics * Kind * ... }` → `pub struct Entry { pub topics: Topics, pub kind: Kind, ... }`

**Enum variants and constructors** from namespace bindings:
- A bare-name header like `[Record Observe Lookup Count Remove LookupStash]` at
  `spirit.schema:2` emits the full `Input` enum, its constructors, and FromStr.
- Variant payloads are named-type bindings (e.g., `RecordAccepted SemaReceipt`),
  so enum variants carry direct payloads instead of wrapper structs.

**Engine traits + plane envelopes**:
- `SignalEngine`, `NexusEngine`, `SemaEngine` (three generic trait impls).
- `Signal<Root>`, `Nexus<Root>`, `Sema<Root>` plane envelopes (auto-generated
  wrappers carrying origin_route + the root object).
- Per-plane `Plane::{Signal,Nexus,Sema}` match enum for code needing to branch
  across planes (only when using the bootstrap all-in-one runtime target).

**Wire codec** (rkyv + optional NOTA):
- `encode_signal_frame` / `decode_signal_frame` on `Input` / `Output` (binary
  rkyv round-trip).
- NOTA text codec (`NotaEncode`/`NotaDecode`) emitted behind the `nota-text`
  feature, so the daemon can skip NOTA codegen for its lean binary build.

**Emission targets** (per `RustEmissionTarget`):
- `WireContract`: external signal or meta-signal contract (schema nouns, rkyv,
  NOTA, short headers, encode/decode frame methods).
- `SignalRuntime` / `NexusRuntime` / `SemaRuntime`: per-plane daemon support
  (envelope, route/trace vocabulary, engine trait and lifecycle hooks).
- `ComponentRuntime`: bootstrap compatibility target (old combined Signal/Nexus/SEMA
  in one schema + cross-plane projections).

### A.4 What Is Stable vs In Flux

**Stable (proven, main branch, structural):**

- The three-engine plane-envelope type system (SignalEngine, NexusEngine, SemaEngine).
  A cross-engine call is a **compile-time type error** (spirit pilot ships a
  `compile_fail` doctest proving `Store::apply` is unreachable from Nexus).
- Schema type declaration → Rust code emission (aliases, newtypes, structs).
- Namespace binding → enum variant payload mapping.
- rkyv frame codec emission on Signal types.
- NOTA text codec emission (feature-gated).
- The `triad-runtime` library surface (LengthPrefixedCodec, Runner, TraceLog).

**In flux (ratified intent, not yet main):**

- The dual-engine bug in schema-next (record 1586, operator work: fix at lowering).
- The RustItem token model for impl emission (1576/1584, operator work: replace
  504 hand-indented lines).
- The generic `TriadComponent::serve()` runner (1574/1581, operator work: extract
  from spirit's hand-written accept loop into triad-runtime).
- The sema-engine adoption in spirit pilot (bead `primary-w42y`, operator work:
  replace raw redb with sema-engine calls).
- The SymbolPath flat-vs-structured shape (record 1586, psyche decision reopened).

## B. The Reference Component Shape (Spirit Pilot)

### B.1 What the Author Writes (Hand-Written Layer)

From `spirit/ARCHITECTURE.md` and source inspection (spirit/src/):

**Three trait implementations** (domain logic):

1. `impl SignalEngine for SignalActor` (src/engine.rs:180-231):
   - Admission: mints origin route, issues message identifier, validates.
   - Triage: branches on short header to dispatch Input variants.
   - Reply framing: converts Nexus action into Output frame.

2. `impl NexusEngine for Nexus` (src/nexus.rs:222-268):
   - The decide loop: consume mail → decide → act → re-consume.
   - Per-fact deciders: routes the four mail-trigger shapes.
   - Observe→Stash→Reply recursion: a genuine domain decision (read result
     becomes a Stash command, not a direct reply).

3. `impl SemaEngine for Store` (src/store.rs:194-332):
   - Durable table operations: `record`, `observe`, `lookup`, `count`, `remove`,
     `ensure_tables`, `committed_record_count`, `commit_sequence`.
   - rkyv round-trip of Entry rows: archive on write, dearchive on read.
   - **CURRENT BUG**: raw `redb::Database` calls instead of `sema-engine`.

**Data-bearing nouns** (generated + hand-written):

- Record types from schema namespace: `Entry`, `Query`, `RecordIdentifier`, etc.
  (generated by schema-rust-next).
- Runtime centers: `SignalActor`, `Nexus`, `Store` (hand-written Rust structs,
  no schema encoding—they hold the trait impl).
- In-memory bookkeeping: `StashTable` (HashMap handle store in Nexus, nexus.rs:55),
  `MailLedger` (Vec behind Mutex in Engine, engine.rs:53-56).

**Schema file** (authored):

- One `.schema` file: `spirit/schema/lib.schema` (current bootstrap all-in-one).
- Declares the wire vocabulary (Input, Output enum variants), the SEMA namespace
  (Query, Entry), the Nexus namespace (Mail, Action).
- **Future split**: separate `signal.schema`, `nexus.schema`, `sema.schema` per
  plane (ratified; not yet split).

**Transport + daemon scaffolding** (hand-written, awaiting runner extraction):

- `daemon.rs:152` (Daemon::run): socket bind, UnixListener loop, per-stream
  dispatch. **Zero domain logic.**
- `transport.rs:84-100` (SignalTransport): length-prefix framing delegates
  encode/decode to schema-emitted `encode_signal_frame`/`decode_signal_frame`.
- `config.rs`: DaemonCommand, configuration loading, startup.
- `bin/spirit-daemon.rs`, `bin/spirit.rs`: thin entry points (load config, start
  or connect, run).

### B.2 What Is Generated

All of the following are emitted by schema-rust-next at build time (checked into
`src/schema/lib.rs`):

**Type declarations** (spirit/src/schema/lib.rs lines 1-100+):
- Type aliases (String, Integer, Boolean, Path, etc.).
- Newtype wrappers (RecordIdentifier, TopicMatch, etc.).
- Record structs (Entry with Topics, Kind, Description, Magnitude, Privacy, etc.).
- Enum variants and payload types.

**Engine traits with lifecycle**:
- `SignalEngine::on_start`, `on_stop`, plus `admit`, `triage_inner`, `reply_inner`.
- `NexusEngine::on_start`, `on_stop`, plus `decide`.
- `SemaEngine::on_start`, `on_stop`, plus `apply`, `observe`, and the five
  database verbs.
- Default lifecycle hooks (no-ops unless `testing-trace` feature).

**Plane envelopes**:
- `signal::Signal<Input>`, `signal::Signal<Output>` (with origin_route).
- `nexus::Nexus<NexusWork>`, `nexus::Nexus<NexusAction>` (with origin_route).
- `sema::Sema<WriteInput>`, `sema::Sema<ReadInput>` (with origin_route).
- Projection enum: `Plane::{Signal,Nexus,Sema}` (bootstrap compatibility only).

**Frame codec**:
- `Input::encode_signal_frame() -> (ShortHeader, RkyvArchive)`
- `Input::decode_signal_frame(ShortHeader, RkyvArchive) -> Result<Input>`
- Same pair for Output (generated at spirit/src/schema/lib.rs:1145, 1154, 1213, 1222).

**Trace support** (when `testing-trace` feature enabled):
- `TraceEvent` newtype (generated).
- `SignalObjectName` enum (triaged, sent, rejected, etc.).
- `NexusObjectName` enum (entered, decided, acted).
- `SemaObjectName` enum (write applied, read observed, etc.).
- Hook implementations that emit `TraceEvent` via `TraceLog`.

**NOTA text codec** (behind `nota-text` feature):
- `NotaDecode`/`NotaEncode` derives on all types.
- `FromStr` on enum roots.
- `Display` on all types.
- Omitted from the lean daemon binary; only the CLI includes it.

### B.3 The Boundary: Spirit as a Real Working Example

The spirit pilot (github.com/LiGoldragon/spirit) is the **only currently deployed
schema-derived component** following the triad shape:

- **Wire**: signal-spirit contract (records, NOTA/rkyv codecs).
- **Daemon**: 489 lines in engine.rs, 304 in nexus.rs, 359 in store.rs = ~1200
  lines of hand-written domain logic (plus 74 transport, 168 daemon scaffolding).
- **Test surface**: process-boundary tests prove Signal→Nexus→SEMA event sequences
  over a real Unix socket with real rkyv frames.
- **Production status**: not yet deployed to production; blocked on sema-engine
  adoption (record 2563).

---

## C. Lojix Current State + Adoption Path

### C.1 Current Lojix Shape (horizon-leaner-shape Branch)

**Status**: In-development on feature branch. Not yet on main; docs on main are
skeleton. Current implementation exists only on `horizon-leaner-shape`.

**Current architecture** (horizon-leaner-shape, NOT triad-derived):

- **One crate, two binaries**: lojix-daemon (long-lived orchestrator), lojix
  (thin CLI client).
- **Wire**: signal-core frames carrying signal-lojix records. signal-lojix is
  currently a **skeleton**—no Cargo.toml, no src/, no implementation (active-repositories.md:112).
- **Storage**: sema-engine (the typed database engine library). Daemon owns one
  redb file (hand-opened via sema-engine, correct boundary). Tables registered
  at startup: live set, GC roots, event log, container-lifecycle.
- **Actors**: Kameo supervisor with per-deployment actors (DeploymentActor,
  DeploymentLedgerActor, GarbageCollectionRoots, CriomeAuthorization). No use
  of generated Signal/Nexus/SEMA engine traits.
- **Runtime root**: RuntimeRoot holds the configuration and spawns child actors.
  Accepts RuntimeRequest messages (AllocateDeployment, StartDeployment, etc.).
  This is **hand-written actor choreography**, not the triad pattern.

**Explicit non-triad structure** (from lojix/src/lib.rs comments):

- "The current runtime slice owns the Signal socket path, typed startup
  configuration, and a Kameo RuntimeRoot that accepts build-only deployment
  submissions."
- "A CriomeAuthorization actor must grant the canonical deployment request
  digest before build jobs run in per-deployment actors."
- Actors coordinate via Kameo mailbox passing (internal actor messages), not
  via the Nexus mail-keeper + decide-loop pattern.

### C.2 The Gap: Lojix vs the Triad Shape

**Today's lojix** (horizon-leaner-shape):

- Hand-written Kameo actor supervision.
- No generated Signal/Nexus/SEMA engine traits.
- Hand-written socket listener + frame dispatch (daemon.rs + socket.rs).
- Per-deployment Kameo actors (correct use of actor framework), but orchestrated
  via actor-message passing, not the typed Nexus work/action shape.
- Signal contracts are hand-authored (no schema).

**What the triad shape requires**:

1. A `lojix.schema` file (NOTA, authored once):
   - Wire vocabulary: Deploy, Pin, Unpin, Retire, Query, Watch, Unwatch verbs.
   - Output shapes: Deployed, Pinned, Unpinned, Retired, Queried, Watching,
     typed rejection reasons.
   - Event shapes: DeploymentPhaseEvent, CacheRetentionTransitionEvent streams.
   - Namespace: record types used by Nexus (DeploymentWork, DeploymentAction,
     generation ledger query shapes, etc.).

2. Schema-rust-next emission (automatic at build.rs):
   - Input enum from Deploy/Pin/Unpin/Retire/Query/Watch/Unwatch.
   - Output enum from success/rejection variants.
   - SignalEngine trait (admission, triage, reply).
   - NexusEngine trait (the decide loop, per-request deciders).
   - SemaEngine trait (database verbs over live-set, GC-roots, event-log tables).
   - Plane envelopes and frame codec.

3. Hand-written trait impls (domain logic only):
   - `impl SignalEngine for SignalActor`: admission, validation, route minting.
   - `impl NexusEngine for Nexus`: the decide loop routing Deploy requests to
     planning work, Watch requests to subscription setup, etc.
   - `impl SemaEngine for Store`: the five database verbs over the three tables
     (live set, GC roots, event log) using sema-engine.

4. Simplified orchestration:
   - No hand-written Kameo actor supervision—the generic runner (once 1574/1581
     lands) owns the accept loop, frame transport, and Nexus loop.
   - Per-deployment jobs become NexusEngine side effects (RunEffect), not
     separate Kameo actors (or they remain as background Kameo actors invoked
     by effects, but the signal boundary stays clean).

### C.3 Concrete Adoption Steps

**Phase 1: Schema + Emission** (lojix repo + signal-lojix repo in parallel):

1. Write `lojix/src/schema/lib.schema` (NOTA) authored once, one schema file for
   all three planes (bootstrap all-in-one, like spirit):
   - Signal namespace: Request/Reply variants (Deploy, Pin, Unpin, Retire, Query,
     Watch, Unwatch and their success/rejection outcomes).
   - Nexus namespace: Work shape (DeploymentSubmission, SubscriptionRequest,
     etc.), Action shape (ActivateBuild, StartDeployment, CompleteWatch, etc.).
   - SEMA namespace: WriteInput shape (record generation facts, cache retention),
     ReadInput shape (query live set, query event log).

2. Land signal-lojix Cargo.toml + src/ with the `signal_channel!` declaration
   and typed records (Deploy, Pin, Pinned, DeployRejected, etc.). **No behavior.**

3. Run schema-rust-next emission at build.rs (per spirit's pattern using
   GenerationPlan::component_runtime_compatibility). Check in generated
   `src/schema/lib.rs` (rkyv, NOTA text, engine traits, plane envelopes).

**Phase 2: Engine Trait Implementation** (lojix daemon logic):

1. Write `src/engine.rs` (thin composer, no logic):
   - Create Engine struct holding SignalActor, Nexus, Store.
   - Route frames through Signal admission → Nexus execution → reply framing.
   - Wire lifecycle: Engine::start → NexusEngine::on_start → SemaEngine::on_start,
     Engine::stop in reverse order.

2. Write `src/signal.rs` (SignalEngine impl):
   - Admission: route/identifier minting, validation of Deploy/Pin/Watch/etc.
     variants.
   - Triage: branch on Input variant to decide if it's a request or subscription.
   - Reply framing: output conversion (Deployed, Pinned, DeployRejected, etc.).

3. Write `src/nexus.rs` (NexusEngine impl):
   - Decide loop: consume mail, route by Input variant.
   - Decider for Deploy: validate request, mint DeploymentIdentifier, emit
     PlanBuild effect or ActivateBuild effect; reply Deployed on success.
   - Decider for Query: read live set via sema-engine, reply Queried.
   - Decider for Watch: setup subscription via sema-engine, reply Watching.
   - Decider for Pin/Unpin/Retire: validate authorization, emit MutateLiveSet
     effect; reply Pinned/Unpinned/Retired.
   - Effects: PlanBuild (invoke nix-build), ActivateBuild (activate system),
     WriteLiveSetEntry (call sema-engine), StartContainer (systemd dbus), etc.

4. Write `src/store.rs` (SemaEngine impl):
   - Open `.sema` redb file via sema-engine at startup.
   - Register three table families: LiveSet (Generation), GCRoots (PathSymlink),
     EventLog (DeployEvent).
   - Implement apply/observe/etc. verbs over those tables via sema-engine.
   - **Correct**: sema-engine is the only database boundary, no raw redb calls.

**Phase 3: Wiring and Testing** (integration):

1. Replace hand-written Kameo actor supervision with the generic runner (once
   1574/1581 lands). Until then: keep RuntimeRoot but simplify it to spawning
   only background effect actors, not request-handling actors.

2. Write process-boundary tests (per spirit example): start real daemon, send real
   signal-lojix frames, verify event sequences over a real Unix socket.

3. Align signal-lojix with the three-layer model (per reports/designer/246 and
   248): contract-local operation verbs (Deploy, Pin, Watch) + daemon-internal
   Component Commands + sema-engine operation classification (Assert, Mutate,
   Retract, Subscribe).

### C.4 Why Lojix Should Adopt the Triad Shape

**Record 4sff** (Spirit Decision): "lojix should be built on the triad engine and
schema substrate now that those are stabilizing, the same schema-derived
component shape the other components are converging on, rather than remaining a
hand-written hack."

**Concrete gains**:

- **Type safety**: Every wire record, every Nexus decision point, every SEMA verb
  is generated from a single source (the schema). Impossible to have a mismatched
  Input variant and Reply type (compiler enforces it).
- **Auditability**: The Signal/Nexus/SEMA engine separation is structural, not
  policed by human review (type system proves it).
- **Reusability**: The runner (once 1574/1581) is written once; lojix (and every
  other component) uses the same accept loop and frame transport.
- **Observability**: Generated trace object names (SignalObjectName::Triaged,
  NexusObjectName::Entered, SemaObjectName::WriteApplied) provide typed trace
  events without hand-rolled string logging.
- **Maintenance**: Changes to the deploy protocol (new Pin/Unpin variants, new
  event types) are authored in one schema file; the Rust code regenerates
  automatically.

---

## D. Horizon-rs Current State ("Hack" Diagnosis)

### D.1 What Makes Horizon-rs a Hack

**Status**: CANON (active). Long-term target: parts may migrate into forge's
in-process actors.

**Current architecture** (from ARCHITECTURE.md + source):

- **Purpose**: Projection library—Rust types and helper code for walking cluster
  proposals to compute NixOS rebuild inputs.
- **Role**: Linked in-process by lojix-cli's deploy path (not a daemon, not a
  component, not a triad).
- **Structure**: `lib/src/` Rust lib (projection code) + `cli/` small CLI (ad-hoc
  projection calling the library).

**The "hack" specifics**:

1. **In-process only, not a component**: horizon-rs is a library dependency, not a
   daemon with a socket. It has no wire contract, no Signal envelope, no Nexus
   mail keeper, no SEMA database boundary. It is imported and called as a Rust
   function.

2. **Hand-rolled projection logic**: The projection from cluster proposals to
   derived facts (node domain, LAN CIDR, router SSID, resolver addresses) lives
   in hand-written Rust methods on the proposal types, not in a schema-derived
   engine. Example: `view/` module contains `impl ClusterProposal { fn domain()
   { ... } }` and similar projections.

3. **NOTA discipline inconsistency**: horizon-rs's CLI accepts NOTA input for
   cluster proposals but emits Rust types internally. The `lib/` crate owns the
   projection algorithms; the boundary between NOTA text and typed structure is
   hand-managed (nota-codec import + manual `encode`/`decode` calls), not
   generated.

4. **No durable state, no database**: horizon-rs reads a cluster proposal NOTA
   file once, projects it, and returns the view. No redb, no sema-engine, no
   durable tables. The "hack" label refers to the **one-off library pattern**
   rather than component-shaped architecture.

5. **Embedded in the deploy path**: lojix-cli links horizon-rs directly and calls
   it as `horizon_lib::view::View::from_proposal()`. It is not a separate
   component consuming/producing signal-frame messages.

### D.2 Regular Component Shape: What Would Be Required

If horizon-rs were to become a **schema-derived triad component**:

1. **Wire contract** (signal-horizon):
   - Input: ProjectClusterProposal(ClusterProposal)—read a cluster proposal,
     compute view.
   - Output: ProjectionReady(View) or ProjectionRejected(ValidationError).
   - SEMA: no database (read-only projection).
   - Nexus: one decision rule—validate proposal shape, call projection, return
     view.
   - Signal: admission, triage, reply.

2. **Schema file** (horizon.schema):
   - Signal namespace: ProjectClusterProposal verb, ProjectionReady/
     ProjectionRejected replies.
   - Nexus namespace: ProjectionWork, ProjectionAction.
   - SEMA namespace: empty (no database operations).

3. **Daemon scaffolding** (horizon-daemon binary):
   - Bind a Unix socket (or inherit it via systemd socket activation).
   - Call schema-rust-next-emitted engines.
   - Accept signal-horizon frames.
   - Invoke the projection library as a Nexus effect.
   - Return typed ProjectionReady reply.

4. **Runtime integration** (lojix consuming it):
   - lojix would NOT link horizon-rs directly.
   - Instead: lojix sends a ProjectClusterProposal request to the horizon-daemon
     Unix socket.
   - horizon-daemon replies with ProjectionReady(View).
   - lojix continues with the view in hand.

**Why this would help**:

- **Separation of concerns**: horizon's projection algorithms live in one place
  (horizon-daemon); lojix doesn't need to know the projection logic, only the
  wire contract.
- **Auditability**: the View type is schema-defined and wire-encoded; no risk of
  stale Views or mismatched field sets.
- **Future schema evolution**: if the cluster proposal schema changes, the
  horizon-daemon recompiles and handles the new shape; lojix continues using the
  same ProjectClusterProposal message.
- **Testability**: horizon-daemon can be tested in isolation (start daemon, send
  real NOTA cluster proposals over the socket, verify View).

### D.3 Why Horizon Remains a Library (Current Decision)

**From ARCHITECTURE.md**: "Long-term: parts may migrate into forge's in-process
actors when the forge family unifies."

**Current decision**: horizon-rs is **not** becoming a triad component in the
rewrite. The "horizon-leaner-shape" branch (active-repositories.md:124) refactors
the proposal boundary and pan-horizon constants, but horizon-rs stays in-library.

Reasons (inferred from the active work):

- **Frequency of use**: lojix calls the projection on every deploy request. A
  Unix-socket round-trip for every projection would add latency. Linking the
  library is faster.
- **Build-time derivation**: The eventual plan is for horizon to be fully
  schema-derived (the proposal shapes themselves authored in schema, the
  projection logic generated). Until that generative move, keeping it as a library
  and calling it in-process is a pragmatic realization step.
- **Forge family convergence**: The long-term plan is for horizon projection to
  be absorbed into the broader forge build-system unification, where it may
  become a different kind of component shape (not a triad daemon, but an
  in-process module in a larger build-orchestration engine).

### D.4 Horizon-rs in the Rewrite Arc (horizon-leaner-shape)

The current active work (active-repositories.md:124-136):

- **Pan-horizon constants** (criomos-horizon-config repo, new): a split-out
  constants repo that horizon-rs consumes. Contains: internal DNS suffix
  (`criome`), public DNS suffix (`criome.net`), LAN address pool, reserved
  subdomain labels.
- **Cleaner proposal boundary** (horizon-leaner-shape branch): horizon-rs uses
  service variants instead of positional booleans (good discipline). Proposal
  shapes are tighter (audit report 207).
- **Lean horizon view** (horizon-leaner-shape): the projection code is simplified
  to accept pan-horizon config + cluster proposal, emit a clean view for deploy.

**Lojix integration** (horizon-leaner-shape): lojix daemon's RuntimeRoot loads
horizon config (from criomos-horizon-config) and calls the projection library per
deploy request. horizon-rs stays in-library; lojix is the only (current) consumer.

---

## E. The Two Deploy Stacks

### E.1 Stack A — Production Today

**Status**: Running on every node.

**Repos** (main branches in canonical `/git/github.com/LiGoldragon/...` checkouts):

- `horizon-rs` (main)
- `lojix-cli` (main)—the current monolithic orchestrator
- `CriomOS` (main)
- `CriomOS-home` (main)
- `CriomOS-lib` (main)
- `goldragon` (main)

**Flow**:

1. Operator uses `lojix-cli` command (thin CLI + monolithic orchestrator in one
   repo).
2. lojix-cli projects `horizon-rs/main` over `goldragon/datom.nota` (cluster
   proposal).
3. lojix-cli writes the horizon, system, deployment flake inputs into CriomOS at
   deploy time.
4. CriomOS (via Nix) materializes the configuration, activates on the node.

**Database**: CriomOS flake locks pin `lojix-cli` at `4c66b8a6fa55` (frozen).

**Fixes**: Production edits go to `main` in the canonical checkouts.

### E.2 Stack B — Lean Rewrite (Smoke-Built, Not Yet Deployed)

**Status**: In-development on feature branch `horizon-leaner-shape` (branched from
earlier `horizon-re-engineering`). Smoke-built end-to-end through `prometheus`;
has **not** been cut over to any production node.

**Repos** (horizon-leaner-shape branches in worktrees under `~/wt/github.com/LiGoldragon/<repo>/horizon-leaner-shape/`):

- `horizon-rs` (horizon-leaner-shape)
- `lojix` (new daemon + thin CLI, horizon-leaner-shape)
- `signal-lojix` (new wire contract, horizon-leaner-shape)
- `criomos-horizon-config` (new constants repo, horizon-leaner-shape)
- `CriomOS` (horizon-leaner-shape)
- `CriomOS-home` (horizon-leaner-shape)
- `CriomOS-lib` (horizon-leaner-shape)
- `goldragon` (horizon-leaner-shape)

**Flow**:

1. Operator uses `lojix` thin CLI client (new binary, part of `lojix` daemon crate).
2. lojix CLI connects to `lojix-daemon` Unix socket, sends `signal-lojix` frame.
3. lojix-daemon (long-lived orchestrator):
   - Loads `criomos-horizon-config` (pan-horizon constants).
   - Projects `horizon-rs` over the cluster proposal.
   - Plans deploy: invoke nix commands, build closure, activate.
   - Records events: BuildRealized, CachePublished, ActivationSucceeded.
   - Replies with DeploymentIdentifier; emits events over subscription stream.
4. lojix daemon writes system/deployment flake inputs into CriomOS (same flow as
   Stack A, but triggered from daemon state, not monolithic CLI invocation).

**Database**: lojix-daemon owns one `.sema` redb file (via sema-engine) recording
the live generation set, GC roots, event log, and container-lifecycle observations.

**Fixes**: Rewrite edits go to `horizon-leaner-shape` in the worktrees.

### E.3 Cutover Discipline

**From active-repositories.md §"Cutover discipline"**:

- Each replacement repo has a documented "replaces" target.
- Build replacement to feature parity, run both in parallel, switch producers/
  consumers one at a time, then retire the original.
- **Do not fold one stack into the other piecemeal.** Schemas have diverged.
- Cutover happens as a coordinated multi-repo merge **after the rewrite reaches
  feature parity** (Signal 1567, work tracked under horizon-leaner-shape arc).

**Status**: Feature parity not yet achieved. lojix-cli (Stack A) is the canonical
production path until CriomOS migrates to consume Stack B lojix-daemon's
projection.

---

## F. For the Orchestrator — Load-Bearing Facts

### F.1 The Five Essential Truths

1. **The triad engine separation is structural, not policed.** Schema-rust-next
   emits three engine traits (SignalEngine, NexusEngine, SemaEngine) whose plane
   envelopes make cross-engine calls a compile-time type error. The strong half
   (Nexus cannot touch SEMA, Signal cannot touch Nexus) is already proven by the
   type system (spirit pilot ships a `compile_fail` doctest). This is the
   foundation of the stack rewrite.

2. **Spirit is the reference component, but broken on the sema-engine boundary.**
   Spirit pilot implements the full triad shape correctly and runs in production
   test mode. However, it opens `redb::Database` directly instead of using
   sema-engine—a violation of record 2563 (psyche correction). This must be fixed
   (bead primary-w42y, sema-engine adoption) before promotion to production. The
   architecture is sound; the implementation is incomplete.

3. **Lojix is hand-written Kameo orchestration, not a triad component.** Current
   horizon-leaner-shape lojix uses sema-engine (correct database boundary) and
   signal-core (correct wire kernel), but skips the schema-derived Signal/Nexus/
   SEMA engines. It hand-writes its own actor supervision instead of using the
   generated triad pattern. Adoption is straightforward (write one .schema file,
   implement three trait impls, remove hand-written actor choreography), and
   necessary (record 4sff: lojix should adopt the triad substrate).

4. **Horizon-rs is a library projection, not a component, and will stay that way.**
   horizon-rs reads cluster proposals and emits views (NodeDomain, LAN CIDR,
   router SSID, etc.). It is not a daemon and is not schema-derived by design:
   it's a realization step toward the eventual forge-family unification. The
   "hack" label refers to the in-process library pattern, not a violation. The
   active rewrite (horizon-leaner-shape) cleans up the proposal boundary and
   extracts pan-horizon constants; this is good hygiene within the library design,
   not a move toward componentization.

5. **The runner is the missing piece that makes the constraint structural.** The
   generic `TriadComponent::serve()` function (ratified 1574/1581, not yet built)
   owns the accept loop, frame transport, and Nexus loop once, for all
   components. Until it exists, each daemon (spirit, and future lojix) hand-writes
   this scaffolding. Once the runner lands, component authors write **only** the
   three engine trait impls and the data nouns; the audit becomes vacuous by
   construction.

### F.2 The Three Open Questions

1. **Sema-engine adoption in the spirit pilot** (bead primary-w42y): Replace raw
   redb calls with sema-engine API. Straightforward code edit; no psyche decision.
   This unblocks spirit's promotion to production.

2. **RustItem token model for schema-rust-next** (ratified 1576/1584): Replace
   504 hand-indented `self.line()` calls in the impl emission layer with a typed
   token data model. Operator work; refactoring, not new semantics.

3. **The runner extraction** (ratified 1574/1581): Extract spirit's hand-written
   accept loop + transport + Nexus loop into `triad-runtime::TriadComponent::serve()`.
   Operator work; unblocks all subsequent components (lojix, future daemons) from
   writing transport plumbing.

### F.3 Next Steps for Lojix Adoption

1. **Write lojix.schema** (NOTA, authored once): Signal (Deploy/Pin/Watch/etc.),
   Nexus (Work/Action shapes), SEMA (table definitions for live set / GC roots /
   event log).

2. **Land signal-lojix Cargo + src** (pure contract, no behavior): type records,
   signal_channel! declaration, rkyv/NOTA codecs.

3. **Run schema-rust-next emission** (build.rs): lojix/src/schema/lib.rs
   generated, checked in.

4. **Implement three engine traits** (lojix domain code): SignalEngine (admission,
   validation), NexusEngine (decide loop, deploy planning/activation), SemaEngine
   (live set / GC roots / event log tables via sema-engine).

5. **Replace hand-written Kameo supervision** (once runner lands): use generic
   TriadComponent::serve().

6. **Test with process-boundary witnesses**: real daemon, real signal-lojix frames,
   real event sequences.

---

## Verification and Citations

**Schema-rust-next emission**: `schema-rust-next/ARCHITECTURE.md` lines 24-122
(input contract, emission targets, wire contract definition, builder patterns,
cross-crate imports).

**Spirit pilot engine separation**: `spirit/src/engine.rs` lines 26-128
(Engine/SignalActor/SignalAccepted/SignalRejected structure);
`spirit/src/nexus.rs` lines 222-268 (decide loop);
`spirit/src/store.rs` lines 194-332 (SEMA operations). Audit report 501 verifies
strict separation holds.

**Sema-engine boundary violation**: `spirit/src/store.rs` lines 156-174 opens
redb directly (Database::open, Database::create) instead of via sema-engine.
Report 63 (2026-06-04) audits the violation; bead primary-w42y tracks remediation.

**Lojix structure** (horizon-leaner-shape): `lojix/src/lib.rs` (47 lines,
documented); `lojix/src/runtime.rs` (150+ lines, RuntimeRoot actor spawning);
`lojix/Cargo.toml` (horizon-leaner-shape branch) shows dependencies: signal-core,
signal-lojix, sema-engine, sema, horizon-lib, nota-codec, kameo, tokio.

**Horizon-rs**: `horizon-rs/ARCHITECTURE.md` (in-process library, not a daemon);
`lib/src/view/` (hand-written projection code); `cli/` (small CLI wrapper).
active-repositories.md:98-99 lists it as "Adjacent Active Work," with long-term
convergence into forge.

**Signal 4sff** (lojix adoption intent): cited in
`71-intent-architecture-and-stack-rewrite-study-2026-06-04/0-frame-and-method.md`
line 63.

**Signal 4v45** (horizon-rs hack clarification): same source, line 65.

**Signal 2560** (strict engine separation): audit 501, psyche record 2560 (VeryHigh).

**Signal 2563** (sema-engine boundary): audit 63, psyche record 2563 (Correction High).

**Records 1574/1581** (runner extraction): active-repositories.md truth pins;
referenced in 501 design-questions and schema-rust-next ARCHITECTURE.

**Records 1576/1584** (RustItem token model): designer/500 entry 5 (overview).

