# Spirit record redesign — per-kind variants + relations + weight (version 5→6)

System-designer design report. Corrected, source-grounded, implementable
shape for the next Spirit record in the schema-derived spirit pilot. Every
schema construct below is confirmed against the schema-next / schema-rust-next
language map; every pilot fact is cited to `file:line` in
`/git/github.com/LiGoldragon/spirit`.

## Intent anchors

The corrected direction captured this session, honored exactly:

- `(Spirit Decision 3awz)` [Spirit record fields vary by kind rather than
  every record carrying every field; a private-bearing record carries a
  privacy field, an ordinary public record omits it; eliminates fields a kind
  does not use; tighter purpose-fit shape per kind.]
- `(Spirit Correction 22t6)` [There is NO composite intent type in code —
  composite/agglomeration is a language and behavior concept, not a record
  type or variant. Provenance/agglomeration is expressed through a RELATIONS
  FIELD on records, not a dedicated Composite type. Refreshing several intents
  need not produce one merged record — it may produce two or three records of
  different kinds.]
- `(Spirit Decision 50qy)` [Spirit records gain a relations field — a vector
  of short record-identifier hashes pointing to other records. Not all kinds
  carry relations but some do; the relation meaning can come from the
  kind/field that holds it. The relations field is the ONLY code change needed
  to support intent relation and agglomeration.]
- `(Spirit Principle 66bd)` [Intent refresh/agglomeration is primarily AGENT
  BEHAVIOR trained through a skill, not engine logic. The only supporting code
  is the relations field.]
- `(Spirit Decision 1gwe)` [Agglomeration/refresh is triggered by an automated
  auditor that auto-PROPOSES refreshes; the psyche CONFIRMS the retire of
  source records. Automated discovery, human-gated removal.]
- `(Spirit Clarification 515t)` [weight uses the same Magnitude ladder
  (Zero..Maximum) on a second axis distinct from certainty, NOT an integer
  count.]
- `(Spirit Principle 6vsl)` [certainty = confidence; weight = accumulated
  importance/reinforcement, especially for records derived from multiple
  sources.]

**No Composite variant, no Composite kind exists in this design.** The
agglomeration result is one-or-more ordinary records (any kind) whose
`relations` field points to the records they were refreshed from. `weight` is
a `Magnitude`, never a count.

## What the pilot looks like today (the starting point)

The record type is `Entry`, a flat five-field struct declared once in the
wire plane (`schema/signal.schema:65`):

```
Entry { Topics * Kind * Description * Magnitude * Privacy * }
```

Generated as a struct where every field is present on every record
(`src/schema/signal.rs:220-226`): `topics`, `kind`, `magnitude`,
`description`, `privacy` (`Privacy` is an alias of `Magnitude`,
`signal.schema:59`). `Kind` is a five-variant unit enum
(`signal.schema:69`); `Magnitude` is the eight-level ladder
(`signal.schema:70`) carrying an ordinal `weight()` in `src/store.rs:346-359`.
SEMA imports the same `Entry` for storage (`schema/sema.schema:2`), so stored
and wire shape are one rkyv type — there is no divergence to reconcile.
Identity is sema-engine's allocated `u64` `RecordIdentifier`
(`signal.schema:32`, allocated in `Store::record` `src/store.rs:201-207`),
not a hash and not a field on the record. The `Record` write-op variant
carries `Entry` as payload (`signal.schema:12` `Record Entry`; sema
`WriteInput::Record(Entry)`).

The two flaws this redesign fixes: every record carries `privacy` even when
public, and there is no way to express that one record refreshes or corrects
others.

## The new record shape: a Kind-headed enum of per-kind structs

### Why an enum, not a wider struct

Per-kind field sets (3awz) means the record's shape depends on its kind. The
schema language gives exactly one way to make a field set depend on a tag: an
enum where each variant carries a distinct struct payload. The language map
confirms a variant payload is a single `TypeReference` (one struct name), not
an inline field list — so the idiom is "declare a named struct per kind,
reference it as the variant payload" (the exercised triad pattern, e.g.
`MailLedgerEvent [Sent Processed]` + `Sent SentMail` / `Processed
ProcessedMail` at `signal.schema:52-54`). We apply that pattern to the record
itself.

