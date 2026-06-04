# Production Spirit Feature Port Audit

Date: 2026-06-04

Role: operator

Scope: compare production `persona-spirit` against the schema-derived `spirit`
repository formerly named `spirit-next`, then classify which production
behaviors can be ported directly and which should wait for shared runtime,
library, or macro substrate.

Late input folded in:
`reports/system-designer/61-spirit-situation-projection-engine-analysis-proposals-2026-06-04.md`.

## Short Answer

The new `spirit` already has the right lean center of gravity: generated schema
types, `SignalActor`, `Nexus`, `Store`, and a small binary daemon wrapper. It is
not blocked by the production actor tree.

The direct production feature ports are:

- `ChangeCertainty`
- topic catalog observation
- identifier-range observation
- observation modes, especially summary versus provenance
- recorded capture time/provenance
- certainty filtering, if the new `Entry::magnitude` field is intended to mean
  certainty

The non-direct ports are:

- `CollectRemovalCandidates`
- `Watch` / `Unwatch`
- `Tap` / `Untap`
- owner socket and owner lifecycle
- engine-management socket
- version handover / upgrade socket / `SCM_RIGHTS` descriptor handoff
- production `State` / `Questions` behavior

Those should not be copied as component-local code. They are exactly where the
production daemon becomes large: socket supervision, fanout, handover state,
archive-before-retract policy, and actor/runtime coordination. Porting them
straight into `spirit/src/daemon.rs` or `spirit/src/nexus.rs` would recreate
the boilerplate we are trying to remove.

System-designer report 61 sharpens the strategic point: new functionality now
has a targeting decision in front of it. Either it keeps landing in production
`persona-spirit` and later gets ported again, or the projection `spirit` is
declared the forward home and production becomes fixes-only while parity lands.
My operator lean is the latter, because it prevents a double-build and keeps
the schema-derived engine from becoming permanently behind.

Archive work is also not just `CollectRemovalCandidates`. It is a lifecycle:
nominate, collect/archive, retrieve, restore, compact, purge, and possibly
tombstone. The first new implementation should not build only collection and
leave restore/privacy as afterthoughts.

## Sources Checked

- `/git/github.com/LiGoldragon/persona-spirit`
- `/git/github.com/LiGoldragon/signal-persona-spirit`
- `/git/github.com/LiGoldragon/spirit`
- `/git/github.com/LiGoldragon/triad-runtime`
- `reports/system-designer/61-spirit-situation-projection-engine-analysis-proposals-2026-06-04.md`

Primary files read:

- `persona-spirit/src/observation.rs`
- `persona-spirit/src/store.rs`
- `persona-spirit/src/daemon.rs`
- `persona-spirit/ARCHITECTURE.md`
- `signal-persona-spirit/spirit.schema`
- `signal-persona-spirit/src/lib.rs`
- `spirit/schema/lib.schema`
- `spirit/src/daemon.rs`
- `spirit/src/transport.rs`
- `spirit/src/nexus.rs`
- `spirit/src/store.rs`
- `spirit/src/config.rs`
- `spirit/ARCHITECTURE.md`
- `triad-runtime/src/lib.rs`
- `triad-runtime/src/trace.rs`

## Current New-Spirit Shape

The schema-derived `spirit` currently exposes these Signal inputs:

- `Record`
- `Observe`
- `Lookup`
- `Count`
- `Remove`
- `LookupStash`

It exposes these Signal outputs:

- `RecordAccepted`
- `RecordsObserved`
- `RecordsStashed`
- `RecordFound`
- `RecordsCounted`
- `RecordRemoved`
- `Error`
- `Rejected`

Its schema already has a useful runtime triad:

- Signal roots: `Input` / `Output`
- Nexus roots: `NexusWork` / `NexusAction`
- SEMA write roots: `SemaWriteInput` / `SemaWriteOutput`
- SEMA read roots: `SemaReadInput` / `SemaReadOutput`

The runtime code is mostly in the right places:

- `SignalActor` validates and admits generated `Input`.
- `Nexus` owns the store, mail ledger, stash table, and decision loop.
- `Store` owns redb `.sema` persistence and implements generated `SemaEngine`.
- `DaemonCommand` is the startup noun; daemon `main` is thin.

