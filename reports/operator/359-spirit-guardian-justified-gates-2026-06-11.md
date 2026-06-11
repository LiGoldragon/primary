# Spirit Guardian Justified Gates

## Context

This operator slice resumed the Spirit guardian branch after deployed main moved
forward. The branch was already based on the deployed main commit, so the work
continued from the current production baseline rather than from a stale pre-deploy
base.

Designer reports 584, 585, and 586 were the active design inputs:

- The guardian judges semantic admission, not deterministic code.
- The decision journal is Spirit-owned and separate from the live intent store.
- Every state-changing public write must carry or derive the psyche statement
  and context the guardian judges against.
- Runtime referents are registry data guarded by a referent-specific verdict,
  while domain remains schema vocabulary.

## Implemented Shape

Spirit branch commit: `6b599aa5` (`spirit: gate justified guardian mutations`).

Spirit is bumped to `0.9.0` because the public Signal contract changed.

Signal now carries explicit justification on public write operations:

- `Record RecordRequest`
- `Propose Proposal`
- `Clarify Clarification`
- `Supersede Supersession`
- `Retire Retirement`
- `Remove Removal`
- `ChangeRecord RecordChange`
- `RegisterReferent ReferentRegistration`
- `CollectRemovalCandidates RemovalCandidateCollection`

`RecordRequest`, `Proposal`, `Removal`, `RecordChange`,
`ReferentRegistration`, `Clarification`, `Supersession`, `Retirement`, and
`RemovalCandidateCollection` all include a `Justification`. `State` derives its
`RecordRequest` justification from the original statement.

Nexus now exposes guardian effect verbs for mutation paths that were still direct:

- `GuardRecord`
- `Propose`
- `Clarify`
- `Supersede`
- `Retire`
- `GuardRemove`
- `GuardChangeRecord`
- `GuardReferentRegistration`
- `CollectRemovalCandidates`

With `agent-guardian`, public remove and record replacement route through the
guardian before SEMA writes. Bulk removal candidate collection also asks the
guardian before archiving/removing matched candidates.

The referent path is separately guarded:

- `ReferentGuardianVerdict [Accept (RejectReferent)]`
- `ReferentGuardianRejectionReason`
- `ReferentGuardianRejected`
- decision journal entries for referent verdicts

The model prompt remains a typed NOTA verdict request with temperature `0`. The
agent component already owns provider/model dispatch; Spirit passes provider and
model configuration through the existing guardian agent configuration.

## Decision Journal

The guardian journal now stores two decision kinds in the sidecar DB:

- record-operation decisions with the operation, retrieved record bundle,
  verdict, and database marker
- referent-registration decisions with the registration, registered referent
  bundle, verdict, and database marker

This keeps the live intent store lean and puts the training flywheel in a
separate append-only Spirit-owned database.

## Test And Build Results

Passed locally:

- `cargo test --features agent-guardian,nota-text`
- `cargo test`
- `cargo test --features testing-trace --test instrumentation_logging`
- `cargo clippy --features agent-guardian,nota-text -- -D warnings`

Passed through Nix:

- `nix flake check`

The flake check built and tested the `0.9.0` package set on the remote builder
and ended with `all checks passed`.

## Remaining Deployment Boundary

This branch is code-ready, but not deployed in this slice. Deployment still
needs operator or system-operator integration into the live pin and service
activation after the branch lands.

The active production daemon remains whatever is pinned in CriomOS until that
deployment step happens.
