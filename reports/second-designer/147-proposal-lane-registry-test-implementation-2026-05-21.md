# 147 — Lane registry test-implementation proposal

*Test-implementation-ready proposal for the typed lane-registry
slice of persona-orchestrate. Sliced from `/2`
(persona-orchestrate lane management) after the role-vector model
settled with intent IDs 97 (open-string discipline) + 98 (role
vectors) + 99 (token-driven skill loading) + 100 (operator
parallel-lane rename). Scope is narrow on purpose: just the
registry. The claim surface is deferred per `/137` §"Open Q1".*

## 0 · TL;DR

Land a working slice of the typed lane registry inside
persona-orchestrate that **does not replace** the bash
`orchestrate/roles.list` yet — it runs alongside, witnesses that
the typed shape is sound, and exposes Observe so agents can read
the registry through the daemon. Two contracts get extended
(`signal-persona-orchestrate` for Observe; `owner-signal-persona-orchestrate`
for Register / Retire / SetAuthority). The lane identifier is
derived inside the daemon from `(role, authority)` + a registration
ordinal. Storage is one redb table.

This is **not** the full persona-orchestrate migration (that's
bead `primary-c620`). It is one focused slice that proves out the
role-vector shape end-to-end and seeds the bigger migration.

## 1 · Scope

**In scope:**
- Typed records (`RoleToken`, `Role`, `LaneAuthority`, `LaneIdentifier`,
  `LaneRegistration`).
- Three owner-channel operations: `Register`, `Retire`, `SetAuthority`.
- One working-channel operation: `Observe(Lanes)` returning the
  registered lane list.
- Lane-identifier derivation logic in the daemon.
- One redb table backing the registry.
- Round-trip + derivation tests in `tests/`.

**Out of scope:**
- The claim surface (`Claim` / `Release` / `Handoff`). Deferred per
  `/137` §"Open Q1" — the destination shape is itself unsettled.
- Replacing the bash `orchestrate/roles.list` as source of truth.
  The bash file stays canonical for this slice; the typed registry
  runs alongside as a witness.
- Lane mutation through the working channel. Only the owner channel
  can `Register` / `Retire` / `SetAuthority`.
- Reports-subdirectory creation. The daemon emits the derived
  identifier; creating `reports/<lane>/` on disk is a follow-up
  slice once the registry proves out.
- skill-bundle delivery. The role-vector model implies token-driven
  skill loading (intent 99) but the actual mind→agent skill delivery
  is persona-mind's surface, not orchestrate's. This slice produces
  the data; persona-mind consumes it later.

## 2 · Wire types

Land in `signal-persona-orchestrate/src/lib.rs` (or extracted to a
sibling crate if the working contract is being kept narrow — operator
judgment).

```rust
use nota_codec::{NotaTransparent, NotaRecord, NotaEnum};
use rkyv::{Archive, Deserialize as RkyvDeserialize, Serialize as RkyvSerialize};

/// An identifier token in a role vector. Open-string per intent ID 97;
/// the workspace adds new tokens (PersonaSignal, Note, System, …)
/// without contract bumps.
#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaTransparent, ...)]
pub struct RoleToken(String);

/// A role is a non-empty vector of role tokens. The last token is the
/// base discipline (Designer, Operator, ...) which determines the
/// authority chain. Preceding tokens are specialization tokens.
///
/// NOTA shape: `[PersonaSignal Designer]`, `[Note Designer]`, `[Designer]`.
#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaRecord, ...)]
pub struct Role {
    pub tokens: Vec<RoleToken>,   /* non-empty; validation needed */
}

/// Lane authority class.
#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaEnum, ...)]
pub enum LaneAuthority {
    Structural,  /* full main-role authority */
    Support,     /* bounded support-scope (assistants) */
}

/// The filesystem stuffed-string form of the (role, authority, ordinal)
/// tuple. Derived inside the daemon at registration time.
#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaTransparent, ...)]
pub struct LaneIdentifier(String);

/// The registry record stored per lane.
#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaRecord, ...)]
pub struct LaneRegistration {
    pub lane: LaneIdentifier,
    pub role: Role,
    pub authority: LaneAuthority,
}
```