The pilot also has a useful new-only behavior: `Observe` can stash full
records and reply with `RecordsStashed`, then `LookupStash` retrieves the full
record set. Production `persona-spirit` does not have that exact slim-output
path.

## Boilerplate Posture

The new code is leaner than production in the important architectural sense:
domain behavior is not spread across a large actor tree, and most request flow
goes through generated roots and data-bearing runtime objects.

But there are still generic mechanics living in component-local code:

- `spirit/src/transport.rs` owns length-prefixed Signal frame I/O.
- `triad-runtime/src/trace.rs` independently owns another length-prefixed frame
  implementation for trace events.
- `spirit/src/daemon.rs` owns Unix socket bind/remove/accept and one-request
  stream handling.
- `spirit/src/nexus.rs` owns `ContinuationBudget` and the recursive runner
  loop that should become generated or shared runtime machinery.
- `spirit/src/store.rs` owns direct redb table/ledger scanning logic; that is
  acceptable for the pilot, but it should not grow into a general store
  framework inside the component.
- `spirit/src/bin/spirit-next.rs` still owns text CLI edge logic and
  environment-variable socket selection.

The immediate library extraction target is therefore:

- a generic length-prefixed archive frame transport in `triad-runtime`;
- a generic single-socket daemon runner in `triad-runtime`;
- a generic Nexus continuation runner, either emitted by `schema-rust-next` or
  housed in `triad-runtime` over generated traits;
- component-local methods only for actual Spirit semantics.

## Production Features Already Present

### Record

Production: `Record(Entry)` persists a typed intent record, stamped by daemon
time.

New Spirit: `Record(Entry)` persists generated `Entry` into redb and returns
`RecordAccepted(SemaReceipt)`.

State: present, but missing daemon-stamped time/provenance.

### Observe Records

Production: `Observe(Records(RecordQuery))` supports topic, kind, certainty,
recorded-time, privacy, and output mode.

New Spirit: `Observe(Query)` supports topic match, optional kind, and privacy.
It currently returns a stash handle for non-empty observations.

State: partially present.

### Lookup Exact Identifier

Production: `Observe(RecordIdentifiers((Exact id) mode))`.

New Spirit: `Lookup(RecordIdentifier)`.

State: present as a different wire shape. If compatibility matters, add a
schema alias/root for `RecordIdentifiers`; if lean correctness matters,
`Lookup` is a better exact-id verb.

### Count

Production: no direct public count root in `signal-persona-spirit`; topic
counts exist through `Observe Topics`.

New Spirit: `Count(Query)`.

State: new-spirit feature, useful to keep.

### Remove

Production: `Remove(RecordIdentifier)` retracts one record.

New Spirit: `Remove(RecordIdentifier)` retracts one record and advances the
database marker.

State: present. Production emphasizes tombstone-before-remove; new Spirit
currently leaves that discipline to caller behavior.

### Privacy Selection

Production: `PrivacySelection` defaults ordinary observation to exact `Zero`;
higher magnitudes narrow audience.

New Spirit: same directional model exists, and `PrivacySelection::default_observation_privacy()`
returns exact `Zero`.

State: present.

### Durable Marker

Production: handover marker includes commit sequence, write counter, last
record identifier, date, and time.

New Spirit: `DatabaseMarker` includes persisted commit sequence plus blake3
content digest.

State: present in a different and arguably cleaner shape for ordinary reads and
writes. It is not yet enough for production version handover.

## System-Designer 61 Integration

Report 61 adds four concrete constraints to this operator audit.

First, the projection `spirit` versus production `persona-spirit` split is now
the main risk. If archive/privacy/typed-feedback work keeps landing in
production first, then the same features must be reimplemented in the
schema-derived projection later. The cleaner route is to name projection
`spirit` as the forward home, then port production parity there in deliberate
slices.

Second, archive privacy must be part of the first archive design. If private
records can be collected into an archive database, that archive database must
preserve privacy and gate retrieval behind the same explicit privacy selectors
as the hot store. Otherwise archive retrieval becomes a privacy bypass.

Third, restore is the missing inverse operation. Production currently has
nominate and collect; a schema-derived forward implementation should add
restore so an archived record can return to the hot store through a typed
operation rather than manual re-entry.

