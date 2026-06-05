---
title: 528 — Per-repo INTENT.md drafts + landing plan
role: designer
variant: Design
date: 2026-06-05
topics: [intent, repo-intent, schema-next, schema-rust-next, spirit, mind, router, message, contract-repos]
description: |
  Drafts produced by the intent-centralization subagent pass (psyche
  directive: straighten up the INTENT.md situation). Distilled INTENT.md
  for the 3 over-captured core repos, drafted INTENT.md for 3 missing
  daemons, a reusable contract-repo template + examples, and a tail plan
  for the ~55 missing files. Pending the psyche/operator landing decision
  (code-repo main is operator-owned). The training-file centrality edits
  (AGENTS.md, ESSENCE.md, skills.nota, intent-log.md) already landed.
---

# 528 — Per-repo INTENT.md drafts + landing plan

These are DRAFTS, not yet landed. Code-repo `main` is operator-owned;
landing is a coordinated decision (see §Landing). The training-file
centrality half of the psyche directive is already applied to AGENTS.md,
ESSENCE.md, skills.nota, and intent-log.md.

## Distilled — the 3 over-captured core INTENT.md files

### schema-next (currently 357 lines → distilled)

**For:** Replacement schema engine that consumes NOTA source, runs position-aware macros, and emits typed assembled schema.

**Moves out to `ARCHITECTURE.md`:** Current implementation details: MacroRegistry dispatch, NotaDocument parsing pipeline, StructureHeader witness, SchemaSource codec shapes (SourceImports, SourceRootEnum, SourceNamespace, SourceDeclarationValue, SourceStructBody, SourceEnumBody, SourceVariantSignature), RawSchemaFile reading mode for core schema inspection, Asschema compatibility surface for existing downstream consumers, the bootstrap macro-library artifact workflow, and per-position macro-context recording for diagnostics.

**Distilled `INTENT.md` draft:**

```markdown
# INTENT — schema-next

`schema-next` is the schema macro engine and typed assembled schema data model for the schema-derived stack.

Load-bearing constraints:

*Macros are position-aware structural matching over NOTA objects.* The delimiter shape, contained object count, and qualification predicates select macro variants that lower objects into assembled schema. A macro invocation is data—a tagged/payload-carrying schema node at a macro position, represented as data before execution so tables can be serialized, deserialized, tested, and eventually pre-assembled.

*Schema files read as a known root struct.* The top-level schema shape supplies the root type name and field positions; inner variable vectors contain macro objects that expand by position into assembled schema.

*Reserved scalars belong in assembled schema, not Rust.* `String`, `Integer`, `Boolean`, and `Path` lower to scalar `TypeReference` variants; `Plain(Name)` is reserved for declared schema types and importable names. Scalar names cannot be re-declared.

*Cross-crate schema imports resolve through Cargo-exposed dependency directories.* A schema import source uses single-colon path syntax `crate:module:Type`; `ImportResolver` loads the dependency's schema module, confirms the name exists as either a namespace type or root enum, and records the resolved import.

*NOTA owns raw structure; Schema owns type-name vocabulary.* Square brackets are raw vector structure, not `Vec` type syntax. Schema type-reference objects include `(Vec T)`, `(Map (K V))`, and `(Optional T)`, lowering to `Vector`, `Map`, and `Optional` in assembled schema. Parentheses are composite-reference and macro-call form.

*Assembled schema namespace entries are visibility-tagged.* The canonical NOTA shape is `(Public Name Value)` or `(Private Name Value)`; top-level declarations lower to public, inline PascalCase declarations lower to private.

*Enum bodies are homogeneous vectors of variant-signature objects.* A unit variant is a bare PascalCase symbol; a data-carrying variant is `(Variant PayloadType)`. Bracket members remain one variant-signature object.

*Root input/output headers may list exported variant names directly.* When a bare header entry resolves to a namespace declaration, the variant carries the same-named payload type. Inline declarations are inserted into the exported namespace before the root enum is assembled.

*Authored schema is its own typed value before assembled schema.* `SchemaSource` reads `.schema` documents into source-language data (imports, input/output enums, namespace declarations) and writes canonical `.schema` text projections back out. This source codec is separate from raw NOTA parsing and separate from `Asschema` serialization.

*The structured macro-node mechanism belongs at the NOTA layer.* nota-next owns structural macro-node codec machinery; schema-next owns schema positions and handlers. Built-in schema macros load through a serialized macro-library artifact, with hand-authored source kept as a freshness-checked bootstrap source.

*Asschema is now a compatibility projection.* The target pipeline is: authored `.schema` deserializes into Rust datatypes that fully define the schema, that typed value is rkyv-serializable, and Rust code is lowered from that typed value. The current `Asschema` type, `.asschema` text, and `.asschema.rkyv` binary surfaces remain only until source-node types and Rust emission finish migration.

This repository owns the schema macro engine and the ordered assembled schema data model. It does not emit Rust source code.
```

### schema-rust-next (currently 300 lines → distilled)

**For:** Replacement Rust emission layer that consumes typed schema data and emits Rust source code as a separate step before any Rust macro ergonomics.

**Moves out to `ARCHITECTURE.md`:** Implementation mechanics: RustEmitter engine, RustModule data model carrying scalar aliases/imports/declarations/root enums, RustCode rendered output, GeneratedFile artifact naming, RustModulePath single-colon to crate-local mapping, RustEmissionTarget variants (WireContract/SignalRuntime/NexusRuntime/SemaRuntime/ComponentRuntime), RustEmissionOptions nota_surface configuration, GenerationPlan crate/modules/targets/dependencies, the compatibility Asschema projection path and artifact handoff methods (emit_file_from_artifact, emit_file_from_nota_path, emit_file_from_binary_path), visibility-tagged namespace entry projection, tuple newtype/struct vs alias distinction in emission, typed bridge methods like from_nota_block and to_nota.

**Distilled `INTENT.md` draft:**

