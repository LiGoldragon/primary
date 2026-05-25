# 186 - orchestrate upgrade socket implementation

*Kind: Implementation report. Topic: orchestrate private upgrade socket and Mirror wire path. Date: 2026-05-25. Lane: second-operator.*

## Frame

Inputs used:

- `reports/operator/178-primary-wdl6-spirit-v0-1-0-protocol-build-2026-05-25.md`
- `reports/designer/333-upgrade-mechanism-full-design-explained.md`
- Existing orchestrate Mirror payload report: `reports/second-operator/185-orchestrate-mirror-handover-implementation-2026-05-25.md`

The corrected operator reference made Spirit v0.1.0.1 the maturity model: bind the private upgrade socket and serve `signal-version-handover` marker/readiness/completion frames. Designer `/333` clarified the orchestrate-specific phase ordering: orchestrate Mirror is not a post-completion payload; it belongs in the marker-to-readiness window because orchestrate has critical state to transfer before final handover.

## Implemented

Repository: `/git/github.com/LiGoldragon/orchestrate`

Changed files:

- `ARCHITECTURE.md`
- `Cargo.lock`
- `src/configuration.rs`
- `src/daemon.rs`
- `src/handover.rs`
- `src/service.rs`
- `src/tables.rs`
- `tests/daemon_cli.rs`

Implemented behavior:

- `DaemonConfiguration` now carries `upgrade_socket_path`.
- `OrchestrateDaemon` now binds three sockets: ordinary, owner, private upgrade.
- The upgrade socket decodes `signal-version-handover::Frame`, validates `ShortHeader` against the decoded upgrade operation root, dispatches to `OrchestrateService`, and replies with the same contract frame shape.
- `AskHandoverMarker` returns an orchestrate marker using `MirrorSnapshot::current_contract_version()` and `sema-engine::Engine::current_commit_sequence()`.
- `ReadyToHandover` accepts only when the current commit sequence still matches the source marker.
- `HandoverCompleted` finalizes only after readiness and removes the ordinary/owner socket paths.
- `Mirror` restores an orchestrate `MirrorSnapshot` in the marker-to-readiness window and rejects invalid component/kind/target/archive payloads as `SchemaMismatch`.
- `Divergence` and `RecoverFromFailure` are minimally wired so every protocol operation has a typed response.
- Architecture text now reflects the three-socket runtime and the Mirror-before-readiness rule.

## Tests Added

New daemon-level coverage in `tests/daemon_cli.rs`:

- Upgrade socket serves marker/readiness/completion and retires ordinary/owner socket paths.
- Upgrade socket accepts Mirror before readiness, persists claims and lanes, finalizes, then the store is reopened to prove the snapshot landed.
- Upgrade socket rejects wrong-target Mirror payloads with typed schema mismatch.
- Upgrade socket rejects ordinary contract frames.

Existing service-level Mirror tests remain in `tests/handover.rs`.

## Verification

Passed:

- `cargo test --test daemon_cli`
- `cargo test`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `nix flake check --option max-jobs 0`

The Nix check used the remote builder and passed all flake checks.

## Remaining Gaps

1. `Divergence` is only acknowledged with identifier `0`; there is not yet a durable upgrade-divergence ledger for protocol-level handover divergence.
2. `RecoverFromFailure` resets only the in-process handover state. A real supervisor-driven recovery flow still belongs with persona-daemon.
3. Public socket retirement removes ordinary/owner socket paths after completion, but the listener threads still exist until the process exits. This is enough to make new path-based connects fail, but a final production shape should explicitly drain and terminate the old daemon.
4. The marker uses `sema-engine::current_commit_sequence`, but many existing orchestrate table writes still go through direct storage-kernel writes. The marker is now structurally correct, but sequence fidelity depends on continuing the migration toward sema-engine mutation paths.

## Questions

1. Should protocol-level `Divergence` records reuse orchestrate's existing `divergences` table, or should version handover get its own small durable table keyed by handover failure identifier?
2. After `HandoverCompleted`, should orchestrate immediately exit the old daemon process, or should persona-daemon always be the only component that kills it?
