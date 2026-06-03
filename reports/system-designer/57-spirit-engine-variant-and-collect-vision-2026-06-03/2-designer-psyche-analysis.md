---
title: 2 — Designer psyche-analysis on Spirit engine variants + collect + defaults
role: system-designer
variant: Psyche
date: 2026-06-03
topics: [spirit, variants, collect, defaults, psyche-analysis]
description: |
  Designer-side psyche analysis of the four new Spirit operations directed
  today — CollectRemovalCandidates, OutputTarget, the small-record data type,
  and RecordDefault — read against the SOURCE AS IT STANDS TODAY, against the
  operator-vision sibling report inside this directory, and against the
  parallel cluster-of-reports landing today in the system-operator lane. Shows
  verbatim code excerpts at the load-bearing insertion points, names the
  surprise that one of the four operations is already in source, lays out
  open decisions in plain terms, and ties the slice to the deployment-chain
  gap from report 53.
---

# 57.2 — Designer psyche-analysis on Spirit engine variants + collect + defaults

Kind: psyche
Topics: spirit, variants, collect, defaults, psyche-analysis
Date: 2026-06-03

## Intent Anchors

[Spirit gains an explicit CollectRemovalCandidates operation as a Signal
root. It collects all records currently at Zero certainty and emits their
summary form to a configurable output target. Separates the discovery /
extraction concern from the destruction concern in Remove.] (Decision High,
today)

[Operations that extract or emit content from Spirit accept a customizable
output-target enum as the final field in the request shape. Variants
include Stdout, Stderr, and File with a path payload. Not an error channel
— Stderr is one option among normal outputs. Keeps the wire interface
uniform across extraction operations.] (Decision High, today)

[Spirit defines a small-record data type carrying the core load-bearing
fields — identifier, topics, kind, description summary, magnitude,
daemon-stamped date and time. The variant-ladder short forms and
CollectRemovalCandidates emit the small record; archiving tools consume
it. Reduces wire weight; matches the natural reading shape an agent or
human wants.] (Decision High, today)

[Spirit gains a RecordDefault short-form recording operation taking only
fields agents commonly customize — topics, kind, description, magnitude
— with defaults injected for the rest (privacy at Zero per the dev-mode
public-repo grounding, daemon-stamped date and time, plus any other
rarely-customized field). Record remains the canonical full-fidelity
operation.] (Decision High, today)

[Spirit operations should support a simpler-to-more-complex variant
ladder — short forms with summary defaults for normal operations,
complex forms with full metadata for custom operations.] (Decision High,
today)

[The workspace context that grounds Spirit's most-public default is
development-mode for public repositories — collaborative work on shared
open-source software where most intent captures inform future agents
and contributors.] (Clarification High, today)

[Open-work and psyche reports must explain opaque unresolved items in
plain terms, including what the item means and why it matters; listing
a label without explanation is not enough.] (Correction High, today)

## Section 1 — Today's direction, in plain terms

Today's fresh intent surfaces four new Spirit operations that pull the
load apart along three separate axes.

The first axis is WHAT IS BEING CAPTURED. The current `Record` operation
asks an agent to compose a full `Entry` — five positional fields with
every detail filled in (topics, kind, description, certainty, privacy).
The new direction names a `SmallRecord` data type carrying only the
load-bearing seven fields — identifier, topics, kind, description summary,
magnitude, and daemon-stamped date and time. The small record is the
shape archiving tools consume and short-form reads emit.

The second axis is HOW OUTPUT IS CONSUMED. The current operations all
reply through the same socket — the daemon doesn't choose where the
output goes. The new `OutputTarget` enum names variants `Stdout`,
`Stderr`, and `File (path)` as the last positional field on extraction
operations, lifting the where-does-it-go choice into the request
contract.

The third axis is WHICH DEFAULTS ARE CONVENIENT. The current `Record`
operation requires every field on every call. The new `RecordDefault`
operation takes only the four fields agents commonly customize — topics,
kind, description, magnitude — with privacy at Zero baked in, date and
time stamped by the daemon. The full `Record` form survives unchanged.

The fourth piece is the operation `CollectRemovalCandidates` itself —
explicit nominate-then-archive-then-retract semantics for records that
have been reviewed and marked at Zero certainty. Today's direction
positions it as the canonical extraction surface.

All four pieces sit downstream of the broader variant-ladder thread —
today's intent surfaces [Spirit operations should support a
simpler-to-more-complex variant ladder — short forms with summary
defaults for normal operations, complex forms with full metadata for
custom operations.] (Decision High, today). The variant-ladder design at
`/home/li/primary/reports/system-designer/55-spirit-variant-ladder-design-research-2026-06-02.md`
proposed ~30 short-form operation roots; today's four-operation slice is
the bedrock the rest of that ladder lands on. CollectRemovalCandidates
and RecordDefault are specifically the **variant-ladder shape for
specialized rituals**, not the generic short-read family (those land
later as `Recent`, `Today`, `Lookup`, etc.).

The shape of the problem these four operations solve, in one sentence:
the current wire conflates record-capture-format, output-destination, and
field-default-policy into a single overdense operation each, and today's
direction pulls those concerns apart into composable pieces.

## Section 2 — The situation on the ground

The most important finding in this analysis is one the operator-vision
sub-agent missed: **`CollectRemovalCandidates` is already implemented in
source**. The operation exists in the schema, in the contract crate, in
the daemon Command/Effect projection, in the store handler, and in the
dispatch arm-table. It is not source-new. It is deploy-new. The deployed
v0.3.0 binary doesn't yet route it (verified this session — the live
binary returns *"unknown request head: CollectRemovalCandidates"*), and
the new direction asks for slight reshaping of the existing operation,
not de-novo construction.

This reframes the implementation cost dramatically. The operator vision
budgeted ~250 lines of production Rust across the four operations; with
the existing scaffolding accounted for, the slice is closer to ~80 lines
of production Rust plus reshaping decisions.

