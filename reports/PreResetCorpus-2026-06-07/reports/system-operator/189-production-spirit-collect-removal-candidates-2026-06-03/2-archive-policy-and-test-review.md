# Archive Policy And Test Review

## Assignment

Sidecar review for Production Spirit `CollectRemovalCandidates`.

Read surfaces:

- `AGENTS.md`
- `skills/reporting.md`
- `reports/system-operator/188-component-data-archival-and-garbage-collection-2026-06-03.md`
- `reports/system-operator/189-production-spirit-collect-removal-candidates-2026-06-03/0-frame-and-method.md`
- `/git/github.com/LiGoldragon/persona-spirit/skills.md`
- `/git/github.com/LiGoldragon/persona-spirit/ARCHITECTURE.md`
- current `persona-spirit` store, dispatch, observation, boundary, actor-runtime, and sema-projection tests
- current `signal-persona-spirit` architecture and contract tests

Central intent citations:

- [Production Spirit should implement an explicit collect-removal-candidates operation that archives or emits reviewed Zero-certainty records before retracting them from the hot store.]
- [Spirit removal-candidate collection should support an explicit output target for archive material, such as a file path or process stream, so another component can preserve the compact valued representation before hot-store removal.]
- [Common Spirit operations should have short default forms that lower to the full data types, so agents do not have to compose every rarely-configured field for routine calls.]

## Executive Finding

The archive-before-retract invariant is testable and should be made stronger than the frame currently states. `CollectRemovalCandidates` must never trust caller-provided `RecordQuery` as the complete removal selector. The operation must either enforce `CertaintySelection::Exact(Magnitude::Zero)` internally or reject any collection query whose certainty selector is not exact `Zero`.

The largest design hazard is process-stream output. A daemon operation can safely write an archive file before retracting because file writing is inside the daemon's transaction envelope. It cannot safely write to the caller's stdout or stderr before retracting because the daemon does not own the caller's process streams. If stdout/stderr output is required as real archive emission, the implementation needs either a two-phase prepare-and-commit flow or a CLI-mediated protocol that does not retract until the stream write has succeeded. Otherwise stdout/stderr can only be a display or preview mode, not an archive-before-retract collection target.

## Current Runtime Shape That Matters

Production `persona-spirit` is currently degenerate-atomic: one ordinary operation lowers to one local `Command`, and the `CommandExecutor` rejects multi-command operation plans. Existing `Remove` lowers to `Command::RemoveRecord`, routes through `RecordStore`, and does a sema `Retract`. Existing `ChangeCertainty` lowers to `Command::ChangeCertainty`, mutates the stored record, and lowering to `Zero` makes a record visible to exact-`Zero` removal-candidate review.

The contract already has the compact valued material the psyche is asking for:

- `RecordSummary` carries identifier, topics, kind, description, certainty, and privacy.
- `RecordProvenance` wraps `RecordSummary` plus daemon-stamped date and time.
- `RecordQuery::removal_candidates(mode)` already constructs an exact-`Zero` candidate query.

The collection operation therefore needs to preserve `RecordSummary` at minimum in its archive material and receipt. A receipt that contains only identifiers is too weak because it proves retraction happened, but not that the valued record material was emitted before the retraction.

## Policy Recommendations

### Use An Owning Command

Implement collection as one owning local command, for example:

```text
Command::CollectRemovalCandidates(Collection)
```

The command should internally perform:

1. read matching candidate summaries or provenances;
2. archive or emit the valued material;
3. retract only archived candidates;
4. return a typed receipt carrying archived material and skipped identifiers.

This preserves the current single-command executor discipline while making the operation internally multi-step for a real domain reason.

### Enforce Exact Zero At The Boundary

If the contract accepts a `RecordQuery`, collection must not simply execute that query. The operation should normalize or reject the certainty selector:

- acceptable: `Exact Zero`;
- rejected or forcibly intersected: `Any`, `AtMost`, `AtLeast`, `Exact Minimum`, and every non-Zero exact selector.

