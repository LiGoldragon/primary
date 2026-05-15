# 167 — Theoretical literature for a universal verb model

*Designer research-survey report, 2026-05-14. Surveys the major
theoretical frameworks that propose a universal classification of
verbs across natural language — Sanskrit grammar (Pāṇini's kāraka /
dhātupāṭha / lakāra; Bhartṛhari's kriyā-sphoṭa; Mīmāṃsā's vidhi;
Nyāya; Buddhist arthakriyā), Aristotle's categories, Halliday's
process types, Tesnière's valency, Austin/Searle's illocutionary
forces, Vendler's aspectual classes, Levin's alternation classes, and
the cognitive-semantic decomposition frameworks (Schank, Wierzbicka,
Jackendoff, Talmy). Synthesizes what every tradition agrees on, what
no tradition agrees on, and bears the findings against Persona's
six-verb Signal spine.*

**Retires when**: the survey's findings are absorbed into a decision
about Persona's verb-spine (either ratified or revised), or another
designer report supersedes this one with a deeper synthesis.

---

## 0 · TL;DR

**Every tradition I surveyed treats the verb as the structural and
semantic core of the proposition.** Sanskrit grammarians, Aristotle,
contemporary functional linguistics, speech act theory, and cognitive
semantics all converge on this. **No tradition agrees on the exact
cardinality of a closed universal verb-set.** The closed-set
cardinalities proposed across the literature range from 4 (Vendler)
through 5 (Searle's illocutionary types) through 6 (Halliday's
process types, Pāṇini's kāraka roles) through 10 (Pāṇini's dhātupāṭha
gaṇas, Pāṇini's lakāra moods) through 11 (Schank's CD primitives) up
to ~17 verbal primes within Wierzbicka's 65-prime NSM and ~50 verb
classes in Levin's English verb alternations.

Crucially, **the closed-set claims classify along different axes**.
They are not competing answers to one question; they answer different
questions:

| Axis | Question | Example frameworks | Typical cardinality |
|---|---|---|---|
| **Process type** | What kind of act is happening? | Halliday's process types, Searle's illocutionary forces | 5–6 |
| **Argument structure / role** | How does the act bind to its participants? | Pāṇini's kāraka, Tesnière's valency, Levin's alternations | 6 roles; 0–3 actants; ~50 alternation classes |
| **Aspectual / temporal contour** | How does the act unfold over time? | Vendler's classes, Pāṇini's lakāra | 4 (aspectual); 10 (tense-mood) |
| **Decompositional primitive** | Of what semantic atoms is the verb made? | Schank's CD, Wierzbicka's NSM, Jackendoff's primitives | 8–17 |
| **Force-dynamics** | What forces interact? | Talmy | small closed set of patterns |
| **Morphological class** | What is the verb's formal behaviour? | Pāṇini's dhātupāṭha gaṇas | 10 |

Persona's six-verb Signal spine (`Assert`, `Mutate`, `Retract`,
`Match`, `Subscribe`, `Validate`, per `/166`) sits on the **process
type axis** — it classifies *what kind of boundary act* is happening.
This puts it in the same family as Halliday's six process types and
Searle's five illocutionary forces. **It does not contradict** the
other axes (kāraka, valency, aspect, decomposition); those classify
different things.

**Chat-surfaced observations** (the points needing your attention):

1. **The closest theoretical neighbour to Persona's spine is
   Halliday's six process types** (`material`, `mental`, `relational`,
   `behavioral`, `verbal`, `existential`). Halliday's claim is
   explicitly universalist for the three major types
   (material/mental/relational) and weaker for the three boundary
   types (behavioral/verbal/existential). The six-with-three-boundaries
   structure has a stronger universality argument than Persona's flat
   six.

2. **The Sanskrit tradition is more rigorous than its modern reception
   credits**. Pāṇini gives *three* closed sets at three layers
   (6 kāraka roles + 10 dhātu morphological classes + 10 lakāra
   tense/mood frames) plus a fourfold word-type classification
   (jāti/dravya/guṇa/kriyā). The pattern of *multi-axis closure* is
   the deeper Sanskrit lesson, not any single number. The persona
   spine names one axis; the Sanskrit precedent suggests naming
   multiple axes explicitly.

3. **No closed verbal-prime set proposed by any framework is genuinely
   universal**. NSM's 65 primes are the most-tested cross-linguistic
   claim; even there, expansion from 14 (1972) → 65 (current) shows
   the closure is empirical, not deductive. Schank's 11 CD primitives
   have never been independently validated cross-linguistically.
   Halliday acknowledges minor types vary across languages. **The
   workspace's seven (now six) is a database-operation closure, not a
   natural-language-meaning closure**; the universality argument has
   to lean on the *boundary-act-kind* dimension, not on
   meaning-decomposition.

4. **Vendler's aspectual classification (states / activities /
   accomplishments / achievements) cuts across Persona's spine
   orthogonally**. Persona's `Subscribe` is durative-stative;
   `Assert`/`Mutate`/`Retract` are punctual-telic; `Match` is
   durative-telic; `Validate` is hypothetical-perfective. The
   aspectual structure is *implicit* in each verb's payload but not
   surfaced. If Persona's spine grows to expose aspect explicitly,
   Vendler is the canonical frame.

5. **The verb-centric stemma (Tesnière)** maps directly onto the
   Persona protocol: every Signal frame has one verb-tagged operation
   (the stemma root) plus zero or more participants (the typed payload
   plus the implicit reply). This isn't a coincidence — Tesnière's
   structural-syntax tradition is the lineage Signal's frame shape
   honors.

---

## 1 · What "universal verb model" means in the literature

Two senses of "universal" appear, and they're often conflated:

- **Cross-linguistic universality** — every human language has verbs
  fitting this classification. Empirical claim; falsifiable by finding
  a language whose verbs don't fit. Wierzbicka's NSM, Halliday's
  process types, Searle's illocutionary forces all make this kind of
  claim with varying degrees of evidence.
- **Combinatorial universality** — every verb-meaning decomposes into
  combinations of these primitives. Generative claim. Schank's CD,
  Wierzbicka's NSM, Jackendoff's conceptual primitives all make this
  claim.