Fourth, redb version drift matters before archive storage moves into the
projection. The new `spirit` uses `redb 2.6.3`; production/sema-engine context
in report 61 points at `redb 4.1.0`. Archive storage should not add another
database substrate until the redb generation is unified.

## Production Features Missing From New Spirit

### ChangeCertainty

Production behavior:

- `ChangeCertainty(CertaintyChange)` mutates one stored record.
- The identifier stays the same.
- Setting certainty to `Zero` makes the record visible to removal-candidate
  review.
- The production projection classifies this as SEMA `Mutate`.

Straightforwardness: high.

Port shape:

- Schema:
  - add `ChangeCertainty CertaintyChange` to `Input`;
  - add `CertaintyChanged CertaintyChangeReceipt` or reuse a direct payload;
  - add `ChangeCertainty` to `SemaWriteInput`;
  - add `ChangedCertainty` to `SemaWriteOutput`.
- Nexus:
  - `Input::ChangeCertainty(change)` maps to
    `NexusAction::CommandSemaWrite(SemaWriteInput::change_certainty(change))`.
  - `SemaWriteOutput::ChangedCertainty(receipt)` maps to
    `Output::CertaintyChanged(receipt)`.
- Store:
  - read the archived `Entry`;
  - replace only the certainty/magnitude field;
  - write the same identifier back in one redb write transaction;
  - advance commit sequence and marker.

Open naming question: new `Entry` currently has `magnitude`, while production
calls the same semantic slot `certainty`. If `magnitude` is meant to be the
canonical field, the operation name might still be `ChangeCertainty` because
the user-facing intent log calls it certainty. If not, add an explicit
`Certainty` alias and field name in schema.

### Observe Topics

Production behavior:

- `Observe Topics` returns `TopicsObserved(Vec<TopicCount>)`.

Straightforwardness: high.

Port shape:

- Schema:
  - add `Topics` or `ObserveTopics` read input/output.
  - add `TopicCount { Topic * RecordCount * }` or equivalent.
- Nexus:
  - map `Input::Observe(Observation::Topics)` or `Input::Topics` to
    `SemaReadInput::Topics`.
- Store:
  - scan records;
  - count unique topics;
  - return sorted counts for stable output.

This is a good early port because it is read-only and does not require new
runtime substrate.

### Identifier Range Observation

Production behavior:

- `Observe(RecordIdentifiers((Exact id) mode))`
- `Observe(RecordIdentifiers((Range start end) mode))`
- mode selects summaries or provenance.

Straightforwardness: medium-high.

Exact lookup already exists as `Lookup`. Inclusive range is a small store scan.
The only complication is output mode, because new Spirit does not yet store
capture time/provenance.

Lean port shape:

- Keep exact lookup as `Lookup`.
- Add `LookupRange` or `RecordIdentifiers` only if the schema wants production
  compatibility.
- Return generated `RecordSet` first.
- Add provenance mode after the entry model stores daemon-stamped time.

### Observation Modes

Production behavior:

- `SummaryOnly`
- legacy `DescriptionOnly`
- `WithProvenance`

Straightforwardness: medium.

New Spirit currently stores only `Entry` values and returns full entries or
stashed full entries. A summary is basically the same shape if new `Entry`
remains compact. Provenance requires a stamped stored record.

Port shape:

- Add `ObservationMode [SummaryOnly WithProvenance]`.
- Do not preserve `DescriptionOnly` unless compatibility requires it; production
  already treats it as legacy in tests.
- Add `StampedEntry { Entry * RecordedTime * }` or add date/time fields to the
  stored record wrapper rather than to caller-submitted `Entry`.

### Recorded Time / Provenance

Production behavior:

- Clients do not submit capture time.
- Daemon stamps records before storage.
- Provenance replies expose `date` and `time`.
- Queries can filter recorded time by `Any`, `Between`, `Since`, `Until`,
  `Recent`, `Shallow`, `Deep`, `VeryDeep`.

Straightforwardness: medium.

The code is not hard, but it changes storage format. It should be done before
the new `.sema` file is treated as canonical production storage.

Port shape:

- Store redb value as `StoredRecord { identifier, entry, recorded_time }` or
  equivalent generated noun.
