# Scout — Archived-Record Rehoming Routing Assessment

Read-only assessment of how ~505 ARCHIVED Spirit records (the matter set the
strict-bar rejudge ledger routed out of intent) map to target repos/surfaces.
No record, file, config, or runtime state was changed.

## Task and scope

Characterize the routing problem and recommend an approach for a bulk rehoming
pass of the ledger's matter categories: architecture-doc (384), code/config
(33), spirit-manual (76), vocabulary-doc (12). DO NOT map all 505. Determine
whether records carry per-repo attribution or must be content-inspected; sample
~12-15 across the four categories; recommend a routing approach with a rough
volume estimate; flag workspace-level vs repo-level and any un-routable category.

## Files and commands consulted

- Ledger: `/home/li/primary/reports/legacy-disposition/spirit-strict-rejudge-ledger-2026-06-29.md` (per-category id lists).
- Earlier plan with human-readable descriptions: `/home/li/primary/reports/legacy-disposition/spirit-cleanup-plan-2026-06-26.md`.
- Prior independent scout of the same removal: `/home/li/primary/reports/legacy-disposition/SITUATION-2026-06-30-parked-spirit-tracks.md` (Track 4 is this exact problem).
- Wire shapes from source: `repos/spirit/src/schema/sema.rs`, `repos/spirit/manual.md`, `repos/spirit/README.md`; cached contract checkouts `~/.cargo/git/checkouts/signal-spirit-44a4bfaa970650f7/5d0905a/src/schema/{signal,domain}.rs` and `~/.cargo/git/checkouts/meta-signal-spirit-218ef8a834c9b65d/98704a3/src/schema/meta_signal.rs` (locked revs from `repos/spirit/Cargo.lock`).
- Live store via deployed `spirit` (0.20.0): `Observe`, `Lookup`, `Count`.
- Archive store on disk: `/home/li/.local/state/spirit/spirit.archive.sema` and snapshot `spirit.sema.preremoval-631-20260630T000025`, inspected with `od`, `strings`, `grep` (not the deployed CLI — no archive-read op exists).

## Observed facts

### F1. The 505 records are NOT live-queryable; they are archived-out.

- Live store now holds exactly **21 records** (`spirit "(Count (Any Any Any Any None Any Any Any))"` -> `(RecordsCounted 21)`; same at `(AtLeastCertainty Zero)`, so no Zero tombstones linger). These 21 are the strict keep-set (e.g. `jlo7`, `k09z` present).
- Every sampled ledger id across all four categories returns `(Error [record not found])` on `(Lookup <id>)`: `06l6 e8iu zrrv` (arch), `0a9p zgwf` (code), `0fmg ztX` (spirit-manual), `1i1b tnam` (vocab), `8dib wa4j` (repo-intent). The removal was a true archive-out.

### F2. There is NO deployed CLI surface that reads archived records by id or content.

- Main `spirit` Input enum (signal-spirit `5d0905a`): `Record Propose Clarify Supersede Retire ResolveClarification Observe PublicTextSearch PublicRecords PrivateRecords Lookup Count ChangeCertainty BumpImportance ChangeRecord RegisterReferent ...`. All operate on the **live** store only; `Lookup`/`Observe` of an archived id return not-found.
- Owner meta-socket `meta-spirit` Input enum (meta-signal-spirit `98704a3`): `Configure Import CollectRemovalCandidates ObserveHead ObserveHeadObject` — **no archive observe/query/lookup**. `CollectRemovalCandidates` is the write-side archive-out op, not a reader.
- Consequence: archived content is reachable only by (a) `strings`/redb tooling over the `.sema` file, or (b) restoring the `preremoval-631` snapshot into a daemon and querying live. Both are operator actions outside the deployed read surface.

### F3. The archive IS recoverable text (redb + UTF-8 payloads).

- All three `.sema` files are **redb** databases (magic bytes `redb`). `spirit.archive.sema` is 1.73 MB.
- `strings spirit.archive.sema` extracts full record **descriptions** verbatim (confirmed: found "positively" from `jlo7`; pulled complete architecture descriptions about schema/NOTA/SEMA/Sub-ID). Referent text is also present (~1900 hyphenated tokens). Record ids are stored as 4-char codes paired with numeric slot indices (e.g. `a2t4-3853`), not as raw description ASCII (so grepping a bare id finds nothing).

