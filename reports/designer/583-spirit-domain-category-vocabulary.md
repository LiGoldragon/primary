# Spirit — the category vocabulary, researched and seeded

The resolved answer to "research and create a starting category set, and is
`category` even the right term?" Grounded in the knowledge-organization literature
(Hjørland's domain analysis, Ranganathan's faceted tradition, ANSI/NISO Z39.19
thesaurus discipline, the Propædia outline, IAB / DMOZ / WordNet / ATUS, the
wellbeing "life domains" frameworks, and the library's Aristotle/Sāṃkhya bedrock).
This supersedes the category direction in `581`/`582` (and finally retires the 12
gerunds). Method: a 9-agent research+synthesis fan-out (`wf_d04c4bdc-6aa`).

## 1. The term — two tiers: `domain` › `category`

The single most-backed structural finding: **every grounded classification that
actually scales ships two tiers** — a small near-frozen top over a large growable
bottom (IAB: stable Tier-1 over 1,500+ leaves; ATUS: 17 majors over ~400 codes;
DMOZ: 16 frozen tops; WordNet: 45 frozen lexnames; Propædia: 10 parts over 167
sections). So Spirit wants two terms, not one. The answer to "another term?" is yes
— for the broad tier:

- **`domain`** = the broad sphere (the ~24 near-frozen tops). It's the one word
  that names *both* a knowledge-domain (medicine, law, category-theory) *and* a
  life-domain (parenting, money, grief) — exactly what *intent* needs, since intent
  spans both. It carries a real pedigree on both sides (Hjørland's "domain analysis";
  the wellbeing literature's "life domains") and, crucially, **no small-fixed-set
  connotation** — it doesn't lie about "hundreds."
- **`category`** = the specific grounded leaf (the taggable unit a record files
  into; ~196 to seed, growing to hundreds). Kept deliberately: it's idiomatic for
  exactly this — IAB calls its 1,500 leaves "categories" — it matches your own
  phrasing ("hundreds of categories"), and it's the live Rust type. We keep the word
  and **discard its Aristotelian reading**: a category here is a concrete
  controlled-vocabulary focus (the SKOS-concept / LCSH-subject / IAB-leaf sense),
  *not* a "fundamental kind of being." The 12 gerunds failed precisely because they
  used `category` in that closed-supreme-kinds sense.

Rejected: `topic` (poisoned — the old bloated free-text field you already renamed
away from), `facet` (a facet is an *axis* like time/place/agent, not a subject —
reserved for §6), `concept` (too abstract for "what is this intent about"), `subject`
(KO-pure but reads bibliographic; viable as the leaf if you dislike `category`'s
local history). If you want a single term, it's `domain` — but the evidence says take
the two tiers.

**The anti-failure rule that makes this work: records file at the `category` leaf,
never at the `domain`.** The gerunds failed (81% ambiguous, 65% in one bucket)
because records filed *at the abstract level*. Demote the breadth to a non-filing
curation index and the top tier no longer has to be mutually exclusive — domains can
be grounded-but-overlapping life-spheres instead of the disjoint abstract seams that
killed the prior attempt.

## 2. The starting vocabulary — 24 domains, 196 seed categories

Universal coverage of lived human intent (cross-tabulated from ATUS-17, Propædia-10,
Wheel-of-Life, IAB, OECD-BLI — keeping every sphere that recurs across multiple
independent frameworks), adapted toward *intent* not *knowledge* (practical life
domains are first-class; religion is tradition-neutral; place/time/value are facets,
not categories — §6).

- **health-and-body** — physical-health, mental-health, nutrition, fitness-and-exercise, sleep, medical-care, illness-and-disease, medication, therapy, reproductive-health, sexual-health, aging, disability, addiction-and-recovery, dentistry, vision-and-hearing, pain-management, preventive-care, first-aid, rehabilitation
- **food-and-drink** — cooking, diet-and-eating, recipes, baking, food-preservation, fermentation-and-brewing, beverages, hospitality-and-entertaining, foraging, fasting, restaurants-and-dining
- **home-and-dwelling** — housing, home-maintenance, home-improvement, interior-furnishing, cleaning-and-housekeeping, household-organization, moving-and-relocation, real-estate, property-and-land, utilities-and-services, home-security, appliances-and-fixtures
- **money-and-finance** — budgeting, saving, spending, debt, credit, investing, retirement-planning, taxes, insurance, income, banking, giving-and-charity, financial-planning, accounting-and-bookkeeping
- **work-and-livelihood** — career, job-search, workplace, profession-and-vocation, management-and-leadership, entrepreneurship, hiring-and-employment, compensation-and-benefits, scheduling, retirement, unemployment, freelancing, collaboration-and-teamwork, productivity, project-management
- **craft-and-making** — software-engineering, software-architecture, data-modeling, systems-and-infrastructure, version-control, testing-and-verification, hardware-and-electronics, construction-and-building, carpentry-and-woodworking, metalworking, textiles-and-sewing, manufacturing, mechanics-and-repair, engineering, tooling-and-instruments, handcraft, invention-and-prototyping
- **knowledge-and-inquiry** — mathematics, logic, physics, chemistry, biology, astronomy, earth-science, computer-science, medical-science, statistics-and-data, research-methods, history, linguistics, philosophy, economics, cognitive-science, theory-of-classification
- **learning-and-education** — studying, teaching, schooling, skill-acquisition, reading, memory-and-retention, curriculum-and-pedagogy, tutoring-and-mentoring, self-directed-learning, credentials
- **language-and-communication** — writing, speaking-and-rhetoric, translation, grammar-and-usage, conversation, correspondence, listening, public-speaking, editing-and-revision, naming-and-terminology, notation
- **arts-and-creativity** — literature-and-fiction, poetry, music, visual-art, drawing-and-painting, photography, film-and-video, theater-and-performance, dance, design, sculpture, creative-process, storytelling, publishing
- **relationships-and-kinship** — friendship, romance-and-dating, marriage-and-partnership, family, parenting, child-rearing, extended-family, conflict-and-reconciliation, boundaries, trust-and-intimacy, communication-in-relationships, caregiving, loss-and-grief, social-connection
- **self-and-identity** — personal-growth, self-knowledge, habits-and-discipline, emotions, character-and-virtue, motivation, confidence-and-esteem, identity-and-belonging, life-purpose, decision-making, temperament, self-care, emotion-regulation
- **spirituality-and-meaning** — religious-practice, prayer, meditation, ritual-and-liturgy, faith-and-belief, doctrine-and-theology, contemplation, pilgrimage, scripture, ethics-and-morality, mortality-and-death, transcendence, monastic-and-ascetic-life, wisdom
- **society-and-governance** — politics, government, public-administration, civic-participation, voting-and-elections, activism, public-policy, diplomacy, social-movements, community-organizing, public-services, citizenship, war-and-conflict
- **law-and-justice** — legal-rights, contracts, property-law, criminal-law, litigation-and-disputes, compliance-and-regulation, intellectual-property, family-law, liability, legal-procedure, justice-and-fairness, law-enforcement, dispute-resolution
- **community-and-belonging** — neighborliness, volunteering, mutual-aid, membership-and-clubs, social-events, reputation, service, hospitality-civic, local-institutions
- **land-and-living-world** — agriculture, gardening, plant-cultivation, animal-husbandry, pet-care, forestry, fishing-and-aquaculture, hunting, ecology-and-conservation, weather-and-climate, wilderness, sustainability, natural-resources, land-stewardship
- **travel-and-movement** — travel-planning, destinations, transportation, driving-and-vehicles, navigation-and-wayfinding, commuting, logistics-and-shipping, migration, tourism, public-transit, walking-and-cycling
- **commerce-and-trade** — selling, buying, marketing, retail, supply-and-sourcing, trade, customer-service, pricing, negotiation, ownership-and-assets, markets
- **leisure-and-play** — recreation, sports, games-and-puzzles, hobbies, entertainment, collecting, outdoor-activities, play, rest-and-relaxation, festivals-and-celebration, fandom
- **appearance-and-presentation** — clothing-and-fashion, grooming, style-and-aesthetics, beauty-and-cosmetics, etiquette-and-manners, personal-presentation
- **safety-and-security** — personal-safety, emergency-preparedness, risk-management, defense-and-protection, cybersecurity, privacy, disaster-response, military-and-defense, crime-prevention
- **information-and-media** — information-management, record-keeping, documentation, news-and-current-events, media-and-broadcasting, libraries-and-archives, databases, search-and-retrieval, knowledge-organization
- **technology-and-systems** — energy, power-and-utilities, automation, robotics, artificial-intelligence, networks-and-telecom, materials, industrial-machinery, instrumentation, aerospace-and-spaceflight

## 3. The curation model — what makes "hundreds" work instead of 1,300-synonym bloat

A **warrant-gated thesaurus** (ANSI/NISO Z39.19) governed like a classification
editorial board (IAB / OCLC-DDC): versioned, never free-text. Each category record
carries one canonical NOTA atom, a one-line **scope note** fixing its boundary,
exactly one owning domain, and an explicit **UF ("use-for") synonym list** that
redirects non-preferred wordings to it. *The UF redirect table is the "one canonical
`schema`, not 20 accidental synonyms" mechanism* — and the precise repair for the old
free-text `Keyword` field, whose only flaw was the absence of this table.

**The enlargement gate — three tests, in order, scanned within the candidate's domain
(~8–20 siblings, the reason the domain tier exists):**

1. **Synonym test** (Z39.19 equivalence) — is it just another wording of an existing
   category? `data-schema`/`record-shape`/`type-definition` → `data-modeling`; `git`
   and `jj` → `version-control`. If synonym: record as a UF variant and stop. *This
   single test kills the bloat that ruined the old `Keyword` field.*
2. **Subsumption / nesting test** — is it already covered, or a genuinely finer
   child? If finer (`queen-rearing` under `animal-husbandry`), it **nests** as an
   informal third level rather than joining as a new peer. Nesting-over-proliferation
   is the rule that keeps the workspace's `nota`/`signal`/`sema`/`nix` from ever
   becoming peer categories, let alone domains.
3. **Three-warrant test** — admit a new canonical category only with all three:
   *literary* (it recurs across real records, not a one-off), *user* (people actually
   name intent with this word), *structural* (it fills a real gap). Tests 1–2 are
   mechanical (an auditor pass can auto-propose them); test 3 and the very rare new
   *domain* need a human bless.

**Domains are near-frozen; categories grow by accretion under them** (freeze the top,
grow the leaves — the DMOZ/WordNet/IAB lesson). Until the auditor lane lands, the
interim owner is *designer proposes, psyche blesses*.

## 4. It holds the real corpus — and software needs no domain of its own

The live ~1418-record software corpus is a *narrow sample*, and it absorbs cleanly
across **three or four** universal domains without inflating the top tier — the proof
that a universe-spanning vocabulary holds a real corpus:

- `craft-and-making` takes the bulk — schema/nota → `data-modeling` (+ `notation`
  under language-and-communication for NOTA's surface grammar); signal/sema/nexus/
  daemon → `software-architecture` / `systems-and-infrastructure`; rust →
  `software-engineering`; jj → `version-control`; nix/deploy →
  `systems-and-infrastructure`.
- `information-and-media` takes Spirit's own meta-layer — reports → `documentation`;
  spirit/intent records → `knowledge-organization` (an intent-capture system *is*
  knowledge organization).
- `nota`/`signal`/`sema`/`daemon`/`nix` are **third-tier nests** under those leaves,
  never peers and never domains. New finer leaves (`deployment`, `nota-syntax`) enter
  via the gate as warrant accrues.

Stress test passed across archetypes — a farmer ("rotate the south field" →
`agriculture`), doctor ("confirm allergies before prescribing" → `medication`),
novelist ("first drafts get no editing" → `creative-process`), parent, monk, and
engineer each file at exactly one concrete leaf. Two workspace records correctly land
*outside* the engineering leaves — "reports go in files not chat" → `documentation`,
"agents over-log into spirit" → `knowledge-organization` — discrimination the flat 12
gerunds could never produce.

## 5. What this changes in the code

Pre-production, so no compatibility constraint — this is a clean value-set swap plus
a small structural addition:

- `Category` value-set: the 12 gerunds → the 196 grounded atoms, **as a schema enum**
  (the Rust type stays; the enum *contents* change — psyche confirmed recompile +
  zero-downtime redeploy makes this trivial, so no runtime registry; see §6.7).
- Add the `Domain` tier (`Domain`/`Domains`) and a **category→domain table** so the
  domain is *derived*, never separately stored on a record (a leaf can be re-parented
  without rewriting records).
- **Retire the free-text `Keyword` field** (`signal.rs:295`); its job moves to the
  curated vocabulary + the UF synonym table. *(Flag: this is a real change from
  `581`/`582`, where asterisk-span keywords were the within-category discriminator.
  Confirm we replace them with the synonym table rather than keep both — §6.)*
- Migration: re-map the 1418 records off the gerunds + free-text keywords onto
  canonical leaves (rule-table from existing keyword strings, or re-derive by a
  classifier from each Description) — the first real exercise of the gate, run through
  the agglomeration machinery, not a 1:1 passthrough.

## 6. Decisions for the psyche

1. **The term — confirm `domain` › `category`** (two tiers, records file at
   `category`). Or pick a variant: `domain` single-tier; `area`›`category` (if you
   want to avoid the `domain-criome` name collision); `domain`›`subject` (if you want
   `category`'s gerund history fully gone).
2. **Motivation/value as a separate facet.** The research strongly recommends a second
   orthogonal field for *why* (Schwartz's 10 values, or PERMA) so "exercise for
   self-esteem" files as `fitness-and-exercise` (the about) without esteem competing
   for the slot. Recommendation: **reserve the design slot, defer the field — but do
   not fold motivation back into categories** (that reintroduces the gerund ambiguity).
3. **The third tier** (`queen-rearing` under `animal-husbandry`; `nota` under
   `data-modeling`) — a *stored* level on the record, or *curation-only* grouping that
   collapses to the tier-2 leaf at storage? Curation-only keeps records two-tier but
   loses the `nota`-vs-`signal` distinction at query time. Needs deciding before the
   value-set is frozen.
4. **Keep asterisk-keywords, or fully replace with the UF synonym table?** (§5.)
5. **Multi-tag vs primary.** `Categories` is already a `Vec`; keep one-or-more (a
   record can touch `financial-planning` *and* `parenting`), or designate one primary
   category per record for the "one canonical about" framing?
6. **Religion neutrality** — confirm specific traditions (christianity/buddhism/islam)
   are *never* categories; they live as an optional tradition facet or third-tier nest
   under `religious-practice`, so the vocabulary privileges none (correcting DDC's bias).
7. **Enum vs registry — RESOLVED by psyche: stay a schema enum.** Recompiling to
   change an enum set is a *trivial* operation in these components, and zero-downtime
   upgrade is a design goal — so "adding a category means a schema regeneration" is a
   non-cost, not a problem to design around. The vocabulary lives in the schema (the
   source of truth), the editorial-board curation gate (§3) simply *is* a reviewed,
   versioned schema change, and a virgin daemon already knows all categories because
   they're compiled into its binary (consistent with binary-startup discipline — no
   runtime registry, no config-seeded growable value). The one asymmetry to keep:
   *adding* a category is free; *renaming/removing* one needs a `SPIRIT_SCHEMA_VERSION`
   bump + a `production_migration` mapping for records carrying the old atom — which is
   exactly where the UF synonym-redirect table earns its keep (it absorbs a rename as a
   redirect without a data migration).
8. **Interim gate ownership** — confirm "designer proposes, psyche blesses" is
   acceptable until the auditor lane lands, rather than blocking the vocabulary on it.

Research run `wf_d04c4bdc-6aa` (6 surveys → 2 syntheses → merge+stress-test).
