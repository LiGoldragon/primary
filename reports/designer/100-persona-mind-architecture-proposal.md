# 100 — Persona-mind architecture — designer companion

*Designer report. Operator/101
(`~/primary/reports/operator/101-persona-mind-full-architecture-proposal.md`)
is the architecture; operator/100
(`~/primary/reports/operator/100-persona-mind-central-rename-plan.md`)
is the consolidation that grounds it. This designer companion
contributes only what operator/101 explicitly leaves open or
doesn't pin. The first version of this report (commit
24d47bd) carried push backs that were wrong-shaped — see
§"Retracted from prior draft" below.*

---

## 0 · TL;DR

Operator/101 is the architecture: persona-mind is the central
state component (role coordination + memory/work graph in one
place); the actor tree (`MindRootActor` / `MindIngressActor`
/ `MindStateActor` / `ViewActor` / `SubscriptionActor`) is the
component's structure across phases; lock files are retired
(Phase 3 = typed read views, not projections); `mind.redb`
holds the typed truth via `persona-sema`.

This report contributes five concrete pins for what
operator/101 names but doesn't fully specify:

- §1 — `DisplayId` mint algorithm
- §2 — concrete sema table key shapes
- §3 — caller-identity mechanism (resolves operator/101 §8 +
  §15's open issue)
- §4 — `mind.redb` path with env override
- §5 — subscription contract sketch (Phase 5 preview)

§6 names open questions worth surfacing before Phase 2.

---

## 1 · `DisplayId` mint algorithm

Current contract has `DisplayId(String)`
(`/git/github.com/LiGoldragon/signal-persona-mind/src/lib.rs:441`)
without a generation spec. Pin before Phase 2 sema persistence.

```rust
fn mint_display_id(item: StableItemId, existing: &DisplayIndex) -> DisplayId {
    // base32-crockford encoding of BLAKE3(StableItemId).
    // Crockford avoids 0/O 1/I/l confusion — important for
    // human transcription and LLM tokenisation.
    let full = base32_crockford(blake3(item.as_bytes()));
    // Try lengths 3, 4, 5, ... until uncollided.
    for len in 3.. {
        let candidate = DisplayId::new(&full[..len]);
        if !existing.contains(&candidate) {
            return candidate;
        }
    }
    unreachable!("BLAKE3 has 256 bits; collision exhaustion impossible");
}
```

Examples (illustrative): `9iv`, `kxa`, `ffj` (3-char default);
`9ivx` (collision-extended).

No workspace prefix on the wire (`9iv`, not `mind-9iv`, not
`primary-9iv`). Imported BEADS aliases (`primary-9iv` style)
preserve the old token via `ExternalAlias` records;
resolution goes through the `ALIASES` index, not the
`DISPLAY_IDS` index.

---

## 2 · Concrete sema table key shapes

Operator/101 §6 names tables; per
`~/primary/reports/assistant/90-rkyv-redb-design-research.md`
§"Do Not Store Arbitrary rkyv Archives as redb Keys",
keys are designed bytes, not rkyv-encoded. Proposed key
shapes:

| Table | Key | Value | Notes |
|---|---|---|---|
| `CLAIMS` | `(role_byte, scope_kind_byte, scope_bytes)` | `Claim` | Composite key; ordered for prefix scans by role then by scope kind |
| `HANDOFFS` | `OperationId` bytes | `Handoff` | One row per handoff |
| `ACTIVITIES` | `EventSeq(u64)` BE bytes | `Activity` | Append-only; chrono order |
| `ITEMS` | `StableItemId` bytes | `Item` | Direct lookup |
| `EDGES_BY_SOURCE` | `(StableItemId, edge_kind_byte, EdgeTargetBytes)` | `Edge` | Outbound graph index |
| `EDGES_BY_TARGET` | `(EdgeTargetBytes, edge_kind_byte, StableItemId)` | `Edge` | Inbound graph index |
| `NOTES_BY_ITEM` | `(StableItemId, EventSeq)` | `Note` | Per-item chrono |
| `ALIASES` | `ExternalAlias` bytes | `StableItemId` | Reverse lookup: imported alias → native item |
| `DISPLAY_IDS` | `DisplayId` bytes | `StableItemId` | Reverse lookup: short id → native item |
| `EVENTS` | `EventSeq(u64)` BE bytes | `Event` | The truth layer |
| `META` | `&'static str` | `Vec<u8>` | `schema_version`, `event_seq_counter`, `operation_id_counter`, … |

Type-discriminator bytes (`role_byte`, `scope_kind_byte`,
`edge_kind_byte`) are 1-byte enum tags chosen at the
application layer, documented in `persona-mind/src/tables.rs`,
and protected by schema-version bumps. Big-endian encoding for
numeric keys gives lexicographic ordering equal to numeric
ordering — important for range scans on `EVENTS` and
`ACTIVITIES`.

---

## 3 · Caller-identity mechanism — resolves operator/101 §8 + §15

Operator/101 §8 surfaces the open issue:

> *"Current memory mutations need a reliable actor identity.
> The clean solution is a common request envelope:
> `MindEnvelope { actor, request }`. If the CLI derives actor
> identity from the role configuration, the actor field must
> still enter the typed state transition before persistence."*

Operator/101 §15 hedges to *"Add or confirm a common request
envelope carrying actor identity."*

Concrete proposal — three-layer caller-identity resolution
plus dispatcher-side enforcement:

### Resolution order (CLI side)

The `mind` CLI determines the calling actor in priority order:

1. **`MIND_ACTOR` env var** — explicit override; primarily
   for test harnesses and one-shot pipelines.
2. **`~/.config/persona/actor.toml`** — per-machine default:
   ```toml
   actor = "designer"
   ```
3. **Process-ancestry resolver** — same shape
   `persona-message`'s `actors.nota` resolver uses
   (`/git/github.com/LiGoldragon/persona-message/src/resolver.rs`).
   Walks the process tree; matches PID against registered
   actor bindings; returns the matched `ActorName`.

If none of these yields an `ActorName`, the CLI exits with a
typed error (no implicit "unknown" actor).

### Envelope shape (wire)

Operator/101 §8's `MindEnvelope { actor, request }` is the
right shape. The CLI constructs it:

```rust
MindEnvelope {
    actor:   resolve_caller_identity()?,    // from layers above
    request: parse_argv_into_mind_request()?,
}
```

### Dispatcher enforcement (state-actor side)

The `MindStateActor` reads `envelope.actor` and inserts it
into the `EventHeader.actor` of every event the operation
appends. The reducer's typed request types (`Opening`,
`NoteSubmission`, `Link`, `StatusChange`, `AliasAssignment`,
`Query`) carry no `actor` field — the type system enforces
that the agent's payload cannot supply or override actor
identity. Per ESSENCE §"Infrastructure mints identity, time,
and sender": the wire carries the envelope; the *event* that
gets persisted carries the dispatcher-stamped actor.