### F4. A record's structured routing-signal fields are: domain vector + referent vector. Neither names a repo by convention.

- Entry schema (from `manual.md` / `spirit-cli` skill / live Observe): domain vector, kind, description, certainty, importance, privacy, **referent vector**. Live example `jlo7`: domain `[(Language Rhetoric) (Information Documentation)]`, referents `[guidelines positive-wording]`.
- The manual calls referents "the primary retrieval and dedup key... the named particulars a record is about." They are topic/concept tags (e.g. `positive-wording`, `schema-next`, `field-name`), NOT repo names.
- Domains are life-area taxonomy (`Technology (Software ...)`, `Information`, `Governance`), not repo identity. So no field deterministically names the owning repo.

### F5. Description text carries the routing signal, mostly as TOPIC not explicit repo.

- Explicit "X repo" mentions in archive descriptions are rare: a `strings | grep` for "... repo" found only ~9 hits total (`signal-component repo` x2, `nota repo` x2, `spirit repo`, `signal-X repo`, `schema-types repo`, `schema-library repo`, `NOTA repo`) against 384 architecture-doc records.
- The overwhelming majority carry a **topic that implies a repo**: schema/NOTA/SEMA/nexus/signal/wire/storage/codec/actor/Sub-ID/domain-naming. Some cross-reference other records by number ("per spirit 391"), not by repo.

## Sample (13 records, spread across the four categories)

Descriptions are reconstructed from the 2026-06-26 cleanup plan (which captured
human-readable summaries) and from `strings` over the archive. "Routing signal"
is scout interpretation.

### architecture-doc (4 sampled of 384)

