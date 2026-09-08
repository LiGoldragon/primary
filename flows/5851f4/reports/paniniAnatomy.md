# Panini and the anatomy of communicating, thinking, and reacting

Flow 5851f4. Report carried by a research subflow; web research authorized. Written 2026-09-08.

## How to read this report

Every claim carries a tag:

- **[P]** primary text — a sutra, karika, or canonical passage, with reference.
- **[S]** scholarly secondary source — named author and work.
- **[W]** general web page — encyclopaedia, teaching site, blog. Flagged where the source is popular, devotional, or advocacy writing.
- **[F]** the flow's own inference. Not found in any source; mine.
- **[?]** uncertain — the underlying research could not verify the reference, or sources conflict.

The report is a carried account. It relays what four parallel research passes found; it witnesses nothing itself. Where sources disagree, the disagreement is reported rather than resolved. Where a plausible connection is *not* attested, that is stated as a negative finding, which is the most useful thing in sections 4 and 5.

The synthesis in section 8 is kept strictly separate from sections 1-7. Nothing enters the synthesis that is not sourced above it.

---

## 1. The Ashtadhyayi as a system

An anatomy of stages, not a history. The Ashtadhyayi has roughly 3,950-4,000 sutras in 8 adhyayas x 4 padas [W: exact count varies by recension; 3,959 and 3,983 are both commonly cited] [?].

### 1.1 The sutra types — the instruction set

The traditional six-fold taxonomy is transmitted in a mnemonic verse [W: Hindi Wikipedia सूत्र; Sanskrit-grammar blogs]:

> *samjna ca paribhasha ca vidhir niyama eva ca / atideso 'dhikarasca shadvidham sutralakshanam*

The verse is **not** in the Ashtadhyayi and could not be pinned to a named classical author [?]. Treat it as traditional-pedagogical, not primary.

| Type | Function in the system | Example |
|---|---|---|
| **samjna** | Defines a technical term. Creates a name that has meaning only inside the system. | 1.1.1 *vrddhir ad-aic*; 1.4.14 *suptinantam padam* [P] |
| **paribhasha** | Metarule. Tells you how to *read and apply* other rules; prescribes no linguistic operation itself. | 1.1.49 *shashthi sthaneyoga*; 1.4.2 *vipratishedhe param karyam* [P] |
| **vidhi** | Operational. Prescribes an actual substitution, augment, affix, or deletion. | 6.1.77 *iko yan aci* [P] |
| **niyama** | Restriction. Narrows an already-established general rule to a subset. | textbook example uncertain [?] |
| **atidesha** | Extension by analogy. "Treat X as Y" — transfers Y's properties without restating them. Diagnostic marker: the suffix *-vat*. | 1.1.56 *sthanivad adesho 'nalvidhau*; 6.4.22 *asiddhavad atra bhat* [P] |
| **adhikara** | Governing heading. A term or condition that carries into every following sutra in its domain. | 1.4.23 *karake*; 2.3.1 *anabhihite*; 3.1.91 *dhatoh*; 8.2.1 *purvatrasiddham* [P] |

Source for the type descriptions: Learn Sanskrit Online, "The Structure of the Ashtadhyayi" [W]. Note that page glosses *niyama* as "exception," which is loose — exception proper is *apavada* — so do not rely on that gloss.

**Disagreement on the taxonomy.** Lists give five, six, seven or more types [W, multiple]:
- Five-fold lists drop *niyama* (folding it into *vidhi*) or drop *paribhasha* (treating metarules as a separate genre outside the typology).
- Seven-/eight-fold lists add **pratishedha/nishedha** (prohibition — Panini certainly has prohibitive sutras, e.g. 1.1.5 *kniti ca*, and *pratishedha* is standard Mahabhashya vocabulary [P]), **vibhasha** (optionality: *va*, *vibhasha*, *anyatarasyam*), and sometimes **nipatana** (irregular forms stipulated wholesale).
- Western scholarship generally treats the typology as a *post-Paninian pedagogical* classification, not something Panini declared. *Adhikara* is not itself defined by any sutra; it is a commentators' term [?, no single scholarly paper adjudicating the 5-vs-6-vs-more question was located].

**[F]** Read as an anatomy: the six types are four distinct kinds of thing. *samjna* builds the vocabulary. *paribhasha* is the interpreter's own rules — the layer that says how the machine runs. *vidhi* is the only type that does work on the material. *adhikara*, *niyama*, *atidesha* are all scope and inheritance devices — they control which vidhis see what. The system separates **what a term means**, **what an operation does**, **when an operation is visible**, and **how conflicts resolve**, into four different sutra genres. That separation is the architectural fact.

### 1.2 The Shiva sutras and pratyahara — the encoding layer

The 14 sutras, final letter of each being an *it* / *anubandha* marker (a metalinguistic tag, not a phoneme of the language) [W: Learn Sanskrit Online, "The Shiva Sutras"; Wikipedia "Shiva Sutras"]:

```
 1. a i u Ṇ          8. jha bha Ñ
 2. ṛ ḷ K            9. gha ḍha dha Ṣ
 3. e o Ṅ           10. ja ba ga ḍa da Ś
 4. ai au C         11. kha pha cha ṭha tha ca ṭa ta V
 5. ha ya va ra Ṭ   12. ka pa Y
 6. la Ṇ            13. śa ṣa sa R
 7. ña ma ṅa ṇa na M 14. ha L
```

**Mechanism.** A *pratyahara* is formed by taking any phoneme in the list and appending any following anubandha. The result denotes the continuous interval from that phoneme up to (not including) that marker. Licensed internally by three sutras [P]: **1.3.3** *hal antyam* (a final consonant is an *it*), **1.3.9** *tasya lopah* (an *it* is deleted), **1.1.71** *adir antyena sahetā* (an initial together with a final *it* denotes itself and everything between).

Worked: **aC** = a i u ṛ ḷ e o ai au = all vowels. **haL** = everything from *ha* in S5 to the *L* of S14 = all consonants. **iK** = i u ṛ ḷ, used in 6.1.77 *iko yan aci*. Roughly 41-42 pratyaharas are in actual use. Note *ha* appears **twice** (S5 and S14) — a deliberate redundancy that lets *haL* cover all consonants while *shaL/jhaL* groupings still work.

**Why "optimal" is a real claim and not rhetoric.** Wiebke Petersen, "A Mathematical Analysis of Panini's Sivasutras," *Journal of Logic, Language and Information* 13(4):471-489 (2004) [S] gives a set-theoretic proof: given the set of natural classes Panini needs to denote (closed under intersection), and linking its Hasse diagram to interval representations, Panini's ordering is provably optimal — no shorter or fewer-marker arrangement expresses the same class set as intervals. The argument uses only the class set, not phonological features. Also: Petersen, "On the Construction of Sivasutra-Alphabets" [S]. J. F. Staal, "A Method of Linguistic Description: The Order of Consonants according to Panini," *Language* 38 (1962) [S] [?, exact year/pages unverified] is the earlier formal treatment. Kiparsky (1991) is reported to argue the ordering does not depend on traditional phonetic ordering and could have been derived independently from the pratyahara requirements [?, attribution from search summaries only].

**[F]** In interface terms: the Shiva sutras are a lookup table with interval addressing. Every phonological class the grammar needs becomes a two-character address. The grammar's operational rules never have to enumerate a sound class — they name one. This is the single clearest instance in the system of a *compression layer sitting between the rule layer and the material*.

### 1.3 The derivation pipeline — meaning-intent to utterance

The reconstruction, chiefly Kiparsky's levels analysis [S: Kiparsky, "On the Architecture of Panini's Grammar," in *Sanskrit Computational Linguistics*, LNCS 5402, Springer 2009]:

**vivaksha → karaka → vibhakti → stem + pratyaya → pada → sandhi → tripadi → utterance**

