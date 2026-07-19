# Spirit SEMA and daemon redesign gate

## Status and recommendation

This is a design-only proposal. It does not change Spirit, storage, generated code, or a production database. It does not settle Protos source spelling or the Nomos macro surface.

Recommendation: replace the current single `EngineActor` plus embedded `Nexus` and `Store` shape with explicit Signal, Nexus, SEMA, owner-policy, subscription, and effect actors. Make the version-14 Spirit store a small authoritative state model with two application record families, and let the versioned SEMA log be its transition history. Keep public ordinary, meta, and streaming contract semantics stable where they remain clean; change storage layout without treating version-13 rows as an architectural constraint.

Implementation is gated on explicit psyche acceptance of this redesign. Migration proof is separately gated on an isolated, consistent snapshot only.

## Evidence reviewed

The design is grounded in the current `SpiritLineageBTrain` sources:

- `spirit/schema/nexus.schema` currently declares an open-ended internal effect catalogue and the Signal-to-Nexus-to-SEMA roots.
- `spirit/schema/sema.schema` currently declares `StoredRecord`, `StoredReferent`, and `Migration` families.
- `spirit/build.rs` imports the ordinary and meta contracts, then emits Nexus, SEMA, and daemon modules through the pre-Lineage-B generation driver.
- `signal-spirit/schema/signal.schema` owns ordinary request/reply/event vocabulary and the existing intent subscription relation.
- `meta-signal-spirit/schema/meta-signal.schema` owns privileged configuration, import, removal, and head-observation vocabulary.
- `spirit/src/engine.rs`, `src/nexus.rs`, `src/store/mod.rs`, and generated `src/schema/daemon.rs` carry the current composition, storage, subscriptions, and transport.
- `sema-storage/src/lib.rs` and `signal-sema-storage/src/lib.rs` show the separate prototype storage actor and its signal vocabulary. That prototype is not adopted as Spirit's storage topology; it is evidence for the single durable writer and typed push boundary.

The current source worktrees were clean when reviewed. No private Spirit data or state path was opened.

## Current complexity that the redesign dissolves

1. One generated `EngineActor` owns ordinary work, meta connections, the `Engine`, `Nexus`, and the SEMA store. The actor serializes every one of those concerns. The owner control plane can therefore wait behind ordinary work, while a long owner request can wait behind ordinary work. This conflicts with the required physical separation between control and data planes.

2. `Nexus` owns storage, in-flight mail, stash retention, observer retention, subscription token allocation, policy, and external effect decisions. A single noun therefore owns unrelated lifetime and failure boundaries.

3. Synchronous SEMA reads and writes run inside the Nexus loop, using `block_in_place` when possible. Durable storage work is therefore embedded in the decision actor instead of being owned by the SEMA actor.

4. The generated subscription registry holds its mutex while writing and flushing each subscriber socket. A slow subscriber can delay registration, removal, and delivery for every subscriber.

5. The live store has entries, referents, migrations, an in-memory archive target, a separate archive database, and a separately versioned guardian journal. The current archive path is a two-store operation rather than one atomic lifecycle transition.

6. Version-13 migration support contains readers for numerous historical layouts. That is useful recovery history, but it must not become the version-14 daemon's normal data model.

7. One request correlation is represented by several plane-local `OriginRoute` wrappers and manually converted between them. A request identity should be carried once across actor mail.

## Proposed state and actor topology

The process supervisor owns the following actors. Each has a single named state owner and a failure boundary.

```text
ordinary listener -> SignalAdmission -> SpiritNexus -> SpiritSema
                                          |              |
                                          |              +-> CommittedChange -> SubscriptionBroker
                                          |
                                          +-> JudgeClient / GateClient / MirrorProjection

owner listener -> OwnerPolicy -> SpiritNexus -> SpiritSema

SubscriptionBroker -> one Delivery actor per live subscription writer
```

### Process supervisor

The supervisor owns startup order, shutdown order, child references, metrics, and restart policy. It starts SEMA before Nexus, Nexus before listener admission, and starts the owner listener independently of ordinary traffic. Shutdown stops new admission first, rejects or drains in-flight work by typed terminal outcome, stops effect dispatch, commits or aborts a staged durable transition, releases listeners and database resources, then publishes termination.

A storage-open or storage-integrity failure stops ordinary admission. It is not retried by spawning a second writer. A failed subscription delivery removes only that subscription. A failed judge, gate, or mirror effect returns its typed failure to Nexus; it cannot mutate SEMA by itself.