Below: the load-bearing code excerpts that show what's already there,
each annotated with the engine-analysis vocabulary — *hooked* (full
code path, exercised), *stubbed* (typed unimplemented), *contract-only*
(types declared, no handler), *conceptual* (architecture says it, code
doesn't), or *stale* (docs / code names contradict current truth).

### The schema operation list — CollectRemovalCandidates is already a root

In `/git/github.com/LiGoldragon/signal-persona-spirit/spirit.schema:6-15`:

```
[
  (State (Statement))
  (Record (Entry))
  (Observe (Observation))
  (Watch (Subscription))
  (Unwatch (SubscriptionToken))
  (Remove (RecordIdentifier))
  (ChangeCertainty (CertaintyChange))
  (CollectRemovalCandidates (RemovalCandidateCollection))
]
```

Status: **hooked**. CollectRemovalCandidates IS in the operation root
list today (line 14), takes a `RemovalCandidateCollection` payload, and
the `signal_channel!([schema])` macro at
`signal-persona-spirit/src/lib.rs:1166` synthesizes it into the
`Operation` enum.

The schema's reply set at the same file lines 102-115 already includes
`RemovalCandidatesCollected` as a reply variant. The schema's
`OperationKind` at line 97 already includes `CollectRemovalCandidates`
in the kind enum.

The operator vision proposed adding this operation to the schema list.
The schema already has it.

### The existing `RemovalCandidateCollection` payload

At `signal-persona-spirit/src/lib.rs:814-848`:

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaRecord, Debug, Clone, PartialEq, Eq)]
pub struct RemovalCandidateCollection {
    pub record_query: RecordQuery,
    pub archive_target: ArchiveTarget,
}

impl RemovalCandidateCollection {
    pub fn new(record_query: RecordQuery, archive_target: ArchiveTarget) -> Self {
        Self {
            record_query,
            archive_target,
        }
    }

    pub fn inline() -> Self {
        Self::new(
            RecordQuery::removal_candidates(ObservationMode::SummaryOnly),
            ArchiveTarget::Inline,
        )
    }

    pub fn file(path: impl Into<String>) -> Self {
        Self::new(
            RecordQuery::removal_candidates(ObservationMode::SummaryOnly),
            ArchiveTarget::file(path),
        )
    }

    pub fn is_exact_zero_candidate_query(&self) -> bool {
        matches!(
            self.record_query.certainty_selection,
            CertaintySelection::Exact(Magnitude::Zero)
        )
    }
}
```

Status: **hooked**. The payload carries a `RecordQuery` (the same filter
substrate the rest of the contract uses) plus an `ArchiveTarget`. Two
constructor short-forms — `inline()` and `file(path)` — already produce
the canonical extraction call with a pre-baked Zero-certainty query.

The `is_exact_zero_candidate_query` predicate is the safety check that
the daemon-side guard uses to reject broad collection queries. This is
the existing source-level answer to the safety concern about
accidentally removing non-Zero records.

### The existing `ArchiveTarget` — two variants today

At `signal-persona-spirit/src/lib.rs:802-812`:

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaEnum, Debug, Clone, PartialEq, Eq)]
pub enum ArchiveTarget {
    Inline,
    File(ArchivePath),
}

impl ArchiveTarget {
    pub fn file(path: impl Into<String>) -> Self {
        Self::File(ArchivePath::new(path))
    }
}
```

Status: **hooked**. Two variants — `Inline` (reply carries the records
back, no file write) and `File(ArchivePath)` (daemon writes a serialized
NOTA archive to disk and replies with an acknowledgement).

The direction in today's intent names a different enum — `OutputTarget`
with three variants `Stdout`, `Stderr`, `File`. The relationship between
`ArchiveTarget` and `OutputTarget` is the central reshaping decision in
this slice. Two readings:

- **Reading A: rename and extend.** The existing `ArchiveTarget` becomes
  `OutputTarget` and gains the `Stderr` variant. The `Inline` variant
  collapses into the new `Stdout` variant — both mean "reply contains
  the records, the CLI wrapper routes the reply text to its terminal."
- **Reading B: parallel types.** Keep `ArchiveTarget` for the archive
  emission semantics (Inline / File-on-daemon-disk) and add a new
  `OutputTarget` for the broader output-routing axis on the new
  variant-ladder short-reads that consume it.

Reading A is the cleaner direction. The existing `Inline` already does
exactly what `Stdout` would do — daemon emits records as typed reply
data, CLI wrapper renders. The semantic content the new `Stderr` variant
adds is *"route the reply to standard error instead of standard
output."* The existing `Inline` is `Stdout` in different vocabulary.

The system-operator contract-shape sidecar at
`/home/li/primary/reports/system-operator/189-production-spirit-collect-removal-candidates-2026-06-03/1-contract-shape-review.md`
landed at 15:31 today reaches the same conclusion: *"For ordinary CLI
use `Inline` is the better first target … `Inline` means the daemon
returns the compact archive material as typed reply data; the CLI can
then render that material to stdout. This is the clean way to satisfy
`stdout` behavior without commanding the daemon to write into its own
systemd/service stdout stream."* That reading is the parallel-lane
operator angle; reading A in this report agrees.

### The existing daemon handler — combines extract AND remove

In `/git/github.com/LiGoldragon/persona-spirit/src/store.rs:126-144`:

```rust
pub fn collect_removal_candidates(
    &self,
    collection: RemovalCandidateCollection,
) -> Result<RemovalCandidatesCollected> {
    CollectionQueryGuard::new(&collection).validate()?;
    let candidates = self.records_for_query(&collection.record_query)?;
    let archive = RemovalCandidateArchive::from_stored_records(&candidates);
    archive.write_to_target(&collection.archive_target)?;
    for record in &candidates {
        self.engine
            .retract(Retraction::new(self.records, StoredRecord::key(record.identifier)))
            .map_err(Error::spirit_store)?;
    }
    Ok(RemovalCandidatesCollected::new(
        archive.records(),
        candidates.iter().map(|record| record.identifier).collect(),
        Vec::new(),
    ))
}
```

Status: **hooked**. The handler validates the request (must be
exact-Zero certainty), runs the query, archives to the chosen target,
then retracts each candidate. This is the **combined extract-and-remove**
shape — the existing operation is NOT pure-extract; it removes after a
successful archive.

The order-of-operations is significant: archive-first, retract-only-on-
success. If archive emission fails (e.g., a `File(path)` target that
fails to write), the records are NOT removed. This is the safety
property the system-operator's parallel sidecar report at
`reports/system-operator/189-…/2-archive-policy-and-test-review.md`
names explicitly — *no collection without archive emission*.

Today's intent statement reads — [Spirit gains an explicit
CollectRemovalCandidates operation as a Signal root. It collects all
records currently at Zero certainty and emits their summary form to a
configurable output target. Separates the discovery / extraction
concern from the destruction concern in Remove.] (Decision High, today)
— and the *"Separates the discovery / extraction concern from the
destruction concern in Remove"* clause is the load-bearing reshaping
question. The existing implementation **does NOT separate them** — it
extracts and retracts in one operation. Today's intent could be read
either way:

- **Reading 1: strictly extract.** The intent reshapes the existing
  operation to drop the retraction step. CollectRemovalCandidates becomes
  pure extraction; a separate `Remove` call per identifier is required
  to actually delete.