- Add a daemon-side `Clock` data-bearing object or put clock ownership on
  `Store::record` through a constructor-injected clock.
- Keep time stamping out of the CLI and out of Signal input.
- Add time filters after storage shape lands.

### Certainty Filtering

Production behavior:

- `RecordQuery` carries `CertaintySelection`.
- Removal candidates are exact `Zero` certainty.

Straightforwardness: medium.

New Spirit has `Entry.magnitude` and privacy, but its `Query` filters topic,
kind, and privacy only. If `magnitude` is certainty, this is a tiny query
extension. If not, the schema needs a separate certainty field.

Port shape:

- Add `CertaintySelection [Any Exact AtMost AtLeast]`.
- Add it to `Query`.
- Extend `Entry::matches`.

### CollectRemovalCandidates

Production behavior:

- Requires exact `Zero` certainty query.
- Archives compact `RecordSummary` material before any retraction.
- `ArchiveTarget::Inline` returns the archive in the reply.
- `ArchiveTarget::File(ArchivePath)` writes a tagged `RecordsObserved` NOTA
  file and fsyncs before deletion.
- Archive failures skip deletion and return skipped candidates.

Straightforwardness: not direct.

The store mechanics are simple, but the policy is not merely a store mutation.
It is a multi-step maintenance transaction:

1. read exact-zero candidates;
2. shape compact archive material;
3. write archive material or carry it inline;
4. retract only successfully archived records;
5. return removed and skipped identifiers.

Porting this directly into `Store` would mix archive I/O, policy validation,
and durable mutation. Porting it into `Nexus` without a shared effect model
would hand-roll a multi-step workflow.

Correct port shape:

- Schema:
  - `CollectRemovalCandidates RemovalCandidateCollection`
  - `RemovalCandidatesCollected`
  - `OutputTarget` or `ArchiveTarget` split into durable archive location and
    print style, following report 61:
    - archive to default/backup/error database location;
    - print to stdout/stderr by returning typed records to the client, with no
      archive write.
  - skip reasons
- Nexus:
  - orchestrate the maintenance flow over typed actions:
    - read candidates from SEMA;
    - command an archive effect;
    - command SEMA removal for archived successes;
    - reply with collection result.
- Store:
  - expose candidate query and remove-many write behavior;
  - do not own file archive I/O.
- Runtime/library:
  - archive effect should be a shared typed effect or a small archive
    substrate, not local ad hoc file writing.
  - archive retrieval must preserve and honor privacy selectors.

This should land after the generic Nexus effect/continuation runner is no
longer component-local.

Report 61 changes the target shape from "copy production inline/file archive"
to "specialized archive sema-database plus retrieval and restore". The old
`ArchiveTarget::File` path is useful evidence, not the forward design.

### Restore

Production behavior: missing.

Straightforwardness: medium, but should be designed with collection.

Restore is the inverse of collection: read archived records from the archive
database and re-assert selected records into the hot Spirit store with typed
results. It is not required to port production parity, but it is required to
make archive/retract usable without manual reconstruction.

Correct port shape:

- archive schema stores record summaries/provenance plus original privacy;
- retrieval query honors explicit privacy selectors;
- restore command emits ordinary SEMA writes to the hot store;
- restored records receive new hot-store identifiers unless the schema
  explicitly ratifies identifier preservation.

### Watch / Unwatch

Production behavior:

- `Watch State`
- `Watch Records`
- `Unwatch State`
- `Unwatch Records`
- production currently opens and retracts typed subscriptions with snapshots;
  full live delivery is still not complete.

Straightforwardness: not direct.

This is fanout/subscription runtime work. The component-local domain part is
small: what snapshot to return and what event kinds exist. The reusable part is
larger: token minting, stream registration, stream lifetime, backpressure,
event delivery, and close semantics.

Correct port shape:

- Put generic subscription registry and fanout in `triad-runtime` or a dedicated
  signal runtime crate.
- Generated schema declares domain stream/event types.
- `Nexus` decides when events occur.
- Component code owns only snapshot and event content.

### Tap / Untap

Production behavior:

- Mandatory persona observability surface on ordinary socket.
- `Tap(ObserverFilter)` opens an observer subscription.
- `Untap(ObserverSubscriptionToken)` closes it.
- Production can shape valid-but-unimplemented replies for observer paths.