```markdown
# INTENT — schema-rust-next

`schema-rust-next` emits Rust interface source from typed schema data and powers the shared build-driver orchestrator for generated schema modules.

Load-bearing constraints:

*Rust emission is a separate step from Rust macros.* Schema generates Rust code first; macros are a later or separate consumption surface. Generated Rust code is emitted into the consumer crate source tree under `src/schema/`, not hidden in `OUT_DIR`. Source-visible generated interfaces are reviewable and can become committed or freshness-checked build artifacts.

*Schema-generated objects are the Rust nouns that carry behavior.* Actor input and output roots become enums; runtime engines implement generated Nexus traits with one method per reaction variant on data-bearing objects, not free helper functions.

*Cross-crate schema imports preserve type ownership.* A consumer schema that imports `crate:module:Type` emits a local Rust alias to the dependency crate's generated type instead of re-declaring. The imported crate owns the type definition; the consumer only uses the alias.

*Plane payload names are scoped by emitted namespaces.* Generated public surface reads `signal::Input`, `nexus::Input`, `sema::WriteInput`, and `sema::ReadInput` inside their respective planes, not redundant plane ancestry at every use site.

*Collection references emit standard Rust collections with deterministic rkyv/NOTA round-trips.* `(Vec T)` emits `Vec<T>`, `(Map (K V))` emits `std::collections::BTreeMap<K, V>` (ordered), and `(Optional T)` emits `Option<T>`.

*The shared generation driver consumes `SchemaSource` at the component build boundary.* Per-crate `GenerationDriver` owns the load/lower/emit/freshness sequence so component `build.rs` files do not hand-roll it. Runtime schemas import contract roots through Cargo-exposed dependency schema directories.

*NOTA text projection is opted into per-emission target.* Generated binaries always carry rkyv support. `nota_next::NotaDecode` and `nota_next::NotaEncode` are feature-gated (`nota-text`) or omitted for binary-only daemon consumers. A binary-only daemon crate builds dependencies with `default-features = false` and carries no `nota_next` in its dependency closure.

*Asschema aliases and newtypes are separate data shapes.* Bare bindings lower to `TypeDeclaration::Alias` and emit as Rust `type` aliases. Brace-body declarations with exactly one field lower to `TypeDeclaration::Newtype` and emit as tuple newtypes.

*Authored schema macro syntax is not an emitter input.* Tests lower real `.schema` fixtures into typed `Asschema` values before comparing generated Rust. No assembled-schema text fixture is accepted as a normal input.

This repository owns the Rust code generation step and the shared build-driver orchestrator. It does not define schema semantics.
```

### spirit (currently 259 lines → distilled)

**For:** Public runnable pilot proving a schema-derived component can be built and operated with Signal/Nexus/SEMA planes as a real CLI and daemon pair.

**Moves out to `ARCHITECTURE.md`:** Implementation details: DaemonCommand startup noun from environment, Configuration binary rkyv structure, daemon main as thin entrypoint calling library nouns, MailLedger lifecycle event recording, MailLedgerEvent/SentMail/ProcessedMail/OriginRoute noun details, Store redb handle and sema-engine integration, the generated `/src/schema/{signal,nexus,sema}.rs` artifact paths and freshness checking in `build.rs`, generated engine trait lifecycle hooks on_start/on_stop, the three-plane startup order (SEMA→Nexus→Signal for start, reversed for stop), trace build packages vs normal lean packages via flakes, the `testing-trace` feature configuration, trace socket listener and Unix domain socket mechanics, generic typed trace client from triad-runtime, the strict NOTA brace semantics in plane schemas, derived-member field shorthand like `Topics *`, and the comparison of checked-in generated Rust with freshly generated artifacts.

**Distilled `INTENT.md` draft:**

```markdown
# INTENT — spirit

`spirit` proves a running Spirit-like component can be built from schema-derived interfaces. It is intentionally separate from production `spirit`/`persona-spirit` so operators can iterate without disturbing the deployed substrate.

Load-bearing constraints:

*CLI input and output are NOTA when the `nota-text` feature is enabled.* Component/process communication is always binary rkyv. Generated schema datatypes always carry rkyv support; NOTA encode/decode is an opt-in text-client surface, not a daemon requirement. The daemon binary must not depend on `nota-next`; the CLI crate enables `nota-text`. Tests run `cargo tree --edges normal --no-default-features` and assert `nota-next` is absent from the binary, while the text surface must contain it.

*Rust data types are generated from crate-local `schema/{signal,nexus,sema}.schema` plane schemas.* Authored schema source is a typed artifact before assembly. The shared generation driver reads each plane schema into `SchemaSource`, round-trips canonical source text through `SchemaSourceArtifact`, lowers from that typed source value, and compares only the generated Rust artifacts with checked-in files. The source language has an in/out codec instead of being a one-way parser.

*Schema namespaces are strict NOTA key-value maps.* Braces are key-value pairs. A namespace entry is a pair like `Topic String`, `Entry { Topics * Kind * ... }`, or `Kind [...]`. Struct fields are key-value pairs; `Topics *` reuses the same type, while `kind (Optional Kind)` binds a field to a different reference. Enum bodies are square-bracket lists of exported object names. Bare bindings lower to aliases and direct enum payloads, not wrapper structs.

*The three runtime centers are concrete objects.* `SignalActor` handles admission, `Nexus` is the mail keeper and translator owning the store and ledger, and `Store` is the durable SEMA plane over `sema-engine`. `Engine` composes them and owns no SEMA state. Generated plane namespaces expose `signal::Input`/`signal::Output`, `nexus::Work`/`nexus::Action`, and `sema::WriteInput`/`sema::WriteOutput`/`sema::ReadInput`/`sema::ReadOutput`.

*Signal admission is explicit.* `SignalActor::admit` mints the origin route, validates generated `Input`, and creates `SignalAccepted`. Invalid input returns `Output::Rejected(SignalRejection { validation_error, database_marker })` where `ValidationError` is generated from schema; the runtime does not use a hand-written rejection enum.

*Nexus is the recursive runner payload keeper.* Signal triage produces a generated `nexus::Nexus<nexus::Work>` envelope; `triad-runtime::Runner` owns the continuation budget and repeated dispatch. Hand-written `Nexus` implements one decision step, SEMA write/read hooks, and the effect hook.

*SEMA is durable.* `Store` maps generated SEMA roots onto `sema-engine` identified-record operations over a `.sema` file. Each `Record` calls `Engine::assert_identified`, each `Remove` calls `Engine::retract_identified`, and `Observe`/`Lookup`/`Count` read through `Engine::match_identified`. SEMA replies carry generated `DatabaseMarker` values so Signal replies report the state commit sequence and digest.

*The daemon's single argument is a path to a binary rkyv `Configuration` object.* Text-facing launchers may create that file, but the daemon startup path only decodes binary state.

*Trace is optional runtime instrumentation.* The `testing-trace` surface observes Signal/Nexus/SEMA calls through generated trait hooks without affecting production binary behavior. Trace events carry schema-generated typed `ObjectName`, not free strings. Spirit owns the typed `TraceEvent` over plane-local object names; `triad-runtime` owns the reusable log, frame mechanics, and client-side collection.

Load-bearing proof: the real process boundary is tested, not only in-memory function calls. Trace events cross the Signal admission, `SignalEngine`, `NexusEngine`, and `SemaEngine` boundary, proving actor/interface use instead of source-string presence.
```