- **Reading 2: extract-then-remove, where "separation from Remove" means
  separation from the ad-hoc per-record `Remove` operation.** The
  existing combined operation already separates the GUIDED MASS-COLLECT
  from per-record removal. The intent is about avoiding the use of
  `(Remove N)` calls in a loop, not about decoupling archive from
  retract within `CollectRemovalCandidates` itself.

This is open decision #1 in §4 below and the most important question
for the psyche to engage with — it determines whether today's directive
reshapes the existing handler or strictly preserves it.

### The existing guard rail and write path

In the same file at lines 362-407 (the `CollectionQueryGuard` and
`RemovalCandidateArchive` structs):

```rust
impl<'collection> CollectionQueryGuard<'collection> {
    fn new(collection: &'collection RemovalCandidateCollection) -> Self {
        Self { collection }
    }

    fn validate(&self) -> Result<()> {
        if self.collection.is_exact_zero_candidate_query() {
            return Ok(());
        }
        Err(Error::RequestRejected {
            reason: "CollectRemovalCandidates requires an exact Zero certainty query".to_string(),
        })
    }
}

impl RemovalCandidateArchive {
    fn from_stored_records(records: &[StoredRecord]) -> Self {
        Self {
            records: records.iter().map(StoredRecord::summary).collect(),
        }
    }

    fn write_to_target(&self, target: &ArchiveTarget) -> Result<()> {
        match target {
            ArchiveTarget::Inline => Ok(()),
            ArchiveTarget::File(path) => self.write_to_file(path),
        }
    }

    fn write_to_file(&self, path: &ArchivePath) -> Result<()> {
        let observed = RecordsObserved::new(self.records.clone());
        let mut encoder = Encoder::new();
        observed
            .encode(&mut encoder)
            .map_err(Error::invalid_spirit_reply)?;
        let mut file = FileSystemFile::create(path.as_str()).map_err(Error::input_output)?;
        file.write_all(encoder.into_string().as_bytes())
            .map_err(Error::input_output)?;
        file.write_all(b"\n").map_err(Error::input_output)?;
        file.sync_all().map_err(Error::input_output)?;
        Ok(())
    }
}
```

Status: **hooked**. The guard rejects any request whose certainty filter
isn't exact-Zero, preventing accidental mass-deletion of non-candidate
records. The archive emission writes serialized NOTA records, encoded
through the same `Encoder` the rest of the wire uses, to the target file
with `sync_all()` for durability before any retraction happens.

`FileSystemFile::create()` uses POSIX `O_TRUNC | O_CREAT` semantics —
existing file gets truncated, new file gets created. This matters for
the file-target semantics question (open decision #3 in §4).

### The dispatch arm-table — CollectRemovalCandidates routes today

At `/git/github.com/LiGoldragon/persona-spirit/src/actors/dispatch.rs:237-269`:

```rust
async fn execute_command(&self, command: Command) -> Result<CommandEffect<Command, Effect>> {
    let reply = match command.clone() {
        Command::ClassifyStatement(statement) => self.classify_statement(statement).await?,
        Command::AssertEntry(entry) => self.capture_entry(entry).await?,
        Command::RemoveRecord(identifier) => self.remove_entry(identifier).await?,
        Command::ChangeCertainty(change) => self.change_certainty(change).await?,
        Command::CollectRemovalCandidates(collection) => {
            self.collect_removal_candidates(collection).await?
        }
        Command::ReadRecords(observation) => self.observe_records(observation).await?,
        Command::ReadRecordIdentifiers(query) => self.observe_record_identifiers(query).await?,
        Command::ReadTopics => self.observe_topics().await?,
        Command::ReadState => self.observe_state().await?,
        Command::ReadQuestions => self.observe_questions().await?,
        // ... subscription arms ...
    };
    Ok(CommandEffect::new(command, Effect::from_reply(reply)))
}
```

Status: **hooked**. The dispatch arm at line 243-245 routes
CollectRemovalCandidates to `self.collect_removal_candidates(collection)`
which is the handler at lines 329-342 in the same file (the actor-side
ask wrapper that delegates to the store).

The operator vision walked through this arm-table as the place where a
new operation lands. The arm already lives there.

### The existing `Entry::open` constructor — the source-level twin of RecordDefault

At `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs:387-402`:

```rust
impl Entry {
    pub fn open(
        topics: Topics,
        kind: Kind,
        description: Description,
        certainty: Certainty,
    ) -> Self {
        Self {
            topics,
            kind,
            description,
            certainty,
            privacy: Magnitude::Zero,
        }
    }
}
```

Status: **hooked** (as in-process API), **contract-only** (no wire-level
twin yet).

`Entry::open` is the in-process constructor that bakes
`privacy: Magnitude::Zero` as the default. An author calling
`Entry::open` is opting in to the open-public default without thinking
about it; an author who wants elevation constructs the full `Entry`
struct directly.

This four-field constructor is the source-level manifestation of [The
workspace context that grounds Spirit's most-public default is
development-mode for public repositories — collaborative work on shared
open-source software where most intent captures inform future agents
and contributors.] (Clarification High, today). The four fields it
takes — topics, kind, description, certainty — are exactly the four
fields the new `RecordDefault` operation takes per today's directive.

`RecordDefault` is the WIRE-LEVEL TWIN of `Entry::open`. The mechanical
transformation: a new `OpenEntry` payload type wraps the four fields,
the new `RecordDefault` operation root takes `(OpenEntry)`, and the
daemon handler converts via `OpenEntry::into_entry()` which calls
`Entry::open(...)`. The same `Magnitude::Zero` privacy default lands at
the daemon side; no parser change needed.

### The existing `CertaintySelection::removal_candidates()` constructor

At `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs:556-559`:

```rust
impl CertaintySelection {
    pub const fn removal_candidates() -> Self {
        Self::Exact(Magnitude::Zero)
    }
    // ...
}
```

The corresponding `RecordQuery::removal_candidates(mode)` at lines
637-647:

```rust
impl RecordQuery {
    pub fn removal_candidates(mode: ObservationMode) -> Self {
        Self {
            topic_selection: TopicSelection::any(),
            kind: None,
            certainty_selection: CertaintySelection::removal_candidates(),
            recorded_time_selection: RecordedTimeSelection::Any,
            privacy_selection: PrivacySelection::default_observation_privacy(),
            mode,
        }
    }
}
```

Status: **hooked**. The Zero-certainty selector and the canonical
removal-candidate query both already exist as named constructors. The
existing `CollectRemovalCandidates` operation reuses both. Any
reshaping of the operation reuses these same constructors — no new
filter logic.

(Note: the operator-vision sub-agent cited these as lines 622-633.
The actual lines are 556-559 for `CertaintySelection` and 637-647 for
`RecordQuery`. Both are present; the line numbers shifted as the file
grew.)

### The existing reply shape — already a four-vector receipt

At `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs:891-922`:

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaRecord, Debug, Clone, PartialEq, Eq)]
pub struct RemovalCandidatesCollected {
    pub archived_records: Vec<RecordSummary>,
    pub removed_identifiers: Vec<RecordIdentifier>,
    pub skipped_candidates: Vec<SkippedRemovalCandidate>,
}

