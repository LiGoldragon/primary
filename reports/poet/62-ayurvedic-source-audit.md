# 62 — Ayurvedic source audit

*State of the project's Āyurvedic sources: what exists, where,
in what shape, what is missing, and what stops us finding the
rest.*

## Frame

The project's Āyurvedic argument — chiefly in TheBookOfSol but
extending into the caraka-samhita repo and downstream into the
Apathya, Cooking and Spices, Witnesses Against Salt — Āyurveda,
and Two Pillars essays — rests on a small canon of classical
texts and a wider ring of secondary scholarship. This audit asks
five questions of that source set:

1. *Where do the sources live?*
2. *What is actually present, by canonical text?*
3. *Can an agent read what is present?* (i.e. text-extractable
   into searchable, citable English or IAST, not opaque
   image-PDF.)
4. *What is missing that the argument needs?*
5. *Why are the missing texts missing?* (network, OCR, edition
   pricing, taxonomic gap.)

"Agent-readable" here means: the file's text content is
recoverable by `pdftotext`, `unzip` to OCR text, or direct
markdown read — not locked behind an image-only scan or absent
from disk.

The Āyurvedic canon, for purposes of this audit, is the
classical *bṛhat-trayī* (Caraka, Suśruta, Vāgbhaṭa's *Aṣṭāṅga
Hṛdaya* and *Aṣṭāṅga Saṅgraha*), the mediaeval *laghu-trayī*
(Mādhava Nidāna, Śārṅgadhara Saṃhitā, Bhāvaprakāśa), the major
classical commentaries (Cakrapāṇidatta on Caraka, Ḍalhaṇa on
Suśruta, Aruṇadatta and Hemādri on Vāgbhaṭa), the principal
specialised compendia (Cakradatta, Yoga Ratnākara), and the
ring of secondary scholarship that gives Western-philological
access (Meulenbeld, Wujastyk, Zysk, Larson, Dasgupta).

## Where the library actually is

The single most important finding before any further audit:

**The bibliography is at `/home/li/Criopolis/library/`, not
`~/git/bibliography/`.** TheBookOfSol's `AGENTS.md` (lines
13–46) and caraka-samhita's `AGENTS.md` (the "Related
repositories" section) both reference `~/git/bibliography/` as
the canonical book-binary path. That directory does not exist
on this machine. `/home/li/git/` is empty. The active library
lives inside Criopolis, under
`/home/li/Criopolis/library/{en,fr,de,el,la,sa}/<author>/`,
indexed by `/home/li/Criopolis/library/bibliography.md` (1156
lines). The same MD5-hash naming convention is preserved.

An agent reading either repo's `AGENTS.md` and following its
instructions will look in the wrong place and conclude no
sources exist. Both `AGENTS.md` files need their bibliography
path corrected. This audit does not edit those files — the
correction is a coordination decision for the user (was the
standalone repo deprecated? Is the Criopolis library a fork or
a replacement?). Flagged as the first action item below.

The Criopolis library is actively curated. Recent jj history
shows commits dated 2026-05-02 and 2026-05-03 — *"catalog forum
round six acquisitions,"* *"catalog vedic depth round two
acquisitions,"* *"add public-domain classics wishlist
sources."* The library is alive; the Āyurvedic gap is a gap in
a moving target, not in a frozen archive.

## What exists, and how readable it is

The canonical Āyurvedic texts present on disk, with the
agent-readability test result for each:

| Canonical text | Edition / translator | Path | Format | Readable? |
|---|---|---|---|---|
| *Caraka Saṃhitā* (Vol I only) | Priya Vrat Sharma, Chaukhambha 2014 | `Criopolis/library/en/caraka/caraka-samhita-priya-vrat-sharma.pdf` | PDF, bilingual SA+EN | Yes — `pdftotext -layout` returns clean English with IAST artifacts only on dense Devanagari verses |
| *Suśruta Saṃhitā* (complete) | Kaviraj Kunjalal Bhishagratna, Cosmo (reprint of Calcutta 1907) | `library/en/susruta/susruta-bhishagratna-complete.pdf` + `…vol1.pdf` | PDF, English | Yes — clean English extraction; slight 19th-c. typography artifacts |
| *Aṣṭāṅga Hṛdaya* (3 vols) | K. R. Srikantha Murthy, Krishnadas Ayurveda | `library/en/vagbhata/vagbhata-astanga-hrdaya-srikantha-murthy.pdf` | PDF, bilingual SA+EN | Yes, but degraded — Devanagari portions render with diacritic artifacts (`As$äflgä` for *Aṣṭāṅga*); English clean |

