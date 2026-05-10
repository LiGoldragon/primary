# 106 — Actor discipline: status + open questions

*Designer report. Supersedes designer/104 (Kameo runtime + naming
agglomeration) and designer/105 (project-wide actor sweep) — both
deleted in the same commit that lands this report. Substance is now
either in `~/primary/skills/`, in landed commits across the persona-*
runtime crates, or carried forward as one of the questions below.*

---

## 0 · TL;DR

Two waves landed in parallel during this report's authoring:

1. **operator + operator-assistant** landed Kameo runtime work across
   `persona-router`, `persona-message`, `persona-system`,
   `persona-harness`, `persona-wezterm`, `persona`, and
   `persona-mind` — six commits in ~90 minutes that resolved much of
   the topology cleanup the prior sweep called for.
2. **designer-assistant** landed `actor-systems.md` updates (commit
   `a9c73b06`) that codify rules for: data-type-shadowed actors,
   forwarding trampolines, the `DelegatedReply` carve-out, and the
   manifest-aspirational-name anti-pattern.

Net result: most of the design-philosophy questions in the prior
sweep are now answered by the new rules. **The remaining questions
fall in three buckets**:

- **Application** — the rule has spoken; should designer file beads
  to enforce it against current code, or wait for operator's natural
  next cycle? (§3)
- **Decisions still needed** — design calls the rules don't make
  (orchestrate-CLI shape, contract-vs-runtime validation, etc.). (§4)
- **Skill clarifications I'll land if you don't object** — small
  edits where the right answer is plain. (§5)

Skip to §3 if you want the decisions.

---

## 1 · Status: what's resolved, what's open

| Sweep finding | Status | Where it landed |
|---|---|---|
| `RouterRuntime` non-actor wrapper | **RESOLVED** | `persona-router/src/router.rs:209` — `impl kameo::actor::Actor for RouterRuntime` (commit `6839fa`) |
| `MindRoot` double-wrapper (3 layers) | **PARTIALLY** | Reduced to 2 layers (`MindRuntime → ActorRef<MindRoot>`); `MindRootHandle` removed. `MindRuntime` still a non-actor single-wrapper. (Q-dec-3 below) |
| Three different public-surface conventions | **CONVERGED** | persona-router and persona-message use raw `ActorRef` + actor types; persona-mind reduced as above |
| `*Actor` suffix sweep tail | **DONE** | `bfd2c0` (`TerminalDeliveryActor` → `TerminalDelivery`); `fe2cdb` (persona-router); zero `*Actor` suffix on any `impl Actor` type across persona-* |
| `ClaimNormalize → ClaimNormalizer` rename, abstractions.md rewrite, ZST `Supervisor` example fix, Calculator naming | **DONE** | Commit `4413f01` (T6) |
| `kameo-testing` self-bugs (Recorder shared-lock, Infallible imports, magic delays) | **DONE** | Commit `ea1d417f` |
| Data-type-shadowed actors — *rule for when to collapse* | **RULE LANDED** | `actor-systems.md:111-128` §"Actor or data type" — designer-assistant commit `a9c73b06`. Application to 5 specific cases: Q-app-1 below |
| Forwarding-trampoline actors — *rule* | **RULE LANDED** | Same section: *"if the type has only `ActorRef<_>` fields and just forwards messages, it is a forwarding helper, not an actor"*. Application to 4 cases: Q-app-2 below |
| `DelegatedReply` contradicts no-detached-tasks | **RESOLVED IN SKILL** | `actor-systems.md:233-238` — explicit carve-out for short reply deferrals; long-lived work still requires a supervised actor |
| Manifest-declared actors without `impl Actor` | **RULE LANDED** | `actor-systems.md:136-140` — *"every manifest-declared actor must have a concrete `impl Actor`. Trace-only variants in an `ActorKind` enum are not actors. Either create the actor, or rename the enum to the thing it really is (`PipelinePhase`, `TracePoint`, `ResidencyPlane`)"*. Application to `persona-mind`'s `ActorKind`: Q-app-3 below |
| `TerminalDelivery` never spawned | **RULE-DECIDED** | The new "actor or data type" rule says delete; offering for confirmation as Q-app-1 case |
| `ActorKind` 47/9 "gap" framing | **REFRAMED** | `persona-mind/src/actors/manifest.rs:30-107` — `ActorResidency::TracePhase` makes "trace marker" an explicit residency. The 38 trace variants are by-design trace phases, not unimplemented actors. Q-app-3 is now whether to also split the static enum |
| Designer/100's 5 implementation pins (0/5 done) | **STILL OPEN** | Q-dec-4 |
| operator/95 vs designer/98 contradictions block primary-9iv | **STILL OPEN** | Q-dec-1, Q-dec-2 |
| Counter-only state pattern policy | **STILL OPEN** | Q-skill-3 |
| `RestartPolicy::Never` default for state-owning actors | **STILL OPEN** | Q-skill-4 |
| `*Subscriber` ambiguity in `naming.md:297` | **STILL OPEN** | Q-skill-1 |
| `OneForAll`/`RestForOne` restart-policy bypass | **STILL OPEN** | Q-skill-2 |

