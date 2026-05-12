# 136 — `strum::EnumDiscriminants` proposal review

*Designer review of `reports/designer/135-kind-enums-via-strum-enum-discriminants.md`,
performed by reading `persona/src/schema.rs` and
`persona/src/engine_event.rs` directly, checking the
`nota-derive` source for `NotaEnum`'s actual constraints, and
fetching `strum_macros/src/macros/enum_discriminants.rs` to verify the
specific `From` impls the derive generates. Affirms the recommendation;
corrects the central justification; tightens the proposed code; pins
one open migration choice; flags a broader related duplication the
proposal doesn't address.*

---

## TL;DR

`/135`'s recommendation — `strum::EnumDiscriminants` on the parent
enums in `engine_event.rs`, with the kind enums moved next to their
parents and the hand-written projection methods deleted — is right.
The strum syntax `/135` cites is correct
(`#[strum_discriminants(name(...))]`, `#[strum_discriminants(derive(...))]`)
and the derive does generate `From<&EngineEventBody>` (verified in
`strum_macros/src/macros/enum_discriminants.rs` — both the owned and
the reference `From` impls are emitted unconditionally).

But the proposal has three real issues worth fixing before the
operator implements:

1. **The central justification is the weaker of two available
   arguments.** `/135` argues the kind enum is "a structural projection
   of the parent enum, not a schema concept." That's defensible but
   philosophical. The *load-bearing* reason the kind enum exists at
   all is `nota-derive/src/nota_enum.rs:15-20`: `NotaEnum` panics
   on payload-bearing variants, so `EngineEventBody` (which has
   payloads) cannot derive `NotaEnum` directly. The kind enum is a
   payload-free shadow specifically engineered to satisfy
   `NotaEnum`'s unit-variant constraint. This is the architectural
   fact; the structural-projection argument is a downstream observation.
2. **The proposed pass-through derive list duplicates strum's
   defaults.** `/135` shows
   `#[strum_discriminants(derive(NotaEnum, Debug, Clone, Copy, PartialEq, Eq))]`,
   but `EnumDiscriminants` already emits `Clone, Copy, Debug, PartialEq, Eq`
   by default. The pass-through should be just `derive(NotaEnum)`.
3. **One migration choice is left dangling.**
   `tests/manager_store.rs:11` imports `EngineEventBodyKind` and
   `EngineEventSourceKind` from `persona::schema`. Moving the kind
   enums to `engine_event` requires either a re-export from `schema`
   or an updated test import. `/135` notes both options without
   picking; this report picks the re-export and explains why.

A fourth observation, out of scope for `/135` but worth naming:
`schema.rs` lines 215-272 carry the *same* duplication pattern for
five other enums (`EnginePhase`, `ComponentKind`,
`ComponentDesiredState`, `ComponentHealth`,
`SupervisorActionRejectionReason`), each with a hand-written
`from_contract` method that mechanically maps variants from the
`signal-persona` crate's enum to schema's parallel enum. These are
not discriminant projections — they're same-shape enum copies across
crate boundaries — so `strum::EnumDiscriminants` does not help.
Their deduplication is a separate proposal.

---

## 1 — Verified claims

Direct verification against the docs and source for each technical
claim in `/135`:

