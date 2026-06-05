# 77.1 — The refreshed triad-port recipe (successor to report 75/3)

Source-grounded re-baseline of the port recipe after the foundation moved. Verified
against current source: spirit HEAD `fae33ee` on emitter v0.1.14; `triad-runtime`
0.2.1 (`973e1d3`); `schema-rust-next` `7f59b39`/v0.1.14; `sema-engine` `e1aeef1`; lojix
`triad-port` present and building. Confidence: **High** (read-only — no fresh `cargo
test`, so "builds" rests on source shape + recent commits + checked-in artifacts).
Full per-agent detail in workflow transcript `w35dr52v4` / `wf_62cd64af-ec2`.

## The one-sentence shape (still holds)

A triad daemon checks in `.schema` files; `schema-rust-next`'s `build.rs` driver emits
plane modules carrying the engine **traits** + the runner adapter; the author hand-writes
the trait **impls** + a Store over `sema-engine` + a ~190-line daemon shell. **There is
no `triad_main!` macro** — the emitter stops at the engine traits + runner adapter
(verified empty grep). spirit is the single-listener worked example; **lojix/triad-port
is now the multi-listener worked example.**

## The recipe, step by step (what changed from 75/3 annotated)

### Step 0 — Author `.schema` files

Three plane files for a split daemon (`signal`/`nexus`/`sema`), positional NOTA,
type-first. The pipeline beneath is confirmed end-to-end with **no assemble step**
(`vez8`): authored text → `nota_next::Document::parse` → `schema_next::SchemaSource::
from_document` (structural macro node codec) → `SchemaEngine` lowers to
`schema_next::Schema` → `schema-rust-next LowerToRust<RustModule>` → `RustModule::
render()`. **Asschema is fully removed** in both repos (one stale doc-comment at
`schema-rust-next/lib.rs:2565`; the `Assembled*` names in schema-next are
macro-expansion stages, NOT the removed artifact — do not confuse them).