---

## 2 · How the persona-mind topology now reads

Worth reading before §3, because the new `ActorResidency` classification
in `/git/github.com/LiGoldragon/persona-mind/src/actors/manifest.rs:30-107`
clarifies what the topology is *trying* to be:

- **`Root`** (1 actor): `MindRoot`. The supervision-tree root.
- **`LongLived`** (8 actors): `Config`, `IngressSupervisor`,
  `DispatchSupervisor`, `DomainSupervisor`, `StoreSupervisor`,
  `ViewSupervisor`, `SubscriptionSupervisor`, `ReplySupervisor`. Real
  `impl Actor` types.
- **`TracePhase`** (~38 variants): `RequestSession`, `NotaDecoder`,
  `EnvelopeBuilder`, `ClaimFlow`, `MemoryFlow`, `QueryFlow`, `ItemOpen`,
  `NoteAdd`, `Link`, `SemaWriter`, `SemaReader`, `IdMint`, `Clock`,
  etc. **No `impl Actor` types — explicitly trace markers.**

So the prior framing of "47 named actors but only 9 implemented" was
wrong: the architecture is saying *"these 38 are trace phases, by
design, not actors at all."*

The new `actor-systems.md` rule (the `PipelinePhase` / `TracePoint` /
`ResidencyPlane` rename suggestion) directly applies — see Q-app-3.

---

## 3 · Application questions — rule has spoken; file beads now or wait?

The new `actor-systems.md` rules answer these clearly. The remaining
question is purely whether designer files beads now (with operator
currently on contract-naming work for designer-assistant/7) or waits
for operator's natural next cycle.

### Q-app-1. Five data-type-shadowed actors — rule says collapse 3 + delete 2

Per `~/primary/skills/actor-systems.md:111-128` §"Actor or data type":

> *"If the wrapped data type already owns the state and verbs, put the
> mailbox on that type."*

> *"If the wrapper owns lifecycle, supervision, admission control,
> backpressure, restart policy, or a real child set, keep the wrapper
> actor and make those responsibilities explicit in its fields and
> tests."*

The five cases and what the rule says:

| Actor | File | Wraps | Wrapper owns? | Verdict |
|---|---|---|---|---|
| `StoreSupervisor` | `persona-mind/src/actors/store.rs:11` | `MemoryState` (handler does `self.memory.dispatch_envelope(envelope)`) | nothing extra | **collapse to `impl Actor for MemoryState`** |
| `Config` | `persona-mind/src/actors/config.rs:7` | `StoreLocation` (only message is `#[allow(dead_code)] ReadStoreLocation`) | nothing — only message is dead code | **delete the actor** |
| `Ledger` | `persona-message/src/actors/ledger.rs:9` | `MessageStore` (handler does `envelope.execute(&self.store)`) | one counter | **collapse to `impl Actor for MessageStore`** |
| `NiriFocus` | `persona-system/src/niri_focus.rs:9` | `FocusTracker` (handler does `self.tracker.apply_event(...)`) | two counters | **collapse to `impl Actor for FocusTracker`** |
| `TerminalDelivery` | `persona-wezterm/src/terminal.rs:122` | `WezTermMux` — but **never spawned in production**; consumer at `persona-router/src/harness_delivery.rs:55` calls `mux.pane(pane_id).deliver(&prompt)` synchronously | nothing — and the actor isn't even used | **delete the actor** |

