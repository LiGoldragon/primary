# Ethos Terminology Research

Flow f426777b, 2026-08-26. Directed by the psyche in
`flows/f426777b/vision/spokenVocabulary.md`:

> So I want you to do some research in, like, ontology, category
> theory, how we model the universe, and how we would model
> this—Ethos specifically [...] So we need to think of better terms
> for our language, for Ethos, for how we talk about everything. And
> we need a more specific way to declare traits.

Everything below is proposal for the psyche's ruling. Nothing is
chosen. Where the evidence forks, the fork is shown. Web findings are
relayed claims from the cited literature; the acoustic assessments
are reasoned predictions, not witnessed tests against the psyche's
actual speech-to-text (a real test would run the candidate words
through that engine — see Open forks).

## Selection criteria

Derived from standing rulings, in order of force:

1. **Spoken-language fitness first.** The vocabulary is dictated
   aloud. "I don't like the word 'trait,' if only because it's a bit
   acoustically ambiguous, maybe—kind of like how the Rust language
   often is mistaken for REST" (f426777b spokenVocabulary
   2026-08-26). Near-homophones with common tech words are flagged
   per candidate.
2. **Terms that come back a lot and stick.** "what kind of terms come
   back a lot and seem to [...] stick with them. And these are the
   ones we want to favor" (aa4c7747 spokenVocabulary 2026-08-24).
   Cross-discipline recurrence is evidence.
3. **Short.** The capability word is spoken constantly ("declare a
   trait", "this trait has three interactions"); syllable count
   matters most for it.
4. **The qualifier reading preserved.** A type carrying the thing is
   capable of something ("the type that the trait qualifies, the
   qualified type" — aa4c7747 2026-08-24; Create: "when something
   has a new method, it means that it can be created" —
   traitsAsCapabilities 2026-08-21).
5. **Elaborate specific terms acceptable when module-qualified.** "we
   don't have to be afraid to use more elaborate terms [...] if we
   fully qualify the name, it's self-describing"
   (traitsAsCapabilities 2026-08-13).
6. **Names must be true of what exists.** "if you need to still write
   it, it hasn't been generated yet" (mainFunction 2026-08-21); the
   Create-over-TryFrom alias was rejected: "If we want TryFrom/From,
   then that's what we'll call it" (aa4c7747 ethosTraitSyntax
   2026-08-25).
7. **Family fit** (observed, not ruled): the existing naming universe
   is Greek — Ethos, Logos, Nomos, Protos, Datom, Sema, Nexus. A
   candidate that joins the family gains coherence; this is a
   tendency in the corpus, not a stated criterion.

Acoustic note on "trait" itself: /treɪt/ sits in a dense phonetic
neighborhood — trade (trade-off), tray, treat, straight; plural
"traits" against "trades" and "trace" (tracing is a major tech word).
The psyche's hedge ("a bit acoustically ambiguous, maybe") is fair:
the risk is real but moderate compared to Rust/REST.

## a. The capability word (replacing "trait")