The two are connected but separable. A classification can be
cross-linguistically universal without being combinatorially
universal (e.g., Halliday's process types are types of *clause*, not
decomposition primitives). A classification can be combinatorially
universal in principle without being cross-linguistically validated
(e.g., Schank's 11 ACTs).

Persona's six-verb spine is **a database-operation closure**, not
either of the above. The universality claim Persona makes is
**bounded-domain**: across *every component contract in the
workspace*, every boundary act fits one of the six. This is a
narrower claim than cross-linguistic universality but a stronger one
than "useful in practice" — it's a *closed-set decision* enforceable
by `signal-core::SignalVerb`'s match-exhaustiveness.

---

## 2 · The Sanskrit grammar tradition

The Sanskrit tradition develops the most multi-layered closed-set
classifications of verbs found in any tradition. Pāṇini's
*Aṣṭādhyāyī* (c. 5th century BCE) gives three orthogonal closed sets;
Bhartṛhari's *Vākyapadīya* (c. 5th century CE) makes kriyā (verbal
action) the temporal axis of the entire sentence; Mīmāṃsā treats
every verb as fundamentally an injunction; Nyāya treats kriyā as the
relational hub.

### 2.1 · Pāṇini's three closed sets

#### Kāraka — six syntactic-semantic roles around kriyā

| Kāraka | Gloss | Semantic role | Default case |
|---|---|---|---|
| `kartṛ` | agent | the one who performs the action | nominative |
| `karman` | patient/object | what is most-affected by the action | accusative |
| `karaṇa` | instrument | the means by which the action is performed | instrumental |
| `sampradāna` | recipient | the one for whom the action is done | dative |
| `apādāna` | source | that from which something separates | ablative |
| `adhikaraṇa` | locus | the place/time/context of the action | locative |

The kāraka system is **not** modern thematic-role theory (agent /
patient / instrument), though it overlaps. It's a closed set of
semantic functions, each potentially mapping to multiple syntactic
realizations. Pāṇini sets these as the **arguments of the verb**
(kriyā) — sentence meaning is the verb plus its kārakas. The system
is anchored at sūtras 1.4.23–1.4.51 of the Aṣṭādhyāyī.

Cross-linguistic claim: the kāraka system has been argued by Cardona,
Kiparsky, and Bhate-Kak as a universal semantic-role inventory; this
is contested. The kāraka *roles* may be universal even if their
*case-mapping* is Sanskrit-specific. **Persona's elementary verbs do
not map onto kārakas** — kāraka classifies *participants of an
action*, not *kinds of action*. The two axes are orthogonal.

#### Dhātupāṭha — ten morphological classes of verb roots

Pāṇini classifies ~2000 verb roots (dhātu) into 10 morphological
classes (gaṇa). The classes are named after their first root:

| # | Name | Stem-formation | Example root |
|---|---|---|---|
| 1 | bhvādi | thematic -a- (~50% of roots) | bhū "be" |
| 2 | adādi | athematic, no formant | ad "eat" |
| 3 | juhotyādi | athematic, reduplication | hu "offer" |
| 4 | divādi | thematic -ya- | div "shine" |
| 5 | svādi | athematic -nu- | su "press" |
| 6 | tudādi | thematic -a-, ending accent | tud "push" |
| 7 | rudhādi | athematic nasal infix | rudh "obstruct" |
| 8 | tanādi | athematic -o- | tan "stretch" |
| 9 | kryādi | athematic -nā- | krī "buy" |
| 10 | curādi | thematic -aya- (causative) | cur "steal" |

The classification is primarily **morphological** (how the verb forms
its stem), but the morphology is grounded in inherited
Proto-Indo-European stem-formation patterns. The 10 classes are
**not** semantic categories — they describe how verb roots conjugate,
not what they mean.

Cross-linguistic claim: the *morphological* classification doesn't
generalize. The *typological observation* — that verb-stem formation
varies along a thematic/athematic axis with sub-patterns — is more
defensible.

#### Lakāra — ten tense/mood frames

Pāṇini gives **ten lakāra** (named after the affix-letters they take):

| Lakāra | Function | Modern equivalent |
|---|---|---|
| `laṭ` | present tense | present indicative |
| `liṭ` | parokṣa-bhūta (remote past) | perfect |
| `luṭ` | bhaviṣyat (periphrastic future) | future |
| `lṛṭ` | bhaviṣyat (simple future) | future |
| `leṭ` | Vedic subjunctive (lost in Classical) | subjunctive |
| `loṭ` | imperative | imperative |
| `laṅ` | bhūta (past) | imperfect |
| `liṅ` | optative + benedictive | optative |
| `luṅ` | bhūta (aorist) | aorist |
| `lṛṅ` | conditional | conditional |

This is a **closed set of tense-mood frames** — every Sanskrit verb,
in every utterance, takes exactly one lakāra. The mood lakāras
(loṭ imperative, liṅ optative, leṭ subjunctive) carry the
illocutionary force. The Mīmāṃsā philosophical school (next section)
argues that the optative liṅ is the *fundamental* lakāra — every
Vedic sentence is at its core an injunction.

Cross-linguistic claim: every language has finite tense and mood
distinctions, but the *number* and *boundaries* of categories vary.
The 10 lakāra is Sanskrit-specific in detail but a partial reflex of
Proto-Indo-European tense-mood architecture.

### 2.2 · Bhartṛhari — kriyā as the temporal axis of the sentence

Bhartṛhari's *Vākyapadīya* (c. 5th century CE) develops the
**sphoṭa** theory: a sentence is a single indivisible meaning-burst
(sphoṭa), and the verb (kriyā) is its temporal axis. Without the
verb, no sentence exists; a sentence is a kriyā unfolding in time
(per Coward, *The Sphoṭa Theory of Language*, pp. 122–123, 128–129).

The key asymmetry: a noun uttered alone is incomplete and requires an
implicit verbal action to acquire sentence-meaning; a verb uttered
alone is *itself* a complete (if minimal) sentence. **The verb is
sentence-complete; the noun is not.** This is Bhartṛhari's deepest
universality claim — across all languages, the verb is the
sentence-completing element.

