# Vocabulary of the conversion chain: ontology and etymology

Flow 564f55. Research delegated by the main flow, 2026-09-09.

The chain being named:

```
text  <->  protoform  <->  datom  <->  <the Rust value>        (currently: corpus)
(glyph stream) (structure, (the dialect's   (what the program
               no meaning)  concept)         computes with)

beside it: Signal — the rkyv zero-copy archived binary, readable in
memory without decoding, used on the wire between components.
```

Wanted: a noun for the Rust-value layer that says **what the information IS
there**; and positive names for **both directions**, not negations like
`deserialize`. Kinds are `-able` adjectives (`Textualizable`, `Datomizable`),
never verbs.

Throughout, **witnessed** marks something read in a source or in this
codebase, with the source named. **Claim** marks an inference or a reading
that the source does not itself state.

---

## 0. What this codebase already says

Witnessed, by grep over `/git/github.com/LiGoldragon` on 2026-09-09.

`protos/src/kinds.rs`, `protos/protos-kinds.ethos`, `protos/README.md`:

| capability | kind | goes to |
|---|---|---|
| `protosize` | `Protosizable` | Protoform |
| `conceive` | `Conceivable<C>` | Concept |
| `incorporate` | `Incorporable<T>` | Corporate |
| `actualize` | `Actualizable<T>` | Corporate (the whole descent) |
| `textualize` | `Textualizable` | Text |
| `situate` | `Situating` | Text |

`protos/src/lib.rs`: "Four layers: Text, Protoform, Concept, Corporate. Text
arrives as a `Potential` value and descends — protosize, conceive,
incorporate — and may fault on the way; a corporate value ascends —
conceive, protosize, textualize — and cannot."

`protos/src/anatomy.rs:216`: `Potential<T, C>` is documented as "Text that may
become a `T` through the concept `C`: potential until it matches its anatomy."

**Two findings that bear directly on the psyche's question.**

1. **The potency/act frame is already load-bearing, and it already has its
   contrast term.** The psyche's worry was that "actual … sounds like we're
   contrasting it with something that isn't actual, which is kind of
   confusing." Witnessed: that contrast is not accidental, it is the design.
   `Potential<T, C>` *is* the not-yet-actual, and it is a real type in the
   crate. So `actualize` is coherent with what is already there. The open
   question is narrower than it looked: it is about the **layer noun**
   (`Corporate`/`corpus`), not about the descent verb `actualize`.

2. **`native` is already claimed, by Signal.** Witnessed,
   `signal/README.md:7`: "Signal is the **native binary form** of the records
   criome holds: sema is by definition computer-cognizable, so its native form
   is binary." Naming the Rust-value layer `Native` would collide head-on with
   the one neighbouring component that already uses the word for itself, and
   would do so at exactly the point in the chain where the two meet. This is a
   strong argument against `native`, and it was not visible from the
   conversation alone.

Name availability, witnessed by grep: `Native` and `Corpus` are unused as type
or trait names anywhere in `protos`, `datom-codec`, `ethos-zero`, `datom`.
`Corporate` is used, but only as a `Fault` variant
(`datom-codec/src/anatomy.rs:229`), not as a layer type. `Incorporable` exists
in `protos/src/kinds.rs` and is exported, but is **not** declared in
`protos-kinds.ethos` — it is listed there only in a comment as one of the
kinds with no Declaration form.

`ethos-zero/README.md` already names a pass **"datomization"**, so
`Datomizable` is continuous with existing usage.

---

## 1. Etymology and original technical sense

### serialize / deserialize