## Drafted — missing daemons

### mind

**For:** Central Persona state component for orchestration, work memory, and typed graph semantics.

```markdown
# INTENT — mind

`mind` owns Persona's central workspace state: work items, typed Thought and Relation
records, notes, dependencies, decisions, aliases, event history, subscriptions, channel
choreography policy, and ready/blocked views. Lock files are transitional; `mind`
replaces them.

The authority principle is load-bearing: `mind` is the authority root of the Persona
control plane. It *receives inbound* observations (Assert, Match, Subscribe) from peers
and *issues outbound* orders (Mutate, Retract) to downstream components. Authority
direction is "observe up-tree, order down-tree": mind subscribes to router/harness/
orchestrate events and decides; then issues Mutate orders (ChannelGrant, ChannelExtend,
ChannelRetract, AdjudicationDeny) that peer components obey and confirm.

The CLI is a thin client boundary. The daemon owns `MindRoot` for its process lifetime.
Requests enter through `MindEnvelope` (caller identity + typed `MindRequest`). The
database is workspace-local `mind.redb` opened only by `StoreKernel`. Typed Thought/
Relation graph records write through `sema-engine` Assert on registered table families.
Graph IDs are compact sequence-derived tokens minted from engine snapshot; they are
not content hashes, timestamps, or embedded type prefixes. Queries are read-only;
writes append typed events. Work/memory mutations replace the typed memory_graph
snapshot in `mind.redb` before success replies. Typed graph subscriptions register
through `sema-engine` Subscribe and persist durable Persona-specific filters.

Key constraints: the CLI accepts exactly one NOTA request and prints exactly one
reply. All public operations enter as one MindEnvelope. Caller identity, time, event
sequence, operation IDs, and display IDs are minted by infrastructure/store actors,
not by request payloads. State-bearing phases are actors or reducers owned by actors—
no shared Arc<Mutex<T>>. Typed Thought and Relation records are immutable; correction
is a new record plus a relation like Supersedes. Durable truth is mind.redb; lock
files are outside this implementation, and BEADS is import/history only.
```

### router

**For:** Delivery reducer and message routing policy enforcement for Persona.

```markdown
# INTENT — router

`router` owns routing policy, delivery state, and authorized-channel authority. It does
not own OS backends, terminal byte transport, terminal lifecycle, or contract definitions.
Delivery decisions are local: router checks channel authorization, queues pending deliveries,
attempts delivery through harness, commits results, and emits subscription deltas.

The authority principle mirrors mind: `router` *receives inbound* channel-state mutations
from higher authority (today from `mind`: ChannelGrant, ChannelExtend, ChannelRetract,
AdjudicationDeny) and *issues outbound* observations (AdjudicationRequest for missed
channels, observation queries back to introspect). The router obeys, then confirms—authority
lives upstream. Routing is the router's decision: a typed message fact (Assert-shaped)
Enters the system; the router decides delivery based on channel state. A message without
an authorized channel parks for mind adjudication.

The CLI is a thin client; the daemon owns `RouterRuntime` for its process lifetime.
Requests enter as length-prefixed Signal frames; replies are typed `RouterReply` records.
Router-owned durable state is `router.redb`: accepted messages, channels, adjudication-
pending records, delivery attempts, and results. Message acceptance commits before delivery
attempt. Delivery results update state before post-delivery subscription events. Every
accepted message carries typed `IngressContext` from the accepted socket relation.
Origin is provenance, not an auth proof.

Key constraints: routing reacts to pushed events (no polling). Authorization is channel-
table authorization plus mind adjudication for misses. One-shot channels authorize
exactly one message, then retire. Retracted and expired time-bound channels cannot
authorize. A message without an active channel never reaches HarnessDelivery. Delivery
attempts produce typed observable state: delivered, deferred, or rejected. Durable effects
commit before externally visible delivery events. Router does not depend on terminal crates
directly; terminal delivery stays behind harness.
```

### message

**For:** Engine message ingress: the message CLI and supervised message-daemon for owner-writable socket binding.

```markdown
# INTENT — message

`message` owns two binaries: the `message` CLI (thin client) and `message-daemon`
(supervised first-stack component). Neither carries a durable message ledger. Both are
stateless boundary surfaces. Routing policy, delivery state, and channel authority
remain in router.

The daemon owns one Kameo root actor and binds `message.sock` (mode 0660, engine-owner
group). It reads typed `MessageDaemonConfiguration` from argv via `nota-config`—socket
paths, socket modes, owner identity, supervision socket. The daemon stamps
`MessageSubmission` frames with configured owner identity, SO_PEERCRED-derived origin,
and ingress timestamp; then forwards `StampedMessageSubmission` frames to router's
internal socket (`router.sock`, 0600). Provenance is typed, minted by the daemon, never
infered from uid or accepted from payload.

The CLI accepts exactly one NOTA `Send` or `Inbox` record, projects to a length-prefixed
Signal frame, sends to `message.sock`, reads one reply frame, prints the NOTA reply.
Request/reply matching is frame-level: every request carries an ExchangeIdentifier, and
every reply echoes it.

Key constraints: caller identity is not accepted from model or CLI payload. The daemon
requires a typed configuration on argv; it exits if missing or malformed. The daemon
applies configured socket mode before accepting client traffic. CLI and daemon outbound
traffic are length-prefixed rkyv Signal frames. The component depends on stable Persona
Kameo lifecycle reference. Graceful supervision stop releases the socket and rejects later
ingress. Production daemon reads no environment variables for control-plane configuration.
Mismatched Signal verb/payload pairs are rejected as typed RequestRejectionReason.
```

## Contract repos — reusable template

