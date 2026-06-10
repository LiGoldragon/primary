# Spirit Intent Redesign Feedback Against Current Source

Reviewed target: `reports/designer/578-intent-redesign-synthesis.md`

Companions checked:

- `reports/designer/577-intent-tool-state-and-the-real-flaw.md`
- `reports/designer/579-spirit-agglomeration-pass-2026-06-10.md`
- `/git/github.com/LiGoldragon/spirit/schema/signal.schema`
- `/git/github.com/LiGoldragon/spirit/src/store.rs`
- `/git/github.com/LiGoldragon/spirit/tests/collect_removal_candidates.rs`
- `/git/github.com/LiGoldragon/spirit/tests/process_boundary.rs`

This supersedes the status-sensitive parts of
`reports/operator/351-Audit-spirit-intent-redesign-synthesis-feedback.md`.
That earlier feedback was right for the source it checked, but current Spirit
has already absorbed the certainty-query and removal-candidate collection
pieces.

## Current Read

The designer synthesis is still directionally right: Spirit should expose a
coherent live intent surface, with correction, supersession, retirement, and
guardian disagreement represented as motion around that surface rather than
as bloat inside every record.

The implementation frontier has shifted. The first blocker is no longer "query
cannot filter certainty." Current Spirit has `CertaintySelection` on `Query`,
`Query::matches` applies it to `Entry.magnitude`, ordinary observations default
to at least `Minimum`, and removal-candidate collection uses exact `Zero`.
Tests cover the critical behavior: a zero-certainty record is hidden from
ordinary observation, explicit zero-certainty queries can find it, and
collection ignores nonzero records.

So the feedback now is not "build certainty filtering." It is: do not stop
there and call the synthesis production-ready. The remaining design pressure is
around identifiers, separate weight, history, and the guardian protocol.

## Clear Attention Items

### 1. Add identifier-bearing observations before building the auditor

`Lookup` returns a `FoundRecord` with `RecordIdentifier`, but `Observe` still
returns `ObservedRecords` containing only `Entry` values. That is workable for a
human reading intent, but not for a real auditor or guardian.

The future auditor needs to say "retire these source records." The guardian
needs to say "this proposal conflicts with these records." Both need ordinary
query results that carry identifiers.

Recommendation: add a snapshot type such as
`RecordSnapshot { RecordIdentifier Entry }` and return a vector of snapshots
from the read surface used by agents. Pre-production compatibility should not
keep the identifier-less observation shape if the operational domain needs
identifiers.

### 2. Separate certainty from weight

Current source uses `Entry.magnitude` as certainty. That solves the
removal-candidate problem, but it does not solve reaffirmation.

Certainty answers "how current or trusted is this record?" Weight answers "how
much has this direction been reaffirmed, how central is it, or how often should
it win ranking?" A stale record can have high historical weight and zero current
certainty. A fresh record can be high certainty but low weight until it is
reaffirmed.

The synthesis hints at this in its `Weight` discussion, and the psyche later
made the distinction explicit. Treating one ladder as both certainty and
weight will recreate bloat: repetitions either become new records or distort
certainty.

Recommendation: add a dedicated `Weight` field or a reaffirmation-count field
before designing ranking, duplicate-folding, or guardian "already known"
behavior.

### 3. Keep live state lineage-free, but journal operations durably

The synthesis says correction events "evaporate." That is right only if it
means they do not pollute live intent queries. It is wrong if it means the
system cannot later explain what happened.

Production Spirit needs a durable operation journal or archive outside the live
intent surface for:

- which record was superseded;
- which records an auditor proposed to retire;
- which psyche confirmation authorized a retirement;
- why a guardian refused a proposal;
- how to reverse a bad supersede or bad collection.

The existing separate archive database for removal candidates is already the
right kind of split: live intent stays clean, operational history remains
recoverable.

### 4. Define the guardian as a typed signal workflow

The synthesis correctly keeps daemon judgment out of the daemon. The daemon
should store, route, subscribe, and enforce typed results; the harness/agent
does the judgment.

The missing production detail is the contract. "Guardian says yes/no with a
reason" is not enough. The system needs typed states and typed refusal reasons:
duplicate, contradiction, compound record, non-intent task state, unclear
privacy, unclear topic, insufficient retrieval, and supersede-required.

Recommendation: model pending capture as a signal workflow:

- `ProposeRecord` creates a pending proposal, not a live record.
- guardian clients subscribe to pending proposals;
- guardian clients return `CaptureVerdict`;
- the daemon admits, rejects, or asks for explicit supersede based on the typed
  verdict;
- subscribers see the later admit/reject event.

That keeps the daemon dumb while making the gate real and testable.

### 5. Park-vs-block changes the user-visible contract

The synthesis leans toward parking proposals while a guardian works. That is
probably the better production shape, but it must be explicit. A parked
proposal is not recorded intent.

If the CLI returns "pending," callers need a lifecycle: pending, admitted,
rejected, supersede-required. If the CLI blocks, the daemon now depends on live
model latency and failure. This is not an implementation detail; it is a user
contract and a reliability decision.

Recommendation: choose park, but make the pending lifecycle first-class in the
schema and subscription events.

### 6. Closed topics need a catalog and migration, not only policy

The synthesis is right that topics must become broad and curated. The source
still treats topics as strings in `Topics`, so enforcement needs a new artifact:
a topic catalog, aliases from old strings, and a migration/reclassification
tool.

This also determines how keywords work. A former topic such as a narrower
schema-language phrase should become broad topic `schema` plus a keyword or
phrase index. That mapping should be inspectable, not just left to agent prose
discipline.

Recommendation: implement closed topics as a typed catalog with an enlargement
gate. Reject unknown topics or route them into the enlargement flow.

### 7. Keyword emphasis is authoring sugar, not the whole index

Asterisk-marked keywords inside bracket strings are useful and NOTA-safe, but
they should lower into a deterministic keyword index. Otherwise ordinary prose
editing changes retrieval behavior invisibly.

Recommendation: define exact extraction and normalization rules: case folding,
phrase units, duplicate handling, literal asterisk handling, and whether keyword
matches rank or filter. Keep full-text search as the recall floor.

### 8. Kind reduction needs a migration pass

Removing `Correction` from live intent state is conceptually right if
correction becomes an event. `Clarification` is less settled because some
existing clarification records are probably forward arrows under a weak label,
while others are conversation residue.

Recommendation: do not shrink `Kind` only by editing the enum. First migrate
existing records:

- fold clear corrections into current forward records and journal the
  supersession;
- rewrite forward clarifications as `Decision`, `Principle`, or `Constraint`;
- keep `Clarification` only if it gets a precise forward-only definition.

## Updated Build Order

1. Keep the current certainty-filtering and collection behavior; it is the right
   base and already has witnesses.
2. Add identifier-bearing observation snapshots.
3. Add `Weight` or reaffirmation count separate from certainty.
4. Add a durable operation journal/archive outside live intent queries.
5. Define pending capture and guardian verdict signal types.
6. Add the topic catalog and old-topic migration map.
7. Add deterministic keyword extraction/indexing.
8. Migrate `Correction` and inspect `Clarification`.
9. Then wire guardian harness clients onto the pending-proposal stream.

## Net Feedback

`578` should stay as the philosophical architecture: state is rest, stream is
motion, guardian prevents new bloat, auditor distills old bloat.

The part that clearly needs attention is the contract layer. Current Spirit has
already implemented the immediate certainty-selection gap, so the next danger is
building a guardian around an observation surface that cannot name records, a
single magnitude field doing two jobs, and a "pending" lifecycle that callers
cannot reason about.
