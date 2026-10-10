# Ontology for the meaning language

Delegated by the main flow of f38926 on 2026-09-19 against the living's
ruling: *"Top-level domains, a root of the ontology. We're going to have a
full ontology. This is meaning, so it could mean anything, the whole
universe. Go find the best ontology in the world, and let's put it into a
data shape of enums and structs that have qualities."*
(`flows/f38926/vision/meaningLanguage.md`, read in full, all five entries,
plus `vision/subflows.md`.)

**Marking.** **W** = witnessed at a primary source, cited in `## Sources`.
**R** = relayed: witnessed at source by a named research subflow of this
flow, whose citation is carried. **I** = this flow's inference, not
witnessed.

## Survey

Columns: roots / qualities / time+events / agents+intention / ids / form, size, licence, state.

| Ontology | Top-level roots | Qualities | Time & events | Agents & intention | IDs | Form, size, licence, state |
|---|---|---|---|---|---|---|
| **BFO** ISO 21838-2:2021 **W** | `entity` → `continuant` {independent, specifically dependent, generically dependent} / `occurrent` {process, process boundary, temporal region, spatiotemporal region} **R** | `quality` ⊂ SDC, `inheres in` a bearer; no determinable layer **R** | 3D snapshot+video; CLIF indexes `instance-of` with a time argument, OWL drops it **R** | **none** — no person, agent or intention **R** | opaque `obo/BFO_0000001` **R** | OWL2+CLIF; 36 cls / 40 props; CC BY 4.0; live **R** |
| **DOLCE** ISO 21838-3:2023 **W** | `particular` → endurant / perdurant / quality / abstract **R** | Quality / Quale / Region tripartite — this rose's red ≠ the colour region **R** | 3D; `perdurant` → event {accomplishment, achievement} / stative {state, process} **R** | none in Lite; **DUL** adds Agent, Person, Plan, Goal, Norm, Contract, Right **R** | readable names **R** | OWL2+CL; 37/70 (Lite), ~78 cls (DUL); **licence unstated**; stable since 2003 **R** |
| **TUpper** ISO 21838-4:2023 **W** | no tree — a modular lattice of generic theories (time, process, space) extending PSL **W** | — | process-first (PSL) **W** | — | — | Common Logic; 2023 **W** |
| **SUMO** | `Entity` → Physical {Object, Process, Collection} / Abstract {Quantity, Attribute, SetOrClass, Relation, List, Proposition} **R** | `Attribute` is a top-level root; `attribute` predicate + `MeasureFn` **R** | full Allen interval calculus; `Process` ⊂ Physical **R** | `Human` ⊂ `CognitiveAgent`; believes, knows, desires, wants, prefers, hasPurpose, `Plan` **R** | **bare symbols, no IRIs** **R** | SUO-KIF (HOL); ~20k terms; **IEEE header vs GPL README conflict**; pushed 2026-09-18 **R** |
| **Cyc** | `Thing` → Individual / Collection; microtheories **R** | predicates **R** | temporal things + Mt contexts **R** | richest (modal, scripts, attitudes) **I** | `Mx…` GUIDs (OpenCyc only) **R** | CycL; ~24.5M assertions; **closed** — OpenCyc withdrawn 2017, ResearchCyc unsupported 2019 **R** |
| **GFO** | `Entity` → `Item` {Individual, Category} / `Set` **R** | `Property` + `Property_value` + `Value_space` **R** | time and space are own entities (`Chronoid`, `Topoid`); `Persistant` bridges 3D/4D **R** | no Agent class; `has_agent`, `has_goal` only **R** | readable **R** | OWL DL; 77 cls; FOL unpublished; BSD-style; **frozen 2006/2008, two files disagree** **R** |
| **UFO / gUFO** | `Individual` → Concrete {Endurant {Object, Collective, Quantity, Relator, Mode, Quality}, Perdurant} / Abstract **R** | **best in class**: Quality + quality structure / dimension / quale; `inheresIn` with non-migration; `Relator` as truthmaker **R** | 3D; perdurants modally fragile; gUFO reifies change as `Situation` **R** | **UFO-C is the richest coherent set** — Belief, Desire, Intention, SocialCommitment, Goal, Plan — but **gUFO ships A/B only** **R** | readable `nemo/gufo#` **R** | OWL2 DL; 51 cls / 40 props; CC BY 4.0; live **R** |
| **YAMATO** | no single root; substrate (space, time) vs entity **R** | 4-level: generic quality type / quality role type / quality / quality instance; reconciles BFO, DOLCE, GALEN **R** | process (wholly present, can change) vs event (interval-whole, cannot) **R** | plan content, goal accomplishment **R** | ad hoc **R** | Hozo+OWL; ~500 cls, partly axiomatized; licence unstated; last 2021 **R** |
| **PROTON** | `Entity` → Abstract / `Happening` {Event, Situation, TimeInterval} / `Object` {Agent, Location, Statement} **R** | **none** **R** | `TimeInterval` ⊂ Happening; no calculus **R** | Agent, Person; **no intention at all** **R** | **cleanest**: `ptop:` / `pext:` **R** | OWL; 37+666 cls; CC BY 3.0; **frozen, modules gone from host** **R** |
| **Schema.org** | `Thing` → Action, BioChemEntity, CreativeWork, Event, Intangible, MedicalEntity, Organization, Person, Place, Product, Taxon **R** | properties only; advisory `domainIncludes`/`rangeIncludes` **R** | `Action` with agent/object/instrument/result/start/end + `actionStatus`; 16 Action types **R** | Person, Organization; `potentialAction` the only modality hook **R** | `schema.org/X` **R** | 826 types / 1540 props; v30.1 2026-09-16; CC BY-SA 3.0; live **R** |
| **WordNet / OEWN** | 25 noun + 15 verb unique beginners, all nouns under `entity` **R** | `attribute` is a beginner **R** | `event`, `process`, `act`, `state` are beginners **R** | `person`, `motive`, `feeling`, `cognition` beginners **R** | PWN offsets unstable; OEWN ids + ILI **R/I** | 175,979 synsets (PWN) / 120,068 (OEWN); BSD / CC BY 4.0; OEWN live **R** |
| **FrameNet / VerbNet** | frames; Levin classes **R** | — | FN: Subframe, Precedes, Causative_of. VN: `start/during/end(E)`, subevents e1≺e2≺e3 **R** | frame elements / 23 thematic roles **R** | names **R** | 1,224 frames; VN 274 cls / 5,257 senses; CC BY 3.0 **I**; live |
| **UMR** (AMR, PropBank) | abstract concepts + rolesets **R** | — | **aspect lattice**, 23 values; temporal dependency **R** | modal dependency over *conceivers*; `:modstr` Full/Partial/Neutral × polarity — **epistemic, evidential and deontic collapsed into one scale** **R** | — | guidelines 0.9; open **I**; live **R** |
| **gist** | ~100 plain business classes (Person, Organization, Agreement) **W** | properties **W** | — | Person, Organization **W** | — | OWL; v14.1.0 April 2026; CC BY 4.0; live **W** |
| **Vaiśeṣika** (Kaṇāda, c. 6th–2nd c. BC) | **seven padārthas**: dravya, guṇa, karman, sāmānya, viśeṣa, samavāya, abhāva **W** | **guṇa is itself a root**; 24 enumerated, including desire, aversion, effort, cognition **W** | kāla and dik are two of nine dravyas; karman is a root **W** | ātman and manas are dravyas; intention is guṇa inhering in ātman **W** | — | natural language; public domain **I** |