```markdown
# INTENT — [COMPONENT-NAME] Signal Contract

*The wire vocabulary contract for [COMPONENT-NAME]. Defines the [ordinary/owner-only] typed
request/reply channel that [primary peer] uses to [verb phrase of domain action].
Companion to `ARCHITECTURE.md` and `Cargo.toml`. Maintenance: `primary/skills/repo-intent.md`.*

## Repo-scope only

This file carries only the intent that is FOR this `signal-[component]` contract.
Workspace-shape intent stays in the primary workspace `primary/INTENT.md`.
Component daemon intent stays in `[component]/INTENT.md`.

## Why this repo exists

`signal-[component]` is the **[ordinary/owner-only] peer-callable wire contract** for the `[component]`
daemon. It carries the [brief description of vocabulary: "vocabulary for X operations", "policy
configuration", "observation queries", "lifecycle orders", etc.]. 

[For owner-signal-*:] Owner-only authority and policy surface. Ordinary peer operations stay in
`signal-[component]`; runtime actors, sockets, storage, and decision logic live in `[component]`.

[For meta-signal-*:] Owner-only meta-signal policy and authority vocabulary. Ordinary peer
traffic stays in `signal-[component]`; daemon-internal state lives in `[component]`.

## The channel shape

The [relation name] channel carries:

- **Requests:** [list operation root verbs: `Submit`, `Query`, `Configure`, etc.] — [one sentence per operation family if needed]
- **Replies:** [Closed enumeration of success/failure/rejection replies corresponding to request kinds]
- **Observations** (if applicable): [Domain-specific observer tap vocabulary]

The wire vocabulary is contract-local — [e.g. "the daemon lowers these public operations into
component-local commands; Sema classification happens at observation time, not on the wire"].

## Channels are closed, boundaries are named

- Wire enums are closed. No `Unknown` escape hatch.
- Request payloads do not mint [list authority-minted fields: timestamp, ID, sequence, sender, etc.].
- [Component] mints [timestamp/ID/etc.] at the daemon; request records accept [submitted values] only.
- No stringly-typed dispatch. Status fields are typed closed enums.

## Wire vocabulary discipline

Per `primary/skills/contract-repo.md` §"Public contracts use contract-local operation verbs":

- Operation roots are domain verbs in verb form: `Submit`, `Query`, `Configure`, `Observe`, `Register`,
  `Start`, `Stop`, not Sema class words.
- Reply success variants are past-tense matching the operation: `Submit` → `Submitted`;
  `Query` → `Queried`; `Configure` → `Configured`.
- Reply rejections are `*Rejected` carrying a typed closed-enum reason.
- Payload record names are the domain nouns the operation carries: `Message`, `Configuration`,
  `Registration`, `Query`, not `Request`, `Data`, or generic containers.

## Constraints

- This crate carries only typed wire vocabulary, NOTA codecs, and round-trip witnesses.
- No runtime code: no actors, no tokio, no socket binding, no redb, no Persona policy logic.
- Contract types derive NOTA in this crate. Clients do not carry shadow types that re-derive
  the text surface.
- Every operation and reply variant round-trips through both rkyv frames and NOTA text;
  witnesses live in `tests/round_trip.rs` and `examples/canonical.nota`.
- Wire dependency pins use named branches or tags, not raw revision hashes (`git = "..."` with
  a branch, or a crates.io version).

## Three-layer model

Layer 1 (this crate): contract operations on the wire (domain verbs like `Submit`, `Query`).
Layer 2 (daemon): component-local typed commands that the daemon executes.
Layer 3 (observation): payloadless Sema class labels for cross-component introspection.

The contract names the public action at the boundary; the daemon decides what internal work
and Sema class label each action maps to. Sema classification never appears on the wire.

## Code map

```text
src/lib.rs              — payload records, NOTA codecs, and signal_channel! invocation
examples/canonical.nota — one canonical NOTA example per operation/reply variant
tests/round_trip.rs     — rkyv frame and NOTA round-trip witnesses per variant
```

## Non-ownership

This crate does not own:

- daemon runtime, actors, or component lifecycle;
- [component].redb or any storage tables;
- socket binding, transport, or version handshake policy;
- [list daemon-specific concerns: policy logic, authorization, reducers, etc.];
- NOTA projection policy or surface (CLI formatting, audit wrapping, Nexus composition).

## See also

- `ARCHITECTURE.md` — detailed channel shape, per-operation vocabulary, and closed-enum discipline.
- `../[component]/INTENT.md` — daemon-side intent (schema-driven planes, actors, state).
- `../owner-signal-[component]/INTENT.md` — owner-only sibling contract (if applicable).
- `primary/skills/contract-repo.md` — contract repo discipline and naming rules.
- `primary/skills/component-triad.md` — repo triad structure and wire layers.
```

### Filled examples

#### signal-mind

```markdown
# INTENT — signal-mind

*The wire vocabulary contract for Persona's central mind. Defines the typed request/reply
channel that the `mind` CLI and external components use to submit work-graph operations,
query typed thoughts/relations, observe channel choreography, and subscribe to state changes.
Companion to `ARCHITECTURE.md` and `Cargo.toml`. Maintenance: `primary/skills/repo-intent.md`.*

## Repo-scope only

This file carries only the intent that is FOR this `signal-mind` contract. Workspace-shape
intent stays in the primary workspace `primary/INTENT.md`. Component daemon intent stays
in `mind/INTENT.md`.

## Why this repo exists

`signal-mind` is the **ordinary peer-callable wire contract** for the `mind` daemon.
It carries the vocabulary for submitting typed thoughts and relations, querying the work
graph and memory state, observing channel choreography, and subscribing to state changes.
Owner-only policy configuration stays in `owner-signal-mind`; runtime actors, sockets,
storage, and choreography logic live in `mind`.

## The channel shape

The mind contract carries:

- **Requests:** `Submit` (thoughts/relations), `Query` (typed reads), `Adjudicate` (channel
  choreography requests), `Tap`/`Untap` (mandatory observer streams)
- **Replies:** `ThoughtCommitted`, `RelationCommitted`, `Queried`, `AdjudicationReceipt`,
  `Rejection` (with typed reasons), `Unimplemented` (skeleton honesty)
- **Events:** `SubscriptionDelta` events for open streams; `Untap` closes the stream

The wire vocabulary is contract-local — the daemon lowers these public operations into
component-local commands; Sema classification happens at observation time, not on the wire.

## Channels are closed, boundaries are named

- Wire enums are closed. No `Unknown` escape hatch.
- Request payloads do not mint timestamp, event sequence, thought ID, relation ID, or sender.
- `mind` mints those values at the daemon; request records accept submitted thought/relation
  bodies and metadata only.
- No stringly-typed dispatch. Graph kinds, channel endpoints, and reason fields are typed
  closed enums.

## Wire vocabulary discipline

Per `primary/skills/contract-repo.md` §"Public contracts use contract-local operation verbs":

- Operation roots are domain verbs: `Submit`, `Query`, `Adjudicate`, `Tap`, `Untap`.
- Reply success variants match operation past-tense: `Submit` → `ThoughtCommitted`; `Query` → `Queried`.
- Reply rejections are `Rejection` carrying typed `RejectionReason`.
- Payload records are domain nouns: `Thought`, `Relation`, `Query`, `AdjudicationRequest`,
  not `ThoughtRequest` or `SubmitPayload`.

## Constraints

- This crate carries only typed wire vocabulary, NOTA codecs, and round-trip witnesses.
- No runtime code: no actors, no tokio, no socket binding, no redb, no choreography policy logic.
- Contract types derive NOTA in this crate. Clients do not carry shadow types.
- Every operation and reply variant round-trips through both rkyv frames and NOTA text.
- Request payloads cannot carry timestamps, IDs, or sequence numbers; daemon supplies those.
- Channel choreography observation is read-only in this contract; authority orders live in
  `owner-signal-mind`.

## Three-layer model

Layer 1 (this crate): contract operations on the wire (`Submit`, `Query`, `Adjudicate`).
Layer 2 (daemon): component-local `MindCommand` enum that the daemon executes.
Layer 3 (observation): payloadless Sema class labels (`Assert`, `Mutate`, `Match`, `Subscribe`)
  for cross-component introspection.

The contract names the public action; the daemon decides internal work and Sema class.
Sema classification never appears on the wire.

## Code map

```text
src/lib.rs              — Thought/Relation/Query records, NOTA codecs, signal_channel! invocation
examples/canonical.nota — NOTA examples: (Submit ...), (Query ...), (Adjudicate ...)
tests/round_trip.rs     — rkyv frame and NOTA round-trip witnesses per operation
```

## Non-ownership

This crate does not own:

- `mind` daemon runtime, Kameo actors, or component lifecycle;
- `mind.redb` or any storage tables, graph indices, or choreography state;
- socket binding, transport, version handshake, or signature validation;
- choreography policy logic, channel grant execution, or adjudication decisions;
- CLI formatting, audit wrapping, or Nexus record composition.

## See also

- `ARCHITECTURE.md` — detailed channel shape, three-layer model, closed-enum discipline.
- `../mind/INTENT.md` — daemon-side schema-driven planes, actor topology, state schema.
- `../owner-signal-mind/INTENT.md` — owner-only policy signal.
- `primary/skills/contract-repo.md` — contract repo discipline and naming rules.
- `primary/skills/component-triad.md` — repo triad structure and wire layers.
```

