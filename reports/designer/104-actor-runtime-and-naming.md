# 104 — Actor runtime and naming

*Designer report. Agglomerates the Kameo runtime switch and the
no-Actor-suffix naming rule into one closing record. Supersedes
designer/102 (Kameo deep dive) and designer/103 (Kameo wave
landed) — both deleted in the same commit that lands this report,
with their substance preserved in `~/primary/skills/kameo.md`,
`~/primary/skills/actor-systems.md`, and the present report.*

---

## 0 · TL;DR

Two settled decisions:

1. **Workspace runtime is Kameo 0.20** (replaces direct `ractor`).
   `Self` IS the actor; `Args = Self` is the documented common
   case; supervision is declarative; library users see
   `ActorRef<A>` directly. Deep substance in
   `~/primary/skills/kameo.md`; falsifiable source in two test
   repos:
   - `/git/github.com/LiGoldragon/kameo-testing` (designer; 27
     passing tests).
   - `/git/github.com/LiGoldragon/kameo-testing-assistant`
     (designer-assistant; 15 complementary tests).

2. **Drop the `Actor` suffix from type names.** A `Counter` that
   implements `Actor` IS an actor; the suffix is framework category,
   not role. Same rule for messages (`Inc`, not `IncMessage`),
   replies (`SubmitReceipt`, not `SubmitReply`), and consumer
   surfaces (`ActorRef<Counter>`, not `CounterHandle`).
   Role-descriptive suffixes (`Supervisor`, `Normalizer`,
   `Resolver`) stay — they name what the type does.

Both decisions captured across `skills/kameo.md` (new),
`skills/actor-systems.md` (updated to drop suffix in example
tables and supervision diagram), `skills/rust-discipline.md`
(updated `*Handle`-wrapper language), `skills/naming.md` (new
anti-pattern section: framework-category suffixes), and
`skills/autonomous-agent.md` (new active-beads-check section,
landed earlier in the wave).

---

## 1 · The Kameo switch — what landed

The wave produced:

| Where | What |
|---|---|
| `/git/github.com/LiGoldragon/kameo-testing` | Designer's test bed. `crane+fenix` flake mirroring signal-core's shape. 27 passing tests across 9 files (lifecycle, messages, spawn, mailbox, registry, supervision, streams, links, topology). |
| `~/primary/skills/kameo.md` | New workspace skill. Core shape, naming, ActorRef as public surface, module map, lifecycle hooks, messages/replies, spawn, supervision, mailbox, registry, streams, links, anti-patterns, maturity signals. Every claim cited against the test repo. |
| `~/primary/skills/autonomous-agent.md` | New top-level section *"Active beads — check first, work them through"*. The protocol used to run this wave end-to-end. |
| `~/primary/skills/actor-systems.md` | Kameo as runtime default; example tables and supervision diagram updated to drop the `Actor` suffix; `*Handle` wrapper language retired. |
| `~/primary/skills/rust-discipline.md` | §"Actors: logical units with kameo" rewritten — declarative supervision, the tell-of-fallible-handler trap, ActorRef as the library-public surface. |
| `~/primary/skills/naming.md` | New anti-pattern §: framework-category suffixes on type names. Cross-references kameo's naming section. |

