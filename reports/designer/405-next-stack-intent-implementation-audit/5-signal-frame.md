# 405/5 — signal-frame: next-stack intent↔implementation audit

*Kind: Meta-report sub-audit · Topics: signal, signal-frame, schema, nota, mail-mechanism, rest, rust-discipline, audit, intent · 2026-05-28*

*Repo: `/git/github.com/LiGoldragon/signal-frame`. Audited at HEAD
`d61ebf25997c47c997c0dce1d576f870e3e8383c` ("signal-frame: constrain
schema boxed nota codecs") — matches the pinned commit, no drift. The
yardstick is the amalgamated psyche intent in `405/0` §1 plus the
audit-prompt items; not the repo's own ARCHITECTURE.md (itself audited
for drift below).*

## Verdict

signal-frame is a mature, well-typed wire substrate that gets the
*identity* and *REST-shape* halves of the intent right and the *mail
mechanism* half almost entirely wrong-by-omission. Message identity and
async correlation are first-class typed wire data
(`ExchangeIdentifier` / `LaneSequence` / `SessionEpoch` on every
`Request`/`Reply` frame variant), and the schema-driven generator
(`schema-rust` + `emit_schema!`) emits genuinely REST-shaped resource
operations (root resource + endpoint + route table + `Interact`
effect dispatch), proven end-to-end by `tests/emit_schema.rs`. But the
universal MAIL MECHANISM the intent demands — typed `MessageSent`
event, `on_sent` hook surface, reusable async mail-state manager, and a
DATABASE-STATE-MARKER slot on replies — is **completely absent**: zero
occurrences of message-sent / mail-state / state-marker anywhere in
`src/`. The intent (records 935/963/970, all dated 2026-05-27) assigns
the runtime mail-keeper + `on_sent` hook to **Nexus**, so the missing
*runtime manager* is arguably out of scope here; but record 935
explicitly pairs *signal-frame + mail + database marker*, and that
database-marker slot on `Reply` is a wire-type obligation this repo
owns and has not built. The repo's own ARCHITECTURE.md predates the
mail architecture and never mentions Nexus-as-mail-keeper, the
database marker, or `on_sent` — genuine intent drift. Separately, the
crate carries real method-only violations: 11 module-level free
functions across `frame.rs`/`caller.rs`/`namespace.rs` in the runtime
crate, plus ~70 more in the `macros` and `schema-rust` generator
crates. The single biggest schema-driven gap: signal-frame's OWN wire
spine (`Frame`/`Request`/`Reply`) is hand-written, and
`schema/signal-frame.concept.schema` is an orphan referenced by no
code — the crate is a schema-driven GENERATOR whose own substrate is
hand-written-with-schema-aside. `cargo test --workspace` passes (all
suites green, exit 0).

## Per-item classification

### Item 1 — Signal protocol = universal mail mechanism (records 935, 960-963)

**PARTIAL.** The identity-as-typed-data half is MET; the mail-mechanism
framing is MISSING.

- Message identity IS typed wire data, not ambient bookkeeping.
  `ExchangeIdentifier { session_epoch, lane, sequence }`
  (`src/exchange.rs:94-99`) is minted by the request frame and echoed by
  the reply frame; it rides inside the frame body as a structural field:
  `ExchangeFrameBody::Request { exchange, request }` and
  `Reply { exchange, reply }` (`src/frame.rs:51-58`). Correlation is
  therefore carried in the protocol, satisfying record 960's "message
  identity becomes typed data in the protocol."
- `StreamEventIdentifier` (`src/exchange.rs:119-124`) gives daemon-pushed
  events their own typed identity on the acceptor lane.
- BUT there is no notion of "the mail" as an object, no SENT-STATE
  lifecycle, and no mailer/dispatcher/push abstraction in this crate.
  Grep for `mail` / `MessageSent` / `dispatcher` / `mailbox` across
  `src/` returns nothing. The CLI client mints a **hardcoded** identity
  for every one-shot request — `CommandLineDispatch`'s
  `fn exchange()` returns `ExchangeIdentifier::new(SessionEpoch::new(0),
  ExchangeLane::Connector, LaneSequence::first())`
  (`src/command_line.rs:763-769`) — i.e. correlation IDs exist as types
  but nothing allocates or tracks them across messages.