Straightforwardness: not direct.

This is also fanout/runtime substrate. It should share the same subscription
mechanism as `Watch` and should not be Spirit-local boilerplate.

### State / Questions

Production behavior:

- `State(Statement)` provisionally classifies raw psyche state into a minimum
  certainty record.
- `Observe State` reads current presence/focus.
- `Observe Questions` reads pending clarification questions.
- `Watch State` snapshots state before opening subscription.

Straightforwardness: mixed.

`State(Statement)` is domain behavior, but the current production classifier is
provisional and persona-specific. `Observe Questions` and working state are
not core record-store behavior. Porting them depends on whether new `spirit`
is still meant to own psyche working state, or whether it should stay a lean
intent-record codec/daemon and let another component own live state.

Recommendation: do not port this until the new triad boundary says where
psyche working state lives.

### RequestUnimplemented

Production behavior:

- Valid but not-yet-built request kinds can return typed
  `RequestUnimplemented`.

Straightforwardness: low value unless compatibility demands it.

Schema-derived Spirit can avoid exporting inputs it does not implement. If a
valid variant is exported before implementation, add typed
`RequestUnimplemented`; otherwise, leave it out.

### Owner Socket / Lifecycle / Bootstrap Policy

Production behavior:

- Owner socket uses `owner-signal-persona-spirit`.
- Owner requests route to `OwnerPlane`, not ordinary dispatch.
- Bootstrap policy is seeded/reloaded by owner-side authority.

Straightforwardness: not direct.

This belongs to component-triad layout: ordinary `signal-spirit`, owner
`meta-signal-spirit`, and runtime daemon. New `spirit` currently carries one
schema contract inside the daemon repo. Owner behavior should wait for the
triad split or a generated multi-signal runner.

### Engine Management Socket

Production behavior:

- Optional socket speaks `signal-engine-management`.
- Supports `Announce`, readiness, health, and `Stop`.

Straightforwardness: substrate work.

This is generic daemon lifecycle, not Spirit domain logic. It should be a
generic runner capability with component identity supplied by configuration or
generated metadata.

### Version Handover / Upgrade Socket / Descriptor Handoff

Production behavior:

- Upgrade socket speaks `signal-version-handover`.
- Handover marker checks commit sequence and last identifier.
- Readiness freezes public writes while ordinary reads continue.
- Completion closes public sockets.
- Recovery reopens writes.
- Mirror applies private stamped entries after completion.
- Persona can pass accepted public client descriptors by `SCM_RIGHTS`.

Straightforwardness: not direct.

This is the most dangerous thing to copy. It is generic hot-upgrade and
supervision machinery. It should be implemented once in a runner/versioning
layer over component-provided marker, freeze, mirror, and projection methods.

New Spirit's `DatabaseMarker` is a better base than production's marker in one
respect because it includes a content digest. But it still needs:

- previous/current schema identity;
- last record identifier or equivalent replay cursor;
- public write freeze semantics;
- private mirror write surface;
- component projection policy.

## Recommended Port Order

There are two possible orders depending on the cutover decision. My operator
lean is forward-home projection `spirit`; production `persona-spirit` should
receive only urgent correctness fixes once that is ratified.

### Projection-Forward Order

1. Rename internal package surfaces from `spirit-next` to `spirit`.

This is not a feature port, but it prevents new work from landing on stale
internal names. Current `Cargo.toml`, binary names, README, ARCHITECTURE, and
environment variables still say `spirit-next`.

2. Extract generic transport into `triad-runtime`.

Unify the length-prefixed frame logic currently duplicated in `spirit` and
`triad-runtime` trace support. Component code should provide generated
encode/decode methods; runtime owns byte framing.

3. Extract a generic single-socket runner.

Move bind/remove-stale/accept/read/handle/write lifecycle out of `spirit`.
The component supplies `Configuration`, `Engine`, input decode, and output
encode; the runner supplies daemon mechanics.

4. Move the recursive Nexus runner out of component-local code.

Either generate it from `schema-rust-next` or put a generic runner in
`triad-runtime`. Keep `Nexus::step_decide` as the component decision method.

