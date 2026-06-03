---
title: 1 — Operator vision for Spirit engine variants + collect + defaults
role: system-designer
variant: Design
date: 2026-06-03
topics: [spirit, variants, collect, defaults, vision]
parent_meta_report: reports/system-designer/57-spirit-engine-variant-and-collect-vision-2026-06-03
slot: 1
description: |
  Operator-perspective vision for the four new Spirit operations directed
  today — CollectRemovalCandidates, OutputTarget enum, the small record
  data type, and RecordDefault — plus the broader variant-ladder direction
  from earlier today. Shows the concrete code shape each operation lands as
  in signal-persona-spirit, persona-spirit, and spirit-next, with verbatim
  excerpts of the existing code that serves as the implementation template.
  Includes sequencing, dependencies, and open questions for the psyche.
---

# 1 — Operator vision for Spirit engine variants + collect + defaults

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
ladder — short forms with summary defaults for normal operations, complex
forms with full metadata for custom operations.] (Decision High, today)

## Current state

Spirit's working layer sits in three repositories whose shapes do not yet
agree. The production daemon `persona-spirit` carries the live wire
contract `signal-persona-spirit` at HEAD; the privacy field landed in
source weeks ahead of deploy, and the live `spirit-v0.3.0` binary still
rejects the privacy selector at the wire because the slot wrapper hasn't
been rebuilt from a privacy-aware commit. The schema-derived pilot
`spirit-next` carries a parallel wire contract in
`/git/github.com/LiGoldragon/spirit-next/schema/lib.schema`, with its own
`Lookup` / `Count` / `LookupStash` roots and a `DatabaseMarker` envelope on
every reply. The CriomOS-home deploy chain has full per-version slot
infrastructure already wired but currently points the spirit-next slot at
the wrong repository — `persona-spirit?ref=main` instead of
`spirit-next?ref=main`. Reports
`reports/system-designer/53-spirit-next-production-parity-2026-06-02/5-overview.md`,
`reports/system-operator/182-spirit-privacy-and-shorthand-interface-audit-2026-06-02.md`,
`reports/system-designer/55-spirit-variant-ladder-design-research-2026-06-02.md`,
and `reports/system-designer/56-psyche-meta-report-spirit-recent-work-2026-06-03.md`
together establish the parity picture, the privacy thread, the variant-
ladder design with corpus analysis, and the psyche-facing synthesis.

Today's four new operations land into this landscape. They share a deeper
direction: separate WHAT is being captured (small record), HOW the output
is consumed (output target), and WHICH defaults are convenient (record
default + collect). The current `Record` operation conflates all three;
the new vocabulary pulls them apart into composable pieces.

The operator implementation path is short because the existing scaffolding
is generous. Wire types live in
`/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs` as
hand-written rkyv-archived structs with `NotaEncode`/`NotaDecode`
instances. The daemon's request dispatch fans through
`persona-spirit/src/observation.rs` (Command/Effect projection) and
`persona-spirit/src/actors/dispatch.rs` (`execute_command` arm-table).
Each new operation lands as one Operation variant, one Command variant,
one Effect variant, one dispatch arm, one store handler, and one
boundary test. The pattern is mechanical once the wire types are typed.

## What lands in this slice

Four new operations + the small record + the broader variant-ladder
direction. Each section below shows where it lands, the Rust signature
that mirrors the existing patterns, the handler shape, the test shape,
and the wire interaction.

### Small record data type — lands first

The small-record type is the data shape every other operation in this
slice emits. It lands before any of the new operations because they all
reference it. The existing `RecordSummary` and `RecordProvenance` types
already carry the load-bearing fields; the new `SmallRecord` either
reuses one of them or sits alongside as a third reply-payload variant.

The existing `RecordSummary` shape at
`/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs:793-801`:

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaRecord, Debug, Clone, PartialEq, Eq)]
pub struct RecordSummary {
    pub identifier: RecordIdentifier,
    pub topics: Topics,
    pub kind: Kind,
    pub description: Description,
    pub certainty: Certainty,
    pub privacy: Privacy,
}
```

This is the six-field summary the wire emits for `(RecordsObserved ...)`.
The existing `RecordProvenance` adds date+time at
`signal-persona-spirit/src/lib.rs:803-808`:

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaRecord, Debug, Clone, PartialEq, Eq)]
pub struct RecordProvenance {
    pub summary: RecordSummary,
    pub date: Date,
    pub time: Time,
}
```

The directive's small-record list — *identifier, topics, kind,
description summary, magnitude, daemon-stamped date and time* — maps
directly to `RecordProvenance`. The privacy field is absent from that
list; the small record is shaped for **archival reading**, not for the
privacy-axis distinction.

Two implementation choices land in this slot.

**Choice A: rename and extend.** Replace `RecordSummary` with
`SmallRecord` and rework `RecordProvenance` to embed the new name.
Cleaner but disruptive — touches every reply variant that mentions
`RecordSummary`.

**Choice B: parallel type.** Add `SmallRecord` next to `RecordSummary` /
`RecordProvenance` and convert from the underlying `StoredRecord` (in
`persona-spirit/src/store.rs`) via an `impl From<&StoredRecord> for
SmallRecord`. Existing replies unchanged; the new operations emit
`SmallRecord` directly.

Choice B is the safer operator path. The new operation roots
(`CollectRemovalCandidates`, the variant-ladder short reads if they
emit small records) can wire to the new type without disturbing the
existing wire vocabulary. Once the small record proves out in usage,
choice A becomes a deliberate cleanup pass.

Insertion point in `signal-persona-spirit/src/lib.rs`, after the
`RecordProvenance` declaration at line 808:

```rust
/// Archive-shaped record carrying the core load-bearing fields plus
/// the daemon-stamped date and time. The variant-ladder short forms
/// and `CollectRemovalCandidates` emit this; archiving tools consume
/// it.
#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaRecord, Debug, Clone, PartialEq, Eq)]
pub struct SmallRecord {
    pub identifier: RecordIdentifier,
    pub topics: Topics,
    pub kind: Kind,
    pub description: Description,
    pub certainty: Certainty,
    pub date: Date,
    pub time: Time,
}

impl SmallRecord {
    pub fn new(
        identifier: RecordIdentifier,
        topics: Topics,
        kind: Kind,
        description: Description,
        certainty: Certainty,
        date: Date,
        time: Time,
    ) -> Self {
        Self { identifier, topics, kind, description, certainty, date, time }
    }
}
```

