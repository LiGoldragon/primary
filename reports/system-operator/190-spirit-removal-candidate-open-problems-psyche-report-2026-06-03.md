# Spirit Removal-Candidate Collection Open Problems - Psyche Report

Kind: psyche-facing operator report

Topics: spirit, removal-candidates, archival, shorthand, deployment, authorization

Date: 2026-06-03

## Purpose

This report shows the open problems left after the production-source
implementation of Spirit `CollectRemovalCandidates`.

Load-bearing intent:

- [Production Spirit should implement an explicit collect-removal-candidates operation that archives or emits reviewed Zero-certainty records before retracting them from the hot store.]
- [Spirit removal-candidate collection should support an explicit output target for archive material, such as a file path or process stream, so another component can preserve the compact valued representation before hot-store removal.]
- [Common Spirit operations should have short default forms that lower to the full data types, so agents do not have to compose every rarely-configured field for routine calls.]

The source implementation exists and tests pass. The remaining problems
are about whether this is the exact shape we want to make live, and how
to keep the operation from quietly becoming a dangerous bulk-delete
surface.

## Current Source State

Production source now has the following:

- `signal-persona-spirit` commit `a69769b3`: ordinary signal operation
  `CollectRemovalCandidates`, `ArchiveTarget::{Inline, File}`, typed
  reply `RemovalCandidatesCollected`.
- `persona-spirit` commit `7233075c`: runtime handler that reads exact
  `Zero` candidates, writes archive material, then retracts only after
  archive success.
- `primary` commit `144ce383`: skills and report documentation.
- Closed bead `primary-m89k`: Zero-certainty soft-removal path and
  candidate collection are now implemented in source.

What is not true yet: the installed user-profile `spirit` wrapper may
still point at an older pinned `persona-spirit` commit until CriomOS-home
updates the flake lock and the profile is activated.

## Current Flow

```mermaid
flowchart LR
    record["Intent record in hot Spirit store"]
    nominate["ChangeCertainty(record, Zero)<br/>recoverable nomination"]
    query["CollectRemovalCandidates<br/>query must be Exact Zero"]
    archive{"Archive target"}
    inline["Inline reply<br/>caller-visible typed material"]
    file["File(path)<br/>daemon writes NOTA archive"]
    retract["Retract records from hot store"]
    skipped["Skipped candidates<br/>records remain queryable"]

    record --> nominate --> query --> archive
    archive --> inline --> retract
    archive --> file --> retract
    archive -->|write failure| skipped
```

This is a safe first source implementation for archive-before-retract.
The important caveat is that the operation is not a pure extraction
operation. It is a maintenance sweep: if the archive step succeeds, the
records leave the hot database.

## Open Problem Map

```mermaid
flowchart TB
    center["CollectRemovalCandidates<br/>source implemented"]

    deploy["Live deployment gap<br/>profile may still run older wrapper"]
    name["Verb semantics<br/>collect sounds less destructive than retract"]
    shape["Archive record shape<br/>summary lacks date/time"]
    stream["Output targets<br/>daemon stdout is not caller stdout"]
    auth["Authorization and privacy<br/>ordinary operation can become bulk maintenance"]
    blocking["Runtime blocking<br/>file write happens inside store path"]
    test["Missing live migration tests<br/>unit tests green, profile not exercised"]
    shorthand["Short/default operations<br/>constructors exist, named signal roots do not"]

    center --> deploy
    center --> name
    center --> shape
    center --> stream
    center --> auth
    center --> blocking
    center --> test
    center --> shorthand
```

## Problem 1 - Source Complete Is Not Live

The production source is updated, but live usability depends on the
CriomOS-home pin and the user profile. The designer-side report
`reports/system-designer/57-spirit-engine-variant-and-collect-vision-2026-06-03/2-designer-psyche-analysis.md`
observed the same issue earlier: the live wrapper had not yet routed
the new operation.

Why it matters: agents reading `skills/spirit-cli.md` may try the new
operation and get an unknown-head error if the profile is stale.

Suggestion:

1. Update CriomOS-home to pin `persona-spirit` commit `7233075c`.
2. Build and activate the profile with low local build pressure.
3. Smoke-test the live wrapper with a fixture or disposable database
   before touching the real intent store.
4. Only then treat `CollectRemovalCandidates` as live operator tooling.

Recommendation: do this as an explicit deployment slice, not as an
incidental profile update.

## Problem 2 - The Name Understates Destruction

`CollectRemovalCandidates` currently means archive-and-retract. That is
useful, but the word `Collect` can read like pure extraction.

