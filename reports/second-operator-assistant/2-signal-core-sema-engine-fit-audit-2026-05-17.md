# signal-core ↔ sema-engine fit — audit per brief 118

*Code-grounded audit answering "do `signal-core` and `sema-engine`
play well together today?" Verdict: **partial fit, right shape**.
The six wire verbs map onto verb-shaped engine methods one-for-one;
the kernel split is clean. Three real gaps require adapter code in
every component: write-`Validate` is not a first-class engine call;
cross-table atomic commits go through the kernel escape hatch; and
the contract-to-reducer dispatch boilerplate repeats per daemon.
Recommendation: keep sema-engine's shape; add three thin helper
APIs; emit one boilerplate-eliminating macro extension.*

Date: 2026-05-17

Author: second-operator-assistant

---

## §0 — TL;DR

Per brief 118 §6, this report names:

1. **Verdict** — good fit. No engine API additions required for
   current consumers. The kernel/daemon split holds.
2. **Verb → engine API table** — §1. All six verbs are
   verb-shaped methods on `Engine`; structural atomicity rides on
   `CommitRequest`.
3. **Boilerplate list** — §3. The original audit listed three
   patterns; falsification dissolved one (write-validation),
   reframed one (stringly seams are component-side), and the
   third (per-daemon match-on-variant dispatch) reads as normal
   Rust pattern matching rather than painful boilerplate.
4. **Recommendation** — §4. Keep sema-engine as is. The three
   helper APIs the first pass proposed (`validate_write`,
   `commit_multi`, `unsubscribe`) either dissolve through
   composition or have known-cleaner alternatives. Component-side
   composition of `Engine::match_records` covers write
   pre-validation; component supervisors manage subscription
   lifetime; cross-table atomicity is usually a schema-design
   question, not a kernel API question.
5. **Witness-test plan** — §5. Six wire→engine seam witnesses
   landed at `tests/signal_core_seam.rs`; six gap-falsification
   witnesses landed at `tests/seam_gap_falsification.rs`; the
   brief's open witnesses are either already exercised by the
   existing sema-engine suite or wait on the first owner-signal
   contract crate to land.

```mermaid
flowchart LR
    request[signal-core Request&lt;Payload&gt;]
    decode[component dispatch<br/>match on variant]
    reducer[domain reducer<br/>per-component]
    engine[sema-engine Engine]
    db[component.redb]
    reply[signal-core Reply]

    request --> decode
    decode -- "verb-shaped call" --> reducer
    reducer -- "Engine::assert / mutate / retract<br/>match_records / validate / subscribe / commit" --> engine
    engine --> db
    engine -- typed receipt --> reducer
    reducer -- typed reply payload --> reply
```

The arrows that work cleanly today: every `signal-core` verb has a
verb-shaped engine method; the engine's commit log carries each
operation's verb; subscriptions emit typed deltas; receipts name
the verb that produced them.

The arrows that need adapter code today: the **match on variant**
edge (boilerplate per daemon), the **typed receipt → reply
payload** edge (each daemon shapes its own typed reply), and the
**reducer-side validate** path (sema-engine cannot dry-run a write
through component reducer logic).

---

## §1 — Verb → sema-engine API table

Concrete mapping at `/git/github.com/LiGoldragon/sema-engine/src/engine.rs`.