That is the entire bṛhat-trayī presence on disk: three trees,
all in English translation, none in critical Sanskrit. Each is
agent-readable in its English layer; each loses fidelity in its
Sanskrit layer.

Adjacent classical Āyurvedic primary sources also present:

| Text / class | Edition | Path | Readable? |
|---|---|---|---|
| *Ḍāmar Tantra* (śivāmbu kalpa) | Lotus Press EN | `library/en/damar-tantra/damar-tantra-lotus.epub` | Yes — EPUB, plain text |
| *Śivāmbu Gītā* | G. K. Thakkar | `library/en/g-k-thakkar/shivambu-gita-thakkar.pdf` | Yes |
| *Haṭha Yoga Pradīpikā* | Muktibodhānanda, Bihar School | `library/en/svatmarama/hatha-yoga-pradipika-muktibodhananda.pdf` | Yes |
| *Gheraṇḍa Saṃhitā* | Mallinson, bilingual | `library/en/gheranda/gheranda-samhita-mallinson.pdf` | Yes |
| *Śiva Saṃhitā* | Mallinson | `library/en/siva-samhita/siva-samhita-mallinson.pdf` | Yes |

The *yogic-Āyurvedic* shared diet doctrine (cited extensively
in *Apathya* and *Cooking and Spices*) is well-sourced: HYP
1.57–59, Gheraṇḍa 5.21, Śiva 3.33 are all reachable.

Modern scholarship on Āyurveda — the tier that gives the
Anglophone reader philological access — is moderately
populated:

| Author / title | Path | Notes |
|---|---|---|
| Wujastyk, *The Roots of Ayurveda* (Penguin 1998) | `library/en/dominik-wujastyk/wujastyk-roots-of-ayurveda.pdf` | Selections w/ critical introduction; the sceptical counterweight |
| Wujastyk & Smith, *Modern and Global Ayurveda* | `library/en/dominik-wujastyk/wujastyk-smith-modern-global-ayurveda.pdf` | Reception history |
| Zysk, *Asceticism and Healing in Ancient India* | `library/en/kenneth-zysk/zysk-asceticism-healing-ancient-india.pdf` | Buddhist/early-Āyurvedic monastic medicine |
| Zysk, *Religious Medicine* | `library/en/kenneth-zysk/zysk-religious-medicine.pdf` | The Atharvaveda → Āyurveda bridge |
| Fields, *Religious Therapeutics* | `library/en/gregory-fields/fields-religious-therapeutics.pdf` | Comparative framework (Yoga / Āyurveda / hospice) |
| Frawley, *Yoga and Ayurveda* | `library/en/david-frawley/frawley-yoga-and-ayurveda.pdf` | Practitioner-side unity argument |
| Dasgupta, *History of Indian Philosophy* I–V | `library/en/surendranath-dasgupta/` | Vol II ch. XIII treats Āyurveda as philosophy |
| Larson, *Classical Sāṃkhya* | `library/en/gerald-larson/` | Caraka-as-pre-Īśvarakṛṣṇa Sāṃkhya |

