# Query Suffix As Missing Schema Layer

## Verdict

The psyche's critique is right. The repository-ledger rename pass fixed one
class of bad names — redundant ancestry prefixes such as
`RepositoryPushObservation` — but it left another class visible:

```text
EventQuery
RecentRepositoriesQuery
ChangedFileQuery
CommitMessageQuery
CatalogQuery
```

The repeated `Query` suffix is a schema smell. It means the type names are
carrying a logic plane that should probably be represented as a separate typed
layer.

The correct conceptual shape is:

```text
SignalVerb::Match
  -> repository-ledger Query
       -> RecentRepositories / ChangedFiles / CommitMessages / Events / Catalog
```

`Query` is not a seventh Signal verb. The Signal verb is still `Match`.
`Query` is a domain read-plan family inside the repository-ledger contract.

## What The Current Guidance Already Says

`ESSENCE.md` gives the upstream rule:

- names do not carry their full ancestry;
- surrounding namespace supplies context;
- ugliness is diagnostic evidence that the structure is missing.

`skills/naming.md` now says not to repeat namespace supplied by crate, module,
contract, channel, enclosing enum, or owning component.

That rule caught `RepositoryChangedFileQuery` inside
`signal-repository-ledger`, because `Repository` was just restating the
contract domain.

But the current guidance is weaker on a second pattern:

> When several sibling type names repeat the same prefix or suffix, that
> repeated word may not be a name at all. It may be a missing schema layer.

The repository-ledger `*Query` names are the live example.

## Why The Current Shape Is Wrong

Current contract excerpt:

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
    }
}
```

Every read-side request says `Match` and then repeats `Query` in the payload
variant. That duplicates the read plane in the payload names.

The name has three layers collapsed into one identifier:

```text
RecentRepositoriesQuery
recentness + repository target + query relation
```

The `query relation` part should not be a suffix repeated across every sibling.
It should become the parent enum. Then the inner variants can name the actual
read target.

## Better Contract Shape

Recommended next shape:

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

The exact inner noun names can still improve, but this is already structurally
better:

- `Match` carries the Signal root verb.
- `Query` names the repository-ledger read-plan family.
- `RecentRepositories`, `ChangedFiles`, `CommitMessages`, `Events`, and
  `Catalog` name the concrete read targets.
- The request root has fewer sibling variants because the read relation is no
  longer smeared across all variant names.

Current human-side CLI shape:

```nota
(RecentRepositoriesQuery None 5)
```

Better payload-only shape if the CLI is still doing human shorthand:

```nota
(Query (RecentRepositories None 5))
```

Better full Signal shape once the CLI accepts kernel operation NOTA directly:

```nota
(Match (Query (RecentRepositories None 5)))
```

The daemon wire must be the full Signal shape: an operation whose verb is
`Match` and whose payload is `Query(...)`. The CLI may still translate a
shorter human form, but the translated daemon frame cannot hide the verb.

## How Far To Split

The psyche also named the possible next split:

```text
query -> recent -> repositories
```

That is the right instinct, but it should be earned by repetition. Today
`RecentRepositories` is the only obvious recency-shaped read target. If future
queries add:

```text
RecentCommits
RecentReports
RecentChangedFiles
```

then `Recent` has become another repeated logic plane and should be extracted
into a filter or ordering record:

```rust
pub struct RecencyWindow {
    pub since_received_at: Option<Timestamp>,
    pub limit: QueryLimit,
}
```

Then the target-specific query can compose it instead of encoding recency in
the name.

The rule is not "split every English word immediately." The rule is: when a
word recurs across sibling names as a category marker, stop and ask whether
that word is a missing type.

## Guidance To Add

This should become a naming skill rule, adjacent to the namespace-prefix rule.

Proposed wording:

> Repeated category words in sibling names are schema smells. If several
> adjacent types or variants share the same prefix or suffix — `*Query`,
> `*Command`, `*Event`, `*Request`, `*Listing` — do not merely rename them one
> by one. Ask whether the repeated word is a missing parent enum, relation,
> record, module, or contract layer. Names should not carry logic planes that
> the schema can represent directly.

Worked example:

```rust
// Smell — Query is repeated as a suffix across siblings
RecentRepositoriesQuery
ChangedFileQuery
CommitMessageQuery

// Better — Query is the parent relation; siblings name read targets
Query::RecentRepositories(RecentRepositorySelection)
Query::ChangedFiles(ChangedFileSelection)
Query::CommitMessages(CommitMessageSelection)
```

This belongs in `skills/naming.md`. `skills/contract-repo.md` should also carry
the contract-specific version: root request variants should name mutually
exclusive ways a relation moves; if several variants share the same category
word, that category probably deserves a root family.

## Implementation Consequence

The repository-ledger contract should break again. Backward compatibility is
not a constraint here, and this is exactly the kind of early contract churn the
workspace should accept while the shape is still being found.

Implementation order:

1. In `signal-repository-ledger`, add `Query` and `QueryResult` enums.
2. Replace the five `Match *Query(...)` request variants with one
   `Match Query(Query)` variant.
3. Replace the read reply variants with one `QueryResult(QueryResult)` reply
   variant, unless the reply side has a strong reason to keep result variants
   at root level.
4. Update `repository-ledger` dispatch to match on `Request::Query(query)` and
   then dispatch inside `Query`.
5. Update CLI examples and live hook/query tests from `*Query` heads to the new
   `Query (...)` head.
6. Keep `PushObservation` and `ReceiveHookNotification` as direct `Assert`
   variants; they are not part of the read-plan family.

## Open Question

One design question remains for the psyche:

Should the repository-ledger CLI accept only full Signal operation NOTA such as
`(Match (Query (RecentRepositories None 5)))`, or may it accept a shorter
human-facing shorthand such as `(Query (RecentRepositories None 5))` and wrap
that into `Match` internally?

The daemon wire should be full Signal either way. The question is only about
the CLI's human/agent text surface.
