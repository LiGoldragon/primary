# Spirit redesign — situation snapshot (re-situation)

Where the Spirit redesign actually stands as of this session, after the design was
blessed (588) and handed to operator. **Headline: the blessed design is essentially
fully implemented on `origin/main`; it is not yet deployed. The remaining gap is a
single system-operator deploy plus a Craft→Software re-tag migration over the live
1398-record store.**

## The deploy gap — the one fact that matters

| Layer | Commit | State |
|---|---|---|
| **Deployed daemon** (live, v0.8.1, 1398 records) | `9055609` | Domain enum + referent registry, **old 24-area vocabulary** (Craft still holds `Programming/Architecture/Schema/Infrastructure/Versioning/Testing/Tooling`); **no Software branch**; pre-guardian-hardening. |
| **`origin/main`** (built, not deployed) | `c30bed3` | + guardian write-gate hardening (`5d47de6`), + justified-mutation gating (`18cb7f1`), + Software domain branch & 719-line `production_migration.rs` (`c30bed3`). |

So the live daemon a CLI talks to today is *behind the design*. Everything we blessed is
code on `origin/main` — it just hasn't been cut over. The cutover is **migration-gated**:
1398 live records, many tagged with Craft leaves that *no longer exist* in the new enum
(`Craft(Programming)`, `Craft(Architecture)`, …), must be re-tagged to their `Software`
cluster leaf before/by the deploy. `production_migration.rs` is operator's vehicle for
this; running it is system-operator's deploy step (587 decision 7).

## Design fidelity — operator built it faithfully

Spot-checked the three implementing commits against the design reports:

- **Software branch (587)** — `origin/main` schema carries the exact tree: 12 clusters
  (Languages, Theory, Systems, Distributed, Data, Intelligence, Security, Quality,
  Operations, Observability, Surfaces, Engineering), three-tier `(Software (Cluster
  Leaf))`, and `Craft` cleaned back to physical making (`Electronics … Handicraft
  Invention`) with the seven software leaves evicted. Matches report 587.
- **Guardian gate + journal (585, 586)** — `guardian_journal.rs` opens its **own**
  `sema_engine` database (`guardian-decisions` table, own schema version) — the separate
  append-only decision-log of 585 §3, *not* commingled with the intent store.
  `GuardianOperation` covers **every** live-arrow-changing write
  (Record/Propose/Clarify/Supersede/Retire/Remove/ChangeRecord/CollectRemovalCandidates) —
  the "model checks everything, gate every door" decision. `GuardianDecision` has both a
  `Record` and a `Referent` variant — "one mechanism, two surfaces" (586 §3). It journals
  the operation + the record-set bundle the guardian saw + the verdict — the training
  dataset, captured from the start.

## Intent layer — coherent, all design records live

The store holds **1398 records**. The session's design decisions are all live and
consistent:

| Record | Domain | What |
|---|---|---|
| `zjho` | `(Information Documentation)` | Spirit is a universal intent tool for every human |
| `0zi7` | `(Knowledge Taxonomy)` | Domain granularity tracks intent density |
| `4wt3` | `(Knowledge Taxonomy)` | Variable-depth tree; dense branches nest a third tier |
| `tfpd` | `(Governance Policy)` | Guardian judges against verbatim psyche words + context |
| `r57r` | `(Governance Policy)` | Every change needs a justifying statement; deletion ≠ replacement |
| `kasm` | `(Craft Architecture)` | Guardian decides entry + new referents atomically (no orphans) |
| `bsrv` | `(Information Documentation)` | camelCase for multi-word string atoms |
| `uuh7` | `(Information Documentation)` | Recompile is cheap; zero-downtime is the goal |
| `qjrf` | `(Information Classification)` | Intent layer holds intent, not information |