I recommend rejection for the first implementation because it gives tests a crisp failure shape and avoids surprising callers whose broader query is silently narrowed.

### Treat File Output As The Safe First Archive Target

`File` can satisfy archive-before-retract in a single daemon operation:

1. open the target path;
2. write the archive material;
3. flush and close or sync according to the chosen durability promise;
4. retract records;
5. return the receipt.

If the file write fails, no records are retracted.

### Do Not Pretend Daemon Stdout Is Caller Stdout

`StandardOutput` and `StandardError` are only meaningful for the CLI process. A daemon request cannot write to the caller's stdout or stderr unless the caller sent a file descriptor or the protocol is two-phase. Writing archive material to the daemon service's stdout/stderr would be a misleading implementation because it would land in daemon logs or the service manager, not in the invoking agent's pipeline.

There are three coherent choices:

1. First implementation supports `File` for collection and exposes stream targets only for preview or observe.
2. `CollectRemovalCandidates` becomes two-phase: prepare returns archive material, caller writes to stream, commit retracts the exact prepared identifiers.
3. The daemon accepts archive sink file descriptors over the socket, which is much larger than this change.

For production safety, choice 1 is the clean first implementation.

## Proposed Tests

### Contract Tests In `signal-persona-spirit`

1. `collect_removal_candidates_operation_round_trips_with_file_archive_output`

Witness:

```text
(CollectRemovalCandidates (((Any []) None (Exact Zero) Any (Exact Zero) SummaryOnly) (File [/tmp/spirit-archive.nota])))
```

Expected:

- rkyv round-trip preserves the operation;
- NOTA round-trip emits bracket strings and positional records;
- the operation kind is `CollectRemovalCandidates`.

2. `collect_removal_candidates_rejects_legacy_or_flag_like_output_shape`

Witnesses:

- no `--output` style syntax;
- no quoted strings;
- no labeled record fields such as `(target ...)`;
- no boolean "archive true" shape.

Expected:

- NOTA decode fails with the existing structured decode error path.

3. `removal_candidates_collected_reply_carries_compact_records`

The reply should include compact valued material, not identifiers alone. A good reply shape would be closer to:

```text
(RemovalCandidatesCollected ([(1 [intent] Decision [obsolete] Zero Zero)] [] []))
```

Where the vectors are collected summaries, removed identifiers if retained separately, and skipped identifiers or skip records. If the implementation keeps only identifier vectors, add a separate archive receipt type that contains the emitted `RecordSummary` values.

Expected:

- rkyv and NOTA round-trip preserve at least the collected `RecordSummary` values;
- the summary includes privacy and certainty so the archive preserves the visible access/certainty state at collection time.

### Store Tests In `persona-spirit/src/store.rs`

4. `spirit_store_collects_only_exact_zero_candidates`

Setup:

- record 1: certainty `Zero`;
- record 2: certainty `Minimum`;
- record 3: certainty `High`;
- record 4: certainty `Zero`.

Operation:

- collect with the exact-`Zero` candidate query.

Expected:

- archive material contains summaries for records 1 and 4 only;
- records 1 and 4 are gone from normal observation after collection;
- records 2 and 3 remain visible;
- record identifiers are not reused.

5. `spirit_store_rejects_non_zero_collection_query_without_retracting`

Setup as above.

Operations:

- attempt collection with `CertaintySelection::Any`;
- attempt collection with `AtMost Low`;
- attempt collection with `AtLeast Minimum`;
- attempt collection with `Exact Minimum`.

Expected:

- each attempt returns an error or typed rejection;
- every original record remains queryable;
- archive file is absent or empty according to the chosen output policy;
- sema-engine commit sequence does not advance through a retract operation.

This is the main bypass test. Without it, a broad query can make collection a disguised bulk delete.

6. `spirit_store_archive_failure_does_not_retract_candidates`