The projection from the daemon-side `StoredRecord` at
`persona-spirit/src/store.rs:414-432` mirrors the existing `summary` and
`provenance` methods — a new `small_record` method on `StoredRecord`:

```rust
impl StoredRecord {
    // ... existing summary() and provenance() methods ...

    fn small_record(&self) -> SmallRecord {
        SmallRecord {
            identifier: self.identifier,
            topics: self.entry.entry.topics.clone(),
            kind: self.entry.entry.kind,
            description: self.entry.entry.description.clone(),
            certainty: self.entry.entry.certainty,
            date: self.entry.date,
            time: self.entry.time,
        }
    }
}
```

Schema-source side: the spirit-next `schema/lib.schema:1-56` would gain a
`SmallRecord` declaration in its types block (currently the file uses an
inline `Entry` shape, line 51, but no projected reply shape). The new
declaration lands around line 51:

```
SmallRecord { RecordIdentifier * Topics * Kind * Description * Magnitude * Date * Time * }
```

The privacy field is absent — this is intentional per the directive's
field list. The small record is for archival reading; the privacy axis
lives on the full `Entry`.

Estimated size impact: ~25 lines of production Rust + ~3 lines of
schema source + ~5 lines of test fixture. Encoder/decoder derived from
`NotaRecord` macro.

### OutputTarget enum — the orthogonal axis

The `OutputTarget` enum is the trailing field on every extraction
operation. The directive: variants `Stdout`, `Stderr`, and
`File (path)`. Not a flag, not an error channel — one of the regular
operation fields.

This is a new enum without a current analog in the codebase. Existing
operations always reply back through the same socket; the daemon doesn't
choose where output goes. The new type makes output-target a first-class
piece of the request contract.

Insertion point in `signal-persona-spirit/src/lib.rs`, near the
`ObservationMode` enum at line 317-343. The enum has the same shape as
`ObservationMode` — small closed set, hand-coded `NotaEncode`/`NotaDecode`
to match the existing PascalCase + tagged-variant pattern.

```rust
#[derive(
    Archive, RkyvSerialize, RkyvDeserialize, NotaTransparent, Debug, Clone, PartialEq, Eq, Hash,
)]
pub struct OutputPath(String);

impl OutputPath {
    pub fn new(value: impl Into<String>) -> Self {
        Self(value.into())
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq, Hash)]
pub enum OutputTarget {
    Stdout,
    Stderr,
    File(OutputPath),
}

impl OutputTarget {
    pub const fn stdout() -> Self {
        Self::Stdout
    }
}

impl NotaEncode for OutputTarget {
    fn encode(&self, encoder: &mut Encoder) -> nota_codec::Result<()> {
        match self {
            Self::Stdout => encoder.write_pascal_identifier("Stdout"),
            Self::Stderr => encoder.write_pascal_identifier("Stderr"),
            Self::File(path) => {
                encoder.start_record_tagged("File", 1)?;
                path.encode(encoder)?;
                encoder.end_record()
            }
        }
    }
}

impl NotaDecode for OutputTarget {
    fn decode(decoder: &mut Decoder<'_>) -> nota_codec::Result<Self> {
        match decoder.peek_token()? {
            Some(Token::Ident(name)) if name == "Stdout" => {
                let _ = decoder.read_pascal_identifier()?;
                Ok(Self::Stdout)
            }
            Some(Token::Ident(name)) if name == "Stderr" => {
                let _ = decoder.read_pascal_identifier()?;
                Ok(Self::Stderr)
            }
            _ => {
                decoder.expect_tagged_record_start("File", 1)?;
                let path = OutputPath::decode(decoder)?;
                decoder.expect_record_end()?;
                Ok(Self::File(path))
            }
        }
    }
}
```

The hand-coded encode/decode follows the same pattern as
`ObservationMode` at lines 323-343 — bare PascalCase for the no-payload
variants, tagged-record for the variant carrying a payload. The `File`
variant is the only one with a payload, so it gets the tagged-record
treatment.

**Composition into operations** — `OutputTarget` is the **final
positional field** on extraction operations per the directive. Where it
attaches:

- `CollectRemovalCandidates` (new): yes, as the only positional field.
- Variant-ladder short reads that emit content to a target: optional.
  The current `(Recent)` / `(Today)` / `(Lookup N)` design from
  report 55 returns through the reply socket; if the directive's scope
  extends to those, each gains `OutputTarget` as a trailing field.
- `Observe (Records ...)`: existing operation — gains `OutputTarget`
  as a seventh positional field on `RecordQuery`? OR stays bare and
  the small-record variants live in new operation roots? **Open
  question — see Open Questions §1 below.**

**File-target failure modes.** A `File` variant carries a path; the
daemon attempts to open + write + close. Failure modes the daemon must
handle:

1. **Path doesn't resolve.** Parent directory missing, permission
   denied. Return a typed `OutputWriteFailed` reply variant.
2. **File exists but isn't writable.** Same handling — `OutputWriteFailed`.
3. **File created successfully.** Reply with a small acknowledgement
   carrying the record count and the absolute path. Possibly:
   `(OutputWritten (<count> [<path>]))`.

The implementation adds an `OutputWriteFailed` reply variant to the
working reply enum and a thin write-side method on a new
`OutputSink` noun-bearing struct. The actor lane is `dispatch.rs` →
new `output::OutputSink` actor → reply.

**Wire examples for each variant** (using the new
`CollectRemovalCandidates` operation as the carrier):

```
(CollectRemovalCandidates Stdout)
(CollectRemovalCandidates Stderr)
(CollectRemovalCandidates (File [/tmp/removal-candidates.nota]))
```

Estimated size: ~80 lines of production Rust (enum + path type +
encode/decode + sink actor for File variant) + ~4 lines of schema
source.

### CollectRemovalCandidates — the new top-level operation