`INTENT.md` reflections from 588: **primary done** (`uuh7`). The `spirit/INTENT.md` and
`nota-next/INTENT.md` prose from 588 **did not land** — verified against `origin/main`:
neither repo's INTENT.md carries the domain/referent/guardian model or the camelCase
constraint, even though the schema/code did ship. Operator landed the implementation but
skipped the per-repo INTENT.md reflection. This is a live gap (the rule is "update a
repo's INTENT.md on the same branch as the work"); see open item #5.

## Migration reality — the table is the easy part

The Craft→Software remap **already exists** in `production_migration.rs` (origin/main,
deterministic, tested as `upgrades_version_seven_domains_into_software_branch`):

| Old Craft leaf | New |
|---|---|
| Programming | `(Software (Languages ProgrammingLanguages))` |
| Architecture | `(Software (Engineering SoftwareArchitecture))` |
| Schema | `(Software (Data SchemaEvolution))` |
| Infrastructure | `(Software (Operations InfrastructureAsCode))` |
| Versioning | `(Software (Engineering VersionControl))` |
| Testing | `(Software (Quality Testing))` |
| Tooling | `(Software (Operations BuildSystem))` |

But its **blast radius is 2 records** — only `(Craft Architecture)` has live records (2);
the other six evicted leaves have zero. So the mandatory mechanical migration is a no-op.

The real finding: **the live store barely uses the domain vocabulary.** Of 1398 records,
**1102 are under `(Information Documentation)` and 302 under `(Governance Policy)`** —
essentially the whole store sits in two catch-all leaves. A direct sample of the
`(Information Documentation)` bucket is overwhelmingly *software-engineering* intent (NOTA
encoding, Rust discipline, schema lowering, daemon protocol, SEMA, secrets) — dumped there
because the old vocabulary had no precise software home. So deploying the Software branch
refines the *schema* but the *data* stays generic. Making the corpus actually reflect the
294-domain + Software vocabulary is a **per-record semantic re-tag** — the guardian's job,
not a variant→variant table — and it's optional, post-deploy, and corpus-wide (~1400).
**Deferred per psyche (2026-06-11): it needs an LLM pass; not now.**
This is the empirical case for the Software branch: software is by far the dominant slice
of real intent (`0zi7` confirmed by the data), it just never had a home.

## Open items

1. **Deploy + migration is the gate to "live."** System-operator deploy of `origin/main`
   `c30bed3` + run `production_migration.rs` over the 1398-record store. Until then the
   live vocabulary is the old one.
2. **Overlap ruling (587 decision 6) is unresolved and now lives in the enum.** Both
   `Technology(Networking)` and `Software(Distributed(Networking))` exist; same for
   `Information(Database)` vs `Software(Data)`, `Technology(Intelligence)` vs
   `Software(Intelligence)`. A networking/DB/AI intent has two plausible homes — capture
   is non-deterministic until the boundary is ruled. Proposed boundary (587): Technology =
   hardware/societal framing, Information = records/library framing, Software = build-it
   framing.
3. **Re-file `kasm` and peers post-deploy.** `kasm` (and other software-meta records under
   the soon-to-vanish `Craft` software leaves) re-tag to `Software(...)` + referent
   `spirit`. Mechanically the migration handles the re-tag; whether to *enrich* with
   referents is a separate guardian-aware pass.
4. **Guardian implementation audit (optional).** The gate/journal landed; a designer audit
   against 585/586 (temperature-0 pin, complete-retrieval, reason-set-generated-from-enum,
   type-aware retry) would confirm the *judgment* quality, not just the plumbing.
5. **588 INTENT.md prose unmerged.** The `spirit/INTENT.md` (domain+referent model,
   guardian constraints) and `nota-next/INTENT.md` (camelCase) reflections from 588 are not
   on `origin/main`. They're prose syntheses of already-recorded intent — ready to land on a
   designer `next` branch in `~/wt` (code repos; designers don't push code-repo main), or
   for operator to fold into the next integration.

## Net

Nothing is blocked on design. The redesign is built and faithful; it stands one deploy
away from live. The substantive remaining *design* question is the overlap ruling (#2);
everything else is operator/system-operator execution.