Of the four ISO-ratified top-level ontologies only BFO and DOLCE are categorial
trees; TUpper is deliberately a modular lattice (**W**). A comparative survey
(Trojahn, Vieira, Schmidt, Pease, Guizzardi, *Semantic Web* 2022) records BFO
as stridently realist, SUMO and DOLCE as admitting a subjective standpoint, and
DOLCE as lacking SUMO's process-type hierarchy, organisms, units and event
roles (**W**). BFO has the largest install base, through OBO Foundry and IOF
(**R**).

## Judgment and forks

**No single existing ontology is the base.** Each candidate fails on a
different axis of what the living asked for. BFO is the most authoritative and
the smallest — and has no person, no agent, no intention (**R**). UFO has the
best quality theory and the only coherent typed Belief/Desire/Intention set —
but its shipped OWL omits exactly that fragment (**R**), and it is not ISO.
SUMO has breadth, attitudes and a live repo — with no IRIs at all and an
unresolved IEEE-vs-GPL licence conflict (**R**). Cyc, the largest, is
unobtainable (**R**); PROTON and GFO are frozen (**R**). Schema.org and gist are
practical but shallow; WordNet, FrameNet and VerbNet are lexical, not
categorial. UMR is the closest *shape* to what is wanted — typed concepts plus
aspect, person and number as gracefully-degrading lattices — but it collapses
epistemic certainty, evidentiality and deontic force into one three-valued
scale (**R**), which is precisely the collapse a language carrying intention
must not make.