Setup:

- at least one `Zero` candidate.

Operation:

- collect to a path that cannot be created or written, such as a directory path used as a file target or a path under a missing parent directory if the implementation does not create parents.

Expected:

- operation returns a write/archive failure;
- the `Zero` candidate remains queryable through exact-`Zero` review;
- no `RecordRetracted` trace action is emitted if this is an actor-level test;
- archive material is not partially accepted as success.

7. `spirit_store_partial_archive_failure_retracts_only_successful_records`

Only needed if the implementation writes per-record rather than all-or-nothing.

Setup:

- multiple `Zero` candidates;
- an archive sink fixture that succeeds for the first record and fails on the second.

Expected:

- first record may be retracted only if its archive write was committed before failure;
- failed record remains queryable;
- receipt records collected and skipped separately;
- no candidate without successful archive emission is removed.

If the implementation is all-or-nothing, write the inverse test: any per-record failure retracts none.

### Actor Runtime Tests In `tests/actor_runtime.rs`

8. `persona_spirit_collect_removal_candidates_uses_reader_then_writer_planes`

Setup:

- submit one `Zero` candidate and one `Maximum` record.

Operation:

- submit text or typed request for collection to a file target.

Expected trace:

- `DISPATCH_PHASE`;
- `SIGNAL_EXECUTOR`;
- `RECORD_STORE`;
- `SEMA_READER` before archive emission;
- `SEMA_WRITER` only after successful archive emission;
- `SEMA_OBSERVER`;
- `REPLY_TEXT_ENCODER`.

Expected state:

- archive file contains the `RecordSummary` of the `Zero` record;
- `Observe` after collection returns only the non-Zero record;
- exact-`Zero` observe returns empty.

9. `persona_spirit_collect_removal_candidates_archive_failure_skips_writer_plane`

Setup:

- one `Zero` candidate.

Operation:

- collect to a failing file target.

Expected:

- reply is an error or typed rejection;
- trace contains read-side activity but no `TraceAction::RecordRetracted`;
- subsequent exact-`Zero` query still returns the candidate.

10. `persona_spirit_collect_removal_candidates_does_not_run_as_remove_alias`

Setup:

- one `Maximum` record.

Operation:

- call collection with a broad query if the decoder allows it, or try to create an invalid collection request through typed API.

Expected:

- rejection, not removal;
- record remains queryable;
- trace does not contain `RecordRetracted`.

This test catches the easy bad implementation where collection is written as "observe query, then call remove for every identifier" without candidate certainty gating.

### Boundary CLI Tests In `tests/boundary.rs`

11. `persona_spirit_client_collects_zero_candidates_to_file`

Setup through CLI fixture:

- record one `Zero` candidate, record one non-Zero entry.

Operation:

```text
(CollectRemovalCandidates (((Any []) None (Exact Zero) Any (Exact Zero) SummaryOnly) (File [/tmp/.../archive.nota])))
```

Expected:

- CLI reply is a typed collection receipt;
- archive file contains compact `RecordSummary` material for the `Zero` record;
- normal observation excludes the collected record;
- non-Zero record remains.

12. `persona_spirit_client_collect_file_failure_preserves_candidate`

Setup:

- one `Zero` candidate.

Operation:

- collect to an invalid file target.

Expected:

- CLI surfaces structured failure;
- exact-`Zero` query still returns the candidate;
- invalid archive target does not become a hidden removal path.

13. `persona_spirit_client_standard_output_collection_is_not_unsafe`

This test depends on the design choice.

If stdout/stderr are rejected for first implementation:

- request with `StandardOutput`;
- expect typed rejection;
- candidate remains queryable.

If stdout/stderr are supported through a two-phase CLI protocol:

- archive material appears on the selected stream;
- typed receipt appears on the opposite or explicitly documented stream;
- candidate is retracted only after the stream write succeeds;
- a simulated broken pipe preserves the candidate.

