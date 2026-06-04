# Spirit Privacy, Archive, And Versioning Followup - 2026-06-04

Kind: followup report

Topics: spirit, privacy, archive, versioning, designer-59

## What Changed In The Psyche Direction

This report follows
`reports/system-designer/59-design-to-implementation-audit-2026-06-04/5-psyche-report.md`
and my prior system-operator report
`reports/system-operator/191-production-spirit-privacy-and-shorthand-situation-2026-06-04.md`.

The psyche gave new direction on four points:

- Versioning must become normal discipline: code and logic changes bump
  component versions instead of leaving binaries on stale versions like
  `0.3.0`.
- `CollectRemovalCandidates` should automatically archive collected
  records before hot-store removal. The long-term archive shape should
  be typed, likely a dedicated SEMA archive store for that object kind,
  with retrieval tooling rather than loose ad hoc files.
- Spirit read surfaces should default to `privacy = Zero`, and any
  elevated privacy read should be an explicit query shape.
- Spirit status/output should be represented as self-describing NOTA
  enums and structs rather than long free-text messages.

## Effect On Designer 59 Decision Queue

### D1 — CollectRemovalCandidates

The psyche direction leans strongly toward Reading B: a combined
archive-then-retract operation. It does not mean "pure extract only".
The missing part is the archive substrate: the operation should not rely
only on caller-provided files. It should have a default archive surface,
then possibly a backup surface if the primary archive cannot be written.

### D2 — Output Target And Messages

The direction weakens the case for process-stream `Stdout` and `Stderr`
as daemon semantics. The important thing is typed output. A daemon reply
should say what happened with variants and records, for example:

```nota
(RemovalCandidatesCollected
  (ArchiveCreated ...)
  [removed-identifiers]
  [skipped-candidates])
```

The exact names should be designed, but the principle is settled:
structured values first; explanatory strings only for genuinely
unstructured external errors.

### D3 — Small Record And Archive Record

The archive store needs an archive-record type, not just an ephemeral
`RecordSummary`. It should carry enough data to retrieve and understand
what left the hot store, including privacy classification. Omitting
privacy would make the archive less trustworthy for future private use.

### D4 — RecordDefault

The prior `RecordDefault` question remains: older intent listed
magnitude as a customized field, but newer intent says routine certainty
should default to `Medium`. My current lean remains:

```nota
(RecordDefault ([topics] Kind [description]))
```

lowering to certainty `Medium` and privacy `Zero`.

Use full `Record` or a distinct `RecordOpen`/`RecordPrivate` shape when
certainty or privacy are intentional custom fields.

### D6 — Privacy Direction

This is now sharper: ordinary queries must show only `Zero` privacy by
default. Any request that can reveal elevated privacy needs an explicit
privacy selector in the request type. Exact/range identifier lookups,
topic counts, and subscriptions must follow the same rule.

## Skill Work Done

Created `skills/versioning.md` and indexed it in `skills/skills.nota`.
Also added it to operator and system-operator required reading.

The versioning skill distinguishes:

- component release version;
- wire contract version;
- storage schema version;
- deployment slot version.

It requires behavior-changing code or logic edits to bump the relevant
version in the same change set.

## Implementation Queue

This is operator-shaped production Spirit work, not system-operator
deployment glue:

1. Fix privacy filtering on all read surfaces, not only
   `Observe (Records ...)`.
2. Add explicit privacy selector support where elevated privacy reads are
   allowed.
3. Design and implement the default archive substrate for removal
   candidates.
4. Replace free-text operational status with typed outcome enums where
   the outcome space is known.
5. Bump `persona-spirit` and `signal-persona-spirit` versions when the
   source changes land.
6. Only then update CriomOS-home pins and deploy the new versioned
   wrapper.