1. `06l6` — desc not captured in any report; lives only in archive. Routing signal: UNKNOWN without per-record archive read. Representative of the bulk's opacity.
2. (archive string) "All Spirit Signal, Nexus, and SEMA operations must be declared in the schema files first; generated schema types are the source of every operation data type..." — topic = schema-first authoring. Implies the **spirit** (or **schema-next**/**signal**) repo. Repo-level, not workspace.
3. (archive string) "Schemas inside the schema component are stored in a much more efficient binary representation than NOTA text... the schema component holds the COMPILED runtime representation..." — topic = compiled-schema/runtime. Implies **schema-next** / **sema**. Repo-level.
4. (archive string) "Sub-ID is a SignalCore primitive type for entities that are 'a thing' but do not have their own Criome identity. Sub-ID = content-address fingerprint..." — topic = SignalCore/Criome identity. Implies **signal** / **criome**. Repo-level.

Signal pattern: architecture-doc records carry a clear *topic*, but the topic
maps to a repo only by an engineer who knows the component layout. No explicit
repo field; a handful name a repo in prose. **Per-record content inspection
required.**

### code/config (5 sampled of 33) — descriptions from the 2026-06-26 plan

5. `go41` — "local-llm token path". Routing: a config/operational fact. Owning home is the LLM/inference component (CriomOS-home or persona/cloud). Repo-level, UNTRACKED repo.
6. `nz0t` — "prometheus gopass token wiring". Owning home = CriomOS-home / monitoring config. Repo-level, UNTRACKED.
7. `16l0` — "flarectl on cloud daemon PATH". Owning home = cloud/CriomOS-home deploy. Repo-level, UNTRACKED.
8. `upza` — "privileged ops via ssh root@host". Owning home = ops/CriomOS-home. Repo-level, UNTRACKED.
9. `osoo` — "backup WiFi password via sops-nix". Owning home = CriomOS-home secrets. Repo-level, UNTRACKED. (Privacy note: it is Privacy Zero per the ledger, but it is operational-secret-adjacent; confirm before publishing.)

Signal pattern: code/config descriptions are explicit and self-routing by
*subject* (token X, node Y, deploy Z), and the 2026-06-26 plan already named the
home for each. But nearly every home is an **UNTRACKED repo** (`repos/...`) — a
landing blocker, not a routing blocker.

### spirit-manual (2 sampled of 76)

10. `0fmg` — 2026-06-26 plan groups it under "report conventions". Routing: Spirit-usage / reporting-convention matter -> `repos/spirit/manual.md` or a reporting skill. Workspace/tooling-level, not a sub-repo's architecture.
11. (category as a whole) the 76 are Spirit/guardian/certainty/capture mechanics -> single home `repos/spirit/manual.md` (already exists and is the agent-facing Spirit doctrine manual). Many are already covered there.

Signal pattern: spirit-manual routes by **category -> one surface** (the spirit
manual), almost no per-record repo decision. Cheapest category to route.

### vocabulary-doc (2 sampled of 12)

12. `1i1b` — 2026-06-26 plan routes vocabulary/definitional terms to `workspace-vocabulary.md`. Routing: a "what term X means" definition -> a glossary surface. Workspace-level (or per-repo glossary if the term is component-bound).
13. `4vde` — plan groups under schema skills / definitional. Routing: a schema-term definition -> schema-component glossary or `structural-forms`/`nota-design`. Borderline workspace-vs-repo depending on whether the term is component-specific.

Signal pattern: vocabulary-doc routes by **category -> a glossary surface**;
split is workspace-glossary vs component-glossary, decidable from the term.

## Answers to the four questions

### 1. Do records/ledger carry per-repo attribution, or must each be content-inspected?

**No reliable per-repo attribution exists.** No record field names the owning
repo: domains are a life-area taxonomy and referents are topic/concept tags
(F4). The ledger's category column is a *surface-type* tag (architecture-doc /
code / spirit-manual / vocabulary-doc), not a repo. Explicit "X repo" appears in
prose for only ~9 of 384 architecture records (F5). Therefore:

- **architecture-doc and code/config must be content-inspected per record** to
  pick the repo (the topic implies the repo to a human who knows the layout).
- **spirit-manual and vocabulary-doc route by category to a known surface** with
  little per-record judgement.

A precondition for any of this: the archive descriptions must first be extracted
(via `strings`/redb or a snapshot restore), because no deployed CLI reads them
(F2) and the bulk (architecture-doc) has almost no descriptions captured in any
existing report.

### 2. Sample — see the 13 records above.

### 3. Recommended routing approach

Two-stage, **category-first then topic-to-repo only where needed**:

- Stage A — recover the corpus once. Extract id + category + domain + referents
  + description for all matter ids from `spirit.archive.sema` (redb/`strings`),
  or restore `spirit.sema.preremoval-631-20260630T000025` into a scratch daemon
  and `Lookup` each id. This single extraction unblocks every downstream
  routing call and is the highest-leverage step.
- Stage B — route by category:
  - **spirit-manual (76) -> one surface** (`repos/spirit/manual.md`). Bulk
    category->surface; per-record work is only "already covered? migrate vs
    discard." Cheapest.
  - **vocabulary-doc (12) -> glossary surface** (workspace glossary, or a
    component glossary when the term is component-bound). Near-mechanical.
  - **code/config (33) -> owning component config/architecture**, using the
    2026-06-26 plan's already-named homes as the seed map. Mechanical to route,
    BLOCKED on landing (untracked repos) — needs the psyche's hold /
    edit-untracked / transitional-in-tree call.
  - **architecture-doc (384) -> per-repo ARCHITECTURE.md by content topic.** This
    is the only category needing genuine per-record/per-cluster judgement. Bucket
    by topic keyword first (schema/NOTA -> schema-next/nota; SEMA/storage ->
    sema; signal/nexus/wire -> signal-*; Criome/SignalCore -> criome; guardian/
    Spirit-internal -> spirit), then resolve residue by hand.

Do NOT bucket by an existing field — none routes to a repo. Bucket by category
for the three small categories and by description-topic for the large one.

### 4. Workspace-level vs repo-level; un-routable categories

- **Mostly repo-level**: architecture-doc (384) and code/config (33) are
  component/repo-bound by topic — ~417 records, the bulk. Most of their homes are
  UNTRACKED repos.
- **Mostly workspace/tooling-level (not a sub-repo's ARCHITECTURE.md)**:
  spirit-manual (76) routes to the spirit repo's manual (a tooling surface, not
  the primary workspace ARCHITECTURE.md, and not scattered component arch). 
  vocabulary-doc (12) is mostly workspace-glossary-level, a few component-bound.
- **Routing to the PRIMARY workspace ARCHITECTURE.md specifically**: from the
  sample, very few. Architecture-doc records are component-architecture, which
  belongs in each sub-repo's ARCHITECTURE.md, not the primary one. The records
  that are genuinely workspace-level (cross-cutting workspace direction) were
  largely the ones the strict bar KEPT as intent (the live 21), not these
  matter records. Expect only a small tail of architecture-doc/vocabulary records
  to land in primary ARCHITECTURE.md.
- **Category mostly un-routable without heavy per-record judgement**:
  **architecture-doc (384)**. No field routes it, ~9/384 name a repo, and its
  descriptions are not captured in any existing report — every record needs the
  archive description read and a component-layout judgement to place. This single
  category is ~76% of the 505 and carries essentially all the routing cost.

## Rough volume estimate per target

- spirit repo manual (`repos/spirit/manual.md`): ~76 (spirit-manual) + the
  guardian/Spirit-internal slice of architecture-doc. Largely "verify-covered,
  discard duplicate."
- per-component ARCHITECTURE.md (schema-next / sema / nota / signal-* / nexus /
  criome / etc.): the 384 architecture-doc records split across these by topic —
  the dominant clusters from the sample are schema/NOTA, SEMA/storage, and
  signal/SignalCore/Criome. Exact per-repo split is NOT estimable without Stage A
  (the descriptions for the 384 are not in any report).
- component config / CriomOS-home / cloud: ~33 (code/config), pre-mapped by the
  2026-06-26 plan, blocked on untracked-repo landing.
- glossary surface(s): ~12 (vocabulary-doc).
- primary workspace ARCHITECTURE.md: expected small single digits.

## Checks run (exact results)

- `spirit "(Count (Any Any Any Any None Any Any Any))"` -> `(RecordsCounted 21)`.
- `(Lookup 06l6 | e8iu | zrrv | 0a9p | zgwf | 0fmg | ztX | 1i1b | tnam | 8dib | wa4j)` -> all `(Error [record not found])`.
- `(Lookup jlo7)` / `(Lookup k09z)` -> found (live keep-set).
- `meta-spirit` / `spirit` Input enums read from locked-rev cached checkouts: no archive-read variant in either.
- `od` on the three `.sema` files -> all `redb` magic; archive 1.73 MB.
- `strings spirit.archive.sema | grep` -> recovered "positively" and full architecture descriptions; confirmed descriptions+referents are recoverable text, ids stored as `<code>-<slot>`.
- `strings | grep '...repo'` -> only ~9 explicit repo mentions across the archive.

## Blockers and unknowns

- **Primary blocker**: no deployed CLI reads archived content. The 384
  architecture-doc descriptions are nowhere in existing reports and must be
  extracted from `spirit.archive.sema` (redb/`strings`) or via a snapshot restore
  before they can be routed. This is the gating prerequisite for the bulk.
- **Landing blocker (not routing)**: most code/config and architecture-doc homes
  are UNTRACKED `repos/...` (and a few may be `private-repos/`, off-limits without
  authorization). Routing can be decided; landing needs the psyche's
  hold / edit-untracked / transitional-in-tree call.
- The exact per-record id->description for the 384 was NOT enumerated here (only
  sampled via `strings`); the `<code>-<slot>` keying means a clean per-id dump
  needs the redb value payloads decoded (rkyv) or a daemon restore, not bare
  `strings`.
- The 2026-06-26 plan's home tags predate the strict rejudge; treat them as a
  seed map for code/config and vocabulary, re-verified at execution.
- Count discrepancy to confirm at execution: brief says ~505 across four
  categories (384+33+76+12 = 505); the ledger's full MATTER set is 621 (adds
  skill 98, repo-intent 11, junk 7). The four-category 505 is the brief's scope.
- Privacy: the ledger states all are Privacy Zero (public). `osoo` (backup WiFi
  password) and the token-path config facts are operational-secret-adjacent;
  confirm publishing each is acceptable before landing, per the secrets/privacy
  discipline.

## Follow-up requirements

- Provide an archive-content read path before the bulk pass: either extract
  descriptions from `spirit.archive.sema` (redb tooling that decodes the rkyv
  entry payloads, not bare `strings`) or restore `preremoval-631` into a scratch
  daemon and `Lookup` each id. Recommend the latter for fidelity.
- Get the psyche's call on the untracked-repo landing blocker before routing
  code/config and the untracked-repo slice of architecture-doc.