The directive: collect all records at Zero certainty, emit their
small-record form to a configurable output target. Separates discovery
from destruction.

The existing Spirit `Operation` enum is macro-generated from the schema
declaration at `/git/github.com/LiGoldragon/signal-persona-spirit/spirit.schema:7-14`:

```
[
  (State (Statement))
  (Record (Entry))
  (Observe (Observation))
  (Watch (Subscription))
  (Unwatch (SubscriptionToken))
  (Remove (RecordIdentifier))
  (ChangeCertainty (CertaintyChange))
]
```

The seven existing operation roots produce the generated `Operation` enum
through the `signal_channel!([schema])` macro at
`signal-persona-spirit/src/lib.rs:1052`. The new operation lands by
appending a line:

```
[
  (State (Statement))
  (Record (Entry))
  (Observe (Observation))
  (Watch (Subscription))
  (Unwatch (SubscriptionToken))
  (Remove (RecordIdentifier))
  (ChangeCertainty (CertaintyChange))
  (CollectRemovalCandidates (OutputTarget))
]
```

The schema's types block at `spirit.schema:20-92` gains the
`OutputTarget` and `OutputPath` and `SmallRecord` declarations alongside
the existing `Entry` / `RecordQuery` / etc. The schema's reply block at
`spirit.schema:94-115` gains new variants:

```
(Reply
  RecordAccepted
  RecordRemoved
  StateObserved
  RecordsObserved
  RecordProvenancesObserved
  TopicsObserved
  QuestionsObserved
  SubscriptionOpened
  SubscriptionRetracted
  RequestUnimplemented
  CertaintyChanged
  RemovalCandidatesCollected      ; new
  OutputWritten                   ; new
  OutputWriteFailed)              ; new
```

`RemovalCandidatesCollected` carries a list of `SmallRecord` for the
Stdout/Stderr targets; `OutputWritten` carries an acknowledgement for
the File target. The conventional shape:

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaTransparent, Debug, Clone, PartialEq, Eq)]
pub struct RemovalCandidatesCollected(Vec<SmallRecord>);

#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaRecord, Debug, Clone, PartialEq, Eq)]
pub struct OutputWritten {
    pub record_count: u64,
    pub path: OutputPath,
}

#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaRecord, Debug, Clone, PartialEq, Eq)]
pub struct OutputWriteFailed {
    pub path: OutputPath,
    pub reason: OutputWriteFailureReason,
}

#[derive(Archive, RkyvSerialize, RkyvDeserialize, NotaEnum, Debug, Clone, PartialEq, Eq)]
pub enum OutputWriteFailureReason {
    PathDoesNotResolve,
    PermissionDenied,
    AlreadyExists,
    IoError(String),
}
```

The handler shape in `persona-spirit/src/observation.rs` mirrors the
existing `Command::ReadRecords` pattern. The current `Command` enum at
`persona-spirit/src/observation.rs:18-34` gains a new variant:

```rust
pub enum Command {
    ClassifyStatement(Statement),
    AssertEntry(signal_persona_spirit::Entry),
    RemoveRecord(RecordIdentifier),
    ChangeCertainty(CertaintyChange),
    ReadRecords(RecordObservation),
    ReadRecordIdentifiers(RecordIdentifierQuery),
    ReadTopics,
    ReadState,
    ReadQuestions,
    // ... subscription variants ...
    CollectRemovalCandidates(OutputTarget),  // new
}
```

The `Effect` enum gains a parallel variant:

```rust
pub enum Effect {
    // ... existing 12 variants ...
    RemovalCandidatesCollected(RemovalCandidatesCollected),  // new
    OutputWritten(OutputWritten),                            // new
    OutputWriteFailed(OutputWriteFailed),                    // new
}
```

The `Command::from_request` mapping at
`persona-spirit/src/observation.rs:52-82` gains an arm:

```rust
impl Command {
    pub fn from_request(request: WorkingOperation) -> Option<Self> {
        match request {
            // ... existing arms ...
            WorkingOperation::CollectRemovalCandidates(target) => {
                Some(Self::CollectRemovalCandidates(target))
            }
        }
    }
}
```

The dispatch arm in `persona-spirit/src/actors/dispatch.rs:238-264`
mirrors the existing `Command::RemoveRecord` and `Command::ReadRecords`
shape:

```rust
async fn execute_command(&self, command: Command) -> Result<CommandEffect<Command, Effect>> {
    let reply = match command.clone() {
        Command::ClassifyStatement(statement) => self.classify_statement(statement).await?,
        Command::AssertEntry(entry) => self.capture_entry(entry).await?,
        Command::RemoveRecord(identifier) => self.remove_entry(identifier).await?,
        Command::ChangeCertainty(change) => self.change_certainty(change).await?,
        Command::ReadRecords(observation) => self.observe_records(observation).await?,
        // ... existing arms ...
        Command::CollectRemovalCandidates(target) => self.collect_removal_candidates(target).await?,
    };
    Ok(CommandEffect::new(command, Effect::from_reply(reply)))
}
```

The `collect_removal_candidates` method shape — mirrors the existing
`observe_records` pattern but routes through the new `OutputSink` actor:

```rust
async fn collect_removal_candidates(&self, target: OutputTarget) -> Result<WorkingReply> {
    let trace = self.trace.snapshot();
    let pipeline = self
        .store
        .ask(store::CollectRemovalCandidates {
            target: target.clone(),
            trace,
        })
        .await
        .map_err(Self::store_send_error)?;
    let (reply, trace) = pipeline.into_parts();
    self.trace.replace(trace);
    Ok(reply)
}
```

On the store-actor side, the implementation reuses the existing
`removal_candidates` constructor — `RecordQuery::removal_candidates`
already builds the right filter at
`signal-persona-spirit/src/lib.rs:622-633`:

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

`CertaintySelection::removal_candidates()` at lines 541-544 returns
`Self::Exact(Magnitude::Zero)` — exactly the Zero-certainty filter the
directive names. The new handler method on `SpiritStore` (alongside the
existing `observe_records` at `persona-spirit/src/store.rs:141-144`):

```rust
pub fn collect_removal_candidates(&self, target: OutputTarget) -> Result<WorkingReply> {
    let query = RecordQuery::removal_candidates(ObservationMode::WithProvenance);
    let records = self.records_for_query(&query)?;
    let small_records: Vec<SmallRecord> =
        records.iter().map(|stored| stored.small_record()).collect();
    match target {
        OutputTarget::Stdout | OutputTarget::Stderr => Ok(WorkingReply::RemovalCandidatesCollected(
            RemovalCandidatesCollected::new(small_records),
        )),
        OutputTarget::File(path) => Self::write_small_records_to_file(small_records, path),
    }
}
```

The `Stdout` and `Stderr` variants emit the small records inline in the
reply — the CLI wrapper on each socket decides whether to route the
reply to standard output or standard error. The `File` variant has the
daemon write directly to disk and reply with the acknowledgement.

**Why Stdout/Stderr distinguish at the wire level rather than at the
CLI level.** The directive frames Stderr as "one option among normal
outputs, not an error channel." On a single-call CLI like spirit, the
daemon's reply normally goes to standard output. Naming Stderr as a
variant lets a caller request "put this on Stderr instead" — useful
when piping ordinary work and wanting the removal candidates surfaced
out-of-band. The CLI wrapper inspects the target field and routes
accordingly. The wire shape carries the intent; the wrapper carries it
out.

**Wire shape — example NOTA call + reply:**

```
spirit "(CollectRemovalCandidates Stdout)"
=> (RemovalCandidatesCollected [(123 [workspace nota] Decision [the description] Zero 2026 5 22 14 30 0) ...])