**New Step-0 sub-decision (streaming gate):** if the port needs push/subscribe, the
schema MUST declare a stream (`Schema::streams()` non-empty) AND the stream's event type
must equal the `Output` enum's `Event`-variant payload. This `streaming_event_payload is
Some` condition (`lib.rs:3419,3269`) gates not just the `StreamingFrame` aliases but also
the `LogVariant`/`RequestPayload` impls (`lib.rs:1106-1112`). A bare `Output.Event` name
is not enough.

### Step 1 — `build.rs` via the convenience constructors

API **unchanged and stable** — copy it. Use the convenience constructors, not a
hand-rolled loop:
- a wire / **meta-signal** CONTRACT crate → `GenerationPlan::wire_contract(root,name,ver)`
  (`RustEmissionTarget::WireContract`, no engine traits);
- a single-crate DAEMON → `GenerationPlan::daemon_runtime(...)` (auto-adds
  `nexus_runtime()`+`sema_runtime()`) + `.with_module(ModuleEmission::
  signal_runtime_module("signal"))`;
- an unsplit bootstrap → `component_runtime_compatibility(...)`.

Cross-crate imports: `with_dependency_schema_directory(name,dir,ver)` or
`DependencySchema::from_cargo_metadata(...)`; the dependency contract crate must call
`CargoSchemaMetadata::emit_schema_directory` in its `build.rs`. Then
`GenerationDriver::new(plan).generate()?.write_or_check("<CRATE>_UPDATE_SCHEMA_ARTIFACTS")?`
— writes when the env var is set, else asserts checked-in `src/schema/*.rs` byte-identical
(`StaleGeneratedArtifact`) after a text+rkyv round-trip.

*Changed from 75/3:* the convenience constructors are now the recommended entry points
(75/3 only showed the manual per-plane `.with_module`). Five `RustEmissionTarget`
variants unchanged.

### Step 2 — Implement the emitted engine TRAITS (now tokenized)

Hooks on data-bearing types (never free functions): `SignalEngine` →
`triage_inner`/`reply_inner`; `NexusEngine` → `decide`, `apply_sema_write(origin_route,
input)`, `observe_sema_read(origin_route,input)`, `run_effect(input)`,
`budget_exhausted_reply(exhausted)` + the **emitted, non-overridden `execute()`** that
builds `Runner::new(continuation_limit())`, wraps `self` in the emitted
`NexusRunnerAdapter`, calls `runner.drive` (author never writes the adapter; budget
default 32, a final Reply is free); `SemaEngine` → `apply_inner`/`observe_inner`. Plus
`on_start`/`on_stop`.

**Two hard rules now LANDED:**
- **`gb95` placement gate:** signal-frame route/encode/decode + streaming surfaces emit
  ONLY when `emits_signal()` is true (`WireContract`/`SignalRuntime`/`ComponentRuntime`
  bootstrap). `NexusRuntime`/`SemaRuntime` plane modules carry NO signal-frame code. Put
  the wire surface on the contract crate or the signal module — never on
  `nexus.schema`/`sema.schema`.
- **Runner-shape gate:** for `NexusRunnerAdapterTokens` to emit, the nexus action
  vocabulary must be the exhaustive runner shape (`ReplyToSignal` + matching
  `CommandSema*`/`CommandEffect`/`Continue`, each with its completion-work variant).
  Unknown action variants **reject runner emission outright** — no wildcard fallthrough.

*Changed from 75/3:* the traits/adapter/trace/streaming now `impl ToTokens` and emit via
`quote!` (`SignalEngineTraitTokens` 1409, `NexusEngineTraitTokens` 1518,
`SemaEngineTraitTokens` 1661, `NexusRunnerAdapterTokens` 4101). **Functionally
equivalent hooks; the emitted text differs — do not hand-diff against 75/3's quoted
snippets, regenerate.** 75/3's `lib.rs` line numbers are obsolete.

### Step 3 — Hand-write the Store over `sema-engine` (full identified CRUD now available)

`store.rs` implements `SemaEngine` over ONE `sema_engine::Engine` handle
(`Engine::open(EngineOpen::new(path, SchemaVersion::new(1)))`). **No raw redb** — now
mechanically test-gated by `sema-engine`'s own `tests/dependency_boundary.rs`. Pick
identity per table: `register_table(TableDescriptor::new(name))` for a natural key
(`EngineRecord::record_key()`); `register_identified_table(IdentifiedTableDescriptor::
new(name))` for engine-minted identity. Hold each returned `*TableReference` (Copy) as a
Store field; for N tables call `register_*` N times on the SAME Engine inside `open()`.

**Identified CRUD is now COMPLETE** (`817236a` Jun-4 + `e1aeef1` Jun-5 added
`mutate_identified`): `assert_identified` (mints `IdentifiedMutationReceipt`),
`match_identified` (`all`/`identifier`/`identifier_range` only — NO filter/predicate),
`mutate_identified` (replace at id), `retract_identified` (destructive). Keyed tables
additionally get `commit`/multi-op atomicity (the closed 6-op set, no `Atomic`).
`current_commit_sequence()?.value()` is the handover high-water mark; the Engine is
single-owner (held in the Nexus mutex; single-writer SEMA actor `e440` still PROPOSED).

*Changed from 75/3:* the mutate-via-retract-plus-assert workaround is **gone**;
no-raw-redb is now mechanically enforced inside sema-engine. **New named gaps:**
identified tables have NO subscribe, NO secondary index, NO multi-op atomic, and
reads are AllRows/ByIdentifier/ByIdentifierRange only.

### Step 4a — Request/reply transport (schema-emitted plane frame + triad-runtime prefix)

Copy `spirit/src/transport.rs` nearly verbatim. The request/reply byte layout is the
**schema-emitted raw plane frame**: `Input/Output::encode_signal_frame()` →
`[u64 little-endian short_header][rkyv archive]`; `decode_signal_frame` recovers
`(route, value)`. The transport wraps those bytes in `triad_runtime::LengthPrefixedCodec`
+ `FrameBody` (4-byte big-endian length prefix). **`signal_frame::ExchangeFrame` is used
by NOTHING in the daemon stack** (empty grep) — do not construct one; signal-frame
contributes only typed nouns here (`Request`, `Reply`, `ShortHeader`,
`ExchangeIdentifier`).

*Changed from 75/3:* this is a clarification, not a reversal — 75/3's "wrap
encode_signal_frame in LengthPrefixedCodec" was right; the attribution of the byte layout
to "signal-frame transport" was loose. **Watch-out:** a request/reply-ONLY port (no
stream declared) does NOT get `LogVariant`/`RequestPayload`/`Frame` aliases (streaming-
gated); `encode/decode_signal_frame` always emit under `emits_signal()`, so the raw
transport works regardless.

### Step 4b — Daemon shell (SingleListener or MultiListener; still hand-written)

~190 lines, no macro. ONE socket → `impl DaemonRuntime` on a data-bearing runtime →
`SingleListenerDaemon::new(socket_path, runtime, RequestErrorLog::new(name)).run()`
(spirit template). ORDINARY + META/OWNER sockets → a `Clone+Display` listener-tag enum
(lojix's `ListenerRole{Ordinary,Owner}`), `impl MultiListenerRuntime`, hand a
`Vec<ListenerSocket<Tag>>` (each `.with_socket_mode(SocketMode::new(bits))`) to
`MultiListenerDaemon::new(sockets, runtime, error_log).run()`. **`lojix/triad-port/src/
daemon.rs` (188 lines) is the canonical two-listener template — copy lojix, not spirit,
for two sockets.** Do NOT invent a `DualListenerDaemon` (`rcn3`).

*Changed from 75/3:* lojix is now the CONFIRMED first `MultiListenerDaemon` consumer.
New `should_continue()` supervised-stop hook (`ceb7794`) + Drop socket-file cleanup
(`973e1d3`). `should_continue()` exists ONLY on the multi path — a single-socket port
needing graceful supervised shutdown should use `MultiListenerDaemon` with one socket.
`triad-runtime` 0.2.1 deps = `signal-frame` + `thiserror` only (no `signal-core`).

### Step 4c — Push/subscribe (spirit IS now the worked template — the biggest change)

Copy `spirit/src/subscription.rs` (`SubscriptionHub`) + `daemon.rs:148-182`. The path:
(1) declare open/close-subscription ops + an `Output.Event` variant whose payload == the
declared stream's event type; (2) in `handle_stream` clone the `UnixStream`, compute a
`SubscriptionFilter`, on a `SubscriptionStarted` reply `register(token, filter.
into_query(), writer)` on a `SubscriptionHub` over `triad_runtime::SubscriptionRegistry`
+ `SubscriptionEventPublisher::acceptor(ShortHeader::new(OUTPUT_EVENT), SessionEpoch)`;
(3) `publish` → `registry.publish_matching(&event, Query::matches, ...)` →
`publisher.publish(token, event)` building a real `StreamingFrame` → `encode()` →
`write_body`, unregistering dead writers. Client reads via `StreamingFrame::decode` after
the `SubscriptionStarted` reply (two wire encodings coexist on the socket by design).

*Changed from 75/3:* streaming was PROPOSED/not-landed there. **Now FULLY LANDED and
daemon-driven** — `triad-runtime/src/streaming.rs` (registry+publisher+token-issuer, 9
tests), `schema-rust-next` emits the `StreamingFrame` aliases + `into_subscription_frame`,
spirit consumes it end-to-end. **Caveat:** spirit publishes at the DAEMON layer from the
reply, not via sema-engine subscribe; sema-engine subscribe is KEYED-tables-only (no
`subscribe_identified`).

## What report 75 got wrong (corrections that matter)

- **Streaming is landed, not proposed** (75/3's single biggest stale claim). spirit is
  the push template.
- **The meta-signal rename partially ran — but the contracts are concept-only stubs.**
  `meta-signal-router` (`a67c331`), `meta-signal-orchestrate` (`bb421a9`), and
  `meta-signal-{lojix,cloud,domain-criome,repository-ledger,upgrade}` now exist on disk.
  BUT `meta-signal-router` has only `schema/meta-signal-router.concept.schema` (37 lines)
  + a 321-line `src/lib.rs`, **no `build.rs`, no schema-rust-next dep** — it is NOT yet an
  emitting wire contract. The repo rename happened; the schema is not yet real. **This
  resupersedes report 9's "rename hasn't run" — it ran, but produced stubs.**
- **`primary-vllc` payload-less concern fully retired** — lojix/triad-port builds with
  payload-carrying AND payload-less variants emitting + decoding cleanly. lojix is the
  live proof.
- **Engine-trait line numbers + snippets are obsolete** (lib.rs churned ~2286 lines) —
  regenerate, never hand-diff.
- **`gb95` `emits_signal()` gate is now a hard rule** (75/3 didn't mention it).

## The gap/blocker table (drives the per-component sweep)

| Gap | Severity | Who/how to clear | Which ports it gates |
|---|---|---|---|
| `meta-signal-*` are concept-only stubs, not emitting contracts | **BLOCKER** | promote each `.concept.schema` → real `.schema` + `build.rs` + `GenerationPlan::wire_contract` (lojix already did this for `meta-signal-lojix`) | every two-listener port's META socket: router, orchestrate, mind, terminal, repository-ledger, upgrade, cloud, domain-criome, agent, persona |
| sema-engine has NO secondary-index / multi-key / append-log / predicate-filter; identified reads are point/range only; no identified multi-op atomic | **BLOCKER** (for 1:N ledgers) | trigger a live `ox7e` cycle on sema-engine (secondary-index/append/identified-commit primitive) OR build a porter-side index table via `Engine::storage_kernel()` | router (delivery_* by sequence, lookup by message-id, atomic message+delivery); orchestrate role/activity registries; any 1:N ledger |
| `LogVariant`/`RequestPayload`/`Frame` aliases emit only inside the streaming block | SOFT | declare a stream, hand-impl the 2 markers, or trigger an emitter fix to emit them unconditionally under `emits_signal()` | request/reply-only ports that reference those traits |
| No `subscribe_identified` (engine deltas are keyed-tables-only) | SOFT | publish at daemon layer (spirit pattern), model watched table as keyed, or `ox7e` an engine addition | any port wanting engine-level deltas on an identity table |
| Streaming push is per-component daemon glue (no macro) | SOFT | copy `spirit/src/subscription.rs` + `daemon.rs:148-182` | every subscribe port |
| Split-schema daemons need hand-written `plane.rs` From-glue (auto-emitted only for ComponentRuntime bootstrap) | SOFT | hand-write `plane.rs` (spirit does); candidate for `schema-core` | every split (3-file) daemon |
| `should_continue()` clean-stop only on the multi path | COSMETIC | use `MultiListenerDaemon` with one socket when supervised shutdown matters | single-socket supervised ports |
| Emitter internals mid-refactor; deps pinned `branch=main`; emitted text churns | COSMETIC | rely on `write_or_check` freshness gate; regenerate each bump | all ports |

## Net for the sweep

The **spirit-shape single-table request/reply OR daemon-layer-streaming port is fully
unblocked today** (the foundation carries it end-to-end). Two real blockers gate the
richer ports: (1) any component with a META/owner socket needs its `meta-signal-*`
concept stub promoted to a real emitting contract first (mechanical; lojix is the worked
example); (2) any component with a 1:N ledger or secondary-index need triggers a live
`ox7e` cycle on sema-engine. The per-component sweep classifies each remaining component
against these.
