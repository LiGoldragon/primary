# The Book of Sol — Full Audit: Style, Consistency, Citations, Organization

Role: poet. Date: 2026-06-19. Subject repo: `/git/github.com/LiGoldragon/TheBookOfSol` (150 markdown files).

## Method

Two layers. A deterministic layer the orchestrator ran directly (horizontal rules, curly quotes, the `sodium`/`chloride of sodium` lexicon, internal-link resolution, `_index.md` orphans, Substack-state consistency, Unicode artefacts, numbering gaps) — these are certain, not inferred. Then a judgment layer: a background workflow of **34 agents** across 17 bundles (one per category cluster plus three cross-cutting passes — organization, doctrinal consistency, Sanskrit-citation accuracy), each finding adversarially verified by an independent skeptic agent before it survived. Every rule traces to the repo's own `AGENTS.md`. Workflow cost: ~3.5M tokens, 648 tool calls, 16 minutes.

## Headline

**309 distinct findings** after de-duplication (43 high · 140 medium · 126 low). They concentrate hard: three categories — negative-contrast **tics** (73), **citation-errors** (49), and **quote-format** breaks (42) — account for over half. The doctrine is consistent (salt position holds; the B-12 purge is complete; the cooked-first/raw-exceptions principle is stated compatibly everywhere). The work ahead is finishing, not rebuilding.

### Most urgent: high-severity issues on LIVE Substack pages (8)

These are shipped to readers right now.

