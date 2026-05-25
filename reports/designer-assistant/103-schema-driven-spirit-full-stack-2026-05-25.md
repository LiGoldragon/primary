# 103 — schema-driven full-stack spirit implementation

*Designer-lane subagent dispatch 2026-05-25 implementing the
schema-driven full-stack pattern for `persona-spirit` per psyche
directive. Authority: /345 (multi-schema-per-crate), /346 (actor
schemas + upgrade mechanism), /343 (EffectTable / FanOutTargets — with
/345 §8 correction), /341 (the seven crystallized principles). Intent
records 656-696 are load-bearing; no new captures.*

## Summary

| Repo | Branch | Worktree path | What landed | What's blocked |
|---|---|---|---|---|
| `signal-persona-spirit` | `designer-schema-full-stack-spirit-2026-05-25` | `/home/li/wt/github.com/LiGoldragon/signal-persona-spirit/designer-schema-full-stack-spirit-2026-05-25` | Documentation note in src/lib.rs describing the planned migration `signal_channel!([schema])` -> `emit_schema!()` per /345 §11 item 7; no schema split needed (owner is a sibling crate) | Migration itself gated on downstream qualified-path switch (`spirit::Operation` module wrapper) |
| `persona-spirit` | `designer-schema-full-stack-spirit-2026-05-25` | `/home/li/wt/github.com/LiGoldragon/persona-spirit/designer-schema-full-stack-spirit-2026-05-25` | Six new .schema files (storage, recorder, observer, supervisor, reading-actor, upgrade-log); src/schema_driven/ Rust engine stubs showing the actor pattern from /346 §2 | Composer extensions in signal-frame/schema-rust + schema crate (per /346 §8 items 16-22) |
| `signal-frame` | `designer-schema-full-stack-spirit-2026-05-25` | `/home/li/wt/github.com/LiGoldragon/signal-frame/designer-schema-full-stack-spirit-2026-05-25` | Documentation note in macros/src/schema_entry.rs describing the three invocation forms; existing LitStr-path parameter is already structurally sufficient | EffectTable + FanOutTargets + StorageDescriptor + UniversalUnknown emission in schema-rust composer |
| `schema` | `designer-schema-full-stack-spirit-2026-05-25` | `/home/li/wt/github.com/LiGoldragon/schema/designer-schema-full-stack-spirit-2026-05-25` | Three new `Feature` variants (`EffectTable`, `FanOutTargets`, `StorageDescriptor`) with their typed supporting structs; sketch of `UniversalUnknownMacro` builtin in engine.rs | Full wiring (multi-pass NOTA parsers for the new features; post-pass `LoweringContext::finalize_universal_unknowns()` hook; idempotent injection helper on `DeclarationBody::Enum`) |

## What's in each branch

### signal-persona-spirit branch

Minimal scope per the prompt's "Likely small changes" guidance. The
current wire spirit.schema is already correctly shaped (single wire
channel; owner is in the sibling `owner-signal-persona-spirit` crate);
the multi-schema-per-crate convention from /345 §4 does NOT split this
crate.

`src/lib.rs` now imports both `signal_channel` (current) and
`emit_schema` (target); a comment block documents the planned switch
and explicitly flags that downstream code must adopt the
`signal_persona_spirit::spirit::*` qualified module path because
`emit_schema!` wraps emissions in `pub mod spirit { ... }`. That code
migration is operator territory; this branch documents the intent and
keeps the import staged.

### persona-spirit branch

The big-leverage branch. Six new .schema files:

- `spirit-storage.schema` — storage contract (redb table layouts as
  schema declarations); mirrors the current
  `StoredRecord`/`StampedEntry`/`RecordIdentifierMint` shapes from
  `src/store.rs`; includes a `VersionMarker` namespace declaration +
  `StorageDescriptor` feature
- `spirit-recorder.schema` — internal channel for the recorder actor;
  `RecorderAction` (RecordEntry / ObserveRecorder / SnapshotRecords /
  OpenRecordSubscription / CloseRecordSubscription / QueryStatus) +
  `RecorderResponse` (RecordAccepted / RecordsObserved /
  RecordSnapshotReturned / SubscriptionOpened / SubscriptionRetracted /
  StatusReturned); `EffectTable` + `FanOutTargets` features wiring
  actions to storage-side effects per /345 §8 correction
- `spirit-observer.schema` — observer fan-out hub actor; observer
  ACTION+RESPONSE; effect-table for subscription open/close + publish
- `spirit-supervisor.schema` — supervisor's lifecycle actions; effect
  fan-out into recorder/observer/storage drain orchestration
- `spirit-reading-actor.schema` — response dispatcher actor per /346
  §5; its own action+response set; auto-tap to logging facility
- `spirit-upgrade-log.schema` — separate storage contract for the
  upgrade ceremony log per /346 §4 step 6

Plus `src/schema_driven/` Rust engine stubs (one file per actor +
storage stub) demonstrating the /346 §2 pattern (structure is schema;
logic is Rust). The stubs:

