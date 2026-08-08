# Contract Shape Review

## Scope

Sidecar review of
`reports/system-operator/189-production-spirit-collect-removal-candidates-2026-06-03/0-frame-and-method.md`
against the current `signal-persona-spirit` ordinary contract.

Read surfaces:

- `/home/li/primary/AGENTS.md`
- `/home/li/primary/skills/reporting.md`
- `/home/li/primary/skills/contract-repo.md`
- `/home/li/primary/skills/component-triad.md`
- `/home/li/primary/skills/architectural-truth-tests.md`
- `/home/li/primary/skills/nota-design.md`
- `/git/github.com/LiGoldragon/signal-persona-spirit/skills.md`
- `/git/github.com/LiGoldragon/signal-persona-spirit/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs`
- `/git/github.com/LiGoldragon/signal-persona-spirit/examples/canonical.nota`
- `/git/github.com/LiGoldragon/signal-persona-spirit/tests/round_trip.rs`
- `/git/github.com/LiGoldragon/signal-persona-spirit/tests/short_header.rs`
- `/git/github.com/LiGoldragon/signal-persona-spirit/spirit.schema`

Load-bearing intent:

- [Production Spirit should implement an explicit collect-removal-candidates operation that archives or emits reviewed Zero-certainty records before retracting them from the hot store.]
- [Spirit removal-candidate collection should support an explicit output target for archive material, such as a file path or process stream, so another component can preserve the compact valued representation before hot-store removal.]
- [Common Spirit operations should have short default forms that lower to the full data types, so agents do not have to compose every rarely-configured field for routine calls.]

## Headline

The operation belongs beside ordinary `Remove` and
`ChangeCertainty`, but the frame shape needs three adjustments before
implementation:

1. The request payload should be a named product record, not an
   anonymous tuple in prose.
2. The output choice should distinguish archive destination from
   caller rendering; raw `StandardOutput` / `StandardError` in a
   daemon contract is ambiguous.
3. The receipt needs typed skipped reasons, not only a third vector of
   opaque identifiers.

The existing `RecordQuery` should stay the selector substrate, but the
daemon must force or validate `certainty_selection == Exact(Zero)`.
The collection operation must never let an arbitrary `RecordQuery`
remove non-`Zero` records.

## Proposed Contract Adjustment

Add a data-bearing operation variant:

```rust
Operation::CollectRemovalCandidates(RemovalCandidateCollection)
```

The operation name is acceptable: `Collect` is the contract-local verb
and `RemovalCandidates` names the domain object. It also mirrors the
existing `ChangeCertainty` maintenance verb.

Add a request payload:

```rust
pub struct RemovalCandidateCollection {
    pub query: RecordQuery,
    pub target: ArchiveTarget,
}
```

`ArchiveTarget` is a better name than `ArchiveOutput` because the enum
chooses where compact archive material goes. `Output` collides
mentally with Signal replies and with CLI stdout.

Recommended target enum:

```rust
pub enum ArchiveTarget {
    Inline,
    File(ArchivePath),
}
```

`Inline` means the daemon returns the compact archive material as typed
reply data; the CLI can then render that material to stdout. This is
the clean way to satisfy "stdout" behavior without commanding the
daemon to write into its own systemd/service stdout stream.

If the implementation keeps process streams, make them explicit:

```rust
pub enum ArchiveTarget {
    Inline,
    ProcessStream(ProcessStream),
    File(ArchivePath),
}

pub enum ProcessStream {
    StandardOutput,
    StandardError,
}
```

That still needs daemon-side documentation: these streams are the
daemon process streams, not the caller's terminal. For ordinary CLI use
`Inline` is the better first target.

`ArchivePath` should be a transparent string newtype in the contract:

```rust
pub struct ArchivePath(String);
```

Do not put `PathBuf` in the contract vocabulary. Runtime code can
project `ArchivePath` into `PathBuf` inside `persona-spirit`.

Add a reply payload:

```rust
pub struct RemovalCandidatesCollected {
    pub archived: Vec<RecordIdentifier>,
    pub removed: Vec<RecordIdentifier>,
    pub skipped: Vec<SkippedRemovalCandidate>,
    pub inline_archive: Vec<RecordSummary>,
}
```