The chloride-witnesses tier is unusually well-sourced (this is
the project's strongest evidentiary leg):

| Witness | Path | Notes |
|---|---|---|
| Hoelzel, *A Devotion to Nutrition* | `library/en/frederick-hoelzel/devotion-to-nutrition.zip` | IA per-page TXT; agent-readable via `unzip` |
| Dahl, *Excessive Salt Intake and Hypertension* | `library/en/lewis-dahl/dahl-excessive-salt-hypertension.zip` | IA per-page TXT |
| Graham, *Lectures on the Science of Human Life* | `library/en/sylvester-graham/graham-lectures-science-human-life.zip` | IA per-page TXT, ~600 pages |
| Liebig, *Animal Chemistry* | `library/en/justus-liebig/liebig-animal-chemistry.pdf` | Yes |
| Shelton, *Hygienic System Vol II* | `library/en/herbert-shelton/shelton-hygienic-system-vol2-orthotrophy.pdf` | Yes |
| Kempner, *Scientific Publications Vol II* | `library/en/walter-kempner/kempner-scientific-publications-vol-ii.pdf` | Yes |
| Newborg, *Walter Kempner and the Rice Diet* | `library/en/walter-kempner/newborg-kempner-rice-diet.pdf` | Yes |
| Fregly & Kare, *Salt in Cardiovascular Hypertension* | `library/en/salt-research/fregly-kare-...pdf` | Yes |
| Rettig, Ganten, Luft, *Salt and Hypertension* | `library/en/salt-research/rettig-ganten-luft-...pdf` | Yes |
| Kurlansky, *Salt: A World History* | `library/en/mark-kurlansky/kurlansky-salt-world-history.epub` | Yes |

The .zip files (Hoelzel, Dahl, Graham) are Internet Archive
per-page TXT dumps. They are agent-readable but cumbersome —
to find a passage, an agent must `unzip` and then `grep`
across hundreds of files named `00000NNN.txt`. A one-time
concatenation pass would convert each into a single
searchable document.

The substantive caraka-samhita repo at
`/git/github.com/LiGoldragon/caraka-samhita/` extends the
Caraka surface with chapter-level English markdown
(`sharma-2014/01-sutrasthana/…`), per-*sthāna* digests
(`sutrasthana.md`, `nidanasthana.md`, `vimanasthana.md`,
`sarirasthana.md`, `indriyasthana.md`), and one verified
philological note (`notes/philology/sutrasthana-5-12.md` on
the *saindhavān* question). All of this is plain markdown,
fully agent-readable. It is the cleanest Āyurvedic surface in
the workspace — but it covers only Caraka Vol I (5 *sthānas*,
66 chapters), not the clinical-therapeutics half (Cikitsā,
Kalpa, Siddhi).

## What is missing

The classical Āyurvedic canon contains substantially more than
what is on disk. The gaps:

| Missing text | Class | Why it matters |
|---|---|---|
| **Caraka Saṃhitā Vols II–VI** | bṛhat-trayī | The clinical-therapeutics half (Cikitsā, Kalpa, Siddhi). Without it, the project quotes only the doctrinal opening of Caraka. |
| **Sharma & Dash, *Caraka Saṃhitā with Cakrapāṇi's Āyurveda Dīpikā*** (7 vols, Chowkhamba) | bṛhat-trayī w/ commentary | Caraka with the canonical traditional commentary that resolves grammatical anomalies. caraka-samhita's own `notes/translation-sources.md` flags this **HIGH** priority. Without it, philological work in `notes/philology/` cannot reach definitive conclusions. |
| **Aṣṭāṅga Saṅgraha** (the longer Vāgbhaṭa) | bṛhat-trayī | The earlier and longer Vāgbhaṭa work; the *Aṣṭāṅga Hṛdaya* on disk is its summary. Some passages are recoverable only from the *Saṅgraha*. |
| **Mādhava Nidāna** (with Madhukoṣa commentary) | laghu-trayī | The diagnosis text. The whole *nidāna* / etiology vocabulary in Āyurveda is anchored here. Cited in Suśruta-tradition diagnoses; not reachable on disk. |
| **Śārṅgadhara Saṃhitā** | laghu-trayī | The pharmacy / prescription / dosage text — the substrate for everything *aṅga* about Āyurvedic preparation. Murthy's English translation is the standard. |
| **Bhāvaprakāśa** of Bhāvamiśra | laghu-trayī | The encyclopedic Materia Medica (16th c.). Foods, herbs, regimens; the canonical reference for any plant-substance argument. Krishnadas Academy edition is the standard. |
| **Cakradatta** of Cakrapāṇidatta | specialised compendium | Therapeutic compendium, organised by disease. The single most-cited classical Āyurvedic prescription manual. |
| **Yoga Ratnākara** | late therapeutic compendium | The 17th–18th-c. summary. Cited in modern Āyurvedic-college curricula; useful for cross-checking received doctrine. |
| **Aruṇadatta — *Sarvāṅga Sundarā*** | commentary | The principal traditional commentary on *Aṣṭāṅga Hṛdaya*. Resolves *Hṛdaya*'s compressed verses. |
| **Hemādri — *Āyurveda Rasāyana*** | commentary | Second major *Aṣṭāṅga Hṛdaya* commentary. |
| **Cakrapāṇidatta — *Āyurveda Dīpikā*** (standalone) | commentary | The Caraka commentary; partially included in Sharma & Dash above, but a standalone Sanskrit edition is what the philological work in caraka-samhita actually needs. |
| **Ḍalhaṇa — *Nibandha Saṅgraha*** | commentary | The principal Suśruta commentary. Without it, the Bhishagratna translation has no traditional gloss to check against. |
| **Meulenbeld, *A History of Indian Medical Literature*** (5 vols, Brill 1999–2002) | secondary | The reference work for *what is or is not Āyurvedic literature*. Currently *zero presence* despite an empty `library/en/jan-meulenbeld/` directory. The empty directory is itself a signal — it was created with intent to populate, never populated. |

In addition: the Sanskrit-language directories
`library/sa/ayurveda/` and `library/sa/yoga/` are *both
empty*. The project has no critical Sanskrit Āyurvedic edition
on disk in any language layer. Every classical citation
currently passes through one English translator's interpretive
hand. The `notes/philology/sutrasthana-5-12.md` analysis in
caraka-samhita (the *saindhavān* question) shows the cost of
this — the received Sharma English silently smooths over a
grammatical non-agreement that the Sanskrit makes visible.

Three further empty author directories are present but
unfilled: `library/en/sharma-dash/`, `library/en/bepin-behari/`,
`library/en/james-mallinson/`. These were created with
intent. The intent has not yet landed binaries.

## Why we cannot find them

The reasons divide into four named obstacles, each with a
known fix or a known why-not.

**1. annas-mcp HTTP timeout on large files.**
caraka-samhita's `notes/translation-sources.md` records the
Sen & Sen 1894 (72.5 MB) and Angot 2011 (52.5 MB) downloads
both failed mid-stream around 30 MB on 2026-04-23. The
`timeout` shell wrapper does not override the client's
internal HTTP timeout. The same obstacle would defeat any
Sharma & Dash volume (each is 70–200 MB).

*Fix.* Download via direct `curl` or `aria2c` from the Anna's
landing page (`annas-archive.gd/md5/<hash>`) with resumable
transfer. The `annas` CLI is for *finding* hashes; large file
retrieval should not go through it. This needs to be encoded
as a workspace skill — currently it is buried in one
caraka-samhita note and replays as a fresh failure each time
an agent reaches for `annas book-download` on a multi-volume
text. A short addition to a future bibliography skill should
state: *use `annas book-search` to discover; use `aria2c -c`
to download.*

**2. Devanagari OCR has not been run on public-domain editions.**
The 1922 Nirnaya Sagar edition of Caraka *with Cakrapāṇi's
Āyurveda Dīpikā commentary* is freely on Internet Archive (a
733 MB PDF, public domain). Its automatic OCR completely
failed on Devanagari — `_djvu.txt` returns CC-0 metadata
stamps and nothing else. A local Tesseract pass with `san`
language data, or a Google Cloud Vision pass, would unlock
the entire commentary tradition for free. This work has not
been scheduled.

The same diagnosis applies to any of the other freely
available Devanagari Āyurvedic texts — *Bhāvaprakāśa* (Internet
Archive has multiple 19th-c. editions), Sanskrit *Suśruta
Saṃhitā* (the Vidyāsāgar edition is on archive.org), Sanskrit
*Aṣṭāṅga Hṛdaya* (multiple editions). These are *findable*;
they are *not searchable* until an OCR pass is performed.

**3. The Brill HIML problem.**
Meulenbeld's *A History of Indian Medical Literature* (5 vols,
Brill 1999–2002) is the reference work for the entire field.
It is also a Brill set with original prices in the four-figure
range. Anna's Archive surfaces a Meulenbeld-edited 1987
World Sanskrit Conference proceedings volume
(`a84ebae8df0dc655507a220b1daf3b7a`) and a Cerulli volume,
but not the HIML 5-vol set. This is not a network failure — it
is a publisher gap. The HIML set has historically been hard
to torrent; libraries are the realistic path for it. An
inter-library loan request, or a Brill subscription via an
academic institution, would close this gap. A purchased copy
is also feasible; the set is still in print.

