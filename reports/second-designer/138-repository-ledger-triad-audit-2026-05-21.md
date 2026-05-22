# 138 — repository-ledger triad audit

*Audit of the repository-ledger triad: `signal-repository-ledger`
(working contract) + `owner-signal-repository-ledger` (policy
contract) + `repository-ledger` (runtime, daemon + thin CLI).
Spirit landed as the canonical persona pilot per
`intent/signal.nota` 2026-05-20T17:10:00Z; ledger has been
sequenced as the simpler alternate pilot. The working contract is
partly current; the runtime crate and the policy contract are
stale, and the runtime is structurally inconsistent with the
contract it imports.*

## 0 · TL;DR

The triad is roughly **one-third migrated**. The working contract
`signal-repository-ledger/src/lib.rs` has been brought up to the
new contract-local-verb shape (`operation Receive(...)`,
`operation Observe(...)`, `operation Query(Query)`) and has
already lifted `QueryResult` per `intent/signal.nota`
2026-05-20T00:07:55+02:00. The owner contract still imports
`signal_core::signal_channel` and uses the old universal-verb
shape (`Mutate Registration(...)`, `Retract Retirement(...)`,
`Mutate SpoolDirectoryPolicy(...)`, `Mutate MirrorPolicy(...)`).
The runtime crate still imports `signal_core` symbols
(`NonEmpty`, `Reply as CoreReply`, `RequestRejectionReason`,
`SubReply`, `ExchangeFrameBody`, `FrameError`) and references
ledger types that no longer exist in the migrated working
contract (`EventQuery`, `RecentRepositoriesQuery`,
`ChangedFileQuery`, `CommitMessageQuery`, `CatalogQuery`,
`LedgerRequest::EventQuery`, `LedgerReply::EventListing`,
`LedgerReply::RecentRepositoriesListing`, etc.). The runtime
therefore does not compile against the present contract — the
working-contract migration is half-done at the source level only.

State summary:

- `signal-repository-ledger`: contract-local verbs ✓, `Query`/
  `QueryResult` lift ✓; **but still has the 5-line frame alias
  re-export dance** (`pub type Frame = LedgerFrame; ...`),
  `RequestUnimplemented` carries both `operation` and `query`
  fields, no `observable` block, `Timestamp(String)` is a stringly
  field with no typed shape, and `OperationKind`/`QueryKind` are
  hand-maintained.
- `owner-signal-repository-ledger`: **still on `signal-core`**,
  uses retired universal-verb shape (`Mutate`/`Retract`), 5-line
  alias dance, `RequestUnimplemented { operation, reason }`
  redundancy, `OperationKind` hand-maintained, hand-written
  `operation_kind()` match, no observable block (but owner channels
  generally do not need one — see §3 below).
- `repository-ledger` runtime: imports `signal-core` directly,
  uses retired pre-executor frame plumbing
  (`ExchangeFrameBody`/`CoreReply`/`SubReply` open coded), does
  not depend on `signal-executor`, does not use `Lowering`,
  `OperationPlan`, `BatchPlan`, `CommandExecutor`, or
  `ObserverChannel`, has no `ToSemaOperation` /
  `ToSemaOutcome` projections, and references stale contract type
  names that the migrated working contract has already renamed
  away. The daemon also has no `bootstrap-policy.nota` file and
  no first-start bootstrap step.

**Priority for the triad's next slice**: bring the runtime crate
back into compile with the migrated working contract (fix imports
and stale type names), execute the `owner-signal-repository-ledger`
verb-shape migration, drop the redundant `operation`/`query`
fields from both `RequestUnimplemented` records, retire the alias
dance per `intent/component-shape.nota` 2026-05-21T10:30:00Z
(modules-not-options principle once `signal-frame`'s prefix-drop
work lands), then migrate the daemon onto `signal-executor`.
Ledger remains a useful simpler external pilot for the canonical
triad daemon shape, after the working contract pilot is finished.

## 1 · /257 findings status

### /257 §1.1 — Old universal-verb shape on operations

**Status: WORKING CONTRACT FIXED; OWNER CONTRACT STALE.**

`signal-repository-ledger/src/lib.rs:479-490` declares the new
shape:

```rust
signal_channel! {
    channel Ledger {
        operation Receive(ReceiveHookNotification),
        operation Observe(PushObservation),
        operation Query(Query),
    }
    reply Reply {
        EventRecorded(EventRecorded),
        QueryResult(QueryResult),
        RequestUnimplemented(RequestUnimplemented),
    }
}
```

`owner-signal-repository-ledger/src/lib.rs:86-102` still uses the
retired prefix shape:

```rust
signal_channel! {
    channel Owner {
        request Request {
            Mutate Registration(Registration),
            Retract Retirement(Retirement),
            Mutate SpoolDirectoryPolicy(SpoolDirectoryPolicy),
            Mutate MirrorPolicy(MirrorPolicy),
        }
        reply Reply { ... }
    }
}
```

That is the pre-2026-05-19T19:45 universal-verb shape, with the
`request Request { ... }` outer block also from the old grammar.
Required rewrite: drop the `Mutate`/`Retract` prefixes, drop the
outer `request Request { ... }` wrapper, and use contract-local
verbs (`operation Register(Registration)`,
`operation Retire(Retirement)`, etc. — see §3).

### /257 §1.2 — Doubling smell

**Status: ONE INSTANCE PRESENT IN THE WORKING CONTRACT.**

`operation Query(Query)` at
`signal-repository-ledger/src/lib.rs:483` — the verb is `Query`
and the payload is `Query`. Per the verb/noun-homograph
clarification in `intent/component-shape.nota`
2026-05-19T21:15:00Z, positional context disambiguates: the
operation-root position implies a verb, the payload position
implies a noun. This is acceptable. The `Match Query(Query)` form
that psyche flagged in `intent/component-shape.nota`
2026-05-19T19:30 was wrong because the leading word was a Sema
classification used as a public-contract verb prefix; the bare
`operation Query(Query)` is the right replacement and is what
landed here.