Sphoṭa theory also gives the four levels of speech: parā (transcendent),
paśyantī (intuitive), madhyamā (mental), vaikharī (articulated). The
verb's unfolding in time (kālaśakti — "power of time") is what produces
the four-level differentiation from the unified sphoṭa.

Bhartṛhari's universalism is more about **the role of verbs in
language** than about a specific closed set of verbs. Per Coward:
Bhartṛhari proposes universal principles of how meaning operates
(whole before parts, sphoṭa-based cognition), but the grammatical
apparatus (kāraka, dhātu) stays Sanskrit-specific.

### 2.3 · Mīmāṃsā — verb as cosmic injunction (vidhi)

The Mīmāṃsā school (Kumārila Bhaṭṭa, Prabhākara Miśra; c. 6th–8th
centuries CE) argues that every Vedic sentence is at its core an
**injunction** (vidhi). The prototypical verb form is *yajeta* "one
should sacrifice" — the optative. **The verb in the optative carries
the cosmic ordering force; all other verb-forms are derivative.**

Mīmāṃsā does not give a closed set of verbs but rather argues that
*one type of speech act is fundamental*. This is closer to Searle's
project (a closed taxonomy of speech-act types) than to Pāṇini's
(closed sets of forms). It's the strongest claim in the literature
that *one verb-type is privileged* — the injunctive — even though
Mīmāṃsā doesn't generalize this beyond Vedic discourse.

Mīmāṃsā also develops **svatah-prāmāṇya** — the doctrine that
verbal cognition (śabda-bodha) arising from injunctive sentences is
intrinsically valid unless defeated by a counter-condition. The
universality claim is *epistemic* (about how verb-mediated knowledge
works), not *taxonomic* (about a closed verb-set).

(Per Matilal, *Logic, Language and Reality*, pp. 204–210.)

### 2.4 · Nyāya — kriyā as relational hub

The Nyāya school takes kriyā (verbal action) as the **central
relational element** that binds substance (dravya, the chief
qualificand) to its qualities, instruments, and effects via the six
kārakas. Where Pāṇini's kāraka system is morphosyntactic, Nyāya's
treatment is **ontological** — kriyā is a relator, not a substance.

Nyāya's analysis of the sentence *harir vihagaṃ paśyati* ("Hari sees
a bird") gives the verbal cognition as: *vihaga-karmaka-darśanānukūla-
kṛti-mān hariḥ* — "Hari is qualified by the effort generating the
activity-of-seeing that has a bird as object." **Hari (substance) is
primary; kriyā is the qualifier.** This is the inverse of
Bhartṛhari's grammarian view, where kriyā is the chief qualificand.

(Per Matilal, pp. 390–415.) Jagadīśa's fourfold word-classification
(jāti, dravya, guṇa, kriyā — i.e., class-character, substance,
quality, action) places kriyā as **one of four word-types**, not as
the sentence-axis. This is the most explicit closed-set word-class
proposal in the Indian tradition, though Jagadīśa himself notes its
incompleteness (e.g., negative-existential words like *mūka* "mute"
fit none of the four).

### 2.5 · Buddhist — kṣaṇika kriyā and arthakriyā

Dignāga and Dharmakīrti (Sautrāntika and Yogācāra schools, c.
5th–7th centuries CE) treat verbs as naming **kṣaṇika** (momentary)
events. The Buddhist universality claim is *ontological*: nothing
persists; "things" are conceptual constructions over event-streams.
Verbs are more honest than nouns about this momentariness.

The key technical concept is **arthakriyā** — causal efficacy. A
cognition is valid (pramāṇa) iff it leads to successful arthakriyā
("getting at the object's efficacy"). The verb-form is the cognitive
honest-form; the noun-form is the convenient-fiction-form. This is
the deepest universality claim in the Buddhist tradition: **verbs
fit reality more honestly than nouns do**.

The claim doesn't generate a closed set of verbs but does generate a
*priority ordering*: verbs over nouns, processes over substances,
events over things. This is congenial to a verb-centric protocol
design.

---

## 3 · The Greek tradition

### 3.1 · Aristotle's poiein and paskhein

Aristotle's *Categories* (c. 350 BCE) gives **ten categories** of
things that can be said: substance (ousia), quantity (poson),
quality (poion), relation (pros ti), place (pou), time (pote),
position (keisthai), state (echein), action (poiein), and passion
(paskhein).

**Two of the ten — action (poiein) and passion (paskhein) — are
verb-shaped.** Action is the doing; passion is the suffering of
something done. Aristotle gives the canonical examples:
*cuts/burns* (action) and *is cut/is burned* (passion). These are
distinguished from substance (man, horse) and qualities (white, hot).

Aristotle's claim is **ontological**, not lexical: the ten categories
are the ten kinds of *predication* that can apply to a substance. The
verb-shaped categories (action, passion) are **two of ten** —
suggesting that *what verbs do* is one specific kind of predicate
function, not the entirety of language.

The action/passion split tracks the **active/passive voice**
distinction modern grammar inherits. In Tesnière's later framework
(§4.2) this becomes the diathesis transformation — the same verb can
be active or passive without changing its valency.

The Aristotelian framework was decisive for Western scholastic and
modern grammar but is not itself a *universal verb classification* —
the verb is one slot in a larger ontological partition. Aristotle
does not propose a closed set of verbs as such.

---

## 4 · The 20th-century linguistic frameworks

### 4.1 · Halliday's six process types

M.A.K. Halliday's Systemic Functional Linguistics (*Introduction to
Functional Grammar*, 4th ed., Ch. 5) proposes **six process types**
that exhaust the transitivity system of every human language:

| Process | Domain | Exemplar verbs | Participants |
|---|---|---|---|
| `material` | doing, happening — outer experience, energy → change | do, make, happen, fall, rule, create | Actor + Goal (+ Range, Beneficiary) |
| `mental` | sensing, thinking — inner experience, consciousness | hate, like, fear, want, believe, know | Senser + Phenomenon |
| `relational` | being, having — abstract relations | be, have, seem, become, belong to | Carrier+Attribute, or Token+Value |
| `behavioral` | physiological/psychological behavior, mediates material+mental | laugh, breathe, cough, smile, dream, sleep | Behaver (+ Range) |
| `verbal` | saying — symbolic relations | say, tell, reply, write, express | Sayer + Verbiage (+ Receiver, Target) |
| `existential` | existing/occurring | be, exist, occur, happen | Existent |

**The structure is not flat**. Halliday explicitly argues (p. 216)
that the six form a **closed loop** organized like a color wheel:
three major types (material, mental, relational) sit at the corners
of a triangle; three boundary types (behavioral, verbal, existential)
sit at the edges between the majors. *Behavioral* mediates material
↔ mental; *verbal* mediates mental ↔ relational; *existential*
mediates relational ↔ material.

> "It does not matter where we move in. They are ordered; and what is
> important is that our model of experience is one of regions within a
> continuous space; the continuity is not between two poles, it is
> round in a loop." — Halliday, IFG p. 217

Universality claim: the **three major types are proposed universal**;
the three boundary types vary across languages (existential clauses
may merge with locative or possessive in some languages; behavioral
may collapse into material). This is the strongest contemporary
universality claim in the universal-verb-classification literature.

Boundary tests Halliday uses to distinguish the types:

- Material vs Mental: Actor need not be conscious; Senser must be.
- Mental vs Relational: Mental can project quotes/reports (*I think
  that...*); Relational cannot.
- Material vs Behavioral: Behavioral Behaver is conscious like
  Senser; process is material-like.
- Verbal vs Mental: Sayer need not be conscious (institutions, signs
  can be Sayers).
- Present-tense diagnostic: Material/Behavioral take present-in-
  present (*is doing*); Mental/Relational take simple present
  (*knows*, *is*).

**This is the most direct theoretical neighbour to Persona's six-verb
spine.** Persona's six (Assert/Mutate/Retract/Match/Subscribe/Validate)
classify *boundary acts of meaning* between component daemons;
Halliday's six (material/mental/relational/behavioral/verbal/existential)
classify *acts of meaning* in human language. Both are six. Both are
closed. Both are organized by topology (Halliday explicitly; Persona's
seven-planet bijection in `/162` implicitly).

### 4.2 · Tesnière's verb-centric stemma and valency

Lucien Tesnière's *Éléments de syntaxe structurale* (1959, posthumous)
founded dependency grammar with the thesis that **the verb is the
structural center of every sentence**. Around the verb stand the
"actants" (arguments) and "circumstants" (adjuncts). The sentence
forms a **stemma** (dependency tree) with the verb at the root.

Tesnière's central image (Ch. 48): *"The verbal node, found at the
centre of the majority of European languages, is a theatrical
performance. Like a drama, it obligatorily involves a process and most
often actors and circumstances."*

#### Valency — verbs classified by number of obligatory actants

| Valency | Term | Example |
|---|---|---|
| 0 | avalent | "It rains" (no actants — only the process) |
| 1 | monovalent | "Alfred falls" |
| 2 | divalent | "Alfred hits Bernard" |
| 3 | trivalent | "Alfred gives the book to Charles" |

#### Diathesis — five voice transformations preserving valency

Active / Passive / Reflexive / Reciprocal / Causative (factitive).
Each transforms the surface arrangement of actants without changing
the verb's underlying valency.

#### Four nucleus types

Sentences organize around four kinds of structural nuclei (verbal,
nominal, adjectival, adverbial), with the **verbal nucleus primary**.

Universality claim: Tesnière argues that **verb centrality is
universal** across the languages he surveyed (Indo-European, Slavic,
several Asian languages). Valency is universal even when the surface
realization (case endings vs. prepositions vs. position) varies. The
actant/circumstant boundary is universal.

The Tesnière framework maps onto Persona's protocol with surprising
fidelity:

| Tesnière | Persona / Signal |
|---|---|
| Verb at stemma root | `SignalVerb` at Operation root |
| Actants (obligatory) | Typed payload fields |
| Circumstants (optional) | Implicit context (origin, time, etc.) |
| Diathesis transformations | Active CLI (`mind '(Assert ...)'`) → daemon reply pair |
| Avalent / mono / di / tri | Payload field count |

This isn't a coincidence — modern dependency grammar (which descends
from Tesnière) is the same conceptual lineage as typed-record wire
protocols. The verb is structurally primary; everything else is
dependent.

### 4.3 · Searle's five illocutionary forces

J.L. Austin (*How to Do Things with Words*, 1962) distinguished three
levels of speech act:

- **Locutionary** — the act of producing meaningful utterance
- **Illocutionary** — the act performed *in* saying (promising,
  commanding, asserting)
- **Perlocutionary** — the effect produced *by* saying (persuading,
  frightening)

Austin's original five illocutionary classes: verdictives, exercitives,
commissives, behabitives, expositives.

John Searle revised this in "A Taxonomy of Illocutionary Acts" (1975)
to **five categories organized by direction of fit**:

| Category | Direction of fit | Example verbs | Psychological state |
|---|---|---|---|
| **Assertives** | word-to-world | state, claim, deny, predict, describe | belief |
| **Directives** | world-to-word | command, request, advise, ask | want |
| **Commissives** | world-to-word | promise, vow, threaten, bet | intention |
| **Expressives** | null (presupposes) | thank, apologize, congratulate | various affective |
| **Declarations** | both / null | "I now pronounce...", "you're fired" | none |

Searle and Vanderveken extended this in *Foundations of Illocutionary
Logic* (1985) to a seven-component force-vector
(illocutionary-point + strength + mode + content + preparatory +
sincerity + sincerity-strength).

**The Searle universality debate is unresolved.** Wikipedia/SEP both
note: *"nothing rules out the possibility of there being illocutionary
acts that are not named by a verb either in a particular language such
as Swahili or Bengali, or indeed in any language at all."* The
taxonomy describes **possible** forces; the lexical realization is
language-specific.

