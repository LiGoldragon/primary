# 138 — Contract types own wire and text derives — the Pattern A reversal

*Designer report. The user pushed back on `/137` §1.1's conclusion
that Pattern A's cross-crate wire/text duplication is "load-bearing."
Their argument: centralization — one type per concept — is a deeper
workspace value than audience-scoped compile-time isolation, and
making contract messages NOTA-encodable is a real debuggability /
testing / logging unlock, not a downstream cost. This report
investigates the actual blockers (rather than the framed ones),
finds none, names a concrete workspace precedent that already does
exactly this, and proposes the policy shift along with the migration
that follows.*

---

## 0 — User's stated intent (the weight)

Recorded verbatim:

> I don't think that deriving the text decoding capability on the
> same contract types is necessarily bad. I think that centralizing
> the types has a huge advantage that overpowers the cost of
> carrying the nota derive on those types. And then there's the
> bonus that all these messages, these contracts, become encodable
> into nota for readable debugging, which we'll probably want to do
> for testing or for logging.

Two design forces named:

1. **Centralization (primary).** One type per concept is a load-bearing
   workspace discipline (`skills/rust/methods.md` §"One type per
   concept", `skills/abstractions.md` §"Find the structure that
   makes the special case dissolve into the normal case"). Pattern A
   creates two types named `ComponentKind` in two crates that mean the
   same concept. That violates the principle.
2. **Debuggability bonus.** Today, dumping a wire value to a log or
   panic message requires manual conversion to the schema-side
   mirror. With `NotaEnum` on contract types, every wire message is
   `.to_nota()`-able for free — readable in tests, in logs, in error
   messages, in fixtures. This is a *capability* change, not just a
   refactor.

This report weighs the policy shift the user is proposing against
the existing architectural reasons for the wire/text separation,
finds the architectural reasons less load-bearing than they appeared,
and recommends the shift.

---

## 1 — Why `/137` got the Pattern A framing wrong

`/137` §1.1 argued that adding `nota-codec` to `signal-persona` would
"couple every wire contract crate to NOTA" and cited
`skills/contract-repo.md` lines 49-62 ("audience-scoped compile-time
isolation") as the load-bearing justification. The framing treated
this as an architectural invariant.

It isn't. Two facts the prior framing missed:

**1. The base contract crate already depends on `nota-codec`.**
`signal-core/Cargo.toml` lines 15-19:

```toml
[dependencies]
nota-codec = { git = "https://github.com/LiGoldragon/nota-codec.git", branch = "main" }
rkyv = { version = "0.8", default-features = false, features = ["std", "bytecheck", "little_endian", "pointer_width_32", "unaligned"] }
thiserror = "2"
```

`signal-core` is the workspace's wire kernel — frames, channel macro,
the Signal protocol's shared primitives. Every `signal-*` contract
crate in the workspace transitively depends on `signal-core`, which
transitively depends on `nota-codec`. The build-graph reach
argument is moot: nota-codec is already in the graph for every
consumer of any signal contract.

**2. `signal-core` already combines `rkyv` and `NotaEncode`/`NotaDecode`
on the same contract types.** `signal-core/src/pattern.rs` defines
`Bind`, `Wildcard`, and `PatternField<T>` with both wire and text
derives composed on the same types. The pattern this report
advocates is **what `signal-core` already does**. `signal-persona`'s
strict-wire-only-derives shape is the outlier, not the rule.

The "wire-only contract crates" discipline the prior report cited from
`contract-repo.md` describes a stricter policy than the workspace
actually follows. The skill is out of date relative to the code; this
report's recommendations include bringing the skill into line.

---

## 2 — Investigating blockers (rather than costs)

The user's framing draws the right distinction: costs are paid once
and amortized; blockers actually prevent the move. Going through the
candidate blockers systematically:

### 2.1 — Build-graph cycle

**Not a blocker.** `nota-codec` deps are `nota-derive` (proc-macro) +
`thiserror`. `nota-derive` deps are `proc-macro2` + `quote` + `syn`.
None of these depend on `signal-*`. The graph is one-way:
`signal-* → nota-codec → nota-derive`. No cycle, no circular import
risk.

### 2.2 — Macro composition

**Not a blocker, verified twice.** `/136` §2.1 established that
`NotaEnum` and `rkyv::Archive` generate disjoint impls
(`NotaEncode`/`NotaDecode` vs `Archive`/`ArchivedFoo`/`impl Archive`).
`signal-core/src/pattern.rs` is empirical confirmation — the
composition has been compiling in production code for at least
several months. No name collisions, no derive-order issues, no
attribute-parsing conflicts.

### 2.3 — `no_std` / feature-flag complications

**Not a blocker.** `signal-persona/Cargo.toml` already pulls rkyv
with `default-features = false, features = ["std", ...]`, indicating
the crate is std-bearing. `nota-codec` is std-only by default. The
feature surfaces align.

### 2.4 — `NotaEnum`'s unit-variant constraint

**Not a blocker for the five Pattern A enums.** All five
(`EnginePhase`, `ComponentKind`, `ComponentDesiredState`,
`ComponentHealth`, `SupervisorActionRejectionReason`) are unit-variant
per `signal-persona/src/lib.rs:40-78`. The constraint at
`nota-derive/src/nota_enum.rs:15-20` is satisfied by construction.

For the payload-bearing struct types in `signal-persona`
(`ComponentStatus`, `EngineStatus`, `EngineStatusQuery`,
`ComponentStatusQuery`, `ComponentStartup`, `ComponentShutdown`,
`SupervisorActionAcceptance`, `ComponentStatusMissing`,
`SupervisorActionRejection`), the corresponding derive is
`NotaRecord` (for structs with named fields, per `nota-derive`'s
README). Same shape, no obstacle.

### 2.5 — Compile time

**A cost, not a blocker.** `nota-codec` is small (one decoder, one
encoder, the trait pair, plus the derives in `nota-derive`). For an
already-in-graph dependency (per §1), adding direct derives on
contract types adds nothing structural — only the time to expand the
derives, which for unit-variant enums is a handful of match arms each.

### 2.6 — Wire-format stability concerns

**Not a blocker; the policy shift actively helps.** A concern someone
*might* raise: if NotaEnum text encoding becomes part of the contract,
breaking text-side changes (renaming a variant, changing case
convention) become wire-side breaking changes. This is real, but the
opposite holds today too — when wire variants are added, the text-side
mirror has to be updated separately, which is itself a maintenance
hazard. Unifying the type means changes are visible at one site
instead of two; that's a stability *gain*, not a loss.

### 2.7 — Audience-scoped compile-time isolation

**The headline cost.** This is the one the prior `/137` framing
treated as a blocker; on examination it's actually a cost, and not
even a present one. The argument was: "front-end clients that depend
only on the base contract don't recompile on layered-crate churn."
But every front-end client already pulls `nota-codec` transitively
through `signal-core` (§1). Whatever recompile cost exists from
NOTA churn is already paid. Adding direct `NotaEnum` derives on
`signal-persona` enums adds *some* recompile triggers (any change to
`nota-derive`'s output forces signal-persona to re-derive), but the
marginal cost over today's transitive-dep cost is small.

### 2.8 — The contract-repo.md skill says otherwise

**A documentation cost, not a blocker.** The skill prescribes
wire-only contract crates. The workspace's actual code (signal-core)
doesn't follow that prescription. The skill is out of date relative
to the implementation; reconciliation has to go one way or the other.
Given the user's stated intent and the empirical workspace precedent,
the right move is updating the skill to match the looser policy:
*contract crates own typed wire records and may also derive text
projection on those records when the same type concept is consumed
by readable surfaces.*

### Verdict

**No structural blockers.** Every named concern is either a paid cost
(§2.5, §2.7), a documentation update (§2.8), or non-applicable
(§2.1-§2.4, §2.6). The user's instinct is right.

---

## 3 — What the centralization actually wins

Beyond the "one type per concept" discipline and the debuggability
bonus the user named, three concrete wins drop out:

**1. Drift impossibility.** Today, `signal_persona::ComponentKind`
and `schema::ComponentKind` are two types. Adding a variant to one
requires adding it to the other plus updating the `from_contract`
projection. The compiler catches missing match arms but not extra or
misspelled variants on the schema side. With one type, the drift can't
exist.

**2. Tests speak NOTA.** Round-trip tests in
`persona/tests/manager_store.rs` currently construct `EngineEventReport`
values by hand:

```rust
EngineEventBodyKind::ComponentSpawned   // schema-side type
```

With `NotaEnum` on the wire side, fixtures can use the wire types
directly *and* assert via NOTA text:

```rust
let event = decode_nota::<EngineEvent>(r#"
    EngineEvent{
      sequence: 42
      engine: "dev"
      source: Manager
      body: ComponentSpawned{ component: "persona-harness" }
    }
"#);
```

Readable fixtures replace constructor chains. This is exactly the
"falsifiable spec by example" discipline from
`skills/contract-repo.md` §"Examples-first round-trip discipline" —
applied to contracts that today can't speak NOTA directly.

**3. Logs and error messages.** Today, a panic like
`assert_eq!(left, right)` where `left: signal_persona::ComponentKind`
produces an opaque `Debug` output. With `NotaEnum` derived, the same
value can be formatted as canonical NOTA text — the same form
consumers see in fixtures and traces. Debug print and on-the-wire
form align. The `EngineEvent` log projection (`/24` §3) doesn't need
the `*Report` shadow types anymore — events log themselves directly.

These wins are visible at every consumer of `signal-persona`, not
just `persona`. Tests in `signal-persona-auth`, future tests in
`signal-persona-message` or `signal-persona-mind`, and any future
component that uses these contract types all gain readable NOTA forms.

---

## 4 — Migration shape

Two phases, both contained.

### Phase 1 — Land `NotaEnum`/`NotaRecord` on `signal-persona`

In `signal-persona/Cargo.toml`, add direct `nota-codec` dependency
(not strictly required since it's transitive through `signal-core`,
but explicit is clearer):

```toml
[dependencies]
nota-codec = { git = "https://github.com/LiGoldragon/nota-codec.git", branch = "main" }
rkyv = { version = "0.8", default-features = false, features = ["std", "bytecheck", "little_endian", "pointer_width_32", "unaligned"] }
signal-core = { git = "https://github.com/LiGoldragon/signal-core.git" }
```

For each of the five unit-variant enums, add `NotaEnum`:

```rust
use nota_codec::NotaEnum;

#[derive(
    Archive, RkyvSerialize, RkyvDeserialize,
    NotaEnum,
    Debug, Clone, Copy, PartialEq, Eq,
)]
pub enum ComponentKind { Mind, Router, Message, System, Harness, Terminal }
```

For each of the payload-bearing structs (`ComponentStatus`,
`EngineStatus`, etc.), add `NotaRecord` and ensure each field type
also implements `NotaEncode`/`NotaDecode` (the unit-variant enums
above will after the derive lands; payload types like `Vec<T>` and
`String` are already covered by `nota-codec`'s blanket impls; the
remaining work is `ComponentName` and `EngineGeneration`, which use
`NotaTransparent`).

### Phase 2 — Delete the schema-side mirrors

In `persona/src/schema.rs`:

- Delete `EnginePhase`, `ComponentKind`, `ComponentDesiredState`,
  `ComponentHealth`, `SupervisorActionRejectionReason` definitions
  (lines 40-78).
- Delete the five `from_contract` impl blocks (lines 369-430).
- Delete the `TextComponentName` / `TextEngineId` newtypes (lines
  6-38) once the contract-side types implement NOTA directly.
- Update `ComponentStatusRecord` and `EngineStatusReport` to hold
  contract types directly — no field-by-field conversion needed.

Estimated deletion: ~120 lines.

### Phase 3 — Refactor other contract crates incrementally

The same move applies to:
- `signal-persona-auth`'s enums (when the next pass touches them).
- `signal-persona-message`, `signal-persona-mind`, etc. (as those
  crates land contract additions).

This is *opportunistic*, not blocking. Each contract crate gains
`NotaEnum`/`NotaRecord` on its types as part of the next pass that
touches it. The policy is "new contract types derive NOTA from the
start; existing types upgrade on next-touch."

---

## 5 — Skill update required

`skills/contract-repo.md` needs updating to reflect the actual policy:

**Today's text (lines 49-62), out of date:**

> - **Front-end stability.** When a layered effect crate adds
>   per-verb payloads (e.g. signal-forge over signal), front-end
>   clients that depend only on the base contract don't recompile
>   on layered-crate churn. Audience-scoped compile-time isolation.

**Proposed text:**

> - **Front-end stability.** Contract crates depend only on what they
>   need to express the types' wire and text forms. `rkyv` provides
>   the wire shape; `nota-codec` provides the text projection. Both
>   are appropriate dependencies for contract crates whose types
>   appear in both wire frames and readable surfaces (NOTA logs,
>   fixtures, error messages). Layered effect crates that add
>   per-verb payloads still keep their own derives out of the base
>   contract.

And the "What goes in a contract repo" section's enumeration of
owned types should add:

> - `NotaEnum`/`NotaRecord`/`NotaTransparent` derives on the typed
>   wire records — contract types are readable as NOTA text directly,
>   without per-consumer mirror types. The same type IS the wire form
>   and IS the text form; consumers don't carry shadow types.

This update is workspace-skill work, in designer's lane. It lands
alongside Phase 1 (when the first signal contract starts deriving
NotaEnum on wire-side types as a deliberate policy choice, not a
signal-core-style accident).

---

## 6 — Combined plan with `/135` and `/137`

The three reports land in sequence on `persona`:

1. **`/138` Phase 1 — signal-persona side.** Add `NotaEnum`/`NotaRecord`
   to the five Pattern A enums + structs. Update `signal-persona`'s
   tests if any (none currently exist for NOTA round-trips, but adding
   them is the natural verification step).
2. **`/138` Phase 2 — persona side.** Delete Pattern A mirrors and
   `from_contract` projections from `schema.rs`. Update consumers to
   use contract types directly. ~120 lines deleted.
3. **`/137` — Pattern B fix.** Delete the operation-kind mirrors and
   their `from_kind` projections (which `/138` partly invalidates —
   if `NotaEnum` is the policy, the operation-kind enums in
   `engine_event.rs` derive it directly without going through
   `*Report` shadow types). ~110 lines deleted.
4. **`/135` — strum migration for `EngineEventBody`/`EngineEventSource`.**
   Add `strum::EnumDiscriminants`; delete `EngineEventBodyKind` /
   `EngineEventSourceKind` hand-written enums + projections. ~34
   lines deleted.

Total deletion across the three reports: **~264 lines** from
`schema.rs` plus its adjacent test fixtures. The remaining
`schema.rs` carries only the genuinely payload-transforming
projections (the `EngineEventBodyReport::from_event_body` block
that lifts contract types into NOTA-friendly record shapes — and
even those simplify once the contract types speak NOTA natively, so
the remaining schema-side work may be much less than today).

Phase 1 of `/138` blocks `/137` (since `/137` Pattern B's fix uses
the same "wire type derives NotaEnum" approach), but the work order
is straightforward: do `/138` Phase 1 first.

---

## 7 — One thing this report doesn't settle

The user's stated intent generalizes: *centralization is the design
value*. That value applies to every wire/text mirror in the workspace,
not just `signal-persona`. Two questions follow:

1. Should every existing wire-only contract crate (`signal-persona-auth`
   today, others as they exist) get `NotaEnum` derives in the
   *current* pass, or wait for opportunistic next-touch?
2. Should the eventually-self-hosting stack (`persona/ARCHITECTURE.md`
   §0.5) inherit this policy directly — wire and text always
   centralized on the same type — or is that a future re-decision?

Both are deferrable. `/138` recommends current-pass for `signal-persona`
(scope matched to the work `/137` and `/135` are doing) and
opportunistic for the rest. The eventually-self-hosting stack
inherits the *current* policy; that future re-decision is far enough
away that it can be made when the substrate work begins.

---

## 8 — Summary

`/137` §1.1 framed Pattern A as load-bearing duplication. It isn't.
The workspace's base contract crate (`signal-core`) already combines
`rkyv` and NOTA derives on contract types. `signal-persona`'s strict
wire-only-derive shape is the outlier. The user's instinct —
centralize, gain debuggability — is right; the skill's current text
describes a discipline the workspace doesn't actually follow.

No structural blocker. The migration is ~120 lines deleted in
`persona/schema.rs` plus ~10-15 lines of derives added across
`signal-persona`. Combined with `/137` (Pattern B) and `/135` (strum),
the three reports remove ~264 lines of duplication and unlock
NOTA-encodable contract messages for tests, logs, and debugging
across the entire `signal-persona` consumer set.

The `contract-repo.md` skill needs a parallel update naming the
policy correctly: contract crates own typed records and *both* their
wire and text projections; consumers don't carry shadow types.

---

## See also

- `reports/designer/137-operation-kind-mirrors-deduplication.md`
  §1.1 — the prior framing this report corrects, and the Pattern B
  half of the work that builds on the policy shift.
- `reports/designer/136-strum-enum-discriminants-proposal-review.md`
  §4 — the original flag of "the broader `from_contract` duplication
  as a separate future proposal"; this report is that proposal.
- `reports/designer/135-kind-enums-via-strum-enum-discriminants.md`
  — the strum migration that composes with this work.
- `reports/operator-assistant/108-kind-enum-pattern-survey.md` — the
  workspace-wide survey that named the operation-kind report
  mirrors and confirmed the pattern is rare.
- `/git/github.com/LiGoldragon/signal-core/Cargo.toml` line 16 — the
  empirical evidence that contract crates already depend on
  `nota-codec` (the "audience-scoped compile-time isolation" argument
  is already moot).
- `/git/github.com/LiGoldragon/signal-core/src/pattern.rs` lines 1-9
  — the workspace precedent for combining rkyv and `NotaEncode`/
  `NotaDecode` on the same contract types.
- `/git/github.com/LiGoldragon/signal-persona/src/lib.rs` lines 40-78
  — the five Pattern A enums that gain `NotaEnum` derives.
- `/git/github.com/LiGoldragon/persona/src/schema.rs` lines 40-78,
  369-430 — the ~120 lines of mirrors and `from_contract` projections
  that delete.
- `~/primary/skills/contract-repo.md` lines 49-62 — the workspace
  skill text that's out of date relative to the code, named in §5
  for parallel update.
- `~/primary/skills/rust/methods.md` §"One type per concept" — the
  workspace discipline the user's argument leans on.
- `~/primary/skills/abstractions.md` §"Find the structure that
  makes the special case dissolve into the normal case" — same.
- User message 2026-05-12 (this thread) — the recorded design
  intent in §0.
