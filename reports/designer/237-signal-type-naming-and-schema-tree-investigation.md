# 237 — signal-type naming + schema-as-tree investigation

*Investigating the psyche's diagnosis that agents over-declarate
signal type names and produce flat schemas where trees are needed.
Recovers a lost intent record from `/124`. Locates two distinct
naming failure modes both rooted in the same schema-shape failure.
Proposes guidance-file edits to bring this into skills/naming.md
and skills/contract-repo.md. Addresses the "are we underusing
signal verbs?" question.*

## 0 · TL;DR

Three findings:

1. **The lost intent is recovered.** `reports/designer-assistant/124-query-suffix-as-missing-schema-layer.md` carries the analysis the prior agent should have logged as intent. I've now recorded the substance in `intent/naming.nota` (2026-05-19T18:55Z). The substance: *"Query is its own logic plane — not a name suffix repeated across sibling variants."* The psyche specifically named the deeper split: `query -> recent -> repositories`.

2. **Signal verbs are not underused.** The 6-verb spine
   (`Assert` / `Mutate` / `Retract` / `Match` / `Subscribe` /
   `Validate`) is being used correctly at the request-variant
   level. The actual problem is that domain types **duplicate
   the verb signal at the payload-name level** (e.g., five
   `Match *Query(*Query)` siblings all carrying `Query` in their
   names). The verb is the right verb; the payload name is
   redundantly carrying the read-plane signal that the verb
   already supplied.

3. **The naming failures and the schema-shape failure are the
   same failure.** Both `Repository*` redundant prefixes
   (addressed by `/123` rename pass) and `*Query` repeated
   suffixes (analyzed in `/124` but unactioned) are symptoms of
   the same underlying mistake: not seeing the schema as a tree
   that can grow. Agents create new top-level variants with
   descriptive names instead of recognizing that a repeated
   category word is the schema asking for a parent type.

## 1 · The live evidence: signal-repository-ledger

Current contract on `main` (2026-05-19, unchanged since `/124`
was written):

```rust
signal_channel! {
    channel Ledger {
        request Request {
            Assert ReceiveHookNotification(ReceiveHookNotification),
            Assert PushObservation(PushObservation),
            Match EventQuery(EventQuery),
            Match RecentRepositoriesQuery(RecentRepositoriesQuery),
            Match ChangedFileQuery(ChangedFileQuery),
            Match CommitMessageQuery(CommitMessageQuery),
            Match CatalogQuery(CatalogQuery),
        }
        reply Reply {
            EventRecorded,
            EventListing,
            RecentRepositoriesListing,
            ChangedFileListing,
            CommitListing,
            CatalogListing,
            RequestUnimplemented,
        }
    }
}
```

Three observations:

- **Five sibling variants in the request enum all suffixed
  `*Query`.** That suffix repetition is the schema smell.
- **Five sibling variants in the reply enum all suffixed
  `*Listing`.** Same pattern — the reply side has the same
  missing parent.
- **The 6-verb spine is correct.** `Match` is the right verb
  for reads; `Assert` is the right verb for writes. The verb
  isn't the problem.

The right shape (per `/124`):

```rust
signal_channel! {
    channel Ledger {
        request Request {
            Assert ReceiveHookNotification(ReceiveHookNotification),
            Assert PushObservation(PushObservation),
            Match Query(Query),
        }
        reply Reply {
            EventRecorded(EventRecorded),
            QueryResult(QueryResult),
            RequestUnimplemented(RequestUnimplemented),
        }
    }
}

pub enum Query {
    Events(EventSelection),
    RecentRepositories(RecentRepositorySelection),
    ChangedFiles(ChangedFileSelection),
    CommitMessages(CommitMessageSelection),
    Catalog(CatalogSelection),
}

pub enum QueryResult {
    Events(EventListing),
    RecentRepositories(RecentRepositoriesListing),
    ChangedFiles(ChangedFileListing),
    CommitMessages(CommitListing),
    Catalog(CatalogListing),
}
```

The tree grew: where there were 5 flat sibling Match-variants,
there's now one `Match Query` variant that branches into a
`Query` enum carrying the read targets. Same data; cleaner
shape; correct separation of concerns.

The psyche's deeper split — `query -> recent -> repositories` —
would happen later, once recency recurs across multiple query
targets:

```rust
pub struct RecencyWindow {
    pub since_received_at: Option<Timestamp>,
    pub limit: QueryLimit,
}

pub enum Query {
    Events(EventSelection, RecencyWindow),
    Repositories(RepositoryFilter, RecencyWindow),
    Commits(CommitFilter, RecencyWindow),
    ...
}
```

The schema continues to grow into a tree as repetition reveals
the next missing parent. *"the schema needs to grow more
complex."*

## 2 · The naming failure is the schema-shape failure

The psyche's diagnosis was sharper than I initially understood:
*"the agent doesn't see how the schema needs to evolve because
it doesn't create the base schema properly from the beginning.
So it ends up being this really stuffy, flat table of things
where it should really grow into a tree."*