### SignalAdmission actor

SignalAdmission owns request correlation allocation, typed frame admission, validation, and the reply capability associated with an accepted connection. It has no durable state and no direct store handle. It decodes only the contract frame from `signal-spirit` or `meta-signal-spirit`, rejects malformed or unauthorized-tier input before creating work, and sends a typed `NexusRequest` mail.

The ordinary and owner listeners remain separate at the transport boundary. Listener tier and socket permissions decide which contract decoder is used. The actor records a terminal reply or failure for every accepted request; it never polls SEMA.

### SpiritNexus actor

SpiritNexus owns the in-flight request table, pure operation lowering, continuation state, and child references for external effects. It does not own the database, a socket writer, a NameTable, or a subscription registry.

A Nexus request becomes one of three typed actions:

- a SEMA read or mutation command;
- an external effect request, such as a judge verdict, a cluster authorization decision, or mirror distribution;
- a terminal reply.

The decision object carries one process-local request correlation through every mail. It is not an encoded language identifier and it is never persisted as a NameTable row. A SEMA result or effect result returns as typed mail and causes the next decision or terminal reply. This preserves Signal to Nexus to SEMA traversal without direct helper calls.

### SpiritSema actor

SpiritSema is the sole owner of the v14 `sema-engine` handle and all durable writes. It receives typed read and mutation mail. Its mutation handler validates transition preconditions, commits one legal transition, returns the typed receipt to Nexus, and pushes one `CommittedChange` only after commit succeeds.

Reads are typed SEMA queries. They either run through this actor or through a future read-only snapshot actor created and published by SpiritSema. No reader receives mutable database access. The first implementation may serialize reads behind the SEMA mailbox; performance work must add published immutable snapshots, not a shared mutable database lock.

When cluster authorization is enabled, the SEMA actor owns one durable staged-advance slot through the storage engine's staging facility. A staged mutation is not visible to queries or subscriptions. A grant causes one materialization commit; any other terminal decision discards the staged mutation. Restart recovery sees that one slot and refuses a new advance until it is resolved by typed owner policy.

### OwnerPolicy actor

OwnerPolicy is the independent control-plane actor. It owns only live owner policy: archive projection target, gate target, mirror target, and other daemon configuration that is intentionally reset from binary configuration on process restart. It is not a SEMA record family.

A meta request first passes the owner listener's authority boundary, then OwnerPolicy. Policy updates are pushed to the affected child actor and acknowledged before the meta reply. Owner import and lifecycle commands carry explicit owner authority through Nexus to SEMA, but do not queue behind the ordinary listener's admission queue.

### SubscriptionBroker and Delivery actors

SubscriptionBroker owns the token-to-filter registry and only subscription metadata. A separate Delivery actor owns each live socket writer. The broker never holds a registry lock while awaiting socket I/O.

For a subscription open, SEMA supplies the commit marker at which the subscription begins. The broker reserves the token and filter before the ordinary acknowledgement is written, then activates it after that acknowledgement. Committed events carry their commit marker. Events after the start marker are queued in order until activation, so the client cannot miss an event between acceptance and activation or receive an event before its acknowledgement.

A close request uses the accepted streaming relation's closed token type. Broker removal is terminal: after the close acknowledgement, no later event is sent for that token. A writer failure sends `DeliveryFailed` back to the broker; it removes that one token and does not block other subscribers or SEMA.

### Effect actors

JudgeClient, GateClient, and MirrorProjection are supervised children of SpiritNexus. Each owns its external connection and timeouts. Each accepts and returns typed values. Judge and gate failures are fail-closed for the operations they govern. Mirror failure never changes whether a committed local intent exists; it changes only the typed distribution outcome and retry state.

## Version-14 durable record families

The v14 live Spirit database has exactly two application record families.

1. **IntentRecord** is the one authoritative row for an intent record identity. It contains the opaque public record handle, the imported `signal-spirit` entry value, and one closed lifecycle state. The lifecycle state has active, retired, superseded, and archived states. A superseded state carries its replacement record identities. A clarification or correction is a legal transition of this row and its versioned-log history, not a new special family.

2. **ReferentRecord** is the one authoritative row for a canonical referent. It contains the canonical referent value and its aliases. It is the only referent alias authority. The alias list is data about a referent, not a NameTable and not a Protos transparent type alias.

