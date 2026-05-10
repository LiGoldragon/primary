# 105 — Actor discipline project-wide sweep

*Designer report. Project-wide audit of actor-related skills, reports,
code (across persona-* runtime crates), and test bed repos. Four
parallel survey agents (skills, reports, code, tests); synthesis here.
Best patterns to showcase, worst patterns to retire, open questions
where I can't quite resolve but feel something is off.*

---

## 0 · TL;DR

Four parallel agents surveyed the workspace's actor surface. The
discipline is sound and the Kameo wave landed cleanly — but the
audit surfaced concrete gaps:

- **persona-mind's actor topology is half-real** — the `ActorKind`
  enum names 44 planes, but only 9 have `impl Actor` types. The
  other ~35 are pure trace markers. The "actors all the way down"
  rule produced names without bodies.
- **5 data-type-shadowed actors** — `StoreSupervisorActor` wraps
  `MemoryState`, `Ledger` wraps `MessageStore`, `NiriFocus` wraps
  `FocusTracker`, `TerminalDeliveryActor` wraps `WezTermMux`,
  `ConfigActor` wraps `StoreLocation`. Each adds counters + mailbox
  + trace recording over a data type that already has the methods.
  The user's exact pattern: "actor that doesn't seem to fit
  somewhere; data type needs to refine; or the data type just
  becomes the actor."
- **4 forwarding-trampoline actors in persona-mind** — Ingress,
  Dispatch, Domain, View. No domain state; only ActorRef fields.
  Exist to record trace events and forward to the next stage.
- **`TerminalDeliveryActor` is never spawned in production** —
  `persona-router` calls `mux.pane(pane_id).deliver(&prompt)`
  synchronously at `harness_delivery.rs:55`, going around the actor
  to call the data type directly. This is the single strongest
  signal that the actor framing is overhead in many cases.