**4. Taxonomic gap — empty author directories that signal
intent.**
`library/en/sharma-dash/`, `library/en/jan-meulenbeld/`,
`library/en/bepin-behari/`, `library/en/james-mallinson/`,
`library/sa/ayurveda/`, `library/sa/yoga/`. Each was created
deliberately — `mkdir` does not happen by accident in a
curated repo. The empty state is a backlog, not an absence of
intent. The bibliography is being built up; these are the
*next acquisitions* if the cataloguing cadence continues.

## Anna's Archive availability snapshot

Searches run during this audit (subset; representative):

| Target | Found on Anna's? | MD5 / notes |
|---|---|---|
| Sharma & Dash *Caraka* Vol II | Yes | `724d10c448ea5542470cbbfe0a8029f6` (155.5 MB). Vol I and others searchable separately. |
| Sharma & Dash *Caraka* Śārīrasthāna | Yes (partial) | `037f1c66533e9a9701f4c8c2907bbda7` (11.8 MB). Already noted in caraka-samhita as a partial. |
| Mādhava Nidāna w/ Vijaya Rakshita commentary | Yes | `e2b566a80272fd905cf442a211332f2d` (0.5 MB, 1876 Vidyāsāgar, Sanskrit). Public domain. |
| Śārṅgadhara *Paddhati* (anthology, Sanskrit) | Yes | `8bdce08f83bda9831639d492767c95d7` (0.7 MB, 1888 Peterson). The *Saṃhitā* itself needs a separate query — Murthy's translation is the standard target. |
| *Aṣṭāṅga Hṛdaya* (Brahmanand Tripathi, Hindi+Sanskrit) | Yes | `f55c348b5812492f2db72995a949f560` (76.5 MB). |
| *Aṣṭāṅga Hṛdayam* (3-vol Murthy, on disk already) | Yes | `e58d87bd09fe58c8991e8a1d0019d792` — confirms the on-disk copy hash. |
| *Aṣṭāṅga Saṅgraha* | Mixed | The longer Vāgbhaṭa appears under different titles; needs targeted searches by translator (Athavale, Murthy). |
| *Bhāvaprakāśa* | Initial query unproductive | Returns mostly modern wellness titles. Needs query refinement (`"bhavamishra"`, `"sitaram bulusu bhavaprakasha"`). |
| Meulenbeld *HIML* 5-vol | No | Brill set; not surfaced. See obstacle 3 above. |

