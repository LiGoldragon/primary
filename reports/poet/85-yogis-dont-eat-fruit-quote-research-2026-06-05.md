# Yogis Don't Eat Fruit — quote research, Vedic + raw-food expansion, and Caraka validity check

Session of 2026-06-05. Role: poet. Repos touched: `TheBookOfSol` (article + four source-extracts), `caraka-samhita` (one philology note + one note edit), `primary` (this report). Lane claimed for the two `/git` repos; no shared primary surfaces claimed (reports are exempt).

## What was asked

Two psyche prompts, one thread. First: research and find more quotes to support the article *Yogis Don't Eat Fruit* — look online, treat the local Caraka as possibly invalid, and find Vedic material on fruit being secondary, eaten sparingly and in season, and on yoga not advising a fruit-heavy diet. Second: corroborate that raw vegetables, raw fruit, large quantities of greens, raw salad, raw-vegan eating, and juicing have specific consequences in Āyurveda, and show why yoga would not condone them.

Both are working orders, not durable intent; no Spirit record was warranted (the article's thesis is pre-existing content, and the Caraka data-quality concern is already documented in the `caraka-samhita` repo). The deliverable is verified quotes, extracted and woven in.

## The Caraka validity finding — content sound, numbering divergent

The sharpest result. The concern that "the version we have doesn't seem valid" resolves, for the fruit chapter, into a precise two-sided answer:

- **The content is authentic.** Every Caraka Sūtrasthāna 27 fruit verse the project cites was checked against GRETIL's authoritative Unicode Sanskrit (Oliver Hellwig's contribution, which covers exactly Sū. 1, 12, 26, 27, 28 — the food chapters included). All match verbatim in substance. The project is not quoting a corrupt or invented text.
- **The verse numbers diverge.** The Sharma 2014 numbers the project's citations follow do not match GRETIL's, and not by a constant offset: grapes shift ~18 verses (Sharma 27.143 = GRETIL 27.125–126), mango ~7 (27.146 = 27.139), *āmalaka* ~9 (27.156 = 27.147), pomegranate (27.157 = 27.149–150), the six *tridoṣaghna* fruits (27.158 = 27.145–146). One genuine variant reading surfaced: Sharma's *ketakī* is GRETIL's *tṛṇaśūnya* in the six-fruit list.

The corrective is the same as for the already-documented Sū. 5.12 problem (interpretive English): name the edition, cross-check the critical Sanskrit, treat the bare verse number as provisional. Full mapping with GRETIL Sanskrit anchors is in `caraka-samhita/notes/philology/sutrasthana-27-fruit-verses-gretil.md`; a pointer was added to `notes/translation-sources.md`.

GRETIL does **not** cover Sū. 5 (daily routine) or Sū. 6 (seasonal regimen), so those rest on Sharma plus the wisdomlib cross-check.

## New quotes added to the article

Four additions to `diet/Yogis_Dont_Eat_Fruit.md`, each deepening the existing one-image structure (anna = floor / fruit = broom; solar = clearing / lunar = binding) rather than braiding a new image:

1. **Bhagavad Gītā 6.16–17** (in "What the Gītā Requires") — yoga itself is barred to the one who eats too much or fasts to depletion; it belongs to the *yuktāhāra*, the measured eater. This is the most direct textual answer to "yoga doesn't advise eating a whole bunch," and it was missing from the article. Verified verbatim (Devanagari + IAST) against two sources.
2. **Ṛgveda 4.58.1** (in "The Solar Excess") — the *Ghṛta-sūkta* names clarified butter the secret name of *amṛta*, the tongue of the gods, the navel of the immortal. A Vedic witness for the lunar/ghee pillar, which the article had been asserting without a source. Sanskrit half-line verified.
3. **Seasonal / *kāla-viruddha*** (in "What the Texts Actually Say") — Caraka counts eating against the season among its named categories of incompatible food (*viruddha-āhāra*). This makes "eaten in season" a clause of classical law, not a preference. No new block; inline citation to Sū. 26.
4. **The raw plate — salad, juice, raw-vegan** (in "And Neither Do They Eat Salad") — the *sāmānya* "like increases like" law; the GRETIL-verified dry-rough-taste consequence verse (Sū. 26.43: dries the seven *dhātus*, roughens the channels, derangess *vāta*); the juice-strips-chewing-and-warmth point; and the close — yoga excludes raw greens (*harita-śāka*) by name and prescribes their cooked *snigdha-madhura* opposite. The raw regimen framed as "the fruitarian error in a second key."

The article's six pre-existing quote-blocks were also brought from the legacy form (Sanskrit-in-quotes, no blank line, English unquoted) to the canonical form mandated by the repo `AGENTS.md` (bare-bold Sanskrit, blank `>` line, English in double quotes), so the whole article is now internally consistent.

## New material extracted (the "more quotes" deliverable proper)

Extraction is where the bulk of the quotes live, per the project's source-extracts convention:

- **`source-extracts/Apathya.md`** — added Bhagavad Gītā 6.16–17 (yoga requires the measured eater) to the *mitāhāra* section, and the GRETIL-verified *tikta* (bitter) and *kaṣāya* (astringent) rasa-atiyoga verses to the rasa-excess section. These complete the six-rasa-in-excess set (the project already held *amla*, *lavaṇa*, *kaṭu*; *madhura* lives in `Fruit_as_Medicine`). The dry-rough pair is the textual ground for the raw-food verdict.
- **`source-extracts/Rg_Veda/ghrta-as-amrta.md`** (new) — the Ṛgveda 4.58 *Ghṛta-sūkta* witness: ghṛta as *amṛta*, the streams of ghee descending, ghee as the fit oblation; framed against the observation that the Vedic nourishing vocabulary is grain, milk, ghee, and Soma — *phala* is not a Vedic food-category.
- **`source-extracts/Fruit_as_Medicine.md`** — added a seasonality section (the *ṛtu-sātmya* principle and the *kāla-viruddha* block, Sū. 26.86–87) and a Suśruta concord section (the verified *Annapāna-vidhi* opening, Sū. 46, plus a clearly-marked prose summary of Suśruta's *phala-varga* verdict, which matches Caraka point for point).
- **`source-extracts/Raw_Vegan_Salad_and_Juice.md`** (new) — an applied digest assembling the classical verdict on the three modern raw modes (salad / raw-vegan / juice) and the yoga-exclusion conclusion, leaning on pointers to the deep `Cooking_and_Agni`, `Apathya`, and `Raw_and_Cooked_Cross_Tradition` extracts rather than re-quoting.

The project's raw-vs-cooked coverage was already deep (`Cooking_and_Agni.md`, `Raw_and_Cooked_Cross_Tradition.md` — the latter carrying Hippocrates, Galen, Avicenna, Chinese medicine, Lévi-Strauss, and Wrangham's Giessen raw-food clinical data). The additive work was the *mechanism* (the *sāmānya* law tying raw-cold-dry food to *vāta* derangement) and the *application* to the specific modern modes.

## Tooling and library state

- **`annas` (Anna's Archive CLI)** works unauthenticated for search; invoke from `~/primary/repos/library` so it finds `.env` and filter the startup WARN/stack-trace noise. Caraka Vol. II (the clinical half, `724d10c448ea5542470cbbfe0a8029f6`) and Suśruta (Bhishagratna, `6d7c8a8610d3a4f0c4556cc6a3d08bc1`) are available if ever needed; no download was required this session.
- The library already holds the texts this work needed: Ṛgveda (Griffith complete), Atharvaveda (Whitney), Yajurveda, Suśruta (Bhishagratna), Vāgbhaṭa (Aṣṭāṅga Hṛdaya), Caraka (Sharma 2014), Gheraṇḍa, Śiva Saṃhitā, plus a Sanskrit Caraka OCR and a Cakrapāṇi-Harinatha zip under `sa/ayurveda/`.

## Follow-up (same day, after a mid-session crash): two items resolved

A reboot interrupted the follow-up pass; on resume the two highest-value follow-ups were carried to completion.

- **Suśruta verbatim — done.** The `Fruit_as_Medicine` §X Suśruta section now carries verbatim Bhishagratna block-quotes for grapes (*drākṣā*), *āmalaka*, mango (*āmra*), pomegranate (*dāḍima*), and the sour-fruit rule — verified against the on-disk OCR bundle and wisdomlib's Bhishagratna text — replacing the earlier prose summary. The concord with Caraka Sū. 27 is now shown rather than asserted.
- **Cakrapāṇidatta's commentary — found on disk and used.** `sa/ayurveda/caraka-cakrapani-harinatha.zip` (the Harinātha Viśārada Caraka-with-*Āyurveda-Dīpikā*) has recoverable OCR for the Sūtrasthāna 26–27 pages. It **settles the *ketakī*/*tṛṇaśūnya* variant**: Cakrapāṇi glosses *tṛṇaśūnya* as the *ketakī-phala* — one fruit under two names, not a textual disagreement. The same page numbers the verse 124 (a third edition-numbering, against Sharma 158 / GRETIL 145–146) and quotes Suśruta on pomegranate in the commentary's own voice. The caraka-samhita philology note records the resolution, and `translation-sources.md` is corrected — its framing of Cakrapāṇi as the unacquired "single most useful addition" was stale, since a recoverable Cakrapāṇi edition had been on disk all along.

## Still open
- **GRETIL cross-numbering** could be extended across the whole Sū. 27 fruit/vegetable catalogue and folded into `caraka-samhita/fruit-vegetable-warnings.md` as a parallel column.
- **Atharvaveda barley hymn (AV 6.142)** would be a clean Vedic grain-primacy witness; the sacred-texts fetch was blocked (403) this session, so it was left out rather than quoted unverified. Whitney is on disk.

## Note on method

All Sanskrit added or reformatted was verified against a primary source before being presented as a quote (GRETIL for Caraka 26/27, wisdomlib/holy-bhagavad-gita for the Gītā, wisdomlib/Wikisource for the Ṛgveda). Where a clean verbatim was not in hand — the Caraka Sū. 6 seasonal verse and the Suśruta per-fruit properties — the principle was stated in prose with a chapter-level citation rather than fabricated as a block-quote, per the project's verifiability discipline.
