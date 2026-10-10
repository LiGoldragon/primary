# Book Collision Audit — TheBookOfSol grain claims vs. the two 2026-07-22 evidence reports

Read-only audit. No book file was edited. No edit is recommended anywhere below;
this document reports collisions, it does not resolve them.

Compiled 2026-07-22.

## Sources

**Book (read-only):** `/home/li/primary/repos/TheBookOfSol`

**Evidence reports (read-only):**

- `/home/li/primary/agent-outputs/BookOfSol-grain-research/rice-and-wheat.md`
  (tiers E1–E4, provenance `(v)` verified in-session / `(r)` recalled)
- `/home/li/primary/agent-outputs/BookOfSol-grain-research/canon-and-minor-grains.md`
  (Part 1 canonical philology; Part 2 modern measurement with STRONG / MODERATE /
  WEAK / NEGATIVE / UNSUPPORTED / HYPOTHESIS verdicts and `[delegated]` provenance flags)

Tiers are respected throughout. Where a report says a finding is E3, E4, HYPOTHESIS,
or explicitly unresolved, that is stated at the point of use and the collision is
scored no stronger than the tier permits.

## How the book was searched

`grep -rinE` over the whole repository for: grain, grains, rice, wheat, barley, oat,
oats, millet, millets, gluten, lectin, lectins, phytate, phytic, starch, protein,
glycaem/glycem, śāli, ṣaṣṭika, yava, godhūma, vrīhi, śyāmāka, anna, dhānya, arsenic,
cadmium, celiac/coeliac, fibre/fiber, glucan, phytase, ferment, sourdough, sprout,
germinat, parboil, polish, brown rice, white rice, whole grain.

**Observation worth recording before any collision.** The following words return
**zero hits anywhere in the book**: *lectin*, *phytate*, *phytic*, *glycaemic*,
*resistant starch*, *amylase*, *celiac*, *coeliac*, *β-glucan*, *glucan*, *phytase*,
*sourdough*, *parboil*, *brown rice*, *white rice*, *whole grain*, and *arsenic* /
*cadmium* in any food context (the single `arsenic` hit is a Sylvester Graham quote
about salt in `chloride/witnesses/Witnesses_Against_Salt_Hygienists.md:50`). The
book's grain doctrine is argued entirely in *guṇa* vocabulary plus one negative
epistemological claim about the modern literature. This shapes the whole audit:
most collisions are either (a) canon-vs-canon, or (b) the book asserting the absence
of evidence that the reports supply.

## Verdict counts

| Verdict | Count |
|---|---|
| CONTRADICTED | 8 |
| UNSUPPORTED | 7 |
| CONFIRMED | 7 |
| STRENGTHENABLE | 8 |
| Book claims neither report covers (gaps) | 22 |
| Sanskrit attribution collisions | 6 flagged + 5 checked-clean |

## Discipline note

**OBSERVATION** = what the book's text says, and what a study measured.
**HYPOTHESIS** = a causal or interpretive reading not established by the cited work.
**UNKNOWN** = neither report determines it.
These are labelled inline. No contradiction below is softened, and none is
manufactured: three candidate collisions I checked came out clean and are recorded
as such in §6 so the checking is visible.

# 1. CONTRADICTED

Ranked by how load-bearing the claim is.

## C1 — "The hypothesis of intrinsic grain toxicity has zero experimental support"

**Book claim,** `diet/Fear_of_Grains.md`:

- L5: *"Experimental science requires isolation, control, and falsification. None of
  the claims underlying grain or gluten avoidance meet that threshold. No experiment
  has isolated grains themselves — wheat included — prepared in non-irritating forms,
  while independently controlling hydration, chloride load, preparation method, and
  quantity, and demonstrated intrinsic harm. **The hypothesis that grains are
  inherently problematic has never been tested.**"*
- L17: *"The correct scientific statement is plain: the hypothesis of intrinsic grain
  toxicity has zero experimental support."*
- L19: *"The fear of grains, and the fear of gluten as its symbolic focus, persists by
  repetition. **It has never been properly tested.**"*
- L9 (on Dicke): *"**Gluten was not isolated. No experiment was performed.**"*

**Evidence.**

*rice-and-wheat.md* §II.3, quoted: *"Pooled global prevalence: **Seroprevalence**
(anti-tTG and/or EMA positive): **1.4%** (95% CI 1.1–1.7), n = 275,818;
**Biopsy-confirmed**: **0.7%** (95% CI 0.5–0.9), n = 138,792"* — Singh P, Arora A,
Strand TA, Leffler DA, Catassi C, Green PH, et al., *Clin Gastroenterol Hepatol*
2018;16(6):823–836.e2. **[E1]**. The report's own summary: *"This is the only
wheat-related condition with an unambiguous mechanism, a defined genetic restriction
(HLA-DQ2.5/DQ8), a diagnostic standard, and a proven treatment."*

Mechanism, §II.2 **[E1]**: the immunodominant peptide α2-gliadin p57–89 is a
*"**33-amino-acid, proline-rich, protease-resistant fragment containing six partly
overlapping copies of three DQ2.5-restricted T-cell epitopes**"* encoded at *Gli-D2*
(Ozuna CV, et al., *Plant J* 2015;82(5):794–805).

Gluten *has* been isolated and blind-administered to humans. §II.6, Skodje GI, et al.,
*Gastroenterology* 2018;154(3):529–539.e2: **double-blind, randomised,
placebo-controlled crossover; n = 59** adults, celiac excluded; concealed in muesli
bars, 7 days per arm with ≥7-day washout; **gluten 5.7 g, fructan 2.1 g, or placebo**.
§II.7 Point 2, Biesiekierski 2013: gluten added back at **16 g/day** against a
FODMAP-reduced background. §II.11: extensively hydrolysed sourdough products were
*"tolerated by celiac patients over 60 days without symptoms or histological change."*

**Verdict: CONTRADICTED.** The absolute form of the claim fails. Gluten has been
isolated, concealed, dose-controlled, blind-administered and scored against placebo
in humans, with histological endpoints available in the celiac literature.

**What survives, stated precisely.** The book's *narrow conjunctive* claim at L5 —
that no trial has controlled **chloride load** and **hydration** and **preparation
method** simultaneously — is **not** contradicted. Neither report identifies any trial
that controlled sodium chloride, hydration state, or a wet-porridge-versus-bread
contrast. That specific negative stands (see §5, gaps G5–G6).

**Load-bearing: maximal — the whole file.** `Fear_of_Grains.md` is a single argument
whose thesis sentence (L3) and closing sentence (L19) both restate this claim. If the
absolute form goes, what remains is a much narrower and defensible claim about a
*specific untested comparison*, plus the file's historical critiques of Dicke, Atkins
and Davis — which the reports actually strengthen (see S1–S4). Downstream, the claim
is the licence for `diet/Grains.md`'s framing that grains are blamed without warrant.

## C2 — "wheat yields gluten … the body encounters them as obstacles"

**Book claim,** `diet/Protein.md`:

- L13: *"Across all foods, the same fraction behaves the same way: the resistant
  portion clings, ferments, and rots. Milk yields casein, flesh yields fibrous strands,
  **wheat yields gluten**, legumes yield foaming sludge. These residues share no
  subtlety or vitality; they share only resistance. **The body encounters them as
  obstacles.**"*
- L15: *"**Digestion of this dense residue is dismantling, not assimilation.**"*
- L7: *"Examined without inherited awe, what goes under the name of protein reveals no
  correspondence with vitality."*

**Evidence.**

*rice-and-wheat.md* §I.1, the FAO-preferred DIAAS metric (pig standardised ileal
digestibility, 0.5–3 y reference pattern), Herreman L, Nommensen P, Pennings B,
Laus MC, *Food Sci Nutr* 2020;8(10):5379–5391 **[E1 for the numbers]**:

| Protein | DIAAS |
|---|---|
| Corn | 36 ± 14.9 |
| Rice | 47 ± 2.3 |
| Wheat | 48 ± 10.6 |
| Oat | 57 ± 5.8 |
| Whey | 85 ± 10.8 |
| Egg | 101 ± 11.7 |
| **Casein / pork** | **117** |

Casein — the book's first named exemplar of inert residue — scores highest of every
protein in the table. In humans directly, §I.1 also records an indicator-amino-acid-
oxidation study in healthy young men reporting that *"lysine from cooked white rice is
**highly metabolically available**"* **[E2]** — testing the limiting amino acid in
humans rather than by pig proxy.

Population-scale, §II.12: Lebwohl B, et al., *BMJ* 2017;357:j1892 **[E2 observational,
large, well-adjusted]** — ~110,000 participants (64,714 Nurses' Health Study women;
45,303 Health Professionals Follow-up Study men), celiac excluded: no association
between estimated gluten intake and incident coronary heart disease, and *"**After
adjustment for refined grain intake, higher gluten intake was associated with LOWER CHD
risk: HR 0.85 (0.77–0.93)**."*