**What the survey did find.** The four-category spine on which BFO, DOLCE, GFO
and UFO all converge — substance, quality inhering in substance, process,
universal — is a rediscovery of the Vaiśeṣika padārthas (**I**, from **W** on
both sides). And Vaiśeṣika does natively what every Western top-level ontology
defers to an extension: **guṇa is a root category, and desire (icchā), aversion
(dveṣa), effort (prayatna) and cognition (buddhi) are among its 24 enumerated
qualities, inhering in ātman** (**W**). Intention is not bolted on; it is a
quality of a self. Samavāya is BFO's `inheres in` and UFO's `inheresIn`,
promoted to a root (**I**).

This matters because the living has already ruled the verb layer: Pāṇini's
Aṣṭādhyāyī is named as *"the base for everything: how our system thinks,
communicates, and classifies things in the world"*
(`flows/5851f4/vision/ashtadhyayiKnowledgeBase.md`, **W**). The Pāṇinian verb
supplies, as productive stackable operators on the root, what no ontology
carries: desiderative = intention, causative = causation, gerundive =
obligation, intensive = iteration, denominative = act-as/seek (**R**). The six
kārakas are a semantic role layer held apart from surface case, with voice
(prayoga) as a presentational projection over a fixed role assignment (**R**) —
the exact stratification a typed language wants.

**This flow's recommendation, for the living to rule on.** Take the root enum
from Vaiśeṣika's seven padārthas, dual-named against BFO/UFO so every root
carries an outbound mapping; take the quality theory from UFO (quality /
dimension / quale) filled with the 24 guṇas as the opening enum; take the verb
system whole from Pāṇini; take nothing wholesale from BFO, SUMO or Cyc — map to
them, import nothing. Identity is the living's checksum, never a borrowed IRI;
a borrowed IRI is an annotation on a meaning, not the meaning's name.

**The forks, plainly.**

1. **Whose names are the roots?** (a) Vaiśeṣika Sanskrit — coherent with the
   Pāṇinian verb already ruled, and it makes quality and intention roots rather
   than extensions; interop by mapping. (b) BFO's ISO names —
   `continuant`/`occurrent` — buying interop and a standard, at the cost of no
   native agent, no intention, and a vocabulary at odds with the verb layer.
   (c) Both, dual-named on every root. This flow leans (a) with (c)'s mapping
   table. The living's call.

2. **"Top-level domains" — categories or subject areas?** The phrase reads two
   ways: *ontological categories* (what kind of thing this is — substance,
   quality, motion), seven of them; or *subject domains* (what this is about —
   person, artifact, communication, cognition), WordNet's 25 or Schema.org's 11
   (**I** on the ambiguity). They are orthogonal and the language may want both
   axes. The sketch takes the categorial reading.

3. **How much content is imported?** (a) Root skeleton only, growing the rest
   natively from use. (b) Import a whole tree — SUMO's 20k terms, OEWN's 120k
   synsets — as the initial lexicon. (a) keeps the language small and owned;
   (b) makes it immediately broad but inherits a licence (SUMO's is in
   conflict) and another project's decisions.