The pattern: **the public-domain classical Sanskrit texts are
generally findable on Anna's**; the modern critical English
translations are *partially* findable (parts of multi-volume
sets); the recent Brill scholarship is *not findable* and
needs a different acquisition path.

## The Sanskrit problem

The empty `library/sa/ayurveda/` is the audit's most
load-bearing absence. The project's argument repeatedly rests
on Sanskrit nuance — the *saindhavān lavaṇaṃ* compound, the
exact *atiyoga* verse, the IAST that distinguishes *snigdha*
from *snigdhā*, the genitive that decides whether *ghṛta* is
the subject or the object of a verse. None of this can be
verified against received translations alone; some translators
silently smooth, some translators silently choose. The
caraka-samhita repo has begun the discipline of verifying one
verse at a time (`sutrasthana-5-12.md` is the worked example),
but it does so against a *single* English translator and a
*partial* online Sanskrit (GRETIL covers only Caraka
Sūtrasthāna 1, 12, 26, 27, 28). For Sūtrasthāna 5, 6, 11, 13,
14, 15 — the chapters where the diet doctrine is most densely
stated — there is no critical Sanskrit on disk.

The asymmetry: the project asks the reader to take seriously
that *"chloride of sodium" is not "sodium chloride"* because
the linguistic ordering carries the toxicology. It then quotes
*Caraka Sūtrasthāna 26.43* against received English with no
Sanskrit cross-check on disk. The discipline applied to
chemistry vocabulary has not yet been applied to Sanskrit
philology.

