# Vision-OCR trial pass on caraka-1922 + scan-quality audit of remaining Tier S/A/B candidates

*Poet · 2026-05-09*

The 1922 Nirṇaya-Sāgara *Caraka with Cakrapāṇi Dīpikā* PDF cannot
be OCR'd at any quality grade. The book has been removed from the
library. The next vision-OCR target is **Plutarch Moralia V
(Isis-Osiris)** — Tier S, no existing text layer, exceptionally
clean scan, Greek alphabet (vision-OCR-friendly), and the most-cited
Western primary in *The Chloride Indictment* and *Witnesses Against
Salt — Greek*.

A second Sanskrit primary, the 19th-c. Vidyāsāgara *Caraka*
(`charakasanhita-vidyasagara-sanskrit.pdf`), shows the same scan
pathology and is flagged for trial-test before any further budget
commitment.

## Trial pass

A 36-page calibration run against
`sa/ayurveda/caraka-with-cakrapani-dipika-1922-nirnaya-sagar.pdf`
was dispatched as 6 parallel Claude vision-OCR subagents (6 pages
each, 300 DPI PNG inputs, structured-markdown outputs in
`library/.vision-ocr/caraka-1922-nirnaya-sagar/text/`). Two agents
completed before cancellation; the rest produced partial output.

The transcriptions divide cleanly into two layers:

**Layer 1 — large display type (title page, chapter headings).**
Excellent. Page 1 was transcribed faithfully:

> *agniveśamaharṣikṛtā carakapratisaṃskṛtā*
> *śrīcarakasaṃhitā*
> *śrīmaccarakacaturānanaśrīcakrapāṇidattapraṇītayā…*

Editor (Vāmana-śāstri Vaidyabhūṣaṇa of Janasthāna), publisher
(Pāṇḍuraṅg Jāvajī, Nirṇayasāgara), and date (Śaka 1843 = 1921–22 CE)
were extracted accurately. Library stamps and handwritten accession
numbers were correctly relegated to the `## Notes` section rather
than polluting the main content.

