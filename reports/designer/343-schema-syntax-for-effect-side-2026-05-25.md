# 343 — schema syntax for the effect side: authored effect-table + fan-out targets

## Frame

Operator/185 landed all seven crystallized principles' RUNTIME SCAFFOLDING in `signal-frame/schema-rust` + `signal-frame/tests/emit_schema.rs`:

- `ExtendedHeader` (256-byte fixed; byte 0..8 is `ShortHeader` per record 657) ✓
- `Interact<Input>` trait + `InteractionActor<Input>` marker trait (record 660) ✓
- `Effect` enum (record 659, partial — derived from routes, not authored)
- `EffectTable` (record 661, partial — `Operation -> Effect` identity)
- `FanOut` / `FanOutOutput` (record 662, scaffold only — outputs not yet target-tagged)
- Parallel `OwnerEffect` / `SemaEffect` / `OwnerEffectTable` / `SemaEffectTable` / `OwnerFanOut` / `SemaFanOut`

5 emit_schema tests + 1 schema-rust unit test passing. Runtime shape is complete.

What did NOT land is the **schema-language extension for the effect side** — operator notes per /185 §"What I Discovered":

> The current schema substrate is ready for prefix-preserving extended headers because routes already carry leg, root slot, endpoint slot, root name, endpoint name, and body descriptor. The effect side is only partially ready. `AssembledSchema` does not yet carry an authored effect vocabulary or authored effect table. Deriving `Operation -> Effect` one-to-one from routes is therefore the honest first bridge: it gives the generated runtime a stable shape without pretending the schema syntax has already expressed internal actor semantics.

This report designs the schema-syntax extension to express the effect side AUTHORED, not route-derived. This is the next designer slice; the next operator slice consumes this design and lands it in `schema/src/feature.rs` + the `schema-rust` composer.

## §1 The principle: extension, not new section

Per record 657 (extension semantics for headers) and record 656 (schema crystallization), additions are by extension. The schema's 6-position `SchemaDocument` (imports / ordinary-header / owner-header / sema-header / namespace / features) stays unchanged. The effect-side declarations land as **new variants of the existing `Feature` enum**.

Three new `Feature` variants:

| Variant | What it declares | Schema-rust emission |
|---|---|---|
| `EffectTable` | Closed `Operation -> Effect` mapping (record 661) | `Effect` enum + `EffectTable::effect_for_operation` |
| `FanOutTargets` | Per-effect set of `(actor, method)` output targets (record 662) | `FanOutOutput` variants + `FanOut` composition |
| (implicit) | `<Operation>Interact` trait derived from above + existing `Reply` feature | Trait definition + dispatcher glue per /342 |

No 7th position. No new section. Three new feature kinds.

## §2 Effect vocabulary: just namespace declarations

The effect data types (`RecordEffect`, `ObserveEffect`, etc.) live in the existing namespace section. They're regular schema declarations — structs or unit variants per record 616 ("everything reduces to structs"). No special syntax distinguishes them from wire-vocabulary types; the `EffectTable` feature is what marks them as effects.

```nota
;; namespace section (position 4)
RecordEffect [Entry Timestamp]
ObserveEffect [QueryFilter Mode]
WatchEffect [QueryFilter ObserverIdentifier]

;; storage actors referenced from fan-out targets
SpiritStore [DatabasePath]
ObserverSet [SubscriptionTable]
```

## §3 The `EffectTable` feature variant

Maps each operation root from the ordinary header to an effect type from the namespace. Closed mapping. One entry per operation root.

```nota
(EffectTable [
  (Record RecordEffect)
  (Observe ObserveEffect)
  (Watch WatchEffect)
])
```

Each entry is `(<OperationRoot> <EffectType>)` where `OperationRoot` is a header root declared in position 1 (ordinary header) and `EffectType` is a namespace declaration.

`AssembledSchema` carries this as `Feature::EffectTable(EffectTableFeature { entries: Vec<(Name, Name)> })`.

`schema-rust` composer emits:

```rust
pub enum Effect {
    Record(RecordEffect),
    Observe(ObserveEffect),
    Watch(WatchEffect),
}

pub struct EffectTable;

impl EffectTable {
    pub fn effect_for_operation(op: Operation) -> Effect {
        match op {
            Operation::Record(payload) => Effect::Record(payload.into()),
            Operation::Observe(payload) => Effect::Observe(payload.into()),
            Operation::Watch(payload) => Effect::Watch(payload.into()),
        }
    }
}
```

`Into<RecordEffect>` is emitted automatically when the effect type's first field equals the operation payload type (the common case). Otherwise hand-written.

