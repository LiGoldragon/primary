# Naming Guidance — Redundant Domain Prefixes

## Finding

The psyche's correction agrees with the existing guidance.

`skills/naming.md` already had the general rule: a type belongs to
its module/crate context, and repeating the crate name in the type
name is redundant ceremony. `skills/contract-repo.md` also already
said not to repeat namespace supplied by the crate, module, or
enclosing enum, and its mistake table already had a namespace-prefix
row.

The guidance was directionally correct, but not sharp enough for
the exact failure that just happened in `signal-repository-ledger`.
It named crate-prefix repetition, but it did not explicitly call out
contract-domain repetition across payload records and request
variants. That left enough room for an agent to justify names like
`RepositoryPushObservation` and `RepositoryChangedFileQuery` as
"consistent with the contract style," even though the crate and
channel already provide the repository-ledger context.

## Skill Edits Landed

Updated `skills/naming.md`:

- broadened "prefixing type names with the crate name" into
  "prefixing names with their namespace or domain";
- explicitly says crate, module, contract, channel, enclosing enum,
  and owning component are namespaces;
- adds wrong/right contract examples:
  `RepositoryPushObservation` -> `PushObservation`,
  `RepositoryChangedFileQuery` -> `ChangedFileQuery`;
- makes the discriminator: keep descriptive leading words, drop
  leading words that only name a namespace already visible at the
  use site.

Updated `skills/contract-repo.md`:

- strengthens the namespace rule from style guidance into a hard
  naming rule;
- explicitly names `signal-repository-ledger` payloads as the worked
  example;
- updates the common-mistakes table with
  `RepositoryChangedFileQuery` inside `signal-repository-ledger`.

## Consequence For Repository Ledger

The current repository-ledger contract names are wrong under the
tightened rule. The next implementation pass should rename the
ordinary contract payloads and replies before more components depend
on them.

Preferred shape:

```rust
ReceiveHookNotification
PushObservation
CommitObservation
FileChange
RecentRepositoriesQuery
RecentRepositoriesListing
RecentRepository
ChangedFileQuery
ChangedFileListing
ChangedFile
CommitMessageQuery
CommitListing
Commit
EventQuery
EventListing
Event
EventRecorded
CatalogQuery
CatalogListing
Registration
DaemonConfiguration
```

Root/channel names can still carry the component boundary when they
are exported from the crate, but even there the better long-term
shape is likely `Request`, `Reply`, `Frame`, and `RequestBuilder`
inside the crate, with aliases only if downstream ergonomics require
them.
