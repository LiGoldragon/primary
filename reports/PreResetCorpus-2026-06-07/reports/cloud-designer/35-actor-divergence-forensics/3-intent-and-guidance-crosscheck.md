# 3 — intent authorization (adversarial) + guidance cross-check

cloud-designer, 2026-06-07. Verbatim from the verification workflow's two
remaining agents: an adversarial skeptic tasked to REFUTE "no record authorizes
the sync stack," and an independent guidance cross-check. Both materially corrected
the orchestrator's initial verdict (`1-forensic-verdict.md`).

## Part A — adversarial intent skeptic (verdict: claim "substantially correct but under-states")

**Claim under test:** No recorded psyche intent authorizes the new schema-derived
triad daemon stack being SYNCHRONOUS and using ZERO kameo; the records only defer a
specific advanced trait surface, not actors/kameo themselves.

The skeptic found records the orchestrator had NOT listed, which **positively
authorize the concurrency shape**:

- **`2alg`** (Decision High, 2026-06-06): authorizes a "concurrent worker model",
  explicitly resolving "against the single-writer serial model", with PER-REQUEST
  in-flight state and a connection-permit cap.
- **`k6w1`** (Principle High, 2026-06-06): names it the "bounded
  **thread-per-connection** worker model" and puts it in `triad-runtime` for every
  triad daemon.
- **`tj99`** (Decision High, 2026-06-06): "**BoundedWorkers** concurrent serving
  with a fresh **per-request engine** over a shared store" for the GENERATED daemon
  emitter.

These authorize the thread-per-request generated-daemon model *as such*. So a flat
"no recorded intent authorizes the thread-per-request generated daemon" is wrong.

**But** no record establishes the *specific properties* "sync" or "no kameo":
- No record names kameo, blesses or forbids an actor runtime.
- No record chooses sync vs async. `opvx`: "the public contract does not encode how
  parallel a daemon runs."
- The deferrals (`czw0`/`1487`, `59dr`, `1483`) defer the actor
  **mailbox / backpressure / runtime-control / scheduling** machinery — not actors
  as a concept.
- "Actor" language is used architecturally throughout (`u1nr` "decision-making
  actor system over schema-emitted nouns"; `e440` "single-writer actor") — but as
  *conceptual* actors, not kameo-the-crate.

**Live contradiction in repo docs:** `lojix/ARCHITECTURE.md` (Status 2026-05-15,
stale, pre-triad-port) still says "Each daemon actor is a Kameo actor"; the actual
`triad-port/` code dropped kameo. Never updated past the rewrite — a manifestation
gap.

**Skeptic bottom line:** the thread-per-request *concurrency shape* IS authorized
(`2alg`+`k6w1`+`tj99`); the precise "synchronous + zero-kameo" property is NOT
authorized *as such* — it is an agent realization consistent-with the authorized
thread model, never explicitly chosen, and actively contradicted by stale lojix
docs. The original claim's spirit is largely right; its letter ("records only
defer") is too strong.

## Part B — guidance cross-check (verdict: present-tense mandate YES, but a carve-out DOES exist — in a different file)

Prior reading under test: "`actor-systems.md` mandates actors in the present tense
for schema-derived daemons, with NO today-sync/eventually-actors carve-out."
Verdict: **half right.** The present-tense mandate is real; the "no carve-out"
claim is **refuted** — an explicit deferral carve-out exists, in
`component-triad.md` (Spirit `1483` + `1487`).

### (a) Present-tense actor mandate? YES.
`skills/actor-systems.md`, as standing discipline:
- L65: "**Actors all the way down.**"
- L86-89: "In schema-driven daemons, the three default actor-shaped planes are
  Signal, Nexus, and SEMA."
- L557-558: "A daemon, service, router, watcher, database owner, or runtime root
  **is** an actor."
- Runtime default is kameo 0.20 (L21-25).

### (b) Sync-now / actors-eventually carve-out? YES — in `component-triad.md`, not `actor-systems.md`.
`skills/component-triad.md` §"Runtime triad engine traits" is the substrate that
actually **landed** (`triad_main!` emitted daemon module, `triad-runtime` runner,
spirit pilot at parity). It is **synchronous schema-emitted trait methods, not
actor mailboxes**:
- `NexusEngine::execute(&mut self, NexusWork) -> NexusAction` — `&mut self` is the
  single-flight guard, a plain method, no mailbox.
- `SemaEngine::apply(&mut self, …)` / `observe(&self, …)`.
- Driven by a runner loop reading `NexusAction` variants on the same call stack.

The deferral, verbatim:
- **Spirit `1487`** (= `czw0` text): "Full actor mailbox, backpressure, and
  runtime-control traits stay deferred; lifecycle hooks are the minimum addressable
  surface…"
- **Spirit `1483`**: "Workspace explicitly defers … actor scheduling/prioritization
  and related deeper-runtime work … future-deeper-runtime that won't be touched for
  a while."
- "if the actor-trait promotion lands later, it composes as a supertrait extension
  without breaking the engine-trait substrate."
- "The substrate above is what lands now; deeper work arrives if/when overload
  evidence appears in real production load."

That is precisely a *today = engine-trait methods (effectively sync, no mailbox);
eventually = kameo-actor promotion* carve-out.

### (c) Where is the actor-density truth-pin?
In `actor-systems.md` as standing discipline (not a numbered "actor density is
required" pin): L65 "Actors all the way down" and L558 "a daemon … is an actor",
enforced by §"Test actor density" (topology-manifest, actor-count, no-zst-actor
tests). INTENT.md's Pattern B describes Signal/Nexus/SEMA purely as schema-emitted
engine traits (`execute`, `apply`/`observe`), never as a required kameo topology —
consistent with the component-triad deferral.

### Net
The two skills are in **genuine tension**. `actor-systems.md` asserts the actor
end-state as present-tense discipline; `component-triad.md` (Spirit `1483`/`1487`)
carries the explicit deferral that makes the currently-generated daemon stack run
on synchronous engine-trait methods with kameo mailbox/supervision promotion
postponed. Anyone citing `actor-systems.md` to claim "the generated daemon must be
kameo actors today, no exceptions" is overreading; anyone citing `component-triad.md`
to claim "actors are deferred, sync is the sanctioned end-state" is also overreading
— the deferral is explicitly conditional ("until overload evidence appears").