| `SignalVerb` | sema-engine call | Receipt | Touches commit log | Emits subscription delta |
|---|---|---|---|---|
| `Assert` | `Engine::assert(Assertion<RecordValue>)` (engine.rs:67) | `MutationReceipt` (verb=Assert) | yes — `CommitLogOperation::new(SignalVerb::Assert, …)` | yes (`DeltaKind::Assert`) |
| `Mutate` | `Engine::mutate(Mutation<RecordValue>)` (engine.rs:130) | `MutationReceipt` (verb=Mutate) | yes | yes (`DeltaKind::Mutate`) |
| `Retract` | `Engine::retract(Retraction<RecordValue>)` (engine.rs:193) | `MutationReceipt` (verb=Retract) | yes | yes (`DeltaKind::Retract`) |
| `Match` | `Engine::match_records(QueryPlan<RecordValue>)` (engine.rs:404) | `QuerySnapshot` (verb=Match) | no | no |
| `Subscribe` | `Engine::subscribe(QueryPlan, Arc<dyn SubscriptionSink>)` (engine.rs:514) | `SubscriptionReceipt` carrying `InitialSnapshot` | no (subscription registration persists separately) | yes (initial + post-commit deltas) |
| `Validate` | `Engine::validate(QueryPlan<RecordValue>)` (engine.rs:466) | `ValidationReceipt` (verb=Validate) | no | no |
| *(structural atomicity)* | `Engine::commit(CommitRequest<RecordValue>)` (engine.rs:259) | `CommitReceipt` carrying `operation_count` | yes — one `CommitLogEntry` with `NonEmpty<CommitLogOperation>` | yes — one delta per `CommittedEffect` |

The engine internally stamps the verb on every commit-log entry and
mutation receipt (engine.rs:99, 162, 222, 300, 323, 343). The
six-root spine round-trips end-to-end: the wire-level
`Operation<Payload>::verb` is carried into the engine; the engine
writes the verb into the durable log; the receipt carries the verb
back; the subscription delta's `DeltaKind` converts to
`SignalVerb` via `DeltaKind::verb` (subscribe.rs:218).

---

## §2 — Answers to the brief's seven questions

### Q1. Does `signal_channel!` emit enough metadata for sema-engine?

**Partial.** The macro emits:

- per-variant `signal_verb()` (the `RequestPayload` trait
  implementation; signal-core round-trip tests assert
  `operation.verb == request.signal_verb()`);
- the typed request / reply / event enums and their NOTA codecs;
- `Frame` aliases (`MindFrame` etc.) plus typed frame bodies;
- stream relation witnesses (`opened_stream()`, `closed_stream()`,
  `stream_kind()`) when streams are declared.

What it does **not** emit:

- a per-variant dispatcher trait the daemon can implement (so each
  daemon writes its own match-on-variant — see §3.A);