4. **Does intention type separately from certainty?** UMR collapses epistemic,
   evidential and deontic into one scale (**R**); Sanskrit keeps them in
   distinct morphology — liṭ marks *unwitnessed* past, the gerundive marks
   obligation, the desiderative marks want (**R**). Keeping them apart costs
   more enums and buys the distinction the living named.

## Data shape sketch

Ethos syntax per the `ethos` skill: `Name.Type` alias, `Name.{ }` struct,
`Name.[ ]` enum; fields are named after their types in snake case, so a role
name must be carried by an alias (`Bearer.Link`, not a bare `Link` field).
A `Library` in sweet form, sections `imports types kinds associations`.

```
Library
[ datom-codec:Meaning ]
[ ; --- the root enum: the top-level domains ------------------------
  Root.[ Substance.Substance      ; dravya
         Quality.Quality          ; guṇa
         Motion.Motion            ; karman
         Universal.Universal      ; sāmānya
         Particular.Particular    ; viśeṣa
         Inherence.Inherence      ; samavāya
         Absence.Absence ]        ; abhāva

  ; --- three levels beneath one root ------------------------------
  Substance.[ Material.MaterialSubstance  Immaterial.ImmaterialSubstance ]
  MaterialSubstance.[ Object.Object  Aggregate.Vector<Bearer>  FiatPart.Bearer ]
  Object.[ Organism.Organism  Artifact.Artifact  Portion.Bearer  Feature.Bearer ]
  Organism.[ Person  Animal  Plant  Microbe ]
  ImmaterialSubstance.[ Space  Time  Ether  Self  Mind  Site.Bearer ]

  ; --- how a Quality attaches to a thing --------------------------
  Quality.{ QualityKind Bearer Quale }          ; inherence is the struct itself
  QualityKind.[ Colour Taste Smell Touch Number Magnitude Separateness
                Conjunction Disjunction Priority Posteriority
                Cognition Pleasure Pain Desire Aversion Effort
                Heaviness Fluidity Viscosity Merit Demerit Sound Disposition ]
  Quale.[ Word.String  Count.Integer  Amount.Decimal
          Point.Dimension  Opaque.Meaning ]
  Dimension.{ QualityKind Decimal }

  ; --- the content-addressed link ---------------------------------
  Link.{ Checksum Option<Locator> }             ; checksum over content and its links
  Checksum.String
  Locator.String                                ; index hint, built on demand
  Bearer.Link
  Target.Link
  Filler.Link

  ; --- the verb: Pāṇini's categories ------------------------------
  Act.{ Dhatu Stem Lakara Prayoga Purusha Vachana Linga Vector<Karaka> }
  Dhatu.String                                  ; verbal root, opaque for now
  Stem.[ Primary Causative Desiderative Intensive Denominative ]
  Lakara.[ Lat Lit Lut Lrt Let Lot Lan VidhiLin AshirLin Lun Lrn ]
  Prayoga.[ Kartari Karmani Bhave ]
  Purusha.[ Prathama Madhyama Uttama ]
  Vachana.[ Eka Dvi Bahu ]
  Linga.[ Pum Stri Napumsaka ]
  Karaka.{ KarakaRole Filler }
  KarakaRole.[ Kartr Karman Karana Sampradana Apadana Adhikarana ]

  ; --- statement, annotation, utterance ---------------------------
  Statement.{ Act Vector<Link> }                ; subparts by link, not by nesting
  Annotation.{ Target Note }
  Note.[ Prose.Meaning  Formal.Statement ]
  Utterance.[ Single.Statement  Series.Vector<Statement> ] ]
[]
[]
```

Two things Ethos cannot express here, said plainly. **(1)** It has no
indirection, so a directly recursive `Statement` holding a `Statement` would
need a Rust `Box`. The sketch does not need one: subparts are reached by
content-addressed `Link`, which is what the living ruled anyway — recursion
through the store, not through the struct. **(2)** `Stem` is drawn as a flat
enum, but Sanskrit stems *compose* (the desiderative of a causative, **R**).
Composition wants `Vector<StemOperator>`, and whether order is significant is
an open question for the living. Also noted: Ethos names a field from its type,
so role-carrying aliases (`Bearer`, `Target`, `Filler`) are load-bearing, not
decoration.

