# 251 — "supervisor" identity disambiguation

*Investigation into /249 High-severity gap #2. The English word "supervisor"
is doing five distinct semantic jobs across spirit/ARCH, persona/ARCH,
mind/ARCH, signal-persona/ARCH, and persona-terminal/ARCH. Psyche's
authority-graph statement names "the supervisor" but does not specify which
workspace object that is. This report lays out the five meanings, where
they collide, and three resolution paths — and surfaces the choice for
psyche.*

## 0 · TL;DR

The word "supervisor" appears in workspace surfaces with **five distinct
referents**:

1. **The OS-level engine-manager process** (psyche-stated "supervisor" —
   the entity with higher infrastructure permission above spirit).
   Currently named `persona-daemon` in code; called "the supervisor" in
   psyche-statements and in spirit/ARCH's authority mermaid; called
   "engine manager" in persona/ARCH prose.
2. **`EngineSupervisor` Kameo actor** at `persona/src/supervisor.rs` —
   the in-process actor that starts/stops prototype-supervised child
   processes. A subcomponent of meaning #1.
3. **`SupervisionOperation` / `SupervisionReply` / `SupervisionRequest`
   wire vocabulary** in `signal-persona`. The protocol that meaning #1
   uses to talk to each supervised component.
4. **Kameo actor-tree supervisors INSIDE components** —
   `StoreSupervisor`, `SubscriptionSupervisor` in `persona-mind`;
   `IngressPhase` / `StoreSupervisor` / `SubscriptionSupervisor` in
   `persona-spirit`. Generic Kameo terminology for parent actors that
   supervise child actors. Unrelated to authority chain.
