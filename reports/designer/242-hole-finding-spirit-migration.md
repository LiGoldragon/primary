# 242 — Hole-finding by sketching the signal-persona-spirit migration

*Sketched the contract-local-verbs refactor of `signal-persona-spirit`
+ `owner-signal-persona-spirit` against the spec in `/241`. Surfaces
ten holes — places the spec doesn't say what to do, or where the
spec's rules collide with the contract's real shape. None are
blockers for landing the pilot (`signal-repository-ledger`), but
several need answers before per-component refactors cascade.
Component picked because it has the broadest variety of operation
shapes (asserts, reads, subscriptions, retracts, owner contract,
multiple relations bundled in one channel).*

## 0 · TL;DR

Ten holes found. By severity:

**Architecture-level (need design before cascade)**:
1. The verb-form rule **produces collisions** when a domain word is both verb and noun — `State` in spirit is the test case (psyche "states" intent; spirit observes "state").
2. **Reply / event variant naming has no documented rule.** The verb-form rule covers operation roots but is silent on what shape reply and event variants should take.
3. **Compound actions don't fit the single-verb model.** `DrainAndStopOrder` — one action that does two things — has no clean verb-form rendering.
4. **The observer hook mechanism is unspecified.** /241 says every daemon publishes operations and Sema effects to optional observers but doesn't say HOW (built-in macro op? separate contract? convention?).
5. **The Sema lowering executor pattern has no library or trait.** Every daemon will roll its own; conventions will drift.

**Convention-level (less urgent but real)**:
6. **Stream-close operation disambiguation** — if multiple operations take the same token type, the macro can't tell which closes the stream.
7. **Verb-pair convention not documented** — Watch/Unwatch, Subscribe/Unsubscribe, Open/Close. Migration guide accepts any verb but doesn't say which.
8. **Per-operation reply mapping convention not documented** — multi-op requests produce positional replies; which reply variant for which op isn't spelled out.
9. **Multi-op atomicity vs partial commit** — current spec says NonEmpty<Payload> is atomic, but a daemon might want to accept some ops and reject others. Not addressed.
10. **Suffix-noun discipline on owner contracts** — `*Order` suffix on every variant (StartOrder, RetireOrder) is redundant ceremony per the no-redundant-ancestry rule. Not specifically called out in /241.

## 1 · Method

Walked through what each operation in `signal-persona-spirit` and
`owner-signal-persona-spirit` becomes under the /241 spec. Where
the spec gave a clean answer, I noted the result. Where the spec
left the question open, ambiguous, or actively conflicting, I
recorded a hole. Contract code read from `main` of both repos at
the time of this report.

## 2 · Sketch — signal-persona-spirit after migration

Current shape (live `main`):

```rust
signal_channel! {
    channel Spirit {
        request SpiritRequest {
            Assert Statement(Statement),
            Assert Entry(Entry),
            Match StateObservation(StateObservation),
            Match RecordObservation(RecordObservation),
            Match QuestionPending(QuestionPending),
            Subscribe SubscribeState(StateSubscription) opens StateStream,
            Retract StateSubscriptionRetraction(StateSubscriptionToken),
            Subscribe SubscribeRecords(RecordSubscription) opens RecordStream,
            Retract RecordSubscriptionRetraction(RecordSubscriptionToken),
        }
        reply SpiritReply { … }
        event SpiritEvent { … }
        stream StateStream { … }
        stream RecordStream { … }
    }
}
```

Proposed shape under /241 (with holes marked **★**):

```rust
signal_channel! {
    channel Spirit {
        operation State(Statement),       ★ ← but State is also the noun "spirit observing state"
        operation Record(Entry),
        operation Observe(Selection),      ← collapses StateObservation + RecordObservation + QuestionPending under one Query/Observe verb (or do they stay as three? — hole 6)
        operation Watch(Subscription) opens RecordStream,
        operation Unwatch(RecordSubscriptionToken),
        operation ObservePresence opens PresenceStream,  ★ ← awkward; the "psyche state" stream needs a different word than "state"
        operation UnobservePresence(PresenceSubscriptionToken),
        ...
    }
    reply SpiritReply { ... }
    event SpiritEvent { ... }
    stream RecordStream { ... }
    stream PresenceStream { ... }
}
```