Net: 3 collapses, 2 deletes, across 4 repos. **Operator's lane to
implement.**

**Question for you**: file 5 P2 beads (one per actor), 1 batched P2
bead ("apply data-type-shadowing rule across persona-*"), or wait for
operator's natural cycle?

**My recommendation**: 1 batched bead. The rule is one rule; the
application is one work session.

---

### Q-app-2. Four forwarding-trampoline actors in persona-mind — rule says collapse, but the trace plane needs somewhere to go

Per `~/primary/skills/actor-systems.md:126-128`:

> *"If the type has only `ActorRef<_>` fields and just forwards
> messages, it is a forwarding helper, not an actor. Either give it
> real state/failure policy or collapse it into the parent."*

The four trampolines:

`/git/github.com/LiGoldragon/persona-mind/src/actors/dispatch.rs:14-18`:

```rust
pub(super) struct DispatchSupervisor {
    domain: ActorRef<domain::DomainSupervisor>,
    view:   ActorRef<view::ViewSupervisor>,
    reply:  ActorRef<reply::ReplySupervisor>,
}
```

Same shape: `IngressSupervisor` (1 child ref), `DomainSupervisor` (1
child ref), `ViewSupervisor` (1 child ref). All are `LongLived` per
the manifest, all are named `*Supervisor` despite not actually
supervising (supervision is set up in `MindRoot::on_start`).

The rule says: collapse into the parent (`MindRoot`). But these
actors emit trace events on the way through — and the trace plane is
arguably the domain (each hop witnesses that the pipeline ran a
particular stage).

**Two readings**:

(a) **The rule is right; collapse into `MindRoot`.** Trace emission
   becomes free-function calls from `MindRoot` handlers. Lose the
   per-stage actor witness; gain one fewer actor layer. Cleaner code.

(b) **The trace plane IS the domain; rename and document.** Rename
   `*Supervisor` → `*Phase` (matching `TracePhase` residency).
   Document the carve-out in `actor-systems.md`: *"phase actors —
   actors whose only state is downstream `ActorRef`s and whose only
   behavior is forward-with-trace — are acceptable when the trace
   plane IS the domain."* Adds an exception to the rule.

**Question for you**: which reading? My recommendation is (b) — the
actors do have a real reason (witness emission), and the misleading
`*Supervisor` name is the actual problem. But this is a design call.

If (b): file 1 P2 bead "rename `*Supervisor` → `*Phase` in
persona-mind; document trace-phase carve-out in `actor-systems.md`."
If (a): file 1 P2 bead "collapse 4 trampolines into `MindRoot`."

---

### Q-app-3. `ActorKind` enum mixes real actors with trace phases — rule says split

Per `~/primary/skills/actor-systems.md:136-140`:

> *"Every manifest-declared actor must have a concrete `impl Actor`.
> Trace-only variants in an `ActorKind` enum are not actors. Either
> create the actor, or rename the enum to the thing it really is
> (`PipelinePhase`, `TracePoint`, `ResidencyPlane`) so tests do not
> mistake an aspirational name for runtime architecture."*

Current state in `persona-mind`: `ActorKind` has 47 variants, only 9
are real actors. Manifest classifies via `ActorResidency::TracePhase`,
but the enum itself doesn't distinguish. A future agent writing
`ActorKind::IdMint` in a spawn or ref position compiles fine but
finds no actor.

The rule says: split. Two enums — one for real actors, one for trace
phases.

**The work**: rename ~38 of `ActorKind`'s variants out into a new
enum. ~50-100 call sites across `persona-mind/src/actors/` need
re-typing. Trace-event emission infrastructure stays roughly the same
shape (just typed differently).