5. **`persona-terminal-supervisor` binary** — a transitional binary in
   `persona-terminal` being folded into the single terminal daemon (per
   /249 gap #32). Was the "server" side of the cell+supervisor split.
   Component-internal naming.

Of these, **#1, #2, #3 all refer to the same engine-manager role** with
inconsistent naming. **#4 is the unrelated Kameo convention** sharing the
English word. **#5 is transitional residue.**

The gap is two things conflated:

- **Naming inconsistency** for one thing (the engine-manager role):
  workspace alternates between "the supervisor," "engine manager,"
  "persona-daemon," and `EngineSupervisor` without rule.
- **Word collision** between the engine-manager role and component-
  internal Kameo actor-tree supervisors.

The psyche used the word "supervisor" in their verbatim intent statement
(`intent/persona.nota` 2026-05-18 14:00Z: *"the apex, the most powerful
part, notwithstanding the supervisor, which only has higher permission
because it's an infrastructure component that's there to make sure the
engine is running"*). So the word is load-bearing in psyche language —
it can't simply be deleted; the question is what it names canonically.

## 1 · The five senses, with citations

### Sense 1 — engine-manager role (psyche-stated)

Psyche intent (`intent/persona.nota` 2026-05-18T14:00):

> *"notwithstanding the supervisor, which only has higher permission
> because it's an infrastructure component that's there to make sure the
> engine is running"*

Restated authority chain (`intent/persona.nota` 2026-05-19T15:30Z):

> *"supervisor → spirit → mind → orchestrate → router/harness/terminal"*

This is the entity that:

- Runs as the dedicated `persona` system user.
- Holds higher infrastructure permission than spirit.
- Spawns and stops components.
- Owns sockets at `/var/run/persona/`.
- Holds `owner-signal-*` contracts for components below it.

In code/architecture, this entity is named **inconsistently**:

| Surface | Name used |
|---|---|
| persona/ARCH §0 prose | "engine manager" / "host-level engine manager" |
| persona/ARCH §1.5 heading | "Engine Manager Model" |
| persona/ARCH §"Engine manager" socket | `/var/run/persona/persona.sock` |
| persona/ARCH binary references | `persona-daemon` |
| persona-spirit/ARCH authority mermaid | `persona supervisor` |
| persona-spirit/ARCH owner-contract line 16 | "supervisor-only owner contract" |
| /232 §0 TL;DR line 19 | "The supervisor has higher permission only as infrastructure" |
| persona.nota verbatim | "the supervisor" |

### Sense 2 — `EngineSupervisor` Kameo actor

Inside `persona-daemon`, a specific Kameo actor:

- `persona/src/supervisor.rs` — "Kameo EngineSupervisor actor that
  starts/stops prototype-supervised processes."
- persona/ARCH line 727: "`EngineSupervisor` actor, resolves
  prototype-supervised component commands through [...]"

This is meaning #1's internal implementation. Not a separate authority.

The `signal-persona/ARCH` line 31 mentions a `Supervisor*` prefix being
dropped from rename pass (e.g., `SupervisorActionAcceptance` →
`ActionAcceptance`) — agent-design wanted to drop the redundant prefix.
The signal-persona ARCH §1 still keeps `SupervisionOperation` etc.

### Sense 3 — `SupervisionOperation` wire vocabulary

`signal-persona` ARCH §1:

- `SupervisionOperation` (variants: `Announce` / `Query` / `Stop`).
- `SupervisionReply` (variants: `Ready` / `NotReady` / `Stopped` /
  `HealthReport` / `Unimplemented`).
- Every supervised daemon implements this contract on its supervision
  socket.

This is the wire-level relation between meaning #1 (the engine manager)
and each supervised component. Not a separate authority, but a separate
*name surface* for the relation.

### Sense 4 — component-internal Kameo actor supervisors

Inside each component, Kameo actor trees use parent-supervises-child
patterns. The parent is conventionally named `*Supervisor`:

- `persona-mind/ARCH` §3: `StoreSupervisor`, `SubscriptionSupervisor`,
  `ChoreographyAdjudicator`, `ViewPhase`, etc.
- `persona-spirit/ARCH` §"Actor topology": `IngressPhase`,
  `DispatchPhase`, `StatePlane`, `SubscriptionPlane`, `RecordStore`.
  (Spirit uses `Phase` / `Plane` instead of `Supervisor` for most;
  consistency partial.)
- `skills/actor-systems.md` §"Failure policies": "Each supervisor needs
  a typed failure policy" — generic Kameo terminology.

These are unrelated to authority chain. The word collision is purely
linguistic — same English word, different domain.

### Sense 5 — `persona-terminal-supervisor` binary

`persona-terminal/ARCH` lines 161, 254:

- "`persona-terminal-supervisor` currently binds the engine-facing
  Signal socket [...]"
- "transitional code being folded into the consolidated daemon"

This is a transitional binary in the terminal component. It is the
"server" side of an earlier cell+supervisor split that the consolidation
plan (gap #32 in /249, "Low" severity) is collapsing into one terminal
daemon. Once consolidation lands, this name disappears.

## 2 · Where the meanings collide

**Collision 1 — persona/ARCH internal**: the engine-manager process
is called "engine manager" in section headings (`§1.5 Engine Manager
Model`) but its internal actor is `EngineSupervisor`. A reader does not
know whether "the engine manager" and "the supervisor" are the same
thing or different things until they read enough context to figure out
that the actor is a piece of the process.

**Collision 2 — spirit ARCH vs persona ARCH**: spirit/ARCH calls the
upstream entity "the supervisor" (line 9, line 23 mermaid). persona/ARCH
calls itself "the engine manager." A reader following the authority
chain from spirit upward arrives at a different name than the chain's
own self-description.

**Collision 3 — actor supervisors inside components**: when a section
says "the supervisor restarts" (e.g., persona/ARCH line 602: *"The
supervisor's restart policy then decides..."*), the reader must
disambiguate from context whether this is the OS-level engine manager
restarting child processes, the `EngineSupervisor` actor inside
persona-daemon, OR a component-internal Kameo actor supervisor
restarting child actors.

**Collision 4 — psyche intent vs implementation**: psyche said
"supervisor" with a clear referent (the infrastructure-permission entity
above spirit). The implementation has fragmented that one role across
multiple names. Agents reading psyche intent and agents reading code
look at different vocabularies for the same thing.

**Collision 5 — `SupervisionOperation` as wire vocabulary**: when a
component receives a `SupervisionOperation::Stop`, is "supervision" the
generic Kameo concept (the parent supervising the child) or the
specific engine-manager-to-component relation? Wire context makes it
clear, but the word reuses the same stem.

## 3 · Resolution paths

### Path A — Keep "supervisor" as the authoritative name for sense #1; rename senses #2 + #4

The psyche used "supervisor" — preserve that as the canonical name for
the engine-manager role.

Changes:

- Rename `persona/src/supervisor.rs` to `engine_manager.rs` (or
  `engine.rs`) and the actor inside from `EngineSupervisor` to
  `EngineLauncher`. (persona/ARCH already says "data-bearing Kameo
  launcher/supervisor actor" — choose `Launcher`.)
- Persona/ARCH replaces "engine manager" with "the supervisor" or
  "the persona supervisor" in role descriptions, keeps
  `persona-daemon` as the binary name.
- Component-internal actor supervisors (`StoreSupervisor`,
  `SubscriptionSupervisor`) rename to `*Root` or `*Coordinator` per
  Kameo's parent-actor convention (multiple options; not super
  important; the point is dropping the word "supervisor").
- `SupervisionOperation` keeps — it IS the supervisor talking to its
  children, no ambiguity once internal `Supervisor`-type actors are
  renamed.
- `persona-terminal-supervisor` disappears with consolidation
  (independent).

Tradeoffs:

- Closest to psyche language. Word "supervisor" maps 1:1 to the role
  psyche named.
- Forces renaming agent-named code (`EngineSupervisor`,
  `StoreSupervisor`, `SubscriptionSupervisor`).
- The actor-tree convention loses its conventional name; some Kameo
  literature uses "supervisor," so this breaks that link. But Kameo
  doesn't *require* the name; it's just a convention.

### Path B — Drop "supervisor" entirely for sense #1; canonicalize "engine manager"

The persona/ARCH text already uses "engine manager" / "persona-daemon"
extensively. Treat that as the official name; relegate "supervisor" to
actor-tree convention only.

Changes:

- Edit `intent/persona.nota` to add a Clarification record: "supervisor
  in psyche intent statements means the engine manager
  (persona-daemon); the word is the role description, not the
  workspace name."
- Persona-spirit/ARCH mermaid: `supervisor["persona supervisor"]` →
  `manager["persona engine manager"]` or `daemon["persona-daemon"]`.
- Persona-spirit/ARCH line 9: "The supervisor has higher
  infrastructure permission only" → "The engine manager has higher
  infrastructure permission only."
- /232 §0: "The supervisor has higher permission only as
  infrastructure" → "The engine manager has higher permission only
  as infrastructure."
- `SupervisionOperation` etc. could optionally rename to
  `EngineManagementOperation` for full consistency, but this is
  larger churn and `SupervisionOperation` is contextually clear
  even with the rename.
- Component-internal `*Supervisor` actors keep their names — Kameo
  convention, scoped by namespace.

Tradeoffs:

- Diverges from psyche's literal word but preserves the meaning.
- "Engine manager" is more descriptive than "supervisor" — names the
  actual responsibility.
- "Supervisor" can then mean only the Kameo actor-tree convention
  with no overload.
- Requires editing psyche-verbatim references — the intent log keeps
  the verbatim quote but the agent restatement clarifies "supervisor"
  = "engine manager."

### Path C — Stratify by namespace; keep all current names

Accept that "supervisor" is a context-dependent English word and rely on
namespace/section context to disambiguate.

Changes:

- No renames.
- Add a glossary section to persona/ARCH and ESSENCE/INTENT defining
  the five senses and where each applies.
- New ARCH files MUST IMPLEMENT a "Glossary" note at the top
  whenever using "supervisor" so readers know which sense.

Tradeoffs:

- Cheapest. Lowest churn.
- Trades resolution for vigilance. Future agents still need to read
  context to disambiguate.
- Workspace `ESSENCE.md` "Beauty is the criterion" leans against
  this — beauty says find a structure that makes the ambiguity
  dissolve, not document around it.

## 4 · Recommendation (designer view)

**Path A** is the closest match to psyche language. The psyche named
"supervisor" with a clear role; preserving the word as canonical honors
that. The cost is renaming agent-named code (`EngineSupervisor`,
`StoreSupervisor`, `SubscriptionSupervisor`) — substantial but bounded.
Persona/ARCH already documents the rename pattern (`Supervisor*` prefix
drop in `signal-persona/ARCH` §31).

**Path B** is the most descriptive of the actual responsibility. "Engine
manager" tells a reader what the entity does. The cost is diverging
slightly from psyche's literal word — but the intent log's *verbatim
quote* stays; only the agent restatement clarifies the mapping.

**Path C** is rejected — it accepts the ambiguity that the gap analysis
flagged. ESSENCE's "beauty" criterion (special cases dissolve into the
normal case) leans against a glossary patch.

Between A and B, designer lean is **Path A** (preserve psyche
vocabulary) — the psyche's word is load-bearing in intent records and
agent restatement should track psyche language, not invent its own.

But this is a psyche call. Either path resolves the ambiguity cleanly;
neither is structurally worse than the other; the choice is about which
vocabulary the workspace canonicalizes.

## 5 · Questions for psyche

1. **Path A vs B**: do you want "the supervisor" or "the engine
   manager" as the official workspace name for the OS-level entity
   above spirit?

   Path A keeps your word "supervisor" canonical; Path B canonicalizes
   "engine manager" and treats "supervisor" as your role-description
   word in intent statements.

2. **`SupervisionOperation` wire name** — if Path B, do you want to
   rename it to `EngineManagementOperation` (full consistency, larger
   churn) or keep it (`SupervisionOperation` reads cleanly in context
   even after the role renames)?

   Designer recommendation: keep `SupervisionOperation` regardless of
   path. The wire vocabulary names the *relation*; the relation IS
   one of supervision (parent watches child), and the wire context
   makes it clear which supervision.

3. **Component-internal actor supervisors** — do you have a
   preference between `*Supervisor` (Kameo convention) and `*Root` /
   `*Coordinator` / `*Parent` for renaming, if Path A is chosen?

   Designer recommendation: `*Root` for the top of an actor tree
   inside a component (`StoreRoot`, `SubscriptionRoot`). Already
   used in persona-spirit (`SpiritRoot`).

## 6 · Implementation scope (whichever path)

Once psyche picks:

**Path A scope** (~12 files):

- `persona/src/supervisor.rs` → `engine_launcher.rs`; `EngineSupervisor`
  type → `EngineLauncher`.
- `persona/ARCH` — global rename of "engine manager" prose to "the
  supervisor" / "persona supervisor" where role is meant; keep
  "persona-daemon" as the binary name.
- `persona-mind/ARCH` — `StoreSupervisor` → `StoreRoot`,
  `SubscriptionSupervisor` → `SubscriptionRoot`.
- `persona-mind/src/actors/*.rs` — same renames in code.
- `intent/persona.nota` — no edits (psyche's verbatim quotes stay;
  this path matches them).
- `skills/component-triad.md` — no edits if it doesn't reference
  these names directly (quick verification needed).

**Path B scope** (~8 files + intent record):

- `intent/persona.nota` — add Clarification record explaining
  "supervisor" in verbatim quotes = "engine manager" in canonical
  vocabulary.
- `persona-spirit/ARCH` — mermaid + line 9 prose: "supervisor" →
  "engine manager" or "persona-daemon."
- `reports/designer/232-persona-spirit-new-component.md` — §0 TL;DR
  line: "supervisor" → "engine manager." (Already in keep list.)
- `persona/ARCH` — make "engine manager" everywhere consistent;
  optionally rename `EngineSupervisor` actor to `EngineLauncher`
  (decoupled choice).
- Component-internal `*Supervisor` names stay.
- `SupervisionOperation` stays.

Both paths leave `persona-terminal-supervisor` alone — its phase-out
is the cell+supervisor consolidation gap (/249 #32) and is independent.

## 7 · References

- `/249` §"OS-level supervisor identity vs cognitive supervisor"
  (lines 196–202) and gap #2 (line 1129) — gap surface.
- `/232` §0 TL;DR (line 19) and §1 (line 41 quote) — spirit's
  authority-graph framing.
- `intent/persona.nota` 2026-05-18T14:00, 2026-05-19T15:30Z —
  psyche-stated authority chain and apex.
- `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md` —
  engine-manager prose, `EngineSupervisor` actor references
  (especially §1.5, line 727, line 1497).
- `/git/github.com/LiGoldragon/persona-spirit/ARCHITECTURE.md`
  §"Authority" — uses "supervisor" in mermaid + prose.
- `/git/github.com/LiGoldragon/persona-mind/ARCHITECTURE.md` §3 —
  `StoreSupervisor` / `SubscriptionSupervisor` actor tree.
- `/git/github.com/LiGoldragon/signal-persona/ARCHITECTURE.md` §1,
  §"Type renames" — `SupervisionOperation` vocabulary; `Supervisor*`
  prefix-drop precedent.
- `/git/github.com/LiGoldragon/persona-terminal/ARCHITECTURE.md` —
  `persona-terminal-supervisor` (transitional, /249 #32).
- `skills/actor-systems.md` §"Failure policies" — Kameo
  parent-supervises-child convention.

This report retires when psyche picks a path and the named edits land.