#### owner-signal-router

```markdown
# INTENT — owner-signal-router

*The owner-only wire contract for Persona router policy and authority. Defines the
typed request/reply channel that orchestrate (and persona-spirit as router owner) use
to issue channel grants, extensions, revocations, and adjudication denials.
Companion to `ARCHITECTURE.md`. Maintenance: `primary/skills/repo-intent.md`.*

## Repo-scope only

This file carries only the intent that is FOR this owner-only `owner-signal-router` contract.
Workspace-shape intent stays in `primary/INTENT.md`. Component daemon intent stays in
`router/INTENT.md`.

## Why this repo exists

`owner-signal-router` is the **owner-only authority contract** for the `router` daemon.
It carries the vocabulary for issuing channel authority orders: `Grant` (open a new channel),
`Extend` (prolong channel lifetime), `Revoke` (close a channel), and `Deny` (reject an
adjudication request). Ordinary message routing and observation stay in `signal-router`;
runtime actors, sockets, storage, and routing logic live in `router`.

## The channel shape

The owner channel carries:

- **Requests:** `Grant` (channel creation), `Extend` (lifetime), `Revoke` (closure), `Deny` (rejection)
- **Replies:** `Authorized` (order accepted), `DenialAcknowledged` (rejection recorded),
  `RequestRejected` (with typed reason), `Unimplemented` (skeleton honesty)

This is an authority surface. Calls arrive from orchestrate (on behalf of owner) and carry
the authority that establishes which channel endpoints are allowed to exchange messages.

## Channels are closed, boundaries are named

- Wire enums are closed. No `Unknown` escape hatch.
- Request payloads do not mint channel IDs, timestamps, or authorization sequence numbers.
- `router` mints those at the daemon; request records carry the authority decision and
  channel endpoint specification only.
- Authority rejections use typed `DenialReason` closed enum (not string descriptions).

## Wire vocabulary discipline

Per `primary/skills/contract-repo.md` §"Public contracts use contract-local operation verbs":

- Operation roots are authority verbs: `Grant`, `Extend`, `Revoke`, `Deny`.
- Reply success variants match past-tense: `Grant` → `Authorized`; `Deny` → `DenialAcknowledged`.
- Reply rejections are `RequestRejected` with typed `RequestRejectionReason`.
- Payload records are authority nouns: `Grant`, `Extension`, `Revocation`, `Denial`,
  not `GrantRequest` or `ChannelAuthority`.

## Constraints

- This crate carries only typed wire vocabulary, NOTA codecs, and round-trip witnesses.
- No runtime code: no actors, no tokio, no socket binding, no redb, no grant execution logic.
- Contract types derive NOTA in this crate. Clients do not carry shadow types.
- Every operation and reply variant round-trips through both rkyv frames and NOTA text.
- Request payloads cannot mint channel IDs, authorization timestamps, or sequence numbers.
- Owner orders are distinct from ordinary observations; `signal-router` carries read-only
  observation vocabulary.

## Three-layer model

Layer 1 (this crate): owner operations on the wire (`Grant`, `Extend`, `Revoke`, `Deny`).
Layer 2 (daemon): component-local `RouterCommand` enum (e.g., `CreateChannel`, `UpdateDuration`).
Layer 3 (observation): payloadless Sema class labels for introspection.

The contract names the authority action; the daemon executes the channel mutation and
mints the durable channel ID and timestamp. Sema classification never appears on the wire.

## Code map

```text
src/lib.rs              — Grant/Extension/Revocation/Denial records, NOTA codecs, signal_channel!
examples/canonical.nota — NOTA examples: (Grant ...), (Revoke ...), (Deny ...)
tests/round_trip.rs     — rkyv frame and NOTA round-trip witnesses
```

## Non-ownership

This crate does not own:

- `router` daemon runtime, Kameo actors, or component lifecycle;
- `router.redb` or channel grant state tables, message slots, or delivery logs;
- socket binding, transport, or version handshake policy;
- channel authority enforcement logic, grant/revoke reducers, or message routing decisions;
- adjudication policy or message deferred-delivery logic.

## See also

- `ARCHITECTURE.md` — authority surface shape and closed-enum discipline.
- `../router/INTENT.md` — daemon-side schema-driven planes, actor topology.
- `../signal-router/INTENT.md` — ordinary observation and read contract.
- `primary/skills/contract-repo.md` — contract repo discipline and naming rules.
- `primary/skills/component-triad.md` — repo triad structure and authority tiers.
```