`Role` is currently a struct wrapping `Vec<RoleToken>` rather than a
typed-newtype over `Vec`. Reason: the workspace doesn't yet have a
`NonEmpty` NOTA primitive; landing one is a sibling slice. The
validation lives in the daemon: `Register` rejects an empty role
vector. Operator may use the existing `signal_executor::NonEmpty`
type if it fits; otherwise validate at the daemon boundary.

## 3 · Operations

### Owner channel (`owner-signal-persona-orchestrate`)

```rust
pub struct LaneRegistrationRequest {
    pub role: Role,
    pub authority: LaneAuthority,
}

pub struct LaneAuthorityChange {
    pub lane: LaneIdentifier,
    pub authority: LaneAuthority,
}

/* Operation root additions: */
operation Register(LaneRegistrationRequest),
operation Retire(LaneIdentifier),
operation SetAuthority(LaneAuthorityChange),
```

**Replies:**

```rust
/* On Register: */
pub struct LaneRegistered {
    pub registration: LaneRegistration,  /* derived identifier inside */
}

/* On Retire: */
pub struct LaneRetired {
    pub lane: LaneIdentifier,
}

/* On SetAuthority: */
pub struct LaneAuthoritySet {
    pub lane: LaneIdentifier,
    pub authority: LaneAuthority,
}
```

### Working channel (`signal-persona-orchestrate`)

Extend `Observe` with a new variant:

```rust
pub enum Observation {
    /* existing variants */
    Lanes,  /* read the registered lanes; no filter in this slice */
}

pub struct LanesObserved {
    pub lanes: Vec<LaneRegistration>,
}
```

The working channel is read-only on the registry in this slice;
peers cannot mutate.

## 4 · Lane-identifier derivation

The daemon derives `LaneIdentifier` from `(role, authority,
prior_count_of_same_role_authority)`:

```
fn derive_identifier(role: &Role, authority: LaneAuthority, prior_count: usize) -> LaneIdentifier {
    // 1. Render the role vector: lowercase tokens joined by "-".
    let role_part = role.tokens.iter()
        .map(|t| pascal_to_kebab(t.0.as_str()))
        .collect::<Vec<_>>()
        .join("-");

    // 2. Append "-assistant" if Support authority.
    let with_auth = if authority == LaneAuthority::Support {
        format!("{role_part}-assistant")
    } else {
        role_part
    };

    // 3. Prepend "second-" / "third-" / ... if this is not the first
    //    registration of the same (role, authority) pair.
    let final_id = match prior_count {
        0 => with_auth,
        1 => format!("second-{with_auth}"),
        2 => format!("third-{with_auth}"),
        n => format!("{}-{with_auth}", ordinal_word(n + 1)),
    };

    LaneIdentifier(final_id)
}
```

`pascal_to_kebab("PersonaSignal")` → `"persona-signal"`;
`pascal_to_kebab("Designer")` → `"designer"`. Standard
PascalCase-to-kebab-case split on capital letters.

`ordinal_word(2)` → `"second"`, `ordinal_word(3)` → `"third"`,
`ordinal_word(4)` → `"fourth"`, etc. Operator picks the
implementation; an off-the-shelf crate or a small hand-table is
fine. Beyond ten the workspace likely has a different organizational
problem; failing past `tenth` is acceptable.

## 5 · Storage

One redb table keyed by `LaneIdentifier`:

```
TABLE: "lane_registry"
KEY:   LaneIdentifier (rkyv)
VALUE: LaneRegistration (rkyv)
```

`Register` flow:
1. Validate role is non-empty.
2. Read all current registrations into memory (cheap; small N).
3. Count existing registrations matching `(request.role,
   request.authority)`.
