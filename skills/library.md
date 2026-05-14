# Skill — research library

*The workspace's curated bibliography. When and how to consult
it; how to fetch new material.*

---

## What this skill is for

When a task wants depth — primary-source philosophy, formal
mathematics, ontology engineering, classical texts in a domain —
the workspace has a curated reference library. Use it. Don't
treat training-data priors as a substitute for actually reading
when the work is supposed to be deep.

The library is at:

```
~/primary/repos/library/
```

Per `~/primary/repos/library/CLAUDE.md`, this is *"the scholarly
foundation that sema's ontology is built on"* — classical
source texts (Ptolemy, Valens, Parasara, Lilly), modern
systematizers, category theory (Mazzola, Spivak, Zalamea),
correspondence systems, Vedic philosophy, and the project's own
work. Binary files (PDF, EPUB, DJVU) are gitignored locally and
indexed by Anna's Archive MD5 hashes; text-form bibliography is
in `~/primary/repos/library/bibliography.md`.

---

## Layout

```
~/primary/repos/library/
├── bibliography.md        — complete tiered bibliography with MD5 hashes
├── documentation-spec.md  — category-theoretic documentation framework
├── samskara-world-upgrade-plan.md — relation design notes
├── en/<author-name>/      — English sources (one dir per author)
├── fr/<author-name>/      — French
├── de/<author-name>/      — German
├── el/<author-name>/      — Greek
├── la/<author-name>/      — Latin
└── sa/<author-name>/      — Sanskrit
```

Author directories use lowercase-hyphenated naming (e.g.
`john-sowa`, `david-spivak`, `gottlob-frege`). Filenames inside
encode the work and translator/edition (e.g.
`conceptual-structures.pdf`,
`semantic-conception-truth-foundations-semantics.pdf`).

---

## When to consult the library

| Situation | Use library? |
|---|---|
| Foundational concept needs a real source (e.g. citing Sowa on intension/extension) | Yes — read the actual text |
| Cross-language audit (comparing two formal systems) | Yes — read the canonical references for each |
| Quick recall of a well-known fact | No — training data is fine; cite cautiously |
| Designing a new abstraction inspired by a known framework | Yes — verify the framework's actual claims, not my paraphrase |
| Audit / report meant to be deep | Yes — the library is the depth |
| Implementation detail, language reference | No — use the language's own spec |

When in doubt: if the task description asks for *depth* or
*research*, use the library. If a previous report drew on
secondhand training-data analogues and the user pushed back,
read the source.

---

## Reading from the library

PDFs are read via the `Read` tool with the `pages:` parameter:

```
Read /home/li/primary/repos/library/en/john-sowa/conceptual-structures.pdf pages:1-15
```

Notes:
- Maximum 20 pages per request — for long books, request in
  batches.
- For large PDFs (more than 10 pages), `pages` is mandatory.
- EPUB and DJVU are not directly supported by `Read` — convert
  via `ebook-convert` (Calibre, available via Nix) when needed:

```sh
nix run nixpkgs#calibre -- ebook-convert input.epub output.pdf
```

For DJVU:

```sh
nix run nixpkgs#djvulibre -- ddjvu -format=pdf input.djvu output.pdf
```

---

## Adding new books — the `annas` CLI

The CLI tool that searches and downloads from Anna's Archive is
a Go binary built from `~/git/annas-mcp` and installed on PATH
via the home-manager profile (`/home/li/.nix-profile/bin/annas`).
Invoke it as `annas`. If `which annas` returns nothing, fall back
to `find /nix/store -maxdepth 2 -name annas -type f 2>/dev/null`
and invoke by the nix-store path.

### Running it cleanly

Always invoke `annas` from the library directory so it finds
`.env`:

```sh
cd ~/primary/repos/library && annas book-search "<query>"
```

The CLI emits a noisy startup `WARN` line and Go stack trace
when `.env` is missing or empty; pipe through a filter when you
just want results:

```sh
annas book-search "<query>" 2>&1 \
  | grep -v "WARN\|Error loading\|cli.go\|main.go\|proc.go\|annas-mcp\|runtime.main\|StartCLI\|^github"
```

### Configure the environment

Two variables, both stored in `~/primary/repos/library/.env`:

```
ANNAS_SECRET_KEY=<API key from annas-archive.li>
ANNAS_DOWNLOAD_PATH=/home/li/primary/repos/library/<lang>/<author>/
```

The `.env` in `~/primary/repos/library/` is gitignored. As of
this skill's writing, the workspace runs **unauthenticated**
(searches work without a key; downloads may require one).

### Searching

```sh
annas book-search "category theory for sciences"
annas book-search "spivak ologs"
annas article-search "10.1038/nature12345"
annas article-search "neural networks"
```