The sketch produces tensions immediately. See holes 1, 6, 7.

## 3 · Sketch — owner-signal-persona-spirit after migration

Current shape:

```rust
signal_channel! {
    channel OwnerSpirit {
        request OwnerSpiritRequest {
            Mutate StartOrder(StartOrder),
            Mutate DrainAndStopOrder(DrainAndStopOrder),
            Mutate ReloadBootstrapPolicyOrder(ReloadBootstrapPolicyOrder),
            Mutate RegisterIdentity(RegisterIdentity),
            Retract RetireIdentity(RetireIdentity),
        }
        reply OwnerSpiritReply { … }
    }
}
```

Proposed:

```rust
signal_channel! {
    channel OwnerSpirit {
        operation Start(StartParameters),                 ← Order suffix drops (hole 10)
        operation DrainAndStop(DrainAndStopParameters),   ★ ← compound verb (hole 3)
        operation ReloadBootstrapPolicy,                  ← unit payload? Or a NoArgs marker?
        operation Register(Identity),
        operation Retire(IdentityName),
    }
}
```

## 4 · The ten holes

### Hole 1 — Verb-form collision: `State`

The psyche's "state" is overloaded:
- **As verb**: "to state" — what the psyche does when articulating intent. Verb-form replaces the current noun `Statement`.
- **As noun**: "the psyche's state" — presence, focus area, what spirit observes about the psyche. Used in `StateObservation`, `StateSubscription`, `StateStream`.

Both meanings live in `signal-persona-spirit`. The proposed sketch needs `operation State(Statement)` (verb) AND something like `operation ObservePresence` (renamed to avoid State-as-noun collision). The verb-form rule produces the collision.

**Options**: (a) rename one — call psyche's "state" something else (Presence? FocusContext? Mood?); (b) use a different verb for stating intent (Articulate? Declare? Express?); (c) accept the overload because English does. **The spec is silent.**

### Hole 2 — Reply / event variant naming convention

Current spirit reply: `RecordAccepted`, `StateObserved`, `RecordsObserved`, `StateSubscriptionOpened`, `RecordSubscriptionRetracted`. These are past-participles describing what happened.

The /241 verb-form rule covers operation roots but says nothing about reply or event variants. By convention, reply variants seem to be **past-tense outcomes** (X was Accepted, Y was Observed, Z was Captured). Event variants are similar.

**Hole**: this convention isn't documented in /241 or `skills/naming.md`. The next agent designing a contract will either invent their own convention or copy from spirit.

**Specifically open**:
- Should reply variants be 1:1 with request operations? (`operation Submit` → reply `Accepted`? Or `Submitted`?)
- Do reply variants describe success outcomes only, or include failures? (RequestRejectionReason::Internal covers some; what about domain-level rejections?)
- Past-tense vs. result-shape? `Accepted` (past) vs `Acceptance` (noun) vs `Receipt` (alternate noun)?

### Hole 3 — Compound actions

`DrainAndStopOrder` is one atomic action with two verbs in its name. The verb-form rule wants a single verb. Three options surface:

- **Single verb capturing the spirit**: `Stop(StopParameters { graceful: true })`. The "drain" is part of stop semantics.
- **Different single verb**: `Drain(...)` — implying the component stops after draining. Names what the daemon WAITS for, not what it does at end.
- **Compound verb**: `DrainAndStop(...)` — agglutinated. Awkward but explicit.

**Hole**: spec doesn't address compound actions. Each agent will pick differently.

Similar candidates elsewhere: `LoadAndValidate`, `FetchAndCache`, `CompileAndDeploy`.

### Hole 4 — Observer hook mechanism

/241 §"E. Observer hook" says every daemon publishes its inbound contract operations and outbound Sema effects to optional observers, subscribed via the public socket. But it doesn't say HOW:

- Is the observer subscription a **built-in operation** every contract gets through the macro?
  ```
  operation Observe(ObserverFilter) opens ObserverStream
  ```
  If yes, the macro must inject this — and every contract crate gets it for free. Cost: ObserverFilter / ObserverStream become workspace-wide types.
- Is it a **separate contract** (`signal-observe`) that daemons implement?
  Cost: daemons depend on signal-observe AND their own contract; observers know they're subscribing to a "well-known" channel.
