# 64 — Āyurvedic source acquisition pass

*Action log following report 62. What was hunted, what landed,
what remained blocked, and where the wall sits.*

## Frame

Report 62 (`reports/poet/62-ayurvedic-source-audit.md`) named the
gaps in the project's Āyurvedic source layer: laghu-trayī absent,
Sanskrit primaries absent, major commentaries absent,
Sharma & Dash 7-vol Caraka high-priority and unacquired. This
pass executed against that gap list using the `annas` CLI on
top of the existing Criopolis library at
`/home/li/Criopolis/library/`.

## What landed

Nine new Āyurvedic primary-source files, all registered in
`/home/li/Criopolis/library/bibliography.md` in the same commit
that placed them.

The most consequential single find was already on disk and
unrecognised: **the 1922 Nirnaya Sagar *Caraka Saṃhitā* with
Cakrapāṇi's *Āyurveda Dīpikā* commentary** had been sitting in
`/tmp/caraka-dipika.pdf` since 2026-05-03 from a prior session
that never moved it into the library. 64 MB, 733 pages, PDF
real format, image-only Devanagari. Identified by `pdfinfo`
metadata + page count matching report 62's wishlist note.
Now placed at:

`sa/ayurveda/caraka-with-cakrapani-dipika-1922-nirnaya-sagar.pdf`
— MD5 `549e679c4fa376674123e3c1f6dea19b`. Public-domain. Needs a
local Devanagari OCR pass (Tesseract `san` or Google Cloud Vision)
to become searchable; without OCR it is image-only.

The other eight acquisitions:

| # | Text | Edition | Path | Size | Format |
|---|---|---|---|---|---|
| 1 | *Caraka Saṃhitā* (Sanskrit) | Vidyāsāgara, real PDF | `sa/ayurveda/charakasanhita-vidyasagara-sanskrit.pdf` | 31.7 MB | PDF |
| 2 | *Caraka* w/ Cakrapāṇi (Sanskrit OCR) | Harināth Viśārada, IA bundle | `sa/ayurveda/caraka-cakrapani-harinatha.zip` | 0.8 MB | OCR-text ZIP |
| 3 | *Caraka Saṃhitā* (Sanskrit OCR alt) | Vidyāsāgara, IA bundle | `sa/ayurveda/charakasanhita-vidyasagara-alt.zip` | 1.0 MB | OCR-text ZIP |
| 4 | *Mādhava Nidāna* w/ Vijaya Rakṣita commentary (Sanskrit OCR) | Vidyāsāgara 1876, IA bundle | `sa/ayurveda/madhava-nidana-vidyasagara-1876.zip` | 0.5 MB | OCR-text ZIP |
| 5 | *Cakradatta* (Sanskrit OCR) | Vidyāsāgara, IA bundle | `sa/ayurveda/cakradatta-vidyasagara.zip` | 0.5 MB | OCR-text ZIP |
| 6 | *Suśruta Saṃhitā* Vol III (Bhishagratna Uttaratantra) | 1907 | `en/susruta/susruta-bhishagratna-1907-vol3-uttaratantra.pdf` | 26.1 MB | PDF |
| 7 | *Suśruta Saṃhitā* Bhishagratna Vols I, II, III (Sanskrit/English OCR) | 1907 IA bundles | `sa/ayurveda/susruta-bhishagratna-1907-vol{1,2,3}-ocr-bundle.zip` | 0.5–0.8 MB each | OCR-text ZIP |
| 8 | *Aṣṭāṅga Hṛdayam* Vol II (Murthy, Nidāna+Cikitsita+Kalpasiddhi) | Krishnadas Academy | `en/vagbhata/vagbhata-astanga-hrdaya-murthy-vol2-nidana-cikitsita-kalpasiddhi.pdf` | 33.9 MB | PDF |
| 9 | *Śiva Saṃhitā* (Vasu, alt edition Sanskrit+English) | Srisa Chandra Vasu | `en/siva-samhita/siva-samhita-vasu-sanskrit-english.pdf` | 5.7 MB | PDF (image-only) |

Closing the laghu-trayī gap fully would require Bhāvaprakāśa
and Śārṅgadhara Saṃhitā, both still missing (see below).
**Mādhava Nidāna and Cakradatta are now reachable** as Sanskrit
OCR text — a substantive jump from report 62's "zero presence"
state.

## The IA-OCR-ZIP discovery

Report 62 anticipated downloading PDFs. What the small-hash
results from `annas book-search` actually serve, for many 19th-c.
public-domain editions, is **Internet Archive per-page OCR text
bundles**: ZIP files of `00000NNN.txt` files containing OCR'd
text from the underlying scan. These are mis-extensioned as
`.pdf` by the metadata but are agent-readable as text after
`unzip`.