`inline_archive` is empty unless `ArchiveTarget::Inline` was requested.
If the main implementation wants the archive material to be provenance
rich later, use a separate enum such as `ArchivedRecord::Summary` /
`ArchivedRecord::Provenance`. Do not encode ad hoc text strings as the
typed reply material.

Add skipped metadata:

```rust
pub struct SkippedRemovalCandidate {
    pub identifier: RecordIdentifier,
    pub reason: RemovalCandidateSkipReason,
}

pub enum RemovalCandidateSkipReason {
    ArchiveFailed,
    RecordChanged,
    RecordAlreadyRemoved,
    NoLongerCandidate,
}
```

The current frame's three vectors are too weak. If a record is skipped,
the caller needs to know whether archive emission failed, the record
changed away from `Zero`, or the record disappeared under concurrent
maintenance.

## NOTA Shape

Canonical request with inline archive material:

```nota
(CollectRemovalCandidates (((Any []) None (Exact Zero) Any (Exact Zero) SummaryOnly) Inline))
```

Canonical request with a file target:

```nota
(CollectRemovalCandidates (((Any []) None (Exact Zero) Any (Exact Zero) SummaryOnly) (File [/tmp/spirit-removal-candidates.nota])))
```

Canonical reply with inline summaries:

```nota
(RemovalCandidatesCollected ([1] [1] [] [(1 [workspace] Correction [candidate description] Zero Zero)]))
```

Canonical reply with one skipped record:

```nota
(RemovalCandidatesCollected ([] [] [(1 NoLongerCandidate)] []))
```

These examples follow current NOTA rules:

- `RemovalCandidateCollection` is a struct payload, so it is untagged
  inside the data-carrying operation variant.
- `Inline` is a unit enum variant.
- `(File [/tmp/...])` is a data-carrying enum variant.
- `ArchivePath` is a bracket string.
- `SkippedRemovalCandidate` is a struct, so each vector element is
  `(1 NoLongerCandidate)`, not `(SkippedRemovalCandidate 1 ...)`.

## Query Constraint

`RecordQuery` already carries the useful selector axes:

- topic selection: `Any`, `Partial`, `Full`
- kind: `Option<Kind>`
- certainty selection
- recorded time selection
- privacy selection
- mode

Use it, but do not trust all of it.

The collection operation should either:

1. Reject any request whose `query.certainty_selection` is not
   `Exact(Zero)`, or
2. Intersect the supplied query with `Exact(Zero)` before executing.

The first implementation should reject. It keeps the contract honest:
`CollectRemovalCandidates` collects candidates; a request asking for
`Any`, `AtMost(Low)`, or `AtLeast(Medium)` is malformed for this
operation even though those selectors are valid for `Observe`.

`RecordQuery::removal_candidates(ObservationMode::SummaryOnly)` is the
right constructor for the canonical example. Add a constructor on
`RemovalCandidateCollection` that uses this default and a target, so
the production CLI can expose a short/default command without agents
hand-composing the full six-field query.

## Derive And Type Requirements

Every new wire/text type needs the same derives used around the
current contract:

- `Archive`
- `RkyvSerialize`
- `RkyvDeserialize`
- `NotaRecord`, `NotaEnum`, or `NotaTransparent` as appropriate
- `Debug`
- `Clone`
- `PartialEq`
- `Eq`
- `Hash` / `Copy` only where the payload shape supports it

Likely derive mapping:

- `ArchivePath`: `NotaTransparent`, `Clone`, `PartialEq`, `Eq`, `Hash`
- `ArchiveTarget`: `NotaEnum`, `Clone`, `PartialEq`, `Eq`
- `ProcessStream`: `NotaEnum`, `Copy`, `Hash`
- `RemovalCandidateCollection`: `NotaRecord`, `Clone`, `PartialEq`, `Eq`
- `RemovalCandidatesCollected`: `NotaRecord`, `Clone`, `PartialEq`, `Eq`
- `SkippedRemovalCandidate`: `NotaRecord`, `Clone`, `PartialEq`, `Eq`
- `RemovalCandidateSkipReason`: `NotaEnum`, `Copy`, `Hash`