There are three coherent semantic choices:

```mermaid
flowchart LR
    zero["Zero candidates"]
    preview["PreviewRemovalCandidates<br/>extract only"]
    collect["CollectRemovalCandidates<br/>archive + retract"]
    prepare["PrepareRemovalCandidateArchive<br/>no retract"]
    commit["CommitRemovalCandidateRetraction<br/>exact prepared ids"]

    zero --> preview
    zero --> collect
    zero --> prepare --> commit
```

Suggestion:

- Keep the current operation as the maintenance sweep if the contract
  explicitly says archive-before-retract.
- Add a pure preview/read operation only if `Observe` plus exact-Zero
  query is not ergonomic enough.
- If humans or agents need to pipe archive material to external tools
  before removal, add a two-phase prepare/commit path instead of
  overloading `Collect`.

Recommendation: keep the current combined operation, but document it as
destructive maintenance and consider a stronger verb later:
`ArchiveRemovalCandidates` or `SweepRemovalCandidates`.

## Problem 3 - Archive Material May Be Too Small

The current archive material is compact `RecordSummary`: identifier,
topics, kind, description, certainty, and privacy. It does not include
daemon-stamped date/time.

The user-facing intent asked for "summaries and whatever else is
considered like the core valued part of the record." The designer-side
analysis in
`reports/system-designer/57-spirit-engine-variant-and-collect-vision-2026-06-03/2-designer-psyche-analysis.md`
argued that the small archive shape should include daemon-stamped date
and time.

Why it matters: once records leave the hot store, date/time becomes part
of the archival value. Without it, the archive preserves what was said
but not when Spirit recorded it.

Suggestion:

```mermaid
classDiagram
    class RecordSummary {
        identifier
        topics
        kind
        description
        certainty
        privacy
    }
    class RecordProvenance {
        summary
        date
        time
    }
    class RemovalArchiveRecord {
        summary
        recorded_date
        recorded_time
        collected_date
        collected_time
    }
    RecordProvenance --> RecordSummary
    RemovalArchiveRecord --> RecordSummary
```

Recommendation: upgrade archive material to `RecordProvenance` now, or
introduce `RemovalArchiveRecord` if collection time should also be
recorded. I favor `RemovalArchiveRecord` only if we want a real archive
receipt; otherwise `RecordProvenance` is enough and reuses existing
contract vocabulary.

## Problem 4 - True Stream Targets Are Not Implemented

The user asked about stdout/stderr-style output targets. The
implementation deliberately did not add them because a daemon writing to
its own `stdout` is not writing to the CLI caller's terminal or pipe.

Why it matters: a fake `StandardOutput` target would look right in the
contract while sending archive material to daemon logs or nowhere useful.

Suggestion:

- `Inline` is the correct caller-visible target for normal CLI use.
  The CLI receives typed reply material and renders it to stdout.
- `File(path)` is the correct durable first archive target.
- Real stream targets need either:
  - SCM_RIGHTS file-descriptor passing, so the daemon writes to a caller-owned descriptor;
  - two-phase prepare/commit, so the caller writes the stream and then asks the daemon to retract exact prepared identifiers;
  - ARCA archive objects, once ARCA is ready.

Recommendation: do not implement raw daemon stdout/stderr. Keep bead
`primary-flwg` open for the real design.

## Problem 5 - Privacy And Authority Are Not Settled

The operation lives in the ordinary signal contract. That makes sense
for local agent ergonomics, but it is also a bulk maintenance operation:
it removes records from the hot store after archiving.

There are two separate concerns:

- Privacy filtering: default candidate queries only touch `privacy =
  Zero`, but a caller can construct other privacy selections unless the
  runtime forbids it.
- Authority: a destructive maintenance sweep may deserve owner-channel
  authority even if single-record `Remove` remains ordinary.

Why it matters: once privacy tiers matter, collection should not
silently sweep `Personal`, `Sensitive`, or `Sealed` records because an
agent used a broad privacy selector.

Suggestion:

```mermaid
flowchart TD
    request["CollectRemovalCandidates request"]
    public["privacy Exact Zero"]
    elevated["privacy Any / AtLeast / elevated exact"]
    ordinary["ordinary channel"]
    owner["owner channel"]

    request --> public --> ordinary
    request --> elevated --> owner
```

Recommendation: before deployment, either:

1. Restrict ordinary `CollectRemovalCandidates` to both `certainty =
   Exact Zero` and `privacy = Exact Zero`; or