The OCR is mixed-quality — clean for printed English, mixed for
printed Devanagari, poor for handwritten or marginal text. A
quick spot-check on `madhava-nidana-vidyasagara-1876.zip`
returned legible Sanskrit (`ज्वर-निदानम्` / *jvara-nidānam*) on
the test page. So these bundles are useful for `grep`-able
verse retrieval even where the OCR is imperfect — they unlock
keyword searches across Sanskrit primaries that were previously
inaccessible without on-disk text.

Practical convention: rename `.pdf` → `.zip` after download, or
register both. Per-page TXT is enumerable with
`unzip -p file.zip <page>.txt`.

## What remained blocked

The `annas-mcp` CLI's internal HTTP-client timeout caps any
single download at roughly the first ~15–48 MB, regardless of
the bash-tool's foreground or `run_in_background` mode. Two
attempted background downloads of large targets failed mid-stream:

| Target | MB | Got to | Outcome |
|---|---|---|---|
| Sharma & Dash *Caraka* Vol II | 155.5 | 13.2 MB | `context deadline exceeded (Client.Timeout)` |
| Sen & Sen 1894 *Caraka* | 72.5 | 16.4 MB | same |

Earlier (foreground, 600s cap):

| Target | MB | Got to | Outcome |
|---|---|---|---|
| *Aṣṭāṅga Hṛdayam* Vol II Murthy | 33.9 | 33.9 MB ✓ | succeeded after retry — borderline |
| Bhishagratna *Suśruta* DJVU 1907 part 1 | 15.2 | 0 | API key required ("fast download member") |
| Sharma & Dash *Caraka* Śārīrasthāna | 11.8 | 0 | API key required |

The Vol II Murthy succeeded on a foreground retry; Sen-Sen and
Sharma & Dash Vol II failed even with `run_in_background`. The
governor is annas-mcp's own HTTP timeout, not the bash
runtime.

**Two acquisition routes remain blocked:**

1. **No mirror outside Anna's exists for the file** — the
   download path returns "API request failed with status 400"
   demanding the `key` (Anna's Archive *fast-download* member
   API key). Sharma & Dash Śārīrasthāna and the Bhishagratna
   DJVU Vol I both fall here. Files in this category cannot be
   acquired via this CLI without a paid Anna's membership.

2. **A non-Anna's mirror exists but the HTTP client times out
   before completion** — the download starts, transfers
   10–50 MB, then is killed by annas-mcp's internal client
   deadline. Sharma & Dash Vol II (155 MB) and Sen-Sen (72 MB)
   fall here. These would be acquirable with a tool that
   supports resumable HTTP (`aria2c -c`), pointed at a direct
   non-DDoS-Guarded mirror URL — but `annas-archive.gd`'s
   `slow_download` URL goes through a JS challenge that raw
   `curl` / `aria2c` cannot solve.

## What was confirmed unfindable

The following were searched aggressively (multiple query
variants, including translator names, publisher names,
"treatise on Hindu medicine" pattern, and Sanskrit
transliterations) and surfaced nothing usable on Anna's:

- **Bhāvaprakāśa** (Bhāvamiśra). Not on Anna's in any English
  translation, Sanskrit critical edition, or 19th-c. IA bundle
  form. The Krishnadas Academy bilingual edition is the
  standard target.
- **Śārṅgadhara Saṃhitā** (the Āyurvedic pharmacy text — not
  to be confused with Śārṅgadhara's *Paddhati* anthology, which
  *is* findable but is a literary work, not Āyurvedic). The
  Murthy English translation is the standard target.
- **Yoga Ratnākara**. Not surfaced under any of: "yoga
  ratnakara," "yogaratnakara," "Indian medicine," "Hindu
  medicine treatise." The 17th-c. compendium is genuinely hard
  to source online.
- **Aṣṭāṅga Saṅgraha** (the *longer* Vāgbhaṭa work, distinct
  from *Aṣṭāṅga Hṛdaya*). Searches return only *Hṛdaya*
  editions despite explicit "Saṅgraha" and "vrddha vāgbhaṭa"
  query terms.
- **Major commentaries standalone** — Aruṇadatta's *Sarvāṅga
  Sundarā* on *Aṣṭāṅga Hṛdaya*, Hemādri's *Āyurveda Rasāyana*,
  Ḍalhaṇa's *Nibandha Saṅgraha* on *Suśruta*. Not surfaced in
  searchable form.
- **Meulenbeld *A History of Indian Medical Literature*** (5
  vols, Brill 1999–2002). Confirms report 62: this Brill set is
  not on Anna's and needs an institutional / purchase route.