#### meta-signal-upgrade

```markdown
# INTENT — meta-signal-upgrade

*The owner-only meta-signal contract for the upgrade component. Defines the typed
request/reply channel that spirit (as upgrade owner) uses to manage upgrade catalogue policy,
selector authority (force-flip, rollback, quarantine), and migration permit control.
Companion to `ARCHITECTURE.md`. Maintenance: `primary/skills/repo-intent.md`.*

## Repo-scope only

This file carries only the intent that is FOR this `meta-signal-upgrade` contract.
Workspace-shape intent stays in `primary/INTENT.md`. Component daemon intent stays in
`upgrade/INTENT.md`.

## Why this repo exists

`meta-signal-upgrade` is the **owner-only meta-signal contract** for the `upgrade` daemon.
It carries the vocabulary for upgrade catalogue policy (`Register`, `Allow`, `Block`, `Query`)
and selector authority orders (`ForceFlip`, `Rollback`, `Quarantine`). Ordinary upgrade
attempts stay in `signal-upgrade`; runtime state, policy reducers, and selector logic
live in `upgrade`.

## The channel shape

The meta channel carries:

- **Catalogue policy:** `Register` (add migration to catalogue), `Allow` (permit attempt),
  `Block` (forbid attempt), `Query` (read policy)
- **Selector authority:** `ForceFlip` (override live selector), `Rollback` (revert migration),
  `Quarantine` (mark as failed)
- **Replies:** `Registered`, `PolicyUpdated`, `PolicySnapshot`, `SelectorActed`,
  `PolicyRejected` (typed reason), `Unimplemented` (skeleton honesty)

This is the authority surface for upgrade policy and emergency selector control.
Orchestrate calls this contract on behalf of spirit; peers call `signal-upgrade` for
ordinary migration attempts.

## Channels are closed, boundaries are named

- Wire enums are closed. No `Unknown` escape hatch.
- Request payloads do not mint policy revisions, timestamps, or authority sequence numbers.
- `upgrade` mints those at the daemon; request records carry the policy decision only.
- Policy rejection reasons are typed closed enums (not descriptions).

## Wire vocabulary discipline

Per `primary/skills/contract-repo.md` §"Public contracts use contract-local operation verbs":

- Operation roots are policy/authority verbs: `Register`, `Allow`, `Block`, `Query`,
  `ForceFlip`, `Rollback`, `Quarantine`.
- Reply success variants match past-tense: `Allow` → `PolicyUpdated`; `Rollback` → `SelectorActed`.
- Reply rejections are `PolicyRejected` with typed `PolicyRejectionReason`.
- Payload records are policy nouns: `Registration`, `Permission`, `SelectorAction`,
  not `RegisterRequest` or `UpgradePolicy`.

## Constraints

- This crate carries only typed wire vocabulary, NOTA codecs, and round-trip witnesses.
- No runtime code: no actors, no tokio, no socket binding, no redb, no policy execution logic.
- Contract types derive NOTA in this crate. Clients do not carry shadow types.
- Every operation and reply variant round-trips through both rkyv frames and NOTA text.
- Request payloads cannot mint policy revisions or timestamps; daemon supplies those.
- Ordinary migration attempts (`AttemptUpgrade`) stay in `signal-upgrade`; owner authority
  configures the gating policy that permits or blocks those attempts.

## Three-layer model

Layer 1 (this crate): owner/meta operations on the wire (policy and selector verbs).
Layer 2 (daemon): component-local `UpgradeCommand` enum (e.g., `RegisterMigration`,
`AllowUpgrade`, `ForceFlipSelector`).
Layer 3 (observation): payloadless Sema class labels for introspection.

The contract names the authority action; the daemon executes the policy/selector mutation.
Sema classification never appears on the wire.

## Code map

```text
src/lib.rs              — policy and selector records, NOTA codecs, signal_channel!
examples/canonical.nota — NOTA examples: (Register ...), (Allow ...), (ForceFlip ...)
tests/round_trip.rs     — rkyv frame and NOTA round-trip witnesses
```

## Non-ownership

This crate does not own:

- `upgrade` daemon runtime, Kameo actors, or component lifecycle;
- `upgrade.redb` or policy catalogue state tables, selector state, migration logs;
- socket binding, transport, or version handshake policy;
- policy enforcement logic, catalogue reducers, or selector state mutation;
- migration orchestration or handover coordination.

## See also

- `ARCHITECTURE.md` — meta-signal surface shape, catalogue policy, selector authority.
- `../upgrade/INTENT.md` — daemon-side schema-driven planes, actor topology, state schema.
- `../signal-upgrade/INTENT.md` — ordinary migration attempt contract.
- `primary/skills/contract-repo.md` — contract repo discipline and naming rules.
- `primary/skills/component-triad.md` — repo triad structure and authority tiers.
```

## Landing plan (the ~55 remaining)

## Tail Plan: ~55 Missing INTENT.md Files

The missing INTENT.md files cluster into four distinct groups by shape and landing mechanism.
Code-repo `main` is operator-owned; designers branch via `~/wt` and land on `main` branches
incrementally. Rather than 55 individual next-branches, batch by group and land in coordinated
pulls. Each group follows its template shape below.

### Group 1: Ordinary Signal Contracts (32 repos)

**Repos:** `signal-{agent, cloud, core, criome, domain-criome, engine-management, executor, forge,
frame, harness, introspect, lojix, message, orchestrate, persona, persona-origin, persona-spirit,
repository-ledger, sema, sema-upgrade, spirit, system, terminal, upgrade, version-handover}` + 7 more.

**Shape:** Wire vocabulary only. Single channel. Request/reply or request/event. No owner sibling
(or owner sibling exists separately). No daemon code.

**Template:** Use the reusable INTENT.md TEMPLATE above, filling:
- Component name and domain action description (from ARCHITECTURE.md)
- List of request verbs and reply variants (from signal_channel! declaration)
- Constraint list (closed enums, no runtime code, NOTA codec discipline)
- Non-ownership section (daemon, storage, policy logic)

**Filling approach:** Read each repo's existing `ARCHITECTURE.md` (all have one); extract the
"what is this" sentence, the channel operations list, and the constraints section. Most constraints
are boilerplate (closed enum, no tokio, NOTA derives). Verify the channel shape against the
`signal_channel!` invocation in `src/lib.rs`.

