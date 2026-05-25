# 185 — Orchestrate Mirror handover implementation

*Kind: Implementation report · Topic: orchestrate version handover · Date: 2026-05-25 · Lane: second-operator*

## Summary

Implemented the first concrete orchestrate slice from `reports/second-designer/175-upgrade-mechanism-full-design-2026-05-25.md`: an orchestrate-owned Mirror snapshot that travels through `signal-version-handover::MirrorPayload`.

Pushed in `/git/github.com/LiGoldragon/orchestrate` as commit `72105447` (`orchestrate: add version handover mirror snapshot`).

## What changed

- Added `src/handover.rs`.
- Added `MirrorSnapshot`, carrying active `StoredClaim` records and `LaneRegistration` records.
- Added `MirrorVersions`, carrying source and target contract versions for the handover payload.
- Added encode/decode validation:
  - component must be `orchestrate`;
  - record kind must be `MirrorSnapshot`;
  - target contract version must match orchestrate's current version marker;
  - payload bytes must decode as a rkyv `MirrorSnapshot`.
- Added `OrchestrateService::mirror_snapshot`, `mirror_payload`, and `restore_mirror_payload`.
- Added table-level replacement helpers for restoring claims and lanes.
- Added `signal-version-handover` and `version-projection` dependencies.
- Updated `ARCHITECTURE.md` to describe the current Mirror status and the remaining private-upgrade-socket gap.
- Added `tests/handover.rs`, proving a two-service old-to-new mirror transfer and rejection of wrong component, wrong kind, wrong target version, and invalid archive bytes.

## Verification

All checks passed:

- `cargo test --test handover`
- `cargo test`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `nix flake check --option max-jobs 0`

## Current state

Orchestrate can now build and consume the payload body that the private upgrade socket needs to move. The daemon socket itself is not wired yet: no third listener, no `VersionHandover` operation handler, no marker/readiness/completion state machine inside orchestrate.

The implemented slice is still useful because it removes the largest ambiguity from Mirror wiring: the payload is now a typed orchestrate runtime object, not an unspecified byte blob.

## Important design edge

Designer report `/175` describes Mirror for orchestrate as moving in-memory critical state. Current orchestrate stores claims and lanes durably in sema/redb already. I still mirrored those tables because they are the state the report names as critical and because a future in-memory sequencer/cache can use this same snapshot boundary without changing the wire contract.

## Next implementation work

The next complete slice should wire the private upgrade listener in orchestrate daemon:

1. Add an upgrade socket path to daemon configuration or the incoming spawn envelope shape.
2. Bind a `VersionHandover` listener beside ordinary and owner sockets.
3. Handle `Mirror(MirrorPayload)` by decoding/restoring the payload and replying `MirrorAcknowledged`.
4. Handle at least `Divergence` rejection/reporting for schema mismatch.
5. Add daemon-level tests proving ordinary/owner sockets remain public surfaces while the upgrade socket is private handover vocabulary.

## Questions

1. Should orchestrate's Mirror snapshot stay limited to claims + lanes, or should it include dynamic roles too? The current implementation follows `/175`'s named critical state, but dynamic roles are also orchestration policy state.
2. Should the orchestrate current contract version marker be a temporary semantic byte marker, or must the next slice replace it with a schema-derived hash before daemon socket wiring?
3. Should orchestrate handover use the same marker/readiness/completion ceremony as Spirit exactly, or should orchestrate require Mirror before it accepts `ReadyToHandover`?