5. Unify redb generation with the archive/sema-engine substrate.

Do this before adding archive databases to the projection. Avoid growing two
database generations in the forward stack.

6. Port `ChangeCertainty`.

This is the first high-value, low-boilerplate production feature. It proves
SEMA mutation without importing production's actor tree.

7. Port topic observation.

Simple read-only feature, useful for intent maintenance, no runtime substrate.

8. Port certainty filtering, explicit privacy selectors, and identifier ranges.

These improve operator/designer query ergonomics and prepare the removal
candidate flow.

9. Add daemon-stamped provenance.

Do this before production cutover because it changes stored record shape.

10. Add typed feedback/rejection enums through schema emission where possible.

This keeps archive/privacy outcomes typed and avoids a new local string-error
language.

11. Build archive database, retrieval, and restore as one lifecycle slice.

Archive must preserve privacy and retrieval must require explicit privacy
scope for private material.

12. Port removal-candidate collection through Nexus effects.

Only after the generic Nexus runner/effect path is ratified. Do not put archive
file I/O directly in `Store`.

13. Defer subscriptions, owner lifecycle, engine management, and version
handover to shared runtime/multi-signal work.

These are important production behaviors, but they are not Spirit-specific
enough to belong as copied daemon code.

### Production-First Order If Projection Target Is Not Ratified

If the psyche decides new functionality continues landing in production
`persona-spirit` first, use report 61's production-oriented order:

1. version honesty for `persona-spirit` and `signal-persona-spirit`;
2. typed feedback;
3. explicit privacy split;
4. archive library plus retrieval;
5. collection archiving with default/backup/error and print target;
6. restore;
7. lifecycle ladder naming.

This path is workable, but it knowingly creates a later porting obligation into
projection `spirit`.

## Concrete Nexus Mapping

### ChangeCertainty

Signal arrival:

```text
Input::ChangeCertainty(change)
  -> NexusAction::CommandSemaWrite(SemaWriteInput::ChangeCertainty(change))
```

SEMA write completion:

```text
SemaWriteOutput::CertaintyChanged(receipt)
  -> Output::CertaintyChanged(receipt)
```

Store behavior:

```text
read identifier
decode stored entry
replace certainty field
write same identifier
advance commit sequence
return receipt with DatabaseMarker
```

### Observe Topics

Signal arrival:

```text
Input::Observe(Observation::Topics)
  -> NexusAction::CommandSemaRead(SemaReadInput::Topics)
```

SEMA read completion:

```text
SemaReadOutput::TopicsObserved(topic_counts)
  -> Output::TopicsObserved(topic_counts)
```

### Identifier Range

Signal arrival:

```text
Input::LookupRange(range)
  -> NexusAction::CommandSemaRead(SemaReadInput::LookupRange(range))
```

Store behavior:

```text
scan records table in identifier order
retain start <= identifier <= end
shape summaries or provenance according to mode
```

### CollectRemovalCandidates

Nexus flow:

```text
Input::CollectRemovalCandidates(collection)
  -> SemaReadInput::RemovalCandidates(collection.query)
  -> NexusEffectCommand::ArchiveRemovalCandidates(candidates, collection.output_target)
  -> SemaWriteInput::RemoveMany(archived_successes)
  -> Output::RemovalCandidatesCollected(result)
```

This is the feature that most wants the recursive Nexus engine. It is not just
a store method.

## Dependency State Relevant To Porting

Production `persona-spirit`:

- Rust edition 2024, rust-version 1.89
- `kameo` fork branch `persona-lifecycle-terminal-outcome`
- `nota-codec`
- `signal-frame`
- `signal-executor`
- `signal-persona-spirit`
- `owner-signal-persona-spirit`
- `signal-engine-management`
- `signal-version-handover`
- `signal-sema`
- `sema-engine`
- `sema`
- `version-projection`
- `rkyv 0.8`
- `tokio 1`
- `unix-ancillary 0.2`
- `thiserror 2`

New `spirit`:

- Rust edition 2024, rust-version 1.85
- `nota-next` optional behind `nota-text`
- `rkyv 0.8`
- `redb 2.6.3`
- `blake3 1`
- `triad-runtime` optional behind `testing-trace`
- build dependencies `schema-next` and `schema-rust-next`
- dev dependency `tempfile 3`