The CLI prints results as a table with MD5 hashes. The MD5 is
what `bibliography.md` records.

### Downloading

```sh
annas book-download <md5-hash> "filename.pdf"
annas article-download "10.1038/nature12345"
```

Filename should follow the workspace convention: lowercase-
hyphenated, encoding work + translator (e.g.
`category-theory-for-sciences.pdf`,
`tetrabiblos-robbins-loeb.pdf`).

### Adding to the bibliography

After downloading, add to `~/primary/repos/library/bibliography.md`
in the appropriate tier and author section. The format follows
the existing entries:

```markdown
### Author Name — Work Title (date)
Short description of why this work is here.
- `en/author-name/` — Translator/edition: `<md5-hash>`
```

The MD5 hash is what survives the gitignored binary; if a
machine loses the local file, the MD5 is the bridge back to
Anna's Archive.

---

## What the library contains today (workspace highlights)

This isn't an exhaustive list — see `bibliography.md` for the
full tiered version. Just orientation by domain:

| Domain | Authors |
|---|---|
| Knowledge representation | Sowa (Conceptual Structures), Guarino (Handbook on Ontologies) |
| Category theory | Spivak, Mazzola, Zalamea |
| Type theory & natural language | Aarne Ranta (Grammatical Framework) |
| Logic & philosophy of language | Frege (Sense and Reference), Tarski (Semantic Conception of Truth), Wittgenstein (Philosophical Investigations), Quine (Two Dogmas), W.V.O. Quine (others) |
| Classical philosophy | Aristotle (Categories, Metaphysics, Posterior Analytics, Ethics), Plato, Plotinus |
| Indian philosophy | Patanjali, Sankara, Nagarjuna, Bhartrhari, Abhinavagupta, Mimamsa, Nyaya |
| Astrology (sema's domain) | Ptolemy, Valens, Firmicus, Lilly, Brennan, George, Lehman |
| Linguistics | Halliday, Tesnière, Mel'čuk, Sowa |
| Pattern languages | Christopher Alexander |
| Hermeticism / correspondence | Hermes Trismegistus, Crowley, Skinner |

When picking a foundational citation, the right move is
usually:
- For knowledge representation / ontology: **Sowa**.
- For category-theoretic data modeling: **Spivak**.
- For meaning-of-meaning: **Frege**, **Wittgenstein**, **Quine**.
- For formal definitions of truth and model theory: **Tarski**.
- For categorial semantics of natural language: **Aarne Ranta**.
- For domain-specific (sema's astrology): **Ptolemy**, **Valens**.

---

## Citing in reports

When a designer report draws on a library text, cite it
explicitly with author + year + title + section, plus the local
path:

```markdown
- **Sowa, J. F. (1984).** *Conceptual Structures: Information
  Processing in Mind and Machine.* Addison-Wesley.
  Chapter 1 §1.4 (Intensions and Extensions).
  Local: `~/primary/repos/library/en/john-sowa/conceptual-structures.pdf`
```

This makes citations falsifiable: the next agent reading the
report can verify the claim by reading the same page range.

If a claim *paraphrases* without reading: say so. *"Per my
prior knowledge of Frege's sense/reference distinction"* is
fair, *"Frege showed in §2 that..."* is a citation that should
correspond to actual reading.

---

## Anti-patterns

- **Citing without reading.** Drive-by mentions of "as Sowa
  showed" without page references is the failure mode this
  skill exists to prevent.
- **Reaching for training-data analogues for deep work.** When
  a task asks for depth, training-data familiarity with a name
  is not the same as the named work's actual claims.
- **Adding to the library without the bibliography update.**
  Files in author directories that aren't in `bibliography.md`
  drift; future agents won't find them by topic search.
- **Treating the library as canonical workspace state.** The
  library is `~/primary/repos/library/`, not under `~/primary/`.
  It's a sibling resource. Don't move references to it inside
  `~/primary/`.

---

## See also

- `~/primary/repos/library/CLAUDE.md` — the library's own
  agent-facing intro.
- `~/primary/repos/library/bibliography.md` — the full curated
  index.
- `~/primary/repos/library/documentation-spec.md` — the
  category-theoretic documentation framework that organizes
  the library.
- `~/git/annas-mcp/README.md` — the source repo for the CLI
  tool.
- `~/primary/skills/reporting.md` — when reports cite library
  texts, the citation form belongs in the report's "See also"
  with the local file path (per this skill's "Citing in
  reports" section).
- `~/primary/ESSENCE.md` §"Rules find their level" — workspace
  tooling lives at the workspace level; this skill is the
  canonical home for library use.