**The one measurement that goes the book's way, at its true tier.** §I.1 **[E2]**:
*"Intact rice prolamin/PB-I particles have been recovered by electron microscopy from
fresh human faeces, having survived pepsin proteolysis; PB-II glutelin is readily
digested."* This is a genuine measured undigested protein residue — but it is **rice
prolamin**, not gluten or casein, and the report states that *"the exact quantitative
contribution of PB-I escape to whole-diet protein losses in humans is **unknown**."*

**Verdict: CONTRADICTED.** The claim that this fraction is uniformly non-assimilable is
the direct negation of what the standard method measures, and the measurement runs
hardest against the book's own named exemplar.

**Load-bearing: maximal — the whole file, plus one other file.** `Protein.md`'s
sections "Residue, Toxicity, and the Burden on the Body," "A Belief System Defending
Itself" and "The Failure of the Nutrient and Machine Models" all rest on the premise
that the protein fraction is not assimilated. If it goes, what remains is a separate
and unaddressed argument about *measurement frames* (L29–L33), not about physiology.
Downstream: `ayurveda/Madhumeha.md:13` (*"Concentrated tissue-foods … behave as tamasic
residue"*) and `:49` (*"All concentrated tissue-foods must be stopped"*) inherit the
premise as a therapeutic instruction.

## C3 — "A grain functions as a neutral substrate"

**Book claim,** `diet/Grains.md:3`: *"Grains are routinely blamed for heaviness,
eruptions, and reactivity; Āyurveda assigns responsibility to **preparation,
combination, and condition**. **A grain functions as a neutral substrate** whose effect
is formed by **saṃskāra** (processing), **saṃyoga** (combination), **uṣṇatā–śītatā**
(temperature), **ārdra–rūkṣa** (moisture or dryness), **kāla** (timing), **deśa** and
**guṇa** (quality and provenance)…"*

**Evidence — from the canon the sentence invokes.**

*canon-and-minor-grains.md* §1.3 records Caraka Sū. 27.8–22 assigning intrinsic
per-cultivar properties *before* any processing variable:

- śāli group (27.10): *śīta* in vīrya, *madhura* in both rasa and vipāka,
  *alpa-māruta*, binding, *snigdha*, *bṛṃhaṇa*, *śukrala*, *mūtrala*.
- vrīhi (27.15): *"**Madhura* in rasa but **amla* in vipāka** — sour post-digestion —
  hence *pittakara* and *guru*."*
- yava (27.19): *rūkṣa*, *śīta*, ***aguru***, *svādu*, ***bahu-vāta-śakṛt***,
  *sthairyakṛt*, *balya*, *śleṣma-vikāra-nut*.
- godhūma (27.21): ***sandhāna-kṛt***, *vāta-hara*, *svādu*, *śītala*, *jīvana*,
  *bṛṃhaṇa*, *vṛṣya*, *snigdha*, *sthairyakara*, ***guru***.

The report's own summary line: *"**Barley is *aguru*; wheat is *guru*. The two are
opposed on exactly that axis.**"* And §1.4: Sū. 25.38 makes *rakta-śāli* the single
*pathyatama* substance of the class; Sū. 25.39 makes *yavaka* the single *apathyatama*
of the same class. These are rankings of grains against each other, at fixed
preparation.

**Evidence — modern.** DIAAS separates the cereals (C2 table above) **[E1]**. Celiac
toxicity is Triticeae-restricted and rice-absent (*rice-and-wheat.md* §I.2, **[E1]**:
*"Rice contains no gliadin/glutenin-equivalent proteins … Rice's celiac safety is
settled clinical practice"*).

**Verdict: CONTRADICTED**, on both limbs, and notably by the authority the sentence
cites in its own clause.

**Load-bearing: high.** It is the opening thesis of `Grains.md` and the implicit premise
of `Fear_of_Grains.md`'s central inference — that generalising from preparation to
ingredient is *invalid in principle*. If grains are not neutral substrates, that
inference becomes an argument about the *relative size* of a preparation effect versus
a species effect, which is an empirical question the book does not take up.

## C4 — "Ṣaṣṭika, śāli, mudga, yava, dhānya — five grains"

**Book claim,** three files:

- `source-extracts/Fruit_as_Medicine.md:285`: *"The list is the entire Caraka theory of
  daily eating in one verse. ***Ṣaṣṭika, śāli, mudga, yava, dhānya* — five grains.**"*
- `source-extracts/Cooking_and_Agni.md:197`: *"Of the items: *ṣaṣṭika*, *śāli*, *mudga*,
  *yava*, *dhānya* — **five grains**, all cooked before eating…"*
- `source-extracts/Raw_and_Cooked_Cross_Tradition.md:103`: *"**Five grains at the
  centre.** The Sanskrit canonical daily-routine list (Caraka Sū. 5.12) names *ṣaṣṭika,
  śāli, mudga, yava, dhānya* — **five grains**. Two corpora, two cosmologies, the same
  plate."* — repeated at `:197`: *"The HDNJ names five grains as primary nourishment.
  Caraka Sū. 5.12 names five grains."*

**Evidence.** *canon-and-minor-grains.md* §1.4, on Sū. 5.12: *"**Caveat:** the received
Sanskrit of this verse has three independent anomalies (a number/gender disagreement at
*saindhavān lavaṇaṃ*; ***dhānyaṃ* rendered "rain water" by two translators without
warrant**; *ghṛtam* appearing twice), and one lineage adds *jāṅgala-māṃsa*."*

And §1.2 on the varga scheme: *"**Caraka** (Sū. 27.5) opens the food catalogue with
twelve *vargas*, of which *śūkadhānya* (awned grain) is first and **śamīdhānya*
(legume) second."* §1.4: *"Sū. 25.38 — *rakta-śāli* is the single most wholesome
(*pathyatama*) substance among the *śūkadhānya*; **mudga* (green gram) is best among
legumes**."* §1.5 identifies *śāli* and *ṣaṣṭika* as two cultivar groups of the same
species, *Oryza sativa* L.

So the five decompose as: **ṣaṣṭika + śāli = one species, two cultivar groups**;
**mudga = a legume, in a different varga**; **yava = barley**; **dhānya = the disputed
term**. That is at most three distinct grains, two of which are the same species.

**Aggravating internal fact.** In all three files the book's own quoted *translation*,
two lines above the count, renders *dhānya* as **"rain water"**:
`Fruit_as_Medicine.md:280–282`, `Cooking_and_Agni.md:192–194`,
`source-extracts/Apathya.md:369–371` all read *"…barley, **rain water**, milk, ghee and
honey."* The same item is water in the quotation and a grain in the prose beneath it.
The book's own `ayurveda/Apathya.md:289` gets the legume right — *"Rice and other grains
(*ṣaṣṭika*, *śāli*, barley). Mung (*mudga*) and other pulses"* — so the miscount is
confined to the source-extracts.

**Verdict: CONTRADICTED.**

**Load-bearing: high, and specific.** At `Raw_and_Cooked_Cross_Tradition.md:103` the
number **is** the argument: the whole cross-tradition convergence rests on the
numerical coincidence with the Huang Di Nei Jing's five grains (`:97` — *"They are
wheat, glutinous millet, millet, rice, and beans"*, itself a list containing beans).
If the count goes, the coincidence goes and the convergence reverts to a qualitative
resemblance, which is what `:197`'s synthesis point 3 also asserts. At
`Fruit_as_Medicine.md:285` it supports *"The daily plate is grain plus rasāyana plus
medicinal salt"* — a claim that survives in weakened form (grain is still the plurality
of the verse) but not at "five."

## C5 — "vrīhi-yavādayaḥ anna-vargaḥ"

**Book claim,** `diet/Yogic_Food.md:25–28`:

> *"**vrīhi-yavādayaḥ anna-vargaḥ.***
>
> *"Rice, barley, and the like constitute the anna category."\
> — proverbial formulation, after* Caraka Saṃhitā *Sūtrasthāna 27"*

and immediately after, `:30`: *"**Anna is grain specifically, not "food in general."**"*

**Evidence.** *canon-and-minor-grains.md* §1.2: *"**Caraka** (Sū. 27.5) opens the food
catalogue with twelve *vargas*, of which *śūkadhānya* (awned grain) is first and
*śamīdhānya* (legume) second. **Caraka himself gives no sub-classification of the awned
grains and never uses the word *kudhānya***."* There is no *anna-varga* in Caraka's
scheme; the awned-grain category is *śūkadhānya*, which the book itself quotes
correctly elsewhere (`Fruit_as_Medicine.md:69`, from Sū. 27.5–7).

Second limb: *vrīhi* is the wrong exemplar. §1.3 on 27.15 — vrīhi is *amla* in vipāka,
*pittakara*, *guru*, with the *pāṭala* variety *"produc[ing] copious urine, faeces and
heat and disturb[ing] all three doṣas."* §1.10 files *vrīhi* under **"Restricted or
downgraded."** §1.7.6 further records a classificatory dispute: *"Caraka places vrīhi in
śūkadhānya; Suśruta places it inside the śāli varga."*

**Verdict: CONTRADICTED** on both limbs — the varga name is not Caraka's, and the grain
chosen to fix the referent of *anna* is the one Caraka downgrades. The book's *"proverbial
formulation, after"* hedge covers the wording; it does not cover the content, because the
sentence's job is to fix a referent and it fixes it on the demoted rice.

**Load-bearing: high, and it propagates.** This quotation is the pivot of
`Yogic_Food.md` — it licenses `:30` *"Anna is grain specifically"*, which is restated as
load-bearing at `diet/Ambrosian_Diet.md:35` (*"Anna is not 'food in general.' It is a
technical term with a fixed referent across the Sanskrit corpus: grain. Rice, barley,
wheat."*) and `diet/Yogis_Dont_Eat_Fruit.md:7`. **The referent claim itself survives on
other grounds** — canon §1.9 gives verified Sanskrit for HYP 1.62–63 naming four grains
as *śobhanānna* — so what falls is the citation, not the conclusion.

## C6 — "Soft rice, millet, or oats cooked very moist restore mass and peristaltic coordination"

**Book claim,** `diet/Fruitarianism.md:56`: *"*Grounding when needed.* **Soft rice,
millet, or oats cooked very moist restore mass and peristaltic coordination**, a
correction rather than a contradiction."* — in a prescriptive list under "How
nourishment actually happens," addressed to a depleted (vāta-excess) reader.

**Evidence — millet, canon.** *canon-and-minor-grains.md* §1.3, Caraka 27.16:
śyāmāka-with-koradūṣa is *kaṣāya-madhura*, *laghu* (light), ***vātala*** (vāta-
aggravating), *kapha-pitta-ghna*, *śīta*, *saṅgrāhi* (binding), ***śoṣaṇa***
(absorbing/drying). §1.7.1: Suśruta Sū. 46.21–25 makes the kudhānya group ***uṣṇa***,
*rūkṣa*, *kaṭu*-vipāka, kapha-subduing but ***vāta- and pitta-aggravating***, and
urine-retaining; Vāgbhaṭa's *tṛṇa-dhānya* verse gives *śīta*, *laghu*, vāta-increasing,
***lekhana*** (scraping). The report's own conclusion: *"**There is no canonical
consensus on millet vīrya**"* — but every source surveyed agrees millet is
vāta-increasing and drying, scraping or binding. That is the opposite register from
"restore mass."

**Evidence — oats, canon.** §1.5, verbatim: *"**Grains conspicuously absent from every
list above:** oats (*Avena sativa*), rye (*Secale cereale*), maize (*Zea mays*), and
buckwheat. … **The canon has nothing to say about oats.** Any Āyurvedic property
assignment for oats is a modern extrapolation from taste and texture, not a textual
transmission."*

**Evidence — millet, modern.** §2.8, Malavika M, Shobana S, …Mohan V, Sudha V,
*Indian J Med Res* 2020;152(4):401–9: **12 healthy volunteers**, standard international
GI methodology — *"**unpolished foxtail millet GI 88.6 ± 8.7; unpolished little millet
GI 88.6 ± 5.7; white rice GI 82.5 ± 8.8.** The millets scored **higher than white
rice**."* Same paper: 48 brands across 100 retailers, *"**~90% of market millet samples
heavily polished** despite label claims."* The report's verdict on the competing
promotional meta-analysis (Anitha 2021, GI 52.7 ± 10.3): *"**WEAK, and the headline
number is contradicted by direct measurement.**"*

**Verdict: CONTRADICTED for millet** (canon and direct measurement both run against it);
**UNSUPPORTED-from-canon for oats** (no canonical basis of any kind exists).

**Load-bearing: an aside, but a prescriptive one.** It is one sentence in a list; nothing
else in the book depends on it. What falls if it goes is one line of dietary advice given
to a depleted reader on the authority of a corpus that (a) never mentions one of the two
grains named and (b) assigns the other the opposite qualities. The surrounding sentences
(*"Sweet as grounding … well-cooked grain"*, `:50`) do not depend on it.

## C7 — Madhumeha prescribed without the canon's own prameha grain

**Book claim,** `ayurveda/Madhumeha.md`, subtitled *"A Clean Ayurvedic Guide for
Dissolving Madhumeha"*:

- L76–81 (Practical Daily Structure, Midday): *"A single light, cooked meal, with ripe
  fruit in season taken by indication / No concentrated tissue-foods … / No salt / No
  nuts or seeds in excess / Ghee as the sole dairy."*
- No grain is named anywhere in the file.

The book's fixed referent for "a single light, cooked meal" is set elsewhere:
`ayurveda/Apathya.md:171` and `:296` — *"**Vilēpī* — rice porridge with water and
ghee"*; `diet/Ambrosian_Diet.md:148` — *"**Anna**: grain cooked soft in ample water,
finished with ghee. Vilēpī, peya, yavāgū. The stable ground."*

**Evidence — canon.** *canon-and-minor-grains.md* §1.4, verbatim: *"**Sū. 27, kṛtānna
section** — *apūpa*, *yāvaka* and *vāṭya* made of barley remove *udāvarta*, coryza,
cough, ***prameha*** (the polyuric/diabetic syndrome) and throat disorders. **Barley is
the text's named grain for prameha.**"* Also §1.4, Sū. 27.305: *yāvaśūka* (alkali from
barley awns) is indicated for heart disease, anaemia, grahaṇī, splenomegaly, throat
disease, kaphaja cough and piles.

**Evidence — modern, at its stated tier.** *rice-and-wheat.md* §13, Hu EA, Pan A, Malik
V, Sun Q, *BMJ* 2012;344:e1454 **[E2 observational]**: white rice intake and incident
type 2 diabetes, pooled **RR 1.11 per serving/day (95% CI 1.08–1.14)**; Asian
populations at 3–4 servings/day pooled **RR 1.55**; Western at 1–2 servings/week **1.12**;
**7 prospective cohorts, 13,284 incident cases among 352,384 participants, follow-up
4–22 years.** The report's own caveats, carried: *"Residual confounding by overall diet
quality and socioeconomic transition is a live concern, and the association is
dose-dependent rather than categorical. The mechanistic reading … is plausible but is a
**hypothesis**, and the corresponding brown-rice substitution trials on hard endpoints
do not exist."*

**Verdict: CONTRADICTED on the canonical limb** — a file presenting itself as a clean
Āyurvedic protocol for the diabetic syndrome omits the one grain Caraka names for that
syndrome, while the book's default staple elsewhere is the rice preparation. **The
modern limb is E2 observational only** and does not establish causation; it is reported
here at that tier and no stronger.

**Load-bearing: high within its file.** `Madhumeha.md` is a therapeutic protocol given
as a daily structure (L68–91). The grain question is not an aside in a file about a
carbohydrate-metabolism syndrome; it is the one lever the invoked canon actually pulls
for this indication, and the file does not pull it. What falls if the collision stands
is the file's claim to be "clean Ayurvedic" for this specific condition — not the
solar/lunar framework, which is argued independently.

## C8 — "Across both of its great manuals the Yogic corpus prescribes the same plate"

**Book claim,** `diet/Yogis_Dont_Eat_Fruit.md:24`: *"The *Gheraṇḍa Saṃhitā* opens its
own food list with rice, barley bread, wheat bread, and legumes, and gives **ghee,
butter, and milk a prominent place**. … **Across both of its great manuals the Yogic
corpus prescribes the same plate**: the body of the meal is grain and ghee, and fruit is
an accessory admitted by name and by season."* The same convergence underwrites
`diet/Ambrosian_Diet.md:156–158` and the ghee-supremacy argument of
`diet/Penultimate_Sāttvic_Food.md`.

**Evidence.** *canon-and-minor-grains.md* §1.9, Gheraṇḍa Saṃhitā, verbatim:

> *"**5.23–27, 5.29–31** — apathya: bitter, acid, salt, pungent and roasted things,
> curd, whey, heavy vegetables, wine, *kulattha* and *masūr*, many fruits — **and also
> fresh butter, ghee, thickened milk, sugar and date-sugar**."*

and the report's conclusion: *"Gheraṇḍa's apathya includes **ghee, butter, sugar and
thickened milk — the very items HYP's pathya verse names as wholesome.** This is a flat
contradiction between the two principal haṭha manuals."*

**Tier, stated fully.** The report qualifies its own finding: the Gheraṇḍa material is
*"Verse-range and content via a peer-reviewed review; **Sanskrit not obtained**"*
(§1.1), and the contradiction *"may be softened by the Vasu translation's framing ('in
the beginning of yoga-practice, one should discard…'), i.e. a staged rather than
absolute prohibition. **Flagged as translation-dependent and not resolved here.**"*

**Verdict: CONTRADICTED**, at the weak tier the report itself assigns. The best available
reading of Gheraṇḍa places ghee, butter and thickened milk on the *apathya* side; the
book asserts the two manuals agree. This does **not** settle the matter — the Sanskrit
was not obtained by either party.

A second divergence in the same section: Gheraṇḍa's pathya admits ***māṣa* (urad)** and
***caṇaka* (chickpea)**, *"where Caraka Sū. 25.39 ranks **māṣa* the single most
unwholesome legume**. The yogic and the medical canon diverge here."* The book's
convergence argument does not register this either.

**Load-bearing: moderate-to-high.** `Yogis_Dont_Eat_Fruit.md` cites Gheraṇḍa 5.16 twice
(at `:131–136`) as the disqualifier of unmeasured practice, and `Ambrosian_Diet.md:166–171`
does the same. Using Gheraṇḍa's chapter 5 for *mitāhāra* while relying on HYP for ghee,
without noting that Gheraṇḍa's own chapter 5 lists ghee among things to discard, is the
exposed joint. If it goes, the ghee case rests on Caraka and the Ṛgveda (which is where
`Penultimate_Sāttvic_Food.md` mainly puts it), not on a two-manual yogic consensus.

# 2. UNSUPPORTED

Book asserts more than any evidence in either report establishes, without being
contradicted. Ranked by how load-bearing.

## U1 — vilepī as "the gold standard for taking grains"

**Book claim.** `diet/Grains.md:32`: *"This preparation is treated not as a compromise,
but as the **gold standard** for taking grains and supplying the stable material the
body uses to rebuild itself."* `:5`: *"This form **minimizes friction, supports
rebuilding, and supplies stable nourishment**."* Restated at `diet/Yogic_Food.md:5,37`,
`diet/Ambrosian_Diet.md:148`, `diet/Yogis_Dont_Eat_Fruit.md:129`.

**Evidence bearing on it.** **Neither report contains a single study of a slow-cooked
wet grain porridge on any human endpoint.** The nearest measured processes point
elsewhere, and one points against:

- *Parboiling* (soak, steam in husk, dry, mill) is described in *rice-and-wheat.md* §4
  as *"one of the few traditional food processes whose biochemistry is well
  characterised"* — thiamine, niacin and B6 in the milled endosperm rise **roughly
  three-fold [E1]**; gelatinisation-then-retrogradation converts RDS to SDS and RS
  **[E1 in vitro]**. Human data: Alkandari S, et al., *Foods* 2025;14(11):1905,
  randomised crossover at 50 g available carbohydrate — healthy **n = 9**, glucose AUC
  177.86 ± 50.02 (parboiled) vs 245.56 ± 87.78 mmol·min/L (white), **p = 0.047**; T2D
  **n = 8 / 6**, 187.38 ± 75.87 vs 278.83 ± 84.28, **p = 0.051**. Report tier: **[E3]**
  — *"n=9/8, acute only, COVID-disrupted recruitment, and the T2D result missed
  significance. Treat as supportive, not conclusive."* This is a hydrothermal-and-dried
  process, not a wet porridge.
- *Wet cooking measured against the one grain fraction with an E1 human effect goes the
  wrong way.* *canon-and-minor-grains.md* §2.4, Grundy MML, Quint J, Rieder A, et al.,
  *Carbohydr Polym* 2017;175:20–7 **[delegated]**: cooking **halved extractability**
  (56.3% → 28.8% for oat flour; 50.5% → 25.1% for flakes) **with molecular weight
  essentially unchanged**, attributed to starch gelatinisation physically trapping the
  β-glucan. Since the clinical variable is **Mw × solubilised concentration**
  (Wolever 2010, §2.2, 345 completers), halving solubilised concentration reduces the
  delivered effect at unchanged grams.
- *The processes with the strongest measured benefits are acidification and
  fermentation, not water-cooking.* Sourdough at pH 3.6–3.7: phytate down up to ~90%
  **[E2]**; fructans consumed **[E2]**; ATI tetramers partially degraded with human
  THP-1 monocytes releasing significantly less MCP-1 and TNF-α, p < 0.05 **[E3]**.

**Verdict: UNSUPPORTED.** Nothing contradicts vilepī. Nothing establishes it as superior
to any alternative on any measured endpoint, and where wet cooking has been measured
against a fraction with a demonstrated human effect it reduces delivery.

**Load-bearing: maximal in scope, minimal in what falls.** This is the operative
prescription of four files. But what the reports touch is only the phrase **"gold
standard"**, which reads as an evidential ranking. The *textual* case for vilepī — the
Caraka yavāgū / peyā / vilēpī register — is untouched by either report (see U5, U6, G7
for the state of that case's own citations).

## U2 — "The idea of a safe threshold arises from theory, not from physiology"

**Book claim,** `diet/Protein.md:17`: *"The residue obstructs the body's channels …
**Whether consumed in small or large quantities, its nature does not change. What harms
in excess harms in principle. The idea of a safe threshold arises from theory, not from
physiology.**"*

**Evidence.** Neither report contains a dose-threshold study for dietary protein. The
claim is UNSUPPORTED in the strict sense.

But the reports are saturated with measured dietary dose-response, which is the general
proposition the sentence denies:

- WGA (*rice-and-wheat.md* §II.5, **[E4 for the harm claim]**): adverse GI effects occur
  at **7 g WGA/kg body weight over 10 days** — *"For a 70 kg human that would be ~490 g
  of pure WGA over ten days; at 50 µg/g whole wheat flour, that is nominally ~10,000 kg
  of flour."* Cooked pasta ~0.3 µg/g. The report's framing: *"the gap between the doses
  that do anything in vivo and dietary doses is roughly six orders of magnitude."*
- Phytate (*canon-and-minor-grains.md* §2.9, **[delegated]**): Hallberg L, Brune M,
  Rossander L, *Am J Clin Nutr* 1989;49:140–4 — **2 mg phytate inhibited iron absorption
  by 18%, 25 mg by 64%, 250 mg by 82%** — a semilogarithmic dose-response. Hallberg 1987:
  *"as little as 5–10 mg phytate phosphorus added to a wheat roll containing 3 mg iron
  inhibited iron absorption by 50 per cent."*
- Gluten in NCGS (§II.6–7): 5.7 g concealed produced a measurable group effect; 16 g/day
  against a FODMAP-reduced background did not.

**Verdict: UNSUPPORTED.**

**Load-bearing: high within its file, and it exports.** This is the sentence that converts
`Protein.md` from a critique of excess into a categorical prohibition. It is what licenses
`ayurveda/Madhumeha.md:49` — *"**All** concentrated tissue-foods **must be stopped**"* —
as an absolute rather than a dose instruction. If it goes, `Protein.md`'s argument
becomes a dose argument, which the book does not currently make.

## U3 — "grains cooked slowly in ample water are moistening; the same grains rendered dry, browned, and concentrated are drying and irritating"

**Book claim,** `diet/Fear_of_Grains.md:7`: *"Traditional medical systems such as
**Āyurveda** are emphatic that preparation is constitutive of effect: **grains cooked
slowly in ample water are treated as moistening, supportive, and restorative, whereas
the same grains rendered dry, browned, and concentrated are treated as drying and
irritating.** Modern discourse erased this distinction and generalized outcomes observed
with the most aggressive preparation forms — baked, dehydrated, salted products — to the
grain itself."*

**Evidence.** *canon-and-minor-grains.md* §1.4 records Caraka's own named example of a
beneficial *saṃskāra*, and it is dry parching: *"**Sū. 27.339** — processing overrides
intrinsic quality: *vrīhi*, heavy, becomes light when parched into *lājā*."* And §1.4
again: *"**Sū. 27.309–310** — cereals and legumes are recommended **one year old**; new
grain is *guru* and kapha-producing, old grain mostly ***rūkṣa***."* — the canon prefers
the drier, aged grain.

**Verdict: UNSUPPORTED.** The wet-good / dry-bad dichotomy attributed to Āyurveda is not
found in the canon report, and for the dry-parching case the canon runs the other way.
Note that the book **quotes 27.339 correctly elsewhere** and draws the opposite lesson
there — `diet/In_Praise_of_Agni.md:78–79` and `source-extracts/Cooking_and_Agni.md:146–150`
both present *vrīhi → lājā* as heat *lightening* a heavy grain.

**Load-bearing: high within its file.** This is the mechanism sentence of
`Fear_of_Grains.md` — the specific diagnosis of what modern discourse got wrong. If the
canon does not license "dry/browned = irritating," the file's diagnosis loses its
Āyurvedic backing and the argument reduces to the (independent, surviving) epistemological
point that the ingredient was never tested apart from the product.

## U4 — "washing … removes surface impurities so cooking proceeds on a clean substrate"

**Book claim,** `diet/Grains.md:3`: *"Grain grown in degraded soil, treated with modern
agrochemicals, or stored poorly differs materially from grain grown cleanly and handled
simply; **washing with pure or nearly-pure water removes surface impurities so cooking
proceeds on a clean substrate. Washing is part of saṃskāra.**"*

**Evidence.** Neither report measures rinsing. What is measured is **cooking-water
volume**, and the result is large. *rice-and-wheat.md* §10, Raab A, et al., *PLOS One*
2015;10(7):e0131608 **[E2]**: percolating near-boiling water removes **49 ± 7%** of
inorganic arsenic across wholegrain and polished rice; excess-water cooking at **12:1
removes 57 ± 5%** on average, up to ~70% — *"but also leaches enriched vitamins and some
minerals."* Menon M, et al., *Environ Sci Technol* 2019 **[E2]**: modified parboiling of
husked wholegrain cut inorganic arsenic in final polished grain by **~25%** in
village-scale trials in rural Bangladesh.

**Verdict: UNSUPPORTED as stated** (rinsing is not the measured variable), and undercut
by its own logic: the book's prescribed preparation is *absorbed-water* porridge, which
retains the cooking water and therefore retains the leachable fraction that 12:1 cooking
removes. The contaminant the measurements are about is not named anywhere in the book
(gap G17).

**Load-bearing: low as a claim, high as a missed lever.** One clause; nothing rests on
it. But it is the book's only stated purity mechanism for grain, and the reports supply
a far better-quantified one that points at a different preparation.

## U5 — "peya-yavāgū-ādiḥ śreṣṭhaḥ āhāraḥ" credited to Suśruta as independent affirmation

**Book claim,** `diet/Yogic_Food.md:39–44`: *"The **Suśruta Saṃhitā** independently
affirms the same baseline:*

> ***peya-yavāgū-ādiḥ śreṣṭhaḥ āhāraḥ.***
>
> *"Peya, yavāgu, and similar preparations are the best nourishment."\
> — proverbial formulation, after* Suśruta Saṃhitā *Sūtrasthāna 46"*

**Evidence.** *canon-and-minor-grains.md* §1.1, source-standing table: Suśruta Sū. 45–46
was reached in that pass only via *"Bhiṣagratna-derived English digests (**secondary**).
**Verse numbers unstable:** two independent digests of Sū. 46 place *yava* at 46.40–42
and at 46.41–42, and *godhūma* at 46.43 and 46.43–44. **Cite the Suśruta grain verses as
'Sū. 46, barley/wheat section' until checked against a Sanskrit edition with Dalhaṇa.**"*
No such sentence appears anywhere in the report's Suśruta material.

**Verdict: UNSUPPORTED.** Not contradicted — the report simply never reached Suśruta
Sū. 46 in Sanskrit. But the word doing the work in the book's sentence is
***independently***, and the independence is exactly what is unestablished.

**Load-bearing: moderate.** It is the second leg of a two-corpora argument in
`Yogic_Food.md`. If it goes, the vilepī doctrine rests on Caraka alone — and on a Caraka
citation the book itself flags as unverified (U6).

## U6 — "yavāgūḥ sarva-rogeṣu pathyā"

**Book claim.** `diet/Yogic_Food.md:32–35`: *"**yavāgūḥ sarva-rogeṣu pathyā.** / 'Grain
gruel is wholesome in all conditions.' / — proverbial formulation, after* Caraka Saṃhitā
*Cikitsāsthāna (Rasāyana-pāda)"*. Same verse at `diet/Ambrosian_Diet.md:39–42`,
`source-extracts/Cooking_and_Agni.md:203`.

**Evidence.** The verse appears nowhere in *canon-and-minor-grains.md*, whose Caraka
coverage is §1.3 (27.8–22), §1.4 (25.38–40, 27.4, 27.305, 27.309–310, 27.339, the
kṛtānna barley section, 5.12) and §1.6 (25.39 / 27.12). The report reached
Cikitsāsthāna material not at all.

**Verdict: UNSUPPORTED.** Note the book already knows this in one place and not another:
`Ambrosian_Diet.md:42` carries the flag *"no numbered verse verified in the current
source trail"*; `Yogic_Food.md:35` and `Cooking_and_Agni.md:203` carry no such flag for
the same verse.

**Load-bearing: moderate.** It is the strongest single sentence in the book's grain case
— an unrestricted therapeutic endorsement of grain gruel — and it is the one carrying no
verse number.

## U7 — "Germination does not lighten the grain"

**Book claim.** `source-extracts/Raw_Vegan_Staples_Warnings.md:39`: *"**Germination does
not lighten the grain**; the text files it among the *guru* preparations."* Restated at
`diet/Yogis_Dont_Eat_Fruit.md:117` (*"for germination does not lighten the seed"*) and
`diet/Vegan.md:85`. Cited to Caraka Sū. 27.265–267.

**Evidence.** Germination measurably changes the grain, in the direction of removing an
absorption inhibitor and creating a compound absent before:

- *rice-and-wheat.md* §6 **[E1 for the chemistry]**: brown-rice germination activates
  glutamate decarboxylase; GABA rises ~**330% at 36 h**; Njavara at 72 h soak+germinate,
  **28.63 → 130.29 mg/kg** (≈4.5-fold). Report: *"Germination genuinely creates a
  compound that is essentially absent from the ungerminated milled grain."*
- §11: *"Sprouting reliably reduces phytate (endogenous phytase activation)."*
  *canon-and-minor-grains.md* §2.9, Makokha 2002 **[delegated]**: malting reduced
  phytate **−23.9% / −45.3%** in Kenyan sorghum and finger millet.

**But**: neither report measures *guru*/*laghu*, gastric emptying, or digestibility of
sprouted grain, and §11 is explicit about the limit of what is known — for ATIs,
*"there is essentially no published measurement — this is a genuine gap, not a settled
negative. **Do not repeat the claim that sprouting reduces ATIs; it is untested.**"*

**Verdict: UNSUPPORTED** as a biochemical claim. The book's narrow textual claim (that
Caraka files germinated grain among the *guru* preparations) is not contradicted — but
neither is it corroborated, since Sū. 27.265–267 is outside the canon report's coverage
(gap G7).

**Load-bearing: low.** It is one rebuttal in a list of rebuttals to the raw-vegan plate,
in a file whose other items (raw nuts *guru*, raw legume strength-reducing) are
independent. Nothing collapses.

# 3. CONFIRMED

## K1 — Caraka Sū. 27.4, the four grain exceptions

`source-extracts/Fruit_as_Medicine.md:57` quotes: *"Sweet is mostly *kapha*-aggravating
except honey / and old *śāli*, *ṣaṣṭika* (rice), barley and wheat."*

*canon-and-minor-grains.md* §1.4: *"**Sū. 27.4** — the rule 'sweet taste is mostly
kapha-aggravating' is given **four grain exceptions plus honey**: *old śāli*, *ṣaṣṭika*,
*barley*, *wheat*. These four are the only sweet grains the text exempts from its own
kapha rule."* **CONFIRMED** — verse number, item list and count all match.

## K2 — Caraka Sū. 25.38, rakta-śāli best of the awned grains

`source-extracts/Fruit_as_Medicine.md` (Sū. 25.38 block): *"Red *śāli* rice is the best
wholesome among the awned cereals, green gram among the legumes…"*

Canon §1.4: *"**Sū. 25.38** — *rakta-śāli* is the single most wholesome (*pathyatama*)
substance among the *śūkadhānya*; *mudga* (green gram) is best among legumes."*
**CONFIRMED.**

## K3 — Caraka Sū. 25.39, yavaka worst of the awned grains

`source-extracts/Fruit_as_Medicine.md` (Sū. 25.39 block): *"*Yavaka* is the most
unwholesome among the awned cereals, black gram among the legumes…"*

Canon §1.4: *"**Sū. 25.39** — ***yavaka* is the single most unwholesome (*apathyatama*)
among the *śūkadhānya***; *māṣa* (black gram) worst among legumes."* **CONFIRMED** — with
the referent complication recorded in §6/A4 below.

## K4 — Caraka Sū. 27.339, vrīhi → lājā

`source-extracts/Cooking_and_Agni.md:143–150` and `diet/In_Praise_of_Agni.md:78–79`:
*"Such as *vrīhi* (heavy) becomes light when transformed into *lājā* after frying."*

Canon §1.4: *"**Sū. 27.339** — processing overrides intrinsic quality: *vrīhi*, heavy,
becomes light when parched into *lājā*."* **CONFIRMED** — verse number and content.

## K5 — "Modern wheat has more gluten" is not established (the *Wheat Belly* critique)

`diet/Fear_of_Grains.md:13`: *"Later popular works, including *Wheat Belly* by **William
Davis**, completed the rhetorical shift from 'carbohydrates' to 'gluten,' without adding
experimental rigor. The same foods were removed. The same improvements were reported.
**The causal agent was reassigned, not demonstrated.**"*

*rice-and-wheat.md* Part IV.1, **[E1]**: *"'Modern wheat has been bred to be much higher
in gluten than old wheat.' **False.** Gluten content is flat over 120 years; protein has
fallen slightly; ancient wheats measure *higher* in protein and gliadin."* **CONFIRMED**,
and much more than confirmed — see S1.

## K6 — The canon forbids no grain

Implicit throughout `diet/Fear_of_Grains.md` and explicit at
`diet/Yogis_Dont_Eat_Fruit.md:11` (the HYP apathya list is given as tastes, greens, sour
gruel, alcohol, fish, flesh, curds, reheated food).

*canon-and-minor-grains.md* §1.9, verbatim: *"HYP 1.59–60 (apathya) forbids, among
others, sour, bitter, pungent, salty and heating things … **No grain is forbidden.** The
apathya list operates on tastes, oils, ferments and flesh, not on cereals."* **CONFIRMED.**

## K7 — Provenance and storage change the grain materially

`diet/Grains.md:3`: *"Grain grown in degraded soil, treated with modern agrochemicals, or
stored poorly **differs materially** from grain grown cleanly and handled simply."*

*canon-and-minor-grains.md* §2.2b, environment: *"Direction is consistent across at least
five independent studies: **water deficit and warm, dry grain filling raise grain
β-glucan; irrigation and wet, cool grain filling lower it**"*; Anker-Nilssen K et al.,
*J Cereal Sci* 2008;48(3):670–7 — under controlled growth temperature, *"water-soluble
β-glucan, its viscosity AND its molecular weight all increased with rising growth
temperature."* Storage: *rice-and-wheat.md* §5 **[E2]** — over 3–12 months, free fatty
acids rise, amylose–lipid V-type inclusion complexes form, pasting temperature and
hardness rise.

**CONFIRMED** in the specific sense that growing conditions and storage measurably change
grain composition and function. **UNKNOWN**: the book's implied *direction* (degraded
soil → worse grain) is not what these studies measured; they measured temperature, water
availability and storage time, and the β-glucan direction is *drier growing = more*.

# 4. STRENGTHENABLE

Places where the evidence supports the book more strongly, or more precisely, than the
book currently argues.

## S1 — The *Wheat Belly* premise is refutable by direct measurement, not just by rigour-critique

The book (`Fear_of_Grains.md:13`) charges Davis only with "not adding experimental
rigor." The reports refute the empirical premise outright, at **[E1]**:

- Geisslitz S, Longin CFH, Scherf KA, Koehler P, *Foods* 2019;8(9):409 — **15 cultivars
  per species (75 total), 4 German locations, 297 samples**: common wheat gluten
  80.4 mg/g vs spelt up to 111.6; gliadin:glutenin ratio common wheat **2.5**, einkorn
  **6.5 (range 3.7–12.1)**. *"**Ancient wheats had HIGHER protein and gliadin than modern
  common wheat.**"*
- Kasarda DD, *J Agric Food Chem* 2013;61(6):1155–1159 — *"**No evidence of any trend
  toward higher protein content** in US spring or winter wheats since the early 20th
  century."* Kasarda attributes rising celiac incidence to increased total wheat-flour
  and **vital wheat gluten** consumption, not to breeding.
- Pronin D, Börner A, Weber H, Scherf KA, *J Agric Food Chem* 2020 — **120 years** of
  German cultivars grown together: modern varieties **slightly less protein**, **gluten
  content constant**, composition shifted **toward glutenin** (away from the gliadin
  fraction carrying most CD epitopes).
- Brouns F, et al., *Nutr Bull* 2022;47(2):157–167 — ancient wheats contain *"**greater
  contents of many CD-active epitopes**"*; explicit conclusion *"no single wheat type can
  be recommended as better or safer for reducing or mitigating CD."*

The book has an E1 refutation of its opponent's core factual claim available and uses
none of it.

## S2 — The lectin fear has a measured dose gap and a named provenance trail

`Fear_of_Grains.md:3,19` asserts that the fear "persists by repetition." *rice-and-wheat.md*
§II.5 demonstrates it, with numbers and named sources **[E4 for the harm claim, i.e. the
harm claim fails]**:

- WGA content: wheat germ 0.1–0.5 g/kg; whole wheat flour 5.70–50 µg/g; **cooked pasta
  ~0.3 µg/g** (two orders of magnitude below flour).
- In vivo toxicity threshold: **7 g WGA/kg body weight over 10 days** — *"For a 70 kg
  human that would be ~490 g of pure WGA over ten days; at 50 µg/g whole wheat flour,
  that is nominally ~10,000 kg of flour."*
- *"**There are no data available on the mean dietary intake of WGA in humans.**"*
- Authors' conclusion: symptoms are *"extremely rare with normal intake of food prepared
  for human use."*
- Report's own provenance finding: *"**Every popular claim about WGA (joint attack,
  leptin-receptor blockade, systemic inflammation from ordinary bread) traces to
  wellness-media sources (Mercola, GreenMedInfo, goop, Shortform) rather than to primary
  human data.**"*

That last line is the book's thesis — "repetition without confirmation" — established
with a dose figure and a citation trail. The book never mentions lectins at all.

## S3 — The causal agent in non-celiac wheat sensitivity was in fact reassigned, and to a named alternative

`Fear_of_Grains.md:13` says only that "the causal agent was reassigned, not
demonstrated." *rice-and-wheat.md* §II.6–7 supplies both halves:

- Skodje 2018 **[E1 for "fructans contribute", E2 for "fructans rather than gluten
  dominate"]**: DBPC crossover, **n = 59**, gluten 5.7 g / fructan 2.1 g / placebo;
  GSRS-IBS gluten 33.1 ± 13.3, **fructan 38.6 ± 12.3**, placebo 34.3 ± 13.9, **P = 0.04**;
  bloating highest on fructan **P = 0.003**. Report's honest note: *"gluten scored
  *below* placebo."*
- Biesiekierski 2013: the originating group's own follow-up — gluten at **16 g/day**
  indistinguishable from placebo once FODMAPs were controlled.
- Molina-Infante & Carroccio 2017: across pooled DBPC challenges *"only a small minority
  showed gluten-specific reproducible symptoms; a large fraction responded to placebo."*
- Capannolo 2015 (via Brouns 2022): **392 IBS patients** self-reporting gluten
  sensitivity — **6.63%** celiac, **0.51%** wheat allergy, and after 6 months gluten-free
  and reintroduction **85.96% showed no specific reaction to gluten.**
- Report's tiering: *"Nocebo/expectancy is a large, measured component: **[E1]**."*

Against this the book should also carry the report's counterweight, stated at its own
tier: *"That *some* non-celiac individuals have reproducible wheat-triggered symptoms:
**[E2]**."*

## S4 — Whole-grain and gluten intake track *better* outcomes in the large cohorts

`Fear_of_Grains.md` and `Grains.md` defend grain on classical and epistemological
grounds only. Available at **[E1/E2]**:

- Lebwohl 2017 *BMJ* **[E2 observational]** — ~110,000 participants, celiac excluded:
  after adjustment for refined grain, **HR 0.85 (0.77–0.93)** for higher gluten intake;
  authors: *"the promotion of gluten-free diets among people without celiac disease
  should not be encouraged."*
- Brouns F, *Nutrients* 2021;14(1):25 **[E1 for the conclusion in mixed diets]** — *"In
  mixed Western diets, higher whole-grain intake is associated with **better** health
  outcomes despite phytate … **reduced in vitro phytate does not reliably translate into
  improved mineral status in humans** … advice to avoid whole grains on phytate grounds
  is unjustified."*

**Counterweight the book would have to carry with it,** from *canon-and-minor-grains.md*
§2.9: the 20–25% mortality reduction popularly attributed to whole grains is *"**entirely
observational**"* (Aune 2016, 45 cohorts, **I² = 83%**), and Kelly SA, et al., *Cochrane*
2017;8:CD005051 found across **nine RCTs and 1,414 participants** *"**no studies that
reported the effect of whole grain diets on total cardiovascular mortality or
cardiovascular events**"*, evidence quality **low**.

## S5 — The HYP grain list is four grains, and it is a *strict subset* of Caraka's praised grains

The book gives three: `diet/Yogis_Dont_Eat_Fruit.md:11` — *"wheat, rice, barley, milk,
ghee, raw sugar, butter, honey, dry ginger, and mung *dāl*"*; `diet/Ambrosian_Diet.md:51`
— *"good grains, wheat, rice, barley, milk, ghee, brown sugar…"*. Both drop **ṣāṣṭika**.

*canon-and-minor-grains.md* §1.9 supplies **verified Devanagari + IAST** for HYP 1.62–63
(= 1.65 in the Brahmānanda numbering):

> *godhūma-śāli-yava-ṣāṣṭika-śobhanānnaṃ kṣīrājya-khaṇḍa-navanīta-siddhā-madhūni |*

and the observation the book does not make: *"the yogic list is *four grains*, in that
fixed compound order, and it is a **strict subset of Caraka's praised grains**: śāli,
ṣaṣṭika, yava, godhūma are precisely the four that Caraka Sū. 27.4 exempts from the
sweet-taste kapha rule (with 'old śāli'), and *mudga* is Caraka's *pathyatama* legume
(Sū. 25.38)."*

That is a four-for-four set identity plus the legume — considerably stronger than the
book's *"The two corpora converge on the same staple at the same word"*
(`Yogis_Dont_Eat_Fruit.md:57`). The dropped grain, *ṣaṣṭika*, is one of only two Caraka
calls ***tridoṣaghna*** (§1.3, 27.13).

## S6 — The canonical grain roster is nameable, and the millet silence is a positive finding

`canon-and-minor-grains.md` §1.10: *"**Praised, unambiguously, across Āyurveda and the
yogic manuals:** *rakta-śāli* (best of all awned grains, Caraka), *ṣaṣṭika* (tridoṣaghna
and light), *yava* (barley), *godhūma* (wheat), and — Caraka only — old śāli."*

And §1.9: *"**No millet appears in the HYP pathya list.** Not śyāmāka, not kodrava, not
priyaṅgu, not nīvāra. The entire Caraka millet block is simply absent — neither praised
nor forbidden."* Plus §1.2's observation about category drift: *"In the earliest layer
(Caraka) barley and wheat sit in the *same* category as rice and the millets … In the
latest layer surveyed (Bhāvaprakāśa) barley and wheat are the **only** members of the
'awned grain' category. **The category narrowed around them.**"*

The book asserts the roster loosely and could state it as a closed four-name list with
a documented narrowing over time.

## S7 — Preparation-as-constitutive has a best-quantified instance the book does not use

`Grains.md`'s thesis is that saṃskāra is constitutive of effect. The single
best-quantified instance in either report is arsenic removal by cooking-water method:
**49 ± 7%** by percolating near-boiling water, **57 ± 5%** (up to ~70%) by 12:1
excess-water cooking (Raab 2015, **[E2]**), and **~25%** by modified parboiling of husked
wholegrain (Menon 2019, **[E2]**). Nothing else in either report shows a preparation
variable moving a health-relevant quantity by that margin.

The caveat is real and must travel with it: excess-water cooking *"also leaches enriched
vitamins and some minerals"*, and it is the opposite of absorbed-water porridge.

## S8 — Traditional processing has strong measured effects, though not the ones the book prescribes

*rice-and-wheat.md* §4 on parboiling **[E1]**: thiamine, niacin and B6 in the milled
endosperm rise **roughly three-fold** *"because water-soluble vitamins migrate inward
from the bran/aleurone during soaking and steaming and are then fixed by
gelatinisation — a genuine nutrient-rescue mechanism unique to hydrothermally processed
cereals in the husk."* §11: sourdough acidification activates endogenous cereal phytase
with *"reductions of up to ~90% of phytate"* **[E2]**, and *"Wheat's own phytase makes
this work — the same reason rice does not respond well to soaking."*

That last clause is directly relevant to the book, which prescribes washing and soaking
of rice: rice is among the low-phytase cereals (§11, *"Rye has the highest cereal phytase
activity, followed by wheat and barley; oats, maize and rice are low"* — **[E2 for the
ranking; the popular "14×" figure is E4 and traced to advocacy sources]**).

# 5. Book claims neither report covers

Listed so the gap is visible rather than silently absent. "Not covered" means the reports
do not bear on it — not that it is wrong.

## Preparation and practice

- **G1.** Vilepī / peyā / yavāgū as a preparation. No study in either report measures a
  slow-cooked wet grain porridge on any human endpoint.
  (`Grains.md:5,32`; `Yogic_Food.md:5,37`; `Ambrosian_Diet.md:148`;
  `Yogis_Dont_Eat_Fruit.md:129`)
- **G2.** Ghee-with-grain as a combination (*snigdha*). No data on fat-with-starch
  co-ingestion in either report. (`Grains.md:5`; `Yogis_Dont_Eat_Fruit.md:22`)
- **G3.** All *guṇa* vocabulary — *rasa*, *vīrya*, *vipāka*, *prabhāva*, *ojas*, *agni*,
  *āma*, sāttva/rajas/tamas. Both reports are explicitly bracketed from this; the canon
  report's preamble states *"Part 1 is not evidence for Part 2 and Part 2 is not a
  validation of Part 1."* (`Protein.md:29`; `Penultimate_Sāttvic_Food.md` throughout)
- **G4.** *Saṃyoga* / *viruddhāhāra* (incompatible combination) as a mechanism.
  (`Grains.md:12–15`)
- **G5.** Sodium chloride as the confounder in grain trials — the book's central
  alternative hypothesis. Neither report examined salt in any grain study.
  (`Fear_of_Grains.md:11,15`)
- **G6.** Hydration state as a confounder. Same. (`Fear_of_Grains.md:5,9,15`)

## Sanskrit passages outside the canon report's coverage

The canon report's Caraka coverage is Sū. 5.12, 25.38–40, 27.4–22, 27.305, 27.309–310,
27.339, and the kṛtānna barley section. Everything else the book cites is uncorroborated
here:

- **G7.** Caraka Sū. 27.257–259 (odana well-cooked light / poorly cooked heavy) —
  `Cooking_and_Agni.md:161–169`, `In_Praise_of_Agni.md:81–87`.
  Caraka Sū. 27.265–267 (germinated grain *guru*) — `Raw_Vegan_Staples_Warnings.md:36`.
  Caraka Sū. 27.275, Sū. 27.349–350, Vimānasthāna 1, Sū. 26 (viruddhāhāra) — all
  uncovered.
- **G8.** Suśruta Sū. 46 in Sanskrit. Canon §1.1: secondary digests only, verse numbers
  unstable. (`Yogic_Food.md:44`; `Cooking_and_Agni.md:332`)
- **G9.** Aṣṭāṅga Hṛdaya Sū. 6 in Sanskrit. Canon §1.1: *"Secondary English digest only
  — **Sanskrit not verified in this pass**."* Also AH Sū. 8 (`Grains.md:20`), Śā. 3.54
  (`Fruitarianism.md:48`), Sū. 10.34cd (`source-extracts/Apathya.md:361`).
- **G10.** Gheraṇḍa Saṃhitā Sanskrit. Canon §1.1 and §1.9: *"**Sanskrit not obtained**."*
- **G11.** Yoga Yājñavalkya 1.66–67, the mouthful counts. In neither report.
  (`Yogic_Food.md:57`; `Yogis_Dont_Eat_Fruit.md:140`; `Ambrosian_Diet.md:175`)
- **G12.** Taittirīya Upaniṣad 2.2.1 and 3.2 (*annāt puruṣaḥ*, *annaṃ brahma*). In
  neither report. This is the metaphysical foundation of `Yogic_Food.md`,
  `Ambrosian_Diet.md` and `Yogis_Dont_Eat_Fruit.md`.
- **G13.** Atharvaveda 6.142 and the whole of
  `source-extracts/Atharva_Veda/barley-and-grain.md`, including its load-bearing claim
  that *"the Veda blesses grain (with milk, ghee, and Soma) as the staple; no fruit
  receives a comparable hymn"* (`:29`). The canon report's earliest layer is Caraka; it
  reaches no Vedic saṃhitā.
- **G14.** Buddhist Vinaya *odana* / *yāgu* and the Mahāsaccaka Sutta rice-gruel episode
  (`Yogic_Food.md:63`).
- **G15.** Huang Di Nei Jing Suwen — the five grains (`Raw_and_Cooked_Cross_Tradition.md:97`)
  and the rice-gruel-as-medicine passage (`:107`).
- **G16.** Hippocrates *On Ancient Medicine* and Galen on wheat
  (`Raw_and_Cooked_Cross_Tradition.md:16–57`).
- **G16b.** Śiva Saṃhitā. The book does not cite it for diet; the canon report flags it
  as **"Not verified"** (§1.9). Clean, and noted so the absence is deliberate.

## Modern material the reports cover and the book does not mention at all

These are gaps in the other direction — the reports carry them, the book is silent.
Listed because silence on them is itself a finding about a book that prescribes grain as
a universal daily floor.

- **G17.** **Arsenic and cadmium in rice.** *rice-and-wheat.md* §10 calls this *"the
  single most consequential piece of rice biology for human health, and it is unusually
  well resolved mechanistically"* **[E1]**: at paddy redox potential arsenate is reduced
  to arsenite As(OH)₃, *"a near-perfect structural mimic of silicic acid, Si(OH)₄"*, which
  the silicon transporters Lsi1/Lsi2 then carry into the grain (Ma JF, et al., *PNAS*
  2008;105(29):9931–9935); *lsi2* mutants show greatly decreased xylem transport and
  grain accumulation. FDA action level for inorganic arsenic in **infant rice cereal:
  100 ppb**. Rice-borne cadmium caused **itai-itai disease** in the Jinzu River basin.
  The report's own framing, carried in full: *"It is **not** a reason to avoid rice in a
  mixed diet; it is a reason not to base an infant's diet on rice products."* The book
  prescribes rice porridge as the daily floor for everyone, including the depleted and
  the ill, and never mentions this.
- **G18.** The entire modern vocabulary: β-glucan, phytate, phytase, lectins, resistant
  starch, glycaemic index, DIAAS, celiac disease, FODMAPs, ATIs. Zero occurrences in the
  book.
- **G19.** **Millet-specific hazards.** *canon-and-minor-grains.md* §2.8: kodo millet
  poisoning from fungal **cyclopiazonic acid**, a specific SERCA inhibitor at
  **IC₅₀ ≈ 0.6 µM** (Seidler 1989), mouse oral LD50 **64 ± 4.4 mg/kg** — *"**no published
  contamination survey, no regulatory CPA limit for kodo, and no surveillance
  programme**"* — and pearl millet C-glycosylflavone goitrogens inhibiting thyroid
  peroxidase (Gaitan 1989/1995). Report verdict: *"ESTABLISHED as a phenomenon with a
  coherent molecular mechanism, THIN as a literature, and unmonitored."* The book
  recommends millet at `Fruitarianism.md:56` without qualification. The report itself
  insists on the separation the book would have to respect: *"Part 1 records that Caraka
  ranks *kodrava* the best *rūkṣaṇa* food and says nothing about poisoning. The two are
  not describing the same thing and must not be merged."*
- **G20.** **Oats.** Recommended at `Fruitarianism.md:56`. Canon: silent (§1.5). Modern:
  Abelilla JJ, Liu Y, Stein HH, *J Sci Food Agric* 2018;98(1):410–4 — pig standardised
  ileal digestibility, DIAAS **41 / 56 / 67** for infants, 6 mo–3 y, and >3 y; FAO
  thresholds are ≥100 "excellent" and ≥75 "good source" — *"**Oat clears neither.**"*
  Report verdict: *"'oat is a complete protein' is FALSE by the standard scoring
  method."*
- **G21.** **Buckwheat.** Recommended at `diet/Interrupting_Fasts.md:31` (*"take a small
  amount of simple, living food: rice, buckwheat, or another gentle staple"*). Canon
  §1.5 lists buckwheat among the grains *"conspicuously absent from every list."* The
  modern report does not cover buckwheat either. **Double gap.**

# 6. Sanskrit attributions the canon report finds disputed, misfiled, or belonging elsewhere

## Flagged

**A1 — *anna-varga* attributed to Caraka Sū. 27.** `diet/Yogic_Food.md:25–28`. Caraka's
first varga is *śūkadhānya*, not *anna-varga* (canon §1.2, Sū. 27.5). The book quotes
the correct varga name elsewhere (`Fruit_as_Medicine.md:69`). **Misattributed category
name.** See C5.

**A2 — *vrīhi* used as the exemplar of the praised staple.** Same lines. Caraka 27.15
makes *vrīhi* **amla in vipāka**, *pittakara*, *guru*, with *pāṭala* tridoṣa-deranging;
canon §1.10 files it under "Restricted or downgraded." Suśruta additionally places it in
a different varga from Caraka (§1.7.6). **Wrong grain for the doctrine it carries.**

**A3 — *dhānya* in Caraka Sū. 5.12 translated as "rain water" and counted as a grain.**
`Fruit_as_Medicine.md:280–282` + `:285`; `Cooking_and_Agni.md:192–194` + `:197`;
`source-extracts/Apathya.md:369–371`; count reused at
`Raw_and_Cooked_Cross_Tradition.md:103,197`. Canon §1.4: *"**dhānyaṃ* rendered 'rain
water' by two translators **without warrant**."* **Disputed reading, used in both senses
within the same paragraph.** See C4.

**A4 — *mudga* counted among "five grains".** Same lines. *Mudga* is Caraka's
*śamīdhānya* (legume) varga — the second of the twelve, not the first (canon §1.2) — and
Sū. 25.38 names it best **among legumes** (§1.4). The book's own
`ayurveda/Apathya.md:289` classifies it correctly as a pulse, so the misfiling is
confined to the source-extracts. **Misfiled category.**

**A5 — "peya-yavāgū-ādiḥ śreṣṭhaḥ āhāraḥ" credited to Suśruta Sū. 46 as an independent
affirmation.** `Yogic_Food.md:39–44`. Canon §1.1 reached Suśruta Sū. 45–46 only through
Bhiṣagratna-derived secondary digests with **unstable verse numbers**, and instructs:
*"Cite the Suśruta grain verses as 'Sū. 46, barley/wheat section' until checked against a
Sanskrit edition with Dalhaṇa."* **Unverified attribution presented as independent
corroboration.** See U5.

**A6 — *yavaka*: ranking confirmed, referent unresolved.** `Fruit_as_Medicine.md` quotes
Sū. 25.39 without noting the dispute. Canon §1.6 records *"the single sharpest internal
contradiction in Caraka's grain material"*: Sū. 27.12 files *yavaka* among the inferior
*śālis* said to *"imitate the śālis in merits and demerits"*, while Sū. 25.39 makes it
the worst substance in the whole class. **Cakrapāṇidatta and Gaṅgādhara** hold it is
*trimalakara* with qualities *opposite* to rakta-śāli, reading *guṇāguṇaiḥ* as
*guṇa-viparīta-doṣa*; **Yogendranāth Sen** takes the plain reading that it has the *same*
guṇas as śāli. Some botanical indices assign it *Hordeum vulgare*; elsewhere in Caraka
*yāvaka* is a barley *preparation*. Report's instruction: *"Anyone building on Caraka's
grain rankings has to decide this and should say that they are deciding it."*
**Unresolved referent, used as though settled.**

## Checked and clean

Recorded so the checking is visible.

**A7 — *veṇuyava*.** Canon §1.5 flags *"Mistaking veṇuyava for a barley variety is a real
and recurring modern error"* — it is bamboo seed, *Bambusa arundinacea*. The book never
uses the term. **Clean.**

**A8 — *rakta-śāli* equated with a marketed red rice.** Canon §1.5: *"the modern practice
of equating it with any specific marketed red rice is unwarranted."* The book quotes the
Sū. 25.38 verse and makes no such equation. **Clean.**

**A9 — *nīvāra* rendered as "wild rice" with *Zizania* data attached.** Canon §1.5 calls
this *"the most consequential identification dispute in the list"* and §2.8 adds that
*"Zizania has no native Indian distribution, so Vedic and Āyurvedic *nīvāra* cannot refer
to it."* The book never uses *nīvāra*. **Clean.**

**A10 — barley as "the Āyurvedic fat-scraper."** Canon §1.7.5: *"The popular 'barley is
the Āyurvedic fat-scraper' claim rests on Suśruta and Bhāvaprakāśa, **not** on Caraka"* —
Caraka's fat-reducing superlatives go to *gavedhukā* (karśanīya) and *kodrava* (rūkṣaṇa)
at Sū. 25.40. The book makes no barley-lekhana claim. **Clean.**

**A11 — HYP 1.59–60 item list.** The book's rendering (via `source-extracts/Apathya.md:113`,
`Cooking_and_Agni.md:269`, `research_yoga_ayurveda_lineage/06_structural_parallels.md:434`)
includes *"horse-gram, jujube"*; the canon report's §1.9 rendering includes *piper
longum* and does not list jujube, but says *"among others"* and is itself from a
secondary review. **Neither is from verified Sanskrit for 1.59–60. Recorded as a
divergence between two secondary renderings, not scored as a misattribution.**

# 7. Reading notes on tier discipline

Three places where a collision could have been reported harder than the evidence allows,
and was not:

1. **C7 (Madhumeha).** The white-rice/T2D association is **[E2 observational]** with the
   report's own warning that residual confounding is *"a live concern"* and the mechanism
   is *"a hypothesis."* The collision is scored on the canonical limb, where it is clean.
2. **C8 (Gheraṇḍa vs HYP).** The report's Gheraṇḍa material has **Sanskrit not obtained**
   and the contradiction is flagged by the report as *"translation-dependent and not
   resolved here."* Scored as CONTRADICTED at that weak tier, with the caveat stated in
   place.
3. **C6 (millet GI).** Malavika 2020 is **n = 12** by standard international GI
   methodology; the competing pooled figure (Anitha 2021, GI 52.7) comes from an
   ICRISAT-affiliated millet-promotion programme. The report's verdict is *"WEAK, and the
   headline number is contradicted by direct measurement"* — the collision is reported as
   a direct-measurement contradiction of a pooled advocacy estimate, not as settled fact
   about millet glycaemia.

And one place a collision was **not** manufactured: `diet/Fear_of_Grains.md:15`'s
specific negative — that no controlled trial has tested grain *"slowly cooked in ample
water, without chloride of sodium, without spices, without industrial processing—while
holding other variables constant"* — is **true against both reports**. Neither identifies
such a trial. It is recorded as surviving, under C1.