impl RemovalCandidatesCollected {
    pub fn new(
        archived_records: Vec<RecordSummary>,
        removed_identifiers: Vec<RecordIdentifier>,
        skipped_candidates: Vec<SkippedRemovalCandidate>,
    ) -> Self {
        Self {
            archived_records,
            removed_identifiers,
            skipped_candidates,
        }
    }

    pub fn archived_records(&self) -> &[RecordSummary] {
        &self.archived_records
    }

    pub fn removed_identifiers(&self) -> &[RecordIdentifier] {
        &self.removed_identifiers
    }

    pub fn skipped_candidates(&self) -> &[SkippedRemovalCandidate] {
        &self.skipped_candidates
    }
}
```

Status: **hooked**. The reply already carries three vectors — archived
records, removed identifiers, and skipped candidates with typed reasons
(`RemovalCandidateSkipReason::ArchiveFailed | RecordChanged |
RecordAlreadyRemoved | NoLongerCandidate` at lines 873-881).

The system-operator sidecar at the contract-shape review proposed
adding a fourth field `inline_archive: Vec<RecordSummary>` for the
Inline-target case. The current shape uses `archived_records` for that
slot already — when target is `Inline`, the archived_records vector
carries the records back through the reply, when target is `File`, the
archived_records vector still carries the records (so the caller sees
what was written). This pattern works for both targets.

### The existing observe handler patterns — the templates the operator vision named

At `/git/github.com/LiGoldragon/persona-spirit/src/store.rs:165-173`:

```rust
pub fn observe_records(&self, observation: RecordObservation) -> Result<WorkingReply> {
    let records = self.records_for_query(&observation.query)?;
    Ok(RecordReply::new(records, observation.query.mode).into_working_reply())
}