```mermaid
flowchart LR
    cli["mind CLI"] -->|"MIND_ACTOR / config / ancestry"| resolve["resolve_caller_identity()"]
    resolve -->|"ActorName"| envelope["MindEnvelope { actor, request }"]
    envelope -->|"signal-persona-mind frame"| ingress["MindIngressActor"]
    ingress -->|"envelope"| state["MindStateActor"]
    state -->|"insert envelope.actor"| header["EventHeader.actor"]
    header --> event["persisted Event"]
```

### Architectural-truth witness

| Witness | Catches |
|---|---|
| Request body cannot supply actor | Compile-fail — `Opening`, `NoteSubmission`, `Link`, `StatusChange`, `AliasAssignment`, `Query` literally have no `actor` field |
| `EventHeader.actor` equals `MindEnvelope.actor` | Synthetic-envelope test — submit `MindEnvelope { actor: ActorName::new("designer"), request: Opening { … } }`; assert resulting `ItemOpenedEvent.header.actor == ActorName::new("designer")`; vary actor; assert lockstep |

### Trust note

`MIND_ACTOR` env override is trust-on-first-use; in a
single-user workspace this is fine. For multi-user contexts,
fall through to process ancestry which is harder to spoof
(requires controlling a parent process registered as that
actor). Actor authentication beyond ancestry is deferred —
operator/101's `signal-persona-mind` doesn't carry an
`AuthProof` shell yet, and adding one is a coordinated schema
bump for a later wave.

---

## 4 · `mind.redb` path with env override

Operator/101 §6 says workspace-local first. Pin the exact
path + env override before Phase 2:

| Source | Path | When |
|---|---|---|
| `MIND_DB_PATH` env var | (override) | Test isolation; CI; future multi-workspace |
| Default | `~/primary/.mind/mind.redb` | The standard path |

`~/primary/.mind/` is gitignored. The path mirrors per-workspace
shape `<role>.lock` files used today (until they're retired in
Phase 3). System-level multi-workspace deployment can move the
location behind configuration without changing the contract.

---

## 5 · Subscription contract sketch — Phase 5 preview

Operator/101 §14 Phase 5 names "Post-commit subscriptions"
without fixing the wire shape. Worth sketching now so
consumers (router, harness, future external integrations) can
plan for it:

```rust
pub enum MindRequest {
    // …existing 12…
    Subscribe(Subscribe),
    Unsubscribe(Unsubscribe),
}

pub enum MindReply {
    // …existing…
    SubscriptionAccepted(SubscriptionAccepted),
    SubscriptionEvent(SubscriptionEvent),
    UnsubscribeAcknowledgment(UnsubscribeAcknowledgment),
}

pub struct Subscribe {
    pub filter: SubscribeFilter,
}

pub enum SubscribeFilter {
    AllEvents,
    Coordination,                       // role/handoff/activity changes
    Memory,                             // item/edge/note/alias changes
    ItemsOfKind(Kind),
    EventsForItem(ItemReference),
}
```

Per `~/primary/skills/push-not-pull.md` §"Subscription
contract" — every subscription emits the producer's current
state on connect, then deltas. For mind:

| Filter | On-connect emission | Then deltas |
|---|---|---|
| `AllEvents` | Every event from a starting `EventSeq` (default current+1) | Every committed event |
| `Coordination` | Current `RoleSnapshot` | Coordination-touching events |
| `Memory` | Current `View` snapshot | Memory-touching events |
| `ItemsOfKind(k)` | Current `Item` projections of kind `k` | Events affecting matching items |
| `EventsForItem(ref)` | Recent events for the item | Events affecting the item |

Phase 5 lands when push-not-pull discipline (the subscription
substrate behind future router/system integrations) genuinely
requires it. Pinning the wire shape now means consumers can
write against the future contract today.

---

## 6 · Open questions worth surfacing

Concerns that need designer/operator dialogue before Phase 2,
beyond what operator/101 §15 already lists:

1. **Item kind `Note` vs Note records on items.** Contract has
   `Kind::Note` (an item kind) AND a `Note` record (commentary
   on any item). Standalone observations → `Kind::Note` items;
   commentary on tracked work → `Note` attached to the work
   item. Worth documenting in `signal-persona-mind/ARCHITECTURE.md`
   so an agent doesn't have to reverse-engineer the convention.

2. **`Status::Blocked` vs `EdgeKind::DependsOn` open blocker.**
   Two ways to express "this can't proceed": status flag or
   incoming open dependency. Lean: `Blocked` is for *external*
   blockers (waiting on a human, infra); `DependsOn` on an
   open item is *internal* blocking. Both legitimate; document
   the distinction.

3. **`HANDOFFS` table semantics.** Operator/101 §6 names the
   table; operator/101 §7 says *"a handoff is not a release
   plus a claim. It is a typed transition with one event that
   preserves provenance."* Is `HANDOFFS` append-only history
   with current pending state derivable, or live mutable
   pending-handoff state? Lean append-only.

4. **CLI sub-shims.** Acceptable as long as they lower into
   the canonical `mind '<NOTA record>'` form. Operator/101
   §11 already names the rule. Pin the sub-shim set before
   Phase 4; suggest `mind ready` / `mind open <kind> <title>`
   / `mind note <id> <body>` as the v1 set.

5. **`Body(String)` typed migration.** Same `primary-b7i`
   wave that touches `signal_persona::Message::body` and
   `signal_persona_harness::DeliverMessage::body`. Mind's
   `Body(String)` field travels with that migration; no
   separate handling needed.

---

## Retracted from prior draft

The first version of this report (commit 24d47bd) carried
five push backs in §2 that were wrong-shaped:

- **§2.1 — actor framing in Phase 1.** The push back conflated
  CLI-request lifetime with persona-mind's component
  structure. The actor tree (operator/101 §4) describes the
  *component's* shape across all phases; the CLI is one
  short-lived access path. Starting with actors in Phase 1
  avoids a structural refactor at Phase 5 when subscriptions
  land. Retracted.
- **§2.3 — `Status::Closed` carries no `Resolution`.** The
  push back proposed adding closure metadata to `Status`, but
  closure relationships (`Duplicates`, `Supersedes`,
  `Answers`) already live on `EdgeKind`. The current
  contract's design (flat Status; semantic relationships on
  edges) is intentional and the right separation. Retracted.
- **§2.5 — flat `MindRequest`.** Already light; recommended
  stay-flat; no real disagreement. Dropped from this version
  because there's nothing to push back on.

The remaining /98 §2.2-derived observations (`EventHeader.actor`
filling from a trustworthy source; `Body(String)` flagging for
typed-Nexus migration) appear in this revised version where
they're load-bearing — §3 (caller-identity mechanism) and §6
(open questions) respectively.

The prior draft also referenced "lock-file projections" as
mind's compatibility output. Operator/101 has been updated
since: lock files are retired entirely (Phase 3 is "Typed
read views"; §7 says *"Mind does not keep lock files alive as
projections. Old lock files are migration artifacts only."*).
This revised version aligns with that direction throughout.

---

## See also

- `~/primary/reports/operator/100-persona-mind-central-rename-plan.md`
  — the consolidation that grounds operator/101.
- `~/primary/reports/operator/101-persona-mind-full-architecture-proposal.md`
  — the architecture this report companions.
- `~/primary/reports/assistant/90-rkyv-redb-design-research.md`
  §"Do Not Store Arbitrary rkyv Archives as redb Keys" —
  the basis for §2 explicit byte-key shapes.
- `~/primary/reports/designer/97-persona-system-vision-and-architecture-development.md`
  §6 — typed Nexus body migration (primary-b7i); applies to
  mind's `Body(String)` fields too (§6 here).
- `/git/github.com/LiGoldragon/signal-persona-mind/src/lib.rs`
  — the contract today; lines cited.
- `/git/github.com/LiGoldragon/persona-message/src/resolver.rs`
  — the process-ancestry resolver shape §3 reuses.
- `~/primary/ESSENCE.md` §"Infrastructure mints identity, time,
  and sender" — the rule §3 dispatcher-enforcement applies.
- `~/primary/skills/push-not-pull.md` §"Subscription contract"
  — the on-connect-current-state rule §5 follows.