**Landing mechanism:** One PR per 5-8 repos (batched by component family: messaging, observation,
orchestration). Land on `main` in one coordinated pull after 2-3 repos are reviewed and accepted
(establish pattern confidence; subsequent batches move faster).

**Effort:** 32 repos ÷ 6-repos-per-batch = 6 batches. Est. 20 min per batch (template fill +
ARCHITECTURE extraction + review). Total: ~2 hours.

### Group 2: Owner-Only Signal Contracts (13 repos)

**Repos:** `owner-signal-{agent, mind, orchestrate, persona, persona-spirit, repository-ledger,
router, sema-upgrade, terminal, version-handover}` + 3 more.

**Shape:** Owner-only policy/authority surface. Paired with an ordinary `signal-*` sibling.
Request/reply only. No events/subscriptions (unless rare).

**Template:** Derive from the reusable INTENT.md TEMPLATE; adjust:
- Lead sentence: "owner-only authority contract for [component]" instead of "ordinary peer-callable"
- Constraints section: emphasize "owner orders are distinct from ordinary observations"
- Non-ownership: add "authority enforcement logic" and policy-specific items
- See also: link to both the ordinary `signal-*` sibling and owner-recipient component

**Filling approach:** Read each repo's `ARCHITECTURE.md`. Owner contracts are typically smaller
and more focused than their ordinary siblings. Extract verb list (usually 3-5: `Grant`, `Allow`,
`Configure`, `Inspect`, etc.) and constraint list. Verify closure against the sibling `signal-*`
docs.

**Landing mechanism:** One PR per owner-contract family (mind + owner-signal-mind paired,
agent + owner-signal-agent paired, etc.). Land after the ordinary sibling is accepted. Each pair-PR
bundles ~2-3 owner contracts.

**Effort:** 13 repos ÷ 3-repos-per-batch = 5 batches. Est. 15 min per batch. Total: ~75 min.

### Group 3: Meta-Signal Contracts (3 repos)

**Repos:** `meta-signal-{upgrade, cloud, domain-criome}`.

**Shape:** Owner-only meta-signal surface. Paired with an ordinary `signal-*` sibling. Higher
abstraction level than `owner-signal-*` — models policy catalogue, selector authority, and
feature gates, not just individual channel orders.

**Template:** Derive from the INTENT.md TEMPLATE; adjust for the meta-layer abstraction:
- Lead sentence: "owner-only meta-signal contract for [component]"
- Constraints: emphasize "meta-policy configuration" and "selector/catalogue authority"
- Non-ownership: add "catalogue reducers" or "selector logic"
- Code map: note any schema artifacts if the repo carries them

**Filling approach:** Read each repo's `ARCHITECTURE.md` (all are recent and well-documented).
Meta contracts use domain-specific vocabulary (catalogue, selector, delegation, projection policy).
Extract the operation set and constraints from the arch doc. Link carefully to the ordinary
sibling.

**Landing mechanism:** One PR for all three meta-signal contracts (they are rare and closely
coordinated with the schema migration). Land after their ordinary siblings + owner siblings
are accepted.