## §4 The `FanOutTargets` feature variant

Per effect, declares the closed set of fan-out outputs. Each output names an actor type + a method tag.

```nota
(FanOutTargets [
  (RecordEffect [
    (Store SpiritStore Insert)
    (Notify ObserverSet Publish)
    (Reply RecordAccepted)
  ])
  (ObserveEffect [
    (Reply RecordsObserved)
  ])
  (WatchEffect [
    (Subscribe ObserverSet Open)
    (Reply Subscribed)
  ])
])
```

Each row is `(<EffectType> [<Output>+])`. Each `<Output>` is:

- `(<MethodTag> <ActorType> <ActorMethod>)` — a fan-out output dispatched to a storage/subscription actor
- `(Reply <ReplyVariant>)` — a fan-out output that materializes as a wire reply

`AssembledSchema` carries this as `Feature::FanOutTargets(FanOutTargetsFeature { entries: Vec<(Name, Vec<FanOutOutputDecl>)> })`.

`schema-rust` composer emits:

```rust
pub enum FanOutOutput {
    Store { actor: ActorRef<SpiritStore>, method: SpiritStoreMethod, payload: Entry },
    Notify { actor: ActorRef<ObserverSet>, method: ObserverSetMethod, payload: RecordSummary },
    Subscribe { actor: ActorRef<ObserverSet>, method: ObserverSetMethod, payload: Subscriber },
    Reply(Reply),
}

pub struct FanOut {
    pub outputs: Vec<FanOutOutput>,
}
```

The `<ActorType>Method` enum (e.g. `SpiritStoreMethod`) is emitted as a closed enum of method tags referenced from the fan-out rows. Each operation root's `<Operation>Interact` trait returns `FanOut` carrying the closed set of possible outputs for THAT effect.

## §5 The interaction-trait derivation (implicit, no new declaration)

Per /342, the interact-trait per operation is implicit:

```rust
pub trait RecordInteract {
    fn interact(&self, payload: RecordEffect) -> FanOut;
}

pub trait ObserveInteract {
    fn interact(&self, payload: ObserveEffect) -> FanOut;
}

pub trait WatchInteract {
    fn interact(&self, payload: WatchEffect) -> FanOut;
}
```

Each trait's method signature is determined by:
- Input: the effect type from `EffectTable`
- Output: `FanOut` (the fan-out output set)

No new schema declaration needed for the trait itself — schema-rust derives it from `EffectTable` + `FanOutTargets`. User writes the impl per /342 §2:

```rust
impl RecordInteract for SpiritRecorder {
    fn interact(&self, payload: RecordEffect) -> FanOut {
        let stamped = StampedEntry::stamp_now(payload.entry);
        FanOut {
            outputs: vec![
                FanOutOutput::Store {
                    actor: self.store.clone(),
                    method: SpiritStoreMethod::Insert,
                    payload: stamped.entry,
                },
                FanOutOutput::Notify {
                    actor: self.observers.clone(),
                    method: ObserverSetMethod::Publish,
                    payload: stamped.summary(),
                },
                FanOutOutput::Reply(Reply::RecordAccepted(stamped.summary())),
            ],
        }
    }
}
```

## §6 Worked example — spirit.schema after extension

Position 5 (features) for `spirit.schema` after this extension:

```nota
[
  (Reply RecordSummary)
  (Reply RecordsObserved)
  (Reply Subscribed)
  (Reply RecordAccepted)
  
  (Event RecordAdded)
  
  (Observable RecordAdded)
  
  (EffectTable [
    (Record RecordEffect)
    (Observe ObserveEffect)
    (Watch WatchEffect)
  ])
  
  (FanOutTargets [
    (RecordEffect [
      (Store SpiritStore Insert)
      (Notify ObserverSet Publish)
      (Reply RecordAccepted)
    ])
    (ObserveEffect [
      (Reply RecordsObserved)
    ])
    (WatchEffect [
      (Subscribe ObserverSet Open)
      (Reply Subscribed)
    ])
  ])
]
```

Everything before `EffectTable` is current schema language. `EffectTable` + `FanOutTargets` are the two new feature variants.

## §7 Implementation plan — the next operator slice