The sema-engine format header, family descriptors, commit sequence, content digest, and the optional one-slot staged advance are storage-engine metadata, not extra Spirit application families. Version-14 has no application `Migration` family, no mutable subscription family, no stash family, no mail-ledger family, and no persistent runtime-policy family.

The archive is a lifecycle state in the authoritative store. Owner collection atomically changes eligible records to archived, so ordinary queries exclude them and the response can retain the existing removal-facing contract semantics. A separately configured archive database, if still desired for operations, is a retryable derived projection of committed archived rows. It is not the truth that permits removal. This dissolves the current cross-store archive-then-retract partial-failure shape.

Judge reasoning and model transcripts do not enter the authoritative Spirit SEMA store. If durable audit is required, the judge component owns a separately authorized typed audit store. Spirit retains only typed acceptance or rejection outcomes needed for the current request and trace boundary.

## Identity, name, and version boundaries

There are four distinct identity classes. They must not be converted by convenience casts.

1. An **encoded identifier** is the language identity carried by an encoded form. It is a closed enum whose tag is the component namespace and whose payload is a `u16`. The central slice authority governs the tag set. Spirit, its ordinary signal contract, its meta contract, Schema, and Logos each use their component-owned namespace. No new construct assumes a flat integer or one global NameTable.

2. A **NameTable entry** maps an encoded identifier to a rendering name. Each component owns one composable NameTable slice. Manifest composition borrows slices by namespace; it does not use `extend_from`, copy unrelated entries, or flatten identifier spaces. Nomos receives typed encoded values and identifiers only. Name lookup, ordinal derivation, and rendering happen at the NameTable and emission boundary.

3. A **transparent source alias**, if one is needed by the Rust projection, is first represented as an additional NameTable entry resolving to the target encoded identifier. It disappears during decode and is re-emitted from the NameTable only. No encoded alias declaration is added unless this route demonstrably fails to preserve the contract's source and Rust fidelity.

4. An **IntentRecord handle** is the durable identity of a user intent row. It is an opaque contract value and is not an encoded identifier, a NameTable key, a type identifier, or a process request correlation. A **request correlation** is process-local and disappears after its terminal reply. A **database marker** describes a committed state; it is not either kind of identity.

The v13 to v14 boundary is a storage-layout boundary. V14 is a new `sema-engine` schema version with new family descriptors and a generated v14 contract surface. Existing public ordinary and meta contract values should retain their operation meanings and ordering where this remains clean. Any wire change required by the accepted streaming relation or lifecycle redesign is a separately versioned contract change with explicit old/new proof; it is never silently smuggled in through a storage migration.

## Minimal generated constructs

The redesign deliberately avoids a broad Rust abstract-syntax expansion.

The new pipeline must generate or project only:

- imported encoded contract type references from `signal-spirit` and `meta-signal-spirit`;
- closed structs, newtypes, vectors, options, maps, enums, and unit-or-one-payload interface variants needed for signal, SEMA, actor mail, and record families;
- typed manifest dependencies and one bidirectional StructureTree for read and re-emission;
- the accepted closed streaming relation, which projects the existing subscription opener, acknowledgement, token, event, and close-token frame surface;
- concrete actor mail types and their typed frame adapters;
- ordinary Rust implementations of the shared actor/runtime interfaces for generated data-bearing actors, emitted from the same generic runtime pattern for every component.

The redesign does not require schema-authored component trait definitions, associated types, default methods, opaque `impl Future` associated outputs, arbitrary where clauses, or a general Rust-method-body language. The current component-specific `NexusEngine`, `SemaEngine`, and `ComponentDaemon` trait families are not the target source model.

If the shared runtime needs a generic adapter to host generated actor mail, that adapter belongs in `triad-runtime` and applies to every component. A Spirit-only generated trait hierarchy would be a bypass. Handwritten behavior remains on data-bearing runtime actors and consumes generated mail types; it does not recreate contract or storage types locally.

This does require the general Rust projection to support imports and concrete trait implementation blocks used by the shared actor framework, plus asynchronous actor handlers. Those are small, reusable code-generation needs. They do not require a user-authored macro surface, and this proposal supplies no macro spelling.

## Worked flows

### Ordinary record

