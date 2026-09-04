# Psyche gathering — the topics 6329f1 touches

Flow b9a334, subflow report, 2026-09-04. Written for a later subflow
to turn into a web report for the living. The living's words are
carried verbatim throughout; each quote carries its path, its entry
heading, its date, and its provenance line as the record carries it.

How to read the marks. **Witnessed** means this subflow read the file
or ran the command itself. **Relayed** means a read subagent of this
subflow read it and this subflow carries its report; where a relayed
fact mattered, this subflow re-read the file and the mark says
witnessed. **Inference (mine)** marks a conclusion this subflow drew.
**Distilled** on a raw record means Vision/sources/<topic>.md names
that flow and entry; **undistilled** means it does not.

Provenance lines are carried as the record writes them; older records
write "— psyche, <date> (<session>), typed", newer ones "-- psyche,
typed." or "-- psyche, STT." Archived records open with an "Archived
on landing" line; notions are in a flow's notion/ directory and are
marked as notions.

---

## 1. Core topics

### 1.1 Protos

#### Distilled state

**Vision/protos.md** (witnessed whole, 95 lines). Sections: What
Protos is; What Protos knows; Direction; Structure; Delineation;
Layers; Multi-pass; Canonical print. The file itself names no landing
flow. Its git history (witnessed): replaced whole by 6329f1's landing
commit 23aaf7a7f on 2026-09-04 17:14:39 +0200 ("Land the living's
corrected vision: Protos layers and the Ethos Declaration"); before
that, 10a2eb054 on 2026-08-27 by flow 04db2fd2 ("Vision/protos.md —
direction"). The 6329f1 archive headers say which sections the flow's
records went to: archive-protos.md → Direction, Structure,
Delineation, Layers; archive-vocabulary.md → Direction, Layers.

**Vision/sources/protos.md** (witnessed whole, 26 entries): a5587095
protosIsTheSharedStyle; ba906ae2 protosIsTheSharedStyle; ba906ae2
encodedFormIsTheCode; e4a40e protos; 04db2fd2 anatomy, multiPass,
portion, delimiters; e8c4cc61 protos, prospective, kinds; 62022e8f
kinds, layers, concept, passes, vocabulary; 2ef42163 kinds; b675f3d9
structuralParsing, kinds; 1c282d protosizable, vocabulary; ad19b1
ethos; 6329f1 protos, vocabulary.

**Intent/protosParsing.md** (relayed): approved 2026-08-13 in session
a5587095; protos parsing is context-driven, met shapes announce types
whose contexts take over until completion; reading and writing are
one walk in two directions; carries an annotation that "two-way
structural transcoding" is dead vocabulary.

The landed text on the map question, witnessed, Vision/protos.md
lines 44–48:

```
    44	An enclosed structure stands between its delimiters. Six delimiter
    45	pairs in all: four structural — braces, brackets, guillemets, angle
    46	brackets — and two opaque — curly quotes, where every glyph inside
    47	is content, and parentheses, read by balance. Angle brackets are a
    48	real protos delimiter. A bare structure has no delimiters.
```

That is the only line in Vision/protos.md naming guillemets; the file
does not use the « » glyphs and does not carry the word "map"
(witnessed by grep).

#### Raw records, oldest first

All protos records below were read by the protos-gathering subagent
(relayed) unless marked witnessed.

**flows/a5587095/vision/protosIsTheSharedStyle.md** — not archived.
Distilled (a5587095 protosIsTheSharedStyle). Twelve entries dated
2026-08-11 through 2026-08-13, all in Designer session a5587095.
Those bearing on the layers, structure, delineation, delimiters, or
multi-pass:

> ## 2026-08-11 — the definition; context-switching parse; the protos engine
>
> > remember; once we open the Meaning delimiter (that what were
> > calling it), all the delimiters and structured parsing spectrum is
> > available, until that closing delimiter comes in and changes the
> > parser's context; that is how all our languages parse and why we
> > can design so freely. This is important and is the part of the
> > code which can be shared between all parsers (should be in protos;
> > protos is the name we give to the style which all our dialects
> > share; hence why the final fully-decomposed engine with 3 daemons
> > is the protos engine, with datom sort of sitting besides it, as it
> > is only for pure, typed data)
>
> — psyche, 2026-08-11T19:44+02:00, typed.

> ## 2026-08-11 — there is always a parsing context; it changes, never suspends; always use trait
>
> > no, there is always a parsing context. it doesnt suspend, it
> > *changes*, but the underlying mechanism is always the same; Now,
> > we are parsing in context X and can therefore expect A, B or C
> > shapes of things, and Z would end that context, but meeting A
> > would switch to the context which A entails. That has been the
> > ruling principle of NOTA (datoms's ancestor) from day one. I want
> > to extend it now to say it should always use trait.
>
> — psyche, 2026-08-11T19:53+02:00, typed.

> ## 2026-08-12 — recursion keeps the parent's position; logic planes
>
> > because of recursion, the position of the parent context still
> > needs to be kept, so that returning to the parent context resumes
> > at the following position.
>
> > Your read impl for ShapeDefined seem to want to implement
> > parsing. I dont know if thats where we want to put that logic. We
> > might want to just get the type, and let that type implement its
> > parsing context. Big implementations are a sign of a missing
> > logic plane. Everything should be simple individually. The
> > complexity is in the totality, not the individual parts.
>
> — psyche, 2026-08-12T21:23+02:00, typed.

> ## 2026-08-13 — no traits is no good
>
> > I only looked at the code. I need to see the traits. No traits
> > is no good
>
> — psyche, 2026-08-13T00:29+02:00, typed.

**flows/ba906ae2/vision/protosIsTheSharedStyle.md** — not archived.
Distilled (ba906ae2 protosIsTheSharedStyle). One entry:

> ## 2026-08-14 — datom is a protos dialect, not part of the rust-generation engine
>
> > because datom doesnt take part in the multi pass engine which
> > ethos->nomos->logos->rust is slated to become. but youre right;
> > beside sounds like its not a protos dialect. it *is* a protos
> > dialect, but not part of the future ethos/nomos/logos
> > rust-generation engine
>
> — psyche, 2026-08-14T10:09+02:00 (Designer session ba906ae2), typed.

**flows/2b34fafa/vision/protosIsTheSharedStyle.md** — not archived.
Undistilled (not in sources/protos.md). One entry:

> ## 2026-08-18 — define the block: start with the text source code; every logical aspect a type; ontology of source code
>
> > "we need to define the block. start with the text source code. turn
> > every logical aspect into a type. ontology of source code"
>
> — psyche, typed (Design session 2b34fafa, 2026-08-18).

**flows/04db2fd2/vision/anatomy.md** — distilled (04db2fd2 anatomy).
Protos anatomy as structural recognition. Relayed; not quoted here
since it is carried in Vision/protos.md's "What Protos knows".

**flows/04db2fd2/vision/multiPass.md** — distilled (04db2fd2
multiPass). Multiple passes over single pass. Relayed; carried in
Vision/protos.md's "Multi-pass".

**flows/04db2fd2/vision/portion.md** — distilled (04db2fd2 portion).
Portion as the unit of text; superseded by "structure" (1c282d) and
"Protoform" (1c282d). Relayed.

**flows/04db2fd2/vision/delimiters.md** — distilled (04db2fd2
delimiters). Delimiter pairs; includes a correction on the guillemet
glyph: "this is false; you are talking about guillements, and what you
showed is a double angle bracket pair." Relayed.

**flows/04db2fd2/vision/delineate.md** — not archived. Undistilled.
Relayed; delineation as the structural survey of text.

**flows/04db2fd2/vision/text.md** — not archived. Distilled (04db2fd2
text, in sources/datom.md). Relayed; on Text as a type over String
with normalization.

**flows/04db2fd2/vision/textualTypes.md** — not archived. Distilled
(04db2fd2 textualTypes, in sources/datom.md). Four entries; quoted in
the datom section (1.3).

**flows/04db2fd2/vision/directionAsymmetry.md** — not archived.
Distilled in sources/datom.md (04db2fd2 directionAsymmetry) but not in
sources/protos.md, though Vision/protos.md's Direction carries it.
Quoted in the datom section (1.3):

> ## Approved for distilled vision: in is a prospective datom untrusted until matched; out is a datom
>
> > exactly. this can go straight into distilled vision
>
> -- psyche, typed.

**flows/04db2fd2/vision/decomposable.md** — not archived. Undistilled.
Relayed; a notion about decomposable types.

**flows/04db2fd2/vision/kinds.md** — not archived. Distilled (04db2fd2
kinds in sources/protos.md and sources/ethos.md). Quoted in the ethos
section (1.2).

**flows/e8c4cc61/vision/protos.md** — not archived. Distilled
(e8c4cc61 protos). Two entries:

> ## Structure is a better Portion
>
> > your Structure is a better Portion (better name anyway)
>
> -- psyche, typed.

> ## Delineatable is better expressed as Structural
>
> > and Delineatable is better expressed as Structural.
>
> -- psyche, typed.

**flows/62022e8f/vision/kinds.md** (protos-bearing entries) — not
archived. Distilled (62022e8f kinds, layers, concept, passes in
sources/protos.md). Quoted in full in the ethos section (1.2); the
entries bearing directly on protos layers and vocabulary:

> ## Potential and actualize, universally, layer to layer; Embodied is the bound; Corporal is kept for the layer
>
> > One, I prefer the terminology potential and actualized over
> > Prospective [STT: perspective] and prospect. And that is the kind
> > that I want to use universally to go from one layer to the next.
> > ... And I think the embodied is probably better because then we keep
> > the corporal for... And this answers your third question. We keep
> > corporal for the layer concept.
>
> -- psyche, STT.

> ## The layer capabilities sit on the layer above
>
> > So, yeah, the structural kind, like the structural capability, if
> > we want to say that, or the capability, the structure capability
> > would be on text and the conceive capability would be on structure
> > and the incorporate capability would be on concept.
>
> -- psyche, STT.

> ## Datomizable narrows too explicitly to datom: protoform
>
> > Maybe there's like an actual word here that like is proto, maybe
> > it's a prototype or proto form. It's kind of cool sounding actually.
>
> -- psyche, STT.

**flows/b675f3d9/vision/kinds.md** (protos-bearing entries) — not
archived. Distilled (b675f3d9 kinds, structuralParsing). Quoted in
the ethos section (1.2).

**flows/2ef42163/vision/kinds.md** (protos-bearing entries) — not
archived. Distilled (2ef42163 kinds). The embody ruling and the text
vs textual debate; quoted in the ethos section (1.2).

**flows/1c282d/vision/protosizable.md** — not archived. Distilled
(1c282d protosizable). Witnessed:

> ## The form is protos; the kind is Protosizable
>
> > ethos isnt datom-expressible. the form is protos. I think protosic
> > is the right kind. `type.protosize() -> protoform` - does that
> > make sense. flesh the fuck out of that for me, with the ethos spec
> > of it all and ascii visuals
>
> > protosizable!
>
> — psyche, typed.

> ## The association: Concept bears Protosizable
>
> > ethos:Concept.[ Protosizable]
>
> — psyche, typed.

> ## Structure is really Protoform
>
> > looks like Structure is really Protoform.
>
> — psyche, typed.

**flows/db97561c/vision/prospective.md** — not archived. Undistilled
(not in sources/protos.md). Witnessed. Four typed entries on the
Prospective kind, later superseded by "potential" (1c282d, 6329f1):

> ## Prospective<Embodied> is a kind
>
> > I see Prospective<Embodied> as a kind. do you?
>
> -- psyche, typed.

> ## Prospective<Protos> comes first; Protos is a type
>
> > `Prospective<Protos>` is needed first. Protos is a type which
> > contains the portions and their protosic anatomy
>
> -- psyche, typed.

**flows/e4a40e/vision/protos.md** — not archived. Distilled (e4a40e
protos). Quoted in 1.1's distilled-state section.

**flows/6329f1/vision/archive-protos.md** — archived (distilled into
Vision/protos.md (Direction, Structure, Delineation, Layers), flow
6329f1, 2026-09-04). Distilled (6329f1 protos). Witnessed. Five STT
entries:

> ## 2026-09-04 — the maximal run part is not understood; take it out
>
> > I don't understand this maximal run part. I think just take it out
> > unless there's something there that is valid that you failed to
> > express properly.
>
> -- psyche, STT.

> ## 2026-09-04 — text and concept are protosizable; corporal and protoform are conceivable; both ways for the middle layers
>
> > Well, it seems to me that both the text and the concept are
> > protosizable, just like the corpus [STT: corporal] and the
> > protoform are conceivable. For the middle layers, both the type
> > above and below can be changed into that type because we can go
> > both ways.
>
> -- psyche, STT.

> ## 2026-09-04 — realizing becomes incorporating, since the layer is corporal; incorporate on text daisy-chains
>
> > I also think that, to be consistent, since we're saying that to
> > texturize [STT: textualize] is to go to the text layer, we should
> > also say that we should change "realizing" to "incorporating"
> > because the layer is called the corpus [STT: corporal].
> >
> > Essentially, the text could be corporal, right? Calling
> > "incorporate" on the text would essentially just daisy-chain
> > through "protosize," and then it would conceive, and then it would
> > incorporate the concept.
>
> -- psyche, STT.

> ## 2026-09-04 — actualize on a potential yields its target; is a layer missing
>
> > When you say "actualize on a potential is delineate," that is not
> > true because potential is wet [STT: unclear], right? A potential
> > peritaform [STT: Protoform] that is actualized yields a peritaform
> > [STT: Protoform], and I'm not sure where the delineate here is
> > actually going to fit, unless you think there's a layer between
> > text and perdaform [STT: Protoform], which is wet [STT: unclear],
> > delineated text. Are we missing a layer here?
>
> -- psyche, STT. (Asked as a question; answered "no layer. your answer
> is good" in e996e8 protos.)

> ## 2026-09-04 — drop Embodied; stick with Sized
>
> > I think I want to drop "embodied" and just stick with the rest:
> > "sized," because, first of all, it's not that much better than
> > "sized" cognitively, and it seems to have confused you because that
> > sentence is actually quite fuzzy and confusing.
>
> -- psyche, STT. Supersedes the earlier Embodied rulings on this
> specific question of the bound.

**flows/e996e8/vision/protos.md** — not archived. Undistilled.
Witnessed. Three entries dated 2026-09-04, all post-landing:

> ## 2026-09-04 — no layer between Text and Protoform; the flow's answer stands
>
> > no layer. your answer is good
>
> -- psyche, typed.

> ## 2026-09-04 — Incorporable could replace Corporal; is corporate a word?
>
> > Incorporable could replace Corporal. Is corporate a word?
> > Corporal/corporate Incorporable/incorporate ?
>
> -- psyche, typed. (Asked as a question.)

> ## 2026-09-04 — the key-value map delimiters are abandoned everywhere
>
> > You might want to check out recent flows. I've been talking about
> > these topics and [STT: in] other flows, and we've abandoned the key
> > value map limiters [STT: delimiters] everywhere. We're sort of
> > stripping some stuff out now, and now I'm dropping the version.
>
> -- psyche, STT.

### 1.2 Ethos

#### Distilled state

**Vision/ethos.md** (witnessed whole, 285 lines). Sections: What Ethos
is; Why Ethos; Generation; Non-repetition; Self-description; Horizon
(these six landed by flow 68512643, commit c2a0223b6, 2026-08-24);
Kind; Naming; Identity (landed by flow ad19b1, commit c2ac4cdb2,
2026-09-04 01:58:51 +0200, which also folded Vision/kinds.md into
ethos); Declaration with subsections File, Imports, Types, Kinds,
Associations, Spacing (appended by flow 6329f1, commit 23aaf7a7f,
2026-09-04 17:14:39 +0200). Landing flows and dates are from git
history, witnessed; the file itself names none.

**Vision/sources/ethos.md** (witnessed whole, 34 entries): 01a02a34
ethos, schemaSyntax; vision-raw ethosDotosDivisionAndHelp,
ethosNonRepetitionLaw; f426777b spokenVocabulary; b675f3d9 kinds;
6863ef19, 06196cc7, 2b34fafa traitsAsCapabilities; 04db2fd2 kinds;
5abf3be8 encodedFormFingerprintTraitDesign; 4decf7 kinds; 2ef42163
ethos; e8c4cc61 kinds; b675f3d9 structuralParsing; ac1e9ec8
datomSyntax; e4a40e kinds; ad19b1 kinds; e8c4cc61 ethosFileAnatomy,
kinds; 995a164e ethosTypes; 62022e8f ethosTypes; aa4c7747
interactions, tuples, ethosTraitSyntax; 2b34fafa ethosSourceFiles,
ethosNamespaces; b675f3d9 kinds, structuralParsing; ad19b1 ethos,
designPractice; 6329f1 ethos.

**Vision/ethosMonolith.md** exists with its own sources file; not
read for this report beyond its listing.

**Intent/mandatoryTraits.md** (relayed): approved 2026-08-13, session
d2bb5f5f; every method call lives under a trait; traits are the
comprehension surface; Rust is the new assembly.

The landed Declaration on the map question, witnessed, Vision/ethos.md:

```
   153	A struct is a headed brace — the name, a dot, and braces holding its
   154	positions in order. An enum is a headed bracket — the name, a dot,
   155	and brackets holding its variants. An alias is a headed bare — the
   156	name, a dot, and the aliased type. A map is a headed guillemet — the
   157	name, a dot, and guillemets holding the key type and the value type.
```
```
   162	[ Record.{ Text Integer }
   163	  Report.{ Text Vector<Integer> }
   164	  SinkError.[ Closed Full ]
   165	  LockId.Integer
   166	  Roles.« Text Integer » ]
```
```
   174	pub type Roles = std::collections::BTreeMap<protos::Text, protos::Integer>;
```
```
   234	A complex kind opens with a brace after the dot. Inside: superkinds
   235	in a bracket, associated types with their constraints in a bracket,
   236	associated constants in a guillemet — upper case, in the map
   237	delimiter — and capabilities in a bracket.
```
```
   239	[ Streamable.{ [ Fillable ]
   240	               [ Item<Serializable> ]
   241	               « CAPACITY Integer »
   242	               [ next![ Option<Item> ] ] } ]
```
```
   248	    const CAPACITY: protos::Integer;
```

The Identity section (ad19b1's landing) carries no guillemet and no
map; its example uses angle brackets for constraints (witnessed by
grep: the only map/guillemet hits in Vision/ethos.md are lines 156,
157, 167, 174, 236, 242).

#### Raw records, oldest first

All ethos records below were read by the ethos-gathering subagent
(relayed) unless marked witnessed.

**flows/01a02a34/vision/archive-ethos.md** — archived ("Archived
2026-08-23 by flow 68512643; distilled into Vision/ethos.md and
Vision/ethosMonolith.md"). Distilled (01a02a34 ethos, schemaSyntax).
Two typed entries:

> ## 2026-08-22 — schema, like, which is basically what Ethos is. It's a schema language.
>
> > schema, like, which is basically what Ethos is. It's a schema language.
>
> — psyche, 2026-08-22T17:32:33.328Z, typed.

> ## 2026-08-22 — It would also be great if we can use ethos instead of schema
>
> > It would also be great if we can use ethos instead of schema but ethos-monolith might not be ready to use.
>
> — psyche, 2026-08-22T21:43:29.015Z, typed.

**flows/aa4c7747/vision/ethos.md** — not archived. Distilled (aa4c7747
ethos, as part of the ethosMonolith sources). One STT entry:

> ## 2026-08-24 — the biggest short-term gain: mental model and code in one swoop
>
> > ethos is essentially meant to give us, for now anyway, the entry or
> > the biggest gain short-term is to give us a language that allows us
> > to, in one swoop, write down our mental model of the machine and
> > write code so that we don't get this problem where the code and the
> > ideas for the code, well, we have psyche for that, but psyche is
> > sort of one step back from the actual hard implementation.

**flows/aa4c7747/vision/ethosTraitSyntax.md** — not archived. Distilled
(aa4c7747 ethosTraitSyntax). Five entries; the two bearing on the
Declaration:

> ## 2026-08-24 — traits meant trait declaration; implementation syntax is not MVP
>
> > When I said traits I just meant trait declaration. Implementation
> > would be a big job; it would mean developping the syntax for full
> > function bodies, and the rust generation - thats not MVP sounding
> > anymore.
>
> -- psyche, typed.

> ## 2026-08-25 — the trait implementation checking mechanism is approved
>
> > I approve your trait implementation checking mechanism.
>
> -- psyche, typed.

**flows/aa4c7747/vision/interactions.md** — not archived. Distilled
(aa4c7747 interactions). Two entries:

> ## 2026-08-24 — interactions is the term for Ethos trait implementations
>
> > I think interactions are good, because I think that describes it
> > well, what it is really conceptually.
>
> -- psyche, STT.

> ## 2026-08-24 — interactions use the type itself in all cases
>
> > So, they're interactions use the type itself in almost all cases.
> > Well, really in all cases, because if it's not using the type
> > itself, then is it really an interaction of that type?
>
> -- psyche, STT.

**flows/aa4c7747/vision/tuples.md** — not archived. Distilled
(aa4c7747 tuples).

> ## 2026-08-24 — no tuple in the code we design; contact points only
>
> > tuple: no tuple in the code we design: if some parts require it
> > (standard traits, dependencies), then we allow it at that contact
> > point only

**flows/cff271af/vision/tuples.md** — not archived. Distilled
(cff271af tuples, if in sources/ethos.md). Seven entries, 2026-08-22,
typed; the one bearing on the Declaration:

> ## 2026-08-22 — the newtype is allowed and must be mentioned; tuples are a form of un-specification
>
> > the newtype is allowed. the fact that its a tuple is unfortunate
> > for us, so it would have to be mentionned in case.
> >
> > do we have to allow those? I really dont like tuples, they're a
> > form of un-specification
>
> -- psyche, typed.

**flows/2b34fafa/vision/ethosSourceFiles.md** — not archived. Distilled
(2b34fafa ethosSourceFiles). Three typed entries, 2026-08-20:

> ## 2026-08-20 — one document per file, one Rust module per document
>
> > "for the monolith thats good enough. easy cognition is the first
> > safe bet."

> ## 2026-08-20 — File is the type; "document" is dead
>
> > "document sucks. I dont understand your question. What's wrong with
> > File?"

**flows/2b34fafa/vision/ethosNamespaces.md** — not archived. Distilled
(2b34fafa ethosNamespaces). One typed entry:

> ## 2026-08-20 — namespace inside a file is ridiculous
>
> > "this concept is ridiculous in ethos. we're building the foundation
> > and youre talking about wallpaper"

**flows/b675f3d9/vision/kinds.md** — not archived. Distilled (b675f3d9
kinds). Seven entries, 2026-08-26 and 2026-08-27; the key ones:

> ## Qualifier form; Kind is the word; no generics in Ethos
>
> > 1. qualifier. Write isnt a kind. we say kind now, not trait.
> > declare a new kind = declare a new trait, in Ethos world, which
> > will imply some things which arent in rust world (tbd). so in
> > Ethos there are no generics, only kinds.
>
> -- psyche, 2026-08-26, typed.

> ## Capability is a function a kind has
>
> > 4. capability will refer to the actual functions a kind has
> > (Runnable would be the Kind, run would be a capability)
>
> -- psyche, 2026-08-26, typed.

> ## The kind syntax proposal is inappropriate; start from the anatomy of a Rust trait
>
> > Your kind syntax proposal is very... is completely inappropriate.
> > So start by looking at a rust trait, which is what our kind
> > essentially becomes, and in its most complex form ...
>
> -- psyche, 2026-08-26, STT.

> ## A kind's identity must mirror Rust's: name and constraints
>
> > important: in rust, a trait is identified by its name *and*
> > constraints. How would we want to mirror that?
>
> -- psyche, 2026-08-26, typed.

> ## A struct always has the same fields in the same order
>
> > a struct {} always has the same fields, in the same order. the
> > struct definition declares the field types, so they can be
> > anything; there are no restriction in which type a field can hold!
>
> -- psyche, 2026-08-27, typed.

**flows/62022e8f/vision/ethosTypes.md** — not archived. Distilled
(62022e8f ethosTypes). The map type in ethos. Quoted in the datom
section's supersession chain and in section 3.f:

> ## A map type is declared with guillemets: key type, value type
>
> > I just realized I never addressed KV specification in ethos.
> >
> > SomeMap.<< NameType ValueType>>
> >
> > I use << instead of guillemets because I dont know how to type
> > guillemets.
>
> -- psyche, typed.

**flows/62022e8f/vision/kinds.md** — not archived. Distilled (62022e8f
kinds). Quoted in the protos section (1.1) for the layer entries.

**flows/995a164e/vision/ethosTypes.md** — not archived. Distilled
(995a164e ethosTypes). One typed entry, 2026-08-30:

> ## The contained kind declaration is ethos, not datom
>
> > this is wrong. It ethos not datom.
> >
> > so maybe whrat [typed; what] youre reaching for is an Ethos meta
> > type which is followed by an implied (delimit-less) vector of
> > explicit ethos objects, such as KindDeclaration.{ ...
>
> -- psyche, typed (artifact comment).

**flows/995a164e/vision/kinds.md** — not archived. Distilled (995a164e
kinds, if in a sources file). Three typed entries:

> ## Name could be a capability of Conceptual
>
> > name could perhaps be a capability of Conceptual
>
> -- psyche, typed (artifact comment).

> ## Associated kinds, associated values: did you mean associated types? why not constants?
>
> > What's an associated kind? Russ [typed; Rust] doesn't have
> > associated traits, so did you mean associated types?
>
> > Why values? What's wrong with constants?
>
> -- psyche, typed (artifact comments).

**flows/2ef42163/vision/ethos.md** — not archived. Distilled (2ef42163
ethos). One typed entry:

> ## Rust syntax is the target; a principle in Rust is pointed at by recycling the same syntax
>
> > as Result and Self showed, rust syntax is the target, so whenever
> > we need to point at a principle in rust, we usually will recycle the
> > same syntax
>
> -- psyche, typed.

**flows/e8c4cc61/vision/ethosFileAnatomy.md** — not archived. Distilled
(e8c4cc61 ethosFileAnatomy). The handwritten page and the sweet-form
design. Seven entries; the ones bearing on the Declaration:

> ## The outer braces are omitted in any ethos file
>
> > the outer {} should be omitted and always implied in any ethos file
>
> -- psyche, typed.

> ## The sweet file syntax has a corresponding type
>
> > if we want the "sweet" ethos file syntax, we need a corresponding
> > type, like EthosFile (I dont like that name)
>
> -- psyche, typed. (The full sweet/canonical conversion example is
> quoted in the file and carried by Vision/ethos.md's Declaration.)

**flows/e8c4cc61/vision/kinds.md** — not archived. Distilled (e8c4cc61
kinds). Twelve entries; the key ones on the Declaration and kinds:

> ## A kind declaration's position holds a kind, not a type
>
> > that doesnt work. The kind declaration must use a kind, not a type.
>
> -- psyche, typed.

> ## No Embodiable; Embodied is an alias of Sized
>
> > I dont think there is any Embodiable. It's just Embodied, which is
> > an alias of Sized. Would that work?
>
> -- psyche, typed.

> ## A second syntax for a more complex kind, opening with `{`
>
> > your trait syntax doesnt work. Looks like we need to redesign the
> > kind syntax. We could add a second syntax for a more complex kind
> > which opens with { and has a few fields for things like super
> > traits.
>
> -- psyche, typed.

**flows/04db2fd2/vision/kinds.md** — not archived. Distilled (04db2fd2
kinds). Long typed entry on qualifier naming, Textualized, the Embodied
debate. Quoted in the protos section for its relevance to layers.

**flows/e4a40e/vision/archive-kinds.md** — archived (distilled into
Vision/ethos.md (Identity), flow ad19b1, 2026-09-04). Distilled
(e4a40e kinds). Two STT entries:

> ## 2026-09-03 — two heads differing in a required kind are two kinds
>
> > Yes, obviously those would be two kinds [STT: too kind].
>
> -- psyche, STT.

> ## 2026-09-03 — what identifies a trait in Rust is what identifies a kind
>
> > You don't have to decide which constraints are not part of an
> > identifier. What identifies a trait in Rust is what identifies a
> > kind in the ethos, because we're compiling the Rust [STT: rest], so
> > we don't have a choice.
>
> -- psyche, STT.

**flows/4decf7/vision/archive-kinds.md** — archived (distilled into
Vision/kinds.md (Kind, Naming), flow 4decf7, 2026-09-03). Distilled
(4decf7 kinds). Three entries:

> ## 2026-09-03 — kinds are qualifier-named
>
> > kinds are qualifier-named
>
> -- psyche, typed.

**flows/ad19b1/vision/archive-kinds.md** — archived (distilled into
Vision/ethos.md (Identity), flow ad19b1, 2026-09-04). Distilled
(ad19b1 kinds). Witnessed. Five typed entries:

> ## 2026-09-04 — "I said rust not rest"
>
> > I said rust not rest. what a shitshow!
>
> -- psyche, typed.

> ## 2026-09-04 — that's not how a Rust trait is identified
>
> > no, thats not how rust trait is identified. we spent hours over
> > this today.
>
> -- psyche, typed.

> ## 2026-09-04 — kind is an ethos concept, narrower than ethos; it goes in ethos
>
> > no, not at all. it is narrower than ethos, since it is an ethos
> > concept. so it goes in ethos.
>
> -- psyche, typed.

**flows/ad19b1/vision/ethos.md** — not archived. Distilled (ad19b1
ethos). Witnessed. Four entries, all 2026-09-04:

> ## 2026-09-04 — an associated constant is CAPACITY, written with the key-value map delimiter
>
> > it should be CAPACITY. and use a key-value map delimiter
>
> -- psyche, typed.

> ## 2026-09-04 — space the delimiters and the inner content
>
> > space the delimiters and the inner content.
>
> -- psyche, typed.

> ## 2026-09-04 — the constants in the key-value delimiter only works if their order doesn't matter
>
> > I've said that I wanted the constant association, or whatever
> > they're called, to use the key-value delimiter, but this can only
> > work if the constant declarations' order doesn't matter, as you
> > said. In the key map, the order is not guaranteed, right?
>
> -- psyche, STT.

> ## 2026-09-04 — key-value delimiters for sections that cannot have the same key
>
> > Let me see what it would look like if we used the key-value
> > delimiters for declaring sections that could not have the same key,
> > such as type declaration, kinds, or kind capabilities.
>
> -- psyche, STT.

The third and fourth entries are undistilled (not in
Vision/sources/ethos.md). The first two are distilled.

**flows/6329f1/vision/archive-ethos.md** — archived (distilled into
Vision/ethos.md (Declaration), flow 6329f1, 2026-09-04). Distilled
(6329f1 ethos). Witnessed. Two STT entries:

> ## 2026-09-04 — the file is the sweet form; the braced form is canonical
>
> > You didn't understand that the ethos file is the sweet form, and
> > the second version, where it's `library.` and then it opens `{}`,
> > is the canonical form, the non-sweet form. You have them backwards,
> > and in order to keep the pipe clean, the suite [STT: sweet] file
> > form of ethos should be kept out of the main logic run. It should
> > be done as a pre-step before we even get to text, so that,
> > essentially, an ethos file, we just do not consider it text yet. It
> > should be converted mechanically to the proper text form before we
> > proceed.
>
> -- psyche, STT.

> ## 2026-09-04 — proper ethos is variant-headed: kinds, types, signal, sema variants
>
> > That way, the ethos parser uses proper ethos, which is
> > variant-headed and is a properly defined struct with its version and
> > all of its different fields. There would be:
> >
> > * a `kinds` variant, which only holds kinds
> > * a `types` variant, which only holds types
> > * a `signal` variant, which holds certain specialized types that
> >   automatically have kind associations
> >
> > You would have a query type and a response type, and these would
> > each have their own respective implied associations, implied kind
> > associations. The same would be true of a sema ethos type, which
> > would have a storage type or a record type (whatever you want to
> > call it) that would have associated kinds, implied associated kinds.
> >
> > It's sort of just a shorthand syntax. Instead of just manually
> > always adding the associations, it's just implied because these
> > types always need to implement those kinds in these ethos variants,
> > essentially different kinds of structs.
>
> -- psyche, STT.

**flows/e996e8/vision/ethos.md** — not archived. Undistilled.
Witnessed. One typed entry, post-landing:

> ## 2026-09-04 — drop the version number altogether; any type needs an import section
>
> > I think I want to drop the version number altogether. datom doesnt
> > have versions. if we version stuff it should be in a manifest of
> > some kind. Lets drop the versionning everywhere for now. I guess
> > any type would need an import section.
>
> -- psyche, typed.

### 1.3 Datom

#### Distilled state

**Vision/datom.md** (witnessed whole, 202 lines). Sections: Name;
Nature; Repository and migration; The interface shape;
De/serialization; Relation to Ethos; Syntax; Meaning. Git history
(witnessed): c2a0223b6 2026-08-24 flow 68512643 (first landing);
7a3459519 2026-08-24 flow 68512643 (output-is-an-enum); 6880ce021
2026-08-27 flow 04db2fd2 ("curly-quote strings, guillemet maps");
6600aa659 2026-08-27 flow acbb6006; 388f6fc29 2026-09-03 (rename
child-flow → subflow, incidental); 5c5f75977 2026-09-03 22:32 flow
ad19b1 ("Land the datom Meaning distillate"). The Syntax block's
present wording landed through flow e4a40e on 2026-09-03 according to
the archive headers of the records it consumed (04db2fd2
archive-datomMaps, e8c4cc61 archive-datomSyntax, 62022e8f
archive-datomSyntax, 995a164e archive-datomSyntax, e4a40e
archive-datom, archive-vocabulary, all "distilled … into
Vision/datom.md (Syntax), flow e4a40e, 2026-09-03"); no commit
message in Vision/datom.md's history names e4a40e, so the commit that
carried it is not identified here (unknown).

**Vision/sources/datom.md** (witnessed whole, 40 entries): ac1e9ec8
datomSyntax, datomIsData; 01a03eda datomInteger; 04db2fd2 datomMaps,
datomNexus, text, textualTypes, anatomy, portion, directionAsymmetry;
e8c4cc61 datomSyntax, datomizable, protos; 62022e8f datomSyntax,
kinds, symbols, headedAndContained; 995a164e datomSyntax; 01a04339
datom; 01a035d3 rustCodeFromTheData; 01a03d6e dotosFiles,
ethosInterfaces; a5587095 structuredStringType; 5abf3be8
colonLegalInStringPosition; 06196cc7 datomSyntax; b675f3d9
structuralParsing; 4decf7 datomSyntax; e4a40e datom, vocabulary,
newtypeWrappingAndSingleFieldStructs; 06196cc7 encodedFormIsTheCode;
a5587095 datomSyntax, threeStacks, colonFormTransformerSyntax,
protosIsTheSharedStyle; 01a03eda datomSyntax; vision-raw datomSyntax;
ad19b1 meaning.

**Intent/data.md** (relayed): approved as Intent 2026-09-02, flow
995a164e; everything is data; code is data; one plane.

The landed Syntax block on the map question, witnessed, Vision/datom.md:

```
   112	quoted string is opaque: every delimiter inside it is content until
   113	the closing quote. Guillemets delimit a map; inside, key and value are
   114	separated by a space, resolving by position. A map in a position that
   115	expects a map carries no head, since the position already knows its
   116	type; a head is thereby always a variant. An integer is written as
```
```
   148	; a map of Text to Address
   149	« home { “12 Rue de la Paix” Paris 75002 }  work { “1 Place Vendôme” Paris 75001 } »
   150	
   151	; a map of Text to Integer
   152	« name:first Ada  born 1990 »               ; the colon inside a bare word is content: the position holds a string
```

These are the only map/guillemet lines in Vision/datom.md (witnessed
by grep; line 34's "keyed by the content-addressed hash" is not the
map concept).

#### Raw records, oldest first

All datom records below were read by this subflow (witnessed) unless
marked relayed.

**vision-raw/archive-datomSyntax.md** — archived ("Archived 2026-08-23
by flow 68512643; distilled into Vision/datom.md"). Distilled
(vision-raw datomSyntax). Two entries:

> ## 2026-08-11 — Datom carries data only; no generics
>
> > datom doesnt do generics, it only carries data, like json (but
> > strictly typed of course)
>
> — psyche, 2026-08-11T17:35+02:00 (Designer session 012fbf07), typed,

> ## 2026-08-11 — fix Datom first; the syntax must become consistent
>
> > So we can just fix datum [Datom] first because we need that. We
> > need the syntax to start being consistent.
>
> > I'm not even sure where parentheses are going to be in datum
> > [Datom] because in ethos, they're for transformers.
>
> — psyche, 2026-08-11T17:35+02:00 (Designer session 012fbf07),
> dictated;

**flows/a5587095/vision/archive-datomSyntax.md** — archived ("Archived
2026-08-23 by flow 68512643; distilled into Vision/datom.md").
Distilled (a5587095 datomSyntax). Three entries; the one on maps:

> ## 2026-08-11 — map payload is a vector: `Map.[key.val …]`
>
> > Yes, map would use .[ since a map is conceptually a list of
> > key/values
>
> — psyche, 2026-08-11T19:17+02:00 (Designer session a5587095), typed.
> Supersedes the ported `Map.(…)` encoding: the map payload is a
> square-bracket vector of `key.value` entries.

The other two entries (parentheses must not be unused in Datom;
parentheses delimit the structured string) are the seeds of Meaning.
This map entry is superseded by ac1e9ec8's 2026-08-26 guillemet
ruling below, which is in turn superseded by ad19b1's 2026-09-04 drop
ruling (section 3.f).

**flows/06196cc7/vision/archive-datomSyntax.md** — archived ("Archived
2026-08-23 by flow 68512643; distilled into Vision/datom.md").
Distilled (06196cc7 datomSyntax). Nine entries dated 2026-08-13 and
2026-08-14, all "— psyche, 2026-08-1x (Designer session 06196cc7),
typed". The entries bearing on the layers and structure:

> ## 2026-08-14 — the dotted prefix of a delimiter is part of its type
>
> > And the dotted prefix of a delimiter must be part of its type. it
> > could be a universal type, and unprefixed blocks simply have no
> > prefix. what do we want to call the prefix shape?

> ## 2026-08-14 — Head is the official term
>
> > I like the Head terminology actually. lets make it official
>
> > for the text block type? Head

> ## 2026-08-14 — variants always re-emit their head; special shapes depend
>
> > is Note a variant? then yes. does it have a special shape? then
> > it might. It depends.
>
> > Like in ethos, when we are defining types, X.{} is a struct
> > called X, and textualizing that type back will re-emit X.{} which
> > must be understood in the right context if printed alone, or
> > inserted in the right position, if the whole source is
> > textualized

> ## 2026-08-14 — bare strings may carry load-bearing symbols
>
> > If its a string, then it can use symbols which would be load
> > bearing in other situations, just like delimiters in string
> > blocks. no problem there. lets make the machinery fit for this,
> > bullet proof not by lots of complex code, but by the right
> > abstraction layers.

The remaining five entries (Meaning postponed; string blocks ignore
interior delimiters; a string that doesn't need quotes must not be
quoted; parentheses default then backpedalled to balance-based; bare
{…} is a struct) are carried in Vision/datom.md's Syntax and Meaning.
The 2026-08-14 "parentheses are the default string delimiter" entry is
superseded by ac1e9ec8's 2026-08-26 curly-quotes ruling below, as
that record itself says.

**flows/4decf7/vision/archive-datomSyntax.md** — archived ("distilled
… into Vision/datom.md (Syntax, De/serialization), flow e4a40e,
2026-09-03"). Distilled (4decf7 datomSyntax).

> ## 2026-08-04 — String is correct; remove the table entry
>
> > String is correct; remove the table entry
>
> -- psyche, typed. Transcript 6b31eff3, line 741.

> ## 2026-08-07 — how do we represent floating integer, represent in decimal
>
> > I also dont like the version number. which makes me wonder; how do we represent floating integer, represent in decimal (0.1)? Technically, if the expected position is a float, then it should be aple to read Interface.0.1.0 right?
>
> -- psyche, typed. Transcript d63804f2, line 129.

**flows/5abf3be8/vision/archive-colonLegalInStringPosition.md** —
archived (distilled into Vision/datom.md (Syntax), flow e4a40e,
2026-09-03). Distilled (5abf3be8 colonLegalInStringPosition).

> > and : remains legal in a position expecting a string
>
> — psyche, 2026-08-06T17:39:42Z (Designer session 5abf3be8; entry
> captured 2026-08-08 from the session transcript during the
> rulings-audit backfill)

**flows/01a03eda/vision/archive-datomInteger.md** — archived
(distilled into Vision/datom.md (Syntax), flow e4a40e, 2026-09-03).
Distilled (01a03eda datomInteger).

> ## 2026-08-26T17:54:13Z
>
> Context: The living answered the proposal that Datom Integer use canonical bare decimal syntax—`0`, `42`, `-42`; ASCII digits, no leading `+`, and no leading zero except `0`.
>
> > 1. yes
> > 2. I dont understand why Current needs an entire struct. Locks.Current should be enough. But Observe.CurrentLocks is even better.
>
> Only answer 1 concerns this entry. Provenance: current Codex history, session `01a03eda-0e08-7451-a5bf-ab48a2f67328`, physical line 7385, transcript ordinal 7384.

**flows/01a03eda/vision/archive-datomSyntax.md** — archived
("distilled into Vision/datom.md (Meaning), flow ad19b1, 2026-09-03").
Distilled (01a03eda datomSyntax). One entry, a reconstruction of the
ac1e9ec8 curly-quotes ruling quoted below; provenance
"`/home/li/.claude/projects/-home-li-primary/ac1e9ec8-903f-4ee0-a9e3-4a5d472c05e0.jsonl`, physical line 332, living message `0087e679-c696-40da-826e-9a33ea14c6db`."

**flows/01a03d6e/vision/archive-dotosFiles.md** — archived (distilled
into Vision/datom.md (Repository and migration), flow e4a40e,
2026-09-03). Distilled (01a03d6e dotosFiles).

> ## 2026-08-26T10:10:32.842Z — there should be no Dotos files anymore
>
> > There should be no Dodos files anymore.
> >
> > So this is also something which we should indicate somewhere. I'm not sure where, but you'd have to make a proposal for some parts.
>
> Speech-to-text correction beside the quote: `Dodos` → `Dotos`.
>
> — psyche, source-event timestamp `2026-08-26T10:10:32.842Z`; typed message record …

**flows/01a03d6e/vision/ethosInterfaces.md** — not archived. Distilled
(01a03d6e ethosInterfaces is in sources/datom.md). Three entries,
2026-08-26, typed (Codex session 01a03d6e). The one bearing on the
CLIs speaking datom:

> ## 2026-08-26T15:04:27.982Z — that is obsolete nota/dotos format
>
> Agent-proposed forms corrected by the psyche:
>
> > (Lock LockSpecification.{name flow-id paths description})
> > (Release LockId.42)
> > (Observe (Locks Current))
>
> The correction is:
>
> > that is obsolete nota/dotos format

And on the interface shape:

> ## 2026-08-26T14:22:01.126Z — observe is the root variant
>
> > the better design would be observe with a, observe is the root variant, and then it has, it contains another, maybe a list, or sorry, another enum, right, which is represented as a list in that particular spot in the ethos syntax of the subcommand for that observe.

**flows/ac1e9ec8/vision/datomSyntax.md** — not archived. Distilled
(ac1e9ec8 datomSyntax). The record that chose guillemets for maps.
Every entry is "— psyche, 2026-08-26 (Design session ac1e9ec8),
typed". Quoted whole because it is the origin of what ad19b1 dropped:

> ## 2026-08-26 — a map in an expected position carries no Map head
>
> The flow's view showed a map as `Map.[ k.v k.(v) … ]`. The correction:
>
> > If a position expects a map, the data will be [ k.v ... ], no Map.
>
> Asked in the same message, not ruled:
>
> > Is there a scenario in which a Head. isnt a variant?

> ## 2026-08-26 — considering positional key/values in a map
>
> > Im considering making key/values resolve by position in a map
> >
> > [ key value second-key second-value ... ]
> >
> > that looks cleaner and makes the Head. always a variant; lower
> > cognitive cost
>
> — … Under consideration, not ruled.

> ## 2026-08-26 — or a dedicated delimiter for maps
>
> > or we could use one of the unused delimiters for maps, making them
> > easy to spot visually
>
> — … Under consideration, not ruled.

> ## 2026-08-26 — guillemets delimit a map
>
> > let use the guillemets.
>
> — psyche, 2026-08-26 (Design session ac1e9ec8), typed, choosing
> between positional pairs in brackets and a dedicated map delimiter
> (guillemets or angle brackets). Entries resolve by position inside;
> a Head is thereby always a variant.

> ## 2026-08-26 — corrections to the first full-vision draft
>
> On "Datom is the psyche's own coinage for the data notation":
>
> > dont be so apologetic. Datom is the most advanced textual data
> > format in the world.
>
> On "Generics and Rust generation belong to Ethos":
>
> > I said no negatives. This is useless. Do we say "JSON doesnt
> > support generics"?
>
> On "like JSON":
>
> > Let's keep this noise out. Totally unecessary.
>
> On "All naming and self-description live in the type":
>
> > this is ambiguous. Try explaining it properly. You might have to
> > understand it first. Apply this to the whole proposal; understand
> > then explain clearly and unambiguously. Separate statements that
> > make a sentence confusing when you try to say them together. Split
> > everything up then re-assemble <- there's something to extract into
> > distillation skill from this.
>
> On bare strings:
>
> > re: bare strings: make sure it's clear that a string is a string
> > only in a position where the type defines a string.
>
> On the glyph question (typed « » or ASCII << >>):
>
> > I dont understand. those are completly different things. <> is
> > used in ethos, and those two must remain compatible in case datom
> > is ever eventually embedded into some ethos positions.
>
> On "each delimiter shows its container's kind":
>
> > this conflicts with ethos vocabulary.
>
> On whether "the root text" opens with the variant or the type name:
>
> > "the root text" - what are you talking about? If we are reading an
> > enum, then it'll start with a variant. if not, it wont. I feel like
> > you really still dont understand the datom vision. the
> > implementation must be pretty bad

> ## 2026-08-26 — curly quotes are the string delimiter; parentheses reserved for Meaning; datom is the edge form of signal
>
> On "Consistency comes first: datom's syntax is fixed before the rest.":
>
> > what does this mean? the rest of what?
>
> On "Curly quotes are the legacy string delimiter, read and landing as String.":
>
> > not legacy. In fact I think they should be positioned as the
> > default string delimiter. the vision is that parenthesis will
> > become the delimiter for structured strings, still to be designed.
> > So let's switch it all to curly quotes first, with parenthesis
> > reserved for structured strings, which we currently designate as
> > Meaning
>
> On "Everything is datom: every data file and every wire message.":
>
> > no, this is false. all our components speak signal, not datom;
> > datom is only used at the edge to let text-based systems (LLMs and
> > all existing editors) understand signal.
>
> — psyche, 2026-08-26 (Design session ac1e9ec8), typed. Supersedes the
> 2026-08-14 ruling that parentheses are the default string delimiter.

**flows/ac1e9ec8/vision/datomIsData.md** — not archived. Distilled
(ac1e9ec8 datomIsData).

> ## 2026-08-26 — the proposal mixed datom with ethos
>
> The flow proposed distilled statements on datom syntax that carried
> protos parse machinery (shapes, contexts, Realize/Textualize, real
> and signal forms) and Ethos-side rulings (variant naming, guillemets,
> program arguments). The correction:
>
> > you've mixed up datom with ethos. datom is data
>
> — psyche, 2026-08-26 (Design session ac1e9ec8), typed.

**flows/01a04339/vision/archive-datom.md** — archived (distilled into
Vision/datom.md (The interface shape), flow e4a40e, 2026-09-03).
Distilled (01a04339 datom).

> ## 2026-08-27 — good enough for now
>
> After the flow proposed `Observed.Locks.[]` as the self-describing reply shape, rather than `Observed.[]`:
>
> > >   Observed.Locks.[]
> >
> > good enough for now.
>
> — psyche, 2026-08-27T12:56:23.765Z (14:56:23.765 CEST), Codex session `01a0434b-3b36-7822-bc90-63e3663f0031`, transcript physical line 275 / response-item ordinal 274, typed.

**flows/4d5fc7da/vision/datom.md** — not archived. Undistilled (no
sources file names 4d5fc7da). Date not in the record; context is the
Lojix deploy request redesign.

> ## Datom does not support omittable fields yet
>
> Context: the flow had shown the redesigned Lojix deploy request with its
> optional revision left out of the written datom
> (`Deploy.Host.{zeus Activate}` for `Deploy.Host.{ Node Action Option<Revision> }`).
>
> > just remember datom doesnt support omittable fields yet.
>
> -- psyche, typed.

**flows/04db2fd2/vision/archive-datomMaps.md** — archived ("distilled
as they were spoken, into Vision/datom.md (Syntax), flow e4a40e,
2026-09-03"). Distilled (04db2fd2 datomMaps). No date in the entry
heading; the flow is dated 2026-08-27/28.

> ## Guillemets for maps; key and value separated by a space
>
> > Vision/datom.md still says parentheses-default strings and [key.value ...] maps; your 2026-08-26 rulings supersede both ... lets get that fixed, we use guillemets for maps now, with key and value separated by a space
>
> -- psyche, STT.

**flows/04db2fd2/vision/archive-datomNexus.md** — archived (distilled
into Vision/datom.md (Repository and migration), flow e4a40e,
2026-09-03). Distilled (04db2fd2 datomNexus). One STT entry: datom
stays a library for now; eventually a nexus translating formats.

**flows/04db2fd2/vision/text.md** — not archived. Distilled (04db2fd2
text).

> ## Text must have something over String; normalized (non-structural whitespace removed); a type needed anyway to implement the trait; content-addressed hash for cached reading; first use for a datom nexus, deferred; library renamed to free "datom" for the nexus
>
> > Re: Text: It would have to have something over a String. non-structural whitespace-removed? Otherwise it's really just a String. Although we might need a type anyway just so we can implement the trait for it (Prospective) since the impl must live either with the type or the trait. If we normalize it then we can have a reliable content-addressed hash tied to it which could be hand for cached-reading (instantly get the data without parsing from a parsing cache? could be the first use for a datom nexus - deferred for now, lets stick with the library. Let's call the library something different so we free 'datom' for the eventual nexus. datom-codec?)
>
> -- psyche, typed.

**flows/04db2fd2/vision/textualTypes.md** — not archived. Distilled
(04db2fd2 textualTypes). Four entries; the ones bearing on the layers
and the vocabulary:

> ## The type is a prospective datom [STT: datum]; the invert does not yield the same thing
>
> > in the implementation of the datum [STT: Datom] ... The type could be... Like it's a candidate, or it's a possible datum [STT: Datom]. Yeah, it's a possible datum [STT: Datom], basically. It's a prospective datum [STT: Datom]. Because until it has actually been parsed, we don't know if it actually is. Whereas when it comes back the other way around, it will be a datum [STT: Datom]. So actually, the invert operation doesn't yield the same thing. ... it comes in untrusted, or, you know. Because the only way it comes in direct is as a signal, as a binary signal, and that is not datum [STT: Datom].
>
> -- psyche, STT.

> ## Prospective<T> for text as a would-be T; Datom is kind not type since it lacks a definite shape
>
> > I like "Text taken as a would-be T: Prospective<T>" which gives us Prospective<Datom> although Im unsure if Datom is type or kind, probably kind, since it doesnt have a definite shape yet: give me your input on that.
>
> -- psyche, typed.

> ## Re datom kind: Datomic
>
> > Re datom kind: Datomic
>
> -- psyche, typed.

"Prospective" in these entries is superseded by 1c282d's "potential"
(2026-09-04) and 6329f1's "potential, not prospective" (section 1.4).

**flows/04db2fd2/vision/directionAsymmetry.md** — not archived.
Distilled in sources/datom.md (04db2fd2 directionAsymmetry); not in
sources/protos.md though Vision/protos.md's Direction carries it (as
e996e8's log also notes).

> ## Approved for distilled vision: in is a prospective datom untrusted until matched; out is a datom; Realize faults, Textualize does not; spans found inbound, computed outbound; multi-pass
>
> > exactly. this can go straight into distilled vision
>
> Context: the flow's statement that in is a prospective datom untrusted until it matches, out is a datom; Realize carries a fault and Textualize none; spans are found on the way in and computed on the way out; multi-pass.
>
> -- psyche, typed.

**flows/e8c4cc61/vision/archive-datomSyntax.md** — archived (distilled
into Vision/datom.md (Syntax), flow e4a40e, 2026-09-03). Distilled
(e8c4cc61 datomSyntax). Flow dated 2026-08-29.

> ## A single semicolon is the comment marker
>
> Context: the protos skill draft used `;` for comments, as on the
> psyche's handwritten page; the realization prompt had used `;;`.
>
> > I guess a single ; is for comments now. semi-colon isnt load bearing anymore so that works.
>
> -- psyche, typed.

> ## Style: a space inside a bracket delimiter, at both ends
>
> Not load-bearing for the parser; readability.
>
> > This is not load-bearing on a parser, but just for ease of reading, I would like it whenever there's a delimiter in proto syntax, not the curly quotes, not for strings, but for the brackets or maybe just the brackets. I think it would be good style to leave a space between the delimiter and the next thing inside of it, both at the beginning and the end. It's easier to see the separation there. Otherwise, it just looks like one big word with the head, the dot, the delimiter, and the other thing inside it. It's hard to visually separate them.
>
> -- psyche, STT.

**flows/e8c4cc61/vision/datomizable.md** — not archived. Distilled
(e8c4cc61 datomizable). Four entries; the first is a notion raised to
vision:

> ## Datomizable: a default kind describing a type's textual structure and its inner context
>
> Filed as Notion at first ("the
> following is on the bottom layer"); raised to Vision by the psyche on 2026-08-29, see below.
>
> > Datomizable would be a kind with a default capability, and born by all ethos types by default. It would describe the textual structure of this type (maybe even in different contexts, so and this very context could also be a capability of any Datomizable kind which is used whenever a portion is interpreted *inside* the portion of such a kind)
> >
> > Explain this concept to me with actual examples to see if you got it
>
> -- psyche, typed.

> ## The default capability exists to be overridden
>
> > no, the point being that it can be overriden
>
> -- psyche, typed.

> ## Raised from notion to vision
>
> > This is a notion but I think it's quickly becoming a vision so let's just make it a vision. Spare no ambition.
>
> -- psyche, STT.

> ## The context idea was not expressed properly; the word is overloaded; contexts are a set, per dialect
>
> > I didn't really express the context idea properly and I think also we need a better word because the word context is a bit overloaded. Let's take an example that actually has variations.
> >
> > I explained earlier, maybe it was in this flow, that there would be a logical dependency to what I'm saying. ... Right there would be a set of different contexts. A type definition is a certain kind of context. Also we're per dialect. This is per dialect, right? I don't know if this would be implied already or not which dialect we're working on or if it would be explicit, like ethos type decoration.
>
> -- psyche, STT (first sentence typed).

The fourth entry, "The complex example: a variant named as an
existing type, and the inventory pass", is STT and describes a
first-pass inventory of types before variants can be completed.

**flows/995a164e/vision/archive-datomSyntax.md** — archived (distilled
into Vision/datom.md (Syntax), flow e4a40e, 2026-09-03). Distilled
(995a164e datomSyntax).

> ## A datom is not preceded by a Datom root; a comment may indicate it is datom
>
> Context: artifact comment on a recap example block that began with the root `Datom` (2026-08-30 18:52).
>
> > datom is not preceded by a Datom. but one could use a comment to indicate it is datom.
>
> -- psyche, typed (artifact comment).

**flows/62022e8f/vision/archive-datomSyntax.md** — archived (distilled
into Vision/datom.md (Syntax), flow e4a40e, 2026-09-03). Distilled
(62022e8f datomSyntax). Flow dated 2026-09-02.

> ## Spaces inside delimiters are canonical, braces included; never inside curly quotes
>
> Context: the flow had asked whether braces get the inner space like
> brackets, citing the psyche's own compact `{0 1 0}`.
>
> > The example with the compact version number I had just copied, so it was not intentional for me to not have spaces there between the delimiters and the content. It will be canonical, but it is not load-bearing or considered good style to leave a space between the delimiters and the content, except for the strings, of course. The curly quotes, there it'll be bad because a space in that would be load-bearing, so it actually even disqualifies just on that fact.
>
> -- psyche, STT.

Note (mine): the sentence "it is not load-bearing or considered good
style to leave a space" reads against Vision/protos.md's Canonical
print ("it is canonical, and it is considered good style, to leave a
space"). Both e8c4cc61 above and ad19b1's "space the delimiters and
the inner content" say the space is good style; I read the 62022e8f
sentence as STT with a dropped word, but I do not resolve it. Listed
in section 4.

**flows/62022e8f/vision/symbols.md** — not archived. Distilled
(62022e8f symbols).

> ## A capitalized and a non-capitalized bare symbol are two different types, needing two terms
>
> > And a bare [STT: bear] symbol also is different, and we should have a different term to speak of those two different types, whether it's capitalized or not.
> >
> > One is an Embodiment ... A Corporal symbol, I guess you could say.
> >
> > The non-capitalized version is more like a reference. It's more like a path to something, like a link, if you will. Maybe like a linking symbol or something. Also, because of the bare string capability, it could also just be a bare string. You don't want to use this extremely specifically and uncontextualized, or again, there's that word context, which is being overloaded in so many ways.
>
> -- psyche, STT.

**flows/62022e8f/vision/headedAndContained.md** — not archived.
Distilled (62022e8f headedAndContained). Two STT entries; the second:

> ## Headed and contained are the terms; the contained form is how the embodiment is specified; the headed form is syntax sugar
>
> Context: artifact comment on the Headed-and-contained figure.
>
> > I like the headed and contained. I think these terms are appropriate to differentiate the two forms. So the headed form and the contained form of an embodiment are the two ways which it can be represented textually. And the contained form is how its embodiment is specified, because obviously in Rust, this all needs to be written with Rust types. So in Rust it's going to be a struct, and its head or its name is going to be one of the fields in that Rust type. So the headed form is really a syntax facility or a syntax sugar, if you will.
>
> -- psyche, STT.

The first entry is a long STT passage on the same pattern; its
sentence on the ethos file is quoted in the ethos section's
cross-reference below since it bears on the sweet form: "in the ethos
file there is no surrounding delimiter because they would be, the
whole point is to make the file sort of cleaner because these
delimiters are sort of, they're redundant."

**flows/e4a40e/vision/archive-datom.md** — archived (distilled into
Vision/datom.md (Relation to Ethos, Syntax), flow e4a40e, 2026-09-03).
Distilled (e4a40e datom). Five STT entries dated 2026-09-03:

> ## 2026-09-03 — ethos could depend on datom, but for quite different reasons
>
> On the distillate's sentence "Ethos depends on Datom, at minimum to intake data for signals":
>
> > Well, that's not quite true, although ethos could depend on datom [STT: datum], but for quite different reasons. Ethos could be read as datom [STT: datum] in a certain pass, which could be interesting, but I'm not sure that that's even possible given the context and actualization of parsing involved in parsing ethos. I don't think that's a good subject for now. Why don't we just take that out and/or leave a very well-explained summary of kind of what I mean? The stuff that preceded that is good. Just saying, I approve what preceded that so far.
>
> -- psyche, STT.

> ## 2026-09-03 — a certain subset of text qualifies as a head
>
> On the distillate's "a Head is bare text ending in a dot":
>
> > No, not quite. A head has to qualify also in other ways than just bare text. Bare text is true, but it's not specific enough. There's a certain subset of text that qualifies as a head.
>
> -- psyche, STT.

> ## 2026-09-03 — "block" is ambiguous; the re-emitting sentence is fuzzy
>
> On the distillate's "the Head is part of the block's type, and a variant always re-emits its Head when textualized":
>
> > Here, I'm not sure what you mean by "block," so this could be ambiguous. Even the rest of your sentence, "a variant [STT: invariant] always re-emits its head when textualized," is kind of fuzzy.
>
> -- psyche, STT.

> ## 2026-09-03 — a braced structure in datom is a struct; with a head it is a variant carrying that struct
>
> On the distillate's "A brace structure without a head is a struct":
>
> > here you say a "braced [STT: brazed] structure without a head" is a struct, but a "braced [STT: brazed] structure in Datom [STT: Datum]" is a struct. It's just that if it has a head, then it's a variant that carries data, which is a struct. This line could be confusing, and maybe you need to re-understand what you're trying to understand here. Yes, "structure" is the right word. I would like an example that shows what the structure is in practice and where the recursive structure is inside the structure, and so on.
>
> -- psyche, STT.

> ## 2026-09-03 — the whole struct itself is also a structure
>
> On the structure-in-practice example:
>
> > your example is good, but you should also make it clear that the whole struct itself is also a structure.
>
> -- psyche, STT.

**flows/e4a40e/vision/archive-vocabulary.md** — archived (distilled
into Vision/datom.md (Syntax), flow e4a40e, 2026-09-03). Distilled
(e4a40e vocabulary).

> ## 2026-09-03 — "block" is not one of our terms; it's an ugly term
>
> The flow had explained the datom Syntax sentence using "block" for a delimited unit of text.
>
> > Absolutely not. "Block" is not any of the terms that we have been considering to talk about this thing, so no, no, no, no, no, no, no, no. On the block, absolutely not. It's an ugly term.
>
> -- psyche, STT.

**flows/ad19b1/vision/archive-meaning.md** — archived (distilled into
Vision/datom.md (Meaning), flow ad19b1, 2026-09-03). Distilled
(ad19b1 meaning). Three typed entries dated 2026-09-03: "there is no
more meaninigOrString. strings are strings, and meaning is meaning";
"no." (to "Meaning is seen in both datom and ethos and can live in
datom"); "Meaning is datom".

**flows/ad19b1/vision/datom.md** — not archived. **Undistilled** (no
sources file names ad19b1 datom). These are the records on the merit
of the map, written after 6329f1 opened; quoted whole in section 3.f.

### 1.4 Vocabulary

#### Distilled state

There is no Vision/vocabulary.md and no Vision/sources/vocabulary.md
(witnessed: the sources directory lists datom, distillation, ethos,
ethosMonolith, flowNexus, highLevelView, nexus, orchestrate, protos,
remembering). Vocabulary records are consumed by the topic they name:
Vision/sources/protos.md names 62022e8f vocabulary, 1c282d
vocabulary, 6329f1 vocabulary; Vision/sources/datom.md names e4a40e
vocabulary. The words themselves stand in Vision/protos.md (Direction:
"potential value"; Layers: "Potential and actualize", "incorporate",
"Corporal", "Sized is the bound borne by every corporal type";
Structure: "Structure is the word for every unit of the text; its
type is Protoform") and in Vision/datom.md (Syntax: "Structure is the
word for every unit of the text").

#### Raw records, oldest first

**flows/2f6b1dc5/vision/vocabulary.md** — not archived. Undistilled.
(Relayed; on the vocabulary skill, not on protos terms.) Three
entries, 2026-08-23 and 2026-08-24, typed: "no, a machine doesnt make
mistakes. The context created this output. But you never loaded the
deployment as a skill into your mid layer, and the vocabulary skill
doesnt (I think) instruct the model to override competing
terminology, which it should."; "good. approved." (the line "A
defined term overrides competing terminology in the flow's own
words"); "I prefer context to prompt. base context, stock context,
user context, etc. what do you think?"

**flows/01a052b6/vision/vocabulary.md** — not archived. Undistilled.
(Relayed.) One STT entry, 2026-08-30:

> ## Machine
>
> Context: The living clarified the preferred term for the non-living participant.
>
> > "I don't like the word, the term AI. And as you can see, I prefer to talk of flows rather than agents. And the machine is the term that I want to use, which is just basically a short for thinking machine."
>
> -- psyche, STT.

**flows/995a164e/vision/vocabulary.md** — not archived. Undistilled.
(Relayed; created 2026-09-01.) Three entries; the first bears on the
protos layer vocabulary:

> ## The vocabulary is not settled enough to judge the distillation wording
>
> Context: terminal, on the flow's proposed Vision/layers.md sentence.
>
> > Your vision distillation looks reasonable, but I still don't understand enough of the whole vocabulary. It's not settled enough for me in my mind to be able to say whether or not these are the terms that we should use to explain this particular part of the vision.
>
> -- psyche, STT.

The other two ("raw means you didnt ask for confirmation. and intent
requires confirmation. only vision can be raw"; "Actually, you forgot
that Notion can also be raw …") are on the psyche system's own
vocabulary.

**flows/62022e8f/vision/vocabulary.md** — distilled (62022e8f
vocabulary in sources/protos.md). Carried in the protos section
above, where the gathering agent read it.

**flows/e4a40e/vision/archive-vocabulary.md** — 2026-09-03, "block" is
an ugly term; quoted in the datom section above.

**flows/1c282d/vision/vocabulary.md** — not archived. Distilled
(1c282d vocabulary in sources/protos.md). Flow dated 2026-09-04; no
date in the entry headings. (Relayed, then witnessed.)

> ## Potential replaces Prospective
>
> > potential
>
> -- psyche, typed. (Answering: Prospective vs. Potential -- which stands?)

> ## Structure replaces Portion
>
> > structure
>
> -- psyche, typed. (Answering: Portion vs. Structure -- should it become Structure?)

**flows/6329f1/vision/archive-vocabulary.md** — archived ("distilled
into Vision/protos.md (Direction, Layers), flow 6329f1, 2026-09-04").
Distilled (6329f1 vocabulary). Witnessed.

> ## 2026-09-04 — potential, not prospective
>
> On the proposed Vision/protos.md Direction paragraph, "Text arrives as a prospective value and leaves as a value":
>
> > I thought we had agreed to switch from perspective [STT: prospective] to potential.
>
> -- psyche, STT.

**flows/e996e8/vision/protos.md**, second entry — not archived.
Undistilled. Witnessed. A vocabulary question on the corporal layer:

> ## 2026-09-04 — Incorporable could replace Corporal; is corporate a word?
>
> On the layers table's incorporate row, which names no kind (the flow had offered Incorporable):
>
> > Incorporable could replace Corporal. Is corporate a word? Corporal/corporate Incorporable/incorporate ?
>
> -- psyche, typed. (Asked as a question.)

**vision-raw/dictation-vocabulary.md** — title only, "# we should look
at the vocabulary for my speech-to-text", body empty (relayed).
**vision-raw/letsUseTheSameVocabulary.md** — one entry, "TrueNamed it
is", 2026-08-06, session 5abf3be8 (relayed); not on protos terms.

Supersession in this topic: Prospective (04db2fd2, e8c4cc61
prospective) → Potential (1c282d, then 6329f1). Portion (04db2fd2
portion) → Structure (1c282d) → "Structure is really Protoform"
(1c282d, per 6329f1's log). Embodied as the bound (62022e8f) → Sized
(6329f1 archive-protos: "drop Embodied; stick with Sized"). Realize →
incorporate (6329f1 archive-protos). Corporal → Incorporable is asked
as a question by e996e8 and not ruled.

---

## 2. Secondary topics

Path, heading, date, one-line gist; verbatim only where the record
bears on the map, the Declaration, the layers, or how reports and
distillations are presented to the living. All relayed from the
read-critical subagent unless marked witnessed.

### Distillation and design practice

- **Vision/distillation.md** (distilled; sources: b675f3d9
  visionImpurities, acbb6006 distillation, b675f3d9 distillation,
  ac1e9ec8 distillationNegatives). Headings: Vision impurities;
  Impurities fall out through distillation; A proposal names each
  statement's destination; A statement carries what the psyche said;
  Designing model behavior is vision; No useless negatives; A
  statement never attributes itself to the psyche.
- **flows/ac1e9ec8/vision/archive-distillationNegatives.md**
  (witnessed), 2026-08-26, typed: useless negatives are archived and
  the archive linked; "I want this kind of stuff to be in the
  forbidden list for vision distillation; this *is* the psyche's
  vision."
- **flows/cff271af/vision/distillation.md**, 2026-08-22: it's always
  better to distill; "never" is a very strong word; "There is no more
  manifest". Verbatim, on how distillation presents: "Distilled psyche
  has more value than raw psyche because the raw psyche is always
  archived, so it's always still there, and it's referenced by the
  new distillation. But it's more clear and it's more compact, so it
  offers more signal to noise."
- **flows/a60a9e85/vision/distillation.md**, 2026-08-23: "lets go
  through one concept at a time. you are unable to do a synthesis
  because you didnt understand the concept themselves. Lets take this
  opportunity to understand each concept to distill the psyche at the
  same time; they are the same thing really; distillation is
  comprehension"
- **flows/acbb6006/vision/archive-distillation.md**, 2026-08-27:
  sources files are one line per reference; "all distillation refers
  to the raw psyche it was distilled from. ... the references should
  sit in a separate file (one per topic) which only lists all the
  sources, appending new ones after every distillation."; "no, just
  the ID and topic; the path can be reconstructed from it. `e06e4c07
  nexus` one line per reference. simple"
- **flows/b675f3d9/vision/archive-distillation.md**, 2026-08-27: a
  proposal says where each statement goes; placement is part of the
  proposal.
- **flows/e4a40e/vision/distillation.md**, 2026-09-03: how a proposal
  is presented. Verbatim: "You're not going to show me the whole
  topic again. You're going to show me what you're changing, and
  you're not showing me a diff. You're just showing me you're
  incorporating your distillation. ... I just want to see the vision.
  I'll read it, and if I agree with it, then it lands. That's it. It's
  actually pretty simple, but I still want the flow to understand the
  procedure here, which seems to have not been the case so far." And:
  "Did you take the consideration to look at what you might be
  distilling into? Are you just distilling with the distillate, or are
  you just distilling the raw by itself without considering the
  already distilled vision? ... Why is it that every flow seems to
  have his own idea of how to do vision distillation?" Also: datom
  vision shows datom, not ethos syntax; elaborate examples, not baby
  stuff.
- **flows/ad19b1/vision/distillation.md** (witnessed), 2026-09-04,
  three typed entries: "Does that even make sense to you? Does that
  sentence even look like it remotely makes sense to you? Why would
  you even repeat this nonsense?"; "the distillation skill line
  should be made more universal."; and on the Declaration distillate's
  "what that brace holds and in what order is not yet designed": "Well,
  it will be as soon as I fucking approve this. Now I can't approve it
  because you're basically saying that I can't approve it by saying
  it's not decided. You're deciding for me ahead of time that I can't
  agree to this design. Do you see the ridiculous situation that
  you're creating here?"
- **flows/ad19b1/vision/designPractice.md** (witnessed), 2026-09-04,
  typed, on the Identity distillate's ethos example shown without its
  Rust: "dont forget to show the target rust". Distilled (ad19b1
  designPractice in sources/ethos.md).
- **flows/e8c4cc61/vision/designPractice.md**, 2026-08-29: main flow
  writes markdown; converting subagent uses scaled SVG, not mermaid;
  "Thinking machines just copy what they see, so any bad pattern is
  bad no matter where it appears and no matter at what layer."; find
  the beautiful Rust first, then work backward. Undistilled.
- **flows/62022e8f/vision/designPractice.md**, 2026-08-30/09-02: three
  skills protos, datom, ethos; datom and ethos show Rust; the protos
  skill stays general; always present the ethos spec of any new
  object; syntax in code blocks with comments, not broken-up bits.
  Undistilled.
- **flows/995a164e/vision/designPractice.md**, 2026-09-01: the protos
  skill shows datom, not ethos; pages are raw vision-ready content;
  do not spend Fable output on HTML. Verbatim on the layers: "we have
  different layers that are mixed up in the same block of code, which
  is problematic. So, either we need to make it very clear with
  comments that these are different sections. ... at least we need a
  variant. ... the first non-comment line would say kinds, capitalize
  of course, because it's a variant." Undistilled.
- **flows/4decf7/design/proposal1/distillation.md**, 2026-09-03, a
  proposal text (not a raw record): "A distillation re-distills: the
  existing distilled text of a topic goes into the distiller with the
  raw records, and the whole comes out distilled anew."; "Rust code is
  never shown alone: its equivalent ethos is always shown with it."
- **flows/ad19b1/vision/psycheSystem.md** (witnessed), 2026-09-04,
  typed: "looks like my psyche system is failing".

### Orchestrate and nexus, the CLIs speaking datom

- **Vision/orchestrate.md** (relayed): Deployment; The skill. Carries
  nothing on datom.
- **flows/01a03d6e/vision/ethosInterfaces.md** (witnessed),
  2026-08-26: imperative, verb-oriented interface; observe is the root
  variant; "that is obsolete nota/dotos format" (quoted in 1.3).
- **flows/01a04339/vision/archive-datom.md** (witnessed), 2026-08-27:
  `Observed.Locks.[]` "good enough for now." (quoted in 1.3).
- **flows/4d5fc7da/vision/datom.md** (witnessed): "just remember datom
  doesnt support omittable fields yet." (quoted in 1.3).
- 6329f1's own brief (witnessed, flows/6329f1/log.md line 9, typed):
  "regenerate orchestrate's ethos and make its CLIs actually speak
  datom."

### The release train

No psyche record on the release train was found in any vision or
notion directory. 6329f1's log (witnessed, line 178) says the
release-train record was written in datom at
release-trains/ProtoformStack.datom by a subflow and corrected on the
main flow's word, not the living's. 6329f1's log line 185: "No psyche
was spoken in this flow: the living's opening message was working
instruction". The living's later words to 6329f1 ("keep going",
fourth word) are logged as working instruction.

---

## 3. Checks the ad19b1 ruling raises

The ruling, witnessed, flows/ad19b1/vision/protos.md whole:

```
     1	# Protos
     2	
     3	## 2026-09-04 — drop the key-value delimiter and concept entirely from protos and its dialects
     4	
     5	After the research on the merit and the uses of the key-value map,
     6	and the FlatBuffers and GraphQL passages reprinted whole:
     7	
     8	> ok lets drop that delimiter and concept entirely from protos and its dialects.
     9	
    10	-- psyche, typed.
```

### a. Does the landed Vision/protos.md carry guillemets or a map? Does the Declaration?

**Witnessed.** Vision/protos.md at HEAD is the text 23aaf7a7f landed
(git log shows no later commit on the file). It names guillemets once,
as one of the six delimiter pairs, and does not use the glyphs or the
word "map":

```
    44	An enclosed structure stands between its delimiters. Six delimiter
    45	pairs in all: four structural — braces, brackets, guillemets, angle
    46	brackets — and two opaque — curly quotes, where every glyph inside
    47	is content, and parentheses, read by balance. Angle brackets are a
    48	real protos delimiter. A bare structure has no delimiters.
```

The Declaration section of Vision/ethos.md carries the map concept and
the guillemets in six lines (the full context is quoted in 1.2):

```
   156	name, a dot, and the aliased type. A map is a headed guillemet — the
   157	name, a dot, and guillemets holding the key type and the value type.
   167	  Roles.« Text Integer » ]
   174	pub type Roles = std::collections::BTreeMap<protos::Text, protos::Integer>;
   236	associated constants in a guillemet — upper case, in the map
   242	               « CAPACITY Integer »
```

Line 248, `const CAPACITY: protos::Integer;`, is the Rust the
guillemet line targets.

### b. Vision/datom.md's Syntax block

**Witnessed.** Every line carrying guillemets, "map", or the key-value
concept:

```
   113	the closing quote. Guillemets delimit a map; inside, key and value are
   114	separated by a space, resolving by position. A map in a position that
   115	expects a map carries no head, since the position already knows its
   116	type; a head is thereby always a variant. An integer is written as
   148	; a map of Text to Address
   149	« home { “12 Rue de la Paix” Paris 75002 }  work { “1 Place Vendôme” Paris 75001 } »
   151	; a map of Text to Integer
   152	« name:first Ada  born 1990 »               ; the colon inside a bare word is content: the position holds a string
```

Two further observations on line 152, both witnessed: 6329f1's log
(line 168) records its protos+datomic writer's finding that
"Vision/datom.md's 'map of Text to Integer' example holds Ada, not an
integer — a suspect example to surface to the living", and its closing
of the third word (line 229) lists "Vision/datom.md's map example"
among the decisions surfaced. ad19b1's datom record (3.f) shows the
living rejecting a fixed-key map example on 2026-09-04: "your using a
map that should be a struct".

### c. Does flows/6329f1/reports/remember-ad19b1.md carry the drop ruling?

**Witnessed: it does not.** The word "drop" does not occur in the
file. It does not name flows/ad19b1/vision/protos.md or
flows/ad19b1/vision/datom.md, neither of which existed when it was
written (see d). What it says about the map, the key-value delimiter
and the guillemets is the earlier, opposite ruling and the Declaration
example that carried it:

```
    22	## 2026-09-04 — an associated constant is CAPACITY, written with the key-value map delimiter
    27	> it should be CAPACITY. and use a key-value map delimiter
   255	Ethos, Syntax with the Person example and the Reply, map and vector
   372	                 « CAPACITY Integer »                           ;   then associated constants, a map of name to type,
   425	| dfbbcf00e | Record the living's ruling: associated constants are upper case, in the map delimiter |
```

Its commit table ends at 9bee4de31 ("space the delimiters and the
inner content", 2026-09-04 02:14:33), which was ad19b1's last commit
when 6329f1's subflow read it.

### d. Timeline from git

**Witnessed** (`git log --format='%H %ai %an %s' -1` on each):

| commit | author date | subject |
|---|---|---|
| 7d19dcacf | 2026-09-04 03:08:31 +0200 | Open flow 6329f1: remember 1c282d and ad19b1, gather, and fix the ProtoformStack design |
| 23aaf7a7f | 2026-09-04 17:14:39 +0200 | Land the living's corrected vision: Protos layers and the Ethos Declaration |
| 55554e368 | 2026-09-04 21:06:34 +0200 | Record the living's ruling: the map is dropped from protos and its dialects; close flow ad19b1 |

Order: 6329f1 opened, 6329f1 landed, then ad19b1's drop ruling was
committed, about three hours and fifty minutes after the landing.
ad19b1 kept running beside 6329f1 all day; its record commits after
6329f1 opened (witnessed, `git log -- flows/ad19b1/vision/{protos,datom,ethos}.md`):

| commit | author date | subject |
|---|---|---|
| 1444df20e | 2026-09-04 13:07:55 | Record the living's ruling: a map with fixed keys should be a struct |
| 5e748192a | 2026-09-04 14:14:22 | Record the living's thought on the map as a vector of structs; log the research dispatch |
| cc2b6c181 | 2026-09-04 19:37:19 | Record the living's words on constants order and on Datom not needing the standard; log the research dispatch |
| d0f69cf37 | 2026-09-04 19:44:02 | Record the living's words: key-value delimiters for unique-keyed sections |
| 55554e368 | 2026-09-04 21:06:34 | Record the living's ruling: the map is dropped from protos and its dialects; close flow ad19b1 |

Inference (mine): the first two of these predate 6329f1's landing, so
"a map with fixed keys should be a struct" and the research request
were in the tree when 6329f1 landed the Declaration; the drop ruling
itself was not.

### e. Does the realized code carry the map?

**Witnessed.** The datomic repository is at
/git/github.com/LiGoldragon/datomic (a worktree also exists under
/home/li/wt/github.com/LiGoldragon/datomic). The checkout is detached
at e4430bf; `main` and `origin/main` are both 4712361c0194fd4e251b2b79a80b2c298f82ce4b
("Fix Cargo.lock version for 0.9.1", 2026-09-04 14:17:26 +0200), the
datomic 0.9.1 that 6329f1's log names as the train's final datomic.
Read with `git show main:src/lib.rs`.

The Datom type at main has a Map variant:

```
/git/github.com/LiGoldragon/datomic  main = 4712361c  src/lib.rs
    19	pub enum Datom {
    20	    Variant(Symbol, Separator, Option<Box<Datom>>),
    21	    Struct(Vec<Datom>),
    22	    Vector(Vec<Datom>),
    23	    Map(Vec<Pair>),
    24	    Text(Text),
    25	    Meaning(Text),
    26	    Bare(Symbol),
    27	}
```

The reader treats a guillemet enclosure as a map (conceive):

```
   228	                Protoform::Enclosed(Enclosure::Guillemets, children)
   287	                Enclosure::Guillemets => {
   288	                    if children.len() % 2 != 0 {
   289	                        return Err(Fault::Conceptual(path.to_vec(), Problem::Pairing));
   290	                    }
   291	                    let mut pairs = Vec::with_capacity(children.len() / 2);
   292	                    for chunk in children.chunks_exact(2) {
   ...
   306	                        pairs.push(Pair(chunk[0].conceive_at(&kp)?, chunk[1].conceive_at(&vp)?));
   307	                    }
   308	                    Ok(Datom::Map(pairs))
```

And `BTreeMap<K, V>` bears Corporal and Datomic through `Datom::Map`
(lines 626–660); `Expected::Map` is a fault shape (line 94).

The protos repository at /git/github.com/LiGoldragon/protos: local
`main` is 56c683e (0.15.0); `origin/main` is 48061367 ("Derive Clone,
Debug, PartialEq, Eq on Situated<F>; bump to 0.15.1"), the protos
0.15.1 datomic 0.9.1 pins. At origin/main, `git show origin/main:src/lib.rs`:

```
    70	/// Structural enclosures: `{ }` `[ ]` `« »` `< >`
    75	    Guillemets,
   386	const OPEN_GUILLEMET: char = '\u{00AB}'; // «
   387	const CLOSE_GUILLEMET: char = '\u{00BB}'; // »
   432	        OPEN_GUILLEMET => Some(Enclosure::Guillemets),
   442	        Enclosure::Guillemets => CLOSE_GUILLEMET,
   987	                    Enclosure::Guillemets => ("\u{00AB}", "\u{00BB}"),
```

So the realized code at main carries the map and reads « » as its
delimiter, in both datomic and protos. Also witnessed: a
`ProtoformStack` branch exists locally and on origin in the protos
repository (e996e8's log had reported none visible).

### f. Psyche records on the merit of the key-value map or on guillemets, beyond the ruling

**Witnessed.** All records found by grep for "map", "guillemet",
"key-value", "«" across flows/*/vision, flows/*/notion and vision-raw
that speak to the merit or the choice, oldest first:

**flows/a5587095/vision/archive-datomSyntax.md**, 2026-08-11, typed
(session a5587095): "Yes, map would use .[ since a map is conceptually
a list of key/values" — the map as a vector of key.value entries.

**flows/ac1e9ec8/vision/datomSyntax.md**, 2026-08-26, typed: the four
entries quoted whole in 1.3 — "If a position expects a map, the data
will be [ k.v ... ], no Map."; "Im considering making key/values
resolve by position in a map … that looks cleaner and makes the Head.
always a variant; lower cognitive cost"; "or we could use one of the
unused delimiters for maps, making them easy to spot visually"; "let
use the guillemets."; and on the glyphs: "I dont understand. those are
completly different things. <> is used in ethos, and those two must
remain compatible in case datom is ever eventually embedded into some
ethos positions."

**flows/04db2fd2/vision/archive-datomMaps.md**, STT (flow of
2026-08-27/28): "we use guillemets for maps now, with key and value
separated by a space" (quoted whole in 1.3).

**flows/62022e8f/vision/ethosTypes.md** (relayed by the ethos
gathering; the map type in ethos), heading "A map type is declared
with guillemets: key type, value type", with the living's line: "I use
<< instead of guillemets because I dont know how to type guillemets."

**flows/ad19b1/vision/ethos.md**, 2026-09-04, witnessed whole:

> ## 2026-09-04 — an associated constant is CAPACITY, written with the key-value map delimiter
>
> On the complex kind example's associated constant, written
> `[Capacity.Integer]`, the name, a dot and its type in a bracket:
>
> > it should be CAPACITY. and use a key-value map delimiter
>
> -- psyche, typed.

> ## 2026-09-04 — the constants in the key-value delimiter only works if their order doesn't matter
>
> On the complex kind's associated constants, ruled earlier into the
> map delimiter:
>
> > I've said that I wanted the constant association, or whatever they're called, to use the key-value delimiter, but this can only work if the constant declarations' order doesn't matter, as you said. In the key map, the order is not guaranteed, right?
>
> -- psyche, STT.

> ## 2026-09-04 — key-value delimiters for sections that cannot have the same key; capabilities would need another design for self
>
> > Let me see what it would look like if we used the key-value delimiters for declaring sections that could not have the same key, such as type declaration, kinds, or kind capabilities. Obviously, it's not a big deal. If we used key-value delimiters for capabilities, we would have to change our design, which uses the head delimiter to convey something about the mutability or presence or absence of self. We could probably easily design something else, but I'd like to see what it would look like.
>
> -- psyche, STT.

(The second entry of that file, "space the delimiters and the inner
content", is not on the map.)

**flows/ad19b1/vision/datom.md**, 2026-09-04, witnessed whole,
undistilled:

> ## 2026-09-04 — using a map that should be a struct
>
> On the flow's proposed map example `« born 1815  died 1852 »`, a map
> of Text to Integer whose keys are fixed:
>
> > no, its all bad. your using a map that should be a struct
>
> -- psyche, typed.

> ## 2026-09-04 — the key-value map, where it really is just a vector of structs
>
> After three map examples for the datom Syntax block had failed, the
> living turned to the map itself:
>
> > Do some research into people that have questioned the existential merit of the key-value map, where it really is just a vector of structs.
>
> -- psyche, typed.

> ## 2026-09-04 — Datom doesn't need to implement something simply because it has been standard
>
> Asking for research into the legitimate uses of the key-value
> paradigm, to see whether key-values are wanted in data at all:
>
> > I think that will probably help us to see if key values are actually a thing that we want to have in data at all, because Datom [STT: Datum] is a revolutionary approach to data representation. It doesn't need to implement something simply because it has been so standard in the past.
>
> -- psyche, STT.

**flows/e996e8/vision/protos.md**, 2026-09-04, witnessed, undistilled
— the living restating the drop to the flow that succeeded 6329f1:

> ## 2026-09-04 — the key-value map delimiters are abandoned everywhere
>
> > You might want to check out recent flows. I've been talking about these topics and [STT: in] other flows, and we've abandoned the key value map limiters [STT: delimiters] everywhere. We're sort of stripping some stuff out now, and now I'm dropping the version.
>
> -- psyche, STT.

Related but not on the map: **flows/04db2fd2/vision/delimiters.md**
(relayed by the protos gathering), typed: "this is false; you are
talking about guillements, and what you showed is a double angle
bracket pair" — on the glyph, not the concept.

Supersession chain on this subject, stated plainly: Map.[key.val …]
(2026-08-11) → [ k.v … ] no Map head (2026-08-26) → guillemets,
positional pairs (2026-08-26, restated 04db2fd2) → map type in ethos
with guillemets (62022e8f) → constants in the map delimiter (ad19b1,
02:13) → "a map that should be a struct" and research into the merit
(ad19b1, 13:07–19:44) → "drop that delimiter and concept entirely
from protos and its dialects" (ad19b1, 21:06) → "abandoned … everywhere"
(e996e8). The landed Vision texts in 1.2 and 1.3 and the code in 3.e
stand at the guillemet stage.

---

## 4. Contradictions and tensions

Each with both quotes; none resolved here.

**4.1 The map, in all three landed files, against the drop ruling.**
Latest record, flows/ad19b1/vision/protos.md, 2026-09-04, typed: "ok
lets drop that delimiter and concept entirely from protos and its
dialects." Restated flows/e996e8/vision/protos.md, STT: "we've
abandoned the key value map limiters [STT: delimiters] everywhere."
Landed: Vision/protos.md line 45 "four structural — braces, brackets,
guillemets, angle brackets"; Vision/ethos.md lines 156–157 "A map is a
headed guillemet — the name, a dot, and guillemets holding the key
type and the value type.", line 167 `Roles.« Text Integer »`, lines
236–237 "associated constants in a guillemet — upper case, in the map
delimiter", line 242 `« CAPACITY Integer »`; Vision/datom.md lines
113–115 "Guillemets delimit a map; inside, key and value are separated
by a space, resolving by position. A map in a position that expects a
map carries no head", lines 148–152 the two map examples. The
Declaration's "in the map delimiter" carries ad19b1's own 02:13 ruling
("it should be CAPACITY. and use a key-value map delimiter"), which
the same flow's 21:06 ruling supersedes.

**4.2 The version in the Declaration against e996e8's drop of the
version.** Latest record, flows/e996e8/vision/ethos.md, 2026-09-04,
typed: "I think I want to drop the version number altogether. datom
doesnt have versions. if we version stuff it should be in a manifest
of some kind. Lets drop the versionning everywhere for now. I guess
any type would need an import section." Landed, Vision/ethos.md lines
104–105: "An ethos file is written in the sweet form: the root's head
with its version, then the sections as siblings"; line 78 `{0 1 0}`;
lines 126 and 131 `Types.{ 0 1 0 }` and `{ 0 1 0 }`; lines 112–113 "a
properly defined struct with its version and all of its fields" (this
last is the living's own 6329f1 words, archive-ethos.md: "a properly
defined struct with its version and all of its different fields").

**4.3 "Corporal" as the layer name against e996e8's question.**
Latest record, flows/e996e8/vision/protos.md, typed, asked as a
question: "Incorporable could replace Corporal. Is corporate a word?
Corporal/corporate Incorporable/incorporate ?" Landed, Vision/protos.md
line 60 "Text, Protoform, Concept, Corporal — four layers", line 77
"| incorporate | Corporal | Concept, and the layers above through the
chain |" (the row names no kind). A question, not a ruling; listed as
a tension, not a contradiction.

**4.4 Whether the inner space is good style (62022e8f against
Canonical print).** flows/62022e8f/vision/archive-datomSyntax.md, STT:
"It will be canonical, but it is not load-bearing or considered good
style to leave a space between the delimiters and the content, except
for the strings, of course." Landed, Vision/protos.md lines 92–94: "It
is canonical, and it is considered good style, to leave a space
between the delimiters and the content, except for the curly quotes
where a space would be load-bearing." The later records (ad19b1 "space
the delimiters and the inner content"; e8c4cc61 "it would be good
style to leave a space") agree with the landed text; the 62022e8f
sentence stands against it as written.

**4.5 The map example's Ada (a suspect example).** Vision/datom.md
lines 151–152: "; a map of Text to Integer" / `« name:first Ada  born
1990 »`. 6329f1's log line 168: "Vision/datom.md's 'map of Text to
Integer' example holds Ada, not an integer — a suspect example to
surface to the living." No psyche record rules on it; ad19b1's "your
using a map that should be a struct" was said of a different example
(`« born 1815  died 1852 »`). Moot if 4.1 is acted on.

**4.6 Unreviewed Declaration text against the living's reading
boundary.** Not a contradiction between records, but a standing
caveat 6329f1's log states (line 244 and the e996e8 remembering): the
living read the two proposals "up to the Declaration's File section";
everything in Vision/protos.md past Direction and everything in the
Declaration from Imports on was landed on the flow's authority under
the one-sweep instruction. The map lines in 4.1 (ethos 156–157, 167,
236, 242) all fall in that unreviewed span.

**4.7 6329f1's remembering of ad19b1 against ad19b1's later records.**
flows/6329f1/reports/remember-ad19b1.md line 27 carries "it should be
CAPACITY. and use a key-value map delimiter" as ad19b1's ruling;
ad19b1's later record in the same file, flows/ad19b1/vision/ethos.md
line 26, questions it ("this can only work if the constant
declarations' order doesn't matter … In the key map, the order is not
guaranteed, right?"), and protos.md line 8 drops it. The remembering
was accurate when written and is stale now (inference mine, from the
commit dates in 3.d).

---

## Sources

Every file read by this subflow or by its read subagents, by path.
Files read by this subflow directly are marked (w); files read only
by a subagent and relayed are marked (r).

Distilled and intent:
- /home/li/primary/Vision/protos.md (w)
- /home/li/primary/Vision/ethos.md (w)
- /home/li/primary/Vision/datom.md (w)
- /home/li/primary/Vision/distillation.md (r)
- /home/li/primary/Vision/orchestrate.md (r)
- /home/li/primary/Vision/sources/protos.md (w)
- /home/li/primary/Vision/sources/ethos.md (w)
- /home/li/primary/Vision/sources/datom.md (w)
- /home/li/primary/Vision/sources/distillation.md (w)
- /home/li/primary/Intent/protosParsing.md (r)
- /home/li/primary/Intent/data.md (r)
- /home/li/primary/Intent/mandatoryTraits.md (r)

Flow logs and reports:
- /home/li/primary/flows/e996e8/log.md (w)
- /home/li/primary/flows/6329f1/log.md (w, in part by grep and sed)
- /home/li/primary/flows/6329f1/reports/remember-ad19b1.md (w)
- /home/li/primary/flows/6329f1/reports/psyche-mining.md (w, first 200 lines)

Raw records, flow ad19b1 (w, all):
- /home/li/primary/flows/ad19b1/vision/protos.md
- /home/li/primary/flows/ad19b1/vision/datom.md
- /home/li/primary/flows/ad19b1/vision/ethos.md
- /home/li/primary/flows/ad19b1/vision/archive-kinds.md
- /home/li/primary/flows/ad19b1/vision/archive-meaning.md
- /home/li/primary/flows/ad19b1/vision/designPractice.md
- /home/li/primary/flows/ad19b1/vision/distillation.md
- /home/li/primary/flows/ad19b1/vision/psycheSystem.md

Raw records, flows 6329f1 and e996e8 (w, all):
- /home/li/primary/flows/6329f1/vision/archive-protos.md
- /home/li/primary/flows/6329f1/vision/archive-ethos.md
- /home/li/primary/flows/6329f1/vision/archive-vocabulary.md
- /home/li/primary/flows/e996e8/vision/protos.md
- /home/li/primary/flows/e996e8/vision/ethos.md

Raw records, datom (w unless marked):
- /home/li/primary/vision-raw/archive-datomSyntax.md
- /home/li/primary/flows/a5587095/vision/archive-datomSyntax.md
- /home/li/primary/flows/a5587095/vision/archive-structuredStringType.md
- /home/li/primary/flows/06196cc7/vision/archive-datomSyntax.md
- /home/li/primary/flows/4decf7/vision/archive-datomSyntax.md
- /home/li/primary/flows/5abf3be8/vision/archive-colonLegalInStringPosition.md
- /home/li/primary/flows/01a03eda/vision/archive-datomInteger.md
- /home/li/primary/flows/01a03eda/vision/archive-datomSyntax.md
- /home/li/primary/flows/01a03d6e/vision/archive-dotosFiles.md
- /home/li/primary/flows/01a03d6e/vision/ethosInterfaces.md
- /home/li/primary/flows/ac1e9ec8/vision/datomSyntax.md
- /home/li/primary/flows/ac1e9ec8/vision/datomIsData.md
- /home/li/primary/flows/ac1e9ec8/vision/archive-distillationNegatives.md
- /home/li/primary/flows/ac1e9ec8/vision/datomSkill.md (title only)
- /home/li/primary/flows/ac1e9ec8/vision/distillationNegatives.md (title only)
- /home/li/primary/flows/01a04339/vision/archive-datom.md
- /home/li/primary/flows/4d5fc7da/vision/datom.md
- /home/li/primary/flows/04db2fd2/vision/archive-datomMaps.md
- /home/li/primary/flows/04db2fd2/vision/archive-datomNexus.md
- /home/li/primary/flows/04db2fd2/vision/text.md
- /home/li/primary/flows/04db2fd2/vision/textualTypes.md
- /home/li/primary/flows/04db2fd2/vision/directionAsymmetry.md
- /home/li/primary/flows/e8c4cc61/vision/archive-datomSyntax.md
- /home/li/primary/flows/e8c4cc61/vision/datomizable.md
- /home/li/primary/flows/62022e8f/vision/archive-datomSyntax.md
- /home/li/primary/flows/62022e8f/vision/symbols.md
- /home/li/primary/flows/62022e8f/vision/headedAndContained.md
- /home/li/primary/flows/995a164e/vision/archive-datomSyntax.md
- /home/li/primary/flows/e4a40e/vision/archive-datom.md
- /home/li/primary/flows/e4a40e/vision/archive-vocabulary.md
- /home/li/primary/flows/b675f3d9/vision/structuralParsing.md

Raw records, protos (r unless marked):
- /home/li/primary/flows/a5587095/vision/protosIsTheSharedStyle.md
- /home/li/primary/flows/ba906ae2/vision/protosIsTheSharedStyle.md
- /home/li/primary/flows/2b34fafa/vision/protosIsTheSharedStyle.md
- /home/li/primary/flows/04db2fd2/vision/anatomy.md
- /home/li/primary/flows/04db2fd2/vision/multiPass.md
- /home/li/primary/flows/04db2fd2/vision/portion.md
- /home/li/primary/flows/04db2fd2/vision/delimiters.md
- /home/li/primary/flows/04db2fd2/vision/delineate.md
- /home/li/primary/flows/04db2fd2/vision/text.md
- /home/li/primary/flows/04db2fd2/vision/textualTypes.md
- /home/li/primary/flows/04db2fd2/vision/directionAsymmetry.md
- /home/li/primary/flows/04db2fd2/vision/decomposable.md
- /home/li/primary/flows/04db2fd2/vision/kinds.md
- /home/li/primary/flows/e8c4cc61/vision/protos.md
- /home/li/primary/flows/e4a40e/vision/protos.md
- /home/li/primary/flows/1c282d/vision/protosizable.md
- /home/li/primary/flows/db97561c/vision/prospective.md

Raw records, ethos (r unless marked):
- /home/li/primary/flows/01a02a34/vision/archive-ethos.md
- /home/li/primary/flows/aa4c7747/vision/ethos.md
- /home/li/primary/flows/aa4c7747/vision/ethosTraitSyntax.md
- /home/li/primary/flows/aa4c7747/vision/ethosMonolith.md
- /home/li/primary/flows/aa4c7747/vision/interactions.md
- /home/li/primary/flows/aa4c7747/vision/tuples.md
- /home/li/primary/flows/cff271af/vision/tuples.md
- /home/li/primary/flows/2b34fafa/vision/ethosSourceFiles.md
- /home/li/primary/flows/2b34fafa/vision/ethosNamespaces.md
- /home/li/primary/flows/b675f3d9/vision/kinds.md
- /home/li/primary/flows/b675f3d9/vision/ethosMonolith.md
- /home/li/primary/flows/62022e8f/vision/ethosTypes.md
- /home/li/primary/flows/62022e8f/vision/kinds.md
- /home/li/primary/flows/995a164e/vision/ethosTypes.md
- /home/li/primary/flows/995a164e/vision/kinds.md
- /home/li/primary/flows/2ef42163/vision/ethos.md
- /home/li/primary/flows/2ef42163/vision/kinds.md
- /home/li/primary/flows/e8c4cc61/vision/ethosFileAnatomy.md
- /home/li/primary/flows/e8c4cc61/vision/ethosTypes.md
- /home/li/primary/flows/e8c4cc61/vision/kinds.md
- /home/li/primary/flows/4decf7/vision/archive-kinds.md
- /home/li/primary/flows/e4a40e/vision/archive-kinds.md
- /home/li/primary/flows/5abf3be8/vision/encodedFormFingerprintTraitDesign.md
- /home/li/primary/flows/5abf3be8/vision/sectionsExistToConferTraits.md
- /home/li/primary/flows/5abf3be8/vision/chainedNamesScrapped.md
- /home/li/primary/flows/01a03d6e/vision/ethosInterfaces.md
- /home/li/primary/flows/68512643/vision/negatives.md
- /home/li/primary/flows/d63804f2/vision/newtypeWrappingAndSingleFieldStructs.md
- /home/li/primary/flows/f426777b/vision/ethosSourceFiles.md
- /home/li/primary/flows/06196cc7/vision/traitsAsCapabilities.md
- /home/li/primary/flows/6863ef19/vision/traitsAsCapabilities.md
- /home/li/primary/flows/2b34fafa/vision/traitsAsCapabilities.md

Raw records, vocabulary and secondary (r unless marked):
- /home/li/primary/flows/995a164e/vision/vocabulary.md
- /home/li/primary/flows/2f6b1dc5/vision/vocabulary.md
- /home/li/primary/flows/01a052b6/vision/vocabulary.md
- /home/li/primary/flows/1c282d/vision/vocabulary.md
- /home/li/primary/vision-raw/dictation-vocabulary.md
- /home/li/primary/vision-raw/letsUseTheSameVocabulary.md
- /home/li/primary/vision-raw/protosIsTheSharedStyle.md (title only)
- /home/li/primary/flows/e4a40e/vision/distillation.md
- /home/li/primary/flows/cff271af/vision/distillation.md
- /home/li/primary/flows/a60a9e85/vision/distillation.md
- /home/li/primary/flows/acbb6006/vision/distillation.md
- /home/li/primary/flows/acbb6006/vision/archive-distillation.md
- /home/li/primary/flows/b675f3d9/vision/distillation.md (title only)
- /home/li/primary/flows/b675f3d9/vision/archive-distillation.md
- /home/li/primary/flows/4decf7/design/proposal1/distillation.md
- /home/li/primary/flows/995a164e/vision/designPractice.md
- /home/li/primary/flows/62022e8f/vision/designPractice.md
- /home/li/primary/flows/e8c4cc61/vision/designPractice.md

Code, read with git show at the named revisions (w):
- /git/github.com/LiGoldragon/datomic — src/lib.rs and Cargo.toml at main = origin/main = 4712361c
- /git/github.com/LiGoldragon/protos — src/lib.rs and Cargo.toml at main = 56c683e and origin/main = 48061367

Git commands run in /home/li/primary (w): `git log` on 55554e368,
7d19dcacf, 23aaf7a7f; `git log -- Vision/protos.md`, `-- Vision/ethos.md`,
`-- Vision/datom.md`, `-- flows/ad19b1/vision/{protos,datom,ethos}.md`;
`git show 23aaf7a7f --stat`. Directory listings: flows/*/vision,
flows/*/notion, Vision/, Vision/sources/, Intent/, vision-raw/,
flows/6329f1/{vision,notion,reports}.