| File (post) | Category | Problem | Fix |
|---|---|---|---|
| `chloride/The_Chloride_Indictment.md` | tic | The PUBLISHED anchor article runs the banned 'X is not Y. It is Z.' construction at least a dozen times, maki… | Do a full negative-contrast pass: cut the 'not Y' setup and keep only the positive claim … |
| `chloride/The_Chloride_Indictment.md` | tic | The Verdict bullets are a sustained negative-contrast hammer (four consecutive 'not X / it is Y' bullets plus… | Rewrite each bullet as a direct positive claim: 'Chloride irritates a living system that … |
| `chloride/The_Chloride_Indictment.md` | sodium-naming | This standalone 'sodium' (meaning total chloride-of-sodium intake) is in Section VII, outside the sanctioned … | Replace with 'chloride': '...whose entire daily chloride is under a single grain of salt.' |
| `diet/Ambrosian_Diet.md` | citation-error | The identical sūtra (kaṇṭhakūpe kṣutpipāsānivṛttiḥ) is cited as 3.30 in the PUBLISHED Ambrosian Diet and as 3… | Fix both to the standard Vyāsa numbering (Yoga Sūtra 3.30) and unify the title form (`Yog… |
| `diet/Ambrosian_Diet.md` | citation-error | The hunger-and-thirst-cessation aphorism (kaṇṭhakūpe kṣutpipāsānivṛttiḥ) is Yoga Sūtra 3.31, not 3.30; YS 3.3… | Change "*Pātañjalayoga-sūtra* 3.30" to "*Pātañjala Yoga-sūtra* 3.31" to match the correct… |
| `diet/Ambrosian_Diet.md` | citation-error | "annaṃ brahmeti vyajānāt" is Bhṛgu's first realization in the Bhṛgu Vallī (third vallī), Taittirīya Upaniṣad … | Cite as *Taittirīya Upaniṣad* 3.2 (Bhṛgu Vallī) and drop the framing that makes it the sa… |
| `water/The_Distilled_Water_Paradox.md` | citation-error | All five Sanskrit verses are presented as verbatim primary-source quotation (bold, quoted, attributed to *Car… | Either ground each verse against a verified note in /git/github.com/LiGoldragon/caraka-sa… |
| `water/The_Distilled_Water_Paradox.md` | quote-format | Every quote block inverts the house format on a published article: the Sanskrit is wrapped in straight quotes… | Reformat each to the canonical shape: bold un-quoted IAST line(s) with `\`, a blank `>` l… |

## At a glance

### By category

| Category | Count |
|---|---|
| tic | 73 |
| citation-error | 49 |
| quote-format | 42 |
| organization | 20 |
| gloss-missing | 15 |
| meta-prose | 14 |
| em-dash-density | 13 |
| doctrine-contradiction | 10 |
| other | 10 |
| redundancy | 10 |
| factual-error | 9 |
| stub-quality | 8 |
| weak-closing | 7 |
| sodium-naming | 6 |
| filler | 5 |
| micronutrition | 4 |
| index-gap | 4 |
| structural-mirror | 4 |
| broken-link | 3 |
| earth-as-planet | 2 |
| symbology-inversion | 1 |

### Worst-offending files (top 20)

| File | Findings |
|---|---|
| `diet/Ambrosian_Diet.md` | 12 |
| `cosmology/All_Instruments_Measure_a_Level_Earth.md` | 8 |
| `ghee/Ethical_Ghee.md` | 6 |
| `ayurveda/Āyurveda.md` | 5 |
| `chloride/The_Chloride_Indictment.md` | 5 |
| `diet/Penultimate_Sāttvic_Food.md` | 5 |
| `personal/The_Pressure_of_Being.md` | 5 |
| `sol-luna/Kali_Yuga.md` | 5 |
| `source-extracts/Salt_Dosage_and_Conditions.md` | 5 |
| `water/The_Distilled_Water_Paradox.md` | 5 |
| `yoga-tantra/Vajrolī.md` | 5 |
| `diet/Yogic_Food.md` | 4 |
| `ghee/Ghee_Restored_my_Vitality.md` | 4 |
| `ghee/Ghṛta_Golden_Magic.md` | 4 |
| `sol-luna/Celestial_Name.md` | 4 |
| `source-extracts/Apathya.md` | 4 |
| `source-extracts/Cooking_and_Agni.md` | 4 |
| `ayurveda/Apathya.md` | 4 |
| `ayurveda/The_Two_Pillars_of_Nourishment.md` | 4 |
| `chloride/Inorganic_Minerals.md` | 4 |

## High-severity findings — full detail

All 43, grouped by file.

### `chloride/The_Chloride_Indictment.md` **(PUBLISHED)**

- **[tic]** The PUBLISHED anchor article runs the banned 'X is not Y. It is Z.' construction at least a dozen times, making it the article's default rhythm — the exact rhetorical move AGENTS.md most wants gone, in the file AGENTS.md holds up as a reference voice.
  - Evidence: "The distinction is not grammatical. It is diagnostic." / "The vocabulary is not ornament. It is the minimum honesty..." / "What follows is not a new claim. It is an old claim..." / "...is not a reclassification." / "Th…
  - Locator: L23, L27, L19, L39, L75, L99, L103, L111, L125, L144, L154 (and bullets L133-136) · Rule: Rule 7 — negative-contrast 'X is not Y. It is Z.' is the single most important …
  - Fix: Do a full negative-contrast pass: cut the 'not Y' setup and keep only the positive claim (e.g. 'The distinction is diagnostic.'; 'The vocabulary is the minimum honesty required.'; 'What follows is an old claim finally assembled.'). Where the denied term carries information, fold it into a trailing concession used sparingly.
- **[tic]** The Verdict bullets are a sustained negative-contrast hammer (four consecutive 'not X / it is Y' bullets plus two 'does not merely'), the most concentrated instance of the banned pattern in the corpus, in a published article.
  - Evidence: "- Chloride is not an electrolyte of ordinary nutrition. It is an inorganic mineral..." / "- Chloride is not merely harmful at excess. It produces its harm at every dose..." / "- Chloride does not merely poison; it addi…
  - Locator: L133-136 (Section X bullet list) · Rule: Rule 7 — 'Not A. Not B. But C.' triple/quadruple-fragment hammer
  - Fix: Rewrite each bullet as a direct positive claim: 'Chloride irritates a living system that cannot use it.' / 'Chloride harms at every dose, with no floor below which benefit appears.' / 'Chloride poisons and addicts: its damage becomes the craving for the next dose.' / 'Chloride's universality is the strongest evidence of its narcotic character.'
- **[sodium-naming]** This standalone 'sodium' (meaning total chloride-of-sodium intake) is in Section VII, outside the sanctioned Section II linguistic-contrast exception, in a PUBLISHED article.
  - Evidence: "the Western plate sits roughly two orders of magnitude above the Yanomami, whose entire daily sodium is under a single grain of salt"
  - Locator: L101 — "whose entire daily sodium is under a single grain of salt" · Rule: Rule 3 — standalone 'sodium' for the compound/intake is forbidden outside Secti…
  - Fix: Replace with 'chloride': '...whose entire daily chloride is under a single grain of salt.'

### `diet/Ambrosian_Diet.md` **(PUBLISHED)**

- **[citation-error]** The identical sūtra (kaṇṭhakūpe kṣutpipāsānivṛttiḥ) is cited as 3.30 in the PUBLISHED Ambrosian Diet and as 3.31 in Fruitarianism; at least one is wrong and the cluster is internally inconsistent.
  - Evidence: Ambrosian: **"kaṇṭhakūpe kṣutpipāsānivṛttiḥ."** … — *Pātañjalayoga-sūtra* 3.30  \|  Fruitarianism: **kaṇṭhakūpe kṣutpipāsānivṛttiḥ** … — *Yoga Sūtra* 3.31
  - Locator: line 117, '> — *Pātañjalayoga-sūtra* 3.30' vs Fruitarianism.md line 36 '> — *Yoga Sūtra* 3.31' · Rule: Rule 2 / citation accuracy — the same verse must carry one correct, consistent …
  - Fix: Fix both to the standard Vyāsa numbering (Yoga Sūtra 3.30) and unify the title form (`Yoga Sūtra` vs `Pātañjalayoga-sūtra`) across the cluster.
- **[citation-error]** The hunger-and-thirst-cessation aphorism (kaṇṭhakūpe kṣutpipāsānivṛttiḥ) is Yoga Sūtra 3.31, not 3.30; YS 3.30 is the nābhicakra / body-composition sūtra. The project's own Fruitarianism.md cites the identical line correctly as 3.31, so this is also an internal inconsistency.
  - Evidence: > **"kaṇṭhakūpe kṣutpipāsānivṛttiḥ."**\ > When the throat-well is mastered, hunger and thirst cease.\ > — *Pātañjalayoga-sūtra* 3.30
  - Locator: L117 — "*Pātañjalayoga-sūtra* 3.30" · Rule: Bundle citation-accuracy; AGENTS.md quote-block attribution must be correct
  - Fix: Change "*Pātañjalayoga-sūtra* 3.30" to "*Pātañjala Yoga-sūtra* 3.31" to match the correct locus and the project's own Fruitarianism.md.
- **[citation-error]** "annaṃ brahmeti vyajānāt" is Bhṛgu's first realization in the Bhṛgu Vallī (third vallī), Taittirīya Upaniṣad 3.2 — not 2.2.4. The article also frames it as the conclusion of the same section as the 2.1/2.2 anna-puruṣa chain, but the two passages sit in different vallīs (Ānanda Vallī vs Bhṛgu Vallī). The project's own Cooking_and_Spices.md cites this line correctly as 3.2, so the corpus contradicts itself.
  - Evidence: > **"annaṁ brahma iti vyajānāt."**\ > He realized anna as Brahman.\ > — *Taittirīya Upaniṣad* 2.2.4
  - Locator: L29-31 — "annaṁ brahma iti vyajānāt" cited as *Taittirīya Upaniṣad* 2.2.4 · Rule: Bundle citation-accuracy (verify Taittirīya Upaniṣad 2.x)
  - Fix: Cite as *Taittirīya Upaniṣad* 3.2 (Bhṛgu Vallī) and drop the framing that makes it the same section's conclusion as 2.2.1.

### `water/The_Distilled_Water_Paradox.md` **(PUBLISHED)**

- **[citation-error]** All five Sanskrit verses are presented as verbatim primary-source quotation (bold, quoted, attributed to *Caraka Saṃhitā* and *Bṛhadāraṇyaka Upaniṣad*) yet none can be located in source-extracts/ or the dedicated caraka-samhita repo; the constructed strings (and the irregular grammar of 'jīvenā') read as composed Sanskrit, none carry a chapter.verse, and none are flagged as paraphrase.
  - Evidence: > **"mṛttikā-loha-bhakṣaṇaṃ tamaḥ-nimittam."** / Eating earth or metal arises from tamas.  ...  > **"yad bhūtam jāyate jīvenā."** / That which has passed through life becomes fit to sustain life.
  - Locator: lines 43-44, 52-53, 57-58, 94-95, 101-102 (five Sanskrit quote blocks) · Rule: AGENTS.md 'Primary-source quote blocks' + Bibliography Convention (Caraka cites…
  - Fix: Either ground each verse against a verified note in /git/github.com/LiGoldragon/caraka-samhita (notes/philology) with full chapter.verse, or re-mark them as paraphrase per the rule: '— proverbial formulation, after *Caraka Saṃhitā* ...'. Verify the Upaniṣad attribution for 'yad bhūtam jāyate jīvenā' separately.
- **[quote-format]** Every quote block inverts the house format on a published article: the Sanskrit is wrapped in straight quotes (quotes belong on the English), there is no blank `>` separator line between Sanskrit and English, the English translation is NOT quoted, and there is no em-dash attribution line at all — the source name floats in surrounding prose with no chapter.verse.
  - Evidence: > **"mṛttikā-bhakṣaṇam apāthyaṃ … rasānāṃ mārgān pidhāyati, vāyum uparuddhaṃ karoti."**\  > Clay-eating is unwholesome. It obstructs the pathways of the vital fluids and causes the obstruction of vāyu.
  - Locator: lines 43-44, 52-53, 57-58, 94-95, 101-102 · Rule: Rule 2 (Sanskrit bold → blank `>` line → English in double quotes with `\` brea…
  - Fix: Reformat each to the canonical shape: bold un-quoted IAST line(s) with `\`, a blank `>` line, then "English translation" in quotes with `\`, then `— *Caraka Saṃhitā* <sthāna>.<verse>` (or paraphrase attribution) on its own `\`-broken final line.

### `ayurveda/The_Allure_of_Vata.md`

- **[citation-error]** The identical svastha verse (samadoṣaḥ samāgniś ca samadhātumalakriyaḥ...) is attributed to two different home texts and verse numbers across the bundle — Suśruta Sū. 15.41 in one published-voice article, Caraka Sū. 15.48 in three others; at least one attribution is wrong and the corpus contradicts itself on a frequently-quoted verse.
  - Evidence: The_Allure_of_Vata: "— *Suśruta Saṃhitā*, Sūtrasthāna 15.41"  vs  Apathya/Cooking/Agni: "— *Caraka Saṃhitā*, Sūtrasthāna 15.48"
  - Locator: L41 and L209 vs Cooking_and_Spices.md L95 / Apathya.md L64 / Agni.md L93 · Rule: citation accuracy (cross-article consistency)
  - Fix: Settle the canonical source (the verse is standardly Suśruta Saṃhitā Sūtrasthāna 15.41(48)) and use one attribution everywhere; if both texts carry it, say so explicitly rather than asserting a single conflicting home.

### `ayurveda/Āyurveda.md`

- **[quote-format]** Multiple blocks omit or misplace attribution. The Bhagavad Gītā and HYP blocks here pair Sanskrit + English + citation in inconsistent order, and the "amṛtasya nāma yad brahma" block (L25-28) has NO source attribution whatsoever — an unverifiable, possibly fabricated Vedic line. Several attributions (HYP 3 at L81, L90; Bhagavad Gītā 14.27) lack precise verse numbers. AGENTS.md L80 names Āyurveda.md specifically as carrying the wrong pattern.
  - Evidence: > **amṛtaṁ vai prāṇāḥ** > > "Prāṇa itself is Amṛta."\ > — *Bṛhadāraṇyaka Upaniṣad*  ... and L25: > **amṛtasya nāma yad brahma** / "That which is called Amṛta is Brahman." (no attribution at all)
  - Locator: L25-32, L38-50, L76-90 — citation placed BETWEEN Sanskrit and English; also L25-28 amṛtasya nāma yad brahma has no attribution · Rule: AGENTS.md primary-source quote-block: Sanskrit -> blank line -> English -> em-d…
  - Fix: Rebuild each block to the canonical order with a precise, verifiable locus; supply or remove the unattributed "amṛtasya nāma yad brahma" line; give HYP chapter 3 verses real numbers (the Amarolī/Vajrolī verses are HYP 3.96–99, not bare "3").

### `chloride/witnesses/Ancient_Witnesses_Against_Salt.md`

- **[factual-error]** The index calls itself "Eight-Tradition" and heads the table "The Eight Files," but the table enumerates nine files/traditions (and the repo AGENTS.md explicitly says nine); the count is internally contradictory.
  - Evidence: ## *An Index to the Eight-Tradition Quote-Book on Chloride* ... ### The Eight Files ... [table with nine rows: Ayurveda, Yoga, Tantra, Dharma, Greek, Hebrew, Chinese, Hygienists, Political]
  - Locator: lines 3, 11, 13 (subtitle "An Index to the Eight-Tradition Quote-Book"; heading "### The Eight Files"; the table that follows lists nine rows) · Rule: Rule 10 / internal consistency; parent AGENTS.md L193 calls it "the index to th…
  - Fix: Replace "Eight-Tradition" -> "Nine-Tradition" in the subtitle and "### The Eight Files" -> "### The Nine Files."

### `chloride/witnesses/Witnesses_Against_Salt_Yoga.md`

- **[tic]** The exact signature negative-contrast two-sentence pattern ("X is not Y. It is Z.") that AGENTS.md names as the single most important thing to eliminate, on a published article.
  - Evidence: This is the strongest possible framing: salt is not a dietary inconvenience. It is a moral obstruction, in the same register as the *kleśas* that Patañjali lists as the root of bondage.
  - Locator: line 51: "This is the strongest possible framing: salt is not a dietary inconvenience. It is a moral obstruction" · Rule: Rule 7 — negative-contrast "This is not X. It is Z." (the single most important…
  - Fix: State the positive directly: "Salt is classed here as a moral obstruction, in the same register as the *kleśas* that Patañjali lists as the root of bondage." Drop the "not a dietary inconvenience" setup and the meta "strongest possible framing" lead-in.

### `cosmology/All_Instruments_Measure_a_Level_Earth.md`

- **[tic]** The exact signature ChatGPT negative-contrast move (deny an alternative, then assert) opens section IV's central paragraph on a PUBLISHED article.
  - Evidence: This is not a caricature of the textbook position. It is the textbook position, stated by the textbooks themselves.
  - Locator: line 113, "This is not a caricature of the textbook position. It is the textbook position" · Rule: Rule 7 / AGENTS.md "Negative-contrast (the 'X is not Y. It is Z.' pattern) is t…
  - Fix: State the positive directly: "The textbook position itself, stated by the textbooks, redefines the word every one of their instruments is built to find..." Drop the "This is not... It is..." scaffold.
- **[tic]** Second instance of the banned "X is not Y. It is Z." pattern as a paragraph opener in the published article; with line 113 the pattern has become a structural rhythm.
  - Evidence: This is not a fringe claim. It is the first operation in every manual ever written for the craft.
  - Locator: line 16, "This is not a fringe claim. It is the first operation" · Rule: Rule 7 / AGENTS.md negative-contrast two-sentence form, used as a paragraph ope…
  - Fix: Open positively: "It is the first operation in every manual ever written for the craft" — the "not a fringe claim" denial adds nothing and can be cut entirely.
- **[meta-prose]** Explicit structure-announcing meta-prose ("the essay that follows assembles... for a single thesis") in a published article, the exact move the rule forbids.
  - Evidence: The essay that follows assembles the witnesses, from the standard university texts of the discipline to the zetetic primary sources that first pressed the point, for a single thesis:
  - Locator: line 21, "The essay that follows assembles the witnesses... for a single thesis" · Rule: Rule 7 / AGENTS.md "No meta-prose about the essay itself... Do not announce the…
  - Fix: Delete the meta-frame and state the thesis directly as a claim about the world: "The instruments take level for their reference and measure the world against it; the textbooks concede that reference surface is flat; and the curvature of the globe is never a reading the instrument takes but a figure the calculator assumes and adds by hand."

### `diet/Clay_Eating.md`

- **[quote-format]** Every one of the six bold-IAST quote blocks in this article lacks any em-dash source attribution, so none of the Sanskrit can be located or verified to a text/chapter/verse.
  - Evidence: > **"mṛttikā-bhakṣaṇam ca apy apāthyaṃ … rasānāṃ mārgān pidhāyati, vāyum uparuddhaṃ karoti."**\ > Clay-eating is unwholesome. It obstructs the pathways of the vital fluids and causes the obstruction of vāyu.
  - Locator: lines 7-8, 16-17, 23-24, 28-29, 33-34, 69-70 (all six Sanskrit quote blocks) · Rule: Rule 2 — primary-source quote blocks require an em-dash source attribution on t…
  - Fix: Add a `\`-broken em-dash attribution line to each block (e.g. `— *Caraka Saṃhitā*, Sūtrasthāna 26.xx`); if the verse cannot be sourced, replace with an attributable verse or mark it `— proverbial formulation, after *X*`.
- **[micronutrition]** Under 'True nourishment', the article positively prescribes 'bioavailable minerals' — endorsing the reductionist micronutrient register rather than naming it to reject it, which is exactly the residue rule 4 forbids.
  - Evidence: - Plant-based minerals offer true bioavailable nourishment.
  - Locator: line 60, '- Plant-based minerals offer true bioavailable nourishment.' · Rule: Rule 4 — no micronutrition vocabulary; this affirmatively recommends 'minerals'…
  - Fix: Replace with an Āyurvedic-mechanism recommendation (e.g. 'cooked grain and ghṛta rebuild rasa and ojas without burdening the channels') and drop the mineral/bioavailability framing.

### `diet/Fruits_From_India_Are_Different.md`

- **[factual-error]** Jobs died of a neuroendocrine pancreatic tumor (a cancer), not a fruit-caused 'pancreas failure'; asserting his and Kutcher's pancreatic problems were 'caused by fruit' as plain fact is an unsupported causal overreach, and the celebrity-anecdote run plus the 'It is caused by fruit' cap lets the example dominate the doctrine.
  - Evidence: Steve Jobs ate fruit in California. His pancreas failed. Ashton Kutcher ate fruit in Los Angeles. His pancreas rebelled within weeks. … It is caused by fruit.
  - Locator: line 39, 'Steve Jobs ate fruit in California. His pancreas failed. Ashton Kutcher … His pancreas rebelled within weeks.' · Rule: Factual accuracy; Rule 10 — example illustrates, never dominates
  - Fix: Drop or heavily qualify the causal claim (Kutcher's was a brief self-reported scare; Jobs had cancer); subordinate the anecdotes to the classical guṇa argument rather than ending the section on them.

### `diet/Interrupting_Fasts.md`

- **[quote-format]** The first Sanskrit block has no source attribution at all, and the second block's em-dash line is a grammatical parsing note rather than a text/chapter/verse citation, so neither quote is verifiable to a primary source.
  - Evidence: > **"mṛttikā-bhakṣaṇaṃ doṣa-kārakam ojas-hāri."**\ > Ingesting earth disturbs the system and diminishes Ojas.   …   > — *jīvena*: by means of the living principle; the dative of *jīva*, "life," …
  - Locator: lines 11-12 (quote block) and line 25 ('— *jīvena*: by means of the living principle…') · Rule: Rule 2 — every primary-source block needs an em-dash source attribution; the em…
  - Fix: Give each block a real `— *Caraka Saṃhitā*, …` attribution; move the *jīvena* parsing into the surrounding prose rather than onto the attribution line.

### `diet/Penultimate_Sāttvic_Food.md`

- **[quote-format]** Quote blocks violate the format on four counts at once: the citation is placed in the prose lead-in before the Sanskrit, there is no blank `>` separator line, the IAST is wrapped in quotation marks, and the English is italicized rather than plain-double-quoted with an em-dash attribution.
  - Evidence: Ṛg-Veda 1.142.3 declares: > **"ghṛtaṃ nabho amṛtasya nābhir."**\ > *"Ghee is the navel of immortality."*
  - Locator: lines 13-14, 34-35, 98-99 (quote blocks); citations sit in prose preambles at lines 11, 20, 32 · Rule: Rule 2 — Sanskrit (bold, unquoted) → blank `>` line → English in plain double q…
  - Fix: Reformat every block to the canonical shape: unquoted bold IAST, blank `>`, English in straight double quotes with `\` break, then `— *Ṛg-veda* 1.142.3` as the final attribution line.
- **[doctrine-contradiction]** The same guṇa *guru* is glossed as "deeply nourishing" in Penultimate but as "weighty"/"heavy" everywhere else in the corpus; *guru* means heavy/weighty, and "deeply nourishing" both mistranslates the guṇa and contradicts the project's own consistent gloss in Ghee.md and Dehydrated_Fruit, where *guru* is precisely the burdensome quality fruit/coconut are faulted for.
  - Evidence: Penultimate_Sāttvic_Food.md L43: "**guru** (deeply nourishing)"; Ghee.md L17: "*guru* (weighty)"; Dehydrated_Fruit_Coconut_Honey.md L27/L68: "**guru** (heavy)".
  - Locator: L43 "**guru** (deeply nourishing)" · Rule: Rule 5 (doṣa/guṇa symbology — name the guṇa the substance carries) + Rule 8 (co…
  - Fix: Change the Penultimate gloss to "*guru* (weighty/heavy)" to match Ghee.md and Dehydrated_Fruit; if the intent is to praise ghee's nourishing depth, attribute that to *ojaskara*/*bṛṃhaṇa*, not to *guru*.

### `diet/Vegan_Dairy.md`

- **[tic]** The entire article is structured on the negative-contrast pattern — title ('Dairy Is Not Intrinsically Non-Vegan'), opening ('never framed as… but as'), body ('reciprocal, not extractive'; 'the relationship, not the substance'), and closing ('reciprocity is not') — far exceeding the ~3-occurrence threshold that the rule says requires a full pass.
  - Evidence: It was never framed as a rule about excluding entire categories … but as an ethical criterion … / what matters is the relationship, not the substance. / Milk obtained through protection, care, and reciprocity is not.
  - Locator: lines 5, 11, 15, 17 (and title line 3) · Rule: Rule 7 — negative-contrast 'X is not Y, but Z' / 'not A but B' as the article's…
  - Fix: Rewrite around the positive claim ('Veganism is an ethical criterion of non-abuse; ghee from a cared-for cow satisfies it'); reserve at most one trailing-concession 'X, not Y' and cut the rest.

### `diet/Yogic_Food.md`

- **[citation-error]** Same misattribution: "annaṃ brahmeti vyajānāt" belongs to the Bhṛgu Vallī (TU 3.2), not 2.2.4, and is again framed as the conclusion of the same section as 2.2.1.
  - Evidence: > **Annaṃ brahma iti vyajānāt.** > > "He realized anna as Brahman." > > — Taittirīya Upaniṣad 2.2.4
  - Locator: L17-21 — "Annaṃ brahma iti vyajānāt" cited as Taittirīya Upaniṣad 2.2.4 · Rule: Bundle citation-accuracy (Taittirīya locus)
  - Fix: Cite as *Taittirīya Upaniṣad* 3.2.

### `diet/Yogis_Dont_Eat_Fruit.md`

- **[citation-error]** Same misattribution as Ambrosian_Diet: the line is Bhṛgu Vallī (TU 3.2), not Ānanda Vallī 2.2.4. The article calls it the close of "the ascent" begun at 2.1, but 2.1 (Ānanda Vallī) and the realization at 3.2 (Bhṛgu Vallī) are different chapters, so the chain it draws is bibliographically inaccurate.
  - Evidence: > **annaṃ brahmeti vyajānāt** > > "He knew anna as Brahman."\ > — *Taittirīya Upaniṣad* 2.2.4
  - Locator: L44-46 — "annaṃ brahmeti vyajānāt" cited as *Taittirīya Upaniṣad* 2.2.4 · Rule: Bundle citation-accuracy (Taittirīya locus)
  - Fix: Cite *Taittirīya Upaniṣad* 3.2; rephrase the connective so the 2.1 kośa-chain and the 3.2 Bhṛgu realization are not presented as one continuous section.

### `ghee/Ghee_Restored_my_Vitality.md`

- **[tic]** This is the exact "Not A. Not B. Not C." fragment hammer AGENTS.md names as a banned variant of the signature ChatGPT negative-contrast move.
  - Evidence: Nothing else had done this.\ Not disciplined raw fruit.\ Not the so-called protein foods.\ Not the intensity of śivāmbu or amarolī.
  - Locator: L17-21 "Nothing else had done this.\nNot disciplined raw fruit.\nNot the so-called protein foods.\nNot the intensity of śivāmbu or amarolī." · Rule: Rule 7 — negative-contrast, the triple-fragment hammer ("Not A. Not B. Not C.")
  - Fix: Cut the fragment cascade. State positively: "Ghṛta revealed the missing structure my system had been seeking — what raw fruit, the protein foods, and śivāmbu alone never supplied." Fold the dismissed items into a single trailing concession at most.

### `ghee/Ghṛta_Golden_Magic.md`

- **[quote-format]** Three format breaks: no blank `>` line separating the bold Sanskrit from the English; the English translation is not in double quotes; the attribution em-dash has no following space ("—*Bhagavadgītā*").
  - Evidence: > **dveṣa-rāga-viyuktais tu viṣayān indriyaiś caran\ > ātmavaśyair vidheyātmā prasādam adhigacchati**\ > Moving among the objects of the world without hatred or clinging,\ > one who is self-governed attains inner clarit…
  - Locator: L20-24 Bhagavadgītā 2.64 block · Rule: Rule 2 — Sanskrit / blank `>` line / quoted English with hard breaks / em-dash …
  - Fix: Insert a blank `>` line after the Sanskrit, wrap the translation in double quotes with `\` hard breaks, and write the attribution as "— *Bhagavadgītā* 2.64" with a space after the em-dash. Same fix for the 2.52 block at L28-32.
- **[quote-format]** Same three format breaks as the 2.64 block (no blank `>` separator, unquoted English, spaceless attribution dash). The English here is also a loose paraphrase, not a literal rendering of the verse.
  - Evidence: > **yadā te moha-kalilaṃ buddhir vyatitariṣyati\ > tadā gantāsi nirvedaṃ śrotavyasya śrutasya ca**\ > When your understanding crosses beyond the tangle of delusion,\ > you withdraw from the reactive energy of blame and …
  - Locator: L28-32 Bhagavadgītā 2.52 block · Rule: Rule 2 — quote-block structure
  - Fix: Apply the canonical structure; if the English is a paraphrase, attribute as "— proverbial formulation, after *Bhagavadgītā* 2.52" per rule 2.

### `personal/Age_of_Saturation.md`

- **[tic]** The negative-contrast / 'not-X-but-Y' construction is the article's pervasive default rhythm, recurring in nearly every paragraph (~10 instances in a 484-word piece).
  - Evidence: "it is not merely mechanical" (L3); "energetically rather than materially" (L3); "descriptive, not metaphorical" (L7); "That does not make them imaginary" (L9); "feedback dominance rather than total control" (L13); "imb…
  - Locator: L3, L5, L7, L9, L13, L15, L17, L19, L21, L23 · Rule: Rule 7 — negative-contrast 'X is not Y, it is Z' / 'not merely' / 'rather than'…
  - Fix: Rewrite each sentence to state the positive directly: e.g. "The current weakens when it is no longer fed" (drop "it is not fought"); "voladores, the fliers, a descriptive name" (drop "not metaphorical"); "Kali Yuga is imbalance" (drop "not evil in the cinematic sense"). A full pass is required.

### `personal/Olivier_Francoeur.md`

- **[stub-quality]** This is raw private astrological shorthand about a named individual, with zero explanatory prose; it does not belong in a public published essay collection and exposes a personal name. It is linked from the public _index.md.
  - Evidence: Entire body: '- ☉ ∥ ⯓ / - ☽ ∦ Asc ∥ Mc / - ⚸ ∥ ☿' — three bullets of bare astrological glyphs with no prose, no gloss, no title context, and a personal name as the only heading.
  - Locator: Whole file (L1-L5); linked from _index.md L129 · Rule: Bundle stub-quality concern; AGENTS.md 'Each file is a self-contained essay' — …
  - Fix: Remove from the public collection (delete the _index.md L129 link and relocate to private notes), or develop into an actual essay with glossed symbols; as-is it should not be published.

### `personal/The_Pressure_of_Being.md`

- **[other]** The article uses a long underscore line as a horizontal-rule separator between every section (8 occurrences) — a horizontal rule in disguise, banned by the house rule; the article already has '##' headings doing the structural work.
  - Evidence: ______________________________________________________________________
  - Locator: L5, L11, L17, L23, L29, L35, L43, L55 (lines of '______________________________________________________________________') · Rule: Rule 1 — No horizontal-rule separators; structure by headings only. (A long und…
  - Fix: Delete every underscore-rule line; the existing '## Bhagavad Gītā' etc. headings already separate the sections.

### `political/Cost_of_Manipulative_AI.md`

- **[other]** The H1 is rendered in Unicode mathematical-bold letters (U+1D400 block) instead of plain ASCII wrapped in markdown bold, an LLM/export artifact that breaks anchors, search, screen-readers, and Substack rendering.
  - Evidence: # **𝐓𝐡𝐞 𝐄𝐧𝐞𝐫𝐠𝐲 𝐂𝐨𝐬𝐭 𝐨𝐟 𝐊𝐞𝐞𝐩𝐢𝐧𝐠 𝐀𝐩𝐩𝐞𝐚𝐫𝐚𝐧𝐜𝐞𝐬 𝐈𝐧𝐭𝐚𝐜𝐭**
  - Locator: L1: # **𝐓𝐡𝐞 𝐄𝐧𝐞𝐫𝐠𝐲 𝐂𝐨𝐬𝐭 𝐨𝐟 𝐊𝐞𝐞𝐩𝐢𝐧𝐠 𝐀𝐩𝐩𝐞𝐚𝐫𝐚𝐧𝐜𝐞𝐬 𝐈𝐧𝐭𝐚𝐜𝐭** · Rule: AGENTS.md straight-quotes / no-export-artifacts clause; markdown heading hygiene
  - Fix: Rewrite the heading as plain ASCII: `# The Energy Cost of Keeping Appearances Intact` (drop the redundant `**` bold inside an H1).

### `political/Danger_of_Knowledge.md`

- **[quote-format]** Every Sanskrit block violates the house form: the IAST is unaccented and not bold, the English sits inline with the Sanskrit on the same line (no blank `>` separator, not in double quotes), the source titles are not italicized, and every attribution uses a plain hyphen `- ` instead of an em-dash `—`.
  - Evidence: > ayogye na kathayet *It should not be taught to the unfit.* > > - Hatha Yoga Pradipika
  - Locator: L37-L39 and L43-L45 (inline Sanskrit + italic English) and all attribution lines L9,L15,L21,L27,L33,L39,L45,L51,L57 · Rule: Rule 2 (primary-source quote-block structure: bold IAST line, blank `>` line, E…
  - Fix: Reformat each to canonical form: bold accented IAST on its own line with `\`, a blank `>` line, English translation in straight double quotes with `\`, then `> — *Haṭha Yoga Pradīpikā*` etc. on the final line. Add proper IAST diacritics (e.g. *ayogye na kathayet*, *Manusmṛti*).

### `political/Unfree_Markets.md`

- **[citation-error]** Several quotations are spurious or unverifiable: the Mayer Amschel Rothschild 'Permit me to issue...' line is a long-debunked apocryphal quote, the 'few who understand the system' line is also widely attributed-without-source, and the Voltaire 'paper money returns to its intrinsic value—zero' line is unsourced/apocryphal — presenting these as historical testimony weakens the essay's credibility.
  - Evidence: > "Permit me to issue and control the money of a nation, and I care not who makes its laws."\ > — *Attributed to Amschel Rothschild*
  - Locator: L5-L6 (Karl Marx), L12-L14 (Ayn Rand), L26 (Voltaire), L35-L36 (Rothschild), L50-L51 (Rothschild) · Rule: Rule 2 (attribution integrity; flag paraphrase/attributed/spurious quotes)
  - Fix: Drop or explicitly mark the Rothschild and Voltaire lines as 'attributed, source uncertain' (the file already hedges 'attributed' on two — extend the same honesty or cut them), and prefer verifiable primary sources (Bastiat, Rand are genuine).

### `research_yoga_ayurveda_lineage/00_index.md`

- **[broken-link]** The research index lists eight numbered files (01-08) but only 01, 02, 03, 06, 07 exist on disk; 04, 05, 08 are linked but missing. The directory's own index promises files that were never written, leaving three dead links and a numbering gap (04/05/08).
  - Evidence: - [04_shared_rsis_and_lineages.md](04_shared_rsis_and_lineages.md) — ... / - [05_shared_anthropology.md](05_shared_anthropology.md) — ... / - [08_modern_scholarship.md](08_modern_scholarship.md) — ...
  - Locator: lines 12, 13, 16 (links to 04_shared_rsis_and_lineages.md, 05_shared_anthropology.md, 08_modern_scholarship.md) · Rule: ARCHITECTURE invariant (index is canonical) + AGENTS §The Project (index links …
  - Fix: Either write the three missing files (04 shared ṛṣis, 05 shared anthropology, 08 modern scholarship) or remove their links from 00_index.md and renumber 06/07 to close the gap. The thesis paragraph references their content, so writing them is the intent-aligned fix.

### `sol-luna/Celestial_Name.md`

- **[tic]** The published article opens on a stacked negative-contrast ("do not fear... as they fear", "is not inadequacy but power"), the exact deny-then-assert rhythm the house style names as the single most important thing to eliminate.
  - Evidence: Human beings do not fear their flaws as deeply as they fear their own magnitude. The greatest terror is not inadequacy but power—power that demands coherence, responsibility, and visibility.
  - Locator: L3: "The greatest terror is not inadequacy but power" · Rule: Rule 7 — "Not X but Y" negative-contrast as the article's opening move
  - Fix: Open positively: "What human beings fear most deeply is their own magnitude — the power that demands coherence, responsibility, and visibility."

### `sol-luna/Kali_Yuga.md`

- **[tic]** Closing-counsel paragraph built on the triple-deny-then-assert hammer; with L14 ("not about survival alone, but about wholeness") and L43 ("this is not foreign—it is you") the article uses the pattern 3+ times and has made it the default rhythm.
  - Evidence: Plasma retention is not about ritual, nor about defiance. It is about remembering yourself in an age designed to make you forget.
  - Locator: L61: "Plasma retention is not about ritual, nor about defiance. It is about remembering yourself..." · Rule: Rule 7 — "Not A. Not B. ... It is C." multi-fragment negative-contrast
  - Fix: State positively: "Plasma retention is the practice of remembering yourself in an age designed to make you forget." Remove the "not ritual, nor defiance" setup.

### `sol-luna/Solar_Excess.md`

- **[tic]** Textbook two-sentence negative-contrast: the signature ChatGPT antithesis the house style bans outright, sitting at the article's rhetorical climax.
  - Evidence: It burns through burden, then through reserve, then through tissue itself. This is not failure of the sun. It is absence of the moon.
  - Locator: L9: "This is not failure of the sun. It is absence of the moon." · Rule: Rule 7 — negative-contrast "X is not Y. It is Z." (the single most important ti…
  - Fix: State the positive directly: "The sun has not failed; the moon never arrived." or simply "What is missing is the moon." Cut the "is not / it is" scaffold.

### `source-extracts/Apathya.md`

- **[citation-error]** The source-extract that downstream articles cite repeats the wrong locus (2.2.4) for "annaṃ brahmeti vyajānāt," which is Bhṛgu Vallī 3.2. Because this file is the citation authority, the error propagates into every article that quotes from it.
  - Evidence: ### Taittirīya Upaniṣad 2.2.4 — food as Brahman  > **annaṁ brahmeti vyajānāt.** > > "He knew *anna* as Brahman."\ > — *Taittirīya Upaniṣad* 2.2.4
  - Locator: L491-496 — heading "Taittirīya Upaniṣad 2.2.4 — food as Brahman" · Rule: Bundle citation-accuracy; source-extract is the citation backbone for the artic…
  - Fix: Correct the heading and attribution to Taittirīya Upaniṣad 3.2 (Bhṛgu Vallī); fixing it here is the upstream fix for the article-level repeats.

### `source-extracts/Cooking_and_Agni.md`

- **[citation-error]** Same wrong locus (2.2.4) for the Bhṛgu Vallī line (TU 3.2). Note this same file at L351 also attaches the heading "Taittirīya Upaniṣad 2.2" to oṣadhībhyo'nnam (2.2.1) — the two are conflated as one 2.2 section.
  - Evidence: ### Taittirīya Upaniṣad 2.2.4 — anna as Brahman  > **annaṃ brahmeti vyajānāt \|\|** > > "He knew *anna* as Brahman."\ > — *Taittirīya Upaniṣad* 2.2.4
  - Locator: L41-46 — heading "Taittirīya Upaniṣad 2.2.4 — anna as Brahman" · Rule: Bundle citation-accuracy
  - Fix: Correct to *Taittirīya Upaniṣad* 3.2.

### `source-extracts/Fruit_as_Medicine.md`

- **[citation-error]** Same wrong locus (2.2.4) for a line that is Taittirīya Upaniṣad 3.2 (Bhṛgu Vallī).
  - Evidence: ### Taittirīya Upaniṣad 2.2.4 — anna as Brahman  > **annaṃ brahmeti vyajānāt \|\|** > > "He knew *anna* as Brahman."\ > — *Taittirīya Upaniṣad* 2.2.4
  - Locator: L377-382 — heading "Taittirīya Upaniṣad 2.2.4 — anna as Brahman" · Rule: Bundle citation-accuracy
  - Fix: Correct to *Taittirīya Upaniṣad* 3.2.

### `source-extracts/Golden_Fountain/urine-as-nectar-and-the-amaroli-tradition.md`

- **[citation-error]** The ghee-as-amṛta phrase is cited as Ṛgveda 1.142.3, but the project's own dedicated Rg_Veda extract (ghrta-as-amrta.md L15-19, L66) locates `ghṛtasya nāma… amṛtasya nābhiḥ` at RV 4.58.1 (the Ghṛta-sūkta), verified against the accented text and Wikisource; RV 1.142.3 is an Āprī hymn and does not contain this line, so the two project files contradict each other.
  - Evidence: The same name attaches to ghee (*ghṛtam amṛtasya nābhiḥ*, Ṛgveda 1.142.3)
  - Locator: L14: "(*ghṛtam amṛtasya nābhiḥ*, Ṛgveda 1.142.3)" · Rule: Rule 2 (citation accuracy) / bundle guidance (citation accuracy still applies t…
  - Fix: Change "Ṛgveda 1.142.3" to "Ṛgveda 4.58.1" to match the verified citation in source-extracts/Rg_Veda/ghrta-as-amrta.md; or cite RV 4.58.1 and cross-link that file.

### `source-extracts/Salt_Dosage_and_Conditions.md`

- **[sodium-naming]** Standalone "sodium chloride" in the project's own prose, in a file that is not a sanctioned linguistic-contrast exception and not a verbatim citation title; the parallel passage in Apathya.md L374 correctly writes "~95–99% chloride of sodium."
  - Evidence: Note throughout: saindhava is itself ~95–99% sodium chloride (see [*Witnesses Against Salt — Āyurveda*]...)
  - Locator: L3: "saindhava is itself ~95–99% sodium chloride" · Rule: Rule 3 — "chloride of sodium," never "sodium chloride"
  - Fix: Replace with "chloride of sodium" to match Apathya.md L374 and the house rule.

### `yoga-tantra/Vajrolī.md`

- **[quote-format]** All eleven quote blocks violate the house quote form: the Sanskrit is NOT bold, there is NO blank '>' separator line, the translation is in italics instead of double quotes, the attribution uses a bare parenthetical '(Haṭha Yoga Pradīpikā 3.83)' instead of an em-dash line, and the source title is not italicized.
  - Evidence: > svecchayā vartamāno'pi yogoktair niyamair vinā / vajrolīṃ yo vijānāti sa yogī siddhi-bhājanam\ > *Even one who lives by personal inclination...becomes a vessel of accomplishment.*\ > (Haṭha Yoga Pradīpikā 3.83)
  - Locator: L7-L9 (and every quote block, e.g. L17-L19, L27-L29, L41-L43) · Rule: Rule 2 — Sanskrit (bold IAST) on top, blank '>' line, English translation in DO…
  - Fix: Reformat each block to: '> **svecchayā ... siddhi-bhājanam**' / '>' / '> "Even one who lives by personal inclination ..."\\' / '> — *Haṭha Yoga Pradīpikā* 3.83'.

## Medium-severity findings

All 140, grouped by bundle.

### ayurveda (19)

| File | Category | Problem | Fix |
|---|---|---|---|
| `Agni.md` | em-dash-density | Em-dash density in running prose is ~8.7 per 500 words, roughly double the ceiling; epithet gl… | Recast epithet glosses with colons or parentheses ("Jātavedas, knower of a… |
| `Agni.md` | tic | Textbook "not merely X. It is Y." negative-contrast, the signature banned move. | State it positively: "the modern raw-food register refuses the offering" —… |
| `Apathya.md` | citation-error | A central claim (salt grouped with clay/metal-eating under tamas) rests on a Caraka 'doctrinal… | Supply a real Caraka chapter.verse for the clay/metal-eating teaching (ver… |
| `Fidelity_of_Transmission.md` | filler | 38 bolded spans in a 15-line essay; bold is used as a default emphasis tic (the textual analog… | Strip nearly all bold (reserve it for genuine first-use terms) and rewrite… |
| `Fidelity_of_Transmission.md` | tic | Repeated X-not-Y antithesis is the article's governing rhythm, the highest-priority banned pat… | Convert each antithesis to a single positive assertion. |
| `Lineages_of_Science.md` | quote-format | Every one of ~20 quotes uses inline-italic English with a parenthetical (Citation) instead of … | Convert each to a `>` block with the English in straight quotes and an em-… |
| `Lineages_of_Science.md` | citation-error | HYP 3.96 is cited here for an amarolī/long-life claim, while the same project (Āyurveda.md L77… | Pin the exact HYP verse for the amarolī claim and use it consistently acro… |
| `Madhumeha.md` | other | The article is framed as a clinical treatment protocol (dose schedules, named medicated-ghee f… | Reframe around the classical doctrine (madhumeha as ojakṣaya / srotas-obst… |
| `Madhumeha.md` | quote-format | An Ayurveda article makes strong clinical claims (curing diabetes) with zero IAST primary-sour… | Add the canonical prameha/madhumeha verses from Caraka Nidānasthāna/Cikits… |
| `Mechanical_Purging.md` | tic | The article is built almost entirely on antithesis (X not Y, but Z) in a sustained mock-script… | Cut the not-but constructions and the pseudo-archaic pastiche; state the p… |
| `Mechanical_Purging.md` | quote-format | Every quote uses a two-line bold-Sanskrit/plain-English form with no blank `>` separator line,… | Convert each to the canonical block with a blank `>` line, quoted English,… |
| `Medical_Bleeding.md` | quote-format | Quotes are bare English with no IAST Sanskrit, no em-dash attribution line, and no chapter/ver… | Either supply the Sanskrit + verse in the canonical block, or use the sanc… |
| `Medical_Bleeding.md` | citation-error | The section is headed "Vedic Testimony" but quotes the Ḍamar Tantra and Haṭha Yoga Pradīpikā —… | Retitle to "Tantric and Yogic Testimony" or similar; reserve "Vedic" for a… |
| `Nourishment_in_Kali_Yuga.md` | quote-format | None of the quotations are blockquotes — they sit in body text as bold Sanskrit + plain Englis… | Wrap every quote in the canonical `>` block with bold IAST, blank `>` line… |
| `Nourishment_in_Kali_Yuga.md` | doctrine-contradiction | The thesis — that an eater's intention restores ojas to industrial ghee that 'by classical mea… | Either ground the intention claim in a real source (the brahmārpaṇa verse … |
| `The_Two_Pillars_of_Nourishment.md` | quote-format | A designated framework-anchor article (AGENTS.md L195) contains zero primary-source quote bloc… | Anchor the two-pillars claim with at least one Vedic/Caraka verse per pill… |
| `The_Two_Pillars_of_Nourishment.md` | doctrine-contradiction | This article calls clarified plant/nut/seed oils 'ojas-building' members of the lunar family, … | Reconcile: either restrict ojas-building to true ghṛta in both places, or … |
| `Triphala.md` | quote-format | All three quote blocks omit the blank `>` separator line and the quotation marks on the Englis… | Add the blank `>` line, quote the English, supply chapter.verse, and mark … |
| `Āyurveda.md` | quote-format | This quote block has no attribution line at all — no text, no em-dash — so the source of "amṛt… | Add an em-dash attribution with text and verse to L25-27, and supply chapt… |

### chloride-top (11)

| File | Category | Problem | Fix |
|---|---|---|---|
| `Chloride_Extrapolation.md` | citation-error | The book title is not italicized and drops the leading article; the Indictment correctly rende… | Render as '*A Devotion to Nutrition*'. |
| `Chloride_Extrapolation.md` | organization | Title does not match filename, and the article duplicates the narcotic framing and the identic… | Either retitle to reflect the genuine 'extrapolation/burden-of-proof' argu… |
| `Chloride_Extrapolation.md` | tic | Repeated negative-contrast fragments ('These are not X. They are Y.') and a trailing-summary c… | State positives directly ('These are accepted facts.') and replace the sum… |
| `Chloride_the_Narcotic.md` | tic | The article closes on the banned 'X does not Y. It Z's' construction, and uses the negative-fr… | Close on the positive: 'Chloride suppresses life — slowly, reliably, and a… |
| `Chloridism.md` | tic | Several 'not merely X, but Y' / 'not X but Y' constructions, the explicitly-named variant of t… | Rewrite as direct positives: 'To say chloride of sodium is to describe the… |
| `Inorganic_Minerals.md` | quote-format | All five primary-source blocks omit the blank blockquote separator, leave the English translat… | Reformat each to: bold IAST line(s), blank '>' line, "English translation"… |
| `Leaving_the_Chloridics.md` | citation-error | This Sanskrit block has NO attribution at all (every other quote in the file cites Gītā or Cas… | Add a source/locus, or label it '— proverbial formulation' per Rule 2; if … |
| `Minerals.md` | redundancy | The two files cover the same thesis (life-origin nourishment vs inert minerals) with overlappi… | Differentiate explicitly: make Minerals.md the 'ash/combustion category-er… |
| `NaCl_Not_Vegan.md` | tic | Opens on a stacked 'not X, nor Y, but Z' negative-contrast and the title/closing rest on 'salt… | Open positively: 'Veganism is a principle about harm: the refusal to parti… |
| `The_Chloride_Indictment.md` | tic | The final aphorism leads with the banned 'X is not Y' move; a published article closes on the … | Close on the positive assertion alone: '*Chloride is chloride. The record … |
| `The_Chloride_Indictment.md` | meta-prose | Multiple sentences announce what the essay itself is doing ('This essay sets down...', 'The ta… | Begin and continue with substance: open with the indictment itself, and re… |

### cosmology+surveying (3)

| File | Category | Problem | Fix |
|---|---|---|---|
| `All_Instruments_Measure_a_Level_Earth.md` | em-dash-density | Running-prose em-dash density is ~8.7 per 500 words, roughly 1.7x the rule's ceiling, on a pub… | Restructure the densest paragraphs (notably 170, 140, 152) into cleaner sy… |
| `All_Instruments_Measure_a_Level_Earth.md` | quote-format | Every quote block omits the required `\` hard break at the end of the English line before the … | Append a trailing backslash to the last English line of each block so the … |
| `Horizon_Dip_vs_Altitude.md` | tic | Uses the explicitly-banned "not merely... but..." construction to close the note. | State positively: "...and that everywhere below it the flat reading is exa… |

### diet (12)

| File | Category | Problem | Fix |
|---|---|---|---|
| `Ambrosian_Diet.md` | quote-format | In this PUBLISHED article the English translations are not wrapped in double quotes, deviating… | Wrap each English translation in straight double quotes to match the canon… |
| `Ambrosian_Diet.md` | tic | The opening of this PUBLISHED article uses the triple-negation hammer ('not… not… not. It is…'… | State the positive directly: 'The Ambrosian Diet is the diet described acr… |
| `Ambrosian_Diet.md` | em-dash-density | This PUBLISHED article runs roughly 10 prose em-dashes per 500 words, twice the ceiling, with … | Convert several parenthetical em-dash asides to commas or new sentences, e… |
| `Clay_Eating.md` | tic | Classic 'not Y but Z' negative-contrast construction opening the article's argument; the closi… | State positively: 'The ancient physicians read the craving for earth as a … |
| `Dehydrated_Fruit_Coconut_Honey.md` | em-dash-density | This (publish:true) article runs roughly 12 prose em-dashes per 500 words, well over the ~5 ce… | Rework the paragraphs at 66, 74, 101, 131-133 to use commas/colons and spl… |
| `Fear_of_Grains.md` | filler | Paragraph opens with the banned filler intensifier 'Crucially,' (the AGENTS.md remove-on-sight… | Delete 'Crucially,' and begin 'No controlled trial has ever tested grains … |
| `Fruits_From_India_Are_Different.md` | tic | Section-closing negative-contrast in its purest two-sentence form ('not caused by X. It is cau… | Collapse to a single positive: 'the depletion is caused by fruit, wherever… |
| `In_Praise_of_Agni.md` | em-dash-density | This PUBLISHED article runs roughly 11-12 prose em-dashes per 500 words (about double the ~5 c… | Restructure the heaviest paragraphs (89, 191, 197, 199, 235) into commas/c… |
| `Penultimate_Sāttvic_Food.md` | other | Every heading is wrapped in `**bold**` markdown, which renders as bold-on-bold and is inconsis… | Strip the `**` from all headings so they read `## The Sāttvic Hierarchy`, … |
| `Penultimate_Sāttvic_Food.md` | stub-quality | The article is built almost entirely from bullet lists and survey-style section headers ('Mode… | Rewrite the bulleted attribute dumps into running prose framed around the … |
| `Protein.md` | tic | The article's thesis sentence uses the 'not from X but from Y' antithesis, and the move recurs… | Recast positively: 'The modern concept of protein arose from the examinati… |
| `Yogic_Food.md` | quote-format | Mixed convention with the rest of the cluster: source titles are not italicized (`Taittirīya U… | Italicize the source titles on every attribution line (`— *Taittirīya Upan… |

### ghee (9)

| File | Category | Problem | Fix |
|---|---|---|---|
| `Ethical_Ghee.md` | tic | One-sentence negative-contrast form, one of three such constructions in this short article (al… | State positively: "This ethical rule is intrinsic to Āyurvedic logic." The… |
| `Ethical_Ghee.md` | tic | Second instance of the negative-contrast em-dash form in the same article; with L13 and L66 th… | "Ethical dairy is the original model:" — drop the "not theoretical" setup. |
| `Ethical_Ghee.md` | gloss-missing | ama (sticky residue of unfinished digestion), ojas (refined vital essence), sāttvic (of sattva… | Gloss each on first appearance, e.g. "ama (the sticky residue of incomplet… |
| `Ethical_Ghee.md` | micronutrition | The article leans on modern animal-welfare science and "the nutritive profile" as confirming e… | Cut the section or recast it in Āyurvedic terms: a distressed animal's mil… |
| `Ghee_Restored_my_Vitality.md` | tic | Standalone "This is not X. It is Y." closing paragraph — the explicitly banned negative-contra… | Replace with the positive claim alone: "It is lived truth, unfolding with … |
| `Ghee_Restored_my_Vitality.md` | gloss-missing | śivāmbu (urine therapy / one's own urine) and amarolī (the urine-retention yogic practice) are… | On first use: "śivāmbu (the practice of drinking one's own urine)", "amaro… |
| `Ghṛta_Golden_Magic.md` | tic | "X is not Y" opener; the article repeatedly builds via denial (L34 "not into apathy, but into … | "This golden magic follows the same metaphysical law that governs mantra…"… |
| `Ghṛta_Golden_Magic.md` | doctrine-contradiction | The article advances a novel action-at-a-distance mechanism (gratitude physically softening a … | Scope the claim to the practitioner's own state (the Gītā's actual teachin… |
| `Universality_of_Ghee.md` | tic | Negative-contrast "not because… but because…" form, sitting under a "## Conclusion" heading th… | "Ghee is sacred as the clarified essence of a gentle, herbivorous, sattvic… |

### political (12)

| File | Category | Problem | Fix |
|---|---|---|---|
| `All_Life_Is_Sacred.md` | gloss-missing | Several technical terms appear bolded but un-glossed on first use: *sekhem* (Egyptian term for… | Add brief inline glosses on first use: *prāṇa* (vital breath), *kuṇḍalinī*… |
| `Cheap_Talk.md` | tic | The signature negative-contrast pattern (the single-most-important tic to eliminate) is the de… | State the positive directly: 'A doer is defined by exposure.' / 'A doer ri… |
| `Cheap_Talk.md` | tic | A three-line italic 'X is not Y' fragment hammer placed as a quasi-epigraph — exactly the mech… | Replace with a single positive aphorism (the house prefers brief positive … |
| `My_Mothers_My_Sisters.md` | quote-format | All five Gītā quotes are English-only with no IAST Sanskrit line, where clean IAST is readily … | Add the IAST first pāda(s) above each English block (e.g. patraṃ puṣpaṃ ph… |
| `Obsolete_Social_Medias.md` | redundancy | Obsolete_Social_Medias.md and Twitter_is_Obsolete.md share near-identical passages verbatim (t… | Consolidate the two into one essay, or sharply differentiate them (Twitter… |
| `On_Anthropic.md` | meta-prose | The essay is openly scaffolded as a guided tour ('Let us begin', 'Consider next', 'Let us ask … | Cut the 'Let us begin/Consider next/Let us ask' connectives and open each … |
| `The_Duty_You_Cannot_Refuse.md` | tic | A staccato negative-fragment hammer ('No laboratory. No factory. No supplement.'), a variant o… | Compress to a single positive claim: 'No laboratory, factory, or supplemen… |
| `The_Duty_You_Cannot_Refuse.md` | structural-mirror | This essay heavily duplicates My_Mothers_My_Sisters.md (same vegan-decoy argument, same Gītā 3… | Decide which essay owns the vegan-alliance argument and differentiate or m… |
| `The_Duty_You_Cannot_Refuse.md` | quote-format | The Sanskrit line is wrapped in double quotes (the house form bolds bare IAST, no quotes), the… | Reformat: `> **sarva-bhūta-hite ratāḥ**\` then a blank `>` line, then `> "… |
| `The_Idol_of_Wisdom.md` | meta-prose | A heading literally labeled 'Conclusion' announces the essay's structure, and the section is a… | Drop the 'Conclusion:' label (rename or merge), and end on the strong fina… |
| `The_Idol_of_Wisdom.md` | structural-mirror | The essay is structured wholly as a recap of one secondary author's polemic (six 'Bjerknes arg… | Reframe to assert the project's own claim (mathematical mysticism displace… |
| `The_Warrior.md` | meta-prose | The opening explicitly announces 'Herein lies a cohesive guide...as gleaned from the teachings… | Delete the sentence and open on the warrior's substance; if the Castaneda … |

### research (7)

| File | Category | Problem | Fix |
|---|---|---|---|
| `00_index.md` | tic | The index thesis opens on the banned "Not A. Not B. But C." triple-fragment hammer — the signa… | State the positive directly: "Yoga and Āyurveda are two faces of a single … |
| `00_index.md` | index-gap | Files 04, 05, 08 are linked from the index and forward-referenced from inside 01–03 (e.g. 01 L… | Either write the three files, or remove their index entries and the forwar… |
| `01_vedic_origins.md` | tic | The "X is not Y; it is Z" / "X is not Y. It is Z." construction is the file's default close fo… | Rewrite each Relevance close as a positive declarative: e.g. "The lineage … |
| `01_vedic_origins.md` | citation-error | The same Kaṭha first-definition-of-yoga verse is cited two different ways across the research … | Standardize on Olivelle's sectional numbering (Kaṭha 2.3.10–11) throughout… |
| `03_sastric_crossreferences.md` | tic | The concluding-synthesis paragraph opens on the two-sentence negative-contrast form; combined … | Open positively: "Yoga and Āyurveda are one discipline with two registers … |
| `03_sastric_crossreferences.md` | citation-error | This quotation is garbled — broken syntax, ellipsis-stitched fragments that do not parse ("But… | Re-extract the passage verbatim from Dasgupta vol. I (the Pañcaśikha–Carak… |
| `06_structural_parallels.md` | tic | The opening claim leads with the "not X. They are Y." negative-contrast form, then stacks mirr… | Open with the positive claim ("Patañjali's aṣṭāṅga-yoga and the Āyurvedic … |

### sol-luna (11)

| File | Category | Problem | Fix |
|---|---|---|---|
| `2-Luna.md` | tic | Negative-contrast construction; the positive claim ("these are aspects of one thing") stands o… | "They are aspects of one thing." — delete the "not analogies" setup, or fo… |
| `Celestial_Name.md` | tic | Two further negative-contrast constructions; with the L3 opener the pattern recurs >3 times, c… | "Civilizations also predicted renewal." / "these are participants in renew… |
| `Kali_Yuga.md` | tic | Two more negative-contrast constructions reinforcing the article's reliance on the banned anti… | "The act is about wholeness — body, mind, and spirit in circulation." / "F… |
| `Kali_Yuga.md` | gloss-missing | prāṇa (vital breath/life-current) is used untranslated on first appearance; Amarolī is given a… | "prāṇa (the vital breath)" on first use; expand Amarolī inline: "(Amarolī,… |
| `Sidereal.md` | index-gap | The index title "Sidereal" matches neither the H1 nor any content of the article (the article … | Rename the index link to match the H1 ("Zodiac and Nakṣatras: Grammars of … |
| `Solar_Excess.md` | tic | Opens the article on the negative-contrast move; combined with L9 and L8 ("What is absent is t… | Recast as a positive diagnosis: "The fruitarian lacks the lunar. Fruit is … |
| `Solar_Excess.md` | gloss-missing | Śivāmbu (urine therapy / one's own water), snigdha (unctuous), and ojas appear with no parenth… | Gloss on first use: "Śivāmbu (one's own water, the urine-elixir) is solar"… |
| `The_108_Solar_Divisions.md` | organization | The Uttara Phalguni group header says "Padas 46-48" but Pada 45 is the Leo pada of the same na… | Correct the boundary: Leo holds Pada 45 (Uttara Phalguni pada 1), Virgo ho… |
| `The_360_Phases_of_Sol.md` | organization | The article opens with a free-floating prose blurb before any heading and never declares an H1… | Add an H1 ("# The 360 Phases of Sol"), and either drop the structure-annou… |
| `The_Solar_Matrix_of_Creation.md` | tic | Two negative-contrast constructions, the second opening the final section; mechanical antithes… | "The twelve divisions of the Sun's circle become twelve currents of creati… |
| `The_Toroidal_Heart.md` | factual-error | The lunar nodal cycle is ~18.6 years (correctly given), but the asserted bodily mapping (wisdo… | Frame as analogy/correspondence rather than mechanism: "The body keeps cyc… |

### src-astrology (5)

| File | Category | Problem | Fix |
|---|---|---|---|
| `science-and-astrology.md` | citation-error | The '(L/T³ or LT)' alternative contradicts the rest of the document and Young's own angular sc… | Render the cell as 'Control (L/T³)' to match the body of the extract, or, … |
| `astrological-houses.md` | tic | Four consecutive bullets all built on the same not-X-but-Y antithesis, making the negation the… | Recast at least two of the four as direct positive statements ('The horizo… |
| `astrology-of-personality.md` | quote-format | A verbatim Rudhyar quotation is embedded inline in italics inside the framing prose with no at… | Lift it into a proper blockquote ending with '— Dane Rudhyar, *The Astrolo… |
| `astrology-of-personality.md` | tic | Textbook two-sentence negative-contrast setup in the editorial connective tissue — deny the al… | State the positive directly: 'Astrology is the index of the prevailing rel… |
| `astrology-of-transformation.md` | redundancy | The same Prologue quotation is reproduced twice in one extract — line 32 is a near-verbatim su… | Keep the fuller version (line 146) as the closing and replace line 32's du… |

### src-lunar-death (6)

| File | Category | Problem | Fix |
|---|---|---|---|
| `urine-as-nectar-and-the-amaroli-tradition.md` | factual-error | The text's name is spelled "Khecharīvidyā" (extra 'h') here, whereas the canonical dedicated e… | Standardize to "Khecarīvidyā" (matching Khecarividya/lunar-nectar-and-brea… |
| `lunar-nectar-and-breath.md` | broken-link | Source links point to a GitHub repo `LiGoldragon/bibliography`, but AGENTS.md names the canoni… | Point bibliography paths at the canonical `~/primary/repos/library/en/<aut… |
| `passages.md` | tic | Two negative-contrast constructions in adjacent Notes bullets ("not an image or a reflection, … | Recast positively: "Luna has substance, weight, locus — a world"; "Luna ci… |
| `soma-and-the-moon.md` | quote-format | The IAST Sanskrit for RV 10.90.13 is placed below the English translation and attribution as a… | Restructure to canonical form: bold IAST Sanskrit inside the blockquote on… |
| `soma-and-the-moon.md` | tic | Explicit "not merely X — Y" negative-contrast construction, the signature banned pattern; stat… | State positively: "Luna is poured out and refilled" (the waning is the god… |
| `moon-as-soul-threshold.md` | tic | Negative-contrast "not Y; she is Z" followed by a second antithesis ("interrogation, not illum… | State directly: "She is a gatekeeper who asks a question; her verb is inte… |

### src-yoga-diet (5)

| File | Category | Problem | Fix |
|---|---|---|---|
| `Cooking_and_Agni.md` | quote-format | This is the line the project's own verification note (Raw_Vegan_Fruitarian_Harm.md L5) identif… | Either drop the constructed Sanskrit line and keep the English with the pr… |
| `Cooking_and_Agni.md` | tic | Negative-contrast antithesis closing section IX; mechanical setup-then-assert form the house s… | Recast positively: "The raw-foodist error is making the raw plate the stap… |
| `Fruit_as_Medicine.md` | citation-error | The "all rasas strength-promoting / one rasa debilitating" aphorism is the verse immediately f… | Verify against the Sharma 2014 / caraka-samhita digest and renumber the ap… |
| `Raw_Vegan_Staples_Warnings.md` | tic | Closing the synthesis on the signature negative-contrast antithesis the house style bans, and … | State it positively: "The tradition examined the raw-vegan plate food by f… |
| `Raw_and_Cooked_Cross_Tradition.md` | micronutrition | "total calories," "protein structure," and "nutrients" appear in the compilation's own editori… | Recast in Āyurvedic mechanism: cooking as saṃskāra shifting guru→laghu and… |

### water (4)

| File | Category | Problem | Fix |
|---|---|---|---|
| `Plasma_Recycling_Manual.md` | quote-format | On a published article the primary-source quotes are labeled with the citation BEFORE the quot… | Move each source to a trailing '— *Ḍāmara Tantra* Verse N' / '— *Haṭha Yog… |
| `The_Distilled_Water_Paradox.md` | earth-as-planet | The project's own prose calls Earth 'the planet'; this is not a quotation of another author, s… | Replace with 'on earth' / 'the most ubiquitous inorganic mineral worldwide… |
| `The_Distilled_Water_Paradox.md` | tic | The two-sentence 'is not X. It is Y.' negative-contrast pattern recurs at least five times in … | Do a full pass: cut the 'is not ...' setup and keep the positive claim in … |
| `The_Distilled_Water_Paradox.md` | filler | Banned filler phrase 'the fact that' used where it is compressible. | 'would have to confront that they are eating the earth...' or 'would have … |

### witnesses (7)

| File | Category | Problem | Fix |
|---|---|---|---|
| `AGENTS.md` | organization | All nine per-tradition witnesses files now use the CORRECT attribution-at-end pattern (bold IA… | Remove `chloride/witnesses/Witnesses_Against_Salt_*.md` from the list of f… |
| `Witnesses_Against_Salt_Ayurveda.md` | em-dash-density | Prose em-dash density is ~9.7 per 500 words even before excluding quote-block words from the d… | Restructure the heaviest parenthetical asides (the catalogue interjections… |
| `Witnesses_Against_Salt_Chinese.md` | em-dash-density | Prose em-dash density ~8.5 per 500 words (inflated denominator includes Chinese-character/piny… | Convert the bullet-gloss parentheticals (L24-26, L9, L39) to comma clauses… |
| `Witnesses_Against_Salt_Greek.md` | tic | "do not merely moderate ... They abstain" is the "not merely X, but Y" negative-contrast varia… | Rewrite positively: "The priests abstain so strictly that even bread baked… |
| `Witnesses_Against_Salt_Political.md` | factual-error | The sentence says "five cases" then lists six (Aztec, Roman, Han Chinese, French, British Indi… | Change "the five cases" to "the six cases." |
| `Witnesses_Against_Salt_Tantra.md` | tic | "not merely X but Y" negative-contrast construction, the banned LLM rhythm, on a published art… | "The body, for tantric practice, is a laboratory in which ordinary substan… |
| `Witnesses_Against_Salt_Yoga.md` | em-dash-density | Prose em-dash density ~8.3 per 500 words (inflated denominator includes Sanskrit verse lines, … | Recast the parenthetical asides at L7, L33, L62, L66, L72 with commas or s… |

### xcut-citation (7)

| File | Category | Problem | Fix |
|---|---|---|---|
| `Apathya.md` | citation-error | Apathya.md attributes the eight-salts-plus-lead-and-alkali grouping to AH Sū. 6.147, but Witne… | Reconcile the locus across Apathya.md, Witnesses_Against_Salt_Ayurveda.md,… |
| `Āyurveda.md` | citation-error | Bold-IAST quote blocks attributed only to "*Ḍamar Tantra*" (no chapter/verse) and to "classica… | Add a locatable chapter/verse for each Ḍamar Tantra block or demote to cle… |
| `Witnesses_Against_Salt_Ayurveda.md` | quote-format | The lavaṇa verse is cited only as "Sūtrasthāna 26 (atiyoga-prakaraṇa)" while the project's own… | Pin the lavaṇa verse to Sū. 26.43(3) to match the source extracts; either … |
| `Witnesses_Against_Salt_Ayurveda.md` | citation-error | The Sanskrit opens "varaṃ" (the best) but the translation renders it "Saindhava (the best)" — … | Translate varaṃ as "the best (i.e. saindhava)" transparently; reconcile wh… |
| `Ambrosian_Diet.md` | citation-error | The bare "*Ṛg-veda*" gives no maṇḍala.hymn.verse, and the wording differs from the project's o… | Either cite RV 4.58.1 with the attested wording (ghṛtasya ... jihvā devānā… |
| `Ambrosian_Diet.md` | citation-error | The project's own source extract Cooking_and_Agni.md (L201-204) cites the same line as Cikitsā… | Match the source extract: mark as proverbial formulation, after *Caraka Sa… |
| `Yogic_Food.md` | citation-error | Both bold-IAST lines read as direct verses but are short, formula-like constructions attribute… | Replace with attested verses from the source extracts (e.g. Caraka Sū. 5.1… |

### xcut-consistency (6)

| File | Category | Problem | Fix |
|---|---|---|---|
| `The_Two_Pillars_of_Nourishment.md` | doctrine-contradiction | Two Pillars promotes clarified seed/plant oils as ojas-building lunar equals of ghee, while Fr… | Qualify the Two Pillars "plant-ghee/seed-ghee" passage to state these are … |
| `Ambrosian_Diet.md` | citation-error | Three articles render the single "navel of immortality" ghee-verse with three different Sanskr… | Pick one verified locus and Sanskrit (Ghee.md's RV 4.58.1 *ghṛtasya nāma g… |
| `Ambrosian_Diet.md` | doctrine-contradiction | Ambrosian_Diet's own quotation of HYP 1.62-63 includes paṭola (a fruit) and "five leafy greens… | Reconcile the two HYP food-list characterizations: either acknowledge in Y… |
| `Fruitarianism.md` | citation-error | The identical sūtra (throat-well, cessation of hunger and thirst) is attributed to 3.30 in Amb… | Verify against the Pātañjala-yoga-sūtra (the throat-well sūtra is canonica… |
| `Yogis_Dont_Eat_Fruit.md` | doctrine-contradiction | Yogis_Dont_Eat_Fruit lists saindhava as one of the daily-admitted foods with no chloride cavea… | Add the standing caveat where saindhava is named on the daily list (e.g. "… |
| `Salt_Dosage_and_Conditions.md` | sodium-naming | This source-extract writes the banned English order "sodium chloride" in running prose while i… | Replace "~95–99% sodium chloride" with "~95–99% chloride of sodium" to mat… |

### xcut-organization (7)

| File | Category | Problem | Fix |
|---|---|---|---|
| `AGENTS.md` | organization | AGENTS.md still names these files as exemplars of the retired citation-between pattern, but th… | Update the AGENTS.md L80 sentence: remove the now-migrated files from the … |
| `_index.md` | index-gap | The source-extracts indexing in _index.md is haphazard: 14 of the source-extract files are not… | Decide a deliberate policy: either list every extract that an article cite… |
| `Minerals.md` | redundancy | chloride/Minerals.md and chloride/Inorganic_Minerals.md make the identical core argument (the … | Merge into a single canonical 'minerals' essay (Inorganic_Minerals.md is t… |
| `All_Instruments_Measure_a_Level_Earth.md` | index-gap | All_Instruments_Measure_a_Level_Earth.md is marked publish:true but is missing from .substack-… | Add a .substack-posts.json entry (source_path + banner_image) and generate… |
| `Notes.md` | stub-quality | Notes.md is a three-bullet scratch outline titled 'The Vedas are the Superior Scriptures' — no… | Either remove the _index.md link until the note becomes a real article, or… |
| `Olivier_Francoeur.md` | stub-quality | The author-bio file linked first under 'Personal & meta' is three lines of bare astrological a… | Replace with an actual prose author bio (the _index.md byline already says… |
| `Salt_Dosage_and_Conditions.md` | sodium-naming | A source-extract under the project's own authorship (not a verbatim citation title) writes 'so… | Change to 'saindhava is ~95-99% chloride of sodium'. (Flagged by orchestra… |

### yoga-tantra+personal (9)

| File | Category | Problem | Fix |
|---|---|---|---|
| `Longevity.md` | quote-format | The attribution line is separated from the quote by a blank line and falls OUTSIDE the blockqu… | Append '\\' to the quote's last line and prefix the attribution with '>': … |
| `Notes.md` | stub-quality | Notes.md is a 3-line rough insight list, not a self-contained essay, yet it is linked from the… | Either develop into an essay or remove the public _index.md link (L130) an… |
| `Refinement.md` | organization | Refinement is half-registered in the Substack manifest (entry exists with banner) while its ow… | Decide the intent: either set 'publish: true' and complete the manifest en… |
| `Refinement.md` | meta-prose | Self-referential meta-prose announcing what 'this article' will do over 'the length of its rea… | Cut the clause; end the sentence at "the picture the old corpora keep retu… |
| `The_Pressure_of_Being.md` | quote-format | No quote in the anthology uses the house attribution form: translations are wrapped in italics… | Reformat each as: English in plain double quotes, then a '\\'-broken em-da… |
| `The_Pressure_of_Being.md` | citation-error | Several quotes lack any source locus (Kolbrin passage, all four Castaneda impeccability quotes… | Add chapter/verse for the Kolbrin passage and book titles for the four Cas… |
| `The_Pressure_of_Being.md` | stub-quality | The piece is a raw quote-dump with a trailing bullet summary and no connective prose; it reads… | Either develop it into framed prose (short orientation, quote, minimal com… |
| `Vajrolī.md` | gloss-missing | Key technical terms appear unglossed: 'Vajrolī' itself is never defined as a perineal/urethral… | Gloss on first use: Vajrolī (the upward-contraction/retention practice), b… |
| `Vajrolī.md` | tic | The negative-contrast pattern recurs ~5 times across the article's own commentary, becoming a … | State each positively: e.g. "Its authority arises from understanding that … |

## Low-severity findings

All 126, grouped by bundle (polish-level).

### ayurveda (11)

| File | Category | Problem |
|---|---|---|
| `Agni.md` | weak-closing | The article closes with a multi-line restatement/summary cascade rather than a single aphoristic line; the final "## Th… |
| `Apathya.md` | meta-prose | Even this reference-voice article opens two sections with structure-announcing meta-prose ("The essay translates and gl… |
| `Fidelity_of_Transmission.md` | quote-format | Text titles are bolded rather than italicized, and *Damar Tantra* lacks the IAST diacritic (*Ḍamar Tantra*) used in sib… |
| `Lineages_of_Science.md` | organization | The article's load-bearing content (Anunnaki, a 'great white pyramid' encoding cataclysm intervals, Toltec energy-scien… |
| `Madhumeha.md` | gloss-missing | agni, ojas, ghṛta, vāta, kapha, pitta, medas, srotāṃsi, rasāyana all appear without a first-use English gloss in this a… |
| `Medical_Bleeding.md` | doctrine-contradiction | The article equates loss of 'plasma' with bloodletting, but the project's plasma = śivāmbu = urine (retained, not disch… |
| `The_Two_Pillars_of_Nourishment.md` | redundancy | The solar-plasma / lunar-ghee framework is defined in full here and re-defined from scratch in Madhumeha.md (and again … |
| `Triphala.md` | stub-quality | The article is a 21-line fragment built on three unsourced couplets and one very long abstract opening sentence; it ass… |
| `True_Ayurveda.md` | tic | The article leans on antithesis (scalpel-not-buffet, False/True paired clauses, 'authority resides in what sustains lif… |
| `True_Ayurveda.md` | quote-format | The article names Caraka's defining verse and the HYP amarolī verse in prose but never quotes either in the canonical b… |
| `Āyurveda.md` | organization | The flagged defect is now stale: Āyurveda.md's quote blocks place the citation AFTER the English (compliant), and True_… |

### chloride-top (5)

| File | Category | Problem |
|---|---|---|
| `Chloride_In_Produce_Evidence_Table.md` | micronutrition | This research note repeats 'essential micronutrient'/'essential elements' as accepted plant-science framing rather than… |
| `Chloride_In_Produce_Evidence_Table.md` | organization | The evidence table (already noted by the orchestrator as an _index orphan) is also not referenced from the articles who… |
| `Inorganic_Minerals.md` | citation-error | This IAST line reads as a constructed/paraphrased motto, not a locatable Bṛhadāraṇyaka verse (no chapter.verse given; g… |
| `Inorganic_Minerals.md` | gloss-missing | prāṇa appears first at L12 with no gloss; Amarolī and śilājatu are named without a parenthetical English gloss on first… |
| `Inorganic_Minerals.md` | tic | The triple 'X is not rasāyana' fragments are the negative-fragment hammer; combined with L61's stacked negatives the se… |

### cosmology+surveying (5)

| File | Category | Problem |
|---|---|---|
| `All_Instruments_Measure_a_Level_Earth.md` | gloss-missing | "Zetetic" — the load-bearing term of art naming the entire tradition the article rests on — is used four times with no … |
| `All_Instruments_Measure_a_Level_Earth.md` | weak-closing | The italic coda restates verbatim the imagery and claims already delivered in the section VII closers (lines 172-174: "… |
| `Horizon_Dip_vs_Altitude.md` | em-dash-density | Em-dash density runs ~10.7 per 500 words, over twice the ceiling; lines 48 and 56 each pack 4 into a single paragraph. … |
| `Horizon_Dip_vs_Altitude.md` | meta-prose | The clause critiques an earlier draft phrasing of this same note ("calling the low end 'nothing' blurred..."), leaking … |
| `Surveying_Instruments_And_The_Shape_Of_The_Earth.md` | stub-quality | A dedicated subsection (VIII) and the Sources entry (line 888) carry Garwood as a heading with an explicit admission th… |

### diet (7)

| File | Category | Problem |
|---|---|---|
| `Grains.md` | citation-error | A stray `\*` (escaped asterisk) sits after 'Caraka Saṃhitā' on the attribution line — a leftover italic-marker artifact… |
| `Grains.md` | quote-format | The block inverts the convention — Sanskrit is italicized rather than bold and the English translation is bolded rather… |
| `In_Praise_of_Agni.md` | gloss-missing | In this PUBLISHED article *ojas* and *sattva* appear first without a parenthetical English gloss (prāṇa is glossed at l… |
| `Interrupting_Fasts.md` | meta-prose | The italic subtitle is a 'How X triggers Y and derails Z' mechanism-announcement that pre-narrates the essay's structur… |
| `Interrupting_Fasts.md` | redundancy | Three diet articles re-make the same anti-clay argument (jīvena jīvam, ojas-hāri, channel obstruction) with overlapping… |
| `Penultimate_Sāttvic_Food.md` | factual-error | *Guru* is glossed as 'deeply nourishing', but the guṇa *guru* means heavy/dense (its nourishing connotation is interpre… |
| `Vegan_Dairy.md` | weak-closing | The closing restates the thesis in the same 'is / is not' antithesis the whole article runs on, ending on contrast rath… |

### ghee (4)

| File | Category | Problem |
|---|---|---|
| `Ethical_Ghee.md` | em-dash-density | Eight prose em-dashes (none are quote attributions) in 488 words is ~8.2 per 500, above the ~5 threshold; the dash has … |
| `Ethical_Ghee.md` | other | Every heading is wrapped in `**bold**` markers (redundant inside a heading), a ChatGPT-export tic absent from the polis… |
| `Ghee_Restored_my_Vitality.md` | doctrine-contradiction | The same two unglossed practices are first framed as the failing crutch of depleted fruitarians (L45) and then as somet… |
| `Universality_of_Ghee.md` | redundancy | The "pure life → pure milk → pure ghee" chain is stated three times (L31, L45-46, L59-61) and the Conclusion restates t… |

### political (14)

| File | Category | Problem |
|---|---|---|
| `Cheap_Talk.md` | filler | Dense, repeated single-word/short-phrase italic emphasis (a dozen-plus instances) is an LLM emphasis tic; it substitute… |
| `Cheap_Talk.md` | tic | The title itself is built on the negative-contrast move ('Talk Is Cheap, Reality Is Not'), and the H1/H2 are italicized… |
| `Danger_of_Knowledge.md` | citation-error | Several quotes are loose paraphrases presented as verbatim with no logion/section number ('Gospel of Thomas' has no cha… |
| `Danger_of_Knowledge.md` | citation-error | Castaneda attribution lacks the work (The Teachings of Don Juan); 'wideawake' is also a transcription artifact (should … |
| `EU_Law_Against_Intelligence.md` | filler | Nearly every paragraph ends on an italicized one-word payload, a recognizable LLM emphasis cadence; combined with the a… |
| `Freedom_of_Thought.md` | citation-error | This famous line is not actually in Plato's Phaedrus and is apocryphally attributed to Socrates; the Plutarch 'An unjus… |
| `My_Mothers_My_Sisters.md` | gloss-missing | First use of *ojas* (the central term of the essay) carries no gloss; *snigdha-madhura*, *sarpiṣāṃ paramam*, *tapas*, *… |
| `Obsolete_Social_Medias.md` | tic | The chained-anaphora 'X hardened into Y. Y hardened into Z.' is a recognizable LLM rhythmic device (it recurs identical… |
| `Poisonous_Music.md` | gloss-missing | Minor: source titles in attributions are not italicized (Ṛgveda, Śiva Sūtra, Bṛhadāraṇyaka Upaniṣad, Śatapatha Brāhmaṇa… |
| `The_Idol_of_Wisdom.md` | citation-error | Direct quotations (Tesla on relativity, the two Einstein epigrams) are embedded inline without source, date, or em-dash… |
| `The_Tyrant.md` | citation-error | The entire essay is a close paraphrase of Castaneda's petty-tyrant teaching (death-as-adviser, the four attributes of w… |
| `The_Warrior.md` | quote-format | Direct Castaneda quotations are embedded inline with no attribution anywhere in the piece, and a space precedes the clo… |
| `The_Warrior.md` | organization | A heading-like phrase ('The Four Natural Enemies of a Man of Knowledge') is run into the body sentence with no heading … |
| `Unfree_Markets.md` | quote-format | Attribution italicizes the author name (*Karl Marx*, *Voltaire*) instead of the source work; the rule italicizes the so… |

### research (5)

| File | Category | Problem |
|---|---|---|
| `01_vedic_origins.md` | citation-error | Every source path in these research notes points at `~/git/bibliography/...`, the stale location flagged in the known .… |
| `02_samkhya_shared_metaphysics.md` | tic | The closing synthesis uses the "not merely X — they Y" negative-contrast variant in the project's own voice (distinct f… |
| `03_sastric_crossreferences.md` | meta-prose | All-caps editorial flagging ("CROWN JEWEL", "KEYSTONE") and self-referential "Why this is the crown jewel" headings are… |
| `06_structural_parallels.md` | em-dash-density | Em-dash is the habitual rhythmic break in the file's connective prose, pushing density over the ceiling even discountin… |
| `06_structural_parallels.md` | quote-format | The chloride-of-sodium vocabulary has been bracket-substituted into a verbatim Muktibodhananda quotation. Brackets do m… |

### sol-luna (22)

| File | Category | Problem |
|---|---|---|
| `2-Luna.md` | tic | Another not-X-but-Y; defensible here as a correction of a likely misreading, but it is the second negative-contrast in … |
| `2-Luna.md` | gloss-missing | "shivambu" appears bare (no IAST diacritics, no italics, no gloss) in a list where rasa and ojas are both italicized an… |
| `Celestial_Name.md` | other | Uses tight (unspaced) em-dashes, inconsistent with the spaced em-dash convention used everywhere else in the bundle (e.… |
| `Celestial_Name.md` | weak-closing | The article opens with a long abstract thesis paragraph in the author's own voice before any primary source; the house … |
| `Kali_Yuga.md` | other | The H1 wraps the title in bold (**...**), which every other sol-luna article avoids (plain "# Sol", "# Luna", "# The To… |
| `Kali_Yuga.md` | organization | All four practice steps are authored as "1." (lazy ordered-list numbering). It renders 1-2-3-4 in most engines but is f… |
| `Line_of_Sight.md` | weak-closing | The article closes under a heading literally titled "Bottom line" with a summary restatement, the trailing-summary clos… |
| `Line_of_Sight.md` | quote-format | The English-only block quotes lead with the citation (author/title) and then the quoted text, the inverse of the house … |
| `Line_of_Sight.md` | other | The article is built almost entirely as a line-by-line tabulation of engineering examples and a debunking formula, the … |
| `Sidereal.md` | tic | Single negative-contrast construction; isolated (the rest of the article is clean) but it is the banned form. |
| `Sidereal.md` | quote-format | Two distinct verses (I.6 and II.9) are concatenated inside one quote block with a single merged attribution; same at L1… |
| `The_108_Solar_Divisions.md` | organization | 925-line enumeration with no framing prose and no source attribution for the pada-by-pada symbolism (Navāṃśa/nakshatra-… |
| `The_360_Phases_of_Sol.md` | citation-error | The entire degree-by-degree symbolism is lifted from Rudhyar's An Astrological Mandala (1973) but the article gives no … |
| `The_360_Phases_of_Sol.md` | redundancy | Two very long machine-generated enumeration tables (360 and 108 rows) sit side by side in the same bundle with near-ide… |
| `The_Solar_Matrix_of_Creation.md` | quote-format | The block quotes at L18, L38 are English-only with no attribution line beneath (no "— Rudhyar, *The Zodiac as the Unive… |
| `The_Solar_Matrix_of_Creation.md` | meta-prose | Opens by referencing "the earlier essay" (Sidereal/The_Zodiac), making the article a sequel that announces its relation… |
| `The_Toroidal_Heart.md` | other | The front-matter banner_image path is repo-root-relative (generated-images/...) while the inline image uses ../generate… |
| `The_Toroidal_Heart.md` | meta-prose | A sentence that talks about the article's own duration/method rather than its subject — the kind of structure-announcin… |
| `The_Toroidal_Heart.md` | tic | Negative-contrast construction; one instance in an otherwise disciplined, primary-source-led article. |
| `The_Zodiac.md` | meta-prose | A run-on thesis sentence that announces the article's dual-lens method before any content, plus an embedded "not the un… |
| `The_Zodiac.md` | tic | Two "not merely" constructions in the Leo entry; the article otherwise uses zero em-dashes and reads cleanly, so these … |
| `The_Zodiac.md` | structural-mirror | Every one of the twelve entries follows an identical three-move skeleton ("Psychologically it is" / "In physical terms … |

### src-astrology (5)

| File | Category | Problem |
|---|---|---|
| `science-and-astrology.md` | tic | Negative-contrast framing in the connective tissue where the positive ('a methodological choice') stands on its own. |
| `science-and-astrology.md` | em-dash-density | Em-dash is the default break device across the editorial connective tissue; line 213 stacks three in a single sentence. |
| `science-and-astrology.md` | meta-prose | Announces the extract's own method ('The aim is to...') rather than beginning with substance; mild but it is the kind o… |
| `astrology-of-personality.md` | tic | Negative-contrast closing sentence on the 'signs as twelve phases' bullet. |
| `astrology-of-transformation.md` | em-dash-density | Editorial connective tissue leans on em-dash asides as the default emphasis device (~12 per 500 prose words). |

### src-lunar-death (3)

| File | Category | Problem |
|---|---|---|
| `hymn-32-to-selene.md` | tic | "Does not merely reflect… she bears" plus the trailing "productive, not derivative" is the negative-contrast pattern; l… |
| `breatharian-witnesses.md` | broken-link | Same stale `LiGoldragon/bibliography` GitHub path that conflicts with the canonical `~/primary/repos/library/` conventi… |
| `giri-bala-the-yogini-who-never-eats.md` | factual-error | Spells the primary text "Khecharīvidyā" (three occurrences) against the canonical "Khecarīvidyā" used in its own siblin… |

### src-yoga-diet (10)

| File | Category | Problem |
|---|---|---|
| `Agni_and_Tapas.md` | tic | Negative-contrast antithesis closing section II. |
| `Apathya.md` | tic | Negative-contrast construction; the same passage recurs verbatim in Fruit_as_Medicine.md L47 (with a positive recast th… |
| `Apathya.md` | citation-error | The saindhava eye-exception is cited with no verse number here, while Salt_Dosage_and_Conditions.md L34/L39/L51 pins th… |
| `water-and-srotas.md` | citation-error | Points the reader at a `LiGoldragon/bibliography` GitHub repo for the source binary, whereas the sibling cross-traditio… |
| `Cooking_and_Agni.md` | tic | Two-sentence negative-contrast opener, the banned signature rhythm, used to open a section. |
| `Fruit_as_Medicine.md` | tic | Negative-contrast antithesis used as a section-closing emphasis device. |
| `quotes.md` | quote-format | These raw-extract files use plain English block-quotes with no `\` hard breaks and a bare attribution line; the canonic… |
| `Raw_and_Cooked_Cross_Tradition.md` | tic | Negative-contrast antithesis; the same "not-borrowing-but-recognition" move recurs at L5 ("The convergence is not borro… |
| `Salt_Dosage_and_Conditions.md` | sodium-naming | Repeated standalone "sodium" used as the intake comparator for the compound; the rule directs standalone-sodium-for-the… |
| `Salt_Dosage_and_Conditions.md` | tic | Triple-fragment negative-contrast hammer; the positive claim (a trace under a grain a day) carries the whole point. |

### water (4)

| File | Category | Problem |
|---|---|---|
| `Aqua_Vitae.md` | factual-error | The count 'Eight corpora' contradicts the ten-item list that follows it in the same sentence (and the article devotes a… |
| `Keep_the_Plasma.md` | structural-mirror | Two articles in the same bundle close on the identical sentence 'The body has already made what it needs', and both als… |
| `Plasma_Recycling_Manual.md` | citation-error | The same source text is transliterated three different ways across the bundle ('Ḍāmara Tantra' vs '*Damar Tantra*' vs u… |
| `Plasma_Recycling_Manual.md` | gloss-missing | Read standalone, this published manual never tells a non-expert that 'plasma' here means the recycled bodily fluid (ras… |

### witnesses (5)

| File | Category | Problem |
|---|---|---|
| `Witnesses_Against_Salt_Ayurveda.md` | quote-format | The English splits a single Sanskrit clause oddly — "pacifies all three *doṣas*" then separately "it alleviates *vāta*"… |
| `Witnesses_Against_Salt_Dharma.md` | gloss-missing | *samādhi*, *maunam*, and *dhyāna* appear for the first time in this article unglossed, strung together for a non-expert… |
| `Witnesses_Against_Salt_Hygienists.md` | organization | The index's "Core Witnesses" column for the Hygienist file omits Colburn and Hoffman, two writers the file treats at se… |
| `Witnesses_Against_Salt_Political.md` | earth-as-planet | "planetary scale" used in the project's own prose to mean worldwide; the house rule prefers terrestrial/universal/world… |
| `Witnesses_Against_Salt_Political.md` | redundancy | Unlike its sibling witnesses files, the Political file is author-argument-dominant with primary sources thin and mostly… |

### xcut-citation (8)

| File | Category | Problem |
|---|---|---|
| `Apathya.md` | citation-error | Apathya.md cites the Vāgbhaṭa salt-excess verse as AH Sū. 10.12–13, while Witnesses_Against_Salt_Ayurveda.md L52 and so… |
| `Cooking_and_Spices.md` | citation-error | This file alone cites the line correctly as 3.2 (Bhṛgu Vallī). Flagged only to mark it as the correct reference standar… |
| `True_Ayurveda.md` | citation-error | The article repeatedly asserts that named texts (Caraka, Suśruta, Aṣṭāṅga Hṛdaya, HYP) support its claims but supplies … |
| `Āyurveda.md` | citation-error | These bold-IAST blocks read as direct Caraka verses but are attributed to a non-locus ("Sūtrasthāna tradition"). Presen… |
| `Ambrosian_Diet.md` | citation-error | The attribution honestly marks it proverbial (good), but the immediately preceding prose at L41 introduces it as "A pro… |
| `Ambrosian_Diet.md` | citation-error | The ghee-praise content (memory, intelligence, agni, ojas ...) corresponds to Caraka Sū. 27.231–233, which the project'… |
| `Yogic_Food.md` | quote-format | This file sentence-capitalizes the first word of each Sanskrit line (Oṣadhībhyo, Annāt, Annaṃ, Vrīhi, Yavāgūḥ, Peya, Hi… |
| `Apathya.md` | citation-error | The heading and attribution both omit the chapter/verse ("Caraka Sū." / "Sūtrasthāna, on the lavaṇa-varga"). Caraka enu… |

### xcut-consistency (1)

| File | Category | Problem |
|---|---|---|
| `In_Praise_of_Agni.md` | doctrine-contradiction | Curd (*dadhi*) and buttermilk (*takra*) are presented as sanctioned raw exceptions in the cooking essays but as prohibi… |

### xcut-organization (7)

| File | Category | Problem |
|---|---|---|
| `.gitignore` | organization | The .gitignore comment points at a stale library path (~/git/bibliography/); AGENTS.md and the workspace AGENTS both na… |
| `Chloride_In_Produce_Evidence_Table.md` | organization | A kind:research data table sits inside the chloride/ article directory rather than in the research/source-extracts scaf… |
| `NaCl_Not_Vegan.md` | organization | The veganism-ethics argument is split across two category dirs: chloride/NaCl_Not_Vegan.md (salt-is-not-vegan) lives un… |
| `Vegan_Dairy.md` | redundancy | Vegan_Dairy.md and NaCl_Not_Vegan.md open with the same premise restated in near-identical words. The shared 'veganism … |
| `ghee-banner.png` | organization | generated-images/ghee-banner.png is a superseded v1 banner that no article or manifest entry references — only ghee-ban… |
| `My_Mothers_My_Sisters.txt` | organization | The teasers/ directory is undocumented and unintegrated: two .txt teaser blurbs exist for two of the ~90 articles, tied… |
| `Vajrolī.md` | organization | The yoga-tantra/ category is a near-empty bucket (one article) while genuinely yoga/tantra-themed material is scattered… |

### yoga-tantra+personal (10)

| File | Category | Problem |
|---|---|---|
| `Age_of_Saturation.md` | weak-closing | The closing is a three-beat 'It was never X. It was merely Y.' negative-contrast restatement rather than a clean aphori… |
| `Dharma_by_Annie_Besant.md` | organization | A full verbatim reproduction of another author's lecture sits in 'personal/' alongside original essays with no editoria… |
| `Longevity.md` | tic | One clear instance of the 'not X but Y' construction in the article's own prose; isolated rather than pervasive, but it… |
| `Longevity.md` | factual-error | The '200 years of age' claim and its attribution to McCarrison are extraordinary and likely a garbled secondary citatio… |
| `Notes.md` | sodium-naming | Minor consistency: 'Ayurveda' lacks the macron used project-wide ('Āyurveda'), 'ie' should be 'i.e.', and ' - ' is used… |
| `Olivier_Francoeur.md` | other | Publishing a named person's natal-chart shorthand in a public collection is a privacy concern regardless of essay quali… |
| `Physical_Mortality_and_Essential_Immortality.md` | tic | The clipped numeric-fragment refrain ('Three X. One Y.') recurs at the close of nearly every section, becoming a mechan… |
| `Psyche_and_Machine.md` | tic | One clear instance of the 'no longer X. It is Z.' negative-contrast closing construction; the rest of the piece is most… |
| `The_Pressure_of_Being.md` | symbology-inversion | Minor: the bullet thread restates each quote, which is the trailing-summary pattern the house style discourages; no doc… |
| `Vajrolī.md` | weak-closing | The final sentence is a three-clause summary restatement ('where...where...where...') of the whole essay rather than an… |

## Synthesis (lead-editor narrative)

## Executive summary

The Book of Sol is the work of a writer who has found a real voice and a coherent cosmology, and who has assembled an unusually deep bench of primary sources to carry it. The strongest articles — `sol-luna/The_Toroidal_Heart.md`, `ghee/Ghee.md`, `sol-luna/2-Luna.md`, `ayurveda/Cooking_and_Spices.md`, `personal/Physical_Mortality_and_Essential_Immortality.md`, and most of the `chloride/witnesses/` series — read as finished craft: orientation, then the rishi brought forward, then a turn that lands. The doctrine is, on the whole, remarkably consistent across ninety-odd files. The salt position holds (none as food, only a minuscule medicinal trace of saindhava); the cooked-first principle and its sanctioned raw exceptions are stated in near-identical language wherever they recur; the mitāhāra citations have settled into two distinct, correctly-attributed verses; no surviving B-12 or deficiency-as-evidence argument was found anywhere in the corpus. That is a real achievement and the foundation the rest of this audit stands on.

What most needs attention is narrower than the 312 findings suggest, because the findings concentrate. Three things matter first. The signature negative-contrast tic — "X is not Y. It is Z." — is live on published Substack pages, including the two articles the house guide itself holds up as reference voices (`chloride/The_Chloride_Indictment.md` and `cosmology/All_Instruments_Measure_a_Level_Earth.md`), where it has become the default rhythm rather than an occasional slip. The Sanskrit citation layer has two systemic faults that propagate through the source-extracts into the articles that quote them: a six-file Taittirīya misattribution (3.2 cited as 2.2.4) and a recurring practice of setting invented or unlocatable Sanskrit in the bold format reserved for attested verse, worst in `ayurveda/Āyurveda.md`. And a handful of unfinished private fragments and a privacy exposure are linked live from the public index. None of these is hard to fix; all of them are visible to a reader on the first page they touch.

What is already clean deserves saying plainly, because it bounds the work. Earth-as-planet is clean in the project's own prose across every bundle (the "planet" hits are all quotations or refer to actual planets). Micronutrition vocabulary is almost everywhere used to reject the category, which the rules permit. The doṣa/guṇa symbology is sound — ghee descends, gathers, binds, settles; vāta's dryness is named only as the condition remedied — with exactly one genuine inversion to fix. Smart quotes and horizontal rules are absent but for two stray cases. The book's bones are good. The work ahead is finishing, not rebuilding.

## Systemic style themes

### 1. Negative-contrast ("X is not Y. It is Z.") — the dominant defect, and it is on published pages

This is the single most frequent and most consequential craft problem, and the house guide names it the one thing to eliminate. It recurs in every bundle. The acute cases are the published anchors, where it has hardened into the article's governing rhythm rather than appearing once.

Worst offenders, in order of how much they matter:
- **`chloride/The_Chloride_Indictment.md`** (published, and the named reference for the "clinical summary voice") runs the pattern a dozen-plus times, with a four-bullet hammer in the Verdict — "Chloride is not an electrolyte of ordinary nutrition. It is an inorganic mineral... Chloride does not merely poison; it addicts." — and closes on it: "*Chloride is not salt. Chloride is chloride.*"
- **`cosmology/All_Instruments_Measure_a_Level_Earth.md`** (the sole published cosmology piece): "This is not a caricature of the textbook position. It is the textbook position" and "This is not a fringe claim. It is the first operation in every manual ever written for the craft."
- **`personal/Age_of_Saturation.md`**: ~10 instances in 484 words — "descriptive, not metaphorical," "thermodynamic, not moral," "it is not fought" — the pattern is the entire prose texture.
- Also pervasive in `ghee/Ghee_Restored_my_Vitality.md` (the "Not A. Not B. Not C." fragment cascade), `ayurveda/Mechanical_Purging.md`, `ayurveda/Fidelity_of_Transmission.md`, `diet/Vegan_Dairy.md` (built on it from title to close), `sol-luna/Celestial_Name.md`, `sol-luna/Kali_Yuga.md`, `political/Cheap_Talk.md` ("Maps are not roads. / Constants are not machines."), and the research index thesis ("Yoga and Āyurveda are not cousins, not siblings, but two faces of a single lineage").

The fix is uniform: state the positive, delete the denied alternative, and reserve the trailing-concession form ("X is Z, not Y") for the rare case where the denied term carries real information. The irony worth naming: the argument's content is usually *unity, sameness, restoration* — and the writer keeps reaching for antithesis to express it. A single pass converting these to positive declaratives would lift the whole book.

### 2. Quote-block format non-compliance — the second systemic fault, concentrated in the Sanskrit-heavy bundles

The canonical block (bold IAST → blank `>` line → English in double quotes → em-dash attribution last) is followed correctly by the reference articles and broken almost everywhere else, in several distinct ways at once. `diet/Penultimate_Sāttvic_Food.md` violates it on four counts (citation before the Sanskrit, no separator, quoted IAST, italic English). `ayurveda/Mechanical_Purging.md`, `chloride/Inorganic_Minerals.md`, and `water/The_Distilled_Water_Paradox.md` (published) strip the attribution entirely or invert quote-mark placement. `ghee/Ghṛta_Golden_Magic.md` and `political/The_Duty_You_Cannot_Refuse.md` wrap the Sanskrit in quotes and leave the English bare. `yoga-tantra/Vajrolī.md` breaks all eleven of its blocks identically. The pattern is bimodal: the polished articles know the form; everything else ignores it. A mechanical normalization pass would close most of these.

### 3. Em-dash density — over the ceiling on three published pages

The ~5-per-500-words ceiling is exceeded by roughly 2x on `cosmology/All_Instruments_Measure_a_Level_Earth.md`, `diet/In_Praise_of_Agni.md`, and `diet/Dehydrated_Fruit_Coconut_Honey.md` — all published — plus `ayurveda/Agni.md`, the `chloride/witnesses/` Ayurveda/Chinese/Yoga files, and the heavier research notes. The em-dash has become the default emphasis device, stacking three and four per paragraph. This is the most material density issue on shipped pages.

### 4. Glossing gaps — load-bearing terms left cold

Recurs across bundles but the failure is local: the central term of an article goes unglossed on first use. `ghee/Ghee_Restored_my_Vitality.md` never glosses śivāmbu or amarolī though the whole argument rests on them; `yoga-tantra/Vajrolī.md` never defines bindu, rajas, amarī, or Vajrolī itself; `cosmology/All_Instruments` uses "zetetic" five times cold; `ayurveda/Madhumeha.md` leaves agni, ojas, srotāṃsi, medas unglossed. The reference articles gloss reliably, so the standard exists.

### 5. doṣa/guṇa symbology — one genuine inversion, otherwise sound

The symbology axis is largely clean, which makes the one real error stand out: **`diet/Penultimate_Sāttvic_Food.md`** glosses *guru* as "deeply nourishing," where every other file in the corpus correctly renders it "weighty/heavy" — and where the nourishing connotation is precisely what fruit and coconut are *faulted* for elsewhere. This both mistranslates a core guṇa and inverts the corpus gloss in the one article meant to praise the substance. Fix it to "weighty/heavy" and attribute the nourishing sense to *ojaskara*/*bṛṃhaṇa*.

### 6. Meta-prose and weak closings — structure announced, endings restated

Persistent low-grade tics. Structure-announcing openers ("The essay that follows assembles the witnesses... for a single thesis" in `All_Instruments`; "Herein lies a cohesive guide... as gleaned from" in `political/The_Warrior.md`; the "Let us begin / Consider next / Let us ask" scaffold in `political/On_Anthropic.md`; "this article holds steady in for the length of its reading" in both `The_Toroidal_Heart.md` and `personal/Refinement.md`). Weak closings under literal "## Conclusion" / "Bottom line" headings (`political/The_Idol_of_Wisdom.md`, `sol-luna/Line_of_Sight.md`) restate rather than turn.

## Cross-article inconsistencies

These are the discrepancies that span files — where two articles tell a reader different things, or where the corpus contradicts itself on a citation. Both sides are named.

**The Taittirīya 3.2 / 2.2.4 misattribution (six files).** The line *annaṃ brahmeti vyajānāt* belongs to the Bhṛgu Vallī, Taittirīya Upaniṣad **3.2**. It is cited as **2.2.4** in `diet/Ambrosian_Diet.md`, `diet/Yogis_Dont_Eat_Fruit.md`, `diet/Yogic_Food.md`, `source-extracts/Apathya.md`, `source-extracts/Fruit_as_Medicine.md`, and `source-extracts/Cooking_and_Agni.md` — and all six wrongly chain it to the 2.1/2.2 anna-puruṣa passage as if one continuous section. The project itself proves the error: `ayurveda/Cooking_and_Spices.md`, the named reference implementation, cites it correctly as 3.2. Fix the two source-extracts and the article repeats follow.

**The throat-well sūtra: 3.30 vs 3.31.** *kaṇṭhakūpe kṣutpipāsānivṛttiḥ* is cited as Yoga Sūtra **3.30** in the published `diet/Ambrosian_Diet.md` and **3.31** in `diet/Fruitarianism.md`. The standard locus is 3.31; the published article carries the error.

**The svastha verse: Suśruta vs Caraka.** *samadoṣaḥ samāgniś ca...* is attributed to *Suśruta Saṃhitā* Sū. 15.41 in `ayurveda/The_Allure_of_Vata.md` and to *Caraka Saṃhitā* Sū. 15.48 in `ayurveda/Apathya.md`, `ayurveda/Agni.md`, and `ayurveda/Cooking_and_Spices.md`. The verse is canonically Caraka; the Suśruta attribution (in a published-voice article) is the outlier of one against three.

**The "navel of immortality" ghee-verse: three wordings, three loci.** `ghee/Ghee.md` gives *ghṛtasya nāma guhyaṁ... amṛtasya nābhiḥ* at RV 4.58.1 (the attested Ghṛta-sūkta); `sol-luna`'s sibling and `diet/Penultimate_Sāttvic_Food.md` give *ghṛtaṃ nabho amṛtasya nābhir* at RV 1.142.3; `diet/Ambrosian_Diet.md` gives *ghṛtasya nābhim amṛtasya dhāma* with bare "*Ṛg-veda*" and no verse; and `source-extracts/Golden_Fountain/...` cites the phrase as RV 1.142.3 against its own verified Rg_Veda extract's 4.58.1. RV 4.58.1 is correct; the flagship ghee-citation cannot all be these at once.

**The salt position — one surviving gap.** `diet/Yogis_Dont_Eat_Fruit.md` (L57) lists saindhava plainly among Caraka's daily-admitted foods *without* the mandatory "minuscule medicinal trace, not a food" caveat that `chloride/The_Chloride_Indictment.md`, `source-extracts/Salt_Dosage_and_Conditions.md`, and `source-extracts/Fruit_as_Medicine.md` attach everywhere else. The fix is a single canonical gloss reused at every salt mention.

**The HYP wholesome-food list — greens recommended or avoided.** `diet/Ambrosian_Diet.md` (L47) quotes paṭola (a fruit) and "five leafy greens" *on* the HYP recommended list one line after asserting "fruit appears nowhere," while `diet/Yogis_Dont_Eat_Fruit.md` puts greens on the *avoid* list and omits paṭola. The two articles characterize the same source list incompatibly.

**Plant "ghee" and ojas — does it build or not.** `ayurveda/The_Two_Pillars_of_Nourishment.md` calls clarified nut/seed/plant oils "smooth, cohesive, and ojas-building" lunar equals of ghee; `ayurveda/Madhumeha.md` states plant oils "do not build ojas and cannot substitute for true ghṛta"; `ayurveda/Apathya.md` and `diet/Fruitarianism.md` place pressed seed oils / *taila* on the apathya list as unstable and inferior. The corpus both endorses and condemns seed-oil fats.

**The mitāhāra / HYP / Gheraṇḍa attribution — resolved, and worth recording as a non-issue.** The corpus has correctly settled: the *snigdha-madhura* definition is HYP 1.58, the no-yoga-without-measure precondition is Gheraṇḍa Saṃhitā 5.16, and the proverbial *hitaṁ mitaṁ ca bhoktavyaṁ* maxim is consistently marked "proverbial formulation." No stale "HYP 1.15 / 1.57" attribution survives in the assigned files. This axis is clean.

**The B-12 / deficiency argument — confirmed absent.** No surviving deficiency-as-evidence argument anywhere. `diet/Vegan.md`'s modern-evidence section argues exclusively from clinical outcomes (blood pressure, stroke, renal, bone); the fruit and raw critiques argue from dhātu-kṣaya / ojakṣaya. The register the project rejects has been kept out.

**The AH salt-group locus drift.** A reconciliation item rather than a reader-facing contradiction: the lead/alkali salt-group is cited as AH 6.147 in `ayurveda/Apathya.md` but AH 10.27 in `chloride/witnesses/Witnesses_Against_Salt_Ayurveda.md` and `source-extracts/Salt_Dosage_and_Conditions.md` (10.27 attested twice, so Apathya's 6.147 is the likely error).

## File & system organization

The architecture is fundamentally sound — ten category directories, a single canonical `_index.md` (with `readme.md` symlink), a clean source-extracts/standalone-library/caraka-samhita boundary that is actually respected on disk, and a principled frontmatter convention (the 19-of-103 YAML files are exactly the published and article-shaped ones, not a haphazard scatter). The debt clusters in five places.

**Index and manifest drift — the highest-value organizational fixes, each breaking a stated invariant.**
- `research_yoga_ayurveda_lineage/00_index.md` links files **04, 05, 08 that do not exist** (three dead links plus a numbering gap). Their planned content has already been absorbed into the five files that do exist; the fix is to delete the entries and two internal forward-references, not to write new files.
- The source-extracts indexing in `_index.md` is half-curated: **14 extracts are unlinked**, including `source-extracts/Surveying_Instruments_And_The_Shape_Of_The_Earth.md`, which the published cosmology article names as its companion. There is no consistent rule for which extracts appear.
- `cosmology/All_Instruments_Measure_a_Level_Earth.md` is `publish: true` but **absent from `.substack-posts.json`** and has no banner — the pipeline cannot ship it as configured.

**Stub files live in the public index.** `personal/Notes.md` (a three-bullet scratch outline) and `personal/Olivier_Francoeur.md` (three lines of astrology glyphs about a *named private individual*) are linked from the public `_index.md`, against INTENT.md's "public-facing surface, not a private notebook." `personal/The_Pressure_of_Being.md` is a published quote-dump using underscore-rule separators (a banned horizontal rule in disguise, 8×). De-list the first two until written; the Olivier file is also a standalone privacy exposure.

**Redundant / overlapping articles.** Two clusters duplicate rather than divide labor: (a) `chloride/Minerals.md` and `chloride/Inorganic_Minerals.md` argue the identical ash/"life cannot eat the dead" thesis with overlapping Caraka citations — merge candidates; (b) the veganism-ethics premise is restated near-verbatim across `chloride/NaCl_Not_Vegan.md`, `diet/Vegan.md`, and `diet/Vegan_Dairy.md`, split across two directories. Separately, the narcotic argument recycles the same five hygienist quotes across `chloride/Chloride_Extrapolation.md` (whose filename does not even match its H1), `chloride/Chloride_the_Narcotic.md`, and `chloride/Chloridism.md`; `political/Twitter_is_Obsolete.md` and `political/Obsolete_Social_Medias.md` share verbatim paragraphs; `political/The_Duty_You_Cannot_Refuse.md` and `political/My_Mothers_My_Sisters.md` share the entire vegan-decoy argument and Gītā set.

**Two long enumeration files read as data dumps.** `sol-luna/The_360_Phases_of_Sol.md` (449 lines, no H1, no References for derivative Rudhyar content) and `sol-luna/The_108_Solar_Divisions.md` (925 lines, no orientation, no provenance, plus an off-by-one pada-range error at the Leo/Virgo boundary) strain the "each subject invents its own form" rule. They want short essay heads or relocation to an appendix.

**Source-extract indexing policy, naming, research-dir gaps, category cut.** The source-extracts listing needs one deliberate policy — list every extract an article cites, or list none — rather than the current half-and-half. The `yoga-tantra/` directory is a one-article bucket while yoga-themed material lives in `diet/` and `chloride/witnesses/`. The `teasers/` directory and a superseded `generated-images/ghee-banner.png` v1 are undocumented orphans. `chloride/Chloride_In_Produce_Evidence_Table.md` (`kind: research`) sits inside an article directory.

**AGENTS.md self-staleness.** The rule doc has fallen behind its corpus on two points: **L80** still names `chloride/witnesses/Witnesses_Against_Salt_*.md` and `ayurveda/Āyurveda.md` as exemplars of the retired citation-between-Sanskrit-and-English pattern, but those files have already been migrated to the correct attribution-last form — so the guide now points future editors at compliant files. And the **`.gitignore`** comment routes book binaries to the stale `~/git/bibliography/` instead of the canonical `~/primary/repos/library/`.

## Prioritized remediation plan

1. **Strip negative-contrast from the published Substack pages first.** Full pass on `chloride/The_Chloride_Indictment.md` (the dozen body instances, the four-bullet Verdict hammer, the closing aphorism) and `cosmology/All_Instruments_Measure_a_Level_Earth.md` (L16, L113, and the L21 structure-announcing meta-frame). These are live, and both are the guide's own reference voices. Convert each to the positive claim; keep at most one trailing concession.

2. **Bring the other published pages to the hard rules.** Fix the published citation errors: Yoga Sūtra **3.30 → 3.31** in `diet/Ambrosian_Diet.md`, and that file's unquoted-English quote blocks; reduce em-dash density to under the ceiling on `cosmology/All_Instruments`, `diet/In_Praise_of_Agni.md`, and `diet/Dehydrated_Fruit_Coconut_Honey.md`; correct the `diet/Penultimate_Sāttvic_Food.md` *guru* gloss to "weighty/heavy"; rebuild the malformed quote blocks in `water/The_Distilled_Water_Paradox.md` and fix its "on the planet"; correct the standalone "sodium" in `chloride/The_Chloride_Indictment.md` L101 to "chloride."

3. **Remove the public-surface liabilities now.** De-list `personal/Notes.md` and `personal/Olivier_Francoeur.md` from `_index.md` (the latter is also a privacy exposure of a named individual's natal chart); replace the underscore horizontal rules in `personal/The_Pressure_of_Being.md`; add the `.substack-posts.json` entry and banner for the published `cosmology/All_Instruments`, or set it `publish: false` until ready.

4. **Fix the two systemic citation faults at their source.** Correct *annaṃ brahmeti vyajānāt* from **2.2.4 to 3.2** in the two source-extracts (`Apathya.md`, `Fruit_as_Medicine.md`, and `Cooking_and_Agni.md`), letting the article repeats follow, and un-chain it from the 2.1/2.2 passage. Then locate-or-demote the invented/unlocatable Sanskrit set in bold-verse format, worst in `ayurveda/Āyurveda.md` (the unattributed *amṛtasya nāma yad brahma* block and the "after Caraka tradition" couplets) — either pin a real chapter.verse or stop using the primary-verse bold that makes fabricated lines indistinguishable from attested ones.

5. **Run the corpus-wide style sweeps.** One negative-contrast pass across the high-density unpublished offenders (`personal/Age_of_Saturation.md`, `ayurveda/Mechanical_Purging.md`, `ayurveda/Fidelity_of_Transmission.md`, `ghee/Ghee_Restored_my_Vitality.md`, `diet/Vegan_Dairy.md`, the research thesis lines). One quote-format normalization pass converting every non-compliant block to the canonical shape. One gloss pass adding first-use English for the load-bearing terms in `yoga-tantra/Vajrolī.md`, `ghee/Ghee_Restored_my_Vitality.md`, and `ayurveda/Madhumeha.md`.

6. **Reconcile the doctrinal splits with one canonical sentence each.** Adopt a single reused gloss for saindhava ("a minuscule medicinal trace by indication, not a food") and add it at the bare mention in `diet/Yogis_Dont_Eat_Fruit.md` L57; settle whether plant "ghee" builds ojas (`Two_Pillars` vs `Madhumeha` vs `Apathya`); reconcile the HYP greens-recommended-vs-avoided characterization between `Ambrosian_Diet` and `Yogis_Dont_Eat_Fruit`; settle the svastha verse on Caraka 15.48 and the ghee-verse on RV 4.58.1 everywhere.

7. **Close the organizational debt.** Resolve the `research_yoga_ayurveda_lineage/00_index.md` dead links (delete 04/05/08 entries and their forward-references); set one source-extract indexing policy and add the cited-but-unlinked extracts (starting with `Surveying_Instruments`); merge the two minerals essays and consolidate the veganism premise; refresh AGENTS.md L80 and the `.gitignore` path comment; relocate the orphan research note and document or remove `teasers/` and the superseded banner.

The book already knows the difference between what nourishes and what merely fills. Let the prose follow the doctrine: say what a thing is, and let the rishis carry the rest.

## Per-bundle auditor notes

### sol-luna

OVERALL IMPRESSION. The sol-luna bundle splits cleanly into two registers. The strongest articles — The_Toroidal_Heart, 2-Luna, and Sidereal — are primary-source-dense, glossed, and largely obey the house voice; The_Toroidal_Heart in particular is the bundle's reference-quality piece (correct IAST+transliteration quote blocks, trailing em-dash attributions, disciplined em-dash density of ~32 prose dashes across ~2,400 prose words = well under 5/500, and a genuinely aphoristic close \"The body is at home\"). The weakest are the two giant enumeration tables (The_108 at 925L, The_360 at 449L), which read as generated data dumps with no framing prose and no provenance, and Celestial_Name + Solar_Excess + Kali_Yuga, which lean on the banned negative-contrast tic as a default rhythm.

QUALITY RANKING (best to worst):
1. The_Toroidal_Heart.md — reference-grade; only nits (one meta-prose sentence L23, one \"not by X but Y\" L68, a banner-path mismatch, and a factual-overreach on the bodily nodal cycle).
2. 2-Luna.md — excellent voice and source density; two negative-contrast instances and an unglossed/under-styled \"shivambu\".
3. Sidereal.md — clean and well-sourced, but the index calls it \"Sidereal\" while it is actually \"Zodiac and Nakṣatras\" (title/content mismatch), and it merges multiple verses under single attributions.
4. The_Zodiac.md — internally consistent and tic-light (zero em-dashes), but rigidly mirror-structured across all 12 signs and opens with a method-announcing run-on.
5. 1-Sol.md — short, liturgical, strong; English-only Gītā quote misses the IAST form its siblings use.
6. The_Solar_Matrix_of_Creation.md — good Rudhyar synthesis but sequel-framing meta-prose (\"the earlier essay\"), two negative-contrasts, and unattributed block quotes.
7. Line_of_Sight.md — the flat-earth/curvature brief; carries the project's stance but is built as an example-dominated debunking table with head-of-block citations and a \"Bottom line\" summary close. Doctrinally consistent with the project's stationary-Earth framework (not flagged as doctrine-contradiction), but structurally the audit/ledger shape the house style cautions against.
8. Kali_Yuga.md — substantive practice but tic-saturated (3+ negative-contrasts), bold-wrapped H1, lazy ordered-list numbering, and unglossed prāṇa/Amarolī.
9. Celestial_Name.md — published, sweeping cross-cultural piece, but opens on a stacked negative-contrast and uses the pattern 3+ times; tight (unspaced) em-dashes are a Word/ChatGPT export artifact inconsistent with the rest of the bundle.
10. The_108_Solar_Divisions.md — useful as a reference, but no H1 intro, no source attribution, and a pada-range off-by-one at the Leo/Virgo boundary (Pada 46 claimed by both headers).
11. The_360_Phases_of_Sol.md — opens with prose before any H1 (no H1 at all), structure-announcing blurb, and the entire Sabian-Symbol/Rudhyar content carries no References despite being directly derivative of An Astrological Mandala.

EARTH-AS-PLANET (Rule 6): CLEAN across the bundle. Every \"planet\" reference checked is either the five visible planets, a quotation of another author (Sūrya Siddhānta, Bṛhat Parāśara, Rudhyar), or the adjective \"planetary\"/\"planetary Mind\" in Sabian symbolism — none refer to Earth as a planet. The Toroidal_Heart and Solar_Matrix both correctly treat Earth as the stable center/disk, not a planet.

SODIUM / MICRONUTRITION (Rules 3-4): CLEAN. No sodium-naming issues and no micronutrition vocabulary in this bundle; Solar_Excess argues correctly from Āyurvedic mechanism (ojas, vāta, dhātu) and directly-shown outcomes (tissue consumption) rather than nutrient categories.

SYMBOLOGY (Rule 5): Solar_Excess handles the lunar/ghee symbology CORRECTLY — ghee is described as descending, binding, coating, building ojas (all lunar/cohesive verbs), and \"Vāta rises\" names the aggravating quality as the condition being remedied, which the rule explicitly permits. No symbology inversion found in the bundle.

ORGANIZATION OBSERVATIONS. (a) The two enumeration files (108, 360) would benefit from being reframed as appendices/data with short essay heads, or at minimum given orientation paragraphs and References; as published they strain the \"each subject invents its own form\" rule by being near-identical repetitive lattices. (b) The Sidereal index-title mismatch is the one outright index defect new to this bundle (not in the orchestrator's pre-cataloged list). (c) The_360 having no H1 is a structural outlier — every other bundle file leads with a heading. (d) Front-matter is present only on The_Toroidal_Heart (publish:false, consistent with its absence from the substack registry); the other eleven carry no front-matter, which is fine for unpublished essays. (e) The 108-divisions Leo/Virgo pada-range overlap (Pada 46) is a genuine internal-consistency error worth a verifier's eye.

CROSS-CUTTING TIC NOTE. The negative-contrast pattern is the dominant defect of this bundle, concentrated in Celestial_Name, Kali_Yuga, Solar_Excess, and Solar_Matrix. None of these crosses into the triple-fragment hammer except Kali_Yuga's close, but several articles use the pattern as a recurring rhythm (3+ times) and per the rule-of-thumb warrant a full editorial pass rather than spot fixes.

### cosmology+surveying

Overall impression: the bundle is strong, careful work. The long source-extract (Surveying_Instruments..., 888L) is the best file here — its OWN prose (Frame, section intros, the section-IX Synthesis) is disciplined, documentary, and clean of the banned filler/tic phrases; the high filler+tic candidate counts the mechanical sweep flagged are almost entirely INSIDE the verbatim quotations ("notably," in Carpenter's Proof 4, "the fact that" in cited passages, etc.), which are exempt as preserved source wording. I found no genuine tic/filler violation in the extract's authored prose; its only real issues are the empty Garwood subsection and the Frame listing Garwood as a quoted source it never extracts.

Quality ranking (best to weakest on house-rule adherence):
1. source-extracts/Surveying_Instruments_And_The_Shape_Of_The_Earth.md — exemplary documentary discipline; quotes carry the argument exactly as the project wants; only the Garwood placeholder mars it.
2. cosmology/Computing_vs_Measuring_The_Curve.md — tight, technical, almost no tics (one "is not circular" is benign); clean structure. Unpublished note.
3. cosmology/Horizon_Dip_vs_Altitude.md — substantively sharp but carries a banned "not merely... but" close, an em-dash density ~2x the ceiling, a self-referential edit-history clause, and a title/filename mismatch. Unpublished note, so lower stakes.
4. cosmology/All_Instruments_Measure_a_Level_Earth.md — the one PUBLISHED article and the weakest on the prose rules: two instances of the single-most-banned "X is not Y. It is Z." pattern (lines 16, 113), explicit structure-announcing meta-prose (line 21 "The essay that follows assembles the witnesses... for a single thesis"), em-dash density ~1.7x the ceiling (48 em-dashes / 2764 prose words), a quote-format deviation across all ~20 blocks (missing the trailing `\` hard break the reference implementation uses), an unglossed load-bearing term ("zetetic"), and a closing coda that restates rather than turns. None of these touch the chloride/micronutrition/dosa-symbology rules (not in scope for cosmology), and the Earth-as-planet rule is clean — all three "planet" occurrences are inside exempt verbatim quotations.

Organization observations: Earth-as-planet (rule 6) is fully clean in authored prose. The two cosmology orphan notes (Computing, Horizon_Dip) are publish:false working notes, so their absence from _index.md is expected, not a defect — but note the orchestrator already cataloged them as orphans. A deeper coherence question for the psyche: the cosmology section publishes ONLY the flat-earth thesis (All_Instruments) while keeping the two notes that lay out the globe model's strongest measured-curve rebuttal (arc measurement, triangle excess, reciprocal leveling, the √h dip) unpublished. Whether that asymmetry is the intended editorial posture (settled thesis vs. open zetetic inquiry) is an intent-level decision, flagged as low-severity doctrine-contradiction. No broken links beyond those the orchestrator listed; the companion-file cross-link in All_Instruments (line 186) resolves correctly to the source-extract.

### chloride-top

SCOPE: 10 top-level chloride articles. Only The_Chloride_Indictment.md is publish:true; the rest are drafts (Chloride_In_Produce_Evidence_Table.md is publish:false/kind:research). I did NOT re-report the orchestrator's confirmed mechanical items (the produce-table index orphan, broken links, the sodium-chloride sanctioned exceptions in Chloridism/Indictment Section II), except where a NEW angle applies.

HEADLINE FINDING: The published anchor, The_Chloride_Indictment.md, is the single worst offender against Rule 7 (negative-contrast 'X is not Y. It is Z.'), the rule AGENTS.md calls 'the single most important thing to avoid.' It carries 12+ such constructions in body prose plus a four-bullet hammer in Section X and a negative-contrast closing aphorism. This is acute because AGENTS.md L163 holds this exact file up as the 'clinical summary voice' reference implementation — the model article is violating the headline rule. This should be the top remediation priority. Em-dash density, by contrast, is FINE: 27 em-dashes over ~3487 words of body prose = ~3.9/500, under the ~5 threshold (the 24 em-dashes in the References block are citation separators, correctly excluded). The one real sodium-naming violation in the Indictment is L101 'whose entire daily sodium' (Section VII, outside the sanctioned Section II contrast). The other 19 'sodium' instances flagged upstream are all either 'chloride of sodium' (sanctioned), 'sodium bicarbonate/citrate' (legitimate compound names), Romance-language quotes, scare-quoted critiques, or citation titles — NOT violations.

NaCl_Toxicity 'sodium' count (24) is almost entirely legitimate: in ion-substitution trials 'sodium' correctly names the Na+ cation held constant across anions — this is the ONE context where standalone 'sodium' is right. Only 'sodium loads'/'sodium content' (L23/L25) flirt with the flagged shorthand; low severity.

REDUNDANCY (your specific ask): Minerals.md and Inorganic_Minerals.md are substantially overlapping — both argue inorganic-mineral-as-jaḍa/ash, both cite Caraka, both resolve via amarolī/plasma. They need explicit division of labor or a merge. SEPARATELY, Chloride_Extrapolation.md, Chloride_the_Narcotic.md, and Chloridism.md form a THREE-way narcotic-argument cluster that recycles the same five hygienist quotes (Bouchon/Cummins/Liebig/Drew/Hoelzel) and the same skeleton (linguistic framing → narcotic pattern → witnesses → burden-of-proof). Chloride_Extrapolation.md is the weakest of these: its filename ('Extrapolation') doesn't match its H1 ('the quiet narcotic'), and its core 'monotonic-extrapolation-to-zero' argument is also made better and more tightly inside the Indictment (Section VII). Recommend one canonical home for the hygienist witnesses and demoting/merging Extrapolation.

QUOTE-FORMAT: The drafts diverge from the canonical block structure. Inorganic_Minerals.md (5 blocks) omits the blank '>' line, unquotes the English, and omits the em-dash attribution entirely. Chloride_Extrapolation.md (7 blocks) puts attributions in lead-in prose instead of an in-block '— Source' line. Leaving_the_Chloridics.md is mostly correct EXCEPT the 'saṅgaḥ saṁsāra-hetuḥ' block which has NO attribution. Several bold IAST 'quotes' (the constructed Bṛhadāraṇyaka motto in Inorganic_Minerals L9, the unsourced Vedānta maxim in Leaving_the_Chloridics) read as paraphrases/fabrications presented as verbatim verses — they should either be located with chapter.verse or relabeled 'proverbial formulation, after *X*' per Rule 2. I flagged these medium-confidence because I could not verify the Sanskrit against the library; a Sanskritist verifier should confirm.

MICRONUTRITION: Minerals.md uses 'minerals/micronutrition' heavily but to REJECT them (scare-quoted) — Rule 4 explicitly permits this; NOT a violation. The genuine concern is Chloride_In_Produce_Evidence_Table.md, which repeats 'essential micronutrient'/'essential elements' approvingly as plant-science framing rather than naming-to-reject; low severity given it's an internal research note.

SYMBOLOGY: No real inversions found. Chloridism L69 'agitates, dries, and desolates' correctly attributes drying to the aggravating substance (chloride is rūkṣa), and Inorganic_Minerals L49 'ghee... steadies vāta' is correct (guru/snigdha → settling). I included both as low/medium notes only so a verifier doesn't mistake them for inversions.

EARTH-AS-PLANET: none in these files. STRAIGHT QUOTES: clean (consistent with orchestrator). HORIZONTAL RULES: none in these articles (Indictment's YAML front-matter '---' at L1/L7 is front-matter delimiters, not a horizontal rule — not a violation).

QUALITY RANKING (best to weakest):
1. NaCl_Toxicity.md — tightest, most evidence-disciplined, clean dose-response framing; minor sodium-shorthand quibbles only. Excellent companion piece.
2. Leaving_the_Chloridics.md — strong primary-source-led form (Gītā + Castaneda woven), correct quote blocks, good aphoristic beats; one unattributed Sanskrit block to fix.
3. NaCl_Not_Vegan.md — clean, short, logically tight; negative-contrast opener and 'salt is not vegan' frame are the only style debts.
4. The_Chloride_Indictment.md — the most ambitious and best-sourced article, BUT as the published anchor it carries the heaviest Rule-7 tic load and a real sodium-naming slip; high-value, high-priority cleanup. Its quality potential is highest; its current rule-compliance is among the lowest.
5. Minerals.md — vivid ash/combustion conceit, good aphoristic close ('Plasma returned to life remains sovereign'), but redundant with Inorganic_Minerals.
6. Chloridism.md — solid linguistic primary, but 'not merely... but' tics and overlap with the narcotic cluster.
7. Inorganic_Minerals.md — good doctrine, but 5 malformed quote blocks and unglossed/possibly-fabricated Sanskrit drag it down.
8. Chloride_the_Narcotic.md — competent but duplicative; negative-contrast closing.
9. Chloride_Extrapolation.md — weakest article: title/filename mismatch, heaviest redundancy, recycled quote set, summarizing close. Candidate for merge or deletion.
10. Chloride_In_Produce_Evidence_Table.md — fine AS a research note (and labeled as such), but imports the rejected micronutrition register and sits orphaned from the articles that depend on its premise.

### witnesses

QUOTE-PATTERN VERDICT (the bundle's central question): All nine per-tradition witnesses files use the CORRECT attribution-at-end pattern. Every primary-source block with IAST runs bold Sanskrit -> blank `>` line -> English in double quotes with `\` hard breaks -> em-dash attribution on the final line (Āyurveda L17-20/45-52/71-76/80-87, Yoga L15-19/27-31, Greek L17-25, Hebrew L15-20 and throughout, Gītā in Dharma L15-19, Damar Tantra blocks are English-only with end-attribution as permitted). NONE places the citation between the Sanskrit and the English. AGENTS.md line 80 is therefore STALE for the witnesses series and should drop the `chloride/witnesses/Witnesses_Against_Salt_*.md` reference (reported as a finding against AGENTS.md). The two ayurveda/ files named on that line are outside my bundle and should be checked separately.

OTHER MECHANICAL CONFIRMATIONS: No `---` rules, no curly quotes, no literal "sodium chloride" in any witnesses file (the only "chloride of sodium" usages are correct). English-only paraphrase blocks (Chinese Ch.5/74/Lingshu, Damar Tantra, Suśruta, Graham/Shelton/Trall/Colburn/Hoffman/Thoreau/Rush) are correctly handled. No micronutrition vocabulary or deficiency-arguments — the series argues from clinical outcomes (teeth, bones, hair, thirst, wasting, longevity) and Āyurvedic/Chinese mechanism throughout, exactly as the rule wants; "iron-deficiency anemia" at Ayurveda L105 is used only to gloss the classical *pāṇḍu-roga* category, not enlisted as evidence, so it is allowed. No symbology-inversion in the witnesses prose (the action-words honor the doṣa direction; the one questionable line is inside a translated quote block, flagged low).

QUALITY RANKING (cleanest to most-in-need-of-work):
1. Witnesses_Against_Salt_Hebrew.md — best in bundle. Disciplined em-dash use (1.67/500w), scripture carries the argument, the covenantal-exception section pre-empts the obvious objection, strong aphoristic closings ("Scripture knows which way salt normally works."). Reference-quality.
2. Witnesses_Against_Salt_Dharma.md — lean (1.56/500w em-dashes), well-glossed, the aluṇa-vrata gradient is genuinely illuminating; only the L56 unglossed samādhi/maunam/dhyāna cluster mars it.
3. Witnesses_Against_Salt_Hygienists.md — long but the long Graham/Shelton verbatim blocks justify it; primary sources dominate as intended; the index undercounts its witnesses (Colburn, Hoffman).
4. Witnesses_Against_Salt_Greek.md — strong material (Homer, Plutarch, Pythagoras) but carries the "not merely" tic (L42), a filler "The phrase is surgical," and the Diogenes paraphrase-as-quotation; em-dash heavy (7.2/500w).
5. Witnesses_Against_Salt_Tantra.md — short and focused but only English paraphrase quotes (no IAST), one "not merely" tic (L7), and a high em-dash rate for its length.
6. Witnesses_Against_Salt_Chinese.md — rich (the nine-character Suwen line is a highlight) but em-dash-saturated bullet glosses (8.5/500w).
7. Witnesses_Against_Salt_Yoga.md — solid source coverage but carries the bundle's one HIGH tic (L51 "salt is not a dietary inconvenience. It is a moral obstruction") and high em-dash density.
8. Witnesses_Against_Salt_Ayurveda.md — the AGENTS.md-named reference implementation for the series, and the quote-format is indeed clean, but it is the most em-dash-saturated (9.7/500w) and has a muddled translation at L84-87.
9. Ancient_Witnesses_Against_Salt.md (index) — useful map, but the Eight/Nine count contradiction (title + "The Eight Files" heading vs a nine-row table) is a visible error a reader hits immediately.
10. Witnesses_Against_Salt_Political.md — the weakest fit to the series' form. At 4330 words it is nearly the length of the other nine combined per-section, yet it is author-thesis-dominant with only four thin paraphrased sources; it repeats the "anti-solar narcotic / pharmacology of compliance" claim across four sections, miscounts its own cases ("five" then lists six), and uses "planetary scale." It reads as a standalone polemic essay grafted into a quote-book, against "let primary sources do the heavy lifting."

ORGANIZATION OBSERVATIONS: (a) The index file's self-count is wrong and should be fixed alongside AGENTS.md L80. (b) Series cohesion is otherwise excellent: each file opens with a register-specific framing, runs orientation -> source -> minimal commentary, and closes with a "Convergence" + "Sources" + cross-link footer; the structural sameness is by design here (a compilation series) and reads as a feature, not the banned "structural mirroring," EXCEPT that the repeated "Convergence" closing section across all nine plus the parent's own "The Convergence" risks formula fatigue — consider varying the final-section heading. (c) The Political file is the structural outlier and would benefit most from being re-shaped toward the series form or split (a short Political witness entry + a separate full essay elsewhere in the collection for the anti-solar-narcotic thesis).

### ayurveda

Bundle ayurveda, 15 files audited in full against AGENTS.md.

PUBLISH STATE drives severity: only Apathya.md and Cooking_and_Spices.md carry publish:true. Honey_and_Fire.md and The_Allure_of_Vata.md are publish:false; the other 11 files have NO frontmatter at all (Agni, Madhumeha, Mechanical_Purging, Medical_Bleeding, Nourishment_in_Kali_Yuga, The_Two_Pillars, Triphala, True_Ayurveda, Āyurveda, Fidelity_of_Transmission, Lineages_of_Science). Because the rubric reserves 'high' for hard-rule breaks on PUBLISHED articles or factual/citation/doctrine errors, most quote-format and tic breaks land at medium even where egregious. The one high-severity finding is the cross-article citation contradiction on the svastha verse (Suśruta Sū. 15.41 in The_Allure_of_Vata vs Caraka Sū. 15.48 in three other files) — a verifiable factual inconsistency that survives into a clean published-voice article.

QUALITY RANKING (best to worst against the reference voice):
1. Cooking_and_Spices.md — the reference anchor; clean quote blocks, source-dense, only minor not-Y residue.
2. Apathya.md — the other anchor; excellent text-tour and gloss discipline, but undercut by (a) structure-announcing meta-prose openers and (b) the whole-article 'audit of one recipe' frame that AGENTS.md L138 explicitly warns against. Strong but not flawless as an exemplar.
3. Honey_and_Fire.md — quiet, well-cited, canonical quote blocks; the best of the unpublished set. Should probably be published.
4. The_Allure_of_Vata.md — ambitious, well-structured, disciplined em-dash use; marred by the 15.41/15.48 citation conflict and a missing banner.
5. Agni.md — rich and largely source-grounded but over the em-dash ceiling (~8.7/500 words), with a recap closing section and a 'not merely' tic.
6. Āyurveda.md — quote format now compliant (retired-pattern flag at AGENTS.md L80 is STALE), but leans on unverifiable 'proverbial formulation, after Caraka tradition' pseudo-verses and one unattributed block.
7. True_Ayurveda.md — coherent thesis, no quote blocks, antithesis-driven; L80 flag also stale (it has no mid-block citations because it has no blocks).
8. Nourishment_in_Kali_Yuga.md — interesting argument but every quote is un-blocked, truncated locators, and the intention-upgrades-industrial-ghee thesis contradicts the bundle's ghṛta doctrine.
9. The_Two_Pillars_of_Nourishment.md — a designated framework anchor (AGENTS.md L195) with ZERO primary sources, and it contradicts Madhumeha on whether plant 'ghee' builds ojas.
10. Madhumeha.md — reads as a prescriptive cure-protocol (dose schedules, daily regimen) with no sources; genre mismatch with the house voice.
11. Lineages_of_Science.md — unsourced Anunnaki / great-white-pyramid / Toltec lost-civilization assertions stated as fact; speculative register that drags the bundle; quote format wrong throughout.
12. Triphala.md — 21-line fragment, three unsourced couplets, reads as a draft.
13. Mechanical_Purging.md — sustained mock-scriptural pastiche built entirely on antithesis; all six 'quotes' lack any citation.
14. Medical_Bleeding.md — short, 'Vedic Testimony' heading over tantric sources, bare English quotes, undefined 'plasma'.
15. Fidelity_of_Transmission.md — 38 bolded spans in 15 lines; bold-as-tic plus relentless X-not-Y; no source quotations at all.

CROSS-CUTTING OBSERVATIONS:
- Quote-format compliance is bimodal: the four frontmatter/reference articles (Cooking, Apathya, Honey, Allure) and Āyurveda.md follow the canonical bold-IAST→blank-`>`→quoted-English→em-dash block; nearly every other file ignores it (no `>` markers, no blank line, no em-dash attribution, bare or missing locators). A single mechanical pass converting all quotes to the canonical block would lift half the bundle.
- The svastha verse and the amarolī (HYP 3.x) citations vary across articles — pin canonical verse numbers once and reuse.
- Doctrinal coherence gap on plant 'ghee': Two_Pillars says clarified plant/nut/seed oils are ojas-building lunar substances; Madhumeha says they 'do not build ojas and cannot substitute for true ghṛta'; Cooking/Apathya treat ghṛta as paramam. Needs one ruling.
- AGENTS.md L80's retired-pattern list (Āyurveda.md, True_Ayurveda.md) is now stale and should be updated — neither still places the citation between Sanskrit and English.
- The symbology rule (5) is respected where tested: Madhumeha's 'vāta dries the tissues' names the doṣa's aggravating action (correct), and 'Ghee anchors vāta, binds ojas' runs with the lunar/snigdha current (correct). No symbology inversions found.
- No earth-as-planet, no curly quotes, no micronutrition-vocabulary or deficiency-argument violations found in this bundle (Madhumeha's 'free from minerals' refers to water purity, not a nutritional argument, so not flagged).
- ORGANIZATION: Lineages_of_Science.md and (to a lesser degree) Medical_Bleeding.md / Fidelity_of_Transmission.md sit in the ayurveda/ directory but are really cosmology/polemic; consider relocating Lineages to a cosmology or 'preserved-science' section. The śivāmbu/plasma articles (Āyurveda, Two_Pillars, Madhumeha, Medical_Bleeding, Mechanical_Purging, Fidelity, True_Ayurveda) heavily overlap and restate the same plasma-recycling thesis — there is room to consolidate to one canonical statement plus focused satellites.

### ghee

QUALITY RANKING (best to weakest):

1. ghee/Ghee.md (PUBLISHED) — the reference-quality piece of the bundle. Etymology-first opening, primary sources carry the argument, doṣa/guṇa symbology is handled exactly right: ghee is shown settling/grounding vāta via snigdha+guru and cooling pitta via śīta, descent is correctly read as the lunar direction of gathering/binding, and nowhere does an action-verb run against the lunar current. Glosses are thorough. Em-dash density is fine once the quote-attribution dashes are excluded. Only nit: the Cārvāka attribution is a school aphorism with no italic source title (low). Calling Jupiter "the planet of wisdom" is EXEMPT — rule 6 bars calling Earth a planet, not Jupiter. No symbology inversion anywhere in this file. Clean to publish.

2. ghee/The_Guṇas_of_Ghṛta.md — nearly as strong. Tight litany structure, correct guṇa naming (cooling, sweet, kindles agni, builds ojas, allays vāta+pitta), good glossing, primary-source dense. One mild "doctrine, not flourish … rather than spoiling" antithesis (L16), not worth a separate finding beyond noting the house dislikes the reflex. Plain headings, macron-correct. This and Ghee.md are the model the other four should be rewritten toward.

3. ghee/Universality_of_Ghee.md — coherent thesis (purity over species) and the inline glossing of madhura/śīta/saumya/ojovardhaka and Ahāra/Vihāra/Manas is good. Weakened by triple repetition of the "pure life → pure milk → pure ghee" chain, a "not because X but because Y" close, a "## Conclusion" scaffold, bolded headings, and "Ayurveda" without macron. The human-milk-ghee passage (L36-47) is speculative but framed as doctrine; thin on primary sources for a universalizing claim.

4. ghee/Ethical_Ghee.md — the weakest on tics: three negative-contrast constructions (L13, L52, L66) push it past the ~3 threshold AGENTS.md sets for a full rewrite pass, em-dash density is ~8/500 (over), headings are all bolded, "Ayurveda" lacks the macron, and the "Modern Ethological Evidence" section defers to animal-welfare science and "nutritive profile" — the modern register rule 4 rejects. Glosses (ama, ojas, vaidyas, sāttvic) are missing. The "Voices of Wisdom" structure is generic and the Tibetan/East-Asian claims are asserted without citation.

5. ghee/Ghee_Restored_my_Vitality.md — strong personal voice but carries the bundle's flagrant tic: the "Not A. Not B. Not C." fragment hammer (L17-21) and a "This is not X. It is Y." standalone close (L49-51). The flagged micronutrition hit ("protein," L9/L20) is technically permitted as naming-to-reject but recurs and the L20 instance is unquoted — tighten to one scare-quoted mention. śivāmbu/amarolī/tamasic are never glossed though they are load-bearing, and the valence of those practices shifts confusingly.

6. ghee/Ghṛta_Golden_Magic.md — the most doctrinally adventurous and the riskiest. It builds a novel action-at-a-distance karmic mechanism (a "golden thread" of gratitude that reaches and relieves an abused cow and remotely reforms the farmer) and presents it as established law, while the two Bhagavadgītā quotes it leans on actually teach only the practitioner's own non-attachment — they do not support field-transmission to the animal. Reads close to rationalizing continued consumption of harm. Both Gītā blocks also break quote-format hard (no blank-line separator, unquoted English, spaceless attribution dash). Negative-contrast is the article's structural habit ("not sentimental," "not into apathy but into radiance," "not excused; rather").

CROSS-BUNDLE OBSERVATIONS:
- Symbology (rule 5, the load-bearing axis here): CLEAN across all six. No inversion found — ghee is consistently settling, grounding, cooling, gathering, descending, binding; vāta's dryness/heat/depletion are named only as the condition remedied, never as ghee's action. Ghee.md is exemplary on this point and could serve as the symbology reference for the whole corpus.
- Two distinct authorial registers are obvious: Ghee.md and The_Guṇas_of_Ghṛta.md are the polished "rishi-forward" voice; the other four (Ethical, Universality, Restored, Golden_Magic) share an LLM-drafted surface — bolded headings, bolded inline emphasis on nouns, "Ayurveda" without macron, generic "Voices of Wisdom"/"Conclusion" section skeletons, and negative-contrast as default rhythm. A normalization pass should bring the four up to the two.
- Quote-format: the only hard breaks are the two Bhagavadgītā blocks in Golden_Magic; everything else conforms or is legitimately English-only.
- No new broken links, index orphans, sodium-naming, or earth-as-planet violations found in this bundle beyond what the orchestrator already cataloged.

### diet

Audited all 15 diet articles in full against AGENTS.md. The recent salt/B-12 edits largely landed cleanly: the saindhava-trace exception is stated consistently in Ambrosian_Diet (L125) and Vegan (L72), no B-12 or deficiency-as-evidence argument survives anywhere in the cluster (Vegan's modern-toxicology block argues from blood pressure/stroke/renal/bone outcomes only), the mitāhāra verses are correctly split (the `hitaṃ mitaṃ ca` line as 'proverbial yogic formulation', the distinct Gheraṇḍa 5.16 `mitāhāraṃ vinā` line cited to Gheraṇḍa Saṃhitā 5.16), and the raw-exceptions clause (honey/ripe-fruit-in-season/fresh-dairy) is handled cleanly and consistently across In_Praise (L109), Vegan (L94), Fruitarianism (L48), and Yogis_Dont_Eat_Fruit. No earth-as-planet and no sodium-naming violations beyond the orchestrator's already-cataloged Salt_Dosage source-extract item. No new broken links: all three source-extract references from the cluster (Fruit_as_Medicine, Raw_Vegan_Fruitarian_Harm, Raw_Vegan_Staples_Warnings) resolve.

Two published articles (Ambrosian_Diet, In_Praise_of_Agni) and the publish:true Dehydrated_Fruit_Coconut_Honey all break the em-dash density ceiling by roughly 2x — the most material hard-rule issue on shipped pages. The Protein.md question from the brief: it STAYS inside sanctioned name-it-to-reject-it territory — it scare-frames 'protein/micronutrient/gram-counts' as the rejected mechanical register and argues from āma/residue/obstruction and Āyurvedic mechanism, never from deficiency or counter-nutritional claims. Its one real defect is the antithesis-as-default-rhythm tic.

Quality ranking, cleanest to weakest:
1. Yogis_Dont_Eat_Fruit — the strongest essay in the cluster: dense primary sources, correct quote format throughout, controlled tic load, genuine aphoristic close ('No one lives on a broom.').
2. In_Praise_of_Agni — rich, well-sourced, glosses mostly present; held back only by em-dash density and two unglossed core terms.
3. Fruitarianism — clean voice, good source pacing, correct format.
4. Yogic_Food — solid and consistent; only the non-italicized source titles mar it.
5. Grains — substantively fine but format-inverted quote blocks and a stray `\*` artifact.
6. Vegan — strong reclamation argument; the toxicology section is listy but compliant.
7. Ambrosian_Diet (PUBLISHED) — central positive-diet essay, but carries the triple-negation tic, unquoted-English quote blocks, em-dash density, and the 3.30/3.31 citation conflict.
8. Dehydrated_Fruit_Coconut_Honey — well-sourced but em-dash-saturated.
9. Fear_of_Grains — clean argument, one 'Crucially,' filler.
10. Clay_Eating — six quote blocks with ZERO attributions plus an affirmative-micronutrition residue ('bioavailable minerals').
11. Interrupting_Fasts — unattributed quotes, meta-prose subtitle, redundant with Clay_Eating/Ambrosian.
12. Fruits_From_India_Are_Different — good doctrinal core undercut by the unsupported Steve-Jobs/Kutcher causal claim and example-dominance.
13. Penultimate_Sāttvic_Food — weakest by a wide margin: reads as an unedited LLM outline (every heading bold-wrapped, pervasive bullet lists, 'Modern Echoes'/'parallels' survey sections), and every quote block violates the format (citation-before-Sanskrit, no blank line, quoted IAST, italic English, no attribution). Strong candidate for a full rewrite.

Cluster-level organization note: the anti-clay argument is made three times (Clay_Eating, Interrupting_Fasts, Ambrosian's exclusion section) with overlapping Sanskrit (jīvena jīvam, ojas-hāri); consider consolidating to Clay_Eating and cross-linking. Quote-format compliance is the most uneven dimension across the cluster — Yogis/In_Praise/Fruitarianism follow the canonical bold-IAST + quoted-English + italic-title + em-dash-attribution form, while Clay_Eating, Interrupting_Fasts, Penultimate, Grains, Yogic_Food, and Ambrosian each diverge on one or more of those four points.

### water

QUALITY RANKING (best to weakest):
1. Carbon_Dioxide.md — short, clean, aphoristic ('Spirit exhales. Matter inhales. The world breathes as one.'). No tics, glosses vāyu/prāṇa/apāna on first use, one well-formatted HYP quote and one John quote. The single 'is not' construction ('There is no waste in it; only exchange', L17) is the sanctioned trailing-concession form, not the banned negative-contrast. Cleanest file in the bundle. Not published.
2. Aqua_Vitae.md — strong cross-tradition convergence essay, dense with primary sources, glosses handled well, em-dash density fine (~2.3/500). One real defect: the 'Eight corpora' / ten-traditions numeric mismatch (L120). Otherwise polished. Not published.
3. Keep_the_Plasma.md (PUBLISHED) — the doctrinal anchor; excellent IAST quote blocks in correct house format (Aṣṭāṅga Hṛdaya, Caraka rasa verses all properly Sanskrit→blank-line→English→em-dash-attribution). Glosses are thorough. Only minor issues (shared closing with Aqua; 'Damar Tantra' transliteration). The 'spirit ... drying' description (L158) is NOT a symbology inversion — the spirit is the solar/rajasic fraction, so adding dryness/heat is doctrinally correct; the lunar essence is correctly 'watery, quiet, sustaining'. Symbology is sound throughout.
4. Plasma_Recycling_Manual.md (PUBLISHED) — useful procedural companion but the bundle's least source-grounded and least house-conformant: three scriptural snippets all use citation-before-quote format (rule 2 violation), inconsistent/un-italicized source titles, and 'plasma'/'amarolī' never glossed for a standalone reader. Defensible as a manual but needs the quote-format and gloss fixes.
5. The_Distilled_Water_Paradox.md (PUBLISHED) — rhetorically the strongest-WRITTEN piece (vivid, well-argued split-mind thesis) but carries the most house-rule breaches, several on a PUBLISHED article: (a) FIVE Sanskrit quote blocks that are un-grounded in source-extracts OR the dedicated caraka-samhita repo and read as composed Sanskrit ('mṛttikā-loha-bhakṣaṇaṃ tamaḥ-nimittam', 'yad bhūtam jāyate jīvenā' with irregular grammar) — presented as verbatim verse without paraphrase-flagging or chapter.verse; (b) all five also invert the quote FORMAT (quotes on the Sanskrit, no blank separator, no quotes on the English, no em-dash attribution line); (c) 'on the planet' (earth-as-planet); (d) a five-instance negative-contrast tic cluster making it the article's default rhythm; (e) one 'the fact that' filler; (f) the doctrinal tension where its own life-passed standard would disqualify the distilled water it endorses. This file needs a full editorial pass before it should stand as published.

DISTILLED-WATER CONSISTENCY CHECK (per bundle guidance): The three published articles are reconcilable but not cleanly so. Keep the Plasma ranks distilled water as the best FOREIGN water (passed through fire/condensation, not life) and explicitly inferior to recycled essence; Plasma Manual L139 calls distilled water 'foreign'. The Distilled Water Paradox, however, validates the distilled-water baseline ('So far, so good'; 'Let water be water') and never notes that its own cited rule — only what has passed through life sustains life — disqualifies distilled water itself. The Paradox is internally about the clay-eating contradiction, not about distilled water's own status, so the tension is latent rather than a flat contradiction; flagged medium. Note the orchestrator's '2 sodium hits' in this file appear already corrected — every NaCl reference now reads 'chloride of sodium' (correct); only the 'planet' issue remains from that area.

NEW broken-link / index findings: none beyond the orchestrator's catalog. All five water articles are present in _index.md (lines 98-102) and the three published banners exist in generated-images/. Aqua_Vitae and Carbon_Dioxide correctly carry no front-matter / publish flag (not published), consistent with the .substack state.

MICRONUTRITION CHECK: The Distilled Water Paradox names modern categories ('inorganic minerals', 'calcium, aluminum, silicon, iron, magnesium', '84 trace minerals') but always to REJECT them (mocking the remineralization crowd) — this is the sanctioned 'naming the category to reject it' usage, not a micronutrition argument. No micronutrition violation in the bundle.

### yoga-tantra+personal

Bundle "yoga-tantra+personal" — 10 files audited in full. The AGENTS.md house rules were read first and applied.

QUALITY RANKING (strongest to weakest):
1. personal/Physical_Mortality_and_Essential_Immortality.md — by far the strongest piece in the bundle and a near-reference implementation: carefully sourced cross-traditional quotes (Olivelle, Copenhaver, Griffith translations all attributed), quote blocks correctly using double quotes + em-dash attribution + italic titles, glosses on ātman/nous/Puruṣa. Its only real weakness is the recurring clipped 'Three X. One Y.' fragment refrain (medium tic). Banner image present, post_id present, publish:true — fully consistent. This is the model the rest of the bundle should imitate.
2. personal/Refinement.md — also high quality: the smith/fire conceptual through-line is disciplined, quotes are close to house form (bold non-Latin + blank '>' + double-quote English + em-dash attribution). Two flaws: one meta-prose sentence ('this article holds steady in for the length of its reading') and a publish-state inconsistency (frontmatter publish:false but a dangling .substack-posts.json entry with banner, no post_id/slug). NOTE: this CORRECTS the orchestrator's pre-catalog — Refinement IS registered in .substack-posts.json (with banner) and the file explicitly says publish:false, not 'lacks publish:true'.
3. personal/Psyche_and_Machine.md — clean modern prose, one isolated negative-contrast tic; main question is fit/register (a social-media-design essay with no primary-source grounding in a source-grounded collection).
4. personal/Longevity.md — solid Āyurvedic framing (ojas/agni/ati-pravṛtti/saṃgraha all used well, no micronutrition language), but the McCarrison quote attribution is malformed (attribution line falls outside the blockquote) and the '200 years of age, verified' claim is an extraordinary factual claim resting on a 1931 popular-magazine secondary source — should be verified or softened.
5. yoga-tantra/Vajrolī.md — graceful prose but ALL eleven quote blocks violate the house quote form (Sanskrit not bold, no blank '>' separator, translation in italics not double quotes, parenthetical citation instead of em-dash line, source title not italicized). Also ~5 negative-contrast tics and unglossed core terms (bindu, rajas, amarī, Amarolī). High-value content, needs a full quote-format + gloss pass. (Cataloged broken-link note for The_Allure_of_Vata banner is a different file, not in this bundle.)
6. personal/Dharma_by_Annie_Besant.md — a 192-line VERBATIM reproduction of Besant's 1898 Benares lectures. Exempt from prose-style rules (tics, earth-as-planet, em-dash density inside it are all quotation), but it lacks any editorial frame explaining its inclusion and sits among original essays.
7. personal/Age_of_Saturation.md — the worst prose-discipline offender: negative-contrast / 'not-X-rather-Y' is the article's pervasive default rhythm (~10 instances in 484 words), exactly the saturation AGENTS.md flags as needing a full pass. Weak three-beat closing. Content is coherent but the form is the signature ChatGPT antithesis move throughout.
8. personal/The_Pressure_of_Being.md — quality-wise the weakest: (a) uses long underscore lines as horizontal-rule separators between every section (8×) — a banned HR in disguise, NEW instance not in the orchestrator's HR catalog (which listed only skills.md); (b) every quote uses bare parenthetical citations in italics with no em-dash attribution and no italic source titles; (c) several quotes (Kolbrin, all four Castaneda) are unsourced; (d) it is a quote-dump plus a trailing-summary bullet list (anthology stub) yet published in the public index.
9. personal/Notes.md — 3-line rough insight list ('First insight...'), not an essay, with casing/style errors; publicly linked.
10. personal/Olivier_Francoeur.md — 5 lines of bare astrological glyphs about a named private individual, zero prose. Highest stub-quality + privacy concern in the bundle; should not be on the public surface.

KEY ORGANIZATION OBSERVATIONS:
- The 'personal/' directory mixes four genuinely finished essays (Physical_Mortality, Refinement, Psyche_and_Machine, Longevity) with three stubs/notes (Notes, Olivier_Francoeur, The_Pressure_of_Being) and one verbatim third-party reproduction (Dharma_by_Annie_Besant). All eight are linked from the public _index.md (L129-137). The stubs and the reproduction dilute the collection; recommend either developing or de-listing Notes.md, Olivier_Francoeur.md, and The_Pressure_of_Being.md from the public index.
- Olivier_Francoeur.md publishes a named person's natal chart — a privacy concern flagged independent of essay quality.
- NEW horizontal-rule instance: The_Pressure_of_Being.md uses '____...' underscore rules (8×) which render identically to '---' and are not in the orchestrator's HR catalog.
- Substack-state correction: Refinement.md is registered in .substack-posts.json (with banner_image) but with no post_id/slug, while its frontmatter is publish:false — a genuine inconsistency, but the orchestrator's framing ('registered without post_id and file lacks publish:true') is imprecise: the file actively declares publish:false.
- Two publish-flagged files in this bundle (Physical_Mortality: publish:true, post_id present, banner present — fully consistent; Refinement: publish:false, partial manifest entry — inconsistent).
- No chloride/sodium, micronutrition, em-dash-density (max was Psyche_and_Machine at ~4/405 words, within limit), or earth-as-planet violations found anywhere in the bundle's original prose.

### political

SCOPE: Audited all 16 political/ethical essays in full against AGENTS.md. Bundle-wide mechanical state is clean for the items the orchestrator pre-cataloged: no `---` rules, no curly quotes, no 'sodium'/'planet', no micronutrition vocabulary used as evidence (the lone 'supplement' in The_Duty L13 and 'mineral' in All_Life_Is_Sacred L3 are category-naming / kingdom-of-nature uses, not violations). I found NO new broken links or index orphans in this bundle. No symbology-inversion or earth-as-planet findings here (these essays are political, not Āyurvedic-mechanism heavy). Cost_of_Manipulative_AI.md's only non-ASCII is the math-bold H1 already cataloged — re-flagged because severity matters and the body is otherwise clean (no further artifacts found). Em-dash density: every file is under the 5-per-500-words prose threshold once attribution-line dashes are excluded (The_Duty is highest at ~3.2/500, On_Anthropic ~2.6/500) — so no em-dash-density finding, though The_Duty stacks two prose dashes in several single paragraphs.

DOMINANT THEMES (judgment-level):
1. CITATION INTEGRITY is the most serious cross-bundle weakness. Unfree_Markets.md and Freedom_of_Thought.md lean on apocryphal/spurious quotes (the Rothschild 'permit me to issue' line, Voltaire 'returns to zero', the pseudo-Socrates 'definition of terms', Plutarch 'unjust law'). Danger_of_Knowledge.md's quote blocks are loose paraphrases dressed as verbatim scripture with no locators or translators and use plain-hyphen attributions. High severity because false attribution undermines a book that stakes its authority on primary sources.
2. QUOTE-FORMAT non-compliance is pervasive in the dharmic essays. Danger_of_Knowledge.md, The_Duty_You_Cannot_Refuse.md, and My_Mothers_My_Sisters.md all deviate from rule 2: inline Sanskrit+English on one line, English-only blocks where IAST exists, quotes around the Sanskrit instead of the English, unitalicized source titles, hyphen instead of em-dash attributions. Poisonous_Music.md is closest to compliant (bold IAST, blank line, em-dash) but still leaves source titles unitalicized and translations unflagged-as-paraphrase.
3. STRUCTURAL MIRRORING / REDUNDANCY: two pairs duplicate each other heavily. (a) Twitter_is_Obsolete.md and Obsolete_Social_Medias.md share verbatim paragraphs (the 'amplification', 'hardened into platforms', *psyche*-definition, personal-AI-agent passages) — they are nearly the same essay. (b) The_Duty_You_Cannot_Refuse.md and My_Mothers_My_Sisters.md share the entire vegan-decoy argument, the same four Gītā citations (3.8, 4.39, 18.66, plus the offering verse), and the Walmart/feedlot/'close the circuit'/'desertion' motif. The book should pick one of each pair or sharply differentiate.
4. META-PROSE / ESSAYISTIC SCAFFOLDING: On_Anthropic.md ('Let us begin', 'Consider next', 'Let us ask', the Plutarch 'Parallel Lives'/'Being an Account of' costume, Roman-numeral I-V), The_Warrior.md ('Herein lies a cohesive guide...as gleaned from'), and The_Idol_of_Wisdom.md ('## Conclusion') openly announce structure — the house voice forbids this. On_Anthropic and The_Idol_of_Wisdom also drift toward the banned 'audit/critique-of-one-source' framing (The_Idol_of_Wisdom is essentially a chapter-by-chapter recap of one Bjerknes book).
5. EMPHASIS-AS-TIC: Cheap_Talk.md, Cost_of_Manipulative_AI.md, and EU_Law_Against_Intelligence.md terminate most sentences on an italicized one-word payload (*exposure*, *fragmentation*, *capacity*) — a recognizable ChatGPT cadence. These three plus Cost read as the most machine-drafted in the bundle and least tonally coherent with the book's grounded, source-led voice.

QUALITY RANKING (best-conforming to most-needing-work):
- STRONG / near-target: My_Mothers_My_Sisters.md (vivid, grounded, strong aphoristic close 'Soon is a schedule.' — but mirrors The_Duty and needs gloss/quote-format fixes); Twitter_is_Obsolete.md (clean declarative prose, well-paced — but mirrors Obsolete_Social_Medias).
- SOLID with fixable issues: The_Tyrant.md and The_Warrior.md (coherent Castaneda exposition, but unattributed paraphrase; The_Warrior has a malformed heading); Poisonous_Music.md (good quote discipline, minor title/paraphrase flags); Freedom_of_Thought.md (tight argument, but spurious Socrates/Plutarch citations and filename mismatch); Unfree_Markets.md (forceful, but anchored on apocryphal quotes).
- WEAKEST / most off-voice: Cost_of_Manipulative_AI.md (math-bold H1 artifact + emphasis-tic body, thin); EU_Law_Against_Intelligence.md (abstract, agentless, emphasis-tic — reads generated); Cheap_Talk.md (negative-contrast is the default rhythm incl. the title); All_Life_Is_Sacred.md (ungrounded Theosophical homily, stub-like, no sources/glosses); Danger_of_Knowledge.md (worst quote-format and citation discipline in the bundle); The_Idol_of_Wisdom.md (book-recap framing, 'Conclusion' heading, unsourced inline quotes); Obsolete_Social_Medias.md (duplicate of Twitter_is_Obsolete).

ORGANIZATION OBSERVATIONS: (a) Freedom_of_Thought.md filename does not match its IP-abolition subject — index/link risk. (b) Twitter_is_Obsolete vs Obsolete_Social_Medias and The_Duty vs My_Mothers are candidates for merge/dedup at the editorial level. (c) Several political essays (Cost, EU_Law, Cheap_Talk, Obsolete_Social_Medias, On_Anthropic) are AI/tech-policy pieces with no Āyurvedic or solar grounding — they cohere as a sub-cluster but sit tonally apart from the book's core; worth a deliberate editorial decision about whether this political wing belongs and which entries earn their place. I did not invent issues to pad — All_Life_Is_Sacred and the cleaner essays simply yielded fewer findings.

### src-yoga-diet

OVERALL: This is a strong, citation-dense, well-organized bundle of source-extract files — the doctrinal backbone that feeds the diet/ayurveda articles. Most primary-source quote blocks DO follow the canonical Sanskrit→blank→English→attribution-last format correctly (Apathya.md, Cooking_and_Agni.md, Fruit_as_Medicine.md, Astanga_Hrdaya/water-and-srotas.md are exemplary). The bundle is largely clean on the hard rules: no `---` rules, no curly quotes, no Earth-as-planet violations (the two \"planet\" hits in Damar_Tantra/quotes.md L67/L75 are inside Damar Tantra quotations, exempt under rule 6), and the canonical apathya verses (HYP 1.59, GhS 5.21, BhG 17.9) are quoted consistently across files.

BUNDLE-GUIDANCE ITEMS RESOLVED:
- Salt_Dosage_and_Conditions.md L3 \"sodium chloride\" — CONFIRMED violation (high). Apathya.md L374 has the correct \"chloride of sodium\" for the identical fact, so this is a one-word fix and a consistency miss.
- The \"hitaṃ mitaṃ ca bhoktavyaṃ\" diet-verse — found only in Cooking_and_Agni.md L217, and it IS correctly marked \"proverbial yogic formulation\" (the systemic HYP 1.57 misattribution has been cleaned up per Raw_Vegan_Fruitarian_Harm.md L5). Residual concern: the constructed Sanskrit is still presented in bold-IAST primary-source format though the project says its source is unlocated (flagged, medium).
- Gheraṇḍa Saṃhitā 5.16 (mitāhāra precondition) — quoted correctly in Apathya.md L42-50 and Fruit_as_Medicine.md L259-267, consistent.
- The genuine HYP 1.57 brahmacārī verse is NOT misused anywhere in this bundle.

JUDGMENT-LEVEL THEMES:
1. Negative-contrast tic (rule 7) is the most recurrent style issue — at least 7 instances across Cooking_and_Agni, Raw_Vegan_Staples_Warnings, Agni_and_Tapas, Fruit_as_Medicine, Apathya, Salt_Dosage, and Raw_and_Cooked. Several land as section-closers or section-openers (the worst placements). No single file crosses the ~3-per-article threshold that mandates a full pass, but as a corpus the rhythm is establishing itself; worth a sweep.
2. Citation precision: the duplicated \"Caraka Sū. 25.40\" label in Fruit_as_Medicine.md (two distinct verses) is the most consequential citation issue because downstream files (Raw_Vegan_Salad_and_Juice, Raw_Vegan_Staples_Warnings) cite the aphorism by that number. The AH saindhava-exception verse is pinned in one file (Salt_Dosage) but left chapter-only in another (Apathya).
3. Micronutrition vocabulary leaks into Raw_and_Cooked_Cross_Tradition.md prose (calories/protein/nutrients) — the one file where the modern register slips in without being named-to-reject. Notably, Raw_Vegan_Fruitarian_Harm.md handles the same hazard impeccably (L7 explicitly brackets \"bone mineral density\"/\"amenorrhea\" as published terms and refuses the deficiency-argument register), so the standard exists in the bundle and Raw_and_Cooked should meet it.

QUALITY RANKING (cleanest → most in need of a pass):
1. Astanga_Hrdaya/water-and-srotas.md — exemplary quote discipline; only the bibliography-path inconsistency.
2. Atharva_Veda/barley-and-grain.md — clean, well-scoped, format note self-declared; no findings.
3. Agni_and_Tapas.md — strong; one tic, otherwise clean (cross-tradition quotes well-attributed).
4. Apathya.md — the doctrinal anchor; comprehensive and mostly correct; one tic, one chapter-only AH locator.
5. Fruit_as_Medicine.md — excellent material; the 25.40 double-label and one tic.
6. Cooking_and_Agni.md — rich; two tics (one a section-opener) and the unlocated-Sanskrit presentation issue.
7. Raw_Vegan_Fruitarian_Harm.md — model handling of the micronutrition hazard; minor: the Sources list (L67-68) has two entries run together on one line (\"...PMID 9831783.\" immediately followed by the next bullet without a newline; same at L68) — a markdown formatting slip, cosmetic.
8. Raw_Vegan_Salad_and_Juice.md / Raw_Vegan_Staples_Warnings.md — solid applied digests; one closing tic in Staples; both depend on the 25.40 locator being correct upstream.
9. Salt_Dosage_and_Conditions.md — substantively the most exposed: the \"sodium chloride\" violation plus the standalone-\"sodium\" comparators sit in the one file whose whole subject is the chloride argument, so the register slips matter most here.
10. Hatha_Yoga_Pradipika/quotes.md, Damar_Tantra/quotes.md — pure raw-extract quote lists; non-canonical quote-block form (no `\\` hard breaks) but functioning as pre-formatting scratch.

ORGANIZATION OBSERVATION: cross-file referencing is dense and mostly coherent (each file points to siblings for shared verses rather than re-quoting), which is good practice; the risk surface is exactly there — a miscited verse number (25.40) or an inconsistent term (sodium chloride vs chloride of sodium) propagates because downstream files cite by reference. A single normalization pass on (a) the 25.40/25.41 locator, (b) chloride-of-sodium wording, and (c) the bibliography-path convention would tighten the whole bundle.

### src-lunar-death

Overall: this is a strong, scholarly, quote-driven bundle. Sixteen files, almost all of which correctly follow the project's quote-block convention (bold IAST → blank `>` → English in straight quotes → em-dash attribution last) where Sanskrit is present, and use English-only blocks with attribution where there is no clean IAST (the Greek, Hermetic, Castaneda, Torres, Armstrong, and van der Kroon files). Clean on: smart quotes (none), horizontal rules (none), sodium-naming (none — no occurrence in any file), micronutrition vocabulary/deficiency-arguments (none), doṣa/guṇa symbology (ghee correctly named descending/gathering/binding/settling; \"dispersal\" is correctly attributed to the *fruit/solar* contrast-pole, not to ghee), and earth-as-planet (the only \"planetary\" use, Hermetic L61 \"seven planetary zones,\" is the classical Hermetic ascent term-of-art for the planetary spheres, not a reference to Earth — not a violation). Cross-reference links all resolve (Khecarividya, Golden_Fountain, Roots_of_Yoga, and Rg_Veda links checked and OK).\n\nMost significant issue (HIGH): an internal citation contradiction — Golden_Fountain L14 cites the ghee-as-amṛta phrase `ghṛtam amṛtasya nābhiḥ` as Ṛgveda 1.142.3, while the project's own verified Rg_Veda extract locates it at RV 4.58.1 (the Ghṛta-sūkta). 1.142.3 is wrong; this should be fixed before the phrase propagates into a published article.\n\nRecurring cross-file issues worth a sweep: (1) the title \"Khecarīvidyā\" is misspelled \"Khecharīvidyā\" in Golden_Fountain and Yogananda (the canonical extract and Mallinson use no extra 'h'); (2) bibliography source links point at `github.com/LiGoldragon/bibliography/...`, which conflicts with the AGENTS.md canonical library location `~/primary/repos/library/` that the Rg_Veda extract uses correctly — same stale-path class the orchestrator already flagged in .gitignore; (3) a Luna \"is-not-Sol's-X, she-is-Y\" negative-contrast refrain recurs across the Luna-themed Notes sections (soma-and-the-moon, moon-as-soul-threshold, Plutarch, the Homeric hymns) — fine as note scaffolding but the downstream Luna article must not inherit it, since negative-contrast is the project's single most-important banned tic.\n\nOne structural quote-format slip: soma-and-the-moon.md RV 10.90.13 (L9-12) puts the IAST below the English+attribution as a plain non-blockquoted line, inverting the canonical Sanskrit-on-top order — the only quote-block in the bundle that breaks the convention.\n\nQuality ranking (cleanest → most-needing-work):\n1. Hesiod theogony-sun-moon-dawn.md and hymn-31-to-helios.md — short, clean, correct attributions, italicized titles, minimal author prose.\n2. Upanisads/death-and-the-imperishable-self.md — exemplary quote density, clean structure, strong restraint in commentary.\n3. Plutarch_De_Facie/passages.md — excellent, but two negative-contrast tics in the Notes.\n4. Khecarividya/lunar-nectar-and-breath.md and Roots_of_Yoga/breatharian-witnesses.md — rich, well-attributed; bibliography-path issue.\n5. Hermetic_Corpus, Carlos_Castaneda, Armando_Torres — long English-only quote compilations, attributions present and consistent; light prose, mostly clean (their \"is not\" instances are inside quotations or benign).\n6. Yogananda/giri-bala — strong, but Khecharīvidyā misspelling and bibliography path.\n7. Water_of_Life/quotes.md — pure quote dump, attributions present; the lightest file, no judgment issues, though it lacks a Sources/edition footer block that the other extracts carry (minor).\n8. soma-and-the-moon.md — the richest Luna note-set but carries the quote-format inversion (RV 10.90.13) plus the most pronounced negative-contrast refrain; most-needing-work in the bundle.\n9. Golden_Fountain/urine-as-nectar — substantively excellent compilation, but holds the one HIGH citation error plus the title misspelling and bibliography path.\n\nOrganization note: the bundle implicitly forms two coherent clusters — a lunar/nectar/inedia cluster (Rg_Veda, Khecarividya, Golden_Fountain, Roots_of_Yoga, Yogananda, plus the Upaniṣad moon-threshold file) feeding \"The Body Does Not Want Water,\" and a death-and-immortality cluster (Upaniṣad imperishable-self, Hermetic, Castaneda, Torres, Plutarch) feeding a death/immortality article. The Water_of_Life Armstrong quotes overlap heavily with the Golden_Fountain Armstrong material (both cite the 45-day fast); when these feed an article, watch for redundancy between the two urine-therapy extracts.

### src-astrology

Scope: 7 astrology source-extract files (1 Arthur Young, 6 Dane Rudhyar). CRITICAL CALIBRATION: none of these files appear in _index.md (the index lists other source-extracts under source-extracts/ but NOT Arthur_Young/ or Dane_Rudhyar/), and none carry publish:true frontmatter. They are UNPUBLISHED working extraction notes, so no hard-rule-on-a-published-article 'high' severities apply — every style finding is medium/low accordingly.

Earth-as-planet (the headline concern in the bundle guidance): CLEAN in the project's own framing prose. Every 'planet/planets' in framing prose refers to actual planets (Saturn, Mars, Venus, the trans-Saturnian set, etc.), never to Earth. The high raw 'planet' counts live entirely inside quotations of Young/Rudhyar, for whom 'planet' is native vocabulary and exempt. The one framing-prose 'earth' (astrology-of-personality:54, 'life on earth') is lowercase terrestrial usage, not 'planet' — compliant. Quoted authors do say 'planet' (e.g. transformation:32/146 'the planet, the solar system, our galaxy') — correctly left intact as quotation.

Mechanical hygiene in these files is clean: no curly quotes, no --- horizontal rules, no banned filler ('notably/crucially/moreover/furthermore/delves into/rich tapestry' all absent), attribution lines uniformly use the em-dash + italicized-source format, the Paracelsus quote is properly double-attributed. English-only blocks (no Sanskrit) are the correct form here per Rule 2.

The two findings worth a human's attention:
1. (redundancy, high confidence) astrology-of-transformation duplicates the same Prologue 'vaster wholes' quotation at line 32 and line 146 — line 32 is a subset of the fuller closing at 146.
2. (citation-error, medium confidence) science-and-astrology summary table line 290 reads 'Control (L/T³ or LT)', contradicting L/T³ everywhere else in the file and Young's own LT=M angular identity (LT would be Mass, 120°, not the third derivative). Likely an OCR artifact that injected a dimensional error.
Plus a quote-format inconsistency (astrology-of-personality:52 inline quote with no attribution) and a handful of low-grade negative-contrast tics / em-dash-heavy passages typical of the editorial connective tissue.

Quality ranking (cleanest first):
1. pulse-of-life.md — best of the set; tight framing prose, em-dash density in bounds (~5.6/500), strong use of the Day-force/Night-force structure, Aries portrait well chosen as the method-exemplar, no tics of note.
2. astrological-study-of-psychological-complexes.md — clean, well-organized (urge/planet-pair table is genuinely useful), one mild 'not just... but' at line 24.
3. astrological-houses.md — strong content and the Sol-etymology gem ties it to the project, but the four 'Key reformulations' bullets (115-118) stack the not-X-but-Y antithesis four times.
4. practice-of-astrology.md — solid; the 13-step ToC is a good spine; em-dash-per-500 looks high only because the file is quote-dominated with little prose (arithmetic artifact, not a real tic).
5. astrology-of-personality.md — content-rich but carries the worst single tic (line 37 two-sentence negative-contrast) and the unattributed inline quote (line 52).
6. astrology-of-transformation.md — good synthesis but holds the duplicate-quotation redundancy and runs em-dash-heavy.
7. science-and-astrology.md — the most ambitious and most prose-dense; carries the formula inconsistency (290), the highest em-dash load (line 213 has three in one sentence), and a mild meta-prose opener (line 10). Still coherent, just the most in need of a polish pass.

Organization note: if any of these astrology extracts are meant to feed published articles, they should be registered in _index.md like the other source-extracts; their current absence means they are off the index entirely (consistent with working-note status, but worth a deliberate decision rather than an accident).

### research

SCOPE: Read AGENTS.md in full plus all six assigned files completely (01 vedic-origins 732L, 02 samkhya 1156L, 03 sastric-crossrefs 1272L, 06 structural-parallels 732L, 07 upanisadic 1212L, 00 index). These are raw quote-compilation research notes, not articles, so I judged to the lighter article-voice bar the bundle guidance specifies and did not penalize the quote-dense, low-orientation form (that form is the directory's stated purpose, 00_index L20).

OVERALL QUALITY: This is the strongest, most disciplined research material I would expect to find in the repo. Primary-source density is exceptional; citations carry text/chapter/verse/translator/page throughout; Sanskrit IAST is consistently provided; the thesis is genuinely supported by the weight of quotation rather than assertion. The corpus is CLEAN on the categories that usually break: no `---` rules, no curly quotes, no \"sodium chloride\", no \"planet\", no micronutrition vocabulary, no doṣa/guṇa symbology inversions, no broken quote-block ordering. The salt-water references (06 L558/560) describe yogic saline technique, not dietary NaCl — correctly not a sodium-naming violation.

QUALITY RANKING (best to weakest):
1. 02_samkhya — cleanest prose, tightest citations, least tic-laden; the \"One enumeration, five voices\" / parallel-reading device is effective without rhetorical antithesis. Only one minor \"not merely\" slip (L1143).
2. 07_upanisadic — superb source coverage (Taittirīya→Yoga-Upaniṣads), strong sequential argument; near-zero tics in own voice; the filler \"moreover\" hits are inside Hume/Dasgupta quotations and exempt.
3. 01_vedic_origins — excellent material but the \"X is not Y; it is Z\" close has hardened into the default rhythm of its Relevance notes; Kaṭha citation numbering disagrees with file 07.
4. 03_sastric — the richest cross-reference catalog, but carries the heaviest editorial meta-prose (CROWN JEWEL / KEYSTONE all-caps flags, \"Why this is the crown jewel\"), the worst em-dash load (12.3/500w incl. attributions), a garbled Dasgupta quote (L1003), and a negative-contrast conclusion opener.
5. 06_structural — outstanding parallel tables (sadvṛtta↔yama-niyama, pañca-karma↔ṣaṭ-karma, cikitsā↔yoga catuṣpāda are the bundle's best evidence), but the thesis paragraph stacks negative-contrast + chiasmus + 6 em-dashes, and it contains the one quote-integrity concern (bracket-substituted \"[chloride of sodium]\" inside a Muktibodhananda quote, L439).
6. 00_index — functional, but its one-sentence thesis (L5) is the purest triple-fragment negative-contrast tic in the set, and it advertises three files (04/05/08) that do not exist.

DEAD 04/05/08 ASSESSMENT (per bundle guidance): These are abandoned/unwritten stubs, NOT missing research. Their planned content has been substantially absorbed into the five existing files — ṛṣi-lineage into 01/03, shared anthropology (tridoṣa/prāṇa/nāḍī/kośa) into 01/02/07, modern scholarship (Mallinson/Singleton/Wujastyk/Larson/Meulenbeld/Zysk) into the \"Scholarly voices\" section that every existing file already carries. Recommendation: delete the three index entries and the two internal forward-references to them (01 L728, 03 L429) rather than write new files, since the coverage already exists; the numbering gap (04,05,08) is then harmless.

DOMINANT THEME ACROSS BUNDLE: The single recurring judgment-level issue is the negative-contrast tic (rule 7). Every file's thesis or conclusion leans on \"not X, but/it-is Y\" or \"not two — they are one\" (00 L5, 01 thesis+notes, 02 L1143, 03 L1214, 06 L3). The argument's actual content — sameness, unity, one-lineage — keeps getting expressed through the rhetorical-antithesis move the house voice forbids. A single pass converting these to positive declaratives would lift the whole set. No structural-mirroring-between-articles problem in the harmful sense — the parallel structure here is the intended method, not imitation.

No factual/doctrinal errors of substance found; the one factual-integrity concern is the garbled Dasgupta extraction (03 L1003) which reads as a corrupted placeholder and should be re-pulled or cut.

### xcut-consistency

CROSS-ARTICLE DOCTRINAL CONSISTENCY — overall the corpus is unusually well-harmonized; the central doctrines hold across all 22 files. Axis-by-axis verdict against the bundle guidance:

(a) SALT — Largely consistent. Every article that mentions the exception states the same shape: none as food, only a minuscule medicinal trace of saindhava by indication. Vegan.md §5's flat operational rule \"No salt should ever be used on anything\" is immediately reconciled in-file by the trace exception, and the source-extracts quote that rule verbatim, so it is not a contradiction. The one genuine gap: Yogis_Dont_Eat_Fruit.md L57 lists saindhava plainly as one of the daily-admitted Caraka foods WITHOUT the mandatory \"trace, not food\" caveat that The_Chloride_Indictment L101, Salt_Dosage_and_Conditions, and Fruit_as_Medicine all attach (reported). Plus the lone \"sodium chloride\" order in Salt_Dosage_and_Conditions L3 (reported; this is the same candidate the orchestrator flagged, here framed as the cross-article naming inconsistency since its siblings say \"chloride of sodium\").

(b) FRUIT — Consistent on the thesis (most fruit poison / fruit is medicine-by-indication, not a staple) across Fruitarianism, Yogis_Dont_Eat_Fruit, In_Praise_of_Agni, Ambrosian_Diet, Dehydrated_Fruit, and the Fruit_as_Medicine extract. No article treats fruit as ordinary food. The one real wrinkle is the HYP recommended-food LIST: Ambrosian_Diet L47 quotes paṭola (a fruit) and \"five leafy greens\" ON the wholesome list one line after asserting \"fruit appears nowhere,\" whereas Yogis_Dont_Eat_Fruit L11 puts greens on the AVOID list and omits paṭola (reported as doctrine-contradiction on the source-list characterization).

(c) RAW EATING — Cooked-first principle and the sanctioned raw exceptions (honey / ripe-fruit-in-season / fresh dairy) are stated in near-identical language in In_Praise_of_Agni L109 and Cooking_and_Agni L386 — strongly consistent. The only tension: fresh curd/buttermilk are named as raw exceptions there while Apathya lists dadhi/takra as apathya (reported, low severity — it is the medical-register vs yogic-beginner-register split, just not flagged as such).

(d) MITĀHĀRA VERSE — RESOLVED/CLEAN in the assigned files. The corpus has settled on two distinct verses, consistently attributed: the snigdha-madhura definition = Haṭha Yoga Pradīpikā 1.58 (Apathya, Yogis_Dont_Eat_Fruit, In_Praise_of_Agni, Keep_the_Plasma, both source-extracts), and the no-yoga-without-mitāhāra precondition = Gheraṇḍa Saṃhitā 5.16 (Ambrosian_Diet, Yogis_Dont_Eat_Fruit, In_Praise_of_Agni, both source-extracts). No stale \"HYP 1.15 / 1.57\" attributions survive in any assigned file; the poet report note in Raw_Vegan_Fruitarian_Harm.md L5 confirms that misattribution was cleaned corpus-wide. The proverbial \"hitaṁ mitaṁ ca bhoktavyaṁ annaṁ...\" maxim is consistently marked \"proverbial yogic formulation\" everywhere. This axis is effectively a non-finding — good.

(e) DISTILLED WATER — Consistent. Ambrosian_Diet and Keep_the_Plasma prescribe distilled/rain water; The_Distilled_Water_Paradox ENDORSES the distiller (calling it \"the mechanical answer to a conceptual diagnosis\") and only attacks the clay-eating contradiction, not distillation itself. No contradiction. The yad-bhūtam-jāyate-jīvenā life-origin rule is applied uniformly across Minerals, Inorganic_Minerals, Chloridism, Distilled_Water_Paradox, and Keep_the_Plasma.

(f) B-12 / DEFICIENCY ARGUMENTS — None survive in any assigned file. Vegan.md's modern-evidence compilation argues exclusively from clinical outcomes (blood pressure, weight, menstruation, bone) and never enlists a deficiency argument; Fruitarianism and Yogis_Dont_Eat_Fruit argue from dhātu-kṣaya / ārtava-kṣaya / ojakṣaya. Clean on this axis.

ADDITIONAL cross-article citation drift found (reported): three different Sanskrit wordings + three different Ṛgveda loci for the \"navel of immortality\" ghee verse (Ghee 4.58.1 / Penultimate 1.142.3 / Ambrosian unnumbered); the kaṇṭhakūpe throat-well sūtra cited as 3.30 (Ambrosian) vs 3.31 (Fruitarianism); the *guru* guṇa glossed \"deeply nourishing\" in Penultimate vs \"weighty/heavy\" everywhere else (this last is the most clearly wrong and the highest-severity item).

QUALITY RANKING of the assigned files (cleanest/strongest first): Ghee.md, The_Chloride_Indictment.md, Apathya.md, and the two big source-extracts (Cooking_and_Agni.md, Fruit_as_Medicine.md) are the strongest — dense, internally rigorous, careful with citations. Keep_the_Plasma.md and In_Praise_of_Agni.md are excellent and consistent. The_Distilled_Water_Paradox.md and Chloridism.md are clean. The two WEAKEST and the source of most findings: (1) Penultimate_Sāttvic_Food.md — visibly older drafting layer (bold-everything headings, bullet-listy, the \"guru = deeply nourishing\" error, divergent ghee-verse citation) and reads as not yet brought up to the corpus's current standard; (2) The_Two_Pillars_of_Nourishment.md — an esoteric/schematic register (solar/lunar/earth shadows) that admits \"seed-ghee/plant-ghee\" as ojas-building, lightly contradicting the taila-is-apathya line, and uses no primary-source quote blocks at all despite being named in AGENTS.md as a key anchor text. These two would most repay a consistency-and-voice pass.

ORGANIZATION observation: the saindhava-as-daily-food framing is the one doctrine that genuinely needs a single canonical sentence the project reuses verbatim — right now each article re-derives the caveat (or, in Yogis_Dont_Eat_Fruit, drops it), which is exactly where drift creeps in. A one-line canonical gloss (\"saindhava: a minuscule medicinal trace by indication, not a food\") referenced from every salt mention would close the axis.

### xcut-citation

SCOPE: I read all 16 assigned files in full and externally verified the bundle's flagged traps via web search (Yoga Sūtra 3.31, HYP 1.57 vs 1.58, RV 4.58.1, Taittirīya vallī structure, Yoga Yājñavalkya mouthfuls). The dominant, highest-confidence finding is a REPEATED CITATION ERROR: "annaṃ brahmeti vyajānāt" is Taittirīya Upaniṣad 3.2 (Bhṛgu Vallī), but six files cite it as 2.2.4 (Ānanda Vallī). The project itself proves these wrong — ayurveda/Cooking_and_Spices.md (the AGENTS.md-designated reference implementation) cites it correctly as 3.2. Fix it once in the two source extracts (Apathya.md, Fruit_as_Medicine.md, Cooking_and_Agni.md) and the article repeats follow. The articles also wrongly present 2.1 (oṣadhībhyo'nnam) and 3.2 (annaṃ brahma) as one continuous section; they are different vallīs.

SECOND THEME: the two "old-pattern" files AGENTS.md L80 explicitly names for retirement — ayurveda/Āyurveda.md and the chloride/witnesses/Witnesses_Against_Salt_*.md files — are still un-migrated. Beyond format, Āyurveda.md is the weakest file for citation integrity: it sets multiple INVENTED or unlocatable Sanskrit lines in the bold primary-verse format (amṛtasya nāma yad brahma with NO attribution; two "after Caraka Sūtrasthāna tradition" mūtra-loss couplets; bare "Ḍamar Tantra" and "classical Ayurvedic formulation" blocks). Setting unsourced Sanskrit in the same bold format as attested verses is the most serious systemic problem in the bundle, because a reader cannot tell fabricated from genuine.

THIRD THEME — cross-file verse-number drift that should be reconciled: (a) the lead/alkali salt-group is cited as AH 6.147 in Apathya.md but AH 10.27 in both Witnesses_Against_Salt_Ayurveda.md and Salt_Dosage_and_Conditions.md (10.27 is attested twice, so Apathya's 6.147 is the likely error); (b) the Vāgbhaṭa salt-excess catalogue drifts between AH 10.12–13 (Apathya.md) and AH 10.13–14ab (two other files); (c) the AH na-hy-apakvād / cooking-pot verse is 3.54 / 3.55–56 in In_Praise_of_Agni but 3.53–54 in Cooking_and_Agni; (d) Damar vs Ḍamar Tantra spelling.

QUALITY RANKING (best to worst on citation integrity):
1. source-extracts/Apathya.md and source-extracts/Cooking_and_Agni.md — dense, precise, mostly attested, honest proverbial markers; the 2.2.4 Taittirīya error is the main blemish.
2. ayurveda/Cooking_and_Spices.md — the reference implementation; cleanest blocks, correct 3.2 locus.
3. source-extracts/Fruit_as_Medicine.md — thorough and well-pinned, same 2.2.4 slip.
4. diet/In_Praise_of_Agni.md, diet/Yogis_Dont_Eat_Fruit.md, diet/Fruitarianism.md — strong, mostly verifiable; minor verse-number and Taittirīya issues.
5. ayurveda/Apathya.md — excellent prose, but carries the 6.147 conflict and the unlocated mṛttikā-loha verse.
6. source-extracts/Salt_Dosage_and_Conditions.md — good, but the "sodium chloride" violation (house rule 3) is a hard break.
7. diet/Ambrosian_Diet.md — the most citation-loose of the diet articles: YS 3.30 error, bare "Ṛg-veda", paraphrased ghee verses in bold, un-hedged yavāgū and annaṃ-brahma lines.
8. diet/Yogic_Food.md — non-canonical block format (double blank line, capitalized IAST), unlocated paraphrase verses in bold, 2.2.4 error.
9. chloride/witnesses/Witnesses_Against_Salt_Yoga.md — all-English blocks, citation order acceptable, but several "wider corpus" attributions (Yoga Yājñavalkya, Dattātreya, Haṭhābhyāsa Paddhati) are asserted without loci.
10. chloride/witnesses/Witnesses_Against_Salt_Ayurveda.md — old retired pattern, varaṃ->saindhava silent substitution, 6.147/10.27 confusion, unlocated mṛttikā-loha.
11. ayurveda/Āyurveda.md — weakest: unattributed and likely-invented Sanskrit in primary-verse format; needs the deepest rework.
12. ayurveda/True_Ayurveda.md — no quote blocks at all; asserts textual authority with zero loci (separate problem from the others, but it is a published article leaning entirely on un-cited texts).
13. source-extracts/Hatha_Yoga_Pradipika/quotes.md — a clean Muktibodhananda extract; HYP 1.15 six-destroyers verse correctly placed (confirms the corpus avoids the HYP-1.15 mitāhāra trap). No issues beyond being English-only by design.

ORGANIZATION NOTE: Yogic_Food.md and True_Ayurveda.md lack YAML front-matter that the other published diet/ayurveda articles carry (title/kind/publish/banner). Yogic_Food.md, Yogis_Dont_Eat_Fruit.md, and Fruitarianism.md also lack front-matter, which may be an index/publish-state gap worth a quick check against _index.md. The Damar/Ḍamar Tantra spelling and the saindhava chloride-percentage wording ("~95–99% sodium chloride" vs "chloride of sodium") should be standardized corpus-wide in one pass.

### xcut-organization

OVERALL ARCHITECTURAL ASSESSMENT

The Book of Sol is a well-developed essay collection (~90 articles + ~40 source-extract files) whose CORE organization is sound: ten category directories, a single canonical _index.md (with readme.md symlink), a clean source-extracts/ vs standalone-library vs caraka-samhita boundary, and a coherent frontmatter convention. The boundary discipline AGENTS.md preaches is actually respected on disk — no book binaries (.pdf/.epub/etc.) leaked into the repo, the .gitignore enforces it, and no Caraka OCR/digest material is misplaced here. The frontmatter rule ("frontmatter + kind:article/publish only when published or article-shaped") holds: exactly 19 of 103 files carry YAML, and the set is principled — every one of the 12 manifest-published articles has frontmatter, plus a handful of publish:false drafts (Honey_and_Fire, The_Allure_of_Vata, The_Toroidal_Heart, Refinement) and the two cosmology kind:note working-notes. Frontmatter is NOT haphazard; the apparent sparsity is the rule working as intended.

The real organizational debt clusters in four places:

1. INDEX/MANIFEST DRIFT (highest-value fixes). The research_ sub-index promises 04/05/08 that don't exist (3 dead links + numbering gap). The source-extracts listing in _index.md is half-curated: 14 extracts unlinked, including Surveying_Instruments which the cosmology article cites by name as its "companion file." cosmology/All_Instruments (publish:true) and skills.md (publish:true, anomalous) are both absent from .substack-posts.json. These are concrete, mechanical, and each breaks a stated invariant ("_index.md is canonical", "publish:true must be in the manifest").

2. STUBS IN THE PUBLIC INDEX. personal/Notes.md (a 3-bullet scratch outline) and personal/Olivier_Francoeur.md (3 lines of astrology glyphs) are linked from the public _index.md but are unfinished private fragments — a direct tension with INTENT.md's "not a private notebook ... public-facing surface" framing. These should be de-listed until written.

3. REDUNDANCY / CROSS-DIR SPLIT in two clusters. (a) chloride/Minerals.md and chloride/Inorganic_Minerals.md argue the identical ash/"life cannot eat the dead" thesis with overlapping Caraka citations — merge candidates. (b) The veganism-ethics argument is split across chloride/NaCl_Not_Vegan.md and diet/Vegan.md + diet/Vegan_Dairy.md, the latter two restating the same "veganism = non-abuse, humans are animals" premise near-verbatim. State the premise once; place the corollaries together or cross-link.

4. CATEGORY-CUT IMBALANCE + UNDOCUMENTED AUX DIRS. yoga-tantra/ is a one-article bucket (Vajrolī) while yoga-themed material lives in diet/ and chloride/witnesses/. teasers/ (two .txt blurbs) is undocumented and tied to nothing. generated-images/ carries an orphaned ghee-banner.png v1 superseded by v2. Images/cover.png vs generated-images/ split is correct and intentional (cover is project chrome, banners are per-article).

DOC STALENESS: AGENTS.md L80 still names Witnesses_Against_Salt_*.md and ayurveda/Āyurveda.md as exemplars of the retired citation-between quote pattern, but those files have ALREADY been migrated to the correct pattern (verified: bold Sanskrit, blank >, English, em-dash attribution last). The rule doc lags its corpus. The .gitignore comment points at the stale ~/git/bibliography/ instead of the canonical ~/primary/repos/library/.

NON-ISSUES (checked and cleared): diet/Protein.md ("The Protein Delusion") titling the banned category is explicitly permitted ("naming the modern category to reject it is allowed"). The chloride/witnesses/ per-tradition cut (Ayurveda/Yoga/Tantra/Dharma/Greek/Hebrew/Chinese/Hygienists/Political) is a deliberate compilation form, correctly nested. The two cosmology working-notes (Computing_vs_Measuring, Horizon_Dip) are correctly publish:false and correctly omitted from the public index — they support All_Instruments. The Surveying_Instruments extract is linked from the cosmology article body (just not from _index.md). readme.md->_index.md symlink is correct.

QUALITY RANKING OF FILES READ (organizational health, best to worst): (1) AGENTS.md / ARCHITECTURE.md / INTENT.md / skills.md — the doc set is strong and mostly internally consistent, only the L80 + .gitignore staleness drags it. (2) .substack-posts.json — clean and well-formed, just missing two publish:true entries. (3) _index.md — comprehensive and well-ordered for articles, but the source-extracts tail is the weakest section (inconsistent curation). (4) research_yoga_ayurveda_lineage/00_index.md — promises 3 files that don't exist; worst index-integrity of any file. (5) personal/Notes.md and personal/Olivier_Francoeur.md — the two genuine stubs that shouldn't be in the public surface yet.

RECOMMENDED TARGET STRUCTURE
- Keep the 10 category dirs, but either grow yoga-tantra/ (pull Yogic_Food, Yogis_Dont_Eat_Fruit into it) or fold Vajrolī into ayurveda/practice; one-article dirs are not worth a top-level cut.
- Move kind:research / kind:note non-articles OUT of article category dirs: Chloride_In_Produce_Evidence_Table.md -> source-extracts/ or a research_chloride/. The two cosmology notes can stay (they are the only cosmology working-notes and sit beside their one article) but should be acknowledged as a working-notes cluster, not articles.
- Adopt ONE explicit _index.md policy for source-extracts: list every extract an article cites (and add the 14 currently missing, especially Surveying_Instruments), OR list none and keep _index.md to published articles + the curated Rudhyar/Young/Caraka reading lists. Document the choice in skills.md.
- Merge the two minerals essays into one; consolidate the veganism premise once and place/cross-link the salt + dairy corollaries together.
- Fix the indices: write or de-link research 04/05/08; add cosmology/All_Instruments and resolve skills.md's stray publish:true; add the two missing manifest entries.
- De-list personal/Notes.md and personal/Olivier_Francoeur.md from the public index until they are real essays.
- Refresh AGENTS.md L80 and the .gitignore path comment to match the current corpus.
- Document or remove teasers/; delete the orphaned ghee-banner.png v1.

## Appendix — deterministic baseline (orchestrator-confirmed, certain)

- Horizontal rules (`---`): only `skills.md` (8). No article.
- Curly/smart quotes: none in the corpus.
- Literal "sodium chloride": `AGENTS.md` (rule), `chloride/Chloridism.md` + `The_Chloride_Indictment.md` (sanctioned contrast), `diet/Vegan.md` L117-118 (citation titles, allowed), `source-extracts/Salt_Dosage_and_Conditions.md` L3 (violation — fix to "chloride of sodium").
- Broken links: `ayurveda/The_Allure_of_Vata.md` → missing `allure-of-vata-banner.png`; `skills.md` → `../generated-images/in-praise-of-agni-banner.png` (escapes repo); `research/00_index.md` → nonexistent `04_shared_rsis_and_lineages.md`, `05_shared_anthropology.md`, `08_modern_scholarship.md`.
- `_index.md` article orphans: `chloride/Chloride_In_Produce_Evidence_Table.md`, `cosmology/Computing_vs_Measuring_The_Curve.md`, `cosmology/Horizon_Dip_vs_Altitude.md`.
- Substack: `personal/Refinement.md` registered w/o `post_id` and not `publish:true`; `cosmology/All_Instruments…` and `skills.md` are `publish:true` but absent from `.substack-posts.json`; `skills.md` should not be `publish:true`.
- Unicode math-bold heading: `political/Cost_of_Manipulative_AI.md`.
- `.gitignore` comment points at stale `~/git/bibliography/` (canonical `~/primary/repos/library/`).
- research numbering gaps: 04, 05, 08 absent.

## Remediation log (2026-06-19)

Acting on the psyche's triage of this audit: fix the high-severity findings on live Substack pages, and prune the dead research links. Done and shipped — TheBookOfSol commit `32e57ab2` (the citation/tic/format fixes), re-published to Substack the same day.

### Live-page high-severity fixes (re-published)

- **`chloride/The_Chloride_Indictment.md`** (post 194783381) — full negative-contrast pass: removed every `X is not Y. It is Z.` instance (the Section I–IX prose hammers, the six-bullet Verdict, and the closing line `Chloride is not salt. Chloride is chloride.` → `Chloride is chloride.`), converting each to a positive declarative and reserving the trailing-concession form for the three cases where the denied term carries information. Fixed the one out-of-bounds standalone `sodium` (L101, "daily sodium" → "daily chloride"); the Section II sodium/chloride contrast is sanctioned and was left.
- **`diet/Ambrosian_Diet.md`** (post 193562915) — `annaṁ brahmeti vyajānāt` was attributed to *Taittirīya Upaniṣad* 2.2.4 (Ānanda Vallī); it is **3.2 (Bhṛgu Vallī)**. Corrected the citation, reframed the surrounding prose (it is not the conclusion of the 2.x anna-puruṣa chain but Bhṛgu's first realization), and brought the block to canonical format (un-quoted bold IAST, blank line, quoted English).
- **`water/The_Distilled_Water_Paradox.md`** (post 195637783) — all five Sanskrit quote blocks were presented as verbatim *Caraka Saṃhitā* / *Bṛhadāraṇyaka* verse but are unlocatable / composed. Reformatted each to canonical shape and re-marked the attribution as `— proverbial formulation, after the *Caraka Saṃhitā* / *Bṛhadāraṇyaka Upaniṣad*`, which the house rule permits for paraphrase. Tidied the irregular `jīvenā` → `jīvena`.

### Off-page consistency fix (committed, not published)

- **`diet/Fruitarianism.md`** — the throat-well aphorism (`kaṇṭhakūpe kṣutpipāsānivṛttiḥ`) was cited as *Yoga Sūtra* 3.31, contradicting Ambrosian's 3.30. Verified the canonical number is **3.30** (Centre for Yoga Studies, Trevor Leggett, wisdomlib) — so the live Ambrosian page was already correct and the verifier's "change Ambrosian to 3.31" advice was wrong. Aligned Fruitarianism to 3.30. *(Lesson: a verifier agent flip-flopped on this number; the orchestrator web-checked before touching a live page.)*

### Organization fix

- **`research_yoga_ayurveda_lineage/00_index.md`** — pruned the three dead links (`04_shared_rsis_and_lineages`, `05_shared_anthropology`, `08_modern_scholarship`) to files that were never written. The index now lists only the five chapters that exist (01, 02, 03, 06, 07).

### Still open

The remaining ~301 findings (the corpus-wide tic sweep, quote-format normalization across the unpublished articles, glossing gaps, the `Penultimate_Sāttvic_Food` *guru* mistranslation, the stub fragments in the public index, the `skills.md` horizontal rules + stray `publish:true`, the `AGENTS.md` self-staleness on the witnesses-pattern claim and the `.gitignore` path) are catalogued above and await a dedicated pass when the psyche calls for one.