**Effort:** 3 repos. Est. 30 min total (they're small and already well-documented).

### Group 4: Daemon/Component Runtimes (7 repos)

**Repos:** `mind`, `router`, `message`, `introspect`, `criome`, `upgrade`, `orchestrate`
(7 of 7 missing; 1 has INTENT.md: `orchestrate`).

**Shape:** Long-lived daemon. Owns redb storage, Kameo actors, sockets, policy logic. Schema-driven
planes (signal/nexus/sema). Paired with one `signal-*` and zero or more `owner-signal-*` +
`meta-signal-*` siblings.

**Template:** Create a daemon-specific INTENT.md template (distinct from contract repos):

```markdown
# INTENT — [component]

*The [component] daemon and central state holder for [domain area].
Owns [list: "work graph state", "message routing", "upgrade orchestration"].
Paired with contract repos `signal-[component]`, `owner-signal-[component]` (if applicable),
and `meta-signal-[component]` (if applicable).
Companion to `ARCHITECTURE.md` and schema files. Maintenance: `primary/skills/repo-intent.md`.*

## Repo-scope only

This file carries daemon-side intent. Contract-side intent stays in `signal-*/INTENT.md`.
Workspace-shape intent stays in `primary/INTENT.md`.

## Why this repo exists

`[component]` is the long-lived daemon for [domain]. It holds durable state in `[component].redb`,
implements three schema-driven planes (Signal/Nexus/SEMA), owns Kameo actor topology, and
binds sockets for [peer/client] communication.

## Daemon-specific intent — [bullet list]

- [e.g., "Holds the work graph as the central source of truth"]
- [e.g., "Executes router logic and adjudication policy"]
- [e.g., "Orchestrates upgrade migrations and selector state"]

## Sibling contracts

- `signal-[component]/INTENT.md` — ordinary peer-callable operations
- `owner-signal-[component]/INTENT.md` — owner-only policy/authority (if applicable)
- `meta-signal-[component]/INTENT.md` — owner meta-signal policy (if applicable)

## Three-plane schema-driven architecture

Per `primary/skills/component-triad.md`:

- **Signal plane:** `schema/signal.schema` → `SignalRuntime` emits `SignalEngine` (admission,
  triage, reply dispatch).
- **Nexus plane:** `schema/nexus.schema` → `NexusRuntime` emits `NexusEngine` (action planning,
  effect sequencing).
- **SEMA plane:** `schema/sema.schema` → `SemaRuntime` emits `SemaEngine` (state management,
  observation).

## Constraints

- Durable state belongs here and lives in redb. Contracts hold wire vocabulary only.
- Policy logic, reducers, and transaction boundaries belong here. Contracts are behavior-free.
- Actors implement the three plane engines. No daemon logic leaks into contract codecs.
- Socket binding, transport, and version handshake policy belong here. Contracts are agnostic
  to transport.

## Code map

```text
src/lib.rs                      — component library surface
src/bin/[component]-daemon.rs   — long-lived daemon
src/bin/[component].rs          — thin CLI client
schema/signal.schema            — signal plane declaration
schema/nexus.schema             — nexus plane declaration
schema/sema.schema              — sema plane declaration
[component].redb                — durable state (at runtime)
```

## Non-ownership

This repo does not own:

- Contract wire vocabulary (lives in `signal-[component]` + siblings).
- Cross-component coordination (orchestrate owns that).
- [List component-specific non-owned items: "backup policy", "cross-worker scheduling", etc.]

## See also

- `ARCHITECTURE.md` — daemon architecture, plane integration, actor topology.
- `signal-[component]/INTENT.md` — ordinary contract intent.
- `owner-signal-[component]/INTENT.md` — owner contract intent (if applicable).
- `primary/skills/component-triad.md` — runtime triad structure and schema planes.
```

**Filling approach:** Daemon INTENT.md files are heavier because they describe state, actors,
planes, and logic. Read each daemon's existing `ARCHITECTURE.md` and schema files. Extract:
- One-sentence domain description
- List of sibling contract repos
- List of schema planes (all current daemons have signal + nexus + sema)
- Daemon-specific intent (e.g., "holds durable state", "owns actors", "executes policy")
- Code map (list the binaries, schema files, and redb)

Most daemons already carry detailed ARCHITECTURE.md; use those as the primary source.
Existing INTENT.md examples (`orchestrate`) provide the daemon-side tone.

**Landing mechanism:** One PR per daemon family (messaging: message; routing: router; work graph:
mind; etc.). Land after all related contract repos are accepted (so the cross-links are safe).

**Effort:** 7 repos. Est. 40-50 min per daemon (schema file extraction + relationship mapping).
Total: ~4.5 hours.

### Group 5: Libraries (3 repos)

**Repos:** `signal-core` (wire kernel), `signal-derive` (NOTA derives), `signal-frame` (frame
envelope and codec).

**Shape:** Shared library. No daemon. Depended on by many contract repos. No owner/meta tier.
Pure Rust crate.

**Template:** Create a library-specific INTENT.md template:

```markdown
# INTENT — [library]

*Shared [purpose: "wire kernel", "derive macros", "frame codec"]. Depended on by
[list major consumers: "every signal contract", "every daemon"].
Maintenance: `primary/skills/repo-intent.md`.*

## Repo-scope only

This file carries library-side intent. Workspace-shape intent stays in `primary/INTENT.md`.

## Why this repo exists

`[library]` is the shared library for [purpose]. It is depended on by [consumers] and
provides [list: "Frame encode/decode", "Nota derive macros", "binary framing rules"].

## Library discipline

- **No daemon.** This is a pure library crate.
- **Exported API is stable.** Every consumer pins a version; breaking changes require
  coordinated upgrades across [list: contracts, daemons, or the full stack].
- **Separation of concerns.** [e.g., "Frame owns the envelope and length-prefix mechanics;
  payload interpretation stays in consumer contracts"].

## Constraints

- Stability is load-bearing. Do not break the exported API without a major version bump
  and coordinated upgrade of all consumers.
- The library is not a grab-bag. If multiple unrelated concerns are bundled, consider splitting.
- Wire-format rules belong here; business logic belongs in contracts or daemons.

## Code map

```text
src/lib.rs              — library API entry
src/[module].rs         — per-module implementation
tests/                  — round-trip and invariant witnesses
Cargo.toml              — versioned dependency spec
```

## Major consumers

[List repos that depend on this library and describe the relationship:
- `signal-*` contracts depend on [frame codec] for wire mechanics
- `triad-runtime` depends on [trace codec] for transport
- etc.]

## See also

- `ARCHITECTURE.md` — detailed API design and stability policy.
- `Cargo.toml` — version and dependency spec.
```

**Filling approach:** Library INTENT.md files are small because libraries have simpler scope.
Read `ARCHITECTURE.md` for each. Extract:
- One-sentence purpose
- List of major consumers
- API stability statement
- Code map

These are straightforward; most of the text is boilerplate.

**Landing mechanism:** One PR for all three libraries (they are small and rarely change).
Land early (they are depended on by contracts; contracts need clean dependencies before landing).

**Effort:** 3 repos. Est. 20 min total.

---

## Implementation Sequence

1. **Week 1 — Libraries.** Land the three library INTENT.md files (signal-core, signal-derive,
   signal-frame). Establishes the foundation for contract repos.

2. **Week 1-2 — Ordinary Signal Contracts (Batch 1-2).** Land 10-12 ordinary contract repos
   (signal-message, signal-router, signal-mind, etc.). Batches of 5-6.

3. **Week 2 — Owner-Only Signal Contracts (Batch 1-2).** Land 6-7 owner-signal repos.
   Batches of 2-3.

4. **Week 2-3 — Meta-Signal Contracts.** Land 3 meta-signal repos in one PR.

5. **Week 3 — Remaining Ordinary Contracts (Batch 3-6).** Land remaining 22 signal-*
   repos in 4-5 batches.

6. **Week 3-4 — Remaining Owner Contracts.** Land remaining 6-7 owner-signal repos in 2-3 batches.

7. **Week 4 — Daemon Runtimes.** Land 7 daemon INTENT.md files (mind, router, message,
   introspect, criome, upgrade). Likely 3-4 PRs.

---

## Recommended Landing Mechanism

**Grouping:** Batch by component family and authority tier. One PR bundles logically related
repos to reduce review context-switching:

- **Contract batches:** 5-6 repos per PR. Group by domain (messaging, routing, observation,
  orchestration).
- **Authority batches:** 2-3 repos per PR (ordinary + owner sibling pair, or isolated owner).
- **Meta contracts:** All 3 in one PR (rare, well-scoped).
- **Daemons:** 1-2 per PR (heavy context; spread review load).

**Review load:** ~2 hours per day, 4 days a week = ~8 hours/week.
Total task: ~12-15 hours of agent time (extraction + template filling + cross-linking).
Actual PRs can move faster once the template is proven on 2-3 examples.

**Authority:** Operator lands these on `main`. Designers read+approve in code review; landing
is operator's call once the template pattern is proven (first 3-4 PRs establish confidence).

**Stale-proof:** Once the task is done, all 516 repos have INTENT.md covering their specific
scope. Workspace-level intent stays in `primary/INTENT.md` + specific skills. Per-repo INTENT.md
becomes the single source of truth for "why does this repo exist."

## Landing — the coordination decision

Code-repo `main` is operator-owned; designers branch via `~/wt`. Landing
60+ INTENT.md files as 60+ designer next-branches is impractical.
Recommendation:

- **Operator lands the distilled 3** (schema-next, schema-rust-next,
  spirit) as part of the active schema-stack work on `main` — they own
  those repos and are editing them now.
- **Operator or designer lands the 3 daemons** (mind, router, message)
  from the drafts above.
- **The ~55 contract tail batches by group** (per the plan above) using
  the template — one focused operator pass per group, not per-file
  branches.

Awaiting the psyche's call on the mechanism (operator batch-lands vs
designer next-branch waves), and operator concurrence since it is their
`main`.