`Kind` stops being a unit enum and becomes the record's discriminant: the
record IS `Kind`, and each variant carries its per-kind struct. This collapses
the old `Entry.kind: Kind` field into the enum tag — the kind is no longer a
field, it is the variant.

### The new `.schema` source (confirmed real syntax)

Authored into `schema/signal.schema`, replacing the flat `Entry { ... }` line
and the unit `Kind [ ... ]` line. All forms below are confirmed by the
language map: brace = struct, square-bracket = enum body, `(Variant Payload)`
= payload variant, `Type *` = derived field name, `(Vec T)` = vector, alias =
namespace-key with single reference.

```
  Certainty Magnitude
  Weight Magnitude
  Relations (Vec RecordIdentifier)

  CommonFields { Topics * Description * Certainty * Weight * }

  Decision DecisionFields
  Principle PrincipleFields
  Correction CorrectionFields
  Clarification ClarificationFields
  Constraint ConstraintFields

  DecisionFields      { CommonFields * Relations * }
  PrincipleFields     { CommonFields * Relations * }
  CorrectionFields    { CommonFields * Relations * }
  ClarificationFields { CommonFields * Relations * }
  ConstraintFields    { CommonFields * Privacy * Relations * }

  Entry [Decision Principle Correction Clarification Constraint]
```

Notes on what each line relies on, with map citations:

- `Certainty Magnitude` and `Weight Magnitude` are aliases onto the existing
  `Magnitude` ladder — the same idiom the pilot already uses for `Privacy
  Magnitude` (`signal.schema:59`). Two aliases over one enum on one record is
  confirmed unblocked (map Q5, Q7c). `Certainty` is the renamed successor of
  the old `Entry.magnitude` field (6vsl: certainty = confidence); the field is
  spelled with its purpose now that a second axis exists.
- `Relations (Vec RecordIdentifier)` is a vector-of-identifier alias —
  confirmed unblocked (map Q7b, `collections.rs:49-55`). `RecordIdentifier` is
  the engine's `Integer`/`u64` (`signal.schema:32`); see the relations
  decision below for the "short hash" reconciliation.
- `CommonFields { ... }` is a multi-field struct (4 fields), so it stays a
  named-field struct rather than collapsing to a Newtype (map: a one-field
  brace silently becomes a Newtype; two+ fields keep the struct).
- Each `*Fields` struct flattens `CommonFields` by reference plus its
  per-kind fields. **`Privacy` appears ONLY in `ConstraintFields`** —
  honoring 3awz (privacy only on the private-bearing variant). The other four
  kinds have no privacy field at all and cannot carry one.
- `Entry` is now an enum body listing the five kind variants; each variant
  name (`Decision` etc.) binds to its `*Fields` payload via the
  `Decision DecisionFields` alias lines (the `(Variant Payload)` binding form,
  exactly as `Record Entry` / `Sent SentMail` work today at
  `signal.schema:12,53`).

`Kind` as a standalone unit enum is **deleted** from the struct body — its
role is absorbed into the `Entry` variant tag. `Query` still needs to filter
by kind, so it keeps a kind selector; see the query section.

### Per-kind field rationale

The four-axis common core (`topics`, `description`, `certainty`, `weight`)
applies to every kind, so it lives in `CommonFields`. Beyond that:

- **Privacy** belongs only to records that can bear private substance. In the
  pilot the records that elevate privacy are constraints and the personal
  carve-outs; this design puts `Privacy` on `ConstraintFields` only, matching
  the captured intent's worked example ("a private-bearing record carries a
  privacy field, an ordinary public record omits it"). If the psyche wants
  another kind to be private-bearing, add `Privacy *` to that kind's `*Fields`
  struct — a one-line, additive change. **Open question flagged below.**
- **Relations** belongs to the kinds that point at other records:
  `Correction` (what it corrects) and any refreshed record (its sources). The
  decision below argues relations should be present on *all* kinds and reasons
  why; the schema above reflects that (every `*Fields` carries `Relations *`).