### /257 §1.3 — `Mutate <Verb>` grammatically wrong

**Status: OWNER CONTRACT HAS THE WRONG SHAPE FOR THIS REASON
AS WELL.**

`Mutate Registration(Registration)` reads as "mutate a
registration"; that is borderline (Registration is a noun). But
`Retract Retirement(Retirement)` is incoherent for the same
reason psyche flagged in `intent/component-shape.nota`
2026-05-19T19:30 — Retirement is a verb-form noun. The fix is the
same as §1.1: drop the universal-verb prefix entirely and pick a
contract-local verb. Suggested:

- `operation Register(Registration)` ← peer registers a
  repository under owner authority.
- `operation Retire(Retirement)` ← peer retires a registration.
- `operation SetSpoolDirectory(SpoolDirectoryPolicy)`.
- `operation SetMirror(MirrorPolicy)`.

See §3 for the full owner-contract restatement.

### /257 §1.4 — Repeated-suffix smell

**Status: WORKING CONTRACT LIFTED; OWNER CONTRACT HAS TWO
SIBLINGS WITH THE SAME PATTERN BUT TOO SMALL TO LIFT.**

The working contract lifted `QueryResult` per `intent/signal.nota`
2026-05-20T00:07:55+02:00:

```rust
pub enum QueryResult {
    Events(EventListing),
    RecentRepositories(RecentRepositoriesListing),
    ChangedFiles(ChangedFileListing),
    Commits(CommitListing),
    Catalog(CatalogListing),
}
```

That is the canonical shape from the lift correction.

The owner reply variants `SpoolDirectoryPolicySet(...)` and
`MirrorPolicySet(...)` share the `*Set` suffix. Two siblings is
under the "third sibling, stop and ask" threshold from
`skills/naming.md` §"Anti-pattern: repeated category words"; if
the owner gains a third "Set"-shaped reply it should lift. For
now the explicit names read cleanly.

### /257 §1.5 — Ancestry-prefixed type names

**Status: WORKING CONTRACT MOSTLY CLEAN; ONE BORDERLINE.**

The working contract is clean — `Name`, `GitoliteUser`,
`ObjectIdentifier`, `RefName`, `Timestamp`, `CommitMessage`,
`FilePath`, `FileStatus`, `TextSearch`, `EventSequence`,
`QueryLimit`, `FilesystemPath`, `SocketMode`, `Class`,
`RefUpdate`, `ReceiveHookNotification`, `FileChange`,
`CommitObservation`, `PushObservation`, `Registration`, `Event`,
`EventRecorded`, `Events`, `EventListing`, `RecentRepositories`,
`RecentRepository`, `RecentRepositoriesListing`, `ChangedFiles`,
`ChangedFile`, `ChangedFileListing`, `CommitMessages`, `Commit`,
`CommitListing`, `Catalog`, `CatalogListing`, `Query`,
`QueryResult`, `DaemonConfiguration`, `OperationKind`,
`QueryKind`, `UnimplementedReason`, `RequestUnimplemented`. The
crate name `signal-repository-ledger` supplies the
"repository-ledger" domain; none of the types restate it. ✓

The one borderline: `ReceiveHookNotification`
(`signal-repository-ledger/src/lib.rs:252`). "Receive" is the
ordinary operation that consumes this record. "HookNotification"
is the descriptive part. Either the record is `HookNotification`
(payload of `operation Receive(...)`) or it stays the current
five-word compound. Designer lean: rename to `HookNotification`
— the contract is already about the Gitolite hook surface, and
the variant carries the action label.

The owner contract has no ancestry-prefix smells: `MirrorTarget`,
`Retirement`, `SpoolDirectoryPolicy`, `MirrorPolicy`,
`Registered`, `Retired`, `SpoolDirectoryPolicySet`,
`MirrorPolicySet`, `OperationKind`, `UnimplementedReason`,
`RequestUnimplemented`. ✓

### /257 §1.6 — `*RequestUnimplemented { operation, reason }`

**Status: PRESENT IN BOTH CONTRACTS, AGGRAVATED IN THE WORKING
CONTRACT.**

Working contract
`signal-repository-ledger/src/lib.rs:472-477`:

```rust
pub struct RequestUnimplemented {
    pub operation: OperationKind,
    pub query: Option<QueryKind>,
    pub reason: UnimplementedReason,
}
```

Two redundant fields. `operation` restates the operation position
the reply is paired with; `query` further restates which inner
`Query` variant produced the failure, which is also recoverable
from the original request. Fix: collapse to
`pub struct RequestUnimplemented { pub reason: UnimplementedReason }`,
matching the spirit fix.

The `query: Option<QueryKind>` field is the more interesting
smell: it exists because the contract author wanted to preserve
which inner `Query` variant failed when the unimplemented reason
applies to a `Query` operation, but the inner variant is already
in the operation payload that the caller sent. The two-layer
identification (operation + inner query) is the missing-schema-
layer pattern from `skills/naming.md` §"Anti-pattern: repeated
category words" reading downward: the reply doesn't need to
re-identify what the request positionally said.

Owner contract `owner-signal-repository-ledger/src/lib.rs:80-84`:

```rust
pub struct RequestUnimplemented {
    pub operation: OperationKind,
    pub reason: UnimplementedReason,
}
```

Same smell. Drop `operation`; keep `reason`. After the owner-
contract verb migration (§3), the `OperationKind` enum can also
retire — once the macro generates `OperationKind`, hand-
maintenance disappears.

### /257 §1.7 — Empty marker records

**Status: ONE INSTANCE IN THE WORKING CONTRACT.**