1. The ordinary listener decodes a typed ordinary request and sends it to SignalAdmission.
2. SignalAdmission validates it, assigns a process correlation, and sends typed mail to SpiritNexus.
3. SpiritNexus requests referent settlement or a judge decision when the operation requires it. The external child returns a typed result.
4. SpiritNexus sends one typed mutation command to SpiritSema.
5. SpiritSema commits the IntentRecord and any referent transition atomically, returns a typed receipt to Nexus, and pushes `CommittedChange` to SubscriptionBroker after the commit.
6. Nexus sends the ordinary typed reply through SignalAdmission. The broker pushes matching committed events independently. A subscriber never causes a second store read to reconstruct an event.

### Ordinary observation

1. SignalAdmission validates and sends the observation to Nexus.
2. Nexus lowers it to a typed SEMA query.
3. SpiritSema returns a typed snapshot at a database marker.
4. Nexus returns the matching ordinary output. No effect actor, subscription event, or mutable store access is involved.

### Owner policy and import

1. The owner listener accepts only the meta contract tier and sends the request to OwnerPolicy.
2. A policy update is validated, pushed to the affected child actor, and acknowledged before the typed meta reply.
3. An owner import or lifecycle request carries owner authority to Nexus and then to SpiritSema. It is still a typed SEMA transition, but it bypasses the ordinary judge only because the meta boundary granted that authority.
4. Archived lifecycle changes are committed before any optional archive projection runs. Projection failure is visible and retryable; it cannot resurrect or silently alter the authoritative state.

### Streaming subscription

1. SignalAdmission sends the typed subscription opener with its delivery endpoint to Nexus.
2. Nexus obtains a start marker from SEMA and asks SubscriptionBroker to reserve a typed token and filter at that marker.
3. SignalAdmission writes the typed acknowledgement. It then activates the reservation.
4. Every later SEMA commit pushes a typed event to the broker. The broker routes only matching events to the appropriate Delivery actors.
5. A typed close request removes the reservation. Delivery failure also removes only the failed reservation.

## Trust and failure boundaries

- Frame parsing and archive validation are Signal concerns. Invalid bytes never become Nexus work.
- Ordinary versus owner authority is enforced by separate listeners, socket permission, and listener tier. Connection credentials may add checks, but they do not become a stringly route.
- Only SpiritSema writes the authoritative database. No Nexus, subscription, judge, mirror, or transport actor owns mutable store state.
- A commit is the only source of a subscription event. Events are push notifications, not evidence that a client successfully observed them.
- Judge and gate failures refuse their governed mutation before SEMA commit. Mirror failure is a distribution failure after local commit.
- Pending gated work is invisible until materialized. Crash recovery is one explicit staged slot, not a hidden retry queue.
- NameTable composition is a source and emission concern. It is not a storage, daemon, or Nomos string-manipulation concern.
- Private content and private snapshot material must never appear in migration logs, generated source, commits, or this design artifact.

## v13 to v14 migration plan

The v14 migration is a one-way, logged fold with one frozen reader, not a permanent compatibility tower.

1. Freeze the version-13 reader and its signal contract dependencies in a dedicated migration crate. It accepts only the version-13 layout and rejects every other source version loudly. Older layouts must first be migrated to v13 by their existing historical tooling.
2. Require a consistent source snapshot. The migrator never copies a live-mutating database file by ordinary file copy.
3. Open the snapshot with the frozen v13 reader. Read only the version-13 `StoredRecord` and `StoredReferent` material needed for the new model.
4. Construct a fresh v14 database beside the candidate input. Fold each source record into an IntentRecord, preserving its opaque record handle and public entry semantics. Fold referent rows into ReferentRecord. Map retired, superseded, and removal-candidate behavior to the v14 lifecycle rule through explicit typed transitions.
5. Run typed validation before exposure: source rows map exactly once, reference targets resolve, lifecycle invariants hold, the v14 store reopens, and ordinary/meta/streaming contract tests pass. Diagnostics report pass or typed failure categories, never record contents, identifiers, counts, or hashes from a private candidate.
6. Write a migration-completed record only through the storage engine's version metadata and committed log; do not add a special mutable migration family. Close the candidate store and reopen it before declaring success.
7. Preserve the source snapshot as rollback input. For a later production migration, create a backup, then expose the new file through one atomic rename only after an approved migration result. The live path is never modified during snapshot proof.
8. Remove the frozen v13 reader after the deployment migration window closes. It is a migration tool, not a runtime dependency of the v14 daemon.

## Future isolated-production-snapshot proof

This proof has not run. It runs only after psyche acceptance of this redesign and after implementation.