| Claim | Verified against | Result |
|---|---|---|
| `strum::EnumDiscriminants` exists; current `strum` version supports it. | `docs.rs/strum/latest/` | ✅ strum 0.28; `EnumDiscriminants` is in `strum_macros` and re-exported through `strum`. |
| Add via `strum = { version = "0.28", features = ["derive"] }`. | strum docs | ✅ confirmed. |
| Attribute syntax `#[strum_discriminants(name(EngineEventBodyKind))]`. | `docs.rs/strum_macros/.../derive.EnumDiscriminants.html` | ✅ `name(OtherName)` is the canonical form (not `name = "..."`). |
| Attribute syntax `#[strum_discriminants(derive(...))]` to pass derives through. | strum docs | ✅ confirmed. |
| Generates `From<&EngineEventBody> for EngineEventBodyKind`, not just `From<EngineEventBody>`. | `strum_macros/src/macros/enum_discriminants.rs` source | ✅ **both** are emitted unconditionally. The source comment notes "we are not able to check if a type is `Copy`," so the macro generates both owned and reference `From` impls for caller flexibility. |
| Default derives on the emitted enum. | strum docs | ✅ `Clone, Copy, Debug, PartialEq, Eq`. (See §2.2 — `/135`'s example duplicates these.) |
| The call-site can switch from `EngineEventBodyKind::from_event_body(event.body())` to `EngineEventBodyKind::from(event.body())` or `event.body().into()`. | strum behavior + source code reading | ✅ `event.body()` returns `&EngineEventBody`, and `From<&EngineEventBody>` is generated, so no clone is required. |

Five of the six syntactic claims passed verification cleanly. The
sixth — `From<&Parent>` — had to be checked against the macro's
source because the docs page summary on `docs.rs` only mentions
`From<MyEnum>` without explicitly naming the reference impl. The
source confirms both are emitted.

---

## 2 — What `/135` missed or understated

### 2.1 — The load-bearing justification is `NotaEnum`'s unit-variant constraint

`nota-derive/src/nota_enum.rs` lines 15-20:

```rust
match input.data {
    syn::Data::Enum(data_enum) => data_enum,
    _ => panic!("NotaEnum can only be derived for enums (with unit variants only)"),
}

for variant in &data_enum.variants {
    if !matches!(variant.fields, syn::Fields::Unit) {
        panic!(
            "NotaEnum requires every variant to be a unit variant; `{}::{}` carries data",
            name, variant.ident
        );
    }
}
```

`EngineEventBody` is a payload-bearing enum
(`ComponentSpawned(ComponentLifecycleEvent)`,
`ComponentExited(ComponentExited)`, etc.). Trying to add
`#[derive(NotaEnum)]` to it would panic at compile time. The kind
enum in `schema.rs` exists *for the precise purpose of giving NotaEnum
a unit-variant enum to derive on*.

`/135` mentioned this in passing ("the NOTA-specific piece is the
`NotaEnum` derive on that projection; that derive can live wherever
the projection lives") but framed the choice as a module-boundary
preference. It isn't. The constraint is concrete and load-bearing:
without the unit-variant shadow, NOTA cannot represent the
discriminator at all.

This sharpens — but does not contradict — `/135`'s recommendation.
The strum derive *still* solves the duplication, because the emitted
unit-variant enum is exactly what `NotaEnum` needs as input. The
composition is:

1. `strum::EnumDiscriminants` reads `EngineEventBody`'s variant list
   and emits a unit-variant `EngineEventBodyKind`.
2. The `#[strum_discriminants(derive(NotaEnum))]` pass-through applies
   `#[derive(NotaEnum)]` to the emitted enum.
3. `NotaEnum`'s proc macro runs against the unit-variant enum and
   accepts it (the constraint check at `nota_enum.rs:15-20` passes).

The right framing in the proposal would be: *NotaEnum forces a
unit-variant shadow; strum removes the cost of maintaining that
shadow by hand.* The kind enum is structurally a property of the
parent, but the reason we need a *named, NotaEnum-derived* version of
that structural property is `nota-derive`'s constraint, not a
philosophical preference.

### 2.2 — strum places the emitted enum next to the parent — there is no choice

`/135`'s "module boundary argument" treats the placement of the kind
enum as a designer-discretion question. With strum, it isn't.
`strum::EnumDiscriminants` is a *derive on the parent enum*. The
emitted code — the discriminants enum plus the `From` impls — is
inserted at the parent enum's definition site by the macro expansion.
There is no syntax to say "emit the kind enum in a different module."

So the choice the user is making with this proposal is not "where does
the kind enum live?" — strum decides that. The choice is:

- **(a)** accept the kind enum living in `engine_event.rs` (and pay
  the migration cost to re-export it from `schema.rs` or update the
  test import); or
- **(b)** keep the kind enum hand-written in `schema.rs` (and pay the
  duplication cost forever).

There is no third option that uses strum and keeps the kind enum in
`schema.rs`. `/135`'s philosophical argument for engine_event placement
should be replaced with this concrete observation: strum forces it,
and the migration cost is small and one-time.

### 2.3 — Pass-through derive list is redundant

`/135` shows:

```rust
#[strum_discriminants(derive(NotaEnum, Debug, Clone, Copy, PartialEq, Eq))]
```

`Debug, Clone, Copy, PartialEq, Eq` are already the default derives
strum emits on the discriminants enum. The pass-through only needs to
add what strum doesn't emit. Correct form:

```rust
#[strum_discriminants(derive(NotaEnum))]
```

Minor, but worth catching before it becomes a copy-paste pattern.

### 2.4 — Migration diff is closer to -34 lines, not -24

Actual count from `persona/src/schema.rs`:

| Item | Lines |
|---|---|
| `pub enum EngineEventSourceKind { Manager, Component }` + derive frame | ~6 |
| `pub enum EngineEventBodyKind { … 8 variants … }` + derive frame | ~10 |
| `impl EngineEventSourceKind { fn from_event_source(…) … }` block | ~9 |
| `impl EngineEventBodyKind { fn from_event_body(…) … }` block | ~15 |
| **Total deletion in schema.rs** | **~40 lines** |
| Strum derive + attribute lines added to `engine_event.rs` (×2 parents) | ~6 |
| **Net change** | **~-34 lines** |

`/135` underestimated the deletion; the actual win is bigger.

### 2.5 — `NotaEnum` × strum composition needs a smoke test, not just an architectural argument

The composition is plausible (per §2.1) but proc-macro composition can
fail in non-obvious ways — name collisions, attribute parsing
disagreements, ordering issues, generic-handling differences. The
proposal should add an explicit verification step before declaring the
migration complete:

> Run `cargo expand` on `engine_event.rs` to confirm the generated
> `EngineEventBodyKind` and `EngineEventSourceKind` enums carry every
> derive (`NotaEnum`, `Debug`, `Clone`, `Copy`, `PartialEq`, `Eq`),
> and run the existing `tests/manager_store.rs` round-trip tests
> (lines 251-252 assert `projection.source == EngineEventSourceKind::Manager`
> and `projection.body == EngineEventBodyKind::ComponentSpawned`).
> If both compile and pass, the composition is verified.

This is cheap and forecloses the small risk of an unexpected proc-macro
interaction.

---

## 3 — Refined shape

Combining the corrections from §2:

```rust
// persona/src/engine_event.rs

use strum::EnumDiscriminants;

#[derive(
    rkyv::Archive, rkyv::Serialize, rkyv::Deserialize,
    Debug, Clone, PartialEq, Eq,
    EnumDiscriminants,
)]
#[strum_discriminants(name(EngineEventBodyKind))]
#[strum_discriminants(derive(NotaEnum))]
pub enum EngineEventBody {
    ComponentSpawned(ComponentLifecycleEvent),
    ComponentReady(ComponentLifecycleEvent),
    ComponentUnimplemented(ComponentUnimplemented),
    ComponentExited(ComponentExited),
    RestartScheduled(RestartScheduled),
    RestartExhausted(RestartExhausted),
    ComponentStopped(ComponentLifecycleEvent),
    EngineStateChanged(EngineStateChanged),
}

#[derive(
    rkyv::Archive, rkyv::Serialize, rkyv::Deserialize,
    Debug, Clone, PartialEq, Eq,
    EnumDiscriminants,
)]
#[strum_discriminants(name(EngineEventSourceKind))]
#[strum_discriminants(derive(NotaEnum))]
pub enum EngineEventSource {
    Manager,
    Component(ComponentName),
}
```

Differences from `/135`'s proposed shape:

- `derive(NotaEnum)` instead of `derive(NotaEnum, Debug, Clone, Copy, PartialEq, Eq)` — strum emits the latter five by default.
- One `use strum::EnumDiscriminants;` at the top of `engine_event.rs` (the derive needs the import in scope, not just on the attribute).

---

## 4 — Companion observation: the `from_contract` duplication

`/135` is scoped to `EngineEventBodyKind` and `EngineEventSourceKind`.
`schema.rs` lines 215-272 carry a *different* duplication for five
other enums:

```rust
// schema.rs — five hand-written from_contract methods like:
impl EnginePhase {
    pub fn from_contract(phase: contract::EnginePhase) -> Self {
        match phase {
            contract::EnginePhase::Starting => Self::Starting,
            contract::EnginePhase::Running  => Self::Running,
            contract::EnginePhase::Degraded => Self::Degraded,
            contract::EnginePhase::Draining => Self::Draining,
            contract::EnginePhase::Stopped  => Self::Stopped,
        }
    }
}
```

Each pair (`contract::EnginePhase` ↔ `schema::EnginePhase`,
`contract::ComponentKind` ↔ `schema::ComponentKind`, …) has identical
variant lists. These are not discriminant projections of payload-bearing
enums — they're same-shape enum copies across crate boundaries, kept
separate because `contract::*` derives `rkyv::Archive` for wire
transport while `schema::*` derives `NotaEnum` for text projection.

`strum::EnumDiscriminants` does not solve this. The right
deduplication move here is one of:

- **(a)** derive `NotaEnum` directly on the `contract::*` enums in
  `signal-persona`, and delete schema's copies + the five
  `from_contract` methods entirely. Requires `signal-persona` to take
  a `nota-codec` dependency. This is the cleanest answer if the
  dependency direction is acceptable.
- **(b)** keep the parallel enums but generate the projection with a
  proc macro that takes two identical-shape enums and emits both
  `From` directions. Heavier than the duplication it eliminates;
  probably not worth it for five enums.
- **(c)** accept the duplication as the cost of the wire/text
  separation.

This is the right size for a follow-up proposal (`/137` or later),
not a fold-in to `/135`'s scope. Flagging here so the work isn't
forgotten.

---

## 5 — Refined migration steps

Tightened version of `/135` §5, with the pinned choices from this
review:

1. Add `strum = { version = "0.28", features = ["derive"] }` to
   `persona/Cargo.toml` `[dependencies]`. Place alphabetically
   between `signal-persona-message` and `thiserror`.
2. In `engine_event.rs`: add `use strum::EnumDiscriminants;` at the
   top; add the two `EnumDiscriminants` derive lines + the four
   `#[strum_discriminants(...)]` attribute lines from §3 above.
3. In `schema.rs`: replace the four hand-written items
   (`EngineEventSourceKind` enum + `EngineEventBodyKind` enum +
   their `from_event_*` impls) with a single re-export line:
   ```rust
   pub use crate::engine_event::{EngineEventBodyKind, EngineEventSourceKind};
   ```
   Re-exporting from `schema` keeps the existing import path
   `use persona::schema::{EngineEventBodyKind, EngineEventSourceKind};`
   in `tests/manager_store.rs:11` valid. Net zero-churn at call
   sites outside `schema.rs` itself.
4. In `schema.rs::EngineEventReport::from_event` (lines 107-114):
   replace `EngineEventSourceKind::from_event_source(event.source())`
   with `event.source().into()`, and
   `EngineEventBodyKind::from_event_body(event.body())` with
   `event.body().into()` (the target type is inferred from the
   field types of `EngineEventReport`).
5. Run `cargo expand --bin persona-daemon` (or `--lib`) and confirm
   the emitted `EngineEventBodyKind` / `EngineEventSourceKind` carry
   the expected derives.
6. Run `cargo test -p persona` and confirm
   `tests/manager_store.rs` lines 251-252 still pass — the NOTA
   round-trip for `EngineEventReport` is the load-bearing
   witness that the strum-emitted enums behave identically to the
   hand-written ones.

Step 3's re-export choice resolves the open question in `/135` §5
step 3 ("update imports … *or* re-export"). Re-exporting from
`schema` keeps the *teleological* identity of the kind enums visible
in `schema`'s public surface (these enums exist for NOTA projection
per §2.1) while letting their *structural* definition live next to
the parent enum where strum forces it to live.

---

## 6 — One-sentence summary

`/135`'s `strum::EnumDiscriminants` recommendation is sound and the
syntax is correct (both `From<EngineEventBody>` and
`From<&EngineEventBody>` are emitted per the strum macro source); the
proposal should be tightened by replacing its module-boundary
philosophical argument with the concrete `NotaEnum` unit-variant
constraint that actually forces the shadow enum to exist, by removing
the duplicate-of-strum-defaults from the pass-through derive list,
and by pinning the schema-re-export migration choice so the test
import doesn't churn.

---

## See also

- `reports/designer/135-kind-enums-via-strum-enum-discriminants.md`
  — the proposal this report reviews.
- `reports/designer/134-component-skeletons-and-engine-event-log-review.md`
  §2.1 — the broader typed-operation argument `/135` is a narrower
  case of.
- `/git/github.com/LiGoldragon/persona/src/schema.rs` lines 80-96,
  273-296 — the hand-written kind enums and projection impls that
  `/135` proposes to delete.
- `/git/github.com/LiGoldragon/persona/src/schema.rs` lines 215-272 —
  the broader `from_contract` duplication pattern in §4 (out of
  `/135`'s scope; flagged for a future proposal).
- `/git/github.com/LiGoldragon/persona/src/engine_event.rs` — where
  the strum derives land.
- `/git/github.com/LiGoldragon/persona/tests/manager_store.rs` lines
  11, 251-252 — the call sites that constrain the schema-re-export
  vs. test-import-update choice; pinned in §5 step 3 to re-export.
- `/git/github.com/LiGoldragon/nota-codec/../nota-derive/src/nota_enum.rs`
  lines 15-20 — the `NotaEnum` unit-variant panic that is the
  load-bearing reason the kind enum exists at all (§2.1).
- [`strum::EnumDiscriminants` docs](https://docs.rs/strum_macros/latest/strum_macros/derive.EnumDiscriminants.html)
  — current at strum 0.28.
- [`strum_macros/src/macros/enum_discriminants.rs`](https://raw.githubusercontent.com/Peternator7/strum/master/strum_macros/src/macros/enum_discriminants.rs)
  — the macro source that confirms both owned and reference `From`
  impls are generated unconditionally.