**One datom text example** — an `Annotation`, whose `Target` is a statement
already in the store and whose `Note` is prose. Positions walk the type:
`Target` (`Checksum`, `Option<Locator>`), then `Note` as a variant.

```
{ { 7ae4c0b93f1d2e58 Some.idx-meaning-2026-09 }
  Prose.(the desiderative here reads as imminence, not as want) }
```

And the statement it points at — "he wishes to know it" — `Statement`:
`Act` (`Dhatu`, `Stem`, `Lakara`, `Prayoga`, `Purusha`, `Vachana`, `Linga`,
`Vector<Karaka>`), then `Vector<Link>` of subparts:

```
{ { jñā Desiderative Lat Kartari Prathama Eka Pum
    [ { Kartr { 9f2c71a4b5e60d13 None } }
      { Karman { 3bd08e15c7a24f90 None } } ] }
  [] }
```

## Unknowns

- Whether "top-level domains" means categories or subject areas — fork 2. Not
  resolvable from the record; the living must say.
- Whether the meaning language wants the Vaiśeṣika roots at all, or whether
  the Pāṇini ruling was about the *verb* only. Both readings fit the record.
- What the checksum covers exactly. The living said "all of its content and all
  of its links" — whether that is the rkyv archive (the Nexus rule: an encoded
  form fingerprints itself by the hash of its rkyv archive) or the datom text
  is undecided here.
- Whether `Meaning` stays an opaque parenthesized string once the verb set
  lands, or is replaced by `Statement`. Today `Meaning` is `String` in
  datom-codec (**W**, `tools/messaging-codec/vendor/datom-codec/`).
- Sanskrit liṅga (gender) is grammatical, not biological. The living named
  "gender" among the verb's relations; whether the type means grammatical
  concord or something about persons is not settled.
- FrameNet's licence and current counts could not be confirmed at source — its
  site now serves only a JS shell (**R**). WordNet's ILI id scheme was inferred,
  not witnessed (**R**).
- Whether any of this should be *imported* rather than *mapped to*. This flow
  recommends mapping only; it is fork 3 and not this flow's to decide.

## Sources

Read 2026-09-19 by this flow (**W**):

- https://en.wikipedia.org/wiki/ISO/IEC_21838 — parts 1–4, Part 1 conformance requirements (OWL 2 direct semantics *and* a Common Logic axiomatization per ISO/IEC 24707)
- https://www.iso.org/standard/78927.html, https://www.iso.org/standard/74572.html, https://www.iso.org/standard/78928.html (via search metadata; iso.org returns 403 to direct fetch) — 21838-2:2021 BFO, -3:2023 DOLCE, -4:2023 TUpper
- https://journals.sagepub.com/doi/abs/10.3233/AO-220263 — Grüninger, Ru, Thai, *TUpper: A top level ontology within standards*, Applied Ontology 17(1), 2022; modular "sideways" approach extending PSL
- https://en.wikipedia.org/wiki/Vaisheshika — seven padārthas, nine dravyas, 24 guṇas (17 original + 7 added by Praśastapāda), samavāya, Kaṇāda c. 6th–2nd c. BC
- https://www.wisdomlib.org/hinduism/book/a-history-of-indian-philosophy-volume-1/d/doc209816.html — Dasgupta on the six padārthas
- https://www.semanticarts.com/gist/ — gist v14.1.0 (April 2026), ~100 classes, CC BY 4.0
- https://www.semantic-web-journal.net/system/files/swj2650.pdf — Trojahn, Vieira, Schmidt, Pease, Guizzardi, *Foundational ontologies meet ontology matching: A survey*, Semantic Web 2022
- Repository, read directly: `flows/f38926/vision/meaningLanguage.md`, `flows/f38926/vision/subflows.md`, `flows/5851f4/vision/ashtadhyayiKnowledgeBase.md`, `flows/5851f4/vision/anatomyOfCommunicatingThinkingAndReacting.md`, `flows/b81560/vision/operational-meaningLanguageLogographic.md`, `flows/b81560/vision/operational-meaningGarbageCollectionAndOntology.md`, `vision-raw/worldModelBeforeCode.md`, `tools/messaging-codec/vendor/datom-codec/` (`Meaning` is `String`; `Form::Meaning(Opaque)`)

