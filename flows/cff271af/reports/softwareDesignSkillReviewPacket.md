# Software-Design Skill Review Packet

Nine draft passages for psyche ruling. Each entry states the draft text
verbatim, its origin (psyche words or agent inference, clearly labelled),
the exact fork to be ruled on, and the wording that stands if approved.

Draft: `reports/SkillDrafts/softwareDesign/draft.md` v3 (123 lines, 2026-08-21).
Provenance: `reports/SkillDrafts/softwareDesign/provenance.md`.

No edits to draft, provenance, skill files, or psyche files were made.

---

## Choice 1 — "Steps are walks… a service is a step dressed as a thing" as agent formulation

**Draft lines (17–21):**

> Steps are walks across the map, never things on it. Where a proposed
> type names a process instead of a thing — a Resolver, a Controller, a
> Manager — the process is a walk across existing things, and the type
> does not belong on the map.

**Origin:**

The map-before-code principle and the exclusion of process-named types
are psyche-sourced. From `psyche-raw/Vision/worldModelBeforeCode.md`
2026-08-20 (typed):

> "I think training the model to catch themselves before creating a fake
> trait means we have already failed; the model is trying to write code
> before it has a *model of the world*. could we say this is about
> building ontology, anatomy .. a *map* of what we are creating as an
> object/capability-oriented layout?"

The map-of-the-world framing is affirmed there. The specific formulation
"steps are walks across the map" and "a service is a step dressed as a
thing" (the latter appears in the Diseases section as "a step wearing the
clothes of a thing") are agent coinages from the import-resolution world
map exercise; they are not psyche-verbatim. The provenance flags this as
an agent formulation from the approved world map, not a psyche statement.

**The fork:**

Does the "steps are walks" framing capture your position correctly, or
does it introduce a shape you would word differently? The doctrine it
tries to state: a type that names a process (Resolver, Controller,
Manager) does not belong on the map — the process is not a thing, it is
movement across things. The question is whether "walk" is the right word
for that movement, and whether "a service is a step dressed as a thing"
accurately names the anti-pattern in your terms.

**Wording that stands if approved:**

The draft lines stand as written (17–21) and the disease entry "The
service object — a step wearing the clothes of a thing" (line 279) stands.

---

## Choice 2 — "Contents before behavior" as an explicit step

**Draft lines (83–96):**

> ## Types first; contents before behavior
>
> Enumerate the types before asking what anything does. The types are
> the things that exist; turn every logical aspect into a type.
>
> > "we need to think very carefully of what the types are. First,
> > really, because the traits are something that the types implement.
> > We don't look for traits and then think of types for that."
>
> Then list what each type contains, before any behavior. Containment
> is not behavior: a table has entries; it does not do lookups. When
> something is built from two things, the pair is usually a thing
> itself, waiting for its name — an assembly file and a registry make
> a resolved assembly.

**Origin:**

"Types first" is psyche-verbatim from `psyche-raw/Vision/traitsAsCapabilities.md`
2026-08-13 (dictated), quoted in the draft. The sequencing "contents
before behavior" and the "a table has entries; it does not do lookups"
illustration are agent inference. The provenance notes: "the sequencing
is observed in the worked example; no psyche statement in those words."
There is no psyche entry stating "list what each type contains before
any behavior" as a separate step.

**The fork:**

The draft treats contents-before-behavior as an explicit step in the
design sequence, alongside types-first. The psyche stated types first
clearly. The separate injunction to list contents before behavior, and
the "containment is not behavior" gloss, are the agent's inference from
how the import-resolution world map was drawn. Should "contents before
behavior" stand as a named step in the skill, or is it part of what
types-first already carries and does not need its own statement?

**Wording that stands if approved:**

The section heading "Types first; contents before behavior" (line 83)
and the paragraph "Then list what each type contains…" (lines 92–96)
stand. If the living rules it a subset of types-first, the heading
becomes "Types first" and the contents paragraph is removed.

---

## Choice 3 — The placement law's positive form

**Draft lines (105–107):**

> A capability is placed on the type that contains its subject. The
> thing that carries the name is the thing that resolves. The text
> realizes; the real textualizes.

**Origin:**

The psyche's words in `psyche-raw/Vision/traitsAsCapabilities.md`
2026-08-20 (typed) state the law in the negative:

