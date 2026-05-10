# 107 — Contract enum naming pass: signal-persona-mind variant rename

*Designer report. Captures the deep enum pass on signal-persona-mind
that landed in commits `4505abab` (signal-persona-mind) and `5db412a6`
(persona-mind), plus the contract-coverage survey that informed it
and the remaining work queued for the next pass.*

---

## 0 · TL;DR

Per user instruction (claim+implement on contract enum work), did the
deep variant-rename pass on `signal-persona-mind`. The role/activity
variants were already noun-form; the memory-graph variants were the
remaining out-of-pattern cases — verb-shape (`Open`, `AddNote`,
`ChangeStatus`, `AddAlias`) and past-participle (`Opened`, `NoteAdded`,
`Linked`, `StatusChanged`, `AliasAdded`, `Rejected`). Renamed all 10
to match payload type names (the rest of the channel's convention).

| Repo | Commit | Status |
|---|---|---|
| `signal-persona-mind` | `4505abab` "contract: rename MindRequest/MindReply memory-graph variants to noun-form" | pushed; 35 round-trip tests passing |
| `persona-mind` | `5db412a6` "persona-mind: track signal-persona-mind variant rename" | pushed; cargo test passes (incl. weird_actor_truth, smoke, memory) |

**Survey finding**: no contract repos are missing for any current
relation in the Persona architecture. The only known gap (subscription
contract for persona-mind change-feeds) is queued for designer-assistant
pre-pass on designer/100 pins (bead `primary-qqb`). The signal-persona
placeholder cleanup (Ok / Generic / Mixed) had already landed in
operator's 14:33 commit before I started this pass.

**Queued for the next pass**: signal-persona-mind generic enum prefix
(`Kind` → `ItemKind`, `Status` → `ItemStatus`, `Priority` →
`ItemPriority`) — wider rename cascade across persona-mind consumers.
Bead filed.

---

## 1 · Survey of contract coverage

Before touching any code, I dispatched four parallel survey agents to
build a current picture of the architecture, with explicit instructions
to be skeptical of stale content and verify against `git log` /
`jj log`.

**Active contract repos** (per `~/primary/protocols/active-repositories.md`
+ verified via direct inspection):

| Repo | Relation | Naming health (post-14:34 sweep) |
|---|---|---|
| `signal-core` | Wire kernel (typed frames, envelopes, channel macro) | Good — `SemaVerb` is acceptable as the named universal verb spine |
| `signal` | Sema-ecosystem record vocabulary atop `signal-core` | Architectural ambiguity: still has parallel direct `Request`/`Reply` enums alongside `signal-core::Request<Payload>` kernel layering (DA/7 to-do #5; not blocking) |
| `signal-persona` | Persona-wide vocabulary (Authorization, Binding, Delivery, Harness, Lock, Message, Observation, Transition, Stream) | Mostly cleaned in commit `76629533` — `ReplyPayload::Ok` → `CommitAccepted`, `CommitOutcome::Generic` → typed-per-record variants, `Records::Mixed` → `RecordBatch`, `Slotted<Record>` → `SlottedRecord<RecordValue>` |
| `signal-persona-message` | message CLI ↔ router | Good — renamed in commit `8ea1e96a`; `MessageSubmission`, `SubmissionAccepted`, `InboxListing`, etc. |
| `signal-persona-system` | system observer ↔ router | Good — renamed in commit `809e032e`; `FocusSubscription`, `FocusSnapshot`, `ObservationTargetMissing`, etc. |
| `signal-persona-harness` | router ↔ harness | Good — renamed in commit `f64ff038`; `MessageDelivery`, `InteractionPrompt`, `DeliveryCancellation`, etc. |
| `signal-persona-mind` | mind/orchestration vocabulary | Mostly good post-`34257322` (role taxonomy) + `4505abab` (this pass — variant rename); minor weaknesses still queued (Q-app-3 below) |
| `signal-persona-terminal` | harness ↔ terminal backend | New, in flight (operator-assistant lock) |
| `signal-forge` | criome ↔ forge | Skeleton only; not in current persona scope |

**Verdict on coverage**: every Persona runtime relation that exists
today has a contract repo for it. No gaps requiring NEW contract
creation in this session.

---

## 2 · The variant rename pass — what changed

Before:

```rust
signal_channel! {
    request MindRequest {
        // …role/activity variants (already noun-form)…
        Open(Opening),
        AddNote(NoteSubmission),
        Link(Link),
        ChangeStatus(StatusChange),
        AddAlias(AliasAssignment),
        Query(Query),
    }
    reply MindReply {
        // …role/activity replies (already noun-form)…
        Opened(OpeningReceipt),
        NoteAdded(NoteReceipt),
        Linked(LinkReceipt),
        StatusChanged(StatusReceipt),
        AliasAdded(AliasReceipt),
        View(View),
        Rejected(Rejection),
    }
}
```

After:

```rust
signal_channel! {
    request MindRequest {
        // …role/activity variants…
        Opening(Opening),
        NoteSubmission(NoteSubmission),
        Link(Link),
        StatusChange(StatusChange),
        AliasAssignment(AliasAssignment),
        Query(Query),
    }
    reply MindReply {
        // …role/activity replies…
        OpeningReceipt(OpeningReceipt),
        NoteReceipt(NoteReceipt),
        LinkReceipt(LinkReceipt),
        StatusReceipt(StatusReceipt),
        AliasReceipt(AliasReceipt),
        View(View),
        Rejection(Rejection),
    }
}
```

**Why this matters**: variant-name = payload-name is the convention
the rest of the channel follows (`RoleClaim(RoleClaim)`,
`ActivitySubmission(ActivitySubmission)`, `ClaimAcceptance(ClaimAcceptance)`,
etc.). Future agents reading the macro see one rule, not two; consumers
pattern-matching on a variant get the same name they would get
constructing one.

**Cascade**: the rename touched 7 consumer files in persona-mind
(`src/memory.rs`, `src/actors/{dispatch,domain,store}.rs`,
`tests/{actor_topology,memory,weird_actor_truth}.rs`) plus
`signal-persona-mind/tests/round_trip.rs`. All updated; all 35 contract
round-trip tests pass; all persona-mind tests pass (including the 8
weird-actor-truth tests).

---

## 3 · Queued for the next pass

### Q-app-4. Generic enum prefix in signal-persona-mind — `Kind` / `Status` / `Priority` → `Item*`

Per `~/primary/reports/designer-assistant/7-contract-relation-naming-survey.md`
§"signal-persona-mind": *"`Kind`, `Status`, and `Priority` are too
generic outside their local section. Prefer `ItemKind`, `ItemStatus`,
and `ItemPriority`."*

Current state in `/git/github.com/LiGoldragon/signal-persona-mind/src/lib.rs`:

```rust
pub enum Kind { Task, Defect, Question, Decision, Note, Handoff }
pub enum Status { Open, InProgress, Blocked, Closed, Deferred }
pub enum Priority { Critical, High, Normal, Low, Backlog }
```

These are used as field types throughout `Item`, `Opening`,
`StatusChange`, `StatusChangedEvent`, and as filter cases in
`QueryKind::ByKind`, `QueryKind::ByStatus`. The rename is wide because:

- `Kind` collides with `EdgeKind` and `QueryKind` (different domains
  in the same crate).
- `Status` is a common Rust word (`std::process::ExitStatus`); the
  bare name is ambiguous.
- `Priority` is generic across many domains.

**Cascade**: ~30 sites across `signal-persona-mind/src/lib.rs`,
`signal-persona-mind/tests/round_trip.rs`, and persona-mind consumers
(`src/memory.rs`, `src/actors/view.rs`, several tests).

**Cannot use plain sed** because `Kind::Task` is fine to rewrite but
`EdgeKind::DependsOn` and `QueryKind::Ready` need to be left alone.
Surgical Edits required.

### Q-app-5. `Body` field type — context-specific newtypes

Per DA/7: *"`Body` is too broad for a central work graph. Consider
`ItemBody`, `NoteBody`, or `TextBody` depending on whether one type is
intended to span all text-bearing records."*

Current: `pub struct Body(String)` is used by `Item.body`, `Note.body`,
`Edge.body`, `Opening.body`, `NoteSubmission.body`, `Link.body`,
`StatusChange.body`, `StatusChangedEvent.body`.

Two options:
- **`TextBody(String)`** — single newtype, just renamed for clarity. Smallest change.
- **Per-context newtypes** (`ItemBody`, `NoteBody`, `EdgeBody`) — sharper types but more wire-format duplication.

Recommendation: `TextBody` for now. The single-newtype shape preserves
wire compatibility while making the name say what it is.

### Q-app-6 (small). `Records` enum in signal-persona

Per DA/7: *"`Records` is convenient, but it weakens the type boundary."*
The 14:33 sharpening pass renamed the `Mixed` variant to `RecordBatch`,
but the enum itself is still called `Records`. Consider:

- enum `Records` → `RecordBatch` (matching the most common variant name)
- the catch-all variant becomes `RecordBatch::Mixed(Vec<Record>)`

Cascade: only signal-persona's own files; no external consumers found.

---

## 4 · What I deliberately did NOT touch

- **`signal-persona-subscription`** — would be a new contract for
  persona-mind change-feeds. Per user decision (Q-dec-4 in
  `~/primary/reports/designer/106-actor-discipline-status-and-questions.md`),
  designer-assistant runs the pre-pass on designer/100's 5 pins first
  (bead `primary-qqb`). Don't pre-empt the pre-pass.

- **`signal` vs `signal-core` kernel rationalization** (DA/7 to-do
  #5) — architectural ambiguity (parallel `Request`/`Reply` enums in
  `signal` alongside the `signal-core` kernel). Not blocking current
  work; defer to a focused pass.

- **persona-mind `ARCHITECTURE.md`** — left in working tree. Pre-existing
  changes from operator that document the daemon decision and lock-file
  retirement; not mine to commit.

---

## 5 · Bead trail

- **Filed during this session**: `primary-rz1` (P2,
  operator-assistant) — generic-name polish: `Kind`→`ItemKind`,
  `Status`→`ItemStatus`, `Priority`→`ItemPriority`, `Body`→`TextBody`
  in signal-persona-mind; `Records`→`RecordBatch` in signal-persona.
- **Already filed**: `primary-qqb` (P1, designer-assistant pre-pass on
  designer/100 pins; covers subscription contract scope), `primary-9yq`
  (P2, operator-assistant rename `*Supervisor` → `*Phase` in persona-mind),
  `primary-9iv` (P1, Rust persona-mind implementation wave; design
  constraints recorded as notes).

---

## 6 · Recommendation

The variant rename pass that landed today is the highest-value
single naming change for `signal-persona-mind` — it removed the
internal inconsistency between role/activity vectors (already
noun-form) and memory-graph vectors (verb/past-participle). All
35 contract round-trip tests + all persona-mind tests pass.

The remaining items (`Kind`/`Status`/`Priority` prefix; `Body` newtype
clarification; `Records` enum rename in signal-persona) are smaller
and don't share a single theme — they're polish, not the core
discipline. A focused follow-up bead can sweep them.

---

## See also

- `~/primary/reports/designer/106-actor-discipline-status-and-questions.md`
  — the decisions that authorized this work (Q-dec-1 daemon, Q-dec-2
  validation split, etc.)
- `~/primary/reports/designer-assistant/7-contract-relation-naming-survey.md`
  — the canonical naming standard + to-do list this pass partially
  satisfies (to-do #2 root enum rename, partial)
- `~/primary/reports/operator/105-command-line-mind-architecture-survey.md`
  — operator's parallel survey of the implementation gaps (NOTA, durable
  state, role/activity flows, ID mint)
- `~/primary/skills/contract-repo.md` §"Contracts name relations" — the
  doctrine this pass applies
- `~/primary/skills/naming.md` — the verb-belongs-to-noun rule