Relayed (**R**) — witnessed at source by three research subflows of this flow,
which carried these citations (one line per system; each subflow's full list is
in its return):

- **BFO** `raw.githubusercontent.com/BFO-ontology/BFO-2020/master/21838-2/owl/bfo-core.ttl` (hierarchy, 36 cls / 40 props, CC BY 4.0) + that repo's `21838-2/common-logic/` release notes 2025-12-07 (ternary `instance-of`); `bfo-ontology.github.io`; `obofoundry.org/ontology/bfo.html`; `spec.industrialontologies.org/iof/ontology/core/Core/`
- **DOLCE** `loa.istc.cnr.it/dolce/overview.html` (OWL drops modality and temporal indexing); `loa.istc.cnr.it/ontologies/DOLCE-Lite.owl`; `ontologydesignpatterns.org/ont/dul/DUL.owl` (DUL 4.2)
- **GFO** `onto-med.de/ontologies/gfo` + `gfo.owl` + `gfo-basic.owl`
- **UFO** `inf.ufes.br/~gguizzardi/Applied_Ontology__UFO__Unified_Foundational_Ontology.pdf` (axioms a7–a14, a34–a43, a65–a67, a83–a89); `nemo-ufes.github.io/gufo/` + `gufo.ttl`; `arxiv.org/html/2603.20948v1`; `dev.nemo.inf.ufes.br/seon/UFO.html`
- **SUMO** `raw.githubusercontent.com/ontologyportal/sumo/master/Merge.kif` (IEEE licence header) + `Mid-level-ontology.kif` + `WordNetMappings30-noun.txt`; `github.com/ontologyportal/sumo` (GPL README); `api.github.com/repos/ontologyportal/sumo`
- **Cyc** `en.wikipedia.org/wiki/Cyc`, `/CycL`; `cyc.com`; `mkbergman.com/2034/fare-thee-well-opencyc/`; `opencyc-2012-05-10-readable.owl.gz`
- **YAMATO** `hozo.jp/onto_library/AO-YAMATO_final.pdf`, `YAMATO101216.pdf`, `upperOnto.htm`
- **PROTON** `ontotext.com/proton/protontop.rdf`, `protonext.rdf` (v3.0, CC BY 3.0 in `dc:rights`)
- **Schema.org** `schema.org/Thing`, `/Action`, `/docs/schemas.html`, `/docs/releases.html`, `/docs/terms.html`
- **WordNet** `en.wikipedia.org/wiki/WordNet`; `en-word.net`; `manpages.ubuntu.com/manpages/bionic/man5/lexnames.5WN.html` (45 lexicographer files)
- **FrameNet / VerbNet / PropBank** `en.wikipedia.org/wiki/FrameNet`; `verbs.colorado.edu/verbnet/`; `aclanthology.org/W19-3318/` (Brown et al. 2019, subevents); `propbank.github.io`
- **UMR** `raw.githubusercontent.com/umr4nlp/umr-guidelines/master/guidelines.md` (0.9 — aspect §3-3-1, ref-person/number §3-3-5, modstr §4-3-1-1, modal dependency §4-3)
- **Sanskrit** `en.wikisource.org/wiki/Sanskrit_Grammar_(Whitney)` §§528–541, 952–994, 998–1063; `learnsanskrit.org/vyakarana/tinanta/lakara/` (ten lakāras with sūtras); `learnsanskrit.org/vyakarana/subanta-1/karaka/` (six kārakas, A. 1.4.24/32/42/45/49/54); `learnsanskrit.org/guide/verbs-1/karmani-and-bhave-prayoga/`
- **ISO-TimeML / OntoNotes** `en.wikipedia.org/wiki/ISO-TimeML`; `catalog.ldc.upenn.edu/LDC2013T19`