spirit "(CollectRemovalCandidates (File [/tmp/removal-2026-06-03.nota]))"
=> (OutputWritten (3 [/tmp/removal-2026-06-03.nota]))

spirit "(CollectRemovalCandidates (File [/no/such/dir/file.nota]))"
=> (OutputWriteFailed ([/no/such/dir/file.nota] PathDoesNotResolve))
```

**Witness test shape**, modeled on the existing
`persona_spirit_client_changes_certainty_to_zero_for_removal_candidate_review`
at `persona-spirit/tests/boundary.rs:360-388`:

```rust
#[test]
fn persona_spirit_client_collects_removal_candidates_to_stdout() {
    let fixture = StoreFixture::new("collect-removal-candidates-stdout");
    fixture
        .reply_text("(Record ([workspace] Decision [first description] Maximum))")
        .expect("first entry persisted");
    fixture
        .reply_text("(Record ([workspace] Correction [second description] Medium))")
        .expect("second entry persisted");
    fixture
        .reply_text("(ChangeCertainty (1 Zero))")
        .expect("first marked for removal");

    let collected = fixture
        .reply_text("(CollectRemovalCandidates Stdout)")
        .expect("removal candidates collected");

    assert!(collected.starts_with("(RemovalCandidatesCollected ["));
    assert!(collected.contains("(1 [workspace] Decision [first description] Zero"));
    // Second record is at Medium certainty — not a removal candidate.
    assert!(!collected.contains("(2 "));
}

#[test]
fn persona_spirit_client_writes_removal_candidates_to_file() {
    let fixture = StoreFixture::new("collect-removal-candidates-file");
    // ... record + mark as before ...

    let temp_path = format!("/tmp/persona-spirit-test-{}.nota", std::process::id());
    let acknowledgement = fixture
        .reply_text(&format!(
            "(CollectRemovalCandidates (File [{}]))",
            temp_path
        ))
        .expect("removal candidates written");

    assert!(acknowledgement.starts_with("(OutputWritten "));
    let written = std::fs::read_to_string(&temp_path).expect("file readable");
    assert!(written.contains("[workspace] Decision [first description] Zero"));
    let _ = std::fs::remove_file(&temp_path);
}

#[test]
fn persona_spirit_client_reports_output_write_failure() {
    let fixture = StoreFixture::new("collect-removal-candidates-write-failure");

    let failure = fixture
        .reply_text("(CollectRemovalCandidates (File [/proc/no-such-file]))")
        .expect("failure reply returned");

    assert!(failure.starts_with("(OutputWriteFailed "));
}
```

Estimated size impact:

- Production Rust (`signal-persona-spirit`): ~40 lines (enum, payloads,
  encode/decode).
- Production Rust (`persona-spirit/store.rs`): ~30 lines (handler
  method + file-write helper).
- Production Rust (`persona-spirit/observation.rs`): ~10 lines (Command
  + Effect variant additions).
- Production Rust (`persona-spirit/actors/dispatch.rs`): ~10 lines
  (dispatch arm + ask-store wrapper).
- Schema source (`spirit.schema`): ~6 lines (operation + reply
  variants).
- Test Rust (`tests/boundary.rs`): ~50 lines (three tests).

### RecordDefault — short-form recording

The directive: a short-form `Record` operation that injects defaults for
fields rarely customized. Topics, kind, description, magnitude come from
the call; privacy defaults to Zero; date and time stamped by the daemon
(already automatic on `Record`); any other rare-customize fields go in
with defaults.

The existing `Record` operation already daemon-stamps date+time — the
clock-actor pipeline at `persona-spirit/src/actors/dispatch.rs:273-282`
takes the bare `Entry` and produces a `StampedEntry`. The "defaults
injected" the directive names are mostly already there. The novel piece
is **privacy at Zero baked in** — letting the wire call omit the privacy
field entirely.

The existing `Entry::open` constructor at
`signal-persona-spirit/src/lib.rs:372-387` is the source-level mirror of
this idea:

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

`Entry::open` is the in-process API; `RecordDefault` is the wire-level
twin. The schema lands a new payload type — call it `OpenEntry` to match
— and a new operation root that consumes it:

Schema-source addition at `spirit.schema`:

```
[
  (State (Statement))
  (Record (Entry))
  (RecordDefault (OpenEntry))           ; new
  (Observe (Observation))
  ...
]

OpenEntry [Topics Kind Description Certainty]    ; new
```

The wire shape: four positional fields — the same four `Entry::open`
takes.

The new `OpenEntry` type lands in
`/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs` after the
existing `Entry` declaration at line 363:

```rust
/// Open-public default record entry. Carries the four fields agents
/// commonly customize. Privacy is filled with `Magnitude::Zero` at
/// decode time; date and time are stamped by the daemon.
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub struct OpenEntry {
    pub topics: Topics,
    pub kind: Kind,
    pub description: Description,
    pub certainty: Certainty,
}