Report 61 flags a forward-stack mismatch: the projection uses `redb 2.6.3`,
while the sema-engine/archive direction is on a newer redb generation. Treat
that as a prerequisite for archive database work rather than letting the
archive layer bake in another generation split.

The dependency direction is good: the new Spirit avoids production's actor,
signal-management, owner, version-handover, and sema-engine dependency stack
for now. Do not pull those production crates into `spirit` merely to regain
features. Port the behavior through generated schema and small runtime
libraries instead.

## Glaring Issues

1. Internal names still say `spirit-next`.

The repository was renamed to `spirit`, but package name, library name, binary
names, README, architecture title, environment variables, and several tests
still say `spirit-next`. New feature work should not deepen that mismatch.

2. `triad-runtime` is too small for the stated intent.

It only exports trace support today. The repeated length-prefix code in
`spirit/src/transport.rs` and `triad-runtime/src/trace.rs` is the proof that
runtime mechanics have not been extracted far enough.

3. `NexusEngine::decide` currently owns the generic runner loop.

The comments correctly say the loop should be generated/shared. Until that
lands, every multi-step production feature risks adding more local control
machinery.

4. New Spirit has no provenance model.

Production intent work relies on daemon-stamped date/time for provenance.
`spirit` currently stores only `Entry`, so any `WithProvenance` port requires a
storage shape change.

5. Removal-candidate collection crosses too many responsibilities.

It is the production feature most likely to create bad local code if ported
too early. It needs a typed archive/effect layer and exact-zero query support.

Report 61 makes this stronger: collection is not complete without retrieval,
restore, and archive privacy. A local `ArchiveTarget::File` clone would be
regression-shaped even if it passes tests.

6. Production handover is essential but should not be copied.

The behavior is important for deployment, but it is a daemon/versioning concern
that should be runner substrate over component hooks.

7. The cutover target is unresolved.

Without a decision that projection `spirit` is the forward home, every
production feature lands under a shadow port. This is now the largest planning
risk, not an implementation detail.

## Proposed Implementation Slice

The clean next operator implementation slice is:

1. Rename internal `spirit-next` surfaces to `spirit`.
2. Move length-prefixed frame transport to `triad-runtime`.
3. Move the basic single-socket daemon runner to `triad-runtime`.
4. Move or generate the recursive Nexus continuation runner.
5. Unify redb generation before archive storage.
6. Add `ChangeCertainty` using schema-first regeneration.
7. Add `Observe Topics`.
8. Add certainty/privacy query split and identifier ranges.

That slice ports real production behavior without importing production's
boilerplate. It also proves the correct home for later archive/retrieve/restore
and `CollectRemovalCandidates`.

## Open Questions

1. Should new `Entry.magnitude` be renamed or aliased as `certainty`?

Production uses `certainty`; user-facing Spirit records use certainty. The new
schema currently calls the field `Magnitude`. If the field is semantically
certainty, the schema should probably expose the user concept as certainty and
reuse `Magnitude` as the scalar type.

2. Should exact lookup remain `Lookup`, or should production-compatible
`Observe(RecordIdentifiers(...))` return?

`Lookup` is leaner. `RecordIdentifiers` is more compatible and supports range
with mode in one shape.

3. Does new `spirit` own psyche working state?

If yes, port `State` and `Questions`. If no, keep Spirit lean as the intent
record codec/daemon and put working state elsewhere.

4. Should removal-candidate archive target include files in the first new port?

Report 61 supersedes the old inline/file framing: the forward shape is archive
database location plus print target. Print returns typed records to the client;
the daemon does not print. Archive writes use default then backup then error.

5. Is production hot handover a runner-level requirement for every daemon?

The code shape suggests yes. If so, do not implement it in `spirit`; implement
the generic runner hooks first.

6. Is projection `spirit` the forward home for new archive/privacy/typed
feedback work?

My operator lean: yes. Production should move to fixes-only once this is
ratified, otherwise the archive/privacy thread will be built twice.

7. Does restore preserve identifiers or re-assert as new hot-store records?

Re-asserting as new records is simpler and honest about the destructive
retraction boundary. Preserving identifiers is possible but needs explicit
schema and migration rules.