1. **Extend `schema/src/feature.rs`** — add `Feature::EffectTable(...)` and `Feature::FanOutTargets(...)` variants with typed payloads.
2. **Add `EffectTableMacro` + `FanOutTargetsMacro`** to the schema crate's builtin macros — each parses the NOTA `(EffectTable ...)` / `(FanOutTargets ...)` form into the typed feature.
3. **Wire into `AssembledSchema`** — `features()` already returns `&[Feature]`; new variants flow through naturally.
4. **Extend `schema-rust` composer** in three places:
   - `Effect` enum + `EffectTable::effect_for_operation` from `Feature::EffectTable`
   - `FanOutOutput` variants + `<ActorType>Method` enums + `FanOut` from `Feature::FanOutTargets`
   - `<Operation>Interact` traits derived implicitly from both above
5. **Migrate `signal-persona-spirit/spirit.schema`** — add the `EffectTable` + `FanOutTargets` features; ensure existing route table still works
6. **Update `signal-frame/tests/emit_schema.rs`** — add tests that prove (a) `EffectTable::effect_for_operation` returns the AUTHORED effect (not route-identity), (b) `FanOutOutput` enum has the authored target variants, (c) `<Operation>Interact` trait can be implemented and the impl can return a multi-output `FanOut`

Test gates:
- Byte-equivalent against operator/185's current emission for the wire side (no regression on ExtendedHeader, ShortHeader, Operation, Reply, Event)
- New: AUTHORED effect table emission proven for spirit fixture

Estimated scope: ~150 LoC schema crate (feature + macros) + ~200 LoC schema-rust composer (effect-table + fan-out + interact-trait emission) + ~50 LoC test additions.

## §8 Open design questions

1. **Method tag enums — schema-declared or derived?** `SpiritStoreMethod::Insert` could be a schema namespace declaration (closed enum of the actor's methods) or could be derived implicitly from `FanOutTargets` usage. **Lean: schema-declared.** Same model as the wire vocabulary — explicit closed enum in the namespace section, referenced from feature declarations. This composes with future storage descriptors.

2. **`Into<EffectType>` impl auto-generated?** When `EffectType` has a single field of the operation payload type (e.g. `RecordEffect [Entry]`), schema-rust auto-emits `impl From<Entry> for RecordEffect`. When the effect type has more fields (e.g. `RecordEffect [Entry Timestamp]`), the user writes the `From` impl. **Lean: yes, auto-emit only the trivial 1:1 case; everything else is user code.**

3. **Reply variants in FanOutTargets — must match `Feature::Reply` declarations?** `(Reply RecordAccepted)` references `RecordAccepted` which should be declared as a reply variant via `(Reply RecordAccepted)` elsewhere. **Lean: schema engine enforces — if a fan-out target names `Reply X`, `X` must be a reply variant in the same schema. Validation at AssembledSchema build time.**

4. **Storage descriptors (redb tables) — same feature or separate?** `SpiritStore` is an actor reference; its underlying redb tables also have schema-derivable layouts. **Lean: separate feature `(StorageDescriptor SpiritStore [(EntriesTable Entry) (...)] )`. Future slice; not blocking the effect-side syntax.**

5. **Cross-actor fan-out (one effect → another actor's fan-out)?** Sometimes a Record effect triggers a Notify effect on the ObserverSet which itself has its own fan-out (notify each subscriber). Does the schema chain these? **Lean: no chaining at schema level. Each effect declares its DIRECT outputs; cascade happens because the actor's own impl returns its own FanOut. Composes recursively at runtime; schema stays flat per effect.**

## §9 What this unblocks

Once the schema language carries authored `EffectTable` + `FanOutTargets`:

- The 38 contract crates currently on legacy `signal_channel! { ... }` can migrate to `emit_schema!()` AND express their internal actor architecture in the SAME `.schema` file
- The persona-daemon supervisor topology becomes schema-declarable — supervisor + working actors + storage actors all named with their interact-traits explicit
- Cross-component migration (the upgrade machinery) becomes more uniform — the upgrade-handover ceremony IS an interaction between two component versions; its trait surface lives in `signal-version-handover.schema`
- The `primary-cklr` slice (UpgradeMacro Rust code emission) per /338 §8 #2 absorbs into this — `Upgrade` feature emits effect-tables for the version-projection From-chain

## §10 References

- Operator/185 — implementation that surfaced this gap
- /341 — schema crystallization synthesis (the seven principles)
- /342 — interact-trait code walkthrough (clarifies emission scope)
- /340 — schema emission no-legacy review (15-item emit inventory + composer architecture)
- Records 656-665 — the load-bearing principles + the trait-emission-scope clarification
- `signal-frame/schema-rust/src/lib.rs` — current composer state (570 LoC; growing)
- `/git/github.com/LiGoldragon/schema/src/feature.rs` — feature kinds; needs `EffectTable` + `FanOutTargets` variants
- `signal-persona-spirit/spirit.schema` — first migration target for the authored effect-side