The two failure modes I've now seen — `Repository*` redundant
prefixes and `*Query` repeated suffixes — both come from this
same diagnosis. In the first case, the schema put the contract
domain in every variant name (flat: each variant introduces
itself as "I'm a thing from the repository ledger"). In the
second case, the schema put the read-plane category in every
variant name (flat: each variant introduces itself as "I'm a
query").

In neither case did the agent ask: *"is this repeated word a
missing parent type?"* — which is the question that produces
the tree shape.

The fix is a single rule at the cross-language level:

> **Repeated category words across sibling names are schema
> smells.** When several adjacent types or variants share the
> same prefix or suffix — `*Query`, `*Command`, `*Event`,
> `*Listing`, `*Selection` — stop and ask whether that
> repeated word is a missing parent enum, relation, record,
> module, or contract layer. Names should not carry logic
> planes that the schema can represent directly.

This goes one level deeper than the existing namespace-prefix
rule. The namespace-prefix rule says "don't repeat what the
namespace already supplies"; the repeated-category-word rule
says "if the same word appears across siblings, the schema is
missing a layer that would carry it."

The /124 report has a draft of this rule. It hasn't landed in
the skill files yet.

## 3 · Are we underusing signal verbs?

No. The 6-verb spine is being used correctly. Examples across
the workspace's contracts:

- `signal-repository-ledger`: 2× `Assert`, 5× `Match`. Read /
  write boundary is honored.
- `signal-persona-spirit`: 2× `Assert`, 3× `Match`, 2×
  `Subscribe`, 2× `Retract`. All verb mappings correct.
- `signal-persona-mind`, `signal-persona-orchestrate`,
  `signal-persona-router`, `signal-persona-harness`: I haven't
  audited these in detail, but the patterns in the workspace
  reports suggest similar verb-correct usage.

What IS happening is that domain payload types carry
verb-shaped suffixes (`*Query`, `*Subscription`, `*Observation`)
that duplicate the verb already declared at the request
variant. The redundancy is at the payload-name level, not the
verb level.

A useful distinction for the skill files:

- **`*Subscription`** for a payload of a `Subscribe` variant —
  the suffix names the relation kind, which IS the carrier
  of subscription identity (token, lifecycle). The relation
  has a real noun form. Likely keep.
- **`*Observation`** for a `Match` payload — the suffix names
  the query as a noun ("the act of observing X"). Defensible
  as domain vocabulary; could also collapse.
- **`*Query`** for a `Match` payload — the suffix names the
  query relation flatly; when there are many of them, the
  parent missing.
- **`*Listing`** for a query result reply — same shape; when
  there are many sibling listings, the parent missing.

The pattern: when a suffix appears once (or twice) in a
contract, it's domain vocabulary and probably fine. When it
appears 5+ times across siblings, it's an unrepresented
parent. The skill should name the threshold by behavior
("when you find yourself adding a third sibling with the same
suffix, stop and ask") rather than by count.

## 4 · The over-declarative-names pattern

The persona-spirit example (the operator's rename list that
opened this turn) is the cleanest case study of
over-declaration:

```
IntentTopic, IntentSummary, IntentQuote, IntentContext,
IntentTimestamp, IntentRecordIdentifier, IntentRecordQuery,
IntentRecordObservation, IntentRecordSubscription,
IntentRecordSubscriptionToken, IntentRecordSummary,
IntentRecordProvenance, IntentRecordCaptured,
IntentRecordsObserved, IntentRecordSubscriptionOpened,
IntentKind, IntentCertainty, IntentObservationMode
```

Sixteen types prefixed `Intent`. The crate is
`signal-persona-spirit`; the domain is intent. **Every
prefix is redundant.**

The operator's correction (in this turn's prompt) lands the
right rename per the no-redundant-ancestry rule. But the
deeper question is: how did this happen in the first place?

The pattern: an agent designing the schema reaches for
"safe" naming — each type self-introduces with its domain
prefix so the type name "stands alone." This is exactly the
mistake the namespace-prefix rule catches, generalized to
domain-prefix. The agent didn't trust the namespace to supply
context.

The operator's renames take this from elaborate to clean.
That's the fix at the rename level. The deeper fix — agents
not creating elaborate names in the first place — comes from
the AGENTS.md hard override + ESSENCE.md §Naming. With the
pair-of-rules now visible upfront (per this session's edits),
the next agent designing a contract should reach for the
cleaner shape from the start.

## 5 · Proposed skill edits

Three edits would land the schema-tree intent into the
discipline surfaces. None applied yet — surfacing for psyche
review first.

### `skills/naming.md` — new §"Repeated category words = missing schema layer"

Position: after the existing "Anti-pattern: prefixing names
with their namespace or domain" section.

Draft:

```markdown
## Anti-pattern: repeated category words across sibling names

When several adjacent types or variants share the same prefix
or suffix — `*Query`, `*Command`, `*Event`, `*Listing`,
`*Selection`, `*Mode`, `*Result` — stop and ask whether the
repeated word is a missing parent enum, relation, record,
module, or contract layer. Repeated category words are schema
smells, not naming choices.

```rust
// Wrong — Query repeated as a suffix across 5 siblings
Match EventQuery(EventQuery),
Match RecentRepositoriesQuery(RecentRepositoriesQuery),
Match ChangedFileQuery(ChangedFileQuery),
Match CommitMessageQuery(CommitMessageQuery),
Match CatalogQuery(CatalogQuery),

// Right — Query is the parent enum; siblings name read targets
Match Query(Query),

pub enum Query {
    Events(EventSelection),
    RecentRepositories(RecentRepositorySelection),
    ChangedFiles(ChangedFileSelection),
    CommitMessages(CommitMessageSelection),
    Catalog(CatalogSelection),
}
```

The threshold is behavioral, not numeric. When you find
yourself adding a third sibling with the same suffix, stop:
the schema is asking for a parent type.

**Why this rule pairs with the no-redundant-ancestry rule.**
The ancestry rule says "don't restate what the namespace
already supplies." The repeated-category rule says "if a word
recurs across siblings, the schema is missing a namespace that
would supply it." Together: names carry only what the schema's
structure doesn't carry; when names repeat a word, that word
should become structure.

This is one of the two failure modes producing "stuffy flat
tables of things where the schema should grow into a tree."
The other is the redundant-namespace prefix above. Both
symptoms; same underlying cause — not seeing the schema as a
growing tree.
```

### `skills/contract-repo.md` — strengthen the underspecified-roots row

The existing "Common mistakes" table has a row for "Root
variants underspecified." Extend it with the sibling-suffix
diagnostic; ensure the contract-specific worked example
(repository-ledger's `*Query`) is named.

Also: under §"Contracts name a component's wire surface", add
a paragraph after the existing "Do not fix under-specified
names by adding generic suffixes" bullet pointing at the
schema-tree principle.

### `skills/language-design.md` — strengthen Rule 6 ("Every value is structured")

Rule 6 already says *"As the schema grows, strings collapse
into typed records."* Add an equivalent for repeated names:
*"As the schema grows, repeated category words collapse into
typed parent enums."* Same shape; same underlying principle —
strings and repeated category words are both transitional
placeholders for structure not yet pulled out.

## 6 · Implementation consequences

These are real contracts on `main` that should churn. None
blocking, but worth tracking:

- **`signal-repository-ledger`** — flat `*Query` and `*Listing`
  variants. The `/124` proposal still applies; the refactor
  hasn't landed. Bead-worthy or operator pickup.
- **`signal-persona-spirit`** — operator's rename list (this
  turn) addresses the redundant `Intent*` prefix problem. After
  that lands, the spirit contract has `*Observation`,
  `*Subscription`, `*Pending` siblings — fewer of them, but
  worth a second pass to see if the same parent-extraction is
  warranted (e.g., do `RecordObservation` and `PsycheStateObservation`
  belong under a `Match` payload like `Observation`? Probably
  not because they're across different relations within the
  same channel; but worth thinking about).
- **Other signal-persona-* contracts** — I have not audited.
  Once the discipline surfaces are updated, an audit pass is
  warranted; could be a designer-side bead.

## 7 · Questions for psyche

Two open questions surfaced by this investigation:

### Q1 · Skill-edit landing

The three proposed skill edits in §5 are ready to write. Want
me to land them now, or do you want to review the proposed
wording first? My lean: land them — they're tight extensions
of existing rules and the substance is settled by the intent
records captured this turn.

### Q2 · Refactor sequencing for signal-repository-ledger

`/124` proposed the refactor and it never landed. Now that
the rule will be in the skills, the refactor becomes a
straightforward operator pickup. Should this become a bead
under operator pickup now, or wait until the skill edits land
first so the operator has the canonical rule to reference?

## 8 · References

- `intent/naming.nota` — 9 records as of 2026-05-19T18:55Z;
  including the recovered "Query is its own logic plane"
  record.
- `reports/designer-assistant/123-naming-guidance-redundant-domain-prefixes.md`
  — the prior naming-rule landing for redundant prefixes.
- `reports/designer-assistant/124-query-suffix-as-missing-schema-layer.md`
  — the prior analysis of the `*Query` suffix problem; the
  source of the recovered intent.
- `/git/github.com/LiGoldragon/signal-repository-ledger/src/lib.rs`
  — the live contract with the flat `*Query` shape.
- `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs`
  — the contract with the elaborate `Intent*` prefixes the
  operator is about to fix.
- `skills/naming.md` — the rule home; current pair-of-rules
  structure ready to extend.
- `skills/contract-repo.md` — the contract-specific naming
  guidance; currently mentions namespace prefix but not the
  repeated-category-sibling pattern.
- `skills/language-design.md` — the upstream principle store;
  Rule 6 ("Every value is structured") is the deepest
  framing.
- `signal-core/src/request.rs` — the 6-verb spine that agents
  ARE using correctly.
