# Spirit — the single-noun `domain` vocabulary + the `referent` facet

Resolves two psyche directives on top of `583`: (1) kill the `x-and-y` names —
single nouns only; (2) add a field linking an intent to a concrete repo/project/
thing. Supersedes `583` §1-2 on naming. Method: a 4-agent run
(`wf_01d0cd52-685`) — two independent single-noun renames merged with programmatic
collision-checking, plus the facet design.

**Two later psyche corrections folded in:** (a) **NOTA naming idiom** — unspaced
multi-word atoms are **camelCase** (mirroring PascalCase for type variants):
`firstAid`, `jobSearch`, `recordKeeping`, and referents like `theSouthField` — *not*
kebab-case. (b) **No `copyright`/intellectual-property domain** — intellectual
property is not a legitimate form of property, so the `law` area carries no IP domain
(294 → 293).

## 1. The terms, settled

- **`domain`** = the unit a record tags. **293** of them, each a single grounded
  noun: `architecture`, `schema`, `agriculture`, `parenting`, `prayer`, `notation`.
  This is the "hundreds of domains" you wanted; `category`/`topic` are retired as
  terms.
- **`area`** = the 24 broad groupings (`health`, `craft`, `knowledge`, `land`→`nature`
  …). **Never tagged on a record** — they exist only to organize the vocabulary and
  to give the enlargement gate a ~12-sibling neighborhood to dedup within. Near-frozen.
  *(If you'd rather the broad tier also be called something else — `field`, `sphere` —
  it's a one-word swap; `area` is my lean.)*
- **`referent`** = the new optional facet (§3): the concrete named instance an intent
  governs.

So a record carries one-or-more `domain` atoms (what it's about) and zero-or-more
`referent` atoms (which named thing it governs). New `Entry`:
`{ Domains · Kind · Description · Certainty · Importance · Privacy · Referents }`.

## 2. The single-noun vocabulary — 24 areas, 293 domains

Every name a single English noun; the `x-and-y` compounds are gone; all atoms
verified globally unique (zero collisions, checked by program). Multi-word atoms are
camelCase per the NOTA idiom (`firstAid`, `jobSearch`, `recordKeeping`).

- **health** — body · mind · nutrition · exercise · sleep · medicine · disease · medication · therapy · reproduction · sexuality · aging · disability · addiction · dentistry · senses · pain · prevention · firstAid · rehabilitation
- **food** — cooking · diet · recipe · baking · preservation · fermentation · beverage · entertaining · foraging · fasting · dining
- **home** — housing · maintenance · renovation · furnishing · cleaning · tidying · relocation · realty · property · utilities · locksmithing · appliances
- **finance** — budgeting · saving · spending · debt · credit · investing · retirement · tax · insurance · income · banking · charity · planning · accounting
- **work** — career · jobSearch · workplace · vocation · leadership · entrepreneurship · employment · compensation · scheduling · unemployment · freelancing · teamwork · productivity · project
- **craft** — programming · architecture · schema · infrastructure · versioning · testing · electronics · construction · carpentry · metalworking · sewing · manufacturing · repair · engineering · tooling · handicraft · invention
- **knowledge** — mathematics · logic · physics · chemistry · biology · astronomy · geology · computing · physiology · statistics · research · history · linguistics · philosophy · economics · cognition · taxonomy
- **education** — studying · teaching · schooling · skill · reading · memorization · pedagogy · mentoring · autodidacticism · credential
- **language** — writing · rhetoric · translation · grammar · conversation · correspondence · listening · oratory · editing · terminology · notation
- **art** — fiction · poetry · music · painting · photography · film · theater · dance · design · sculpture · creativity · storytelling · publishing
- **kinship** — friendship · romance · marriage · family · parenting · relatives · reconciliation · boundaries · intimacy · rapport · caregiving · grief · belonging
- **self** — growth · introspection · discipline · emotion · virtue · motivation · confidence · identity · purpose · decision · temperament · wellbeing · composure
- **spirituality** — worship · prayer · meditation · ritual · faith · theology · contemplation · pilgrimage · scripture · ethics · mortality · transcendence · asceticism · wisdom
- **governance** — politics · government · administration · citizenship · elections · activism · policy · diplomacy · movements · organizing · services · naturalization · war
- **law** — rights · contract · title · crime · litigation · compliance · custody · liability · procedure · justice · policing · arbitration
- **community** — neighborliness · volunteering · solidarity · membership · gatherings · reputation · service · hospitality · institutions
- **nature** — agriculture · gardening · horticulture · husbandry · pets · forestry · fishing · hunting · conservation · weather · wilderness · sustainability · resources · stewardship
- **travel** — itinerary · destination · transportation · driving · navigation · commuting · logistics · migration · tourism · transit · cycling
- **commerce** — selling · buying · marketing · retail · sourcing · trade · support · pricing · negotiation · assets · market
- **leisure** — recreation · sport · games · hobby · entertainment · collecting · outdoors · play · relaxation · celebration · fandom
- **appearance** — clothing · grooming · style · cosmetics · etiquette · comportment
- **safety** — protection · preparedness · risk · cybersecurity · privacy · disaster · military · deterrence
- **information** — curation · recordKeeping · documentation · news · broadcasting · archives · database · retrieval · classification
- **technology** — energy · power · automation · robotics · intelligence · networking · materials · machinery · instrumentation · aerospace

**Notable renames** (for anyone holding the `583` names): `land-and-living-world` →
**`nature`** (the one non-obvious area rename); `software-engineering` → `programming`,
`software-architecture` → `architecture`, `data-modeling` → `schema`, `version-control`
→ `versioning` (where the live software corpus files); `medical-care` → `medicine`,
`mental-health` → `mind`, `physical-health` → `body`. **Four merges** trimmed 298→294,
then **`copyright` dropped** (psyche: intellectual property isn't legitimate) → **293**:
visual-art + drawing → `painting`; parenting + child-rearing → `parenting`;
personal-safety + defense → `protection` (national sense kept as `military`); the two
`retirement` leaves → one global `retirement` under `finance`.

**Flagged judgment calls** (yours to wave through or adjust):
- `autodidacticism` — a real but long single noun for self-directed learning. Keep, or
  prefer a shorter compound?
- **`copyright`/intellectual-property removed entirely** — per your call that IP isn't
  legitimate. `law` now has no IP domain (no copyright/patent/trademark).
- `citizenship` vs `naturalization` kept as two atoms (civic engagement vs legal
  status). Fold to one if you want it leaner (→292).
- `firstAid`, `jobSearch`, `recordKeeping`, `cybersecurity`, `realty` — the only
  multi-word atoms; first three are camelCase per the NOTA idiom, last two are
  lexicalized single words.

## 3. The `referent` facet — linking intent to a concrete named thing

**It is warranted, and it's a genuinely different axis from `domain`.** `domain`
answers *about-what* (universal, shared by everyone); `referent` answers *which-one*
(particular, drawn from one person's own inventory). The cross-product is the point:

| Intent | domain | referent |
|---|---|---|
| "spirit's architecture should be schema-first" | `architecture` | `spirit` |
| "rotate the south field to legumes" | `agriculture` | `theSouthField` |
| "first drafts get no editing" (a life principle) | `creativity` | *(none)* |
| "the signal-* crates stay binary-by-default" | `schema` | `signalSpirit`, `signalAgent`, … |

(Referent atoms follow the camelCase NOTA idiom — `theSouthField`, `signalSpirit`.
One open question: a referent that maps to an existing repo — does it use the repo's
kebab name `signal-spirit`, or the camelCase atom `signalSpirit`? My lean: camelCase
atom, with the kebab repo-name as a UF synonym that redirects to it.)

Both, either, or neither — most life-principles are domain-only, which is why the
field is **optional**.

**The name: `referent`** — the one noun whose dictionary sense already *is* "the
concrete thing referred to," with zero work/tech bias (a repo, an abbey, a child, a
marriage, a field are all referents). Runner-up **`holding`** (more concrete, but
leans property/ownership — a child reads oddly as a "holding"). Your floated `project`
and `resource` both fail the universality test (a farmer has no "project"; a marriage
isn't a "resource") — they become UF *synonyms* that redirect to the field, not the
field name. (Worth noting: `resource` is also already a `domain` leaf under `nature`.)

**Curation — the person's own registry, not a universal vocabulary.** Same warrant-
gated, synonym-controlled, never-free-text discipline that saves `domain` from bloat
— but where the `domain` vocabulary is world-universal and editorial-board-blessed,
the `referent` registry is *the person's private particulars*, grown **self-service**
through a low-ceremony `RegisterReferent` op, gated only by the synonym check (so "20
spellings of spirit" can't accumulate: `spirit-repo`/`the-spirit-project` redirect to
`spirit`). For this workspace it seeds directly from `protocols/active-repositories.md`
+ `RECENT-REPOSITORIES.md` — each repo becomes one canonical referent, and the Spirit
triad is expressible as a referent that nests its three legs.

**Schema shape:** `Referents(Vec<Referent>)`, **optional**, on `Entry` — Vec because
one intent can govern several named things at once. **`Referent` is a runtime-registry
reference, NOT a schema enum** (this is the key way it differs from `Domain`). A
referent is registered by a runtime `RegisterReferent` write into a stored registry,
synonym-gated; it is never a compile-time enum value. Why the two facets diverge:
**`Domain` is shared vocabulary** (universal, slowly-curated, public → a schema enum,
where "recompile-to-add" is trivial because additions are rare and blessed);
**`Referent` is per-person data** (a private, frequently-growing inventory of named
things → store state, not the schema). Three reasons a referent enum is wrong: (1)
**privacy** — referents are private particulars (`aNamedChild`, `myTherapist`, a named
relationship), and the schema is a *shared, public, compiled contract*; you cannot bake
one person's private inventory into it; (2) **it's data, not type** — you don't put
rows/instances in the type system; (3) **frequency** — new repos/fields/projects are
registered constantly and casually, so a recompile+redeploy per referent is absurd
ceremony (the "recompile is trivial" principle was about *rare, deliberate vocabulary*
changes, not frequent personal registrations). Add a `ReferentSelection` to `Query` so
**"show every intent governing `spirit`"** becomes a first-class read — that's the
payoff you're after. `referent` locates the subject;
the `Certainty`/`Importance`/`Privacy` axes still grade the statement (a private-
relationship referent can carry a *default* privacy hint, but the per-record `Privacy`
stays authoritative).

## 4. Decisions for the psyche

1. **Tier names** — confirm `domain` (the 294 tagged units) + `area` (the 24 broad
   groupings, never tagged). Or rename the broad tier (`field`/`sphere`).
2. **The vocabulary** — wave through the 294, or adjust the flagged calls (§2:
   autodidacticism, copyright/IP, citizenship split, the four merges).
3. **The facet name** — `referent` (my lean) or `holding`; `project`/`resource` → UF
   synonyms.
4. **Referent registry policy** — confirm self-service growth (person registers their
   own particulars, synonym-gated) vs the editorial-board gate `domain` uses.
5. **Referent shape** — optional `Vec`, schema-enum atom, `ReferentSelection` in
   `Query`; seed this workspace's registry from the active repos now (so the 1418-record
   migration can populate referents in the same pass).
6. **Migration interaction** — when remapping the 1418 records, auto-derive a referent
   from software keywords (`spirit`,`nota`) in the same pass, or leave null and
   back-fill (auto-deriving risks tagging a domain-only record with a spurious referent)?

None of this is logged to Spirit yet — it's a proposal. The blessed vocabulary + the
`referent` decision become intent (a Spirit record + reflection into `spirit/INTENT.md`)
once you confirm.

Run `wf_01d0cd52-685` (2 renames → collision-checked merge + facet design).