- Reframe per `405/0` §1 and workspace `INTENT.md` §"Signal protocol":
  records 970/963 put the runtime mail keeper in **Nexus**, so the
  *runtime* mailer legitimately is not signal-frame's job. What IS
  signal-frame's job (record 935: "Communicate + signal-frame + mail +
  database marker") is the typed wire vocabulary the mailer rides on —
  identity (present) and a database marker on replies (absent, see
  item 4).

### Item 2 — Message-sent is an event surface with behavior (record 961)

**MISSING.** No typed `MessageSent` action, no `on_sent` hook point, no
subscriber/router commit surface tied to send. The only "event" surface
is `StreamingFrameBody::SubscriptionEvent` (`src/frame.rs:79-83`) and
the `ObservableSet` publish traits (`src/observable.rs:43-117`) — but
those fire on *executor* facts (`publish_operation_received` /
`publish_effect_emitted`), i.e. inbound-operation and committed-effect
moments, not on the message-SENT boundary. There is no method-on-message
that fires "as soon as the message is sent" (record 961). Per
`INTENT.md`, record 963 places the `on_sent` hook at the Signal→Nexus
handoff ("the on_sent hook fires when Signal hands mail TO Nexus"), so
the hook may belong to the Nexus boundary rather than signal-frame's
wire types — but nothing in signal-frame even names a send event for a
hook to attach to.

### Item 3 — Async at the data-type level; push not poll (records 962, 989)

**PARTIAL.** The push *primitives* exist; the push *manager* does not.

- Push direction is structurally present: `SubscriptionEvent` is a
  daemon-INITIATED frame variant (`src/frame.rs:77-83`) on the acceptor
  lane with its own monotonic `LaneSequence` — events are pushed, not
  polled. ARCHITECTURE.md §1 ("which channels emit pushed events") and
  the streaming-frame split reflect a push model.
- Correlation lives at the data-type level (item 1): `ExchangeIdentifier`
  is a field on the frame body, not runtime side-state.
- BUT there is no mail manager that pushes lifecycle transitions
  (sent / being-processed / replied). `LaneSequence::next()`
  (`src/exchange.rs:87-89`) is the only sequencing primitive, and
  *nothing in this crate calls it in a loop* — allocation and tracking
  are left to downstream daemons. The async state machine the intent
  describes (record 989 / Pattern A) is absent here.

### Item 4 — Reusable async mail-state manager + database marker on replies (record 930)

**MISSING (the crown gap).** This is the sharpest divergence from intent.

- No mail-state manager: no unique-message-identifier allocator, no
  handshake-state tracker, no response-correlation table. The handshake
  exists as wire records (`HandshakeRequest`/`HandshakeReply`,
  `src/version.rs:38-69`) but there is no stateful manager object that
  owns in-flight correlation.
- No database state marker on replies. `Reply<ReplyPayload>`
  (`src/reply.rs:36-50`) carries `AcceptedOutcome` / per-operation
  `SubReply`, and the closest thing to a durable-state signal is
  `CommitStatus { NotCommitted, Unknown }` (`src/reply.rs:162-170`) —
  which only says *whether* anything committed, never *what durable
  state counter/hash resulted*. Record 930 wants the reply to carry "what
  durable state counter/hash resulted so a client knows which request a
  reply answers + what durable state resulted." That slot does not exist
  on `Reply`.
