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

---

## 0.5 · Decisions just landed (2026-05-10)

User answered four of the questions below via `AskUserQuestion`.
Recorded as durable decisions; the relevant question sections below
are rewritten to reflect them. Beads filed.

| # | Question | Decision | Action |
|---|---|---|---|
| Q-dec-1 | CLI lifecycle (one-shot vs daemon) | **Daemon**: long-lived process owns `MindRoot`; CLI calls connect as thin clients | Note added to existing bead `primary-9iv` |
| Q-dec-2 | `WirePath` / `TaskToken` validation location | **Split**: contract enforces value invariants; runtime enforces environment facts (target exists, claim is open, route is reachable) | Note added to `primary-9iv` |
| Q-dec-4 | designer/100's 5 implementation pins | **Designer-assistant pre-pass first**: verify which pins are still load-bearing, then bundle into one bead | New P1 bead: `primary-qqb` |
| Q-app-2 | Forwarding-trampoline actors | **Rename to `*Phase` + document trace-as-domain carve-out** | Skill carve-out landed in `~/primary/skills/actor-systems.md` §"Actor or data type"; new P2 bead `primary-9yq` for the persona-mind rename |

Q1+Q2 together resolve the operator/95-vs-designer/98 contradictions
that had blocked `primary-9iv` since the Kameo wave.

Still open after this round: §3 Q-app-1 (5 data-type-shadowed actors
collapse), §3 Q-app-3 (ActorKind enum split), §4 Q-dec-3 (`MindRuntime`
promote/delete/keep), §4 Q-dec-5 (`RestartPolicy::Never` default),
§5 Q-skill-1 through Q-skill-3.

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
| Designer/100's 5 implementation pins (0/5 done) | **DECIDED** | Bead `primary-qqb` filed (DA pre-pass). Q-dec-4 |
| operator/95 vs designer/98 lifecycle contradiction | **DECIDED** | Daemon. Note on `primary-9iv`. Q-dec-1 |
| operator/95 vs designer/98 validation-location contradiction | **DECIDED** | Split (contract for value, runtime for environment). Note on `primary-9iv`. Q-dec-2 |
| Forwarding-trampoline actors — application | **DECIDED** | Rename to `*Phase` + carve-out landed in skill. Bead `primary-9yq` filed. Q-app-2 |
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

### Q-app-2. **DECIDED**: rename `*Supervisor` → `*Phase`; trace-as-domain carve-out lands in `actor-systems.md`

Four `LongLived` actors in persona-mind have only `ActorRef<_>`
fields and forward messages while emitting trace events
(`IngressSupervisor`, `DispatchSupervisor`, `DomainSupervisor`,
`ViewSupervisor`). The trace plane IS the domain — each forwarding
hop is a witness that the pipeline ran a particular stage.

**Skill change landed**: `~/primary/skills/actor-systems.md`
§"Actor or data type" gains a *"Phase actors are the second
exception"* paragraph. A `*Phase` actor earns its place when (1)
the trace event is structurally part of the domain witness contract,
(2) a test asserts the witness was emitted, (3) supervision happens
elsewhere — the name doesn't lie.

**Bead filed**: `primary-9yq` for operator-assistant — rename the
four trampolines + corresponding `ActorKind` variants + manifest
entries. Blocked-by the skill update (already landed).

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

### Q-dec-1. **DECIDED**: persona-mind CLI hits a daemon

The Rust `persona-mind` implementation is a long-lived daemon
process owning `MindRoot`. CLI calls (`persona mind ...`) connect
as thin clients (Unix socket + signal-core frames). Not one-shot
per call.

This resolves the operator/95-vs-designer/98 contradiction that
had been blocking `primary-9iv`. The supervision tree is observable
across calls; warm state is preserved.

**Bead update**: design constraint added as a note on existing bead
`primary-9iv`. Daemon installation/lifecycle/recovery is part of
that bead's scope.

---

### Q-dec-2. **DECIDED**: split validation — contract for value invariants, runtime for environment

Contract enforces what makes a value *valid*: shape, format,
structural rules. `signal-persona-mind` already does this for
`WirePath` (absolute path, no `..`, normalized `.`/repeated
components), `TaskToken` (no brackets/whitespace/empty),
`ScopeReason` (no empty/multiline), `TimestampNanos` (store-supplied).

Runtime enforces what makes a value *meaningful right now*: target
exists, claim is currently open, route is reachable, etc.

The line between value invariant and environment fact is sharp and
natural. Contract changes are slow but correct; runtime changes are
fast but transient.

**Bead update**: design constraint added as a note on `primary-9iv`.

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

### Q-dec-4. **DECIDED**: designer-assistant pre-pass first, then bundle

Designer-assistant claims a 1-2 hour pre-pass to verify which of
designer/100's 5 implementation pins are still load-bearing against
the current `persona-mind` state (some may have been overtaken by
topology changes since 100 was written). Output: a designer-assistant
report that lets operator-assistant either claim the surviving pins
as one bundled bead or understand the spec deltas needed first.

The 5 pins (DisplayId mint, sema table key shapes, caller-identity
3-layer, `mind.redb` path with env override, subscription contract
sketch) — see designer/100 for the original spec.

**Bead filed**: `primary-qqb` (P1, assigned designer-assistant).

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