What the word must do: name the unit under which every behavior
falls; keep the qualifier reading (a type carrying Write is capable
of writing); survive constant dictation; compound cleanly ("X
declaration", "mandatory Xs", "the X qualifies the type"). The
individual names stay infinitive verbs (Write, Read, Resolve, Walk)
regardless — this word is the category word.

### Philosophy-of-powers and formal-ontology family

**Capability** — BFO (Basic Formal Ontology, the most widely adopted
formal upper ontology) makes capability a first-class term: a special
sort of disposition that "can be evaluated on the basis of how well
it is realized" (Merrell et al., "Capabilities"; Arp & Smith,
"Realizable Entities in BFO"). It also anchors capability-based
security ("a capability is a communicable, unforgeable token of
authority" — Dennis & Van Horn, Miller's object-capability model),
Pony's reference capabilities (type qualifiers on an actor
language — the closest existing use to Ethos's), the Sen/Nussbaum
capability approach in philosophy of welfare, enterprise capability
modeling, and robotics. No other candidate comes back this often
across this many disciplines; criterion 2 is maximally satisfied.
Qualifier reading exact. Acoustics: five syllables — long, but
essentially impossible to mishear or mistranscribe. The psyche's own
corpus already leans on it: the standing topic is titled "Traits as
capabilities". Collision risk: "capability" in security means a
held token, not a declared qualification — different enough in
context. The cost is purely length; there is no good short form
("cap" collides with caps/limits).

**Power** — the dispositions-metaphysics term of art (Molnar,
*Powers: A Study in Metaphysics*; Mumford): powers are real
properties of their bearers, directed at their manifestations,
"exercised" when they produce effects. One syllable, qualifier
reading exact ("the type has the power Write"), and the verb that
comes with it is good speech ("exercising a power"). Acoustically
distinct as a word. Collision: heavy semantic overload in tech —
exponent (pow), electrical power, compute power, "powers of two".
Spoken sentences stay parseable ("declare a power", "the powers of
Registration") but the overload is real.

**Disposition** — the exact BFO and metaphysics category: "a
disposition inheres in a material entity and is realized in a
certain kind of process" (Arp & Smith). The realization language
harmonizes uncannily with existing vocabulary (protos::Realize;
flows "realizing" psyche into code) — see the modeling section.
Four syllables; acoustically distinct; near-zero tech collisions.
Fails on connotation: a disposition tends to fire when triggered
(glass disposed to break), where Ethos traits are abilities
exercised on demand. BFO's own answer to that connotation is
precisely its "capability" subtype.

**Affordance** — Gibson: "what the environment offers the animal";
"the action possibilities of the object" (TheoryHub; IxDF
encyclopedia). Sticky in HCI, design, and current robotics/RL. The
relational reading is genuinely apt for a schema language: a trait
is what a type affords the system. Three syllables, no acoustic
collisions. Fails on direction: an affordance is offered to an actor
who acts on the object; Ethos capabilities belong to the type
itself. Also design-jargon flavored.

**Capacity** — Cartwright's term in philosophy of science;
BFO-adjacent. Four syllables, distinct. Collision: capacity planning
(ops), capacitance. Weaker recurrence than capability with the same
length cost; dominated by capability.

### Greek family (joins Ethos, Logos, Nomos, Protos)

**Dynamis** — Aristotle's own word for capacity/potentiality/power,
one half of the dynamis/energeia (potentiality/actuality) pair
(Unlu, "Dynamis and Energeia in Aristotle's Metaphysics"). The
family fit is perfect and the pair would give the effect vocabulary
for free (see d). Acoustic risk is the killer: dictated, "dynamis"
will plausibly transcribe as "dynamics" — one of the most common
words in engineering speech. That is exactly the Rust/REST failure
mode. Flagged as a family-fit dark horse with a probable acoustic
disqualification.

**Hexis** — Aristotle's stable disposition, the acquired condition
between raw capacity and active exercise. Would be the most precise
Greek term for "a capability the type reliably holds". Two hard
collisions: `hexis` is already a component in this system, and one
the psyche distrusts ("we should completly review hexis'
architecture [...] I dont trust that component very much" —
15b67974, 2026-08-21); and spoken "hexis"/"hexes" brushes against
hex (hexadecimal). Effectively blocked unless the component is
renamed first.

**Arete / Virtue** — aretē is the excellence-of-function concept
that pairs with ēthos in Aristotle's ethics; English "virtue" gives
the idiom that literally is the qualifier reading: a type writes *by
virtue of* Write. Virtue's collision is "virtual" (virtual machine,
virtualization) — adjacent in fast speech and STT. Arete is obscure
and will mistranscribe. Register is moralistic for both. Presented
for the family resonance, not expected to win.

### Programming-languages family

The same construct is named trait (Rust, from Self via Schärli et
al.'s "Traits: Composable Units of Behaviour", ECOOP 2003),
typeclass (Haskell), protocol (Swift, Python), concept (C++20),
interface (Go, Java) — one comparative source: Hoekstra, "C++
Concepts vs Rust Traits vs Haskell Typeclasses vs Swift Protocols"
(ACCU 2021). **Protocol** is the strongest of these on stickiness
but collides with wire protocols — fatal in an actor/message system
where "protocol" will be needed for its networking sense.
**Concept** and **interface** dissolve into everyday speech
("the concept of the concept"). **Typeclass** is clunky spoken.
None preserves the qualifier reading better than the philosophy
candidates; the family is documented mainly so the report shows what
was considered and why the discipline's own words lose.

### Plain-English family

**Ability** — the plain word behind every "-able" adjective the
vocabulary already produces (a type is creatable because it has the
ability Create). Three-to-four syllables, zero collisions,
maximally sticky because it is ordinary. Qualifier reading exact.
Its weakness is the same ordinariness: "ability" resists becoming a
term of art, and "an ability declaration" is slightly limp spoken.

**Skill** — blocked internally: skills are already a load-bearing
concept in this workspace (Curriculum skills, agent skills).
**Faculty** — scholastic register fits, but the university sense
intrudes. **Facet** — near-homophone with faucet in some accents,
and names an aspect, not an ability. **Gift/Talent** — granted
rather than declared; whimsical. **Might** — cited only as an
example of total acoustic failure (homophone with the modal verb).

### Ranked shortlist (a)

1. **Capability** — the term that comes back the most across the
   most disciplines (BFO, security, Pony, welfare economics,
   enterprise, robotics), qualifier-exact, unmishearable; costs only
   length, and the psyche's corpus already reaches for it.
2. **Power** — one syllable, dispositions-literature exact, and
   brings "exercise" as its natural verb; pays for brevity with
   semantic overload in engineering speech.
3. **Ability** — collision-free, ordinary, qualifier-exact; risks
   being too plain to hold as a term of art.
4. **Disposition** — formally exact (BFO) and harmonized with the
   existing Realize vocabulary, but connotes triggering over
   deliberate exercise; its BFO subtype "capability" fixes exactly
   that, which argues for 1.
5. **Dynamis** — perfect family fit, probable STT disqualification
   ("dynamics"); worth one witnessed dictation test before
   discarding.

Fork presented honestly: criterion 2 and criterion 4 point at
Capability; criterion 3 points at Power. If constant dictation makes
five syllables intolerable, Power is the best short form; if
unambiguity dominates, Capability. No candidate wins all criteria at
once.

## b. The trait declaration

The thing to name: "a more specific way to declare traits" — the
explicit statement of what a capability is and what interactions it
has, since "I don't think we can just define traits implicitly [...]
it's going to be complex to try to extract what that trait actually
is and how many interactions it has" (f426777b, 2026-08-26).

**Signature** — universal algebra's exact word: a signature Σ
declares the operation symbols and their arities, prior to and
independent of any algebra that implements them (Hyland & Power,
"The Category Theoretic Understanding of Universal Algebra"). The
algebraic-effects literature uses it for exactly the effectful case
("effect signatures" — Pretnar's tutorial), and Standard ML calls a
module's declared interface its signature. Comes back across
mathematical logic, PL theory, and cryptography; sticks. Spoken:
three syllables, distinct; "the Write signature declares two
interactions" parses aloud. Collisions: function signature
(adjacent, arguably harmonious — the declaration is made of
signatures) and cryptographic signature (distant domain). The one
internal wrinkle: if the declaration contains per-interaction
"signatures" in the Rust sense, the word does double duty at two
levels.

**Charter** — a formal document that constitutes a capacity: it
states what its holder is and what its holder may do (ship charters,
city charters, project charters). "The Write charter" reads as the
authoritative declaration of the capability, and chartering carries
empowerment — closer to the qualifier reading than contract's
obligation. Two syllables, acoustically distinct (mild neighbor:
"charger"). Not from the researched disciplines; its strength is
purely English and spoken.

**Contract** — design-by-contract (Meyer/Eiffel), API contracts;
very sticky in engineering speech. But a contract binds parties to
obligations, where the psyche's reading is qualification —
capability, not duty. Also collides with blockchain smart contracts.

**Theory** — the categorically exact word (a Lawvere theory is
presented by operations and equations; implementations are its
models — see modeling). Unusable aloud: "in theory" intrudes on
every sentence.

**Anatomy** — internal-vocabulary continuity candidate: the psyche's
corpus already uses anatomy for a thing's declared structure ("its
basic CLI help emits the Ethos that describes its anatomy" —
Vision/ethos.md). The declaration states the capability's anatomy.
Names the content well, the document less well.

**Canon** ("cannon" homophone), **profile** (profiling), **spec**
(already in use for the program-object: "a spec that is an object" —
mainFunction 2026-08-21), **manifest** (already the assembly-file
concept) — each blocked by collision, three of them internal.

A fork to present rather than hide: possibly no new noun is needed.
The psyche's own sentence was "When I said traits I just meant trait
declaration" (aa4c7747 ethosTraitSyntax 2026-08-24) — if the
capability word from (a) is well chosen, "declaration" may carry the
rest ("the Write declaration"), and the specific work is syntax
design, not naming.

### Ranked shortlist (b)

1. **Signature** — the researched disciplines' own word for exactly
   this artifact (operations declared prior to any implementation),
   sticky and speakable; minor two-level double duty with function
   signatures.
2. **Charter** — best purely-spoken candidate; declaration as
   empowerment, matching the qualifier reading.
3. **(No new noun)** — "declaration" qualified by the (a) word;
   zero vocabulary cost, matches the psyche's own phrasing.
4. **Contract** — stickiest engineering word, wrong emphasis
   (obligation over capability).

## c. "Interaction" — resonance check

Ruled and liked: "Yeah, I think interactions are good, because I
think that describes it well, what it is really conceptually"
(aa4c7747 interactions.md 2026-08-24). The research supports keeping
it, and strengthens it:

- **Physics**: the fundamental forces are the "fundamental
  interactions"; a particle's properties are only ever manifest in
  its interactions. This matches the Ethos rule that an interaction
  always involves the qualified type — a capability is invisible
  except in the interactions of its bearer.
- **Dispositions literature**: manifestation is standardly treated
  as something that happens between reciprocal partners (Martin's
  mutual-manifestation picture; relayed from the literature, not
  separately fetched this session), and McKitrick argues
  manifestations are effects ("Manifestations as effects"). An
  interaction as the manifestation-form of a capability is
  philosophically well-grounded.
- **Recurrence**: HCI, UML interaction diagrams, drug interactions,
  statistical interaction terms — the word comes back everywhere
  and sticks, per criterion 2.

Acoustics: four syllables, distinct; no serious tech near-homophone.
One honest tension: in ordinary English an interaction needs two
parties. The Ethos usage survives because the second party is the
capability's subject matter (the store written, the message sent) —
and the aa4c7747 ruling that an interaction must use the type itself
is exactly what keeps the word honest. No replacement proposed.

## d. The effect operation (Apply audit)

The semantics to name: "when an object is going into the nexus for
an effect to take place [...] we're not really trying to get the
response. We will get a response as an effect of that" — the punch
analogy (fd301d9a-lineage, f426777b nexusTraits.md 2026-08-26).
Standing lean: "I like apply but I'm not certain" (same file).

**Apply — the audit.** Two English senses pull in opposite
directions. The functional-programming sense (apply a function to an
argument) is pure application — precisely the conversion reading
the psyche is escaping; applicatives, Scala/JS `apply` reinforce it.
The operational sense (apply pressure, apply the brakes, apply a
coat of paint, apply a migration, `git apply`, `kubectl apply`) is
exactly right: a declarative object handed to an engine so that
state changes. `kubectl apply` in particular is the industry's
best-known "object enters engine for effect" verb. A further wrinkle
against it: the subject is ambiguous aloud — does the nexus apply
the registration, or is the registration applied to the nexus? Both
parse, and the carrying direction blurs. Apply is viable; its
uncertainty is earned.

**Perform** — the algebraic-effects literature's own verb: a program
performs an operation from an effect signature; the handler enacts
the effect and resumes with the response (Plotkin & Pretnar;
Pretnar's tutorial; Leijen). This is the published formalism whose
shape matches the psyche's distinction exactly (see modeling), and
"the nexus performs the registration" has a clean subject. Two
syllables; collision: performance/perf (moderate, adjacent domain).

**Enact** — to make into act; en-act carries the actor substrate in
its morphology, and laws are enacted — resonant with Nomos. "The
nexus enacts the registration": clean subject, effect-first, the
response nowhere in the name (true to "we're not really trying to
get the response"). Two syllables; near-neighbor "intact" is a mild
risk aloud. Not a term of art in any researched discipline — its
strength is English precision plus family resonance.

**Actuate** — control-systems exact: an actuator is the component
that turns a signal into a physical effect. Three syllables,
essentially collision-free, sticks in robotics. Slightly clinical
aloud.

**Exercise** — the dispositions literature's verb for a power
producing its manifestation (Molnar/Mumford: "powers exercise
themselves"). Pairs naturally if (a) lands on Power. Three
syllables; gym connotation aloud.

**Effect (as verb)** — semantically perfect ("to effect a change")
and acoustically disqualified: affect/effect is the most infamous
homophone pair in English — the exact Rust/REST failure mode.
Flagged so it is seen to have been considered.

**Trigger** — in BFO and dispositions talk, the trigger is the
stimulus that starts the realization. That names the entering
object, not the engine's act — potentially useful for the message
side of the vocabulary, wrong for this slot. **Commit** (git),
**execute** (exec; also "run code", not "receive object for
effect"), **ingest/admit** (name the entry, not the effecting —
and the psyche's point is that the entry is *for* the effect) —
each set aside for the stated reason.

### Ranked shortlist (d)

1. **Perform** — the verb of the one formalism (algebraic effects)
   built on exactly the psyche's distinction; clean spoken subject.
2. **Enact** — effect-first, actor-and-Nomos resonance, response
   absent from the name; weakest on discipline recurrence.
3. **Apply** — keeps the psyche's lean honest: kubectl/migration
   sense is exactly right, FP sense is exactly wrong, subject
   direction blurs aloud; liked, and legitimately uncertain.
4. **Actuate** — collision-free and precise; clinical register.

## e. The trait-typed yield (generic in return position)

The thing to name: a declared result position that is
capability-typed, resolved concrete per carrier — "we would probably
need the object returned to be a [generic], in which case? It's a
trait because in ethos, generics and traits are essentially the same
thing" (nexusTraits 2026-08-26), resting on "the answer is the
mandatory trait! so T would be a trait!" (2026-08-01).

Mechanism kinship first, because it sharpens the naming: Rust's
`-> impl Trait` in a trait is desugared by the compiler to an
anonymous associated type, whose concrete value each implementation
determines (RFC 3425, return-position impl Trait in traits; RFC 1951
calls the construct an opaque type). Rust's own names for this slot
are "opaque type", "associated type", and — in the Fn traits —
`Output`. So the concept the psyche reached is exactly the one Rust
leaves anonymous; Ethos would be naming what Rust cannot spell. A
name that emphasizes *declared openness resolved per bearer* fits;
"opaque" (which emphasizes hiding) does not.

**Yield** — already in the psyche's mouth for exactly this
relation: "a graph of data that can yield the entire program"
(mainFunction 2026-08-21). One syllable. Comes back across
disciplines and sticks: crop yield, chemical yield, bond yield,
yield strength. "The interaction's yield is a Resolve" — the
declared yield, resolved concrete per carrier. Collision: the
`yield` keyword of generators (Python/JS/Rust coroutines) — adjacent
and arguably harmonious (a yielded value), but a real overlap for
readers from those languages. Acoustics: distinct.

**Outcome** — semantically exact for the effect reading: the
response arises as the outcome of the effect, not its purpose. Two
syllables, common, sticky, essentially collision-free. Slightly
managerial register.

**Fruit** — the dispositions image (coming to fruition), one
syllable, acoustically unmistakable, and epistemically apt: you know
a type by its fruits. Register risk: whimsical/biblical; may not
survive serious schema text.

**Output** — Rust's own precedent (`Fn::Output`); safe, plain,
already half-standard; generic to the point of invisibility.

**Consequent** (logic's antecedent/consequent — precise but
stiff aloud), **upshot** (sticky idiom, informal), **echo**
(poetically exact for the punch analogy — what returns from the
impact — but `echo` is among the most-typed shell words),
**recoil/repercussion** (punch-exact, negative), **issue** (GitHub
collision), **product/image** (categorical product, Docker image —
both blocked): considered and set aside as annotated.

### Ranked shortlist (e)

1. **Yield** — the psyche's own verb for the relation, one syllable,
   cross-discipline sticky; generator-keyword overlap is the only
   cost.
2. **Outcome** — names effect-of-the-effect exactly,
   collision-free; blander.
3. **Output** — the Rust-precedented safe choice; invisible as a
   term of art.

## Modeling: how the strong frames carve the world, and where Ethos lands

**Formal ontologies.** BFO divides what exists into continuants
(things that persist — objects, and the qualities and *realizable
entities* that depend on them) and occurrents (processes and
events). A realizable entity — role, disposition, function,
capability — inheres in a bearer and is *realized in a process*
(Arp & Smith). Dispositions are "internally grounded": if the
disposition ceased, its bearer would be physically changed; roles by
contrast are externally grounded in circumstance. DOLCE draws the
same continuant/occurrent line as endurant/perdurant, joined by
*participation* (an endurant is in time by participating in
perdurants). The map writes itself: an Ethos type is a continuant
kind; a trait is a realizable entity — BFO's word is literally
capability — borne by the type; an effectful operation in flight is
the occurrent in which the capability is realized; the entering
object is the trigger; stores are the material bearers whose
qualities the process changes; messages are the information-bearing
participants. Two existing rulings turn out to be formally exact.
The internally-grounded criterion is the psyche's cornerstone
complaint made precise: "if the type needs a 'name' to resove the
import, then it's not resolvable" (traitsAsCapabilities 2026-08-20)
— a capability whose subject must be handed in from outside is
externally grounded, a role wearing a capability's clothes. And the
vocabulary of realization already in use (protos::Realize, flows
realizing psyche into code) is BFO's own realization relation:
capabilities are realized in processes. One caution: "realization"
is therefore doing double duty (psyche-to-code, and
capability-in-process); the report flags the overload rather than
resolving it.

**Category theory and universal algebra.** A category is objects
and arrows; the psyche's "the program is a spec of objects tied by
conversions" (mainFunction 2026-08-21) *is* a diagram — types as
objects, From/TryFrom as arrows, main as a composite arrow. One
level up, Lawvere's functorial semantics (Hyland & Power; nLab)
gives the sharpest available frame for the trait system: a *theory*
is presented by operations and equations; a *model* (or algebra) of
the theory is a structure-preserving interpretation of it. Read in
Ethos: a trait declaration presents a theory; a type's interaction
is a model of that theory in the type. This single identification
grounds three rulings at once. First, explicit declaration: a theory
exists prior to and independently of its models, and cannot be
recovered from any one of them — which is exactly "it's going to be
complex to try to extract what that trait actually is" from
implementations. Second, generic-is-a-trait: to declare a generic
parameter bounded by a trait is to work relative to the theory,
deferring the choice of model; instantiating the generic *is*
choosing the model — so "T would be a trait" is, in this frame, a
theorem rather than a convention. Third, the trait-typed yield (e):
an operation whose result sort is itself only theory-constrained,
resolved when the carrier's model is chosen — what Rust desugars to
an anonymous associated type.

**Effects.** Moggi showed computational effects are uniformly
modeled by monads ("Notions of Computation and Monads"); Plotkin,
Power, and Pretnar refined this into algebraic effects: an effect is
a *signature of operations*; a *handler* interprets those operations
by actually enacting them, and resumes the suspended program's
continuation with the response. This is the psyche's punch
distinction, published: performing an operation is not a conversion
into its response — the handler makes the effect happen, and the
response arrives as the continuation's argument, an effect of the
effect. In Ethos terms the nexus is the handler, the entering object
is a performed operation, the response is the resumption value, and
the pure-conversion arrows (From/TryFrom) stay in the base category,
cleanly separated — which is why the psyche's instinct that TryFrom
"may not be how to think about" processing is the same cut the
literature makes between functions and effects.

**Actors.** Hewitt and Agha's model gives the substrate Ethos takes
for granted: an actor can send messages, create actors, and
designate the behavior for the next message (Garnock-Jones, History
of Actors). "Behavior" is that literature's word for what an actor
does with a message — worth knowing when the (a) word is chosen,
since Ethos capabilities sit one level above actor behaviors: a
behavior is what one actor does; a capability is what a kind of
thing can do.

**The compact map.** Type = continuant kind / object of the
category. Trait = capability (BFO) / presented theory (Lawvere) /
effect signature (Plotkin-Power). Trait declaration = the theory's
presentation: operations with arities and yields. Interaction =
realization profile / model of the theory in the type. Pure
conversion = arrow (From/TryFrom), composed into main. Effect
operation = performed operation against a handler (the nexus);
response = the continuation's value, effect of the effect. Store =
material bearer whose qualities the process changes. Message =
information-bearing participant; the entering object is the
trigger of a realization.

The single most load-bearing insight: **a trait declaration is a
presented theory and each interaction is a model of it** — one
identification that simultaneously grounds explicit declaration
(theories are not recoverable from their models), generic-is-a-trait
(instantiation is model-choice), and the yield position (a
theory-constrained result sort resolved per model); with BFO
supplying the ontological reading of the same structure (capability,
bearer, realized-in-process) and its internally-grounded test
formalizing the "regular functions pretending to be traits"
cornerstone.

## Open forks and untested assumptions

- The acoustic assessments are reasoned, not witnessed. A decisive
  test: dictate the shortlisted words through the psyche's actual
  speech-to-text and read what comes back (especially
  capability/power, dynamis/dynamics, enact/intact, yield).
- Capability vs Power is a genuine criteria conflict (recurrence and
  precision vs brevity); no recommendation is made between them.
- Whether (b) needs a noun at all, or only syntax plus
  "declaration", is left to the ruling.
- "Realization" doing double duty (psyche-to-code; capability-in-
  process) is flagged, not resolved.
- Hexis is blocked only contingently — by the existing distrusted
  component of that name.

## Sources

Psyche records read (quote ground):

- /home/li/primary/flows/f426777b/vision/spokenVocabulary.md
- /home/li/primary/flows/f426777b/vision/nexusTraits.md
- /home/li/primary/flows/aa4c7747/vision/spokenVocabulary.md
- /home/li/primary/flows/aa4c7747/vision/interactions.md
- /home/li/primary/flows/aa4c7747/vision/ethosTraitSyntax.md
- /home/li/primary/psyche-raw/Vision/traitsAsCapabilities.md
- /home/li/primary/psyche-raw/Intent/mandatoryTraits.md
- /home/li/primary/psyche-raw/Vision/genericParametersAreTraits.md
- /home/li/primary/psyche-raw/Vision/mainFunction.md
- /home/li/primary/flows/fd301d9a/vision/nexusTraits.md
- /home/li/primary/flows/15b67974/vision/hexis.md
- /home/li/primary/Vision/ethos.md

Web (found via search this session; relayed as claims):

- Arp & Smith, Realizable Entities in Basic Formal Ontology —
  http://ontology.buffalo.edu/smith/articles/realizables.pdf
- Arp & Smith, Function, Role, and Disposition in Basic Formal
  Ontology — https://philarchive.org/archive/ARPFRA
- Merrell et al., Capabilities (BFO capability paper) —
  https://philarchive.org/archive/MERC-14v2
- Spear, Ceusters & Smith, Functions in Basic Formal Ontology —
  http://ontology.buffalo.edu/smith/articles/Functions-in-BFO.pdf
- Molnar, Powers: A Study in Metaphysics —
  https://philpapers.org/rec/MOLPAS
- McKitrick, Manifestations as Effects —
  https://digitalcommons.unl.edu/cgi/viewcontent.cgi?params=/context/philosfacpub/article/1034/&path_info=McKitrick_MP_2010_Manifestations_as_effects__DC_VERSION.pdf
- NDPR review, The Metaphysics of Powers —
  https://ndpr.nd.edu/reviews/the-metaphysics-of-powers-their-grounding-and-their-manifestations-2/
- Pretnar, An Introduction to Algebraic Effects and Handlers —
  https://www.eff-lang.org/handlers-tutorial.pdf
- Plotkin & Pretnar, Handlers of Algebraic Effects —
  https://link.springer.com/chapter/10.1007/978-3-642-00590-9_7
- Leijen, Algebraic Effects for Functional Programming —
  https://www.microsoft.com/en-us/research/wp-content/uploads/2016/08/algeff-tr-2016-v2.pdf
- Moggi, Notions of Computation and Monads —
  https://dl.acm.org/citation.cfm?id=116984
- Hyland & Power, The Category Theoretic Understanding of Universal
  Algebra: Lawvere Theories and Monads —
  https://www.irif.fr/~mellies/mpri/mpri-ens/articles/hyland-power-lawvere-theories-and-monads.pdf
- nLab, Lawvere theory — https://ncatlab.org/nlab/show/Lawvere+theory
- Wikipedia, Lawvere theory —
  https://en.wikipedia.org/wiki/Lawvere_theory
- Unlu, Dynamis and Energeia in Aristotle's Metaphysics —
  https://philarchive.org/archive/UNLDAE
- Cambridge (Shakespeare and Virtue ch. 2), Dynamis and Energeia —
  https://www.cambridge.org/core/books/abs/shakespeare-and-virtue/dynamis-dynamism-capacity-and-energeia-actuality/C279F345A7C038B8A1C9486C54E61A36
- TheoryHub, Affordances Theory —
  https://open.ncl.ac.uk/theories/22/pdf/affordances-theory/
- IxDF, Affordances (Encyclopedia of HCI) —
  https://ixdf.org/literature/book/the-encyclopedia-of-human-computer-interaction-2nd-ed/affordances
- Schärli, Ducasse, Nierstrasz & Black, Traits: Composable Units of
  Behaviour (ECOOP 2003) —
  https://www.cs.cmu.edu/~aldrich/courses/819/Scha03aTraits.pdf
- Wikipedia, Trait (computer programming) —
  https://en.wikipedia.org/wiki/Trait_(computer_programming)
- Hoekstra, C++ Concepts vs Rust Traits vs Haskell Typeclasses vs
  Swift Protocols (ACCU 2021) —
  https://accu.org/video/spring-2021-day-3/hoekstra/
- Rust RFC 3425, return-position impl Trait in traits —
  https://rust-lang.github.io/rfcs/3425-return-position-impl-trait-in-traits.html
- Rust RFC 1951, expand impl Trait —
  https://rust-lang.github.io/rfcs/1951-expand-impl-trait.html
- Garnock-Jones, History of Actors —
  https://groups.seas.harvard.edu/courses/cs252/2016fa/12.pdf
- Wikipedia, Capability-based security —
  https://en.wikipedia.org/wiki/Capability-based_security
- awesome-ocap (object-capability survey) —
  https://github.com/dckc/awesome-ocap
- Pony tutorial, Reference Capabilities —
  https://tutorial.ponylang.io/reference-capabilities/reference-capabilities.html
- Borgo et al., DOLCE: A Descriptive Ontology for Linguistic and
  Cognitive Engineering — https://arxiv.org/pdf/2308.01597

Relayed from training knowledge, not fetched this session: Martin's
mutual-manifestation / reciprocal-disposition-partners picture;
Norman's perceived-affordance adaptation (corroborated by the IxDF
source); `kubectl apply` and migration-apply usage; the Fn traits'
`Output` associated type.