`signal-repository-ledger/src/lib.rs:381-382`:

```rust
pub struct Catalog;
```

The `Catalog` query has no payload. Today it sits inside
`Query::Catalog(Catalog)` as a unit-struct variant. With mixed-
enum support per `intent/persona.nota` 2026-05-20T20:00:00Z (no-
op as explicit command rule and mixed-enum-variant support), the
right shape is:

```rust
pub enum Query {
    Events(Events),
    RecentRepositories(RecentRepositories),
    ChangedFiles(ChangedFiles),
    CommitMessages(CommitMessages),
    Catalog,                  // unit variant, no Catalog struct
}
```

Drop the `pub struct Catalog;` and let `Query::Catalog` be a unit
variant. This is the spirit `Observation::State` shape recovery.

### /257 §1.9 — Frame type alias boilerplate

**Status: PRESENT IN BOTH CONTRACTS.**

Working contract `signal-repository-ledger/src/lib.rs:492-497`:

```rust
pub type Frame = LedgerFrame;
pub type FrameBody = LedgerFrameBody;
pub type ChannelRequest = LedgerChannelRequest;
pub type ChannelReply = LedgerChannelReply;
pub type RequestBuilder = LedgerRequestBuilder;
pub type Request = LedgerOperation;
```

Six aliases — including `pub type Request = LedgerOperation;`
which is doubly aliased (the macro already emits
`LedgerOperation`, the contract author renames it `Request` for
external use). The whole dance disappears when the macro emits
unprefixed names by default per `intent/component-shape.nota`
2026-05-21T10:30:00Z (modules-not-options).

Owner contract has the same five-line block
(`owner-signal-repository-ledger/src/lib.rs:104-108`).

This is the workspace-wide `primary-77hh` mechanical concern; the
fix lands at the `signal-frame` macro level, then ledger drops
both blocks.

### /257 §1.10 — No observable block

**Status: NOT FIXED IN THE WORKING CONTRACT.**

Ledger is not a persona component per the strict
`intent/persona.nota` 2026-05-20T02:00:00Z mandate (which scopes
Tap/Untap to persona components only — repository-ledger is a
workspace-infrastructure component that lives outside the persona
authority chain). Designer reading: the observable block is
**not** mandatory here. Repository-ledger does not need the
debug-the-debugger meta-introspection surface that
`intent/persona.nota` 2026-05-21T10:00:00Z established for
persona-introspect.