1. Stop or quiesce the production writer long enough to use the storage engine's supported checkpoint or snapshot mechanism. Create a private, permission-restricted candidate copy from that consistent snapshot. Do not inspect, print, commit, or report its contents, paths, counts, or hashes.
2. Run the frozen v13 reader and v14 migrator against the candidate only. Confirm source integrity without changing the original.
3. Start the Nix-built v14 daemon against the migrated candidate with isolated sockets and typed local judge/gate fixtures. No candidate daemon uses production sockets or writes production paths.
4. Prove ordinary record and observation operations, owner policy/import/lifecycle operations, and streaming open, acknowledgement, ordered delivery, close, and failed-writer cleanup. Prove a candidate-only mutation, daemon restart, reopen, and typed observation of that mutation.
5. Run the required old/new contract compatibility matrix where the public wire contract remains compatible: old client to new daemon and new client to old daemon for ordinary, meta, and streaming paths. If a contract version must change, run an explicit version-handover/rejection proof instead; do not report it as compatibility.
6. Verify the original production source remains unchanged through the approved snapshot mechanism and a typed integrity check. Delete the candidate store, sockets, logs, and temporary runtime files after the all-green run.
7. Report only the exact Nix commands, their truthful full denominators, and pass/fail categories. Do not report private data.

## Alternatives considered

### Retain the current single EngineActor

This minimizes initial code movement but keeps control-plane queueing, direct SEMA work inside Nexus, shared subscription delivery locking, and a component-sized failure domain. It does not dissolve the observed complexity. Rejected.

### Move generic daemon behavior into triad-runtime while keeping generated component traits

This reduces some Spirit code but leaves the language pipeline responsible for broad trait definitions, associated types, asynchronous opaque return forms, default methods, and component-specific runner APIs. It turns a runtime adaptation concern into a large language feature. Rejected.

### Recommended: shared actor runtime plus generated typed mail and concrete component actors

The shared runtime owns generic actor and listener mechanics. The language engine owns encoded contract types, typed mail data, manifests, StructureTrees, and projections. Spirit owns only its domain transitions and data-bearing actor behavior. This keeps the generator end-to-end without making Spirit a special compiler target. Recommended.

## Review findings

- **High — `spirit/src/schema/daemon.rs:438-482`:** subscription publication holds the registry mutex while awaiting writes and flushes. A slow subscriber can block all subscription registry changes and deliveries. The redesign assigns each writer to a separate Delivery actor.
- **High — `spirit/src/schema/daemon.rs:566-652`:** ordinary, staged, and owner meta requests share one EngineActor mailbox. This collapses the owner control plane into ordinary data-plane scheduling. The redesign creates an independent OwnerPolicy actor and listener path.
- **Medium — `spirit/src/nexus.rs:1044-1071`:** Nexus performs synchronous durable reads and writes with `block_in_place` or direct calls. This puts blocking storage inside the decision actor. The redesign makes SpiritSema the only database owner.
- **Medium — `spirit/src/store/mod.rs:109-119`:** one Store carries database state, family handles, path, mutable archive policy, and tracing. Runtime policy and storage authority have different lifetimes. The redesign moves policy to OwnerPolicy and keeps SEMA state limited to record families and engine metadata.
- **Medium — `spirit/src/production_migration.rs:224-370`:** the runtime migration code enumerates many historical layouts and archive combinations. V14 should use one frozen v13 reader for its migration window rather than inheriting the historical reader tower.
- **Low — `spirit/src/plane.rs:6-59`:** a single request route is copied between local, Nexus, and SEMA wrappers through hand-written conversions. The redesign carries one typed process correlation in actor mail.

## Residual risks

- The exact lawful source forms for aliases, interface variants, streaming relations, imports, and any concrete implementation blocks remain a separate codec-verified source-surface gate. This proposal intentionally does not invent spelling.
- The closed namespace variant set for encoded identifiers is governed by the active slicing design. Spirit must consume that authority rather than define a local flat or merged identifier representation.
- Making archive status authoritative changes the current two-store operational mechanism. Public meta behavior and physical retention policy need an explicit contract review before implementation.
- A v13 snapshot may expose historical values whose semantics cannot be mapped to the v14 lifecycle model without a typed migration rejection. The migrator must reject rather than silently flatten those cases.
- The actual `sema-engine` snapshot API and atomic swap behavior must be verified during implementation. This design does not assume a raw file copy is safe.
- Subscription delivery ordering is defined by commit markers, but backpressure and bounded per-subscriber queues need a concrete policy before implementation. A full queue must produce typed closure or explicit loss policy; it must not silently drop committed events.