- a metadata reflection API (e.g. "give me all variants tagged
  `Mutate`, or all variants that open a specific stream") that
  would let consumers route by capability without enumerating
  variants by hand;
- the ordinary-vs-owner contract distinction — a contract crate is
  either ordinary or owner by repo identity, not by per-variant
  flag. (This is correct per the triad's "permission as shape, not
  as runtime gate" stance — the wrong contract simply cannot
  express the wrong frames.)

The missing dispatcher trait is the main usability gap. The
metadata is there at runtime; consumers just rewrite the
boilerplate that mechanically maps it onto handler methods.

### Q2. Does sema-engine expose verb-shaped operations?

**Yes.** Six methods, one per `SignalVerb` root, plus
`Engine::commit` for structural multi-op atomicity. See §1.

The engine names them with workspace-shaped nouns (`Assertion`,
`Mutation`, `Retraction`, `QueryPlan`, `CommitRequest`) — full
English words; no `Op` or `Req` abbreviation. The wrapper types
(`Assertion`, etc.) bind a `TableReference<RecordValue>` to a
record, which keeps the type system carrying the table identity.

### Q3. Where does `Validate` live?

**Read-side only.** `Engine::validate` (engine.rs:466) is
implemented as `match_records` plus receipt wrapping — it dry-runs
a query without mutating storage. It does **not** dry-run a write
through reducer logic.

What `Validate` cannot do today:

- check that a candidate `Assert` would not collide with an
  existing key (the `DuplicateAssertKey` check fires only inside
  `Engine::assert` / `Engine::commit`, after the engine has
  decided to write);
- check that a candidate `Mutate` would find an existing record
  (the `RecordNotFound` check is the same shape);
- run component-supplied precondition checks (the engine knows
  nothing about component-level invariants — those run in the
  reducer);
- validate a multi-operation `CommitRequest` end-to-end.

Concrete consequence: a `Validate (Mutate record)` request that
the wire kernel accepts has no engine-side execution path. The
daemon would have to write a parallel "dry-run" implementation of
each reducer to satisfy the contract's `Validate` verb on writes.
That parallel implementation is the highest drift risk in the
brief's gap list.

This is the most consequential gap. §4 names a thin helper API
that closes it without reshaping the engine.

### Q4. Where do subscriptions come from?

**Engine-native, with two real gaps.**

What works (engine.rs:514, subscribe.rs):

- initial state delivered as `SubscriptionEvent::InitialSnapshot`
  carrying a `QuerySnapshot`;
- post-commit deltas delivered as
  `SubscriptionEvent::Delta<RecordValue>` carrying
  `DeltaKind::{Assert, Mutate, Retract}`;
- typed `SubscriptionHandle` carrying id + table + snapshot;
- per-query filter (`QueryFilter::accepts(key)`) so a subscription
  ignores deltas on other rows;
- detached or inline delivery mode (`SubscriptionDeliveryMode`);
- durable registration persisted to a known engine slot
  (`SUBSCRIPTIONS` table, engine.rs:625) so registrations survive
  process restart.

Real gaps:

- **No `Engine::unsubscribe(SubscriptionHandle)`.** The wire-side
  `Subscribe` opens a stream; the wire-side
  `Retract SubscriptionRetraction` closes it (per persona-mind's
  signal-channel grammar). The engine has no symmetric close
  method. Each consumer manages this externally (e.g.
  persona-mind's `SubscriptionSupervisor` decides when to stop
  delivering); the engine's `SubscriptionRegistry` keeps growing
  for the daemon's lifetime.
- **No flow-control protocol.** `SubscriptionSink::deliver`
  returns `Result<(), SinkError>`; if the sink is slow, the engine
  spawns a detached thread per delta (subscribe.rs:415). There is
  no backpressure signal back to the engine; no demand-driven
  delivery; no bounded buffer per subscription.

The post-commit delivery itself is not polled. The engine calls
`SubscriptionRegistry::deliver_delta` synchronously inside the
write transaction's downstream (engine.rs:114, 177, 240, 387). The
push-not-pull discipline is satisfied at the engine layer; the
gaps are about closing streams cleanly and bounding memory.

### Q5. What is the transaction boundary?

**Per-table, structural atomicity.**

- A single-op `Assert` / `Mutate` / `Retract` commits in one redb
  write transaction, writing one `CommitLogEntry`.
- A multi-op `Engine::commit(CommitRequest)` commits in one redb
  write transaction, writing one `CommitLogEntry` whose
  `NonEmpty<CommitLogOperation>` carries every op's verb.
- The `CommitRequest` is **single-table** by shape: it takes one
  `TableReference<RecordValue>` and the per-op `WriteOperation`
  values share that record type. Multi-table atomic commits go
  through `Engine::storage_kernel()` and a hand-written
  `storage.write(|transaction| ...)` closure — the named escape
  hatch.
- Domain side effects (PTY spawn, network IO, subprocess
  invocation) are **not** in the transaction. Per sema-engine ARCH
  §"Constraints": *"Component domain validation happens before
  calling Engine. Component actors own ordering, supervision,
  sockets, and delivery."* — the daemon sequences side effects
  around the typed commit; the durable record names the *intent*,
  not the side-effect's success.

The single-table shape of `CommitRequest` is the second
consequential gap. Concrete: a `RoleClaim` Mutate that updates
both the `claims` table and appends to the `activities` table
needs cross-table atomicity. Today the consumer either does two
separate commits (atomicity lost) or escapes through
`storage_kernel()` (typed engine API bypassed). §4 names the
`Engine::commit_multi` helper that closes this.

### Q6. Are owner-signal operations first-class?

**Not yet, by design.** The engine is contract-blind — `assert`,
`mutate`, etc. don't carry caller identity; the table + verb +
record is the entire input. The contract / socket layer enforces
the boundary (per `skills/component-triad.md` invariant 5 and
`reports/designer-assistant/116` §13).

The clean shape this enables: ordinary and owner contracts call
the *same* engine methods on the *same* tables; the dispatch in
the daemon (one actor per contract surface) decides which contract
is allowed to issue which write. The engine doesn't grow a parallel
write API per permission class.

The gap is that no `owner-signal-*` crates exist yet to exercise
this shape. Once `owner-signal-persona-orchestrate` lands, the
witness `owner-signal-request-uses-same-reducer-through-owner-socket`
becomes implementable as a pure dispatch-routing test.

### Q7. Can errors stay typed from wire to state and back?

**Mostly. Two stringly seams.**

Typed all the way:

- engine errors (`sema_engine::Error`) are a structured enum:
  `TableNotRegistered { table }`, `RecordNotFound { table, key }`,
  `DuplicateAssertKey { table, key }`, `DuplicateWriteKey`,
  `EmptyCommit { table }`, `UnsupportedReadPlan { operator }`,
  `SubscriptionRegistryPoisoned`, `SubscriptionSink { message }`;
- `signal-core::Reply` is a typed sum (`Accepted { outcome,
  per_operation }` / `Rejected { reason }`) with per-op
  `SubReply::{Ok, Invalidated, Failed, Skipped}`;
- per-channel reply payloads (`MindReply::*`) are typed records.

Stringly seams:

- `SinkError { message: String }` (subscribe.rs:228) — when a
  subscription delivery fails, the engine loses the typed cause
  and carries a string back to the caller.
- Consumer actor-call boundaries — persona-mind's dispatch path
  (`persona-mind/src/actors/dispatch.rs:130-200`) maps every
  Kameo `SendError` into
  `crate::Error::ActorCall(error.to_string())`. The actor's typed
  reply error is preserved through `SendError::HandlerError`, but
  the *transport* error is flattened to a string. The dispatch
  layer then maps the actor-call error to
  `PersistenceRejection::reply(error)` which produces a typed
  `MindReply::Rejection` — so the wire reply is typed again, just
  with the inner cause as a string.

Both seams are component-side, not engine-side. The engine's
typed-error surface is honest.

---

## §3 — Boilerplate / adapter code repeated in components

Three patterns repeat across triad daemons.

### §3.A — Match-on-variant dispatch

Every daemon writes a `match request.payload() { Variant(_) => ... }`
to route a typed payload to the right handler. The match
re-enumerates information the macro already encodes (the variant
exists; its verb is declared).

Worked example: `persona-mind/src/actors/dispatch.rs:55-119` has
the full match across all `MindRequest` variants — 26 arms, each
delegating to a `self.<method>(envelope, trace)` call that itself
unpacks the typed payload. The same shape repeats in every other
component daemon that consumes `signal-core` frames.

What a macro extension could emit: a `MindDispatcher` trait with
one method per request variant
(`async fn handle_submit_thought(&self, payload: SubmitThought)
-> MindReply` etc.). The dispatch loop becomes
`request.dispatch(&self).await`. Consumers implement the trait;
the macro emits the routing.

### §3.B — Engine-call-to-reply shaping

After the engine returns a typed receipt (`MutationReceipt`,
`QuerySnapshot`, `SubscriptionReceipt`, `CommitReceipt`,
`ValidationReceipt`), the daemon must shape it into a
contract-typed reply payload. Today this happens in each
component's reply-shaper code; the mapping is mechanical (the
receipt carries the verb, table, key, snapshot; the reply carries
some subset of those plus domain-specific fields).