The pattern: **the bṛhat-trayī plus *Mādhava Nidāna* and
*Cakradatta* were preserved in the late-19th-c. Vidyāsāgara
publication tradition** which Internet Archive scanned and
OCR'd. The laghu-trayī's other two members (Bhāvaprakāśa,
Śārṅgadhara Saṃhitā) and the major commentaries were not in
that tradition's output, and are accordingly missing from the
free public corpus today.

## Implications for report 62's priorities

| 62 Priority | Status after this pass |
|---|---|
| **P0** path-correction in TheBookOfSol/AGENTS.md and caraka-samhita/AGENTS.md | unchanged — still pending user decision |
| **P1** Sharma & Dash 7-vol Caraka with Cakrapāṇi commentary | partial — Vol II and Śārīra-sthana hashes known but blocked behind API key / HTTP timeout. Vol I, III–VI still unidentified |
| **P2** Devanagari OCR on the 1922 Nirnaya Sagar PDF | **unblocked** — the PDF is now in `sa/ayurveda/` ready for the OCR pass |
| **P3** populate `library/sa/ayurveda/` with at least one canonical Sanskrit edition per text | **substantially closed** — 9 files now present, covering Caraka (3 ways), Suśruta (3 OCR vols), Mādhava Nidāna, Cakradatta, and the 1922 Cakrapāṇi |
| **P4** acquire missing laghu-trayī | partial — Mādhava Nidāna landed (Sanskrit only); Cakradatta landed; Bhāvaprakāśa and Śārṅgadhara Saṃhitā **confirmed unfindable** on Anna's, need different acquisition path |
| **P5** Meulenbeld HIML | unchanged — confirmed unfindable on Anna's |
| **P6** concatenate IA-ZIPs into searchable text | unchanged — quick win still pending |
| **P7** encode the Anna's-vs-aria2c distinction as a skill | new finding to encode: the **API-key wall** is the *named obstacle*, not just timeout. The free public path serves files via libgen.li / z-lib.gd / IA mirrors when those mirrors exist; files Anna's-only are gated. The diagnosis "annas-mcp times out" was incomplete — *some* files time out (large but with non-Anna's mirror), *others* fast-fail with a JSON 400 demanding a `key` field |

## Recommended next actions

1. **Run Devanagari OCR on the 1922 Cakrapāṇi PDF.** Free; the
   file is on disk; Tesseract `san` or Google Cloud Vision both
   work. Output a searchable text alongside the image PDF.
   This is the highest-leverage zero-cost action remaining.

2. **Decide on Anna's Archive membership.** A paid membership
   (USD $5/month at last check) unlocks the API-key gated
   files: Sharma & Dash 7-vol, Bhishagratna DJVUs, multi-volume
   Sanskrit critical editions. With the key, the entire blocked
   tier becomes scriptable.

3. **For the unfindable laghu-trayī (Bhāvaprakāśa, Śārṅgadhara
   Saṃhitā, Yoga Ratnākara, Aṣṭāṅga Saṅgraha):** these need a
   non-Anna's path — direct purchase from Chaukhamba / Krishnadas
   Academy / Vedic Books, or institutional library access, or a
   targeted manual search at a different Sanskrit-text repository
   (sanskritdocuments.org, GRETIL, archive.org via direct item
   ID).

4. **Update the path-correction in TheBookOfSol/AGENTS.md and
   caraka-samhita/AGENTS.md** (report 62 P0). This pass added
   substantively to the Criopolis library; the AGENTS.md files
   still tell agents to look in `~/git/bibliography/`. Each
   future agent re-discovers the wrong path and starts fresh.

5. **Concatenate the IA-OCR ZIPs into single searchable text
   files.** One short loop per archive:
   ```
   for z in /home/li/Criopolis/library/sa/ayurveda/*-ocr-bundle.zip; do
     base="${z%.zip}"; mkdir -p "$base"
     unzip -d "$base" "$z" > /dev/null
     find "$base" -name '*.txt' | sort | xargs cat > "${base}-concat.txt"
   done
   ```
   This converts the per-page bundles into a single grep-able
   text per text. Recommended for the same reason as the
   chloride-witness IA-ZIPs in report 62 P6.

## Closing

The Sanskrit primary layer is no longer empty. Nine files
landed; the most consequential (1922 Cakrapāṇi Dīpikā) was on
disk all along. The remaining hard gaps — Bhāvaprakāśa,
Śārṅgadhara Saṃhitā, Yoga Ratnākara, Meulenbeld HIML — are
gaps in the *free public corpus* itself, not gaps in this
machine's local copy of it. They cannot be closed by a more
aggressive `annas` pass; they need a different acquisition
channel.

The single under-100-USD action that would close the largest
remaining gap is **Anna's Archive membership** — it unlocks
Sharma & Dash 7-vol, Bhishagratna DJVUs, and the Sanskrit
critical editions in one move.