However, the operator/150 §5.2 framing of "no observable block"
as a smell is correct in the sense that a daemon that participates
in the workspace's cross-component observation story benefits from
a uniform observer surface even when persona-introspect is not its
intended consumer. The pragmatic question is whether ledger
exposes activity that some future workspace tool needs to
subscribe to: repository pushes, commit-message activity, file-
change activity. The current consumer story is agent discovery
queries (one-shot Match through `Query`), not subscription, so
the observable block is deferred for the same reason spirit
deferred fanout per `intent/persona.nota` 2026-05-20T20:00:00Z
("Tap/Untap fanout is not required before the spirit substrate
replacement").

**Recommendation**: do not add an `observable` block to ledger
now. When persona-introspect lands and the workspace has a
universal observer story, revisit. Until then, the ledger's
absence is intentional, not a gap.

### /257 §1.11 — Single-field timestamps (and excess precision)

**Status: WRONG SHAPE — STRING TIMESTAMPS, NOT TYPED.**

`signal-repository-ledger/src/lib.rs:70-83`:

```rust
pub struct Timestamp(String);
```

`Timestamp` is a `String` wrapper. The runtime uses it for
both received-at and commit-timestamp fields and compares as
string slices (`signal-repository-ledger/src/lib.rs:344,
361, 372, 416-418, 449-453, 506-513`). The
`ARCHITECTURE.md` calls this out: *"Time-window queries
compare received-at timestamps in their canonical
UTC-sortable string form. This is acceptable while the
contract still uses `Timestamp(String)` and should collapse
into native timestamp comparison when the workspace
timestamp type lands."*

The intent-record two-field timestamp Decision in
`intent/workspace.nota` 2026-05-19 18:30 explicitly scopes to
intent records; runtime/protocol timestamps elsewhere have not
been settled. The cross-workspace question raised in /257 §1.12
remains open. Designer lean for ledger: align with whatever
`signal-persona`'s `TimestampNanos` lowers to once the workspace-
wide timestamp settles (likely `seconds-since-epoch u64` or
`Timestamp { date, time }` matching the intent-record shape).
The string form is provisional.

This is independent of the rest of the migration. Don't block
the verb-shape work on the timestamp settlement.

### /257 §1.13 — `supervision::` namespace stale

Not applicable to ledger.

## 2 · New findings specific to this triad

### 2.1 — Runtime crate references type names the contract has retired

`repository-ledger/src/lib.rs:28-35` imports:

```rust
use signal_repository_ledger::{
    CatalogListing, ChangedFile, ChangedFileListing, ChangedFileQuery, ChannelReply,
    ChannelRequest, Commit, CommitListing, CommitMessageQuery, CommitObservation, Event,
    EventListing, EventQuery, EventRecorded, EventSequence, Name, PushObservation, QueryLimit,
    ReceiveHookNotification, RecentRepositoriesListing, RecentRepositoriesQuery, RecentRepository,
    Registration, Reply as LedgerReply, Request as LedgerRequest, RequestUnimplemented, Timestamp,
};
```

The names `ChangedFileQuery`, `CommitMessageQuery`, `EventQuery`,
`RecentRepositoriesQuery`, `CatalogQuery` (in `tests/store.rs:13`)
**do not exist in the migrated working contract**. The contract
now declares `Events`, `ChangedFiles`, `CommitMessages`,
`RecentRepositories`, `Catalog` as the typed query payloads, all
under the lifted `Query` enum. Likewise
`LedgerRequest::EventQuery(...)`, `LedgerRequest::ChangedFileQuery(...)`,
`LedgerRequest::CommitMessageQuery(...)`,
`LedgerRequest::RecentRepositoriesQuery(...)`,
`LedgerRequest::CatalogQuery(...)` (`src/lib.rs:585-602`) no
longer match — those variants do not exist; the operation root is
now `Query(Query)` with the inner enum variants.
`LedgerReply::EventListing`, `LedgerReply::RecentRepositoriesListing`,
`LedgerReply::ChangedFileListing`, `LedgerReply::CommitListing`,
`LedgerReply::CatalogListing` (`src/lib.rs:579-602`) likewise no
longer exist — the contract collapsed them into `QueryResult`
with inner variants.

This means the runtime crate **does not compile against the
present working contract**. Either the contract was migrated in
isolation, or the runtime is held by an older Cargo.lock
pinning. Either way the migration is half-finished at the source
level. The first migration slice for ledger has to land a
matching runtime adjustment before any further work.

The required runtime changes:

- `LedgerRequest::EventQuery(query)` →
  `LedgerRequest::Query(Query::Events(events))`.
- `LedgerRequest::RecentRepositoriesQuery(query)` →
  `LedgerRequest::Query(Query::RecentRepositories(query))`.
- `LedgerRequest::ChangedFileQuery(query)` →
  `LedgerRequest::Query(Query::ChangedFiles(query))`.
- `LedgerRequest::CommitMessageQuery(query)` →
  `LedgerRequest::Query(Query::CommitMessages(query))`.
- `LedgerRequest::CatalogQuery(query)` →
  `LedgerRequest::Query(Query::Catalog(catalog))` (or
  `Query::Catalog` once the unit-variant shape lands per §1.7).
- `LedgerReply::EventListing(listing)` →
  `LedgerReply::QueryResult(QueryResult::Events(listing))`.
- `LedgerReply::RecentRepositoriesListing(listing)` →
  `LedgerReply::QueryResult(QueryResult::RecentRepositories(listing))`.
- `LedgerReply::ChangedFileListing(listing)` →
  `LedgerReply::QueryResult(QueryResult::ChangedFiles(listing))`.
- `LedgerReply::CommitListing(listing)` →
  `LedgerReply::QueryResult(QueryResult::Commits(listing))`.
- `LedgerReply::CatalogListing(listing)` →
  `LedgerReply::QueryResult(QueryResult::Catalog(listing))`.

The query payload parameter types also change:
`EventQuery` → `Events`, `RecentRepositoriesQuery` →
`RecentRepositories`, `ChangedFileQuery` → `ChangedFiles`,
`CommitMessageQuery` → `CommitMessages`. The store methods
`repository_events`, `recent_repositories`, `changed_files`,
`commit_messages` keep their interfaces; only the imported
type names change.

### 2.2 — Runtime imports `signal_core`, contract imports `signal_frame`

`repository-ledger/src/lib.rs:25-27`:

```rust
use signal_core::{
    NonEmpty, OperationFailureReason, Reply as CoreReply, RequestRejectionReason, SubReply,
};
```

`repository-ledger/src/client.rs:7-10`:

```rust
use signal_core::{
    ExchangeFrameBody, ExchangeIdentifier, ExchangeLane, HandshakeReply, HandshakeRequest,
    LaneSequence, Reply as CoreReply, RequestPayload, SessionEpoch, SubReply,
};
```

`repository-ledger/src/frame_io.rs:3` and `daemon.rs:9` likewise.
`Cargo.toml:30` depends on `signal-core` directly. The working
contract has moved to `signal-frame` (`Cargo.toml:18`); the
runtime has not followed. `signal-core` is the retired crate per
`intent/component-shape.nota` 2026-05-19T20:00:00Z (`signal-core`
is renamed to `signal-frame`); the new repo is the source of
truth.

The owner contract is the worst offender here: it declares
`use signal_core::signal_channel;` at line 5 — directly using
the retired crate's macro, not the new one.

### 2.3 — Runtime does not use `signal-executor`

`repository-ledger/src/lib.rs:519-575` open-codes the request
dispatch:

```rust
pub fn handle_ordinary_request(&self, request: ChannelRequest) -> ChannelReply {
    let checked = match request.into_checked() {
        Ok(checked) => checked,
        Err((reason, _request)) => return CoreReply::rejected(reason),
    };
    if checked.operations.len() != 1 {
        return CoreReply::rejected(RequestRejectionReason::Internal);
    }
    let operation = checked.operations.into_head();
    let verb = operation.verb;
    let operation_kind = operation.payload.operation_kind();
    match self.execute_ordinary_payload(operation.payload) {
        Ok(payload) => CoreReply::completed(NonEmpty::single(SubReply::Ok { verb, payload })),
        Err(error) => CoreReply::aborted(
            0,
            OperationFailureReason::DomainRejection,
            NonEmpty::single(SubReply::Failed { ... }),
        ),
    }
}
```

This is the pre-`signal-executor` shape: the daemon walks the
`ChannelRequest`, picks the single operation by hand, maps to a
reply by hand, builds the `SubReply::Ok`/`Failed` wrappers
manually. The same pattern is in `handle_owner_request`
(`src/lib.rs:548-575`). None of `Lowering`, `OperationPlan`,
`BatchPlan`, `CommandExecutor`, `ObserverChannel`,
`AcceptedOutcome::OperationAborted/BatchAborted`, or
`BatchErrorClassification` is used. The daemon does not have a
local `Command` enum (it operates directly on contract
`Operation` payloads), does not have a local `Effect` enum, has
no `ToSemaOperation` projection, no `ToSemaOutcome` projection.

Spirit's migrated shape (operator/150 §5.1) is the template. The
ledger migration needs to define:

- `repository_ledger::Command` enum carrying the daemon's typed
  executable shape (`RecordHookNotification`,
  `RecordPushObservation`, `ReadEvents`, `ReadRecentRepositories`,
  `ReadChangedFiles`, `ReadCommitMessages`, `ReadCatalog`,
  `Register`, `Retire`, `SetSpoolDirectory`, `SetMirror`).
- `repository_ledger::Effect` enum (`EventAsserted`,
  `RegistrationMutated`, `RegistrationRetracted`,
  `EventListed`, etc.) carrying the typed outcome.
- `impl ToSemaOperation for Command` — Receive/Observe →
  `Assert`, Query family → `Match`, Register/SetSpoolDirectory/
  SetMirror → `Mutate`, Retire → `Retract`.
- `impl ToSemaOutcome for Effect` — variant-by-variant
  classification to the `SemaOutcome` enum.
- `impl Lowering for LedgerLowering` translating
  `LedgerOperation` to `OperationPlan<Command>`.
- `impl CommandExecutor for LedgerCommandExecutor` wrapping the
  current `Store` methods.
- `impl Lowering for OwnerLedgerLowering` (or shared) for the
  owner contract.

### 2.4 — Receive / Observe / Query as contract-local verbs

The three operation roots are `Receive(ReceiveHookNotification)`,
`Observe(PushObservation)`, and `Query(Query)`. They read as
contract-local verbs that match the action the caller is taking.

`Receive` reads slightly oddly because the receiver is the
daemon, not the verb's grammatical subject — the caller is
*notifying the daemon that a hook receive happened*. The verb
encodes the upstream event ("a receive happened in Gitolite"),
not the local action. Two alternative shapings:

- `operation Notify(ReceiveHookNotification)` — caller notifies
  the daemon of a hook event. Verb is the action the caller
  takes; the receiver-side semantics are clear.
- `operation Record(ReceiveHookNotification)` — caller asks the
  daemon to record this notification.

Both read more cleanly. Spirit uses `operation Record(Entry)`
for the equivalent capture path (per /256). For consistency
with the persona-spirit pilot, `operation Record(...)` reads
best. Designer lean: rename `Receive` → `Record`. The
`Observe` operation should likely follow the same rename if a
single typed capture operation is wanted, but the two operations
carry semantically different payloads (`ReceiveHookNotification`
is the bare hook event; `PushObservation` is the richer
post-push observation). A typed capture sum is the natural
lift:

```rust
operation Record(Capture),

pub enum Capture {
    HookNotification(ReceiveHookNotification),
    PushObservation(PushObservation),
}
```

This collapses two operation roots to one, with the typed
payload sum distinguishing what was captured. Same shape as
`Query`/`QueryResult`. Designer lean: lift to a single
`Record(Capture)` operation; psyche confirms.

The `Query` operation root reads cleanly as the verb-action
"query for something" with the `Query` enum naming the inner
variant. ✓

`Observe` as a standalone operation is therefore not the right
shape today; either it stays (and `Receive` renames) or it
collapses into the lifted `Record(Capture)` form.

### 2.5 — `QueryResult` lift correctness

`signal-repository-ledger/src/lib.rs:410-417`:

```rust
pub enum QueryResult {
    Events(EventListing),
    RecentRepositories(RecentRepositoriesListing),
    ChangedFiles(ChangedFileListing),
    Commits(CommitListing),
    Catalog(CatalogListing),
}
```

Note the asymmetry: `Query::Catalog(Catalog)` →
`QueryResult::Catalog(CatalogListing)`. The query variant is
named `Catalog` (the empty marker; or unit variant after §1.7);
the result variant is also named `Catalog` but carries
`CatalogListing`. The pairing reads correctly.

`Query::CommitMessages(CommitMessages)` →
`QueryResult::Commits(CommitListing)`. The variant name changed
from `CommitMessages` (query side) to `Commits` (result side).
That's an inconsistency — the variant name should match across
the request/result pair so the reader can mentally line them up.
The result side is the cleaner name; rename the query side:
`Query::CommitMessages` → `Query::Commits` (and rename
`CommitMessages` payload struct → `CommitsQuery` or similar).
Or rename the result side back to `CommitMessages`. Designer
lean: pick `Commits` everywhere — the query is "find commits
matching a message substring," the variant is best named after
what the query targets (commits), not the filter it uses
(message contents). The filter (`message_contains`) is already a
field of the payload.

The `kind()` impls at `src/lib.rs:398-407` and `419-429` have a
matching asymmetry — `QueryResult::Commits(_) => QueryKind::CommitMessages`
on the result side does the inverse mapping. Either rename the
`QueryKind::CommitMessages` variant to `QueryKind::Commits` or
keep the asymmetry intentional. The `QueryKind` enum is
hand-maintained today; per `intent/component-shape.nota`
2026-05-21T01:15:44+02:00 it should be macro-generated from the
`Query` enum's variants, which forces consistency naturally.

The lift itself (typed sum on both sides of the request/reply
boundary, symmetric `Query`/`QueryResult` shape) is correct.

### 2.6 — `QueryKind`, `OperationKind`, hand-written `operation_kind()`

`signal-repository-ledger/src/lib.rs:443-461`:

```rust
pub enum OperationKind { Receive, Observe, Query }
pub enum QueryKind { Events, RecentRepositories, ChangedFiles, CommitMessages, Catalog }
```

`signal-repository-ledger/src/lib.rs:499-507`:

```rust
impl LedgerOperation {
    pub fn operation_kind(&self) -> OperationKind {
        match self {
            Self::Receive(_) => OperationKind::Receive,
            Self::Observe(_) => OperationKind::Observe,
            Self::Query(_) => OperationKind::Query,
        }
    }
}
```

Both `OperationKind` enums (working and owner) and `QueryKind`
are derivable from the `Operation`/`Query` enum variants; the
two `operation_kind()` impls are mechanical projections.
Per `intent/component-shape.nota` 2026-05-21T01:15:44+02:00, the
macro should generate these. Until that lands, they are
hand-maintenance debt that goes stale on every variant addition.

### 2.7 — Owner contract still uses `request Request { ... }` outer block

`owner-signal-repository-ledger/src/lib.rs:86-102`:

```rust
signal_channel! {
    channel Owner {
        request Request {
            Mutate Registration(Registration),
            ...
        }
        reply Reply { ... }
    }
}
```

The new grammar (per `signal-frame` macros, used in the working
contract) drops the outer `request Request { ... }` wrapper:
operations live at the top level under `channel`, replies live
under `reply` directly. The owner contract is on the older macro
syntax — which is consistent with its `use signal_core::signal_channel`
import. Migration to the new grammar happens with the
`signal-core` → `signal-frame` switch.

### 2.8 — `pub use signal_repository_ledger::{FilesystemPath, Name, Registration};`

`owner-signal-repository-ledger/src/lib.rs:6` re-exports three
types from the working contract. The owner contract is a sibling
to the working contract; in the workspace's component-triad
shape the two are independent contract crates that share the
same domain. Cross-contract type sharing is reasonable for
identity types (`Name`) but creates a dependency from the owner
contract to the working contract that may not be desired.

Two resolution paths:

- **Keep the dependency**. `Name` and `FilesystemPath` are
  domain identifiers; both contracts use them. The dependency
  direction (owner → working) is acceptable because the working
  contract is the more fundamental surface; the owner channel
  manages policy *about* the same domain.
- **Extract to a `signal-repository-ledger-types` crate**. As
  the workspace did for `signal-persona-auth` per /257 §1.12 —
  the universal identity types live in a small types crate, both
  contract crates depend on the types crate, no cross-contract
  dependency.

Designer lean: leave it as-is for now (the dependency is small).
If the owner contract grows other shared types, extract.

### 2.9 — Runtime references `ChannelRequest`/`ChannelReply` aliases

`repository-ledger/src/lib.rs:519`:

```rust
pub fn handle_ordinary_request(&self, request: ChannelRequest) -> ChannelReply {
```

The runtime uses the contract's `ChannelRequest`/`ChannelReply`
aliases (which alias `LedgerChannelRequest`/`LedgerChannelReply`).
Once the macro emits unprefixed names by default per
`intent/component-shape.nota` 2026-05-21T10:30:00Z, these alias
names retire. The runtime should update to whatever the cleaned
emission shape is (likely `Request`/`Reply` directly from the
macro, with the `Ledger` channel disambiguator coming from the
crate name).

### 2.10 — No bootstrap-policy.nota; no first-start bootstrap

The repository has no `bootstrap-policy.nota` file. The daemon
does not implement the first-start bootstrap step required by
`skills/component-triad.md` §5 (policy state populates from
`bootstrap-policy.nota` exactly once on first start). The
runtime opens the store and immediately begins accepting socket
traffic without any policy-state seeding step.

The triad invariant 5 (policy state and working state both in
one sema-engine DB, policy bootstrapped once from
`bootstrap-policy.nota`) is therefore not satisfied. Today's
ledger uses owner-contract `SetSpoolDirectory`/`SetMirror`
operations to populate the same state at runtime, which works
but means the daemon has no declared first-start policy and
deployment requires an out-of-band step (an owner-signal write)
to make the daemon usable.

When the persona-spirit pilot established the bootstrap pattern,
ledger inherited the requirement. Today's gap: add a
`bootstrap-policy.nota` declaring at least the default spool
directory, and a bootstrap-once code path in the daemon that
reads it on first start and writes the typed records as if they
had been `SetSpoolDirectory`-mutated.

### 2.11 — No witness tests against the five triad invariants

`/git/github.com/LiGoldragon/repository-ledger/tests/store.rs`
covers store-level behavior — recording notifications, recording
push observations, agent discovery queries through the signal
frame. The triad-invariant witnesses listed in
`skills/component-triad.md` §"Witness tests" are absent:

- No `ledger-cli-accepts-one-argument-and-prints-one-nota-reply`
  test.
- No `ledger-cli-has-exactly-one-signal-peer` test (the CLI does
  go to one daemon but no test asserts it cannot multiplex).
- No `ledger-cli-cannot-open-any-database-or-peer-socket` test.
- No `ledger-daemon-rejects-non-signal-traffic-on-its-socket` test.
- No `ledger-signal-verb-mapping-covers-every-request-variant`
  test.
- No `ledger-owner-socket-rejects-ordinary-frame` test.
- No `ledger-ordinary-socket-rejects-owner-frame` test.
- No `ledger-owner-socket-mode-matches-spawn-envelope` test.
- No `ledger-policy-tables-empty-on-first-start-trigger-bootstrap`
  test (this would fail today because there is no bootstrap step).
- No `ledger-bootstrap-runs-exactly-once` test.
- No `ledger-policy-changes-after-bootstrap-only-via-owner-signal`
  test.
- No `ledger-working-tables-never-read-bootstrap-file` test.
- No `ledger-binary-rejects-flag-style-arguments` test (the runtime
  has the `FlagArgument` error variant; an enforcement test should
  exist).

Most of these can be small constraint tests; the bootstrap-related
ones depend on §2.10 landing first.

### 2.12 — CLI does not dispatch to the owner socket

`repository-ledger/src/client.rs:30-93` is a single-socket
client: it connects to one socket path (the ordinary socket) and
sends only working-contract operations. There is no policy-socket
client surface in the CLI. Owner operations are unreachable from
the CLI.

Per `intent/signal.nota` 2026-05-20T22:27:40+02:00 and
`/129-mind-orchestrate-payload-and-cli-dispatch-option-a-2026-05-20.md`,
component CLIs use a generated `signal_cli!` dispatch macro that
takes both contract enums and routes by operation head. Ledger's
CLI has not adopted this — it has no `signal_cli!` invocation,
and the binary at `src/bin/repository-ledger.rs` reads as
`Client::run_from_environment()` which calls
`CliRequest::from_arguments` and decodes only `LedgerRequest`
(working contract). Owner operations require a different code
path that does not exist.

Migration: invoke `signal_cli!` with both
`signal_repository_ledger::LedgerOperation` and
`owner_signal_repository_ledger::OwnerOperation` as the working
and policy enums respectively. The macro generates the
compile-time dispatch table.

## 3 · Owner signal audit

`owner-signal-repository-ledger` is the more retro of the two
contracts — same authority of stale shape across the board. It
declares four operations and four reply variants.

### Current shape (stale)

```rust
signal_channel! {
    channel Owner {
        request Request {
            Mutate Registration(Registration),
            Retract Retirement(Retirement),
            Mutate SpoolDirectoryPolicy(SpoolDirectoryPolicy),
            Mutate MirrorPolicy(MirrorPolicy),
        }
        reply Reply {
            Registered(Registered),
            Retired(Retired),
            SpoolDirectoryPolicySet(SpoolDirectoryPolicySet),
            MirrorPolicySet(MirrorPolicySet),
            RequestUnimplemented(RequestUnimplemented),
        }
    }
}
```

Five smells:

- Old `signal-core` macro + `request Request { ... }` wrapper.
- Universal-verb prefixes (`Mutate`/`Retract`).
- `Mutate Registration` reads borderline (Registration is a noun);
  `Retract Retirement` is incoherent (Retirement is a verb-form
  noun).
- `RequestUnimplemented { operation, reason }` redundancy.
- 5-line alias dance.

### Target shape

```rust
use signal_frame::signal_channel;

signal_channel! {
    channel Owner {
        operation Register(Registration),
        operation Retire(Retirement),
        operation SetSpoolDirectory(SpoolDirectoryPolicy),
        operation SetMirror(MirrorPolicy),
    }
    reply Reply {
        Registered(Registered),
        Retired(Retired),
        SpoolDirectorySet(SpoolDirectorySet),
        MirrorSet(MirrorSet),
        RequestUnimplemented(RequestUnimplemented),
    }
}

pub struct RequestUnimplemented {
    pub reason: UnimplementedReason,
}
```

Notes:

- Verbs are contract-local actions: `Register`, `Retire`,
  `SetSpoolDirectory`, `SetMirror`.
- Reply variants drop the `Policy*Set` suffix (the contract is
  about policy; "policy" is already implied by the crate): rename
  `SpoolDirectoryPolicySet` → `SpoolDirectorySet`,
  `MirrorPolicySet` → `MirrorSet`. The `*Policy` suffix on the
  payload types (`SpoolDirectoryPolicy`, `MirrorPolicy`) is the
  ancestor-prefix-on-payloads pattern — strictly, the working
  noun should be `SpoolDirectory(FilesystemPath)`,
  `Mirror(MirrorPolicy fields)`. But payload names refer to the
  declared policy record, not the operation; "policy" reads as
  the noun here. Designer lean: leave payload names as
  `SpoolDirectoryPolicy`/`MirrorPolicy` (they describe what
  the record IS, a policy); drop "Policy" from reply variants.

### Scope of state the owner contract owns

The owner channel manages policy:

- Repository registration: which Gitolite repositories are
  ledger-tracked. State: `mirror_policies` and
  `repository_registrations` tables in the sema-engine DB.
- Spool directory policy: where fallback spool files are read
  from. State: `spool_directory_policy` table.
- Mirror policy: which repositories mirror to which external
  remotes. State: `mirror_policies` table.

The triad invariant 5 framework applies cleanly: registration,
spool-directory, and mirror policies are policy state; the event
and commit tables are working state. The bootstrap-policy.nota
slot (§2.10) should seed the spool directory policy and any
default-registered repositories.

### Future scope

`ARCHITECTURE.md:34-46` lists owner-scope ownership including
"GitHub mirroring execution in the first slice" as *not owned*
today. That carve-out is fine for the prototype but the mirror
policy is currently declared without an executor — the daemon
stores mirror policies but does nothing with them. The owner
contract may need to grow over time (e.g., explicit
`SyncMirror(Name)` operations to trigger one-shot mirror runs)
but that is beyond the present audit.

## 4 · Recommended next slice

In priority order:

1. **Resolve the runtime/contract source drift** (§2.1). The
   runtime currently does not compile against the migrated working
   contract; this is a hard blocker on every other slice.
   Mechanical pass renaming variant references and updating
   imports.

2. **Drop the redundant fields from `RequestUnimplemented`** in
   both contracts (§1.6). Working contract:
   `{ operation, query, reason }` → `{ reason }`. Owner contract:
   `{ operation, reason }` → `{ reason }`. Update the runtime
   `as_unimplemented_reason` / `into_owner_unimplemented`
   construction sites.

3. **Migrate `owner-signal-repository-ledger` to `signal-frame`**
   (§1.1, §1.3, §2.7). Switch dependency, drop the old `request
   Request { ... }` wrapper, rename to contract-local verbs
   (`Register`, `Retire`, `SetSpoolDirectory`, `SetMirror`).
   Update runtime imports.

4. **Switch the runtime crate's `signal-core` imports to
   `signal-frame`** (§2.2). Update `Cargo.toml`, `src/lib.rs`,
   `src/client.rs`, `src/daemon.rs`, `src/frame_io.rs`. The
   import names are mostly unchanged at the use-site level
   (`Reply as CoreReply` → either `Reply as FrameReply` or
   directly named). The pre-executor handle code in
   `handle_ordinary_request` / `handle_owner_request` can stay
   for one slice (re-typed against `signal-frame` names) and
   then retire when the executor migration lands.

5. **Add the `bootstrap-policy.nota`** (§2.10). Declare the
   default spool directory at minimum. Add a first-start
   bootstrap step to the daemon that reads it once and writes the
   typed records as if they came through owner-Mutate.

6. **Drop the empty `Catalog` marker; switch to a unit variant**
   (§1.7). Small.

7. **Rename `Receive`/`Observe` to `Record(Capture)`** (§2.4).
   Lift to a single capture operation with a typed sum payload,
   matching spirit's `Record(Entry)`. Updates the working
   contract's operation root; updates the runtime's dispatch
   match.

8. **Rename `QueryKind::CommitMessages` → `QueryKind::Commits`**
   and align the `Query`/`QueryResult` variant pair to be
   symmetric (§2.5). Update the hand-written `kind()` impls and
   the runtime's variant references.

9. **Adopt the generated `signal_cli!` dispatch** (§2.12). Pull
   both contracts into the macro invocation; let the CLI route by
   compile-time operation head. Owner operations become reachable
   from the CLI.

10. **Migrate the daemon onto `signal-executor`** (§2.3). Define
    `repository_ledger::Command` and `Effect` enums; implement
    `ToSemaOperation`, `ToSemaOutcome`, `Lowering`, and
    `CommandExecutor`. Replace `handle_ordinary_request` /
    `handle_owner_request` with `Executor::execute(request)`.
    This is the structurally heaviest slice.

11. **Drop the 5-line alias dance** in both contracts (§1.9),
    contingent on the `signal-frame` macro prefix-drop work
    landing (cross-workspace bead `primary-77hh`).

12. **Add the missing triad-invariant witness tests** (§2.11),
    deferred to after the bootstrap and CLI dispatch slices land
    since the witnesses depend on those features existing.

13. **Resolve the workspace-wide timestamp question** (§1.11).
    Independent of the rest; align ledger's `Timestamp(String)`
    with whatever the workspace settles.

Open questions for psyche (carried in §0 chat reply):

- §2.4 — lift `Receive`/`Observe` to one `Record(Capture)` with
  typed sum, matching spirit. Designer lean: yes.
- §1.10 — observable block on ledger. Designer lean: no, defer
  until persona-introspect lands and the workspace has a
  universal observer story (ledger is non-persona infrastructure).

## 5 · References

- `operator/150-triad-signal-sema-migration-current-state.md`
  §5.2 (ledger pilot status) and §7 (migration playbook).
- `designer/258-persona-signal-triad-audit-2026-05-21.md` (audit
  shape template; engine-manager triad).
- `designer/257-signal-contracts-names-and-shape-audit.md` (cross-
  workspace contract audit; §1.1–1.11 patterns).
- `second-operator-assistant/11-signal-type-naming-and-shape-design-guideline.md`
  (signal-type naming and shape design guidance).
- `designer-assistant/129-mind-orchestrate-payload-and-cli-dispatch-option-a-2026-05-20.md`
  (the generated CLI dispatch macro design).
- `intent/persona.nota` 2026-05-20T15:00:00Z — persona-spirit
  pilot priority; ledger as alternate pilot.
- `intent/signal.nota` 2026-05-20T17:10:00Z — spirit pilot
  complete; ledger work resumes on landed signal/sema logic.
- `intent/signal.nota` 2026-05-20T00:07:55+02:00 — `QueryResult`
  lift correction for the ledger pilot specifically.
- `intent/component-shape.nota` 2026-05-19T19:45 / 20:00 /
  20:30 — contract-local verbs, signal-frame rename,
  macro shape.
- `intent/component-shape.nota` 2026-05-21T10:30:00Z — modules-
  not-options for macro disambiguation (informs §1.9 retirement
  path).
- `intent/component-shape.nota` 2026-05-21T01:15:44+02:00 — macro
  generates `OperationKind` and `From<Payload> for Reply`
  (informs §2.6).
- `intent/workspace.nota` 2026-05-19 18:30 — two-field timestamp
  Decision (scopes to intent records; ledger timestamp is
  open).
- `skills/component-triad.md` §1–5 — the five invariants and the
  single-argument rule (informs §2.10–2.11 gaps).
- `skills/naming.md` §"Anti-pattern: repeated category words" and
  §"Anti-pattern: prefixing names with their namespace or
  domain" (informs §1.5, §2.4).
- `ESSENCE.md` §"Naming" — full English words + no redundant
  ancestry.
- Code: `/git/github.com/LiGoldragon/signal-repository-ledger/src/lib.rs`,
  `/git/github.com/LiGoldragon/owner-signal-repository-ledger/src/lib.rs`,
  `/git/github.com/LiGoldragon/repository-ledger/src/lib.rs`,
  `/git/github.com/LiGoldragon/repository-ledger/src/client.rs`,
  `/git/github.com/LiGoldragon/repository-ledger/src/daemon.rs`,
  `/git/github.com/LiGoldragon/repository-ledger/src/bin/`,
  `/git/github.com/LiGoldragon/repository-ledger/Cargo.toml`,
  `/git/github.com/LiGoldragon/owner-signal-repository-ledger/Cargo.toml`,
  `/git/github.com/LiGoldragon/signal-repository-ledger/Cargo.toml`,
  `/git/github.com/LiGoldragon/repository-ledger/ARCHITECTURE.md`,
  `/git/github.com/LiGoldragon/repository-ledger/AGENTS.md`,
  `/git/github.com/LiGoldragon/repository-ledger/tests/store.rs`.

This report retires when the runtime/contract drift is resolved
(step 1), the owner contract migration lands (step 3), the
runtime moves to `signal-frame` (step 4), and the daemon adopts
`signal-executor` (step 10) — or when a successor audit
supersedes.
