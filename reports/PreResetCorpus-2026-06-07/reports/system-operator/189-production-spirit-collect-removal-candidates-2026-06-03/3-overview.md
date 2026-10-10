# Production Spirit Collect Removal Candidates Overview

## Locator

Implementation session for Production Spirit removal-candidate collection.

Reports in this meta-report:

- `0-frame-and-method.md` — operator frame and first design.
- `1-contract-shape-review.md` — sidecar contract review.
- `2-archive-policy-and-test-review.md` — sidecar archive/test review.
- `3-overview.md` — this synthesis.

## Intent

- [Production Spirit should implement an explicit collect-removal-candidates operation that archives or emits reviewed Zero-certainty records before retracting them from the hot store.]
- [Spirit removal-candidate collection should support an explicit output target for archive material, such as a file path or process stream, so another component can preserve the compact valued representation before hot-store removal.]
- [Common Spirit operations should have short default forms that lower to the full data types, so agents do not have to compose every rarely-configured field for routine calls.]

## Design Decision

The implemented production shape is:

```nota
(CollectRemovalCandidates (((Any []) None (Exact Zero) Any (Exact Zero) SummaryOnly) Inline))
(CollectRemovalCandidates (((Any []) None (Exact Zero) Any (Exact Zero) SummaryOnly) (File [/tmp/spirit-removal-candidates.nota])))
```

The sidecars both found that daemon stdout/stderr are ambiguous: a daemon writing to its process stream is not the caller's shell stdout. The implementation therefore uses:

- `ArchiveTarget::Inline` for caller-visible typed archive material in the reply.
- `ArchiveTarget::File(ArchivePath)` for safe daemon-side archive-before-retract.

Raw `StandardOutput` and `StandardError` were deliberately not added. They need either caller-owned file-descriptor passing or a two-phase prepare/commit protocol before they can be true archive targets.

## Implemented Contract

Repository: `/git/github.com/LiGoldragon/signal-persona-spirit`

Added ordinary contract types:

- `ArchivePath`
- `ArchiveTarget::{Inline, File(ArchivePath)}`
- `RemovalCandidateCollection`
- `RemovalCandidateSkipReason::{ArchiveFailed, RecordChanged, RecordAlreadyRemoved, NoLongerCandidate}`
- `SkippedRemovalCandidate`
- `RemovalCandidatesCollected`

Added operation and reply:

- `Operation::CollectRemovalCandidates(RemovalCandidateCollection)`
- `Reply::RemovalCandidatesCollected(RemovalCandidatesCollected)`

Added short/default constructors:

- `RemovalCandidateCollection::inline()`
- `RemovalCandidateCollection::file(path)`
- `RemovalCandidateCollection::new(record_query, archive_target)`

Critical contract method:

- `RemovalCandidateCollection::is_exact_zero_candidate_query()`

This makes the exact-`Zero` requirement available to the runtime without reinterpreting contract internals.

Contract commit pushed:

- `a69769b3` — `signal-persona-spirit: add removal candidate collection`

## Implemented Runtime

Repository: `/git/github.com/LiGoldragon/persona-spirit`

Runtime changes:

- `Command::CollectRemovalCandidates(RemovalCandidateCollection)` lowers from the new ordinary operation.
- `Effect::RemovalCandidatesCollected(RemovalCandidatesCollected)` projects as `Retracted`.
- `DispatchPhase` routes the command to `RecordStore`.
- `RecordStore` reads candidates through the Sema reader trace plane, writes archive material, then uses the Sema writer trace plane only when records are actually retracted.
- `SpiritStore::collect_removal_candidates` rejects non-exact-`Zero` queries.
- `ArchiveTarget::File` writes a tagged `RecordsObserved [...]` NOTA value before retraction.
- Archive write failure returns `RemovalCandidatesCollected` with `ArchiveFailed` skipped candidates and retracts nothing.

The runtime dependency lock now pins `signal-persona-spirit` to `a69769b3`.

Runtime commit pushed:

- `7233075c` — `persona-spirit: collect removal candidates`

## Tests Added

Contract tests:

- Operation round-trip for inline and file archive targets.
- Reply round-trip carrying compact `RecordSummary` archive material.
- `OperationKind::CollectRemovalCandidates`.
- Generated handler witness update.
- Canonical NOTA examples.

Runtime tests:

- Store collects only exact-`Zero` candidates and preserves non-Zero records.
- Store rejects broad/non-Zero collection queries without retracting.
- Store archive failure returns skipped candidates and preserves records.
- Actor runtime archives to file before retraction and traces reader before writer.
- CLI boundary collects exact-`Zero` candidates to file before removing them.
- CLI boundary archive failure returns `(RemovalCandidatesCollected ([] [] [(1 ArchiveFailed)]))` and preserves candidates.
- Sema projection classifies collection as `Retract` / `Retracted`.

## Verification

Commands run:

```sh
cd /git/github.com/LiGoldragon/signal-persona-spirit
CARGO_BUILD_JOBS=2 cargo test

cd /git/github.com/LiGoldragon/persona-spirit
cargo update -p signal-persona-spirit
CARGO_BUILD_JOBS=2 cargo test collect
CARGO_BUILD_JOBS=2 cargo test
```

Results:

- `signal-persona-spirit`: all tests passed.
- `persona-spirit`: all tests passed.

## Documentation Updated

Contract repo:

- `/git/github.com/LiGoldragon/signal-persona-spirit/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-persona-spirit/INTENT.md`
- `/git/github.com/LiGoldragon/signal-persona-spirit/skills.md`

Runtime repo:

- `/git/github.com/LiGoldragon/persona-spirit/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/persona-spirit/INTENT.md`
- `/git/github.com/LiGoldragon/persona-spirit/skills.md`

Workspace skills:

- `/home/li/primary/skills/spirit-cli.md`
- `/home/li/primary/skills/intent-maintenance.md`

## Remaining Design Gap

True stdout/stderr archive targets are not implemented. The current `Inline` target is the correct caller-visible replacement for normal CLI use. If future work needs real stream targets, the design should use one of:

- two-phase prepare archive material, caller writes stream, then commit exact prepared identifiers;
- SCM_RIGHTS file-descriptor passing so the daemon writes to caller-owned descriptors;
- ARCA archive objects once ARCA is ready.

Until then, daemon process streams must not be represented as caller stdout/stderr.