pub fn observe_record_identifiers(&self, query: RecordIdentifierQuery) -> Result<WorkingReply> {
    let records = self.records_for_identifier_query(query)?;
    Ok(RecordReply::new(records, query.mode).into_working_reply())
}
```

Status: **hooked**. These are the two-line handler shapes the operator
vision named as the templates new operations would mirror. The pattern
is: query → fetch records → wrap in reply.

The interesting thing is that `RecordReply::new(records, mode)` at
`store.rs:342-360` dispatches on `mode` to produce either a summary-only
reply or a provenance-stamped reply. The small-record direction from
today asks for an emit-shape that's between the two — the summary fields
PLUS date and time but NOT the privacy field. This is a third dispatch
arm on the existing `RecordReply::into_working_reply` method, not a
parallel handler.

### Summary of what's hooked, stubbed, or new

| Piece | Status | Where |
|---|---|---|
| `CollectRemovalCandidates` operation | hooked | `spirit.schema:14` + `lib.rs:1166` macro |
| `RemovalCandidateCollection` payload | hooked | `lib.rs:814-848` |
| `ArchiveTarget` (Inline / File) | hooked | `lib.rs:802-812` |
| `RemovalCandidatesCollected` reply | hooked | `lib.rs:891-922` |
| Skipped reasons enum | hooked | `lib.rs:873-881` |
| Store handler | hooked, combines extract + remove | `store.rs:126-144` |
| Dispatch arm | hooked | `dispatch.rs:243-245` |
| Guard + archive write | hooked | `store.rs:362-407` |
| `Entry::open` (privacy-Zero default) | hooked (in-process) | `lib.rs:387-402` |
| `RecordDefault` (wire-level twin of Entry::open) | not yet — new operation | needs schema + handler |
| `SmallRecord` shape | conceptual — `RecordSummary` lacks date/time, `RecordProvenance` lacks privacy-omission semantics | `lib.rs:857-871` |
| `OutputTarget` enum vs existing `ArchiveTarget` | reshape decision | see open decision #2 |
| Boundary tests for `CollectRemovalCandidates` | partially hooked (in-store tests) but no NOTA wire boundary tests | `store.rs:980-1110` |
| Deployed v0.3.0 binary serves `CollectRemovalCandidates` | stale — source ahead of deploy | verified this session |

The picture: today's slice is **mostly reshape** of existing source plus
**two new pieces** (`SmallRecord` + `RecordDefault`). The amount of NEW
code is small; the amount of THINKING ABOUT EXISTING SHAPES is large.

## Section 3 — How the operator sees it

The operator-vision sub-agent at
`reports/system-designer/57-spirit-engine-variant-and-collect-vision-2026-06-03/1-operator-vision.md`
proposes a seven-phase landing sequence:

1. **Phase 1: Schema additions in `signal-persona-spirit`.** Land the
   `SmallRecord`, `OutputTarget`/`OutputPath`, new reply types, `OpenEntry`,
   and new operation roots (CollectRemovalCandidates, RecordDefault,
   Tier-1 short-form reads). Substantial schema delta but mechanical.
2. **Phase 2: Handler implementations in `persona-spirit`.** Command +
   Effect enum additions, store handler methods, dispatch arms. ~250
   lines of production Rust.
3. **Phase 3: Boundary tests.** ~250 lines of test Rust, ~8 new tests
   modeled on existing patterns.
4. **Phase 4: CLI handling.** Implicit — the `signal_cli!` macro derives
   the surface from schema, no hand-written changes needed.
5. **Phase 5: Parallel additions to `spirit-next`.** Schema mirror in
   the schema-derived pilot.
6. **Phase 6: Deployment config.** Only if config-shape changes; for
   this slice, no daemon-config field additions, just a rebuild.
7. **Phase 7: Production cutover.** Either rebuild the v0.3.0 slot from
   the new source, or land on the spirit-next pilot first.

The operator vision identifies six open questions: where OutputTarget
attaches on existing operations, whether CollectRemovalCandidates
remains separate from Remove, file-target failure modes, the small-
record's exact field list, RecordDefault privacy override, and source-
first vs deploy-first ordering.

### Where the designer agrees

The seven-phase sequencing is sound. Schema-first is correct because the
schema drives macro emission of the `Operation` enum, and the rest of
the pipeline follows from there. Tests-after-handlers is the right
order. The CLI being implicit is correct — `signal_frame::signal_cli!`
already derives the surface.

The operator vision's lean toward Option C on question 1 — *"add
OutputTarget only on operations the directive explicitly names"* — is
the safe direction. The existing `RecordQuery` six-field shape doesn't
need a seventh field added; the new short-form reads can carry their
own `OutputTarget` field when relevant.

The operator vision's lean on question 4 — *"strict directive, omit
privacy entirely from SmallRecord"* — agrees with the directive's
literal field list. The small record is shaped for archival reading,
not privacy-axis filtering. The privacy axis lives on the full record.

The operator vision's lean on question 5 — *"strict four fields for
RecordDefault, privacy elevation requires Record or a named variant"*
— agrees with the directive's framing. The convenience of RecordDefault
is exactly the *don't-type-Zero* property; admitting an optional fifth
field defeats that convenience.

### Where the designer sees a different shape

**Major gap: the operator vision missed that
CollectRemovalCandidates is already in source.** The vision walks
through the schema operation list as if appending `(CollectRemovalCandidates
(OutputTarget))` is the addition. The schema already declares
`(CollectRemovalCandidates (RemovalCandidateCollection))` at
`spirit.schema:14`. The operation root is hooked.

This changes the framing of the slice substantially. The work is not
*add a new operation*; the work is *reshape the existing operation's
payload from `RemovalCandidateCollection` (carrying RecordQuery +
ArchiveTarget) into something that better matches today's intent*. Or
keep the payload and just rename `ArchiveTarget` to `OutputTarget` to
gain `Stderr` as a third variant.

**Major gap: the operator vision missed that the existing handler
combines extract AND remove.** The vision walks through proposing a new
`collect_removal_candidates` method that emits records but doesn't
remove them — it lands as an `Observe`-shape (read-only) operation. The
existing handler at `store.rs:126-144` archives THEN retracts in one
call. The slice's directive — *"Separates the discovery / extraction
concern from the destruction concern in Remove"* — needs psyche
clarification on whether the existing combined-shape is correct (the
existing operation separates BULK collect from PER-RECORD `Remove`) or
whether the directive asks for fully decoupling archive from retract.

**Secondary gap: the operator vision under-credits the existing
constructors.** `RemovalCandidateCollection::inline()` and
`RemovalCandidateCollection::file(path)` are already there as the
ergonomic shortcuts the directive's *"common operations should have
short default forms"* clause asks for.

**Secondary gap: the operator vision proposes a 4-field
`RemovalCandidatesCollected` reply (with a new `inline_archive` field)
to match the system-operator sidecar review's recommendation.** But the
existing reply at `lib.rs:891-922` already carries
`archived_records: Vec<RecordSummary>` — the same role as
`inline_archive`. The two proposals (operator vision + system-operator
sidecar) are reinventing a field that already exists.

### Where the designer adds substance the operator vision didn't surface

**The SmallRecord vs RecordSummary vs RecordProvenance shape question
is more subtle than choice A/B.** The operator vision frames it as
*"replace RecordSummary with SmallRecord"* OR *"add SmallRecord as a
parallel type"*. The actual landscape:

- `RecordSummary` (lines 857-863) carries `identifier, topics, kind,
  description, certainty, privacy` — six fields, no date/time, has
  privacy.
- `RecordProvenance` (lines 866-871) wraps `RecordSummary` plus `date,
  time` — eight fields effectively, has privacy.
- The directive's `SmallRecord` field list — *identifier, topics, kind,
  description summary, magnitude, daemon-stamped date and time* — has
  seven fields, no privacy.

The directive omits `privacy` and includes `date, time`. None of the
existing shapes exactly matches. The natural answer is: SmallRecord IS
its own type. The operator vision's choice B (parallel type) is
correct, but there's a clean implementation path the operator vision
missed: define `SmallRecord` as a projection of `RecordProvenance` that
drops the privacy field. The projection is one `impl From<RecordProvenance>
for SmallRecord` method.

**The DatabaseMarker envelope question crosses this slice.** Per report
56 §"Move 2: DatabaseMarker envelope on every reply," spirit-next
bundles a provenance envelope on every reply. The directive's
SmallRecord doesn't mention DatabaseMarker. Does the small record include
the marker (consistent with spirit-next discipline) or skip it
(consistent with the directive's literal field list)? The operator
vision missed this entirely. This is open decision #6 in §4.

**The variant-ladder Tier 1 connection is closer than the operator
vision named.** The operator vision treats `Recent`, `Today`, `Lookup`,
etc., as Phase 5 territory — separate from this slice. But the
directive's variant-ladder clause is one of the four bracket-quoted
anchors of this slice. The Tier 1 zero-argument short-forms are
candidate FIRST-WAVE landings alongside the four named operations
because they're conceptually unified: they all instantiate the same
*short-form-with-summary-defaults* pattern. Whether they land in this
slice or wave 2 is a sequencing question, but they should not be
deferred indefinitely; they are the broader load-bearing direction.

### Honest assessment of the operator vision

Strengths:

- The sequencing logic is correct and mechanical.
- The wire-shape examples are accurate.
- The boundary-test patterns are valid templates.
- The size estimates are roughly right (if interpreted as the *full
  slice including reshape work*, not just additions).
- The open questions are well-framed and the leans are mostly correct.

Weaknesses:

- Missed that CollectRemovalCandidates is already in source.
- Missed that the existing handler combines extract + remove.
- Under-credited the existing constructors and reply shape.
- Didn't surface the DatabaseMarker question.
- Treated the variant-ladder as a separate phase rather than a
  conceptual sibling.
- The proposed `OutputWritten` and `OutputWriteFailed` reply variants
  duplicate functionality the existing `RemovalCandidatesCollected`
  reply already carries (the archived_records vector is empty in the
  failed-write case; the skipped_candidates vector explains why).

The vision report is a strong starting point — the seven-phase
structure and the per-operation walkthrough remain the right shape. The
factual corrections above are important for accurate scope estimation
but don't change the broader direction.

## Section 4 — Open decisions for the psyche

Each open decision below names what the item is in plain terms, why it
matters, the options, and a recommendation when one is justified. The
discipline is from today's [Open-work and psyche reports must explain
opaque unresolved items in plain terms, including what the item means
and why it matters; listing a label without explanation is not enough.]
(Correction High, today).

### Decision 1 — Does CollectRemovalCandidates remain combined (extract + remove) or split into pure-extract?

**What it is.** The existing handler at
`/git/github.com/LiGoldragon/persona-spirit/src/store.rs:126-144` does
archive-then-retract in one call. Today's directive — [Spirit gains an
explicit CollectRemovalCandidates operation as a Signal root. It
collects all records currently at Zero certainty and emits their
summary form to a configurable output target. Separates the discovery /
extraction concern from the destruction concern in Remove.] (Decision
High, today) — has a clause about separation that reads two ways. Either
the directive is asking for pure-extract semantics (drop the retract
step from the existing handler), or the directive is naming the
SEPARATION FROM PER-RECORD Remove (the existing combined handler
already provides this).

**Why it matters.** This is the load-bearing reshape question. If
pure-extract is intended, the existing handler shrinks and a separate
follow-up flow (multi-remove? batched delete?) is needed for the
remove half. If the existing combined handler is correct, the slice is
mostly cosmetic reshape (variant rename, field tweaks) and the existing
safety properties stay intact.

**The options.**

- **A. Strictly extract.** The new operation only collects records to
  the output target. The retract step is dropped. To actually delete
  records, the caller must follow up with `(Remove N)` per identifier.
  Reading 1 above.
- **B. Keep combined.** The directive's separation language refers to
  separation from per-record Remove, not separation of extract from
  retract within CollectRemovalCandidates. The existing handler is
  correct. Reading 2 above.
- **C. Hybrid — two operations.** Both shapes land. `CollectRemovalCandidates`
  becomes pure-extract; a new `CollectAndRemoveRemovalCandidates` (or
  similarly-named) becomes the combined operation. Caller chooses.

**Recommendation: B.** The existing combined shape is what the system-
operator sidecar at report 189 just ratified independently — *"the
operation removes candidates from the hot intent store after archive
emission succeeds, so the visible store effect is retraction."* The
*"separation from Remove"* in the directive is best read as separation
from the *per-record* `(Remove N)` flow. The combined-but-guarded
operation captures the workflow correctly: review at Zero, then collect
(which archives + removes) in one call. Pure-extract leaves the caller
in an awkward two-step that loses the safety guarantee (archive-before-
retract).

**This is the most important decision for the psyche.** Either the
existing implementation is the correct shape (the slice becomes a small
reshape pass) or the implementation needs significant rework (the
slice becomes a re-architect pass).

### Decision 2 — Does OutputTarget replace ArchiveTarget, or sit alongside it?

**What it is.** The existing `ArchiveTarget` at
`signal-persona-spirit/src/lib.rs:802-812` has two variants — `Inline`
and `File(ArchivePath)`. Today's intent names a different enum
`OutputTarget` with three variants — `Stdout`, `Stderr`, `File(path)`.
The relationship between them is undefined.

**Why it matters.** Two different vocabularies, almost-but-not-quite the
same semantics. If both land, the schema carries duplicate concepts. If
one replaces the other, every existing call site (`RemovalCandidateCollection::inline()`,
`::file(path)`) reshapes.

**The options.**

- **A. Rename ArchiveTarget → OutputTarget, add Stderr.** The existing
  Inline variant becomes Stdout in vocabulary (both mean "reply carries
  records back, CLI wrapper routes"). The File variant stays. The new
  Stderr variant is added. The existing constructors rename
  (`RemovalCandidateCollection::stdout()` etc.). Cleanest.
- **B. Parallel types.** Keep ArchiveTarget for `CollectRemovalCandidates`
  semantics; OutputTarget for the new variant-ladder short-reads. Two
  enums in the wire vocabulary. Risk: the conceptual overlap confuses
  future readers.
- **C. ArchiveTarget stays untouched; new OutputTarget gets a different
  three-variant set including a fourth variant for the existing
  Inline semantics.** Most legacy-friendly but proliferates the
  vocabulary.

**Recommendation: A.** The existing Inline IS Stdout in different
vocabulary, and the rename is mechanical (one enum, one set of
constructors). The added Stderr variant is what the directive names. The
existing call sites update with a search-and-replace. No semantic loss,
clean vocabulary.

### Decision 3 — File-target semantics: create-or-truncate, create-or-fail, or split into two variants?

**What it is.** The existing `RemovalCandidateArchive::write_to_file`
at `store.rs:395-407` uses `FileSystemFile::create(...)` which has POSIX
`O_TRUNC | O_CREAT` semantics — existing file gets truncated, new file
gets created. The operator vision proposes more conservative options.

**Why it matters.** Accidental overwrites of files agents care about.
The current behavior is shell `>` redirection semantics — overwrite
silently. The conservative shape is fail-if-exists. The user can also
choose to make the choice explicit via two enum variants.

**The options.**

- **A. Current behavior (create-or-truncate).** What's implemented today.
  Risk: surprising overwrite if the path happens to match.
- **B. Create-or-fail (`O_EXCL | O_CREAT`).** Agent must delete the
  file between calls. Safer but more verbose.
- **C. Two variants: `File(path)` for create-or-fail, `FileOverwrite(path)`
  for create-or-truncate.** Explicit intent on the wire.
- **D. Append-or-create (`O_APPEND | O_CREAT`).** Each call adds to
  the file. Log-file semantics.

**Recommendation: B for the safety-conscious default, with C as the
explicit-intent path if the psyche prefers it.** The current behavior
is unsafe — a typo in a path can silently overwrite. Switching to
create-or-fail makes the agent re-confirm via explicit cleanup. C is
strictly more expressive than B and adds one enum variant; if the
psyche wants both semantics, C is the cleanest.

Note: the deployed v0.3.0 binary doesn't yet route CollectRemovalCandidates
at all (this session verified), so changing the semantics now has no
behavioral risk to existing users — there are no existing users.

### Decision 4 — SmallRecord field list — exactly which fields, and does it carry the DatabaseMarker envelope?

**What it is.** The directive names *identifier, topics, kind,
description summary, magnitude, daemon-stamped date and time* — seven
fields, no privacy. Two subquestions:

- Does the SmallRecord include `privacy` as an eighth field? The
  directive's list omits it.
- Does the SmallRecord include a `DatabaseMarker` envelope (per spirit-
  next's discipline)?

**Why it matters.** Every emission of SmallRecord carries those fields
and only those fields. Adding or omitting any is a wire-contract
commitment.

**The options.**

For the privacy question:

- **A. Strict directive — omit privacy entirely.** The small record is
  for archival reading; privacy axis lives on the full record.
- **B. Include privacy.** Match `RecordProvenance`'s existing seven-
  field shape with one rename.
- **C. Two variants — `SmallRecord` strictly per directive, plus
  `SmallPrivateRecord` for queries that want it.** Overengineered for
  this slice.

For the DatabaseMarker question:

- **D. Include marker.** Consistent with spirit-next discipline; every
  reply carries provenance.
- **E. Skip marker.** Consistent with the directive's literal field
  list; archive tools that need provenance can query separately.

**Recommendation: A + E.** Strict directive on both axes. The small
record is shaped for archival reading; archive tools that need privacy
or database-state provenance can issue a follow-up
`(Lookup N WithProvenance)` call. Keeping SmallRecord literally seven
fields matches the directive's *"matches the natural reading shape an
agent or human wants"* clause.

The DatabaseMarker envelope question becomes its own separate decision
when spirit-next becomes the canonical wire — production
`RemovalCandidatesCollected` today doesn't carry a marker, so adding
one is a separate cross-cutting change.

### Decision 5 — RecordDefault: strict four fields, or admit optional privacy override?

**What it is.** The directive — [Spirit gains a RecordDefault short-form
recording operation taking only fields agents commonly customize —
topics, kind, description, magnitude — with defaults injected for the
rest (privacy at Zero per the dev-mode public-repo grounding, daemon-
stamped date and time, plus any other rarely-customized field).
Record remains the canonical full-fidelity operation.] (Decision High,
today) — names four fields. The variant-ladder design at report 55
proposes a `RecordSealed` / `RecordPersonal` family as named privacy
variants. Does `RecordDefault` admit an optional fifth field that
overrides privacy?

**Why it matters.** The agent ergonomics question. Strict-four-fields
forces an agent who wants elevated privacy to reach for full `Record`
(more typing) or for a named variant. Admitting an optional privacy
field defeats the no-think-about-privacy convenience.

**The options.**

- **A. Strict four fields.** Privacy elevation requires `Record` or a
  named variant like `RecordSealed`.
- **B. Optional fifth field.** Both `(RecordDefault ([topics] Kind
  [desc] Magnitude))` and `(RecordDefault ([topics] Kind [desc]
  Magnitude Privacy))` parse.
- **C. Strict four for `RecordDefault`; add `RecordSealed`,
  `RecordPersonal`, etc., as siblings.**

**Recommendation: A.** The directive is specific about the field list,
and the value of RecordDefault is exactly the don't-type-Zero
convenience. Named-variant siblings (option C's additions) can land
later as a clean follow-up.

### Decision 6 — Sequencing: source-first then deploy, or deploy current source then iterate?

**What it is.** The existing privacy thread shows the source-ahead-of-
deploy pattern is tolerated. The privacy fields landed in source weeks
before the deployed binary serves them. Today's CollectRemovalCandidates
is in the same state — source-implemented, not yet deployed.

**Why it matters.** Source-first lets the design absorb feedback before
deployment costs are sunk. Source-and-deploy together makes the new
operations live for agents to use; otherwise they're type-system facts
nobody can call.

**The options.**

- **A. Source-first.** Land schema + types + handlers + tests, ship to
  the repository, then redeploy later as part of a larger Phase 2/3
  cutover.
- **B. Source-and-deploy.** Land the source AND rebuild the v0.3.0 slot
  from the new commit in the same cycle. The new operations become
  live immediately.
- **C. Source-and-deploy on the spirit-next slot.** Per report 53's
  Phase 2, the spirit-next slot is repointed at the actual pilot. New
  operations land on spirit-next first; v0.3.0 follows when the
  broader cutover lands.

**Recommendation: B for the immediate cycle, C for the longer arc.**
The deploy chain is short (the work is a rebuild + slot version flip,
not a redesign). Rebuilding v0.3.0 from a privacy-aware + CollectRemovalCandidates-
aware commit closes the source-ahead-of-deploy gap. Once spirit-next
is also live (per report 53's Phase 2), the same operations re-land
there for the schema-derived stack.

### Decision 7 — Tier-1 variant-ladder short reads: this slice, or follow-on?

**What it is.** Today's directive includes the broader variant-ladder
direction. The operator vision treats `Recent`, `Today`, `Lookup`,
etc., as Phase 5 territory — separate from this slice. But the four
explicitly-named operations are themselves a variant-ladder pattern
(specialized rituals with summary defaults). The question: do the
zero-argument convenience reads land in this slice or the next?

**Why it matters.** Conceptual unity vs scope discipline. If the four
new operations land alone, the *"these are variant-ladder shapes"*
framing is clearer when the next-wave short-reads arrive. If they land
together, agents get a coherent ergonomic upgrade in one cycle.

**The options.**

- **A. Four-operation slice only.** CollectRemovalCandidates,
  OutputTarget reshape, SmallRecord, RecordDefault. The Tier-1 short
  reads (Recent, Today, Lookup, etc.) wait for a follow-on slice.
- **B. Four-operation slice plus Tier-1 zero-arg short reads.** Eight
  more operation roots land alongside (Recent, Shallow, Deep, VeryDeep,
  Today, ThisWeek, Lookup, LookupRange per report 55's recommendation).
  Substantial schema delta but conceptually unified.
- **C. Four-operation slice plus Lookup/LookupRange only.** Two of the
  Tier-1 short reads — the single-record fetch — pair naturally with
  CollectRemovalCandidates and RecordDefault as the *follow-up-on-a-
  specific-record* flow.

**Recommendation: C.** `Lookup N` and `LookupRange (N M)` are the
load-bearing complement to CollectRemovalCandidates and RecordDefault —
the agent who collects candidates wants to inspect specific ones; the
agent who records a default-form wants to reference it back. Adding the
zero-arg time-range short reads (Recent, Today, etc.) is a bigger scope
expansion that should wait for a focused variant-ladder slice. Option B
is acceptable if the psyche prefers the bigger landing.

### Decision 8 — Spirit-next parallel additions: this slice, or after spirit-next deploys?

**What it is.** The spirit-next schema at
`/git/github.com/LiGoldragon/spirit-next/schema/lib.schema` already
declares `Privacy Magnitude`, `PrivacySelection`, `Entry { ... Privacy * }`,
but doesn't have a CollectRemovalCandidates operation root. The operator
vision proposes mirroring this slice into spirit-next as Phase 5.

**Why it matters.** Convergent design across the two stacks. If
spirit-next lags, the eventual cutover (per report 53's Phase 5)
becomes harder because the operation vocabulary diverges. If spirit-next
gets the additions now, the schema-derived emission needs to be
re-tested with the new types.

**The options.**

- **A. Mirror into spirit-next now.** Same operations land in both
  schemas. Both stacks march in parallel.
- **B. Defer spirit-next until production parity is reached.** Per
  report 53's Phase 3 sequence (9 schema additions for daily-use
  parity), CollectRemovalCandidates is one of the additions that
  closes the gap. Land it as part of the broader parity work.
- **C. Land in spirit-next first.** The schema-derived pilot is the
  cleaner experimental surface. Once it works there, port back to
  production.

**Recommendation: B.** The spirit-next parity work at report 53 already
sequences these additions. Adding CollectRemovalCandidates ad-hoc now
duplicates the parity work. Let spirit-next absorb this slice as part
of its planned parity arc.

### Decision 9 — DatabaseMarker envelope question for the new reply

**What it is.** Per report 56 §"Move 2", every spirit-next reply carries
a `DatabaseMarker { CommitSequence, StateDigest }` envelope.
Production's `RemovalCandidatesCollected` today doesn't carry one. If
this slice ships in production AND spirit-next, the marker question
needs to be settled.

**Why it matters.** Cross-stack consistency. If the marker is present on
spirit-next replies but absent on production replies, downstream
consumers must handle both shapes. If the marker is added to production
replies, every existing reply variant changes shape.

**The options.**

- **A. No marker on production replies; marker on spirit-next.** Honor
  each stack's existing discipline. Downstream consumers handle both.
- **B. Add marker to production replies.** Adopt spirit-next's
  discipline globally.
- **C. Per-reply choice — markers on extraction-shape replies
  (CollectRemovalCandidates), not on per-record replies (RecordAccepted).**
  Markers where provenance is load-bearing.

**Recommendation: A.** Each stack respects its discipline. The cutover
question (production → spirit-next) is broader than this slice and
should not be forced now. Open decision #9 from report 56 already
named this as a psyche question; this slice should not pre-empt that
answer.

## Section 5 — Path-to-ship, narrated

The operator's seven-phase sequence composes cleanly with the broader
spirit-next deployment-chain gap from
`reports/system-designer/53-spirit-next-production-parity-2026-06-02/5-overview.md`,
but the composition requires reading the two together.

The deployment-chain gap from report 53 names a five-phase progression:

1. The flake.lock bump (5 minutes).
2. The spirit-next slot redirect + config-materialisation snippet
   (~half-day).
3. The 9 schema additions for daily-use parity (days, designer-shape).
4. Historical record migration (weeks, designer 447's upgrade-as-SEMA).
5. The `currentDefault = "next"` flip (one line).

This slice fits between phases 2 and 3. The four operations land as
SOURCE FIRST (the existing source-ahead-of-deploy pattern applies
already), then either rebuild the v0.3.0 slot to make them live OR wait
for the spirit-next slot to absorb them in Phase 3.

If decision 6 above lands at recommendation B (source-and-deploy now),
the timeline tightens — the four operations become live on the v0.3.0
slot within one cycle. The spirit-next slot gets the same operations
when Phase 3's nine additions land (CollectRemovalCandidates is
implicitly part of those nine — it's already in production source, so
spirit-next has to add it for parity).

If decision 6 lands at A (source-first only), the four operations sit
in source while the broader cutover plays out. This matches the
existing privacy pattern — privacy fields are in source today, not yet
live. The risk is the source-ahead-of-deploy gap accumulating.

The variant-ladder Tier-1 short-reads (Recent, Today, Lookup, etc.)
under decision 7 are the broader follow-on. Whether they land in this
slice or the next, they re-use the same SmallRecord type and the same
OutputTarget enum. Today's slice is the foundation those Tier-1 reads
build on.

The deployment-chain gap closure has its own load-bearing dependency:
the `persona-spirit-next` flake input in
`/git/github.com/LiGoldragon/CriomOS-home/flake.nix:144-145` currently
points at `github:LiGoldragon/persona-spirit?ref=main` instead of
`github:LiGoldragon/spirit-next?ref=main`. The redirect is mechanical
but pending psyche ratification.

If the psyche ratifies decision 1 at B (keep the existing combined
handler), decision 2 at A (rename ArchiveTarget → OutputTarget),
decisions 4 + 5 at the strict-directive readings, and decision 6 at B
(source-and-deploy now), the slice ships in this cycle. Estimated
effort: ~80 lines of production Rust (mostly enum rename + add Stderr
variant + add OpenEntry + add RecordDefault arm), ~60 lines of new
boundary tests, schema mirror to spirit-next when Phase 3 lands.

If the psyche ratifies decision 1 at A (split into pure-extract), the
slice is a larger architectural change: the existing combined handler
shrinks, a multi-remove flow gets designed, and the safety property of
archive-before-retract has to be re-derived from two-call coordination
instead of one-call atomicity. Estimated effort: ~250 lines of
production Rust, ~150 lines of test Rust, plus a separate design pass
on the multi-remove follow-on.

The cross-lane convergence pattern from report 56 §"Section 4" continues
today: the system-operator lane is independently arriving at the same
shape via report 189 — the contract-shape review and archive-policy
review both ratify the existing combined-handler design with minor
refinements. Three lanes (this analysis, the operator-vision sibling,
and the system-operator parallel work) reach consonant conclusions on
the load-bearing reshape questions. That convergence IS the correctness
signal per the pattern designer 461 named.

## See also

- `/home/li/primary/reports/system-designer/57-spirit-engine-variant-and-collect-vision-2026-06-03/0-frame-and-method.md`
  — the meta-report frame
- `/home/li/primary/reports/system-designer/57-spirit-engine-variant-and-collect-vision-2026-06-03/1-operator-vision.md`
  — the operator-vision sibling sub-agent report
- `/home/li/primary/reports/system-operator/189-production-spirit-collect-removal-candidates-2026-06-03/0-frame-and-method.md`
  — the parallel system-operator lane working the same operation today
- `/home/li/primary/reports/system-operator/189-production-spirit-collect-removal-candidates-2026-06-03/1-contract-shape-review.md`
  — the contract-shape sidecar (independent ratification of the
  existing operation's shape)
- `/home/li/primary/reports/system-operator/188-component-data-archival-and-garbage-collection-2026-06-03.md`
  — the lifecycle research that frames today's archive-then-collect
  direction
- `/home/li/primary/reports/system-operator/182-spirit-privacy-and-shorthand-interface-audit-2026-06-02.md`
  — the privacy implementation state and shorthand-interface direction
- `/home/li/primary/reports/system-designer/55-spirit-variant-ladder-design-research-2026-06-02.md`
  — the variant-ladder design with empirical corpus mining
- `/home/li/primary/reports/system-designer/56-psyche-meta-report-spirit-recent-work-2026-06-03.md`
  — the recent psyche-style meta-report
- `/home/li/primary/reports/system-designer/53-spirit-next-production-parity-2026-06-02/5-overview.md`
  — the deployment-chain gap synthesis
- `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs` —
  the existing wire types
- `/git/github.com/LiGoldragon/signal-persona-spirit/spirit.schema` —
  the schema declaration
- `/git/github.com/LiGoldragon/persona-spirit/src/store.rs` — the
  daemon-side store with the existing CollectRemovalCandidates handler
- `/git/github.com/LiGoldragon/persona-spirit/src/observation.rs` —
  the Command / Effect projection layer with the existing handler
- `/git/github.com/LiGoldragon/persona-spirit/src/actors/dispatch.rs`
  — the dispatch fan-out
- `/git/github.com/LiGoldragon/spirit-next/schema/lib.schema` — the
  schema-derived pilot's schema for the parallel additions
- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix` — the flake
  input that points the spirit-next slot at the wrong repository
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix`
  — the deploy chain with the per-version slot infrastructure