**Stage 0 — vivaksha (the desire to express).** *Vivaksha*, from the desiderative of √vac, "the intention or desire of the speaker with regard to the sense to be conveyed" [W: wisdomlib]. **This is outside the grammar proper.** Panini's grammar takes semantic content plus speaker intent as *input*; it does not derive them. It is a commentators' term, heavily used in the Mahabhashya, and there appears to be **no sutra defining it** [?]. The tradition crystallizes it as the paribhasha *vivakshatah karakani bhavanti* — "karakas obtain according to the intention to express" [W: wisdomlib lists it explicitly as a paribhasha] [?, could not verify whether this exact formula is Patanjali's own wording or a later Kaiyata/Nagesha crystallization]. Panini does make speaker's intention an explicit rule condition in places, e.g. **A 4.1.147**, where whether one addresses someone disrespectfully is the speaker's choice [P, via search summary] [?].

**Stage 1 — karaka assignment.** Governed by the adhikara **1.4.23 *karake***, running 1.4.23-1.4.55. Semantic-relational participant roles are assigned here. See 1.4 below.

**Stage 2 — vibhakti assignment.** Chapter 2 pada 3, governed by the adhikara **2.3.1 *anabhihite*** ("when not already expressed") [P]. This is a crucial gate: a nominal takes a case ending for its karaka **only if that relation is not already signalled elsewhere** — e.g. by the verbal ending in an active or passive finite verb. Then:

| Sutra | Rule | Effect |
|---|---|---|
| 2.3.2 *karmani dvitiya* | accusative for *karma* | [P] |
| 2.3.13 *caturthi sampradane* | dative for *sampradana* | [P] [?] |
| 2.3.18 *kartrkaranayos trtiya* | instrumental for *kartr* and *karana* | [P] |
| 2.3.28 *apadane pancami* | ablative for *apadana* | [P] [?] |
| 2.3.36 *saptamy adhikarane ca* | locative for *adhikarana* | [P] [?] |
| 2.3.46 *pratipadikartha-...-matre prathama* | nominative for bare stem-meaning | [P] [?] |
| 2.3.50 *shashthi shese* | genitive as the residue case | [P] [?] |

The 2.3.13/28/36/46/50 numbers were not individually verified [?]. Note that **the genitive is a case with no karaka** — the residue. **[F]** That is architecturally significant: the karaka layer does not exhaust the case layer, so the mapping between the two is not a bijection, which is exactly why the two levels must be distinct.

**Stage 3 — stem and affix.**
- **1.3.1 *bhuvadayo dhatavah*** defines *dhatu* (verbal root) by reference to the Dhatupatha [P].
- **1.2.45 *arthavad adhatur apratyayah pratipadikam*** defines *pratipadika* (nominal stem): meaningful, not a root, not an affix [P].
- **3.1.91 *dhatoh*** is the adhikara governing the entire affixation apparatus from 3.1.91 to the end of adhyaya 3 [P].
- **3.4.78** enumerates the *tin* (finite verbal) endings; **4.1.1-4.1.2** introduce the 21 *sup* (nominal case) endings, 7 cases x 3 numbers [P].

**Stage 4 — pada.** **1.4.14 *suptinantam padam***: "that which ends in a *sup* or a *tin* affix is a *pada*" [P]. Only padas are subject to external sandhi and to *padanta* conditions. **[F]** Pada-hood is a gate that turns on a whole further class of operations — the boundary between word-internal and word-external processing.

**Stage 5 — phonology.** Internal sandhi (chapters 6-7), then the **tripadi** (8.2.1-8.4.68) for the final, order-sensitive phonology. See 1.5.

### 1.4 The six karakas — the model of an event

Adhikara **1.4.23 *karake***, block 1.4.23-1.4.55 [P]. Sanskrit and glosses from Learn Sanskrit Online [W], corroborated by a Shodhganga thesis chapter on karaka theory [S].

| Karaka | Sutra | Sanskrit | Sense | Default case |
|---|---|---|---|---|
| **apadana** (source) | 1.4.24 | *dhruvam apaye 'padanam* | the fixed point from which movement away occurs | 5th ablative |
| **sampradana** (recipient) | 1.4.32 | *karmana yam abhipraiti sa sampradanam* | the one whom the agent intends to reach by the action | 4th dative |
| **karana** (instrument) | 1.4.42 | *sadhakatamam karanam* | the **most** effective means | 3rd instrumental |
| **adhikarana** (locus) | 1.4.45 | *adharo 'dhikaranam* | the substratum, the locus | 7th locative |
| **karma** (object) | 1.4.49 | *kartur ipsitatamam karma* | what the agent **most** desires to obtain | 2nd accusative |
| **kartr** (agent) | 1.4.54 | *svatantrah karta* | the independent one | 3rd, or unmarked when expressed by the verb ending |

Plus **1.4.55 *tatprayojako hetush ca*** — the instigator of that agent is *hetu* and is also called *kartr*, giving the causative agent [P].

**The superlatives are the disambiguation mechanism.** *sadhakatamam*, *ipsitatamam* — "most effective," "most desired." Not decoration: they force a unique assignment when several participants could qualify.

**Is karaka semantic or syntactic? Genuinely unsettled.**
- The standard framing is **syntactico-semantic**: an intermediate level. Not case (many karakas map to non-default cases; the genitive is a case with no karaka), and not quite a thematic role in the Fillmore/Gruber sense (assignment is sensitive to *vivaksha* and speaker construal, not purely to lexical semantics) [S, multiple converging].
- **Kiparsky** (LNCS 5402, 2009) [S]: the grammar is traversed by three mappings, semantics → morphosyntax → phonology, with karakas as *role types* mediating, aiming at one-to-one correspondence between roles and morphological expressions. Earlier: Joshi & Kiparsky, *Panini as a Variationist* (1979/1980); Kiparsky, *Some Theoretical Problems in Panini's Grammar* (1982) [S].
- **Cardona** [S: *Panini: A Survey of Research*, Mouton 1976; "Panini's Syntactic Categories," *JOIB* 1967; "Panini's Karakas: Agency, Animation and Identity," *JIP* 1974] holds a more strongly **semantic** reading — semantics is the basis of all derivations. Cardona also insists a karaka is *not* a "case" in the Latin/Western sense.
- **Deshpande**, "Karakas: Direct and Indirect Relationships" [S] distinguishes direct from indirect karaka relations, complicating any flat semantic-role reading.
- A dissenting position holds flatly that karaka is *neither* a semantic nor a semantic-syntactic category [W: Shreevatsa, Medium, which states explicitly that **what karakas are is still debated**] [?, original proponent unidentified].
- **Kulkarni et al.**, "Semantic Processing in Panini's Karaka System," LNCS 5402 [S] gives the concrete reason the debate exists: karaka assignment involves **both semantic and co-occurrence (distributional) conditions**.

### 1.5 Anuvritti, utsarga/apavada, asiddha — the rule-ordering machinery

**anuvritti** — a term stated in one sutra is silently carried forward into subsequent sutras until cancelled. The sutras are radically elliptical; reading the Ashtadhyayi *requires* reconstructing which words are inherited from which predecessors. The ashtadhyayi.com data repository ships explicit `anuvritti` files per sutra precisely because this is not recoverable from the bare text [W]. **[F]** Anuvritti is the compression mechanism that makes ~4,000 short sutras cover a language; it is also the single largest source of interpretive dispute, since commentaries disagree about how far a term carries.

**adhikara** — the structured form of anuvritti: a heading whose scope is an explicit block. **[F]** Functionally these are lexical-scope declarations.

**utsarga vs apavada** — general rule vs exception; the exception blocks the general rule in its domain [S: S. D. Joshi and the *Paribhashendushekhara* tradition].

**1.4.1 *a kadarad eka samjna*** — up to the sutra beginning *kadara*, only one samjna applies. A uniqueness constraint on technical-term assignment [P] [?, sutra text unverified this session].

**1.4.2 *vipratishedhe param karyam*** — "in conflict, the later operation is to be done." The master conflict-resolution metarule [P]. Traditional interpretation, established by Katyayana and Patanjali in the Mahabhashya: *para* = **later in the serial order of the text**. Of two equally applicable rules, the higher-numbered one wins.

Combined with the strength hierarchy paribhasha [W: worldsanskrit.net *sutranam balabalam*; Dharmawiki]:

> *para-nitya-antaranga-apavadanam uttarottaram baliyah*

Strength ranking, weakest to strongest: *para* (later) < *nitya* (obligatory) < *antaranga* (internally conditioned) < *apavada* (exception). This is a *Paribhashendushekhara*-tradition paribhasha, **not** a Paninian sutra.

**asiddha / asiddhavat and the tripadi.** Three sutras control visibility between rule blocks:

- **8.2.1 *purvatrasiddham*** [P] — "what follows is not-accomplished (asiddha) with respect to what precedes." This adhikara runs 8.2.1 to 8.4.68, the last three padas: the **tripadi**. Everything before it (1.1.1-8.1.74) is the **sapadasaptadhyayi**. Effect: a rule applying inside the tripadi is **invisible** to every rule before it, and on the standard reading to every earlier rule within the tripadi. So the tripadi is a strictly sequential, single-pass, non-backtracking block; the sapadasaptadhyayi is a re-entrant, best-match block where rules are re-tried until fixed point [W: Learn Sanskrit Online, "The asiddha section," which draws the contrast explicitly — before 8.2.1 "the best-matching rule is selected from available options"; after, rules apply "in order" and "we cannot go back"].
- **6.4.22 *asiddhavad atra bhat*** [P] — governs the *abhiya* block (6.4.22-6.4.129). The *-vat* makes it an **atidesha**: a *simulated* asiddha-hood, weaker than 8.2.1's real one.
- **6.1.86 *shatvatukor asiddhah*** [P] — a localized asiddha.

**Kulkarni**, "Computer Simulation of Ashtadhyayi: Some Insights," LNCS 5402 [S] describes these three as providing "a model which can be best described with privacy of data spaces" — i.e. scoping/visibility declarations, like module-private state. **Joshi & Kiparsky, "The Extended Siddha-Principle"** [S] is the standard scholarly treatment [?, venue/year unverified; PDF exists at Stanford but its argument was not read].

**[F]** The architecture reads as a two-phase rewriting system. Phase 1 is conflict-resolved and re-entrant, with an explicit resolution policy (specificity first, then several strength criteria, then textual order as tiebreak) and an explicit uniqueness constraint on term assignment. Phase 2 is sequential, single-pass, and opaque — its intermediate results hidden from phase 1. That opacity is precisely the device that produces counterbleeding/counterfeeding effects without stipulating rule order case by case.

---

## 2. What derives from it about expression

### 2.1 Patanjali's Mahabhashya on meaning and intention

Standard edition for the opening section: **S. D. Joshi & J. A. F. Roodbergen, *Patanjali's Vyakarana-Mahabhashya: Paspasahnika*, University of Poona, 1986** [S]. The points below come from summaries and from a Hindi study of the Paspasahnika [W: indianwisdomtradition.blogspot.com — a blog, but it quotes the Sanskrit and matches the standard account]. The Paspasa is the first *ahnika* of the Mahabhashya, its general introduction [W: wisdomlib; Wikipedia "Mahabhashya"].

**What is a word?** Patanjali asks *gaur ity atra kah shabdah?* — "in the case of *gauh* (cow), what is the word?" — and answers with a functional criterion [P]:

> *yenoccaritena sasna-langula-kakuda-khura-vishaninam sampratyayo bhavati sa shabdah*
> "That, by whose being uttered, there arises the cognition of the thing possessing dewlap, tail, hump, hooves and horns — that is the word."

**[F]** Note what this defines: a word is defined *by its effect on the hearer's cognition*, not by its acoustics and not by its reference. The definition is already a claim about the impression side.

**The eternity of the word-meaning relation.** The first varttika of the section is *siddhe shabdarthasambandhe* — "the word, the meaning, and their relation being *siddha*." **Patanjali glosses *siddha* as *nitya*** (eternal): the triad shabda-artha-sambandha is not established by human convention but is given [W: bvparishat discussion thread; indianwisdomtradition]. The grammar therefore does not *create* correct words; it *regulates* (*anushasana*) an already-given relation.

**Akriti vs dravya — Vajapyayana vs Vyadi.** What does a word denote, the generic form (*akriti*/*jati*) or the individual substance (*dravya*)? **Vajapyayana**: akriti — the *jati-vadin*. **Vyadi**: dravya — the *dravya-vadin*. Located at the varttikas on **A 1.2.64** [P] [?, varttika numbering varies by edition; search summaries place Vajapyayana at varttika 34 and Vyadi at 45]. Downstream consequence: on Vyadi's view sentence-meaning is *bheda*, difference among substances; on Vajapyayana's, *samsarga*, conjunction of generic entities. Patanjali's own move in the Paspasa is not to decide flatly but to work through different senses of each and re-read the varttika under each; whichever is taken as *nitya* is the one that can serve as *padartha* [?, "Patanjali accepts both" is a common textbook claim that could not be pinned to a verified passage].

**Vivaksha governing karaka assignment.** Covered at 1.3 above. The mechanism: karakas are assigned on the basis of the participant's role in the action **as the speaker construes it**, not on the basis of extralinguistic fact. The same real-world situation can therefore be encoded differently — an instrument or a locus spoken of as agent — depending on vivaksha [S: Cardona, "Panini's Karakas," *JIP*].

**Yatha laukikavaidikeshu.** The phrase (fuller: *yatha laukikavaidikeshu krtanteshu*) appears in the Paspasa, licensing examples from both ordinary and Vedic language [W: wisdomlib]. Patanjali remarks Vararuci could have said *yatha loke vede ca*, and observes that "southerners are fond of taddhita forms" — an incidental sociolinguistic note.

**Shabdapramanaka vayam — the best-sourced citation in this report.**

> *shabdapramanaka vayam; yac chabda aha tad asmakam pramanam*
> "We are those for whom the word is the means of knowledge; what the word says, that is authoritative for us."

**Located by Cardona at Mahabhashya, Paspasa, Kielhorn ed. I.11.1-2, and again ad A 2.1.1, I.366.12-13** [S: Cardona, "Panini's Karakas: Agency, Animation and Identity," *JIP*]. Significance: linguistic form, not extralinguistic fact, is the authority for grammatical analysis. **[F]** This is what underwrites vivaksha-governed karaka assignment — if the word is the evidence, then how the speaker chose to put it *is* the datum, and the world behind it is not.

**The purposes of grammar.** The varttika *rakshohagamalaghvasandehah prayojanam*, a dvandva naming five [W: indianwisdomtradition; sanskritgyan.com — Hindi study articles quoting the Sanskrit]:
1. **raksha** — protection of the Vedic text;
2. **uha** — modification/adaptation (ritual substitution of appropriate forms) [?, one summary rendered this "inference"; the Mimamsaka technical sense is almost certainly meant];
3. **agama** — correct transmission;
4. **laghu** — brevity, economy;
5. **asandeha** — removal of doubt about meaning.

Patanjali adds thirteen subsidiary purposes. Also from the Paspasa: *prayojanam anuddishya mando 'pi na pravartate* ("without aiming at a purpose, even a dull person does not act"), and *lakshyalakshane vyakaranam* ("grammar is both the *lakshya*, the data, and the *lakshana*, the rule").

Patanjali also states in the Paspasa that the meaning-conveying *shabda* is eternal and resident in the intellect, the momentary sound merely manifesting it — the seed of the sphota doctrine. Wikipedia credits Patanjali with the "first technical use" of *sphota* [W]. **[?]** How much sphota theory is genuinely in Patanjali versus read back into him by Bhartrihari and later grammarians is a real scholarly question no located source settles.

### 2.2 Bhartrihari's Vakyapadiya and sphota

**A numbering warning applying throughout.** The Vakyapadiya circulates in two incompatible numberings. **Wilhelm Rau**'s critical edition of the mulakarikas (Wiesbaden, 1977) gives Kanda I = 183 verses; **K. A. Subramania Iyer**'s editions number differently. "VP 1.142" and "VP 1.159" can denote the *same* verse. Every karika number below is edition-relative and should be checked against Rau or Iyer.

**Structure.** Three kandas: **Brahmakanda** (also *Agamasamuccaya*), **Vakyakanda**, **Padakanda** (also *Prakirnaka*) [W: wisdomlib]. Each is named from a salient word in its opening karika [W: sreenivasaraos.com — blog, unverified]. A blog mapping of Brahmakanda→pashyanti, Vakyakanda→madhyama, Padakanda→vaikhari is **an interpretive scheme, not established**; do not treat it as doctrine.

**Shabda-brahman.** **VP 1.1** [P, quoted in IEP]: "The Brahman is without beginning and end, whose essence is the Word, who is the cause of the manifested phonemes, who appears as the objects, from whom the creation of the world proceeds" (*anadinidhanam brahma shabdatattvam yad aksharam*). IEP glosses *shabda-brahman* as "the unity of all existence as the foundation for all linguistically designated individual phenomena" [W: IEP, "Bhartrihari"].

**Sphota.** From √sphut, "to burst": the meaning bursts forth on the mind [W: Wikipedia "Sphota"]. Three levels — **varna-sphota**, **pada-sphota**, **vakya-sphota**. **Important qualification: for Bhartrihari the primary meaning-bearing unit is the sentence** (*vakya-sphota*); word and phoneme levels are analytic abstractions [W: IEP — "the meaning-unit, which for him is the sentence, as a single entity"; Wikipedia concurs]. Nageshabhatta (18th c., *Sphotavada*) later distinguishes eight kinds.

**Sphota vs dhvani.** Sphota is the manifested (*vyangya*); dhvani is the manifester (*vyanjaka*). The relation is **manifestation, not causation** — **VP I.97** [P, via wisdomlib's study of Vacaspati Misra's *Tattvabindu*]. Related karikas from the same source:
- **VP I.44** — the word has two aspects, one underlying sound-production, one attached to meaning [P].
- **VP I.46** — *shabdo buddhisthah*, the word as a psychical entity resident in the intellect [P].
- **VP I.50** — *atmarupam yatha jnane jneyarupam ca drshyate / artharupam tatha shabde svarupam ca prakashate*: as in cognition both its own form and the form of the knowable appear, so in the word both its own form and the form of the meaning shine forth [P].

**Nada.** Some presentations distinguish *nada* (gross audible sound, an aggregate of subtler dhvanis) from *dhvani*; others treat them as near-synonyms [W: sreenivasaraos.com vs Wikipedia]. **The terminological division is not uniform across sources; report the disagreement rather than picking one.**

**Prakrta vs vaikrta dhvani.** The standard modern reconstruction, attributed to **Staal** [S], is three-way:
1. **sphota** — the expression as a single meaning-bearing unit;
2. **prakrta-dhvani** — the phonological structure assigned to the *type*: the sequence, duration and qualities specified by the language system;
3. **vaikrta-dhvani** — the phonetic realization in a particular *token*, varying with speaker tempo, accent, idiosyncrasy.

**Verse reference contested in the sources** [?]: one summary gives VP 1.78, wisdomlib gives I.76-I.77, and wisdomlib elsewhere attaches *iha dvividho dhvanih, prakrto vaikrtash ca* to "I.142" — which is probably a **Vritti** passage on the 1.76-78 area, i.e. a numbering or attribution error. Verify before quoting a number. **Bronkhorst, "Studies on Bhartrihari, 8: *Prakrta Dhvani* and the Samkhya *Tanmatras*"** (*JIP*) [S] connects prakrta dhvani to the tanmatra doctrine; the paper was not read, so attribute nothing beyond the title.

**Invariance.** Variation in dhvani — speed, loudness, dialect — does not alter the sphota [W: Wikipedia; sreenivasaraos.com].

**[F]** Prakrta/vaikrta dhvani is a **type/token split in the signal**, sitting below the meaning-unit. Combined with the sphota/dhvani manifestation relation, Bhartrihari has three distinct strata in what a modern account would collapse into "the sound": the invariant meaning-unit, the language-specified phonological form, and the physical realization. The interfaces between them are named (manifestation; superimposition of sequence).

**Krama vs akrama — the load-bearing problem.** How does a temporally sequenced sound yield a partless meaning-unit?

**VP I.48** [P, via wisdomlib]:
> *nadasya kramajanmatvat na purvo naparash ca sah / akramah kramarupena bhedavan iva jayate*
> "Because sound is born in sequence, the sphota is neither prior nor posterior; being sequenceless (*akrama*), it appears **as if** possessed of parts, in the form of sequence."

The *iva* ("as if") is the crux: **sequence and division belong to the manifesting medium, not to the manifested unit.** **VP I.49** gives the reflection analogy — the moon in moving water: the sphota is one and unchanging; the sound produces the appearance of multiplicity [P].

**This was contested.** **Kumarila Bhatta** (Mimamsa, 7th c.) argued the sphota is composed of smaller units notwithstanding the holistic cognition; **Jayanta Bhatta** (Nyaya, 9th c.) pressed compositionality. Mimamsa and Nyaya generally held the *khanda-paksha* (part-ist position) against the grammarians' holism [W: Wikipedia "Sphota"]. Vacaspati Misra's *Tattvabindu* is a major locus.

**Matilal** (*The Word and the World*, OUP 1990) [S]: thought involves vibrations having sound-like properties, and thought is impossible without language — Wikipedia characterizes this as broadly Whorfian [W] [?, "Whorfian" is Wikipedia's framing, not Matilal's word]. **A. B. Keith** dismissed sphota as mystical; modern consensus treats the sphota/dhvani distinction as psychological/linguistic rather than mystical [W: Wikipedia].

**Pratibha.** The instantaneous flash in which meaning is grasped whole. IEP describes it as "an instantaneous flash" and identifies it with *shabda* itself, "the very same speech principle," operating in the hearer [W: IEP]. **VP 2.143-152**, with the identification of pratibha with sentence-meaning around **2.143-145**: once individual word-meanings are grasped, "an altogether different insight (*pratibha*) arises" [P, via search summaries of the *JIP* literature].

**Aklujkar (1970)** on pratibha [S, quoted at second hand — verify against his Harvard dissertation *The Philosophy of Bhartrihari's Trikandi* before quoting verbatim] [?]: "a cognition that immediately precedes an action..., a cognition of the know-how type that paves the way to the desired action." Tied to *itikartavyata* — knowing-what-is-to-be-done. **On this reading pratibha is practical, non-representational, action-oriented knowledge, not a mental picture of a state of affairs.** Also: Honda, "Bhartrihari on Sentence and its Meaning as *pratibha*," *JIBS* 46.2 (1998) [S].

**[F]** Aklujkar's reading, if right, is the most important single datum in this report for an anatomy of *reacting*: the terminus of comprehension is not a representation but a disposition to act. That places the boundary between understanding and reacting somewhere other than where a representational model would put it.

### 2.3 The levels of speech: para, pashyanti, madhyama, vaikhari

**The attribution caution is correct and confirmed.**

**Bhartrihari names three: pashyanti, madhyama, vaikhari.** The key karika, **VP 1.159** in Rau numbering (= the ~1.142 area in Iyer numbering) [P, via sreenivasaraos.com; SARIT's digital text returned HTTP 502 during research, so the Sanskrit rests on a blog source — **verify against Rau**] [?]:

> *vaikharya madhyamayash ca pashyantyash caitad adbhutam / anekatirthabhedayas trayya vachah param padam*
> "This is the wondrous supreme state (*param padam*) of the threefold Speech (*trayi vak*), which has many divisions — of vaikhari, madhyama and pashyanti."

Note: the verse itself uses *param padam*, "supreme state," **of the threefold speech**. That is a plausible seed for the later fourth level but is not itself a fourth level named *para vac*.

**"Para" as a fourth level is not named by Bhartrihari.** Explicit: "Bhartrihari does not specifically name Para, pure consciousness, as the source of all speech," and "Bhartrihari regards levels of speech as three, while Abhinavagupta discusses four" [W: sreenivasaraos.com]. Some scholars argue Bhartrihari's *shabda-tattva* "virtually equates to" Abhinavagupta's *para vac* — **report this as a harmonizing interpretation by later readers, not as Bhartrihari's doctrine** [W, which itself frames it as scholars "trying to reconcile that seeming difference"].

A related dispute: even *pashyanti* as the highest is contested in emphasis. The **Vritti on VP 1.14** presents pashyanti as the supreme reality, shabda-brahman, identified with pratibha. **[F]** If that is right, pashyanti in Bhartrihari occupies structurally the place *para* occupies in Trika — which is why the fourth level looks like a Shaiva addition rather than a recovery.

**The Vritti's authorship is itself disputed, and this matters** because much of the *staged* description comes from the Vritti, not the karikas:
- **Single authorship** (karika-author = Vritti-author = Bhartrihari): Subramania Iyer, Aklujkar; Houben accepts it for Kandas I-II [S].
- **Separate authorship**: Biardeau, Bronkhorst [S]; Aklujkar has criticized them.
Consequence: claims of the form "Bhartrihari says pashyanti is X" should be qualified as "the Vakyapadiya-Vritti says," since on Biardeau's and Bronkhorst's view that is a different author.

**What each level is** (composite from sreenivasaraos.com [W] and Wikipedia [W]):

| Level | Character |
|---|---|
| **para** (Shaiva addition) | Transcendent, undifferentiated consciousness; unmanifest source. Abhinavagupta: "all dealings, whether of knowledge or action, arise in an undifferentiated way." |
| **pashyanti** ("the seeing one") | Latent, visualized-but-unspoken. **Indivisible and without temporal sequence (*akrama*)**. Identified in the Vritti with *pratibha*. Abhinavagupta: "the initial field in the order of succession; only a germ of difference." |
| **madhyama** ("intermediate") | The *buddhi* stage; inner dialogue. Words and constructions are selected; sequence and the knower/known distinction appear **inwardly**, but no audible sound. |
| **vaikhari** ("articulated") | Overt, gross, audible, sequenced speech, produced by the vocal organs, heard by external senses. |

**A discrepancy to flag.** Wikipedia's "Sphota" article glosses the three as *speaker's conceptualization (pashyanti) → performance of speaking (madhyama) → comprehension by the interpreter (vaikhari)*. That last gloss — vaikhari as the **hearer's comprehension** — is anomalous relative to every other source consulted. Treat the Wikipedia gloss as unreliable on this point.

**As a staged model.** Production: undifferentiated speech-principle → pashyanti (whole, sequenceless intention-meaning) → madhyama (inner sequencing in buddhi, word selection) → vaikhari (articulated dhvani). Comprehension: the reverse — vaikhari at the ear → madhyama (inner reconstruction) → pashyanti / pratibha (the whole grasped at once). **[?] The reverse-order comprehension staging was not found stated as such in any karika; it is a reconstruction from the doctrine plus the pratibha material. Do not present it as an explicit Vakyapadiya teaching.** [W: sreenivasaraos.com; Padoux, *Vac*, described as showing how the levels "develop into articulate speech and discursive thought"].

### 2.4 The comprehension side, stage by stage

The standard reconstruction, chiefly from **Harold G. Coward, *The Sphota Theory of Language: A Philosophical Analysis*, Motilal Banarsidass 1980/1997** [S]:

1. **Dhvani/nada strikes the ear.** The utterance arrives temporally extended.
2. **Successive varna-cognitions.** Each phoneme is cognized in turn; each perishes as the next arrives. **This is the problem**: no two phonemes coexist, so no assemblage of them is ever present at once.
3. **Samskaras accumulate.** Each cognition leaves a memory trace; each successive cognition is aided by the traces of its predecessors.
4. **The final sound, aided by the traces, reveals the sphota.** Coward's analogy (also traditional): successive glimpses of a gem, culminating in a last cognition that, helped by prior samskaras, apprehends the thing fully.
5. **Pratibha — the flash.** Coward: "a moment of recognition, an instantaneous flash whereby the hearer is made conscious, through hearing sounds, of the latent meaning-unit already present in his consciousness." Uttering the nada "induces the same mental state or sphota in the listener."
6. **Artha.** The meaning is had, whole and at once.

**On "pratyabhijna" as the name for step 4-5: caution.** Sources describe the step as *recognition*, and the samskara-plus-final-cognition mechanism has the structure of recognitive cognition — but **no source was found using the technical term *pratyabhijna* for this step in the grammarians' own vocabulary.** *Pratyabhijna* is the Kashmir Shaiva technical term (Utpaladeva's *Ishvarapratyabhijnakarika*). The label may be an importation from Trika [?].

**Further caution.** The six steps are essentially the *epistemology of sphota-manifestation* as worked out by later Vyakarana (Mandana Misra's *Sphotasiddhi*, Nagesha's *Sphotavada*) and reconstructed by Coward. Bhartrihari's own karikas are far more compressed. **Do not present the six steps as a Vakyapadiya passage.**

### 2.5 The Kashmir Shaiva elaboration

**Scope note: everything in this subsection is second-hand. No Sanskrit text was reached.**

**Abhinavagupta** develops the four-level scheme most systematically in the **Tantraloka** and the **Paratrishika-vivarana** [W: sreenivasaraos.com; Jaideva Singh's translation, *Para-trishika-Vivarana of Abhinavagupta*, Motilal Banarsidass]. Read as a graded descent from undifferentiated transcendence to gross differentiation (and, in practice, an ascent for the yogin). **[?] Paraphrase of a paraphrase; verify against Singh before quoting.**

The standard scholarly monograph is **André Padoux, *Vac: The Concept of the Word in Selected Hindu Tantras*, SUNY 1990** [S] — the only systematic English study of the doctrines of the Word in the Kashmirian Shaiva tantras; it treats how the levels of the Word abide in the human being, their linkage to kundalini, and their development into articulate speech and discursive thought. **Padoux was not read.** This is the book that would settle whether *para* is a Shaiva addition to Bhartrihari.

**Utpaladeva: negative finding.** No source attributes a specific four-levels-of-vak elaboration to Utpaladeva as distinct from Abhinavagupta. Bhartrihari's influence on the Pratyabhijna school is well known, and the *Ishvarapratyabhijnakarika* is the doctrinal basis Abhinavagupta comments on, but **do not assert a distinct Utpaladeva treatment of the four levels.**

**Cakra correspondences.** A widely repeated mapping: para at the *karanabindu* in muladhara; pashyanti at manipura; madhyama at anahata; vaikhari at vishuddhi. With the image: "The Vak which sprouts in Para gives forth leaves in Pashyanti, buds forth in Madhyama, and blossoms in Vaikhari." **This is credited to the *Yoga-Kundalini Upanishad*, not to Abhinavagupta or Bhartrihari** [W: sreenivasaraos.com]. Other popular sources give **different** mappings (pashyanti at the navel). **The cakra correspondence is not stable across the tradition; report it as one scheme among several and do not attribute it to Bhartrihari at all.**

**Matrka and malini.** *Matrka* ("the little mother"): the fifty Sanskrit varnas taken as the power of sound inherent in the alphabet and as **the basis of limited, bound knowledge**. When the power is unrecognized, matrka "impels people towards all kinds of worldly activities"; recognized, it leads to liberation. Words formed of letters shape ideas and thereby obstruct realization. Textual anchors reported: **Shiva Sutra I.4** *jnanadhishthanam matrka* ("the ground of bound knowledge is Matrka") and the Tantraloka [W: philosophicain.wordpress.com — **a personal WordPress site, low authority; its Tantraloka citation is malformed and unverifiable**]. **Malini** — the non-sequential "garland" arrangement of the same fifty phonemes, associated with the *Malinivijayottara-tantra* — **is a genuine gap: no reliable account of the matrka/malini contrast was reached.** Padoux's *Vac* and Tantraloka ahnikas 3 and 15 would be the sources.

**[F]** The matrka doctrine, if the reporting is even roughly right, is the one place in this material where the phoneme inventory itself is claimed to be constitutive of bound cognition rather than a neutral vehicle. That is a strong claim and it is exactly the kind that needs a primary text before use.

---

## 3. Branches into psychology

### 3.1 Samkhya: the antahkarana and the thirteenfold instrument

Verse numbers below were independently verified by the researcher against Sanskrit on two sites [W: yogasutrastudy.info; scriptures.redzambala.com; cross-check yogastudies.org]. Standard scholarly treatment is Gerald Larson, *Classical Samkhya* [S, not fetched].

**The three internal organs:**
- **Buddhi = adhyavasaya** (determination, ascertainment). **SK 23** [P]: *adhyavasayo buddhir dharmo jnanam viraga aishvaryam...* Its sattvic modes are dharma, jnana, viraga, aishvarya; tamasic modes their opposites. Also called *mahat*.
- **Ahamkara = abhimana** (self-appropriation, "I-making"). **SK 24** [P]: *abhimano 'hankaras tasmad dvividhah pravartate sargah* — from ahamkara proceed the eleven organs and the five tanmatras.
- **Manas = samkalpaka, ubhayatmaka**. **SK 27** [P]: *ubhayatmakam atra manah samkalpakam indriyam ca sadharmyat* — manas partakes of both natures (sensory and motor), is the deliberating and coordinating faculty, and is itself counted an indriya.

**Specific vs common function. SK 29** [P]: each of the three has its own peculiar function; the function common to all instruments is the five vital airs.

**The order-of-operation question — simultaneous or successive. SK 30** [P]:
> *yugapac catushtayasya tu vrttih kramashash ca tasya nirdishta / drshte tathapy adrshte trayasya tat-purvika vrttih*
> "The function of the four [buddhi, ahamkara, manas + one external sense] with respect to a seen object is declared to be both simultaneous (*yugapat*) and successive (*kramashah*); with respect to the unseen, the function of the three internal organs is preceded by that."

**Vacaspati Misra's *Tattvakaumudi*** supplies the standard illustration [S, via wisdomlib essay on Vacaspati's contribution]: a man sees a tiger by a lightning flash and flees — sense, manas, ahamkara, buddhi "seem to occur at the same moment, though really they are successive." The successive case: eye grasps form → manas particularises (*samkalpa*) → ahamkara appropriates ("this concerns me") → buddhi decides.

**Disagreement on the handoff** [S, same essay]: **Vacaspati** holds the external senses yield only indeterminate (nirvikalpaka) content which manas renders determinate; **Vijnanabhikshu** (*Samkhyapravacanabhashya*) holds both determinate and indeterminate perception are delivered by the senses themselves [?, primary wording not retrieved].

**Motive. SK 31** [P]: *svam svam pratipadyante parasparakuta-hetukam vrttim / purushartha eva hetur na kenacit karyate karanam* — the instruments perform their functions prompted by mutual impulse; the sole motive is purusha's purpose; no other agent drives the instrument.

**The thirteenfold karana. SK 32** [P]: thirteen instruments (buddhi, ahamkara, manas, 5 buddhindriyas, 5 karmendriyas) doing seizing, holding, illuminating; tenfold object. Commentators diverge on which organs do which (Gaudapada vs Vacaspati vs Mathara) [W]. **SK 33** [P]: internal organ threefold, external tenfold; **external operates only in the present, internal in all three times.**

**Doorkeepers and doors. SK 35** [P]: since buddhi with the other internal organs "dives into" every object, the three internal organs are the **doorkeepers (*dvarin*)**, the rest are the **doors (*dvara*)**. **SK 36** [P]: these, like a lamp, illuminate the whole object for purusha's sake and present it to buddhi. (The clause "buddhi presents all to purusha" is strictly **SK 37**; the 36/37 split is often blurred in summaries.)

**[F]** The dvarin/dvara distinction is an interface statement: the senses are ports, the internal organs are the processes that hold the ports. And SK 33's temporal asymmetry — external instruments present-only, internal tri-temporal — is a clean statement of what each stage can and cannot address.

### 3.2 Yoga Sutra psychology

Sanskrit verified against Woods (Harvard Oriental Series 1914) [P] and Vivekananda [W].

**Citta and vritti.** **YS 1.2** *yogash citta-vrtti-nirodhah*. **1.3** *tada drashtuh svarupe 'vasthanam*. **1.4** *vrtti-sarupyam itaratra* — "at other times the seer takes the same form as the vrittis." **[F]** 1.4 is a statement about the default failure mode: identification with the content of cognition.

**The five vrittis.** **1.5** *vrttayah pancatayyah klishtaklishtah* (afflicted / unafflicted). **1.6** *pramana-viparyaya-vikalpa-nidra-smrtayah*. **1.7** *pratyakshanumanagamah pramanani* — three pramanas: perception, inference, testimony. **1.8** *viparyayo mithya-jnanam atad-rupa-pratishtham* (error = false cognition not grounded in the thing's form). **1.9** *shabda-jnananupati vastu-shunyo vikalpah* — vikalpa is cognition that follows on word-knowledge yet is empty of an object. **1.10** sleep is a vritti whose object is absence. **1.11** *anubhuta-vishayasampramoshah smrtih* (memory = non-loss of an experienced object). All [P].

**[F]** YS 1.9 is the first place the tradition separates word-driven content from object-driven content, and it names the word-driven kind as a *distinct type of mental event*, not as a defective perception.

**Samapatti stages.** **1.17** *vitarka-vicaranandasmita-rupanugamat samprajnatah* [P]. **1.42** *tatra shabdartha-jnana-vikalpaih samkirna savitarka samapattih* — savitarka samapatti is that in which **word, object, and cognition are commingled (*samkirna*)** [P]. **1.43** when memory is purified, the state shines as the object alone, as if empty of its own form: nirvitarka [P]. **1.44** the same explains savichara/nirvichara on subtle objects [P].

**Samskara and vasana.** **1.18** asamprajnata: only samskara remains [P] [?, standard wording, not re-fetched]. **1.50** the samskara born of nirvichara insight obstructs other samskaras. **4.8** only those vasanas manifest that correspond to karmic fruition. **4.9** *jati-desha-kala-vyavahitanam apy anantaryam smrti-samskarayor eka-rupatvat* — **memory and samskara are of one form**, hence causal continuity across birth, place, time. **4.10** samskaras are beginningless. **4.11** *hetu-phalashrayalambanaih samgrhitatvad esham abhave tad-abhavah* — samskaras are held together by cause, fruit, substrate, and object; remove these and they cease. All [P]. **Cycle: samskara → (conditions) → vritti/experience → new samskara.**

**Klesha as a model of reaction.** **2.3** *avidyasmita-raga-dvesabhinivesah panca kleshah* [P]. **2.4** avidya is the field of the others, whether dormant, attenuated, intercepted, or active. **2.5** avidya = taking the impermanent/impure/painful/non-self for their opposites. **2.6** *drg-darshana-shaktyor ekatmateva asmita* — asmita = seer and instrument appearing as one self. **2.7** *sukhanushayi ragah*; **2.8** *duhkhanushayi dveshah* — **attachment and aversion as residues (*anushayin*) following pleasure and pain.** **2.9** *sva-rasa-vahi vidusho 'pi tatha rudho 'bhiniveshah* — clinging to life flows by its own momentum even in the wise. **2.10** subtle kleshas removed by *pratiprasava* (involution to source); **2.11** their active vrittis by dhyana. **2.12** *klesha-mulah karmashayah*. **2.13-2.14** fruits according to merit/demerit. **2.15** for the discriminating, all is duhkha because of change, anxiety, samskara, and the conflict of the gunas' operations. All [P].

**Reaction chain as the sutras give it:** avidya → asmita → raga/dvesha → action → karmashaya → samskara → renewed vritti.

**[F]** YS 2.10-2.11 gives a two-level intervention model: active vrittis are handled by one method (dhyana), latent kleshas by another (pratiprasava). An anatomy that only addresses the active layer would, on this account, leave the generator intact.

**YS 3.17 — the sutra on shabda, artha, pratyaya.** Directly relevant; reported carefully; verified by the researcher.

**[P]** *shabdartha-pratyayanam itaretaradhyasat samkaras tat-pravibhaga-samyamat sarva-bhuta-ruta-jnanam.*

- **Rama Prasada (1924)**: "The word, the object and the idea appear as one, because each coincides with the other; by Samyama over their distinctions comes the knowledge of the sounds of all living beings."
- **Woods (1914)**: "Word and intended-object and presented-idea are confused because they are erroneously identified with each other. By constraint upon the distinctions between them there arises knowledge of the cries of all living beings."

Three distinct relata — **shabda** (sound/word), **artha** (object denoted), **pratyaya** (the cognition/idea) — are habitually fused by *itaretara-adhyasa* (mutual superimposition), producing *samkara* (confusion), so that cow-word, cow-object and cow-idea are experienced as one thing.

**Vyasa's Bhashya** [P, wisdomlib]: speech emits discrete phonemes in sequence; hearing registers only these; **buddhi grasps the word as a unity only at the last phoneme**; the word-object relation is *samketa* (convention), which Vyasa calls "a manifestation of memory showing the mutual correlation of word and meaning in the shape of coincidence."

**[F]** Vyasa's "buddhi grasps the word as a unity only at the last phoneme" is structurally the same mechanism as Coward's step 4 in the sphota reconstruction (2.4 above), arrived at in a different school. Two traditions independently locate the unification at the terminal element of the sequence. That convergence is worth noting; it is not a borrowing claim.

### 3.3 Nyaya: pramanas, perception, inference, testimony

Primary: Ganganatha Jha, *The Nyaya-Sutras of Gautama* with Vatsyayana's Bhashya [P]. Secondary: SEP "Epistemology in Classical Indian Philosophy" (Phillips & Vaidya); SEP "Perceptual Experience and Concepts in Classical Indian Philosophy" (Chadha); SEP "Analytic Philosophy in Early Modern India" (Ganeri) [S].

**Four pramanas. NS 1.1.3** *pratyakshanumanopamanashabdah pramanani* [P]. **NS 1.1.4** [P]: *indriyartha-sannikarshotpannam jnanam avyapadeshyam avyabhicari vyavasayatmakam pratyaksham* — "Perception is that knowledge which arises from the contact of a sense with its object and which is determinate, unnameable and non-erratic" (Jha). Vatsyayana's glosses: *sannikarsha* excludes inference; *jnanam* excludes pleasure/pain; *avyapadeshya* excludes verbal cognition; *avyabhicari* excludes illusion; *vyavasayatmaka* excludes doubt. **1.1.5** anumana: purvavat, sheshavat, samanyatodrshta. **1.1.6** upamana. **1.1.7** *aptopadeshah shabdah*. **1.1.8** shabda is drshtartha or adrshtartha. All [P].

**Nirvikalpaka → savikalpaka — disagreement reported, and it is substantial.** The distinction is **not** in the Sutra, the Bhashya, or Uddyotakara's Varttika. **Vacaspati Misra** (c. 10th c., following Trilocana) read *avyapadeshyam* as nirvikalpaka and *vyavasayatmakam* as savikalpaka and claimed Gautama implied it; Jayanta Bhatta is also credited with an early division; **Gangesha** built the developed causal argument. **Chadha (SEP)** [S] reports **Pradyot Mondal (1982)** showing most Naiyayikas read the terms as plain exclusions, not as endorsing two perception-types; contemporary dispute continues between **Stephen Phillips** (defending an indeterminate stage) and **Arindam Chakrabarti** (denying it is needed). Contrast: **Dignaga**'s pratyaksha is *kalpanapodha* (free of conceptual construction), **Dharmakirti** adds *abhranta* — for Buddhists only the non-conceptual stage is perception; for Nyaya both stages are.

**Sannikarsha — the six laukika contact types** (Tarkasamgraha) [W: wisdomlib]: samyoga (eye-pot); samyukta-samavaya (colour inhering in the conjoined pot); samyukta-samaveta-samavaya (colourness in that colour); samavaya (sound in the ear's akasha); samaveta-samavaya (soundness in sound); visheshana-visheshya-bhava (absence of a pot on the ground) [?, exact wording for items 3 and 5 not pulled from primary]. **Alaukika** types: samanyalakshana, jnanalakshana (seeing "fragrant sandalwood"), yogaja.

**The five-membered syllogism. NS 1.1.32** *pratijna-hetudaharanopanaya-nigamanany avayavah*; **1.1.33** *sadhya-nirdeshah pratijna*; **1.1.34** *udaharana-sadharmyat sadhya-sadhanam hetuh*; **1.1.35** *tatha vaidharmyat*; **1.1.36-37** homogeneous and heterogeneous udaharana; **1.1.38** upanaya; **1.1.39** *hetv-apadeshat pratijnayah punar-vacanam nigamanam*. All [P].

Worked: (1) the mountain has fire; (2) because it has smoke; (3) whatever has smoke has fire, like a kitchen; (4) the mountain has smoke pervaded by fire; (5) therefore the mountain has fire.

**The internal psychological steps.** *vyapti-jnana* (knowledge of pervasion) + *paksha-dharmata-jnana* (the reason is in the subject) → **linga-paramarsha** (*parvato vahni-vyapya-dhumavan*, "this mountain has smoke pervaded by fire"), which **Annambhatta's Tarkasamgraha names the *karana* of *anumiti*** (the inferential cognition *parvato vahniman*) [W: wisdomlib Tarkasamgraha essay]. **The five-member form is for *pararthanumana* (demonstration to others); the three-step private process is *svarthanumana*.** That distinction originates with **Dignaga** (*Pramanasamuccaya*) and is adopted by Annambhatta.

**[F]** The svartha/parartha split is an explicit separation of the *thinking* pipeline from the *communicating* pipeline, with the same content passing through both in different formats. It is the closest thing in this material to an explicit interface between cognition and expression, and it is stated as a difference of *number of stages* — three private, five public.

**Shabda as testimony.** *apta* = *yathartha-vakta* (Tarkasamgraha). **Disagreement:** early Vaisheshikas (per Shridhara) and Buddhist logicians **reduce testimony to inference** (the utterance is a sign, the speaker's reliability the pervasion); **Nyaya insists shabda is sui generis** because its certification conditions differ [S: SEP epistemology-india; W: wisdomlib] [?, primary Dharmakirti passage unverified].

### 3.4 Mimamsa and Navya-Nyaya on sentence meaning

Secondary: Malcolm Keating, SEP "Language and Testimony in Classical Indian Philosophy" and "The Literal-Nonliteral Distinction in Classical Indian Philosophy" [S]; K. Kunjunni Raja, *Indian Theories of Meaning* (Adyar 1963) [S]; Jonardon Ganeri, *Semantic Powers* (OUP 1999) [S].

**Conditions of *shabdabodha* (verbal cognition):**
- **akanksha** — syntactic expectancy between words.
- **yogyata** — semantic fitness. Standard failure case: *vahnina sincati*, "he sprinkles with fire."
- **sannidhi / asatti** — contiguity; words uttered without undue gap.
- **tatparya** — speaker's intention. **[P]** Vishvanatha, *Nyayasiddhantamuktavali* on *Bhashapariccheda* v. 84: *vaktur iccha tu tatparyam parikirtitam*.

The triad as a codified definition of "sentence" is standard in Annambhatta's *Tarkasamgraha* and Vishvanatha's *Bhashapariccheda*/*Muktavali*; rigorous analysis in Gangesha's *Tattvacintamani* Shabdakhanda. The originating sutra in Jaimini/Shabara was not pinned [?].

**Who accepts tatparya — a real disagreement.**
- **Naiyayikas including Navya-Nyaya** (Gangesha, Vishvanatha) accept it as a fourth necessary condition, needed to resolve ambiguity — *saindhavam anaya*, "bring the salt" / "bring the horse."
- **Bhatta Mimamsakas** (Kumarila's school) **reject** it as a distinct condition: the Veda is *apaurusheya*, so no speaker-intention can ground Vedic meaning; the unifying work is done by the abhihitanvaya mechanism instead.
- **Prabhakaras** do not need it structurally, since on anvitabhidhana words already denote connected meanings.
- **Vacaspati Misra** reconciles by grounding "tatparya" in elders' usage (*vyavahara*) rather than psychological intention [S: Keating].
- Jayanta Bhatta and Abhinavagupta treat tatparya as a **separate semantic power**.
[?] The Bhatta-vs-Prabhakara contrast *in reasons* is the researcher's synthesis; no single source states it in those terms.

**Anvitabhidhana vs abhihitanvaya — how word-meanings combine.**
- **abhihitanvaya** (Kumarila Bhatta; Bhatta school; **Nyaya sides with this**): words first denote isolated meanings via *abhidha*; a **second operation** connects (*anvaya*) the already-denoted (*abhihita*) meanings, aided by akanksha/yogyata/sannidhi. Sentence-meaning is a distinct subsequent cognition. [W: Hindupedia; S: Kunjunni Raja]
- **anvitabhidhana** (Prabhakara Misra; "Guru" school): words denote their meanings **as already connected** (*anvita*); Shalikanatha says construction is "never a subsequent function" but presupposed in utterance. Support: the ***vrddha-vyavahara* argument** — a child learns from watching elders' commands ("bring the cow") and the ensuing action, first grasping whole-sentence-to-situation correlation, only later isolating word-meanings by *anvaya-vyatireka*; hence relational meaning is primary. [S: Kunjunni Raja p. 26; W: wisdomlib] [?, primary Prakaranapancika passage not pulled]
- **Third alternative**: Bhartrihari's sphota — the sentence is an indivisible meaning-bearer grasped by *pratibha*; words are heuristic fictions. **Rejected by both Mimamsa and Nyaya** [S: Keating; Kunjunni Raja ch. 3].

**Staged sequence:** *padajnana* (word-cognition) → *padartha-smrti* (recollection of meaning via *shakti*/*samketa*) → *anvaya* (connection under the conditions) → *shabdabodha*. Individual stages are well attested; the four-term formula as a single canonical quotation was not located [?]. Navya-Nyaya treats *padajnana* as the *karana* of *shabdabodha*.

**[F]** This is the sharpest three-way disagreement in the material about *where composition happens*: as a second step after denotation (Nyaya/Bhatta), inside denotation (Prabhakara), or nowhere because there are no parts (Bhartrihari). Any anatomy that puts a "compose the meaning" stage in the pipeline is taking the abhihitanvaya side of a live dispute, and should say so.

### 3.5 Rasa and bhava: the model of reaction and impression

Primary: Natyashastra ch. 6, Manomohan Ghosh translation [P/W: wisdomlib]. Secondary: Sheldon Pollock, *A Rasa Reader* (Columbia UP 2016); Raniero Gnoli, *The Aesthetic Experience According to Abhinavagupta* (Chowkhamba 1968); Ingalls/Masson/Patwardhan, *The Dhvanyaloka of Anandavardhana with the Locana of Abhinavagupta* (HOS 49, 1990); Keating SEP [S].

**The rasa-sutra** [P]:
> *vibhavanubhava-vyabhicari-samyogad rasa-nishpattih*
> Ghosh: "The Sentiment is produced from a combination of Determinants, Consequents and Complementary Psychological States."

**Citation convention:** it is a **prose** sutra following verse 31 of chapter 6; cited as "NS 6.31" or "NS 6, prose after 31." (One auto-summary gave "7.31" — an error, not a variant.)

**Components.** *vibhava* (determinants — the alambana/uddipana subdivision is later systematisation, not pinned to an NS verse [?]); *anubhava* (visible consequents); *vyabhicari*/*sancari-bhava* (33 transitory states, named in ch. 6, elaborated in ch. 7); *sattvika-bhava* (8: stambha, sveda, romanca, svarabheda, vepathu, vaivarnya, ashru, pralaya); *sthayi-bhava* (8 stable emotions).

**Rasas and their sthayibhavas** [P]: shringara/rati, hasya/hasa, karuna/shoka, raudra/krodha, vira/utsaha, bhayanaka/bhaya, bibhatsa/jugupsa, adbhuta/vismaya.

**Shanta** (the 9th) is **not** among Bharata's eight: first argued for by Udbhata (c. 800), carried by Anandavardhana, defended philosophically by Abhinavagupta (linked to moksha); its sthayibhava is disputed between *shama* and *nirveda*; its presence in extant NS manuscripts is regarded by many scholars as interpolation. Vatsalya (10th) and bhakti-rasa (Rupa Gosvamin, 16th c.) are later.

**The four commentators — a genuine four-way disagreement about the mechanism of impression.** All three pre-Abhinavagupta views survive chiefly as quoted and refuted in Abhinavagupta's *Abhinavabharati*; their own works are lost. **Pollock and others warn that the doxographic sharpness is partly Abhinavagupta's rhetorical framing** [S].

1. **Bhatta Lollata** (c. 825) — ***utpatti-vada***: rasa is the sthayibhava **produced** and intensified (*upacita*) by the vibhavas; located primarily in the character, secondarily in the actor by imitation; the spectator experiences it by attribution (*aropa*).
2. **Shri Shankuka** (c. 850) — ***anumiti-vada***: the spectator **infers** the emotion from the vibhavas as signs, Nyaya-style; the actor is apprehended under the *citra-turaga-nyaya* (painted-horse analogy): neither truly the character, nor false, nor doubtful, nor merely similar — a sui generis cognition; rasa is inferred imitation (*anukarana*).
3. **Bhatta Nayaka** (early 10th c.; *Hrdayadarpana*, lost) — ***bhukti/bhoga-vada***: alongside *abhidha* he posits **bhavakatva** (the power that de-particularises the vibhavas — ***sadharanikarana***, universalisation, so the emotion is neither "mine" nor "his") and **bhojakatva** (the power of relishing). **Rasa is not a meaning but an experience caused by the text** [S: Keating]. [?, attribution of *vishranti* language to Nayaka himself is uncertain]
4. **Abhinavagupta** (c. 975-1025) — ***abhivyakti-vada***: rasa is **manifested** (*vyangya*), not produced or inferred; it rests on **the spectator's own latent samskaras/vasanas of the sthayibhava**, universalised (accepting sadharanikarana), and emerges when obstacles (*vighnas*) are removed; the state is *alaukika*, marked by *camatkara* and *vishranti*; requires the *sahrdaya*. Loci: *Abhinavabharati* on NS 6; *Locana* on the *Dhvanyaloka*.

**[F]** The four positions are four different answers to "where does the impression come from" — the sender (Lollata), an inference the receiver draws (Shankuka), a special power of the medium (Nayaka), or the receiver's own stored dispositions unlocked by the medium (Abhinavagupta). Any anatomy has to choose, and the choice determines whether the reaction stage is modelled as transmission, inference, or activation.

**Dhvani.** **Anandavardhana** (9th c., *Dhvanyaloka*) proposes **vyanjana** (suggestion) as a third word-power beyond **abhidha** (denotation) and **lakshana** (indication, triggered by failure of literal fit — "feed the sticks"); suggestion needs no such failure. Three types: *vastu-dhvani*, *alankara-dhvani*, *rasa-dhvani* (highest).

**Disagreement on dhvani:** **Mukula Bhatta** (Mimamsaka) reduces suggestion to *lakshana*; **Bhatta Nayaka** denies rasa is a meaning at all; **Mahima Bhatta** (*Vyaktiviveka*) reduces dhvani to **inference** via pervasion between meanings; **Abhinavagupta's *Locana*** defends dhvani and expands to **four powers: abhidha, tatparya, lakshana, vyanjana** [S: Keating; Kunjunni Raja]. There is no SEP entry titled "Rasa" or "Aesthetics in Indian Philosophy"; the relevant entry is the literal-nonliteral one.

### 3.6 Buddhist Abhidhamma: citta-vithi

Primary: *Abhidhammattha Sangaha* ch. 4 (*Vithi-sangaha*) [P]. Secondary: Bhikkhu Bodhi, *A Comprehensive Manual of Abhidhamma* (BPS 1993); Gethin, "Bhavanga and Rebirth According to the Abhidhamma"; Cousins, "The Patthana and the Development of the Theravadin Abhidhamma" (*JPTS* IX, 1981); Karunadasa, *The Theravada Abhidhamma* (2010); SEP "Abhidharma" [S].

**Five-door process, "very great" (*atimahanta*) object — 17 mind-moments** [P]:

1. *atita-bhavanga* (1)
2. *bhavanga-calana* (1) — vibration of the life-continuum
3. *bhavangupaccheda* (1) — arrest of the life-continuum
4. *pancadvaravajjana* (1) — five-door adverting
5. *panca-vinnana* e.g. *cakkhu-vinnana* (1) — bare sense-consciousness
6. *sampaticchana* (1) — receiving
7. *santirana* (1) — investigating
8. *votthapana* (1) — determining
9-15. **javana* (7)** — the kammically decisive impulsion moments
16-17. *tadarammana* (2) — registration
→ back to *bhavanga*.

17 = the lifespan of a *rupa* in mind-moments.

**By object intensity:** *atimahanta* — full process with tadarammana; *mahanta* — ends after javana; *paritta* — reaches votthapana only (repeated 2-3 times), no javana; *atiparitta* — only bhavanga-calana, no vithi arises (*mogha-vara*).

**Mind-door process:** bhavanga-calana → bhavangupaccheda → *manodvaravajjana* → javana (7) → tadarammana (2). Manodvaravajjana performs **both** adverting and determining functions. **Appana (absorption) process** for jhana/magga: *parikamma, upacara, anuloma, gotrabhu* → appana javanas; no tadarammana.

**The caveat, and it matters.** Bodhi's own Introduction [S] states that the detailed cognitive process is among "Abhidhammic conceptions that are characteristic of the Commentaries but either unknown or recessive in the Abhidhamma Pitaka itself... tacitly recognized in the canonical books" but drawn out only later; *khana* replaces canonical *samaya*; the 17-moment rupa lifespan is commentarial. *Bhavanga* occurs in the Patthana and in the paracanonical Milindapanha, Nettippakarana and Petakopadesa, **not in the Nikayas** [?, exact Patthana context unverified]. The Visuddhimagga (ch. XIV) and Atthasalini present the 14 functions (*kicca*) and the process sequence (the Atthasalini's mango simile); **the tabular systematisation with the four object-intensity classes is the *Sangaha*'s** (Anuruddha, c. 10th-12th c. per Bodhi). Correction issued by the researcher against one of its own passes: the Visuddhimagga *does* describe the process in sequence, so "not in Visuddhimagga at all" would overstate.

**Scholarly positions:** Cousins argues the Patthana's *anantara*/*samanantara* conditions supplied the scaffolding; Karunadasa places the doctrine in Buddhaghosa, Buddhadatta and Anuruddha "based on earlier descriptions in the Dhammasangani and Patthana"; **Gethin treats bhavanga as an exegetical construct solving a continuity problem the Nikayas leave open** [S] [?, primary PDFs not fetched].

**Alternatives.** *Sarvastivada/Vaibhashika*: no bhavanga; continuity via the four *samskrita-lakshanas* and tri-temporal existence of dharmas. *Sautrantika*: radical momentariness plus *bija/vasana* perfuming the *santana*. *Yogacara*: **alayavijnana** as substrate; **klishta-manas** (7th consciousness) appropriating alaya as self — **structurally parallel to ahamkara**; six *pravritti-vijnanas*; seed → manifestation → seed, **paralleling samskara → vritti → samskara**. **Schmithausen** (*Alayavijnana*, 1987) derives alaya from the *nirodhasamapatti* problem and considers direct borrowing from bhavanga **unlikely — convergence, not genealogy** [S] [?, secondary paraphrase].

**[F]** Citta-vithi is the only account in this material that assigns a *fixed number of moments* to each stage and makes the karmic weight fall on one specific stage (javana). It is also the only one with an explicit "nothing happened" outcome (*mogha-vara*) for a too-weak stimulus — a threshold. Both are structural features an anatomy can use, and neither has a counterpart in the grammarians.

---

## 4. Branches into astrology (Jyotisha)

**This section is mostly negative findings. That is the honest result and it is reported as such.**

### 4.1 "Karaka" in Jyotisha and its relation to Panini's karaka

**The word.** Sanskrit *karaka* = "doer, maker, causer, that which brings about," a *nvul*-suffix agent noun from √kr [P: Monier-Williams 1899]. Both the grammatical and the astrological technical senses are specializations of this one ordinary word.

**Jyotisha's karaka** = **significator**: the graha (or bhava) that stands for a given person or matter [W: Wikipedia "Atmakaraka"].

**The verdict — stated plainly.** **No source, primary, scholarly, or otherwise, was found that derives the astrological *karaka* from Panini's technical *karaka*, or that even discusses the two as related technical terms.** Specific negative evidence:
- **Dr. Satya Prakash Choudhary's "Light on 'Karaka'"** [W: karmicrhythms.com — the most philologically careful jyotisha treatment located, citing BPHS's *karakadhyaya*, Jaimini Sutras with Somanatha Misra's *Kalpalata*, Brihat Jataka, Phaladipika, Sarvartha Cintamani, Jataka Parijata] defines karaka purely as "significator / one who causes" and makes **zero** reference to grammar or Panini.
- A search for Pingree-style philological work on jyotisha's technical vocabulary and grammatical borrowing found nothing addressing this. (David Pingree, *Jyotihshastra: Astral and Mathematical Literature*, Harrassowitz 1981 [S] is the standard survey; its contents could not be verified online.)
- One search-engine statement asserting a "significant conceptual connection between grammatical and astrological domains" was **an AI summary artifact, not a citable source. Discount it.**

**Best-supported reading:** the two are the **same Sanskrit word independently technicalized in two shastras** — grammar's "participant-in-the-action," astrology's "causer/producer of a result." The semantic bridge is generic agentive causation (√kr), not borrowing. **Anyone asserting Jyotisha took the term from Panini is going beyond the evidence.** Note the chronology: the grammatical sense is far older (Panini, c. 5th-4th c. BCE) than the horoscopic sense (post-Hellenistic; Varahamihira 6th c. CE). *If* one wanted a directional claim it would have to be grammar → astrology — but no source establishes even that. **State it as unattested.**

### 4.2 Grahas as agents of perception and action

**Brihat Jataka of Varahamihira, ch. 2, verse 2.1** — the locus classicus [P, N. Chidambaram Aiyar translation via chestofbooks; Sanskrit/English at wisdomlib]:

> "To the Kalapurusha, the Sun is the soul, the Moon is the mind, Mars is strength, Mercury is speech, Jupiter is knowledge and health, Venus is desire, and Saturn is sorrow."

So: **Surya = atman, Candra = manas, Budha = vak, Guru = jnana, Shukra = kama, Shani = duhkha, Mangala = bala.** **Note: Mercury here is *vak* (speech), not *buddhi*.** The Mercury-as-buddhi association is a later or derived commonplace.

**BPHS ch. 3, slokas 12-13** (R. Santhanam trans.) [P]: "The Sun is the soul of all. The Moon is the mind. Mars is one's strength. Mercury is speech-giver, while Jupiter confers knowledge and happiness. Venus governs semen (potency), while Saturn denotes grief." Essentially the same verse. BPHS 3.14-15 adds the planetary cabinet.

**Phaladipika of Mantreshvara, ch. 2, sloka 26** (V. Subrahmanya Sastri trans.) gives a **different** scheme [P]: "The Moon represents the body, and the Sun, the soul. Mars and the other planets denote the five senses... Mercury governs smell; Venus and the Moon, taste; the Sun and Mars, sight; Jupiter, sound; Saturn, Rahu and Ketu, touch."

**Disagreement to flag:** Phaladipika assigns Mercury *smell* and Jupiter *sound*, which does not line up with Brihat Jataka's Mercury = speech. **The tradition is not uniform.**

**A correction to a widespread premise.** **BPHS ch. 32, "Planetary Karakatvas" (*karakadhyaya*)** — the *naisargika* (constant) karakas there are **kinship-based, not psychological** [P]: vv. 18-21 — stronger of Sun/Venus = father; stronger of Moon/Mars = mother; Mars = sister and younger brother; Mercury = maternal relatives; Jupiter = paternal grandfather; Venus = husband; Saturn = sons; Ketu = wife and in-laws. vv. 22-24 map these to houses *from* the karaka (9th from Sun = father, 4th from Moon = mother, etc.). Same doctrine at BPHS 8.39-43.

**Therefore: the popular list "Sun = atman, Moon = manas, Mercury = vak/buddhi, Jupiter = jnana" is *not* BPHS's naisargika karakas (ch. 32); it is the Kalapurusha/graha-svabhava verse (BJ 2.1 = BPHS 3.12-13). Modern writing conflates the two.**

**Phaladipika ch. XV, sloka 17** does give explicit **bhava-karakas** [P]: 1st Sun; 2nd Jupiter; 3rd Mars; 4th Moon and Mercury; 5th Jupiter; 6th Saturn and Mars; 7th Venus; 8th Saturn; 9th Sun and Jupiter; 10th Jupiter, Sun, Mercury, Saturn; 11th Jupiter; 12th Saturn. **Note Mercury is karaka of the 4th and 10th — not of the 2nd (speech) or 3rd.**

### 4.3 The Jaimini chara karakas

**BPHS ch. 32, vv. 3-8 and 13-17** [P]: the graha with the highest degrees traversed **within its sign** (ignoring which sign) is **Atmakaraka**; ties broken by minutes then seconds; for Rahu subtract from 30°. Atmakaraka is supreme "just as the king is the most famous among the men of his country." vv. 9-12: no other karaka can override the Atmakaraka. vv. 13-17: descending order gives **Amatyakaraka, Bhratrkaraka, Matrkaraka, Pitrkaraka, Putrakaraka, Jnatikaraka, Strikaraka (= Darakaraka)**. Parashara notes a school treating Matr- and Putra-karaka as identical, yielding **7** rather than 8.

**Jaimini's Upadesha Sutras, Adhyaya 1, Pada 1** [P]: the Atmakaraka definition beginning *atmadhikah kaladibhih* — of the seven grahas Sun to Saturn, or eight including Rahu, whichever gets the highest degrees becomes Atmakaraka; followed by *sa ishte bandha-mokshayoh* ("through his desire, bondage or liberation") and *tasyanusaranad amatyah*. **Numbering varies by edition** — cited as sutra 11 in Suryanarain Rao / B. V. Raman, and as 1.1.10-1.1.12 in Sanjay Rath's and the Venkatesha-commentary numbering [?]. **Do not cite a single sutra number as canonical.** Classical commentaries: Somanatha Misra's *Kalpalata*, Neelakantha's *Jaimini Sutra Bhashya*.

*Karakamsha* = the navamsha sign occupied by the Atmakaraka (BPHS ch. 33 on its effects).

**[F]** The chara-karaka scheme is the one place in Jyotisha where role assignment is *computed* rather than fixed by table — the roles are assigned by rank-ordering a continuous quantity. Structurally that resembles Panini's *superlative* disambiguation (*sadhakatamam*, "**most** effective") more than anything else in the astrological material. But this is a structural resemblance I am noting, not an attested connection, and it should not be presented as one.

### 4.4 Bhavas — the houses

**Phaladipika ch. 1, slokas 10-16** is the best classical source because it lists each house's *names and synonyms*, which is where **vak** appears explicitly [P]:

- **1st:** Lagna, Hora, Kalya, Deha, Udaya, Rupa, Shirsha, Vartamana, Janma.
- **2nd:** Vitta (wealth), **Vidya (learning)**, Sva, Annapana, Bhukti, Dakshakshi (right eye), **Asya (face/mouth)**, **Patrika (letter/document)**, **Vak (speech)**, **Kutumba (family)**. ← *the explicit classical attestation of 2nd house = vak.*
- **3rd:** Duschikya, Uras, right ear, army, **courage, valour, prowess (vikrama)**, brother.
- **4th:** house, land, maternal uncle, relations, friend, vehicle, mother, kingdom, happiness, water.
- **5th:** Rajanka, minister, Kara, **Atman**, **Dhi (intelligence)**, knowledge of the future, Asu, Suta, Jathara, **Shruti**, **Smrti**.
- **6th:** Rna (debt), Astra, Cora, Kshata, Roga, Shatru, Jnati, Aji, Dushkrtya, Agha, Bhiti, Avajna.
- **7th:** Jamitra, Cittottha (desire), Mada, Asta, Kama, Dyuna, Adhvan, Loka, Pati, Marga, Bharya.
- **8th:** Mangalya, Randhra, Malina, Adhi (mental pain), Parabhava, Ayus, Klesha, Apavada, Marana, Ashuci, Vighna, Dasa.
- **9th:** **Acarya (preceptor)**, Daivata, Pitr, Shubha, **Purva-bhagya**, Puja, **Tapas**, Sukrta, Pautra, **Japa**, Aryavamsha.
- **10th:** Vyapara, Aspada, Mana, **Karma**, Jaya, Kirti, Kratu, Jivana, Vyoma, Acara, Guna, Pravrtti, Gamana, Ajna, Meshurana.
- **11th:** Labha, Aya, Agamana, Apti, Siddhi, Vibhava, Prapti, Shlaghyata, eldest sibling, left ear.
- **12th:** Duhkha, Anghri, Vama-nayana (left eye), Kshaya, Sucaka, Antya.

**BPHS ch. 11, "Judgement of Houses," vv. 2-13** is terser and — **important honest note — does not list vak for the 2nd house** [P, Santhanam trans.]:
- 1st: physique, appearance, intellect (*buddhi*), complexion, vigour, weakness, happiness, grief, innate nature.
- **2nd: wealth, grains/food, family (*kutumba*), death, enemies, metals, precious stones.** (No "speech.")
- **3rd: valour, servants, siblings, initiatory instruction (*upadesha*), journey, parents' death.**
- 4th: conveyances, relatives, mother, happiness, treasure, lands, houses.
- **5th: amulets (*yantra*), sacred spells (*mantra*), learning (*vidya*), knowledge (*jnana*), sons, authority, fall of position.** — mantra and vidya yes; ***purva-punya* is not in this verse**; it comes from Phaladipika's "purva-bhagya" (9th) and later tradition.
- 6th: maternal uncle, doubts about death, enemies, ulcers, step-mother.
- 7th: wife, travel, trade, loss of sight, death.
- 8th: longevity, battle, enemies, forts, wealth of the dead, past and future events.
- **9th: fortunes, wife's brother, religion (*dharma*), brother's wife, visits to shrines.**
- 10th: royalty, place, profession, honour, father, foreign residence, debts.
- 11th: all articles, son's wife, income, prosperity, quadrupeds.
- 12th: expenses, history of enemies, one's own death.

BPHS 8.39-43 does say the 2nd from Lagna and from the Moon is examined for "sight, speech, learning, wealth" — but "speech" there is in Santhanam's **expository note**, and the underlying verse is about doubling the reference point, not defining the 2nd house.

**Bottom line on 2nd = vak:** classically attested in **Phaladipika 1.10** and standard in later handbooks; **not in the BPHS bhava chapter. Do not cite BPHS for it.**

### 4.5 Is there any staged mapping of cognition or communication in Jyotisha?

**No.** **No classical Jyotisha text was found that maps a process of cognition or speech-production, stage by stage, onto grahas or bhavas.** What the classical texts give is a **static significator table** (BJ 2.1, BPHS 3.12-13, BPHS 32, Phaladipika 1.10-16 and 15.17). The house sequence 1→12 is enumerated in order but is **never presented as a temporal or derivational pipeline of thought-into-speech.**

**On the four levels of vak specifically:** the scheme is from the grammarian-philosophical tradition, not from jyotisha. **No classical jyotisha text mapping para/pashyanti/madhyama/vaikhari onto grahas or bhavas was found. No systematic modern astrology treatment doing so was found either** — searches returned either pure spiritual-philosophy pages on the four levels or pure astrology pages on Mercury and the 2nd house, with no page joining the two. **If anyone presents such a correspondence, treat it as a modern synthesis by whoever is presenting it, not as classical doctrine, unless they produce a verse.**

### 4.6 Vyakarana and Jyotisha as Vedangas — the "eyes and mouth" verse, verified

The six Vedangas: **shiksha** (phonetics), **kalpa** (ritual), **vyakarana** (grammar), **nirukta** (etymology), **chandas** (metre), **jyotisha** (astronomy/astrology) [W: Vedic Heritage Portal; S: "Importance of the Vedangas: An Analysis"].

**Paniniya Shiksha 41-42**, verified against the Sanskrit [W: advocatetanmoy.com; Hindi Wikipedia वेदांग]:

> **41.** *chandah padau tu vedasya hastau kalpo 'tha pathyate | jyotisham ayanam cakshur niruktam shrotram ucyate ||*
> **42.** *shiksha ghranam tu vedasya mukham vyakaranam smrtam | tasmat sangam adhityaiva brahmaloke mahiyate ||*

"Chandas is the Veda's two feet; Kalpa its two hands; **jyotisha, the science of the movements of the luminaries, is the eye**; Nirukta is the ear. Shiksha is the nose, and **vyakarana is held to be the mouth**. Therefore, having studied the Veda together with its angas, one is exalted in Brahmaloka."

**Three caveats, stated honestly:**
1. The commonly-quoted phrasing "*jyotisham cakshuh, vyakaranam mukham*" is a **paraphrase**; the verse reads *jyotisham ayanam cakshuh* and *mukham vyakaranam smrtam*.
2. **Verse numbering 41-42 belongs to the vulgate/Panjika recension.** When the researcher checked **Manomohan Ghosh's critical edition** of the Paniniya Shiksha, **the couplet was not found in the edited text body** — so it is likely a widely-transmitted addendum rather than securely original. The same couplet circulates in Puranic and Vedanga-prashamsa literature.
3. **The verse says nothing about a functional division of labour between grammar and astrology.** It is a *mahatmya* (praise) trope. It supplies imagery — jyotisha as the eye that sees time, vyakarana as the mouth that speaks — **not a theory.**

**On roles.** Jyotisha's Vedanga function is **calendrical** — fixing the correct time for ritual. The *Vedanga Jyotisha* of Lagadha is purely astronomical/calendrical, **with no horoscopy at all**; horoscopic astrology enters India with Hellenistic transmission (cf. the *Yavanajataka*, and Varahamihira 6th c. CE) [W: Wikipedia "Vedanga Jyotisha," "Jyotihshastra"].

**This matters for the karaka question.** The Vedanga that shares a canon-slot with vyakarana is *calendrical* jyotisha, whereas the texts that use *karaka* as "significator" (BPHS, Jaimini, Brihat Jataka) belong to the much later horoscopic layer. **That further weakens any "shared framework" story.**

---

## 5. What modern linguistics and cognitive science took from Panini

Included only insofar as it helps build the anatomy.

### 5.1 Generative grammar — what Chomsky actually said

**The one canonical statement**, *Aspects of the Theory of Syntax* (MIT Press, 1965), **Preface, p. v** [P]:

> "Nevertheless, it seems that even Panini's grammar can be interpreted as a fragment of such a 'generative grammar,' in essentially the contemporary sense of this term."

Note the hedging: *even*, *can be interpreted as*, *a fragment*. This is a nod to precedent in a passage whose main subject is von Humboldt. In a 2001 Kolkata address Chomsky said, more strongly, "the first generative grammar in the modern sense was Panini's grammar." Chomsky & Halle's *The Sound Pattern of English* (1968) ends with an allusion to Panini's final sutra (*a a*, A 8.4.68) — a wink, not a debt. A substantive Panini passage in *Current Issues in Linguistic Theory* (1964) **could not be verified** [?].

A careful survey of the evidence: Nick Nicholas, "What were Noam Chomsky's views on Panini's Ashtadhyayi?" [W: hellenisteukontos.opoudjis.net] — conclusion: Chomsky's engagement is "complimentary, but not deep"; he cites Panini as precedent without deriving anything from him.

**Popular inflation to flag:** claims that Chomsky "based generative grammar on Panini," or that Panini "was the first programmer," are **popular/nationalist web content, not scholarship**. Chomsky developed transformational grammar out of Harris, Bloomfield and Post.

**Where real Paninian influence did enter:** through Sanskritist-linguists at MIT, above all **Paul Kiparsky** (PhD MIT 1965 under Halle), and through **Kiparsky & Staal**, "Syntactic and Semantic Relations in Panini," *Foundations of Language* 5 (1969): 83-117 [S], who read the Ashtadhyayi as a multi-level derivational architecture: **semantics (with karaka and tense assignment) → morphosyntax → abstract morphology → phonological output.**

**A caution from the same paper:** Kiparsky & Staal explicitly note that Panini's operations are **derivations, not rewritings** in the Post/Chomsky sense; and the Paninian formalism is arguably *more* powerful than context-free rewriting. "Panini's rules are ordered rewrite rules" is a first approximation that specialists qualify.

### 5.2 The Elsewhere Condition — the one substantive transfer

**Paul Kiparsky, "'Elsewhere' in Phonology," in Anderson & Kiparsky (eds.), *A Festschrift for Morris Halle* (Holt, Rinehart & Winston, 1973), pp. 93-106** [S]. It argues that *SPE*'s treatment of disjunctive ordering is inadequate and replaces it with the **Elsewhere Condition: a specific rule blocks a general rule whose structural description properly includes it.**

**The Paninian ancestry is genuine and acknowledged**: the *utsarga*/*apavada* relation, plus *anavakashatva* ("having no other scope" — a rule that would otherwise never apply takes precedence), and A 1.4.2. Kiparsky's own assessment in his *Oxford History of Phonology* chapter: the core intuition "was already there in Panini... but Panini's implementation of it as a relation between special and general rules goes much further," unified via the siddha/asiddha relation. Related: Stephen R. Anderson's 1969 MIT dissertation independently identified disjunctive-blocking cases; Prince, "Elsewhere & Otherwise" (ROA-217) reviews the formulation critically. The label **"Panini's Principle"** for specific-over-general blocking is standard in the literature.

**Verdict: the Elsewhere Condition is the one place where a Paninian principle demonstrably entered generative theory as substance rather than decoration — and the transmission vector is Kiparsky, a trained Sanskritist, not Chomsky.**

### 5.3 Backus-Naur Form — priority, not influence

**Peter Zilahy Ingerman, "'Panini-Backus Form' suggested," *Communications of the ACM* 10(3), March 1967, p. 137** [P] — a short **letter to the editor**, not a paper. Its actual content: Backus "was not the first to use the form with which his name has become associated, although he did discover it **independently**"; Panini "invented a notation which is equivalent in its power to that of Backus, and has many similar properties," including analogues of `|` alternation and of the meta-brackets `<...>`; therefore "Panini-Backus Form" would be a better name, "since there is clear evidence that Panini was the earlier **independent** inventor."

**What Ingerman did NOT claim: that Backus or Naur knew of, read, or were influenced by Panini. He explicitly says "independent." The influence claim is a later accretion.**

**State of the historical question:** Naur named it "Backus normal form" in the ALGOL 60 report (1963); Knuth's 1964 CACM letter proposed "Backus-Naur form." **Naur is on record saying "I do not know where BNF came from in the first place."** Backus's stated route is Emil Post's production systems. **No documentary evidence links either man to Panini** [W: Wikipedia "Backus-Naur form"]. The sites pushing "Panini-Backus Form" hardest are **advocacy sources** (Infinity Foundation and affiliates) and should be flagged as such.

**Technical caveat worth carrying: Paninian rule formalism is strictly more powerful than the context-free grammars BNF describes, so "Panini invented BNF" is wrong in both directions.**

**Verdict: priority of a similar notation — well supported. Influence on Backus/Naur — unsupported; treat as false unless someone produces evidence.**

Related formal work: **Gerald Penn & Paul Kiparsky, "On Panini and the Generative Capacity of Contextualized Replacement Systems," COLING 2012 Posters, pp. 943-950** [S] — reported to show the Ashtadhyayi's formalism has expressive power well beyond regular and context-free languages [?, the paper was not read; secondary summaries in the enthusiast literature inflate this into "Panini invented Turing-complete computation," which a careful reading does not support. **Read the PDF before repeating a complexity claim.**]. A critical treatment, "Revisiting Panini's Generative Power" (Oxford ORA) [?, author unidentified], signals the question is live.

### 5.4 Paninian frameworks in computational linguistics — the live line of descent

**The Paninian Grammar Framework.** Akshar Bharati, Vineet Chaitanya & Rajeev Sangal, ***Natural Language Processing: A Paninian Perspective***, Prentice-Hall of India, 1995 [S]. ("Akshar Bharati" is a collective pen-name of the IIIT-Hyderabad / IIT-Kanpur group.) Companion: Bharati, Chaitanya & Sangal, "Paninian framework and its application to Anusaraka," *Sadhana* 19(1), 1994 [S].

Core idea: **karakas are syntactico-semantic relations mediating between surface form (vibhakti/postposition + verb form) and meaning** — a **dependency** (not phrase-structure) formalism, well suited to free-word-order languages. This is a *reconstructed application* of Paninian ideas to modern Indian languages, not Panini's own grammar.

**Karaka-labelled dependency treebanks.** The **AnnCorra** guidelines: Bharati, Sharma, Husain, Bai, Begum & Sangal, *AnnCorra: TreeBanks for Indian Languages — Guidelines for Annotating Hindi TreeBank v2.0*, LTRC IIIT-Hyderabad, 2009 [S]. Tagset: roughly **19 fine-grained karaka tags** (k1 karta, k2 karma, k3 karana, k4 sampradana, k5 apadana, k7 adhikarana, with subtypes) plus ~**25 non-karaka relations** (r6 genitive, rh hetu, rt tadarthya). Downstream: the Hindi/Urdu Treebank, Hindi CCGbank, and **"Conversion from Paninian Karakas to Universal Dependencies for Hindi Dependency Treebank"** (Tandon, Chaudhry, Bhatt, Sharma, Xia, LAW 2016) [S] — the honest place to see where karaka labels and UD labels do and do not line up.

**Sanskrit proper.** **Amba Kulkarni** (University of Hyderabad) builds Paninian language processors: karaka analyser, sandhi splitter, verb analyser, POS tagger, and the **Samsadhani** platform [S]. Her distinctive angle is **linking traditional *shabdabodha* theory and karaka theory to AI knowledge representation.** Recent: "Some Strategies to Capture Karaka-Yogyata with Special Reference to apadana" (arXiv 2201.01700); "Neural Approaches for Data Driven Dependency Parsing in Sanskrit" (arXiv 2004.08076).

**Sanskrit Heritage Platform.** **Gérard Huet** (INRIA), from c. 2000: a Sanskrit-French lexicon doubling as a computational lexical database, finite-state morphology, a segmenter/sandhi analyser, and a dependency/karaka interface built jointly with Kulkarni [S: Huet & Kulkarni, "A Distributed Platform for Sanskrit Processing," COLING 2012]. Huet founded the International Symposium on Sanskrit Computational Linguistics (3rd at Hyderabad, Jan. 2009; proceedings = LNCS 5402, the volume containing Kiparsky's "On the Architecture").

**Verdict: this is the strand where Panini is genuinely *operative* rather than ceremonial — karaka labels are the actual annotation vocabulary of Indian-language treebanks in production use.**

### 5.5 Levelt's model of speech production

**Willem J. M. Levelt, *Speaking: From Intention to Articulation*, MIT Press, 1989** [S]. Three components, feed-forward and incremental:

1. **CONCEPTUALIZER** — message generation, two sub-processes:
   - **macroplanning**: selecting and ordering the information that will serve the communicative intention (elaborating the intention into a sequence of speech-act sub-goals);
   - **microplanning**: giving the message propositional shape, perspective, topic/focus assignment, and the conceptual features the target language obligatorily encodes.
   - Output: the **PREVERBAL MESSAGE**.
2. **FORMULATOR** — conceptual into linguistic structure:
   - **grammatical encoding**: **lemma** retrieval from the mental lexicon (a lemma = meaning + syntax, without form), driving **functional processing** (lexical selection + function assignment) and **positional processing** (constituent assembly + inflection). Output: **SURFACE STRUCTURE**.
   - **phonological encoding**: retrieval of the **lexeme** / word form, syllabification, prosody. Output: the **PHONETIC PLAN**, i.e. internal speech.
3. **ARTICULATOR** — executes the phonetic plan → **OVERT SPEECH**.

Plus the **SPEECH-COMPREHENSION SYSTEM** (with **AUDITION**) feeding the **self-monitoring loop**: the speaker parses both his *internal* speech (the phonetic plan, **before articulation**) and his *overt* speech, and can interrupt and repair. Knowledge stores: the **MENTAL LEXICON** and discourse model / situation knowledge / encyclopedia.

Levelt's later restatement, "Producing spoken language: a blueprint of the speaker" (1999) [S], renames the stages in finer grain: **conceptual preparation → lexical concept → lexical selection (lemma) → morphological encoding → phonological encoding / syllabification → phonetic encoding (mental syllabary) → articulatory score → articulation → self-perception.**

**WEAVER++.** **Levelt, Roelofs & Meyer, "A theory of lexical access in speech production," *Behavioral and Brain Sciences* 22(1), 1999, pp. 1-38** [S]. Word preparation is "staged and feed-forward": conceptual preparation → lexical selection → morphological and phonological encoding → phonetic encoding → articulation, with output control by **monitoring of self-produced internal and overt speech**. WEAVER++ ("Word-form Encoding by Activation and VERification") is a spreading-activation network with a *verification* mechanism keeping it functionally discrete.

**Contrast models.**
- **Garrett (1975, 1980)** [S], built from speech-error data: **message level → functional level** (lexical selection of content words + grammatical function assignment; order not yet fixed) **→ positional level** (constituent frames with slots; function words and inflections inserted; order fixed) **→ phonetic level → articulation**. Word-exchange errors diagnose the functional level, sound-exchange errors the positional level. The functional/positional split is the direct ancestor of Levelt's grammatical-encoding sub-stages.
- **Dell (1986)**, "A spreading-activation theory of retrieval in sentence production," *Psychological Review* 93: 283-321 [S] — an **interactive** connectionist alternative: semantic, lexical and phonological node layers with **bidirectional** spreading activation and no strict stage separation, so phonological information can feed back into lexical selection. **The Levelt-discrete vs Dell-interactive dispute is the central axis of the field.**

**Does anyone explicitly compare Levelt's stages with Panini's or Bhartrihari's? NO SUCH PUBLISHED COMPARISON WAS FOUND.**

What exists nearby, and only nearby: work applying a psycholinguistic lens to the Vakyapadiya in general terms — e.g. "Communication as Cognitive Unfolding: Bhartrihari's Theory of Vak in Vakyapadiya" [W: academia.edu], which frames pashyanti/madhyama/vaikhari as a movement "from thought to articulation," language that *invites* the comparison but does not make it against Levelt. Matilal's *The Word and the World* and M. S. Murti's *Bhartrihari, the Grammarian* are philosophical, not model comparisons. Levelt's own *A History of Psycholinguistics: The Pre-Chomskyan Era* (OUP 2013) has no Indian-tradition chapter.

**[F]** The structural rhyme is real: pashyanti ≈ preverbal message, madhyama ≈ internal phonetic plan, vaikhari ≈ overt speech; and Levelt's self-monitoring of *inner* speech before articulation has a suggestive analogue in the classical claim that madhyama is apprehended before utterance. **This is my observation, not a citable finding, and the literature has not made it.** It is offered as a bridge for building the anatomy, not as evidence for either tradition.

---

## 6. Where the Ashtadhyayi can be obtained machine-readable

Candidates only. HTTP reachability was checked by the researcher (September 2026); contents were not audited.

| Resource | URL | What it gives |
|---|---|---|
| **GRETIL** (Göttingen) | `https://gretil.sub.uni-goettingen.de/gretil/corpustei/sa_pANini-aSTAdhyAyI.xml` | TEI-XML Ashtadhyayi. Best-curated scholarly structured text. Index at `gretil.sub.uni-goettingen.de/gretilbk.htm` |
| **sanskritdocuments.org** | `https://sanskritdocuments.org/doc_z_misc_major_works/aShTAdhyAyI.html` | Devanagari + transliteration, PDF/ITX. Site also carries Kashika, Mahabhashya, Dhatupatha, Siddhantakaumudi |
| **ashtadhyayi.com** | `https://ashtadhyayi.com/` | Best interactive resource: sutra text, padaccheda, **anuvritti**, **adhikara**, multiple vrttis, a prakriya (derivation) generator, offline mode |
| **github.com/ashtadhyayi-com/data** | `https://github.com/ashtadhyayi-com/data` | The structured data behind the above. Devanagari markdown with YAML frontmatter for vrttis; plain text for padaccheda / anuvritti / adhikara / full_sutra. **The most directly machine-consumable structured dataset found.** |
| **github.com/sanskrit/ashtadhyayi** | `https://github.com/sanskrit/ashtadhyayi` | Commentaries; UI at `ashtadhyayi.github.io/suutra/` |
| **INRIA Sanskrit Heritage** | `https://sanskrit.inria.fr/` | Not the text, but the reference computational-Sanskrit toolchain: morphological generator/analyzer, sandhi engine, segmenter, downloadable lexicon |
| **Digital Corpus of Sanskrit** | `http://www.sanskrit-linguistics.org/dcs/` | ~650k text lines, sandhi-split, full morphological analysis, >4.5M tokens, ~400 texts. A corpus, not the grammar |
| **ambuda-org/vidyut** | `https://github.com/ambuda-org/vidyut` | Rust toolkit including `vidyut-prakriya`, a modern implementation of Paninian derivation. **The closest thing to a runnable Ashtadhyayi.** |
| **drdhaval2785/SanskritVerb** | `https://github.com/drdhaval2785/SanskritVerb` | Paninian verb-form derivation engine with sutra-by-sutra derivation traces |
| **sanskritdictionary.com per-sutra** | `https://sanskritdictionary.com/panini/1-4-2` | Per-sutra pages with Kashika / Vasu English translation. Returns 403 to scripted curl; browser-reachable |

Not individually verified: Ambuda (`ambuda.org`) for commentaries; the Sanskrit Library (`sanskritlibrary.org`) for Scharf's encoded texts and his Paninian implementation; SARIT (`sarit.indology.info`) for TEI editions — note SARIT returned HTTP 502 during this research.

**Recommendation as relayed:** **GRETIL TEI-XML** for a clean canonical sutra text, plus **github.com/ashtadhyayi-com/data** for the sutra text *and* the machine-relevant metadata (anuvritti, adhikara, padaccheda) that cannot be recovered from the bare sutras. **vidyut-prakriya** for an executable model rather than a text.

---

## 7. Contested points, gathered

Listed so that no stage of the synthesis rests silently on a disputed claim.

1. **The sutra typology** — five, six, seven or more types; the six-fold verse is post-Paninian pedagogy, not primary.
2. **Rajpopat on 1.4.2.** Rishi Rajpopat's Cambridge thesis (Dec 2022; Harvard UP 2025 as *Panini's Perfect Rule*) rejects the traditional reading of *para* as "later in the text" and reads it as **"right-hand side"** — of two rules applicable to the left and right portions of a word, choose the right one; recast as Same Operand Interaction (specificity wins) vs Different Operand Interaction (right-side principle). **Reception is divided.** Cambridge's press release quotes experts calling it revolutionary; **Peter M. Scharf** has criticized it as not sufficiently engaging the commentarial discussion and "largely ineffective" — **but that critique was located only in partisan Indian opinion outlets, with no peer-reviewed rebuttal found. Do not cite Scharf's critique as published scholarship.** Language Log covered it; ANU's neutral framing: "it will take a while for the scholarly dust to settle." **Report as contested.**
3. **Karaka: semantic, syntactic, or neither** — Kiparsky (mediating role types), Cardona (semantic basis), Deshpande (direct vs indirect), and a dissenting "neither" position. Still debated.
4. **Whether "para vac" is Bhartrihari's** — it is not; it is a Shaiva fourth level, harmonized onto him by later readers.
5. **Whether the Vakyapadiya-Vritti is by Bhartrihari** — Iyer, Aklujkar, Houben yes; Biardeau, Bronkhorst no. Much of the *staged* speech-level description comes from the Vritti.
6. **Sphota holism vs part-ism** — grammarians (akhanda) against Kumarila and Jayanta Bhatta (khanda-paksha).
7. **Nirvikalpaka/savikalpaka in Nyaya** — not in the Sutra, Bhashya, or Varttika; read in by Vacaspati; Mondal (1982) against; Phillips vs Chakrabarti today.
8. **Where sentence-composition happens** — abhihitanvaya (second step), anvitabhidhana (inside denotation), sphota (no parts).
9. **Whether tatparya is a condition of verbal understanding** — Nyaya yes, Bhatta Mimamsa no, Prabhakara structurally unnecessary, Vacaspati reinterprets it as usage.
10. **The mechanism of rasa** — Lollata (produced), Shankuka (inferred), Nayaka (relished via universalisation), Abhinavagupta (manifested from the receiver's own traces). Pollock warns the sharpness is partly Abhinavagupta's framing.
11. **Whether dhvani is a distinct power** — Anandavardhana and Abhinavagupta yes; Mukula reduces to lakshana; Mahima Bhatta reduces to inference; Nayaka denies rasa is a meaning.
12. **Citta-vithi's canonicity** — commentarial elaboration, not canonical; bhavanga absent from the Nikayas; the 17-moment tabulation is the Sangaha's.
13. **Whether testimony is sui generis** — Nyaya yes; Vaisheshika (per Shridhara) and Buddhist logicians reduce it to inference.
14. **Jyotisha karaka ↔ Panini karaka** — **unattested in any direction.**
15. **Chomsky's debt to Panini** — one hedged sentence; the real transfer is Kiparsky's Elsewhere Condition.
16. **Backus/Naur's debt to Panini** — **none evidenced**; Ingerman claimed independence and priority only.
17. **Levelt vs the Indian models** — **no published comparison exists.**
18. **Levelt-discrete vs Dell-interactive** — the live dispute in speech production about whether stages are separable at all. **[F]** This bears directly on whether an anatomy of stages is the right shape of thing.

---

## 8. Synthesis: a first rough anatomy

**This section is the flow's construction.** It arranges only what sections 1-7 support. Each stage names its source. Where the arrangement itself is mine, it is marked **[F]**. Where the sources disagree about a stage, the disagreement is carried into the stage rather than resolved out of it.

**A caveat carried from item 18 above:** Dell's interactive model, and the Prabhakara position on sentence-meaning, both deny that the stages are cleanly separable. A staged anatomy is a commitment, not a neutral description. The sources support the stages; they do not agree that the boundaries are real.

### 8.1 The expression arc — intention to utterance

| # | Stage | What happens | Source |
|---|---|---|---|
| E0 | **Ground / disposition** | The standing state from which an impulse arises. Named differently and not identically: *shabda-brahman* (Bhartrihari VP 1.1); *para vac* (Abhinavagupta, not Bhartrihari); *bhavanga*, the life-continuum from which every process departs and to which it returns (Abhidhammattha Sangaha 4); the store of *samskara/vasana* (YS 4.9-4.11). | [P] VP 1.1; [P] AS ch.4; [P] YS 4.9-4.11 |
| E1 | **Vivaksha — the desire to express** | The intention to say. **Explicitly outside the grammar**: Panini's system takes it as input and does not derive it. It governs which participant becomes which karaka. | [P] Mahabhashya, *vivakshatah karakani bhavanti* (paribhasha, attribution uncertain); [S] Cardona |
| E2 | **Pashyanti — the whole meaning, sequenceless** | The intended meaning grasped as one, *akrama*, without temporal parts. Identified in the Vritti with *pratibha*. | [P] VP 1.159 (Rau) / ~1.142 (Iyer); [P] VP I.48 on *akrama* |
| E3 | **Event structure — karaka assignment** | The situation is cast as an action with roles: *kartr* (independent one), *karma* (most desired), *karana* (most effective means), *sampradana*, *apadana*, *adhikarana*. Superlatives force uniqueness. Assignment follows the speaker's construal, not the facts. | [P] A 1.4.23-1.4.55 |
| E4 | **Madhyama — inner sequencing and selection** | Sequence appears; words and constructions are selected in *buddhi*; the knower/known distinction appears inwardly; no audible sound. | [P/W] VP 1.159 with Vritti; [W] IEP |
| E5 | **Encoding — vibhakti, affix, pada** | Case endings assigned **only where not already expressed** (*anabhihite* gate); root/stem plus affix; the result is a *pada* when it ends in *sup* or *tin*, which is what turns on external-boundary operations. | [P] A 2.3.1; A 3.1.91; A 1.4.14 |
| E6 | **Phonological realization — prakrta then vaikrta dhvani** | The type-level phonological form specified by the language, then the token-level physical realization varying with speaker, tempo, accent. Internal sandhi, then the single-pass opaque *tripadi*. | [S] Staal on prakrta/vaikrta; [P] A 8.2.1 *purvatrasiddham* |
| E7 | **Vaikhari — overt speech** | Articulated, gross, audible, sequenced, produced by the vocal organs. | [P/W] VP 1.159 |

**Interfaces on the expression arc:**

- **E0→E1**: a disposition becomes a directed intention. No source in this material describes the mechanism. **[F] This is the least-specified joint in the whole anatomy, and every tradition surveyed leaves it dark.**
- **E1→E2**: not a transformation but a **condition**. The grammar takes vivaksha as given input and derives nothing behind it. **[P] the boundary is explicit in Panini's silence: there is no sutra for vivaksha.**
- **E2→E3**: the interface where **the sequenceless becomes structured but not yet ordered**. Karakas are roles, not positions; case comes later. [P] the 1.4.23 block precedes the 2.3 block.
- **E3→E4**: roles become **a plan with sequence**. [F] Panini has no stage for this; Bhartrihari's madhyama does. The two traditions cover different halves of the same joint and neither covers both.
- **E4→E5**: the ***anabhihite* gate** — the only *conditional* interface in the pipeline. A relation is marked morphologically **only if not already marked elsewhere**. [P] A 2.3.1. **[F] This is a redundancy check standing between plan and form, and it is the sharpest single interface Panini names.**
- **E5→E6**: the ***pada* boundary** [P] A 1.4.14, and then the **asiddha wall** [P] A 8.2.1 — below which operations are invisible to everything above. **[F] A one-way membrane: phonetic detail cannot inform the choices already made.**
- **E6→E7**: type to token. Variation here does not alter the meaning-unit [W/S: the sphota invariance principle].

### 8.2 The impression arc — utterance to understanding

| # | Stage | What happens | Source |
|---|---|---|---|
| I1 | **Sound at the sense-gate** | Dhvani/nada strikes the ear. The external instrument operates **only in the present**. In Abhidhamma terms the life-continuum vibrates and is arrested, then five-door adverting occurs. | [P] SK 33; [P] AS ch.4 (bhavanga-calana, bhavangupaccheda, pancadvaravajjana) |
| I2 | **Bare sense-cognition** | Contact-born cognition, prior to naming. Nyaya's *sannikarsha*-born *pratyaksha*; Abhidhamma's *panca-vinnana*; the disputed *nirvikalpaka* stage. | [P] NS 1.1.4; [P] AS ch.4. **Contested**: nirvikalpaka is not in the Sutra/Bhashya/Varttika; read in by Vacaspati; Mondal against; Phillips vs Chakrabarti |
| I3 | **Reception and investigation** | The content is received and examined. *sampaticchana* then *santirana*; in Samkhya, *manas* particularises (*samkalpa*). | [P] AS ch.4; [P] SK 27, SK 30 with Vacaspati's tiger illustration |
| I4 | **Appropriation** | "This concerns me." *ahamkara* (*abhimana*); *asmita* (seer and instrument appearing as one self); Yogacara's *klishta-manas*. **[F] Structurally the same move in three schools.** | [P] SK 24; [P] YS 2.6; [S] Yogacara |
| I5 | **Determination** | The content is settled. *buddhi* as *adhyavasaya*; *votthapana*; in inference, *linga-paramarsha*, the *karana* of *anumiti*. | [P] SK 23; [P] AS ch.4; [P/W] Tarkasamgraha |
| I6 | **Sequence to unity** | The strung-out signal yields a partless meaning-unit. Samskaras accumulate over successive phoneme-cognitions; the final element, aided by the traces, reveals the whole. **Vyasa independently: buddhi grasps the word as a unity only at the last phoneme.** | [S] Coward's reconstruction; [P] Vyasa on YS 3.17; [P] VP I.48-49. **Contested**: Kumarila and Jayanta hold the unit is composed |
| I7 | **Composition of sentence-meaning** | Word-meanings become sentence-meaning under *akanksha*, *yogyata*, *sannidhi* (and *tatparya*, disputed). | [P] Nyayasiddhantamuktavali on Bhashapariccheda 84. **Three-way contested**: second step (abhihitanvaya) / inside denotation (anvitabhidhana) / no parts at all (sphota) |
| I8 | **Pratibha — the flash** | The meaning is had, whole and at once. On Aklujkar's reading this is **practical, action-oriented knowledge** — *itikartavyata*, knowing-what-is-to-be-done — not a representation. | [P] VP 2.143-145; [S] Aklujkar 1970 (quoted at second hand) |

**Interfaces on the impression arc:**

- **I1→I2**: a **threshold**. Abhidhamma alone states it explicitly: a too-weak object produces only bhavanga vibration and **no cognitive process arises at all** (*mogha-vara*). [P] AS ch.4. **[F] The only place in this material where "nothing happened" is a modelled outcome rather than an omission.**
- **I2→I3**: **the disputed one.** Whether there is a pre-conceptual stage handing content to a conceptual one is exactly what Nyaya has argued about for a millennium, and what Buddhist epistemology answers oppositely (for Dignaga only the non-conceptual stage is perception).
- **I3→I4**: coordination hands to appropriation. **[F] This is the interface the psyche's own concern points at** (see 8.4): the point where content acquires a stake in the self, before determination.
- **I4→I5**: appropriation hands to determination. In Samkhya, SK 30 says these are **both simultaneous and successive** — phenomenally instantaneous, really staged. [P] SK 30. **[F] The tradition anticipates the objection that the stages are not felt as separate, and answers it.**
- **I5→I6**: the sequenced becomes the unified. Both the grammarians and Vyasa locate the unification **at the terminal element of the sequence**. [F] two traditions converging, not borrowing.
- **I6→I7**: contested out of existence by two of the three positions — Prabhakara has no separate composition step, Bhartrihari has no parts to compose.
- **I7→I8**: understanding terminates. **[F] If Aklujkar is right, the terminus is already a disposition to act, which means the impression arc does not end before reaction begins — there is no clean seam here.**

### 8.3 The reaction arc

| # | Stage | What happens | Source |
|---|---|---|---|
| R1 | **Impulsion** | The kammically decisive moment. Seven *javana* moments; this is where the act is weighted. | [P] AS ch.4 |
| R2 | **Valence as residue** | *raga* follows pleasure, *dvesha* follows pain — both as *anushayin*, residues. Rooted in *avidya* via *asmita*. | [P] YS 2.3-2.9 |
| R3 | **Deposit** | *tadarammana* registration, then return to bhavanga; *karmashaya*; *samskara*. Memory and samskara are of one form (YS 4.9), which is what makes the loop close. | [P] AS ch.4; [P] YS 2.12, 4.9-4.11 |
| R4 | **Return to ground** | The deposit becomes part of E0 for the next cycle. | [P] YS 4.9-4.11; [P] AS ch.4 |

**Two-level intervention** [P] YS 2.10-2.11: active vrittis yield to *dhyana*; latent kleshas require *pratiprasava*, involution to the source. **[F] An anatomy that only handles the active layer leaves the generator running.**

**The impression side of reaction — where the impression comes from.** The rasa literature is the tradition's most explicit argument about this, and it is a **genuine four-way disagreement** that an anatomy must choose among:

| Position | Mechanism | Where the impression originates |
|---|---|---|
| **Lollata**, *utpatti-vada* | rasa is produced and intensified in the character | **the sender** |
| **Shankuka**, *anumiti-vada* | the spectator infers the emotion from signs | **the receiver's inference** |
| **Bhatta Nayaka**, *bhukti-vada* | *bhavakatva* universalises (*sadharanikarana*), *bhojakatva* relishes | **a power of the medium** |
| **Abhinavagupta**, *abhivyakti-vada* | rasa is manifested from the spectator's **own latent samskaras**, once obstacles are removed | **the receiver's stored dispositions** |

[P/S] Abhinavabharati on NS 6, all four; [S] Pollock, Gnoli. Pollock warns the sharpness is partly Abhinavagupta's own framing.

**[F]** These four are not variants of one model. They put the causal locus in four different places, and they imply four different anatomies of the reaction stage. **The choice cannot be made from the sources; it has to be made deliberately.**

### 8.4 What the anatomy actually gives

Reading across the three arcs, the sources support these as **structural features**, each with a named origin:

1. **Intention is input, not output.** Panini's grammar begins after vivaksha and derives nothing behind it. [P] the absence of a vivaksha sutra.
2. **Roles are assigned before positions.** Karaka precedes vibhakti; the mapping is not one-to-one (the genitive is a case with no karaka). [P] A 1.4.23 block before A 2.3 block.
3. **Marking is conditional on non-redundancy.** [P] A 2.3.1 *anabhihite*.
4. **Disambiguation is by superlative.** When several participants qualify, "most" decides. [P] A 1.4.42, 1.4.49.
5. **Conflicts resolve by a declared policy, not ad hoc.** Specificity, then strength criteria, then textual order. [P] A 1.4.2 plus the *balabala* paribhasha. **Contested** (Rajpopat).
6. **Some stages are invisible to others, by declaration.** [P] A 8.2.1, 6.4.22, 6.1.86; [S] Kulkarni's "privacy of data spaces."
7. **Compression sits between rules and material.** [P] the pratyahara mechanism; [S] Petersen's optimality proof.
8. **Context carries forward silently and must be reconstructed.** [P/W] anuvritti.
9. **Type and token are distinct strata of the signal.** [S] prakrta vs vaikrta dhvani.
10. **The sequenced and the unified are different orders of thing, and the interface between them is superimposition, not composition.** [P] VP I.48 (*iva*).
11. **Unification happens at the terminal element.** [S] Coward; [P] Vyasa on YS 3.17.
12. **The private and public forms of the same reasoning differ in stage count.** Three (*svarthanumana*) vs five (*pararthanumana*). [P/S] Dignaga, Annambhatta.
13. **Word, object, and idea are habitually fused, and separating them is a discipline.** [P] YS 3.17 *itaretaradhyasat samkarah*; [P] YS 1.42 *samkirna*.
14. **Appropriation is a distinct stage between coordination and determination.** [P] SK 24, SK 30; [P] YS 2.6.
15. **A stimulus below threshold produces no process.** [P] AS ch.4 *mogha-vara*.
16. **The loop closes through a deposit that is of one form with memory.** [P] YS 4.9.
17. **There are two levels of intervention, active and latent.** [P] YS 2.10-2.11.
18. **The terminus of understanding may already be a disposition to act.** [S] Aklujkar on *pratibha* as *itikartavyata* — second-hand, verify.

**[F] Bearing on the flow's stated purpose.** The psyche's recorded interest (`flows/5851f4/vision/thinkingPhases.md`) is in breaking the thinking process into phases assigned to different flows, and specifically in a layer that removes anger before it reaches the layer that produces the artifact. Three findings above bear directly and are worth naming as such:

- **Item 14** locates *appropriation* — the "this concerns me" move — as a distinct stage sitting **between** reception and determination. That is precisely the seam at which a stripping layer would have to sit. [P] SK 30 puts it there and says it is really successive though phenomenally simultaneous.
- **Item 17** says a layer that only handles the active reaction leaves the generator intact. [P] YS 2.10-2.11.
- **Item 12** says the same reasoning takes a different number of stages when it is for oneself and when it is for another. [P/S] svartha/parartha. **[F]** That is an argument for the phases being genuinely different pipelines rather than one pipeline observed twice.

None of these is a recommendation. They are the places in the material where the psyche's stated concern has an attested structural counterpart.

### 8.5 What the anatomy does not have

Stated so the gaps are not mistaken for stages:

- **No source describes E0→E1** — how a standing disposition becomes a directed intention to say something.
- **No source in this material joins the expression arc and the impression arc into one loop** except Levelt's self-monitoring, which is modern and which no one has compared to this tradition [negative finding, section 5.5].
- **No classical Jyotisha text stages cognition or communication.** Its significators are static tables [negative finding, section 4.5]. Nothing in the astrological material contributed a stage to the synthesis above; it contributed vocabulary (*karaka* as significator, *manas*/*vak*/*jnana* as graha-significations) and a warning about a false etymological bridge.
- **No attested link between Panini's *karaka* and Jyotisha's *karaka*** [negative finding, section 4.1]. The synthesis uses karaka only in Panini's sense.
- **No stage in the sources for "checking whether to say it at all"** — the Mahabhashya's purposes of grammar include *asandeha* (removal of doubt) but as a purpose of the discipline, not a stage in the pipeline. **[F]**

---

## Sources

Grouped by section, tagged **[P]** primary, **[S]** scholarly secondary, **[W]** general web. Reference-uncertain items are marked. This report did not fetch any source itself; sources were reached by four parallel research passes whose findings this report relays.

### The Ashtadhyayi

- **[P]** Panini, *Ashtadhyayi*. Sutras cited: 1.1.1, 1.1.5, 1.1.49, 1.1.56, 1.1.68, 1.1.71, 1.2.45, 1.2.64 (varttikas), 1.3.1, 1.3.3, 1.3.9, 1.4.1, 1.4.2, 1.4.14, 1.4.23-1.4.55, 2.3.1, 2.3.2, 2.3.13, 2.3.18, 2.3.28, 2.3.36, 2.3.46, 2.3.50, 3.1.91, 3.4.78, 4.1.1-4.1.2, 4.1.147, 6.1.77, 6.1.86, 6.4.22, 7.3.84, 8.2.1, 8.4.68. Several 2.3.x numbers unverified.
- **[P]** Katyayana, *Varttikas*; Patanjali, *Mahabhashya*; Jayaditya & Vamana, *Kashikavrtti*.
- **[S]** Wiebke Petersen, "A Mathematical Analysis of Panini's Sivasutras," *Journal of Logic, Language and Information* 13(4):471-489 (2004). `link.springer.com/article/10.1007/s10849-004-2117-7`
- **[S]** Petersen, "On the Construction of Sivasutra-Alphabets."
- **[S]** Paul Kiparsky, "On the Architecture of Panini's Grammar," in *Sanskrit Computational Linguistics*, LNCS 5402, Springer 2009. `link.springer.com/chapter/10.1007/978-3-642-00155-0_2`
- **[S]** Kiparsky & Staal, "Syntactic and Semantic Relations in Panini," *Foundations of Language* 5 (1969): 83-117.
- **[S]** Joshi & Kiparsky, *Panini as a Variationist* (1979/1980); Kiparsky, *Some Theoretical Problems in Panini's Grammar* (1982).
- **[S]** Joshi & Kiparsky, "The Extended Siddha-Principle." `web.stanford.edu/~kiparsky/Papers/siddha.new.pdf` — venue/year unverified; text not extracted.
- **[S]** George Cardona, *Panini: A Survey of Research* (Mouton 1976); "Panini's Syntactic Categories," *JOIB* (1967); "Panini's Karakas: Agency, Animation and Identity," *JIP* 2 (1974). `jstor.org/stable/23438766`
- **[S]** Madhav Deshpande, "Karakas: Direct and Indirect Relationships," in *Indian Linguistic Studies*.
- **[S]** Amba Kulkarni et al., "Semantic Processing in Panini's Karaka System," LNCS 5402. `link.springer.com/chapter/10.1007/978-3-642-00155-0_9`
- **[S]** Kulkarni, "Computer Simulation of Ashtadhyayi: Some Insights," LNCS 5402. `sanskritlibrary.org/symposium2/Papers/AmbaSimulation.pdf`
- **[S]** Kulkarni, "Paninian Syntactico-Semantic Relation Labels." `aclanthology.org/W19-7724.pdf`
- **[S]** Kulkarni, "Panini's Ashtadhyayi: A Computer Scientist's Viewpoint." (The phrase "Panini as a computer scientist" is **very likely Kulkarni's, not Kiparsky's** — a probable misattribution corrected here.)
- **[S]** Gerald Penn & Paul Kiparsky, "On Panini and the Generative Capacity of Contextualized Replacement Systems," COLING 2012 Posters, 943-950. `aclanthology.org/C12-2092/` — not read.
- **[S]** J. F. Staal, "Euclid and Panini," *Philosophy East and West* 15 (1965) [?]; "A Method of Linguistic Description," *Language* 38 (1962) [?]; *Word Order in Sanskrit and Universal Grammar* (Reidel 1967); *A Reader on the Sanskrit Grammarians* (MIT Press 1972).
- **[S]** Rishi Atul Rajpopat, *In Panini We Trust*, PhD thesis, Cambridge, 15 Dec 2022. `cam.ac.uk/system/files/rajpopat_phd_thesis_15_dec_2022.pdf`. Book: *Panini's Perfect Rule*, Harvard UP 2025.
- **[S]** Shodhganga thesis chapter on karaka theory. `shodhganga.inflibnet.ac.in/bitstream/10603/209380/14/14_chapter%205.pdf`
- **[W]** Learn Sanskrit Online: "The Structure of the Ashtadhyayi," "The Shiva Sutras," "karaka," "vibhakti," "The asiddha section." `learnsanskrit.org`
- **[W]** Wikipedia, "Shiva Sutras."
- **[W]** worldsanskrit.net, *sutranam balabalam*; Dharmawiki, *Utsarga Apavada Vyavastha*.
- **[W]** University of Cambridge press release, "Solving grammar's greatest puzzle"; Language Log `languagelog.ldc.upenn.edu/nll/?p=57378`; ANU China Institute, "A Marriage of Tradition and Technology."
- **[W, partisan — flagged]** Organiser, HinduPost, Samvada World, reporting Peter M. Scharf's critique of Rajpopat. **No peer-reviewed rebuttal located.**
- **[W]** Shreevatsa, Medium, on the karaka debate.
- **[?]** The six-fold sutra-type verse (*samjna ca paribhasha ca...*), source-unpinned; via Hindi Wikipedia and Sanskrit-grammar blogs.

### Expression: Bhartrihari, Patanjali

- **[P]** Bhartrihari, *Vakyapadiya*. Karikas cited: 1.1, I.44, I.46, I.48, I.49, I.50, I.76-78, I.97, 1.159 (Rau) / ~1.142 (Iyer), Vritti on 1.14, 2.143-152, 3.14.360-389. **All numbers edition-relative.**
- **[P]** Patanjali, *Mahabhashya*, Paspasahnika. *shabdapramanaka vayam* at **Kielhorn I.11.1-2** and ad A 2.1.1, **I.366.12-13** (located by Cardona).
- **[S]** Wilhelm Rau, *Bhartrharis Vakyapadiya: Die Mulakarikas*, DMG, Wiesbaden 1977.
- **[S]** K. A. Subramania Iyer, *Vakyapadiya Kanda I* (1966). `archive.org/details/VakyapadiyaOfBhartrhariKandaI1966K.A.SubramaniaIyer`
- **[S]** S. D. Joshi & J. A. F. Roodbergen, *Patanjali's Vyakarana-Mahabhashya: Paspasahnika*, University of Poona, 1986.
- **[S]** Harold G. Coward, *The Sphota Theory of Language: A Philosophical Analysis*, Motilal Banarsidass 1980/1997.
- **[S]** Bimal Krishna Matilal, *The Word and the World: India's Contribution to the Study of Language*, OUP 1990.
- **[S]** Ashok Aklujkar, *The Philosophy of Bhartrihari's Trikandi*, Harvard dissertation 1970 — quoted at second hand, **verify**.
- **[S]** Yoshichika Honda, "Bhartrihari on Sentence and its Meaning as *pratibha*," *JIBS* 46.2 (1998).
- **[S]** J. E. M. Houben, "Bhartrihari's Perspectivism (1)" and "(2)." academia.edu 35492240, 35807488.
- **[S]** Johannes Bronkhorst, "Studies on Bhartrihari, 8: *Prakrta Dhvani* and the Samkhya *Tanmatras*," *JIP* — not read.
- **[S]** Madeleine Biardeau — on separate Vritti authorship.
- **[S]** André Padoux, *Vac: The Concept of the Word in Selected Hindu Tantras*, trans. Gontier, SUNY 1990 — **not read; the book that would settle the *para vac* attribution.**
- **[S]** Jaideva Singh, trans., *Para-trishika-Vivarana of Abhinavagupta*, Motilal Banarsidass.
- **[S]** M. S. Murti, *Bhartrihari, the Grammarian* (1997).
- **[W]** IEP, "Bhartrihari." `iep.utm.edu/bhartrihari/` — **no SEP entry on Bhartrihari or sphota exists.**
- **[W]** Wikipedia, "Sphota," "Bhartrhari," "Mahabhashya." **Its gloss of vaikhari as the hearer's comprehension is anomalous and should not be relied on.**
- **[W]** wisdomlib: sphota theory (Tattvabindu study, doc1502612), "Vakyapadiya," "Vivaksha," "Paspasa," "Laukika," "Vaidika," "Shabda: A Valid Source of Knowledge."
- **[W]** sreenivasaraos.com — Bhartrihari, Vaikhari, Pashyanti, Dhvani, Abhinavagupta tags. **Well-informed blog, unrefereed; orienting only.**
- **[W]** indianwisdomtradition.blogspot.com and sanskritgyan.com — Hindi Paspasahnika studies quoting the Sanskrit.
- **[W, low authority — flagged]** philosophicain.wordpress.com, "Matrika and Malini." Its Tantraloka citation is malformed.
- **[W]** SARIT digital Vakyapadiya `sarit.indology.info/bhartrhari-vakyapadiya.xml` — returned HTTP 502.

### Psychology

- **[P]** *Samkhyakarika* 23, 24, 27, 29, 30, 31, 32, 33, 35, 36, 37. Verified against yogasutrastudy.info, scriptures.redzambala.com, yogastudies.org.
- **[P]** *Yoga Sutras* 1.2-1.11, 1.17, 1.18, 1.42-1.44, 1.50, 2.3-2.15, 3.17, 4.8-4.11, with **Vyasa's Bhashya on 3.17**. Woods (Harvard Oriental Series 1914) `amsi.ge/pat/ys_woods.html`; Rama Prasada (1924) via wisdomlib; Vivekananda via shlokam.org.
- **[P]** *Nyaya Sutras* 1.1.3-1.1.8, 1.1.32-1.1.39, with Vatsyayana's Bhashya — Ganganatha Jha translation. `archive.org/stream/NyayaSutra/nyaya_sutras_of_gautama_djvu.txt`
- **[P]** Annambhatta, *Tarkasamgraha*; Vishvanatha, *Bhashapariccheda* / *Nyayasiddhantamuktavali* (v. 84: *vaktur iccha tu tatparyam parikirtitam*); Gangesha, *Tattvacintamani* Shabdakhanda.
- **[P]** *Natyashastra* ch. 6, rasa-sutra as **prose following verse 31** — Manomohan Ghosh translation via wisdomlib.
- **[P]** *Abhidhammattha Sangaha* ch. 4 (*Vithi-sangaha*). `vipassana.info/chapter_4.htm`
- **[S]** Gerald Larson, *Classical Samkhya*, Motilal Banarsidass — not fetched.
- **[S]** Vacaspati Misra, *Tattvakaumudi*; Vijnanabhikshu, *Samkhyapravacanabhashya* — via wisdomlib essay on Vacaspati's contribution.
- **[S]** SEP: "Epistemology in Classical Indian Philosophy" (Phillips & Vaidya); "Perceptual Experience and Concepts in Classical Indian Philosophy" (Chadha); "Analytic Philosophy in Early Modern India" (Ganeri); "Language and Testimony in Classical Indian Philosophy" (Keating); "The Literal-Nonliteral Distinction in Classical Indian Philosophy" (Keating); "Abhidharma."
- **[S]** Pradyot Mondal (1982), on nirvikalpaka — via Chadha (SEP).
- **[S]** K. Kunjunni Raja, *Indian Theories of Meaning*, Adyar 1963. `archive.org/stream/kunjunni_raja_indian_theories_of_meaning/`
- **[S]** Jonardon Ganeri, *Semantic Powers*, OUP 1999.
- **[S]** Sheldon Pollock, *A Rasa Reader*, Columbia UP 2016.
- **[S]** Raniero Gnoli, *The Aesthetic Experience According to Abhinavagupta*, Chowkhamba 1968.
- **[S]** Ingalls, Masson & Patwardhan, *The Dhvanyaloka of Anandavardhana with the Locana of Abhinavagupta*, HOS 49, 1990.
- **[S]** Bhikkhu Bodhi, *A Comprehensive Manual of Abhidhamma*, BPS 1993. Introduction: `accesstoinsight.org/lib/authors/bodhi/abhiman.html`
- **[S]** Rupert Gethin, "Bhavanga and Rebirth According to the Abhidhamma"; L. S. Cousins, "The Patthana and the Development of the Theravadin Abhidhamma," *JPTS* IX (1981); Y. Karunadasa, *The Theravada Abhidhamma* (2010) — primary PDFs not fetched.
- **[S]** Lambert Schmithausen, *Alayavijnana* (1987) — secondary paraphrase only.
- **[W]** wisdomlib: "Pratyaksha in the old Nyaya" (doc1211191), "Sannikarsha and its divisions" (doc1601330), Tarkasamgraha essay (doc627342), Tattvabindu study (doc1502619), Vacaspati essay (doc627950).
- **[W]** Hindupedia, "Abhihitanvaya-vada"; anusilana.in on *vaktur iccha*; eGyankosh and inflibnet on rasa-sutra interpretations.

### Jyotisha

- **[P]** Varahamihira, *Brihat Jataka* ch. 2, v. 2.1 — N. Chidambaram Aiyar translation via chestofbooks; Sanskrit/English via wisdomlib.
- **[P]** *Brihat Parashara Hora Shastra*, ch. 3.12-15, ch. 8.39-43, ch. 11.2-13, ch. 32 (vv. 3-24), ch. 33 — R. Santhanam translation. `archive.org/stream/BPHSEnglish/BPHS%20-%201%20RSanthanam_djvu.txt`
- **[P]** Mantreshvara, *Phaladipika* ch. 1.10-16, ch. 2.26, ch. XV.17 — V. Subrahmanya Sastri translation (2nd ed. 1950). `archive.org/stream/Phaladeepika2ndEd.1950ByVSubrahmanyaSastri/...`
- **[P]** Jaimini, *Upadesha Sutras* 1.1 — Suryanarain Rao / B. V. Raman translation `archive.org/stream/in.ernet.dli.2015.142198/...`; Venkatesha-commentary numbering at jaiminicommentary.wordpress.com. **Sutra numbering varies by edition.**
- **[P]** *Paniniya Shiksha* 41-42 (vulgate/Panjika recension) — Sanskrit at advocatetanmoy.com and Hindi Wikipedia वेदांग. **Not found in Manomohan Ghosh's critical edition body; likely a transmitted addendum.**
- **[P]** Monier-Williams, *Sanskrit-English Dictionary* (1899), s.v. *karaka*. `sanskrit-lexicon.uni-koeln.de/monier/`
- **[S]** David Pingree, *Jyotihshastra: Astral and Mathematical Literature*, Harrassowitz 1981 — contents unverified.
- **[S]** Somanatha Misra, *Kalpalata*; Neelakantha, *Jaimini Sutra Bhashya* — classical commentaries, not consulted directly.
- **[W]** Satya Prakash Choudhary, "Light on 'Karaka'." `karmicrhythms.com/light-on-karaka/` — the most philologically careful jyotisha treatment located; **makes no reference to Panini.**
- **[W]** Wikipedia, "Atmakaraka," "Vedanga Jyotisha," "Jyotihshastra."
- **[W]** Vedic Heritage Portal, "Vedangas." `vedicheritage.gov.in/vedangas/`
- **[S]** "Importance of the Vedangas: An Analysis." `oaji.net/articles/2016/1707-1477986558.pdf`
- **[W, popular astrology — flagged]** jagannathhora.com, blog.pocketpandit.com, vedicka.com, steer.coach; yogainternational.com, veda.harekrsna.cz. Low evidentiary value; cited only to record that **none joins the four levels of vak to grahas or bhavas.**

### Modern uptake

- **[P]** Noam Chomsky, *Aspects of the Theory of Syntax*, MIT Press 1965, Preface p. v.
- **[P]** Peter Zilahy Ingerman, "'Panini-Backus Form' suggested," *CACM* 10(3), March 1967, p. 137. DOI 10.1145/363162.363165.
- **[S]** Paul Kiparsky, "'Elsewhere' in Phonology," in Anderson & Kiparsky (eds.), *A Festschrift for Morris Halle*, Holt Rinehart & Winston 1973, pp. 93-106.
- **[S]** Kiparsky, "Panini," in *The Oxford History of Phonology*. Bibliography: `web.stanford.edu/~kiparsky/Pubs/bibl.pdf`
- **[S]** Stephen R. Anderson, MIT dissertation 1969; Alan Prince, "Elsewhere & Otherwise," ROA-217. `roa.rutgers.edu/files/217-0997/roa-217-prince-2.pdf`
- **[S]** Bharati, Chaitanya & Sangal, *Natural Language Processing: A Paninian Perspective*, Prentice-Hall of India 1995; "Paninian framework and its application to Anusaraka," *Sadhana* 19(1), 1994.
- **[S]** Bharati, Sharma, Husain, Bai, Begum & Sangal, *AnnCorra: TreeBanks for Indian Languages — Guidelines for Annotating Hindi TreeBank v2.0*, LTRC IIIT-Hyderabad 2009.
- **[S]** Tandon, Chaudhry, Bhatt, Sharma & Xia, "Conversion from Paninian Karakas to Universal Dependencies for Hindi Dependency Treebank," LAW 2016.
- **[S]** Amba Kulkarni, arXiv 2201.01700 (karaka-yogyata), arXiv 2004.08076 (neural Sanskrit dependency parsing); ACL Anthology author page.
- **[S]** Gérard Huet & Amba Kulkarni, "A Distributed Platform for Sanskrit Processing," COLING 2012. `aclanthology.org/C12-1062.pdf`. Platform: `sanskrit.inria.fr`; code: `gitlab.inria.fr/huet/Heritage_Platform`
- **[S]** Willem J. M. Levelt, *Speaking: From Intention to Articulation*, MIT Press 1989.
- **[S]** Levelt, "Producing spoken language: a blueprint of the speaker," in Brown & Hagoort (eds.), *The Neurocognition of Language*, OUP 1999. `mpi.nl/world/materials/publications/levelt/Levelt_Producing_spoken_language_1999.pdf`
- **[S]** Levelt, Roelofs & Meyer, "A theory of lexical access in speech production," *Behavioral and Brain Sciences* 22(1), 1999, 1-38.
- **[S]** Levelt, "Spoken word production: a theory of lexical access," *PNAS* 98(23), 2001.
- **[S]** Ardi Roelofs, "The WEAVER model of word-form encoding in speech production," *Cognition* 64 (1997).
- **[S]** Merrill Garrett (1975, 1980) on the functional/positional distinction.
- **[S]** Gary Dell, "A spreading-activation theory of retrieval in sentence production," *Psychological Review* 93 (1986): 283-321.
- **[S]** Levelt, *A History of Psycholinguistics: The Pre-Chomskyan Era*, OUP 2013 — **no Indian-tradition chapter.**
- **[W]** Nick Nicholas, "What were Noam Chomsky's views on Panini's Ashtadhyayi?" `hellenisteukontos.opoudjis.net/2017-04-29-...`
- **[W]** Wikipedia, "Backus-Naur form," "Aspects of the Theory of Syntax."
- **[W]** *Psychology of Language* (open textbook), "Speech Production Models"; Wikiversity, "Models of Speech Production."
- **[W]** "Communication as Cognitive Unfolding: Bhartrihari's Theory of Vak in Vakyapadiya," academia.edu 145888776 — **frames the levels as thought-to-articulation but does not compare to Levelt.**
- **[W, advocacy — flagged]** Infinity Foundation / ECIT / indicmandala pieces on "The Panini-Backus Form"; 5sensestours.com "Panini: The World's First Programmer." Programmatic priority-claim content; discount.

### Flow psyche consulted

- **[P]** `/home/li/primary/flows/5851f4/vision/anatomyOfCommunicatingThinkingAndReacting.md` — the brief in the psyche's own words.
- **[P]** `/home/li/primary/flows/5851f4/vision/thinkingPhases.md` — the standing concern this anatomy was asked to serve, drawn on in 8.4 only.

### Negative findings, recorded as sources in their own right

- No source connects Jyotisha's *karaka* to Panini's *karaka*. Searched: Choudhary (karmicrhythms), Pingree-adjacent philology, general scholarly search. **Unattested.**
- No classical Jyotisha text stages cognition or speech-production across grahas or bhavas. **Unattested.**
- No classical text maps para/pashyanti/madhyama/vaikhari to grahas or bhavas; no systematic modern astrology treatment either. **Unattested.**
- No published comparison of Levelt's model to Panini or Bhartrihari. **Unattested.**
- No evidence Backus or Naur knew of Panini. Ingerman explicitly claimed independence. **Unattested; the influence claim is a later accretion.**
- No SEP entry on Bhartrihari, sphota, or rasa exists.
- No reliable account of the matrka/malini contrast was reached. **A genuine gap; Padoux and Tantraloka ahnikas 3 and 15 would be the sources.**