- Is it **per-contract convention** (each contract author opts in)?
  Cost: drift; not every daemon has it; persona-introspect has to learn each contract's mechanism.

This is the biggest architectural hole. The /241 guide intends a uniform observer pattern but doesn't deliver one.

### Hole 5 — Sema lowering executor pattern

/241 §5 sketches a daemon handler that converts contract ops into `Vec<SemaOperation>`. But:

- No typed `Lowering` trait.
- No skeleton library for the executor pattern.
- No documented atomicity guarantees (does fanning Submit → [Assert, Mutate] commit atomically?).
- No documented error model (which `RequestRejectionReason` for which failure class?).
- No documented retry semantics.

Each daemon will roll its own. Conventions will drift across components. The Sema layer should not be re-invented per daemon.

### Hole 6 — Stream-close operation disambiguation

The macro (per /138) infers the close-op from payload type matching the stream's token type. Spirit has two streams: `StateStream` (token `StateSubscriptionToken`) and `RecordStream` (token `RecordSubscriptionToken`). Two different token types, so no ambiguity for spirit specifically.

**But the model has no general escape**: if a contract has two streams that share a token type (e.g., a generic `SubscriptionToken` used by multiple stream kinds), the macro can't tell which close-op closes which stream. The spec assumes per-stream unique token types, which is reasonable but not explicit.

### Hole 7 — Verb-pair convention (Watch/Unwatch, etc.)

`/241` mentions Watch/Unwatch/Detach/Cancel as candidate close-verbs but doesn't pick. Each contract author picks differently:
- `Watch` / `Unwatch` — most natural inverse pair.
- `Subscribe` / `Unsubscribe` — but Subscribe collides with the old SignalVerb name; also clunky.
- `Open` / `Close` — generic.
- `Attach` / `Detach` — physical metaphor.
- `Start` / `Stop` — collides with lifecycle verbs.

Spirit's current `SubscribeRecords` / `RecordSubscriptionRetraction` becomes... `Watch` / `Unwatch`? `Subscribe` / `Unsubscribe`? Convention is contract-author choice. Reads ok, but cross-contract inconsistency will accumulate.

### Hole 8 — Per-operation reply mapping

Multi-op requests produce positional replies via `Reply::Accepted.per_operation`. But the contract's reply enum has many variants; the spec doesn't say which reply variant maps to which request op.

For spirit, sketch: a multi-op request `[(State stmt1) (Record entry1) (Observe selection1)]` produces a reply with three SubReply slots. What's in each slot?

- Slot 0 (State): `Accepted(StatementAccepted)` or `Rejected(...)`?
- Slot 1 (Record): `Accepted(RecordCaptured)` or `Rejected(...)`?
- Slot 2 (Observe): `Observed(RecordsObserved)` or `Rejected(...)`?

Convention: each op produces ONE reply, picked from the contract's reply enum by op type. But this isn't enforced by the macro or documented in /241. **Each contract author will pick differently**.

### Hole 9 — Multi-op atomicity vs partial commit

Current model: `NonEmpty<Payload>` is atomic (commit all or abort all). But real daemons may want partial commit — e.g., a 3-op request where op-1 succeeds, op-2 fails validation, op-3 doesn't run.

The current spec offers two outcomes (Accepted with all results vs Rejected with one reason). There's no middle ground for "ops 1 and 3 accepted, op 2 rejected, all rolled back" or "ops 1 and 3 accepted, op 2 skipped." The atomicity guarantee is implicit.

**Hole**: is atomicity required across multi-op? If so, where does it bind (kernel? daemon? sema-engine)? The spec is silent.

### Hole 10 — Owner-contract suffix discipline

Current owner-spirit variants: `StartOrder`, `DrainAndStopOrder`, `ReloadBootstrapPolicyOrder`, `RegisterIdentity`, `RetireIdentity`. The `*Order` suffix is redundant — the daemon receives orders by definition on the owner socket. Per the no-redundant-ancestry rule, drop the suffix.

**Hole**: this rule applies to the broader owner-contract pattern. Should `/241` explicitly call out: "*Order, *Request, *Command suffixes on owner-contract variants are redundant ceremony — drop them"? Currently the rule applies via the general no-redundant-ancestry rule but isn't specifically named for owner contracts.

