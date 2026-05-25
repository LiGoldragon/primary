# Skill — schema-driven actors

*How to author an actor schema. The actor-schema pattern is ACTION
enum + RESPONSE enum + universal `Unknown` safety floor + authored
EffectTable + authored FanOutTargets — declared in NOTA, lowered
through the schema crate, projected into Rust by the schema-rust
composer, consumed by hand-written engine logic.*

## What this skill is for

Use this skill when **authoring a new actor schema** or extending
an existing one. The actor-schema pattern is the next-substrate
discipline for persona daemons: each major internal-channel actor
declares its own `.schema` file as a channel-contract per the
schemas-warrant-per-channel principle (workspace `INTENT.md` §"The
schema-driven stack").

Use `skills/actor-systems.md` for the runtime actor discipline
(typed mailboxes, supervision, trace witnesses). This skill is
specifically about the **schema authoring + engine pattern** that
the schema-driven substrate uses.

## The pattern

Every actor schema declares two enums plus a universal variant:

```nota
;; spirit-recorder.schema (excerpt)
{
  RecorderAction (
    RecordEntry
    ObserveRecorder
    SnapshotRecords
    OpenRecordSubscription
    CloseRecordSubscription
    QueryStatus
  )
  RecorderResponse (
    RecordAccepted
    RecordsObserved
    RecordSnapshotReturned
    SubscriptionOpened
    SubscriptionRetracted
    StatusReturned
  )                                         ;; Unknown injected by macro

  ;; payloads
  RecordEntry [Entry]
  ObserveRecorder [QueryFilter]
  ;; ...
}

[
  (EffectTable [
    (RecordEntry RecordWriteEffect)
    (OpenRecordSubscription SubscriptionOpenEffect)
    (CloseRecordSubscription SubscriptionCloseEffect)
  ])
  (FanOutTargets [
    (RecordWriteEffect [
      (Store SpiritStorage InsertStampedEntry)
      (Notify ObserverSet PublishRecordCaptured)
      (Reply RecordAccepted)
    ])
  ])
]
```

Two structural commitments:

1. **ACTION enum** — the closed set of things this actor can do
   when called. Author writes this. There is no universal
   `Unknown` on the action side — the action enum is closed.
2. **RESPONSE enum** — the closed set of things this actor can
   say back. Author writes the non-Unknown variants; the schema
   engine's `UniversalUnknownMacro` injects `Unknown(String)`
   automatically. Universal Unknown is the **actor's safety
   floor**.

Plus authored features:

- **`EffectTable`** — closed mapping from ACTION variants to
  effect type names.
- **`FanOutTargets`** — per-effect closed set of fan-out outputs.
  Three output kinds: Actor (`(MethodTag ActorType ActorMethod)`),
  Reply (`(Reply ResponseVariant)`), Subscribers
  (`(FanOutSubscribers ActorType DispatchMethod)`).
- **`StorageDescriptor`** (storage schemas only) — closed set of
  `(logical_name table_type)` redb table entries.

## Naming the response enum — the `*Response` suffix matters

The universal-Unknown injection only fires on local enums whose
name **ends in `Response`**. If the actor's response enum is named
`RecorderOutput` or `RecorderReply`, the injection skips it.
**Always name the response enum `<Actor>Response`.** This is the
suffix the `UniversalUnknownMacro::is_response_enum_name`
predicate matches; renames break the safety floor silently.

If you have a legitimate `*Response` enum that should NOT receive
the universal Unknown — rare — the schema-side guard is structural
(record bodies and aliases are skipped), so a `*Response` record
declaration is safe. Avoid naming non-enum types `*Response` to
keep the rule clean.

## Structure is schema; logic is Rust

The engine code consumes schema-emitted types and writes only
logic. Hand-written Rust is ONLY the decision-making bodies inside
actor methods:

```rust
pub fn handle(&self, action: RecorderAction) -> RecorderResponse {
    match action {
        RecorderAction::RecordEntry(entry) => self.record_entry(entry),
        RecorderAction::ObserveRecorder(filter) => self.observe(filter),
        RecorderAction::SnapshotRecords(filter) => self.snapshot(filter),
        RecorderAction::OpenRecordSubscription(p) => self.open_subscription(p),
        RecorderAction::CloseRecordSubscription(c) => self.close_subscription(c),
        RecorderAction::QueryStatus => self.status(),
        // No Unknown arm --- the action enum is closed.
    }
}

fn record_entry(&self, entry: Entry) -> RecorderResponse {
    match self.store.insert(entry) {
        Ok(summary) => RecorderResponse::RecordAccepted(summary),
        Err(e) => RecorderResponse::Unknown(e.to_string()),
    }
}
```

The outer `match` is exhaustive because the action enum is closed;
Rust enforces this at compile time. Any error path inside a method
returns `<Actor>Response::Unknown(error_string)` rather than
panicking. The Unknown variant is structurally valid by
construction.

**Do not reinvent data structures.** If a payload type is needed,
declare it in the schema's namespace section; consume the emitted
type. Hand-written struct/enum declarations that duplicate
schema-emitted types are a discipline break.

## The three FanOutOutputDeclaration kinds

When authoring `FanOutTargets` rows, pick the right output kind:

| Output kind | NOTA shape | When |
|---|---|---|
| Actor | `(MethodTag ActorType ActorMethod)` | The fan-out dispatches a method-tagged message to a named actor (e.g. storage write, notification publish). The first token is the method tag (e.g. `Store`, `Notify`, `Drain`); the second is the actor type; the third is the actor method to invoke. |
| Reply | `(Reply ResponseVariant)` | The fan-out materialises as a wire reply variant. Use when the actor's response feeds back to the original caller. |
| Subscribers | `(FanOutSubscribers ActorType DispatchMethod)` | The fan-out dispatches into a subscriber set rather than a single named actor. Use for publish/notify patterns. |

The Actor form is the default; recognized by the parser as the
fallback when the first token is not `Reply` or `FanOutSubscribers`.
This is the only open-by-convention surface in the dispatch; the
closed parts are guarded by explicit literal matches.

## The reading-actor + auto-tap pattern

The response dispatcher in a schema-driven daemon is itself an
actor — the **reading actor** — with its own schema. Its action
vocabulary is dispatch-by-response-type
(`DispatchRecorderResponse`, `DispatchObserverResponse`, etc).
Its fan-out targets ALWAYS include a `(Tap LogSinkSet WriteEntry)`
row; the auto-tap to a logging facility is schema-declared, not
runtime convention. Every response is captured; nothing is
invisible.

When authoring a new reading-actor variant or extending the
existing one, keep the `(Tap LogSinkSet WriteEntry)` row on every
DispatchEffect's FanOutTargets. The tap is structural — losing it
loses observability.

## The rkyv-one-format discipline

The rkyv binary encoding of every schema-emitted type lives in a
**single byte layout** that survives both:

- **Sema** — the body at rest in redb (state surviving process
  exit).
- **Signal** — the body in transit on a socket (channel between
  clients).

Same bytes, two homes. NOTA is the text-readable projection
emitted at CLI read time or for human inspection. When you
serialize an actor's response into a wire reply, you're using the
same byte layout the daemon would use to persist the response to
disk if it wanted to. **Don't hand-author a second codec.** The
schema-emitted rkyv codec is the canonical encoding.

## Storage schemas + auto-migration

When authoring a storage schema, declare:

- The redb table types in the namespace section.
- The `VersionMarker [u32 u32 u32]` namespace declaration (or
  equivalent) — load-bearing for the auto-migration runner.
- `(StorageDescriptor [ (LogicalName TableType) ... ])` feature
  naming the tables.

The daemon's `<Store>Handle::open(path)` function reads the
on-disk version marker and runs the three-branch migration match:

| Branch | Behaviour |
|---|---|
| `None` (fresh DB) | Write NEXT marker; log `NoMigrationNeeded`. |
| `Some(NEXT)` (already up to date) | No-op; log `NoMigrationNeeded`. |
| `Some(previous)` (older marker) | Run `run_migration` bridge; write NEXT on success; log outcome. |

`run_migration` is hand-written per version-boundary; when the
schema diff is empty, the bridge body is elided.

## The next/main/previous vocabulary

Authors always write from the point of view of **NEXT**.

- **NEXT** = the in-progress version being authored.
- **MAIN** = the current published baseline (imported as
  comparison).
- **PREVIOUS** or **LAST** = the prior iteration.

In the daemon source, use `mod next` and `mod previous` for the
migration bridge module names (renamed from the older
`mod historical` / `mod current_shape` per record 672). The
8-byte ShortHeader prefix preservation discipline IS this vocabulary
applied at the wire layer — byte 0 of NEXT preserves byte 0 of
MAIN.

## What still defers — cross-crate import resolution

When an actor schema needs to import types from a sibling crate
(`signal-persona-spirit/spirit.schema` from
`persona-spirit/spirit-recorder.schema`, etc.), the current
`LoadedSchema::read_path` resolver can't follow the import. The
workaround until the proc-macro's resolution algorithm lands:
hand-written Rust types that match what `emit_schema!` will emit
once the resolver supports cross-crate paths.

This is the lowest-leverage deferral — the actor engines, the
migration runner, the universal Unknown floor, the full
compile-time chain for any single schema, and the dual-emission
wire-side — all work today against the hand-written types.

## Anti-patterns

- **Naming the response enum `<Actor>Output` or `<Actor>Reply`.**
  The universal-Unknown injection skips it; the actor loses its
  safety floor. Always `<Actor>Response`.
- **Adding `Unknown` to the ACTION enum.** Actions are closed; the
  caller cannot legally send Unknown. Universal Unknown lives on
  the response side only.
- **Hand-authoring duplicate type declarations.** If a type is
  declared in the schema's namespace, consume the emitted type.
  Don't declare a parallel Rust enum with the same shape.
- **Computing dispatch instead of matching.** *Match always; map
  always; never compute when you can match.* If the engine is
  doing string parsing or runtime type checks to choose an effect,
  the EffectTable is missing an entry — add it to the schema.
- **Skipping the auto-tap in a reading actor.** The
  `(Tap LogSinkSet WriteEntry)` row on every DispatchEffect's
  FanOutTargets is what makes the observability discipline hold.

## See also

- `skills/actor-systems.md` — the workspace's runtime actor
  discipline (typed mailboxes, supervision, trace witnesses).
- `skills/component-triad.md` — the triad-shape framework this
  pattern lives inside.
- `skills/nota-design.md` — the NOTA encoding conventions actor
  schemas use.
- `repos/schema/INTENT.md` — the parse + lowering substrate intent.
- `repos/signal-frame/INTENT.md` — the composer's responsibility.
- `repos/persona-spirit/INTENT.md` — the daemon-side schema-
  driven actor architecture (first worked example).