impl OpenEntry {
    pub fn into_entry(self) -> Entry {
        Entry::open(self.topics, self.kind, self.description, self.certainty)
    }
}

impl From<OpenEntry> for Entry {
    fn from(value: OpenEntry) -> Self {
        value.into_entry()
    }
}

impl NotaEncode for OpenEntry {
    fn encode(&self, encoder: &mut Encoder) -> nota_codec::Result<()> {
        encoder.start_record_untagged()?;
        self.topics.encode(encoder)?;
        self.kind.encode(encoder)?;
        self.description.encode(encoder)?;
        self.certainty.encode(encoder)?;
        encoder.end_record()
    }
}

impl NotaDecode for OpenEntry {
    fn decode(decoder: &mut Decoder<'_>) -> nota_codec::Result<Self> {
        decoder.expect_positional_record_start("OpenEntry", 4)?;
        let topics = Topics::decode(decoder)?;
        let kind = Kind::decode(decoder)?;
        let description = Description::decode(decoder)?;
        let certainty = Certainty::decode(decoder)?;
        decoder.expect_record_end()?;
        Ok(Self { topics, kind, description, certainty })
    }
}
```

The encode/decode pattern mirrors the existing `Entry` encode/decode at
lines 389-422. The `expect_positional_record_start` count drops from 5
to 4 because the privacy field is absent from the wire shape.

The daemon-side handler at `persona-spirit/src/observation.rs` adds one
mapping arm — `RecordDefault` lowers to the same `Command::AssertEntry`
the canonical `Record` lowers to, after `OpenEntry::into_entry()` fills
in `privacy = Zero`:

```rust
impl Command {
    pub fn from_request(request: WorkingOperation) -> Option<Self> {
        match request {
            WorkingOperation::Record(entry) => Some(Self::AssertEntry(entry)),
            WorkingOperation::RecordDefault(open_entry) => {
                Some(Self::AssertEntry(open_entry.into_entry()))
            }
            // ... rest ...
        }
    }
}
```

That's the entire daemon-side change for `RecordDefault`. The dispatch
arm already exists (`Command::AssertEntry` → `capture_entry`). The
clock-stamp + store-write already happen. The privacy field is filled
by `Entry::open`.

**Wire example — shorter NOTA call:**

```
spirit "(RecordDefault ([workspace spirit] Decision [observation about something] Maximum))"
=> (RecordAccepted N)
```

Versus the canonical:

```
spirit "(Record ([workspace spirit] Decision [observation about something] Maximum Zero))"
=> (RecordAccepted N)
```

One fewer field per call — the agent doesn't type `Zero` for the
overwhelmingly common dev-mode public-repo case.

**Witness test shape**, modeled on the existing
`persona_spirit_client_asserts_entry_and_mints_record_identifier` at
`tests/boundary.rs:229-237`:

```rust
#[test]
fn persona_spirit_client_records_default_short_form_with_zero_privacy() {
    let fixture = StoreFixture::new("record-default-zero-privacy");

    let accepted = fixture
        .reply_text("(RecordDefault ([workspace] Decision [observation] Maximum))")
        .expect("default short-form record persisted");

    assert_eq!(accepted, "(RecordAccepted 1)");

    let observed = fixture
        .reply_text("(Observe (Records ((Any []) None Any Any (Exact Zero) SummaryOnly)))")
        .expect("zero-privacy records observed");

    assert_eq!(
        observed,
        "(RecordsObserved [(1 [workspace] Decision [observation] Maximum Zero)])"
    );
}

