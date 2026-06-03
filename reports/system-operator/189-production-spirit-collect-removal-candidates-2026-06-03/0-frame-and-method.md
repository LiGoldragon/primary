# Production Spirit Collect Removal Candidates

## Frame

This meta-report frames the Production Spirit implementation of an
explicit operation that collects reviewed removal candidates.

Load-bearing psyche intent captured before implementation:

- [Production Spirit should implement an explicit collect-removal-candidates operation that archives or emits reviewed Zero-certainty records before retracting them from the hot store.]
- [Spirit removal-candidate collection should support an explicit output target for archive material, such as a file path or process stream, so another component can preserve the compact valued representation before hot-store removal.]
- [Common Spirit operations should have short default forms that lower to the full data types, so agents do not have to compose every rarely-configured field for routine calls.]

Prior report:

- `reports/system-operator/188-component-data-archival-and-garbage-collection-2026-06-03.md` established the field pattern: nomination, tombstone/soft-delete, archive or lower tier, collect, compact, optional purge.

## Working Interpretation

`Zero` certainty remains a reversible candidate marker. It is not
itself deletion.

`CollectRemovalCandidates` is an explicit operation. It selects
records through a `RecordQuery`, emits archive material to a declared
target, then retracts only the records whose archive emission
succeeded.

The first production implementation should stay inside the existing
ordinary Spirit contract because `Remove` is already ordinary
intent-store maintenance in `signal-persona-spirit`. This can be
revisited for owner-only policy later, but production parity and local
ergonomics are better served by landing beside `Remove` and
`ChangeCertainty`.

## Proposed Contract Shape

The ordinary contract gains:

```nota
(CollectRemovalCandidates
  (<RecordQuery>
   <ArchiveOutput>))
```

`ArchiveOutput` is a closed enum, not flags:

```nota
StandardOutput
StandardError
(File <ArchivePath>)
```

The reply is a typed receipt:

```nota
(RemovalCandidatesCollected
  ([<RecordIdentifier> ...]
   [<RecordIdentifier> ...]
   [<RecordIdentifier> ...]))
```

The three vectors are archived, removed, and skipped identifiers.
Skipped exists because archive emission can fail or a matching record
can become ineligible when collection runs.

The first implementation may keep archive material as compact
`SummaryOnly` lines because that is the "small valued" representation
the psyche asked for. It should be straightforward to extend the target
to provenance-rich output once Arca or another archive component is
ready.

## Implementation Plan

1. Update `signal-persona-spirit` with the new request/reply payloads,
   NOTA/rkyv derives, canonical examples, and round-trip tests.
2. Update `persona-spirit` command lowering so the contract operation
   becomes one local command and projects to SEMA `Retract`.
3. Add store/query support that selects `Exact Zero` candidates through
   the existing read path, writes compact archive records to the target,
   retracts successful records through the existing write path, and
   returns the typed receipt.
4. Add actor-runtime and boundary tests proving archive-before-retract,
   skipped-on-archive-failure, exact-Zero filtering, and no removal of
   non-Zero records.
5. Update repo `INTENT.md` and `ARCHITECTURE.md` surfaces in both repos.
6. Update workspace skills only if the live command surface changes
   enough that agents need the new invocation syntax.

## Constraints

- No silent background GC.
- No collection without archive emission or archive receipt.
- No hard removal of non-Zero records through this operation.
- No shell flags; the output target is data in the NOTA request.
- No direct database opening from the CLI.
- No free functions in production Rust.
- No ZST namespace types.
- No hand-rolled parser for output paths or request text.
- Do not use `/nix/store` filesystem search.

## Subagent Work

The main system-operator keeps implementation ownership on the critical
path.

Sidecar subagents are non-blocking and disjoint:

- `1-contract-shape-review.md` — review the proposed ordinary-contract
  shape against `signal-persona-spirit` naming, NOTA, rkyv, and tests.
- `2-archive-policy-and-test-review.md` — review archive-before-retract
  policy and propose concrete tests that catch dangerous bypasses.

The synthesis file will be added after implementation and sidecar review.