- A `Revision` type DOES exist (`src/identity.rs:57-73`, "the per-row
  revision counter used by pre-condition checks") and `Slot<T>`
  (`src/identity.rs:26-42`) is a typed wire identity for a row — these
  are exactly the right raw materials for a database marker. But they are
  standalone primitives NOT threaded onto `Reply`; the wire response
  carries no revision/marker field. The building block is present; the
  obligation (marker-on-reply) is unmet.
- Against `405/0` §1 (record 1000: "no hand-written DatabaseMarker
  shims" — the marker must be a schema-emitted type): signal-frame has
  neither a hand-written nor a schema-emitted database-marker type.

### Item 5 — REST-shaped wire (record 951)

**MET (for generated contracts).** This is the strongest area.

- The schema-driven composer emits resource-shaped operations, not RPC
  calls. `schema-rust/src/lib.rs` `operation_items`
  (`schema-rust/src/lib.rs:195-246`) emits `Operation` as
  `RootResource(RootEndpoint)` nesting — a typed resource plus a typed
  endpoint operation — and a `route_for_short_header(leg, header) ->
  RouteDescriptor { leg, root_slot, endpoint_slot, root, endpoint, body }`
  (`schema-rust/src/lib.rs:430-485`). That is a REST resource/route
  table, not a flat method-call enum.
- Single-owner canonical-state semantics show up as the `EffectTable` +
  `Interact`/`InteractionActor` scaffold
  (`schema-rust/src/lib.rs:305-325`, `327-428`): an operation maps to an
  effect via `impl From<Operation> for Effect` and `EffectTable::interact`
  returns a `FanOut`. Resource operation in, effect out.
- Proven end-to-end: `tests/emit_schema.rs:24-34` instantiates
  `Operation::State(StateEndpoint::Declaration(Declaration { .. }))` from
  a real `.schema` and checks the route table and short-header
  projection. `route.root == "State"`, `route.endpoint == "Declaration"`
  (`tests/emit_schema.rs:15-17`).
- Caveat: the REST shape applies to the operation types the composer
  GENERATES for downstream contracts. signal-frame's own frame spine is
  request/reply-shaped (correct for a transport), so item 5 is judged on
  the generated contract surface, where it is cleanly met.

### Item 6 — Schema-driven (the stack premise + the pinned commit)

**DIVERGENT.** The schema-driven path is real and substantial, but
signal-frame's OWN substrate is hand-written and its concept schema is
orphaned.

- The genuine schema-driven path: `emit_schema!`
  (`macros/src/schema_entry.rs:21-30`) flows
  `schema::LoadedSchema::read_path` → `schema_rust::RustComposer::compose`
  → tokens. `schema-rust/src/lib.rs` is an 858-line composer lowering an
  `AssembledSchema` into types, Operation/OwnerOperation/SemaOperation
  enums, `LogVariant` impls, Reply/Event enums, Effect/FanOut/EffectTable,
  `Interact` traits, `ExtendedHeader`, and route tables. This is
  not aspirational — `tests/emit_schema.rs` exercises it and passes.
- BUT signal-frame's own wire spine is entirely hand-written Rust:
  `Frame`/`ExchangeFrameBody` (`src/frame.rs:47-96`),
  `Request<Payload>` (`src/request.rs:31-35`), `Reply<ReplyPayload>`
  (`src/reply.rs:36-50`), exchange identifiers, handshake. None of `src/`
  invokes `emit_schema!` or `signal_channel!` (grep confirms only doc
  comments reference them). The spine cannot bootstrap itself through the
  generator because the generator depends on it (`signal_frame::LogVariant`,
  `signal_frame::ShortHeader` are referenced in emitted code,
  `schema-rust/src/lib.rs:237`, `474-477`).
- `schema/signal-frame.concept.schema` is an ORPHAN. Grep for
  `concept.schema` across all `.rs`/`.toml` returns nothing — no code or
  test reads it. Worse, it is *stale*: it declares `Frame (ShortHeader
  Payload)` and `Reply (Frame)` (`schema/signal-frame.concept.schema:10,15`),
  whereas the real `ExchangeFrameBody` has four variants including
  handshake and a structural `exchange` field, and `Reply` is a typed
  Accepted/Rejected sum. The concept schema is an aspirational
  side-artifact that no longer matches the hand-written truth.
- The pinned commit ("constrain schema boxed nota codecs") narrows the
  channel macro's boxed-NOTA-codec emission to only the schema types
  reachable from request payloads, via a new
  `request_payload_schema_names` reachability walk
  (`macros/src/emit.rs:977-1013`, added in `d61ebf2`). It also splits one
  glob `compile_fail` into nine explicit cases
  (`tests/channel_macro_compile_fail.rs:3-12`) and deletes the
  now-obsolete `schema_input_rejected` UI fixture. The commit is a
  correctness tightening of the GENERATOR, and reinforces that the
  schema-driven work targets downstream contracts, not the spine.

Against the orchestrator yardstick (record 1000: "schema-emitted Rust
types are the canonical type for *every type that appears in the
system*"), signal-frame's spine is the clearest counter-example in the
stack: the most-depended-on wire types are hand-authored.

### Item 7 — Method-only Rust; no ZST namespace holders; no free functions (records 712, 882, 881)

**DIVERGENT.** Real violations in the runtime crate, heavier ones in the
generator crates.

Runtime crate (`src/`), genuine module-level free functions outside
`#[cfg(test)]`/`fn main`:

- `src/frame.rs:156` `encode_archive`, `:165` `length_prefix`, `:176`
  `strip_length_prefix`, `:191` `pub short_header_from_archive`, `:200`
  `pub short_header_from_length_prefixed`, `:204` `encode_frame_archive`,
  `:215` `strip_short_header` — 7 free functions. These are orphan codec
  logic that should be associated functions on `ShortHeader` (the header
  parsers) or on a frame-codec noun (the encode/strip helpers); the two
  `pub` ones are re-exported in `lib.rs:53-54` as crate API.
- `src/caller.rs:105` `parent_executable`, `:109` `parent_start_time`,
  `:114` `start_time_ticks` — 3 free functions reading `/proc`; these
  belong on `Caller` (the `/proc` walk) and on a `ProcStat`-style noun
  (`start_time_ticks` parses a stat line — invent the noun).
- `src/namespace.rs:32` `pub const fn classify` — 1 free function that is
  the exact "free function in disguise" anti-pattern: `NamespaceSection::classify`
  (`src/namespace.rs:42`) already exists and just delegates to it. The
  free function is redundant and should be deleted, with callers using
  the inherent method.

Generator crates (`macros/`, `schema-rust/`) — same rule, larger scale:

- `schema-rust/src/lib.rs`: 21 module-level free functions (all above the
  `#[cfg(test)]` boundary at line 836), e.g. `module_name_for_schema`
  (`:542`), `routes_for_leg` (`:565`), `enum_variant_tokens` (`:679`),
  `type_expression_tokens` (`:715`), `primitive_tokens` (`:738`),
  `route_descriptor_tokens` (`:751`), `type_ident` (`:806`). The
  composer's logic lives almost entirely in free functions rather than on
  `RustComposer` or on schema-noun impls (e.g. `primitive_tokens` is a
  textbook `impl From`-or-method-on-`Primitive` candidate).
- `macros/src/emit.rs`: 48 module-level free functions (the file has no
  test module). `macros/src/schema_reader.rs`: 17. `macros/src/validate.rs`:
  10 (`validate.rs:10-17` etc.). `macros/src/lib.rs:68-92` and
  `schema_entry.rs:14,21,68,79` add more.
- Proc-macro internal helpers are a softer target than runtime API, but
  the discipline (`skills/rust/methods.md`) draws no proc-macro exemption,
  and the composer especially carries domain nouns (`SchemaType`,
  `Primitive`, `Route`, `RootRoutes`) that the free functions operate on
  from the outside.

ZST check: no illegitimate ZST namespace holders found in `src/`. The
generated `EffectTable` is a unit struct used as a real `Interact` impl
receiver (`schema-rust/src/lib.rs:410-425`) — it carries dispatch
identity, not a namespace, so it passes. `PhantomData` uses
(`Slot<T>` `src/identity.rs:27`, `CommandLineDispatch`
`src/command_line.rs:230`) are legitimate type-parameter markers.

### Item 8 — NOTA discipline: bracket strings only, no emitted quotes

**MET.** No quote-emission found. Grep for escaped-quote literals across
`src/`, `macros/src/`, `schema-rust/src/` returns nothing. The codecs
delegate string emission to `nota_codec`'s `Encoder` (`src/request.rs:145-156`,
`src/command_line.rs:743-760`), which per the workspace override
structurally cannot emit `"`. The boxed-NOTA-codec path in the pinned
commit (`macros/src/emit.rs:1022+`, `emit_boxed_nota_codec`) routes field
encode/decode through `::nota_codec::NotaDecode` and
`::nota_box::decode_binary_box` — no raw quote characters, brackets only.
`Request`'s NOTA codec emits sequences via `encoder.start_seq()` /
`end_seq()` (`src/request.rs:149-153`), i.e. bracket forms. (Minor note:
`nota_box` is not a declared dependency at the workspace/macro Cargo
level; the boxed codec emits `::nota_box::...` paths that the downstream
contract crate must provide — a generation-time assumption, not a
NOTA-discipline violation.)

## Crown findings

**(a) Does signal-frame implement the universal mail mechanism?**
No — it is aspirational and lives only in spirit-next / the intent log,
not here. signal-frame provides the *identity* substrate the mechanism
would ride on (`ExchangeIdentifier`, `LaneSequence`, push-shaped
`SubscriptionEvent`) but none of the mechanism itself: no `MessageSent`
event (item 2), no `on_sent` hook (item 2), no async mail-state manager
(item 4), and — the obligation this repo most clearly owns per record
935 — no database-state-marker slot on `Reply` (item 4). The raw
materials for the marker exist as unused standalone types (`Revision`,
`Slot<T>`, `src/identity.rs`). The intent that defines all of this
(records 935/960-963/970/989) is dated 2026-05-27; HEAD is 2026-05-25 and
ARCHITECTURE.md never mentions mail / Nexus-as-keeper / `on_sent` /
database-marker — so this is intent that has simply not landed yet, not
intent that was implemented and diverged.

**(b) Is the wire genuinely schema-driven or hand-written-with-schema-aside?**
Both, split by audience. The schema-driven generator (`schema-rust` +
`emit_schema!`) is real, tested, and REST-shaped — for the DOWNSTREAM
contracts it emits. signal-frame's OWN wire spine
(`Frame`/`Request`/`Reply`/handshake/exchange) is hand-written, and its
`schema/signal-frame.concept.schema` is an orphaned, stale side-artifact
referenced by no code. So the crate is a schema-driven generator whose
own substrate is hand-written-with-schema-aside — directly counter to the
orchestrator yardstick (record 1000) that every type in the system be
schema-emitted.

## Top gaps (ranked)

1. **No database-state-marker slot on `Reply`** (item 4, record 935).
   The one mail-mechanism obligation signal-frame unambiguously owns
   (vs Nexus). `Reply` carries no durable state counter/hash; `Revision`
   and `Slot<T>` exist (`src/identity.rs`) but are not threaded onto the
   reply. Highest-priority because it is in-scope-here AND unbuilt.

2. **Mail-mechanism intent (records 935/960-963/970/989) has not landed
   at all** (items 1-4). No `MessageSent` event, no `on_sent` hook
   surface, no async mail-state manager. ARCHITECTURE.md predates and
   omits the entire mail-keeper / Nexus framing — the repo's synthesised
   docs are drifted from current psyche intent and need a sweep even if
   the runtime manager ends up living in Nexus.

3. **Spine is hand-written, concept schema is orphaned + stale**
   (item 6, record 1000). `schema/signal-frame.concept.schema` is read by
   no code and no longer matches `src/frame.rs`/`reply.rs`. Either delete
   it as misleading, or make the spine schema-emitted to honor
   "every type schema-emitted." At minimum the orphan should not pose as
   the contract.

4. **11 method-only violations in the runtime crate** (item 7, records
   712/882). `src/frame.rs` (7 free fns incl. 2 `pub` API),
   `src/caller.rs` (3), `src/namespace.rs` (1 redundant with its own
   inherent method). These are the in-scope, ship-as-API violations;
   relocate onto `ShortHeader` / `Caller` / a frame-codec noun.

5. **~70 method-only violations in the generator crates** (item 7).
   `macros/src/emit.rs` (48), `schema_reader.rs` (17),
   `schema-rust/src/lib.rs` (21), `validate.rs` (10). Lower priority
   (proc-macro internals) but the composer operates on real schema nouns
   that should own the logic; large surface to migrate.

6. **CLI mints a hardcoded exchange identity** (item 1/3,
   `src/command_line.rs:763-769`). `fn exchange()` always returns epoch
   0 / Connector / sequence 0 — fine for one-shot CLI today, but it means
   the identity substrate is unexercised by any allocator/tracker, which
   is why the mail-state-manager gap (gap 2) has no pressure to close.