## Recommendations, in priority order

**P0 — Path correction (one edit each, low cost).**
Update `TheBookOfSol/AGENTS.md` and
`caraka-samhita/AGENTS.md` to reference
`/home/li/Criopolis/library/` (or a chosen short alias for
it) instead of `~/git/bibliography/`. This is a dual-write —
both `AGENTS.md` files have the wrong path. Verify whether
the standalone `~/git/bibliography/` repo was deprecated
deliberately or whether it is supposed to coexist; resolve
the naming.

**P1 — Acquire Sharma & Dash 7-vol Caraka with Cakrapāṇi
commentary.** Already named HIGH in
`caraka-samhita/notes/translation-sources.md`. With Anna's
hashes for at least Vol II and Śārīrasthāna already in hand,
a `aria2c -c` campaign can land both within a few hours.
Continue search for Vol I, Vol III, Vol IV, Vol V, Vol VI by
volume name. This single acquisition unlocks the verified
philological pass on Caraka.

**P2 — Run Devanagari OCR on the 1922 Nirnaya Sagar Caraka +
Cakrapāṇi PDF.** Free, in-hand, blocked only by an OCR pass
nobody has scheduled. Tesseract `san` on the local PDF, or a
Google Cloud Vision call, produces a searchable text version
of the entire Cakrapāṇi commentary. After this lands, the
project has access to the canonical traditional commentary
without paying Brill prices.

**P3 — Begin populating `library/sa/ayurveda/` with one
canonical Sanskrit edition per text.** The minimum useful set:
Jādavji Trikamji Āchārya's critical Caraka, the Vidyāsāgar
1876 Mādhava Nidāna already located on Anna's, a Sanskrit
*Suśruta* (Nirṇaya Sāgara), and any *Aṣṭāṅga Hṛdaya* Sanskrit
edition. The annas-mcp timeout means using `aria2c` for
download. Each is < 1 GB.