The four kinds without per-kind extras (`Decision`, `Principle`,
`Clarification`, plus `Correction`) differ from `Constraint` only by the
absence of `Privacy`. That is the point of 3awz: eliminate the field a kind
does not use. A public `Decision` cannot accidentally carry a privacy level
because the field does not exist on its struct.

## The relations decision: ONE field, meaning supplied by kind

**Decision: a single `relations` field, present on every kind's `*Fields`
struct, with meaning supplied by the variant tag — not per-kind distinct
relation fields, and not a separate relation-type tag.**

### Reconciling "some kinds relate" with "one field"

The psyche said both "a field for relations that contains just a short hash"
(one field) and "some kinds should relate" (selective presence). These
reconcile cleanly: relations is **one field name**, but its **meaning is read
through the variant tag**, and it is **empty (`[]`) on records that do not
relate**. A `Decision` with empty relations is a fresh root decision; a
`Correction` with non-empty relations corrects those records; a refreshed
`Principle` with non-empty relations was agglomerated from those sources. One
field, polysemous by kind, defaulting empty — this is exactly 50qy's "the
relation meaning can come from the kind/field that holds it."

I considered putting `Relations` only on the kinds that semantically relate
(`Correction` always; others only when refreshed). I recommend AGAINST that
and put it on all five, for three reasons:

1. **Refresh produces records of any kind** (22t6: "two or three records of
   different kinds"). An agglomerated `Decision`, `Principle`, or
   `Clarification` all need to carry source relations. Restricting relations
   to `Correction` would block the dominant refresh case.
2. **Empty-vector default costs nothing.** An empty `Vec` is the zero value;
   a root record simply has `[]`. There is no "field a kind does not use" cost
   here the way there is for privacy — relations is *usable* by every kind,
   just often empty.
3. **Uniform queries.** Keeping the field on every variant means a
   relation-walking query ("show me everything that refreshed record N") does
   not branch on kind.

The trade I am accepting: relations is structurally present on every record
even when empty, which is a mild tension with 3awz's "eliminate fields a kind
does not use." I resolve it by the distinction *unused vs usable-but-empty*:
privacy is genuinely unusable on a public Decision (it would be a category
error), so it is eliminated; relations is usable on every kind (any kind can
be a refresh result), so it stays with an empty default. Privacy is the field
3awz is really about; relations is the field 50qy adds.

### Refresh vs supersession distinguishable WITHOUT a relation-type tag

Agent-2's guardrail: a refresh and a supersession must be distinguishable, so
an automated walker does not confuse "this record absorbed those" with "this
record overrules those." The KIND supplies that distinction; no separate
relation-type tag is needed:

- A **`Correction`** with relations = `[N]` means *N is wrong / overruled* —
  supersession semantics. This is the existing correction relationship made
  explicit.
- A **non-`Correction`** record (`Decision`, `Principle`, `Clarification`,
  `Constraint`) with non-empty relations means *this record was refreshed /
  agglomerated FROM those sources* — refresh/provenance semantics. The sources
  are retired only after the psyche confirms (1gwe), but the records they roll
  into are not corrections — they are fresh statements of the same kind that
  consolidate the sources.

So: relations under a `Correction` tag = supersession; relations under any
other tag = agglomeration/refresh. The five-way kind tag already partitions
the relation meaning; adding a `RelationType [Refreshes Supersedes Cites]`
enum would duplicate information the kind already carries and is therefore
NOT added. (If a future need arises to cite a record without correcting or
refreshing it — e.g. "this decision builds on that principle" — that is the
one case the kind tag does not cover, and it would justify a minimal tag then.
Carried as a deferred possibility, not built now.)

## The weight decision

`weight` is a second `Magnitude` field (`Weight Magnitude` alias), distinct
from `certainty`, on `CommonFields` so every kind carries it (515t, 6vsl).

- **Default for ordinary records: `Medium`** (or whatever the psyche/agent
  states at authoring). Weight is accumulated importance; a brand-new single-
  source record has not accumulated anything, so it sits mid-ladder rather
  than at an extreme. (`Zero` would read as "no importance," which is wrong for
  a freshly-stated intent; `Medium` is the neutral resting value.) The CLI
  author may state it explicitly; if omitted, the author-facing default is
  `Medium`. **This default is a behavior/skill choice, flagged for psyche
  confirmation below — the engine does not impose it.**
- **A refreshed record's weight** is set by the proposing auditor / confirming
  psyche, conceptually *compounding* from its sources: a record that
  consolidates three `High`-certainty sources should land high on the weight
  ladder (e.g. `VeryHigh` or `Maximum`). Because weight is a `Magnitude` not a
  count, "compounding" is a qualitative judgment ("these sources together are
  very important"), not arithmetic. **This is behavior, not engine logic** —
  the engine stores whatever `Magnitude` the record carries; the skill
  trains how the auditor proposes it and how the psyche adjusts it. The
  existing `Magnitude::weight()` ordinal (`src/store.rs:346-359`) already lets
  queries sort/threshold on it, so weight is query-comparable for free.

certainty and weight are orthogonal: a record can be `Maximum` certainty
(we are sure) and `Low` weight (minor matter), or `Low` certainty (tentative)
and `High` weight (would matter a lot if true). Two independent `Magnitude`
axes on one record are confirmed unblocked (map Q7c — precedent is the pilot's
own `Entry { ... Magnitude * Privacy * }` where both fields are the same enum).

## Code vs behavior split

This is the heart of 66bd / 50qy: **the relations field is the ONLY engine
change that supports relation and agglomeration. Everything about WHEN to
refresh, WHAT to merge, and WHICH sources to retire is agent behavior in a
skill.**

### CODE (small, mechanical)

1. **Schema** (`schema/signal.schema`): replace flat `Entry`/`Kind` with the
   per-kind enum + `*Fields` structs + `Certainty`/`Weight`/`Relations`
   aliases (source above).
2. **Emitted Rust** (`src/schema/signal.rs`, `src/schema/sema.rs`,
   `src/schema/nexus.rs` — all regenerated, never hand-edited): `Entry`
   becomes a five-variant enum; five `*Fields` structs and `CommonFields`
   appear; `Kind` unit enum disappears. Driven by `build.rs` regen.
3. **Store predicate** (`src/store.rs`): `Entry::matches`, `Query::matches`,
   and `Entry::magnitude_weight` must read through the variant instead of flat
   fields (they currently read `entry.topics`, `entry.kind`, `entry.privacy`,
   `self.magnitude` directly at `src/store.rs:313-343`). New accessors like
   `Entry::topics()`, `Entry::certainty()`, `Entry::privacy() -> Option<...>`
   match on the variant. `privacy()` returns `Option` because four kinds have
   no privacy; the privacy filter treats "no privacy field" as public
   (`Zero`).
4. **Validation** (`src/engine.rs`): `Entry::validate` (`src/engine.rs:362-375`)
   matches on the variant to reach `topics`/`description` (same emptiness
   rules, now per-variant).
5. **Wire/operation binding**: the `Record` write-op variant payload stays
   `Entry` (`signal.schema:12`, sema `WriteInput::Record(Entry)`); since
   `Entry` is now the enum, no change to the operation binding — only the
   payload's internal shape changed. Sema continues importing
   `spirit:signal:Entry` (`sema.schema:2`), one rkyv identity across planes
   (map Q6).
6. **CLI**: no code change — the CLI parses a NOTA `Input` and the daemon
   links the NOTA surface behind `nota-text`. The author-facing form changes
   (see below) but that is a consequence of the schema, not CLI code.
7. **Version bump** (`build.rs`): `"0.1.0"` → next version literal (see
   migration); plus the dead `UpgradeFrom`/`AcceptPrevious` stubs get their
   first real impl for `OldEntry → Entry`.

That is the entire code surface. There is **no** Composite type, **no** merge
function, **no** refresh engine, **no** auditor code in spirit itself.

### BEHAVIOR (the substance, in skills)

- **The refresh/agglomeration judgment** — when several intents are stale or
  overlapping, deciding to consolidate them, choosing the resulting kind(s)
  (22t6: may be two or three records of different kinds), writing the new
  record(s) with `relations` pointing at the sources and a compounded
  `weight` — lives in `skills/intent-maintenance.md` (and the intent-log
  skill). This is agent behavior trained through prose, per 66bd.
- **The automated auditor** (1gwe) — discovers refresh candidates and
  auto-PROPOSES them; the psyche CONFIRMS the retire of source records. The
  auditor is the proposed third role (DeepSeek, per AGENTS.md); its proposals
  are records-with-relations awaiting psyche confirmation. Automated
  discovery, human-gated removal. The retire itself is the existing
  `Remove RecordIdentifier` operation — no new engine op.
- **weight defaults and compounding** — the `Medium` default and the
  qualitative compounding of source weights are skill-trained authoring
  conventions, not engine rules.
- **relation meaning by kind** — that a `Correction`'s relations = what it
  supersedes, and a non-`Correction`'s relations = what it refreshes-from, is
  a reading convention documented in the skill; the engine stores raw
  identifier vectors and assigns them no meaning.

## Migration: version 5 → 6 (flat Entry → per-kind enum)

This is a **breaking contract change** requiring psyche authorization —
already given for the pilot (version 5→6). Every existing flat record maps
deterministically onto a new variant because each already carries a `Kind`.

### Migration table

| Old flat `Entry` field | Old value example | New per-kind variant + field |
|---|---|---|
| `kind` | `Decision` | selects variant `Entry::Decision(DecisionFields{..})` |
| `kind` | `Constraint` | selects variant `Entry::Constraint(ConstraintFields{..})` |
| `topics` | `[[schema]]` | `CommonFields.topics` (unchanged) |
| `description` | `[...]` | `CommonFields.description` (unchanged) |
| `magnitude` | `Maximum` | `CommonFields.certainty` (renamed, same value) |
| (none) | — | `CommonFields.weight` = `Medium` (new; default for migrated records) |
| `privacy` = `Zero` | public | DROPPED — variant has no privacy field |
| `privacy` > `Zero` | elevated | preserved ONLY if kind is `Constraint`; see note |
| (none) | — | `relations` = `[]` (new; empty for all existing records) |

Notes:

- **certainty** is the old `magnitude` value verbatim — pure rename, no value
  change (6vsl).
- **weight** is new; migrated records get `Medium` (the neutral default).
  Records the psyche wants weighted higher are adjusted afterward by behavior,
  not by the migration.
- **privacy on `Zero` records is dropped** — they were public, and the new
  public variants have no privacy field. Nothing is lost (the absent field IS
  public).
- **privacy on elevated records**: only `Constraint` has a privacy field in
  this design. Migration must check — if an existing elevated-privacy record is
  NOT a `Constraint`, its privacy level has nowhere to land. This is the one
  migration risk and the reason the privacy-bearing-kinds question is flagged
  for the psyche below. The map confirms elevated-privacy records exist; the
  migration must enumerate which kinds currently carry `privacy > Zero` before
  finalizing which `*Fields` get `Privacy *`.
- **relations is empty for every existing record** — no existing record was
  authored with relations, so all migrate to `[]`.

### Mechanism (the pilot's actual version-handover path)

The map names the real (currently-dead) mechanism, so the migration uses it
rather than inventing one:

1. Bump the asschema version literal in `build.rs:31`
   `GenerationPlan::new(&crate_root, "spirit", "0.1.0")` to the 6 version
   (this propagates into all three `*.asschema` headers). Regenerate with
   `SPIRIT_UPDATE_SCHEMA_ARTIFACTS` set.
2. Retain the old flat `Entry` as `OldEntry` (the "last version" package the
   pilot intends but has not wired — `INTENT.md:209-212`,
   `ARCHITECTURE.md:437-438`). This is the first real population of the
   version-handover slot.
3. Implement the dead trait stub for real:
   `impl UpgradeFrom<OldEntry> for Entry` (the generated trait at
   `src/schema/signal.rs:1197-1209`, currently zero impls) performing the
   field-mapping above — match old `kind`, build the matching variant, rename
   `magnitude`→`certainty`, default `weight`=`Medium`, drop/relocate
   `privacy`, set `relations`=`[]`.
4. Storage handover is exercised as the pilot already does it: copy a seeded
   real `.sema` file and run the upgrade over it
   (`ARCHITECTURE.md:319`, `INTENT.md:239`). The sema-engine
   `SchemaVersion::new(1)` (`src/store.rs:23`) is the database-format version,
   independent of the asschema 6; bump it only if the on-disk table layout
   changes (the rkyv `Entry` bytes DO change shape here, so this likely bumps
   to `SchemaVersion::new(2)` and the upgrade runs at open time).

This is the first time the pilot's `UpgradeFrom`/`AcceptPrevious` machinery
does real work — the redesign converts dead stubs into the live migration
path, which is itself the explicit next-slice gap the maps flag
(`ARCHITECTURE.md:448-450`, `INTENT.md:261-263`).

## CLI surface impact

Today the author-facing record is `(Record ([topics] Kind [desc] Magnitude
Privacy))` — positional, with the README example omitting privacy
(`README.md:47`): `(Record ([[schema]] Constraint [schema creates the
interface] Maximum))`. With per-kind variants, the **Kind becomes the record
head** (it is now the enum variant tag, not a positional field), and the body
is that kind's `*Fields` struct in declared field order.

NOTA is positional, bracket-strings only, no quotation marks (per AGENTS.md).
`CommonFields` flattens into each variant's leading positions. Three worked
examples:

**A public Decision** (no privacy field; relations empty). `Entry::Decision`
carrying `DecisionFields { CommonFields(topics, description, certainty,
weight), relations }`:

```
spirit "(Record (Decision ([[runtime] [schema]] [schema creates the interface] Maximum Medium [])))"
```

Reading positionally: topics `[[runtime] [schema]]`, description `[schema
creates the interface]`, certainty `Maximum`, weight `Medium`, relations `[]`.

**A Correction with relations** (supersedes record 7 and record 12; the kind
supplies "these are corrected"):

```
spirit "(Record (Correction ([[naming]] [Identifier not Id — full English words] VeryHigh High [7 12])))"
```

topics `[[naming]]`, description `[Identifier not Id ...]`, certainty
`VeryHigh`, weight `High`, relations `[7 12]`. Because the variant is
`Correction`, the walker reads `[7 12]` as *superseded*, not *refreshed-from*.

**A private Constraint** (the one kind with a privacy field). `ConstraintFields
{ CommonFields..., privacy, relations }`:

```
spirit "(Record (Constraint ([[deploy]] [the staging key rotates weekly] High Medium VeryHigh [])))"
```

topics `[[deploy]]`, description `[...]`, certainty `High`, weight `Medium`,
privacy `VeryHigh` (narrow audience), relations `[]`. Only `Constraint` accepts
a privacy positional; attempting `(Record (Decision (... VeryHigh ...)))` with
an extra privacy value would fail to parse because `DecisionFields` has no such
field — the per-kind shape is enforced by the schema, exactly as 3awz intends.

A **refreshed Principle** (agglomerated from records 3, 9, 14; kind is
`Principle`, so relations read as *refreshed-from*; weight compounded up):

```
spirit "(Record (Principle ([[intent] [naming]] [names are full English words and do not carry ancestry] Maximum Maximum [3 9 14])))"
```

The auditor proposes this record (1gwe); the psyche confirms; then `(Remove
3)`, `(Remove 9)`, `(Remove 14)` retire the sources — the existing remove op,
human-gated.

Query also changes shape: `Query` currently has `kind (Optional Kind)`
(`signal.schema:66`), but `Kind` the unit enum is deleted. The query keeps a
kind selector by reintroducing a lightweight `KindSelector [Decision Principle
Correction Clarification Constraint]` unit enum used ONLY for filtering (it is
not the record), so `(Observe ((Full [[schema]]) (Some Decision)))` still
works. This is a small additive code item folded into the edit list.

## Ordered implementer edit list

1. `schema/signal.schema` — delete the flat `Entry { ... }` line
   (`:65`) and the unit `Kind [ ... ]` line (`:69`). Add: `Certainty
   Magnitude`, `Weight Magnitude`, `Relations (Vec RecordIdentifier)`,
   `CommonFields { ... }`, the five `*Fields` structs, the five
   `Decision DecisionFields`-style variant bindings, `Entry [Decision
   Principle Correction Clarification Constraint]`, and a `KindSelector [ ...
   ]` unit enum for queries. Repoint `Query` to `kind (Optional KindSelector)`.
2. `build.rs:31` — bump `"0.1.0"` to the version-6 literal.
3. Regenerate: run the build with `SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1` so
   `src/schema/{signal,sema,nexus}.rs` and `schema/*.asschema` rewrite. Do NOT
   hand-edit generated files.
4. `src/store.rs` — rewrite `Entry::matches`, `Query::matches`,
   `Entry::magnitude_weight` (now `certainty`/`weight` accessors) and the
   privacy filter (`PrivacySelection::matches`) to read through the variant;
   add `Entry::topics()`, `Entry::certainty()`, `Entry::weight()`,
   `Entry::privacy() -> Option<Privacy>`, `Entry::relations()` accessors. Treat
   `privacy() == None` as public (`Zero`) in the filter
   (`src/store.rs:313-343`).
5. `src/engine.rs` — rewrite `Entry::validate` (`:362-375`) to match the
   variant for `topics`/`description` emptiness checks.
6. `src/schema/signal.rs` (generated) — confirm `OldEntry` retention for the
   upgrade: add the previous flat `Entry` as `OldEntry` in a kept-around
   module (the "last version" package), and write `impl UpgradeFrom<OldEntry>
   for Entry` performing the migration-table mapping.
7. `src/store.rs:23` — bump `SchemaVersion::new(1)` → `new(2)` (the on-disk
   rkyv shape changed) and run the `UpgradeFrom` upgrade at open time over a
   copied seed `.sema`.
8. Tests — exercise the migration over a seeded real `.sema`
   (`ARCHITECTURE.md:319`); add per-kind round-trip tests (public Decision,
   Correction-with-relations, private Constraint, refreshed Principle).
9. `ARCHITECTURE.md` / `INTENT.md` — record the per-kind shape, the relations
   semantics-by-kind, the weight axis, and that the dead `UpgradeFrom`
   machinery is now live.
10. Skills — `skills/intent-maintenance.md` (and intent-log skill) gain the
    refresh/agglomeration behavior, the auditor-proposes / psyche-confirms loop
    (1gwe), the weight-compounding convention, and the relations-meaning-by-kind
    reading rule. This is the behavior half of the code-vs-behavior split.

## Residual open questions for the psyche

1. **Which kinds bear privacy?** This design puts `Privacy` on `Constraint`
   only, following the captured worked example. But existing elevated-privacy
   records may be other kinds — migration cannot relocate their privacy if
   their kind has no privacy field. Need the psyche to confirm the
   private-bearing kind set (Constraint only? also Decision/Clarification?)
   before the migration is finalized.
2. **weight default for ordinary records.** I chose `Medium` (neutral resting
   value, since a single-source record has accumulated no reinforcement).
   Confirm, or prefer `Low`/`Minimum`.
3. **A cite-without-correct-or-refresh relation** (e.g. "this decision builds
   on that principle") is the one case the kind tag does not partition. Carried
   as deferred — confirm it is genuinely out of scope for version 6, or it
   justifies a minimal `RelationType` tag now.

## Verification outcome — four blockers and the revised direction

The design above was adversarially verified by three independent agents
(feasibility / migration / intent-fidelity), one of which *empirically lowered
the proposed schema and round-tripped it through NOTA*. All three returned
`sound=false`. Four blockers, all evidenced against source. The sections below
**supersede** the corresponding parts above.

### Blocker 1 — no struct flattening (supersedes the `CommonFields` schema + the flat CLI examples)

`CommonFields *` does **not** flatten — schema-next/schema-rust-next have no
struct-field flattening (verified by grep + emission); `CommonFields *` lowers
to a *nested* field `common_fields: CommonFields`. The flat positional CLI
examples (lines 427, 437, 448, 461) and the migration table's field-peer
mapping are therefore wrong as written.

**Revision: inline the common fields into each per-kind struct** (no
`CommonFields`), giving the intended flat positional wire form:

```
  Certainty Magnitude
  Weight    Magnitude
  Relations (Vec RecordIdentifier)

  DecisionFields      { Topics * Description * Certainty * Weight * Relations * }
  PrincipleFields     { Topics * Description * Certainty * Weight * Relations * }
  CorrectionFields    { Topics * Description * Certainty * Weight * Relations * }
  ClarificationFields { Topics * Description * Certainty * Weight * Relations * }
  ConstraintFields    { Topics * Description * Certainty * Weight * Privacy * Relations * }

  Entry [Decision Principle Correction Clarification Constraint]
```

The four-line repetition per kind is the cost of an honest flat wire form; it is
acceptable and keeps the positional CLI examples (Decision/Correction/Constraint
above) correct as written. The per-kind enum itself, `Vec<RecordIdentifier>`,
two same-`Magnitude` fields, and cross-plane reuse are all confirmed *feasible*
— only the flatten assumption was false.

### Blockers 2 & 3 — the pilot has no migration machinery; clean break instead

The `SchemaVersion` bump is a **hard reject**, not a migration trigger: sema
(`sema/src/lib.rs:528-540`) refuses to open a file on version mismatch, and
`UpgradeFrom`/`AcceptPrevious` are zero-impl stubs with no caller, no registry,
nothing in the open path. There is no `OldEntry` / read-as-old-type module, and
`spirit/INTENT.md:209-212` **explicitly forbids faking** the last-version
package (no real previous release tag exists). The pilot's version literals are
`0.1.0` / `SchemaVersion(1)` — there is no "5/6" in the pilot at all; the
"5→6" is *production* Spirit's record-schema numbering, a different axis.

**Revision: this branch is a clean-break SHAPE prototype** (subject to the scope
decision below). The pilot is `0.1.0`, not production, with no precious data:
change the record shape, bump `SchemaVersion(1)→(2)` so any stale pilot DB is
rejected (correct — start fresh), and write **no** `UpgradeFrom`. The real
migration of production records is *operator/production* work for when
production Spirit cuts over to the schema-derived stack — not the designer's
pilot prototype. This dissolves blockers 2 and 3 and the migration-table
privacy-loss risk (there are no records to migrate in the pilot).

### Blocker 4 — relations must reference the stable hash, not reusable `u64`

`50qy` says relations is a vector of record-identifier **hashes** "sized just
long enough for non-collision." The design typed it `Vec<RecordIdentifier>`
where the pilot's `RecordIdentifier` is the engine's reusable sequential
`u64` — the *exact* identity this lane's report 64 (`Spirit 2581-2583`)
replaced with hashes *because* reuse-on-removal makes references unstable. A
relations vector of reusable `u64` points at slots that can be reassigned — a
silent-corruption bug by construction.

**Revision: relations must reference the stable hash identity.** Production
Spirit v0.5.0 already mints base36 hashes; the schema-derived pilot still uses
`u64` and is *behind* production on identity. So this redesign is **coupled to
the hash-identity adoption (report 64)** in the pilot. See the scope decision.

### The genuine decisions (for the psyche)

1. **Scope / migration.** Recommended: clean-break SHAPE prototype in the pilot
   (no migration; production migration is later operator work). Alternative:
   also build the out-of-band migration tool + frozen `OldEntry` reader now.
2. **Hash-identity coupling.** relations needs stable hashes (`50qy` + report
   64). The pilot is still on `u64`; production v0.5.0 already has hashes.
   Recommended: bring the pilot to hash identity *on this branch* (it is the
   coherent "next record architecture" change and makes relations correct by
   construction). Alternative: land hash identity first as its own branch, then
   relations on top.
3. **Privacy shape.** `3awz` says public records omit privacy, private records
   carry it — but privacy is orthogonal to the five kinds (a Decision can be
   private). Putting privacy only on `Constraint` (the design above) was a
   misread. Recommended: privacy is an optional field available to *any* kind
   (absent = public), so any kind can be private. Alternative: a dedicated
   private record shape distinct from the five kinds.

Minor (resolved, not asked): relations stays on **all** kinds with an empty
default (a refresh can produce any kind, per `22t6`); the verifier asked this be
surfaced rather than silently chosen — it is surfaced here. The `KindSelector`
re-export break (`lib.rs:70`), the `weight()` vs `Magnitude::weight()` naming
collision (rename the ordinal to `Magnitude::rank()`), and the three-version-axis
disambiguation are folded into the implementer edit list as mechanical fixes.