- Use the schema-emitted ACTION + RESPONSE enums (commented as BLOCKED
  imports)
- Show the match-block contact point between ACTION and RESPONSE
- Document the universal `Unknown` floor variant per /346 §1
- Carry BLOCKED markers at every spot the composer extensions are
  needed (per file + per method)

The new module is added to `src/lib.rs` as `pub mod schema_driven`;
existing `src/actors/*` remain on MAIN's path and continue to ship.

### signal-frame branch

Documentation note in `macros/src/schema_entry.rs` describing the
three invocation forms of `emit_schema!()`. The proc-macro already
accepts an optional `LitStr` path argument structurally (lines 52-65);
this branch's contribution is making the multi-schema-per-crate use
case explicit in the docstring so a reader can find their way to
`emit_schema!("spirit-recorder.schema")` for an internal-channel
schema.

The composer side (`schema-rust/src/lib.rs::module_name_for_schema`)
already derives the Rust module name from the schema file stem
correctly (`spirit-recorder.schema` -> `pub mod spirit_recorder`) so
the structural foundation for multi-schema-per-crate is intact today.

What this branch does NOT do (deliberately out of scope; would
overlap operator's composer work): emit the new EffectTable +
FanOutTargets + StorageDescriptor + UniversalUnknown Rust types. That
work consumes the schema crate's new Feature variants and adds to
the 857-line schema-rust composer.

### schema branch

Three new `Feature` enum variants in `src/feature.rs`:

- `Feature::EffectTable(EffectTableFeature)` — closed action→effect
  mapping; entries are `(action_name, effect_type_name)` pairs
- `Feature::FanOutTargets(FanOutTargetsFeature)` — per-effect fan-out
  outputs; each output is one of three closed kinds
  (`FanOutOutputDeclaration::Reply { variant }`,
  `::Actor { method_tag, actor_type, actor_method }`,
  `::Subscribers { actor_type, dispatch_method }`)
- `Feature::StorageDescriptor(StorageDescriptorFeature)` — closed set
  of `(logical_name, table_type)` entries

Plus all the supporting typed structs (`EffectTableEntry`,
`FanOutTargetsEntry`, `FanOutOutputDeclaration`,
`StorageDescriptorEntry`) with constructor + getter methods.

`src/lib.rs` now re-exports the new types.

`src/engine.rs` carries a sketch of the `UniversalUnknownMacro`
builtin per /346 §9:

- `is_response_enum_name(name)` — shape-logic predicate
  (`name.ends_with("Response")`)
- `body_is_enum(body)` — only injects into closed enums
- `UNKNOWN_VARIANT_NAME` — the universal constant "Unknown"
- `inject_unknown_into_enum_body_template` — idempotent injection
  body (pseudocode; needs `Variant::new` public helper)

What's NOT done (operator territory): multi-pass NOTA parsers for
the new feature syntaxes, the post-pass
`LoweringContext::finalize_universal_unknowns()` hook, the actual
mutation helper on `DeclarationBody::Enum`. The feature variants are
authored so downstream code can REFERENCE them while the parsing +
finalization paths are filled in.

## Worktrees created (for tracking per intent 633)

- `/home/li/wt/github.com/LiGoldragon/signal-persona-spirit/designer-schema-full-stack-spirit-2026-05-25`
- `/home/li/wt/github.com/LiGoldragon/persona-spirit/designer-schema-full-stack-spirit-2026-05-25`
- `/home/li/wt/github.com/LiGoldragon/signal-frame/designer-schema-full-stack-spirit-2026-05-25`
- `/home/li/wt/github.com/LiGoldragon/schema/designer-schema-full-stack-spirit-2026-05-25`

All four are jj workspaces tracking branches pushed to GitHub. PR
URLs offered by `jj git push` (not opened; operator initiates PR
when integration cycle starts).

## What operator needs to land next

Ordered list of composer / emit_schema! extensions needed to make
this substrate actually compile end-to-end:

1. **`schema` crate — multi-pass parsers for the three new feature
   forms** (`(EffectTable ...)`, `(FanOutTargets ...)`,
   `(StorageDescriptor ...)`). Currently the schema-document parser
   walks the features sequence position by position; the new
   builtins need shape-logic dispatch entries in
   `multi_pass.rs::FeatureMacroPipeline`.

2. **`schema` crate — wire up `UniversalUnknownMacro` as a
   post-lowering pass**. Add `LoweringContext::finalize_universal_unknowns(&mut self)`
   that walks `self.types`, identifies any local enum whose name ends
   in `Response`, and idempotently injects an `Unknown(String)`
   variant via a public `Variant::new(name, payload)` helper. Call
   the hook from the pipeline AFTER all `TypeMacro` invocations but
   BEFORE `LoweringContext::finish()`.

3. **`signal-frame/schema-rust` — emit Rust for the three new
   features**. The current composer emits route-derived `Effect`,
   `EffectTable`, `FanOut`, `FanOutOutput` enums (line 79+); these
   need to switch from route-derivation to authored-feature
   consumption when the schema declares the new variants. Plus
   `pub struct StorageDescriptor` + `TableDescriptor` items from
   `StorageDescriptor` feature.

4. **`signal-frame/schema-rust` — composer module-name behavior
   for multi-schema invocations is already correct** (file-stem
   derivation at line 542); just need to verify the test suite
   covers the new multi-schema fixture (e.g. add a
   tests/fixtures/recorder.schema + emit_schema test in
   signal-frame/tests/emit_schema.rs).

5. **`persona-spirit` — wire the daemon to consume the schemas**.
   Once the composer emits the actor enums + the
   `StorageDescriptor`, the existing `SpiritStore` in `src/store.rs`
   migrates to schema-emitted `RecordsTable::descriptor()`. The
   existing `src/actors/store.rs` + `src/actors/pipeline.rs`
   migrate to consume `RecorderAction`/`RecorderResponse` instead of
   the current hand-written `CaptureEntry`/`ObserveRecords` shapes.
   Cross-component dependency: the upgrade machinery from /346 §4
   reads the `VersionMarker` from spirit-storage.schema, so /338 §8
   `primary-cklr` integrates here too.

6. **`persona-spirit` — auto-migration runner**. Add the daemon
   startup path that reads version marker, routes through
   `mod previous` bridge code if needed, writes marker forward. Per
   /346 §4 step 6. Likely lives in `src/store.rs` (or moves into
   `src/schema_driven/storage.rs` once activated).

7. **`signal-persona-spirit` — flip the switch**. Replace
   `signal_channel!([schema])` with `emit_schema!()` and migrate every
   downstream `signal_persona_spirit::Foo` import to
   `signal_persona_spirit::spirit::Foo`. This is the breaking change
   the documentation note flags; sequence after item 3 so the
   emit_schema output is structurally complete.

## Anomalies / judgement calls

1. **persona-spirit's worktree was rolled back mid-session.** The
   `jj workspace add` + subsequent edits were interrupted by a
   concurrent `jj` operation (likely the bookmark moves), and the
   worktree's working copy reset to the empty designer commit. I
   re-applied all six schemas + the six Rust stubs from the in-context
   buffer; the final pushed commit `1320ad79` carries the full
   substrate.

2. **`signal-persona-spirit` schema did NOT split into
   wire + owner-spirit.** The prompt suggested possibly splitting
   `owner-spirit.schema` out from `spirit.schema` IF an owner-channel
   should be its own schema. Investigation showed the owner channel
   ALREADY has its own crate (`owner-signal-persona-spirit/`) with
   its own schema. Per the triad rule
   (`skills/component-triad.md`) the wire/owner separation is
   already enforced at the crate boundary. Multi-schema-per-crate
   doesn't apply here — this crate is single-channel.

3. **Did not migrate `signal_channel!([schema])` to `emit_schema!()`
   on the signal-persona-spirit branch.** The migration would break
   every downstream consumer of `signal_persona_spirit::Operation` /
   `::Reply` / etc. because `emit_schema!` wraps emissions in
   `pub mod spirit`. That's an across-the-board API rewrite — best
   sequenced as operator work AFTER the composer extensions land
   (item 7 in "what operator needs to land next"). The branch
   documents the intent + stages the `emit_schema` import.

4. **Did not write composer extensions in signal-frame/schema-rust.**
   Per the prompt's time-budget priority list, "Composer extensions in
   signal-frame (only if reachable)" was item 4. The 857-line
   composer + the not-yet-existent multi-pass parsers for the new
   feature variants would constitute substantial operator-scope
   work. Authored the Feature variants in the schema crate (so the
   types are visible) + the docstring update in macros/src/schema_entry.rs
   (so the multi-schema convention is documented) but stopped short
   of emitting Rust from the new features.

5. **Did not implement the universal-Unknown injection itself.**
   Sketched the `UniversalUnknownMacro` struct + the predicates +
   the constant in `engine.rs`. The actual injection requires
   public helpers (`Variant::new` constructor, `DeclarationBody::Enum`
   mutation) that I judged better landed as part of an operator pass
   that touches the pipeline finalize hook. Per `skills/architecture-editor.md`
   §"Carrying uncertainty" the sketch makes the intent visible without
   forcing the implementation shape now.

6. **`(divergent)` jj markers.** The worktree-update conflicts left
   some commits with the `(divergent)` annotation. Each branch's
   tip commit is unique on its own bookmark; the divergence marker
   refers to the change-id history, not to branch state. Pushes
   succeeded cleanly to GitHub.

7. **Schema file syntax may not literally parse** without the
   composer extensions (the `(EffectTable ...)`, `(FanOutTargets ...)`,
   `(StorageDescriptor ...)` feature variants need their multi-pass
   parsers per "operator landing item 1"). The schemas are written
   AS IF the parsers exist; if `LoadedSchema::read_path` is invoked
   on them today it would error. The schemas serve dual purpose: (a)
   the canonical authored-form to drive the composer extension work,
   (b) live documentation of the channel-contract shape per actor.
   Per /346 §10 worked example this is the intended flow — the
   schema files lead, the composer follows.