**P4 — Fill the missing-laghu-trayī gap.** Mādhava Nidāna
(both Sanskrit and Murthy's English translation), Śārṅgadhara
Saṃhitā (Murthy's bilingual edition), Bhāvaprakāśa (Krishnadas
Academy bilingual). All exist as published bilingual editions;
all are findable; none are currently on disk. The laghu-trayī
absence is the single most surprising gap given how often the
project cites Caraka — these three texts are the medieval
reception of Caraka and the substrate for nearly every
classical Āyurvedic clinical claim younger than Vāgbhaṭa.

**P5 — Acquire Meulenbeld HIML through a non-Anna's path.**
The 5-vol set is the field's reference work. Brill subscription
via institutional access, inter-library loan, or purchased
copy. Without it, the project cannot *audit* its own claims
against the canonical literature-history record — it can only
quote translators who themselves rely on Meulenbeld.

**P6 — Concatenate the Internet Archive ZIPs into single
searchable text files.** Hoelzel, Dahl, and Graham each ship
as hundreds of `00000NNN.txt` files inside a ZIP. A
one-command pass per archive (`for f in $(ls); do cat "$f";
echo; done > devotion-to-nutrition.txt`) gives one searchable
document per witness. Cheap, immediately useful for
witness-quoting in chloride essays.

**P7 — Encode the Anna's-vs-aria2c distinction as a workspace
or library-repo skill.** Currently the timeout knowledge lives
in one caraka-samhita note. The next agent that hits it will
re-discover it from the same starting failure. A short addition
either to a `library/skills.md` (if the library repo grows one)
or to TheBookOfSol's bibliography conventions would make the
distinction load-bearing.

## Implications for TheBookOfSol's argument

Where the source layer is strong:

- **Chloride toxicology.** The strongest leg. Two centuries
  of clinical evidence are present and agent-readable
  (Bright's nineteenth-century work via secondary citation;
  Widal/Achard/Digne via Hoelzel and the salt-research
  monographs; Kempner directly; Dahl directly; Liebig
  directly; Shelton directly; Graham via IA-ZIP; Kurlansky
  for cultural history). The Chloride Indictment's evidence
  is fully sourced.

- **Yogic-Āyurvedic shared diet.** The HYP, Gheraṇḍa, Śiva
  Saṃhitā, and Bhagavad Gītā passages quoted in *Apathya*,
  *Cooking and Spices*, and *The Ambrosian Diet* are all
  reachable in their English editions on disk. The
  *mitāhāra* / *apathya* doctrine is well-sourced.

- **Caraka Sūtrasthāna doctrine.** Sharma's English
  translation is on disk; caraka-samhita has chapter-level
  markdown for Sūtrasthāna 1–30. The doctrinal claims about
  *agni*, *rasa*, *ojas*, *svastha*, *viruddha-anna* are
  reachable.

Where the source layer is thin:

- **Caraka clinical-therapeutics chapters (Cikitsā, Kalpa,
  Siddhi).** Vols II–VI of Sharma are not on disk. Any claim
  the project makes about Caraka's *therapy* doctrine
  (rasāyana, *naṣṭaja*, specific disease management) is
  currently unverifiable on local material.

- **Suśruta beyond what Bhishagratna paraphrases.** The
  Bhishagratna English is a 19th-c. paraphrase, not a
  philological translation. Suśruta-specific claims (the
  surgical doctrine, the *rakta-pitta* etiology, the *anna-ja
  tṛṣṇā* diagnosis) are reachable in English only.

- **Aṣṭāṅga Hṛdaya verses cited from memory.** The Murthy
  edition is on disk and readable, but the Sanskrit
  diacritics are mangled by the source PDF's typesetting.
  Citations of Vāgbhaṭa Sūtrasthāna 6.143, 6.147, 10.13,
  10.27, 10.34 in the chloride articles need to be checked
  against GRETIL's plain-text edition (referenced in
  `library/bibliography.md` line 612) verse by verse. This
  is procedural verification work, not a research gap.

- **Mādhava-Bhāvaprakāśa-Śārṅgadhara stratum.** Currently
  zero presence. The project does not yet cite these
  directly; if it begins to, the foundation must be acquired
  first.

- **Sanskrit philology generally.** The *saindhavān* worked
  example is the project's only verified-Sanskrit verse so
  far. Every other Sanskrit-quoting essay rests on the
  English translator's interpretive hand, with whatever
  silent smoothing that hand performed.

## Closing

The Āyurvedic source layer is not absent — the bṛhat-trayī
English is on disk, the chloride witnesses are densely
sourced, and the yogic-Āyurvedic primary corpus is reachable.
The layer is *thinner than the project's argument requires* in
three specific ways: Caraka beyond Vol I, the entire
laghu-trayī, and any critical Sanskrit. Each gap has a known
fix; only one (Meulenbeld HIML) requires money or institutional
access. The rest are procedural — `aria2c`, Devanagari OCR,
one cataloguing pass — and could be closed in a sustained
acquisition session of perhaps a weekend.

The single highest-leverage action is **path correction in
both `AGENTS.md` files**. Without it, every future agent will
look in the wrong place and conclude the library is empty.
The correction is one edit per file.