## 5 · Holes specific to signal-persona-spirit (vs cross-cutting)

Hole 1 (State collision) is the most spirit-specific. The others are cross-cutting and will appear in any contract.

Within spirit, two more open shapes worth surfacing before operator picks up:

**Open question on Statement vs Entry distinction.** Currently spirit has two assert-shaped ops: `Statement` (psyche utterance) and `Entry` (agent-typed record). Both record intent into spirit's state. Under verb-form:
- `State(Statement)` — psyche speaking.
- `Record(Entry)` — agent submitting typed record.

But semantically, these are two paths into the same store. Spirit's classifier eventually translates `Statement` into `Entry` (per /232 §"LLM mediation is intrinsic"). Are they really two verbs, or are they two payload variants under one verb (`Capture(Statement|Entry)`)?

**Open question on the three Match-shaped reads.** `StateObservation`, `RecordObservation`, `QuestionPending`. Under verb-form, sketch options:
- Collapse under one `Observe` verb with payload variants (Observe a State, Observe a Record, Observe Pending Questions).
- Three separate verbs: `ObserveState`, `Query`, `Watch`. (Verb-form-but-domain-specific.)
- One `Query` verb with payload variants.

Per the repeated-category-words rule (/237, sweep into `skills/naming.md`), three siblings with `*Observation` suffix → one `Observe` verb with three payload variants. But "QuestionPending" doesn't fit the `*Observation` pattern. The collapse needs care.

## 6 · Recommendations

In rough priority:

1. **Design the observer hook mechanism (hole 4).** This unblocks Phase 3 component refactors. Recommend one of: built-in macro injection (cheapest for contract authors), or a `signal-observe` contract (cleanest separation). Either deserves a designer report.
2. **Design the Sema-lowering executor pattern / library (hole 5).** Recommend a `sema-executor` crate or library module documenting: typed `Lowering` trait, atomicity guarantees, error-model contract, retry semantics. Without this, the per-component refactors will produce inconsistent executor patterns.
3. **Extend `skills/naming.md` to cover replies + events (hole 2).** Document the past-tense-outcome convention. Drop the implicit 1:1 op↔reply mapping question; pick a convention.
4. **Document the verb-pair convention (hole 7).** Pick the canonical pair (Watch/Unwatch) and name alternatives only when the canonical is awkward.
5. **Spell out the compound-action escape (hole 3).** Pick a stance: prefer split where it works; use agglutinated compound where it doesn't.
6. **Add the `*Order` / `*Request` / `*Command` suffix rule to owner-contract guidance (hole 10).** Small addition to `skills/contract-repo.md`.
7. **Document the multi-op atomicity contract (hole 9).** Likely: atomicity required at the daemon level; the daemon executor's responsibility; if a daemon needs partial-commit semantics, it splits the work across multiple Requests.
8. **Document the per-op reply mapping (hole 8).** Likely: each op produces exactly one SubReply variant from the channel's reply enum; convention is positional.
9. **Spirit-specific: settle the State collision (hole 1).** My lean: rename the psyche's "state of presence" to `Presence`; psyche's "to state intent" stays as the verb `State`.
10. **Spirit-specific: settle Statement/Entry as two verbs or one (open question §5).** My lean: two verbs (`State`, `Record`) — the public actions are distinct even if they converge in storage.

## 7 · References

- `/241 reports/designer/241-signal-architecture-migration-guide.md` — the spec being tested.
- `reports/operator/138-signal-frame-macro-migration-work.md` — the macro shape this assumes.
- `reports/designer/240-signal-frame-operation-collapse-check-removal.md` — the kernel cleanup.
- `reports/designer/236-persona-spirit-audit-and-intent-manifestation-2026-05-19.md` — prior spirit audit; some of the conventions there now contradict the new direction.
- `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs` — current contract on `main`.
- `/git/github.com/LiGoldragon/owner-signal-persona-spirit/src/lib.rs` — current owner contract.
- `intent/component-shape.nota` 2026-05-19T19:30Z onward — the psyche statements driving the migration.
- `intent/naming.nota` — the verb-form rule.
- `skills/contract-repo.md` — current contract discipline.
- `skills/naming.md` — current naming discipline.