- **My own `kameo-testing` repo has bugs** — `Recorder { trace:
  Arc<Mutex<Vec<Trace>>> }` is exactly the gratuitous-shared-lock
  pattern `actor-systems.md` warns against; 12 sites use
  `std::convert::Infallible` instead of `kameo::error::Infallible`;
  5+ tests use magic-delay sleeps where push witnesses (oneshot/
  watch channels — DA's pattern) would be deterministic.
- **`ClaimNormalize` vs `ClaimNormalizer`** — the workspace's
  flagship example uses both names interchangeably across skills.
  `kameo.md` line 69 says `ClaimNormalize`; line 126 says
  `ClaimNormalizer` is the "Right" form. Verb-shaped residue from
  the ractor `*State` era.
- **Designer/100's 5 implementation pins are 0/5 implemented** after
  the Kameo wave — DisplayId mint algorithm, sema table key shapes,
  caller-identity 3-layer resolution, mind.redb path, subscription
  contract sketch. The Kameo migration covered topology but not
  these pins. They sit in operator/operator-assistant's lane;
  unclear who picks them up.
- **Naming sweep is mostly DONE** — operator and operator-assistant
  swept persona-mind/message/system/harness/sema/signal-persona-mind
  to 0 `*Actor` / `*Message` / `*Handle` hits. Only persona-router
  and persona-wezterm have residual hits (operator's in-flight tail).
- **A new rule landed mid-sweep**: someone added §"Runtime roots
  are actors" to `skills/actor-systems.md` (commit 284da3a) — it
  says non-actor wrappers around multiple `ActorRef<_>` values
  recreate the wrapper-everywhere shape this discipline retires.
  This complements my v3 single-actor wrapper rule and directly
  retires `MindRuntime` (3 ActorRefs in a struct) and
  `RouterRuntime` (3 sibling ActorRefs).

---

## 1 · What the sweep covered

Four parallel survey agents:

| Agent | Scope | Output |
|---|---|---|
| A — skills audit | 8 actor-related skills + ESSENCE | 8 inconsistencies, 10 best examples, 9 worst, 9 gaps, 5 unclear rules, stale refs catalog, 7 cross-skill discoveries |
| B — reports audit | 14 actor-related reports across all roles | 10 settled decisions, 14 open, 11 contradictions, 17 unfolded recommendations, 4 stale-but-keepable reports, 12 cross-report dependencies, 12 corpus-level patterns |
| C — code audit pass 1 | 7 persona-* runtime repos | 14 real `impl Actor` types inventoried; 5 data-type-shadowed actors; 4 forwarding trampolines; 3 different public-surface conventions; 1 actor never spawned in production |
| D — test repos comparison | `kameo-testing` (designer) + `kameo-testing-assistant` (DA) | 27+15 tests catalogued; per-repo best patterns; 5 worst patterns identified incl. 2 bugs in my own repo |

Total roughly 35-40 distinct findings. Synthesis below organizes them
into best patterns (showcase), worst patterns (retire/fix), gaps,
contradictions, and open questions.

---

## 2 · Best patterns — showcase

These are the patterns the skill set should hold up as exemplars.
Each cites file:line so the canonical example is identifiable.

### 2.1 Push-driven test witnesses (DA's mainstay)

`/git/github.com/LiGoldragon/kameo-testing-assistant/tests/failure_and_mailbox.rs:94`
`bounded_mailbox_applies_backpressure_to_senders` uses `tokio::sync::oneshot`
and `tokio::sync::watch` channels as push witnesses for transient state
(handler started, generation incremented, link death observed). No
polling, no magic sleeps, no flake risk.

```rust
let (started_sender, started_receiver) = oneshot::channel();
let (release_sender, release_receiver) = oneshot::channel();
gate_for_hold.tell(HoldUntilReleased::new(started_sender, release_receiver)).await;
started_receiver.await?;        // deterministic: handler is running NOW
gate.tell(MarkProcessed::labeled("queued")).await?;
```

The `tokio::time::timeout(30ms, ...).await.is_err()` form proves a
should-be-infinite wait — that's a bounded should-not-fire timeout,
not a magic delay.

`failure_and_mailbox.rs:258` `transient_supervision_restarts_after_unhandled_tell_error`
uses `watch::channel` for restart-generation observation:

```rust
let (start_sender, mut start_receiver) = watch::channel(0);
async fn on_start(mut state, _) -> ... {
    let start_count = state.starts.fetch_add(1, Ordering::SeqCst) + 1;
    let _ = state.start_sender.send(start_count);
    Ok(state)
}
start_receiver.changed().await?;        // exact, no deadline arithmetic
```

**Skill action**: my `kameo.md` should add a §"Test patterns" with
oneshot/watch witnesses as the canonical test-discipline for
asserting on transient actor states, citing this test.

### 2.2 Match-on-structured-stop-reason

`failure_and_mailbox.rs:483` asserts the **exact** structured stop
reason rather than a counter:

```rust
let right_reason = right.wait_for_shutdown_result().await?;
assert!(matches!(
    right_reason,
    ActorStopReason::LinkDied { reason, .. } if matches!(*reason, ActorStopReason::Killed)
));
```

Compare to my `tests/links.rs:66` `linked_peer_death_fires_on_link_died_in_survivor`
which asserts `>= 1` on a counter — proves the hook fired but doesn't
prove *why*. The DA pattern is sharper.

### 2.3 Falsifiable test names (designer's mainstay)

Every test in `kameo-testing/tests/` reads as a complete claim:

- `args_self_passes_actor_directly_into_on_start`
- `bounded_full_try_send_returns_mailbox_full`
- `register_collision_returns_name_already_registered`
- `attach_stream_empty_still_emits_started_and_finished`
- `restart_policy_never_does_not_restart_on_panic`

The pattern is `<subject>_<action>_<outcome>`. If the test passes, the
sentence is true. This is the model.

### 2.4 Local-to-test actor types (designer's pattern)

`kameo-testing/tests/lifecycle.rs` defines its actor types **inside the
test fn**:

```rust
#[tokio::test]
async fn args_self_passes_actor_directly_into_on_start() {
    struct Counter { count: i64 }
    impl Actor for Counter { ... }
    struct Read;
    impl Message<Read> for Counter { ... }
    let actor_ref = Counter::spawn(Counter { count: 7 });
    ...
}
```

Each test is a copy-pastable demo. For a teaching repo this is the
right shape — the entire actor lives where you read it. Compare to
DA's module-scope actors which require scrolling between fixture and
test.

### 2.5 Bare role-noun naming (persona-router/message/system/harness)

The non-mind persona crates land bare role-noun actors:

- `persona-router`: `RouterRoot`, `HarnessRegistry`, `HarnessDelivery`
- `persona-message`: `DaemonRoot`, `Ledger`
- `persona-system`: `NiriFocus`
- `persona-harness`: `Harness`

Each names what the type IS or what role it plays. The `*Actor`
suffix appears nowhere outside persona-mind (and `TerminalDeliveryActor`
in wezterm — operator's in-flight cleanup tail).

### 2.6 Cross-role iteration chain — operator/95 → designer/98 → operator/99

Per Agent B §7.7: this is a model for cross-role work. Each report
names its predecessor + its action items. The 4 unresolved follow-ups
in operator/99 form a known debt list, not lost work. The pattern that
made it work: each report explicitly says what's done and what's
deferred.

### 2.7 The `tell`-of-fallible-handler-trap citation chain (one canonical home + cites)

Per Agent A §7.4: the cleanest cross-skill chain in the workspace.
Substance lives in `kameo.md` §"The `tell`-of-fallible-handler trap";
`actor-systems.md` and `rust-discipline.md` cite back. No duplication.
This is the model for the actor-density and ZST-anti-pattern rules
which currently sprawl across 7 and 6 phrasings respectively.

### 2.8 Domain-named wrapper with domain methods (when it earns its place)

The refined v3 rule in `kameo.md` §"Public consumer surface" — a
wrapper earns its place when it composes multiple `ActorRef`s, exposes
domain verbs, owns lifecycle, narrows capabilities, prevents unsafe
sends, maps errors, hides topology, or supports library publication.
DA/6's specific arguments. Now codified.

The shape is `Mind::claim(role, scope, reason)` instead of
`mind_ref.ask(MindRequest::Claim { role, scope, reason })`. Caller
writes domain English; wrapper constructs the typed Message.

### 2.9 Restart-reconstructs-state test (DA's load-bearing supervision claim)

`failure_and_mailbox.rs:424` `supervised_restart_reconstructs_from_args_not_mutated_state`
proves the workspace's load-bearing supervision rule with a 10→12→crash→10
sequence. The `kameo.md` §"Supervision" prose ("a counter the crashed
instance had bumped to 12 reads back as 0") is backed by this exact
test. Should be cited from the skill.

### 2.10 PreparedActor::run for state assertions

`/git/github.com/LiGoldragon/kameo-testing-assistant/tests/data_bearing_patterns.rs:195`
demonstrates the pre-enqueue + run pattern that gives back the actor's
final state:

```rust
let prepared_actor = MemoryLedgerActor::prepare();
let actor_reference = prepared_actor.actor_ref().clone();
actor_reference.tell(OpenItem::titled("queued before run")).await?;
actor_reference.tell(AddNote::with_body("also queued")).await?;
let stop_task = tokio::spawn(async move { actor_reference.ask(StopAndReadLedger).await });
let (final_actor, stop_reason) = prepared_actor
    .run(MemoryLedgerActor::named("prepared-ledger"))
    .await?;
assert!(matches!(stop_reason, ActorStopReason::Normal));
assert_eq!(final_actor.snapshot(), stop_snapshot);
```

`kameo.md` §"Spawning" mentions `prepare/run` mechanically but doesn't
showcase this. Add as the canonical test pattern for "I need the
actor's final state."

---

## 3 · Worst patterns — retire or fix

### 3.1 The aspirational `ActorKind` enum in persona-mind

`persona-mind/src/actors/trace.rs:1` declares 44 `ActorKind` variants.
**Only 9 have `impl Actor` types.** The other ~35 are pure trace
markers (`SemaWriterActor`, `IdMintActor`, `ClockActor`,
`EventAppendActor`, `CommitActor`, `ReadyWorkViewActor`,
`GraphTraversalActor`, etc.). `ActorManifest::persona_mind_phase_one()`
declares all 44 as actors with residency assignments.

This is the workspace's most concrete instance of the user's pattern
warning: *"actors that don't seem to fit somewhere — maybe one of our
data types needs to be refined and split, or there's simply just a
missing data type."* The 35 trace-only `ActorKind` variants either
need real `impl Actor` types **OR** the manifest needs to retract
them.

The runtime asserts ordering against fictional planes. Architecture
is half-real.

**Skill action**: `actor-systems.md` should add a rule: *"every
manifest-declared actor must have an `impl Actor`. Trace-only
markers are not actors."* `architectural-truth-tests.md` should add a
witness pattern: *"manifest entries match `impl Actor` set, no
fictional planes."*

### 3.2 Five data-type-shadowed actors

The user's exact pattern. For each: the actor exists but the wrapped
data type already has the methods. The actor adds counters + trace +
mailbox.

| Actor | Wrapped data | Evidence | Status |
|---|---|---|---|
| `StoreSupervisorActor` (`persona-mind/src/actors/store.rs:11`) | `MemoryState` (`memory.rs:17`) | both `apply_memory` and `read_memory` end in `self.memory.dispatch_envelope(envelope)` | **Could be `impl Actor for MemoryState`** |
| `Ledger` (`persona-message/src/actors/ledger.rs:9`) | `MessageStore` (`store.rs:50`) | `ledger.rs:26` calls `envelope.execute(&self.store)`; whole actor adds 1 counter | **Could be `impl Actor for MessageStore`** |
| `NiriFocus` (`persona-system/src/niri_focus.rs:9`) | `FocusTracker` (`niri.rs:289`) | `niri_focus.rs:72` calls `self.tracker.apply_event(&message.event)`; adds 2 counters | **Could be `impl Actor for FocusTracker`** |
| `TerminalDeliveryActor` (`persona-wezterm/src/terminal.rs:122`) | `WezTermMux::pane(...).deliver(...)` | **Never spawned in production**; consumers go around it | **Delete the actor; data type IS the API** |
| `ConfigActor` (`persona-mind/src/actors/config.rs:7`) | `StoreLocation` | only message is `#[allow(dead_code)]`; never invoked | **Delete the actor entirely** |

Operator's lane to act on. Designer surfaces the recommendation; the
collapse decisions belong to operator + operator-assistant who own
the persona-* runtime code.

### 3.3 Four forwarding-trampoline actors in persona-mind

`IngressSupervisorActor`, `DispatchSupervisorActor`,
`DomainSupervisorActor`, `ViewSupervisorActor` — all have only
`ActorRef` fields, no domain state. They exist to record trace events
and forward to the next stage. The "supervisor" naming is misleading —
they don't actually supervise anything; supervision is set up in
`MindRootActor::on_start`, not in these "supervisors."

`DispatchSupervisorActor` is the worst case: pure routing, `&self`
handler (not even `&mut`), six of eight `MindRequest` variants are
unsupported and fall to a stub `unsupported()`. Equivalent to a
function. The actor adds nothing the dispatch logic couldn't do as a
free function called from `IngressSupervisorActor` (which is itself a
trampoline).

**Skill action**: `actor-systems.md` already says *"Do not create
actors for pure value transformations that have no domain failure
and no independent runtime ownership."* Add a sharper version:
*"Do not create actors whose only state is one or more `ActorRef`
fields; those are forwarding helpers, not actors. Either give them
real state or collapse them into the parent."*

### 3.4 Cross-crate consumers go AROUND the actor (TerminalDeliveryActor)

The smoking gun. `persona-router/src/harness_delivery.rs:55` calls
`mux.pane(pane_id).deliver(&prompt)` synchronously, *bypassing the
unused* `TerminalDeliveryActor` and calling the `WezTermMux` data
type directly. This proves that for that case the actor wrapping was
unnecessary — the data type IS the API.

When the consumer chooses the data type over the actor, the actor
has lost its claim to existence.

### 3.5 Counter-only state pattern

9 actors have telemetry counter fields used only by tests:
`HarnessRegistry`, `HarnessDelivery`, `DaemonRoot`, `Ledger`,
`NiriFocus`, `Harness`, `TerminalDeliveryActor`,
`SubscriptionSupervisorActor`, `ReplySupervisorActor`. Several go
unread (`applied_event_count`, `delegated_delivery_count`,
`last_status_requester`).

These exist to give the architectural-truth tests something to assert
about ("the actor actually ran") without inspecting reply payloads.
Useful pattern, but the unread counters are pure overhead. **Skill
action**: when adding counters for testability, also add the test
that asserts on them — otherwise the field is dead code.

### 3.6 My own kameo-testing repo's bugs

Surfaced by Agent D against my own work:

- **`Recorder { trace: Arc<Mutex<Vec<Trace>>> }`** at `tests/streams.rs:20`
  is exactly the gratuitous-shared-lock pattern `actor-systems.md`
  warns against. The lock is dead weight — the trace is only
  accessed from inside the actor's handler. Should be
  `Recorder { trace: Vec<Trace> }` with a `ReadTrace` message
  returning a clone.
- **12 sites use `std::convert::Infallible`** instead of
  `kameo::error::Infallible`. The kameo-native one has serde
  derives that the std one doesn't (per `notes/findings.md`); this
  matters for actors whose state may be serialized.
- **5+ tests use magic-delay sleeps**: `tests/links.rs:78` sleep(100ms)
  for "give the link-death signal time to traverse";
  `tests/registry.rs:89` sleep(50ms) for "give the lifecycle driver a
  beat"; `tests/streams.rs:72,97` sleep(50ms) for "give the actor a
  moment to process Finished"; `tests/supervision.rs:152,156,160` for
  spacing crashes. All should be push witnesses (oneshot/watch) per §2.1.

T6 will fix these in my repo.

### 3.7 `ClaimNormalize` vs `ClaimNormalizer` — flagship-example self-contradiction

Per Agent A §1.1: the workspace's flagship example uses both names
interchangeably *within `kameo.md`*:

- `kameo.md:69` — core shape uses `ClaimNormalize`
- `kameo.md:126` — naming guidance "Right" example uses `ClaimNormalizer`
- `kameo.md:149` — table says `ClaimNormalize→ClaimNormalizer` (wrong→right)
- `kameo.md:198` — consumer-surface example reverts to `ClaimNormalizer`

`ClaimNormalize` is verb-shaped (the imperative "normalize this
claim") — residue of the ractor `*State` pattern with the suffix
dropped (`ClaimNormalizeState` → `ClaimNormalize`). Per the workspace's
own naming rule, the noun-shape is `ClaimNormalizer`.

Sweep: `kameo.md`, `actor-systems.md`, `rust-discipline.md` all need
the `ClaimNormalize` → `ClaimNormalizer` rename.

### 3.8 `abstractions.md:224-234` triple-anachronism

Per Agent A §1.3: the §"Actor frameworks" section references:
1. raw `ractor` (workspace runtime is now Kameo);
2. `*State` split (Kameo collapses Self and State);
3. "public handles" (retired by current Handle position).

Three obsolete claims in 11 lines. T6 will rewrite for Kameo.

### 3.9 `kameo.md:460` public ZST `Supervisor` example

Per Agent A §4.6, §5.3: the `kameo.md` supervision example shows
`struct Supervisor;` — a public ZST actor — while the same skill's
no-public-ZST-actor rule explicitly forbids them (line 629). Either
the example needs fields, or supervisors deserve a stated carve-out.
Currently the rule contradicts the example.

### 3.10 `kameo.md` Calculator example violates naming

Per Agent A §3.5, §7.7: `kameo.md:344-352` uses message types
`Inc`, `Mul`, `Read`. Per the same skill's naming guidance:
- `Inc` is the abbreviation `naming.md:35` retires (`Op→Operation`,
  `Inc` is the same shape).
- `Mul` similarly.
- `Read` shadows `std::io::Read`.

Right form: `Increment`, `Multiply`, `ReadCount`.

### 3.11 Multi-actor non-actor wrappers (now retired by the new rule)

Per Agent C §1.3, §1.15, §8.9: persona-mind has a *double wrapper*
(`MindRuntime` → `MindRootHandle` → `ActorRef<MindRootActor>`).
`RouterRuntime` holds 3 sibling ActorRefs and exposes convenience
methods. Both are now explicitly retired by the just-landed
`actor-systems.md` §"Runtime roots are actors" rule (commit 284da3a):
*"A struct that merely owns several `ActorRef<_>` values and exposes
convenience methods is a hidden non-actor owner."*

The runtime root should itself be an actor. `MindRootActor` already
is; the `MindRuntime` outer wrapper is the part to retire.
`RouterRuntime` should become an actor with `root`/`registry`/`delivery`
as its state.

### 3.12 Three different public-surface conventions in active use

Per Agent C §8.9:
1. **Double wrapper** (persona-mind: `MindRuntime` → `MindRootHandle` → `ActorRef`)
2. **Single runtime wrapper** (persona-router: `RouterRuntime` holding sibling refs)
3. **No wrapper, raw `ActorRef`** (persona-message, persona-system, persona-harness)

The new "runtime roots are actors" rule favors option 3 in concept.
The Mind/Cache/Ledger domain wrapper (per kameo.md §"Public consumer
surface") is the right shape when domain methods justify wrapping
*one* actor — but the multi-ref convenience-method shape of
`MindRuntime` and `RouterRuntime` is being retired.

### 3.13 designer/100's 5 implementation pins are 0/5 implemented

Per Agent B §7.3: after the Kameo wave landed, designer/100's pins
remain unimplemented. Spot-checks confirm:
- DisplayId mint algorithm (BLAKE3 + base32-crockford): `memory.rs:398-418`
  uses different algo (counter-based);
- Sema table key shapes: no `tables.rs`, no `persona-sema` dep;
- Caller-identity 3-layer resolution: hardcoded
  `ActorName::new("persona-mind")` per op-asst/97 P1;
- mind.redb path: Phase 2 not started;
- Subscription contract sketch: Phase 5 deferred.

Open question — see §5.

---

## 4 · Cross-skill consolidation needed

Per Agent A §7.1, §7.2: the actor-density rule has **7 phrasings**
across 4 skills, and the ZST anti-pattern has **6+ formulations**.
The `tell`-of-fallible-handler trap (§2.7 above) is the model for
cross-skill consolidation: one canonical home, cites elsewhere.

| Rule | Current phrasings | Where to consolidate |
|---|---|---|
| Actor-density (when to introduce an actor) | ESSENCE.md:176-184; actor-systems.md:42, 48-50; rust-discipline.md:556, 578; architectural-truth-tests.md:210; kameo.md:629 | Canonical: `actor-systems.md:48-50` (the three-condition triplet). Others cite. |
| ZST anti-pattern | rust-discipline.md:84-124, 127-146, 827; actor-systems.md:208, 242-243, 300; kameo.md:113-114, 629-633; architectural-truth-tests.md:212, 271 | Canonical: `rust-discipline.md:84-124` (the general rule) + `actor-systems.md` §"Rust shape" (the actor-specific elaboration). Others cite. |

Net duplication: ~70 lines collapsible to ~25 + cross-references.

---

## 5 · Open questions

The user explicitly asked: *"if there's something that you don't seem
quite to figure out but you feel is wrong, bring it up as questions."*

### 5.1 Who picks up designer/100's 5 implementation pins?

Designer surfaced them; operator's lane to implement. The Kameo wave
covered topology but not pins. Operator-assistant landed 6 crates of
migration without folding them. Are they orphaned? Should designer
file P0 beads to force the work into someone's lane, or wait?

### 5.2 Are the 4 forwarding-trampoline actors in persona-mind justified?

Ingress, Dispatch, Domain, View. They have no domain state, only
ActorRef fields. They record trace events on the way through. If the
trace recording IS the domain (witnessing the pipeline ran), the
actor framing is justified. If the trace is observability noise, the
actors should collapse and the pipeline should go straight from
RequestSession → memory dispatch.

The user's framing supports collapse: *"don't create actors where
there's already a data type."* But there's no data type these wrap —
they wrap nothing, they ARE just the trace plane. So either: (a)
make the trace plane a data type (`PipelinePhase` enum?), or (b)
accept that some actors are pure-routing and document the carve-out,
or (c) collapse them entirely and accept lossier traces.

### 5.3 Counter-only state — pattern to keep or retire?

9 actors have telemetry counter fields used only by tests. Without
them, "the actor ran" is hard to assert without inspecting reply
payloads (which test-couple to the actor's reply shape). With them,
you have field-pollution and dead-code drift.

Alternatives: (a) move counters to a separate metrics actor that all
domain actors `tell`; (b) accept counter-only fields as a workspace
test convention; (c) require every counter field to have a passing
test that reads it (no dead counters).

Currently the workspace has all three patterns simultaneously across
different actors. No rule.

### 5.4 The `*Subscriber` ambiguity in naming.md:297

Per Agent A §1.5: `naming.md` puts `*Listener` and `*Subscriber` in
the WRONG-suffix column "(when describing trait participation)". But
`Subscriber` is also the noun-shape of "subscribe" — same shape as
`Tracker`/`Cache`/`Ledger` which are in the right column. The "(when
describing trait participation)" qualifier doesn't disambiguate
sharply.

When does `Subscriber` flip from category tag to role? The skill
should answer.

### 5.5 DelegatedReply contradicts the no-detached-tasks rule

Per Agent A §1.9: `actor-systems.md:198-199` says *"No detached tasks.
If work must run independently, it is an actor or a supervised worker
pool."* `kameo.md` describes `DelegatedReply` which spawns a detached
`tokio::spawn` task. The carve-out is implicit (`actor-systems.md:240-241`
mentions DelegatedReply without naming the contradiction).

A reader of `actor-systems.md` alone concludes DelegatedReply is
forbidden. Either the no-detached-tasks rule needs the carve-out
named explicitly, or DelegatedReply needs to be flagged as an
exception with criteria.

### 5.6 What's the canonical actor-owns-redb-table shape?

Per Agent A §4.5: the workspace asserts the rule that durable state
belongs in sema, that each domain actor owns its tables, that no
shared store-actor namespace is allowed. But the *positive shape*
is missing — does the actor hold the `Database` handle or an
`Arc<Database>`? Does each handler open its own write txn? Does the
actor cache reads?

`StorageActor` is named as the anti-pattern (rust-discipline.md:824)
but no canonical positive shape is shown. Without one, the rule is
defensive without being constructive. Designer/100 §2 sketches sema
table key shapes for persona-mind specifically; that's the closest
thing to a worked example.

### 5.7 Cross-role unresolved contradictions (operator/95 vs designer/98)

Per Agent B §3.1, §3.3, §6.7: two direct conflicts unresolved since
the Kameo wave:
- **Short-lived actor per CLI invocation**: operator/95 said yes;
  designer/98 said no; operator/99 acknowledged but didn't act.
  persona-mind ARCHITECTURE.md keeps both paths open.
- **`WirePath`/`TaskToken` validation location**: operator/95 said
  "validate in persona-mind first"; designer/98 said "validate in
  contract from day one." Operator/99 deferred to designer.

Both block `primary-9iv` (the Rust persona-mind implementation wave
that hasn't landed). Need a designer/operator decision before
implementation starts.

### 5.8 `RestartPolicy::Never` for state-owning actors until durable substrate?

Per Agent B §2.13 (op-asst/98 §9): until `persona-sema` is the
durable substrate, restarting a state-owning actor loses state
(restart reconstructs from Args, not from memory). Per the
discipline, `RestartPolicy::Never` is the safe default until durable
state exists. But this isn't a workspace rule — it's a per-actor
design choice that may or may not get made. Should the skill make it
explicit?

### 5.9 `OneForAll`/`RestForOne` restart-policy bypass behavior

Per Agent B §4.9 (op-asst/99 §5.5): coordinated restart paths can
call sibling factories directly, *"apparently bypassing
`RestartPolicy::Never`."* This is a Kameo gotcha worth documenting in
`kameo.md` §"Anti-patterns and gotchas" but currently isn't.

### 5.10 The naming sweep tail

Two persona-* repos still have residual `*Actor` / `*Message` hits:
`persona-router` (1 + 1) and `persona-wezterm` (1, the dead
`TerminalDeliveryActor`). Operator's in-flight tail. Will close
itself, but worth confirming.

---

## 6 · Skill updates landed during the sweep

T1 already landed (the Handle v3 refinement after DA/6). T6 will
land additional updates:

- Sweep `ClaimNormalize` → `ClaimNormalizer` across the three skills
- Rewrite `abstractions.md:224-234` for Kameo (drop ractor, *State,
  public-handles)
- Fix `kameo.md` Calculator example (`Inc` → `Increment`, `Mul` →
  `Multiply`, `Read` → `ReadCount`)
- Fix `kameo.md:460` public ZST `Supervisor` example (give it
  fields)
- Fix broken cross-ref at `actor-systems.md:223` (cites a section
  that doesn't exist)
- Add the `oneshot`/`watch` push-witness test pattern to `kameo.md`
  (cite DA's `failure_and_mailbox.rs:94, 258, 424`)
- Add `PreparedActor::run` for state assertions to `kameo.md`
  §"Spawning" (cite DA's `data_bearing_patterns.rs:195`)
- Add the *match-on-structured-stop-reason* test pattern (cite DA's
  `failure_and_mailbox.rs:483`)
- Document the `actor-vs-data-type-collapse` rule in
  `actor-systems.md` (when an actor wraps one data type that has the
  methods, prefer `impl Actor for X` over a wrapper actor)
- Document the *aspirational-name* anti-pattern in `actor-systems.md`
  (every manifest-declared actor must have an `impl Actor`)

T7 reports to user.

In the kameo-testing repo:
- Fix `Recorder { trace: Arc<Mutex<...>> }` → `Recorder { trace: Vec<Trace> }`
- Replace 12 `std::convert::Infallible` → `kameo::error::Infallible`
- Replace 5+ magic-delay sleeps with push witnesses (oneshot/watch)

These will be a separate kameo-testing commit.

---

## 7 · Cross-role activity acknowledged

While I ran the sweep:

- **operator** swept `*Actor` / `*Message` suffixes across persona-mind,
  persona-harness, persona-system, persona, and (in flight)
  persona-router and persona-message. Lock comment: *"kameo naming
  and no-zst cleanup after designer 104"*.
- **operator-assistant** worked on `persona-router` actor-density
  (*"make router runtime an actor, remove non-actor owner wrapper"*) —
  directly addressing one of Agent C's findings and the new
  `actor-systems.md` §"Runtime roots are actors" rule.
- **designer-assistant** added the *"Runtime roots are actors"*
  section to `actor-systems.md` (commit 284da3a). New rule, lands
  during the sweep, complements the v3 single-actor-wrapper rule.

The cross-role discipline is working — multiple roles are converging
on the same patterns Agent C surfaced, without coordination.

---

## 8 · Bead trail for this sweep

Will close after T6 + T7:

- T1 (closed earlier) — DA/6 Handle position v3 refinement
- T2 — Wave 1 ingestion (4 agents)
- T3 — Wave 2 deferred (operator + operator-assistant in parallel
  + manual naming grep)
- T4 — Naming sweep (mostly done by other roles; designer confirmed
  via grep)
- T5 — this report
- T6 — skill updates with showcase examples + my own kameo-testing
  fixes
- T7 — final user report

---

## See also

- `~/primary/skills/kameo.md` — workspace usage skill (refined v3
  Handle position lands here; T6 adds showcase patterns)
- `~/primary/skills/actor-systems.md` — architectural discipline
  (newly extended with §"Runtime roots are actors" by another role
  mid-sweep)
- `~/primary/skills/rust-discipline.md` §"Actors: logical units with
  kameo"
- `~/primary/skills/naming.md` §"Anti-pattern: framework-category
  suffixes on type names"
- `~/primary/reports/designer/100-persona-mind-architecture-proposal.md`
  — the 5 implementation pins (0/5 implemented; see §5.1 open
  question)
- `~/primary/reports/designer/104-actor-runtime-and-naming.md` —
  prior closing record (v3 Handle position, naming rule)
- `~/primary/reports/designer-assistant/5-kameo-testing-assistant-findings.md`
  — DA's testing findings, folded into kameo.md
- `~/primary/reports/designer-assistant/6-public-handle-case-for-kameo.md`
  — DA's counterproposal that prompted v3
- `~/primary/reports/operator-assistant/100-kameo-persona-actor-migration.md`
  — operator-assistant's Kameo migration log
- `/git/github.com/LiGoldragon/kameo-testing` — designer's test bed
  (27 tests; T6 fixes Recorder + Infallible + magic delays)
- `/git/github.com/LiGoldragon/kameo-testing-assistant` — DA's test
  bed (15 tests; source for many showcase patterns in §2)