If stdout/stderr are supported by daemon writing to its own streams, the test should fail the design because it cannot prove the invoking caller received archive material.

14. `persona_spirit_client_standard_error_collection_keeps_stdout_parseable`

If `StandardError` is supported, this should prove that ordinary stdout still carries exactly one parseable typed reply. Archive lines must not corrupt the reply stream.

Expected:

- stdout is one NOTA reply;
- stderr contains archive summaries;
- candidate retraction follows only after successful stderr write, or the operation is documented as preview-only.

### Sema Projection Tests In `tests/sema_projection.rs`

15. `spirit_collect_removal_candidates_projects_to_retracted_observation_after_archive`

Expected:

- successful collection projects to `SemaOperation::Retract` and `SemaOutcome::Retracted`;
- the projection is emitted only for the owning collection command, not for each internal per-record removal unless the runtime intentionally publishes one observation per candidate.

16. `spirit_collect_removal_candidates_archive_failure_projects_to_no_change_or_error`

Expected:

- failed archive output does not project as `Retracted`;
- if the reply is a typed failure, projection should be `NoChange` or no successful observation according to current error handling.

## Additional Implementation Review Checks

### Receipt Shape

A receipt should be self-auditing. It should not merely say "removed [1, 2]". It should carry enough material to verify what was archived:

- collected compact summaries;
- skipped identifiers with reasons if possible;
- failed identifiers with reasons if partial failures exist;
- output target or target descriptor;
- mode used, at least `SummaryOnly` versus `WithProvenance`.

If provenance output is implemented, use `RecordProvenance` directly rather than inventing a new text shape.

### Privacy

Default collection query should retain the same default privacy as observation: exact `Zero`. That prevents a casual collection from archiving or removing elevated records. Tests should include a high-privacy `Zero` candidate and prove it is not collected unless the query explicitly widens privacy.

Suggested test:

```text
persona_spirit_collect_default_privacy_does_not_collect_elevated_private_candidates
```

Setup:

- record 1: certainty `Zero`, privacy `Zero`;
- record 2: certainty `Zero`, privacy `High`.

Expected:

- default collection collects record 1 only;
- explicit `(AtLeast High)` or `Any` privacy collection can collect record 2 only if the operation is allowed to target elevated records on the ordinary socket.

This exposes a policy question: because elevated privacy is already on ordinary read path with explicit selection, ordinary collection may be acceptable, but this should be intentional.

### Existing `Remove`

`Remove` remains a hard-delete escape hatch. If `CollectRemovalCandidates` is added but `Remove` stays unchanged, tests still prove the new operation is safe, but they do not stop an agent from bypassing archive policy by calling `Remove` directly.

The architecture should say one of:

- `Remove` remains a manual irreversible operation requiring report tombstone discipline;
- `Remove` is owner-only in a later contract migration;
- `Remove` rejects records that are not already `Zero`.

The last option is a strong safety improvement, but it changes production behavior and should be a separate explicit decision.

## Minimal Green Bar For This Change

The implementation is not complete until these witnesses pass:

1. Contract round-trip for operation, output target, and receipt.
2. Boundary CLI file-target collection: zero candidates archived and removed, non-zero records retained.
3. Archive failure test: no retraction when archive emission fails.
4. Non-Zero bypass test: broad or non-Zero queries cannot remove non-Zero records.
5. Actor trace test: collection is not a `Remove` alias and uses read/archive/write ordering.
6. Sema projection test: success is `Retract`; archive failure is not `Retract`.
7. Privacy default test: elevated private records are not collected by a default open query.

## Best Question For The Main Operator

Should `StandardOutput` and `StandardError` be accepted for actual collection in the first production implementation?

My recommendation is no: support `File` for the first safe `CollectRemovalCandidates` operation, and keep stdout/stderr for a separate preview or report operation until a two-phase collect protocol exists. This preserves the archive-before-retract invariant instead of weakening it around process streams.
