# Version Handover Foundation Implementation

## Situation

I refreshed on the latest Spirit/database-upgrade intent and reports before editing. The current canonical shape is:

- `version-projection` owns per-type forward/reverse projection traits and shared version/policy records.
- `signal-version-handover` owns the private upgrade signal contract between two versions of one component.
- `sema-engine` owns the durable commit high-water mark used for replay.
- `sema-upgrade` owns prototype migration/handover orchestration, not production daemon sockets.

Designer's latest update added bead `primary-5w28` for `sema-engine` commit sequencing. I treated that as a prerequisite to the smart Spirit cutover and implemented it in this slice.

## Landed

### version-projection

Repo: `/git/github.com/LiGoldragon/version-projection`

Commit: `69bd2dd0` on `main`

Added a new public library crate with:

- `VersionProjection<Source, Target>` trait.
- `ProjectionError` with `NotRepresentable`, `TransformFailed`, and `DirectionNotImplemented`.
- `ContractVersion([u8; 32])` and `ComponentName`.
- `ComponentPolicy`, `OperationPolicy`, `OperationKind`, `WritePolicy`, `ReadPolicy`, and `SubscribePolicy`.
- Default subscription policy is `TerminateAtHandover`.

This matches the intent that projection is per type and per version pair, while policy is separate from the projection transform itself.

### signal-version-handover

Repo: `/git/github.com/LiGoldragon/signal-version-handover`

Commit: `f2dfe3b4` on `main`

Added a new signal contract crate with operations:

- `AskHandoverMarker`
- `ReadyToHandover`
- `HandoverCompleted`
- `Mirror`
- `Divergence`
- `RecoverFromFailure`

Replies include marker reporting, acceptance, finalization, mirror acknowledgement, divergence acknowledgement, recovery result, and typed rejection.

The crate is signal-only. It does not own runtime sockets, migration code, deployment, or daemon state.

### sema-engine

Repo: `/git/github.com/LiGoldragon/sema-engine`

Commit: `e0a7153c` on `main`

Added `CommitSequence`, a durable per-database monotonic commit counter:

- every successful write transaction advances `CommitSequence`;
- failed commits do not advance it;
- `MutationReceipt` and `CommitReceipt` carry the committed sequence;
- `CommitLogEntry` carries `commit_sequence`;
- `Engine::current_commit_sequence()` returns the current high-water mark;
- `Engine::replay_from_sequence(start)` returns commit-log entries by commit sequence.

Snapshots remain intact. Existing snapshot-based subscription replay still works. Commit sequence is now the handover high-water mark.

### sema-upgrade

Repo: `/git/github.com/LiGoldragon/sema-upgrade`

Commits:

- `060982d0` on `main`: adds handover prototype.
- `677206d5` on `main`: repins to the new `sema-engine` commit-sequence support.

Added `src/handover.rs`, a testable prototype state machine over the new handover contract:

- current endpoint starts public;
- next endpoint is prepared separately;
- `ReadyToHandover` rejects if the marker moved;
- successful handover flips active traffic to next and leaves current private-upgrade-only;
- mirror uses `VersionProjection`;
- nonrepresentable reverse projection records typed `Divergence`.

This is not yet production Spirit daemon wiring. It is the executable protocol witness that the production wiring should now follow.

## Tests

All Nix checks used the remote builder with `--option max-jobs 0`.

Passed:

- `version-projection`: `nix flake check --option max-jobs 0 -L`
- `signal-version-handover`: `nix flake check --option max-jobs 0 -L`
- `sema-engine`: `nix flake check --option max-jobs 0 -L`
- `sema-upgrade`: `nix flake check --option max-jobs 0 -L`

The sema-engine Nix run includes the new tests proving sequence monotonicity, persistence across reopen, no advancement on failed commit, and replay from sequence.

The sema-upgrade Nix run includes the handover prototype tests proving state flip, stale marker rejection, representable mirror, nonrepresentable divergence, and integration against the updated sema-engine.

## Beads

Closed:

- `primary-la7q` (per-type migration trait for component cutovers): projection trait and sema-upgrade prototype landed.
- `primary-5w28` (sema-engine commit sequence): commit sequence API, replay API, and persistence tests landed.

Updated:

- `primary-x3ci` (Spirit v0.1.1 cutover): foundation stack advanced; remaining production cutover prerequisites listed there.

## Remaining Work

The true zero-downtime Spirit cutover is not done yet. The remaining chain is:

1. Retrofit `persona-spirit` v0.1.0 with private upgrade protocol code while keeping its database schema stable.
2. Re-tag and redeploy that v0.1.0 protocol-aware daemon as production.
3. Build v0.1.1 with the same protocol plus the `Magnitude` schema.
4. Add production private upgrade sockets and listening loops.
5. Add active-version selector flip in CriomOS-home or the deployment layer.
6. Use `sema-engine` `CommitSequence` to copy at sequence N and replay from N+1.

Open design pressure still visible:

- Mirror payload is currently raw bytes in `signal-version-handover`. This is adequate for the foundation tests, but `/285` still leaves the raw-bytes vs typed-enum shape open for production.
- Read semantics during handover are not yet implemented. The prototype only covers write handover and mirror/divergence.
- Failure logs are local in the prototype. Persona-introspect integration can stay deferred for the first cutover.