Operator and operator-assistant carried out the parallel
implementation (operator-assistant/100 *"Kameo Persona Actor
Migration"*): persona-mind, persona-router, persona-message,
persona-system, persona-harness, persona-wezterm migrated to
direct Kameo. persona-sema stays a library, untouched.

Designer-assistant landed `kameo-testing-assistant` and report 5
*"Kameo testing assistant findings"* — complementary test bed +
findings folded into `skills/kameo.md` (Maturity subsection,
restart-reconstructs-from-Args, observational-vs-supervision
links, Rust 1.88 MSRV note).

---

## 2 · Why Kameo, captured for future readers

The framework's shape agrees with the workspace's discipline.
Concretely:

| Workspace rule | Kameo native shape |
|---|---|
| Public actor nouns must carry data (`skills/actor-systems.md` §"Rust shape") | `Self` IS the actor; `Args = Self` is the documented common case |
| Verbs live on the data-bearing noun | All lifecycle hooks take `&mut self`; methods on the actor type directly |
| Typed mailbox per actor | `mailbox::bounded(64)` default; per-message `Message<T>` impls |
| Supervision is part of the design | Declarative `RestartPolicy` + `SupervisionStrategy` + `restart_limit(n, window)` |
| No shared locks | Message passing model — same as ractor — discipline-enforced |
| Push-only / no polling | Mailbox is the push channel; no scheduled wakeups by default |
| Actor type IS the public surface | `ActorRef<A>` is statically typed against the actor |

Under direct ractor, the same rules required carve-outs ("framework
markers OK if private", "give State a domain name", "behavior on
State or reducers, not on the marker"). Under Kameo, no carve-outs
— the framework agrees with the discipline.

Migration cost was bounded: persona-mind had ~9 real ractor
actors at the start of the wave; every additional ractor actor
written between then and a future switch would have been written
in the awkward shape that needs unwinding. The cost grows
nonlinearly. Switching now beat switching at 90 actors.

---

## 3 · The naming rule

**Name the type by what it IS or what role it plays — never by
the framework category it falls into.** `Counter` is an actor;
`CounterActor` is `Counter` plus framework-category ceremony.

```rust
// Right
pub struct ClaimNormalizer { … }
pub struct MindRoot { … }
pub struct StoreSupervisor { … }
pub struct Counter { count: i64 }

// Wrong — framework-category suffix
pub struct ClaimNormalizerActor { … }
pub struct MindRootActor { … }
pub struct StoreSupervisorActor { … }
pub struct CounterActor { … }
```

The same rule applies to messages, replies, and consumer surfaces:

| Wrong (framework category) | Right (role / what it IS) |
|---|---|
| `IncMessage`, `IncMsg` | `Inc` |
| `SubmitMessage`, `SubmitRequest` | `Submit` (or `SubmitClaim` if scoped) |
| `SubmitReply` | `SubmitReceipt` |
| `CounterHandle` (defensive wrap of `ActorRef<Counter>`) | `ActorRef<Counter>` directly |

Role-descriptive suffixes earn their place — they describe what
the type DOES, not what category it's in. `Supervisor`,
`Normalizer`, `Resolver`, `Validator`, `Decoder`, `Encoder`,
`Dispatcher`, `Tracker`, `Cache`, `Ledger`, `Store`, `Builder`,
`Factory`. These name the function. `Actor` / `Message` /
`Handler` name the framework category and add ceremony without
meaning.

The historical drift toward `*Actor` / `*Message` suffixes came
from frameworks like ractor where the actor's behavior marker was
a separate ZST from its `State` — the suffix disambiguated. In
Kameo, where `Self` IS the actor, that disambiguation is moot and
the suffix becomes the workspace's "feels too verbose" trap (per
`ESSENCE.md` §"Naming"). Drop from the start.

This rule lands in three places:

- `skills/naming.md` §"Anti-pattern: framework-category suffixes
  on type names" — the cross-language form, with the discriminator
  table.
- `skills/kameo.md` §"Naming actor types" — the actor-specific
  application with worked examples.
- `skills/actor-systems.md` example tables and supervision diagram
  — already updated to follow the rule.

A follow-up bead (filed below) sweeps operator-assistant's
just-landed `*Actor` and `*Message` types in the persona-* runtime
crates. Theirs landed under the prior convention; the cleanup is a
mechanical rename.

---

## 4 · `ActorRef<A>` is the public consumer surface

Kameo's `ActorRef<A>` is statically typed against the actor; the
message types it accepts are guaranteed by `impl Message<T> for A`
at compile time. There is no class of misuse a `*Handle` newtype
prevents — sending the wrong message is a type error at the call
site.

**Export `ActorRef<A>` as the public consumer surface, including
for library users.** Re-export `kameo::actor::ActorRef` from the
crate root if it makes consumer imports cleaner; that is the
limit of the wrapping needed.

The user's reasoning, in their own framing:

> Actors are by design really correct, so it would be hard to
> misuse them. And our libraries are going to start using
> agents — so if our library users want to use the libraries,
> they're going to have to use the handle, they're going to
> have to be able to use it.

Yes. `ActorRef<A>` IS the handle; it's already statically typed;
a defensive `*Handle` wrapper adds nothing the type system isn't
already enforcing.

The narrow case where a wrapper IS appropriate: the crate
genuinely exposes a different abstraction (e.g., a builder that
returns an `ActorRef` after async setup). The wrapper has its own
role-shaped name (`ClaimNormalizerBuilder`), not `*Handle`.

This decision retires the older "every actor pairs with a `*Handle`"
language that lived in `skills/actor-systems.md` and
`skills/rust-discipline.md` from the ractor era. Both updated this
wave.

---

## 5 · Bead trail

This wave was the first end-to-end use of the new active-beads
protocol. Six designer beads filed, six closed. Two follow-ups
filed. One stale ractor-adoption bead retired.

Closed:

- `primary-jfr` — kameo-testing repo created
- `primary-5lm` — Kameo deep research (3 background subagents,
  notes folded into `kameo-testing/notes/findings.md`)
- `primary-585` — exhaustive Kameo test suite (27 passing)
- `primary-95c` — `skills/kameo.md` written
- `primary-s5j` — active-beads section added to
  `skills/autonomous-agent.md`
- `primary-m9u` — `skills/actor-systems.md` and
  `skills/rust-discipline.md` updated to make Kameo the runtime
  default
- `primary-gyg` — `on_panic` Continue test fixed (call-sequence
  bug in mine; designer-assistant/5 surfaced the working pattern)
- `primary-186` — *"Persona daemons adopt ractor"* superseded by
  the Kameo wave

Filed (this report's wave):

- `primary-???` (filed after this report) — sweep `*Actor` /
  `*Message` suffixes across operator-assistant's just-landed
  persona-* migration; rename to role-noun form per
  `skills/kameo.md` §"Naming actor types".

Open from prior follow-ups:

- `primary-jsi` (P3, system-specialist) — `lore/rust/kameo.md`
  as a tool reference (companion to `~/primary/skills/kameo.md`).

---

## 6 · Reports retired

Deleted in the same commit that lands this report:

- `~/primary/reports/designer/102-kameo-deep-dive.md` — research
  that motivated the switch. Substance now in `skills/kameo.md`
  §"Maturity and pinning", §"Module map", and the per-section
  detail; raw research notes preserved at
  `kameo-testing/notes/findings.md`.
- `~/primary/reports/designer/103-kameo-wave-landed.md` — wave
  closing record. Superseded by §1 of this report.

Preserved (load-bearing substance not folded in):

- `~/primary/reports/designer/100-persona-mind-architecture-proposal.md`
  — persona-mind implementation pins (DisplayId mint algorithm,
  concrete sema table key shapes, `CallerIdentityResolver` +
  `EnvelopeBuilder` mechanics, `mind.redb` path with env
  override, subscription contract sketch). Operator-assistant's
  Kameo migration covers the actor topology but not these
  pins — they remain implementation-pending.

---

## See also

- `~/primary/skills/kameo.md` — workspace usage skill (the
  framework reference for this workspace).
- `~/primary/skills/actor-systems.md` — architectural discipline
  (what counts as actor-shape; updated this wave).
- `~/primary/skills/rust-discipline.md` §"Actors: logical units
  with kameo" — Rust style for actor code (updated this wave).
- `~/primary/skills/naming.md` §"Anti-pattern: framework-category
  suffixes on type names" — cross-language form of the naming rule.
- `~/primary/skills/autonomous-agent.md` §"Active beads — check
  first, work them through" — the new session-start protocol that
  surfaced this wave's beads to the next agent every time.
- `/git/github.com/LiGoldragon/kameo-testing` — designer's test
  bed; 27 passing tests across 9 subsystems.
- `/git/github.com/LiGoldragon/kameo-testing-assistant` —
  designer-assistant's complementary test bed.
- `~/primary/reports/designer-assistant/5-kameo-testing-assistant-findings.md`
  — complementary findings (maturity signals, restart-from-args,
  observational link patterns); folded into this skill.
- `~/primary/reports/operator-assistant/100-kameo-persona-actor-migration.md`
  — the parallel runtime migration of persona-* crates.
- `~/primary/reports/operator/103-actor-abstraction-drift-correction.md`
  — the corrective report that preceded this wave; retired
  `persona-actor` / `workspace-actor` as wrapper-crate inventions.
- `~/primary/reports/designer/100-persona-mind-architecture-proposal.md`
  — persona-mind implementation pins (still load-bearing for
  Phase 2 of the persona-mind implementation).