> "if the type needs a 'name' to resove the import, then it's not
> resolvable."

And in `psyche-raw/Vision/traitsAsCapabilities.md` 2026-08-18 (typed):

> "realize isnt implemented by the same type as textualize. if you
> cant find two different types, the implementation is wrong. You
> dont textualize the text, and you dont realize the realized data."

The positive form — "a capability is placed on the type that contains
its subject" — is the agent's interpretation, not a psyche statement.
The provenance flags: "the psyche's words are the negative ('then it's
not resolvable'); positive form is interpretation."

**The fork:**

Should the skill state the placement law affirmatively ("placed on the
type that contains its subject"), or should it stay in the negative form
the psyche used? The positive form is a generalization the agent drew
from the negative case. If it is wrong or too broad, it will misdirect
future design work more than the quoted negative case would.

**Wording that stands if approved:**

Lines 105–107 stand as written. If the living prefers the negative form,
the positive lines are replaced by the quoted fingerprint and the
direction-pair ruling, with no added interpretation.

---

## Choice 4 — The honest boundary + creation exemption

**Draft lines (114–120):**

> Strip the trait wrapper — if a free function serves equally well,
> the trait added nothing. Boundary: parameters that narrow or direct
> an operation the receiver already owns — a query span, a callback,
> an event payload — are legitimate. Creation is exempt: the created
> thing does not exist yet, so its inputs arrive as parameters and are
> consumed into it.

**Origin:**

The costume-trait fingerprint (rejecting trait methods where the subject
is a parameter) comes from the psyche's 2026-08-20 correction, quoted
verbatim in the draft. The boundary reasoning — that certain parameters
(spans, callbacks, payloads) do not trigger the fingerprint — is agent
derivation from the research report `reports/CostumeTraitFingerprint-2026-08-20.md`,
Section 2, "Boundary: legitimate parameters." That report names this
"honest boundary summary (agent interpretation)." The creation exemption
(the created thing does not exist yet) was developed in the
`CreateTraitCrateSearch-2026-08-21.md` search and is also
agent-inferred, not psyche-stated. The provenance flags both as
"research-derived, unruled by the psyche."

**The fork:**

Two sub-questions, which may be ruled together or separately:

(a) Boundary: are parameters that narrow or direct an existing capability
(query spans, callbacks, event payloads) genuinely exempt from the
costume-trait fingerprint, or does the fingerprint apply to any
non-self parameter?

(b) Creation: is the Create trait (a method whose inputs do not exist on
a receiver yet) legitimately exempt from the fingerprint — or does
creation belong to a factory type, making this exemption unnecessary?

**Wording that stands if approved:**

Lines 114–120 stand. If either sub-question is ruled differently, the
boundary sentence and/or the creation sentence are revised to match.

---

## Choice 5 — `rust.write()` in the main example

**Draft lines (165–172):**

```rust
fn main() -> Result<()> {
    let input    = Input::try_from(datom)?;
    let registry = Registry::try_from(input.registry)?;
    let assembly = AssemblyFile::try_from(input.assembly)?;
    let resolved = ResolvedAssembly::try_from((registry, assembly))?;
    let rust     = AssembledRust::try_from(resolved)?;
    rust.write()
}
```

**Origin:**

The chain shape and the type names are sourced to `psyche-raw/Vision/assembly.md`
and `psyche-raw/Vision/mainFunction.md` 2026-08-21/22. The final line
`rust.write()` is a placeholder: the psyche's words established that
`AssembledRust` is assembled whole in memory before anything is written
("if you need to still write it, it hasn't been generated yet" —
mainFunction.md 2026-08-21), but the exact call form — an inherent
method on the type, a Write trait, a separate conversion to OS bytes —
has not been designed. The provenance flags: "`rust.write()`'s exact
form undesigned — flagged (choice 5)."

**The fork:**

The draft uses `rust.write()` as a stand-in for the output step. Should
the skill show this call as written (an inherent method, implying Write
is an action trait with an inherent entry point), show it differently
(e.g., as a TryFrom to bytes + OS write), or acknowledge the step
without committing to a spelling — for instance, a comment instead of a
call? The form matters because it teaches what the output machine looks
like.

**Wording that stands if approved:**

`rust.write()` stands. If the living prefers a different form or a
placeholder comment, the final line is replaced accordingly.

---

## Choice 6 — The earning-properties list for actors

**Draft lines (205–210):**

> An actor is a thing on the map, never a step. It earns its mailbox
> by what it IS: a truly concurrent activity of the world, holding its
> own mutable state, owning its own lifecycle, its own failure domain,
> its own pacing. The traditions converge on these properties from
> independent origins; a thing with none of them is not an actor.

**Origin:**

Each individual property comes from sourced literature in
`reports/ActorSystemBoundaries-2026-08-21.md`, Section 6, with
convergence across Hewitt 1973, Agha 1986, De Koster 2016, Akka, Orleans,
and Armstrong/Erlang. The provenance states: "no surveyed source
assembles them as one list — the assembly is ours." The six properties
in the report are: own mutable state, own lifecycle, own failure domain,
true concurrency in the world, own pacing, and distribution/location
transparency. The draft uses five (omitting distribution/location
transparency), with the note "left out of the draft as not yet
load-bearing for us." The provenance flags: "The boundaries report also
lists a sixth property, distribution / location transparency, left out
of the draft as not yet load-bearing for us."

**The fork:**

The list as assembled (five properties: concurrent activity, mutable
state, lifecycle, failure domain, pacing) is an agent synthesis from
convergent evidence, never stated as a single checklist by any source.
Should it stand as the skill's actor boundary criterion? And should the
sixth property (distribution/location transparency) be included or
remain out?

**Wording that stands if approved:**

Lines 205–210 stand with five properties. If the living adds the sixth,
the sentence becomes: "…its own pacing, its own location across nodes."
If the living prefers fewer or differently named properties, the list is
revised to match.

---

## Choice 7 — The actor-as-machine synthesis

**Draft lines (231–238):**

> Read as a machine, the actor is the three-part shape continued: the
> mailbox and the current state agglomerate; the handler creates the
> next coherent state; replies and effects convert onward. The actor's
> state is a coherent type; the handler is a conversion. An actor
> named for a process — a ResolverActor, a ManagerActor — is the
> service object with a mailbox.

And lines (223–230):

> **The conversion arrows are never actors.** The machine's arrows are
> demand-driven and stateless; they have no lifecycle, no failure
> domain, no pacing. An actor per pipeline stage is code organization
> wearing concurrency. The machine lives inside the actor: the logic
> is a pure state machine — the sans-io school's rule — and the actor
> is its shell at the I/O boundary, where the world is actually
> concurrent: an ingress, a session, a store serving concurrent
> writers.

**Origin:**

The conversion-arrows-never-actors position is sourced from
`reports/ActorSystemBoundaries-2026-08-21.md`, Section 7, which reasons
from the Elixir official documentation and Armstrong. The sans-io
attribution is sourced from the same report, Section 3. The
actor-as-machine-continued framing (mailbox + state = agglomerate step;
handler = coherent step; replies + effects = convert step) is
agent synthesis — "Designer synthesis resolving the map-law tension
(actors persist, but steps are walks)." The provenance flags both
together as choice 7: "unruled by the psyche."

**The fork:**

Two propositions to rule on together or separately:

(a) The conversion arrows are never actors — steps that are pure
conversions (TryFrom, From) do not earn a mailbox. The pure machine
lives inside the actor; the actor is only the I/O shell.

(b) The actor maps onto the three-part machine: mailbox + state
agglomerate; handler creates the next coherent state; replies and
effects convert onward. This is a design frame for how to think about
actors in terms already in the skill, not a sourced claim.

**Wording that stands if approved:**

Lines 223–238 stand. If the living accepts (a) but not (b), the
actor-as-machine paragraph is removed. If neither proposition is ruled,
both are removed and the section retains only the quoted Armstrong and
Elixir sources.

---

## Choice 8 — "Agents translate, never invent"

**Draft lines (253–258):**

> **Supervision is drawn on the map.** Failure domains are map
> artifacts: which things die together and who restarts whom is
> designed with the ontology, before code. The agent evidence is
> one-sided: left to invent, agents produce unsupervised spawns,
> sleep-based synchronization, and happy paths — "crappy OTP by
> default"; handed the supervision shape and the message vocabulary,
> they translate faithfully. Actors are the map law at its sharpest:
> the topology is the design, and code is its translation.

**Origin:**

The supervision-on-the-map principle connects to `psyche-raw/Vision/worldModelBeforeCode.md`
2026-08-20 (the map is the primary design artifact). The agent-behaviour
claims — unsupervised spawns, sleep-based synchronization, happy paths,
"crappy OTP by default" (a direct practitioner quote) — are sourced from
`reports/AgentBuiltActorMachines-2026-08-21.md`, "Recurring failures"
section, which draws on an Elixir Forum practitioner thread (2024–2025).
The positive half — "handed the supervision shape and the message
vocabulary, they translate faithfully" — comes from the same report's
"Recurring strengths: Boilerplate translation" section, which describes
practitioner reports, not witnessed code: "No inspectable actor system
substantially built by AI coding agents was found." The provenance flags:
"the positive half rests on thinner evidence than the negative half."

**The fork:**

The draft makes a symmetrical claim: agents fail left to invent, and
succeed when given the design. The failure half is sourced (multiple
practitioner accounts). The success half is also sourced, but from
practitioner reports about boilerplate translation, not a witnessed
actor system built end-to-end by an agent with a design handed in. Is
the positive half — "they translate faithfully" — strong enough to state
as doctrine, or should the skill state only the negative (and the
implication that design-before-code is the mitigation)?

**Wording that stands if approved:**

Lines 253–258 stand. If the living rules the positive half overstated,
the sentence "handed the supervision shape and the message vocabulary,
they translate faithfully" is removed, leaving: "left to invent, agents
produce unsupervised spawns, sleep-based synchronization, and happy
paths."

---

## Choice 9 — The Input line in main (name and datom carrier undesigned)

**Draft line (166):**

```rust
    let input    = Input::try_from(datom)?;
```

**Origin:**

`psyche-raw/Vision/mainFunction.md` 2026-08-22 quotes the psyche's
correction as "in your main block, you forgot the input, which is a
strictly typed object coming in as datom." — but cff271af's bc05da32
remembering witnessed the transcript: the psyche's actual typed words
are:

> "I dont see the arg input. where is datom coming from?"

(bc05da32 transcript L706; the mainFunction.md sentence is
agent-constructed.) The actual words establish that main's input was
missing and that the input arrives as datom; the "strictly typed
object" phrasing is agent inference from the surrounding exchange. It does not name the type `Input`, and it does not
specify how the datom reaches main (whether `datom` is a variable, a
function call, an OS argument, or something else). The provenance flags:
"`Input`'s name and the datom's carrier (how the datom reaches main)
are undesigned; the line stands as the typed entry of the chain per
mainFunction.md 2026-08-22."

**The fork:**

Two sub-questions:

(a) Is `Input` the right name for the typed object that carries the
datom-realized entry into the chain? The psyche's ruling specifies a
strictly typed object; it does not name it. The interface's root enum
(the type whose variants are the main operations) is the likely referent
— if so, what is that type called?

(b) Is `datom` an acceptable placeholder for the datom's carrier, or
should the line show the actual carrier form (e.g., a macro call, a
function from the entry crate, a raw bytes argument)?

**Wording that stands if approved:**

Line 166 stands as written. If the living names the type or the carrier,
the line is revised accordingly. If both remain undesigned for now, the
line can stay as a placeholder with a comment.

---

## Sources

- `reports/SkillDrafts/softwareDesign/draft.md` — v3, 2026-08-21/22
- `reports/SkillDrafts/softwareDesign/provenance.md` — reading choices 1–9
- `psyche-raw/Vision/worldModelBeforeCode.md` — map-before-code rulings, 2026-08-20/21/22
- `psyche-raw/Vision/traitsAsCapabilities.md` — types-first, placement law, direction pairs, verb names, 2026-08-13/14/18/20/21
- `psyche-raw/Vision/importResolution.md` — placement law fingerprint, 2026-08-20/21
- `psyche-raw/Vision/mainFunction.md` — main chain, Input ruling, AssembledRust name, 2026-08-21/22
- `reports/CostumeTraitFingerprint-2026-08-20.md` — honest boundary derivation (agent interpretation)
- `reports/ActorSystemBoundaries-2026-08-21.md` — earning properties, actor/machine reading, conversion arrows, sans-io, granularity
- `reports/ActorDataflowDesignSkills-2026-08-21.md` — closed message enum, effects as data, eight conventions
- `reports/AgentBuiltActorMachines-2026-08-21.md` — agent failure modes, boilerplate-translation strength, scarcity finding