- **Etymology** (witnessed, [etymonline](https://www.etymonline.com/word/serialize),
  [series](https://www.etymonline.com/word/series)): Latin *series* "row,
  chain" ← *serere* "to join, link". English *serialize* 1852, "publish in
  installments".
- **Original technical sense.** Two homonyms, and the older one is not ours.
  The concurrency/database sense — force operations into an order equivalent
  to some serial execution — is IBM OS/360 mid-1960s and is made formal in
  Eswaran, Gray, Lorie & Traiger, *CACM* 19(11), 1976
  ([ACM](https://dl.acm.org/doi/10.1145/360363.360369)). The object-graph
  sense is much later: the earliest dated use the research found is **MFC 1.0,
  March 1992**, `CObject::Serialize(CArchive&)`
  ([Microsoft](https://learn.microsoft.com/en-us/cpp/mfc/serialization-in-mfc)),
  then Sun's *Java Object Serialization Specification*, JDK 1.1, 1997
  ([spec](https://docs.oracle.com/en/java/javase/21/docs/specs/serialization/)).
  Earlier systems used other words entirely: NeXTSTEP 1988 "archiving",
  Modula-3 1992 "pickle".
- **What it literally claims:** *to lay out as one chain*. Nothing more. It
  claims linearization and only linearization.
- **Honest for us** on the ascent to text: text really is a single ordered
  chain, and that is exactly what `Textualizable` produces.
- **Misleads for us** in three ways. (a) `de-` is a negation, which the psyche
  has ruled out. (b) It names only the *shape of the output* (a chain), so it
  says nothing about the layer it came from — it cannot distinguish our four
  layers, which is why serde needs one flat pair where we need several. (c)
  The concurrency homonym is older and still live.

**Claim.** Serde's pair is not a good abstraction to port, and the reason is
structural, not aesthetic: serde has *two* layers (Rust value, wire) and so
needs one pair of names. Our chain has four, and each crossing is a different
crossing. The psyche's instinct that "maybe the abstraction of serde doesn't
fit our level of abstraction" is confirmed by the etymology: `serialize` names
an output shape, not a crossing.

### marshal / unmarshal

- **Etymology** (witnessed,
  [etymonline](https://www.etymonline.com/word/marshal)): Old High German
  *marahscalc* "horse-servant" → Old French *mareschal* "stable officer" →
  "commander who arrays troops".
- **Original technical sense** (witnessed): **Bruce Jay Nelson, *Remote
  Procedure Call*, Xerox PARC CSL-81-9, May 1981**, §5.4.3 "Marshaling
  Parameters"
  ([bitsavers](https://archive.org/stream/bitsavers_xeroxparctoteProcedureCall_14151614/CSL-81-9_Remote_Procedure_Call_djvu.txt)).
  Then Xerox Courier, Dec 1981; Birrell & Nelson, *ACM TOCS* 2(1), 1984: "the
  client stub marshals the parameters into one or more network messages"
  ([PDF](https://web.eecs.umich.edu/~mosharaf/Readings/RPC.pdf)).
- **What it literally claims:** *to muster scattered items into formation
  ready to march*. Arrangement for movement, with the stub as the officer.
- **Honest** about the wire: it is about transport, and it presumes a
  destination.
- **Misleads for us:** it says nothing about representation change, only about
  ordering for a journey. And `un-` is a negation.

### pickle

- **Etymology** (witnessed,
  [etymonline](https://www.etymonline.com/word/pickle)): Middle Dutch *pekel*
  "brine"; verb 1550s "preserve in brine".
- **Original technical sense** (witnessed): **Modula-3 `Pickle` interface, DEC
  SRC, 1992** — "a representation of a Modula-3 value as a stream of bytes
  that preserves value, shape and sharing"
  ([Purdue mirror](https://www.cs.purdue.edu/homes/hosking/m3/help/gen_html/libm3/src/pickle/ver1/Pickle.i3.html)).
  Python's `pickle` first shipped in **Python 1.2, 13 April 1995**
  (CPython `Misc/HISTORY`).
- **What it literally claims:** *preservation against time*. The thing is put
  in brine so it can be eaten later.
- **Misleads for us** entirely: our chain is not about durability. Nothing in
  it is preserved against time; text is a *form*, not a larder.

### hydrate / dehydrate

- **Etymology:** Greek *hydōr* "water".
- **Original technical sense:** the research **could not find a primary dated
  source**. Secondary sources attribute the ORM sense to Hibernate; Microsoft
  MTS/COM+ "dehydrate/rehydrate" (late 1990s) is often cited as parallel but
  no primary was retrieved.
- **What it literally claims:** the object's *structure* exists dry and inert,
  and data is the water that makes it live.
- **Misleads for us** badly, and instructively: it presumes the shape
  pre-exists the content and only needs filling. Our protoform is the
  opposite — structure is *found in* the text, not waiting to be filled.

### materialize

- **Etymology** (witnessed,
  [etymonline](https://www.etymonline.com/word/materialize)): 1710 "represent
  as material"; **1866 "appear in bodily form", from spiritualism** — a séance
  word.
- **Original technical sense** (witnessed): Adiba & Lindsay 1980 called the
  thing a "snapshot"; the phrase "materialized view" is established without
  introduction by **Blakeley, Larson & Tompa, SIGMOD 1986**
  ([ACM](https://dl.acm.org/doi/10.1145/16856.16861)). First coinage
  unresolved.
- **What it literally claims:** a *definition* is given *matter* — an
  intension acquires stored extension.
- **Honest** for a cached view. **Misleads for us:** it claims the thing was
  previously immaterial, which is false of text; text is the most material
  thing in our chain. The spiritualist origin is not incidental — the word
  carries "appears out of nothing".

### reify

- **Etymology** (witnessed, [etymonline](https://www.etymonline.com/word/reify)):
  *reification* 1846, *reify* 1854; Latin *res* "thing" + *-ficare* "to make".
- **Original technical sense** (witnessed): Marx's *Verdinglichung*, then
  Lukács 1923
  ([marxists.org](https://www.marxists.org/archive/lukacs/works/history/hcc05.htm));
  in CS via Brian Cantwell Smith's procedural reflection (MIT 1982), and Cliff
  Jones's VDM "data reification" — abstract type to concrete representation
  with a retrieve function
  ([VDM](https://homepages.cs.ncl.ac.uk/cliff.jones/publications/Books/vdm_tn.pdf)).
- **What it literally claims:** something that was a relation or an
  abstraction is *made into a thing that can be pointed at*.
- **Misleads for us:** in Marx it is a *charge of error* — treating a relation
  as a thing is the mistake. That charge is still audible. Also, our datom is
  already a thing; nothing needs promoting.

### instantiate

- **Etymology** (witnessed, [etymonline](https://www.etymonline.com/word/instantiate)):
  1946 "represent by an instance"; Latin *instantia* "a standing near",
  rendering Greek *enstasis*.
- **Original technical sense** (witnessed): logic's universal/existential
  instantiation, fixed in the textbooks through Copi 1954; then OOP.
- **What it literally claims:** to produce a *standing example* — a particular
  that stands near the universal and exhibits it.
- **Misleads for us:** it is a type/token relation, not a conversion. Our
  Rust value is not an instance *of* the datom; it is the same information in
  another form.

### encode / decode

- **Etymology** (witnessed, [etymonline](https://www.etymonline.com/word/code)):
  Latin *codex* "tree trunk, wooden tablet, book" ← *caudex*; "system of
  signals" 1808.
- **Original technical sense** (witnessed): Shannon, *A Mathematical Theory of
  Communication*, BSTJ 27, 1948
  ([PDF](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf)).
- **What it literally claims:** to put the message *into the register* — a
  fixed, shared rule-book. This is the only word in the transport cluster that
  literally claims a *change of representation*.
- **Honest** in claiming a shared convention. **Misleads for us:** `de-` is a
  negation, and "code" suggests an arbitrary lookup, where our mapping is
  structural and derivable — which is precisely the psyche's argument for a
  derive macro.

### parse

- **Etymology** (witnessed, [etymonline](https://www.etymonline.com/word/parse)):
  1550s, from Middle English *pars* ← Latin ***pars orationis*, "part of
  speech"**. The schoolroom exercise: state the part of speech of each word.
- **Original technical sense** (witnessed): Irons, "A Syntax Directed Compiler
  for ALGOL 60", *CACM* 4(1), Jan 1961
  ([ACM](https://dl.acm.org/doi/10.1145/366062.366083)); Knuth 1965 uses
  "parsing" as already established.
- **What it literally claims:** *to assign each token its part in a
  grammatical whole*. Structure, explicitly **not** meaning.
- **Honest for us, and precisely so.** This is the best-fitting classical word
  for the text→protoform crossing, because protos is by design "only about
  structure … What a structure means is said by the dialect, never by protos"
  (`protos/src/lib.rs`). *Pars orationis* claims exactly that much and no
  more. It is a verb, so it cannot be a kind name, but it confirms
  `Protosizable` is aimed at the right target.

### realize / actualize

- **Etymology** (witnessed): *realize* 1610s "make real" ← *res*
  ([etymonline](https://www.etymonline.com/word/realize)); *actualize* 1810,
  Coleridge, ← *actus* "a doing"
  ([etymonline](https://www.etymonline.com/word/actualize)).
- **Original technical sense** (witnessed): Kleene's *realizability*, 1945 — a
  formula is realized by a recursive witness
  ([PDF](https://webspace.science.uu.nl/~ooste110/studsemIntMod/Kleene45.pdf)).
  Also the X Toolkit's `XtRealizeWidget`: creates the actual X window for a
  widget that was until then only a data structure
  ([man page](https://invisible-island.net/xterm/xtoolkit/XtCreateWindow.3.html)).
- **What they literally claim:** *realize* — give a description thinghood;
  *actualize* — move from potential to completed act.
- **Honest for us:** `XtRealizeWidget` is a close structural parallel to our
  `actualize`, and Kleene's realizability is exactly "an existence claim gets
  an exhibited witness", which is what a successful parse is.

### embody / incorporate

- **Etymology** (witnessed): *embody* 1540s "invest (a spirit) with a body"
  ([etymonline](https://www.etymonline.com/word/embody)); *incorporate* late
  14c. "put into the body of another" ← *in-* + *corpus*
  ([etymonline](https://www.etymonline.com/word/incorporate)).
- **Original technical sense:** none in computing. Both remain ordinary prose.
- **What they claim:** *embody* — an abstraction receives *a* body, one and
  whole. *incorporate* — something is absorbed *into* an existing body, or
  many are bound into one.
- **The psyche's objection is correct, and the etymology sharpens it.** The
  objection was: "a Datom text also has a body." Precisely — and worse,
  `incorporate` claims *absorption into an existing body*, which is the wrong
  picture for producing a fresh value. If the corporal language were kept, the
  honest word would be `embody` (confer one whole body), not `incorporate`.
  But the objection stands against both: body is not the differentia. Every
  layer in our chain has a body.

### native

- **Etymology** (witnessed, [etymonline](https://www.etymonline.com/word/native)):
  late 14c., Latin *nativus* "innate, produced by birth" ← *nasci* "to be
  born"; of metals "in a pure natural state" 1690s.
- **Original technical sense** (witnessed): "native method" predates JNI;
  "native code" contrasts with p-code and interpreted intermediates. First
  fixed use unresolved.
- **What it literally claims:** *born here* — belongs innately to this
  platform, contrasted with the foreign.
- **Misleads for us, decisively, on two counts.** (a) It is a **relative**
  term: native *to what*? It always needs an implied foreigner, which is the
  very objection the psyche raised against "actual" — and it applies worse to
  `native`, because `Potential` gives `actual` an explicit named contrast in
  the code, whereas `native` has none. (b) Witnessed collision: `signal`
  already calls itself "the native binary form". Two adjacent layers cannot
  both be the native one.

### evaluate

- **Etymology** (witnessed, [etymonline](https://www.etymonline.com/word/evaluate)):
  ← Latin *valere* "be worth"; *evaluation* 1755, verb 1831, originally
  mathematical, "find the numerical value of".
- **Original technical sense** (witnessed): McCarthy, *CACM* 3(4), April 1960,
  the mutually recursive `eval`/`apply`
  ([PDF](https://www-formal.stanford.edu/jmc/recursive.pdf)).
- **What it claims:** to *find the worth* of an expression.
- **Misleads for us:** evaluation reduces; our conversions preserve. A datom
  and its Rust value carry the same information.

### denote

- **Etymology** (witnessed, [etymonline](https://www.etymonline.com/word/denote)):
  1590s ← Latin *denotare* "mark out" = *de-* + *notare*.
- **Original technical sense** (witnessed): Mill, *A System of Logic* 1843
  (denotation vs connotation); Frege 1892; Scott & Strachey, Oxford PRG-6,
  Aug 1971 ([PDF](https://www.cs.ox.ac.uk/files/3228/PRG06.pdf)).
- **What it claims:** the symbol *marks out* an object standing apart from it.
- **Misleads for us:** denotation is a relation to something *outside* the
  chain. Our layers are not about each other; they are the same content.

### represent / representation

- **Etymology** (witnessed, [etymonline](https://www.etymonline.com/word/represent)):
  late 14c. ← Latin *repraesentare* "to make present again" = *re-* +
  *praesentare*.
- **Original technical sense** (witnessed): McCarthy & Hayes 1969
  ([PDF](https://www-formal.stanford.edu/jmc/mcchay69.pdf)); Minsky, AI Memo
  306, 1974; and for data, **Hoare, "Proof of Correctness of Data
  Representations", *Acta Informatica* 1(4), 1972** — the abstraction function
  from concrete representation to abstract value
  ([DOI](https://doi.org/10.1007/BF00289507)).
- **What it claims:** to *make present again* what is absent.
- **Honest, and structurally the right frame.** Hoare's picture — one abstract
  value, several concrete representations, an abstraction function between
  them — is exactly our chain. **Claim:** this is the best justification for
  the psyche's own instinct that the layers are *the same information in
  different forms*, and it argues that the layer nouns should name *forms of
  one thing*, not *different things*.

### manifest

- **Etymology** (witnessed, [etymonline](https://www.etymonline.com/word/manifest)):
  adjective late 14c. ← Latin *manifestus* "palpable, evident", plausibly
  *manus* "hand" + *-festus* "caught, seized" — **caught by the hand, caught
  in the act**. Separately, the noun path reaches **"a certified list of a
  ship's cargo" by 1706**.
- **Original technical sense** (witnessed): two lineages. The adjective:
  **BCPL's `MANIFEST` declaration, Richards 1967** — a name directly
  associated with a value at compile time
  ([BCPL manual](https://www.cl.cam.ac.uk/~mr10/bcplman.pdf)); hence C's
  "manifest constant" and "manifest typing". The noun: JAR `MANIFEST.MF`,
  Android, Kubernetes, OCI.
- **What it claims:** adjective — *stated outright, in view, not inferred*.
  Noun — *a declared complete inventory*.
- **Mixed for us.** The adjective sense is genuinely apt for the psyche's
  question, and Sanskrit's *vyakta* is its exact counterpart (§4). But the
  cargo-list sense is now the dominant one in software, and `Manifest` as a
  type name will read as "a file listing things" to every Rust programmer.
  **Claim:** this collision is fatal for a type name, though not for prose.

---

## 2. Information science and semiotics

### Which term names which layer

Witnessed, with the layer assignment marked as claim where it is ours.

**signal.** Etymology (witnessed,
[etymonline](https://www.etymonline.com/word/signal)): late 14c. "visible
sign", ← Medieval Latin *signale* ← Latin *signum*; **"modulation of an
electric current" from 1855**.

Shannon 1948 is decisive and worth quoting, because it settles the Signal
question. Witnessed, from the paper
([PDF](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf)):

> 2. A **transmitter** which operates on the message in some way to produce a
> signal suitable for transmission over the channel. […]
> 4. The **receiver** ordinarily performs the inverse operation of that done by
> the transmitter, reconstructing the message from the signal.

And the famous exclusion:

> Frequently the messages have meaning; that is they refer to or are correlated
> according to some system with certain physical or conceptual entities. These
> semantic aspects of communication are irrelevant to the engineering problem.

Figure 1 runs: INFORMATION SOURCE → MESSAGE → TRANSMITTER → **SIGNAL** →
RECEIVED SIGNAL → RECEIVER → MESSAGE → DESTINATION.

**Finding, strongly witnessed.** In Shannon the *message* is what source and
destination share; the *signal* is what the transmitter manufactures from it,
"suitable for transmission over the channel", and it is the only thing noise
touches. **Signal means the physically transmitted form.** Our `Signal` — the
rkyv wire form between components — is therefore named *exactly* right, on
Shannon's own definition, and needs no revisiting. Note the irony: *signum*
means sign, and Shannon's signal is the sign with signification stripped off.

**Consequence for the psyche's question in `vision/signal.md`** — whether
Signal can be "wedged in as a layer between the concept and the in-memory
value". **Claim: no, and Shannon says why.** Signal is not a station on the
descent from text to value; it is the *channel form*, orthogonal to the
chain, reached from the value when the value must cross a wire. Shannon's
diagram has the signal on a different axis from the message's own levels. Our
diagram should keep Signal beside the chain, which is how the brief already
draws it.

**token / type.** Peirce, 1906, verbatim (witnessed,
[CP 4.537](https://www.gnusystems.ca/ProlegomPrag.htm)):

> Such a definitely significant Form, I propose to term a *Type*. A Single event
> which happens once and whose identity is limited to that one happening […] I
> will venture to call a *Token*. […] In order that a Type may be used, it has
> to be embodied in a Token which shall be a sign of the Type.

So for Peirce **type is abstract and "does not exist; it only determines
things that do exist"; token is the dated, placed occurrence.**

**Warning, witnessed.** Compiler practice *inverts* this: there the **token**
is the category and the **lexeme** is the concrete matched text. Any layer
named "token" inherits a live ambiguity. Avoid.

**data / datum.** Witnessed
([etymonline](https://www.etymonline.com/word/data)): English 1640s, "a fact
given or granted", ← Latin *datum*, neuter past participle of *dare* "to
give"; the computing sense "transmittable and storable information" dates to
**1946**. **What it claims:** *givenness* — that the thing was handed to you,
needs no justification, and is the *starting point* of a calculation.

**capta.** Witnessed (Checkland & Holwell 1998; Kitchin): *capta* from
*capere* "to take", proposed against *data* from *dare* "to give" — capta is
the subset selected because someone took an interest.
**Claim, and a sharp one:** everything our reader produces is *capta*, not
*data*. A protoform was **taken** by a grammar that chose what counts. The
honest word for the structural layer is closer to "taken" than "given".

**information / in-forming.** Witnessed
([etymonline](https://www.etymonline.com/word/information)): late 14c.
*information* ← Latin *informationem* "outline, concept, idea"; *informare* =
*in-* + *formare*, "to shape, give form to, delineate". The Scholastic sense
is that the intellect *becomes informed by a form*. **Note for us:** protos's
own reader module is called `delineation` — and *delineare* is one of the
glosses of *informare*. The existing name is etymologically well chosen.

**Explicit layer answers** (claim, on witnessed definitions):

| our layer | best classical name | source |
|---|---|---|
| text (glyph stream) | *lexeme*; Peircean *token*; Saussure's *signifiant* | Peirce CP 4.537 |
| protoform (structure, no meaning) | no good classical term; nearest is *capta* | Checkland & Holwell |
| datom (the concept) | Peirce's **type**; Saussure's *signifié*; Frege's *Sinn* | Peirce CP 4.537 |
| the Rust value | **none of them names it well** | — |
| Signal (wire) | **signal**, on Shannon's own definition | Shannon 1948 §I |

**The gap is the finding.** Semiotics has no word for the in-memory value,
because semiotics is about signs standing for things, and the Rust value is
not standing for anything — it *is* the information, held. That is why the
psyche's question is hard, and it is why the answer has to come from
metaphysics (§3) or from the Indian grammarians (§4), not from semiotics.

---

## 3. Philosophy: potentiality, actuality, form

### Aristotle

Witnessed ([SEP, Aristotle's
Metaphysics](https://plato.stanford.edu/entries/aristotle-metaphysics/);
Metaphysics Θ, [MIT](http://classics.mit.edu/Aristotle/metaphysics.9.ix.html)):

> we must not seek a definition of everything but be content to grasp the
> analogy, that it is as that which is building is to that which is capable of
> building, and the waking to the sleeping, and that which is seeing to that
> which has its eyes shut but has sight.

*energeia* = *en-* + *ergon* → "being-at-work". *entelecheia* = *enteles*
(complete) + *echein* (to hold) → "being-at-work-staying-itself" — a word
Aristotle coined and never defined (witnessed, [IEP,
Aristotle](https://iep.utm.edu/aris-mot/)).

**A caution worth recording.** Joe Sachs and IEP argue "actuality" is already a
poor translation of *energeia*, because it connotes a static fact where
Aristotle means ongoing activity; and Aristotle's own test separates *energeia*
from *kinēsis*, the incomplete transition ("we are seeing and have seen … it is
not true that at the same time we are learning and have learnt"). **Claim:**
so `-ization` on `actual` imports exactly the process reading Aristotle
separates off. This is a real but small cost, and it argues for keeping
`actualize` as the *name of the whole descent* (which is a process, correctly)
while not using `Actual` as the *layer noun* (which is a state).

### First and second actuality — the precise hit

Witnessed, *De Anima* II.1, 412a–b (Smith translation,
[MIT](http://classics.mit.edu/Aristotle/soul.2.ii.html); confirmed at [SEP,
Aristotle's Psychology](https://plato.stanford.edu/entries/aristotle-psychology/)):

> Now matter is potentiality, form actuality; of the latter there are two grades
> related to one another as e.g. knowledge to the exercise of knowledge.
>
> It is obvious that the soul is actuality in the first sense, viz. that of
> knowledge as possessed, for both sleeping and waking presuppose the existence
> of soul, and of these waking corresponds to actual knowing, sleeping to
> knowledge possessed but not employed.

**This is the closest thing in the Western tradition to what the psyche asked
for.** The mapping:

| Aristotle | our chain |
|---|---|
| potentiality (the illiterate who could learn) | the text, `Potential<T, C>` |
| **first actuality** — knows, asleep; a *hexis*, a settled possession | **the Rust value, held in memory, typed, not currently being computed with** |
| **second actuality** — contemplating | that value in an expression right now |

The virtue is that this vocabulary **natively distinguishes "held" from "in
use"** — a distinction semiotics simply lacks, and the exact distinction
between a value sitting in a struct field and the same value entering a
computation. And note that first actuality is *simultaneously* a potentiality
for the second act, which is true of our value too: a Rust value is both the
completed result of a parse and the raw material of the next computation.

**Claim.** If the layer is named on this basis, `Actual` is defensible and
`Potential` is its already-existing, already-coded partner. The psyche's worry
— "actual sounds like we're contrasting it with something that isn't actual" —
is answered: yes, and the thing that isn't actual is `Potential<T, C>`, which
is a real type on line 216 of `protos/src/anatomy.rs`.

### Scholastic in-formation: the directional pair

Witnessed, with an important caveat first: **Aquinas did not use the terms
"impressed" and "expressed" species** — they are a later scholastic
systematization of his doctrine
([Encyclopedia.com, "Species,
Intentional"](https://www.encyclopedia.com/religion/encyclopedias-almanacs-transcripts-and-maps/species-intentional)).

The systematized doctrine (witnessed, same source): the intellect has an
**impressed** intelligible species and an **expressed** intelligible species,
the impressed being the *principle* of the act and the expressed its
*terminus*. And the line that matters most:

> The "impression" (species) can come only from the thing being present; but the
> expression (*intentio*, *verbum mentale*) of the thing endures in the
> understanding when the thing is away.

Aquinas's own doctrine (witnessed, [ST I q.85
a.2](https://www.newadvent.org/summa/1085.htm)): the intelligible species is
that **by which** (*quo*) the intellect understands, not that **which**
(*quod*) is understood. Having received the species, the intellect "forms a
definition … expressed by a word". The inner word, *verbum mentis*, is the
concept; its procession from the act of understanding Aquinas calls
***emanatio intelligibilis***.

**Finding.** *species impressa / species expressa* is the best **positive,
symmetric, directional pair** the Western tradition offers: the same form,
received inward from the thing and produced outward by the mind, both nouns,
neither a negation. And the property "endures in the understanding when the
thing is away" is exactly the property wanted of an in-memory value that
outlives the text it came from.

**Claim, with a caution.** Attributing the pair to Aquinas would be wrong; it
is post-Thomistic. And the terms themselves are too Latinate to be Rust kind
names. But the *shape* — impressed/expressed over one content — is the shape
to copy, and it maps onto our two directions without either being a `de-`.

**Aristotle himself gives no such pair.** His couples are all asymmetric in
rank (dynamis/energeia, hyle/morphe, first/second actuality), not directional.
The directional-pair intuition enters with the Scholastic theory of cognition.
That is itself a useful negative result.

### Frege, briefly

Witnessed ([SEP, Frege](https://plato.stanford.edu/entries/frege/)): sign →
*Sinn* (sense, an objective "mode of presentation") → *Bedeutung* (reference),
with the subjective *Vorstellung* explicitly excluded. **Claim:** the virtue
over Saussure is that sense is *objective and shareable*, which is what a type
must be — so `Sinn` is a better analogue of our datom than *signifié* is.

---

## 4. Sanskrit and Pāṇini

### The local repository

**Witnessed.** The living's report is correct: a flow created
`/git/github.com/LiGoldragon/Ashtadhyayi` on 2026-09-08 (commits `190939d`
"Initialize Ashtadhyayi knowledge base repository" and `471cb4f` "Outline the
Ashtadhyayi knowledge base"). It holds Rama Nath Sharma's six-volume
*The Aṣṭādhyāyī of Pāṇini* as DjVu in `sources/`, plus `extracted/`,
`volumes/`, `adhyayas/`, and an empty `sutras/`.

**Usability — an honest assessment, and a caveat the repo does not state.**

| volume | content | extractable text |
|---|---|---|
| 1 (Introduction: the Aṣṭādhyāyī as a grammatical device) | the conceptual volume | **125 characters — cover only** |
| 2 (Adhyāya One) | where 1.1.49, 1.1.56, 1.1.68 live | **279 characters — cover only** |
| 3 (Adhyāyas Two–Three) | — | **262 characters** |
| 4 (Adhyāyas Four–Five) | — | **261 characters** |
| 5 (Adhyāya Six) | — | **243 characters** |
| 6 (Adhyāyas Seven–Eight) | derivational detail | **1,995,033 characters — fully OCR'd** |

Method: `djvutxt` over each file in `sources/`, run this session. Only Volume 6
carries an OCR text layer; the `extracted/*.txt` stubs for volumes 1–5 (17–36
lines each) are not a partial extraction but the *complete* extractable
content. **The repository's README does not say this**, and a later flow
planning "a next pass" to extract sūtras at scale should know that five of the
six volumes will need OCR from the page images first.

OCR quality in Volume 6 is mediocre: diacritics are mangled throughout
(*sthdne* for *sthāne*, *ddyoccdrana* for *ādyoccāraṇa*, *ekddesa* for
*ekādeśa*), and the Devanagari is largely lost. It is searchable in
transliteration if you grep for the mangled forms. **Claim:** usable as a
witness for glosses and for confirming a sūtra is discussed; not usable as a
citable text of the sūtras themselves. Sūtra text below is therefore verified
against the sūtrapāṭha at
[sanskritdocuments.org](https://sanskritdocuments.org/doc_z_misc_major_works/aShTAdhyAyI.html),
with the local repository cited where it supplies Sharma's gloss.

### What the local repository witnesses

Quoted from `extracted/volume6.txt`, with line numbers, OCR as-is:

- **1.1.56** (l. 3755, 1336): "1.1.56 *sthdnivad ddeso nalvidhau*", glossed at
  l. 1662 as "*sthdnivadbhdva* 'treating a replacement as if it was the item it
  replaced'", and at l. 1335 as "'accepting x as y which it replaced'". At
  l. 1672: "A single replacement, therefore, is considered as *sthdni* 'the item
  it replaced'."
- **1.1.49** (l. 20928–29): "1.1.49 *sasthi sthdneyoga*".
- **Paribhāṣā 38** (l. 690): "*ekadesavikrtam ananyavaV* 'that which is
  modified in one part can still be treated as what it was'". And at l. 9087:
  "a form which is modified in one place should still be accepted as its
  unmodified original".
- **upadeśa** (l. 4965): "It has been stated that *upadesa* means
  *ddyoccdrana* 'initial citation'."
- **prakṛti** (l. 8912): "the base (*prakrti*) must occur before a nominal
  ending (*vibhakti*)".
- **ādeśa** (l. 8072): "in connection with replacement (*adesa*)".

### The terms

**sphoṭa / dhvani — the central pair.**

Witnessed ([SEP, Language and Testimony in Classical Indian
Philosophy](https://plato.stanford.edu/entries/language-india/), Deshpande):
Patañjali uses *sphoṭa* for Kātyāyana's "true sounds which are fixed"
(*avasthitā varṇāḥ*) and *dhvani* for "uttered sounds"; "the real sound
(śabda) is thus the sphoṭa … and the quality [length or speed] of the sound is
part of dhvani". Witnessed ([IEP,
Bhartrihari](https://iep.utm.edu/bhartrihari/)): sphoṭa is "the meaning-unit
of speech … not subject to such variations", dhvani is "the audible sound
patterns of speech", "merely the audible possibility of meaning". Root
*sphuṭ*, "to burst forth". Witnessed (SEP, same): "the sentence as a single
partless unit conveys its entire unitary meaning in a flash".

**Finding.** sphoṭa/dhvani is the best semantic fit in the whole survey for
*value versus text*: the indivisible meaning-bearing whole grasped at once,
against the linear audible stream. Neither name is a negation. Abhyankar's
gloss even calls sphoṭa the "**internal** word … revealed when the word is
uttered".

**But — a limit worth stating.** In the theory, *dhvani manifests* (*abhi-vyañj*)
*sphoṭa*: the sound stream is the revealer, the whole is the revealed. The
tradition's one named operation runs **text → value only**. There is no equally
canonical name for the reverse; utterance is described as the speaker's sphoṭa
being *accompanied by* dhvani, not converted into it. So sphoṭa/dhvani names
the two *objects* beautifully and the two *directions* not at all.

**vyakta / avyakta.** Witnessed ([wisdomlib](https://www.wisdomlib.org/definition/vyakta)):
*vi* + *añj* "to make clear" + *-kta*; "manifested, displayed, developed";
avyakta is *mūla-prakṛti* in Sāṃkhya ([IEP,
Sāṅkhya](https://iep.utm.edu/sankhya/)). **Verdict: it fails the psyche's
test.** *avyakta* is morphologically *a-* + *vyakta*, a privative — exactly the
`de-` problem in Sanskrit dress. The tradition itself feels this and reaches
for the positive *mūla-prakṛti* or *pradhāna* instead. Also, in Sāṃkhya the
manifest side is the *richer* one (24 evolved tattvas), which inverts the usual
value-richer-than-text intuition.

**sthūla / sūkṣma.** Witnessed
([Dharmawiki](https://dharmawiki.org/index.php/Sharira_Traya_(%E0%A4%B6%E0%A4%B0%E0%A5%80%E0%A4%B0%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%AF%E0%A4%AE%E0%A5%8D))):
sthūla-śarīra is gross, physical, visible; sūkṣma-śarīra is subtle, holding
manas and buddhi, and persists while gross bodies are assumed and discarded.
**Claim:** the in-memory value is the *sūkṣma* end. Clean positive/positive, no
privative, and *scalar* rather than binary — the tradition itself grades it
(tanmātra vs mahābhūta), so intermediate layers can be "subtler" and "grosser".
Weakness: it names degrees on one scale, not two operations.

**prakṛti / vikṛti — with a correction.** Witnessed ([SEP,
language-india](https://plato.stanford.edu/entries/language-india/)): "While
Pāṇini uses the term *prakṛti* to refer to the derivationally original state of
a word or expression before changes effected by grammatical operations are
applied, **Kātyāyana and Patañjali use the term *vikṛta*** to refer to the
derivationally transformed segment." **So the pair, as a pair, is
post-Pāṇinian.** In Pāṇini's own sūtras *prakṛti* appears mostly in the
instrumental *prakṛtyā*, "remains in its original form" (6.1.115, 6.2.1,
6.3.83, 6.4.163), and the one sūtra where both occur, 5.1.12 *tadarthaṃ
vikṛteḥ prakṛtau*, is about material cause, not stems. Abhyankar's settled
gloss (witnessed, [wisdomlib](https://www.wisdomlib.org/definition/prakriti)):
*prakṛtir upādānakāraṇaṃ tasyaiva uttaram avasthāntaraṃ vikṛtiḥ* — "prakṛti is
the material cause; vikṛti is its later, other state." That is a **conversion**,
not a view.

**Note.** Pāṇini's own working term for "the stem an affix attaches to" is
**aṅga** (1.4.13), not prakṛti.

**sthānin / ādeśa.** Witnessed
([wisdomlib](https://www.wisdomlib.org/definition/sthanin),
[ādeśa](https://www.wisdomlib.org/definition/adesha)): sthānin is "the original
word or part of a word … for which a substitute (ādeśa) is prescribed"; ādeśa
from *ā* + *diś* "to point out, enjoin". Anchored in 1.1.49 *ṣaṣṭhī
sthāneyogā* and 1.1.56 *sthānivad ādeśo 'nalvidhau* (both verified in the
sūtrapāṭha; both witnessed in the local repository). **Assessment:** the
cleanest positive/positive Paninian pair, and 1.1.56 is a deep idea — the
substitute inherits the original's properties for further rules, like a wrapper
that preserves the wrapped type's behaviour. But it is an in-place rewrite
relation, not a crossing between representations, and it has no inverse.

**samāsa / vigraha — the one pair that names two directions.** Witnessed
([wisdomlib](https://www.wisdomlib.org/definition/vigraha)): *vigraha* is
"separation of the constituent words of a compound word", from *vi-* (apart) +
*grah* (to seize) — "seizing apart"; *vṛtyarthāvabodhakaṃ vākyaṃ vigrahaḥ*,
"the vigraha is the sentence that makes known the meaning of the compressed
form". *samāsa* is the compacted form, "putting together". The tradition even
splits *śāstrīya-vigraha* (technical, case endings restored) from
*laukika-vigraha* (ordinary) — **claim:** a canonical unparse versus a
human-readable one, which is a distinction we may eventually want.

**saṃhitā / pada.** Witnessed: 1.4.109 *paraḥ saṃnikarṣaḥ saṃhitā* defines
saṃhitā as maximal proximity of sounds; pada-pāṭha is "a recitation marked by a
conscious pause after every word … this method suppresses euphonic combination
and restores each word in its original intended form"
([Wikipedia, Padapatha](https://en.wikipedia.org/wiki/Padapatha)).
**Claim:** the closest thing in the tradition to "continuous stream" versus
"separated tokens" — our text versus our protoform — with both names positive
and ancient. Underrated.

**upadeśa.** Witnessed
([wisdomlib](https://www.wisdomlib.org/definition/upadesha)): "original
enunciation", glossed *upadeśa ādyoccāraṇam*, "the first utterance"; witnessed
in the local repository at l. 4965. Sūtra 1.3.2 *upadeśe 'j-anunāsika it*: the
`it` markers exist **only** in the upadeśa form and vanish in the used form.
**Claim, and a good one:** this is the tradition's word for *the form as
stored and taught, carrying metadata that is stripped before use* — a citation
form with annotations. Its natural counterpart would be *prayoga* (usage), but
the research **could not verify** prayoga as a standing antonym; treat the pair
as constructed.

**lopa — a bonus.** Witnessed: 1.1.60 *adarśanaṃ lopaḥ*, "non-appearance is
elision", and 1.1.62 *pratyayalope pratyayalakṣaṇam* — after an affix is
elided, operations conditioned by it still apply. **Claim:** an elided element
leaves a ghost that still *types* the derivation. That is a zero-width field
that still participates in schema resolution — worth remembering if datom ever
needs an absent-but-typing field. (Note: wisdomlib misnumbers this sūtra as
1.1.52; the sūtrapāṭha has 1.1.60. 1.1.52 is *alo 'ntyasya*.)

**1.1.68 *svaṃ rūpaṃ śabdasyāśabdasaṃjñā*** — "a word denotes its own form,
unless it is a technical term for a word-class" (verified in the sūtrapāṭha).
**Claim:** Pāṇini legislating use versus mention — quoting versus evaluating.
Directly relevant if datom ever needs "literal token" against "interpreted
token".

**vāc and its four levels.** Witnessed (Ṛgveda 1.164.45,
[wisdomlib](https://www.wisdomlib.org/hinduism/book/rig-veda-english-translation/d/doc830788.html)):
"Four are the definite grades of speech … three, deposited in secret, indicate
no meaning; men speak the fourth." The standard levels
([wisdomlib, paśyantī](https://www.wisdomlib.org/definition/pashyanti), citing
Vākyapadīya I.144):

| level | characterization (witnessed) | our layer (claim) |
|---|---|---|
| **parā** | potential sound, wholly unmanifest | not a representation — the *type*, the capacity |
| **paśyantī** | "seeing"; subtle, pre-audible; identified with *pratibhā*, the first flash of understanding | **the value at rest — whole, unsequenced, grasped at once** |
| **madhyamā** | at the heart; "the basis for conceptual understanding though still not audible"; the speaker "looks for and selects appropriate words, phrases, and their sequence" | **the structured-but-unuttered — the protoform** |
| **vaikharī** | "articulate and audible, manifesting as distinguishable phonemes" | **the text** |

**This is the single most precise mapping in the survey**, because madhyamā
distinguishes *sequenced-but-unemitted* from *unsequenced whole* — the exact
difference between our protoform and our datom, and a difference most Western
vocabulary collapses.

**Caveat, and it matters.** Bhartṛhari himself gives **three** levels; *parā*
is Abhinavagupta's and the Tantric tradition's addition. IEP's Bhartṛhari
entry mentions only paśyantī and vaikharī. The three-vs-four point rests on a
secondary source and should be confirmed in Coward's *The Sphoṭa Theory of
Language* or the Vākyapadīya Brahmakāṇḍa vṛtti on 1.142–144 before being built
on. SEP has **no** Bhartṛhari or sphoṭa entry.

**vivarta / pariṇāma — and this is the Signal answer.** Witnessed
([wisdomlib](https://www.wisdomlib.org/definition/vivarta); [IEP, Advaita
Vedānta](https://iep.utm.edu/advaita-vedanta/)): *vivarta* is "an apparent
form … as a serpent is a vivarta of a rope"; Brahman "appears as the manifold
world **without undergoing an intrinsic change or modification**". *pariṇāma*
is real transformation of the substrate (Sāṃkhya), backed by *satkāryavāda* —
"the effect already exists in its cause prior to its production" ([IEP,
Sāṅkhya](https://iep.utm.edu/sankhya/)).

**Finding.** This maps onto our chain with unusual exactness, and it is the
distinction we currently have no word for:

- **vivarta** = the same bytes viewed under another aspect, substrate
  untouched, reversible by mere knowledge — **a zero-copy view. This is
  Signal/rkyv.**
- **pariṇāma** = an actual conversion producing a new object — **this is every
  other crossing in our chain**, and *satkāryavāda* supplies exactly the
  guarantee wanted of a lossless codec: nothing in the output was absent from
  the input.

Two cautions. *vivarta* carries a **pejorative** charge — the apparent form is
*false*, produced by ignorance — which is wrong for a zero-copy view that is
perfectly valid. And Advaita's vivarta is asymmetric in a way a view is not.
Useful as a *concept* to reason with; poor as a name to ship.

**A striking convergence.** Pāṇini's own tradition already has the zero-copy
idea, positively stated, and the local repository witnesses it: Paribhāṣā 38,
*ekadeśavikṛtam ananyavat* — "that which is modified in one part can still be
treated as what it was" (`extracted/volume6.txt:690`), and Sharma's fuller
gloss at l. 9087, "a form which is modified in one place should still be
accepted as its unmodified original". **Claim:** that is the *identity of a
value under a partial view* — precisely what rkyv's archived form asserts, and
what 1.1.56's *sthānivadbhāva* asserts about a substitute. The Indian
grammarians thought carefully about when a modified form is still the same
thing, which is the central question of a zero-copy format.

### Direct answer to the brief's critical question

**Does any of this give a clean positive pair for the two directions?**

Ranked, claim on witnessed material:

1. **samāsa / vigraha** — the only pair that natively names *two directions of
   conversion*. vigraha ("seizing apart") is the analytic expansion; samāsa
   ("putting together") the compacted form. Both positive, both standard
   Paninian metalanguage.
2. **saṃhitā / pada** — continuous joined stream versus separated words. Both
   positive, both ancient, and Pāṇini defines saṃhitā himself (1.4.109).
3. **sphoṭa / dhvani** — best fit for the two *objects*, no good name for the
   reverse direction.
4. **prakṛti / vikṛti** — positive, but unidirectional; names no inverse.
5. **sthānin / ādeśa** — positive, but substitution within one representation.
6. **vivarta / pariṇāma** — a different and valuable axis: view versus real
   conversion.

Failing the test outright: **vyakta / avyakta**, and anything built on *lopa*
or *adarśana* — all privatives.

---

## 5. Candidate table

Marked **[used]** where the name already appears in the codebase (grep of
`protos`, `datom-codec`, `ethos-zero`, `datom`, `signal`, 2026-09-09), and
**[free]** where it does not.

### 5a. The Rust-value layer noun

| candidate | the case | status |
|---|---|---|
| **`Actual`** | Aristotle's *first actuality*: knowledge possessed, whether or not currently exercised — the exact sense wanted. Its contrast term `Potential` **already exists as a type** (`protos/src/anatomy.rs:216`), which answers the psyche's "contrasted with what?" objection concretely. Cheapest change: `actualize` and `Actualizable` stay. | `Actualizable`, `actualize`, `Potential` **[used]**; `Actual` as a noun **[free]** |
| **`Native`** | "born here, belongs to this platform". Reads well to Rust programmers. **But**: `signal/README.md:7` already calls Signal "the native binary form", so the two adjacent layers would both claim it; and `native` is inherently relative, needing an implied foreigner it does not name. | **[collides]** — witnessed in `signal` |
| **`Corpus` / `Corporate`** | the current name. The psyche's objection stands: a datom text also has a body, so body is not the differentia. `Corporate` additionally reads as the legal sense. | `Corporate` **[used]** as a Fault variant only; `Corpus` **[free]** |
| **`Held`** | first actuality is a *hexis*, a settled possession; "held" says the value is in hand, at rest, available. Plain English, no Latin baggage, no negation. Pairs naturally with a "release"/"utter" direction. | **[free]** |
| **`Grasped`** | matches sphoṭa's "grasped in a flash" and paśyantī's *pratibhā*; says the information has been taken hold of as a whole. Slightly passive-sounding for a type name. | **[free]** |
| **`Subtle`** | *sūkṣma*: the non-public, structured layer where mind and intellect live, against the gross emitted form. Scalar, so intermediate layers can be graded. Reads oddly in Rust. | **[free]** |
| **`Value`** | the honest, boring answer: it is the value the program computes with. Zero mystique, zero collision with the tradition, and it is what every Rust programmer will call it anyway. **Weakness:** so generic it names nothing, and `datom-codec` already has `Problem::Value`. | `Problem::Value` **[used]**; `Value` as a layer **[free]** |

**Claim, the recommendation.** `Actual` is the strongest on evidence, precisely
because the codebase has already committed to its partner. The psyche's stated
worry about it is answered by `Potential` being a real type rather than an
implied contrast — and the same worry applies *more* strongly to `native`,
which has no named partner at all and is already spoken for by Signal. If
`Actual` still grates, `Held` is the best fresh candidate: it carries
Aristotle's *hexis* without the Latin.

### 5b. Kinds (-able adjectives) and capabilities (verbs)

**Descent — text toward value:**

| kind | verb | the case | status |
|---|---|---|---|
| `Protosizable` | `protosize` | text → protoform. Confirmed apt by *pars orationis*: claims structure and explicitly not meaning, which is exactly protos's charter. | **[used]** |
| `Conceivable<C>` | `conceive` | protoform → concept. "Taking together into a concept"; matches Peirce's *type* as the layer reached. | **[used]** |
| `Datomizable` | `datomize` | the psyche's own coinage, already liked; continuous with `ethos-zero`'s existing "datomization" pass. | `Datomizable` **[free]**; "datomization" **[used]** in `ethos-zero/README.md` |
| `Actualizable<T>` | `actualize` | the whole descent, from `Potential`. Parallels `XtRealizeWidget`. | **[used]** |
| `Incorporable<T>` | `incorporate` | concept → the value layer. **Weakest link**: `incorporate` claims *absorption into an existing body*, the wrong picture for producing a fresh value; and it is declared in `src/kinds.rs` but **absent from `protos-kinds.ethos`**. | **[used]**, and out of step with the ethos |
| `Graspable` | `grasp` | proposed replacement for `Incorporable`: sphoṭa "grasped in a flash", positive, no body claim. | **[free]** |

**Ascent — value toward text:**

| kind | verb | the case | status |
|---|---|---|---|
| `Textualizable` | `textualize` | → text. Positive; names the layer reached, not a negation of the other direction. Already the pattern. | **[used]** |
| `Situating` | `situate` | text plus situation in one pass. | **[used]** |
| `Utterable` | `utter` | *vaikharī*, "articulate and audible"; the natural positive partner to a "grasp" descent, and the tradition's own word for the outward direction. | **[free]** |
| `Expressible` | `express` | *species expressa*: "the expression of the thing endures in the understanding when the thing is away". The best-attested positive counterpart to an inward "impression". | **[free]** |

**Claim on the naming rule.** The existing convention — *a kind is named for
the layer its capability reaches* — is already the answer to "positive names
for both directions", and it is better than serde's. `Textualizable` and
`Datomizable` are not opposites of each other; each names a destination. That
is why neither needs a `de-`. **The rule is sound; it is only the
value-layer's name that is unsettled**, and once that noun is chosen its kind
follows automatically (`Actualizable`, or `Nativizable`, or whatever the noun
licenses).

### 5c. The unresolved tension the brief did not ask about

Witnessed, from `vision/datom.md`, 2026-09-09: "I like Datomizable, but it does
start a conflict with the method name of `potential`, which I think was
`actualized`."

**Claim.** The conflict is real and is visible in the code: `Actualizable<T>`
is *the whole descent* (`Potential<T, C>` → `T`), while `Datomizable` would be
*one crossing*. They are at different scales, so both can exist — but only if
the naming makes the scale difference audible. Options: keep `Actualizable`
for the whole descent and let `Datomizable` name the single crossing; or rename
the whole descent to something that says "the whole way" (`Route` already
exists in `src/kinds.rs` and does roughly this). This is a design question for
the psyche, not a research finding, but the research bears on it: `actualize`
is the *process* word (Aristotle's *kinēsis*, the incomplete transition), which
suits a whole descent better than it suits a single crossing.

---

## Sources

Codebase, read 2026-09-09 under `/git/github.com/LiGoldragon`:
`protos/src/kinds.rs`, `protos/src/anatomy.rs`, `protos/src/lib.rs`,
`protos/src/actualization.rs`, `protos/protos.ethos`,
`protos/protos-kinds.ethos`, `protos/README.md`,
`datom-codec/datom-codec.ethos`, `datom-codec/src/anatomy.rs`,
`ethos-zero/README.md`, `signal/README.md`.

Local Pāṇini corpus: `/git/github.com/LiGoldragon/Ashtadhyayi`, commits
`190939d` and `471cb4f` (2026-09-08); `extracted/volume6.txt`; `sources/*.djvu`
probed with `djvutxt`.

Etymology: [etymonline](https://www.etymonline.com/) — serialize, series,
marshal, pickle, materialize, reify, instantiate, code, parse, realize,
actualize, embody, incorporate, native, evaluate, denote, represent, manifest,
signal, data, information, form.

Computing primaries: [Nelson, *Remote Procedure Call*, Xerox PARC CSL-81-9,
1981](https://archive.org/stream/bitsavers_xeroxparctoteProcedureCall_14151614/CSL-81-9_Remote_Procedure_Call_djvu.txt) ·
[Birrell & Nelson, TOCS 1984](https://web.eecs.umich.edu/~mosharaf/Readings/RPC.pdf) ·
[Modula-3 Pickle](https://www.cs.purdue.edu/homes/hosking/m3/help/gen_html/libm3/src/pickle/ver1/Pickle.i3.html) ·
[MFC serialization](https://learn.microsoft.com/en-us/cpp/mfc/serialization-in-mfc) ·
[Java Object Serialization Spec](https://docs.oracle.com/en/java/javase/21/docs/specs/serialization/) ·
[Eswaran et al., CACM 1976](https://dl.acm.org/doi/10.1145/360363.360369) ·
[Blakeley et al., SIGMOD 1986](https://dl.acm.org/doi/10.1145/16856.16861) ·
[Irons, CACM 1961](https://dl.acm.org/doi/10.1145/366062.366083) ·
[McCarthy 1960](https://www-formal.stanford.edu/jmc/recursive.pdf) ·
[McCarthy & Hayes 1969](https://www-formal.stanford.edu/jmc/mcchay69.pdf) ·
[Hoare, *Proof of Correctness of Data Representations*, 1972](https://doi.org/10.1007/BF00289507) ·
[Scott & Strachey, PRG-6, 1971](https://www.cs.ox.ac.uk/files/3228/PRG06.pdf) ·
[Jones, VDM](https://homepages.cs.ncl.ac.uk/cliff.jones/publications/Books/vdm_tn.pdf) ·
[Kleene 1945](https://webspace.science.uu.nl/~ooste110/studsemIntMod/Kleene45.pdf) ·
[BCPL manual](https://www.cl.cam.ac.uk/~mr10/bcplman.pdf) ·
[XtRealizeWidget](https://invisible-island.net/xterm/xtoolkit/XtCreateWindow.3.html).

Information theory and semiotics:
[Shannon 1948](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf) ·
[Peirce, CP 4.537](https://www.gnusystems.ca/ProlegomPrag.htm) ·
[SEP, Peirce's semiotics](https://plato.stanford.edu/entries/peirce-semiotics/) ·
[SEP, types and tokens](https://plato.stanford.edu/entries/types-tokens/) ·
[Chandler on Saussure](https://www.cs.princeton.edu/~chazelle/courses/BIB/semio2.htm) ·
[Checkland & Holwell on data/capta](https://www.taylorfrancis.com/chapters/edit/10.4324/9780080458397-10/data-capta-information-knowledge-peter-checkland-sue-holwell).

Philosophy:
[SEP, Aristotle's Metaphysics](https://plato.stanford.edu/entries/aristotle-metaphysics/) ·
[SEP, form and matter](https://plato.stanford.edu/entries/form-matter/) ·
[SEP, Aristotle's psychology](https://plato.stanford.edu/entries/aristotle-psychology/) ·
[Metaphysics IX](http://classics.mit.edu/Aristotle/metaphysics.9.ix.html) ·
[De Anima II.1](http://classics.mit.edu/Aristotle/soul.2.ii.html) ·
[IEP, Aristotle: Motion](https://iep.utm.edu/aris-mot/) ·
[Species, Intentional](https://www.encyclopedia.com/religion/encyclopedias-almanacs-transcripts-and-maps/species-intentional) ·
[Summa Theologiae I q.85](https://www.newadvent.org/summa/1085.htm) ·
[SEP, medieval mental representation](https://plato.stanford.edu/entries/representation-medieval/) ·
[SEP, Frege](https://plato.stanford.edu/entries/frege/) ·
[SEP, Plotinus](https://plato.stanford.edu/entries/plotinus/).

Sanskrit and Pāṇini:
[Aṣṭādhyāyī sūtrapāṭha](https://sanskritdocuments.org/doc_z_misc_major_works/aShTAdhyAyI.html) ·
[GRETIL sūtra list](http://gretil.sub.uni-goettingen.de/gretil/1_sanskr/6_sastra/1_gram/paniniiu.htm) ·
[SEP, Language and Testimony in Classical Indian Philosophy](https://plato.stanford.edu/entries/language-india/) ·
[SEP, Epistemology in Classical Indian Philosophy](https://plato.stanford.edu/entries/epistemology-india/) ·
[IEP, Bhartrihari](https://iep.utm.edu/bhartrihari/) ·
[IEP, Sāṅkhya](https://iep.utm.edu/sankhya/) ·
[IEP, Advaita Vedānta](https://iep.utm.edu/advaita-vedanta/) ·
wisdomlib entries for
[sphoṭa](https://www.wisdomlib.org/definition/sphota),
[vyakta](https://www.wisdomlib.org/definition/vyakta),
[prakṛti](https://www.wisdomlib.org/definition/prakriti),
[sthānin](https://www.wisdomlib.org/definition/sthanin),
[ādeśa](https://www.wisdomlib.org/definition/adesha),
[vigraha](https://www.wisdomlib.org/definition/vigraha),
[upadeśa](https://www.wisdomlib.org/definition/upadesha),
[lopa](https://www.wisdomlib.org/definition/lopa),
[paśyantī](https://www.wisdomlib.org/definition/pashyanti),
[vivarta](https://www.wisdomlib.org/definition/vivarta),
[artha](https://www.wisdomlib.org/definition/artha),
[vāc](https://www.wisdomlib.org/definition/vac) ·
[Ṛgveda 1.164.45](https://www.wisdomlib.org/hinduism/book/rig-veda-english-translation/d/doc830788.html) ·
[Chāndogya 6.3.2](https://www.wisdomlib.org/hinduism/book/chandogya-upanishad-english/d/doc239266.html) ·
[Padapāṭha](https://en.wikipedia.org/wiki/Padapatha) ·
[Śarīra Traya](https://dharmawiki.org/index.php/Sharira_Traya_(%E0%A4%B6%E0%A4%B0%E0%A5%80%E0%A4%B0%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%AF%E0%A4%AE%E0%A5%8D)).

### Not established

- No primary source found for the ORM sense of hydrate/dehydrate; no coiner
  found for "materialized view", "native code", or the compiler sense of
  "parse".
- The noun *informatio* was not attested in a primary Aquinas text; only the
  verbal in-forming doctrine.
- *species impressa/expressa* is post-Thomistic systematization, **not**
  Aquinas's own vocabulary.
- *prayoga* as the standing antonym of *upadeśa* is unverified.
- Bhartṛhari gives **three** levels of vāc; *parā* as a fourth rests on a
  secondary source and needs confirming in Coward or the Vākyapadīya vṛtti.
- wisdomlib misnumbers the *lopa* sūtra as 1.1.52; the sūtrapāṭha has 1.1.60.
- Volumes 1–5 of the local Ashtadhyayi repository have **no OCR text layer**;
  only Volume 6 (Adhyāyas 7–8) is searchable.