4. Derive `LaneIdentifier` from `(role, authority, count)`.
5. Insert into the table.
6. Return `LaneRegistered` carrying the new registration.

`Retire` flow:
1. Look up by `LaneIdentifier`.
2. Remove from the table.
3. Return `LaneRetired`.
4. Open: should retiring a lane re-number subsequent ordinals?
   Designer lean: no. Retiring `second-designer` does not promote
   `third-designer` to `second-designer`. Identifiers are stable
   once assigned. (Worth confirming with psyche before implementation
   if operator hits the edge case during testing.)

`SetAuthority` flow:
1. Look up by `LaneIdentifier`.
2. Update the authority field.
3. Note: this does NOT recompute the lane identifier. A lane that
   started as `designer-assistant` and gets promoted to Structural
   keeps the `designer-assistant` name (until explicitly retired
   and re-registered). Operator can flag this as a design smell if
   it surfaces during testing.

## 6 · Test cases

At minimum, witness the following round-trips and derivations in
`tests/lane_registry.rs`:

- `RoleToken` NOTA round-trip (`PersonaSignal` → `(PersonaSignal)`
  → back).
- `Role` NOTA round-trip including multi-token vectors.
- `LaneAuthority` NOTA round-trip for both variants.
- `LaneRegistration` rkyv round-trip.
- Derivation: `derive_identifier([Designer], Structural, 0)` →
  `LaneIdentifier("designer")`.
- Derivation: `derive_identifier([Designer], Structural, 1)` →
  `LaneIdentifier("second-designer")`.
- Derivation: `derive_identifier([Note Designer], Support, 0)` →
  `LaneIdentifier("note-designer-assistant")`.
- Derivation: `derive_identifier([PersonaSignal Designer],
  Structural, 0)` →
  `LaneIdentifier("persona-signal-designer")`.
- End-to-end: `Register([Designer], Structural)` → registry has 1
  lane. `Register([Designer], Structural)` again → registry has 2
  lanes, second one has identifier `second-designer`.
- `Observe(Lanes)` returns all registered lanes.
- `Retire("designer")` removes the lane; `Observe(Lanes)` reflects
  the removal.

The tests double as the falsifiable specification for the derivation
rules; future agents reading the tests learn the contract without
reading prose.

## 7 · Constraints

- DO NOT touch the bash `orchestrate/roles.list` source-of-truth in
  this slice. The typed registry runs alongside.
- DO NOT implement the claim surface; that's a separate slice
  pending `/137` Q1.
- DO NOT create `reports/<lane>/` directories from the daemon;
  follow-up slice.
- DO NOT mutate `AGENTS.md` role table or `skills/role-lanes.md`
  from the daemon; designer follow-up after the typed surface
  proves out.
- Follow the existing persona-orchestrate triad shape per `/137`
  (signal-executor in the daemon path, ToSemaOperation /
  ToSemaOutcome, observable block on the working channel).

## 8 · References

- `/2` (this report's parent) — the full lane-management design.
- `/137` — persona-orchestrate triad audit; §"Open Q1" defers
  the claim surface that this slice does NOT include.
- `/129` — mind-orchestrate context; agent registry shape that
  intersects this slice eventually.
- `intent/persona.nota` records (today):
  - **97** — discipline field is open string; roles user-extensible.
  - **98** — roles are vectors; specialization composes.
  - **99** — token-driven skill loading.
  - **100** — double-lane pattern; operator parallel-lane rename.
- `intent/persona.nota` 2026-05-19T15:04:19Z — dynamic roles.
- `intent/persona.nota` 2026-05-20T17:30:00Z — skills bundle into
  roles; mind→orchestrate policy programmability.
- `orchestrate/roles.list` — the bash registry this slice does NOT
  replace yet.
- Bead `primary-c620` — the broader persona-orchestrate migration;
  this slice is one focused piece within it.

This proposal retires when the lane-registry slice ships with all
tests in §6 green, OR a successor proposal supersedes the shape.