**Question for you**: file 1 P2 bead now ("split `ActorKind` per
`actor-systems.md` rule"), or wait for the next persona-mind work
cycle? My recommendation: file the bead, but tag it as blocked-by
Q-app-2 — the trampoline rename (if (b)) might naturally fold this
work in.

---

## 4 · Decision questions — still need your judgment

### Q-dec-1. orchestrate CLI: one-shot per call vs daemon?

Open since designer/98 critiqued operator/95. The Kameo wave didn't
decide; operator/99 deferred to designer; nothing since.

- **operator/95** says YES one-shot: each `persona mind ...` CLI
  invocation spawns a fresh actor that processes the request and
  exits. Lifecycle is bounded. No daemon to install/manage.
- **designer/98** says NO: actors should be long-lived state owners;
  CLI-per-call loses warmed state, persistent connections, and the
  supervision tree's value.
- `persona-mind/ARCHITECTURE.md` keeps both paths open (deliberately,
  per operator/99).

**Why it matters**: every persona-mind handler that touches per-call
state will work differently depending on the answer. Lifecycle of a
CLI call depends on it. `primary-9iv` (Rust persona-mind
implementation) can't progress without the call.

**Options**:

(i) **One-shot per call.** Simple lifecycle. Each CLI call fresh. No
   daemon to install/configure/recover. Lose warmed state and
   connection pooling.
(ii) **Daemon.** Long-lived state. Connection pooling. Better for
   bursty work. Requires daemon installation and lifecycle.
(iii) **Both, selectable by env or flag.** Most flexible; most
   complexity.

**My recommendation**: (ii) daemon. The supervision tree is the
load-bearing thing; a daemon makes it observable across CLI calls.
But this is genuinely your call.

---

### Q-dec-2. `WirePath` / `TaskToken` validation — contract or runtime?

Same provenance as Q-dec-1.

- **operator/95** says: validate in `persona-mind` first; contract
  validation can come later as a hardening pass.
- **designer/98** says: validate in the contract from day one;
  runtime can't be the source of truth for what's a valid wire path.

**Why it matters**: every contract addition needs the answer. If
runtime validates, contract is just a `String` newtype. If contract
validates, contract carries the semantic rules.

**Options**:

(i) **Contract validates.** `WirePath::new(...)` returns `Result<Self,
   WirePathError>`. Runtime trusts. Design pressure forces the
   contract to be exact. Slower contract iteration; more correct
   types.
(ii) **Runtime validates.** Contract is shape-only; runtime checks.
   Faster contract iteration; runtime owns rules.
(iii) **Both.** Contract for shape; runtime for semantics (e.g.,
   target exists). Most defensive.

**My recommendation**: (i). Contract repos are the most-load-bearing
typed surfaces in the workspace (per designer-assistant/7); validation
belongs there. But this is your call.

---

### Q-dec-3. `MindRuntime` — promote to actor, delete, or keep?

Current shape (`/git/github.com/LiGoldragon/persona-mind/src/service.rs`):

```rust
pub struct MindRuntime {
    root: ActorRef<MindRoot>,
}
```

The new `actor-systems.md:242-261` §"Runtime roots are actors"
section says:

> *"A struct that merely owns several `ActorRef<_>` values and
> exposes convenience methods is a hidden non-actor owner."*

> *"A public domain facade may wrap the root actor when it earns its
> place under `skills/kameo.md` §"Public consumer surface": lifecycle
> ownership, topology insulation, safe fallible-message handling,
> capability narrowing, domain errors, domain verbs, or library
> publication. That facade is not the runtime owner; the root actor
> still owns the actor tree."*

`MindRuntime` only holds *one* `ActorRef`, not several — so it's at
the edge of the multi-ref rule. Currently it doesn't have any domain
methods that earn the facade role. It's an empty wrapper.

**Options**:

(a) **Promote `MindRuntime` to an actor.** `impl Actor for
   MindRuntime` with `MindRoot` as a child. Symmetry with
   `RouterRuntime` (which was just promoted). Cost: refactor of
   `MindRuntime`'s lifecycle code.
(b) **Delete `MindRuntime`; expose `ActorRef<MindRoot>` directly.**
   Per the v3 Handle position in `kameo.md`: `ActorRef<A>` IS the
   public surface unless a wrapper earns its place. `MindRuntime`
   doesn't earn it. Cost: consumers retype.
(c) **Keep `MindRuntime` and grow it** into a domain facade with
   actual domain methods (`mind.submit(...)`, `mind.query(...)`,
   etc.). Earns its place per the kameo.md rule. Cost: design + impl.

**My recommendation**: (b) for now. The wrapper isn't doing
anything; deleting it is cheapest. If a domain facade emerges later
(per (c)), it can be added then with real reason.

---

### Q-dec-4. Designer/100's 5 implementation pins remain 0/5 done

The 5 pins from
`~/primary/reports/designer/100-persona-mind-architecture-proposal.md`,
none implemented after the Kameo wave:

1. **DisplayId mint algorithm**: BLAKE3 + base32-crockford, 8 chars.
   Currently `persona-mind/src/memory.rs:398-418` uses a counter stub.
2. **Sema table key shapes**: redb schemas for items, notes, edges,
   aliases, scopes, statuses, claims, sessions. No `tables.rs`
   exists; no `persona-sema` dependency in `persona-mind`'s
   `Cargo.toml`.
3. **Caller-identity 3-layer resolution**: actor → role → principal.
   Currently every spot uses hardcoded `ActorName::new("persona-mind")`
   (per op-asst/97 P1).
4. **`mind.redb` path with env override**:
   `~/.local/share/persona-mind/mind.redb` plus `PERSONA_MIND_DB`
   override. Phase 2 not started.
5. **Subscription contract sketch**: how the change-feed works
   against the redb store. Phase 5 deferred entirely.

The Kameo migration covered topology — the supervision tree exists,
the actor shapes are right, names are clean. But the *content* of
those actors (what data they own, where it persists, who they speak
as) is still stub.

Operator and operator-assistant landed 6 crates of Kameo migration
without folding these in, and have now moved on to the contract
relation naming work prompted by designer-assistant/7. The pins sit
in operator's lane but nobody's claimed them.

**Why it matters**: `primary-9iv` (Rust persona-mind implementation
wave) is the bead pointing at this work. It can't progress until
either the pins land or get reframed.

**Options**:

(a) **File 5 separate P1 beads, one per pin**, and let next operator
   cycle work them. Risk: blocks other work; operator may prioritize
   in-flight contract naming first.
(b) **One bundled P1 bead** "persona-mind implementation pins
   (designer/100 §1-§5)" claimed in one wave by operator-assistant.
(c) **Wait.** Operator's currently on contract-naming work; these
   may surface naturally next cycle.
(d) **Designer-assistant claims a pre-pass: re-read designer/100
   against current code, verify which pins are still load-bearing.**
   Some may have been overtaken by topology changes since 100 was
   written.

**My recommendation**: (d) first (1-2 hours of designer-assistant
work to verify pins are still live), then (b) based on result.

---

### Q-dec-5. `RestartPolicy::Never` for state-owning actors as workspace default — until durable substrate?

Until `persona-sema` is the durable backing for state-owning actors,
restarting one loses state. Kameo's restart reconstructs from `Args`,
not from mutated state — so a counter at 12 reads back as 0 after
restart.

Per the supervision discipline, `RestartPolicy::Never` would be the
safe default for state-owning actors without durable backing — fail
loud rather than fail silent. Currently it's a per-actor choice; the
workspace hasn't picked.

**Why it matters**: a supervised state-owning actor that restarts
after panic silently loses everything it had been told. Worse, it
silently keeps running and accepting writes against an empty state.
This is a correctness footgun.

**Options**:

(a) **Add to `actor-systems.md`: state-owning actors default to
   `RestartPolicy::Never`; `Permanent` requires explicit comment
   justifying the durable-recovery story.** Cheap rule that prevents
   a class of silent bugs.
(b) **Keep case-by-case.** No workspace rule. Current state.
(c) **Block harder: forbid state-owning actors without sema-backed
   durability.** Most disciplined; biggest blast radius (what counts
   as "state-owning" is a spectrum).

**My recommendation**: (a). I can land it in `actor-systems.md`
myself if you say yes — no further user input needed.

---

## 5 · Skill clarifications I'll land if you don't object

Smaller items. Listed for your veto:

### Q-skill-1. `*Subscriber` suffix in `naming.md:297`

Currently in the WRONG-suffix column with the qualifier "(when
describing trait participation)". But `Subscriber` is also the
noun-shape of "subscribe" — same shape as `Tracker` / `Cache` /
`Ledger` (right column). The qualifier doesn't disambiguate sharply.