#[test]
fn persona_spirit_client_record_default_with_elevated_privacy_requires_full_record() {
    let fixture = StoreFixture::new("record-default-cannot-elevate");

    // Short form cannot reach elevated privacy.
    fixture
        .reply_text("(RecordDefault ([workspace] Decision [public note] Maximum))")
        .expect("public note recorded");

    // To record elevated privacy, the agent must use the full Record form.
    fixture
        .reply_text("(Record ([workspace] Decision [elevated note] Maximum High))")
        .expect("elevated note recorded");

    let elevated = fixture
        .reply_text("(Observe (Records ((Any []) None Any Any (AtLeast High) SummaryOnly)))")
        .expect("elevated records observed");

    assert_eq!(
        elevated,
        "(RecordsObserved [(2 [workspace] Decision [elevated note] Maximum High)])"
    );
}
```

Estimated size impact:

- Production Rust (`signal-persona-spirit`): ~35 lines (`OpenEntry`
  type + impls).
- Production Rust (`persona-spirit/observation.rs`): ~3 lines (one
  `from_request` arm).
- Schema source (`spirit.schema`): ~2 lines (operation root + payload
  type).
- Test Rust (`tests/boundary.rs`): ~30 lines (two tests).

### Variant-ladder Tier 1 short reads (from report 55)

The variant-ladder design at
`reports/system-designer/55-spirit-variant-ladder-design-research-2026-06-02.md`
proposes ~30 new operation roots. The most leverage-per-line is Tier 1
— six zero-argument convenience reads. Each expands deterministically
to the canonical complex form.

The existing canonical complex form at
`signal-persona-spirit/src/lib.rs:612-633`:

```rust
pub struct RecordQuery {
    pub topic_selection: TopicSelection,
    pub kind: Option<Kind>,
    pub certainty_selection: CertaintySelection,
    pub recorded_time_selection: RecordedTimeSelection,
    pub privacy_selection: PrivacySelection,
    pub mode: ObservationMode,
}
```

Three of the Tier 1 short forms shown with their canonical expansion:

**`(Recent)`** — 15 most-recent records, summary-only.

```rust
WorkingOperation::Recent => Some(Self::ReadRecords(RecordObservation {
    query: RecordQuery {
        topic_selection: TopicSelection::any(),
        kind: None,
        certainty_selection: CertaintySelection::Any,
        recorded_time_selection: RecordedTimeSelection::Recent,
        privacy_selection: PrivacySelection::default_observation_privacy(),
        mode: ObservationMode::SummaryOnly,
    },
})),
```

**`(Today)`** — records since 00:00:00 daemon-local today.

```rust
WorkingOperation::Today => {
    let today = self.clock.ask(clock::ReadCurrentDate { ... }).await?;
    let since = RecordedTime::new(today, Time::new(0, 0, 0));
    Some(Self::ReadRecords(RecordObservation {
        query: RecordQuery {
            topic_selection: TopicSelection::any(),
            kind: None,
            certainty_selection: CertaintySelection::Any,
            recorded_time_selection: RecordedTimeSelection::Since(since),
            privacy_selection: PrivacySelection::default_observation_privacy(),
            mode: ObservationMode::SummaryOnly,
        },
    }))
}
```

Note `Today` needs the clock actor for the date computation —
unlike `Recent`, which is filter-only. The Tier-1 implementation must
distinguish the static-default short forms from the dynamic-default
ones.

**`(Topics)`** — alias for `(Observe Topics)`. Pure rewrite.

```rust
WorkingOperation::Topics => Some(Self::ReadTopics),
```

These short forms can land as new variants on the `Operation` enum
(via schema additions) without touching the existing operation
shapes. The dispatch arms above slot into `Command::from_request` at
`persona-spirit/src/observation.rs:52-82` alongside the existing
arms.

**Schema additions** at `spirit.schema:7-14`:

```
[
  (State (Statement))
  (Record (Entry))
  (RecordDefault (OpenEntry))
  (Observe (Observation))
  ...
  (CollectRemovalCandidates (OutputTarget))
  Recent                                  ; new — zero positional fields
  Shallow                                 ; new
  Deep                                    ; new
  VeryDeep                                ; new
  Today                                   ; new
  ThisWeek                                ; new
  Topics                                  ; new — alias for (Observe Topics)
  (Lookup (RecordIdentifier))             ; new — alias for (Observe (RecordIdentifiers (...)))
  (LookupRange (RecordIdentifierRange))   ; new
]
```

The zero-arg variants encode/decode through the existing
`NotaEnum`-style PascalCase form — bare `Recent` on the wire. The
`Lookup` variants carry positional arguments and use the tagged-record
form.

The variant-ladder design and the new operations in this slice fit
together: `CollectRemovalCandidates` IS a variant-ladder-shape
operation (specialised short form for a common ritual), and
`RecordDefault` IS the Tier-1 form on the recording side.

## Sequencing and dependencies

The slice has a clear ordering. Some operations have prerequisites; the
order below respects them.

```mermaid
flowchart LR
    S[Schema: types + operations]
    R[Rust: lib.rs types + impls]
    H[Handlers: store + dispatch]
    T[Tests: boundary.rs]
    D[Deploy: rebuild + slot]
    S --> R
    R --> H
    H --> T
    T --> D
```

**Phase 1: Schema additions in `signal-persona-spirit`.** Land the
schema-source first per
`spirit.schema:1-117` as the contract canvas. The schema declarations
land at the right insertion points (operation root list lines 7-14,
types block lines 20-92, reply block lines 94-115):

1. `SmallRecord` type (alongside `RecordSummary`).
2. `OutputTarget` + `OutputPath` types.
3. `RemovalCandidatesCollected` + `OutputWritten` + `OutputWriteFailed`
   reply types (+ `OutputWriteFailureReason`).
4. `OpenEntry` type (for `RecordDefault`).
5. New operation roots:
   `CollectRemovalCandidates`, `RecordDefault`, and the Tier-1 short-form
   reads (`Recent`, `Shallow`, `Deep`, `VeryDeep`, `Today`, `ThisWeek`,
   `Topics`, `Lookup`, `LookupRange`).

This is a substantial schema delta (~16 declarations + 9 operation roots
+ 3 reply types) but each one is small and mechanical.

**Phase 2: Handler implementations in `persona-spirit`.**

Files touched:

- `persona-spirit/src/observation.rs` — `Command` + `Effect` enum
  additions, `Command::from_request` arms.
- `persona-spirit/src/store.rs` — `collect_removal_candidates` method,
  `StoredRecord::small_record` method, new file-write helper
  (`write_small_records_to_file`).
- `persona-spirit/src/actors/dispatch.rs` — dispatch arm for the new
  command + ask-store wrapper.
- (Possibly new) `persona-spirit/src/actors/output.rs` — the new
  `OutputSink` actor for the `File` variant. Optional — the file-write
  can also live as a synchronous helper on `SpiritStore` if it stays
  short.

Estimated total: ~250 lines of production Rust across the four files,
including the variant-ladder Tier 1 arms.

**Phase 3: Tests in `boundary.rs`.**

New tests, modeled on existing ones:

1. `persona_spirit_client_collects_removal_candidates_to_stdout`
2. `persona_spirit_client_writes_removal_candidates_to_file`
3. `persona_spirit_client_reports_output_write_failure`
4. `persona_spirit_client_records_default_short_form_with_zero_privacy`
5. `persona_spirit_client_record_default_with_elevated_privacy_requires_full_record`
6. `persona_spirit_client_recent_short_form_returns_15_most_recent`
7. `persona_spirit_client_today_short_form_uses_daemon_local_date`
8. `persona_spirit_client_lookup_short_form_returns_single_record`

Estimated total: ~250 lines of test Rust.

**Phase 4: CLI handling in the persona-spirit binaries.**

The two CLI bins at
`persona-spirit/src/bin/spirit.rs` and `persona-spirit/src/bin/spirit-next.rs`
are each one-line macro invocations:

```rust
// spirit.rs
signal_frame::signal_cli!(spirit, signal_persona_spirit);