Worked example: `persona-mind/src/actors/store/graph.rs` returns
the kernel reply from a per-message handler; the
`PipelineReply::new(reply, trace)` wraps it; the `ReplyShaper`
actor maps it onto `MindReply::*`. Each component re-implements
this collapse.

This is unavoidable when the reply payload carries domain content
beyond the engine receipt — but for the basic shape (mutation
succeeded; here's the snapshot/key/verb), a contract-emitted
default could absorb the common case.

### §3.C — Write validation (retracted)

The first pass framed component-side write pre-validation as
"reducer-side boilerplate that mirrors engine integrity logic."
Falsification at
`sema-engine/tests/seam_gap_falsification.rs::validate_write_dissolves_into_match_records_dry_run`
shows the composition is three lines of `Engine::match_records`
plus a typed `Result` wrapper. The multi-op case
(`multi_op_write_dry_run_composes_with_match_records_plus_local_staging`)
adds a `HashSet` for within-batch duplicate detection and one
match probe per op — total ~12 lines for the whole batch
walker. The engine's typed errors (`DuplicateAssertKey`,
`DuplicateWriteKey`, `RecordNotFound`) map directly onto the
component-side equivalents; no parallel reducer logic, no
schema-check duplication.

Per the inelegance criterion, this is **not boilerplate** — it
is small typed composition that reads as English. Component
domain validation (the parts the engine doesn't know about, like
persona-mind's relation endpoint validator) remains the
component's responsibility, as the engine docs say.

---

## §4 — Recommendation

**Keep sema-engine as is.** The brief's bottom-line sentence holds
without engine changes:

> *"Signal Core is the wire grammar of operations; sema-engine is
> the durable execution substrate for those operations."*

The first pass of this audit proposed three helper APIs and one
macro extension. Falsification dissolved or deferred all four.

### §4.1 — `Engine::validate_write` (retracted)

**Status: dissolves into composition.** Witness:
`tests/seam_gap_falsification.rs::validate_write_dissolves_into_match_records_dry_run`
and `multi_op_write_dry_run_composes_with_match_records_plus_local_staging`.

A component can dry-run any write by composing
`Engine::match_records(QueryPlan::key(...))` against the proposed
records — three lines for the single-op case, ~12 lines for the
multi-op-with-within-batch-detection case. The engine's typed
errors map onto local enum variants one-for-one. No engine API
extension required.

What the engine doesn't know — domain preconditions like
persona-mind's relation endpoint validator — remains in the
component, as the engine docs say.

### §4.2 — `Engine::commit_multi` (deferred)

**Status: real but unpressed; schema redesign usually cleaner.**
Witness:
`tests/seam_gap_falsification.rs::cross_table_writes_via_two_engine_commits_are_not_engine_atomic`.

The witness confirms that two separate `Engine::assert` calls land
as two `CommitLogEntry` values at two snapshot IDs — not atomic.
The escape hatch is `engine.storage_kernel().write(|txn| { ... })`,
which is genuinely inelegant: it bypasses commit-log emission,
snapshot-ID bump, and subscription delta delivery. A multi-table
write through `storage_kernel` is architecturally invisible to the
engine's verb-tracking machinery.

No consumer pushes for cross-table atomicity today. The workspace
pattern (one component per concern, single-writer-actor per
engine, one engine per component) localises writes per table. When
one logical operation appears to span tables — e.g. a
`RoleHandoff` that retracts a claim from role A and asserts it for
role B — the cleaner answer is usually schema redesign (express
the operation as `Mutate` on one table) rather than growing the
engine API.

Resolution paths, in order of preference when the gap surfaces:

1. **Schema first.** Can the operation live in one table? If yes,
   atomicity is structural in the existing API.
2. **Extend `Engine::commit`.** When the schema genuinely
   requires multiple tables, grow the typed surface to accept a
   multi-table commit request preserving commit-log + snapshot +
   delta delivery semantics.
3. **Document the constraint.** Consumers that hit it surface a
   contract-design issue rather than reaching for
   `storage_kernel`.

Defer the engine extension until a consumer surfaces that
genuinely resists schema redesign.

### §4.3 — `Engine::unsubscribe` (soft; deferred)

**Status: component-side route-around covers correctness.**
Witness:
`tests/seam_gap_falsification.rs::subscription_lifetime_can_be_managed_externally_via_handle_id_filter`.

A component supervisor tracks active subscription IDs externally;
the sink filters delivered events by handle id. Spurious deltas
do not reach domain code. The engine's registry grows monotonically
until daemon shutdown — bounded by daemon lifetime, fine for
steady-state subscription sets, wasteful for churn workloads.

The more load-bearing performance concern is **detached
thread-per-delta** in `SubscriptionDeliveryMode::Detached`
(`sema-engine/src/subscribe.rs:415`): each accepted delta in
detached mode spawns one OS thread. The actor-shaped answer
today is `SubscriptionDeliveryMode::Inline` — the supervisor sink
uses inline delivery, accepts inside its own actor mailbox, and
avoids the per-delta thread cost. A future demand-driven delivery
mode would tighten this further but is not load-bearing yet.

### §4.4 — Dispatcher-trait macro extension (reconsidered)

**Status: normal Rust pattern matching, not painful boilerplate.**

The match-on-variant dispatch at
`persona-mind/src/actors/dispatch.rs:55-119` reads as ordinary
Rust. Each arm carries meaning (which handler to call, which
flow to route to, which trace nodes to record). A macro-emitted
dispatcher trait would replace the explicit match with a typed
method-per-variant trait — saving keystrokes but not adding
clarity. The Rust compiler already catches missed variants on
the `MindRequest` enum.

If a future contract has many more variants and the dispatch
shape is genuinely uniform, the macro extension becomes worth
the cost. Today it isn't.

### §4.5 — What stays as named gaps

The two component-side stringly seams from §2 Q7 stand:

- `SinkError { message: String }` loses the typed cause of sink
  delivery failures.
- Persona-mind's actor-call boundary
  (`crate::Error::ActorCall(error.to_string())`) flattens
  Kameo's typed `SendError` into a string.

Both are component-side fixes, not engine-shape issues. They
follow `skills/rust/errors.md` discipline when addressed.

### §4.6 — What not to add

- **Do not move domain validation into the engine.** Per-component
  preconditions are domain logic; they don't belong in the kernel.
- **Do not move actor topology, sockets, or authorization into the
  engine.** That defeats the kernel-vs-daemon split.
- **Do not invent a parallel API per permission class.** Owner and
  ordinary contracts call the same engine methods; the contract +
  socket boundary is where the distinction lives.

---

## §5 — Witness-test plan

The brief §5 names seven witnesses. Status now:

| Witness | Status |
|---|---|
| `signal-core-request-executes-through-sema-engine-assert` | **landed** at `sema-engine/tests/signal_core_seam.rs::signal_core_assert_operation_lands_as_engine_assert_with_matching_verb`. Persona-mind has a domain-level analogue at `typed_thought_append_uses_sema_engine_operation_log`. |
| `signal-core-request-executes-through-sema-engine-mutate` | **landed** at `tests/signal_core_seam.rs::signal_core_mutate_operation_lands_as_engine_mutate_with_matching_verb`. |
| `signal-core-validate-does-not-commit` | **dissolved** — `Engine::validate(QueryPlan)` already passes the existing engine-suite test `validate_dry_run_returns_validate_receipt_without_commit_log_write`; component-side write dry-run via `match_records` is witnessed at `tests/seam_gap_falsification.rs::validate_write_dissolves_into_match_records_dry_run`. No write-shaped `Validate` API is required. |
| `signal-core-subscribe-receives-initial-state-then-delta` | **landed** at the engine layer via `subscribe_initial_snapshot_uses_latest_committed_snapshot` + `subscribe_delta_fires_after_commit_is_visible`; persona-mind has the domain analogue. The supervisor pattern is witnessed at `tests/seam_gap_falsification.rs::subscription_lifetime_can_be_managed_externally_via_handle_id_filter`. |
| `owner-signal-request-uses-same-reducer-through-owner-socket` | **not yet** — waits on the first owner-signal contract crate. The engine being contract-blind is the structural enabler; nothing engine-side blocks this. |
| `wrong-contract-frame-does-not-reach-reducer` | **not yet** — same blocker; needs a daemon binding both ordinary and owner sockets to demonstrate. |
| `multi-operation-request-has-clear-commit-semantics` | **landed** at `tests/signal_core_seam.rs::signal_core_multi_op_request_lands_as_one_commit_log_entry_with_ordered_per_op_verbs`. The cross-table escape-hatch shape is also witnessed at `tests/seam_gap_falsification.rs::cross_table_writes_via_two_engine_commits_are_not_engine_atomic` so the constraint is documented in code, not just prose. |

Per the brief's §6 ask for a minimal implementation plan for
missing witnesses: the two owner-signal witnesses are blocked on
upstream contract work (`primary-699g` /
`owner-signal-persona-orchestrate`). Nothing in sema-engine blocks
them. When the first owner-signal contract crate lands, the
witnesses become small daemon-side dispatch tests.

The first pass of this audit's "minimal implementation order" for
helper APIs is **retracted**; no helpers are needed given the
falsification results.

---

## §6 — What's outside this audit

- **Backpressure / demand-driven delivery.** Real concern; not a
  fit problem between the crates. Defer to a separate design
  pass when a consumer saturates a sink. The detached
  thread-per-delta path is the most-load-bearing flavour of this
  concern today; `SubscriptionDeliveryMode::Inline` is the
  actor-shaped workaround.
- **Stringly seams** (Q7) — the engine's `SinkError` carries a
  `String`; persona-mind's actor-call errors carry a `String`.
  Operator-side fixes inside each component; not a kernel-shape
  issue.
- **Cross-domain federation / schema versioning** — out of scope
  for the today-stack audit.
- **Owner contract surfaces** — designed in DA/116; once first
  owner contract lands, the two owner-shaped witnesses above
  become implementable. The engine being contract-blind is the
  structural enabler.

---

## See also

- `~/primary/skills/component-triad.md` — the five invariants this
  audit is grounded in (especially invariant 4: daemon state goes
  through sema-engine).
- `~/primary/skills/architectural-truth-tests.md` — the witness
  shape every gap-closing helper should ship with.
- `~/primary/orchestrate/ARCHITECTURE.md` — the orchestrate
  surface that consumes sema-engine as its eventual state backend.
- `/git/github.com/LiGoldragon/sema-engine/ARCHITECTURE.md` — the
  engine's own ARCH; this audit cross-checks against it.
- `/git/github.com/LiGoldragon/sema-engine/src/engine.rs` — the
  six verb-shaped methods and structural commit; primary surface
  this audit reads against.
- `/git/github.com/LiGoldragon/sema-engine/src/subscribe.rs` — the
  subscription sink + delivery mode; Q4's gaps live here.
- `/git/github.com/LiGoldragon/sema-engine/src/mutation.rs` —
  `CommitRequest` / `WriteOperation` shape; Q5's single-table
  constraint is here.
- `/git/github.com/LiGoldragon/signal-core/ARCHITECTURE.md` — the
  wire kernel; verb-direction framing.
- `/git/github.com/LiGoldragon/signal-core/src/lib.rs` — the
  public re-exports and the `signal_channel!` macro entry point.
- `/git/github.com/LiGoldragon/signal-persona-mind/src/lib.rs:1746` —
  the `signal_channel!` invocation that shapes the existing
  consumer surface.
- `/git/github.com/LiGoldragon/persona-mind/src/actors/dispatch.rs:55` —
  the canonical match-on-variant boilerplate (§3.A).
- `/git/github.com/LiGoldragon/persona-mind/src/actors/store/graph.rs` —
  one real consumer's reducer path; the receipt → reply shaping
  (§3.B) is in adjacent files.
- `~/primary/reports/designer-assistant/118-signal-core-sema-engine-fit-investigation-brief-2026-05-17.md` —
  the brief this audit answers.
- `/git/github.com/LiGoldragon/sema-engine/tests/signal_core_seam.rs` —
  six wire→engine seam witnesses landed for this audit.
- `/git/github.com/LiGoldragon/sema-engine/tests/seam_gap_falsification.rs` —
  six falsification witnesses that dissolved, reframed, or
  confirmed the gaps this audit's first pass named.