**My fix**: rewrite the entry to clarify "wrong as a generic
trait-participation tag (e.g., `EventSubscriber` to mean 'thing that
implements `Subscribe`'); right as the role of a thing that genuinely
subscribes (e.g., `Subscriber` as the long-lived actor on the
receiving side of a publish/subscribe channel)." Add a worked
example showing both.

### Q-skill-2. `OneForAll` / `RestForOne` restart-policy bypass — Kameo gotcha to document

Per `op-asst/99` §5.5: coordinated restart paths can call sibling
factories directly, *"apparently bypassing `RestartPolicy::Never`."*

Currently undocumented in `kameo.md`. **My fix**: add to `kameo.md`
§"Anti-patterns and gotchas" with a code example showing the path,
and a recommendation (test the bypass behavior explicitly if your
supervision strategy is `OneForAll` or `RestForOne`).

### Q-skill-3. Counter-only state convention

Nine actors carry `_count: u64` fields used only by tests. Several
go unread (`applied_event_count`, `delegated_delivery_count`,
`last_status_requester`). `RouterRuntime` just added two more in
commit `6839fa`.

**Without** counters, "the actor ran" is hard to assert without
inspecting reply payloads (which couples tests to reply shape).
**With** counters, you have field pollution and dead-code drift.

**My fix**: add to `actor-systems.md` — *"counter-only state fields
are permitted as test witnesses, but every counter field must be read
by at least one test. Unread counters are dead code."* This auto-prunes
the drift case.

(If you'd rather force counters out entirely in favor of push
witnesses (per `kameo.md` test patterns), say so and I'll land that
instead.)

### Q-skill-4. `RestartPolicy::Never` default

If you say yes to Q-dec-5(a), I land the rule in `actor-systems.md`.

---

## 6 · Cross-role coordination acknowledged

While I was writing this report:

- **operator** is on contract relation naming work (`primary-28v`),
  driven by designer-assistant/7's contract survey. Working on
  `signal`, `signal-persona`, plus 4 channel contracts in parallel
  with operator-assistant.
- **operator-assistant** is on the same contract sweep (4 contracts
  in parallel with operator).
- **designer-assistant** added `actor-systems.md` rules (commit
  `a9c73b06`) that pre-empted four of my open questions at the
  rule level.
- **system-specialist** wrote
  `system-specialist/100-wezterm-live-palette-research.md` —
  separate concern (Chroma WezTerm theme switching), not part of
  this actor sweep.

The discipline is converging across roles without coordination. The
next big work-front based on what's in flight: contract relation
naming (operator + op-asst, in flight), then likely the application
of the new actor-systems.md rules to persona-mind (Q-app-1, Q-app-2,
Q-app-3 above).

---

## 7 · Bead trail

- Open beads relevant to this report: `primary-9iv` (Rust persona-mind
  implementation wave), `primary-2w6` (persona-message off
  text-files+polling), `primary-28v` (contract relation naming and
  actor-runtime truth — currently held by operator).
- New beads to open if you say yes:
  - Q-app-1 (collapse 5 data-type-shadowed actors): 1 batched P2
  - Q-app-2 (collapse OR rename 4 trampolines): 1 P2
  - Q-app-3 (split `ActorKind` enum): 1 P2, blocked-by Q-app-2
  - Q-dec-4 (designer/100 pins re-read + claim): 1 P1 (designer-
    assistant pre-pass) + 1 P1 (operator-assistant implementation)

---

## See also

- `~/primary/skills/kameo.md` — workspace usage skill (Handle v3
  position, anti-patterns, test patterns)
- `~/primary/skills/actor-systems.md` — architectural discipline
  (recently extended with §"Actor or data type", §"Runtime roots are
  actors", and the `DelegatedReply` carve-out)
- `~/primary/skills/rust-discipline.md` §"Actors: logical units with
  kameo"
- `~/primary/reports/designer/100-persona-mind-architecture-proposal.md`
  — the 5 implementation pins (Q-dec-4)
- `~/primary/reports/designer/98-critique-of-operator-95-orchestrate-cli-protocol-fit.md`
  — the unresolved contradictions (Q-dec-1, Q-dec-2)
- `~/primary/reports/operator-assistant/100-kameo-persona-actor-migration.md`
  — the migration log
- `~/primary/reports/operator-assistant/99-kameo-adoption-and-code-quality-audit.md`
  — production-readiness judgment + concerns (`OneForAll` bypass,
  detached work first-class, etc.)
- `~/primary/reports/operator/104-kameo-migration-prognosis.md` —
  current-state snapshot
- `~/primary/reports/designer-assistant/7-contract-relation-naming-survey.md`
  — what operator + op-asst are currently working on