2. Move collection to the owner signal contract; or
3. Split it: ordinary may collect public Zero records, owner may collect
   elevated privacy records.

I favor option 3. It preserves agent ergonomics for public workspace
cleanup while respecting the privacy axis.

## Problem 6 - File Archive Writes Can Block The Store Path

The implementation writes archive material before retracting. That is
correct for safety, but it also means file output happens inside the
store command path.

Why it matters: if the archive path is slow, remote, blocked, or very
large, Spirit's store actor could be held up. This is probably fine for
small intent batches, but it is the same architectural pattern we have
learned to watch carefully: a slow side effect inside a state mutation
path.

Suggestion:

- Keep the first implementation because the batch size is expected to be
  small.
- Add a candidate-count cap or explicit limit before live deployment.
- Move larger archive work to a separate archive actor or two-phase
  prepared object when Spirit starts collecting large batches.

Recommendation: add a hard limit to the request or runtime default, even
if the first limit is generous. A destructive sweep should never be
unbounded by accident.

## Problem 7 - Some Skip Reasons Are Ahead Of The Runtime

The contract has skipped reasons:

- `ArchiveFailed`
- `RecordChanged`
- `RecordAlreadyRemoved`
- `NoLongerCandidate`

The first one is exercised. The others describe possible future
concurrency or two-phase behaviors, but the current single store actor
path may not produce them.

Why it matters: dead or unreachable variants are not fatal, but they
make the contract look more mature than the runtime.

Suggestion:

- Keep the variants if two-phase or concurrent collection is likely.
- Add tests that force each variant once the runtime can produce them.
- Until then, document that only `ArchiveFailed` is expected from the
  current source implementation.

Recommendation: keep them for now, but add a contract note in
`signal-persona-spirit/ARCHITECTURE.md` that distinguishes current
reachable skip reasons from future prepared-collection reasons.

## Problem 8 - Named Shorthand Operations Are Not Done

Short constructors exist in Rust:

- `RemovalCandidateCollection::inline()`
- `RemovalCandidateCollection::file(path)`
- compatibility decoding defaults privacy when omitted

But the user asked for short/default Spirit operations so agents do not
hand-compose full records every time. That broader ladder is not
implemented as signal roots.

Why it matters: the current NOTA call is still heavy:

```nota
(CollectRemovalCandidates (((Any []) None (Exact Zero) Any (Exact Zero) SummaryOnly) Inline))
```

That is correct but not ergonomic.

Suggestion:

Possible short roots:

```nota
(CollectRemovalCandidates Inline)
(CollectRemovalCandidates (File [/tmp/spirit-removal-candidates.nota]))
(RecordDefault ([spirit] Decision [summary] High))
(RecordPrivate ([personal] Clarification [summary] High Sensitive))
```

Recommendation: do not add many shorthand roots in production yet.
First settle the schema-derived Spirit-next operation ladder, then bring
back the minimal stable subset to production. Bead `primary-am9d` tracks
this.

## Suggested Next Sequence

```mermaid
flowchart TD
    A["1. Decide privacy/authority gate"]
    B["2. Upgrade archive payload to provenance or archive record"]
    C["3. Add bounded collection limit"]
    D["4. Update CriomOS-home pin and activate profile"]
    E["5. Smoke-test live wrapper on disposable database"]
    F["6. Mark command live in skills without deploy caveat"]
    G["7. Later: shorthand ladder + true stream target design"]

    A --> B --> C --> D --> E --> F --> G
```

My recommendation is:

1. Do not deploy the source exactly as-is until the privacy/authority
   gate is settled.
2. Upgrade archive material to include daemon-stamped date/time before
   first real use.
3. Add a runtime collection limit.
4. Deploy through CriomOS-home only after the above three are done.
5. Leave stdout/stderr and the broad shorthand ladder for separate
   follow-up work.

## Open Beads

- `primary-am9d` - Spirit named shorthand operation ladder. This covers
  explicit short/default signal roots such as `RecordDefault`.
- `primary-flwg` - true stream archive targets. This covers
  stdout/stderr-like behavior using a real protocol rather than daemon
  process streams.

## Bottom Line

The implemented code is a good first maintenance engine, but I would not
call the feature complete for live use yet. The two hardening changes I
would make before deployment are:

1. authority/privacy gating so collection cannot sweep elevated privacy
   records through an ordinary broad query;
2. provenance-rich archive material so removed records keep their
   daemon-stamped time.

After those, the existing `Inline` and `File` target model is strong
enough to use. True stream targets and named shorthand operations should
remain separate follow-up slices.