Keep all constructors and behavior as associated methods on real
data-bearing types. This crate already has a few test free functions,
which are allowed in `#[cfg(test)]` / test modules; production source
should not add free helpers.

## Required Contract Tests

Update `tests/round_trip.rs`:

- Import all new types.
- Add `Operation::CollectRemovalCandidates(...)` to
  `spirit_requests_round_trip`.
- Add `Reply::RemovalCandidatesCollected(...)` to
  `spirit_replies_round_trip`.
- Add a `round_trip_nota` witness for the inline request.
- Add a `round_trip_nota` witness for the file request.
- Add a `round_trip_nota` witness for the collected reply.
- Add a `round_trip_nota` witness for a skipped candidate with reason.
- Extend `spirit_request_exposes_contract_owned_kind` with
  `OperationKind::CollectRemovalCandidates`.

Update `tests/short_header.rs`:

- Add `handle_collect_removal_candidates` to `DispatchWitness`.
- Assert `OperationKind::CollectRemovalCandidates` is dispatched.
- Add or update a short-header witness for the new operation. Do not
  rely only on successful compile; the point of this test is that the
  schema-derived header remains peekable and contract-owned.

Update `examples/canonical.nota` with every new canonical line used by
`round_trip_nota`; the helper already asserts each expected line exists
in the example file.

Update `spirit.schema`:

- Add `(CollectRemovalCandidates (RemovalCandidateCollection))` to the
  operation root.
- Add `CollectRemovalCandidates ((RemovalCandidateCollection))` to the
  type map.
- Add `RemovalCandidateCollection`, `ArchiveTarget`, `ArchivePath`,
  `RemovalCandidatesCollected`, `SkippedRemovalCandidate`, and
  `RemovalCandidateSkipReason`.
- Add `CollectRemovalCandidates` to `OperationKind`.
- Add `RemovalCandidatesCollected` to the `Reply` set.

The older `schema/signal-persona-spirit.concept.schema` is visibly
stale relative to production: it lacks `Remove`, `ChangeCertainty`,
privacy, time filters, and the current `Magnitude` ordering. Either
mark it as concept-only in the implementation report or update it in a
separate cleanup. Do not let it be cited as the production schema
source for this operation.

## SEMA Classification

The frame's `Retract` classification is acceptable for the ordinary
contract. The operation removes candidates from the hot intent store
after archive emission succeeds, so the visible store effect is
retraction.

If the runtime wants to publish richer observation later, that belongs
in daemon-side command/effect projection, not in this contract as an
executable SEMA payload. The current architecture is explicit:
contract operation first, component command second, SEMA
classification third.

## Main Implementation Risks

The biggest contract risk is stdout/stderr confusion. A CLI stdout
target and a daemon stdout target are not the same thing. If the user
expects `spirit "(CollectRemovalCandidates ...)"` to print archive
records to the terminal, model that as `ArchiveTarget::Inline` and let
the CLI render the reply.

The second risk is accidental non-candidate collection. Because
`RecordQuery` is broad enough for ordinary observation, the runtime
must reject or override any non-`Exact(Zero)` certainty selector. A
test in `persona-spirit` should create both `Zero` and `Minimum`
records and prove only `Zero` is archived and removed.

The third risk is pretending the contract test proves archive ordering.
`signal-persona-spirit` can prove names, wire shape, rkyv, NOTA, and
dispatch. Archive-before-retract is a runtime truth and must be tested
in `persona-spirit` through store/actor/boundary tests.

## Recommended First Landing

Land the ordinary contract with:

- `CollectRemovalCandidates(RemovalCandidateCollection)`
- `ArchiveTarget::{Inline, File(ArchivePath)}`
- `RemovalCandidatesCollected` with `archived`, `removed`, `skipped`,
  and `inline_archive`
- skipped reasons
- exact-`Zero` validation documented in architecture
- rkyv and NOTA round trips
- short-header dispatch witness
- schema and canonical example updates

Defer daemon process streams until the CLI/daemon stream distinction is
settled. The inline target gives the user a practical stdout path while
keeping the ordinary Signal contract honest.