**Layer 2 — body type (prefaces, indices, commentary).** Failure.
Pages 3–4 (the editor's Sanskrit prose preface) degenerated into
roughly four lines of plausible-looking Devanagari followed by
hallucinated ligature noise:

> `[?]जन्थ्ल्न्द्रि[?]व्र्र्र्व्न्क्न्व्र्क् भ्र्न्ज्व्र्व्र्न्ज्व्व्न्त्न्र्र्ष्व्र्व्व्र्ज्ज् । ब्व् व् व्व्व्व्व्व्व्ज्व्व्ज्व्ज्ल्द्र्न्तज्व्व्न्नज्व्र् व्ब् ज्व् व्ब् [?]`

The agent itself flagged this in the page's `## Notes`:

> "The fine print on this page is **severely degraded** in the
> scan. Significant portions of the lower half of the page
> (especially the last 4–5 lines) are nearly illegible — the
> 'transcription' there is largely speculative pattern-matching
> against blurred shapes and should not be trusted as accurate.
> A high-resolution rescan is recommended before this page is
> promoted."

Page 8 (a four-column topic index) was worse: the agent recognised
the table structure but most cell contents read
`द्ज्ज्ञ्द्द्व्द्द्व्द्द्व्द्र्द्व्र्द्द्व्द्द` —
random ligature pattern noise.

The pattern is unmistakable: when the source ink dropped below the
threshold of clean character extraction, the vision agents *kept
producing characters* rather than refusing or marking the section
as unrecoverable. The `[?]` discipline held for individual glyphs;
it did not hold for entire paragraphs. This is a known mode of
failure for vision OCR on extremely degraded sources, and it
warrants caution: future vision-OCR work on questionable scans
should include a sanity check that a human (or a second-pass
agent) flag whole regions as unreadable, not just individual
glyphs.

**Verdict:** the source PDF is unrecoverable. Tesseract was already
known to produce broken output on this scan; the vision pass
confirms the limit is the source, not the OCR method. Removed.

## Scan-quality audit of remaining candidates

To answer "what's the next-best candidate?" I sampled one
representative body page from each Tier S/A/B target in
`library/ocr-targets.md` (skipping front matter, picking pages at
~25% depth). Two probes per book:

1. **`pdftotext` byte-count probe.** Substantial output ⇒ the PDF
   has an embedded text layer; vision OCR adds value mostly by
   restoring layout, not by extracting characters from images.
   Empty/near-empty output ⇒ no text layer; vision OCR adds maximum
   value.
2. **300 DPI page render + visual inspection.** Determines whether
   the source is sharp enough that vision OCR can extract
   characters at all.

Sample pages and probe outputs are kept in
`library/.vision-ocr/audit-samples/` (gitignored).

### Per-target findings

| Path | Tier | Text layer | Scan quality | Verdict |
|---|---|---|---|---|
| `en/plutarch/plutarch-moralia-v-isis-osiris.pdf` | S | none | excellent | **Next vision-OCR target.** |
| `en/patanjali/patanjali-arya-vyasa-bhasya.pdf` | A | none | excellent (modern Indian press) | Strong. |
| `en/atharva-veda/atharva-veda-whitney-vol1-books-i-vii.pdf` | A | present, layout-broken | excellent | Vision OCR for layout repair. |
| `en/atharva-veda/atharva-veda-whitney-vol2-books-viii-xix.pdf` | A | present, layout-broken | excellent | Pair with vol 1. |
| `en/upanisads/radhakrishnan-principal-upanisads.pdf` | A | none | moderate (faded diacritics) | Trial-test before commitment. |
| `en/plutarch/plutarch-moralia-viii-table-talk.pdf` | A | present, Greek-corrupted | moderate | Vision OCR fixes Greek apparatus. |
| `en/yoga-upanisads/ayyangar-yoga-upanisads.pdf` | B | none | good (clean Devanagari) | Trial-test recommended. |
| `en/plutarch/plutarch-moralia-xii-de-facie-cherniss.pdf` | B | present | moderate (lower DPI) | Marginal. |
| `en/arthur-avalon/avalon-serpent-power-shatchakranirupana.pdf` | B | present, layout-broken | excellent | Vision OCR for layout repair. |
| `sa/ayurveda/charakasanhita-vidyasagara-sanskrit.pdf` | A | present, corrupted | **marginal — same era/quality as the rejected 1922** | **Flag for trial-test; possible removal.** |

`pdftotext` byte counts on the sampled pages, for the record:

```
atharva-vol1-p160 — 3141 bytes
atharva-vol2-p160 — 2834 bytes
avalon-p190       — 2033 bytes
plutarch-viii-p140 — 1658 bytes
plutarch-xii-p155 — 1938 bytes
vidyasagara-p250  — 3475 bytes (corrupted)
ayyangar-p150     —    1 byte (no text layer)
patanjali-p130    —    1 byte
plutarch-isis-p130 —   1 byte
radhakrishnan-p240 —   1 byte
```

## The next-best target: Plutarch Moralia V (Isis-Osiris)

Path: `library/en/plutarch/plutarch-moralia-v-isis-osiris.pdf`.
529 pp Loeb edition (Greek `grc` + English facing pages). No
existing text layer; the scan is exceptionally crisp.

This is the highest-leverage candidate for three reasons:

1. **Tier S** in `ocr-targets.md`. Contains the Isis-priests
   salt-refusal passages — the most-cited Western primary in
   *The Chloride Indictment* and *Witnesses Against Salt — Greek*.
2. **Vision OCR's marginal value is maximal.** No text layer means
   the choice is "have the text in machine-readable form, or
   don't."
3. **The source is vision-OCR-friendly.** The Greek alphabet has
   far fewer ligatures than Devanagari; Loeb pages are
   typographically clean and well-margined; facing-page
   bilingual structure is regular and parseable.

Estimated pass cost (extrapolating from the trial): roughly 8
minutes wall-clock for 36 pages with 6-way parallelism, so
~2 hours wall-clock for all 529 pages, assuming similar
per-page agent cost. Should be funded from the next available
vision-OCR budget window.

## Standing question: the Vidyāsāgara Sanskrit Caraka

`library/sa/ayurveda/charakasanhita-vidyasagara-sanskrit.pdf`
(1011 pp, Tier A) is the only remaining 19th-c. Sanskrit
Devanagari source on disk. The audit page (p. 250, mid-Cikitsā)
shows the same ghosting / ink-bleed pattern that doomed the 1922
Nirṇaya-Sāgara — characters are blurry but distinguishable to a
human reader. Whether vision OCR will resolve to clean Devanagari
or descend into the same hallucinated-ligature noise is genuinely
uncertain.

**Recommendation:** trial-test 12–36 pages of Vidyāsāgara at
budget-allocation time. If the `[?]`-rate / hallucination-rate
matches the rejected caraka-1922 pattern, remove this book also.
If it produces clean output, promote to a full pass.

The OCR-targets file marks this as `[?]` (trial-recommended); see
`library/ocr-targets.md` for the new status legend.

## Disposition

The following were removed on 2026-05-09:

- `library/sa/ayurveda/caraka-with-cakrapani-dipika-1922-nirnaya-sagar.pdf` (55 MB)
- `library/sa/ayurveda/caraka-with-cakrapani-dipika-1922-nirnaya-sagar.ocr.txt` (7.6 MB Tesseract sidecar)
- `library/.vision-ocr/caraka-1922-nirnaya-sagar/` (gitignored vision-OCR scratch)

Documentation was updated:

- `library/bibliography.md` — entry for the 1922 PDF deleted.
- `library/ocr-targets.md` — Tier S #1 entry removed; added new
  status markers `[?]` (trial-recommended) and `[X]` (tested
  unrecoverable); added "Removed from the library" section
  preserving the trail; refreshed totals.
- `caraka-samhita/notes/translation-sources.md` — moved 1922
  Nirṇaya-Sāgara entry from "Editions on the wish-list" to a new
  "Editions tested and rejected" section; rewrote priorities.
- `caraka-samhita/notes/philology/sutrasthana-5-12.md` — updated
  the four references to acquiring Cakrapāṇi commentary via the
  1922 IA scan.
- `caraka-samhita/README.md` — removed the 1922 Nirṇaya-Sāgara
  wish-list bullet and updated the example sibling-edition list.
- `caraka-samhita/sharma-2014/README.md` — fixed the stale
  `~/git/bibliography/` path and replaced the 1922 alternate-
  edition reference with the Sharma/Dash 7-volume set.
- `caraka-samhita/sharma-2014/CONVENTIONS.md` — replaced
  `nirnaya-sagar-1922/` example sibling dir with
  `trikamji-critical/`.
- `caraka-samhita/AGENTS.md` — replaced 1922 from the example
  sibling-edition list; fixed the broken `../bibliography/CLAUDE.md`
  link to `../library/CLAUDE.md`.

The `library/.vision-ocr/audit-samples/` directory is left in
place (gitignored) for any future audit pass that wants to
reuse the sample images and pdftotext probes.

## Method note for future passes

Vision OCR's failure mode on this trial is worth recording:
**agents do not refuse cleanly when the source is unreadable.**
They mark individual uncertain glyphs `[?]` (good) but they keep
producing plausible-looking ligature noise to fill the page when
the underlying scan is too poor to support character recognition
at all (bad).

For future vision-OCR passes on questionable scans, a useful
prompt addition would be: *"If a region of the page (a paragraph,
a column, or the whole page) is too degraded to support
character-level transcription, mark the entire region
`[unreadable: <reason>]` and stop transcribing it. Do not fill
the space with plausible-looking ligature noise."*

This finding should be folded into the workspace skill on
agent-driven OCR if and when one is written.