Persona's `Assert` lines up with Searle's *assertive*; `Validate`
with no clear single counterpart (it's a "dry-run assert"); `Retract`
with no Searle counterpart (Searle has no closing-of-an-assertion
verb-class).

### 4.4 · Vendler's four aspectual classes

Zeno Vendler (*Verbs and Times*, 1957) classified English verbs by
their **aspectual contour** — how the event they describe unfolds in
time:

| Class | Telic? | Durative? | Dynamic? | Examples |
|---|---|---|---|---|
| **States** | no | yes | no | know, love, own, believe |
| **Activities** | no | yes | yes | run, walk, swim, push |
| **Accomplishments** | yes | yes | yes | build a house, draw a circle |
| **Achievements** | yes | no (punctual) | yes | recognize, find, arrive, die |

Diagnostic tests:
- Progressive form: *is V-ing*. Accepted by activities and
  accomplishments; rejected by states (with exceptions) and
  achievements.
- "For X time" / "in X time": activities accept *for*; accomplishments
  accept *in* (also *for*); achievements accept neither cleanly.
- "Stop V-ing" entailment: differs across classes.
- "It took an hour to V": works for accomplishments, not states or
  achievements.

Comrie added **semelfactives** (punctual atelic — *cough*, *blink*) as
a fifth class. Smith, Krifka, Dowty extended the diagnostics.

Universality: the four-way classification has been argued
cross-linguistically robust (Smith 1991), though languages encode
aspect with different lexical and grammatical means. The four classes
themselves seem language-universal; how each language marks them
varies.

**Mapping to Persona**:

| Persona verb | Vendler class |
|---|---|
| `Assert` / `Mutate` / `Retract` | achievement (punctual, telic) |
| `Match` | accomplishment (durative, telic) — query starts, returns finite reply |
| `Subscribe` | activity / state — ongoing stream, atelic |
| `Validate` | hypothetical-perfective (no Vendler class for dry-run; closest is achievement) |

The Vendler classification cuts across Persona's spine **orthogonally**.
This is not a competing axis — it's a different question, and Persona
could *additionally* tag each verb with its Vendler class if aspect
became load-bearing.

### 4.5 · Levin's verb classes

Beth Levin's *English Verb Classes and Alternations* (1993) gives a
much more granular classification: ~50 verb classes for English,
organized by their behavior under syntactic alternations (the dative
alternation, the causative-inchoative, the locative alternation,
etc.). The thesis: **a verb's meaning is largely predictable from its
alternation behavior**.

Major class groupings include: verbs of putting, removing,
sending/carrying, throwing, transfer-of-possession, exerting force,
killing, contact-by-impact, change-of-state, motion, image-creation,
emission, change-of-possession, communication, perception, body
function, …

Levin's classification is **English-specific in detail** but the
underlying claim — verb meaning is grounded in alternation behavior —
is proposed cross-linguistically (with VerbNet, FrameNet, and PropBank
extending the project). The size of the class space (~50) is much
larger than Halliday's 6 or Searle's 5 because Levin classifies along
*argument-structure-with-alternations*, not along
*kind-of-process*. The two axes are orthogonal: a single Hallidayan
process type (e.g., material) subdivides into many Levin classes
(putting, removing, throwing, exerting force, …).

**This is the granularity Persona doesn't have and probably doesn't
need.** A workspace verb-spine that classifies at Halliday's
cardinality (6) covers boundary acts; Levin-level granularity (50+)
would be the *payload* type system, not the verb spine.

---

## 5 · Cognitive-semantic decomposition frameworks

These frameworks attempt to *decompose* verb meanings into
combinations of universal primitives — a more ambitious claim than
classifying verbs into types.

### 5.1 · Schank's Conceptual Dependency — eleven primitive ACTs

Roger Schank's *Conceptual Dependency theory* (1972, 1975) proposes
**eleven primitive ACTs** to which any verb in any language
decomposes:

| ACT | Meaning | Decomposes (example) |
|---|---|---|
| `PTRANS` | physical transfer | *go, send, deliver* |
| `ATRANS` | abstract transfer (possession) | *give, take, sell, buy* |
| `MTRANS` | mental transfer (information) | *tell, hear, read, listen* |
| `PROPEL` | applying force | *push, kick, throw, hit* |
| `MOVE` | body-part movement | *raise hand, kick (foot)* |
| `GRASP` | grasping with body part | *hold, clutch, grab* |
| `INGEST` | taking into body | *eat, drink, breathe in* |
| `EXPEL` | expelling from body | *spit, cry, vomit* |
| `MBUILD` | mental construction | *think, conclude, decide* |
| `SPEAK` | producing vocal sound | *say, shout, whisper* |
| `ATTEND` | focusing a sensor | *see, hear, smell, look* |

Each ACT has a conceptual structure with slots (actor, object,
direction, source, instrument, etc.). Complex verbs decompose to
combinations: *eat* = INGEST + MOVE-(hand) + GRASP-(food); *teach* =
MTRANS + (causation) + (recipient-MBUILDs).

Universality claim: Schank explicitly proposed CD as a
*language-independent* representation. The claim was never
independently validated cross-linguistically; CD remained an AI/NLP
internal formalism rather than a linguistic theory. Successors
include Jackendoff's conceptual semantics and FrameNet.

### 5.2 · Wierzbicka's NSM — sixty-five semantic primes

Anna Wierzbicka and Cliff Goddard's Natural Semantic Metalanguage
(NSM, 1972 → present) proposes **65 universal semantic primes** that
combine via universal syntactic frames to express any meaning in any
language. The current list includes ~17 verbal/predicate primes:

**Mental predicates** (7): think, know, want, don't-want, feel, see,
hear

**Speech** (1): say

**Actions/events/movement** (3): do, happen, move

**Existence/possession** (3): be-(somewhere), there-is,
be-(someone/something)

**Life/death** (2): live, die

**Physical contact** (1): touch

Plus auxiliaries / modals (can, like, ...) that act as
predicate-modifiers in some analyses.

Methodology: Wierzbicka and Goddard's 1994 and 2002 cross-linguistic
studies surveyed 16+ language families and argued each prime is
**translatable literally** into every language tested. Semantic
**explications** are constructed from these primes (e.g., *broke* =
"this thing did something to that thing; because of this, the other
thing happened; this other thing was not like before"). Semantic
**molecules** bridge primes to complex concepts.

This is the **most thoroughly empirically defended universal verb-set
claim in the literature**. Even so, the expansion from 14 (1972) → 60
(2002) → 65 (current) shows the closure is *empirically discovered*,
not deductively given. Critiques: NSM's exponents are polysemous in
every language; the claim that *one sense* of each is universal
requires careful metalinguistic discipline. NSM has not converged on
a generative theory of how arbitrary verb meanings decompose, only on
explication-by-paraphrase for each studied case.

**Mapping to Persona**: NSM's `do` and `happen` cover everything in
Persona's spine. NSM's `say` covers the entire Signal protocol. NSM's
universalism is **too coarse** to inform a workspace's database-op
verb spine — but it confirms that *some closed verbal-prime set is
defensible* across languages.

### 5.3 · Jackendoff's Conceptual Semantics

Ray Jackendoff (*Semantics and Cognition*, 1983; *Semantic
Structures*, 1990; *Foundations of Language*, 2002) gives a
decompositional framework with:

- **Ontological categories**: EVENT, STATE, ACTION, THING, PLACE,
  PATH, PROPERTY, AMOUNT
- **Function primitives**: GO (motion), BE (location/identity), STAY
  (continuation), CAUSE, LET, ORIENT, EXT (extent), INCH (inchoative),
  PERF (perfective)

The primitives combine via a **Conceptual Structure** layer that
mediates between syntax and broader cognition. A sentence like *John
went to the store* decomposes to GO([THING JOHN], [PATH TO [PLACE
STORE]]); *John pushed the cart to the store* decomposes to CAUSE([JOHN],
GO([CART], TO [STORE])).

Universality claim: Jackendoff proposes Conceptual Structure as a
*universal cognitive substrate* — every language maps its surface
forms onto the same conceptual primitives. The empirical support is
substantial for spatial/motion verbs; the framework has been less
rigorously tested on speech-act, mental, or social verbs.

### 5.4 · Talmy's force-dynamics

Leonard Talmy's *Toward a Cognitive Semantics* (2000) develops
**force-dynamics** — verbs (especially modals and causatives) encode
interactions between two force-entities:

- **Agonist** — the focal force entity, with an intrinsic tendency
  (action or rest)
- **Antagonist** — the opposing force entity

Combinations produce a small closed set of force-dynamic patterns:
extended causation (Antagonist stronger), onset causation (new
Antagonist), blocking, removal of blocking, helping, hindering, etc.

Modals are analyzed as force-dynamic patterns: *must* (strong
Antagonist blocking action), *can* (Agonist overcoming resistance),
*may* (permitted action).

Universality claim: force-dynamics is proposed as a **closed-class
grammatical category** comparable to number and aspect — universally
encoded across human languages, though with different surface
realizations.

Force-dynamics is **the most general** of the cognitive-semantic
frameworks here, in that it abstracts above specific verb meanings to
the *causal/permissive/preventive structure* of any verbal event.
Jackendoff's CAUSE/LET primitives are a special case.

---

## 6 · Synthesis

### 6.1 · Two orthogonal axes are at play

The frameworks above don't compete for "the right cardinality of
verbs." They classify along orthogonal axes:

```
                        ┌─ Process type / illocutionary force
                        │  (Halliday 6, Searle 5, Mīmāṃsā vidhi)
        WHAT KIND ──────┤
                        │  ↘ Aspectual contour
                        │     (Vendler 4, Pāṇini lakāra 10)
                        │
                        └─ Force-dynamic role
                           (Talmy: small closed set)

                        ┌─ Argument structure / kāraka
                        │  (Pāṇini's 6 roles; Tesnière 0–3 actants)
        WHAT BINDS ─────┤
                        │  ↘ Alternation behaviour
                        │     (Levin ~50 English classes)
                        │
                        └─ Word-type within sentence
                           (Jagadīśa 4: jāti/dravya/guṇa/kriyā)

                        ┌─ Mental/action/movement primitives
        WHAT ATOMS ─────┤  (Schank 11, Wierzbicka ~17 verbal)
                        │
                        └─ Conceptual-structure primitives
                           (Jackendoff: GO/BE/STAY/CAUSE/LET)

                        ┌─ Morphological class
        HOW FORMED ─────┤  (Pāṇini's 10 gaṇa)
                        │
                        └─ Voice / diathesis
                           (Tesnière 5: active/passive/reflexive/reciprocal/causative)
```

A complete account of any verb covers all four columns: what kind of
act, what it binds to, what atoms compose it, how the form is built.

### 6.2 · Cardinality table

| Framework | Axis | Closed-set size |
|---|---|---|
| Vendler aspect | aspectual contour | 4 (states / activities / accomplishments / achievements) |
| Searle illocutionary | speech-act type | 5 |
| Austin illocutionary | speech-act type | 5 |
| Halliday process | clause type | 6 (3 major + 3 boundary) |
| Pāṇini kāraka | argument role | 6 |
| Persona signal | database boundary act | 6 elementary (per `/166`) or 7 (current) |
| Jackendoff function primitives | conceptual primitive | ~9 (GO/BE/STAY/CAUSE/LET/ORIENT/EXT/INCH/PERF) |
| Pāṇini dhātupāṭha | morphological class | 10 |
| Pāṇini lakāra | tense/mood | 10 |
| Schank CD | action primitive | 11 |
| Wierzbicka NSM | verbal/predicate prime | ~17 (within 65 total) |
| Levin verb classes | English alternation class | ~50 |

**Patterns**:

- The "kinds of act" axis cluster around 4–7 closed categories. This
  is the **only stable cardinality** in the literature.
- The "argument structure" axis ranges from 3 (Tesnière nucleus types
  + 1 nucleus type) to 6 (kāraka) — also small.
- The "decomposition primitives" axis ranges from ~9 (Jackendoff) to
  ~17 (NSM verbal subset) — moderate.
- The "morphology" axis is 10 in Sanskrit; varies elsewhere.
- The "Levin-style argument-structure-with-alternations" axis is much
  bigger (~50). This is the payload-type granularity, not a closed
  verbal-act set.

### 6.3 · What every tradition agrees on

1. **The verb is the sentence-axis**. Sanskrit grammarians
   (Bhartṛhari's kriyā as sentence-complete; Nyāya's kriyā as
   relational hub), Tesnière (verbal nucleus at stemma root),
   Halliday (process at the heart of the clause), Buddhist
   philosophy (verb-form is ontologically honest), Austin/Searle
   (illocutionary force is the act-of-saying) all agree. No
   tradition gives an alternative center.

2. **A small closed set of *kinds of act* covers the act-of-language
   space**. Halliday's 6, Searle's 5, Persona's 6/7 — all converge in
   the cardinality range 4–7. This is the only stable cardinality
   across traditions.

3. **Verbs bind to a small closed set of *roles***. Pāṇini's 6
   kāraka, Tesnière's 0–3 actants — small closed inventories for
   participant-roles. Modern thematic-role theory (agent / patient /
   instrument / recipient / source / location) often gets to 6, the
   same as kāraka.

4. **Verbs have temporal contour**. Vendler's 4, Pāṇini's 10 lakāra,
   the universal presence of aspect in all known languages.

5. **Verb-as-event is more honest than verb-as-substance**. The
   Buddhist arthakriyā argument, Davidsonian event semantics in
   modern logic, NSM's `happen` prime. Processes get priority over
   things.

### 6.4 · What no tradition agrees on

1. **The exact cardinality of any axis**. Even on the most-stable
   "kinds of act" axis, Halliday says 6, Searle says 5, Vendler says
   4, Persona says 6/7. The cardinality is *task-dependent*.

2. **Whether a finite decomposition basis exists**. NSM argues yes;
   Schank's CD argues yes; both have empirical issues. No framework
   has produced a *deductive* universal verb-set; all are *discovered
   empirically*.

3. **Which axis is primary**. Pāṇini gives multi-axis closure (kāraka
   for roles + dhātupāṭha for morphology + lakāra for tense-mood, all
   simultaneously). Modern frameworks tend to pick one axis. The
   Sanskrit precedent suggests **all axes should be named explicitly**
   — no single number captures the verb's structure.

4. **Whether verbal meaning is genuinely universal or
   culture-specific**. Wierzbicka argues universal; later work
   (Levinson, Evans, Majid) argues for substantial semantic
   diversity. Cross-linguistic surveys keep finding more variation
   than NSM's exponents allow.

---

## 7 · Bearing on Persona's Signal verb spine

The current Persona spine (6 elementary verbs per `/166`'s collapse
proposal: `Assert`, `Mutate`, `Retract`, `Match`, `Subscribe`,
`Validate`) sits on the "kinds of act" axis — same axis as Halliday
and Searle. The choice is sound on this axis.

The Sanskrit precedent suggests Persona should consider naming
*multiple* axes explicitly:

1. **Process-type axis** — already named: `SignalVerb` (6 elementary).
2. **Role / argument-structure axis** — the typed payload fields
   serve this implicitly; making them explicit (à la kāraka) would
   give every variant a closed role-vocabulary.
3. **Aspectual axis** — implicit in payload semantics; not surfaced.
   Could be added if subscribe-vs-one-shot semantics need to be
   declarative.
4. **Diathesis axis** — request/reply pairing handles most of this;
   active/passive transformations don't apply naturally to a
   database protocol.

The Halliday-loop structure (3 major + 3 boundary types) is more
universal than a flat six. If Persona ever revisits the verb-spine
naming, the loop structure is worth considering:

```
Possible Halliday-style loop for Persona:

       Assert ─────────── Subscribe
       (durable        (durable stream
        write)          out)
        │                    │
        │ Mutate              │ Match
        │ (transition)        │ (read once)
        │                    │
        │                    │
       Retract ─────────── Validate
       (withdraw)        (dry-run)
```

This isn't a recommendation, just a possibility. The current
flat-spine is fine for the database-operation domain; the loop
structure would matter only if Persona's spine evolves toward
human-act-of-language territory.

The seven-planet bijection (`/162`) maps onto the verb-spine well at
six (per `/166`'s observation that Jupiter is structurally the binding
relation, not a peer act). The astrological-correspondence reading is
*observational*, not generative — same status as Wierzbicka's NSM
universality (observed across many languages, never deductively
derived).

---

## 8 · Open questions for the user

These are research-shaped questions, not implementation-shaped.

### Q1 — Is the spine genuinely multi-axis, or single-axis?

The literature suggests **multi-axis closure is more robust than
single-axis closure** (Pāṇini's pattern). Persona's current
SignalVerb classifies only the "kind of boundary act" axis. Should
the protocol explicitly name *additional* closed sets (e.g., a
kāraka-style role vocabulary for payload fields; a Vendler-style
aspect annotation per variant)?

This question is research-orientation, not blocking. A
single-axis spine is fine if you're OK leaving the other axes
implicit in payload semantics.

### Q2 — How seriously do you take the cross-linguistic universality argument?

Persona's spine is *workspace-bounded* (database operations between
component daemons). The literature on cross-linguistic universality
(Wierzbicka, Halliday) addresses a much harder claim (every human
language, every act of meaning). You don't *need* cross-linguistic
universality for the workspace's purposes — but the planet-bijection
narrative in `/162` reaches for it.

Decision: do you want the spine to *aim* at cross-linguistic
universality (the Halliday/Wierzbicka tradition), or stay
deliberately bounded (database-op closure only)? The former is
ambitious; the latter is honest about scope.

### Q3 — Are Halliday's process types the right neighbour for Persona?

If Persona's spine is on the "kind of act" axis, Halliday's six is
the strongest theoretical anchor. Should `/162` be revised to cite
Halliday alongside the seven-planet bijection? The Halliday lineage
is more academically defensible than the astrological correspondence,
though the latter has narrative weight.

### Q4 — Where does aspect live?

Vendler-style aspectual classification (state vs activity vs
accomplishment vs achievement) is **orthogonal** to Persona's
verb-spine but maps cleanly onto it. Today aspect is implicit in
each verb's payload shape (`Match` = accomplishment because it
returns finite reply; `Subscribe` = activity because it streams).
Should aspect be surfaced explicitly — e.g., a typed
`AspectualContour` annotation on each variant?

Probably no — adding aspect orthogonal-axis would double the type
system surface. But noting *where* aspect lives in the design
(implicit in payload semantics) is worth recording.

---

## 9 · Sources

In-library (full extraction performed by parallel research agents):

- **M.A.K. Halliday & Christian Matthiessen**, *Introduction to
  Functional Grammar* (4th ed., 2014), Chapter 5 "Clause as
  Representation" — Halliday's six process types with full
  treatment of participant roles, boundary tests, and topology.
  `/git/github.com/LiGoldragon/library/en/michael-halliday/introduction-to-functional-grammar.pdf`
- **Lucien Tesnière**, *Elements of Structural Syntax* (1959, trans.
  Osborne & Kahane 2015), Chapters 47–57, 97–108 — the verbal
  stemma, valency classification, diathesis transformations.
  `/git/github.com/LiGoldragon/library/en/lucien-tesniere/elements-of-structural-syntax.pdf`
- **Bimal Krishna Matilal**, *Logic, Language and Reality: An
  Introduction to Indian Philosophical Studies* — Mīmāṃsā
  authority + sentence definition (pp. 204–210); Bhartṛhari on
  substance/quality (pp. 379–388); Nyāya kāraka theory and
  śābda-bodha (pp. 390–415); Jagadīśa's fourfold classification
  (pp. 390–397).
  `/git/github.com/LiGoldragon/library/en/bimal-matilal/logic-language-reality.pdf`
- **Harold G. Coward**, *The Sphoṭa Theory of Language: A
  Philosophical Analysis* — sphoṭa as eternal meaning-whole,
  kriyā as sentence-axis, Bhartṛhari's universalism caveat,
  kāla-śakti.
  `/git/github.com/LiGoldragon/library/en/harold-coward/sphota-theory-of-language.pdf`
- **Rishi A. Rajpopat**, *In Pāṇini We Trust* — confirmed *not* a
  source for systematic Pāṇini verb-system extraction (rule-conflict
  meta-grammar focus); listed for completeness.
  `/git/github.com/LiGoldragon/library/en/rishi-rajpopat/in-panini-we-trust.pdf`
- **Aristotle**, *Categories* (Edghill trans., Project Gutenberg) —
  ten categories with action (poiein) and passion (paskhein).
  `/git/github.com/LiGoldragon/library/en/aristotle/categories-edghill-gutenberg.epub`
- **Bhartṛhari**, *Vākyapadīya* — text image-only OCR-unfriendly;
  consulted through Coward and Matilal.
  `/git/github.com/LiGoldragon/library/en/bhartrhari/vakyapadiya.pdf`
- **Mīmāṃsā Sūtras** (Jaimini, Jha trans.); **Nyāya Sūtras** (Gotama,
  Vidyābhūṣaṇa trans.) — primary sources for the school
  positions; consulted through Matilal.

External (Wikipedia / Stanford Encyclopedia of Philosophy):

- **Sanskrit verbs** (Wikipedia) — the 10 gaṇa morphological
  classes, 10 lakāra tense-mood frames, ātmanepada / parasmaipada
  voice system.
- **Natural Semantic Metalanguage** (Wikipedia) — Wierzbicka's
  full 65 primes, methodology, expansion history.
- **Speech Acts** (Stanford Encyclopedia of Philosophy) — Austin's
  five categories, Searle's revision with direction of fit,
  Vanderveken's seven-component force vector, Sbisà and current
  debates.
- **Force dynamics** (Wikipedia) — Talmy's Agonist/Antagonist
  framework, modal verb analysis.
- **Conceptual semantics** (Wikipedia) — Jackendoff's framework
  (limited Wikipedia coverage; the substance is in Jackendoff
  1990, 2002).
- **Conceptual dependency theory** (Wikipedia) — Schank's primitive
  ACTs (limited Wikipedia coverage; full eleven from secondary
  knowledge of Schank 1972, 1975).
- **Illocutionary act** (Wikipedia) — Searle's five categories
  (brief).

Not yet acquired (worth getting if this line is to be pursued):

- **Anna Wierzbicka**, *Semantic Primitives* (1972) and *English
  Speech Act Verbs: A Semantic Dictionary* (1987) — the seminal
  closed-set proposal for English speech-act verbs.
- **Cliff Goddard**, *Semantic Analysis: A Practical Introduction*
  (2011) — the contemporary NSM textbook.
- **Roger Schank**, *Conceptual Information Processing* (1975) — the
  full CD theory.
- **Ray Jackendoff**, *Semantic Structures* (1990) — the full
  conceptual-semantics framework.
- **Beth Levin**, *English Verb Classes and Alternations* (1993) —
  the ~50-class alternation-based classification.
- **Zeno Vendler**, "Verbs and Times" (*The Philosophical Review*,
  1957) — the original aspectual-class paper.
- **Leonard Talmy**, *Toward a Cognitive Semantics* (2 vols., 2000)
  — the full force-dynamics + lexicalization-patterns framework.
- **George Cardona**, *Pāṇini: A Survey of Research* (1976) — the
  modern systematic survey of Pāṇinian verb-system scholarship.
- **Hartmut Scharfe**, *Grammatical Literature* (1977) — the
  standard reference for the Sanskrit grammatical tradition.

Companion designer reports:

- `~/primary/reports/designer/162-signal-verb-roots-synthesis.md` —
  the prior synthesis (seven-verb spine, seven-planet bijection).
  This report's `/162 §4` open question on the eighth verb is
  closed by `/163`; the present report's bearing on `/162` is in
  §7 above.
- `~/primary/reports/designer/163-seven-verbs-no-structure-eighth.md`
  — adoption of the seven-only direction (later collapsed to six per
  `/172`; the schema-as-data containment rule survives intact).