// spirit-next.rs
signal_frame::signal_cli!(spirit_next, signal_persona_spirit);
```

The `signal_cli!` macro generates the CLI surface from the schema.
**Phase 4 is implicit** — schema changes from Phase 1 already reach the
CLI through the macro. No hand-written CLI changes needed.

**Phase 5: Parallel schema additions to `spirit-next`.**

The schema-derived pilot at
`/git/github.com/LiGoldragon/spirit-next/schema/lib.schema:1-56`
already declares `Privacy Magnitude` and `PrivacySelection` (per
report 53). To bring the new operations into the schema-derived stack,
the same additions land in the spirit-next schema. The shape mirrors
Phase 1 — `SmallRecord`, `OutputTarget`, `RecordDefault`, etc. — but
written in spirit-next's schema syntax.

The spirit-next stack regenerates its Rust through the schema-derived
emission pipeline. Test fixture work happens once the regenerated code
is current.

**Phase 6: Deployment config in `CriomOS-home` (only if wire shape
change requires it).**

The deploy chain at
`/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix`
needs an update if any of the new operations require additional
daemon-config fields. None of the four new operations DO require that —
they all consume request data through the existing socket dispatch.
The deploy work for THIS slice is: rebuild the v0.3.0 slot from a
commit that includes the new operations.

Per `spirit.nix:163-179`, the deploy chain already supports
side-by-side slot versions and a `currentDefault` switch. Once the
v0.3.0 slot is rebuilt with the new operations, the unsuffixed
`spirit` command serves them.

**Phase 7: Production cutover.**

Per `reports/system-designer/53-spirit-next-production-parity-2026-06-02/5-overview.md`
§"Path-to-ship", the Phase 5 cutover is `currentDefault = "next";`. The
new operations land on either the v0.3.0 slot (with the bigger
production cutover deferred) or on the spirit-next pilot slot (once
the slot is repointed at the actual pilot and the schema additions
land there too).

The order of landing is **source-first**, then a slot rebuild from the
new source. The deployment chain is already wired.

## Open questions

The open questions follow the new "explain opaque items in plain
terms" style — each names what the item is, why it matters, and the
options.

### 1. Where does `OutputTarget` attach on existing operations?

**What is it?** The directive says output-target is the **last
positional field on extraction operations**. The new
`CollectRemovalCandidates` operation clearly takes it. But there are
existing extraction operations — `(Observe (Records ...))` is the big
one — whose request shape is already settled at six fields. Adding
`OutputTarget` as a seventh field changes the wire of every existing
client. Alternative: the new short-form variants
(`Recent`, `Today`, etc.) carry `OutputTarget` while the canonical
`Observe` form does not.

**Why does it matter?** Wire backwards-compatibility. The existing
parser at `signal-persona-spirit/src/lib.rs:648-722` already has a
field-omission tolerance pattern (defaults injected when the request
text stops short). Extending it with one more layer is mechanical.
But each layer adds a parser arm and a documented field-order
contract.

**The options.**

- **A.** Add `OutputTarget` as a seventh field on `RecordQuery`,
  defaulted to `Stdout` when omitted. Existing clients still parse;
  new clients can supply the target.
- **B.** Leave `RecordQuery` at six fields and have the new
  short-form variants (`Recent`, `Today`, etc.) carry `OutputTarget`
  as their final positional field. The canonical form is unchanged.
- **C.** Add `OutputTarget` only on the operations the directive
  explicitly names — `CollectRemovalCandidates` and whichever future
  extraction operations explicitly extract content. Existing read
  shapes stay bare.

The directive seems compatible with B or C; A is the most uniform but
churns the existing wire. Lean: C.

### 2. Does `CollectRemovalCandidates` also Remove after extracting?

**What is it?** The directive separates discovery from destruction:
*"Separates the discovery / extraction concern from the destruction
concern in Remove."* That reads as STRICTLY EXTRACT — `Remove` stays
the only operation that actually deletes records. But a real workflow
"collect everything at Zero then remove them all" wants both steps,
and routing through two operations is more verbose. A combined
operation `(CollectAndRemoveCandidates ...)` would be a useful third
arm.

**Why does it matter?** The directive's framing — *separates the
discovery from the destruction* — reads against a combined operation.
But the practical workflow argues for it. Reading the framing as a
constraint, not just description, would forbid the combined operation
in this slice and leave it as a future variant.

**The options.**

- **A.** Strictly extract. Removing the collected records is a
  separate `(Remove N)` call per identifier. Multi-remove batching
  would need its own operation if it lands.
- **B.** Combined operation `(CollectAndRemoveCandidates target)`
  as a separate top-level root, leaving `CollectRemovalCandidates`
  pure-extract. The directive's wording reads as the pure-extract
  case; the combined case would be a sibling, not a flag.
- **C.** Single operation with a `(WithRemoval | ExtractOnly)`
  modifier as a field on the request — but that's a flag in
  disguise. The single-NOTA-argument rule forbids flags but the
  field is still typed NOTA, so this is technically legal.

The directive's wording leans toward A. The lean here is A, with B as
a future addition if and when "collect then remove" becomes a
recurring workflow.

### 3. Does the `OutputTarget::File` variant create the file if absent?

**What is it?** When the daemon receives
`(CollectRemovalCandidates (File [/tmp/removal-2026-06-03.nota]))`, it
opens the path and writes. If the file doesn't exist, the daemon could
create it (the common shell-like behavior) or could fail-on-not-exists
(safer, more predictable). If the file exists, the daemon could
overwrite, append, or fail.

**Why does it matter?** Accidental overwrites of files agents care
about. The conservative shape — fail-on-already-exists — protects
against this but means the agent must clean up between calls. The
permissive shape — create-or-overwrite — matches POSIX `open(O_TRUNC |
O_CREAT)` and is what `>` redirection does, but it's not safe.

**The options.**

- **A.** Create-or-truncate (POSIX `O_TRUNC | O_CREAT`). Matches
  shell `>` redirection. Risk: surprising overwrite.
- **B.** Create-or-fail (`O_EXCL | O_CREAT`). Agent must delete the
  file between calls. Safer, more verbose.
- **C.** Append-or-create (`O_APPEND | O_CREAT`). Each call adds to
  the file. Matches log-file semantics.
- **D.** Two separate variants — `(File path)` for create-or-fail,
  `(FileOverwrite path)` for create-or-truncate. Lets the call site
  state intent.

The lean here is D — explicit intent on the wire, no surprising
mode. The cost is one more enum variant.

### 4. What is the small record's exact field list?

**What is it?** The directive names *identifier, topics, kind,
description summary, magnitude, daemon-stamped date and time* — seven
fields. The existing `RecordProvenance` carries those plus
`privacy`. The directive's list omits `privacy` from the small
record explicitly.

**Why does it matter?** The small record is a wire-shape — every
emission of it carries those fields and only those fields. If
`privacy` is wanted later, every existing small-record emission
becomes mis-shaped against the new contract. If `privacy` is included
now and the directive truly meant to omit, every emission carries an
extra field forever.

**The options.**

- **A.** Strict directive — omit privacy entirely. Small record is for
  archival reading and the privacy axis lives on the full record.
- **B.** Include privacy on the small record. Match `RecordProvenance`'s
  existing seven-field shape with one rename.
- **C.** Two variants — `SmallRecord` strictly per the directive (no
  privacy), and `SmallPrivateRecord` with privacy for queries that
  want it.

Lean: A — the directive is specific about the field list. If privacy
matters downstream, the full record is reachable through `Lookup N`
or the canonical `Observe`.

### 5. Does `RecordDefault` allow overriding privacy?

**What is it?** The directive frames `RecordDefault` as taking *only
fields agents commonly customize — topics, kind, description, magnitude
— with defaults injected for the rest (privacy at Zero ...)*. That
reads as four fields only. But the variant-ladder design at
`reports/system-designer/55-spirit-variant-ladder-design-research-2026-06-02.md`
§"RecordOpen / RecordPersonal / RecordSealed" proposes named privacy
variants — `(RecordPersonal ...)` lowers to `Record(..., Privacy=Medium)`
and `(RecordSealed ...)` to `Record(..., Privacy=Maximum)`. Does
`RecordDefault` admit an optional fifth field that overrides privacy?

**Why does it matter?** The agent ergonomics question. If
`RecordDefault` is strict-four-fields, the agent who occasionally
wants elevated privacy must reach for the full `Record` form (more
typing) or for a named variant (`RecordSealed`). If `RecordDefault`
admits an optional privacy override, the variant family is smaller
but each call has one more decision.

**The options.**

- **A.** Strict four fields. Privacy elevation requires `Record` or a
  named variant like `RecordSealed`.
- **B.** Optional fifth field. `(RecordDefault ([topics] Kind [desc]
  Magnitude))` and `(RecordDefault ([topics] Kind [desc] Magnitude
  Privacy))` both work.
- **C.** Strict four for `RecordDefault`; add the named variants
  (`RecordSealed`, etc.) as siblings in the same slice.

Lean: A. The directive is specific. Named variants are a clean
follow-up if elevated-privacy short forms prove worth the bytes.

### 6. What's the order of landing — source-first vs deploy-first?

**What is it?** The four new operations could land in code first (with
the slot deploy following weeks later, per the existing privacy
pattern) OR could land in code AND deploy in the same cycle. The
existing privacy thread shows the source-ahead-of-deploy pattern is
already tolerated: the privacy fields landed at
`signal-persona-spirit/src/lib.rs:359-422` weeks before the v0.3.0
binary rebuilt.

**Why does it matter?** Source-first lets the design absorb feedback
before deployment costs are sunk. Source-and-deploy together makes
the new operations live for agents to use; otherwise they're
type-system facts that nobody can actually call.

**The options.**

- **A.** Source-first. Land schema + types + handlers + tests, ship
  to the repository, then redeploy later as part of a larger Phase
  2/3 cutover.
- **B.** Source-and-deploy. Land the source AND rebuild the v0.3.0
  slot from the new commit in the same cycle. The new operations
  become live immediately.
- **C.** Source-and-deploy on the spirit-next slot. Once the
  spirit-next slot is repointed at the actual pilot (per report 53
  Phase 2), the new operations land on spirit-next first and v0.3.0
  follows when the broader cutover lands.

Lean: B. The source-ahead-of-deploy pattern from the privacy thread
is the unfortunate accidental shape, not the intended one. The deploy
chain is short; rebuilding the v0.3.0 slot from a new commit is
mechanical. Letting the new operations be live as soon as their
source lands matches the rest of the workspace's discipline. Once
spirit-next is live (Phase 2), the same code rebuilt for the
schema-derived stack.

## See also

- `reports/system-designer/53-spirit-next-production-parity-2026-06-02/5-overview.md`
  — the production-parity audit synthesis. Frames the deployment slot
  gap and the parity work.
- `reports/system-operator/182-spirit-privacy-and-shorthand-interface-audit-2026-06-02.md`
  — the operator-lane parallel report establishing the source-ahead-of-
  deploy state and the shorthand-interface direction.
- `reports/system-designer/55-spirit-variant-ladder-design-research-2026-06-02.md`
  — the variant-ladder design with the empirical corpus analysis. Tier 1
  zero-argument convenience reads are the closest siblings of
  `CollectRemovalCandidates` and `RecordDefault`.
- `reports/system-designer/56-psyche-meta-report-spirit-recent-work-2026-06-03.md`
  — the recent psyche-style meta-report tying the privacy thread,
  variant ladder, and deployment-chain gap together.
- `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs` — the
  hand-written wire types. The new types land here at the insertion
  points named in each subsection above.
- `/git/github.com/LiGoldragon/signal-persona-spirit/spirit.schema` —
  the schema declaration that drives `signal_channel!`. New operation
  roots and types land here.
- `/git/github.com/LiGoldragon/persona-spirit/src/store.rs` — the
  daemon-side store. New handler methods land here.
- `/git/github.com/LiGoldragon/persona-spirit/src/observation.rs` — the
  Command / Effect projection layer. New variants land here.
- `/git/github.com/LiGoldragon/persona-spirit/src/actors/dispatch.rs` —
  the dispatch fan-out. New arms land in `execute_command`.
- `/git/github.com/LiGoldragon/persona-spirit/tests/boundary.rs` — the
  boundary tests. New tests land here, modeled on the existing fixtures.
- `/git/github.com/LiGoldragon/spirit-next/schema/lib.schema` — the
  schema-derived pilot's schema. Parallel additions land here for the
  spirit-next stack.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix`
  — the deploy chain. This slice's deploy work is: rebuild the v0.3.0
  slot from a new commit.
